# WORK ALLOCATION: WHO DOES WHAT

**Project:** Design and Scale-Up of a Closed Ferrochrome SAF from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Tebogo (Project Leader)
**Document:** 06 (Rev 0), 2026-11-18
**This document replaces the member codes M1–M6 used in documents 00 to 05 with names** (see Section 6).

---

## 1. The team and their chapters

| Name | Role | Report chapters (lead) | Effort points* | Checks the work of |
|---|---|---|---|---|
| **Tebogo** | Project Leader; integration; Power BI dashboard | 1, 2, 4, 18, 20 + Power BI + final editing | 12 | Everyone (final sign-off) |
| **Mkhonto** | Electrical and electrode engineer | 10, 12 | 7 | Jeff (Ch. 7) |
| **Ngesi** | Metallurgist: mass and energy balances | 8, 9, 11 | 8 | Sibandze (Ch. 15) |
| **Jeff** | Furnace, thermal and mechanical engineer | 7, 13, 14 | 7 | Mkhonto (Ch. 10) |
| **Sibandze** | Literature review editor; economics; sensitivity | 6, 15, 16 | 7 | Ngesi (Ch. 8, 9) |
| **Simphiwe** | Process description, assumptions, risk, implementation, references | 3, 5, 17, 19, References, Appendices | 8 (lower difficulty) | – (Tebogo checks her work) |

\*Effort points: Low = 1, Medium = 2, High = 3, Very high = 4. Everyone also writes one short literature sub-section (Section 4). Simphiwe has the same number of points as the others, but her chapters are **descriptive or template-based** rather than heavy calculation.

---

## 2. All 20 sections at a glance

| Ch. | Section | Lead | Supported by | Effort | Gate | Start from |
|---|---|---|---|---|---|---|
| 1 | Executive summary | **Tebogo** | All | Low (1) | G6 | Written last, from Ch. 18 |
| 2 | Problem definition | **Tebogo** | – | Low (1) | G1 | Doc 00 §0–2 |
| 3 | Existing process description | **Simphiwe** | Ngesi, Jeff | Medium (2) | G1 | Doc 03 §2 and §5 |
| 4 | Design basis | **Tebogo** | – | Medium (2) | G1 | Doc 00 §6–7, doc 01 |
| 5 | Assumptions | **Simphiwe** | All send new ones to Tebogo | Low (1) | G1 | Common Registers (Excel) |
| 6 | Literature review | **Sibandze** (editor) | Everyone writes a sub-section | Medium (2) | G2 | Doc 05 |
| 7 | Existing condition calculations | **Jeff** | Mkhonto | Medium (2) | G1 | Doc 03 (almost complete) |
| 8 | Mass balance | **Ngesi** | – | High (3) | G3 | Doc 03 §5, refs R-18 to R-20 |
| 9 | Energy balance | **Ngesi** | Jeff (heat losses) | High (3) | G3 | A-04, refs R-04, R-05, R-07 |
| 10 | Electrical analysis (incl. electrodes) | **Mkhonto** | – | Very high (4) | G3 | Doc 02 (preliminary results) |
| 11 | Process/metallurgical analysis | **Ngesi** | Mkhonto (electrode tips) | Medium (2) | G3 | Ch. 8 and 9 |
| 12 | Development of alternatives | **Mkhonto** | Tebogo | High (3) | G3 | Doc 02 cases B0/B20/B30 |
| 13 | Detailed calculations (thermal, mechanical) | **Jeff** | Mkhonto (13.1), Ngesi (13.4) | High (3) | G3 | All chapters 8–12 |
| 14 | Equipment/design requirements | **Jeff** | All | Medium (2) | G4 | Equipment register |
| 15 | Economic evaluation | **Sibandze** | Ngesi (production) | High (3) | G5 | Upgrade list in Ch. 14 |
| 16 | Sensitivity analysis | **Sibandze** | Tebogo (Python) | Medium (2) | G5 | Critical assumptions A-04, A-17, A-18, A-22, A-23 |
| 17 | Risk assessment | **Simphiwe** | Jeff (safety), all | Medium (2) | G5 | Template in Section 3 below |
| 18 | Recommended design | **Tebogo** | All | Medium (2) | G5 | Ch. 12–17 |
| 19 | Implementation plan | **Simphiwe** | Jeff, Mkhonto | Low (1) | G6 | Doc 00 §13, Ch. 14 |
| 20 | Conclusion | **Tebogo** | – | Low (1) | G6 | Written last |
| – | References | **Simphiwe** | All | Low (1) | G6 | Doc 05, reference register |
| – | Appendices | **Simphiwe** | Tebogo (calculation printouts) | Low (1) | G6 | `calcs/`, `results/`, registers |

---

## 3. Task cards: what each person does

### Tebogo – Project Leader (Ch. 1, 2, 4, 18, 20 + Power BI + integration)
* **Do:** write the problem definition and design basis first (G1). Keep the common registers and Python calculations up to date. Run the gate reviews. Build the Power BI dashboard (pages 01 Overview, 02 Electrical, 05 Feasibility, 06 Data provenance). Integrate everything into the recommended design. Write the executive summary and conclusion **last**.
* **Read:** R-02, R-14, and all others for the audit.
* **You receive from:** everyone (all interface results).
* **First step:** set the gate dates in Section 7 and send this document with the team pack.

### Mkhonto – Electrical and electrodes (Ch. 10, 12)
* **Do:** Chapter 10 has two halves:
  * **Electrical (10.1–10.5):** equivalent circuit; transformer loading (PF ≥ 0.923); operating chart; reactance breakdown (check the implied 16 % transformer reactance); losses and efficiency.
  * **Electrodes (10.6–10.9):** current density; how PCD and electrode tip position change the resistance (show how to get the required +21 %); paste consumption.
  * **Chapter 12:** compare the alternatives B0, B20, B30, different PCDs, and "do nothing / maximum MW", then justify the choice.
* **Read first:** R-13 (most important), R-01, R-02, R-14, R-15, then R-03, R-08, R-09, R-12, R-16, R-17.
* **Hand over:** required R, X, I and V to Jeff and Ngesi (by G2); electrode tip position to Jeff and Ngesi (by G3).
* **First step:** confirm the 48 MW / 1.55 m / 110 kA values in R-13, then review doc 02.

### Ngesi – Metallurgy (Ch. 8, 9, 11)
* **Do:** Chapter 8 is the mass balance: per tonne of alloy, then per day at 55 and 60 MW; Cr, Fe, Si, C and O balances; slag and off-gas; Cr recovery. Chapter 9 is the energy balance: calculate the specific energy (MWh/t) instead of assuming it, and include the preheating effect. Chapter 11 covers slag chemistry, slag–metal separation, Cr recovery and the effect of shallower electrode tips.
* **Read first:** R-18 (check the feed analysis), R-19, R-20, R-04, R-05, R-07; find R-10 (alloy specification) and thermodynamic data (gap G-07).
* **Hand over:** production rate, slag and off-gas volumes to Jeff and Sibandze (by G3); heat to cooling water to Jeff.
* **First step:** confirm the LG6 analysis in R-18 and find a charge-chrome alloy specification.

### Jeff – Furnace, thermal and mechanical (Ch. 7, 13, 14)
* **Do:** Chapter 7 writes up the 55 MW baseline calculations from doc 03 (mostly done; turn it into report form and close the open items: hearth depth, tap-holes, roof). Chapter 13 covers the detailed calculations for the chosen design: thermal (cooling-water heat removal, refractory heat flux, hearth power density 0.59 → 0.65 MW/m²) and mechanical (shell, roof, electrode holders, conductor forces), and collects Mkhonto's and Ngesi's 60 MW results. Chapter 14 is the final Retain/Optimise/Upgrade table and specifications for the upgrades.
* **Read first:** R-11, R-16, R-17; find refractory and cooling data (gaps G-04 to G-06).
* **Hand over:** the upgrade list to Sibandze (economics) and Simphiwe (implementation, risk) by G4.
* **First step:** read doc 03 (Reference Furnace Specification) and propose acceptance limits for cooling (DC-06) and refractory (DC-07).

### Sibandze – Literature, economics, sensitivity (Ch. 6, 15, 16)
* **Do:** Chapter 6: collect everyone's literature sub-sections and turn them into one critical review (Section 4). Chapter 15: capital cost of the upgrades, the value of the extra production (about +34 t/d), extra running costs, then NPV, payback and IRR. Chapter 16: vary the critical assumptions (auxiliary margin, tap range, reactance reduction, C₃, SEC, electricity price) and show which ones change the decision (tornado chart).
* **Read first:** doc 05 (the whole literature map), R-05; find cost and price data (gaps G-08, G-09).
* **You receive:** production from Ngesi; the upgrade list from Jeff.
* **First step:** set up the Chapter 6 outline and send each member the deadline for their sub-section.

### Simphiwe – Description, assumptions, risk, implementation, references (Ch. 3, 5, 17, 19, References, Appendices)
Simphiwe's chapters mostly use material that already exists, so she can follow these steps.
* **Chapter 3 – Existing process description:**
  1. Read doc 03, Sections 2 and 5.
  2. Describe the process in words: chromite pellets + reductant + flux → closed furnace → alloy + slag + gas.
  3. Draw a simple block flow diagram (boxes and arrows) and a top-view sketch of the three electrodes on the pitch circle.
  4. Add a table of the feed and slag compositions (copy from doc 03).
  5. Ask Ngesi to check the chemistry.
* **Chapter 5 – Assumptions:** copy the Assumptions sheet from the Common Registers Excel into a report table. Write one paragraph explaining the four critical assumptions (A-17, A-18, A-22, A-23). Before submitting, ask Tebogo for the latest register.
* **Chapter 17 – Risk assessment:** use this template. Ask Jeff for help with the safety risks.

| Risk | Cause | Likelihood (1–5) | Consequence (1–5) | Risk score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| Water leak into the furnace | Cooling panel failure | … | 5 | … | … | Jeff |

* **Chapter 17 (continued):** include at least: water leak (explosion hazard); roof or gas blow-out; electrode breakage; tap-hole failure; transformer overloading; unstable electrode control; lower Cr recovery; cost overrun; shutdown taking longer than planned.
* **Chapter 19 – Implementation plan:** a step-by-step list of how the upgrade would be done: (1) order the equipment; (2) shutdown and install; (3) commission; (4) raise power in steps 55 → 57.5 → 60 MW, with checks at each step; (5) monitor the KPIs (MVA loading, power factor, electrode current, cooling temperatures, Cr recovery, energy use). Use Jeff's upgrade list (Ch. 14).
* **References:** keep one Harvard-style list of every source used, based on doc 05. Check that every R-number cited in the report is on the list.
* **Appendices:** collect the calculation printouts (from Tebogo), the registers and the drawings in order.
* **Read:** doc 03, doc 05, R-06, R-11.
* **First step:** start Chapter 3. It needs only doc 03.

---

## 4. Literature review (Chapter 6): one sub-section each

| Sub-section | Topic | Writer | Main sources |
|---|---|---|---|
| 6.1 | Ferrochrome production and closed-furnace technology | Ngesi | R-05, R-06, R-07, R-18 |
| 6.2 | SAF electrical theory: resistance, reactance, PF, Westly scale-up | Mkhonto | R-01, R-02, R-03, R-12, R-14 |
| 6.3 | Söderberg electrodes, current density, PCD | Mkhonto | R-08, R-09, R-13, R-16, R-17 |
| 6.4 | Refractory, cooling and heat losses | Jeff | R-11 + gaps G-04 to G-06 |
| 6.5 | Brownfield furnace uprating and process description | Simphiwe | R-06, R-11 |
| 6.6 | Economic evaluation of furnace upgrades | Sibandze | Gaps G-08, G-09 |
| – | Editing, linking, critical comparison | Sibandze | All |

Each sub-section is about 1–2 pages. **Compare** the sources and say where they disagree; don't just summarise them.

---

## 5. Who hands what to whom

| From | To | What | By gate |
|---|---|---|---|
| Tebogo | All | Frozen baseline (doc 03) and registers | G1 |
| Mkhonto | Jeff, Ngesi | Required R, X, current and voltage for 60 MW | G2 |
| Mkhonto | Jeff, Ngesi | Electrode tip position and PCD | G3 |
| Ngesi | Jeff | Heat to cooling water, off-gas volume | G3 |
| Ngesi | Sibandze | Production rate at 55 and 60 MW, energy use | G3 |
| Jeff | Sibandze, Simphiwe | Final upgrade list (Retain/Optimise/Upgrade) | G4 |
| Everyone | Simphiwe | Sources used (for References) | G6 |
| Everyone | Tebogo | New assumptions, as soon as they arise | Ongoing |

---

## 6. Name replaces member code (for documents 00 to 05)

| Code in docs 00–05 | Now |
|---|---|
| PL – Project Leader | Tebogo |
| M1 – furnace / mechanical | Jeff |
| M2 – electrical | Mkhonto |
| M3 – electrodes | Mkhonto |
| M4 – thermal / refractory | Jeff (risk assessment moves to Simphiwe) |
| M5 – metallurgy | Ngesi |
| M6 – Power BI / integration | Tebogo |
| M6 – economics / sensitivity | Sibandze |
| (new) – description, assumptions, risk, implementation, references | Simphiwe |

---

## 7. Gate dates (to be set by Tebogo)

| Gate | What is due | Date |
|---|---|---|
| G0 | Everyone confirms they have read the team pack and accept their chapters | ____ |
| G1 | Ch. 2, 3, 4, 5, 7 drafts; baseline frozen | ____ |
| G2 | Ch. 6 sub-sections; each person presents their method | ____ |
| G3 | Ch. 8 to 13 calculated and checked | ____ |
| G4 | Ch. 14; one integrated design | ____ |
| G5 | Ch. 15 to 18; feasibility decision | ____ |
| G6 | Ch. 1, 19, 20, References, Appendices; final report | ____ |

**Rules reminder:** use the common numbers (doc 04 §2); tag every number [S]/[L]/[A]/[C]; send new assumptions to Tebogo; never present assumed values as plant data; if 60 MW doesn't work for your part, say so. That is a valid result.
