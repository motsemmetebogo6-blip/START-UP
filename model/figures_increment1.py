"""
figures_increment1.py – publication-quality figures for Increment 1 (300 dpi PNG + SVG).
Each figure answers one engineering question; scenario values come from results/model/*.csv.
  F1  Operating envelope: which PF/LF combinations give 60 MW mean on 65 MVA?
  F2  On-load transformer loading by scenario: is there headroom? (AF-03)
  F3  Electrode current density vs PF for the two PF-raising routes (AF-10, DC-04)
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, electrical as el   # noqa: E402

ROOT = data_io.ROOT
FIG = os.path.join(ROOT, "report", "figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10,
                     "axes.labelsize": 9, "legend.fontsize": 8, "figure.dpi": 100})
NOTE = "Provenance: S, PF, LF – data workbook; electrode current – Westly estimate (C3 = 8.33, A-18). Model: safmodel I1."


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(FIG, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def scen():
    return {r["scenario"]: r for r in csv.DictReader(open(os.path.join(ROOT, "results", "model", "I1_scenario_summary.csv")))}


def f1_envelope(sc):
    S = 65.0
    pf = np.linspace(0.85, 0.99, 300); lf = np.linspace(0.90, 1.00, 300)
    PF, LF = np.meshgrid(pf, lf); P = S * PF * LF
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    cs = ax.contour(PF, LF, P, levels=[52, 54, 56, 58, 62], colors="0.6", linewidths=0.7)
    ax.clabel(cs, fmt="%d MW", fontsize=7)
    c60 = ax.contour(PF, LF, P, levels=[60], colors="C3", linewidths=1.8)
    ax.clabel(c60, fmt="60 MW mean", fontsize=8)
    ax.axvspan(0.95, 0.99, color="0.85", alpha=0.6)
    ax.text(0.952, 0.905, "PF > 0.95\nnot accepted\n(supervisor)", fontsize=7, color="0.3")
    for sid, mk in (("A", "o"), ("E1", "s"), ("S-B", "D"), ("S-N60", "^")):
        r = sc[sid]
        ax.plot(float(r["PF"]), float(r["LF"]), mk, color="C0", ms=6)
        ax.annotate(f"{sid}\n{float(r['P_mean_MW']):.2f} MW", (float(r["PF"]), float(r["LF"])), xytext=(6, -14),
                    textcoords="offset points", fontsize=7)
    ax.set_xlabel("Power factor PF (–)"); ax.set_ylabel("Load factor LF (–)")
    ax.set_title("Mean active power on a 65 MVA rating:  P_mean = 65 · PF · LF")
    ax.set_xlim(0.85, 0.99); ax.set_ylim(0.90, 1.0); ax.grid(alpha=0.25)
    fig.text(0.01, -0.02, NOTE, fontsize=6, color="0.4")
    save(fig, "F1_operating_envelope")


def f2_loading(sc):
    order = ["A", "S-N55", "E1", "S-B", "S-N60", "S-O60", "C1"]
    short = {"A": "existing (workbook)", "S-N55": "55 MW continuous", "E1": "PF 0.95, LF 0.95",
             "S-B": "60 MW mean (PF 0.95, LF 0.972)", "S-N60": "60 MW continuous (PF 0.93)",
             "S-O60": "60 MW on load (PF 0.93)", "C1": "C1 = S-B + hot charging"}
    labels = [f"{s}  {short[s]}" for s in order]
    S_on = [float(sc[s]["S_on_MVA"]) for s in order]
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    y = np.arange(len(order))[::-1]
    ax.barh(y, S_on, color=["C0" if v < 64.0 else "C1" for v in S_on], height=0.6)
    ax.axvline(65, color="C3", lw=1.2); ax.text(65.1, y[0] + 0.3, "65 MVA rating", color="C3", fontsize=7)
    for yi, v in zip(y, S_on):
        ax.text(v - 0.2, yi, f"{v:.2f} MVA ({100*v/65:.1f} %)", va="center", ha="right", fontsize=7, color="white")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlim(50, 67); ax.set_xlabel("On-load apparent power S_on (MVA)")
    ax.set_title("On-load transformer loading: every 60 MW interpretation leaves < 1 % headroom")
    fig.text(0.01, -0.03, NOTE, fontsize=6, color="0.4")
    save(fig, "F2_transformer_loading")


def f3_routes():
    PF0 = 0.93
    J0 = el.current_density(el.electrode_current_kA(65 * PF0, 8.33), 1.55)
    pf = np.linspace(0.93, 0.95, 50)
    jR = [J0 * el.pf_route_current_ratio(PF0, p, "R") for p in pf]
    jX = [J0 * el.pf_route_current_ratio(PF0, p, "X") for p in pf]
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(pf, jR, color="C2", label="Route R: raise operating resistance (PCD, burden); X fixed")
    ax.plot(pf, jX, color="C1", label="Route X: lower short-network reactance; R fixed")
    ax.axhline(J0, color="C3", ls="--", lw=1)
    ax.text(0.9405, J0 - 0.045, f"DC-04 limit: existing J ≈ {J0:.2f} A/cm² (estimate)", color="C3", fontsize=7)
    ax.set_xlabel("Power factor at constant S = 65 MVA (–)"); ax.set_ylabel("Electrode current density J (A/cm²)")
    ax.set_title("Electrode loading depends on HOW the power factor is raised")
    ax.legend(loc="lower left"); ax.grid(alpha=0.25)
    fig.text(0.01, -0.09, "Ratios I1/I0 are independent of the C3 calibration (Route R: √(sinφ1/sinφ0); Route X: √(PF1/PF0)). " + NOTE,
             fontsize=6, color="0.4", wrap=True)
    save(fig, "F3_pf_route_current_density")


if __name__ == "__main__":
    s = scen(); f1_envelope(s); f2_loading(s); f3_routes()
    print("Figures written to report/figures/: F1_operating_envelope, F2_transformer_loading, F3_pf_route_current_density")
