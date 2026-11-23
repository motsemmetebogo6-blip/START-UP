"""
04_figures_and_matrix.py – Figure 4.1 (system boundary) and the Chapter 12 weighted
decision matrix (preliminary scores, to be revised with Chapter 15 cost data).
Outputs: results/04_system_boundary.png, results/12_decision_matrix.csv
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# ---------------------------------------------------------------- Figure 4.1
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 46); ax.axis("off")
def box(x, y, w, h, text, fc="#E8EEF7"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=fc, ec="#2F4F6F", lw=1))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8)
def arrow(x1, y1, x2, y2, text="", dy=1.2):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color="#2F4F6F"))
    if text: ax.text((x1+x2)/2, (y1+y2)/2 + dy, text, ha="center", fontsize=7, color="#2F4F6F")
box(1, 20, 11, 7, "Grid / HV\nsupply")
box(18, 20, 13, 7, "Furnace\ntransformers\n3 × 21.7 MVA")
box(37, 20, 12, 7, "Short network\n(busbars,\nflexibles)")
box(55, 20, 12, 7, "Söderberg\nelectrodes\n(3 × 1.55 m)")
box(73, 15, 17, 17, "Closed SAF\n(burden, slag,\nalloy)", fc="#DCEFE9")
arrow(12, 23.5, 18, 23.5); ax.text(8.5, 28.5, "65 MVA", fontsize=7, color="#2F4F6F")
arrow(31, 23.5, 37, 23.5, "≈ 293 V")
arrow(49, 23.5, 55, 23.5, "≈ 128 kA")
arrow(67, 23.5, 73, 23.5)
box(73, 36.5, 17, 6.5, "Charge\n(pellets, lumpy ore, fluxes,\ncoke, anthracite)", fc="#FFF4DC")
arrow(81.5, 36.5, 81.5, 32)
box(92, 26, 7.5, 5, "Off-gas\n(CO-rich)", fc="#FFF4DC"); arrow(90, 28, 92, 28.5)
box(92, 17, 7.5, 5, "Alloy\n393.65 t/d", fc="#FFF4DC"); arrow(90, 21, 92, 19.5)
box(92, 8, 7.5, 5, "Slag", fc="#FFF4DC"); arrow(90, 16, 93.5, 13)
box(73, 4, 17, 5, "Cooling water\n(heat losses)", fc="#FFF4DC"); arrow(81.5, 15, 81.5, 9)
ax.add_patch(plt.Rectangle((15.5, 2), 75.5, 42.5, fill=False, ls="--", ec="#B03030", lw=1.2))
ax.text(16.5, 43.2, "Furnace electrical boundary (study boundary)", color="#B03030", fontsize=8)
ax.text(1, 14, "Upstream sintering\nplant excluded", fontsize=7, color="grey")
fig.tight_layout(); fig.savefig(os.path.join(ROOT, "results", "04_system_boundary.png"), dpi=160)

# ---------------------------------------------------------------- Decision matrix
criteria = [("Production capability against 450 t/d", 25), ("Compliance with 60 MW brief", 15),
            ("Capital cost (lower is better)", 20), ("Technical risk (lower is better)", 15),
            ("Impact on existing infrastructure", 15), ("Technology maturity", 10)]
scores = {"E2": [2, 5, 4, 3, 4, 5], "P1": [3, 1, 3, 3, 3, 4], "P2": [5, 1, 1, 2, 1, 3], "C1": [4, 5, 3, 3, 3, 4]}
assert sum(w for _, w in criteria) == 100
def total(alt, w=None):
    w = w or [c[1] for c in criteria]
    return sum(s * wi for s, wi in zip(scores[alt], w)) / 100
rows = [[c, w] + [scores[a][i] for a in scores] for i, (c, w) in enumerate(criteria)]
rows.append(["Weighted score (out of 5)", 100] + [round(total(a), 2) for a in scores])
# sensitivity: capital cost weight 20 -> 35 (taken equally from production and brief)
w_cap = [c[1] for c in criteria]; w_cap[0] -= 8; w_cap[1] -= 7; w_cap[2] += 15
rows.append(["Sensitivity: capital-cost weight 35 %", 100] + [round(total(a, w_cap), 2) for a in scores])
w_eq = [100/6]*6
rows.append(["Sensitivity: equal weights", 100] + [round(total(a, w_eq), 2) for a in scores])
with open(os.path.join(ROOT, "results", "12_decision_matrix.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["Criterion", "Weight_%"] + list(scores)); wr.writerows(rows)
for r in rows: print(r)
