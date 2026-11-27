"""
build_excel.py – formula-driven engineering workbook: deliverables/SAF_Engineering_Model.xlsx
All results are live Excel formulas; inputs (blue) are taken from the supervisor workbook via the
Python data layer and carry a provenance column. Stochastic results (Monte-Carlo) cannot be
reproduced by formulas and are imported as labelled static values.
"""
import csv
import os
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, massbalance as mb   # noqa: E402

ROOT = data_io.ROOT
DEST = os.path.join(ROOT, "deliverables"); os.makedirs(DEST, exist_ok=True)
F = "Arial"
BLUE, BLACK, GREEN = Font(name=F, color="0000FF", size=10), Font(name=F, size=10), Font(name=F, color="008000", size=10)
BOLD, HDR, TITLE = Font(name=F, bold=True, size=10), Font(name=F, bold=True, color="FFFFFF", size=10), Font(name=F, bold=True, size=14)
HFILL, KEY = PatternFill("solid", fgColor="1F4E78"), PatternFill("solid", fgColor="FFFF00")
SUB = PatternFill("solid", fgColor="D9E2F3")
thin = Side(style="thin", color="A6A6A6"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

inp = data_io.load_inputs()
res, eqs, (A, b, names, x) = mb.full_balance(inp)
wb = Workbook()


def hdr(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t); c.font = HDR; c.fill = HFILL; c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="center")


def put(ws, ref, value, font=BLACK, fmt=None, comment=None, fill=None):
    c = ws[ref]; c.value = value; c.font = font; c.border = BOX
    if fmt: c.number_format = fmt
    if comment: c.comment = Comment(comment, "SAF model")
    if fill: c.fill = fill
    return c


def widths(ws, w):
    for i, v in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = v


# ======================================================================= README
ws = wb.active; ws.title = "README"
lines = [
    ("SAF Engineering Model – ferrochrome furnace 55→60 MW uprate (mass balance, electrical, optimisation)", TITLE),
    ("Source data: supervisor's Ferrochrome Data Workbook (read by the Python model, never retyped). Python model: safmodel v0.2; cross-validated in MATLAB/Octave.", BLACK),
    ("", BLACK),
    ("Colour legend", BOLD),
    ("Blue text = input value (edit to test a case). Black = formula. Green = link to another sheet. Yellow fill = key result / design lever.", BLACK),
    ("Provenance column: MEASURED, SUPPLIED, CALIBRATED, DERIVED_WB, TARGET, ASSUMED, LITERATURE, CALCULATED, PROPOSED.", BLACK),
    ("", BLACK),
    ("Sheets", BOLD),
    ("Inputs – compositions, recipe, electrical and process inputs with provenance; blends are formulas.", BLACK),
    ("MassBalance – reconciled stream masses (solver result) and every element/oxide balance, Cr recovery, off-gas and closure as formulas.", BLACK),
    ("Electrical – eight scenarios incl. three meanings of '60 MW'; on-load loading, currents, voltage, current density, production.", BLACK),
    ("Optimisation – closed-form minimum hot-charge temperature for 450 t/d; robust (Monte-Carlo) results imported from Python.", BLACK),
    ("Verification – 52 team numbers recalculated; Python vs MATLAB/Octave cross-validation.", BLACK),
    ("", BLACK),
    ("How to use", BOLD),
    ("1. Change a blue input (e.g. Electrical!C6 power factor, Optimisation!C5 load factor) – results update.", BLACK),
    ("2. The stream masses in MassBalance!C6:C10 are the solution of a weighted least-squares problem solved in Python/Octave. If you edit", BLACK),
    ("   compositions, re-run model/run_increment2.py to re-solve; the residual columns show immediately how well any set of masses closes the balances.", BLACK),
    ("3. Estimates (electrode current, voltage, current density) rest on the Westly relation with one literature calibration (AF-08).", BLACK),
]
for i, (t, f) in enumerate(lines, 1):
    ws.cell(row=i, column=1, value=t).font = f
ws.column_dimensions["A"].width = 150

# ======================================================================= Inputs
ws = wb.create_sheet("Inputs"); widths(ws, [34, 12, 12, 12, 12, 12, 14, 40])
ws["A1"] = "Inputs (from supervisor data workbook unless stated)"; ws["A1"].font = TITLE
R = {}   # name -> cell address

# --- process & electrical scalars
hdr(ws, 3, ["Parameter", "Value", "Unit", "Provenance", "", "", "", "Source"])
scal = [
    ("S_rated", "Transformer rating", "wb.transformer_capacity", "MVA"), ("PF0", "Power factor (existing)", "wb.power_factor", "-"),
    ("LF0", "Load factor (existing)", "wb.load_factor", "-"), ("SEC0", "Specific energy, cold sintered pellets", "wb.specific_energy_baseline", "MWh/t"),
    ("PROD0", "Production, actual", "wb.ferrochrome_production_baseline", "t/d"), ("TARGET", "Production target", "wb.ferrochrome_production_target", "t/d"),
    ("C3", "Westly C3 (electrode current)", "lit.westly_C3", "kA/MW^(2/3)"), ("D", "Electrode diameter", "lit.electrode_diameter_m", "m"),
    ("VHV", "HV supply voltage", "asm.hv_supply_kV", "kV"), ("PFLIM", "Power-factor upper limit", "asm.pf_upper_limit", "-"),
    ("SAVE", "Hot-charge SEC saving per 100 °C", "asm.hot_charge_sec_saving_per_100C", "MWh/t"),
    ("THOT", "Hot-charge temperature (C1)", "asm.hot_charge_temperature_C", "°C"),
    ("PFC1", "Power factor (C1, proposed)", "prop.pf_c1", "-"), ("LFC1", "Load factor (C1, proposed)", "prop.lf_c1", "-"),
]
r = 4
for key, lab, src, unit in scal:
    q = inp[src]
    ws.cell(row=r, column=1, value=lab).font = BLACK
    put(ws, f"B{r}", q.value, BLUE); ws.cell(row=r, column=3, value=unit).font = BLACK
    ws.cell(row=r, column=4, value=q.tag).font = BLACK; ws.cell(row=r, column=8, value=f"{q.source} {q.note}"[:120]).font = BLACK
    R[key] = f"Inputs!$B${r}"; r += 1
ws.cell(row=r, column=1, value="Ambient reference temperature for preheat").font = BLACK
put(ws, f"B{r}", 25, BLUE, comment="AF-14: preheat increase measured from ambient (conservative). Set 0 to reproduce the original 3.15 MWh/t screening value.")
ws.cell(row=r, column=3, value="°C"); ws.cell(row=r, column=4, value="ASSUMED"); ws.cell(row=r, column=8, value="Audit finding AF-14")
R["TREF"] = f"Inputs!$B${r}"; r += 2

# --- atomic masses
ws.cell(row=r, column=1, value="Atomic masses (g/mol)").font = BOLD; r += 1
for el in ("Cr", "Fe", "Si", "C", "O"):
    ws.cell(row=r, column=1, value=el); put(ws, f"B{r}", mb.M[el], BLUE); ws.cell(row=r, column=4, value="LITERATURE")
    ws.cell(row=r, column=8, value="IUPAC standard atomic weights"); R["M" + el] = f"Inputs!$B${r}"; r += 1
r += 1

# --- ore table
ws.cell(row=r, column=1, value="Ore (mass %)  – blend = recipe-weighted").font = BOLD; r += 1
hdr(ws, r, ["Component", "Pellets", "Lumpy ore", "Blend", "", "", "", "Source"]); r += 1
ws.cell(row=r, column=1, value="Recipe fraction"); put(ws, f"B{r}", inp["recipe.ore.pellets"].value, BLUE, "0.00")
put(ws, f"C{r}", inp["recipe.ore.small_lumpy_ore"].value, BLUE, "0.00"); ws.cell(row=r, column=8, value="Workbook!Recipe (SUPPLIED)")
rf = r; r += 1
for comp in ("Cr2O3", "FeO", "Al2O3", "MgO", "SiO2", "CaO"):
    ws.cell(row=r, column=1, value=comp)
    put(ws, f"B{r}", inp[f"ore.pellets.{comp} (%)"].value, BLUE); put(ws, f"C{r}", inp[f"ore.small_lumpy_ore.{comp} (%)"].value, BLUE)
    put(ws, f"D{r}", f"=($B${rf}*B{r}+$C${rf}*C{r})/100", BLACK, "0.0000")
    ws.cell(row=r, column=8, value="Workbook!Ore mean (MEASURED); blend as fraction")
    R["ORE_" + comp] = f"Inputs!$D${r}"; r += 1
r += 1

# --- reductants
ws.cell(row=r, column=1, value="Reductants (mass %, dry basis assumed A-26) – blend = recipe-weighted").font = BOLD; r += 1
hdr(ws, r, ["Component", "Coke", "Anthracite 1", "Anthracite 2", "Blend (fraction)", "", "", "Source"]); r += 1
ws.cell(row=r, column=1, value="Recipe fraction")
for col, m in zip("BCD", ("coke", "anthracite_1", "anthracite_2")):
    put(ws, f"{col}{r}", inp[f"recipe.reductant.{m}"].value, BLUE, "0.00")
rr = r; r += 1
red_map = [("FC", "Fixed carbon, DFC (%)"), ("Ash", "Ash (%)"), ("VM", "Volatile matter (%)"), ("Moist", "Total moisture (%)"),
           ("Al2O3", "Al2O3 (%)"), ("CaO", "CaO (%)"), ("Fe2O3", "Fe2O3 (%)"), ("MgO", "MgO (%)"), ("SiO2", "SiO2 (%)")]
for key, h in red_map:
    ws.cell(row=r, column=1, value=h)
    for col, m in zip("BCD", ("coke", "anthracite_1", "anthracite_2")):
        put(ws, f"{col}{r}", inp[f"reductants.{m}.{h}"].value, BLUE)
    put(ws, f"E{r}", f"=SUMPRODUCT($B${rr}:$D${rr},B{r}:D{r})/100", BLACK, "0.0000")
    ws.cell(row=r, column=8, value="Workbook!Reductants mean (MEASURED)")
    R["RED_" + key] = f"Inputs!$E${r}"; r += 1
r += 1

# --- fluxes
ws.cell(row=r, column=1, value="Fluxes (mass %)").font = BOLD; r += 1
hdr(ws, r, ["Component", "Quartz", "Limestone", "Quartz (fraction)", "Limestone (fraction)", "", "", "Source"]); r += 1
for comp in ("Al2O3", "CaO", "Fe2O3", "MgO", "SiO2", "Total oxide"):
    ws.cell(row=r, column=1, value=comp)
    qv = inp.get(f"fluxes.quartz.{comp} (%)"); lv = inp[f"fluxes.limestone.{comp} (%)"]
    put(ws, f"B{r}", qv.value if qv else None, BLUE); put(ws, f"C{r}", lv.value, BLUE)
    put(ws, f"D{r}", f"=B{r}/100" if qv else None, BLACK, "0.0000"); put(ws, f"E{r}", f"=C{r}/100", BLACK, "0.0000")
    ws.cell(row=r, column=8, value="Workbook!Fluxes mean (MEASURED)")
    R["Q_" + comp] = f"Inputs!$D${r}"; R["L_" + comp] = f"Inputs!$E${r}"; r += 1
ws.cell(row=r, column=1, value="Limestone CO2 (loss on calcination)")
put(ws, f"E{r}", f"=1-{R['L_Total oxide']}", BLACK, "0.0000"); ws.cell(row=r, column=8, value="CALCULATED: 1 - total oxide")
R["L_CO2"] = f"Inputs!$E${r}"; r += 2

# --- alloy & slag
ws.cell(row=r, column=1, value="Alloy and slag (mass %, mean of 5 samples)").font = BOLD; r += 1
hdr(ws, r, ["Component", "Alloy", "Slag", "Alloy (fraction)", "Slag (fraction)", "", "", "Source"]); r += 1
for comp, a_k, s_k in (("Cr", "Cr (%)", None), ("Fe", "Fe (%)", None), ("Si", "Si (%)", None), ("C", "C (%)", "C (%)"),
                       ("Cr2O3", None, "Cr2O3 (%)"), ("FeO", None, "FeO (%)"), ("Al2O3", None, "Al2O3 (%)"),
                       ("MgO", None, "MgO (%)"), ("CaO", None, "CaO (%)"), ("SiO2", None, "SiO2 (%)")):
    ws.cell(row=r, column=1, value=comp)
    if a_k: put(ws, f"B{r}", inp[f"metal.metal.{a_k}"].value, BLUE); put(ws, f"D{r}", f"=B{r}/100", BLACK, "0.0000"); R["ALLOY_" + comp] = f"Inputs!$D${r}"
    if s_k: put(ws, f"C{r}", inp[f"slag.slag.{s_k}"].value, BLUE); put(ws, f"E{r}", f"=C{r}/100", BLACK, "0.0000"); R["SLAG_" + comp] = f"Inputs!$E${r}"
    ws.cell(row=r, column=8, value="Workbook!Metal / Slag mean (MEASURED)"); r += 1

# ======================================================================= MassBalance
ws = wb.create_sheet("MassBalance"); widths(ws, [40, 14, 14, 14, 14, 14, 14, 14, 14, 14, 30])
ws["A1"] = "Mass balance per tonne of alloy – reconciled (weighted least squares)"; ws["A1"].font = TITLE
ws["A2"] = "Stream masses below are the solver result (Python lsq_linear = Octave lsqnonneg to 1e-15). Balances, recovery, gas and closure are formulas."
hdr(ws, 4, ["Stream", "Symbol", "kg / t alloy", "Provenance"])
streams = [("Ore blend", "m_o", x[0]), ("Reductant blend (dry)", "m_r", x[1]), ("Quartz", "m_q", x[2]),
           ("Limestone", "m_l", x[3]), ("Slag", "m_s", x[4])]
for i, (n, sym, v) in enumerate(streams):
    rr_ = 6 + i
    ws.cell(row=rr_, column=1, value=n); ws.cell(row=rr_, column=2, value=sym)
    put(ws, f"C{rr_}", round(float(v), 4), BLUE, "#,##0.0", comment="Solution of the weighted NNLS reconciliation (model/run_increment2.py).")
    ws.cell(row=rr_, column=4, value="CALCULATED (solver)")
    R[sym] = f"MassBalance!$C${rr_}"
ws.cell(row=11, column=1, value="Alloy"); ws.cell(row=11, column=2, value="—"); put(ws, "C11", 1000, BLUE, "#,##0.0")
# factors
ws["A13"] = "Stoichiometric factors"; ws["A13"].font = BOLD
fac = [("fCr", "Cr in Cr2O3", f"=2*{R['MCr']}/(2*{R['MCr']}+3*{R['MO']})"),
       ("fFeO", "Fe in FeO", f"={R['MFe']}/({R['MFe']}+{R['MO']})"),
       ("fFe2", "Fe in Fe2O3", f"=2*{R['MFe']}/(2*{R['MFe']}+3*{R['MO']})"),
       ("fSi", "Si in SiO2", f"={R['MSi']}/({R['MSi']}+2*{R['MO']})")]
for i, (k, lab, f) in enumerate(fac):
    rr_ = 14 + i; ws.cell(row=rr_, column=1, value=lab); put(ws, f"C{rr_}", f, BLACK, "0.00000"); R[k] = f"MassBalance!$C${rr_}"
ws["A18"] = "Oxygen removed by reduction (kg/t)"
put(ws, "C18", f"=1000*{R['ALLOY_Cr']}*3*{R['MO']}/(2*{R['MCr']})+1000*{R['ALLOY_Fe']}*{R['MO']}/{R['MFe']}+1000*{R['ALLOY_Si']}*2*{R['MO']}/{R['MSi']}", BLACK, "#,##0.0")
R["OREM"] = "MassBalance!$C$18"

# balance table
hdr(ws, 20, ["Balance (kg/t)", "Ore", "Reductant", "Quartz", "Limestone", "Total feed", "Slag", "Alloy / reduction", "Total products",
             "Residual (feed − products)", "Residual % of feed"])
mo, mr, mq, ml, ms = R["m_o"], R["m_r"], R["m_q"], R["m_l"], R["m_s"]
rows = [
    ("Al2O3", f"={mo}*{R['ORE_Al2O3']}", f"={mr}*{R['RED_Al2O3']}", f"={mq}*{R['Q_Al2O3']}", f"={ml}*{R['L_Al2O3']}", f"={ms}*{R['SLAG_Al2O3']}", "=0"),
    ("MgO", f"={mo}*{R['ORE_MgO']}", f"={mr}*{R['RED_MgO']}", f"={mq}*{R['Q_MgO']}", f"={ml}*{R['L_MgO']}", f"={ms}*{R['SLAG_MgO']}", "=0"),
    ("CaO", f"={mo}*{R['ORE_CaO']}", f"={mr}*{R['RED_CaO']}", f"={mq}*{R['Q_CaO']}", f"={ml}*{R['L_CaO']}", f"={ms}*{R['SLAG_CaO']}", "=0"),
    ("SiO2", f"={mo}*{R['ORE_SiO2']}", f"={mr}*{R['RED_SiO2']}", f"={mq}*{R['Q_SiO2']}", f"={ml}*{R['L_SiO2']}", f"={ms}*{R['SLAG_SiO2']}",
     f"=1000*{R['ALLOY_Si']}/{R['fSi']}"),
    ("Cr", f"={mo}*{R['ORE_Cr2O3']}*{R['fCr']}", "=0", "=0", "=0", f"={ms}*{R['SLAG_Cr2O3']}*{R['fCr']}", f"=1000*{R['ALLOY_Cr']}"),
    ("Fe", f"={mo}*{R['ORE_FeO']}*{R['fFeO']}", f"={mr}*{R['RED_Fe2O3']}*{R['fFe2']}", f"={mq}*{R['Q_Fe2O3']}*{R['fFe2']}",
     f"={ml}*{R['L_Fe2O3']}*{R['fFe2']}", f"={ms}*{R['SLAG_FeO']}*{R['fFeO']}", f"=1000*{R['ALLOY_Fe']}"),
    ("C", "=0", f"={mr}*{R['RED_FC']}", "=0", "=0", f"={ms}*{R['SLAG_C']}", f"=1000*{R['ALLOY_C']}+{R['OREM']}*{R['MC']}/{R['MO']}"),
]
for i, (n, o_, r_, q_, l_, s_, a_) in enumerate(rows):
    rr_ = 21 + i
    ws.cell(row=rr_, column=1, value=n).font = BOLD
    for col, v in zip("BCDEGH", (o_, r_, q_, l_, s_, a_)):
        put(ws, f"{col}{rr_}", v, BLACK, "#,##0.0")
    put(ws, f"F{rr_}", f"=SUM(B{rr_}:E{rr_})", BLACK, "#,##0.0")
    put(ws, f"I{rr_}", f"=G{rr_}+H{rr_}", BLACK, "#,##0.0")
    put(ws, f"J{rr_}", f"=F{rr_}-I{rr_}", BLACK, "#,##0.00")
    put(ws, f"K{rr_}", f"=IF(F{rr_}=0,0,J{rr_}/F{rr_})", BLACK, "0.00%", fill=KEY)
ws["A28"] = "SiO2 'Alloy / reduction' = SiO2 reduced to Si; C 'Alloy / reduction' = C in alloy + C leaving as CO (all reduction O as CO)."
ws["A28"].font = Font(name=F, italic=True, size=9)

# KPIs
ws["A30"] = "Key results"; ws["A30"].font = BOLD
hdr(ws, 31, ["Result", "Value", "Unit", "Note"])
kp = [
    ("Cr in feed", f"=F25", "kg/t", ""),
    ("Cr to slag", f"=G25", "kg/t", ""),
    ("Cr recovery to alloy (reconciled)", f"=H25/F25", "%", "workbook assumed 78 %; target 93 %"),
    ("Slag rate", f"={ms}/1000", "t/t", ""),
    ("Ore rate", f"={mo}/1000", "t/t", ""),
    ("Reductant rate (dry)", f"={mr}/1000", "t/t", ""),
    ("Flux rate (quartz + limestone)", f"=({mq}+{ml})/1000", "t/t", ""),
    ("Quartz share of flux (free solver result)", f"={mq}/({mq}+{ml})", "%", "recipe 55 %"),
    ("Reductant moisture", f"={mr}*{R['RED_Moist']}/(1-{R['RED_Moist']})", "kg/t", "as-received moisture on dry reductant"),
    ("CO from reduction", f"={R['OREM']}/{R['MO']}*({R['MC']}+{R['MO']})", "kg/t", ""),
    ("CO2 from limestone", f"={ml}*{R['L_CO2']}", "kg/t", ""),
    ("Volatile matter", f"={mr}*{R['RED_VM']}", "kg/t", ""),
    ("Off-gas volume (CO + CO2 + H2O)", f"=({R['OREM']}/{R['MO']}+B42/({R['MC']}+2*{R['MO']})+B40/(2*1.008+{R['MO']}))*22.414", "Nm3/t", "VM volume excluded"),
    ("Mass in", f"={mo}+{mr}+B40+{mq}+{ml}", "kg/t", ""),
    ("Mass out", f"=C11+{ms}+B41+B42+B40+B43", "kg/t", ""),
    ("Mass closure (out − in)/in", "=(B46-B45)/B45", "%", ""),
]
for i, (lab, f, u, note) in enumerate(kp):
    rr_ = 32 + i
    ws.cell(row=rr_, column=1, value=lab)
    fmt = "0.00%" if u == "%" else ("#,##0.000" if u == "t/t" else "#,##0.0")
    put(ws, f"B{rr_}", f, BLACK, fmt, fill=KEY if i in (2, 15) else None)
    ws.cell(row=rr_, column=3, value="" if u == "%" else u); ws.cell(row=rr_, column=4, value=note)
R["GAS"] = "MassBalance!$B$44"; R["REC"] = "MassBalance!$B$34"

# daily
ws["A49"] = "Daily duties"; ws["A49"].font = BOLD
hdr(ws, 50, ["Stream", "Existing (t/d)", "C1 (t/d)", "Increase"])
ws["A51"] = "Alloy production"; put(ws, "B51", f"={R['PROD0']}", GREEN, "#,##0.0"); put(ws, "C51", "=Electrical!N13", GREEN, "#,##0.0")
for i, (lab, ref) in enumerate((("Ore", mo), ("Reductant (dry)", mr), ("Flux", f"({mq}+{ml})"), ("Slag", ms))):
    rr_ = 52 + i
    ws.cell(row=rr_, column=1, value=lab)
    put(ws, f"B{rr_}", f"={ref}*$B$51/1000", BLACK, "#,##0.0"); put(ws, f"C{rr_}", f"={ref}*$C$51/1000", BLACK, "#,##0.0")
    put(ws, f"D{rr_}", f"=C{rr_}/B{rr_}-1", BLACK, "0.0%")
ws["A56"] = "Off-gas (Nm3/h)"; put(ws, "B56", f"={R['GAS']}*B51/24", BLACK, "#,##0"); put(ws, "C56", f"={R['GAS']}*C51/24", BLACK, "#,##0")
put(ws, "D56", "=C56/B56-1", BLACK, "0.0%")

# ======================================================================= Electrical
ws = wb.create_sheet("Electrical"); widths(ws, [10, 34, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 30])
ws["A1"] = "Electrical operating point and production by scenario (formulas)"; ws["A1"].font = TITLE
ws["A2"] = "P_mean blank = furnace at full rating on load (P_mean = S·PF·LF). Estimates (I, V, J) use Westly I = C3·P_on^(2/3) – AF-08."
hdr(ws, 4, ["ID", "Scenario", "PF", "LF", "P_mean (MW)", "P_on (MW)", "S_on (MVA)", "Loading on load", "Q_on (Mvar)",
            "I_e est. (kA)", "V_LL est. (V)", "J est. (A/cm²)", "SEC (MWh/t)", "Production (t/d)", "≥ 450?", "Used by"])
sc = [("A", "Existing (workbook)", f"={R['PF0']}", f"={R['LF0']}", None, f"={R['SEC0']}", "Ch. 4, 7"),
      ("S-N55", "55 MW continuous", f"={R['PF0']}", 1, 55, f"={R['SEC0']}", "Ngesi Ch. 9 (AF-02)"),
      ("E1", "PF raised to 0.95", f"={R['PFC1']}", f"={R['LF0']}", None, f"={R['SEC0']}", "Ch. 12"),
      ("S-B", "60 MW MEAN (recommended)", f"={R['PFC1']}", f"={R['LFC1']}", 60, f"={R['SEC0']}", "Ch. 12, 14, 18"),
      ("S-N60", "60 MW continuous", f"={R['PF0']}", 1, 60, f"={R['SEC0']}", "Ngesi Ch. 9 (AF-01)"),
      ("S-O60", "60 MW on load", f"={R['PF0']}", f"={R['LF0']}", f"=60*{R['LF0']}", f"={R['SEC0']}", "Simphiwe Ch. 16"),
      ("P1", "Hot charging only", f"={R['PF0']}", f"={R['LF0']}", None, f"={R['SEC0']}-{R['SAVE']}*({R['THOT']}-{R['TREF']})/100", "Ch. 12"),
      ("C1", "60 MW mean + hot charging", f"={R['PFC1']}", f"={R['LFC1']}", 60, f"={R['SEC0']}-{R['SAVE']}*({R['THOT']}-{R['TREF']})/100", "Ch. 12, 14, 15, 18")]
for i, (sid, name, pf, lf, pm, sec, used) in enumerate(sc):
    r_ = 6 + i
    ws.cell(row=r_, column=1, value=sid).font = BOLD; ws.cell(row=r_, column=2, value=name)
    put(ws, f"C{r_}", pf, GREEN if isinstance(pf, str) else BLUE, "0.000")
    put(ws, f"D{r_}", lf, GREEN if isinstance(lf, str) else BLUE, "0.000")
    put(ws, f"E{r_}", pm if pm is not None else f"={R['S_rated']}*C{r_}*D{r_}", BLUE if isinstance(pm, (int, float)) else BLACK, "0.00")
    put(ws, f"F{r_}", f"=E{r_}/D{r_}", BLACK, "0.00")
    put(ws, f"G{r_}", f"=F{r_}/C{r_}", BLACK, "0.00")
    put(ws, f"H{r_}", f"=G{r_}/{R['S_rated']}", BLACK, "0.0%", fill=KEY)
    put(ws, f"I{r_}", f"=G{r_}*SQRT(1-C{r_}^2)", BLACK, "0.00")
    put(ws, f"J{r_}", f"={R['C3']}*F{r_}^(2/3)", BLACK, "0.0")
    put(ws, f"K{r_}", f"=G{r_}*1000/(SQRT(3)*J{r_})", BLACK, "0")
    put(ws, f"L{r_}", f"=J{r_}*1000/(PI()/4*({R['D']}*100)^2)", BLACK, "0.00")
    put(ws, f"M{r_}", sec, GREEN, "0.000")
    put(ws, f"N{r_}", f"=24*E{r_}/M{r_}", BLACK, "0.0", fill=KEY)
    put(ws, f"O{r_}", f'=IF(N{r_}>={R["TARGET"]},"YES","no")', BLACK)
    ws.cell(row=r_, column=16, value=used)
ws["A15"] = "Electrode current ratio when PF is raised 0.93 → 0.95 at constant 65 MVA (independent of C3):"; ws["A15"].font = BOLD
ws["A16"] = "Route R (raise R, X fixed): √(sinφ1/sinφ0)"; put(ws, "E16", f"=SQRT(SQRT(1-{R['PFC1']}^2)/SQRT(1-{R['PF0']}^2))", BLACK, "0.0000")
ws["A17"] = "Route X (lower X, R fixed): √(PF1/PF0)"; put(ws, "E17", f"=SQRT({R['PFC1']}/{R['PF0']})", BLACK, "0.0000")

# ======================================================================= Optimisation
ws = wb.create_sheet("Optimisation"); widths(ws, [44, 14, 14, 14, 14, 30])
ws["A1"] = "Optimisation – how the selected design (C1) was set"; ws["A1"].font = TITLE
ws["A2"] = "Problem: minimise hot-charge temperature T subject to production ≥ 450 t/d, S_on ≤ 65 MVA, PF ≤ 0.95, LF ≤ LF_max."
ws["A3"] = "Production rises with PF and LF, so the optimum sits at PF = 0.95 and LF = LF_max; T* follows in closed form (checked with SLSQP and Octave)."
hdr(ws, 4, ["Design lever", "Value", "Unit"])
ws["A5"] = "Power factor (≤ 0.95)"; put(ws, "B5", f"={R['PFC1']}", GREEN, "0.000")
ws["A6"] = "Load factor achieved"; put(ws, "B6", f"={R['LFC1']}", GREEN, "0.000")
ws["A7"] = "Production target"; put(ws, "B7", f"={R['TARGET']}", GREEN, "0")
ws["A8"] = "SEC required = 24·S·PF·LF / target"; put(ws, "B8", f"=24*{R['S_rated']}*B5*B6/B7", BLACK, "0.000"); ws["C8"] = "MWh/t"
ws["A9"] = "Minimum hot-charge temperature T*"; put(ws, "B9", f"={R['TREF']}+100*({R['SEC0']}-B8)/{R['SAVE']}", BLACK, "0", fill=KEY); ws["C9"] = "°C"
ws["A10"] = "Production at the C1 design temperature"; put(ws, "B10", f"=24*{R['S_rated']}*B5*B6/({R['SEC0']}-{R['SAVE']}*({R['THOT']}-{R['TREF']})/100)", BLACK, "0.0"); ws["C10"] = "t/d"
hdr(ws, 12, ["LF_max", "T* (°C), ambient ref", "T* (°C), 0 °C ref"])
for i, lf in enumerate((0.95, 0.96, 0.965, 0.972, 0.975, 0.98)):
    r_ = 13 + i
    put(ws, f"A{r_}", lf, BLUE, "0.000")
    put(ws, f"B{r_}", f"={R['TREF']}+100*({R['SEC0']}-24*{R['S_rated']}*{R['PFLIM']}*A{r_}/{R['TARGET']})/{R['SAVE']}", BLACK, "0")
    put(ws, f"C{r_}", f"=0+100*({R['SEC0']}-24*{R['S_rated']}*{R['PFLIM']}*A{r_}/{R['TARGET']})/{R['SAVE']}", BLACK, "0")
ws["A21"] = "Robustness (imported from Python Monte-Carlo – stochastic, not recalculated in Excel)"; ws["A21"].font = BOLD
hdr(ws, 22, ["Case", "T for P(≥450) = 50 % (°C)", "T for 90 % (°C)", "P(≥450) at 500 °C"])
for i, row in enumerate(csv.reader(open(os.path.join(ROOT, "results", "model", "I2_robust_optimisation.csv")))):
    if i == 0: continue
    for j, v in enumerate(row):
        c = ws.cell(row=22 + i, column=1 + j, value=float(v) if j else v); c.font = BLACK; c.border = BOX
        if j == 3: c.number_format = "0.0%"
mc = {r_[0]: r_[1] for r_ in csv.reader(open(os.path.join(ROOT, "results", "model", "I2_montecarlo_summary.csv")))}
ws["A28"] = "Monte-Carlo C1 (100 000 samples): P(production ≥ 450 t/d)"; put(ws, "B28", float(mc["P(production >= 450 t/d)"]), BLACK, "0.0%")
ws["A29"] = "Monte-Carlo C1 P5 / P50 / P95 (t/d)"; ws["B29"] = f'{mc["P5 t/d"]} / {mc["P50 t/d"]} / {mc["P95 t/d"]}'
ws["A30"] = "Input distributions are assumptions (A-27): saving U(0.035, 0.070); T ±50 °C; LF Tri(0.95, 0.972, 0.98); PF Tri(0.93, 0.95, 0.95); SEC0 N(3.5, 0.035)."
ws["A30"].font = Font(name=F, italic=True, size=9)

# ======================================================================= Verification
ws = wb.create_sheet("Verification"); widths(ws, [8, 16, 44, 12, 12, 10, 10, 13, 60])
ws["A1"] = "Verification of team calculations and Python–MATLAB/Octave cross-validation (imported results)"; ws["A1"].font = TITLE
rows = list(csv.reader(open(os.path.join(ROOT, "results", "model", "I1_verification.csv"))))
hdr(ws, 3, rows[0])
for i, row in enumerate(rows[1:]):
    for j, v in enumerate(row):
        try: v = float(v) if j in (3, 4, 5, 6) else v
        except ValueError: pass
        c = ws.cell(row=4 + i, column=1 + j, value=v); c.font = BLACK; c.border = BOX
        if j == 7 and v != "REPRODUCED": c.fill = PatternFill("solid", fgColor="FCE4D6")
r0 = 6 + len(rows)
ws.cell(row=r0, column=1, value="Cross-validation summary").font = BOLD
for k, fn in enumerate(("I1_crossval.csv", "I2_crossval.csv")):
    cv = list(csv.reader(open(os.path.join(ROOT, "results", "model", fn))))[1:]
    worst = max(float(c[4]) for c in cv); nf = sum(c[5] != "PASS" for c in cv)
    ws.cell(row=r0 + 1 + k, column=1, value=fn.split("_")[0])
    ws.cell(row=r0 + 1 + k, column=3, value=f"{len(cv)} comparisons, {nf} failures, worst relative difference {worst:.1e}")

for s_ in wb.worksheets:
    for row in s_.iter_rows():
        for c in row:
            if c.font and c.font.name != F:
                c.font = Font(name=F, size=c.font.size or 10, bold=c.font.bold, italic=c.font.italic, color=c.font.color)
    s_.freeze_panes = None
out = os.path.join(DEST, "SAF_Engineering_Model.xlsx")
wb.save(out)
print(out)
