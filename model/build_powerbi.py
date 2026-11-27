"""
build_powerbi.py – Power BI pack (Power BI Desktop is not available in this environment):
  powerbi/SAF_PowerBI_Dataset.xlsx   star schema, each table as an Excel table (Get Data > Excel)
  powerbi/SAF_measures.dax           DAX measures
  powerbi/SAF_theme.json             report theme
  report/figures/PBI_page*.png       page mock-ups rendered from the SAME dataset (design reference)
Every row carries its provenance so the dashboard can filter by evidence type.
"""
import csv
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, massbalance as mb, optimise as op, production as pr   # noqa: E402

ROOT = data_io.ROOT
PBI = os.path.join(ROOT, "powerbi"); FIG = os.path.join(ROOT, "report", "figures"); RES = os.path.join(ROOT, "results", "model")
os.makedirs(PBI, exist_ok=True)
rd = lambda f: list(csv.DictReader(open(os.path.join(RES, f), encoding="utf-8")))

inp = data_io.load_inputs()
S = 65.0; SEC0 = 3.5
summary = {r["scenario"]: r for r in rd("I1_scenario_summary.csv")}
long = rd("I1_scenario_results.csv")
J0 = float(summary["A"]["J_A_cm2_est"]); I0 = float(summary["A"]["I_electrode_kA_est"])
res, eqs, _ = mb.full_balance(inp)
prod0 = inp["wb.ferrochrome_production_baseline"].value

tables = {}
tables["dim_scenario"] = (["ScenarioID", "Scenario", "Definition", "UsedBy", "Order", "Role"],
    [[s, summary[s]["name"], summary[s]["definition"], summary[s]["used_by"], i,
      {"A": "Baseline", "C1": "Selected design", "S-B": "Electrical uprate"}.get(s, "Alternative / interpretation")]
     for i, s in enumerate(summary)])
units = {}
rows = []
for r in long:
    units[r["metric"]] = r["unit"]
    try: v = float(r["value"])
    except ValueError: continue
    rows.append([r["scenario"], r["metric"], v, r["unit"], r["provenance"], r["equation"], r["note"]])
tables["fact_scenario_metrics"] = (["ScenarioID", "Metric", "Value", "Unit", "Provenance", "Equation", "Note"], rows)
tables["dim_metric"] = (["Metric", "Unit", "Module", "IsEstimate"],
    [[m, u, "production" if m.startswith(("production", "SEC", "E_daily", "meets")) else "electrical",
      "Yes" if m.endswith("_est") else "No"] for m, u in units.items()])

# constraints per scenario
crit = []
for s, d in summary.items():
    P = float(d["P_mean_MW"]); prod = float(d["production_tpd"]); aux = (prod / prod0) / 1.10
    for cid, name, val, lim, sense, unit, prov in (
        ("DC-01", "On-load apparent power", float(d["S_on_MVA"]), 65.0, "<=", "MVA", "CALCULATED"),
        ("DC-02", "Power factor", float(d["PF"]), 0.95, "<=", "-", "SUPPLIED limit"),
        ("DC-04", "Electrode current density (est.)", float(d["J_A_cm2_est"]), J0, "<=", "A/cm2", "CALCULATED (estimate)"),
        ("DC-05", "Electrode current (est.)", float(d["I_electrode_kA_est"]), I0, "<=", "kA", "CALCULATED (estimate)"),
        ("DC-06", "Auxiliary utilisation (10 % design margin, A-22)", aux, 0.90, "<=", "fraction", "ASSUMED margin"),
        ("DC-10", "Specific energy", float(d["SEC_MWh_t"]), 3.5, "<=", "MWh/t", "SUPPLIED limit"),
        ("DC-14", "Production", prod, 450.0, ">=", "t/d", "TARGET"),
    ):
        ok = (val <= lim + 1e-9) if sense == "<=" else (val >= lim - 1e-9)
        util = val / lim if sense == "<=" else lim / val
        crit.append([s, cid, name, round(val, 4), lim, sense, unit, round(util, 4), "PASS" if ok else "FAIL", prov])
tables["fact_constraints"] = (["ScenarioID", "CriterionID", "Criterion", "Value", "Limit", "Sense", "Unit", "Utilisation", "Status", "Provenance"], crit)

mbrows = [[r["direction"], r["stream"], float(r["kg_per_t_alloy"]),
           float(r["t_per_day_existing_393.65"]) if r["t_per_day_existing_393.65"] else None,
           float(list(r.values())[4]) if list(r.values())[4] else None]
          for r in rd("I2_mass_balance.csv") if r["direction"] in ("IN", "OUT")]
tables["fact_mass_balance"] = (["Direction", "Stream", "kg_per_t", "t_per_d_existing", "t_per_d_C1"], mbrows)
tables["fact_balance_residuals"] = (["Balance", "Feed_kg_per_t", "Residual_kg_per_t", "Residual_pct_of_feed"],
    [[r["equation"], float(r["feed_kg_per_t"]), float(r["residual_kg_per_t"]), float(r["residual_pct_of_feed"]) / 100] for r in rd("I2_balance_residuals.csv")])
tables["fact_mb_kpi"] = (["KPI", "Value", "Unit", "Provenance", "Note"],
    [[r["kpi"], float(r["value"]), r["unit"], r["provenance"], r["note"]] for r in rd("I2_mass_balance_kpis.csv")])
tables["fact_optimisation"] = (["LF_max", "T_reference", "PF_opt", "LF_opt", "T_opt_C", "Production_tpd"],
    [[float(r["LF_max"]), r["T_reference"], float(r["PF_opt"]), float(r["LF_opt"]), float(r["T_opt_SLSQP_C"]), float(r["production_at_opt_tpd"])]
     for r in rd("I2_optimisation_minT.csv")])
tables["fact_robust"] = (["Case", "T_P50_C", "T_P90_C", "P_at_500C"],
    [[r["case"], float(r["T_for_P50_C"]), float(r["T_for_P90_C"]), float(r["P_at_500C"])] for r in rd("I2_robust_optimisation.csv")])
tables["fact_tornado"] = (["Input", "Key", "Low", "High", "Production_low", "Production_high"],
    [[r["input"], r["key"], float(r["low"]), float(r["high"]), float(r["production_at_low"]), float(r["production_at_high"])] for r in rd("I2_tornado.csv")])
rng = np.random.default_rng(20261127)
dist = {"s": lambda g, n: g.uniform(0.035, 0.070, n), "T": lambda g, n: g.triangular(450, 500, 550, n),
        "LF": lambda g, n: g.triangular(0.95, 0.972, 0.98, n), "PF": lambda g, n: g.triangular(0.93, 0.95, 0.95, n),
        "SEC0": lambda g, n: g.normal(3.5, 0.035, n), "T_ref": lambda g, n: np.full(n, 25.0)}
M, _ = op.monte_carlo(100000, S, SEC0, rng, dist)
cnt, edges = np.histogram(M, bins=np.arange(405, 481, 2.5))
tables["fact_montecarlo_hist"] = (["Bin_low_tpd", "Bin_mid_tpd", "Count", "Share", "MeetsTarget"],
    [[float(edges[i]), float((edges[i] + edges[i + 1]) / 2), int(c), float(c / len(M)), "Yes" if edges[i] >= 450 else "No"] for i, c in enumerate(cnt)])
tables["fact_verification"] = (["Check", "Document", "Quantity", "TeamValue", "ModelValue", "RelDiffPct", "Status", "AuditNote"],
    [[r["check"], r["document"], r["quantity"], float(r["team_value"]), float(r["model_value"]), float(r["rel_diff_pct"]), r["status"], r["basis / audit note"]]
     for r in rd("I1_verification.csv")])
cv = [["I1 electrical", r["metric"], float(r["python"]), float(r["octave"]), float(r["rel_diff"]), r["status"]] for r in rd("I1_crossval.csv")]
cv += [["I2 " + r["block"], r["item"], float(r["python"]), float(r["octave"]), float(r["rel_diff"]), r["status"]] for r in rd("I2_crossval.csv")]
tables["fact_crossval"] = (["Block", "Item", "Python", "MATLAB_Octave", "RelDiff", "Status"], cv)
inputs_rows = list(csv.DictReader(open(os.path.join(ROOT, "model", "inputs", "model_inputs.csv"), encoding="utf-8")))
tables["dim_input_provenance"] = (["Input", "Value", "Unit", "Provenance", "Source"],
    [[r["name"], float(r["value"]), r["unit"], r["provenance"], r["source"]] for r in inputs_rows])

wb = Workbook(); wb.remove(wb.active)
for name, (hdr, rows) in tables.items():
    ws = wb.create_sheet(name[:31]); ws.append(hdr)
    for r in rows: ws.append(r)
    ref = f"A1:{chr(64 + len(hdr))}{len(rows) + 1}"
    t = Table(displayName=name, ref=ref); t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(t)
    for i, h in enumerate(hdr): ws.column_dimensions[chr(65 + i)].width = max(12, min(45, len(h) + 4))
wb.save(os.path.join(PBI, "SAF_PowerBI_Dataset.xlsx"))

# ---------------------------------------------------------------- DAX measures
dax = r"""// ===== SAF engineering dashboard – DAX measures (create in a 'Measures' table) =====
// Relationships: dim_scenario[ScenarioID] 1–* fact_scenario_metrics[ScenarioID]
//                dim_scenario[ScenarioID] 1–* fact_constraints[ScenarioID]
//                dim_metric[Metric]       1–* fact_scenario_metrics[Metric]

Metric Value = SUM ( fact_scenario_metrics[Value] )
Production t/d = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "production_tpd" )
Mean Power MW = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "P_mean_MW" )
On-load Power MW = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "P_on_MW" )
On-load MVA = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "S_on_MVA" )
On-load Loading % = DIVIDE ( [On-load MVA], 65 )
Transformer Headroom MVA = 65 - [On-load MVA]
Electrode Current kA (est.) = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "I_electrode_kA_est" )
Current Density A/cm2 (est.) = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "J_A_cm2_est" )
SEC MWh/t = CALCULATE ( [Metric Value], fact_scenario_metrics[Metric] = "SEC_MWh_t" )
Baseline Production t/d = CALCULATE ( [Production t/d], dim_scenario[ScenarioID] = "A" )
Production Gain t/d = [Production t/d] - [Baseline Production t/d]
Production Gain % = DIVIDE ( [Production Gain t/d], [Baseline Production t/d] )
Gap to 450 t/d = [Production t/d] - 450
Meets 450 = IF ( [Production t/d] >= 450, "Meets 450 t/d", "Below target" )

Criteria Failed = CALCULATE ( COUNTROWS ( fact_constraints ), fact_constraints[Status] = "FAIL" )
Criteria Passed = CALCULATE ( COUNTROWS ( fact_constraints ), fact_constraints[Status] = "PASS" )
Max Utilisation = MAX ( fact_constraints[Utilisation] )
Binding Criterion =
    VAR m = [Max Utilisation]
    RETURN CALCULATE ( FIRSTNONBLANK ( fact_constraints[Criterion], 1 ), fact_constraints[Utilisation] = m )

Cr Recovery % = CALCULATE ( SUM ( fact_mb_kpi[Value] ), fact_mb_kpi[KPI] = "Cr recovery to alloy (reconciled)" ) / 100
Mass Closure % = CALCULATE ( SUM ( fact_mb_kpi[Value] ), fact_mb_kpi[KPI] = "Mass closure" ) / 100
Max Balance Residual % = MAXX ( fact_balance_residuals, ABS ( fact_balance_residuals[Residual_pct_of_feed] ) )

P(>=450 t/d) = DIVIDE ( CALCULATE ( SUM ( fact_montecarlo_hist[Count] ), fact_montecarlo_hist[MeetsTarget] = "Yes" ),
                        SUM ( fact_montecarlo_hist[Count] ) )
Tornado Swing t/d = SUMX ( fact_tornado, ABS ( fact_tornado[Production_high] - fact_tornado[Production_low] ) )

Checks Reproduced % = DIVIDE ( CALCULATE ( COUNTROWS ( fact_verification ), fact_verification[Status] = "REPRODUCED" ),
                               COUNTROWS ( fact_verification ) )
Cross-validation Worst Rel Diff = MAX ( fact_crossval[RelDiff] )
Inputs by Provenance = COUNTROWS ( dim_input_provenance )
"""
open(os.path.join(PBI, "SAF_measures.dax"), "w", encoding="utf-8").write(dax)
theme = {"name": "SAF Engineering", "dataColors": ["#3B6E8F", "#7A1F1F", "#C9A227", "#B9B9B9", "#2E7D32", "#D9822B", "#5B9BD5", "#404040"],
         "background": "#FFFFFF", "foreground": "#222222", "tableAccent": "#3B6E8F",
         "good": "#2E7D32", "neutral": "#C9A227", "bad": "#C62828",
         "textClasses": {"title": {"fontFace": "Segoe UI Semibold", "fontSize": 13}, "label": {"fontFace": "Segoe UI", "fontSize": 10}}}
json.dump(theme, open(os.path.join(PBI, "SAF_theme.json"), "w"), indent=2)

# ---------------------------------------------------------------- page mock-ups (design reference)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
C = {"blue": "#3B6E8F", "red": "#7A1F1F", "gold": "#C9A227", "grey": "#B9B9B9", "green": "#2E7D32", "bad": "#C62828"}


def card(ax, title, value, sub="", color=C["blue"]):
    ax.axis("off"); ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc="#F4F6F8", ec="#D0D5DA", transform=ax.transAxes))
    ax.text(0.06, 0.72, title, fontsize=7.5, color="#555", transform=ax.transAxes)
    ax.text(0.06, 0.30, value, fontsize=11.5, color=color, weight="bold", transform=ax.transAxes)
    ax.text(0.06, 0.08, sub, fontsize=6.5, color="#777", transform=ax.transAxes)


def page(title, subtitle):
    fig = plt.figure(figsize=(13.33, 7.5))
    fig.patches.append(plt.Rectangle((0, 0.93), 1, 0.07, fc="#1F4E78", transform=fig.transFigure, figure=fig))
    fig.text(0.015, 0.955, title, color="white", fontsize=15, weight="bold")
    fig.text(0.985, 0.955, subtitle, color="#DDE6EE", fontsize=8, ha="right")
    fig.text(0.015, 0.012, "Power BI page mock-up rendered from powerbi/SAF_PowerBI_Dataset.xlsx – build in Power BI Desktop per docs/10. "
             "Estimates (I, V, J) rest on Westly C3 calibration (AF-08).", fontsize=6.5, color="#777")
    return fig


A, C1 = summary["A"], summary["C1"]
# Page 1 – overview
fig = page("01  Baseline vs selected design (C1)", "Ferrochrome SAF uprate • 65 MVA • data: supervisor workbook")
vals = [("Mean power", f"{float(A['P_mean_MW']):.2f} → {float(C1['P_mean_MW']):.2f} MW", "PF 0.93→0.95, LF 0.95→0.972"),
        ("Production", f"{float(A['production_tpd']):.0f} → {float(C1['production_tpd']):.0f} t/d", "+16 % (450 t/d target met)"),
        ("Specific energy", f"3.50 → {float(C1['SEC_MWh_t']):.2f} MWh/t", "hot charging ~500 °C"),
        ("On-load loading", f"{float(A['loading_on_pct']):.0f} % → {float(C1['loading_on_pct']):.0f} %", "no on-load headroom (AF-03)"),
        ("Cr recovery", f"{100*res['Cr_recovery']:.1f} %", "reconciled (workbook assumed 78 %)"),
        ("P(≥ 450 t/d)", f"{100*np.mean(M >= 450):.0f} %", "Monte-Carlo – saving not verified")]
for i, (t, v, s_) in enumerate(vals):
    card(fig.add_axes([0.015 + i * 0.164, 0.76, 0.155, 0.15]), t, v, s_,
         C["bad"] if t.startswith("P(") or t.startswith("On-load") else C["blue"])
ax = fig.add_axes([0.05, 0.10, 0.38, 0.56])
order = ["A", "E1", "S-B", "P1", "C1"]
ax.bar(order, [float(summary[s]["production_tpd"]) for s in order], color=[C["grey"], C["blue"], C["blue"], C["gold"], C["red"]])
ax.axhline(450, color=C["bad"], lw=1); ax.text(4.45, 452, "450 t/d", color=C["bad"], fontsize=7, ha="right")
for i, s in enumerate(order): ax.text(i, float(summary[s]["production_tpd"]) + 3, f"{float(summary[s]['production_tpd']):.0f}", ha="center", fontsize=7)
ax.set_ylim(350, 480); ax.set_title("Production by alternative (t/d)", loc="left", fontsize=9)
ax2 = fig.add_axes([0.72, 0.10, 0.26, 0.56])
cr = [r for r in crit if r[0] == "C1"]
ax2.barh([r[1] + " " + r[2][:28] for r in cr], [r[7] for r in cr], color=[C["green"] if r[8] == "PASS" else C["bad"] for r in cr])
ax2.axvline(1.0, color="k", lw=0.8); ax2.set_xlim(0.8, 1.25); ax2.invert_yaxis()
for i, r in enumerate(cr): ax2.text(min(r[7], 1.24), i, f" {r[7]:.2f}", va="center", fontsize=7, ha="right" if r[7] > 1.2 else "left")
ax2.set_title("C1 – utilisation of each acceptance criterion (1.0 = limit)", loc="left", fontsize=9)
fig.savefig(os.path.join(FIG, "PBI_page1_overview.png"), dpi=150); plt.close(fig)

# Page 2 – electrical
fig = page("02  Transformer and electrical loading", "Is there headroom? Which '60 MW'?")
ax = fig.add_axes([0.05, 0.12, 0.42, 0.74])
ids = ["A", "S-N55", "E1", "S-B", "S-N60", "S-O60", "C1"]
v = [float(summary[s]["S_on_MVA"]) for s in ids]
ax.barh(ids, v, color=[C["bad"] if x > 64 else C["blue"] for x in v]); ax.axvline(65, color="k"); ax.set_xlim(55, 66); ax.invert_yaxis()
for i, x in enumerate(v): ax.text(x - 0.15, i, f"{x:.2f}", ha="right", va="center", color="white", fontsize=7)
ax.set_title("On-load apparent power vs 65 MVA rating (MVA)", loc="left", fontsize=9)
ax = fig.add_axes([0.55, 0.55, 0.42, 0.31])
ax.bar(ids, [float(summary[s]["J_A_cm2_est"]) for s in ids], color=C["gold"]); ax.axhline(J0, color=C["bad"], lw=1)
ax.set_ylim(6.0, 7.0); ax.set_title("Electrode current density, est. (A/cm²) – DC-04 line = existing", loc="left", fontsize=9)
ax = fig.add_axes([0.55, 0.12, 0.42, 0.33]); ax.axis("off")
tbl = [[s, f"{float(summary[s]['PF']):.3f}", f"{float(summary[s]['LF']):.3f}", f"{float(summary[s]['P_mean_MW']):.2f}", f"{float(summary[s]['P_on_MW']):.2f}",
        f"{float(summary[s]['I_electrode_kA_est']):.1f}", f"{float(summary[s]['V_secondary_LL_V_est']):.0f}"] for s in ids]
t = ax.table(cellText=tbl, colLabels=["ID", "PF", "LF", "P_mean", "P_on", "I_e est.", "V_LL est."], loc="center", cellLoc="center")
t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.25)
fig.savefig(os.path.join(FIG, "PBI_page2_electrical.png"), dpi=150); plt.close(fig)

# Page 3 – mass balance
fig = page("03  Mass balance and metallurgy", "Reconciled from measured analyses • closure −0.4 %")
for i, (t_, v_, s_) in enumerate((("Ore", f"{res['m_ore']/1000:.2f} t/t", "80 % pellets / 20 % lumpy"), ("Reductant (dry)", f"{res['m_reductant_dry']/1000:.3f} t/t", "10 % coke / 90 % anthracite"),
                                   ("Slag", f"{res['m_slag']/1000:.2f} t/t", ""), ("Cr recovery", f"{100*res['Cr_recovery']:.1f} %", "vs 78 % assumed"),
                                   ("Off-gas", f"{res['gas_Nm3']:.0f} Nm³/t", "CO + CO2 + H2O"))):
    card(fig.add_axes([0.015 + i * 0.197, 0.76, 0.185, 0.15]), t_, v_, s_)
ax = fig.add_axes([0.20, 0.10, 0.30, 0.56])
mbs = [r for r in mbrows]
ins = [r for r in mbs if r[0] == "IN"]; outs = [r for r in mbs if r[0] == "OUT"]
ax.barh([r[1].split("(")[0].strip()[:24] for r in ins + outs], [r[2] for r in ins + outs], color=[C["blue"]] * len(ins) + [C["red"]] * len(outs))
ax.invert_yaxis(); ax.set_title("Streams per tonne alloy (kg) – blue in, red out", loc="left", fontsize=9)
ax = fig.add_axes([0.57, 0.10, 0.40, 0.56])
rr_ = tables["fact_balance_residuals"][1]
ax.bar([r[0] for r in rr_], [100 * r[3] for r in rr_], color=C["blue"]); ax.axhline(0, color="k", lw=0.6); ax.set_ylim(-4, 4)
ax.set_title("Balance residuals (% of species feed)", loc="left", fontsize=9)
fig.savefig(os.path.join(FIG, "PBI_page3_massbalance.png"), dpi=150); plt.close(fig)

# Page 4 – optimisation & uncertainty
fig = page("04  Optimisation and robustness", "Minimum preheat for 450 t/d • Monte-Carlo • tornado")
ax = fig.add_axes([0.05, 0.12, 0.27, 0.74])
o = [r for r in tables["fact_optimisation"][1] if r[1].startswith("ambient")]
ax.plot([r[0] for r in o], [r[4] for r in o], "o-", color=C["red"]); ax.axhline(500, color=C["gold"], ls="--", lw=1)
ax.set_xlabel("Achievable load factor"); ax.set_title("T* for 450 t/d at PF 0.95 (°C)", loc="left", fontsize=9)
ax = fig.add_axes([0.38, 0.12, 0.27, 0.74])
h = tables["fact_montecarlo_hist"][1]
ax.bar([r[1] for r in h], [r[2] for r in h], width=2.3, color=[C["green"] if r[4] == "Yes" else C["grey"] for r in h])
ax.set_title(f"C1 production distribution – P(≥450) = {100*np.mean(M >= 450):.0f} %", loc="left", fontsize=9); ax.set_xlabel("t/d")
ax = fig.add_axes([0.80, 0.12, 0.18, 0.74])
tor = tables["fact_tornado"][1]
for i, r in enumerate(tor):
    ax.barh(i, r[4] - 454.8, left=454.8, color=C["grey"]); ax.barh(i, r[5] - 454.8, left=454.8, color=C["blue"])
ax.set_yticks(range(len(tor))); ax.set_yticklabels([r[1] for r in tor]); ax.invert_yaxis(); ax.axvline(450, color=C["bad"])
ax.set_title("Tornado (t/d)", loc="left", fontsize=9)
fig.savefig(os.path.join(FIG, "PBI_page4_optimisation.png"), dpi=150); plt.close(fig)

# Page 5 – verification & provenance
fig = page("05  Model verification and data provenance", "How much rests on assumptions? Do Python and MATLAB agree?")
ver = tables["fact_verification"][1]
card(fig.add_axes([0.015, 0.76, 0.23, 0.15]), "Team numbers reproduced", f"{sum(r[6]=='REPRODUCED' for r in ver)}/{len(ver)}", "differences = audit findings")
card(fig.add_axes([0.26, 0.76, 0.23, 0.15]), "Python vs MATLAB/Octave", f"{sum(r[5]=='PASS' for r in cv)}/{len(cv)} pass", f"worst {max(r[4] for r in cv):.0e}")
prov = {}
for r in inputs_rows: prov[r["provenance"]] = prov.get(r["provenance"], 0) + 1
card(fig.add_axes([0.505, 0.76, 0.23, 0.15]), "Inputs measured / supplied", f"{prov.get('MEASURED',0)+prov.get('SUPPLIED',0)}/{len(inputs_rows)}", "rest: literature, assumed, targets")
ax = fig.add_axes([0.12, 0.10, 0.30, 0.56])
ax.barh(list(prov), list(prov.values()), color=C["blue"]); ax.set_title("Inputs by provenance", loc="left", fontsize=9)
ax = fig.add_axes([0.52, 0.10, 0.46, 0.56]); ax.axis("off")
diff = [[r[0], r[2][:30], f"{r[3]:g}", f"{r[4]:.4g}", r[7].split(":")[0][:8]] for r in ver if r[6] != "REPRODUCED"]
t = ax.table(cellText=diff, colLabels=["Check", "Quantity", "Team", "Model", "Finding"], loc="upper center", cellLoc="left",
             colWidths=[0.10, 0.50, 0.13, 0.13, 0.14])
t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.4); ax.set_title("Team numbers that differ – all explained", loc="left", fontsize=9)
fig.savefig(os.path.join(FIG, "PBI_page5_verification.png"), dpi=150); plt.close(fig)
print("Power BI pack written:", ", ".join(sorted(os.listdir(PBI))))
