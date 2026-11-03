# In-Force Implementation Notes

**Status:** Draft, 2026-11-03. `VUL_US_SEC` is [`VUL_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year, and policies to be written in the ten
years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
The product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in
`BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is
still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `VUL_US_S` on another time axis, and it reads `VUL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements come from four registered
> prospectuses [S1] [S2] [S3] [S4]. The separate-account return scenario, the dominant
> assumption for this product, is **[std]** in full, and so are the current COI scale,
> the mortality table, the lapse vector and every expense. Replace them with company data
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/variable_ul/run_sec.py            # point 1: the anchor cell, in force
python products/variable_ul/run_sec.py 6          # point 6: the loan cell, six months on
python products/variable_ul/run_sec.py --block    # every model point, summed row by row
```

The first prints, as rows `t = 0 … 11`, the account value roll-forward and the cash flows
`run.py` prints for `VUL_US_S`'s point 1, the worked example's month at `t = 0` among
them, each table line for line the same, and then the counts and rates behind them. Point
1 is in force 24 months at the valuation date, as it is at the start of `VUL_US_S`'s own
projection, so its row `t = 0` is the worked example's month here as there. Three lines to
the same thing for point 6:

```python
import modelx as mx
model = mx.read_model("products/variable_ul/VUL_US_SEC")
model.Projection[6].result_cf()
```

`Projection` takes a `point_id`, as in `VUL_US_S`. Its four result tables are indexed by
`t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `VUL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — the **gross (policyholder) view**, income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `VUL_US_S`'s per-policy account value roll-forward, in the columns and order of the technical notes' worked example, with zeros before issue |
| `result_net()` | `VUL_US_S`'s **net-of-account (general-account strain) view**, derived from the same run, under the notes' own column names |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `VUL_US_S`'s two monthly decrement rates, written 0 outside cover |

`VUL_US_S`'s three self-checks, `check_av_roll_fwd()`, `check_margin()` and
`check_net_view()`, run over the same frame.

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
  date to the end of the projection, the last month at attained age 121.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month from issue,
  `duration_inforce + t`, and the contract runs on it:
  `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1` and
  `age(t) = age_at_entry() + duration(t)`, as in `VUL_US_S`. `BasicTerm_SE` reaches the
  same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`VUL_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force points there: points 1 and 2 at 24 months and point 4 at 120, with
their subaccounts, their fixed option and their loan. What the valuation clock adds is
that `t = 0` is one instant for every point, that a point may be issued after it, and that
a point in force brings in what its past has left it: the loan account, which has grown
apart from the debt since the loan was taken, and the face its withdrawals have left.

Point 4 is `VUL_US_S`'s in-force cell with a loan, in force 120 months. At `t = 0` it is
on the anniversary that opens policy year 11, at attained age 55, with a fixed-option
balance and an $8,000 loan at the preferred loan rate, and its frame has 804 rows,
`t = 0 … 803`. Point 6 is the same policy six months on, in force 126 months: policy year
12 begins at `t = 6`, where the attained age steps to 56, and its frame has 798 rows.
Point 9 is `VUL_US_S`'s point 3 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first premium of $500.00 falls at `t = 25`, and its frame has 949 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the surrender charge by policy year and the lapse spike at its cliff, policy month `12 × runoff_years`; the loan's preferred rate from policy year 10; the guaranteed COI scale, the base lapse rates and the premium persistency scale by policy year; the corridor factor and the mortality rate at the attained age; the single premium and acquisition in the issue month; premiums, withdrawals and monthly deductions ceasing at attained age 121; the end of the projection at policy month `omega_mth()`; the at-issue pricing path behind the funding ratio, keyed by the policy month from issue | the separate-account return scenario, `gross_return_mth(t, i)`; the declared fixed rate, `crediting_rate_ann(t)`, flat as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 0 as shipped; the two first-month pins, which apply at `t = 0`, the valuation month |

**The return scenario** is an economic input. `VUL_US_S` keys `scenario_table.csv` by its
projected month `t` already, so the table is on the valuation clock as it stands: a
scenario is a path of the economy from the valuation date, the same month for every point
of a block, however old the policy. On `VUL_US_S`'s own in-force points the two models
read the same months, because `VUL_US_S` opens them at its own `t = 0`. A point restated
at a later month reads the path from its own valuation date instead. `VUL_US_S`'s point 1
restated in force at its month 12 reads month 0 of `WE` as shipped, the worked example's
month, +1.00% on its first subaccount, where `VUL_US_S` in its month 12 reads the level
path, 0.4868% a month. Its first subaccount closes month 0 at 34,396.04 against
`VUL_US_S`'s 34,221.25, 174.79 above, its account value 46.71 below, and its `net_cf` is
0.152 above in month 0 and 0.129 above in month 100. On a copy of `WE` re-based to month
12 the row is `VUL_US_S`'s projection exactly. That is the clock at work, not a fault: a
restated row continues the S projection only on a scenario re-based to its own valuation
date, so the tests give every restated or future row a re-based copy of its own
(*Tests*, below). The committed derived rows all read the flat `LEVEL6`, on which the
month makes no difference.

**Expense inflation** keeps `VUL_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. It ships at 0, as in `VUL_US_S`, since the variable-UL notes give the
$75 a year no inflation, so the clock shows in no number. The declared fixed rate is an
economic input too, read at `t`, and ships flat at 1.0%. Acquisition is charged per policy
issued, in the issue month, and not inflated, as in `basiclife/BasicTerm_SE`; it ships at
zero, as in `VUL_US_S`.

**The two first-month pins**, `corridor_override_m1` and `coi_rate_override_m1`, apply at
`t == 0`, as in `VUL_US_S`, and here `t = 0` is the valuation month. Point 1, the worked
example's anchor cell, is in force there, so its `corridor_factor(0)` is the pinned 2.15
and its `coi_rate(0)` the pinned 0.04, where the rule, which takes over at `t = 1`, gives
2.03 and 0.1297335 in policy year 3; point 2, the same cell with both pins blank, takes
the rule from `t = 0`. `Data` refuses a pin on a point issued after the valuation date,
where `t = 0` falls before issue and the pin would never apply, and the generator leaves
the pins blank on every row it restates at a later month.

**The pricing path** behind the funding ratio, the notes' `AV*`, is a projection made at
issue: the account value under the level 6% pricing return, current charges and planned
premiums, with no decrements, loans or withdrawals, from zero at issue. It is keyed by the
policy month from issue, `m = duration_mth(t)`, so it is on the policy clock, and it reads
no state: a point in force reads it from issue, with no opening value. Beyond its chain of
calls, one cell a month here (*Counts and timings*, below), it parts from `VUL_US_S`'s in
two places. `funding_ratio(t)` is 1.0 outside cover before it computes `m`: before issue
`m` is negative, and the path, based at `m = 0`, would recurse without end. And the path
credits its fixed option at `pricing_fixed_return_mth()`, one rate for
every policy month, the declared rate's level, which is
`(1 + max(guar_rate_ann, crediting_rate_curr))^(1/12) − 1`, where `VUL_US_S` credits it at
`fixed_return_mth(m)`, the projection's rate read at a policy month as though it were a
month of the projection. As shipped the two are one float. Under a declared rate that
moves with `t` they part: `VUL_US_S`'s pricing path moves with it, a different rate for
each point, and this model's does not, since no declaration after issue moves a projection
made at issue. The behaviour module ships off, `dyn_behavior_on = False`, so no shipped run
reads the path at all.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`VUL_US_S` computes, whatever the point's count: `VUL_US_S` charges acquisition on the
policies in force in the issue month, which on new business are the policies issued. On
point 3, the twin of `VUL_US_S`'s one new-business point, every cash flow and every count
agrees, and so does every other cell the two models share, at every argument `VUL_US_S`'s
own sweep evaluates, but three whose meaning changed: `pols_if_init()`, now the count
already in force at the valuation date, 0 for new business; `model_point()`, a row of
another table; and `result_pols()`, which gains `pols_new_biz`. On points 1, 2 and 4,
`VUL_US_S`'s in-force points, which both models open at the valuation date, the projection
is `VUL_US_S`'s from `t = 0` on, in every report and every cell the two share but
`model_point()`, the expenses included, since inflation ships at 0.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `VUL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and ten of its columns are the in-force interface,
with the shipped lineup of two subaccounts: `basiclife/BasicTerm_SE`'s two, six that open
an in-force policy's state, one of them for each subaccount, and `VUL_US_S`'s two
first-month pins, which apply in the valuation month. Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `sa_pp_init_<i>`, one for each subaccount of `subaccount_table.csv` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | subaccount `i`'s value, the policy's own, never the premium allocation times the account value |
| `fa_pp_init` | dollars | the start of month 0 | the fixed option's value |
| `la_pp_init` | dollars | the start of month 0 | the loan account: the collateral a loan has moved out of the investment options, part of the account value |
| `loan_bal_init` | dollars | the start of month 0 | the policy debt, the interest accrued to then included |
| `sum_assured_init` | dollars of face | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date; at most `sum_assured`, the face at issue |
| `corridor_override_m1`, `coi_rate_override_m1` | a corridor factor, and a current COI rate per $1,000 a month, or blank | the valuation month, `t = 0` | the worked example's two pins, which apply at `t = 0` alone; blank where a point pins nothing, and on a point issued after the valuation date |

The six state columns are 0 on a point issued at or after the valuation date: it is issued
with no account value and no loan, at the face `sum_assured`. `sa_pp_init_<i>`,
`fa_pp_init` and `loan_bal_init` are `VUL_US_S`'s own columns: they already measure the
accounts and the debt entering `VUL_US_S`'s first month, so they keep their names. Each new
column is named for the cell it opens, on `VUL_US_S`'s stem: `la_pp_init` for the loan
account, `la_pp_at`, beside `VUL_US_S`'s `sa_pp_init` and `fa_pp_init`, and
`sum_assured_init` for `sum_assured_at`, under `UL_US_SEC`'s name for the face in force.
`UL_US_SEC`'s other three state columns would open no cell here. The product tracks no free
withdrawal allowance, since the variable-UL notes cut the face proportionately with no free
amount, and neither the premiums paid nor a MEC latch, since the notes do not enforce the
guideline premium or 7-pay limits in the baseline: so there is no `wd_used_year_init`,
`cum_prem_init` or `is_mec_init`. No quantity of the product is read at the last
anniversary, so none needs a column at a second instant.

| `VUL_US_S` | `VUL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `sa_pp_init_<i>`, `fa_pp_init`, `loan_bal_init` | the same | `VUL_US_S` already opens its in-force points from them |
| — | `la_pp_init` | `VUL_US_S` opens the loan account at the debt, `loan_bal_init` **[std]**, which holds on the loan's first day only |
| — | `sum_assured_init` | `VUL_US_S` opens every point at the face at issue, `sum_assured` |
| `corridor_override_m1`, `coi_rate_override_m1` | the same | Applied at `t == 0` in both, which here is the valuation month |

On the twins the two new columns take what `VUL_US_S` itself assumes, so each twin opens as
its S row does: on point 4 a collateral equal to its debt, 8,000.00, and on points 1, 2
and 4 the face at issue, 500,000.

The columns carried over are read as `VUL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the option, the premium, its load, the
allocation, the withdrawal and the scenario excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `VUL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the base of the $0.20 per $1,000 charge and of the surrender charge, whatever later withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL` or `SINGLE` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, paid monthly on `LEVEL`, once in the issue month on `SINGLE` |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `alloc_<i>`, `alloc_fixed` | fractions of each net premium | the allocation over the frame |
| `wd_pp` | dollars a month | the withdrawal taken in every month of cover until attained age 121; 0 on every shipped point |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `scenario_id` | a scenario ID, rows of `scenario_table.csv` | the path read from the valuation date on |
| `provenance` | text: `VUL_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, `sa_pp_init_<i>` for each subaccount
  `Data.subaccounts()` lists, and so are `age_at_entry`, `has_surr_charge`, every amount
  the projection reads as a number, `sum_assured`, `premium_pp_ann` and `wd_pp`, and every
  share it reads, `load_prem_rate`, each `alloc_<i>` and `alloc_fixed`;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more: "model_point_table_sec.csv: duration_mth must be -120 or
  more, a policy issued at most 120 months after the valuation date; it is not at point_id
  [9]". Future new business is written over a horizon, `Data.future_horizon_mth`, 120
  months as shipped, so that no frame runs longer than the projection from issue plus ten
  years: 1,584 months at issue age 0, the youngest the product issues, and 1,044 at 45,
  the only issue age the shipped COI scale carries. Set to 0, the Reference refuses future
  new business altogether, and a negative horizon is itself refused;
- `age_at_entry` is a whole number of years, 0 or more: the projection takes its `int()`
  and counts its frame and every attained age on it;
- `sum_assured` is a number above 0, the face every policy holds at issue, and each of
  `premium_pp_ann` and `wd_pp` is a number, zero or more. Each reaches the account value,
  the face or the death benefit, where `VUL_US_S` reads a blank as a missing value;
- `load_prem_rate`, each `alloc_<i>` and `alloc_fixed`, the share of each premium the load
  takes and the shares of each net premium the accounts take, is a number from 0 to 1:
  "model_point_table_sec.csv: load_prem_rate must be a number from 0 to 1; it is not at
  point_id [3]". A load past 1 would credit the accounts a net premium below 0, every
  check passing: at 1.5, point 3's accounts would take −250.00 of its 500.00 premium in
  month 0. Allocations past 1 would credit them more than the net premium;
- `has_surr_charge` is `True` or `False`, as pandas reads those words. A blank, a number or
  any other text is refused, naming only the points at fault: one text value turns the
  whole column into text, where `"False"` is a true string, so that every point would read
  as carrying a surrender charge;
- each subaccount, the fixed option, the loan account, the debt and the face in force is a
  number, zero or more. A balance is never negative in force. `VUL_US_S` lets a subaccount
  fall below zero once the point is in permanent shortfall, because it does not implement
  the grace cascade that would end such a policy, so the message for the accounts says what
  to do: restate a point in permanent shortfall no later than the last month its account
  value is still zero or more, as point 7 is;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- `sum_assured_init` is above 0 on a policy in force, which holds a face, so an extract
  that leaves the column at zero is refused, rather than projected on the corridor alone;
- `sum_assured_init` is at most `sum_assured`, since face increases are not modelled. A
  face below it is accepted, whether withdrawals cut it or an elective decrease the model
  does not implement, and it is projected from the value given;
- the loan account is above 0 exactly where the debt is: "model_point_table_sec.csv:
  la_pp_init must be above 0 where loan_bal_init is, and 0 where it is 0: the loan account
  holds a loan's collateral while the loan is outstanding; it is not at point_id [1]". A
  loan moves value out of the investment options into the loan account, and the model
  takes no new loan and no repayment, so the two are held together from the loan's first
  day, each growing at its own rate;
- each pin is blank, or a number, zero or more;
- each pin is blank on a policy issued after the valuation date: a pin applies in the
  valuation month, `t = 0`, before such a policy is issued, so it would never apply.

A point at or past the end of the projection at the valuation date,
`duration_mth ≥ 12 × (122 − age_at_entry)`, reads, but `proj_len()` refuses it, naming the
point: "point_id 4: duration_mth 924 is at or past the end of the projection, policy month
924, attained age 122". The end of the projection is the model's rule, not the table's. So
a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent, its count or its lineup from. The tables read at a policy
year or an attained age take their extents from `prem_persistency_last_year()`,
`lapse_last_year()`, `corridor_age_first()` and `corridor_age_last()`, and
`mort_age_first()` and `mort_age_last()`, beyond which each reads its nearest row, and
from `coi_rate_last_years()`, the last policy year of each issue-age cell of
`coi_rates.csv`. The key column is read by value, so a year written `5.0` is 5, and a key
that is blank, text or not a whole number is refused, naming the file, the column and the
lines it is on. So are keys that do not run one row a year or an age, without a gap or a
repeat, policy years from 1, the message naming each key that repeats, with its lines, and
each that is missing: "lapse_table.csv: the policy years must run from 1, one row a year,
without a gap or a repeat; no line holds policy_year 5". So is a blank sex or class in the
COI scale, and a rate that is blank, text or infinite. A lapse or mortality rate is a
probability, held to 0 to 1, since past 1 the monthly rate `1 − (1 − q)^(1/12)` has no
real value: "lapse_table.csv: lapse_rate_ann must be a number from 0 to 1; it is not on
line [6]". A class factor, a guaranteed COI rate, a fund expense and a premium persistency
factor are held to 0 or more, since below it each projects negative deaths, a credit or a
negative premium, every check passing. A COI rate is a charge per $1,000 of net amount at
risk, not a decrement, and the current scale passes 1 from attained age 72, as it should.
`class_count()` and `surr_charge_count()` check the class factors and the surrender-charge
schedules, for the per-point joins that read them, the same way: a class or a schedule
blank or on two rows, and a factor or a charge that is not a number, or is below 0. A
charge below 0 is none to `VUL_US_S`'s `max` through the schedule's years, and after them a
charge that rises each policy year: written at −18.00, the shipped schedule charges $1.29
per $1,000 in policy year 16, every check passing. `surr_charge_count()` also refuses a
run-off that is not a whole number of years, 1 or more: "surr_charge_table.csv:
runoff_years must be a whole number of years, 1 or more; it is not on line [2]". The
projection divides the charge by the run-off and counts policy years on it, where
`VUL_US_S` truncates a fraction with `int()` and divides by zero at 0.

Two tables are checked in cells of their own, because their keys do more than find a row.
`subaccounts()` is the subaccount lineup, checked and read by value, and the one copy of
it `Projection.subaccount_ids` and `Projection.fund_expense_ann` read. Its ids name the
model point table's columns, `sa_pp_init_<i>` and `alloc_<i>`, so an id written `1.0` must
still name `sa_pp_init_1`: here it does, and `VUL_US_S`, which names the column from the
id as pandas reads it, asks for `sa_pp_init_1.0` and raises `KeyError`. An id that is
blank, text or not whole, a lineup with no subaccount, an id on two rows and a fund
expense that is not a number, or is below 0, are refused. `scenario_last_mths()` checks
the return scenario, which `scenario_rows()` reads once, in the file's order, so that a
refusal can name lines, and gives the last month of each scenario and subaccount. A blank
`scenario_id`, a `subaccount_id` or `t` that is not whole and a return that is not a
number are refused, and so are months that do not run one row a month, from 0 or later,
without a gap or a repeat, each clause naming its scenario and subaccount:
"scenario_table.csv: the months of each scenario_id and subaccount_id must run one row a
month, from 0 or later, without a gap or a repeat; at ('WE', 1), no line holds t 2". A
path may start after month 0: one re-based to a policy issued after the valuation date
holds nothing before its issue month, and a read there raises.

Each reader asks for its extent, the count or the lineup before it reads a value, so a
projection meets the checks first. `VUL_US_S` takes each extent from the key column as
pandas reads it, where a blank key is a missing value the extent skips: the table is cut
short, and every later year reads the last good row, without a word. A blank value is a
missing value to it too, which shows in its flows or is lost in a `min` or a `max`: a
blank corridor factor reads as no corridor and a blank surrender charge as none. Here the
cap on the mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing,
as `VUL_US_S`'s own does, and each of them is refused before any rate is read.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`VUL_US_S` and its table by `tests/sec_support.py`, from the `VUL_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `VUL_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py VUL_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 2 | twin | S points 1 and 2 | in force 24 months, in policy year 3 at attained age 47, with 30,000.00 and 20,000.00 in the two subaccounts on the `WE` scenario: the worked example's anchor cell, point 1 with the worked example's two first-month pins and point 2 with both blank |
| 3 | twin | S point 3 | issued at `t = 0`: new business on Option B, `VUL_US_S`'s one new-business point |
| 4 | twin | S point 4 | `VUL_US_S`'s in-force cell with a loan, in force 120 months, on the anniversary opening policy year 11, with 40,000.00 and 25,000.00 in the subaccounts, 10,000.00 in the fixed option and an 8,000.00 loan |
| 5 | derived | S point 3 at S month 12 | on its first anniversary, inside the surrender-charge period: 3,877.96 of account value |
| 6 | derived | S point 4 at S month 6 | the in-force cell six months on, in force 126 months, mid-year: 86,248.90 of account value, its collateral 8,039.90 and its debt 8,041.89 |
| 7 | derived | S point 3 at S month 593 | Option B in the month its permanent shortfall begins, policy year 50, attained age 94, with 26.59 of account value |
| 8 | derived | S point 4 at S month 768 | the first month at attained age 119, where the mortality rate reaches 1.0: every survivor dies at `t = 0`, and `result_cf()`'s 35 later rows are zeros |
| 9 | future | S point 3, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `VUL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `VUL_US_S` carries into it, each column read as
`VUL_US_S`'s own formulas read it: each subaccount as `sa_pp_at(d, i, "BEF_PREM")`, the
fixed option as `fa_pp_at(d, "BEF_PREM")`, the collateral as `la_pp_at(d, "BEF_PREM")`, the
debt as `loan_bal_pp_at(d, "BEF_PREM")` and the face as `sum_assured_at(d − 1)`. So the row
continues the S projection from there: point 5 opens with 0.938584 policies, and point 8
with 4.006e-10. Its two pins are blank, since `VUL_US_S` applies a pin at its own `t = 0`
only, before month `d`, and so are a future row's, copied from its S point's, which are
blank. A derived row's `policy_id` is the S row's with the month appended,
`VUL-000003-M12`, and a future row's carries the months to issue, `VUL-000003-F25`. Row `t`
of a generated point is month `t + source_mth` of its S point. The derived rows restate S
points 3 and 4, which read the flat `LEVEL6`, so they need no scenario of their own. All
nine are on the anchor configuration M45 / StdNT / $500,000, because the notes disclose a
COI anchor for that cell alone [S4], so a point on any other issue age, sex or class needs
`coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `VUL_US_S` already names:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_MAT"`, the count before any maturity, `VUL_US_S`'s meaning: the `"BEF_DECR"`
  count, since the contract never matures and no event of the month separates the two.

Any other timing raises. `VUL_US_S`'s cell of the name returns `pols_if(t)` for every
timing, and nothing calls it. `"BEF_NB"` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `VUL_US_S` counts the issued policies, and this model counts them as new
business, not yet in. As in `UL_US_SEC`, `basiclife/BasicTerm_SE`'s `"BEF_MAT"`, the count
at the start of the month before its new business, is not adopted: the name keeps its S
model's meaning.

The account value keeps `VUL_US_S`'s timings, which name the points of the month in the
notes' processing order: `"BEF_PREM"`, the opening balance; `"BEF_WD"`, after the net
premium; `"BEF_FEE"`, after the withdrawal and its fee, the post-premium value the death
benefit and the net amount at risk are measured on; `"BEF_INV"`, after the monthly
deduction; and `"BEF_ME"`, after the gross return and the fund expense, before the M&E
charge. `av_at` adds `"EOM"`, the closing balance before the decrements.

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `"BEF_NB"`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's deaths and lapses in the order `pols_death` and
`pols_lapse` take them. Each account's opening balance forms the previous month's close the
same way, the same products in the same order as the closing cell `VUL_US_S` calls for:
`sa_pp_at(t, i, "BEF_PREM")` from its own value at `t − 1` and month `t − 1`'s net premium
share, withdrawal share, deduction share and unit-value growth, where `VUL_US_S`'s
subaccount ran through six cells a month; `fa_pp_at(t, "BEF_PREM")` likewise, where
`VUL_US_S`'s fixed option ran through five; and the loan account's and the debt's,
`la_pp_at` and `loan_bal_pp_at`, a month's credited or charged interest on their own value
at `t − 1`, where `VUL_US_S`'s ran through two. The subaccounts and the fixed option share
each month's withdrawal and deduction pro rata, so whichever is called first runs the
others alongside it, a month at a time. The face, `sum_assured_at`, calls itself at
`t − 1` before anything else. The account value's opening balance,
`av_pp_at(t, "BEF_PREM")`, is not a chain of its own: it is `av_pp(t − 1)`, which sums its
parts' closes.

On a model just read, a cold `net_cf` in the last month of point 1's 900-month frame runs
919 cells deep, against 5,411 for `VUL_US_S`'s point 1: 20 cells above the chain back to
`t_entry()`. Point 3's and point 4's run 21 above theirs, 944 and 824 cells. At the
longest cover the contract allows, issue age 0 and 1,464 months, it runs 1,484 deep,
whether the policy is issued at the valuation date or 120 months after it, because every
chain stops at the issue month: about 370 KiB of C stack at gcc's 255 bytes a level. Each
chain's head called alone, the loan's, the collateral's, the face's, a subaccount's and the
count's, runs at most 10 cells above its chain. Each report evaluates its columns in
ascending `t`, and on a model just read the committed points' four reports and three
checks run that way under a recursion limit of 17, and `VUL_US_S`'s under 16. That is
with the behaviour module off, as shipped.

With the behaviour module on, the funding ratio reads the pricing path at the policy month
from issue, and the path is a chain of its own, one cell a month, based at issue: each
opening balance of the path forms the previous month's close itself, where `VUL_US_S`'s ran
through four cells a month. So a cold `net_cf` on a point in force runs back to issue, not
to the valuation date: 938 cells on points 1 and 4, the 923 months of the frame's last
month from issue and 15 more. At the longest cover it runs 1,484 deep, module on or off.
The path stays based at issue. Its state is its own balances, the subaccounts' and the
fixed option's, which the pro-rata deduction couples month by month, so a form based at the
valuation date would have to carry them all through one loop in one cell.

So with the module on, the first month's funding ratio of a point in force at policy month
`d` reads the pricing path cold, back to issue, however the months after it are evaluated,
and an ascending sweep runs about `d + 15` cells deep: 39 on point 1, 135 on point 4, 903
on point 8, and 1,477 on a point in force in its last covered month at issue age 0,
against 18 on every committed point, and 14 on that one, with the module off. It needs a
modelx recursion limit of `d + 14`, 38 on point 1 and 134 on point 4. A point issued at or
after the valuation date, whose path starts in its issue month, sweeps 22 deep under a
limit of 21. The cold call's bound is unchanged, 1,484 cells at the longest cover, so the
deepest stack is the same; only the depth of a typical point in force grows with its
duration.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `VUL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < omega_mth()`, where
`omega_mth() = 12 × (omega_age − age_at_entry + 1)` is `VUL_US_S`'s frame from issue, the
first month at attained age 122. Outside it, before issue and from `t = proj_len()` on,
every count, premium, withdrawal, charge, decrement rate, decrement, claim and cash flow is
zero and every flag false; only the two clocks, the inputs read on the valuation clock, the
loan account's level credited rate, and the neutral 1.0 of the two lapse multipliers and
the funding ratio hold values there, and the month after the frame holds one exception
more, below. No count evaluates a decrement rate there, and no table is read at a policy
year or an attained age the policy does not have: `prem_persistency`,
`prem_persistency_base`, `premium_pp`, `wd_pp`, `sum_assured_at`, `corridor_factor`,
`db_pp`, `db_pp_eom`, `coi_rate_guar`, `coi_rate`, `coi_pp`, `maint_fee_pp`,
`loan_rate_ann`, `surr_charge_rate`, `mort_rate`, `lapse_rate_base`, `pols_death`,
`pols_lapse` and `expenses` are zero, and `is_default` false, before any table or rate is
read, and every other value is zero through them. `lapse_rate_sc_mult` is 1.0 there,
before it compares the policy month with the cliff, since a run-off of `n` years puts the
spike at policy month `12 n`, which can be the month after the frame; and `funding_ratio`
is 1.0 before it computes the policy month the pricing path is read at. The scenario's two
readers, `gross_return_mth` and `inv_return_mth`, take no guard, since an economic input
is one path for every point, and no formula reads them outside cover. Each table read at a
policy year or an attained age has one reader keyed by it, called inside cover only, so on
point 9, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below 1
or an attained age below 45.

**The end of the projection.** The frame ends at `omega_mth()` because the mortality table
ends at attained age 121, not at an event of the contract, which never matures. With the
shipped table, whose annual rate is 1.0 from attained age 119, and a class factor and an
A/E of 1 or more, every life has died by the end of the first month at attained age 119:
point 8, valued in that month, loses its last 4.006e-10 of a policy at `t = 0`. With a
preferred class, an A/E below 1 or a table that stays below 1, lives survive the last
month, and `VUL_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and `av_change()`
read the account value in force entering month `t + 1`, which in the last month is
`t = proj_len()`. So the two opening values read there, the count carried in
(`pols_if_at(t, "BEF_NB")`, and through it `pols_if(t)`) and the account value carried in
(`av_pp_at(t, "BEF_PREM")`), are defined for `0 ≤ duration_mth(t) ≤ omega_mth()`: in the
month after the frame they are the survivors of the last month and the account value they
carry, `VUL_US_S`'s own values there. Everything else is zero or false there, each
account's opening balance included, since a loan account carried into the month would earn
a month's credit past the frame's end, and the expenses, which would otherwise fall on the
carried count. Nothing reads past it: `av_change()` and the three checks' residual cells,
which read `t + 1`, are zero outside cover before they read it. At the shipped assumptions
the survivors at `proj_len()` are exactly 0.0 on every committed point. At an A/E of 0.56,
the rest as shipped, they are 3.88e-6 of a policy on the twin of point 1, 3.46e-6 on the
twin of point 3 and 5.44e-6 on the twin of point 4, each equal to `VUL_US_S`'s, and the
three checks close.

**A lapse rate past 1.** `VUL_US_S`'s annual lapse rate, the base rate times the cliff's
spike times the dynamic multiplier, has no cap, and this model keeps it so. `Data` holds
each base rate to 0 to 1, but the spike, `lapse_shock_mult`, and the multiplier's bound,
`lapse_dyn_cap`, are References. With both at 0 or more, the annual lapse rate is at most
`max(1, lapse_shock_mult)` × (`lapse_dyn_cap` with the behaviour module on, 1 with it off)
× the largest base rate, since the spike is 1 outside its month and the multiplier 1 with
the module off. It stays at most 1 while that product is at most 1: 0.06 as shipped, 0.12
with the module on and 0.36 under the tests' splice. Past 1 the monthly rate
`1 − (1 − q)^(1/12)` is complex, and so is every count after it, in both models: with a
spike of 40, point 3's rate is 1.2 in its cliff month, policy month 168. `VUL_US_S`'s
checks raise `TypeError` there, and so do this model's, whose residuals are `float`s, so
that a complex residual, whose magnitude would pass, cannot. Compiled, the power is NaN
instead, and the checks fail rather than raise.

## The opening state

`VUL_US_S` opens its in-force points from three kinds of column, each subaccount, the fixed
option and the debt entering its first month, and takes the rest as they stand at the start
of a loan and at issue: the loan account equal to the debt **[std]**, and the face at issue.
Its points 1, 2 and 4 need no more, and their twins open the same way. A policy valued in
any month of its life needs all six state columns, each what `VUL_US_S` carries into that
month. Point 6, `VUL_US_S`'s in-force cell six months on, shows two of them, and each is
compared below with the same row read as `VUL_US_S` would open it:

- **`la_pp_init`.** In six months the collateral has grown at the 1.0% credited to the
  loan account and the debt at the 1.05% charged in policy year 11, so point 6 holds
  8,039.90 of collateral against a debt of 8,041.89. Read as the debt, as `VUL_US_S` opens
  its loan account, the account value entering month 0 would be 86,250.89 for 86,248.90,
  1.99 high, and `net_cf` 0.00496 lower in month 0 and 0.00487 lower in month 11.
- **`sa_pp_init_<i>` and `fa_pp_init`.** The two subaccounts and the fixed option hold
  41,701.23, 26,052.83 and 10,454.95, each what its own returns have made of it: the
  subaccounts grow at the scenario's return less their fund expenses and the M&E charge,
  the fixed option at the declared rate. Spread by the allocation, 50/30/20, the unloaned
  78,209.01 would be 39,104.50, 23,462.70 and 15,641.80, the same total, and the account
  value would close month 0 16.12 lower and month 11 196.05 lower, `net_cf` 0.040 and
  0.473 higher.

No committed point withdraws, so none shows the face in force. It shows on
`VUL_US_S`'s point 3 changed to Option A and a withdrawal of $100 a month, at the shipped
assumptions. `VUL_US_S` takes the withdrawal in every month from issue and, on Option A,
cuts the face in proportion to it, as the variable-UL notes say: in the issue month $100
out of the 480.00 of account value the first net premium buys cuts the 500,000 by
104,166.67, and the withdrawals of months 0 to 12 leave a face of 174,445.82 entering
month 13:

- **`sum_assured_init`.** Restated at month 13, the point opens with that face. Month 0's
  withdrawal cuts it by 5,137.44 more, to 169,308.38, the death benefit of month 0, on
  which the cost of insurance is 19.83. Read as the face at issue, as `VUL_US_S` opens
  every point, month 0's cut would be 14,725.03 and the death benefit 485,274.97, with a
  cost of insurance of 57.58. The surrender charge is 8,357.14 either way, since it is
  quoted on the face at issue.

The two pins are not state: they are the worked example's two lookups, applied in the one
month it describes, and the generator leaves them blank on every row it restates.

## Departures from VUL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year or an attained age answers
for the months outside cover. Of `VUL_US_S`'s 148 cells in `Projection`, 60 are unchanged,
36 have a new docstring only, most of them to say what `t` now counts, and 52 are
rewritten. None is removed or renamed, and 28 cells are new, 176 in all. A cell of
`VUL_US_S`'s that this model lacked would fail the twin identity. `VUL_US_S`'s `math`
Reference is dropped. Of `Data`'s eleven, `model_point_table` is rewritten to check the
table as it reads it, `scenario_table` is formed from `scenario_rows()`, the scenario's one
read, the same frame as `VUL_US_S`'s, and five readers have their `read_csv` call wrapped;
twelve cells are new, 23 in all, and so is the Reference `future_horizon_mth`, 120. The cap
on mortality, `min(q, 1.0)`, is `VUL_US_S`'s own, and no departure.

| Cells | `VUL_US_S` | `VUL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `omega_mth` | `12 × (omega_age − x + 1) − duration_mth_init()`, the months from the first projected month | `omega_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the end of the projection | `omega_mth()` is new and is `VUL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left has no frame |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`; `"BEF_NB"` the count before the month's new business, and `"BEF_MAT"` the `"BEF_DECR"` count, as in `VUL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `sa_pp_at`, `fa_pp_at`, `la_pp_at`, `loan_bal_pp_at` | `sa_pp_init(i)`, `fa_pp_init()`, and `loan_bal_init()` for the loan account and the debt alike, at `t = 0`, then the previous month's closing cell: chains of six cells a month, five, two and two | the openings at `t_entry()`, the loan account from `la_pp_init()`, then the previous month's close formed in the cell itself, `VUL_US_S`'s arithmetic in its order; every timing zero outside cover | Every chain one cell a month, since a compiled model runs it on the C stack; the loan account and the debt part once interest accrues |
| `av_pp_init`, `av_pp_at` | `sum(SA_i(0)) + FA(0) + D(0)`, the debt standing in for the loan account, opened at `t = 0` | `sum(SA_i(0)) + FA(0) + LA(0)`, the subaccounts summed in a loop, opened at `t_entry()` and carried into `t = proj_len()` | The loan account is part of the account value, the debt is not |
| `sum_assured_at`, `face_reduction_pp` | the face at issue at `t = 0`, then the previous month's | `sum_assured_init()` at `t_entry()` on a point in force, the face at issue on any other, then the previous month's | A policy in force brings in the face its withdrawals have left |
| `funding_ratio`, `sa_pricing_pp_at`, `fa_pricing_pp_at`, `fa_pricing_pp` | the pricing path read at `duration_mth(t)` in any month; its fixed option credited at `fixed_return_mth(m)`; each opening balance the previous month's closing cell, four cells a month | 1.0 outside cover, before the policy month is computed; the fixed option credited at `pricing_fixed_return_mth()`; the previous month's close formed in the cell itself | Before issue the policy month is negative, and the path, based at issue, would recurse without end. `fixed_return_mth(m)` reads the projection's declared rate at a policy month: a rate path on the valuation clock would credit each point's pricing path with rates declared after the valuation date |
| `prem_persistency_base`, `coi_rate_guar_at`, `lapse_rate_base`, `corridor_factor_at`, `mort_rate` | the table read in the cell, clamped to the extent of the key column as pandas reads it | one reader keyed by the year or the age — `prem_persistency_py`, `coi_rate_guar_at`, `lapse_rate_base_py`, `corridor_factor_at`, `mort_rate_base_at` — with `VUL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the rates, called inside cover only | No table is read at a year or an age the policy does not have, each is read once a year or an age, and a blank, text or fractional key, keys that repeat or leave a gap, a rate that is not a number, a lapse or mortality rate outside 0 to 1 and a premium persistency factor or a COI rate below 0 are refused by name, where `VUL_US_S`'s extent skips a blank key and cuts the table short, a blank rate is a missing value, and a rate or a factor out of range projects a count, a premium or a charge no policy can have |
| `surr_charge_rate`, `lapse_shock_month` | the schedule's row read in each | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one reader for each of the schedule's two columns, each asking `data.surr_charge_count()` first; `int()` of the run-off where `VUL_US_S` takes it | The same numbers on any schedule, with no table read in a monthly cell; a blank charge, which `VUL_US_S`'s `max` reads as none, a charge below 0, which it reads as none and then as a charge rising once the schedule has run off, and a run-off that is not a whole number of years, 1 or more, are refused |
| `subaccount_ids`, `fund_expense_ann`, `gross_return_mth` | the lineup and the scenario as pandas reads them, the scenario's extent taken from its rows in each month | `data.subaccounts()`, the lineup checked and read by value; the scenario's last month from `scenario_last_mth(i)`, a join on `data.scenario_last_mths()`, which checks the table | An id written `1.0` still names `alloc_1`; a fund expense below 0, and a gap, a repeat or a blank in the scenario, are refused by name |
| `premium_pp`, `prem_pricing_pp`, `db_pp`, `db_pp_eom`, `db_pricing_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `db_option()` and `qual_test()` | branches on five decodes, `is_level_premium()`, `is_single_premium()`, `is_db_option_a()`, `is_db_option_b()` and `is_gpt()`, each reading its column from `model_point()` | No monthly cell compares text, and no projection cell calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `VUL_US_S`'s message |
| `class_factor`, `coi_rate_scale` | the class factor and the COI scale, joined on the label accessors | the same joins, on keys read from `model_point()`: the class factor once `data.class_count()` has checked its table, the COI scale, through its one reader, once `coi_rate_last_year()` has | A blank factor, a missing value to `VUL_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and is refused, as is one below 0; a blank COI rate would reach the account value |
| `corridor_factor`, `coi_rate` | the pin read from the model point in the cell, applied at `t == 0` | the pin read once a point as a value and a flag, `corridor_override_m1()` and `has_corridor_override_m1()`, `coi_rate_override_m1()` and `has_coi_rate_override_m1()`, applied at `t == 0`, the valuation month | A monthly cell tests a flag rather than a missing value, and reads no model point column in its own formula |
| `prem_persistency`, `premium_pp`, `wd_pp`, `sum_assured_at`, `corridor_factor`, `db_pp`, `db_pp_eom`, `coi_rate_guar`, `coi_rate`, `coi_pp`, `maint_fee_pp`, `loan_rate_ann`, `surr_charge_rate`, `is_default`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult` | unguarded: no `VUL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_sc_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2. At `t = proj_len()` nothing is charged, paid or withdrawn, whatever `omega_age` and `charges_cease_age` are set to |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `wd_pp` | the model point's `wd_pp` column read in the monthly cell | read once a point, by `wd_pp_mth()` | A monthly cell the accounts' chains read reads no table |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_margin`, `check_net_view` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)`, `check_margin_resid(t)` and `check_net_view_resid(t)`, each a `float`; a residual that is not a number fails, and one that is not real raises, as `VUL_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin`, `check_net_view` | the lapse term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers; the death term keeps the whole loan | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `VUL_US_S`'s identities are off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its checks fail on a projection that is right; the death claim has no floor. On every shipped point the cash value covers the loan, and the two agree |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`, the two new
opening-state accessors, `la_pp_init` and `sum_assured_init`, `coi_rate_last_year`, the
extent of a point's COI scale, and `wd_pp_mth`, the withdrawal column read once a point.
Of the cells with a new docstring only, `first_default_month` and `first_shortfall_month`
keep `VUL_US_S`'s loops and return a month counted from the valuation date: point 7,
restated in the month its shortfall begins, is in shortfall from `t = 0`.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it, and only once inflation is switched on: it ships at 0. At 2.5% a year, point 4's
`expenses(t)` is `VUL_US_S`'s divided by `1.025^10`, about 1.280, at every `t`, and point
1's by `1.025^2`: both models step on their anniversaries. Point 6's is `VUL_US_S`'s point
4's divided by `1.025^10` for `t = 0 … 5` and by `1.025^11` for `t = 6 … 11`, where its
policy year has stepped and the valuation year has not. Point 9 is `VUL_US_S`'s point 3
twenty-five months on in its other cash flows, its counts and its account value. Its
maintenance expense is `1.025^2` above `VUL_US_S`'s, and `1.025^3` in the last month of
each policy year, where the valuation year has stepped and the policy year has not.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on point 3, issued at the
  valuation date, every cell of `VUL_US_S`'s agrees at every argument `VUL_US_S` evaluates
  in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose meaning
  changed, and a cell this model lacked would fail it. The identity holds on any count,
  since `VUL_US_S` already charges acquisition on the policies issued. The same suite
  holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The in-force twins**, in `tests/test_variable_ul_us_sec.py`: points 1, 2 and 4 open
  with `VUL_US_S`'s own opening balances, the collateral at the debt and the face at
  issue, and each is `VUL_US_S`'s projection from `t = 0`, in every report and every cell
  the two share, to 1e-9 relative with no absolute floor. So the goldens
  `tests/test_variable_ul_us.py` asserts on point 1 — every row and column of the worked
  example's month, from the opening balances to the end-of-month death benefit and net
  amount at risk, to the cent — hold here at `t = 0`, the valuation month, with no number
  restated.
- **The splice**: each `VUL_US_S` point restated in force at a month either side of its
  events continues the S projection from there, in its four reports, column by column, and
  in every other cell the two share, the subaccounts, the fixed option, the loan account,
  the debt and the face at every timing among them, and the pricing path at `VUL_US_S`'s
  own policy months, to 1e-9 relative with no absolute floor. It leaves out those the twin
  identity skips, `VUL_US_S`'s own opening values and frame, and the scenario's id, since
  each row reads a copy of its own; the first default and shortfall months are asserted
  instead as the first `VUL_US_S` finds at or after the row's month, less that month. The
  months straddle the product's events: the first anniversaries, the loan's preferred
  rate, the lapse table's last year, the surrender charge's cliff and its one-month lapse
  spike, the month a shortfall begins, the attained age at which the splice's charges
  cease, the corridor's first binding and the last covered month, whose `t = 1` is the
  month the survivors are carried into. So are nine variants of S's points, in a copy of
  S's table that is never committed, each changing S's columns only and each with input
  rows of its own, for branches S's own points do not reach: withdrawals on either option,
  a single premium with no surrender charge, an Option B point funded past its face, a
  point on a second surrender-charge schedule with a loan, an issue age below the
  mortality and corridor tables' first age, each first-month pin alone, so that neither's
  flag stands in for the other's, the COI pin set above the guaranteed rate that bounds
  it, and a withdrawal larger than the account value its first premium buys, whose cut
  takes the face past 0, where it is floored. Between them they carry both sexes and every
  class, and one COI scale stops short of its cover, so that its later years are read at
  its last. `VUL_US_S`'s in-force points 1, 2 and 4, and the variants in force 24 and 60
  months, are splice cases too, at their own month 0. The References are set in both
  models to reach what the shipped values leave unreached: the behaviour module on, so
  that the pricing path, the funding ratio and the premium persistency scale are compared;
  the lapse spike at 3 times; an acquisition expense of $250; the mortality A/E at 0.56,
  which leaves survivors at the end of every frame; charges ceasing at attained age 100,
  inside every frame; and the declared rate at 2.5%, apart from the guaranteed 1.0%. The
  return scenario is a path that moves every month, and each restated or future row reads
  its own copy, re-based to its month.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column and every kind of valuation month, and a test asserts that they do. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs the
  full grid too. The tests that read the splice are one class, first in the module, whose
  models are closed before the committed model and `VUL_US_S` are first read, so the
  module never holds both, and each splice row is released once it has been compared.
- **Future new business**: issued later than the valuation date, S point 3 and each
  new-business variant is the S projection moved on, cell by cell, the count at each of
  its timings among them but the count before new business in the issue month, which
  `VUL_US_S`'s cell counts as in force; with zeros before issue in every report, no
  decrement rate evaluated there, and no scenario month read before issue.
- **How it computes**: each row the splice and the future business compare is first run on
  the books, its reports, its checks and then every monthly cell at every month from
  `t_entry()` to `proj_len() − 1`, at every subaccount, timing and kind, as Phase 2's
  sweep will run it, and is then scanned, before the comparison evaluates its cells at
  `VUL_US_S`'s keys: no cell has been called at a negative month, none evaluated from
  `t_entry()` on has read a month before it, none evaluated at month `t` has read a month
  later than `t + 1`, and no cell without a month but the loops over the frame has read
  one keyed by a month. The sweep is what reaches the account value's opening balance in a
  later point's issue month, which no report reads, since the funding ratio returns there
  first. The pricing path, a projection made at issue and based there, is the one
  look-back allowed, and is held to the rest at its own policy months. On a fresh read of
  the committed model the policy clock is a closed form, every point's reports run under a
  lowered recursion limit, which a recursion backward over the frame would exceed, and no
  projection cell has read a label accessor. And every chain is called cold, on a fresh
  read, at the shipped References, with the behaviour module on and at the longest cover:
  modelx's stack trace counts no more than one cell a month back to `t_entry()`, or back
  to issue through the pricing path, and a fixed overhead, which a chain of two cells a
  month would exceed. With the module on, the twins of points 1 and 4 sweep in ascending
  `t` under a recursion limit of their policy month at the valuation date and that
  overhead, and the twin of point 3 and the row issued 25 months on under the module
  off's.
- **Counts, validation and regeneration**: the roll-forward closes, the last month
  included, `"BEF_MAT"` is the `"BEF_DECR"` count, and `pols_if_at` refuses a timing it
  does not have; `result_pols()` is `VUL_US_S`'s, column for column, with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, with every assumption that ships at zero
  switched on, multiplies every cash flow and moves no per-policy value; each malformed
  row is refused naming its point, by its own rule, and so is a projection of it; each
  assumption table with a malformed key, a policy year below 1 among them, or a value that
  is not a number, is refused naming its file, its column and its lines, and so is one
  with a lapse or mortality rate outside 0 to 1, or a class factor, a COI rate, a fund
  expense, a premium persistency factor or a surrender charge below 0, while the bounds of
  each range are read; a `db_option`, `qual_test` or `premium_type` no decode knows raises
  `VUL_US_S`'s message; the horizon is a Reference, which at 0 refuses any future business,
  saying so; a point at or past the end of the projection is refused by `proj_len()`; the
  edges of the interface are accepted, the keys of every keyed table written as floats
  among them; the committed table is what `VUL_US_S` generates, and each of its derived and
  future rows projects its S point's reports from its month on; and the generator reads
  one opening column for each subaccount of the lineup, and every S point it issues later
  has both pins blank.
- **The opening state and the rest**: point 6 opens from its own collateral and its own
  subaccounts, and read as `VUL_US_S` would open it gives the numbers above; the face in
  force opens from its column; a row restated on `WE` as shipped reads the worked
  example's month at `t = 0`, and on a copy re-based to its month is `VUL_US_S`'s; expense
  inflation runs on the valuation clock, the fund returns and the declared rate are one
  number for every point in each month, each subaccount's path repeating its own last
  month, the two ending apart, and a declared rate that moves leaves the pricing path
  where it was; with a current COI scale above the guaranteed one and a declared rate
  below the guaranteed 1.0%, point 4 is `VUL_US_S`'s in every cell, every current rate the
  guaranteed one and the fixed option and the pricing path credited at the floor; a check
  whose residual is not a number fails, the NaN sent through the M&E rate, a Reference; a
  lapse rate past 1 makes every check raise, in both models; each check decides as
  `VUL_US_S`'s `math.isclose` does where its sides fall below 1, a miss inside the
  absolute tolerance passing and one outside it failing; on a point whose loan comes to
  exceed its cash value the three checks hold where `VUL_US_S`'s margin and net-view
  identities fail; acquisition falls on new business alone, per policy issued and not
  inflated; a StdTob point at an A/E of 1.0, whose product first passes 1 at attained age
  113, 1.09495, is `VUL_US_S`'s in every cell, the capped months included, as new business
  and restated in force the month before the cap, the rate there is the float 1.0 in both
  models, every life in force dies in that month and nothing is in force after it; a NaN
  that reaches the cap stays NaN, sent through the class factor's formula or the A/E, a
  Reference, and so does one that reaches a bound on the COI rate written second, the
  scale's cap, the guaranteed rate over the current one and the pin's; every monthly cell
  holds its value outside cover and reads no table there; the points of a block sum row by
  row; an extract without the generator's three columns, relabelled, projects the same
  numbers; and `run_sec.py` prints the model's numbers.

```bash
python -m pytest tests/test_variable_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_variable_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k VUL_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
