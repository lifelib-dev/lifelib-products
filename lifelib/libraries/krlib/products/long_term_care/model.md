# Implementation Notes

**Status:** Draft, 2026-09-03. The product this implements is specified in
[`product-spec.md`](product-spec.md); the worked example is in
[`technical-notes.md`](technical-notes.md) and the sources are resolved in
[`sources.md`](sources.md). Every parameter value here is one of theirs, and where the model
carries something the documents do not settle, it is named below rather than absorbed.

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced on
> this product is the contractual machinery: the grade-only trigger with no company-basis limb,
> the once-only 장기요양진단급여금 (*janggi-yoyang jindan geubyeogeum*) that extinguishes its
> own benefit line without terminating the contract, the survival-tested 간병연금 (*ganbyeong
> yeongeum*) with its twelve-month guarantee and 120-month cap, the amount and the 감액 both
> frozen at first certification, the 납입면제 firing on the same event as the benefit, the bar
> on surrender once the annuity has started, the nil 해약환급금 during the premium-paying
> period, and the 계약자적립액 payable on death from a cause the contract does not cover [S1]
> [S2] [S3] [S4] [REG-R17]. Almost everything quantitative is a **[std]** standardization.
> 보험개발원 publishes **neither a 장기요양 incidence table nor a post-onset mortality table**,
> the 경험생명표 is not released in full [REG-R33] [REG-R34], and no 사업방법서 or 산출방법서
> was retrieved for any Korean long-term-care product — so the office premium is a model-point
> **input**, the mortality table is a construction anchored on published summary 기대여명, and
> the whole morbidity basis is built in public from the 노인장기요양보험 통계연보 [R4] and
> calibrated against the one disclosed 예정위험률 [S1]. Replace the assumption tables with
> company data before drawing any conclusion from the output.

`LTC_KR_S` is the modelx implementation: a monthly, single-model-point projection of gross
best-estimate liability cash flows for 간병보험 (*ganbyeong boheom*, long-term-care insurance)
on the **공적기준 (type ②)** design, whose 지급사유 is written by reference to a 장기요양등급
awarded by a 등급판정위원회 under the 노인장기요양보험법 and to nothing else.

**The chassis.** This product states its deltas against the `krlib` fixed-benefit (정액)
제3보험 chassis, whose model is [`Cancer_KR_S`](../cancer/model.md). `LTC_KR_S` does **not**
inherit from it in modelx — `Projection._bases` is empty and every formula here is written out
— so the relationship is documentary, not structural. What is inherited in substance is the
monthly grid, the timing conventions, the 만나이 projection basis, the mortality construction,
the 90-day 보장개시일 with its 재해 carve-back, the one-year 50% 감액기간, the 무해지환급형
surrender-value cliff and the log-linear lapse vector. What is replaced outright is the trigger
and with it the shape of the liability: cancer pays on a **pathological event with a date**,
long-term care pays on an **administrative determination of a state** in which the insured then
lives, draws an annuity, stops paying premiums and dies at a rate well above a healthy life's.
There is no severity ladder here, no 유사암 reduced tier and no 재진단 clock; there is a
compartment chain and a survival-tested annuity ledger instead.

## Run it

From the repository root:

```
python lifelib/libraries/krlib/products/long_term_care/run.py       # anchor cell, point 1
python lifelib/libraries/krlib/products/long_term_care/run.py 5     # another model point
```

or, three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("lifelib/libraries/krlib/products/long_term_care/LTC_KR_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked example's anchor cell and
`Projection[5]` a different policy. A full cold sweep of the nine shipped model points takes
about a minute.

## Four compartments, three of which add to `pols_if`

The contract is a **three-state model** — healthy, in long-term care, dead — but the care state
is not entered in one step. Only **13.3%** of current 1등급 certifications arose from a first
application, against 69.5% from a renewal, whereas at 인지지원등급 — a grade nobody can
progress *down* into — the first-application share is **69.8%** [R4 표2-5, derived].
Severe-grade lives are in the main people who entered the scheme years earlier at a light grade
and deteriorated. So the in-force block is carried in three compartments and one absorbing
counter:

| Cells | What it holds | Premium | Lapse | Mortality |
|---|---|---|---|---|
| `pols_healthy(t)` | never certified | pays | exposed | `mort_rate_mth` |
| `pols_light(t)` | certified **below** `benefit_grade()` | pays | exposed | `mort_rate_light_mth` |
| `pols_care(t)` | certified at or above it | waived | **not** exposed | `mort_rate_care_mth` |
| `pols_dem(t)` | already paid the 치매 rider | — | — | `mort_rate_dem_mth` |

`pols_act(t)` is the first two together — the premium-paying, lapse-exposed population — and
`pols_if(t) = pols_act(t) + pols_care(t)`. `pols_dem` is a **first-event counter nested
inside** the block, never added to it; `check_nesting()` asserts both the addition and the
nesting.

Zero lapse in the care state is a **constraint, not an assumption**: the premium is waived, and
the 약관 bars surrender outright once the annuity has started — 「최초 지급사유가 발생한 후에는
이 특약을 해지할 수 없습니다」 [S1].

Within a month the order is **certification, then mortality, then lapse** [std].
`pols_*_mid(t)` are the counts after the month's certifications and before its mortality, and
they are what the death and lapse decrements are taken from.

## 인정률 is a prevalence, and the conversion is the modelling work

The one large public dataset counts people **holding** a certification, not people entering one
[R4]. Writing `P(x)` for the all-grade prevalence at 만나이 `x`, `s_G(x)` for the share of
certified lives at grade `G` or above, `P_C = s_G P`, `P_L = P - P_C`, and `mu_H`, `mu_L`,
`mu_C` for the three forces of mortality with `mu_bar` the population average, the compartment
identities in a stationary population are

    inflow_C(x) = P_C'(x) + P_C(x) ( mu_C(x) - mu_bar(x) )
    inflow_L(x) = P_L'(x) + P_L(x) ( rho(x) + mu_L(x) - mu_bar(x) )

**The excess-mortality term is not a refinement.** A rising prevalence understates entry,
because the compartment it measures is being drained by an excess mortality the population
around it does not carry — and that drain is exactly what the 간병연금 is exposed to. Using
`mu_C` alone in place of `mu_C - mu_bar` overstates entry, materially so at the ages where the
certified share is large; that is why `mort_force_avg_at` exists.

Two equations carry three unknowns. The closing assumption is the one the sources leave open:
`direct_entry_share` = **0.20** [std], the share of gross inflow into the care state arriving
straight from health rather than by progression, anchored on the 13.3% / 69.8% split above.
Then

    i_D(x) = direct_entry_share * inflow_C(x) / ( 1 - P(x) )
    rho(x) = ( 1 - direct_entry_share ) * inflow_C(x) / P_L(x)
    i_L(x) = inflow_L(x) / ( 1 - P(x) )

which are `inc_rate_direct_at`, `prog_rate_at` and `inc_rate_light_at`. Getting
`direct_entry_share` wrong does not change the lifetime claim count much; it changes **when**
the claim arrives, which on a contract priced at 2.0% over fifty years is most of the answer.

Three properties belong in front of a reader rather than in a footnote.

- **Stationarity.** The cross-sectional 인정률 by age is read as the prevalence path a cohort
  will follow. The Korean certified stock grew **71.8%** in six years [R4] [R18], so the
  cross-section is not a cohort path, and the identity **understates** entry.
- **The care compartment leaves only by death.** **107,365** current certifications — 9.2% of
  the stock — arose from a 등급변경신청, so grades move both ways [R4 표2-5]. No retrieved
  source gives a transition matrix, so the model implements the threshold it can evidence; the
  omission understates entry again.
- **Below 65 there is no prevalence data at all.** The statute admits an under-65 applicant
  only through the closed 25-item 노인성 질병 list — no cancer, no musculoskeletal condition,
  no frailty category [REG-R55] [R2] — so below 65 the two entry rates are carried down from
  their age-65 values on `sub65_factor_at`, the log-gradient of the one disclosed 예정위험률:
  **13.0% a year for men and 17.9% for women** [S1, derived]. The progression rate is **not**
  scaled, being a property of a life already certified rather than of the gate.

## The disclosed 예정위험률, and the ratio the model publishes

Exactly one retrieved document publishes a Korean long-term-care incidence rate: one carrier's
예정위험률 at 만나이 40, 50 and 60 by sex, for 요양(1등급) and 요양(2등급) separately [S1]. It
is used for its **gradient and its sex ratio** below 65, and as the level cross-check — never
as the level. `disclosed_inc_ratio_at(x)` publishes the comparison rather than hiding it:

| 만나이 | model first-entry rate over disclosed 예정위험률, male anchor cell |
|---|---|
| 40 | 0.240 |
| 50 | 0.246 |
| 60 | 0.240 |

So the disclosed pricing rate is about **4.2 times** this model's best estimate at the same
age, and the ratio is almost flat, which is what a level difference rather than a shape
difference looks like. Four things all push the same way and none of them is quantified by any
retrieved source: a 예정위험률 is a **loaded** rate and not a best estimate; the conversion
reads a cross-section as a cohort path in a growing scheme; the care compartment is treated as
leaving only by death; and the disclosed card is quoted on **보험나이**, about half a year
older than this model's 만나이. It is the largest single uncertainty in the model and
`technical-notes.md` carries it as a stated sensitivity rather than closing it with an invented
factor.

The construction is nonetheless coherent with the *other* sourced anchor. At the shipped basis
the present value at the 예정이율 of the anchor cell's long-term-care benefit outgo is
**46.0%** of the present value of its premium income, and the present value of its whole
expense and commission basis is **20.3%** against the 20.7% loading `net_prem_ratio()` implies
— and the anchor premium of ₩5,600 is a figure built from a published rate card [S2] and not
from this model. The female anchor runs at 51.5%, so the model's population-derived sex ratio
is steeper than the card's. The seven other model points carry premiums set at approximately
the anchor's ratio, landing between 31% and 43% once model point 7's 60-month annuity cap and
model point 8's 간편심사 loading are applied.

## The grade share is indexed by age, and that is load-bearing

`share_ge_at(grade, x)` interpolates linearly between six sourced band representative ages — 60
for the under-65 band, then 67, 72, 77, 82 and 88.5 — because the severe share is **U-shaped**
in age: 1·2등급 is **22.2%** of certified lives under 65, falls to **11.1%** at 80-84 and rises
again to **14.8%** at 85 and over [R4 표2-9, derived]. The under-65 population is severe
because only the 노인성 질병 list gets in at all; the 80-84 trough is where the marginal
entrant is a lightly impaired person newly crossing the 51-point line. **A model applying one
grade-mix vector at all ages mis-prices a 1~2등급 benefit by up to a factor of two.**

Because the share moves with age, `prev_care_slope_at` uses the **full product rule**, `s_G'(x)
P(x) + s_G(x) P'(x)`. The first term is negative over most of the range for a severe threshold;
dropping it overstates the entry rate wherever the severe share is falling.

`share_slope_at` is exact for the piecewise-linear share rather than a difference quotient, and
`prev_slope_at` is the **analytic** derivative of the logistic — a numerical derivative would
put noise straight into the claim rate.

## The 간병연금 ledger: monthly, annually tested, guaranteed for a year, capped

Instalments are **monthly**; the cohort certified in month `s` is paid in months `s … s + n_A -
1`, of which the first twelve are guaranteed against death and each later block of twelve is
released only by the annual survival test on the anniversary of the 진단확정일 [S1]:

    ann_count(t) = sum over u = 0 … n_A-1 of  n_C(t-u) * weight(u)
    weight(u)    = 1                                   for u < annuity_guar_mths()
                 = S_C(t-u, t-u + 12*floor(u/12))      otherwise

The first instalment falls in the **month of certification**. `care_surv(s, t)` is a **partial
product** of `(1 - q_C(u))` and never a ratio of cumulative products: `q_C` reaches 1 at the
terminal age of the table, so a cumulative product underflows to zero and the ratio form
divides by zero exactly where the tail of this liability lives.

`ann_pay(t)` is the same sum valued at each cohort's **own** amount, `ann_amount_at(s)`, which
is what carries the two freezes [S1]:

- the **amount** is the grade-blend at the entry age — `annuity_high` at 1등급 and
  `annuity_low` at every other grade inside the gate, weighted by the age-specific grade shares
  — so a life entering at 2등급 and deteriorating to 1등급 keeps the lower rate for all ten
  years;
- the **감액 decision** is frozen too. A claim starting inside the reduction window stays
  halved for the whole term of the annuity. **A model that re-tests the 감액 at each instalment
  date overstates every claim arising in the first policy year**, which is the single most
  easily mis-modelled rule in the product.

`ann_tests(t)` counts the annual proof-of-life events — 「매년 진단 확정일에 피보험자의
주민등록등본을 제출하여야 합니다」 [S1] — and the claim-handling expense is charged on those,
not on every monthly instalment.

The cap and the maturity truncation bind **jointly**: nothing is paid at or after `proj_len()`.
An insured certified at 85 on a 90세만기 contract has five years of term and ten years of
annuity, and no retrieved document resolves whether the instalments continue past maturity. The
model truncates, which is the conservative reading, and it materially understates the benefit
for late entrants [std].

## 보장개시일 and 감액기간 are two different mechanisms

Korean practice keeps them apart and so does the model.

- **보장개시일.** A certification inside the window does **not** defer the claim: it makes the
  benefit 무효 and the premiums paid for it come back — 「특약을 무효로 하며, 이미 납입한
  보험료를 돌려드립니다」 [S1] [S2] — and unlike the cancer chassis there is no cancellation
  option and no revival. Those lives are `pols_void(t)`, a **decrement** with `claims(t,
  "VOID")` attached, and they never reach `pols_entry_care`. On the anchor cell it is three
  months at 만나이 40, so the decrement is of order 1e-7 of the cohort; it is carried because
  it is a product fact, not because it is material.
- **감액기간.** Cover has started and the benefit is merely halved. `red_factor(t)` returns `1
  - (1 - red_fraction) * disease_share`. The 약관 test is on the **cause**, not the grade — a
  질병-caused certification inside the window is paid at 50%, an 상해/재해-caused one in full
  [S4] — and the relative frequency of the two is given by **no retrieved source**, so
  `disease_share` = 0.95 [std] and the blended factor is **0.525**. The accident carve-out is
  named rather than dropped.

Model point 9 carries the other observed combination — 180 days and two years at 50%, the
우체국 design [S1] — so the spread is reachable without a second chassis.

## The 계약자적립액, and why a pure protection contract carries an account

감독규정 제7-63조제1항제1호 requires a 제3보험 contract to pay the **계약자적립액**, plus the
미경과보험료, on death from a cause the policy does not cover, and terminate [REG-R17] [REG-R25
제22조]. So death here is **a decrement with a large cash flow attached**, which the Japanese
counterpart does not have at all: on the anchor cell 35% of the cohort dies before maturity and
`claims_death` is a third of undiscounted premium income.

`av_pp(t)` has two branches meeting at 납입완료:

- up to it, the accumulation of the net premium at the **예정이율 of 2.0%** — the one place in
  `krlib` where the pricing interest rate is a *retrieved* figure, stated in terms in a
  기초서류 extract [S1];
- after it, the sourced run-off of `av_table.csv`, indexed on the **fraction of the way from
  납입완료 to maturity** so that one published progression serves every term and paying period
  [std].

`net_prem_ratio()` is **derived, not assumed**: the fraction that, accumulated at the 예정이율
over the paying period, reproduces the sourced 계약자적립액 at 납입완료. On the anchor cell it
is **0.7932**, implying a 예정사업비 loading of 20.7%. `check_av_continuity()` asserts the
join, and it fails the moment someone replaces the derivation with a round number.

Two reconstruction assumptions are named rather than buried. The published progression is the
*미지급형's* 환급률 against its own premiums, and the model reads the doubled figure as that
contract's own 계약자적립액 — but the 기본형 comparator is a product that **cannot be bought**,
「'기본형'은 … 가입이 불가능하며 … 해지율을 적용하지 않고 계산합니다」 [S2], and its premium is
higher, so the two accounts are not in fact the same quantity [std]. And the run-off between
the sourced anchors is linear [std], where the real curve bends with the risk cost.

## The surrender-value cliff, and the four forms that are three names

`cv_pp(t)` implements three of the four forms on the Korean shelf, as a model point field
rather than a switch on a ratio, because reading 「50%」 without reading which side of 납입완료
it attaches to puts the cliff upside down:

| `cv_form` | during the paying period | after 납입완료 | source |
|---|---|---|---|
| `mijigeup` | **nil** | 50% of the 계약자적립액 | [S2] |
| `half_during` | 50% | 100% | [S4] |
| `pyojun` | `max(AV - 해약공제액, 0)` from year 1 | the same | [S1] [REG-R19] |

The composite is `mijigeup`, because **63.8% of Korean 보장성 초회보험료 in 2024 H1 was written
in a 무·저해지 form** [REG-R27] and a library modelling only 표준형 would be modelling a
minority of the market. Its legal basis is 감독규정 제7-66조제4항, which lets a 순수보장성보험
priced on a **최적해지율** pay less than the ordinary 계약자적립액 − 해약공제액 floor
[REG-R19].

On the anchor cell the model reproduces the published 환급률 progression exactly — **0.0% at
years 1, 5, 10 and 15, 48.7% at 20, 54.4% at 30, 50.5% at 40 and 0.0% at 50** [S2] — because
those figures *are* the input. `check_cv_form()` asserts the shape rather than the values: the
해약환급금 is never negative, never exceeds the account, and on the 미지급형 form is exactly
nil for the whole premium-paying period.

`surr_chg_pp(t)` runs the 해약공제액 off straight-line over the premium-paying period **capped
at seven years** [REG-R19 제7-66조제1항], at the supervisor's own rule of thumb of **13 times
the monthly premium** for a 보장성보험 [REG-R29]. The rule of thumb is used rather than 별표
14's formula because 별표 15 제9호 computes the notional 보험가입금액 of a contract with no
death benefit as a ratio of risk premiums that **excludes** 「치매 또는 일상생활장해 등 타인의
간병을 필요로 하는 상태」 — read literally, it excludes long-term-care risk premium from the
very ratio that gives a care-only contract its 보험가입금액 [REG-R21].

## The waiver is not an independent decrement here

`G_W = G_B`. The 납입면제 fires on the **same event** as the benefit, waiving the main contract
and every attached rider [S3], so unlike the Japanese product there is **no band of lives
paying nothing and claiming nothing** — the single most mis-modelled item in that product
simply does not exist. It is implemented by charging premium on `pols_act(t)` rather than on
`pols_if(t)` and nothing else.

It is not free, though: it converts a level premium into a stream that stops at an uncertain
date and stays stopped for the duration of the care state, and that duration is exactly the
quantity the prevalence-to-incidence conversion cannot pin down. On the anchor cell — issue at
40, 20년납, a claim expected in the eighties — the waiver almost never bites inside the paying
period. At model point 6, issue 65 with a 10-year pay, it does.

## Modules that are off in the base run

- **The 치매진단급여금 rider** (`dementia_rider`, on at model points 5 and 8). Its incidence is
  built by the **same prevalence-to-incidence identity** from a *sourced* prevalence — the 2023
  치매역학조사 band rates, 4.99% at 65-69 rising to 21.18% at 85 and over [R7] — rather than as
  a share of the certification rate, because the two triggers are correlated but not
  proportional. `dementia_wait_mths = 15` is the one-year 보장개시일 plus the 90-day
  persistence test written into the definition of the state itself [S2] [S4]; the one-year
  period is not a carrier choice but the settled market answer to the 2019 supervisory
  intervention [R10]. Two weaknesses are named: the 65-69 and 70-74 anchors are almost equal
  and no logistic reproduces that (the fit is out by 31% at 70-74), and the sex factor is
  **flat in age** where the sourced series has the male rate above the female at 65-79 and
  below it at 80 and over [R7] — so the model does **not** reproduce the market fact that 치매
  covers are priced cheaper for women while 장기요양 covers are priced dearer [S2].
- **The 간병연금** (`annuity_on`, off at model point 4). Switching it off reduces the contract
  to a lump-sum-only cover and removes most — not all — of the dependence on the post-onset
  mortality basis: the waiver still stops premium for the duration of the care state.
- **The 간편심사 loading** (`uw_loading`, 1.40 at model point 8). A **premium** multiplier
  only. No retrieved source gives the simplified pool's incidence separately, so on a loaded
  model point the extra premium is pure margin in this model and the true claim cost of that
  pool is understated [S2].
- **The 표준형 lapse vector** (`lapse_form`, `pyojun` at model point 7), carried so the two
  assumptions can be compared — which is the comparison [REG-R27] requires an insurer to
  disclose.

## Absences that are product facts

- **No general death benefit.** No retrieved life-side long-term-care contract pays one [S1]
  [S3]. What `claims_death` carries is the statutory **계약자적립액**, not a sum assured.
- **No 만기환급금.** 「이 상품은 순수보장성보험으로 보험계약 만기시 지급받는 금액(만기환급금)이
  없습니다」 [S3]. `claims_maturity` is a column of zeros, published rather than dropped.
- **No policy loan and no 보험료 자동대출납입** during the paying period on the 미지급형 form:
  there is no surrender value to lend against, so a missed premium lapses the contract outright
  [REG-R25 제33조] [REG-R28]. There is nothing to break the fall, and the lapse assumption
  nonetheless has lapse *falling* toward 납입완료.
- **No recovery decrement.** The contract makes the care state absorbing for cash-flow purposes
  — the amount is frozen and the instalments are metered on **survival**, not on continued
  certification [S1] — so a Korean 간병연금 needs a post-onset **mortality** basis and not a
  recovery basis. This is a simplification the *contract* makes, not one the model imposes.
- **No 갱신형 machinery.** Every retrieved document writes the long-term-care benefit 비갱신형
  and attaches renewal to the hospital-carer and 노인성 질환 riders travelling with it [S1]
  [S2]. The invariance is the finding.
- **No 간병인사용일당.** The daily indemnity for hiring a carer during a hospital stay shares
  nothing with this product but the word 간병; it is a hospital-days frequency-severity cover
  [R15] and is out of scope. Note that its one published rate is a **frequency, not a
  probability** — 0.49 to 2.30 across ages and sexes, in days [S1].

## Inputs are external files

Eight CSVs live beside `run.py`, not inside the model folder, and are read **once per model**
by the unparameterized `Data` Space. This is the `annuallife/TradLife_A` layout; contrast
`basiclife/BasicTerm_S`, which keeps its inputs inside the model. The consequence: **the model
is not portable on its own** — copying `LTC_KR_S/` without its parent's CSVs produces a model
that reads and then fails on first evaluation.

| File | Read by | What it holds |
|---|---|---|
| `model_point_table.csv` | `model_point_table()` | nine policies; the only file exempt from the provenance rule |
| `mort_table.csv` | `mort_table()` | healthy-life q by sex and 만나이 30-120, a [std] construction |
| `prevalence_table.csv` | `prevalence_table()` | the 연령별 인정률 anchors [R4] and the fitted logistic |
| `grade_share_table.csv` | `grade_share_table()` | cumulative grade shares by age band [R4 표2-9] |
| `incidence_table.csv` | `incidence_table()` | the disclosed 예정위험률 [S1] |
| `dementia_table.csv` | `dementia_table()` | the 치매역학조사 prevalence [R7] and its fitted logistic |
| `lapse_table.csv` | `lapse_table()` | the four lapse parameters [REG-R27] |
| `av_table.csv` | `av_table()` | the 계약자적립액 run-off from the published 환급률 [S2] |

Every row of every assumption file carries a `provenance` cell beginning with a citation tag,
which is this library's own escalation of the house rule: when **every** row is a
standardization, "the column is populated" stops being a meaningful check and "the row says
which authority it stands on" starts being one.

### The mortality table is a construction, not a copy

경험생명표 — the industry experience table, 제10회 applied from 2024-04 — is produced by
보험개발원 and is **not published in full**: only the summary, the 평균수명 and the 기대여명,
is released [REG-R33] [REG-R34]. There is no Korean analogue of a downloadable standard table,
and the single-year 완전생명표 qx tables were not retrieved either [REG-R39]. `mort_table.csv`
is therefore a **[std] Makeham-Gompertz construction**,

    q(x) = 1 - exp( -( A + B * c^x ) ),   A = 0.0003 [std],  c = 1.10 [std]

in which `B` is solved, per sex, so that the complete expectation of life at 65 reproduces the
published 경험생명표 65세 기대여명 — **23.7 years for men and 27.1 for women** [REG-R33]. That
is the only thing fitted. The construction then reproduces the *second* published summary
statistic without being asked to: the implied 평균수명 at issue age 40 is **86.4** for men
against the published 86.3, and **90.3** for women against 90.7. The agreement is a cross-check
on the shape, not evidence about any insurer's experience, and **no conclusion about Korean
insured mortality should be drawn from the file**. There is no best-estimate adjustment factor:
the anchor is an experience statistic, not a valuation margin, so there is nothing to unwind.

Two impaired-life bases sit on top of it as multiples, because **no retrieved source gives a
post-certification mortality table by grade**:

- `care_mort_mult = 3.0` [std]. The yearbook roll-forward and the application-route estimator
  agree that the mean duration of a certification is near **4 to 5.5 years** [R4] [R18,
  derived], and the mean 만나이 of a certified decedent is over 75 [R11]; at 만나이 82 on the
  shipped table a mean duration of 4.5 years implies a force of 0.222 against a healthy force
  of 0.075, a multiple of **2.96**. The one study measuring time from certification to death —
  516.2 days, 8.7% inside a month, 45.6% inside a year [R11] — is a **right-censored decedent
  cohort** and a lower bound, so it fixes the early shape and not the level. Note the coupling:
  `care_mort_mult` is also the excess-mortality term of the incidence identity, so it moves the
  entry rate and the annuity's run-off in **opposite directions at once**.
- `light_mort_mult = 1.8` [std], between healthy and care. The mean 인정점수 of certified
  decedents is 82.1, squarely inside 2등급 [R11], so the deaths are concentrated in the severe
  grades and a light-grade life is materially healthier than that cohort. There is **no
  observed range**.
- `dem_mort_mult = 2.5` [std], for the rider's own ledger. No source gives it.

## Sign convention

`net_cf(t)` is **income positive**: premiums less every benefit, less expenses, less the
claim-handling expense, less commission. The technical notes print the same sign, so there is
no outgo-positive `liability_cf` companion to publish. The shape to expect is a deep month-0
strain — acquisition expense plus the whole initial commission against a single month's premium
— then thin positive margins for twenty years, then a long negative tail.

## Naming

Library vocabulary throughout: `model_point`, `proj_len`, `age`, `pols_if`, `mort_rate`,
`claims`, `expenses`, `net_cf`, `result_cf`; `mort_rate` / `mort_rate_mth` and `lapse_rate` /
`lapse_rate_mth` for the annual and monthly pairs; `check_*()` with no argument returning a
`bool` and its per-`t` residual at `check_*_resid(t)`; `prem_int_rate` for the 예정이율, never
a romanized Korean identifier. `proj_len()` is the **last projected period index**, so
`result_cf()` carries `proj_len() + 1` rows and its last row is the maturity instant.

Cells whose names end `_at` are keyed by **만나이** rather than by `t` — `mort_rate_at_age`,
`prev_rate_at`, `inc_rate_direct_at`, `av_ratio_at`. They exist because the morbidity
construction has to evaluate the whole basis at 만나이 65 while the life being projected is
younger than that.

## Standardizations used

Every number the model carries that is not read from a sourced row, with where it comes from.

| Reference | Value | Basis |
|---|---|---|
| `care_mort_mult` | 3.0 | [std] from the 4-5.5 year duration bracket [R4] [R18] and the decedent cohort's shape [R11] |
| `light_mort_mult` | 1.8 | [std]; no source, bounded by the 82.1 mean 인정점수 at death [R11] |
| `dem_mort_mult` | 2.5 | [std]; no source |
| `direct_entry_share` | 0.20 | [std] from the 13.3% / 69.8% first-application split [R4 표2-5] |
| `prog_rate_cap` | 1.0 | [std] guard; does not bind on any shipped model point |
| `sub65_age` | 65 | [REG-R54] 노인장기요양보험법 제2조제1호 |
| `disease_share` | 0.95 | [std]; the 질병 / 상해 split of certifications is in no retrieved source |
| `red_fraction` | 0.50 | [S4]; invariant wherever a 감액 is stated |
| `dementia_wait_mths` | 15 | [S2] [S4]: a one-year 보장개시일 plus the 90-day persistence test |
| `prem_int_rate` | 0.02 | **[S1]**, retrieved: 「연단위 복리 2.0%」 |
| `surr_chg_ratio` | 13.0 | [REG-R29] 표준해약공제액 rule of thumb for a 보장성보험 |
| `surr_chg_years` | 7 | [REG-R19 제7-66조제1항] 해약공제기간 cap |
| `expense_acq_mths` | 5.2 | [std]; 13.0 − 7.8, so acquisition plus initial commission is the 표준해약공제액 |
| `comm_init_mths` | 7.8 | [REG-R29]; 60% of the 표준해약공제액, the cap on annual commission |
| `comm_renewal_rate` | 0.03 | [std]; no Korean renewal-commission scale was retrieved |
| `expense_maint` | 200.0 | [std], set so the PV of the whole expense basis at the 예정이율 lands on the 20.7% loading `net_prem_ratio()` implies; it lands at 20.3% |
| `expense_claim` | 30000.0 | [std]; per claim **event** — first certification, each annual survival test, a dementia diagnosis |
| `inflation_rate` | 0.02 | [std]; the Bank of Korea inflation target, no retrieved Korean expense-inflation assumption |
| `prev_ceil`, `prev_beta`, `prev_x_mid` | fitted | [std] three-parameter logistic through five sourced 인정률 [R4] |
| `dem_ceil`, `dem_beta`, `dem_x_mid` | fitted | [std] three-parameter logistic through five sourced prevalences [R7] |
| `lapse_year1` | 0.08 | [std]; no Korean durational persistency series retrieved |
| `lapse_completion`, `lapse_ultimate` | 0.001, 0.008 | **[REG-R27]**, the guidance's own values |
| `lapse_level_std` | 0.04 | [std] 표준형 comparison vector |
| Monthly rates | `1 - (1-q)^(1/12)` for decrements, `/12` for incidence | [std], uniform within the policy year |
| Processing order | certification, mortality, lapse | [std order] |
| Annuity truncation at maturity | conservative reading | [std]; no retrieved document resolves it |

Model point premiums are **inputs**, not assumptions: the two anchors are [S2]-derived and the
other seven are set at approximately the anchor's implied discounted benefit ratio, which is a
configuration choice recorded in `technical-notes.md`.

## Checks

Six, each taking no argument, returning a real `bool`, and `True` on every shipped model point,
with the signed per-`t` residual under `check_*_resid(t)`.

| Check | What it asserts |
|---|---|
| `check_pols_roll_fwd()` | `l(t) − l(t+1) = deaths + lapses + voids + maturities` — the four ways a life leaves |
| `check_nesting()` | the three compartments are non-negative and add to `pols_if`; `pols_dem` stays inside it |
| `check_ann_ledger()` | `ann_count(t)` equals an independent rebuild scanning every cohort in the window |
| `check_av_continuity()` | the two branches of `av_pp` meet at 납입완료 |
| `check_cv_form()` | the 해약환급금 is non-negative, never exceeds the account, and is exactly nil during the paying period on the 미지급형 form |
| `check_net_cf()` | `net_cf(t)` re-adds from the seventeen columns of `result_cf()` |

## Tests

`tests/test_long_term_care_kr.py` asserts the technical notes' worked example cell by cell to
the precision the notes display, the policy-year-1 aggregate, the compartment recursions, the
annuity ledger's freezes, the surrender-value cliff and the known modelling pitfalls. The
house-style contract — the `Data` / `Projection` split, the docstrings, the naming, the frame
conventions and the read-once property — is asserted for every model in the library by
`tests/test_model_conventions_kr.py`.
