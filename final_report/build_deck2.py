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


# =====================================================================================
# 1. Title (template picture kept; its baked text is covered and rewritten)
# =====================================================================================
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
s1.notes_slide.notes_text_frame.text = "Final presentation of the MPG 118S project. The slides follow the order of the report: chapters 1 to 20, then the digital tools (CAD and thermal model, Power BI, MATLAB, Excel) and the references."

# =====================================================================================
# 2. Outline
# =====================================================================================
s = new_slide("Presentation Outline", "The order follows the report. Each slide carries the chapter number in its top-left corner.")
left = ["1-2  Executive summary, background and problem", "3-5  Existing process, design basis, assumptions", "6-7  Literature review, existing condition",
        "8  Mass balance and optimisation", "9-11  Energy, electrical and metallurgical analysis", "12  Alternatives and selected design"]
right = ["13  Detailed calculations, CAD and thermal model", "14-16  Equipment, economics, sensitivity", "17-19  Risk, recommended design, implementation",
         "Digital tools: Python, MATLAB, Excel, Power BI", "20  Conclusions and recommendations", "References and questions"]
b, tf = textbox(s, 0.8, 1.6, 5.9, 4.7)
for i, t in enumerate(left):
    add_par(tf, t, size=19, first=(i == 0), space_after=14, bullet=True)
b, tf = textbox(s, 7.0, 1.6, 5.9, 4.7)
for i, t in enumerate(right):
    add_par(tf, t, size=19, first=(i == 0), space_after=14, bullet=True)

# =====================================================================================
# 3. Executive summary
# =====================================================================================
s = new_slide("Executive Summary: C1 Is Worth Doing, With Gates", "C1 = 60 MW mean power (PF 0.95, LF 0.972) on the existing 65 MVA transformers plus hot charging of the pellets at about 500 C.", tag="Chapter 1")
card(s, 0.6, 1.5, 3.9, 1.5, "455 t/d", "C1 production, from 394 t/d today")
card(s, 4.7, 1.5, 3.9, 1.5, "R1 540 M", "net present value, IRR about 70 %")
card(s, 8.8, 1.5, 3.9, 1.5, "R402 M", "total investment")
bullets(s, [
    [("Binding limit: ", True), ("the 450 t/d target, not the economics; the hot-charging saving, the load factor of 0.972 and PF 0.95 must all be delivered.", False)],
    [("Mass balance: ", True), ("Cr recovery 86.9 %, flux 0.366 t/t; the plant data are consistent (closure -0.41 %).", False)],
    [("Optimisation: ", True), ("452 °C is the least preheat; a plant trial makes C1 robust at about 610 °C.", False)],
    [("Verified ", True), ("in Python, MATLAB and Excel, with a Power BI dashboard and a CAD and thermal model.", False)],
], 0.6, 3.25, 12.1, 3.2, size=18, space_after=6)

# =====================================================================================
# 4. Background
# =====================================================================================
s = new_slide("Background and Motivation", "Electricity is the heat source and one of the largest operating costs.", tag="Chapters 1 and 2")
bullets(s, [
    [("Electricity is the heat source and a major cost ", True), ("of ferrochrome smelting in a submerged arc furnace.", False)],
    "Eskom tariffs rose 12.74 % in April 2025 and 8.76 % in April 2026, while the alloy price is set in US dollars.",
    "Competitiveness must come from the furnace: more alloy from the same electrical installation, at lower energy per tonne.",
    [("Brief: ", True), ("uprate the existing closed, three-phase furnace to 60 MW mean power on its 65 MVA transformers.", False)],
], 0.6, 1.5, 7.4, 4.9, size=19)
card(s, 8.5, 1.5, 4.2, 1.5, "57.43 MW", "mean power today (60.45 MW on load)")
card(s, 8.5, 3.15, 4.2, 1.5, "393.65 t/d", "alloy production today")
card(s, 8.5, 4.8, 4.2, 1.5, "3.5 MWh/t", "specific energy today")

# =====================================================================================
# 5. Problem
# =====================================================================================
s = new_slide("Problem Statement and Constraints", "At a fixed transformer rating production can only rise through power factor, load factor or specific energy.", tag="Chapter 2")
box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.45), Inches(12.1), Inches(1.45))
box.adjustments[0] = 0.08
box.fill.solid(); box.fill.fore_color.rgb = LIGHT; box.line.fill.background(); box.shadow.inherit = False
tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = tf.margin_right = Inches(0.25)
add_par(tf, [("How can the existing furnace be uprated to 60 MW mean power on its 65 MVA transformers, keeping the existing infrastructure, and can it deliver at least 450 t/d?", False)], size=20, first=True, space_after=0)
tf.paragraphs[0].runs[0].font.italic = True
b, tf = textbox(s, 0.6, 3.1, 5.9, 3.3)
add_par(tf, [("Central difficulty", True)], size=20, first=True, space_after=6, color=BLUE)
add_par(tf, "Mean power = rating × power factor × load factor.", size=18, bullet=True)
add_par(tf, "450 t/d at 3.5 MWh/t needs 65.6 MW mean, more than the transformers can deliver.", size=18, bullet=True)
add_par(tf, [("The specific energy must also fall.", True)], size=18, bullet=True)
b, tf = textbox(s, 6.9, 3.1, 5.8, 3.3)
add_par(tf, [("Constraints", True)], size=20, first=True, space_after=6, color=BLUE)
add_par(tf, "Transformer fixed at 65 MVA; power factor at most 0.95.", size=18, bullet=True)
add_par(tf, "Shell, hearth, roof and Søderberg electrodes retained.", size=18, bullet=True)
add_par(tf, "Slag superheat of only about 44 °C.", size=18, bullet=True)

# =====================================================================================
# 6. Existing process
# =====================================================================================
s = new_slide("Existing Process: Closed Three-Phase SAF", "Chromite ore is reduced by carbon with electrical energy released in the burden by three Soderberg electrodes.", tag="Chapter 3")
table(s, [["Item", "Description"],
          ["Ore", "80 % pellets and 20 % lumpy ore; Cr₂O₃ 39.8 %, FeO 25.0 %"],
          ["Flux", "55 % quartz and 45 % limestone"],
          ["Reductant", "10 % coke, 54 % anthracite 1, 36 % anthracite 2"],
          ["Electrical", "3 single-phase transformers of 21.67 MVA; 3 Søderberg electrodes"],
          ["Products", "Alloy 50.4 % Cr; slag with 9.5 % Cr₂O₃, basicity 0.95"],
          ["Auxiliaries", "Cooling water, gas extraction and cleaning, material handling"]],
      0.6, 1.45, 12.1, [2.0, 10.1], size=15, row_h=0.5)
bullets(s, [
    "Reduction: FeO + C → Fe + CO and Cr₂O₃ + 3C → 2Cr + 3CO.",
    "Heat is released in the burden around the electrode tips; metal and slag separate by density and are tapped.",
], 0.6, 5.1, 12.1, 1.3, size=17, space_after=4)

# =====================================================================================
# 7. Design basis
# =====================================================================================
s = new_slide("Design Basis and Acceptance Criteria", "Plant data govern; literature and assumptions are used only where the plant data are silent.", tag="Chapter 4")
table(s, [["Criterion", "Requirement"], ["Apparent power", "Not above 65 MVA"], ["Power factor", "0.93 to 0.95"], ["Production", "At least 450 t/d"],
          ["Specific energy", "Not above 3.5 MWh/t"], ["Slag superheat", "Positive"], ["Auxiliary utilisation", "Not above 90 %"], ["Net present value", "Positive"]],
      0.6, 1.5, 6.6, [2.8, 3.8], size=16, row_h=0.52)
b, tf = textbox(s, 7.6, 1.5, 5.1, 4.8)
add_par(tf, [("Hierarchy of data sources", True)], size=20, first=True, space_after=8, color=BLUE)
for i, t in enumerate(["Supervisor-confirmed plant data", "Project brief", "Published literature", "Documented assumptions"]):
    add_par(tf, [(f"{i + 1}.  ", True), (t, False)], size=18, space_after=8)
add_par(tf, "Every value carries a provenance tag: [WB] data, [S] brief, [L] literature, [A] assumption, [C] calculated.", size=16, space_after=0)

# =====================================================================================
# 8. Assumptions
# =====================================================================================
s = new_slide("Assumptions Register: Four Critical Assumptions", "28 assumptions are listed with confidence and status in Chapter 5.", tag="Chapter 5")
table(s, [["ID", "Assumption", "Confidence", "Tested in"],
          ["A-24", "Hot charging saves 0.07 MWh/t per 100 K (vendor rule)", "Low, critical", "Chapters 8, 16"],
          ["A-22", "Auxiliary systems have a 10 % design margin", "Low, critical", "Chapter 16"],
          ["A-23", "Existing secondary tap range 260 to 340 V", "Low, critical", "Chapter 10"],
          ["A-17", "Reactance can be cut by 20 %", "Low", "Chapter 16"],
          ["A-05", "Baseline power factor 0.93 (assumed in the data)", "Medium", "Gate G1: metering"]],
      0.6, 1.5, 12.1, [1.0, 6.6, 2.0, 2.5], size=15, row_h=0.6)
bullets(s, ["Measured values replace assumptions at the measurement gate before capital is committed.", "Economic assumptions (price US$1 500/t, R17.42 per US$, R1.65/kWh) are varied in the sensitivity analysis."], 0.6, 5.3, 12.1, 1.3, size=17)

# =====================================================================================
# 9. Literature review
# =====================================================================================
s = new_slide("Literature Review: What Limits a Power Increase", "Power cannot be raised independently of the transformer, electrodes and electrical circuit.", tag="Chapter 6")
table(s, [["Source", "Contribution to this design"],
          ["Barker (2011)", "Scale-up is limited by reactance and electrode current capacity"],
          ["De Waal et al. (1992)", "Furnace represented by resistance and reactance; throughput within limits"],
          ["Magnussen (2018)", "Electrode spacing, diameter, resistance and reactance decide performance"],
          ["Sweeten et al. (2018)", "Ore mineralogy governs the mass and energy balance"],
          ["Westly (1974)", "Current from similarity relation I = C₃ P^(2/3); used as an estimate only"]],
      0.6, 1.5, 12.1, [3.2, 8.9], size=16, row_h=0.62)
bullets(s, ["The 55 MW reference is the existing condition; 60 MW is tested by electrical, mass and energy balances."], 0.6, 5.5, 12.1, 0.9, size=17)

# =====================================================================================
# 10. Existing condition
# =====================================================================================
s = new_slide("Existing Condition: Where 60 MW Mean Power Is Possible", "Mean power = S x PF x LF. Every 0.001 of load factor is worth about 0.06 MW.", tag="Chapters 4 and 7")
picture(s, "F1_operating_envelope.png", 0.5, 1.4, 7.4, 5.0)
bullets(s, [
    [("PF 0.95 and LF of at least 0.972 ", True), ("are needed together.", False)],
    "The plant data reproduce 393.65 t/d at 57.43 MW to 0.04 %.",
    "Chromium recovery is about 87 %, not the 78 % assumed.",
    "No electrical measure alone reaches 450 t/d.",
], 8.2, 1.5, 4.6, 4.9, size=18)

# =====================================================================================
# 11-13 Mass balance
# =====================================================================================
s = new_slide("Mass Balance: Seven Balances, Five Unknowns", "The plant data have no stream flows, so the balance is a data reconciliation problem solved by weighted non-negative least squares.", tag="Chapter 8")
picture(s, "F4_mass_balance.png", 0.5, 1.4, 6.6, 5.0)
bullets(s, [
    "Balances on Al₂O₃, MgO, CaO, SiO₂, Cr, Fe and C per tonne of alloy.",
    "Unknowns: ore, dry reductant, quartz, limestone and slag.",
    [("Weighted non-negative least squares ", True), ("in Python, repeated in MATLAB.", False)],
    "Closure -0.41 %; every residual within 3 %.",
], 7.4, 1.5, 5.4, 4.9, size=18)

s = new_slide("Mass Balance Results", "Chromium recovery is 86.9 percent, not the 78 percent in the data. All duties rise 15.5 percent at C1.", tag="Chapter 8")
picture(s, "F6_chromium_recovery.png", 0.5, 1.5, 6.3, 3.0)
table(s, [["Per tonne of alloy", "Value"], ["Ore blend", "2.144 t"], ["Dry reductant", "0.433 t"], ["Flux", "0.366 t"], ["Slag", "1.188 t"], ["Off-gas", "597 Nm³"]],
      7.1, 1.5, 5.6, [3.2, 2.4], size=16, row_h=0.45)
card(s, 0.6, 4.75, 3.9, 1.5, "86.9 %", "chromium recovery (78 % assumed)")
card(s, 4.7, 4.75, 3.9, 1.5, "+15.5 %", "daily duties at C1")
card(s, 8.8, 4.75, 3.9, 1.5, "105 %", "auxiliary use with a 10 % margin")

s = new_slide("Daily Duties and Auxiliary Systems at C1", "Per-tonne rates are fixed by chemistry, so every duty rises with production.", tag="Chapter 8")
picture(s, "F10_daily_duties.png", 0.5, 1.4, 7.4, 5.0)
bullets(s, ["Ore 844 → 975 t/d; slag 468 → 540 t/d.", "Off-gas 9 797 → 11 315 Nm³/h.", "At a 10 % design margin, auxiliary use is 105 %, above the 90 % limit.", "Upgrades are required; the R30 M allowance is essential."], 8.2, 1.5, 4.6, 4.9, size=18)

# =====================================================================================
# 14-16 Optimisation
# =====================================================================================
s = new_slide("How the Optimisation Was Achieved", "Step one finds the least intervention, step two tests it against uncertainty, step three designs it to hold.", tag="Chapter 8")
b, tf = textbox(s, 0.6, 1.4, 12.1, 0.9)
add_par(tf, [("Minimise the preheat temperature T  subject to  production at least 450 t/d,  PF at most 0.95,  S on load at most 65 MVA", True)], size=18, first=True, align=PP_ALIGN.CENTER)
labels = [("1  Deterministic", "SLSQP, checked by the closed form and in MATLAB", "T* = 452 °C"),
          ("2  Monte Carlo", "100 000 samples of the uncertain inputs", "Meets 450 t/d in about 10 % of cases"),
          ("3  Robust", "Chance-constrained design temperature", "About 610 °C once the saving is verified")]
for i, (h, d_, r_) in enumerate(labels):
    x = 0.6 + i * 4.2
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.5), Inches(3.7), Inches(3.0))
    sh.adjustments[0] = 0.06
    sh.fill.solid(); sh.fill.fore_color.rgb = LIGHT; sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.2); tf.margin_top = Inches(0.2)
    add_par(tf, [(h, True)], size=22, first=True, space_after=10, color=BLUE)
    add_par(tf, d_, size=17, space_after=14)
    add_par(tf, [(r_, True)], size=19, space_after=0)
    if i < 2:
        arrow(s, x + 3.72, 3.7, 0.46, 0.5)
b, tf = textbox(s, 0.6, 5.75, 12.1, 0.7)
add_par(tf, "Closed form: T* = T_ref + 100 (SEC0 - 24 S PF LF / 450) / s, with s = 0.07 MWh/t per 100 K from ambient 25 °C.", size=16, first=True, align=PP_ALIGN.CENTER, color=GREY)

s = new_slide("Optimum 452 °C, but Only a 10 % Chance of 450 t/d", "Each extra 0.01 of load factor saves about 48 degrees of preheat. The Monte Carlo result is driven by the unverified hot-charging saving.", tag="Chapter 8")
picture(s, "F7_optimisation_map.png", 0.4, 1.4, 6.2, 4.3)
picture(s, "F8_montecarlo.png", 6.7, 1.4, 6.2, 4.3)
caption(s, "Minimum preheat for 450 t/d", 0.4, 5.75, 6.2)
caption(s, "100 000 Monte Carlo samples of C1 production", 6.7, 5.75, 6.2)
b, tf = textbox(s, 0.6, 6.05, 12.1, 0.5)
add_par(tf, [("Design temperature of 500 °C leaves a 48 °C margin; median production is 438 t/d.", True)], size=17, first=True, align=PP_ALIGN.CENTER)

s = new_slide("Robust Design: Verify the Saving First", "Without a plant trial no practical temperature is robust. A trial that confirms the vendor saving makes C1 robust at about 610 C.", tag="Chapter 8")
picture(s, "F11_robust_optimisation.png", 0.4, 1.4, 7.0, 4.9)
table(s, [["Hot-charging saving", "T for 50 %", "T for 90 %"], ["Unverified", "670 °C", "925 °C"], ["Verified, full vendor value", "520 °C", "610 °C"], ["Verified, 75 % of vendor", "670 °C", "780 °C"]],
      7.6, 1.5, 5.2, [2.6, 1.3, 1.3], size=14, row_h=0.55)
bullets(s, [[("Plant trial before capital release ", True), ("is the cheapest risk reduction.", False)], "Design the preheater for about 610 °C."], 7.6, 4.0, 5.2, 2.4, size=18)

# =====================================================================================
# 17 Energy balance
# =====================================================================================
s = new_slide("Energy Balance and Hot Charging", "The vendor rule describes heating of the whole charge, so the scope of the hot charging system must be defined by feed heat.", tag="Chapter 9")
card(s, 0.6, 1.5, 3.9, 1.6, "2.90 MWh/t", "process requirement")
card(s, 4.7, 1.5, 3.9, 1.6, "0.15 MWh/t", "electrical circuit loss")
card(s, 8.8, 1.5, 3.9, 1.6, "0.46 MWh/t", "thermal loss")
bullets(s, [
    "Reduction of the oxides takes 1.66 MWh/t of the 3.50 MWh/t.",
    [("Pellets at 500 °C return 712 MJ/t: ", True), ("444 t/d at 60 MW, just below the gate.", False)],
    [("Pellets, lumpy ore and fluxes at 500 °C: ", True), ("463 t/d.", False)],
    "The 450 t/d gate needs a feed heat of at least 832 MJ/t.",
], 0.6, 3.4, 12.1, 3.0, size=20)

# =====================================================================================
# 18-19 Electrical
# =====================================================================================
s = new_slide("Electrical Analysis: No Transformer Headroom", "Eight scenarios on one 65 MVA basis. 47 of 52 numbers of the earlier chapters are reproduced.", tag="Chapter 10")
picture(s, "F2_transformer_loading.png", 0.5, 1.4, 7.6, 4.8)
bullets(s, [
    [("S-B, 60 MW mean: ", True), ("64.98 MVA, 100 % of rating.", False)],
    [("S-N60, continuous: ", True), ("64.52 MVA, but needs a load factor of 1.", False)],
    [("S-O60, 60 MW on load: ", True), ("only 57.0 MW mean, 391 t/d, below today.", False)],
    "Python and MATLAB agree on 104 of 104 values.",
], 8.4, 1.5, 4.4, 4.9, size=18)

s = new_slide("Raising the Power Factor: Two Routes", "These ratios do not depend on the uncertain Westly constant, so the result is robust.", tag="Chapter 10")
picture(s, "F3_pf_route_current_density.png", 0.5, 1.4, 7.4, 4.9)
bullets(s, [
    [("Raise operating resistance: ", True), ("electrode current falls 7.8 % at PF 0.95.", False)],
    [("Lower reactance ", True), ("(the selected conductor rearrangement): current rises 1.1 %.", False)],
    "Estimated current density at C1 is 6.90 A/cm², 1.5 % above 6.80, so criterion DC-04 must be revisited.",
], 8.2, 1.5, 4.6, 4.9, size=18)

# =====================================================================================
# 20 Process / metallurgical
# =====================================================================================
s = new_slide("Process and Metallurgical Analysis", "Findings of Chapter 11. The slag margin of 44 C is the reason the electrodes are not raised.", tag="Chapter 11")
card(s, 0.6, 1.5, 3.9, 1.5, "87 %", "chromium recovery; 90 % planning value, 93 % target")
card(s, 4.7, 1.5, 3.9, 1.5, "44 °C", "mean slag superheat; stop-increase level 25 °C")
card(s, 8.8, 1.5, 3.9, 1.5, "58 %", "pellet metallisation needed for 2.41 MWh/t")
bullets(s, [
    "FeO, Cr₂O₃ and SiO₂ reduce above about 746, 1 218 and 1 637 °C; the slag at 1 730 to 1 800 °C exceeds all three.",
    "The flux of 0.449 t/t is more than the slag chemistry needs (about 0.33 to 0.39 t/t); Chapter 8 gives 0.366 t/t.",
    "At 40 to 50 % metallisation the specific energy is 2.58 to 2.77 MWh/t, so 2.41 MWh/t is a long-term ambition.",
], 0.6, 3.3, 12.1, 3.2, size=18)

# =====================================================================================
# 21-22 Alternatives
# =====================================================================================
s = new_slide("Alternatives: Only Two Combinations Reach 450 t/d", "Values from the alternatives chapter with the preheat measured from 0 C. The verified model gives 454.6 t/d for C1 with the ambient reference.", tag="Chapter 12")
table(s, [["Alternative", "Mean power (MW)", "SEC (MWh/t)", "Production (t/d)", "450 t/d"],
          ["E0 existing", "57.43", "3.50", "393.8", "No"], ["E1 PF 0.95", "58.66", "3.50", "402.3", "No"], ["E2 PF 0.95, LF 0.972", "60.00", "3.50", "411.4", "No"],
          ["P1 hot charging", "57.43", "3.15", "437.5", "No"], ["P2 pre-reduced pellets", "57.43", "2.41", "571.9", "Yes"],
          ["C1 E2 + P1", "60.00", "3.15", "457.1", "Yes"], ["C2 E2 + P2", "60.00", "2.41", "597.5", "Yes"]],
      0.6, 1.5, 8.2, [3.2, 1.8, 1.6, 1.8, 1.0], size=15, row_h=0.5)
bullets(s, [[("C1 ranked first ", True), ("under every weighting tested.", False)], "P2 and C2 would exceed the gas, tapping and slag systems.", "Pre-reduction is kept as a longer-term route."], 9.1, 1.5, 3.7, 4.9, size=17)

s = new_slide("Selected Design C1 and Investment", "Capital figures are early-stage estimates with an accuracy of minus 40 to plus 40 percent.", tag="Chapters 12 and 14")
bullets(s, [
    [("Power factor 0.93 to 0.95 ", True), ("by rearranging the conductor bars.", False)],
    [("Load factor 95 % to 97.2 % ", True), ("by electrode care and instrumentation.", False)],
    [("Pellets hot-charged at about 500 °C ", True), ("to cut energy per tonne.", False)],
    "Transformers, furnace shell and Søderberg electrodes retained.",
], 0.6, 1.5, 6.0, 4.9, size=19)
table(s, [["Item", "R million"], ["Conductor rearrangement", "45"], ["Transformer monitoring", "25"], ["Controls and metering", "10"], ["Auxiliary upgrades", "30"],
          ["Hot-charging allowance", "200"], ["Contingency (20 %)", "62"], ["Shutdown production loss", "30"], ["Total investment", "402"]],
      7.0, 1.5, 5.7, [3.8, 1.9], size=15, row_h=0.5, bold_last=True)

# =====================================================================================
# 23 Detailed calculations
# =====================================================================================
s = new_slide("Detailed Calculations of C1", "All values calculated in the verified model and repeated in MATLAB.", tag="Chapter 13")
table(s, [["Quantity", "Equation", "Value"],
          ["Mean power", "65 × 0.95 × 0.972", "60.02 MW"],
          ["On-load apparent power", "(60 / 0.972) / 0.95", "64.98 MVA (99.97 %)"],
          ["Electrode current (estimate)", "8.33 × P_on^(2/3)", "130.1 kA"],
          ["Specific energy", "3.50 - 0.07 × (500 - 25)/100", "3.1675 MWh/t"],
          ["Production", "24 × 60 / 3.1675", "454.6 t/d"],
          ["Least preheat for 450 t/d", "T* closed form", "452 °C"]],
      0.6, 1.5, 12.1, [3.8, 4.6, 3.7], size=16, row_h=0.6)
bullets(s, ["The margin in specific energy is only 1.0 %, so the hot-charging saving must be verified before capital is committed."], 0.6, 5.9, 12.1, 0.8, size=17)

# =====================================================================================
# 24-28 CAD and thermal model
# =====================================================================================
s = new_slide("CAD Model of the Furnace and Revolve Cut", "The geometry was rebuilt in CadQuery from the SolidWorks screenshot. Only four dimensions are plant data; the rest are tagged estimates.", tag="Chapter 13, Appendix A")
picture(s, "iso_open_cut_quarter.png", 0.4, 1.4, 5.0, 5.0)
bullets(s, [
    [("Parametric model: ", True), ("shell, lining, roof, three electrodes with angled feet, two tap pipes.", False)],
    [("Revolve cut: ", True), ("the hearth cavity (radius 5.44 m, height 7.50 m) is cut from the lining block.", False)],
    [("Files: ", True), ("STEP assembly with named bodies, STL, and a DXF half-section for SolidWorks.", False)],
    [("Data: ", True), ("shell 13.70 m, hearth 10.88 m, electrode 1.55 m, pitch circle 4.19 m.", False)],
], 5.6, 1.5, 7.2, 4.9, size=17)

s = new_slide("Open Cut Section A-A with Dimensions", "Section on the plane y = 0 through the axis and electrode 1. Dimensions in metres; an asterisk marks a value estimated from the picture or assumed.", tag="Chapter 13, Appendix A")
picture(s, "view_section_open_cut.png", 0.4, 1.35, 6.4, 5.15)
picture(s, "iso_full.png", 7.0, 1.35, 3.0, 5.15)
bullets(s, ["Lining 1.41 m, hearth 10.88 m, electrode 1.55 m.", "Electrode column from the tip at z = 1.50 m through the roof.", "Replace values in params.py to update every view."], 10.1, 1.5, 2.9, 4.9, size=14, space_after=6)

s = new_slide("Top, Side and Bottom Views with Dimensions", "Electrodes E1 to E3 at 0, 120 and 240 degrees; tap pipes T1 and T2 at -145 and -35 degrees. The drawing sheet with all four views is in Appendix A.", tag="Chapter 13, Appendix A")
picture(s, "view_top.png", 0.3, 1.4, 4.2, 4.6)
picture(s, "view_side.png", 4.6, 1.4, 4.2, 4.6)
picture(s, "view_bottom.png", 8.9, 1.4, 4.2, 4.6)
caption(s, "Top view", 0.3, 6.05, 4.2, size=13); caption(s, "Side view (front elevation)", 4.6, 6.05, 4.2, size=13); caption(s, "Bottom view", 8.9, 6.05, 4.2, size=13)

s = new_slide("Thermal Model of the Electrode (COMSOL-Type)", "Steady heat conduction with Joule heating including the skin effect, finite volume, axisymmetric unit cell. The COMSOL set-up is listed in Appendix A.", tag="Chapter 13, Appendix A")
table(s, [["Input", "Value", "Tag", "COMSOL feature"],
          ["Slag, metal temperature", "1 800, 1 732 °C", "DATA", "Temperature"],
          ["Electrode current", "130.1 kA", "Estimate", "Heat source, 50 Hz"],
          ["Resistivity, conductivity", "30 µΩ·m, 20 W/(m·K)", "ASSUMED", "Material"],
          ["Films: freeboard, roof, shoes", "150, 30, 300 W/(m²·K)", "ASSUMED", "Convective flux"],
          ["Study", "Stationary", "n/a", "Heat transfer in solids"]],
      0.6, 1.5, 12.1, [3.4, 3.3, 1.6, 3.3], size=15, row_h=0.55)
bullets(s, ["Burden temperature is prescribed from the process; the cell edge is adiabatic; contact shoes are water cooled.", "The geometry imports from the STEP file; no .mph file was made because COMSOL was not available."], 0.6, 5.1, 12.1, 1.6, size=17)

s = new_slide("Thermal Results: Temperature in the Electrode Cell", "Temperatures of slag, metal and floor follow from plant data. Temperatures inside the electrode depend on assumed material data and are illustrative.", tag="Chapter 13, Appendix A")
picture(s, "thermal_temperature_field.png", 0.3, 1.35, 7.6, 5.1)
card(s, 8.2, 1.5, 4.5, 1.3, "2.74 MW", "Joule heat in one electrode", vsize=30)
card(s, 8.2, 3.0, 4.5, 1.3, "9.94 m", "500 °C isotherm, 0.34 m above the contact shoes", vsize=30)
card(s, 8.2, 4.5, 4.5, 1.6, "2 550 °C", "highest temperature (2 220 to 3 580 °C over the cases tested)", vsize=30)

s = new_slide("Thermal Model: Validation and Sensitivity", "Analytic case, mesh refinement, energy balance and an independent Octave solution all pass.", tag="Chapter 13, Appendix A")
picture(s, "thermal_sensitivity.png", 0.3, 1.4, 7.6, 3.9)
table(s, [["Check", "Result"], ["Analytic cylinder", "error 3.5 × 10⁻⁸"], ["Mesh 1 440 to 22 992 cells", "Tmax within 1.1 °C"], ["Energy balance", "residual 1.5 × 10⁻⁸ W"], ["MATLAB/Octave solution", "difference 1.5 × 10⁻¹¹ °C"]],
      8.1, 1.5, 4.7, [2.5, 2.2], size=14, row_h=0.5)
bullets(s, ["Resistivity, conductivity and current move the maximum temperature by more than 1 000 °C; the baking zone moves only 0.5 m.", "Needed: SolidWorks dimensions, paste and refractory data, one measured temperature."], 0.6, 5.4, 12.1, 1.2, size=16, space_after=2)

# =====================================================================================
# 29 Equipment
# =====================================================================================
s = new_slide("Equipment and Design Requirements", "Packages and allowances of Chapter 14; auxiliary duties scaled from the mass balance.", tag="Chapter 14")
table(s, [["Package", "Requirement", "R million"],
          ["Conductor works", "Rearrange busbars and flexibles; PF 0.93 to 0.95", "45"],
          ["Transformer monitoring", "Winding and oil temperature, tap position, thermal confirmation", "25"],
          ["Controls and metering", "Power-quality meters, electrode baking and slip monitors, clamps", "10"],
          ["Auxiliary upgrades", "Gas cleaning, slag handling, tapping, cooling to the C1 duties", "30"],
          ["Hot-charging system", "Insulated conveyance, hot-rated bins, dust control", "200"]],
      0.6, 1.5, 12.1, [2.9, 7.6, 1.6], size=15, row_h=0.62)
bullets(s, ["Electrodes stay as they are: 1.55 m Søderberg, no replacement, raising or resizing.", "Reaching 60 MW mean needs the furnace on load 97.2 % of the time."], 0.6, 5.4, 12.1, 1.3, size=17)

# =====================================================================================
# 30 Economics
# =====================================================================================
s = new_slide("Economic Evaluation", "Chapter 15 figures. The verified model gives R1 479 M and an IRR of 68.7 percent with the conservative production of 454.8 t/d.", tag="Chapter 15")
card(s, 0.6, 1.5, 3.9, 1.5, "R402 M", "total investment")
card(s, 4.7, 1.5, 3.9, 1.5, "R383 M/yr", "incremental profit before tax")
card(s, 8.8, 1.5, 3.9, 1.5, "R1 540 M", "net present value, 15 years at 12 %")
table(s, [["Indicator", "Value"], ["Extra production", "63.3 t/d, 23 105 t/yr"], ["Incremental revenue", "R604 M/yr"], ["Incremental operating cost", "R220.7 M/yr"], ["Internal rate of return", "about 70 %"], ["Payback after tax", "about 1.4 years"]],
      0.6, 3.3, 7.6, [3.8, 3.8], size=16, row_h=0.5)
bullets(s, ["Alloy price US$1 500/t, R17.42 per US$, electricity R1.65/kWh.", "Verified model: R1 479 M, IRR 68.7 %."], 8.6, 3.3, 4.2, 3.0, size=17)

# =====================================================================================
# 31-33 Sensitivity
# =====================================================================================
s = new_slide("Sensitivity: What Moves the NPV", "The NPV stays positive in every case. It reaches zero only at an alloy price of US$734 per tonne or a capital cost above R1 620 M.", tag="Chapter 16")
picture(s, "F12_npv_tornado.png", 0.4, 1.4, 8.4, 4.9)
bullets(s, [[("Alloy price ", True), ("has the largest swing, R1 159 M.", False)], [("Hot-charging saving: ", True), ("R761 M, and 450 t/d fails if halved.", False)], "Capital cost and electricity tariff matter little.", "NPV is zero only at US$734/t."], 9.0, 1.5, 3.8, 4.9, size=17)

s = new_slide("Sensitivity: Electrical and Auxiliary Systems", "Left: at 60 MW mean the transformers reach 65 MVA exactly at PF 0.95. Right: every duty rises 15.5 percent, so auxiliaries need about 28 percent spare capacity.", tag="Chapter 16")
picture(s, "F14_electrical_sensitivity.png", 0.3, 1.4, 6.4, 3.6)
picture(s, "F15_auxiliary_sensitivity.png", 6.65, 1.4, 6.4, 3.6)
caption(s, "Electrical: loading against power factor and mean power against load factor", 0.3, 5.0, 6.4, size=12)
caption(s, "Auxiliary: utilisation and duties against production", 6.65, 5.0, 6.4, size=12)
bullets(s, [[("Electrical: ", True), ("no headroom below PF 0.95; PF 0.93 gives only 445 t/d.", False)], [("Auxiliary: ", True), ("105 % utilisation at a 10 % design margin, so upgrades are required.", False)]], 0.6, 5.45, 12.1, 1.1, size=17, space_after=4)

s = new_slide("Comparison: Economically Robust, Technically at the Limit", "Source: Chapter 16 comparison table. Auxiliary utilisation assumes a 10 % design margin.", tag="Chapter 16")
yes = {"text": "Yes"}
table(s, [["Case", "Production (t/d)", "≥ 450 t/d", "NPV (R M)", "IRR", "Payback (y)"],
          ["Base case C1", "454.8", "Yes", "1 479", "68.7 %", "1.46"], ["Hot-charge saving halved", "432.1", "No", "718", "40.7 %", "2.44"],
          ["Load factor stays 0.95", "444.5", "No", "1 231", "59.6 %", "1.68"], ["Power factor stays 0.93", "445.2", "No", "1 249", "60.2 %", "1.66"],
          ["Alloy price US$1 200/t", "454.8", "Yes", "900", "47.4 %", "2.10"], ["Capital cost +40 %", "454.8", "Yes", "1 339", "50.3 %", "1.98"]],
      0.6, 1.5, 12.1, [4.0, 1.9, 1.5, 1.6, 1.5, 1.6], size=15, row_h=0.52)
b, tf = textbox(s, 0.6, 5.4, 12.1, 1.1)
add_par(tf, [("Three single deviations fail the 450 t/d target while the NPV stays positive: the production target, not the economics, binds the design.", True)], size=18, first=True, color=BLUE)

# =====================================================================================
# 34 Risk
# =====================================================================================
s = new_slide("Risk Assessment", "Initial score is likelihood times consequence; residual assumes the mitigations are implemented.", tag="Chapter 17")
table(s, [["Risk", "Initial", "Residual"],
          ["R-05 Transformer overload", "16 High", "4 Low"], ["R-08 Auxiliary-system limits", "16 High", "8 Moderate"], ["R-01 Water ingress", "15 High", "5 Moderate"],
          ["R-02 Roof or gas blowout", "15 High", "10 High"], ["R-04 Hearth or tap-hole failure", "15 High", "10 High"], ["R-03 Electrode breakage", "12 High", "8 Moderate"],
          ["R-06 Electrical or control instability", "12 High", "8 Moderate"], ["R-07 Reduced chromium recovery", "9 Moderate", "6 Moderate"], ["R-09 Project delays and overruns", "9 Moderate", "6 Moderate"]],
      0.6, 1.4, 8.2, [4.6, 1.8, 1.8], size=14, row_h=0.5)
bullets(s, ["Water ingress, gas blowout and hearth failure keep potentially catastrophic consequences and need continued surveillance.", "Power is raised in stages from 55 to 57.5 to 60 MW, each stage with entry criteria."], 9.1, 1.5, 3.7, 4.9, size=16)

# =====================================================================================
# 35 Recommended design
# =====================================================================================
s = new_slide("Recommended Design and Acceptance Gates", "Chapter 18. The acceptance gate after ramp-up uses the criteria of the design basis.", tag="Chapter 18")
bullets(s, [
    [("Adopt C1: ", True), ("60 MW electrical uprate plus hot charging at about 500 °C; about 457 t/d in Chapter 12 and 454.6 t/d in the verified model.", False)],
    [("Measurement gate: ", True), ("metered PF inside 0.93 to 0.95, measured currents replace estimates.", False)],
    [("Commercial gate: ", True), ("alloy price outlook of at least US$1 200/t.", False)],
    [("Acceptance gate: ", True), ("at least 450 t/d, positive slag superheat, SEC not above 3.5 MWh/t, loading within 65 MVA, no unplanned electrode incident.", False)],
    [("Excluded: ", True), ("new transformer, PF above 0.95, raised electrode tips, pre-reduction plant in this project.", False)],
], 0.6, 1.5, 12.1, 4.9, size=18, space_after=10)

# =====================================================================================
# 36 Implementation
# =====================================================================================
s = new_slide("Implementation Plan: 26 Months, Four Gates", "Chapter 19. The 450 t/d gate needs at least 832 MJ/t of feed heat; the hot-charging option is chosen at Gate G1 on that criterion.", tag="Chapter 19")
card(s, 0.6, 1.5, 3.9, 1.4, "26 months", "from approval to performance test")
card(s, 4.7, 1.5, 3.9, 1.4, "4 gates", "studies, capital, shutdown, acceptance")
card(s, 8.8, 1.5, 3.9, 1.4, "Month 18", "tie-in in the annual shutdown, 3 days float")
bullets(s, [
    [("Measure first, gate the commitment, ", True), ("build off-line, tie in at the shutdown.", False)],
    [("Three power stages: ", True), ("57.4, 58.7 and 60.0 MW with numeric entry criteria, including slag superheat of at least 25 °C.", False)],
    [("Critical path: ", True), ("vendor quotations, capital release, long-lead equipment and the shutdown; a missed tie-in costs about 23 100 t of alloy per year.", False)],
], 0.6, 3.2, 12.1, 3.3, size=18)

# =====================================================================================
# 37-41 Digital tools
# =====================================================================================
s = new_slide("Verification: Python, MATLAB and Excel", "MATLAB was run in GNU Octave. The Excel workbook has 264 live formulas and no errors.", tag="Appendices C and D")
card(s, 0.6, 1.5, 2.85, 1.7, "104/104", "electrical values match MATLAB", vsize=30)
card(s, 3.65, 1.5, 2.85, 1.7, "18/18", "mass balance and optimum match", vsize=30)
card(s, 6.7, 1.5, 2.85, 1.7, "2e-15", "NPV difference, Python against MATLAB", vsize=30)
card(s, 9.75, 1.5, 2.95, 1.7, "1.5e-11 °C", "thermal solver, Python against Octave", vsize=26)
bullets(s, [
    "Python is the reference model; each calculation is repeated independently in MATLAB from the numeric inputs.",
    "Excel: README, Inputs, MassBalance, Electrical, Optimisation and Verification sheets with live formulas.",
    "Every input carries a provenance tag; 47 of 52 numbers from the team's chapters are reproduced and the other five are explained.",
], 0.6, 3.5, 12.1, 3.0, size=18)

s = new_slide("Power BI Dashboard (Pages 1 to 3)", "Five pages, 15 tables in a star schema, DAX measures and a theme. The report pages are rendered from the same dataset.", tag="Appendix B")
for i, (f_, lab) in enumerate([("PBI_page1_overview.png", "1 Baseline against C1"), ("PBI_page2_electrical.png", "2 Electrical loading"), ("PBI_page3_massbalance.png", "3 Mass balance")]):
    x = 0.4 + i * 4.3
    picture(s, f_, x, 1.6, 4.1, 2.35)
    caption(s, lab, x, 4.0, 4.1, size=13)
bullets(s, [[("Question per page: ", True), ("what changes, is there headroom, what goes in and out per tonne.", False)], [("No typed numbers: ", True), ("change an input, run the model, refresh the dashboard.", False)]], 0.6, 4.6, 12.1, 1.9, size=18)

s = new_slide("Power BI Dashboard (Pages 4 and 5)", "Files: SAF_PowerBI_Dataset.xlsx, SAF_measures.dax, SAF_theme.json and the build guide.", tag="Appendix B")
for i, (f_, lab) in enumerate([("PBI_page4_optimisation.png", "4 Optimisation and robustness"), ("PBI_page5_verification.png", "5 Verification and provenance")]):
    x = 0.6 + i * 6.2
    picture(s, f_, x, 1.6, 5.9, 3.3)
    caption(s, lab, x, 4.95, 5.9, size=13)
bullets(s, [[("The .pbix file ", True), ("is built in Power BI Desktop from the dataset in about ten minutes, following the guide.", False)], "Red marks only failed criteria or risks; green only a pass."], 0.6, 5.5, 12.1, 1.1, size=17, space_after=2)

s = new_slide("MATLAB Dashboard", "saf_dashboard.m draws six panels from numeric files written by the model. Only its data part could be run here; the image is rendered from the same files.", tag="Appendix C")
picture(s, "MATLAB_dashboard_preview.png", 0.3, 1.4, 8.6, 5.0)
bullets(s, ["Production and loading of the eight scenarios.", "Mass balance per tonne of alloy.", "Least preheat against load factor.", "NPV tornado.", "Electrode axial temperature.", "Run once in MATLAB before presenting."], 9.1, 1.5, 3.7, 4.9, size=16, space_after=5)

s = new_slide("Digital Files: CAD, COMSOL-Ready and Model Files", "All files are in the project repository; every number in the report can be regenerated by the scripts.", tag="Appendix D")
table(s, [["Group", "Files", "Tool"],
          ["CAD", "furnace_assembly.step, furnace_solid.step, open-cut STEP and STL, revolve-cut DXF", "CadQuery, SolidWorks, COMSOL"],
          ["Views", "Open cut, top, side, bottom and drawing sheet (PNG, PDF, SVG)", "Python"],
          ["Thermal", "thermal_fvm.py, thermal_run.py, results CSV, octave_check.m", "Python, Octave"],
          ["Model", "safmodel package, scenario, mass balance, optimisation, sensitivity scripts", "Python"],
          ["Workbook", "SAF_Engineering_Model.xlsx", "Excel"],
          ["Dashboards", "Power BI dataset, DAX, theme; saf_dashboard.m", "Power BI, MATLAB"]],
      0.6, 1.5, 12.1, [1.8, 7.3, 3.0], size=14, row_h=0.6)

# =====================================================================================
# 42-43 Conclusions
# =====================================================================================
s = new_slide("Conclusions", "Chapter 20 and the verified model.", tag="Chapter 20")
bullets(s, [
    [("C1 ", True), ("(60 MW mean plus hot charging) is the selected design, with about 455 t/d.", False)],
    [("Cr recovery is 86.9 %; ", True), ("flux is 0.366 t/t; all duties rise 15.5 %.", False)],
    [("The NPV is about R1 540 M ", True), ("and positive in every case tested.", False)],
    [("The 450 t/d target binds: ", True), ("hot-charging saving, load factor 0.972 and PF 0.95 must all be delivered.", False)],
    [("The optimum is 452 °C, ", True), ("but only a verified saving makes it robust, at about 610 °C.", False)],
    [("The electrode temperatures ", True), ("rest on assumed material data and need calibration.", False)],
], 0.6, 1.5, 12.1, 4.9, size=19, space_after=10)

s = new_slide("Recommendations and Open Items", "Gate G1 settles the open measurements before capital is spent.", tag="Chapter 20")
b, tf = textbox(s, 0.6, 1.4, 6.0, 5.0)
add_par(tf, [("Before capital release", True)], size=22, first=True, space_after=8, color=BLUE)
for t in ["Plant trial to measure the hot-charging saving.", "Meter the power factor and load factor.", "Survey auxiliary-system capacities.", "Replace estimated electrode values with measurements.", "Design the preheater for about 610 °C."]:
    add_par(tf, t, size=18, bullet=True, space_after=6)
b, tf = textbox(s, 6.9, 1.4, 5.9, 5.0)
add_par(tf, [("Open items", True)], size=22, first=True, space_after=8, color=BLUE)
for t in ["Chapter 14 quotes 63.2 MVA at 97 %; the on-load value is 64.98 MVA (Chapter 10).", "C1 production: 457 t/d (0 °C preheat) or 454.6 t/d (ambient).", "SolidWorks dimensions, paste and refractory data, one measured electrode temperature.", "A 3D COMSOL study of the STEP assembly."]:
    add_par(tf, t, size=17, bullet=True, space_after=6)

# =====================================================================================
# References (TUT Harvard) and thank you
# =====================================================================================
def ref_slide(title, items):
    s = new_slide(title, "TUT Harvard style: author names in capitals, titles of books, reports and journals in italics. The full list is in the report.", tag="References")
    tb, tf = textbox(s, 0.6, 1.35, 12.1, 5.2)
    for i, parts in enumerate(items):
        p = add_par(tf, [parts[0]], size=15, first=(i == 0), space_after=6, align=PP_ALIGN.JUSTIFY)
        for text, ital in parts[1:]:
            r = p.add_run(); r.text = text; set_run(r, 15, False, DARK, italic=ital)
    return s

ref_slide("References (1 of 3)", [
    [("BARKER, I.J. 2011. Some considerations on future developments in ferroalloy furnaces. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 111(10):721-728.", False)],
    [("CADQUERY CONTRIBUTORS. n.d. ", False), ("CadQuery documentation", True), (". [Online]. Available: https://cadquery.readthedocs.io [Accessed 27 November 2026].", False)],
    [("CARSLAW, H.S. and JAEGER, J.C. 1959. ", False), ("Conduction of heat in solids", True), (". 2nd edition. Oxford: Clarendon Press.", False)],
    [("COMSOL AB. n.d. ", False), ("Heat transfer module", True), (". [Online]. Available: https://www.comsol.com/heat-transfer-module [Accessed 27 November 2026].", False)],
    [("DE WAAL, A., BARKER, L.J., RENNIE, M.S., KLOPPER, J. and GROENEVELD, B.S. 1992. Electrical factors affecting the economic optimization of submerged-arc furnaces. In: ", False), ("Proceedings of INFACON 6", True), (", Cape Town, 1:247-252.", False)],
    [("ESKOM HOLDINGS SOC LTD. 2026. ", False), ("2026/2027 tariff increase: distribution", True), (". Johannesburg: Eskom.", False)],
    [("FERROCHROME DATA WORKBOOK. 2026. ", False), ("Ferrochrome_Data_Workbook.xlsx", True), (". Unpublished data set supplied by the project supervisor.", False)],
    [("GASIK, M. (ed.). 2013. ", False), ("Handbook of ferroalloys: theory and technology", True), (". Oxford: Butterworth-Heinemann/Elsevier.", False)],
])
ref_slide("References (2 of 3)", [
    [("GNU OCTAVE. n.d. ", False), ("GNU Octave documentation", True), (". [Online]. Available: https://docs.octave.org [Accessed 27 November 2026].", False)],
    [("LAWSON, C.L. and HANSON, R.J. 1974. ", False), ("Solving least squares problems", True), (". Englewood Cliffs: Prentice-Hall.", False)],
    [("MAGNUSSEN, T.E. 2018. Basic parameters in the operation and design of submerged arc furnaces. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 118(6):631-636.", False)],
    [("MATHWORKS. n.d. ", False), ("MATLAB documentation", True), (". [Online]. Available: https://www.mathworks.com/help/matlab/ [Accessed 27 November 2026].", False)],
    [("METSO. n.d. ", False), ("SAF smelting plant", True), (". [Online]. Available: https://www.metso.com/portfolio/saf-smelting-plant/ [Accessed 18 November 2026].", False)],
    [("MICROSOFT. n.d. ", False), ("Power BI documentation", True), (". [Online]. Available: https://learn.microsoft.com/en-us/power-bi/ [Accessed 27 November 2026].", False)],
    [("MULHOLLAND, A.C. 2009. The effectiveness of current control of submerged arc furnace electrode penetration in selected scenarios. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 109(10).", False)],
    [("NERSA. 2025. ", False), ("Media statement: NERSA's decision on Eskom's MYPD6 revenue application", True), (". Pretoria: NERSA.", False)],
])
ref_slide("References (3 of 3)", [
    [("PATANKAR, S.V. 1980. ", False), ("Numerical heat transfer and fluid flow", True), (". New York: Hemisphere Publishing.", False)],
    [("SCHEI, A., TUSET, J.K. and TVEIT, H. 1998. ", False), ("Production of high silicon alloys", True), (". Trondheim: Tapir Forlag.", False)],
    [("SMM. 2026. Samchrome cuts Q4 European ferrochrome benchmark by 4 cents to 152 US cents/lb. ", False), ("Shanghai Metals Market", True), (", 27 October.", False)],
    [("SMYTHE, W.R. 1968. ", False), ("Static and dynamic electricity", True), (". 3rd edition. New York: McGraw-Hill.", False)],
    [("SWEETEN, N.J., VERRYN, S.M.C., OBERHOLZER, J. and ZIETSMAN, J.H. 2018. Chrome ore mineralogy and the furnace mass and energy balance. ", False), ("Journal of the Southern African Institute of Mining and Metallurgy", True), (", 118(6):637-643.", False)],
    [("VIRTANEN, P. et al. 2020. SciPy 1.0: fundamental algorithms for scientific computing in Python. ", False), ("Nature Methods", True), (", 17:261-272.", False)],
    [("WESTLY, J. 1974. Resistance and heat distribution in a submerged-arc furnace. In: ", False), ("Proceedings of the First International Ferro-Alloys Congress (INFACON I)", True), (", Johannesburg, pp. 121-127.", False)],
    [("YU, Y., LI, B., WANG, C., FANG, Z., YANG, X. and TSUKIHASHI, F. 2019. Evaluation and synergy of material and energy in the smelting process of ferrochrome pellets. ", False), ("Energy", True), (", 179:792-804.", False)],
])

s = new_slide("Thank You", "Questions.")
b, tf = textbox(s, 0.6, 2.2, 12.1, 3.0)
add_par(tf, [("Questions?", True)], size=44, first=True, align=PP_ALIGN.CENTER, color=BLUE, space_after=20)
add_par(tf, "Report, Excel workbook, Power BI dataset, MATLAB scripts and the CAD and thermal files are in the project repository.", size=20, align=PP_ALIGN.CENTER)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
