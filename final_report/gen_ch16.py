import csv
R='/home/user/START-UP/results/model/'
n0=lambda x:f"{float(x):,.0f}".replace(',',' ')
torn=list(csv.DictReader(open(R+'CH16_npv_tornado.csv')))
names={'price_usd':('Alloy price','US$1 200 to 1 800/t'),'save':('Hot-charging saving','0.035 to 0.070 MWh/t per 100 K'),'fx':('Exchange rate','R16.00 to 18.50 per US$'),
'disc':('Discount rate','10 to 14 %'),'LF':('Load factor achieved','0.95 to 0.98'),'PF':('Power factor achieved','0.93 to 0.95'),'capex_core':('Capital cost','-20 % to +40 %'),
'ore_price':('Ore price','R2 400 to 3 200/t'),'ore_rate':('Ore rate','2.14 to 2.39 t/t'),'elec':('Electricity tariff','R1.45 to 1.85/kWh'),'red_price':('Reductant price','R2 400 to 3 200/t')}
t4=['| Rank | Assumption | Range tested | NPV at low end (R M) | NPV at high end (R M) | Swing (R M) |','|---|---|---|---|---|---|']
for i,r in enumerate(torn,1):
    nm,rg=names[r['key']]
    t4.append(f"| {i} | {nm} | {rg} | {n0(r['NPV_at_low_RM'])} | {n0(r['NPV_at_high_RM'])} | {n0(r['swing_RM'])} |")
comp=list(csv.DictReader(open(R+'CH16_comparison.csv')))
t7=['| Case | Mean power (MW) | SEC (MWh/t) | Production (t/d) | 450 t/d met | Auxiliary use | NPV (R M) | IRR (%) | Payback (y) |','|---|---|---|---|---|---|---|---|---|']
cn={'Alloy price US$1 200/t':'Alloy price US$1 200/t','Capital cost +40 %':'Capital cost +40 %'}
for r in comp:
    t7.append(f"| {r['case']} | {float(r['P_mean_MW']):.2f} | {float(r['SEC_MWh_t']):.3f} | {float(r['production_tpd']):.1f} | {'Yes' if r['meets_450']=='YES' else 'No'} | {float(r['aux_util_pct_(10%_margin)']):.0f} % | {n0(r['NPV_RM'])} | {float(r['IRR_pct']):.1f} | {float(r['payback_y']):.2f} |")
pfrows=[]
for pf in (0.88,0.90,0.92,0.923,0.93,0.95):
    a=60/pf; b=60/0.972/pf
    pfrows.append(f"| {pf:.3f} | {a:.2f} | {100*a/65:.1f} % | {b:.2f} | {100*b/65:.1f} % |")
md=f'''# Purpose

This chapter shows how changing specific design assumptions affects the technical feasibility and the economic performance of the proposed furnace uprating. It tests whether the increase from 57.43 MW to 60 MW mean power remains feasible under varying conditions of the key electrical, operational and economic parameters, for the selected design C1: a 60 MW mean power on the existing 65 MVA transformers combined with hot charging of the pellets. Three questions are answered. Which assumptions have the greatest effect on the project net present value (NPV)? How do the electrical system and the auxiliary systems (cooling water, off-gas, feed, tapping and slag handling) respond? Under which conditions does the recommendation change?

# Methodology

A one-variable-at-a-time approach was used. Each selected parameter is varied within an approved range while the remaining inputs are held at their reference values. The procedure was:

1. Establish the 60 MW operating condition (C1) as the reference case.
2. Obtain the baseline assumptions from the common assumptions register (Chapter 5).
3. Define lower and upper sensitivity limits for each parameter (Table 16.2, assumption A-28).
4. Recalculate the relevant outputs, including the electrical, operating and economic results.
5. Compare the results with the project acceptance criteria of Chapter 4.
6. Determine which parameters have the greatest influence on both feasibility and project returns.

The results are presented as comparison tables and graphs, a tornado chart that ranks the effect of each assumption on the project NPV, and separate technical plots that show the change in electrical performance and in auxiliary-system performance. The economic model follows the method of Chapter 15. It is updated with the reconciled mass balance of Chapter 8 (ore 2.144 t/t, reductant 0.433 t/t, flux 0.366 t/t) and with the conservative production of C1, in which the preheat is measured from ambient temperature. The base-case NPV was also calculated independently in MATLAB and the two results agree to 2 × 10⁻¹⁵.

# Critical sensitivity parameters

Seven parameters were identified for investigation. Table 16.1 states the reference assumption of each, what is assessed, and the principal result.

::: {{custom-style="Table Caption"}}
Table 16.1: Critical sensitivity parameters
:::

| Parameter | Reference assumption | Sensitivity assessment | Principal result |
|---|---|---|---|
| A-22: Auxiliary margin | 10 % design margin | Effect on the capacity of the cooling-water, off-gas and feed systems | At least 28 % spare capacity is needed to stay below 90 % utilisation |
| A-23: Transformer tap range | Existing range 260-340 V (assumed); indicative requirement 280-400 V | Ability to achieve the required secondary voltage | Estimated 288 V at C1, inside the assumed range |
| A-17: Reactance reduction | 20 % reduction | Effect on power factor and transformer loading | PF must reach 0.95; at 0.93 production is 445 t/d |
| A-18: Current calibration | C₃ = 8.33 (range 6-11) | Effect on estimated electrode current and current density | Existing electrode current spans 92 to 169 kA |
| A-04: Specific energy | 3.5 MWh/t measured; 3.0-3.5 investigation range; 3.17 MWh/t with hot charging | Effect on production and electricity consumption | ±2 % on the cold-charge value gives 445 to 465 t/d |
| A-06: Electrical efficiency | 0.94-0.98 (0.958 implied by the brief) | Effect of electrical losses on energy utilisation | Carried in the power factor and load factor cases |
| Electricity price | R1.65/kWh | Effect on operating cost and NPV | NPV changes by only R45 M over R1.45 to 1.85/kWh |

# Parameters and ranges tested for the NPV

::: {{custom-style="Table Caption"}}
Table 16.2: Parameters investigated and their ranges
:::

| Parameter | Base value | Range tested | Basis |
|---|---|---|---|
| Alloy price | US$1 500/t | US$1 200 to 1 800/t | Chapter 15 (SMM benchmark) |
| Hot-charging saving | 0.070 MWh/t per 100 K | 0.035 to 0.070 | Vendor rule (Metso), half to full |
| Exchange rate | R17.42 per US$ | R16.00 to 18.50 | Chapter 15 |
| Discount rate | 12 % | 10 to 14 % | Chapter 15 |
| Load factor achieved | 0.972 | 0.95 to 0.98 | C1 requires 0.972 |
| Power factor achieved | 0.95 | 0.93 to 0.95 | Supervisor limit 0.95 |
| Capital cost | R310 M plus 20 % contingency | -20 % to +40 % | Accuracy of the Chapter 14 estimate |
| Ore price | R2 800/t | R2 400 to 3 200/t | Chapter 15 |
| Ore rate | 2.144 t/t (reconciled) | 2.144 to 2.39 t/t | 2.39 t/t if the recovery were 78 % |
| Electricity tariff | R1.65/kWh | R1.45 to 1.85/kWh | Chapter 15, Eskom tariff path |
| Reductant price | R2 800/t | R2 400 to 3 200/t | Chapter 15 |
| Auxiliary design margin (A-22) | 10 % | 5 to 20 % | Technical plot only (Figure 16.4) |

# Base case

::: {{custom-style="Table Caption"}}
Table 16.3: Base case of the economic model
:::

| Quantity | Updated base | Chapter 15 basis, reproduced |
|---|---|---|
| C1 production | 454.8 t/d | 457.3 t/d |
| Extra alloy | 22 311 t/yr | 23 233 t/yr |
| Incremental revenue | R583.0 M/yr | R607.1 M/yr |
| Incremental operating cost | R214.5 M/yr | R222.0 M/yr |
| Incremental profit before tax | R368.5 M/yr | R385.1 M/yr |
| Total investment | R402.0 M | R402.0 M |
| After-tax cash flow | R276.2 M/yr | R288.3 M/yr |
| **NPV (15 years, 12 %)** | **R1 479 M** | R1 562 M |
| IRR | 68.7 % | 71.7 % |
| Payback after tax | 1.46 years | 1.39 years |

When the model uses the production and rates of Chapter 15 it reproduces that chapter, which reports a profit of about R383 M, an NPV of about R1 540 M and an IRR of about 70 %, to within 1.5 %. The updated base is about R60 M lower in NPV because it uses the conservative production of 454.8 t/d instead of 457.1 t/d and the reconciled ore, reductant and flux rates.

# Economic sensitivity: tornado chart

![](../../report/figures/F12_npv_tornado.png){{width=6.2in}}

::: {{custom-style="Figure Caption"}}
Figure 16.1: Tornado chart ranking the effect of each assumption on the project NPV.
:::

::: {{custom-style="Table Caption"}}
Table 16.4: NPV at the limits of each range, ranked by swing
:::

{chr(10).join(t4)}

![](../../report/figures/F13_npv_spider.png){{width=5.4in}}

::: {{custom-style="Figure Caption"}}
Figure 16.2: Spider plot of the NPV against the percentage change in each input. The lines for the alloy price and the exchange rate coincide because both act only through the revenue.
:::

The results show the following.

* **The market dominates the economics.** The alloy price, and with it the exchange rate, has the largest effect. The NPV nevertheless stays positive across the whole range. It falls to zero only at an alloy price of US$734/t, about half of the current benchmark. This is higher than the break-even of about US$550/t in Chapter 15, because that value covers only the operating cost while the NPV break-even also recovers the capital.
* **The hot-charging saving is the largest technical uncertainty.** If only half of the vendor saving is achieved, the NPV falls by R761 M and production drops to 432 t/d, which fails the 450 t/d requirement.
* **The project is not sensitive to the capital cost or the electricity tariff.** The core capital cost would have to rise to about R1 620 M, more than five times the estimate, before the NPV became zero. A change of R0.20/kWh in the tariff moves the NPV by less than R25 M.
* **Operating discipline has real value.** The load factor and the power factor achieved together swing the NPV by more than R550 M, which justifies the electrode-reliability and short-network work.

# Electrical sensitivity: power factor and transformer loading

The transformer apparent power requirement is calculated from:

::: {{custom-style="Equation"}}
S = P / PF  (16.1)
:::

where S is the apparent power (MVA), P the active power (MW) and PF the power factor. For 60 MW while on load at a power factor of 0.923, S = 60 / 0.923 = 65 MVA, which uses the full installed transformer capacity. Because the furnace is on load only 97.2 % of the time at C1, the power while on load is 60 / 0.972 = 61.73 MW, and the apparent power is 61.73 / 0.95 = 64.98 MVA at PF 0.95. The effect of the power factor on the transformer loading is shown in Figure 16.3 and Table 16.5.

![](../../report/figures/F14_electrical_sensitivity.png){{width=6.2in}}

::: {{custom-style="Figure Caption"}}
Figure 16.3: Electrical sensitivity. Left: on-load transformer loading against power factor. Right: mean active power against load factor.
:::

::: {{custom-style="Table Caption"}}
Table 16.5: Transformer loading against power factor
:::

| Power factor | S for 60 MW on load (MVA) | Loading | S for 60 MW mean at LF 0.972 (MVA) | Loading |
|---|---|---|---|---|
{chr(10).join(pfrows)}

Varying the data shows that a lower power factor raises the apparent power and can overload the transformers. The power factor of about 0.923 is the minimum for 60 MW while on load, with no excess transformer load. For 60 MW mean power at a load factor of 0.972, the transformers reach their 65 MVA rating on load at exactly PF 0.95, so there is no headroom if the power factor falls. At a power factor of 0.93, even a load factor of 0.99 does not reach 60 MW mean. The electrical uprate is therefore governed by two operating parameters that must both reach their limits: PF = 0.95 and LF of at least 0.972.

# Auxiliary-system sensitivity

![](../../report/figures/F15_auxiliary_sensitivity.png){{width=6.2in}}

::: {{custom-style="Figure Caption"}}
Figure 16.4: Auxiliary-system sensitivity. Left: utilisation against production for design margins of 5 to 20 %. Right: off-gas and slag duty against production.
:::

The consumption and generation rates per tonne of alloy are fixed by the chemistry (Chapter 8), so every auxiliary duty rises in proportion to production, by 15.5 % at C1. The off-gas rises from 9 797 to 11 315 Nm³/h, the slag from 468 to 540 t/d and the ore from 844 to 975 t/d. Whether the auxiliary systems can carry this depends on their design margin (A-22), which is not known.

::: {{custom-style="Table Caption"}}
Table 16.6: Auxiliary utilisation at C1 production
:::

| Design margin over the existing duty | Utilisation at C1 | Criterion DC-06 (not above 90 %) |
|---|---|---|
| 5 % | 110 % | Fails |
| 10 % (assumed) | 105 % | Fails |
| 15 % | 100 % | Fails |
| 20 % | 96 % | Fails |
| 28 % or more | 90 % or less | Passes |

Unless the existing cooling-water, off-gas, slag-handling and ore-handling systems were designed with at least 28 % spare capacity, they must be upgraded for C1. This confirms the R30 M auxiliary allowance of Chapter 14 as essential, and makes a survey of the actual capacities a priority.

# Technical and financial effects of the selected parameters

The selected parameters affect the electrical performance, the auxiliary-system performance, the production and energy consumption, and the economic performance of the proposed design:

* *Electrical performance:* the reactive compensation achieved, the transformer tap range and the electrode calibration decide what operating point the system can reach, how much load can be put through the transformer and how the electrodes are loaded.
* *Auxiliary-system performance:* the design margin decides whether the cooling-water, off-gas and feed systems need upgrades.
* *Production and energy consumption:* the specific energy per tonne of alloy decides the electrical energy used and therefore the production.
* *Economic performance:* the electricity price and the electrical efficiency decide the operating cost of the extra tonnes and whether the added value justifies the cost of the uprate.

The sensitivity analysis therefore evaluates both the technical limitations and the economic implications. Achieving 60 MW electrically shows that the uprate is technically possible, but it does not by itself show that the project is economically justified. The overall feasibility is also decided by the auxiliary systems: if they cannot carry the additional duty, the extra electrical power cannot be used.

# Combined comparison of key cases

::: {{custom-style="Table Caption"}}
Table 16.7: Technical and economic comparison of key sensitivity cases
:::

{chr(10).join(t7)}

# Conclusions

1. **The project is economically robust.** The NPV is positive in every case tested. Break-even needs an alloy price below US$734/t or a capital cost more than five times the estimate.
2. **The project is technically fragile against the production target.** Three single deviations each cause the 450 t/d requirement to fail: a hot-charging saving that is only half the vendor value, a load factor that stays at 0.95, and a power factor that stays at 0.93. The production target, not the economics, is the binding requirement.
3. **The power factor must reach 0.95.** Below this the transformers would be overloaded at 60 MW mean power.
4. **Auxiliary upgrades are required** unless the existing systems have at least 28 % spare capacity.
5. **Recommended actions:** a plant trial to measure the actual hot-charging saving before capital is released, power-quality metering to confirm the achievable power factor, an availability plan to reach the load factor of 0.972, and a survey of the actual auxiliary-system capacities.
'''
open('/home/user/START-UP/final_report/md/ch16_sensitivity_analysis.md','w',encoding='utf8').write(md)
print('ok',len(md))
