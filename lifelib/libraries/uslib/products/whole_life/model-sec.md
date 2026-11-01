# In-Force Implementation Notes

**Status:** Draft, 2026-11-01. `WholeLife_US_SEC` is [`WholeLife_US_S`](model.md) taught
to project from a valuation date. Besides policies issued at that date, it takes policies
already in force there, in any month of their policy year, and policies to be written in
the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes. The suffix adds lifelib's letters to `S`: `E` for in force, as
in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is
still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `WholeLife_US_S` on another time axis, and it reads `WholeLife_US_S`'s assumption tables
> in place, every assumption unchanged. The contractual skeleton is sourced, the
> final-expense rate card [S7] among it, and everything else is a **[std]**
> standardization, **including all four guarantee-basis tables**: illustrative curves
> calibrated to the worked example's anchors, *not* the 2017 CSO / 4% tables the notes
> name, and not even one basis between them, as
> [`model.md` sets out](#uslib-whole_life-guarantee-basis-tables). Replace them with
> company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/whole_life/run_sec.py            # point 1: the anchor cell, in force
python products/whole_life/run_sec.py 19         # point 19: the loan variant, mid-year
python products/whole_life/run_sec.py --block    # every model point, summed row by row
```

The first prints, as rows `t = 0 … 11`, the twelve months `run.py` prints for
`WholeLife_US_S`'s point 1, the worked example's policy year 10, with the counts and rates
behind them. Every column agrees with `run.py`'s but `expenses`, which are in
valuation-date dollars here, 5.00 in the first month where `run.py` prints 5.98, and
`net_cf` and `liability_cf` with them. Three lines to the same thing for point 19:

```python
import modelx as mx
model = mx.read_model("products/whole_life/WholeLife_US_SEC")
model.Projection[19].result_cf()
```

`Projection` takes a `point_id`, as in `WholeLife_US_S`. `result_cf()` has
`WholeLife_US_S`'s twelve columns — `pols_if`, `premiums`, `rider_premiums`, `expenses`,
`premium_taxes`, `claims_death`, `claims_lapse`, `claims_maturity`, `div_cash_paid`,
`loan_draws`, and the net flow under both signs, `net_cf` and `liability_cf` — with one
row per month from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out
the counts behind it on the same rows: `pols_if`, `pols_new_biz`, then the month's deaths
and surrenders in processing order and the maturities of the last covered month, then
`WholeLife_US_S`'s four decrement rates, annual and monthly, written 0 outside cover.
`result_cv()` has `WholeLife_US_S`'s values per policy, each month's closing balances and
its two benefit amounts, with zeros before issue. `result_cf_annual()` sums `result_cf()`
into policy years, as in `WholeLife_US_S`, and leaves out the months before issue.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`), so the
run holds the cells of one point at a time.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to maturity at attained age 100.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index, and the contract runs on
  it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1` and
  `age(t) = age_at_entry() + duration(t)`, as in `WholeLife_US_S`, and `is_anniv(t)` is
  true in the last month of each policy year in cover. `BasicTerm_SE` reaches the same
  numbers by adding one a month, a recursion as long as the frame; the closed form needs
  no such chain of calls.

`anniv_mth(t)`, the month of the anniversary that ends the policy year containing `t`, is
on the valuation clock: `t + 11 − duration_mth(t) % 12`, where `WholeLife_US_S` returns the
policy month `12 × duration(t) + 11`. The two are the same number only where the clocks
coincide.

Point 1 is the worked example's anchor cell, in force 108 months. At `t = 0` it is on the
anniversary that opens policy year 10, at attained age 54. Its tenth anniversary, where
the year's dividend is credited and buys paid-up additions, falls at `t = 11`,
`WholeLife_US_S`'s month 119, and its frame has 552 rows, `t = 0 … 551`. Point 19 is the
loan variant in force 114 months, six months into policy year 10: its tenth anniversary
falls at `t = 5`, its next premium, policy year 11's $1,800, at `t = 6`, and its frame has
546 rows. Point 22 is point 2 to be issued three months after the valuation date:
`duration_mth(0) = −3`, it is on the books from `t_entry() = 3`, rows 0 to 2 are zeros,
and its frame has 663 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium-paying period and the months instalments fall due, the guaranteed cash value schedule and its interpolation, the net single premiums and theirs, guaranteed mortality at the attained age and the scale and best-estimate rates built on it, the lapse schedule and its final-year zero, the dividend declaration and its first year, loan-interest capitalization, the purchases of the PUA rider and the REDUCE_PREM excess, the graded death benefit's policy years 1–2, maturity at attained age 100 | expense inflation, `inflation_factor(t) = 1.02^(t/12)` |

The interest-sensitive lapse overlay reads a constant, `competitor_rate`, so it is on
neither clock, and the product has no scenario table. Expense inflation alone runs on `t`,
so the maintenance charge is in valuation-date dollars, for every point alike.
Acquisition, 90% of the first year's annual premium plus $250, is charged per policy
issued, in the issue month, and not inflated, as in `basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`WholeLife_US_S` computes, whatever the point's count: `WholeLife_US_S` already charges
acquisition on the policies in force at its `t = 0`, which on new business are the
policies issued. On `WholeLife_US_S`'s fourteen new-business points every cash flow and
every count agrees, and so does every other cell the two models share but three whose
meaning changed: `pols_if_init()`, now the count already in force at the valuation date,
0 for new business; `model_point()`, a row of another table; and `result_pols()`, which
gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `WholeLife_US_S`'s
columns, and nine of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s
two, and seven that open an in-force policy's state. Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `pua_face_init` | dollars of paid-up face | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the paid-up additions in force |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, capitalized interest included |
| `div_accum_init` | dollars | the start of month 0 | the dividend accumulation balance, interest and dividends to date included; 0 unless the option is ACCUM |
| `pua_face_prev_anniv_init` | dollars of paid-up face | the anniversary that opened the policy year under way, on or before the valuation date: the close of policy month `12 × duration(0) − 1` | the paid-up additions entering the policy year, which its PUA-block dividend and its term-blend gap read |
| `loan_bal_prev_anniv_init` | dollars | that anniversary | the loan entering the policy year, on which the year's interest capitalizes and which the dividend's interest margin credits at the loan rate |
| `div_prev_anniv_init` | dollars | that anniversary | the dividend credited there, which `div_prev_anniv` returns through the year under way, and so the year's premium offset and its REDUCE_PREM excess read |
| `prem_cum_init` | dollars | the start of month 0 | the gross premium, before any dividend offset, of every instalment due from issue to policy month `duration_mth − 1`, which the graded final-expense death benefit reads |

The seven state columns are 0 on a point issued at or after the valuation date, the
values at issue. In the first policy year, `duration_mth` 1 to 11, the three anniversary
columns hold their issue values, 0, because that year opened at issue, and
`div_accum_init` is 0 too, because no dividend has been credited yet. On a point valued
on an anniversary, `duration_mth` a multiple of 12, the two `_prev_anniv_init` columns
are the same instant as `pua_face_init` and `loan_bal_init`, and must equal them.
`prev_anniv` is `WholeLife_US_S`'s word, as in its `div_prev_anniv`: the anniversary that
**opened** the policy year, where `anniv` alone, as in `is_anniv` and `anniv_mth`, is the
one that ends it. An extract that fills the three anniversary columns from the
anniversary after the valuation date is a year out.

Everything else the projection uses is fixed at issue, in `WholeLife_US_S`'s columns, or
follows from the policy clock: the cash value is read from the guaranteed schedule by
policy year, the net single premiums and the mortality by attained age, and the premium
from the model point or, on final expense, from the rate table.

| `WholeLife_US_S` | `WholeLife_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_inforce` (whole policy years) | `duration_mth` | The policy clock, in months, so that a policy can be valued in any month of its year; the S column is dropped |
| `puaf_inforce` | `pua_face_init` | Renamed in place, so that the seven state columns share one vocabulary: a column measured entering month 0 is the cell it opens with `_init` added, and so is `div_prev_anniv_init`, `div_prev_anniv`'s value through the year under way; a balance measured at the anniversary adds `_prev_anniv_init` |
| `loan_inforce` | `loan_bal_init` | The same |
| — | `pua_face_prev_anniv_init` | `WholeLife_US_S` opens its in-force frame on an anniversary, where this is `puaf_inforce` |
| — | `loan_bal_prev_anniv_init` | The same, with `loan_inforce` |
| — | `div_accum_init` | `WholeLife_US_S` opens the accumulation balance at 0, the notes' `DA = 0` |
| — | `div_prev_anniv_init` | `WholeLife_US_S` takes last year's dividend as 0, an anniversary before its frame |
| — | `prem_cum_init` | `WholeLife_US_S` sums the premiums paid from issue, whatever its frame |

On the twins the five new columns take what `WholeLife_US_S` itself assumes, so each twin
opens as its S row does: on point 1 the paid-up additions at the anniversary are its
4,100, the loan 0, the accumulation balance and last year's dividend 0, and the premiums
paid 16,200, nine years at $1,800.

The columns carried over are read as `WholeLife_US_S` reads them. For a policy in force,
the facts they record are still those at issue, the dividend option and the premium mode
excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `product`, `premium_period`, `sex`, `risk_class` | codes, as in `WholeLife_US_S`'s table | issue |
| `issue_age` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `face_amount` | dollars, level for the life of the policy | issue |
| `annual_premium` | dollars a year, the participating design's `G`; blank on final expense, whose premium comes from `premium_rates.csv` | issue |
| `dividend_option` | `PUA`, `CASH`, `ACCUM`, `REDUCE_PREM`, or `NONE` on final expense | the option in force over the frame |
| `premium_mode` | `A`, `SA`, `Q` or `M` | the mode billed over the frame; its instalments fall on the policy clock |
| `pua_rider_premium` | dollars a year, level while premiums are payable | issue |
| `term_blend_target` | dollars of target face, 0 for no blend | issue |
| `loan_utilization` | a fraction of the guaranteed cash value | an assumption, not a fact about the policy |
| `provenance` | text: `WholeLife_US_S`'s on a twin, the generator's on any other row | — |

The loan is not carried forward as a balance. `WholeLife_US_S` holds it at
`loan_utilization × CV_t` in every month of its frame, and this model does the same from
month 0 on, whatever `loan_bal_init` says. That column is what month 0's advance,
`loan_draw(0)`, is measured from, and what the death benefit of month 0 deducts, so the
advance closes any gap between the extract's loan and the fraction: point 19 owes
2,070.00 entering month 0 and 2,098.33 at its end, an advance of 28.33.

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the nine in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,320 months at issue age 0, the youngest the product
  issues, and 780 at 45, the youngest the shipped tables carry. Set to 0, the Reference
  refuses future new business altogether, and a negative horizon is itself refused;
- each opening-state column is a number, zero or more;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- the non-participating final-expense design has no paid-up additions,
  `pua_face_init` and `pua_face_prev_anniv_init`, and no dividend, `div_prev_anniv_init`;
- only the ACCUM option has an accumulation balance, which on any other the projection
  would drop from every benefit;
- on a point valued on an anniversary the two `_prev_anniv_init` columns equal
  `pua_face_init` and `loan_bal_init`;
- in the first policy year, which opened at issue and has credited no dividend yet, the
  three anniversary columns and `div_accum_init` are 0.

A row whose paid-up additions at the anniversary exceed those entering month 0 is
accepted. The model never shrinks the block, so such a row records a partial surrender
of additions, which the model does not implement, and it is projected from the values it
gives.

A point whose cover had ended by the valuation date,
`duration_mth ≥ 12 × (100 − issue_age)`, reads, but `proj_len()` refuses it, naming the
point: the end of cover is the product's rule, not the table's. So a loop over the block
meets such a row only when it reaches it, after projecting the points before it.
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`WholeLife_US_S` and its table by `tests/sec_support.py`, from the `WholeLife_US_SEC`
entry in its `SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a
`WholeLife_US_S` row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py WholeLife_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 | twin | S point 1 | the anchor cell in force 108 months, on the anniversary opening policy year 10, with its 4,100 of paid-up additions: the worked example's year |
| 2–15 | twin | S points 2–15 | issued at `t = 0`: `WholeLife_US_S`'s new business, under each dividend option, with a loan, the PUA rider, the term blend funded and unfunded, limited pay, the female cell, final expense level and graded, and monthly mode |
| 16 | derived | S point 5 at S month 108 | REDUCE_PREM on the anniversary opening policy year 10, last year's dividend 288.66 |
| 17 | derived | S point 4 at S month 108 | ACCUM on the same anniversary, with 1,766.74 accumulated |
| 18 | derived | S point 8 at S month 78 | the funded term blend six months into policy year 7, before its crossover: 106,074.52 of paid-up additions, 93,241.47 at the anniversary |
| 19 | derived | S point 6 at S month 114 | the loan variant six months into policy year 10: a loan of 2,070.00, 1,900.00 at the anniversary |
| 20 | derived | S point 12 at S month 18 | the graded final-expense plan inside its graded years, with 3,162.00 of premiums paid |
| 21 | derived | S point 5 at S month 659 | REDUCE_PREM in its last month of cover: a one-row frame |
| 22 | future | S point 2, 3 months on | to be issued at `t = 3` |

A derived row's `policy_count` is the count `WholeLife_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `WholeLife_US_S` carries into it, each column
read as `WholeLife_US_S`'s own formulas read it: the paid-up additions, the loan and the
accumulation balance at the close of S month `d − 1`; the paid-up additions and the loan
at the close of S month `anniv_mth(d) − 12`, the anniversary that opened the policy year
of `d`; S's `div_prev_anniv(d)`; and S's `prem_cum(d − 1)`. So the row continues the S
projection from there: points 16 and 17 open with 0.704576 policies, and point 21 with
0.041820. Its `policy_id` is the S row's with the month appended, `WLPAR-000005-M108`,
and a future row's carries the months to issue, `WLPAR-000002-F3`. Row `t` of a
generated point is month `t + source_mth` of its S point. All 22 are at issue age 45 on
the participating design or 65 on final expense, the only issue ages `cv_table.csv`
carries, so a point at any other needs the schedules extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_SURR"`, after the month's deaths;
- `"BEF_MAT"`, after its surrenders;
- `"AFT_DECR"`, after the maturities of the last covered month, the notes' `l_{t+1}`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `WholeLife_US_S`'s,
unchanged but for their guard outside cover and, in `"AFT_DECR"`, the last covered month
read on the policy clock. Any other timing raises. One name means two instants in the two
references: `BasicTerm_SE`'s `"BEF_MAT"` counts the policies at the **start** of a month,
before that month's maturities, where `WholeLife_US_S`'s counts them at its **end**, after
the month's surrenders. The policies here mature at the end of the last covered month, as
in `WholeLife_US_S`, so the name keeps the S meaning, and `BasicTerm_SE`'s timing is not
adopted.

The survivors carried into month `t` are those of month `t − 1`'s `"BEF_DECR"` count,
which `"BEF_NB"` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's deaths and surrenders in the order `"BEF_MAT"` takes them. So
`pols_if_at(t, "AFT_DECR")` is `pols_if_at(t + 1, "BEF_NB")` at every `t` of every frame,
and it is `pols_if(t + 1)` except where month `t + 1` is an issue month, whose new business
joins `pols_if`. The chain of calls from month `t` back to `t_entry()` is one cell a month,
where `WholeLife_US_S`'s ran through five: a cold `net_cf` in the last month of a
660-month frame runs 669 cells deep, against 3,304 in `WholeLife_US_S`, so modelx needs a
recursion limit of 668 for it. On the longest frame the shipped tables allow, 780 months
for point 2 issued 120 months on, it runs 669 deep too, because the chain stops at the
issue month. Each report evaluates its columns in ascending `t`, and a sweep of the
committed points that way runs at most 29 cells deep, on the graded final-expense point.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `WholeLife_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `WholeLife_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (100 − issue_age)` is `WholeLife_US_S`'s frame from issue. Outside
it, before issue and from maturity on, every count is zero, and so every cash flow, every
value state and every dividend. No count evaluates a decrement rate there, and no table is
read at a policy year or an attained age the policy does not have: `is_anniv` and
`prem_due` are false, and `premium_pp_ann`, `rider_premium_pp_ann`, `prem_cum`, `cv_pp`,
`nsp_mth`, `mort_rate_guar`, `div_prev_anniv`, `div_credited`, `oyt_face`, `div_to_pua`,
`div_accum`, `pua_face_offset`, `pua_face`, `pua_cv`, `loan_bal`, `loan_draw` and the
death benefit are zero before any table is read. Every other value is zero through them.

## The opening state

`WholeLife_US_S` opens an in-force point on an anniversary, from three columns,
`duration_inforce`, `puaf_inforce` and `loan_inforce`, and assumes the rest: no
accumulation balance, no dividend at the anniversary before its frame, and premiums
summed from issue. That is all the worked example's policy year 10 needs. A policy valued
at any month of its life needs all seven state columns, each what `WholeLife_US_S` carries
into that month, and each shows on a derived row:

- **`div_prev_anniv_init`.** Point 16, on REDUCE_PREM, is valued on the anniversary opening
  policy year 10. It pays 1,800.00 less last year's dividend of 288.66 at `t = 0`, so
  1,511.34 a policy, as `WholeLife_US_S` collects at its month 108. With the column at 0
  it would pay 1,800.00.
- **`div_accum_init`.** Point 17, on ACCUM, is valued on the same anniversary with
  1,766.74 accumulated, which earns its monthly interest from `t = 0` and reaches the
  death, surrender and maturity benefits. With the column at 0 the balance would be lost
  from every benefit, and the maturity claims of its last month alone would be 1,060.82
  lower.
- **`prem_cum_init`.** Point 20, the graded final-expense plan valued six months into
  policy year 2, has paid two annual premiums of $1,581, 3,162.00. To the end of the
  graded years, `t = 5`, its death benefit is
  `0.97 × 1.1 × 3,162.00 + 0.03 × 15,000 = 3,823.85`, and from `t = 6`, policy year 3, the
  face. With the column at 0 it would be 450.00.

A valuation off an anniversary needs the year's opening values as well, because the
annual quantities of a policy year read the balances entering it, and inside the year
those have moved on:

- **`pua_face_prev_anniv_init`.** Point 18 is the funded term blend six months into policy
  year 7. The year's rider instalment, paid at its start, has bought 12,833.05 of
  additions since the anniversary, so the point holds 106,074.52 entering month 0 against
  93,241.47 at the anniversary. The one-year-term layer of the year is sized on the
  second: `200,000 − 100,000 − 93,241.47 = 6,758.53`, which the year's dividend funds in
  full, so the death benefit of month 0 is `100,000 + 106,074.52 + 6,758.53 = 212,833.05`,
  `WholeLife_US_S`'s at its month 78. On the current additions there would be no gap at
  all.
- **`loan_bal_prev_anniv_init`.** Point 19, the loan variant six months into policy year
  10, owes 2,070.00 entering month 0 against 1,900.00 at the anniversary. At its tenth
  anniversary, `t = 5`, the year's interest capitalizes on the second, 6% of 1,900.00,
  114.00. The dividend's interest margin reads the same 1,900.00, though at the shipped
  rates, 6.00% on the loan and on the dividend alike, the loan cancels out of it.

On a point valued on an anniversary each pair is one instant, and `Data` refuses a row
where they differ. Off an anniversary they differ wherever the year has moved the balance
since it opened: by the rider's purchases, by the REDUCE_PREM excess, which buys additions
in the year's first month, and, for the loan, every month with the cash value. Point 21,
REDUCE_PREM in its last month, holds 4,823.37 of additions against 4,544.40 at its
anniversary.

`WholeLife_US_S`'s goldens on its point 1 read four values from the month before its
frame: `pua_face(107)`, `loan_bal(107)`, `cv_pp(107)` and `pua_cv(107)`. On the twin no
month comes before the frame, and each is opening state at `t = 0`: `pua_face_init()` is
the 4,100, `loan_bal_init()` 0, `cv_pp_anniv(9)` 9,500, the guaranteed cash value entering
policy year 10, and `pua_face_prev_anniv_init() × nsp(54)` 1,648.93, each `WholeLife_US_S`'s
value. The worked example's year then runs as in `WholeLife_US_S`: the dividend of 326.25
credited at `t = 11` brings the paid-up additions to 4,876.79, `WholeLife_US_S`'s
`pua_face(119)`.

## Departures from WholeLife_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock or of the opening
state, and every recursion begins at `t_entry()`. Where `WholeLife_US_S`'s test would have
stayed correct on the valuation clock, it moved anyway, so that cover has one definition.
Of `WholeLife_US_S`'s 97 cells, 40 are unchanged, one of them, `dyn_lapse_factor`, with a
line re-wrapped, 9 have a new docstring only and 44 are rewritten; two are renamed and two
removed, and 11 cells are new, 106 in all. The twin identity names each of the four, with
its reason: a cell of `WholeLife_US_S`'s that this model lacked would fail it otherwise.

| Cells | `WholeLife_US_S` | `WholeLife_US_SEC` | Why |
|---|---|---|---|
| `duration_mth` | `t` | `duration_mth_init() + t` | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × (100 − x)`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past maturity | The frame starts at the valuation date. `maturity_mth()` is new and keeps `WholeLife_US_S`'s formula |
| `proj_start`, `duration_inforce` | an in-force frame opens at `12 × duration_inforce()`, the elapsed policy years | removed: every report and check runs over `range(proj_len())` | Every frame opens at `t = 0`, and `duration_mth_init()` replaces the elapsed years |
| `puaf_inforce`, `loan_inforce` | the in-force point's opening paid-up additions and loan | renamed `pua_face_init` and `loan_bal_init` | One vocabulary for the seven state columns |
| `pols_if`, `pols_if_init`, `pols_if_at` | a recursion from `pols_if_init()`, the column's 1.0, at `proj_start()`, five cells a month | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`, one cell a month; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `pua_face`, `div_accum`, `loan_draw`, `claim_pp(·, "DEATH")`, `check_pua_roll_fwd_resid` | open at `proj_start()` from `puaf_inforce()`, 0 and `loan_inforce()` | open at `t_entry()` from `pua_face_init()`, `div_accum_init()` and `loan_bal_init()` | Every recursion begins on the books, from the opening state |
| `prem_cum` | a recursion back to issue | opens at `t_entry()` from `prem_cum_init()` | No cell asks for a month before the valuation date |
| `div_prev_anniv` | `div_credited(12 × duration(t) − 1)`, a policy month passed as `t`; 0 before the frame | `div_credited(anniv_mth(t) − 12)`, or `div_prev_anniv_init()` where that month is before `t_entry()` | On the valuation clock month `12 × duration(t) − 1` is not the anniversary |
| `anniv_mth` | `12 × duration(t) + 11`, a policy month | `t + 11 − duration_mth(t) % 12`, a valuation month | The same |
| `div_int` | the cash value `cv_pp(t − 12)`, in any month | `cv_pp_anniv(duration(t))`, and the loan from `loan_bal_prev_anniv_init()` where `t − 12` is before `t_entry()`; zero but at an anniversary | `cv_pp(t − 12)` is a month before the valuation date in a point's first projected year. At an anniversary, the one month its dividend reads it, the two cash values agree to within an ulp. In any other month nothing reads it, and before issue it would read the schedule at a negative policy year |
| `div_pua`, `oyt_face`, `loan_int` | the balance twelve months back, or `puaf_inforce()` and `loan_inforce()` before the frame | the same, or `pua_face_prev_anniv_init()` and `loan_bal_prev_anniv_init()` where that month is before `t_entry()` | A policy year under way at the valuation date opened before it |
| `pua_face_rider` | a mid-year instalment priced at `nsp_mth(t − 1)` | the same straight line, written at the start of month `t` | At `t = 0` on a valuation off an anniversary, `t − 1` is before the valuation date. The arithmetic is the same |
| `lapse_rate`, `cv_pp_anniv` | the years to maturity as `proj_len() // 12` | `maturity_mth() // 12` | `proj_len()` now counts from the valuation date |
| `expenses` | acquisition, `0.9 G + 250` at `t = 0`, on the policies in force there | `(0.9 G + 250) × pols_new_biz(t)` | A point already in force bears none, and one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `inflation_factor` | `1.02^(t/12)`, `t` the policy month | the same formula, `t` the valuation month | Unit costs in valuation-date dollars |
| `check_pols_roll_fwd_resid`, `check_pols_roll_fwd` | `pols_if(t) − pols_if(t + 1) − …`, the tolerance scaled by `pols_if_init()` | `pols_if(t) − pols_if_at(t + 1, "BEF_NB") − …`, scaled by `policy_count()` | Next month's new business is no part of month `t`'s movement, and `pols_if_init()` is 0 on new business |
| `div_to_pua`, `claim_pp(·, "MATURITY")`, `pols_maturity`, `pols_if_at(·, "AFT_DECR")` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `is_anniv`, `prem_due`, `premium_pp_ann`, `rider_premium_pp_ann`, `cv_pp`, `pua_cv`, `nsp_mth`, `mort_rate_guar`, the dividends and the counts | unguarded, or guarded by `t` against 0, `proj_start()` or `proj_len()` | false or zero outside cover, `is_active(t)`, before any table or rate is read | A future point's months before issue have `t ≥ 0`, and policy month −1 is no anniversary |
| `result_cf`, `result_cv`, `check_pua_roll_fwd` | `range(proj_start(), proj_len())` | `range(proj_len())` | Every frame opens at `t = 0` |
| `result_cf_annual` | whole policy years | the policy years in the frame, the months before issue left out | An in-force point's first row holds the rest of its current policy year, and its `pols_if` is the count at the valuation date |
| `result_pols` | `pols_if`, the three outflows and four rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()`, and no rate read before issue |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz` and the five new opening-state accessors.

One read goes further ahead than the month after its own, and it is kept.
`oyt_face(t)` sizes the term-blend layer of the policy year containing `t` on the dividend
credited at the anniversary that ends it, `div_credited(anniv_mth(t))`, up to eleven
months ahead, because the one-year term in force through the year is bought with that
dividend. It opens no chain forward: the dividend depends on the balances entering the
year and on the schedules alone, never on the layer or on a later month, and the frame
ends on an anniversary, so the read never leaves it.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
and `liability_cf` with it. A point in force carries that expense in valuation-date
dollars, so point 1's `expenses(t)` is `WholeLife_US_S`'s `expenses(108 + t)` divided by
`1.02^9`, about 1.195. Its other cash flows and its counts are `WholeLife_US_S`'s from
month 108 on. Point 22 is `WholeLife_US_S`'s point 2 three months on in those columns too;
its maintenance expense is `1.02^(3/12)` above S's, and its acquisition, 1,870.00, is
S's exactly.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 2 to 15, issued
  at the valuation date, every cell of `WholeLife_US_S`'s agrees at every argument
  `WholeLife_US_S` evaluates in its own sweep, but for `pols_if_init`, `model_point` and
  `result_pols`, whose meaning changed, and the four cells this model renamed or removed.
  So the goldens `tests/test_whole_life_us.py` asserts on those points — every dividend
  option, the loan, the rider, the term blend funded and unfunded, limited pay, the
  female cell, final expense and monthly mode — hold here with no number restated. Unlike
  `Term_US_SEC`'s, the identity holds on any count, since `WholeLife_US_S` already charges
  acquisition on the policies issued. The same suite holds the model to the conventions
  every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the `"BEF_DECR"`
  count, new business enters once at its `policy_count`, nothing happens before issue,
  and the in-force columns are present.
- **The splice**, in `tests/test_whole_life_us_sec.py`: each `WholeLife_US_S` point
  restated in force at a month either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share,
  to 1e-9, but those the twin identity skips, `pols_if_init` and `model_point`, and those
  whose value is a month or a frame on the valuation clock, `proj_len`, `anniv_mth` and
  `result_cf_annual`. The participating points are restated at months 12, 108, 115, 119,
  120 and 600,
  the final-expense points at 12, 18, 23, 24, 115 and 400: inside the graded years, in
  their last month, in the first after them, and later. The funded blend is restated at
  78 and 83 too, before its crossover, and ACCUM, REDUCE_PREM and final expense level in
  their last covered month.
  So does the anchor cell's twin from S's month 108, and S's point 1 restated later in its
  life. So do three variants of S's points, in a copy of S's table that is never
  committed, for branches S's own points do not reach: the PUA rider paid monthly,
  REDUCE_PREM paid semi-annually, and the graded plan paid quarterly. Inflation, the one
  input on the valuation clock, is set to 0 in both models. Three switches that ship off
  are turned on in both, the PUA-block dividend, the premium-offset overlay and the
  interest-sensitive lapse overlay, and the loan rate is set apart from the dividend rate,
  because at the shipped settings parts of the opening state show in one place alone: the
  additions at the anniversary in the term blend, last year's dividend under REDUCE_PREM,
  and the loan at the anniversary in its interest.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column, every kind of valuation month and every premium mode, and a test asserts that
  they do. The other cases carry the `sec_full` marker and show as skipped, with the
  reason, unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI
  run runs the full grid too.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point
  is the S projection moved on, with zeros before issue in `result_cf`, `result_pols` and
  `result_cv` and no decrement rate evaluated there, and so is each variant issued a month
  on.
- **How it computes**: on every row the splice and the future business compare, the core
  by default and the full grid with `USLIB_SEC_FULL=1`, after every report, no cell has
  been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1` but
  `oyt_face`, which reads the year's dividend at `anniv_mth(t)` and nowhere else. On a
  fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, because the policy clock is a closed form, and every point is swept
  under modelx's recursion limit lowered to 60, which a recursion backward over the frame
  would exceed.
- **Counts, validation and regeneration**: the roll-forward closes, `"AFT_DECR"` is the next
  month's `"BEF_NB"`, and `pols_if_at` refuses a timing it does not have; `result_pols()`
  is `WholeLife_US_S`'s, column for column, with `pols_new_biz` beside it; doubling
  `policy_count` doubles every cash flow and moves no per-policy value; each malformed row
  is refused naming its point, a missing, negative or misplaced opening state among them,
  at either end of the first policy year and on the first anniversary; the horizon is a
  Reference, which at 0 refuses any future business, saying so; a point past its cover is
  refused by `proj_len()`, and `run_sec.py --block` refuses it before printing anything; a
  zero count, durations written as floats, balances written as whole numbers, a policy
  issued 120 months on, rows valued on the first anniversary and the month after, and a
  row whose additions at the anniversary exceed those entering month 0 are accepted; and
  the committed table is what `WholeLife_US_S` generates.
- **The opening state and the rest**: the twin of the worked example's point opens with
  the four values `WholeLife_US_S`'s goldens read before its frame, and at the shipped
  assumptions it is S's point from month 108 on, in every cell but those expense inflation
  moves, which carries the walk through policy year 10 over; the derived rows carry the
  dividend, the accumulation balance, the premiums paid and the anniversary values as
  above, and with the first three zeroed they give the 1,800.00, the shortfall of 1,060.82
  and the 450.00 above; expense inflation runs on the valuation clock at the shipped 2%,
  which only this test sees, since the splice sets the rate to 0; acquisition falls on new
  business alone; every guarded cell holds its value outside cover and reads no rate
  there, on the committed points and on the splice's future rows, which carry the rider,
  the blend and each dividend option before issue; the points of a block sum row by row;
  an extract without the generator's three columns projects the same numbers; and
  `run_sec.py` prints the model's numbers, for a point in force, a point restated, a point
  to be issued and the block, line by line.

```bash
python -m pytest tests/test_whole_life_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_whole_life_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k WholeLife_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
