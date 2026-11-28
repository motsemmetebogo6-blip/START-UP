@echo off
REM Windows: run each line from the package root in a Command Prompt where python is on the PATH
python -m pytest -q model\tests
python model\run_increment1.py
python model\crossval_I1.py
python model\run_increment2.py
python model\crossval_I2.py
python model\run_sensitivity_ch16.py
python model\build_excel.py
python model\build_powerbi.py
python model\export_dashboard_data.py
cd furnace_cad
python run_all.py
cd ..
echo Now run the MATLAB scripts: see README_RUN.md section 3
