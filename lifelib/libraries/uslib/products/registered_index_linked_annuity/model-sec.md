# In-Force Implementation Notes

**Status:** Draft, 2026-11-03. `RILA_US_SEC` is [`RILA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of any term, and contracts to be written in the ten years
after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The
product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in `BasicTerm_SE`,
and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `RILA_US_S` on another time axis, and it reads `RILA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced: the 10% buffer, the
> 1, 3 and 6 year terms and their guaranteed minimum rates, the 7-7-6-5-4-3-0 withdrawal
> charge above a 10% free amount, the return-of-premium death benefit for issue ages 80
> and under, the Maturity Date rule and the interim value algebra [S1] [S2] [S4] [S5] [S6]
> [R2]. The declared rates and the market data are a **[std]** snapshot, every behavioural
> and expense assumption is a **[std]** standardization, and the shipped mortality table
> is illustrative, *not* a published basis. Replace them with company data before drawing
> any conclusion from the numbers.

## Run it

```bash
python products/registered_index_linked_annuity/run_sec.py          # point 1, at t = 0
python products/registered_index_linked_annuity/run_sec.py 16       # in force 71 months
python products/registered_index_linked_annuity/run_sec.py --block  # every point, summed
```

The first prints what `run.py` prints for `RILA_US_S`'s point 1, the worked example's
anchor cell, issued here at the valuation date: the option budget of 10.0632%, 10,063.19
of the 100,000 purchase payment, the fixed leg opening at 89,936.81 and accreting at
1.7834%, a 2.22% spread; the interim value decomposition at `t = 0`, 11, 35, 71 and 143;
and the cash flows of rows `t = 0 … 11`, every number the same. Above them it says where
the point stands at the valuation date and where the term under way started.

The second prints point 16, the same contract in force 71 months. Its row `t = 0` is the
worked example's month 71, the Term End Date at +40%: the index at 140 against the
`I_s` of 100 that the term started from, which the row carries, credits 40% on the
Investment Amount of 100,000, so the interim value is 140,000.00. The roll split then
leaves 119,000.00 in the option and moves 21,000.00 to the Fixed Account, 21,051.79 after
the month's interest, and the term-end surrender concentration of a charge-free year, 10%,
takes 12,454.89 of surrender value. Every column agrees with `RILA_US_S`'s months 71 to
359 but `expenses`, which are in valuation-date dollars here, 4.25 at `t = 0` where
`RILA_US_S` has 4.81, and `net_cf` with them. Its decomposition prints `t = 0`, the
second term's midpoint, `t = 36`, and that term's end, `t = 72`, where the index, still at
140, credits nothing. Three lines to the same thing for point 16:

```python
import modelx as mx
model = mx.read_model("products/registered_index_linked_annuity/RILA_US_SEC")
model.Projection[16].result_cf()
```

`Projection` takes a `point_id`, as in `RILA_US_S`. `result_cf()` has `RILA_US_S`'s nine
columns — `pols_if`, `premiums`, `withdrawals`, `claims_death`, `claims_lapse`,
`claims_maturity`, `expenses`, `premium_taxes` and `net_cf` — with one row per month from
the valuation date, `t = 0 … proj_len() − 1`. `result_av()` has `RILA_US_S`'s eleven
values per contract on the same rows, `result_iv()` the interim value decomposition, one
column per leg of the replicating portfolio, and both are zeros before issue.
`result_pols()` sets out the counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then
the month's deaths, surrenders, the term-end part of those surrenders and the forced
annuitizations at the Maturity Date, then `pols_if_aft_decr`, the notes' end-of-month
`l(t+1)`, as in `RILA_US_S`.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]`, then a
collection), so the run holds the cells of one point at a time. It freezes what is alive
once the model and its table are read (`gc.freeze()`), and again before the projections,
so that each collection scans only what the run has made since. It prints a line per point
on where it stands at the valuation date, then the block's first twelve rows and the block
summed into projection years, `t // 12 + 1`. Each derived row runs on its own copy of its
scenario (*The market scenario*, below), so the shipped table is a set of test cases rather
than a block valued on one market, and the block shows how the frames add, and nothing
more.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however long the contract has been in force,
  month `t` runs from time `t` to time `t + 1`, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the Maturity Date.
- **`duration_mth(t)`, the policy clock**, counts the months elapsed from issue at the
  start of month `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is `RILA_US_S`'s `t`, and the
  contract runs on it. `RILA_US_S`'s two readings of the contract year are kept, each on
  this clock: the interval reading `duration(t) = duration_mth(t) // 12`, which sets the
  attained age `age(t) = age_at_entry() + duration(t)`, and the month-end reading
  `duration_eom(t) = (duration_mth(t) + 1) // 12`, which sets the withdrawal charge and
  `policy_year(t) = duration_eom(t) + 1`. The term in force is
  `term_elapsed_mth(t) = duration_mth(t) % (12 T) + 1` months old at the month end, and
  `is_term_end(t)` is true where that reaches `12 T`. `BasicTerm_SE` reaches the policy
  clock by adding one a month, a recursion as long as the frame; the closed form needs no
  such chain of calls.

Every within-month quantity is still evaluated at the month **end**, time `t + 1`, as in
`RILA_US_S`: the market state, the interim value, the Account Value and the benefits on
row `t` are the values there, while `pols_if(t)` is the count entering the month at time
`t`. So the month that closes on an anniversary or a Term End Date is the last month of
its contract year or of its term, policy month `12 cy − 1` or `12 T k − 1`.

Point 16 is the anchor cell in force 71 months. At `t = 0` it is in policy month 71, the
last month of contract year 6, at attained age 65: the month that closes on its sixth
anniversary and on the end of its first term. Its first renewal term opens at `t = 1` and
ends at `t = 72`, policy month 143, its next at `t = 144`, and the Maturity Date closes
policy month 359, at `t = 288`, so its frame has 289 rows. Point 20 is a Step Rate option
on a one-year term in force 30 months: the term under way began at policy month 24, six
months before the valuation date, from the `I_s` of 100 that its row carries, and ends at
`t = 5`, policy month 35, crediting the 8% step on the index's 120. Point 24 is the
anchor cell to be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is
on the books from `t_entry() = 13`, rows 0 to 12 are zeros, its first anniversary closes
`t = 24`, its first term ends at `t = 84`, and its frame has 373 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the terms, their Term Start and End Dates and the Transfer Period at each Term End Date; the cap re-solved at each renewal under `nge_reset`; the time to expiry `tau` of the option in force; the Contract Anniversaries, the free-withdrawal base snapshotted at each and the reset of the Free Withdrawal Amount; the behavioural withdrawal at each anniversary; the withdrawal programme, whose `month_end` in `withdrawal_table.csv` is a policy month end; the withdrawal charge by complete contract years and the charge-expiry shock year; the base surrender rate by contract year and the term-end surrender concentration; mortality at the attained age; the return-of-premium band, by issue age; the Maturity Date | the market scenario, `market_state(t, name)`, whose `month_end` in `market_scenario_sec.csv` is a time on the valuation clock: the index level, the Market Value Rate, the risk-free rate, the dividend yield and the implied volatility at month `t`'s end, `t + 1`, and on the Term Start Date of a term that starts at or after the valuation month; expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

The market scenario is a path in calendar time, shared by every contract of a block, so it
moves to `t`. What a term fixed when it started is a fact of the contract instead: the
index level `I_s`, the Market Value Rate `r_0` and the risk-free rate, dividend yield and
volatility the option budget is priced at, and, at a renewal under `nge_reset`, the cap
solved from them. A Term Start Date at or after the valuation month is read from the
scenario at the time it falls at, and one before it from the opening state (*The opening
state*, below). `term_start_month(t)` still returns a policy month, and each of the five
cells that read a term's start, `index_at_term_start`, `mvr_at_term_start`,
`risk_free_at_term_start`, `div_yield_at_term_start` and `impl_vol_at_term_start`, and
`cap_rate`, turns it into a month from the valuation date once, by subtracting
`duration_mth_init()`. Point 19, valued at its renewal at policy month 72, takes its `I_s`
of 140 and its re-solved cap from its scenario at `t = 0`; point 18, eight months later,
takes both from its row.

Expense inflation keeps `RILA_US_S`'s annual step, which `RILA_US_S` takes on the contract's
anniversaries as `1.025^duration(t)`, but takes it every twelve months from the valuation
date, `1.025^(t // 12)`, so the maintenance charge, $60 a contract a year, is in
valuation-date dollars for every point alike. Acquisition, 6% of the purchase payment plus
$200 a contract issued, is charged in the issue month and not inflated, and so is the
premium tax, 0% as shipped, on the purchase payments of the contracts issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`RILA_US_S` computes, whatever the point's count: `RILA_US_S` already takes the purchase
payment and charges acquisition on the contracts in force at its `t = 0`, which on new
business are the contracts issued, and on a contract issued at the valuation date this
model's market is `RILA_US_S`'s own scenario. On `RILA_US_S`'s fifteen points every cash
flow, every count and every value per contract agrees bit for bit, and so does every
other cell the two models share but three whose meaning changed: `pols_if_init()`, now the
count already in force at the valuation date, 0 for such a point; `model_point()`, a row
of another table; and `result_pols()`, which gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `RILA_US_S`'s columns,
and fifteen of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and
thirteen that open an in-force contract's state. Each of the fifteen is a number, and
every amount is per contract. The market scenario the table's rows run on is in a second
file, `market_scenario_sec.csv` (*The market scenario*, below).

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy months elapsed from issue: positive in force, in any month of any term, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `inv_amt_pp_init` | dollars, 0 or more | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | `IA`, the Investment Amount (AG 54's Index Strategy Base [R2]): the notional the month's crediting and interim value apply to, after every term-end credit, roll split and proportional withdrawal reduction before it. It is also the crediting basis |
| `fixed_acct_pp_init` | dollars, 0 or more | the start of month 0 | `FA`, the Fixed Account |
| `holding_acct_pp_init` | dollars, 0 or more | the start of month 0 | `HA`, the Holding Account |
| `av_pp_init` | dollars, of either sign | the start of month 0: after policy month `duration_mth − 1`'s withdrawal | `AV`, the Account Value, the interim value plus the two accounts |
| `av_pp_prev_anniv_init` | dollars, of either sign | the Contract Anniversary on or before the valuation date, before the withdrawal of the month that closes on it, policy month `12 × (duration_mth // 12) − 1` | `AV_anniv(y)`, the base of the contract year's Free Withdrawal Amount; the purchase payment in the first contract year, which opened at issue |
| `free_wd_remain_init` | dollars, 0 or more | the start of month 0 | the Free Withdrawal Amount still unused in the contract year |
| `rop_pp_init` | dollars, 0 to the purchase payment | the start of month 0 | the return-of-premium death benefit base: the purchase payment, reduced in proportion by each withdrawal |
| `index_at_term_start_init` | an index level, above 0; blank where not read | the Term Start Date of the term under way, where it precedes the valuation month | `I_s`, the index level the term's performance is measured from |
| `mvr_at_term_start_init` | a rate a year, effective, above −1; blank where not read | the same | `r_0`, the Market Value Rate then, which the interim value's rate adjustment reads [S2] |
| `risk_free_at_term_start_init`, `div_yield_at_term_start_init` | rates a year, effective, above −1; blank where not read | the same | the risk-free rate and the dividend yield the term's option budget is priced at |
| `impl_vol_at_term_start_init` | a volatility a year, above 0; blank where not read | the same | the implied volatility the term's option budget is priced at |
| `cap_rate_init` | a rate, at least the term's guaranteed minimum cap; blank where not read | the Term Start Date of the term under way, where it is a renewal under `nge_reset` before the valuation month | `c`, the Cap Rate re-solved at that renewal and floored at the guaranteed minimum |

On a point issued at or after the valuation date every amount is 0 and every term-start
value blank: such a contract opens with nothing, its purchase payment arriving in its issue
month, and its first term reads its start from the scenario. In the first contract year,
`duration_mth` 1 to 11, no free amount is available, so `free_wd_remain_init` is 0, and the
year opened at issue, so `av_pp_prev_anniv_init` is the purchase payment. Before the first
Term End Date, `duration_mth` 1 to `12 T − 1`, nothing has been transferred to either
account, so both are 0. On a point valued at a renewal, `duration_mth` a positive multiple
of `12 T`, the month before closed a term, where the interim value is the Investment Amount
itself, so `av_pp_init` is the Investment Amount plus the two accounts. On a point valued
on an anniversary, `duration_mth` a positive multiple of 12, the anniversary that opened
the year is the valuation date itself, and `av_pp_prev_anniv_init` is the Account Value
before that month's withdrawal and `av_pp_init` the value after it: they differ by the
withdrawal, as on point 17, by its $8,000. `prev_anniv` is the anniversary that **opened**
the contract year: an extract that fills the column from the anniversary after the
valuation date is a year out.

**The term-start values are given only where the term began before the valuation month**,
`duration_mth` positive and not a multiple of `12 T`, and blank everywhere else. They are
facts frozen at a past date, as `DIA_US_SEC`'s cohort weights are: no scenario re-based to
the valuation date holds a level before it, and a sensitivity run that moves the market at
the valuation date must not move them. Where the Term Start Date is at or after the
valuation month the scenario holds it: a renewal at the valuation month reads the
scenario at `t = 0`, and a future row's first term reads its copy at its issue month. So
a blank is the honest value there, and `Data` holds every given index above 0, the level
`index_perf` divides by, with no exception for a row that does not read it. A table
written the other way, with the value entering month 0 on every row, is refused.
`cap_rate_init` is narrower still: it is given only where that term began at a renewal
under `nge_reset`, `duration_mth` above `12 T`. Off `nge_reset`, and under it in the
initial term, the cap is the model point's declared cap floored at the guaranteed
minimum, which no column needs to restate. At a renewal under `nge_reset`, `RILA_US_S`
re-solves the cap from that date's market and the References `earned_rate`, `nge_spread`,
`nge_solve_iter` and `nge_cap_search_max`, a contractual fact fixed then.

**The Account Value may be of either sign.** It is the interim value plus the two
accounts, and the interim value can be negative even when the index has risen [S2]:
flooring it is not implementing the contract. `RILA_US_S` carries a contract through a
negative interim value, so `Data` accepts any finite `av_pp_init` and
`av_pp_prev_anniv_init`. The four balances a contract holds, the Investment Amount, the
two accounts and the return-of-premium base, are zero or more, and a contract in force
that holds none of the first three is refused instead: only a full withdrawal leaves a
contract nothing, and such a contract is no longer in force.

**There is no Performance Lock.** `RILA_US_S` does not implement it: the notes give the
election rule and the dollar-for-dollar withdrawal consequence, but not the rate at which
a locked bucket accrues to term end (*What is not implemented* in [`model.md`](model.md)).
This model is `RILA_US_S` run in force and adds none, so the notes' `lock_flag` and
`lock_value` are not columns, and an in-force contract carries no locked value. Nor is
there a column for the Term Start Date: terms start at issue and renew every `12 T` policy
months, so the date follows from `duration_mth` and `term_years`.

| `RILA_US_S` | `RILA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under `BasicTerm_SE`'s name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months. Every `RILA_US_S` point is new business, opening its frame at issue |
| — | `inv_amt_pp_init` | `RILA_US_S` opens the Investment Amount with the purchase payment at `t = 0` |
| — | `fixed_acct_pp_init`, `holding_acct_pp_init` | `RILA_US_S` opens both accounts empty |
| — | `av_pp_init` | `RILA_US_S` opens the month's investment return from the purchase payment, and the block's Account Value from 0, at `t = 0` |
| — | `av_pp_prev_anniv_init` | `RILA_US_S` reads every anniversary's base from its frame, which starts at issue |
| — | `free_wd_remain_init` | `RILA_US_S` opens the remainder at 0 in contract year 1, which has no free amount |
| — | `rop_pp_init` | `RILA_US_S` opens the base at the purchase payment |
| — | the five `*_at_term_start_init` | `RILA_US_S` reads every term's start from its scenario, at the Term Start Date's policy month passed as a time from issue |
| — | `cap_rate_init` | `RILA_US_S` re-solves every renewal's cap under `nge_reset` from its scenario |

A column measured entering month 0 is the cell it opens with `_init` added; the base
measured at the anniversary adds `_prev_anniv_init`, and the five fixings and the cap name
the cell they stand in for before the valuation month, with `_init`.
`free_wd_remain_init` takes no `_ytd`: it is not an accumulator restarting each year but
the remainder of an annual allowance, which each anniversary resets.

The columns carried over are read as `RILA_US_S` reads them. For a contract in force, the
facts they record are still those at issue, the option's terms included: a renewal keeps
its option, at the declared or the re-solved cap.

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex` | `M` or `F` | — |
| `premium` | dollars, the single purchase payment | issue |
| `term_years`, `buffer`, `crediting_type` | years, 1, 3 or 6; a fraction; `CAP`, `STEP`, `EDGE` or `FLOOR` | issue: the option, renewed at each Term End Date |
| `declared_cap`, `declared_step`, `declared_edge`, `participation`, `floor_rate` | rates; `declared_cap` blank for an uncapped option | issue: the declared rates of the initial term, and of every renewal off `nge_reset` |
| `iv_family`, `amort_rule` | `portfolio`, `notional`, `delta` or `legacy`; `straight_line` or `updated_expiry` | issue: the interim value algebra |
| `nge_reset` | a flag, `True` or `False` | issue: whether the cap is re-solved at each renewal **[std]** |
| `wd_rate_ann` | a fraction of the Account Value a year | the behavioural withdrawal rule **[std]** |
| `scenario_id`, `wd_schedule_id` | keys into `market_scenario_sec.csv` and `withdrawal_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `RILA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it. First the table's own shape:

- the fifteen in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, read by value, so that `12.0` is 12;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,200 months at issue age 0, the youngest the product
  issues [S1] [S2], and 720 at 40, the youngest the shipped mortality table rates. Set to
  0, the Reference refuses future new business altogether, and a negative horizon is
  itself refused.

Then the contract's terms, `term_years` before every check that reads the term clock:

- `age_at_entry` is a whole number of years, 0 or more, and `term_years` a whole number of
  years, 1 or more, each read by value: `RILA_US_S` reads both by `int()`, which truncates
  a fraction without a word, and the term clock counts months modulo `12 T`;
- `premium` is a number above 0;
- `buffer` and `floor_rate` are fractions, 0 or more and below 1, each the strike
  `I_s (1 − x)` of a put, and `participation` is a number above 0, by which the cap's
  strike divides;
- `declared_cap` is blank, for an uncapped option, or a number, zero or more, and
  `declared_step`, `declared_edge` and `wd_rate_ann` are numbers, zero or more: each
  reaches a `max` or a `min` that would lose a blank;
- `nge_reset` is a flag, read by value: `True` or `False`, as pandas reads either, or 1 or
  0, where `RILA_US_S`'s `bool()` reads any text, a blank among them, as `True`;
- `nge_reset` is set only on a capped Cap Rate option, `crediting_type` `CAP` with
  `declared_cap` given. `RILA_US_S`'s solver prices the at-the-money call, the call at the
  cap and the buffer's put: on a Floor option it would solve the wrong portfolio, and on a
  Step, an Edge or an uncapped option the flag does nothing, and `RILA_US_S` projects
  either without a word.

Then the opening state:

- the Investment Amount, the two accounts, the remainder and the return-of-premium base
  are numbers, zero or more, and the Account Value and its base at the anniversary are
  finite numbers of either sign;
- each term-start value, where given, is a number in its range: the index level and the
  volatility above 0, the Market Value Rate, the risk-free rate and the dividend yield
  above −1, each added to 1 under a division or a logarithm, and the cap a finite number;
- a contract not yet in force, `duration_mth` 0 or less, holds nothing yet: its seven
  amounts are 0;
- the five term-start values are given exactly where the term under way began before the
  valuation month, and `cap_rate_init` exactly where, besides, that term began at a
  renewal under `nge_reset`;
- a contract in force holds an Investment Amount or an account balance;
- `rop_pp_init` is at most the purchase payment;
- in the first contract year the remainder is 0 and the base at the anniversary is the
  purchase payment;
- before the first Term End Date both accounts are 0;
- on a renewal valuation `av_pp_init` is the Investment Amount plus the two accounts;
- on an anniversary valuation `av_pp_prev_anniv_init` is at least `av_pp_init`, the
  anniversary month's withdrawal lying between them.

Last, each point's keys into the tables it is joined with, each table's count cell asked
first, so that a malformed table is refused by its own message (below): its `scenario_id`
is a scenario of `market_scenario_sec.csv` that sets its levels by the first month the
point is on the books, `t = 0` or its issue month if later; its `wd_schedule_id` is a
programme of `withdrawal_table.csv`; its `term_years` is a term of
`guar_min_rate_table.csv`; `mort_table.csv` gives a rate at its `sex` and its attained age
in that first month; and `cap_rate_init`, where given, is at least the guaranteed minimum
cap of its term, which `cap_rate` floors every re-solved cap at. `RILA_US_S` meets a key
its table lacks only as it projects: a missing scenario, sex or age raises Python's own
error, naming no file, and a missing withdrawal programme takes no withdrawal, without a
word.

An extract may carry each amount of money to the cent, as an administration system holds it,
each within half a cent of its exact value, and every rule between amounts allows for that
without a tie falling to floating point: a cent where a rule compares one amount with
another or with 0, as `MYGA_US_SEC`'s do, and two and a half cents in the renewal rule,
whose identity ties four amounts and so can miss by two cents, half a cent from each.
`RILA_US_S`'s Edge option restated at its renewal at 36, every amount carried to the cent,
misses its identity by a cent, which floating point reads as 0.010000000009, and is read;
point 19's Account Value 0.024 above its Investment Amount and Fixed Account is read, and
0.03 above is refused. The generated rows carry `RILA_US_S`'s own values, unrounded. The
table is returned with the columns those checks read by value as the numbers they were
checked as: `duration_mth`, `age_at_entry` and `term_years` int64, `policy_count`,
`premium`, the rates and the thirteen opening-state columns float64, blank as NaN, and
`nge_reset` the flags it was checked as. A text column outside its categories passes `Data`
and is refused, with `RILA_US_S`'s message, by the cell that branches on it, wherever the
model first reads it (`invalid crediting_type`, `invalid iv_family`, `invalid amort_rule`).

Accepted, because a contract can be in each state: an Account Value below 0, at the
valuation date or at the anniversary; a zero count; and a `duration_mth`, an
`age_at_entry` or a `term_years` written as a float, read as the whole number it holds.

Two rules are the product's rather than the table's, because they need `Projection`
References, which `Data` cannot read, and `proj_len()` checks them, each raising
`ValueError` naming the point. A point at or past its Maturity Date at the valuation date,
`duration_mth ≥ maturity_mth()`, which needs `maturity_age` and `maturity_min_years`, has
no frame and is refused rather than projecting nothing. And from the second contract
year, `duration_mth` 12 or more, the remainder is at most the year's Free Withdrawal
Amount, `free_wd_rate × av_pp_prev_anniv_init`, to a cent: the year's withdrawals only
ever reduce it. That rule holds where the base is 0 or more, and is not applied below 0.
On a negative base `RILA_US_S`'s allowance is negative too, and its behavioural rule,
`min(wd_rate_ann × AV, allowance)`, takes the more negative of two negative amounts, a
withdrawal below 0, which the cap at the Account Value passes through; at a behavioural
rate above `free_wd_rate` that leaves a positive remainder no allowance bounds. This model,
`RILA_US_S` run in force, computes the same, and no shipped point's Account Value falls
below 0. A loop over the block meets a refused row only when it reaches it, after
projecting the points before it, so `run_sec.py --block` asks every point for its frame
before it projects any, and stops before it prints anything.

Left to the projection: an attained age past the mortality table's last before the
Maturity Date raises a `KeyError` there, as in `RILA_US_S`, because the maturity age is a
`Projection` Reference; the shipped table runs to 120, past every contract's cover. And
nothing can check that a term-start value is the one the point's own history ran on,
because no scenario holds a path before `t = 0`.

The five assumption tables are `RILA_US_S`'s, read in place by `RILA_US_S`'s readers, and
the scenario companion through `RILA_US_S`'s reader too. Beside each reader a `Data` cell
checks the table once and returns its rows, an int, and the one `Projection` cell that
reads the table asks for it before it reads a value: `market_scenario_count`,
`mort_table_count`, `surr_charge_count`, `guar_min_rate_count`, `lapse_table_count` and
`withdrawal_count`. Each reads its table's keys by value, once, as the join matches them,
so that a month written `36.0` is 36, and refuses, naming the file, the column and the
lines at fault: a key that is blank, text or not a whole number, or below its least value;
a key on two rows; a sex other than `M` or `F`; a gap in a sex's ages; a surrender charge
table whose contract years do not run from 0, one row a year, which `RILA_US_S` would read
as no charge in the missing year; and a lapse table whose first year is not 1, under which
the years before it would have no rate. It refuses a value that is blank, text, infinite
or outside its range: a mortality rate below 0, a surrender charge or base surrender rate
outside 0 to 1, a guaranteed minimum rate or a withdrawal below 0, an index level or a
volatility not above 0, a Market Value Rate, risk-free rate or dividend yield not above
−1. A mortality rate above 1 is accepted, and capped. `RILA_US_S` takes the keys as pandas
reads them: one written as text turns its column to text, every lookup on it misses, and
a surrender charge or a withdrawal is then zero without a word, or a lookup raises an
error that names no file.

## The market scenario

`RILA_US_S` keys its market by the month end from issue, `market_scenario.csv`'s
`month_end`, which is the valuation clock of a contract issued at the valuation date and of
no other. Its scenarios step: Scenario A's index is 100 from issue, 120 from month end 36
and 140 from month end 72, Scenario B's 100, 80 and 75. A contract restated in force at
month `d` reads month `d + t` of its path at its own `t`, which one table on the valuation
clock cannot hold for contracts restated at different months.

So `RILA_US_SEC` reads its own, `market_scenario_sec.csv`, through `RILA_US_S`'s reader,
`Data.market_scenario()`, whose Reference `Data.market_scenario_file` names it. It has
`RILA_US_S`'s columns — `scenario_id`, `month_end`, `index_level`, `mvr`, `risk_free`,
`div_yield`, `impl_vol` and `provenance` — and `month_end` is a time in months from the
valuation date. It holds 27 rows:

- `RILA_US_S`'s ten rows as they stand, `up`, `down`, `legacy` and `charge_ex`, for the
  twins, so that a twin reads `RILA_US_S`'s own market;
- for each row restated at month `d`, a copy of its S point's path re-based to that month,
  `{id}-M{d}`: each `month_end` less `d`, the level in force at `d` moved to 0, and the
  levels before it dropped. `up-M71` holds 120 at 0, S's level from month end 36, and 140
  at 1, S's month end 72;
- for each row issued `k` months on, a copy moved `k` months later, `{id}-F{k}`: `up-F13`
  holds Scenario A's three levels at 13, 49 and 85, and none before the issue month.

No row is typed by hand: the file is generated with the table, by the same spec (*The
model points*, below), from `RILA_US_S`'s scenarios as `RILA_US_S`'s reader reads them,
each copied row keeping `RILA_US_S`'s `provenance`, and the tests regenerate it and compare.
`Projection.market_state(t, name)` joins on the model point's `scenario_id` and reads the
state that holds at time `t`, the step search `RILA_US_S`'s; the month's state is the one
at its month end, `t + 1`. A real block shares one scenario on the valuation clock, and
then needs no copies: the shipped table is a set of test cases, each derived row valued on
its own market.

`Data.market_scenario_count()` checks the file as `Data` checks the assumption tables
(above), and `Data` refuses a point whose scenario sets no level by its first month on the
books. A scenario may start after `t = 0`, for business issued later, so the month it must
start by is the point's: a future row's copy holds no level before its issue month, and no
cell reads one there.

## The model points

No row of `model_point_table_sec.csv` or `market_scenario_sec.csv` is typed by hand. Every
one is generated from `RILA_US_S`, its table and its scenarios by `tests/sec_support.py`,
from the `RILA_US_SEC` entry in its `SEC_SPECS`, and the tests regenerate both files and
compare, so an edit to a `RILA_US_S` row reaches them or fails the suite. In the source
repository, `python tools/gen_sec_points.py RILA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–15 | twin | S points 1–15 | issued at `t = 0`: `RILA_US_S`'s fifteen contracts — the worked example's anchor cell on Scenarios A and B, the second with its $8,000 withdrawal at the term midpoint, the behavioural withdrawal rule, Step, Edge and Floor crediting, interim value families (b) and (c), the pre-AG 54 engine, the updated-time-to-expiry amortization, a participation rate above 100% on a 20% buffer, an uncapped option at issue age 81, the cap re-solved at each renewal, an excess withdrawal that bears the charge, and the [S2] withdrawal charge example |
| 16 | derived | S point 1 at S month 71 | the anchor in the last month of its first term: the Term End Date at +40% at `t = 0`, from the row's `I_s` of 100, with 0.850607 contracts in force and an Account Value of 119,890.17 entering the month |
| 17 | derived | S point 2 at S month 36 | Scenario B's anchor on its third anniversary, after the $8,000 withdrawal of the month that closed on it: 84,803.11 before it, 76,803.11 after, 480.31 of the year's 8,480.31 free amount left, and the return-of-premium base at 90,566.38, above the Account Value |
| 18 | derived | S point 13 at S month 80 | the reset point mid-term after its first renewal, at policy month 72: the cap re-solved there, 99.7038%, and its `I_s` of 140 from the row, and 19,019.70 in the Fixed Account from the first term's end |
| 19 | derived | S point 13 at S month 72 | the same contract valued at that renewal: no term-start column, its `I_s` of 140 and its cap re-solved from its scenario at `t = 0` |
| 20 | derived | S point 4 at S month 30 | the Step Rate option on a one-year term, mid-term, with 30,835.04 in the Fixed Account from two term ends |
| 21 | derived | S point 15 at S month 59 | the pre-AG 54 engine in the month that closes on its fifth anniversary, an Account Value of 100,000.00 entering it and 80,000.00 at its end: the [S2] withdrawal charge example at `t = 0` |
| 22 | derived | S point 12 at S month 40 | the uncapped option at issue age 81, mid-term on Scenario B, with its `r_0` of 4.00% from the row against a current Market Value Rate of 5.00% |
| 23 | derived | S point 7 at S month 119 | interim value family (b) in its last covered month, a one-row frame ending on the Maturity Date: 0.332808 contracts in force, its renewal term's `I_s` of 75 from the row |
| 24 | future | S point 1, 13 months on | to be issued at `t = 13`, on its own copy of Scenario A, `up-F13` |

A derived row's `policy_count` is the count `RILA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `RILA_US_S` carries into it, each column read as
`RILA_US_S`'s own formulas read it: the Investment Amount, the two accounts, the Account
Value, the remainder and the return-of-premium base at the close of S month `d − 1`; the
Account Value before withdrawals at the anniversary that opened the contract year of `d`,
S's `av_pp_at(12 × (d // 12) − 1, "BEF_WD")`, or the purchase payment in the first year;
where the term under way began before `d`, S's market at its Term Start Date,
`market_state(term_start_month(d), name)`; and, on a renewal under `nge_reset`, S's
`cap_rate(d)`. So the row continues the S projection from there, in every cell but those
expense inflation moves, to the last bit, or to a few parts in 10^16 where pandas reads a
value of the table back an ulp off. Its `policy_id` is the S row's with the month appended,
`RILA-000001-M71`, and a future row's carries the months to issue, `RILA-000001-F13`. Row
`t` of a generated point is month `t + source_mth` of its S point. All 24 are at
`RILA_US_S`'s issue ages, 60, 75, 80 and 81; the product issues from age 0 [S1] [S2], but
the shipped mortality table starts at attained age 40, so a point issued younger needs it
extended first, and `Data` refuses such a point until it is.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, the
  notes' `l(t)`;
- `"BEF_LAPSE"`, after its deaths;
- `"BEF_TERM_SURR"`, after its background surrenders;
- `"AFT_DECR"`, after the term-end surrender concentration `phi`, the notes' end-of-month
  `l(t+1)`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `RILA_US_S`'s, unchanged
but for their guard outside cover. `"BEF_DECR"` already meant in `RILA_US_S` what it means
in `BasicTerm_SE`, so no name clashes, and `"BEF_NB"` is the one timing running in force
adds. Any other timing raises. `BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a
month before its maturities, is not adopted: the contracts here mature at the end of the
last covered month, as `pols_maturity`, where `RILA_US_S` puts the Maturity Date.

The survivors carried into month `t` are those of month `t − 1`'s `"BEF_DECR"` count, which
`"BEF_NB"` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's deaths, background surrenders and term-end surrenders in the order
`"AFT_DECR"` takes them. So `pols_if_at(t, "AFT_DECR")` is `pols_if_at(t + 1, "BEF_NB")`,
bit for bit, in every month but the last covered one, where the Maturity Date empties the
block, and it is `pols_if(t + 1)` except where month `t + 1` is an issue month, whose new
business joins `pols_if`.

The chain of calls from month `t` back to `t_entry()` is one cell a month, where
`RILA_US_S`'s count ran through two, `pols_if` and `pols_if_at`, and so are the Investment
Amount's, which ran through three, and the two accounts' and the free-withdrawal carry's,
which ran through two; the return-of-premium base's was one already. A cold `net_cf` in
the last month of the anchor's 360-month frame, point 1, runs 378 cells deep, counted as
modelx's stack trace counts it, against 1,095 in `RILA_US_S`: 359 Investment Amounts, one
a month back to month 0, nine cells above them, from the net cash flow down through the
behavioural withdrawal to the opening notional of the last month, and ten below, where
month 0's interim value prices the term's option budget at its Term Start Date's market.
Every committed point runs one cell a month back to `t_entry()` and 13 to 21 more, the
most on point 19, valued at a renewal under `nge_reset`, whose month 0 re-solves the cap
under the option budget; point 24, issued 13 months on, runs as deep as point 1, because
its chains stop at its issue month. At the longest cover the product allows, issue age 0,
1,080 months from issue, on a copy whose mortality is extended below the table's age 40,
it runs 1,098 deep, as new business at the valuation date and issued 120 months on alike.
Each report evaluates its columns in ascending `t`, and a sweep of the committed points
that way, every report and check, runs at most 19 cells deep, on the reset point's twin,
point 13, and on point 19, where the month after a renewal reads, under its surrender
rate, the interim value whose option budget re-solves the cap. `RILA_US_S`'s own sweep runs
as deep on each of its points as this model's on its twin, but for points 4, 5, 12 and 13,
one level less, 18 at most: their deepest stack runs under the count, where this model's
`pols_if` reads `"BEF_DECR"` and it `"BEF_NB"`.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `RILA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `RILA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing Account Value, `av_at(t, "AFT_WD")`, is
weighted by `pols_if_at(t + 1, "BEF_NB")`. Both roll-forward checks scale their tolerance
with `policy_count`, `max(policy_count(), 1)` times `RILA_US_S`'s, since a residual is
rounding on that many contracts, and keep `RILA_US_S`'s `all(...)`, so that a residual that
is not a number fails the check. The term-end identity is per contract and keeps
`RILA_US_S`'s tolerance.

The purchase payment, its premium tax and acquisition fall on `pols_new_biz(t)`, in the
issue month: `t = 0` on the twins, `t = 13` on point 24, and never on a point already in
force, which paid its purchase payment before the valuation date. `RILA_US_S` puts them at
`t = 0` on `pols_if(0)`, the contracts issued, so on a twin they are the same at any count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()` is `RILA_US_S`'s frame from issue: 360 policy months
at issue age 60, 120 at 80 or above. Outside it, before issue and from the Maturity Date
on, every count is zero, and so every cash flow and every value per contract. No count
evaluates a decrement rate there, no table is read at a contract year or an attained age
the contract does not have, and no market path is read: every rate, factor and amount is
0.0 and every flag false, but the two surrender multipliers, `lapse_rate_sc_mult` and
`lapse_iv_mult`, which are 1.0, their neutral value. The market readers, `market_state`
and the five cells of the month's market, are read in cover only: a future row's copy
holds no level before its issue month, and `result_iv()` writes the index level as 0.0
there. The clock's own arithmetic, `duration`, `duration_eom`, `policy_year`, `age` and
the term clock, is defined in every month but means nothing outside cover, and no cell
calls it there; `duration_mth` and `inflation_factor` are defined in every month.

## The opening state

`RILA_US_S` projects new business only, so its frame always opens at issue, from the
purchase payment allocated wholly to the option. Read cell by cell, its recursions carry
the Investment Amount, the Fixed and Holding Accounts, the Account Value's movement, the
Free Withdrawal Amount's carry, the return-of-premium base and the count, and its cells
read the market at each Term Start Date and the Account Value at each anniversary, which a
contract valued in force may have reached before the valuation date. The interim value
has no state of its own: it is the Investment Amount times a factor priced from the
month's market and the term's start. So the opening state is thirteen columns, and the
technical notes' model point attributes and state variables map onto them:

| Notes attribute or state | Column |
|---|---|
| `investment_amount`, `IA_k(t)` | `inv_amt_pp_init` |
| `fixed_account_value`, `holding_account_value`, `FA(t)`, `HA(t)` | `fixed_acct_pp_init`, `holding_acct_pp_init` |
| `AV(t)` | `av_pp_init` |
| `AV_anniv(y)` | `av_pp_prev_anniv_init` |
| `FW_used(y)`, as its complement | `free_wd_remain_init` |
| `rop_base`, `ROP(t)` | `rop_pp_init` |
| `term_start_index`, `I_s` | `index_at_term_start_init` |
| `term_start_mvr`, `r_0` | `mvr_at_term_start_init` |
| the market on the Term Start Date, `(r, q, sigma)` | `risk_free_at_term_start_init`, `div_yield_at_term_start_init`, `impl_vol_at_term_start_init` |
| `declared_cap`, `c`, as re-solved at a renewal | `cap_rate_init` |
| `lock_flag`, `lock_value` | none: no Performance Lock |

The Investment Amount's basis is the Investment Amount itself, the notional the month's
crediting and interim value multiply, after the withdrawals and the roll split before the
valuation month, so no second basis column is needed. The term-start market is carried in
full, not the option budget alone, which straight-line amortization would need: the
`updated_expiry` rule re-prices the term-start portfolio at every month's time to expiry,
and one form serves both rules and every crediting type.

Each column is read where the contract needs it, and only there:

- the Investment Amount, the two accounts and the return-of-premium base at `t_entry()`
  on every row in force, each opening its recursion;
- `free_wd_remain_init` at `t_entry()`, unless the valuation month is the last of its
  contract year, `duration_mth % 12` being 11, where the anniversary resets the allowance:
  on points 16, 21 and 23 it is carried unread;
- the five term-start values wherever the term under way began before the valuation
  month, and `cap_rate_init` wherever that term began at a renewal under `nge_reset`;
- `av_pp_prev_anniv_init` by `free_wd_base(t)` and `free_wd_allow(t)` in the months of
  the year under way before the month that closes on its next anniversary. No cash flow
  reads it: the allowance is read only in a month that closes on an anniversary, whose
  base is then in the frame, so the column holds the base of the year under way, by which
  `proj_len()` bounds the remainder;
- `av_pp_init` by month 0's investment return, `inv_income_pp(0)`, and the block's
  movement, `av_change(0)`, where the two cancel in the Account Value's roll-forward. No
  report reads it either: the Account Value of the month is the Investment Amount priced
  at the month's market plus the two accounts. So `Data` checks it rather than the model
  reading it: against the two accounts and the Investment Amount on a renewal valuation,
  and against the base at the anniversary on an anniversary valuation.

The rows show each, with what it gives when the column is wrong:

- **`index_at_term_start_init`.** Point 16's term began at issue from `I_s` = 100, and its
  row carries it: at `t = 0`, the Term End Date, the index at 140 credits
  `140 / 100 − 1` = 40%, under the cap of 100%, and the interim value is 140,000.00, the
  worked example's. Its copy of Scenario A, re-based to month 71, holds 120 at `t = 0`,
  S's level from month end 36: a term begun before the valuation month cannot read its
  start from the scenario. With the column at 80 the credit would be 75% and the interim
  value 175,000.00.
- **`mvr_at_term_start_init`.** Point 22, mid-term on Scenario B, carries `r_0` = 4.00%,
  against a current rate of 5.00%: its interim value's rate adjustment at `t = 0` is
  `(1.04 / 1.05)^(31/12)` = 0.975582, 31 months being left in the term at the month end,
  and its interim value 78,979.80. With `r_0` at the current 5.00% there would be no
  adjustment, and the interim value would be 81,145.33.
- **`risk_free_at_term_start_init`, `div_yield_at_term_start_init`,
  `impl_vol_at_term_start_init`.** They price the term's option budget, 13.4077% on point
  22, which the straight-line rule amortizes over the term, and with which the cap solve
  and the `updated_expiry` rule price. A volatility of 25% would make it 13.8162% and the
  interim value at `t = 0` 78,818.33; a risk-free rate of 5.00%, 17.2706% and 77,452.64; a
  dividend yield of 3.00%, 8.7345% and 80,827.31.
- **`cap_rate_init`.** Point 18 carries the cap re-solved at its renewal at policy month 72
  from that date's market, 99.7038%, against the declared 100% of its initial term, and
  reads it in every month of its 40-month frame: the next renewal, at policy month 144,
  falls after its Maturity Date. With a cap of 20% the short call at the cap would be
  worth −14,233.12 at `t = 0` rather than −2,688.05, and the interim value 105,653.72
  rather than 106,565.25. Point 19, the same contract valued at that renewal, re-solves
  the cap from its scenario at `t = 0` and reaches `RILA_US_S`'s `cap_rate(72)` and option
  budget, 10.0450%, bit for bit.
- **`inv_amt_pp_init`.** Point 22's 94,119.20 is the purchase payment less the
  proportional reductions of its behavioural withdrawals at policy months 11, 23 and 35.
  The interim value is homogeneous of degree one in it: halved, the Account Value at
  `t = 0` would halve too, from 78,979.80 to 39,489.90, the accounts being empty.
- **`fixed_acct_pp_init`, `holding_acct_pp_init`.** Point 20's Fixed Account holds 30,835.04
  from its two term ends, at policy months 11 and 23, each moving 15% of the credited
  Investment Amount into it, with interest at 3.00% and less the account's share of the
  anniversary withdrawals. Point 18's, 19,019.70, halved would take its Account Value at
  `t = 0` from 125,631.86 to 116,098.56. The Holding Account is 0 on every shipped row,
  its share of the roll split being 0 as shipped.
- **`free_wd_remain_init`.** Point 17 has 480.31 left of the year's 8,480.31: the $8,000 at
  its third anniversary used the rest. So a surrender at the end of `t = 0` is charged 5%
  of its Account Value of 76,889.71 less the 480.31, 3,820.47. Had the year's allowance
  been left whole, it would shelter 8,480.31, and the charge would be 3,420.47. The
  remainder carries through `t = 10`, and at `t = 11`, the month that closes on the fourth
  anniversary, the allowance resets to 7,784.76, 10% of the frame's own Account Value
  there, 77,847.64.
- **`av_pp_prev_anniv_init`.** Point 17's base is its Account Value at the third
  anniversary before the $8,000, 84,803.11: `free_wd_base(t)` and `free_wd_allow(t)` are
  84,803.11 and 8,480.31 for `t = 0` to 10, and `proj_len()` holds the remainder, 480.31,
  to that allowance. At 90,000 they would be 90,000 and 9,000, and nothing else would
  move. On point 16, valued in the last month of contract year 6, the base of every year
  it reads is in the frame, and the column is carried unread.
- **`rop_pp_init`.** Point 17's base is the purchase payment reduced by the $8,000 in
  proportion to the Account Value before it, `100,000 × (1 − 8,000 / 84,803.11)` =
  90,566.38, above its Account Value, so its death benefit at `t = 0` is the base. Had the
  withdrawal been left out of it, the death claims at `t = 0` would be 57.20 rather than
  51.80. Point 22, issued at 81, has no return-of-premium guarantee, and its death benefit
  is the Account Value, 78,979.80, below its base of 94,119.20.
- **`av_pp_init`.** Point 21 enters its valuation month with 100,000.00 and closes it at
  80,000.00, the pre-AG 54 interim value at an accrued rate of −20% on the fifth
  anniversary: the [S2] example then falls at `t = 0`, 8,000 free, 72,000 charged at 3%,
  2,160.00, and a surrender value of 77,840.00, none of which reads the column. Point 22's
  column at 70,000 rather than 78,855.68 would move month 0's investment return from 124.11
  to 8,979.80 and the block's movement with it, and no report and no check.

## Departures from RILA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock, on the valuation clock
or of the opening state, and every recursion begins at `t_entry()`. Where `RILA_US_S`'s
test would have stayed correct on the valuation clock, it moved anyway, so that cover has
one definition. Of `RILA_US_S`'s 156 `Projection` cells, 63 are unchanged, 21 have new text
only and 72 are rewritten; none is renamed or removed, and 36 cells are new, 192 in all.
The 21 are eighteen new docstrings, two docstrings and one code line, `bs_d1`'s, rewrapped
to 92 characters, its syntax unchanged. The `Projection` References are `RILA_US_S`'s
`point_id`, its 28 constants, `data`, `math` and `pd`, every value unchanged. The twin
identity would fail on a cell of `RILA_US_S`'s that this model lacked.

| Cells | `RILA_US_S` | `RILA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration`, `duration_eom`, `is_anniv` | `t`, `t // 12`, `(t + 1) // 12`, `(t + 1) % 12 == 0` | `duration_mth_init() + t`, and the others the same of `duration_mth(t)`; `is_anniv` false outside cover | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × policy_term()`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the Maturity Date, and for a remainder above the year's Free Withdrawal Amount | The frame starts at the valuation date. `maturity_mth()` is new and keeps `RILA_US_S`'s formula; the two rules need `Projection` References |
| `term_elapsed_mth`, `term_start_month`, `tau`, `is_term_end` | arithmetic of `t` | the same of `duration_mth(t)`, `term_start_month` still a policy month; `tau` 0.0 and `is_term_end` false outside cover | Terms align with issue, on the policy clock |
| `market_state` | `market_state(k, name)`, `k` a month from issue, on the scenario `scenario_id()` names | `market_state(t, name)`, `t` a time from the valuation date, on the scenario the model point's `scenario_id` names, after `Data.market_scenario_count()`; `RILA_US_S`'s step search kept | The market is a path in calendar time. The parameter is a time on the valuation clock, so it takes `t`'s name, and every caller passes it by position |
| `index_at_term_start`, `mvr_at_term_start` | `market_state(term_start_month(t), …)`, a policy month passed as a time | the scenario at `term_start_month(t) − duration_mth_init()` where that is `t_entry()` or later; the model point's `*_at_term_start_init` before it | A Term Start Date before the valuation month is a fact of the contract, which no scenario re-based to the valuation date holds |
| `opt_component`, `opt_budget_at_cap` | the Term Start Date's market read from the scenario at `term_start_month(t)` in place | through the new `risk_free_at_term_start`, `div_yield_at_term_start` and `impl_vol_at_term_start`, each read as the index is | The same |
| `cap_rate` | re-solved under `nge_reset` at every renewal | the same at a renewal at or after the valuation month; `cap_rate_init()` for a renewal before it | A cap re-solved before the valuation date is a fact of the contract, which a change to the market or a Reference at the valuation date must not move |
| `index_perf`, `step_rate`, `edge_rate`, `opt_budget_at_cap`, `declared_cap_solved`, `opt_component`, `opt_budget`, `fixed_leg_yield`, `nge_spread_implied`, `credit_rate_at`, `budget_amort_factor`, `mva_factor`, `fixed_proxy_factor`, `deriv_proxy_factor`, `trading_cost_factor`, `cap_calc_factor`, `iv_factor`, `opt_component_pp` | unguarded: no `RILA_US_S` frame has a month outside cover | 0.0 outside cover, before any market or table is read | No market path is read outside cover: a future row's copy holds no level before issue |
| `opt_legs`, `opt_component`, `credit_rate_at`, `budget_amort_factor`, `fixed_proxy_factor`, `deriv_proxy_factor`, `trading_cost_factor`, `cap_calc_factor`, `iv_factor` | branch on the text of `crediting_type()`, `iv_family()` and `amort_rule()` | branch on ten `is_*` cells, one bool for each value `RILA_US_S` tests, decoded from the model point's column; a value `RILA_US_S` does not know raises its message where `RILA_US_S` raises it | No projection cell compares a model point column's text or calls a label accessor, which are left to reporting; Phase 2 moves the decodes into `Data` |
| `inv_amt_basis_pp`, `inv_amt_pp`, `fixed_acct_pp_at`, `fixed_acct_pp`, `holding_acct_pp_at`, `holding_acct_pp`, `rop_pp`, `inv_income_pp` | open at `t = 0` from the purchase payment, or from 0; `inv_amt_pp` through `inv_amt_pp_at` and `inv_amt_basis_pp`, the accounts through their `_at` cells | open at `t_entry()` from the opening state, or from the purchase payment in the issue month, the opening written inline, one cell a month; the arithmetic `RILA_US_S`'s | Every recursion begins on the books, from the opening state |
| `free_wd_avail` | reset where `t` closes on an anniversary; carried as `free_wd_remain(t − 1)`, two cells a month; 0 at `t = 0` | reset on the policy clock; carried as `free_wd_avail(t − 1) − wd_free_pp(t − 1)`, one cell a month, from `free_wd_remain_init()` at `t_entry()` | The contract year is on the policy clock, and the remainder carried into the valuation month is opening state |
| `free_wd_base` | `av_pp_at(12 cy − 1, "BEF_WD")`, a policy month passed as `t` | the same month on the valuation clock, `12 cy − 1 − duration_mth_init()`, or `av_pp_prev_anniv_init()` where it precedes `t_entry()` | On the valuation clock month `12 cy − 1` is not the month that closes the anniversary |
| `wd_scheduled_pp` | the withdrawal table at `(wd_schedule_id(), t + 1)` | `wd_amount_pm(duration_mth(t) + 1)`, the new reader keyed by policy month end | The withdrawal programme stays on the policy clock |
| `mort_rate`, `surr_charge_rate`, `lapse_rate_base`, `guar_min_rate`, `lapse_shock_year` | read their tables in place; `lapse_rate_base` and `lapse_shock_year` take the `max` and the `min` of a list of the table's keys | read through one reader per table, `mort_rate_base_at(x)`, `surr_charge_rate_at(cy)` and `lapse_rate_base_py(y)`, each asking its table's count first, as `guar_min_rate` does in place; loops for the lists | A key the table cannot be read by is refused by name before a value is read, and every table is read through one cell |
| `free_wd_base`, `free_wd_allow`, `wd_pp`, `surr_charge_rate`, `mort_rate`, `lapse_rate_base`, `lapse_rate`, `lapse_rate_sc_mult`, `lapse_iv_mult`, `pols_death`, `pols_lapse`, `pols_lapse_term`, `expenses` | unguarded, but `expenses`, zero where `t < 0` or `t ≥ proj_len()` | zero outside cover, `lapse_rate_sc_mult` and `lapse_iv_mult` 1.0, before any table or rate is read | A contract year or an attained age the contract does not have is never looked up, and nothing is charged or decremented there |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_maturity` | `pols_if(t)` from the column's 1.0 at `t ≤ 0`, through `pols_if_at(t − 1, "AFT_DECR")`, two cells a month; the maturity at `t == proj_len() − 1` | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`, one cell a month, with `"BEF_NB"` added; `pols_if_init()` 0 unless in force; the maturity at `duration_mth(t) == maturity_mth() − 1` | Contracts in force open the count, and new business joins it in its issue month; one definition of cover |
| `premiums`, `prem_to_av_pp`, `prem_to_av`, `expenses` | the purchase payment and acquisition at `t == 0`, the block's on `pols_if(0)` | in the month with `duration_mth(t) == 0`, the block's on `pols_new_biz(t)` | A point in force paid its purchase payment before the valuation date, and one issued later pays it in its issue month |
| `inflation_factor` | `1.025^duration(t)`, stepping on the contract's anniversaries | `1.025^(t // 12)`, stepping every twelve months from the valuation date | Unit costs in valuation-date dollars |
| `check_pols_roll_fwd_resid`, `av_at`, `av_change` | `pols_if(t + 1)`, the next month's count; the block's Account Value opening from 0 at `t = 0` | `pols_if_at(t + 1, "BEF_NB")`; from `av_pp_init() × pols_if_init()` at `t_entry()` | Next month's new business is no part of month `t`'s movement, and a point in force opens with its Account Value |
| `check_av_roll_fwd`, `check_pols_roll_fwd` | `all(...)` over the frame, the tolerance fixed | the same `all(...)`, the tolerance times `max(policy_count(), 1)` | A residual is rounding on that many contracts, and `all` fails a residual that is not a number |
| `result_pols` | `pols_if`, the four movement columns and `pols_if_aft_decr` | `pols_new_biz` after `pols_if` | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `result_iv` | `index_level(t)` in every row | 0.0 outside cover | A future row's copy holds no level before issue |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz` and the thirteen opening-state accessors. Mortality caps as `RILA_US_S`
does, `min(q × mort_ae_factor, 1.0)`, the bound second, so that a missing input stays NaN:
`RILA_US_S`'s cell, guarded, and no departure.

In `Data`, `model_point_table` reads `model_point_table_sec.csv` and checks it, and
`market_scenario` reads `market_scenario_sec.csv`, through the Reference
`market_scenario_file`; `future_horizon_mth` is new. Four readers' docstrings changed,
`market_scenario`'s and `withdrawal_table`'s to name the clock their `month_end` is on, and
`surr_charge_table`'s and `guar_min_rate_table`'s to name the count that checks them; six
count cells are new, one beside each reader of the assumption tables and the scenarios.
`input_dir`, `mort_table` and `lapse_table` are unchanged.

`Data` also refuses, naming the point, what `RILA_US_S` projects without a word: `nge_reset`
written as any text, which `RILA_US_S`'s `bool()` reads as `True`; `nge_reset` off a capped
Cap Rate option, where `RILA_US_S`'s solver prices the wrong portfolio or does nothing; an
issue age or a term that is not a whole number, which `RILA_US_S` truncates; a term of 0, on
which the term clock divides by zero; a blank or text rate that a `max` or a `min` reads;
and assumption tables whose keys or values cannot be read (above). Each is a recorded
departure: `RILA_US_S` projects such a point.

No read goes further ahead than the month after its own: the month's market is read at its
month end, `t + 1`, and the block's closing Account Value and the in-force roll-forward read
the count carried into month `t + 1`.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, and its steps fall
on the valuation date's anniversaries rather than the contract's, so point 16's
`expenses(t)` is `RILA_US_S`'s `expenses(71 + t)` divided by `1.025^6`, or by `1.025^5` at
`t = 0, 12, 24, …`, where the valuation clock has stepped and the contract's anniversary is
a month away. Its other cash flows, its counts and every value per contract are
`RILA_US_S`'s from its month 71 on. Point 24 is `RILA_US_S`'s point 1 thirteen months on in
those columns too, its purchase payment and acquisition included. Its maintenance expense is
1.025 times `RILA_US_S`'s, since the valuation clock stepped at `t = 12`, before the point's
issue, and `1.025^2` times in the last month of each of its contract years, between the
valuation clock's next step and the point's own anniversary.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 15, issued at
  the valuation date, every cell of `RILA_US_S`'s agrees at every argument `RILA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`,
  whose meaning changed. So the goldens `tests/test_registered_index_linked_annuity_us.py`
  asserts on cells that sweep reaches — the notes' interim value table to the cent, the
  option budget and the fixed leg's yield, the term-end identity for every crediting type,
  the pre-AG 54 worked example and the [S2] withdrawal charge example among them — hold
  here with no number restated. The identity holds on any count, since `RILA_US_S` already
  takes the purchase payment and charges acquisition on the contracts issued. The same
  suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The splice**, in `tests/test_registered_index_linked_annuity_us_sec.py`: each
  `RILA_US_S` point restated in force at months either side of its events continues the S
  projection, in its four reports, frame by frame, and in every other cell the two share, at
  every argument S evaluates from that month on, to 1e-9 relative with no absolute floor,
  the roll-forward residuals apart, which are rounding around 0 and keep a floor of 1e-9; it
  skips the cells the twin identity skips, `proj_len`, a frame on the valuation clock, and
  `scenario_id`, which names the row's own copy. The months are those the product's events
  need: either side of each Term End Date and renewal, 11 and 12 and 23 and 24 on a one-year
  term, 35 and 36, 59 and 60, 71 and 72; months mid-term; the anniversaries, with the year's
  base read from the opening state or from the frame; the months around each withdrawal; a
  month after a renewal under `nge_reset`; and the last covered months. So do ten variants
  of S's points, in a copy of S's table that is never committed, for what S's own points do
  not reach: a three-year term; a one-year term under `nge_reset`, re-solving its cap every
  year; a behavioural rate above the free rate, which the allowance binds; a Floor option
  whose cap binds; a crash path, whose interim value falls below 0, and on it a behavioural
  rate above the free rate and a positive request on a negative Account Value; a withdrawal
  above the Account Value, which leaves nothing held; an Edge term ending exactly at its
  buffer, where the Edge rate is credited; and a withdrawal at a negative interim value on a
  positive Account Value, which the accounts alone pay, the option's share floored at 0.
  Each spliced row runs on its own copy of its scenario, re-based to its month, and S's
  paths are replaced in both models by paths that step in every field, the index, the Market
  Value Rate, the risk-free rate, the dividend yield and the volatility, so that a term's
  start read from the current market reads another number; and a row valued mid-term runs on
  a copy whose state at `t = 0`, which month 0, valued at `t = 1`, never reads, is moved off
  the row's term-start columns, so that a term's start read from the scenario at the
  valuation date does too. Inflation, on the valuation clock, is set to 0 in both models;
  the assumptions that ship at zero, the Holding Account's share of the roll split and the
  premium tax, are switched on in both, References that ship equal are set apart, and bounds
  that bind nowhere as shipped are made to bind, so that a term read in the wrong place
  reads another number.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every opening-state column, every kind of
  valuation month and every binding floor, cap, clamp and branch a test lists, and which run
  every line of the model the full grid runs, as measured at M10. The other cases carry the
  `sec_full` marker and show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set.
  One leg of the CI matrix sets it, so every CI run runs the full grid too.
- **Future new business**: issued 13 months after the valuation date, more than a year on,
  seven of S's points and seven of the variants are each the S projection moved on, with
  zeros before issue in every report, its own copy of its scenario, which holds no level
  before issue, and no decrement rate evaluated nor table read before issue; and so are the
  anchor issued a month on and at the horizon, 120 months on.
- **How it computes**: on every row the splice and the future business compare, no cell has
  been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1`, directly
  or through a cell keyed by no month; and no table reader has been reached from a month
  outside cover. On a fresh read of the committed model the policy clock is a closed form,
  every point is swept under a lowered recursion limit, which a recursion backward over the
  frame would exceed, and a cold last-month call runs at most one cell a month back to
  `t_entry()`, plus a fixed overhead, on six of the committed points, two twins, three rows
  in force, point 19, the deepest, among them, and the row issued later, and at issue age 0.
- **Counts, validation and regeneration**: the count rolls forward through new business and
  decrements, and `pols_if_at` refuses a timing it does not have; `result_pols()` is
  `RILA_US_S`'s, column for column, with `pols_new_biz` beside it; multiplying
  `policy_count` by 2.5, a count that is not whole, multiplies every counted cell and moves
  no per-contract value, and at 10^8 contracts both roll-forward checks close on their
  scaled tolerance, each residual above the fixed tolerance it would have had. Each
  malformed row is refused naming its point, by the one rule under test, on a model read for
  it and again through a projection; so is each assumption table whose keys or values cannot
  be read, naming the file and the lines, and each point at or past its Maturity Date or
  carrying a remainder above the year's allowance, by `proj_len()`, each rule refused at the
  first month it reads; an unknown crediting type, interim value family or amortization rule
  is refused where the model first reads it; the edges of each rule are accepted, a renewal
  valuation with every amount carried to the cent and `nge_reset` written 1 or 0, or 1.0 or
  0.0, among them, and so is every state `RILA_US_S` reaches on the splice's inputs,
  restated at its anniversaries, its renewals and its years' last months among others, but a
  contract a full withdrawal has emptied; keys written as floats are read by value; the
  horizon is a Reference, which at 0 refuses any future business, saying so; and the
  committed table and scenarios are what `RILA_US_S` generates, and each derived and future
  row in them, projected at the shipped assumptions, is its `RILA_US_S` point from its month
  on, frame by frame and cell by cell, but for what expense inflation moves.
- **The opening state and the rest**: each derived row's opening state is what `RILA_US_S`
  carries into its month, and each column, changed, moves a committed row where it is read;
  a term begun before the valuation date reads its start from the row, a renewal at the
  valuation date reads its start and its cap from the scenario, and a re-solved cap is read
  until the next renewal; the year under way reads its free-withdrawal state; withdrawals
  stay on the policy clock and the market runs on the valuation clock; expense inflation
  runs on the valuation clock at the shipped 2.5%, which only this test sees, since the
  splice sets the rate to 0; acquisition and the purchase payment fall on new business
  alone; where the cap on mortality binds, both models' annual and monthly rates are the
  float 1.0, the count is 0.0 after, every cell agrees with S, and a NaN A/E factor stays
  NaN; each check fails a residual that is not a number, sent through a Reference set
  before the model computes anything; every guarded cell holds its value outside cover;
  the points of a block sum row by row; an extract without the generator's three columns,
  relabelled, projects the same numbers; `run_sec.py` prints the model's numbers; and the
  docstrings describe the valuation clock.

```bash
python -m pytest tests/test_registered_index_linked_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_registered_index_linked_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k RILA_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-registered_index_linked_annuity-r2
[std]: #uslib-std
<!-- END generated citation links -->
