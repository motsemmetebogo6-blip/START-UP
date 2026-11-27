# Power BI Engineering Dashboard – Build Guide

*Ferrochrome SAF uprate · dataset: SAF_PowerBI_Dataset.xlsx · Revision A*

## 1. Purpose

The dashboard is the project's **engineering decision-support tool**. Each of the five pages answers one engineering question, using only data exported from the verified model. No values are typed into Power BI. A page mock-up is provided for each page; it was rendered from the same dataset and shows the intended layout.

## 2. Files in the pack

| File | Use |
|---|---|
| `SAF_PowerBI_Dataset.xlsx` | 15 tables (star schema) – the only data source |
| `SAF_measures.dax` | All DAX measures (copy into a "Measures" table) |
| `SAF_theme.json` | Colour theme (View › Themes › Browse for themes) |
| `PBI_page1…5.png` | Layout mock-ups of the five pages (also in the presentation) |

## 3. Load and model the data (about 10 minutes)

1. **Get Data › Excel workbook** › select `SAF_PowerBI_Dataset.xlsx`. Tick all **tables** (not sheets) and click **Load**.
2. **Model view:** create these relationships (single direction, many-to-one):
   * `fact_scenario_metrics[ScenarioID]` → `dim_scenario[ScenarioID]`
   * `fact_constraints[ScenarioID]` → `dim_scenario[ScenarioID]`
   * `fact_scenario_metrics[Metric]` → `dim_metric[Metric]`
3. **Home › Enter data** › create an empty table named `Measures`. Paste each measure from `SAF_measures.dax` (one per **New measure**).
4. Set the formats:
   * percentage measures as %;
   * `Production t/d` with 0 decimals;
   * `On-load MVA` with 2 decimals.
5. Sort `dim_scenario[Scenario]` by `dim_scenario[Order]`.
6. Apply the theme `SAF_theme.json`.

## 4. Tables in the dataset

| Table | Rows | Content |
|---|---|---|
| dim_scenario | 8 | Scenario ID, name, definition, chapter that uses it, role |
| fact_scenario_metrics | 192 | 24 electrical and production metrics × 8 scenarios, with unit, provenance and equation |
| dim_metric | 24 | Metric, unit, module, estimate flag |
| fact_constraints | 56 | 7 acceptance criteria × 8 scenarios: value, limit, utilisation, PASS/FAIL |
| fact_mass_balance | 11 | Streams (kg/t; t/d existing and C1) |
| fact_balance_residuals | 7 | Residual of each conservation balance |
| fact_mb_kpi | 16 | Cr recovery, rates, off-gas, closure |
| fact_optimisation | 12 | Minimum hot-charge temperature against achievable load factor |
| fact_robust | 3 | Temperatures for 50 % and 90 % probability of 450 t/d |
| fact_tornado | 6 | Sensitivity of C1 production |
| fact_montecarlo_hist | 30 | Histogram of 100 000 Monte-Carlo samples |
| fact_verification | 52 | Team numbers recalculated, with status and audit note |
| fact_crossval | 122 | Python against MATLAB/Octave comparisons |
| dim_input_provenance | 157 | Every model input with its provenance tag |

## 5. Pages to build

### Page 1 – Baseline vs selected design (C1)

*Question: what does the selected design change?*

| Visual | Fields |
|---|---|
| 6 cards | `Mean Power MW`, `Production t/d`, `SEC MWh/t`, `On-load Loading %` (filters A and C1 side by side, or one card per scenario); `Cr Recovery %`; `P(>=450 t/d)` |
| Clustered column chart | Axis: `dim_scenario[ScenarioID]` (filter A, E1, S-B, P1, C1); Value: `Production t/d`; constant line at 450 |
| Bar chart | Axis: `fact_constraints[Criterion]`; Value: `Max Utilisation`; filter `ScenarioID = C1`; conditional colour by `Status` (PASS green, FAIL red); constant line at 1.0 |

### Page 2 – Transformer and electrical loading

*Question: is there headroom, and which "60 MW" is meant?*

| Visual | Fields |
|---|---|
| Bar chart | Axis: ScenarioID; Value: `On-load MVA`; constant line at 65; data labels on |
| Column chart | Axis: ScenarioID; Value: `Current Density A/cm2 (est.)`; constant line at the existing value 6.80 |
| Table | ScenarioID, Definition, PF, LF, `Mean Power MW`, `On-load Power MW`, `Electrode Current kA (est.)` |
| Slicer | `dim_metric[IsEstimate]`, so estimates can be switched on and off |

### Page 3 – Mass balance and metallurgy

*Question: what goes in and out per tonne, and is the data consistent?*

| Visual | Fields |
|---|---|
| 5 cards | From `fact_mb_kpi`: ore rate, reductant rate, slag rate, `Cr Recovery %`, off-gas Nm³/t |
| Bar chart | Axis: `fact_mass_balance[Stream]`; Value: kg_per_t; Legend: Direction |
| Column chart | Axis: `fact_balance_residuals[Balance]`; Value: Residual_pct_of_feed; reference lines at ±3 % |
| Clustered column | Stream against t_per_d_existing and t_per_d_C1 (auxiliary duty increase) |

### Page 4 – Optimisation and robustness

*Question: what is the least intervention that meets 450 t/d, and how sure are we?*

| Visual | Fields |
|---|---|
| Line chart | X: `fact_optimisation[LF_max]`; Y: T_opt_C; Legend: T_reference; constant line at 500 °C |
| Column chart (histogram) | X: Bin_mid_tpd; Y: Count; colour by MeetsTarget |
| Card | `P(>=450 t/d)` |
| Bar chart (tornado) | Axis: `fact_tornado[Input]`; Values: Production_low and Production_high; reference line at 450 |
| Table | `fact_robust`: case, T_P50_C, T_P90_C |

### Page 5 – Model verification and data provenance

*Question: how much rests on assumptions, and do the models agree?*

| Visual | Fields |
|---|---|
| 3 cards | `Checks Reproduced %`, `Cross-validation Worst Rel Diff`, count of MEASURED and SUPPLIED inputs |
| Bar chart | Axis: `dim_input_provenance[Provenance]`; Value: count of Input |
| Table | `fact_verification` filtered to Status ≠ REPRODUCED: Check, Quantity, TeamValue, ModelValue, AuditNote |

## 6. Rules for the dashboard

* **No hand-typed numbers.** If a value changes, re-run the model (`run_increment1.py`, `run_increment2.py`, `build_powerbi.py`) and press **Refresh**.
* Every page footer must state: *"Electrode current, voltage and current density are estimates (Westly C₃ calibration); see audit finding AF-08."*
* Use red only for a failed criterion or a risk, and green only for a pass, so colour carries engineering meaning.

## 7. DAX measures

All measures are in `SAF_measures.dax`. The most important are:

```
Production t/d = CALCULATE([Metric Value], fact_scenario_metrics[Metric] = "production_tpd")
On-load Loading % = DIVIDE([On-load MVA], 65)
Production Gain % = DIVIDE([Production Gain t/d], [Baseline Production t/d])
P(>=450 t/d) = DIVIDE(CALCULATE(SUM(fact_montecarlo_hist[Count]), fact_montecarlo_hist[MeetsTarget] = "Yes"),
                      SUM(fact_montecarlo_hist[Count]))
Binding Criterion = VAR m = [Max Utilisation]
                    RETURN CALCULATE(FIRSTNONBLANK(fact_constraints[Criterion], 1), fact_constraints[Utilisation] = m)
```
