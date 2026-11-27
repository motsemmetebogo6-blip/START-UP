"""
run_increment1.py – Increment 1: electrical + production model, scenario evaluation,
automated verification of every team calculation, exports for Octave/MATLAB cross-validation.

Run from the repository root:   python3 model/run_increment1.py
Outputs (results/model/):
  I1_scenario_results.csv   long format (scenario, metric, value, unit, provenance, equation, note)
  I1_scenario_summary.csv   wide summary table for the report
  I1_pf_route_comparison.csv
  I1_verification.csv       every team number recalculated, with status
  ../../model/inputs/model_inputs.csv, octave_scenarios.csv
"""
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safmodel import data_io, electrical as el, production as pr, scenarios as scn   # noqa: E402
from safmodel.provenance import RECORD_HEADER                                         # noqa: E402

ROOT = data_io.ROOT
OUT = os.path.join(ROOT, "results", "model")
os.makedirs(OUT, exist_ok=True)


def write(name, header, rows):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    return p


def main():
    inp = data_io.load_inputs()
    data_io.write_inputs_csv(inp)
    S = inp["wb.transformer_capacity"].value
    PF0, LF0 = inp["wb.power_factor"].value, inp["wb.load_factor"].value
    SEC0 = inp["wb.specific_energy_baseline"].value
    C3 = inp["lit.westly_C3"].value; D = inp["lit.electrode_diameter_m"].value

    # ---------------------------------------------------------------- scenarios
    scs = scn.build_scenarios(inp)
    allrecs, summary = [], []
    keys = ["P_mean_MW", "P_on_MW", "S_on_MVA", "loading_on_pct", "Q_on_Mvar", "RX_ratio",
            "I_electrode_kA_est", "V_secondary_LL_V_est", "J_A_cm2_est", "SEC_MWh_t", "production_tpd",
            "meets_450_tpd"]
    for sc in scs:
        Pm, recs = scn.evaluate(sc, inp)
        allrecs += recs
        d = {r.metric: r.value for r in recs}
        summary.append([sc.sid, sc.name, sc.PF, sc.LF, sc.definition, sc.used_by] + [round(d[k], 4) for k in keys])
    write("I1_scenario_results.csv", RECORD_HEADER, [r.row() for r in allrecs])
    write("I1_scenario_summary.csv", ["scenario", "name", "PF", "LF", "definition", "used_by"] + keys, summary)

    # ---------------------------------------------------------------- PF-raising routes (AF-10)
    rows = []
    J0 = el.current_density(el.electrode_current_kA(S * PF0, C3), D)
    for pf1 in (0.93, 0.935, 0.94, 0.945, 0.95):
        for route in ("R", "X"):
            ratio = el.pf_route_current_ratio(PF0, pf1, route)
            rows.append([route, pf1, round(ratio, 5), round(J0 * ratio, 4), round(100 * (ratio - 1), 3),
                         "PASS" if ratio <= 1 + 1e-12 else "EXCEEDS existing J (DC-04)"])
    write("I1_pf_route_comparison.csv",
          ["route", "PF", "I_ratio_vs_existing", "J_A_cm2_est", "J_change_pct", "DC-04"], rows)

    # ---------------------------------------------------------------- verification of team numbers
    V = []
    def chk(cid, doc, desc, team, model, tol=0.005, basis="OK"):
        rel = abs(model - team) / abs(team) if team else abs(model)
        status = "REPRODUCED" if rel <= tol else "DIFFERS"
        V.append([cid, doc, desc, team, round(model, 4), round(100 * rel, 3), tol * 100, status, basis])

    Pmean0 = S * PF0 * LF0
    # Ngesi Ch. 9 (arithmetic reproduced; basis disputed AF-01/02)
    chk("N-01", "Ngesi Ch9", "S at 55 MW, PF 0.93 (MVA)", 59.14, 55 / PF0, basis="AF-02: 55 MW continuous not the workbook baseline")
    chk("N-02", "Ngesi Ch9", "Loading at 55 MW (%)", 90.98, 100 * 55 / PF0 / S)
    chk("N-03", "Ngesi Ch9", "S at 60 MW, PF 0.93 (MVA)", 64.52, 60 / PF0)
    chk("N-04", "Ngesi Ch9", "Loading at 60 MW (%)", 99.26, 100 * 60 / PF0 / S)
    chk("N-05", "Ngesi Ch9", "'95 % loading ceiling' P (MW)", 57.43, S * PF0 * 0.95, basis="AF-01: 0.95 is a load (time) factor, not a loading cap")
    chk("N-06", "Ngesi Ch9", "PF required for 60 MW at '95 % loading'", 0.972, 60 / (S * 0.95), basis="AF-01: under workbook meaning this is PF needed with LF 0.95")
    chk("N-07", "Ngesi Ch9", "Rating required at PF 0.93 & 95 % (MVA)", 67.91, 60 / (PF0 * 0.95), basis="AF-01")
    chk("N-08", "Ngesi Ch9", "Daily energy 55 / 60 MW (MWh/d) – 60 MW", 1440, pr.daily_energy_MWh(60))
    chk("N-09", "Ngesi Ch9", "Production at 55 MW, 3.5 (t/d)", 377.14, pr.production_tpd(55, SEC0), basis="AF-02: actual baseline is 393.65 t/d")
    chk("N-10", "Ngesi Ch9", "Production at 60 MW, 3.5 (t/d)", 411.43, pr.production_tpd(60, SEC0))
    chk("N-11", "Ngesi Ch9", "SEC for 450 t/d at 60 MW", 3.20, pr.sec_required(60, 450))
    chk("N-12", "Ngesi Ch9", "SEC for 480 t/d at 60 MW", 3.00, pr.sec_required(60, 480))
    chk("N-13", "Ngesi Ch9", "Production at 57.43 MW and 2.41 (t/d)", 571.7, pr.production_tpd(Pmean0, 2.41))
    # Jeff Ch. 2 / Tebogo Ch. 7 / Ch. 12
    chk("J-01", "Jeff Ch2/Ch7", "Mean power (MW)", 57.43, Pmean0)
    chk("J-02", "Ch7", "On-load power (MW)", 60.45, S * PF0)
    chk("J-03", "Ch7", "On-load reactive power (Mvar)", 23.89, S * math.sqrt(1 - PF0 ** 2))
    chk("J-04", "Ch7", "R/X", 2.53, el.rx_ratio(PF0))
    chk("J-05", "Jeff Ch2/Ch7", "Power for 450 t/d at 3.5 (MW)", 65.6, pr.power_required(450, SEC0))
    chk("J-06", "Ch7", "Production from energy (t/d)", 393.8, pr.production_tpd(Pmean0, SEC0))
    chk("J-07", "Ch7", "Electrode current est. (kA)", 128.0, el.electrode_current_kA(S * PF0, C3), tol=0.01)
    chk("J-08", "Ch7", "Secondary voltage est. (V)", 293, el.secondary_voltage_V(S, el.electrode_current_kA(S * PF0, C3)), tol=0.01)
    chk("J-09", "Ch7", "Current density est. (A/cm2)", 6.8, el.current_density(el.electrode_current_kA(S * PF0, C3), D), tol=0.01)
    chk("T-01", "Ch12", "C1 production (t/d) – project rule (ref 0 C)", 457.1, pr.production_tpd(60, pr.hot_charge_sec(SEC0, 0.07, 500)))
    chk("T-02", "Ch12", "C1 production if preheat measured from 25 C (t/d)", 457.1, pr.production_tpd(60, pr.hot_charge_sec(SEC0, 0.07, 500, 25)),
        basis="AF-14: ambient reference lowers C1 to ~454.6 t/d")
    chk("T-03", "Ch12", "R/X increase PF 0.93 -> 0.95 (%)", 20.2, 100 * (el.rx_ratio(0.95) / el.rx_ratio(PF0) - 1), tol=0.01)
    chk("T-04", "Ch12", "LF needed for 60 MW at PF 0.95", 0.972, el.pf_lf_required(60, S, PF=0.95))
    # Sibandze Ch. 14 / 15
    chk("S-01", "Sibandze Ch14", "S at 60 MW and PF 0.95 (MVA)", 63.2, 60 / 0.95,
        basis="AF-03: uses MEAN power; on-load S under C1 = 64.98 MVA (100 %)")
    chk("S-02", "Sibandze Ch14", "C1 on-load S (MVA) – model", 63.2, (60 / 0.972) / 0.95, tol=0.005,
        basis="AF-03: model value is the on-load apparent power")
    chk("S-03", "Sibandze Ch14", "S at 60 MW and PF 0.93 (MVA)", 64.5, 60 / PF0)
    chk("S-04", "Sibandze Ch14", "Electrode current at 60 MW (kA)", 128.0, el.electrode_current_kA(60.45, C3), tol=0.01,
        basis="at C1 on-load (61.73 MW) the estimate is 130.1 kA")
    chk("S-05", "Sibandze Ch14", "Ore duty at 457 t/d (t/d), 2.13 t/t", 975, 457.1 * 2.13, tol=0.01, basis="AF-05: 2.13 is an estimate, not measured")
    chk("S-06", "Sibandze Ch14", "Reductant duty (t/d), 0.433 t/t", 198, 457.1 * 0.433, tol=0.01, basis="0.433 t/t not traceable (mass balance not received)")
    chk("S-07", "Sibandze Ch14", "Slag duty (t/d) vs MgO tracer 1.151 t/t", 530, 457.1 * 1.151, tol=0.01)
    dt = 457.1 - inp["wb.ferrochrome_production_baseline"].value
    chk("S-08", "Sibandze Ch15", "Production gain (t/d)", 63.3, dt, tol=0.005)
    rev = 23105 * 1500 * 17.42 / 1e6
    chk("S-09", "Sibandze Ch15", "Incremental revenue (R M/yr)", 604, rev)
    costs = 37.1 + 137.8 + 28.0 + 7.3 + 3.8 + 6.7
    chk("S-10", "Sibandze Ch15", "Electricity cost (R M/yr)", 37.1, 2.57 * 8760 * 1.65 / 1e3)
    chk("S-11", "Sibandze Ch15", "Ore cost (R M/yr)", 137.8, 23105 * 2.13 * 2800 / 1e6)
    chk("S-12", "Sibandze Ch15", "Total incremental cost (R M/yr)", 220.7, costs)
    profit = rev - costs
    chk("S-13", "Sibandze Ch15", "Incremental profit (R M/yr)", 383, profit)
    capex = (45 + 25 + 10 + 30 + 200) * 1.2 + 30
    chk("S-14", "Sibandze Ch15", "Total investment (R M)", 402, capex)
    cf = profit - 0.27 * (profit - capex / 15)
    chk("S-15", "Sibandze Ch15", "After-tax cash flow (R M/yr) – incl. depreciation shield", 286, cf, tol=0.01,
        basis="AF-11: depreciation shield (402/15) not stated in Ch15")
    ann = (1 - 1.12 ** -15) / 0.12
    chk("S-16", "Sibandze Ch15", "NPV 15 y @12 % (R M)", 1540, cf * ann - capex, tol=0.02)
    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cf * (1 - (1 + mid) ** -15) / mid - capex > 0: lo = mid
        else: hi = mid
    chk("S-17", "Sibandze Ch15", "IRR (%)", 70, 100 * lo, tol=0.03)
    chk("S-18", "Sibandze Ch15", "Break-even alloy price (US$/t)", 550, costs * 1e6 / 23105 / 17.42, tol=0.01,
        basis="AF-11: operating break-even (excludes capital recovery)")
    # Simphiwe Ch. 16 PF table and Ch. 3
    for i, (pf, Steam) in enumerate(((0.923, 65.00), (0.920, 65.22), (0.900, 66.67), (0.880, 68.18), (0.950, 63.16))):
        chk(f"M-0{i+1}", "Simphiwe Ch16", f"S at 60 MW, PF {pf} (MVA)", Steam, 60 / pf, basis="60 MW treated as on-load power (S-O60)")
    chk("M-06", "Simphiwe Ch3", "Secondary voltage (V)", 312, el.secondary_voltage_V(S, el.electrode_current_kA(S * PF0, C3)), tol=0.01,
        basis="AF-04: 312 V is the pre-workbook (PF 0.846) value")
    chk("M-07", "Simphiwe Ch3", "Electrode current (kA)", 120.5, el.electrode_current_kA(S * PF0, C3), tol=0.01, basis="AF-04")
    chk("M-08", "Simphiwe Ch3", "Current density (A/cm2)", 6.38, el.current_density(el.electrode_current_kA(S * PF0, C3), D), tol=0.01, basis="AF-04")
    write("I1_verification.csv", ["check", "document", "quantity", "team_value", "model_value", "rel_diff_pct",
                                  "tolerance_pct", "status", "basis / audit note"], V)

    # ---------------------------------------------------------------- export for Octave/MATLAB
    with open(os.path.join(ROOT, "model", "inputs", "octave_scenarios.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["idx", "P_mean_or_neg1", "PF", "LF", "SEC", "S_rated", "C3", "D_m", "V_HV_kV"])
        for i, sc in enumerate(scs, 1):
            w.writerow([i, -1 if sc.P_mean is None else sc.P_mean, sc.PF, sc.LF, sc.SEC, S, C3, D,
                        inp["asm.hv_supply_kV"].value])
    with open(os.path.join(OUT, "I1_python_numeric.csv"), "w", newline="") as f:
        w = csv.writer(f)
        cols = ["P_mean_MW", "P_on_MW", "S_on_MVA", "Q_on_Mvar", "loading_on_pct", "I_primary_A_at_HV",
                "I_electrode_kA_est", "V_secondary_LL_V_est", "R_phase_mohm_est", "X_phase_mohm_est",
                "J_A_cm2_est", "E_daily_MWh", "production_tpd"]
        w.writerow(["idx"] + cols)
        for i, sc in enumerate(scs, 1):
            d = {r.metric: r.value for r in allrecs if r.scenario == sc.sid}
            w.writerow([i] + [repr(d[c]) for c in cols])

    n_rep = sum(1 for v in V if v[7] == "REPRODUCED")
    print(f"Scenarios evaluated: {len(scs)}; verification: {n_rep}/{len(V)} reproduced")
    for v in V:
        if v[7] != "REPRODUCED":
            print("  DIFFERS:", v[0], v[2], "team", v[3], "model", v[4], "|", v[8])
    return inp, scs, allrecs, V


if __name__ == "__main__":
    main()
