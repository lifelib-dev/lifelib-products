# In-Force Implementation Notes

**Status:** Draft, 2026-11-04. `ULSG_US_SEC` is [`ULSG_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year and in their grace, and policies to be
written in the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes. The suffix adds lifelib's letters to `S`: `E` for in force, as
in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is
still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `ULSG_US_S` on another time axis, and it reads `ULSG_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced from the retrieved
> carrier documents behind the product spec: the 25% premium load and the $5.50 monthly
> per-policy charge [S3] [S7], the 2.0% guaranteed credited rate [S3] [S5] [S7], the 5.0%
> and 3.0% loan rates [S4], the 61-day grace period [S7], the return-of-premium
> percentages, anniversaries and 40%-of-face cap [S1], the in-force test on the shadow
> account net of indebtedness [S4] [S2] [S9] and the cessation of charges at attained age
> 121 [S7]. **Every shadow-account parameter is a [std] standardization**: no carrier
> publishes them and no specimen policy form was retrievable. So are the guaranteed
> maximum COI curve, which is not the 2017 CSO table, the mortality table and its
> improvement, the lapse table, the dynamic-lapse formulas, the exercise rates and every
> expense. Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/guaranteed_ul/run_sec.py            # point 1: the worked example, in force
python products/guaranteed_ul/run_sec.py 5          # point 5: S point 1 at 81, in its grace
python products/guaranteed_ul/run_sec.py --block    # every model point, summed row by row
```

The first prints, as rows `t = 0 … 11`, the cash flows, the two account values, the
guarantee diagnostics and the counts behind them for point 1, the technical notes'
worked-example policy. It is in force 300 months at the valuation date, as it is at the
start of `ULSG_US_S`'s own projection, so its rows `t = 0 … 4` are the worked example's
five months, policy months 301 to 305, here as in `run.py`: the account value closes them
at 7,679.31, 4,834.68 and 1,965.91, is exhausted at `t = 3`, and the guarantee carries the
policy from there. Its account values and guarantee diagnostics are `run.py`'s line for
line. Of its cash flows only `expenses` differ, 8.24 in the first month where `run.py`
prints 13.57, because the maintenance expense is in valuation-date dollars here, and
`net_cf` with them, −12,383.41 against −12,388.75. Three lines to the same thing for point
5:

```python
import modelx as mx
model = mx.read_model("products/guaranteed_ul/ULSG_US_SEC")
model.Projection[5].result_guar()
```

`Projection` takes a `point_id`, as in `ULSG_US_S`. Its four result tables are indexed by
`t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `ULSG_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `claims_rop`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `ULSG_US_S`'s two account values per policy, in the columns and order of the technical notes' worked example, then the forgone deduction and the status, with zeros before issue |
| `result_guar()` | `ULSG_US_S`'s guarantee diagnostics: the net amount at risk and the cost of insurance on each account, the deduction forgone across the policies in force, the shadow account net of debt, whether the guarantee is active, the catch-up premium that would restore it and the grace counter |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths, surrenders, refund exercises and terminations in grace, in that order, and its maturities, which are always zero; then `ULSG_US_S`'s two monthly decrement rates, written 0 outside cover |

`ULSG_US_S`'s three self-checks, `check_av_roll_fwd()`, `check_sg_roll_fwd()` and
`check_margin()`, run over the same frame, and hold on every committed point.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`, then a
collection), so the run holds the cells of one point at a time. It prints where each point
stands at the valuation date, then the block's first twelve rows and the block summed into
projection years, `pols_if` the count entering each. The committed block opens with 5.43
policies, 186,024.04 of premiums and a net cash flow of 723.45. A label not in the table,
or not a number, stops the runner with the table's labels and no traceback.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the first month at attained age 121, where premiums
  and charges cease.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' `duration_months + t`, and the contract
  runs on it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1`
  and `age(t) = age_at_entry() + duration(t)`, as in `ULSG_US_S`. `BasicTerm_SE` reaches
  the same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`ULSG_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force point there: point 1 at 300 months, with its account value, its shadow
account, its loan and its premiums to date. What the valuation clock adds is that `t = 0`
is one instant for every point, that a point may be issued after it, and that a point in
force brings in what its past has left it: one value more than `ULSG_US_S` reads, the
months it has already spent in its grace.

Point 1 is `ULSG_US_S`'s in-force point, in force 300 months. At `t = 0` it is on the
anniversary that opens policy year 26, at attained age 85, where its 25th anniversary's
return-of-premium window falls, and its frame has 432 rows, `t = 0 … 431`. Point 7 is
`ULSG_US_S`'s point 2 restated at its month 305, five months into policy year 26: its
policy anniversaries, and with them its annual premiums, fall at `t = 7, 19, …`, and its
frame has 427 rows. Point 9 is `ULSG_US_S`'s point 2 to be issued 25 months after the
valuation date: `duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0
to 24 are zeros, its first premium, the $10,800 at the 98% premium persistency, $10,584.00,
falls at `t = 25`, and its frame has 757 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium months of each mode, the single premium in the issue month and the ten-pay years; acquisition in the issue month and its load on the first year's premiums; withdrawals from policy year 2; the surrender charge by policy month; the return-of-premium windows at the 20th and 25th anniversaries; the guaranteed COI scale, the mortality rate and the corridor factor at the attained age, and the improvement rate graded by it; the base lapse rate by policy year; premiums and charges ceasing, and the projection ending, at attained age 121, policy month `charges_cease_mth()` | the declared credited rate, `crediting_rate_ann(t)` and `inv_return_mth(t)`, flat as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 2.5% as shipped; mortality improvement, `mort_improve_factor(t)`, a year of it at each anniversary of the valuation date for 20 years |

**Expense inflation** keeps `ULSG_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. `ULSG_US_S` steps it on the policy year, from the policy's issue, so on
a point in force it inflates the $75 a year from the issue year: point 1's maintenance
expense is `ULSG_US_S`'s divided by `1.025^25`, about 1.854, at every `t`, since both
models step on its anniversaries. Acquisition, $300 a policy in the issue month and 90% of
every first-year premium, is charged per policy issued and not inflated, as in
`basiclife/BasicTerm_SE`: `ULSG_US_S` charges it on the policies in force in the issue
month, which are the policies issued. The claim expense, $300 a death, is not inflated in
either model.

**Mortality improvement** runs from the start of `ULSG_US_S`'s own projection: the factor
is 1.0 in its first year and gains a year of improvement on each anniversary of that start,
for at most 20 years, each year's at the rate graded at the attained age a year before,
1.0% to attained age 85 and 0 from 95. This model keeps both cells' formulas, so
improvement runs from the valuation date, for every point of a block, which is what
`ULSG_US_S` already does for its own in-force point 1: the years accrue at `t = 12, 24, …`,
in the same months for every point, whatever its own anniversaries. Between them the factor
moves only where a graded rate it reads moves, at attained ages 85 to 95, and those step on
the policy's anniversaries: on point 7, valued mid-year at attained age 85, it moves at
`t = 12, 19, 24, 31, 36, …`. A point written `k` months after the valuation date takes the
improvement of the valuation years before its issue too, each graded at the age its cohort
had reached in that year: point 9 dies at 0.9801 of the table's rate in its issue month,
`t = 25`, where `ULSG_US_S`'s point 2, issued at its own `t = 0`, dies at the table's rate.

So a point restated at `ULSG_US_S`'s month `d`, or written later, continues its S point
per policy, but its counts part from S's by design: it improves from its own valuation
date, and S's point from S's `t = 0`. On the committed points the account value and the
shadow account per policy are `ULSG_US_S`'s exactly, while the count of point 6,
`ULSG_US_S`'s point 2 restated at 240, is up to 0.0271 of a policy apart and its `net_cf`
up to 342.78. The tests compare the counts with improvement and inflation set to 0 in both
models, and hold each of the two to the valuation clock, at its shipped value, in a test of
its own (*Tests*, below).
The declared credited rate is an economic input too, read at `t`, and ships flat at 3.50%,
so its clock shows in no number.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`ULSG_US_S` computes, whatever the point's count. On `ULSG_US_S`'s three new-business
points every cash flow and every count agrees, and so does every other cell the two models
share, at every argument `ULSG_US_S`'s own sweep evaluates, but three whose meaning
changed: `pols_if_init()`, now the count already in force at the valuation date, 0 for new
business; `model_point()`, a row of another table; and `result_pols()`, which gains
`pols_new_biz`. The four cells of `ULSG_US_S`'s funding-premium solve are not in this
model (*Departures*, below). On point 1, `ULSG_US_S`'s in-force point, which both models
open at the valuation date, the projection is `ULSG_US_S`'s from `t = 0` on, in every cell
the two share but `inflation_factor` and the cells it reaches, the expenses, the expense
margin, `net_cf` and `result_cf()`; with inflation set to 0 in both, every cell agrees.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `ULSG_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and seven of its columns are the in-force interface:
`basiclife/BasicTerm_SE`'s two, and five that open an in-force policy's state. Every amount
is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, 0 or more | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value, its loaned part included |
| `sg_pp_init` | dollars, of either sign | the start of month 0 | the shadow account, which is never floored: below 0 it measures the catch-up shortfall |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `cum_prem_init` | dollars | the start of month 0 | the premiums paid from issue to policy month `duration_mth − 1`, withdrawals not netted, which the return-of-premium refund reads |
| `grace_mth_init` | whole months, an int | the start of month 0: the counter after policy month `duration_mth − 1` | the months already spent in the grace period, 0 for a policy not in grace; at most `grace_months − 1`, 1 as shipped |

The five state columns are 0 on a point issued at or after the valuation date: it is issued
with no account value, no shadow account, no loan, nothing paid and no grace.
`av_pp_init`, `sg_pp_init`, `loan_bal_init` and `cum_prem_init` are `ULSG_US_S`'s own
columns, and the technical notes' `av_init`, `sg_init`, `loan_init` and `cumprem_init`:
they already measure the balances entering `ULSG_US_S`'s first month, so they keep their
names. `grace_mth_init` is named for the cell it opens, `grace_mth`, as they are for
theirs; the technical notes give the counter no model point attribute, and open it at 0.
The shadow account is state, carried in its own column like the account value: it is the
policy's own balance, not a path a model could recompute from issue.
`UL_US_SEC`'s other state columns would open no cell here. The face never moves, since a
withdrawal reduces the two accounts and not the face, and the product has neither a free
withdrawal allowance nor a 7-pay test, which the notes put out of the model: so there is no
`sum_assured_init`, `wd_used_year_init` or `is_mec_init`. Nor is there a loan account, as
in `VUL_US_SEC`: the loaned part of the account value is the debt itself. No quantity of
the product is read at the last anniversary, so none needs a column at a second instant.

| `ULSG_US_S` | `ULSG_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `sg_pp_init`, `loan_bal_init`, `cum_prem_init` | the same | `ULSG_US_S` already opens its in-force point from them |
| — | `grace_mth_init` | `ULSG_US_S` reads the grace counter of the month before its frame as 0 |

On the twins the new column takes what `ULSG_US_S` itself assumes, 0, so each twin opens as
its S row does: point 1 with the worked example's account value of 2,400.00, shadow account
of 118,000.00, no loan, 270,000.00 of premiums paid, 25 annual premiums of $10,800, and no
grace.

The columns carried over are read as `ULSG_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the mode and the withdrawal excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `ULSG_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the face, level for the life of the policy, on which the per-unit charges and the surrender charge are quoted |
| `guarantee_age` | an attained age, 90 to 121 | the guarantee elected at issue; 121, the lifetime election, sets the lifetime lapse multiplier |
| `premium_type` | `LEVEL`, `SINGLE` or `TEN_PAY` | the pattern over the frame: a single premium falls in the issue month alone, ten-pay's in the first ten policy years |
| `premium_pp_ann` | dollars a year, the scheduled premium, or the single premium on `SINGLE` | issue: the premium the policy was issued on, which a point in force goes on paying |
| `premium_mode` | `A`, `S`, `Q` or `M` | the mode over the frame; its instalments fall on the policy clock |
| `load_prem_rate` | a fraction of each premium | the base premium load, contractual |
| `prem_persistency_override` | a probability, or blank | a pin of the point, which holds in every month (below) |
| `coi_rate_dp` | decimal places, or blank | a pin of the point, which holds in every month (below) |
| `wd_pp` | dollars a month | the withdrawal taken in every month of cover from policy year 2; 0 on every shipped point |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `rop_elected` | a flag | whether the return-of-premium endorsement applies |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

**The premium is an input.** It is fixed at issue, and a policy in force goes on paying
the premium it was issued on, whatever its shadow account now stands at: so the model reads
it from `premium_pp_ann`, as `basiclife/BasicTerm_SE` reads its premium from a table.
`ULSG_US_S`'s funding-premium solve, which finds the level premium that keeps the guarantee
in force from issue, stays `ULSG_US_S`'s (*Departures*, below). On its point 2 it finds
10,803.93, where the column holds the technical notes' `P*`, 10,800.00.

**The two pins**, `prem_persistency_override` and `coi_rate_dp`, are rules of the point,
not state, and `ULSG_US_S` applies each in every month of its frame. So does this model,
and a point restated in force or written later keeps its S point's pins. Point 1 and point
5, the worked-example policy restated 81 months on, pin both: the premium persistency at
1.00 and the declared COI scales to 2 decimals per $1,000, which reconciles the notes'
worked example with their own factor rule. Every other committed point leaves both blank,
and takes the 98% persistency of a level payer and the scales at full precision.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, and so is every column of `ULSG_US_S`'s own that the
  projection reads as a number or a flag: `age_at_entry`, `sum_assured`, `guarantee_age`,
  `premium_pp_ann`, `wd_pp`, `load_prem_rate`, the two pins, `has_surr_charge` and
  `rop_elected`: "model_point_table_sec.csv has no grace_mth_init column";
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more: "model_point_table_sec.csv: duration_mth must be -120 or
  more, a policy issued at most 120 months after the valuation date; it is not at point_id
  [9]". Future new business is written over a horizon, `Data.future_horizon_mth`, 120
  months as shipped, so that no frame runs longer than the projection from issue plus ten
  years: 1,356 months at issue age 18, the youngest the product issues, and 1,032 at 45,
  the youngest the shipped COI scale serves. Set to 0, the Reference refuses future new
  business altogether, and a negative horizon is itself refused;
- `age_at_entry` and `guarantee_age` are each a whole number of years, 0 or more: the
  projection takes the `int()` of each, where `ULSG_US_S` would truncate a guarantee age of
  95.5 to 95;
- `sum_assured` is a number above 0, the face every policy holds, and each of
  `premium_pp_ann` and `wd_pp` a number, zero or more;
- `load_prem_rate`, the share of each premium the load takes, is a number from 0 to 1:
  "model_point_table_sec.csv: load_prem_rate must be a number from 0 to 1; it is not at
  point_id [3]". Past 1 the account would be credited a net premium below 0, which the
  account value's floor at zero absorbs: at a load of 1.5 `ULSG_US_S`'s account-value and
  margin checks fail on each of its points;
- `prem_persistency_override` is blank, where the point takes the rule, or a number from 0
  to 1, a probability, and `coi_rate_dp` is blank, where the point quotes its scales
  exact, or a whole number of decimal places, 0 or more, where `ULSG_US_S` would take the
  `int()` of 2.5;
- `has_surr_charge` and `rop_elected` are each `True` or `False`, as pandas reads those
  words, in any case, so that `TRUE`, `false` and `FaLsE` decode, and project, as `True`
  and `False` do. A blank, a number, 1, 0, 1.0 and 0.0 among them, or any other text is
  refused: one such value turns the whole column into text, where `"False"` and `"0"` are
  true strings, so that every point would read as carrying the flag;
- `av_pp_init` is a number, zero or more. A balance is never negative in force.
  `ULSG_US_S` lets the account value close a month below zero with a loan on an exhausted
  account, through the loaned part's lower credited rate, so the message says what to do:
  restate such a point no later than the last month its account value is still zero or
  more;
- `sg_pp_init` is a number, of either sign: the shadow account is never floored;
- `loan_bal_init` and `cum_prem_init` are each a number, zero or more;
- `grace_mth_init` is a whole number of months, 0 or more;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros:
  "model_point_table_sec.csv: grace_mth_init must be 0 on a policy not yet in force,
  duration_mth 0 or less; it is not at point_id [9]".

The text columns, `sex`, `rate_class`, `premium_type`, `premium_mode` and
`surr_charge_id`, are keys and codes, which the projection decodes or joins on at their
first read, as `ULSG_US_S` does: a pattern or a mode no decode knows raises `ULSG_US_S`'s
message, and a class or a schedule its table lacks raises at its first read. The grace
counter is not held to the account value: `ULSG_US_S` can carry a positive account value
in grace, once the loaned part earns more than the unloaned, so no such rule could be
right.

Three kinds of point read, but `proj_len()` refuses each, naming the point, because each
is a rule of the product, read from `Projection`'s References, not the table's. It checks
them in this order:

- a point to be issued at or past attained age 121, which would never be in cover: "point_id
  9: age_at_entry 121 is at or past charges_cease_age, 121: a policy issued there would
  never be in cover". The age is checked first, so that a point issued past it within a
  year, whose frame would also end before the valuation date, is refused by its age, not
  by a policy month below 0. A point to be issued at attained age 120 is a policy, with a
  year of cover;
- a point at or past the end of the projection at the valuation date,
  `duration_mth ≥ 12 × (121 − age_at_entry)`: "point_id 3: duration_mth 732 is at or past
  the end of the projection, policy month 732, attained age 121";
- a point whose grace expired before the valuation date, `grace_mth_init ≥ grace_months`:
  "point_id 5: grace_mth_init 2 is at or past grace_months, 2: the grace expired before the
  valuation date, so the policy lapsed then, with no value". A policy whose grace has
  expired lapsed at the start of the next month, with nothing to pay, and is not in force,
  and the in-force interface carries no lapse latch.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent or its count from. The tables read at an attained age or a
policy year take their extents from `corridor_age_first()` and `corridor_age_last()`,
`mort_age_first()` and `mort_age_last()`, `lapse_last_year()` and `coi_rate_last_ages()`,
the last attained age of each sex and rate class of `coi_rates.csv`, beyond which each
reads its nearest row. The COI scale is clamped at its last age alone, as in `ULSG_US_S`:
an attained age below its cell's first raises at the first read. The key column is read by
value, so a year written `5.0` is 5, and a key that is blank, text or not a whole number is
refused, naming the file, the column and the lines it is on. So are keys that do not run
one row an age or a year, without a gap or a repeat, policy years from 1, the message
naming each key that repeats, with its lines, and each that is missing: "lapse_table.csv:
the policy years must run from 1, one row a year, without a gap or a repeat; no line holds
policy_year 5", and, inside a cell of the COI scale, "coi_rates.csv: the ages of each sex
and rate_class must run one row an age, without a gap or a repeat; at ('M', 'StdNT'), no
line holds age 61". So is a blank sex or class in the COI scale, and a value that is blank,
text or infinite. A lapse or mortality rate is a probability, held to 0 to 1, since past 1
the monthly rate `1 − (1 − q)^(1/12)` has no real value: "mort_table.csv: mort_rate must be
a number from 0 to 1; it is not on line [44]". A class factor, a guaranteed COI rate and a
surrender charge are held to 0 or more, since below it each projects negative deaths, a
credit for the insurance or a surrender charge that rises once its schedule has run off.
A COI rate is a charge per $1,000 of net amount at risk a year, not a decrement: the
shipped scale is above 1 at every age it charges and 0 at 121, where charges cease, and the
current monthly rate passes 1 from attained age 69, as it should. A corridor factor is held
to 0 or more too, a multiple of the account value that the statute's applicable
percentages hold to 100% or more: one below 1 only makes the corridor bind later, and one
below 0 would leave `db_pp`'s floor on the account value the one thing between an account
below 0 and a death benefit above the face. `class_count()` and
`surr_charge_count()` check the class factors and the surrender-charge schedules, for the
per-point joins that read them, the same way: a class or a schedule blank or on two rows,
and a factor or a charge that is not a number, or is below 0. `surr_charge_count()` also
refuses a run-off that is not a whole number of years, 1 or more, which the projection
divides the charge by, where `ULSG_US_S` divides by zero at 0: "surr_charge_table.csv:
runoff_years must be a whole number of years, 1 or more; it is not on line [2]".
`rop_count()` checks the return-of-premium windows, which are read by membership of their
anniversaries: an anniversary that is blank, text, not a whole number of years, 1 or more,
or on two rows, is refused, and so is a refund ratio or an exercise rate outside 0 to 1.

Each reader asks for its extent or its count before it reads a value, so a projection meets
the checks first. `ULSG_US_S` takes each extent from the key column as pandas reads it,
where a blank key is a missing value the extent skips: the table is cut short, and every
later year or age reads the last good row, without a word. A blank value is a missing value
to it too, which shows in its flows or is lost in a `min` or a `max`: a blank lapse rate
reaches the lapse rate's floor and is read as it, 0.3%, a blank corridor factor reads as no
corridor, a blank surrender charge as none, and a blank COI rate reaches the account
value's floor at zero, which reads it as an exhausted account. Here the cap on the
mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing, as
`ULSG_US_S`'s own does, and each of them is refused before any rate is read.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`ULSG_US_S` and its table by `tests/sec_support.py`, from the `ULSG_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `ULSG_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py ULSG_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 | twin | S point 1 | the technical notes' worked-example policy, in force 300 months, on the anniversary opening policy year 26, at attained age 85, with 2,400.00 of account value, a shadow account of 118,000.00 and 270,000.00 of premiums paid: its `t = 0 … 4` are the worked example's policy months 301 to 305, and its 25th anniversary's window falls at `t = 0` |
| 2–4 | twin | S points 2–4 | issued at `t = 0`: `ULSG_US_S`'s new business, the same policy from issue on the notes' behavioural basis, the lifetime guarantee funded by one premium of $152,300, and a guarantee to attained age 90, underfunded at $6,000 a year, with no endorsement |
| 5 | derived | S point 1 at S month 81 | a month into its grace, in force 381 months, at attained age 91, with 0.428726 in force, no account value, a shadow account of −1,365.21 and a grace counter of 1: it lapses at `t = 1` |
| 6 | derived | S point 2 at S month 240 | on its 20th anniversary, whose 50% window falls at `t = 0`: 911.21 of account value and 211,680.00 of premiums paid |
| 7 | derived | S point 2 at S month 305 | five months into policy year 26, at attained age 85, its account value exhausted and the guarantee carrying it on a shadow account of 244,383.19: its anniversaries fall at `t = 7, 19, …` |
| 8 | derived | S point 3 at S month 731 | its last covered month, at attained age 120, with 4.012e-10 of a policy: a one-row frame, whose `t = 1` is the month its survivors are carried into |
| 9 | future | S point 2, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `ULSG_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `ULSG_US_S` carries into it, each column read as
`ULSG_US_S`'s own formulas read it: the account value as `av_pp_at(d, "BEF_PREM")`, the
shadow account as `sg_pp_at(d, "BEF_PREM")`, the loan as `loan_bal_pp_at(d, "BEF_INT")`, the
premiums to date as `cum_prem_pp(d − 1)` and the grace counter as `grace_mth(d − 1)`. So the
row continues the S projection from there, per policy: point 5 opens with 0.428726 policies,
and point 8 with 4.012e-10. A month by which `ULSG_US_S` has lapsed the policy cannot be
restated, since no policy is in force there to restate: the generator refuses it, naming
the point and the month (*The opening state*, below). Each pin is the S point's. A derived
row's `policy_id` is the S row's with the month appended, `GUL-000001-M81`, and a future
row's carries the months to issue, `GUL-000002-F25`. Row `t` of a generated point is month
`t + source_mth` of its S point. All nine are on the anchor cell M60 / StdNT / $500,000,
because the illustrative COI scale covers that cell alone, from attained age 45, so a point
on any other sex or class, or issued younger than 45, needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `ULSG_US_S` already names:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it, or 0 once the policy has lapsed for insufficiency;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_MAT"`, the count before any maturity, `ULSG_US_S`'s meaning: the `"BEF_DECR"`
  count, since the contract never matures and no event of the month separates the two.

Any other timing raises. `ULSG_US_S`'s cell of the name returns `pols_if(t)` for every
timing, and nothing calls it. `"BEF_NB"` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `ULSG_US_S` counts the issued policies, and this model counts them as new
business, not yet in. As in `UL_US_SEC` and `VUL_US_SEC`, `basiclife/BasicTerm_SE`'s
`"BEF_MAT"`, the count at the start of the month before its new business, is not adopted:
the name keeps its S model's meaning.

The month's decrements are `ULSG_US_S`'s, in its order, all at the end of the month: deaths,
then surrenders out of the survivors, then return-of-premium exercises out of those left,
and, in the month before a grace expires, every policy still left, `pols_lapse_grace(t)`,
which terminates with no value. The lapse latch, `is_lapsed(t)`, then shuts from the next
month, and the count is 0 from there.

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `"BEF_NB"`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's four decrements in `ULSG_US_S`'s order. Each account's
opening balance forms the previous month's close the same way, the same operations in the
same order as the closing cell `ULSG_US_S` calls for: `av_pp_at(t, "BEF_PREM")` from its own
value at `t − 1` and month `t − 1`'s net premium, withdrawal and fee, expense charges, cost
of insurance, zero floor and interest, where `ULSG_US_S`'s account value ran through six
cells a month; `sg_pp_at(t, "BEF_PREM")` likewise, where `ULSG_US_S`'s shadow account ran
through six; and `loan_bal_pp_at(t, "BEF_INT")`, a month's interest on its own value at
`t − 1`, where `ULSG_US_S`'s loan ran through two. The premiums to date call themselves at
`t − 1`, and the grace counter and its latch are one chain between them, as in
`ULSG_US_S`. The mortality improvement factor reads itself a year back, a chain of one cell
a year: past 20 years, from `t = 252` on, it is the factor of month 240, so it is at most 22
cells deep.

On a model just read, a cold `net_cf` in the last month of point 1's 432-month frame runs
447 cells deep, against 2,111 for `ULSG_US_S`'s point 1: 16 cells above the chain back to
`t_entry()`. The other committed points run 14 to 18 above theirs: 747 cells on points 2,
3, 4 and 9, each on the books for 732 months. At the longest cover the contract allows,
issue age 18 and 1,236 months, it runs 1,252 deep at the valuation date and 1,256 issued
120 months after it, 17 and 21 above the chain: every chain stops at the issue month, but in
its first month the mortality of a point issued later reads the improvement factor of the
valuation years before its issue. That is about 313 KiB of C stack at gcc's 255 bytes a
level. Each chain's head called alone, on a read of its own with every chain cold, the
loan's, the premiums', the account value's, the shadow account's, the grace counter's with
its latch and the count's, runs at most 12 cells above its chain on the committed points,
the count's the deepest, which runs 13 above at the longest cover at the valuation date and
17 issued 120 months on; the improvement factor asked alone runs at most 27 levels, from
`t = 252` on. Each report evaluates its columns in ascending `t`, and on a model just read
the committed points' four reports and three checks run that way under a recursion limit
of 16, and `ULSG_US_S`'s under 14. A point issued 120 months on needs 19, since its first
month reads the improvement factor of the ten years before it. Exported by modelx, with
the recursion limit set after the import, the cold `net_cf` of the last month needs a
limit of 916 on point 1, 1,516 on points 3 and 9, and 2,524 at the longest cover, issued
now or 120 months on, and the ascending sweep 54, against 3,929 to 5,977 and 52 for
`ULSG_US_S`'s points.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `ULSG_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_rop(t) + pols_lapse_grace(t) + pols_maturity(t)
```

at every `t` of every frame, the month of a lapse and every month after it included, and
`pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < charges_cease_mth()`, where
`charges_cease_mth() = 12 × (charges_cease_age − age_at_entry)` is `ULSG_US_S`'s frame from
issue, the first month at attained age 121. Outside it, before issue and from
`t = proj_len()` on, every count, balance, premium, withdrawal, charge, decrement rate,
decrement, claim and cash flow is zero and every flag false, the grace counter and the
return-of-premium anniversary are the int 0, and `status` says why: `"PRE_ISSUE"` before
issue and `"CEASED"` from `t = proj_len()` on. Only the two clocks, the inputs read on the
valuation clock and the dynamic lapse multiplier's neutral 1.0 hold values there, and the
month after the frame holds three exceptions more, below. No count evaluates a decrement
rate there, and no table is read at a policy year, an attained age or an anniversary the
policy does not have: `sum_assured_at`, `prem_persistency`, `premium_pp`, `cum_prem_pp`,
`wd_pp`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `sg_coi_pp`, `maint_fee_pp`,
`sg_maint_fee_pp`, the timings of the two accounts and the loan, `surr_charge_rate`,
`mort_rate`, `lapse_rate_base`, `lapse_rate`, the four decrements and `expenses` are zero,
`is_premium_mth` false and `grace_mth` and `rop_anniversary` 0, before any table or rate is
read, and every other value is zero through them. `lapse_rate_dyn_mult` is 1.0 there,
before it reads the guarantee or the account value. Each table read at a policy year, an
attained age or an anniversary has one reader keyed by it, called inside cover only, so on
point 9, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below 1
or an attained age below 60. The mortality improvement rate is the one cell read at an
attained age before issue, on a point written later, and it reads no table: it grades the
improvement of the valuation years before issue at the age the cohort has reached in each.

**The end of the projection.** The frame ends at `charges_cease_mth()` because premiums and
charges cease at attained age 121, not at an event of the contract, whose cover continues
there [S7]. The shipped mortality table reaches 1.0 at attained age 120, but improvement
takes the rate below it: on a point issued at or after the valuation date at attained age
60, 20 years of 1% leave the rate at attained age 120 at 0.817907, and on point 1, whose
years of improvement fall from attained age 85 on, at 0.946302. So lives can survive the
last month, and `ULSG_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and
`av_change()` read the account value in force entering month `t + 1`, and
`pols_lapse_grace()` the lapse latch of month `t + 1`, which in the last month is
`t = proj_len()`. So the three opening values read there, the count carried in
(`pols_if_at(t, "BEF_NB")`, and through it `pols_if(t)`), the account value carried in
(`av_pp_at(t, "BEF_PREM")`) and the latch (`is_lapsed(t)`), are defined for
`0 ≤ duration_mth(t) ≤ charges_cease_mth()`: in the month after the frame they are the
survivors of the last month, the account value they carry and the latch the last month
leaves, `ULSG_US_S`'s own values there. Everything else is zero or false there, the shadow
account included, which no cell reads there, and the expenses, which would otherwise fall
on the carried count. Nothing reads past it: `av_change()`, `pols_lapse_grace()` and the
three checks' residual cells, which read `t + 1`, are zero outside cover before they read
it. At the shipped assumptions the survivors at `proj_len()` are 3.48e-10 of a policy on
the twin of point 3, `ULSG_US_S`'s own, and 0.0 on every other committed point: points 1,
2, 4, 5, 6, 7 and 9 lapse before the end, and point 8, whose improvement restarts at its
valuation date, dies in its one month at the table's 1.0.

**Rates stay rates.** The annual mortality rate is capped at 1.0, as in `ULSG_US_S`,
`min(q, 1.0)` with its bound second, so that a missing input stays missing. On no committed
point does the product pass 1, since all are on StdNT, whose factor is 1.0: the cap binds
on the tobacco classes, whose factors take the table past 1, first on StdTob at attained
age 107, 1.75 × 0.582849, at an A/E of 1.0 with improvement off.
The annual lapse rate keeps `ULSG_US_S`'s floor of 0.3% and cap of 50%, each bound written
first, `min(lapse_rate_cap, max(lapse_rate_floor, rate))`, and `Data` holds each base rate
to 0 to 1, so the rate stays a probability while `lapse_rate_cap` is at most 1. On the
committed points the rate before its bounds is at most 0.04, so the cap never binds there,
while the floor binds from policy year 21 on, where the base rate is 0.75% and the
multipliers take it below 0.3%.

## The opening state

`ULSG_US_S` opens its in-force point 1 from four columns, the account value, the shadow
account, the loan and the premiums to date entering its first month, and reads the grace
counter of the month before its frame as 0. The worked example's policy is not in grace at
its policy month 300, so point 1 needs no more, and its twin opens the same way. A policy
valued in any month of its life needs all five columns, each what `ULSG_US_S` carries into
that month. The committed points show what each changes, each compared with the same row
read with the column at what `ULSG_US_S` assumes or at 0, or, for the shadow account,
floored at zero as the account value is:

- **`grace_mth_init`.** Point 5 is `ULSG_US_S`'s point 1 a month into its grace, at its
  month 81. It carries a counter of 1, which its first month, whose deduction fails again,
  advances to 2: the grace has run its two months, every policy left at the end of month
  0, 0.423179 of them, terminates, and `pols_if(1)` is 0.0, as `ULSG_US_S`'s `pols_if(82)`
  is. Read with the counter at 0, as `ULSG_US_S` reads the month before its frame, the grace
  would open afresh at `t = 0` and the policy would lapse a month late, with 0.423179
  policies still in force at `t = 1`.
- **`sg_pp_init`.** The same row's shadow account is −1,365.21, below zero: the guarantee
  has failed, and the negative balance is the catch-up shortfall. Month 0's charges take
  it to −5,551.43, so the catch-up premium that would restore the guarantee is 6,034.16.
  Floored at zero, as the account value is, the shadow account would close month 0 at
  −4,180.11 and the catch-up premium would be 4,543.60.
- **`cum_prem_init`.** Point 1 has paid 25 annual premiums of $10,800, 270,000.00, and its
  25th anniversary's window falls at `t = 0`: the refund there is the premiums paid,
  month 0's included, 280,800.00, capped at 40% of the face, 200,000.00, so the 0.099303 of
  a policy that exercises is paid 19,860.68 and `net_cf(0)` is −12,383.41. With the column
  at 0 the refund would be month 0's premium alone, 10,800.00, the refunds 1,072.48 and
  `net_cf(0)` 6,404.80. Point 6, on its 20th anniversary, has paid 211,680.00, and its 50%
  window refunds 111,132.00 a policy at `t = 0`; with the column at 0 it would refund
  5,292.00.
- **`av_pp_init`.** Point 6 also holds 911.21 of account value entering month 0, so that
  the account closes the month at 7,098.16, the cash surrender value of a policy that
  surrenders then, where read as 0 it would close at 6,181.24.

`loan_bal_init` is 0 on every committed point, as on every point of `ULSG_US_S`'s. A loan is
read where `ULSG_US_S` reads it: the loaned part of the account value earns the loan credit
rate, both of the guarantee's tests net it, and every claim deducts it.

**A row in its grace, and none after a lapse.** At the shipped assumptions `ULSG_US_S`'s
point 1 exhausts its account at its month 3, the guarantee carries it through month 79,
its grace opens at 80, and it lapses at the start of 82, with no value:

| S month | `pols_if` | `grace_mth` | `is_lapsed` | `sg_pp_at(t, "BEF_PREM")` | `status` |
|---|---|---|---|---|---|
| 79 | 0.439333 | 0 | `False` | 6,871.71 | `IN FORCE - GUARANTEE` |
| 80 | 0.434093 | 1 | `False` | 2,779.48 | `GRACE` |
| 81 | 0.428726 | 2 | `False` | −1,365.21 | `GRACE` |
| 82 | 0.0 | 0 | `True` | −5,551.43 | `LAPSED` |
| 83 | 0.0 | 0 | `True` | −9,756.36 | `LAPSED` |

A row restated at 80 carries a counter of 0, and one at 81 the counter of 1 that point 5
carries, `ULSG_US_S`'s `grace_mth(80)`; each lapses where `ULSG_US_S` does, at `t = 2` and
`t = 1`. No row is restated at 82 or later. The policy has lapsed: `ULSG_US_S`'s count there
is 0 and its latch shut, and the in-force interface carries no latch, since a lapsed policy
is not in force. So the generator refuses every month by which `ULSG_US_S` has lapsed the
policy, naming the point and the month, and `proj_len()` refuses a hand-made row whose
counter is at or past `grace_months`, as a row at 82 would carry 2. A row at 83 would carry
a count of 0 and a counter of 0, since `ULSG_US_S`'s counter reads 0 once the policy has
lapsed, and the model's rules accept that as a point with no policy in force: so it is the
generator, which reads `ULSG_US_S`'s latch, that refuses it. Points 2 and 4 lapse at their
months 504 and 236, and the last months each can be restated at, in its grace with a
counter of 1, are 503 and 235.

A counter carried in resets where `ULSG_US_S`'s does, in the first month whose deduction no
longer fails: a grace can end without a lapse where a scheduled premium falls due and
carries the deduction. `ULSG_US_S`'s point 4 paying $6,150 a year, a variant the tests use,
enters its grace at its month 239, and the anniversary premium at 240 cures it. Restated at
240 with a counter of 1, it resets at `t = 0` and stays in force; restated at 243, where its
second grace is a month old, it lapses at `t = 1`. With improvement and inflation set to 0
in both models, each is `ULSG_US_S`'s projection from there, cell by cell.

## Departures from ULSG_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year, an attained age or an
anniversary answers for the months outside cover. Of `ULSG_US_S`'s 139 cells in
`Projection`, 55 are unchanged, 34 have a new docstring only, most of them to say what `t`
now counts, and 46 are rewritten; four, the funding-premium solve, are removed, none is
renamed, and 25 cells are new, 160 in all. A cell of `ULSG_US_S`'s that this model lacked
would fail the twin identity, which names each of the four with its reason. `ULSG_US_S`'s
References `solve_tol`, `solve_max_doublings` and `math`, which only the solve and the
checks' `math.isclose` read, are dropped. Of `Data`'s nine cells, `model_point_table` is
rewritten to check the table as it reads it, three readers have their `read_csv` call
wrapped and `mort_table` its docstring; nine cells are new, 18 in all, and so is the
Reference `future_horizon_mth`, 120. The cap on mortality, `min(..., 1.0)`, is
`ULSG_US_S`'s own and no departure, and so are the shadow account never floored, the lapse
rate's two bounds in `ULSG_US_S`'s order and improvement from the start of the projection,
which here is the valuation date.

| Cells | `ULSG_US_S` | `ULSG_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `charges_cease_mth` | `12 × (charges_cease_age − x) − duration_mth_init()`, the months from the first projected month | `charges_cease_mth() − duration_mth_init()`, the months from the valuation date; raises, in this order, for a point to be issued at or past attained age 121, one at or past the end of the projection and one whose grace has expired | `charges_cease_mth()` is new and is `ULSG_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left, or none in cover, has no frame, and a policy whose grace has expired lapsed before the valuation date |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse`, `pols_rop`, `pols_lapse_grace` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`; `"BEF_NB"` the count before the month's new business, formed from the month before in the cell itself, and `"BEF_MAT"` the `"BEF_DECR"` count, as in `ULSG_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month; the chain is one cell a month |
| `av_pp_at`, `sg_pp_at`, `loan_bal_pp_at` | `av_pp_init()`, `sg_pp_init()` and `loan_bal_init()` at `t = 0`, then the previous month's closing cell: chains of six cells a month, six and two | the same openings at `t_entry()`, then the previous month's close formed in the cell itself, `ULSG_US_S`'s arithmetic in its order, its floor written first; every timing zero outside cover but the account value's opening, carried into `t = proj_len()` | Every chain one cell a month, since a compiled model runs it on the C stack |
| `cum_prem_pp`, `grace_mth`, `is_lapsed` | opened at `t = 0` from `cum_prem_init()`, a counter of 0 and a latch that is false | opened at `t_entry()` from `cum_prem_init()` and `grace_mth_init()` on a point in force, and from the issue values on any other; the latch false at `t_entry()`, and carried into `t = proj_len()` | A policy in force brings in its premiums to date and the months it has spent in grace; a policy that has lapsed is not in force |
| `premium_freq`, `is_premium_mth`, `prem_persistency`, `premium_pp`, `lapse_rate_pattern_mult` | branches on the text of `premium_type()` and `premium_mode()` | branches on three decodes, `is_level_premium()`, `is_single_premium()` and `is_ten_pay_premium()`, each reading its column from `model_point()`, as `premium_freq` reads the mode | No monthly cell compares text, and no projection cell calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `ULSG_US_S`'s message |
| `prem_persistency`, `wd_pp` | the model point's `prem_persistency_override` and `wd_pp` columns read in the monthly cell, the pin through `pd.isna` | read once a point: the pin as a value and a flag, `prem_persistency_override()` and `has_prem_persistency_override()`, and the withdrawal by `wd_pp_mth()` | A monthly cell tests a flag rather than a missing value, and reads no model point column in its own formula; `coi_rate_dp`, already read once a point, is `ULSG_US_S`'s |
| `class_factor`, `coi_rate_scale` | joined on the label accessors | the same joins, on keys read from `model_point()`: the class factor once `data.class_count()` has checked its table, the COI scale through its one reader, once `coi_rate_last_age()` has | A blank factor, a missing value to `ULSG_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and is refused, as is one below 0; a blank COI rate would reach the account value's floor |
| `corridor_factor`, `mort_rate`, `coi_rate_guar`, `lapse_rate_base` | the table read in the monthly cell, at `age(t)` or `policy_year(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the age or the year — `corridor_factor_at`, `mort_rate_base_at`, `coi_rate_guar_at` and `lapse_rate_base_py` — with `ULSG_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the values, called inside cover only | No table is read at an age or a year the policy does not have, each is read once an age or a year, and a blank, text or fractional key, keys that repeat or leave a gap, a value that is not a number, a lapse or mortality rate outside 0 to 1 and a corridor factor or a COI rate below 0 are refused by name, where `ULSG_US_S`'s extent skips a blank key and cuts the table short, and a blank value is a missing value |
| `surr_charge_rate` | the schedule's row read in the cell | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one reader for each of the schedule's two columns, each asking `data.surr_charge_count()` first | The same numbers on any schedule, with no table read in a monthly cell; a blank charge, which `ULSG_US_S`'s `max` reads as none, a charge below 0 and a run-off that is not a whole number of years, 1 or more, are refused |
| `rop_anniversary`, `rop_ratio`, `rop_rate` | the return-of-premium table read in each | three readers keyed by the anniversary, `is_rop_anniv(y)`, `rop_ratio_anniv(y)` and `rop_rate_anniv(y)`, each asking `data.rop_count()` first | No monthly cell reads a table; an anniversary that is not a whole number of years, 1 or more, or is on two rows, and a refund ratio or an exercise rate outside 0 to 1 are refused |
| `sum_assured_at`, `is_premium_mth`, `prem_persistency`, `premium_pp`, `cum_prem_pp`, `wd_pp`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `sg_coi_pp`, `maint_fee_pp`, `sg_maint_fee_pp`, `surr_charge_rate`, `grace_mth`, `rop_anniversary`, `mort_rate`, `lapse_rate_base`, `lapse_rate_dyn_mult`, `lapse_rate` | unguarded: no `ULSG_US_S` frame has a month before issue | zero, false or the int 0 outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_dyn_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2. At `t = proj_len()` nothing is charged, paid or withdrawn. The six `age(t) >= charges_cease_age` branches stay `ULSG_US_S`'s, never taken in cover, since the frame ends where the charges do |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `status` | `"LAPSED"`, `"GRACE"`, `"IN FORCE - GUARANTEE"` or `"IN FORCE"` | the same, and `"PRE_ISSUE"` before issue and `"CEASED"` from `t = proj_len()` on | Labels for the months outside cover, which `ULSG_US_S`'s frame never holds |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_sg_roll_fwd`, `check_margin` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)`, `check_sg_roll_fwd_resid(t)` and `check_margin_resid(t)`, each a `float` over the larger side and 1; a residual that is not a number fails, and one that is not real raises, as `ULSG_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the lapse term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `ULSG_US_S`'s identity is off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its check fails on a projection that is right; on every shipped point no loan is outstanding, and the two agree |
| `result_pols` | `pols_if`, the four outflows, the maturities and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `solve_len`, `sg_pp_solve`, `guar_min_sg`, `no_lapse_premium` | the funding-premium solve, a bisection over the level premium of a replay of the shadow account | removed | The premium is an input fixed at issue (below) |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`,
`grace_mth_init`, the new opening-state accessor, and `coi_rate_last_age`, the extent of a
point's COI scale.

**The funding-premium solve is not in this model.** `ULSG_US_S` implements the technical
notes' complete algorithm, a bisection over the level annual premium of a replay of the
shadow account with decrements off, as a side calculation that nothing in its projection
reads, and its tests check it. It is an issue-time calculation: it finds the premium a
policy is issued on, and a point in force carries that premium from issue, in its
`premium_pp_ann`. So this model reads the premium from the column, and the solve stays
`ULSG_US_S`'s. Kept unchanged here, the solve would answer a question no point valued later
asks. It replays the shadow account from the frame's first month, not from the policy's
issue, so on a point in force it solves from the valuation date: 11,961.02 on point 6, which
was issued on 10,800.00 and is still paying it, and 31,033.42 on point 1, from its shadow
account of 118,000.00 at month 300, as `ULSG_US_S` finds on its own point 1. On a point
written later, whose months before issue enter its minimum at zero, it finds no premium at
all and raises. And its cells take the premium as a float argument, which a compiled model
could cache only in a Python dictionary. To solve a policy's premium from a later state,
give `ULSG_US_S` a point carrying that state, as its point 1 does: it solves from that
point's own start.

Of the cash flows, the change of clock moves the maintenance expense, and `net_cf` with it,
and on a point restated or written later, through mortality improvement, the counts and
every flow they weight. Point 1's `expenses(t)` less its claim expense is `ULSG_US_S`'s
divided by `1.025^25` at every `t`. Point 9's maintenance expense is `1.025^2` above
`ULSG_US_S`'s point 2's, month for month, and `1.025^3` in the last month of each policy
year, where the valuation year has stepped and the policy year has not; its acquisition,
9,825.60 a policy, is `ULSG_US_S`'s exactly.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 2, 3 and 4, issued
  at the valuation date, every cell of `ULSG_US_S`'s agrees at every argument `ULSG_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose
  meaning changed, and the four cells of the funding-premium solve, which this model does
  not have; a cell this model lacked would fail it otherwise. The identity holds on any
  count, since `ULSG_US_S` already charges acquisition on the policies issued. The same
  suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The in-force twin**, in `tests/test_guaranteed_ul_us_sec.py`: point 1 opens with
  `ULSG_US_S`'s own opening balances and no grace, and with expense inflation set to 0 in
  both models it is `ULSG_US_S`'s projection from `t = 0`, in every cell and every report,
  to 1e-9 relative with no absolute floor; at the shipped assumptions the two part in the
  maintenance expense alone, in the inflation factor, the expenses, the expense margin and
  the net cash flow, and in no other cell. So the goldens `tests/test_guaranteed_ul_us.py`
  asserts on point 1 — every cell of the worked example's five rows, the notes' NAAR
  constants, the account value's exhaustion at `t = 3` and the guarantee carrying the
  policy from `t = 4` — hold here, with no number restated.
- **The splice**: each `ULSG_US_S` point restated in force at a month either side of its
  events continues the S projection from there, in its four reports, column by column, and
  in every other cell the two share, the two accounts at every timing, the loan, the grace
  counter, the latch and the checks' verdicts among them, to 1e-9 relative with no absolute
  floor, since its counts fall far below 1e-7. It leaves out those the twin identity skips
  and `ULSG_US_S`'s own opening values and frame. The months straddle the product's events:
  the first anniversaries; the surrender charge's last month; the account's exhaustion under
  the guarantee; a grace that opens in the valuation month, and a counter carried into it,
  which lapses the policy a month on; the 20th and 25th anniversaries' windows, at `t = 0`
  and, on a row valued mid-year, at `t = 1`; the month the shadow account's net amount at
  risk is floored; and the last covered month, whose `t = 1` is the month the survivors are
  carried into. So are variants of S's points, in a copy of S's table that is never
  committed, each changing S's columns only and each with input rows of its own, for
  branches S's own points do not reach: ten-pay premiums, quarterly; withdrawals that outrun
  an exhausted account, semi-annually; a loan under a funded account, in force at 300; a
  loan of $10,000 on S point 1's exhausted account, in force at 300, which takes the account
  entering 65 of its months below 0 and decides the guarantee's test in two, so that its
  twin and its row restated at 3, the last month its account is still 0 or more, compare
  `ULSG_US_S` where the loan's credit and the guarantee's test both read the debt; a single
  premium large enough for the corridor to bind, on a COI scale that stops short of its
  cover, so that its later ages are read at its last; a guarantee to 99, monthly, with
  neither a surrender charge nor the endorsement; each pin alone; issue age 40, below the
  mortality table's first age, on a second surrender-charge schedule; S point 4 paying
  $6,150 a year, whose anniversary premium cures its grace; S point 2 paying $100 a year,
  too little for its first month's deductions, issued 13 months on, the one row in grace
  from its issue month, which reads the grace counter's base there; and S point 2 with a
  guarantee to 100, the lifetime guarantee's age the splice sets, met exactly, where the
  guarantee to 99 meets it a year short. Between them they carry both sexes and every class.
  The twin of each variant issued at the valuation date is compared with its S point cell by
  cell, as a row issued there is, so that an issue rule only a variant takes at `t = 0` is
  reached; the two variants of point 1, in force 300 months, are splice cases from `t = 0`,
  as point 1 is. The References are set in both models: expense inflation and mortality
  improvement at 0, the two inputs on the valuation clock that move a number; the mortality
  A/E at 0.56, which leaves survivors at the end of every frame that does not lapse; a
  premium tax of 2%, the one assumption the product ships at zero; and the lifetime
  guarantee's age at 100 and the single premium's lapse factor at 0.65, each set apart from
  the Reference it ships equal to, `charges_cease_age`'s 121 and the dynamic lapse
  multiplier's 0.6, so that a cell reading the one for the other shows. A second fixture, on
  References of its own, binds the two bounds `ULSG_US_S` ships idle, the lapse rate's cap,
  lowered to 1.25%, and the credited rate's floor, under a declared rate of 1.5%. Charges
  cannot cease in cover, since the frame ends where they do.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every line of the model the full grid
  reaches, every opening-state column, every kind of valuation month, every premium pattern
  and mode, and every floor and cap the grid binds, each checked by the raw value it bounds,
  and a test asserts that they do. It also records each side of every `min` and `max` the
  core's rows bind, by the values each call compares, and asserts that every side binds
  there but the seven bound by tests of their own: the two bounds `ULSG_US_S` ships idle, on
  the second fixture; the cap on mortality; the three clamps of the tables shorter than the
  cover; and the shadow account residual's floor of 1, where its sides are small. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs the full
  grid too.
- **Future new business**: issued 1, 12, 13 and 25 months after the valuation date, S point
  2 is the S projection moved on, cell by cell, and so are S points 3 and 4 and each
  new-business variant issued 13 months on, whose months before issue reach policy year
  −1; with zeros before issue in every report and no decrement rate evaluated there.
- **How it computes**: each row the splice and the future business compare is first run on
  the books and scanned: no cell has been called at a negative month, none evaluated from
  `t_entry()` on has read a month before it but the mortality improvement factor, which on
  a point written later reads the valuation years before its issue, by design, and none
  evaluated at month `t` has read a month later than `t + 1`. Every monthly cell holds its
  value outside cover and reads no table there, before issue and at `proj_len()`, on the
  committed points and on the splice. On a fresh read of the committed model the policy
  clock is a closed form, every point's reports run under a lowered recursion limit, which
  a recursion backward over the frame would exceed, no projection cell has read a label
  accessor, and the solve's cells are absent. And every chain is called cold, each call on
  a read of its own: `net_cf` in the last month on the committed points, and each chain's
  head on the twin of point 3, and both on the two rows of the longest cover, one issued
  now and one 120 months on, whose frames are asserted first, modelx's stack trace
  counting no more than one cell a month back to `t_entry()` and a fixed overhead, which a
  chain of two cells a month would exceed, while the improvement factor stays within a
  bound of its own; the ascending sweep at the longest cover belongs to the full grid.
- **Counts, validation and regeneration**: the roll-forward closes, the month of a lapse and
  the last month included, `"BEF_MAT"` is the `"BEF_DECR"` count, and `pols_if_at` refuses a
  timing it does not have; `result_pols()` is `ULSG_US_S`'s, column for column, with
  `pols_new_biz` beside it; multiplying `policy_count` by 2.5, with every assumption that
  ships at zero switched on, scales every counted cell and moves no per-policy value; each
  malformed row is refused naming its point, by its own rule, and so is a projection of it,
  a flag written 1, 0, 1.0 or 0.0 among them; a flag written `True` or `False` in any case
  decodes, and projects, as written; each assumption table with a malformed key, a policy
  year below 1 among them, or a value that is not a number, is refused naming its file,
  its column and its lines, and so is one with a value outside its range, a corridor
  factor below 0 among them, while the bounds of each range are read; a `premium_type` or
  `premium_mode` no decode knows raises `ULSG_US_S`'s message; the horizon is a Reference,
  which at 0 refuses any future business, saying so; a point to be issued at or past
  attained age 121, one at or past the end of the projection and one whose grace has
  expired are refused by `proj_len()`, in that order, a counter at `grace_months` and one
  past it among them, and with `grace_months` moved to 3 a counter of 3 is refused and one
  of 2 projects, and a point issued at attained age 120 has a year of cover; every state
  `ULSG_US_S` reaches on either splice's inputs,
  restated in force by the generator at the edges of its windows, or with
  `USLIB_SEC_FULL=1` at every month before its lapse, is read by `Data` and has a frame,
  but the one it refuses by name, an account value below 0 under a loan on an exhausted
  account, which also fails `ULSG_US_S`'s own checks; the edges of the interface are
  accepted, the keys of every keyed table and the integer columns written as floats among
  them; the committed table is what `ULSG_US_S` generates, and the generator refuses a
  month after a lapse; and each committed derived and future row opens with `ULSG_US_S`'s
  own count and state at its month and continues its S point per policy, frame by frame,
  at the shipped assumptions.
- **The opening state and the rest**: point 5 opens from its own grace counter and shadow
  account, and the twin of point 1 from its own premiums to date, and read as `ULSG_US_S`
  would open them they give the numbers above; mortality improvement, expense inflation and
  the declared rate run on the valuation clock, the improvement 0.9801 in point 9's issue
  month; a check whose residual is not a number fails, the NaN sent through a Reference the
  counts read, the improvement rate, and through two that reach a residual without them, the
  declared rate and the shadow account's rate, and each check decides as `ULSG_US_S`'s
  `math.isclose` does where its sides fall below 1; a lapse rate past 1, under a cap raised
  past it, makes the account value's and the margin's checks raise in both models, the
  residuals being floats; on a point whose loan comes to exceed its cash value the margin
  identity holds where `ULSG_US_S`'s fails; acquisition falls on new business alone, per
  policy issued and not inflated; a StdTob point at an A/E of 1.0 with improvement off,
  whose product first passes 1 at attained age 107, is `ULSG_US_S`'s in every cell, the
  capped months included, as new business and restated in force, the rate there is the float
  1.0 in both models, every life in force dies in that month and nothing is in force after
  it; a NaN that reaches the cap stays NaN, sent through the A/E or the improvement rate,
  each a Reference, and so does one that reaches a bound written second; a corridor table
  cut to ages 61 to 94 and a mortality table ended at 110, each read past its ends at its
  nearest row, leave two variants `ULSG_US_S`'s points in every cell, each clamp binding
  with an effect; each pin holds in every month and alone; the premium is the column's, and
  the solve is `ULSG_US_S`'s; the docstrings describe this model and not `ULSG_US_S`, their
  tables read into the right cells, and they parse under docutils with nothing rendered
  wrongly; both models read the one copy of each assumption table, and every other Reference
  of either Space is `ULSG_US_S`'s, value for value, but the horizon this model adds and the
  solve's tolerance, its limit of doublings and the `math` module, which it leaves out with
  the solve; the grace's length, which ships equal to the failed guarantee's lapse
  multiplier, 2, is set apart from it at three months, and the twins of `ULSG_US_S`'s points
  1, 2 and 4 are its points then, each through its lapse, a month later; the points of a
  block sum row by row; an extract without the generator's three columns, relabelled,
  projects the same numbers; and `run_sec.py` prints the model's numbers.

```bash
python -m pytest tests/test_guaranteed_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_guaranteed_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k ULSG_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
