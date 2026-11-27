"""crossval_I2.py – Python vs MATLAB/Octave for the mass balance and the optimum temperature."""
import csv, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.join(ROOT, "results", "model")
py = next(csv.DictReader(open(os.path.join(R, "I2_python_massbalance.csv"))))
oc = next(csv.DictReader(open(os.path.join(R, "I2_octave_massbalance.csv"))))
rows = []
for k in py:
    a, b = float(py[k]), float(oc[k]); rel = abs(a - b) / abs(a)
    rows.append(["mass balance", k, a, b, rel, "PASS" if rel <= 1e-6 else "FAIL"])
opt_py = list(csv.DictReader(open(os.path.join(R, "I2_optimisation_minT.csv"))))
opt_oc = list(csv.DictReader(open(os.path.join(R, "I2_octave_optimum.csv"))))
for o in opt_oc:
    for ref, col in (("project rule (0 C ref)", "T_ref0"), ("ambient ref (AF-14)", "T_ref25")):
        p = next(r for r in opt_py if abs(float(r["LF_max"]) - float(o["LF_max"])) < 1e-9 and r["T_reference"] == ref)
        a, b = float(p["T_opt_SLSQP_C"]), float(o[col]); rel = abs(a - b) / abs(b)
        rows.append(["optimum T (SLSQP vs closed form)", f"LF_max {o['LF_max']} {ref}", a, b, rel, "PASS" if rel <= 1e-3 else "FAIL"])
with open(os.path.join(R, "I2_crossval.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["block", "item", "python", "octave", "rel_diff", "status"]); w.writerows(rows)
nf = sum(r[5] == "FAIL" for r in rows)
print(f"I2 cross-validation: {len(rows)} comparisons, {nf} failures, worst {max(r[4] for r in rows):.2e}")
sys.exit(1 if nf else 0)
