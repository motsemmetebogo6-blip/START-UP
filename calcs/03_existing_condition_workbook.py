"""
03_existing_condition_workbook.py – Chapter 7 (existing condition) and Chapter 12
screening, from the supervisor-confirmed data workbook (data/Ferrochrome_Data_Workbook.xlsx).

Workbook values are read directly (no retyping). Values not in the workbook (electrode
diameter, Westly C3, HV voltage) come from parameters.py and stay tagged as assumptions.
Outputs: results/07_existing_condition.csv, results/12_alternatives_screening.csv
"""
import csv, math, os
import openpyxl
import parameters as p

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
wb = openpyxl.load_workbook(os.path.join(ROOT, "data", "Ferrochrome_Data_Workbook.xlsx"), data_only=True)

def mean_row(sheet, material=None):
    ws = wb[sheet]
    hdr = [c.value for c in ws[4]]
    for row in ws.iter_rows(min_row=5, values_only=True):
        if material is not None and row[0] != material: continue
        label = row[1] if material is not None else row[0]
        if label == "Mean (reported)":
            return {h: v for h, v in zip(hdr, row) if h}
    raise KeyError(sheet, material)

A = {r[0]: r for r in wb["Assumptions"].iter_rows(min_row=5, values_only=True) if r[0]}
def num(x):
    """Workbook stores some numbers as text: convert where possible."""
    try: return float(x)
    except (TypeError, ValueError): return x
val = lambda k: num(A[k][2] if A[k][2] is not None else A[k][1])

out = []
def rec(group, item, value, unit, tag, basis, fmt="{:.3f}"):
    out.append((group, item, round(value, 4) if isinstance(value, float) else value, unit, tag, basis))
    v = fmt.format(value) if isinstance(value, (int, float)) else value
    print(f"  {item:<58} {v:>10} {unit:<10} [{tag}] {basis}")

# ------------------------------------------------------------------ electrical
print("ELECTRICAL (furnace electrical boundary)")
S, PF, LF = val("transformer_capacity"), val("power_factor"), val("load_factor")
phi = math.acos(PF)
P_on = S * PF; Q_on = S * math.sin(phi); P_mean = S * PF * LF
rec("Electrical", "Transformer rating S", S, "MVA", "S/WB", "workbook: fixed constraint")
rec("Electrical", "Power factor", PF, "-", "A/WB", "workbook: accepted by supervisor (<=0.95 acceptable)")
rec("Electrical", "Load factor", LF, "-", "C/WB", "workbook: back-solved, not measured")
rec("Electrical", "On-load active power P = S·PF", P_on, "MW", "C", "65 x 0.93")
rec("Electrical", "On-load reactive power Q = S·sinφ", Q_on, "Mvar", "C", "65 x sin(acos 0.93)")
rec("Electrical", "Mean active power P = S·PF·LF", P_mean, "MW", "C", "workbook 57.43")
rec("Electrical", "Mean phase power P/3", P_mean / 3, "MW", "C", "balanced")
rec("Electrical", "Energy per day", P_mean * 24, "MWh/d", "C", "workbook 1378.3")
rec("Electrical", "Transformer loading on load", 100.0, "%", "C", "S at rating")
rec("Electrical", "R/X = tanφ⁻¹ = PF/sqrt(1-PF²)", PF / math.sin(phi), "-", "C", "")
rec("Electrical", "Implied bath-to-total power if brief '55 MW' is bath power", 55 / P_mean, "-", "C", "reconciliation option A")
# Electrode current: not in workbook -> Westly calibration (A-18) on on-load power
C3 = p.ANALOGUE_I_KA / p.ANALOGUE_P_MW ** (2/3)
I = C3 * P_on ** (2/3)
V = S * 1e6 / (math.sqrt(3) * I * 1e3)
R = P_on * 1e6 / (3 * (I * 1e3) ** 2); X = R * math.tan(phi)
A_cm2 = math.pi / 4 * (p.D_ELECTRODE_M * 100) ** 2
rec("Electrical", "Electrode current (Westly C3 = 8.33, A-18)", I, "kA", "A/C", "no secondary data in workbook")
rec("Electrical", "Secondary voltage (line)", V, "V", "C", "S/(sqrt3 I)", "{:.0f}")
rec("Electrical", "Operating resistance per phase", R * 1e3, "mohm", "C", "P/(3I²)")
rec("Electrical", "Reactance per phase", X * 1e3, "mohm", "C", "R·tanφ")
rec("Electrical", "Electrode current density (D = 1.55 m, A-16)", I * 1e3 / A_cm2, "A/cm2", "C", "I/A")
for kv in (p.HV_KV, p.HV_KV_ALT):
    rec("Electrical", f"Primary line current at {kv:.0f} kV", S * 1e6 / (math.sqrt(3) * kv * 1e3), "A", "C", "A-21", "{:.0f}")

# ------------------------------------------------------------------ production
print("PRODUCTION AND ENERGY")
SEC = val("specific_energy_baseline"); prod_sup = val("ferrochrome_production_baseline")
prod_calc = P_mean * 24 / SEC
rec("Production", "Specific energy (cold sintered pellets)", SEC, "MWh/t", "S/WB", "confirmed by supervisor")
rec("Production", "Production calculated = E/SEC", prod_calc, "t/d", "C", "1378.3/3.5")
rec("Production", "Production supplied (actual)", prod_sup, "t/d", "S/WB", "supervisor 393.5-393.8")
rec("Production", "Difference calc vs supplied", 100 * (prod_calc - prod_sup) / prod_sup, "%", "C", "consistency check")
rec("Production", "Annual production", prod_sup * 365 / 1000, "kt/a", "C", "x365")
rec("Production", "Production target (not achieved)", float(val("ferrochrome_production_target")), "t/d", "S/WB", "bottleneck")
rec("Production", "SEC required for 450 t/d at 57.43 MW", P_mean * 24 / 450, "MWh/t", "C", "workbook 3.06")

# ------------------------------------------------------------------ feed, alloy, slag
print("FEED, ALLOY, SLAG")
recipe = {r[1]: num(r[2]) / 100 for r in wb["Recipe"].iter_rows(min_row=5, values_only=True) if r[0] == "ore"}
pel, lump = mean_row("Ore", "pellets"), mean_row("Ore", "small_lumpy_ore")
blend = {k: recipe["pellets"] * pel[k] + recipe["small_lumpy_ore"] * lump[k]
         for k in ("Cr2O3 (%)", "FeO (%)", "Al2O3 (%)", "MgO (%)", "SiO2 (%)", "CaO (%)")}
CR, FE = 2 * 51.996 / 151.99, 55.845 / 71.844
for k, v in blend.items(): rec("Feed", f"Ore blend {k} (80 % pellets / 20 % lumpy)", v, "%", "C", "recipe-weighted")
crfe_pel = pel["Cr2O3 (%)"] * CR / (pel["FeO (%)"] * FE)
rec("Feed", "Pellet Cr/Fe calculated vs reported 1.40", crfe_pel, "-", "C", "consistency check")
blend_crfe = blend["Cr2O3 (%)"] * CR / (blend["FeO (%)"] * FE)
rec("Feed", "Ore blend Cr/Fe", blend_crfe, "-", "C", "")
met = mean_row("Metal"); slag = mean_row("Slag")
rec("Alloy", "Alloy Cr / Fe / Si / C", f"{met['Cr (%)']} / {met['Fe (%)']} / {met['Si (%)']} / {met['C (%)']}", "%", "M/WB", "mean of 5")
rec("Alloy", "Alloy Cr/Fe", met["Cr (%)"] / met["Fe (%)"], "-", "C", "")
rec("Alloy", "Tap temperature / liquidus / superheat", f"{met['Tap temp, derived (°C)']} / {met['Liquidus (°C)']} / {met['Superheat (°C)']}", "°C", "M/WB", "")
bas = (slag["CaO (%)"] + slag["MgO (%)"]) / slag["SiO2 (%)"]
rec("Slag", "Basicity (CaO+MgO)/SiO2 calculated vs reported 0.95", bas, "-", "C", "consistency check")
rec("Slag", "MgO/Al2O3", slag["MgO (%)"] / slag["Al2O3 (%)"], "-", "C", "")
rec("Slag", "Cr2O3 in slag (measured; replaces supplied 15 %)", slag["Cr2O3 (%)"], "%", "M/WB", "")
rec("Slag", "Liquidus Levin / FactSage; in-furnace temperature", f"{slag['Liquidus, Levin (°C)']} / {slag['Liquidus, FactSage (°C)']} / {slag['In-furnace temp (°C)']}", "°C", "M/WB", "model estimates")

# ------------------------------------------------------------------ Cr recovery check
print("CHROMIUM RECOVERY CHECK (per tonne alloy)")
Cr_alloy = met["Cr (%)"] * 10                     # kg Cr / t alloy
Cr_ore = blend["Cr2O3 (%)"] / 100 * CR            # kg Cr / kg ore
fCr_slag = slag["Cr2O3 (%)"] / 100 * CR           # kg Cr / kg slag
R78 = val("chromium_recovery_baseline") / 100
ore78 = Cr_alloy / (R78 * Cr_ore)
slag78 = (Cr_alloy / R78 - Cr_alloy) / fCr_slag
rec("Recovery", "Workbook recovery 78 % -> ore required", ore78 / 1000, "t/t", "C", "")
rec("Recovery", "Workbook recovery 78 % -> implied slag (all loss to slag)", slag78 / 1000, "t/t", "C", "workbook 'about 2.2'")
res = {}
for tracer, ore_k, slag_k in (("Al2O3", "Al2O3 (%)", "Al2O3 (%)"), ("MgO", "MgO (%)", "MgO (%)")):
    k = blend[ore_k] / slag[slag_k]               # kg slag per kg ore (ore-only tracer)
    m = Cr_alloy / (Cr_ore - k * fCr_slag)        # ore per t alloy from Cr balance
    Rr = Cr_alloy / (m * Cr_ore); res[tracer] = (m, k * m, Rr)
    rec("Recovery", f"{tracer} tracer: ore required", m / 1000, "t/t", "C", "ore-only tracer, no dust loss")
    rec("Recovery", f"{tracer} tracer: slag mass", k * m / 1000, "t/t", "C", "")
    rec("Recovery", f"{tracer} tracer: Cr recovery to alloy", 100 * Rr, "%", "C", "upper bound (ignores dust, ash/flux oxides)")

# ------------------------------------------------------------------ Chapter 12 screening
print("CHAPTER 12 – ALTERNATIVES SCREENING (production at fixed 65 MVA)")
alts = []
def alt(code, name, P_mw, sec, note):
    t = P_mw * 24 / sec
    alts.append((code, name, round(P_mw, 2), round(sec, 3), round(t, 1), round(100 * (t / prod_calc - 1), 1),
                 "yes" if t >= 450 else "no", note))
    print(f"  {code:<4} {name:<52} P={P_mw:6.2f} MW SEC={sec:5.2f} → {t:6.1f} t/d ({100*(t/prod_calc-1):+5.1f} %)  450? {'yes' if t>=450 else 'no'}")
rx = lambda pf: pf / math.sqrt(1 - pf**2)
rec("Screening", "R/X at PF 0.93 (existing)", rx(PF), "-", "C", "")
rec("Screening", "R/X at PF 0.95 (supervisor upper limit)", rx(0.95), "-", "C", "")
rec("Screening", "R/X increase needed 0.93 -> 0.95", 100 * (rx(0.95) / rx(PF) - 1), "%", "C", "electrode geometry / short network")
rec("Screening", "LF needed for 60 MW mean at PF 0.93", 60 / (S * PF), "-", "C", "")
rec("Screening", "LF needed for 60 MW mean at PF 0.95", 60 / (S * 0.95), "-", "C", "")
SEC_hot = SEC - 0.07 * 5   # A-24: hot charging at ~500 C, R-04 sensitivity (screening assumption)
SEC_pre = val("specific_energy_target")
alt("E0", "Existing operation (PF 0.93, LF 0.95)", P_mean, SEC, "baseline")
alt("E1", "Raise PF to 0.95 (R/X +20 %), LF 0.95", S * 0.95 * 0.95, SEC, "electrode geometry and/or short-network reactance")
alt("E2", "E1 + load factor to 0.972 → 60 MW mean", 60.0, SEC, "fewer power interruptions")
alt("P1", "Hot-charged pellets ~500 °C (A-24), power unchanged", P_mean, SEC_hot, "-70 kWh/t per 100 °C (R-04)")
alt("P2", "Pre-reduced hot pellets 40–50 % metallised", P_mean, SEC_pre, "workbook target SEC 2.41")
alt("C1", "E2 + P1 (60 MW and hot charging)", 60.0, SEC_hot, "electrical uprate + preheat")
alt("C2", "E2 + P2 (60 MW and pre-reduction)", 60.0, SEC_pre, "upper bound; other bottlenecks will limit")
rec("Screening", "SEC needed for 450 t/d at 60 MW mean", 60 * 24 / 450, "MWh/t", "C", "")
rec("Screening", "Power needed for 450 t/d at 3.5 MWh/t", 450 * SEC / 24, "MW", "C", "> 60.45 MW on-load max")
rec("Screening", "Max mean power at PF 0.95, LF 0.95", S * 0.95 * 0.95, "MW", "C", "")
rec("Screening", "PF x LF needed for 60 MW mean on 65 MVA", 60 / S, "-", "C", "")

os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
with open(os.path.join(ROOT, "results", "07_existing_condition.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Group", "Item", "Value", "Unit", "Tag", "Basis"]); w.writerows(out)
with open(os.path.join(ROOT, "results", "12_alternatives_screening.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Code", "Alternative", "Mean_power_MW", "SEC_MWh_t", "Production_t_d", "Change_pct", "Meets_450", "Note"]); w.writerows(alts)
print("\nWrote results/07_existing_condition.csv and results/12_alternatives_screening.csv")

# ------------------------------------------------------------------ Chapter 12 chart
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 5))
secs = np.linspace(2.3, 3.7, 100)
for Pm, ls, lab in ((P_mean, "-", f"{P_mean:.2f} MW mean (existing)"), (S*0.95*0.95, "--", "58.66 MW (PF 0.95)"), (60.0, ":", "60.00 MW (PF 0.95, LF 0.972)")):
    ax.plot(secs, Pm * 24 / secs, ls, color="C0", label=lab)
ax.axhline(450, color="C3", lw=1); ax.text(3.55, 453, "target 450 t/d", color="C3", fontsize=8)
for code, name, Pm, sec, t, *_ in alts:
    ax.plot(sec, t, "o", color="C1" if code.startswith("C") else ("C2" if code.startswith("P") else "C0"))
    ax.annotate(code, (sec, t), xytext=(5, 4), textcoords="offset points", fontsize=8)
ax.set_xlabel("Specific electrical energy SEC (MWh/t alloy)"); ax.set_ylabel("Alloy production (t/d)")
ax.set_title("Chapter 12 – production at fixed 65 MVA: power vs specific energy")
ax.invert_xaxis(); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "results", "12_alternatives_chart.png"), dpi=150)
print("Wrote results/12_alternatives_chart.png")
