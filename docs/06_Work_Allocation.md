# WORK ALLOCATION: WHO DOES WHAT (Rev 3 – balanced)

**Project:** Design and Scale-Up of a Closed Ferrochrome SAF from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Tebogo Motsemme (Project Leader)
**Document:** 06 (Rev 3), 2026-11-18. **Replaces all previous allocations.**
**Governs:** where documents 00 to 05 name a lead for a chapter, **this document takes precedence**.

---

## 1. Final allocation

| Member | Lead chapters | Effort points* |
|---|---|---|
| **Tebogo Motsemme** | 2 Problem definition · 12 Development of alternatives · 15 Economic evaluation | **7** |
| **Jeff** | 7 Existing condition calculations · 10 Electrical analysis | **6** |
| **Mkhonto** | 5 Assumptions · 6 Literature review (editor) · 8 Mass balance | **6** |
| **Ngesi** | 9 Energy balance · 11 Process/metallurgical analysis · 19 Implementation plan | **6** |
| **Sibandze** | 4 Design basis · 13 Detailed calculations · 14 Equipment/design requirements | **7** |
| **Simphiwe** | 3 Existing process description · 16 Sensitivity analysis · 17 Risk assessment | **6** |
| **Report compiler** | 1 Executive summary · 18 Recommended design · 20 Conclusion | not counted |

\*Effort points per chapter: Low = 1, Medium = 2, High = 3, Very high = 4. The 17 member chapters total 38 points, split **6–7 per person** (38 ÷ 6 cannot be exact).

**Chapters 1, 18 and 20** are written by the **report compiler** during final integration, once all other chapters are complete. They summarise the members' results and are not counted in anyone's load.

**Everyone also:**
* writes **one literature sub-section** for Chapter 6 (Section 4);
* gives Simphiwe **three risks** for Chapter 17 and the **input ranges** from their own chapter for Chapter 16;
* checks one other member's work (Section 5).

**Tebogo additionally** keeps the common registers and Python calculations, runs the gate reviews, builds the Power BI dashboard and compiles the Appendices (leader duties, not counted).

---

## 2. All chapters at a glance

| Ch. | Section | Lead | Supported by | Effort | Gate |
|---|---|---|---|---|---|
| 1 | Executive summary | Compiler | All | – | G6 |
| 2 | Problem definition | **Tebogo** | – | Low (1) | G1 |
| 3 | Existing process description | **Simphiwe** | Mkhonto (chemistry), Jeff | Medium (2) | G1 |
| 4 | Design basis | **Sibandze** | Tebogo | Medium (2) | G1 |
| 5 | Assumptions | **Mkhonto** | Everyone sends new assumptions to Tebogo for the register | Low (1) | G1 |
| 6 | Literature review | **Mkhonto** (editor) | Everyone writes one sub-section | Medium (2) | G2 |
| 7 | Existing condition calculations | **Jeff** | Sibandze | Medium (2) | G1 |
| 8 | Mass balance | **Mkhonto** | Ngesi | High (3) | G3 |
| 9 | Energy balance | **Ngesi** | Mkhonto (mass balance), Sibandze (heat losses) | High (3) | G3 |
| 10 | Electrical analysis (incl. electrodes) | **Jeff** | – | Very high (4) | G3 |
| 11 | Process/metallurgical analysis | **Ngesi** | Mkhonto | Medium (2) | G3 |
| 12 | Development of alternatives | **Tebogo** | Jeff, Ngesi | High (3) | G3 |
| 13 | Detailed calculations | **Sibandze** | Jeff (13.1 electrical), Ngesi (13.4 metallurgical) | High (3) | G3 |
| 14 | Equipment/design requirements | **Sibandze** | All | Medium (2) | G4 |
| 15 | Economic evaluation | **Tebogo** | Mkhonto, Ngesi (production), Sibandze (upgrade list) | High (3) | G5 |
| 16 | Sensitivity analysis | **Simphiwe** | All (input ranges); Tebogo (Python model) | Medium (2) | G5 |
| 17 | Risk assessment | **Simphiwe** | All (three risks each) | Medium (2) | G5 |
| 18 | Recommended design | Compiler | All | – | G5 |
| 19 | Implementation plan | **Ngesi** | Sibandze | Low (1) | G6 |
| 20 | Conclusion | Compiler | – | – | G6 |
| – | References | **Mkhonto** (as literature editor) | All | – | G6 |
| – | Appendices | **Tebogo** | All | – | G6 |

---

## 3. Task cards

### Tebogo Motsemme – Ch. 2, 12, 15 (+ leader duties)
* **Ch. 2 Problem definition:** the governing question; brownfield philosophy (retain, optimise, verify); constraints; why 65 MVA forces PF ≥ 0.923.
* **Ch. 12 Development of alternatives:** compare **B0** (raise resistance only; needs 367 V, so a transformer upgrade), **B20** (reactance −20 % plus resistance +21 %), **B30** (mainly reduce reactance), PCD options (PCD/D 2.7 to 3.0), and "do nothing / maximum MW". Comparison matrix against DC-01 to DC-13, cost and risk; justified choice.
* **Ch. 15 Economic evaluation:** capital cost of the Upgrade items; value of the extra production (about +34 t/d); extra electricity, reductant and paste costs; NPV, payback and IRR.
* **Read first:** docs 00 and 02; R-02, R-14, R-15, R-05; cost data gaps G-08, G-09.
* **First step:** set the gate dates (Section 7) and define the alternatives and evaluation criteria.

### Jeff – Ch. 7, 10
* **Ch. 7 Existing condition calculations:** the 55 MW baseline in report form (from doc 03): electrical operating point, transformer currents, electrode current density, geometry, production, consistency checks. Close the open items (hearth depth, tap-holes).
* **Ch. 10 Electrical analysis:** equivalent circuit; transformer loading; operating chart; reactance breakdown (check the implied 16 % transformer reactance); losses; electrode current density; how PCD and electrode tip position give the required +21 % resistance; paste consumption.
* **Hands over:** required R, X, current and voltage to Tebogo, Sibandze and Ngesi (by G2).
* **Read first:** **R-13** (most important), R-01, R-02, R-14, R-15, R-08, R-09.
* **First step:** confirm the 48 MW / 1.55 m / 110 kA values in R-13; review docs 02 and 03.

### Mkhonto – Ch. 5, 6, 8 (+ References)
* **Ch. 5 Assumptions:** the full assumptions table from the common register, with an explanation of the four critical assumptions (A-17, A-18, A-22, A-23). Coordinate with Tebogo, who keeps the master register.
* **Ch. 6 Literature review:** edit the six sub-sections into one critical review, and write sub-section 6.1 yourself. Make sure sources are compared, not just summarised.
* **Ch. 8 Mass balance:** per tonne of alloy, then per day at 55 and 60 MW; Cr, Fe, Si, C and O balances; alloy, slag and off-gas; Cr recovery; reductant requirement.
* **References:** one Harvard-style list of every source used (from doc 05).
* **Hands over:** mass balance to Ngesi for the energy balance (early in G3); production, slag and off-gas volumes to Tebogo and Sibandze.
* **Read first:** doc 05 (whole), **R-18** (confirm the feed analysis), R-19, R-20; find R-10 (alloy specification).
* **First step:** send each member their literature sub-section and a deadline; confirm the LG6 analysis.

### Ngesi – Ch. 9, 11, 19
* **Ch. 9 Energy balance:** calculate the specific energy (MWh/t) instead of assuming it; reaction heats; sensible heat of alloy, slag and gas; heat losses (from Sibandze); preheating effect; 55 vs 60 MW.
* **Ch. 11 Process/metallurgical analysis:** slag chemistry (basicity 0.83, MgO/Al₂O₃ 0.88); slag–metal separation; Cr recovery; the effect of shallower electrode tips; product quality.
* **Ch. 19 Implementation plan:** equipment ordering; shutdown and installation; commissioning; power raised in steps 55 → 57.5 → 60 MW with hold points; KPIs to monitor.
* **Hands over:** specific energy and heat to cooling water to Sibandze and Tebogo (by G3).
* **Read first:** R-04, R-05, R-07, R-19, R-20; thermodynamic data (gap G-07).
* **First step:** set up the energy-balance method and the thermodynamic data while Mkhonto starts the mass balance.

### Sibandze – Ch. 4, 13, 14
* **Ch. 4 Design basis:** Scenario A and Scenario B; units; standards (IEC 60076-1, IEEE C57.17, IEC 60909, NRS 048-2); acceptance criteria DC-01 to DC-13 with justified limits.
* **Ch. 13 Detailed calculations for the chosen alternative:** thermal (cooling-water heat removal, refractory heat flux, hearth power density 0.59 → 0.65 MW/m²) and mechanical (shell, roof, electrode holders, conductor forces). Collect Jeff's 13.1 and Ngesi's 13.4. End each section with a pass/fail verdict.
* **Ch. 14 Equipment/design requirements:** the final Retain/Optimise/Upgrade table (EQ-01 to EQ-13) and a specification for each upgrade.
* **Hands over:** heat losses to Ngesi (Ch. 9); the upgrade list to Tebogo, Ngesi and Simphiwe (by G4).
* **Read first:** R-11, R-16, R-17; refractory and cooling data (gaps G-04 to G-06); standards.
* **First step:** draft Chapter 4 and propose the cooling (DC-06) and refractory (DC-07) limits.

### Simphiwe – Ch. 3, 16, 17
* **Ch. 3 Existing process description:** the reference 55 MW furnace and its process; main reduction reactions; furnace construction (shell, lining, roof, three Söderberg electrodes, transformers, short network); feed, product and slag; auxiliaries; block flow diagram and electrode layout on the pitch circle. Chemistry agreed with Mkhonto.
* **Ch. 16 Sensitivity analysis:** vary the critical assumptions (A-22 auxiliary margin, A-23 tap range, A-17 reactance reduction, A-18 C₃, A-04 SEC, electricity price); tornado chart; the conditions under which the decision changes. Tebogo supplies the Python model.
* **Ch. 17 Risk assessment:** the risk register (likelihood × consequence → score, mitigation, owner, residual risk), including the **water-leak explosion hazard**, roof/gas blow-outs, electrode breakage, tap-hole failure, transformer overloading, control instability, Cr recovery loss, cost and schedule risks. Collect three risks from each member.
* **Read first:** docs 00 and 03; R-02, R-06, R-11.
* **First step:** draft Chapter 3 from doc 03 and send the team the risk-register template.

### Report compiler – Ch. 1, 18, 20
Written at final integration, after all other chapters are checked:
* **Ch. 18 Recommended design:** the chosen design in one place: operating point (MW, MVA, PF, kA, V), electrode geometry, upgrades, performance, and how each acceptance criterion is met (from Ch. 12–17).
* **Ch. 20 Conclusion:** answers the governing question directly.
* **Ch. 1 Executive summary:** 1–2 pages covering the problem, approach, key numbers, recommendation, cost, risks and decision.

---

## 4. Literature review (Chapter 6): one sub-section each

| Sub-section | Topic | Writer | Main sources |
|---|---|---|---|
| 6.1 | Ferrochrome production and closed-furnace technology | Mkhonto | R-05, R-06, R-07, R-18 |
| 6.2 | SAF electrical theory: resistance, reactance, PF, Westly scale-up | Jeff | R-01, R-02, R-03, R-12, R-13, R-14 |
| 6.3 | Söderberg electrodes, current density and furnace geometry | Ngesi | R-08, R-09, R-16, R-17 |
| 6.4 | Refractory, cooling and heat losses | Sibandze | R-11 + gaps G-04 to G-06 |
| 6.5 | Furnace safety and risk in closed SAFs | Simphiwe | R-06, R-11 + safety literature |
| 6.6 | Brownfield uprating and economic evaluation of furnace upgrades | Tebogo | R-15 + gaps G-08, G-09 |
| – | Editing and critical comparison | Mkhonto | All |

---

## 5. Checking pairs

| Author | Checked by | Why this pair |
|---|---|---|
| Jeff (7, 10) | Sibandze | Sibandze uses Jeff's electrical results in Ch. 13 |
| Sibandze (4, 13, 14) | Jeff | Jeff supplies section 13.1 |
| Mkhonto (5, 6, 8) | Ngesi | Ngesi's energy balance is built on the mass balance |
| Ngesi (9, 11, 19) | Mkhonto | Mkhonto supplies the mass balance |
| Tebogo (2, 12, 15) | Simphiwe | Simphiwe's sensitivity analysis tests Tebogo's economics and choice |
| Simphiwe (3, 16, 17) | Tebogo | Tebogo supplies the Python model for Ch. 16 |

---

## 6. Who hands what to whom

| From | To | What | By gate |
|---|---|---|---|
| Tebogo | All | Frozen baseline (doc 03), registers, this allocation | G1 |
| Jeff | Tebogo, Sibandze, Ngesi | Required R, X, current, voltage; electrode tip position and PCD | G2 / G3 |
| Mkhonto | Ngesi | Mass balance (alloy, slag, gas per tonne) | early G3 |
| Mkhonto, Ngesi | Tebogo, Sibandze | Production rate, slag and off-gas volumes, specific energy | G3 |
| Sibandze | Ngesi | Heat losses (cooling water, shell, roof) | G3 |
| Tebogo | Sibandze, Simphiwe, Ngesi | Chosen alternative (Ch. 12) | G3 |
| Sibandze | Tebogo, Ngesi, Simphiwe | Final upgrade list (Retain/Optimise/Upgrade) | G4 |
| Everyone | Simphiwe | Three risks each; sensitivity input ranges | G5 |
| All members | Compiler | Checked chapters for Ch. 1, 18, 20 | G5 / G6 |

---

## 7. Gate dates (to be set by Tebogo)

| Gate | What is due | Date |
|---|---|---|
| G0 | Everyone accepts this allocation | ____ |
| G1 | Ch. 2, 3, 4, 5, 7 drafts; baseline frozen | ____ |
| G2 | Ch. 6 sub-sections; each person presents their method | ____ |
| G3 | Ch. 8 to 13 calculated and checked | ____ |
| G4 | Ch. 14; one integrated design | ____ |
| G5 | Ch. 15 to 17; feasibility decision | ____ |
| G6 | Ch. 19, References, Appendices; compiler writes Ch. 1, 18, 20; final report | ____ |

**Rules reminder:** use the common numbers (doc 04 §2); tag every number [S]/[L]/[A]/[C]; send new assumptions to Tebogo; never present assumed values as plant data; if 60 MW doesn't work for your part, say so. That is a valid result.
