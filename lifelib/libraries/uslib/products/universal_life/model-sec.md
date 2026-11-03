# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `UL_US_SEC` is [`UL_US_S`](model.md) taught to project from
a valuation date. Besides policies issued at that date, it takes policies already in force
there, in any month of their policy year, and policies to be written in the ten years
after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The
product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in `BasicTerm_SE`,
and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `UL_US_S` on another time axis, and it reads `UL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual mechanics are sourced from a specimen policy
> [S3]. The two assumptions that drive this product hardest, the **current credited rate**
> and the **current COI scale**, are both **[std]**, because insurers do not publish them,
> and so are the mortality table, the lapse vector, the premium persistency scale and every
> expense. Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/universal_life/run_sec.py            # point 1: the anchor cell, at t = 0
python products/universal_life/run_sec.py 6          # point 6: the in-force cell, mid-year
python products/universal_life/run_sec.py --block    # every model point, summed row by row
```

The first prints, as rows `t = 0 … 11`, the cash flows and the account value roll-forward
`run.py` prints for `UL_US_S`'s point 1, the worked example's three rows among them, each
table line for line the same, and then the counts and rates behind them. Three lines to
the same thing for point 6:

```python
import modelx as mx
model = mx.read_model("products/universal_life/UL_US_SEC")
model.Projection[6].result_cf()
```

`Projection` takes a `point_id`, as in `UL_US_S`. Its three result tables are indexed by
`t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `UL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — income-positive, so the flow columns sum to `net_cf` |
| `result_av()` | `UL_US_S`'s per-policy account value roll-forward, in the columns and order of the technical notes' worked example, with zeros before issue |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `UL_US_S`'s two monthly decrement rates, written 0 outside cover |

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`, then a
collection), so the run holds the cells of one point at a time. It prints where each point
stands at the valuation date, then the block's first twelve rows and the block summed into
projection years.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the last month at attained age 120.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index `d(t)`, and the contract
  runs on it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1`
  and `age(t) = age_at_entry() + duration(t)`, as in `UL_US_S`. `BasicTerm_SE` reaches the
  same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`UL_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force point there. What the valuation clock adds is that `t = 0` is one
instant for every point, that a point may be issued after it, and that a point in force
brings in what its past has left it: the face its withdrawals have left, the free
allowance it has used in the policy year, the premiums it has paid and its MEC status.

Point 3 is `UL_US_S`'s in-force cell, in force 120 months. At `t = 0` it is on the
anniversary that opens policy year 11, at attained age 45, with its surrender charge run
off, and its frame has 912 rows, `t = 0 … 911`. Point 6 is the same policy six months on,
in force 126 months: policy year 12 begins at `t = 6`, where the premium persistency
steps from 80% to 78% and the attained age to 46, and its frame has 906 rows. Point 9 is
`UL_US_S`'s point 1 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first premium of $150.00 falls at `t = 25`, and its frame has 1,057 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the surrender charge run-off and the lapse shock in the policy year after it, the guaranteed COI scale, the per-unit charge's step-down after policy year 10, the premium persistency and base lapse scales, the GPT and 7-pay limits, all by policy year; the corridor factor and the mortality rate at the attained age; withdrawals from the first anniversary; charges, premiums and withdrawals ceasing at attained age 121; the end of the projection at policy month `omega_mth()` | expense inflation, `inflation_factor(t) = 1.025^(t // 12)`; the declared credited rate `crediting_rate_ann(t)` and the competitor rate `comp_rate_ann(t)`, flat as shipped |

Expense inflation keeps `UL_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. The two declared rates are economic inputs: a declared-rate scenario
would be indexed by `t`, one path for every point of a block, however old the policy. As
shipped both are 4.00% in every month, so the clock shows in no number, and the dynamic
lapse multiplier is 1. Acquisition is charged per policy issued, in the issue month, and
not inflated, as in `basiclife/BasicTerm_SE`; it ships at zero, as in `UL_US_S`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`UL_US_S` computes, whatever the point's count: `UL_US_S` charges acquisition on the
policies in force in the issue month, which on new business are the policies issued. On
`UL_US_S`'s two new-business points every cash flow and every count agrees, and so does
every other cell the two models share, at every argument `UL_US_S`'s own sweep evaluates,
but three whose meaning changed: `pols_if_init()`, now the count already in force at the
valuation date, 0 for new business; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz`. On point 3 the projection is `UL_US_S`'s,
month for month, its expenses apart, which are in valuation-date dollars.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `UL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and eight of its columns are the in-force
interface: `basiclife/BasicTerm_SE`'s two, and six that open an in-force policy's state.
Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value, its loaned part included |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `sum_assured_init` | dollars of face | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date; at most `sum_assured`, the face at issue |
| `wd_used_year_init` | dollars | the start of month 0 | the free withdrawal allowance already used in the policy year under way: the free part of every withdrawal since the anniversary on or before the valuation date, so 0 on a point valued on an anniversary |
| `cum_prem_init` | dollars, of either sign | the start of month 0 | the gross premiums paid from issue to policy month `duration_mth − 1`, less every withdrawal paid, which the GPT test, the 7-pay test and the TARGET premium cap read |
| `is_mec_init` | an int code: 0, not a MEC; 1, a MEC | the start of month 0: the latch after policy month `duration_mth − 1`'s 7-pay test | whether the policy has failed the 7-pay test, and so is a modified endowment contract for good |

The six state columns are 0 on a point issued at or after the valuation date: it is issued
at the face `sum_assured`, with no account value, no loan, and nothing used, paid or
failed. `av_pp_init` and `loan_bal_init` are `UL_US_S`'s own columns: they already measure
the account value and the loan entering `UL_US_S`'s first month, so they keep their names.
Each new column is named for the cell it opens: `sum_assured_init` for `sum_assured_at`,
`wd_used_year_init` for `wd_used_year`, whose name already says that it restarts each
policy year, `cum_prem_init` for `cum_prem_pp`, under `ULSG_US_S`'s name for the same
column, and `is_mec_init` for `is_mec`. No quantity of the product is read at the last
anniversary, so none needs a column at a second instant.

| `UL_US_S` | `UL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `loan_bal_init` | the same | `UL_US_S` already opens its in-force point from them |
| — | `sum_assured_init` | `UL_US_S` opens every point at the face at issue, `sum_assured` |
| — | `wd_used_year_init` | `UL_US_S` takes none of the year's free allowance as used at its `t = 0` |
| — | `cum_prem_init` | `UL_US_S` restarts the premiums less withdrawals at 0 on its in-force point, though the TARGET premium cap reads them |
| — | `is_mec_init` | `UL_US_S`'s latch looks back from its `t > 0` only |

On the twins the four new columns take what `UL_US_S` itself assumes, so each twin opens
as its S row does: on point 3 the face at issue, 100,000, and nothing used, paid or failed.

The columns carried over are read as `UL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the option, the premium, its load and the
withdrawal excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `UL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the surrender-charge base, whatever later withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL`, `SINGLE` or `TARGET` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, paid monthly |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `wd_pp` | dollars a month | the withdrawal taken in every month of the frame from the first anniversary on |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `gsp`, `glp`, `seven_pay_prem` | dollars, the compliance inputs | issue |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the eight in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than the
  projection from issue plus ten years: 1,356 months at issue age 18, the youngest the
  product issues, and 1,152 at 35, the only issue age the shipped COI scale carries. Set
  to 0, the Reference refuses future new business altogether, and a negative horizon is
  itself refused;
- the account value, the loan, the face and the year's usage are each a number, zero or
  more. A balance is never negative in force. `UL_US_S` lets a point's account value fall
  below zero once it is in permanent shortfall, because it does not implement the grace
  cascade that would end such a policy, so the message for `av_pp_init` says what to do:
  restate a point in permanent shortfall no later than the last month its account value is
  still zero or more. Without a loan that is the month its shortfall begins, as point 7
  is; with one, the shortfall test, which nets the loan, fails months earlier;
- `cum_prem_init` is a number, of either sign. Premiums less withdrawals is a tax measure,
  not a balance, and since the notes' "less a portion of withdrawals" is taken as the whole
  withdrawal **[std]**, withdrawals can exceed the premiums paid;
- `is_mec_init` is 0 or 1, an int code; written as 1.0 it reads as `True`;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- `sum_assured_init` is above 0 on a policy in force, which holds a face, so an extract
  that leaves the column at zero is refused, rather than projected on the corridor alone;
- `sum_assured_init` is at most `sum_assured`, since face increases are not modelled. A
  face below it is accepted, whether withdrawals cut it or an elective decrease the model
  does not implement, and it is projected from the value given;
- on a point valued on a policy anniversary, `duration_mth` a multiple of 12,
  `wd_used_year_init` is 0: the year's allowance restarts there before any usage is read,
  so any other value would be dropped without a word;
- `is_mec_init` is 1 wherever the 7-pay test has already failed in the month before the
  valuation date: `cum_prem_init` above `seven_pay_prem` times the policy years to then,
  in the first seven. A failure the cumulative premium no longer shows, after withdrawals,
  is the column's to record, and either value is accepted.

A point at or past the end of the projection at the valuation date,
`duration_mth ≥ 12 × (121 − age_at_entry)`, reads, but `proj_len()` refuses it, naming
the point: "point_id 5: duration_mth 1032 is at or past the end of the projection, policy
month 1032, attained age 121". The end of the projection is the model's rule, not the
table's. So a loop over the block meets such a row only when it reaches it, after
projecting the points before it. `run_sec.py --block` asks every point for its frame
before it projects any, and stops before it prints anything.

The assumption tables read at a policy year or an attained age are checked too, each once,
in the `Data` cell its reader in `Projection` takes its extent from: the last policy year of
`prem_persistency.csv` and `lapse_table.csv`, the first and last ages of
`corridor_factors.csv` and `mort_table.csv`, beyond which each reads its nearest row, and
the last policy year of each issue-age cell of `coi_rates.csv`. The key column is read by
value, so a year written `16.0` is 16, and a key that is blank, text or not a whole number
is refused, naming the file, the column and the lines it is on: "prem_persistency.csv:
policy_year must be a whole number; it is not on line [17]". So are keys that do not run one
row a year or an age, without a gap or a repeat, policy years from 1, the message naming
each key that repeats, with its lines, and each that is missing: "mort_table.csv: the ages
must run one row an age, without a gap or a repeat; age 26 is on line [10, 11]; no line
holds age 27". So is a blank sex or class in the COI scale, and a rate that is blank, text
or infinite: "mort_table.csv: mort_rate must be a number; it is not on line [44]".
`class_count()` and `surr_charge_count()` check the class factors and the surrender-charge
schedules the same way: a class or a schedule blank or on two rows, and a factor, a charge
or a run-off that is not a number. The reader asks for its extent, or the count, before it
reads a value, so a projection meets the checks first. `UL_US_S` takes each extent from the
key column as pandas reads it, where a blank is a missing value the extent skips: with the
last policy year of `prem_persistency.csv` blank, every year from 16 on reads year 15's 72%
in place of 70%, and nothing says so. A blank rate is a missing value to it too, which shows
in its flows or is lost in a `min` or a `max`: a blank lapse rate reads as the cap of 35%, a
blank corridor factor as no corridor and a blank surrender charge as none. Here the cap on
the mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing, as
`UL_US_S` does; written `min(1.0, q)` it would read one as 1.0, every policy dying in that
month. Each is refused.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`UL_US_S` and its table by `tests/sec_support.py`, from the `UL_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `UL_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py UL_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 2 | twin | S points 1 and 2 | issued at `t = 0`: `UL_US_S`'s worked example on Option A, and the same policy on Option B, which runs into permanent shortfall in policy year 57 |
| 3 | twin | S point 3 | `UL_US_S`'s in-force cell, in force 120 months, on the anniversary opening policy year 11, with 15,000.00 of account value and a 2,000.00 loan |
| 4 | derived | S point 1 at S month 12 | on its first anniversary, inside the surrender-charge period: 1,244.21 of account value and 1,800.00 of premiums paid |
| 5 | derived | S point 1 at S month 113 | in policy year 10, the lapse-shock year, its surrender charge run off: the shock runs to `t = 6`, and policy year 11 begins at `t = 7` |
| 6 | derived | S point 3 at S month 6 | the in-force cell six months on, in force 126 months, mid-year with its loan: 15,755.09 of account value and a loan of 2,027.31 |
| 7 | derived | S point 2 at S month 676 | Option B in the month its permanent shortfall begins, policy year 57, attained age 91, with 309.04 of account value |
| 8 | derived | S point 1 at S month 1,008 | the first month at attained age 119, where the mortality rate reaches 1.0: every survivor dies at `t = 0`, and the frame's 23 later rows are zeros |
| 9 | future | S point 1, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `UL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `UL_US_S` carries into it, each column read as
`UL_US_S`'s own formulas read it: the account value as `av_pp_at(d, "BEF_PREM")`, the loan
as `loan_bal_pp_bom(d)`, the face as `sum_assured_at(d − 1)`, the year's usage as
`wd_used_year(d)`, the premiums less withdrawals as `cum_prem_pp(d − 1)` and the MEC latch
as `is_mec(d − 1)`. So the row continues the S projection from there: point 4 opens with
0.939317 policies, and point 8 with 1.765e-10. Point 6's premiums to date, 720.00, are the
six months' since `UL_US_S`'s first month, because `UL_US_S` counts its in-force point's
premiums from there; an extract carries every premium since issue. A derived row's
`policy_id` is the S row's with the month appended, `UL-000001-M12`, and a future row's
carries the months to issue, `UL-000001-F25`. Row `t` of a generated point is month
`t + source_mth` of its S point. All nine are on the anchor configuration M35 / StdNT /
$100,000, because the specimen gives a guaranteed COI scale for that cell alone [S3], so a
point on any other issue age, sex or class needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `UL_US_S` already names:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_MAT"`, the count before any maturity, `UL_US_S`'s meaning: the `"BEF_DECR"` count,
  since the contract never matures and no event of the month separates the two.

Any other timing raises. `UL_US_S`'s cell of the name returns `pols_if(t)` for every
timing, and nothing calls it. `"BEF_NB"` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `UL_US_S` counts the issued policies, and this model counts them as new
business, not yet in. Each S model's `"BEF_MAT"` keeps that model's meaning, and
`basiclife/BasicTerm_SE`'s, the count at the start of the month before its new business,
is not adopted: `WholeLife_US_SEC`'s is the end of its month, after the surrenders, and
this model's the start of the month, after its new business.

The survivors carried into month `t` are those of month `t − 1`'s `"BEF_DECR"` count, which
`"BEF_NB"` forms itself, as its own value at `t − 1` plus that month's new business, less
that month's deaths and lapses in the order `pols_death` and `pols_lapse` take them. The
account value and the loan are carried the same way. `av_pp_at(t, "BEF_PREM")` forms month
`t − 1`'s closing balance itself, from its own value at `t − 1` and month `t − 1`'s net
premium, withdrawal, fee, deduction and interest, the same sum in the same order as
`av_pp(t − 1)`, and `loan_bal_pp_bom(t)` accrues a month's loan interest on its own value at
`t − 1`, as `loan_bal_pp(t − 1)` does. The face, the year's usage and the premiums to date
each call themselves at `t − 1` before anything else, and the MEC latch does once its
in-year test, which reads the same month's premiums to date, has run. So every chain of
calls from month `t` back to `t_entry()` is one cell a month, where `UL_US_S`'s account
value ran through five cells a month and its loan through two. A cold `net_cf` in the last
month of point 1's 1,032-month frame runs 1,047 cells deep and needs modelx's recursion
limit at 1,046, against 5,166 for `UL_US_S`'s point 1, and point 3's 912-month frame needs
926: 16 cells above the chain back to `t_entry()`, the deepest of them month 0's COI rate,
its extent, the check of the COI table and its read. At the longest cover the
contract allows, issue age 18 and 1,236 months, it runs 1,251 deep and needs 1,250, whether
the policy is issued at the valuation date or 120 months after it, because every chain
stops at the issue month: about 311 KiB of C stack at gcc's 255 bytes a level. Each report
evaluates its columns in ascending `t`, and every committed point's reports and checks run
that way under a limit of 15, as `UL_US_S`'s do.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `UL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < omega_mth()`, where
`omega_mth() = 12 × (121 − age_at_entry)` is `UL_US_S`'s frame from issue, the first month
at attained age 121. Outside it, before issue and from `t = proj_len()` on, every count,
premium, withdrawal, charge, decrement rate, claim and cash flow is zero and every flag
false; only the two clocks, the inputs read on the valuation clock and the lapse shock's
neutral 1.0 hold values there, and the month after the frame holds one exception more,
below. No count evaluates a decrement rate there, and no table is read at a policy year or
an attained age the policy does not have: `prem_persistency`, `premium_pp`, `wd_pp`,
`wd_used_year`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`,
`maint_fee_pp`, `loan_bal_pp_bom`, `surr_charge_rate`, `cum_prem_pp`, `gpt_limit`,
`seven_pay_limit`, `mort_rate`, `lapse_rate_base`, `pols_death`, `pols_lapse` and
`expenses` are zero, and `gpt_ok` and `is_mec` false, before any table or rate is read,
and every other value is zero through them. `lapse_rate_sc_mult` is 1.0 there, before it
compares the policy year with the shock year: a point with no surrender charge has the
shock year 0, and before issue the valuation clock reaches policy year 0. Each table read
at a policy year or an attained age has one reader keyed by it, called inside cover only,
so on point 9, whose policy year is −2 at `t = 0`, no reader holds a key below policy year
1 or attained age 35.

**The end of the projection.** The frame ends at `omega_mth()` because the mortality table
ends at attained age 120, not at an event of the contract, which never matures. With the
shipped table, whose annual rate is 1.0 at ages 119 and 120, and a class factor and an A/E
of 1 or more, every life has died by the end of the first month at attained age 119:
point 8, valued in that month, loses its last 1.765e-10 of a policy at `t = 0`. With a
preferred class, an A/E below 1 or a table that stays below 1, lives survive the last
month, and `UL_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and `av_change()`
read the account value in force entering month `t + 1`, which in the last month is
`t = proj_len()`. So the two opening values read there, the count carried in
(`pols_if_at(t, "BEF_NB")`, and through it `pols_if(t)`) and the account value carried in
(`av_pp_at(t, "BEF_PREM")`), are defined for `0 ≤ duration_mth(t) ≤ omega_mth()`: in the
month after the frame they are the survivors of the last month and the account value they
carry, `UL_US_S`'s own values there. Everything else is zero or false there, the expenses
included, which would otherwise fall on the carried count, and nothing reads past it:
`av_change()` and the checks' two residual cells, which read `t + 1`, are zero outside
cover before they read it. At the shipped assumptions the survivors at `proj_len()` are
exactly 0.0 on every committed point. Under the splice's References, an A/E of 0.56 among
them, they are 4.02e-6 of a policy on the twins of points 1 and 2 and 9.27e-6 on the twin of
point 3, equal to `UL_US_S`'s, and both checks close.

## The opening state

`UL_US_S` opens its in-force point 3 from two columns, the account value and the loan
entering its first month, and takes the rest as they stand at issue: the face at issue,
none of the year's free allowance used, no premium paid, and the MEC latch off. Point 3
needs no more, since it withdraws nothing and pays inside every limit, and its twin opens
the same way. A policy valued in any month of its life needs all six columns, each what
`UL_US_S` carries into that month. The committed points show the first two: point 6, the
in-force cell six months on, opens with 15,755.09 of account value and a loan of 2,027.31,
where `UL_US_S`'s columns hold the 15,000.00 and 2,000.00 of six months before; month 0's
roll-forward, interest credit, shortfall test and death claim read them.

On the committed points the other four columns show nothing: they withdraw nothing and pay
level premiums inside every limit, so the face stays at issue, no allowance is used, the
latch stays off, and no level premium reads the premiums paid. Each shows instead on a
variant that the splice restates in force (tests below), `UL_US_S`'s point 1 with a few of
its columns changed, in a copy of the tables that gives the variant's class COI rows of its
own, beside the same row with the column as `UL_US_S` assumes it, zero, or the face at issue
for the face:

- **`cum_prem_init`.** The TARGET variant, `UL_US_S`'s point 1 planning $6,000 a year,
  restated at month 71, in policy year 6. Its premiums to date, 33,750.00, leave 388.15 of
  room under the GPT limit, the guideline single premium of 34,138.15, so it collects
  388.15 at `t = 0` and nothing more in the year. With the column at 0 it would collect its
  level 450.00 at once, and 5,290.00 over the twelve months.
- **`is_mec_init`.** The single-premium variant, $50,000 capped at the guideline single
  premium, restated at month 85, in policy year 8. It failed the 7-pay test in its issue
  month, and the in-year test no longer applies, so `is_mec(0)` is true from the latch
  alone. With the column at 0 it would be false.
- **`wd_used_year_init`.** The withdrawal variant, `UL_US_S`'s point 1 withdrawing $60 a
  month from its first anniversary, restated at month 13. The year's first withdrawal has
  used 60.00 of its free allowance, so month 0's free amount is 82.39 where 10% of the
  account value is 142.39, and at `t = 1` the year's third withdrawal exceeds what is
  left of it and cuts the face by 35.66, to 99,964.34. With the column at 0 the free amount
  would be 142.39, and the first cut would come a month later.
- **`sum_assured_init`.** The same variant restated at month 24, its second anniversary.
  A year of withdrawals has cut the face to 99,442.27, and that is the death benefit of
  month 0; read as the face at issue, it would be 100,000.00. The surrender charge is
  691.67 either way, because it is quoted on the face at issue.

The in-year test runs before the latch looks back, in the valuation month as in every
other, so a policy that fails the test at `t = 0` is a MEC from then on, whatever
`is_mec_init` says. The over-funded variant, planning $24,000 a year and restated at month
3, has paid 6,000.00, inside the first year's 7-pay limit of 6,702.10, so its
`is_mec_init` is 0, and month 0's 2,000.00 takes it to 8,000.00: `is_mec(0)` is true.

## Departures from UL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year or an attained age answers
for the months outside cover. Of `UL_US_S`'s 107 cells in `Projection`, 45 are unchanged,
one of them, `lapse_rate_dyn_mult`, with a line re-wrapped, 26 have a new docstring only,
most of them to say what `t` now counts, and 36 are rewritten. None is removed or renamed,
and 26 cells are new, 133 in all. A cell of `UL_US_S`'s that this model lacked would fail
the twin identity. Of `Data`'s nine, `model_point_table` is rewritten to check the table as
it reads it, and nine cells are new, eighteen in all: the extents of the five tables read
at a policy year or an attained age, each of which checks its table's keys and rates, and
`class_count` and `surr_charge_count`, which check the class factors and the
surrender-charge schedules.

| Cells | `UL_US_S` | `UL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `omega_mth` | `12 × (omega_age − x + 1) − duration_mth_init()`, the months from the first projected month | `omega_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the end of the projection | `omega_mth()` is new and is `UL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left has no frame |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`; `"BEF_NB"` the count before the month's new business, and `"BEF_MAT"` the `"BEF_DECR"` count, as in `UL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `av_pp_at` (`"BEF_PREM"`), `loan_bal_pp_bom` | `av_pp_init()` and `loan_bal_init()` at `t = 0`, then `av_pp(t − 1)` and `loan_bal_pp(t − 1)`: chains of five cells a month and of two | the same openings at `t_entry()`, then the previous month's close formed in the cell itself, `UL_US_S`'s arithmetic in its order | Every chain one cell a month, since a compiled model runs it on the C stack |
| `sum_assured_at`, `wd_used_year`, `cum_prem_pp`, `is_mec`, `premium_pp` | opened at `t = 0` at the face at issue, 0, 0 and `False`, and the TARGET cap's premiums to date at 0 | opened at `t_entry()` from `sum_assured_init()`, `wd_used_year_init()`, `cum_prem_init()` and `is_mec_init()` on a point in force, and from the issue values on any other | A policy in force brings in its face, the year's withdrawals, its premiums and its MEC status |
| `prem_persistency`, `coi_rate_guar`, `lapse_rate_base`, `corridor_factor`, `mort_rate` | the table read in the monthly cell, at `policy_year(t)` or `age(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the year or the age — `prem_persistency_py`, `coi_rate_guar_py`, `lapse_rate_base_py`, `corridor_factor_at`, `mort_rate_base_at` — with `UL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the rates, called inside cover only | No table is read at a year or an age the policy does not have, each is read once a year or an age, and a blank, text or fractional key, keys that repeat or leave a gap and a rate that is not a number are refused by name, where `UL_US_S`'s extent skips a blank key and cuts the table short, and a blank rate is a missing value |
| `surr_charge_rate`, `lapse_shock_year` | the schedule's row read in each | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one reader for each of the schedule's two columns, each asking `data.surr_charge_count()` first, which checks the table | The same numbers for any schedule, with no table read in a monthly cell; a blank charge, which `UL_US_S`'s `max` reads as no charge, is refused |
| `premium_pp`, `db_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `db_option()` and `qual_test()` | branches on six decodes, `is_level_premium()`, `is_single_premium()`, `is_target_premium()`, `is_db_option_a()`, `is_db_option_b()` and `is_gpt()` | No monthly cell compares text. The label accessors stay for reporting, and an unknown value still raises |
| `class_factor` | the factor of the point's class, read from the table | the same, once `data.class_count()` has checked the table's classes and factors | A blank factor, a missing value to `UL_US_S`, would reach the cap on `mort_rate`, `min(q, 1.0)`, which keeps it missing |
| `prem_persistency`, `premium_pp`, `wd_pp`, `wd_used_year`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `maint_fee_pp`, `surr_charge_rate`, `cum_prem_pp`, `gpt_limit`, `gpt_ok`, `seven_pay_limit`, `is_mec`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult` | unguarded: no `UL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_sc_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2, and policy year 0 is the shock year of a point with no surrender charge. At `t = proj_len()` nothing is charged, paid or withdrawn, whatever `omega_age` and `charges_cease_age` are set to |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `inflation_factor` | `1.025^(policy_year(t) − 1)`, stepping on the policy anniversaries | `1.025^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_margin` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)` and `check_margin_resid(t)`; a residual that is not a number fails | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the loan term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers | The lapse claim is the net cash value floored at 0, so once a loan exceeds the cash value `UL_US_S`'s identity is off by `(CSV(t) − L(t)) × pols_lapse(t)` and its check fails on a projection that is right; on every shipped point the cash value covers the loan, and the two agree |
| `wd_pp` | the model point's `wd_pp` column read in the monthly cell | read once a point, by `wd_pp_mth()` | A monthly cell the account value's chain reads reads no table |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`, the four
new opening-state accessors, `coi_rate_last_year`, the extent of a point's COI scale, and
`wd_pp_mth`, the withdrawal column read once a point.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 3's
`expenses(t)` is `UL_US_S`'s divided by `1.025^10`, about 1.280, at every `t`: both models
step on its anniversaries. Its other cash flows, its counts and its account value
roll-forward are `UL_US_S`'s from month 0 on. Point 9 is `UL_US_S`'s point 1 twenty-five
months on in those columns too. Its maintenance expense is `1.025^2` above `UL_US_S`'s,
and `1.025^3` in the last month of each policy year, where the valuation year has stepped
and the policy year has not.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 and 2, issued
  at the valuation date, every cell of `UL_US_S`'s agrees at every argument `UL_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`,
  whose meaning changed, and a cell this model lacked would fail it. So the goldens
  `tests/test_universal_life_us.py` asserts on those points — every cell of the worked
  example's three rows to the cent, the issue-month trace at full precision, the pitfalls,
  the shortfall table of point 2 — hold here with no number restated. The identity holds
  on any count, since `UL_US_S` already charges acquisition on the policies issued. The
  same suite holds the model to the conventions every `_SEC` model meets: every frame
  starts at `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The splice**, in `tests/test_universal_life_us_sec.py`: each `UL_US_S` point restated in
  force at a month either side of its events continues the S projection, in `result_cf`,
  `result_pols` and `result_av`, column by column, and in every other cell the two share, to
  1e-9, but those the twin identity skips, `pols_if_init` and `model_point`, the accessors
  of the S point's own opening, `duration_mth_init`, `av_pp_init` and `loan_bal_init`, whose
  values are `UL_US_S`'s at its first month, and `proj_len`, which counts from another first
  month. Points 1 and 2 are restated at months 1, 11, 12 and 13, around the first
  anniversary; at 107, the first month without a surrender charge, and 108, 113 and 119,
  inside the lapse-shock year; at 120, where the shock ends and the per-unit charge steps
  down; and at 125. Point 2 is restated at 676 too, where its shortfall begins, point 1 at
  1,031, its last covered month, whose `t = 1` is the month the survivors are carried into,
  and at 779 and 780, either side of the attained age at which the splice's charges cease,
  and point 3 at 1, 6 and 12, besides its own twin from `UL_US_S`'s month 0. So are variants
  of S's points, in a copy of S's table that is never committed, each with its own COI rows,
  for branches S's own points do not reach, each at the months its own events need:
  withdrawals on Option A and on Option B, a single premium with no surrender charge, a
  TARGET premium on a second surrender-charge schedule, an over-funded level premium,
  restated among others in the month it fails the 7-pay test, issue age 18, the longest
  cover, in its last month too, and a level premium of $24,000 a year on Option B, whose
  account value outgrows the face, restated either side of the months the corridor starts
  and stops binding. Between them they carry both sexes and every class. Inflation, the one
  input on the valuation clock that moves a number, is set to 0 in both models, and the
  rest is set in both to reach what the shipped values leave unreached: an acquisition
  expense of $250; the mortality A/E at 0.56, which leaves survivors at the end of every
  frame, so the count and the account value carried into `proj_len()` are compared on every
  row; charges ceasing at attained age 100, inside every frame, where the shipped 121 is
  past the table's last age; and the lapse shock at 10 times, so that the shock year's rate
  meets the lapse rate's cap of 35%.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column, every kind of valuation month and every premium type, the corridor on either
  option, the lapse rate's cap and charges ceasing in cover among them, and a test asserts
  that they do; the premium is monthly in every case, the only mode the model has. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs the
  full grid too.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point
  is the S projection moved on, cell by cell, the count at each of its timings among them
  but the count before new business in the issue month, which `UL_US_S`'s cell counts as
  in force; with zeros before issue in `result_cf`, `result_pols` and `result_av` and no
  decrement rate evaluated there; and so is each variant issued 13 months on, whose months
  before issue reach policy year −1.
- **How it computes**: on every row the splice and the future business compare, after every
  report, no cell has been called at a negative month, none evaluated from `t_entry()` on
  has read a month before it, and none evaluated at month `t` has read a month later than
  `t + 1`. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, because the policy clock is a closed form, and every point's reports
  run under modelx's recursion limit lowered to 40, which a recursion backward over the
  frame would exceed. And every chain is called cold, on a fresh read, in the last month of
  the twins of points 1 and 3 and at the longest cover, issue age 18, issued now and 120
  months on: `net_cf` first, then each chain's head alone, the loan's, the face's, the
  premiums', the latch's and the count's among them, and modelx's stack trace counts no more
  than one cell a month back to `t_entry()` and a fixed overhead, which a chain of two cells
  a month would exceed.
- **Counts, validation and regeneration**: the roll-forward closes, the last month included,
  `"BEF_MAT"` is the `"BEF_DECR"` count, and `pols_if_at` refuses a timing it does not have;
  `result_pols()` is `UL_US_S`'s, column for column, with `pols_new_biz` beside it; doubling
  `policy_count` doubles every cash flow and moves no per-policy value; each malformed row
  is refused naming its point, a count blank, text, negative or infinite, a duration blank,
  text, fractional or beyond the horizon, an opening-state column missing, blank, text,
  negative, infinite or set on a policy not yet in force, a MEC latch that is no int code, a
  face of zero in force or above the face at issue, a year's usage on an anniversary and a
  latch missing after a failure among them; each assumption table read at a policy year or
  an age is refused naming its file and column, with the lines of a key that is blank, text
  or fractional, or with each key that repeats, its lines, and each that is missing, where
  the keys repeat, leave a gap, miss policy year 1 or have no row, and so is the first
  projection of a point that reads it; so is a rate of those tables, a class factor or a
  surrender-charge value that is blank, text or infinite, with its lines, and a class or a
  schedule blank or on two rows; a `db_option`, `qual_test` or `premium_type` no decode
  knows raises `UL_US_S`'s message; the horizon is a Reference, which at 0 refuses any
  future business, saying so; a point at or past the end of the projection is refused by
  `proj_len()`, and `run_sec.py --block` refuses it before printing anything; a zero count,
  durations and the MEC latch written as floats, the face, the usage and the premiums to
  date written as whole numbers, the keys of the five keyed tables written as floats, a
  policy issued 120 months on, rows either side of the first anniversary and of the seventh
  policy year, a reduced face and a negative `cum_prem_init` are accepted; the committed
  table is what `UL_US_S` generates, and each of its derived and future rows projects its S
  point's three reports from its month on, to 1e-9, which pins the committed counts more
  tightly than the table's own comparison, 1e-12 absolute.
- **The opening state and the rest**: the twin of point 3 is `UL_US_S`'s point 3 from month
  0 on, at the shipped assumptions, in every cell but those expense inflation moves, which
  carries `UL_US_S`'s goldens on it over; the variants carry the premiums paid, the latch,
  the year's usage and the face as above, and with the column as `UL_US_S` assumes it give
  the 450.00, the `False`, the 142.39 and the 100,000.00 above; expense inflation runs on
  the valuation clock at the shipped 2.5%, and the declared rates, overridden to move, are
  one number for every point in each month, which only these tests see, and on those paths
  the account value entering each month is the close of the month before, both checks hold,
  and the twins of S's points 1 and 3 project what `UL_US_S` projects on the same paths,
  the dynamic lapse multiplier above 1 throughout; a check whose residual is not a number
  fails; on S's in-force point withdrawing on Option B, whose loan comes to exceed its cash
  value, both checks hold where `UL_US_S`'s margin identity fails; acquisition falls on new
  business alone; a tobacco point at the shipped A/E, as new business and restated in force
  the month before the cap, is `UL_US_S`'s in every cell, the capped months included, to
  1e-9 with no absolute floor, and on those rows and one restated inside the capped year,
  from `t = 936` at issue, attained age 113, where the cap first binds, its rate is the
  float 1.0 in both models, every life in force dies in that month, nothing is in force
  after it, and its numbers are real and finite, with both checks closing; a NaN sent to
  the cap, through `class_factor`'s formula replaced, stays NaN; every monthly cell holds
  its value outside cover and reads no table there, before issue and at `proj_len()`; the
  points of a block sum row by row; an extract without the generator's three columns,
  relabelled, projects the same numbers; and `run_sec.py` prints the model's numbers, for
  a point issued at the valuation date, a point restated, a point to be issued and the
  block.

```bash
python -m pytest tests/test_universal_life_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_universal_life_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k "[UL_US_SEC]"
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
