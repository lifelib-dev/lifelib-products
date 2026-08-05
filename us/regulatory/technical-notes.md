# U.S. Statutory Accounting and Capital: Calculation Technical Notes

- **Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope and division of labour.** This file specifies *how to compute* the statutory accounting items and capital requirements that sit on top of a liability cash flow projection. The companion `us/regulatory/statutory-accounting-and-capital.md` explains what those items are and why they exist; that material is not repeated here. The product models in `us/products/` emit cash flows and policy state; this file consumes them and produces reserves, an IMR/AVR pair, a statutory income statement and surplus roll-forward, and an RBC calculation. Constructions are lifelib/modelx style: explicit state, explicit recursions, per contract or per model point.

**Citation conventions** (identical to the rest of the library, non-negotiable). **[REG-R#]** cites the shared U.S. reference numbering in `us/references/regulatory-and-actuarial-references.md`, which after this work runs R1–R142 with permanently unused gaps at **R114–R124** and **R143–R149**; R1–R72 are the pre-existing life and annuity entries, R73–R142 the statutory accounting and capital entries added now. Every quantitative parameter, factor, threshold, formula and effective date carries a [REG-R#], or **[std]** if it is a standardization introduced for this reference implementation, or **[unverified]** if the research could not confirm it against a retrieved document. Facts the research marked [unverified] **stay** [unverified]; nothing is upgraded. This subject punishes plausible recollection. The per-entry bibliography for this directory — every [REG-R#] cited here and in the explainer, with publisher, URL, access date and fetched/not-fetched marker — is `us/regulatory/sources.md`.

**Documents that could not be read, said plainly at the point of use.** (a) The **NAIC Life and Fraternal Risk-Based Capital Forecasting and Instructions is a sold NAIC publication** marked "Not for Distribution"; the 2024 and 2023 editions used here were read from copies posted by the Indiana Department of Insurance, and the **2025 edition could not be parsed at all** [REG-R128][REG-R129][REG-R139] — nothing here is asserted about year-end 2025 factors, and the forecasting spreadsheet was never obtained. (b) The **AP&P Manual is no longer paid** (the *As of March 2026* edition was retrieved in full [REG-R73], superseding R33's "paid, not fetched" note), but its **Appendix A items A-820 and A-830 were not read** [REG-R110] and **AG 33 and AG 35 remain unread** [REG-R39][REG-R40], so formulaic CRVM and CARVM below rest on the Standard Valuation Law itself [REG-R1] and Model #830 [REG-R6]. (c) The **AVR factor tables and the IMR grouped-amortisation factor tables were deliberately not transcribed** [REG-R89]: their role and location are described and **no factor value is stated for either**. (d) **VM-21 and VM-22 internals were not re-derived**; they are reached through VM-G §1.A, VM-31 §2.A and the RBC instructions' restatement [REG-R109][REG-R108][REG-R128], so that section is an interface specification, not a transcription [REG-R35][REG-R36].

---

## Notation and conventions

**The two computational modes.** Most confusion in statutory modelling comes from conflating them; keep them separate in code, and never let a Mode V routine mutate Mode P state. **Mode V — valuation at a date:** given the in-force at valuation date τ and a fixed assumption/scenario set, return a *number* — a CRVM or CARVM reserve, a VM-20 NPR/DR/SR, a VM-21 CTE statistic. Any projection inside Mode V is an instrument of the calculation, discarded once the statistic is taken; Mode V feeds the annual statement and the RBC pages. **Mode P — projection of statutory quantities forward:** return a *time series* of statutory balance sheets and income statements at τ, τ+1, …. Mode P feeds cash flow testing, C-3 Phase I, distributable earnings, and the Model #312 RBC Plan, which requires projected statutory operating income, net income and capital and surplus for the current year and **at least four succeeding years** [REG-R125 §3.B]. Mode P contains a Mode V call at every future date; that nesting is the dominant runtime cost and has its own section below.

| Symbol | Meaning |
|---|---|
| τ, t | valuation date (a December 31 unless stated); projection index in integer years from τ, t = 0 at τ (m for months) |
| j, K, G | contract index; VM-20 reserving category ∈ {Term, ULSG, All Other}; model segment or aggregation subgroup [REG-R3] |
| x, s | issue age; policy duration in years (s = 0 at issue) |
| ω, N | scenario index; number of scenarios |
| l_j(t) | in-force / survivorship weight for contract j at t (per policy issued, or a count) |
| F, AV, CSV, NAR | face amount; account value; cash surrender value; net amount at risk (the C-2 definition differs — see below) |
| i_v, i_e, NAER | maximum valuation interest rate **by calendar year of issue** [REG-R1 §4b]; earned rate; net asset earned rate path [REG-R3 §7.H] |
| d_ω(t) | scenario-ω discount factor from t back to 0 on the applicable prescribed path |
| V(τ) | reserve at τ; superscripts **gr** gross of reinsurance, **ced** ceded credit, **net** = gr − ced [REG-R89] |
| A, L, S | admitted assets; liabilities; statutory capital and surplus, S = A − L |
| pre/after tax | RBC components are built pre-tax then tax-adjusted on LR030 before covariance [REG-R128]; VM-20 DR/SR **exclude federal income tax entirely** [REG-R3 §7.A]; cash flow testing **includes** it [REG-R111] |

**Per-contract versus aggregate.** NPR, CRVM and CARVM are seriatim [REG-R1][REG-R3 §3]. The DR and SR are computed for a *group* within a model segment and allocated to policies in proportion to each policy's minimum NPR, with an explicit duty to avoid allocating excess to policies that did not produce it [REG-R3 §2.C]. RBC factors read **annual statement values**, not model quantities [REG-R128] — so a projected RBC ratio needs a projected annual statement, not merely projected cash flows (inferred from the blank's line sources; **[unverified]** as a stated requirement).

---

## Required model outputs

The contract between `us/products/` and this section. Anything missing makes something below uncomputable.

| Output | Granularity / basis | Consumed by |
|---|---|---|
| Cash flows by type: gross premium/consideration, death, surrender and withdrawal, annuity and supplementary-contract payments, commission, other acquisition expense, maintenance expense, premium tax, policy loan flows | per contract per period, **gross and ceded separately, never netted** [REG-R89] | every reserve; income statement; Exhibits 5 and 7 |
| Reinsurance cash flows and reserve credit; modco deposit and funds withheld balances | per treaty per period; credit on the **same method and assumptions** as the direct reserve [REG-R92 ¶37] | Exhibit 5 ceded column; VM-20 §8; AG 55 [REG-R103] |
| Face amount in force, policy counts, in-force roll-forward on an **incurred** basis | per product column, in thousands [REG-R89] | Exhibit of Life Insurance; C-2 NAR |
| Net amount at risk | per policy; for C-2, **face in force − statutory reserve (GA + SA), net of reinsurance** [REG-R142] | C-2 mortality |
| Account value, cash surrender value, surrender charge state, MVA state | per contract per period | CARVM; NPR floors; C-3a bucketing |
| Guaranteed benefit streams **by elective path** (surrender, annuitization by option, withdrawal, guarantee election), each with its own timing | per contract, one stream per path | CARVM greatest present value [REG-R1 §5a.B] |
| Secondary-guarantee state: FFSG, ASG, LSG; shadow account | per ULSG contract per period [REG-R3 §3.B.5] | VM-20 NPR (ULSG); §3.C.3 lapse |
| Reserves by category and basis: CRVM/CARVM, VM-20 NPR/DR/SR, VM-21/VM-22, additional AAT reserve, deficiency reserve | per policy then per reserving category, keyed by **valuation standard and year of issue** [REG-R89] | Exhibit 5; minimum reserve; RBC exposure bases |
| Valuation-basis ("tabular") quantities: valuation net premium, valuation mortality, tabular interest, tabular cost | per policy per year, on the **reserve** basis, distinct from experience | Analysis of Increase in Reserves [REG-R90] |
| Separate account asset and reserve balances, GA transfers, SA charges, GA guarantee reserves, fair-value vs ¶18 book-value flag | per contract; SA surplus constrained non-negative [REG-R83 ¶8] | SSAP No. 56 split; C-4a; C-3c |
| **Asset-side interface**: starting-asset block and its statement value; BACV by NAIC designation and issuer; NAER and discount paths per segment; reinvestment/disinvestment strategy; realized gains split interest- vs credit-related; allocated PIMR/IMR (sign-aware) and allocated AVR | per model segment per period | DR/SR; AAT; C-1; C-3 Phase I; IMR/AVR |
| Tax reserve per IRC §807 = max(net surrender value, 92.81% × NAIC-method reserve), capped at statutory [REG-R16][REG-R72] | seriatim, same valuation date | FIT; DTA scheduling; C-3 Phase II tax adjustment |

---

## Formulaic reserves

**CRVM — the modified net premium construction.** For contract j issued at age x with guaranteed benefit stream B and **contract** gross premiums G_k at durations k = 0, 1, 2, … [REG-R1 §5.A]:

```
E   = α − β                                              (the CRVM expense allowance)
α   = min( APV_0(benefits provided after the first policy year) / ä_0 , P19(x+1) )
ä_0 = APV at issue of an annuity-due of 1 payable on the first and each subsequent premium-paying anniversary
β   = net one-year term premium for the benefits provided in the first policy year
P19(x+1) = net level annual premium on the NINETEEN-year premium whole life plan, same amount, at age x+1
k*  : APV_0( k*·G ) = APV_0(B) + E     ⇒     k* = ( APV_0(B) + E ) / APV_0(G)
V_CRVM(s) = max( 0 , APV_s(B) − k*·APV_s(G) )
```

The modified net premiums are that **uniform percentage k\*** of the respective contract premiums [REG-R1 §5.A]. Two traps: the cap is the 19-pay whole life premium at age **x+1**, not x; and V(0) = −E before flooring, so `−V(0)` pre-floor is a free unit test of the allowance. Under **§5.B**, where the first-year contract premium exceeds the second-year premium with no comparable extra first-year benefit and the policy provides an endowment or CSV greater than that excess, the reserve at any anniversary on or before the **assumed ending date** (first anniversary at which endowment plus available CSV exceeds the excess premium) is `max(V_5A, V_5A')`, where V_5A' repeats §5.A with α reduced by **15% of the excess first-year premium**, all present values ignoring premiums and benefits after that date, the policy assumed to mature as an endowment then with the CSV then available as the endowment benefit [REG-R1]. Under the **mean reserve** method the reserve is ½ (terminal reserve + initial reserve), the initial reserve being the prior terminal plus the current-year net annual valuation premium, assuming the whole annual net premium at the start of the policy year and issues spread ratably over the calendar year; because premiums arrive modally the reserve is overstated, so a **deferred premium asset** = gross modal premiums from the next modal due date to the next anniversary, less those collected, less loading. The mid-terminal method instead averages terminal reserves at the surrounding anniversaries and adds an unearned premium reserve [REG-R81/IP51 ¶21]. Inside a VM-20 projection **deferred premiums are zero**, because the projection reflects premium mode directly [REG-R3 §7.B].

**CARVM — the greatest-present-value construction.** For each contract-year end k = 1 … H [REG-R1 §5a.B]:

```
X(k) = APV_τ( guaranteed benefits, INCLUDING guaranteed nonforfeiture benefits, provided at the end of contract year k )
     − APV_τ( future valuation considerations required by the contract that become payable BEFORE the end of year k )
V_CARVM(τ) = max over k of X(k)
```

Future guaranteed benefits use the mortality table (if any) and interest rate(s) **specified in the contract for determining guaranteed benefits**; valuation considerations are the portions of the gross considerations applied under the contract to determine nonforfeiture values [REG-R1 §5a.B]. The implementation obligation is **path enumeration** — one benefit stream per elective path; missing a path can only understate the reserve. AG 33 and AG 35 are the interpretive layers and **their texts were not retrieved** [REG-R39][REG-R40][REG-R41].

**Valuation interest rate, by calendar year of issue.** A **step function of calendar year of issue** (or of the year of the change in fund), not a projection variable [REG-R1 §4b]. Life, also at VM-20 §3.C.2.a.i: `I = 0.03 + W·(R1 − 0.03) + (W/2)·(R2 − 0.09)` with `R1 = min(R, 0.09)`, `R2 = max(R, 0.09)`; SPIAs and life-contingent annuity benefits use `I = 0.03 + W·(R − 0.03)` with **W = 0.80** [REG-R1 §4b.B][REG-R3]. Rounding is to the nearer quarter of 1%, ties **down** for the §3.C.2.a rate [REG-R1][REG-R3]. Life weighting factors by guarantee duration: **0.50** for 10 years or less, **0.45** over 10 to 20, **0.35** over 20 [REG-R1 §4b.C(1)(a)]. Other annuities and GICs use the Plan Type A/B/C table on an issue-year basis (≤5 years 0.80/0.60/0.50; >5–10 0.75/0.60/0.50; >10–20 0.65/0.50/0.45; >20 0.45/0.35/0.35) with change-in-fund increments **+0.15/+0.25/+0.05** and a further **+0.05** for all three plan types in the stated no-forward-guarantee cases [REG-R1 §4b.C(1)(c)]. R is the monthly average of the **Moody's composite yield on seasoned corporate bonds**: for life, the **lesser** of the 36-month and 12-month averages ending June 30 of the year *preceding* issue; for SPIAs and life-contingent annuity benefits, the 12-month average ending June 30 of the year *of* issue [REG-R1 §4b.D][REG-R3]. **Stability rule:** if the life rate differs from the prior calendar year's actual rate by **less than one-half of 1%**, it is set equal to the prior year's rate [REG-R1 §4b.B(2)][REG-R3]. Because §4b.E permits an NAIC-adopted alternative if Moody's ceases publication, implement the reference series as a **configurable table keyed by calendar year**, never a hard-coded feed. VM-20's NPR rate is the same machinery plus a deficiency-style uplift: for term amounts under §3.B.4 and ULSG amounts under §3.B.5.c the rate is **increased by 1.5% but in no event greater than 125% of it**, rounded to the nearest quarter with **ties up**; §3.B.5.d uses the unuplifted rate with ties down [REG-R3]. Income annuities run on a market-linked mechanic instead: four Valuation Rate Buckets A–D keyed to reference period and, with life contingencies, initial age, with **jumbo = initial consideration ≥ $250 million** (contracts to the same holder within 90 days combined), jumbo rates published daily and non-jumbo quarterly [REG-R37].

**Valuation mortality** is the other prescribed input and is keyed the same way. The NPR uses the tables of VM-20 §3.C.1 together with VM-M §1.H [REG-R3]; VM-A indexes the requirements that fix which table applies — A-812 smoker/nonsmoker tables, VM-A-814 recognition of the 2001 CSO (Model #814), A-815 preferred tables and A-821 the annuity table (Model #821) [REG-R110]; and Exhibit 5 Column 1 requires the mortality or disability table actually used to be stated **by years of issue**, its prescribed abbreviation set running from the American Experience Table through **2017 CSO** and **2012 IAR** [REG-R89]. Model it as a lookup keyed by (year of issue, product, sex, smoker, risk class, age basis ANB/ALB), not as a single global table.

**Deficiency and other additional reserves.** A deficiency arises where the valuation net premium exceeds the actual gross premium collected; the interpretive vehicle is Actuarial Guideline I in the VM-C index [REG-R41] and the substantive current standard for term and ULSG is Model #830 through VM-A item A-830 [REG-R6][REG-R110] — **neither text was retrieved** [REG-R33]. The Exhibit 5 Miscellaneous Reserves block carries these and their siblings: variable life minimum death benefit guarantee reserves; excess of valuation net premiums over gross premiums; non-deduction of deferred fractional premiums or return of premium at death; **surrender values in excess of reserves otherwise carried**; and **additional actuarial reserves — asset/liability analysis** [REG-R89][REG-R81/IP51 ¶28][REG-R80 ¶16]. The fourth catches a CARVM result falling below the immediately available surrender value.

**Worked example 1 — CRVM.** Three-year endowment: face 1,000 payable at end of year of death, endowment 1,000 at end of year 3, level annual contract gross premium **G = 320** at the start of each of three years. Valuation basis: flat **q = 0.010**, **i_v = 4%**, and **P19(x+1) = 25.00** per 1,000 so the cap binds — all three **[std]**, chosen so the arithmetic is checkable by hand; a real valuation uses the prescribed table and the calendar-year-of-issue rate above.

| Quantity | Value | | Quantity | Value |
|---|---|---|---|---|
| APV₀(B) = 9.615385 + 9.153107 + 8.713053 + 862.592278 | **890.073822** | | β = 1000·0.01·v | **9.615385** |
| ä₀ = 1 + 0.99·v + 0.9801·v² | **2.858080621** | | E = α − β | **15.384615** |
| APV₀(benefits after year 1) | 880.458438 | | APV₀(G) = 320·ä₀ | 914.585799 |
| uncapped α = 880.458438 / 2.858080621 = 308.059343, capped | **α = 25.000000** | | k\* = 905.458438 / 914.585799 | **0.9900202** |
| V(1) = 924.926036 − k\*·624.615385 | **306.544172** | | V(2) = 961.538462 − k\*·320 | **644.731990** |

Self-check: `APV₀(B) − k*·APV₀(G) = −15.384615 = −E`, so the reserve at issue floors to zero and the expense allowance is exactly E [REG-R1 §5.A].

**Worked example 2 — CARVM.** Single premium deferred annuity: consideration 10,000, guaranteed rate **3.0%**, surrender charges **5/4/3/2/1/0%** in years 1–6, **i_v = 4.25%**, mortality ignored for the surrender stream — all **[std]**. A single premium contract has no future valuation considerations, so `X(k)` is the discounted `CSV(k) = 10,000·1.03^k·(1 − sc_k)`.

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| CSV(k) | 9,785.00 | 10,184.64 | 10,599.45 | 11,029.99 | 11,476.81 | 11,940.52 |
| v^k | 0.9592326 | 0.9201272 | 0.8826160 | 0.8466341 | 0.8121190 | 0.7790111 |
| X(k) | **9,386.09** | 9,371.16 | 9,355.25 | 9,338.36 | 9,320.54 | 9,301.80 |

`V_CARVM = max_k X(k) = 9,386.09` at k = 1, because the valuation rate exceeds the guarantee. It sits **below** the immediately available surrender value of 9,500; that gap is picked up separately as "surrender values in excess of reserves otherwise carried" in Exhibit 5 [REG-R89][REG-R81/IP51 ¶28].

---

## VM-20

**The three components and their combination**, per reserving category K ∈ {Term, ULSG, All Other VM-20} [REG-R3 §2.A, VM-01]:

```
neither DR nor SR computed :  MinRes(K) = Σ_j NPR_j
DR but not SR              :  MinRes(K) = Σ_j NPR_j + max(0, DR − (A − B))
DR and SR                  :  MinRes(K) = Σ_j NPR_j + max(0, max(DR, SR) − (A − B))
A = Σ_j policy minimum NPR for those policies ;  B = due and deferred premium asset held
Total minimum reserve = Σ over the three categories
```

Computing "neither" is permitted only for ULSG with a **non-material secondary guarantee** passing both exclusion tests, or for All Other. Two asymmetries: the DR/SR excess is measured **net of the due-and-deferred premium asset**, and for Term the valuation net premium is zero in policy year 1, so B and the unearned premium reserve are zero in year 1. DR and SR may be computed as of a date **no earlier than three months before τ** with a roll-forward [§2.E]. The general-account share may not be less than zero and the separate-account share is bounded below by Σ CSV and above by Σ AV attributable to the separate account [§2.F]. **Reserving-category dependence is structural:** the minimum reserve is a *sum* of three per-category results, so a Term excess cannot be offset against All Other slack; if a DR group spans categories a DR is computed for each single-category subgroup with any difference allocated **proportionally** [§4.C]; if an SR aggregation subgroup spans categories the **SR must also be computed stand-alone for each category** [§5]. All [REG-R3].

**Net premium reserve (§3), seriatim.** **Term** uses §3.B.4 with prescribed lapses — **10%** during a level premium period under five years, **6%** for five or more, **0%** once the final premium has been payable — plus the prescribed shock-lapse table for the final year of a level premium period, applied after benefits assumed payable that year and before the increased premium takes effect, ranging **25% to 80%** by the before/after period lengths and whether the gross premium increase per $1,000 reaches **400%** [§3.C.3]. **ULSG** under §3.B.5.d uses **0%** lapse throughout; under §3.B.5.c a level rate fixed at τ, `R = clip((FFSG − ASG)/(FFSG − LSG), 0, 1)` then `L = R·0.01 + (1 − R)·0.005·r`, giving a **1% level lapse at issue** where ASG = 0. **All Other, and IUL where no DR or SR is computed, take the VM-A/VM-C formulaic basic reserve** — the CRVM engine above [§3.B.6][REG-R110]. Assumed YRT is **one half year's cost of insurance on the reinsured net amount at risk**. Floors [§3.D]: for non-UL, the greater of the cost of insurance to the next paid-to-date and the CSV; for UL, the amount needed to cover the cost of insurance to the next processing date on which COI charges are deducted, **based on the net amount at risk and on the valuation mortality rate, not the contractual COI or expense charges**. **Policy minimum NPR = NPR less the §8 ceded reinsurance credit** [§3.E]; the NPR must reflect continuous deaths and immediate payment of claims. All [REG-R3].

**Deterministic reserve (§4) — both forms**, since VM-31 §3.D.2.h requires the company to state which was used **for each model segment** [REG-R108]:

```
§4.A gross premium valuation form
  DR = APV(benefits, expenses and related amounts) − APV(premiums and related amounts)
     − PIMR allocated at the valuation date + separate account asset balance + policy loan balance
§4.B direct iteration form
  DR = a − b ,  a = aggregate annual statement value of the starting assets which, projected with all premium and
       investment income, exactly liquidates all projected future benefits and expenses by the end of the horizon;
       b = the allocated PIMR
```

**Prescribed scenario: economic scenario 12** of §7.G.1 / Appendix 1.E, discounted on the **path of discount rates for the corresponding model segment** determined under §7.H.3 — a net asset earned rate construction. The APV of premiums and related amounts includes future gross premiums and other revenue, net separate-account-to-general-account flows, net policy loan flows, net §8 reinsurance flows and net derivative-liability-program flows allocated to the group. **Federal income taxes are excluded from projected expenses** [§4.A, §7.A]. A group excluded from the SR requirement **may not include future non-hedging derivative program transactions in its DR** [§4.A.5]. All [REG-R3].

**Stochastic reserve (§5).** Per scenario ω, for each model segment, at the model start date and each projection year end, discount **the negative of the projected statement value of general and separate account assets** back to the start on the §7.H.4 path; sum across model segments at each date; then [REG-R3 §5]:

```
ScenRes(ω) = statement value of starting assets across all model segments
           + max over dates d of  Σ_segments ( − AssetStatementValue_ω(d) · discount_ω(d) )
SR         = CTE70({ScenRes(ω)}) + any additional amount for material risks not reflected in the models − allocated PIMR
CTE_a(X)   = mean of the worst (1 − a) fraction of the ranked sample; rank low to high, average the largest 30% for CTE 70
```

Aggregation subgroups must be consistent with how the company **actually manages risk**, and contract types with significantly different risk profiles may not be grouped [§5]. The 2026 GOES phase-in, if elected before the Dec. 31, 2026 valuation, applies `DR = D − (B − A)·(DR1 − DR2)/B` and `SR = S − (B − A)·(SR1 − SR2)/B` with **B = 36 months**, A = months elapsed since Dec. 31, 2025, DR1/SR1 on the 2026 scenario basis and DR2/SR2 on the 2025 basis, both as of Jan. 1, 2026 on the same in-force and **ignoring exclusion tests**; the phase-in amount is deemed zero for a component whose exclusion test is passed [§2.J].

**Exclusion tests as decision procedures.** They determine what the model must be *capable* of, so implement them as gates. **Stochastic Exclusion Test** [REG-R3 §6.A], three alternative routes:

```
route 1  SERT — annually, within 12 months before τ:
         a = adjusted DR under economic scenario 9 (the baseline, Appendix 1.E)
         b = the LARGEST adjusted DR under any of the OTHER 15 of the 16 prescribed scenarios
         c = PV of BENEFITS under the baseline, adjusted for reinsurance by subtracting ceded benefits, using the
             benefit cash flows from "a" and the same discount path
         PASS iff (b − a) / c < 6%
route 2  Stochastic Exclusion Demonstration Test — first year and at least every third calendar year: compare
         max(DR, NPR − due-and-deferred-premium-asset) against the stand-alone SR, or against scenario reserves from a
         sufficient number of adverse deterministic scenarios, or against an SR on a representative sample, or
         demonstrate the driving risks are absent or substantially eliminated
route 3  SET Certification Method — first year and at least every third calendar year; NOT available for variable life
         or ULSG
```

The numerator is `b − a` — **not** the largest difference and **not** the largest absolute difference, both of which the guidance note says give an incorrect result. Benefits for "c" are death benefits, surrender or withdrawal benefits and **policyholder dividends**; premium, ceded premium, expense, reinsurance expense allowance, modco reserve adjustment and experience refund flows are **not** benefits. The adjusted DR may be built either as the §4.A DR with scenario-specific interest rates, equity returns, NAER and discount rates, **or** as the gross premium reserve developed from the company's own asset adequacy analysis models using its cash-flow-testing assumptions, provided that model carries explicit margins or sensitivities reflecting moderately adverse conditions for the non-economic risks [§6.A.2.b.i] — the Valuation Manual therefore explicitly contemplates one engine serving both VM-30 cash flow testing and the VM-20 test. **YRT relief:** passing gross of YRT but failing net still passes if `SERT_gy × LPIR_ny / LPIR_gy < 0.060` with `LPIR = (b − a)/a` on each basis [§6.A.2.c]. **Blocking rule:** the SERT may not be used if the Demonstration Test was attempted on current-year data and failed, or the qualified actuary actively undertook the certification and concluded it could not legitimately be made [§6.A.2.d]. **Hedging bar:** a group with one or more future hedging strategies may not be excluded from the SR except where all such strategies relate solely to features immaterial under §7.B.1 due to low utilization [§6.A.1.b]. All [REG-R3]. **Deterministic Exclusion Test** [§6.B]:

```
DEEMED FAIL    ULSG that does not meet the "non-material secondary guarantee" definition, or any group not excluded
               from the SR requirement
NOT AVAILABLE  at all for term insurance policies or term riders
otherwise      Deterministic Net Premium Test: PASS iff Σ future valuation net premiums ≤ Σ corresponding guaranteed
               gross premiums, on a direct or assumed basis
```

Test conventions [§6.B.5]: lapse rates set to **0% at all durations** where the NPR comes from §3.B.4 or §3.B.5; for shock-lapse designs the comparison considers **only the initial premium period**; and where anticipated experience mortality plus §9.C.6 margins exceeds prescribed CSO, that basis must be used, mortality measured as the PV of future death claims discounted at the NPR valuation rate. Guaranteed gross premium for UL with none specified is the level annual gross premium at issue that would keep the policy in force for the whole coverage period on the guarantees [§6.B.6]. A closed group passing three consecutive years is thereafter tested **at least once every five years** [§6.B.4]. **Governance consequence:** passing via the DR-based SERT method, the VM-22 adjusted-scenario-reserve method or the Demonstration Test **re-imposes VM-G Sections 2 and 3** on a company otherwise exempt, and a company computing no DR or SR still files a VM-31 sub-report and must report **readiness to compute the DR and/or SR** [REG-R109][REG-R108].

---

## VM-21 and VM-22

**VM-21 (variable annuities), as an interface.** Scenario Reserves come from one stochastic run over the VM-21 §4 accumulated-deficiency construction. The reserve is **CTE 70** of the Scenario Reserves plus the **Additional Standard Projection Amount** of VM-21 Section 6; the capital requirement is built from **CTE 98** of the *same* Scenario Reserves plus the *same* ASPA [REG-R128][REG-R35]. Grouping, sampling, scenario count and simplification "should be identical to those used in calculating the company's statutory reserves following VM-21", and certification and documentation follow VM-31 [REG-R128][REG-R108]. AG 43 contracts are documented as VM-21 business, and where AG 43 business is aggregated with VM-21 business VM-G applies to the combined valuation [REG-R108][REG-R109].

**The efficiency point, as an architectural requirement.** The variable annuity reserve and its capital requirement are **two order statistics from a single stochastic run** [REG-R128][REG-R35]. Compute the Scenario Reserve vector once, retain it, and read CTE 70 and CTE 98 off it; compute the ASPA once under VM-21 §6 and use it in both. Any design that reruns the projection for capital is slower *and* can produce a CTE 70 > CTE 98 inconsistency that is undetectable without the shared vector. VM-21 records the elective federal income tax treatment as the only substantive difference between the reserve and RBC projections [REG-R35].

**VM-22 (non-variable annuities).** Its **Section 7 exclusion tests and Single Scenario Test** are the annuity counterparts of VM-20 §6, and VM-G §1.A and VM-31 §2.A name VM-22 alongside VM-20 [REG-R36][REG-R109][REG-R108]. The adjusted-scenario-reserve route of VM-22 §7.C.2.a.i carries the same VM-G Section 2/3 consequence as the VM-20 SERT DR method [REG-R109]. The formulaic track survives inside VM-22 through VM-V §1 income annuity rates [REG-R37]. **This research did not re-derive VM-22's internals** — build them from R36 directly. Reporting consequence: annuities valued using VM-22 valuation interest rates are reported in Exhibit 5 split **Jumbo / Non-Jumbo in 50-basis-point valuation interest bands** [REG-R89]. Transition: SSAP Nos. 3, 51 and 52 were revised in March 2026 to give guidance on the **optional implementation period** for Valuation Manual revisions regarding the economic scenario generator and non-variable annuities [REG-R88].

---

## Projecting reserves forward — the nested-valuation problem

**What actually requires it.** VM-20's DR and SR **do not project future statutory reserves at all**: the DR is a gross premium valuation or a direct-iteration starting-asset solve, and the SR is built from projected *asset* statement values [REG-R3]. Cash flow testing needs a reserve-like quantity at the **end**, not throughout: VM-30 defines ending surplus operationally as either extending the projection until the remaining in-force and associated assets and liabilities are immaterial, **or** adjusting end-of-projection surplus by an amount estimating the value expected to arise from what remains in force [REG-R100]. Where reserves genuinely must be projected at every date is the capital and distributable-earnings side: **C-3 Phase I requires S(t) = statutory assets − statutory liabilities at every calendar year end of every scenario** [REG-R128], C-3 Phase II requires a projected statutory balance sheet including federal income tax [REG-R47], and the RBC Plan requires five years of projected statutory income and surplus [REG-R125]. **[REG-R47] is the *pre-reform* C-3 Phase II package and is superseded in its parameters by the current instructions [REG-R128]** — read it for the shape of the projection requirement, never for a CTE level, a scalar or a tax rate.

**The algorithm and its cost.** For each outer scenario ω and future date t the reserve at t is itself a valuation on the in-force projected to t: `state(ω,t) ← project(product model, ω, t)`; `V(ω,t) ← Mode-V valuation at state(ω,t)`; `S(ω,t) ← A(ω,t) − V(ω,t) − IMR(ω,t) − AVR(ω,t) − other liabilities`. Cost is `N_out × T × (inner cost)`, and if the inner valuation is itself stochastic the inner cost is `N_in × T` and the run blows up quadratically.

**Mitigations, in the order to try them.** (1) **Formulaic reserves need no nesting** — CRVM, CARVM and the VM-20 NPR are functions of projected policy state under prescribed assumptions, computable by a duration recursion at each date; write the reserve routine to take a state vector, not a valuation date. (2) **Working-reserve proxy:** C-3 Phase II's own standard device is **modelling the statutory reserve as equal to the working reserve** inside the projection [REG-R47], with a **Tax Adjustment** required under Specific Tax Recognition where actual tax reserves exceed projected tax reserves at the projection start [REG-R47][REG-R128]. The device and the tax adjustment both survive in the current instructions [REG-R128]; the surrounding [REG-R47] parameters do not. (3) **One direct-iteration routine, three uses** — iterating the starting asset amount until ending surplus is immaterial serves the VM-20 §4.B DR, the VM-21 reserve and the CFT ending-surplus problem; the Academy practice note makes exactly this observation [REG-R111][REG-R3]. (4) **Terminal value instead of a long horizon**, per VM-30's explicit alternative [REG-R100]; the discount rate for a PV of ending surplus is a modelling choice, not a prescription — reported practice includes the after-tax portfolio earned rate, Treasury spot rates, and inferring the factor by re-running with additional initial assets, from a **2012 survey, indicative of practice shape, not a calibration target** [REG-R111]. (5) **Grouping and compression**, permitted only on a demonstration that the simplification does not materially understate the reserve **and** that the expected value of the simplified reserve is not less than the unsimplified one, model segmentation for net asset earned rates being exempt from that demonstration [REG-R3 §2.G]; VM-31 §3.D.2 requires the grouping rationale and a commitment that any subgroup can be audited against a seriatim model [REG-R108]. (6) **Proxy functions or fitted reserve surfaces** are an engineering option **[std]**; no cited document sanctions them, and §2.G and §2.I still apply. **§2.I explicitly disallows** the tempting shortcuts: not computing even a simplified NPR; not computing a simplified DR or SR without passing the relevant test; omitting prescribed mortality margins; establishing no lapse margins; not building even a simplified asset model for the DR; using the alternative investment strategy without first showing it produces a higher reserve; and **ignoring post-level-term losses** [REG-R3].

---

## Statutory income and surplus roll-forward

**The recursion**, on the Summary of Operations line sequence [REG-R90]:

```
Income(t)       = Prem(t) + ConsiderationsSupplContractsLifeCont(t) + NII(t) + IMRamort(t) + SA_NetGainFromOps(t)
                + CommAndExpAllowancesOnCeded(t) + ReserveAdjustmentsOnCeded(t) + MiscIncome(t)   # incl. deposit-type fees
Benefits(t)     = Death(t) + MaturedEndowments(t) + AnnuityBenefits(t) + DisabilityAndAH(t) + Coupons(t)
                + SurrenderAndWithdrawal(t) + GroupConversions(t) + InterestOnContractAndDepositFunds(t)
                + PaymentsSupplContractsLifeCont(t) + ΔV(t)              # ΔV = increase in aggregate reserves, Line 19
Expenses(t)     = Commissions(t) + GeneralExpenses(t) + InsuranceTaxesLicencesFees(t) + ΔLoading(t)
                + NetTransfersToSeparateAccounts(t) + WriteIns(t)
GainPreTax(t)   = Income(t) − Benefits(t) − Expenses(t) − PolicyholderDividends(t)
GainAfterTax(t) = GainPreTax(t) − FIT(t)
S(t) = S(t−1) + GainAfterTax(t) + NetRealizedCapitalGains(t) + ΔUnrealizedCapitalGains(t) − ΔAVR(t)
     − ΔNonAdmittedAssets(t) + ChangeInValuationBasis(t) + CapitalAndSurplusPaidIn(t) − StockholderDividends(t)
     + OtherSurplusAdjustments(t)
```

with `ΔV(t) = V(t) − V(t−1)` on the **statutory** reserve and `ΔLoading(t)` the change in loading on deferred and uncollected premium, which is an **expense**, not a reduction of premium [REG-R79 ¶11]. Acquisition costs enter `Commissions` and `GeneralExpenses` **in the period incurred, with no deferral and no DAC asset** [REG-R75 ¶2]; why that reshapes the earnings signature relative to GAAP is in the explainer, "Why statutory differs from GAAP". The lower recursion is the Capital and Surplus Account, which several items reach without passing through income: the change in valuation basis is measured as old-basis minus new-basis reserve **as of the beginning of the year**, goes **direct to surplus**, is **not** graded in unless an NAIC actuarial guideline prescribes a transition, and is **excluded** from both the Summary of Operations and the Analysis of Operations, appearing in Exhibit 5A [REG-R79][REG-R80 ¶14][REG-R89]; AVR movements go directly to surplus [REG-R86]; non-admitted assets are charged against surplus rather than carried [REG-R74 ¶36]; and the change in non-admitted disallowed IMR runs through the same account [REG-R87][REG-R89].

**Analysis of Increase in Reserves During the Year** [REG-R90], by the same product columns as the Analysis of Operations. Additions: 1 opening reserve; 2 **tabular net premiums or considerations**; 3 PV of disability claims incurred; 4 **tabular interest**; 5 **tabular less actual reserve released**; 6 increase on account of **change in valuation basis**; **6.1 change in excess of VM-20 deterministic/stochastic reserve over net premium reserve**; 7 other increases (net); 8 totals. Deductions: 9 **tabular cost**; 10 reserves released by death; 11 reserves released by other terminations (net); 12 annuity, supplementary contract and disability payments involving life contingencies; 13 net transfers to or from separate accounts; 14 total deductions; 15 closing reserve; then 16 ending CSV and 17 the amount available for policy loans on that CSV. These are **reserve-basis** quantities, not experience quantities. The instructions' precise definitions were **not transcribed by the research** [REG-R89]; the reference implementation uses **[std]** `TabNetPrem(t) = Σ_j π_j·l_j(t−1)`, `TabInterest(t) = i_v·(V(t−1) + TabNetPrem(t))`, `TabCost(t) = Σ_j q^val·(B_j − V_j(t))·l_j(t−1)` and `ReservesReleasedByDeath(t) = Σ_j q^val·V_j(t)·l_j(t−1)`, so that `TabCost + ReservesReleasedByDeath` equals expected death benefits on the valuation basis — which is why the statement can deduct both without double counting **[std, derived]**. Read the operative definitions from [REG-R89] before filing.

**The reconciliation identity that must hold**, at every t: `S(t) = A(t) − L(t)` with `L(t) = V(t) + IMR(t) + AVR(t) + other statutory liabilities`, **and** `S(t) − S(t−1)` = after-tax gain plus the direct-to-surplus items above. Assert both: the first catches a reserve or asset booking error, the second catches an item routed to the wrong statement.

---

## Interest maintenance reserve and asset valuation reserve

**IMR — the amortisation algorithm.** What the IMR is, why it amortises rather than releasing, and why it has no GAAP analogue are in `us/regulatory/statutory-accounting-and-capital.md`, "Asset valuation reserve and interest maintenance reserve"; the operative scope rule the algorithm needs is that it carries interest-rate-driven realized gains and losses on investments sold **and** certain liability gains and losses, each amortised over the expected remaining life of the item released [REG-R85 ¶2]. Balance recursion, per the annual statement form [REG-R90]: `IMR(y) = IMR(y−1) + Σ_d g_net(d) ± LiabilityAdjustment(y) − Amort(y)`, where `g_net(d)` is the current-year realized pre-tax gain transferred **net of taxes** and `Amort(y)` is released to **Summary of Operations Line 4**. The supporting schedule is a grid of **30 future calendar years plus an "and later" row**; the balance sits at Page 3 Line 9.4 and the amortisation is allocated by line of business [REG-R89][REG-R90]. Per disposal d:

1. **Classify.** Interest-related (→ IMR) if the NAIC designation at the end of the holding period differs from the beginning designation by **one or less**; otherwise credit-related (→ AVR); anything ever designated **"6"** during the holding period always goes to AVR; and an **acute credit event** not yet in CRP ratings or the SVO feed that predominantly drove the gain/loss excludes it from IMR. A gain is **either** interest or non-interest, never a blend, except as SSAP No. 43 specifies; same-CUSIP purchase lots are treated as individual assets [REG-R89].
2. **Exclude** gains and losses that per contract terms directly increased or decreased **contract benefit payments or reserves** in the period, and those funding **excess withdrawal activity** (below) [REG-R89].
3. **Net of tax.** Capital gains tax follows the company's own statutory allocation method, and the attached tax amortises **in proportion to the pre-tax amortisation** [REG-R89].
4. **Set the expected maturity date.** Fixed-repayment instruments use the contractual retirement date producing the lowest amortisation value (**yield to worst**) across all call dates and maturity; scheduled sinking funds add a yield-to-average-life calculation at 50% repaid; **puttable** instruments use the put or maturity date producing the **highest IRR**; SVO Identified Funds on systematic value use the WAL of the underlying bonds; **perpetuals, and fixed income with no maturity date or sinking fund schedule, use 30 years**; MBS/ABS use remaining WAL on repurchase-price prepayment assumptions. A callable bond bought at a premium and called or sold **after** its expected maturity date has **no amortisation** — the gain or loss goes straight to income, likewise a convertible disposed of after its expected maturity date [REG-R89].
5. **Amortise by one of two methods, locked in for that year's gains once chosen and not changeable without commissioner approval** [REG-R89]. **Seriatim:** the annual amortisation is the excess of the income that would have been reported had the asset **not** been disposed of over the income that would have been reported had it been **repurchased at its sale price**; for MBS/ABS on a schedule built from the prepayment assumptions that would have applied at the repurchase price. **Grouped:** group net-of-tax gains by **calendar years to expected maturity** in the bands **0, 1, 2–5, 6–10, 11–15, 16–20, 21–25, over 25** (calendar year of maturity minus calendar year of sale) and multiply by the **published amortisation factors for the year of sale**, each year's gains using that year's table for all future years, current-year gains on the prior year's factors until the current table is published. **Those factor tables are published annually and were not transcribed by the research; no value is stated here** [REG-R89]. The current bands begin with a separate "0 calendar years" band, unlike the 1990s text in the issue paper [REG-R86].

**Liability leg.** The interest-rate-related gain/loss net of tax on the sale, transfer or reinsurance of a **block of liabilities** enters IMR only where the portion reinsured exceeds **5% of general account liabilities** (Page 3, Line 26), the transaction is **irrevocable and to a non-affiliate**, and it completed in the current year; the amount is the **negative of the sum** of the IMR balance and future amortisation from past and present dispositions of the block's associated assets plus the IMR that would arise if the remaining associated assets were sold [REG-R86][REG-R92 ¶54]. Material **market value adjustments** on contracts backed by assets carried at book also enter IMR, amortised consistently with the MVA determination; **material = in excess of both 0.01% of liabilities and $1,000,000** [REG-R86].

**Excess-withdrawal exemption, as a procedure** [REG-R89]:

```
WR(y−1) = withdrawable reserves at BOY: reserves and liabilities net of policy loans on any policy or contract subject
          to withdrawal or surrender WITHOUT an MVA at the holder's discretion (ordinary and industrial life, SPDAs,
          benefit-sensitive GICs), NET OF REINSURANCE
EW(y)   = effective withdrawals: unscheduled withdrawals and surrenders computed without market adjustment + net
          increase in policy loans + cash transfers to separate accounts other than pass-through transfers of new
          premium, NET OF REINSURANCE
wr(y)   = EW(y) / WR(y−1) ;   TWL(y) = 1.50 × min( wr(y−1), wr(y−2) ) × WR(y−1) ;   XS(y) = max(0, EW(y) − TWL(y))
```

Gains and losses on the investments required to fund XS(y) are **excluded from IMR and flow straight to net income**, identified specifically where possible and otherwise pro rata across the year's sales [REG-R89].

**Negative IMR admittance — the gates, as a computable test.** Baseline: a positive net IMR is a liability at Page 3 Line 9.4; a **negative** net IMR ("disallowed IMR") is a miscellaneous other-than-invested write-in asset and **non-admitted**, the change running through the Capital and Surplus Account [REG-R87 ¶¶3–4][REG-R89]. INT 23-01 gives a limited-time, optional exception [REG-R87]:

```
cap    = min( 0.10 × AdjCapSurplus(most recently filed statement), 0.10 × CapSurplus(current period, unadjusted) )
         # ¶9.a; the second cap was added in the August 2025 revision. AdjCapSurplus excludes net positive goodwill,
         # EDP equipment and operating system software, net deferred tax assets, and admitted net negative IMR
gate 1 : adjusted RBC greater than 300% of Authorized Control Level, TAC adjusted for the same four items, AFFIRMED
         for every quarterly and annual statement in which admitted negative IMR is reported            # ¶9.b
gate 2 : derivative losses carried at fair value before termination are eligible ONLY with documented historical
         evidence that fair-value derivative GAINS were reversed to IMR and amortised — evidence required separately
         for the general account, the insulated separate account and the non-insulated separate account  # ¶9.c
gate 3 : the ¶13 data-captured disclosures are fully completed, else NON-ADMIT ALL                       # ¶9.d
gate 4 : admitted negative IMR is captured in the PBR calculation or in asset adequacy / cash flow testing under
         VM-20 §7.D.7 and VM-30 §3.B.5, with a reconciliation to the IMR reflected there                 # ¶9.e
order  : admit ALL general account net negative IMR first, up to cap; only if the cap is not reached may a separate
         account IMR ASSET be recognised, allocated proportionately between insulated and non-insulated  # ¶10
```

Reporting: a general account write-in to miscellaneous other-than-invested assets, **asset page line 25**, captioned "Admitted Disallowed IMR", with an **equal amount allocated from unassigned funds to special surplus funds line 34**, explicitly so admitted negative IMR cannot be reported as funds available to dividend; separate accounts use asset page line 15 and special surplus line 19 [REG-R87 ¶¶11–12]. **Sunset:** extended on August 11, 2025 to **December 31, 2026, with automatic nullification January 1, 2027**, and the date may move again [REG-R87 ¶¶14–15]; the Academy practice note's statement that nullification occurred January 1, 2026 predates that extension and is superseded [REG-R111]. A **revised SSAP No. 7** absorbing the AVR/IMR guidance from the annual statement instructions was in drafting at the 2026 Spring National Meeting alongside an adopted "IMR proof of reinvestment" concept; **the exposed text was not located** [REG-R88].

**Feedback into the reserve model.** VM-30 §3.B.5 requires an appropriate allocation of assets **in the amount of the IMR, positive or negative**, in *any* asset adequacy analysis; any portion of the total company IMR **not admitted** must be removed first; **the full amount of any admitted negative IMR must be used**, and in that case the allocated assets are **reduced by its absolute value** [REG-R100]. Assets supporting the **AVR** may be allocated for **asset default risk only**, may not be applied to any other risk, and the amount used must be disclosed in both the opinion's reserve table and the memorandum [REG-R100]. The IMR has **no cash flows** — it is a sign-aware, non-cash-flow adjustment to starting assets [REG-R111]. Because the AVR consumed in asset adequacy testing is also removed from Total Adjusted Capital [REG-R128], the AAT routine must **report how much AVR it used**; that number is an input to the capital numerator, not a by-product.

**AVR — the accumulation mechanic.** Purpose and scope are in the explainer, "Asset valuation reserve and interest maintenance reserve"; what the algorithm needs is the sub-component structure — Default (bond and preferred stock including derivative counterparty exposure; mortgage) and Equity (common stock; real estate and other invested assets) — over the SSAP No. 7 ¶2 asset base, which excludes cash, policy loans, premium notes, collateral notes and income receivable [REG-R85 ¶2][REG-R86 ¶11(B)]. Per sub-component c per year [REG-R89][REG-R90]:

```
Bal_c(y) = Bal_c(y−1) ± RealizedGains_c(y) net of tax          # general and separate accounts on separate lines
         ± UnrealizedGains_c(y) net of deferred tax on an SSAP No. 101 basis
         − GainsCreditedOrLossesChargedToContractBenefitsOrReserves_c(y)          # anti-double-count line
         + BasicContribution_c(y) + Accumulation_c(y) ± Transfers_c(y) + VoluntaryContribution_c(y)
Accumulation_c(y) = 0.20 × ( ReserveObjective_c(y) − accumulated balance )        # negative when the objective is exceeded
then floor at 0 and cap at Maximum_c(y)
```

The **20% of the shortfall to the reserve objective** is the only numeric parameter of this mechanic the research captured [REG-R89, AVR Line 11]. The three factor families have stated *roles*: the **basic contribution factor** produces on average an amount approximating expected annual losses; the **reserve objective factor** targets an accumulation covering, in the aggregate, **about 85% of the distribution of losses** for the asset category; the **maximum reserve factor** caps the accumulation. They are tabulated by NAIC designation (bonds, preferred stock, short-term, derivative counterparty exposure) and by mortgage category using the **Life RBC classification methodology**, on the AVR supporting forms — **the numeric factors were not transcribed and no value is stated here** [REG-R89][REG-R90]. Transfers: an excess over a sub-component maximum goes to its sister sub-component if that sister is below its maximum; an excess over a whole component's maximum may move to the other component or be **released to surplus**; a negative sub-component balance transfers to its sister only to the extent it does not reduce the sister's positive pre-transfer balance below **50%**; and there are **no transfers between AVR and IMR** [REG-R89]. U.S. government and full-faith-and-credit agency securities are exempt from AVR, and affiliated life insurers maintaining their own AVR carry a **0% maximum reserve factor** [REG-R89]. Movements go direct to surplus; the balance sits at Page 3 Line 24.01 [REG-R86][REG-R89]. Separate accounts: an IMR is required for **book-value** separate accounts and not for fair-value ones, applied account by account [REG-R83 ¶¶26–27]; a separate account AVR is required where the reporting entity rather than the policyholder bears default or fair-value loss — traditional VA and VL separate accounts need none **except on seed money** — and separate account AVR is **combined with the general account AVR** in the general account statements [REG-R83 ¶¶11, 23–25].

---

## Risk-based capital

**Read every number in this section against its source limit.** All of it comes from the **2024** *Life and Fraternal Risk-Based Capital Forecasting and Instructions*, a **sold NAIC publication marked "Not for Distribution"**, read from a copy posted by the Indiana Department of Insurance [REG-R128]; the 2023 edition was used only to date the structures [REG-R129]; **the 2025 edition could not be parsed, so nothing here is a year-end 2025 factor** [REG-R129][REG-R139]. Buy the current edition before filing.

| Component | Driver | Page |
|---|---|---|
| **C-0** | insurance subsidiaries plus off-balance-sheet and miscellaneous items; a life affiliate contributes its own **line (69) plus twice its AG 48 shortfall**, prorated by ownership | LR031 [REG-R128] |
| **C-1o** | asset default on bonds, mortgages and other non-common-stock assets: BACV × factor by NAIC designation × **bond size factor** | LR002 etc. [REG-R128] |
| **C-1cs** | unaffiliated common stock, Schedule BA common stock, the concentration factor, affiliated non-insurers | LR031 [REG-R128][REG-R136] |
| **C-2** | mortality on business written (**NAR**-based) and **longevity** (**reserve**-based), plus health claim reserves and the premium stabilization credit | LR025, LR025-A [REG-R128] |
| **C-3a** | interest rate risk: factor charges by **withdrawal provision**, or C-3 Phase I cash flow testing, plus the interest component from Phase II | LR027 [REG-R128] |
| **C-3b / C-3c** | health credit risk / market risk from variable products with guarantees (C-3 Phase II) | LR028, LR027 line 37 [REG-R128] |
| **C-4a / C-4b** | general business risk: **2.53%** of Schedule T life premiums and annuity considerations, **0.63%** of A&H premiums, **0.06%** of separate account liabilities / health administrative expense | LR029 [REG-R128] |

C-1o bond factors run across **20 designation categories**, from 1.A at **0.00158** to 5.C and NAIC 6 both at **0.30000** [REG-R128][REG-R130]. The **bond size factor** aggregates by issuer (first six CUSIP digits): weighted issuers = 2.40 × first 50 + 1.53 × next 50 + 0.85 × next 100 + 0.85 × next 300 + 0.82 × over 500; size factor = total weighted issuers ÷ total issuers; **a blank issuer count is charged the maximum 2.40** [REG-R128]. LR002's published *Basis of Factors* narrative still describes the pre-2021 calibration while the factors are the 2021 Moody's set — an observation from comparing two documents, **[unverified]** as to NAIC intent [REG-R128][REG-R130].

**C-2 mortality: the NAR definition and the pricing-flexibility test.** Exposure base, **net of reinsurance throughout**, now derived from the annual statement rather than free-form company records [REG-R142]:

```
Total Individual & Industrial Life NAR
  = (Exhibit of Life Insurance, sum of Columns 2 and 4, Line 23 × 1000)
  − [ (Exhibit 5, sum of Columns 3 and 4, Line 0199999) + (Separate Accounts Exhibit 3, Column 3, Line 0199999)
    + (General Interrogatories Part 2, Column 1, Line 10.01) − (General Interrogatories Part 2, Column 1, Line 10.02) ]
```

i.e. **face amount in force minus life reserves, general account plus separate account, with a reinsurance adjustment** [REG-R142]. Size bands apply to the *total* for individual and industrial life and separately to the total for group and credit life, then are allocated proportionately to each factor category: band 1 up to **$500 million** NAR, band 2 above $500 million to **$25 billion**, band 3 above $25 billion [REG-R128][REG-R133].

| Category (pre-tax, per dollar of NAR) | First $500M | Next $24,500M | Over $25,000M |
|---|---|---|---|
| Individual & Industrial **with** Pricing Flexibility | 0.00220 | 0.00105 | 0.00080 |
| Individual & Industrial **Term without** Pricing Flexibility | 0.00280 | 0.00120 | 0.00085 |
| Individual & Industrial **Permanent without** Pricing Flexibility | 0.00400 | 0.00175 | 0.00120 |
| Group & Credit Term Life, remaining rate terms ≤ 36 months | 0.00140 | 0.00055 | 0.00040 |
| Group & Credit Term Life, remaining rate terms > 36 months | 0.00190 | 0.00080 | 0.00055 |

FEGLI/SGLI take a separate **0.0004** factor applied to **amount in force**, not NAR [REG-R142]. **Pricing flexibility is a categorisation the model must earn, not a product code**: it is the ability to *materially* adjust rates on in-force contracts through premiums and/or non-guaranteed elements as of the valuation date and within the next **5 policy years**, reflecting typical business practices, tested on a present value basis — `minimum dollar margin needed = flexibility factor × NAR`, the flexibility factor being the difference in mortality risk provided for in the factors for contracts with and without pricing flexibility, and the contract passes into the "with" category only if the margin actually available from repricing over those 5 policy years, **on a present value basis**, is at least that amount [REG-R128]. Grouping may be at contract or pricing-cohort level; contracts may move between categories at successive valuation dates; and **an insurer may simply elect the "without" categories if the evaluation is not completed** [REG-R128][REG-R133]. Defaults where no assessment is performed: direct individual term → Term without; direct individual permanent → Permanent without; direct group → over-36-months; non-affiliated **ceded** individual → With Pricing Flexibility; non-affiliated ceded group → 36-months-and-under; affiliated reinsurance follows the direct categorisation [REG-R133]. Product examples in the instructions: *with* — participating whole life, UL **without** secondary guarantees, annually repriceable YRT; *term without* — level term with guaranteed level premiums; *permanent without* — **ULSG and non-participating whole life**, also the **default bucket with the highest factors** [REG-R128]. A model must therefore be able to run a **repricing scenario**, not merely a base scenario.

**C-2 longevity** is reserve-based: **0.0171 / 0.0108 / 0.0095 / 0.0089** on the first $250 million, next $250 million, next $500 million and over $1,000 million of life-contingent annuity reserves [REG-R128]. In scope: payout annuities in pay status, **deferred income annuities that will enter pay status**, structured settlements with any life-contingent benefit, group annuities including pension risk transfer, and **variable immediate** annuity reserves under VM-21 — the **entire** reserve of an in-scope contract, including the period-certain portion of a certain-and-life annuity. Out of scope: non-life-contingent annuities; deferred annuities with a right but no obligation to annuitize; a certain-and-life annuity reduced to certain payments only after the annuitant's death; and **variable deferred annuity reserves under VM-21, including contracts whose account value has reached zero but a lifetime benefit remains payable** [REG-R128].

```
Total C-2 pre-tax = TotalHealthClaimReserves + PremiumStabilizationCredit
  + greatest of [ GF × (IndivLifeC2 + GroupLifeC2),  GF × LongevityC2,
                  sqrt( (IndivLifeC2 + GroupLifeC2)² + LongevityC2² + 2·ρ·(IndivLifeC2 + GroupLifeC2)·LongevityC2 ) ]
```

with **guardrail factor GF = 0** and **correlation ρ = −0.25** as stated on LR025-A, so the "greatest of" collapses to the square-root term in every non-degenerate case — the guardrail is present but switched off and the −25% mortality/longevity diversification credit applies in full [REG-R128][REG-R134]. Group life and health premium stabilization reserves give a **50% credit** against C-2, limited to the RBC otherwise calculated [REG-R128].

**C-3a: withdrawal-provision bucketing.** Why the categories key off the withdrawal provision is in the explainer, "Risk-based capital"; the operative table is below. Factors were built assuming well-matched durations and then loaded 50% for less well-matched portfolios [REG-R128]. The second figure applies where the company submits an **unqualified actuarial opinion based on asset adequacy testing** (or one qualified solely because of AG 48 direction) — a **one-third reduction** [REG-R128]:

| Risk category | Contents | Factor (pre-tax) |
|---|---|---|
| Low | annuity reserve **with fair value adjustment** (excluding unitized separate accounts); annuity reserve **not withdrawable** (excluding structured settlements); GIC reserve within 1 year of maturity; single premium life and life insurance reserves | 0.0095 → 0.0063 |
| Medium | annuity reserve at **book value less a surrender charge of 5% or more**; Exhibit 7 reserves not included elsewhere; **structured settlements**; additional actuarial reserves from asset/liability analysis; supplementary contracts without life contingencies and dividend accumulations | 0.0190 → 0.0127 |
| High | annuity reserve at **book value without adjustment** (minimal or no charge); debt with GIC-like characteristics | 0.0380 → 0.0253 |

The low-risk derivation is published: an assumed asset/liability duration mismatch of **0.125** with a possible **4% one-year interest rate swing** gives **0.0063**, loaded 50% for less well-matched portfolios to **0.0095**. **Equity-indexed products take the same factors as their non-indexed counterparts, based on guaranteed values ignoring those related to the index, and are excluded from C-3 cash flow testing.** Callable/pre-payable assets add an after-tax charge of **50% of the excess of BACV over current call price**, asset by asset, zero for assets used in C-3 cash flow testing or Phase II. All [REG-R128]. **When cash flow testing is compelled — LR049**, either test forces it [REG-R128]:

```
test 1 (significance): C-3a% = (factor-based C-3a on single premium and annuity reserves, excluding equity-indexed,
        + C-3a on all other reserves) ÷ (C-0 + C-1cs + C-1o + C-2 + both C-3a pieces + C-3b + C-3c + C-4a + C-4b)
        REQUIRED if C-3a% exceeds 40%
test 2 (stress): recompute the covariance formula substituting adjusted C-3a
        = [ line(17)×0.79 + line(16)×(1 − t) ] + [ line(17) × 6.5 × (1 − t) ] + all-other C-3a
        REQUIRED if Total Adjusted Capital ÷ that stressed RBC-after-covariance is less than 100% and non-zero
```

**The whole formula must therefore be computable before you know whether cash flow testing is required.** Companies with less than **$100 million** in admitted assets need not complete the line unless a test triggers, and once the cash flow method is elected it must be continued unless the domiciliary regulator approves reverting [REG-R128].

**The C-3 Phase I procedure** [REG-R128][REG-R135]. *Model:* the year-end asset adequacy cash flow testing model, or a consistent one, with the **same assumptions and "as-of" date**, but different interest scenarios and a different measurement. *Scope*, "Certain Annuities": deferred and immediate annuities, structured settlements, guaranteed separate accounts (excluding guaranteed indexed separate accounts on a Class II strategy), GICs including synthetic GICs and funding agreements, plus single premium life; **variable annuities are excluded, including guaranteed fixed options within them** (they go through Phase II). *Initial asset basis:* **initial assets = reserves** with no surplus assets; **AVR-related assets excluded** and future AVR contributions not modelled, though *expected* credit losses stay in the cash flows; **IMR assets are used**; profits retained, no stockholder dividends withdrawn, policyholder dividends and credited rates modelled realistically. *Scenarios:* the standard **50-scenario** set or the more conservative **12-scenario** set, different sets permitted for different products, horizon until surplus contributions on a closed block are immaterial, rates held constant at the year-30 level beyond the generator's 30 years. *Per-scenario statistic:* capture `S(t) = statutory assets − statutory liabilities` at every calendar year end; the scenario's C-3 measure is the **most negative of the series of present values S(t)·pv(t)**, discounting at **105% of the after-tax one-year U.S. Treasury rate** for that scenario. *Ranking and weighting:* rank descending, rank 1 = worst; for the 50-scenario set apply weights to ranks **17, 16, …, 5** of **0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.16, 0.12, 0.10, 0.08, 0.06, 0.04, 0.02** (peaking at rank 11) and sum the products; for the 12-scenario set take the **average of ranks 2 and 3, floored at half the worst**. *Assembly:* total C-3 = cash-flow-tested annuities and single premium life + equity-indexed on factors + all other on factors + the callable/pre-payable add-on, **but not less than half the C-3 component computed entirely on factors** (the 1999 design collared the result between half and double; only the half floor survives [REG-R135]). *Certification:* an appointed actuary **C-3 Assumption Statement** accompanies the filing, key assumptions must be stress tested (e.g. **lapses increased by 50%**), and if the actual result exceeds the year-end estimate by more than **5%**, or triggers regulatory action, a revised filing is due by **June 15**.

**C-3 Phase II for variable annuities.** Scope is "all policies and contracts that have been valued following the requirements of AG-43 or VM-21". Seven steps: (1) determine **CTE 98**, "the numerical average of the 2% largest values of the Scenario Reserves, as defined by Section 4 of VM-21", using the same process and methods as the reserve; (2) convert to a C-3 RBC amount by the formula below, floored at $0; (3) for **Alternative Methodology** contracts compute under Appendix 2 of the instructions; (4) C-3 RBC = (2) + (3) ≥ 0, and **Total Asset Requirement = the VM-21 reserve before any phase-in plus the C-3 RBC amount**; (5) phase in if a VM-21 §2.B reserve phase-in was elected; (6) smooth if elected — ratio = 0.4 × prior-year (C-3 RBC ÷ reserve) + 0.6 × current-year ratio, applied to the current-year aggregate reserve with voluntary reserves stripped from both years; (7) divide by (1 − enacted maximum federal corporate income tax rate) to reach a pre-tax amount and **split it into an interest rate component (→ C-3a, line 35) and a market risk component (→ C-3c, line 37)**, neither negative. All [REG-R128]. Two permitted tax methods. **Macro Tax Adjustment** — modelled cash flows ignore federal income tax so each Scenario Reserve is numerically identical to the VM-21 reserve calculation's, and tax enters through the formula, **reproduced exactly as printed**:

> `25% x ((CTE (98) + Additional Standard Projection Amount – Statutory Reserve) x (1 – Federal Income Tax Rate) – (Statutory Reserve – Tax Reserve) x Federal Income Tax Rate`

**The parentheses in the published text are unbalanced, so the intended bracketing of the second term is [unverified]** and is reproduced rather than silently resolved. The instruction's own gloss — that "the difference between statutory reserves and tax reserves multiplied by the Federal Income Tax Rate … may not exceed the portion of the company's non-admitted deferred tax assets attributable to the same portfolio of contracts to which VM-21 is applied" — supports reading it as a separate deduction with its own cap, but that is a reading, not the text [REG-R128]. Confirm against the RBC software or a current Academy practice note before coding. **Specific Tax Recognition** — tax is reflected inside the projection of Accumulated Deficiencies (VM-21 §4.A) with after-tax discounting, and `25% x (CTEAT (98) + Additional Standard Projection Amount – Statutory Reserve)`, with a **tax adjustment** where actual tax reserves exceed projected tax reserves at the projection start: increase CTEAT(98) by *corporate tax rate × f × (actual − projected tax reserves at t = 0)*, where **f = 1 − the average, across the CTE(98) scenarios, of the ratio of contracts in force at the scenario's greatest-present-value duration to contracts in force at the start**; under the Alternative Method **f ≈ 0.5** [REG-R128]. Switching from STR back to MTA requires prominent disclosure, and under STR the company must still disclose the TAR and C-3 RBC that MTA would have produced.

**The covariance combination, exactly as published** [REG-R128, LR031 line (69)]:

```
RBC after Covariance Before Operational Risk
  = C-0 + C-4a + Square Root of [ (C-1o + C-3a)² + (C-1cs + C-3c)² + (C-2)² + (C-3b)² + (C-4b)² ]

Gross Basic Operational Risk (70) = 0.03 × line (69)
Net Basic Operational Risk (72)   = (70) − ( C-4a post-tax + C-4a of U.S. life insurance subsidiaries ), floored at 0
AG 48 add-on (73)                 = Primary Security shortfall for all AG 48 cessions × 2
Total RBC After Covariance (74)   = (69) + (72) + (73)
Authorized Control Level RBC (75) = 0.50 × (74) ;   Mandatory Control Level RBC = 0.70 × Authorized Control Level RBC
```

The grouping is confirmed three ways inside that document — the blank line with superscripts intact, the narrative spelled out in words, and LR049 line (20). **C-3a is added to C-1o inside one squared term; C-3c is added to C-1cs (the Phase II instruction says the line (37) amount "is to be combined with the C-1cs component for covariance purposes"); C-2, C-3b and C-4b are standalone squared terms; C-0 and C-4a sit outside the radical.** All terms entering line (69) are post-tax, each pre-tax component having been netted against its tax effect on LR030; a parallel pre-tax tax-sensitivity test runs the same formula at line (76). The AG 48 doubling followed by the halving produces a **dollar-for-dollar** increase in Authorized Control Level for the shortfall, and applies even where a state has waived AG 48 compliance [REG-R128][REG-R11][REG-R12]. A **1% charge on admitted adjusted gross deferred tax assets** (SSAP No. 101 ¶¶11.a and 11.b) is applied **outside** the covariance adjustment, reduced to **0.5%** for the ¶11.a component where the insurer filed its own federal return or was in a consolidated return whose common parent is an insurance company [REG-R128]. A proposal to replace the square-root form with an explicit five-category correlation matrix exists but **is not in force** as of the 2024 instructions [REG-R137][REG-R128], as does a C-3 alignment project that would unify Phase I and Phase II and bring fixed indexed annuities into scope [REG-R138].

**Total Adjusted Capital** [REG-R128, LR033]: (1) Capital and Surplus (Page 3, Col 1, Line 38) × 1.000; (2) **Asset Valuation Reserve** (Line 24.01) × 1.000; (3) Dividends Apportioned for Payment (Line 6.1) × 0.500; (4) Dividends Not Yet Apportioned (Line 6.2) × 0.500; (5) Hedging Fair Value Adjustment × −1.000; (6) life subsidiary AVR prorated × 1.000; (7) life subsidiary dividend liability prorated × 0.500; (8) carrying value of non-admitted insurance affiliates × 1.000; (9) less non-tabular discount and/or Alien Insurance Subsidiaries–Other; (10) subtotal before capital notes; (11.4) plus the limited credit for capital notes; (12) less the XXX/AXXX Reinsurance RBC Shortfall; (13) **TOTAL ADJUSTED CAPITAL**. Why a liability counts in the capital numerator is in the explainer; the operative constraint on line (2) is that **the AVR included is limited to the amount not utilized in asset adequacy testing in support of the actuarial opinion for reserves** [REG-R128][REG-R29], so the AAT routine must report the AVR it consumed.

**Action levels and the trend test.** Company Action **2.0×**, Regulatory Action **1.5×**, Authorized Control **1.0×**, Mandatory Control **0.70×** Authorized Control Level RBC, with the **Authorized Control Level RBC Ratio = TAC ÷ ACL RBC** [REG-R125][REG-R128][REG-R127]. The trend test applies only where TAC is below the safe harbour of **3.0 ×** ACL RBC *and* the Level of Action is otherwise "None"; margin in a year = TAC − ACL RBC; the one-year decrease is prior-year margin − current-year margin floored at zero; the three-year average decrease is **⅓ × (third-prior-year margin − current-year margin)** (the exact wording of the intermediate line is **[unverified]** — it did not survive text extraction); **Marginal Difference = the greater of the two**; and **if TAC − Marginal Difference is less than 1.9 × ACL RBC the company triggers Company Action Level** [REG-R128]. The life safe harbour was **2.5× before the 2011 amendment raised it to 3.0×** [REG-R126].

---

## Worked example — one policy, carried through

Worked Example 1's endowment, on an expected (survivorship-weighted) basis per policy issued. Additional **[std]** assumptions: first-year commission **60% of premium**; maintenance expense **25** at BOY; earned rate **4.0%**; tax rate **21%**; net surrender value **0**; tax reserve per IRC §807 = max(NSV, 92.81% × statutory) capped at statutory [REG-R16].

| Year-1 item | Value | Year-1 item | Value |
|---|---|---|---|
| Premium (BOY) | 320.000000 | Closing statutory reserve = 306.544172 × 0.99 | 303.478731 |
| Acquisition expense 0.60 × 320, **expensed as incurred** [REG-R75 ¶2] | 192.000000 | Increase in aggregate reserves [REG-R90 Line 19] | 303.478731 |
| Maintenance expense (BOY) **[std]** | 25.000000 | **Pre-tax gain** = 320 + 4.12 − 10 − 217 − 303.478731 | **−206.358731** |
| Invested assets after BOY flows = 320 − 217 | 103.000000 | Tax reserve = 0.9281 × 303.478731 [REG-R16] | 281.658610 |
| Net investment income = 4.0% × 103 **[std]** | 4.120000 | Taxable income = 320 + 4.12 − 10 − 217 − 281.658610 | −184.538610 |
| Expected death benefits = 1,000 × 0.01 | 10.000000 | FIT at 21% (a benefit, assumed realizable **[std]**) | −38.753108 |
| | | **After-tax gain = end-of-year-1 surplus** | **−167.605623** |

Reconciliation, which must close exactly: assets = 0 + 320 − 217 − 10 + 4.12 + 38.753108 = 135.873108; surplus = assets − reserve = 135.873108 − 303.478731 = **−167.605623** ✓. RBC at the same date: NAR = face in force − reserve = (0.99 × 1,000) − 303.478731 = **686.521269**, and a non-participating endowment falls in **Permanent without Pricing Flexibility**, band 1 [REG-R128].

| RBC item | Calculation | Pre-tax | Tax factor **[std]** | Post-tax |
|---|---|---|---|---|
| C-2 mortality | 686.521269 × 0.00400 | 2.746085 | × 0.79 | 2.169407 |
| C-3a (low risk, life reserves, unqualified AAT opinion) | 303.478731 × 0.0063 | 1.911916 | × 0.79 | 1.510414 |
| C-4a | 320 × 0.0253 | 8.096000 | × 0.79 | 6.395840 |
| C-1o (assets 135.873108 at designation 1.A, size factor 1.00 **[std]**) | 135.873108 × 0.00158 | 0.214680 | × 0.79 | 0.169597 |

Covariance, with C-0 = C-1cs = C-3b = C-3c = C-4b = 0: `0 + 6.395840 + sqrt((0.169597 + 1.510414)² + 0² + 2.169407² + 0² + 0²) = 6.395840 + sqrt(2.822435 + 4.706328) = 6.395840 + 2.743859 = 9.139699`. Operational risk = 0.03 × 9.139699 = 0.274191, less C-4a post-tax 6.395840 → floored at **0**. Total RBC after covariance = 9.139699, so **Authorized Control Level RBC = 0.50 × 9.139699 = 4.569850** [REG-R128]. Two honesty flags: the **0.79 tax factor is [std]** — the per-component tax factors live on LR030 and were not transcribed by the research [REG-R128] — and the size factor of 1.00 is a toy, since a blank issuer count is charged **2.40** [REG-R128].

---

## Implementation notes and model architecture

**Layering**, four layers with one direction of dependency: (1) product models in `us/products/` emit cash flows and policy state; (2) a **valuation layer** turns state into reserves — CRVM, CARVM, NPR, DR, SR, VM-21/VM-22; (3) a **statutory ledger** turns cash flows plus reserve movements into Exhibits 5/6/7, the Analysis of Operations, the Analysis of Increase in Reserves, IMR, AVR and surplus; (4) a **capital layer** reads the ledger's statement values. Layer 4 reads statement values, not model values [REG-R128] — do not let it reach back into layer 1.

| Once per valuation | Once per scenario | Per projection path |
|---|---|---|
| CRVM/CARVM/NPR — prescribed assumptions, no scenario dependence [REG-R1][REG-R3] | SR scenario reserves [REG-R3 §5] | AVR and IMR balances |
| DR — a single prescribed scenario 12 [REG-R3 §4] | VM-21 Scenario Reserves: computed **once**, read **twice** at CTE 70 and CTE 98 [REG-R128] | statutory income and surplus |
| Additional Standard Projection Amount [REG-R128] | C-3 Phase I S(t) series [REG-R128] | projected annual statement for a forward RBC ratio |
| RBC factors, size bands, action-level multipliers | — | tax reserves and DTA scheduling |

**Practical ordering of a statutory reporting run.** (1) In-force extract and cash flow projection. (2) Formulaic reserves: CRVM, CARVM, deficiency, NPR. (3) Exclusion tests — SERT/DET and the VM-22 analogues — recording *how* each was passed, because that drives VM-G scope [REG-R109]. (4) DR and/or SR where required, per reserving category and aggregation subgroup. (5) Minimum reserve per category, allocated to policy in proportion to policy minimum NPR [REG-R3 §2.C]. (6) VM-21/VM-22 stochastic run, retaining the Scenario Reserve vector. (7) Exhibit 5/6/7 assembly with valuation-standard and year-of-issue keys, VM-20 business split NPR versus excess, VM-22 business split Jumbo/Non-Jumbo × 50bp bands [REG-R89]. (8) Asset adequacy analysis: starting assets whose statement value is **no greater than** the statement value of the reserves tested [REG-R29 §3.1][REG-R112], sign-aware IMR allocation and disclosed AVR allocation [REG-R100], producing any **additional reserve** — then **iterate**, because the additional reserve changes the reserves being tested and therefore the permitted starting assets. (9) IMR and AVR balances and the negative-IMR admittance test. (10) Income statement, Analysis of Increase in Reserves, surplus roll-forward. (11) Tax: tax reserves, temporary differences, DTA admittance. (12) RBC — which needs the AVR consumed in AAT and the opinion-qualification flag from step 8, and whose LR049 test needs the entire formula before you know whether C-3 cash flow testing was required. (13) Trend test and level of action. **Two circularities to break explicitly:** the DTA admittance percentage depends on the **ExDTA ACL RBC ratio**, computed *without* net deferred tax assets precisely so the loop terminates [REG-R97 ¶11]; and the AAT additional reserve depends on the reserve it is added to, so iterate to a fixed point with a stated tolerance **[std]**.

---

## Validation and reconciliation checks

1. **CRVM construction.** `APV₀(B) − k*·APV₀(G) = −E` exactly, so the reserve at issue floors to zero and the expense allowance equals E [REG-R1 §5.A].
2. **Reserve roll-forward closure.** Analysis of Increase in Reserves line 15 = line 8 − line 14, and that closing reserve equals an independent Mode-V valuation at t [REG-R90]; Exhibit 5A's life contract subtotal must agree with the "increase in reserve on account of change in valuation basis" line [REG-R89].
3. **Surplus reconciliation.** `S(t) = A(t) − L(t)` **and** `S(t) − S(t−1)` = after-tax gain plus the direct-to-surplus items — both, not either.
4. **Gross minus ceded.** `V_net = V_gr − V_ced`, the ceded credit on the **same mortality, interest and valuation method** reflecting the actual mode of reinsurance, with **no deduction for modified coinsurance** [REG-R89][REG-R92 ¶37]. The ceded column must be produced, not inferred by subtraction.
5. **CTE monotonicity.** From one Scenario Reserve vector, `CTE 70 ≤ CTE 98 ≤ max(ScenRes)`; a violation means reserve and capital did not come from the same run [REG-R128][REG-R35].
6. **VM-20 floors.** Minimum reserve ≥ Σ NPR in every category by construction; each NPR ≥ its §3.D floors; the total is the **sum** of the three category results, never a company-level maximum [REG-R3].
7. **TAC composition.** TAC ties to LR033 line by line; the AVR included is net of the amount consumed in asset adequacy testing; `ACL = 0.50 × total RBC after covariance` and `MCL = 0.70 × ACL` [REG-R128].
8. **Statement ties.** Exhibit 5 total → Liabilities page Line 1; IMR → Page 3 Line 9.4; AVR → Page 3 Line 24.01; change in non-admitted disallowed IMR → Page 4 Line 41 [REG-R89][REG-R87]. These are **2025** blank references and should be re-verified against the 2026 blank before being hard-coded [REG-R89][REG-R90].
9. **IMR grid.** The 30-year amortisation grid plus the "and later" row must sum to the balance before current-year amortisation [REG-R90].
10. **Classification immutability.** The life-versus-deposit-type flag is set at inception and **cannot change** [REG-R78 ¶5]; assert it never does, and assert the Exhibit 5 footnote (a) asymmetry — a contract life-contingent at issue stays in Exhibit 5 even after the mortality risk disappears [REG-R89].
11. **AAT starting assets.** Statement value of the chosen assets ≤ statement value of the reserves and other liabilities being tested [REG-R29 §3.1][REG-R112].

---

## Key sensitivities and model risks

- **Calendar-year-of-issue rate tables.** The valuation interest rate is a step function of issue year with a ±0.5% stability rule; one mis-set year silently misvalues an entire cohort [REG-R1 §4b].
- **The CRVM expense allowance cap** is the 19-pay whole life premium at age **x+1**, not x, and binds more often than intuition suggests on short endowments and high-premium designs [REG-R1].
- **CARVM path enumeration.** Omitting an elective-benefit path can only understate the reserve, and the interpretive guidance — AG 33 and AG 35 — was **not retrievable** [REG-R39][REG-R40].
- **Exclusion tests are cliffs.** A 6% SERT ratio drifting to 6.01% turns on the whole SR machinery and, depending on the route taken, VM-G Sections 2 and 3 as well [REG-R3][REG-R109].
- **Tail estimation.** CTE 70 and especially CTE 98 are averages of the worst 30% and worst 2%; at small scenario counts the CTE 98 estimate rests on a handful of paths [REG-R128][REG-R3].
- **Negative IMR is doubly cliff-edged** — a **300% ACL RBC** gate and a **10%** cap breachable by a surplus decline alone — and carries an **automatic nullification on January 1, 2027** as currently written [REG-R87]. Test admittance at every reporting date, not once.
- **AVR and IMR factor tables are not in this library.** They are published annually and were deliberately not transcribed [REG-R89]; a model that hard-codes remembered values will be wrong.
- **C-2 misclassification.** Modelling pricing flexibility off a product code misclassifies, and the default where the assessment is not performed is the **highest-factor** bucket [REG-R128][REG-R133].
- **Published-formula ambiguity.** The C-3 Phase II Macro Tax Adjustment formula has unbalanced parentheses in the source; the bracketing is **[unverified]** and must be confirmed before coding [REG-R128].
- **Double-counted default costs.** C-1 factors were parameterised at expected loss plus ½ standard deviation while PBR reserves cover CTE 70 and C-3 Phase I covers only expected — part of what the C-3 alignment project exists to fix [REG-R138].
- **Nested-valuation proxy error** is invisible in a base run and appears in the tail; §2.G requires a demonstration that the expected simplified reserve is not below the unsimplified one [REG-R3].
- **RILA has no RBC treatment to code.** The instructions read **never name registered index-linked annuities, ILVA or index-linked annuities at all** [REG-R128]. Whether a RILA lands in C-3 Phase II turns on whether it is valued under AG 43 / VM-21; otherwise it would take factor-based C-3, presumably on the equity-indexed convention. **Neither reading is sourced and both are [unverified]** [REG-R128] — see the explainer's product-applicability notes, where the `?` marks record the same hole.
- **Time-sensitive source risk.** The 2025 RBC instructions could not be parsed [REG-R129]; the revised SSAP No. 7 was not located [REG-R88]; the correlation-matrix and C-3 alignment proposals are **not in force** [REG-R137][REG-R138]. Re-check all four before relying on any parameter here for a current filing.
