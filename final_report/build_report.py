#!/usr/bin/env python3
"""
build_report.py: compile the final MPG 118S report.

Takes the project compiler's document (preserved text and structure), adds the missing and updated chapters
(Executive summary, Problem definition, Assumptions, Mass balance, Electrical analysis, Detailed calculations,
Sensitivity analysis, References), then applies one consistent format: Arial 12 black text, 1.5 line spacing,
simple clean tables, no em dashes, table of contents with lists of tables and figures.

Usage: python3 build_report.py <compiler.docx> <out.docx>
"""
import copy
import io
import os
import random
import re
import subprocess
import sys
import tempfile

import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt
from docx.text.paragraph import Paragraph
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "md")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
COVER_TRIM = 14
TEXT_W = 9026  # A4 with 1 inch margins, in twips
NS = {"w": W, "m": M, "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture"}


def xp(el, path):
    return etree.ElementBase.xpath(el, path, namespaces=NS)

# ---------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------


def q(tag):
    return qn(tag)


def para_text(p):
    return "".join(t.text or "" for t in p.iter(q("w:t")))


def style_of(p):
    ps = p.find(q("w:pPr") + "/" + q("w:pStyle"))
    return ps.get(q("w:val")) if ps is not None else None


def is_heading(p, lvl=None):
    s = style_of(p)
    if s is None or not s.startswith("Heading"):
        return False
    return lvl is None or s == f"Heading{lvl}"


def in_table(el):
    a = el.getparent()
    while a is not None:
        if a.tag == q("w:tc"):
            return True
        a = a.getparent()
    return False


def in_math(el):
    a = el.getparent()
    while a is not None:
        if a.tag in (q("m:oMath"), q("m:oMathPara")):
            return True
        a = a.getparent()
    return False


def pandoc_fragment(md_file, reference, out):
    txt = open(md_file, encoding="utf8").read()
    txt = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", "\u00a0", txt)  # keep thousands groups together
    tmp_md = out.replace(".docx", "_nbsp.md")
    open(tmp_md, "w", encoding="utf8").write(txt)
    subprocess.run(
        ["pandoc", tmp_md, "-f", "markdown-tex_math_dollars-implicit_figures", "-t", "docx",
         "--shift-heading-level-by=1", "--reference-doc", reference, "--resource-path", os.path.dirname(os.path.abspath(md_file)),
         "-o", out], check=True)


# ---------------------------------------------------------------------------------------------------
# merging fragments into the compiler's document
# ---------------------------------------------------------------------------------------------------


def merge_numbering(doc, fdoc, orig_nums):
    """Copy the list definitions that pandoc added (numIds not in the compiler's file) into the main numbering part."""
    try:
        fnum = fdoc.part.numbering_part.element
    except Exception:
        return {}
    mnum = doc.part.numbering_part.element
    abs_ids = [int(a.get(q("w:abstractNumId"))) for a in mnum.findall(q("w:abstractNum"))]
    num_ids = [int(n.get(q("w:numId"))) for n in mnum.findall(q("w:num"))]
    next_abs = max(abs_ids or [0]) + 1
    next_num = max(num_ids or [0]) + 1
    amap, nmap = {}, {}
    first_num = mnum.find(q("w:num"))
    tail = mnum.find(q("w:numIdMacAtCleanup"))
    fabs = {int(a.get(q("w:abstractNumId"))): a for a in fnum.findall(q("w:abstractNum"))}
    for n in fnum.findall(q("w:num")):
        old = int(n.get(q("w:numId")))
        if old in orig_nums:
            continue
        nn = copy.deepcopy(n)
        ab = nn.find(q("w:abstractNumId"))
        old_abs = int(ab.get(q("w:val")))
        if old_abs not in amap:
            na = copy.deepcopy(fabs[old_abs])
            na.set(q("w:abstractNumId"), str(next_abs))
            nsid = na.find(q("w:nsid"))
            if nsid is not None:
                nsid.set(q("w:val"), "%08X" % random.randint(0x10000000, 0x7FFFFFFF))
            amap[old_abs] = next_abs
            next_abs += 1
            first_num.addprevious(na)
        nn.set(q("w:numId"), str(next_num))
        ab.set(q("w:val"), str(amap[old_abs]))
        nmap[old] = next_num
        next_num += 1
        (tail.addprevious(nn) if tail is not None else mnum.append(nn))
    return nmap


def fragment_elements(doc, md_name, reference, tmpdir, orig_nums):
    """Run pandoc on a markdown file and return deep-copied body elements ready for insertion into doc."""
    out = os.path.join(tmpdir, md_name.replace(".md", ".docx"))
    pandoc_fragment(os.path.join(MD, md_name), reference, out)
    fdoc = docx.Document(out)
    nmap = merge_numbering(doc, fdoc, orig_nums)
    existing_ids = [int(x) for x in xp(doc.element.body, "//wp:docPr/@id")]
    next_id = max(existing_ids or [0]) + 1
    elems = []
    for child in list(fdoc.element.body):
        if child.tag in (q("w:sectPr"), q("w:bookmarkStart"), q("w:bookmarkEnd")):
            continue
        el = copy.deepcopy(child)
        for bm in xp(el, ".//w:bookmarkStart | .//w:bookmarkEnd"):
            bm.getparent().remove(bm)
        for n in xp(el, ".//w:numPr/w:numId"):
            v = int(n.get(q("w:val")))
            if v in nmap:
                n.set(q("w:val"), str(nmap[v]))
        for blip in xp(el, ".//a:blip"):
            rid = blip.get(q("r:embed"))
            blob = fdoc.part.related_parts[rid].blob
            new_rid, _ = doc.part.get_or_add_image(io.BytesIO(blob))
            blip.set(q("r:embed"), new_rid)
        for dp in xp(el, ".//wp:docPr"):
            dp.set("id", str(next_id))
            next_id += 1
        for rs in xp(el, ".//w:rStyle"):
            if rs.get(q("w:val")) == "VerbatimChar":
                rs.getparent().remove(rs)
        elems.append(el)
    return elems


def find_h1(body, title):
    for p in body.iterchildren(q("w:p")):
        if is_heading(p, 1) and re.sub(r"\s+", " ", para_text(p)).strip().upper() == title.upper():
            return p
    raise KeyError(title)


def insert_after(anchor, elems):
    ptr = anchor
    for el in elems:
        ptr.addnext(el)
        ptr = el
    return ptr


def clear_between(body, start_h1, end_h1=None):
    """Remove all body elements after start_h1 up to (not including) end_h1 (or the final sectPr)."""
    el = start_h1.getnext()
    while el is not None and el is not end_h1 and el.tag != q("w:sectPr"):
        nxt = el.getnext()
        body.remove(el)
        el = nxt


# ---------------------------------------------------------------------------------------------------
# text fixes
# ---------------------------------------------------------------------------------------------------


def replace_text(body, old, new, count_expected=None):
    n = 0
    for p in body.iter(q("w:p")):
        if old not in para_text(p):
            continue
        done = False
        for t in p.iter(q("w:t")):
            if t.text and old in t.text:
                t.text = t.text.replace(old, new)
                n += 1
                done = True
        if not done:  # text split over runs: rebuild in the first run
            ts = list(p.iter(q("w:t")))
            full = "".join(t.text or "" for t in ts).replace(old, new)
            ts[0].text = full
            ts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            for t in ts[1:]:
                t.text = ""
            n += 1
    if count_expected is not None and n != count_expected:
        print(f"  note: '{old[:30]}' replaced {n} times (expected {count_expected})")
    return n


def fix_dashes(body):
    n = 0
    for t in body.iter(q("w:t")):
        if t.text and any(c in t.text for c in "—―"):
            t.text = re.sub(r"\s*[—―]\s*", ", ", t.text)
            n += 1
        if t.text and "--" in t.text:
            t.text = re.sub(r"(?<=\d)--(?=\d)", "-", t.text)
            t.text = re.sub(r"\s*--\s*", ", ", t.text)
            n += 1
        if t.text and "–" in t.text:
            t.text = re.sub(r"(?<=\d)–(?=\d)", "-", t.text)
            t.text = re.sub(r"\s–\s", ", ", t.text)
            t.text = t.text.replace("–", "-")
            n += 1
    return n


# ---------------------------------------------------------------------------------------------------
# styles and numbering
# ---------------------------------------------------------------------------------------------------


def black_arial_styles(doc):
    st = doc.styles.element
    dd = st.find(q("w:docDefaults"))
    rpr = dd.find(q("w:rPrDefault")).find(q("w:rPr"))
    for ch in list(rpr):
        if ch.tag in (q("w:rFonts"), q("w:sz"), q("w:szCs"), q("w:color")):
            rpr.remove(ch)
    rf = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Arial"/>')
    rpr.insert(0, rf)
    rpr.append(parse_xml(f'<w:color {nsdecls("w")} w:val="000000"/>'))
    rpr.append(parse_xml(f'<w:sz {nsdecls("w")} w:val="24"/>'))
    rpr.append(parse_xml(f'<w:szCs {nsdecls("w")} w:val="24"/>'))
    # canonical order inside rPr: rFonts, color, sz, szCs, then the rest (lang)
    order = {q("w:rFonts"): 0, q("w:color"): 1, q("w:sz"): 2, q("w:szCs"): 3}
    kids = sorted(list(rpr), key=lambda e: order.get(e.tag, 9))
    for k in kids:
        rpr.remove(k)
    for k in kids:
        rpr.append(k)
    ppd = dd.find(q("w:pPrDefault"))
    if ppd is not None:
        ppr = ppd.find(q("w:pPr"))
        if ppr is None:
            ppr = OxmlElement("w:pPr")
            ppd.append(ppr)
        for ch in list(ppr):
            if ch.tag == q("w:spacing"):
                ppr.remove(ch)
        ppr.append(parse_xml(f'<w:spacing {nsdecls("w")} w:after="120" w:line="360" w:lineRule="auto"/>'))

    keep_size = {"Heading1": 28, "Heading2": 24, "Heading3": 24, "Title": None, "Caption": 20, "TableCaption": 20,
                 "FigureCaption": 20, "TableNote": 18, "ImageCaption": 20, "Footer": 20, "Header": 20,
                 "TOC1": 22, "TOC2": 22, "TableofFigures": 22, "TOCHeading": 28}
    for s in st.findall(q("w:style")):
        sid = s.get(q("w:styleId"))
        if s.get(q("w:type")) not in ("paragraph", "character"):
            continue
        rp = s.find(q("w:rPr"))
        if rp is None:
            continue
        for ch in list(rp):
            if ch.tag == q("w:color"):
                rp.remove(ch)
            elif ch.tag == q("w:rFonts") and s.get(q("w:type")) == "paragraph":
                rp.remove(ch)
            elif ch.tag in (q("w:sz"), q("w:szCs")) and sid not in keep_size:
                rp.remove(ch)
        if sid in ("Caption", "TableCaption", "FigureCaption", "ImageCaption"):
            for ch in list(rp):
                if ch.tag in (q("w:i"), q("w:iCs")):
                    rp.remove(ch)
            for ch in list(rp):
                if ch.tag in (q("w:sz"), q("w:szCs")):
                    ch.set(q("w:val"), "20")
        # drop emptied rPr
        if len(rp) == 0:
            s.remove(rp)

    def set_style(sid, ppr_xml=None, rpr_xml=None):
        s = xp(st, f'w:style[@w:styleId="{sid}"]')
        if not s:
            return
        s = s[0]
        if ppr_xml is not None:
            old = s.find(q("w:pPr"))
            new = parse_xml(f'<w:pPr {nsdecls("w")}>{ppr_xml}</w:pPr>')
            if old is not None:
                s.replace(old, new)
            else:
                nxt = s.find(q("w:rPr"))
                (nxt.addprevious(new) if nxt is not None else s.append(new))
        if rpr_xml is not None:
            old = s.find(q("w:rPr"))
            new = parse_xml(f'<w:rPr {nsdecls("w")}>{rpr_xml}</w:rPr>')
            if old is not None:
                s.replace(old, new)
            else:
                s.append(new)

    # headings (numbering stays attached through numPr in the heading styles)
    set_style("Heading1",
              '<w:keepNext/><w:keepLines/><w:pageBreakBefore/><w:numPr><w:numId w:val="1"/></w:numPr>'
              '<w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="0"/>',
              '<w:b/><w:bCs/><w:caps/><w:sz w:val="28"/><w:szCs w:val="28"/>')
    set_style("Heading2",
              '<w:keepNext/><w:keepLines/><w:numPr><w:ilvl w:val="1"/><w:numId w:val="1"/></w:numPr>'
              '<w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="1"/>',
              '<w:b/><w:bCs/><w:caps/><w:sz w:val="24"/><w:szCs w:val="24"/>')
    set_style("Heading3",
              '<w:keepNext/><w:keepLines/><w:numPr><w:ilvl w:val="2"/><w:numId w:val="1"/></w:numPr>'
              '<w:spacing w:before="200" w:after="100" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="2"/>',
              '<w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/>')
    set_style("TableCaption", '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="80" w:line="240" w:lineRule="auto"/>',
              '<w:b/><w:bCs/><w:sz w:val="20"/><w:szCs w:val="20"/>')
    set_style("FigureCaption", '<w:keepLines/><w:spacing w:before="80" w:after="240" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
              '<w:b/><w:bCs/><w:sz w:val="20"/><w:szCs w:val="20"/>')
    set_style("Reference", '<w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:left="567" w:hanging="567"/><w:jc w:val="both"/>')
    set_style("TableNote", '<w:spacing w:before="60" w:after="200" w:line="240" w:lineRule="auto"/>',
              '<w:sz w:val="18"/><w:szCs w:val="18"/>')
    set_style("Compact", '<w:spacing w:before="0" w:after="60" w:line="360" w:lineRule="auto"/>')
    set_style("BodyText", '<w:spacing w:before="0" w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/>')

    # new styles for the contents pages
    def add_style(xml):
        sid = re.search(r'w:styleId="([^"]+)"', xml).group(1)
        for old in xp(st, f'w:style[@w:styleId="{sid}"]'):
            st.remove(old)
        st.append(parse_xml(xml))

    add_style(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="left" w:pos="567"/>'
              '<w:tab w:val="right" w:leader="dot" w:pos="9016"/></w:tabs><w:spacing w:before="120" w:after="0" w:line="240" w:lineRule="auto"/>'
              '</w:pPr><w:rPr><w:b/><w:bCs/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>')
    add_style(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="left" w:pos="1418"/>'
              '<w:tab w:val="right" w:leader="dot" w:pos="9016"/></w:tabs><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
              '<w:ind w:left="567"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>')
    add_style(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="TableofFigures"><w:name w:val="table of figures"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs>'
              '<w:tab w:val="right" w:leader="dot" w:pos="9016"/></w:tabs><w:spacing w:before="0" w:after="60" w:line="240" w:lineRule="auto"/>'
              '<w:ind w:left="1134" w:hanging="1134"/></w:pPr><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>')
    add_style(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="AppendixHeading"><w:name w:val="Appendix Heading"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/></w:pPr>'
              '<w:rPr><w:b/><w:bCs/></w:rPr></w:style>')
    add_style(f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="TOCHeading"><w:name w:val="TOC Heading"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="0" w:after="240" '
              'w:line="360" w:lineRule="auto"/></w:pPr><w:rPr><w:b/><w:bCs/><w:caps/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>')


def fix_numbering(doc):
    num = doc.part.numbering_part.element
    for a in num.findall(q("w:abstractNum")):
        # black list symbols
        for c in a.iter(q("w:color")):
            c.getparent().remove(c)
    a5 = None
    for n in num.findall(q("w:num")):
        if n.get(q("w:numId")) == "1":
            a5 = n.find(q("w:abstractNumId")).get(q("w:val"))
    for a in num.findall(q("w:abstractNum")):
        if a.get(q("w:abstractNumId")) == a5:
            for lvl in a.findall(q("w:lvl")):
                il = int(lvl.get(q("w:ilvl")))
                txt = lvl.find(q("w:lvlText"))
                ind = lvl.find(q("w:pPr") + "/" + q("w:ind"))
                if il == 0:
                    txt.set(q("w:val"), "%1.")
                    ind.set(q("w:left"), "567"); ind.set(q("w:hanging"), "567")
                elif il == 1:
                    txt.set(q("w:val"), "%1.%2")
                    ind.set(q("w:left"), "720"); ind.set(q("w:hanging"), "720")
                elif il == 2:
                    txt.set(q("w:val"), "%1.%2.%3")
                    ind.set(q("w:left"), "851"); ind.set(q("w:hanging"), "851")


# ---------------------------------------------------------------------------------------------------
# paragraph, run, table and figure normalisation
# ---------------------------------------------------------------------------------------------------
STRIP_RUN = (q("w:rFonts"), q("w:sz"), q("w:szCs"), q("w:color"), q("w:highlight"), q("w:shd"))

# w:rPr child order (subset used here)
RPR_ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline", "shadow",
             "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing", "w", "kern",
             "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs",
             "em", "lang", "eastAsianLayout", "specVanish", "oMath"]


def sort_rpr(rpr):
    kids = list(rpr)
    kids.sort(key=lambda e: RPR_ORDER.index(etree.QName(e).localname) if etree.QName(e).localname in RPR_ORDER else 99)
    for k in kids:
        rpr.remove(k)
    for k in kids:
        rpr.append(k)


def clean_rpr(rpr, size=None, bold=None):
    for ch in list(rpr):
        if ch.tag in STRIP_RUN:
            rpr.remove(ch)
    if size is not None:
        rpr.append(parse_xml(f'<w:sz {nsdecls("w")} w:val="{size}"/>'))
        rpr.append(parse_xml(f'<w:szCs {nsdecls("w")} w:val="{size}"/>'))
    if bold:
        if rpr.find(q("w:b")) is None:
            rpr.append(parse_xml(f'<w:b {nsdecls("w")}/>'))
    sort_rpr(rpr)


def normalise_runs(p, size=None, bold=None):
    ppr = p.find(q("w:pPr"))
    if ppr is not None:
        prp = ppr.find(q("w:rPr"))
        if prp is not None:
            clean_rpr(prp, size, bold)
    for r in p.iter(q("w:r")):
        if in_math(r) or r.tag.startswith("{" + M):
            continue
        rpr = r.find(q("w:rPr"))
        if rpr is None:
            if size is None and not bold:
                continue
            rpr = OxmlElement("w:rPr")
            r.insert(0, rpr)
        clean_rpr(rpr, size, bold)
        if len(rpr) == 0:
            r.remove(rpr)


def set_ppr(p, line=None, before=None, after=None, jc=None, keep_next=None, drop_ind=False, drop_tabs=False):
    para = Paragraph(p, None)
    pf = para.paragraph_format
    if line is not None:
        pf.line_spacing = line
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if keep_next is not None:
        pf.keep_with_next = keep_next
    ppr = p.find(q("w:pPr"))
    if ppr is not None:
        if drop_ind:
            for e in ppr.findall(q("w:ind")):
                ppr.remove(e)
        if drop_tabs:
            for e in ppr.findall(q("w:tabs")):
                ppr.remove(e)
    if jc is not None:
        from docx.enum.text import WD_ALIGN_PARAGRAPH as A
        pf.alignment = {"both": A.JUSTIFY, "left": A.LEFT, "center": A.CENTER, "right": A.RIGHT}[jc]


PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr", "suppressLineNumbers",
             "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
             "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents",
             "suppressOverlap", "jc", "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle",
             "rPr", "sectPr", "pPrChange"]


def sort_all_ppr(body):
    for ppr in body.iter(q("w:pPr")):
        kids = list(ppr)
        kids.sort(key=lambda e: PPR_ORDER.index(etree.QName(e).localname) if etree.QName(e).localname in PPR_ORDER else 99)
        for k in kids:
            ppr.remove(k)
        for k in kids:
            ppr.append(k)


def current_jc(p):
    j = p.find(q("w:pPr") + "/" + q("w:jc"))
    return j.get(q("w:val")) if j is not None else None


CAP_RE = re.compile(r"^\s*(Table|Figure)\s+((?:\d+|[A-D])\.\d+)\s*(:|\.)?\s*([A-Z(À-ſ].*)$", re.S)


def caption_kind(p):
    if in_table(p):
        return None
    t = re.sub(r"\s+", " ", para_text(p)).strip()
    if len(t) > 260 or not t:
        return None
    m = CAP_RE.match(t)
    if not m:
        return None
    return m.group(1)


def set_pstyle(p, style_id):
    ppr = p.find(q("w:pPr"))
    if ppr is None:
        ppr = OxmlElement("w:pPr")
        p.insert(0, ppr)
    ps = ppr.find(q("w:pStyle"))
    if ps is None:
        ps = OxmlElement("w:pStyle")
        ppr.insert(0, ps)
    ps.set(q("w:val"), style_id)


def normalise_body(doc, cover_end_el):
    body = doc.element.body
    # captions: unify the style
    for p in body.iter(q("w:p")):
        if p is cover_end_el:
            pass
    children = list(body)
    cover = True
    prev_was_table = False
    for el in children:
        if el is cover_end_el:
            cover = False
    # work through all paragraphs (including those in tables)
    reached = False
    for p in body.iter(q("w:p")):
        if p is cover_end_el:
            reached = True
        if not reached:
            continue
        if in_table(p):
            continue
        k = caption_kind(p)
        if k == "Table":
            set_pstyle(p, "TableCaption")
        elif k == "Figure":
            set_pstyle(p, "FigureCaption")

    def numbered(p):
        return p.find(q("w:pPr") + "/" + q("w:numPr")) is not None

    reached = False
    for p in list(body.iter(q("w:p"))):
        if p is cover_end_el:
            reached = True
        if not reached or in_table(p):
            continue
        sid = style_of(p)
        has_draw = bool(xp(p, ".//w:drawing"))
        has_math = bool(xp(p, ".//m:oMath"))
        if sid in ("Heading1", "Heading2", "Heading3"):
            normalise_runs(p)
            # direct spacing/justification off so the style governs
            ppr = p.find(q("w:pPr"))
            for e in list(ppr):
                if e.tag in (q("w:spacing"), q("w:jc"), q("w:ind"), q("w:tabs")):
                    ppr.remove(e)
            continue
        if sid == "AppendixHeading":
            normalise_runs(p)
            ppr = p.find(q("w:pPr"))
            for e in list(ppr):
                if e.tag in (q("w:spacing"), q("w:jc"), q("w:ind"), q("w:tabs")):
                    ppr.remove(e)
            continue
        if sid in ("TableCaption", "FigureCaption"):
            normalise_runs(p, size=20, bold=True)
            ppr = p.find(q("w:pPr"))
            for e in list(ppr):
                if e.tag in (q("w:spacing"), q("w:ind"), q("w:tabs")):
                    ppr.remove(e)
            if sid == "TableCaption":
                set_ppr(p, jc="left")
            else:
                set_ppr(p, jc="center")
            continue
        if sid == "Reference":
            normalise_runs(p)
            continue
        if sid == "TableNote":
            normalise_runs(p, size=18)
            continue
        normalise_runs(p)
        if has_draw:
            set_ppr(p, line=1.0, before=6, after=0, jc="center", keep_next=True, drop_ind=True, drop_tabs=True)
            continue
        if sid == "Equation" or has_math:
            set_ppr(p, line=1.5, before=6, after=6, jc="center", drop_ind=True, drop_tabs=True)
            continue
        if numbered(p) or sid in ("ListParagraph", "Compact"):
            set_ppr(p, line=1.5, before=0, after=3, jc="both")
            continue
        set_ppr(p, line=1.5, before=0, after=6, jc="both", drop_ind=True, drop_tabs=True)
        j = current_jc(p)
        # headings that were typed as bold normal paragraphs keep their left alignment
        txt = para_text(p).strip()
        if len(txt) < 70 and all((r.find(q("w:rPr") + "/" + q("w:b")) is not None) for r in p.iter(q("w:r")) if (r.find(q("w:t")) is not None)):
            set_ppr(p, jc="left", keep_next=True)


def clamp_images(doc, max_emu=5600000):
    for inl in xp(doc.element.body, ".//wp:inline"):
        ext = inl.find(qn("wp:extent"))
        cx, cy = int(ext.get("cx")), int(ext.get("cy"))
        if cx > max_emu:
            r = max_emu / cx
            ncx, ncy = int(cx * r), int(cy * r)
            ext.set("cx", str(ncx)); ext.set("cy", str(ncy))
            for e in xp(inl, ".//a:xfrm/a:ext"):
                e.set("cx", str(ncx)); e.set("cy", str(ncy))


def normalise_tables(doc, skip_first=True):
    body = doc.element.body
    tables = list(body.iter(q("w:tbl")))
    for ti, tbl in enumerate(tables):
        if ti == 0 and skip_first:
            cap = tbl.find(q("w:tblPr") + "/" + q("w:tblCaption"))
            if cap is not None:
                cap.getparent().remove(cap)
            continue
        grid = [int(g.get(q("w:w"))) for g in tbl.find(q("w:tblGrid")).findall(q("w:gridCol"))]
        ncols = len(grid)
        if ncols > 1 and max(grid) - min(grid) <= 0.02 * max(grid):
            # pandoc tables come with equal columns: size them from the content instead
            rows_ = tbl.findall(q("w:tr"))
            wts = []
            for c in range(ncols):
                lens = []
                for tr in rows_:
                    tcs = tr.findall(q("w:tc"))
                    if len(tcs) == ncols:
                        lens.append(len(para_text(tcs[c]).strip()))
                mx, av = max(lens or [5]), sum(lens or [5]) / max(1, len(lens))
                wts.append(max(5.0, min(48.0, 0.45 * mx + 0.55 * av)))
            s_ = sum(wts)
            wts = [max(0.07, w / s_) for w in wts]
            s_ = sum(wts)
            grid = [int(10000 * w / s_) for w in wts]
            # enforce a minimum width so that the longest word of each column does not break
            mins = []
            for c in range(ncols):
                lw = 3
                for tr in rows_:
                    tcs = tr.findall(q("w:tc"))
                    if len(tcs) == ncols:
                        for word in re.split(r"\s+", para_text(tcs[c]).strip()):
                            lw = max(lw, len(word))
                mins.append(lw * 118 + 190)
            scale = TEXT_W / 10000.0
            wd = [g * scale for g in grid]
            for _ in range(10):
                short = [i for i in range(ncols) if wd[i] < mins[i]]
                if not short:
                    break
                need = sum(mins[i] - wd[i] for i in short)
                for i in short:
                    wd[i] = mins[i]
                donors = [i for i in range(ncols) if i not in short and wd[i] > mins[i]]
                room = sum(wd[i] - mins[i] for i in donors) or 1
                for i in donors:
                    wd[i] -= need * (wd[i] - mins[i]) / room
            grid = [int(x * 10000 / TEXT_W) for x in wd]
        tot = sum(grid) or 1
        widths = [max(300, round(g * TEXT_W / tot)) for g in grid]
        diff = TEXT_W - sum(widths)
        widths[widths.index(max(widths))] += diff
        for g, w in zip(tbl.find(q("w:tblGrid")).findall(q("w:gridCol")), widths):
            g.set(q("w:w"), str(w))
        size = 20 if ncols <= 6 else (18 if ncols <= 9 else 16)
        # table properties rebuilt
        tpr = tbl.find(q("w:tblPr"))
        for ch in list(tpr):
            tpr.remove(ch)
        tpr.append(parse_xml(f'<w:tblStyle {nsdecls("w")} w:val="TableGrid"/>'))
        tpr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="{TEXT_W}" w:type="dxa"/>'))
        tpr.append(parse_xml(
            f'<w:tblBorders {nsdecls("w")}>' + "".join(
                f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="595959"/>' for s in
                ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>"))
        tpr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))
        tpr.append(parse_xml(
            f'<w:tblCellMar {nsdecls("w")}><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
            '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'))
        tpr.append(parse_xml(f'<w:tblLook {nsdecls("w")} w:val="0420" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'))
        rows = tbl.findall(q("w:tr"))
        for ri, tr in enumerate(rows):
            trpr = tr.find(q("w:trPr"))
            if trpr is None:
                trpr = OxmlElement("w:trPr")
                # trPr must follow tblPrEx if present, before cells
                first_tc = tr.find(q("w:tc"))
                first_tc.addprevious(trpr)
            for ch in list(trpr):
                trpr.remove(ch)
            trpr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            if ri == 0:
                trpr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            col = 0
            for tc in tr.findall(q("w:tc")):
                tcpr = tc.find(q("w:tcPr"))
                span, vm = 1, None
                if tcpr is not None:
                    gs = tcpr.find(q("w:gridSpan"))
                    span = int(gs.get(q("w:val"))) if gs is not None else 1
                    vm = tcpr.find(q("w:vMerge"))
                    vm = copy.deepcopy(vm) if vm is not None else None
                    tc.remove(tcpr)
                w = sum(widths[col:col + span])
                col += span
                new = OxmlElement("w:tcPr")
                new.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{w}" w:type="dxa"/>'))
                if span > 1:
                    new.append(parse_xml(f'<w:gridSpan {nsdecls("w")} w:val="{span}"/>'))
                if vm is not None:
                    new.append(vm)
                if ri == 0:
                    new.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="F2F2F2"/>'))
                new.append(parse_xml(f'<w:vAlign {nsdecls("w")} w:val="center"/>'))
                tc.insert(0, new)
                for p in tc.findall(q("w:p")):
                    jc = current_jc(p)
                    normalise_runs(p, size=size, bold=(ri == 0))
                    set_pstyle(p, "Compact")
                    set_ppr(p, line=1.0, before=0, after=0, drop_ind=True, drop_tabs=True,
                            jc=("center" if jc == "center" else ("right" if jc == "right" else "left")),
                            keep_next=(True if (len(rows) <= 14 and ri < len(rows) - 1) else None))
                    ppr = p.find(q("w:pPr"))
                    for e in ppr.findall(q("w:numPr")):
                        ppr.remove(e)
        # spacing after the table
        nxt = tbl.getnext()
        if nxt is not None and nxt.tag == q("w:p") and style_of(nxt) not in ("TableCaption", "FigureCaption", "TableNote", "Heading1", "Heading2", "Heading3"):
            ppr = nxt.find(q("w:pPr"))
            set_ppr(nxt, before=10)


def remove_duplicate_captions(body):
    """Chapters 4 and 12 carry a short 'Image Caption' duplicate of the figure caption beneath the figure."""
    for p in list(body.iter(q("w:p"))):
        if style_of(p) == "ImageCaption":
            nxt = p.getnext()
            if nxt is not None and caption_kind(nxt) == "Figure":
                body.remove(p)
            else:
                set_pstyle(p, "FigureCaption")


# ---------------------------------------------------------------------------------------------------
# contents pages
# ---------------------------------------------------------------------------------------------------


def heading_numbers(body):
    """Return list of (level, number_label, title, element) for numbered Heading 1 and 2 paragraphs."""
    out, c = [], [0, 0, 0]
    for p in body.iterchildren(q("w:p")):
        s = style_of(p)
        if s not in ("Heading1", "Heading2", "Heading3"):
            continue
        n = p.find(q("w:pPr") + "/" + q("w:numPr") + "/" + q("w:numId"))
        if n is not None and n.get(q("w:val")) == "0":
            out.append((int(s[-1]), "", re.sub(r"\s+", " ", para_text(p)).strip(), p))
            continue
        lvl = int(s[-1])
        c[lvl - 1] += 1
        for i in range(lvl, 3):
            c[i] = 0
        label = ".".join(str(x) for x in c[:lvl]) + ("." if lvl == 1 else "")
        out.append((lvl, label, re.sub(r"\s+", " ", para_text(p)).strip(), p))
    return out


def run_xml(text=None, tab=False, fld=None, instr=None, bold=False):
    if fld:
        return f'<w:r><w:fldChar w:fldCharType="{fld}"/></w:r>'
    if instr:
        return f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
    if tab:
        return "<w:r><w:tab/></w:r>"
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<w:r><w:t xml:space="preserve">{esc}</w:t></w:r>'


def toc_paragraph(style, parts, first_instr=None, last=False, keep=False):
    xml = f'<w:p {nsdecls("w")}><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    if first_instr:
        xml += run_xml(fld="begin") + run_xml(instr=first_instr) + run_xml(fld="separate")
    for kind, val in parts:
        xml += run_xml(tab=True) if kind == "tab" else run_xml(text=val)
    if last:
        xml += run_xml(fld="end")
    return parse_xml(xml + "</w:p>")


def build_contents(body, pages, anchor):
    """Insert table of contents, list of tables and list of figures after anchor. pages: dict key -> page number."""
    heads = heading_numbers(body)
    ptr = anchor

    def add(el):
        nonlocal ptr
        ptr.addnext(el)
        ptr = el

    t = parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>Table of contents</w:t></w:r></w:p>')
    add(t)
    entries = [(l, n, ti) for (l, n, ti, e) in heads if l <= 2]
    for i, (l, n, ti) in enumerate(entries):
        pg = pages.get(("H", i), "")
        style = "TOC1" if l == 1 else "TOC2"
        parts = []
        if n:
            parts += [("t", n), ("tab", None)]
        parts += [("t", ti.upper()), ("tab", None), ("t", str(pg))]
        add(toc_paragraph(style, parts, first_instr=' TOC \\o "1-2" \\h \\z \\u ' if i == 0 else None, last=(i == len(entries) - 1)))
    # list of tables, list of figures
    for kind, title, tstyle in (("Table", "List of tables", "Table Caption"), ("Figure", "List of figures", "Figure Caption")):
        caps = []
        for p in body.iter(q("w:p")):
            if style_of(p) == ("TableCaption" if kind == "Table" else "FigureCaption") and not in_table(p):
                caps.append(re.sub(r"\s+", " ", para_text(p)).strip())
        h = parse_xml(f'<w:p {nsdecls("w")}><w:pPr><w:pStyle w:val="TOCHeading"/><w:pageBreakBefore/></w:pPr><w:r><w:t>{title}</w:t></w:r></w:p>')
        add(h)
        for i, c in enumerate(caps):
            m = re.match(r"^((?:Table|Figure)\s+(?:\d+|[A-D])\.\d+)\s*[:.]?\s*(.*)$", c)
            label, text = (m.group(1), m.group(2)) if m else ("", c)
            pg = pages.get((kind, i), "")
            add(toc_paragraph("TableofFigures", [("t", f"{label}: {text}" if label else text), ("tab", None), ("t", str(pg))],
                              first_instr=f' TOC \\h \\z \\t "{tstyle},1" ' if i == 0 else None, last=(i == len(caps) - 1)))
    return entries


# ---------------------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------------------


def assemble(src, out, pages=None, tmp=None):
    doc = docx.Document(src)
    body = doc.element.body
    orig_nums = {int(n.get(q("w:numId"))) for n in doc.part.numbering_part.element.findall(q("w:num"))}
    cover_h1 = find_h1(body, "EXECUTIVE SUMMARY")

    # ---- remove the compiler's duplicates, then insert the new chapters
    sens = find_h1(body, "SENSITIVITY ANALYSIS")
    risk = None
    for p in body.iterchildren(q("w:p")):
        if is_heading(p, 1) and re.sub(r"\s+", " ", para_text(p)).strip().upper().startswith("RISK AS"):
            risk = p
    clear_between(body, sens, risk)
    refs = find_h1(body, "REFERENCES")
    clear_between(body, refs, None)
    refpar = fragment_elements(doc, "references.md", src, tmp, orig_nums)

    chapters = [
        ("EXECUTIVE SUMMARY", "ch01_executive_summary.md"),
        ("PROBLEM DEFINITION", "ch02_problem_definition.md"),
        ("ASSUMPTIONS", "ch05_assumptions.md"),
        ("MASS BALANCE", "ch08_mass_balance.md"),
        ("ELECTRICAL ANALYSIS", "ch10_electrical_analysis.md"),
        ("DETAILED CALCULATIONS", "ch13_detailed_calculations.md"),
        ("SENSITIVITY ANALYSIS", "ch16_sensitivity_analysis.md"),
    ]
    for title, md in chapters:
        h = find_h1(body, title)
        nxt = h.getnext()
        # the target chapter must be empty (or just cleared)
        if nxt is not None and nxt.tag == q("w:p") and not is_heading(nxt, 1) and para_text(nxt).strip():
            raise RuntimeError(f"{title} is not empty: {para_text(nxt)[:60]}")
        insert_after(h, fragment_elements(doc, md, src, tmp, orig_nums))
        print("  inserted", title)
    last = insert_after(refs, refpar)
    appendices = [("APPENDIX A: CAD MODEL AND THERMAL (COMSOL-TYPE) MODEL OF THE ELECTRODE", "appA_cad_thermal.md"),
                  ("APPENDIX B: POWER BI DASHBOARD", "appB_powerbi.md"),
                  ("APPENDIX C: MATLAB SCRIPTS, CROSS-VALIDATION AND DASHBOARD", "appC_matlab.md"),
                  ("APPENDIX D: EXCEL WORKBOOK AND REGISTER OF DIGITAL FILES", "appD_excel_files.md")]
    for title, md in appendices:
        h = copy.deepcopy(refs)
        for t_ in list(h.iter(q("w:t")))[1:]:
            t_.text = ""
        list(h.iter(q("w:t")))[0].text = title
        hp = h.find(q("w:pPr"))
        for e in hp.findall(q("w:numPr")):
            hp.remove(e)
        hp.find(q("w:pStyle")).addnext(parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'))
        last.addnext(h)
        last = insert_after(h, fragment_elements(doc, md, src, tmp, orig_nums))
    # unnumbered references heading
    ppr = refs.find(q("w:pPr"))
    npr = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>')
    for e in ppr.findall(q("w:numPr")):
        ppr.remove(e)
    ps = ppr.find(q("w:pStyle"))
    ps.addnext(npr)
    # move keepNext etc. not needed (style)

    # ---- text corrections (the compiler's wording is kept; only typographical slips and citations are fixed)
    replace_text(body, "SURNAME & INTIALS", "SURNAME & INITIALS", 1)
    replace_text(body, "RISK ASESSMENT", "RISK ASSESSMENT", 1)
    replace_text(body, "EQUIPMENTS/ DESIGN REQUIREMENTS", "EQUIPMENT AND DESIGN REQUIREMENTS")
    replace_text(body, "(ABM, 2007)", "(Jaccard, 2007)", 1)
    replace_text(body, "(Metso, 2025)", "(Metso, n.d.)", 1)
    print("  dashes fixed in", fix_dashes(body), "text nodes")

    # ---- formatting
    black_arial_styles(doc)
    fix_numbering(doc)
    remove_duplicate_captions(body)
    cover_h1 = find_h1(body, "EXECUTIVE SUMMARY")
    normalise_body(doc, cover_h1)
    normalise_tables(doc)
    clamp_images(doc)
    sort_all_ppr(body)

    # cover: runs only black (sizes of the cover are the compiler's), first page without footer number
    for p in list(body.iterchildren(q("w:p")))[:36]:
        if p is cover_h1:
            break
        for c in xp(p, ".//w:color"):
            c.set(q("w:val"), "000000")
            for a in ("themeColor", "themeShade", "themeTint"):
                if c.get(q("w:" + a)) is not None:
                    del c.attrib[q("w:" + a)]
    # trim the blank spacer paragraphs of the cover so that it fits on one page
    removed = 0
    for p in list(body.iterchildren(q("w:p"))):
        if p is cover_h1:
            break
        if not para_text(p).strip() and not xp(p, ".//w:drawing") and not xp(p, './/w:br[@w:type="page"]') and not p.getprevious() is None:
            idx = list(body).index(p)
            if idx > 3 and removed < COVER_TRIM:
                body.remove(p)
                removed += 1
    sect = body.find(q("w:sectPr"))
    if sect.find(q("w:titlePg")) is None:
        tp = OxmlElement("w:titlePg")
        dg = sect.find(q("w:docGrid"))
        (dg.addprevious(tp) if dg is not None else sect.append(tp))
    # footer: Arial 10 black
    for sec in doc.sections:
        for p in sec.footer.paragraphs:
            normalise_runs(p._p, size=20)

    # ---- contents pages after the cover (which ends with a page break paragraph just before the first chapter)
    anchor = cover_h1.getprevious()
    pages = pages or {}
    build_contents(body, pages, anchor)

    # core properties
    doc.core_properties.title = "Design and Scale-Up of a Closed Ferrochrome Submerged Arc Furnace from 55 MW to 60 MW"
    doc.core_properties.author = "MPG 118S project team"
    doc.save(out)
    return out


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    with tempfile.TemporaryDirectory() as tmp:
        assemble(src, out, tmp=tmp)
    print("saved", out)
