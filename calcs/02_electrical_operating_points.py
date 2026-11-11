"""
02_electrical_operating_points.py – Phase 2 electrical design.

Model (balanced 3-phase, per-electrode star equivalent):
    P = 3 I^2 R        Q = 3 I^2 X        S = 3 I^2 Z = 3 V_ph I
    Z = sqrt(R^2 + X^2)   PF = R / Z   V_LL = sqrt(3) V_ph
R = furnace (bath + electrode) operating resistance per phase,
X = total circuit reactance per phase referred to the secondary.
Westly:  I = C3 P^(2/3)  (I kA, P MW)  -> used to CALIBRATE baseline current.
Outputs: tables to stdout, results/02_operating_points.csv, results/02_operating_chart.png
"""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import parameters as p

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results"); os.makedirs(OUT, exist_ok=True)

def area_cm2(d_m): return math.pi / 4 * (d_m * 100) ** 2

def point(P_MW, I_kA, X_mohm):
    """Operating point from P, I and X."""
    I = I_kA * 1e3
    R = P_MW * 1e6 / (3 * I**2)                 # ohm
    X = X_mohm * 1e-3
    Z = math.hypot(R, X)
    S = 3 * I**2 * Z / 1e6                      # MVA
    Vph = S * 1e6 / (3 * I)
    return dict(P=P_MW, I=I_kA, R=R*1e3, X=X_mohm, Z=Z*1e3, PF=R/Z, S=S,
                Q=math.sqrt(max(S**2 - P_MW**2, 0)), Vph=Vph, VLL=math.sqrt(3)*Vph,
                J=I / area_cm2(p.D_ELECTRODE_M), C3=I_kA / P_MW**(2/3))

def point_from_RX(P_MW, R_mohm, X_mohm):
    I_kA = math.sqrt(P_MW * 1e6 / (3 * R_mohm * 1e-3)) / 1e3
    return point(P_MW, I_kA, X_mohm)

def show(tag, d):
    print(f"{tag:<34} P={d['P']:5.1f} MW  I={d['I']:6.1f} kA  R={d['R']:.3f} mΩ  "
          f"X={d['X']:.3f} mΩ  PF={d['PF']:.3f}  S={d['S']:5.1f} MVA  "
          f"V_LL={d['VLL']:5.0f} V  J={d['J']:.2f} A/cm²  C3={d['C3']:.2f}")

rows = []
# ---------------------------------------------------------------- 1 Calibration
C3_cal = p.ANALOGUE_I_KA / p.ANALOGUE_P_MW ** (2/3)
print(f"1) Westly C3 calibrated on analogue: C3 = {p.ANALOGUE_I_KA} / {p.ANALOGUE_P_MW}^(2/3) "
      f"= {C3_cal:.2f}  (literature FeCr range {p.C3_FECR_RANGE})")
J_an = p.ANALOGUE_I_KA * 1e3 / area_cm2(p.D_ELECTRODE_M)
print(f"   Analogue current density = {p.ANALOGUE_I_KA*1e3:.0f} A / {area_cm2(p.D_ELECTRODE_M):.0f} cm² "
      f"= {J_an:.2f} A/cm²  (patent guideline {p.J_GUIDE_A_CM2} A/cm²)\n")

# ---------------------------------------------------------------- 2 Baseline
I_base = C3_cal * p.P_BASE_MW ** (2/3)
I = I_base * 1e3
R_b = p.P_BASE_MW * 1e6 / (3 * I**2)
Z_b = p.S_BASE_MVA * 1e6 / (3 * I**2)           # A-14: baseline at full 65 MVA
X_b = math.sqrt(Z_b**2 - R_b**2) * 1e3
base = point(p.P_BASE_MW, I_base, X_b)
print("2) Baseline (A-14: 55 MW at 65 MVA)")
show("   Baseline 55 MW", base); rows.append(("Baseline 55 MW", base))

# ---------------------------------------------------------------- 3 Uprate cases
print("\n3) 60 MW cases")
# 3a Westly-ideal current, existing reactance
w = point(p.P_NEW_MW, C3_cal * p.P_NEW_MW ** (2/3), X_b)
show("   3a Westly-ideal, X unchanged", w); rows.append(("60 MW Westly-ideal, X unchanged", w))
# 3b Constant R (same geometry, more current)
cR = point_from_RX(p.P_NEW_MW, base["R"], X_b)
show("   3b Constant R, X unchanged", cR); rows.append(("60 MW constant R, X unchanged", cR))
# 3c..e Minimum R that keeps S = 65 MVA, for reactance reductions
print("   -- Required R for S = 65 MVA (PF = 60/65 = 0.923):")
pf_req = p.P_NEW_MW / p.S_RATED_MVA
for xr in (0.0, 0.10, 0.20, 0.30):
    X = X_b * (1 - xr)
    R_req = X * pf_req / math.sqrt(1 - pf_req**2)
    d = point_from_RX(p.P_NEW_MW, R_req, X)
    show(f"   3c X -{xr*100:3.0f} %  (R +{(R_req/base['R']-1)*100:4.1f} %)", d)
    rows.append((f"60 MW at 65 MVA, X -{xr*100:.0f}%", d))

# ---------------------------------------------------------------- 4 Sensitivity
print("\n4) Sensitivity: baseline calibration across literature C3 range (A-14 held)")
for c3 in (6.0, 7.0, C3_cal, 9.0, 11.0):
    Ib = c3 * p.P_BASE_MW ** (2/3) * 1e3
    Rb = p.P_BASE_MW * 1e6 / (3 * Ib**2); Zb = p.S_BASE_MVA * 1e6 / (3 * Ib**2)
    Xb = math.sqrt(Zb**2 - Rb**2)
    R_req = Xb * pf_req / math.sqrt(1 - pf_req**2)
    print(f"   C3={c3:5.2f}: I_base={Ib/1e3:6.1f} kA, R_base={Rb*1e3:.3f}, X={Xb*1e3:.3f} mΩ "
          f"-> R_req(60 MW)={R_req*1e3:.3f} mΩ (+{(R_req/Rb-1)*100:.0f} %), "
          f"V_LL base={math.sqrt(3)*p.S_BASE_MVA*1e6/(3*Ib):.0f} V")
print("   -> The REQUIRED % increase in R/X is independent of C3 (it depends only on PF):")
rx = lambda pf: pf / math.sqrt(1 - pf**2)
pf_b = p.P_BASE_MW / p.S_BASE_MVA
print(f"      R/X: {rx(pf_b):.3f} -> {rx(pf_req):.3f}  (+{(rx(pf_req)/rx(pf_b)-1)*100:.1f} %)")
print("\n   Electrical efficiency (A-06): S needed for 60 MW in bath at the 3c(X unchanged) PF")
for eta in p.ETA_EL_RANGE:
    print(f"      eta={eta:.2f}: PF needed = {p.P_NEW_MW/eta/p.S_RATED_MVA:.3f}")

# ---------------------------------------------------------------- 5 Output
with open(os.path.join(OUT, "02_operating_points.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    keys = ["P", "I", "R", "X", "Z", "PF", "S", "Q", "VLL", "J", "C3"]
    wr.writerow(["case", "P_MW", "I_kA", "R_mohm", "X_mohm", "Z_mohm", "PF", "S_MVA",
                 "Q_Mvar", "V_LL_V", "J_A_cm2", "C3"])
    for name, d in rows:
        wr.writerow([name] + [round(d[k], 4) for k in keys])

# Operating chart: P vs I at constant X, with 65 MVA limit and J guideline
fig, ax = plt.subplots(figsize=(8, 5.5))
Ivals = np.linspace(80, 140, 300)
for xr, ls in ((0.0, "-"), (0.2, "--")):
    X = X_b * (1 - xr) * 1e-3
    # P at S = 65 MVA: Z = S/(3I^2), R = sqrt(Z^2 - X^2)
    Z = p.S_RATED_MVA * 1e6 / (3 * (Ivals * 1e3) ** 2)
    R = np.sqrt(np.clip(Z**2 - X**2, 0, None))
    ax.plot(Ivals, 3 * (Ivals * 1e3) ** 2 * R / 1e6, ls, color="C0",
            label=f"65 MVA limit, X = {X*1e3:.3f} mΩ" + (" (−20 %)" if xr else " (existing)"))
for Rm in (1.0, 1.265, 1.5, 1.9):
    ax.plot(Ivals, 3 * (Ivals * 1e3) ** 2 * Rm * 1e-3 / 1e6, ":", color="grey", lw=1)
    I_lab = min(math.sqrt(72e6 / (3 * Rm * 1e-3)) / 1e3, 136)   # label inside axes
    ax.annotate(f"R={Rm} mΩ", (I_lab, 3 * (I_lab * 1e3) ** 2 * Rm * 1e-3 / 1e6),
                fontsize=7, color="grey", rotation=55, xytext=(3, -12), textcoords="offset points")
ax.axhline(p.P_NEW_MW, color="C3", lw=1); ax.axhline(p.P_BASE_MW, color="C2", lw=1)
for jg in p.J_GUIDE_A_CM2:
    ax.axvline(jg * area_cm2(p.D_ELECTRODE_M) / 1e3, color="C1", lw=1, ls="-.")
ax.text(p.J_GUIDE_A_CM2[1] * area_cm2(p.D_ELECTRODE_M) / 1e3 + 0.5, 42,
        "J guideline\n4.5–5 A/cm²\n(D=1.55 m)", fontsize=7, color="C1")
for name, d in rows:
    if name.startswith(("Baseline", "60 MW Westly", "60 MW at 65 MVA, X -0", "60 MW at 65 MVA, X -20")):
        ax.plot(d["I"], d["P"], "o"); ax.annotate(name, (d["I"], d["P"]), fontsize=7,
                                                   xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("Electrode current I (kA)"); ax.set_ylabel("Furnace active power P (MW)")
ax.set_ylim(40, 75); ax.set_xlim(80, 140); ax.grid(alpha=0.3)
ax.set_title("Operating chart – reference furnace, 65 MVA total (calc 02)")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "02_operating_chart.png"), dpi=150)
print("\nWrote results/02_operating_points.csv and results/02_operating_chart.png")
