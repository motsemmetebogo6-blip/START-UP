"""
01_reference_furnace.py – derives the Reference Furnace Specification (RFS, docs/03)
for the existing 55 MW furnace and runs internal-consistency checks.
Inputs: parameters.py only. Output: results/01_rfs.csv
"""
import csv, math, os
import parameters as p

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = []
def rec(group, name, value, unit, tag, basis, fmt="{:.3f}"):
    rows.append((group, name, round(value, 4) if isinstance(value, float) else value, unit, tag, basis))
    v = fmt.format(value) if isinstance(value, (int, float)) else value
    print(f"  {name:<52} {v:>10} {unit:<8} [{tag}] {basis}")

# ---- Electrical (baseline calibration identical to calc 02) ----------------
print("ELECTRICAL")
C3 = p.ANALOGUE_I_KA / p.ANALOGUE_P_MW ** (2/3)
I = C3 * p.P_BASE_MW ** (2/3)                       # kA
R = p.P_BASE_MW * 1e6 / (3 * (I*1e3)**2)            # ohm
Z = p.S_BASE_MVA * 1e6 / (3 * (I*1e3)**2)
X = math.sqrt(Z**2 - R**2)
VLL = math.sqrt(3) * p.S_BASE_MVA * 1e6 / (3 * I*1e3)
rec("Electrical", "Active power", p.P_BASE_MW, "MW", "S", "S-01")
rec("Electrical", "Phase power P/3", p.P_BASE_MW/3, "MW", "C", "balanced")
rec("Electrical", "Apparent power (= rating)", p.S_BASE_MVA, "MVA", "A", "A-14")
rec("Electrical", "Power factor", R/Z, "-", "C", "R/Z")
rec("Electrical", "Reactive power", math.sqrt(p.S_BASE_MVA**2 - p.P_BASE_MW**2), "Mvar", "C", "sqrt(S2-P2)")
rec("Electrical", "Electrode current", I, "kA", "C", "Westly C3 = %.2f (A-18)" % C3)
rec("Electrical", "Secondary voltage (line)", VLL, "V", "C", "S/(sqrt3 I)", "{:.0f}")
rec("Electrical", "Operating resistance per phase", R*1e3, "mohm", "C", "P/(3I2)")
rec("Electrical", "Total reactance per phase", X*1e3, "mohm", "C", "sqrt(Z2-R2)")
Xsn = p.SHORT_NETWORK_X_SHARE * X; Xt = X - Xsn
rec("Electrical", "Reactance: short network + columns (70 %)", Xsn*1e3, "mohm", "C", "R-14 share")
rec("Electrical", "Reactance: transformer + remainder (30 %)", Xt*1e3, "mohm", "C", "R-14 share")
Zb = VLL**2 / (p.S_BASE_MVA*1e6)
rec("Electrical", "Total reactance, per unit on 65 MVA/312 V", X/Zb, "pu", "C", "X/Zbase")
rec("Electrical", "Transformer share, per unit (implied u_k)", Xt/Zb, "pu", "C", "check vs literature (WP3)")
rec("Electrical", "Transformer units", "3 x 21.67 MVA 1-phase", "-", "A", "docs/02 s6")
Iw = I / math.sqrt(3)
Iw_rating = (p.S_RATED_MVA/3)*1e6 / VLL / 1e3
rec("Electrical", "Secondary winding current (delta at electrodes)", Iw, "kA", "C", "I/sqrt3")
rec("Electrical", "Winding current from unit rating 21.67 MVA / V_LL", Iw_rating, "kA", "C", "consistency check")
for kv, tag in ((p.HV_KV, "A-21"), (p.HV_KV_ALT, "A-21 sens.")):
    rec("Electrical", f"Primary line current at {kv:.0f} kV", p.S_BASE_MVA*1e6/(math.sqrt(3)*kv*1e3), "A", "C", tag, "{:.0f}")
rec("Electrical", "Existing secondary tap range (min)", p.TAP_RANGE_V[0], "V", "A", "A-23", "{:.0f}")
rec("Electrical", "Existing secondary tap range (max)", p.TAP_RANGE_V[1], "V", "A", "A-23", "{:.0f}")

# ---- Geometry ----------------------------------------------------------------
print("GEOMETRY")
D = p.D_ELECTRODE_M; PCD = p.PCD_D_RATIO * D; Dh = p.HEARTH_PCD_RATIO * PCD
cc = PCD * math.sqrt(3) / 2
rec("Geometry", "Electrode diameter D", D, "m", "A", "A-16")
rec("Geometry", "Electrode cross-section", math.pi/4*D**2, "m2", "C", "pi D2/4")
rec("Geometry", "Electrode current density", I*1e3/(math.pi/4*(D*100)**2), "A/cm2", "C", "I/A")
rec("Geometry", "Pitch circle diameter PCD", PCD, "m", "A", "A-19 (PCD/D = %.2f)" % p.PCD_D_RATIO)
rec("Geometry", "Electrode centre-to-centre spacing", cc, "m", "C", "PCD sqrt3/2")
rec("Geometry", "Clear gap between electrodes", cc - D, "m", "C", "spacing - D")
rec("Geometry", "Hearth (inner lining) diameter", Dh, "m", "A", "A-20 (hearth/PCD = %.2f)" % p.HEARTH_PCD_RATIO)
rec("Geometry", "Electrode surface to hearth wall", Dh/2 - PCD/2 - D/2, "m", "C", "radial")
rec("Geometry", "Shell inner diameter", p.SHELL_ID_M, "m", "L", "R-11")
lining = (p.SHELL_ID_M - Dh)/2
rec("Geometry", "Implied sidewall lining thickness", lining, "m", "C", "(shell - hearth)/2 - plausibility check")
Ah = math.pi/4*Dh**2
rec("Geometry", "Hearth area", Ah, "m2", "C", "pi Dh2/4")
rec("Geometry", "Hearth power density at 55 MW", p.P_BASE_MW/Ah, "MW/m2", "C", "P/A")
rec("Geometry", "Hearth power density at 60 MW (same hearth)", p.P_NEW_MW/Ah, "MW/m2", "C", "P/A")
rec("Geometry", "Power per electrode / PCD-circle area at 55 MW", p.P_BASE_MW/(math.pi/4*PCD**2), "MW/m2", "C", "P/A_PCD")

# ---- Process -------------------------------------------------------------------
print("PROCESS")
f = p.FEED_CONC
Cr = f["Cr2O3"] * 2*51.996/151.99; Fe = f["FeO"] * 55.845/71.844
rec("Process", "Feed Cr (from Cr2O3)", Cr, "mass %", "C", "R-18 analysis")
rec("Process", "Feed Fe (from FeO)", Fe, "mass %", "C", "R-18 analysis")
rec("Process", "Feed Cr/Fe ratio (calc vs reported %.2f)" % p.FEED_CR_FE_REPORTED, Cr/Fe, "-", "C", "consistency check")
rec("Process", "Feed analysis closure (5 oxides)", sum(f.values()), "mass %", "C", "remainder = CaO, TiO2, V2O5, LOI etc.")
rec("Process", "Specific electrical energy", p.SEC_MWH_T, "MWh/t", "A", "A-04 mid")
rec("Process", "Utilisation", p.UTILISATION, "-", "A", "A-09 mid")
td = p.P_BASE_MW*24*p.UTILISATION/p.SEC_MWH_T
rec("Process", "Alloy production at 55 MW", td, "t/d", "C", "P 24 u / SEC", "{:.0f}")
rec("Process", "Alloy production at 55 MW (annual)", td*365/1000, "kt/a", "C", "x365", "{:.1f}")
rec("Process", "Alloy production at 60 MW (same SEC, indicative)", p.P_NEW_MW*24*p.UTILISATION/p.SEC_MWH_T, "t/d", "C", "WP7 to confirm", "{:.0f}")
s = p.SLAG_TYPICAL
rec("Process", "Slag basicity (CaO+MgO)/SiO2", (s["CaO"]+s["MgO"])/s["SiO2"], "-", "C", "R-19 typical")
rec("Process", "Slag MgO/Al2O3", s["MgO"]/s["Al2O3"], "-", "C", "R-19 typical")

# ---- Auxiliaries -------------------------------------------------------------
print("AUXILIARIES")
cap = 1 + p.AUX_DESIGN_MARGIN
rec("Auxiliary", "Aux. design capacity (relative to 55 MW duty)", cap, "x", "A", "A-22")
rec("Auxiliary", "Aux. utilisation at 60 MW (if load ~ power)", (p.P_NEW_MW/p.P_BASE_MW)/cap, "fraction", "C", "1.0909 / 1.10")

with open(os.path.join(OUT, "01_rfs.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["Group", "Item", "Value", "Unit", "Tag", "Basis"]); w.writerows(rows)
print(f"\nWrote results/01_rfs.csv ({len(rows)} items)")
