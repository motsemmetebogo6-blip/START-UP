# CHAPTER 7 – EXISTING CONDITION CALCULATIONS

*Author: T. Motsemme · Revision B (academic draft) · Checked by: Simphiwe – pending*

## 7.1 Introduction

Before any modification can be evaluated, the existing operating condition must be quantified and the data on which it rests must be shown to be internally consistent. This chapter establishes the electrical, production and metallurgical state of the furnace in Scenario A (Chapter 4, Table 4.3). It also tests the plant data for consistency and identifies the constraints that currently limit production. The results form the reference against which every alternative in Chapter 12 is measured.

## 7.2 Method

All calculations follow the definitions in Section 4.5 and use the mean values of the plant data (Ferrochrome Data Workbook, 2026). To eliminate transcription errors, each calculation was reproduced independently in Python by a script that reads the data workbook directly (`calcs/03_existing_condition_workbook.py`). Quantities for which no plant data exist (the electrode current and the secondary voltage) are estimated from the scale-up relation of Westly (1974) and are identified as estimates. Three types of consistency check are applied: (i) agreement between derived and reported values; (ii) agreement between energy-based and reported production; and (iii) closure of a chromium balance using oxide tracers.

## 7.3 Electrical Operating Condition

With *S* = 65 MVA, PF = 0.93 and LF = 0.95, the power-factor angle is φ = cos⁻¹(0.93) = 21.57°. The on-load active and reactive powers then follow:

*P*~on~ = *S* · PF = 65 × 0.93 = 60.45 MW  (7.1)

*Q*~on~ = *S* · sin φ = 65 × 0.3676 = 23.89 Mvar  (7.2)

The mean active power and the daily energy are:

*P*~mean~ = *S* · PF · LF = 65 × 0.93 × 0.95 = 57.43 MW  (7.3)

*E*~d~ = 24 × 57.43 = 1378.3 MWh/d  (7.4)

The ratio of furnace resistance to circuit reactance, which governs the power factor of an SAF (Mulholland, 2009), is:

*R*/*X* = PF / √(1 − PF²) = 0.93 / 0.3676 = 2.53  (7.5)

Assuming a 132 kV supply (A-21), the primary line current at full rating is *I*₁ = *S* / (√3 · *V*~HV~) = 65 × 10⁶ / (√3 × 132 × 10³) = 284 A (426 A at 88 kV).

**Table 7.1:** Electrical operating condition, Scenario A

| Quantity | Symbol | Value |
|---|---|---|
| On-load active power | *P*~on~ | 60.45 MW |
| On-load reactive power | *Q*~on~ | 23.89 Mvar |
| Mean active power | *P*~mean~ | 57.43 MW |
| Mean power per phase | *P*~mean~/3 | 19.14 MW |
| Daily energy | *E*~d~ | 1378.3 MWh/d |
| Transformer loading on load | *S*/*S*~rated~ | 100 % |
| Resistance-to-reactance ratio | *R*/*X* | 2.53 |
| Primary line current (132 kV) | *I*₁ | 284 A |

The results show that **the furnace already operates at its full transformer rating whenever it is on load**, drawing approximately 60.45 MW. The mean power of 57.43 MW is lower only because the furnace is at full load for 95 % of the time. At a fixed rating, the mean power can therefore be increased only by raising the power factor, the load factor, or both. At the supervisor's upper limit of PF = 0.95 and the present load factor, the maximum mean power is 65 × 0.95 × 0.95 = 58.66 MW. A mean power of 60 MW would additionally require LF = 60/(65 × 0.95) = 0.972.

## 7.4 Estimated Secondary-Circuit Parameters

The plant data contain no secondary voltage or electrode current. These were therefore estimated from the relation of Westly (1974), *I* = C₃ · *P*^(2/3), with C₃ = 8.33 obtained by calibration on a published ferrochrome furnace of the same electrode diameter (*Finite element modelling of electric currents in AC submerged arc furnaces*, n.d.)†:

*I* = 8.33 × 60.45^(2/3) ≈ 128 kA  (7.6)

*V*~LL~ = *S* / (√3 · *I*) = 65 × 10⁶ / (√3 × 128.3 × 10³) ≈ 293 V  (7.7)

*R* = *P*~on~ / (3*I*²) ≈ 1.22 mΩ;  *X* = *R* · tan φ ≈ 0.48 mΩ  (7.8)

*J* = *I* / (π*D*²/4) = 128 300 / 18 869 ≈ 6.8 A/cm²  (7.9)

These values are of the correct order for large ferrochrome furnaces, but they rest on a similarity relation whose general validity has been questioned (ABM, 2007)†. They are therefore treated as estimates, refined in Chapter 10 and varied in Chapter 16.

## 7.5 Production and Specific Energy

Applying Equation (4.4) to the existing condition:

*M* = *E*~d~ / SEC = 1378.3 / 3.5 = 393.8 t/d  (7.10)

This agrees with the reported production of 393.65 t/d to within 0.04 % (Table 7.2).

**Table 7.2:** Production and specific energy, Scenario A

| Quantity | Value |
|---|---|
| Production calculated from energy (Eq. 7.10) | 393.8 t/d |
| Production reported (actual) | 393.65 t/d |
| Difference | +0.04 % |
| Annual production (365 d) | 143.7 kt/a |
| SEC required for 450 t/d at 57.43 MW | 1378.3/450 = 3.06 MWh/t (−12.5 %) |
| Mean power required for 450 t/d at 3.5 MWh/t | 450 × 3.5/24 = 65.6 MW |

The close agreement confirms that **production is limited by the electrical energy supplied**: at 3.5 MWh/t, the furnace produces as much alloy as its energy input permits. The final row of Table 7.2 is particularly significant. The mean power required to reach 450 t/d at the present specific energy (65.6 MW) exceeds even the on-load maximum of 60.45 MW. **The production target therefore cannot be met by electrical measures alone**, and a reduction in specific energy is required.

## 7.6 Raw Material Blend

The mean ore composition fed to the furnace is the recipe-weighted mean of the pellet and lumpy-ore analyses:

*x*~blend~ = 0.80 · *x*~pellets~ + 0.20 · *x*~lumpy~  (7.11)

**Table 7.3:** Ore blend composition (mass %)

| Component | Pellets | Lumpy ore | Blend |
|---|---|---|---|
| Cr₂O₃ | 39.76 | 38.65 | 39.54 |
| FeO | 25.00 | 23.25 | 24.65 |
| Al₂O₃ | 15.61 | 15.51 | 15.59 |
| MgO | 9.48 | 11.05 | 9.79 |
| SiO₂ | 7.02 | 9.02 | 7.42 |
| CaO | 0.65 | 1.17 | 0.75 |

As a check, the pellet Cr/Fe ratio is recalculated from the oxide analyses: Cr = 39.76 × (2 × 52.00/151.99) = 27.20 %, and Fe = 25.00 × (55.85/71.84) = 19.43 %. This gives Cr/Fe = 1.400, in exact agreement with the reported value of 1.40. The Cr/Fe ratio of the blend is 1.41.

## 7.7 Alloy and Slag Characteristics

The mean alloy contains 50.42 % Cr, 35.99 % Fe, 3.64 % Si and 6.71 % C, which is typical of South African charge-grade ferrochrome. The alloy Cr/Fe ratio (1.40) equals that of the ore. The alloy is tapped at 1732 °C, giving a metal superheat of 182 °C above its liquidus of 1550 °C.

The slag basicity is recalculated as (CaO + MgO)/SiO₂ = (7.55 + 18.22)/27.23 = 0.946, which agrees with the reported 0.95. The MgO/Al₂O₃ ratio is 0.60. The slag liquidus predicted by FactSage (1757 °C) lies only about **44 °C** below the estimated in-furnace slag temperature (1800 °C), and one of the five samples has a negative superheat. The slag therefore operates with a narrow thermal margin. This has a direct design consequence. Any modification that reduces the heat input to the lower furnace, such as raising the electrode tips to increase the operating resistance, risks slag freezing and tapping difficulties (Mulholland, 2009)†. This constraint is carried forward to the evaluation of alternatives.

## 7.8 Chromium Recovery: Mass-Balance Check

The plant data give a baseline chromium recovery of 78 %, which is an assumed value. The data themselves note that recovery should be an *output* of the mass balance (Ferrochrome Data Workbook, 2026). The value is tested here using a simplified balance per tonne of alloy. The Cr content of the alloy is 504.2 kg/t, that of the ore blend 39.54 × 0.684 = 27.05 %, and that of the slag 9.54 × 0.684 = 6.53 %.

**(a) At the assumed 78 % recovery.** The ore requirement is 504.2/(0.78 × 0.2705) = 2.39 t/t. The chromium lost is 142 kg/t. If all of this loss reports to the slag, the slag rate would be 142/0.0653 = **2.18 t/t**.

**(b) Oxide-tracer balance.** If all the Al₂O₃ in the ore reports to the slag, the slag-to-ore ratio is 15.59/30.23 = 0.516. The chromium balance is then:

0.2705 *m* = 504.2 + 0.0653 × 0.516 *m*  (7.12)

This gives an ore requirement of *m* = 2.13 t/t, a slag rate of **1.10 t/t** and a recovery of **87.6 %**. Repeating the calculation with MgO as the tracer gives 1.15 t/t and 87.0 %.

The two independent tracers agree closely, and a slag rate of about 1.1 t/t is consistent with charge-chrome practice, whereas 2.2 t/t is not. The assumed recovery of 78 % is therefore unlikely to be correct, unless it includes substantial losses outside the slag, such as dust or metal entrained in the slag. The tracer results are upper bounds, because they neglect the Al₂O₃ and MgO contributed by reductant ash and flux. The chromium recovery is resolved in the full mass balance (Chapter 8).

## 7.9 Validation of the Data Set

**Table 7.4:** Summary of consistency checks

| Check | Calculated | Reported | Verdict |
|---|---|---|---|
| Mean active power (Eq. 7.3) | 57.43 MW | 57.43 MW | Consistent |
| Production from energy (Eq. 7.10) | 393.8 t/d | 393.65 t/d | Consistent (0.04 %) |
| Pellet Cr/Fe | 1.400 | 1.40 | Consistent |
| Slag basicity | 0.946 | 0.95 | Consistent |
| Chromium recovery | ≈ 87 % (tracer) | 78 % (assumed) | **Inconsistent** – referred to Chapter 8 |
| Brief vs data power | 57.43 MW | ≈ 55 MW | Open item A-25 (Chapter 4) |

## 7.10 Discussion: Constraints Governing the Existing Furnace

Four constraints emerge from the analysis:
1. **Electrical.** The transformers are fully loaded on load, so the furnace is power-limited rather than capacity-limited. The only electrical levers are the power factor (capped at 0.95) and the load factor.
2. **Energetic.** The present specific energy of 3.5 MWh/t reflects the charging of cold sintered pellets. The production target requires this to fall to ≤ 3.06 MWh/t at present power, or ≤ 3.20 MWh/t at 60 MW.
3. **Thermal.** The slag superheat of about 44 °C limits any strategy that shifts heat away from the hearth.
4. **Metallurgical.** The chromium recovery is uncertain and must be established before the benefits of any alternative can be valued.

## 7.11 Summary

The existing furnace operates at 57.43 MW mean (60.45 MW on load) on its fully loaded 65 MVA transformers. It produces 393.65 t/d of alloy at 3.5 MWh/t. The plant data are internally consistent except for the assumed chromium recovery, which an oxide-tracer balance places at about 87 %. The analysis shows that the 450 t/d target cannot be reached by an electrical uprate alone, and that the slag's narrow thermal margin constrains electrode-based measures. These findings define the problem addressed in Chapter 12.

## References

ABM (2007) 'Correlação entre tensão ideal, potência e diâmetro de eletrodos nos fornos a arco submerso – fator J', *Proceedings of the Associação Brasileira de Metalurgia, Materiais e Mineração*. São Paulo: ABM.†

Ferrochrome Data Workbook (2026) *Ferrochrome smelting – data workbook: consolidated plant inputs, charge recipe, raw materials, metal, slag and process assumptions*. Unpublished plant data set supplied by the project supervisor.

*Finite element modelling of electric currents in AC submerged arc furnaces* (n.d.) [Author and source to be confirmed; available via ResearchGate, publication 30509695.]†

Mulholland, A.C. (2009) 'The effectiveness of current control of submerged arc furnace electrode penetration in selected scenarios', *Journal of the Southern African Institute of Mining and Metallurgy*, 109(10).†

Westly, J. (1974) 'Resistance and heat distribution in a submerged-arc furnace', *Proceedings of the First International Ferro-Alloys Congress (INFACON 74)*. Johannesburg: SAIMM.†

† Consulted at abstract level; to be verified against the full text before submission (reference register, document 05).
