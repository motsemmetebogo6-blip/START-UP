# 08 – Project Audit and Engineering Modelling Architecture

**Prepared by:** Tebogo Motsemme (Project Leader), with engineering-model support · **Date:** 2026-11-27 · **Revision:** A

---

## Part A – Audit of the existing project

### A.1 Scope of the audit

| Item audited | Author | Content |
|---|---|---|
| `Jeff_CHAPTER_2_PROBLEM_DEF.docx` | Jeff | Ch. 2 Problem definition |
| `Ngesi__Design.docx` | Ngesi | Ch. 9 Energy balance, Ch. 11 Process/metallurgical analysis, Ch. 19 Implementation plan (28 pages, including 16 table and figure images) |
| `MPG_PROJECT_1.docx` | Sibandze | Ch. 14 Equipment requirements, Ch. 15 Economic evaluation, Ch. 18 Recommended design |
| `MPG_project_individual_part_revised_2.docx` | Simphiwe | Ch. 3 Existing process description, Ch. 16 Sensitivity, Ch. 17 Risk |
| `MPG_FINAL_PROJECT.docx` | Compiled | Title page, chapter headings, literature review |
| `Ferrochrome_Data_Workbook_1.xlsx` | Supervisor | **Byte-identical** to `data/Ferrochrome_Data_Workbook.xlsx` already in the repository |
| Repository | Tebogo | Docs 00–07; Ch. 4, 7, 12; `calcs/`; registers |

**Not received, so not audited:** Mkhonto's Ch. 5, 6 and 8 (mass balance) and Jeff's Ch. 10 and 13. Several numbers used in Ch. 14 and 15 come from that mass balance: 0.433 t reductant/t, 0.449 t flux/t, 530 t/d slag and 10 200 m³/h gas. **Those numbers cannot be traced yet.**

### A.2 Method

Every numerical result in the team documents was recalculated independently. Increment 1 of the model (`model/tests/test_team_verification.py`) reproduces each team calculation automatically and states whether it agrees. Definitions were checked against the source wording in the data workbook.

### A.3 Findings

Severity levels:
* **Critical:** changes a design conclusion.
* **Major:** a wrong value or label that would mislead a reader.
* **Moderate:** an inconsistency.
* **Minor:** presentation or reference quality.

| ID | Severity | Where | Finding | Evidence | Recommended action |
|---|---|---|---|---|---|
| **AF-01** | **Critical** | Ngesi Ch. 9, 19 | The workbook's **load factor 0.95** is interpreted as a **"95 % transformer-loading limit"**. From this, Ngesi derives "PF ≥ 0.972 required" and "67.91 MVA required". | Workbook `Assumptions!F7`: *"back-solved from supplied actual production … not independently measured"*. Mean power = 65 × 0.93 × **0.95** is a time-average factor, not a loading cap. | Adopt the workbook meaning. The model computes both readings side by side (scenarios S-N55 and S-N60) so the difference is visible. Under the workbook meaning, 60 MW mean needs PF × LF ≥ 0.923. |
| **AF-02** | **Critical** | Ngesi Ch. 9, 11, 19 | The baseline is taken as **55 MW continuous → 377 t/d**. The supervisor's actual production is **393.65 t/d at 57.43 MW mean**. | Workbook `Assumptions!C12`. Ch. 7 shows the energy-based production matches the actual to 0.04 %. | Use 57.43 MW / 393.65 t/d as the baseline in every chapter. Keep the brief's "≈ 55 MW" only as an interpretation note (A-25). |
| **AF-03** | **Major** | Sibandze Ch. 14 | "At 60 MW and PF 0.95 the transformer carries 63.2 MVA (97 %)." This applies the **mean** power to the **on-load** rating. Under C1 (LF 0.972), on-load power = 60 / 0.972 = 61.73 MW, so *S*_on = 61.73 / 0.95 = **64.98 MVA (≈ 100 %)**. | Model scenario S-C1 | The transformers have **no on-load headroom** under C1. The OEM thermal check (IEC 60076-7 loading guide) becomes a hard gate, not a formality. |
| **AF-04** | **Major** | Simphiwe Ch. 3 | The electrical table gives **312 V, 120.5 kA, 6.38 A/cm²** and says the present PF is **≈ 0.846**. These are pre-workbook values. At the workbook PF of 0.93 the same method gives **≈ 293 V, ≈ 128 kA, ≈ 6.8 A/cm²**. | `results/07_existing_condition.csv` | Update Ch. 3 to the workbook basis. Also: two table captions are swapped, slag is described as "solid" (it is molten), and the viscosity has no unit. |
| **AF-05** | **Major** | Sibandze Ch. 14, 15 | Ore consumption of **2.13 t/t is called "measured"**. It is a **calculated upper-bound estimate** from the Al₂O₃ tracer balance (Ch. 7 §7.8). | Ch. 7 §7.8 | Relabel it as an estimate. The economics change by about R8 M/yr per 0.05 t/t, so it should go into the sensitivity analysis. |
| **AF-06** | Moderate | Simphiwe Ch. 16 | SEC reference **3.25 MWh/t** (superseded A-04) instead of the workbook's **3.5**. A-23 is described as a "280–400 V requirement"; in fact A-23 is the *existing* range of 260–340 V, and 280–400 V is the *required* range. | Assumptions register | Correct the parameter table. |
| **AF-07** | Moderate | Ngesi Ch. 9 Table 9.2 | Slag Cr₂O₃ 9.54 % is called a "provisional target, not a measured result". The workbook says **Measured** (the mean of 5 samples, *correcting* the earlier 15 %). | Workbook `Assumptions!E18` | Correct the label. The "36.4 % reduction in losses" argument then does not apply: 9.54 % is the actual state, not an improvement. |
| **AF-08** | Moderate | All chapters with electrode current | Secondary current, voltage and current density all come from a **single literature calibration** (Westly C₃ = 8.33). The plant data contain **no electrical measurements**. Over the reported C₃ range (6–11), the current ranges from 92 to 169 kA. | Ch. 7 §7.4 | Show these values everywhere as estimates with a range. Measurement is gate 1 in Ch. 18. |
| **AF-09** | Moderate | Ch. 12, 14, 15, 18 | The C1 production of 457 t/d rests on SEC 3.15 MWh/t (hot charging at 500 °C, A-24, using a vendor rule of thumb). The margin over the 3.20 needed is only **1.6 %**. | Ch. 12 §12.7 | This is the most important uncertainty to quantify (Increment 4: Monte-Carlo). |
| **AF-10** | **Major** (new) | Ch. 12, 14, 18 | **Whether the electrode current density meets DC-04 depends on how the power factor is raised.** Raising *R* (PCD or burden) lowers the current by about 8 %. Lowering *X* (short network) at constant *R* raises it by about 1 %. Ch. 14 and 18 prescribe the short-network route, which **slightly exceeds** DC-04 ("J not above existing"). | Model `electrical.pf_route_comparison` | Jeff (Ch. 10/13) must decide. Options: a combined *R*/*X* route, or relax DC-04 to a literature limit. |
| **AF-11** | Minor | Sibandze Ch. 15 | The arithmetic is **verified to within rounding**: revenue R604 M, costs R220.7 M, profit R383 M, investment R402 M, NPV ≈ R1 546 M, IRR ≈ 71 %. Not stated: (i) the after-tax figure includes a straight-line depreciation tax shield over 15 years; (ii) the break-even price excludes capital recovery; (iii) the energy cost of the hot-charging heat source is excluded. | `model/tests` | State the three bases explicitly. Add the preheat energy cost when it is known. |
| **AF-12** | Minor | References | "Saevarsdottir *et al.* (2023) … INFACON 8": INFACON 8 was held in 1998. "Hurman Eric, R. (2024)" has a suspect author format. Several sources were read only at abstract level (doc 05). | Reference register | Verify before submission. |
| **AF-14** | Moderate | Ch. 12 (Tebogo) | The hot-charging rule (−70 kWh/t per +100 °C) was applied to the **full 500 °C** (3.5 − 0.35 = 3.15 MWh/t). The preheat increase should be measured from ambient (≈ 25 °C): 3.5 − 0.07 × 4.75 = **3.1675 MWh/t**, giving C1 = **454.6 t/d** instead of 457.1 t/d. The 450 t/d gate still passes, but the margin shrinks from 1.6 % to **1.0 %**. | Model check T-02 | Report both values. Carry the ambient-referenced value as the conservative case in sensitivity and economics. |
| **AF-13** | Info | Jeff Ch. 2 | Consistent with the workbook and with Ch. 4, 7 and 12. No corrections needed. | – | – |

### A.4 Three different meanings of "60 MW" in the team documents

The most important consequence of AF-01 to AF-03 is that **"60 MW" is used with three meanings**. The model therefore carries all three as named scenarios:

| Scenario | Meaning | PF | LF | *P*_on (MW) | *S*_on (MVA) | On-load loading | Used by |
|---|---|---|---|---|---|---|---|
| S-B | 60 MW **mean**, workbook definition (C1 electrical) | 0.95 | 0.972 | 61.73 | 64.98 | ≈ 100 % | Ch. 12, 14, 18 |
| S-N60 | 60 MW **continuous** (LF = 1) | 0.93 | 1.00 | 60.00 | 64.52 | 99.3 % | Ngesi Ch. 9 |
| S-O60 | 60 MW **on load**, LF unchanged | 0.93 | 0.95 | 60.00 | 64.52 | 99.3 % | Simphiwe Ch. 16; mean only 57.0 MW |

**Recommendation:** the report should define 60 MW as the **mean** active power (S-B), consistent with the workbook's own definition of 57.43 MW. Every chapter should then state its loading on the **on-load** basis.

---

## Part B – Implementation architecture

### B.1 Design principles

1. **Single source of truth.** The supervisor's workbook is read directly and never retyped. All other inputs live in one versioned input table (`model/inputs/model_inputs.csv`) that carries a **provenance tag** for every value.
2. **Provenance on every number.** Each input and output carries one tag: `MEASURED`, `SUPPLIED`, `CALIBRATED`, `DERIVED-WB`, `TARGET`, `ASSUMED`, `LITERATURE`, `CALCULATED` or `PROPOSED`. The tags propagate into tables, figures and Power BI.
3. **Preserve the original work.** Existing chapters, `calcs/` scripts and results are not modified. The new package lives in `model/`, `matlab/`, `cad/` and `powerbi/`.
4. **Verify before extending.** Each increment starts by reproducing the existing team numbers (automated tests), and only then adds new capability.
5. **Independent cross-validation.** MATLAB/Octave code re-implements the core equations **without calling Python**. Both read the same input table. A comparison script checks agreement to a relative tolerance of 10⁻⁶.
6. **No invented data.** Where data are missing (for example reaction enthalpies or secondary measurements), the model either uses cited literature values with ranges or stops and reports the gap.

### B.2 Component architecture

```
                 ┌──────────────────────────────────────────────┐
                 │ data/Ferrochrome_Data_Workbook.xlsx (supervisor, read-only)
                 └───────────────┬──────────────────────────────┘
                                 │ read + provenance tagging
                 ┌───────────────▼──────────────────────────────┐
                 │ model/inputs/model_inputs.csv  (single input table)
                 │   workbook values + literature + assumptions │
                 └───────┬─────────────────────────────┬────────┘
                         │                             │
        ┌────────────────▼──────────────┐   ┌──────────▼───────────────┐
        │ Python package  model/safmodel│   │ MATLAB/Octave  matlab/    │
        │  provenance · data_io         │   │  saf_electrical.m         │
        │  electrical · production      │   │  saf_production.m         │
        │  massbalance · energy         │   │  saf_massbalance.m (I2)   │
        │  sensitivity · optimise       │   │  scenario + figure scripts│
        │  scenarios · geometry/CAD     │   └──────────┬───────────────┘
        │  reporting (figures/tables)   │              │ outputs CSV
        └───────┬───────────────┬───────┘              │
                │               │       ┌──────────────▼──────────────┐
                │               └──────►│ crossval: Python vs MATLAB   │
                │                       │ (relative tolerance 1e-6)    │
                │                       └──────────────┬──────────────┘
   ┌────────────▼─────────┐  ┌──────────────────┐     │
   │ results/model/*.csv  │  │ cad/*.dxf, *.png │     │
   │ report/figures/*     │  └──────────────────┘     │
   └────────────┬─────────┘                           │
                │   star-schema export                │
        ┌───────▼───────────────────────────────▼─────┐
        │ powerbi/ – fact & dimension CSVs, DAX measures,│
        │ page specification (engineering dashboard)     │
        └────────────────────────────────────────────────┘
```

### B.3 Module responsibilities

| Module | Engineering content | Data support |
|---|---|---|
| `electrical` | Mean versus on-load power; *S*, *P*, *Q*; transformer loading; primary and secondary line currents; winding current (delta closed at electrodes); electrode current (Westly C₃, with range); current density; *R*, *X*, *R*/*X*; PF and LF required; comparison of PF-raising routes (*R* versus *X*) | Workbook (S, PF, LF), literature (D, C₃), assumptions (HV) |
| `production` | Daily energy, production, SEC required, power required, target checks | Workbook |
| `massbalance` (I2) | Over-determined element balance (Cr, Fe, Si, C, O, Al₂O₃, MgO, CaO, SiO₂) solved by non-negative least squares for ore, reductant, quartz, limestone and slag. Residuals expose inconsistencies in the data; Cr recovery is an output | Workbook analyses and recipe |
| `energy` (I3) | Enthalpy balance using cited standard-state data (NIST-JANAF) with stated reference states. Effect of preheat on SEC. Theoretical minimum energy | Literature thermochemistry; workbook temperatures |
| `sensitivity` (I4) | One-at-a-time tornado charts and Monte-Carlo propagation of the uncertain inputs (PF, LF, SEC, C₃, ore rate, prices) | All |
| `optimise` (I4) | Feasible region in PF–LF–SEC space for 450 t/d; least-change design; capex-weighted optimum (when cost data are confirmed) | Model + Ch. 15 costs |
| `geometry` / CAD (I6) | Parametric plan and section drawings (DXF + PNG): shell, hearth, electrodes on the PCD, clearances, PCD/D options. Clearly labelled **literature-based, not as-built** | Literature geometry (A-16, A-19, A-20) |
| `reporting` | Publication-style figures (300 dpi PNG + SVG), engineering tables (CSV and Word), provenance footnotes | Model outputs |

### B.4 Power BI design (Increment 7)

The star schema is fed only from the model export:
* `fact_results` (scenario × metric)
* `fact_constraints` (scenario × acceptance criterion: value, limit, utilisation, pass/fail)
* `fact_sensitivity`
* `fact_crossval`
* `dim_scenario`, `dim_metric` (with unit, provenance and module), `dim_criterion`

Pages, each answering one engineering question:
1. **Baseline vs 60 MW:** what changes?
2. **Transformer and electrical loading:** is there headroom?
3. **Production levers (PF, LF, SEC):** what reaches 450 t/d?
4. **Constraints:** which acceptance criterion binds?
5. **Uncertainty:** how robust is C1?
6. **Data provenance and model verification:** how much rests on assumptions, and do Python and MATLAB agree?

No decorative visuals: every chart answers one engineering question. Power BI Desktop is not available in this environment, so the deliverable is the dataset, the DAX measures and the page specification. The .pbix file is built in Power BI Desktop.

### B.5 Where specialised electrical software (ETAP or equivalent) adds value

| Study | Why it matters here | Input data needed (currently missing) |
|---|---|---|
| Load flow including the grid | Voltage at the furnace transformer HV terminals at 65 MVA; tap selection | Grid fault level and X/R at the PCC; HV cable/line data; transformer impedance and tap table |
| Short circuit (IEC 60909) | Electromagnetic forces on busbars and electrode holders for Ch. 13 mechanical checks; switchgear duty | Transformer *u*_k; short-network geometry |
| Harmonics and flicker (IEC 61000-3-6/-3-7, NRS 048-2) | A SAF is a non-linear, fluctuating load; a higher power factor and new short-network geometry change the emissions | Furnace harmonic spectrum; grid impedance |
| Transformer thermal loading (IEC 60076-7) | AF-03: the transformers run at ≈ 100 % on load under C1 | Nameplate, cooling class, ambient, load cycle |
| Arc flash (IEEE 1584) and protection coordination | Safety of the secondary-circuit modifications | Protection settings, fault currents |

The Python model provides the **per-phase steady-state** analysis that the design decision needs now. ETAP becomes necessary at the detailed-design stage, once the impedance and grid data above are obtained.

### B.6 Increments and deliverables

| Inc. | Content | Deliverables | Depends on |
|---|---|---|---|
| **I1** | Data layer and provenance; electrical and production models; three "60 MW" scenarios; automated verification of every team calculation; Octave cross-validation; operating-envelope figures | `model/`, `matlab/`, `results/model/`, verification report | – |
| I2 | Least-squares mass balance; Cr recovery; slag and gas rates; Octave cross-validation | Mass-balance tables and Sankey figure | – |
| I3 | Energy balance (cited thermochemistry); preheat effect on SEC | Energy-balance tables and figures | Thermo data |
| I4 | Sensitivity (tornado and Monte-Carlo) and optimisation of the 450 t/d feasible region | Robustness figures | I1–I3 |
| I5 | Electrical deep-dive: PF-raising routes, electrode current against DC-04, ETAP study scope | Electrical chapter graphics | I1 |
| I6 | Parametric CAD: DXF plan and section drawings | `cad/` | Geometry assumptions |
| I7 | Power BI dataset, DAX and page specification | `powerbi/` | I1–I5 |
| I8 | Report and presentation pack: final figures, tables, methods appendix | `report/figures/`, appendix | All |

### B.7 Limitations stated up front

* No secondary-circuit electrical measurements exist. All currents and voltages are estimates (AF-08).
* No furnace dimensions exist in the plant data. CAD and geometry use literature analogues (A-16, A-19, A-20).
* No stream flow rates, temperatures of every stream, off-gas analysis or cooling-water data exist. The energy balance will therefore be a model with ranges, not a reconciled plant balance.
* MATLAB is represented here by **GNU Octave 8.4**. The scripts are written in the common subset and should run unchanged in MATLAB, but they must be confirmed in MATLAB by the team.
