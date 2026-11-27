"""Automated tests for Increment 1 (run: python3 -m pytest model/tests -q)."""
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from safmodel import data_io, electrical as el, production as pr   # noqa: E402

INP = data_io.load_inputs()


def test_workbook_values_read_not_retyped():
    assert INP["wb.transformer_capacity"].value == 65
    assert INP["wb.power_factor"].value == 0.93
    assert INP["wb.load_factor"].value == 0.95
    assert INP["wb.power_factor"].tag == "ASSUMED"          # workbook status "Assumed"
    assert INP["wb.load_factor"].tag == "CALIBRATED"        # back-solved, not measured
    assert INP["wb.ferrochrome_production_target"].tag == "TARGET"
    assert INP["slag.slag.Cr2O3 (%)"].tag == "MEASURED"


def test_mean_power_matches_workbook():
    S, PF, LF = 65, 0.93, 0.95
    assert abs(S * PF * LF - INP["wb.mean_active_power"].value) < 0.01


def test_production_reconciles_with_actual():
    m = pr.production_tpd(65 * 0.93 * 0.95, 3.5)
    assert abs(m - 393.65) / 393.65 < 0.001


def test_onload_identity():
    op = el.operating_point(60.0, 0.95, 0.972, 65, 8.33, 1.55, 132)
    assert abs(op["S_on_MVA"][0] - 60 / 0.972 / 0.95) < 1e-12
    assert op["loading_on_pct"][0] > 99.9            # AF-03: no on-load headroom under C1


def test_secondary_consistency_delta():
    I = el.electrode_current_kA(60.45, 8.33)
    V = el.secondary_voltage_V(65, I)
    Iw = el.winding_current_kA(I)
    assert abs((65 / 3) * 1e6 - V * Iw * 1e3) / (65 / 3 * 1e6) < 1e-12   # each 1-phase unit carries S/3


def test_pf_route_ratios_independent_of_C3():
    rR = el.pf_route_current_ratio(0.93, 0.95, "R")
    rX = el.pf_route_current_ratio(0.93, 0.95, "X")
    assert rR < 1 < rX
    assert abs(rR - math.sqrt(math.sqrt(1 - .95**2) / math.sqrt(1 - .93**2))) < 1e-12


def test_verification_and_crossval_pass():
    root = data_io.ROOT
    r = subprocess.run([sys.executable, os.path.join(root, "model", "run_increment1.py")], capture_output=True, text=True)
    assert "verification: 47/52 reproduced" in r.stdout      # 5 differences are explained audit findings
