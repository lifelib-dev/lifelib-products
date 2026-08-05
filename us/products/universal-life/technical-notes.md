# Universal Life Insurance (current assumption) — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`us/_research/universal-life.md`; [REG-R#] tags refer to the cross-product reference
library `us/references/regulatory-and-actuarial-references.md` (its own R-numbering;
research provenance in `us/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation. Parameter values are
identical to those in `product-spec.md`; the implementation anchor for mechanics is
the Pacific Life Versa-Flex PRO specimen policy [S3].

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows (premiums, death claims, surrender
  and withdrawal payments, expenses, loan flows optional) for a single-policy model
  point of current-assumption fixed UL, on a monthly grid. Reserves are not computed
  (see Valuation and reserve pointers).
- **Projection frequency.** Monthly. The contract credits interest daily on a 365-day
  year [S3]; the model discretizes to monthly compounding **[std]**: one month of
  interest is applied at the end of each policy month to the post-deduction balance.
- **Timing / monthiversary processing.** All policy transactions are processed on the
  monthiversary (the monthly payment date — the same day each month as the policy
  date [S3]), at the beginning of the policy month (BOM); interest accrues over the
  month and is credited at end of month (EOM) **[std]**. The monthly deduction taken
  at BOM pays for that policy month's coverage (the specimen states the deduction
  provides coverage for the following policy month [S3]; with BOM indexing the
  deduction at the start of month t covers month t).
- **Age basis.** Age nearest birthday (ANB) **[std]**. Rationale: the specimen's
  nonforfeiture basis is 2001 CSO ANB [S3], the SOA/LIMRA UL study methodology is ANB
  [R7], and the 2017 CSO/2015 VBT families provide ANB variants [R4][REG-R18].
- **Model points.** Single-policy model points, projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  No aggregation logic is specified here.
- **Decrement order within a month.** Contractual transactions first (BOM), then
  decrements (death, lapse) treated as EOM events **[std]** (see processing order).
- **Rounding.** Intermediate values carried at full precision; cash flows reported to
  cents **[std]**. (Production admin systems round per-transaction; the specimen is
  silent on model rounding.)

---

## Model point attributes

| Attribute | Type | Example (anchor cell [S3]) |
|---|---|---|
| `issue_age` | int (ANB) | 35 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum (6 classes, spec table) | Standard NT |
| `face_amount` | currency | 100,000 |
| `db_option` | enum {A, B} | A |
| `qual_test` | enum {GPT} (CVAT out of scope) | GPT |
| `issue_date` / `policy_month_offset` | date / int | month 1 |
| `planned_premium_annual` | currency | 1,800 **[std]** |
| `premium_pattern` | enum {level, single, target} | level **[std]** |
| `premium_mode` | enum {monthly, annual} | monthly **[std]** |
| `av_initial` | currency (0 at issue; >0 for in-force cells) | 0 |
| `loan_balance_initial` | currency | 0 |
| `sc_layer_table` | schedule per $1,000 | $9.00 initial, 9-yr **[std]** |
| `guideline_single_premium` | currency (compliance input) | 34,138.15 [S3, incl. riders] |
| `guideline_level_premium` | currency (compliance input) | 2,825.52 [S3, incl. riders] |
| `seven_pay_premium` | currency (compliance input) | 6,702.10 [S3, incl. riders] |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AV(t)` | Account value (the specimen's "accumulated value") at end of policy month t | monthly recursion |
| `F(t)` | Total face amount (after any option changes/withdrawal-driven reductions) | on events |
| `DB(t)` | Death benefit in month t after corridor test | monthly |
| `NAAR(t)` | Net amount at risk for COI in month t | monthly |
| `SC(t)` | Surrender charge in month t | monthly amortization |
| `L(t)` | Policy loan balance (with capitalized interest) | monthly |
| `CumPrem(t)` | Cumulative premiums less withdrawal offsets (GPT/7-pay tracking) | monthly |
| `l(t)` | In-force probability at end of month t (survivorship) | monthly decrements |
| `grace_flag(t)` | In-grace indicator and months-in-grace counter | monthly |
| `wd_used_year` | Free-withdrawal usage in current policy year | on withdrawal |

---

## Assumption inputs

Three classes are distinguished explicitly. Class (a) is contractual and cannot be
changed by the insurer; class (b) is the insurer-declared current scale (an NGE under
ASOP 2 [R8]); class (c) is the modeler's view of policyholder/insurer experience.

### (a) Contractual / guaranteed elements (from the spec)

| Input | Value | Basis |
|---|---|---|
| Guaranteed minimum annual interest `i_guar` | 2.00% | pick from 2%–3% range [S1][S2][S3]; **[std]** |
| Guaranteed max COI rates `q_coi_guar(s)` per $1,000/month | specimen table by policy year s (spec, charges table) | [S3]; interpolation **[std]** |
| Guaranteed max premium load | 9% | [S1]; composite **[std]** |
| Per-policy charge (guaranteed = current) | $7.50/month to age 121 | [S3]; composite **[std]** |
| Per-unit charge | $0.26/$1,000/mo yrs 1–10; $0.156 to age 121 | [S3]; composite **[std]** |
| Surrender charge schedule | $9.00/$1,000 initial, linear monthly runoff, 0 from year 10 | pattern [S1][S2], mechanics [S3], amount **[std]** |
| Corridor factors (GPT) | specimen table 250% (ages 0–40) → 101% (94+) | [S3][R2] |
| Loan spread (charged − credited on loaned AV) | 0.75% | [S3]; level **[std]** |
| Grace | 61 days; required payment 3xMD + load | [S2][S3] |
| Charges cease / premiums stop | attained age 121 | [S2][S3] |

### (b) Current non-guaranteed scales (snapshot; revisable NGEs [R8])

| Input | Value | Basis |
|---|---|---|
| Current credited annual rate `i_cr` | 4.00% | **[std]** — current declared rates are not public; the one rates page attempted returned HTTP 403 [S5] |
| Current COI scale | 60% x guaranteed max, all durations | **[std]** — current COI scales are not public; only guaranteed maxima appear in the specimen [S3] |
| Current premium load | 6% | [S1]; composite **[std]** |
| Current per-policy charge | $7.50/month | [S3]; composite **[std]** |

NGE revision logic (optional module): under ASOP 2, scales are revised only on changes
in anticipated experience factors, with no recouping of past losses and prospective
profitability not materially greater than original [R8]. A simple reference rule:
`i_cr(t) = max(i_guar, earned_rate(t) − spread)` with a constant spread **[std]**;
the base projection holds the snapshot scales level.

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality | 2015 VBT (sex/smoker-distinct, ANB) x 100% A/E **[std]** factor; monitor against ILEC 2012–2019 A/E experience | [REG-R18][REG-R19]; factor **[std]** |
| Mortality improvement | None in base **[std]** | — |
| Guaranteed-element mortality reference | 2017 CSO (cap for guaranteed COI; valuation/nonforfeiture basis for new issues) | [R4][REG-R17]; COI-cap role [unverified — search-result context] |
| Base lapse/surrender | SOA/LIMRA UL studies (2015–2021 UL persistency & lapse; 2009–2013 all-product persistency); detailed tables are behind the paid package, so the reference table below is **[std]** | [R7][REG-R21][REG-R20] |
| Premium persistency | SOA/LIMRA 2015–2021 UL study: premium persistency (paid/planned) highest in year 1 (dump-ins); current-assumption products highest ongoing persistency | [R7]; reference factors **[std]** |
| Maintenance expense | $75/policy/year, inflating 2.5%/year | **[std]** |
| Premium tax / percent-of-premium expense | 2.5% of premium | **[std]** |

Reference base lapse table **[std]** (annual rates, all calibration to be replaced by
the user's experience; shape informed qualitatively by [R7][REG-R20]):

| Policy year | 1 | 2 | 3–9 | 10 | 11+ |
|---|---|---|---|---|---|
| Annual lapse `w_base` | 6% | 5% | 4% | 4% x shock (below) | 3% |

Reference premium persistency factors `pp(y)` **[std]** (fraction of planned premium
actually paid, level-pay pattern): 100% in year 1, declining 2 percentage points per
year to a 70% floor (year 2: 98%, year 3: 96%, ..., floor from year 16).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month index, t = 1, 2, ... (t=1 is the issue month); y = policy year = ceil(t/12); x = issue age; attained age = x + y − 1 (ANB) |
| `F` | total face amount (per policy) |
| `U` | units of face = F / 1000 |
| `GP(t)` | gross premium received at BOM of month t |
| `pl` | current premium load rate (0.06) |
| `NP(t)` | net premium = GP(t) x (1 − pl) |
| `W(t)` | partial withdrawal amount at BOM of month t (plus fee `wf` = $25 when W>0) |
| `e_pol` | per-policy charge ($7.50/month) |
| `e_unit(y)` | per-unit charge per $1,000/month (0.26 yrs 1–10; 0.156 yrs 11 to age 121; 0 after) |
| `rc(t)` | rider charges (0 in base model) |
| `q_coi(s)` | current monthly COI rate per $1,000 NAAR at policy year s = 0.60 x q_coi_guar(s) |
| `i_guar` | guaranteed annual effective rate (0.02) |
| `i_cr` | current credited annual effective rate (0.04) |
| `i_m` | monthly credited rate = (1 + i_cr)^(1/12) − 1 = 0.0032737 (derived) |
| `i_gm` | monthly guaranteed rate = (1 + i_guar)^(1/12) − 1 = 0.0016516 (derived) |
| `cf(a)` | GPT corridor factor at attained age a (spec table) [S3][R2] |
| `AV'(t)` | AV after premium and withdrawal, before monthly deduction |
| `MD(t)` | monthly deduction |
| `NAAR(t)` | net amount at risk |
| `DB(t)` | death benefit after corridor test |
| `SC(t)` | surrender charge; `CSV(t) = AV(t) − SC(t)`; `NCSV(t) = CSV(t) − L(t)` |
| `L(t)` | loan balance; `r_L` charged loan rate (0.0275); loaned AV credited at i_guar |
| `q_m(t)` | best-estimate monthly mortality rate; `w_m(t)` monthly lapse rate |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |

Dimensional check: `q_coi` is per $1,000 per month, so COI charge = q_coi/1000 x NAAR
is in currency; `e_unit x U` is currency; all MD components are currency/month.

### Monthly processing order (monthiversary, per the specimen [S3]; discretization [std])

At BOM of month t (skip steps 2–7 from attained age 121: charges cease, premiums not
accepted [S2][S3]):

1. Set policy year y, attained age a. Amortize surrender charge:
   `SC(t) = max(0, (9.00 − t/12) x U)` (per-layer if face increases are modeled)
   **[std amount; mechanics [S3]]**.
2. Premium: `GP(t)` per the premium pattern and persistency assumption; check GPT
   guideline limit and 7-pay limit (compliance side-calculation — see below); deduct
   load; credit `NP(t)` to AV. (If L(t−1) > 0, unallocated payments repay the loan
   first unless designated premium [S3] — base model designates all as premium.)
3. Withdrawal: deduct `W(t) + wf`; apply free-amount rule (10% of AV per policy year
   **[std]**); under Option A reduce F if the withdrawal would otherwise increase
   NAAR beyond the free amount [S3].
   After steps 2–3: `AV'(t) = AV(t−1) + NP(t) − W(t) − wf x 1{W>0}`.
4. Death benefit and corridor:
   `DB(t) = max(optionDB(t), cf(a) x AV'(t))` where `optionDB = F` (Option A) or
   `F + AV'(t)` (Option B) [S1][S3]; corridor per GPT [S3][R2].
5. NAAR (specimen discounting convention — DB discounted one month at the guaranteed
   rate; AV measured before the deduction [S3]):
   `NAAR(t) = DB(t) / (1 + i_gm) − AV'(t)`, floored at 0.
   (The specimen states this as DB / NAAR-factor with factor 1.03^(1/12) = 1.0024663
   at its 3% guarantee [S3]; at the composite 2% guarantee the factor is
   1.02^(1/12) = 1.0016516, derived.)
6. Monthly deduction:
   `MD(t) = e_pol + e_unit(y) x U + rc(t) + q_coi(y)/1000 x NAAR(t)` [S3].
7. Shortfall test: if `AV'(t) − L(t−1) < MD(t)`, enter grace [S2][S3] (see grace
   logic); otherwise deduct: AV after deduction = `AV'(t) − MD(t)`.
8. Interest (EOM): credit one month at the current rate on unloaned AV and at the
   guaranteed rate on the loaned portion; accrue loan interest at r_L **[std
   discretization of daily crediting [S3]]**:
   `AV(t) = (AV'(t) − MD(t) − L(t−1)) x (1 + i_m) + L(t−1) x (1 + i_gm)`
   `L(t) = L(t−1) x (1 + r_L)^(1/12)` (capitalized annually per contract [S3];
   monthly compounding **[std]**).
9. Decrements (EOM): deaths at `q_m(t)`, lapses/surrenders at `w_m(t)` applied to
   survivors; update `l(t) = l(t−1) x (1 − q_m(t)) x (1 − w_m(t))` **[std order:
   death before lapse]**.

With no loans and no withdrawals, steps 2–8 collapse to the core recursion:

    AV(t) = [ AV(t−1) + NP(t) − MD(t) ] x (1 + i_m)

with `NP(t) = GP(t) x (1 − pl)`, matching the contractual roll-forward in which the
policy-date AV equals net premium minus the first monthly deduction [S3].

### Grace and lapse-for-insufficiency logic

- Trigger (month t): `AV'(t) − L(t−1) < MD(t)` on a monthiversary [S2][S3]. (Model 585
  default defines lapse at NCSV = 0 with >= 30-day grace [R1]; the composite follows
  the specimen trigger.)
- During grace (61 days ≈ 2 policy months **[std]**): coverage continues; deductions
  accrue as due-and-unpaid; if death occurs, claim = DB − L − overdue deductions [S3].
- Required cure payment: >= 3 x MD due plus premium load [S3]. In the deterministic
  base model, planned-premium payers are assumed to cure if `pp(y) x planned >= cure`
  **[std]**; otherwise the policy lapses at the end of the second month in grace with
  zero payment (terminates without value [S3]).
- Reinstatement is not modeled (contractual provision only [S3]) **[std scope]**.

### Cash flow outputs (per policy, month t, before survivorship weighting)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | GP(t) | + |
| Death claims | DB(t) − L(t−1) − overdue deductions (in grace) [S3] | − |
| Surrender outgo | NCSV(t) = AV(t) − SC(t) − L(t) | − |
| Withdrawal outgo | W(t) (fee wf retained by insurer) | − |
| Maintenance expense | 75/12 x (1.025)^(y−1) **[std]** | − |
| Percent-of-premium expense | 0.025 x GP(t) **[std]** | − |
| Loan flows (optional) | new loans −, repayments + | +/− |

Aggregate expected cash flows multiply each row by the appropriate in-force factor:
premiums/expenses by l(t−1); death claims by l(t−1) x q_m(t); surrenders by
l(t−1) x (1 − q_m(t)) x w_m(t) **[std timing]**.

### MEC / 7-pay and guideline premium tests (compliance side-calculations)

The GPT limit (cumulative premiums less a portion of withdrawals may not exceed
max(GSP, cumulative GLP)) and the 7-pay MEC test are tracked as compliance
side-calculations that cap or refuse premiums [S3][R2][R3][REG-R13][REG-R14]; they
generate no cash flow of their own — a refused premium simply never enters the model,
and MEC status changes policyholder taxation, not insurer liability cash flows [R3
consequence detail [unverified] beyond the statutory cross-reference]. The base model
verifies `CumPrem(t) <= max(GSP, GLP x years elapsed)` and flags (does not project)
7-pay failures.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; calibration sources are
cited where they exist.

- **Premium patterns [std].** `level`: GP(t) = planned/12 x pp(y) each month (pp per
  the persistency table); `single`: one premium at issue capped at GSP, no further
  premiums; `target`: GP as level but capped so CumPrem stays within the GPT limit.
  Qualitative anchors: year-1 premium persistency is highest (dump-ins), and
  current-assumption products show the highest ongoing paid-to-planned ratios after
  early years [R7].
- **Base lapse [std].** Annual `w_base(y)` per the table above, converted monthly:
  `w_m = 1 − (1 − w_annual)^(1/12)`.
- **Surrender-charge-expiry shock [std].** During policy year 10 (the first year with
  SC = 0): `M_sc = 2.0`; else 1.0. Rationale: the surrender charge suppresses
  surrender while it is positive; its expiry is a known industry lapse-shock point
  (product-specific studies are proprietary; shape assumption).
- **Interest-sensitive (dynamic) lapse [std].**
  `M_rate(t) = min(3.0, 1 + 5 x max(0, r_comp(t) − i_cr(t) − 0.01))`
  where `r_comp` is a competitor/market new-money rate input. Base deterministic run:
  `r_comp = i_cr`, so M_rate = 1.
- **Total lapse.** `w_annual(y,t) = min(0.35, w_base(y) x M_sc(y) x M_rate(t))`
  **[std cap]**.
- **Premium suspension [std].** Implicit in pp(y) < 1; no separate paid-up state is
  modeled.

---

## Worked example

Anchor cell: Male 35 Standard NT, F = $100,000 (U = 100), Option A, GPT; GP = $150/mo;
pl = 6% → NP = $141.00; e_pol = $7.50; e_unit = 0.26 → $26.00/mo; guaranteed COI year
1 = 0.10090 [S3], current = 60% → q_coi = 0.060540 per $1,000/mo **[std]**;
i_m = 0.0032737 (from i_cr = 4.00% **[std]**); 1 + i_gm = 1.0016516 (from i_guar =
2.00% **[std]**); DB/(1+i_gm) = 100,000 x 0.9983511 = 99,835.11; corridor 250% x AV'
never binds at these AV levels [S3]. No withdrawals or loans. All figures in dollars,
rounded to cents for display (full precision carried).

| Month t | AV(t−1) | NP | AV' | DB | NAAR = 99,835.11 − AV' | COI = 0.06054xNAAR/1000 | MD = 7.50+26.00+COI | AV'−MD | Interest (x i_m) | AV(t) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 141.00 | 141.00 | 100,000 | 99,694.11 | 6.04 | 39.54 | 101.46 | 0.33 | 101.80 |
| 2 | 101.80 | 141.00 | 242.80 | 100,000 | 99,592.32 | 6.03 | 39.53 | 203.27 | 0.67 | 203.93 |
| 3 | 203.93 | 141.00 | 344.93 | 100,000 | 99,490.18 | 6.02 | 39.52 | 305.41 | 1.00 | 306.41 |

Trace, month 1: AV' = 0 + 141.00; corridor min = 2.50 x 141.00 = 352.50 < 100,000 so
DB = 100,000; NAAR = 99,835.11 − 141.00 = 99,694.11; COI = 0.060540/1000 x 99,694.11
= 6.0355 (displayed 6.04); MD = 7.50 + 26.00 + 6.0355 = 39.5355 (displayed 39.54);
AV(1) = (141.00 − 39.5355) x 1.0032737 = 101.80. Month-1 shortfall test: AV' (141.00)
>= MD (39.54), no grace. This reproduces
the contractual policy-date rule AV = net premium − first monthly deduction [S3],
followed by one month's interest.

---

## Statutory accounting and capital

Framework and the twelve-product applicability matrix are in
`us/regulatory/statutory-accounting-and-capital.md`; formulas, factor tables and
algorithms are in `us/regulatory/technical-notes.md`. This section states only what is
specific to current-assumption fixed UL. Two source limits from those files bite here:
the **AVR and IMR factor tables were deliberately not transcribed**, and no value for
either is stated anywhere in this library [REG-R89]; and every RBC figure below comes
from the **2024** *Life and Fraternal Risk-Based Capital Forecasting and Instructions*,
a sold NAIC publication read from a state posting, the **2025 edition having failed to
parse** [REG-R128][REG-R129].

### Contract classification and reporting

- **Life contract, always and immutably.** SSAP No. 50 ¶9 names **universal life type**
  expressly, and classification "shall be made at the inception of the contract and
  shall not change" [REG-R78 ¶¶5, 9]. No configuration of this product is deposit-type:
  the mortality-risk test is met at every duration, including the post-age-121
  charge-free period in which coverage continues [REG-R80 ¶2][S3]. In the model this is
  a flag set at issue, never derived from `NAAR(t)`.
- **Exhibit 5, never Exhibit 7.** Reserves report **gross** with a separately computed
  ceded deduction, Column 1 stating the valuation standard **by years of issue**; VM-20
  business occupies **two lines**, the net premium reserve and the excess over it
  [REG-R89][REG-R90]. Settlement options and dividend accumulations are the only route
  to an Exhibit 7 balance, and the composite puts the installment death-benefit payout
  option out of scope [S2], so the base model produces none [REG-R80][REG-R89].
- **Considerations are premium income, gross when received** [REG-R79 ¶¶2–5]. So
  `NP(t) = GP(t) x (1 − pl)` is a **contract-mechanics quantity, not a statutory revenue
  quantity** — premium income is `GP(t)` and the 6% load is not a reduction of it; a
  premium refused under the GPT or 7-pay limit never becomes revenue, consistent with
  this file's treatment of those tests as caps and flags; and statutory **loading** is a
  third object again — gross less valuation net premium — whose change on deferred and
  uncollected premium is an **expense** line [REG-R79 ¶11][S3][R2][R3].
- **Reporting column, with one inference flagged.** The Analysis of Operations carries
  **Universal Life** and **Universal Life With Secondary Guarantees** as separate
  Individual Life columns [REG-R90]. The base model excludes the 5-year NLG of spec
  footnote 17, so it reports **Universal Life**; the instructions state generally that a
  policy issued with secondary guarantees is reported consistently with how it was issued,
  so **expired guarantees still report as ULSG**, and the only printed include/exclude on
  the ULSG column concerns indexed UL — **whether a 5-year built-in no-lapse guarantee makes
  the policy one "with secondary guarantees" for column purposes is not addressed by the
  retrieved instructions** [REG-R89][unverified]. Incidental riders report on the
  **base contract's** line — where `rc(t)` charges land once a rider module is switched
  on — and a **waiver of monthly deductions** benefit is "not to be considered revenue
  nor a benefit paid", a UL-specific rule that bites the moment the disability rider
  listed out of scope in `product-spec.md` is modeled [REG-R89][REG-R79 ¶14].
- **Acquisition costs are expensed as incurred; there is no DAC asset** [REG-R75
  ¶2][REG-R76]. Specific to this charge structure: commission and issue expense hit
  surplus in the issue year while the design recovers acquisition cost through the
  **$0.26 per $1,000 per month per-unit charge in policy years 1–10** (spec footnote 11)
  [S3] — a ten-year recovery against a one-year charge, nothing deferred to offset it.
  The chronic-illness, LTC and disability riders catalogued in `product-spec.md` are A&H
  contracts under SSAP No. 54, reserved separately but reported on the base contract's
  line; zero in the base model [REG-R82][REG-R89].

### Reserve basis

- **Two engines, and PBR does not retire the formulaic one.** Pre-Valuation-Manual
  issues take the **Model 585 Section 5 CRVM adaptation** — Guaranteed Maturity Premium
  / Guaranteed Maturity Fund with the `r = min(1, policy value / GMF)` ratio and the
  alternative minimum reserve test [R1][REG-R5]. From the operative date (2017-01-01
  [R5]) the Valuation Manual standard is the minimum and **VM-20 constitutes CRVM**
  [REG-R1 §11][REG-R3]. But this product's reserving category is **All Other**, whose
  net premium reserve is determined "pursuant to applicable methods in **VM-A and VM-C**
  for the basic reserve" [REG-R3 §3.B.6][REG-R41], and VM-A indexes the UL requirement
  as **A-585** [REG-R110]. **A UL without secondary guarantees therefore runs the Model
  585 CRVM calculation inside a PBR-era minimum reserve.** VM-A is an index, not a text:
  the AP&P Appendix A print of A-585 was **not retrieved**, so the mechanics here rest
  on the model regulation itself [REG-R110][R1].
- **The reserving category drives the exclusion tests.** All Other — not Term, not
  ULSG — unless a secondary guarantee is modeled. So the **deterministic exclusion test
  is available** (barred outright only for term, deemed failed for a ULSG whose
  secondary guarantee is not non-material); the **stochastic exclusion certification
  method is available** (unavailable only to variable life and ULSG); and with both
  passed, `MinRes = Σ_j NPR_j` with **neither DR nor SR computed**. The base model
  carries **no hedging strategy**, so the §6.A.1.b bar on excluding a group with future
  hedging strategies from the SR does not bite — unlike the indexed sibling. All
  [REG-R3].
- **The DET needs a gross premium this contract does not have.** The Deterministic Net
  Premium Test compares future valuation net premiums against **guaranteed gross
  premiums**; for a UL with none specified, §6.B.6 constructs one — the **level annual
  gross premium at issue that would keep the policy in force for the whole coverage
  period on the guarantees** [REG-R3]. Here that solve runs on `i_guar` = 2.00%, the
  guaranteed maximum COI table, the **9%** guaranteed maximum load and the guaranteed
  per-policy and per-unit charges [S1][S3], over a coverage period with **no maturity
  date** and deductions ceasing at attained age 121 [S2][S3]; `planned_premium_annual`
  is a billing target and is **not** this quantity. Note which §6.B.5 convention does
  *not* reach the product: 0% lapse at all durations applies where the NPR comes from
  §3.B.4 or §3.B.5 — term and ULSG — not the §3.B.6 basis used here; what does reach it
  is the switch to anticipated experience mortality plus §9.C.6 margins where that
  exceeds prescribed CSO [REG-R3].
- **The NPR floor is a valuation quantity, not a contract quantity.** For UL the §3.D
  floor is the cost of insurance to the next processing date on which COI charges are
  deducted, **based on the net amount at risk and on the valuation mortality rate, not
  the contractual COI or expense charges** [REG-R3 §3.D]: one monthiversary of COI on
  `NAAR(t)` at valuation mortality — **not** `q_coi(y) = 0.60 x q_coi_guar(y)`, and
  **not** including `e_pol` or `e_unit(y)`. Policy minimum NPR is the NPR less the §8
  ceded credit [REG-R3 §3.E].
- **Opinion and governance apply whatever the tests say.** VM-30 covers all in-force at
  the statement date and makes any shortfall an **additional reserve**, which Standard
  Valuation Law §6.B makes part of *minimum* reserves; ASOP 22's threshold is
  **moderately adverse conditions** and its starting assets must have a statement value
  **no greater than** that of the reserves tested [REG-R100][REG-R1][REG-R29]. A company
  computing no DR or SR still files a **VM-31 sub-report** and must report **readiness
  to compute** them, and passing by the DR-based SERT route or the demonstration test
  **re-imposes VM-G Sections 2 and 3** [REG-R108][REG-R109]. AG 53 and AG 55 reach this
  product through **company-level and treaty-level** triggers, not through anything in
  the product design [REG-R105][REG-R103].

### What this product's model must additionally produce

The shared output contract is `us/regulatory/technical-notes.md`, "Required model
outputs", and is not repeated. Specific to this chassis:

| Statutory item | This model's output | Cite |
|---|---|---|
| Exhibit 5 Column 1, valuation standard by year of issue | reserve keyed to Model 585 / A-585 for pre-operative issues and to **VM-20NPR** plus, where computed, **VM-20 DET/STO on a second line**, for post-operative issues | [REG-R89][REG-R3] |
| Exhibit 5 Miscellaneous Reserves — surrender values in excess of reserves otherwise carried | `max(0, CSV(t) − V(t))` per policy; grows once `SC(t)` reaches zero from policy year 10 | [REG-R89] |
| Exhibit of Life Insurance | `F(t)` in thousands on an **incurred** in-force roll-forward; whether Option B's account-value component enters "amount in force" is not addressed by the retrieved instructions [unverified] | [REG-R89] |
| Analysis of Operations column | **Universal Life**; **ULSG** if a secondary guarantee is modeled | [REG-R90][REG-R89] |
| Analysis of Increase in Reserves | tabular net premium, tabular interest, tabular cost on the **valuation** basis — never `GP(t)` and never `MD(t)` | [REG-R90] |
| Premium income and loading | `GP(t)` gross when received; `NP(t)` is not a statutory quantity; change in loading is an **expense** | [REG-R79] |
| C-2 exposure | statement-derived NAR = face in force − life reserves (GA + SA), net of reinsurance — **not** `NAAR(t)` | [REG-R142] |
| C-3a exposure | statutory life reserve `V(t)`, plus the VM-30 opinion category flag, which switches the factor | [REG-R128][REG-R100] |
| C-4a exposure | Schedule T life premium — `GP(t)` actually received, which premium flexibility makes volatile | [REG-R128] |
| IMR excess-withdrawal test | `W(t)`, surrenders computed without market adjustment, and the **net increase in `L(t)`** | [REG-R89] |
| Tax reserve | `max(NSV(t), 0.9281 x NAIC-method reserve)` capped at statutory, with `NSV(t) = CSV(t) − L(t)` | [REG-R16] |
| Reinsurance | gross and ceded produced **separately, never netted**; ceded on the same mortality, interest and method | [REG-R89][REG-R92 ¶37] |

**One open point, not filled by invention.** The VM-20 combination measures the DR/SR
excess net of `B`, the due-and-deferred premium asset held [REG-R3 §2.A]; nothing in
`us/regulatory/` states how `B` behaves for a **flexible-premium** design in which no
premium is ever contractually due. Treat `B` as an input, not a hard-coded zero.

### Risk-based capital

- **C-2 mortality dominates, and it is NAR-based.** Exposure is the **statement-derived**
  NAR — Exhibit of Life Insurance face in force less Exhibit 5 and Separate Accounts
  Exhibit 3 life reserves, with the General Interrogatories reinsurance adjustment, net
  of reinsurance throughout [REG-R142]. The factor turns on a **pricing-flexibility
  categorisation the model must earn**: whether rates on in-force contracts can be
  *materially* adjusted through premiums and/or non-guaranteed elements within the next
  **5 policy years**, on a present value basis, by at least `flexibility factor x NAR`
  [REG-R128]. The instructions' own example of the "with pricing flexibility" bucket is
  **UL without secondary guarantees**, and this product's levers are the three NGEs of
  `product-spec.md` — current COI at **60% of the guaranteed maximum**, credited rate
  **4.00%** against a **2.00%** guarantee, load **6%** against a **9%** maximum [S1][S3]
  — headroom computable from the spec tables, but the repricing scenario must be one
  **ASOP 2** would permit: revision only on changes in anticipated experience, no
  recouping of past losses [R8][REG-R26]. **Where the assessment is not performed,
  direct individual permanent defaults to "Permanent without Pricing Flexibility"**
  [REG-R133] — band-1 factor **0.00400** rather than **0.00220**, the highest-factor
  bucket [REG-R128]; non-affiliated ceded individual business defaults the other way, to
  *with* [REG-R133]. Size bands apply to the **total** individual and industrial NAR
  (first **$500 million**, next **$24,500 million**, over **$25,000 million**) then
  allocate proportionately, so a block below the first threshold sits entirely at the
  highest band factor [REG-R128][REG-R133].
- **C-2 longevity does not apply** — no life-contingent annuity benefit [REG-R128].
- **C-3a applies on the reserve, and the opinion switches the factor.** The published
  categories put **single premium life and life insurance reserves** in **Low**, at
  **0.0095** pre-tax, cut by one third to **0.0063** where the company files an
  unqualified actuarial opinion based on asset adequacy testing [REG-R128]. The
  **withdrawal-provision axis** the categories are built on — fair-value-adjusted or not
  withdrawable (Low), **book value less a surrender charge of 5% or more** (Medium),
  **book value without adjustment** (High) — is stated for **annuity** reserves; the
  retrieved instructions state **no UL-specific bucket keyed to the surrender charge**,
  and this library does not invent one. It matters twice anyway: any Exhibit 7 balance
  the block throws off sits in **Medium**, with supplementary contracts without life
  contingencies and dividend accumulations [REG-R128]; and the driver the axis uses is
  already a state variable here — `SC(t)`, a fixed dollar amount per $1,000 of *initial*
  face, amortised monthly and **zero from the start of policy year 10** [S1][S2][S3] —
  so under any reading that did apply the axis to a cash-value UL liability the block
  migrates toward "book value without adjustment" as the charge runs off, and on a
  level-pay Option A cell some years before year 10, as the declining charge falls below
  5% of a growing account value. Record the reading used.
- **C-3 Phase I reaches this product only through a single-premium cell.** Phase I scope
  is "Certain Annuities" **plus single premium life** [REG-R128][REG-R135], so a
  `premium_pattern = single` model point is in scope and a level-pay one is not; the
  LR049 significance test puts factor-based C-3a on **single premium** and annuity
  reserves in its numerator on the same footing [REG-R128].
- **C-1 is entirely C-1o**; fixed UL has **no separate account**, so nothing here
  generates C-1cs or the separate-account capital interactions the variable sibling
  carries [REG-R83][REG-R128].
- **C-3b and C-3c do not apply; C-4a does**, at **2.53%** of Schedule T life premiums and
  annuity considerations [REG-R128] — and premium flexibility makes it behave unlike a
  fixed-premium chassis: a well-funded block whose owners suspend premium keeps its
  reserve and NAR, hence its C-2 and C-3a, while C-4a falls toward zero, because `pp(y)`
  and the grace cascade determine premium received [R7].
- **No AG 48 add-on** unless a secondary guarantee is modeled: the XXX/AXXX Primary
  Security shortfall, doubled before the halving that produces Authorized Control Level
  so it lands dollar-for-dollar, is a term and ULSG item [REG-R128][REG-R11][REG-R12].
- **Size and mix.** Early durations of an Option A cell are almost all C-2: NAR ≈ face
  while account value and reserve are small; as funding accumulates the reserve rises
  and NAR falls, rotating the mix toward C-3a and C-1o. Under **Option B**
  (`DB = F + AV`) NAR does not decay with funding, so C-2 stays at face level for life.
  And under GPT the **corridor** pushes the other way on heavily funded young cells:
  with `DB = 250% x AV'` to attained age 40, a dump-in raises the death benefit
  alongside the account value, so it raises NAR — and C-2 [S3][R2].
- **TAC couples back to the opinion.** The AVR counts in Total Adjusted Capital only to
  the extent **not utilized in asset adequacy testing** in support of the actuarial
  opinion, so the AAT routine must report the AVR it consumed [REG-R128][REG-R29]. Model
  #312 separately requires an RBC Plan projecting statutory operating income, net income
  and capital and surplus for the current year and **at least four succeeding years**,
  with and without corrective action [REG-R125].

### Product-specific interactions and traps

1. **The account value is not the reserve, and neither is the cash surrender value.**
   `AV(t)` is a contract-mechanics balance; the statutory reserve is the Model 585
   GMP/GMF construction, or the VM-20 minimum built on it. Where the reserve falls below
   the immediately available surrender value the gap is picked up separately as
   **surrender values in excess of reserves otherwise carried** in Exhibit 5
   Miscellaneous Reserves [REG-R89] — not by raising the reserve to `CSV(t)`. Model
   585's alternative minimum reserve test is the formulaic counterpart [R1].
2. **Two different net amounts at risk live in one model.**
   `NAAR(t) = DB(t)/(1 + i_gm) − AV'(t)` is the COI base, discounted one month at the
   *guaranteed* rate with AV measured before the deduction [S3]; the **C-2 NAR is face
   in force minus statutory reserves**, general and separate account, net of
   reinsurance, sourced from annual statement lines [REG-R142]. Using the COI NAAR for
   C-2 misstates capital.
3. **The surrender-charge schedule surfaces in three statutory places at once**: the
   Exhibit 5 Miscellaneous Reserves excess above; the driver the C-3a
   withdrawal-provision axis would key off if that axis were applied to a life reserve
   (unsourced, not asserted); and the year-10 lapse shock `M_sc = 2.0` **[std]** this
   file already carries, which moves surrender cash flows into asset adequacy analysis
   and the C-3a exposure base.
4. **"All Other" does not mean "no formulaic work".** Passing both exclusion tests
   removes the DR and SR, not the NPR — and this product's NPR *is* the VM-A/VM-C
   formulaic basic reserve [REG-R3 §3.B.6][REG-R110]. A model treating VM-20 as a
   replacement for the Model 585 engine cannot compute its own net premium reserve.
5. **The NGE pair is a pricing lever, a C-2 categorisation input and an ASOP
   2-constrained quantity at once.** The credited-rate spread and the 60% COI factor
   this file already names as the dominant sensitivities are the same quantities the RBC
   pricing-flexibility test measures [REG-R128] and ASOP 2 restricts [R8][REG-R26]; a
   sensitivity run widening the spread without asking whether the repricing would be
   ASOP 2-admissible produces a C-2 categorisation the company could not defend.
6. **AVR and IMR: no factor values here, and the legs that bite are specific.** Both
   apply to the general account backing this block [REG-R85][REG-R86], and **no AVR
   factor and no IMR amortisation factor is stated anywhere in this library** [REG-R89].
   This product has **no market value adjustment**, so the MVA leg of the IMR does not
   arise; the liability leg that can is **block reinsurance**, entering IMR only where
   the portion reinsured exceeds **5% of general account liabilities**, irrevocably and
   to a non-affiliate [REG-R86][REG-R92 ¶54]. The **excess-withdrawal exemption** does
   reach the product directly: withdrawable reserves include ordinary life surrenderable
   without an MVA, and effective withdrawals include unscheduled withdrawals and
   surrenders **plus the net increase in policy loans** [REG-R89] — so `W(t)` and
   `ΔL(t)` are statutory inputs, not only behaviour. Negative-IMR admittance must be
   tested **at every reporting date** on a **10%** cap and a **300% of Authorized
   Control Level** gate, and is currently written to sunset **December 31, 2026 with
   automatic nullification January 1, 2027** [REG-R87]; the replacement guidance is
   still open — see `us/regulatory/statutory-accounting-and-capital.md`.
7. **This is the base chassis for three siblings, and each changes the statutory
   answer.** `indexed-ul` keeps the same §3.B.6 VM-A/VM-C NPR where no DR or SR is
   computed [REG-R3] but takes C-3a factors **on guaranteed values ignoring those
   related to the index** and is **excluded from C-3 cash flow testing** [REG-R128],
   engages the §6.A.1.b hedging bar once an index hedge program exists, and reports in
   the **ULSG** column if it carries a secondary guarantee [REG-R89]. `variable-ul` adds
   a separate account under SSAP No. 56 — premiums are general account income *and* a
   transfer, GMDB reserves stay in the **general account**, separate account surplus may
   not be negative, a fair-value separate account needs **no IMR and no AVR except on
   seed money**, the VM-20 §2.F split floors the general account share at zero, and the
   **stochastic exclusion certification method is unavailable to variable life**
   [REG-R83][REG-R3]. `guaranteed-ul` moves to the **ULSG** category: NPR under §3.B.5
   with its own lapse construction, **deemed failure of the deterministic exclusion
   test** unless the secondary guarantee is non-material, no certification method, the
   **"Permanent without Pricing Flexibility"** C-2 bucket at the highest factors, and
   AG 48 / Model #787 exposure [REG-R3][REG-R128][REG-R11][REG-R12][REG-R7]. Switching
   on this product's own footnote-17 no-lapse guarantee moves it toward that world.

---

## Valuation and reserve pointers

This library projects gross liability cash flows; reserve layers consume them and are
NOT reproduced here. Where these bases sit inside statutory reporting and capital —
which applies from when, which exhibit consumes the result, and what the model must
additionally produce — is "Statutory accounting and capital" above; the list below is
the pointer set only:

- **Statutory (pre-PBR / formulaic).** Model 585 Section 5 CRVM adaptation for UL:
  Guaranteed Maturity Premium / Guaranteed Maturity Fund construction with the
  r = min(1, policy value/GMF) ratio, and the alternative minimum reserve test [R1].
  Nonforfeiture floor: Model 585 Section 6A retrospective minimum CSV [R1].
- **Statutory (PBR).** VM-20 minimum reserve for life products (net premium reserve
  plus deterministic/stochastic excess subject to exclusion tests), per the Valuation
  Manual (operative 2017-01-01; accreditation standard 2020-01-01) [R5][REG-R3];
  implementation guidance in the AAA VM-20 practice note [REG-R23]. Prescribed NPR
  mortality: 2017 CSO family via VM-M [REG-R3][REG-R17; exact table mapping
  [unverified]].
- **Tax.** IRC 807: greater of net surrender value and 92.81% of the NAIC-method
  reserve, capped at statutory [REG-R16].
- **Standards for the modeling work itself.** ASOP 7 (life cash flow analysis)
  [REG-R27]; ASOP 52 (PBR reserves) [REG-R31]; ASOP 56 (modeling: validation,
  documentation, model risk) [REG-R32]; NGE determination under ASOP 2 [R8].

---

## Key sensitivities and model risks

Dominant assumptions (in rough order for a cash-value-oriented block):

1. **Credited-rate spread and current COI scale (the NGE pair).** They set the AV
   growth net of charges and hence funding adequacy, surrender values, and the
   grace/lapse cascade. Both are [std] snapshots here because insurers do not publish
   them [S3][S5]; sensitivity-test the 60% COI factor and the 4.00% credited rate
   first.
2. **Premium persistency.** UL cash flows are premium-behavior-driven; paid/planned
   ratios vary by product focus and duration [R7]. Underfunding accelerates
   shortfall-driven lapse; dump-ins interact with GPT/7-pay limits.
3. **Lapse/surrender, especially at surrender-charge expiry.** Current-assumption UL
   charge structures can be lapse-supported; the year-10 shock multiplier materially
   moves the value of later-duration COI margins.
4. **Mortality at high attained ages.** COI rates grade to 1000/12 at ages 112–120
   and to zero at 121+ while coverage continues [S3]; late-age mortality assumptions
   drive the cost of the post-121 charge-free period.

Known modeling pitfalls:

- **Deduction/interest ordering.** The recursion applies interest to the
  post-deduction balance; reversing the order overstates AV by roughly one month's
  interest on MD each month and compounds over decades.
- **NAAR convention.** The specimen discounts DB one month at the *guaranteed* rate
  and measures AV *before* the deduction [S3]. Using the current rate in the
  discount, or AV after deduction (which makes COI implicit and requires iteration),
  produces small but systematic COI errors.
- **Corridor circularity under Option B.** DB depends on AV' and NAAR depends on DB;
  with the BOM ordering above there is no simultaneity, but corridor-active cells
  (heavily funded, older ages) are sensitive to where in the order AV is measured.
- **Daily-vs-monthly interest.** The contract credits daily on a 365-day year [S3];
  monthly discretization is a [std] approximation — do not also compound daily, and
  document the convention when reconciling to admin-system values.
- **ANB vs ALB mismatch.** Mortality/corridor lookups must match the [std] ANB basis;
  the 2017 CSO/2015 VBT families ship both variants [R4][REG-R18].
- **Era mixing.** The guaranteed COI table is a 2001 CSO-era specimen table [S3]
  paired here with a 2%-guarantee-era interest assumption **[std]**; a production
  model for post-2020 issues should substitute a 2017 CSO-capped guaranteed table
  (not publicly obtained — research gap) [R4][unverified].
- **Grace-period timing.** The 61-day grace spans two monthiversaries; skipping the
  due-and-unpaid deduction accrual understates death claims in grace [S3].
- **MEC/GPT are not cash flows.** Modeling them as charges or refunds distorts
  premium income; they are caps/flags only [S3][R2][R3].
