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


# ---------------------------------------------------------------------------------------------
# 22-slide version: every report chapter and every digital tool is kept, the outline is kept.
# ---------------------------------------------------------------------------------------------
s1 = prs.slides[0]
fb = s1.shapes.build_freeform(Inches(0), Inches(1.76))
fb.add_line_segments([(Inches(12.2), Inches(1.76)), (Inches(10.47), Inches(3.75)), (Inches(8.93), Inches(5.25)),
                      (Inches(8.36), Inches(5.81)), (Inches(0), Inches(5.81))], close=True)
cover = fb.convert_to_shape()
cover.fill.solid(); cover.fill.fore_color.rgb = BLUE
cover.line.fill.background(); cover.shadow.inherit = False
patch = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.7), Inches(6.9), Inches(2.64), Inches(0.62))
patch.fill.solid(); patch.fill.fore_color.rgb = RGBColor(0xE6, 0xE6, 0xE6)
patch.line.fill.background(); patch.shadow.inherit = False
tb, tf = textbox(s1, 0.45, 1.8, 7.5, 3.8, anchor=MSO_ANCHOR.MIDDLE)
add_par(tf, [("FACULTY OF ENGINEERING AND THE BUILT ENVIRONMENT", True)], size=18, first=True, space_after=2, color=GOLD)
add_par(tf, [("MPG 118S  FINAL PROJECT PRESENTATION", True)], size=16, space_after=14, color=WHITE)
add_par(tf, [("Design and Scale-Up of a Closed Ferrochrome Submerged Arc Furnace from 55 MW to 60 MW Using 65 MVA Transformers", False)], size=24, space_after=14, color=WHITE)
add_par(tf, [("Sithole SP, Motsemme T, Ngesi SK, Mabapa LJ, Sibandze PS and Mkhonto AS", False)], size=15, space_after=2, color=WHITE)
add_par(tf, [("Department of Chemical, Metallurgy and Material Sciences Engineering, 28 November 2026", False)], size=13, space_after=0, color=WHITE)
s1.notes_slide.notes_text_frame.text = "Final presentation in 22 slides. The order follows the report, chapters 1 to 20, then the digital tools and the references."

# 2 Outline (table of contents)
s = new_slide("Presentation Outline", "Table of contents of the presentation. Each slide shows the chapter or appendix of the report that it summarises.")
rows = [("3", "Executive summary, background and problem", "Chapters 1-2"), ("4", "Existing process, design basis and assumptions", "Chapters 3-5"),
        ("5", "Literature review and existing condition", "Chapters 6-7"), ("6-8", "Mass balance and optimisation", "Chapter 8"),
        ("9", "Energy balance and metallurgical analysis", "Chapters 9, 11"), ("10", "Electrical analysis", "Chapter 10"),
        ("11", "Alternatives, selected design and investment", "Chapters 12, 14"), ("12", "Detailed calculations and equipment", "Chapters 13, 14"),
        ("13-16", "CAD model and thermal (COMSOL-type) model", "Chapter 13, Appendix A"), ("17", "Economics and sensitivity analysis", "Chapters 15-16"),
        ("18", "Risk assessment and implementation", "Chapters 17-19"), ("19-20", "Power BI, MATLAB and Excel tools", "Appendices B-D"),
        ("21-22", "Conclusions, recommendations and references", "Chapter 20")]
table(s, [["Slide", "Content", "Report"]] + [list(r) for r in rows], 0.9, 1.35, 11.5, [1.2, 7.3, 3.0], size=14, row_h=0.37)

# 3 Executive summary, background, problem
s = new_slide("Executive Summary, Background and Problem", "C1 = 60 MW mean power (PF 0.95, LF 0.972) on the existing 65 MVA transformers plus hot charging of the pellets at about 500 C.", tag="Chapters 1 and 2")
card(s, 0.6, 1.4, 3.9, 1.25, "455 t/d", "C1 production, from 394 t/d today", vsize=30)
card(s, 4.7, 1.4, 3.9, 1.25, "R1 540 M", "net present value, IRR about 70 %", vsize=30)
card(s, 8.8, 1.4, 3.9, 1.25, "R402 M", "total investment", vsize=30)
b, tf = textbox(s, 0.6, 2.85, 5.9, 3.6)
add_par(tf, [("Background and problem", True)], size=18, first=True, space_after=5, color=BLUE)
for t in ["Electricity is the heat source and a major cost; tariffs rose 12.74 % and 8.76 %.", "Brief: uprate the closed three-phase furnace from 57.43 MW to 60 MW mean on its 65 MVA transformers.", "450 t/d at 3.5 MWh/t needs 65.6 MW mean, more than the transformers deliver, so the specific energy must also fall."]:
    add_par(tf, t, size=15, bullet=True, space_after=4)
b, tf = textbox(s, 6.9, 2.85, 5.9, 3.6)
add_par(tf, [("Findings", True)], size=18, first=True, space_after=5, color=BLUE)
for t in ["Cr recovery 86.9 %, flux 0.366 t/t; plant data consistent (closure -0.41 %).", "Least preheat 452 °C; robust at about 610 °C once a plant trial verifies the saving.", "The 450 t/d target binds, not the economics.", "Verified in Python, MATLAB and Excel; Power BI and CAD tools added."]:
    add_par(tf, t, size=15, bullet=True, space_after=4)

# 4 Existing process, design basis, assumptions
s = new_slide("Existing Process, Design Basis and Assumptions", "Plant data govern; literature and assumptions are used only where the data are silent. 28 assumptions are listed in Chapter 5.", tag="Chapters 3, 4 and 5")
table(s, [["Criterion", "Requirement"], ["Apparent power", "Not above 65 MVA"], ["Power factor", "0.93 to 0.95"], ["Production", "At least 450 t/d"], ["Specific energy", "Not above 3.5 MWh/t"],
          ["Slag superheat", "Positive"], ["Auxiliary use", "Not above 90 %"], ["Net present value", "Positive"]], 0.6, 1.4, 5.2, [2.4, 2.8], size=14, row_h=0.45)
b, tf = textbox(s, 6.1, 1.35, 6.7, 2.1)
add_par(tf, [("Existing process", True)], size=17, first=True, space_after=4, color=BLUE)
for t in ["Ore 80 % pellets, 20 % lumpy; flux 55 % quartz, 45 % limestone.", "Reductant 10 % coke, 54 % and 36 % anthracite.", "3 × 21.67 MVA transformers; three Søderberg electrodes."]:
    add_par(tf, t, size=14, bullet=True, space_after=3)
b, tf = textbox(s, 6.1, 3.45, 6.7, 3.0)
add_par(tf, [("Critical assumptions (low confidence)", True)], size=17, first=True, space_after=4, color=BLUE)
for t in ["A-24 hot charging saves 0.07 MWh/t per 100 K.", "A-22 auxiliary design margin 10 %.", "A-23 existing tap range 260 to 340 V.", "A-17 reactance cut of 20 %; PF 0.93 is not metered."]:
    add_par(tf, t, size=14, bullet=True, space_after=3)
b, tf = textbox(s, 0.6, 5.2, 5.2, 1.3)
add_par(tf, "Data hierarchy: plant data, brief, literature, assumptions. Every value carries a provenance tag.", size=14, first=True)

# 5 Literature and existing condition
s = new_slide("Literature Review and Existing Condition", "Power cannot be raised independently of the transformer, electrodes and circuit. The plant data reproduce 393.65 t/d at 57.43 MW to 0.04 percent.", tag="Chapters 6 and 7")
picture(s, "F1_operating_envelope.png", 0.4, 1.35, 5.4, 5.1)
table(s, [["Source", "Contribution"], ["Barker (2011)", "Scale-up limited by reactance and electrode current"], ["De Waal et al. (1992)", "Furnace as resistance and reactance"],
          ["Magnussen (2018)", "Spacing, diameter, resistance, reactance"], ["Sweeten et al. (2018)", "Ore mineralogy sets the balance"]], 6.0, 1.4, 6.8, [2.3, 4.5], size=13, row_h=0.45)
bullets(s, [[("PF 0.95 and LF at least 0.972 ", True), ("give 60 MW mean.", False)], "Chromium recovery is about 87 %, not 78 %.", "No electrical measure alone reaches 450 t/d."], 6.0, 4.0, 6.8, 2.5, size=16)

# 6 Mass balance
s = new_slide("Mass Balance: Seven Balances, Five Unknowns", "Weighted non-negative least squares, solved in Python and repeated in MATLAB. Chromium recovery is 86.9 percent, not 78 percent.", tag="Chapter 8")
picture(s, "F4_mass_balance.png", 0.4, 1.35, 4.6, 3.3)
picture(s, "F6_chromium_recovery.png", 5.1, 1.35, 4.6, 3.3)
table(s, [["Per tonne of alloy", "Value"], ["Ore blend", "2.144 t"], ["Dry reductant", "0.433 t"], ["Flux", "0.366 t"], ["Slag", "1.188 t"], ["Off-gas", "597 Nm³"]], 9.9, 1.4, 2.9, [1.7, 1.2], size=12, row_h=0.42)
card(s, 0.6, 4.95, 3.9, 1.4, "-0.41 %", "mass closure; all residuals within 3 %", vsize=28)
card(s, 4.7, 4.95, 3.9, 1.4, "+15.5 %", "all daily duties at C1", vsize=28)
card(s, 8.8, 4.95, 3.9, 1.4, "105 %", "auxiliary use at a 10 % margin", vsize=28)

# 7 Optimisation
s = new_slide("How the Optimisation Was Achieved", "Step one finds the least intervention, step two tests it against uncertainty, step three designs it to hold. Closed form: T* = T_ref + 100 (SEC0 - 24 S PF LF / 450) / s.", tag="Chapter 8")
for i, (h, d_) in enumerate([("1  Deterministic", "SLSQP and closed form: T* = 452 °C"), ("2  Monte Carlo", "100 000 samples: meets 450 t/d in about 10 %"), ("3  Robust", "Chance-constrained: about 610 °C")]):
    x = 0.6 + i * 4.2
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.35), Inches(3.7), Inches(1.15))
    sh.adjustments[0] = 0.08
    sh.fill.solid(); sh.fill.fore_color.rgb = LIGHT; sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.15)
    add_par(tf, [(h, True)], size=18, first=True, space_after=3, color=BLUE)
    add_par(tf, d_, size=14, space_after=0)
    if i < 2:
        arrow(s, x + 3.72, 1.7, 0.46, 0.45)
picture(s, "F7_optimisation_map.png", 0.4, 2.65, 6.2, 3.35)
picture(s, "F8_montecarlo.png", 6.7, 2.65, 6.2, 3.35)
caption(s, "Minimum preheat for 450 t/d", 0.4, 6.0, 6.2, size=12); caption(s, "Monte Carlo distribution of C1 production", 6.7, 6.0, 6.2, size=12)

# 8 Robust design
s = new_slide("Robust Design: Verify the Saving First", "Without a plant trial no practical temperature is robust. A trial that confirms the vendor saving makes C1 robust at about 610 C.", tag="Chapter 8")
picture(s, "F11_robust_optimisation.png", 0.4, 1.4, 7.0, 4.9)
table(s, [["Hot-charging saving", "T for 50 %", "T for 90 %"], ["Unverified", "670 °C", "925 °C"], ["Verified, full vendor value", "520 °C", "610 °C"], ["Verified, 75 % of vendor", "670 °C", "780 °C"]], 7.6, 1.5, 5.2, [2.6, 1.3, 1.3], size=14, row_h=0.55)
bullets(s, [[("Plant trial before capital release ", True), ("is the cheapest risk reduction.", False)], "Design the preheater for about 610 °C.", "Each 0.01 of load factor saves about 48 °C of preheat."], 7.6, 4.0, 5.2, 2.4, size=17)

# 9 Energy and metallurgical analysis
s = new_slide("Energy Balance and Metallurgical Analysis", "Energy balance from Chapter 9. The slag margin of 44 C is the reason the electrodes are not raised.", tag="Chapters 9 and 11")
card(s, 0.6, 1.4, 3.9, 1.3, "2.90 MWh/t", "process requirement", vsize=28)
card(s, 4.7, 1.4, 3.9, 1.3, "0.15 MWh/t", "electrical circuit loss", vsize=28)
card(s, 8.8, 1.4, 3.9, 1.3, "0.46 MWh/t", "thermal loss", vsize=28)
b, tf = textbox(s, 0.6, 2.95, 5.9, 3.5)
add_par(tf, [("Energy and hot charging", True)], size=18, first=True, space_after=5, color=BLUE)
for t in ["Pellets at 500 °C return 712 MJ/t: 444 t/d.", "Pellets, lumpy ore and fluxes at 500 °C: 463 t/d.", "The 450 t/d gate needs at least 832 MJ/t of feed heat."]:
    add_par(tf, t, size=15, bullet=True, space_after=4)
b, tf = textbox(s, 6.9, 2.95, 5.9, 3.5)
add_par(tf, [("Metallurgy", True)], size=18, first=True, space_after=5, color=BLUE)
for t in ["Chromium recovery about 87 %; 90 % planning value, 93 % target.", "Slag superheat 44 °C; stop-increase level 25 °C.", "Flux 0.449 t/t exceeds the 0.33 to 0.39 t/t needed.", "2.41 MWh/t needs 58 % metallisation, above the 40 to 50 % range."]:
    add_par(tf, t, size=15, bullet=True, space_after=4)

# 10 Electrical
s = new_slide("Electrical Analysis: No Transformer Headroom", "Eight scenarios on one 65 MVA basis. 47 of 52 numbers of the earlier chapters are reproduced; Python and MATLAB agree on 104 of 104 values.", tag="Chapter 10")
picture(s, "F2_transformer_loading.png", 0.4, 1.35, 6.3, 3.6)
picture(s, "F3_pf_route_current_density.png", 6.8, 1.35, 6.1, 3.6)
bullets(s, [[("S-B, 60 MW mean: ", True), ("64.98 MVA, 100 % of rating; 60 MW on load would give only 391 t/d.", False)],
            [("Resistance route ", True), ("cuts electrode current 7.8 %; ", False), ("the selected reactance route ", True), ("raises it 1.1 %, to 6.90 A/cm², above 6.80 (DC-04).", False)]], 0.6, 5.15, 12.1, 1.3, size=15, space_after=4)

# 11 Alternatives, design, investment
s = new_slide("Alternatives, Selected Design C1 and Investment", "Chapter 12 values with the preheat measured from 0 C; the verified model gives 454.6 t/d with the ambient reference. Capital accuracy is minus 40 to plus 40 percent.", tag="Chapters 12 and 14")
table(s, [["Alternative", "MW", "SEC", "t/d", "450"], ["E0 existing", "57.43", "3.50", "393.8", "No"], ["E1 PF 0.95", "58.66", "3.50", "402.3", "No"], ["E2 PF 0.95, LF 0.972", "60.00", "3.50", "411.4", "No"],
          ["P1 hot charging", "57.43", "3.15", "437.5", "No"], ["P2 pre-reduced", "57.43", "2.41", "571.9", "Yes"], ["C1 E2 + P1", "60.00", "3.15", "457.1", "Yes"], ["C2 E2 + P2", "60.00", "2.41", "597.5", "Yes"]],
      0.6, 1.4, 6.6, [2.7, 1.0, 0.9, 1.1, 0.9], size=13, row_h=0.42)
table(s, [["Item", "R million"], ["Conductor works", "45"], ["Transformer monitoring", "25"], ["Controls and metering", "10"], ["Auxiliary upgrades", "30"], ["Hot charging", "200"], ["Contingency 20 %", "62"], ["Shutdown loss", "30"], ["Total", "402"]],
      7.5, 1.4, 5.3, [3.4, 1.9], size=13, row_h=0.4, bold_last=True)
bullets(s, [[("C1 ranked first ", True), ("under every weighting: PF 0.95, LF 0.972 and pellets hot-charged at about 500 °C.", False)], "Transformers, shell and Søderberg electrodes are retained."], 0.6, 5.0, 6.6, 1.5, size=15, space_after=3)

# 12 Detailed calculations and equipment
s = new_slide("Detailed Calculations of C1 and Equipment", "Calculated in the verified model and repeated in MATLAB. Equipment packages are those of Chapter 14.", tag="Chapters 13 and 14")
table(s, [["Quantity", "Equation", "Value"], ["Mean power", "65 × 0.95 × 0.972", "60.02 MW"], ["On-load apparent power", "(60 / 0.972) / 0.95", "64.98 MVA"], ["Electrode current (estimate)", "8.33 × P_on^(2/3)", "130.1 kA"],
          ["Specific energy", "3.50 - 0.07 (500 - 25)/100", "3.1675 MWh/t"], ["Production", "24 × 60 / 3.1675", "454.6 t/d"], ["Least preheat for 450 t/d", "closed form", "452 °C"]],
      0.6, 1.4, 7.4, [2.8, 2.7, 1.9], size=13, row_h=0.5)
b, tf = textbox(s, 8.3, 1.35, 4.5, 4.9)
add_par(tf, [("Equipment (Chapter 14)", True)], size=17, first=True, space_after=5, color=BLUE)
for t in ["Conductor rearrangement for PF 0.95.", "Transformer thermal monitoring.", "Electrode baking and slip monitors.", "Auxiliary upgrades to the C1 duties.", "Hot-charging system: insulated conveyance, hot-rated bins."]:
    add_par(tf, t, size=14, bullet=True, space_after=4)
bullets(s, ["The margin in specific energy is only 1.0 %, so the hot-charging saving must be verified before capital is committed."], 0.6, 5.2, 7.4, 1.3, size=15)

# 13 CAD
s = new_slide("CAD Model of the Furnace: Open Cut and Revolve Cut", "Rebuilt in CadQuery from the SolidWorks screenshot. Only four dimensions are plant data; the rest are tagged estimates marked with an asterisk.", tag="Chapter 13, Appendix A")
picture(s, "view_section_open_cut.png", 0.3, 1.35, 4.9, 5.1)
picture(s, "iso_open_cut_quarter.png", 5.3, 1.35, 4.2, 5.1)
bullets(s, [[("Revolve cut: ", True), ("hearth cavity radius 5.44 m, height 7.50 m.", False)], [("Files: ", True), ("STEP assembly with named bodies, STL, DXF half-section.", False)], [("Data: ", True), ("shell 13.70 m, hearth 10.88 m, electrode 1.55 m, pitch circle 4.19 m.", False)]], 9.6, 1.5, 3.3, 4.9, size=14, space_after=6)

# 14 Views
s = new_slide("Top, Side and Bottom Views with Dimensions", "Electrodes E1 to E3 at 0, 120 and 240 degrees; tap pipes T1 and T2 at -145 and -35 degrees. Dimensions in metres.", tag="Chapter 13, Appendix A")
picture(s, "view_top.png", 0.3, 1.4, 4.2, 4.6); picture(s, "view_side.png", 4.6, 1.4, 4.2, 4.6); picture(s, "view_bottom.png", 8.9, 1.4, 4.2, 4.6)
caption(s, "Top view", 0.3, 6.05, 4.2, size=13); caption(s, "Side view (front elevation)", 4.6, 6.05, 4.2, size=13); caption(s, "Bottom view", 8.9, 6.05, 4.2, size=13)

# 15 Thermal set-up
s = new_slide("Thermal Model of the Electrode (COMSOL-Type)", "Steady heat conduction with Joule heating including the skin effect; finite volume, axisymmetric unit cell. The geometry imports from the STEP file; no .mph file was made.", tag="Chapter 13, Appendix A")
table(s, [["Input", "Value", "Tag", "COMSOL feature"], ["Slag, metal", "1 800, 1 732 °C", "DATA", "Temperature"], ["Electrode current", "130.1 kA", "Estimate", "Heat source, 50 Hz"],
          ["Resistivity, conductivity", "30 µΩ·m, 20 W/(m·K)", "ASSUMED", "Material"], ["Films: freeboard, roof, shoes", "150, 30, 300 W/(m²·K)", "ASSUMED", "Convective flux"], ["Study", "Stationary", "n/a", "Heat transfer in solids"]],
      0.6, 1.4, 7.6, [2.6, 2.4, 1.2, 2.2], size=12, row_h=0.5)
table(s, [["Validation check", "Result"], ["Analytic cylinder", "error 3.5 × 10⁻⁸"], ["Mesh refinement", "Tmax within 1.1 °C"], ["Energy balance", "1.5 × 10⁻⁸ W"], ["MATLAB/Octave", "1.5 × 10⁻¹¹ °C"]], 8.5, 1.4, 4.3, [2.2, 2.1], size=12, row_h=0.5)
picture(s, "thermal_sensitivity.png", 0.4, 4.45, 7.4, 2.05)
bullets(s, ["Burden temperature prescribed; cell edge adiabatic; shoes water cooled.", "Inputs marked ASSUMED make the electrode temperatures illustrative."], 8.1, 4.5, 4.7, 2.0, size=14, space_after=4)

# 16 Thermal results
s = new_slide("Thermal Results: Temperature in the Electrode Cell", "Slag, metal and floor temperatures follow from plant data. The temperatures inside the electrode depend on assumed material data.", tag="Chapter 13, Appendix A")
picture(s, "thermal_temperature_field.png", 0.3, 1.35, 7.6, 5.1)
card(s, 8.2, 1.45, 4.5, 1.25, "2.74 MW", "Joule heat in one electrode", vsize=28)
card(s, 8.2, 2.85, 4.5, 1.25, "9.94 m", "500 °C isotherm, 0.34 m above the contact shoes", vsize=28)
card(s, 8.2, 4.25, 4.5, 1.5, "2 550 °C", "highest temperature (2 220 to 3 580 °C over the cases tested)", vsize=28)

# 17 Economics and sensitivity
s = new_slide("Economic Evaluation and Sensitivity", "Chapter 15 figures; the verified model gives R1 479 M and an IRR of 68.7 percent. The NPV is zero only at US$734/t or a capital cost above R1 620 M.", tag="Chapters 15 and 16")
card(s, 0.6, 1.4, 2.85, 1.15, "R402 M", "investment", vsize=26); card(s, 3.65, 1.4, 2.85, 1.15, "R383 M/yr", "profit before tax", vsize=26)
card(s, 6.7, 1.4, 2.85, 1.15, "R1 540 M", "NPV, 15 y at 12 %", vsize=26); card(s, 9.75, 1.4, 2.95, 1.15, "1.4 years", "payback after tax", vsize=26)
picture(s, "F12_npv_tornado.png", 0.4, 2.7, 7.4, 3.75)
bullets(s, [[("Alloy price: ", True), ("largest swing, R1 159 M.", False)], [("Hot-charging saving halved: ", True), ("432 t/d, fails 450.", False)], [("PF 0.93 or LF 0.95: ", True), ("445 or 444 t/d, fails.", False)], [("Auxiliaries: ", True), ("105 % use at a 10 % margin; about 28 % spare needed.", False)]], 8.0, 2.75, 4.8, 3.7, size=14, space_after=5)

# 18 Risk and implementation
s = new_slide("Risk Assessment and Implementation Plan", "Residual ratings assume the mitigations are implemented. Power is raised in three stages, each with numeric entry criteria.", tag="Chapters 17, 18 and 19")
table(s, [["Risk", "Initial", "Residual"], ["R-05 Transformer overload", "16 High", "4 Low"], ["R-08 Auxiliary limits", "16 High", "8 Moderate"], ["R-01 Water ingress", "15 High", "5 Moderate"],
          ["R-02 Roof or gas blowout", "15 High", "10 High"], ["R-04 Hearth or tap-hole failure", "15 High", "10 High"], ["R-03 Electrode breakage", "12 High", "8 Moderate"]],
      0.6, 1.4, 6.4, [3.4, 1.5, 1.5], size=13, row_h=0.46)
card(s, 7.3, 1.4, 2.6, 1.2, "26 months", "to performance test", vsize=24); card(s, 10.1, 1.4, 2.7, 1.2, "4 gates", "G1 to G4", vsize=24)
bullets(s, [[("Stages: ", True), ("57.4, 58.7, 60.0 MW; slag superheat at least 25 °C.", False)], [("Tie-in ", True), ("in the annual shutdown, month 18.", False)], [("Acceptance: ", True), ("450 t/d, SEC at most 3.5 MWh/t, loading within 65 MVA.", False)]], 7.3, 2.85, 5.5, 2.4, size=14, space_after=4)
bullets(s, ["Excluded: new transformer, PF above 0.95, raised electrode tips, pre-reduction plant."], 0.6, 4.95, 6.4, 1.5, size=14)

# 19 Power BI
s = new_slide("Power BI Dashboard: Five Pages", "Fifteen tables in a star schema, DAX measures, a theme and a build guide. The .pbix is built in Power BI Desktop from the dataset in about ten minutes.", tag="Appendix B")
pgs = [("PBI_page1_overview.png", "1 Baseline against C1"), ("PBI_page2_electrical.png", "2 Electrical loading"), ("PBI_page3_massbalance.png", "3 Mass balance"), ("PBI_page4_optimisation.png", "4 Optimisation"), ("PBI_page5_verification.png", "5 Verification")]
for i, (f_, lab) in enumerate(pgs):
    row, col = divmod(i, 3)
    x = 0.4 + col * 4.3; y = 1.4 + row * 2.75
    picture(s, f_, x, y, 4.1, 2.3); caption(s, lab, x, y + 2.3, 4.1, size=12)
b, tf = textbox(s, 8.7, 4.15, 4.3, 2.3)
add_par(tf, "No typed numbers: change an input, run the model, refresh.", size=14, first=True, bullet=True, space_after=4)
add_par(tf, "Red marks only failed criteria; green only a pass.", size=14, bullet=True, space_after=4)
add_par(tf, "Every page states that electrode values are estimates.", size=14, bullet=True)

# 20 MATLAB, Excel, files
s = new_slide("MATLAB Dashboard, Excel Model and Digital Files", "saf_dashboard.m draws six panels from numeric files written by the model. Only its data part could be run here; the image is rendered from the same files. Run it once in MATLAB before presenting.", tag="Appendices C and D")
picture(s, "MATLAB_dashboard_preview.png", 0.3, 1.35, 6.9, 3.45)
bullets(s, [[("Verification: ", True), ("104/104 electrical, 18/18 mass balance and optimum, NPV to 2e-15, thermal 1.5e-11 °C.", False)], [("Excel: ", True), ("264 live formulas, six sheets, no errors.", False)], [("Python ", True), ("is the reference; MATLAB (run in Octave) repeats each calculation.", False)]], 7.4, 1.45, 5.4, 3.7, size=14, space_after=5)
table(s, [["Group", "Files", "Tool"], ["CAD and views", "STEP assembly, solids, revolve-cut DXF, section, top, side, bottom", "CadQuery, SolidWorks, COMSOL"], ["Thermal and model", "thermal_fvm.py, safmodel package, octave_check.m", "Python, Octave"], ["Workbook, dashboards", "SAF_Engineering_Model.xlsx, Power BI dataset, saf_dashboard.m", "Excel, Power BI, MATLAB"]],
      0.6, 4.95, 12.1, [2.4, 6.6, 3.1], size=12, row_h=0.3)

# 21 Conclusions
s = new_slide("Conclusions and Recommendations", "Chapter 20 and the verified model. Gate G1 settles the open measurements before capital is spent.", tag="Chapter 20")
b, tf = textbox(s, 0.6, 1.4, 6.0, 5.0)
add_par(tf, [("Conclusions", True)], size=20, first=True, space_after=6, color=BLUE)
for t in ["C1 (60 MW mean plus hot charging) is selected: about 455 t/d.", "Cr recovery 86.9 %; flux 0.366 t/t; duties rise 15.5 %.", "NPV about R1 540 M, positive in every case tested.", "The 450 t/d target binds: saving, LF 0.972 and PF 0.95 must all be delivered.", "Optimum 452 °C; robust only at about 610 °C."]:
    add_par(tf, t, size=15, bullet=True, space_after=5)
b, tf = textbox(s, 6.9, 1.4, 5.9, 5.0)
add_par(tf, [("Before capital release", True)], size=20, first=True, space_after=6, color=BLUE)
for t in ["Plant trial to measure the hot-charging saving.", "Meter power factor and load factor.", "Survey auxiliary capacities.", "Replace estimated electrode values with measurements.", "SolidWorks dimensions, paste and refractory data and one measured electrode temperature for the thermal model."]:
    add_par(tf, t, size=15, bullet=True, space_after=5)

# 22 References
s = new_slide("References and Questions", "TUT Harvard style: author names in capitals, titles of books, reports and journals in italics. The full list of 38 references is in the report.", tag="References")
refs = [
    [("BARKER, I.J. 2011. Some considerations on future developments in ferroalloy furnaces. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 111(10):721-728.", False)],
    [("CADQUERY CONTRIBUTORS. n.d. ", False), ("CadQuery documentation", True), (". [Online]. Available: https://cadquery.readthedocs.io [Accessed 27 November 2026].", False)],
    [("CARSLAW, H.S. and JAEGER, J.C. 1959. ", False), ("Conduction of heat in solids", True), (". 2nd edition. Oxford: Clarendon Press.", False)],
    [("COMSOL AB. n.d. ", False), ("Heat transfer module", True), (". [Online]. Available: https://www.comsol.com/heat-transfer-module [Accessed 27 November 2026].", False)],
    [("DE WAAL, A. et al. 1992. Electrical factors affecting the economic optimization of submerged-arc furnaces. In: ", False), ("Proceedings of INFACON 6", True), (", Cape Town, 1:247-252.", False)],
    [("ESKOM HOLDINGS SOC LTD. 2026. ", False), ("2026/2027 tariff increase: distribution", True), (". Johannesburg: Eskom.", False)],
    [("FERROCHROME DATA WORKBOOK. 2026. ", False), ("Ferrochrome_Data_Workbook.xlsx", True), (". Unpublished data set supplied by the project supervisor.", False)],
    [("GASIK, M. (ed.). 2013. ", False), ("Handbook of ferroalloys: theory and technology", True), (". Oxford: Butterworth-Heinemann/Elsevier.", False)],
    [("GNU OCTAVE. n.d. ", False), ("GNU Octave documentation", True), (". [Online]. Available: https://docs.octave.org [Accessed 27 November 2026].", False)],
    [("MAGNUSSEN, T.E. 2018. Basic parameters in the operation and design of submerged arc furnaces. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 118(6):631-636.", False)],
    [("MATHWORKS. n.d. ", False), ("MATLAB documentation", True), (". [Online]. Available: https://www.mathworks.com/help/matlab/ [Accessed 27 November 2026].", False)],
    [("MICROSOFT. n.d. ", False), ("Power BI documentation", True), (". [Online]. Available: https://learn.microsoft.com/en-us/power-bi/ [Accessed 27 November 2026].", False)],
    [("PATANKAR, S.V. 1980. ", False), ("Numerical heat transfer and fluid flow", True), (". New York: Hemisphere Publishing.", False)],
    [("SWEETEN, N.J. et al. 2018. Chrome ore mineralogy and the furnace mass and energy balance. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 118(6):637-643.", False)],
]
for col in range(2):
    tb, tf = textbox(s, 0.5 + col * 6.3, 1.35, 6.1, 4.7)
    for i, parts in enumerate(refs[col * 7:(col + 1) * 7]):
        p = add_par(tf, [parts[0]], size=11, first=(i == 0), space_after=4, align=PP_ALIGN.JUSTIFY)
        for text, ital in parts[1:]:
            r = p.add_run(); r.text = text; set_run(r, 11, False, DARK, italic=ital)
b, tf = textbox(s, 0.6, 6.0, 12.1, 0.5)
add_par(tf, [("Thank you. Questions?", True)], size=22, first=True, align=PP_ALIGN.CENTER, color=BLUE)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
