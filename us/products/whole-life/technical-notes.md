# Whole Life Insurance — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03 (underlying research accessed 2026-08-03).

Scope note: these notes specify a reference liability cash flow projection model
(lifelib/modelx style) for the standardized composite products defined in `product-spec.md`
("RefWL-Par" participating whole life; "RefWL-FE" non-par final-expense whole life). They do
not describe any single insurer's model. [S#]/[R#] tags cite the product research file
(`us/_research/whole-life.md`); [REG-R#] tags cite the cross-product reference library
(`us/references/regulatory-and-actuarial-references.md`; research provenance in
`us/_research/regulatory-actuarial.md`, same R-numbering). **[std]** marks standardizations introduced for the
reference implementation. Parameter values are identical to those in `product-spec.md`.

---

## Model scope and conventions

- **Projection frequency: annual**, on policy years (anniversary to anniversary) **[std]**.
  Rationale: the contract's cash flow drivers — level annual premium, annual dividend
  declaration, anniversary loan-interest capitalization [S1] — are all annual. No
  monthiversary processing is performed; monthly modal premiums would enter only as a
  premium-income refinement via modal factors [S1] and are excluded by the annual-mode
  standardization (product-spec Table 2 note (f)).
- **Timing conventions [std]:** premiums and premium-linked expenses at the beginning of the
  policy year (BOY); death claims, dividends, surrenders, and maturity at the end of the
  policy year (EOY), in the processing order given below. State variables are stored at EOY
  (= policy anniversary t).
- **Age basis: age nearest birthday (ANB)** **[std]** (product-spec Table 1 note (a)); the
  2017 CSO set provides ANB tables [R8]. Attained age at anniversary t is `x + t`.
- **Projection horizon:** to the anniversary at attained age 100, where the model pays a
  maturity benefit and terminates **[std]**. The contract itself matures at 121 [S1], but the
  guaranteed CV equals face at 100 and PUA CV equals PUA face at 100 [S1][S3], so from age 100
  the policy is economically an endowment at face; truncating at 100 changes only the timing
  of the terminal payment between ages 100–121 (mortality vs. maturity), not its amount per
  survivor.
- **Model points:** single-policy model points, projected seriatim; results scale linearly in
  face within a band-free specification **[std]**. Amounts are U.S. dollars per policy;
  probabilities are per policy year.
- **Decrement model:** annual rates; deaths before surrenders at EOY; dividends credited to
  policies in force at EOY before surrender processing **[std]** (order list below).
- **Sex-distinct** rates throughout (unisex only as a variant) [S1][S3].

## Model point attributes

| Attribute | Type | Example |
|---|---|---|
| `policy_id` | str | "WLPAR-000001" |
| `product` | enum {WL_PAR, WL_FE_LEVEL, WL_FE_GRADED} | WL_PAR |
| `premium_period` | enum {TO_100, PAY_10, PAY_20, TO_65} | TO_100 **[std]** (product-spec Table 1 note (b); menu [S1][S3]) |
| `issue_age` (x) | int | 45 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum {PREF_NT, STD_NT, TOB} **[std]** | STD_NT |
| `face_amount` (F) | float | 100,000 **[std]** |
| `annual_premium` (G) | float | 1,800.00 **[std illustrative]** (product-spec Table 2 note (c)) |
| `dividend_option` | enum {CASH, REDUCE_PREM, ACCUM, PUA} | PUA (default [S1][S2]) |
| `pua_rider_premium` (A_t) | float per year | 0.00 |
| `term_blend_target` | float (0 = off) | 0.00 (variant: 2 × F **[std]**) |
| `loan_utilization` | float in [0,1] | 0.00 (variant: 0.20 **[std]**) |
| `duration_inforce` (t0) | int (0 for new business) | 0 |
| `puaf_inforce` | float (PUA face at t0) | 0.00 |
| `loan_inforce` | float | 0.00 |

## State variables

| Variable | Meaning | Initialization |
|---|---|---|
| `l_t` | Probability in force at anniversary t (per issued policy) | `l_0 = 1` |
| `CV_t` | Guaranteed cash value per policy (base), EOY t | table input; `CV_{100−x} = F` [S1][S3] |
| `PUAF_t` | Paid-up additions face in force, EOY t | `PUAF_0 = puaf_inforce` |
| `PUACV_t` | PUA cash value, EOY t | `PUAF_t · NSP_{x+t}` **[std]** |
| `DA_t` | Dividend accumulation balance (ACCUM option only) | 0 |
| `L_t` | Loan balance incl. capitalized interest, EOY t | `L_0 = loan_inforce` |
| `DB_t` | Death benefit payable on death in year t | formula below |
| `D_t` | Dividend credited at EOY t | recursion below |

## Assumption inputs

The model distinguishes three assumption classes. Keeping them in separate input structures is
deliberate: (a) is locked by contract, (b) is an insurer-declared snapshot that re-rates
annually, (c) is the modeler's experience basis.

### (a) Contractual / guaranteed elements (from the product spec)

| Input | Value | Basis |
|---|---|---|
| Guarantee interest `i_g` | 4.00% | [S1]; Model 808 floor [R1] |
| Guarantee mortality `q^g_{x+t}` | 2017 CSO composite, sex-distinct, ANB | [S1][R3][R8]; ANB **[std]** |
| Guaranteed CV schedule `CV_t` | Table input per model point (generated on the above basis) | [S1][R1]; see below |
| Gross premium `G` | Model point input (level, guaranteed) | [S1][S3] |
| Loan rate `i_L` | 6.00% fixed, in arrears | [S1] |
| Endowment/maturity | `CV = F` at age 100; model maturity at 100 | [S1][S3]; truncation **[std]** |
| FE premium rates | Per $1,000 rate table + $36 fee | [S7] |
| FE graded DB | 110% of premiums paid, natural death in years 1–2 | [S6][S7] |

### (b) Current non-guaranteed scale (insurer-declared; snapshot)

| Input | Value | Basis |
|---|---|---|
| Dividend interest rate `i_d` | 6.00% (2026-scale snapshot) | **[std]**, within observed 5.75%–6.60% [S4][S14] |
| Experience mortality in scale `q^{sc}_{x+t}` | `AE^{sc} · q^{2015VBT}_{x+t}` with `AE^{sc} = 0.70` of 2017 CSO in the worked example | **[std illustrative]**; structure per [S4][R6], tables [REG-R18] |
| Expense margin in scale `e^{m}_t` | $25 per policy per year | **[std]** |
| Dividend floor | `D_t ≥ 0` | **[std]** (dividends are non-negative distributions of surplus [R6]) |
| PUA purchase basis | `NSP_{x+t}` on 2017 CSO / 4%, unloaded (dividend purchases); 10% load on rider payments | **[std]** / [S3] (product-spec Table 3 note (k), Riders) |
| Accumulation option credit rate | `i_d` | [S2] rate declared annually; reuse of DIR **[std]** |

Non-guaranteed scales are constrained in illustration use by the disciplined-current-scale and
self-support / lapse-support machinery of Model 582 [R2] and ASOP 24 [REG-R30]; the model's
"current scale" should be interpreted as a currently-payable-scale snapshot, not a projection
of future scale changes.

### (c) Behavioral / experience assumptions (modeler-set; recommended public bases)

| Input | Recommended base | Reference value |
|---|---|---|
| Best-estimate mortality `q^e_{x+t}` | 2015 VBT (sex/smoker-distinct, ANB) × company A/E; industry A/E from the ILEC 2012–2019 study | tables [REG-R18], experience [R9]/[REG-R19]; A/E factor 0.70 × 2017 CSO in the worked example **[std illustrative]** |
| Base lapse `w_t` | LIMRA/SOA U.S. Individual Life Persistency study (WL by duration/size/mode) | [REG-R20] for the study; rates below **[std]** (study figures not recorded in the research file) |
| Lapse schedule **[std]** | 5.0% year 1, grading linearly to 2.0% at year 10, level 2.0% thereafter; 0 within 1 year of maturity | **[std]** — "low and level" pattern consistent with mature par WL persistency; source study [REG-R20] |
| Premium persistency | 1 (premiums are fixed and guaranteed; premium cessation = lapse/RPU) | [S1][S3]; convention **[std]** |
| Maintenance expense | $60 per policy per year, inflating 2.0%/yr | **[std]** |
| Acquisition expense | 90% of first-year premium + $250 per policy | **[std]** |
| Premium tax | 2.0% of premium | **[std]** |
| Loan utilization | 0% base; 20% of CV variant | **[std]** |

All experience values marked **[std]** are reference placeholders: no carrier experience data
is public in the research base; assumption governance patterns are per the Academy's PBR
Assumptions Resource Manual [REG-R25] and ASOP 56 model governance [REG-R32].

## Cash flow components and recursions

### Notation (defined once, used throughout)

```
x           issue age (ANB)                     t   policy year, t = 1 … 100 − x
F           base face amount                    G   gross annual premium
i_g         guaranteed interest (4.00%)         i_d dividend interest rate (6.00%)
i_L         policy loan rate (6.00%)            v_g = 1 / (1 + i_g)
q^g_{y}     2017 CSO rate at attained age y     q^e_{y}  best-estimate rate at age y
w_t         lapse rate in policy year t         l_t  in-force probability at EOY t
CV_t        guaranteed cash value (base), EOY t
NSP_y       net single premium per 1 of paid-up (endow-at-100) WL face at age y,
            on 2017 CSO / 4%:  NSP_y = A_{y:(100−y)|}  (endowment insurance to 100)
ä_{y:n|}    annuity-due, n years, on 2017 CSO / 4%
D_t         dividend credited at EOY t          PUAF_t, PUACV_t  PUA face / cash value
DA_t        dividend accumulation balance       L_t  loan balance at EOY t
DB_t        death benefit for deaths in year t  E_t  expense outgo in year t
```

### Guaranteed cash value: conceptual formula and practical treatment

Conceptual (Standard Nonforfeiture Law minimum, adjusted-premium / nonforfeiture-net-level-
premium method) [R1]:

```
NNLP      = F · NSP_x / ä_{x:(100−x)|}                       (net level premium, NF basis)
EA        = 0.01 · F + 1.25 · min(NNLP, 0.04 · F)            (expense allowance)  [R1]
P_adj     such that  P_adj · ä_{x:m|} = F · NSP_x + EA       (m = premium period)  [R1]
CV_t^min  = F · NSP_{x+t} − P_adj · ä_{x+t:(m−t)|}           (t < m; second term 0 for t ≥ m)
```

on 2017 CSO / 4% [S1][R1][R3]. Properties to verify: `CV_{100−x}^min = F` (since
`NSP_100 = 1`), and smooth progression by duration [R1].

Practical treatment **[std]**: the reference implementation reads `CV_t` (per $1,000 of face)
from a table input, because contractual CV tables are policy-form documents not publicly
available for the surveyed carriers (research gap noted in `us/_research/whole-life.md`). The
shipped table is generated from the formula above; an implementer replacing it with a carrier
table changes no other logic. Contractual `CV_t ≥ CV_t^min` always [R1].

### Dividend recursion (three-factor contribution formula)

Anchor (published mechanics, Northwestern Mutual) [S4]:

```
D_t = ( CV_{t−1} + G − MEC_t ) · (1 + i_d) − CV_t
```

where `MEC_t` is the mortality-and-expense charge based on actual company results — i.e., the
dividend is the excess of an experience-basis accumulated value over the guaranteed value [S4].

Reference parametrization **[std]** (exact carrier factor formulas are proprietary; this is the
classic three-factor contribution decomposition consistent with [S4] and the contribution
principle [R6]):

```
D_t = D^int_t + D^mort_t + D^exp_t ,   floored at 0
D^int_t  = (i_d − i_g) · (CV_{t−1} + NP_g)                       (interest margin)
D^mort_t = (q^g_{x+t−1} − q^{sc}_{x+t−1}) · (F − CV_t)           (mortality margin)
D^exp_t  = e^m_t                                                  (expense margin)
```

with `NP_g = NNLP` (the nonforfeiture net level premium, so the interest margin applies to the
guaranteed fund including the year's net premium) **[std]**, `q^{sc}` the scale's experience
mortality (class (b)), and `e^m_t` the per-policy expense margin (class (b)). Dimensions: every
term is dollars per policy per year. Refinements observed in practice — interest on the
mortality margin, premium-timing adjustments, banded factors [S1][S3] — are absorbed into the
calibration of `q^{sc}` and `e^m_t` **[std]**.

Dividends on the PUA block (PUAs are dividend-eligible [S14]) **[std]**:

```
D^PUA_t = (i_d − i_g) · PUACV_{t−1} + (q^g_{x+t−1} − q^{sc}_{x+t−1}) · (PUAF_{t−1} − PUACV_{t−1})
```

No dividend is credited for policy year 1 (`D_1 = D^PUA_1 = 0`) **[std]** (product-spec Table
3 note (j); Guardian pays none [S1], MassMutual pays a first-year dividend [S3]).

Direct recognition (loaned values) **[std]** parametrization of [S1][S3]: replace `i_d` with
`i_L` on the loaned portion:

```
D^int_t (adjusted) = (i_d − i_g) · (CV_{t−1} + NP_g − L_{t−1}) + (i_L − i_g) · L_{t−1}
```

With `i_L = 6.00%` [S1] and the snapshot `i_d = 6.00%` **[std]** the adjustment is zero — a
coincidence of the snapshot, not a model property.

### Dividend application (by option)

- **PUA (default [S1][S2]):** `ΔPUAF_t = (D_t + D^PUA_t) / NSP_{x+t}`; `PUAF_t = PUAF_{t−1} +
  ΔPUAF_t`; `PUACV_t = PUAF_t · NSP_{x+t}` **[std]** (valuing all PUA face at the attained-age
  NSP on the guarantee basis; exact at issue of each layer and at age 100, approximate between
  **[std]**). At age 100, `NSP_100 = 1` so `PUACV = PUAF` [S1].
- **CASH:** dividend paid out; policyholder cash flow at EOY.
- **REDUCE_PREM:** offsets next year's BOY premium: `G^{net}_{t+1} = max(G − D_t, 0)`, excess
  to PUAs **[std]** (excess-to-PUA per MassMutual RPD [S3]).
- **ACCUM:** `DA_t = DA_{t−1} · (1 + i_d) + D_t`; balance adds to death and surrender
  proceeds [S1][S2].

### PUA rider (in-scope rider)

Rider payment `A_t` (BOY, within limits set at issue [S3][S11]):
`ΔPUAF^rider_t = A_t · (1 − 0.10) / NSP_{x+t−1}` — 10% load **[std]** from the observed
7.5%–10% range [S3]. Rider PUAs merge into `PUAF_t`.

### Term-blend rider (in-scope rider, simplified **[std]**)

Target face `TF = 2 F` **[std]** (within observed caps: ≤ 9× base [S2], ≤ 300% of base [S3]).
Each year, OYT face `= max(TF − F − PUAF_t, 0)`; the dividend first pays the OYT cost
`q^{sc}_{x+t} · OYT_t · v_g` **[std]**, remainder buys PUAs; crossover when `PUAF_t ≥ TF − F`,
after which the rider is pure PUA [S2][S3][S11]. Death benefit while blended: `TF + excess
PUAs − L_t`.

### Benefit amounts

```
DB_t   = F + PUAF_{t−1} + DA_{t−1} − L_{t−1}                 (PUA/ACCUM components as elected)
CSV_t  = CV_t + PUACV_t + DA_t − L_t                          (surrender value, EOY t)
MAT    = F + PUAF_T + DA_T − L_T   at T = 100 − x             (model maturity [std])
```

`DB` per the contractual formula [S1], reduced to modeled components **[std]**. Deaths in year
t are assumed to occur at EOY before the year-t dividend is credited, so `DB_t` carries the
prior year's PUA face **[std]** (terminal-dividend and premium-refund items not modeled,
product-spec Table 3 note (m)).

### Annual processing order (policy year t, per unit in force `l_{t−1}`)

1. **BOY:** collect gross premium `G` (if `t ≤` premium period) and PUA rider premium `A_t`;
   pay premium tax and acquisition/maintenance expense `E_t`.
2. **BOY:** apply REDUCE_PREM offset from `D_{t−1}` if elected.
3. **During year:** interest accrues implicitly (CV table on `i_g` [S1]; loan at `i_L` [S1]).
4. **EOY — deaths:** probability `q^e_{x+t−1}`; outgo `q^e_{x+t−1} · l_{t−1} · DB_t`.
5. **EOY — loan interest capitalization:** `L_t = L_{t−1} · (1 + i_L)` less repayments [S1].
6. **EOY — dividend:** credit `D_t + D^PUA_t` to survivors (from t = 2 **[std]**); apply per
   dividend option; update `PUAF_t, PUACV_t, DA_t`.
7. **EOY — surrenders:** probability `w_t` applied to survivors
   `l_{t−1} · (1 − q^e_{x+t−1})`; outgo `= CSV_t` per surrendering policy.
8. **Update in force:** `l_t = l_{t−1} · (1 − q^e_{x+t−1}) · (1 − w_t)`.
9. **At T = 100 − x:** pay `MAT · l_T`; terminate **[std]**.

Ordering (deaths → dividend → surrenders at EOY) is **[std]**; it makes surrender values
include the just-credited dividend, consistent with anniversary processing.

### Net liability cash flow (per issued policy, year t)

```
NetCF_t = − G^{net}_t · l_{t−1} − A_t · l_{t−1} + E_t · l_{t−1}          (BOY items, sign: outgo +)
          + q^e · l_{t−1} · DB_t + w_t · l_{t−1}(1 − q^e) · CSV_t        (EOY benefits)
          + D^{cash}_t · l_{t−1}(1 − q^e) + MAT · l_T · 1{t=T}           (cash dividends, maturity)
```

Internal dividend applications (PUA, ACCUM, REDUCE_PREM) are not cash flows when credited;
they emerge later through `DB`, `CSV`, and `MAT` **[std]**. Loans are modeled on the offset
view: see next.

### Loans (offset treatment — brief)

Base run: `loan_utilization = 0`. Variant **[std]**: `L_t = 0.20 · CV_t` maintained by
borrowing/repaying at EOY; borrowed amounts are policyholder cash outflows from the insurer,
loan interest received is an inflow, and `DB`/`CSV`/`MAT` are net of `L_t` [S1][S3][S9]. Under
direct recognition the dividend adjustment above applies [S1][S3]. Economically the loan is an
offsetting asset; the reference model reports gross liability flows plus a separate loan
account rather than netting into a "net amount at risk" presentation **[std]**.

### RefWL-FE variant deltas

- Premium: `G = (F/1000) · rate(x, sex, tobacco) + 36` [S7]; no dividends (non-par
  [unverified]; modeled non-par).
- Graded plan: for natural-cause deaths in years 1–2, `DB_t = 1.10 · (cumulative premiums
  paid)`; accidental deaths pay `F` from day 1 [S6][S7]. Accidental split requires an
  accidental-death fraction of `q^e` **[std]** (reference value 3% of deaths **[std]**).
- Maturity at age 100 (120 in FL — not modeled **[std]**) pays `F − L_T` [S8].
- CV schedule: reuse of the par nonforfeiture machinery **[std]** (product-spec Table 5 note (r)).
- Lapse: FE simplified-issue business lapses higher than par WL; reference schedule 12% year 1,
  10% year 2, grading to 6% level by year 5 **[std]** (no FE-specific study in the research
  base; flagged as an open issue).

## Policyholder behavior modeling

Base behavior is static (schedules in class (c)). Dynamic overlays, all **[std]**:

- **Interest-sensitive lapse multiplier** (for scenario runs):
  `w_t^dyn = w_t · min(1 + 2.0 · max(0, r^{cmp}_t − i_d − 0.01), 3.0)` where `r^{cmp}_t` is
  the competitor/market rate in the scenario. Rationale: par WL cash values are liquid at book
  value, so sustained rate spreads induce excess surrender; the low base level reflects the
  strong persistency of dividend-paying WL. Calibration is judgmental **[std]** — the research
  base records no dynamic-lapse study for WL.
- **Premium offset behavior:** once `D_t ≥ G` (dividend covers the premium), a fraction
  `0.50` **[std]** of policyholders switch to REDUCE_PREM/premium-offset behavior (offset is a
  real product feature: Guardian option S [S2]; MassMutual APO [S3]). This shifts premium
  income to internal dividend application in later durations.
- **Loan utilization:** static 0%/20% variants only **[std]**; no dynamic loan take-up (the
  6%-fixed direct-recognition design largely neutralizes loan arbitrage [S1][S3]).
- **No dynamic mortality (anti-selection) on lapse** for the base par product **[std]**;
  selective-lapse mortality loading is documented mainly for term post-level-period designs
  (see the SOA persistency/PLT study family around [REG-R20]), not level-premium par WL.

## Worked example

Single-year walk-through of the core recursion: RefWL-Par, male Standard NT, `x = 45`,
`F = 100,000` **[std]**, `G = 1,800` **[std illustrative]**, PUA dividend option, no rider, no
loan. Policy year `t = 10` (attained age 55 at EOY). All table values are illustrative
**[std]** (the shipped CV/NSP tables are generated on 2017 CSO / 4% as specified above);
`i_g = 4.00%` [S1], `i_d = 6.00%` **[std]**.

| Step | Item | Formula | Value |
|---|---|---|---|
| 1 | Guaranteed CV, BOY (EOY 9) | `CV_9` (table) | 9,500.00 **[std]** |
| 2 | Guaranteed CV, EOY | `CV_10` (table) | 11,200.00 **[std]** |
| 3 | Net level premium (NF basis) | `NP_g` | 1,300.00 **[std]** |
| 4 | Guarantee mortality, age 54 | `q^g_54` | 0.00320 **[std]** |
| 5 | Scale mortality, age 54 | `q^{sc}_54 = 0.70 · q^g_54` | 0.00224 **[std]** |
| 6 | Interest margin | `(0.06 − 0.04) · (9,500 + 1,300)` | 216.00 |
| 7 | Mortality margin | `(0.00320 − 0.00224) · (100,000 − 11,200)` | 85.25 |
| 8 | Expense margin | `e^m_10` | 25.00 **[std]** |
| 9 | Dividend | `D_10 = 216.00 + 85.25 + 25.00` | 326.25 |
| 10 | NSP at age 55 | `NSP_55` (table) | 0.42 **[std]** |
| 11 | PUA face purchased | `ΔPUAF = 326.25 / 0.42` | 776.79 |
| 12 | PUA face, EOY (prior 4,100.00 **[std]**) | `PUAF_10 = 4,100.00 + 776.79` | 4,876.79 |
| 13 | PUA cash value, EOY | `PUACV_10 = 4,876.79 × 0.42` | 2,048.25 |
| 14 | Death benefit for year 11 deaths | `F + PUAF_10` | 104,876.79 |
| 15 | Surrender value, EOY 10 | `CV_10 + PUACV_10` | 13,248.25 |

(For clarity the PUA-block dividend `D^PUA_10` is omitted from this table; in the model it
adds `(0.02 · PUACV_9) + (0.00096 · (PUAF_9 − PUACV_9))` to the amount in step 9 **[std]**.)

## Statutory accounting and capital

Framework and the shared model-output contract live in
`us/regulatory/statutory-accounting-and-capital.md` (concepts, formulas, algorithms and the
product-applicability matrix); only what is specific to RefWL-Par and
RefWL-FE is recorded here. **Source limits, reproduced at the point of use:** every RBC factor below
is from the **2024** Life/Fraternal RBC instructions, a sold NAIC publication read from a state
posting — the **2025 edition could not be parsed and no year-end 2025 factor is asserted**
[REG-R128][REG-R129]; and **no AVR or IMR factor value exists anywhere in this library**, the
research having deliberately not transcribed them [REG-R89]. **One limit has been lifted.** The AP&P
Manual is a **free download**, not the paid publication the library recorded [REG-R73], and its
**A-820** — the codification of the Standard Valuation Law, with A-821 and A-822 — and **A-830**
have now been read in full [REG-R153][REG-R154]. The formulaic CRVM statements below therefore no
longer rest on the Standard Valuation Law print [REG-R1] and the separately published Model #830
alone. **Still unread and named where relied on:** the **Actuarial Guideline I** text behind
deficiency reserves [REG-R41]; **A-817**, the preneed appendix that A-820 ¶5 carves out of its own
ordinary-life mortality rules [REG-R153 ¶5]; and **A-791**, cited only through SSAP No. 61
[REG-R92].

### Contract classification and reporting

Both designs are **life contracts** — the SSAP No. 50 ¶5 test is that the entity assumes mortality
risk, which a death-contingent benefit does, and whole life heads the life-contract list
[REG-R78 ¶¶5, 9] — classified **at inception, immutably**, ¶5 also being where classification is
fixed at inception and barred from changing [REG-R78 ¶5]: a per-model-point flag set at issue,
never re-derived. The reserve reports in **Exhibit 5** (Liabilities page Line 1), the block in the
annual statement's own **Whole Life** column of the Analysis of Operations and the Analysis of
Increase in Reserves, and face in force in the **Exhibit of Life Insurance** [REG-R89][REG-R90].
Considerations are **premium income, gross when due**, not a direct credit to reserve — that is
the deposit-type treatment this contract never takes [REG-R79 ¶¶2–5][REG-R80 ¶6]; PUA rider
payments `A_t` are premium on the same basis, and the
gross-to-net **loading** difference is an *expense*, not a reduction of premium [REG-R79 ¶11]. The
annual-mode standardization leaves no deferred and uncollected premium asset and no loading change;
a modal run creates both (mean reserves at [REG-R81/IP51 ¶21]), and in a VM-20 projection deferred
premiums are zero [REG-R3 §7.B]. Riders report on the **base contract's line**, so both in-scope
riders and an A&H disability waiver rider reserve report as Whole Life [REG-R82][REG-R89].
**One balance is genuinely unsettled:** SSAP No. 52 ¶5 names **dividend accumulations** among
deposit-type candidates and Exhibit 7 carries a dividend accumulations column [REG-R80][REG-R89],
yet the product-applicability matrix leaves whole life blank on both rows — the sources read do not
settle where a par WL's `DA_t` reports, and the same question decides its C-3a bucket below.

### Reserve basis

**Formulaic:** CRVM under Standard Valuation Law §5, on the mortality table and valuation interest
rate fixed by **calendar year of issue** (§4b), with the §6.A aggregate nonforfeiture floor and the
§6.B floor at the amount the appointed actuary needs to render the opinion [REG-R1]; mean or
mid-terminal reserve per [REG-R81/IP51 ¶21]. **That construction is no longer second-hand.**
AP&P **Appendix A-820**, the codification of the Standard Valuation Law, has been read in full, and
**¶11 confirms the RefWL chassis element by element**: modified net premiums are a **uniform
percentage of the respective contract premiums**; the expense allowance is the excess of `a.` (the
APV at issue of the benefits provided **after the first policy year**, over the premium-paying
annuity-due, **capped at the net level annual premium on the nineteen-year premium whole life plan
at an age one year higher than the issue age**) over `b.` (a net one-year term premium for the
first-year benefits); and the reserve is "the excess, **if any**" [REG-R153 ¶11]. No discrepancy was
found between the two prints, so [REG-R1 §5] and [REG-R153 ¶11] are independent citations for the
same machinery. Three refinements this product needs. (i) **¶11 governs only the uniform-amount,
uniform-premium base policy.** A PUA block and a term blend are neither, and A-820 prints no
construction for them: the hooks are **¶13.a** (life insurance policies providing for a *varying
amount of insurance* or requiring *varying premiums*, valued by a method "consistent with the
principles of paragraphs 11 and 12") and **¶21** (plans whose minimum reserves cannot be determined
by the methods described, reserved on a basis "appropriate in relation to the benefits and the
pattern of premiums" and "consistent with the principles of this Appendix") — both are *directions*,
not formulas, so the PUA and blend reserve method stays a modelling choice **[std]** and is now
documented as such rather than as an unsourced gap [REG-R153 ¶¶13.a, 21]. (ii) **The waiver and
accidental-death riders route separately:** ¶13.c puts disability and accidental death benefits in
*all* policies on a CRVM-consistent method, and ¶5.d/¶5.e give their bases — Period 2 disablement
with 1930–1950 termination rates from the 1952 Disability Study, and the 1959 Accidental Death
Benefits Table, each **combined with a mortality table permitted for life insurance reserves**
[REG-R153 ¶¶5.d, 5.e, 13.c]. Neither table is printed in A-820. (iii) **The valuation interest rate
is now computable rather than merely named.** ¶7.a.i(a) prescribes, for life insurance,
`I = .03 + W(R1 − .03) + (W/2)(R2 − .09)` with `R1 = min(R, .09)`, `R2 = max(R, .09)`, **rounded to
the nearer one-quarter of one percent** and **no tie-break prescribed**; `R` is the **lesser of the
36-month and 12-month averages of the Moody's composite yield on seasoned corporate bonds, each
ending June 30 of the calendar year *preceding* the year of issue** (¶9.a); `W` comes from the ¶8.a
life table — **.50** for a guarantee duration of 10 years or less, **.45** over 10 and up to 20,
**.35** over 20 — where guarantee duration for life insurance is "the maximum number of years the
life insurance can remain in force on a basis guaranteed in the policy". **That is a per-model-point
lookup, not a product constant:** RefWL-Par runs to contractual maturity at 121, so `121 − x > 20`
at every issue age in the menu and it always takes **W = .35**; RefWL-FE matures at 100, so
`100 − x > 20` only for issue ages up to 79 and **issue ages 80–85 fall in the "more than 10, but
not more than 20" band at W = .45** — a band change inside a single product's issue-age range, on a
product whose issue ages run 45–85. ¶7.a.ii then adds a **life-only stability rule** — a rate
differing from the
*actual* prior calendar year's rate by less than **one-half of one percent** is set equal to it, so
the recursion runs on the published series, not on a freshly recomputed one. ¶10 requires an
NAIC-adopted alternative if Moody's ceases publication, which is why the reference series must be a
**configurable table keyed by calendar year**, never a hard-coded feed [REG-R153 ¶¶7–10]. **Two
caveats survive intact.** A-820 **never names the 2017 CSO**: ¶5.a prescribes the 2001 CSO (or the
2001 CSO with 25-Year Select Mortality Factors) for standard-basis ordinary issues from 1 January
2004, and the 2017 CSO can enter only through ¶5.a.iii's forward reference to tables "adopted
subsequently by the NAIC" or, for post-operative-date issues, through the Valuation Manual under ¶23
— so **this product's 2017 CSO basis remains sourced to VM-02 [R3], not to A-820** [REG-R153 ¶¶5.a,
23]. And ¶7's own applicability threshold is "the effective date of the Codification", **a date
A-820 never prints** — do not supply one [REG-R153 ¶7]. **A citation correction on the second
aggregate floor:** the library has been citing SVL §6.B for the rule that makes asset adequacy
analysis part of *minimum* reserves; **A-820 as printed contains no §6.B analogue** — its ¶16 carries
only the aggregate nonforfeiture-basis floor, and that floor is **aggregate across all life insurance
policies, not seriatim, and expressly excludes disability and accidental death benefits**. In the
manual the additional reserve sits in the four-paragraph **Appendix A-822**, at its ¶3 — "the company
**shall establish** the additional reserve" [REG-R153 ¶16][REG-R153]. Note the naming trap that
comes with it: AP&P **Appendix A-822 is not NAIC Model #822**, the Actuarial Opinion and Memorandum
Regulation; it carries no opinion wording, no scenarios and no memorandum requirements [REG-R153].

**A-830 is a near-miss for this product, and the near-miss is the finding.** Its ¶2 declares that
*its* basic-reserve method constitutes CRVM for the policies it reaches, and ¶3 reaches "all life
insurance policies" subject to six exceptions; but **¶3.b routes only nonlevel-guaranteed-premium or nonlevel-guaranteed-benefit
non-UL designs (→ ¶¶21–28) and UL with a secondary guarantee (→ ¶¶29–32)**. A level-premium,
level-benefit par whole life is inside the ¶3 scope sentence and inside ¶2's declaration **with no
calculation paragraph of its own** — that is an observation about the print, **not** a licence to
infer an outcome, and the base-policy reserve therefore still runs on A-820 ¶11 [REG-R154 ¶¶2, 3].
The **term-blend rider is the component A-830 would reach**: a one-year-term layer has neither level
guaranteed premiums nor a level guaranteed benefit, which is exactly ¶3.b's first routing condition,
and ¶26 carries an optional exemption for **attained-age-based YRT** policies (premium rates on both
the initial current and guaranteed maximum scales independent of issue year and identical across
insureds of the same sex, risk class, plan and attained age) that is an **all-or-nothing company-level
election** under ¶26.g, not a per-policy one. **A-830 does not say whether a rider is valued as a
policy for ¶3.b purposes**, so that routing step is an inference — **[unverified]** [REG-R154 ¶¶3.b,
26].

**Principle-based:** VM-20 constitutes CRVM for individual life subject to a principle-based
valuation [R3][REG-R1 §11]. **The statutory-law trigger is year of issue and the date it prints is
1 January 2017:** A-820 ¶3 applies the Valuation Manual standard to all policies issued on or after
"the **January 1, 2017**, operative date of the Valuation Manual", and ¶4 grandfathers earlier issues
onto ¶¶5–22, adding that the PBR provisions "**shall not apply to any such policies and contracts**"
[REG-R153 ¶¶3–4]. **A-820 contains no elective-transition window, no phase-in and no company
election anywhere**, so the 2020-01-01 date this library has attached to VM-20 for ordinary life —
which is the PBR *accreditation* standard year — is **not** confirmed as a reserve-election trigger
and stays **[unverified]**; ¶24.e delegates "transition rules" to the Valuation Manual, so if such an
election exists it lives in VM-20/VM-01, not in the statutory-law layer [REG-R153 ¶¶3, 4, 24.e]. Whole
life is the **All Other** reserving category, whose net premium reserve is itself determined
"pursuant to applicable methods in VM-A and VM-C" [REG-R3 §3.B.6][REG-R110] — and **the
statutory-layer half of that sentence is now sourced too**: the Valuation Manual **must** specify
"the commissioners reserve valuation method for life insurance contracts" (¶24.a.i); for policies not
subject to a principle-based valuation the minimum standard may simply "**be consistent with the
minimum standard of valuation prior to the operative date of the Valuation Manual**" (¶24.d.i); and
"**a principle-based valuation may include a prescribed formulaic reserve component**" (¶27)
[REG-R153 ¶¶24.a.i, 24.d.i, 27]. So **the formulaic engine is not legacy code**: it computes the NPR
for this product inside a PBR-era manual, and it is also what a Life PBR Exemption company uses
outright [R3]. Consequences specific to this product:

- **The deterministic exclusion test is available and normally passed**: Σ future valuation net
  premiums against Σ corresponding **guaranteed gross premiums** [REG-R3 §6.B]. The dividend never
  enters that comparison, so premium-offset behaviour cannot fail it — the substantial guaranteed
  gross premium is what passes it [R3]; a closed group passing three consecutive years is thereafter
  tested at least every five [§6.B.4]. But the test is **barred entirely for term riders** [§6.B]:
  a RefWL-Par carrying the term-blend rider has a component for which it is unavailable, and that
  component sits in the **Term** reserving category on §3.B.4 prescribed and shock lapses. The
  minimum reserve is a **sum** across categories, so Term excess cannot offset All Other slack
  [§2.A, §4.C] — reporting column (Whole Life) and reserving category (Term) are different dimensions
  needing separate model keys. The split runs the same way on the formulaic side: the term-blend
  component is the one A-830 ¶3.b would route to ¶¶21–28 while the base policy stays on A-820 ¶11
  (above), so the blend needs its own key whichever regime the block is in. Whether the *one-year
  term dividend option* is a "term rider" for §6.B is not addressed by the sources read —
  **[unverified]**.
- **The stochastic exclusion certification method is available** to whole life, barred only for
  variable life and ULSG [REG-R3 §6.A]; the route taken is a governance fact, since passing by the
  SERT's deterministic-reserve method or the Demonstration Test **re-imposes VM-G Sections 2 and 3**,
  and a company computing no DR or SR still files a VM-31 sub-report and must report readiness to
  compute them [REG-R109][REG-R108].
- **The NPR floor is the cash surrender value** — for non-UL, the greater of the cost of insurance to
  the next paid-to-date and the CSV [REG-R3 §3.D]. The guaranteed CV schedule *is* a reserve floor,
  not only a benefit, and the quantity to floor on is `CSV_t = CV_t + PUACV_t + DA_t − L_t`. A
  formulaic reserve below the immediately available surrender value leaves a gap carried as
  "surrender values in excess of reserves otherwise carried" in Exhibit 5 Miscellaneous Reserves
  [REG-R89][REG-R81/IP51 ¶28]. **A difference in kind the model must not paper over:** A-830's
  parallel floor at ¶23 is on **total** reserves — basic plus deficiency plus reserves for
  supplemental benefits expiring on termination — and is expressly the amount the policyowner would
  receive "**exclusive of any deduction for policy loans**" [REG-R154 ¶23], where the quantity this
  product floors on nets `L_t` off. Whether VM-20 §3.D's "cash surrender value" is gross or net of
  policy loans **is not addressed by the sources read** — **[unverified]**; record the convention
  chosen rather than inferring one.
- **Deficiency reserves now have a retrieved formulaic construction.** A-820 ¶19 expresses the
  deficiency **as a floor on the policy reserve, not as a separate additive reserve**: where in any
  contract year the gross premium charged is less than the valuation net premium computed **by the
  method actually used** but on the **minimum** standards of mortality (¶5) and interest (¶¶7–10),
  the minimum reserve is `max(V_actual, V_def)`, `V_def` being that same method on the minimum
  standards with **the actual gross premium substituted for the valuation net premium only in the
  deficient years** [REG-R153 ¶19]. ¶20 adds that for an excess-first-year-premium design the ¶19
  test is run **as if the method actually used were ¶11 CRVM**, and the reserve is the greater of the
  ¶¶11–12 and the ¶¶19–20 minimums [REG-R153 ¶20] — which **no RefWL variant as specified triggers**,
  every one of them having a level guaranteed premium, but which a design whose first-year premium
  exceeds its second-year premium with no comparable extra first-year benefit would. For a
  component A-830 reaches, the construction is different in shape: the deficiency reserve is
  **quantity A less the basic reserve**, A being a full re-run of the basic reserve with the
  **guaranteed** gross premium substituted for the net premium duration by duration wherever the
  gross is the smaller, on the basis (segmented or unitary) that won the ¶21 maximum [REG-R154 ¶¶6,
  17, 22]. Note the two triggers are not worded alike — A-820 ¶19 keys to the **gross premium
  charged**, A-830 ¶7 to the **guaranteed gross premium**, "guaranteed and determined at issue"; for
  a level guaranteed-premium whole life they coincide, for a rider they need not. **Actuarial
  Guideline I, the interpretive vehicle indexed by VM-C, is still unretrieved** [REG-R41] — the base
  mechanic is no longer second-hand, the interpretation is.
- **Change in valuation basis** goes direct to surplus at beginning-of-year values, is not graded in
  and is excluded from the Summary and Analysis of Operations [REG-R79][REG-R89]; a 55-year product
  carries more years-of-issue cohorts than anything else here, and Exhibit 5 Column 1 states the
  standard **by years of issue** [REG-R89]. **What counts as such a change is now sourced on both
  sides.** A-820 ¶17 permits an optional **higher** standard for any category of policies, contracts
  or benefits producing greater aggregate reserves, with a constraint the library did not carry: for
  policies **other than annuity and pure endowment contracts** the interest rate used may **not
  exceed the rate used in calculating the nonforfeiture benefits** — so on the representative
  4.00%/2017 CSO guarantee basis, an elective strengthening of this product may not be taken at a
  valuation rate above **4.00%** [REG-R153 ¶17]. ¶18 permits reverting to a lower standard but not
  below the minimum, with the proviso that "**the holding of additional reserves previously
  determined by the appointed actuary shall not be deemed to be the adoption of a higher standard of
  valuation**" [REG-R153 ¶18]; A-822 ¶4 is its mirror — the release of an asset-adequacy additional
  reserve "would **not** be deemed an adoption of a lower standard of valuation" [REG-R153]. That
  pair keeps both the establishment and the release of the asset adequacy reserve **outside** the
  change-in-valuation-basis machinery, in both directions.

### What this product's model must additionally produce

The shared contract in `us/regulatory/statutory-accounting-and-capital.md`, "Required model
outputs", applies in full and is not restated. What RefWL-Par/RefWL-FE must add or specialise:

| Statutory item | Whole-life-specific model output |
|---|---|
| Exhibit 5, standard by years of issue [REG-R89] | reserve keyed by (year of issue, CSO table, `i_v`), base and PUA layers separable; `i_v` itself is now a computed quantity, not an input — the ¶7.a.i(a) life formula with `W` looked up **per model point** from the ¶8.a guarantee-duration table, a **configurable calendar-year Moody's reference table** behind `R`, and the ¶7.a.ii half-of-1% stability rule applied against the *published* prior-year rate [REG-R153 ¶¶7–10] |
| Exhibit 5 Miscellaneous Reserves [REG-R89] | `max(0, CSV_t − V_t)` per policy per duration; a deficiency reserve if the DET is ever failed |
| Exhibit of Life Insurance [REG-R89] | face in force `= F + PUAF_t` (+ term-blend face), in thousands, on an incurred roll-forward |
| Analysis of Increase in Reserves [REG-R90] | tabular net premium, tabular interest at `i_v`, tabular cost on **valuation** mortality — a **fourth** basis alongside `q^g/i_g`, `q^{sc}/i_d`, `q^e` — plus line 16 ending CSV and line 17 loan value available on it |
| Policyholder dividends [REG-R90][REG-R128] | the declared dividend as its **own deduction line** (not a benefit, not an expense), *and* the apportioned / not-yet-apportioned dividend **liability** balances, which Total Adjusted Capital needs |
| IMR excess-withdrawal test [REG-R89] | withdrawable reserves at BOY **net of policy loans**, and effective withdrawals **including the net increase in policy loans** — ordinary life is expressly in that base |
| C-2 mortality [REG-R142][REG-R128] | NAR = face in force − life reserves (GA + SA), net of reinsurance — the reference model reports gross flows plus a separate loan account and **no NAR** **[std]**, so add it — plus a **dividend-scale repricing scenario** on a present value basis over five policy years |
| C-3a bucketing [REG-R128] | reserves split by risk category: base life reserve Low, dividend accumulations Medium |
| Tax and reinsurance [REG-R16][REG-R97][REG-R92][REG-R154 ¶25.f] | §807 reserve seriatim and the statutory-versus-tax difference with its reversal pattern; gross and ceded reserves **separately, never netted**, a YRT credit being the one-year term mean reserve on the ceded amount on the **original policy's** basis [¶¶36–38] — plus, where the *assuming* company elects A-830's optional YRT-reinsurance exemption, an **independent ceiling**: the ceding company's reserve credit "shall be limited to the amount of reserve held by the assuming company" [REG-R154 ¶25.f]. That is a second constraint alongside the SSAP No. 61 rule, not a restatement of it, and it needs the assuming company's held reserve as an input the ceding model does not otherwise have |
| Asset adequacy analysis [REG-R100][REG-R29] | the **AVR consumed**, reported as an output — it is subtracted from the capital numerator |

### Risk-based capital

C-2, C-3a and C-4a bite this product; C-0, C-1cs, C-3b, C-3c and the AG 48 add-on do not arise for
it on the sources read (no separate account, no subsidiary, no XXX/AXXX cession recorded for whole
life), and C-1o bites through the assets backing the block, not the liability [REG-R128].

**C-2 mortality is the charge that splits the two reference designs.** The exposure base
is **net amount at risk, net of reinsurance** — face amount in force less life reserves, general
plus separate account, now taken from the annual statement [REG-R142]. Bucketing is by **pricing
flexibility, not product code**: the instructions' own examples place **participating whole life** in
*With Pricing Flexibility* and **non-participating whole life** in *Permanent without Pricing
Flexibility*, the highest-factor bucket and the default where no assessment is performed
[REG-R128][REG-R133]. RefWL-Par and RefWL-FE therefore take different factors on the same chassis,
and the difference is the dividend. The "with" categorisation must be *earned*: minimum dollar
margin needed = flexibility factor (the gap between the without and with factors) × NAR, and the
margin available from repricing over the next five policy years must reach it on a present value
basis [REG-R128] — for par WL that lever is the dividend scale (`i_d`, `q^{sc}`, `e^m`), so the model
must run a scale-reduction scenario, not merely a base scenario. Other defaults: direct individual
permanent → *Permanent without*; non-affiliated **ceded** individual → *With Pricing Flexibility*
[REG-R133]. Size bands apply to the **company total** individual and industrial NAR, then allocate
proportionately [REG-R128][REG-R133], so the block's marginal charge is a function of company mix.
Two product mechanics move the exposure: **each PUA purchase raises face in force and therefore
NAR** by roughly (PUA face − PUA reserve), converting current earnings into future C-2 exposure; and
because `CV_t → F` and `PUACV → PUAF` at age 100 [S1][S3], NAR runs off to zero at the endowment
point **by construction, not by lapse**. For the RefWL-FE graded plan the years 1–2 benefit is 110%
of premiums paid [S6][S7]; whether the Exhibit of Life Insurance reports `F` or the graded amount
there is not addressed by the sources read — **[unverified]**.

**C-3a is factor-based, bucketed by withdrawal provision.** Life insurance reserves sit in **Low** at
**0.0095** pre-tax, **0.0063** where an unqualified actuarial opinion based on asset adequacy testing
is filed; **dividend accumulations sit in Medium**, **0.0190 → 0.0127** [REG-R128] — the ACCUM option
is about twice as capital-expensive per dollar as the base reserve, and whether that balance is an
Exhibit 7 item is the open classification question above. **C-3 Phase I does not reach this product
as specified:** its life scope is *single premium life*, and RefWL-Par is level-pay or 10-pay
[REG-R128][REG-R135] — a single-premium design would pull the block into Phase I on the year-end
asset adequacy model. LR049's significance test measures C-3a against total RBC, so the whole formula
must be computable before you know whether cash flow testing is compelled [REG-R128].

**C-4a is 2.53% of Schedule T life premiums**, outside the covariance radical, dollar for dollar
[REG-R128]: a level-premium whole life pays it for the entire premium period, while a paid-up, RPU
or premium-completed 10-pay block stops generating it. **Total Adjusted Capital carries the
participating-specific item** — the AVR counts as capital, limited to the amount not consumed in
asset adequacy testing [REG-R128][REG-R29], **and 50% of dividends apportioned for payment plus 50%
of dividends not yet apportioned** [REG-R128, LR033 lines (3)–(4)]; a model producing only dividend
*payments* cannot supply that. The Model #312 RBC Plan requires projected statutory operating income,
net income, capital and surplus for the current year and **at least four succeeding years**
[REG-R125] — which is why this product needs a projection run, not only a valuation.

### Product-specific interactions and traps

1. **Dividends carry three statutory meanings at once.** Their own deduction line in the Summary of
   Operations, neither benefit nor expense [REG-R90]; a **benefit** in the VM-20 SERT's
   PV-of-benefits denominator, where premium, expense and reinsurance flows are not [REG-R3 §6.A];
   and the pricing-flexibility lever for C-2 [REG-R128]. Because `D_t` is floored at zero **[std]**,
   adverse experience does not claw back, so projected statutory *earnings* are asymmetric in the
   scale even where the reserve is not.
2. **Guaranteed cash values are a reserve floor.** §3.D floors the NPR at CSV [REG-R3], SVL §6.A —
   printed in the manual as **A-820 ¶16** — floors the aggregate reserve on the nonforfeiture basis
   [REG-R1][REG-R153 ¶16], and any residue is a Miscellaneous Reserves line [REG-R89]. A model
   treating the CV table only as a benefit schedule understates the reserve in exactly the durations
   where that schedule is richest. Two properties of ¶16 the model has to respect and a seriatim
   engine will get wrong: the test is on **aggregate reserves for all life insurance policies**, not
   policy by policy, and it **excludes disability and accidental death benefits** — so the waiver and
   accidental-death rider reserves come out of the comparison, while the base and PUA reserves stay
   in. ¶16 also re-runs **the same methods** (¶¶11–15, ¶¶19–21) on the *nonforfeiture* mortality and
   interest basis, which for this product is the same 2017 CSO / 4.00% basis the CV table is built
   on, so the floor and the schedule are computed from one source [REG-R153 ¶16].
3. **Policy loans.** No admissibility rule for policy loans is asserted here — SSAP No. 49 was not
   read, and the only general principle in the retrieved sources is that assets not usable to meet
   policyholder obligations are non-admitted and charged against surplus [REG-R74 ¶36]. What *is*
   recorded: loans are **excluded from the AVR asset base** [REG-R85 ¶2]; they enter the VM-20 §4.A
   deterministic reserve as both a balance and a net flow [REG-R3]; the IMR excess-withdrawal test
   counts the **net increase in policy loans** as an effective withdrawal and measures withdrawable
   reserves **net of policy loans** [REG-R89]; and line 17 of the Analysis of Increase in Reserves
   reports the loan value available on the ending CSV [REG-R90]. Whether RBC charges policy loans on
   a line of its own **was not established by the instructions read** [REG-R128] — do not code a zero
   charge on the strength of the AVR exclusion.
4. **First-year strain is a modelled output.** The 90%-of-first-year-premium plus $250 acquisition
   assumption **[std]** is expensed as incurred with **no DAC asset**, against a single year's
   premium and the initial reserve; levelized-commission funding is looked through [REG-R75 ¶¶2, 4–5].
5. **Tax.** The §807 reserve is `max(net surrender value, 92.81% × NAIC-method reserve)` capped at
   statutory [REG-R16]; for whole life the NSV leg is a real competitor because the CV schedule is
   substantial, so which leg binds must be tested **by duration**, not assumed. The difference feeds
   DTA/DTL scheduling and admittance, which runs on the ExDTA ACL RBC ratio [REG-R97].
6. **Company- and treaty-level items still land on this statement:** AG 53 by a company-level size
   test [REG-R105], AG 55 by treaty [REG-R103], negative-IMR admittance as a company balance that
   must still be captured in the PBR calculation or asset adequacy testing [REG-R87][REG-R100]; and
   AVR and IMR need **asset-side disposal detail** this liability model does not produce, with AVR
   movements going direct to surplus [REG-R89][REG-R86].
7. **Four open items this library will not guess**, all **[unverified]** — record the convention
   chosen rather than inferring one. (a) Whether a premium paid by the REDUCE_PREM/premium-offset
   option, or a dividend applied to buy PUAs, is reported **gross** (premium income plus an
   offsetting policyholder dividend) or netted: premium is recognised gross when due [REG-R79 ¶¶2–5]
   but the application case is not addressed, and C-4a is 2.53% of premium [REG-R128]. (b) Whether a
   PUA layer bought in a later calendar year takes the base policy's year-of-issue valuation basis or
   the purchase year's — SVL §4b keys to calendar year of issue [REG-R1], and the answer moves both
   `i_v` and the mortality table for the PUA block. **A-820 ¶¶7–10 have now been read in full and do
   not settle it**: the paragraphs are keyed to the calendar year of issue for all business and say
   **nothing about paid-up additions purchased after issue**, so this stays open on primary
   authority rather than for want of a document [REG-R153 ¶¶7–10]. (c) How an ETI or RPU block
   affects the VM-20 reserving category, the C-2 pricing-flexibility bucket or the C-4a premium base.
   (d) **New, and specific to RefWL-FE:** A-820 ¶¶5.a and 5.b carve **preneed policies** out of the
   ordinary-life mortality rules and send them to **Appendix A-817**, which **was not retrieved**
   [REG-R153 ¶5][REG-R110]. Nothing in the sources read says whether a simplified-issue final-expense
   policy of the Living Promise type is a "preneed policy" for that carve-out; RefWL-FE is modelled
   on the ordinary-life basis and the classification is not asserted.

## Valuation and reserve pointers (brief)

This library projects **gross liability cash flows**; statutory, tax, and GAAP measurement are
separate layers, cited not reproduced. Statutory measurement is developed at length in the preceding
section, "Statutory accounting and capital"; the entries below are the entry points it builds on and
do not restate it:

- **Statutory:** Standard Valuation Law root [REG-R1], codified in the AP&P Manual as **Appendix
  A-820** and now read in full — ¶11 CRVM, ¶¶7–10 the valuation interest rate, ¶16 the aggregate
  nonforfeiture floor, ¶¶19–20 deficiency reserves, ¶¶24 and 27 the formulaic/PBR boundary
  [REG-R153]; **A-830** likewise [REG-R154], though ¶3.b routes no calculation paragraph to a
  level-premium level-benefit whole life. Both were "not retrieved" behind the VM-A index entry
  [REG-R110] and no longer are. For issues on/after 2020-01-01 — a date that is the PBR
  *accreditation* year, the statutory-law trigger A-820 ¶¶3–4 prints being **1 January 2017**; see
  "Reserve basis" above — VM-20 minimum reserve = f(net premium reserve, deterministic reserve,
  stochastic reserve) with exclusion tests; seriatim NPR on 2017 CSO; traditional par WL typically
  passes the deterministic exclusion test (valuation net premiums ≤ guaranteed gross premiums) and
  many WL blocks hold NPR only [R3]. Small companies under the Life PBR Exemption (< $300M) value
  under VM-A/VM-C (pre-PBR CRVM) [R3]. ASOP 52 governs the actuary's PBR work [REG-R31].
- **Tax:** IRC §807 — greater of net surrender value and 92.81% of the CRVM/VM reserve,
  capped at statutory [REG-R16]; the statutory engine plus a haircut/cap wrapper.
- **GAAP:** LDTI (ASU 2018-12) rewrites long-duration GAAP (annually updated cash flow
  assumptions, single-A discounting through OCI) [REG-R34 — not fetched; characterization
  corroborated only by secondary summaries]. Same projected cash flows, different measurement
  overlay — the reason projection and measurement are separated in this library.
- **Model governance:** ASOP 56 (modeling) [REG-R32] and, for cash-flow analysis engagements,
  ASOP 7 [REG-R27 — listed in the regulatory bibliography] frame validation/documentation
  expectations for the implementation itself.

## Key sensitivities and model risks

Dominant assumptions (in typical order of impact on par WL liability value):

1. **Dividend scale vs. guarantee spread** (`i_d − i_g`, mortality margin, expense margin):
   drives dividends, hence PUA growth, hence death benefit and surrender value trajectories —
   compounding because PUAs themselves earn dividends [S14]. The DIR snapshot is a declared,
   changeable rate (observed 5.75%–6.60% for 2026 alone [S4][S14]); scale-change dynamics are
   a scenario input, not a model constant.
2. **Best-estimate mortality** (level and improvement vs. 2015 VBT [REG-R18], A/E per ILEC
   [R9]): sets both claim outgo and the mortality margin of the dividend; note the same table
   family feeds two places with opposite signs — a consistency trap.
3. **Lapse:** low and level for par WL, but long-duration liabilities are convex in lapse;
   illustration regulation exists precisely because lapse-supported scales misstate value
   [R2]. Verify the model is not inadvertently lapse-supported when testing dividend scales.
4. **Expense inflation** on per-policy maintenance for a product with 55+-year horizons.
5. **Loan utilization** under direct recognition [S1][S3]: shifts dividend composition and
   net cash flow timing; the fixed-6%/DIR-6% snapshot coincidence (zero adjustment) will not
   survive a scale change.

Known modeling pitfalls:

- **CV-table vs. first-principles mismatch:** if the CV table input and the `NSP`/annuity
  functions come from different bases, `PUACV ≠ PUAF` at age 100 and the dividend recursion
  leaks. Regenerate all guarantee-basis quantities from one 2017 CSO / 4% source [S1][R1][R8].
- **Dividend floor and negative margins:** with `D_t` floored at 0 **[std]**, adverse
  experience does not claw back — asymmetry matters in stochastic runs.
- **First-dividend timing** (year 1 vs 2) shifts early-duration PUA compounding; it is a real
  cross-carrier difference [S1][S3], keep it a parameter.
- **MEC administration on limited-pay variants:** 10-pay premiums approach 7-pay limits; face
  decreases can retroactively create MECs and PUA-rider payments consume 7-pay room
  [R5][S3][S1]. The reference model does not police §7702/§7702A limits [R4][R5] — flag
  model points that would fail rather than silently projecting them **[std]**.
- **Truncation at age 100** **[std]** is exact for surrender/maturity amounts but reallocates
  age-100–121 payments from death to maturity; do not use the truncated model for
  mortality-timing-sensitive measures beyond age 100 [S1].
- **State variations** (FL maturity 120, WA face minimums, ND suicide, MT unisex)
  [S6][S7][S8][S1] are not modeled; the reference is a generic-state contract **[std]**.
