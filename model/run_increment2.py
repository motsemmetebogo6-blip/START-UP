"""
run_increment2.py – Increment 2: mass balance (data reconciliation), optimisation and uncertainty.
Run from repo root:  python3 model/run_increment2.py
Outputs: results/model/I2_*.csv, model/inputs/octave_massbalance_*.csv, report/figures/F4–F10
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, massbalance as mb, optimise as op, production as pr   # noqa: E402

ROOT = data_io.ROOT
OUT = os.path.join(ROOT, "results", "model"); FIG = os.path.join(ROOT, "report", "figures")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "legend.fontsize": 8})
NOTE_MB = "Provenance: compositions and recipe – data workbook (measured means); balance – weighted least squares (safmodel I2)."


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    inp = data_io.load_inputs()
    S = inp["wb.transformer_capacity"].value; SEC0 = inp["wb.specific_energy_baseline"].value
    s = inp["asm.hot_charge_sec_saving_per_100C"].value
    prod_A = inp["wb.ferrochrome_production_baseline"].value
    prod_C1 = pr.production_tpd(60.0, pr.hot_charge_sec(SEC0, s, 500, 25))        # conservative (AF-14)

    # ================================================================ MASS BALANCE
    res, eqs, (A, b, names, x) = mb.full_balance(inp)
    ore, red, q, lime, alloy, slag = mb.feeds_from_inputs(inp)
    per_t = [
        ("IN", "Ore blend (80 % pellets / 20 % lumpy)", res["m_ore"]),
        ("IN", "Reductant, dry (10 % coke / 90 % anthracite)", res["m_reductant_dry"]),
        ("IN", "Reductant moisture", res["m_reductant_moisture"]),
        ("IN", "Quartz", res["m_quartz"]),
        ("IN", "Limestone", res["m_limestone"]),
        ("OUT", "Alloy (HC FeCr)", 1000.0),
        ("OUT", "Slag", res["m_slag"]),
        ("OUT", "CO (reduction gas)", res["CO_kg"]),
        ("OUT", "CO2 (limestone calcination)", res["CO2_lime_kg"]),
        ("OUT", "H2O (reductant moisture)", res["H2O_kg"]),
        ("OUT", "Volatile matter", res["VM_kg"]),
    ]
    rows = [[d, n, round(v, 2), round(v * prod_A / 1000, 2), round(v * prod_C1 / 1000, 2)] for d, n, v in per_t]
    rows.append(["CHECK", "Mass in", round(res["mass_in"], 2), "", ""])
    rows.append(["CHECK", "Mass out", round(res["mass_out"], 2), "", ""])
    rows.append(["CHECK", "Closure (out-in)/in, %", round(res["closure_pct"], 3), "", ""])
    write("I2_mass_balance.csv", ["direction", "stream", "kg_per_t_alloy", "t_per_day_existing_393.65",
                                  f"t_per_day_C1_{prod_C1:.1f}"], rows)
    write("I2_balance_residuals.csv", ["equation", "feed_kg_per_t", "residual_kg_per_t", "residual_pct_of_feed", "residual_scaled_pct"],
          [[e["equation"], round(e["feed_kg"], 3), round(e["residual_kg"], 3), round(e["residual_rel_pct"], 3),
            round(e["residual_scaled_pct"], 3)] for e in eqs])
    kpi = [
        ["Cr recovery to alloy (reconciled)", round(100 * res["Cr_recovery"], 2), "%", "CALCULATED", "output of balance"],
        ["Cr recovery (workbook assumption)", 78.0, "%", "ASSUMED", "Workbook!Assumptions C19"],
        ["Cr in feed", round(res["Cr_in"], 1), "kg/t", "CALCULATED", ""],
        ["Cr to slag", round(res["Cr_slag"], 1), "kg/t", "CALCULATED", ""],
        ["Cr unaccounted (dust/fume, measurement error)", round(res["Cr_unaccounted"], 1), "kg/t", "CALCULATED", "negative = slight over-closure"],
        ["Slag rate", round(res["m_slag"] / 1000, 3), "t/t", "CALCULATED", ""],
        ["Ore rate", round(res["m_ore"] / 1000, 3), "t/t", "CALCULATED", "team used 2.13 (estimate)"],
        ["Reductant rate, dry", round(res["m_reductant_dry"] / 1000, 3), "t/t", "CALCULATED", "team used 0.433"],
        ["Flux rate (quartz + limestone)", round((res["m_quartz"] + res["m_limestone"]) / 1000, 3), "t/t", "CALCULATED", "team used 0.449"],
        ["Quartz share of flux (free result)", round(100 * res["m_quartz"] / (res["m_quartz"] + res["m_limestone"]), 1), "%", "CALCULATED", "workbook recipe 55 %"],
        ["Oxygen removed by reduction", round(res["O_removed"], 1), "kg/t", "CALCULATED", ""],
        ["Off-gas volume (CO+CO2+H2O)", round(res["gas_Nm3"], 1), "Nm3/t", "CALCULATED", "VM not included"],
        ["Off-gas, existing", round(res["gas_Nm3"] * prod_A / 24, 0), "Nm3/h", "CALCULATED", f"{prod_A} t/d"],
        ["Off-gas, C1", round(res["gas_Nm3"] * prod_C1 / 24, 0), "Nm3/h", "CALCULATED", f"{prod_C1:.1f} t/d"],
        ["Mass closure", round(res["closure_pct"], 3), "%", "CALCULATED", ""],
        ["Max |relative residual| of the 7 balances", round(max(abs(e["residual_rel_pct"]) for e in eqs), 3), "%", "CALCULATED", "data consistency"],
    ]
    write("I2_mass_balance_kpis.csv", ["kpi", "value", "unit", "provenance", "note"], kpi)

    # export compositions for independent Octave/MATLAB build of the equations
    comp = os.path.join(ROOT, "model", "inputs", "octave_massbalance_compositions.csv")
    with open(comp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stream", "Cr2O3", "FeO", "Fe2O3", "Al2O3", "MgO", "CaO", "SiO2", "FC"])
        w.writerow([1, ore["Cr2O3"], ore["FeO"], 0, ore["Al2O3"], ore["MgO"], ore["CaO"], ore["SiO2"], 0])
        w.writerow([2, 0, 0, red["Fe2O3"], red["Al2O3"], red["MgO"], red["CaO"], red["SiO2"], red["FC"]])
        w.writerow([3, 0, 0, q["Fe2O3"], q["Al2O3"], q["MgO"], q["CaO"], q["SiO2"], 0])
        w.writerow([4, 0, 0, lime["Fe2O3"], lime["Al2O3"], lime["MgO"], lime["CaO"], lime["SiO2"], 0])
        w.writerow([5, slag["Cr2O3"], slag["FeO"], 0, slag["Al2O3"], slag["MgO"], slag["CaO"], slag["SiO2"], slag["C"]])
    with open(os.path.join(ROOT, "model", "inputs", "octave_massbalance_alloy.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Cr", "Fe", "Si", "C"]); w.writerow([alloy["Cr"], alloy["Fe"], alloy["Si"], alloy["C"]])
    with open(os.path.join(OUT, "I2_python_massbalance.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["m_ore", "m_red", "m_quartz", "m_lime", "m_slag", "Cr_recovery"])
        w.writerow([repr(float(v)) for v in list(x) + [res["Cr_recovery"]]])

    # ================================================================ OPTIMISATION
    opt_rows = []
    for LFmax in (0.95, 0.96, 0.965, 0.972, 0.975, 0.98):
        for Tref, lab in ((0.0, "project rule (0 C ref)"), (25.0, "ambient ref (AF-14)")):
            r = op.solve_min_T(S, SEC0, s, Tref, LFmax)
            Tcf = op.T_closed_form(0.95, LFmax, S, SEC0, s, Tref)
            opt_rows.append([LFmax, lab, round(r.x[0], 4), round(r.x[1], 4), round(r.x[2], 1), round(Tcf, 1),
                             round(abs(r.x[2] - Tcf), 4), round(op.production(*r.x, S, SEC0, s, Tref), 2)])
    write("I2_optimisation_minT.csv", ["LF_max", "T_reference", "PF_opt", "LF_opt", "T_opt_SLSQP_C",
                                       "T_closed_form_C", "abs_diff_C", "production_at_opt_tpd"], opt_rows)

    # ================================================================ UNCERTAINTY (C1)
    rng = np.random.default_rng(20261127)
    N = 100000
    dist = {
        "s": lambda g, n: g.uniform(0.035, 0.070, n),          # half to full vendor saving (A-27)
        "T": lambda g, n: g.triangular(450, 500, 550, n),       # achieved preheat temperature (A-27)
        "LF": lambda g, n: g.triangular(0.95, 0.972, 0.98, n),  # achieved load factor (A-27)
        "PF": lambda g, n: g.triangular(0.93, 0.95, 0.95, n),   # achieved power factor (A-27)
        "SEC0": lambda g, n: g.normal(3.5, 0.035, n),           # 1 % s.d. on cold SEC (A-27)
        "T_ref": lambda g, n: np.full(n, 25.0),
    }
    M, smp = op.monte_carlo(N, S, SEC0, rng, dist)
    p450 = float((M >= 450).mean())
    pct = np.percentile(M, [5, 50, 95])
    write("I2_montecarlo_summary.csv", ["metric", "value"],
          [["samples", N], ["P(production >= 450 t/d)", round(p450, 4)], ["P5 t/d", round(pct[0], 1)],
           ["P50 t/d", round(pct[1], 1)], ["P95 t/d", round(pct[2], 1)], ["mean t/d", round(M.mean(), 1)]])
    base = dict(s=0.07, T=500.0, LF=0.972, PF=0.95, SEC0=3.5, T_ref=25.0)
    ranges = {"s": (0.035, 0.070, "Hot-charge SEC saving (0.035–0.070 MWh/t per 100 °C)"),
              "T": (450.0, 550.0, "Preheat temperature (450–550 °C)"),
              "LF": (0.95, 0.98, "Load factor (0.95–0.98)"),
              "PF": (0.93, 0.95, "Power factor (0.93–0.95)"),
              "SEC0": (3.43, 3.57, "Cold-charge SEC (±2 %)"),
              "T_ref": (0.0, 25.0, "Preheat reference temperature (0 / 25 °C)")}
    M0, tor = op.tornado(base, ranges, S)
    write("I2_tornado.csv", ["input", "key", "low", "high", "production_at_low", "production_at_high"],
          [[t[0], t[1], t[2], t[3], round(t[4], 1), round(t[5], 1)] for t in tor])

    # ================================================================ FIGURES
    # F4 – mass in vs out
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ins = [(n, v) for d, n, v in per_t if d == "IN"]; outs = [(n, v) for d, n, v in per_t if d == "OUT"]
    cin = ["#3B6E8F", "#2F2F2F", "#8FB8D0", "#C9A227", "#B9B9B9"]
    cout = ["#7A1F1F", "#A0A0A0", "#D9822B", "#E6B87A", "#9CC3DA", "#CFCFCF"]
    for row, items, cols in ((1, ins, cin), (0, outs, cout)):
        left = 0
        for (n, v), c in zip(items, cols):
            ax.barh(row, v, left=left, color=c, edgecolor="white", height=0.55, label=f"{n} ({v:.0f} kg)")
            if v > 400: ax.text(left + v / 2, row, f"{n.split('(')[0].strip()}\n{v:.0f}", ha="center", va="center", fontsize=6.5,
                               color="white" if c not in ("#B9B9B9", "#CFCFCF", "#E6B87A", "#8FB8D0", "#9CC3DA") else "black")
            left += v
        ax.text(left + 30, row, f"{left:,.0f} kg", va="center", fontsize=8)
    ax.set_yticks([1, 0]); ax.set_yticklabels(["Inputs", "Outputs"]); ax.set_xlim(0, 3400); ax.set_ylim(-0.6, 1.6)
    ax.legend(fontsize=6, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.22), frameon=False)
    ax.set_xlabel("kg per tonne of alloy")
    ax.set_title(f"Reconciled mass balance per tonne of alloy (closure {res['closure_pct']:+.2f} %)")
    fig.text(0.01, -0.42, NOTE_MB, fontsize=6, color="0.4"); save(fig, "F4_mass_balance")

    # F5 – residuals
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    ev = [e["residual_rel_pct"] for e in eqs]; en = [e["equation"] for e in eqs]
    ax.bar(en, ev, color=["C3" if abs(v) > 3 else "C0" for v in ev])
    ax.axhspan(-3, 3, color="C2", alpha=0.08); ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel("Residual, % of species feed"); ax.set_ylim(-4, 4)
    ax.set_title("Data consistency: all seven balances close within ±3 % of species feed")
    for i, v in enumerate(ev): ax.text(i, v + (0.15 if v >= 0 else -0.35), f"{v:+.2f}", ha="center", fontsize=7)
    fig.text(0.01, -0.05, "Residual = (feed − products)/feed for each element/oxide; ±3 % band shown. " + NOTE_MB, fontsize=6, color="0.4")
    save(fig, "F5_balance_residuals")

    # F6 – Cr distribution and recovery
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"width_ratios": [1.3, 1]})
    parts = [("Alloy", res["Cr_alloy"], "#7A1F1F"), ("Slag (Cr2O3)", res["Cr_slag"], "#A0A0A0")]
    left = 0
    for n, v, c in parts:
        ax[0].barh(0, v, left=left, color=c)
        if v > 200: ax[0].text(left + v / 2, 0, f"{n}\n{v:.0f} kg", ha="center", va="center", color="white", fontsize=8)
        else: ax[0].annotate(f"{n}\n{v:.0f} kg", (left + v / 2, 0.3), xytext=(left + v / 2, 0.55), ha="center", fontsize=7,
                             arrowprops=dict(arrowstyle="-", lw=0.5))
        left += v
    ax[0].set_yticks([]); ax[0].set_xlabel("kg Cr per tonne alloy"); ax[0].set_ylim(-0.5, 0.8)
    ax[0].set_title(f"Chromium distribution (feed {res['Cr_in']:.0f} kg/t)")
    ax[1].bar(["Workbook\n(assumed)", "Reconciled\nbalance", "Target"], [78, 100 * res["Cr_recovery"], 93],
              color=["#B9B9B9", "#7A1F1F", "#3B6E8F"])
    for i, v in enumerate([78, 100 * res["Cr_recovery"], 93]): ax[1].text(i, v + 1, f"{v:.1f} %", ha="center", fontsize=8)
    ax[1].set_ylim(60, 100); ax[1].set_ylabel("Cr recovery (%)"); ax[1].set_title("Cr recovery")
    fig.text(0.01, -0.05, "Dust/fume Cr not measured; unaccounted Cr = " + f"{res['Cr_unaccounted']:+.1f} kg/t. " + NOTE_MB, fontsize=6, color="0.4")
    fig.tight_layout(); save(fig, "F6_chromium_recovery")

    # F7 – optimisation map
    pf = np.linspace(0.93, 0.95, 200); lf = np.linspace(0.95, 0.98, 200)
    PFm, LFm = np.meshgrid(pf, lf)
    Treq = op.T_closed_form(PFm, LFm, S, SEC0, s, 25.0)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    cf = ax.contourf(PFm, LFm, Treq, levels=np.arange(400, 720, 20), cmap="YlOrRd")
    cb = fig.colorbar(cf, ax=ax); cb.set_label("Hot-charge temperature needed for 450 t/d (°C)")
    c = ax.contour(PFm, LFm, Treq, levels=[452, 500, 550, 600], colors="k", linewidths=0.7)
    ax.clabel(c, fmt="%d °C", fontsize=7)
    Topt = op.T_closed_form(0.95, 0.972, S, SEC0, s, 25.0)
    ax.plot(0.95, 0.972, "D", color="C0", ms=7); ax.annotate(f"Optimum (C1)\nPF 0.95, LF 0.972\nT* = {Topt:.0f} °C", (0.95, 0.972),
                                                          xytext=(-120, -45), textcoords="offset points", fontsize=7,
                                                          arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.plot(0.93, 0.95, "o", color="k"); ax.annotate(f"Existing\nT = {op.T_closed_form(0.93, 0.95, S, SEC0, s, 25):.0f} °C needed",
                                                     (0.93, 0.95), xytext=(10, 25), textcoords="offset points", fontsize=7,
                                                     arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.set_xlabel("Power factor PF (upper limit 0.95)"); ax.set_ylabel("Load factor LF")
    ax.set_title("Optimisation: minimum hot-charge temperature to reach 450 t/d")
    fig.text(0.01, -0.04, "SEC(T) = 3.5 − 0.07·(T − 25)/100 (Metso rule, R-04; ambient reference). Constraints: S_on ≤ 65 MVA, PF ≤ 0.95.", fontsize=6, color="0.4")
    save(fig, "F7_optimisation_map")

    # F8 – Monte Carlo
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.hist(M, bins=80, color="#3B6E8F", alpha=0.85)
    ax.axvline(450, color="C3", lw=1.4); ax.text(451, ax.get_ylim()[1] * 0.9, "450 t/d target", color="C3", fontsize=8)
    ax.axvline(pct[1], color="k", ls="--", lw=0.8)
    ax.set_xlabel("C1 production (t/d)"); ax.set_ylabel("Frequency")
    ax.set_title(f"Monte-Carlo (n = {N:,}): P(≥ 450 t/d) = {100*p450:.0f} %;  P5–P95 = {pct[0]:.0f}–{pct[2]:.0f} t/d")
    fig.text(0.01, -0.05, "Assumed input distributions (A-27): saving U(0.035, 0.070); T Tri(450, 500, 550); LF Tri(0.95, 0.972, 0.98); PF Tri(0.93, 0.95, 0.95); SEC0 N(3.5, 0.035).",
             fontsize=6, color="0.4")
    save(fig, "F8_montecarlo")

    # F9 – tornado
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    for i, (label, k, lo, hi, Mlo, Mhi) in enumerate(reversed(tor)):
        ax.barh(i, Mlo - M0, left=M0, color="#B9B9B9"); ax.barh(i, Mhi - M0, left=M0, color="#3B6E8F")
        ax.text(min(Mlo, Mhi) - 1, i, f"{min(Mlo, Mhi):.0f}", ha="right", va="center", fontsize=7)
        ax.text(max(Mlo, Mhi) + 1, i, f"{max(Mlo, Mhi):.0f}", ha="left", va="center", fontsize=7)
    ax.set_yticks(range(len(tor))); ax.set_yticklabels([t[0] for t in reversed(tor)], fontsize=7)
    ax.axvline(M0, color="k", lw=0.8); ax.axvline(450, color="C3", lw=1.2)
    ax.set_xlabel("C1 production (t/d)"); ax.set_xlim(415, 475)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#B9B9B9", label="input at LOW end of range"), Patch(color="#3B6E8F", label="input at HIGH end of range")],
              fontsize=6.5, loc="lower left")
    ax.set_title(f"Tornado: what the 450 t/d result depends on (base {M0:.1f} t/d)")
    save(fig, "F9_tornado")

    # F10 – daily duties existing vs C1
    keys = [("Ore", "m_ore"), ("Reductant", "m_reductant_dry"), ("Flux", None), ("Slag", "m_slag")]
    va = [res["m_ore"], res["m_reductant_dry"], res["m_quartz"] + res["m_limestone"], res["m_slag"]]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    xx = np.arange(4); w = 0.38
    ax.bar(xx - w / 2, [v * prod_A / 1000 for v in va], w, label=f"Existing ({prod_A} t/d alloy)", color="#B9B9B9")
    ax.bar(xx + w / 2, [v * prod_C1 / 1000 for v in va], w, label=f"C1 ({prod_C1:.1f} t/d alloy)", color="#3B6E8F")
    for i, v in enumerate(va):
        ax.text(i + w / 2, v * prod_C1 / 1000 + 10, f"{v*prod_C1/1000:.0f}", ha="center", fontsize=7)
        ax.text(i - w / 2, v * prod_A / 1000 + 10, f"{v*prod_A/1000:.0f}", ha="center", fontsize=7)
    ax.set_xticks(xx); ax.set_xticklabels([k[0] for k in keys]); ax.set_ylabel("t/d")
    gA, gC = res["gas_Nm3"] * prod_A / 24, res["gas_Nm3"] * prod_C1 / 24
    ax.set_title(f"Auxiliary duties rise {100*(prod_C1/prod_A-1):.0f} %; off-gas {gA:,.0f} → {gC:,.0f} Nm³/h")
    ax.legend(); fig.text(0.01, -0.05, NOTE_MB, fontsize=6, color="0.4"); save(fig, "F10_daily_duties")

    # F11 – robust (chance-constrained) optimisation
    rng2 = np.random.default_rng(7)
    cases = [("Saving uncertain: U(0.035, 0.070)", {}, "#B9B9B9"),
             ("Saving verified ≈ 0.070 by plant trial", {"s_lo": 0.066, "s_hi": 0.070}, "#3B6E8F"),
             ("Saving verified ≈ 0.0525 (75 % of vendor)", {"s_lo": 0.050, "s_hi": 0.055}, "#C9A227")]
    rob_rows = []
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for lab, kw, col in cases:
        T90, curve = op.robust_T(S, SEC0, 450, 0.90, rng2, **kw)
        T50 = next((t for t, pp in curve if pp >= 0.5), None)
        ax.plot([c[0] for c in curve], [100 * c[1] for c in curve], color=col, label=f"{lab}: T50 = {T50} °C, T90 = {T90} °C")
        rob_rows.append([lab, T50, T90, round(dict(curve)[500], 3)])
    ax.axhline(90, color="C3", ls="--", lw=0.8); ax.axhline(50, color="0.5", ls=":", lw=0.8)
    ax.axvline(452, color="k", lw=0.7); ax.text(455, 4, "deterministic\noptimum 452 °C", fontsize=7)
    ax.axvline(500, color="C1", lw=0.7); ax.text(503, 20, "C1 design\n500 °C", fontsize=7, color="C1")
    ax.set_xlim(400, 1000); ax.set_ylim(0, 100); ax.set_xlabel("Design hot-charge temperature (°C)")
    ax.set_ylabel("P(production ≥ 450 t/d) (%)"); ax.legend(fontsize=6.5, loc="lower left"); ax.grid(alpha=0.25)
    ax.set_title("Robust optimisation: preheat temperature for a 90 % chance of 450 t/d")
    fig.text(0.01, -0.05, "LF Tri(0.95, 0.972, 0.98), PF Tri(0.93, 0.95, 0.95), SEC0 N(3.5, 0.035), achieved T = design ±50 °C (triangular) – assumptions A-27.",
             fontsize=6, color="0.4")
    save(fig, "F11_robust_optimisation")
    write("I2_robust_optimisation.csv", ["case", "T_for_P50_C", "T_for_P90_C", "P_at_500C"], rob_rows)

    print(f"Mass balance: ore {res['m_ore']:.1f}, reductant {res['m_reductant_dry']:.1f}, quartz {res['m_quartz']:.1f}, "
          f"limestone {res['m_limestone']:.1f}, slag {res['m_slag']:.1f} kg/t; Cr recovery {100*res['Cr_recovery']:.2f} %; "
          f"closure {res['closure_pct']:+.3f} %")
    print(f"Optimum T* (LF 0.972, ambient ref) = {Topt:.1f} C; SLSQP/closed-form max diff = {max(r[6] for r in opt_rows):.2e} C")
    print(f"Monte-Carlo P(>=450) = {p450:.3f}; P5/P50/P95 = {pct[0]:.1f}/{pct[1]:.1f}/{pct[2]:.1f}; tornado base {M0:.1f}")
    return res


if __name__ == "__main__":
    main()
