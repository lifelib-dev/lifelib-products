# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`product-spec.md`](product-spec.md); the worked
example the model reproduces is in [`technical-notes.md`](technical-notes.md), and every
source tag is resolved in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced — the level whole-of-life 사망보험금 with no 만기보험금, the identity
> 해약환급금 = 계약자적립액 − 해약공제액, the 표준해약공제액 formula of 별표 14 and the
> seven-year 해약공제기간 cap, the fact that the suppression multiplies a **표준형 comparison
> twin priced with the lapse assumption switched off** and not sold, the equality of the
> suppressed and 표준형 values from 납입완료, the policy-loan rate formula 예정이율 + 1.5%,
> and the 50% 장해지급률 premium waiver with premiums **deemed paid**. Every quantitative
> assumption is a **[std]** standardization. The 예정이율, the 적용위험률 and the 예정사업비율
> live in the filed but unpublished 산출방법서 [REG-R2]; the 제10회 경험생명표 is not published
> in full [REG-R33] [REG-R34]; and no carrier publishes an expense rate, a commission scale or
> a lapse curve by duration. Replace them with company data and a real 산출방법서 before
> drawing any conclusion from the numbers.

## Run it

Two ways, and they are the same model. From the repository root:

```bash
python products/whole_life/run.py            # the anchor cell, point_id = 1
python products/whole_life/run.py 3          # the 무해지환급형 point
python products/whole_life/run.py 8          # the 단기납 유지보너스 point
```

The runner prints the basis it used, the cash flow statement around 납입완료, the surrender
values at the same durations, the undiscounted totals and every `check_*()`. Its first and
last blocks on the anchor cell, abridged to the width of this page — the runner prints two
further header fields, the `claims_reduction` and `claim_expenses` columns, more rows and the
whole of `result_val()`:

```text
WholeLife_KR_A - jongsin boheom (whole life), annual grid, boheom nai
model point 1: WL-KR-0001 - M40, cover KRW 100,000,000, 20-year premium term
form: jeohaeji hwangeuphyeong (low surrender value), k = 0.50
premium = KRW 2,776,140.00 p.a.   projection = 76 years to attained age 115
basis: pricing rate 2.500%   accrual rate 2.500%   policy loan rate 4.000%
net level premium P = KRW 2,106,700.54   pyojun haeyak gongjeaek = KRW 3,106,700.54
...
    pols_if    premiums  claims_death  claims_lapse    expenses  commissions      net_cf
t
1      1.00  2776140.00      85000.00          0.00  1202867.99   2019355.35  -531338.34
19     0.60  1669150.22     255204.77      18419.29    84906.87     50074.51  1259779.18
20     0.60  1659947.45     277515.94      30608.06    85463.53     49798.42  1215728.95
21     0.59        0.00     301740.88     248321.14    53009.39         0.00  -603976.63
...
undiscounted totals per policy issued (KRW):
pols_if                   28.70
premiums            38202010.27
claims_death        50813891.72
claims_lapse         9284540.18
net_cf             -29799000.60

checks:
  policy count roll forward   True
  decrements sum to one       True
  account roll forward        True
  account prospective form    True
  surrender charge under cap  True
  suppression and the cliff   True
  policy loan roll forward    True
  acquisition cost under cap  True
  net cash flow ledger        True
```

`run.py` and everything it prints are pure ASCII, so the output survives a Windows console
under any code page: Korean is romanized and the currency is written `KRW`.

Three lines to the same thing, from Python:

```python
import modelx as mx
model = mx.read_model("products/whole_life/WholeLife_KR_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy year `t` with one column per cash flow
line, `pols_if` first and `net_cf` last; `expenses` there is acquisition plus maintenance,
with the claim handling expense in its own `claim_expenses` column. `result_pols()` and
`result_val()` publish the decrement run and the value run beside it — the second because on
this product the surrender value *is* the mechanic, and printing it only inside a cash flow
hides the one number the whole specification turns on.

## No maturity, no tail states, and a horizon that is the table's

Policy year `t` runs 1 … `proj_len()` = `omega_age() − age_at_entry() + 1`. A 종신 contract
has no expiry and pays nothing on survival [S1] [S2] [S3] [S4] [S6] [S8], so the horizon is
not the contract's — it is the terminal age of the shipped mortality table, **ω = 115** for
both sexes. Every remaining life dies in the final year, `pols_if(proj_len() + 1)` is zero,
and nothing is paid at the horizon but the death benefit. On the anchor cell the split is
**0.5081389172 deaths against 0.4918610828 lapses**, which is what `check_decrement_sum()`
asserts: every policy issued leaves by a modelled decrement and there is no residual
population anywhere.

The second structural fact is the one a term model does not have: **premiums stop at 납입완료
and nothing else does.** `premiums(t)` is zero from `prem_end() + 1`, and so is renewal
commission; maintenance expense, death claims, surrender benefits and the account all
continue for life. On the anchor cell the premium runs for 20 of 76 policy years and carries
₩38.2m of income against ₩60.1m of claims and ₩7.9m of expense and commission, so a
projection truncated at 납입완료 would miss most of the liability and all of its sign.
`Σ net_cf` over `t = 1 … 20` is **+₩27,935,040.25** and over `t = 21 … 76` is
**−₩57,734,040.85**.

Ages are **보험나이** (*boheom nai*, insurance age) throughout: the 만 나이 at the 계약일 with
a fraction under six months discarded and six months or more rounded up, incrementing on each
계약해당일 rather than on the birthday [REG-R25 제21조](#krlib-reg-r25). An annual grid stepped on
anniversaries therefore ages the contract correctly by construction. The public statistics the
shipped table is calibrated against are on **만나이** [REG-R38], no public mapping between the
two bases exists, and no conversion is applied **[std]** — so the table is read for a life
about half a year younger than the one being projected, on every row. That is a
one-directional bias and it is not corrected.

## One policy value, one multiplier

The account is the **계약자적립액**, a contractual quantity and not a 책임준비금. Under K-IFRS
제1117호 the insurer books no 보험료적립금 as a separate statutory reserve [REG-R60] [REG-R10],
which is the visible reason a 2024 상품요약서 writes 「계약자적립액에서 미상각신계약비를
공제한 금액」 where a pre-2023 one wrote 「순보험료식 책임준비금에서 해지공제액을 공제한
금액」 for the identical identity [S2] [S8]. `pol_val_pp` is that account and **this model
computes no reserve at all.**

It is solved forward on the net level recursion the specification states:

```
V(0) = 0
V(t) (1 − q) = ( V(t−1) + P·1{t ≤ m} ) (1 + i_acc) − q·SA
```

with `q = q(x + t − 1)` and `P` fixed at issue by `P·ä(x, m) = SA·A(x)` on the 예정이율.
`V(T)` is defined as zero: at the terminal age `q = 1` and the recursion degenerates.
감독규정 제7-65조제2항 is the permission that lets an annual grid carry a monthly-premium
product's account — 「연납보험료를 기준으로 하여 산출할 수 있다」 [REG-R18] — and
제7-66조제1항제4호's monthly-then-daily accrual convention renders as an image in the 고시 and
did not extract, so the annual step is a **[std]** approximation of it [REG-R19].
`check_pol_val_prosp()` asserts the substantive cross-check: the forward recursion and the
closed-form prospective value `SA·A(x+t) − P·ä(x+t, m−t)` agree at every duration, which they
do only if the net premium, the payment period and the discount basis are all consistent. On
the anchor the largest disagreement over 76 years is under ₩0.1.

Everything else in the model is that one value times one factor:

```
SC(t)  = 표준해약공제액 × max(0, 1 − t / n_sc),   n_sc = min(m, 7)
W(t)   = max(0, V(t) − SC(t))                     the 표준형 twin's 해약환급금
CV(t)  = k·W(t)  for t < m;  W(t)  for t ≥ m      the amount actually payable
```

The factor multiplies the **twin**, not the sold product's own account, and that is sourced
rather than assumed: every carrier selling a suppressed form names a comparison product in the
same sentence and says it is not sold — 「"표준형"의 경우는 … 동일한 보장내용으로
**해지율을 적용하지 않고** … 계산된 상품이며 … 비교안내를 위한 종목으로 **실제로 판매하지
않습니다**」 [S1], with the same sentence at three more carriers [S2] [S3] [S4]. So there is
one account run in this model, never two, and `CV(t)` is **independent of the sold form's own
premium**. That single fact is the whole of the 환급률 arithmetic the product is sold on: the
suppressed form's post-완납 value is identical to the 표준형's while its premiums are lower,
so its refund ratio is mechanically higher. On the shipped points the anchor's 환급률 crosses
100% at **duration 24** (1.002637, from 0.983271) and its 표준형 twin's at **duration 30**
(1.009492, from 0.991409), from the same account.

**The step at 납입완료 is a step.** `cv_pp(20) / cv_susp_pp(20)` is exactly **2.0** on the
anchor, `cv_pp` going from ₩24,143,647.50 at `t = 19` to ₩51,428,412.54 at `t = 20`. Anything
between is an interpolation the contract does not have. `check_cv_cliff()` asserts it,
together with the equality of the suppressed and 표준형 values from 납입완료 and the fact that
the payable value never exceeds the twin's.

That is the **value** test and deliberately not the **환급률** test. 감독규정
제7-66조제4항제2호나목 conditions the deepest designs on their post-완납 refund *ratio*
exceeding the greater of 100% and the 표준형's [REG-R19], while the FSC's own announcement of
the same amendment frames it the other way — 「전(全) 보험기간 동안 표준형 보험의 환급률
이내로」 [REG-R28]. On model point 3 the 무해지 form's post-완납 환급률 is **1.068759** against
the 표준형's **0.833632**: legal on the 고시 reading, and outside the press release's. Both
statements are recorded in `product-spec.md` as they stand and neither is asserted here.

**The step is not a surrender-charge effect.** 감독규정 제7-66조제1항제2호 caps the
해약공제기간 at seven years [REG-R19], so on the anchor's 20년납 contract `surr_chg_pp` is
already zero at `t = 7` — **thirteen years before the cliff**. `check_surr_chg_cap()` asserts
both bounds: the charge stays under the 표준해약공제액 of 별표 14 and is gone at `n_sc`.

On a **전기납** point (`prem_term = 0`) `prem_period()` is `proj_len()`, the suppressed period
runs for life and the step never happens. Model point 5 is written that way — `cv_mult(t)` is
0.50 at every duration — and is the one configuration in which the product's signature
mechanic is absent by construction.

## The surrender charge is bounded by a published schedule, and that is the whole defence

No Korean insurer publishes an expense rate. Both 상품요약서 in the source set define
계약체결비용 and 계약관리비용 and then give no number [S2] [S8], and the 산출방법서 that holds
the 예정사업비율 is a filed but unpublished 기초서류 [REG-R2]. What *is* public is a cap, and
it has no US or UK analogue at this level of prescription — 별표 14 [REG-R20]:

```
표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000
```

For a 보장성보험 the 해약공제계수 is the 보험기간 capped at 20 and the 연납순보험료 is
recomputed on a **20년납** footing where the 보험기간 is 20 years or more, which for a 종신
contract it always is. The formula therefore collapses to **one year's net premium plus one
per cent of the sum assured**, and `prem_net_20yr_pp()` exists solely to carry that
normalisation — a 7년납 point's cap is computed on the same footing as a 20년납 point's. On
the anchor the cap is **₩3,106,700.54**, of which ₩1,000,000 is the 보험가입금액 term. Two
cross-checks, neither used to fit it: the FSC states the same cap as 「보장성보험 월 보험료의
13배 수준」 [REG-R29], and 13 × ₩257,050 = ₩3,341,650, so the model sits **7.0% below** the
rule of thumb; and 별표 15 takes the 보험가입금액 entering the formula before any 체증 or 체감
[REG-R21].

The model then sets `acq_cost_pp()`, the 계약체결비용 actually incurred, **at the cap exactly**
**[std]**, which makes `surr_chg_pp(t)` literally the unamortised balance of it and closes the
loop between the expense the insurer incurs and the deduction the policyholder bears. Two
further published bounds are asserted by `check_acq_cost_cap()`: 계약체결비용 within **1.4 ×**
the 표준해약공제액, the tolerance under which a whole-life death-benefit 보장성보험 need not
publish a 계약체결비용지수 [REG-R22 제7-45조제11항](#krlib-reg-r22); and first-year remuneration within the
**first year's expected premium** [REG-R22 제4-32조제5항](#krlib-reg-r22), which binds on the long-payment-term
points where the premium is small against a cap computed on a 20년납 footing.

Only the **shape between the two ends** is standardized — a straight line to `n_sc` — the real
run-off living in the unpublished 산출방법서. That is the honest position: the cap is sourced
and exact, the level is set at the cap, and the shape is [std]. The visible consequence is the
calibration against the one published 표준형 grid at the identical cell: the model sits at
**0.889–0.911** of DB생명's printed 해지환급금 across durations 3 to 20 [S4], a level offset,
which is what setting 계약체결비용 *at* the statutory cap should produce against a real product
that presumably charges less.

## Lapse is behavioural, and the vector is the argument

**No 자동대출납입 was found in any Korean document read for this library.** `jplib`'s whole
life chassis turns on the 自動振替貸付, which advances the premium against the surrender value
at the end of grace so that lapse there is a *funded* event. In Korea, on the evidence
retrieved, there is no such test: a policyholder who misses a 14-day 납입최고기간 loses the
contract whatever its cash value, and on a 무해지 form receives nothing at all [S5 제25조]
[REG-R25 제26조](#krlib-reg-r25). That absence is **[unverified]** rather than established — the 생명보험
표준약관 is understood to contain such an article and the retrieved 별표 15 extract does not
carry it — and it is the single highest-value item for a later research pass, because finding
one would change this chassis in kind rather than in degree.

So lapse is a plain decrement, and which vector it runs on is a supervisory question.
`lapse_table.csv` holds two bases as three parameters each, rather than a rate per policy
year, because the convergence point is 납입완료 and that is a model point attribute:

| basis | first year | at 납입완료 | ultimate | provenance |
|---|---|---|---|---|
| `loglinear` | 10.0% | 0.1% | 0.8% | the FSS **원칙모형** [REG-R27] |
| `flat` | 4.0% | 4.0% | 4.0% | the level comparison basis **[std]** |

The `loglinear` basis is the log-linear model the November 2024 계리가정 decision adopts as the
원칙모형, with its practical convergence point of 0.1% at 납입완료 and its 0.8% ultimate rate
[REG-R27] [R3]. The 10% start is the top of the 연 1%~10% 적용해지율 envelope one carrier
discloses in its 상품요약서 [S2] and sits inside the 연 0%~13.4% one at another [S8]. **The
shape between the two ends is [std]**; no Korean lapse curve by duration is public, and the two
disclosed bases — a *pricing* 적용해지율 and a *valuation* assumption — serve different
purposes and cannot be reconciled from public data. This is the largest single assumption gap
on this product.

The two bases are shipped side by side because that comparison *is* the disclosure the guidance
obliges, not an afterthought. It is also what makes the cliff legible. **The cliff moves less
cash than a reader expects on the 원칙모형, and that is the point**: the payable value doubles
at `t = 20`, but the lapse rate that year is 0.1%, so almost nobody is there to be paid the
step —

| basis | `claims_lapse(19)` | `claims_lapse(20)` | `net_cf(20)` | `Σ claims_death` | `Σ net_cf` |
|---|---|---|---|---|---|
| `loglinear` | ₩18,419.29 | ₩30,608.06 | ₩1,215,728.95 | ₩50,813,891.72 | −₩29,799,000.60 |
| `flat` | ₩444,737.31 | ₩905,221.12 | ₩16,276.98 | ₩18,032,089.04 | −₩10,210,977.48 |

— while on the level basis the same step produces a visible one-year hole, a 98.7% collapse in
`net_cf(20)` in a single row. The surrender outgo on the 원칙모형 arrives in the year *after*
the cliff, when the rate returns to 0.8% against a value that has doubled: ₩248,321.14 at
`t = 21`. The `flat` run's undiscounted total looks **better**, and that is a trap rather than
a finding: a 4% lapse rate empties the book before the expensive years, so expected death
claims fall by 64.5%, and the sign reverses once the 환급률 exceeds 1 — which is exactly why
the K-ICS 대량해지위험 shock splits by whether surrender reduces or increases net assets
[REG-R36] [R7].

## 보험계약대출, and every payment floored at zero

The loan is a modelled state: `L(t+1) = (L(t) + D(t))·(1 + i_L)`, compound, with interest
capitalised into principal and **no repayment modelled [std]** — repayment is permitted at any
time without fee and no Korean repayment statistic is public. The rate is
`acc_int_rate() + 1.5%`, which is 예정이율 + 1.5% on a 금리확정형 contract and 공시이율 + 1.5%
on a 금리연동형 one, stated at three carriers independently [S9] [S11] [S13]. It is a
**vintage** rate: because the base is the contract's own 예정이율, a policy written in a
high-rate era carries a high loan rate for life, and one carrier's live published range spans
연 3.5%~10.5% across its in-force book under a 최고 적용 대출이율 of 9.90% [S11] [S12].

The limit is **80% of the payable 해약환급금** — the observed range is 50%–85% at one carrier
and 50%–80% at another, and the composite takes 80% [S5 제34조] [S11] [S13]. That it is a
fraction of the *payable* value and not of `W(t)` is the whole demonstration. Model point 6
draws the contractual maximum at the tenth anniversary of a 저해지 contract and gets
**₩8,167,325.83**, half what the same election on the 표준형 twin would produce; model point 3
makes the identical election on a **무해지** contract and draws **exactly nothing**, because
during 납입기간 there is no value to lend against — the point the FSS made in terms in its 2019
소비자경보 and the 표준약관 repeats [REG-R28] [R4] [REG-R25 제33조](#krlib-reg-r25).

Korea has no equivalent of the Japanese loan-excess lapse notice: the deduction is automatic
and termination is driven by the demand period, not by the balance [S5 제34조]. So a balance
that outgrows the value does not terminate anything — it simply floors the payment at zero, and
on model point 6 it does: by `t = 76` the balance is **₩108,712,698.33** against a sum assured
of ₩100,000,000, and both the death benefit and the surrender benefit are zero. Every payment
in `claims()` is floored for that reason, and `check_loan_roll_fwd()` asserts the accumulation
in both directions — non-trivially on point 6, and as a statement that zero stays zero on
point 3.

## 보험료 납입면제 is a state, not a rate adjustment

Korea puts **no severe-disability acceleration** on this chassis. The slot Japanese whole life
fills with a 高度障害保険金 at the sum assured is filled here by the premium waiver, which
stops the premiums and *continues* the contract [S2] [S3] [S6] [S8]. The trigger is a **50%
장해지급률** aggregated across body parts from one cause, accident or disease alike, on the
장해분류표 of 생명보험 표준약관 부표 3 [REG-R25].

What makes it a modelling problem is the deemed-paid rule: 「보험료가 보험료 납입기간
종료일까지 … 정상적으로 납입된 것으로 하여 사망보험금 및 해지환급금을 계산합니다」 [S2] [S3]
[S8]. A waived policy therefore accrues surrender value on the full premium scale while paying
nothing — and on a suppressed form it is **the only route to the cliff that the policyholder
does not have to fund**, which makes the waiver a genuine option with value rather than a
protection feature. So it is a distinct in-force state with its own persistency: `pols_waived`
carries no premium income, full benefit outgo, full account accrual and the ordinary
decrements. Carrying the same lapse rate as the paying cohort is **[std]** — no Korean
statistic distinguishes them. Model point 7 runs it at 0.4% a year and reaches **0.042858** of
the surviving book waived by `t = 20`.

The wiring detail worth stating, because it is invisible in the base run: `premiums(t)` is
weighted by `pols_pay_exp(t)` and every other line by the whole in-force count. The two are
equal wherever `waiver_rate` is zero, so an implementation that weights premium by `pols_if(t)`
reproduces the worked example exactly and fails only once the module is switched on.

## Modules that are off in the base run

Six constructions are implemented and switched off, so that the base run reproduces the worked
example while the machinery stays visible and testable. Each is a **model point column**, so
the base run and the module run are the same model and the suppressed form sits beside the
ordinary one in one projection.

| Module | Switch | Off value | Exercised on | Signature number |
|---|---|---|---|---|
| 보험계약대출 | `loan_util` | `0.0` | points 3, 6 | `loan_draw(10)` = ₩8,167,325.83 on 저해지; **₩0.00** on 무해지 |
| 보험료 납입면제 | `waiver_rate` | `0.0` | point 7 | `pols_waived(20)` = 0.042858 at 0.4% p.a. |
| 유지보너스 | `bonus_rate` | `0.0` | point 8 | `lapse_rate(7)` = **0.301** against a base of 0.001 |
| 금리연동형 crediting | `int_basis` | `fixed` | point 9 | `pol_val_pp(20)` **9.38%** above its prospective form |
| 감액 | `reduce_year` | `0` | point 10 | `claims_reduction(15)` = ₩163,333,687.53 |
| 부활 | `reinstate_rate` | `0.0` | point 10 | a reinstated lapse is paid **no** surrender value |

Four of them need a sentence of their own.

**유지보너스** is a 7년납 단기납 design crediting **13.8%** of total premiums to the
계약자적립액 at 납입완료 [S7], which lifts the 환급률 at 완납 to 0.962906. Switching it on
switches `lapse_spike()` on with it: the supervisor requires an **additional lapse of at least
30%** at any bonus date [REG-R27], so the point's `lapse_rate(7)` is 0.301 against a base of
0.001. Turning the bonus on without the spike would misstate the liability in the insurer's
favour, which is exactly what the guidance exists to prevent, and the two are wired together so
they cannot be separated by accident.

**금리연동형 crediting** puts the account on a declared 공시이율 floored at a **최저보증이율
of 연복리 0.75%** [S5] while the net premium stays on the 예정이율 fixed at issue, so the
account is genuinely path-dependent and runs 9.38% ahead of its prospective form by `t = 20`.
`check_pol_val_prosp()` is **defined as zero** there rather than asserted, because the identity
is not a property of that contract. Asserting it unconditionally fails; discounting the account
on the pricing rate to make it pass would silently change the product.

**감액** treats the reduced portion as **surrendered** and pays the corresponding 해약환급금 on
the basis applying at that duration [S5 제20조] — so a reduction made during 납입기간 pays at
`k W(t)` and pays nothing at all on a 무해지 contract. The sum assured, the premium, the
account and the surrender charge all restate pro rata through a single `sa_factor(t)`, which is
**exact** here rather than an approximation because every one of them is proportional to the
보험가입금액. The reduction anniversary is the one year `check_pol_val_roll_fwd()` cannot
close, because the value is re-based by the election rather than rolled forward — so the
residual is taken on `pol_val_base_pp`, the unreduced path, and the scaling is asserted
separately by the ledger.

**부활** returns 20% of one year's lapses to the paying cohort a year later **[std]**. The
substantive effect is that a reinstated lapse is **not paid a surrender value**: 부활 requires
that the 해약환급금 has not been drawn, and the 약관's parenthesis expressly includes the case
where there was none — 「해지환급금이 없는 경우를 포함」 — so a 무해지 contract is always
reinstatable within three years [S5 제26조] [REG-R25 제27조](#krlib-reg-r25). No arrears cash flow arises on
the annual grid because no premium instalment falls inside a one-year gap **[std]**.

`mort_be_factor` is the last lever, 1.00 on every point but 10. At 1.00 the base run is a
**pricing-table run, not a best estimate**: the shipped table is calibrated toward an insured
level and no retrieved source sizes the margin a Korean carrier's 적용위험률 carries against
its own experience. Claims move proportionately with it; the terminal rate is held at 1
whatever it is set to, because `omega_age` is the horizon of the table and not an
experience assumption.

Two things are deliberately **not** modelled and are named so a reader does not assume them.
**감액완납 and 연장정기보험** appear in no retrieved Korean document — neither in the only full
약관 in the set nor in any 상품요약서 [S5] — and are **[unverified]** rather than established;
a reader arriving from `jplib`, where 払済保険 and 延長定期保険 are both in the 約款, will
reach for them and should not. And the **해약환급금준비금**, the IFRS 17 CSM and the K-ICS
요구자본 consume `result_cf()` rather than living inside it.

## Inputs are external files

### Read once, in `Data`

Three CSVs live in this directory, beside `run.py`, and the model folder holds nothing but
formulas — no `_data/`, no IOSpec, no embedded values. This follows `annuallife.TradLife_A`;
contrast `basiclife.BasicTerm_S`, which stores its inputs inside the model. The consequence
worth knowing is that **the model is not portable on its own**: copying `WholeLife_KR_A/`
without its parent's CSVs produces a model that reads and then fails on first evaluation.

Every reader and every `*_file` Reference lives in `Data`, which takes no parameters, so each
file is read **once per model** rather than once per model point. `Projection` is parameterized
by `point_id` and every `Projection[N]` is a separate ItemSpace with its own cells cache; a
reader placed there would re-read every file for every policy.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `data.model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `data.mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `data.lapse_table()` | `lapse_table.csv` |

`input_dir()` returns `_model.path.parent`, resolved at run time from wherever the model was
read, so the model works from any checkout and from a copy made by `lifelib.create()`. Every
row of the two assumption files carries a `provenance` cell beginning with a citation tag,
which is a property of this library rather than a habit, and the conventions suite asserts it.

### `model_point_table.csv` — ten points, and the anchor is sourced

Twenty columns, indexed by `point_id`. Point 1 is 남자, 보험나이 40세, 보험가입금액 1억원,
종신, 20년납, 저해지환급형 `k = 0.50` — the technical notes' worked-example anchor cell, and
the cell Korean industry comparison disclosure itself uses (1억원 / 종신 / 20년납 / 월납)
[S17]. Its annual premium of **₩2,776,140** is `0.900 ×` the 표준형 twin's ₩3,084,600
**[std]** [S1], and ₩3,084,600 is 12 × the published ₩257,050 monthly rate for exactly that
cell [S4]. That twin is `point_id = 2`, and the two run side by side throughout the notes.

The other nine take their premiums from the same rule and cover both sexes, issue ages 30 to
65, sum assureds ₩10,000,000 to ₩1,000,000,000 (1,000만원 ~ 10억원), the four suppression
factors 1.00 / 0.50 / 0.30 / 0.00, payment terms of 7, 10, 20 and 30 years and 전기납, and each
optional module. No modal discount is applied to the annualisation **[std]**: no carrier
publishes an annual scale, so 12 × the monthly premium slightly overstates the annual one.

### `mort_table.csv` — a [std] construction, and it must never be called the 경험생명표

202 rows, `sex` × attained 보험나이 15 … 115, with `mort_rate` and `provenance`. The **제10회
경험생명표** is not published in full — what is released is the 평균수명 and the 기대여명, and
even those reached this library through a trade newspaper [REG-R33] [REG-R34] — so unlike
`jplib`, where the 生保標準生命表 is free to read and only its redistribution is restricted,
there is **no published Korean insured rate to anchor a proxy on**. The file is built in three
parts and every row says which it is:

- **ANCHOR** rows at 보험나이 20, 40 and 60 take the mean of the only two Korean insured
  mortality rates in the public domain at those ages, the sample 적용위험률 grids that 하나생명
  [S2] and KDB생명 [S8] print in their 상품요약서 — `q(40) = 0.00085` is the mean of 0.000780
  and 0.00092, `q(60) = 0.005075` the mean of 0.004550 and 0.00560. The two rates are sourced;
  taking their mean is the standardization. They differ by **10%–23%** at every age and sex, so
  they bracket rather than fix a level.
- **CONSTRUCTED** rows below 60 are log-linear in `ln q` between those anchors and extrapolated
  below age 20 on the same slope; above 60 they follow a Gompertz in `ln q` with a quadratic
  deceleration term whose two parameters are solved so that the table's 65세 기대여명 is 23.7
  years (male) and 27.1 (female) — the 국가데이터처 완전생명표 figures of 19.5 and 23.7
  [REG-R38] plus the gap to the reported 제10회 figures [REG-R33] — and so that `q` reaches 1
  at ω = 115.
- The **TERMINAL** row sets `q = 1` at ω = 115, which closes the table. The 제10회 terminal age
  is not public either.

Two checks on the construction were not used to fit it and are worth recording. The resulting
평균수명 at birth is **85.4 years (male)** and **90.4 (female)** against the 86.3 and 90.7
reported for the 제10회 [REG-R33]. And the model's own 표준형 surrender values sit at a
consistent **0.889–0.911** of the fullest published grid at the same cell across durations 3 to
20 [S4] — a level offset rather than a shape error, reported duration by duration in
`technical-notes.md`. **No row of this file is a 경험생명표 value.** A user with a real
산출방법서 replaces `mort_table.csv` with a same-schema file and changes no formula.

### `lapse_table.csv` — two bases, three parameters each, and no rate per duration

Two rows, indexed by `lapse_basis`, with `first_year_rate`, `completion_rate`,
`ultimate_rate` and `provenance`. The columns are parameters rather than a rate per policy year
because the convergence point is 납입완료 and that differs by model point: a 7년납 contract
converges at `t = 7` and a 30년납 one at `t = 30`, on the same two rows. The `loglinear` row's
endpoints are the supervisor's [REG-R27] [R3] and its first-year rate the top of a disclosed
pricing envelope [S2] [S8]; the shape between them is [std]. The `flat` row is [std] end to
end, level because the 표준형 comparison twin is priced with no lapse assumption at all [S1].

Expense, commission and interest levels are `Projection` References rather than a fourth table,
because each is a single scalar: `prem_int_rate` 2.50%, `min_guar_rate` 0.75%, `prem_loading`
1.4642, `acq_cost_ratio` 1.00, `comm_init_share` 0.65, `comm_renewal_rate` 3.0%,
`expense_maint_pp` ₩60,000, `expense_maint_prem_rate` 2.0%, `expense_claim_pp` ₩300,000,
`inflation_rate` 2.0%, `loan_spread` 1.5%, `loan_limit` 0.80, `lapse_bonus_spike` 0.30, and the
five 별표 14 parameters `surr_chg_prem_rate` 5%, `surr_chg_coef` 20, `surr_chg_sa_rate` 1%,
`surr_chg_prem_years` 20 and `surr_chg_max_years` 7.

## Sign convention

`net_cf` is **income positive** — premiums less claims, expenses and commission — which is both
the specification's own sign and the library-wide one, so there is no outgo-positive
`liability_cf` companion to publish: one stream, one sign, one name.

That the published statement adds up is `check_net_cf()`, with the per-`t` signed residual at
`check_net_cf_resid(t)` — the library-wide name for this check on every model. **The identity
is `net_cf(t) = premiums(t) − claims_death(t) − claims_lapse(t) − claims_reduction(t) −
claim_expenses(t) − expenses(t) − commissions(t)`**, that is, every non-`pols_if` column of
`result_cf()` on row `t` sums to that row's `net_cf`. So a fourth benefit kind added to
`claims()` and left out of the statement shows up here rather than vanishing from it.
`result_cf()` publishes `claims_death`, `claims_lapse` and `claims_reduction` and **no bare
`claims` column**, which is what makes the columns sum with nothing to skip; the
`claims(t, kind)` cells stays, and `claims(t)` with `kind` omitted is their total.

On the anchor cell the undiscounted total is **−₩29,799,000.60** per policy issued, which is
the expected shape and not a defect: expected death claims of ₩50.81m plus surrender benefits
of ₩9.28m come to ₩60.10m of benefit against ₩38.20m of premium, and everything that closes
that gap — discounting, the investment return on the account, the CSM — belongs to a layer this
model deliberately stops before.

## Naming

Cells names follow lifelib's `basiclife.BasicTerm_S` and `savings.CashValue_SE` wherever those
models have an analogue: `pols_*` for policy counts, plural nouns for cash flows, `*_rate` for
rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind` string,
`pols_if_at(t, timing)` for the within-year in-force reads. This is a contractual account and a
surrender value, so it is `pol_val_pp` and `cv_pp`; there is no `av_pp` anywhere, and no
`reserve_pp`, because the model computes no reserve. `lapse_rate` is the annual rate, as on
every annual-grid model in the library.

The technical notes use compact actuarial symbols and the `Projection` Space docstring carries
the full symbol-to-cells map. Five cases needed care, and three of them were settled by the
cross-model review:

| Notes | Cells | Why |
|---|---|---|
| `SC(t)`, cap | `surr_chg_pp` / `surr_chg_cap_pp` | The first is the 해약공제액 and the second the **표준해약공제액** that bounds it. `surr_charge_pp` was retired for the first; the second is a Korean quantity with no analogue in any sister library, and the `_cap_` in the middle is what tells a reader which of the two they are looking at |
| `k`, 환급률 | `cv_floor_ratio` / `refund_ratio` | The bare `cv_ratio` was retired because this chassis carries two ratios on the same object — the suppression factor and the 환급률 — and a name that does not say which is a bug waiting to be written |
| `i`, declared | `prem_int_rate` / `decl_rate` | The 예정이율 and the 공시이율. A romanized `yejeong_rate` / `gongsi_rate` pair reads as two exotic quantities when the second is the same object `delib` already spelled `decl_rate` for the laufende Verzinsung |
| `V(t)`, `W(t)`, `k W(t)` | `pol_val_pp` / `cv_std_pp` / `cv_susp_pp` | Three names for one account and one multiplier. `cv_std_pp` is the **표준형 twin's** value and `cv_susp_pp` the suppressed one at *every* duration, so both exist at `t = m` and the step can be read off one table rather than inferred |
| `m` | `prem_term` / `prem_period` / `prem_end` | `prem_term` is the model point column, with **0 denoting 전기납**; `prem_period` is the effective number of years, `proj_len()` on a 전기납 contract; `prem_end` is the last year a premium is actually due |

`pol_val_base_pp` is the fifth name a reader will ask about: it is the account on the
**unreduced** path, which exists only so that `check_pol_val_roll_fwd()` has something to roll
forward across a 감액 anniversary, where `pol_val_pp` is re-based by the election.

## Standardizations used

Every one of these is a **[std]** choice, and each is stated in the cells docstring that uses
it. Where the research pass established an observed range across insurers, it is given.

| Parameter | Value | Basis for the choice | Observed range |
|---|---|---|---|
| 예정이율 `prem_int_rate` | 2.50% | centre of the band read from six carrier documents; equals the 2026 평균공시이율 [REG-R48] | 2.25%–2.75% [S1] [S2] [S5] [S6] [S7] [S8] |
| 최저보증이율 `min_guar_rate` | 0.75% | stated verbatim in the one full 약관 retrieved [S5] | one observation |
| Mortality table | ω = 115, e(65) = 23.7 / 27.1 | anchors [S2] [S8]; calibration [REG-R38] [REG-R33] | the two anchors differ by 10%–23% |
| Lapse `loglinear` | 10% → 0.1% at 납입완료, 0.8% after | endpoints [REG-R27]; first year from a disclosed pricing envelope [S2] | 연 1%~10% [S2]; 연 0%~13.4% [S8] |
| Lapse `flat` | 4.0% | inside both disclosed envelopes | as above |
| Bonus-date lapse spike | +30 pp | 「30% 이상」 required at a bonus date [REG-R27] | one instrument |
| Premium loading `prem_loading` | 1.4642 | calibrated once so the 표준형 anchor reproduces 12 × ₩257,050 [S4] | fits to 0.0010% |
| 계약체결비용 `acq_cost_ratio` | 1.00 × 표준해약공제액 | at the cap, inside the 1.4 × tolerance [REG-R22] | no carrier publishes one |
| Commission share `comm_init_share` | 0.65 of 계약체결비용 | capped at the first year's premium [REG-R22 제4-32조제5항](#krlib-reg-r22) | no scale is public |
| Renewal commission | 3.0% of premium | as above; paid only to 납입완료 | no scale is public |
| 계약관리비용 | ₩60,000 p.a. + 2.0% of premium | no Korean expense rate is public [S2] [S5] [S8] [REG-R2] | none |
| Claim expense | ₩300,000 per claim | as above, uninflated | none |
| Expense inflation | 2.0% p.a. | the Bank of Korea target; compounds to 4.42 over 76 years | none |
| Policy loan limit | 80% of the payable 해약환급금 | top of the narrower published range | 50%–85% [S11]; 50%–80% [S13] |
| Policy loan repayment | none modelled | permitted at any time without fee; no statistic is public | none |
| Surrender-charge shape | straight line to `n_sc` | the cap and the period are sourced and exact; only the shape is [std] | none |
| Suppression factor `k` | model point column | the market runs all four values | 0.00 / 0.30 / 0.50 / 1.00 [S1] [S4] [S6] [S7] [S8] |
| Cliff date | 납입완료 | three of five observed designs | also 7년 [S2] and 납입기간+3년 [S3] |
| Waiver persistency | same lapse rate as the paying cohort | no Korean statistic distinguishes them | none |
| 부활 lag and rate | one year, 20% | no Korean reinstatement statistic is public | none |
| Annual mode | 12 × the monthly premium | no carrier publishes an annual scale, so no modal discount is applied — the annual premium is slightly overstated | none |
| Age basis | 보험나이 read against a 만나이-calibrated table | no public mapping exists between the two [REG-R38] | none |

**Where the cliff falls is the standardization a reader is most likely to need to change.** The
composite hard-codes 납입완료, which three of the five observed designs use; a model
reproducing [S2] or [S3] must expose that date as a parameter of its own, because on those
contracts the step is at seven years and at 납입기간 + 3년 respectively, neither of
which is 납입완료.

## Tests

`tests/test_model_conventions_kr.py` runs the house style over this model with every other in
the library: the two-Space layout and the model folder holding formulas only, `input_dir()`
resolving to the parent, every CSV beside the model actually read by a `*_file` Reference,
the provenance tag on every assumption row, a docstring on every Space and every single cells,
the model docstring's house disclaimers, the `Projection` docstring's symbol map and its
statement of the age basis, the `Data` docstring naming `TradLife_A`, `lower_snake_case` cells
names and the shared retired-name register, `lapse_rate` as the annual rate, the `result_cf()`
column vocabulary and its `net_cf` column, `net_cf` income-positive, `pols_if` as a
start-of-period count, `check_net_cf()` published and `True`, every model point in the shipped
table projecting without raising, the inputs read **once per model** rather than once per model
point, and a `read → write → re-read` round trip reproducing the same file set and the same
numbers.

`tests/test_whole_life_kr.py` asserts what is specific to this product. The notes' worked
example is held **hard-coded as a module-level table** — the cash-flow rows, the
surrender-value rows, the derived scalars, the undiscounted totals and the decrement split — so
a reviewer can lay it beside `technical-notes.md` and compare by eye. Money is asserted to
two decimal places of the won, in-force to six decimals and the decrement totals to ten,
which is the precision the notes display.

Beyond the worked example, every entry in the notes' **Known modeling pitfalls** list has a
test named after it, because each is a way an implementation can look right and be wrong:

- the cliff as a step and not a ramp, `cv_pp(20) / cv_susp_pp(20)` exactly `1 / k = 2.0`, and
  its **absence** on the 전기납 point where `cv_mult(t)` is `k` for life;
- the surrender in policy year `m` paid on the **full** value, with both values published at
  the boundary;
- one account and one multiplier — points 1 and 2 reaching the identical `pol_val_pp` from
  different premiums, and the 환급률 crossing 100% at duration 24 against 30;
- the step not being a surrender-charge effect: `surr_chg_pp(7) = 0`, thirteen years early;
- `P` and `P₂₀` as different annuities, tested on the 7년납 and 10년납 points where they do
  **not** coincide, since a test run only on the anchor cannot see the difference;
- premiums stopping at `m` where nothing else does, with `net_cf` swinging by ₩1,819,705.57
  across `t = 20 → 21` and negative in all 56 remaining years;
- the nil surrender value of the 무해지 form through the whole of 납입기간 and the
  **exactly zero** policy loan that follows from it at `loan_util = 1.0`;
- every payment floored at zero, on point 6 where the loan balance exceeds the sum assured;
- the 30-point lapse spike at the 유지보너스 date, and that the bonus cannot be switched on
  without it;
- the prospective identity withdrawn rather than forced on the 금리연동형 point;
- `pol_val_pp` never appearing in `net_cf` and never being read as a reserve;
- waived premiums counted as paid, and the waiver as a state rather than a rate adjustment;
- lapse behavioural rather than funded — no APL machinery imported from `jplib`;
- the pro-rata restate after a 감액, and the 부활 that is paid no surrender value.

Beyond those: all nine `check_*()` identities on all ten model points, the roll-forward and
decrement-sum identities rebuilt independently of the recursions, each optional module in
**both** positions, the CSVs' encoding and the mortality table's row-by-row provenance, an
input swapped by repointing a filename Reference, and the calibration band against the
published 표준형 grid [S4].

```bash
python -m pytest lifelib/libraries/krlib/tests/test_whole_life_kr.py -q
python -m pytest lifelib/libraries/krlib/tests/test_model_conventions_kr.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #krlib-whole_life-r3
[R4]: #krlib-whole_life-r4
[R7]: #krlib-whole_life-r7
[REG-R10]: #krlib-reg-r10
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R48]: #krlib-reg-r48
[REG-R60]: #krlib-reg-r60
<!-- END generated citation links -->
