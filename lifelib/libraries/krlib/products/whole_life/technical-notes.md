# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite whole life assurance
(*jongsin boheom*, 종신보험) of `product-spec.md` (same directory) into a reference
liability cash-flow projection on paper, and then into `WholeLife_KR_A` beside it. **They
describe no single insurer's contract.** [S#] and [R#] tags resolve against `sources.md`,
whose numbering is carried verbatim from `_research/whole-life.md` and is frozen; [REG-R#]
tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R60 numbering is
separate and also frozen. **[std]** marks a standardization introduced for the reference
implementation; [unverified] marks a claim that could not be confirmed against a retrieved
document. **Every parameter value here is identical to `product-spec.md`'s**, and every
number in the worked example is read off the shipped model rather than recomputed by hand.

Three quantities appear here that the specification names but does not fix, all three
internal to the surrender-value and expense construction it defers to this document: the
gross-to-net loading `θ`, the acquisition-cost ratio `a` against the 표준해약공제액 cap, and
the first-year commission share `c₀`. Each is **[std]**, and each is derived, bounded or
calibrated below rather than asserted.

**This is the library's savings/protection chassis.** Five mechanics are specified once,
here, and inherited rather than restated:

- the **계약자적립액** (*gyeyakja jeongnibaek*, the policyholder account) recursion, the
  contractual successor of the 보험료적립금 (*boheomnyo jeongnipgeum*, policy reserve);
- the **해약환급금** (*haeyak hwangeupgeum*, surrender value) and its 해약공제액, capped by
  the **표준해약공제액** of 보험업감독규정 별표 14 [REG-R20];
- the **무해지환급형 / 저해지환급형** suppressed forms — nil, or a stated fraction `k`,
  during 납입기간, stepping up at 납입완료. **A cliff, not a curve**, carried as a model
  point column so the suppressed and the ordinary run appear side by side in one
  projection;
- the **보험계약대출** (policy loan) as a modelled state, unavailable during 납입기간 on a
  무해지환급형 contract because there is no value to lend against; and
- **보험료 납입면제** (premium waiver), a distinct in-force state in which premiums cease
  and are **deemed paid** for benefit and surrender-value purposes.

The [CI technical notes (CI보험)](../ci_insurance/technical-notes.md) inherit the whole of
it and add an accelerated critical-illness payment; the [pension savings technical notes
(연금저축보험)](../pension_savings/technical-notes.md) inherit the accumulation half. The
[term life technical notes (정기보험)](../term_life/technical-notes.md) carry the
protection chassis and its 갱신형 / 비갱신형 split, and share this document's
surrender-value regime, because 감독규정 제7-69조 and 제7-70조 apply 제7-65조 through
제7-68조 to 장기손해보험 and to 제3보험 *mutatis mutandis* — **one surrender-value regime
governs all ten `krlib` products** [REG-R19].

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  death claims, surrender benefits, 감액 proceeds, expenses and commission — undiscounted
  and gross of reinsurance. Korea runs **three** measurement bases over one such stream and
  all three are live: IFRS 17 (K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS
  in the same quarter [REG-R13], and the **해약환급금준비금**, which has no counterpart
  anywhere else in this repository [REG-R11]. **Discounting, the risk adjustment, the CSM,
  요구자본 and every reserve are out of scope** and are cited, not reproduced — see
  *Valuation and reserve pointers*.
- **Projection frequency.** **Annual**, on policy years running 계약해당일 to 계약해당일
  (`WholeLife_KR_A`). The permission is explicit rather than assumed: 감독규정
  제7-65조제2항 allows the 계약자적립액 of a monthly-premium contract to be computed on an
  annualised premium basis — 「연납보험료를 기준으로 하여 산출할 수 있다」 [REG-R18]. The
  composite has no intra-year contractual structure on the annual grid: the sum assured is
  level for life, the premium is level, and the one date inside a year that matters — the
  **납입완료일** — is an anniversary by construction.
- **What the annual grid approximates [std].** 제7-66조제1항제4호 accrues the account
  **monthly before 납입완료 and daily afterwards**; both formulas render as images in the
  고시 and did not extract, so the annual step is a stated approximation rather than a
  reproduction [REG-R19]. Two consequences travel with it: the 14-day
  **납입최고(독촉)기간** collapses into the anniversary, so a lapse is dated to the policy
  year [S5 제25조] [REG-R25 제26조]; and **미경과보험료**, required on termination by
  제7-66조제5항 [REG-R19], is not added, because on an annual grid with premiums in advance
  and surrenders at the anniversary there is none **[std]**.
- **Timing conventions [std].** Premium at the **start** of each policy year, in advance,
  for years 1 … m, on the paying cohort only; maintenance expense, the premium-related
  expense and renewal commission at the start of each year; acquisition expense and initial
  commission at issue; death claims and claim expenses at the **end** of the policy year of
  death; surrenders and any 감액 at the **end** of the policy year, **after** deaths, on
  the surrender value at that anniversary; 부활 at the **start** of the following year.
- **Age basis: 보험나이.** 보험나이 (*boheom nai*, insurance age) is the 만 나이 at the
  계약일 with a fraction under six months discarded and six months or more rounded up, and
  it increments on each **계약해당일** rather than on the birthday [S5 제21조] [REG-R25
  제21조]. An annual grid stepped on anniversaries therefore ages the policy correctly by
  construction, and the attained age in year `t` is `x + t − 1` exactly. **The table does
  not share that basis and no conversion is applied [std]:** the statistics
  `mort_table.csv` is calibrated against [REG-R38] are on **만나이**, and no public mapping
  exists. The six-month rule means the two differ for **half of all issue dates**, so the
  model reads the table about half a year of ageing too young — worth roughly 4.6% of `q`
  between attained ages 40 and 60, against a 9.3% step for a full year. Named, not hidden.
- **Currency.** KRW throughout, written ₩ with thousands separators and the Korean
  만원 / 억원 convention alongside where a Korean reader expects it: the anchor's
  ₩100,000,000 is 1억원. `run.py` prints `KRW` and pure ASCII.
- **Model points.** Single-policy, projected on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. `point_id` parameterizes `Projection` and
  **`point_id = 1` is the worked-example anchor cell.** Ten points ship; no aggregation
  logic is specified here.
- **Termination and horizon.** There is no expiry, no 만기보험금 and no survival benefit at
  any age [S1] [S2] [S4] [S8]. The projection runs to the **terminal age of the mortality
  table**: `T = ω − x + 1` with **ω = 115** for both sexes, the first age at which
  `q(ω) = 1`. ω is itself **[std]** — the 제10회's terminal age is no more public than its
  rates [REG-R33] [REG-R34]. Every remaining life dies in year `T`, nothing is paid there
  but the death benefit, and **there are no tail states.**
- **Contract boundary.** The premium is level and guaranteed for the whole of 납입기간 with
  no unilateral repricing right on a 금리확정형 contract [S2] [S8], so the whole contract
  sits inside any defensible boundary and no boundary test is implemented. (The question is
  real on this library's **갱신형** products and is specified in [term life
  (정기보험)](../term_life/technical-notes.md), not here.)
- **Rounding.** Intermediate values at full double precision; displayed cash flows and
  surrender values to **two decimal places [std]**, policy counts to six or ten, rates to
  eight or ten — the precision `tests/test_whole_life_kr.py` asserts. Contractual amounts a
  policyholder receives are integral won; the model does not round them, a
  probability-weighted expected value having no contractual denomination.
- **Sign convention.** `net_cf` is **income-positive** — premiums less claims, claim
  expenses, expenses and commission. That is both these notes' sign and the library-wide
  one, so there is **no** outgo-positive `liability_cf` companion: one stream, one sign,
  one name.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `WL-KR-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, **보험나이**, 15–65 | **40** |
| `sum_assured` (`SA`) | KRW, ₩10,000,000–₩1,000,000,000 in ₩1,000,000 units | **100,000,000** (1억원) |
| `prem_term` (`m`) | int years, or **0 for 전기납 (종신납)** | **20** |
| `premium_annual` (`G`) | KRW, level for years 1 … m | **2,776,140** |
| `cv_floor_ratio` (`k`) | 해약환급금 suppression factor, 1.00 / 0.50 / 0.30 / 0.00 | **0.50** — 저해지환급형 |
| `prem_susp_ratio` | the suppressed form's premium as a fraction of the 표준형's | **0.90** |
| `int_basis` | enum {`fixed`, `linked`} — 금리확정형 / 금리연동형 | `fixed` |
| `decl_rate` | 공시이율 on a `linked` point; unused on a `fixed` one | 0.025 |
| `lapse_basis` | enum {`loglinear`, `flat`} — the FSS 원칙모형 or the level comparison | `loglinear` |
| `waiver_rate` | 납입면제 incidence p.a. during 납입기간 | 0.0 |
| `loan_util` / `loan_year` | 보험계약대출 take-up fraction, and the year of the draw | 0.0 / 0 |
| `bonus_rate` | 유지보너스 credited at 납입완료, as a fraction of premiums paid | 0.0 |
| `reduce_year` / `reduce_frac` | 감액 year, and the fraction of `SA` reduced | 0 / 0.0 |
| `reinstate_rate` | 부활 proportion of the previous year's lapses | 0.0 |
| `mort_be_factor` | multiplier on the table rate | 1.0 |

**There is no issue-date attribute**, and that is a product fact rather than an omission:
the projection runs on policy years, 보험나이 is fixed at the 계약일 and increments on the
계약해당일 rather than on the birthday [S5 제21조] [REG-R25 제21조], and the one intra-year
date that matters is the 납입완료일, an anniversary by construction.

`prem_term = 0` denotes **전기납 (종신납)**: `m` becomes the whole projection, no 납입완료
date exists, the suppressed period runs for life and **the cliff never happens** —
`cv_mult(t) = k` for every `t`. That configuration must be in the shipped table because it
is the one in which the product's signature mechanic is absent by construction
(`point_id = 5`).

**The anchor premium is derived from a sourced one, not invented.** DB생명 publishes
₩257,050 a month for the 표준형 at exactly this cell — 남 40세, 1억원, 20년납, 월납 [S4] —
and the annual figure is 12 × that = ₩3,084,600 **[std]**, which is `point_id = 2`. The
anchor's ₩2,776,140 is **0.900 × ₩3,084,600** [std], the 처브라이프 observation at that
exact factor [S1], inside the observed 81.5%–95.4% envelope [S1] [S2] [S4] [S6]. No carrier
publishes an annual-mode scale, so the modal discount a real 연납 rate would carry is **not
applied**: the annual premium is slightly overstated and the first year's interest credit
correspondingly understated. Stated, not corrected.

Two attributes need a note. `cv_floor_ratio` is the **suppression factor `k`** and
`refund_ratio(t)` is the **환급률**; the cross-library register retired the bare name
`cv_ratio` because a Korean whole life model carries two ratios on the same object. And
`prem_susp_ratio` is a **price** input, not a value input: it scales the premium, never the
surrender value. The model's own loading rule reproduces the anchor premium to **0.0010%**
— ₩2,776,167.83 against ₩2,776,140 — and the projection uses the model-point value.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of policy year `t`; `pols_if(1) = 1` | annual recursion |
| `pols_if_pay(t)` | Of those, the cohort still **paying premium in cash**; the weight on premium and commission | annual recursion |
| `pols_waived(t)` | Of those, the cohort in the **납입면제** state: in force, paying nothing, accruing value as if paying | annual recursion |
| `pols_death(t)`, `pols_lapse(t)` | Expected deaths and 해지 in year `t` | decrement |
| `pols_surr(t)` | Of the lapses, those **paid** a surrender value — `pols_lapse(t)` less next year's 부활 | decrement |
| `pols_reinstate(t)` | **부활** at the start of year `t`, from year `t − 1`'s lapses | decrement |
| `mort_rate(t)` | 적용위험률 at attained 보험나이 `x + t − 1`, times `mort_be_factor` | table lookup |
| `lapse_rate(t)` | Annual 해지율, plus the bonus-date spike where one applies | assumption |
| `waiver_rate(t)` | 납입면제 incidence, during 납입기간 only | assumption |
| `pol_val_pp(t)` | `V(t)` — the **계약자적립액**, the 표준형 twin's account at anniversary `t` | forward recursion |
| `surr_chg_pp(t)` | `SC(t)` — the **해약공제액**, bounded by the 표준해약공제액 | closed form |
| `cv_std_pp(t)` | `W(t)` — the **표준형 twin's 해약환급금**, `max(0, V − SC)` | closed form |
| `cv_pp(t)` | `CV(t)` — the **해약환급금 actually payable**, after the multiplier and any 유지보너스 | closed form |
| `cv_susp_pp(t)` | `k W(t)` — the suppressed value at **every** `t`, published so the step is visible on both sides | closed form |
| `cum_prem_pp(t)`, `refund_ratio(t)` | Premiums paid to `t`; the **환급률** `CV(t) / cumprem(t)` | recursion / ratio |
| `loan_pp(t)`, `loan_draw(t)` | **보험계약대출** balance at the start of year `t`; the draw in year `t` | annual recursion |
| `sa_factor(t)`, `sum_assured_at(t)` | The 감액 step-down factor and the sum assured in year `t` | closed form |

Three of these carry design decisions worth stating explicitly.

**There is exactly one policy value in this model.** `pol_val_pp` is the 표준형 twin's
계약자적립액 and the suppression is a multiplier on the surrender value derived from it —
not a second account run, not a second reserve basis. Every carrier that sells the form
names the comparison product in the same sentence and says it is not sold: 「"표준형"의
경우는 … 동일한 보장내용으로 **해지율을 적용하지 않고** … 계산된 상품이며 … 비교안내를
위한 종목으로 **실제로 판매하지 않습니다**」 [S1], with the same sentence at three more
carriers [S2] [S3] [S4]. The published grids confirm it arithmetically: every pre-완납
suppressed/표준형 ratio is exactly `k` (1,164,500 / 2,329,000 = 0.50000 [S1]; 1,526,128 /
5,087,095 = 0.30000 [S4]) and every post-완납 pair is **identical to the won** [S1] [S4]
[S6].

**`pols_waived` is a state, not a rate adjustment.** The waiver's wording forces it:
「그러나 이 경우에도 보험료가 … 정상적으로 납입된 것으로 하여 사망보험금 및 해지환급금을
계산합니다」 [S2], verbatim at two more carriers [S3] [S8]. A waived policy pays nothing and
accrues everything, so it cannot be represented by scaling the premium; and on a suppressed
form it is **the only route to the cliff the policyholder does not have to fund**.

**`pols_reinstate` makes lapse non-terminal**, because the 약관 counts the surrender value
as undrawn 「… 또는 **해지환급금이 없는 경우를 포함**합니다」 [S5 제26조] [REG-R25 제27조] —
so **a 무해지 contract is always reinstatable within three years.** Treating every exit as
terminal understates later-duration in force; the parameter exists and is zero in the base
run.

The base run carries **no loan, no waiver, no bonus, no 감액 and no 부활**, so
`loan_pp ≡ 0`, `pols_waived ≡ 0`, `pols_surr ≡ pols_lapse`, `sa_factor ≡ 1` and every
benefit is gross. Each module is exercised on at least one shipped model point.

---

## Assumption inputs

Three classes, kept apart on purpose. The split is not a modelling nicety in Korea: the
**보험가격지수** exists precisely because a Korean consumer cannot see the pricing basis
[REG-R22 제7-45조제7항], the 산출방법서 that holds the guaranteed elements is a filed but
**unpublished** 기초서류 [REG-R2], and the November 2024 계리가정 decision draws a hard line
between an assumption an insurer may choose and one the supervisor now sets [REG-R27].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 사망보험금 | `SA`, **평준형**, level for life, payable on death at any time, net of `L(t)` | [S5 제34조] [S6] [REG-R25 제33조] |
| 보험기간 | **종신** — no expiry, no 만기보험금, no survival benefit at any age | [S1] [S2] [S3] [S4] [S6] [S8] |
| Premium `G` | Level and guaranteed for years 1 … m; **none thereafter** | [S2] [S8] |
| Severe-disability benefit | **None.** Korea puts no 고도장해보험금 at the sum assured on this chassis | [S2] [S3] [S6] [S8] |
| 보험료 납입면제 | On a **50% 장해지급률** aggregated across body parts from one cause, accident or disease; premiums cease and are **deemed paid** to the end of 납입기간 for benefit *and* surrender-value purposes | [S2] [S3] [S6] [S8] [REG-R25 부표 3] |
| 해약환급금 identity | **계약자적립액 − 해약공제액**, floored at zero — a negative difference 「이를 영(零)으로 처리한다」 | [S2] [S8] [REG-R19 제7-66조제1항제1호] |
| 해약공제액 | 미상각신계약비, 「이미 지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라 계산한 금액」, **capped at the 표준해약공제액** | [S5 제2조] [S8] [R6] [REG-R19] [REG-R20] |
| 표준해약공제액 | **연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000**; for a 보장성보험 the 계수 is the 보험기간 capped at **20**, and the 연납순보험료 is recomputed on a **20년납** footing for a term of 20 years or more | [REG-R20 별표 14 주2·주3] |
| 보험가입금액 entering the cap | The 일반사망보험금, taken **before any 체증 or 체감** | [REG-R21 별표 15 제3호·제8호] |
| 해약공제기간 | **납입기간 or 신계약비 부가기간, capped at 7년** | [REG-R19 제7-66조제1항제2호] |
| Suppression factor `k` | Applies for elapsed duration **< 납입기간**; `k = 1` from 납입완료 | [S1] [S4] [S6] [S7] [S8] |
| What `k` multiplies | The **표준형 twin's** 해약환급금 — a non-marketed comparison product with identical benefits priced **with the lapse assumption switched off** | [S1] [S2] [S3] [S4] |
| Post-cliff equality | From 납입완료 the suppressed and 표준형 values are **identical** in every published grid | [S1] [S4] [S6] |
| Clawback | Where premiums falling in the suppressed period were unpaid, they must be made good before the post-cliff basis applies | [S2] [S3] [S8] |
| Waived premiums | Count as **paid** for the surrender-value computation | [S2] [S3] [S6] [S8] |
| 보험계약대출 limit | Within the 해약환급금 net of existing principal and interest, 「그러나, 순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수 있습니다」 | [S5 제34조] [REG-R25 제33조] |
| Loan settlement | Deducted from any benefit, from the 해약환급금, and **즉시** on 해지 | [S5 제34조] [REG-R25 제26조·제33조] |
| 감액 | The reduced portion is **treated as surrendered** and pays the corresponding 해약환급금 | [S5 제20조] [REG-R25] |
| 납입최고(독촉)기간 | **14일 이상** from the day after the 계약해당일; the contract is 해지 the day after it ends | [S5 제25조] [REG-R25 제26조] |
| 부활 | Within **3년** of 해지, on fresh 고지 and arrears with interest; available **even where the 해약환급금 was nil** | [S5 제26조] [REG-R25 제27조] |
| 면책 — suicide | No death benefit where the insured takes their own life within **2년** of the 계약일; zero incidence modelled | [S1] [S3] [S6] [S7]; [REG-R49 제659조] [REG-R50 제732조의2] |
| Refused claim | The insurer must still pay 「보험수익자를 위하여 적립한 금액」 — in practice the 계약자적립액 | [REG-R50 제736조] [REG-R25 제22조] |
| Minimum death benefit | At least cumulative premiums paid, except where the 납입기간 ends at age 80 or below — which the anchor (완납 at 보험나이 60) satisfies | [REG-R16 제7-60조제9호] |

**The suppression is a regulatory dispensation, not a contractual gimmick**, and the
condition attached to it is what makes the lapse vector a first-class model input.
제7-66조제4항 permits an insurer to pay **less than** the 제1항 value that 별표 14 floors
only where the premium or benefit was computed 「**최적해지율**을 사용하여」 — using a
best-estimate lapse rate [REG-R19]. 제4항제1호 bars the form outright for a 변액보험 (so
`VA_KR_S` may not use it), and 제4항제2호 attaches two further conditions **only where** the
surrender value during 납입기간 is **less than 50%** of an otherwise identical 표준형
product's [REG-R19]. **The anchor sits exactly at that threshold and not below it**, which
is the most likely reason three independent carriers chose 50% [S1] [S6] [S7].

### (b) Insurer-discretionary current elements

Unlike a UK guaranteed-premium term policy, this class is not nearly empty — it is where
the product's economics live. Korea differs from Japan in one respect that matters
throughout: **the pricing rate is published**, in the 상품요약서, and so is a sample of the
적용위험률 and the 적용해지율 envelope [S2] [S8]. What is *not* published is the
산출방법서 itself, so a disclosure of a parameter is what this library has, never the
filing [REG-R2].

| Input | Model value | Basis |
|---|---|---|
| 예정이율 `i` (`prem_int_rate`) | **2.50% p.a., 연복리, flat** | Disclosed range 2.25%–2.75% at six carrier documents [S1] [S2] [S5] [S6] [S7] [S8]; centre **[std]**, and equal to the 2026 평균공시이율 [REG-R48] |
| 최저보증이율 (`min_guar_rate`) | **0.75% p.a.**, floor on a `linked` point | Stated verbatim in the one full 약관: 「최저보증이율은 연복리 0.75%를 적용」 [S5 제32조] |
| 공시이율 (`decl_rate`) | **2.75%** on the one `linked` model point, held flat | Mechanism sourced [S5 제32조] [REG-R18 제7-65조제3항] [REG-R24 별표 27]; the level **[std]** |
| Accrual rate `i_acc` (`acc_int_rate`) | `i` on a 금리확정형 point; `max(공시이율, 최저보증이율)` on a 금리연동형 one | [REG-R16 제7-60조제10호] [REG-R18] |
| 보험계약대출이율 `i_L` | **예정이율 + 1.5% = 4.00% p.a.**, compound, flat, and a **vintage** rate | Formula at three carriers independently [S9] [S11] [S13]; level **[std]** |
| 보험계약대출 limit | **80%** of the *payable* 해약환급금 | Observed 50%–85% [S11] and 50%–80% [S13]; pick **[std]** |
| Gross-to-net loading `θ` (`prem_loading`) | **1.4642** | **[std]**, calibrated once so the 표준형 anchor reproduces 12 × ₩257,050 [S4] |
| Acquisition-cost ratio `a` (`acq_cost_ratio`) | **1.00** — 계약체결비용 set **at** the 표준해약공제액 | **[std]**, bounded by the 1.4 × tolerance of 제7-45조제11항 [REG-R22] |
| First-year commission share `c₀` (`comm_init_share`) | **0.65** of 계약체결비용, capped at one year's premium | Cap sourced [REG-R22 제4-32조제5항]; share **[std]** |
| Renewal commission `c_r` | **3.0%** of premium, years 2 … m | **[std]** |
| 계약관리비용 per policy `e` | **₩60,000** p.a. for life, inflating at 2.0% | **[std]** |
| 유지관련비용 on premium | **2.0%** of premium collected | **[std]** |
| Claim handling expense `ec` | **₩300,000** per death claim | **[std]** |
| Expense inflation | **2.0% p.a.**, the Bank of Korea target | **[std]** |
| 유지보너스 | **13.8%** of total premiums at 납입완료 on the one 7년납 point | Published 10.8% / 13.8% / 15.0% by 납입기간 [S7]; off in the base run |
| 계약자배당 | **None.** The composite is 무배당, as is every product in the retrieved set | [S2] [S8] [R8]; frame not implemented [REG-R12] |

**Why the expense parameters are all [std], and what bounds them.** Both 상품요약서 in the
set define 계약체결비용 and 계약관리비용 in words and then give **no number** [S2] [S8];
the 약관 defines 부가보험료 and 해약공제액 by reference to the 산출방법서 [S5 제2조]
[REG-R2]. **No Korean expense rate as a percentage of premium was obtained from any source
in this research pass.** Four public handles bound the standardization instead, and the
model is built to sit inside all four:

1. **The 표준해약공제액 itself** [REG-R20]. The model sets 계약체결비용 exactly at it —
   `acq_cost_ratio = 1.00` — so the acquisition cost is by construction recoverable within
   the statutory surrender charge and no more.
2. **The 1.4 × disclosure tolerance** of 제7-45조제11항, under which a whole-life
   death-benefit 보장성보험 need not publish a 계약체결비용지수 provided its 계약체결비용
   stays within 1.4 × the 표준해약공제액 [REG-R22]. On the anchor that outer bound is
   ₩4,349,380.75 and the model sits at ₩3,106,700.54, comfortably inside it.
   `check_acq_cost_cap()` asserts it.
3. **The first-year remuneration cap** of 제4-32조제5항: first-year distributor remuneration
   may not exceed the first year's expected premium, with the projected one-year surrender
   value added to the commission side where the contract deducts 80% or more of the
   표준해약공제액 — which is exactly what a 무·저해지 design does [REG-R22] [REG-R29]. The
   model caps `comm_init_pp()` at `1.00 × premium_pp()` and the same check asserts it. On
   the anchor the cap does **not** bind: 0.65 × ₩3,106,700.54 = ₩2,019,355.35 against a
   premium of ₩2,776,140.
4. **The 보험가격지수**, whose observed range of **85.4%–110.9%** across two carriers at
   this very cell bounds how far a Korean whole-life product's total loading can sit from
   the industry mean [S2] [S8].

The 60%-a-year instalment structure of 제4-32조제8항 [REG-R22] [REG-R29] governs how the
cost is *paid* rather than how much it is; it is cited and not modelled.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality.** The 제10회 경험생명표 (*gyeongheom saengmyeongpyo*), produced by 보험개발원
and applied to new business from **2024-04**, is **not published in full**: only 평균수명
and 기대여명 are released, and even those reached this library through a trade newspaper
[REG-R33] [REG-R34]. The 참조순보험요율 the bureau files for life mortality are likewise
never published, becoming visible only as the 보험가격지수 [REG-R4] [REG-R22]. **There is
therefore no published Korean insured mortality rate to anchor a proxy on** — the sharp
contrast with `jplib`, where the 生保標準生命表 is free to read and only its redistribution
is restricted.

`mort_table.csv` is accordingly a **[std] construction** and its `provenance` column says
so row by row. Three kinds of row:

| Row kind | Construction | Basis |
|---|---|---|
| **ANCHOR** (보험나이 20, 40, 60) | The **mean** of the only two Korean insured rates in the public domain at those ages | Rates sourced [S2] [S8]; the mean **[std]** |
| **CONSTRUCTED** below 60 | Log-linear in `ln q` between anchors | **[std]** |
| **CONSTRUCTED** above 60 | Gompertz in `ln q` with a quadratic deceleration, two parameters solved so 65세 기대여명 is **23.7 (M) / 27.1 (F)** and `q(115) = 1` | Targets from [REG-R38] plus the reported 제10회 gap [REG-R33]; the form **[std]** |
| **TERMINAL** | `q = 1` at **ω = 115** | **[std]**; the 제10회 terminal age is not public |

Two unfitted checks are worth recording because neither was used in the calibration: the
resulting **평균수명 at birth is 85.4 (M) / 90.4 (F)** against the 86.3 / 90.7 reported for
the 제10회 [REG-R33]. **No row of this file is a 경험생명표 value and the table must never
be presented as one.**

| Input | Value | Basis |
|---|---|---|
| Base table | `mort_table.csv`, sex-distinct, `q` at attained 보험나이 `x + t − 1` | **[std]** on [S2] [S8] [REG-R33] [REG-R38] |
| `mort_be_factor` | **1.00** in the base run | **[std]** |
| Terminal age ω | **115**, both sexes | **[std]** |
| Improvement overlay | None | **[std]** |
| 만나이 → 보험나이 conversion | **None applied** | **[std]**; no public mapping exists |

`mort_be_factor = 1.00` is a choice, not a default: **the base run is a pricing-table run,
not a best estimate.** The two disclosed grids differ by **10%–23% at every age and sex** —
남 40세 0.000780 [S2] against 0.00092 [S8], 여 60세 0.001730 against 0.00214 — so they
**bracket** rather than fix a level, and one is labelled 「무배당 **예정 경험**사망률」, the
giveaway that it is a 경험생명표 derivative carrying a 무배당 loading rather than the table
[S2] [S8]. A production basis would sit below 1.00 and move claims proportionately;
`point_id = 10` runs at 0.90 so the lever is exercised.

**Lapse — and this is the assumption the whole product turns on.** Two independent public
bases exist in Korea, they are disclosed, and they do not agree.

The **pricing basis is published in the 상품요약서**, which has no counterpart anywhere else
in this repository. One carrier: 「「…(해지환급금 일부지급형)」에 적용한 해지율은
**1%~10%**이며, **일반형에는 적용해지율이 적용되지 않습니다**」 [S2]. Another: 「적용해약률은
… 보험료 납입기간 중 **연 0%~연 13.4%**를 적용합니다. 보험료 납입기간 이후에는 **연
1.0%~연 11.3%**의 해약률을 적용합니다」 [S8]. Neither publishes the *shape*, only the
envelope.

The **valuation basis was set by the supervisor in November 2024** and it is far lower. The
problem the FSS named: with no experience on 무·저해지 business, insurers assumed high lapse
right up to 완납 on contracts where lapsing pays nothing, booking CSM that would never be
realised and pricing low enough to tilt the market toward the form [REG-R27] [R3]. The
remedy: among models converging to zero at 완납 the **로그-선형 (log-linear) 모형** is the
**원칙모형**, with a convergence point of **0.1% at 납입완료**, an ultimate rate of **0.8%**
after it, permission to depart only against audited disclosure of the difference in CSM,
BEL, K-ICS ratio and net income, and an **additional lapse of at least 30%** at a 단기납
bonus date [REG-R27] [R3] [R7].

`lapse_table.csv` therefore ships **both**, as three parameters each rather than a rate per
policy year — the convergence point is 납입완료, which is a model point attribute:

| `lapse_basis` | `first_year_rate` | `completion_rate` | `ultimate_rate` | Basis |
|---|---|---|---|---|
| `loglinear` | 0.10 | 0.001 | 0.008 | Endpoints [REG-R27] [R3] and the top of the disclosed 1%~10% envelope [S2]; the interpolation **[std]** |
| `flat` | 0.04 | 0.04 | 0.04 | **[std]** level comparison basis, inside both disclosed envelopes [S2] [S8] |

    w(t) = w1 * (wm / w1) ^ ((t - 1) / (m - 1))      for 1 <= t <= m
    w(t) = wu                                        for t > m

On the anchor that is `w(1) = 0.10` exactly, `w(20) = 0.001` exactly, and a flat 0.008 from
`t = 21`. **The 표준형 twin is priced with no lapse assumption at all** [S1], which is why
the `flat` basis is level rather than shaped: it is a comparison, not a second estimate.

**Everything else in class (c).**

| Input | Base value | Note |
|---|---|---|
| 납입면제 incidence `u(t)` | **0** in the base run; **0.4% p.a.** during 납입기간 on `point_id = 7` | **[std]**. No Korean 장해 incidence at the 50% 장해지급률 threshold was retrieved |
| 보험계약대출 take-up | **0**; a single draw of 100% of the contractual room at `loan_year` on points 3 and 6 | **[std]**. No Korean take-up data is public |
| Loan repayment | **None modelled** | **[std]**. Repayment is free of fee at every carrier that states one [S11] [S13], so a real book repays; the model does not |
| 부활 rate | **0**; **20%** of the prior year's lapses on `point_id = 10`, one year later | **[std]** |
| 감액 | **Off**; 50% of `SA` at duration 15 on `point_id = 10` | **[std]** |
| 자동대출납입 (APL), 감액완납, 연장정기보험 | **Not modelled, because none was found in any retrieved Korean document** | [unverified] [S5] — see below |
| 청약철회, 품질보증해지, 위법계약해지권; 우량체 / 건강등급 discounts, 선납, 중도인출, 추가납입 | Out of scope; the projection starts from cover in force, and each is named in `product-spec.md` | **[std]** [REG-R25] [REG-R51] |

**The single sharpest Korea/Japan difference, and it is a negative finding.** `jplib`'s
whole life chassis turns on the 自動振替貸付, which advances the premium against the
surrender value at the end of grace, so lapse there is a **funded** event. **No 자동대출납입
provision was found in any Korean document retrieved for this library.** The 생명보험
표준약관 is understood to contain such an article, but the retrieved 별표 15 extract does not
carry it [REG-R25], and the one full Korean 약관 in the set handles non-payment through a
월대체보험료 deduction from the account — a 유니버셜 mechanic, not an APL [S5 제24조].
`WholeLife_KR_A` therefore models lapse as a **behavioural decrement at the end of a 14-day
납입최고기간**, and the absence is tagged **[unverified]**: the highest-value single item for
the next research pass, because a 표준약관 article found later would change this chassis
**in kind**. The consumer consequence runs the opposite way to Japan's — in Korea there is
no buffer at all, and a 무해지 policyholder who misses fourteen days receives **nothing**,
which is the finding behind the FSS's 2019 소비자경보 [R4] [REG-R28].

---

## Cash flow components and recursions

### Notation

Defined once, used throughout, and identical to `product-spec.md`'s. The
`Projection` docstring carries the same table mapping every symbol to its cells name.

| Symbol | Meaning | Cells |
|---|---|---|
| `t` | policy year, `t = 1 … T`; attained 보험나이 in year `t` is `x + t − 1` | `age(t)` |
| `x`, `T`, `ω` | 가입나이 (보험나이); projection length `T = ω − x + 1`; table terminal age | `age_at_entry()`, `proj_len()`, `omega_age()` |
| `m` | 납입기간 in years; `m = T` on a 전기납 contract | `prem_period()`, `prem_end()` |
| `n_sc` | 해약공제기간 `= min(m, 7)` | `surr_chg_period()` |
| `SA`, `SA(t)` | 보험가입금액 at issue, and in year `t` after any 감액 | `sum_assured()`, `sum_assured_at(t)` |
| `G` | annual 영업보험료, level for `t ≤ m`, zero thereafter | `premium_pp()`, `premium_at_pp(t)` |
| `P`, `P₂₀` | 연납순보험료 over `m`; the same on the 별표 14 **20년납** footing | `prem_net_level_pp()`, `prem_net_20yr_pp()` |
| `i`, `i_acc`, `i_L` | 예정이율; the account accrual rate; 보험계약대출이율 `= i_acc + 1.5%` | `prem_int_rate`, `acc_int_rate()`, `loan_int_rate()` |
| `q(t)`, `w(t)`, `u(t)` | 적용위험률; 해지율; 납입면제 incidence, in year `t` | `mort_rate(t)`, `lapse_rate(t)`, `waiver_rate(t)` |
| `A(y)`, `ä(y, n)` | whole-life EPV of 1 at 보험나이 `y`; `n`-year annuity-due, both on `i` and the table | `epv_death(y)`, `annuity_due(y, n)` |
| `l(t)`, `lp(t)`, `lw(t)` | in force at the start of year `t`; of those, paying; of those, waived | `pols_if(t)`, `pols_if_pay(t)`, `pols_waived(t)` |
| `D(t)`, `S(t)`, `Sp(t)`, `R(t)` | deaths; 해지; 해지 **paid** a value; 부활 | `pols_death(t)`, `pols_lapse(t)`, `pols_surr(t)`, `pols_reinstate(t)` |
| `V(t)` | 계약자적립액 at anniversary `t` | `pol_val_pp(t)` |
| `SC(t)`, `SC*` | 해약공제액 at `t`; the **표준해약공제액** cap | `surr_chg_pp(t)`, `surr_chg_cap_pp()` |
| `W(t)` | 표준형 twin's 해약환급금, `max(0, V(t) − SC(t))` | `cv_std_pp(t)` |
| `k`, `κ(t)` | suppression factor; the multiplier actually applied in year `t` | `cv_floor_ratio()`, `cv_mult(t)` |
| `CV(t)` | 해약환급금 payable at `t` | `cv_pp(t)` |
| `B(t)` | 유지보너스 credited at 납입완료 | `bonus_pp(t)` |
| `cumprem(t)`, `ρ(t)` | premiums paid to `t`; **환급률** `CV(t) / cumprem(t)` | `cum_prem_pp(t)`, `refund_ratio(t)` |
| `L(t)`, `Δ(t)` | 보험계약대출 balance at the start of year `t`; the draw in year `t` | `loan_pp(t)`, `loan_draw(t)` |
| `AC`, `c₀`, `c_r`, `e`, `ec`, `π` | 계약체결비용; first-year commission share; renewal rate; per-policy 계약관리비용; claim expense; expense inflation | `acq_cost_pp()`, `comm_init_share`, `comm_renewal_rate`, `expense_maint_pp`, `expense_claim_pp`, `inflation_rate` |
| `CF(t)` | net cash flow of year `t`, **income-positive** | `net_cf(t)` |

**Dimensional check.** `q`, `w`, `u`, `k`, `κ`, `ρ`, `c₀`, `c_r`, `l`, `lp`, `lw` and the
`sa_factor` are dimensionless; `i`, `i_acc`, `i_L`, `π` are per annum; `A` and `ä` are pure
numbers (`ä` in years of premium, so `SA × A / ä` is ₩ per year); `SA`, `G`, `P`, `V`, `SC`,
`W`, `CV`, `B`, `L`, `AC`, `e`, `ec` are ₩; every term of `CF(t)` is ₩ per policy issued per
year. No term mixes a per-annum rate with a stock without an explicit year count.

### The net premium, and the two annuities that are not the same

The 표준형 twin's net level premium is fixed at issue by equivalence over the 납입기간, on
the 예정이율 and the 적용위험률:

    P × ä(x, m) = SA × A(x)          =>      P = SA * A(x) / ä(x, m)

with `A` and `ä` evaluated end-year and premium-in-advance respectively:

    A(y)      = v * ( q(y) + (1 - q(y)) * A(y + 1) ),     A(y) = 0 for y > omega
    ä(y, n)   = 1 + v * (1 - q(y)) * ä(y + 1, n - 1),     ä(y, 0) = 0
    v         = 1 / (1 + i)

**A second annuity is required and it is not the same object.** 별표 14 note 3 says the
연납순보험료 entering the 표준해약공제액 is recomputed on a **20년납** footing where the
보험기간 is 20 years or more — which for a 종신 contract it always is [REG-R20]. So

    P     = SA * A(x) / ä(x, m)             the pricing net premium, over m years
    P20   = SA * A(x) / ä(x, 20)            the 별표 14 net premium, over 20 years

and `P₂₀ = P` **only when `m = 20`**, which is the anchor's case and is exactly why the
anchor was chosen. On the 7년납 point they differ substantially, and a model that reuses `P`
in the cap formula overstates the statutory surrender charge on every short-pay design.
`prem_net_20yr_pp()` exists as a separate cells for that reason alone.

**The gross premium is an input, not an output.** `G` comes from the model point, sourced
[S4]; the model also carries its own loading rule, `prem_gross_calc_pp() = θ × P ×
prem_susp_ratio` with `θ = 1.4642` **[std]**, calibrated once against the 표준형 anchor and
reported in the worked example. **The projection uses the model-point value.** A loading
that reproduces a sourced premium to five significant figures is a documented fit, not a
pricing model, and is not allowed to drive cash flows.

### 계약자적립액 — the account recursion this chassis defines

The 표준형 twin's account is the classical net-level recursion on the annual grid, with the
death benefit falling at the **end** of the year:

    V(0)                  = 0
    V(t) * (1 - q(x+t-1)) = ( V(t-1) + P * 1{t <= m} ) * (1 + i_acc) - q(x+t-1) * SA
    V(T)                 := 0

solved forward. Rearranged as the model computes it,

    V(t) = ( ( V(t-1) + P * 1{t <= m} ) * (1 + i_acc) - q * SA ) / (1 - q)

Three properties are contractual rather than conventional and a model must not lose them.

**It is net level premium.** The acquisition cost is **not** Zillmerised into the account;
it is deducted **from** it, and the deduction is what 별표 14 caps [REG-R20]. The
consequence is visible in the worked example's first row: `V(1)` is ₩2,076,132.76 while
`SC(1)` is ₩2,662,886.18, so `W(1) = max(0, V − SC) = 0` and the first-year surrender value
is nil — which is what every published Korean grid shows at duration 1 [S1] [S4] [S6] [S8].

**It runs on the 표준형 net premium**, not on the sold form's lower one. `CV(t)` is
therefore **independent of the sold form's own premium**, and that single fact is the whole
of the 환급률 arithmetic that sells the product: the suppressed form's post-완납 surrender
value is identical to the 표준형's while its premiums are lower, so its refund ratio is
mechanically higher. Nothing is credited that the 표준형 does not get; the **denominator is
smaller**.

**It is bounded below by nothing.** The account may be smaller than the surrender charge, in
which case the 해약환급금 is zero and never negative [REG-R19 제7-66조제1항제1호].

Two identities are asserted rather than assumed. `check_pol_val_roll_fwd()` re-derives the
recursion residual at every `t`. `check_pol_val_prosp()` compares the forward account
against its **prospective** form,

    prosp_val_pp(t) = SA * A_acc(x + t) - P * ä_acc(x + t, max(m - t, 0))

on the accrual rate, and asserts equality to `val_tol × SA`. **It is defined as zero on a
금리연동형 point**, and that is not a dodge: once the crediting rate can differ from the
pricing rate the account is genuinely path-dependent and the retrospective and prospective
forms are different numbers. On `point_id = 9` — 여 45세, 금리연동형 at 2.75% against a
2.50% pricing rate — the forward account at `t = 20` runs **9.38% above** its prospective
form (₩53,524,380.95 against ₩48,934,924.41). A model that asserts the identity
unconditionally will fail there and, worse, may be "fixed" by discounting the account on the
wrong rate.

**The 금리연동형 variant, and why the crediting rate is a slow scalar.** 공시이율 =
공시기준이율 ± 조정률, the 공시기준이율 being
`외부지표금리 × α + 운용자산이익률 × (1 − α)` on a three-month weighted moving average with
**α capped at 60%**, uniform across a product class of which 보장성보험(종신보험) is one, and
floored by a mandatory 최저보증이율 [REG-R18] [REG-R24 별표 27] [REG-R23] [REG-R16]. The α
cap is the modelling point: a Korean declared rate is majority-weighted to the insurer's
**own realised** 운용자산이익률, not to market yields, which is why `decl_rate` is a
slow-moving [std] scalar and not a function of a yield curve.

### 해약공제 and the 표준해약공제액 cap

별표 14 states the cap in one line [REG-R20]:

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보장성보험의 보험가입금액 × 10/1000

For a 보장성보험 the 해약공제계수 is the **보험기간 capped at 20 years** [REG-R20 주2], and
a 종신 contract's 보험기간 always exceeds 20, so the coefficient is 20 and 5% × 20 = 1.0.
For this product the formula therefore collapses to **one year's net premium plus one per
cent of the sum assured**:

    SC*  =  0.05 * 20 * P20  +  0.01 * SA  =  P20 + 0.01 * SA

with `SA` taken as the 일반사망보험금 **before any 체증 or 체감** [REG-R21 별표 15 제3호,
제8호]. The *level* of the charge is set at the cap **[std]**, and only its *shape between
the ends* is standardized — a straight line to `n_sc`:

    SC(t) = SC* * max(0, 1 - t / n_sc) * sa_factor(t),      n_sc = min(m, 7)

**The duration is fixed by regulation and it is short.** 제7-66조제1항제2호: 「해약공제기간은
보험료 납입기간 또는 신계약비 부가기간으로 하되 … **7년 이상일 때에는 7년으로** 한다」
[REG-R19]. On the anchor's 20년납 contract the charge is fully amortised by duration 7 —
**thirteen years before the cliff.** That separation is the single most important structural
fact in this section, because it means the step at 납입완료 has nothing whatever to do with
the surrender charge running off: by then it has been gone for over a decade.
`check_surr_chg_cap()` asserts both limbs — never above `SC*`, and exactly zero from `n_sc`.

That is the honest position on the three components: the **cap is sourced and exact**, the
**level is set at the cap** and defended by the four public bounds in class (b), and only
the **shape between the ends** is [std].

### 해약환급금 and the 무해지 / 저해지 cliff

    W(t)  = max( 0, V(t) - SC(t) )                          the 표준형 twin's value
    kappa(t) = k    for t <  m      (and for all t on a 전기납 contract)
    kappa(t) = 1    for t >= m
    CV(t) = kappa(t) * W(t) + B(t)                          the payable value
    CVs(t) = k * W(t)                                       the suppressed value at every t

and the transition at `t = m` is a **step, not a ramp**. `CV(m) / (k W(m))` is exactly
`1 / k` and **anything between is an interpolation the contract does not have.** Both
quantities exist at `t = m` and the model publishes both, `cv_pp` and `cv_susp_pp`, side by
side in `result_val()` so the step can be read off one row rather than inferred.

**[std] ordering rule.** A surrender occurring in policy year `m` is paid at the end of year
`m` on `CV(m)` — the **full** value. The suppressed value applies to years 1 … m − 1. This
is a convention on an annual grid and it is stated because it is worth real money: on the
anchor the difference between the two readings of year 20 is a factor of two on
₩51,428,412.54.

`check_cv_cliff()` asserts three things: that `CV(t) − B(t) = κ(t) W(t)` at every `t`, that
the payable value net of any bonus **never exceeds the 표준형 twin's**, and that at `t = m`
they are **equal**. It deliberately does **not** assert the FSC press-release framing 「전(全)
보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로」 [REG-R28], because the
denominators differ and the two statements can disagree: on `point_id = 3` the 무해지 form's
post-완납 환급률 is **1.068759** against the 표준형's 0.833632, which satisfies
제7-66조제4항제2호 나목 as recorded in the 고시 [REG-R19] and contradicts the press-release
reading. `product-spec.md` records both statements as they stand and so does this document;
neither resolves them, because the operative article text and the press-release sentence
were retrieved from different documents and no third document reconciles them.

**Everything derived from the surrender value is suppressed with it.** The 보험계약대출
limit and the 감액 proceeds are computed off `CV(t)`, so during 납입기간 both are `k` times
their 표준형 size — and on a **무해지** contract the policy loan **does not exist at all**,
which the FSS said in terms in its 2019 alert and the 표준약관 repeats as 「순수보장성보험 등
보험상품의 종류에 따라 보험계약대출이 제한될 수 있습니다」 [R4] [REG-R28] [REG-R25 제33조].
`point_id = 3` is that case and draws **exactly nothing**.

### 유지보너스, and the lapse spike that is not optional

On a 단기납 design the insurer credits a persistency bonus to the 계약자적립액 at 납입완료:
**10.8% (5년납) / 13.8% (7년납) / 15.0% (10·15년납)** of total 주보험 premiums, with a
second 18.5% credit at duration 10 on the 5·7년납 forms [S7]. The model carries the first
credit only, and **as an addition to the payable surrender value from `t ≥ m`** rather than
as a credit inside the account recursion **[std]**, no crediting formula being published:

    B(t) = bonus_rate * cumprem(m)     for t >= m on a term-pay contract,  else 0

**The supervisor requires an additional lapse of at least 30% at any such bonus date**, or a
rate backed out of the 표준형 product's cumulative persistency, calibrated against the
29.4%–30.2% eleventh-year lapse observed on single-premium bancassurance savings [REG-R27]
[R3]. `lapse_spike()` therefore turns on **with** the bonus and cannot be switched on
separately: on `point_id = 8` the year-7 lapse rate is **0.301** against a base of 0.001.
Turning the bonus on without the spike would misstate the liability in the insurer's favour,
which is exactly what the guidance exists to prevent.

### 보험계약대출 as a modelled state

    L(1)   = 0
    L(t+1) = ( L(t) + Delta(t) ) * (1 + i_L)
    Delta(t) = util * max( 0, 0.80 * CV(t - 1) - L(t) )     at t = loan_year, else 0

and every payment is made **net of the balance and floored at zero**:

    death benefit    = max(0, SA(t) - L(t))
    surrender payout = max(0, CV(t) - L(t))
    감액 proceeds     = reduce_frac * max(0, CV(t) - L(t))

Four features of the Korean loan matter and none is optional. **The rate is a vintage
rate** — 「예정이율 + 1.5%」 on a 금리확정형 contract, 「공시이율 + 1.5%」 on a 금리연동형
one, at three carriers independently [S9] [S11] [S13] — so one carrier's live range spans
**연 3.5% ~ 10.5%** across its in-force book [S11]. **The limit is a fraction of the
*payable* value**, so on a suppressed form it is suppressed too. **There is no
early-repayment fee** [S11] [S13]. And **the loan is settled first on every exit**, 즉시 on
해지 [S5 제34조] [REG-R25 제26조]: Korea has **no equivalent of the Japanese
loan-excess-lapse notice**, so the balance never terminates the contract — it absorbs the
payout instead.

**No repayment is modelled [std]** and the draw is a single event, so the balance compounds
untouched: on `point_id = 6` a draw of ₩8,167,325.83 at `t = 10` grows to
**₩108,712,698.33 by `t = 76`**, above the ₩100,000,000 sum assured, so every later payment
floors at zero. A real book repays; this one does not, and the floor is where it shows.

`check_loan_roll_fwd()` asserts the recursion at every `t`.

### 보험료 납입면제 as a state transition

Within policy year `t`, **before** the premium is taken:

    waiver(t)   = lp(t) * u(t)                      moves out of the paying cohort
    lp_exp(t)   = lp(t) - waiver(t)                 pays the premium this year
    lw_exp(t)   = lw(t) + waiver(t)                 accrues value, pays nothing

Both cohorts then carry the **same** mortality and the **same** lapse rate **[std]** — no
Korean source distinguishes the persistency of a waived contract — and both roll forward
together:

    lp(t+1) = lp_exp(t) * (1 - q(t)) * (1 - w(t)) + R(t+1)
    lw(t+1) = lw_exp(t) * (1 - q(t)) * (1 - w(t))
    l(t)    = lp(t) + lw(t)

The premium is weighted by `lp_exp(t)`, everything else by `l(t)`. **That is the whole
content of the waiver in cash-flow terms**: a waived policy contributes to the in-force
count, to maintenance expense and to every benefit, and to neither premium nor commission.
The two weights coincide in the base run, where `u ≡ 0`, which is exactly why the
distinction has to be written down rather than discovered when the module is switched on.
`point_id = 7` runs it at 0.4% p.a. and reaches `pols_waived(20) = 0.042858`.

### 감액 as a partial surrender

감액 is universal and the 약관 treats the reduced portion as terminated: 「그 감액된 부분은
해지된 것으로 보며, 이로써 회사가 지급하여야 할 해지환급금이 있을 때에는 … 지급합니다」
[S5 제20조]. On a suppressed contract the accompanying warning is the main event rather than
a caveat: a reduction made during 납입기간 pays at `k W(t)`, and on a 무해지 contract it
pays **nothing at all**.

    claims(t, "REDUCTION") = reduce_frac * max(0, CV(t) - L(t)) * l_after_decrements(t)
    sa_factor(t) = 1 - reduce_frac     for t > reduce_year

The restatement is exact here because **every** quantity carrying the 가입금액 is
proportional to it: `SA(t)`, `G(t)`, `V(t)`, `SC(t)` and therefore `W(t)` all step down by
the same factor from `t + 1`. The 약관's pro-rata restatements of 이미 납입한 보험료,
중도인출 누적액 and 초과납입액 [S5 제20조] matter only on designs whose death benefit is a
function of premiums paid, which the 평준형 composite is not. `point_id = 10` reduces 50%
of a ₩1,000,000,000 cover at duration 15.

### 부활 as a one-year re-entry

    R(t) = reinstate_rate * S(t - 1)        into the paying cohort at the start of year t
    Sp(t) = S(t) - R(t + 1)                 the lapses actually paid a surrender value

The substantive effect is not the count but the **payment**: a reinstated policyholder is
not paid a surrender value, because 부활 requires that the 해약환급금 has not been drawn and
the 약관 expressly includes the case where there was none to draw [S5 제26조] [REG-R25
제27조]. A one-year lag is a **[std]** simplification of a three-year window, and no arrears
cash flow is modelled: on an annual grid with premiums in advance there is no premium
instalment falling inside a one-year gap. `point_id = 10` runs it at 20%.

### Processing order (policy year `t = 1 … T`)

The order is explicit because two steps in it are worth money and one is a convention.

1. **Start of year — the in-force split.** `l(t) = lp(t) + lw(t)`. This is the
   `result_cf()` row's `pols_if` and the weight on every non-premium cash flow in it.
2. **Start of year — 납입면제 transition.** `waiver(t) = lp(t) × u(t)` moves out of the
   paying cohort **before** the premium is taken.
3. **Start of year — premium.** `premiums(t) = G(t) × lp_exp(t)` for `t ≤ m`, in advance, on
   the paying cohort only. **Zero from `m + 1` onwards, for ever.**
4. **Start of year — expenses and commission.** Acquisition expense and initial commission
   at `t = 1` only, on `l(1)`. Maintenance expense `e × (1 + π)^(t−1) × l(t)` at the start of
   **every** year, for life. The premium-related expense and renewal commission on the
   premium **actually collected**, years 2 … m.
5. **Start of year — 보험계약대출 draw**, where one is elected, off `CV(t − 1)`.
6. **Cash values.** `V(t)`, `SC(t)`, `W(t)`, `CV(t)` at the year-end anniversary.
7. **End of year — deaths.** `D(t) = l(t) × q(t)`, paid `max(0, SA(t) − L(t))` each, plus
   `ec × D(t)` of claim expense.
8. **End of year — 해지**, on the survivors of mortality — **death before lapse [std
   order]**: `S(t) = l(t) × (1 − q(t)) × w(t)`, of which `Sp(t) = S(t) − R(t + 1)` is paid
   `max(0, CV(t) − L(t))`.
9. **End of year — 감액**, at the same anniversary, on those continuing after both
   decrements.
10. **End of year — loan roll-up.** `L(t + 1) = (L(t) + Δ(t)) × (1 + i_L)`.
11. **Start of year `t + 1` — 부활.** `R(t + 1)` of year `t`'s lapses returns to the paying
    cohort, and is **not** paid a surrender value.
12. **Update in force**, per the two-cohort recursion above.
13. **At `t = T`** the table's terminal rate is 1, so `l(T + 1) = 0` and the projection ends.
    `V(T) := 0` by definition. No maturity payment, no tail states.

**Death before lapse is a [std] ordering** and it is not neutral: reversing it applies the
lapse rate to the full in-force count instead of to survivors, moving both the surrender
outgo and the roll-forward. Asserted by `check_pols_roll_fwd()`.

**The account recursion runs on its own clock.** `V(t)` is a function of `t`, `P`, `i_acc`
and `q` alone — **not of `l(t)`, `w(t)` or `u(t)`** — because it is a per-policy contractual
quantity. That is why the 표준형 twin can be priced 「해지율을 적용하지 않고」 [S1] and still
be the same object the sold form's value is a fraction of.

### Net cash flow

Income-positive, per policy issued:

    CF(t) =   G(t) * lp_exp(t) * 1{t <= m}                       (premiums)
            - max(0, SA(t) - L(t)) * D(t)                        (claims_death)
            - max(0, CV(t) - L(t)) * Sp(t)                       (claims_lapse)
            - reduce_frac * max(0, CV(t) - L(t)) * l_aft(t)      (claims_reduction)
            - ec * D(t)                                          (claim_expenses)
            - ( AC - c0*AC ) * 1{t = 1} * l(1)                   (expenses: acquisition)
            - e * (1 + pi)^(t-1) * l(t)                          (expenses: maintenance)
            - 0.02 * premiums(t)                                 (expenses: premium-related)
            - min(c0 * AC, G) * 1{t = 1} * l(1)                  (commissions: initial)
            - c_r * premiums(t) * 1{2 <= t <= m}                 (commissions: renewal)

`result_cf()` publishes these as `pols_if`, `premiums`, `claims_death`, `claims_lapse`,
`claims_reduction`, `claim_expenses`, `expenses`, `commissions`, `net_cf` — `pols_if` first,
`net_cf` last, **no `claims` subtotal column**, so the columns sum exactly to `net_cf`.
`expenses` is acquisition plus maintenance plus the premium-related component; the claim
handling expense stands beside it, the settled vocabulary across the six libraries.
`claims_reduction` is zero on the anchor and published rather than dropped, 감액 being
universal on this chassis. `check_net_cf()` asserts the ledger at every `t`.

**Two roll-forward identities close the projection.**

    l(t) - l(t+1) - D(t) - S(t) + R(t+1) = 0                    check_pols_roll_fwd()
    l(1) + sum R - sum (D + S) - l(t+1)  = 0                    check_decrement_sum()

Because the table terminates, every policy leaves by one of the two decrements, so
`Σ D(t) + Σ S(t) = 1` in the base run and `l(T + 1) = 0`. Each `check_*()` takes **no
argument and returns a bool** over all `t`, with the per-`t` signed residual at
`check_*_resid(t)`. Nine of them ship and all nine are `True` on all ten model points.

### Optional modules (all off in the base run)

| Module | Switch | Base | Exercised on |
|---|---|---|---|
| 보험계약대출 | `loan_util`, `loan_year` | 0 | `point_id = 6` (저해지) and `3` (무해지, draws zero) |
| 보험료 납입면제 | `waiver_rate` | 0 | `point_id = 7`, 0.4% p.a. |
| 유지보너스 + the mandatory ≥ 30% lapse spike | `bonus_rate` | 0 | `point_id = 8`, 13.8% on a 7년납 design |
| 금리연동형 crediting | `int_basis`, `decl_rate` | `fixed` | `point_id = 9`, 공시이율 2.75% |
| 감액 | `reduce_year`, `reduce_frac` | 0 | `point_id = 10`, 50% at duration 15 |
| 부활 | `reinstate_rate` | 0 | `point_id = 10`, 20% |
| `flat` lapse basis | `lapse_basis` | `loglinear` | `point_id = 10`, and re-run on the anchor below |
| Best-estimate mortality lever | `mort_be_factor` | 1.00 | `point_id = 10`, 0.90 |

Each module is implemented and switched off so the base run reproduces the worked example
while the machinery stays visible and testable. **Nothing here is a placeholder**: every one
produces a signature number asserted in `tests/test_whole_life_kr.py`.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions. There is no public calibration
evidence for any of them on this product, and the one place where a supervisor has
substituted its own judgement — the lapse vector — is precisely the place where that
absence became a systemic problem.

- **Base surrender.** The `loglinear` vector of class (c): 10% in year 1 decaying
  log-linearly to 0.1% at 납입완료, then 0.8% for life. It is the FSS 원칙모형 [REG-R27]
  [R3] with its start pinned to the top of a disclosed 적용해지율 envelope [S2]. The
  disclosed *pricing* envelopes are much higher — 1%–10% [S2], 0%–13.4% [S8] — and the two
  bases serve different purposes and cannot be reconciled from public data. **This is the
  single largest assumption gap for this product.**
- **The 표준형 twin carries no lapse assumption at all** [S1] — which is what makes it a
  pure account run-off, and why the `flat` basis here is level rather than shaped.
- **The shape between the ends is [std] and it does the work.** The endpoints are
  regulatory; the log-linear interpolation is this library's. Alternatives — 선형-로그,
  로그-로그 — are permitted to a Korean insurer only against audited disclosure of the
  difference in **CSM, BEL, K-ICS ratio and net income**, external validation, quarterly FSS
  reporting and an on-site inspection [REG-R27] [R3]. The shipped `flat` basis runs that
  comparison in one line; it is exercised below.
- **No dynamic lapse function is implemented [std].** The natural driver here is the 환급률
  crossing 1, which on the anchor happens at `t = 24`, four years after the cliff; a form
  keyed on `refund_ratio(t)` would generate a spike there endogenously. It is deliberately
  **not** shipped: the November 2024 decision fixes the base vector, and an overlay on a
  supervised assumption is a departure requiring the disclosure regime above [REG-R27]. The
  hook is `lapse_rate(t)`; adding one changes no other formula.
- **The spike at a 유지보너스 date is a mechanic, not a behaviour, in one direction only.**
  The bonus credit is contractual [S7]; the ≥ 30% additional lapse is a supervisory
  requirement on the assumption [REG-R27]. Modelling the first without the second is not a
  simplification, it is an error, and `lapse_spike()` is wired to `bonus_rate()` so it cannot
  be done by accident.
- **Lapse is behavioural and terminal only by choice.** With no APL in evidence [S5]
  [REG-R25], a Korean policyholder who misses the 14-day 납입최고기간 loses the contract
  whatever its cash value. But 부활 within three years is available **even where the
  해약환급금 was nil** [S5 제26조] [REG-R25 제27조], so the exit is not terminal in the
  contract. `reinstate_rate` is zero in the base run, which **understates** later-duration
  in force and therefore both premium income and claims. The bias is stated rather than
  corrected because no retrieved source gives a Korean reinstatement rate.
- **보험계약대출 take-up is static, and the loan does not terminate the contract.** Korea
  has no loan-excess-lapse notice [S5] [REG-R25], so unlike `jplib`'s APL the loan cannot end
  the policy — it only absorbs the payout, which on `point_id = 6` it eventually does in
  full.
- **The premium waiver is an option with value, not a protection feature.** Because waived
  premiums count as paid [S2] [S3] [S6] [S8], the waiver is the only route to the cliff the
  policyholder does not have to fund. On a 무해지 contract that asymmetry is extreme: the
  waiver converts a contract worth nothing on surrender into one that steps to the full
  표준형 value at 납입완료 without another won being paid. No incidence rate for the 50%
  장해지급률 trigger was retrieved, so the 0.4% p.a. on `point_id = 7` is **[std]** and its
  purpose is to exercise the state, not to size the option.
- **The disease riders that extend the waiver trigger are not modelled.** 3대질병, 6대질병
  and their 90-day 면책기간 belong to the incidence machinery of [cancer
  (암보험)](../cancer/technical-notes.md) and [CI (CI보험)](../ci_insurance/technical-notes.md)
  [S1] [S2] [S3] [S5] [S6].
- **면책 incidence is zero in the base run [std], and refusal is not forfeiture.** On an
  면책사유 the insurer must still pay 「보험수익자를 위하여 적립한 금액」, in practice the
  계약자적립액 [REG-R50 제736조] [REG-R25 제22조]. The composite carries no exclusion
  incidence, so nothing is deducted; **treating an exclusion as a zero-payment event
  overstates the insurer's position** by the account, not by the claim.

---

## Worked example

### The anchor cell

**`point_id = 1`** — 남자, 보험나이 **40세**, 보험가입금액 **₩100,000,000 (1억원)**,
보험기간 **종신**, 납입기간 **20년**, 월납 annualized, **저해지환급형 `k = 0.50`**, annual
premium **₩2,776,140**. `T = 115 − 40 + 1 = 76` policy years, attained 보험나이 40 to 115.
Every optional module is off: `waiver_rate = loan_util = bonus_rate = reduce_frac =
reinstate_rate = 0`, `int_basis = fixed`, `lapse_basis = loglinear`, `mort_be_factor = 1.00`.

The premium is **0.900 × ₩3,084,600 [std]** [S1], and ₩3,084,600 is 12 × the published
₩257,050 monthly rate for exactly this cell [S4], which is `point_id = 2` — **the 표준형
comparison twin, same cell, `k = 1.00`.** The two run side by side throughout.

**Assumption values used, in full.** `i = i_acc = 2.50%` **[std]** on the disclosed
2.25%–2.75% band [S1] [S2] [S5] [S6] [S7] [S8]; `q` from `mort_table.csv` 남 at attained
보험나이 with `mort_be_factor = 1.00`, **[std]** construction anchored on [S2] [S8] and
calibrated to [REG-R38] and [REG-R33]; `w` the `loglinear` vector, endpoints [REG-R27] [R3]
and [S2], interpolation **[std]**; `SC* ` from 별표 14 [REG-R20] with the 7-year 해약공제기간
of [REG-R19]; `AC = SC*` and `c₀ = 0.65` **[std]** inside [REG-R22]; `c_r = 3.0%`,
`e = ₩60,000` p.a. inflating at 2.0%, 2.0% of premium, `ec = ₩300,000` per claim, all
**[std]**; `i_L = 4.00%` [S9] [S11] [S13], unused here because `loan_pp ≡ 0`.

**Derived scalars, at full precision.**

| Quantity | Cells | Value |
|---|---|---|
| Terminal age ω | `omega_age()` | 115 |
| Projection length `T` | `proj_len()` | **76** |
| 납입기간 `m` | `prem_period()`, `prem_end()` | 20 |
| 해약공제기간 `n_sc` | `surr_chg_period()` | **7** |
| `A(40)` | `epv_death(40)` | 0.332153184440 |
| `ä(40, 20)` | `annuity_due(40, 20)` | 15.766511588794 |
| 연납순보험료 `P` | `prem_net_level_pp()` | **₩2,106,700.5378440050** |
| 연납순보험료, 20년납 footing `P₂₀` | `prem_net_20yr_pp()` | ₩2,106,700.5378440050 |
| 영업보험료 `G` | `premium_pp()` | **₩2,776,140.0000000000** |
| Loaded premium on the model's own rule | `prem_gross_calc_pp()` | ₩2,776,167.8347600726 |
| **표준해약공제액** `SC*` | `surr_chg_cap_pp()` | **₩3,106,700.5378440050** |
| 계약체결비용 `AC` | `acq_cost_pp()` | ₩3,106,700.5378440050 |
| First-year commission | `comm_init_pp()` | ₩2,019,355.3495986033 |
| Acquisition **expense** at `t = 1` | `acq_cost_pp() − comm_init_pp()` | ₩1,087,345.1882454017 |
| Accrual rate `i_acc` | `acc_int_rate()` | 0.025 |
| Loan rate `i_L` | `loan_int_rate()` | 0.04 |

`P₂₀ = P` here because `m = 20` exactly — the one configuration in which the two annuities
coincide, and part of why the anchor is the regulator's own reference cell [REG-R9]
[REG-R20]. **`prem_gross_calc_pp()` misses the sourced premium by 0.0010%**
(₩2,776,167.83 against ₩2,776,140.00, a fit of 1.0000100), and the projection uses the
sourced number. On the 표준형 twin the same rule gives ₩3,084,630.93 against ₩3,084,600 —
the identical relative error, because `θ` was calibrated on that cell once and applied
unchanged.

**Two cross-checks on the statutory cap, neither used to fit it.** The FSC states the same
cap as 「보장성보험 월 보험료의 13배 수준」 [REG-R29], and 13 × ₩257,050 = ₩3,341,650; the
model's ₩3,106,700.54 is **7.0% below** that rule of thumb. And the net-premium ratio the
model computes is `P / G_표준형` = **0.682974**, not the 80% `product-spec.md` uses to
*illustrate* the cap — so the specification's ₩3,470,000 illustration and the model's
₩3,106,700.54 differ by 10.5%, entirely because the model derives `P` from equivalence
rather than assuming a loading ratio. The model's is what is projected.

**The anchor's mortality and lapse rates, `t = 1 … 25`.**

| t | attained age | `mort_rate(t)` | `lapse_rate(t)` |
|---|---|---|---|
| 1 | 40 | 0.00085000 | 0.1000000000 |
| 2 | 41 | 0.00092944 | 0.0784759970 |
| 3 | 42 | 0.00101630 | 0.0615848211 |
| 4 | 43 | 0.00111127 | 0.0483293024 |
| 5 | 44 | 0.00121513 | 0.0379269019 |
| 6 | 45 | 0.00132869 | 0.0297635144 |
| 7 | 46 | 0.00145286 | 0.0233572147 |
| 8 | 47 | 0.00158864 | 0.0183298071 |
| 9 | 48 | 0.00173710 | 0.0143844989 |
| 10 | 49 | 0.00189944 | 0.0112883789 |
| 11 | 50 | 0.00207696 | 0.0088586679 |
| 12 | 51 | 0.00227106 | 0.0069519280 |
| 13 | 52 | 0.00248330 | 0.0054555948 |
| 14 | 53 | 0.00271538 | 0.0042813324 |
| 15 | 54 | 0.00296914 | 0.0033598183 |
| 16 | 55 | 0.00324662 | 0.0026366509 |
| 17 | 56 | 0.00355003 | 0.0020691381 |
| 18 | 57 | 0.00388180 | 0.0016237767 |
| 19 | 58 | 0.00424458 | 0.0012742750 |
| **20** | 59 | 0.00464125 | **0.0010000000** |
| 21 | 60 | 0.00507500 | 0.0080000000 |
| 22 | 61 | 0.00551816 | 0.0080000000 |
| 23 | 62 | 0.00600277 | 0.0080000000 |
| 24 | 63 | 0.00653292 | 0.0080000000 |
| 25 | 64 | 0.00711315 | 0.0080000000 |

`q(40) = 0.00085` and `q(60) = 0.005075` are **ANCHOR** rows — the mean of 하나생명's
0.000780 [S2] and KDB생명's 0.00092 [S8] at 40, and of 0.004550 and 0.00560 at 60; the rates
are sourced, the mean is **[std]**. Everything between is log-linear in `ln q`. `w(1) = 0.10`
and `w(20) = 0.001` are exact by construction, and `w(21) = 0.008` is the FSS ultimate rate
[REG-R27].

### First periods of the base run

Per policy issued, income-positive, to two decimal places — the precision the tests assert.

| t | age | `pols_if(t)` | premiums | claims_death | claims_lapse | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 1.000000 | 2,776,140.00 | 85,000.00 | 0.00 | 255.00 | 1,202,867.99 | 2,019,355.35 | -531,338.34 |
| 2 | 41 | 0.899235 | 2,496,402.25 | 83,578.50 | 69,772.73 | 250.74 | 104,961.23 | 74,892.07 | 2,162,946.99 |
| 3 | 42 | 0.827896 | 2,298,356.43 | 84,139.12 | 116,951.51 | 252.42 | 97,647.74 | 68,950.69 | 1,930,414.96 |
| 4 | 43 | 0.776121 | 2,154,620.59 | 86,248.00 | 135,877.69 | 258.74 | 92,509.96 | 64,638.62 | 1,775,087.58 |
| 5 | 44 | 0.737791 | 2,048,210.63 | 89,651.18 | 139,216.88 | 268.95 | 88,880.72 | 61,446.32 | 1,668,746.57 |
| 6 | 45 | 0.708946 | 1,968,133.90 | 94,196.97 | 134,039.01 | 282.59 | 86,326.71 | 59,044.02 | 1,594,244.60 |
| 7 | 46 | 0.686932 | 1,907,018.11 | 99,801.53 | 124,416.36 | 299.40 | 84,556.15 | 57,210.54 | 1,540,734.11 |
| 8 | 47 | 0.669912 | 1,859,769.56 | 106,424.90 | 110,022.82 | 319.27 | 83,366.49 | 55,793.09 | 1,503,842.99 |
| 9 | 48 | 0.656588 | 1,822,780.00 | 114,055.89 | 96,254.81 | 342.17 | 82,613.44 | 54,683.40 | 1,474,830.28 |
| 10 | 49 | 0.646019 | 1,793,439.41 | 122,707.45 | 83,492.64 | 368.12 | 82,191.94 | 53,803.18 | 1,450,876.07 |
| 11 | 50 | 0.637513 | 1,769,826.31 | 132,408.97 | 71,912.65 | 397.23 | 82,024.04 | 53,094.79 | 1,429,988.63 |
| 12 | 51 | 0.630553 | 1,750,504.72 | 143,202.48 | 61,567.69 | 429.61 | 82,050.93 | 52,515.14 | 1,410,738.86 |
| 15 | 54 | 0.615467 | 1,708,623.01 | 182,740.82 | 37,529.80 | 548.22 | 82,898.21 | 51,258.69 | 1,353,647.28 |
| 19 | 58 | 0.601249 | 1,669,150.22 | 255,204.77 | 18,419.29 | 765.61 | 84,906.87 | 50,074.51 | 1,259,779.18 |
| **20** | 59 | 0.597934 | 1,659,947.45 | 277,515.94 | **30,608.06** | 832.55 | 85,463.53 | 49,798.42 | **1,215,728.95** |
| **21** | 60 | 0.594563 | **0.00** | 301,740.88 | **248,321.14** | 905.22 | 53,009.39 | **0.00** | **-603,976.63** |
| 24 | 63 | 0.570828 | 0.00 | 372,917.56 | 252,559.60 | 1,118.75 | 54,008.32 | 0.00 | -680,604.24 |
| 40 | 79 | 0.402873 | 0.00 | 1,084,850.32 | 230,239.97 | 3,254.55 | 52,327.09 | 0.00 | -1,370,671.93 |
| 60 | 99 | 0.067131 | 0.00 | 1,251,601.30 | 39,891.24 | 3,754.80 | 12,956.36 | 0.00 | -1,308,203.70 |
| 76 | 115 | 0.000001 | 0.00 | 50.84 | 0.00 | 0.15 | 0.13 | 0.00 | -51.13 |

The `claims_reduction` column is identically **0.00** on this cell and is omitted from the
display; it is published in `result_cf()` rather than dropped, because 감액 is universal on
this chassis and `point_id = 10` uses it.

**Four rows do something.** `t = 1` carries the whole acquisition cost and is the only
negative year before 완납. `t = 20` is the **cliff**: the payable surrender value doubles.
`t = 21` is the **first premium-free year**, and it is where the stream turns permanently
negative — premium and commission both go to zero in the same row while every outgo
continues. `t = 76` is the horizon: `q = 1`, everyone dies, and nothing is paid but the
death benefit.

### Surrender values at the same anniversaries

| t | `pol_val_pp(t)` | `surr_chg_pp(t)` | `cv_std_pp(t)` | `cv_pp(t)` | `cv_susp_pp(t)` | `cum_prem_pp(t)` | `refund_ratio(t)` |
|---|---|---|---|---|---|---|---|
| 1 | 2,076,132.76 | 2,662,886.18 | 0.00 | 0.00 | 0.00 | 2,776,140.00 | 0.000000 |
| 2 | 4,198,362.26 | 2,219,071.81 | 1,979,290.45 | 989,645.22 | 989,645.22 | 5,552,280.00 | 0.178241 |
| 3 | 6,367,530.69 | 1,775,257.45 | 4,592,273.24 | 2,296,136.62 | 2,296,136.62 | 8,328,420.00 | 0.275699 |
| 4 | 8,584,499.71 | 1,331,443.09 | 7,253,056.62 | 3,626,528.31 | 3,626,528.31 | 11,104,560.00 | 0.326580 |
| 5 | 10,850,151.59 | 887,628.73 | 9,962,522.87 | 4,981,261.43 | 4,981,261.43 | 13,880,700.00 | 0.358862 |
| 6 | 13,165,397.17 | 443,814.36 | 12,721,582.80 | 6,360,791.40 | 6,360,791.40 | 16,656,840.00 | 0.381873 |
| **7** | 15,531,178.78 | **0.00** | 15,531,178.78 | 7,765,589.39 | 7,765,589.39 | 19,432,980.00 | 0.399609 |
| 8 | 17,948,475.96 | 0.00 | 17,948,475.96 | 8,974,237.98 | 8,974,237.98 | 22,209,120.00 | 0.404079 |
| 9 | 20,418,314.57 | 0.00 | 20,418,314.57 | 10,209,157.28 | 10,209,157.28 | 24,985,260.00 | 0.408607 |
| 10 | 22,941,773.00 | 0.00 | 22,941,773.00 | 11,470,886.50 | 11,470,886.50 | 27,761,400.00 | 0.413196 |
| 11 | 25,519,993.39 | 0.00 | 25,519,993.39 | 12,759,996.69 | 12,759,996.69 | 30,537,540.00 | 0.417846 |
| 12 | 28,154,195.14 | 0.00 | 28,154,195.14 | 14,077,097.57 | 14,077,097.57 | 33,313,680.00 | 0.422562 |
| 15 | 36,406,331.66 | 0.00 | 36,406,331.66 | 18,203,165.83 | 18,203,165.83 | 41,642,100.00 | 0.437134 |
| 18 | 45,217,000.64 | 0.00 | 45,217,000.64 | 22,608,500.32 | 22,608,500.32 | 49,970,520.00 | 0.452437 |
| **19** | 48,287,294.99 | 0.00 | 48,287,294.99 | **24,143,647.50** | 24,143,647.50 | 52,746,660.00 | 0.457728 |
| **20** | 51,428,412.54 | 0.00 | 51,428,412.54 | **51,428,412.54** | 25,714,206.27 | 55,522,800.00 | 0.926258 |
| 21 | 52,472,922.93 | 0.00 | 52,472,922.93 | 52,472,922.93 | 26,236,461.47 | 55,522,800.00 | 0.945070 |
| 23 | 54,593,953.41 | 0.00 | 54,593,953.41 | 54,593,953.41 | 27,296,976.71 | 55,522,800.00 | 0.983271 |
| **24** | 55,669,192.63 | 0.00 | 55,669,192.63 | 55,669,192.63 | 27,834,596.32 | 55,522,800.00 | **1.002637** |
| 25 | 56,753,302.20 | 0.00 | 56,753,302.20 | 56,753,302.20 | 28,376,651.10 | 55,522,800.00 | 1.022162 |
| 30 | 62,277,600.33 | 0.00 | 62,277,600.33 | 62,277,600.33 | 31,138,800.17 | 55,522,800.00 | 1.121658 |
| 40 | 73,413,688.61 | 0.00 | 73,413,688.61 | 73,413,688.61 | 36,706,844.30 | 55,522,800.00 | 1.322226 |
| 60 | 91,301,421.85 | 0.00 | 91,301,421.85 | 91,301,421.85 | 45,650,710.92 | 55,522,800.00 | 1.644395 |
| 75 | 97,560,975.81 | 0.00 | 97,560,975.81 | 97,560,975.81 | 48,780,487.91 | 55,522,800.00 | 1.757134 |
| 76 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 55,522,800.00 | 0.000000 |

**Read the step off rows 19 and 20.** `cv_pp` goes from **₩24,143,647.50** to
**₩51,428,412.54** — exactly `1 / k = 2.0` — while `cv_std_pp` moves smoothly from
₩48,287,294.99 to ₩51,428,412.54, a 6.5% year. The whole of the step is the removal of `k`,
and **the surrender charge reached zero at `t = 7`, thirteen years earlier**, so nothing
about it is a surrender-charge effect. `cv_susp_pp` continues on the other side of the
boundary — ₩25,714,206.27 at `t = 20` — so both quantities are visible at the boundary
rather than inferred.

**Row 1 is nil in both columns**, the surrender charge biting exactly as the regulation
bounds it: `V(1)` = ₩2,076,132.76 against `SC(1)` = ₩2,662,886.18, so `max(0, V − SC)` is
zero and 「이를 영(零)으로 처리한다」 does the flooring [REG-R19]. Every published Korean
grid in the set shows nil at duration 1 [S1] [S4] [S6] [S8]. **Row 76 is zero throughout**:
at the terminal age everyone has died and `V(T)` is defined as zero, so `refund_ratio(76)`
is 0.000000 and not a crossing.

**The 환급률 crosses 100% at `t = 24`** (1.002637), from 0.983271 at `t = 23`. The 표준형
twin, `point_id = 2`, reaches the **identical policy value** and crosses at **`t = 30`**
(1.009492 against 0.991409 at `t = 29`) — six years later, on the same account, purely
because its denominator is ₩3,084,600 a year instead of ₩2,776,140. **That is the whole of
the refund-ratio argument that sells this product**, stated in two numbers.

### Hand traces

Five years, written out term by term, so that a reader with a calculator can reproduce a row
and watch the processing order do its work. All arithmetic is on the printed rates and on
the full-precision values above.

**Trace, year 1 — the acquisition year.**

    l(1) = 1.000000,  lp(1) = 1.000000,  q(1) = 0.00085,  w(1) = 0.10
    premiums   = 2,776,140.00 x 1.000000                          = 2,776,140.00
    D(1)       = 1.000000 x 0.00085                               = 0.0008500000
    claims_death   = max(0, 100,000,000 - 0) x 0.0008500000       = 85,000.00
    claim_expenses = 300,000 x 0.0008500000                       = 255.00
    V(1)  = ( (0 + 2,106,700.5378440050) x 1.025 - 0.00085 x 1e8 ) / (1 - 0.00085)
          = ( 2,159,368.0512901051 - 85,000 ) / 0.99915           = 2,076,132.7641396238
    SC(1) = 3,106,700.5378440050 x (1 - 1/7)                      = 2,662,886.1752948617
    W(1)  = max(0, 2,076,132.7641 - 2,662,886.1753)               = 0.00
    CV(1) = 0.50 x 0.00                                           = 0.00
    survivors of mortality = 1 - 0.00085                          = 0.9991500000
    S(1)  = 0.9991500000 x 0.10                                   = 0.0999150000
    claims_lapse   = max(0, 0.00 - 0) x 0.0999150000              = 0.00
    expenses  = (3,106,700.5378440050 - 2,019,355.3495986033)     = 1,087,345.1882454017
              + 60,000 x 1.02^0 x 1.000000                        = 60,000.00
              + 0.02 x 2,776,140.00                               = 55,522.80
                                                                  = 1,202,867.9882454018
    commissions = min(0.65 x 3,106,700.5378, 1.00 x 2,776,140.00) = 2,019,355.3495986033
    CF(1) = 2,776,140.00 - 85,000.00 - 0.00 - 255.00
            - 1,202,867.99 - 2,019,355.35                         = -531,338.34
    l(2)  = 1.000000 x 0.99915 x 0.90                             = 0.8992350000

The first year is the only negative one before 완납, and the reason is distributional:
**₩3,106,700.54 of acquisition cost against ₩2,776,140.00 of premium.** The commission cap
of 제4-32조제5항 does not bind — 0.65 × the cost is ₩2,019,355.35 — and the residual
₩1,087,345.19 is booked as acquisition expense. The surrender value is nil, so the 10%
first-year lapse costs nothing in cash: **the first-year lapse benefit is zero by
construction, on the suppressed and the standard form alike.**

**Trace, year 2 — the first year with a payable value.**

    l(2) = 0.8992350000,  q(2) = 0.00092944,  w(2) = 0.0784759970
    premiums   = 2,776,140.00 x 0.8992350000                      = 2,496,402.2529
    D(2)       = 0.8992350000 x 0.00092944                        = 0.0008357850
    claims_death   = 1e8 x 0.0008357850                           = 83,578.50
    claim_expenses = 300,000 x 0.0008357850                       = 250.74
    V(2)  = ( (2,076,132.7641396238 + 2,106,700.5378440050) x 1.025
              - 0.00092944 x 1e8 ) / (1 - 0.00092944)             = 4,198,362.2603524810
    SC(2) = 3,106,700.5378440050 x (1 - 2/7)                      = 2,219,071.8127457179
    W(2)  = 4,198,362.2603524810 - 2,219,071.8127457179           = 1,979,290.4476067631
    CV(2) = 0.50 x 1,979,290.4476067631                           = 989,645.2238033816
    survivors = 0.8992350000 x (1 - 0.00092944)                   = 0.8983992150216
    S(2)  = 0.8983992150216 x 0.0784759970                        = 0.0705027741
    claims_lapse   = 989,645.2238 x 0.0705027741                  = 69,772.73
    expenses  = 60,000 x 1.02 x 0.8992350000                      = 55,033.182
              + 0.02 x 2,496,402.2529                             = 49,928.0451
                                                                  = 104,961.23
    commissions = 0.03 x 2,496,402.2529                           = 74,892.07
    CF(2) = 2,496,402.25 - 83,578.50 - 69,772.73 - 250.74
            - 104,961.23 - 74,892.07                              = 2,162,946.99
    l(3)  = 0.8983992150216 x (1 - 0.0784759970)                  = 0.8278964408871874

**Trace, year 3 — the shape settles.**

    l(3) = 0.8278964409,  q(3) = 0.0010163,  w(3) = 0.0615848211
    premiums   = 2,776,140.00 x 0.8278964409                      = 2,298,356.4254
    D(3)       = 0.8278964409 x 0.0010163                         = 0.0008413912
    claims_death   = 1e8 x 0.0008413912                           = 84,139.12
    claim_expenses = 300,000 x 0.0008413912                       = 252.42
    V(3)  = ( (4,198,362.2603524810 + 2,106,700.5378440050) x 1.025
              - 101,630 ) / 0.9989837                             = 6,367,530.6895912290
    SC(3) = 3,106,700.5378440050 x (1 - 3/7)                      = 1,775,257.4501965743
    W(3)  = 6,367,530.6895912290 - 1,775,257.4501965743           = 4,592,273.2393946547
    CV(3) = 0.50 x 4,592,273.2393946547                           = 2,296,136.6196973273
    survivors = 0.8278964409 x (1 - 0.0010163)                    = 0.8270550497343138
    S(3)  = 0.8270550497343138 x 0.0615848211                     = 0.0509340373
    claims_lapse   = 2,296,136.6197 x 0.0509340373                = 116,951.51
    expenses  = 60,000 x 1.02^2 x 0.8278964409                    = 51,680.6074
              + 0.02 x 2,298,356.4254                             = 45,967.1285
                                                                  = 97,647.74
    commissions = 0.03 x 2,298,356.4254                           = 68,950.69
    CF(3) = 2,298,356.43 - 84,139.12 - 116,951.51 - 252.42
            - 97,647.74 - 68,950.69                               = 1,930,414.96
    l(4)  = 0.8270550497343138 x (1 - 0.0615848211)               = 0.7761210124511136

Note what has happened to the surrender outgo between years 2 and 3: the lapse **rate** has
fallen by 22% while the payable **value** has risen by 132%, so `claims_lapse` rises from
₩69,772.73 to ₩116,951.51. It peaks at ₩139,216.88 in year 5 and then falls for fourteen
years to ₩18,419.29 at `t = 19`, because on the `loglinear` basis the rate collapses faster
than the value grows.

**Trace, year 20 — the cliff.**

    l(20) = 0.5979336235,  q(20) = 0.00464125,  w(20) = 0.0010000000,  m = 20
    premiums   = 2,776,140.00 x 0.5979336235                      = 1,659,947.4497
    D(20)      = 0.5979336235 x 0.00464125                        = 0.0027751594
    claims_death   = 1e8 x 0.0027751594                           = 277,515.94
    claim_expenses = 300,000 x 0.0027751594                       = 832.55
    V(20) = 51,428,412.5364992      SC(20) = 0.00  (t >= n_sc = 7)
    W(20) = max(0, 51,428,412.5364992 - 0)                        = 51,428,412.5364992
    kappa(20) = 1  because t >= m
    CV(20) = 1 x 51,428,412.5364992                               = 51,428,412.5364992
    CVs(20) = 0.50 x 51,428,412.5364992                           = 25,714,206.2682496
    survivors = 0.5979336235 x (1 - 0.00464125)                   = 0.5951584641116814
    S(20) = 0.5951584641116814 x 0.0010000000                     = 0.0005951584641
    claims_lapse   = 51,428,412.5365 x 0.0005951584641            = 30,608.06
    expenses  = 60,000 x 1.02^19 x 0.5979336235                   = 52,264.5830
              + 0.02 x 1,659,947.4497                             = 33,198.9490
                                                                  = 85,463.53
    commissions = 0.03 x 1,659,947.4497                           = 49,798.42
    CF(20) = 1,659,947.45 - 277,515.94 - 30,608.06 - 832.55
             - 85,463.53 - 49,798.42                              = 1,215,728.95
    l(21) = 0.5951584641116814 x (1 - 0.0010000000)               = 0.5945633056475697

**The ratio the implementation must reproduce exactly is `CV(20) / CVs(20) = 2.0`**, i.e.
`1 / k`. Both quantities exist at `t = 20` and the model publishes both. The [std] ordering
rule pays year-20 surrenders on the **full** value; paying them on ₩25,714,206.27 instead
would halve `claims_lapse` in that row.

**Trace, year 21 — the first premium-free year, and where the stream turns.**

    l(21) = 0.5945633056,  q(21) = 0.005075,  w(21) = 0.008
    premiums   = 0.00                        (t > m: no premium, ever again)
    D(21)      = 0.5945633056 x 0.005075                          = 0.0030174088
    claims_death   = 1e8 x 0.0030174088                           = 301,740.88
    claim_expenses = 300,000 x 0.0030174088                       = 905.22
    V(21) = ( (51,428,412.5364992 + 0) x 1.025 - 0.005075 x 1e8 ) / (1 - 0.005075)
          = ( 52,714,122.8499117 - 507,500 ) / 0.994925           = 52,472,922.9338007
    CV(21) = 52,472,922.9338007            (kappa = 1 from t = 20 on)
    survivors = 0.5945633056 x (1 - 0.005075)                     = 0.5915458968714082
    S(21) = 0.5915458968714082 x 0.008                            = 0.0047323672
    claims_lapse   = 52,472,922.9338 x 0.0047323672               = 248,321.14
    expenses  = 60,000 x 1.02^20 x 0.5945633056                   = 53,009.39
                (no premium-related component: no premium)
    commissions = 0.00                       (renewal runs 2 <= t <= m only)
    CF(21) = 0.00 - 301,740.88 - 248,321.14 - 905.22 - 53,009.39  = -603,976.63

**Premiums stop at `m` and nothing else does.** In one row the income line goes from
₩1,659,947.45 to zero, commission from ₩49,798.42 to zero, and every outgo continues:
maintenance expense for life, death claims for life, surrender benefits for life on a value
that is still growing. `net_cf` swings by **₩1,819,705.57** between `t = 20` and `t = 21`,
and is negative in every one of the remaining 56 years. A projection that ends at 납입완료
misses the entire liability.

### Undiscounted totals per policy issued, `t = 1 … 76`

| Column | Total |
|---|---|
| `pols_if` | 28.704474 |
| `premiums` | 38,202,010.270460 |
| `claims_death` | 50,813,891.715166 |
| `claims_lapse` | 9,284,540.176799 |
| `claims_reduction` | 0.000000 |
| `claim_expenses` | 152,441.675145 |
| `expenses` | 4,668,005.848038 |
| `commissions` | 3,082,131.457712 |
| **`net_cf`** | **-29,799,000.602401** |

**Roll-forward check.** Over the full 76 years `Σ D(t) = 0.5081389172` and
`Σ S(t) = 0.4918610828`, summing to **1.0000000000** with `l(77) = 0`; every policy leaves by
one of the two decrements because the table terminates. `pols_if` sums to **28.704474**
policy-years of exposure. All nine `check_*()` cells return `True`.

### Reading the shape of the result

`net_cf` is **income-positive**, so the total of **−₩29,799,000.60** says outgo exceeds
income by ₩29.8m per policy issued over 76 undiscounted years. **That is the expected shape
of a whole-life stream and not a defect.** The contract must eventually pay ₩100,000,000 to
someone: expected death claims of ₩50.81m plus surrender benefits of ₩9.28m come to
₩60.10m of benefit against ₩38.20m of premium, and the ₩21.90m gap is closed by nothing in
this model, because everything that closes it — the investment return on the account,
discounting, the CSM — belongs to a layer this projection deliberately stops before. There
is no `liability_cf`.

Four features of the stream are worth reading off directly. **The liability is back-ended
even by whole-life standards:** 69.5% of expected death claims — 0.353404 of 0.508139 —
fall after `t = 40`, when the insured is over 79 and has paid no premium for twenty years.
**The premium-paying period is profitable and the rest is not:** `Σ net_cf` over
`t = 1 … 20` is **+₩27,935,040.25** and over `t = 21 … 76` is **−₩57,734,040.85**. **The
surrender benefit is small relative to the death benefit** — ₩9.28m against ₩50.81m —
because the `loglinear` lapse vector empties out long before the value is large; on the
`flat` basis the same product pays ₩23.68m of surrender benefit and only ₩18.03m of death
claims, which is a different product economically on the same contract. And **expenses are
dominated by the first year**: ₩1,202,867.99 of the ₩4,668,005.85 total, 25.8% of the
lifetime expense in policy year one, which is what the 표준해약공제액 exists to bound.

### Calibration against the published grid

The model's 표준형 surrender value `cv_std_pp(t)` against DB생명's published 1종 표준형 grid
at the identical cell — 남 40세, 1억원, 20년납, 월납 [S4]:

| t | model `cv_std_pp(t)` | published 해지환급금 | model / published |
|---|---|---|---|
| 1 | 0.00 | 0 | — (both nil) |
| 3 | 4,592,273.24 | 5,087,095 | 0.9027 |
| 5 | 9,962,522.87 | 10,940,547 | 0.9106 |
| 10 | 22,941,773.00 | 25,283,000 | 0.9074 |
| 15 | 36,406,331.66 | 40,501,000 | 0.8989 |
| 20 | 51,428,412.54 | 57,838,000 | 0.8892 |
| 40 | 73,413,688.61 | 86,326,000 | 0.8504 |
| 60 | 91,301,421.85 | 104,604,000 | 0.8728 |

**Durations 3 to 20 sit in a 0.889–0.911 band** — a level offset, not a shape error — and
the first year is nil in both, which is the surrender charge biting exactly as 별표 14
bounds it. The offset is what a construction that sets 계약체결비용 **at** the statutory cap
should produce against a real product that presumably charges less: a higher deduction and a
slightly lower value at every duration.

**The widening past duration 20 has a stated cause and is not a fit failure.** The [S4]
product carries a **전환나이 60세** step-up in its death benefit, so its late-duration values
belong to a **rising** benefit the 평준형 composite does not have. The tell is in the grid
itself: its duration-60 value of ₩104,604,000 **exceeds the ₩100,000,000 sum assured**,
which a level whole-life account cannot do. The table records the divergence rather than
tuning the model to close it.

### The `flat` basis, and the disclosure the guidance obliges

Re-running the identical cell with `lapse_basis = flat` — 4.0% level, the comparison basis
the November 2024 decision requires an insurer to disclose against the 원칙모형 [REG-R27] —
changes the product:

| Quantity | `loglinear` (base) | `flat` |
|---|---|---|
| `lapse_rate(19)` / `(20)` / `(21)` | 0.0012742750 / 0.0010000000 / 0.0080000000 | 0.04 / 0.04 / 0.04 |
| `claims_lapse(19)` | 18,419.29 | 444,737.31 |
| `claims_lapse(20)` | **30,608.06** | **905,221.12** |
| `claims_lapse(21)` | 248,321.14 | 882,162.09 |
| `net_cf(20)` | **1,215,728.95** | **16,276.98** |
| `pols_if(20)` | 0.597934 | 0.442091 |
| `Σ claims_lapse` | 9,284,540.18 | 23,676,385.94 |
| `Σ claims_death` | 50,813,891.72 | 18,032,089.04 |
| `Σ net_cf` | -29,799,000.60 | -10,210,977.48 |

**The cliff moves far less cash than a reader expects on the base vector, and that is the
finding.** On the `loglinear` basis the payable value doubles at `t = 20` but the lapse rate
that year is **0.1%**, so `claims_lapse` is only ₩30,608.06 — against ₩18,419.29 the year
before and ₩248,321.14 the year after, when the rate returns to 0.8% against a value that
has already doubled. **The step is in the value, and the cash the step moves is set by the
rate the supervisor fixed.** On the `flat` basis the same step lands on a 4% lapse rate and
opens a visible one-year hole: `net_cf(20)` falls from ₩1,215,728.95 to **₩16,276.98**,
a 98.7% collapse in a single row, and year 20 stops being a profitable year at all. That
contrast **is** the disclosure the guidance obliges [REG-R27], and it is the reason the base
vector is not a free choice for a Korean insurer.

One second-order effect is worth naming because a reader may misread the headline. The
`flat` run's undiscounted `net_cf` is **better** — −₩10.21m against −₩29.80m — but only
because a 4% lapse rate empties the book before the expensive years: `Σ claims_death` falls
by 64.5%. A high lapse rate looks profitable undiscounted on a product whose 환급률 has not
yet crossed 1, and the sign reverses once the value exceeds premiums paid — which is exactly
why the K-ICS 대량해지위험 shock splits by whether surrender **reduces or increases** net
assets [REG-R36] [R7].

### The other nine model points, and what each one is for

| # | Cell | What it demonstrates | Signature number |
|---|---|---|---|
| 1 | M40, 1억, 20년납, `k = 0.50` | the anchor | cliff ratio exactly **2.0** at `t = 20` |
| 2 | M40, 1억, 20년납, `k = 1.00` | the 표준형 comparison twin | 환급률 crosses 100% at **`t = 30`** against the anchor's 24, on the identical account |
| 3 | M40, 1억, 20년납, `k = 0.00`, loan at `t = 10` | 무해지 + **the loan that cannot exist** | `cv_pp(19) = 0.0`; `loan_draw(10) = 0.0` |
| 4 | F30, 5,000만, 30년납, `k = 0.50` | female, long pay, the long horizon | `proj_len() = 86` |
| 5 | M65, 1,000만, **전기납**, `k = 0.50` | no 납입완료, so **no cliff at all** | `cv_mult(t) = 0.5` for life |
| 6 | M40, 1억, 20년납, `k = 0.50`, loan at `t = 10` | the loan on a suppressed value | `loan_draw(10) = 8,167,325.83`; `loan_pp(76) = 108,712,698.33`, above `SA`, so every payment floors at zero |
| 7 | M45, 1억, 20년납, waiver 0.4% p.a. | 납입면제 as a **state** | `pols_waived(20) = 0.042858` |
| 8 | M40, 1억, **7년납**, bonus 13.8% | 단기납 유지보너스 + the mandatory spike | `lapse_rate(7) = 0.301` against a base of 0.001; 환급률 0.962906 at 완납 |
| 9 | F45, 1억, 20년납, **금리연동형** 2.75% | the declared-rate account | `pol_val_pp(20)` runs **9.38%** above its prospective form |
| 10 | M50, **10억**, 10년납, `k = 0.30`, 감액 at 15, 부활 20%, `flat` lapse, `mort_be_factor` 0.90 | 감액 + 부활 + the level basis + the SA ceiling | `claims_reduction(15) = 163,333,687.53`; `net_cf(15) = -178,134,642.51` |

Point 3 is the one to read next after the anchor. On a **무해지** contract the payable
value is zero throughout 납입기간, so the policy loan the point elects **draws exactly
nothing** — `loan_util = 1.0`, `loan_draw(10) = 0.0` — which is the FSS's 2019 consumer
alert reproduced as arithmetic [R4] [REG-R28]. At `t = 20` the value steps from zero to the
full ₩51,428,412.54 and the 환급률 to **1.068759**, above the 표준형 twin's 0.833632:
제7-66조제4항제2호 나목 is the article that permits it [REG-R19].

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced. Korea is the only market in this repository running **three** of
them at once.

- **IFRS 17 — K-IFRS 제1117호, mandatory since 2023-01-01**, not voluntary as in Japan
  [REG-R60]. The liability is fulfilment cash flows plus a risk adjustment plus the CSM,
  discounted on a 국고채-based curve with 관찰금리 to a **20-year** last observable maturity
  extending to 30 years over three years from 2025, an LTFR of **4.55%** and a liquidity
  premium of **91bp**, and **every assumption is re-set at every reporting date** [REG-R27]
  [REG-R60]. `result_cf()` is the fulfilment-cash-flow engine and nothing more; `v(t)`, the
  risk adjustment and the CSM roll-forward are out of scope. **This product is the reason
  the November 2024 계리가정 decision exists**: the supervisor's own framing — 「무·저해지
  상품은 납입기간 중 해지 시 환급금이 없거나 적은 상품임에도 완납 직전까지 해지가
  발생한다고 가정하여 …」 — is a description of this contract's economics [REG-R27] [R7].
- **K-ICS** — the 신지급여력제도, live in the same quarter. 요구자본 comes from five risk
  modules, of which the life module alone carries seven shock-based sub-risks including
  **해지위험액** and **사업비위험액**; the floor is **100%** and the 적기시정조치 ladder
  starts below it [REG-R13] [REG-R14]; the industry ratio after 경과조치 at 2025-09-30 was
  **210.8%** overall and **201.4%** for life insurers [REG-R30]. The 대량해지위험 shock bears
  directly on this product's design: it splits by whether surrender
  **reduces or increases** net assets, adding **+35%p** or **+25%p** to the next year's lapse
  rate on 순자산 감소상품 and applying **× (1 − 40%)** on 순자산 증가상품, against a flat 25%
  (보장성) or 35% (저축성) mass-lapse on the 표준형 [REG-R36] [R7]. **Those figures come from
  시행세칙 별표 22, which was not retrieved**, so they are second-hand and **[unverified] as
  regulatory text** [REG-R26] [REG-R36] — a gap that matters most to exactly this product,
  whose 고환급형 forms are what the test is about.
- **해약환급금준비금 — Korea's own, with no counterpart anywhere else in this repository.**
  At every balance-sheet date the insurer compares, company-wide, the IFRS 17 잔여보장요소
  against the aggregate contractual 해약환급금 **computed under 제7-66조제1항 — on that rule
  even for the 제7-66조제4항 products that may contractually pay less** — and appropriates
  the shortfall inside 이익잉여금 [REG-R11]. **So a 무해지 contract whose contractual
  surrender value is zero still enters the test at its 별표-14-floored value.** The reserve
  stood at **₩23.7조 at end-2022 and ₩32.2조 at end-2023** [REG-R36] [R7] and is graded by
  K-ICS ratio, a well-capitalised insurer appropriating only **80%** [REG-R11].
  `WholeLife_KR_A` does not compute it; it is named because it is why a Korean insurer's
  economics here depend on the **surrender value**, and because `cv_std_pp(t)` is precisely
  the quantity the test needs.
- **책임준비금.** 보험업법 제120조 delegates the mechanics entirely [REG-R3], and 감독규정
  제6-11조 **delegates the calculation to the FSS Governor** — ten paragraphs of the pre-2023
  article, which carried accumulation rules, having been deleted on 2022-12-21 [REG-R10].
  That deletion is the visible trace of the switch from a locked-in statutory reserve to a
  current-estimate one, and it is why **`pol_val_pp` here is a 계약자적립액 and not a
  reserve**. The same drift shows in the product documents — a pre-2023 상품요약서 writes
  「순보험료식 책임준비금에서 해지공제액을 공제한 금액」 and a 2024 one 「계약자적립액에서
  미상각신계약비를 공제한 금액」 for the identical identity [S2] [S8] — and in the renaming of
  the filing from 「보험료 및 **책임준비금** 산출방법서」 to 「보험료 및 **해약환급금**
  산출방법서」 between the 2023 and 2026 editions [REG-R9]. The *causal* reading is
  **[unverified]**; the wording change is sourced twice.
- **The 산출방법서, and why no further research fixes the pricing basis.** 보험업법
  제5조제3호 names the 기초서류, and the 산출방법서 — where the 예정이율, the 적용위험률, the
  예정사업비율 and the surrender-value formula actually live — is **not published** [REG-R2];
  감독규정 제7-64조 lists its five 필수기재사항, the third being the 해약환급금 calculation
  and, where 계약체결비용 exceeds the 표준해약공제액 at the 기준연령 요건, a comparison of the
  two [REG-R18]. **No amount of further research converts an expense or pricing parameter in
  this document into a sourced value**; what research can do, and did, is bound them by
  published caps and published cash values. The 선임계리사 who verifies the 기초서류 is,
  since 2022, barred from product development and from the CEO and CFO roles — a harder
  separation of pricing from sign-off than the UK Chief Actuary split [REG-R5].
- **Disclosure, not valuation, but binding on the model's outputs.** 제7-45조제7항 requires
  a 보장성보험 to publish a **보험가격지수** and a 보장범위지수 [REG-R22] — how a Korean
  consumer sees the price of a product whose pricing basis is confidential; the two observed
  at this cell are **85.4% / 86.2%** and **110.3% / 110.9%** [S2] [S8]. And the 무(저)해지
  form drew an FSS **소비자경보** in 2019, warning that it is unsuitable as savings and
  **cannot support a policy loan during the payment period** [R4] [REG-R28] — which is why
  `point_id = 3` exists.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The lapse vector, and it is not close.** It is the assumption the supervisor took away
   from insurers on exactly this product [REG-R27] [R3], and switching the anchor from
   `loglinear` to `flat` moves undiscounted `net_cf` from **−₩29,799,000.60 to
   −₩10,210,977.48**, expected death claims from ₩50.81m to ₩18.03m and surrender benefits
   from ₩9.28m to ₩23.68m. Two of those move in opposite directions, so no single-signed
   intuition survives. The shape between the two regulatory endpoints is **[std]** and no
   Korean lapse curve by duration is public.
2. **The suppression factor `k` and where the cliff falls.** `k` is a model point column and
   the market runs 0.00 / 0.30 / 0.50 / 1.00 [S1] [S4] [S6] [S7] [S8]. **Where the cliff
   falls is not universal**: at 납입완료 on three of the five observed designs, at **seven
   years** on a formula design whose payment period runs to twenty [S2], and at **납입기간 +
   3년** on a third [S3]. The composite hard-codes 납입완료 and a model reproducing another
   carrier must expose that date as a parameter.
3. **The expense and acquisition-cost block.** `AC = SC*`, `c₀ = 0.65`, `c_r = 3.0%`,
   ₩60,000 + 2.0% of premium a year, ₩300,000 a claim, 2.0% inflation — **every one [std],
   because no Korean expense rate as a percentage of premium was obtained from any source.**
   They total ₩7,750,137.31 of the ₩38.20m premium stream, 20.3%, and the first year alone
   is ₩3,222,223.34 of it. The four public bounds in class (b) constrain the block; nothing
   fixes it.
4. **The mortality table is a construction and `mort_be_factor` is the lever.** Every row of
   `mort_table.csv` is [std]; the two disclosed carrier grids differ by **10%–23%** and
   bracket rather than fix a level [S2] [S8]; and the 제10회 경험생명표 is not published
   [REG-R33] [REG-R34]. Claims move proportionately with `mort_be_factor`, and on a 76-year
   run they are the largest single outgo at ₩50.81m.
5. **The 보험나이 / 만나이 gap.** No conversion is applied and none is public. The table is
   read about half a year of ageing too young, systematically, which understates `q` by
   roughly 4.6% at the ages that matter most on this cell. It is a **one-directional** bias
   and it is not corrected.
6. **The horizon itself.** ω = 115 is [std]. **69.5% of expected death claims fall after
   `t = 40`**, so any truncation of the projection is a direct and large understatement, and
   moving ω moves the tail rather than the shape.
7. **The 예정이율, and the account's sensitivity to it.** 2.50% is the [std] centre of a
   sourced 2.25%–2.75% band [S1] [S2] [S5] [S6] [S7] [S8]. It enters **twice** — through `P`
   (equivalence) and through the accrual — so it moves the surrender value in the same
   direction from both ends, and the 환급률 crossing date with it. A market-wide 예정이율 cut
   in 2025 and again for 2026 was reported in search results and **could not be confirmed
   against any retrieved carrier document** [unverified]; the 평균공시이율 series that *is*
   sourced fell from 2.75% to **2.50%** for 2026, its first fall since 2020 [S10] [REG-R48].
8. **Expense inflation over 76 years.** 2.0% **[std]** compounds to a factor of **4.42**;
   a UK or US habit of 3% would compound to 9.18. No published Korean expense basis anchors
   either. **부활 is likewise not modelled**, so later-duration in force is understated —
   Korean lapse is genuinely non-terminal, including on a 무해지 contract where there was no
   value to draw [S5 제26조] [REG-R25 제27조].
9. **The absence of an APL is [unverified].** If a 자동대출납입 article is found in the
   생명보험 표준약관 in a later research pass, the lapse mechanics of this chassis change
   **in kind**: lapse becomes a funded event with a continuation test, as in `jplib`, and
   every suppressed-form conclusion about who reaches 납입완료 has to be re-derived.

### Known modeling pitfalls

The mistakes a modeller would actually make on this product. Each is specific and checkable,
and each is either asserted by a `check_*()` cells or by a test in
`tests/test_whole_life_kr.py`.

- **The cliff is a step, not a ramp.** `CV(t) = k W(t)` for `t < m` and `W(t)` for `t ≥ m`,
  with `CV(m) / (k W(m))` exactly `1 / k` — **2.0 on the anchor at `t = 20`** [S1] [S4] [S6]
  [S8]. Interpolating, grading or smoothing across the boundary is wrong. So is assuming the
  step always exists: on a **전기납** point `m` is the whole projection, `cv_mult(t) = k` for
  life, and the cliff never happens (`point_id = 5`).
- **Off-by-one at the boundary.** Surrenders in policy year `m` are paid on the **full**
  value; the suppressed value applies to years 1 … m − 1 **[std]**. Both quantities exist at
  `t = m` — ₩51,428,412.54 and ₩25,714,206.27 — and the model publishes both as `cv_pp` and
  `cv_susp_pp`. A model that loses either cannot state the ordering rule it is using.
- **One policy value, one multiplier.** The suppression is a pure haircut on a **common**
  underlying account: at 납입완료 the suppressed and 표준형 values are **identical to the
  won** in every published grid [S1] [S4] [S6]. Running two account recursions, or deriving
  the suppressed form's value from the suppressed form's own premium, is wrong — and it is
  wrong in a way that destroys the product's economics, because `CV(t)` being independent of
  the sold premium is the **whole** of the refund-ratio argument.
- **The step is not the surrender charge running off.** The 해약공제기간 is capped at **7년**
  by 제7-66조제1항제2호 [REG-R19], so on the anchor's 20년납 contract `surr_chg_pp(t) = 0`
  from `t = 7` — **thirteen years before the cliff**. Attributing the step to amortisation,
  or grading the charge to `m` instead of to `min(m, 7)`, is a common and detectable error:
  `check_surr_chg_cap()` fails on it.
- **`P` and `P₂₀` are different annuities.** 별표 14 주3 recomputes the 연납순보험료 on a
  **20년납** footing for a 보험기간 of 20 years or more [REG-R20]. They coincide only when
  `m = 20`, which the anchor satisfies — so a model tested **only** on the anchor will not
  catch the confusion. Test it on the 7년납 and 10년납 points, where reusing `P` in the cap
  formula overstates the statutory surrender charge.
- **The 보험가입금액 entering the cap is taken before any 체증 or 체감** [REG-R21 별표 15
  제8호], and is the 일반사망보험금 for a 보장성보험 covering 일반사망 [REG-R21 제3호]. On a
  design with a 전환나이 step this is not the benefit in force at duration `t`.
- **Premiums stop at `m`; nothing else does.** At `t = 21` premium and renewal commission go
  to zero in the same row while maintenance expense, death claims and surrender benefits all
  continue for life. `net_cf` swings by **₩1,819,705.57** across that boundary and is
  negative in all 56 remaining years. A projection that stops at 납입완료, or that keeps
  charging renewal commission past it, misses the majority of the liability. So does one that
  keeps the premium-related expense running on zero premium.
- **The policy loan does not exist on a 무해지 contract during 납입기간.** There is no value
  to lend against, so `loan_draw` must be **exactly zero** even at `loan_util = 1.0` — which
  is `point_id = 3` [R4] [REG-R28] [REG-R25 제33조]. A model that computes the limit off
  `cv_std_pp` instead of `cv_pp` lends against a value the policyholder cannot claim, and on
  a 저해지 contract lends exactly twice too much.
- **Everything is floored at zero, and on this product the floor bites.** `W(t) =
  max(0, V(t) − SC(t))` is zero at `t = 1` on the anchor; the death benefit `SA(t) − L(t)`
  and the surrender payout `CV(t) − L(t)` both go negative once an unrepaid loan outgrows the
  value, which happens on `point_id = 6` where `loan_pp(76) = ₩108,712,698.33` exceeds the
  ₩100,000,000 sum assured. None of the three may produce a negative payment.
- **Booking the 유지보너스 without the mandatory lapse spike.** The supervisor requires an
  **additional lapse of at least 30%** at any bonus date [REG-R27] [R3]; on `point_id = 8`
  that takes `lapse_rate(7)` from 0.001 to **0.301**. Turning the bonus on alone misstates
  the liability in the insurer's favour, which is precisely what the guidance exists to
  prevent. `lapse_spike()` is wired to `bonus_rate()` so the pair cannot be separated by
  accident.
- **The prospective identity does not hold on a 금리연동형 point.** Once the crediting rate
  differs from the pricing rate the account is path-dependent: on `point_id = 9`
  `pol_val_pp(20)` runs **9.38% above** `prosp_val_pp(20)`. `check_pol_val_prosp()` is
  defined as zero there rather than asserted. Asserting it unconditionally fails; "fixing" it
  by discounting the account on the pricing rate silently changes the product.
- **`pol_val_pp` is a 계약자적립액, not a reserve, and never a cash flow.** Under K-IFRS
  제1117호 the insurer books no 보험료적립금 [REG-R60] [REG-R10], and the model computes no
  책임준비금, no CSM, no 요구자본 and no 해약환급금준비금. None of `pol_val_pp`, `cv_std_pp`
  or `cv_pp` may be read as a reserve or appear in `net_cf`.
- **Waived premiums count as paid, and a waived policy is a state.** 「보험료가 … 정상적으로
  납입된 것으로 하여 사망보험금 및 해지환급금을 계산합니다」 [S2] [S3] [S8]. Modelling the
  waiver by scaling the premium down, or by suppressing the account accrual, breaks the one
  route to the cliff the policyholder does not have to fund. The premium is weighted by the
  paying cohort and everything else by the whole in-force count; the two are equal in the
  base run, so an implementation that weights premium by `pols_if(t)` reproduces this worked
  example exactly and fails only once the waiver module is switched on.
- **Lapse is behavioural in Korea, not funded.** There is **no 자동대출납입** in any
  retrieved Korean document [S5] [REG-R25], so no continuation test precedes the decrement
  and a policyholder who misses fourteen days loses the contract whatever its cash value.
  Importing `jplib`'s APL machinery models a mechanic Korea has not been shown to have — and
  the reverse import is just as wrong: `jplib`'s lapse rate applied without the APL test
  models a decrement **that** contract does not have.
- **감액완납 and 연장정기보험 are not Korean features on this evidence.** Neither appears in
  the 60-article 약관 or in any 상품요약서 in the set [S5], and both are **[unverified]**
  rather than established. A reader arriving from `jplib` — where 払済保険 and 延長定期保険
  are both in the 約款 — will reach for them. What Korea offers in that slot is **감액**, a
  partial surrender paying `k W(t)` during 납입기간 and nothing at all on a 무해지 contract
  [S5 제20조].
- **A refused claim is not a zero payment.** 상법 제736조 obliges the insurer to pay 「보험
  수익자를 위하여 적립한 금액」, in practice the 계약자적립액 [REG-R50] [REG-R25 제22조].
  Modelling an exclusion as forfeiture overstates the insurer's position by the account, not
  by the claim. The composite carries no exclusion incidence, so nothing is deducted.
- **There is no 고도장해 benefit to add.** Korea puts no severe-disability acceleration at
  the sum assured on this chassis [S2] [S3] [S6] [S8]; the slot is filled by the premium
  waiver, which **continues** the contract instead of extinguishing it. Adding a disability
  decrement at `SA` — the Japanese habit — invents a benefit and double-counts a decrement.
- **The 환급률 test and the value test are not the same test.** `check_cv_cliff()` asserts
  that the payable **value** never exceeds the 표준형 twin's, which `k ≤ 1` guarantees. It
  does **not** assert the press-release framing 「전(全) 보험기간 동안 표준형 보험의 환급률
  이내로」 [REG-R28], because the denominators differ: on `point_id = 3` the 무해지 form's
  post-완납 환급률 is **1.068759** against the 표준형's **0.833632**, which satisfies
  제7-66조제4항제2호 나목 as recorded in the 고시 [REG-R19] and contradicts the press-release
  reading. Both statements are recorded as they stand and **neither is resolved here**; a
  model that asserts the press-release form will fail on a legal design.
