#!/usr/bin/env python3
"""build_deck.py: 22-slide final presentation on the TUT FEBE template (layouts, footer, title picture kept; content replaced)."""
import copy
import os
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

TEMPLATE, OUT = sys.argv[1], sys.argv[2]
FIG = "/home/user/START-UP/report/figures/"
BLUE, GOLD, GREY, DARK, LIGHT = RGBColor(0x00, 0x56, 0x96), RGBColor(0xFF, 0xC0, 0x00), RGBColor(0x59, 0x59, 0x59), RGBColor(0, 0, 0), RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(255, 255, 255)
DEPT = "Department of Chemical, Metallurgy and Material Sciences Engineering"

prs = Presentation(TEMPLATE)

# ---- keep only slide 1 (the title picture), drop the template's own content slides
sldIdLst = prs.slides._sldIdLst
for sldId in list(sldIdLst)[1:]:
    prs.part.drop_rel(sldId.rId)
    sldIdLst.remove(sldId)

# ---- footer text of the layouts: department
for lay in prs.slide_layouts:
    for sh in lay.shapes:
        if sh.has_text_frame and "Department of" in sh.text_frame.text:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if "Department" in r.text or "Electrical" in r.text or "Engineering" in r.text and "Faculty" not in r.text:
                        pass
            ps = sh.text_frame.paragraphs
            last = ps[-1]
            if last.runs:
                last.runs[0].text = DEPT
                for r in last.runs[1:]:
                    r.text = ""

LAYOUT = prs.slide_layouts[1]  # Title and Content (title + footer with logo)
W, H = prs.slide_width, prs.slide_height


def set_run(r, size, bold=False, color=DARK, italic=False):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, margin=0.05):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    return tb, tf


def add_par(tf, parts, size=18, bullet=False, align=None, space_after=6, first=False, color=DARK):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    if isinstance(parts, str):
        parts = [(parts, False)]
    for text, bold in parts:
        r = p.add_run()
        r.text = text
        set_run(r, size, bold, color)
    p.space_after = Pt(space_after)
    if align:
        p.alignment = align
    if bullet:
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(Inches(0.3))))
        pPr.set("indent", str(-int(Inches(0.3))))
        for e in pPr.findall(qn("a:buNone")):
            pPr.remove(e)
        bf = etree.SubElement(pPr, qn("a:buFont"))
        bf.set("typeface", "Arial")
        bc = etree.SubElement(pPr, qn("a:buChar"))
        bc.set("char", "•")
    return p


def bullets(slide, items, x, y, w, h, size=18, space_after=8):
    tb, tf = textbox(slide, x, y, w, h)
    for i, it in enumerate(items):
        add_par(tf, it, size=size, bullet=True, first=(i == 0), space_after=space_after)
    return tb


def new_slide(title, notes=None, tag=None, number=[1]):
    number[0] += 1
    s = prs.slides.add_slide(LAYOUT)
    # remove the body placeholder, keep and place the title
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 1:
            ph._element.getparent().remove(ph._element)
    t = s.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.95)
    tf = t.text_frame
    tf.clear()
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = title
    set_run(r, 28, True, DARK)
    tb, tf2 = textbox(s, 12.35, 0.12, 0.8, 0.3)
    add_par(tf2, str(number[0]), size=12, first=True, align=PP_ALIGN.RIGHT, color=GREY)
    if tag:
        tb3, tf3 = textbox(s, 0.6, 0.1, 6.0, 0.3)
        add_par(tf3, tag, size=12, first=True, color=GREY)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def picture(slide, name, x, y, w, h, anchor="center"):
    path = FIG + name
    iw, ih = Image.open(path).size
    r = min(w / iw, h / ih)
    pw, ph = iw * r, ih * r
    px = x + (w - pw) / 2
    py = y + (h - ph) / 2 if anchor == "center" else y
    return slide.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))


def caption(slide, text, x, y, w, size=12):
    tb, tf = textbox(slide, x, y, w, 0.35)
    add_par(tf, text, size=size, first=True, align=PP_ALIGN.CENTER, color=GREY)


def card(slide, x, y, w, h, value, label, vcolor=BLUE, vsize=34):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.08
    sh.fill.solid(); sh.fill.fore_color.rgb = LIGHT
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.12)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = value; set_run(r, vsize, True, vcolor)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = label; set_run(r2, 14, False, DARK)
    return sh


def table(slide, rows, x, y, w, col_w, size=14, row_h=0.36, header=True, bold_last=False):
    nr, nc = len(rows), len(rows[0])
    gs = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    tbl = gs.table
    tblPr = tbl._tbl.tblPr
    for a in ("firstRow", "bandRow"):
        tblPr.set(a, "0")
    tot = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(w * cw / tot)
    for ri, row in enumerate(rows):
        tbl.rows[ri].height = Inches(row_h)
        for ci, val in enumerate(row):
            c = tbl.cell(ri, ci)
            c.margin_left = c.margin_right = Inches(0.08)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = str(val)
            is_h = header and ri == 0
            set_run(r, size, is_h or (bold_last and ri == nr - 1), WHITE if is_h else DARK)
            c.fill.solid()
            c.fill.fore_color.rgb = BLUE if is_h else (LIGHT if ri % 2 == 0 else WHITE)
    return gs


def arrow(slide, x, y, w, h):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    a.fill.solid(); a.fill.fore_color.rgb = GOLD
    a.line.fill.background()
    return a


