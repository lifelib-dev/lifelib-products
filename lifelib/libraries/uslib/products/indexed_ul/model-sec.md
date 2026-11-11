# In-Force Implementation Notes

**Status:** Draft, 2026-11-10. `IUL_US_SEC` is [`IUL_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year and with up to twelve index segments live,
and policies to be written in the ten years after it, as lifelib's `basiclife/BasicTerm_SE`
extends `basiclife/BasicTerm_S`. The product is the one
[`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in
`BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is
still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `IUL_US_S` on another time axis, and it reads `IUL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced: the 10.00% current
> and 2.00% guaranteed caps, the 100% participation and the 0% floor of the Benchmark
> Index Account [S2] [R1], the 4.50% current and 1.00% guaranteed fixed-account rates
> [S2], the monthly ladder of 1-year S&P 500 point-to-point segments, up to twelve live at
> once [S2] [S3] [S4], the $10 policy fee [S3] [S5], the $25 withdrawal fee [S3], the
> cumulative-MNLP no-lapse test [S3] [S4], the 10-year surrender charge period
> [S1] [S5] [S7] and the IRC 7702(d) corridor factors [R4]. Every behavioural and expense
> assumption, the whole COI scale, the surrender charge dollars, the per-unit charge and
> **the 6.40% level index return** are **[std]** standardizations introduced for the
> reference implementation. Replace them with company data before drawing any conclusion
> from the numbers.

## Run it

```bash
python products/indexed_ul/run_sec.py            # point 1: S point 1, issued now
python products/indexed_ul/run_sec.py 7          # point 7: S point 4 in force 65 months
python products/indexed_ul/run_sec.py --block    # every model point, summed row by row
```

The first prints, as rows `t = 0 … 11`, the cash flows, the account value roll-forward,
the segment ladder and the counts behind them for point 1, `IUL_US_S`'s baseline cell
issued at the valuation date: its cash flows, its account values and its segment ladder
are the numbers `run.py` prints for `IUL_US_S`'s point 1 in the same months. The second
prints point 7, `IUL_US_S`'s monthly payer restated 65 months after its issue. It brings
in all twelve of its live segments, and one of them matures in each of its first twelve
rows: the one in slot 12 at `t = 0`, credited 233.73 a policy, 6.40% of its 3,652.04.
Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/indexed_ul/IUL_US_SEC")
model.Projection[7].result_seg()
```

`Projection` takes a `point_id`, as in `IUL_US_S`. Its four result tables are indexed by
`t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `IUL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes`, `net_loan_cf` and `net_cf` — income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `IUL_US_S`'s per-policy account value roll-forward, in the notes' processing order, then the surrender charge, the net cash surrender value and the loan, with zeros before issue |
| `result_seg()` | `IUL_US_S`'s segment ladder, per policy: the index level, the fixed account, the month's sweep into a new segment, the live segments' total and count, the credit of the segment maturing in the month and the return behind it, and the loan collateral; the index level is on the valuation clock (*Two clocks*, below) |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `IUL_US_S`'s two monthly decrement rates, written 0 outside cover |

`IUL_US_S`'s four self-checks, `check_av_components()`, `check_av_roll_fwd()`,
`check_seg_ladder()` and `check_margin()`, run over the same frame and hold on every
committed point, `IUL_US_S`'s point 5 and the three rows restated from it included, where
`IUL_US_S`'s own `check_margin()` fails from policy month 383 (*Departures*, below).

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`, then a
collection), so the run holds the cells of one point at a time. It prints where each point
stands at the valuation date — its months in force, policy year, attained age and count;
its account value and the three parts of it, the fixed account, the live segments and the
loan collateral; its loan, face in force, premiums paid, no-lapse accumulator and MEC
status — then the block's first twelve rows and the block summed into projection years,
`pols_if` the count entering each. The committed block opens with 7.67 policies,
44,514.67 of premiums and a net cash flow of 41,034.86. A label not in the table, or not a
number, stops the runner with the table's labels and no traceback.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the first month at attained age 121.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' own month index from issue, and the
  contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1` and `age(t) = age_at_entry() + duration(t)`, as in
  `IUL_US_S`. `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion
  as long as the frame; the closed form needs no such chain of calls.

`IUL_US_S` already counts its months from the start of its own projection, and opens a
point whose `duration_mth` is above 0 there, from its account value and its loan. But it
ships no such point, and its entry loses what a policy's past has left it: it puts the
whole account value less the loan in the fixed account, opens the loan collateral at the
loan, the face at issue and both premium accumulators at 0, and has no index segment
before its first month. Re-opened that way at its month 60, `IUL_US_S`'s point 4 closes
its month 71, eleven months on, with 50,921.66 of account value where its own projection
holds 53,730.24, about 5% short, and reads its no-lapse guarantee as failed where its own
projection holds it in effect. What the valuation clock adds is that `t = 0` is one instant
for every point, that a point may be issued after it, and that a point in force brings in
its whole state, its live index segments among it (*The opening state*, below).

Point 7 is `IUL_US_S`'s point 4, the monthly payer, restated at its month 65. At `t = 0`
it is five months into policy year 6, at attained age 50, with all twelve segments live,
and its frame has 847 rows, `t = 0 … 846`. Its anniversaries fall at `t = 7, 19, …`, where
the attained age steps to 51 and the premium persistency from 0.98⁵ to 0.98⁶. Point 12 is
`IUL_US_S`'s point 4 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first monthly premium, $833.33, falls at `t = 25`, and its frame has 937 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the anniversary premium, `duration_mth(t) % 12 == 0`, and the premium persistency, 0.98 to the policy years completed; withdrawals from policy year 2 and loans at each anniversary from policy year 21; a segment's creation, in the month of the sweep that makes it, and its maturity twelve policy months later, before which the trailing credited rate is the fixed-account rate; the surrender charge by policy month and the lapse spike in the policy year after it; the COI scale, the base lapse rate, the per-unit charge and the collateral's credited rate by policy year; the mortality rate and the corridor factor at the attained age; the no-lapse period, its test against the minimum premium counted from issue, and the shock at its expiry; the GPT limit and the 7-pay test's seven years; premiums, withdrawals and charges ceasing at `charges_cease_age`, and the projection ending at `maturity_age`, both 121 | the index path, `index_level(t)`, from `index_level_init` at the valuation date; the cap in force, `index_cap_at(t)`, and the fixed-account rate, `fixed_rate_ann(t)`, each level as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 0 as shipped |

**The index path.** `IUL_US_S` grows the index at its level return along its own months,
`index_level(t) = index_level_init × (1 + index_return_ann)^(duration_mth(t) / 12)`: a
path of each point's own from its issue, which is one path for every point it ships, all
issued at its `t = 0`. Here the path runs on the valuation clock,
`index_level_init × (1 + index_return_ann)^(t / 12)`, one path for every point of a block,
as a historical or simulated path would be: `index_level_init`, 4,500.00 as shipped, is its
level at the valuation date. A segment's credit is a ratio of two levels, its level at
maturity over its level at its creation, so the path's clock moves no credit as long as
both levels are on the same path. A segment created in the frame, at month `t − 12`,
starts from `index_level(t − 12)`; one created before the valuation date carries its start
level in its ladder row, on this model's path: `IUL_US_S`'s level at the segment's
creation, times `index_level_init` over `IUL_US_S`'s level at the valuation date. On
point 7 the segment maturing at `t = 0` started from 4,229.32, where `IUL_US_S`'s started
from 5,918.41 and matures at 6,297.18: its return is 6.40% either way. What moves is the
level itself: on a point in force `d` months, `index_level(t)` is `IUL_US_S`'s level at its
month `t + d` divided by `(1 + index_return_ann)^(d / 12)`, 1.399374 on point 7, and so is
the `index_level` column of `result_seg()`. Each credit agrees with `IUL_US_S`'s on a
restated row to the rounding of a ratio of two other levels, a few parts in 10¹⁵, and
every other value of the four reports to within 4e-12 relative on the committed rows, but
the credit of a segment drawn to a rounding about zero (*The segment ladder*, below).
`index_level` is the single point of substitution: override it with a path keyed by the
months from the valuation date, and every segment created in the frame follows it, while
one created before the valuation date reads its start level from its ladder row, which
must then be on the same path.

The cap in force and the fixed-account rate are economic inputs too, read at `t`: a
re-declared rate applies to every point from the month it is declared, and a re-declared
cap to every segment created from that month on, since a segment keeps the cap declared at
its creation (`seg_index_cap(t)`, the ladder's `seg_index_cap_init` for a segment created
before the valuation date). As shipped both are level, 10.00% and 4.50%, so their clock
shows in no number. Expense inflation keeps `IUL_US_S`'s step by year and moves it onto
`t`, so that the maintenance expense would be in valuation-date dollars, for every point
alike; it ships at 0, as in `IUL_US_S`, and moves no number either. Switched on, a point in
force bears `IUL_US_S`'s maintenance expense times
`(1 + inflation_rate)^(t // 12 − (y − 1))`, `y` its policy year in the month, both models
stepping on their own anniversaries. Acquisition, $150 a policy in the issue month, is
charged per policy issued and not inflated, as in `basiclife/BasicTerm_SE`: `IUL_US_S`
charges it on the policies in force in the issue month, which are the policies issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`IUL_US_S` computes, whatever the point's count. On `IUL_US_S`'s five points, all new
business, every cash flow and every count agrees, and so does every other cell the two
models share, at every argument `IUL_US_S`'s own sweep evaluates, bit for bit, but four
whose meaning changed: `pols_if_init()`, now the count already in force at the valuation
date, 0 for new business; `model_point()`, a row of another table; `result_pols()`, which
gains `pols_new_biz`; and `check_margin()`, whose identity this model states with the debt
a surrender recovers (*Departures*, below), and which holds on point 5, where
`IUL_US_S`'s fails.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `IUL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and ten of its columns are the in-force interface:
`basiclife/BasicTerm_SE`'s two, and eight that open an in-force policy's state, two of
them `IUL_US_S`'s own. The live index segments are a companion table,
`inforce_segments_sec.csv`, one row a segment (below). Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, of either sign | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value: the fixed account, the live segments and the loan collateral |
| `loan_bal_init` | dollars, 0 or more | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `fa_pp_init` | dollars, of either sign | the start of month 0 | the fixed (holding) account, which an exhausted policy runs below 0 |
| `lca_pp_init` | dollars, 0 or more, above 0 exactly where the loan is | the start of month 0 | the loan collateral account, part of the account value, as the debt is not |
| `sum_assured_init` | dollars of face, 0 to `sum_assured` | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date |
| `cum_prem_init` | dollars, of either sign | the start of month 0 | the gross premiums paid from issue to policy month `duration_mth − 1`, less every withdrawal, which the GPT test, the 7-pay test and the TARGET premium cap read |
| `cum_prem_net_init` | dollars, of either sign, at most `cum_prem_init` | the start of month 0 | the same less every loan drawn: the no-lapse guarantee's accumulator |
| `is_mec_init` | an int code: 0, not a MEC; 1, a MEC | the start of month 0: the latch after policy month `duration_mth − 1`'s 7-pay test | whether the policy has failed the 7-pay test, and so is a modified endowment contract for good |

The eight state columns are 0 on a point issued at or after the valuation date: it is
issued at the face `sum_assured`, with no account value, no loan, nothing paid and no MEC
status, and with no segment. `av_pp_init` and `loan_bal_init` are `IUL_US_S`'s own columns:
they already measure the account value and the loan entering `IUL_US_S`'s first month, so
they keep their names. Each new column is named for the cell it opens, with `_init` added:
`fa_pp_init` for `fa_pp_at`, `lca_pp_init` for `lca_pp_at`, `sum_assured_init` for
`sum_assured_at`, `cum_prem_init` for `cum_prem_pp`, as in `UL_US_SEC`,
`cum_prem_net_init` for `cum_prem_net_pp` and `is_mec_init` for `is_mec`. No quantity of
the product is read at the last anniversary, so none needs a column at a second instant:
at a mid-year valuation the year's anniversary premium and loan draw are already inside the
two accumulators and the loan.

**The segment ladder.** `inforce_segments_sec.csv` holds, for each point in force, one row
for each of its last `min(12, duration_mth)` policy months, a month whose sweep made a
segment of nothing, or whose segment has since been drawn to nothing, included:

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `point_id` | a label, a point of the table | — | the point the segment belongs to; nothing else in the file names one |
| `slot` | whole months, 1 to 12 | the valuation date | the months since the segment's creation: slot `k` was created in policy month `duration_mth − k`, and slot 12 matures at `t = 0` |
| `seg_bal_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the segment's balance |
| `seg_ded_cum_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the monthly deductions charged to it since its creation |
| `seg_wd_cum_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the withdrawals and loan transfers drawn from it since its creation |
| `seg_index_start_init` | index points, above 0 | the segment's creation | the index level it started from, on this model's path, whose level at the valuation date is `index_level_init` |
| `seg_index_cap_init` | a rate, 0 or more | the segment's creation | the cap declared then, at which its credit at maturity is capped |

A point not yet in force holds no row. A segment's balance, deductions and draws are its
credit base, and its creation balance takes no column: nothing may enter or leave a
segment but a deduction, a withdrawal or a loan transfer, since segments earn no interim
interest, so it is the three summed, the closure `IUL_US_S`'s own ladder check asserts
(*The segment ladder*, below). The ladder is long, a row a segment, rather than sixty
columns of the model point table, and it is read by a `Data` reader of its own,
`inforce_segments()`, which no reader of `IUL_US_S`'s could serve.

| `IUL_US_S` | `IUL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 on every shipped point, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `loan_bal_init` | the same | `IUL_US_S` already opens an in-force point from them |
| — | `fa_pp_init` | `IUL_US_S` opens the fixed account at the account value less the loan |
| — | `lca_pp_init` | `IUL_US_S` opens the loan collateral at the loan |
| — | `sum_assured_init` | `IUL_US_S` opens every point at the face at issue, `sum_assured` |
| — | `cum_prem_init`, `cum_prem_net_init` | `IUL_US_S` opens both accumulators at 0 at its `t = 0` |
| — | `is_mec_init` | `IUL_US_S`'s flag is the 7-pay test of the month alone, and does not latch |
| — | `inforce_segments_sec.csv` | No segment of `IUL_US_S`'s can predate its `t = 0` |

On the twins the six new columns take what `IUL_US_S` itself assumes on new business, 0,
and `IUL_US_S`'s two are as its table has them, 0 on every shipped point, so each twin
opens as its S row does, and holds no ladder row.

The columns carried over are read as `IUL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the plans for premiums, withdrawals and loans
and the allocation excepted, which hold over the frame:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `IUL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the face a policy is issued at, and the surrender charge's base, whatever withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL`, `SINGLE` or `TARGET` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_mode` | `ANNUAL` or `MONTHLY` | the mode over the frame; an annual premium falls on the policy anniversary |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, before the premium persistency |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `index_alloc_rate` | a fraction of the fixed account | the share each month's sweep moves into a new segment |
| `wd_pp`, `wd_first_year` | dollars a month; a policy year | the withdrawal taken in every month from that policy year on, gross of its $25 fee; 0 on every shipped point but 5 |
| `loan_new_pp_ann`, `loan_first_year` | dollars a year; a policy year | the standard loan drawn at each anniversary from that policy year on; 0 on every shipped point but 5 |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `mnlp_rate` | dollars a year per $1,000 of face | issue: the minimum no-lapse premium rate |
| `gsp`, `glp`, `seven_pay_prem` | dollars, the compliance inputs | issue |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once, by
twenty rules in turn. The first that fails raises `ValueError`, naming the missing column
or every point that fails it:

- the in-force columns are present, and so is every column of `IUL_US_S`'s own that the
  projection reads as a number or a flag: `age_at_entry`, `wd_first_year`,
  `loan_first_year`, `sum_assured`, `premium_pp_ann`, `wd_pp`, `loan_new_pp_ann`,
  `mnlp_rate`, `gsp`, `glp`, `seven_pay_prem`, `load_prem_rate`, `index_alloc_rate` and
  `has_surr_charge`;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, and −120 or more: "model_point_table_sec.csv:
  duration_mth must be -120 or more, a policy issued at most 120 months after the
  valuation date; it is not at point_id [12]". Future new business is written over a
  horizon, `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer
  than the projection from issue plus ten years: 1,572 months at issue age 0, the youngest
  the product issues, and 1,032 at 45, the only issue age the shipped COI scale carries.
  Set to 0, the Reference refuses future new business altogether, and a negative horizon
  is itself refused;
- `age_at_entry` is a whole number of years, 0 or more, and `wd_first_year` and
  `loan_first_year` each a whole number of policy years, 1 or more: `IUL_US_S` takes the
  `int()` of each, so a fraction would move an age or a first year without a word;
- `sum_assured`, the face at issue, is a number above 0, and `premium_pp_ann`, `wd_pp`,
  `loan_new_pp_ann`, `mnlp_rate`, `gsp`, `glp` and `seven_pay_prem` are each a number, zero
  or more: the guideline limit's `max` and the single premium's `min` read `gsp` and
  `glp`, and would lose a blank one;
- `load_prem_rate` and `index_alloc_rate`, the share of each premium the load takes and
  the share of the fixed account each month's sweep moves into a segment, are numbers from
  0 to 1;
- `has_surr_charge` is `True` or `False`, as pandas reads those words, in any case. A
  blank, a number or any other text is refused: one such value turns the whole column into
  text, where `"False"` is a true string, so that every point would read as carrying a
  surrender charge;
- `av_pp_init` and `fa_pp_init` are each a number, of either sign (*The opening state*,
  below); `lca_pp_init`, `loan_bal_init` and `sum_assured_init` each a number, zero or
  more, a face of 0 in force among them; and `cum_prem_init` and `cum_prem_net_init` each a
  number, of either sign: each is a tax or guarantee measure, not a balance, and
  withdrawals and loans can exceed the premiums paid;
- `is_mec_init` is 0 or 1, an int code; written as 1.0 it reads as `True`;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros:
  "model_point_table_sec.csv: cum_prem_init must be 0 on a policy not yet in force,
  duration_mth 0 or less; it is not at point_id [12]";
- `sum_assured_init` is at most `sum_assured` on a policy in force, since face increases
  are not modelled. A face below it is accepted, whether withdrawals cut it or an elective
  decrease the model does not implement, and it is projected from the value given;
- `lca_pp_init` is above 0 exactly where `loan_bal_init` is: a standard loan moves value
  into the collateral account on the day it is taken, and the model takes no repayment, so
  the two are held together from the loan's first day, each at its own rate;
- `cum_prem_net_init` is at most `cum_prem_init`, to a cent and a half, half a cent for
  each of the two and half a cent more, since loans only lower it;
- `is_mec_init` is 1 wherever the 7-pay test has already failed in the month before the
  valuation date: `cum_prem_init` above `seven_pay_prem` times the policy years to then,
  in the first seven. A failure the premiums to date no longer show, after withdrawals, or
  one on a policy valued after its seventh year, where the test no longer applies, is the
  column's to record, and either value is accepted.

`Data.inforce_segments()` checks the ladder as it reads it, by nine rules in turn, each
naming the lines or the points it fails on:

- the seven columns are present;
- `point_id` and `slot` are each a whole number, read by value;
- each `point_id` is a point of the table: "inforce_segments_sec.csv: point_id [99] on
  line [68] is no point of model_point_table_sec.csv";
- no `point_id` and `slot` appear together twice;
- `slot` is from 1 to its point's `duration_mth`: no segment predates issue, and a point
  not yet in force holds none;
- each balance, deductions and draws are a number, `−1e-8` or more: a draw or a deduction
  that took a segment's whole balance can leave a rounding about zero of either sign,
  which `IUL_US_S` closes on (*The segment ladder*, below) and an extract carried to the
  cent writes as 0; `check_seg_ladder()` holds every live balance to the same `−1e-8`,
  `IUL_US_S`'s tolerance, so a balance `Data` admits is one the check passes;
- each start level is a number above 0, the level the segment's return divides by;
- each cap is a number, zero or more: the credited rate's `min` reads the cap first, and
  would read a blank cap as a credit at the floor, without a word;
- each point's `av_pp_init` is its `fa_pp_init` plus its `lca_pp_init` plus the balances
  of its segments, to half a cent an amount and half a cent more:
  "model_point_table_sec.csv:
  av_pp_init must be fa_pp_init plus lca_pp_init plus the point's segments in
  inforce_segments_sec.csv, to half a cent an amount and half a cent more; it is not at
  point_id [7]". `check_av_components()` holds that identity in every month, and the
  opening state is the close of the month before. The projection opens the account value
  from its parts, the fixed account, the collateral and the ladder's balances, summed slot
  by slot as `seg_bal_active_pp()` sums, not from this column, so an extract carried to
  the cent, whose rounded parts need not sum to its rounded account value, opens one
  account, and the check holds on it, as it does on every committed point carried to the
  cent. The cent slack also covers an exhausted account: at its worst, on S point 5's
  month 906, the account value is −9.81e9 and its parts differ from it by 3.8e-6.

Four kinds of point read, but `proj_len()` refuses each, naming the point, because each is
a rule of the product, read from `Projection`'s References, not the table's. It checks them
in this order:

- a point to be issued at or past attained age 121, `maturity_age`, which would never be in
  cover: "point_id 12: age_at_entry 121 is at or past maturity_age, 121: a policy issued
  there would never be in cover". The age is checked first, so that such a point is
  refused by its age whenever it is to be issued: one to be issued later would otherwise
  have a frame of months, every one of them before its issue. A point to be issued at
  attained age 120 is a policy, with a year of cover;
- a point at or past the end of the projection at the valuation date,
  `duration_mth ≥ 12 × (121 − age_at_entry)`: "point_id 11: duration_mth 912 is at or past
  the end of the projection, policy month 912, attained age 121";
- a point whose planned withdrawal is above 0 and below the withdrawal fee,
  `0 < wd_pp < wd_fee`: "point_id 5: wd_pp 24.99 is above 0 and below wd_fee, 25.0: a
  withdrawal pays its fee out of itself, so it must be at least the fee". Such a withdrawal
  would debit the account less than the fee the insurer books and pay the policyholder
  nothing: `IUL_US_S` projects it, and its own account value roll-forward and margin
  identity fail on it, as they do on its point 5 withdrawing $20 a month;
- a point in force whose ladder does not hold exactly one row for each of its last
  `min(seg_term_mth, duration_mth)` months, slots 1 to that: "point_id 6:
  inforce_segments_sec.csv holds 11 segments, its last in slot 12, where a policy in force
  60 months holds one a month for its last 12, slots 1 to 12". The count is
  `seg_term_mth`'s, a Reference of `Projection`, which `Data` does not read. `Data`'s slot
  rule accepts twelve rows on the wrong slots, 2 to 13 at month 60, and so this rule
  refuses them, naming the last slot. Each of the five readers of the ladder,
  `seg_bal_pp_init()` to `seg_index_cap_init()`, asks `proj_len()` before it reads a row,
  so that a ladder missing a slot is refused by name, never read as pandas' `KeyError`.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent or its count from. The tables read at an attained age or a
policy year take their extents from `corridor_age_first()` and `corridor_age_last()`,
`mort_age_first()` and `mort_age_last()`, `lapse_last_year()` and `coi_rate_last_years()`,
the last policy year of each issue-age cell of `coi_rates.csv`, beyond which each reads its
nearest row. The key column is read by value, so a year written `5.0` is 5, and a key that
is blank, text or not a whole number is refused, naming the file, the column and the lines
it is on. So are keys that do not run one row an age or a year, without a gap or a repeat,
policy years from 1, the message naming each key that repeats, with its lines, and each
that is missing. So is a blank sex or class in the COI scale, and a value that is blank,
text or infinite. A lapse or mortality rate is a probability, held to 0 to 1, since past 1
the monthly rate `1 − (1 − q)^(1/12)` has no real value. A class factor, a guaranteed COI
rate and a surrender charge are held to 0 or more, since below it each projects, with every
check passing, negative deaths, a credit for the insurance or a surrender charge that rises
once its schedule has run off. A COI rate is a charge per $1,000 of net amount at risk a
month, not a decrement: the current rate passes 1 from attained age 69, as it should, and
nothing caps it. A corridor factor is held to 0 or more too. `IUL_US_S`'s death benefit is
the `max` of the face and the corridor factor times the account value, with no floor on the
account value, so on an exhausted account a factor below 0 would pay far above the face: at
−0.5 from attained age 95, `IUL_US_S`'s point 5 pays 58,155,653.50 on a face of 92,200 at
its month 800, every account check passing. `class_count()` and `surr_charge_count()` check
the class factors and the surrender-charge schedules, for the per-point joins that read
them, the same way, and `surr_charge_count()` also refuses a run-off that is not a whole
number of years, 1 or more, which the projection divides the charge by, where `IUL_US_S`
divides by zero at 0. A class, a COI cell or a schedule the table has no row for is refused
at the join, naming the point, where `IUL_US_S` raises pandas' `KeyError`.

Each reader asks for its extent or its count before it reads a value, so a projection meets
the checks first. `IUL_US_S` takes each extent from the key column as pandas reads it, where
a blank key is a missing value the extent skips: the table is cut short, and every later
year or age reads the last good row, without a word. A blank value is a missing value to it
too, which shows in its flows or is lost in a `min` or a `max`: a blank lapse rate reaches
the lapse cap's `min`, whose bound is written first, and is read as the cap, 1.0, so that
every policy lapses; a blank corridor factor reads as no corridor at all, and a blank
surrender charge as none. Here the cap on the mortality rate, `min(q, 1.0)`, keeps a blank
base rate or class factor missing, as `IUL_US_S`'s own does, and each of them is refused
before any rate is read.

## The model points

No row of `model_point_table_sec.csv` or of `inforce_segments_sec.csv` is typed by hand.
Every one is generated from `IUL_US_S` and its table by `tests/sec_support.py`, from the
`IUL_US_SEC` entry in its `SEC_SPECS`, and the tests regenerate both files and compare, so
an edit to an `IUL_US_S` row reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py IUL_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–5 | twin | S points 1–5 | issued at `t = 0`: `IUL_US_S`'s baseline cell, paying $10,000 a year; the same on Option B; the same with no indexed allocation, the control run the ladder is read against; the same paying monthly, the one point that builds the full ladder of twelve segments; and an underfunded policy paying $6,000 a year, withdrawing $200 a month from policy year 2 and borrowing $6,000 a year from policy year 21 |
| 6 | derived | S point 1 at S month 60 | on its fifth anniversary, at attained age 50, with 48,039.60 of premiums paid: its 43,877.35 of account value is all in the segment created at its fourth anniversary, which matures at `t = 0` with a credit of 2,808.15 as the year's premium of 9,039.21 falls |
| 7 | derived | S point 4 at S month 65 | five months into policy year 6, paying monthly, all twelve segments live, 47,950.61 in all, one maturing each month from `t = 0`; its surrender charge and its no-lapse guarantee in force |
| 8 | derived | S point 5 at S month 6 | six months into its first year: its ladder six months deep, the one segment swept at issue holding 4,998.62 and maturing at `t = 6`; its no-lapse guarantee in effect on its one premium of 6,000.00, failing for good at `t = 43`, policy month 49 |
| 9 | derived | S point 5 at S month 384 | in policy year 33, at attained age 77: its fixed account −112.50 entering the month, its segments empty, and its loan of 87,706.74 above its account value of 87,594.24, so above its cash value; its face cut to 175,600 by its withdrawals |
| 10 | derived | S point 5 at S month 605 | in policy year 51, at attained age 95: its account value −241.18, the fixed account −303,975.15 against a collateral of 303,733.97; its face at 131,400 |
| 11 | derived | S point 1 at S month 888 | two years before the end of its projection, at attained age 119, where the mortality rate is 1.0, with 1.042e-10 of a policy: every survivor dies at `t = 0`, and the frame's 23 later rows of cash flows are zeros |
| 12 | future | S point 4, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `IUL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `IUL_US_S` carries into it, each column read
as `IUL_US_S`'s own formulas read it: the account value, the fixed account and the
collateral as their `"BEF_PREM"` timings at `d`; the loan, the face and the two
accumulators as the close of month `d − 1`, `loan_bal_pp(d − 1)`, `sum_assured_at(d − 1)`,
`cum_prem_pp(d − 1)` and `cum_prem_net_pp(d − 1)`; and the MEC latch as whether
`IUL_US_S`'s 7-pay test failed in any month before `d`, since its flag does not latch. Its
ladder row in slot `k` is the segment `IUL_US_S` created at its month `d − k`: its balance,
deductions and draws at the close of month `d − 1`, `seg_bal_pp(d − 1, d − k)` and the two
running totals beside it; the cap `index_cap_at(d − k)`; and the start level
`index_level(d − k)` rebased onto this model's path, times `index_level_init` over
`index_level(d)`. So the row continues the S projection from there, per policy: point 9
opens with 0.175064 policies, and point 11 with 1.042e-10. A derived row's `policy_id` is
the S row's with the month appended, `IUL-000005-M384`, and a future row's carries the
months to issue, `IUL-000004-F25`. Row `t` of a generated point is month `t + source_mth`
of its S point. All twelve are on the notes' anchor configuration, M45 / NT / $250,000 /
GPT, because the illustrative COI scale covers that cell alone, so a point on any other
issue age, sex or class needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has the
three timings that `IUL_US_S` already names:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_MAT"`, the count before any maturity, `IUL_US_S`'s meaning: the `"BEF_DECR"`
  count, since nothing matures in the frame and no event of the month separates the two.

Any other timing raises. `IUL_US_S`'s cell of the name returns `pols_if(t)` for every
timing, and nothing calls it. `"BEF_NB"` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `IUL_US_S` counts the issued policies, and this model counts them as new
business, not yet in. As in `UL_US_SEC`, `VUL_US_SEC` and `ULSG_US_SEC`,
`basiclife/BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of the month before its new
business, is not adopted: the name keeps its S model's meaning.

The month's decrements are `IUL_US_S`'s, in its order, both at the end of the month:
deaths, then surrenders out of the survivors. No policy is terminated for insufficiency, as
in `IUL_US_S`, whose notes leave the account value in grace and the cash flow of a cure
undetermined: a policy whose account value is exhausted goes on being charged (*The opening
state*, below).

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `"BEF_NB"`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's deaths and lapses, death applied first, as `pols_death`
and `pols_lapse` take them. Each account's opening balance forms the previous month's close
the same way, the same operations in the same order as the closing cell `IUL_US_S` calls
for: `av_pp_at(t, "BEF_PREM")` from its own value at `t − 1` and month `t − 1`'s net
premium, index credit, withdrawal, deduction and interest, where `IUL_US_S`'s account
value ran through five cells a month; `fa_pp_at(t, "BEF_PREM")` from its own and month
`t − 1`'s net premium, matured segment, draw, deduction, sweep and interest, where
`IUL_US_S`'s fixed account ran through six; and `lca_pp_at(t, "BEF_PREM")` from its own,
month `t − 1`'s new loan and the collateral's interest, where `IUL_US_S`'s collateral ran
through two. The loan, the face, the two premium accumulators, the MEC latch, and each
segment's balance and its two running totals call themselves at `t − 1`.

On a model just read, a cold `net_cf` in the last month of point 1's 912-month frame runs
929 cells deep, against 3,974 for `IUL_US_S`'s point 1: 18 cells above the chain back to
`t_entry()`. The other committed points run 16 to 18 above theirs, point 12 18 above its
chain of 911 months from its issue. Each chain's head called alone, on a read of its own
with every chain cold, on the twin of point 4, which pays monthly and keeps twelve segments
live, runs at most 14 cells above its chain: the account value's 8, the fixed account's
12, the collateral's 3, the loan's 4, the face's 5, each accumulator's 4, the latch's 5 and
the count's 14. At the longest cover the contract allows, issue age 0 and 1,452 months, a
cold `net_cf` in the last month runs 1,469 deep, 18 above its chain, both issued at the
valuation date and issued 120 months after it, since every chain stops at the issue month:
about 366 KiB of C stack at gcc's 255 bytes a level. Each report evaluates its columns in
ascending `t`, and on a model just read the committed points' four reports and four checks
run that way under a recursion limit of 18 to 28, and `IUL_US_S`'s points 1 to 4 under 24
to 26. Two rows are the exception, twin 5 and point 8, the rows of `IUL_US_S`'s point 5
on the books before its no-lapse guarantee expires: each needs 217. Their guarantee fails
for good at policy month 49, from which the count reads the account value in no month until
the expiry's shock, at policy month 240, reads the cash value and runs the account value's
chain cold back to month 49, 192 months, one cell a month. `IUL_US_S`'s point 5, whose
chain is five cells a month, does not run that way under 400.

The model exported by modelx 0.33 runs as plain Python, each cell a function call, and
needs more: Python's recursion limit, set after the import, must be at least 1,884 for a
cold `net_cf` in the last month on twin 1 and on point 12, issued 25 months on, 1,754 on
point 7 and 1,113 on point 9, and 2,964 at the longest cover, issue age 0, issued now or
120 months on; the ascending sweep of the four reports and four checks needs 62 on twin 1
and at the longest cover, 70 on point 7, 58 on point 11 and 438 on twin 5, the expiry's
read after a lapsed guarantee. So the export, and Phase 2's sample and runner, need a limit
above 2,964; 10,000, as `Term_US_SEC`'s sets, leaves room.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `IUL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB") = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, the last month included, and `pols_if(t + 1)` adds
`pols_new_biz(t + 1)` to the count on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (maturity_age − age_at_entry)` is `IUL_US_S`'s frame from issue, the
first month at attained age 121. Outside it, before issue and from `t = proj_len()` on,
every count, balance, segment, premium, withdrawal, loan draw, charge, credit, decrement
rate, decrement, claim and cash flow is zero and every flag false, `seg_count` the int 0;
only the two clocks, the inputs read on the valuation clock, the level policy fee and the
neutral 1.0 of the two lapse multipliers hold values there, and the month after the frame
holds two exceptions more, below. No count evaluates a decrement rate there, and no table
is read at a policy year or an attained age the policy does not have: `prem_persistency`,
`premium_pp`, `wd_pp`, `loan_new_pp`, `face_reduction_pp`, `sum_assured_at`,
`corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `expense_unit_mth_at`,
`maint_fee_pp`, `loan_credit_rate_ann`, `surr_charge_rate`, the segment cells, the
opening timings of the three accounts, `loan_bal_pp`, `cum_prem_pp`, `cum_prem_net_pp`,
`cum_mnlp_pp`, `gpt_limit`, `seven_pay_limit`, `cred_rate_ann`, `mort_rate`,
`lapse_rate_base`, `lapse_rate`, `pols_death`, `pols_lapse` and `expenses` are zero, and
`nlg_test_ok`, `nlg_in_effect`, `nlg_expiry_shock`, `is_shortfall`, `gpt_ok` and `is_mec`
false, before any table or rate is read, and every other value is zero through them.
`lapse_rate_sc_mult` and `lapse_rate_dyn_mult` are 1.0 there. The first is 1.0 before it
compares the policy year with the shock year: a point with no surrender charge has the
shock year 0, and before issue the valuation clock reaches policy year 0. Each table read at
a policy year or an attained age has one reader keyed by it, called inside cover only, so
on point 12, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below
1 or an attained age below 45.

**The end of the projection.** The frame ends at `maturity_mth()`, the first month at
attained age 121, the notes' [unverified] maturity inference (spec F5), and not at an event
of the contract, which is described as continuing in force there with no further charges.
Premiums, withdrawals and charges cease at `charges_cease_age`, a Reference of its own, 121
too as shipped; set below `maturity_age`, the projection runs on past the cessation, the
account value earning its interest and the segments their credits with nothing deducted.
Lives can survive the last month, and `IUL_US_S`'s roll-forwards read them:
`check_av_roll_fwd()` and `av_change()` read the account value in force entering month
`t + 1`, which in the last month is `t = proj_len()`. So the two opening values read there,
the count carried in (`pols_if_at(t, "BEF_NB")`, and through it `pols_if(t)`) and the
account value carried in (`av_pp_at(t, "BEF_PREM")`), are defined for
`0 ≤ duration_mth(t) ≤ maturity_mth()`: in the month after the frame they are the survivors
of the last month and the account value they carry, `IUL_US_S`'s own values there.
Everything else is zero or false there, the expenses included, which would otherwise fall
on the carried count, and nothing reads past it: `av_change()` and the checks' residual
cells, which read `t + 1` or are read beside cells that do, are zero outside cover before
they read it. At the shipped assumptions the survivors at `proj_len()` are exactly 0.0 on
every committed point: the mortality table reaches 1.0 at attained age 119, and on the
anchor class, whose factor is 1.0, at an A/E of 1.0, every life has died by the end of the
first month at that age, as point 11 shows. At an A/E of 0.56, which leaves the rate below
1, they are 3.276e-6 of a policy on the twins of points 1 to 3, 3.414e-6 on point 4's and
3.485e-6 on point 5's, `IUL_US_S`'s own counts there, and every check closes.

**Rates stay rates.** The annual mortality rate is capped at 1.0, as in `IUL_US_S`,
`min(q, 1.0)` with its bound second, so that a missing input stays missing. On no committed
point does the product pass 1, since all are on NT, whose factor is 1.0: the cap binds on
the classes whose factor is above 1, first on Tob at attained age 113, 1.75 × 0.625687, and
on PTob at 115, at an A/E of 1.0. The annual lapse rate keeps `IUL_US_S`'s cap,
`min(lapse_rate_cap, rate)`, its bound written first. The cap is 1.0, inert as shipped:
these notes give none, and on the committed points the rate before it is at most 8%, the
4% of policy year 11 doubled by the surrender charge's expiry. The no-lapse guarantee's
expiry shock, `nlg_shock_lapse`, 25%, is returned before the cap, as in `IUL_US_S`: set
past 1 it is a rate past 1, whose monthly rate has no real value, and the account value's
and the margin's checks then raise through their residuals, as `IUL_US_S`'s
`math.isclose` raises. It falls only on a policy with no net cash value in the year after
its no-lapse period, and no committed point takes it. The dynamic lapse multiplier is 1 in
every month, `comp_rate_ann` being `cred_rate_ann`, so neither its floor of 0.5 nor its
cap of 2.0 binds on a committed point.

## The opening state

`IUL_US_S` opens a point whose `duration_mth` is above 0 from two columns, the account
value and the loan entering its first month, and takes the rest from them or as they stand
at issue: the fixed account as the account value less the loan, the collateral as the
loan, no live segment, the face at issue, both premium accumulators at 0, and a MEC flag
from the month's own 7-pay test alone. A policy valued in any month of its life needs all
eight columns and its ladder, each what `IUL_US_S` carries into that month. The committed
points show what most of them change, each compared with the same row read with the column
as `IUL_US_S` would open it:

- **The ladder and `fa_pp_init`.** Point 7 holds its 47,950.61 in twelve live segments and
  nothing in its fixed account, and one segment matures each month, its credit 233.73 at
  `t = 0` and 286.48 at `t = 11`. Read as `IUL_US_S` would open it, all of it in the fixed
  account and no segment live, it would earn no credit until `t = 12`, when the segment
  its first month's sweep makes of the whole account value matures: it would close month 6
  with 52,091.99 of account value where `IUL_US_S`'s own projection, and this model's,
  hold 53,730.24, and month 11 with 54,965.36 where they hold 58,038.13. Point 6 holds its
  43,877.35 in the segment created at its fourth anniversary, which matures at `t = 0` with
  a credit of 2,808.15; read with it in the fixed account, the credit would be lost and the
  account value would close month 0 at 52,341.01 in place of 55,149.71.
- **`sum_assured_init`.** Point 9 has withdrawn $200 a month for 31 years under Option A,
  each withdrawal cutting the face, which stands at 175,600.00 entering month 0, so its
  death benefit at `t = 0` is 175,400.00, after the month's cut. Read at the face at issue,
  as `IUL_US_S` would open it, the death benefit would be 249,800.00, the net amount at
  risk 159,212.58 in place of 84,874.24 and the cost of insurance 331.71 a policy in place
  of 176.83. The surrender charge is quoted on the face at issue either way, and has run
  off.
- **`cum_prem_net_init`.** Point 8, six months after its issue, has paid one annual
  premium of $6,000.00, which keeps its no-lapse test, premiums less withdrawals and loans
  against the minimum no-lapse premium counted from issue, 3,033.33 through month 0,
  passing: its guarantee is in effect, and with no cash value its lapse rate is 0. Read at
  0, as `IUL_US_S` opens the accumulator, the test would fail at once: the guarantee would
  be off, the lapse rate 6%, and 0.993983 policies would be in force at `t = 1` in place of
  0.999121.
- **`loan_bal_init` and `lca_pp_init`.** On the committed points the two are equal:
  `IUL_US_S`'s point 5 borrows only from policy year 21, when the collateral's credited
  rate has stepped up to the loan's 3.00%, so that points 9 and 10 carry 87,706.74 and
  303,733.97 of each. They part on a loan taken in the first ten policy years, when the
  collateral is credited 2.00% against the loan's 3.00%: on a variant of `IUL_US_S`'s
  point 5 borrowing from policy year 6, restated at its month 83, the collateral is
  12,342.02 where the loan is 12,514.54, two balances that have accrued apart since the
  first loan, and that `IUL_US_S`'s entry would merge into one.

The other two columns show nothing on the committed points: none fails the 7-pay test,
and none pays a TARGET premium. Each shows on a variant of an S point, in a copy of S's
table that is never committed, read with the column as above:

- **`cum_prem_init`.** `IUL_US_S`'s point 1 paying a TARGET premium of $30,000 a year,
  restated on its third anniversary, at its month 36, has paid 88,212.00, which leaves
  6,788.00 of room under the guideline premium limit, its guideline single premium of
  95,000: it collects 6,788.00 at `t = 0` and nothing after. With the column at 0 it would
  collect its whole premium for the year, 28,235.76, at once.
- **`is_mec_init`.** `IUL_US_S`'s point 4 paying $36,000 a year, monthly, fails the 7-pay
  test at its policy month 7. Restated at its month 85, in policy year 8, where the in-year
  test no longer applies, `is_mec(0)` is true from the latch alone; with the column at 0
  it would be false, as `IUL_US_S`'s own flag is there, which turns itself off in policy
  year 8, exactly when the failure becomes permanent.

The in-year test runs before the latch looks back, in the valuation month as in every
other, so a policy that fails the test at `t = 0` is a MEC from then on, whatever
`is_mec_init` says: the same variant restated at its month 7 has paid 21,000.00, inside the
first year's limit of 21,000.00, so its `is_mec_init` is 0, and month 0's premium of
3,000.00 takes it to 24,000.00: `is_mec(0)` is true. With `cum_prem_init` at 0 it would be
false.

**An exhausted account, in force.** `IUL_US_S` lapses no policy for insufficiency: a
policy whose account value is exhausted goes on being charged, its fixed account carrying
every deduction and draw the segments cannot, and the cost of insurance then compounds,
since the net amount at risk rises as the account value falls. Its point 5's fixed account
closes below 0 from policy month 383 and its account value from month 604, by design, and
its own tests pin both months; by the end of its frame the account value is about
−1.3 × 10¹⁰. So this model accepts such an opening state: `fa_pp_init` and `av_pp_init`
may be of either sign, held to each other by the account value's identity with the
collateral and the segments. Points 9 and 10 are those states, at 384 and 605, and each
continues `IUL_US_S`'s projection from there, its four checks holding. A face of 0 in force
is accepted too: Option A withdrawals cut the face dollar for dollar, never below 0, while
the policy stays in force. This is where the model departs from `UL_US_SEC` and
`ULSG_US_SEC`, which refuse an account value below 0 and ask for a point to be restated no
later than its last month at 0 or more: `IUL_US_S` carries an exhausted account on by
design, on a shipped point, and a row restated past it is a state its projection
continues. The cash flows stay finite and bounded there, the death claim being the
face less the loan, floored at 0, and the surrender value floored at 0; the account value
is not a meaningful number, as `IUL_US_S`'s [implementation notes](model.md) say.

## The segment ladder

A segment is created at every monthiversary by the sweep, and matures twelve policy months
later, so up to twelve are live at once [S4]. `IUL_US_S` keys each segment by the month of
its creation on its own clock, `seg_bal_pp(t, m)`; this model keys it by the policy month
`m` of its creation, `duration_mth` of the month whose sweep made it, which on a point
issued at `t = 0` is the same number. A parameter that holds a policy month is named `m`,
never `t`, so that the twin comparison shifts `t` alone. The ladder's `slot` is the months
since the segment's creation at the valuation date, `k = duration_mth_init() − m`, which is
what an extract of a policy's live segments knows. The two meet at `t = 0`, where slot `k`
is the segment born in policy month `duration_mth_init() − k`, and slot 12 the one maturing
at `t = 0`.

Each segment cell opens a segment born before the valuation date from its ladder row, at
`t_entry()`: `seg_bal_pp`, `seg_ded_cum_pp` and `seg_wd_cum_pp` from the slot's balance,
deductions and draws, `seg_share` and the pool, `seg_bal_active_pp`, from its balance, and
`index_credit_pp`, `seg_roll_pp` and the closure's residual, at `t = 0`, from slot 12's.
Its creation balance, `seg_new_pp(m)`, is its row's three amounts summed, so the closure
`check_seg_ladder()` asserts holds by construction on the segment maturing at `t = 0`, and
the credit, under either credit base convention, depends on the three amounts alone. A
segment born in the frame is the sweep of its month, as in `IUL_US_S`.

The start level and the cap of the segment maturing in month `t`, `seg_index_start(t)` and
`seg_index_cap(t)`, are `index_level(t − 12)` and `index_cap_at(t − 12)` for a segment born
in the frame, and its ladder row's `seg_index_start_init` and `seg_index_cap_init` for one
born before the valuation date. The projection passes each segment's cap and the credit
base convention, `seg_credit_base_conv`, to the engine cells explicitly, so that no
projection call reaches their `None` defaults, the cap in force at `t = 0` and the
Reference's convention, which the engine cells keep as `IUL_US_S` has them, for its worked
example. Every month the ladder runs reads a start level and a cap, a month whose segment
holds nothing included: the trailing credited rate, `cred_rate_ann(t)`, which drives the
dynamic lapse multiplier, is the credited rate of the segment maturing in the month whether
or not it holds a balance, from policy month 12 on. So every one of the last twelve months
holds a ladder row, empty or not, and `proj_len()` refuses a point in force that lacks
one.

**Rounding about zero.** A draw or a deduction that takes a segment's whole balance can
leave it a rounding about zero, a balance of the order of 10⁻¹⁶ of either sign, and
`IUL_US_S` closes on such states. `seg_share` reads the pool by `IUL_US_S`'s test,
`pool <= 0`, and `seg_count` counts a segment where its balance is above 0, so that on
such a state the two models branch alike; `Data` accepts a segment's balance, deductions
and draws down to `−1e-8` for the same reason, the tolerance `check_seg_ladder()` holds
each live balance to. The credit of a segment drawn to a
rounding about zero is a rounding itself: point 9's slot 12 holds nothing, and its credit
at `t = 0` is −1.455e-14 a policy, as `IUL_US_S`'s is at its month 384, well inside
`check_seg_ladder()`'s tolerance of `1e-8`. On a row restated earlier, every return is a
ratio of two levels on another path, which differs from `IUL_US_S`'s in its last bits, and
so can such a rounding: on point 8 the same credit, at its `t = 378`, is −2.910e-14.

The pool, `seg_bal_active_pp(t)`, and the total, `seg_bal_tot_pp(t)`, sum the segments in
an explicit loop that compensates as Python's `sum()` of floats does from Python 3.12,
Neumaier's improvement of Kahan's summation, so that each is `IUL_US_S`'s `sum()` bit for
bit there, a pool of 10⁻¹⁶ included. `IUL_US_S` sums a generator, which a rewritten cell
does not hold, so that it compiles; `seg_count` counts in a loop for the same reason. Python
3.11's `sum()` is a plain fold, which can put such a pool on the other side of zero, so the
states `IUL_US_S` closes on a rounding about zero depend on the interpreter it runs on.

## Departures from IUL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state and
the ladder on a point in force, and each cell that turns `t` into a policy year or an
attained age answers for the months outside cover. Of `IUL_US_S`'s 156 cells in
`Projection`, 58 are unchanged, 32 have a new docstring only, most of them to say what `t`
now counts, and 66 are rewritten. None is removed or renamed, and 42 cells are new, 198 in
all. A cell of `IUL_US_S`'s that this model lacked would fail the twin identity.
`IUL_US_S`'s Reference `math`, which only its checks' `math.isclose` read, is dropped, and
every other Reference of `Projection` is `IUL_US_S`'s, value for value; none is added. Of
`Data`'s eight cells, `model_point_table` is rewritten to check the table as it reads it,
and eleven cells are new, nineteen in all: the ladder's reader, `inforce_segments`, and its
two summaries, `inforce_segment_count` and `inforce_segment_last`; the six extents of the
four tables read at a policy year or an attained age, each of which checks its table's keys
and values; and `class_count` and `surr_charge_count`, which check the class factors and
the surrender-charge schedules. `Data` gains two References, `inforce_segments_file` and
`future_horizon_mth`, 120, and `model_point_file` names `model_point_table_sec.csv`. The
cap on mortality, `min(q, 1.0)`, is `IUL_US_S`'s own and no departure, and so are the lapse
rate's cap in `IUL_US_S`'s order, its bound written first, and the shock lapse returned
before it.

| Cells | `IUL_US_S` | `IUL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `maturity_mth` | `12 × (maturity_age − x) − duration_mth_init()`, the months from the first projected month | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises, in this order, for a point to be issued at or past attained age 121, one at or past the end of the projection, one withdrawing above 0 and below the fee, and one in force whose ladder lacks a row of its last `min(12, duration_mth)` months or holds another | `maturity_mth()` is new and is `IUL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left, or none in cover, has no frame; a withdrawal below its fee breaks `IUL_US_S`'s own roll-forward; a ladder without its rows misstates the credits and the trailing rate |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`; `"BEF_NB"` the count before the month's new business, formed from the month before in the cell itself, and `"BEF_MAT"` the `"BEF_DECR"` count, as in `IUL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month; the chain is one cell a month |
| `av_pp_at`, `fa_pp_at`, `lca_pp_at`, `loan_bal_pp` | `av_pp_init()`, `av_pp_init() − loan_bal_init()`, `loan_bal_init()` and `loan_bal_init()` at `t = 0`, then the previous month's closing cell: chains of five, six and two cells a month | at `t_entry()`, the account value's parts summed on a point in force, `av_pp_init()` on any other, and `fa_pp_init()`, `lca_pp_init()` and `loan_bal_init()`, then the previous month's close formed in the cell itself, `IUL_US_S`'s arithmetic in its order; zero outside cover but the account value's opening, carried into `t = proj_len()` | The fixed account and the collateral are not the account value less the loan and the loan once a policy has segments or interest has accrued; every chain one cell a month, since a compiled model runs it on the C stack |
| `seg_bal_pp`, `seg_ded_cum_pp`, `seg_wd_cum_pp`, `seg_share`, `seg_bal_active_pp`, `seg_bal_tot_pp`, `seg_count`, `seg_new_pp`, `seg_roll_pp`, `index_credit_pp` | keyed by the month of creation on `IUL_US_S`'s own clock; no segment before `t = 0`; the pool and the total summed by `sum()` over a generator | keyed by the policy month of creation; a segment born before the valuation date opened from the ladder at `t_entry()`, its creation balance its row's three amounts summed, and its share there read only for a slot the ladder holds, 0 for any other `m`, as `IUL_US_S`'s read outside a segment's life gives; the pool and the total summed in a compensated loop, the live segments counted in a loop | A policy in force holds live segments; the loops are `IUL_US_S`'s `sum()` bit for bit from Python 3.12, and compile |
| `index_level`, `seg_return`, `index_credit_pp`, `cred_rate_ann` | the index at `duration_mth(t)`; a segment's start level `index_level(t − 12)` and its cap the engine's default, the cap in force at `t = 0`; the trailing rate's first-segment test `t < 12` | the index at `t`; the start level and the cap from `seg_index_start(t)` and `seg_index_cap(t)`, the frame's or the ladder's, passed to the engine with the credit base convention explicitly; the first-segment test `duration_mth(t) < 12` | One index path for every point, on the valuation clock; each credit stays `IUL_US_S`'s, a ratio of two levels on that path; the ladder runs from the policy's own twelfth month |
| `sum_assured_at`, `face_reduction_pp`, `cum_prem_pp`, `cum_prem_net_pp`, `premium_pp` | opened at `t = 0` at the face at issue, 0 and 0, and the TARGET cap's premiums to date at 0 | opened at `t_entry()` from `sum_assured_init()`, `cum_prem_init()` and `cum_prem_net_init()` on a point in force, and from the issue values on any other | A policy in force brings in its face, its premiums and its no-lapse accumulator |
| `is_mec` | the 7-pay test of the month alone, `policy_year(t) <= 7` and the premiums to date above the limit | the same test, then the latch: month `t − 1`'s flag, or `is_mec_init()` at `t_entry()` | A contract that fails the test is a modified endowment contract for good [R5]; `UL_US_S` latches it, and so does this model |
| `premium_pp`, `db_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `premium_mode()`, `db_option()` and `qual_test()` | branches on eight decodes, each reading its column from `model_point()`: `is_level_premium`, `is_single_premium`, `is_target_premium`, `is_annual_premium`, `is_monthly_premium`, `is_db_option_a`, `is_db_option_b` and `is_gpt` | No monthly cell compares text, and no projection cell calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `IUL_US_S`'s message |
| `class_factor`, `coi_rate_scale`, `surr_charge_rate`, `lapse_shock_year` | joined on the label accessors, the surrender-charge schedule's row read in each | the same joins, on keys read from `model_point()`: the class factor once `data.class_count()` has checked its table, the COI scale through its one reader, once `coi_rate_last_year()` has, and the schedule through `surr_charge_rate_max()` and `surr_charge_runoff_years()`, each once `data.surr_charge_count()` has; a key the table lacks refused, naming the point | A blank factor, a missing value to `IUL_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and a blank charge `surr_charge_rate`'s `max`, which reads it as none; `IUL_US_S` raises pandas' `KeyError` on a missing key |
| `corridor_factor`, `mort_rate`, `coi_rate_guar`, `lapse_rate_base` | the table read in the monthly cell, at `age(t)` or `policy_year(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the age or the year — `corridor_factor_at`, `mort_rate_base_at`, `coi_rate_guar_py` and `lapse_rate_base_py` — with `IUL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the values, called inside cover only | No table is read at an age or a year the policy does not have, each is read once an age or a year, and a malformed key or value is refused by name, where `IUL_US_S`'s extent skips a blank key and cuts the table short, and a blank value is a missing value |
| `prem_persistency`, `premium_pp`, `wd_pp`, `loan_new_pp`, `face_reduction_pp`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `expense_unit_mth_at`, `maint_fee_pp`, `loan_credit_rate_ann`, `sweep_pp`, `seg_index_start`, `seg_index_cap`, `seg_return`, `surr_charge_rate`, `cum_mnlp_pp`, `nlg_test_ok`, `nlg_in_effect`, `nlg_expiry_shock`, `is_shortfall`, `gpt_limit`, `gpt_ok`, `seven_pay_limit`, `is_mec`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult`, `cred_rate_ann`, `lapse_rate_dyn_mult`, `lapse_rate` | unguarded: no `IUL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; the two lapse multipliers 1.0, `lapse_rate_sc_mult` before it compares the policy year with the shock year | A future point's months before issue have `t ≥ 0` and policy years down to −9 at the horizon, and policy year 0 is the shock year of a point with no surrender charge. At `t = proj_len()` nothing is charged, paid, credited or withdrawn |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars; 0 as shipped |
| `wd_pp`, `loan_new_pp` | the model point's `wd_pp` and `loan_new_pp_ann` columns read in the monthly cell | read once a point, by `wd_pp_mth()` and `loan_new_pp_ann()` | A monthly cell on the accounts' chains reads no model point column in its own formula |
| `check_av_components`, `check_av_roll_fwd`, `check_seg_ladder`, `check_margin` | `math.isclose` with `rel_tol=1e-9` and `abs_tol=1e-8`, and the ladder's tests, month by month | the same conditions on residual cells, one a month: `check_av_components_resid(t)`, `check_av_roll_fwd_resid(t)` and `check_margin_resid(t)`, each a `float` over the larger side and 10, and the ladder's four, `check_seg_count_resid(t)`, `check_seg_credit_resid(t)`, `check_seg_bal_resid(t)` and `check_seg_closure_resid(t)`; a residual that is not a number fails, and one that is not real raises, as `IUL_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the loan term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the debt a surrender recovers | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `IUL_US_S`'s identity is off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its check fails on a projection that is right, as on its point 5 from policy month 383: −2.09 on point 9 at `t = 0`. This model states the identity as `UL_US_SEC`, `VUL_US_SEC` and `ULSG_US_SEC` do, and the two agree wherever the loan is within the cash value |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `result_seg` | the return written 0 where `t < 12` | the return `seg_return(t)`, 0 in a policy's first twelve policy months | The ladder runs from the policy's own twelfth month |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`, the six
new opening-state accessors, `fa_pp_init`, `lca_pp_init`, `sum_assured_init`,
`cum_prem_init`, `cum_prem_net_init` and `is_mec_init`, the ladder's five slot accessors,
`seg_bal_pp_init(k)`, `seg_ded_cum_pp_init(k)`, `seg_wd_cum_pp_init(k)`,
`seg_index_start_init(k)` and `seg_index_cap_init(k)`, and `coi_rate_last_year`, the extent
of a point's COI scale.

Of the cash flows, the change of clock moves none at the shipped assumptions: inflation
ships at 0, and the index path's clock moves the level and no credit. On a point restated
in force, every cash flow, count and per-policy value is `IUL_US_S`'s from its month on, to
rounding, and so is every column of `result_seg()` but the index level. On point 12, every
one is `IUL_US_S`'s point 4's, 25 months on.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 5, issued at
  the valuation date, every cell of `IUL_US_S`'s agrees at every argument `IUL_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point`, `result_pols` and
  `check_margin`, whose meaning changed; a cell this model lacked would fail it. So the
  goldens `tests/test_indexed_ul_us.py` asserts on those points — the worked example's
  credits through the engine cells, the anchor's account value rows and its month-0
  trace, the ladder's first segment and its eleven deductions, the pitfalls, point 5's
  overloan from month 383 and its account value turning negative at month 604 — hold here,
  with no number restated. The identity holds on any count, since `IUL_US_S` already
  charges acquisition on the policies issued. The same suite holds the model to the
  conventions every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the
  `"BEF_DECR"` count, new business enters once at its `policy_count`, nothing happens
  before issue, and the in-force columns are present.
- **The splice**, in `tests/test_indexed_ul_us_sec.py`: each `IUL_US_S` point restated in
  force at a month either side of its events, opened with `IUL_US_S`'s own count, state and
  segments there, continues the S projection from there, in its four reports, column by
  column, and in every other cell the two share, to 1e-9 relative with no absolute floor,
  since its counts and its deepest ladder values fall far below 1e-7. A value both models
  give below 1e-9 a policy, a rounding about zero, is held to that floor instead, and
  `seg_count` and `seg_share` are left out of a month where a live segment or the pool is
  such a rounding in either model: off the valuation date each such state is reached
  through other arithmetic than `IUL_US_S`'s, the creation balance of a segment carried in
  summed from its row and each return a ratio of two levels on another path. The
  comparison leaves out those cells the twin identity
  skips, `IUL_US_S`'s own opening accessors and frame, the index level, whose path is on
  another clock, and the MEC flag, which latches here and which a test of its own compares
  with `IUL_US_S`'s flag accumulated. The months straddle the product's events: a
  segment's creation and its maturity, the first anniversaries, a full ladder of twelve
  segments carried in mid-year, the surrender charge's last month, the lapse shock year,
  the no-lapse guarantee failing, passing again and expiring, with its lapse shock on a
  policy with no cash value, the 7-pay test's seventh year and the latch it leaves, the
  guideline cap on a TARGET premium, a loan whose collateral is credited apart from it,
  charges ceasing in cover, a face withdrawn to nothing, a segment and the pool closing on
  a rounding about zero, `IUL_US_S`'s point 5's fixed account and then its account value
  entering the month below 0, and the last covered month, whose `t = 1` is the month the
  survivors are carried into. So are variants of S's points, in a copy of S's table that
  is never committed, each changing S's columns only and each with input rows of its own,
  for branches S's own points do not reach: between them they carry every class and both
  sexes, both death benefit options, the single and the TARGET premium, each premium mode,
  a second surrender-charge schedule and none, issue ages 50 and 65, loans from policy year
  6, a split allocation, a premium over the 7-pay limit, withdrawals that cut the face to
  nothing, withdrawals from the issue month (variant 19, on a row issued 13 months on),
  and underfunded payers whose accounts are exhausted. A row restated at a variant's month
  98 holds a loan its collateral would not fail the shortfall test on, where the loan
  does. The twin of each variant
  issued at the valuation date is compared with its S point cell by cell. The References
  are set in both models to reach what the shipped values leave unreached: the mortality
  A/E at 0.56, which leaves survivors at the end of every frame; charges ceasing at
  attained age 100, inside every frame; the lapse cap at 35% and the lapse spike at 10
  times, so that the cap binds; and the per-unit charge after policy year 10, which ships
  at 0, switched on. Each also sets apart a Reference from another it ships equal to. A
  second fixture, on References of its own, binds the bounds `IUL_US_S` ships idle that
  one pair of models can bind, the guaranteed cap on the credits and the dynamic lapse
  multiplier's floor, and a path of the index overridden alike in both models binds the
  index floor and the multiplier's cap. Splices of their own move the segment term to 6
  months, and to 24 on the full grid, so that every segment cell, the ladder's count and
  the comparison's cut-off read `seg_term_mth`, not the twelve it ships at; and set a
  premium persistency above 1, under which a variant fails the 7-pay test first in policy
  year 7, the window's last, which its twin latches and its row restated there fails at
  `t = 0` with no latch carried in. On a variant's twin the tests of 0 that `seg_count`
  and `seg_share` keep are asserted at a segment and a pool of 5.6e-17, which a threshold
  of `1e-9` would read otherwise; `check_seg_bal_resid` is held to the least balance of
  the segments live in each month.
- **The core grid and the full one.** By default the splice and the future business run a
  core of 40 of their cases, which between them reach every line of the model the full
  grid reaches, every opening-state column, every kind of valuation month and every premium
  pattern and mode, and every floor and cap the grid binds, each checked by the raw value it
  bounds, and a test asserts that they do. The other cases carry the `sec_full` marker and
  show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set, and so do the
  every-state test under the main splice's References, the cold calls at the longest cover
  and the runner's test on the committed table. One leg of the CI matrix sets it, so every
  CI run runs the full grid too. Even so the default run is long: 936 to 955 seconds over
  two runs under load, the longest of the product modules.
  Each splice's S is swept one point at a time, as its cases ask, and its rows are
  generated one S point at a time, so the module's peak is 4.2 to 4.3 GB.
- **Future new business**: issued 1, 6, 13 and 25 months after the valuation date, S's
  points and variants are the S projection moved on, cell by cell, but the count before new
  business in the issue month, which `IUL_US_S`'s cell counts as in force, the index level
  and the MEC flag, as on a restated row; with zeros before issue in every report and no
  decrement rate evaluated there. A point with no surrender charge, issued 6 months on,
  shows the guard on the lapse spike: before its issue its policy year is 0, the shock year
  such a point has.
- **How it computes**: on every row the splice and the future business compare, no cell
  has been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1`. Every
  monthly cell holds its value outside cover and reads no table there, before issue and at
  `proj_len()`. On a fresh read of the committed model the policy clock is a closed form,
  every point's reports run under a lowered recursion limit, raised by a stated allowance
  on the two rows whose expiry shock reads the account value cold, which a recursion
  backward over the frame would exceed, and no projection cell has read a label accessor.
  And every chain is called cold, each call on a read of its own, `net_cf` in the last
  month and each chain's head, on the committed points and at the longest cover, issue age
  0, issued now and 120 months on, modelx's stack trace counting no more than one cell a
  month back to `t_entry()` and a fixed overhead, which a chain of two cells a month would
  exceed.
- **Counts, validation and regeneration**: the roll-forward closes, the last month
  included, `"BEF_MAT"` is the `"BEF_DECR"` count, and `pols_if_at` refuses a timing it
  does not have; `result_pols()` is `IUL_US_S`'s, column for column, with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, with every assumption that ships at zero
  switched on, scales every counted cell and moves no per-policy value; each malformed row
  of the table and of the ladder is refused naming its point or its line, by its own rule,
  and so is a projection of it; each assumption table with a malformed key or value is
  refused naming its file, its column and its lines, a corridor factor below 0 among them,
  while the bounds of each range are read; a `db_option`, `qual_test`, `premium_type` or
  `premium_mode` no decode knows raises `IUL_US_S`'s message, and a class, a COI cell or a
  schedule the tables lack is refused naming the point; the horizon is a Reference, which
  at 0 refuses any future business, saying so; a point to be issued at or past attained
  age 121, one at or past the end of the projection, one withdrawing below its fee and one
  whose ladder lacks a row or holds another are refused by `proj_len()`, in that order,
  each rule on its Reference, read at it, just past it and with it moved, and each pair of
  neighbouring rules broken together refused by the first; a ladder of twelve rows on the
  wrong slots is refused by name, and so is a projection that reads a sparse ladder before
  asking for its frame; every state `IUL_US_S` reaches, under the shipped References, the
  main splice's and the second splice's, each run of the test, restated in force by the
  generator and read through `Data` and `proj_len()`, is accepted, the exhausted
  accounts, a face of 0 and the roundings about zero among them, and the test asserts that
  it met them; each flag reads the same in every spelling `Data` accepts, and the edges of
  the interface are accepted, the tables' keys written as floats among them; the committed
  table and ladder with every amount carried to the cent are read, and each point holds
  its four checks and projects within a cent a policy of its committed row; the committed
  table and ladder are what `IUL_US_S` generates; and each committed derived and future row
  opens with `IUL_US_S`'s own count and state at its month and continues its S point per
  policy, frame by frame, at the shipped assumptions.
- **The opening state and the rest**: each opening column, and the ladder, read as
  `IUL_US_S` would open it, gives the numbers above; the MEC flag latches where
  `IUL_US_S`'s turns itself off; the index path runs on the valuation clock, overridden
  alike in both models; the cap and the fixed-account rate, overridden on this model alone
  by paths that step 30 months from the valuation date, since `IUL_US_S` reads one cap for
  every segment, are read at month `t`, a segment keeping the cap of its creation month
  and one carried in its ladder row's; and expense inflation, switched on, steps on the
  valuation anniversaries; a check whose residual is not a number fails, the NaN sent
  through a Reference before the model computes anything; a shock lapse past 1 makes the
  account value's and the margin's checks raise in both models; on point 5 the margin
  identity holds where `IUL_US_S`'s fails; acquisition falls on new business alone; a
  tobacco point whose mortality passes 1 is `IUL_US_S`'s in every cell, the capped months
  included, the rate there the float 1.0 in both models; a NaN that reaches the cap stays
  NaN; each clamp of a table shorter than the cover binds with an effect; the engine cells
  give the worked example's credits; the docstrings describe this model and not `IUL_US_S`,
  their tables read into the right cells, and they parse under docutils with nothing
  rendered wrongly; both models read the one copy of each assumption table, and every
  Reference of `Projection` is `IUL_US_S`'s, value for value, each pair that ships equal set
  apart somewhere; the points of a block sum row by row; an extract without the generator's
  three columns, relabelled, projects the same numbers; and `run_sec.py` prints the model's
  numbers.

```bash
python -m pytest tests/test_indexed_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_indexed_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k IUL_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-indexed_ul-r1
[R4]: #uslib-indexed_ul-r4
[R5]: #uslib-indexed_ul-r5
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
