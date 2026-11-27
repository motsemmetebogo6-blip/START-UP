"""render_dashboard_preview.py: matplotlib rendering of the same six panels that matlab/saf_dashboard.m draws (for the report and slides)."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "matlab", "dashboard_data")
ld = lambda f: np.loadtxt(os.path.join(D, f + ".csv"), delimiter=",", ndmin=2)
nm = lambda f: [l.strip() for l in open(os.path.join(D, f + "_names.txt")) if l.strip()]
scen, sn, mb, mn, opt, tor, tn, ax, kpi = ld("scen"), nm("scen"), ld("mb"), nm("mb"), ld("opt"), ld("tornado"), nm("tornado"), ld("axial"), ld("kpi").ravel()
blue, orange, grey = "#005696", "#d9541e", "#8c8c8c"
fig, A = plt.subplots(2, 3, figsize=(15, 8.6)); A = A.ravel()
A[0].bar(sn, scen[:, 5], color=blue); A[0].axhline(450, color="r", ls="--"); A[0].set_ylim(350, 480); A[0].set_ylabel("t/d"); A[0].set_title("Production by scenario (target 450 t/d)")
A[1].bar(sn, scen[:, 2], color=orange); A[1].axhline(100, color="k", ls="--"); A[1].set_ylim(85, 105); A[1].set_ylabel("% of 65 MVA"); A[1].set_title("On-load transformer loading")
y = np.arange(len(mn)); A[2].barh(y, mb[:, 0], color=[blue if v == 1 else grey for v in mb[:, 1]]); A[2].set_yticks(y); A[2].set_yticklabels(mn); A[2].invert_yaxis(); A[2].set_xlabel("kg per t alloy"); A[2].set_title("Mass balance (blue = inputs)")
A[3].plot(opt[:, 0], opt[:, 1], "o-", color=blue); A[3].axhline(500, color="r", ls="--"); A[3].set_xlabel("Achievable load factor"); A[3].set_ylabel("Minimum preheat (C)"); A[3].set_title("Optimisation: least preheat for 450 t/d")
base = kpi[2]; order = np.argsort(np.abs(tor[:, 1] - tor[:, 0]))
for k, i in enumerate(order):
    lo, hi = sorted(tor[i]); A[4].barh(k, hi - base, left=base, color=blue); A[4].barh(k, lo - base, left=base, color=grey)
A[4].set_yticks(range(len(order))); A[4].set_yticklabels([tn[i] for i in order], fontsize=7); A[4].axvline(base, color="k", lw=0.8); A[4].set_xlabel("NPV (R million)"); A[4].set_title("Tornado: effect on NPV")
m = ax[:, 1] > 0; m2 = ax[:, 2] > 0; A[5].plot(ax[m, 1], ax[m, 0], "r-", label="axis"); A[5].plot(ax[m2, 2], ax[m2, 0], "b-", label="surface"); A[5].set_xlabel("Temperature (C)"); A[5].set_ylabel("z (m)"); A[5].legend(); A[5].set_title("Electrode axial temperature (assumed inputs)")
for a in A: a.grid(alpha=0.3)
fig.suptitle(f"SAF uprate dashboard   |   C1 production {kpi[0]:.1f} t/d   |   Cr recovery {kpi[1]:.1f} %   |   NPV R{kpi[2]:.0f} M   |   IRR {kpi[3]:.1f} %   |   electrode Tmax {kpi[4]:.0f} C (assumed inputs)", fontsize=11, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
out = os.path.join(ROOT, "report", "figures", "MATLAB_dashboard_preview.png"); fig.savefig(out, dpi=200); print(out)
