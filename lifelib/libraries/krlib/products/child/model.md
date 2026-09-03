# Implementation Notes

**Status:** Draft, 2026-09-03. Built from
[`product-spec.md`](product-spec.md); the worked example the model reproduces is in
[`technical-notes.md`](technical-notes.md), and the sources are resolved in
[`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the 태아가입특칙 verbatim [S8 제53조~제61조], the two
> ages a foetal contract carries, the 면책기간 disapplied below 보험나이 15 and entirely on
> a 태아 cover [S3] [S11] [R5], the 감액 removed from foetal contracts by a 2015 변경권고
> [R2], the statutory bar on a death benefit below 만 15세 and the 계약자적립액 paid instead
> [R7] [REG-R17] [REG-R25], the two premium waivers with the P코드 carve-out [S2] [S10
> 제22조], the 3년만기 갱신형 liability block [S2] [S5], the published 해약환급금 grid and
> the 무해지 cliff [S2] [S1]. **Almost everything quantitative is a [std]
> standardization.** Nothing on Korean child incidence was retrieved from 보험개발원,
> 국가암정보센터 or 통계청; the 참조순보험요율 is filed and never published [REG-R4]; the
> 산출방법서 that holds the 적용위험률 and the 예정사업비율 is an undisclosed 기초서류
> [REG-R2]; the 제10회 경험생명표 is released only as summary statistics
> [REG-R33] [REG-R34]. **Exactly one 적용위험률 is published anywhere in this file** —
> 일반상해 후유장해 발생률(3~100%), 기본계약, 5세, 상해 1급: 남자 0.0001823, 여자 0.0001163
> [S1] — and it is the calibration point of the basic contract's decrement. Replace the
> tables with company data and a real 산출방법서 before drawing any conclusion from the
> numbers.

## Run it

```bash
python products/child/run.py
python products/child/run.py 2      # the calibration cell, boheom nai 5, no modules
python products/child/run.py 4      # the 무해지 (mijigeuphyeong) point
python products/child/run.py 9      # the 30세만기 short-term point
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/child/Child_KR_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell — a
**태아가입** contract, priced male, 계약나이 0 at the 계약일, birth at policy month 5, to a
100세 만기 with a 20년 납입기간. `result_cf()` returns a `DataFrame` indexed by policy
month `t` with one column per cash flow line, `pols_if` first and `net_cf` last;
`expenses` there is acquisition plus maintenance, with the claim handling expense in its
own `claim_expenses` column. `result_pols()` publishes the decrement run — including the
paying and waived compartments and the two ages side by side — and `result_val()` the
account and the surrender values.

The anchor projection is **1,201 rows**: `t = 0` to `t = proj_len() = 1200`. That is the
longest in `krlib` and it is the product, not an artefact.

## The horizon, and where it comes from

`proj_len()` is `12 × (term_age() − issue_age())`, and on a 태아 contract `issue_age()` is
zero because 「계약일에 있어서의 피보험자의 계약나이는 0세로 합니다」 [S8 제60조]. So the
projection runs 1,200 months to the 100세 계약해당일 and the premium runs over the first
240 of them. **Eighty of the hundred years are paid-up**, which is the whole shape of the
liability: `net_cf(t)` is positive for twenty years and negative for eighty, and the
undiscounted total on the anchor cell is **−₩13,103,720** against premiums of
**₩5,458,038**. That is not a defect in the projection. It is what a hundred-year contract
with a twenty-year premium term looks like before discounting, and it is why
`equiv_premium_mth_pp()` exists.

The terminal date is fixed by the **계약일** and not by the birth, so the insured's 만나이
at expiry is 100 less the pre-birth period — **99 years and 7 months** on the anchor cell.
`result_pols()` prints `age` (보험나이) and `age_man` (만나이) in adjacent columns so the
five-month offset can be read off any row.

## The pre-birth period is the part with no analogue anywhere

Months `t = 0 … 4` on the anchor cell carry premium income on all three streams, a **void**
decrement, and nothing else. `born(t)` is false, so every cover on the child's own life is
identically zero and there is neither mortality nor morbidity on the insured:
`mort_rate(t)` is 0 and `age_man(t)` returns −1. `check_cover_at_birth()` asserts it over
`t < birth_month()`, summing the seven child-life claim kinds and requiring zero.

The decrement is `pols_void`, and it is not a lapse. 「태아가 유산 또는 사산에 의해
출생하지 못한 경우에는 **계약을 무효로 합니다** … 이미 납입한 보험료를 돌려드립니다」
[S8 제56조] [S9]: nothing is retained, the contract is de-recognised rather than
terminated, and the cash flow is a refund of **every** premium paid — the 태아 module's own
stream included, which is why `claims(t, "VOID")` adds `prem_foetal_paid_pp(t)` to
`cum_prem_pp(t)`. It is published in its own `claims_void` column so that it is never
netted into `claims_lapse`, where it would look like a surrender value on a contract that
has none.

The 태아 module itself is the one thing that pays in respect of an event before the insured
legally exists, and it pays **from the date of birth** [S8 제59조]. It is therefore
deliberately excluded from `check_cover_at_birth()` and tested separately by
`check_neonatal_term()`, which requires it to pay inside `birth_month() ≤ t <
foetal_cover_end()` and nowhere else.

The rate is a `[std]` construction and the model says so in the cells: **no Korean source
retrieved gives a foetal-loss rate.** What the sources fix is the mechanic.

## Two decrement lives, and a premium that stops on the earlier of two events

The in-force block is carried in two compartments:

`pols_pay(t)`
: in force and still paying premium. Exposed to the void decrement, the waiver, mortality
  and lapse.

`pols_waived(t)`
: in force with the premium waived. Cover continues in full and payment of the 적립보험료
  stops as well [S2]; **not** exposed to lapse, a policy paying nothing having nothing to
  lapse for.

`pols_if(t)` is their sum and is the weight on every `result_cf()` row.
`check_waiver_split()` asserts the identity month by month.

The entry rate `waiver_rate(t)` is `1 − (1 − child)(1 − payer)`. The child's limb is the
cancer, cerebrovascular and cardiac incidences plus `waiver_disab_share` of the two
후유장해 incidences, standing for the 7대질병, the 50% 이상 후유장해 and the
중대한특정상해수술 triggers of [S2]. The 계약자's limb is that life's own mortality grossed
up by `payer_disab_ratio` for the 50% 장해 limb of [S10 제22조]. **The two are read from
two different rows of the same table**, at two different ages, and the second life is 33
years older than the first.

Three implementation points are worth stating because they are choices:

1. **The P코드 carve-out is implemented, not averaged away.** 「출생전후기에 기원한 특정
   병태(P코드) 진단시 납입면제를 적용하지 않음」 [S2]. On a 태아 contract
   `waiver_rate_child(t)` returns zero for `t < foetal_cover_end()`, so the covers most
   likely to pay in the first year of a foetal contract are precisely the ones that cannot
   stop the premium.
2. **The 계약자 limb runs from `t = 0`**, before the insured exists. The policyholder is an
   insured of the contract in his own right — the 생명보험 wording makes the 피보험자
   「계약자와 가입자녀」 [S10 제3조] — so his death is a contractual event from the 계약일.
3. **The two decrements are treated as independent [std]**, and the 계약자 is held fixed for
   the whole projection. A change of 계약자 would change the decrement life mid-projection
   and no retrieved wording says how the waiver responds; the point is marked [unverified]
   in the specification.

## Processing order, and the identity it closes

Within month `t` the order is **void, then the waiver, then mortality, then lapse**
`[std order]`:

```
l_P(t+1) = ( l_P(t) (1 - v(t)) - e(t) ) (1 - q(t)) (1 - w(t))
l_W(t+1) = ( l_W(t) (1 - v(t)) + e(t) ) (1 - q(t))
```

with `e(t) = pols_waiver_entry(t)`. Summing them gives

```
l(t+1) = l(t) - pols_void(t) - pols_death(t) - pols_lapse(t)
```

exactly, which is `check_pols_roll_fwd()`. There are **four exits, not two**, and the first
of them is what makes this product different: a voided contract has not lapsed and has not
died, and netting it into either would hide a decrement and mis-state the cash flow that
goes with it. `check_exit_total()` is the global companion — the four decrements sum over
the projection to `pols_if_init()`, so no mass is lost at the ends.

`pols_if_at(t, timing)` exposes the intermediate states, `"BEF_DECR"` / `"BEF_LAPSE"` /
`"AFT_DECR"`, on the same convention the sister libraries use.

## The benefit is a bundle, and one limb of it is a percentage scale

`benefit_pp(t, kind)` returns the expected outgo per policy in force; `claims(t, kind)`
weights it by `pols_if(t)`. Seven morbidity kinds and four decrement kinds, published as
eleven `claims_*` columns that sum, with the three expense lines, to `net_cf`.

**`"DISABILITY"` is not a lump sum.** The 기본계약 pays 보험가입금액 × 장해지급률 on a
continuous 3~100% scale, payable more than once with the percentages accumulating
[R12] [S1] [S2] [S11], and 장해 is a **settled** impairment — 「치유된 후 신체에 남아 있는
영구적인」 [REG-R25] — so its incidence lags the accident. The model multiplies the
incidence by `disab_severity` = 0.12 `[std]`. A model treating the cover as a lump sum at
₩100,000,000 would overstate this limb by about eight times, which is the single largest
modelling trap in the product.

**`"DIAGNOSIS"` is four 최초 1회한 ledgers.** Each of 암(유사암 제외), 유사암, 뇌출혈 and
급성심근경색증 carries its own `frac_open(t, cause)` — the probability that a policy in
force at `t` has not yet claimed that benefit — recursed as
`frac_open(t) = frac_open(t-1) (1 - i_m(t-1))`. `check_once_only()` asserts that each stays
in `[0, 1]` and never rises. The 유사암 tier is where the product's shape is clearest: it is
20% of the general amount on the chassis ratio, 갑상선암 is overwhelmingly an adult cancer,
so the tier costs almost nothing for thirty years and then becomes the most frequently paid
diagnosis benefit in the contract.

**`"HOSPITAL"` is metered in days, not events.** The `hosp_acc` and `hosp_dis` causes are
expected days per policy year, multiplied by `hosp_daily()` and by `hosp_cap_factor` = 0.92
`[std]` for what survives the 1~180일 per-stay limit. **No 180-day one-hospitalization
memory is implemented**: no retrieved Korean child wording states a re-admission grouping
rule, and inventing one would be an unsourced benefit mechanic. On the shipped basis this is
the largest single benefit line on the anchor cell — **₩5,033,285 undiscounted**, more than
the premium — and the infant peak is visible in the statement: `claims_hospital` falls from
₩7,164 at `t = 16` to ₩3,512 at `t = 17`, which is 만나이 turning from 0 to 1.

**`"LIABILITY"` is the only limb whose claim is a third party's loss**, and the only one a
non-life licence is needed to write [R5] [S5]. It is also where the renewal mechanic has its
one cash consequence: the 누수사고 limb's 90-day 보장개시일 **resets at every renewal** of
the 3년만기 갱신형 block [S5] [S3], so `leak_share` = 0.40 `[std]` of the cost is off for
the first three months of each 36-month cycle. The 갱신형 chassis proper — the whole product
written of 20년/30년 renewable blocks with cover-group ceilings [S7] — is **not**
implemented; it is a documented option and is out of the base run.

**`"NEONATAL"` runs on two terms of its own.** `neonatal_cost_pp("birth")` = **₩47,000** per
birth is the 태아보장기간 limbs — 출생위험 on its three tiers and 조산 진단 — paid at
`t = birth_month()`; `neonatal_cost_pp("block")` = **₩63,450** is the 1년만기 신생아 block,
spread evenly over its twelve months. Two of the limbs are **day-capped rather than
amount-capped** and the table holds expected paid days after the contractual deduction and
inside the cap:

```
incubator benefit = 50,000 x max(0, min(days_used, 60) - 2)          [S1]
perinatal cash    = 10,000 x max(0, min(stay_days, 120) - 3),        [S8] [S1]
                    payable only where stay_days >= 4
```

The module's cost is therefore a length-of-stay question rather than an amount question,
which is why the supervisor's own worked claim — ₩16,836,420 on a birth at 32 weeks and
1.84 kg [R3] — is the useful datum. On the anchor cell the module costs **₩106,331**
undiscounted against a module premium of ₩3,000 × 17 = ₩51,000: the shipped module does not
pay for itself on the shipped basis, and that is reported rather than tuned away.

## The 면책기간 is tested at the 계약일, once, and never again

```
암보장개시일 =
    the day the first premium is received     if 보험나이 < 15 at the 계약일
    the 91st day counting 계약일 as day 1      if 보험나이 >= 15 at the 계약일
    the day the first premium is received     if the cover is a 태아가입용 form
```

`waiting_mths()` is a model point input and `cover_open(t, cover)` applies it to the two
cancer limbs alone. **A model that re-tests the rule at each anniversary is wrong**: the
wording is 「계약일 현재 보험나이 15세 미만 피보험자의 경우」 [S11] and 「최초계약과
부활계약의 면책기간은 보험나이 15세 이상인 경우에만 적용」 [S3], so a contract issued at
계약나이 0 has no cancer waiting period at any point in its hundred-year life, including the
eighty-five years during which the insured is an adult. Model point 7, issued at 보험나이 15,
is the cell on which the switch is on.

`reduction_mths()` returns **zero whatever the model point says on a 태아 contract**, because
the 2015 변경권고 inserted 「단, 피보험자가 보험가입 당시 태아(胎兒)인 경우에는 보험금의
100%를 지급합니다」 across 17 carriers and 56 products [R2]. The disapplication lives in the
cells rather than in the data so that it cannot be switched off by editing a CSV.

## Death pays the account, because a death benefit would be void

`claims(t, "DEATH")` is `(av_pp(t) + unearned_prem_pp(t)) × pols_death(t)` and it is **not a
death benefit**. 상법 제732조 makes a contract on the death of a person under 15 무효
[R7] [REG-R50], 표준약관 제19조제2호 restates it and 제19조제3호 refuses to extend the
age-correction saving to it [REG-R25]; what is paid instead is the 계약자적립액 at the date
of death plus the 미경과보험료, which is what 감독규정 제7-63조제1항제1호 requires of a
제3보험 contract on a death it does not cover [REG-R17] and what 상법 제736조 floors
[REG-R50].

On the anchor cell that is **₩3,693,355 undiscounted** — the second largest outgo line after
hospital cash — because the 표준형's account crosses premiums paid at about year 30 and keeps
rising, and most deaths on a hundred-year contract are late ones. On the 미지급형 switch
(model point 4) the same line is close to nil for the whole payment period, and a family
whose child dies in year 10 receives almost nothing. That is a real and uncomfortable
property of the suppressed form and the model reproduces it rather than smoothing it.

## The account is recovered from a published grid, and the first two years are [std]

`av_table.csv` carries the 표준형 환급률 grid a current 상품요약서 publishes on a named
specimen contract [S2] as a `build` curve indexed by duration in years, and a `taper` curve
indexed by the fraction of the term run off. `refund_ratio(t)` is their product,
`cv_std_pp(t) = refund_ratio(t) × cum_prem_pp(t)`, and `check_refund_grid()` asserts that
the model returns the published figure at every node it reaches — 0.0% at 1 year, 45.6% at
3, 62.5% at 5, 73.7% at 10, 78.3% at 15, 82.6% at 20, 101.2% at 30, 122.5% at 40, 144.1% at
50 and 158.9% at 60. It is the one check in the model that ties a computed quantity to a
number a reader can look up.

Splitting the progression in two is what lets one shipped grid serve a 30세만기, a 100세만기
and a 110세만기 point. The taper node at 0.95 is calibrated so that a 100세만기 contract
reproduces the published **16.0% at 95 years** and pays nothing at 만기 — there is no
만기환급금 on the protection part [S1] [S2], so `claims_maturity` is a column of zeros on the
shipped progression. It is published rather than dropped because the residual 적립부분 is a
real quantity on a contract whose term ends earlier.

**Recovering the 계약자적립액 from the surrender value is where a [std] enters, and the model
is explicit about it.** What the 상품요약서 publishes is 「순보험료식 계약자적립액에서
해약공제액을 공제한 금액」 [S2] — already net of the charge and floored at zero — so the
account can be recovered by adding the unamortised charge back only where the floor is not
binding. Where it is, the identity gives no more than `0 ≤ AV ≤ 해약공제액`, and `av_pp(t)`
is capped instead at the cumulative **net** premium, which is the most a 순보험료식 reserve
can have accumulated before interest or mortality. The account therefore starts at nil, as
it must, rather than at the surrender charge. `check_av_bounds()` asserts all three
inequalities.

## The surrender charge is computed from the regulation, and both its inputs are [std]

`surr_chg_cap_pp()` is the **표준해약공제액** of 감독규정 [별표 14] [REG-R20]:

```
5% x 연납순보험료 x 해약공제계수  +  보장성보험의 보험가입금액 x 10/1000
```

The 해약공제계수 is the policy term capped at 20 — 「보험기간(최대 20년)」 — and binds at 20
on every model point here. The second term is the harder half, and it is the one place where
this product's lack of a death benefit changes the arithmetic: **[별표 15] 제3호 does not
apply and 제9호 does**, 「보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의
보험가입금액」 [REG-R21]. A term policy's risk premium per unit of face is its mortality
rate, so the notional amount is the first policy year's risk premium divided by that rate at
the 기준연령 요건, 남자 만 40세 [REG-R9 제1-2조제2호]. On the anchor cell:

| Quantity | Value |
|---|---|
| first-year risk premium `risk_prem_ann_pp()` | ₩145,537.05 |
| notional 보험가입금액 `sa_notional_pp()` | ₩132,306,409 |
| 연납순보험료 `prem_net_ann_pp()` | ₩252,000.00 |
| **표준해약공제액 `surr_chg_cap_pp()`** | **₩384,306.41** |
| 계약체결비용 `acq_cost_pp()` at 90% of the cap | ₩345,875.77 |
| the same, in months of premium `acq_cost_months()` | **12.35** |

That last row is the cross-check worth having. The FSC's 2019 expense reform states the same
cap as roughly **thirteen months' premium** for a 보장성보험 [REG-R29], and the [별표 14]
computation lands at 12.35 without being asked to. It is published as a diagnostic rather
than asserted as a check, because the two readings do not agree exactly on a low-premium
short-term model point where the notional 보험가입금액 is large relative to the premium.
`check_acq_cost_cap()` tests the [별표 14] bound only; `check_surr_chg_cap()` tests that the
deducted charge never exceeds it, over a 해약공제기간 capped at seven years
[REG-R19 제7-66조제1항제2호].

## The three surrender-value forms

```
cv_pp(t) = cv_std_pp(t)                                       [pyojunhyeong]
         = 0                                        t < m     [mijigeuphyeong]
         = k x cv_std_pp(t)                         t >= m
         = 0                                        t < m     [mijigeuphyeong III]
         = min(0.05 (1 + (t-m)//24), k) x cv_std_pp(t)  t >= m
```

`check_cv_floor()` asserts all three, including that the suppressed value is **exactly nil**
through the whole 납입기간: the cliff is a contractual fact and not an approximation, and the
「60원」 and 「550원」 entries in the published grid are rounding on a nominally zero quantity
[S2]. The graded ladder is the published ten-step one — 5% from the day after the end of year
M to the day before the M+2 계약해당일, then 10, 15, 20, 25, 30, 35, 40, 45 and finally 50%
from M+18 [S1].

**`Child_KR_S` ships the 표준형 as its base, which is the opposite of `Cancer_KR_S`.** The
market is in the suppressed forms — 63.8% of 보장성 초회보험료 by 2024 H1 [R11] [REG-R27] —
and the cancer chassis ships one. This product ships the standard form because the 적립부분
credited at the 공시이율 exists only there, the suppressed forms being 순수보장성 and showing
「-」 for it on the board [S11] [S2]; because the 표준형's value **exceeds premiums paid from
about year 30**, a shape no other `krlib` protection product produces and only a hundred-year
term can; and because shipping the two forms on two products lets a reader compare them
inside one library without either model carrying both.

## Discounting, and the one place the model does discount

The projection publishes **undiscounted gross liability cash flows**, as every model in this
library does; discounting, the 책임준비금, the IFRS 17 CSM and the K-ICS 요구자본 belong to a
layer that consumes them.

The exception is a set of pricing diagnostics that are not in `result_cf()`.
`pv_factor(t)` discounts at the **보장부분 적용이율 of 2.75%** — the modal value of the
comparison board's column, whose observed range is 2.50%–3.00% [S11]. (A full-text search of
the 감독규정 returns **zero** occurrences of 예정이율: the regulation speaks only of the
계약자적립액 적용이율 and of the 금리확정형 / 금리연동형 distinction [REG-R9] [REG-R48], and
the board's 보장부분 적용이율 is the pricing rate under another name.) Then

```
equiv_premium_mth_pp() = epv_outgo_pp() / epv_prem_unit_pp()
```

On the anchor cell that is **₩31,200.64** against a shipped ₩28,000, from an EPV of outgo of
₩4,712,867.73 over 151.0504 discounted monthly premium units. It is a **first-order**
equivalence — the expense basis is held at the level the shipped premium produces rather than
re-scaled with the answer — and `check_equiv_premium()` verifies that the two 1,201-term
summations reproduce each other.

**Where the equivalence premium and the shipped ₩27,000 / ₩28,000 differ, the computed figure
governs.** Nothing in the model depends on the model point's premium being a market rate: no
carrier publishes a rate table by age and duration, and the board's own specimen premiums
vary by a factor of seven on a nominally standardised basis — ₩21,502 to ₩148,250 for a male
5-year-old — because carriers include different compulsory sets in the quoted 보장보험료
[S11]. That the shipped basis lands 11% above the mid-market cluster is the calibration
finding, and it is the honest one.

## Inputs are external files

Seven CSVs live beside `run.py` in `products/child/`, not inside the model folder — the
`annuallife/TradLife_A` layout. Every reader and every `*_file` Reference is on the
unparameterized `Data` Space, so each file is read **once per model** and not once per model
point. `Data.input_dir()` resolves to `_model.path.parent` at run time, so the model works
from any checkout.

| File | What it holds |
|---|---|
| `model_point_table.csv` | ten model points; `point_id = 1` is the anchor |
| `mort_table.csv` | annual mortality by sex and 만나이 0–120, for the child **and** the 계약자 |
| `incidence_table.csv` | eleven causes × two sexes × fourteen pivot ages, log-linearly graduated |
| `basis_table.csv` | thirteen scalar `[std]` parameters that turn an incidence into a cost |
| `neonatal_table.csv` | the 태아 module's nine limbs, with timing, frequency, amount and units |
| `lapse_table.csv` | three lapse bases: the 원칙모형, the disclosed vector and a flat one |
| `av_table.csv` | the published 환급률 `build` grid and the `taper` that takes it to 만기 |

**Every assumption file carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the one exemption: a model point is a
configuration, not an assumption.

## Lapse, and the vector that is the argument

`lapse_rate(t)` is the **annual** rate and `lapse_rate_mth(t)` the monthly one, per the house
convention. Three bases ship:

- **`loglinear`** — the 2024-11-07 계리가정 guideline's 원칙모형: a log-linear decay from the
  first-year rate to **0.1% at 납입완료** and **0.8%** thereafter [REG-R27] [R11]. The
  guideline's own functional form was never converted from HWP and is **[unverified]** at
  instrument level; the two endpoints are verified from the 보도자료. The 5.0% start is the
  top band of the only 적용해지율 any Korean child product publishes [S1].
- **`disclosed`** — the step function one carrier discloses for its suppressed forms, 5.0%
  for the first ten years, 3.0% from ten to fifteen, 1.0% thereafter during the payment
  period and 0.5% after 납입완료 [S1]. This is the comparison the guideline itself obliges an
  insurer departing from the 원칙모형 to disclose, and shipping the two side by side is what
  makes that comparison possible.
- **`flat`** — a level vector, the nearest a projection can come to the **synthetic** 표준형
  the 환급률 comparison is made against, which is priced with no lapse assumption at all
  [S1] [S3].

**Lapse is absorbing.** 부활 is available within three years even where there is no surrender
value [REG-R25 제27조] [S8], every waiting period re-runs from the 부활일 [S3], and below
보험나이 15 there is no cancer waiting period to re-run — so a reinstated child policy is,
uniquely in this library, very nearly the policy that lapsed. The model does not carry it;
the simplification is conservative on a protection product and is recorded as one.

## Modules that are off in the base run, and modules that are not modelled

Off but switchable, on a model point: the **해약환급금 미지급형** and **미지급형Ⅲ**, the
**감액기간** (`reduction_mths`, observed 0 and 12), the **면책기간** (`waiting_mths`,
observed 0 and 3), the **broad 뇌혈관질환 / 허혈성심장질환 definitions** (`broad_def`, at
`broad_def_factor` = 4.0 `[std]`), the **2026 저출산 premium discount** (1%–5% for twelve
months [R6]), **110세만기**, the two **waiver** modules, the **태아** module, and the three
lapse bases.

Not modelled, and deliberately: the full **갱신형 chassis** [S7]; the **임신·출산질환 module**
written on the mother and the **부양자 benefit stack** written on the parent [S2] [S5] [S11],
the second of which the composite replaces with the waiver because a benefit and a decrement
are not the same cash flow; **다태아** plans [R4]; the named-cancer riders and the
후유장해 생활지원금 annuity forms [S1] [S11]; **일반상해사망 from 만 15세** [S1] [S4];
**부활**; the **공시이율 reset**, which the model carries by reference to `WholeLife_KR_A`;
and **실손의료비 riders of any kind**, which have not been attachable to a child policy since
April 2018 and are a statutory impossibility rather than a design choice [R9] [R10]
[REG-R17]. No exclusion decrement is modelled: the general 보험금을 지급하지 않는 사유
articles were not read in full for this product line, and that gap is stated rather than
filled.

## Sign convention

`net_cf` is **income positive** — premiums less benefits, claim handling expense, acquisition
and maintenance expense and commission. That is the library-wide sign and it is the notes'
own, so there is no outgo-positive `liability_cf` companion. `check_net_cf()` reconstructs
`net_cf(t)` from the seventeen published columns of the same row and
`check_net_cf_resid(t)` gives the per-month residual, so an eleventh claim kind added and
left out of the statement fails rather than vanishing.

## Naming

House vocabulary throughout: `model_point`, `proj_len`, `age`, `pols_if`, `mort_rate`,
`claims`, `expenses`, `net_cf`, `result_cf`; `pols_death`, `pols_lapse`, `pols_maturity`,
`pols_if_init`, `premium_mth_pp`, `mort_rate_mth`, `lapse_rate` / `lapse_rate_mth`, `av_pp`,
`cv_pp`, `surr_chg_pp`, `cv_floor_ratio`, `refund_ratio`, `mort_be_factor`,
`check_pols_roll_fwd`, `check_net_cf`, `roll_fwd_tol`, `val_tol`. Product-specific names are
kept English and descriptive — `pols_pay` / `pols_waived` for the two compartments,
`pols_void` for the pre-birth decrement, `frac_open` for a 최초 1회한 ledger, `born` for the
태아가입 gate, `age_man` for the second age, `neonatal_cost_pp` for the module — and no
romanized Korean appears in a cells identifier, per the library's naming review.

## Standardizations used

Every one is tagged at the point of use, in the cells docstring or in the `provenance` column
of the CSV row. The load-bearing ones:

| Standardization | Value | Why |
|---|---|---|
| every incidence rate | see `incidence_table.csv` | nothing on Korean child incidence was retrieved; the one exception is the 5세 disability anchor [S1] |
| mortality | `mort_table.csv` | 경험생명표 is not published in full [REG-R33] [REG-R34]; shaped on 완전생명표 [REG-R38] [REG-R39] |
| 장해지급률 severity | 0.12 accident / 0.15 disease | the benefit is a *fraction* of `S`; the distribution is not published |
| foetal-loss rate | 1.2% a year pre-birth | no Korean source gives one |
| P코드 carve-out | child waiver off over the 신생아 block | a sourced carve-out, implemented approximately |
| waiver independence | product of complements | nothing relates the two lives |
| 계약자 age / sex | 만 33, male | mid-point of the 20~47세 band the mother-side riders state [S2] |
| 순보험료 share | 0.75 | no Korean 예정사업비율 is published [REG-R2] |
| expenses | ₩400 a month + 5% of premium + ₩30,000 a claim | no retrieved document quantifies any expense item |
| expense inflation | 2.0% a year | the Bank of Korea target; over 100 years it compounds to 7.2 |
| 해약공제액 release | linear over the 해약공제기간 | the regulation caps the amount, not the shape |
| account before year 2 | capped at cumulative net premium | the published grid is floored at zero there |
| lapse shape | log-linear between two published endpoints | the guideline's form is [unverified] at instrument level |

## Tests

`tests/test_child_kr.py` asserts the technical notes' worked example cell by cell to the
precision the notes display, the first-year aggregate, the roll-forward and waiver-split
identities, the pre-birth gate, the 태아 module's two terms, the once-only ledgers and the
published 환급률 grid. `tests/test_model_conventions_kr.py` asserts the house style — the
two-Space layout, the read-once property, the documentation, the naming, the `result_cf()`
contract and that every `check_*()` closes on every one of the ten model points.
