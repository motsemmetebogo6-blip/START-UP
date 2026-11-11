"""
export_powerbi.py – builds the Power BI star-schema dataset (docs/00 §10.2).

Reads ONLY repository sources (results/*.csv, registers/*.csv, parameters.py) so the
dashboard can never diverge from the calculations. Run after any calc changes:
    python calcs/export_powerbi.py
Writes powerbi/*.csv
"""
import csv, os
import parameters as p

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "powerbi"); os.makedirs(OUT, exist_ok=True)
REV = "Rev0-G0"

# Map calc-02 cases to framework scenarios (docs/00 §7.1)
SCEN = {
    "Baseline 55 MW": ("A", "Scenario A – existing 55 MW (reference furnace)", "Reference"),
    "60 MW at 65 MVA, X -0%": ("B0", "Scenario B0 – 60 MW, R change only", "Candidate"),
    "60 MW at 65 MVA, X -20%": ("B20", "Scenario B20 – 60 MW, X −20 % + R +21 % (preferred, provisional)", "Preferred"),
    "60 MW at 65 MVA, X -30%": ("B30", "Scenario B30 – 60 MW, mainly X reduction", "Candidate"),
    "60 MW Westly-ideal, X unchanged": ("F1", "Rejected – Westly-ideal current, X unchanged", "Rejected"),
    "60 MW constant R, X unchanged": ("F2", "Rejected – same R, more current", "Rejected"),
}
PARAMS = [  # ParamID, column, name, unit, WP, owner, category
    ("P", "P_MW", "Active power", "MW", "WP3", "M2", "Electrical"),
    ("S", "S_MVA", "Apparent power", "MVA", "WP3", "M2", "Electrical"),
    ("Q", "Q_Mvar", "Reactive power", "Mvar", "WP3", "M2", "Electrical"),
    ("PF", "PF", "Power factor", "-", "WP3", "M2", "Electrical"),
    ("I", "I_kA", "Electrode current", "kA", "WP3", "M2", "Electrical"),
    ("VLL", "V_LL_V", "Secondary voltage (line)", "V", "WP3", "M2", "Electrical"),
    ("R", "R_mohm", "Operating resistance per phase", "mΩ", "WP3", "M2", "Electrical"),
    ("X", "X_mohm", "Circuit reactance per phase", "mΩ", "WP3", "M2", "Electrical"),
    ("J", "J_A_cm2", "Electrode current density", "A/cm²", "WP4", "M3", "Electrodes"),
    ("C3", "C3", "Westly C3", "-", "WP3", "M2", "Electrical"),
]
DERIVED = [("PPH", "Phase power", "MW", "WP3", "M2", "Electrical"),
           ("LOAD", "Transformer loading", "%", "WP3", "M2", "Electrical"),
           ("RX", "R/X ratio", "-", "WP3", "M2", "Electrical"),
           ("D", "Electrode diameter", "m", "WP4", "M3", "Electrodes")]

def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f"powerbi/{name}: {len(rows)} rows")

# dim_scenario
write("dim_scenario.csv", ["ScenarioID", "Name", "Role", "Order"],
      [(sid, name, role, i) for i, (sid, name, role) in enumerate(SCEN.values())])
# dim_parameter
write("dim_parameter.csv", ["ParamID", "Name", "Unit", "WP", "Owner", "Category"],
      [(a, c, d, e, f, g) for a, b, c, d, e, f, g in PARAMS] + list(DERIVED))

# fact_values
facts = []
with open(os.path.join(ROOT, "results", "02_operating_points.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["case"] not in SCEN:
            continue
        sid = SCEN[row["case"]][0]
        for pid, col, *_ in PARAMS:
            tag = "S" if pid == "P" else "C"
            src = "Brief S-01/S-02" if pid == "P" else "calcs/02_electrical_operating_points.py"
            facts.append((sid, pid, float(row[col]), tag, src, "WP3" if pid != "J" else "WP4", "G3-provisional", REV))
        P, S = float(row["P_MW"]), float(row["S_MVA"])
        facts += [(sid, "PPH", round(P / 3, 3), "C", "P/3", "WP3", "G3-provisional", REV),
                  (sid, "LOAD", round(100 * S / p.S_RATED_MVA, 2), "C", "S/65 MVA", "WP3", "G3-provisional", REV),
                  (sid, "RX", round(float(row["R_mohm"]) / float(row["X_mohm"]), 3), "C", "R/X", "WP3", "G3-provisional", REV),
                  (sid, "D", p.D_ELECTRODE_M, "A", "A-16", "WP4", "G1-RFS", REV)]
write("fact_values.csv", ["ScenarioID", "ParamID", "Value", "Tag", "SourceRef", "WP", "Gate", "Rev"], facts)

# fact_limits from equipment register (rows with numeric limit and values)
lim = []
with open(os.path.join(ROOT, "registers", "equipment_classification.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        lim.append((r["EquipmentID"], r["Component"], r["Class"], r["Criterion"], r["Limit"], r["Unit"],
                    r["Value_A_55MW"], r["Value_B_60MW_B20"], r["Owner_WP"]))
write("fact_limits.csv", ["EquipmentID", "Component", "Class", "Criterion", "Limit", "Unit",
                          "Value_A", "Value_B20", "Owner_WP"], lim)

# dim_assumption (copy of the controlled register)
with open(os.path.join(ROOT, "registers", "assumptions_register.csv"), encoding="utf-8") as f:
    rows = list(csv.reader(f))
write("dim_assumption.csv", rows[0], rows[1:])
