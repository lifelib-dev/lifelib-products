# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `MYGA_US_SEC` is [`MYGA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of their contract year, and contracts to be written in the
ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
The product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in `BasicTerm_SE`,
and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `MYGA_US_S` on another time axis, and it reads `MYGA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced, the 4.45% declared
> rate, the 0.25% GMIR and the 2.80% GMSV rate from a rate sheet [S11] and the 9/8/7/6/5
> surrender charge and the 10% free withdrawal from a brochure [S10] among them. Every
> behavioural and expense assumption is a **[std]** standardization, the rate scenarios
> included, and the shipped mortality table is illustrative, *not* a published basis.
> Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/fixed_deferred_annuity/run_sec.py          # point 1, issued at t = 0
python products/fixed_deferred_annuity/run_sec.py 8        # the anchor, a year on
python products/fixed_deferred_annuity/run_sec.py --block  # every point, row by row
```

The first prints, as rows `t = 0 … 11`, the twelve months `run.py` prints for
`MYGA_US_S`'s point 1, the worked example's first contract year, number for number. The
second prints point 8, the same contract valued on its first anniversary. Its row `t = 0`
is the worked example's month 12: the $4,000 free withdrawal taken from 104,450.00,
100,450.00 credited to 100,815.11, and the Model #805 floor at 86,148.02. Every column
agrees with `MYGA_US_S`'s months 12 to 23 but `expenses`, which are in valuation-date
dollars here, 4.09 in the first month where `MYGA_US_S` has 4.19, and `net_cf` with them.
Three lines to the same thing for point 8:

```python
import modelx as mx
model = mx.read_model("products/fixed_deferred_annuity/MYGA_US_SEC")
model.Projection[8].result_cf()
```

`Projection` takes a `point_id`, as in `MYGA_US_S`. `result_cf()` has `MYGA_US_S`'s
eleven columns — `pols_if`, `premiums`, `withdrawals`, `claims_death`, `claims_lapse`,
`claims_annuitization`, `claims_maturity`, `commissions`, `expenses`, `premium_taxes` and
`net_cf` — with one row per month from the valuation date, `t = 0 … proj_len() − 1`.
`result_av()` has `MYGA_US_S`'s values per contract on the same rows, the worked
example's five columns and the surrender trace, with zeros before issue. `result_pols()`
sets out the counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's
annuitizations, deaths and surrenders in processing order and the deemed maturities of the
last covered month, then `pols_if_aft_decr`, the notes' end-of-month `l(t)`, as in
`MYGA_US_S`.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`), so the
run holds the cells of one point at a time.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the contract, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the deemed maturity at attained age 100.
- **`duration_mth(t)`, the policy clock**, counts the months the contract has been in
  force at time `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is the technical notes' month
  index, and the contract runs on it: `duration(t) = duration_mth(t) // 12`, the contract
  year `policy_year(t) = duration(t) + 1` and `age(t) = age_at_entry() + duration(t)`, as
  in `MYGA_US_S`, and the guarantee period containing month `t`,
  `gp_index(t) = duration_mth(t) // (12 n) + 1`. `BasicTerm_SE` reaches the same numbers
  by adding one a month, a recursion as long as the frame; the closed form needs no such
  chain of calls.

Point 8 is the anchor cell in force 12 months. At `t = 0` it is on its first anniversary,
opening contract year 2, at attained age 61, and the $4,000 withdrawal the contract takes
in policy month 12 falls there. Its shock-lapse year, contract year 6, opens at `t = 48`,
and its frame has 468 rows, `t = 0 … 467`. Point 12 is the stress trace in force 61
months, in contract year 6, the month after its first window: its renewal rate and its
MVA reference yield `i0`, fixed at policy month 60, the month before the valuation date,
come from its row, and its next window falls at `t = 59`. Point 14 is the anchor cell to
be issued 15 months after the valuation date: `duration_mth(0) = −15`, it is on the books
from `t_entry() = 15`, rows 0 to 14 are zeros, its $4,000 falls at `t = 27`, and its
frame has 495 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the initial term and each renewal period of `n` years, and the index, start and end of the guarantee period in force; the 30-day window in the first month of each renewal period, and the annuitization elected in it; the redeclaration months; the surrender charge schedules, their clock and the attained-age cap; the MVA term; the free-withdrawal years, the base each fixes and the reset at each anniversary; the scheduled withdrawals, whose `t` in `withdrawal_table.csv` is a policy month, and the free-withdrawal utilization in the first month of each contract year; the base lapse by contract year and the dynamic-lapse exponent; mortality at the attained age; the deemed maturity at attained age 100 | the rate scenario, the market rate `market_rate(t)` and the MVA reference yield `mva_ref_yield(t)`, whose `t` in `rate_scenario.csv` is a valuation month; expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

The rate scenario is a path in calendar time, shared by every contract of a block, so it
moves to `t`. A rate fixed in the past is a fact of the contract instead. The declared
rate of a renewal period is fixed at its redeclaration, the first month of each renewal
period under `rollover` and each anniversary after the initial term under
`annual_redeclare`, and `i0` at the start of each renewal period, which matters under
`rollover`, the one architecture with an MVA after the initial term. A rate fixed at or
after the valuation date is read from the scenario at the valuation month it is fixed in,
and one fixed before it from the opening state (below). Point 11, valued in its 30-day
window at policy month 60, takes its renewal rate, `max(GMIR, MR(0) − s_ren)` = 4.45%,
and its `i0`, 10.00%, from the stress scenario at `t = 0`; point 12, a month later, takes
both from its row. `redeclare_month(t)` and `gp_start_month(t)` still return policy
months, and `credit_rate` and `mva_ref_yield_locked`, the two cells that read them, turn
each into a valuation month once. Each shipped scenario is one row at `t = 0`, a flat
path, so no shipped number depends on the clock it is read on.

Expense inflation keeps `MYGA_US_S`'s annual step, `1.025^duration(t)`, but takes it every
twelve months from the valuation date rather than on the contract's anniversaries, so the
maintenance charge, $50 a contract a year, is in valuation-date dollars for every point
alike. Acquisition, `expense_acq` per contract issued and 0 as shipped, is charged in the
issue month and not inflated, as in `basiclife/BasicTerm_SE`, and so are the 2.00%
commission and the premium tax, on the premium of the contracts issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`MYGA_US_S` computes, whatever the point's count: `MYGA_US_S` already takes the premium
and charges the commission and acquisition on the contracts in force at its `t = 0`,
which on new business are the contracts issued. On `MYGA_US_S`'s seven points every cash
flow, every count and every value per contract agrees, and so does every other cell the
two models share but five whose meaning changed: `pols_if_init()`, now the count already
in force at the valuation date, 0 for new business; `model_point()`, a row of another
table; `av_pp_init()` and `mgsv_pp_init()`, now the account value and the floor in force
entering month 0, 0 for new business, whose issue values are credited in the issue month
instead; and `result_pols()`, which gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `MYGA_US_S`'s columns,
and twelve of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and
ten that open an in-force contract's state. Each of the twelve is a number, and every
amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the contract's age in months: positive in force, in any month of its contract year, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, more than 0 in force | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value |
| `mgsv_pp_init` | dollars, possibly negative | the start of month 0 | the Model #805 floor [R1]: 87.5% of the premium, less each withdrawal as the contract's convention counts it and the monthly contract charge, accumulated at the GMSV rate |
| `prem_accum_gmir_pp_init` | dollars, possibly negative | the start of month 0 | `P_accum@GMIR`, the premium less prior withdrawals accumulated at the GMIR, which the `gmir_floor` MVA cap holds `AV + M` above [S13] |
| `interest_credited_pp_init` | dollars | the start of month 0 | the interest credited from issue, which the `min_sc_interest` MVA cap reads [S8] [S9] |
| `interest_credited_pp_prev_anniv_init` | dollars | the anniversary that opened the contract year under way, on or before the valuation date: the close of policy month `12 × duration(0) − 1` | the interest credited from issue to that anniversary, from which the interest-only allowance of the next contract year is measured [S5] [S6] |
| `free_wd_allow_init` | dollars | that anniversary | the free-withdrawal allowance of the contract year under way: `free_wd_rate`, 10% as shipped, of the account value at the anniversary under `pct_av` [S10]; the interest credited over the contract year before under `interest_only` |
| `free_wd_remain_init` | dollars | the start of month 0 | the part of that allowance the year's withdrawals have not used |
| `tax_basis_pp_init` | dollars | for a point in force, the start of month 0; for any other, issue | the IRC §72 investment in the contract [R6] |
| `credit_rate_init` | a rate a year, effective | the start of month 0: the rate credited in policy month `duration_mth − 1` | the declared rate in force |
| `mva_ref_yield_locked_init` | a rate a year | the start of month 0 | the MVA reference yield `i0` locked for the guarantee period in force |

On a point issued at or after the valuation date every one of the ten is 0 but
`tax_basis_pp_init`: such a contract opens with nothing, and its issue values arrive in
its issue month. `tax_basis_pp_init` is then the basis at issue, as `MYGA_US_S`'s
`tax_basis_initial` is, which varies with tax status: the premium on every shipped point,
all of them non-qualified, and 0 for a qualified contract. In the first contract year,
`duration_mth` 1 to 11, the year opened at issue, so `interest_credited_pp_prev_anniv_init`
is 0 and `free_wd_allow_init` is the issue allowance, `free_wd_rate` times the premium
under `pct_av` and 0 under `interest_only`. On a point valued on an anniversary,
`duration_mth` a positive multiple of 12, the anniversary that opened the year is the
valuation date itself: the interest to it is `interest_credited_pp_init`, and under
`pct_av` the year's allowance is `free_wd_rate` times `av_pp_init`. The remainder carried
into such a month is last year's, which lapses at the anniversary unread, the allowance
being non-cumulative [S4] [S16]. Entering any month of the initial term, `duration_mth` 1
to 12 `n`, the first renewal month included, the declared rate and `i0` are still the
issue values, `declared_rate_initial` and `mva_ref_yield_at_issue`. `prev_anniv` is the
anniversary that **opened** the contract year: an extract that fills the two anniversary
columns from the anniversary after the valuation date is a year out.

Each column is read where the contract needs it, and only there:

- `free_wd_allow_init` on a valuation on an anniversary, where month 0 opens the year and
  the allowance resets to it, as on points 8 and 11. Off an anniversary the remainder
  carries the year, and only `Data`'s check that the remainder does not exceed the year's
  allowance reads this column. Each later year's allowance is fixed in the frame.
- `free_wd_remain_init` off an anniversary, the remainder `free_wd_avail(0)` opens from.
- `interest_credited_pp_prev_anniv_init` under `interest_only` alone, by the allowance of
  the year after the one under way.
- `interest_credited_pp_init` under the `min_sc_interest` cap and the `interest_only`
  allowance, and `prem_accum_gmir_pp_init` under the `gmir_floor` cap.
- `credit_rate_init` wherever the declaration in force was made before the valuation date,
  and `mva_ref_yield_locked_init` wherever a linear-duration or geometric MVA applies in a
  renewal period that started before it. The declared-differential MVA reads no `i0`, and
  under `annual_redeclare` no MVA applies after the initial term, so there the column is
  carried unread.
- `tax_basis_pp_init` by `tax_basis_pp` and `taxable_wd_pp`, which are reported and drive
  no cash flow.

Everything else the projection uses is fixed at issue, in `MYGA_US_S`'s columns, or follows
from the policy clock. The guarantee-period position, the surrender-charge clock, the
window, the base lapse and the attained age all derive from `duration_mth` alone, because
every renewal period is `n` years, as in `MYGA_US_S`.

| `MYGA_US_S` | `MYGA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months. Every `MYGA_US_S` point is new business, opening its frame at issue |
| `tax_basis_initial` | `tax_basis_pp_init` | Renamed in place, after the cell that reads it, so that the ten state columns share one vocabulary; on new business it keeps its meaning, the basis at issue |
| `av_pp_init()` computes `P (1 − load)` | `av_pp_init` | The notes' `av_initial`: the issue value is still computed by its rule, now in the issue month (`prem_to_av_pp`), and the cell reads the account value in force |
| `mgsv_pp_init()` computes `0.875 P` | `mgsv_pp_init` | The notes' `mgsv_initial`, the same way (`prem_to_mgsv_pp`) |
| — | `prem_accum_gmir_pp_init` | `MYGA_US_S` opens `P_accum` with the premium at `t = 0` |
| — | `interest_credited_pp_init` | `MYGA_US_S` opens the interest credited at 0 |
| — | `interest_credited_pp_prev_anniv_init` | `MYGA_US_S` reads the interest at each anniversary from its frame, which starts at issue |
| — | `free_wd_allow_init` | `MYGA_US_S` fixes every year's allowance in its frame |
| — | `free_wd_remain_init` | `MYGA_US_S` resets the allowance at `t = 0`, its issue anniversary |
| — | `credit_rate_init` | `MYGA_US_S` reads every declared rate from the scenario, at its redeclaration month |
| — | `mva_ref_yield_locked_init` | `MYGA_US_S` reads every `i0` from the scenario, at the start of its period |

A column measured entering month 0 is the cell it opens with `_init` added, and so is
`free_wd_allow_init`, the value `free_wd_allow` returns for the contract year under way; a
balance measured at the anniversary adds `_prev_anniv_init`. `free_wd_remain_init` takes
no `_ytd`: it is not an accumulator restarting each year but the remainder of an annual
allowance, which each anniversary resets.

On the twins the nine columns other than `tax_basis_pp_init` are 0, the state of a
contract entering its issue month, and `tax_basis_pp_init` is the S row's
`tax_basis_initial`, so each twin takes its issue values in month 0, as its S row does.

The columns carried over are read as `MYGA_US_S` reads them. For a contract in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `tax_status` | codes, as in `MYGA_US_S`'s table | issue |
| `premium` | dollars, the single purchase payment | issue |
| `guar_period` | years, the initial term and each renewal period | issue |
| `declared_rate_initial`, `gmir`, `mgsv_rate` | rates a year, effective | issue: the initial term's rate, the guaranteed minimum and the GMSV accumulation rate |
| `mgsv_annual_charge` | dollars a year | issue |
| `mgsv_wd_convention`, `renewal_architecture`, `free_wd_rule`, `mva_family`, `mva_cap_rule` | codes, as in `MYGA_US_S`'s table | issue: the contract's provisions |
| `free_wd_mva_exempt` | a flag, `True` or `False` | issue |
| `free_wd_rate` | a fraction of the free-withdrawal base | issue |
| `mva_ref_yield_at_issue` | a rate a year | issue: `i0` for the initial term |
| `premium_tax_rate` | a fraction of the premium | issue |
| `scenario_id`, `wd_schedule_id` | keys into `rate_scenario.csv` and `withdrawal_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `MYGA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the twelve in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `age_at_entry` and `guar_period` are whole numbers of years: `MYGA_US_S` reads both by
  `int()`, which would truncate a fraction without a word, and the initial-term check
  below reads `guar_period` as written;
- `guar_period` is 1 year or more: at 0 the guarantee-period index divides by zero,
  naming no point, and below it the projection runs a period no contract has;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,320 months at issue age 0, the youngest the product
  issues, and 840 at 40, the youngest the shipped mortality table carries. Set to 0, the
  Reference refuses future new business altogether, and a negative horizon is itself
  refused;
- the account value, the two interest columns, the allowance, the remainder and the basis
  are each a finite number, zero or more;
- the floor, `P_accum`, the declared rate and `i0` are each a finite number;
- a contract not yet in force, `duration_mth` 0 or less, has an opening state of zeros,
  `tax_basis_pp_init` apart;
- a contract in force has an account value above 0: one fully withdrawn is no longer in
  force, and the dynamic lapse, which reads the surrender benefit as a share of the
  account value, has nothing to divide by;
- in the first contract year the interest at the anniversary is 0;
- in the first contract year the allowance is the issue allowance;
- on a point valued on an anniversary the interest at the anniversary equals the interest
  entering month 0;
- the interest at the anniversary does not exceed the interest entering month 0;
- under `interest_only`, from the second contract year on, the year's allowance, the
  interest credited over the year before, does not exceed the interest credited to the
  anniversary that opened the year, and in the second year it is that interest, the first
  year's;
- off an anniversary the remainder does not exceed the year's allowance;
- entering a month of the initial term, the first renewal month included, the declared rate
  and `i0` are `declared_rate_initial` and `mva_ref_yield_at_issue`;
- after it, the declared rate is the GMIR or more;
- on a point valued on an anniversary under `pct_av`, the year's allowance is
  `free_wd_rate × av_pp_init`;
- last, each point's keys into the tables it is joined with: its `scenario_id` is a
  scenario of `rate_scenario.csv` that sets its levels by the first month the point is on
  the books, `t = 0` or its issue month if later; its `wd_schedule_id` is a programme of
  `withdrawal_table.csv`; and `mort_table.csv` gives a rate at its `sex` and its attained
  age in that first month. So reading the model point table reads those three tables,
  checked. `MYGA_US_S` meets a key its table lacks only as it projects: a missing
  scenario, sex or age raises Python's own error, naming no file, and a missing
  withdrawal programme takes no withdrawal, without a word.

Amounts of money are compared to a cent, so an extract may carry each column to the cent,
as an administration system holds it. Each amount so carried is within half a cent of its
exact value, so a rule that holds between the exact amounts can miss by half a cent from
each: from the allowance, and from the account value or the premium it is a share of,
scaled by `free_wd_rate`, 0.0055 in all at the product's 10%. A cent holds every such pair
with room for the floating-point error of the comparison, where half a cent left the ties
to that error: point 11's allowance and account value, 12,432.034927 and 124,320.349270,
carried as 12,432.03 and 124,320.35, are 0.005 apart, and so is an issue allowance carried
as 864.18 or 864.19 at 7% of a premium of 12,345.50, which is 864.185. So are read an
allowance of 10,445.00 on an account value of 104,449.99, whose 10% is 10,444.999 in
floating point, and an issue allowance of 7,000.00 at a `free_wd_rate` of 7% of 100,000,
which in floating point is 7,000.000000000001. A stale allowance, last year's or a dollar
out, is still refused. The projection then starts from the allowance as carried. The
generated rows carry `MYGA_US_S`'s own values, unrounded.

Accepted, because a contract can be in each state: a negative floor or `P_accum`, since
every withdrawal is deducted from both and nothing floors either, in either model; any
basis at issue, zero or more, on a contract not yet in force, 0 for a qualified one; on a
point valued on an anniversary, a remainder above the year's allowance, last year's; and
a `duration_mth`, an `age_at_entry` or a `guar_period` written as a float, read as the
whole number it holds.

Left to the projection: an attained age past the mortality table's last before the deemed
maturity raises a `KeyError` there, as in `MYGA_US_S`, because the maturity age is a
`Projection` Reference, which `Data` cannot read. The shipped table runs to 120, past every
contract's cover.

The six assumption tables are `MYGA_US_S`'s, read in place by `MYGA_US_S`'s readers, and
their keys are checked as well. Beside each reader a `Data` cell reads the table's keys by
value, once, checks them and the table's values, and returns the table indexed by the
checked keys, and the projection reads the table there and nowhere else: `mort_rates`,
`surr_charge_scales`, `surr_charge_age_caps`, `rate_scenario_steps`, `wd_schedules` and
`mva_factors`. The age cap's first and last ages and the duration factors' last year,
which bound the reads, are taken from the same checked keys. A key written `1.0` is 1, as
`MYGA_US_S`'s lookups match it. A key that is not a whole number, text and a blank among
them, a blank text key, a rate or an amount that is not a number in its range, a repeated
key, and keys that leave a gap where the projection reads every year or age between a
table's first and last are refused, naming the file, the column and the lines, before a
projection reads a value from the table, and so is a surrender charge table without the
`initial` and the `renewal` schedules, the two `surr_charge_id` names, where `MYGA_US_S`
reads a schedule it cannot find as no charge, so that one spelt `Renewal` would leave
every renewal period free of charge. A scenario may start after `t = 0`, for business
issued later, so the month it must start by is the point's, which the model point table's
last checks hold. `MYGA_US_S` takes the keys as pandas reads them: one written as text
turns its column to text, every lookup on it misses, and a surrender charge or a
withdrawal is then zero without a word, the age cap vanishes, or a lookup raises an error
that names no file.

A point whose cover had ended by the valuation date,
`duration_mth ≥ 12 × (100 − age_at_entry)`, reads, but `proj_len()` refuses it, naming
the point: the end of cover is the product's rule, not the table's. So a loop over the
block meets such a row only when it reaches it, after projecting the points before it.
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`MYGA_US_S` and its table by `tests/sec_support.py`, from the `MYGA_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `MYGA_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py MYGA_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–7 | twin | S points 1–7 | issued at `t = 0`: `MYGA_US_S`'s seven contracts — the worked example's anchor cell, the stress trace, Camp B with the GMIR-floored MVA, the registered-contract conventions, the interest-only, net-of-charges point under the interest-credited cap with its $20,000 excess withdrawal at policy month 29, the asymmetric cap and the declared-differential MVA |
| 8 | derived | S point 1 at S month 12 | the anchor on its first anniversary, with year 2's allowance of 10,445.00, under which its $4,000 at `t = 0` is free |
| 9 | derived | S point 5 at S month 30 | the month after its excess withdrawal, which used up contract year 3's interest-only allowance of 4,648.02: an account value of 91,426.34, the floor net of charges at 75,862.37, 11,426.34 of interest to date and 9,098.02 to the anniversary, and a basis of 91,095.23 |
| 10 | derived | S point 3 at S month 30 | Camp B halfway through contract year 3 of its initial term, with a `P_accum` of 100,626.17, which its GMIR-floored MVA reads |
| 11 | derived | S point 4 at S month 60 | the registered-contract point in its 30-day window at `t = 0`: no surrender charge, no MVA, the annuitization election, and the rate redeclared and `i0` re-locked from the scenario at `t = 0` |
| 12 | derived | S point 2 at S month 61 | the stress trace in the month after its window, in its shock-lapse year, with the renewal rate of 4.45% and the `i0` of 10.00% fixed at policy month 60 |
| 13 | derived | S point 3 at S month 479 | Camp B in its last covered month, a one-row frame ending at the deemed maturity, with the rate declared at policy month 468 |
| 14 | future | S point 1, 15 months on | to be issued at `t = 15` |

A derived row's `policy_count` is the count `MYGA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `MYGA_US_S` carries into it, each column read
as `MYGA_US_S`'s own formulas read it: the account value, the floor, `P_accum`, the
interest credited, the remainder and the basis at the close of S month `d − 1`; the
declared rate and `i0` S credits and holds in that month; the interest at the close of S
month `12 × duration(d) − 1`, the anniversary that opened the contract year of `d`; and
S's allowance of that year, its `free_wd_allow(policy_year(d))`. So the row continues the
S projection from there: point 8 opens with 0.982074 contracts, points 9 and 10 with
0.954660, point 11 with 0.907698, point 12, a month into its 90% shock-lapse year, with
0.741165, and point 13 with 0.001064. Its `policy_id` is the S row's with the month
appended, `MYGA-000001-M12`, and a future row's carries the months to issue,
`MYGA-000001-F15`. Row `t` of a generated point is month `t + source_mth` of its S point.
All fourteen are the anchor cell's male 60, non-qualified, $100,000 contract with a
five-year guarantee period, as every `MYGA_US_S` point is; the shipped mortality table
starts at attained age 40, so a point issued younger needs it extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, the
  notes' `l(t−1)`;
- `"BEF_MORT"`, after the month's annuitization elections;
- `"BEF_LAPSE"`, after its deaths;
- `"AFT_DECR"`, after its surrenders, the notes' end-of-month `l(t)`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `MYGA_US_S`'s, unchanged
but for their guard outside cover. `"BEF_DECR"` already meant in `MYGA_US_S` what it means
in `BasicTerm_SE`, and `"BEF_MORT"` is "before mortality", not `BasicTerm_SE`'s
`"BEF_MAT"`, so no name clashes, and `"BEF_NB"` is the one timing running in force adds.
Any other timing raises.
`BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a month before its maturities, is
not adopted: the contracts here mature at the end of the last covered month, as
`pols_maturity`, where `MYGA_US_S`'s goldens put the deemed maturity.

The survivors carried into month `t` are those of month `t − 1`'s `"BEF_DECR"` count,
which `"BEF_NB"` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's annuitizations, deaths and surrenders in the order `"AFT_DECR"` takes
them. So `pols_if_at(t, "AFT_DECR")` is `pols_if_at(t + 1, "BEF_NB")` in every month but
the last covered one, where the deemed maturity empties the block, and it is
`pols_if(t + 1)` except where month `t + 1` is an issue month, whose new business joins
`pols_if`. The chain of calls from month `t` back to `t_entry()` is one cell a month,
where `MYGA_US_S`'s count ran through two, and so are the account value's, which ran
through three, and the free-withdrawal carry's, which ran through two. A cold `net_cf` in
the last month of a 480-month frame runs 494 cells deep, or 496 on a model just read,
whose deepest frames are `Data`'s first read of the age-cap table, against 1,437 in
`MYGA_US_S`, so modelx needs a recursion limit of 495 for it. At issue age 0, the
contract's longest cover from issue, 1,200 months, on a copy whose mortality is extended
below the table's age 40, it runs 1,214 deep, and a point issued later runs no deeper,
because its chain stops at its issue month. Each report evaluates its columns in
ascending `t`, and a sweep of the committed points that way runs under a recursion limit
of 16.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `MYGA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_annuitization(t) + pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `MYGA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing account value, `av_at(t, "EOM")`, is weighted
by `pols_if_at(t + 1, "BEF_NB")`. Both roll-forward checks scale their tolerance with
`policy_count`, since a residual is rounding on that many contracts.

The premium, the commission, the premium tax and acquisition fall on `pols_new_biz(t)`,
in the issue month: `t = 0` on the twins, `t = 15` on point 14, and never on a point
already in force, which paid its premium before the valuation date. `MYGA_US_S` puts them
at `t = 0` on `pols_if_init()`, the contracts issued, so on a twin they are the same at
any count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (100 − age_at_entry)` is `MYGA_US_S`'s frame from issue. Outside
it, before issue and from the deemed maturity on, every count is zero, and so every cash
flow and every value per contract. No count evaluates a decrement rate there, and no table
is read at a contract year or an attained age the contract does not have:
`in_gp_window` and `mva_in_force` are false, and the declared rate, `i0`, mortality, the
surrender charge and its age cap, the MVA term and duration factor, the base and dynamic
lapse terms, the floor's charge and the scheduled withdrawals are zero before any table or
rate is read. The dynamic-lapse ratio of the surrender benefit to the account value would
be 0/0 there, and the lapse rate's clamp would give its 0.5% floor.

## The opening state

`MYGA_US_S` projects new business only, so its frame always opens at issue, from the
premium and the two rules the notes state for the account value and the floor. A contract
valued in any month of its life needs all ten state columns, each what `MYGA_US_S` carries
into that month, and each shows on a derived row:

- **`free_wd_allow_init`.** Point 8, the anchor valued on its first anniversary, carries
  year 2's allowance, 10% of its account value there, 104,450.00: 10,445.00. Month 0
  resets the allowance to it, so the $4,000 withdrawal at `t = 0` is free of surrender
  charge and MVA and leaves 6,445.00 for the year, as in `MYGA_US_S`'s month 12. `Data`
  holds the column on such a row under `pct_av` to 10% of the account value, to a cent:
  an extract carrying year 1's allowance of 10,000.00, read before the anniversary, is
  refused, and one carrying 10,445.004 projects from 10,445.004, the column, not the
  product. The point's remainder, 10,000.00, is year 1's and lapses unread. On an
  interest-only contract valued on an anniversary the allowance is the interest credited
  over the year before, which no value at the anniversary gives: `MYGA_US_S`'s point 5 at
  its month 12 would carry its first year's interest, 4,450.00, which is also the interest
  to the anniversary, and `Data` holds the column to it in the second contract year. From
  the third year on the allowance is the interest of one year out of several, which no
  other column gives, and `Data` refuses only an allowance above the interest credited to
  the anniversary.
- **`interest_credited_pp_init`.** Point 9, under the interest-credited cap, is valued at
  month 30 with 11,426.34 credited since issue. The cap holds the MVA on a surrender to the
  lesser of the surrender charge and the interest credited to date: at `t = 0` the
  charge, 6,423.11, is the lesser, so the MVA is −6,423.11 and the surrender benefit
  78,912.44. With both interest columns at 0, and year 3's allowance at 0 with them, the
  interest to date would be month 0's alone, 332.31, and the surrender benefit 85,003.23.
- **`interest_credited_pp_prev_anniv_init`.** Point 9 credited 9,098.02 to its second
  anniversary. Its contract year 4, from `t = 6`, has the interest credited over year 3
  as its allowance: 13,438.44 credited by `t = 5` less those 9,098.02, so 4,340.41. With
  the column at 0, and year 3's allowance at 0 with it, since that allowance cannot
  exceed the interest to its anniversary, the allowance would be every dollar credited
  since issue, and the surrender charge on a lapse at `t = 6` would fall from 5,366.26 to
  4,820.38.
- **`free_wd_remain_init`.** Point 9 has nothing left of year 3's allowance of 4,648.02:
  the $20,000 at policy month 29 used it. So a surrender at the end of month 0 is charged
  on the whole account value, 7% of 91,758.65, or 6,423.11. Had the year's allowance been
  left whole, it would shelter 4,648.02, and the charge would be 6,097.74.
- **`prem_accum_gmir_pp_init`.** Point 10, Camp B under the GMIR-floored cap, carries
  100,626.17. The cap holds `AV + M` at or above `P_accum`: at `t = 0` it lifts the MVA
  from its raw −12,203.50 to `P_accum − AV`, −11,257.20, and the surrender value from
  92,631.19 to 93,577.50. With the column at 0 the cap would not bind. In months 0 to 2
  the Model #805 floor binds as well, so the surrender benefit is the floor, 93,970.22 at
  `t = 0`, either way.
- **`mgsv_pp_init`.** That floor opens from point 10's 93,754.22 entering month 0. With the
  column at 0 a lapse at `t = 0` would receive the surrender value of 93,577.50 rather
  than the floor. Point 9's floor, 75,862.37, is net of charges: the $20,000 reduced it by
  the 17,850.72 actually paid, its MVA and its charge deducted.
- **`av_pp_init`.** Every point in force opens its account value from it, at `t = 0`:
  point 9's 91,426.34 is what its $20,000 at policy month 29 left, with that month's
  interest. Halved, to 45,713.17, it closes month 0 at 45,879.33. A contract in force has
  an account value above 0, and `Data` refuses 0: one fully withdrawn is no longer in
  force.
- **`tax_basis_pp_init`.** Point 8's basis is the premium, 100,000.00, with nothing
  withdrawn before its first anniversary, so the $4,000 at `t = 0` is taxable in full,
  income first: the account value exceeds the basis by 4,450.00. With the basis at the
  account value it would be none. Point 9's 91,095.23 is the premium less the 8,904.77 of
  its $20,000 withdrawal that was not gain. The basis drives no cash flow.
- **`credit_rate_init`.** Point 12's renewal rate, 4.45%, was declared at policy month 60,
  the month before the valuation date, and `credit_rate` reads it from the row through
  `t = 58`, policy month 119; at `t = 59`, its next window, the rate is redeclared from
  the scenario. With the column at the GMIR, 0.25%, the least `Data` accepts there, the
  account value at `t = 58` would be 126,313.41 instead of 154,555.49. Point 13 reads its
  rate, declared at policy month 468, from its row too. Point 11, valued in its window,
  redeclares at `t = 0` from the scenario, and its column, the initial rate entering
  month 60, is unread.
- **`mva_ref_yield_locked_init`.** Point 12's `i0`, 10.00%, was locked at policy month 60
  at the stress scenario's yield. At the scenario's current 10.00% the MVA is zero; had `i0`
  been locked at 8%, a surrender at `t = 0` would carry an MVA of `(8% − 10%) × 4.83` years
  on the excess, −10,903.39, capped at the charge, −5,639.69. On point 11 the period starts
  at `t = 0` and `i0` is locked from the scenario, and on point 13, Camp B past its initial
  term, no MVA applies and the column is carried unread.

`MYGA_US_S`'s `av_pp_init()` and `mgsv_pp_init()` compute the issue values,
`P (1 − load_prem_rate)` and `0.875 P`, because, as [`model.md`](model.md) says, shipping
them as data would let a model point silently violate the statute [R1]. The rules are
kept, and moved: `prem_to_av_pp(t)` credits `P (1 − load_prem_rate)` and the new
`prem_to_mgsv_pp(t)` credits `net_consideration_ratio × P` in the month with
`duration_mth(t) = 0`, and `P_accum` takes the premium there too. The cells that bear the
notes' names for the opening values, `av_pp_init()` and `mgsv_pp_init()`, read the opening
state instead, 0 on new business, as `pols_if_init()` does for the count.

The allowance of the year under way is carried rather than the account value at the
anniversary it was fixed on, because the account value gives only the `pct_av` allowance.
The interest-only allowance is the interest credited over the year *before* the one under
way, on an anniversary valuation `I(d − 1) − I(d − 13)`, which needs the cumulative
interest two anniversaries back. Carrying the allowance covers both rules with one
column, and the account value at the anniversary is then needed by nothing.

## Departures from MYGA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock or of the opening
state, and every recursion begins at `t_entry()`. Where `MYGA_US_S`'s test would have
stayed correct on the valuation clock, it moved anyway, so that cover has one definition.
Of `MYGA_US_S`'s 127 cells, 53 are unchanged, 13 have a new docstring only and 61 are
rewritten; none is renamed or removed, and 30 cells are new, 157 in all. The twin identity
would fail on a cell of `MYGA_US_S`'s that this model lacked.

| Cells | `MYGA_US_S` | `MYGA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration`, `policy_year` | `t`, `t // 12`, `t // 12 + 1` | `duration_mth_init() + t`, and the other two on `duration_mth(t)` | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × (100 − x)`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past maturity | The frame starts at the valuation date. `maturity_mth()` is new and keeps `MYGA_US_S`'s formula |
| `gp_index`, `gp_end`, `in_gp_window`, `redeclare_month`, `mva_term` | arithmetic and tests of `t` against `12n` | the same of `duration_mth(t)`; `redeclare_month` still returns a policy month | The guarantee periods, their windows and the redeclarations are on the policy clock |
| `pols_if`, `pols_if_init`, `pols_if_at` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`, two cells a month | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`, one cell a month, with `"BEF_NB"` added; `pols_if_init()` is 0 unless in force | Contracts in force at the valuation date open the count; new business joins it in its issue month |
| `av_pp`, `av_pp_at` | `av_pp(t)` through `av_pp_at` at `"BEF_INV"` and `"BEF_WD"`, three cells a month, from `av_pp_init()` at `t = 0` | the opening written in both, `av_pp(t − 1)`, or `av_pp_init()` at `t_entry()`, plus the premium credited in the issue month | One cell a month. The values are `MYGA_US_S`'s bit for bit |
| `av_pp_init`, `mgsv_pp_init` | compute the issue values, `P (1 − load)` and `0.875 P` | read the in-force columns, 0 on new business | The issue values stay rules, crediting the issue month (`prem_to_av_pp` and the new `prem_to_mgsv_pp`) |
| `prem_to_av_pp`, `mgsv_pp`, `prem_accum_gmir_pp` | the premium credited, the floor's 87.5% and `P_accum`'s premium at `t = 0` | in the month with `duration_mth(t) = 0`, on top of the opening state from `t_entry()` | A contract's issue values arrive in its issue month, whenever that is |
| `interest_credited_pp`, `tax_basis_pp`, `taxable_wd_pp` | open at `t = 0` from 0 and from `tax_basis_initial` | open at `t_entry()` from `interest_credited_pp_init()` and `tax_basis_pp_init()` | Every recursion begins on the books, from the opening state |
| `tax_basis_pp_init` | reads `tax_basis_initial` | reads the same column, renamed `tax_basis_pp_init` | One vocabulary for the opening state |
| `free_wd_avail` | reset where `t % 12 = 0`; carried as `free_wd_remain(t − 1)`, two cells a month | reset where `duration_mth(t) % 12 = 0`; carried as `free_wd_avail(t − 1) − wd_free_pp(t − 1)`, one cell a month, from `free_wd_remain_init()` at `t_entry()` | The contract year is on the policy clock, and the remainder carried into the valuation date is opening state |
| `free_wd_base` | `av_pp_at(12 (y − 1), "BEF_WD")`, a policy month passed as `t` | `av_pp_at(12 (y − 1) − duration_mth_init(), "BEF_WD")`, asked only for a year that opens on the books | On the valuation clock month `12 (y − 1)` is not the anniversary that opens year `y` |
| `free_wd_allow` | the interest credited to the ends of months `12 (y − 1) − 1` and `12 (y − 2) − 1`, policy months passed as `t` | the same months as valuation months; the year under way from `free_wd_allow_init()`, and the interest at the anniversary that opened it from `interest_credited_pp_prev_anniv_init()` | The same, and a year that opened before the valuation date is opening state |
| `credit_rate` | `market_rate(redeclare_month(t))`, a policy month passed as `t`; the initial rate while `t < 12n` | `market_rate(m)`, `m = redeclare_month(t) − duration_mth_init()`, or `credit_rate_init()` where `m` is before `t_entry()`; the initial rate while `duration_mth(t) < 12n` | A rate declared before the valuation date is a fact of the past, and one declared after it is read on the valuation clock |
| `mva_ref_yield_locked` | `mva_ref_yield(gp_start_month(t))`, a policy month passed as `t` | `mva_ref_yield(m)`, `m = gp_start_month(t) − duration_mth_init()`, or `mva_ref_yield_locked_init()` where `m` is before `t_entry()` | The same, for the yield locked at the start of the period |
| `wd_scheduled_pp`, `wd_pp` | the withdrawal table at `(wd_schedule_id, t)`; the utilization where `t % 12 = 0` | at `(wd_schedule_id, duration_mth(t))`; the utilization where `duration_mth(t) % 12 = 0` | Withdrawals stay on the policy clock |
| `in_gp_window`, `redeclare_month`, `surr_charge_id`, `mva_term`, `lapse_rate_base`, `free_wd_allow`, `mva_rate`, `mva_pp_on`, `mgsv_wd_deduct_pp` | branch on the text of `renewal_architecture()`, `free_wd_rule()`, `mva_family()`, `mva_cap_rule()` and `mgsv_wd_convention()` | branch on the new `is_*` cells, one bool for each value `MYGA_US_S` tests, decoded once a point from the model point's column; a value `MYGA_US_S` does not know is answered as there | No projection cell compares a model point column's text or calls a label accessor, which are left to reporting; Phase 2 moves the decodes into `Data`. The text a branch still compares is `MYGA_US_S`'s own: the timing and kind strings, and the schedule `surr_charge_id(t)` names, which `surr_charge_rate` tests for `none` and joins on, part of the surrender-charge join Phase 2 re-keys |
| `mort_rate`, `surr_charge_rate`, `surr_charge_age_cap_at`, `scenario_rate`, `wd_scheduled_pp`, `mva_duration_factor` | read `MYGA_US_S`'s readers' tables, and take the age cap's and the duration factors' extents by `int()` of the raw keys | read `Data`'s checked tables, `mort_rates`, `surr_charge_scales`, `surr_charge_age_caps`, `rate_scenario_steps`, `wd_schedules` and `mva_factors`, and the extents from the same checked keys; the joins on text keys take the key from the model point's column; the duration factors are read through the new `mva_factor_at(k, column)`, keyed by the whole year | A key the table cannot be read by is refused by name before a value is read, and every table is read through one cell |
| `premiums`, `prem_to_av` | at `t = 0`, on `pols_if_init()` | on `pols_new_biz(t)` | A point in force paid its premium before the valuation date, and one issued later pays it in its issue month |
| `expenses` | acquisition at `t = 0` on `pols_if_init()`; zero where `t < 0` or `t ≥ proj_len()` | `expense_acq × pols_new_biz(t)`; zero outside cover | Acquisition per contract issued, in the issue month and not inflated, as in `basiclife/BasicTerm_SE` |
| `inflation_factor` | `1.025^duration(t)`, stepping on the contract's anniversaries | `1.025^(t // 12)`, stepping every twelve months from the valuation date | Unit costs in valuation-date dollars |
| `pols_maturity` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `check_pols_roll_fwd_resid`, `av_at`, `av_change` | `pols_if(t + 1)`, the next month's count; the block's account value opening from 0 at `t = 0` | `pols_if_at(t + 1, "BEF_NB")`; from `av_pp_init() × pols_if_init()` at `t_entry()` | Next month's new business is no part of month `t`'s movement, and a point in force opens with its account value |
| `check_av_roll_fwd`, `check_pols_roll_fwd` | `all(...)` over the frame, the tolerance fixed | a loop over the frame, the tolerance scaled by `max(policy_count(), 1)` | A residual is rounding on that many contracts |
| `pols_annuitization`, `pols_death`, `pols_lapse`, `withdrawals`, `mort_rate`, `surr_charge_rate`, `surr_charge_age_cap`, `mva_in_force`, `mva_duration_factor`, `lapse_rate_base`, `lapse_dyn_exponent`, `lapse_dyn_market`, `lapse_dyn_rate`, `lapse_rate`, `mgsv_charge_pp` | unguarded: no `MYGA_US_S` frame has a month outside cover | zero or false outside cover, before any table or rate is read; `surr_charge_age_cap` calls the new `surr_charge_age_cap_at(age(t))`, the one reader of its table | A contract year or an attained age the contract does not have is never looked up, and nothing is charged or decremented there |
| `result_pols` | `pols_if`, the four outflows and `pols_if_aft_decr` | `pols_new_biz` second | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz`, the seven new opening-state accessors and the fourteen `is_*` decodes. The
docstring-only changes rewrite the time-axis prose, wrap three summaries to 92 characters,
correct "This cells" in `annuitization_pp`, and say that `result_av`'s `free_wd_avail`
column holds `free_wd_remain`. In `Data`, `model_point_table` reads
`model_point_table_sec.csv` and checks it, `future_horizon_mth` is new, four readers'
docstrings changed, `rate_scenario`'s and `withdrawal_table`'s to name the clock their `t`
is on, and nine cells are new: the six checked tables and the three extents,
`surr_charge_age_cap_first`, `surr_charge_age_cap_last` and `mva_factor_last_year`.
`MYGA_US_S`'s six readers are unchanged.

The four joins on text keys stay `MYGA_US_S`'s, each in the one cell that reads its
table: mortality on the model point's `sex`, the scenario on its `scenario_id`, the
withdrawals on its `wd_schedule_id`, and the surrender charge on the schedule
`surr_charge_id(t)` names, a string-valued cell of `MYGA_US_S`'s, which `surr_charge_rate`
also tests for `none`: with the timing and kind strings, the one text a projection cell
compares in a branch. Phase 2 re-keys them, as it turns the decodes into `Data` vectors.
`Data` checks each key before a projection joins on it: the model point table refuses a
point whose scenario, withdrawal programme, or sex and attained age the tables lack, and
the surrender charge table one without both schedules, where `MYGA_US_S` raises an error
that names no file or charges nothing.

No read goes further ahead than the month after its own: the block's closing account
value, weighted by the count carried into the next month, and the in-force roll-forward
read `t + 1`, and the two free-withdrawal cells read nothing later than the anniversary
that opens the year they are asked for.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 8's
`expenses(t)` is `MYGA_US_S`'s `expenses(12 + t)` divided by 1.025, and point 11's,
valued five years on, by `1.025^5`. Their other cash flows, their counts and every value
per contract are `MYGA_US_S`'s from the month they are valued at on. Point 14 is
`MYGA_US_S`'s point 1 fifteen months on in those columns too. Its maintenance expense is
1.025 times S's, since the valuation clock stepped at `t = 12`, before the point's issue,
and `1.025^2` times S's in months 9 to 11 of each of its contract years, between the
valuation clock's next step and the point's own anniversary.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 7, issued at
  the valuation date, every cell of `MYGA_US_S`'s agrees at every argument `MYGA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point`, `av_pp_init`,
  `mgsv_pp_init` and `result_pols`, whose meaning changed. So the goldens
  `tests/test_fixed_deferred_annuity_us.py` asserts on cells that sweep reaches — the
  worked example's table to the cent, both surrender traces line by line and the
  roll-forwards among them — hold here with no number restated. The identity holds on any
  count, since `MYGA_US_S` already takes the premium and charges acquisition on the
  contracts issued. The same suite holds the model to the conventions every `_SEC` model
  meets: every frame starts at `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business
  enters once at its `policy_count`, nothing happens before issue, and the in-force
  columns are present.
- **The splice**, in `tests/test_fixed_deferred_annuity_us_sec.py`: each `MYGA_US_S` point
  restated in force at a month either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share, to
  1e-9, but those the twin identity skips; `proj_len`, a frame on the valuation clock;
  `scenario_id`, which names the row's own scenario (below); and `tax_basis_pp_init`, the
  basis entering the row's valuation month where S's is the basis at issue, though
  `tax_basis_pp` and `taxable_wd_pp`, which open from it, are compared. The months are 11
  and 12, either side of the first anniversary; 30, after point 5's excess withdrawal; 59,
  60 and 61, the last month of the initial term, the window and the month after it; 89,
  inside the first renewal period, after point 3's redeclaration at 84; and 479, the last
  covered month. So do four variants of S's points, in a copy of S's table that is never
  committed, for what S's own points do not reach: a female contract at the GMIR's middle
  band, with the floor's annual charge and premium tax; a qualified contract at its high
  band, with no basis; a seven-year guarantee period; and issue at age 85, where the age cap
  binds. Each spliced row runs on its own copy of its S scenario, re-based to its month and
  stepped within the initial term and the renewal periods, so that a rate read at the wrong
  month or on the wrong clock reads another number, and the renewal surrender charges are
  set apart from the initial ones. Inflation, on the valuation clock, is set to 0 in both
  models, and four assumptions that ship at zero are switched on in both, the
  free-withdrawal utilization, a renewal spread, the acquisition expense and a premium load,
  because at the shipped zeros they hide parts of the state from any comparison. A contract
  year that closed before the splice month is no year of the restated row, and its allowance
  is not compared.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch, every opening-state column,
  every kind of valuation month and every product switch the full grid reaches, and a test
  asserts that they do. The other cases carry the `sec_full` marker and show as skipped,
  with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so
  every CI run runs the full grid too.
- **Future new business**: issued 1 and 15 months after the valuation date, each S point
  is the S projection moved on, with zeros before issue in `result_cf`, `result_pols` and
  `result_av` and no decrement rate evaluated there, and so is each variant issued a month
  on. A point issued 15 months on reads contract year −1 before issue, which is what shows
  a missing guard.
- **How it computes**: on every row the splice and the future business compare, after
  every report, no cell has been called at a negative month, none evaluated from
  `t_entry()` on has read a month before it, none evaluated at month `t` has read a month
  later than `t + 1`, directly or through a cell keyed by a contract year, an age or a
  year remaining, and no contract year that closed before the valuation date has been
  asked for. On a fresh read of the committed model `duration_mth` is a closed form, every
  point is swept under a lowered recursion limit, which a recursion backward over the
  frame would exceed, and a cold last-month call runs at most one cell a month back to
  `t_entry()`, plus a fixed overhead, on the committed points and at issue age 0.
- **Counts, validation and regeneration**: the roll-forward closes, `"AFT_DECR"` is the
  next month's `"BEF_NB"`, and `pols_if_at` refuses a timing it does not have;
  `result_pols()` is `MYGA_US_S`'s, column for column, with `pols_new_biz` beside it;
  doubling `policy_count` doubles every cash flow and moves no per-contract value, and at
  a million contracts both roll-forward checks close on their scaled tolerance; each
  malformed row is refused naming its point, a missing, negative, infinite or misplaced
  opening state among them, each state column on new business and on future business, a
  zero account value in force, an interest-only allowance above the interest at its
  anniversary, a stale allowance at either end of the first contract year and on an
  anniversary, an interest-only allowance apart from the first year's interest at either
  end of the second, and a scenario, a withdrawal programme, a sex or an attained age that
  the table it keys lacks; each assumption table whose keys cannot be read, a key written
  as text in each of the six, a blank, a fractional or a repeated key, a gap, a blank text
  key and a value out of its range, is refused naming the file and the lines, and the
  renewal schedule misspelt naming the file, by `Data` and by a projection that reads it;
  a scenario that starts after the first month a point on it is on the books is refused
  for that point, and read for a point issued no earlier; keys written as floats are read
  by value; the horizon is a Reference, which at 0 refuses any future business, saying so;
  a point past its cover is refused by `proj_len()`, and `run_sec.py --block` refuses it
  before printing anything; a zero count, durations written as floats, a negative floor
  and `P_accum`, a zero basis, a contract issued 120 months on, on an anniversary a
  remainder above the year's allowance, allowances carried to the cent, the ties at half a
  cent among them, and an interest-only contract on its second anniversary, which
  continues `MYGA_US_S`, are accepted; and the committed table is what `MYGA_US_S`
  generates.
- **The opening state and the rest**: each derived row's opening state is what `MYGA_US_S`
  carries into its month, and at the shipped assumptions the row is S's from that month
  on, in every cell but those expense inflation moves; each state column, changed, moves
  its committed row as above; the rate scenario runs on the valuation clock and the
  withdrawals on the policy clock; expense inflation runs on the valuation clock at the
  shipped 2.5%, which only this test sees, since the splice sets the rate to 0;
  acquisition falls on new business alone, per contract issued, asserted at 2.5 contracts
  a point; every guarded cell holds its value outside cover and reads no rate there, and
  every monthly cell answers there; the points of a block sum row by row; an extract
  without the generator's three columns, labelled apart from its positions, projects the
  same numbers; and `run_sec.py` prints the model's numbers, for a point issued at the
  valuation date, two points restated and the block, and writes "1 month" for a point a
  month either side of the valuation date.

```bash
python -m pytest tests/test_fixed_deferred_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_fixed_deferred_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k MYGA_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R6]: #uslib-fixed_deferred_annuity-r6
[std]: #uslib-std
<!-- END generated citation links -->
