# Whole of Life Assurance — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** These notes specify a reference liability cash flow projection model for the
standardized composite product defined in `product-spec.md` (same directory). This is not any
single insurer's product. [S#]/[R#] tags refer to the source list in
`uk/_research/whole-of-life.md` via `sources.md`; [REG-R#] tags refer to the cross-product
reference library `uk/references/regulatory-and-actuarial-references.md` (its own
R-numbering; research provenance in `uk/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks claims not
confirmed against a retrieved document. Parameter values are identical to those in
`product-spec.md`. Two cells share one engine:

- **RefWOL-UW** (underwritten guaranteed; Zurich pattern [S10]) — anchor: male, entry age 40,
  non-smoker, £150,000 sum assured, level cover, £101.25/month **[std]**.
- **RefWOL-O50** (over-50s guaranteed acceptance; L&G/SunLife pattern [S1][S4]) — anchor:
  entry age 70 **[std]**, non-smoker, £30/month, £5,000 cash sum ([R2] stylised pair).

Neither cell carries any account value, unit fund, or surrender value [S1][S4][S7][S9][S10]:
both are **pure-decrement protection models** — the projection is premiums in, death benefits
and expenses out, weighted by survivorship. This is the deliberate contrast with the US
cash-value whole life chassis (no CSV schedule, no dividends, no loans).

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premium income, death
  outgo, expenses; no surrender outgo exists) for single-policy model points of the two
  cells, on a monthly grid. Reserves, discounting, risk margin and capital are pointed to,
  not computed (see Statutory accounting and capital, and Valuation and reserve pointers).
- **Projection frequency.** Monthly **[std]**. Premiums are monthly Direct Debit in the O50
  cell [S1][S4][S7][S9] and monthly or annual at Zurich [S10]; monthly is the natural grid.
- **Timing conventions [std].** Premiums (and premium-linked commission) at the beginning of
  the policy month (BOM); deaths during the month resolved at end of month (EOM) against the
  BOM in-force; lapses at EOM after deaths (death-before-lapse order). Escalation steps
  (Increasing Cover, RPI variants) apply at policy anniversaries [S4][S10]. Annual-grid
  implementations must preserve the month-13 moratorium boundary.
- **Age basis.** Age last birthday (ALB) **[std]**. Rationale: Zurich defines entry age x as
  "before the (x+1)th birthday" [S10], which is ALB; the O50 documents price on "age at
  outset" without stating a basis [S1]. All age lookups in this model are ALB.
- **Currency / units.** GBP. Sum assured in £; premiums in £/month; mortality and lapse
  rates dimensionless per annum, converted to monthly as q_m = 1 − (1 − q)^(1/12) **[std]**.
- **Model points.** Single-policy expected-value projection: survivorship probabilities
  multiply per-policy cash flows. No aggregation logic here. Aggregation caps across
  same-insurer policies (£10,000/£18,000, £100/month [S1][S4][S9]) are immaterial to a
  per-policy model.
- **Claims settlement.** Immediate at EOM of the death month **[std]**; contractual claims
  interest (BoE base − 0.5%, floor 0.5% p.a., between death and payment [S1][S9]) is
  excluded as a settlement-lag refinement, not a liability driver.
- **Rounding.** Full precision carried; cash flows reported to pence **[std]**.

---

## Model point attributes

| Attribute | Type | Example (O50 anchor) | Example (UW anchor) |
|---|---|---|---|
| `cell` | enum {O50, UW} | O50 | UW |
| `entry_age` | int (ALB) | 70 | 40 |
| `sex` | enum {M, F} | F **[std]** (pick for the anchor cell; attribute carried for basis lookup — O50 pricing itself does not rate by sex in the fetched documents, which state age and smoker status as the rate factors [S1][S4]) | M |
| `smoker` | enum {NS, S} | NS | NS (Zurich 3-state definition [S10] collapsed to 2 **[std]**) |
| `sum_assured` | currency (£) | 5,000 | 150,000 |
| `monthly_premium` | currency (£/month) | 30.00 | 101.25 **[std]** |
| `escalation` | enum {level, fixed_5pct, rpi} | level | level (fixed_5pct variant) |
| `cessation_months` | int (∞ for UW) | 240 (anniversary on/after 90th birthday **[std]**) | none — premiums payable for life [S10] |
| `moratorium_months` | int | 12 [S1][S4][S7][S9] | 0 (suicide-only clause instead [S10]) |
| `variant_adb_2x` | bool (Aviva multiplier [S7]) | false | n/a |
| `variant_payout_promise` | bool (Royal London [S9]) | false | n/a |
| `variant_rpi_increasing` | bool (L&G [S4]) | false | n/a |
| `issue_date` | date | month 1 | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly (deaths, lapses) |
| `CumPrem(t)` | Cumulative premiums paid to end of month t (year-1 refund base; crossover tracking) | monthly |
| `N_paid(t)` | Count of monthly payments made (Payout Promise numerator [S9]) | monthly |
| `SA(t)` | Current sum assured / cash sum (escalating variants) | anniversaries |
| `P(t)` | Current monthly premium (escalating variants; 0 after cessation) | anniversaries / cessation |
| `paid_up` | Payout Promise state: policy premium-free with reduced payout PU [S9] | on qualifying lapse |
| `PU` | Paid-up payout = SA x N_paid / N_expected (Payout Promise variant) [S9] | on paid-up conversion |
| `in_moratorium(t)` | Indicator t <= 12 (O50) | monthly |
| `attained_age(t)` | entry_age + floor((t−1)/12) (ALB) | monthly |

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Premium level at issue | Fixed at outset by age and smoker status (O50 [S1][S4]) / full underwriting (UW [S10][S11]); guaranteed never to increase [S1][S4][S7][S9][S10] | anchors: £30/month for £5,000 at 70 [R2]; £101.25/month for £150,000 at 40 **[std]** |
| O50 moratorium | 12 months; non-accidental death → return of premiums paid (no interest stated); accidental death → full cash sum from day 1 | [S1][S4][S7][S9] |
| O50 premium cessation | Anniversary on/after 90th birthday; cover continues | [S4][S5][S9]; pick **[std]** |
| UW terminal illness | Sum assured accelerated on 12-month prognosis; pays once, policy ends | [S10][S12] |
| UW suicide clause | Suicide/intentional self-inflicted injury within 12 months of start (or increase) → refund of premiums for that cover | [S10][S11] |
| UW escalation (variant) | SA +5%/year, premium +10%/year (2% premium per 1% cover) | [S10]; 5% pick **[std]** |
| O50 RPI variant (L&G) | Cash sum +RPI (floor 0%, cap 10%); premium +RPI x 1.5 (cap 15%); freeze on first declined increase; cash-sum indexation continues post-90 | [S4] |
| Payout Promise (RL variant) | If N_paid >= N_expected/2 at premium stop: paid-up payout = SA x N_paid/N_expected; else cancellation with nothing | [S9] |
| Arrears | 60 days to make good; death in window → claim reduced by unpaid amounts; then lapse with no value | [S4][S9]; pick **[std]** |
| Surrender value | None at any time, either cell | [S1][S4][S5][S7][S9][S10] |

### (b) Insurer-discretionary current elements

**This class is nearly empty — the defining feature of both modern cells.** Premiums are
guaranteed [S1][S4][S7][S9][S10]; there are no bonus rates, no reviewable premiums, no
unit-linked charges, no asset shares and no MVRs in either cell (those mechanisms belong to
with-profits and unit-linked business, out of scope here). The discretionary layer reduces
to:

- **New-business rate tables.** Insurers do not publish full premium rate tables (research
  file gap); only quote anchors exist (£20/month at 50 NS → £5,694 [S2]; £25/month NS →
  £7,643/£6,046/£3,701/£1,893 at 50/60/70/80 [S6]) plus the FCA per-£1,000 averages (£71.73
  GO50, £8.10 underwritten) [R2]. The model takes premium as a model-point input; any shipped
  rate table is a **[std]** snapshot calibrated to these anchors.
- **Claims interest rate.** Contractual formula, BoE-base-linked (base − 0.5%, floor 0.5%)
  [S1][S9]; excluded from the base model **[std]** (conventions).
- **Legacy variation only:** the unit-linked reviewable design's review basis (mortality
  charge scale, review outcomes) is insurer-discretionary [S15]; it is documented as a
  closed-book variation, not modeled.

### (c) Behavioral / experience assumptions (modeler's view)

CMI access is honestly restricted: current tables and the Projections Model are limited to
Authorised Users/Subscribers; older publications are free — so a reference basis must be a
**[std]** proxy shaped like the named tables, and cannot redistribute current qx values
[REG-R22][R7].

| Input | Recommended public basis | Basis tags |
|---|---|---|
| UW mortality | Assured-lives shape: CMI "00" series permanent assurances AMC00/AMS00/AMN00, AFC00/AFS00/AFN00 (publicly downloadable; the latest published assured-lives whole of life base tables) x A/E factor 100% **[std]**; AM92/AF92 as the teaching-table alternative shape | [R6][R7][REG-R24]; factor **[std]** |
| O50 mortality | Population-level: ONS national life tables qx (single year of age, sex; freely downloadable under OGL) x anti-selection loading 120%, level across durations **[std]** | [REG-R32]; loading **[std]** (see below) |
| Mortality improvement | None in base **[std]**; sensitivity: "CMI_20xx with long-term rate p% [std]" is the market-standard expression, but the model is subscriber-restricted — a flat 1% p.a. improvement is the [std] sensitivity proxy | [REG-R30][REG-R22] |
| O50 accidental-death share of year-1 deaths | 3% **[std]** — accidental deaths are a small minority at 70+; no public split was found (research gap) | **[std]** |
| UW suicide share of year-1 deaths | 1% **[std]** — refund instead of sum assured; immaterial, carried for completeness | **[std]** |
| Terminal illness acceleration (UW) | Model TI claims as deaths accelerated by 6 months on average; base model ignores the acceleration (pays at death) **[std]** | timing **[std]**; benefit [S10] |
| Lapse | [std] tables below; no public UK WoL lapse study was retrieved (research gap); the FCA documents the lapse-supported dependence qualitatively | [R2]; tables **[std]** |
| Expenses | O50: acquisition £150/policy + commission 25% of year-1 premiums **[std]**; maintenance £30/policy/year inflating 3% p.a. **[std]**. UW: acquisition £300/policy + initial commission **[std]**; maintenance £50/policy/year inflating 3% **[std]**. Commission existence per SunLife (intermediary "paid by commission as a percentage of total annual premium" [S1]); all levels **[std]** | [S1]; levels **[std]** |

**Why the O50 basis is population-plus-loading, not assured lives.** Guaranteed acceptance
removes underwriting, so the pool cannot be better than population and self-selects worse:
the CMI is analysing *non-underwritten* whole of life experience separately from underwritten
— direct recognition of the anti-selection distinction [R7] — and the FCA's price
differential (£71.73 vs £8.10 per £1,000) reflects guaranteed-acceptance anti-selection,
older entry ages and shorter durations [R2]. No insurer discloses its GO50 pricing basis
(expected — proprietary; research file gap), so the 120% loading on ONS population rates is a
**[std]** placeholder to be calibrated; population mortality is itself heavier than insured
experience [REG-R32], so the loading is deliberately modest. The UW cell uses an
assured-lives shape ("00" series [R6]) because full underwriting restores select experience.

Reference base lapse tables **[std]** (annual rates; shapes are drafting constructions —
no public product-specific study; replace with experience):

| Policy year | 1 | 2 | 3–5 | 6+ | after premium cessation |
|---|---|---|---|---|---|
| O50 `w_base` | 8% | 6% | 4% | 4% | 0% (no premiums due — no lapse) |
| UW `w_base` | 6% | 5% | 3% | 2% | n/a (premiums for life) |

---

## Cash flow components and recursions

### Notation (defined once, used throughout; shared with product-spec.md)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1, 2, ...; y = policy year = floor((t−1)/12) + 1 |
| a(t) | attained age (ALB) = entry_age + floor((t−1)/12) |
| P(t) | monthly premium due at BOM of month t (0 after cessation / in paid-up state) |
| SA(t) | sum assured / cash sum in month t (constant unless escalating variant) |
| T_cess | months from start to premium cessation (O50: to anniversary on/after 90th birthday; anchor 240); ∞ for UW |
| CumPrem(t) | Σ_{s<=t} P(s) |
| q(y) | annual mortality rate for policy year y (basis per cell, class (c)) |
| q_m(y) | monthly mortality = 1 − (1 − q(y))^(1/12) **[std]** |
| w(y), w_m(y) | annual / monthly lapse rates, w_m = 1 − (1 − w)^(1/12) **[std]** |
| δ_acc | accidental share of year-1 deaths (O50), 0.03 **[std]** |
| δ_su | suicide share of year-1 deaths (UW), 0.01 **[std]** |
| l(t) | in-force probability at end of month t; l(0) = 1 |
| DB_na(t), DB_ac(t) | death benefit for non-accidental / accidental death in month t (O50) |
| k_adb | accidental multiplier after year 1: 1 (base) or 2 (Aviva variant [S7]) |
| E[·] | expectation over decrements (survivorship weighting) |

Dimensional check: premiums and benefits are £; q_m, w_m, δ are dimensionless; every expected
cash flow below is £ per month per policy issued.

### Monthly processing order (both cells) **[std]**

At month t while in force and not paid-up:

1. BOM: premium P(t) received if t <= T_cess (O50) or always (UW); commission/premium
   expense deducted as an expense flow, not from any fund (there is no fund).
2. BOM: maintenance expense for the month.
3. Anniversary (t ≡ 1 mod 12, t > 12): apply escalation to SA and P (variants only)
   [S4][S10].
4. EOM: deaths at rate q_m(y) applied to l(t−1); benefit per the rules below.
5. EOM: lapses at rate w_m(y) applied to survivors of step 4; death-before-lapse **[std]**.
   In the Payout Promise variant a "lapse" with N_paid >= N_expected/2 converts to paid-up
   (state change, no cash flow) instead of termination [S9].
6. Update l(t) = l(t−1) x (1 − q_m(y)) x (1 − w_m(y)).

Paid-up policies (Payout Promise) and post-cessation O50 policies skip steps 1 and 5
(no premiums due, so no lapse decrement **[std]**) and continue steps 2, 4, 6 with w_m = 0.
Step 3 is also skipped, with one exception: in the RPI-increasing variant the cash sum
continues to index at anniversaries after premiums cease at 90 [S4] (the premium step, being
zero, stops).

### RefWOL-O50 recursions

Premiums (level base design):

    P(t) = P x 1{t <= T_cess},        CumPrem(t) = P x min(t, T_cess)

Death benefit split during the 12-month moratorium [S1][S4][S7][S9]:

    DB_na(t) = CumPrem(t)   if t <= 12          (return of premiums paid, no interest)
             = SA           if t >  12
    DB_ac(t) = SA           if t <= 12          (full cash sum from day 1)
             = k_adb x SA   if t >  12          (k_adb = 2: Aviva variant [S7])

Expected cash flows in month t (per policy issued):

    E[premium](t) = l(t−1) x P(t)
    E[death outgo](t) = l(t−1) x q_m(y) x [ (1−δ_acc) x DB_na(t) + δ_acc x DB_ac(t) ]   if t <= 12
                      = l(t−1) x q_m(y) x [ (1−δ_acc) + δ_acc x k_adb ] x SA           if t >  12
    E[expenses](t) = l(t−1) x [maintenance(t)] + commission/acquisition at their BOM timing

(with k_adb = 1 the post-moratorium death outgo is simply l(t−1) q_m SA). Lapse generates
**no cash flow**: there is no surrender value [S1][S4][S5][S7][S9] — its entire effect is
through l(t). That is the arithmetic meaning of "lapse-supported": every lapse extinguishes
a paid-up-style liability for nothing, and the FCA records that without the continuing-payer
cross-subsidy "insurers would need to rely on lapses to remain profitable" [R2].

Crossover (tipping point): cumulative premiums first exceed the cash sum at

    t* = floor(SA / P) + 1    (months, level premiums, t* <= T_cess)

Anchor: floor(5000/30) + 1 = 167 months = 13 years 11 months, reproducing the FCA's stylised
example exactly [R2]. Total premiums payable are capped at P x T_cess (anchor: £7,200 vs
£5,000 cash sum). A crossover exists iff SA < P x T_cess; the FCA notes entrants at 79–80 are
most exposed and that the majority of policies still pay out more than premiums paid [R2].

Payout Promise variant [S9]: on premium stop at month t with N_paid(t) >= N_expected/2
(N_expected = T_cess):

    PU = SA x N_paid(t) / N_expected        (worked example: 180/240 x £3,500 = £2,625 [S9])

thereafter DB_na = DB_ac = PU (the moratorium is long past), premiums 0, lapse 0 **[std]**.

RPI-increasing variant (L&G [S4]), r_y = RPI inflation for year y:

    SA(y+1) = SA(y) x (1 + min(max(r_y, 0), 0.10))
    P(y+1)  = P(y)  x (1 + min(max(1.5 x r_y, 0), 0.15))       while y < cessation
    SA continues to index after premiums cease at 90; first declined increase freezes both
    (premium step floored at 0 **[std]** — [S4] defines an increase only, no decrease).

### RefWOL-UW recursions

Premiums guaranteed level (base): P(t) = P for all t; no cessation age [S10]. Escalating
variant (5% **[std]**), applied at anniversaries [S10]:

    SA(y) = SA_0 x 1.05^(y−1),      P(y) = P_0 x 1.10^(y−1)

Death/terminal-illness benefit: the sum assured is paid once on death or earlier terminal
illness diagnosis (12-month prognosis), and the policy ends [S10][S12]. The base model pays
SA(y) at death (TI acceleration ignored **[std]**; a TI module would move a fraction of
claims ~6 months earlier **[std]** with no change in amount). Suicide within 12 months
refunds premiums [S10]:

    E[death outgo](t) = l(t−1) x q_m(y) x [ (1−δ_su) x SA(y) + δ_su x CumPrem(t) ]   if t <= 12
                      = l(t−1) x q_m(y) x SA(y)                                      if t >  12

Lapse (2 months' unpaid premiums, no reinstatement [S10]) again generates no cash flow — no
cash-in value at any time [S10] — and only reduces l(t). Milestone-benefit exercises and
requested increases are out of scope (they would step SA and P; anti-selection flagged in
model risks) [S10][S12].

### Cash flow outputs (per policy issued, month t)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | l(t−1) x P(t) | + |
| Death outgo | per cell formulas above | − |
| Acquisition expense + initial commission | at t = 1 (and commission % x premiums in year 1, O50) **[std]** | − |
| Maintenance expense | l(t−1) x (annual maintenance / 12) x (1.03)^(y−1) **[std]** | − |
| Surrender outgo | **none — identically zero in both cells** [S1][S4][S7][S9][S10] | — |
| Claims interest | excluded **[std]** (contractual BoE−0.5% floor 0.5% between death and payment [S1][S9]) | — |

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK whole of life
lapse/persistency study was retrieved (research gap), so shapes are drafting assumptions
with the qualitative anchors cited.

- **Base lapse [std].** Duration-declining tables above; converted monthly. Rationale for the
  declining shape: sunk premiums with zero surrender value and (O50) the approaching
  paid-out-in-full status discourage late lapse.
- **Moratorium-completion effect (O50) [std].** No extra lapse spike at month 13: the
  moratorium gives no incentive to lapse (lapsing returns nothing at any time). The year-1
  rate is set highest instead (affordability/buyer's-remorse attrition; the 30-day
  cooling-off with full refund [S1][S4] is modeled as never-issued business, out of scope).
- **Crossover-aware lapse (O50) [std].** Sensitivity module, off in base:
  `w(t) = w_base(y) x (1 + β x 1{CumPrem(t) > SA})`, β = 0.5. Rationale: Consumer Duty
  communications must enable informed choice about the over-payment risk [R2], which could
  raise post-tipping-point lapses; the FCA has seen no evidence that a significant proportion
  of customers reach the premium caps [R2]. β is a pure stress dial.
- **Payout Promise selection (RL variant) [std].** Once N_paid >= N_expected/2, all would-be
  lapses convert to paid-up (rational: forfeiture is strictly dominated; mechanics per [S9]);
  before the halfway point, lapse means total loss, so the base w applies. This converts
  lapse profit into a retained pro-rata liability — the variant exists precisely to remove
  the forfeiture cliff, and materially weakens lapse support (sensitivity mandatory).
- **Premium reduction options [std].** One-off reductions (SunLife/L&G/RL [S1][S4][S9]) are
  not modeled; they are economically a partial lapse with proportionate SA reduction.
- **Escalation opt-out (UW variant) [std].** Increasing Cover holders decline an increase
  with probability 10% per anniversary; three declines remove the option [S10]; base model
  assumes full take-up.
- **Payment holidays (RL [S9])** are ignored **[std]** (≤ 12 months' premiums deferred or
  netted; second-order).

---

## Worked example

RefWOL-O50 anchor cell: entry age 70 (ALB), non-smoker, P = £30/month, SA = £5,000, T_cess =
240 months (anniversary on/after 90th birthday **[std]**), base design (k_adb = 1, no Payout
Promise). Illustrative walk-through basis **[std]** (placeholder, not attributable to any
table): q(y) = 0.024 x 1.10^(y−1) — i.e. a 0.020 population-style rate at 70 x the 120%
anti-selection loading, with 10% p.a. age progression; lapse 8%/6%/4%/4% (years 1/2/3–5/6+),
0 after cessation; δ_acc = 3%. Monthly rates: q_m(1) = 1 − (1−0.024)^(1/12) = 0.0020223;
w_m(1) = 1 − (1−0.08)^(1/12) = 0.0069244. Expenses omitted from the table for clarity.
E[death outgo](t) = l(t−1) x q_m x (0.97 x DB_na + 0.03 x DB_ac) for t <= 12, and
l(t−1) x q_m x 5,000 thereafter. All £, full precision carried, displayed rounded.

| t | y | CumPrem | DB non-acc | DB acc | l(t−1) | E[premium] | E[death outgo] |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 30.00 | 30.00 | 5,000 | 1.00000 | 30.00 | 0.36 |
| 6 | 1 | 180.00 | 180.00 | 5,000 | 0.95613 | 28.68 | 0.63 |
| 12 | 1 | 360.00 | 360.00 | 5,000 | 0.90601 | 27.18 | 0.91 |
| 13 | 2 | 390.00 | 5,000.00 | 5,000 | 0.89792 | 26.94 | 10.00 |
| 24 | 2 | 720.00 | 5,000.00 | 5,000 | 0.82785 | 24.84 | 9.22 |
| 60 | 5 | 1,800.00 | 5,000.00 | 5,000 | 0.66359 | 19.91 | 9.88 |
| 120 | 10 | 3,600.00 | 5,000.00 | 5,000 | 0.42564 | 12.77 | 10.31 |
| 166 | 14 | 4,980.00 | 5,000.00 | 5,000 | 0.27420 | 8.23 | 9.85 |
| 167 | 14 | 5,010.00 | 5,000.00 | 5,000 | 0.27131 | 8.14 | 9.74 |
| 240 | 20 | 7,200.00 | 5,000.00 | 5,000 | 0.09992 | 3.00 | 6.57 |
| 241 | 21 | 7,200.00 | 5,000.00 | 5,000 | 0.09828 | 0.00 | 7.16 |

Trace, month 1: E[death] = 1.0 x 0.0020223 x (0.97 x 30 + 0.03 x 5,000) = 0.0020223 x 179.10
= £0.36 — the year-1 death outgo is dominated by the small accidental tail paying the full
cash sum, not the premium refund. Trace, month 13: the moratorium ends and the full £5,000
becomes payable for any death: E[death] = 0.89792 x 0.0022271 x 5,000 = £10.00 (q(2) = 0.0264
→ q_m = 0.0022271) — a ~11x jump in expected death outgo at the month-12/13 boundary, the
signature discontinuity of this product. Month 167 is the crossover: CumPrem = £5,010 first
exceeds the £5,000 cash sum (13 years 11 months, reproducing [R2]). Month 241: premiums have
ceased (E[premium] = 0) but death outgo continues — and rises, because lapses stop **[std]**
and mortality steps up at the year-21 anniversary; the post-cessation period is pure outgo,
funded by the pre-cessation premium margins and lapse releases.

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` and `uk/regulatory/technical-notes.md`;
this section states only what is specific to whole of life. [REG-R#] resolves against the
shared UK numbering in `uk/references/regulatory-and-actuarial-references.md`, which now runs
**R1–R120**, with **R50–R52, R74–R76 and R121–R133 unused by design** (the research streams
were allocated parallel blocks and the tails left spare; an unused number is not a missing
entry). [R#] and [S#] continue to resolve against `sources.md`.

**What "statutory accounting" means here.** The UK has no statutory accounting in the U.S.
sense. Three separate measurements run off this one cash flow engine: the **Solvency UK
regulatory balance sheet** (the prudential measurement, PRA Rulebook) [REG-R39][REG-R1]; the
**statutory accounts** (Companies Act accounts under FRS 102 + FRS 103, or UK-adopted IFRS 17)
[REG-R103][REG-R99][REG-R105][REG-R106]; and **tax**, which is not a liability measurement at
all but is computed *from the accounts* with the Finance Act 2012 overlay [REG-R17][REG-R18].
The single most important consequence for a U.S.-trained reader is set out under "Statutory
accounts and tax" below: the U.S. story of acquisition costs expensed as incurred, no DAC
asset and first-year surplus strain is **reversed** in the UK accounts.

### Contract classification and reporting

- **RAO class.** Both modelled cells are **Class I** ("Life and annuity") long-term insurance
  business under RAO Schedule 1 Part II [REG-R14][R5]; the legacy unit-linked reviewable
  variation [S15] is **Class III** ("Linked long term") [REG-R14][R5]. Nothing in this folder
  is Class VII, which matters for the mass-lapse limb below.
- **Solvency UK line of business — the technical basis, not the product label.** TPFR 26.2:
  assignment "must reflect the **nature of the risks**… The **legal form** of the obligation
  **is not necessarily determinative**" [REG-R41]. On that basis both non-profit cells sit in
  **Annex 1 LoB 32** (other long-term insurance business); a unit-linked whole of life sits in
  **LoB 31**; a with-profits whole of life in **LoB 30** [REG-R41]. **That mapping is the
  research's inference from TPFR 26.2, 26.3 and the Annex 1 definitions, not a quotation —
  Annex 1 names no products** [REG-R41]. Neither cell carries a health obligation, so LoB 29
  and the whole health module are unreachable.
- **PRA product ID code (IR.14.01 column C0010).** Both modelled cells report under **104**
  (whole of life OB NP — "OB" ordinary branch, "NP" non-profit); **102** is whole of life OB
  UL, reached only by the legacy unit-linked variation [S15]; **100 / 101** are whole of life
  OB CWP / UWP for participating forms; **105 / 106** are industrial branch and out of scope
  [REG-R89]. Three verified conventions from the code list bite here: the whole-life codes are
  **regular premium business only**, they **include paid-up policies** — so a Payout Promise
  policy [S9] stays in 104 rather than leaving the return — and they **exclude single premium
  bonds "which are technically whole of life"**, which is why a with-profits or unit-linked
  *bond* reports under 111 / 112 and not under a whole-of-life code [REG-R89]. Where technical
  provisions are calculated for a product combination, or the code is uncertain, firms "should
  use an **approximation to apportion** between product codes"; where one product spans rows
  the pattern is `{code}/+/{version}` [REG-R89].
- **Templates this product drives.** IR.12.01 (life technical provisions, quarterly *and*
  annual), IR.12.03, IR.12.04, IR.14.01, IR.05.03, IR.05.05, IR.28.01 (MCR) and the SFCR
  templates apply to every product in the library, subject to **entity-level** thresholds
  [REG-R84][REG-R89][REG-R90]. IR.22.01 (long-term guarantee and transitional impact) is
  marked **x** for whole of life specifically because this is a book that carries TMTP and the
  interest-rate transitional [REG-R84] — see "Transitionals" below.
- **The IR.14.01 rows that are this product's own** [REG-R89]: C0010 = 104, C0030 = LoB 32,
  C0040/C0050 contract counts (identifiable increments and rider benefits count as **a single
  contract**, so a Milestone-benefit increase [S10][S12] does not create a second contract),
  C0060 gross written premiums, C0070 claims paid — **including claims management expenses
  until PS18/26 removes them from that definition with effect from the 31 December 2026
  reference date** [REG-R87] — C0180 gross best estimate, and C0190 capital at risk, "as
  defined in **Solvency Capital Requirement – Standard Formula 7.8 and 7.10**". Reinsurance
  ceded is **not** reported in IR.14.01. The reporting layer also treats **surrender value as
  a disclosure item, not a constraint** on the best estimate [REG-R89] — identically zero for
  both modelled cells at every duration [S1][S4][S5][S7][S9][S10].
- **IR.12.04 has this product's mortality rows and no others — and the instructions do not
  settle where the rest go.** The assumption template gives whole of life its own mortality
  rows (R0010 male non-smoker, R0050 male aggregate, R0090 male smoker, R0130 / R0170 / R0210
  the female equivalents, and R0250 assurance mortality change per annum on the "equivalent
  annual rate over ten years" convention), reported as percentages of a **named table** in
  C0080 with any CMI projection parameterisation in CMI notation [REG-R89]. But **the lapse
  blocks are with-profits endowment, unit-linked endowment, level term, decreasing term and
  investment bond, and the renewal-expense unit-cost rows are with-profits endowment,
  unit-linked endowment, term assurance, investment bond, with-profits and unit-linked
  individual pension, and annuity** — there is **no whole-of-life lapse row and no
  whole-of-life renewal-expense unit-cost row**, and **the retrieved instruction file does not
  say where a whole of life block's lapse assumption or per-policy renewal unit cost is
  reported** [REG-R89]. This library does not fill that hole. Two further template facts bear
  on the model: experience need not be shown where it is of low credibility, with a stated
  guideline of **fewer than 200 claims per annum** for an individual line, and only the
  **largest three subcategories by number of policies** are shown [REG-R89] — which is why the
  model point carries `sex` for the O50 cell even though the fetched documents rate that cell
  on age and smoker status only [S1][S4].
- **IR.12.05 / IR.12.06 do not bite either modelled cell.** They are with-profits templates,
  completed per ring-fenced fund which is also a with-profits fund, on a threshold of
  with-profits net BEL **> £500 million** [REG-R90]. Neither RefWOL-UW nor RefWOL-O50 has any
  bonus, asset share or discretionary distribution mechanism [S1][S4][S7][S9][S10], so both
  sit outside them; a participating whole of life (codes 100/101) falls inside, and IR.12.06
  row **R0090 "future costs of financial options such as guaranteed annuity rates"** is where
  such a contract's GAR would be reported [REG-R90]. Neither cell has a GAR.
- **IR.12.01's unit-linked rows are reached only by the legacy design.** R0300 surrender
  value, R0302 nominal value of units allocated and R0304 matching value of units held are
  three quantities distinct from the BEL and from each other [REG-R89]; in this folder they
  exist only for the closed-book unit-linked reviewable variation, the one design here with a
  positive cash-in value [S15].

### Technical provisions

- **Contract boundary — both cells run to death, and neither is cut.** Obligations are
  recognised at the earlier of becoming a party to the contract and cover beginning (TPFR 2.1)
  [REG-R41]. TPFR 3.3 cuts the boundary at a future date only where the firm holds a
  unilateral right to terminate, to reject premiums, or to amend premiums or benefits so that
  they fully reflect the risks. **Neither modelled cell gives the firm any such right**:
  premiums and sum assured are guaranteed for life in RefWOL-UW, changing only on
  customer-initiated cover changes, contractual escalation or disclosure corrections
  [S10][S11], and the O50 cell is guaranteed acceptance with premiums fixed at outset and
  guaranteed never to increase [S1][S4][S7][S9]. So the boundary is **to death** for
  RefWOL-UW, and **to death** for RefWOL-O50 with premiums ceasing at the policy anniversary
  on/after the 90th birthday **[std]** (h) — *premium cessation is a contractual payment
  schedule, not a boundary event; cover continues premium-free for life* [S4][S5][S9], so
  cash flows past T_cess stay inside the boundary and inside the best estimate.
- **The long-term carve-out is assessed at contract level, and does no work here.** TPFR
  3.3's "premiums fully reflect the risks" limb is assessed at portfolio level *except* for
  long-term insurance business "where an individual risk assessment of the obligations
  relating to the insured person of the contract is carried out at the inception of the
  contract and that assessment cannot be repeated before amending the premiums or benefits",
  where the firm "must assess **at the level of the contract**" [REG-R41]. RefWOL-UW is fully
  medically underwritten at outset and cannot be re-underwritten [S10][S11], so the carve-out
  is engaged — but only to confirm a boundary that runs to death anyway, because there is no
  repricing right to cut it at. RefWOL-O50 is not individually risk-assessed at all (no
  medical questions [S1][S4]) and has no repricing right either. TPFR 3.7 makes the test
  demanding in the extreme in any event: premiums fully reflect the risks only "where there is
  **no circumstance** under which the amount of the benefits and expenses payable under the
  portfolio exceeds the amount of the premiums payable" [REG-R41]. **The one design in this
  folder where the boundary question would be live is the legacy unit-linked reviewable
  variation**, where premium and cover are guaranteed only to the first review [S15]; the
  retrieved sources address the carve-out for reviewable-premium critical illness and income
  protection and **do not settle it for a reviewable unit-linked whole of life**, which is
  documented as a closed-book variation and is not modelled — no boundary is asserted for it.
- **Cash flows in scope, and the one that is easy to miss.** TPFR 13.1 requires eight streams
  [REG-R41]. Live here: benefit payments, expenses, premiums and cash flows resulting from
  them, and — the one usually treated as an expense-loading convention — **payments between
  the firm and intermediaries**. Commission is therefore an **in-scope best-estimate cash
  flow**, so the [std] O50 commission (25% of year-1 premiums) and the UW initial commission
  in "Assumption inputs" sit *inside* the BEL, not in a loading; the existence of commission
  is documented (SunLife: an intermediary "paid by commission as a percentage of total annual
  premium" [S1]) while the levels are **[std]**. Not live: salvage and subrogation; payments
  to and from investment firms (nil for both modelled cells — there is no unit fund; the
  stream exists only for the legacy variation [S15]). Item (8) is **policyholder-charged
  taxation only** — **shareholder corporation tax is not a best-estimate cash flow** and
  enters through deferred tax under Valuation 11 instead [REG-R41][REG-R39].
- **Expenses — two bases, and an unreconciled tension.** TP 9.1(1)–(2) require all expenses of
  servicing the obligations and expense and claims inflation [REG-R1]; TPFR 16.1 names
  administrative, investment management, claims management and **acquisition** expenses, each
  including allocated overheads (16.2). **TPFR 16.4: "Expenses must be projected on the
  assumption that the firm will write new business in the future"** — a *going-concern* unit
  cost — while the risk margin's reference undertaking "assumes no new obligations" (TP
  4B.1(5)) [REG-R41][REG-R1]. Both are correct as printed, so a model carries two expense
  bases, and **no retrieved source explains how the reference undertaking's expenses should be
  set given the tension** [REG-R41]. The tension bites this product harder than a
  fixed-term one: premiums are small and level (£30/month at the O50 anchor), maintenance
  inflates, and after premium cessation at age 90 the policy is **pure outgo with no premium
  to carry the expense** — the going-concern-versus-run-off unit cost is then the whole of the
  expense assumption. Nothing in the rules prescribes an inflation index (RPI, CPI or national
  average earnings), a rate, or a per-policy / per-premium split; the 3% p.a. and the
  £30 / £50 per-policy amounts here are **[std]** [REG-R41].
- **The best estimate is normally negative for RefWOL-O50 early on, and nothing floors it.**
  The over-50s guaranteed-acceptance cell is **the paradigm lapse-supported negative reserve**
  in this library; RefWOL-UW is cell- and duration-dependent and less reliably negative
  [REG-R41][REG-R115]. On the Solvency UK ledger the absence of a floor is settled: TP 3.1
  contains no floor, no minimum and no reference to a surrender or account value; TP 2.2
  requires a **transfer value**, which for a profitable portfolio is legitimately negative
  before the risk margin; TP 2.4's risk margin is non-negative by construction and therefore
  offsets but does not floor [REG-R1]. Three product-side confirmations: the Solvency I floor
  (INSPRU 1.2.62R) was **expressly not carried over**, INSPRU 1.2 not applying to a Solvency II
  firm [REG-R115]; a secondary source states "there is no floor related to the surrender value
  specified in the rules" [REG-R118] — **an entry with no recorded URL, cited without one
  rather than with a guessed one**; and the reporting treatment above [REG-R89]. Note the
  product-specific twist: **the surrender-value limb of that debate is moot here**, because
  there is no surrender value at any duration in either modelled cell [S1][S4][S5][S7][S9][S10]
  — what makes the O50 BEL negative is the premium leg inside an unbounded boundary plus the
  lapse-support profit, not a cash value. The sign must be carried unfloored through every
  aggregation; the UK GAAP floor is applied downstream (see "Statutory accounts and tax").
- **The options and guarantees this design actually contains.** RefWOL-UW: terminal illness
  acceleration — an *integral* benefit that pays the same sum assured earlier, not an
  additional decrement [S10][S12]; Increasing Cover escalation with the 2-for-1 premium step
  and the three-declines-forfeits rule [S10]; the Milestone / guaranteed-insurability option
  [S10][S12]; the smoker-status review [S10]; cover reduction [S10]; and the out-of-scope
  Waiver of Premium rider [S10][S11]. RefWOL-O50: the 12-month accidental / non-accidental
  benefit split [S1][S4][S7][S9]; a once-only irreversible premium reduction [S1][S4][S9]; the
  Royal London Payout Promise paid-up conversion [S9]; and the L&G RPI-indexation variant
  whose first declined increase freezes cash sum and premium permanently [S4]. **What is
  absent is the whole class that forces stochastic valuation**: no guaranteed annuity option,
  no guaranteed surrender or paid-up value in the base designs, no financial guarantee of
  investment return, no market value reduction, no bonus [S1][S4][S5][S7][S9][S10]. TPFR
  19.4–19.5 require a scenario-dependent method only where the present value depends on
  expected future outcomes **and on scenario deviation from the expected outcome** [REG-R41];
  the applicability research marks stochastic valuation `(x)` for whole of life, and that mark
  is for the participating and GAO-bearing forms, not for these two. **A deterministic
  valuation is defensible for both modelled cells — but TPFR 19.4 requires the analysis to be
  performed and documented, not assumed** [REG-R41].
- **Dynamic policyholder behaviour is where this product does get caught.** TPFR 11.1 requires
  an analysis of past behaviour and a prospective assessment, taking into account how
  beneficial exercise was and will be, past and future economic conditions and management
  actions — and closes: "**The likelihood shall only be considered to be independent of the
  elements referred to in (1) to (4) where there is empirical evidence to support such an
  assumption**" [REG-R41]. That is the rule against a flat static lapse table. For a contract
  with **no** surrender value the independence case is far easier to sustain than for a
  guarantee-bearing design — but **the Royal London Payout Promise variant defeats it by
  construction** [S9]: once at least half the expected payments have been made, forfeiture is
  strictly dominated by the pro-rata paid-up payout, so the likelihood of discontinuance
  becomes a function of the policy's own state. The "Policyholder behavior modeling" section
  above models it that way. The crossover-aware lapse dial (`β`, off in base) is the other
  moneyness channel, anchored on the FCA's Consumer Duty requirement that communications
  enable informed choice about the over-payment risk [R2].
- **Matching adjustment — neither route reaches this product.** MA 2.2 requires **no future
  premium payments**; both cells have future premiums inside the boundary (for life in
  RefWOL-UW [S10]; to the age-90 anniversary in RefWOL-O50 [S4][S5][S9]). The permitted
  underwriting risks are longevity, expense, revision, mortality or recovery time, and where
  mortality risk is present **the best estimate must not increase by more than 5% under the
  prescribed mortality stress** — a pure death-benefit contract cannot pass that cap
  [REG-R2]. The **eligible-element** route in MA 1.2 is a closed definition — the guaranteed
  element of a with-profits immediate or deferred annuity, or the in-payment element of a
  group death-in-service dependants' annuity or an **income protection** policy — and a whole
  of life is neither [REG-R2]. The applicability matrix accordingly marks **both** MA rows
  `--` for whole of life. Consequence: the discount curve is the **basic** GBP risk-free
  curve, with the volatility adjustment available only on permission and in a currency for
  which the PRA publishes one [REG-R55]; `3D25` (spread on an MA portfolio), the MA
  attestation, MAIA and the MA-breach reduction formula are all out of scope, as are
  IRR.22.02 / IRR.22.03 and the MALIR returns [REG-R91].
- **Discounting: the last liquid point genuinely bites this product.** GBP liabilities are
  discounted at observed rates to the **GBP last liquid point of 50 years**, retained in the
  2025 assessment (EMIR trade-repository data to 31 July 2025, published 28 November 2025,
  effective 1 January 2026) despite failing the trade-count indicator, on bid-ask evidence and
  stability grounds [REG-R56]. A whole of life written at the UW anchor age of 40 has material
  cash flow beyond year 50, so the extrapolation to the ultimate forward rate is not a tail
  detail here — it is a real part of the answer. **No numeric UFR, convergence period or
  Smith-Wilson alpha appears anywhere in this library**: the PRA's monthly technical-information
  spreadsheets were not opened [REG-R54][REG-R55]. A model must take the last liquid point as
  a currency-keyed input, never a constant.
- **Transitionals — legacy block only.** TMTP and TMIR are marked **x** for whole of life
  because long-duration back-books are where they are material; in this folder that population
  is the pre-2016 unit-linked reviewable design [S15], not new business. TMTP reaches only
  obligations that were qualifying obligations on 31 December 2024 [REG-R3]; TMIR only
  *admissible obligations* — contracts concluded **before 1 January 2016** whose technical
  provisions were determined under INSPRU 1.1.16R as at 31 December 2015 and which are **not**
  subject to an MA permission [REG-R57]. **The two are mutually exclusive in both directions**
  [REG-R3][REG-R57], the PRA generally will not consider new TMTP applications [REG-R58], and
  both run off to zero by 1 January 2032 [REG-R57][REG-R59]. TMTP adjusts technical provisions,
  not projected cash flows; TMIR adjusts the discount rate and needs a Solvency I comparator
  run [REG-R57]. **The materiality judgement behind the `x` mark is the research's, not a
  retrieved fact; the legal availability is verified** [REG-R3][REG-R57].

### The risk margin

The formula, the 4% cost-of-capital rate, the `max(λ^t, λ_floor)` taper with λ = 0.9 and
λ_floor = 0.25, the reference undertaking's thirteen assumptions and the [std] drivers
approach are all in `uk/regulatory/technical-notes.md`, "The risk margin" [REG-R1][REG-R4]
[REG-R44]. Three things change *because this is a whole of life*.

- **The taper spends almost the whole projection on its floor.** The shared file records that
  `0.9^t ≤ 0.25` from `t = 14`, and that **this arithmetic is derived from the rule and appears
  in no retrieved source — it must never be cited to [REG-R1], [REG-R4] or [REG-R44]**. A
  three-year contract never reaches the floor; a whole of life issued at the UW anchor age of
  40, with no maturity date [S10], spends the overwhelming majority of its run-off in the flat
  `λ_floor = 0.25` regime. So the risk margin of this product is essentially a
  quarter-weighted, 4%-scaled present value of a very long `SCR(t)` tail — the taper stops
  discriminating between years 14 and 60, and the answer is driven by the **shape and length**
  of the SCR run-off rather than by the taper.
- **The run-off driver is not monotone decreasing in the escalating variant.** Under the [std]
  drivers approach the natural driver for mortality and catastrophe is expected sum assured in
  force, or capital at risk [REG-R62]. For the level cells that decays with `l(t)`. For the
  RefWOL-UW Increasing Cover variant, `SA(y) = SA_0 × 1.05^(y−1)` [S10] rises faster than
  survivorship falls for the first decades, so **the driver rises before it falls** — a proxy
  calibrated to a monotonically decaying run-off understates the risk margin on that variant.
  **[std]** — rationale: this is an arithmetic consequence of the contractual escalation rate
  and the [std] driver choice, not a statement in any retrieved source. For RefWOL-O50 the
  in-force runs down through mortality alone after premium cessation (lapse is zero
  post-cessation **[std]**), so the driver decays slowly and the tail is long.
- **Nothing about this product changes the reference undertaking, and one thing it removes.**
  The reference undertaking applies **none** of the MA, VA, TMIR or TMTP (TP 4B.1(13))
  [REG-R1]. There is no MA here to lose, but a legacy block's TMTP benefit does not carry into
  the risk margin. Two more shared points that a whole-of-life drafter should not restate but
  must respect: the run-off is discounted at `(1 + r(t+1))^(t+1)` on the **basic** curve in the
  currency of the **financial statements**, and TP 4A.3's allocation to lines of business must
  "adequately reflect the contributions of the lines of business… over the lifetime" while
  **no allocation formula is prescribed** [REG-R1] — a firm writing both cells inside LoB 32
  must still split one whole-portfolio risk margin between them, and the rules do not say how.

Because the O50 best estimate is negative early on and the risk margin is non-negative,
`TP = BEL + RM` can change sign purely through the risk margin. Report both legs; never report
technical provisions for this product as a single number.

### SCR — the modules that bite

Module tree, correlation matrices, stress definitions, the gross/net architecture and the
simplifications are in `uk/regulatory/technical-notes.md`, "The standard formula SCR"
[REG-R62]. Below is only what this product's risk profile does to them.

- **Life underwriting `3B` applies; health `3C` does not reach either cell** (`3.2A`)
  [REG-R62]. Neither modelled cell carries a health obligation, so the entire health module,
  the SLT/NSLT branch and IR.26.04 are out of scope [REG-R84].
- **Mortality `3B1.1` — instantaneous permanent +15% relative**, requiring a **full
  revaluation** of the best estimate, applied **only to policies for which the stress increases
  technical provisions without the risk margin** (`3B1.2`) [REG-R62]. This is the dominant
  biometric stress for both cells.
- **Longevity `3B2.1` — instantaneous permanent −20% — is not `--` for a whole of life, and
  that is the first thing to get right.** A whole of life has **no maturity** [S10], so a
  *decrease* in mortality defers the claim; where a cell's reserve is high relative to the sum
  assured — a mature underwritten policy, or a with-profits whole of life — the longevity
  stress can *increase* technical provisions and the `3B2.2` filter admits it [REG-R62].
  **Both `3B1` and `3B2` must therefore be evaluated policy by policy under their respective
  filters, and a whole-of-life book will generally split between them.** The mortality/longevity
  correlation of **−0.25** is the only negative entry in the standard formula as retrieved
  [REG-R62], so that split is not a rounding detail — it is where the book's own
  diversification comes from.
- **Lapse `3B6` — the direction, which is the classic error on this product.** `3B6.1` takes
  the **highest of three** scenarios, and two of them carry directional filters [REG-R62]:
  `3B6.2` **lapse up** is a permanent **+50% relative** increase in option exercise rates,
  capped so the increased rates do not exceed 100%, applying **only to relevant options for
  which exercise would *increase* technical provisions without the risk margin**; `3B6.3`
  **lapse down** is a permanent **−50% relative** decrease, the decrease not to exceed **20
  percentage points**, applying **only where exercise would *decrease* them**. For a
  lapse-supported whole of life the policyholder has paid premiums, there is **no surrender
  value** [S1][S4][S5][S7][S9][S10] and the future claim disappears, so discontinuance
  **decreases** technical provisions: the policy is filtered **out** of `3B6.2` and **into**
  `3B6.3`. **The binding stress on this design is lapse DOWN, not lapse up** [REG-R62]. The
  applicability research bolds lapse-down for whole of life and records that this is a
  refinement the SCR stream's own matrix does not make — that matrix marked lapse-up `x` for
  term, critical illness, income protection, whole of life, with-profits and the unit-linked
  bond uniformly [REG-R62]. The filter is a **per-policy** test, recomputed at each valuation,
  and **the answer flips as a policy matures** [REG-R62]: early, while the O50 best estimate is
  negative because expected future premiums exceed expected future claims, discontinuance
  removes a profitable contract; late, past the crossover, discontinuance extinguishes a
  liability for nothing. Do not store the direction as a product constant.
  - The diagnostic is `7.12(3)` **surrender strain** = *(amount currently payable on
    discontinuance, net of amounts recoverable from policyholders or intermediaries) −
    (technical provisions without the risk margin)*, signed, per policy [REG-R62]. Because the
    amount payable on discontinuance is **identically zero** in both modelled cells
    [S1][S4][S5][S7][S9][S10], the diagnostic collapses to `−TP`, so **the filter test for this
    product is simply the sign of the technical provisions without the risk margin, per policy**.
    **[std]** — rationale: this is arithmetic from `7.12(3)` combined with the zero-surrender-value
    product fact, not a statement in any retrieved source.
  - **Mass lapse `3B6.6(2)` is 40%, and on a purely lapse-supported cell it is nil.** The 40%
    instantaneous discontinuance applies only to policies "for which discontinuance would
    increase technical provisions without the risk margin"; where that filter is not satisfied
    the charge is zero and **the whole `3B6` maximum collapses onto the lapse-down scenario**
    [REG-R62]. The **70%** limb `3B6.6(1)` reaches RAO Schedule 1 Part II **class VII** (pension
    fund management) only, the class III reference in PRA2024/13 having been declared an error
    on 20 December 2024 and deleted with effect from 31 December 2024 [REG-R64][REG-R42];
    nothing in this folder is class VII.
  - **But `SCR-SF 1.2` defines discontinuance to include making a contract paid-up**, and
    `3B6.8` requires the mass event to be based on **the type of discontinuance that most
    negatively affects basic own funds on a per policy basis** [REG-R62]. That is live here:
    the Royal London Payout Promise variant converts a would-be lapse into a **pro-rata paid-up
    liability** once at least half the expected payments have been made [S9], so on that variant
    the worst discontinuance type is paid-up rather than lapse-without-value and the filter
    answer can turn back the other way. The base designs, having no paid-up value
    [S1][S4][S7], offer only lapse-without-value.
- **Life expense `3B4.1` — +10% to the amount of expenses *and* +1 percentage point to the
  expense inflation rate** [REG-R62]. On a contract with no end date the +1pp limb is the larger
  half: the [std] 3% p.a. becomes 4% and compounds over an unbounded horizon against level,
  small premiums that stop entirely at age 90 [S4][S5][S9].
- **Life catastrophe `3B7.1` — +0.15 percentage points absolute (i.e. +0.0015) to the mortality
  rates for the following 12 months only**, with the `7.14` simplification `Σ_i 0.0015 × CAR_i`
  as its exact factor equivalent [REG-R62]. **Product trap:** on RefWOL-O50 the capital at risk
  in policy months 1–12 is **not** the cash sum. Non-accidental death in the moratorium pays a
  return of premiums paid, and only accidental death pays the full sum assured [S1][S4][S7][S9],
  so a `CAR = SA` shortcut overstates the year-1 catastrophe charge by roughly the
  `(1 − δ_acc)` share of the difference. **[std]** — rationale: derived from the contractual
  moratorium split and the `3B7.1` / `7.14` definitions, not stated in any retrieved source.
- **Full revaluation is required, three times over on lapse.** `3B1`–`3B7` all require a full
  revaluation of the best estimate; lapse needs **three complete runs** [REG-R62]. Every one of
  them must preserve the **month-12/13 moratorium discontinuity** — roughly an 11× jump in
  expected death outgo in the worked example above — which an annual-grid revaluation will
  smooth away.
- **Market and counterparty modules, briefly.** Interest rate `3D5`/`3D6` bites hard: the
  requirement is the higher of the summed-up and the summed-down scenarios across currencies,
  each a full revaluation of assets **and** the BEL, and on a 50-year-plus liability the up
  shock's **one-percentage-point absolute floor** and the down shock's rule that it **must be
  nil for negative basic rates** are both live [REG-R62]. Equity, property, spread,
  concentration and currency are asset-side for this product — there is no unit fund and no
  participation, so no market stress feeds back into the liability [S1][S4][S7][S9][S10].
  Counterparty default type 1 `3E13` reaches the product only through reinsurance recoverables,
  which carry the TPFR 24.4 **50% loss-given-default floor** inside the best estimate
  [REG-R41]; this library models no reinsurance.
- **Operational risk has a product-specific consequence worth stating.**
  `Op_provisions = 0.45% × max(0; TP_life − TP_life-ul) + …` — **note the `max(0; ·)`** — so
  during the period when the O50 cell's technical provisions are negative it contributes
  **nothing** to the provisions leg, and `Op = max(Op_premiums; Op_provisions)` falls to the
  **4% of earned life premiums** limb [REG-R62]. The `0.25 × Exp_ul` term is nil for both
  modelled cells and reaches only the legacy unit-linked design [S15].
- **Modules that expressly do not reach this product.** Health underwriting `3C` in its
  entirety; life disability-morbidity `3B3` — there is no disability benefit in either modelled
  cell, though the out-of-scope Waiver of Premium rider [S10][S11] would bring the `3B3.1`
  combined scenario (+35% for 12 months, +25% thereafter, −20% to recovery rates) into a
  Waiver module if one were built, and note that **`3B3` carries no directional filter and no
  persistency limb**, unlike the health version [REG-R62]; life revision `3B5` — there is no
  annuity benefit, and the O50 RPI-indexation variant [S4] escalates a sum assured, not an
  annuity benefit; the 70% mass-lapse limb; `3D25` spread on an MA portfolio; and the
  undertaking-specific parameters, which are available for revision risk only [REG-R65].
- **`Adj_TP` is zero and one run suffices.** The loss-absorbing capacity of technical
  provisions is capped at **future discretionary benefits** (`6.3(1)`), and neither modelled
  cell has any [S1][S4][S7][S9][S10], so `BSCR = nBSCR` and the two-run gross/net architecture
  is unnecessary — a *with-profits* whole of life is what makes it necessary [REG-R62].
  `Adj_DT` (LACDT) does apply, computed on an instantaneous loss of `BSCR + Adj_TP + SCR_op`,
  with the `6.5` transitional having ended **30 December 2025** [REG-R62].

### Own funds, ring-fenced funds and the MCR

- **No ring fence, no surplus funds, no restricted own funds.** Both modelled cells are
  non-profit business in the shareholder fund [S1][S4][S7][S9][S10], so there is no
  ring-fenced fund, no `SCR-SF 9.1` notional-SCR perimeter, no Own Funds 3L deduction and no
  Tier 1 surplus-funds item [REG-R62][REG-R77][REG-R45]. A negative best estimate therefore
  feeds the **reconciliation reserve** directly, and the reconciliation reserve "may be
  positive or negative" [REG-R77].
- **The with-profits fact that is nonetheless about this product name.** Where a whole of life
  *is* written participating, the Surplus Funds Part applies per with-profits fund, and
  **SS13/15 ¶3.1 names whole-of-life policies** as the case where the retrospective
  (asset-share) calculation "might be negative or significantly lower than the value calculated
  using the prospective approach" — making a with-profits whole of life the archetypal
  **prospective-route** contract under Surplus Funds 3.4 [REG-R45][REG-R46]. It does not bite
  either modelled cell, and it is why the applicability matrix bolds the prospective route for
  whole of life.
- **MCR terms.** `TP_l4` (all other long-term obligations) plus `CAR` for both modelled cells;
  `TP_l1` / `TP_l2` (participating, the latter at the formula's only **negative** coefficient,
  −0.052) and `TP_l3` (linked) are reached only by the participating and unit-linked forms
  [REG-R78]. The absolute floor is **£3,500,000** for long-term insurance and the corridor is
  **25%–45% of the SCR** [REG-R78].
- **The per-term zero floor bites this product specifically.** Each `TP_l` term is floored at
  zero **separately**, so while the O50 best estimate is negative the block contributes
  `TP_l4 = 0` while its `CAR` term stays large — **the folk rule that "the MCR is 25% of the
  SCR" fails for pure protection**; check which limb of the corridor binds rather than assuming
  [REG-R78].
- **Capital at risk, and a definition the model must not conflate.** `CAR = max(0, A − B)`
  **per contract**, where A is the amount the firm would currently pay on death or disability
  net of reinsurance **plus** the expected present value of further amounts payable on
  *immediate* death or disability, and B the corresponding best estimate — floored at zero
  **per contract**, calculated at least quarterly [REG-R78]. That requires a "sum payable on
  immediate death" attribute distinct from the projected death benefit stream. **For
  RefWOL-O50 in policy months 1–12 there is no single such amount**: the contract pays a return
  of premiums paid on non-accidental death and the full cash sum on accidental death
  [S1][S4][S7][S9], and **the retrieved rule does not say how to express a cause-dependent
  immediate-death amount as a single `A`**. Recorded, not resolved. Separately, IR.14.01
  C0190 defines capital at risk by reference to **`SCR-SF 7.8` and `7.10`**, a different
  anchor from MCR 3C.1(5) [REG-R89][REG-R78]; **whether the two quantities coincide is not
  stated in any retrieved source**, so a model should carry them as two outputs until it can
  demonstrate otherwise.
- **EPIFP is not required at all.** The expected profit included in future premiums has been
  removed from Solvency UK reporting and disclosure [REG-R77][REG-R86] — which is a real saving
  on a product whose whole economics sit in future premiums.

### Statutory accounts and tax

- **Measurement model.** Under UK GAAP both modelled cells are insurance contracts within FRS
  103's scope — a pure death benefit carries significant insurance risk [REG-R99]. Under
  UK-adopted IFRS 17 the UKEB's stated expectation for the UK market is **GMM for life
  protection business and annuity contracts, VFA for unit-linked and with-profits contracts,
  and PAA for short-term contracts** [REG-R106]. Both modelled cells are non-participating
  protection with no end date, so both fall under the **general measurement model**; the legacy
  unit-linked variation [S15] and any participating form would take the **variable fee
  approach**; the applicability matrix leaves the PAA row blank for whole of life. **IFRS 17
  itself is paywalled and was never read — every IFRS 17 paragraph reference in this library is
  one the UKEB quotes** [REG-R107][REG-R106].
- **Coverage units are a required model output, and this product makes them awkward.** The CSM
  is released to insurance revenue by coverage units reflecting the **quantity of benefits
  provided and the expected coverage period** [REG-R106]. A whole of life has **no contractual
  end date** [S10], so the expected coverage period is itself an output of the mortality
  projection rather than a contract term — the coverage-unit driver has to come from the
  decrement model, not from the reporting layer.
- **DAC — the U.S. story, reversed. This is the error the library exists to prevent.** Company
  law **requires** deferral: SI 2008/410 Schedule 3 **para 13** requires costs of acquiring
  insurance policies incurred in a financial year but relating to a subsequent financial year
  to be deferred, with DAC at assets item **G.II** and its movement at technical account item
  **8(b) change in deferred acquisition costs** [REG-R105]. FRS 103 **¶3.7** likewise:
  acquisition costs "**shall be deferred**", subject to three carve-outs — costs already
  recovered, insufficient net present value of margins, and insufficiently certain future
  premiums or margins — with **¶3.9** amortising over no longer than the recoverability period
  **and in a similar profile to those margins**, no basis being prescribed [REG-R99]. So the
  [std] acquisition costs in these notes (O50: £150/policy plus 25% of year-1 premiums; UW:
  £300/policy plus initial commission) are **a deferred asset in the statutory accounts, not a
  year-one hit — there is no U.S.-style first-year surplus strain in the UK statutory accounts
  of this product**. Three qualifications, each a configuration switch rather than a default:
  - **Note 17 to Schedule 3** excludes DAC to the extent the long-term business provision
    (item C.2) or the linked provision (item D) **already allows for the costs**, explicitly or
    implicitly through anticipation of future income — which is how a zillmerised or
    gross-premium reserve absorbs acquisition costs *inside* the liability instead of showing
    an asset [REG-R105]. Make it explicit, not an accident of the reserve basis.
  - **FRS 103 ¶3.10** prohibits deferral **for with-profits funds** — irrelevant to both
    modelled cells, and its own scope is unsettled: ¶3.1(b) applies ¶¶3.10–3.15 only to
    with-profits business to which the PRA realistic capital regime (INSPRU 1.3 as at 31
    December 2015) applied before 1 January 2016, while ¶3.7 opens "Except as required by
    paragraph 3.10" and IG1.1 makes ¶3.12 optional outside that scope. **Whether the
    prohibition reaches a with-profits fund that was never in the realistic regime is not
    settled by the retrieved text, and neither reading is asserted here** [REG-R99][REG-R100].
  - **Neither of the other two ledgers carries a DAC asset**, for opposite reasons. Under IFRS
    17 acquisition cash flows sit **inside the fulfilment cash flows** and **reduce the CSM at
    initial recognition**, emerging as reduced revenue over the coverage period [REG-R106].
    Under Solvency UK acquisition expenses are simply projected cash outflows inside the best
    estimate (TPFR 16.1), and the Valuation Part recognises no unamortised expense asset (Val
    8.1) [REG-R41][REG-R39].
- **The UK GAAP floor, which this product makes vivid.** FRS 103 implementation guidance
  **IG2.41**: "no policy may have an overall negative provision except as allowed by PRA rules,
  nor a provision less than any guaranteed surrender or transfer value" [REG-R100]. There is no
  surrender value in either modelled cell [S1][S4][S5][S7][S9][S10], so the *surrender-value*
  limb is inert — but the **non-negative** limb is not, and it is exactly where the O50 cell
  sits. **The same policy therefore carries a negative best estimate on the Solvency UK balance
  sheet and a floored provision in the statutory accounts**; a model carries three liability
  measures, not two. Alongside it runs the **liability adequacy test** (FRS 103 ¶¶2.14–2.18):
  the recognised liability less related DAC, compared against a current-estimate projection of
  all contractual and related cash flows including embedded options and guarantees, with **the
  entire deficiency** recognised in profit or loss if inadequate [REG-R99]. For this product
  that test has to run the moratorium and the crossover on current assumptions, and it is the
  route by which adverse experience first writes off the DAC created above.
- **Tax basis — a conflict this document records rather than resolves.** The cross-product
  applicability research assigns whole of life to **BLAGAB, taxed on the I-E basis**
  [REG-R17][REG-R18]. Against that: FA 2012 excludes **protection business** written from **1
  January 2013** from BLAGAB and taxes it on a trading basis, while policies written before
  that date continue as BLAGAB unless an election is made [REG-R18 LAM01080] — and this
  product's own research recorded that **whether a given over-50s or underwritten whole of life
  contract falls within "protection business" as defined turns on issue-date and definition
  details that were not researched** ([unverified]; see `product-spec.md`, "Regulatory
  context"). Both modelled cells are pure protection by design [S1][S4][S7][S9][S10]. **The
  conflict is reproduced, not resolved.** A reference model therefore carries a **per-product
  BLAGAB / non-BLAGAB flag** — the answer, not a tax engine — and must be able to run either
  way [REG-R17][REG-R18].
- **If BLAGAB, one interaction is specific to this product.** The I-E computation (FA 2012 s.73
  steps, in `uk/regulatory/technical-notes.md`, "Statutory accounts and tax roll-forward")
  computes "E" broadly like an investment company's management expenses, **excluding claims and
  reinsurance premiums** [REG-R18 LAM04010]. The **seven-year acquisition-expense spread** at
  FA 2012 s.79 is **repealed for accounting periods beginning on or after 1 January 2023**,
  from which date the deduction follows recognition in the income statement under GAAP
  [REG-R18][REG-R109]. Because FRS 103 ¶3.7 *requires* deferral for this product, the tax
  deduction from 2023 therefore **follows the DAC amortisation profile** — the two ledgers are
  coupled through the amortisation basis, with the s.77(3) disallowance ensuring relief is
  given only once and pre-2023 spread amounts still running off [REG-R18][REG-R109].
- **Policyholder-level tax is unchanged from `product-spec.md`.** The chargeable-event-gains
  regime (ITTOIA 2005 Part 4 Chapter 9, with IPTM as the working interpretation) bites
  surrender-value-bearing designs — here only the legacy unit-linked variation [S15] — and not
  the modern protection-only cells, which have no surrender value to generate a gain
  [REG-R15][REG-R16].
- **Distributable profits are owned by the prudential balance sheet.** For a Solvency-UK
  authorised long-term insurer, CA 2006 **s.833A** substitutes an `A − L − D` formula on
  *prudential* values for the realised-profits test, capped by the accounts' accumulated
  profits [REG-R104]. The two product-specific deductions in `D` — the **ring-fenced fund**
  surplus and the **matching adjustment portfolio** surplus — are **both nil** for these cells,
  which have neither. A distributable-earnings pattern for this product is therefore a
  projection of the Solvency UK balance sheet subject to an accounts-based cap.
- **Deferred tax needs three measures.** FRS 102 Section 29 recognises deferred tax on timing
  differences [REG-R102]; Valuation 11 measures it on **all** assets and liabilities including
  technical provisions, as the difference between the Solvency UK value and the tax value
  [REG-R39]. These are structurally different numbers for the same block, and the O50 cell's
  negative best estimate against a floored UK GAAP provision is precisely where they diverge
  most.

### Traps peculiar to this product

1. **Stressing lapse upward.** The binding `3B6` scenario on a lapse-supported whole of life is
   **lapse down** (`3B6.3`, −50% relative, capped at 20 percentage points), not lapse up, and
   the 40% mass-lapse charge is **nil** where the same filter fails [REG-R62]. The filter is
   per policy and **flips as the policy matures**; with no surrender value the test reduces to
   the sign of technical provisions without the risk margin **[std]**, per `7.12(3)` [REG-R62].
2. **Treating longevity as irrelevant to a death-benefit product.** `3B2.1`'s −20% can increase
   technical provisions on a contract with no maturity, and `3B2.2` admits it; run both
   biometric filters policy by policy [REG-R62].
3. **Setting capital at risk to the sum assured in policy year 1 of RefWOL-O50.** The
   moratorium pays a return of premiums on non-accidental death and the full sum assured only
   on accidental death [S1][S4][S7][S9], which changes both the `3B7.1` / `7.14` catastrophe
   charge **[std]** and the MCR `CAR` input — and **the rule does not say how to express a
   cause-dependent immediate-death amount as a single `A`** [REG-R78].
4. **Assuming a negative best estimate is impossible, or that it must be floored in the
   projection.** It is neither: no Solvency UK floor exists [REG-R1][REG-R115][REG-R118], the
   sign must survive aggregation, and the UK GAAP floor (IG2.41) is applied **downstream**
   [REG-R100]. Two knock-ons: operational risk's `Op_provisions` leg contributes **zero** while
   the provisions are negative, `max(0; ·)` being in the rule [REG-R62]; and the MCR's
   per-term zero floor leaves `TP_l4 = 0` with a large `CAR`, so the corridor limb that binds
   must be checked, not assumed [REG-R78].
5. **Carrying the U.S. "no DAC, first-year strain" framing into the UK accounts.** Deferral is
   **required** by SI 2008/410 Sch 3 para 13 and by FRS 103 ¶3.7 [REG-R105][REG-R99]; the
   note 17 carve-out and the with-profits ¶3.10 prohibition are the only routes back, the
   latter with an unsettled scope [REG-R99][REG-R100].
6. **Proxying the risk-margin run-off with a monotonically decaying driver.** The λ floor of
   0.25 dominates an unbounded run-off, and the Increasing Cover variant's driver **rises
   before it falls** [S10] **[std]**. The `t = 14` floor arithmetic is **derived and appears in
   no retrieved source** — it must not be cited to [REG-R1], [REG-R4] or [REG-R44].
7. **Looking for a matching adjustment.** Neither the whole-contract route (future premiums;
   the 5% mortality cap) nor the eligible-element route (a closed list that does not include a
   whole of life) reaches this product [REG-R2]; the curve is the basic GBP risk-free curve,
   extrapolated beyond the **50-year** GBP last liquid point [REG-R56], and **no UFR value
   appears anywhere in this library** [REG-R54].
8. **Assuming the reporting template has a row for everything.** IR.12.04 gives whole of life
   mortality rows but **no lapse row and no renewal-expense unit-cost row**, and the retrieved
   instruction file does not say where those assumptions are reported [REG-R89]. Likewise, the
   IR.14.01 C0190 capital-at-risk definition (`SCR-SF 7.8`, `7.10`) is **not** the MCR 3C.1(5)
   definition, and no retrieved source says the two coincide [REG-R89][REG-R78].
9. **Resolving the tax basis.** BLAGAB I-E per the applicability research [REG-R17][REG-R18]
   versus the FA 2012 protection-business exclusion for post-2012 business [REG-R18 LAM01080],
   with the "protection business" test itself [unverified] for this product. Flag it per model
   point; do not hard-code an answer.

---

## Valuation and reserve pointers

This library projects **gross best-estimate liability cash flows**. The Solvency UK balance
sheet, the reporting templates, the SCR and MCR components, the statutory accounts and the tax
basis for this product are in **Statutory accounting and capital** above; this section stays a
pointer list for the valuation layers themselves, which consume those flows but are not
reproduced here:

- **Solvency UK best estimate and technical provisions.** The best estimate is the
  probability-weighted average of future cash flows discounted at the relevant risk-free term
  structure, on realistic assumptions, gross of reinsurance (PRA Rulebook Technical Provisions
  3.1) [REG-R1] — exactly what this model's expected cash flows feed; technical provisions =
  best estimate + risk margin, market-consistent (2.3, 2.4) [R3][REG-R1]. Contract boundaries,
  the cash flows in scope, the expense basis and the negative-BEL question for this product are
  in Statutory accounting and capital above, "Technical provisions".
- **Risk margin.** Cost-of-capital method at 4% (Solvency UK rate, effective 31 December 2024
  definitions) [R3], with the life-business risk-tapering factor lambda = 0.9 (floor 0.25) from
  SI 2023/1346 [REG-R4]. It requires an SCR run-off; the formula and the reference undertaking
  are in `uk/regulatory/technical-notes.md`, and what a whole-of-life run-off shape does to the
  taper is in Statutory accounting and capital above, "The risk margin".
- **Solvency UK frame.** Assimilated Solvency II law was revoked 31 December 2024 and restated
  into PRA rules effective the same date; the PRA Rulebook, not EU text, is the operative
  source [R4]. Legacy back-books (the unit-linked variation [S15]) may carry TMTP, which
  adjusts technical provisions, not projected cash flows [REG-R3] — see "Transitionals" above
  for its scope and its mutual exclusivity with the risk-free-rate transitional.
- **Realistic-lapse warning.** A best estimate on realistic assumptions [REG-R1] *embeds the
  lapse-support profits*: raising assumed lapses lowers the BEL of the O50 cell. The FCA's
  articulation of the reliance on lapses [R2] makes lapse the assumption to govern hardest
  (TAS 100 justified-assumptions discipline [R8]). The capital-side consequence — that the
  binding standard-formula stress is lapse **down**, not lapse up — is in Statutory accounting
  and capital above, "SCR — the modules that bite".
- **IFRS 17.** UK-adopted IFRS 17 (adopted 16 May 2022, effective 1 January 2023, replacing
  IFRS 4) applies to IFRS reporters [REG-R38]; the fulfilment-cash-flow engine consumes the
  same projections with different discounting and aggregation layers. Which measurement model
  each cell falls under is in "Statutory accounts and tax" above.
- **Professional standards.** TAS 100 v2.0 (effective 1 July 2023) applies to all UK
  technical actuarial work including this modeling [R8]; TAS 200: Insurance v2.0 (effective
  1 January 2025) applies additionally to insurance technical actuarial work [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order, for a guaranteed-acceptance (O50) block:

1. **Lapse — sensitivity analysis mandatory.** With no surrender value, every lapse is a
   pure profit release; the FCA itself records the reliance on lapses for profitability [R2]. BEL is
   monotonically decreasing in lapse rates; run at 0.5x / 1x / 2x base lapse and at zero
   lapse (the conduct-stress floor). The Payout Promise variant [S9] converts post-halfway
   lapses into paid-up liabilities and collapses most of the lapse sensitivity — model it as
   a separate variant, never as a small adjustment.
2. **Guaranteed-acceptance mortality and anti-selection.** The 120% x ONS loading is a [std]
   placeholder; the true basis is proprietary and the CMI's non-underwritten whole of life
   analysis was pending as of the fetched announcement [R7][REG-R32]. Year-one anti-selection
   interacts with the moratorium: the refund design exists precisely because year-1
   non-accidental mortality is anti-selected.
3. **Longevity past the crossover and past cessation.** Post-90 the policy is pure outgo;
   improvement assumptions (CMI_20xx-style, subscriber-restricted [REG-R30]) directly
   lengthen it. For the UW cell, whole-of-life duration makes the liability improvements- and
   discount-dominated.
4. **Expense inflation vs fixed premiums.** Premiums are small (£30/month anchor) and level;
   maintenance expenses inflate. The expense margin erodes mechanically — a per-policy
   expense assumption error compounds over 20+ year horizons.
5. **Escalation take-up (UW variant).** Premium escalates at 2x the benefit rate [S10]; the
   variant is premium-margin-accretive but lapse-sensitive (escalating premiums into fixed
   incomes); opt-out behavior (three declines end the option [S10]) is unobserved **[std]**.

Known modeling pitfalls:

- **Moratorium boundary.** The month-12/13 discontinuity (~11x jump in expected death outgo
  in the worked example) must not be smoothed by annual-grid interpolation; if projecting
  annually, split year 1 explicitly.
- **Refund base.** The year-1 non-accidental benefit is *cumulative premiums paid*, not the
  cash sum and not an annualized premium; with the arrears rule, claims in the 60-day window
  are further reduced by unpaid amounts [S9].
- **Lapse after cessation.** There are no premiums to stop paying after T_cess; applying a
  lapse decrement there silently destroys liability. Set w = 0 post-cessation **[std]** (and
  in paid-up states).
- **Aviva variant double-count.** The 2x applies to *accidental* death on/after the first
  anniversary only [S7]; applying it in year 1 (where accidental already pays 1x SA in the
  base plans, and the Aviva year-1 accidental benefit is 1x the Life Insurance Amount [S7])
  or to all deaths overstates outgo.
- **Anti-selective options (UW).** Milestone-benefit increases without underwriting [S10]
  and smoker-status reviews [S10] are exercised against the office; excluding them is a
  [std] scope choice that understates tail risk on large-sum business.
- **Terminal illness timing (UW).** TI pays the same amount earlier; ignoring acceleration
  understates the present value slightly. Do not model TI as an *additional* decrement —
  it accelerates the death benefit, it does not add one [S10][S12].
- **Basis mixing.** The O50 cell uses a population-plus-loading basis, the UW cell an
  assured-lives shape [R6][REG-R32]; feeding either cell the other's basis produces
  plausible-looking but wrong margins (the FCA's £71.73 vs £8.10 differential [R2] is the
  scale of the error).
- **Claims interest.** Excluded [std]; if added, it is a settlement-lag uplift at BoE − 0.5%
  (floor 0.5%) on death claims [S1][S9], not a discounting change.
