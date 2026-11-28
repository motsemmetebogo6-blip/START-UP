#!/usr/bin/env bash
# Runs the whole chain from the package root. Python 3.10 to 3.13; GNU Octave or MATLAB for the cross-checks.
set -e
python3 -m pytest -q model/tests
python3 model/run_increment1.py          # electrical model, 52 team numbers verified, Octave input files
python3 model/crossval_I1.py             # Python against the MATLAB/Octave result (needs results/model/I1_octave_numeric.csv)
python3 model/run_increment2.py          # mass balance, optimisation, Monte Carlo, robust design
python3 model/crossval_I2.py
python3 model/run_sensitivity_ch16.py    # NPV model, tornado, electrical and auxiliary plots
python3 model/build_excel.py             # Excel workbook with live formulas
python3 model/build_powerbi.py           # Power BI dataset, DAX, theme and page mock-ups
python3 model/export_dashboard_data.py   # data files for the MATLAB dashboard
(cd furnace_cad && python3 run_all.py)   # CAD, views, thermal model
echo "Now run the MATLAB/Octave scripts: see README_RUN.md section 3"
