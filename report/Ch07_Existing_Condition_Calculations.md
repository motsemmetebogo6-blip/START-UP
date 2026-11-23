# Chapter 7 – Existing Condition Calculations

*Author: Tebogo Motsemme · Draft Rev A · Checked by: Simphiwe (pending)*
*Verification: `calcs/03_existing_condition_workbook.py`, which reads the data workbook directly. Results are in `results/07_existing_condition.csv`.*

## 7.1 Purpose

This chapter calculates the present (Scenario A) operating condition of the furnace from the supervisor-confirmed data. It checks the data for internal consistency and identifies the constraints that limit production. These numbers are the "before" picture against which every alternative in Chapter 12 is measured.

## 7.2 Electrical operating condition

**Inputs [WB]:** *S* = 65 MVA, PF = 0.93, LF = 0.95.

| Quantity | Equation and substitution | Result |
|---|---|---|
| Power-factor angle | φ = cos⁻¹(0.93) | 21.57° |
| On-load active power | *P*_on = *S* · PF = 65 × 0.93 | **60.45 MW** |
| On-load reactive power | *Q* = *S* · sin φ = 65 × 0.3676 | **23.89 Mvar** |
| Mean active power | *P*_mean = *S* · PF · LF = 65 × 0.93 × 0.95 | **57.43 MW** |
| Mean phase power | 57.43 / 3 | **19.14 MW** per electrode |
| Daily energy | 57.43 × 24 | **1378.3 MWh/d** |
| Transformer loading on load | *S* / *S*_rated | **100 %** |
| R/X ratio of the furnace circuit | PF / √(1 − PF²) = 0.93 / 0.3676 | **2.53** |
| Primary line current (132 kV supply, A-21) | 65 × 10⁶ / (√3 × 132 × 10³) | **284 A** (426 A at 88 kV) |

**Significance:**
1. **When on load, the furnace already uses the full 65 MVA and draws about 60.45 MW.** The average is lower (57.43 MW) because the furnace is on full load only 95 % of the time.
2. Average power can therefore only rise through a **higher power factor** (more MW per MVA) or a **higher load factor** (less time off load). The rating itself is fixed.
3. The supervisor accepts PF up to 0.95, so the maximum mean power with today's load factor is 65 × 0.95 × 0.95 = **58.66 MW**.

**Electrode current (assumption-based).** The workbook contains no secondary voltage or current data, so these are estimated from the literature calibration used throughout the project (Westly C₃ = 8.33, A-18; electrode diameter 1.55 m, A-16):

| Quantity | Equation and substitution | Result |
|---|---|---|
| Electrode current | *I* = C₃ · *P*_on^(2/3) = 8.33 × 60.45^(2/3) | **≈ 128 kA** |
| Secondary voltage (line) | *V* = *S* / (√3 · *I*) = 65 × 10⁶ / (√3 × 128.3 × 10³) | **≈ 293 V** |
| Operating resistance per phase | *R* = *P*_on / (3 *I*²) | **≈ 1.22 mΩ** |
| Reactance per phase | *X* = *R* · tan φ | **≈ 0.48 mΩ** |
| Electrode current density | *J* = *I* / (π *D*² / 4) = 128 300 / 18 869 | **≈ 6.8 A/cm²** |

These five values are **estimates**, not plant data, and will be replaced if secondary measurements become available. Jeff's electrical analysis (Chapter 10) refines them.

## 7.3 Production and energy

| Quantity | Equation and substitution | Result |
|---|---|---|
| Production from energy | *M* = *E* / SEC = 1378.3 / 3.5 | **393.8 t/d** |
| Production supplied (actual) | workbook | **393.65 t/d** |
| Difference | (393.79 − 393.65) / 393.65 | **+0.04 %** |
| Annual production | 393.65 × 365 | **143.7 kt/a** |
| SEC required for 450 t/d at present power | 1378.3 / 450 | **3.06 MWh/t** (−12.5 %) |
| Power required for 450 t/d at 3.5 MWh/t | 450 × 3.5 / 24 | **65.6 MW** (> 60.45 MW on-load maximum) |

**Significance:** the calculated and actual production agree to within 0.04 %. This confirms that **production is power-limited** at present: the furnace makes as much alloy as its energy input allows at 3.5 MWh/t. **450 t/d cannot be reached by power alone** on a 65 MVA supply (it would need 65.6 MW mean). It requires a lower specific energy.

## 7.4 Raw materials – ore blend

The ore blend is calculated from the 80 % pellet / 20 % lumpy-ore split:

*x*_blend = 0.80 · *x*_pellets + 0.20 · *x*_lumpy

| Oxide | Pellets | Lumpy | **Blend** |
|---|---|---|---|
| Cr₂O₃ | 39.76 | 38.65 | **39.54 %** |
| FeO | 25.00 | 23.25 | **24.65 %** |
| Al₂O₃ | 15.61 | 15.51 | **15.59 %** |
| MgO | 9.48 | 11.05 | **9.79 %** |
| SiO₂ | 7.02 | 9.02 | **7.42 %** |
| CaO | 0.65 | 1.17 | **0.75 %** |

Cr/Fe check (pellets): Cr = 39.76 × (2 × 52.00 / 151.99) = 27.20 %; Fe = 25.00 × (55.85 / 71.84) = 19.43 %; **Cr/Fe = 1.400** against the reported 1.40 ✔. The blend Cr/Fe is 1.41.

## 7.5 Alloy and slag

| Property | Value | Comment |
|---|---|---|
| Alloy Cr / Fe / Si / C | 50.42 / 35.99 / 3.64 / 6.71 % | Charge-chrome grade |
| Alloy Cr/Fe | 50.42 / 35.99 = **1.40** | Equal to the ore Cr/Fe |
| Alloy liquidus / tap temperature / superheat | 1550 / 1732 / **182 °C** | Ample metal superheat |
| Slag basicity (CaO + MgO)/SiO₂ | (7.55 + 18.22) / 27.23 = **0.946** | Reported 0.95 ✔ |
| Slag MgO/Al₂O₃ | 18.22 / 30.23 = **0.60** | |
| Slag liquidus (FactSage) / in-furnace temperature | 1757 / 1800 °C | Slag superheat ≈ **44 °C**, which is small |

**Significance:** the slag runs only about 44 °C above its liquidus, and one sample shows a negative superheat. Any alternative that makes the **lower furnace colder** (for example raising the electrode tips to increase resistance, Chapter 12 option E1) risks **slag freezing and tapping problems**. This is a key constraint for the electrode-geometry options.

## 7.6 Chromium recovery check

The workbook gives Cr recovery as 78 % (assumed) and notes that recovery should be an **output** of the balance. A simple check per tonne of alloy:

* Cr in alloy = 504.2 kg/t; Cr in ore blend = 39.54 % × 0.684 = 27.05 %; Cr in slag = 9.54 % × 0.684 = 6.53 %.
* **At 78 % recovery:** ore = 504.2 / (0.78 × 0.2705) = 2.39 t/t; Cr lost = 142 kg/t. If all the loss goes to slag, the slag = 142 / 0.0653 = **2.18 t/t**.
* **Al₂O₃ tracer (all Al₂O₃ from ore reports to slag):** slag/ore = 15.59 / 30.23 = 0.516. The Cr balance 0.2705 *m* = 504.2 + 0.0653 × 0.516 *m* gives *m* = 2.13 t ore/t, slag = **1.10 t/t** and recovery = **87.6 %**.
* **MgO tracer:** slag = 1.15 t/t, recovery = **87.0 %**.

**Significance:** the two independent tracers agree (≈ 87 %, ≈ 1.1 t slag/t). A slag rate of about 1.1 t/t is typical of charge-chrome practice, whereas 2.2 t/t is not. **The 78 % figure is therefore probably too low**, or it includes losses not in the slag (dust, metal entrained in slag). The tracer values are upper bounds because they ignore Al₂O₃ and MgO from reductant ash and flux, and dust losses. **This is passed to Mkhonto for the mass balance (Chapter 8)**, which will settle the recovery.

## 7.7 Summary of consistency checks

| Check | Result | Verdict |
|---|---|---|
| *P*_mean = 65 × 0.93 × 0.95 | 57.43 MW = workbook 57.43 | ✔ |
| Production from energy vs actual | 393.8 vs 393.65 t/d (0.04 %) | ✔ |
| Pellet Cr/Fe calculated vs reported | 1.400 vs 1.40 | ✔ |
| Slag basicity calculated vs reported | 0.946 vs 0.95 | ✔ |
| Cr recovery 78 % vs tracer balance | 78 % vs ≈ 87 % | ✘ **Inconsistent – to Chapter 8** |
| Brief "≈ 55 MW" vs data 57.43 MW | Ratio 0.958 | Open item A-25 |

## 7.8 Conclusions for the design

1. The furnace is **power-limited and fully loaded** on its 65 MVA transformers (100 % loading on load).
2. Mean power can rise only to **58.66 MW** at the supervisor's PF limit of 0.95. **60 MW mean also needs a load factor of 0.972.**
3. **450 t/d cannot be achieved by electrical means alone.** It needs SEC ≤ 3.06 MWh/t (at present power) or ≤ 3.20 MWh/t (at 60 MW).
4. The slag superheat is small (≈ 44 °C), which limits how far the electrode tips can be raised.
5. The recovery figure in the data needs correcting through the mass balance.
