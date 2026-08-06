# Pension Annuity — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md`, numbering carried from `uk/_research/pension-annuity.md`; [REG-R#] tags
refer to the cross-product reference library
`uk/references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `uk/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation. Parameter values are
identical to those in `product-spec.md`; the mechanics anchor is the L&G Pension
Annuity [S1][S2].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (annuity instalments
  to annuitant and dependant, guarantee-period payments, value-protection lump sums,
  maintenance expenses) for a single pension annuity in payment. Discounting, the
  matching adjustment and reserves are not computed (see Valuation and reserve
  pointers).
- **Mortality is the model.** The contract has no premiums after outset [S2 §1.1], no
  surrender value [S2 §12][S5 cl.14.7], no account value and no policyholder options
  after the cancellation window [S1 p4]. The only decrements are deaths; the only
  stochastic drivers are longevity and (for indexed options) inflation. This is the
  design property that makes the liability MA-eligible [R1].
- **Projection frequency.** Monthly grid, t = 1, 2, ... months from the start date
  **[std]**. Payment dates fall on the grid per the frequency m; exact-day mechanics
  (Just's first-of-month payments and stub proportioning [S5 §§5.2–5.3], L&G's
  working-day adjustment [S2 §2.4]) are not modeled **[std]**.
- **Timing conventions [std].** Escalation is applied at the start of the month
  containing the policy anniversary (first at t = 13) [S2 §3.3]. Advance instalments
  are paid at the start of a payment period and require survival at the start;
  arrears instalments at the end, requiring survival at the payment date. Deaths are
  decremented at end of month; a death in month t means the life does not receive an
  arrears payment due at the end of month t **[std convention]**.
- **Age basis.** Age last birthday (ALB) **[std]**, chosen to index the [std] ONS
  life-table proxy by single year of age [R13]; the ONS convention itself is
  [unverified]. Annual rates convert monthly as q_m = 1 − (1 − q_x)^(1/12) **[std]**.
- **Limiting age.** ω = 115 **[std]**: the [std] base table is extended beyond its
  maximum tabulated age by log-linear extrapolation of qx, capped at 1 at ω.
- **Currency and model points.** GBP throughout [S2 §1.3]. Single-policy model
  points, projected on an expected (probability-weighted) basis: survival
  probabilities multiply scheduled per-policy cash flows. No aggregation logic is
  specified here.
- **Joint-life independence.** Annuitant and dependant mortality are independent
  **[std]** (common-shock/"broken-heart" dependence is a documented model risk).

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `purchase_price` P | currency | 100,000 [S1 p11] |
| `annuitant_age` x_a | int (ALB) | 65 [S1 p11] |
| `annuitant_sex` | enum {M, F} | M **[std]** |
| `rating_multiplier` θ_a | float ≥ 1 (1 = standard; enhanced overlay) | 1.0 **[std]** |
| `dependant_present` | bool | true |
| `dependant_age` x_d | int (ALB) | 62 **[std]** |
| `dependant_sex` | enum {M, F} | F **[std]** |
| `dependant_pct` δ | float ≤ 1 [S1 p9] | 0.50 **[std]** |
| `overlap` | bool (with/without overlap [S2 §§5.9–5.11]) | false **[std]** |
| `annual_income` A(1) | currency p.a. | 5,400 **[std]** (see Worked example) |
| `frequency` m | enum {12, 4, 2, 1} [S2 §2.2] | 4 |
| `timing` | enum {advance, arrears} [S2 §2.3] | arrears |
| `proportion` | bool (arrears only [S2 §4]) | false |
| `escalation_type` | enum {level, fixed, rpi_catchup, lpi5} (spec menu) | fixed |
| `escalation_rate` g | float ≤ 0.10 [S2 §3.2] | 0.03 **[std]** |
| `guarantee_months` n | int, 12–360, 0 if none [S1 p10]; XOR with VP [S2 §§6.7, 7.6] | 0 |
| `vp_pct` v | float ≤ 1 [S1 p11]; v + δ ≤ 1 on first-death basis [S2 §7.3] | 0.50 **[std]** |
| `vp_basis` | enum {first_death, last_survivor} [S2 §7.3] | first_death |

The premium P is the amount applied to the annuity after PCLS and adviser charges
[S1 p4]; PCLS itself is pre-purchase and outside the model. A(1) is a pricing input:
no insurer publishes a rate card, so A(1) is taken from a quote or calibrated to the
anchor (£100,000 at 65 buying £6,657 p.a. with 50% VP, January 2026 [S1 p11]; the
illustration's frequency/timing/escalation basis is not recorded).

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `A(y)` | Annualized income in policy year y (annuitant scale) | anniversaries |
| `peak` | Running peak of the RPI reference index (catch-up state) | anniversaries (rpi_catchup only) |
| `G(t)` | Cumulative gross instalments scheduled through month t | payment dates |
| `l_a(t)` | Annuitant survival probability to end of month t; l_a(0) = 1 | monthly |
| `l_d(t)` | Dependant survival probability to end of month t; l_d(0) = 1 | monthly |
| `d_a(t)` | Probability annuitant dies in month t = l_a(t−1) − l_a(t) | monthly |
| `n_rem(t)` | Remaining guarantee months = max(0, n − t) | monthly |
| `VPbal(t)` | Value-protection balance = max(0, v × P − G(t)) | payment dates |

Because instalments while the annuitant is alive are deterministic given the
escalation path, G(t) and VPbal(t) are deterministic schedules in a deterministic
projection — the expected VP outgo needs no path simulation (see recursions).

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Instalment amount | A(y)/m at each payment date | [S1 p8][S2 §2.2] |
| Escalation rule | per `escalation_type`: fixed g ≤ 10%; RPI 0-floor with catch-up (12 months ending six months before the anniversary); LPI = RPI capped 5%, floor 0, September year | [S2 §3.2, §3.3, defs]; LPI floor harmonization **[std]** (spec footnote 5) |
| Dependant's income | δ × income, same escalation basis; % of the higher of income at death and at guarantee end | [S2 §§5.12–5.13] |
| Overlap rule | with: dependant stream runs during remaining guarantee; without: starts at guarantee end | [S2 §§5.9–5.11] |
| Guarantee period | n months of instalments certain, escalation continuing as if alive | [S2 §§6.5–6.6][S7 §4.2] |
| Value protection | max(0, v × P − G(death)) on the chosen basis; v + δ ≤ 1 (first-death) | [S1 p11][S2 §7, §7.3] |
| Surrender value | none, at any time | [S1 p4][S2 §12][S5 cl.14.7] |
| Charges to policyholder | none (priced into the rate) | [S1 p6] |

### (b) Insurer-discretionary current elements

**None post-purchase.** The contract is non-participating [S7 §7.9] with all options
fixed at outset [S1 p4]: there are no bonus rates, no reviewable premiums, no market
value reductions, and no discretionary charges — class (b) is empty for this product.
The only insurer-discretionary quantity is the annuity rate at purchase (pricing, not
an in-force element); its snapshot is the January 2026 anchor quote [S1 p11], and
day-to-day rate setting is not publicly documented [unverified].

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base annuitant mortality | Proper bases: SAPS S3/S4 pensioner tables (S4 released February 2024, graduated on 2014–2019 data) [R10][R11] or the insured-annuitant PMA16/PFA16 family [REG-R27]. Both are restricted to CMI Authorised Users [R11][REG-R22], so the reference basis is a **[std]** proxy: latest ONS UK national life table qx by age/sex [R13] × annuitant adjustment α = 0.80 | [R10][R11][R13][REG-R22][REG-R27]; α **[std]** (i) |
| Mortality improvements | CMI Mortality Projections Model, cited by name/version: CMI_2024 (WP201, June 2025, calibrated to E&W data to 31 Dec 2024) [R12]; current version CMI_2025 (WP211, March 2026) [REG-R30]. Model software restricted; reference fallback is a **[std]** deterministic scale: 1.25% p.a. reduction in qx for ages ≤ 90, tapering linearly to 0% at age 110, applied from the base table's data mid-year | [R12][REG-R30]; scale **[std]** (ii) |
| Enhanced/impaired rating | Overlay on qx: q_rated = min(1, θ_a × q_base), θ_a ≥ 1 (equivalently a rated-age offset); standard life θ = 1.0 | existence [S1 p5][S4][S6][S9]; overlay **[std]** (iii) |
| Lapse / surrender | None — no surrender value exists | [S1 p4][S2 §12][S5 cl.14.7][R1] |
| Maintenance expense | £30 per policy per annum, payable monthly while any payment obligation remains, inflating at the RPI assumption | **[std]** (iv) |
| RPI inflation (for indexed options) | 3.0% p.a. deterministic | **[std]** (v) |

(i) The SAPS table naming convention (e.g. S3PMA/S3PFA) is [unverified — not stated
on the fetched page] [R10]. ONS national life tables are period tables of population
mortality, freely downloadable and updated annually (latest release dated 10 December
2025 per the fetched dataset page) [R13]; population mortality is heavier than
annuitant experience, hence the α < 1 adjustment. α = 0.80 is a shape-level
placeholder, not calibrated to any published annuitant-vs-population comparison — a
production basis must license CMI tables [R11][REG-R22].
(ii) CMI_2025 projects improvements converging to a user-chosen long-term rate with
no default recommendation [REG-R30 detail marked unverified in the reference
library]; the [std] flat-then-taper scale exists only so the reference implementation
is runnable without CMI access, and materially understates the age–period–cohort
structure of the real model [R12].
(iii) Insurers' rating structures (postcode, condition-specific factors [S1 p5][S9])
are not public; the multiplier form is the simplest overlay that reprices longevity
without touching contract mechanics.
(iv) No insurer publishes expense assumptions (charges are priced into the rate
[S1 p6]); £30 p.a. is a round placeholder for in-payment administration. Acquisition
cost is out of scope (single-premium, priced-in).
(v) Deterministic RPI cannot value the RPI floor, the catch-up ratchet, or the LPI
cap — all inflation options. See Key sensitivities.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | month index from start date, t = 1, 2, ...; policy year y = ceil(t/12) |
| m | payments per year (12/4/2/1); payment months T = {12k/m : k = 1, 2, ...} (arrears) or {12k/m : k = 0, 1, ...} mapped to the start of month 12k/m + 1 (advance) |
| A(y) | annualized income in policy year y; inst(t) = A(y(t))/m for t ∈ T |
| g | fixed escalation rate (0.03 **[std]**, ≤ 0.10 [S2 §3.2]) |
| I(k), peak | RPI reference index at anniversary k and its running maximum (catch-up state) [S2 defs] |
| δ | dependant's percentage (0.50 **[std]**, ≤ 1 [S1 p9]) |
| n | guarantee period in months (0 or 12–360 [S1 p10]) |
| v | value-protection percentage (0.50 **[std]**, ≤ 1 [S1 p11]); v + δ ≤ 1 on first-death basis [S2 §7.3] |
| P | purchase price (100,000 [S1 p11]) |
| G(t) | cumulative gross instalments scheduled through month t |
| q_a(t), q_d(t) | monthly mortality of annuitant/dependant (rated, improved) |
| l_a(t), l_d(t) | survival probabilities from outset; d_a(t) = l_a(t−1) − l_a(t) |
| w(t) | dependant-stream availability: 1 if overlap or t > n, else 0 [S2 §§5.9–5.11] |
| c_e, π | maintenance expense p.a. (30 **[std]**) and expense/RPI inflation (0.03 **[std]**) |

Dimensional check: A(y) is currency per annum; inst = A/m is currency per payment;
G, P, VP lump sums are currency; q, l, δ, v, w are dimensionless. Every cash flow
below is currency per month.

### Escalation update (start of month 12(y−1)+1, y ≥ 2) [S2 §3.3]

    level:        A(y) = A(y−1)
    fixed:        A(y) = A(y−1) × (1 + g)
    lpi5:         A(y) = A(y−1) × (1 + min(0.05, max(0, rpi_Sep(y−1))))      [S2 §3.2, defs; floor [S5 §7.1.4][S9 §4.3]]
    rpi_catchup:  see pseudocode                                              [S2 defs]

RPI catch-up pseudocode (path-dependent ratchet [S2 defs]; Aviva operates the same
rule [S9]):

    # I[k] = RPI reference level for anniversary k
    # (index for the 12 months ending six months before the anniversary [S2 defs])
    peak = I[0]                      # reference level at outset
    for k = 1, 2, ...:               # k-th anniversary
        if I[k] > peak:
            A = A * (I[k] / peak)    # increase by the excess over the prior peak
            peak = I[k]
        # else: A unchanged (income frozen until the index exceeds its peak)

Equivalently A(y) = A(1) × max(I(0..y−1)) / I(0): income is indexed to the running
peak of the reference index. Under the deterministic RPI assumption (3.0% **[std]**)
the index is monotone and the ratchet never binds, so rpi_catchup degenerates to
fixed-3%; the ratchet has value only under stochastic inflation (see sensitivities).

### Scheduled payment schedule (per policy, before survival weighting)

At each payment month t ∈ T: scheduled annuitant instalment inst(t) = A(y(t))/m;
scheduled dependant instalment δ × inst(t). Update G(t) = G(t−) + (instalments
scheduled at t). The dependant's amount uses δ × the income "as if alive" A(y(t)):
this implements the contractual "% of the higher of income at death and income at
guarantee end" [S2 §5.12] exactly, because under the (non-decreasing **[std]** menu)
escalation options the as-if-alive income path is monotone, so the higher-of base
plus same-basis escalation [S2 §5.13] reproduces δ × A(y(t)) at every later date.

### Expected cash flows (month t)

**Annuity outgo** (annuitant stream with its guarantee floor, plus dependant stream),
for t ∈ T (arrears; for advance replace l(t) with l(t−1) **[std]**):

    E[ANN(t)] = inst(t) × max(1{t ≤ n}, l_a(t))                — certain during guarantee [S2 §6]
              + inst(t) × δ × (1 − l_a(t)) × l_d(t) × w(t)     — dependant stream [S2 §5]

The first term pays the full instalment regardless of survival while the guarantee
runs (annuity-certain floor [S2 §§6.5–6.6][S7 §4.2]) and l_a(t) × inst(t) thereafter.
The second term pays the dependant when the annuitant is dead and the dependant
alive, gated by w(t): with overlap both streams run during the remaining guarantee;
without overlap the dependant stream starts at guarantee end [S2 §§5.9–5.11].
(Guarantee and VP never coexist in the representative design: n > 0 ⇒ v = 0
[S2 §§6.7, 7.6].)

**Proportionate final payment** (arrears with proportion only [S2 §4]): for a death
in month t, the accrued stub to the next scheduled instalment is approximated as

    E[PROP(t)] = d_a(t) × (h(t) + 0.5) / (12/m) × inst(next(t))   **[std half-month accrual]**

where h(t) is the number of complete months since the last payment date. Without
proportion (representative default) this term is zero and nothing is paid for the
final partial period [S2 §4].

**Value protection** (first-death basis; n = 0):

    E[VP(t)] = d_a(t) × VPbal(t−1),   VPbal(t) = max(0, v × P − G(t))   [S1 p11][S2 §7]

G accumulates gross instalments scheduled while the annuitant is alive; measuring
the balance at t−1 implements "instalments already paid" for a mid-month death
**[std discretization]**. On the last-survivor basis, replace d_a(t) with the density
of the last death, d_last(t) = d(l_a + l_d − l_a l_d)(t), and let G accumulate the
dependant's instalments too [S2 §7.3][S5 §8.4]. (The Canada Life variant additionally
nets guarantee payments due, excluding future RPI/LPI increases [S7 §4.3] —
implementable by extending G with guarantee outflows.)

**Maintenance expense**:

    E[EXP(t)] = (c_e / 12) × (1 + π)^(y−1) × IF(t)                       **[std]**
    IF(t) = min(1, max(1{t ≤ n}, l_a(t)) + 1{δ>0} × (1 − l_a(t)) × l_d(t))

IF(t) is the probability any payment obligation remains (guarantee certain, annuitant
alive, or dependant stream in payment) **[std]**.

**Total gross liability cash flow**: CF(t) = E[ANN(t)] + E[PROP(t)] + E[VP(t)] +
E[EXP(t)]. There is no premium income (single premium at t = 0 is a pricing input,
not projected [S2 §1.1]) and no surrender outgo [S2 §12].

### Mortality construction

    q_base(x, s)   = ONS qx by age/sex [R13] × α,  α = 0.80              **[std]** (proxy for SAPS S4 [R10][R11] / PMA16-PFA16 [REG-R27])
    q_imp(x, c)    = q_base(x) × (1 − f(x))^(c − c_0)                    **[std]** improvement fallback (f = 1.25% p.a. ages ≤ 90, linear taper to 0 at 110; c_0 = base-table data mid-year; production: CMI_2025 with a chosen long-term rate [R12][REG-R30])
    q_rated(x, c)  = min(1, θ × q_imp(x, c))                             **[std]** enhancement overlay
    q_m            = 1 − (1 − q_rated)^(1/12)                            **[std]**
    l(t)           = l(t−1) × (1 − q_m(t)),  separately for annuitant (θ_a) and dependant (θ_d)

### Monthly processing order

1. If t starts a policy year (t = 12(y−1)+1, y ≥ 2): apply the escalation update
   (including catch-up state) [S2 §3.3].
2. If t ∈ T: record scheduled instalments; update G(t).
3. Decrement mortality: update l_a(t), l_d(t), d_a(t).
4. Compute expected payment flows E[ANN(t)], E[PROP(t)] using survival to the
   payment point (arrears: end of month t, i.e. l(t); advance: end of month t−1,
   i.e. l(t−1)) **[std]**.
5. Compute E[VP(t)] from d_a(t) and VPbal(t−1); update VPbal(t).
6. Accrue E[EXP(t)].
7. Stop when IF(t) < 10^-6, or when every in-scope life has passed the limiting age
   (t/12 + x_a > ω and, if a dependant is present, t/12 + x_d > ω), ω = 115 **[std]**
   — stopping on the annuitant's age alone would truncate a younger dependant's tail.

---

## Policyholder behavior modeling

There is none to model, and this is a cited product feature, not an omission: after
the 30-day cancellation window the policyholder holds no options — no surrender or
transfer [S1 p4][S2 §12][S5 cl.14.7][S7 §7.5][S9 §3.9], no alteration of options
[S1 p4][S4][S6][S9], and no premium flexibility [S2 §1.1]. Consequently the model has
**no lapse decrement and no dynamic behavior formulas**; the MA eligibility conditions
effectively require this shape (no policyholder options beyond a bounded surrender
option) [R1].

Behavior enters only at outset, outside the projection, as basis-selection effects
**[std]** to consider when calibrating mortality:

- **Annuitization anti-selection.** Since the 2015 pension freedoms annuitization is
  optional [R6], so voluntary annuitants self-select for longevity — a reason
  annuitant bases sit below population mortality (the direction of α < 1 **[std]**).
- **Enhanced-annuity selection.** Whole-market enhanced quoting is mandated at the
  point of sale [R5]; lives remaining on standard terms are healthier on average.
  The reference model carries this through θ, not through behavior dynamics.
- **Cancellation window.** The 30-day cooling-off [S1 p7][S2 §13] is ignored
  (projection starts from a completed purchase) **[std]**.

---

## Worked example

Configuration (the worked model point; parameters as in `product-spec.md`):
P = £100,000 [S1 p11]; annuitant male 65, dependant female 62 **[std]**; quarterly
(m = 4) in arrears, without proportion [S2 §§2.2–2.3, 4]; fixed escalation g = 3%
**[std]**; dependant δ = 50% **[std]**; value protection v = 50% on the annuitant's
(first) death **[std]** — v + δ = 100%, exactly at the contractual bound [S2 §7.3];
no guarantee period (XOR rule [S2 §§6.7, 7.6]). Starting income A(1) = £5,400 p.a.
**[std]** — an illustrative quote level (no public rate card exists; the cited anchor,
£6,657 p.a., is for a 50%-VP basis whose escalation/frequency basis is not recorded
[S1 p11], and an escalating joint-life basis starts lower than a level one for the
same premium [S1 p8][S4][S6]). Scenario: the annuitant dies in month 17; the
dependant survives throughout. All amounts in GBP.

Instalments: year 1: 5,400/4 = 1,350.00 per quarter; year 2 (from t = 13):
A(2) = 5,400 × 1.03 = 5,562.00, so 1,390.50 per quarter. Dependant income after
death: δ × A(2) = 2,781.00 p.a. = 695.25 per quarter, first paid at the next
scheduled payment date after death (t = 18) **[std convention]**.

| t (month) | Event | Annuitant CF | Dependant CF | VP lump sum | G(t) |
|---|---|---|---|---|---|
| 3 | Q1 instalment (arrears) | 1,350.00 | — | — | 1,350.00 |
| 6 | Q2 instalment | 1,350.00 | — | — | 2,700.00 |
| 9 | Q3 instalment | 1,350.00 | — | — | 4,050.00 |
| 12 | Q4 instalment | 1,350.00 | — | — | 5,400.00 |
| 13 | Anniversary: A ← 5,400 × 1.03 = 5,562.00 | — | — | — | 5,400.00 |
| 15 | Q5 instalment | 1,390.50 | — | — | 6,790.50 |
| 17 | Annuitant dies. VP = max(0, 0.50 × 100,000 − 6,790.50) | — | — | 43,209.50 | 6,790.50 |
| 18 | Q6 date: no annuitant payment (arrears, without proportion [S2 §4]); dependant stream starts | 0.00 | 695.25 | — | 7,485.75 |
| 21 | Q7 instalment (dependant) | — | 695.25 | — | 8,181.00 |
| 24 | Q8 instalment (dependant) | — | 695.25 | — | 8,876.25 |

Checks. VP balance at death uses instalments paid before death: G(16) = 6,790.50, so
the lump sum is 50,000 − 6,790.50 = 43,209.50 [S1 p11][S2 §7]. Had "with proportion"
been chosen, a stub of ≈ (1 + 0.5)/3 × 1,390.50 = 695.25 would be paid for the
accrued month-and-a-half since t = 15 (**[std]** half-month accrual; Just would net
this stub off the VP fund-value formula [S5 §8.3]). The dependant's 695.25 continues
for her life, escalating 3% at each anniversary on the same basis [S2 §§5.12–5.13].

Guarantee/VP interaction. Had the model point instead carried a 10-year guarantee
**[std default]** and no VP (the XOR rule forbids both [S2 §§6.7, 7.6]), the death in
month 17 would change nothing until month 120: instalments of 1,390.50, escalating 3%
each anniversary as if the annuitant were alive [S7 §4.2], continue to beneficiaries
through t = 120 (annuity-certain floor), and — without overlap — the dependant's
695.25-style stream would begin only from the first payment date after t = 120, at
δ × the income at the end of the guarantee period [S2 §§5.9–5.12]. With overlap, the
dependant's stream would run from t = 18 alongside the guarantee payments
[S2 §§5.9–5.11]. In expectation these scenario flows are reproduced by the E[ANN(t)]
formula with n = 120 and w(t) as defined.

---

## Statutory accounting and capital

The framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` (what each item is and why it
exists) and `uk/regulatory/technical-notes.md` (how to compute it); this section
states only what is specific to the pension annuity and points at those files by
section name rather than restating them. **"Statutory accounting" is a U.S. term with
no UK equivalent** — the file names in `uk/regulatory/` mirror `us/regulatory/` for
structural parity across the library and nothing else. What this product sits on is
three separate measurements: the **Solvency UK regulatory balance sheet** (PRA
Rulebook — Valuation, Technical Provisions, Matching Adjustment, SCR, Own Funds and
MCR Parts) [REG-R39][REG-R1][REG-R41][REG-R2][REG-R62][REG-R77][REG-R78]; the
**statutory accounts** (Companies Act accounts under FRS 102 + FRS 103, or
UK-adopted IFRS 17) [REG-R103][REG-R105][REG-R99][REG-R106]; and **tax**, which is
not a liability measurement at all but a computation built on the accounts with the
Finance Act 2012 overlay [REG-R17][REG-R18].

[REG-R#] resolves against the shared UK numbering in
`uk/references/regulatory-and-actuarial-references.md`, which now runs **R1–R120**,
with **R50–R52, R74–R76 and R121–R133 unused by design** (the research streams were
allocated parallel blocks and the tails left spare — an unused number is not a
missing entry). Product-local [S#] and [R#] tags continue to resolve against
`sources.md` in this directory. The reference page's "Scope note on capital", which
recorded the SCR and MCR as cited-not-specified, is superseded by `uk/regulatory/`.

### Contract classification and reporting

- **Long-term insurance Class I, and that fixes one thing only.** The contract is
  Class I (life and annuity) under RAO 2001 Schedule 1 Part II [REG-R14][R8] — which
  matters here mainly for what it excludes: the **70% mass-lapse limb reaches RAO
  class VII (pension fund management) business only**, so it can never touch this
  product [REG-R62][REG-R64].
- **Line of business is decided by the technical basis, not the product label.**
  TPFR 26.2 states that the legal form of the obligation "is not necessarily
  determinative" [REG-R41]; on the segmentation this library uses, a non-profit
  pension annuity sits in **Annex 1 LoB 32, other long-term insurance business**,
  while the participating form would sit in **LoB 30, insurance with profit
  participation**. **That mapping is a drafter's inference from TPFR 26.2, 26.3 and
  the Annex 1 definitions — Annex 1 names no products — and is carried
  [unverified]** [REG-R41].
- **PRA three-digit product codes for IR.14.01** [REG-R89]: the representative design
  reports under **724** (individual pension annuity, non-profit). The
  medically-underwritten variant, which these notes model as a rating overlay θ on qx
  rather than as a structural variant (Assumption inputs (c), note (iii)), has its
  **own code 734** (individual enhanced pension annuity, non-profit) — so a modelling
  simplification and a reporting split disagree, and the model point needs the code as
  an attribute. **720** (with-profits) and **722** (unit-linked) cover forms outside
  the representative non-participating design [S7 §7.9]; **754** (bulk purchase
  pension annuity) is out of this library's scope, as are 700/704 purchased life
  annuity and 710/714 individual deferred annuity.
- **An RPI- or LPI-escalating annuity is not index-linked business for reporting.**
  The IR.14.01 appendix defines IL as covering policies linked to a stock market index
  or specific securities and states that it "excludes RPI / CPI linked policies"
  [REG-R89] — so every escalation option in the spec menu [S1 p8][S2 §3.2] still
  reports as non-profit business under 724 (or 734), and indexation never makes the
  contract linked business for reporting purposes.
- **Templates this product drives.** IR.12.01 (life technical provisions) carries it
  in the **life annuities** column, which the instruction defines as annuities and
  deferred annuities that would fall in the "other life insurance" line — annuities
  get a reporting column of their own even though they are not a separate line of
  business [REG-R89]. The **unit-linked-only rows of IR.12.01** (surrender value,
  nominal value of units, matching value of units) are inert here: there are no units
  and the surrender value is nil at all times [S1 p4][S2 §12][S5 cl.14.7]. The
  **with-profits templates IR.12.05 and IR.12.06** bite only the participating form
  (code 720) written inside a with-profits fund, and only where the firm's
  with-profits net BEL exceeds **£500 million** [REG-R90] — inert for the
  representative design.
- **IR.12.04 rows that are this product's own** [REG-R89], where the firm's gross BEL
  for long-term business exceeds **£50 million** or gross written premiums exceed
  **£10 million**: **R0290 / R0330** individual pension annuitant mortality, male and
  female, expressly **"for standard lives (i.e. not enhanced / impaired annuities)"**;
  **R0370 / R0410** the bulk equivalents; **R1410 / R1450** the complete expectation
  of life for a male aged 65 without and with improvements, labelled "for pension
  annuities" (R1650 / R1690 female 65); and **R2050** the per-policy renewal
  management expense unit cost "for pension annuities in payment" — the row the [std]
  £30 p.a. maintenance assumption would populate. C0080 requires the **named
  underlying table** with the CMI projection parameterisation in CMI notation, against
  five years of the firm's own experience with a credibility guideline of **200 claims
  per annum** per line. Two consequences bite this library directly: **the [std] ONS ×
  α proxy cannot honestly fill C0080**, because the tables a UK annuity writer would
  name are CMI Authorised-User material [R10][R11][REG-R22][REG-R27][REG-R30]; and
  **the retrieved instruction does not say where enhanced or impaired annuitant
  mortality is reported**, R0290/R0330 being restricted to standard lives.
- **The matching adjustment reporting set is the product's largest reporting burden**
  [REG-R91]. **MALIR 3** requires, per MA portfolio, **monthly gross liability cash
  flows out to month 600** in four streams — level or fixed-escalation claims,
  inflation-linked claims, expenses, and other — with the portion beyond year 50
  discounted back to the month-600 row at the basic risk-free rate, plus each stream's
  present value on the basic curve and on basic + MA. **IRR.22.02** requires annual
  liability outflows, expense outflows and de-risked asset cash flows with positive and
  negative undiscounted mismatches reported **separately and never netted**.
  **IRR.22.03** requires both annual effective rates, the MA in basis points, the
  **mortality-stress result for MA eligibility (R0070)**, the best estimate of
  obligations that depend on inflation (R0100) and a **Macaulay-equivalent liability
  duration** (R0170). Submission is no later than **130 business days** after the
  firm's financial year end [REG-R84], at an effective date of **31 December**
  regardless of when that year end falls [REG-R91].
- **What the retrieved instructions do not settle.** **MALIR 4–7 were read only at
  title level, and MALIR 5 contains the quantitative matching tests this product's
  model must pass — the single largest unread block in the reporting research**
  [REG-R91]. **PS18/26 replaces MALIR with a new MA template set moving to XBRL from
  the 31 December 2026 reference date, and removes claims management expenses from the
  IR.14.01 claims-paid definition from the same date; the replacement instruction files
  were not retrieved** [REG-R87]. Whether Solvency UK collects a life best-estimate
  cash-flow projection template at all is **an unresolved conflict**: PS3/24 ¶4.70
  states that S.13.01 "will continue to be collected", yet the final Reporting Part
  contains no IR.13.01 and the PRA's instruction library contains no such file
  [REG-R86][REG-R84][REG-R88] — for this product MALIR 3 is, on the retrieved
  material, the only cash-flow projection actually filed. IR.05.10's scope test is
  stated inconsistently between the Rulebook and the instruction file and is likewise
  unresolved [REG-R84][REG-R90]; where it applies, this product's premiums report in
  its **annuities** row (R0640) and its own-funds generation row carries the
  instruction that "annuity writers are expected to include earning the non-illiquid
  portion of its assets' total spread" [REG-R90].

### Technical provisions

- **The contract boundary is the whole contract, and nothing cuts it.** The single
  premium is already paid and no money can be added afterwards [S2 §1.1][S7 §7.3], so
  there are no future premiums for TPFR 3.3 or 3.5 to exclude [REG-R41]. The
  **contract-level repricing carve-out in TPFR 3.3(3)** — the rule that decides where
  a reviewable-premium protection contract's boundary stops — has nothing to operate
  on here: the annuity rate is fixed at outset and every option is immutable after the
  30-day cancellation window [S1 p4][S2 §13][S4]. The insurer's only right to change
  the income is the **mis-statement remedy**, which can *reduce* income (not below the
  standard rate) and reclaim overpayments where medical or lifestyle information is not
  confirmed [S1 p4] — a downward correction right, not a repricing right, and not a
  boundary trigger. The boundary flag must still be produced with the limb that
  produced it, per the shared model-output contract, rather than stored as a product
  constant [REG-R41].
- **Cash flows in scope, against the eight TPFR 13.1 streams** [REG-R41]. Benefits:
  annuitant instalments, the dependant's income, guarantee-period instalments and
  value-protection lump sums — the `CF(t)` vector these notes already build. Expenses:
  the maintenance stream. **Premiums: none inside the boundary.** Payments to and from
  **intermediaries** are an in-scope best-estimate cash flow in general, but for this
  product adviser charges are deducted from the purchase price at outset and commission
  is priced into the annuity rate [S1 p6][S1 p12][S4][S6][S9], so nothing falls inside
  the boundary. Payments to and from **investment firms** for linked benefits: none.
  **Policyholder-charged taxation: none** — this is pension business, the annuitant's
  PAYE liability is the annuitant's and no fund tax enters the projection
  [REG-R17][REG-R18][S1 p5][S2 §8]. (The applicability matrix marks that row `—` for
  this product where the technical-provisions research stream had marked it `(x)`;
  **the divergence is recorded, not resolved** [REG-R41][REG-R18].)
- **Expenses, and the tension the model cannot dissolve.** TPFR 16.1 names four
  categories, each including allocated overheads, and **TPFR 16.4 requires expenses to
  be projected on the assumption that the firm will write new business in the future**
  — so the [std] £30 p.a. maintenance cost is a **going-concern unit cost**, not a
  run-off unit cost with overheads re-spread over a shrinking annuity book [REG-R41].
  The risk margin's reference undertaking, by contrast, "assumes no new obligations"
  after the transfer (TP 4B.1(5)) [REG-R1]. Both are correct as printed; the model must
  carry **two expense bases**, and **no retrieved source explains how the reference
  undertaking's expenses should be set given that tension** [REG-R41][REG-R1]. Nothing
  in the rules prescribes RPI, CPI or national average earnings as the inflation index,
  or any rate — the 3.0% in Assumption inputs (c) stays **[std]**.
- **The best estimate is never negative for this product, and that is a design
  consequence.** A single-premium annuity in payment has no future premium inside the
  boundary, so the present value of outgo cannot be offset [REG-R41][REG-R115]. The
  UK/U.S. divergence that dominates term assurance — an unfloored negative Solvency UK
  best estimate against a floored UK GAAP provision — therefore **does not arise
  here**, and the FRS 103 IG2.41 non-negative and guaranteed-surrender-value floor is
  live but inert, this contract having no surrender value at any time [REG-R100]
  [S1 p4][S2 §12]. The engine must still preserve the sign through every aggregation:
  the floor belongs downstream, never inside the projection [REG-R1].
- **The options and guarantees this design actually contains are inflation options, and
  the policyholder holds none of them.** After the cancellation window there is no
  surrender, transfer, commutation or alteration right [S1 p4][S2 §12][S5 cl.14.7]
  [S7 §7.5][S9 §3.9], so TPFR 11.1's rule against a static behaviour assumption has
  nothing to bite on — dynamic policyholder behaviour is `—` for this product, a cited
  feature and not an omission [REG-R41]. What the *insurer* has written is asymmetric:
  the **RPI 0-floor with catch-up ratchet** and the **LPI 5% cap** [S2 §3.2, defs]
  [S5 §7.1.4][S9 §4.3]. TPFR 15.1 requires all uncertainties to be reflected, expressly
  including claims inflation and **dependency of cash flows on circumstances prior to
  the date of the cash flow** — which is exactly the `peak` state variable — and TPFR
  19.4–19.5 require a scenario-dependent method where the present value depends on
  expected future outcomes **and on deviation from them** [REG-R41]. So: **for
  level-income and fixed-escalation model points a deterministic projection satisfies
  TPFR 19.4–19.5; for `rpi_catchup` and `lpi5` model points the [std] deterministic
  3.0% path does not**, because it values the floor, the ratchet and the cap at
  intrinsic only (Key sensitivities, item 3). The applicability matrix marks
  scenario-dependent valuation `(x)` for this product for precisely that reason
  [REG-R41].
- **Matching adjustment — this is the one product in the library that passes the
  whole-contract test.** The permission is required before use and, once applied to a
  portfolio, cannot be reverted (MA 2.1, 3.2) [REG-R2]. The liability conditions in
  MA 2.2, checked against the representative design [REG-R2][R1]: **2.2(1)** no future
  premiums ✓ [S2 §1.1]; **2.2(2)** the only underwriting risks connected to the
  portfolio must be longevity, expense, revision, mortality or recovery-time risk —
  satisfied, and note that **mortality risk is present**, because the design pays death
  benefits (value protection, guarantee-period instalments, the dependant's reversion)
  [S1 pp10–11][S2 §§5–7]; **2.2(3)** therefore binds and the **5% cap must be tested**;
  **2.2(4)** no policyholder options — satisfied outright rather than through the
  bounded-surrender limb, since there is no surrender value to bound [S1 p4][S2 §12];
  **2.2(5)–(6)** are asset-side and prudent-person conditions. The matching conditions
  themselves are IRPR regulation 4 [REG-R44].
- **The 5% mortality test, in full** [REG-R2]: the more adverse for basic own funds of
  (a) an instantaneous **permanent +15%** in the mortality rates used for the best
  estimate and (b) an instantaneous **+0.15 percentage points** in the rates used to
  reflect experience in the following 12 months, applied **only to policies for which
  it increases technical provisions**, with multiple policies on the same life
  treatable as one and group-level identification permitted under TPFR 20.1 where not
  materially different. SS7/18 ¶3.5 expects quantitative evidence [REG-R8], and
  IRR.22.03 R0070 reports the resulting percentage increase annually [REG-R91]. **This
  is a valuation-layer stress that decides a discounting question**, so it is not
  optional even though nothing in the SCR requires this product to run a mortality
  stress.
- **The eligible-element route does not apply to this product, and that matters for the
  participating form.** An eligible element is either the guaranteed element of a
  with-profits immediate or deferred annuity or the in-payment element of an income
  protection policy or group death-in-service dependants' annuity (MA 1.2); MA 2.3
  otherwise forbids splitting a contract's obligations, and SS7/18 ¶3.6 regards no
  notional splitting as compatible with 2.3 [REG-R2][REG-R8]. The representative
  non-profit design needs none of this — the whole contract goes in. A **with-profits
  pension annuity (code 720)** would reach an MA portfolio only through the
  eligible-element route, and **MA 2.5 does not disapply the no-future-premiums
  condition for that limb** — only for the in-payment limb [REG-R2]; the PRA
  additionally expects a detailed assessment that only contractually guaranteed
  elements are included and a clear policy on where future attaching bonuses go
  [REG-R8].
- **Inflation-linked escalation and matching.** IRPR regulation 4(9) requires assigned
  asset cash flows to be fixed and not changeable, with three exceptions — one of which
  is **inflation-linked assets matching inflation-linked liabilities** [REG-R44]. So
  the RPI and LPI options do not defeat matching; they drive the MALIR 3 stream
  classification, and MALIR 3's rule is unforgiving: **"for liabilities with a
  combination of fixed and inflation-linked characteristics the full set of liability
  cash flows should be reflected as inflation-linked"** [REG-R91] — a policy with any
  indexation reports its guarantee-period instalments and its level VP lump sum in the
  inflation-linked column too, not split.
- **The MA is the difference of two internal rates of return on the same cash flow
  vector** (MA 4.3, replicating IRPR reg 5(1)) [REG-R2][REG-R44] — which is why the
  model's public interface must be `CF(t)`, not a scalar best estimate. The mechanics,
  the fundamental-spread deduction, the notching requirement, the highly-predictable
  10% cap, the attestation and the breach reduction formula are in
  `uk/regulatory/statutory-accounting-and-capital.md`, "The matching adjustment", and
  `uk/regulatory/technical-notes.md`, "Discount curves"; **no fundamental spread,
  probability of default, cost of downgrade or risk-free rate value appears anywhere in
  this library — the PRA's monthly technical-information spreadsheets were not opened**
  [REG-R54]. **Four of SS7/18's attestation materiality metrics are left as bracketed
  placeholders `[w]`, `[x]`, `[y]`, `[z]` that the PRA does not fill in**, and none is
  invented here [REG-R8].
- **Reinsurance is where this product's counterparty-default adjustment gets large.**
  TPFR 24.4's floor — the average loss "must not be assessed at lower than 50% of the
  amounts recoverable … unless there is a reliable basis for another assessment" — is
  the only hard numeric floor in the technical-provisions apparatus, and it lands
  hardest on annuity books because longevity swaps and funded reinsurance put the
  largest recoverables there [REG-R41]. **What counts as a "reliable basis" is not
  settled by any retrieved source.** SS5/24 requires a firm with funded reinsurance to
  be able to produce a **recapture projection** — the gross liability restored to the
  MA portfolio — so gross and ceded must be produced separately, never netted
  [REG-R47]. SS18/16 governs longevity risk transfers, but **it was read only at grep
  level and everything about it beyond one observation is [unverified]** [REG-R48].

### The risk margin

The method, the cost-of-capital rate of 4%, the life tapering factor λ = 0.9 floored at
0.25 and the discounting convention are generic and are in
`uk/regulatory/technical-notes.md`, "The risk margin" [REG-R1][REG-R4]. Three things
change for this product.

- **The reference undertaking may not use the matching adjustment.** TP 4B.1(13)
  excludes the MA, the VA, the risk-free transitional and TMTP from the reference
  undertaking [REG-R1]. For an MA-backed annuity book the risk margin is therefore
  struck on a **materially higher liability basis than the balance sheet it sits on** —
  the best estimate it supports is discounted at basic + MA, the notional SCRs behind
  the risk margin are not. This is the single largest product-specific consequence in
  the risk margin and it is why the row is emphasised for this product in the
  applicability matrix.
- **The run-off is long and the notional SCR is narrow.** The reference undertaking's
  notional SCR captures underwriting risk on the transferred business, market risk
  **other than interest rate risk** where material, credit risk on reinsurance and
  closely-related exposures, and operational risk — and it carries **no loss-absorbing
  capacity of deferred taxes** and selects assets so as to minimise its own market-risk
  SCR [REG-R1]. For this product that reduces `SCR(t)` to essentially longevity,
  expense, counterparty default and operational risk, projected in integer years over a
  run-off that the model's own stopping rule takes to ω = 115 **[std]**. Because
  interest rate risk and LACDT are excluded, **`SCR(t)` cannot be produced by re-running
  the firm's own SCR on a different curve** [REG-R1].
- **There is no sanctioned shortcut.** The revoked Delegated Regulation's Article 58
  simplified risk-margin hierarchy **was not restated into UK rules** — the TPFR Part's
  "SIMPLIFICATIONS" heading introduces Chapter 27 (proportionality) and nothing else —
  and IRPR regulation 7C preserves the PRA's *power* to permit simplified methods
  without that power having been exercised in the Technical Provisions Parts on the
  rule text retrieved [REG-R41][REG-R49][REG-R44]. Any driver-based `SCR(t)` proxy
  therefore has to be justified against TPFR 27.4 alone, and **how `SCR(t)` should be
  projected in practice is a question the retrieved sources do not settle**. Allocation
  of the whole-portfolio risk margin to lines of business is required by TP 4A.3 with
  **no allocation formula prescribed** [REG-R1].

### SCR — the modules that bite

Stresses, correlations and the full-revaluation split are in
`uk/regulatory/technical-notes.md`, "The standard formula SCR"; what follows is the
incidence for this product [REG-R62].

| Sub-module | Rule | Stress | Bites this product? |
|---|---|---|---|
| Longevity | `3B2.1` | instantaneous permanent **−20%** (relative) to the mortality rates used for the TP | **Yes — the dominant charge.** Full revaluation |
| Mortality | `3B1.1` | permanent **+15%** (relative) | Normally no — see the filter note below |
| Life expense | `3B4.1` | **+10%** to expense amounts **and +1 percentage point** to expense inflation | Yes. Full revaluation; second-order in size, but on a 30+ year stream |
| Revision | `3B5.1` | permanent **+3%** to annuity benefits, only where benefits could increase from a change in the legal environment or the insured's state of health | Normally nil — see below |
| Life catastrophe | `3B7.1` | **+0.15 percentage points** (absolute) to mortality in the following 12 months only | Normally no — same filter as mortality |
| Life lapse (up / down / mass) | `3B6` | ×1.5 capped at 100%; ×0.5 capped at −20pp; **40%** mass (70% for RAO class VII only) | **No — none of the three.** See below |
| Interest rate up / down | `3D5` / `3D6` | relative shocks by maturity, converging to 20% at 90 years; up floored at +1pp absolute; down nil for negative rates | **Yes, twice.** Full revaluation of assets **and** the best estimate |
| Spread on an MA portfolio | `3D25` | stress the assigned assets **and recalculate technical provisions for the impact on the MA**, via a fundamental-spread uplift × a CQS reduction factor (45% / 50% / 60% / 75% / 100% / 100% / 100% for CQS 0–6) | **Yes — the only market sub-module that is a liability revaluation here** |
| Equity, property | `3D9`, `3D15` | equity 39% / 49% + symmetric adjustment; property −25% | Asset side only, and only where the assigned portfolio holds them |
| Counterparty default type 1 | `3E13` | `3σ` / `5σ` / `TLGD` step function | Yes — reinsurance and cash at bank |
| Operational | `5.4` | `min(0.3 × BSCR; Op) + 0.25 × Exp_ul` | Yes on the provisions and premiums legs; `Exp_ul` is zero |
| LACTP `Adj_TP` | `6.3` | second complete pass with FDB responsive | **No** for the non-profit design |
| LACDT `Adj_DT` | `6.4` | deferred taxes after an instantaneous loss of `BSCR + Adj_TP + SCR_op` | Yes |
| MA-portfolio notional SCR | `9.1` | the whole exercise repeated per perimeter | **Yes** |

- **Lapse is nil for this product — all three limbs — and it is not "lapse down".**
  This is the classic error the direction rule invites. On a lapse-supported design a
  modeller correctly reaches for `3B6.3`, the **downward** exercise-rate scenario. Here
  there is nothing to stress in either direction: the contract has no surrender or
  transfer value, cannot be assigned or commuted, and cannot be made paid-up
  [S1 p4][S2 §12][S5 cl.14.7][S7 §7.5][S9 §3.9]. So there is **no "relevant option"
  under `3B6.4`** whose exercise rate could be moved ±50%, and **no "discontinuance"
  within the `SCR-SF 1.2` definition** — which expressly includes making a contract
  paid-up — for the **40%** mass event to apply to [REG-R62]. The 70% mass limb reaches
  RAO Schedule 1 Part II class VII only and this is class I business [REG-R62][REG-R64]
  [REG-R14][R8]. The right implementation is a nil requirement with the reason
  recorded, not a lapse scenario with a zero rate.
- **The mortality and catastrophe filters are per-policy, and this product can trip
  them.** `3B1.2`, `3B2.2` and `3B7.2` apply their stresses **only to policies for
  which the stress increases technical provisions without the risk margin** [REG-R62].
  The applicability matrix marks mortality and life catastrophe `—` for a pension
  annuity on the ground that higher mortality *reduces* annuity provisions. That holds
  for a plain lifetime annuity; **it does not automatically hold for this
  representative design**, which pays a value-protection lump sum of up to 100% of the
  purchase price less instalments already paid, or a guarantee period of up to 30 years
  [S1 pp10–11][S2 §§6–7]. Early in its life a 50%-VP model point has a death benefit
  that can dominate its technical provisions, in which case the filter routes it to
  `3B1` and `3B7` rather than out of them. **This is a derivation from the rule's own
  per-policy filter and the product's cited death-benefit mechanics, not a citation —
  no retrieved source states it.** The implementation consequence is unambiguous
  either way: run the filter per policy at each valuation, do not hard-code the answer
  from the product name.
- **Revision risk is normally nil, for a reason worth stating.** `3B5.1` reaches
  benefits that could **increase** as a result of changes in the legal environment or
  in the annuitant's state of health [REG-R62]. Every escalation in this design is
  contractual and fixed at outset [S1 p8][S2 §3.2], and the only right the insurer has
  to change the income is the downward mis-statement correction [S1 p4]. The health
  analogue `3C15.1` is **+4%** and adds **inflation** as a trigger — which is why an
  index-linked income-protection claim annuity is exposed and an RPI- or LPI-escalating
  pension annuity is not [REG-R62]. It is a life obligation, so the health module never
  reaches it at all: `SCR-SF 3.2A` routes health obligations to the health module and
  everything else that is a life obligation to the life module [REG-R62].
- **Interest rate is the second full revaluation, and the direction matters twice
  over.** The charge is the higher of the summed up-requirements and the summed
  down-requirements across currencies [REG-R62] — this book is single-currency, GBP
  [S2 §1.3]. A long-duration annuity liability typically takes its charge from the
  **down** scenario, and the market correlation coefficient `A` between interest rate
  and each of equity, property and spread is **0 where the charge comes from the up
  scenario and 0.5 otherwise**, so the market SCR is a discontinuous function of the
  balance sheet and the model must record which direction won [REG-R62]. Extrapolation
  is a live consideration for the tail: the 2025 assessment retained a **GBP last
  liquid point of 50 years** [REG-R56], while these notes project a 65-year-old to
  ω = 115 **[std]**, so the last portion of the run-off is discounted on extrapolated
  rates. **No ultimate forward rate, convergence period or Smith-Wilson parameter is
  stated anywhere in this library** [REG-R55][REG-R54].
- **`3D25` is where an annuity writer's spread risk becomes a liability calculation.**
  The stress must revalue the assigned assets **and recalculate technical provisions to
  take account of the impact on the amount of the matching adjustment**, so it reaches
  back into the discounting layer [REG-R62]. Economically the MA absorbs
  `1 − reduction factor` of the widening: a CQS 0 assigned portfolio passes 45% through
  to the fundamental spread, while at **CQS 4 and below the MA gives no offset at all**,
  as does an assigned asset with no ECAI credit assessment [REG-R62].
- **Perimeters, and the diversification this product loses.** Holding an MA portfolio
  forces `SCR-SF` Chapter 9 instead of the ordinary aggregation: a notional SCR for the
  MA portfolio, one for the remaining part, **summed with no diversification between
  them** [REG-R62]. The concrete cost here is the **−0.25 mortality/longevity
  correlation** — the only negative entry anywhere in the retrieved standard formula,
  and the reason a mixed protection-plus-annuity book diversifies at all — which
  `9.1(9)` destroys wherever the annuities sit in an MA portfolio and the protection
  business does not [REG-R62]. Two further subtleties: the **scenario choice is made
  firm-wide**, each notional SCR using the scenario worst for the firm as a whole, so
  the MA portfolio's notional SCR can be driven by a scenario that is not its own
  worst — **and how a firm performs that firm-wide search is not prescribed by any
  retrieved source**; and **an MA portfolio is not a ring-fenced fund**, the Glossary
  excluding it expressly, though it takes the identical treatment [REG-R80][REG-R62].
- **What does not reach this product at all**, beyond lapse: the entire **health
  module** `3C` [REG-R62]; **LACTP**, `Adj_TP` being capped at future discretionary
  benefits which the non-profit design does not have, so `BSCR = nBSCR` and one run
  suffices — the with-profits form (code 720) is what would force the two-run
  architecture [REG-R62]; the **ring-fenced-fund notional SCR** [REG-R62][REG-R71]; the
  **`0.25 × Exp_ul` operational leg**, there being no unit-linked expense [REG-R62];
  **technical provisions as a whole**, TPFR 22.2 declaring biometric-dependent cash
  flows and all servicing expenses non-replicable [REG-R41]; and **EPIFP**, which has
  been removed from Solvency UK reporting and disclosure altogether [REG-R86][REG-R77].
- **Two smaller points.** The **longevity simplification** `7.9`
  `= 0.2 × q × n × 1.1^((n−1)/2) × BE_long` is the one closed form that reaches this
  product, usable only after a documented proportionality assessment of the error
  introduced and never where that error could influence the user, unless it produces a
  higher SCR [REG-R62]. And **undertaking-specific parameters reach exactly one thing
  here** — the increase in the amount of annuity benefits for **life revision risk**,
  and only where the annuities are not subject to material inflation risk, which
  excludes an RPI- or LPI-escalating book and is in any event nil for this design; a USP
  requires a permission and cannot be reverted [REG-R65].
- **A time-sensitive item.** `SCR-SF 6.5`, the transitional permitting an increase in
  deferred tax assets to be used in LACDT, is printed as running "for a transitional
  period ending 30 December 2025", which on its face has expired, and **no PRA
  instrument confirming expiry or extension was retrieved** — treat it as expired for a
  current-date calculation and flag it [REG-R62].

### Own funds, ring-fenced funds and the MA portfolio

- **The representative design is not in a ring-fenced fund, but it takes the identical
  deduction.** Own Funds 3L reduces the excess of assets over liabilities, for
  reconciliation-reserve purposes, by `max(0, restricted own funds within the RFF or MA
  portfolio − that perimeter's notional SCR)`; where the assets, liabilities and risk
  are not material the firm may instead deduct the total restricted own funds and skip
  the notional SCR [REG-R77]. **Restricted own funds inside the MA portfolio therefore
  count towards entity own funds only up to the capital that portfolio itself needs**,
  which is the numerator half of the ring-fencing cost (the denominator half being the
  lost diversification above). **Whether the 3L deduction also bites the MCR coverage
  test is not settled**: 3L operates textually on the reconciliation reserve, while the
  EIOPA ring-fenced-funds guideline is explicit that only own funds equal to the
  notional SCR contribute to coverage of the SCR **and the MCR**, and no retrieved PRA
  rule says so [REG-R77][REG-R80c].
- **Surplus funds and the with-profits estate reach this product only in participating
  form.** The Surplus Funds Part applies per **with-profits fund**, and the Tier 1
  unrestricted own-funds item at Own Funds 3A.1(1)(d) follows from it
  [REG-R45][REG-R46][REG-R77]; a with-profits pension annuity (code 720) written inside
  such a fund is in scope, the representative non-participating contract [S7 §7.9] is
  not. **The PRA Rulebook Glossary definition of "surplus funds" could not be retrieved
  after ten URL forms**, so the scope of the defined term is [unverified] [REG-R45].
- **MCR.** The linear formula's term for this product is `TP_l4`, all other long-term
  obligations — technical provisions **without the risk margin**, net of reinsurance
  and floored at zero term by term. `TP_l2` (future discretionary benefits, carrying
  the formula's only negative coefficient) and `TP_l1` reach only the participating
  form. **Capital at risk** reaches this product only through its death benefits — the
  guarantee period, value protection and the dependant's reversion — where the sign is
  typically negative and the **per-contract** zero floor bites, so the portfolio total
  is not the sum of signed amounts [REG-R78]. The absolute floor for long-term business
  is **£3,500,000**, and for a book of this size `MCR_linear` sits far below 25% of the
  SCR, so the MCR is normally the **25% collar** [REG-R78]. Two unsettled points are
  recorded rather than resolved: MCR 3.1B does not state on its face that the corridor
  SCR includes capital add-ons while MCR 3.3 does, and **the MCR Part contains no
  ring-fenced-fund or MA-portfolio rule at all** [REG-R78].
- **Distributable profits come off the prudential balance sheet, and this product adds a
  deduction of its own.** For a Solvency-UK-authorised long-term insurer, CA 2006
  s.833A makes the realised profit or loss `A − L − D` on **prudential** values, and the
  deduction list `D` includes — where the firm has a matching adjustment permission —
  **the excess of the assigned asset portfolio value over the value of the MA
  obligations**, together with related deferred tax liabilities; s.833A(3) then caps
  distributable profits at accumulated profits per the accounts [REG-R104]. So a UK
  annuity writer's distributable-earnings pattern needs the **MA portfolio surplus
  projected as a separate quantity**, not merely the balance sheet.

### Statutory accounts and tax

- **UK GAAP.** A lifetime annuity transfers significant insurance risk on any reading,
  so the contract is inside **FRS 103** — this product has none of the
  investment-contract ambiguity that reaches a unit-linked bond [REG-R99]. The
  liability is the **long-term business provision**, Schedule 3 liabilities item
  **C.2**, computed under Schedule 3 paragraph 52 [REG-R105]. FRS 103 fixes little of
  the measurement and much of the presentation: it names the **modified statutory
  solvency basis** as "the established accounting treatment for long-term insurance
  business" and grandfathers practices that could not be newly introduced, including
  measuring insurance liabilities **undiscounted** [REG-R99]. The only measurement
  floor UK GAAP imposes is the **liability adequacy test** (¶¶2.14–2.18), which must
  use current estimates of all contractual and related cash flows "as well as cash
  flows resulting from embedded options and guarantees" — for this product that means
  the RPI floor, the catch-up ratchet and the LPI cap belong inside the test even where
  the recognised provision is on a locked-in basis [REG-R99]. **The definitions the
  with-profits half of that apparatus rests on — INSPRU 1.3.40 and 1.3.190 as at
  31 December 2015 — were not retrieved by anyone in this library**
  [REG-R99][REG-R116].
- **DAC: the U.S. story is reversed.** UK company law **requires** deferral —
  SI 2008/410 Schedule 3 **para 13** requires acquisition costs incurred in one
  financial year but relating to a subsequent one to be deferred, with DAC at assets
  item **G.II** and its movement at technical account item **8(b)** — and FRS 103 ¶3.7
  says acquisition costs "**shall be deferred**", subject to recoverability, amortised
  over no longer than the recoverability period and in a similar profile to the margins
  [REG-R105][REG-R99]. **So there is no U.S.-style "expensed as incurred, no DAC asset,
  first-year surplus strain" story to carry across.** What is product-specific: this
  contract's set-up and administration costs are **priced into the annuity rate** and
  adviser charges are deducted from the purchase price before it reaches the annuity
  [S1 p6][S1 p12][S4][S6][S9], and the reference model does not project acquisition
  cash flows at all (Assumption inputs (c), note (iv)) — so the DAC configuration is
  live for the writer and out of scope for this implementation, and neither fact should
  be read as an absence of DAC. The **note 17 carve-out** is the fork to make explicit
  if acquisition costs are ever modelled: DAC is excluded to the extent the long-term
  business provision already allows for the costs, by explicit recognition or
  implicitly through anticipation of future income [REG-R105]. On the Solvency UK ledger
  there is **no DAC at all** — acquisition expenses are projected cash outflows inside
  the best estimate (TPFR 16.1(4)) and the Valuation Part recognises no unamortised
  expense asset (Val 8.1) [REG-R41][REG-R39] — though for an in-force single-premium
  annuity there are no future acquisition cash flows inside the boundary in any event.
- **IFRS 17: the general measurement model.** The UKEB's expectation for the UK is
  explicit — the **variable fee approach** "is expected to be applied to insurance
  contracts such as unit-linked contracts and with-profits contracts" and the premium
  allocation approach to short-term business, **leaving the GMM for protection and
  annuities** [REG-R106]. The representative design has no direct participation
  features [S7 §7.9], so VFA is unavailable to it; the with-profits form would be VFA,
  and VFA eligibility is assessed at inception and **never reassessed**. Acquisition
  cash flows never appear as an asset under IFRS 17 — they sit inside the fulfilment
  cash flows and **reduce the CSM at initial recognition** [REG-R106], a third pattern
  distinct from both ledgers above. **The open issue for this product is the coverage
  unit.** CSM allocation for **annuities** is priority issue A of the UKEB's endorsement
  assessment; the IFRS Interpretations Committee issued a Tentative Agenda Decision on
  the point, and divergence continues over whether investment-return service is a
  separate service and over how coverage units are weighted [REG-R106]. **The
  requirement to identify coverage units binds; the right answer for an annuity is not
  settled by the retrieved material**, which is why the applicability matrix marks that
  row `?` for this product alone. **IFRS 17 itself is paywalled and was never read**, so
  no confidence level, coverage-unit formula or transition proxy appears anywhere in
  this library [REG-R107][REG-R106].
- **Tax: non-BLAGAB pension business, taxed on trade profits.** A pension annuity is
  **pension business**, excluded from BLAGAB by FA 2012 s.57(2)(a) and taxed on trade
  profits rather than on the I-E basis [REG-R17][REG-R18 LAM01080], as the Just
  conditions state expressly [S5 §14.11]. The consequences are all negative and all
  useful: **no I-E computation**; no s.79 seven-year acquisition-expense spreading —
  itself repealed for accounting periods beginning on or after 1 January 2023
  [REG-R18 LAM04130][REG-R109]; no s.93 minimum profits test; and **no s.102–103
  policyholder / shareholder rate split** for this business [REG-R17][REG-R18]. Trade
  profits have been based on **accounting** profits since 1 January 2013
  [REG-R18 LAM01100], so the tax leg consumes the accounts leg, not the Solvency UK
  leg. **The trap is the source of the purchase money, not the contract:** "general
  annuity business" *is* inside BLAGAB, so a **purchased life annuity** bought with
  non-pension money runs the same cash-flow engine on the I-E basis
  [REG-R18 LAM01080] — every projected cash flow, asset and liability still needs a
  **BLAGAB / non-BLAGAB tag** with a commercial allocation applied consistently across
  income, gains and trade profits [REG-R18 LAM05020].
- **Deferred tax exists on two balance sheets, on two different models.** FRS 102
  Section 29 recognises it on **timing differences**; Valuation 11 recognises it on
  **all** assets and liabilities including technical provisions, measured as the
  difference between the Solvency UK value and the tax value [REG-R102][REG-R39]. They
  are structurally different numbers for the same company, which is why a UK model
  carries **three liability measures per period — accounts, tax and Solvency UK — not
  two**, and why LACDT requires a **post-stress tax balance sheet** rather than a factor
  [REG-R62]. Roll-forward mechanics are in `uk/regulatory/technical-notes.md`,
  "Statutory accounts and tax roll-forward".

### What this product's model must additionally produce

Shared contract: `uk/regulatory/technical-notes.md`, "Required model outputs". The rows
below are the ones this product specialises, makes trivial, or alone triggers.

| Output | What it is for this product | Cite |
|---|---|---|
| `CF(t)` monthly to month 600, four streams | level/fixed-escalation claims, **inflation-linked claims** (the whole contract wherever any indexation is present), expenses, other — gross of reinsurance, per MA portfolio, effective 31 December; PV on the basic curve **and** on basic + MA | [REG-R91] |
| Contract-boundary flag | constant: the whole contract, no future premiums, no exclusion limb engaged — but emitted with the limb, not stored as a product constant | [REG-R41] |
| Segmentation keys | LoB 32 (a drafter's inference, [unverified]); MA portfolio as the fund tag; PRA product code **724**, or **734** where the enhanced overlay θ > 1 | [REG-R41][REG-R89] |
| MA eligibility evidence | the best estimate re-run under the MA 2.4 mortality stress — the more adverse of +15% permanent and +0.15pp for 12 months — applied only where it increases TP, as a percentage increase against the 5% cap | [REG-R2][REG-R8][REG-R91] |
| Longevity-stressed best estimate | full revaluation at −20% on the rates used for the TP, filtered to policies where the decrease increases TP without the risk margin | [REG-R62] |
| Per-policy directional flags | for mortality, longevity and life catastrophe — recomputed each valuation, because a VP-heavy or long-guarantee model point can sit on the other side of the filter | [REG-R62] |
| Lapse outputs | **none** — no relevant option, no discontinuance, no worst-discontinuance value; record the nil requirement with its reason | [REG-R62] |
| `SCR(t)` run-off | reference undertaking basis: **no MA**, no interest rate risk, no LACDT, minimise-market-risk assets; integer years over the full annuitant-and-dependant run-off | [REG-R1] |
| Capital at risk | per contract, from the guarantee period, value protection and dependant's reversion only; **floored at zero per contract**, so the portfolio total is not a sum of signed amounts | [REG-R78] |
| Gross and ceded, never netted | plus a **recapture projection** restoring the gross liability to the MA portfolio for any funded reinsurance, and a counterparty-default adjustment at LGD ≥ 50% per counterparty and per line of business | [REG-R47][REG-R41] |
| IR.12.04 assumption pack | annuitant mortality as a percentage of a **named table** with the CMI parameterisation in CMI notation; the complete expectation of life at 65 with and without improvements; the per-policy annuity renewal expense unit cost — with five years of own experience alongside | [REG-R89] |
| Two expense bases | going-concern (TPFR 16.4) for the best estimate and no-new-business for the reference undertaking — **no source specifies the second** | [REG-R41][REG-R1] |

Not needed for this product: future discretionary benefits and the responsive-FDB run;
unit-linked's surrender value, nominal value of units and matching value of units; the
worst-discontinuance value; `Exp_ul`; a ring-fenced-fund notional SCR; and the EPIFP
decomposition, which Solvency UK no longer collects from anyone [REG-R86][REG-R77].

### Traps peculiar to this product

1. **Lapse is nil, not "lapse down".** The habit a modeller brings from a
   lapse-supported design — reach for the downward exercise-rate scenario `3B6.3` — is
   wrong here in a way that produces a plausible non-zero number. There is no relevant
   option under `3B6.4` and no discontinuance within the `SCR-SF 1.2` definition,
   because the contract has no surrender or transfer value, cannot be assigned or
   commuted and cannot be made paid-up [REG-R62][S1 p4][S2 §12][S5 cl.14.7][S7 §7.5]
   [S9 §3.9]. All three limbs, including mass lapse, are nil.
2. **The death benefits can flip the mortality and catastrophe filters.** `3B1.2`,
   `3B2.2` and `3B7.2` are **per-policy** filters on whether the stress increases
   technical provisions without the risk margin [REG-R62]. Value protection at up to
   100% of the purchase price, or a guarantee period of up to 30 years, can make a
   young in-force model point death-benefit-dominated [S1 pp10–11][S2 §§6–7] — so the
   generic "an annuity is a longevity risk, full stop" reading is a portfolio
   statement, not a per-policy rule. **This qualification is a derivation from the rule
   text plus the product's cited mechanics; no retrieved source states it.**
3. **MA eligibility needs a mortality stress that the SCR does not ask for.** Because
   the design carries death benefits, mortality risk is present in the MA obligation
   portfolio and MA 2.2(3) binds: the best estimate must not increase by more than
   **5%** under the MA 2.4 stress [REG-R2][R1], reported annually at IRR.22.03 R0070
   [REG-R91]. A model built to compute only longevity stresses — because that is what
   the SCR charges — cannot demonstrate its own discount rate's eligibility. Related and
   unresolved: **no retrieved source addresses whether the 30-day statutory cancellation
   right [S1 p7][S2 §13] is a "policyholder option" for MA 2.2(4)**; these notes project
   from a completed purchase **[std]** and the question is left open rather than
   answered.
4. **Any indexation makes the whole contract inflation-linked for MALIR 3.** The
   instruction is explicit that "for liabilities with a combination of fixed and
   inflation-linked characteristics the full set of liability cash flows should be
   reflected as inflation-linked" [REG-R91] — so an RPI or LPI model point reports its
   guarantee-period instalments and its level value-protection lump sum in the
   inflation-linked column as well. Splitting a policy across the fixed and
   inflation-linked columns is wrong even though it looks more accurate.
5. **RPI-linked is not index-linked, and GMP tranches are neither.** For IR.14.01 the
   IL definition "excludes RPI / CPI linked policies" [REG-R89], so every escalation
   option here reports under the non-profit code. Separately, GMP and Section 9(2B)
   tranches — excluded from the model **[std]** — carry statutory escalation minima
   (post-88 GMP at RPI capped 3%) on their own escalation dates [S2 §3.3][S5 §7.2],
   which makes such a tranche inflation-linked for MALIR 3 and shifts its escalation
   timing away from the policy anniversary the recursions assume.
6. **Enhanced lives are a reporting split even though they are a modelling overlay.**
   These notes represent enhancement as a multiplier θ on qx **[std]**, but the
   enhanced contract has its own PRA product code **734** and IR.12.04's annuitant
   mortality rows R0290 / R0330 are expressly restricted to **standard lives**, with
   **the retrieved instruction silent on where enhanced or impaired annuitant mortality
   is reported** [REG-R89]. Compounding it, C0080 wants a **named table** and the
   tables a UK annuity writer would name are CMI Authorised-User material, which is why
   the reference basis is an honest ONS × α proxy rather than an approximated
   "SAPS-like" rate [R10][R11][REG-R22][REG-R27].
7. **The risk margin is computed without the matching adjustment.** TP 4B.1(13) bars
   the reference undertaking from applying the MA, the VA, the risk-free transitional
   or TMTP [REG-R1]. Re-using the balance-sheet best estimate, or the firm's own SCR on
   a different curve, understates the risk margin — the reference undertaking also
   excludes interest rate risk and deferred-tax loss absorbency and picks assets to
   minimise its own market-risk SCR.
8. **An MA portfolio destroys the one negative correlation in the standard formula.**
   The **−0.25** mortality/longevity entry is the only negative coefficient in the
   retrieved life matrix, and it is why a mixed protection-and-annuity book diversifies
   — but `SCR-SF 9.1(9)` forbids diversification between an MA portfolio, a ring-fenced
   fund and the remaining part, so the credit is lost wherever the annuities are inside
   the portfolio and the protection business is outside it [REG-R62].
9. **A deterministic RPI path is not a TPFR 19.4–19.5 answer for indexed model points.**
   The 3.0% **[std]** assumption makes the ratchet never bind and the LPI cap never pay
   off, valuing three written options at intrinsic only [S2 §3.2, defs]. For `level` and
   `fixed` model points a deterministic projection is defensible; for `rpi_catchup` and
   `lpi5` it is a documented limitation of the reference implementation, not a
   valuation [REG-R41].
10. **Two expense bases, and the second one has no source.** TPFR 16.4 requires the
    best-estimate expense basis to assume the firm writes new business, while the risk
    margin's reference undertaking assumes no new obligations (TP 4B.1(5)) — both as
    printed, and **no retrieved source explains how to set the reference undertaking's
    expenses** [REG-R41][REG-R1]. A single £30 p.a. **[std]** unit cost used for both is
    a simplification, not a basis.
11. **The tax basis follows the money, not the mechanics.** Identical contractual cash
    flows are non-BLAGAB trade-profit business when bought with pension money and
    BLAGAB general annuity business when bought with anything else
    [REG-R17][REG-R18 LAM01080]. A model that hard-codes "annuity ⇒ no I-E" is right
    for this product and wrong for the purchased life annuity next to it.
12. **Bulk purchase annuities are the same engine under a different code and a heavier
    supervisory overlay.** BPAs are out of this library's scope, report under **754**,
    and are the reason SS5/24 (funded reinsurance, with its recapture-within-MA-portfolio
    expectations) and SS18/16 (longevity risk transfers) exist [REG-R89][REG-R47]
    [REG-R48]; **SS18/16 was read only at grep level and everything about it beyond one
    observation is [unverified]** [REG-R48]. The per-policy mechanics in these notes are
    what such a book is assembled from — but MALIR 5, which contains the quantitative
    matching tests any MA portfolio must pass, **was not read** [REG-R91].

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows. The Solvency UK
balance sheet, the SCR components, the reporting templates and the two other ledgers
**for this product** are in **Statutory accounting and capital** above; this section
stays a pointer list for the valuation layers that consume `CF(t)`, none of which is
reproduced here.

- **Solvency UK best estimate.** Technical provisions = best estimate + risk margin;
  the best estimate is the probability-weighted average of future cash flows
  discounted at the relevant risk-free term structure, market-consistently [REG-R1].
  The `CF(t)` vector above is exactly that input. Mechanics:
  `uk/regulatory/technical-notes.md`, "The best estimate liability".
- **Matching adjustment.** These cash flows feed MA discounting (risk-free + MA) for
  eligible portfolios: MA permission required; eligibility conditions include no
  future premiums, restricted underwriting risks, the ≤ 5% BEL mortality-stress
  test, and no policyholder options [R1][REG-R2]. Reform context: CP19/23 → PS10/24,
  effective 30 June 2024 [R2][REG-R5]; supervisory expectations and matching tests
  in SS7/18 (October 2025 version) [REG-R8]. How the conditions land on this design
  is above; the MA arithmetic is in `uk/regulatory/technical-notes.md`, "Discount
  curves", and remains cited-not-specified in these product notes.
- **Risk margin.** Cost-of-capital method at 4% with life-business tapering λ = 0.9
  (floor 0.25) per SI 2023/1346 [REG-R4]; requires a projected run-off of the
  **reference undertaking's** notional SCR, which for this product is struck without
  the matching adjustment (above, "The risk margin") [REG-R1].
- **Transitionals.** TMTP (simplified regime from 31 December 2024) reaches only
  obligations that were the firm's *qualifying* obligations on **31 December 2024**,
  or obligations assumed after that date through a **transfer event** (2.4); it
  adjusts technical provisions, not projected cash flows, and must not be applied
  after 1 January 2032 (2.3) [REG-R3]. The **pre-2016** test belongs to **TMIR**,
  whose *admissible obligations* are contracts concluded before **1 January 2016**
  whose technical provisions were determined under INSPRU 1.1.16R as at 31 December
  2015 and which are **not subject to an MA permission** [REG-R57]. An MA-backed
  portfolio may therefore carry TMTP but is **excluded from the risk-free
  transitional** [REG-R57].
- **IFRS 17.** UK-adopted IFRS 17 (adopted 16 May 2022, effective 1 January 2023)
  [REG-R38] measures the same contracts as fulfilment cash flows plus risk adjustment
  plus CSM; the expected-cash-flow engine is identical, with regime-specific
  discounting and margins layered on. The measurement mechanics, carried as
  [unverified] general knowledge on the frozen reference page (which verifies the
  adoption facts only), are sourced to the UKEB endorsement assessment in the shared
  framework [REG-R106]; the measurement model for this product, and the unresolved
  coverage-unit question, are above.
- **Tax.** Pension annuities are pension business — non-BLAGAB, trade-profit basis
  [REG-R17][S5 §14.11]; no policyholder fund tax enters the projection. The BLAGAB
  contrast with a purchased life annuity is above.
- **Professional standards.** Technical actuarial work using this model in the UK
  falls under FRC TAS 100 v2.0 [REG-R33] and TAS 200 v2.0 (effective 1 January 2025)
  [R14]. Proxy models fitted on top of heavy annuity cash-flow models — and the
  outputs the heavy model must expose for them — are treated in the IFoA proxy-model
  working party paper [REG-R36].

---

## Key sensitivities and model risks

Dominant assumptions, in order:

1. **Longevity level (base table × α × θ).** The liability is a life-contingent
   payment stream with no offsetting decrements; a lower mortality level lengthens
   every annuity stream. The [std] α = 0.80 population-proxy adjustment is the
   weakest link in the reference basis — production work must substitute licensed
   SAPS S4 / PMA16-era tables [R10][R11][REG-R27][REG-R22].
2. **Longevity trend (improvements).** The [std] deterministic scale stands in for
   CMI_2025 [REG-R30]; the choice of long-term improvement rate is the single most
   sensitive judgment in UK annuity valuation, and the CMI model's user-set long-term
   rate has no default recommendation [REG-R30, detail unverified]. The prescribed MA
   mortality stress (worse of +15% level / +0.15pp additive, ≤ 5% BEL movement) [R1]
   gives a regulatory yardstick for level-risk materiality.
3. **Inflation exposure (RPI/LPI options).** RPI-linked instalments make the
   liability an inflation swap; the 0-floor, catch-up ratchet and LPI 5% cap are
   inflation option positions [S2 §3.2, defs]. A deterministic 3% path **[std]**
   values them at intrinsic only: the floor and ratchet never bind and the cap never
   pays off — stochastic inflation (or option-adjusted margins) is required for a
   market-consistent value. RPI reform risk (index definition) is additional and not
   modeled.
4. **Dependant assumptions.** δ, the age gap, and dependant mortality drive the
   joint-life tail; the independence assumption **[std]** ignores broken-heart
   dependence and common lifestyle factors, overstating the expected dependant
   stream modestly.
5. **Expense inflation.** Second-order (expenses are small against instalments), but
   the in-payment term is 30+ years, so the π assumption compounds.

Known modeling pitfalls:

- **Guarantee double-counting.** During the guarantee, the annuitant stream is
  certain — do not also weight it by l_a(t) (the max(1{t≤n}, l_a) form prevents
  paying 1 + l_a). Symmetrically, VP and guarantee never coexist in the
  representative design [S2 §§6.7, 7.6]; engines supporting the Canada Life
  combinable variant must net guarantee payments off VPbal [S7 §4.3] or the death
  benefit is double-paid.
- **Overlap gating.** Without overlap the dependant stream is gated on t > n even
  when the annuitant died mid-guarantee; applying δ from the death date silently
  converts every without-overlap policy into the more expensive with-overlap form
  [S2 §§5.9–5.11].
- **Higher-of dependant base.** The δ × A(y(t)) simplification relies on
  non-decreasing escalation; if a decreasing option is configured (Just's pure RPI
  [S5 §7.1.2]), the contractual "higher of income at death and at guarantee end"
  [S2 §5.12] must be implemented explicitly.
- **Survival-measurement timing.** Arrears payments require survival at the payment
  date; advance payments at the period start. Using end-of-period survival for
  advance payments understates the liability by roughly one period's mortality per
  payment — material at high ages.
- **Catch-up state.** The RPI ratchet is path-dependent: peak must persist across
  anniversaries. Resetting it each year turns the catch-up into a plain 0-floor and
  overstates indexed income after deflation-recovery paths [S2 defs].
- **Escalation timing.** Increases apply on the anniversary [S2 §3.3], not on
  payment dates; applying the year-2 rate to the t = 12 arrears instalment (accrued
  in year 1) overstates income. GMP-bearing policies use different escalation dates
  (1 April / 1 May at Just [S5 §7.2]) — out of scope with GMP generally **[std]**.
- **VP balance timing.** VPbal must net instalments *paid before death*; netting the
  instalment due at the death-month payment date that was never paid (arrears,
  without proportion) understates the lump sum [S2 §§4, 7]. Symmetrically, on
  advance timing an instalment paid at the *start* of the death month has been paid:
  in advance payment months net it (use VPbal after the month-t advance payment,
  not VPbal(t−1)) or the lump sum is overstated by one instalment.
- **Population-proxy basis risk.** The [std] ONS × α basis has the wrong shape as
  well as level versus annuitant tables (socio-economic mix, amounts weighting
  [R10][R11 detail unverified]); treat all reference-basis results as mechanics
  demonstrations, not valuations — and note the CMI restriction honestly rather
  than shipping approximated "SAPS-like" rates [REG-R22].
