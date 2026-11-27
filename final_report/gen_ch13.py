import sys, math
sys.path.insert(0,'/home/user/START-UP/model')
import run_sensitivity_ch16 as m
B=m.BASE; e=m.economics(B)
S,PF,LF,SEC0,s,T,Tr=65.0,0.95,0.972,3.5,0.07,500.0,25.0
P=60.0; Pon=P/LF; Son=Pon/PF
sec=SEC0-s*(T-Tr)/100; E=24*P; M=E/sec; secreq=E/450
Tstar=Tr+100*(SEC0-24*S*PF*LF/450)/s
dt=e['dt']
el=(e['P_mean']-S*0.93*0.95)*8760*B['elec']/1e3
ore=dt*B['ore_rate']*B['ore_price']/1e6; red=dt*B['red_rate']*B['red_price']/1e6
flux=dt*B['flux_rate']*B['flux_price']/1e6; paste=dt*B['paste_kg']/1000*B['paste_price']/1e6; mnt=0.015*B['capex_core']+2.0
tax=B['tax']*(e['profit']-e['capex']/B['years']); ann=(1-(1+B['disc'])**-B['years'])/B['disc']
f=lambda x,n=1:f"{x:,.{n}f}".replace(',',' ')
alt=lambda sec_:(24*60/sec_)
md=f'''# Purpose and basis

This chapter documents the calculations behind the recommended alternative C1: a mean power of 60 MW at a power factor of 0.95 and a load factor of 0.972, combined with hot charging of the pellets at about 500 °C. Every value was calculated in the verified Python model and repeated in MATLAB (GNU Octave), and the same calculations are available in the accompanying Excel workbook. The inputs and their provenance are listed in Table 13.1.

::: {{custom-style="Table Caption"}}
Table 13.1: Inputs to the detailed calculations
:::

| Input | Symbol | Value | Provenance |
|---|---|---|---|
| Transformer rating | S | 65 MVA | [WB], [S] |
| Power factor | PF | 0.95 | Supervisor limit |
| Load factor required | LF | 0.972 | [C] from Chapter 12 |
| Specific energy, cold charge | SEC₀ | 3.50 MWh/t | [WB] |
| Hot-charging saving | s | 0.070 MWh/t per 100 K | [A], A-24 |
| Preheat temperature | T | 500 °C | [A], A-24 |
| Reference temperature | T_ref | 25 °C (ambient) | [A] |
| Existing production | M₀ | 393.65 t/d | [WB] |
| Production requirement | M_req | 450 t/d | [S] |
| Electrode diameter | D | 1.55 m | [A], A-16 |
| Westly constant | C₃ | 8.33 | [A], A-18 |
| HV supply voltage | V_HV | 132 kV | [A], A-21 |

# Electrical operating point

Equations (10.1) to (10.6) of Chapter 10 give the operating point of C1.

::: {{custom-style="Equation"}}
P_mean = 65 × 0.95 × 0.972 = 60.02 MW, taken as 60.00 MW  (13.1)
:::

::: {{custom-style="Equation"}}
P_on = 60.00 / 0.972 = {f(Pon,2)} MW;   S_on = {f(Pon,2)} / 0.95 = {f(Son,2)} MVA  (13.2)
:::

::: {{custom-style="Equation"}}
Q_on = {f(Son,2)} × sin(arccos 0.95) = {f(Son*math.sin(math.acos(PF)),2)} Mvar  (13.3)
:::

::: {{custom-style="Equation"}}
I_e = 8.33 × {f(Pon,2)}^(2/3) = {f(8.33*Pon**(2/3),1)} kA;   I_winding = {f(8.33*Pon**(2/3)/math.sqrt(3),1)} kA  (13.4)
:::

::: {{custom-style="Equation"}}
V_LL = {f(Son,2)} / (√3 × {f(8.33*Pon**(2/3),1)} kA) = {f(Son*1e3/(math.sqrt(3)*8.33*Pon**(2/3)),0)} V;   J = {f(8.33*Pon**(2/3)*1e3/(math.pi*155**2/4),2)} A/cm²  (13.5)
:::

The transformers are loaded to {f(100*Son/65,2)} % of their rating while on load, which leaves a headroom of {f(65-Son,2)} MVA. The primary current at 132 kV is {f(Son*1e3/(math.sqrt(3)*132),0)} A.

# Specific energy and production

The specific energy with hot charging follows the vendor rule, measured from ambient temperature:

::: {{custom-style="Equation"}}
SEC = SEC₀ − s × (T − T_ref) / 100 = 3.50 − 0.070 × (500 − 25) / 100 = {f(sec,4)} MWh/t  (13.6)
:::

::: {{custom-style="Equation"}}
E = 24 × P_mean = 24 × 60.00 = {f(E,0)} MWh/d;   M = E / SEC = {f(E,0)} / {f(sec,4)} = {f(M,1)} t/d  (13.7)
:::

The specific energy required to meet 450 t/d is {f(E,0)} / 450 = {f(secreq,3)} MWh/t, so the design has a margin of {f(100*(secreq-sec)/secreq,1)} % in specific energy. Chapter 12 measured the preheat from 0 °C, which gives 3.150 MWh/t, 457.1 t/d and a margin of 1.6 %. The ambient reference is the more conservative choice and is adopted here. The economic model of Chapter 16 uses P_mean = 65 × 0.95 × 0.972 = 60.02 MW and therefore obtains {f(e['production'],1)} t/d.

# Minimum preheat temperature

Production rises with both PF and LF, so the least preheat that meets 450 t/d lies at PF = 0.95 and the achievable LF. Setting M = 450 t/d in Equations (13.6) and (13.7) gives:

::: {{custom-style="Equation"}}
T* = T_ref + 100 × (SEC₀ − 24 × S × PF × LF / M_req) / s = 25 + 100 × (3.50 − 24 × 65 × 0.95 × 0.972 / 450) / 0.070 = {f(Tstar,0)} °C  (13.8)
:::

The design temperature of 500 °C therefore carries a margin of {f(T-Tstar,0)} °C. This result was confirmed with a sequential quadratic programming solution (SLSQP) and with an independent MATLAB script, and the three values agree to within 0.1 °C (Chapter 8).

# Cross-check against the energy balance

The energy balance of Chapter 9 calculated the heat returned by the hot feed from first principles instead of using the vendor rule. Its results can be expressed as the equivalent saving per 100 K of preheat, using the same ambient reference.

::: {{custom-style="Table Caption"}}
Table 13.2: Production at 60 MW for different hot-charging assumptions
:::

| Case | SEC (MWh/t) | Production (t/d) | Equivalent saving (MWh/t per 100 K) | 450 t/d met |
|---|---|---|---|---|
| Vendor rule, whole charge at 500 °C | {f(sec,3)} | {f(M,1)} | 0.070 | Yes |
| Chapter 9, pellets only at 500 °C | 3.240 | {f(E/3.24,1)} | {f((3.5-3.24)/4.75,3)} | No |
| Chapter 9, pellets, lumpy ore and fluxes at 500 °C | {f(E/463,3)} | 463.0 | {f((3.5-E/463)/4.75,3)} | Yes |
| Saving halved (Chapter 16) | {f(3.5-0.035*4.75,3)} | {f(E/(3.5-0.035*4.75),1)} | 0.035 | No |

The pellet-only case of Chapter 9 corresponds to a saving of about {f((3.5-3.24)/4.75,3)} MWh/t per 100 K, or {f((3.5-3.24)/4.75/0.07*100,0)} % of the vendor value. The scope of the hot-charging system must therefore be defined by the feed heat delivered, and the saving must be confirmed in a plant trial before capital is released.

# Material and auxiliary duties

Per tonne of alloy the reconciled mass balance (Chapter 8) gives 2.144 t of ore, 0.433 t of dry reductant, 0.366 t of flux, 1.188 t of slag and 597 Nm³ of off-gas. At {f(M,1)} t/d the duties rise by {f(100*(M/393.65-1),1)} %:

::: {{custom-style="Table Caption"}}
Table 13.3: Daily duties of the existing furnace and of C1
:::

| Duty | Existing (393.65 t/d) | C1 ({f(M,1)} t/d) |
|---|---|---|
| Ore blend (t/d) | 843.8 | {f(2.1436*M,1)} |
| Dry reductant (t/d) | 170.6 | {f(0.43343*M,1)} |
| Flux (t/d) | 144.2 | {f(0.36629*M,1)} |
| Slag (t/d) | 467.6 | {f(1.18798*M,1)} |
| Off-gas (Nm³/h) | 9 797 | 11 315 |

With the assumed 10 % design margin on the auxiliary systems (A-22) their utilisation at C1 is {f(100*(M/393.65)/1.10,0)} %, above the limit of 90 % set by criterion DC-06, so the auxiliary upgrades of Chapter 14 are required.

# Economic calculation

The cash flow follows the method of Chapter 15. The extra alloy is {f(dt,0)} t/yr, valued at US$1 500/t and R17.42 per US$:

::: {{custom-style="Equation"}}
Revenue = {f(dt,0)} × 1 500 × 17.42 / 10⁶ = R{f(e['revenue'],1)} M/yr  (13.9)
:::

The operating cost is the sum of the electricity, ore, reductant, flux, paste and maintenance costs. The investment is R310 M plus a 20 % contingency and R30 M of production lost during the shutdown. Tax at 27 % is calculated after a straight-line depreciation shield of the investment over 15 years, and the net present value uses the annuity factor for 15 years at 12 %.

::: {{custom-style="Table Caption"}}
Table 13.4: Cash-flow calculation for C1
:::

| Item | Calculation | Value (R M) |
|---|---|---|
| Incremental revenue | Equation (13.9) | {f(e['revenue'],1)} |
| Electricity | ({f(e['P_mean'],2)} − 57.43) MW × 8 760 h × R1.65/kWh | {f(el,1)} |
| Ore | {f(dt,0)} t × 2.144 t/t × R2 800/t | {f(ore,1)} |
| Reductant | {f(dt,0)} t × 0.433 t/t × R2 800/t | {f(red,1)} |
| Flux | {f(dt,0)} t × 0.366 t/t × R700/t | {f(flux,1)} |
| Electrode paste | {f(dt,0)} t × 10 kg/t × R16 500/t | {f(paste,1)} |
| Maintenance | 1.5 % of R310 M + R2 M | {f(mnt,1)} |
| Incremental operating cost | Sum of the six items | {f(e['opex'],1)} |
| Incremental profit before tax | Revenue − operating cost | {f(e['profit'],1)} |
| Investment | 310 × 1.20 + 30 | {f(e['capex'],1)} |
| Tax | 27 % × (profit − investment / 15) | {f(tax,1)} |
| After-tax cash flow | Profit − tax | {f(e['cf'],1)} |
| Net present value | {f(e['cf'],1)} × {f(ann,3)} − {f(e['capex'],1)} | {f(e['npv'],0)} |

The internal rate of return is {f(100*e['irr'],1)} % and the after-tax payback is {f(e['payback'],2)} years. Chapter 15 reports an incremental revenue of R604 M, an operating cost of R220.7 M, a profit of about R383 M, a net present value of about R1 540 M and an internal rate of return of about 70 %. The model reproduces that evaluation to within 1.5 % (net present value R1 562 M against about R1 540 M) when it uses the Chapter 15 production and rates. The updated result of R{f(e['npv'],0)} M is about R60 M lower because it uses the conservative production of {f(M,1)} t/d (ambient reference) instead of 457.1 t/d, and the reconciled ore, reductant and flux rates of Chapter 8. The net present value was also calculated independently in MATLAB and agrees to 2 × 10⁻¹⁵.

# Summary

The recommended alternative C1 loads the transformers to {f(100*Son/65,2)} % while on load, produces {f(M,1)} t/d at a specific energy of {f(sec,3)} MWh/t, and meets the 450 t/d requirement with a margin of only {f(100*(secreq-sec)/secreq,1)} % in specific energy. The least preheat that meets the requirement is {f(Tstar,0)} °C, so the design temperature of 500 °C carries a margin of {f(T-Tstar,0)} °C. The duties of all auxiliary systems rise by {f(100*(M/393.65-1),1)} %. The investment of R{f(e['capex'],0)} M returns a net present value of about R{f(e['npv'],0)} M. The narrow margin in specific energy is why the hot-charging saving must be verified by a plant trial before capital is committed.
'''
open('/home/user/START-UP/final_report/md/ch13_detailed_calculations.md','w',encoding='utf8').write(md)
print(f(Pon,2),f(Son,2),f(sec,4),f(M,1),f(secreq,3),f(Tstar,0),f(tax,1),f(ann,3),f(e['npv'],0))
print(f(E/3.24,1),f((3.5-3.24)/4.75*100,3),f(E/463,3),f((3.5-E/463)/4.75*100,3),f(E/(3.5-0.035*4.75),1))
