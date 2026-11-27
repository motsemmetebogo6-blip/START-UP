"""export_dashboard_data.py: numeric CSV and name files for the MATLAB/Octave dashboard (matlab/saf_dashboard.m)."""
import csv, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "results", "model"); D = os.path.join(ROOT, "matlab", "dashboard_data"); os.makedirs(D, exist_ok=True)
rd = lambda f: list(csv.DictReader(open(os.path.join(R, f))))

def save(name, arr, names=None):
    np.savetxt(os.path.join(D, name + ".csv"), np.asarray(arr, float), delimiter=",", fmt="%.10g")
    if names is not None:
        open(os.path.join(D, name + "_names.txt"), "w").write("\n".join(names) + "\n")

sc = rd("I1_scenario_summary.csv")
save("scen", [[float(r["P_mean_MW"]), float(r["S_on_MVA"]), float(r["loading_on_pct"]), float(r["J_A_cm2_est"]), float(r["SEC_MWh_t"]), float(r["production_tpd"])] for r in sc], [r["scenario"] for r in sc])
mb = [r for r in rd("I2_mass_balance.csv") if r["direction"] in ("IN", "OUT")]
short = {"Ore blend (80 % pellets / 20 % lumpy)": "Ore", "Reductant, dry (10 % coke / 90 % anthracite)": "Reductant", "Reductant moisture": "Moisture", "Quartz": "Quartz", "Limestone": "Limestone",
         "Alloy (HC FeCr)": "Alloy", "Slag": "Slag", "CO (reduction gas)": "CO", "CO2 (limestone calcination)": "CO2", "H2O (reductant moisture)": "H2O", "Volatile matter": "Volatiles"}
save("mb", [[float(r["kg_per_t_alloy"]), 1.0 if r["direction"] == "IN" else 2.0] for r in mb], [short.get(r["stream"], r["stream"]) for r in mb])
opt = [r for r in rd("I2_optimisation_minT.csv") if "ambient" in r["T_reference"]]
save("opt", [[float(r["LF_max"]), float(r["T_opt_SLSQP_C"])] for r in opt])
tor = rd("CH16_npv_tornado.csv")
save("tornado", [[float(r["NPV_at_low_RM"]), float(r["NPV_at_high_RM"])] for r in tor], [r["input"].split(" (")[0] for r in tor])
ax = list(csv.DictReader(open(os.path.join(ROOT, "furnace_cad", "thermal_results", "axial_profile.csv"))))
save("axial", [[float(r["z_m"]), float(r["T_axis_C"]) if r["T_axis_C"] else -1, float(r["T_surface_C"]) if r["T_surface_C"] else -1] for r in ax])
kp = {r["quantity"]: r for r in rd("CH16_base_case.csv")}
mbk = {r["kpi"]: r for r in rd("I2_mass_balance_kpis.csv")}
import json
th = json.load(open(os.path.join(ROOT, "furnace_cad", "thermal_results", "thermal_summary.json")))["metrics"]
save("kpi", [float(sc[-1]["production_tpd"]), float(mbk["Cr recovery to alloy (reconciled)"]["value"]), float(kp["NPV (15 y, 12 %)"]["updated base (reconciled, conservative)"]),
             float(kp["IRR"]["updated base (reconciled, conservative)"]), th["Tmax"]])
print("dashboard data written to", D)
