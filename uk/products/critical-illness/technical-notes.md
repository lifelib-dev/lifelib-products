# Critical Illness Cover — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `uk/_research/critical-illness.md`); [REG-R#]
tags refer to the cross-product reference library
`uk/references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `uk/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. The model mirrors the term assurance reference model in
`uk/products/term-assurance/` (base chassis); only CI-specific mechanics are new here.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, main
  claims, additional-payment claims, children's-cover claims, expenses) for a
  single-policy model point of accelerated (and, as a variant, standalone) Critical
  Illness Cover. Discounting, reserves and capital are not computed (see Valuation and
  reserve pointers).
- **Projection frequency.** Monthly grid over the policy term (12 x term months)
  **[std]**. The contract itself has no accumulation account; monthly is chosen for
  parity with the other reference models in this library.
- **Timing conventions [std].** Premiums and maintenance expenses at the beginning of
  the policy month (BOM); claims and decrements at the end of the policy month (EOM).
  Annual decrement rates are converted to monthly via
  `q_m = 1 − (1 − q_annual)^(1/12)`; small frequency loadings may use the `rate/12`
  approximation, stated where used.
- **Age basis.** Age nearest birthday (ANB) **[std]**; attained age advances on policy
  anniversaries. Chosen for consistency with the CMI assured-lives table conventions
  [unverified — the convention of the restricted tables was not confirmed from a
  fetched document]; any consistent basis works if used for *all* lookups.
- **Currency.** GBP. All amounts per single policy.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  Joint life first event is a variant (two-life survivorship product) **[std scope:
  not in base]**.
- **Survival period.** 14 days [S1][std pick, see product-spec footnote 9]. In the
  accelerated base model it is cash-flow-neutral (death within 14 days of diagnosis
  pays the same `SA` as a death claim [S1]) and is ignored as a timing refinement
  **[std]**. In the standalone variant it reduces payable claims (below).
- **Rounding.** Intermediate values at full precision; displayed to pence **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `contract_type` | enum {accelerated, standalone} | accelerated |
| `issue_age` | int (ANB) | 40 |
| `sex` | enum {M, F} | M |
| `smoker` | enum {NS, S} | NS |
| `sum_assured` | currency (SA) | 100,000 **[std]** |
| `term_years` | int (5–50 [S2][S5]) | 25 **[std]** |
| `cover_basis` | enum {level} (decreasing/FIB out of scope) | level |
| `life_basis` | enum {single, joint_first_event} | single **[std]** |
| `premium_guarantee` | enum {guaranteed, reviewable} | guaranteed [S1] |
| `premium_monthly` | currency | 55.00 **[std]** (no public rate cards — placeholder) |
| `premium_mode` | enum {monthly, annual} | monthly **[std]** |
| `children_cover` | bool (automatic on the composite [S1]) | true |
| `indexation` | bool (increasing-cover option; base: false) | false **[std]** |
| `issue_date` | date | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly decrements |
| `t` / `y` / `a` | Policy month; policy year = ceil(t/12); attained age = issue_age + y − 1 (ANB) | monthly |
| `P(t)` | Premium rate in force (constant under guaranteed premiums; reset at reviews in the reviewable module) | at reviews only |
| `SA(t)` | Sum assured (constant at SA for level cover; indexation module updates annually) | on events |
| `grace_flag(t)` | In-grace indicator (60-day grace [S1][S4]) — deterministic base model does not enter grace | monthly |
| `n_AP_used` | Additional-payment claims used per condition (contract cap: 1 per condition [S11]) — not tracked in the frequency-loading approximation **[std]** | — |
| `n_child_used` | Children's claims used (cap 2 [S1]) — not tracked in the frequency-loading approximation **[std]** | — |

There is no account value, asset share, surrender value, bonus, or MVR state in this
product: lapse pays nothing [S1][S4][S5][unverified as explicit statement].

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Main benefit | SA on first of death / TI / CI diagnosis + survival (accelerated); CI only (standalone) | [S1][S4][S8][S11] |
| Additional-payment benefit `B_AP` | min(0.25 x SA, 25,000) = 25,000 at the anchor cell; non-depleting | [S1][S4][S11] |
| Children's benefit `B_ch` | min(0.50 x SA, 25,000) = 25,000 at the anchor cell; non-depleting; 2-claim policy cap | [S1] |
| Child funeral benefit | 4,000 — excluded from the base model (de minimis) | [S1]; exclusion **[std]** |
| Survival period | 14 days | [S1]; pick **[std]** |
| Premium | Level, guaranteed for the term; 60-day grace, no surrender value | [S1][S4] |
| Term / expiry | 5–50 years; policy ends by 75th birthday | [S2][S5] |

### (b) Insurer-discretionary current elements (snapshot)

Guaranteed-premium CIC has almost no discretionary machinery — there are no bonus
rates, no asset shares, no MVRs. Two snapshot elements exist:

| Input | Snapshot value | Basis |
|---|---|---|
| Reviewable-premium reviews (variant module only) | Reviews every 5 years from the 5th anniversary; changes driven by claims/industry experience, medical advances, law; Aviva: "no limits" on changes, <2% or 50p ignored; L&G intermediary: ±5% tolerance, individual health not a factor. Snapshot: premiums unchanged at each review **[std]** | [S3][S4][S5] |
| Indexation basis (if `indexation = true`) | RPI snapshot 3.0% p.a. **[std]** → cover +3.0%, premium +4.5% (x1.5 factor), within caps 10%/15% | mechanics [S1][S4]; RPI level **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

The CMI's critical illness investigation covers standalone and full accelerated
(death + CI) business, on a diagnosis-rate approach: AC04 insured-lives accelerated-CI
diagnosis-rate tables (WP50, 2003–2006 experience), cause-specific rates (WP52, updated
WP151), and CIBT93 as the population-based comparison table [R8][R9]. The current
protection base-table generation is the "16" Series (term assurance mortality and
accelerated CI, 2015–2018 experience, finalized with WP154) [REG-R26]; the latest
public experience output is WP167 (accelerated CI by cause, 2017–2020) [R9]. **Honest
flagging:** CMI working papers are public, but current CMI tables and datasets are
restricted to Authorised Users (subscribers) [REG-R22][R9 — access limits
[unverified]]; AC04/16-Series rate values were not obtained. The reference basis below
is therefore a **[std] proxy** shaped like the named tables, to be replaced by a
licensed basis in any real application.

| Input | Reference basis | Basis tags |
|---|---|---|
| CI diagnosis rates `i_ci(x)` | [std] proxy table below, shaped like an insured-lives accelerated-CI diagnosis-rate table (AC04/16-Series structure: sex/smoker-distinct, age-increasing) | structure [R8][REG-R26]; values **[std]** |
| Mortality `q_d(x)` | [std] proxy table below, shaped like ~0.70 x ONS National Life Tables qx (population mortality is heavier than insured experience; scalar and pivot values are rounded placeholders, not derived ONS data) | ONS tables redistributable [REG-R32]; values **[std]** |
| Overlap factor `k` | 0.10 flat (see combined decrement below) | **[std]** |
| Standalone survival-period slippage `δ` | 0.03 (fraction of diagnoses dying within 14 days) | **[std]** |
| Additional-payment frequency | `a(x) = 0.15 x i_ci(x)`, non-terminating | **[std]** |
| Children's-cover claim frequency | `λ_ch = 0.0004` p.a. per policy, non-terminating, while children_cover active | **[std]** |
| Lapse `w(y)` | [std] table below; no dynamic lapse in base | **[std]** |
| Mortality/morbidity improvement and CI trend `τ` | 0% p.a. in base; if an improvement overlay is required, express as "CMI_20xx with long-term rate p% [std]" | [REG-R30]; base **[std]** |
| Expenses | Initial 200 per policy; maintenance 30 p.a. inflating 3% p.a.; claim expense 250 per main claim | **[std]** |

[std] proxy diagnosis and mortality rates (annual, male non-smoker; pure placeholders
— NOT CMI or ONS values; interpolate log-linearly between pivot ages **[std]**):

| Age x | 40 | 45 | 50 | 55 | 60 | 65 |
|---|---|---|---|---|---|---|
| `i_ci(x)` | 0.0015 | 0.0025 | 0.0040 | 0.0070 | 0.0110 | 0.0170 |
| `q_d(x)` | 0.0009 | 0.0014 | 0.0022 | 0.0036 | 0.0060 | 0.0100 |

[std] lapse table (annual rates; protection-book shape, calibration to be replaced by
the user's experience — UK CI lapse studies are proprietary):

| Policy year | 1 | 2 | 3–5 | 6+ |
|---|---|---|---|---|
| `w(y)` | 10% | 8% | 6% | 4% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1..12n (n = term_years); y = ceil(t/12); a = attained age (ANB) |
| `SA` | sum assured (100,000 at the anchor cell) |
| `P` | monthly premium (55.00 **[std]** at the anchor cell) |
| `i_ci(a)` | annual CI diagnosis rate (first diagnosis of a listed condition, incl. TPD) |
| `q_d(a)` | annual best-estimate mortality rate |
| `k` | overlap: proportion of deaths that follow a CI diagnosis that already gave rise to (or would give rise to) a claim in the same year (0.10 **[std]**) |
| `q_claim(a)` | annual combined claim decrement (accelerated), defined below |
| `q_m(t)`, `w_m(t)` | monthly claim and lapse rates: `1 − (1 − annual)^(1/12)` |
| `a_m(t)` | monthly additional-payment frequency ≈ `0.15 x i_ci(a) / 12` **[std]** |
| `λ_m` | monthly children's claim frequency ≈ `λ_ch / 12` = 0.0000333 **[std]** |
| `B_AP`, `B_ch` | 25,000 and 25,000 (anchor cell; see contractual inputs) |
| `E0`, `E_m(y)`, `E_cl` | initial expense 200; maintenance `30/12 x 1.03^(y−1)` per month; claim expense 250 **[std]** |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |
| `δ` | standalone survival-period slippage (0.03 **[std]**) |
| `τ` | CI trend rate (0 in base **[std]**) |

Dimensional check: all benefit amounts are GBP; `q_m`, `w_m`, `a_m`, `λ_m` are
dimensionless monthly probabilities/frequencies; every cash-flow line below is
GBP/month per policy in force at the relevant weighting.

### Combined decrement for accelerated CI

The insured event is *death or first CI diagnosis, whichever first* — the CMI's
accelerated investigation measures exactly this combined claim incidence with
cause-of-claim splits [R8][R9]. Adding `q_d` and `i_ci` naively double-counts lives
that are both diagnosed and die in the same period: once the CI claim has been paid
(diagnosis + 14-day survival), the subsequent death of that life is not a second
claim; and a death within the survival period converts the CI claim into a death claim
of the same amount rather than adding one. The classical independent-rates
formulation is diagnosis rates plus mortality net of the overlap
[unverified as a market-practice statement — recorded as such in the research file]:

    q_claim(a) = i_ci(a) x (1 + τ)^(y−1) + q_d(a) x (1 − k)          [std]

where `k` is the proportion of deaths preceded by a claimable CI diagnosis (deaths
"already counted" in `i_ci`). **[std] simplification:** `k = 0.10`, flat across ages,
in the absence of public cause-of-death-linked CI data (the cause-specific splits in
WP52/WP151/WP167 [R8][R9] are the right calibration source for subscribers).
Sensitivity range 0–0.25 (see Key sensitivities). The 14-day survival period needs no
further adjustment in the accelerated design: whichever way the overlap resolves, `SA`
is paid once [S1].

### Standalone variant deltas

Death pays nothing; the policy simply terminates. Decrement splits into paying and
non-paying parts **[std]**:

    q_pay(a)  = i_ci(a) x (1 + τ)^(y−1) x (1 − δ)        — CI claims paid (survive 14 days)
    q_exit(a) = q_d(a) x (1 − k) + i_ci(a) x (1 + τ)^(y−1) x δ
                                                          — deaths without payment, incl.
                                                            deaths within the survival period

Total decrement `q_claim = q_pay + q_exit` (same in-force runoff as the accelerated
model at these parameters); only the *paid* part generates claim outgo. Death within
the survival period pays nothing on the composite standalone variant [S4][S11]; a
premium-refund-on-death feature exists in some designs [S4][S11 — recorded jointly in
the research file] and is excluded **[std]**.

### Monthly processing order [std]

At BOM of month t:

1. Premium income: `P x l(t−1)` (survivors at the start of the month pay).
2. Maintenance expense: `E_m(y) x l(t−1)`. (Initial expense `E0` at t = 1 only,
   weight 1.)

At EOM of month t:

3. Main claim decrement: expected claim outgo `SA x q_m(t) x l(t−1)` (accelerated;
   standalone uses `q_pay_m`), plus claim expense `E_cl x q_m(t) x l(t−1)`.
4. Additional-payment claims (non-terminating — do NOT decrement `l`):
   `B_AP x a_m(t) x l(t−1)`.
5. Children's-cover claims (non-terminating — do NOT decrement `l`):
   `B_ch x λ_m x l(t−1)`.
6. Lapse applied to non-claiming survivors; update in-force:
   `l(t) = l(t−1) x (1 − q_m(t)) x (1 − w_m(t))` **[std order: claim before lapse]**.
7. At t = 12n (term end): policy expires; no maturity or surrender value
   [S1][S4][S5].

The frequency-loading treatment of steps 4–5 deliberately ignores the contractual
claim-count caps (1 per additional-payment condition [S11]; 2 children's claims [S1])
and the per-child cross-policy cap (£50,000 [S1]): at the [std] frequencies the
probability of hitting a cap is second-order. Exact treatment would need claim-count
state variables (`n_AP_used`, `n_child_used`).

### Cash flow outputs (per policy, month t)

| Cash flow | Formula | Sign | Timing |
|---|---|---|---|
| Premium income | `P x l(t−1)` | + | BOM |
| Initial expense | `E0` at t = 1 | − | BOM |
| Maintenance expense | `E_m(y) x l(t−1)` | − | BOM |
| Main claims | `SA x q_m(t) x l(t−1)` (standalone: `q_pay_m`) | − | EOM |
| Claim expenses | `E_cl x q_m(t) x l(t−1)` | − | EOM |
| Additional-payment claims | `B_AP x a_m(t) x l(t−1)` | − | EOM |
| Children's-cover claims | `B_ch x λ_m x l(t−1)` | − | EOM |
| Surrender outgo | 0 (no surrender value [S1][S4][S5][unverified as explicit statement]) | — | — |

Grace (60 days [S1][S4]) is not separately modeled in the deterministic base: lapse
rates are assumed to already reflect grace-period cures **[std]**. Death during grace
pays the death benefit less unpaid premiums [term chassis]; immaterial at monthly
resolution **[std]**.

### Reviewable-premium module (variant)

For `premium_guarantee = reviewable`: `P(t)` is constant between reviews; at each
5-yearly review from the 5th anniversary [S3][S4], `P ← P x (1 + ρ_review)` where
`ρ_review` is a scenario input (snapshot 0 **[std]**). Contractual constraints:
Aviva-style — no limits, changes under 2% or 50p ignored, policyholder may instead
reduce cover [S4][S5]; L&G-intermediary-style — ±5% tolerance per review, individual
health not a factor [S3]. A review-driven lapse response belongs in behavior modeling
(below). Premium rates for in-force reviewable business are insurer-discretionary
current elements — class (b) snapshots, not guarantees.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; UK CI lapse experience
studies are proprietary, so shapes are stated with rationale and no source is cited
for calibration.

- **Base lapse [std].** `w(y)` per the table above, converted monthly. Rationale:
  protection lapse is duration-skewed (early years highest — buyer's remorse,
  remortgaging, distribution churn) and levels off in later durations.
- **No interest-sensitive lapse.** There is no cash value or credited rate to arbitrage;
  the interest-sensitive dynamic-lapse machinery of the accumulation products in this
  library is deliberately absent **[std]**.
- **Premium-review shock (reviewable module only) [std].**
  `w_shock = min(0.30, w(y) + 2.0 x max(0, ρ_review − 0.05))` applied in the 12 months
  following a review that raises premiums by more than 5%. Rationale: Aviva's
  unlimited review changes [S4] make review-driven shocks the dominant behavioral risk
  on reviewable business; slope and cap are placeholders.
- **Selective lapsation [std].** Optional morbidity-anti-selection overlay: after a
  lapse-shock event, remaining lives carry `i_ci x (1 + η)` with `η = 0.10`.
  Rationale: healthier lives lapse first when premiums rise; magnitude is a
  placeholder.
- **Indexation take-up (if indexed) [std].** Declining an increase 3 years in a row
  removes the option [S1][S4]; base model assumes full take-up while active.
- **GIO / life-change option exercises.** Excluded from the base model point **[std]**;
  exercise creates a new policy/increase at current rates without underwriting
  [S1][S4][S11] — an anti-selection cost that a production model should load for.

---

## Worked example

Anchor cell: male 40 non-smoker, accelerated, SA = £100,000, term 25 years, level
guaranteed premium P = £55.00/month **[std]**. Age-40 assumptions: `i_ci` = 0.0015
**[std]**, `q_d` = 0.0009 **[std]**, `k` = 0.10 **[std]**, `τ` = 0 →
`q_claim = 0.0015 + 0.0009 x 0.90 = 0.00231` annual;
`q_m = 1 − (1 − 0.00231)^(1/12) = 0.00019270`. Year-1 lapse 10% →
`w_m = 1 − 0.90^(1/12) = 0.0087416`. `a_m = 0.15 x 0.0015 / 12 = 0.00001875`;
`λ_m = 0.0004 / 12 = 0.0000333`. `B_AP = B_ch = 25,000`. Maintenance
`E_m = 30/12 = 2.50` (year 1); claim expense 250; initial expense £200 at t = 1 (not
shown in the table). Survivor factor per month:
`s = (1 − q_m)(1 − w_m) = 0.9998073 x 0.9912584 = 0.9910674`.

| Month t | l(t−1) | Premium `P·l` | Main claim `SA·q_m·l` | Claim exp `250·q_m·l` | Add-pay `B_AP·a_m·l` | Child `B_ch·λ_m·l` | Maint `E_m·l` | Net CF | l(t) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 55.00 | 19.27 | 0.05 | 0.47 | 0.83 | 2.50 | 31.88 | 0.991067 |
| 2 | 0.991067 | 54.51 | 19.10 | 0.05 | 0.46 | 0.83 | 2.48 | 31.59 | 0.982215 |
| 3 | 0.982215 | 54.02 | 18.93 | 0.05 | 0.46 | 0.82 | 2.46 | 31.31 | 0.973441 |

Trace, month 1: premium 55.00 x 1; expected main claim 100,000 x 0.00019270 = 19.27;
claim expense 250 x 0.00019270 = 0.05; additional payment 25,000 x 0.00001875 = 0.47;
children's 25,000 x 0.0000333 = 0.83; maintenance 2.50. Net = 55.00 − 23.12 = 31.88
(31.88 − 200 initial expense = −168.12 in total month-1 cash flow).
l(1) = 1 x (1 − 0.00019270) x (1 − 0.0087416) = 0.991067. Note the additional-payment
and children's rows do not enter l(t): they are non-terminating loadings
[S1][S3][S4][S8][S11].

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` and `uk/regulatory/technical-notes.md`;
this section states only what is specific to critical illness cover. [REG-R#] resolves
against the shared UK numbering, which now runs **R1–R120**, with **R50–R52, R74–R76 and
R121–R133 unused by design** (the research streams were allocated parallel blocks and the
tails left spare — an unused number is not a missing entry). Product-local [S#]/[R#] tags are
unchanged and resolve against `sources.md` in this directory.

**What "statutory accounting and capital" means in the UK.** The file names mirror
`us/regulatory/` for structural parity across the library, and nothing else: the UK has no
"statutory accounting" in the U.S. sense. There are three separate measurements over one cash
flow engine — the **Solvency UK regulatory balance sheet** (the PRA Rulebook prudential
measurement) [REG-R39][REG-R1], the **statutory accounts** (FRS 102 + FRS 103, or UK-adopted
IFRS 17) [REG-R99][REG-R105][REG-R106], and **tax**, which is not a liability measurement at
all but is computed **from the accounts** with the FA 2012 overlay [REG-R17][REG-R18]. Two
U.S. framings must not be carried across: the "acquisition costs expensed as incurred, no DAC
asset, first-year surplus strain" story is **reversed** here (SI 2008/410 Schedule 3 para 13
and FRS 103 ¶3.7 both **require** deferral) [REG-R105][REG-R99], and there is no UK analogue
of the annual statement blank — the reporting layer is the **IR./IRR. template family**
[REG-R84][REG-R89].

### Contract classification and reporting

- **Authorisation class.** Accelerated CI written with life cover falls in long-term **Class
  I**; standalone CI is typically argued into **Class IV** (permanent health) or Class I
  [REG-R14]. The retrieved RAO text names no critical illness product, so **the assignment
  itself is [unverified]** — carried forward from `product-spec.md`, "Regulatory context",
  without upgrade.
- **Line of business — a derivation, not a settled answer.** Segmentation follows the
  **nature of the risks**, and the **legal form of the obligation "is not necessarily
  determinative"** (TPFR 26.2); health obligations pursued on a similar technical basis to
  long-term insurance business go to the long-term lines (26.3) [REG-R41]. On that reading a
  UK CI lump sum is **financial compensation arising from illness** — limb (2) of the
  Glossary definition of *health insurance obligation* — hence a health obligation,
  underwritten and multi-year, hence **SLT health, line of business 29** [REG-R42][REG-R41].
  **No retrieved document states that conclusion**, and the numbered line-of-business list
  that would settle it sits in the **unretrieved Annexes to the SCR – Standard Formula Part**
  [REG-R73]; the library's applicability matrix therefore marks this product's life/health
  rows `?` [REG-R62]. Where the accelerated benefit is inseparable from the term chassis of
  `uk/products/term-assurance/`, the whole obligation follows the base contract into LoB 32
  [REG-R41].
- **PRA three-digit product codes — four of them, and the premium guarantee picks between
  them** [REG-R89]: **444** accelerated CI, guaranteed premiums (the base model point of these
  notes); **454** accelerated CI, reviewable premiums; **464 / 474** standalone CI, guaranteed
  / reviewable. So `contract_type` and `premium_guarantee` in "Model point attributes" are
  **reporting keys**, not merely assumption switches — running the reviewable module moves the
  block from code 444 to code 454. Group CI (**584**) and risk-premium CI reinsurance
  (**604**) are out of this product's scope. The code list contains **no participating CI
  code** — unlike income protection, which has 480 CWP and 481 Holloway UWP — which is
  consistent with this product having no asset share, bonus or MVR mechanics anywhere
  [S1][S4][S5][REG-R89].
- **IR.14.01 (life obligations analysis)** is the only PRA template with a product split and
  wants, per code: contracts in force and new contracts in the year, gross written premiums,
  claims paid (**including claims management expenses** — PS18/26 removes them from that
  definition from the **31 December 2026** reference date [REG-R87]), gross best estimate, and
  **capital at risk** as defined in SCR – Standard Formula 7.8 and 7.10 [REG-R89]. Two
  counting conventions bite here: rider benefits and identifiable increments count as **a
  single contract**, so the additional-payment and children's-cover benefits generate no rows
  of their own; and "in case of products unbundled, the different parts of the product shall
  be reported in different rows, using different ID codes" — which is where the
  accelerated-CI unbundling question surfaces in reporting. **Column C0030 line of business is
  a closed list the firm applies itself** (29 health insurance and 32 other life insurance
  among the options) and the code appendix states **no line of business for any of the four CI
  codes**, so two firms can legitimately report the same CI book on different rows [REG-R89].
- **IR.12.04 (best estimate assumptions) has CI rows of its own, and they are narrower than
  this model's basis** [REG-R89]. **R0450** and **R0490** carry CI claim rates for **male
  non-smoker and female non-smoker only** — there is no smoker or aggregate CI row, where
  assurance mortality has six — and **R0530** carries "critical illness change per annum" on
  the ten-year-equivalent-rate convention, which is where the trend parameter `τ` of these
  notes would be reported. The instruction is explicit that "where **accelerated** critical
  illness is the main product the basis should be the percentage of **combined** mortality and
  critical illness claims" — the template presumes exactly the combined decrement `q_claim`
  built above, and so pulls **against** unbundling. Column C0080 requires the **named
  underlying table**, the direct regulatory hook for the AC04 / "16" Series basis this library
  can only proxy [REG-R89][REG-R26][REG-R22]. **The transcribed row list carries no
  CI-specific lapse row and no CI renewal-expense unit-cost row** — the lapse rows are keyed
  to level term, decreasing term, endowment and investment bond, and the unit-cost rows to
  term assurance, investment bond and annuity — so **whether an accelerated CI book reports
  its lapses under the level-term rows is not settled by the retrieved instructions**
  [REG-R89]. The template's trigger is firm-level (gross BEL > £50 million **or** gross
  written premiums > £10 million), not per product.
- **Templates that do not reach this product.** IR.12.05 / IR.12.06 are with-profits templates
  triggered on with-profits net BEL > £500 million and never bite a non-participating CI book
  [REG-R90]; IRR.22.02 / IRR.22.03 and MALIR 1–7 are matching-adjustment returns and this
  product holds no MA portfolio [REG-R91]; the three **unit-linked-only** rows of IR.12.01
  (surrender value, nominal value of units, matching value of units) are all inapplicable
  [REG-R89]: there are no units, and the fetched policy documents describe cancellation with no
  payment other than the cooling-off refund [S1][S4][S5], so **no surrender value exists at any
  time** — **[unverified as an explicit statement; consistent with all fetched terms]**, carried
  forward from `product-spec.md` without upgrade. Whether the
  SCR underwriting disclosure runs through **IR.26.03 (life)** or **IR.26.04 (health)** follows
  the unresolved classification above and is marked `?` for this product [REG-R84][REG-R89].

### Technical provisions

- **Contract boundary — full term on both premium bases, and the reviewable case is the
  interesting one.** With guaranteed premiums (the base model point) no unilateral repricing
  right exists, so TPFR 3.3(3) never engages and every premium and benefit in the `n`-year
  term is inside the boundary [REG-R41]. With **reviewable** premiums the boundary is **still
  the full term, not the review date**: 3.3(3) excludes cover beyond a date at which the firm
  can amend premiums or benefits "so that the premiums fully reflect the risks", assessed at
  portfolio level **except** for long-term insurance business "where an individual risk
  assessment of the obligations relating to the insured person of the contract is carried out
  at the inception of the contract and that assessment cannot be repeated before amending the
  premiums or benefits" — where the test is applied **at the level of the contract**
  [REG-R41]. Individually medically-underwritten CI cannot be re-underwritten at a review, so
  the carve-out applies and the boundary runs to expiry. TPFR 3.7 makes the test harder still:
  premiums fully reflect the risks only "where there is **no circumstance** under which the
  amount of the benefits and expenses payable under the portfolio exceeds the amount of the
  premiums payable" — which even Aviva-style reviews with "no limits on how much your premium
  can change" [S4][S5] do not satisfy, since the review is periodic and the intervening
  experience is not repriceable. **Model consequence:** the reviewable module's `ρ_review`
  path and the review-shock lapse response sit **inside** the boundary and must be projected,
  not truncated. TPFR 23.1 then requires reinsurance recoverables to be calculated
  **consistently with the boundaries of the underlying contracts**, so a reviewable-rate CI
  treaty inherits the full-term boundary of the direct business [REG-R41] — material here
  because UK protection is heavily reinsured.
- **Cash flows in scope, and two that this model does not yet produce.** TPFR 13.1 requires
  eight separately identifiable streams [REG-R41]. Stream (5), **payments between the firm and
  intermediaries**, makes **commission and clawback an in-scope best-estimate cash flow**, not
  an expense-loading convention — and the expense set in "Assumption inputs" (`E0` = 200
  initial, `E_m` = 30 p.a. inflating 3%, `E_cl` = 250 per main claim, all **[std]**) carries
  **no commission line at all**. That gap must be closed before this projection can feed
  either a best estimate or the accounts DAC test below. Stream (8) is **policyholder-charged
  tax only**; because the representative design is post-2012 protection taxed on trade profits
  (see "Statutory accounts and tax"), stream (8) is normally nil here — a derivation from
  TPFR 13.1(8) and LAM01080, not a quoted rule [REG-R41][REG-R18]. Shareholder corporation tax
  is **not** a best-estimate cash flow; it enters through deferred tax under Valuation 11
  [REG-R39].
- **Expenses, on two bases.** TPFR 16.1 names administrative, investment management, claims
  management and **acquisition** expenses, each including allocated overheads, and **TPFR 16.4
  requires expenses to be projected on the assumption that the firm will write new business in
  the future** — so `E_m` is a **going-concern unit cost**, not a run-off unit cost with
  overheads re-spread over a shrinking book [REG-R41]. The risk margin's reference undertaking
  assumes the opposite (TP 4B.1(5), no new obligations) [REG-R1], and **no retrieved source
  explains how to reconcile the two**, so the model carries two expense bases. Nothing in the
  rules prescribes an inflation index or rate: the 3% p.a. here is **[std]**.
- **The best estimate is routinely negative, and nothing floors it.** For CI on guaranteed
  level premiums inside a full-term boundary, the present value of future premiums exceeds the
  present value of future claims and expenses at issue, so the best estimate is negative — the
  library records this product as `x` on the "negative best estimate permitted" row
  [REG-R41][REG-R115]. There is no floor: TP 3.1 contains none, TP 2.2 requires a **transfer
  value** which is legitimately negative for a profitable portfolio, the risk margin is
  non-negative by construction so it offsets but does not floor, the Solvency I floor
  (INSPRU 1.2.62R) was expressly **not** carried over to Solvency II firms [REG-R115], and the
  reporting layer treats surrender value as a **disclosure item** rather than a constraint
  [REG-R89]; a secondary source states "there is no floor related to the surrender value
  specified in the rules" [REG-R118]. **On this product the surrender-value limb of that
  discussion is vacuous on the [unverified] no-surrender-value reading recorded above** — so the
  absence of a floor is not a modelling choice to be made but a fact to be carried: the
  unfloored sign must survive every aggregation, and the accounts floor is applied downstream
  only (see "Statutory accounts and tax"). One design-specific check on magnitude: the
  additional-payment and children's-cover benefits are **non-terminating** outgo [S1][S4][S11]
  — they add claim cost without shortening the premium stream, so they reduce the magnitude of
  the negative best estimate rather than reverse its sign at the anchor cell **[std, derived
  from the cash flow table above]**.
- **Options and guarantees — real, but none of them financial.** TP 9.2(1) requires the value
  of financial guarantees and contractual options to be taken into account, and TPFR 19.4–19.5
  force a scenario-dependent method where the present value depends on expected future
  outcomes and on deviation from them [REG-R1][REG-R41]. The library marks
  **stochastic valuation `—` for this product**: a level-premium CI contract with no surrender
  value — on the [unverified] reading above — and no financial option has no scenario-dependent
  asymmetry [REG-R41]. The options
  this design actually contains are **biometric or continuity** options — indexation
  (increasing cover), the guaranteed insurability / life-change option capped at the lower of
  100% of original cover and £200,000, TPD dropping off at age 70 with a premium reduction,
  and, where elected, waiver of premium [S1][S4][S11] — plus the reviewable-premium repricing
  right. TPFR 3.2 puts obligations relating to **unilateral rights of the firm to renew or
  extend** inside the contract [REG-R41], and the first two are separately exposed to the
  **lapse module as continuity options** (see "SCR" below). None of them requires a stochastic
  valuation; all of them require a take-up assumption.
- **Policyholder behaviour cannot be a flat table on the reviewable variant.** TPFR 11.1
  requires an analysis of past behaviour and a prospective assessment, and closes: "The
  likelihood shall only be considered to be independent of the elements referred to in (1) to
  (4) where there is **empirical evidence** to support such an assumption" [REG-R41]. For
  guaranteed-premium CI with no surrender value — again on the [unverified] reading above —
  independence of moneyness and management
  action is comparatively easy to sustain and the flat `w(y)` table above is defensible
  **[std]**. For the **reviewable** module it is not: the premium-review shock and selective
  lapsation overlays in "Policyholder behavior modeling" are what TPFR 11.1 requires, not an
  optional refinement.
- **The matching adjustment is unavailable, and now for cited reasons.** MA 2.2 requires the
  portfolio to have **no future premium payments** and confines the connected underwriting
  risks to longevity, expense, revision, mortality or recovery time risk; a regular-premium CI
  contract fails the first condition outright, and diagnosis/morbidity risk is not in the list
  [REG-R2]. The **eligible-element** route (MA 1.2, with the no-future-premiums condition
  disapplied by 2.5 for the in-payment limb) names only the guaranteed element of a
  with-profits immediate or deferred annuity and the **in-payment element of a group
  death-in-service dependants' annuity or an income protection policy** — a CI lump sum is
  neither [REG-R2] — and SS7/18 states the recovery-time permission is **not** intended to
  admit any liability type other than IP claims in payment [REG-R8]. This grounds the note
  previously carried in these notes that the matching adjustment "is in practice irrelevant to
  CI term business" [R7][unverified]: the conclusion stands and now rests on the MA Part's own
  eligibility conditions rather than on market practice.
- **Discounting.** The basic GBP risk-free curve, **published monthly by the PRA** and not
  computed by the firm [REG-R44][REG-R54][REG-R55]; **no curve value, ultimate forward rate,
  fundamental spread or volatility adjustment appears anywhere in this library** because the
  four monthly technical-information spreadsheets were not opened [REG-R54]. The GBP last
  liquid point is **50 years** on the 2025 assessment effective 1 January 2026 [REG-R56], so
  extrapolation barely touches a term of at most 50 years and the curve is observed over
  essentially the whole liability. The volatility adjustment is permission-dependent
  [REG-R1]. **TMTP and TMIR are marked `—` for this product**, but that is a materiality
  judgement about the size of pre-2016 CI blocks, **recorded as [unverified] and not upgraded**
  — legal availability of the TMTP turns only on qualifying-obligation status at the relevant
  date [REG-R3][REG-R57].

### The risk margin

- **Parameters and effective date, unchanged from the pointer list this section replaces.**
  Cost-of-capital method at **CoC = 4%** with a tapering factor **λ = 0.9** for long-term
  obligations, floored at **0.25**, in force from 31 December 2023 under SI 2023/1346
  [R7][REG-R1][REG-R4]. The formula, its discounting convention and the currency rule (the
  **basic** curve in the currency of the firm's **financial statements**) are in
  `uk/regulatory/technical-notes.md`, "The risk margin".
- **What is product-specific is the shape of `SCR(t)`, not the formula.** The reference
  undertaking's notional SCR captures underwriting risk on the transferred business, market
  risk **other than interest rate risk** where material, credit risk on reinsurance and
  related exposures, and operational risk — and nothing else; it applies **none of** the MA,
  the VA, the risk-free transitional or the TMTP, and carries **no loss-absorbing capacity of
  deferred taxes** [REG-R1]. For a CI portfolio, whose assets are a small backing portfolio
  against a liability that is negative at issue, that leaves the run-off driven almost
  entirely by the biometric, expense, lapse and counterparty legs.
- **A best-estimate-driven `SCR(t)` proxy does not work on this product.** The best estimate
  starts negative, crosses zero as level premiums pre-fund the steepening `i_ci` curve, and
  returns to zero at expiry, while the stress base rises with attained age — so a driver-based
  run-off keyed to the best estimate has a **driver that changes sign** and is unusable
  **[std, architectural — derived from the decrement basis above]**. There is no UK fallback:
  the Delegated Regulation's simplification hierarchy (Article 58) was **not restated** into
  Solvency UK, leaving only TPFR 27 proportionality and an unexercised PRA power in IRPR
  regulation 7C [REG-R41][REG-R49][REG-R44]. **No rule text sanctions any specific proxy.**
- **Sign discipline in reporting.** Because the risk margin is non-negative and the best
  estimate is negative, technical provisions for this product can be positive while the best
  estimate is negative. The two are reported **separately** in IR.12.01 and described
  separately in SFCR section D.2, which also requires a description of the level of
  uncertainty and an explanation of material differences from the financial-statements basis —
  on this product that difference is largely the accounts floor [REG-R1][REG-R89][REG-R84].

### SCR — the modules that bite

**Which underwriting module applies is the open question, so a CI model must be able to run
both branches.** SCR-SF 3.2A routes non-life obligations other than health to the non-life
module, **life obligations other than health obligations** to the life module, and **health
obligations to the health module** — the health module is not a residual, it **takes
precedence** [REG-R62]. On the derivation recorded above this product is a health obligation
and lands in the **SLT health** branch; where an accelerated contract is not unbundled it
follows the term chassis into the **life** module. TPFR 26.7 requires a contract combining
health and other obligations to be unbundled "**where possible**", and because the accelerated
benefit pays **once**, on the earlier of death and diagnosis, the two legs are not additive and
unbundling is not obviously possible; **the sources give no bright-line test**
[REG-R41][REG-R62]. Neither branch is asserted here.

| Sub-module | SLT health branch [REG-R62] | Life branch [REG-R62] | Bites this product? |
|---|---|---|---|
| Mortality | `3C9.1` **+15%** | `3B1.1` **+15%** | Yes on the **accelerated** death leg. Both carry the "only where TP without risk margin increases" filter, and on the **standalone** variant higher mortality removes lives before diagnosis and so *reduces* provisions, which the filter excludes **[derived from the filter, not a quoted conclusion]** |
| Longevity | `3C10.1` **−20%** | `3B2.1` **−20%** | No — deferring a claim on a fixed-term contract does not increase provisions |
| Disability-morbidity | `3C11.1` = medical-expense + **income-protection** charges; `3C13.1` **+35%** next 12 months, **+25%** thereafter, **−20%** recovery rates *where those rates are lower than 50%*, **+20%** persistency rates *where equal to or lower than 50%* | `3B3.1` **+35%** / **+25%** / **−20%** recovery, with **no TP-increase filter and no persistency limb** | **Yes — this is the dominant charge.** The two conditional limbs of `3C13.1` are **vacuous** on a lump-sum CI contract, which has no recovery and no persistency rates, so only the inception limbs bite |
| Expense | `3C14.1` **+10%** on amounts **and +1 percentage point** on expense inflation | `3B4.1` identical | Yes |
| Revision | `3C15.1` **+4%**, triggers include **inflation** | `3B5.1` **+3%**, no inflation trigger | No — this design pays lump sums, not annuity benefits |
| Lapse | `3C16` — up **×1.5** (capped at 100%), down **×0.5** (capped at 20 percentage points), **40% mass**; **no 70% limb anywhere in the health module** | `3B6` — same three, plus a **70%** mass limb confined to **RAO class VII** business [REG-R64] | Yes; see the direction discussion below. The 70% limb never reaches this product |
| Catastrophe | `3C17`–`3C20`: mass accident, accident concentration (**workers' compensation and group IP only**), pandemic | `3B7.1` **+0.15 percentage points** added to the mortality rates used for the following 12 months — an *absolute* addition, one year only | Life catastrophe bites the death leg; health mass accident and pandemic reach all health obligations other than workers' compensation, accident concentration does not reach individual business |

**The health catastrophe sub-modules cannot be computed from this library's material, and one
of them may not even be defined for this product.** `SCR_healthCAT` aggregates mass accident,
accident concentration and pandemic **without correlation**, and every input ratio sits in
**Annex XVI, which no stream retrieved** [REG-R62][REG-R73]. The pandemic leg is
`L_p = 0.000075 × E + 0.4 × Σ_c (N_c × M_c)` — the two factors are verified from the rule —
where `E` is the exposure measured on benefits payable "**in case of permanent work disability
caused by an infectious disease**" [REG-R62]. A CI contract pays on **diagnosis of a listed
condition**, and reaches permanent work disability only through its TPD definition (own
occupation before 70, or 3 of 6 Specified Work Tasks) [S1]; **what `E` is for a lump-sum CI
book is not stated by any retrieved source.**

**The lapse stress: run all three, and let the sign of the best estimate pick the direction.**
`3C16.1` / `3B6.1` take the **highest** of up, down and mass. The directional filters are the
whole point: the **up** scenario applies **only to relevant options for which exercise would
*increase* technical provisions without the risk margin**, the **down** scenario **only where
exercise would *decrease* them**, and the **40% mass** limb carries the same increase filter
[REG-R62]. Applied to this design, which on that same [unverified] reading has **no surrender
value**, exercising the option takes the policy's liability to zero:

- Where the cell's best estimate is **negative** — the position at issue and through the early
  durations [REG-R41][REG-R115] — discontinuance moves the liability **up** to zero, i.e.
  **increases** technical provisions, so the cell is filtered **into** lapse-up and into the
  40% mass limb.
- Where the best estimate has turned **positive** — the middle durations, where the level
  premium has pre-funded the steep part of the `i_ci` curve — discontinuance **releases** it,
  so the same policy is filtered **into** lapse-down and **out of** the mass-lapse charge.
- The filter is therefore evaluated **per policy** (or per TPFR 20 group), and **a single CI
  book straddles both scenarios**. Do not apply one direction to the whole product.

**A divergence inside this library, recorded rather than resolved.** The applicability matrix
in `uk/regulatory/statutory-accounting-and-capital.md` marks this product **lapse up `x`,
lapse down `(x)`, mass lapse `x`**, while the note attached to that matrix extends the
"lapse-supported cells are stressed by lapse **down**" reading to "profitable protection early
in its life" [REG-R62]. The two readings are not reconciled in the retrieved material and are
not reconciled here. What is not in doubt: all three scenarios must be run, the filter is
evaluated on the sign of technical provisions **without the risk margin**, and where the
highest gross requirement and the highest **net** requirement rest on different scenarios the
charge is the one whose scenario produces the highest **net** requirement — **the selection is
made on the net run and the reported gross number follows it** (`3C16.9` / `3B6.9`)
[REG-R62].

**The continuity options are inside the lapse module, and this model switches them off.**
"Relevant options" are not only the termination-side rights: `3C16.4` / `3B6.4(2)` include all
rights to **establish, renew, increase, extend or resume** cover, and for those **the change in
the option exercise rate is applied to the rate reflecting that the option is NOT exercised**
[REG-R62]. So the **indexation (increasing cover) option** and the **guaranteed insurability /
life-change option** [S1][S4][S11] are stressed inside `3C16` / `3B6`, even though the base
model point above sets `indexation = false` and excludes GIO exercises **[std]**. A model that
cannot vary a take-up rate for those two options cannot compute the lapse sub-module on this
product. Conversely, `SCR-SF 1.2` defines **discontinuance** to include making a contract
**paid-up**, and `3C16.8` / `3B6.8` require the **worst discontinuance type per policy**
[REG-R62]; this product has no paid-up option and, on the [unverified] reading above, no
surrender value, so that maximum collapses to **lapse without value** — the one place where the
absence of contractual optionality simplifies rather than complicates the calculation.

**Which stresses need a full revaluation.** Every biometric, expense and lapse scenario above
requires the liability model to be **re-run end to end** under a changed assumption set
[REG-R62]. Three universal scenario rules bind each run: the scenario is assumed **not** to
change the risk margin, deferred taxes or future discretionary benefits and **no management
actions are taken** in the gross run (`3.3A(1)`); simplifications are permitted unless the
error could influence the user, **unless the simplification produces a higher SCR**
(`3.3A(3)`); and **where a scenario would increase basic own funds the requirement is zero** —
every scenario-based sub-module is **floored at zero** (`3.3A(5)`) [REG-R62].

**Market and other modules.**

- **Interest rate `3D5` / `3D6`** — run twice, revaluing assets **and** the best estimate, the
  charge being the higher direction [REG-R62]. On the liability leg alone, the **up** scenario
  is the adverse direction for a cell with a **negative** best estimate: the negative liability
  shrinks toward zero. That is the opposite of the intuition carried over from a book with
  positive reserves, and it is **derived from the sign of the best estimate, not a quoted
  rule**. The top-level market correlation coefficient `A` is **0** where the up scenario bites
  and **0.5** otherwise [REG-R62].
- **Counterparty default type 1 `3E13`** is the dominant market-side charge for UK protection,
  because CI is heavily reinsured [REG-R62]. It sits alongside the **TPFR 24.4 floor**, the
  only hard numeric floor in the technical-provisions apparatus: the average loss on
  reinsurance default "must not be assessed at lower than **50% of the amounts recoverable** …
  unless there is a reliable basis for another assessment", with **what counts as a reliable
  basis unsettled** [REG-R41]. The PRA's expectations are in SS20/16, **retrieved only as a
  landing page and with its title differing between two retrieved sources** [REG-R120].
- **Operational risk** is `min(0.3 × BSCR; Op) + 0.25 × Exp_ul` with
  `Op = max(Op_premiums; Op_provisions)`, `Op_premiums` at **4%** of non-unit-linked life
  earned premium plus a growth surcharge at the same rate on the excess over **1.2×** the
  preceding 12 months, and `Op_provisions` at **0.45%** of `max(0; TP_life − TP_life-ul)`, with
  those technical provisions **excluding the risk margin and gross of reinsurance**
  [REG-R62]. Two consequences for a high-premium, negative-reserve product: it contributes
  fully to `Op_premiums` (and a fast-growing CI book picks up the growth surcharge) while
  **reducing** the provisions base, which is itself floored at zero — so the charge is
  premium-driven **[derived from the formula, not a quoted conclusion]**. The `0.25 × Exp_ul`
  leg is nil: no unit-linked business.
- **`Adj_TP` is zero and one run suffices.** This product carries **no future discretionary
  benefits**, so `BSCR = nBSCR` and the loss-absorbing capacity of technical provisions is nil
  [REG-R62]. **`Adj_DT` still applies**: the change in deferred taxes from an instantaneous
  loss of `BSCR + Adj_TP + SCR_operational`, with **no benefit taken for an increase in
  deferred tax assets** — the transitional permitting otherwise is printed as running to
  **30 December 2025** and **no PRA instrument confirming its expiry or extension was
  retrieved** [REG-R62].
- **Modules that expressly do not reach this product** [REG-R62][REG-R64][REG-R65]: equity and
  property (and the symmetric adjustment) on the liability side; **spread on a matching
  adjustment portfolio `3D25`**, there being no MA portfolio; the **70% mass-lapse limb**,
  confined to RAO class VII (pension fund management) business by the 20 December 2024
  correction — note that **PS15/24 ¶¶6.16 and 6.18 remain published and unamended**, so anyone
  reading PS15/24 alone gets the wrong scope [REG-R64]; **health revision `3C15`**, no annuity
  benefits; **health catastrophe accident concentration `3C19`**, workers' compensation and
  group income protection only; the **NSLT** premium-and-reserve factor formula, which would
  apply only if the contract were written on a general-insurance technical basis (marked `?`);
  and **undertaking-specific parameters**, whose replaceable-parameter list is exhaustive and
  reaches no mortality, morbidity, lapse, expense or catastrophe parameter [REG-R65].

### Own funds, ring-fenced funds and the MCR

- **No ring-fenced fund, no surplus funds, no estate.** The representative design is written in
  the shareholder fund; there is no participating form (and the PRA code list has no
  participating CI code) [S1][S4][S5][REG-R89]. So SCR-SF Chapter 9's per-perimeter notional
  SCRs, the loss of diversification between perimeters, the Own Funds 3L deduction and the
  Surplus Funds Part all pass this product by [REG-R62][REG-R77][REG-R45].
- **The negative best estimate lands directly in Tier 1 unrestricted.** It flows into the
  **reconciliation reserve**, which "may be positive or negative" (Own Funds 3C.2) and which a
  firm is **not required** to look through for the Tier 1 features (3C.3) [REG-R77]. That is
  the mechanism by which a CI valuation assumption reaches the highest tier of regulatory
  capital, and it is why the assumption governance in "Key sensitivities and model risks"
  below is a capital control, not documentation.
- **EPIFP is gone, and its absence matters more here than on most products.** There is no EPIFP
  rule in the Own Funds Part, and the PRA amended the template instructions to confirm the
  requirement is **removed from all reporting, including disclosure** [REG-R77][REG-R86]. The
  expected profit in future premiums is precisely what makes a CI best estimate negative; the
  economics survive inside the reconciliation reserve, but **a UK CI model does not produce the
  EPIFP decomposition an EU model still needs**.
- **MCR.** `MCR = max(MCR_combined, AMCR)` with
  `MCR_combined = min(max(MCR_linear, 0.25 × SCR), 0.45 × SCR)`, and the absolute floor for
  long-term insurance is **£3,500,000** at entity level [REG-R78]. This product contributes two
  linear terms: `TP_l4` (all other long-term obligations, net of reinsurance, **without the
  risk margin** and **floored at zero term by term**) and **capital at risk**. Two
  product-specific consequences. First, a negative CI best estimate contributes **zero**, not a
  negative amount, to `TP_l4`, because the floor is applied term by term. Second, capital at
  risk is defined per contract as the amount the firm would currently pay **on death or
  disability** plus the expected present value of further amounts payable on immediate death or
  disability, **less** the best estimate of the corresponding obligations, **floored at zero per
  contract**; what the deducted best estimate *is* decides the sign of the gap to the sum
  assured, and the rule does not say. On the **whole-contract** reading — the deduction is the
  contract's own best estimate, negative here because future premiums are inside the boundary —
  that quantity **exceeds** the sum assured and, for the accelerated design, `CAR ≈ SA − BEL` per
  contract. On the narrower **benefit-obligation** reading — the deduction is the best estimate
  of the death/CI benefit outgo alone, a positive present value — it sits just **below** the sum
  assured. The library takes both readings in different places and says so: the term-assurance
  MCR bullet works the whole-contract reading, while the worked example in
  `uk/regulatory/technical-notes.md` adopts the benefit-obligation reading. **No retrieved source
  resolves the fork; it is recorded, not resolved**
  **[std, reading of MCR 3C.1(5)]**. The pure-protection worked example in
  `uk/regulatory/technical-notes.md`, "Worked example — one policy, carried through", applies the
  same rule to a three-year term assurance; read its `CAR` figure against whichever reading is
  adopted. For the **standalone** variant the sum assured is payable on **diagnosis**, not on
  death or disability, and **no retrieved source addresses whether such a lump sum enters the
  "death or disability" limb at all**; the research records the parallel unresolved question for
  an income-protection income stream and this library does not fill either hole [REG-R78]. The
  two product-specific consequences above together defeat the folk rule for the **accelerated**
  design: `TP_l4` is floored to zero while `CAR` — which enters at a coefficient of `0.0007` —
  stays at or near the full sum assured on either reading above, so `MCR_linear` can exceed
  `0.25 × SCR` and **the linear formula, not the collar, may bind** — the collar binds only
  where `SCR > 0.0028 × CAR`, and the term-assurance worked
  example cited above runs below that threshold, with the linear limb winning. Check which limb
  of `min(max(MCR_linear, 0.25 × SCR), 0.45 × SCR)` binds rather than assuming the collar, and
  check both against the **£3,500,000** absolute floor [REG-R78 3.1A, 3.1B, 3C.1]. The general
  observation that `MCR_linear` for a mixed UK life book sits far below 25% of the SCR, so that
  the MCR is normally the **25% collar** [REG-R78], does not carry over to a book concentrated in
  this product; and for the **standalone** variant the size of the `CAR` limb is the unresolved
  question above, so which limb binds cannot be stated either way.

### Statutory accounts and tax

- **UK GAAP: FRS 103 applies, and fixes less than a U.S. reader expects.** The library marks
  FRS 103 insurance-contract scope `x` for this product [REG-R99]; the significant-insurance-
  risk test itself (**FRS 103 Appendix II, not read** [REG-R99]) is not in issue for a contract
  whose only benefits are contingent on death, terminal illness or diagnosis, with no
  investment element to unbundle [S1][S4][S11]. Measurement is entity-specific and largely
  **grandfathered**: FRS 103 permits continuation of practices that could not be newly
  introduced, including **undiscounted** measurement of insurance liabilities (¶2.6), permits
  but does not require the elimination of excessive prudence (¶2.7), and names the **modified
  statutory solvency basis** as the established treatment for long-term business (¶3.11)
  [REG-R99]. The ¶3.10 prohibition on deferring acquisition costs applies to **with-profits
  funds** and does not reach this product [REG-R99].
- **DAC — the U.S. contrast, reversed, and the single most important accounts fact about this
  product.** SI 2008/410 Schedule 3 **para 13** requires acquisition costs incurred in one
  financial year but relating to a subsequent one to be **deferred**, with the asset at
  balance-sheet item **G.II** and its movement at technical account item **8(b)**
  [REG-R105]; FRS 103 **¶3.7** says acquisition costs "**shall be deferred**", subject to the
  three carve-outs (already recovered, insufficient net present value of margins, insufficiently
  certain future premiums or margins), and **¶3.9** requires amortisation over no longer than
  the recoverability period **and in a similar profile to those margins**, with no basis
  prescribed [REG-R99]. **So there is no first-year statutory-accounts surplus strain of the
  U.S. kind on this product.** The note 17 carve-out is a modelling fork that must be an
  explicit configuration: DAC is excluded to the extent the long-term business provision (item
  **C.2**) already allows for the costs, explicitly or through anticipation of future income
  [REG-R105]. On the Solvency UK ledger there is **no DAC at all** — acquisition expense is a
  projected cash outflow inside the best estimate (TPFR 16.1(4)) and the Valuation Part
  recognises no unamortised expense asset (Val 8.1) [REG-R41][REG-R39]. Note the practical
  limit of these notes: `E0` = 200 **[std]** carries no commission, so the DAC asset cannot be
  built from this projection as it stands (see "Technical provisions", stream (5)).
- **The floor, and the largest divergence between the two ledgers on this product.** FRS 103
  implementation guidance **IG2.41**: "no policy may have an overall negative provision except
  as allowed by PRA rules, nor a provision less than any guaranteed surrender or transfer
  value" [REG-R100]. On the [unverified] reading above this product has **no surrender value**,
  and **no transfer value is recorded in any fetched document** [S1][S4][S5][unverified], so the
  second limb is vacuous and what bites is the **non-negative** limb: the
  accounts carry a provision floored at zero on business whose Solvency UK best estimate is
  negative. The **liability adequacy test** (¶¶2.14–2.18) is the only UK GAAP measurement
  floor, requires current estimates of all contractual and related cash flows **including
  embedded options and guarantees**, and sends **the entire deficiency to profit or loss** —
  and it is the mechanism through which CI trend or definition-drift deterioration first
  reaches reported profit, including by writing off the DAC asset [REG-R99]. (**FRS 103 ¶2.16
  tail and ¶¶2.17–2.18 were read only in part** [REG-R99].)
- **IFRS 17, where adopted: the general measurement model.** The UKEB's stated expectation is
  the **VFA for unit-linked and with-profits contracts** and the **PAA for short-term
  contracts**, leaving the **GMM for protection business** — which is what this contract is
  [REG-R106]. The PAA is not available on the base model point: coverage runs 5–50 years
  [S2][S5] and the PAA requires either a reasonable approximation to the GMM or a coverage
  period of one year or less [REG-R106]. Acquisition cash flows sit **inside the fulfilment
  cash flows** and **reduce the CSM at initial recognition** rather than appearing as an
  asset — a third pattern, distinct from both the U.S. no-DAC strain and the UK GAAP deferral
  [REG-R106]. **Annual cohorts** and the onerousness split are set at initial recognition and
  **never reassessed**, so a **reviewable-premium** CI group that turns onerous after a review
  cannot be re-grouped: a **loss component** is recognised instead [REG-R106]. **IFRS 17 itself
  is paywalled and was never read by this library; every paragraph reference is one the UKEB
  quotes, and no confidence level, coverage-unit formula or transition proxy is stated anywhere
  here** [REG-R107][REG-R106].
- **Tax: non-BLAGAB, trade profits — with a date test, not a product test.** Protection business
  written from **1 January 2013** is excluded from BLAGAB and taxed on a trading basis; policies
  written **before** that date continue to be taxed as BLAGAB unless an election is made
  [REG-R18 LAM01080][REG-R17]. The base model point, a new issue, is therefore **non-BLAGAB
  trade profit** — as recorded in `product-spec.md`, "Regulatory context" [REG-R17] — but a real
  CI back-book straddles the date, so the model must carry a **BLAGAB / non-BLAGAB tag keyed on
  the date the policy was written**, and the FA 2012 s.73 six-step I-E computation, the
  policyholders'-rate charge and the minimum profits test are reached **only** by the legacy
  cell [REG-R17][REG-R18]. The seven-year spread of BLAGAB acquisition expenses (s.79) is
  **repealed for accounting periods beginning on or after 1 January 2023**, with legacy sevenths
  still running and any deduction for pre-2023 acquisition costs recognised in a post-2023
  income statement **still disallowed** — again, legacy cell only [REG-R18 LAM04130][REG-R109].
- **Deferred tax exists twice, on two different models.** FRS 102 Section 29 recognises deferred
  tax on **timing differences** [REG-R102]; Valuation 11 recognises it on **all** assets and
  liabilities **including technical provisions**, measured as the difference between the
  Solvency UK value and the tax value [REG-R39]. On this product the two are structurally
  different numbers: a negative Solvency UK best estimate against an accounts provision floored
  at zero produces a deferred tax **liability** on the prudential balance sheet with no
  counterpart in the accounts **[derived from Val 11 and IG2.41, not a quoted rule]**, and it is
  that balance the `Adj_DT` re-run stresses [REG-R62]. A model that projects deferred tax
  carries **three liability measures per period — accounts, tax and Solvency UK — not two**.
- **Distributable profits come off the prudential balance sheet.** CA 2006 s.830(3) makes the
  distribution test subject to **s.833A** for an authorised insurer carrying on long-term
  business: realised profit is **A − L − D** on the **prudential** values, capped by s.833A(3)
  at accumulated profits (realised or not) less accumulated losses [REG-R104]. With no
  ring-fenced fund and no MA portfolio, the `D` deduction list is empty for this product — so a
  UK distributable-earnings pattern for a CI block is a projection of the **Solvency UK**
  balance sheet subject to an **accounts-based cap**, not a projection of the accounts.
- **Policyholder-level tax stays in the product spec.** Qualifying-policy status under
  para 19(3) Schedule 15 ICTA 1988, and the L&G retail wording's bar on issue or assignment into
  trust, are contractual facts recorded in `product-spec.md`, "Regulatory context" [S1]; they do
  not enter the projection.

### Traps peculiar to this product

1. **Carrying the U.S. "no DAC, first-year strain" story across.** It reverses: company law and
   FRS 103 both **require** deferral, and the strain exception is scoped to with-profits funds,
   which this product is not [REG-R105][REG-R99].
2. **Flooring the best estimate because there is no surrender value.** Backwards. The absence of
   a surrender value — **[unverified as an explicit statement; consistent with all fetched
   terms]**, per the flag above — is exactly what leaves the negative best estimate unconstrained
   on the Solvency UK ledger; the floor lives on the **accounts** ledger and is applied there
   [REG-R41][REG-R115][REG-R100]. A real contract that *did* carry a surrender value would invert
   this conclusion, so the premise must be re-verified against the actual policy terms before the
   trap is relied on.
3. **Cutting the reviewable-premium boundary at the review date.** TPFR 3.3(3)'s contract-level
   carve-out for individually-underwritten long-term business keeps the boundary at full term
   [REG-R41] — and switching to the reviewable module also changes the **PRA product code**
   (444 → 454), not just an assumption [REG-R89].
4. **Applying one lapse direction to the whole book.** The `3C16.2` / `3C16.3` (and `3B6.2` /
   `3B6.3`) filters are evaluated per policy on the sign of technical provisions without the
   risk margin, a CI book straddles both, and the scenario **selection is made on the net run**
   [REG-R62]. The library's own matrix and its accompanying note pull in different directions on
   this product, and that divergence is recorded above, not resolved.
5. **Forgetting that indexation and the GIO are lapse-module inputs.** Continuity options are
   "relevant options", and the stress is applied to the rate reflecting that the option is
   **not** exercised [REG-R62], while the base model point above switches both off **[std]**.
6. **Reading IR.12.04's combined-claims instruction as settling the SCR treatment.** The
   template presumes a combined mortality-and-CI basis for accelerated business [REG-R89]; the
   module allocation is unresolved and TPFR 26.7 requires unbundling "where possible"
   [REG-R41][REG-R62][REG-R73]. The reporting layer and the capital layer pull in opposite
   directions, and unbundling would additionally buy the 0.25 Life/Health diversification credit
   at BSCR level that leaving the contract whole does not **[derived from the top-level
   correlation matrix, not a quoted conclusion]** [REG-R62].
7. **Attempting the health catastrophe sub-modules from this library's material.** Not possible:
   **Annex XVI was not retrieved** [REG-R73], and the pandemic exposure `E` is defined on
   permanent work disability, which this contract reaches only through its TPD definition
   [REG-R62][S1].
8. **Putting the claim expense in the wrong template cell.** `E_cl` **[std]** sits inside claims
   paid for IR.14.01 C0070 until the **31 December 2026** reference date and outside it
   afterwards [REG-R87][REG-R89].
9. **Letting a [std] proxy basis reach IR.12.04.** Column C0080 requires a **named** underlying
   table; the proxy `i_ci` and `q_d` tables above are not table names, and the CMI tables that
   would be are subscriber-restricted [REG-R89][REG-R22][REG-R26].
10. **Producing an EPIFP figure.** It has been removed from Solvency UK reporting and disclosure
    altogether; a document describing an EPIFP disclosure is describing the EU regime
    [REG-R86][REG-R77].

## Valuation and reserve pointers

This library projects **gross best-estimate liability cash flows**. The Solvency UK
measurement, the reporting templates, the SCR sub-modules, the accounts and the tax basis
for this product are in **Statutory accounting and capital** above; this section stays a
pointer list for the layers that consume those flows:

- **Solvency UK.** Technical provisions = best estimate + risk margin (Technical
  Provisions 2.4); best estimate = probability-weighted cash flows discounted on the
  relevant risk-free term structure, gross of reinsurance, on realistic assumptions,
  segmented into homogeneous risk groups (3.1–3.2, 9.1–9.2, 10.1) [R7][REG-R1]. Risk
  margin: cost-of-capital method, CoC 4%, λ = 0.9 taper with floor 0.25 [R7][REG-R4].
  Lapse and surrender assumptions must be realistic and reflect dependence on future
  conditions (9.1–9.2) [R7]. The matching adjustment sits in its own Rulebook Part [R7];
  why it is unavailable to this product, and the earlier [unverified] note that it is "in
  practice irrelevant to CI term business", are in **Statutory accounting and capital**
  above, "Technical provisions".
- **The statutory accounts and tax are separate measurements**, from Solvency UK and from
  each other: FRS 102 + FRS 103 (or UK-adopted IFRS 17) for the accounts [REG-R99], and a
  trade-profit computation built on the accounts for tax [REG-R17]. The two facts that most
  change how this projection is consumed — the **FRS 103 ¶3.7 / Schedule 3 para 13 DAC
  requirement** and the **UK GAAP non-negative floor** on a business whose Solvency UK best
  estimate is negative — are in **Statutory accounting and capital** above
  [REG-R105][REG-R100].
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) [REG-R38] measures these
  contracts under the **general measurement model** as fulfilment cash flows plus CSM
  [REG-R106]; the standard itself was never read by this library [REG-R107], so the earlier
  "[mechanics summary: unverified]" caveat stands for anything not sourced to the UKEB. The
  expected-cash-flow engine is the same projection, with regime-specific discounting, risk
  adjustment and aggregation.
- **Professional standards.** TAS 100 v2.0 applies to all technical actuarial work
  from 1 July 2023 [R10][REG-R33]; TAS 200 v2.0 (insurance) applies from 1 January
  2025 [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order:

1. **CI trend and condition-definition drift.** The dominant assumption risk for CI
   business: diagnosis rates trend with medical practice (earlier and wider
   diagnosis), and the covered event itself moves when the ABI revises model
   definitions — the 2021/22 review broadened Alzheimer's to all dementia, tightened
   cancer staging exclusions, and excluded myocardial injury from heart attack, with
   compliance by 31 January 2024 [R2][R3]; prior reviews 2011, 2014, 2018 [R3].
   Definition changes produce *step* changes in `i_ci` that no trend parameter
   anticipates; sensitivity-test `τ` at ±2% p.a. **[std]** and re-map the incidence
   basis at each definition-review generation.
2. **Level and shape of the diagnosis-rate proxy.** `i_ci` here is a [std] placeholder
   because AC04/16-Series values are subscriber-restricted [REG-R22][REG-R26];
   miscalibration scales claims one-for-one. WP167 also flags COVID-affected 2020
   experience [R9].
3. **Overlap factor `k`.** Bounds: assuming `k = 0` maximally double-counts
   (overstates combined incidence by the true overlap x `q_d` per year); `k = 0.25`
   may understate. Calibrate
   from cause-of-claim data (WP52/WP151/WP167 lineage) where licensed [R8][R9].
4. **Lapse.** With level guaranteed premiums against steeply age-increasing `i_ci`,
   early durations pre-fund later ones: higher-than-assumed late-duration lapses
   release liability, lower ones extend exposure to the steep part of the incidence
   curve; the BEL is not monotone in a single lapse scalar. Lapse assumptions must be
   realistic and condition-dependent under the Rulebook (9.1–9.2) [R7].
5. **Expenses and expense inflation.** Second-order next to (1)–(4) on this
   mono-benefit product **[std]** placeholders throughout.
6. **Guaranteed vs reviewable premiums.** The base model's premiums are guaranteed —
   morbidity deterioration cannot be repriced, so items (1)–(3) fall entirely on the
   insurer. The reviewable module transfers trend risk to policyholders at the cost of
   review-shock lapse and selective lapsation (anti-selection multiplier `η`)
   [S3][S4][S5].

Known modeling pitfalls:

- **Double counting death and CI.** Summing `q_d + i_ci` without the overlap term
  overstates accelerated claim incidence; conversely, applying `k` to the standalone
  *paid* decrement (instead of to the non-paying death exit) understates claims.
- **Survival-period misapplication.** Applying the 14-day survival reduction `δ` to
  the accelerated main benefit is wrong — death within the survival period still pays
  `SA` as a death claim [S1]; `δ` bites only in the standalone variant [S4][S11].
- **Depleting the sum assured for partial claims.** Additional-payment and children's
  claims must not reduce `SA` or decrement `l(t)` [S1][S3][S4][S8][S11]; modeling
  them as accelerations (Vitality-style plan-account depletion [S10]) is a different
  product.
- **Terminating on additional-payment claims.** Same error, opposite sign: only the
  main benefit ends the policy [S1][S4][S11].
- **Age-basis mismatch.** `i_ci`, `q_d` and attained-age indexing must share the ANB
  **[std]** basis.
- **Proxy-basis leakage.** The [std] proxy rates in these notes are placeholders and
  must not be presented as CMI or ONS values; production work replaces them with a
  licensed basis and documents the substitution (TAS 100 data/assumption
  requirements [R10][REG-R33]).
- **Premium placeholder.** £55/month is not a market rate (no insurer publishes CI
  rate cards — research-file gap); profitability conclusions from the worked example
  are meaningless. Aviva's reviewable reviews have "no limits" [S4] — do not model
  reviewable business with the guaranteed-premium constraint.
