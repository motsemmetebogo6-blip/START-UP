"""
run_sensitivity_ch16.py – Chapter 16 (Simphiwe): sensitivity of project NPV and of electrical and
auxiliary-system performance for the selected design C1.

Economic model = Sibandze Ch. 15 method (verified in I1: S-09…S-18), updated with:
  * conservative C1 production (ambient preheat reference, AF-14)
  * reconciled mass balance: ore 2.144 t/t, reductant 0.433 t/t, flux 0.366 t/t (Ch. 8)
All economic inputs are Ch. 15 assumptions unless stated; ranges are assumptions (A-28).
Outputs: results/model/CH16_*.csv, report/figures/F12–F15, model/inputs/octave_npv.csv
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, massbalance as mb   # noqa: E402

ROOT = data_io.ROOT; OUT = os.path.join(ROOT, "results", "model"); FIG = os.path.join(ROOT, "report", "figures")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "legend.fontsize": 7.5})
inp = data_io.load_inputs(); res, _, _ = mb.full_balance(inp)
S, PROD0 = 65.0, inp["wb.ferrochrome_production_baseline"].value

BASE = dict(
    price_usd=1500.0,      # US$/t alloy net (Ch. 15, SMM 2026 benchmark)
    fx=17.42,              # R/US$ (Ch. 15)
    elec=1.65,             # R/kWh (Ch. 15, [A])
    capex_core=310.0,      # R M before contingency (Ch. 14)
    contingency=0.20, shutdown=30.0,
    ore_rate=res["m_ore"] / 1000, ore_price=2800.0,
    red_rate=res["m_reductant_dry"] / 1000, red_price=2800.0,
    flux_rate=(res["m_quartz"] + res["m_limestone"]) / 1000, flux_price=700.0,
    paste_kg=10.0, paste_price=16500.0,
    tax=0.27, disc=0.12, years=15,
    save=0.070, T=500.0, T_ref=25.0, LF=0.972, PF=0.95, SEC0=3.5,
)


def economics(p):
    P_A = S * 0.93 * 0.95
    P_C = S * p["PF"] * p["LF"]
    sec = p["SEC0"] - p["save"] * (p["T"] - p["T_ref"]) / 100.0
    prod = 24.0 * P_C / sec
    dt = (prod - PROD0) * 365.0                                  # extra t/yr
    rev = dt * p["price_usd"] * p["fx"] / 1e6
    capex = p["capex_core"] * (1 + p["contingency"]) + p["shutdown"]
    opex = ((P_C - P_A) * 8760 * p["elec"] / 1e3
            + dt * p["ore_rate"] * p["ore_price"] / 1e6 + dt * p["red_rate"] * p["red_price"] / 1e6
            + dt * p["flux_rate"] * p["flux_price"] / 1e6 + dt * p["paste_kg"] / 1000 * p["paste_price"] / 1e6
            + 0.015 * p["capex_core"] + 2.0)
    profit = rev - opex
    cf = profit - p["tax"] * (profit - capex / p["years"])          # straight-line depreciation shield
    ann = (1 - (1 + p["disc"]) ** -p["years"]) / p["disc"]
    npv = cf * ann - capex
    lo, hi = 1e-6, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cf * (1 - (1 + mid) ** -p["years"]) / mid - capex > 0: lo = mid
        else: hi = mid
    return dict(production=prod, dt=dt, revenue=rev, opex=opex, profit=profit, capex=capex, cf=cf, npv=npv,
                irr=lo, payback=capex / cf if cf > 0 else float("inf"), P_mean=P_C, sec=sec)


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    b = economics(BASE)
    # --- reproduce Sibandze's original case as a check (457.1 t/d, ore 2.13, flux 0.449, red 0.433)
    orig = dict(BASE, T_ref=0.0, ore_rate=2.13, flux_rate=0.449, red_rate=0.433)
    o = economics(orig)
    write("CH16_base_case.csv", ["quantity", "updated base (reconciled, conservative)", "Sibandze Ch15 basis (reproduced)", "unit"], [
        ["C1 production", round(b["production"], 2), round(o["production"], 2), "t/d"],
        ["Extra alloy", round(b["dt"], 0), round(o["dt"], 0), "t/yr"],
        ["Incremental revenue", round(b["revenue"], 1), round(o["revenue"], 1), "R M/yr"],
        ["Incremental operating cost", round(b["opex"], 1), round(o["opex"], 1), "R M/yr"],
        ["Incremental profit (pre-tax)", round(b["profit"], 1), round(o["profit"], 1), "R M/yr"],
        ["Total investment", round(b["capex"], 1), round(o["capex"], 1), "R M"],
        ["After-tax cash flow", round(b["cf"], 1), round(o["cf"], 1), "R M/yr"],
        ["NPV (15 y, 12 %)", round(b["npv"], 0), round(o["npv"], 0), "R M"],
        ["IRR", round(100 * b["irr"], 1), round(100 * o["irr"], 1), "%"],
        ["Simple payback (after tax)", round(b["payback"], 2), round(o["payback"], 2), "years"],
    ])

    # --- one-at-a-time NPV tornado (ranges = A-28)
    ranges = [
        ("price_usd", 1200, 1800, "Alloy price (US$1 200–1 800/t)"),
        ("fx", 16.0, 18.5, "Exchange rate (R16.00–18.50/US$)"),
        ("save", 0.035, 0.070, "Hot-charge saving (0.035–0.070 MWh/t per 100 °C)"),
        ("capex_core", 310 * 0.8, 310 * 1.4, "Capital cost (−20 % / +40 %)"),
        ("LF", 0.95, 0.98, "Load factor achieved (0.95–0.98)"),
        ("ore_price", 2400, 3200, "Ore price (R2 400–3 200/t)"),
        ("disc", 0.10, 0.14, "Discount rate (10–14 %)"),
        ("ore_rate", res["m_ore"] / 1000, 2.39, "Ore rate (2.14 reconciled – 2.39 if 78 % recovery)"),
        ("elec", 1.45, 1.85, "Electricity tariff (R1.45–1.85/kWh)"),
        ("PF", 0.93, 0.95, "Power factor achieved (0.93–0.95)"),
        ("red_price", 2400, 3200, "Reductant price (R2 400–3 200/t)"),
    ]
    rows = []
    for k, lo, hi, lab in ranges:
        nl = economics(dict(BASE, **{k: lo})); nh = economics(dict(BASE, **{k: hi}))
        rows.append([lab, k, lo, hi, round(nl["npv"], 1), round(nh["npv"], 1), round(abs(nh["npv"] - nl["npv"]), 1),
                     round(nl["production"], 1), round(nh["production"], 1)])
    rows.sort(key=lambda r: -r[6])
    write("CH16_npv_tornado.csv", ["input", "key", "low", "high", "NPV_at_low_RM", "NPV_at_high_RM", "swing_RM",
                                   "production_at_low_tpd", "production_at_high_tpd"], rows)
    # break-even values (NPV = 0) for key inputs
    def breakeven(k, a, bnd):
        f = lambda v: economics(dict(BASE, **{k: v}))["npv"]
        lo, hi = a, bnd
        if f(lo) * f(hi) > 0: return None
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(lo) * f(mid) <= 0: hi = mid
            else: lo = mid
        return (lo + hi) / 2
    be = [["Alloy price for NPV = 0", breakeven("price_usd", 100, 1500), "US$/t"],
          ["Capital cost (core) for NPV = 0", breakeven("capex_core", 310, 5000), "R M"],
          ["Hot-charge saving for NPV = 0", breakeven("save", 0.0, 0.07), "MWh/t per 100 °C"]]
    write("CH16_breakeven.csv", ["quantity", "value", "unit"], [[a, round(v, 3) if v is not None else "not reached", u] for a, v, u in be])

    # --- F12 NPV tornado
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for i, r in enumerate(reversed(rows)):
        ax.barh(i, r[4] - b["npv"], left=b["npv"], color="#B9B9B9"); ax.barh(i, r[5] - b["npv"], left=b["npv"], color="#3B6E8F")
        ax.text(min(r[4], r[5]) - 25, i, f"{min(r[4], r[5]):,.0f}", ha="right", va="center", fontsize=6.5)
        ax.text(max(r[4], r[5]) + 25, i, f"{max(r[4], r[5]):,.0f}", ha="left", va="center", fontsize=6.5)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=7)
    ax.axvline(b["npv"], color="k", lw=0.8); ax.axvline(0, color="C3", lw=1)
    ax.set_xlabel("Project NPV (R million, 15 years, after tax)")
    ax.set_title(f"Tornado: effect of each assumption on project NPV (base R{b['npv']:,.0f} M)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#B9B9B9", label="input at low end"), Patch(color="#3B6E8F", label="input at high end")], loc="lower right")
    fig.text(0.01, -0.03, "Economic basis: Ch. 15 (Sibandze) updated with reconciled mass balance (Ch. 8) and conservative C1 production 454.6 t/d. Ranges: assumption A-28.",
             fontsize=6, color="0.4")
    save(fig, "F12_npv_tornado")

    # --- F13 spider plot (NPV vs % change in input)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for k, lab, col in (("price_usd", "Alloy price", "C0"), ("fx", "Exchange rate", "C1"), ("capex_core", "Capital cost", "C3"),
                        ("ore_price", "Ore price", "C4"), ("elec", "Electricity tariff", "C2"), ("save", "Hot-charge saving", "C5")):
        pct = np.linspace(-0.3, 0.3, 25)
        npv = [economics(dict(BASE, **{k: BASE[k] * (1 + x)}))["npv"] for x in pct]
        ax.plot(100 * pct, npv, color=col, label=lab, ls="--" if k == "fx" else "-", lw=2.2 if k == "fx" else 1.5)
    ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6, ls=":")
    ax.set_xlabel("Change in input from base case (%)"); ax.set_ylabel("NPV (R million)")
    ax.set_title("Spider plot: NPV response to each assumption"); ax.legend(ncol=2); ax.grid(alpha=0.25)
    fig.text(0.01, -0.03, "Alloy price and exchange rate act only through revenue (price × FX), so their lines coincide (FX shown dashed).", fontsize=6.5, color="0.4")
    save(fig, "F13_npv_spider")

    # --- F14 electrical performance sensitivity (separate technical plot)
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.4))
    pf = np.linspace(0.88, 0.96, 81)
    ax[0].plot(pf, 60 / pf, color="#3B6E8F", label="60 MW on load")
    ax[0].plot(pf, (60 / 0.972) / pf, color="#7A1F1F", label="60 MW mean (LF 0.972)")
    ax[0].axhline(65, color="C3", lw=1); ax[0].text(0.881, 65.3, "65 MVA rating", color="C3", fontsize=7)
    ax[0].axvspan(0.95, 0.96, color="0.85"); ax[0].set_xlabel("Power factor"); ax[0].set_ylabel("On-load apparent power (MVA)")
    ax[0].set_title("Transformer loading vs power factor"); ax[0].legend(fontsize=7); ax[0].grid(alpha=0.25)
    lf = np.linspace(0.94, 0.99, 51)
    for pfv, col in ((0.93, "#B9B9B9"), (0.94, "#C9A227"), (0.95, "#3B6E8F")):
        ax[1].plot(lf, S * pfv * lf, color=col, label=f"PF {pfv}")
    ax[1].axhline(60, color="C3", lw=1); ax[1].axhline(57.43, color="k", lw=0.6, ls=":")
    ax[1].text(0.941, 60.2, "60 MW mean target", color="C3", fontsize=7); ax[1].text(0.941, 56.9, "existing 57.43 MW", fontsize=7)
    ax[1].set_xlabel("Load factor"); ax[1].set_ylabel("Mean active power (MW)"); ax[1].set_title("Mean power vs load factor")
    ax[1].legend(fontsize=7); ax[1].grid(alpha=0.25)
    fig.tight_layout(); save(fig, "F14_electrical_sensitivity")

    # --- F15 auxiliary-system performance sensitivity (separate technical plot)
    fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.4))
    prod = np.linspace(390, 470, 81)
    for m, col in ((0.05, "#C62828"), (0.10, "#C9A227"), (0.15, "#3B6E8F"), (0.20, "#2E7D32")):
        ax[0].plot(prod, 100 * (prod / PROD0) / (1 + m), color=col, label=f"design margin {int(m*100)} %")
    ax[0].axhline(90, color="k", lw=0.8, ls="--"); ax[0].text(391, 91, "DC-06 limit 90 %", fontsize=7)
    ax[0].axvline(b["production"], color="#7A1F1F", lw=0.8); ax[0].text(b["production"] - 1, 112, "C1", ha="right", fontsize=7, color="#7A1F1F")
    ax[0].set_xlabel("Alloy production (t/d)"); ax[0].set_ylabel("Auxiliary utilisation (% of design)")
    ax[0].set_title("Auxiliary utilisation vs production (A-22 varied)"); ax[0].legend(fontsize=6.5); ax[0].grid(alpha=0.25)
    gas = res["gas_Nm3"]
    ax[1].plot(prod, gas * prod / 24, color="#D9822B", lw=2.4, label="Off-gas (Nm³/h, left)")
    ax2 = ax[1].twinx(); ax2.plot(prod, res["m_slag"] / 1000 * prod, color="#404040", ls="--", lw=1.2, label="Slag (t/d, right)")
    for xx in (PROD0, b["production"]):
        ax[1].annotate(f"{gas*xx/24:,.0f} Nm³/h\n{res['m_slag']/1000*xx:.0f} t/d slag", (xx, gas * xx / 24), xytext=(-70 if xx > 430 else 8, 8),
                       textcoords="offset points", fontsize=6.5)
    h1, l1 = ax[1].get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax[1].legend(h1 + h2, l1 + l2, fontsize=6.5, loc="lower right")
    ax[1].axvline(PROD0, color="k", lw=0.6, ls=":"); ax[1].axvline(b["production"], color="#7A1F1F", lw=0.8)
    ax[1].set_xlabel("Alloy production (t/d)"); ax[1].set_ylabel("Off-gas (Nm³/h)", color="#D9822B"); ax2.set_ylabel("Slag (t/d)", color="#7A7A7A")
    ax[1].set_title("Off-gas and slag duty vs production")
    fig.tight_layout(); save(fig, "F15_auxiliary_sensitivity")

    # --- comparison table: technical + economic for the scenarios at C1 inputs varied
    comp = []
    for lab, over in (("Base case C1", {}), ("Hot-charge saving halved", {"save": 0.035}), ("Load factor stays 0.95", {"LF": 0.95}),
                      ("Power factor stays 0.93", {"PF": 0.93}), ("Alloy price US$1 200/t", {"price_usd": 1200}),
                      ("Capital cost +40 %", {"capex_core": 434}), ("Ore rate 2.39 t/t (78 % recovery)", {"ore_rate": 2.39})):
        e = economics(dict(BASE, **over))
        comp.append([lab, round(e["P_mean"], 2), round(e["sec"], 3), round(e["production"], 1), "YES" if e["production"] >= 450 else "no",
                     round(100 * (e["production"] / PROD0) / 1.10, 1), round(e["npv"], 0), round(100 * e["irr"], 1), round(e["payback"], 2)])
    write("CH16_comparison.csv", ["case", "P_mean_MW", "SEC_MWh_t", "production_tpd", "meets_450", "aux_util_pct_(10%_margin)",
                                  "NPV_RM", "IRR_pct", "payback_y"], comp)
    with open(os.path.join(ROOT, "model", "inputs", "octave_npv.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["prod", "prod0", "Pmean_C", "Pmean_A", "price", "fx", "elec", "capex_core", "cont", "shutdown",
                                       "ore_rate", "ore_price", "red_rate", "red_price", "flux_rate", "flux_price", "paste_kg", "paste_price",
                                       "tax", "disc", "years"])
        w.writerow([b["production"], PROD0, b["P_mean"], S * 0.93 * 0.95] + [BASE[k] for k in ("price_usd", "fx", "elec", "capex_core",
                   "contingency", "shutdown", "ore_rate", "ore_price", "red_rate", "red_price", "flux_rate", "flux_price", "paste_kg",
                   "paste_price", "tax", "disc", "years")])
    with open(os.path.join(OUT, "CH16_python_npv.csv"), "w") as f:
        f.write(f"npv,cf\n{float(b['npv'])!r},{float(b['cf'])!r}\n")
    print(f"Base (updated): production {b['production']:.1f} t/d, NPV R{b['npv']:.0f} M, IRR {100*b['irr']:.1f} %, payback {b['payback']:.2f} y")
    print(f"Sibandze basis reproduced: NPV R{o['npv']:.0f} M (Ch15 states ≈ R1 540 M), IRR {100*o['irr']:.1f} %")
    print("Top 4 NPV drivers:", [r[0] for r in rows[:4]])
    print("Break-even:", be)


if __name__ == "__main__":
    main()
