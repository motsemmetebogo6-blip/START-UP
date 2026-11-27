"""crossval_I1.py – compares Python (I1_python_numeric.csv) with MATLAB/Octave (I1_octave_numeric.csv)."""
import csv, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.join(ROOT, "results", "model")
py = {r["idx"]: r for r in csv.DictReader(open(os.path.join(R, "I1_python_numeric.csv")))}
oc = {r["idx"]: r for r in csv.DictReader(open(os.path.join(R, "I1_octave_numeric.csv")))}
TOL = 1e-6
rows, worst = [], 0.0
for idx, p in py.items():
    o = oc[idx]
    for k, v in p.items():
        if k == "idx": continue
        a, b = float(v), float(o[k]); rel = abs(a - b) / max(abs(a), 1e-12)
        worst = max(worst, rel)
        rows.append([idx, k, a, b, rel, "PASS" if rel <= TOL else "FAIL"])
with open(os.path.join(R, "I1_crossval.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["scenario_idx", "metric", "python", "octave", "rel_diff", "status"]); w.writerows(rows)
n_fail = sum(r[5] == "FAIL" for r in rows)
print(f"Cross-validation: {len(rows)} comparisons, {n_fail} failures, worst relative difference {worst:.2e}")
sys.exit(1 if n_fail else 0)
