# Individual Income Protection — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md`, whose numbering is carried verbatim from
`uk/_research/income-protection.md`; [REG-R#] tags refer to the cross-product
reference library `uk/references/regulatory-and-actuarial-references.md` (its own
R-numbering; research provenance for **R1–R38** in
`uk/_research/regulatory-actuarial.md` and for **R39–R120** in the six later research
files — block allocation and unused ranges in *Statutory accounting and capital*
below).
**[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter
values are identical to those in `product-spec.md`.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, benefit
  outgo, expenses) for a single-policy model point of full-term guaranteed-premium
  own-occupation IP. Reserves are not computed (see Valuation and reserve pointers).
- **Model structure.** Three-state multiple-state model — healthy/active (H), sick
  and in claim payment (S), dead (D) — the structure of the CMI graduations: CMIR 12
  introduced the healthy–sick–dead multiple-state model for UK PHI, applied to the
  IPM 1991-98 graduations and carried through to the IP11 Series [R4][R1]. (The CMIR
  12 report title/date is recorded from search summaries only [unverified].) Lapse is
  an additional exit from H. Experience is parameterized exactly as the CMI publishes
  it: claim **inception** rates by sex, deferred period and occupation class, and
  claim **termination** rates split by recovery and death, duration-dependent [R1][R2].
- **Projection frequency.** Monthly grid, matching the monthly-in-arrears benefit
  [S1][S3][S10]. Annual assumption rates are converted to monthly per the formulas
  below **[std]**.
- **Timing conventions [std].** Premiums received at the beginning of the policy
  month (BOM) from lives in H; state transitions occur at end of month (EOM); benefit
  for month t is paid at EOM to lives in claim payment throughout month t — in S at
  BOM and still in S at EOM (monthly in arrears [S1]; a claim incepting at EOM t
  receives its first payment at EOM t+1). The
  contractual daily pro-rating of partial claim months [S1][S3][S10] is replaced by
  whole-month payment **[std]**. Escalation applies at BOM of each anniversary month.
- **Age basis.** Age nearest birthday at entry, advancing with policy year **[std]**.
  No public statement of the IP11 age definition was retrieved (the briefing note
  records graduated age ranges 17–65 M / 17–60 F, extended to 70 [R1]); the choice
  is a pure convention and must be revisited by CMI Authorised Users.
- **Claim duration.** Measured in months since claim (payment) inception, i.e. since
  the end of the deferred period **[std]** convention; IP11 termination rates are
  two-dimensional in age and sickness duration, with run-in periods of increasing
  recovery rates at early durations for DP4/13/26 [R1]. Whether the CMI duration
  clock runs from sickness onset or payment start was not extracted from public
  documents — subscribers must align the convention with the tables they license.
- **Currency and units.** GBP; benefit and premium in £/month; rates are
  probabilities per period unless labelled "per mille".
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis; survivorship/state probabilities multiply per-policy
  cash flows. In-force portfolios need both active cells and claims-in-payment cells
  (with claim duration as a model-point attribute).

---

## Model point attributes

| Attribute | Type | Example (base cell) |
|---|---|---|
| `entry_age` | int | 35 **[std]** |
| `sex` | enum {M, F} | M **[std]** — IP11 rates are sex-split [R1] |
| `occ_class` | enum {1, 2, 3, 4} | 1 **[std]** — CMI occupation classes OC1–OC4 [R1] |
| `benefit_monthly` | currency (£/month at issue) | 2,000 **[std]** |
| `earnings_annual` | currency (underwriting record) | 40,000 **[std]** |
| `deferred_weeks` | enum {4, 8, 13, 26, 52} | 26 **[std]** |
| `expiry_age` | int (50–70) | 65 **[std]** |
| `escalation` | enum {none, RPI} | RPI (capped 10%, premium ×1.5) [S1][S2] |
| `premium_monthly` | currency (£/month at issue) | 35 **[std]** — rates not public |
| `premium_basis` | enum {guaranteed} (reviewable/age-costed out of scope) | guaranteed |
| `status` | enum {active, in_claim} | active |
| `claim_duration_months` | int (in-claim cells only) | 0 |

Smoker status is not an attribute: the IP11 rate structure is sex / deferred period /
occupation class [R1]; any smoker differentiation sits in insurer pricing, which is
not public.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l_H(t)` | Probability in state H (active premium-payer, incl. any sickness spell still inside the deferred period — see Deferred-period mechanics) at EOM t | monthly |
| `l_S(t, z)` | Probability in claim payment at EOM t with claim duration z months (z = 1, 2, ...) | monthly, two-dimensional |
| `l_S(t)` | Total in-claim probability = Σ_z l_S(t, z) | derived |
| `B(y)` | Escalated monthly benefit in policy year y | at anniversaries |
| `P(y)` | Escalated monthly premium in policy year y | at anniversaries |
| `AP(y)` | Amount payable per month of full incapacity (spec formula; base: = B(y)) | at anniversaries |
| `n(t)` | New claim inceptions during month t | monthly |
| `rec(t)`, `dth_S(t)`, `dth_H(t)`, `lps(t)` | Exits: recoveries, deaths in claim, deaths in H, lapses | monthly |

There is no account value, surrender value or unit fund: the contract has no cash-in
value at any time [S4][S5][S7], so the only state is the insured population itself.

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited; from the spec)

| Input | Value | Basis |
|---|---|---|
| Deferred period d | 26 weeks (base cell) | menu [S6]; pick **[std]** |
| Benefit formula parameters | 65% / 50% bands, £60,000 breakpoint, £20,000/month cap, £1,500 guarantee, 90% tolerance | [S1][S2][S5][S7]; picks **[std]** (spec footnotes 6–8) |
| Escalation mechanics | j(y) = min(max(RPI_y, 0), 0.10); B ×(1+j); P ×(1+1.5j); continues in claim | [S1][S2]; multiplier pick **[std]** |
| Premium guarantee | Guaranteed level apart from escalation | [S1][S3][S5][S7] |
| Waiver of premium | No premiums from lives in S (payable through the deferred period) | [S5][S7][S10][S11]; convention **[std]** |
| Linked claims | Same-cause recurrence within 52 weeks: no new deferred period | [S1][S3][S5][S7][S10][S11]; window pick **[std]** |
| Proportionate benefit | (A − B)/A × C on partial return to work | [S7]; common structure [S1][S3][S5][S10][S11] |
| Expiry | All cover and claim payments cease at the policy end date (age 65 base cell) | [S1][S3][S5][S7][S10]; age pick **[std]** |
| Grace | 60 days, cancellation without value | [S1][S3]; pick **[std]** |

### (b) Insurer-discretionary current elements

For the guaranteed-premium full-term composite these are deliberately **thin**: there
are no bonuses, no reviewable charges, and no market value reductions — premiums are
guaranteed [S1][S3][S5][S7] and there is no surrender value [S4][S5][S7]. Recorded
for the variations only:

- **Reviewable premiums** (variation): fixed for 5 years, then reviewed with no
  contractual cap [S1][S4][S6][S10]. Review formulas are discretionary and
  undisclosed (research file gap) — any reviewable-premium model needs a **[std]**
  review rule; none is specified here.
- **Holloway surplus participation** (out-of-scope variation): Surplus Allocation /
  Bonus Allocation / discretionary Terminal Bonus on With-Profits Actuary advice
  [S11][S12] — requires a capital-account state not present in this model.
- **Escalation index snapshot**: future RPI is an economic input, not insurer
  discretion; the reference snapshot is RPI = 3.0%/yr flat **[std]**, so
  j = 0.03, premium growth 4.5%/yr while premiums are payable.

### (c) Behavioral / experience assumptions (modeler's view)

The authoritative UK experience basis is the CMI IP11 Series (individual IP,
2007–2016 data): claim inception rates by sex, deferred period (DP1/4/13/26/52) and
occupation class (OC1–OC4); termination rates split recovery vs death,
two-dimensional in age and sickness duration; table naming
`IP11 {M/F} DP{d} OC{n} {Inc/Rec/Dth}` [R1]. **The rate values are restricted to CMI
Authorised Users** (the working papers and the IP Rate Table Tool are
subscriber-only [R2][R3][R5]; the CMI access model is per [REG-R22]), so the
reference basis below is a **[std] proxy shaped like the IP11 structure — the values
are NOT IP11 values and carry no CMI authority.** Known data issue: IP11 inception
rates are understated due to exposure errors; the CMI published indicative
adjustments alongside WP136 (terminations unaffected) [R1][R2][R3] — users with
table access must apply them.

| Input | Reference basis | Basis tags |
|---|---|---|
| Claim inception rates ι_a(a) | [std] proxy table below (structure: M, DP26, OC1 [R1]) | values **[std]** |
| Recovery rates ρ_a(z) | [std] proxy table below, by claim duration year (IP11 is duration- AND age-dependent [R1]; age suppressed **[std]**) | values **[std]** |
| Mortality in claim q_S_a(z) | [std] proxy, flat 3%/yr all durations (IP11: duration-dependent to 5 years, age-only beyond [R1]) | value **[std]** |
| Active-life mortality q_H_a(a) | ONS UK national life tables qx (sex-specific), ×100% factor | table [REG-R32]; factor **[std]** (1) |
| Mortality/morbidity improvement | None in base **[std]**; CMI_20xx with a [std] long-term rate is the projection convention for mortality | [REG-R30] |
| Lapse w_a(y) | [std] table below; no public UK IP lapse study was retrieved | **[std]** |
| Maintenance expense | £60/policy/yr, inflating 3.0%/yr | **[std]** |
| Claim management expense | £300/yr per claim in payment, inflating 3.0%/yr | **[std]** |
| Offset/guarantee effect | AP(y) = B(y) — amount-payable ratio 1.0 (offsets and guarantee assumed not to bite) | **[std]** (2) |
| Claim severity factor k | 1.0 (proportionate/rehabilitation claims not projected separately) | **[std]** (2) |
| Discount | PRA risk-free term structure for valuation [R7][REG-R1]; flat 3.0%/yr in the worked example only | rate **[std]** |

1. ONS national life tables are the only freely redistributable UK mortality source
   (Open Government Licence); population mortality is heavier than insured
   experience [REG-R32]. CMI assured-lives table *names* are public (e.g. AM92/AF92
   [REG-R24]) but current insured tables are Authorised-User-restricted [REG-R22].
   Active-life mortality is a minor decrement in IP; the ×100% factor is a
   placeholder to be replaced with portfolio experience.
2. Offsets, the minimum benefit guarantee, and proportionate benefits change the
   amount paid relative to the chosen benefit (spec, Contractual mechanics). The base
   model pays the full escalated benefit; portfolio calibrations should set
   AP/B < 1 or k < 1 from claims experience.

**[std] proxy claim inception rates** (annual, per mille of lives in H; male, OC1,
DP26; linear interpolation between pivot ages; pure placeholders):

| Age a | 30 | 35 | 40 | 45 | 50 | 55 | 60 | 64 |
|---|---|---|---|---|---|---|---|---|
| ι_a(a) ‰ | 1.0 | 1.3 | 1.8 | 2.6 | 4.0 | 6.5 | 10.0 | 14.0 |

**[std] proxy claim termination rates** (annual, by claim duration year since
payment inception; pure placeholders):

| Claim duration year | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Recovery ρ_a | 0.40 | 0.25 | 0.15 | 0.10 | 0.05 |
| Death in claim q_S_a | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 |

The declining-with-duration recovery shape mirrors the qualitative structure the CMI
publishes (duration-dependent termination rates [R1]); the IP11 "run-in" feature
(recovery rates *increasing* over the first weeks of claim for DP4/13/26 [R1]) is
not reproduced at this granularity — a monthly refinement point for table licensees.

**[std] lapse table** (annual rates from H; lives in S do not lapse — premiums are
waived and the benefit is valuable **[std]**):

| Policy year | 1 | 2 | 3–5 | 6+ |
|---|---|---|---|---|
| w_a(y) | 10% | 8% | 6% | 4% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1..T; T = 12 × (expiry_age − entry_age) = 360 (base cell); y = ceil(t/12); attained age a = entry_age + y − 1 |
| B(y), P(y), AP(y) | escalated benefit, premium, amount payable (£/month); B(1) = 2,000, P(1) = 35 **[std]** |
| j | escalation rate = min(max(RPI, 0), 0.10); snapshot 0.03 **[std]** |
| ι_m(a) | monthly claim (payment) inception rate = 1 − (1 − ι_a(a))^(1/12) **[std]** |
| q_H_m(a), w_m(y) | monthly active mortality and lapse, same annual-to-monthly conversion **[std]** |
| ρ_m(z), q_S_m(z) | monthly recovery and death-in-claim rates at claim duration z months (from the annual rate of the duration year containing z) **[std]** |
| s_S(z) | monthly in-claim survival = (1 − ρ_m(z)) × (1 − q_S_m(z)) (independent decrements **[std]**) |
| e_m(y), ec_m(y) | monthly maintenance and claim-management expense = 60/12 and 300/12, × 1.03^(y−1) **[std]** |
| v(t) | discount factor to time t (valuation: PRA risk-free curve [R7][REG-R1]; worked example: 1.03^(−t/12) **[std]**) |
| l_H(t), l_S(t, z) | state probabilities (state-variable table); l_H(0) = 1, l_S(0, ·) = 0 for an at-issue cell |

Dimensional check: ι, q, w, ρ are monthly probabilities (dimensionless); B, P, AP,
e are £/month; every cash flow below is £ per month per policy issued.

### Monthly processing order [std]

At month t (skip all steps from t > T; at t = T all cover and any claim in payment
terminate without value [S1][S3][S5][S7][S10]):

1. **Anniversary (BOM, months t = 13, 25, ...):** B(y) = B(y−1) × (1 + j);
   P(y) = P(y−1) × (1 + 1.5 × j) [S1][S2]. In-claim benefit escalates identically
   [S1][S2] — the same B(y) applies to lives in S.
2. **Premium income (BOM):** `PREM(t) = P(y) × l_H(t−1)`. Lives in S pay nothing
   (waiver [S5][S7][S10][S11]); lives in H still inside a deferred period pay
   normally (see Deferred-period mechanics).
3. **Transitions (EOM), from H** — order death, then lapse, then inception among
   survivors **[std]**:
   - `dth_H(t) = l_H(t−1) × q_H_m(a)`
   - `lps(t) = l_H(t−1) × (1 − q_H_m) × w_m(y)`
   - `n(t) = l_H(t−1) × (1 − q_H_m) × (1 − w_m) × ι_m(a)` (new claims at duration z = 1)
4. **Transitions (EOM), from S** — order recovery, then death **[std]**, per
   duration cohort z:
   - `rec(t, z) = l_S(t−1, z) × ρ_m(z)`
   - `dth_S(t, z) = l_S(t−1, z) × (1 − ρ_m(z)) × q_S_m(z)`
   - `l_S(t, z+1) = l_S(t−1, z) × s_S(z)`
   - `l_S(t, 1) = n(t)`
5. **State update:**
   `l_H(t) = l_H(t−1) × (1 − q_H_m) × (1 − w_m) × (1 − ι_m) + Σ_z rec(t, z)`
   (recovered lives return to H and are again exposed to inception **[std]**; see
   the linked-claims limitation below).
6. **Benefit outgo (EOM):** `BEN(t) = k × AP(y) × [l_S(t) − n(t)]` — i.e. paid to the
   surviving cohorts z ≥ 2 only (equivalently Σ_z l_S(t−1, z) × s_S(z)): benefit is
   monthly in arrears [S1], so new inceptions n(t) = l_S(t, 1), seeded at EOM t,
   receive their first payment at EOM t+1. (Including n(t) in BEN(t) would pay a
   full month's benefit at the instant of payment inception and break the
   inception-annuity equivalence in Active-lives valuation.) Whole-month
   convention **[std]**.
7. **Expenses (EOM):** `EXP(t) = e_m(y) × [l_H(t−1) + l_S(t−1)] + ec_m(y) × l_S(t−1)`.
8. **Discount** cash flows at v(t) and accumulate.

Net cash flow (insurer perspective): `CF(t) = PREM(t) − BEN(t) − EXP(t)`. Death and
lapse generate no payment (no death benefit, no surrender value [S4][S5][S7]; the
out-of-scope £5,000–£10,000 death benefits at LV=/Royal London [S3][S5] would add a
`dth × DB` term).

### Deferred-period mechanics

The contract pays after d weeks (26, base cell) of continuous incapacity, with
premiums payable through the deferred period and waived from benefit start (spec).
The model embeds the deferred period **in the inception basis**: ι is a *claim
payment* inception rate specific to DP26 — exactly the quantity the CMI publishes
per deferred period [R1] — so sickness spells that recover inside the deferred
period never leave H, and lives sick within the deferred period remain in H (still
premium-paying, matching the contractual waiver-from-payment-start convention
**[std]**, spec footnote 16). Consequences:

- No separate "sick, not yet in payment" state is needed; the d-week lag between
  onset and payment is absorbed into ι's calibration. A timing refinement (shifting
  inception cash flow impact by d weeks) is second-order at DP26 **[std]**.
- Dual deferred periods and sick-pay-linked NHS/teacher deferreds [S1][S3][S5][S7]
  [S10] would need spell-level modeling and are out of scope.
- **Linked claims limitation [std]:** contractually, a same-cause recurrence within
  52 weeks of payments stopping restarts payment without a new deferred period
  (spec). The base model returns recovered lives to H with the standard DP26
  inception basis, which understates short-horizon re-inception. Refinement: a
  post-recovery flag with a loaded ι for 12 months; not specified further here.

### Claims-in-payment valuation (disabled-life annuity)

A claim in payment is valued as a disabled-life annuity: expected present value of
the escalating benefit until recovery, death or expiry — the "claim annuity values"
the CMI Rate Table Tool produces for subscribers [R5]. For a claim at duration z0
months, attained age a0, with T_rem months to expiry:

    a_dis(a0, z0) = Σ_{m=1}^{T_rem} [ Π_{i=1}^{m} s_S(z0 + i − 1) ] × k × AP(y(m)) / AP(y(0)) × v(m)

so that claims-in-payment BEL outgo per £1/month of benefit in payment is a_dis, and
the cell's benefit liability is AP × a_dis + the claim-expense annuity (same
survival, ec_m in place of AP). Escalation enters through AP(y(m)) (step-ups at
policy anniversaries [S1][S2]); the annuity truncates at expiry — payments stop at
the policy end date [S1][S3][S5][S7][S10].

### Active-lives valuation

Active-life BEL cash flows are steps 1–8 run from the valuation date: premium income
from l_H, benefit outgo from claims yet to incept (each n(t) seeds a new duration
cohort), and expenses. Equivalently, the benefit side can be written as
`Σ_t v(t) × n(t) × [k × AP × a_dis(a(t), 0-month equivalent)]` — the inception-annuity
decomposition of the same multi-state projection.

**Alternative: inception-annuity method [brief].** The historical alternative prices
each year's claim cost as (inception rate) × (disabled-life annuity at claim start)
without tracking in-claim cohorts through time — adequate for premium rating, but it
cannot roll claims-in-payment forward or produce per-period BEL cash flows, which is
why the multi-state formulation is the reference structure. The research file
records the pre-CMIR 12 history (Manchester Unity sickness-rate basis;
inception-annuity vs multi-state reserving) as [unverified] textbook knowledge — no
public IFoA source was retrieved; the CMIR 12 → IPM 1991-98 → IP11 multi-state
lineage itself is verified at landing-page level [R4].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK IP
policyholder-behavior study was retrieved.

- **Base lapse [std].** w_a(y) per the table above; monthly
  w_m = 1 − (1 − w_a)^(1/12). Applied to H only; lives in S never lapse (premiums
  waived, benefit in payment) **[std]**.
- **Premium-shock lapse [std].** With escalation on, premiums rise 1.5 × j each
  year; the model multiplies lapse by
  `M_esc(y) = 1 + 2 × max(0, 1.5 × j(y) − 0.05)` in anniversary years (lapse
  response to premium increases above 5%; e.g. j at the 10% cap gives 1.5 × 0.10 =
  15% premium growth and M_esc = 1.2). Contract anchor: sampled insurers let policyholders
  decline escalation increases, with the option lapsing after consecutive
  refusals — two consecutive cancelled increases end the option at Royal London
  [S5]; declining three consecutive increases removes it at Cirencester [S11];
  declines are modeled as lapse of the
  escalation margin only at portfolio level — the base single-cell model keeps
  escalation always-on and uses M_esc as the aggregate proxy.
- **Economic-cycle morbidity link [std note].** Claim inceptions are widely believed
  to rise (and recoveries to slow) in recessions — job insecurity raises claim
  propensity on an own-occupation definition. No sampled document or public CMI
  output quantifies this; it is recorded here as a scenario overlay
  `ι × M_cycle`, `ρ / M_cycle` with M_cycle = 1 in base **[std]**, not as a
  calibrated assumption.
- **GIO take-up, alterations, career breaks:** held at zero (spec: out of scope).

---

## Worked example

Claims-in-payment recursion for the base cell's level-cover variant **[std]** (the
escalation step falls outside the 3-month window shown): a claim in payment from
duration z = 0, benefit AP = B = £2,000/month, duration-year-1 proxy terminations
(ρ_a = 0.40, q_S_a = 0.03 **[std]**), discount 3.0%/yr flat **[std]**.

Monthly factors (derived): ρ_m = 1 − 0.60^(1/12) = 0.041675;
q_S_m = 1 − 0.97^(1/12) = 0.002535; in-claim survival
s_S = 0.958325 × 0.997465 = 0.955895; v = 1.03^(−1/12) = 0.997540.

| Month m | l_S start | Recoveries ρ_m × l_S | Deaths (1−ρ_m) q_S_m × l_S | l_S(m) = l_S × s_S | Benefit 2,000 × l_S(m) | v^m | PV |
|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 0.041675 | 0.002429 | 0.955895 | 1,911.79 | 0.997540 | 1,907.09 |
| 2 | 0.955895 | 0.039837 | 0.002322 | 0.913735 | 1,827.47 | 0.995086 | 1,818.49 |
| 3 | 0.913735 | 0.038080 | 0.002220 | 0.873434 | 1,746.87 | 0.992638 | 1,734.01 |

Three-month PV of benefit outgo: £5,459.59 per claim in payment. Trace, month 1:
survival s_S = (1 − 0.041675) × (1 − 0.002535) = 0.955895; expected benefit paid at
EOM = 2,000 × 0.955895 = £1,911.79 (in-arrears convention: exits during the month
receive nothing under the whole-month simplification **[std]**; contractually they
would receive a daily pro-rated amount [S1][S3][S10]); PV = 1,911.79 × 0.997540 =
£1,907.09. Claim expense follows the same survival column at ec_m = 300/12 = £25.00
per month **[std]**. On the active-lives side, the same conventions give month-1
premium income P × l_H(0) = £35.00 and expected new inceptions
n(1) ≈ ι_m(35) = 1 − (1 − 0.0013)^(1/12) = 0.000108 — each seeding this in-claim
recursion at z = 1.

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` (what the items are) and
`uk/regulatory/technical-notes.md` (how to compute them); this section states only
what is specific to individual income protection and cross-references those files by
section name rather than restating them. [REG-R#] resolves against the shared UK
numbering, which now runs **R1–R120**, with **R50–R52, R74–R76 and R121–R133 unused
by design** — the research streams were allocated parallel blocks and the tails left
spare, so an unused number is not a missing entry. Twelve documents were independently
numbered by more than one stream — eleven twice, and SS15/16 three times; the
duplication is recorded, not renumbered, and only the canonical number is cited here
(the duplication table is in
`uk/regulatory/sources.md`). Product-local [S#]/[R#] tags continue to resolve against
`sources.md` in this directory.

**Terminology, stated before anything else.** The file names in `uk/regulatory/`
mirror `us/regulatory/` for structural parity across the library and for no other
reason: **the UK has no "statutory accounting" in the U.S. sense** — no NAIC-style
solvency-purpose accounting basis, and no annual statement blank that is also the
ledger. This product is measured on three separate things: the **Solvency UK
regulatory balance sheet** (PRA Rulebook — a prudential supervisory return, not a set
of accounts) [REG-R39][REG-R1]; the **statutory accounts** (Companies Act accounts
under FRS 102 + FRS 103, or UK-adopted IFRS 17) [REG-R103][REG-R105][REG-R99][REG-R106];
and **tax**, which is not a liability measurement at all but a computation *from the
accounts* with the Finance Act 2012 overlay [REG-R17][REG-R18]. Where this section
says "the accounts" it means the second; "Solvency UK" means the first.

### Contract classification and reporting

- **RAO class is settled and is the reason this contract exists in the form it does.**
  Regulated Activities Order Schedule 1 Part II **Class IV, permanent health**
  [R6][REG-R14] — contracts "expressed to be in effect for a period of not less than
  five years" (or to normal retirement age) and non-cancellable by the insurer except
  in contract-specified special circumstances. Every sampled product satisfies it
  [S2][S4][S9][S11], and the 5-year minimum term in the spec is the legal floor, not a
  marketing choice. Note the asymmetry with conduct regulation: prudentially this is
  long-term Class IV business, but distribution runs under FCA **ICOBS** as pure
  protection, not COBS [R9][REG-R11].
- **The Solvency UK line of business is decided by the technical basis, not the product
  label.** TPFR 26.2: assignment "must reflect the **nature of the risks**… The
  **legal form** of the obligation **is not necessarily determinative**"; TPFR 26.3
  sends health obligations pursued on a similar technical basis to that of long-term
  insurance business to the long-term lines [REG-R41]. The Glossary chain is settled
  for this product: a contract paying financial compensation arising from illness,
  accident, disability or infirmity is a **health insurance obligation** (limb (2)),
  and specifically an **income protection insurance obligation** — limb-(2)
  compensation other than compensation for medical treatment or care [REG-R42].
  Written on a long-term technical basis it is **SLT health**, **line of business 29**.
  An annually-renewable or group scheme instead lands in the general lines (LoB 2 / 14)
  and is charged by a factor formula rather than by scenario. Two honest caveats: **no
  retrieved source gives any test for "similar technical basis to that of long-term
  insurance business"** [REG-R41], so two firms writing identical individual IP books
  can legitimately land in different lines and therefore in different SCR sub-modules
  and different reporting rows; and **the numbered line-of-business list itself sits in
  the unretrieved Annexes to the SCR – Standard Formula Part** [REG-R73], so the LoB-29
  mapping is carried as the drafter's inference from TPFR 26.2/26.3 and the Annex 1
  definitions, not as a quotation.
- **PRA three-digit product codes** (the appendix to the IR.14.01 instruction file, the
  former SS36/15 content and the single best map from UK product taxonomy to regulatory
  reporting) [REG-R89]: **494** income protection, guaranteed premiums — the
  representative chassis; **504** reviewable premiums, the documented variation
  [S1][S4][S6][S10]; **514** single premium, not a design in this library; **524 income
  protection claims in payment**; and **480** income protection CWP / **481** income
  protection Holloway accounts UWP for the participating friendly-society variation
  [S11][S12]. Group codes 564 / 574 are out of scope. **The modelling consequence is
  direct:** the `status` attribute in *Model point attributes* above is not merely a
  state flag but a **reporting key** — active cells and claims-in-payment cells report
  under different codes, so contract counts, written premiums, claims paid, gross best
  estimate and capital at risk must all be producible separately for the two
  populations.
- **Templates this product drives, and the rows that are its own.**
  - **IR.12.01** life technical provisions applies; the **unit-linked rows
    R0300/R0302/R0304 do not** — nothing here is linked [REG-R89]. Surrender value is
    collected as a **disclosure** item, not as a constraint [REG-R89], and is
    identically zero for this product at any time [S4][S5][S7].
  - **IR.12.04** best-estimate assumptions is where this product has rows of its own:
    **R0570** inception male, **R0610** inception female, **R0650** termination male,
    **R0690** termination female, each a total row followed by three subcategory rows
    spaced 40 apart for the largest three categories by number of policies [REG-R89].
    Three product-specific consequences. (a) The template offers **three subcategory
    slots** while this product's rate structure is sex × deferred period × occupation
    class — five deferred periods and four occupation classes [R1] — so a firm must
    choose which dimension to disclose, and **the retrieved instructions do not say
    which**. (b) Column **C0080 requires the named underlying table** with the basis
    expressed as a percentage of it [REG-R89]; the IP11 table *names* are public
    (`IP11 {M/F} DP{d} OC{n} {Inc/Rec/Dth}` [R1]) but the values are CMI
    Authorised-User-restricted [R2][R3][R5][REG-R22], and the reference basis in these
    notes is a **[std] proxy that is not a named table at all** — a reference
    implementation cannot populate C0080 honestly, and no table name is invented here.
    (c) There is **no income-protection row in either the lapse/surrender block or the
    renewal-expense unit-cost block**: the lapse rows are with-profits endowment,
    unit-linked endowment, level term, decreasing term and investment bond by duration
    band, and the unit-cost rows are with-profits endowment, unit-linked endowment,
    term assurance, investment bond, with-profits individual pension, unit-linked
    individual pension and annuity [REG-R89]. **Where an IP lapse assumption or an IP
    per-policy renewal expense is reported is not settled by the retrieved
    instructions.** The credibility guideline — experience need not be shown below
    **200 claims per annum** for an individual line [REG-R89] — bites hard once an IP
    book is split by sex and deferred period.
  - **IR.14.01** life obligations analysis, per product code, per fund, per line of
    business: contracts in force, new contracts, gross written premiums, **gross claims
    paid**, gross best estimate and **capital at risk "as defined in Solvency Capital
    Requirement – Standard Formula 7.8 and 7.10"** [REG-R89]. Two IP-specific hooks:
    C0070 claims paid currently **includes claims management expenses**, and **PS18/26
    removes them from that definition from the 31 December 2026 reference date**
    [REG-R87 ¶2.41] — material here because the model carries an explicit per-claim
    management expense (£300/yr per claim in payment **[std]**); and C0190 engages the
    **disability limb** of the capital-at-risk definition, which is unresolved (see
    *Own funds, ring-fenced funds and the MCR* below).
  - **IR.26.04 SCR health underwriting risk** applies. **IR.26.03 SCR life underwriting
    risk does not** — the life module does not reach this product at all [REG-R84].
  - **IR.12.05 / IR.12.06** (with-profits value of bonus; with-profits liabilities and
    assets) bite only the **participating** forms — the Holloway/CWP variants under
    codes 480/481 — and then only where the firm's with-profits net best estimate
    exceeds **£500 million**, completed per ring-fenced fund that is also a with-profits
    fund [REG-R90]. The guaranteed-premium non-profit chassis specified here triggers
    neither.
  - **IRR.22.02 / IRR.22.03 and MALIR 1–7** apply only where the claims-in-payment
    element is actually placed in a matching adjustment portfolio [REG-R91].
  - **IR.05.10** excess capital generation is scoped at entity level on life premiums
    excluding unit-linked above £1bn [REG-R84][REG-R90] — a firm threshold, not a
    product trigger.

### Technical provisions

- **Contract boundary — guaranteed premiums.** The boundary is **the full term to the
  selected expiry age**. TPFR 3.3's three exclusion triggers do not engage: the insurer
  has no unilateral right to terminate, no right to reject premiums, and no repricing
  right — premiums are guaranteed level apart from escalation-option increases
  [S1][S3][S5][S7]. The residual clause that premiums may change "for reasons such as
  tax or legislation" [S1][S3][S5][S7] cannot satisfy TPFR 3.7, which makes the test
  extreme: premiums fully reflect the risks only "where there is **no circumstance**
  under which the amount of the benefits and expenses payable under the portfolio
  exceeds the amount of the premiums payable" [REG-R41]. All 360 months of the base
  cell are inside the boundary.
- **Contract boundary — the reviewable-premium variation, where the long-term carve-out
  does the work.** The documented variation is fixed for 5 years and then reviewed with
  no contractual cap [S1][S4][S6][S10]. TPFR 3.3(3) assesses the "premiums fully reflect
  the risks" limb **at portfolio level**, *except* for long-term insurance business
  "where an individual risk assessment of the obligations relating to the insured person
  of the contract is carried out at the inception of the contract and that assessment
  cannot be repeated before amending the premiums or benefits", where the firm "must
  assess **at the level of the contract**" [REG-R41]. Individual IP is medically and
  financially underwritten at outset [S1][S3][S5][S7] and cannot be re-underwritten at a
  review, so **the boundary is not cut at the 5-year review — it runs to the end of the
  term**, exactly as on the guaranteed chassis. TPFR 23.1 then makes a reviewable-rate
  reinsurance treaty inherit that full-term boundary [REG-R41].
- **Contract boundary — claims in payment.** A different question: recognition is
  already complete and there are no future premiums, the waiver having stopped them at
  benefit-payment start [S5][S7][S10][S11]. The boundary is the remaining claim payment
  period, truncating at the policy end date [S1][S3][S5][S7][S10].
- **Cash flows in scope.** TPFR 13.1 requires **eight** streams [REG-R41]. Live for this
  product: benefit payments; expenses; premiums and cash flows resulting from them; and
  **payments between the firm and intermediaries** — which makes **commission and
  clawback an in-scope best-estimate cash flow**, not an expense-loading convention.
  **The projection above has no commission stream at all**; that is a stated gap, not a
  claim of completeness. Not live: benefits in kind (the sampled rehabilitation support
  services and Vitality Recovery Benefit are out of scope [S3][S10]); payments to
  investment firms (nothing linked); salvage and subrogation; and item (8),
  policyholder-charged taxation — IP benefits are free of income tax to the individual
  under current law [S4][S7][S11] and no policyholder fund tax arises on non-BLAGAB
  protection [REG-R17][REG-R18]. Shareholder corporation tax is **not** a best-estimate
  cash flow; it enters through deferred tax under the Valuation Part [REG-R39].
- **Expenses, and the two-basis problem.** TPFR 16.1 names four categories —
  administrative, investment management, **claims management** and acquisition — each
  including allocated overheads, allocated "in a realistic and objective manner and on a
  consistent basis over time" (16.2) [REG-R41]. Then **TPFR 16.4**: "Expenses must be
  projected on the assumption that the firm will write new business in the future" — so
  the £60/policy/yr maintenance and £300/yr per-claim-in-payment management figures
  above are **going-concern** unit costs, not run-off unit costs with overheads
  re-spread over a shrinking book. That sits in unreconciled tension with the risk
  margin's reference undertaking, which "assumes no new obligations" after the transfer
  (TP 4B.1(5)) [REG-R1]; both are correct as printed, a model must carry **two expense
  bases**, and **no retrieved source explains how the reference undertaking's expenses
  should be set given that tension**. Nothing in the rules prescribes an inflation index
  (RPI, CPI or national average earnings) or an expense-inflation rate; the 3.0%/yr flat
  assumption above is **[std]**. The administrative/claims-management split is not
  cosmetic on this product — a claim in payment can run for decades — and it drives both
  the IR.14.01 C0070 change from 31 December 2026 [REG-R87 ¶2.41] and IR.12.04 **R2090**,
  which "**includes claims management expenses but excludes investment management
  expenses**" [REG-R89]. A model that nets claim-management cost into benefit outgo can
  produce neither.
- **Is the best estimate negative? It splits by cell, and the split is this product's
  own.** The **active-life** cell is routinely negative on a guaranteed-premium
  full-term boundary — the present value of future premiums exceeds the present value of
  future claims and expenses, the same arithmetic as term assurance — and **nothing
  floors it on the Solvency UK ledger**: TP 3.1 contains no floor, no minimum and no
  reference to a surrender value or account value; TP 2.2 requires a **transfer value**,
  which for a profitable portfolio is legitimately negative before the risk margin; the
  risk margin is non-negative by construction so it offsets but does not floor; and the
  Solvency I floor (INSPRU 1.2.62R) was **expressly not carried over**, INSPRU 1.2 not
  applying to a Solvency II firm [REG-R1][REG-R39][REG-R41][REG-R115]. There is in any
  event no surrender value here to floor against [S4][S5][S7]. The
  **claims-in-payment** cell can never be negative: no premiums inside its boundary,
  only outgo. Three consequences: the two cells must be aggregated **with the sign
  preserved**; the UK GAAP floor is applied downstream, never inside the projection; and
  a negative active-life best estimate feeds own funds directly through the
  reconciliation reserve, which "may be positive or negative" (Own Funds 3C.2)
  [REG-R77].
- **The options and guarantees this design actually contains** — TP 9.2(1) requires
  their value to be taken into account [REG-R1], and the list is short and contains no
  financial option on a fund:
  - the **escalation option** — RPI, floored at 0 and **capped at 10%/yr**, premium
    rising 1.5× the benefit increase, increases continuing in claim [S1][S2]. The cap
    makes the payoff **asymmetric in RPI**, so the single deterministic 3.0%/yr path
    used above **[std]** does not value it;
  - the **minimum benefit guarantee** of £1,500/month conditional on working ≥16 h/week
    at incapacity [S1][S2] and the **90% over-insurance tolerance** [S1][S5] — floors on
    the amount payable, biting only where earnings have fallen since outset;
  - the **waived deferred period on linked claims** within 52 weeks of payments stopping
    [S1][S3][S5][S7][S10][S11] — a benefit enhancement contingent on claim history, i.e.
    path dependency, which **TPFR 15.1** requires to be reflected explicitly or
    implicitly ("dependency of cash flows on circumstances prior to the date of the cash
    flow") [REG-R41]. The base model's *Linked claims limitation* above does not reflect
    it and says so;
  - a **policyholder right to decline an escalation increase**, present on some sampled
    contracts — the option ending after two consecutive refusals at Royal London [S5] or
    three at Cirencester [S11] — but **no retrieved source records such a term for the
    Aviva escalation design the composite adopts**, so this is a variation flag rather
    than a feature of the representative design; where it is present it is a policyholder
    option, not insurer discretion (see the lapse discussion below);
  - guaranteed insurability options, alterations and career breaks — held at zero, spec,
    out of scope.
- **Do they force a stochastic valuation? Not in the with-profits sense, but the
  analysis is not optional.** TPFR 19.4–19.5 requires the firm to analyse the extent to
  which the present value depends on **expected future outcomes and on scenario
  deviation from the expected outcome**, and to use a method reflecting those
  dependencies where it does [REG-R41]. For this product the two candidates are the
  10% escalation cap and the economic dependence of claim inceptions and recoveries —
  the `M_cycle` overlay in *Policyholder behavior modeling*, which is **[std]** and
  deliberately uncalibrated. The research marks this product **conditionally** in scope
  for a scenario-dependent method rather than squarely; a deterministic run with an
  explicit RPI-cap sensitivity is a defensible proportionate method under TPFR 27, but
  the demonstration is the firm's and is not made here. Separately, **TPFR 11.1**
  requires an analysis of past policyholder behaviour and a prospective assessment, and
  closes: "The likelihood shall **only** be considered to be independent of the elements
  referred to in (1) to (4) where there is **empirical evidence** to support such an
  assumption" [REG-R41] — that is the rule against a flat static lapse table, and the
  **[std]** table above has no such evidence behind it (no public UK IP lapse study was
  retrieved). The `M_esc` premium-shock multiplier is the beginning of the required
  dynamic function, not its discharge.
- **The experience-basis rules bite this product harder than any other in the library.**
  TPFR 7.1 allows firm-specific information only where it **better reflects the
  portfolio's characteristics** than non-firm-specific information, or where a prudent,
  reliable and objective calculation is impossible without it [REG-R41] — the rule that
  decides when own experience may override an industry table, and the industry table
  here is the CMI's and is subscriber-restricted [R1][R2][R3][R5][REG-R22]. TPFR 4.4
  adds that a firm using **external data** must know its **origin** and the assumptions
  and methodologies used to process it, and must demonstrate that those **reflect the
  characteristics of its own portfolio** — which is the condition a firm must discharge
  to use IP11 at all, and inside which the WP136 indicative inception adjustments
  [R1][R3] sit. TPFR 4.1–4.3 require data to be complete enough to "identify trends" per
  homogeneous risk group; TPFR 5.1 requires a documented **limitations register** with a
  remediation plan and a named responsible function — the natural home for the proxy
  tables above.
- **Technical provisions as a whole are unavailable.** TPFR 22.2 declares three
  categories non-replicable: cash flows depending on the likelihood that policyholders
  exercise contractual options **including lapses and surrenders**; cash flows depending
  on the level, trend or volatility of **mortality, disability, sickness and morbidity
  rates**; and **all** expenses incurred in servicing the obligations [REG-R41]. This
  product is nothing but the second and third categories, so the whole-contract TP-as-a-
  whole route is closed and the reporting rows for it (IR.12.01 R0025/R0026/R0030) stay
  empty [REG-R89].
- **Matching adjustment — the eligible-element route, and this is one of only two
  products in the library that reach it.** The whole contract cannot qualify: MA 2.2
  requires **no future premium payments** and permits only longevity, expense, revision,
  mortality or **recovery time** risk [REG-R2], and an active IP policy has both future
  premiums and inception risk. But **MA 1.2** defines an *eligible element* to include
  **the in-payment element of an income protection policy**, where it can be organised
  and managed separately under IRPR regulation 4(6) and would otherwise be MA-eligible
  but for forming part of a non-complying contract; and **MA 2.5 disapplies the
  no-future-premiums condition for that limb** [REG-R2][REG-R44]. SS7/18 adds three
  things a model owner needs: **recovery time risk** — "the risk that policyholders in
  receipt of income protection payments take longer to recover from sickness than
  expected" — is a permitted underwriting risk; in-payment claims under **both group and
  individual** IP policies may sit in an MA portfolio where not subject to future
  premiums; and **there is no exposure limit on recovery time risk**, in contrast to the
  5% cap on the mortality-stress increase [REG-R8]. So the `a_dis` disabled-life annuity
  computed in *Claims-in-payment valuation* above is precisely the portion a UK insurer
  may discount at risk-free + MA — the mechanical content of the [R8][REG-R2] statement
  the spec already carries. Two limits, both recorded rather than papered over: **how a
  single liability cash flow vector is allocated between MA and non-MA portfolios when
  only an eligible element qualifies is not prescribed by any retrieved source**, so
  whether and how expected *future* inceptions from the active-life cell are excluded
  from the MA portfolio until they incept is open; and SS7/18 states that outside the
  eligible-element cases the PRA regards **no notional splitting** as compatible with MA
  2.3 [REG-R8], so the split cannot simply be assumed convenient. Where an MA portfolio
  does exist, **MALIR 3** requires **monthly liability cash flows out to month 600**,
  gross of reinsurance, split level/fixed-escalation, **inflation-linked**, expenses and
  other — and a contract with **any** inflation linkage is reported **wholly** as
  inflation-linked [REG-R91], which for an RPI-escalating IP claim annuity [S1][S2] is
  the whole of it.
- **Discounting.** The relevant risk-free term structure is **published by the PRA, not
  computed by the firm** [REG-R44][REG-R54][REG-R55]; **no risk-free rate, fundamental
  spread, volatility adjustment or ultimate forward rate appears anywhere in this
  library**, because the monthly technical-information spreadsheets were not opened
  [REG-R54]. The flat 3.0%/yr rate in the worked example is **[std]** and is an
  arithmetic device, not a valuation basis. The GBP **last liquid point was retained at
  50 years** for 1 January 2026 implementation [REG-R56]; cash flows here stop at the
  policy end date [S1][S3][S5][S7][S10], so the longest contract this specification
  permits — entry age 18 (entry band [S1][S2][S6][S9]) to expiry age 70 (expiry band
  [S2][S4][S6][S7][S9]) — runs 52 years, of which
  only the last two fall beyond the LLP, while the base cell (35 → 65, 30 years) is
  entirely inside it (**[std, derived]** — arithmetic from the spec's own entry and
  expiry bands against the cited LLP). Extrapolation is a boundary case for this
  product, not a driver.

### The risk margin

Concept, the thirteen reference-undertaking assumptions and the formula are in
`uk/regulatory/statutory-accounting-and-capital.md`, "The risk margin", and
`uk/regulatory/technical-notes.md`, "The risk margin". Cost of capital **4%**, tapering
factor **λ = 0.9** for long-term obligations, floored at 0.25 [REG-R1][REG-R4] — as the
spec already records. Three things this product's shape changes:

- **The run-off has two humps and the second one is long.** The formula needs a
  projected series `SCR(0), SCR(1), SCR(2), …` for the reference undertaking [REG-R1].
  Here that is the active-life inception exposure, declining to zero at the expiry age,
  *plus* the recovery-time exposure of claims already in payment. A claim incepting at
  early duration on the base cell can run 30 years; a claim incepting near expiry cannot,
  because all cover and claim payments cease at the policy end date
  [S1][S3][S5][S7][S10]. **That truncation is what stops the tail** — an untruncated
  disabled-life annuity overstates the best estimate and every `SCR(t)` behind it, and
  the error compounds through the risk margin.
- **The reference undertaking applies none of the matching adjustment** (TP 4B.1(13))
  [REG-R1]. For this product that strips the MA from the very element — claims in
  payment — that earned it, so the risk margin is struck on a materially higher-liability
  basis than the balance sheet it sits on. The reference undertaking also carries **no
  loss-absorbing capacity of deferred taxes** and excludes **interest rate risk**, and
  selects assets so as to minimise its own market-risk SCR, so the risk margin **cannot
  be produced by re-running the firm's own SCR on a different curve**.
- **There is no UK risk-margin simplification hierarchy to fall back on.** Delegated
  Regulation Article 58 was **not restated** into Solvency UK; the TPFR Part's
  "SIMPLIFICATIONS" heading introduces Chapter 27 (proportionality) only, and IRPR
  regulation 7C preserves a PRA power that has not been exercised in the Technical
  Provisions Parts [REG-R41][REG-R49][REG-R44]. Any driver-based `SCR(t)` proxy for this
  product rests on TPFR 27.4 alone, and **no rule text sanctions any specific proxy**.

### SCR — the modules that bite

Full mechanics, stresses and correlations are in `uk/regulatory/technical-notes.md`,
"The standard formula SCR"; the full-revaluation / formulaic split is in
`uk/regulatory/statutory-accounting-and-capital.md`, "What a 'scenario' means, and which
stresses need a full revaluation".

**The life underwriting module does not reach this product at all.** SCR-SF 3.2A applies
the **life** module to life obligations **other than health insurance obligations** and
the **health** module to health insurance obligations — the health module is **not a
residual; it takes precedence** [REG-R62]. This contract is a health insurance
obligation, so chapter `3B` is out entirely: **no `3B1` mortality +15%, no `3B7` life
catastrophe +0.15pp, no `3B5` life revision +3%, no `3B6` life lapse.** Its mortality
exposure runs through `3C9` and its lapse exposure through `3C16`. Getting this wrong
puts the product in the wrong module *and* the wrong reporting template — IR.26.03
instead of IR.26.04 [REG-R84].

| Sub-module | Stress | Full BEL revaluation? | For this product |
|---|---|---|---|
| Health mortality `3C9.1` | **+15%** instantaneous permanent increase in the mortality rates used in the TP calculation, only where TP without risk margin increases (`3C9.2`) | **Yes** | Two mortality decrements exist here — `q_H` on actives and `q_S` in claim. Higher claimant mortality **shortens** the disabled-life annuity and reduces TP, so the `3C9.2` filter excludes those cells; the active-life exposure is small (a death in H removes a premium payer and a future claim alike). Wording identical to the life stress `3B1` |
| Health longevity `3C10.1` | **−20%** instantaneous permanent decrease | **Yes** | The mirror image, and the one that matters: lower claimant mortality **lengthens** claims in payment. Applies only where a decrease in mortality increases TP |
| Health disability-morbidity `3C11.1` → income protection scenario **`3C13.1`** | One combined instantaneous permanent scenario: **+35%** in disability and morbidity rates for the following 12 months; **+25%** in the years thereafter; **−20%** in recovery rates **where those rates are lower than 50%**; **+20%** in persistency rates **where those rates are equal to or lower than 50%** | **Yes** | The dominant sub-module. `3C11.1` is the **sum** of the medical-expense and income-protection charges, not a correlated aggregation, and the medical-expense leg is nil here. Note the asymmetric thresholds ("lower than" vs "equal to or lower than") and that all four limbs are one scenario, not a maximum. **Unlike a lump-sum contract, this product has real recovery and persistency rates, so the conditional limbs are capable of biting** — but whether each does turns on their level. On the **[std]** proxy termination table above every annual recovery rate (0.40 → 0.05) is below 50%, so the −20% limb applies at every duration; the in-claim survival implied by that same table (0.58 in duration year 1 rising to 0.92 at 5+) exceeds 50% throughout, so on those numbers the +20% limb is vacuous. **The retrieved rule text does not define "persistency rate" for this purpose and no retrieved source supplies a definition**, so whether it means in-claim survival, its complement, or a policy-persistency measure is open and the answer changes which limb bites. Contrast the *life* stress `3B3.1`, which has no conditionality and no persistency limb |
| Health expense `3C14.1` | **+10%** in the amount of expenses **and +1 percentage point** in the expense inflation rate | **Yes** | Hits both streams — per-policy maintenance and per-claim management. Identical to the life expense stress `3B4.1` |
| Health revision **`3C15.1`** | **+4%** instantaneous permanent increase in the amount of annuity benefits, on annuity obligations whose benefits could increase from changes in **inflation**, the legal environment or the state of health of the insured | **Yes** | **A genuine charge here, and not one a pension annuity carries.** The life version `3B5.1` is 3% and has **no inflation trigger**; the health version is 4% and adds one, and an RPI-escalating IP claim annuity [S1][S2] is squarely in scope |
| SLT health lapse `3C16` | The **highest** of: up, `3C16.2` **+50% relative** in option exercise rates with increased rates capped at 100%; down, `3C16.3` **−50% relative**, decrease capped at **20 percentage points**; mass, `3C16.6` a flat **40%** discontinuance | **Yes, three runs** | Direction below. **There is no 70% mass-lapse limb anywhere in the health module** — the `3B6.6(1)` RAO class VII limb has no health counterpart |
| Health catastrophe `3C17`–`3C20` | `SCR_healthCAT = sqrt(SCR_ma² + SCR_ac² + SCR_p²)`, **uncorrelated** | **No — factor**, but the pandemic leg needs a valuation this projection does not produce | Mass accident `3C18` reaches all health obligations other than workers' compensation. Accident concentration `3C19` is scoped by `3C19.3` to workers' compensation and **group** income protection — it does not reach this library's individual design. Pandemic `3C20.1` = `0.000075 × E + 0.4 × Σ_c (N_c × M_c)`, both factors verified in the rule itself; `E` is the income protection pandemic exposure, defined by `3C20.2` as the value of benefits payable on **permanent** work disability, taken for recurring benefits as the best estimate **assuming the person is permanently disabled and will not recover** — the projection above recovers claimants on ρ and produces no such quantity. `N_c` (medical-expense insured persons) is nil here. **The Annex XVI inputs (`r_s`, `x_e`, `H_h`) were not retrieved by any stream, so the health catastrophe charge cannot be computed from this library's material even though its structure is known** [REG-R73] |
| NSLT health premium and reserve `3C2.1` | 3-sigma factor formula on premium and claims-provision volumes; segment 2, "income protection insurance and proportional reinsurance", `sigma_prem` **8.5%**, `sigma_res` **14%** (`3C4`) | **No — factor** | Reaches an **annually-renewable or group** IP contract, not the full-term individual design specified here |
| Interest rate `3D5` / `3D6` | up and down | **Yes, twice** | The claims-in-payment annuity supplies the duration; rebuild the curve, revalue **assets and** the best estimate, take the higher direction, summed across currencies within each direction |
| Spread on a matching adjustment portfolio `3D25` | stress the assets **and recalculate technical provisions for the impact on the amount of the MA**, via a fundamental-spread uplift with a credit-quality-dependent reduction factor | **Yes** | Only where the claims-in-payment element is actually placed in an MA portfolio. The ordinary non-MA spread stress `3D17` is asset-side only |
| Counterparty default type 1 `3E13` | factor on reinsurance recoverables, cash at bank, derivatives, guarantees | **No — factor** | UK protection is heavily reinsured, so this is the dominant counterparty charge. It sits alongside the **TPFR 24.4 loss-given-default floor of 50%** on the counterparty-default adjustment inside the best estimate — "must not be assessed at lower than 50% of the amounts recoverable … unless there is a reliable basis for another assessment", and **what counts as a reliable basis is not settled by any retrieved source** [REG-R41] |
| Operational `5.4(4)` | 0.45% technical-provisions leg | **No — factor** | The `0.25 × Exp_ul` unit-linked-expense leg (`5.4(1)`) is nil — no unit-linked business |
| **LACTP `Adj_TP` (`6.3`)** | — | **Not reached** | There are **no future discretionary benefits** on the guaranteed-premium non-profit chassis — no bonuses, no reviewable charges, no MVRs (*Assumption inputs*, (b)) — so `Adj_TP` is capped at zero, `BSCR = nBSCR`, and **one SCR run suffices**. Live only on the participating Holloway forms |
| LACDT `Adj_DT` (`6.4`) | change in deferred taxes on an instantaneous loss of `BSCR + Adj_TP + SCR_operational` | Balance-sheet revaluation | An **increase in deferred tax assets** arising from that loss **must not be utilised**; the transitional permitting otherwise ran only to **30 December 2025**, is still printed in the 05/08/2026 Rulebook view, and **no PRA instrument confirming its expiry or extension was retrieved** — treat it as expired for a current-date calculation and flag it [REG-R62] |

Equity, property and concentration are asset-side and reach this product only through
whatever backs the liability; there is no linked fund, no account value and no
policyholder investment choice [S4][S5][S7]. Currency risk `3D32` also revalues any
FX-denominated best estimate, which for a GBP-only book is nil.

**Lapse direction — the classic error, stated carefully.** `3C16.2` and `3C16.3` each
carry a **directional filter** [REG-R62]: the **up** scenario applies **only to relevant
options for which exercise would *increase* technical provisions without the risk
margin**; the **down** scenario **only where exercise would *decrease*** them. The test is
on the effect of *exercise*, applied per policy — and it is **not** the same test as
whether a product is "lapse-supported" in the pricing sense. That is where the error is
made. For this product:

- **Claims in payment take no lapse charge at all.** While a claim is in payment there is
  no discontinuance right to exercise: premiums are waived [S5][S7][S10][S11] and there
  is no surrender or cash-in value at any time [S4][S5][S7]. No relevant option under
  `3C16.4`, therefore no `3C16` charge on those cells.
- **The active-life cell is where the filter runs, and its answer moves with duration.**
  A guaranteed level premium set against a rising inception rate (the proxy ι rises from
  1.0‰ at age 30 to 14.0‰ at age 64 **[std]**) makes the cell profitable early and
  expensive late. Where the cell's best estimate is **negative**, discontinuance takes it
  toward zero — there being no surrender value to pay — and therefore **increases**
  technical provisions, routing the policy into the **up** scenario; where it has turned
  **positive**, discontinuance **decreases** them and the **down** scenario applies.
  *That mapping is a derivation from the `3C16.2`/`3C16.3` filter text and the sign of
  this product's best estimate; no retrieved document states it for income protection.*
  It is consistent with the research's product matrix, which marks lapse **up** as the
  material charge for this product and lapse **down** as conditional.
- **A genuinely lapse-supported cell — one whose discontinuance decreases technical
  provisions — is stressed by lapse *down*, not up.** The library's paradigm is the
  over-50s guaranteed-acceptance whole of life, where a lapse is pure profit and the
  whole lapse maximum collapses onto the down scenario [REG-R62]. Do not carry that
  result across to income protection by analogy: run the filter, per policy, on the sign
  of the change in technical provisions.
- **Mass lapse `3C16.6` inherits the same filter** — a flat **40%** discontinuance of the
  policies **for which discontinuance would increase TP without the risk margin**, plus
  40% off future reinsured contracts [REG-R62] — so it is nil on any cell the down
  scenario claims. `3C16.8` requires the calculation to use **the type of discontinuance
  that most negatively affects basic own funds on a per-policy basis**, and `SCR-SF 1.2`
  defines discontinuance to include surrender, lapse without value, **making a contract
  paid-up**, automatic non-forfeiture provisions and not exercising continuity options
  [REG-R62]. This product's discontinuance menu is thin — no surrender value, and unpaid
  premiums cancel the policy **without value** after a 60-day grace period [S1][S3] — so
  "worst discontinuance" collapses in practice to lapse-without-value. It is not empty,
  though: the sampled contracts permit benefit **decreases** without underwriting
  [S1][S3][S5][S7] and permit the policyholder to **decline an escalation increase**
  [S5][S11], and `3C16.4` (reading across from `3B6.4(1)`) makes any right to "fully or
  partly terminate, surrender, **decrease, restrict or suspend** cover" a relevant option
  [REG-R62]. *On its face that puts the escalation-decline right inside the lapse module;
  the retrieved rules do not name escalation options and the reading is a derivation.*
  The `M_esc` multiplier in *Policyholder behavior modeling* is the model's only handle
  on it and is **[std]**.

**Undertaking-specific parameters: the one door the standard formula opens to an IP
writer, and this design closes it.** The `USP 2.3` list of replaceable parameters is
**exhaustive** — there is no USP for any mortality, longevity, lapse, expense or
catastrophe parameter, and none for any market or counterparty parameter — and for the
seven library products it reduces to the **revision-risk** parameter: `3B5` for a pension
annuity and **`3C15` for income protection** [REG-R65]. But `USP 7.1(1)` makes the
revision method available **only if the annuities within scope are not subject to
material inflation risk**, `7.1(2)` treating inflation risk as material where ignoring it
could influence the decision-making or judgement of users including supervisors
[REG-R65]. The representative design's claim annuity escalates with RPI [S1][S2] — the
very feature that puts it inside `3C15` in the first place — so the condition fails on
its face. A USP also requires a permission and **cannot be reverted** once adopted
(`USP 2.1`, `2.2`) [REG-R65].

### Own funds, ring-fenced funds and the MCR

- **Own funds.** This model produces only the **technical provisions leg**; everything
  else is asset-side or capital-management input. The one product-specific consequence:
  a negative active-life best estimate flows through the excess of assets over
  liabilities into the **reconciliation reserve**, which Own Funds 3C.2 states "may be
  positive or negative" [REG-R77] — so the negative reserve is recognised in own funds,
  subject to tiering and to any ring-fenced-fund or MA-portfolio restriction. Note also
  that **EPIFP has been removed from Solvency UK reporting and disclosure altogether**
  [REG-R77][REG-R86 ¶¶4.43–4.44]: despite this being a paradigm product for expected
  profits included in future premiums, there is nothing to report.
- **No ring-fenced fund on the representative chassis.** The guaranteed-premium
  non-profit design sits in the shareholder fund: no with-profits fund, no surplus funds,
  no restricted own funds, no Own Funds 3L deduction [REG-R77][REG-R45].
- **Two perimeters can still appear, from opposite directions.**
  - A **matching adjustment portfolio** holding the claims-in-payment element is **not**
    a ring-fenced fund — the Glossary defines an RFF as an identifiable unit of assets
    and liabilities giving rise to restricted own funds "**other than a matching
    adjustment portfolio**" [REG-R80] — but it attracts the identical Own Funds 3L
    restriction and the identical `SCR-SF 9.1` treatment: a **notional SCR per
    perimeter**, the firm's SCR being their **sum**, with **no diversification between
    the MA portfolio and the remaining part** [REG-R62][REG-R77]. For this product that
    means the active-life morbidity charge and the claims-in-payment
    longevity/recovery-time charge stop diversifying against each other the moment an MA
    permission is used — a real capital cost of taking the MA on the in-payment element.
    One subtlety catches implementers: the *scenario choice* is made **firm-wide**, each
    notional SCR using the scenario under which the basic own funds of the firm **as a
    whole** are most negatively affected, so a perimeter's notional SCR can be driven by
    a scenario that is not its own worst, and **how a firm performs that firm-wide search
    in practice is not prescribed by any retrieved source** [REG-R62].
  - The **participating Holloway variation** [S11][S12] (product codes 480 CWP / 481
    Holloway accounts UWP [REG-R89]) sits inside a with-profits fund, which the PRA
    expects "will generally mean that each with-profits fund displays the characteristics
    of a RFF" [REG-R71][REG-R9]. That brings restricted own funds, the Own Funds 3L
    deduction, surplus funds, LACTP, the With-Profits Actuary duty under Actuaries 5.1(2)
    to advise whether the future-discretionary-benefit assumptions are consistent with
    the PPFM [REG-R93][REG-R9], and the FRS 103 ¶3.10 DAC prohibition. **It is out of
    scope for the reference model, which has no capital-account state** (*Assumption
    inputs*, (b)) — do not model the chassis and then assume the variation inherits its
    capital treatment.
- **MCR.** The linear formula reaches this product through **`TP_l4`**, all other
  long-term insurance obligations [REG-R78] — not `TP_l1` or `TP_l2` (no participation,
  no future discretionary benefits) and not `TP_l3` (nothing index-linked or
  unit-linked). The MCR sits in a corridor of **25%–45% of the SCR** with an absolute
  floor of **£3.5m** for long-term business, and is calculated **at least quarterly**
  (MCR 4.1) [REG-R78][REG-R61].
- **The capital-at-risk term is genuinely unresolved for this product, and the library
  says so rather than inventing a convention.** MCR 3C.1(5)(a) defines `CAR` by what the
  firm "would currently pay on **death or disability** of the persons insured", floored
  at zero **per contract** [REG-R78]. The disability limb is plainly engaged by an income
  protection contract, but **the rule does not say how to express a monthly income stream
  as a "currently payable" amount** — the whole disabled-life annuity, one month's
  benefit, or something else. **No retrieved source settles it.** The same quantity is
  reported in IR.14.01 C0190, defined by cross-reference to `SCR-SF 7.8` and `7.10`
  [REG-R89], so the ambiguity propagates straight into the reporting layer.
- The **general-insurance MCR segment 2** (α 13.1%, β 8.5%) [REG-R78] reaches an
  annually-renewable or group IP contract, not this design.

### Statutory accounts and tax

- **The measurement model.** Under UK GAAP this is an insurance contract within the scope
  of **FRS 103** — significant insurance risk is not in doubt for a morbidity contract
  [REG-R99]. Under UK-adopted IFRS 17 the UKEB's expected mapping puts protection
  business on the **general measurement model (GMM)**: fulfilment cash flows plus an
  explicit risk adjustment for non-financial risk plus a contractual service margin
  [REG-R106]. The **variable fee approach is not available** — there is no underlying
  pool of items and no variable fee; VFA is the unit-linked and with-profits model. The
  **premium allocation approach** does not reach the representative design either: it is
  the short-coverage simplification, and a full-term contract to age 65 is not it; PAA
  would be available only to a group whose coverage period is one year or less, i.e. an
  annually-renewable variant [REG-R106]. Annual cohorts, the coverage-unit requirement,
  the onerous-group loss component and the treatment of acquisition cash flows all bind
  [REG-R106]. **IFRS 17 itself is paywalled and was never read anywhere in this library;
  every IFRS 17 paragraph reference is one the UKEB quotes** [REG-R107][REG-R106].
- **DAC — and here the U.S. story is reversed, not transferred.**
  `us/regulatory/statutory-accounting-and-capital.md` opens on acquisition costs expensed
  as incurred, no DAC asset, and the first-year surplus strain that dominates U.S.
  statutory output. **None of that carries across.** In the UK statutory accounts
  **deferral is required**, and by company law before the standard: SI 2008/410 Schedule
  3 **para 13** requires costs of acquiring insurance policies incurred in one financial
  year but relating to a subsequent one to be **deferred**, with DAC at assets item
  **G.II** and its movement at technical account item **8(b) change in deferred
  acquisition costs** [REG-R105]; **FRS 103 ¶3.7** — "acquisition costs **shall be
  deferred**" — subject only to three carve-outs (costs already recovered; insufficient
  net present value of margins; insufficiently certain future premiums or margins); and
  **¶3.9** requires amortisation over no longer than the recoverability period **and in a
  similar profile to those margins**, with **no amortisation basis prescribed**
  [REG-R99]. So the same cash flows give **an accounts result with a DAC asset and no
  U.S.-style year-one strain**, a **Solvency UK result with acquisition expense inside a
  best estimate that may itself be negative** [REG-R41][REG-R39], and an **IFRS 17**
  result with no DAC asset for the opposite reason — acquisition cash flows sit inside
  the fulfilment cash flows and **reduce the CSM at initial recognition** [REG-R106].
  Three ledgers, three shapes, one cash flow vector.
  The **note 17 carve-out is a modelling fork, not a detail**: DAC is excluded to the
  extent the long-term business provision (item C.2) already allows for the costs, by
  explicit recognition or implicitly through anticipation of future income [REG-R105] —
  which is how a gross-premium or zillmerised IP reserve absorbs acquisition costs
  **inside the liability** instead of showing an asset. It must be an explicit model
  configuration, never an accident of the reserve basis. The **FRS 103 ¶3.10** with-profits
  prohibition does not reach the representative chassis; it reaches the Holloway
  variation, and even there its scope is contested — ¶3.1(b) applies ¶¶3.10–3.15 only to
  with-profits business and funds to which the PRA realistic capital regime (INSPRU
  section 1.3 as at 31 December 2015) applied before 1 January 2016, IG1.1 makes ¶3.12
  optional outside that scope, and **whether the ¶3.10 prohibition reaches a with-profits
  fund that was never in the realistic regime is not settled by the retrieved text**
  [REG-R99][REG-R100][REG-R116]. Neither reading is asserted here.
  **The projection above has no acquisition-expense stream at all** — maintenance and
  claim-management expenses only. Any use of these notes for an accounts, IFRS 17 or
  new-business projection must add one.
- **The UK GAAP floors, and where they diverge from Solvency UK.** FRS 103 implementation
  guidance **IG2.41**: "no policy may have an overall negative provision except as
  allowed by PRA rules, nor a provision less than any guaranteed surrender or transfer
  value" [REG-R100]. For this product the surrender-value limb is **vacuous** — there is
  none at any time [S4][S5][S7] — so the operative limb is the **non-negative floor**,
  and it bites exactly where the Solvency UK active-life best estimate is negative: the
  same block reports a **negative best estimate on the prudential balance sheet and a
  floored provision in the accounts**. In the other direction, the **liability adequacy
  test** (FRS 103 ¶¶2.14–2.18) is the only UK GAAP measurement floor: current estimates
  of all contractual and related cash flows including **claims handling costs** and cash
  flows from **embedded options and guarantees**, with the **entire deficiency**
  recognised in profit or loss [REG-R99]. For an IP block that is the mechanism through
  which morbidity deterioration first hits reported profit — and it **writes off DAC
  first**, because the test compares the carrying amount of insurance liabilities **less
  related DAC** against those cash flows [REG-R99].
- **Tax: non-BLAGAB, trade profits.** Protection business written from **1 January 2013**
  is excluded from BLAGAB and taxed on a **trading basis** like general insurance, so an
  IP model carries a trade-basis tax flag rather than an I-E policyholder tax engine
  [REG-R17][REG-R18 LAM01080] — as the spec's Regulatory context already records. Two
  qualifications it does not. First, policies written **before** that date **continue to
  be taxed as BLAGAB** unless the LAM14040 election has been made [REG-R18 LAM01080], so
  a back-book model needs both bases and the I-E apparatus does not disappear from a real
  IP entity. Second, since 1 January 2013 tax trade profits are computed from
  **accounting** profits (before that date, from the insurance regulatory returns)
  [REG-R18 LAM01100] — so the tax line follows the **DAC amortisation profile above**,
  not the Solvency UK expense run-off, and the three ledgers diverge again. The FA 2012
  **s.79 seven-year spreading of acquisition expenses is a BLAGAB mechanic** and reaches
  this product only through a pre-2013 back-book; it is **repealed for accounting periods
  beginning on or after 1 January 2023**, with legacy 1/7ths continuing to run and relief
  given only once across the transition [REG-R18 LAM04110, LAM04130][REG-R109]. Keep the
  company-tax question separate from the policyholder one: IP benefits funded from taxed
  personal income are free of income tax **to the individual** under current law
  [S4][S7][S11], which is a policyholder fact and has no effect on the company's
  computation.
- **The dividend is decided by the prudential balance sheet, not the accounts.** CA 2006
  s.830(3) makes the realised-profits rule **subject to s.833A** for an authorised
  insurance company carrying on long-term business: the realised profit or loss for
  s.830(2) purposes is **A − L − D** on the **prudential** total value of assets and
  liabilities, D including the excess of ring-fenced-fund assets over RFF liabilities and
  — where the firm has a matching adjustment permission — the excess of the assigned
  asset portfolio value over the value of the MA obligations; s.833A(3) then **caps**
  distributable profits at accumulated profits (realised **or not**) less accumulated
  losses [REG-R104]. Both named deductions can arise on this product: the **MA portfolio**
  if the claims-in-payment element is placed in one, the **RFF** only on the Holloway
  variation. A UK distributable-earnings pattern for income protection is therefore a
  projection of the **Solvency UK** balance sheet plus those deductions, then the
  accounts-based cap — not a projection of the accounts.

### Traps peculiar to income protection

1. **Two reporting populations, one contract.** Active cells report under code **494**
   (or **504** reviewable) and in-payment cells under **524** [REG-R89]. The `status`
   attribute is a reporting key, not just a state flag, and every IR.14.01 quantity —
   contract counts, new contracts, written premiums, claims paid, gross best estimate,
   capital at risk — must be producible separately for the two populations.
2. **The reviewable-premium boundary does not stop at the review.** TPFR 3.3(3)'s
   contract-level carve-out for individually risk-assessed long-term business keeps a
   reviewable IP policy's boundary open to the end of the term [REG-R41]. Cutting it at
   the 5-year review [S1][S4][S6][S10] is the largest boundary error available on this
   product, and it misstates both the premium leg and the claim leg.
3. **Health, not life.** Every instinct trained on term assurance sends this contract to
   the life module; `SCR-SF 3.2A(3)` sends it to health, and the two differ in more than
   labels — 4% revision instead of 3% **with an inflation trigger**, no 70% mass-lapse
   limb, a disability-morbidity scenario with two conditional limbs and asymmetric
   thresholds, and a catastrophe branch containing a **permanent-disability** exposure
   the ordinary projection does not compute [REG-R62].
4. **Lapse direction is decided per policy by a filter on the sign of the change in
   technical provisions**, not by whether the product "is lapse-supported" — see the SCR
   discussion. And `3C16` never reaches the claims-in-payment cells at all.
5. **The pandemic sub-module asks for a number this model cannot produce.** `3C20.2`
   wants the value of benefits payable assuming the insured is **permanently disabled and
   will not recover**; the recursion above terminates claims on ρ and truncates at the
   policy end date [REG-R62]. A separate no-recovery valuation run is required — and even
   with it, **the Annex XVI ratios were not retrieved, so the charge cannot be completed
   from this library's material** [REG-R73].
6. **Claims-management expense is load-bearing here and its reporting definition is about
   to change.** It is a named TPFR 16.1 category inside the best estimate [REG-R41]; it
   is **inside** IR.12.04 R2090 [REG-R89]; and it comes **out** of IR.14.01 C0070 "claims
   paid" from the **31 December 2026** reference date under PS18/26 [REG-R87 ¶2.41]. A
   model that nets claim-management cost into benefit outgo can produce neither version.
7. **The matching adjustment is available for part of the contract only, and the
   allocation rule does not exist.** MA 1.2 and 2.5 admit the in-payment element and
   disapply the no-future-premiums condition for it; SS7/18 ¶3.5B names recovery time
   risk as permitted and imposes **no exposure limit** on it [REG-R2][REG-R8]. But **how a
   single liability cash flow vector is split between the MA portfolio and the rest is
   not prescribed by any retrieved source**, and SS7/18 regards no notional splitting
   outside the eligible-element cases as compatible with MA 2.3 [REG-R8] — so the split
   cannot be assumed convenient. Taking the MA also costs the diversification between the
   two cells under `SCR-SF 9.1` [REG-R62].
8. **`CAR` for a disability income stream is undefined in the retrieved rules.** MCR
   3C.1(5)(a) and IR.14.01 C0190 both require it and neither says how to express a
   monthly benefit as a currently-payable amount [REG-R78][REG-R89]. No convention is
   invented here.
9. **The experience basis a UK model is required to report is one it cannot obtain.**
   IR.12.04 C0080 wants a **named table** and a percentage of it [REG-R89]; the IP11
   Series names are public and the values are CMI Authorised-User-restricted
   [R1][R2][R3][R5][REG-R22]. Every morbidity number in these notes is a **[std]** proxy
   carrying no CMI authority, IP11's known inception understatement needs the WP136
   indicative adjustments that only Authorised Users can apply [R1][R3], and TPFR 4.4's
   external-data conditions cannot be discharged against a proxy [REG-R41].
10. **The one USP the standard formula offers an IP writer is barred by this design's own
    escalation option** — `USP 7.1(1)` requires the annuities in scope not to be subject
    to material inflation risk, and RPI escalation [S1][S2] is what puts them inside
    `3C15` to begin with [REG-R65].
11. **The accounts show a DAC asset this model does not compute, and the U.S. framing is
    wrong here.** SI 2008/410 Sch 3 para 13 and FRS 103 ¶3.7 both **require** deferral
    [REG-R105][REG-R99]; there is no first-year strain of the U.S. kind on this product's
    accounts, and no acquisition-expense stream exists in the projection above to build
    the DAC from.
12. **Three liability measures on one block, with different signs.** Negative and
    unfloored on Solvency UK [REG-R1][REG-R115]; floored non-negative in the accounts
    (IG2.41, with the surrender-value limb vacuous) [REG-R100]; and a GMM fulfilment
    cash flow plus CSM under IFRS 17, where fulfilment cash flows may be negative but a
    group cannot carry a negative CSM — that being what makes a group onerous and creates
    a loss component [REG-R106] (*that comparison is drawn by the drafter of the shared
    framework file, not sourced from retrieved IFRS 17 text, which is paywalled
    [REG-R107]*). Reconciliation between the three is a required output, not a nicety.

---

## Valuation and reserve pointers

This library projects **gross best-estimate liability cash flows**. The Solvency UK
measurement, the SCR modules, the reporting templates and the other two ledgers for this
product are in **Statutory accounting and capital** above; this section stays a pointer
list for the valuation layers themselves, which consume those flows and are NOT
reproduced here:

- **Solvency UK technical provisions.** Technical provisions = best estimate + risk
  margin; the best estimate is the probability-weighted average of future cash flows
  discounted at the relevant risk-free term structure [R7][REG-R1] — i.e. exactly the
  active-life and claims-in-payment projections above, both premium and claim sides.
  Risk margin: cost-of-capital method at 4% with life λ-tapering 0.9 [REG-R4] —
  cited-not-specified here; the product-specific run-off shape, the
  no-MA reference undertaking and the absence of any UK simplification hierarchy are in
  Statutory accounting and capital above, "The risk margin".
- **Matching adjustment.** The claims-in-payment element of IP is an MA "eligible
  element" where organised and managed separately [R8][REG-R2]: the disabled-life
  annuity cash flows are the portion a UK insurer may discount at risk-free + MA under
  an MA permission. The MA 2.5 future-premium disapplication, the SS7/18 recovery-time-
  risk expectations and the unresolved MA/non-MA allocation question are in Statutory
  accounting and capital above, "Technical provisions".
- **IFRS 17.** UK-adopted IFRS 17 (effective 2023) applies to IFRS-reporting UK life
  insurers [REG-R38]; the fulfilment-cash-flow engine consumes the same projections with
  its own discounting, risk adjustment and CSM layers (cited-not-specified). The
  measurement model this product falls under — the general measurement model — is in
  Statutory accounting and capital above, "Statutory accounts and tax".
- **UK GAAP statutory accounts.** FRS 102 + FRS 103, with acquisition costs **deferred**
  and a non-negative provision floor that the Solvency UK number does not have —
  Statutory accounting and capital above, "Statutory accounts and tax"
  (cited-not-specified here).
- **Professional standards.** TAS 100 (all technical actuarial work) and TAS 200
  (insurance-specific) govern UK actuarial use of such models [R10,
  fetched_ok=false in the product research pass; verified via [REG-R33][REG-R34]].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order:

1. **Claim inception and termination (recovery) rates.** They set both sides of the
   liability: inceptions drive new-claim frequency, recoveries drive claim length —
   a small recovery-rate change compounds across the whole disabled-life annuity.
   Both proxy tables here are **[std]** placeholders; the real IP11 basis is
   restricted [R1][R2][R5][REG-R22], and IP11 inceptions carry a known
   understatement requiring the WP136 indicative adjustments [R1][R3].
   Sensitivity-test ι and ρ first, and independently.
2. **Morbidity trend.** The base holds morbidity level **[std]**; cause-mix shifts
   (notably mental-health claims, which interact with own-occupation assessment)
   move both ι and ρ. No public quantification was retrieved — treat as a scenario
   axis, not a calibrated input **[std note]**.
3. **Economic sensitivity of claims.** Recession-linked inceptions and slowed
   recoveries (the M_cycle overlay) are the classic IP experience risk on
   own-occupation business — a [std] scenario note, deliberately not calibrated
   here.
4. **Escalation/inflation.** RPI-linked benefit escalating in claim [S1][S2] makes
   the disabled-life annuity inflation-sensitive precisely when it is longest; the
   10% cap is an embedded inflation option. The premium side compensates only ×1.5
   on actives, and not at all on claims in payment (waiver).
5. **Lapse.** Second-order for claim cost but first-order for premium income and
   deferred-acquisition economics; the table is **[std]** with no public anchor.

Known modeling pitfalls:

- **Duration dimension.** Collapsing l_S(t, z) to a single bucket with
  duration-independent termination rates materially misstates claim runoff — the
  duration gradient (0.40 → 0.05 in the proxy) is the defining feature of IP
  terminations [R1].
- **Premium waiver double-count.** Projecting premium income from l_S lives
  overstates premiums; premiums come from l_H only (waiver [S5][S7][S10][S11]).
- **Expiry truncation.** The disabled-life annuity must truncate at the policy end
  date [S1][S3][S5][S7][S10]; an untruncated annuity materially overstates
  liabilities for claims incepting near expiry.
- **Amount payable vs chosen benefit.** Offsets, the £1,500 guarantee and
  proportionate benefits mean amounts paid can differ from B; modeling AP = B
  **[std]** overstates outgo where the maximum-benefit formula bites (and
  understates nothing — AP ≤ B always).
- **Linked claims.** Returning recovered lives to the standard inception basis
  ignores the waived deferred period on 52-week recurrences (see limitation note) —
  understates outgo for short-recovery portfolios.
- **Run-in periods.** IP11 recovery rates increase over the first weeks of claim
  for DP4/13/26 [R1]; annual duration-year granularity **[std]** smooths this away
  — significant for short deferred periods, less so at DP26.
- **Basis-structure mismatch.** The proxy termination rates drop the age dimension
  **[std]**; IP11 is two-dimensional (age × duration), with claimant mortality
  duration-dependent to 5 years and age-only beyond [R1]. Table licensees should
  restore both dimensions.
- **Escalation timing.** B escalates on policy anniversaries in this model
  **[std]**; some contracts escalate in-claim amounts on claim anniversaries with
  index-lag rules (e.g. RPI five months prior, post-claim catch-up [S10]) — align
  with the contract being modeled.
