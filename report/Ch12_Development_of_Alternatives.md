# Chapter 12 – Development of Alternatives

*Author: Tebogo Motsemme · Draft Rev A (screening stage) · Checked by: Simphiwe (pending)*
*Verification: `calcs/03_existing_condition_workbook.py` → `results/12_alternatives_screening.csv`, `results/12_alternatives_chart.png`.*
*Status: the technical screening is complete. The final selection needs costs (Sibandze, Ch. 15), the energy balance (Ngesi, Ch. 9) and the electrical and detailed checks (Jeff, Ch. 10 and 13).*

## 12.1 Objectives the alternatives must meet

1. **Electrical uprate:** raise the mean active power from 57.43 MW towards **60 MW** on the existing **65 MVA** transformers (project brief).
2. **Production:** reach the supervisor's target of **450 t/d** (DC-14), up from the present 393.65 t/d.
3. **Retain the existing furnace** (brownfield). Meet all acceptance criteria DC-01 to DC-15 (Chapter 4).

## 12.2 The governing relationship

Production at a fixed transformer rating is set by two levers:

**Production *M* (t/d) = *S* × PF × LF × 24 / SEC**

* **Electrical levers:** power factor PF and load factor LF. The rating *S* = 65 MVA is fixed.
* **Process lever:** specific energy SEC, reduced by charging hot and/or pre-reduced pellets.

**Key consequence (Chapter 7):** with SEC = 3.5 MWh/t, 450 t/d needs 65.6 MW mean, which exceeds even the on-load maximum (60.45 MW). The electrical levers alone therefore cannot meet the production target, and **SEC must fall to ≤ 3.20 MWh/t at 60 MW**.

## 12.3 Alternatives considered

| Code | Alternative | What changes | Basis |
|---|---|---|---|
| **E0** | Existing operation (reference) | – | Workbook |
| **E1** | Raise PF from 0.93 to 0.95 | R/X from 2.53 to 3.04 (**+20 %**) through electrode geometry (larger PCD, tip position) and/or lower short-network reactance | Supervisor PF limit 0.95 |
| **E2** | E1 plus load factor 0.95 → 0.972 | Fewer power interruptions (electrode slipping and breakage, tapping, trips) | Needed for 60 MW mean |
| **P1** | Hot charging of sintered pellets at ≈ 500 °C | SEC 3.5 → 3.15 MWh/t (−70 kWh/t per 100 °C) | R-04; A-24 (screening value) |
| **P2** | Hot-charged pre-reduced pellets, 40–50 % metallisation (Fe + Cr) | SEC 3.5 → 2.41 MWh/t | Workbook target |
| **C1** | **E2 + P1** | 60 MW mean and hot charging | Combination |
| **C2** | E2 + P2 | 60 MW mean and pre-reduction | Combination |

Options rejected at the outset:
* **Raising PF above 0.95:** outside the supervisor's accepted range.
* **A larger transformer:** outside the brief (65 MVA fixed).
* **HV-side shunt capacitors:** they improve the grid power factor but **do not** reduce the furnace transformer's MVA loading, so they cannot create extra MW at the furnace.

## 12.4 Technical screening results

| Code | Mean power (MW) | SEC (MWh/t) | Production (t/d) | Change | Meets 450 t/d? |
|---|---|---|---|---|---|
| E0 | 57.43 | 3.50 | 393.8 | – | No |
| E1 | 58.66 | 3.50 | 402.3 | +2.2 % | No |
| E2 | 60.00 | 3.50 | 411.4 | +4.5 % | No |
| P1 | 57.43 | 3.15 | 437.5 | +11.1 % | No (close) |
| P2 | 57.43 | 2.41 | 571.9 | +45.2 % | Yes |
| **C1** | **60.00** | **3.15** | **457.1** | **+16.1 %** | **Yes** |
| C2 | 60.00 | 2.41 | 597.5 | +51.7 % | Yes (upper bound) |

Example substitution for C1: *M* = 60.00 × 24 / 3.15 = **457.1 t/d**.

![Alternatives screening](../results/12_alternatives_chart.png)

**Reading the chart:** each curve is one power level. Moving left to right means lower specific energy. Only points above the red line meet the 450 t/d target. **The electrical uprate (E0 → E2) moves production up by only 4.5 %. The large gains come from lowering SEC.**

## 12.5 Qualitative evaluation (to be completed with cost and risk data)

| Criterion | E1/E2 Electrical uprate | P1 Hot charging | P2 Pre-reduction | **C1 (E2 + P1)** |
|---|---|---|---|---|
| Meets 60 MW brief | Yes (E2) | No | No | **Yes** |
| Meets 450 t/d | No | No (437) | Yes | **Yes (457)** |
| Infrastructure change | Short network, electrode settings, possibly transformer taps | Preheating kiln or shaft and hot transfer | Pre-reduction kiln (large new plant) | Short network + preheater |
| Technical maturity | Proven | Proven (closed-furnace preheaters) | Proven but complex | Proven |
| Capital cost (Ch. 15) | Low–medium | Medium | High | Medium |
| Main technical risk | Higher resistance raises the electrode tips; the slag superheat is only ≈ 44 °C (freezing risk) | Hot fines in a closed furnace (permeability, blow-outs) | Re-oxidation; metallisation control; high capex | Combined; each risk is manageable |
| Effect on auxiliaries (+% throughput) | +4.5 % | +11 % | +45 % (off-gas, tapping, slag handling probably limiting) | +16 % |
| Uses the 65 MVA transformers fully | Yes | Yes | Yes | Yes |

## 12.6 Preliminary recommendation

**C1 – electrical uprate to 60 MW mean (PF 0.95, LF 0.972) combined with hot charging of the sintered pellets** is the preferred alternative at this stage, because:
1. it is the **smallest change that meets both objectives** (60 MW and ≥ 450 t/d);
2. both elements use proven technology and keep the existing furnace;
3. its throughput increase (+16 %) stays within reach of the existing auxiliaries, whereas P2's +45 % would very likely overload the off-gas, tapping and slag systems.

**P2 (pre-reduction)** is kept as a **longer-term option** for the 480 t/d target, subject to the economic evaluation.

## 12.7 What must be confirmed before the selection is final

| Item | Who | Chapter |
|---|---|---|
| SEC reduction actually achievable by hot charging (temperature, A-24) | Ngesi | 9 |
| Electrode geometry and short-network changes giving R/X +20 % without cooling the hearth (slag superheat ≈ 44 °C) | Jeff | 10, 13 |
| Load factor 0.972: the realistic reduction in power-off time | Jeff, Ngesi | 10, 19 |
| Capital and operating costs, NPV of C1 against P2 | Sibandze | 15 |
| Capacity of the off-gas, tapping and cooling systems at +16 % | Jeff, Sibandze | 13, 14 |
| Sensitivity to PF, LF, SEC and recovery | Simphiwe | 16 |
