# Purpose and use of the register

Every value in this report that is neither measured in the plant nor fixed by the project brief is an assumption. This chapter lists those assumptions in one register so that they can be reviewed, challenged and replaced as better information becomes available. The register follows the hierarchy of Chapter 4: supervisor-confirmed plant data govern, the brief ranks next, literature values follow, and documented assumptions are used only where nothing higher is available. Calculated values carry the tag [C], assumptions the tag [A].

Each assumption is given a confidence rating: **H** (supported by several sources), **M** (one credible source or an engineering convention) or **L** (weak, to be verified or tested by sensitivity analysis). The last column states whether the assumption is still open, has been replaced by plant data, or has been closed.

# Technical assumptions

::: {custom-style="Table Caption"}
Table 5.1: Register of technical assumptions
:::

| ID | Assumption and value | Basis | Conf. | Status |
|---|---|---|---|---|
| A-01 | Product is high-carbon ferrochrome from South African chromite (Cr 50-55 %, C 6-8 %, Si 2-6 %) | Typical closed-furnace product | M | Replaced by the measured alloy analyses (Cr 50.4 %, Fe 36.0 %, Si 3.6 %, C 6.7 %) |
| A-02 | Electrodes are self-baking Søderberg electrodes | Standard for large South African closed ferrochrome furnaces | H | Confirmed in the design basis |
| A-03 | 65 MVA is the total installed transformer rating | Project brief, confirmed by the project leader | H | Closed |
| A-04 | Specific energy 3.0-3.5 MWh/t with preheated feed, about 4 MWh/t with cold mixed feed | Literature range for pelletised and preheated feed | M | Revised: the plant value of 3.5 MWh/t governs, 3.15 MWh/t is the hot-charging target |
| A-05 | Baseline power factor 0.80-0.85 | Typical value for ferrochrome furnaces | M | Superseded by the workbook value of 0.93, which is itself an assumption and must be metered |
| A-06 | Secondary-circuit electrical efficiency 0.94-0.98 | Engineering judgement; 0.958 is implied by 55 MW against 57.43 MW | L | Open, tested in Chapter 16 |
| A-07 | Electrode current density must not exceed the existing furnace value (estimated 6.80 A/cm² at 57.43 MW) | Published furnace data and the principle that proven operation is the limit | L-M | Revised, acceptance criterion DC-04 |
| A-08 | Westly relation I = C₃ P^(2/3) applies equally at 57.43 and 60 MW | Classical similarity | L-M | Cross-check only, never the sole basis |
| A-09 | Furnace utilisation 90-95 % of calendar time | Engineering judgement | L | Superseded by the calibrated load factor of 0.95 and the 0.972 required by C1 |
| A-10 | Pitch circle diameter to electrode diameter ratio 2.5-3.0 | Literature range | L | Superseded by A-19 |
| A-11 | The 55 and 60 MW are active power delivered into the furnace | The brief does not define the measurement point | M | Retained; HV-metered power treated as a sensitivity case |
| A-12 | Feed blend, reductant, slag chemistry and product grade are unchanged between the existing and the uprated furnace | Isolates the effect of the uprate | H | Retained as a method |
| A-13 | Furnace shell, hearth and roof are retained | Project brief | H | Closed |
| A-14 | The existing furnace already operates on the full 65 MVA | PF 0.93 and LF 0.95 reproduce 57.43 MW and 393.65 t/d | H | Confirmed by the plant data |
| A-15 | Grid frequency 50 Hz | South African grid | H | Closed |
| A-16 | Electrode diameter 1.55 m | Published South African furnaces of this size | M | Retained |
| A-17 | Achievable reactance reduction 20 % (about 29 % in the short network) | About 70 % of furnace reactance lies in the short network | L | Open, tested in Chapter 16 |
| A-18 | Westly constant C₃ = 8.33 (range 6-11) | One analogue furnace, within the reported range | M | Electrode current, voltage and current density are estimates |
| A-19 | Pitch circle diameter ratio 2.70 | Mid-point of 2.44 and 3.0 in the literature | M | Retained |
| A-20 | Hearth diameter to pitch circle diameter ratio 2.60 | Mid-point of 2.55 and 2.67 in the literature | M | Retained |
| A-21 | HV supply voltage 132 kV (88 kV as a sensitivity case) | Typical supply levels; no plant data | L | Open |
| A-22 | Auxiliary systems have a 10 % design margin over the present duty | Engineering judgement; no plant data | L, critical | Open, tested in Chapter 16 |
| A-23 | Existing secondary tap range 260-340 V; indicative requirement 280-400 V | Engineering judgement around the estimated voltage; no plant data | L, critical | Open, to be confirmed from the transformer nameplate |
| A-24 | Hot charging at about 500 °C saves 0.07 MWh/t per 100 K of preheat | Vendor rule of thumb (Metso, n.d.) | L, critical | Open, to be measured in a plant trial (Chapters 8 and 16) |
| A-25 | The brief's "approximately 55 MW" differs from the data value of 57.43 MW | Brief against plant data | M | The plant data are adopted as the baseline |
| A-26 | Reductant proximate analyses are on a dry basis | Not stated in the data | L-M | Open; if as received, the dry reductant rate is about 6 % lower |
| A-27 | Monte Carlo distributions: hot-charge saving uniform 0.035-0.070 MWh/t per 100 K; temperature 500 ± 50 °C; load factor triangular (0.95, 0.972, 0.98); power factor triangular (0.93, 0.95, 0.95); cold-charge specific energy normal (3.5, standard deviation 0.035) | Engineering judgement | L | To be replaced by trial data |
| A-28 | Ranges of the sensitivity analysis (Table 16.1) | Engineering judgement and the estimate accuracy of Chapter 14 | M | Retained |

# Economic assumptions

The economic assumptions of Chapter 15 are carried unchanged into the sensitivity analysis of Chapter 16. All are estimates and are marked [A] in Chapter 15.

::: {custom-style="Table Caption"}
Table 5.2: Economic assumptions
:::

| Item | Value | Where varied |
|---|---|---|
| Alloy price | US$1 500/t net | Chapter 16, US$1 200-1 800/t |
| Exchange rate | R17.42 per US$ | Chapter 16, R16.00-18.50 |
| Electricity | R1.65/kWh | Chapter 16, R1.45-1.85 |
| Chrome ore | R2 800/t | Chapter 16, R2 400-3 200 |
| Reductant | R2 800/t | Chapter 16, R2 400-3 200 |
| Flux | R700/t | Held constant |
| Electrode paste | R16 500/t | Held constant |
| Maintenance | 1.5 % of capital plus R2 M per year | Held constant |
| Capital estimate | R310 M plus 20 % contingency and R30 M shutdown loss | Chapter 16, -20 % to +40 % |
| Company tax | 27 %, straight-line depreciation over 15 years | Held constant |
| Discount rate and life | 12 % over 15 years | Chapter 16, 10-14 % |

# Critical assumptions

Four assumptions decide whether the design is Retained, Optimised or Upgraded, and each is tested in this report. The hot-charging saving (A-24) decides whether 450 t/d can be reached, and is varied in Chapters 8 and 16. The auxiliary design margin (A-22) and the secondary tap range (A-23) decide the scope of the equipment upgrades, and the achievable reactance reduction (A-17) decides the power factor. The baseline power factor of 0.93 is not measured and must be confirmed by metering before capital is committed, which is why the implementation plan of Chapter 19 contains a measurement gate.
