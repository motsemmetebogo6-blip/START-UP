"""
data_io.py – reads the supervisor's data workbook (never retyped) and assembles the single
input table, combining workbook values, literature values and documented assumptions,
each with a provenance tag. Writes model/inputs/model_inputs.csv.
"""
import csv
import os
import openpyxl

from .provenance import Q, WORKBOOK_STATUS_TO_TAG

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORKBOOK = os.path.join(ROOT, "data", "Ferrochrome_Data_Workbook.xlsx")
INPUTS_CSV = os.path.join(ROOT, "model", "inputs", "model_inputs.csv")


def _num(x):
    """The workbook stores some numbers as text; convert where possible."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _tag(status):
    s = (status or "").strip().lower()
    return WORKBOOK_STATUS_TO_TAG.get(s, "ASSUMED")


def load_workbook_inputs(path=WORKBOOK):
    """Return dict name -> Q for every numeric workbook value used by the model."""
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {}

    # --- Assumptions sheet (row 4 header: Parameter, Original, Adjusted, Unit, Status, Reason)
    for r in wb["Assumptions"].iter_rows(min_row=5, values_only=True):
        name, orig, adj, unit, status, reason = (list(r) + [None] * 6)[:6]
        if not name:
            continue
        v = _num(adj) if adj is not None else _num(orig)
        if v is None:
            continue
        out[f"wb.{name}"] = Q(f"wb.{name}", v, unit or "", _tag(status),
                              "Workbook!Assumptions", (reason or "")[:160])

    # --- Recipe (within-group fractions)
    for r in wb["Recipe"].iter_rows(min_row=5, values_only=True):
        group, mat, frac, status, note = (list(r) + [None] * 5)[:5]
        if group and _num(frac) is not None:
            out[f"recipe.{group}.{mat}"] = Q(f"recipe.{group}.{mat}", _num(frac) / 100, "fraction",
                                             _tag(status), "Workbook!Recipe", note or "")

    # --- Analyses: mean rows of Ore, Fluxes, Reductants (material in col A), Metal, Slag (no material)
    def means(sheet, has_material):
        ws = wb[sheet]
        hdr = [c.value for c in ws[4]]
        for row in ws.iter_rows(min_row=5, values_only=True):
            label = row[1] if has_material else row[0]
            if label != "Mean (reported)":
                continue
            mat = row[0] if has_material else sheet.lower()
            for h, v in zip(hdr, row):
                if h and _num(v) is not None and h not in ("Sample",):
                    key = f"{sheet.lower()}.{mat}.{h}"
                    out[key] = Q(key, _num(v), "", "MEASURED", f"Workbook!{sheet} (mean reported)")

    means("Ore", True); means("Fluxes", True); means("Reductants", True)
    means("Metal", False); means("Slag", False)
    return out


# Values NOT contained in the workbook: literature and documented assumptions (register A-xx).
NON_WORKBOOK_INPUTS = [
    Q("lit.electrode_diameter_m", 1.55, "m", "LITERATURE", "R-11, R-13; A-16", "Söderberg, 63 MVA SA FeCr analogues"),
    Q("lit.westly_C3", 8.33, "kA/MW^(2/3)", "LITERATURE", "Westly (1974) calibrated on R-13 (48 MW, 110 kA); A-18",
      "single-analogue calibration – estimate only"),
    Q("lit.westly_C3_low", 6.0, "kA/MW^(2/3)", "LITERATURE", "R-12 reported FeCr range", ""),
    Q("lit.westly_C3_high", 11.0, "kA/MW^(2/3)", "LITERATURE", "R-12 reported FeCr range", ""),
    Q("lit.pcd_m", 4.185, "m", "LITERATURE", "A-19 (PCD/D 2.70 from R-16, R-17)", ""),
    Q("lit.hearth_diameter_m", 10.881, "m", "LITERATURE", "A-20 (hearth/PCD 2.60 from R-16, R-17)", ""),
    Q("lit.shell_inner_diameter_m", 13.7, "m", "LITERATURE", "R-11", ""),
    Q("asm.hv_supply_kV", 132.0, "kV", "ASSUMED", "A-21", "sensitivity 88 kV"),
    Q("asm.hv_supply_kV_alt", 88.0, "kV", "ASSUMED", "A-21", ""),
    Q("asm.pf_upper_limit", 0.95, "-", "SUPPLIED", "Workbook!Assumptions F6 (supervisor: <=0.95 acceptable)", ""),
    Q("asm.hot_charge_sec_saving_per_100C", 0.070, "MWh/t per 100 C", "LITERATURE", "Metso (n.d.) R-04", "vendor rule of thumb"),
    Q("asm.hot_charge_temperature_C", 500.0, "C", "ASSUMED", "A-24", "screening value"),
    Q("prop.lf_c1", 0.972, "-", "PROPOSED", "Ch. 12 alternative E2/C1", "60 MW mean at PF 0.95"),
    Q("prop.pf_c1", 0.95, "-", "PROPOSED", "Ch. 12 alternative E1/C1", "supervisor limit"),
    Q("brief.P_existing_MW", 55.0, "MW", "SUPPLIED", "Project brief", "'approximately 55 MW' – see A-25"),
    Q("brief.P_proposed_MW", 60.0, "MW", "SUPPLIED", "Project brief", "meaning defined per scenario"),
]


def load_inputs():
    """All inputs as dict name -> Q."""
    d = load_workbook_inputs()
    for q in NON_WORKBOOK_INPUTS:
        d[q.name] = q
    return d


def write_inputs_csv(inputs, path=INPUTS_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "value", "unit", "provenance", "source", "note"])
        for k in sorted(inputs):
            q = inputs[k]
            w.writerow([q.name, q.value, q.unit, q.tag, q.source, q.note])
    return path
