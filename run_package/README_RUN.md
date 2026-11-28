# SAF run package: Python, MATLAB/Octave, CAD and thermal scripts

Project: design and scale-up of a closed ferrochrome submerged arc furnace from 55 to 60 MW (MPG 118S).
All scripts use paths relative to this folder, so unzip it anywhere and run every command from this folder (the "package root").

## 1. What is inside

| Folder | Content |
|---|---|
| `data/` | `Ferrochrome_Data_Workbook.xlsx`, the supervisor's plant data (the governing source) |
| `model/` | Python model package `safmodel` (inputs with provenance, electrical, production, scenarios, mass balance, optimisation), run scripts, cross-validation, tests, Excel and Power BI builders |
| `model/inputs/` | `model_inputs.csv` (157 inputs with provenance tags) and the numeric files read by MATLAB |
| `matlab/` | MATLAB / Octave scripts and `dashboard_data/` for the dashboard |
| `results/model/` | Results written by the scripts (CSV). Copies from the last run are included |
| `furnace_cad/` | Parametric CAD (`params.py`), STEP/STL/DXF in `cad_files/`, dimensioned views in `images/`, thermal model and `thermal_results/` |
| `powerbi/` | Power BI dataset, DAX measures and theme |
| `deliverables/` | `SAF_Engineering_Model.xlsx` (live formulas) |

## 2. Python (3.10 to 3.13)

    pip install -r requirements.txt
    python3 -m pytest -q model/tests          # 7 tests
    python3 model/run_increment1.py           # electrical model; verifies 52 numbers of the team's chapters
    python3 model/run_increment2.py           # mass balance, optimisation, Monte Carlo, robust design
    python3 model/run_sensitivity_ch16.py     # economics, NPV tornado, electrical and auxiliary sensitivity
    python3 model/build_excel.py              # writes deliverables/SAF_Engineering_Model.xlsx
    python3 model/build_powerbi.py            # writes the Power BI dataset, DAX, theme and mock-ups
    python3 model/export_dashboard_data.py    # data for the MATLAB dashboard
    cd furnace_cad && python3 run_all.py      # CAD, views, thermal model (needs cadquery, numba, ezdxf)

`run_all.sh` (Linux/macOS) or `run_all.bat` (Windows) runs the sequence. `cadquery` is a large package; if it cannot be installed, skip the CAD step: the thermal solver (`thermal_fvm.py`, `thermal_run.py`) needs only numpy, scipy and matplotlib, but `thermal_run.py` is called from `furnace_cad/run_all.py` after the CAD step, so run it directly: `cd furnace_cad && python3 thermal_run.py`.

## 3. MATLAB or GNU Octave

Start MATLAB (or `octave-cli`) with the **package root** as the current folder, then:

    addpath('matlab')
    saf_electrical_I1()       % reads model/inputs/octave_scenarios.csv, writes results/model/I1_octave_numeric.csv
    saf_massbalance_I2()      % non-negative least squares (lsqnonneg), writes results/model/I2_octave_massbalance.csv
    saf_optimum_I2()          % least preheat temperature
    saf_npv_ch16()            % NPV and IRR (fzero), writes results/model/CH16_octave_npv.csv
    cd furnace_cad; octave_check()   % thermal solver, independent of Python (reads furnace_cad/octave_io, made by thermal_run.py)
    cd ..; saf_dashboard('dashboard_matlab.png')   % six-panel dashboard (run inside matlab/ or with matlab on the path)

Then compare with Python:

    python3 model/crossval_I1.py      # expect 104 of 104 comparisons pass
    python3 model/crossval_I2.py      # expect 18 of 18 pass (worst relative difference about 1e-4, in the optimum)

Notes: the scripts use only functions available in MATLAB and Octave (`csvread`, `fprintf`, `lsqnonneg`, `fzero`). `saf_dashboard.m` was tested only for its data-reading part (`saf_dashboard('dry')`); run its plotting once in MATLAB.

## 4. Expected key results (to check your run)

| Quantity | Value |
|---|---|
| C1 production (ambient preheat reference) | 454.6 t/d |
| Transformer loading while on load, C1 | 64.98 MVA (99.97 %) |
| Chromium recovery, reconciled | 86.9 % |
| Least preheat for 450 t/d | 452 degrees C |
| P(450 t/d) at 500 degrees C, unverified saving | about 10 % |
| NPV, IRR (verified model) | R1 479 M, 68.7 % |
| Thermal model: Joule heat per electrode, 500 C isotherm | 2.74 MW, z = 9.94 m |

## 5. CAD files for SolidWorks and COMSOL

`furnace_cad/cad_files/`: `furnace_assembly.step` (named bodies), `furnace_solid.step`, `furnace_open_cut_quarter.step`, `.stl`, and `revolve_cut_profile_half_section.dxf` (half-section sketch for the revolve and the revolve cut). Dimensions are in metres and are tagged DATA, DERIVED, PICTURE or ASSUMED in `furnace_cad/params.py`. Change a value there and run `python3 run_all.py` in `furnace_cad` to rebuild every file and view.

## 6. Power BI

`powerbi/SAF_PowerBI_Dataset.xlsx` is the only data source: Get Data, Excel workbook, load all tables, add the three relationships, paste the measures of `SAF_measures.dax`, apply `SAF_theme.json` (steps in the build guide in the submission ZIP).

## 7. Known limits

* Electrode current, voltage, current density and all electrode temperatures are estimates (Westly constant, assumed material data).
* The thermal model is a single-electrode axisymmetric cell with a prescribed burden temperature; no COMSOL `.mph` file is included.
* The MATLAB scripts were run in GNU Octave 8.4, not in MATLAB itself.
