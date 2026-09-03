# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes derive is specified in [`product-spec.md`](product-spec.md), and every
source tag on this page resolves in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced: the split of the single premium into 보장계약 보험료,
> 사업비 and the 연금계약 순보험료 that becomes the opening 계약자적립액
> [R1 §1-가](#krlib-immediate_annuity-r1) [S1 주2]; the accumulation recursion at Max[공시이율, 최저보증이율]
> [R2 §1](#krlib-immediate_annuity-r2) [S7 제7조]; the 만기보험금 지급재원 and its decomposition into interest less a
> retention [R1] [R2 §1](#krlib-immediate_annuity-r2); the 사망보험금 of 10% of the single premium plus the
> 계약자적립액 [S1] [S3] [R1 별표1](#krlib-immediate_annuity-r1); the 해약공제액 of nil at every duration
> [S1 §VIII] [S10]; the prohibition on surrendering a 종신연금형 in payment
> [S3] [S5 주2] [S7 제31조]; and the 보증지급기간's effect, which is that the payment
> obligation survives the annuitant [S1 주5] [S3]. Every **rate** is a **[std]**
> standardization. The 제10회 경험생명표 is produced by 보험개발원 and is **not
> published** [REG-R33] [REG-R34], so `mort_table.csv` is a constructed proxy and must
> never be presented as it. The 공시이율 is a scalar because 감독규정 제7-65조제3항 makes
> it the product of a 공시기준이율 majority-weighted to the insurer's own 운용자산이익률
> [REG-R18] [REG-R24], which no model in this library can derive. Replace the whole basis
> with a filed one before drawing any conclusion from the numbers.

## Run it

```bash
python products/immediate_annuity/run.py       # model point 1, the anchor
python products/immediate_annuity/run.py 6     # 상속연금형, retention as designed
python products/immediate_annuity/run.py 7     # the same contract, retention as ordered
python products/immediate_annuity/run.py 8     # the floor stepping, on a 20-year term
python products/immediate_annuity/run.py 9     # 확정기간연금형, ten years
```

`run.py` prints the model point, the derived quantities at inception, seventeen sampled
rows of the cash flow statement, the undiscounted totals and the eleven `check_*()`
identities. Everything it prints is ASCII, so the output lands on a Windows console under
any code page: amounts are labelled `KRW`, and the product, the three payout shapes and
the age basis are romanized (Revised Romanization). Real output for the anchor, with the
seventeen-row statement elided — it is reproduced in full in
[`technical-notes.md`](technical-notes.md):

```text
Immediate_KR_A - jeuksi yeongeum (Korean single-premium immediate annuity)
model point 1: IA-000001 - jongsin yeongeum-hyeong (life annuity)
annuitant M boheom nai 60 (insurance age)   single premium KRW 100,000,000 (10,000 manwon)
bojeung jigeup gigan (guaranteed period) = 10 years   lapse 0.00%
crediting basis decl_2017: gongsi iyul 2.50%, choejeo bojeung iyul 1.25% to 0.75% -> credited 2.50% at t = 0 and 2.50% at t = 50
expense load 3.50% + wiheom boheomnyo 0.00% -> opening gyeyakja jeongnimaek KRW 96,500,000 (96.50% of premium)
annuity factor 19.5027 -> yeongeum yeonaek KRW 4,948,039 a year (KRW 412,337 a month equivalent)
projection runs t = 0 .. 50 (annual, in arrears; row t pays at t + 1)

Cash flow statement (KRW, income positive in net_cf)
    [ seventeen sampled rows of result_cf(), ten columns, t = 0 .. 50 ]

undiscounted totals over t = 0 .. 50:
    premiums                 100,000,000.00
    annuity_payments         138,160,059.32
    claims_death                       0.00
    claims_lapse                       0.00
    claims_maturity                    0.00
    commissions                2,000,000.00
    expenses                   2,605,280.47
    net_cf                   -42,765,339.80

checks
    check_annuity_basis        True
    check_av_roll_fwd          True
    check_av_terminal          True
    check_guarantee_certain    True
    check_lives_roll_fwd       True
    check_net_cf               True
    check_payment_factor       True
    check_pols_roll_fwd        True
    check_premium_split        True
    check_rate_level           True
    check_surr_value           True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/immediate_annuity/Immediate_KR_A")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[6].result_pols()    # the fund, the annuity, the retention, the decrements
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor.
`result_cf()` returns a `DataFrame` indexed by policy year `t`, one column per cash flow
line, with `pols_if` first and both signs of the net flow published. `result_pols()` is
its companion — everything the statement is built out of and nothing that is itself a cash
flow — and it is the frame in which the retention becomes legible, because `annuity_pp`,
`retention_pp` and `av_pp` sit in adjacent columns. `model.Projection.doc` carries the
notes' symbols mapped to the cells names and states the age basis; `model.Data.doc` says
what each input file is and, for the mortality table, what it is **not**.

## The payout phase standing alone: no premium term, no strain

`Immediate_KR_A` is the library's payout-phase chassis and `Pension_KR_A` is the
accumulation half of the same machinery. A single premium is paid at inception, the whole
load and — on the shapes that keep a death benefit — the whole 위험보험료 are deducted
once, and the residue becomes the opening 계약자적립액. Three consequences run through
every formula in the model:

- **There is no premium term.** 표준약관 제26조's 납입최고 and 제27조's 부활 both
  presuppose a renewal premium that can go unpaid [REG-R25], so neither can operate and
  neither is modelled. `premiums(t)` is the single premium at `t = 0` and zero thereafter.
  The premium is projected as genuine income rather than netted away, because that is what
  makes the next point a property of the printed statement instead of a claim in prose.
- **There is no acquisition strain.** `comm_rate` (2.00%) sits below `acq_charge_rate`
  (2.20%) [S1 §VII] [S1 §VIII], and `acq_expense_rate` is the **[std]** derived residue —
  the 3.50% load less the 2.00% commission — so the charge taken from the fund at
  inception exactly meets the outgo at inception. `check_premium_split()` asserts it:
  `P = commission + expense + 위험보험료 + V(0)`, with nothing left over in either
  direction. There is no deferred acquisition cost to amortise anywhere in this model, and
  no unearned premium to add back on surrender [REG-R19 제7-66조제5항](#krlib-reg-r19).
- **The only decrements are mortality and, on two of the three shapes, surrender.** On the
  종신연금형 surrender is contractually impossible from month one [S7 제31조], and
  `check_surr_value()` asserts that the shipped life-shape model points carry a nil rate
  **and** a nil 해약환급금 rather than leaving it to the table.

## Three shapes, three liabilities, and only one reads the table

The payout shape is a model point column, not a rider, because the three are not variants
of one design. `shape` takes `life`, `inheritance` or `certain`:

| `shape` | Korean | `annuity_pp(t)` | Mortality in the annuity? |
|---|---|---|---|
| `life` | 종신연금형 | `V(0) / ae(x, g, i)`, struck once at commencement | **Yes** |
| `inheritance` | 상속연금형 만기형 | `V(t) i(t) − R(t)`, recomputed each year | No |
| `certain` | 확정기간연금형 | `V(t) / a(n − t, i(t))`, recomputed each year | No |

「옵션 중 사망(생존) 위험률이 적용되는 것은 종신형에 한정된다 … 확정형과 상속형은
사망률을 사용하지 않는다」 [R12 §III-1](#krlib-immediate_annuity-r12). `annuity_factor()` is therefore defined on the
life shape alone and **raises** on the other two, so the distinction cannot be lost by
accident. Mortality still enters the *projection* of the other two shapes, because both
pay a death benefit; a decrement and a pricing basis are two different uses of one table
and the model keeps them apart — `payment_factor()` and `pricing_factor()` are written as
two constructions rather than one calling the other, so that `check_annuity_basis()`
compares two things instead of comparing one with itself.

The life annuity is struck **once**. 「연금개시시의 계약자적립액을 기준으로 … 산출」
[S7 별표1] fixes it on the fund at commencement, and the annuitant-mortality ratchet every
carrier carries is inert on an 즉시연금, because there is no interval between issue and
annuitisation for a table revision to land in — [S6 §10-라] confines it expressly to the
거치형. So this model needs no ratchet logic and the deferred sibling does.
`check_rate_level()` holds the life shape to the level rate that reading assumes: the
representative declared rate of 2.50% is above every step of the floor, so the condition
holds on every shipped life-shape point, and a point that broke it would fail rather than
be projected on a basis the model never priced. The other two shapes recompute annually
and carry a stepping rate correctly, which model point 8 exercises.

## `pols_if` is the probability that a payment obligation remains

It is the technical notes' `IF(t)`, and on this product that is not the probability that
the annuitant is alive. The `pols_if` docstring says so in those words, and the
conventions suite reads that phrase to exempt the model from the start-of-period
policy-count assertion — an exemption a model earns by documenting itself, not by being
added to a list.

- **life** — `max(l(t), 1{t < g})`. Within the 보증지급기간 the instalments are due whether
  or not the annuitant lives — 「보증지급기간안에 사망시에는 잔여보증지급기간 동안,
  미지급된 연금월액을 매월 연금지급일에 드립니다」 [S3] [S1 주5] — so the obligation is
  the *greater* of the two and not their sum. An additive construction would pay
  `1 + l(t)` for the whole guaranteed term; on the anchor it gives a factor of 28.061177
  against the correct 19.502675, an annuity 30.5% too low, for life.
- **certain** — the persistency measure alone; death does not accelerate the term
  [S9 주7] [R12 §III-1](#krlib-immediate_annuity-r12).
- **inheritance** — survival and persistency together, because death itself triggers a
  payment and ends the contract.

`lives_if(t)` is the survival probability proper and the two differ on every shape: on the
anchor `pols_if(9) = 1.000000` while `lives_if(9) = 0.959799`. `pols_exit(t)` is built
from the decrements and the guarantee rather than from `pols_if`, so
`check_pols_roll_fwd()` compares two independent constructions. On the life shape nothing
exits at all until the guarantee expires — `pols_exit(t) = 0` for `t = 0 … 8` — and then
everyone who died inside it exits at once, `pols_exit(9) = 0.046529974860`. An
implementation that decremented the obligation on every death would show a residual from
the first period and would then miss the step.

The two guarantee tests are deliberately different and it is easy to conflate them. The
obligation is open at time `t` for `t < g`; the instalment on row `t` falls at `t + 1` and
is guaranteed for `t + 1 <= g`. So on the same row `pols_if(10) = l(10) = 0.953470025140`
and `payment_factor(10) = l(11) = 0.946528763357` are different numbers, and either error
shifts the guarantee cliff by a year.

The **선지급** (commutation) right is recorded and not exercised. The projection pays the
guaranteed instalments on their contractual dates. That is **[std]**, and it is
value-neutral only because the discount rate the 약관 gives is the same 공시이율 that sets
the annuity [S1 주4] [S3] [S7 제11조제3항]; the option has value on a falling-rate path
and none on a rising one, and this model does not price it.

## The horizon is the limiting age on one shape and the term on the other two

```
proj_len() = max(g − 1, ω − x)      life
           = n − 1                  inheritance, certain
```

`proj_len()` is the **last row index**, not a row count: the anchor has 51 rows, `t = 0`
to `t = 50`, and `ω − x = 110 − 60 = 50`. Reading it as a count drops the last instalment
on the two term shapes — on model point 9 that is ₩9,052,841.76 of outgo, 9.1% of the
annuity total.

On the life shape the projection runs to the limiting age of the shipped table, where
`qx = 1`, so the obligation is **exhausted rather than truncated**: `lives_if(51) = 0`, the
last row's payment weight is exactly zero, and nothing is thrown away at the horizon. That
is what ω = 110 is for, and it is **[std]** — no retrieved Korean source states a limiting
age for an annuitant table. The `max` covers the case, impossible on any shipped model
point but reachable at a high enough issue age, where the 보증지급기간 outlives the
annuitant's limiting age and the guarantee sets the horizon instead.

## The retention is a switch, because the law could not decide either

On the 상속연금형 만기형 the 만기보험금 is the **gross** single premium while the fund
opens at the premium net of the load, so part of each year's interest must be retained.
With `s(m, i)` the accumulation of ₩1 a year in arrears,

```
A(t) = V(t) i(t)  −  (M − V(t)) / s(m, i(t)),      m = n − t
```

and the second term is the **만기보험금 지급재원**. Both terms move against the
policyholder when the rate falls — the interest falls with `i` and the retention *rises*,
because `s` shrinks — which is why an annuity on this shape can more than halve while the
guaranteed floor never moves. That retention was in the 산출방법서 and not in the 약관;
금융분쟁조정위원회 조정결정 제2017-17호 held on 2017-11-14 that it could not be asserted
against the policyholder [R1], the 금융감독원 extended the ruling to the industry on
2018-03-15 [R2 §4](#krlib-immediate_annuity-r2), and the 대법원 restored it for the contracts before it on 2025-10-16
[R6] [R21]. The current market states the deduction on the face of the 약관 [S7 별표1].

Neither reading is "the" right one, so `retention_basis` carries both:

- `as_designed` — `retention_pp(t)` as above, and the fund reaches `M` exactly at maturity;
- `as_ordered` — `retention_pp(t) = 0`, so the annuity is interest on the fund alone, the
  fund stands still at `V(0)`, and the 만기보험금 is met from the insurer's own resources.

Model points 6 and 7 are the same contract on the two bases, so the difference between
their statements is the quantity that was litigated for eight years: **₩1,932,133.95 a
year against ₩2,375,750.00, +22.96% of income**, and ₩3,506,753.94 of extra undiscounted
outgo per ₩100,000,000 of premium. `retention_shortfall_pp()` discounts the same thing to
inception on the crediting path — `(M − V(0)) v(10)` = **₩3,882,556.06** — and it appears
on the **right-hand side of `check_annuity_basis()`** rather than being tolerated away,
because under `as_ordered` the pricing identity does not close on `V(0)` and should not.
A specification that buries the retention inside an annuity factor cannot express the
question the litigation was about, which is why it is an explicit, switchable term here.

`retention_pp(t)` is **re-struck every year against the remaining term at the current
rate**, and that is not decoration. On a level rate a retention computed once at inception
gives the same answer and the fund still lands on `M`, so the error is invisible on points
6 and 7. It appears only on a stepping rate: on point 8 the retention runs ₩220,272.34 →
₩271,273.86 over twenty years and `av_pp(20) = 100,000,000.00` exactly *because* it is
re-struck. `check_av_terminal()` and `check_av_roll_fwd()` are what catch it.

## The 계약자적립액 on the life shape has no contractual role

`av_pp(t)` runs the 약관's own recursion — 「연금개시후에는 생존연금 발생분을 차감한
금액」 [R1] — on all three shapes:

```
V(t + 1) = V(t) (1 + i(t)) − A(t),      i(t) = Max[공시이율, 최저보증이율(t)]
```

It reaches `M` at maturity on the inheritance shape under `as_designed`, stands at `V(0)`
under `as_ordered`, and exhausts to zero on the certain shape (`av_pp(10) = −4.1e−8` on
point 9, float noise against a ₩100m contract); `check_av_terminal()` asserts each. **On
the life shape it is none of those things.** A life annuity's fund is not its reserve, and
the recursion runs negative from `t = 28` — ₩372,637.63 at `t = 27` and −₩4,566,085.59 at
`t = 28` — at about the point where the annuitant has outlived the factor the fund bought.

It is published anyway, and not floored at zero. Flooring it would hide what a 종신연금형
does with the money and would break the retrospective closed form
`V(0)(1 + i)^t − A s(t, i)` that `check_av_roll_fwd()` tests the recursion against.
Nothing downstream reads the negative value: surrender is prohibited on that shape, so
`cv_pp(t)` is nil at every duration, and no benefit is measured on the fund. What holds
the life shape to its basis instead is `check_annuity_basis()`, the actuarial equivalence
at inception.

## Columns that are deliberately zero

Three of `result_cf()`'s ten columns are zero at every `t` on the anchor, and each zero is
a product fact rather than an unimplemented feature. They are published as columns all the
same, because a statement whose columns appear and disappear with the model point cannot
be compared across model points.

| Column | Zero because |
|---|---|
| `claims_death` | the 종신연금형 pays **no** death benefit once the annuity has begun — 「별도의 사망보험금은 지급되지 않습니다」 [S5]; the unpaid guaranteed instalments are what survives the annuitant and they are already inside `annuity_payments`. Adding one double-counts the guarantee |
| `claims_lapse` | 「종신연금이 지급개시된 이후에는 해지할 수 없습니다」 [S7 제31조] [S3] [S5 주2], and on an immediate annuity that bites from month one, so both the rate and the value are nil |
| `claims_maturity` | a life annuity has no 만기보험금 at all; only the inheritance shape has one, and only in its last period |

There is deliberately **no `claims` column** beside the three `claims_*` columns. The
`claims(t, kind)` cells stays, but a cash flow statement must not publish its own subtotal
beside its parts, or the columns stop summing to `net_cf`.

`claims_lapse(N) = 0.00` on **every** shape, including the two that permit surrender: the
lapse rate is suppressed in the final period so that a contract in its last year runs to
its 만기보험금 or its last instalment. Without it the maturity benefit is diverted into a
surrender value of a different amount for no reason any contract states.

## Modules that are off in the base run

Four behaviours are switchable and the anchor exercises none of them, which is why the
anchor's numbers are independent of all four.

| Module | Control | State on the anchor | Exercised by |
|---|---|---|---|
| The retention | `retention_basis` | **inert** — the life shape has no 만기보험금 | points 6 and 7 |
| The stepping floor | `crediting_basis` | **inert** — 2.50% exceeds every step of the floor | point 8, on `min_guar` |
| Voluntary surrender | `lapse_rate` | **off** — nil by contract, not by assumption | points 6, 7, 8, 9 |
| The longer guarantee | `annuity_term` | 10 years | point 3, at 20 years |

`min_guar` is a **[std]** modelling device and not a product a carrier sells: `decl_rate`
is set to zero on that basis so that Max[공시이율, 최저보증이율] resolves to the floor at
every duration, which is the only way the floor's duration stepping gets exercised by a
shipped model point. It is also the basis on which the anchor carrier publishes its
해약환급금 run [S1 §VI-2], so the device has a documentary counterpart.

Everything else a Korean 즉시연금 can carry is **recorded in `product-spec.md` and not
modelled**: the front-loaded life annuity in its six carrier names; the 거치형 selling
mode with its 추가납입 and 중도인출; the proportional split of the fund across shapes [S8];
부부계약 [S6]; the large-contract discount [S6 §10-나] [R27]; the 상속연금형 종신형
sub-shape, only the 만기형 being carried; the 100세 and 기대여명 guarantee options; and the
100.1%-of-premiums fund floor at annuitisation, which is a **deferred**-contract mechanic
[S7 별표1 주8] [S9] — applying it here would erase the whole 3.50% load on day one and make
`check_premium_split()` fail by ₩3,600,000. The 책임준비금, the 해약환급금준비금, the
IFRS 17 CSM and the K-ICS 요구자본 are cited [REG-R10] [REG-R11] [REG-R13] [REG-R60] and
not computed.

## Processing order

Row `t` of `result_cf()` carries period `t`, which runs from time `t` to time `t + 1`.
Three of the flows depend on the order within a period, so it is stated rather than left to
be inferred:

1. the single premium, the commission and the acquisition expense, at time `t`, on row 0
   only;
2. the fund is credited at `i(t) = Max[공시이율, 최저보증이율(t)]`, the floor band being
   the half-open `[dur_from, dur_to)` in completed policy years that contains `t`;
3. the 연금연액 `A(t)` falls due at time `t + 1`, in arrears on the 계약해당일, weighted by
   `payment_factor(t)`, with the 0.80% annuity charge beside it at the same weight;
4. **deaths** are taken at the end of the period, after the crediting and after the annuity
   due to the survivors, so the 사망보험금 is paid on the fund carried forward, `V(t + 1)`
   — ₩372,321.86 rather than ₩370,755.90 on point 6 at `t = 0`;
5. **surrenders** are taken after the deaths, at `cv_pp(t + 1)`, and are suppressed in the
   final period;
6. the 만기보험금 falls at the end of the last period on the inheritance shape, weighted by
   `pols_if(N + 1)` and not `pols_if(N)` — it is payable on survival **to** maturity, one
   further period of decrement away, ₩79,495,349.97 against ₩80,023,013.57.

Steps 4 and 5 are **[std]** end-of-year conventions on an annual grid; a real contract
settles a death mid-year and pays the 연금월액 to the date of death.

## Inputs are external files

Four CSVs sit beside `run.py` in `products/immediate_annuity/`, read at run time rather
than stored inside the model — the `annuallife/TradLife_A` layout, as against
`basiclife/BasicTerm_S`, which keeps its inputs inside the model through modelx's IOSpec
machinery:

```
products/immediate_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  charge_table.csv
  crediting_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Immediate_KR_A/              <- formulas only
    __init__.py                   (the model docstring)
    _system.json
    Data/__init__.py              (reads the four CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

The model folder holds nothing but formulas — no `_data/`, no IOSpec, no embedded values —
so a diff of the model shows logic changes only. The consequence worth knowing is that
**the model is not portable on its own**: copying `Immediate_KR_A/` without its parent's
CSVs produces a model that reads and then fails on first evaluation.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache; readers placed there would re-read every file for
every contract. They live instead in the unparameterized `Data` Space, which takes no
parameters, so each file is read **once per model** however many contracts are projected.
`input_dir()` returns `_model.path.parent`, resolved at run time from where the model was
read, so the model works wherever the repository is checked out.

| Reference | Cells | File | Keyed on |
|---|---|---|---|
| `model_point_file` | `data.model_point_table()` | `model_point_table.csv` | `point_id` |
| `mort_table_file` | `data.mort_table()` | `mort_table.csv` | `(sex, age)`, age in **보험나이** |
| `charge_table_file` | `data.charge_table()` | `charge_table.csv` | `shape` |
| `crediting_table_file` | `data.crediting_table()` | `crediting_table.csv` | none; a duration-band test |

`crediting_table.csv` is the one read **without** an index, because the lookup is a
half-open band test rather than a key lookup. `mort_table.csv` is sorted on read, because
`Projection.mort_rate` indexes into it.

There is no lapse table, no surrender-value schedule and no commission scale, because the
product has none of those things. The 해약공제액 is a published run of zeros
[S1 §VIII] [S10], so a surrender-charge schedule would be a file of zeros and the
statutory 표준해약공제액 cap [REG-R20] binds nothing here; the 모집수수료 is one first-year
rate on a single premium and sits in `charge_table.csv` beside the load it has to stay
below; and **no retrieved source gives a surrender rate for 즉시연금 at all**, so
`lapse_rate` is carried per model point, where its effect can be isolated.

Every input file but the model point table carries a `provenance` column and every cell in
it begins with a citation tag. The model point table carries none, because its columns are
a *configuration* and not an assumption set — with the single exception of `lapse_rate`,
an assumption in disguise, whose absence of a source is stated in the `Data` docstring and
in the technical notes instead.

### `mort_table.csv` is a construction, and there was no alternative

The 제10회 경험생명표, applied from April 2024, is produced by 보험개발원 and is **not
published in full**: only 평균수명 and 65세 기대여명 are released, and they reach this
library through trade press rather than through KIDI itself [REG-R33] [REG-R34]. There is
therefore no Korean annuitant table to transcribe. What is shipped is a Makeham law
`mu(x) = A + B c^(x − 60)`, `q(x) = 1 − exp(−mu(x))`, fitted **exactly** to three published
numbers and to nothing else:

- the 개인연금사망률 at 보험나이 60 and 70, the only carrier-published annuitant rates in
  the corpus — 남자 0.00353 / 0.00728, 여자 0.00118 / 0.00251 [S1 §IV-2];
- the complete 65세 기대여명 of the 제10회 경험생명표, 남 23.7년 / 여 27.1년
  [REG-R33] [REG-R34].

Three constraints, three parameters, no free choice. The residual is the third published
anchor at 보험나이 50, which the fit reproduces at 0.0027451336 against a published 0.00225
for men (**+22.01%**) and 0.0009892120 against 0.00097 for women (+1.98%); the deviation is
recorded in the `provenance` cell of those two rows rather than smoothed away. `qx` is set
to 1 at ω = 110, **[std]**, and that is what lets the life-shape projection close on an
exhausted table instead of a truncated one. The table carries **no improvement scale and
must not acquire one**: it is a period construction on undated anchors, and this is the
opposite posture from `frlib`'s `Rente_FR_S`, whose mandatory tables are generational and
where an improvement factor would double-count.

The one check the construction can be held to is the selection gap. The shipped table gives
a complete `e(65)` of 23.70 / 27.10 years against the public 완전생명표's 만나이 figures of
19.5 / 23.7 [REG-R38] [REG-R39] — about **4.2 years above the population for men and 3.4
for women** — which is the insured-versus-population margin any annuitant basis must show,
and the strongest single reason a Korean immediate-annuity model may not be run on
완전생명표 rates.

The resulting factor at the anchor cell is **19.502675087912** and the 연금연액
**₩4,948,039.16** on a fund of ₩96,500,000. It cannot be checked against a published
factor, because **no carrier publishes one** and no filed 산출방법서 for an 즉시연금 was
retrieved [R31]. What can be checked is the two shapes that carry no mortality, and they
agree closely: the model's 확정기간연금형 at 남자 60, 10년, 2.50% is ₩10,858,010.26 a year,
which is ₩904,834.19 a month before the annual-to-monthly adjustment and **₩894,628.93**
after it, against 교보's published **90만원** at 남자 55 on a 2.52% basis [S3] — −0.5%, on a
shape for which the annuitant's age and sex are irrelevant; and the 상속연금형 만기형 on
the same terms gives ₩1,932,133.95 a year, **₩161,011.16** a month, against
`product-spec.md`'s own independent **[std]** reconstruction of ₩161,000.

### The other three tables

| File | Contents | Provenance |
|---|---|---|
| `charge_table.csv` | one row per `shape`: `acq_charge_rate`, `admin_charge_rate`, `risk_prem_rate`, `comm_rate`, `acq_expense_rate`, `annuity_charge_rate`, `db_rate` | 계약체결비용 and 계약관리비용 published by shape at 남자 60 [S1 §VIII]; the 3.50% composite **[std]**, corroborated to 1.4% against [S3]'s four 확정기간 terms; 위험보험료 1.4669% published for 상속형 20년만기 [S1 §VIII], rounded and applied unscaled **[std]**; 모집수수료 the round mid-point of 2.08% / 1.75% [S1 §VII] **[std]**; `acq_expense_rate` derived **[std]**; `annuity_charge_rate` 0.80% [S1 §VIII] with its treatment as an insurer expense **[std]**; `db_rate` 10% of the single premium [S1] [S3] [R1 별표1](#krlib-immediate_annuity-r1) |
| `crediting_table.csv` | two bases × three duration bands: `decl_rate` and the stepped `min_guar_rate` on half-open `[dur_from, dur_to)` bands | 공시이율 2.50% is the rate the anchor carrier declared on this exact product at 2017-04 [S1 §IV-4]; its adoption **[std]**, the rate being underivable [REG-R18] [REG-R24]. 최저보증이율 1.25 / 1.00 / 0.75% is the only three-step schedule published on a contemporaneous 즉시연금 illustration [S3]; adoption **[std]**. That a floor exists at all is compulsory [REG-R16]. The `min_guar` basis is **[std]**, a modelling device |
| `model_point_table.csv` | ten contracts: both sexes, issue ages 45 / 55 / 60 / 70 / 80, both guarantee lengths, both retention bases, both crediting bases, all three shapes, premiums ₩10,000,000 to ₩5,000,000,000 | a configuration, not an assumption set, so no `provenance` column. Point 1 is the notes' anchor: the premium is the median of the only public dataset [R12 그림3](#krlib-immediate_annuity-r12) and exactly the 소득세법 ten-year exemption cap [REG-R58]; the age is the one the expense, commission and mortality disclosures are all published at [S1]; the ten-year guarantee is the choice 97.3% of life-shape buyers made [R12 표7](#krlib-immediate_annuity-r12). `lapse_rate` is the exception and is **[std]** |

**Substituting a filed basis** means replacing `mort_table.csv` with a same-schema file
keyed on exactly the same `(sex, age)` in 보험나이, and `charge_table.csv` and
`crediting_table.csv` with the filed 산출방법서's own figures. **No formula changes.** The
first thing any production use of this model must do is the mortality replacement, and it
will move `annuity_factor()` and therefore every life-shape figure on this page.

## Sign convention

`net_cf(t)` is **income positive** — premium income less every outgo — which is the
library-wide orientation, so a `result_cf()["net_cf"]` column can be summed or compared
across every model here without checking which product it came from. `net_cf(0)` on the
anchor is a large **positive** number, +₩91,512,376.53, because the single premium is
income; there is never another positive row.

The technical notes print the stream outgo-positive as `CF(t)`, and that orientation is
published verbatim as `liability_cf(t)`, the exact negative. Both are columns, rather than
one being made to stand for the other, so that a reader holding the notes beside the model
reads the same sign in both. No column runs the other way: unlike `frlib`'s *frais
d'arrérages*, every charge in this product is an outgo of the insurer or a deduction from
the fund, and nothing is retained out of a payment.

## The identity `check_net_cf()` closes

`net_cf` = `premiums` − `annuity_payments` − `claims_death` − `claims_lapse` −
`claims_maturity` − `commissions` − `expenses`, read back out of the published
`result_cf()` columns so that a reader adding up the printed statement gets the printed
total.

It is the shortest ledger in the library, and that is the product: no premium income after
`t = 0`, no acquisition cost to amortise, no unearned premium to add back on surrender and
no claim-handling expense. Reading it back out of the frame rather than recomputing it
from the formulas is the point — it is the check that catches a benefit kind that exists
in `claims(t, kind)` but was never given a column, which would leave the statement silently
short of outgo the model is charging, and it is why `result_cf()` publishes the three
`claims_*` splits and no aggregate `claims` column.

The other ten checks are `check_pols_roll_fwd` (the obligation against independently built
exits), `check_lives_roll_fwd` (the survival curve against an explicit product of `1 − q`),
`check_av_roll_fwd` (the fund against a per-shape closed form), `check_av_terminal`,
`check_annuity_basis` (the pricing identity, with `retention_shortfall_pp()` on the
right-hand side), `check_premium_split`, `check_rate_level`, `check_guarantee_certain`,
`check_payment_factor` and `check_surr_value`. All eleven take no argument, return a real
`bool`, and are `True` on every one of the ten shipped model points; the per-`t` residuals
are published under `<name>_resid(t)` where a per-period residual exists.

Two tolerances, and the split is deliberate. `roll_fwd_tol = 1e-10` closes the probability
identities, which are dimensionless and evaluated in one expression. `val_tol = 1e-12` is
**relative** and is multiplied by `prem_pp()` at the point of use, so on a ₩100,000,000
contract the monetary checks close to ₩1e−4 and on a ₩5,000,000,000 one to ₩5e−3 — far
below one won either way, and scaled so that a large model point is not held to an absolute
tolerance a float64 won amount of order 1e9 cannot meet.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S`, `savings/CashValue_SE` and
`annuallife/TradLife_A` wherever those models have an analogue, and follow the sister
libraries' payout models wherever the products share machinery.

### The notes' symbols, and where they live

The full mapping is in the `Projection` Space docstring, so a reader holding the technical
notes beside the model can cross-walk without leaving the model. The rows that carry a
decision rather than a translation:

| Notes | Cells | Why |
|---|---|---|
| `IF(t)` | `pols_if(t)` | not a policy count and not a survival probability, but the probability that a **payment obligation remains**; the name is kept because it is what the rest of the library weights expense by and what `result_cf()` publishes first |
| `l(t)` | `lives_if(t)` | the survival probability proper, which differs from `pols_if` on every shape |
| `n`, `g` | `annuity_term()` | one name for the 보증지급기간, the 보험기간 and the 연금지급기간, because the arithmetic treats them identically; what differs is what the projection does *after* the term, and that is the shape's business |
| `F(t)` | `payment_factor(t)` | the weight on the payment at `t + 1`; `pricing_factor(t)` is the same weight on the pricing basis, written separately so the pricing identity compares two constructions |
| `A(t)`, `R(t)` | `annuity_pp(t)`, `retention_pp(t)` | the retention is a named term of the annuity and not a component of a factor, which is the whole point of the switch |
| `CF(t)` | `liability_cf(t)` | the notes' outgo-positive orientation, published verbatim beside the income-positive `net_cf` |

### Names this product argued for, and against

- **`decl_rate`, not `gongsi_rate`.** The 공시이율 is the declared crediting rate under the
  same definition `delib` settled on for the laufende Verzinsung, and the romanized name
  was retired in the library's naming review. So was `yejeong_rate` for the 예정이율, which
  is `prem_int_rate` and **does not appear in this model at all** — there is no pricing
  interest rate on a product whose annuity is struck at the declared rate.
- **`claims_lapse`, not `claims_surr`.** Named for the decrement rather than for the
  해약환급금, matching the `kind` argument that produces it, which is the convention the
  library settled on across all six country libraries.
- **`lapse_rate` is the annual rate**, as everywhere in this library. There is no
  `lapse_rate_mth`, because the grid is annual; and there is no `mort_rate_mth` for the same
  reason.
- **`av_pp` and `cv_pp` keep the savings-chassis names** even though this contract has no
  accumulation phase, because they are the same two quantities `WholeLife_KR_A` and
  `Pension_KR_A` publish and a reader moving between the three should not have to relearn
  them.

There is deliberately **no** `prem_pp_mth`, `pols_maturity`, `cv_floor_ratio`,
`surr_chg_cap_pp`, `renewal_decline_rate`, `improve_factor`, `deferral_period`,
`payment_freq`, `escalation_rate` or `mort_basis` switch anywhere in the model, and each
absence is a product fact: a single premium has no monthly form; the term shapes end at a
maturity benefit rather than a maturity count; the 해약공제액 is nil so nothing is capped;
there is no renewal; the table is a period construction; the 즉시형 has no deferral; the
annual mode is the contract's own mode and not an approximation of the monthly one; no
retrieved carrier offers indexation of any kind; and one table serves as both the pricing
basis of the life shape and the decrement of all three.

## Standardizations used

Every row is **[std]**. The sourced contractual parameters are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are
not repeated. "Observed range" is what the retrieved documents actually bound; several of
them bound nothing at all, and that is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| `expense_load_rate` = `acq_charge_rate` + `admin_charge_rate` | 2.20% + 1.30% = **3.50%** of P, one rate across all three shapes | the carrier publishes the load by component *and* by shape; the composite carries one number rather than the 0.42-point allocation difference, because a second independent document supports the same total | 종신 2.61 + 1.30 = 3.91%, 상속 20년만기 2.19 + 1.30 = 3.49% at one carrier [S1 §VIII]; solving the annuity-certain identity against 교보's four published 확정기간 terms reproduces all four within **1.4%** on a 4.97% first-day deduction [S3]; the disputed 2012 contract's 사업비 was 5.325% [R1 §1-가](#krlib-immediate_annuity-r1) and the supervisor assumed 6.0% [R2 참고](#krlib-immediate_annuity-r2) |
| `risk_prem_rate` | **0.00%** (life), **1.47%** (inheritance, certain), once at inception | the published 1.4669% is disclosed on a *twenty*-year basis at exactly the anchor age and is applied **unscaled** to a ten-year contract — conservative, and the direction is stated rather than corrected, no source supporting a term scaling | three published levels on one basis: 0.0000% for 종신연금형 1형, 1.4669% for 상속연금형 20년만기, 4.9466% for 종신연금형 2형 [S1 §VIII]; nothing published for the certain shape at all |
| `comm_rate` | **2.00%** of P at `t = 0`, nil thereafter | the round mid-point; what matters structurally is not the level but that it sits **below** the 2.20% 계약체결비용, so the charge covers the commission at the same moment | 2.08% (종신연금형) and 1.75% (상속연금형) at 남자 60 [S1 §VII]; every retrieved figure is first-year-only on a bancassurance sale [S2] [S3] [S4] [S5] |
| `acq_expense_rate` | **1.50%** = load − commission | a *treatment*, not a disclosure: it sets the insurer's own expense equal to the charge it took, which is what makes `check_premium_split()` close and "no acquisition strain" a property of the statement | nothing published; **no Korean carrier discloses an expense rate** for this product |
| `annuity_charge_rate` | **0.80%** of the 연금연액, modelled as an insurer expense and **not** netted off the payment | the charge is disclosed in the **cost** table and not the benefit table, so the annuitant receives the gross annuity; netting it would also break the pricing identity, the fund having bought the gross annuity | the level 0.80% is published on all three shapes [S1 §VIII]; whether a carrier's own 산출방법서 builds it into the factor instead is **[unverified]**, no filed basis document having been retrieved [R31] |
| `decl_rate` (공시이율) | **2.50%** a year, level, exposed as a scalar | the level the anchor carrier declared on this exact product at 2017-04; it equals the 2026 평균공시이율 and sits inside the band of the three most recent observations. **No model in this library derives a Korean declared rate and none should** — it is the product of a 공시기준이율 majority-weighted to the insurer's own 운용자산이익률 [REG-R18] [REG-R24] | 4.8% at 2011-09 [R27]; 4.5% at 2012-09 [R1]; 3.40% → 2.80% over 2015–2016 [S5]; 2.95% [S4]; 2.83% [S2]; **2.50% at 2017-04** [S1 §IV-4]; 2.52% at 2017-12 [S3]; 2.80% at 2023-01 [S13]; 2.55% at 2025-01 [S12]; 2.56% at 2026-09 [S14]; the weighting differs by carrier — 50/50 [S6], 40/60 [S12], 35/65 [R1] |
| `min_guar_rate` (최저보증이율) | **1.25% / 1.00% / 0.75%**, stepping at five and ten completed policy years | the only three-step schedule published on a contemporaneous 즉시연금 illustration whose annuity figures this product also uses, and at the mid-point of the 2017–2026 range. **It is a rate on the fund, never a floor on the annuity** — the substance of the whole dispute | 2.5% / 2.0% for the 2007–2014 cohorts [S10]; 2.0 / 1.5 / 1.0% [S4]; 1.5 / 1.0% [S2]; **1.25 / 1.00 / 0.75%** [S3]; 1.25 / 1.00 / 0.50% [S13] [S14]; 1.0 / 0.75 / 0.50% at 2024 [S7 제7조] |
| the `min_guar` crediting basis | `decl_rate = 0`, so Max[·] resolves to the floor at every duration | a modelling device and not a product: the only way the floor's duration stepping is exercised by a shipped model point. It is also the basis the anchor carrier's own 해약환급금 run is published on [S1 §VI-2] | not a marketed basis anywhere in the corpus |
| mortality construction | Makeham `A + B c^(x − 60)`, three parameters fitted exactly to three published anchors | the 제10회 경험생명표 is not published at all, so there is no table to transcribe and a fitted law is the only honest alternative to inventing one | the fit misses the third published anchor at 보험나이 50 by **+22.01%** (M) and +1.98% (F) [S1 §IV-2]; check: the shipped table sits 4.2 / 3.4 years above the public 완전생명표 at 65 [REG-R38] [REG-R39] |
| limiting age `omega_age` | **110**, with `q(110) = 1` | it is what makes the life-shape obligation *exhausted* rather than truncated: `lives_if(51) = 0` on the anchor | no retrieved Korean source states a limiting age for an annuitant table |
| mortality improvement | **none applied**, and none should be | the table is a period construction on undated anchors; adding a scale is a change to the CSV's schema, not to a formula | none published |
| pricing basis vs best estimate | **one table serves both** | no carrier publishes an annuitant table at all, so a second one would be a second invention. A real limitation: the model shows **no mortality margin** on the life shape | none available |
| `lapse_rate` | **2.00%** a year on the inheritance and certain shapes; **nil** on the life shape as a matter of contract; **nil in the final period on every shape** | a round placeholder, carried per model point so its effect can be isolated. It is not second-order: on point 6 it produces ₩15.9m of `claims_lapse` against ₩17.3m of annuity payments | **nothing**. No retrieved source gives a surrender rate for 즉시연금 by duration, by shape or at all. The one interaction that argues for a low figure is that the 만기보험금 is the gross premium while the surrender value is below it at every earlier duration [S1 §VI-2] |
| maintenance expense, expense inflation | **none** | the only recurring charge any retrieved 즉시연금 document publishes is measured on the annuity, not per policy and not per 만원 of fund; inventing one beside it would be a number with no source | none published |
| decrement timing | deaths at the end of the policy year, then surrenders, then the maturity benefit | annual-grid conventions; a real contract settles a death mid-year and pays the 연금월액 to the date of death | fixed by the grid, not by a disclosure |
| the annual grid itself | one crediting rate per policy year | the 공시이율 is reset on the first of each month and fixed for that month; an annual grid carries one rate a year, exact only where the rate is level, which on the representative basis it is | worth **1.14%** of the annuity's timing value at 2.50% (`i / i^(12)` = 1.0114072482), which is why every comparison with a published 연금월액 on this page is made on the adjusted figure |
| 선지급 (commutation) | right recorded, exercise **not** modelled | value-neutral **only** because the 약관's discount rate is the same 공시이율 that sets the annuity [S1 주4] [S3] [S7 제11조제3항]; the option has value on a falling-rate path and none on a rising one | no take-up figure published anywhere |
| issue-age band, anchor premium | 45–80; ₩100,000,000 | the band is the composite of the retrieved carriers' own bands; the premium is the median of the only public dataset and exactly the 소득세법 ten-year exemption cap [R12 그림3](#krlib-immediate_annuity-r12) [REG-R58] | issue ages from 45 [S1] to 80 [S3] [S4]; minimum premiums ₩10,000,000 upward, differing by carrier [R16, secondary](#krlib-immediate_annuity-r16) |
| `roll_fwd_tol`, `val_tol` | 1e-10, 1e-12 (relative, scaled by `prem_pp()`) | one closes dimensionless probability identities in a single expression; the other closes won amounts of order 1e8 to 1e9 read back out of a `DataFrame` | both far below one won at every shipped premium |

**One row above is a placeholder and is labelled as such rather than dressed up as an
estimate**: `lapse_rate`. It is the most serious data gap in the model after the mortality
table, precisely because it is *not* second-order on the two shapes that permit surrender.
Everything the anchor model point publishes is independent of it, the life shape carrying a
nil rate by contract; nothing on points 6 to 9 is.

## Tests

`tests/test_immediate_annuity_kr.py` asserts the notes' worked example **hard-coded**, so a
reviewer can check it by eye rather than by re-running the model:

- The anchor's derived quantities at inception: `av_pp_init() = 96,500,000.00`,
  `annuity_factor() = 19.502675087912` with its published decomposition into the
  annuity-certain 8.752063930971 and the life-contingent tail 10.750611156941, and
  `annuity_pp(0) = 4,948,039.1569365682` level at every `t`.
- The `t = 0 … 50` cash flow statement to the won at the rows the notes print, the three
  columns that are `0.00` in every row asserted **as zeros** rather than left implied, and
  the undiscounted totals — ₩138,160,059.32 of annuity outgo, ₩2,605,280.47 of expenses
  splitting into ₩1,500,000 at inception and ₩1,105,280.47 of annuity charge, and
  **−₩42,765,339.80** of net cash flow.
- The state behind them: `mort_rate(0) = 0.00353` and `mort_rate(10) = 0.00728` reproduced
  exactly, `pols_if(t) = 1.0` for `t = 0 … 9` against `lives_if(9) = 0.959798841`,
  `pols_exit(8) = 0.0` and `pols_exit(9) = 0.046529974860`, both `t = 10` weights, and
  `av_pp(27) > 0 > av_pp(28)`.
- The dispute panel, points 6 and 7 as one contract on two bases: the two annuity levels
  and the +22.96%, `retention_pp(0) = 443,616.0529903907` against 0,
  `retention_shortfall_pp() = 3,882,556.0565768769`, `claims_maturity` identical at
  ₩79,495,349.97 on both, and the ₩3,506,753.94 difference in `Σ net_cf`.
- The floor-stepping panel, point 8: `crediting_rate(4) = 0.0125` and
  `crediting_rate(5) = 0.0100`, the annuity falling 50.73% from ₩967,602.66 to ₩476,691.58
  while `av_pp(20) = 100,000,000.00` exactly, and the retention *rising* across each step.
- The load cross-check, point 9: `annuity_pp(0) = 10,858,010.2647236791`, its monthly
  equivalent of ₩894,628.93 against 교보's published 90만원 [S3], and `claims_lapse(9) = 0`.

Each of the notes' twenty-one pitfalls earns a test named after it — that `pols_if` is not
a survival probability, that the guarantee is a `max` and not a sum, that the two guarantee
tests differ, that `proj_len()` is a last index, that `q` is read at the age attained at the
*start* of the period, that the model runs on 보험나이 and not 만나이, that the mortality
table is never presented as the 경험생명표, that the life-shape annuity is not re-struck
each year, that `av_pp` is not floored at zero, that the retention is re-struck annually,
that the 최저보증이율 is a rate on the fund and not a floor on the annuity, that the floor's
duration bands are half-open in completed policy years, that the 0.80% charge is not netted
off the payment, that no death benefit is paid on the 종신연금형, that the death benefit is
measured on the fund carried forward, that no lapse decrement touches the life shape, that
no surrender fires in the final period, that the 만기보험금 is weighted by `pols_if(N + 1)`,
that the 100.1% floor is not applied, that no discounted column exists, and that no
aggregate `claims` column is published. The four optional modules are asserted in **both**
positions of their switch.

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
with no orphan CSV, the `provenance` column on every assumption CSV, the docstrings and
their required phrases — including the `payment obligation remains` phrase in the `pols_if`
docstring, which is how this model earns its exemption from the start-of-period
policy-count assertion — the `result_cf()` contract (indexed by `t`, first column
`pols_if`, a `net_cf` column, all names `lower_snake_case`, no NaN, length equal to
`proj_len() + 1`), the round trip through `mx.write_model`, and that every `check_*()`
returns `True` on **every** shipped model point.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-immediate_annuity-r1
[R21]: #krlib-immediate_annuity-r21
[R27]: #krlib-immediate_annuity-r27
[R31]: #krlib-immediate_annuity-r31
[R6]: #krlib-immediate_annuity-r6
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R20]: #krlib-reg-r20
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R58]: #krlib-reg-r58
[REG-R60]: #krlib-reg-r60
<!-- END generated citation links -->
