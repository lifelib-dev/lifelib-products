# Level Premium Term Life Insurance — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03. Companion to `product-spec.md` in this directory — all
contractual parameters used here (premiums, fee, modal factors, windows) are the same
representative values specified there. This is a **standardized composite** for reference
modeling, not any single insurer's product. [S#]/[R#] tags cite the product research notes
(`us/_research/term-life.md`); [REG-R#] tags cite the cross-product reference library
(`us/references/regulatory-and-actuarial-references.md`; research provenance in
`us/_research/regulatory-actuarial.md`, same R-numbering); **[std]** marks standardizations introduced for
the reference implementation; [unverified] flags carry over from the research notes.

---

## Model scope and conventions

- **Scope.** Single-life, fully underwritten level premium term per `product-spec.md`:
  10/20/30-year level periods (base cell 20-year), Jump-to-ART post-level term (PLT) with
  unchanged face to expiry at attained age 95, convertible before min(end of level period,
  attained age 70), no cash value, non-participating [S2][S3][S6]. Gross liability cash
  flows only; reserves are pointers (see Valuation section).
- **Projection frequency [std].** Annual steps are the default; a monthly mode is provided
  as an option. Annual is adequate because all decrements are contractually annual-cycle
  (level premiums, ART renewals at anniversaries) and there is no account value requiring
  monthiversary processing. Monthly mode matters when modal premium cash flow timing,
  mid-year claim timing, or mode-specific behavior (monthly-mode policies show materially
  lower shock lapse and PLT mortality deterioration [R4]) is in scope.
- **Timing [std].** Anniversary (BOY/BOM) processing: premiums and premium-linked expenses
  at the beginning of the period; deaths during the period with claims paid at period end;
  lapses, shock lapses, and conversions at period end after deaths. The shock lapse is
  processed at the END of the final level-period year (equivalently, immediately before the
  first ART premium falls due) — consistent with VM-20's "shock lapse in the final year of
  a level premium period" [R2] and the SOA study's measurement of lapse at the end of the
  level term [R4].
- **Age basis.** Age nearest birthday (ANB) **[std choice, sourced pattern]**: all four
  carriers with verifiable age rules use ANB [S2][S3][S5][S6], and 2017 CSO / 2015 VBT are
  published in ANB variants [R3][REG-R18]. Attained age x+t = issue age + completed policy
  years [S3][S5][S6].
- **Model points.** Single-policy model points (seriatim); one policy per model point with
  a count/weight field for grouping. VM-20 NPR is a seriatim quantity [R2], so seriatim
  granularity keeps the projection reusable for valuation feeds.
- **Units.** Currency in USD; face in dollars; rates per $1,000 where contractual
  [S2][S3][S5]; decrement rates are annual effective unless subscripted `m` for monthly.

---

## Model point attributes

| Attribute | Type | Example (specimen anchor cell) |
|---|---|---|
| `policy_id` | str | "TL-000001" |
| `issue_date` | date | 2026-01-01 |
| `issue_age` | int (ANB) | 35 |
| `sex` | enum {M, F} | M |
| `rate_class` | enum {PPlusNT, PNT, StdNT, StdTob} | StdNT |
| `plan` | enum {T10, T20, T30} | T10 |
| `face_amount` | float ≥ 100,000 | 100,000 |
| `band` | int 1–4 (derived from face) | 1 |
| `premium_mode` | enum {A, SA, Q, M} | A |
| `policy_count` | float (weight) | 1.0 |
| `duration_inforce` | int (for in-force runs; 0 at issue) | 0 |

The example column is the specimen anchor cell M35/StdNT/$100k/10-yr [S6], which the worked
example below projects. Attribute menu per `product-spec.md` (issue-age grid **[std]**,
4 classes **[std]**, 4 bands [S5]/**[std]**).

## State variables

| Variable | Definition |
|---|---|
| `l(t)` | In-force policies at start of period t (l(1) = policy_count at issue) |
| `d(t)` | Deaths in period t |
| `x(t)` | Lapses (incl. shock lapse) at end of period t |
| `c(t)` | Conversions at end of period t |
| `AP(t)` | Annualized guaranteed gross premium for policy year t (from rate table + fee) |
| `dur(t)` | Policy year (curtate duration + 1) |
| `phase(t)` | LEVEL (dur ≤ n), PLT (n < dur, attained age < 95), EXPIRED |
| `conv_elig(t)` | Boolean: dur ≤ n and attained age < 70 |

No account value, cash surrender value, loan, or shadow-account state exists for this
product [S3][S6].

---

## Assumption inputs

Three classes are distinguished; keeping them in separate input structures is deliberate
architecture (the same split VM-20 makes between prescribed/guaranteed and prudent-estimate
elements [R2][REG-R23]).

### (a) Contractual / guaranteed elements (from the spec — cited)

| Item | Value | Basis |
|---|---|---|
| Guaranteed premium scale | Level `AP` for n years, then guaranteed ART scale to age 95; full schedule printed at issue | [S3][S6] |
| Anchor schedule (M35/StdNT/$100k/10-yr) | $140 (yrs 1–10); $764, $830, $992 (yr 15), $1,526 (yr 20), $4,250 (yr 30), $10,946 (yr 40), $30,965 (yr 50), $74,780 (yr 60, age 95) | [S6] |
| Policy fee | $65/yr, level, inside `AP` | [S6] |
| Modal factors | SA 0.52 / Q 0.27 / M 0.08333 | [S6] |
| Death benefit | Level face; proceeds = face + pro-rata unearned premium − due unpaid premium | [S6] |
| Grace | 31 days | [S3][S6][S7] |
| Conversion window / credit | min(n, age 70); credit = one annual premium after year 1 | [S2][S3][S6] |
| Expiry | Attained age 95 | [S2][S3][S5][S6] |

### (b) Current non-guaranteed scales

For this product there are none: premiums and death benefit are fully guaranteed
[S3][S6], and the representative product sets the current PLT scale equal to the
guaranteed Jump-to-ART scale **[std]** (product-spec fn 10; graded current PLT scales
observed in the market [R4] are a documented variation, not modeled). This block is
intentionally empty so the input schema matches sibling products (UL etc.).

### (c) Behavioral / experience assumptions (best estimate)

| Assumption | Recommended public basis | Reference-model standardization |
|---|---|---|
| Best-estimate mortality | 2015 VBT primary tables (ANB, sex/smoker-distinct) with relative-risk (RR) tables for preferred fit [REG-R18], A/E-adjusted to ILEC 2012–2019 inter-company experience [R8][REG-R19] (ILEC expected basis 2015 VBT RR100 [unverified]) | Class factors on 2015 VBT-style base: PPlusNT 0.80, PNT 0.90, StdNT 1.00, StdTob 1.75 **[std]** (fn A) |
| Guaranteed-basis mortality (for reserve feeds) | 2017 CSO, ANB, smoker-distinct, loaded [R3][REG-R17] | Direct table lookup, no adjustment |
| Level-period lapse | SOA/LIMRA 2015–2022 Term & WL lapse study [R6]; older full-factor study [REG-R20] | Duration vector, fn B **[std]** |
| Shock lapse & PLT lapse | SOA U.S. Post-Level Term study (2021) [R4][REG-R22] | Jump-ratio-keyed table, see Policyholder behavior **[std]** |
| PLT mortality deterioration | Same study [R4][REG-R22] | Multiplier grading 3.50 → 2.00, see Policyholder behavior **[std]** |
| Conversion rate | SOA 2016 conversion experience study [R7] (2009–2023 SOA/LIMRA update in progress [R7, partly unverified]) | 1%/yr while eligible; 2% in final eligible year **[std]** (fn C) |
| Maintenance expense | — (no public basis in research set) | $30/policy/yr inflating 2%/yr **[std]** (fn D) |
| Acquisition expense | — | $300/policy at issue **[std]** (fn D) |
| Commission | — | 80% of premium year 1; 5% years 2–n; 2% PLT **[std]** (fn D) |
| Premium tax | — | 2.0% of collected premium **[std]** (fn D) |
| Premium persistency (modal) | Annual-mode base cell; mode mix optional | Mode affects PLT behavior only via [R4] factors, optional **[std]** |

**Footnotes**

- **(A) Class factors [std].** The 2015 VBT provides 10 nonsmoker and 4 smoker RR tables
  for preferred-class fit [REG-R18]; the four factors {0.80, 0.90, 1.00, 1.75} are a
  compressed stand-in chosen so that StdNT reproduces the specimen anchor pricing cell
  [S6] and the NT spread stays inside the RR-table range. Calibration to actual RR tables
  is an implementation refinement.
- **(B) Level-period lapse [std].** Annual rates by policy year: 6%, 5%, then 4% for years
  3 through n−2, n−1: 6% (anticipatory rise — lapse rates begin increasing one to two
  policy years before the end of the level period [R6]), year n: shock lapse (below).
  Detailed study rates by sex/age/band/mode sit behind SOA paid data packages (research
  notes, Gaps); the vector is an order-of-magnitude standardization consistent with the
  public highlights: 30-year term lapse rates at attained ages 60+ run 1.0%–1.5% [R6], so
  for T30 the 4% mid-band grades to 1.5% from attained age 60 **[std]**.
- **(C) Conversion [std].** The public 2016 study landing page documents incidence
  analysis by age/sex/class/size but no headline rate was recorded in the research notes
  [R7]; 1%/yr (2% final year) is a placeholder magnitude. Treatment of the conversion cash
  flow: see Cash flow components.
- **(D) Expenses/commission [std].** No insurer expense or commission data appear in the
  retrieved public documents; these are round reference values for a complete gross cash
  flow statement. Replace with company-specific unit costs in any real application. The
  policy fee ($65 [S6]) is intended as the contractual funding of per-policy maintenance.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| x | Issue age (ANB); n = level term period in years; F = face amount |
| t | Policy year, t = 1, 2, …, 95 − x (annual model) |
| l(t) | In-force count at start of year t; l(1) = 1 per unit model point |
| q(t) | Best-estimate annual mortality at attained age x+t−1, incl. class factor and PLT multiplier |
| w(t) | Annual lapse rate for year t (w(n) = shock lapse) |
| cv(t) | Annual conversion rate (0 outside eligibility window) |
| AP(t) | Annualized guaranteed gross premium for year t |
| G(t) | Premium income in year t; K(t) commission; E(t) expenses; X(t) premium tax |
| DC(t) | Death claims incurred in year t; CV(t) conversion credit outflow |
| M(d) | PLT mortality multiplier at PLT duration d = t − n |
| J | Initial premium jump ratio = AP(n+1)/AP(n), fee included [R4][R2 convention] |

### Decrement order and recursion (annual model)

Deaths first, then end-of-year voluntary decrements (lapse and conversion) applied to
survivors, with conversion and lapse treated as competing rates on the same survivor pool
**[std]**:

```
d(t)  = l(t) · q(t)
s(t)  = l(t) · (1 − q(t))                     survivors to end of year t
c(t)  = s(t) · cv(t)
x(t)  = s(t) · (1 − cv(t)) · w(t)
l(t+1)= s(t) · (1 − cv(t)) · (1 − w(t))
      = l(t) · (1 − q(t)) · (1 − cv(t)) · (1 − w(t))
```

Termination at expiry: l(t) = 0 for x + t − 1 ≥ 95 [S2][S3][S5][S6].

### Cash flows (annual model, per unit in force at issue)

```
G(t)  = AP(t) · l(t)                          premium, BOY  [S6 schedule]
K(t)  = k(t) · G(t)                           commission, BOY  [std]
X(t)  = 0.02 · G(t)                           premium tax, BOY  [std]
E(t)  = 300 · 1{t=1} + 30 · 1.02^(t−1) · l(t) maintenance/acquisition, BOY  [std]
DC(t) = F · d(t)                              death claims, EOY  [S6]
CV(t) = AP(t) · c(t) · 1{t>1}                 conversion credit, EOY  [S6]
NetCF(t) = G(t) − K(t) − X(t) − E(t) − DC(t) − CV(t)
```

Simplifications **[std]**: (i) the pro-rata unearned-premium refund on death [S6] is
ignored in the annual model (it is a half-premium-sized timing item on the deceased cohort;
in monthly mode it becomes immaterial by construction); (ii) grace-period mechanics
[S3][S6] are not separately modeled — lapse is treated as effective at the anniversary;
(iii) reinstatement [S3][S6] is not modeled as a decrement reversal.

### Conversion treatment [std choice — explained]

Two defensible treatments exist:

1. **Decrement with cost load (adopted).** Conversion removes the policy from the term
   block (`c(t)` above); the direct cash flow charged to the term product is the
   contractual conversion credit of one annual premium [S6]. The post-conversion mortality
   anti-selection documented by the SOA conversion studies [R7] is borne by the permanent
   product's model, not double-counted here. Adopted because it keeps the term model
   self-contained, uses only contractual cash flows, and matches how the conversion credit
   is actually paid (against the new policy's initial premium [S6]).
2. **Transfer-out (alternative).** Model conversion as a zero-cash-flow transfer to a
   companion permanent model point (lifelib-style linked runs). Preferable when the library
   is run as a linked term+permanent projection; the switch is an output-routing choice,
   not a different liability.

### Monthly option — processing order (monthiversary)

Monthly decrements **[std]**: `q_m = 1 − (1 − q)^(1/12)`, `w_m = 1 − (1 − w)^(1/12)` for
ordinary lapses; the shock lapse `w(n)` is NOT spread — it is applied in full at the final
level-period monthiversary (month 12n). Numbered order each month:

1. Check expiry (attained age 95) and terminate [S2][S3][S5][S6].
2. Collect modal premium if due this month (monthly mode: 0.08333 × AP [S6]); annualized
   modal load is implicit in the modal factor.
3. Pay commission and premium tax on premium collected **[std]**.
4. Incur 1/12 of annual maintenance expense; acquisition expense in month 1 only **[std]**.
5. Apply deaths at `q_m`; pay claims at end of month: F + pro-rata unearned premium − due
   unpaid premium [S6].
6. Apply conversions at `cv_m` if within the eligibility window; pay conversion credit
   [S2][S3][S6] (before any lapse, matching the annual recursion's conversion-before-lapse
   order).
7. At the level-period-end monthiversary only: apply shock lapse to survivors **[std]**
   (per [R2][R4] timing).
8. Apply ordinary lapses at `w_m` to remaining survivors **[std]**.
9. Roll forward `l`.

---

## Policyholder behavior modeling

All dynamic formulas in this section are **[std]** standardizations calibrated to the
ranges published in the SOA 2021 PLT study [R4][REG-R22]; none is itself a published
industry formula.

### Shock lapse at end of level period

Keyed to the initial premium jump ratio J = AP(n+1)/AP(n) with the policy fee included in
both premiums — the jump definition used by both the SOA 2021 study [R4] and VM-20's
prescribed-shock table (premium increase per $1,000 including the policy fee) [R2]:

| J (jump ratio) | Shock lapse w(n) **[std]** |
|---|---|
| ≤ 2.0 | 35% |
| 2.0 – 4.0 | 55% |
| 4.0 – 6.0 | 80% |
| 6.0 – 8.0 | 85% |
| > 8.0 | 90% |

Rationale: the study's observed Jump-to-ART shock lapses span 27%–96% and increase with
the jump ratio and attained age [R4]; the bucket values sit inside that envelope. The anchor
cell (J ≈ 5.46 [S6]-derived) takes 80% — which coincidentally equals the VM-20 prescribed
NPR shock for its 10-year level period jumping to ART with a ≥400% increase [R2], but note
the two are conceptually distinct (best estimate vs prescribed). Optional refinements
supported by the study: +5 pts at attained ages 60+ and −15 pts for monthly-mode policies
(monthly mode shows materially lower shock lapse [R4]) **[std]**.

### PLT lapse after the shock

Elevated but declining by PLT duration [R4]: w(n+1) = 30%, w(n+2) = 15%, w(n+d) = 10% for
d ≥ 3 **[std]**, until expiry.

### PLT mortality deterioration (anti-selection)

Multiplicative on the best-estimate base table:

```
q(n+d) = q_base(x+n+d−1) · class_factor · M(d)
M(1)   = min(8.0, 1 + 0.55 · (J − 1))          [std]
M(d)   = max(2.0, M(1) − 0.15 · (d − 1))       [std]  (grade to 200%, then level)
```

For the anchor cell J ≈ 5.46 gives M(1) = 3.45 ≈ 3.50 (the worked example uses 3.50).
Rationale: first-year Jump-to-ART deterioration observed at 154%–1,066% of level-period
mortality, increasing with the jump; deterioration declines over PLT durations, falling
below 200% after roughly 10 years [R4] — M(d) reaches 2.00 at d = 11 and stays level.
Monthly-mode policies show lower deterioration [R4]; an optional 0.75 multiplier on
(M(d) − 1) for monthly mode is supported **[std]**.

### Anticipatory lapse

w(n−1) is set 2 points above the mid-duration level (6% vs 4% in the base vector), because
lapse rates begin to rise one to two policy years before the end of the level period [R6]
**[std]**.

### Conversion

cv(t) = 1% while `conv_elig`, 2% in the final eligible year (option value is highest just
before the window closes) **[std]**; zero otherwise. Anti-selective conversion interacts
with PLT deterioration — converters are disproportionately impaired lives [R7 scope;
magnitude not recorded] — so implementations linking term and permanent blocks should not
apply both a conversion cost load and full PLT deterioration to the same lives (see
Conversion treatment above).

---

## Worked example

Specimen anchor-cell model point M35 / Standard NT / $100,000 / 10-year plan / annual mode, unit
in-force. Contractual premiums from the specimen guaranteed schedule: AP(1..10) = $140,
AP(11) = $764, AP(12) = $830 [S6]; J = 764/140 ≈ 5.46. Assumptions: illustrative
best-estimate q_base rising from 0.00080 (age 35) to 0.00160 (age 44) — vector 0.00080,
0.00085, 0.00090, 0.00095, 0.00100, 0.00110, 0.00120, 0.00130, 0.00145, 0.00160 — then
0.00180/0.00200 (ages 45/46) with M(1) = 3.50, M(2) = 3.35 **[std]**; lapse vector 6%, 5%, 4%×6, 6%
(anticipatory), 80% (shock), 30%, 15% **[std]**; commission 80%/5%/2%, premium tax 2%,
maintenance $30 × 1.02^(t−1), acquisition $300 **[std]**. All flows per the recursion above
(premium/commission/tax/expense BOY, claims EOY, no discounting).

| t | l(t) | Premium G | Claims DC | Comm K | Maint+Acq E | Tax X | Net CF | l(t+1) |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 140.00 | 80.00 | 112.00 | 330.00 | 2.80 | −384.80 | 0.939248 |
| 2 | 0.939248 | 131.49 | 79.84 | 6.57 | 28.74 | 2.63 | 13.71 | 0.891527 |
| 3 | 0.891527 | 124.81 | 80.24 | 6.24 | 27.83 | 2.50 | 8.01 | 0.855096 |
| 4 | 0.855096 | 119.71 | 81.23 | 5.99 | 27.22 | 2.39 | 2.88 | 0.820112 |
| 5 | 0.820112 | 114.82 | 82.01 | 5.74 | 26.63 | 2.30 | −1.86 | 0.786520 |
| 6 | 0.786520 | 110.11 | 86.52 | 5.51 | 26.05 | 2.20 | −10.16 | 0.754229 |
| 7 | 0.754229 | 105.59 | 90.51 | 5.28 | 25.48 | 2.11 | −17.79 | 0.723191 |
| 8 | 0.723191 | 101.25 | 94.01 | 5.06 | 24.92 | 2.02 | −24.78 | 0.693361 |
| 9 | 0.693361 | 97.07 | 100.54 | 4.85 | 24.37 | 1.94 | −34.63 | 0.650814 |
| 10 | 0.650814 | 91.11 | 104.13 | 4.56 | 23.33 | 1.82 | −42.73 | **0.129955** |
| 11 | 0.129955 | 99.29 | 81.87 | 1.99 | 4.75 | 1.99 | 8.69 | 0.090395 |
| 12 | 0.090395 | 75.03 | 60.56 | 1.50 | 3.37 | 1.50 | 8.09 | 0.076321 |

Reading the table: the 80% shock lapse at the end of year 10 collapses in-force from 0.651
to 0.130; year-11 premium per survivor jumps 5.46× while year-11 expected claims per
survivor reflect q = 0.00180 × 3.50 = 0.0063 — the anti-selected PLT block barely clears
its own claims [pattern per R4]. Conversion is switched off (cv = 0) in this table to keep
it to one decrement narrative; enabling cv(t) per the behavior section removes a further
~1%/yr of `s(t)` during years 1–10 and adds the CV(t) outflow. (This worked example uses
guaranteed premiums that are contractual [S6]; every decrement/expense number is
illustrative **[std]** — it is a mechanics check, not a pricing result.)

Cross-checks: the table was computed mechanically from the recursion exactly as specified
above; l(11) = 0.650814 × (1 − 0.0016) × (1 − 0.80)
= 0.129955 ✓; monthly q from annual 0.0016 would be 1 − (1 − 0.0016)^(1/12) = 0.00013343 ✓.

---

## Statutory accounting and capital

Framework and the shared model-output contract are in `us/regulatory/statutory-accounting-and-capital.md`
and `us/regulatory/technical-notes.md`; this section states only what is specific to level premium term.
[REG-R#] resolves against the shared numbering used throughout this file, which now runs **R1–R142**
(R114–R124 and R143–R149 unused by design).

### Contract classification and reporting

- **A life contract in every case, so the classification flag is a constant.** The test is mortality risk —
  payments contingent on death [REG-R80 ¶2] — and SSAP No. 50 ¶9 lists term among life contracts. This
  product has nothing *but* mortality risk (no account value, no cash surrender value, no investment
  element [S3][S6]), so the deposit-type route — a contract that "act[s] exclusively as [an] investment
  vehicle" — is unreachable at any point in its life; classification is set at inception and **immutable**
  [REG-R78 ¶¶5, 9][REG-R80].
- **Considerations are premium income**, recognised **gross, when due**, never a direct credit to reserve
  [REG-R79 ¶¶2–5]. The gross-to-net difference is loading, and the change in loading on deferred and
  uncollected premium is an **expense**, not a reduction of premium [REG-R79 ¶11] — live here because the
  modal factors 0.52 / 0.27 / 0.08333 [S6] mean most policies are not annual-mode.
- **Reporting targets.** Reserves to **Exhibit 5** and Liabilities page Line 1, never Exhibit 7; Column 1
  states the valuation standard **by years of issue**, so a XXX-era block and a VM-20 block sit side by
  side rather than one superseding the other, and VM-20 business reports on **two lines** — the net premium
  reserve and the excess over it [REG-R89][REG-R90][REG-R1 §11]. Face in force goes to the **Exhibit of
  Life Insurance** in thousands, and the reporting dimension is the **Term Life** column of the Analysis of
  Operations and of the Analysis of Increase in Reserves; out-of-scope waiver-of-premium and children's
  riders would carry SSAP No. 54 A&H reserves on the **base contract's** line, inside Term Life
  [REG-R89][REG-R90][REG-R82].
- **Conversion presentation is not addressed by the retrieved instructions** — termination-plus-new-issue
  versus transfer across the Term Life and permanent columns is not stated in the instructions or blank
  read [REG-R89][REG-R90], and this library does not fill that hole.

### Reserve basis

- **Two regimes, keyed by year of issue.** Pre-operative-date issues run formulaic **CRVM** under Standard
  Valuation Law §5 through the VM-A index, whose substantive term item is **A-830 — Model #830, "Regulation
  XXX"**; deficiency reserves survive as a distinct **Exhibit 5 Miscellaneous Reserves** item via Actuarial
  Guideline I in the VM-C index and via A-830 [REG-R1][REG-R110][REG-R6][REG-R41][REG-R89]. **A-820 and
  A-830 as printed in the AP&P Manual were not retrieved** [REG-R110][REG-R33], so the mechanics documented
  here rest on Model #830 itself [R1][REG-R6]. Issues on and after the Valuation Manual operative date take
  **VM-20 as the minimum** under SVL §11 [REG-R1] (that date is [unverified] in the print).
- **Term is one of VM-20's three reserving categories**, so the minimum reserve is the *sum* over
  K ∈ {Term, ULSG, All Other} and a Term excess can never be offset against All Other slack; a DR group
  spanning categories is split with the difference allocated proportionally, and an SR aggregation subgroup
  spanning categories must also produce a stand-alone Term SR [REG-R3 §§2.A, 4.C, 5].
- **The "neither DR nor SR" path is closed to term.** Reporting Σ NPR alone is permitted only for ULSG with
  a non-material secondary guarantee passing both tests, or for All Other [REG-R3 §2.A]; with the
  deterministic exclusion test **not available at all for term insurance policies or term riders**
  [REG-R3 §6.B], a term block computes a **deterministic reserve in every case** — no configuration of this
  product lets the VM-20 modelled-reserve engine be skipped.
- **NPR mechanics that are term's own** [REG-R3 §§3.B.4, 3.C.3, 3.D, 3.E]: prescribed lapses of **10%**
  during a level premium period under five years, **6%** for five or more, **0%** once the final premium
  has been payable; the prescribed shock-lapse table of **25%–80%** applied in the final level-period year
  *after* benefits assumed payable that year and *before* the increased premium takes effect (anchor jump
  ≈446% including fee [S6]-derived → **80%** [R2]); a valuation interest rate **increased by 1.5% but
  capped at 125%** of the unuplifted rate, rounded to the nearest quarter with **ties up** — the opposite
  convention from the base rate; a §3.D floor collapsing to the cost of insurance to the next paid-to-date,
  the CSV leg being zero [S3][S6]; and **policy minimum NPR = NPR less the §8 ceded reinsurance credit**.
- **Year one differs and two premium conventions must not mix.** The Term valuation net premium is **zero
  in policy year 1**, so the due-and-deferred premium asset and the unearned premium reserve are zero that
  year [REG-R3 §2.A]; the mean reserve method's deferred premium asset applies to formulaic blocks
  [REG-R81/IP51 ¶21] but **inside a VM-20 projection deferred premiums are zero** [REG-R3 §7.B].

### What this product's model must additionally produce

Shared contract: `us/regulatory/technical-notes.md`, "Required model outputs". Rows below are the ones this
product specialises or makes trivial.

| Statutory item | Required model output for level premium term | Cite |
|---|---|---|
| Exhibit of Life Insurance; C-2 exposure base | Face in force and policy counts on an **incurred** basis, in thousands, gross and net of reinsurance | [REG-R89][REG-R142] |
| C-2 net amount at risk | `NAR = face in force − life reserves`, general **plus separate** account, net of reinsurance — the separate-account leg is identically zero here | [REG-R142] |
| Exhibit 5 | Reserves keyed by **valuation standard × year of issue**; VM-20 business split NPR and excess; XXX-era deficiency reserve to Miscellaneous Reserves | [REG-R89][REG-R6] |
| Analysis of Increase in Reserves | Tabular net premium (zero in NPR year 1), tabular interest, tabular cost, reserves released by death and by other terminations — on the **valuation** basis, not the experience basis of the worked example above | [REG-R90][REG-R3] |
| Summary of Operations | Change in loading on deferred and uncollected premium as an **expense**; commission and issue expense in the issue period with **no DAC stream** | [REG-R79 ¶11][REG-R75 ¶2] |
| Exhibit 5 ceded column; VM-20 §8; AG 55 | Gross and ceded **produced separately, never netted**, per treaty; YRT credit as the one-year term mean reserve on the ceded amount, on the *original policy's* mortality and interest basis | [REG-R89][REG-R92 ¶¶37–38][REG-R103] |
| Tax | Tax reserve = 92.81% × NAIC-method reserve, floored at net surrender value (**zero** for term), capped at statutory | [REG-R16] |
| Asset adequacy analysis | Starting assets no greater in statement value than the reserves tested; sign-aware IMR allocation; the **AVR consumed**, reported as an output because it is removed from Total Adjusted Capital | [REG-R29][REG-R100][REG-R128] |
| VM-31 / VM-G | Which exclusion-test route was taken, and a statement of **readiness to compute the SR** even where it is excluded | [REG-R108][REG-R109] |

Not needed for this product: separate-account balances and transfers (none exist [S3][S6]) and a
**repricing scenario** for the C-2 pricing-flexibility test (below).

### Risk-based capital

- **C-2 mortality dominates and net amount at risk is the whole of it.** With no account value and no cash
  surrender value [S3][S6] there is nothing to net down: `NAR = face in force − life reserves`, net of
  reinsurance, so C-2 tracks **face amount** while term reserves stay small relative to face. Note the
  sign: reserve strengthening *lowers* C-2 while raising the reserve-based C-3a below, and at band-1
  factors the offset is incomplete **[std, derived]**. The base is now taken from annual statement lines
  rather than company records [REG-R142], so the model must reproduce those lines, not a policy-level NAR.
- **The C-2 category is settled by the contract, not by a scenario.** Pricing flexibility is the ability to
  *materially* adjust rates on in-force contracts within the next **5 policy years**, tested on a
  present-value basis [REG-R128]; premiums here are fully guaranteed to expiry with no non-guaranteed
  elements [S3][S6], so no repricing margin exists. The instructions' own example of **"Individual &
  Industrial Term without Pricing Flexibility"** is level term with guaranteed level premiums, and the
  default for direct individual term where no assessment is performed is the same bucket
  [REG-R128][REG-R133]. Pre-tax factors per dollar of NAR: **0.00280** on the first $500M, **0.00120** on
  the next $24,500M, **0.00085** over $25,000M, banded on the *total* individual and industrial NAR then
  allocated proportionately [REG-R128][REG-R133]. So the generic "run a repricing scenario" requirement
  does not bind this product, though it would bind the **graded-PLT** variant that re-rates in-force blocks
  [R4] (`product-spec.md`, fn 10). Ceded business runs the other way — cessions reduce NAR, **annually
  repriceable YRT** is an instruction example of "with pricing flexibility", and the default for
  non-affiliated *ceded* individual business is **With Pricing Flexibility** [REG-R128][REG-R133]. Total
  C-2 is the greatest of two guardrail terms and `sqrt(life² + longevity² + 2ρ·life·longevity)` with
  **GF = 0** and **ρ = −0.25** [REG-R128][REG-R134]: with no life-contingent annuity reserve the longevity
  term is zero, so the −25% diversification credit gives a term writer nothing.
- **C-3a is small and purely factor-based, and C-3 Phase I never reaches this product.** Life insurance
  reserves sit in the **Low** withdrawal-provision category at **0.0095** pre-tax, cut by one third to
  **0.0063** where the company files an unqualified actuarial opinion based on asset adequacy testing **or
  one qualified solely because of AG 48 direction** — a carve-out written for exactly this product's
  reserve-financing problem. C-3 Phase I's scope is "Certain Annuities" **plus single premium life**, and
  level premium term is neither, which is why the shared matrix leaves that row blank rather than marking
  it excluded [REG-R128][REG-R135].
- **Two components sit outside the covariance radical, added dollar-for-dollar** [REG-R128]: **C-4a** at
  **2.53%** of Schedule T life premiums and annuity considerations, proportionally larger for a
  high-premium/low-reserve product; and the **AG 48** Primary Security shortfall on all AG 48 cessions,
  added at **2×** then halved into Authorized Control Level so it lands one-for-one, applying even where a
  state has waived AG 48 compliance [REG-R128][REG-R11][REG-R12]. Inside the radical C-3a is added to C-1o
  in one squared term; Total Adjusted Capital includes the **AVR** limited to the amount not consumed in
  asset adequacy testing [REG-R128][REG-R29]; action levels and the trend test are per Model #312
  [REG-R125][REG-R128].

### Product-specific interactions and traps

1. **Excluding the SR has a governance price.** With the DET barred a DR exists every year and the SERT's
   route 1 is itself DR-based; passing an exclusion test by the **deterministic-reserve method re-imposes
   VM-G Sections 2 and 3** on a company that would otherwise be exempt [REG-R3 §6.A.2][REG-R109], with a
   VM-31 sub-report and a readiness statement still due [REG-R108].
2. **Post-level term decides the statutory and capital numbers.** The DR must assume 100% lapse at the end
   of the level term where PLT would otherwise be profitable while PLT losses must be reflected
   [R2][REG-R3]; §2.I forbids ignoring PLT losses [REG-R3 §2.I]; the NPR shock is prescribed at 25%–80%
   [REG-R3 §3.C.3] against a best-estimate envelope of 27%–96% [R4]. **Three lapse bases on one engine** —
   prescribed NPR, DR-with-PLT-override, prudent estimate — must be switchable, not hard-coded.
3. **XXX financing reaches back into capital.** Model #830 conservatism on term drove captive reserve
   financing, hence AG 48 and Model #787 [REG-R11][REG-R12]; the capital consequences are the RBC add-on
   outside covariance and the AG 48-qualified opinion that still earns the reduced C-3a factor [REG-R128].
4. **The gross-of-YRT run is required twice over.** The SERT's YRT relief compares the test gross and net
   of YRT [REG-R3 §6.A.2.c] and AG 55 §6.G accepts documentation of the **pre-reinsurance PBR reserve** for
   a ceded block in lieu of its mandatory cash-flow-testing run [REG-R103]; both instruct the VM-20 engine
   to run gross of a specific treaty, so build that switch once. AG 53 and AG 55 are otherwise **not
   product triggers** — their scoping is company-level (complex and high-yielding assets, from the December
   31, 2022 statement) and treaty-level (reserves reported in the December 31, 2025 annual statement)
   [REG-R105][REG-R103], which is why the shared matrix marks both `(x)`.
5. **No separate account, no derivatives, no MVA.** SSAP No. 86 is not engaged by this product's own
   mechanics [REG-R96] and the IMR's market-value-adjustment liability leg cannot arise [REG-R85][REG-R86];
   the **block-reinsurance** leg still can, where an irrevocable non-affiliate transfer exceeds **5% of
   general account liabilities** in the current year [REG-R86][REG-R92 ¶54]. Admitted negative IMR feeds
   back into the term reserve — it must be captured in the PBR calculation or in asset adequacy testing
   under VM-20 §7.D.7 and VM-30 §3.B.5 with a reconciliation [REG-R87 ¶9.e][REG-R100 §3.B.5] — and the IMR
   itself has no cash flows, entering as a sign-aware adjustment to starting assets [REG-R111]. **No AVR
   factor and no IMR amortisation factor is stated anywhere in this library**; the research deliberately
   did not transcribe them [REG-R89].
6. **Acquisition strain is the largest single statutory fact about this product.** Commission and issue
   expense are **expensed as incurred with no DAC asset** [REG-R75 ¶2][REG-R76 ¶8], so the worked example's
   year-1 net outflow of −384.80 against a 140 gross premium (80% first-year commission plus $300 issue
   cost, both **[std]**) hits surplus in full alongside the initial reserve [REG-R74 ¶¶30, 38]. Levelizing
   does not fix it: a third-party-funded levelized commission is "in fact, [a] funding agreement" and the
   full initial commission "shall be recognized immediately" [REG-R75 ¶¶4–5]. The first-year ordinary loss
   cannot be carried back by an entity taxed as a life insurance company for tax years after 2017, so its
   DTA admittance runs entirely through the RBC-band and DTL-offset components [REG-R97].
7. **Source limits that bite here.** The RBC factors above come from the **2024** *Life and Fraternal
   Risk-Based Capital Forecasting and Instructions*, a **sold NAIC publication** marked "Not for
   Distribution" read from a state department posting; the **2025 edition could not be parsed**, so **no
   year-end 2025 factor is asserted** [REG-R128][REG-R129]. Exhibit and page/line references come from the
   **2025** reporting-year blank and instructions and should be re-verified against the 2026 blank
   [REG-R89][REG-R90].

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**. Statutory reporting, the annual statement
exhibits and the RBC components for this product are in **Statutory accounting and capital**
above; this section stays a pointer list for the reserve bases themselves. Reserve layers
consume those flows but are not reproduced here:

- **VM-20 minimum reserve** = seriatim NPR + max(0, DR − NPR-aggregate) etc., with term
  NPR on 2017 CSO, prescribed interest, prescribed lapses (6%/10% by level-period length,
  prescribed shock 25%–80%, 0% after final premium) and an NPR floor at the cost of
  insurance to the next paid-to-date; the deterministic exclusion test is **not available at
  all** for term policies or term riders, so a deterministic reserve is computed in every case
  [R2][REG-R3 §6.B] (see Statutory accounting and capital above, "Reserve basis", for the
  reserving-category and exclusion-test consequences). The DR for post-2017 issues must
  assume 100% lapse at the end of the
  level term where PLT would otherwise be profitable — PLT profits cannot be capitalized;
  PLT losses must be reflected [R2]. A projection feeding VM-20 must therefore be able to
  run with (a) prudent-estimate behavior per these notes and (b) the prescribed
  NPR/PLT-override assumption sets, from the same cash flow engine.
- **Pre-PBR in-force (Regulation XXX)**: segmented vs unitary basic reserves under the
  contract segmentation method, deficiency reserves with X-factor select mortality on
  1980 CSO [R1][REG-R6].
- **Asset adequacy / cash flow testing** sits under VM-30/ASOP 22 [REG-R29] with ASOP 7
  governing the cash flow analysis itself [REG-R27] and ASOP 56 governing the model
  [REG-R32]; VM-20 practice detail in the Academy practice note [REG-R23] and assumption
  governance in the Academy resource manual [REG-R25].
- **Tax reserves**: 92.81% of the NAIC-method reserve, floored at net surrender value
  (zero for term), capped at statutory [REG-R16]. **GAAP/LDTI**: the same projected cash
  flows feed the LFPB with annually updated assumptions and single-A discounting through
  OCI [REG-R34] [unverified — source not fetched; corroborated summaries only].
  Reinsurance reserve financing of XXX
  term: AG 48 / Model #787 [REG-R11][REG-R12]; its capital consequence — the Primary Security
  shortfall added outside the covariance adjustment — is in Statutory accounting and capital
  above, "Risk-based capital".

---

## Key sensitivities and model risks

Dominant assumptions, in rough order of economic impact for a level-term block:

1. **PLT shock lapse × mortality deterioration.** These two are jointly calibrated to the
   premium jump [R4]; moving one without the other misstates the PLT tail badly. Because
   VM-20 forces PLT profits to zero in the DR [R2], PLT optimism cannot help statutory
   results but PLT pessimism (deterioration above premium loadings) flows straight through.
2. **Best-estimate mortality level and slope.** The level-period margin is thin (see
   worked example — premiums ≈ expected claims at Standard NT); a few basis points of A/E
   [R8][REG-R19] move the block's lifetime result materially.
3. **Level-period lapse.** Term with no cash value is lapse-supported in early durations
   (acquisition strain recovery) and lapse-sensitive before the shock (each year-9
   anticipatory lapse [R6] forfeits a year of level premium against no benefit).
4. **Conversion incidence.** Converts remove healthy-ish premium payers and (in linked
   models) deliver anti-selected lives to the permanent block [R7]; sensitivity grows with
   the conversion window length.
5. **Expenses/commission [std]** matter mainly through the acquisition strain and the tiny
   PLT in-force tail (fixed per-policy costs on a shrinking block).

Known modeling pitfalls:

- **Shock timing double-count.** Applying the shock lapse both at end of year n and start
  of year n+1, or spreading it across months, changes the PLT premium base materially; it
  belongs at the single point immediately before the first ART premium [R2][R4] **[std]**.
- **Jump ratio definition.** Include the policy fee in both numerator and denominator —
  the 2021 SOA study defines the jump including the fee (the 2014 study did not) [R4], and
  VM-20's shock table keys on premium increase per $1,000 including the fee [R2].
  Fee-in/fee-out inconsistency silently shifts a policy across shock buckets.
- **Deterioration base.** M(d) multiplies the *best-estimate base* mortality, not the
  guaranteed/valuation table; applying it to 2017 CSO (already loaded [R3]) double-counts
  margin.
- **ANB/ALB mismatch.** Model ages, rate table lookups, and mortality tables must share
  the ANB basis [S2][S3][S5][S6][R3]; a silent ALB table import shifts mortality by half a
  year of age.
- **Expiry handling.** The guaranteed schedule ends at attained age 95 [S6]; projecting
  ART premiums past 95, or terminating at 94 (off-by-one on `x + t − 1 ≥ 95`), corrupts
  the tail.
- **Banding on face decrease.** A requested face decrease re-scales premium excluding the
  fee (((a − b) × c) + b [S6]) and can cross a band boundary [S3]; implementations that
  re-derive `band` from `face_amount` each period handle this automatically.

---

*Companion documents: `product-spec.md` (contract terms), `sources.md` (citations).*
