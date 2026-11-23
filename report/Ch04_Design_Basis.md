# Chapter 4 – Design Basis

*Author: Tebogo Motsemme · Draft Rev A · Checked by: Simphiwe (pending)*

## 4.1 Purpose

This chapter fixes the data, definitions, scenarios and acceptance criteria on which every calculation in this report is based. All chapters use the values given here. A value may change only through the change procedure in Section 4.9.

## 4.2 Hierarchy of data sources

Where sources disagree, the higher source in this list governs:

| Rank | Source | Tag | Examples |
|---|---|---|---|
| 1 | **Supervisor-confirmed plant data workbook** (*Ferrochrome Data Workbook*, Index, Assumptions, Recipe, Ore, Fluxes, Reductants, Metal and Slag sheets) | [WB] | PF 0.93, SEC 3.5 MWh/t, 393.65 t/d, ore, alloy and slag analyses |
| 2 | Project brief | [S] | 55 → 60 MW, 65 MVA, closed SAF, existing furnace |
| 3 | Published literature (reference register R-01 to R-20) | [L] | Electrode diameter, furnace geometry ratios, Westly C₃ |
| 4 | Documented assumptions (register A-01 to A-25) | [A] | HV supply voltage, hot-charging temperature |
| – | Calculated in this project (Python, `calcs/`) | [C] | Mean power, currents, ore blend, recovery check |

The workbook makes clear which of its values are **measured, supplied, assumed, calibrated, derived or targets**, and this report keeps that distinction. In particular, the **load factor is back-solved, not measured**, and **450 t/d is a target, not the current baseline**.

## 4.3 System boundary and power definitions

* **Boundary:** the **furnace electrical boundary**, i.e. the furnace transformers, secondary circuit, electrodes and furnace. The upstream sintering plant is excluded (workbook, specific energy note).
* **Transformer rating *S*:** 65 MVA total, a fixed physical constraint.
* **On-load active power:** *P*_on = *S* × PF.
* **Mean active power:** *P*_mean = *S* × PF × LF, where LF (load factor) is the fraction of time at full load. This is the power that sets daily production.
* **Specific electrical energy (SEC):** MWh per tonne of alloy at the furnace electrical boundary.
* **Daily production:** *M* = *P*_mean × 24 / SEC.

**The brief's "55 MW" against the data (open item, A-25).** The workbook gives *P*_mean = 57.43 MW, which reproduces the actual production (Chapter 7). The brief describes the furnace as operating at "approximately 55 MW". Two readings are possible:
* **Option A:** 55 MW is the power reaching the bath, so the secondary-circuit efficiency is 55 / 57.43 = 0.958. This lies inside the 0.94–0.98 range assumed earlier (A-06).
* **Option B:** 55 MW is a rounded nominal label.

Both lead to the same calculations, because **the workbook values are used throughout**. The reading will be confirmed with the supervisor.

## 4.4 Scenarios

| Scenario | Definition | Key values |
|---|---|---|
| **A – Existing** | Present operation, per the workbook | 65 MVA, PF 0.93, LF 0.95, *P*_mean 57.43 MW, SEC 3.5 MWh/t, 393.65 t/d, sintered pellets charged cold |
| **B – Electrical uprate** | 60 MW mean active power on the same 65 MVA | Requires PF × LF ≥ 60/65 = 0.923 (Chapter 12) |
| **Target T – Production** | 450 t/d (workbook target, not yet achieved) | Requires SEC ≤ 3.06 MWh/t at 57.43 MW, or ≤ 3.20 MWh/t at 60 MW |

**Comparison rule:** the same raw-material analyses, alloy grade and calculation methods are used in every scenario. Only the variables of each alternative change.

## 4.5 Design data – electrical and production [WB]

| Parameter | Value | Unit | Status in workbook |
|---|---|---|---|
| Transformer capacity | 65 | MVA | Assumed – fixed constraint |
| Power factor | 0.93 | – | Assumed – **accepted by supervisor; values ≤ 0.95 acceptable** |
| Load factor | 0.95 | – | Calibrated (back-solved from production) |
| Mean active power | 57.43 | MW | Derived (65 × 0.93 × 0.95) |
| Energy per day | 1378.3 | MWh/d | Derived |
| Specific energy, baseline | 3.5 | MWh/t alloy | Supplied – confirmed by supervisor |
| Production, baseline | 393.65 | t/d | Supplied – actual plant production (393.5–393.8) |
| Production target | 450 | t/d | Target – not currently achieved (bottleneck) |
| Higher production target | 480 | t/d | Target |
| SEC target | 2.41 | MWh/t | Target – hot-charged pre-reduced pellets |
| Pellet metallisation target | 40–50 | % | Target – metallisation counts Fe + Cr (confirmed 15 Nov 2026) |
| Pellet state, baseline | Sintered, charged cold | – | Supplied – 0 % metallised |
| Cr recovery, baseline | 78 | % | Assumed – **to be checked by the mass balance** (Chapter 7 §7.6 suggests ≈ 87 %) |
| Cr recovery, target | 93 | % | Target |

## 4.6 Design data – raw materials, alloy and slag [WB, measured means]

**Charge recipe (split within each group):** ore = 80 % pellets + 20 % small lumpy ore; flux = 55 % quartz + 45 % limestone; reductant = 10 % coke + 54 % anthracite 1 + 36 % anthracite 2. The group-to-group ratios (ore : flux : reductant) are **not given** and will come from the mass balance (Chapter 8).

| Ore (%) | Cr₂O₃ | FeO | Al₂O₃ | MgO | SiO₂ | CaO | TiO₂ | Cr/Fe |
|---|---|---|---|---|---|---|---|---|
| Pellets | 39.76 | 25.00 | 15.61 | 9.48 | 7.02 | 0.65 | 0.81 | 1.40 |
| Small lumpy ore | 38.65 | 23.25 | 15.51 | 11.05 | 9.02 | 1.17 | 0.74 | 1.47 |

| Flux (%) | SiO₂ | CaO | MgO | Al₂O₃ |
|---|---|---|---|---|
| Quartz | 96.88 | 0.03 | 0.07 | 1.00 |
| Limestone | 1.52 | 46.59 | 5.89 | 0.52 |

| Reductant (%) | Fixed carbon | Ash | Volatile matter | Total moisture | S (XRF) |
|---|---|---|---|---|---|
| Coke | 81.75 | 16.50 | 1.42 | 15.68 | 0.71 |
| Anthracite 1 | 82.02 | 14.06 | 3.52 | 6.45 | 0.24 |
| Anthracite 2 | 81.49 | 13.27 | 5.01 | 2.96 | 0.66 |

| Alloy (%) | Cr | Fe | Si | C | Ti | Mn | P | S | Liquidus | Tap temperature |
|---|---|---|---|---|---|---|---|---|---|---|
| Mean of 5 | 50.42 | 35.99 | 3.64 | 6.71 | 0.64 | 0.24 | 0.017 | 0.02 | 1550 °C | 1732 °C |

| Slag (%) | Al₂O₃ | CaO | Cr₂O₃ | FeO | MgO | SiO₂ | Basicity (CaO+MgO)/SiO₂ | Liquidus (FactSage) | In-furnace temperature |
|---|---|---|---|---|---|---|---|---|---|
| Mean of 5 | 30.23 | 7.55 | 9.54 | 5.80 | 18.22 | 27.23 | 0.95 | 1757 °C | 1800 °C |

**Data quality notes carried from the workbook:**
* The ore basis (as-received or dry) is unconfirmed.
* The anthracites' reported mean fixed carbon is **above** the maximum limit and their volatile matter is **below** the minimum limit.
* The small lumpy ore's mean SiO₂ (9.02 %) is below its minimum limit (9.50 %).
* Slag sample 2 has a negative superheat and sample 4 a negative spinel value (model artefacts).

The measured slag Cr₂O₃ (9.54 %) **replaces** the earlier supplied value of 15 %.

## 4.7 Design data not supplied in the workbook [L]/[A]

| Parameter | Value | Tag / source |
|---|---|---|
| Electrode type and diameter | Söderberg, 1.55 m | [L] R-11, R-13; A-02, A-16 |
| Pitch circle diameter / hearth diameter / shell inner diameter | 4.19 m / 10.88 m / 13.7 m | [L]/[A] R-11, R-16, R-17; A-19, A-20 |
| Westly C₃ (for electrode current) | 8.33 | [A] A-18 (R-13 calibration) |
| HV supply voltage | 132 kV (88 kV sensitivity) | [A] A-21 |
| Existing secondary tap range | 260–340 V | [A] A-23 (critical) |
| Auxiliary-plant design margin | 10 % | [A] A-22 (critical) |

## 4.8 Units, standards and acceptance criteria

**Units:** SI; MW, MVA, Mvar, kA, V, mΩ; MWh/t; °C; mass %.
**Standards:** IEC 60076-1 (power transformers); IEEE C57.17 (arc-furnace transformers); IEC 60909 (short-circuit currents); IEC 61000-3-6/-3-7 and NRS 048-2 (power quality, flagged only).

**Acceptance criteria** (updated for the workbook data; ◇ = provisional, to be justified by the responsible author):

| ID | Criterion | Acceptance limit |
|---|---|---|
| DC-01 | Transformer apparent power | *S* ≤ 65 MVA continuous |
| DC-02 | Power factor | 0.93 ≤ PF ≤ 0.95 (supervisor: ≤ 0.95 acceptable); PF × LF ≥ 0.923 for 60 MW mean |
| DC-03 | Secondary voltage | Within the transformer tap range with ≥ ±5 % control margin ◇ |
| DC-04 | Electrode current density | Not above the existing operating value ◇ |
| DC-05 | Electrode current | Not above the existing holder/clamp loading ◇ |
| DC-06 | Cooling-water heat removal | ≤ 90 % of design capacity ◇ |
| DC-07 | Refractory and shell | Within design heat flux and temperatures |
| DC-08 | Structural | Within rated loads |
| DC-09 | Cr recovery | Not lower than the baseline (recalculated in Chapter 8); target 93 % |
| DC-10 | Specific energy | ≤ 3.5 MWh/t; ≤ 3.20 MWh/t for 450 t/d at 60 MW |
| DC-11 | Off-gas, feed and tapping | Capacity ≥ the new production rate |
| DC-12 | Stability | Operation inside the stable control region |
| DC-13 | Economics | Positive NPV ◇ |
| DC-14 *(new)* | Production | ≥ 450 t/d (workbook target) |
| DC-15 *(new)* | Alloy quality | Cr, Si, C, S and P within the present ranges; slag superheat > 0 °C |

## 4.9 Change procedure

A change to any value in Sections 4.4 to 4.7 is recorded in the common assumptions register with the reason and the affected chapters. The Project Leader approves it and re-runs the calculations. No assumed or literature value may be presented as plant data.

## 4.10 Open items

1. **A-25:** meaning of the brief's 55 MW against the workbook's 57.43 MW mean (confirm with the supervisor).
2. **Cr recovery:** the workbook's 78 % is inconsistent with an oxide tracer balance (≈ 87 %, Chapter 7 §7.6). To be resolved in Chapter 8.
3. Ore basis (as-received or dry); the ore : flux : reductant ratios.
4. Electrical secondary data (voltage taps, electrode current) are not in the workbook, so the literature-based values in Section 4.7 remain.
