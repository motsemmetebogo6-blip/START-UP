import os, subprocess, re
import script_data as D
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

WPM = 130
def mmss(sec): return f"{int(sec)//60}:{int(sec)%60:02d}"
def words(t): return len(t.split())

# per member and per slide accounting (time derived from word count at 130 words per minute)
mem = {}
order = ["Mkhonto", "Jeff", "Tebogo", "Ngesi", "Simphiwe", "Sibandze"]
for n, title, sp, onscreen, ho in D.SLIDES:
    for name, sec, txt in sp:
        m = mem.setdefault(name, dict(slides=[], words=0))
        if n not in m["slides"]: m["slides"].append(n)
        m["words"] += words(txt)
total_words = sum(m["words"] for m in mem.values())

md = []
A = md.append
A("---\ntitle: \"Presentation Script\"\nsubtitle: \"MPG 118S final project: closed ferrochrome submerged arc furnace, 55 to 60 MW\"\n---\n")
A("# 1. How to use this script\n")
A(f"The presentation has 22 slides and is delivered by six members in about 25 minutes. The script follows the slide order. Each part is marked with the name of the speaker, and the last sentence of a part is the hand-over to the next speaker. The text is written to be read aloud at about {WPM} words a minute, which is {total_words} words, or about {total_words/WPM:.0f} minutes of speaking plus about one minute of hand-overs and slide changes.\n")
A("* Read your own part three times aloud with a timer before the day, and shorten a sentence rather than speed up.\n* Look at the audience, not at the slide; the slide has the figures and this script has the words.\n* Say the numbers exactly as written. They are the verified results of the report.\n* If you are running late, drop the figure description and keep the numbers and the hand-over.\n* Only the speaker named in a heading speaks. Slides 17 and 18 have two speakers.\n")
A("# 2. Who presents what\n")
A("::: {custom-style=\"Table Caption\"}\nTable 1: Allocation of sections, slides and time\n:::\n")
A("| Member | Sections | Slides | Words | Time |\n|---|---|---|---|---|")
for nm in order:
    m = mem[nm]
    A(f"| {nm} | {D.MEMBERS[nm]} | {', '.join(str(s) for s in m['slides'])} | {m['words']} | {mmss(m['words']/WPM*60)} |")
A(f"| Total | | 1 to 22 | {total_words} | {mmss(total_words/WPM*60)} |\n")
A("The names are those used in the project group. If two members swap sections, move their slide numbers between the parts below; the hand-over sentences name the next speaker and must be changed with them.\n")
A("# 3. Running order and timing\n")
A("::: {custom-style=\"Table Caption\"}\nTable 2: Running order with cumulative time (hand-overs of 3 to 4 seconds each are not included)\n:::\n")
A("| Slide | Title | Speaker | Time | Cumulative |\n|---|---|---|---|---|")
cum = 0
for n, title, sp, onscreen, ho in D.SLIDES:
    secs = sum(words(t) / WPM * 60 for _, _, t in sp)
    cum += secs
    A(f"| {n} | {title} | {' and '.join(s[0] for s in sp)} | {mmss(secs)} | {mmss(cum)} |")
A("")
A("# 4. The script, slide by slide\n")
for n, title, sp, onscreen, ho in D.SLIDES:
    A(f"## Slide {n}: {title}\n")
    A(f"*On the screen:* {onscreen}\n")
    for name, sec, txt in sp:
        A(f"**{name.upper()}** ({mmss(words(txt)/WPM*60)})\n")
        A(txt + "\n")
    if ho:
        A(f"*Hand-over:* {ho}\n")
A("# 5. Individual reading sheets\n")
A("Each member can print the sheet below with only their own parts.\n")
for nm in order:
    A("```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n")
    A(f"## Reading sheet: {nm}\n")
    A(f"Sections: {D.MEMBERS[nm]}. Slides {', '.join(str(s) for s in mem[nm]['slides'])}. Time about {mmss(mem[nm]['words']/WPM*60)}.\n")
    for n, title, sp, onscreen, ho in D.SLIDES:
        for name, sec, txt in sp:
            if name == nm:
                A(f"**Slide {n}: {title}**\n")
                A(txt + "\n")
A("# 6. Questions and answers\n")
A("The panel may ask questions after the presentation. The member named answers first; any other member may add. The answers use only the verified numbers of the report.\n")
A("::: {custom-style=\"Table Caption\"}\nTable 3: Likely questions and answers\n:::\n")
A("| Question | Answers | Answer |\n|---|---|---|")
for q, who, a in D.QA:
    A(f"| {q} | {who} | {a} |")
A("")
A("# 7. Checklist before the presentation\n")
A("* Open the PowerPoint and the PDF copy on the presentation computer, and check slide 22 shows the references.\n* Run `saf_dashboard.m` once in MATLAB so that the MATLAB dashboard can be shown live if asked (Sibandze). Only its data part was tested in Octave.\n* Have the report open at Appendix A (CAD and thermal model), Appendix B (Power BI) and Appendix C (MATLAB) for questions.\n* Agree who advances the slides, and who watches the time and signals 5 minutes and 1 minute to the end.\n* Agree the order of answers to questions: the member named in Table 3 first.\n* Say that the temperatures inside the electrode are illustrative and that the 450 t/d target is the binding requirement. These two points will be asked.\n")
open("script.md", "w", encoding="utf8").write("\n".join(md))
ref = "/tmp/claude-0/-home-user-START-UP/3a8d48ac-4768-57df-9a85-5df55b75f1b9/scratchpad/ref/reference.docx"
subprocess.run(["pandoc", "script.md", "-f", "markdown-tex_math_dollars", "-t", "docx", "--reference-doc", ref, "-o", "script_raw.docx"], check=True)

d = Document("script_raw.docx")
# \newpage markers
for p in list(d.paragraphs):
    if p.text.strip() == "\\newpage":
        p.text = ""
        r = p.add_run(); r.add_break(__import__("docx").enum.text.WD_BREAK.PAGE)
def setfont(run, size=None, bold=None):
    run.font.name = "Arial"; run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    run.font.color.rgb = RGBColor(0, 0, 0)
    if size: run.font.size = Pt(size)
for st in d.styles:
    try:
        st.font.name = "Arial"; st.font.color.rgb = RGBColor(0, 0, 0)
    except Exception:
        pass
in_table = set()
for t in d.tables:
    t.style = d.styles["Table Grid"] if "Table Grid" in [s.name for s in d.styles] else t.style
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs: setfont(r, 9.5)
for p in d.paragraphs:
    if p._p.getparent().tag.endswith('}tc'): continue
    sn = p.style.name
    size = 12
    if sn == "Title": size = 20
    elif sn == "Subtitle": size = 13
    elif sn.startswith("Heading 1"): size = 15
    elif sn.startswith("Heading 2"): size = 13
    elif "Caption" in sn: size = 10
    for r in p.runs: setfont(r, size)
    if sn.startswith("Heading") or sn in ("Title", "Subtitle") or "Caption" in sn:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.bold = True
        p.paragraph_format.keep_with_next = True
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
# table width and column widths
from docx.oxml import OxmlElement
for t in d.tables:
    tblPr = t._tbl.tblPr
    for e in tblPr.findall(qn("w:tblW")): tblPr.remove(e)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), "9026"); w.set(qn("w:type"), "dxa"); tblPr.append(w)
    for e in tblPr.findall(qn("w:tblBorders")): tblPr.remove(e)
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "595959"); b.append(e)
    tblPr.append(b)
    for c in t.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs: r.font.bold = True
        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), "F2F2F2"); c._tc.get_or_add_tcPr().append(sh)
W = {"Member": [12, 38, 18, 12, 12], "Slide": [8, 44, 20, 14, 14], "Question": [28, 12, 60]}
for t in d.tables:
    hdr = t.rows[0].cells[0].text.strip()
    pr = W.get(hdr)
    if not pr: continue
    tot = sum(pr)
    widths = [int(9026 * x / tot) for x in pr]
    grid = t._tbl.tblGrid
    for g, w_ in zip(grid.findall(qn("w:gridCol")), widths): g.set(qn("w:w"), str(w_))
    for row in t.rows:
        for c, w_ in zip(row.cells, widths):
            tcPr = c._tc.get_or_add_tcPr()
            for e in tcPr.findall(qn("w:tcW")): tcPr.remove(e)
            e = OxmlElement("w:tcW"); e.set(qn("w:w"), str(w_)); e.set(qn("w:type"), "dxa"); tcPr.insert(0, e)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); t._tbl.tblPr.append(lay)
for s in d.sections:
    s.page_width = Inches(8.27); s.page_height = Inches(11.69)
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)
d.core_properties.title = "MPG 118S Presentation Script"
d.save("MPG118S_Presentation_Script.docx")
print("saved", total_words, "words", mmss(total_words/WPM*60))
