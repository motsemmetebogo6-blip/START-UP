# DATA UPDATE NOTICE – supervisor data workbook now governs

**To:** all members · **From:** Tebogo Motsemme · **Date:** 2026-11-23

From today, the **Ferrochrome Data Workbook** (supervisor-confirmed) is our primary data source. **Where it differs from the earlier team pack, the workbook wins.** Values not in the workbook (electrode size, furnace geometry, HV voltage) still come from the Reference Furnace Specification.

| Item | Old team-pack value | **New value (workbook)** |
|---|---|---|
| Power factor | 0.846 | **0.93** (supervisor accepts ≤ 0.95) |
| Load factor | – | **0.95** (back-solved) |
| Mean active power | 55 MW | **57.43 MW** (on-load 60.45 MW) |
| Specific energy | 3.25 MWh/t | **3.5 MWh/t** |
| Production | 374 t/d | **393.65 t/d** actual; **450 t/d target** |
| Feed | LG6 concentrate, preheated | **80 % pellets + 20 % lumpy ore; sintered pellets charged cold** |
| Ore Cr₂O₃ / Cr/Fe | 44.2 % / 1.62 | **39.54 % (blend) / 1.41** |
| Alloy | typical range | **Cr 50.42, Fe 35.99, Si 3.64, C 6.71 %** |
| Slag | literature typical | **Cr₂O₃ 9.54, SiO₂ 27.23, Al₂O₃ 30.23, MgO 18.22, CaO 7.55 %; basicity 0.95** |
| Flux / reductants | – | **Quartz 55 % + limestone 45 %; coke 10 % + anthracite 54 % + 36 %** |

**What this means for each person:**
* **Jeff (Ch. 10, 13):** use PF 0.93. Moving to PF 0.95 needs R/X **+20 %** (not +51 %). The slag superheat is only ≈ 44 °C, so be careful when raising the electrode tips.
* **Mkhonto (Ch. 8):** the workbook's 78 % Cr recovery looks too low. Al₂O₃ and MgO tracers give **≈ 87 % and ≈ 1.1 t slag/t**. Please resolve this in the mass balance.
* **Ngesi (Ch. 9):** SEC 3.5 MWh/t is for **cold** pellets. Calculate the SEC for hot charging (≈ 500 °C) and for pre-reduced pellets (target 2.41).
* **Sibandze (Ch. 14, 15):** the preferred alternative is provisionally **C1 = 60 MW mean + hot charging (457 t/d)**. Please cost it against pre-reduction (P2).
* **Simphiwe (Ch. 3, 16, 17):** use the workbook feed and recipe in Ch. 3. Sensitivity inputs: PF 0.93–0.95, LF 0.95–0.972, SEC, recovery.

**Open question for the supervisor:** the brief says ≈ 55 MW but the data gives 57.43 MW mean. Is 55 MW the bath power (≈ 4 % circuit losses) or a rounded label?

The workbook is in the repository at `data/Ferrochrome_Data_Workbook.xlsx`. The calculations that read it are in `calcs/03_existing_condition_workbook.py`.
