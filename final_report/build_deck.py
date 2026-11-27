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


def new_slide(title, notes=None, number=[1]):
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
s1.notes_slide.notes_text_frame.text = "Final presentation of the MPG 118S project: the uprate of an existing closed ferrochrome submerged arc furnace from 57.43 MW to 60 MW on its 65 MVA transformers."
for p in tf.paragraphs:
    for r in p.runs:
        r.font.italic = False

# =====================================================================================
# 2. Outline
# =====================================================================================
s = new_slide("Presentation Outline", "Nine parts follow the order of the report.")
left = ["Background and problem", "Existing furnace and design basis", "Mass balance", "Energy and electrical analysis", "Alternatives and selected design"]
right = ["Optimisation of the design", "Economics and sensitivity analysis", "Risk and implementation", "Conclusions and recommendations"]
b, tf = textbox(s, 1.2, 1.7, 5.6, 4.5)
for i, t in enumerate(left):
    add_par(tf, [(f"{i + 1}.  ", True), (t, False)], size=22, first=(i == 0), space_after=16)
b, tf = textbox(s, 7.0, 1.7, 5.6, 4.5)
for i, t in enumerate(right):
    add_par(tf, [(f"{i + 6}.  ", True), (t, False)], size=22, first=(i == 0), space_after=16)

# =====================================================================================
# 3. Background
# =====================================================================================
s = new_slide("Background and Motivation", "Electricity is both the heat source and one of the largest operating costs. The brief is to raise the mean power of the existing furnace to 60 MW without a new transformer.")
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
# 4. Problem
# =====================================================================================
s = new_slide("Problem Statement", "At a fixed transformer rating, production can only rise through power factor, load factor or specific energy.")
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
add_par(tf, [("No electrical measure alone is enough: ", True), ("the specific energy must also fall.", False)], size=18, bullet=True)
b, tf = textbox(s, 6.9, 3.1, 5.8, 3.3)
add_par(tf, [("Constraints", True)], size=20, first=True, space_after=6, color=BLUE)
add_par(tf, "Transformer rating fixed at 65 MVA; power factor at most 0.95.", size=18, bullet=True)
add_par(tf, "Shell, hearth, roof and Søderberg electrodes retained.", size=18, bullet=True)
add_par(tf, "Slag superheat of only about 44 °C above liquidus.", size=18, bullet=True)

# =====================================================================================
# 5. Existing furnace
# =====================================================================================
s = new_slide("Existing Furnace: Power-Limited, Not Capacity-Limited", "All values from the supervisor's plant data workbook. The furnace already loads its transformers to 100 % when on load.")
table(s, [["Parameter", "Value"],
          ["Furnace", "Closed, three-phase submerged arc furnace"],
          ["Transformers", "3 × 21.67 MVA = 65 MVA"],
          ["Mean power (on load)", "57.43 MW (60.45 MW)"],
          ["Power factor, load factor", "0.93, 0.95"],
          ["Production", "393.65 t/d of alloy (50.4 % Cr)"],
          ["Specific energy", "3.5 MWh/t"],
          ["Electrodes", "3 Søderberg, 1.55 m diameter"],
          ["Hearth, shell diameter", "10.88 m, 13.7 m"]],
      0.6, 1.5, 7.6, [3.0, 4.6], size=15, row_h=0.5)
card(s, 8.7, 1.5, 4.0, 1.6, "100 %", "transformer loading while on load")
card(s, 8.7, 3.3, 4.0, 1.6, "65.6 MW", "mean power needed for 450 t/d at 3.5 MWh/t")
card(s, 8.7, 5.1, 4.0, 1.2, "44 °C", "slag superheat margin", vsize=28)

# =====================================================================================
# 6. Design basis
# =====================================================================================
s = new_slide("Design Basis and Acceptance Criteria", "Plant data govern; literature and assumptions are used only where the plant data are silent, and every value carries a provenance tag.")
table(s, [["Criterion", "Requirement"],
          ["Apparent power", "Not above 65 MVA"],
          ["Power factor", "0.93 to 0.95"],
          ["Production", "At least 450 t/d"],
          ["Specific energy", "Not above 3.5 MWh/t"],
          ["Slag superheat", "Positive"],
          ["Auxiliary utilisation", "Not above 90 %"],
          ["Net present value", "Positive"]],
      0.6, 1.5, 6.6, [2.8, 3.8], size=16, row_h=0.52)
b, tf = textbox(s, 7.6, 1.5, 5.1, 4.8)
add_par(tf, [("Hierarchy of data sources", True)], size=20, first=True, space_after=8, color=BLUE)
for i, t in enumerate(["Supervisor-confirmed plant data", "Project brief", "Published literature", "Documented assumptions"]):
    add_par(tf, [(f"{i + 1}.  ", True), (t, False)], size=18, space_after=8)
add_par(tf, "Values calculated in this study are tagged [C], assumptions [A]. 28 assumptions are listed in a register with their confidence and status.", size=16, space_after=0)

# =====================================================================================
# 7. Operating envelope
# =====================================================================================
s = new_slide("Where 60 MW Mean Power Is Possible", "Mean power = S x PF x LF. Every 0.001 of load factor is worth about 0.06 MW.")
picture(s, "F1_operating_envelope.png", 0.5, 1.4, 7.4, 5.0)
bullets(s, [
    [("PF 0.95 and LF of at least 0.972 ", True), ("are needed together.", False)],
    "PF 0.95 is the supervisor's limit, so uptime is the remaining lever.",
    "The transformers have no on-load headroom: 64.98 MVA of 65 MVA.",
    "Three readings of 60 MW were found and separated: mean, continuous and on-load.",
], 8.2, 1.5, 4.6, 4.9, size=18)

# =====================================================================================
# 8. Mass balance method
# =====================================================================================
s = new_slide("Mass Balance: Seven Balances, Five Unknowns", "The plant data have no stream flows, so the balance is a data reconciliation problem solved by weighted non-negative least squares.")
picture(s, "F4_mass_balance.png", 0.5, 1.4, 6.6, 5.0)
bullets(s, [
    "Balances on Al₂O₃, MgO, CaO, SiO₂, Cr, Fe and C per tonne of alloy.",
    "Unknowns: ore, dry reductant, quartz, limestone and slag.",
    [("Solved by weighted non-negative least squares ", True), ("in Python and independently in MATLAB.", False)],
    "Mass closure is -0.41 % and every residual is within 3 %: the plant analyses are consistent.",
], 7.4, 1.5, 5.4, 4.9, size=18)

# =====================================================================================
# 9. Mass balance results
# =====================================================================================
s = new_slide("Mass Balance Results", "Chromium recovery is 86.9 percent, not the 78 percent in the data. The duties of all auxiliary systems rise 15.5 percent at C1.")
picture(s, "F6_chromium_recovery.png", 0.5, 1.5, 6.3, 3.0)
table(s, [["Per tonne of alloy", "Value"],
          ["Ore blend", "2.144 t"],
          ["Dry reductant", "0.433 t"],
          ["Flux", "0.366 t"],
          ["Slag", "1.188 t"],
          ["Off-gas", "597 Nm³"]],
      7.1, 1.5, 5.6, [3.2, 2.4], size=16, row_h=0.45)
card(s, 0.6, 4.75, 3.9, 1.5, "86.9 %", "chromium recovery (78 % assumed)")
card(s, 4.7, 4.75, 3.9, 1.5, "+15.5 %", "daily duties at C1")
card(s, 8.8, 4.75, 3.9, 1.5, "105 %", "auxiliary use with a 10 % margin")

# =====================================================================================
# 10. Energy balance
# =====================================================================================
s = new_slide("Energy Balance and Hot Charging", "From the energy balance chapter. The vendor rule describes heating of the whole charge, so the scope of the hot charging system must be defined by feed heat.")
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
# 11. Electrical scenarios
# =====================================================================================
s = new_slide("Electrical Analysis: No Transformer Headroom", "Eight scenarios on one 65 MVA basis. The verified model reproduces 47 of 52 numbers in the earlier chapters; the other five are explained by the definition of 60 MW and the preheat reference.")
picture(s, "F2_transformer_loading.png", 0.5, 1.4, 7.6, 4.8)
bullets(s, [
    [("S-B, 60 MW mean: ", True), ("64.98 MVA, 100 % of rating.", False)],
    [("S-N60, continuous: ", True), ("64.52 MVA, but needs a load factor of 1.", False)],
    [("S-O60, 60 MW on load: ", True), ("only 57.0 MW mean, 391 t/d, below today.", False)],
    "Python and MATLAB agree on 104 of 104 values.",
], 8.4, 1.5, 4.4, 4.9, size=18)

# =====================================================================================
# 12. Power factor routes
# =====================================================================================
s = new_slide("Raising the Power Factor: Two Routes", "These ratios do not depend on the uncertain Westly constant, so the result is robust.")
picture(s, "F3_pf_route_current_density.png", 0.5, 1.4, 7.4, 4.9)
bullets(s, [
    [("Raise operating resistance: ", True), ("electrode current falls 7.8 % at PF 0.95.", False)],
    [("Lower reactance ", True), ("(the selected conductor rearrangement): current rises 1.1 %.", False)],
    "Estimated current density at C1 is 6.90 A/cm², 1.5 % above today's 6.80, so criterion DC-04 must be revisited.",
    "Electrode current and voltage are estimates until measured.",
], 8.2, 1.5, 4.6, 4.9, size=18)

# =====================================================================================
# 13. Alternatives
# =====================================================================================
s = new_slide("Alternatives: Only Two Combinations Reach 450 t/d", "Values from the alternatives chapter with the preheat measured from 0 C. The verified model gives 454.6 t/d for C1 with the ambient reference.")
table(s, [["Alternative", "Mean power (MW)", "SEC (MWh/t)", "Production (t/d)", "450 t/d"],
          ["E0 existing", "57.43", "3.50", "393.8", "No"],
          ["E1 PF 0.95", "58.66", "3.50", "402.3", "No"],
          ["E2 PF 0.95, LF 0.972", "60.00", "3.50", "411.4", "No"],
          ["P1 hot charging", "57.43", "3.15", "437.5", "No"],
          ["P2 pre-reduced pellets", "57.43", "2.41", "571.9", "Yes"],
          ["C1 E2 + P1", "60.00", "3.15", "457.1", "Yes"],
          ["C2 E2 + P2", "60.00", "2.41", "597.5", "Yes"]],
      0.6, 1.5, 8.2, [3.2, 1.8, 1.6, 1.8, 1.0], size=15, row_h=0.5)
bullets(s, [
    [("C1 ranked first ", True), ("under every weighting tested.", False)],
    "P2 and C2 would exceed the gas, tapping and slag systems.",
    "Pre-reduction is kept as a longer-term route.",
], 9.1, 1.5, 3.7, 4.9, size=17)

# =====================================================================================
# 14. Selected design
# =====================================================================================
s = new_slide("Selected Design C1 and Investment", "Capital figures are early-stage estimates with an accuracy of minus 40 to plus 40 percent.")
bullets(s, [
    [("Power factor 0.93 to 0.95 ", True), ("by rearranging the conductor bars.", False)],
    [("Load factor 95 % to 97.2 % ", True), ("by electrode care and instrumentation.", False)],
    [("Pellets hot-charged at about 500 °C ", True), ("to cut energy per tonne.", False)],
    "Transformers, furnace shell and Søderberg electrodes retained.",
], 0.6, 1.5, 6.0, 4.9, size=19)
table(s, [["Item", "R million"],
          ["Conductor rearrangement", "45"],
          ["Transformer monitoring", "25"],
          ["Controls and metering", "10"],
          ["Auxiliary upgrades", "30"],
          ["Hot-charging allowance", "200"],
          ["Contingency (20 %)", "62"],
          ["Shutdown production loss", "30"],
          ["Total investment", "402"]],
      7.0, 1.5, 5.7, [3.8, 1.9], size=15, row_h=0.5, bold_last=True)

# =====================================================================================
# 15. Optimisation steps
# =====================================================================================
s = new_slide("How the Optimisation Was Achieved", "Step one finds the least intervention, step two tests it against uncertainty, step three designs it to hold.")
b, tf = textbox(s, 0.6, 1.4, 12.1, 0.9)
add_par(tf, [("Minimise the preheat temperature T  subject to  production at least 450 t/d,  PF at most 0.95,  S on load at most 65 MVA", True)], size=18, first=True, align=PP_ALIGN.CENTER)
labels = [("1  Deterministic", "SLSQP, checked by the closed form and in MATLAB", "T* = 452 °C"),
          ("2  Monte Carlo", "100 000 samples of the uncertain inputs", "Meets 450 t/d in about 10 % of cases"),
          ("3  Robust", "Chance-constrained design temperature", "About 610 °C once the saving is verified")]
for i, (h, d, r) in enumerate(labels):
    x = 0.6 + i * 4.2
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.5), Inches(3.7), Inches(3.0))
    sh.adjustments[0] = 0.06
    sh.fill.solid(); sh.fill.fore_color.rgb = LIGHT; sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.2); tf.margin_top = Inches(0.2)
    add_par(tf, [(h, True)], size=22, first=True, space_after=10, color=BLUE)
    add_par(tf, d, size=17, space_after=14)
    add_par(tf, [(r, True)], size=19, space_after=0)
    if i < 2:
        arrow(s, x + 3.72, 3.7, 0.46, 0.5)
b, tf = textbox(s, 0.6, 5.75, 12.1, 0.7)
add_par(tf, "Closed form: T* = T_ref + 100 (SEC0 - 24 S PF LF / 450) / s, with s = 0.07 MWh/t per 100 K from ambient 25 °C.", size=16, first=True, align=PP_ALIGN.CENTER, color=GREY)

# =====================================================================================
# 16. Optimum and Monte Carlo
# =====================================================================================
s = new_slide("Optimum 452 °C, but Only a 10 % Chance of 450 t/d", "Each extra 0.01 of load factor saves about 48 degrees of preheat, so uptime and preheat are interchangeable levers. The Monte Carlo result is driven by the unverified hot-charging saving.")
picture(s, "F7_optimisation_map.png", 0.4, 1.4, 6.2, 4.3)
picture(s, "F8_montecarlo.png", 6.7, 1.4, 6.2, 4.3)
caption(s, "Minimum preheat for 450 t/d", 0.4, 5.75, 6.2)
caption(s, "100 000 Monte Carlo samples of C1 production", 6.7, 5.75, 6.2)
b, tf = textbox(s, 0.6, 6.05, 12.1, 0.5)
add_par(tf, [("Design temperature of 500 °C leaves a 48 °C margin; median production is 438 t/d.", True)], size=17, first=True, align=PP_ALIGN.CENTER)

# =====================================================================================
# 17. Robust optimisation
# =====================================================================================
s = new_slide("Robust Design: Verify the Saving First", "Without a plant trial no practical temperature is robust. A trial that confirms the vendor saving makes C1 robust at about 610 C.")
picture(s, "F11_robust_optimisation.png", 0.4, 1.4, 7.0, 4.9)
table(s, [["Hot-charging saving", "T for 50 %", "T for 90 %"],
          ["Unverified", "670 °C", "925 °C"],
          ["Verified, full vendor value", "520 °C", "610 °C"],
          ["Verified, 75 % of vendor", "670 °C", "780 °C"]],
      7.6, 1.5, 5.2, [2.6, 1.3, 1.3], size=14, row_h=0.55)
bullets(s, [
    [("Plant trial before capital release ", True), ("is the cheapest risk reduction.", False)],
    "Design the preheater for about 610 °C.",
], 7.6, 4.0, 5.2, 2.4, size=18)

# =====================================================================================
# 18. Economics
# =====================================================================================
s = new_slide("Economic Evaluation", "Chapter 15 figures. The verified model gives an NPV of R1 479 M and an IRR of 68.7 percent with the conservative production of 454.8 t/d.")
card(s, 0.6, 1.5, 3.9, 1.5, "R402 M", "total investment")
card(s, 4.7, 1.5, 3.9, 1.5, "R383 M/yr", "incremental profit before tax")
card(s, 8.8, 1.5, 3.9, 1.5, "R1 540 M", "net present value, 15 years at 12 %")
table(s, [["Indicator", "Value"],
          ["Extra production", "63.3 t/d, 23 105 t/yr"],
          ["Incremental revenue", "R604 M/yr"],
          ["Incremental operating cost", "R220.7 M/yr"],
          ["Internal rate of return", "about 70 %"],
          ["Payback after tax", "about 1.4 years"]],
      0.6, 3.3, 7.6, [3.8, 3.8], size=16, row_h=0.5)
bullets(s, ["Alloy price US$1 500/t, R17.42 per US$, electricity R1.65/kWh.", "Verified model: R1 479 M, IRR 68.7 %."], 8.6, 3.3, 4.2, 3.0, size=17)

# =====================================================================================
# 19. NPV tornado
# =====================================================================================
s = new_slide("Sensitivity: What Moves the NPV", "The NPV stays positive in every case. It reaches zero only at an alloy price of US$734 per tonne or a capital cost above R1 620 M.")
picture(s, "F12_npv_tornado.png", 0.4, 1.4, 8.4, 4.9)
bullets(s, [
    [("Alloy price ", True), ("has the largest swing, R1 159 M.", False)],
    [("Hot-charging saving: ", True), ("R761 M, and 450 t/d fails if halved.", False)],
    "Capital cost and electricity tariff matter little.",
    "NPV is zero only at US$734/t.",
], 9.0, 1.5, 3.8, 4.9, size=17)

# =====================================================================================
# 20. Technical sensitivity
# =====================================================================================
s = new_slide("Sensitivity: Electrical and Auxiliary Systems", "Left: at 60 MW mean power the transformers reach 65 MVA exactly at PF 0.95. Right: every duty rises 15.5 percent at C1, so auxiliaries need about 28 percent spare capacity.")
picture(s, "F14_electrical_sensitivity.png", 0.3, 1.4, 6.4, 3.6)
picture(s, "F15_auxiliary_sensitivity.png", 6.65, 1.4, 6.4, 3.6)
caption(s, "Electrical: loading against power factor and mean power against load factor", 0.3, 5.0, 6.4, size=12)
caption(s, "Auxiliary: utilisation and duties against production", 6.65, 5.0, 6.4, size=12)
bullets(s, [
    [("Electrical: ", True), ("no headroom below PF 0.95; PF 0.93 gives only 445 t/d.", False)],
    [("Auxiliary: ", True), ("105 % utilisation at a 10 % design margin, so upgrades are required.", False)],
], 0.6, 5.45, 12.1, 1.1, size=17, space_after=4)

# =====================================================================================
# 21. Risk and implementation
# =====================================================================================
s = new_slide("Risk and Implementation", "Initial scores from the risk register; residual ratings assume the mitigations are implemented. The plan has four gates and three power stages.")
table(s, [["Risk", "Initial score", "Residual rating"],
          ["R-05 Transformer overload", "16", "Low"],
          ["R-08 Auxiliary-system limits", "16", "Moderate"],
          ["R-01 Water ingress", "15", "Moderate"],
          ["R-02 Roof or gas blowout", "15", "High"],
          ["R-04 Hearth or tap-hole failure", "15", "High"]],
      0.6, 1.5, 6.6, [3.6, 1.4, 1.6], size=15, row_h=0.55)
b, tf = textbox(s, 7.6, 1.5, 5.1, 4.9)
add_par(tf, [("Implementation plan", True)], size=20, first=True, space_after=8, color=BLUE)
add_par(tf, "26 months with four decision gates.", size=18, bullet=True)
add_par(tf, "Tie-in during the annual shutdown, with 3 days of float.", size=18, bullet=True)
add_par(tf, "Three power stages (55, 57.5, 60 MW) with numeric acceptance criteria.", size=18, bullet=True)
add_par(tf, "Hot-charging option chosen at Gate G1 on the feed heat it delivers.", size=18, bullet=True)

# =====================================================================================
# 22. Conclusions
# =====================================================================================
s = new_slide("Conclusions and Recommendations", "Close on the decision: proceed to detailed engineering, subject to the plant trial and the measurement gates.")
b, tf = textbox(s, 0.6, 1.4, 6.0, 4.4)
add_par(tf, [("Conclusions", True)], size=22, first=True, space_after=8, color=BLUE)
for t in ["C1 (60 MW mean plus hot charging) is the selected design: about 455 t/d.",
          "Cr recovery is 86.9 %; flux is 0.366 t/t.",
          "NPV about R1 540 M; positive in every case.",
          "The 450 t/d target, not the economics, is the binding requirement."]:
    add_par(tf, t, size=18, bullet=True, space_after=6)
b, tf = textbox(s, 6.9, 1.4, 5.9, 4.4)
add_par(tf, [("Before capital release", True)], size=22, first=True, space_after=8, color=BLUE)
for t in ["Plant trial to measure the hot-charging saving.",
          "Meter the power factor and load factor.",
          "Survey auxiliary-system capacities.",
          "Replace estimated electrode values with measurements.",
          "Design the preheater for about 610 °C."]:
    add_par(tf, t, size=18, bullet=True, space_after=6)
b, tf = textbox(s, 0.6, 5.85, 12.1, 0.6)
add_par(tf, [("Thank you. Questions?", True)], size=26, first=True, align=PP_ALIGN.CENTER, color=BLUE)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
