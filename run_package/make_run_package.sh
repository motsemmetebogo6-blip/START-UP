#!/usr/bin/env bash
# Builds deliverables/SAF_Run_Package.zip: everything needed to run the Python, MATLAB/Octave, CAD and thermal scripts.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
P=/tmp/SAF_Run_Package; rm -rf $P; mkdir -p $P
cp -r data $P/data
mkdir -p $P/model && cp -r model/safmodel model/inputs model/tests model/*.py $P/model/
mkdir -p $P/matlab && cp matlab/*.m $P/matlab/ && cp -r matlab/dashboard_data $P/matlab/
mkdir -p $P/results/model && cp results/model/*.csv $P/results/model/
mkdir -p $P/report/figures && cp report/figures/*.png $P/report/figures/
mkdir -p $P/furnace_cad && cp furnace_cad/*.py furnace_cad/octave_check.m $P/furnace_cad/ && cp -r furnace_cad/cad_files furnace_cad/images furnace_cad/thermal_results $P/furnace_cad/
mkdir -p $P/powerbi && cp powerbi/SAF_PowerBI_Dataset.xlsx powerbi/SAF_measures.dax powerbi/SAF_theme.json $P/powerbi/
mkdir -p $P/deliverables && cp deliverables/SAF_Engineering_Model.xlsx $P/deliverables/
cp run_package/README_RUN.md run_package/requirements.txt run_package/run_all.sh run_package/run_all.bat $P/
find $P -name "__pycache__" -prune -exec rm -rf {} +
rm -f deliverables/SAF_Run_Package.zip
(cd /tmp && zip -qr "$ROOT/deliverables/SAF_Run_Package.zip" SAF_Run_Package)
echo "built $(du -h deliverables/SAF_Run_Package.zip | cut -f1)"
