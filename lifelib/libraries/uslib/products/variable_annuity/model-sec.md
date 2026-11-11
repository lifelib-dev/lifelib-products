# In-Force Implementation Notes

**Status:** Draft, 2026-11-04. `VA_US_SEC` is [`VA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of their contract year, before or after their first
withdrawal and with their account value exhausted or not, and contracts to be written in
the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes. The suffix adds lifelib's letters to `S`: `E` for in force, as
in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`, which is
still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `VA_US_S` on another time axis. It reads `VA_US_S`'s assumption tables in place, every
> assumption unchanged, and its return and rate scenarios are `VA_US_S`'s, moved onto the
> valuation clock. The contractual elements are sourced: the 1.30% base contract asset
> charge, the $35 contract fee and the withdrawal charge scale on Remaining Premium [S2];
> the excess-withdrawal algebra and the GMDB withdrawal adjustment at Contract Year end
> [S1]; the rate-sheet parameters dated 2026-04-27, among them the 1.25% GLWB and 0.90%
> GMDB charges, the 6.00% bonus, the 6.00%/5.00% roll-up, the 105% GWB Adjustment and the
> GAWA% grid [S2] [S3]; the VIX-linked fee reset [S4] [S6] and the CMT-linked roll-up [S7].
> The dynamic lapse, the withdrawal-year factor and the maintenance expense are VM-21's
> [R1]; every other behavioural assumption is a **[std]** standardization, the return path
> is illustrative and the shipped mortality table is *not* a published basis. **Guarantee
> cost cannot be valued deterministically** [R1]: the model verifies the recursion, not the
> value of the guarantees. Replace the assumptions with company data before drawing any
> conclusion from the numbers.

## Run it

```bash
python products/variable_annuity/run_sec.py          # point 1, the anchor issued at t = 0
python products/variable_annuity/run_sec.py 2        # the worked example, in force
python products/variable_annuity/run_sec.py --block  # every point, row by row
```

The first prints point 1, the worked example's anchor cell, issued at the valuation date.
Its row `t = 26` is the worked example's month, the 27th policy month, at whose end the
ninth Contract Quarterly Anniversary falls, and the runner prints it step by step, per
contract: subaccounts of 66,000.00 and 44,000.00 at the beginning of the month, 66,666.82
and 43,796.74 after its growth, the two rider fees, 351.56 on the GWB and 252.81 on the
GMDB Benefit Base, 604.37 in all, and 66,302.07 and 43,557.12 at its end, 109,859.19; a
death benefit of 112,360.00, the Benefit Base, of which 2,500.81 is the guarantee claim;
and a GWB and a Bonus Base of 112,500.00. Its frame has 720 rows, `t = 0 … 719`: its
first withdrawal falls at `t = 120`, the start of contract year 11 at attained age 70, and
its account value runs out at `t = 228`, in contract year 20. The second prints point 2,
the notes' carried state entered as a contract in force 26 months: the same block at
`t = 0`, number for number, on a frame of 694 rows, its first withdrawal at `t = 94` and
its account value exhausted at `t = 202`. Every column of its `result_cf()`,
`result_pols()`, `result_av()` and `result_bases()` agrees with `VA_US_S`'s point 2 but
`expenses`, which are in valuation-date dollars here, 17.34 in the first month where
`VA_US_S` has 17.90, and `net_cf` with them. Three lines to the same thing for point 2:

```python
import modelx as mx
model = mx.read_model("products/variable_annuity/VA_US_SEC")
model.Projection[2].result_cf()
```

`Projection` takes a `point_id`, as in `VA_US_S`. `result_cf()` has `VA_US_S`'s fifteen
columns — `pols_if`, `premiums`, `asset_charges`, `fees_glwb`, `fees_gmdb`, `maint_fees`,
`withdrawals`, `glwb_payments`, `claims_death`, `claims_lapse`, `claims_maturity`,
`expenses`, `commissions`, `premium_taxes` and `net_cf` — with one row per month from the
valuation date, `t = 0 … proj_len() − 1`. `result_av()` has `VA_US_S`'s values per
contract on the same rows, each subaccount, the contract value before the charges, the
three charges collected by unit cancellation, the asset charge and the fund expense, the
contract value and the surrender proceeds, and `result_bases()` the guarantee bases, the
withdrawal, the death benefit and its guarantee claim, and the two moneyness ratios, with
zeros before issue. `result_pols()` sets out the counts behind `result_cf()`: `pols_if`,
`pols_new_biz`, the month's deaths, surrenders and survivors at the end of cover, and
`pols_if_aft_decr`, as in `VA_US_S` with `pols_new_biz` added. `VA_US_S` publishes no
annual report, and nor does this model: the runner sums `result_cf()` into projection
years itself, `t // 12 + 1`.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[point_id]` and a
collection), so the run holds the cells of one point at a time. It freezes everything
alive before each pass, so that each collection scans only what the pass has made since.
It lists the points, each with where it stands at the valuation date and its frame, then
prints the block's first twelve rows and the block summed into projection years 1 to 12.
The runner looks each point up in `Projection` the way the model indexes it, so it runs
unchanged once the model is compiled.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the contract, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of cover, the last month before attained age 120.
- **`duration_mth(t)`, the policy clock**, counts the policy months elapsed at the start
  of month `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()`
  read from the model point's `duration_mth`. The contract runs on it, as in `VA_US_S`:
  the contract year `policy_year(t) = duration_mth(t) // 12 + 1`, the completed years
  `duration(t)`, the attained age `age(t) = age_at_entry() + duration(t)`, the contract
  quarter `contract_quarter(t) = duration_mth(t) // 3 + 1`, and the Contract Anniversaries
  and Contract Quarterly Anniversaries at the end of the months with 11, 23, 35, … and
  2, 5, 8, … policy months elapsed **[std]**. This page names a policy month by that
  count, 0 in the issue month: the notes' "27th policy month" is policy month 26.

`VA_US_S` already counts its `t` from the first month it projects and its policy months
by the same addition, and it enters its point 2 at `t = 0`, 26 months after issue. What it
lacks is a frame with edges: it opens every recursion at `t == 0`, takes the single premium
and charges acquisition there, and guards its cells with `t < 0` and `t ≥ proj_len()`.
Here a contract issued at or after the valuation date is on the books from its issue
month, `t_entry() = max(0, −duration_mth_init())`, where every recursion opens and the
premium falls; a contract in force opens at `t = 0` on the state its row carries; and cover
is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()` is `VA_US_S`'s frame from issue.

The months a formula names for the edges of month `t`'s contract year are months of the
frame, on the valuation clock: `anniv_mth(t) = t + 11 − duration_mth(t) % 12` closes the
year, and `year_open_mth(t) = t − 1 − duration_mth(t) % 12` is the month whose close opened
it. `t_of_month(m) = m − duration_mth_init()` is the month of the frame in which policy
month `m` falls, negative for one before the valuation date: the withdrawal year scans its
months from it, and the VIX-linked fee reads each quarter's VIX-squared average at the
quarter's last month.

Point 2 is the notes' carried state, in force 26 months. At `t = 0` it is in contract
year 3 at attained age 62; its third anniversary falls at the end of `t = 9`,
`anniv_mth(0) = 9`, and the year opened at the close of `t = −3`, before the valuation
date, so the year's opening values come from its row. Point 1 reaches the same month at
`t = 26`, where `anniv_mth(26) = 35` and `year_open_mth(26) = 23`, months of its own
frame. Point 12, the anchor valued at policy month 131, is in the last month of contract
year 11: `anniv_mth(0) = 0`, and the year opened at `t = −12`. Point 23 is the anchor to be
issued 15 months after the valuation date: `duration_mth(0) = −15` and
`policy_year(0) = −1`, it is on the books from `t_entry() = 15`, rows 0 to 14 are zeros,
its premium of 100,000 falls at `t = 15`, and its frame has 735 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the transaction programmes, whose `t` in `transaction_table.csv` is the elapsed policy month; the withdrawal charge scale, by completed years; the GAWA% grid, at the attained age of the first withdrawal; mortality, at the attained age; the base surrender rate and its shock year, by contract year; the start of withdrawals, in the first month of the contract year in which the attained age reaches `wd_start_age`, and of every year after it; the Bonus Period and the GWB Adjustment Date, by contract year, and the roll-up's growth cutoff and the Bonus Period's restart cutoff, by the attained age at the anniversary; the five-yearly fee increase, by completed years; the rider fees at each Contract Quarterly Anniversary, and the contract fee and the seven guarantee events at each Contract Anniversary; the end of cover, at attained age 120 | the gross fund returns, whose `t` in `return_scenario_sec.csv` is a valuation month; the quarterly VIX-squared averages and the 10-year CMT rate, whose `t` in `rate_scenario_sec.csv` is one too; expense inflation, `inflation_factor(t) = 1.025^(valuation_year − 2015 + t // 12)` |

The return and rate scenarios are paths in calendar time, shared by every contract of a
block, so they move to `t`. `VA_US_S` keys them by the elapsed policy month, the `t` of
`return_scenario.csv` and `rate_scenario.csv`, so each of its contracts reads the path from
its own issue. Its `base` path sets returns at policy months 0, 12, 24, 26 and 27,
reverse-engineered so that the anchor's contract value is 104,000.00 and 112,500.00 at
anniversaries 1 and 2, and 110,000.00, split 66,000 and 44,000, entering the 27th policy
month, whose returns are the worked example's +1.20% and −0.30%. Point 1, issued at the
valuation date, reads that month at `t = 26`, and point 2, in force 26 months, at `t = 0`,
so no one path keyed by valuation month reproduces both. So `return_scenario_sec.csv` and
`rate_scenario_sec.csv`, which the generator writes from `VA_US_S`'s scenarios, hold each
of them under its own id, which the points issued at the valuation date read, and, for
every row valued in force or issued later, a copy of its scenario under an id of its own,
named by the months it moves: `base-M26` for point 2, `decline-M144` for point 13,
`variant-M41` for point 17, `base-M40` for points 16 and 20 and so on, and `base-F15` for
point 23; 60 rows of returns and 18 of rates, in seventeen scenarios each. In the copy for
a row valued at policy month `m` the levels `VA_US_S` set before `m` collapse to the one in
force at `m`, at `t = 0`, and the later rows move `m` months earlier, each subaccount's
returns on rows of their own: `base-M26` holds +1.20% and −0.30% at `t = 0`, and 0.50% and
0.20% from `t = 1`. The copy for a row issued `k` months on moves `k` months later and sets
nothing before its issue month. So every row reads each policy month's return and rate at
the valuation month in which that policy month falls, and the model reproduces `VA_US_S`
there. The copies are what reproduce `VA_US_S`'s contracts, each on the path from its own
issue; the contracts of a block valued at one date would read one path, the market as it
moves from the valuation date.

The copy is moved by the row's own `duration_mth`, the policy months elapsed at the
valuation date, not by the S month it was taken from. `VA_US_S` projects its point 2 from
the valuation date, so a row restated from it at S month `d` is in force `26 + d` months:
point 20, `VA_US_S`'s point 2 at its month 14, is in force 40 months and reads `base-M40`,
the copy point 16, `VA_US_S`'s point 5 at its month 40, reads too.

`VA_US_S` reads a month before a contract's issue at its issue month,
`max(duration_mth(t), 0)`, which none of its points reaches. Here no cell reads a scenario
outside cover: `inv_return_mth(t, i)` and `scenario_rate(t, name)` take the last row of the
point's scenario at or before `t`, by an explicit loop, and raise, naming the point, where
there is none, behind `Data`'s refusal of a point whose scenario sets nothing by its first
month on the books. The VIX-squared average of contract quarter `k` is the rate scenario's
level at the valuation month of the quarter's last policy month,
`vix_sq(k) = scenario_rate(t_of_month(3k − 1), "vix_sq")`, read only for quarters on the
books. A past VIX reaches the projection only through the rate of the quarter before the
one under way, the clip's prior, which is the model point's `phi_glwb_init` (below), so no
column holds a level the scenario also sets.

Expense inflation counts the years from the valuation date, `t // 12`, on top of the years
from VM-21's expense base year, 2015, to the valuation year, 2026 [R1], so the maintenance
expense, $100 a contract a year inflating at 2.5%, plus 7 basis points of the account
value, is in valuation-date dollars for every point alike: 10.93 a contract a month at
`t = 0` before the account-value part. `VA_US_S` counts the contract's own completed
years, `duration(t)`, which is `t // 12` on a contract issued at the valuation date and
mixes the two clocks on any other: on point 2 its factor is `1.025^2` higher in the first
ten months of each projection year and `1.025^3` in the last two, where the contract has
passed an anniversary and the projection year has not. Acquisition, 0 as shipped
**[std]**, is charged per contract issued, in the issue month and not inflated, as in
`basiclife/BasicTerm_SE`; `VA_US_S` charges it at `t = 0`, which on its point 2 is a month
in force. The commission and the premium tax, 0 as shipped, fall on every premium as in
`VA_US_S`: the single premium in the issue month and any premium a programme schedules
after it.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`VA_US_S` computes, whatever the point's count: `VA_US_S` already weights its premium by
the contracts in force and charges acquisition at `t = 0`, which on new business is the
issue month. On `VA_US_S`'s eight new-business points every cash flow, every count and
every value per contract agrees, and so does every other cell the two models share, but
those whose meaning changed: `pols_if_init()`, now the count already in force at the
valuation date, 0 for new business; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz`. No cell of `VA_US_S`'s is removed.
`VA_US_S`'s point 2 continues `VA_US_S`'s projection from the valuation date, every count,
cash flow and value per contract `VA_US_S`'s but the maintenance expense, and `net_cf`
with it, so the worked example's goldens hold here on point 1 at `t = 26` and on point 2
at `t = 0`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `VA_US_S`'s columns,
`av_init` apart and nine of them renamed, and twenty-two of its columns are the in-force
interface: `basiclife/BasicTerm_SE`'s two, and twenty that open an in-force contract's
state. Each is a number or a flag, and every amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the contract's age in months: positive in force, in any month of its contract year, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `sa_pp_init_1`, `sa_pp_init_2` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the value of each subaccount, one column for each subaccount a fund set of `fund_table.csv` holds, blank on a point whose set lacks it; their sum is the account value, 0 on a contract whose account value has run out, or the rounding of either sign about 0 that the depletion closed on |
| `gwb_pp_init` | dollars | the start of month 0 | the Guaranteed Withdrawal Balance [S1] |
| `bb_pp_init` | dollars | the start of month 0 | the Bonus Base, on which the bonus is credited [S1] |
| `gawa_pp_init` | dollars a year | the start of month 0 | the Guaranteed Annual Withdrawal Amount, 0 before the GAWA% is locked; on a contract whose account value has run out, what the GLWB pays at each contract year's start |
| `rb_pp_init` | dollars | the start of month 0 | the GMDB Benefit Base |
| `np_pp_init` | dollars | the start of month 0 | the cumulative Net Premiums, the floor under the death benefit that no withdrawal reduces |
| `rp_pp_init` | dollars | the start of month 0 | the Remaining Premium, on which the withdrawal charge is taken [S2] |
| `adj_pp_init` | dollars | the start of month 0 | the GWB Adjustment [S3], 0 once a withdrawal has voided it or its date has passed |
| `gawa_pct_init` | a fraction of the GWB | the start of month 0 | the GAWA% locked at the first withdrawal, or at the attained age at which the account value ran out where that came first [S1] [S3]; 0 before either |
| `bonus_end_init` | a contract year | the start of month 0 | the contract year in which the Bonus Period ends, ten years from issue or from the last step-up that restarted it [S1] |
| `has_wd_init` | a flag, `True` or `False` | the start of month 0 | whether a withdrawal has been taken since issue |
| `sum_wd_pp_ytd_init` | dollars | the start of month 0, in the contract year under way | the gross withdrawals taken in the year so far, the notes' `SumW_y` |
| `free_wd_used_cum_pp_ytd_init` | dollars | likewise | the part of the free-withdrawal allowance those withdrawals used |
| `gmdb_dfd_acc_pp_ytd_init` | dollars | likewise | the GMDB's dollar-for-dollar reduction accrued in the year so far, applied at the year's end [S1] |
| `gmdb_factor_acc_ytd_init` | a factor from 0 to 1 | likewise | the GMDB's proportional factor accrued in the year so far, applied at the year's end, 1 where no withdrawal has gone past the allowance **[std]** |
| `wd_this_year_init` | a flag | likewise | whether the year under way took a withdrawal before month 0 |
| `rb_pp_prev_anniv_init` | dollars | the anniversary on or before the valuation date, the one that opened the contract year under way: the close of policy month `12 × duration(0) − 1` | the GMDB Benefit Base there, the base of the year's dollar-for-dollar allowance [S1] |
| `stepup_base_pp_ytd_init` | dollars | the Contract Quarterly Anniversaries of the year under way before the valuation month | the largest account value at them, on any step-up basis, the history the highest-quarterly step-up base alone reads [S1]; 0 where none has passed |
| `phi_glwb_init` | a rate a year | the last contract quarter to end before the valuation month | on the VIX-linked fee, that quarter's GLWB charge rate, the prior the clip moves the first rate on the books from [S4]; 0 in the first quarter and on the other fee rules |

On a point issued at or after the valuation date every one of the twenty is 0, or `False`,
the factor included: such a contract opens with nothing, and its issue values arrive in its
issue month. On a point valued at a contract year's start, `duration_mth` a positive
multiple of 12, the year to date is empty, three sums of 0 and a factor of 1, the year's
flag `False`, and the Benefit Base at the anniversary is the one entering month 0, the two
instants being one. In the first contract year, `duration_mth` 1 to 11, the year opened at
issue, so the Benefit Base at the anniversary is the issue value, the premium credited at
issue. Before the year's first Contract Quarterly Anniversary, `duration_mth % 12` below 3,
no quarter of the year has ended, and the highest quarterly value is 0. `prev_anniv` is the
anniversary that **opened** the contract year: an extract that fills the column from the
anniversary after the valuation date is a year out.

Each column is read where the contract needs it, and only there:

- `sa_pp_init_1` and `sa_pp_init_2` open the subaccounts' monthly chains, `sa_pp(t, i)`,
  at `t_entry()`, through `Data.fund_values_init()`, and their sum is the account value
  entering month 0, `av_pp_init()`.
- The seven bases, the GAWA% and the Bonus Period's end open their own chains at
  `t_entry()`, and `has_wd_init` opens the withdrawal status, `has_wd_by`, which the
  first-withdrawal test, the GAWA's increase on a later premium, the GWB Adjustment and the
  CMT-linked roll-up's spread read.
- The four `_ytd_init` columns open the year to date where the year under way opened before
  the valuation date: `sum_wd_pp`, which the excess test adds each withdrawal to;
  `free_wd_used_cum_pp` and `free_wd_avail`, the free allowance left for a withdrawal and
  for a surrender; and `gmdb_dfd_acc_pp`, `gmdb_wd_dfd_pp` and `gmdb_factor_acc`, the GMDB's
  adjustment, applied at the year's end.
- `wd_this_year_init` answers for the months of the year under way before `t = 0` in
  `is_wd_year`, which the bonus and the surrender rate's withdrawal-year factor read.
- `rb_pp_prev_anniv_init` is the year's opening Benefit Base where the year opened before
  the valuation date, read by `rb_prior_anniv_pp`, the base of the dollar-for-dollar
  allowance.
- `stepup_base_pp_ytd_init` joins the quarter ends on the books in the step-up base at the
  anniversary closing the year under way, and at no other, on the highest-quarterly basis
  alone.
- `phi_glwb_init` is the prior the clip moves the VIX-linked rate from in the quarter under
  way at the valuation date, read by `phi_glwb_vix`.

Everything else the projection uses is fixed at issue, in `VA_US_S`'s columns, or follows
from the policy clock. The depleted status needs no column: a contract in force enters
month 0 depleted exactly where its opening account value is at or below the threshold
(below).

| `VA_US_S` | `VA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1) | `policy_count` | The count, under `BasicTerm_SE`'s name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth_init`: 0, or 26 on point 2 | `duration_mth` | The policy months elapsed at the valuation date, under `BasicTerm_SE`'s name. `VA_US_S` takes a contract at issue or in force, never one to come; here 0 or less is new business |
| `av_init` | `sa_pp_init_1`, `sa_pp_init_2` | `VA_US_S` splits the account value it enters by the target allocation, `alloc(i) × AV`, which holds at the target only: the subaccounts grow apart (below) |
| `gwb_init`, `bb_init`, `gawa_init`, `rb_init`, `np_init`, `rp_init`, `adj_init` | `gwb_pp_init`, `bb_pp_init`, `gawa_pp_init`, `rb_pp_init`, `np_pp_init`, `rp_pp_init`, `adj_pp_init` | Renamed after the cell each opens |
| `gawa_pct_init`, `bonus_end_init` | `gawa_pct_init`, `bonus_end_init` | Kept |
| — | `has_wd_init` | `VA_US_S` infers a withdrawal from a GAWA% above 0, which a depletion without a withdrawal also locks (below) |
| — | `sum_wd_pp_ytd_init`, `free_wd_used_cum_pp_ytd_init`, `gmdb_dfd_acc_pp_ytd_init`, `gmdb_factor_acc_ytd_init` | `VA_US_S` restarts the year to date at `t = 0`, as though every valuation were a contract year's start |
| — | `wd_this_year_init` | `VA_US_S`'s `is_wd_year` scans the year from `t = 0` only |
| — | `rb_pp_prev_anniv_init` | `VA_US_S` takes the Benefit Base at `t = 0` before the withdrawal, `rb_pp_at(0, "BEF_WD")`, for an anniversary before its frame |
| — | `stepup_base_pp_ytd_init` | `VA_US_S` leaves out every quarter end before `t = 0` |
| — | `phi_glwb_init` | `VA_US_S` recurses the VIX-linked rate from the first contract quarter, through fixings before its frame |

A column measured entering month 0 is the cell it opens with `_init` added, `gwb_pp_init`
for `gwb_pp`; a value of the contract year to date adds `_ytd_init`, since the cells'
names do not say that they restart each year; and a value at the anniversary on or before
the valuation date adds `_prev_anniv_init` instead.

On twins 1 and 3 to 9 the twenty are 0, the state of a contract entering its issue month,
and each takes its issue values in month 0, as its `VA_US_S` row does. Twin 2 is
`VA_US_S`'s point in force, and it carries `VA_US_S`'s columns, with what `VA_US_S`
itself assumes for the columns it has none for: its account value of 110,000.00 split by
the 60/40 allocation, 66,000.00 and 44,000.00, which the notes' carried state holds; no
withdrawal, as its GAWA% of 0 says; an empty year to date; a Benefit Base at the
anniversary of 112,360.00, its entering one, which is `VA_US_S`'s fallback on a month with
no premium; and no quarterly history or VIX prior, `VA_US_S`'s frame holding no month
before its `t = 0`.

The columns carried over are read as `VA_US_S` reads them. For a contract in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `designated_lives`, `tax_status` | codes, as in `VA_US_S`'s table; the last two reported, not modelled | issue |
| `premium` | dollars, the single purchase payment | issue |
| `premium_tax_rate` | a fraction of each premium | issue |
| `fund_set`, `glwb_option`, `cdsc_schedule` | keys into `fund_table.csv`, the subaccounts with their allocation and fund expenses; `gawa_pct_table.csv`, the GAWA% grid; and `cdsc_table.csv`, the withdrawal charge scale | issue: the contract's provisions |
| `glwb_stepup_basis`, `gmdb_option`, `fee_reset_rule`, `rollup_rule` | codes, as in `VA_US_S`'s table | issue: the contract's provisions |
| `wd_start_age`, `wd_intensity` | an attained age, 0 for never; a fraction of the annual limit | assumptions of the base run: when withdrawals begin, and how much of the limit they take |
| `scenario_id`, `txn_id` | keys into the two scenario companions and `transaction_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `VA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, the subaccount values apart, which are checked with the
  fund sets, below;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `age_at_entry`, `wd_start_age` and `bonus_end_init` are whole numbers, 0 or more:
  `VA_US_S` reads each by `int()`, which would truncate a fraction without a word;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,080 months at issue age 40, the youngest the shipped
  mortality table rates. Set to 0, the Reference refuses future new business altogether,
  and says so; a negative horizon is itself refused;
- `has_wd_init` and `wd_this_year_init` are `True` or `False`, read by value, as `True`,
  `False`, `1` or `0`: one cell written as text turns the column to text as pandas reads
  it, so `"True"` and `"False"` are read as the flags they name, and anything else, a blank
  among them, is refused;
- the premium and the withdrawal intensity are each a finite number, zero or more, and the
  premium tax rate a number from 0 to below 1;
- the twelve amounts of the opening state are each a finite number, zero or more, and the
  GAWA%, the GMDB's proportional factor and the VIX prior each a number from 0 to 1;
- a contract not yet in force, `duration_mth` 0 or less, has an opening state of zeros, the
  flags `False` and the factor 0;
- on a contract valued at a contract year's start the year to date is empty, exactly, the
  year's flag is `False`, and the Benefit Base at the anniversary equals the one entering
  month 0, exactly: the two instants are one;
- before the contract year's first quarterly anniversary, `duration_mth % 12` below 3, the
  highest quarterly value is 0;
- the VIX prior is 0 on a contract in force unless it is on the `vix` rule and past its
  first contract quarter, `duration_mth` 3 or more: before then, and off the rule, no
  quarter's rate is the clip's prior;
- in the first contract year the Benefit Base at the anniversary is the issue value, to a
  cent: the premium credited at issue,
  `(premium + the programme's month-0 premium) × (1 − premium_tax_rate)`;
- in force, the Bonus Period's end is a contract year, 1 or more;
- a contract that has withdrawn has no GWB Adjustment, any withdrawal voiding it;
- a GAWA above 0 has a GAWA% above 0, the GAWA being that percentage of a base;
- off a contract year's start, a withdrawal this year is a withdrawal, so the year's flag
  needs `has_wd_init`; withdrawals to date above 0 need the year's flag; the free allowance
  used and the dollar-for-dollar reduction are each part of the withdrawals to date, so
  neither exceeds them by more than a cent; and the proportional factor is below 1 only
  where the year has withdrawals;
- last, each point's keys into the tables it is joined with: its `fund_set` is a set of
  `fund_table.csv`, and each subaccount the set holds has its `sa_pp_init_<i>` column, a
  finite number, zero or more to within 1e-8, and 0 on a contract not yet in force; its
  `scenario_id` is a scenario of `return_scenario_sec.csv` that sets a return for each of
  those subaccounts by the first month the point is on the books, `t = 0` or its issue month
  if later, and, on a point the `vix` fee or the `cmt_linked` roll-up reads it for, one of
  `rate_scenario_sec.csv` that sets its levels by then; its `txn_id` is a programme of
  `transaction_table.csv`; its `glwb_option` is a grid of `gawa_pct_table.csv`, and, in
  force, `has_wd_init` needs a GAWA% above 0 unless that grid gave 0% at an attained age the
  contract reached before the valuation month, since the first withdrawal locks the
  percentage of the age it is taken at, and a GWB and a GAWA% above 0 need a GAWA above 0
  under the same proviso, since the withdrawal or the depletion that locked the percentage
  set the GAWA to it times the GWB, and nothing after takes the GAWA to 0 while a GWB is
  left (`Data.gawa_pct_zero_band` reads the grid at those ages); its `cdsc_schedule` is a
  schedule of `cdsc_table.csv`; and `mort_table.csv` gives a rate at its `sex` and its
  attained age in its first month on the books. So reading the model point table reads every
  assumption table, checked. `VA_US_S` meets a key its table lacks only as it projects: a
  missing fund set, scenario, grid, schedule, sex or age raises Python's own `KeyError`,
  naming no file, and a missing transaction programme schedules nothing, without a word.

The checks run in that order. The rules that hold at a contract year's start and those that
hold off it never apply to the same point, so that a value a year's start fixes is refused
by the rule that fixes it. Amounts of money are compared to a cent, so that an extract may
carry each to the cent, as an administration system holds it: each amount so carried is
within half a cent of its exact value. Two columns that hold one amount at instants that
coincide, at a year's start, are compared exactly. A subaccount value is held to 0 or more
to within 1e-8, not a cent, since a contract that opens depleted has its account released in
month 0 with no flow, and `check_av_roll_fwd`, at 1e-6 a contract, would miss by a cent
below 0 left there: `VA_US_S` runs an account down by scaling each subaccount by one less
the share of the account a charge or a withdrawal takes, so a depletion can close on a
rounding of either sign about 0, of the order of 1e-14, the one amount of the opening state
its arithmetic leaves below 0, the bases being held at 0 or more by its floors. On
`VA_US_S`'s shipped points and inputs every depletion closes on exactly 0. Under the
splice's References with no premium tax its never-withdrawing roll-up closes at policy month
524 on 5.7e-15, and its never-withdrawing return of premium at 659 on −2.3e-14; and under
the shipped References, untaxed too, that return of premium issued at 55 or 56 closes at 752
on −1.1e-13. The generated rows carry `VA_US_S`'s own values, unrounded, such a rounding
among them.

Accepted, because a contract can be in each state: an account value of 0 in force, where
the GLWB pays on and the projection reads the contract as depleted from month 0, or the
rounding about 0 a depletion closed on, above it or below it, which the same test reads as
depleted; a GAWA% above 0 with no withdrawal taken, where the account value ran out first;
free allowance
used and a dollar-for-dollar reduction above what the month allows at the valuation date,
since the allowance is recomputed every month from the earnings and the Remaining Premium;
`has_wd_init` with a GAWA% of 0, or a GWB with no GAWA, where the grid gave 0% at an age
the contract reached, as below a grid's first band; every value at each bound its rule
includes, an allocation, a fund expense, a GAWA%, a withdrawal charge or a mortality rate of
0 or 1, a return or a CMT just above −1, and a premium, a withdrawal intensity or a premium
tax of 0, among them; a `duration_mth`, an age or `bonus_end_init` written as a float, and
a flag written as 1 or 0, or as 1.0 or 0.0, read as the value each holds; and an extract
whose every amount is carried to the cent.

Left to the projection, because each needs a `Projection` Reference, which `Data` cannot
read, and refused by `proj_len()`, naming the point. It refuses a point at or past the end
of cover at the valuation date, `duration_mth ≥ 12 × (120 − age_at_entry)` at the shipped
`omega_age`, and a point issued at or past `omega_age`, whose cover from issue is empty and
which would otherwise project a frame of zeros; on the shipped tables the mortality check
refuses an attained age past 120 first, the table's last. And on a contract in force it
refuses, in this order, an opening state that a rule turning on depletion or on a rate
Reference forbids. A contract in force is depleted exactly where its opening account value
is at or below `av_depletion_threshold`, which the projection derives. So:

- a contract depleted at the valuation date carries an account value of 0, to within 1e-8:
  depletion releases the account in month 0 with no flow, so `check_av_roll_fwd` would miss
  by any more, and `VA_US_S`'s depletions close on roundings of the order of 1e-14;
- a contract that has neither withdrawn nor depleted has no GAWA% locked, the percentage
  locking at the first withdrawal or at depletion, and so no GAWA;
- one depleted without a withdrawal has a GAWA% above 0, the grid's at the age its account
  ran out at, unless its grid gave 0% at an age it reached before the valuation month,
  which `Data.gawa_pct_zero_by_point()` gives `proj_len()`, a vector built in `Data`, so
  that the projection reads no grid at an age before its books;
- on the highest-quarterly basis, one not depleted and three months or more into its
  contract year has a step-up history above the threshold: depletion is absorbing, so every
  quarter end of the year before the valuation month closed above it;
- on the `vix` fee rule, in the second contract quarter, `duration_mth` 3 to 5, the VIX
  prior is the first quarter's rate, `phi_glwb_curr`; and from the third quarter it is at
  most `vix_corridor_hi`, and at least `vix_corridor_lo` where `phi_glwb_curr` is, the
  corridor running upward, since the clip holds every rate after the first at most at the
  corridor's top, and from a first rate at or above its foot, at least at its foot.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it, and `run_sec.py --block` asks every point for its frame before it
projects any, and stops before it prints anything. The rest of the year to date, the
step-up history and the VIX prior are history, which nothing here can check beyond these
rules.

Five of the seven assumption tables are `VA_US_S`'s files, read in place, and the other two
are the generated `return_scenario_sec.csv` and `rate_scenario_sec.csv`. All seven are read
by `VA_US_S`'s readers, and their keys and values are checked as well. Beside each reader a
`Data` cell reads the table's keys by value, once, checks them and the table's values, and
returns the table indexed by the checked keys, and the projection reads the table there and
nowhere else: `mort_rates`, `fund_sets`, `return_scenario_steps`, `rate_scenario_steps`,
`gawa_pct_bands`, `cdsc_scale` and `transactions`. The mortality table's last age, at which
every older age is read, is an int cell, `mort_last_age()`, taken from the same checked
ages. A key written `1.0` is 1, as `VA_US_S`'s lookups match it. A key that is not a whole
number, text and a blank among them, a blank text key, a value that is not a number in its
range, blank, text and infinite values among them, a repeated key, a fund set whose
allocations do not sum to 1, and, where the projection reads every age or year between a
table's first and last, mortality ages or withdrawal charge years that leave a gap are
refused, naming the file and the lines, before a projection reads a value from the table;
for those two the message names each repeated key with its lines and each key or span of
keys missing, every fault in one message. The GAWA% grid is banded, so its ages need not run
one a year, and a scenario may start after `t = 0`, for business issued later, so the month
it must start by is the point's, which the model point table's checks hold. `VA_US_S` takes
the keys as pandas reads them: one written as text turns its whole column to text, so that
every scheduled premium and withdrawal is then zero without a word, and every other lookup
on the column raises Python's own `TypeError`, `KeyError` or `ValueError`, naming no file.
Every value a `min` or a `max` reads is refused blank, as text or infinite, since `min` and
`max` lose a NaN in a later argument without a word.

## The model points

No row of `model_point_table_sec.csv`, `return_scenario_sec.csv` or
`rate_scenario_sec.csv` is typed by hand. Every one is generated from `VA_US_S` and its
inputs by `tests/sec_support.py`, from the `VA_US_SEC` entry in its `SEC_SPECS`, and the
tests regenerate the three files and compare, so an edit to a `VA_US_S` row or scenario
reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py VA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 3 to 9 | twin | S points 1 and 3 to 9 | issued at `t = 0`: the anchor, projected from issue on the reverse-engineered `base` path; a sustained decline to exhaustion, on `decline`; the excess-withdrawal programme, 20,000 at policy month 60 and a further premium of 25,000 at 72; the highest-quarterly step-up basis with the annual-ratchet GMDB; the VIX-linked fee and the CMT-linked roll-up, on `variant`; a contract that never withdraws, on the return-of-premium death benefit with no withdrawal charge and the five-yearly fee increase; another on the Roll-up GMDB, whose account value the rider fees exhaust at `t = 554`; and the return of premium withdrawing from attained age 70 |
| 2 | twin | S point 2, in force at 26 | the notes' carried state at the beginning of the 27th policy month, on `VA_US_S`'s own columns: the worked example's month is its `t = 0`, on `base-M26` |
| 10 | derived | S point 1 at S month 6 | the anchor in its first contract year, the year's opening Benefit Base its issue value, 100,000.00, and two of the year's quarter ends, policy months 2 and 5, behind it |
| 11 | derived | S point 1 at S month 120 | the anchor at the start of contract year 11, attained age 70, taking its first withdrawal at `t = 0`: a GWB of 166,500.00, the Adjustment of 105,000.00 still in force, and subaccounts of 71,849.14 and 36,585.76 |
| 12 | derived | S point 1 at S month 131 | the same contract in that year's last month, after its first withdrawal: 9,573.75 withdrawn this year, all of it inside the GMDB's dollar-for-dollar allowance |
| 13 | derived | S point 3 at S month 144 | the declining point at the start of contract year 13, its account value exhausted, paid its GAWA of 9,200.00 at `t = 0` |
| 14 | derived | S point 4 at S month 60 | the excess programme at the start of contract year 6, taking its withdrawal of 20,000 at `t = 0`, in the 4% charge year |
| 15 | derived | S point 4 at S month 65 | the same contract five months on: 20,000.00 withdrawn this year, 10,262.37 of free allowance used, a dollar-for-dollar reduction of 8,029.35 and a proportional factor of 0.882908; its further premium at `t = 7` |
| 16 | derived | S point 5 at S month 40 | the highest-quarterly point mid-year in contract year 4, its account value at the year's first quarter end, 110,132.46, before the valuation month |
| 17 | derived | S point 6 at S month 41 | the VIX-fee point in the last month of contract quarter 14, the prior quarter's rate of 1.6626% from its row, and the CMT-linked roll-up before any withdrawal |
| 18 | derived | S point 8 at S month 560 | the never-withdrawing Roll-up point after its account value has run out without a withdrawal: `has_wd_init` `False`, with a GAWA% of 6.2% locked at depletion |
| 19 | derived | S point 7 at S month 719 | the never-withdrawing return of premium in its last policy month, at attained age 119: a one-row frame |
| 20 | derived | S point 2 at S month 14 | `VA_US_S`'s point in force restated 14 months on, in force 40 months: its scenario's copy moves by 40, not 14, and is the one point 16 reads, `base-M40` |
| 21 | derived | S point 9 at S month 125 | the withdrawing return of premium five months after its year's withdrawal of 9,744.58, its Benefit Base reduced in proportion to 91,983.20 |
| 22 | derived | S point 7 at S month 100 | the never-withdrawing return of premium before its GWB Adjustment Date, `t = 43`, the Adjustment of 105,000.00 carried |
| 23 | future | S point 1, 15 months on | to be issued at `t = 15` |

A derived row's `policy_count` is the count `VA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `VA_US_S` carries into it, each column read as
`VA_US_S`'s own formulas read it: the subaccount values, a column for each subaccount in the
fund table of the `VA_US_S` the generator reads, so that a fund table given a subaccount
gives the table its column, the seven bases, the GAWA%, the Bonus Period's end and the
withdrawal status at the close of S month `d − 1`; the year to date at that close in the
year under way, and empty at a year's start; whether the year has taken a withdrawal, from
the year's months of S's frame before `d`; the Benefit Base opening the year, S's own
`rb_prior_anniv_pp(d)`; the largest account value at the year's quarter ends before `d`;
and, on the VIX-linked fee, S's rate of the quarter before. So the row continues the S
projection from there: point 10 opens with 0.977100 contracts, point 11 with 0.495831, point
12 with 0.468807, point 13 with 0.527147, point 18 with 6.916464e−05 and point 19 with
2.039028e−13. Its `policy_id` is the S row's with the month appended, `VA-000001-M120`, and
its scenario's id is the S scenario's with the policy months elapsed at the valuation date,
`base-M120`; a future row's carry the months to issue, `VA-000001-F15` and `base-F15`. Row
`t` of a generated point is month `t + source_mth` of its S point. All twenty-three are
contracts on the anchor cell, a male life issued at 60 ANB, single life and non-qualified,
on a $100,000 premium allocated 60/40, as every `VA_US_S` point is, differing only in the
switches the notes make first-class parameters; the shipped mortality table starts at
attained age 40.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
four timings, in processing order:

- `"BEF_NB"`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `"BEF_LAPSE"`, after the month's deaths;
- `"AFT_DECR"`, after its surrenders, the notes' `l(t)`, the count at the end of the
  month.

The first two are `basiclife/BasicTerm_SE`'s, and the other two `VA_US_S`'s, unchanged
but for their guard outside cover. `"BEF_DECR"` already meant in `VA_US_S` what it means in
`BasicTerm_SE`, so no name clashes, and `"BEF_NB"` is the one timing running in force adds.
Any other timing raises. `BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a month
before its maturities, is not adopted: the contracts here leave at the end of the last
covered month, as `pols_maturity`, where `VA_US_S` puts its horizon.

The survivors carried into month `t` are those of month `t − 1`'s `"BEF_DECR"` count, which
`"BEF_NB"` forms itself, as its own value at `t − 1` plus that month's new business, through
the month's deaths and surrenders in the order `"AFT_DECR"` takes them, **death first, then
surrender** **[std]**. So `pols_if_at(t, "AFT_DECR")` is `pols_if_at(t + 1, "BEF_NB")` in
every month but the last covered one, where the survivors leave as `pols_maturity`. Both
decrements are monthly rates converted from the annual ones, `1 − (1 − q)^(1/12)`
**[std]**, so that every anniversary count is the annual grid's.

`pols_if(t)` is `pols_if_at(t, "BEF_DECR")`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `VA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, "BEF_NB")
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `VA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing account value, `av_at(t, "EOM")`, is weighted
by `pols_if_at(t + 1, "BEF_NB")`, the contracts left once the month's decrements have
gone, before the next month's new business, and every other timing of `av_at` by
`pols_if(t)`.

The single premium and acquisition fall in the issue month, the one with
`duration_mth(t) = 0`: `t = 0` on the twins issued at the valuation date, `t = 15` on
point 23, and never on a point already in force, which paid its premium before the
valuation date. The guarantee bases take their issue values from it there, by `VA_US_S`'s
own rules, and the Bonus Period's end opens at `bonus_period_years`. The contract is
flexible-premium, so a premium a programme schedules after issue falls on every contract
then in force, weighted by `pols_if(t)` as every cash flow is: `VA_US_S`'s point 4 pays its
further premium of 25,000 at policy month 72, on twin 4 at `t = 72`, on 0.772986
contracts, 19,324.64 in all, and on point 15 at `t = 7`. In the issue month `pols_if(t)` is
the count issued, so the purchase payment needs no case of its own.

The subaccount and account values are read at five instants of the month, `VA_US_S`'s
`sa_pp_at(t, i, timing)` and `av_pp_at(t, timing)`: `"BEF_PREM"`, the opening balance,
which at `t_entry()` is the model point's `sa_pp_init(i)` and `av_pp_init()`, 0 on new
business; `"BEF_WD"`, after the premium has bought units; `"BEF_INV"`, after the
withdrawal; `"BEF_FEE"`, after the month's growth; and `"EOM"`, after the charges,
`sa_pp(t, i)` and `av_pp(t)`. The guarantee bases, `gwb_pp_at`, `gawa_pp_at` and
`rb_pp_at`, take `"BEF_PREM"`, which opens on the base's `_init` column at `t_entry()`,
`"BEF_WD"` and `"BEF_ANNIV"`; their closing values, after the anniversary events, are
`gwb_pp`, `gawa_pp` and `rb_pp`.

The three checks are loops over the frame. The account value's and the count's scale their
tolerance with `policy_count`, since a residual is rounding on that many contracts: the
References `check_tol_av` and `check_tol_pols`, `VA_US_S`'s 1e-6 and 1e-12 on a point
counting one contract, times `max(policy_count(), 1)`. The charge split, an identity per
contract, keeps `check_tol_charge`, `VA_US_S`'s 1e-8. Each fails at the first month whose
residual is not strictly inside its bound, so a residual that is not a number fails, as it
fails `VA_US_S`'s strict bound. The count's residual and `av_at(t, "EOM")` are 0.0 outside
cover before either reads `t + 1`, so that at `t = proj_len()` nothing reads a month past
the frame; `VA_US_S` guards both only below `t = 0`.

Every chain runs one cell a month back to `t_entry()`: the count, through `"BEF_NB"`; each
subaccount, `sa_pp(t, i)`, with the month's steps written inline, where `VA_US_S`'s ran
through two cells a month, `sa_pp` and `sa_pp_at`; the guarantee bases `gwb_pp`, `bb_pp`,
`gawa_pp`, `rb_pp`, `np_pp`, `rp_pp` and `adj_pp`, the last inline too, where `VA_US_S`'s
read `adj_pp_bef_anniv`; the statuses `has_wd_by`, `depleted_flag`, `gawa_pct_fixed` and
`bonus_end`; the year to date, `sum_wd_pp`, `free_wd_used_cum_pp`, `gmdb_dfd_acc_pp` and
`gmdb_factor_acc`; and the VIX-linked rate, `phi_glwb_vix(k)`, one cell a quarter from the
quarter under way at `t_entry()`. Each reads its previous month first, then the month's
steps, so a cold call walks the chain once. A cold `net_cf` in the last month runs one cell
a month back to `t_entry()` and at most 15 more on the committed points: 734 cells deep on
point 1's 720-month frame, against 1,447 in `VA_US_S`, and 708 on point 2's 694 months,
against 1,395. A chain head called cold alone runs at most 17 more, `bonus_end` and
`gmdb_factor_acc` on twin 4, whose first month opens the withdrawals', the bases' and the
account value's chains beneath them. A cold count alone, `pols_if`, runs up to 20 more than
its months: its first month's surrender rate reads that contract year's withdrawal year at
the anniversary closing it, up to 11 months on (below), which opens the withdrawals' chain
beneath it. At the contract's longest cover from issue, 1,020 months from issue age 35, the
youngest the GLWB is issued at, measured on a mortality table extended below its first age,
40, a cold `net_cf` runs 1,034 deep and a cold `pols_if` 1,040, and a point issued 120
months on runs no deeper, because its chains stop at its issue month. Phase 2 sizes its `t`
cache from that contract issued 120 months on: its frame of 1,140 months and the month after
it, 1,141 in all. Each report evaluates its columns in ascending `t`, and a sweep of the
committed points that way reaches a depth of 569 cells, on point 8, where `VA_US_S`'s sweep
of its point 8 reaches 1,123: the contract never withdraws, its account value runs out at
`t = 554`, and its GAWA, locked there, is first read by the payment that opens contract year
48, at `t = 564`, whose chain then runs back to the books' first month. So the tests sweep
the committed points under a recursion limit of 600, which a recursion backward over the
frame would exceed.

One read reaches ahead of its month, and only one kind. The surrender rate's
withdrawal-year factor, 0.60 in a contract year that takes a withdrawal [R1], is a
property of the year: `lapse_wd_factor(t)` reads `is_wd_year` once, at `anniv_mth(t)`, the
month closing the year, up to 11 months after `t`, the same value as `VA_US_S`'s
`is_wd_year(t)`, which scans the whole year. That anniversary lies inside the frame, since
cover ends at the close of a contract year, and the year's answer there rests on no count,
no decrement and nothing after it, so the read opens no chain past it; `is_wd_year` itself
scans no month after its own, being read at a year's last month only, here and by the bonus
at the anniversary. Called at another month of the year, as Phase 2's full sweep calls every
cell at every month, it answers the same and scans the year's months after it, inside the
frame: a read past `t + 1` that no cell of the model makes. On point 1 the factor is 1.00
to `t = 119` and 0.60 from `t = 120`,
the month of the first withdrawal, to `t = 239`, the close of the contract year in which
its account value runs out, each of those years withdrawing in its first month. Every
other read goes no further than `t + 1`: the block's closing account value, weighted by
the next month's count, and the count's roll-forward, which reads that count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()`, the policy month of attained age `omega_age`, 120:
720 months at issue age 60. Outside it, before issue and from the end of cover on, every
count is zero, and so every cash flow, every balance, every charge and every rate, the
decrement rates included; every flag is `False`; the four factors that multiply a base or a
rate, `gmdb_wd_factor`, `gmdb_factor_acc`, `lapse_dyn_mult` and `lapse_wd_factor`, are 1.0,
no change; `bonus_end` is the int 0; and the phase is `PRE_ISSUE` before issue and
`EXPIRED` from the end of cover. The clocks and `inflation_factor` keep their values. No
count evaluates a decrement rate there, and no table is read at a policy month, a contract
year or an attained age the contract does not have: the surrender charge rate, the
scheduled premium and withdrawal, the GAWA%, mortality, the rider charge rates and the
roll-up rate are 0.0 outside cover before any table or rate is read, and the keyed readers
and the scenario readers are not reached there. `VA_US_S` leaves the moneyness multiplier
and the withdrawal-year factor unguarded: outside its frame the first reads the multiplier
of an empty account's moneyness, and the second scans a year that is not there.

The phase is `VA_US_S`'s text: `ACCUM`, then `DEPLETED` once the account value has run out
with the GLWB alive, and `EXPIRED` from the end of cover, with `PRE_ISSUE` before issue
added. It is a leaf: no cell, report, check or runner reads it, the projection's state
being `depleted_flag`, so it stays text here, and Phase 2 makes it a code.

## The opening state

`VA_US_S` projects its new-business points from issue, on the premium and the issue rules
the notes state, and enters its point 2 at the notes' carried state, opening every
recursion at its `t = 0`. A contract valued in any month of its life needs all twenty state
columns, each what `VA_US_S` carries into that month. Each shows on a committed row:

- **`sa_pp_init_1`** and **`sa_pp_init_2`** open the subaccounts. Point 11, the anchor
  valued at policy month 120, carries 71,849.14 and 36,585.76, 66.3% and 33.7% of its
  account value of 108,434.90: since the worked example's month the first subaccount has
  grown at a gross 0.50% a month and the second at 0.20%. `VA_US_S` enters a contract in
  force with its account value split by the allocation, which here would give 65,060.94 and
  43,373.96. With that split the account value at `t = 11`, the anniversary closing contract
  year 11, is 97,688.70 rather than 97,893.67, and 86,816.22 rather than 87,207.58 a year
  later.
- **`gwb_pp_init`** opens the Guaranteed Withdrawal Balance, of which the first withdrawal
  locks the GAWA. Point 11 carries 166,500.00, ten years of bonuses and a step-up on its
  premium, and takes its first withdrawal at `t = 0`, at attained age 70: 5.75% of the
  GWB, 9,573.75. Carried at its value at anniversary 2, 112,500.00, the withdrawal would
  be 6,468.75, and the GLWB fee at the quarter's end 331.35 rather than 490.39.
- **`bb_pp_init`** is the base the bonus is credited on. Point 20, `VA_US_S`'s point 2
  valued at policy month 40, carries 112,500.00, which the step-up at anniversary 2 set,
  and its bonus at `t = 7`, the anniversary closing contract year 4, is 6% of it,
  6,750.00, taking the GWB to 126,000.00. Carried at the premium, 100,000.00, the bonus
  would be 6,000.00 and the GWB 125,250.00.
- **`gawa_pp_init`** is the GAWA in force, which a contract whose account value has run
  out is paid. Point 13, the declining point valued at the start of contract year 13, is
  paid its 9,200.00 at `t = 0` and at every contract year's start for life: 4,849.76 on
  its 0.527147 contracts at `t = 0`. Carried at 8,000.00, it would be paid 8,000.00 a
  year.
- **`gawa_pct_init`** is the percentage locked at the first withdrawal, at which a later
  premium raises the GAWA. Point 15, the excess programme valued five months after its
  withdrawal at policy month 60, locked 5.55% at attained age 65, and its premium of
  25,000 at `t = 7` raises the GAWA by 5.55% of it, from 6,463.10 to 7,850.60. Carried at
  5.75%, the GAWA would rise to 7,900.60.
- **`rb_pp_init`** opens the GMDB Benefit Base, which is charged quarterly and rolls up at
  each anniversary. Point 2 carries the notes' 112,360.00, on which its GMDB fee at
  `t = 0` is 252.81, and which rolls up 6% at `t = 9` to 119,101.60. Carried at
  100,000.00, the fee would be 225.00 and the roll-up 106,000.00.
- **`np_pp_init`** opens the cumulative Net Premiums, which no withdrawal reduces, a floor
  under the death benefit on the `rollup` and `ratchet` elections [S1]. Point 16, the
  highest-quarterly point on the annual-ratchet GMDB valued at policy month 40, carries
  100,000.00; its withdrawals, from `t = 80`, reduce the ratchet's base in proportion, and
  from `t = 92` the death benefit is the Net Premiums, 100,000.00, against a Benefit Base
  of 92,993.27 and an account value of 91,310.70.
- **`rp_pp_init`** opens the Remaining Premium, on which the withdrawal charge is taken
  [S2]. Point 2 carries 100,000.00: a surrender at `t = 0`, in its third contract year,
  pays the 6.5% charge on the Remaining Premium beyond the free amount, the larger of the
  earnings and 10% of the Remaining Premium, here 10,000.00: 6,490.85. Carried at
  90,000.00, the free amount would be the earnings, 19,859.19, and the charge 5,850.00.
- **`adj_pp_init`** carries the GWB Adjustment, which raises the GWB at the Adjustment
  Date, the later of the anniversary on or after attained age 70 and the 12th, where no
  withdrawal has ever been taken [S1] [S3]. Point 22, the never-withdrawing point valued at
  policy month 100, carries 105,000.00, and its Adjustment Date is `t = 43`, the 12th
  anniversary. There the GWB, 183,211.94 after the year's bonus, is already above it, as
  the bonus of each year without a withdrawal makes it on every shipped point, and the
  Adjustment ends without effect; carried at 205,000.00, it would raise the GWB to
  205,000.00 there.
- **`bonus_end_init`** is the contract year the Bonus Period ends, which a step-up
  restarts [S1]. Point 20 carries 12, the step-up at anniversary 2 having restarted the
  ten-year period, and is credited its bonus at each anniversary without a withdrawal:
  6,750.00 at `t = 19`, the anniversary closing contract year 5. Carried at 4, the bonus
  would stop after contract year 4, and the GWB at `t = 19` would be 126,000.00 rather
  than 132,750.00.
- **`has_wd_init`** opens the withdrawal status. Point 18, the never-withdrawing Roll-up
  point valued at policy month 560, its account value exhausted by the rider fees alone,
  carries `False` with a GAWA% of 6.2%, locked at depletion, where `VA_US_S`'s inference
  would read a withdrawal. The status is read by the first-withdrawal test, the GAWA's
  increase on a later premium, the GWB Adjustment and the CMT-linked roll-up's spread.
  Point 17, the CMT-linked point valued at policy month 41 before any withdrawal, rolls
  its Benefit Base up at `t = 6` by 4.50%, the 3.00% CMT rate plus the 1.50% spread before
  the first withdrawal, from 115,754.65 to 120,963.61. Carried as having withdrawn, its
  Adjustment voided and a GAWA% and a GAWA locked, as `Data` then requires, it would roll
  up at 4.00%, the floor, to 120,384.84. And the status says whether a withdrawal is the
  first, which locks the GAWA% of the age it is taken at: point 11, the anchor at its first
  withdrawal, on a grid that gives 0% from 60 to 64, where a contract may have withdrawn
  with no GAWA% locked, withdraws 5% of its GWB at `t = 0`, the grid's percentage at
  attained age 70, carried as not having withdrawn, and nothing, its GAWA being 0, carried
  as having withdrawn.
- **`sum_wd_pp_ytd_init`**, **`free_wd_used_cum_pp_ytd_init`**,
  **`gmdb_dfd_acc_pp_ytd_init`** and **`gmdb_factor_acc_ytd_init`** carry the contract year
  to date where the year under way opened before the valuation date. Point 15, five months
  after its withdrawal of 20,000 at policy month 60, carries 20,000.00 withdrawn this year,
  10,262.37 of free allowance used, a dollar-for-dollar reduction of 8,029.35, the whole of
  the year's allowance, and a proportional factor of 0.882908 for the excess above it. The
  GMDB's adjustment falls at the year's end, `t = 6`: the Benefit Base, 133,822.56, is
  reduced to `(133,822.56 − 8,029.35) × 0.882908` and rolled up 6%, to 117,727.68. With
  the year to date empty, as `VA_US_S` would restart it at `t = 0`, it would roll up whole,
  to 141,851.91. The free allowance used is netted off a surrender's free amount: a
  surrender at `t = 0` finds none left and pays a charge of 3,604.30, which with the
  allowance used carried at 0 would be 3,243.25. And the withdrawals to date are what the
  excess test adds a later withdrawal to: on point 21, the withdrawing return of premium
  valued five months after its year's withdrawal of 9,744.58, the year's whole limit, a
  further 500.00 the next month, added for a test, is excess, where with the year to date
  carried at 0 it would be inside the limit.
- **`wd_this_year_init`** answers for the months of the year under way before `t = 0`. On
  point 15 it is `True`, the excess withdrawal having fallen at policy month 60, so the
  year's surrender rate takes the withdrawal-year factor, 1.24% a year at `t = 0` rather
  than 2.07%, and the year earns no bonus at its anniversary, `t = 6`. Carried `False`,
  with an empty year to date, as `Data` then requires, the year would be read as one
  without a withdrawal, and its bonus of 6,599.35 would take the GWB to 116,588.55 rather
  than leave it at 109,989.20.
- **`rb_pp_prev_anniv_init`** is the Benefit Base at the anniversary that opened the year
  under way, the base of the year's dollar-for-dollar allowance, `rho × RB` [S1]: on point
  15, 6% of 133,822.56, 8,029.35, which the withdrawal at policy month 60 used whole, as
  the year to date records. In the first contract year it is the issue value: point 10,
  valued at policy month 6, carries the premium, 100,000.00.
- **`stepup_base_pp_ytd_init`** carries the highest-quarterly basis's history of the year
  under way. Point 16 carries 110,132.46, its account value at policy month 38, the year's
  first quarter end, and its step-up base at `t = 7`, the anniversary closing contract
  year 4, is the largest of that and the account values at the quarter ends on the books,
  `t = 1`, 4 and 7: 110,299.01, at `t = 7` itself. The GWB after the year's bonus,
  126,020.93, is above it, and no step-up fires; carried at 130,000.00, the step-up would
  take the GWB to 130,000.00.
- **`phi_glwb_init`** is the rate of the last contract quarter to end before the valuation
  month, on the VIX-linked fee: the prior from which the clip moves each quarter's rate by
  at most 0.40% [S4]. Point 17, valued in the last month of contract quarter 14, carries
  1.6626%, quarter 13's rate, and quarter 14's own, from the quarter's VIX-squared average
  of 602.30, is 1.6626% too, inside the band: its GLWB fee at `t = 0` is 490.46. Carried at
  1.00%, the clip would hold quarter 14 to 1.40% and the fee to 413.00.

The issue values `VA_US_S` computes from the premium stay rules, and move into the issue
month: the premium buys units at the allocation and raises the GWB, the Bonus Base, the Net
Premiums, the Remaining Premium and the Benefit Base, 105% of it the GWB Adjustment, and the
Bonus Period's end opens at `bonus_period_years`, each in the month with
`duration_mth(t) = 0`. The cells that bear the notes' names for the opening values,
`av_pp_init()`, `gwb_pp_init()` and the rest, read the opening state instead, 0 on new
business, as `pols_if_init()` does for the count.

Every recursion opens at `t_entry()` and reads its previous month first: the column there,
`X_init()`, and `X(t − 1)` after it. The year to date opens three ways: empty at a contract
year's start, the month before after `t_entry()`, and the `_ytd_init` column at
`t_entry()` where the year opened before it. The Benefit Base opening the year is read three
ways too: from the frame, `rb_pp(year_open_mth(t))`, where that anniversary is at or after
`t_entry()`; from `rb_pp_prev_anniv_init`, where the year opened before the valuation date
on a contract in force; and by `VA_US_S`'s issue rule, the base after the issue month's
premium, `rb_pp_at(t_entry(), "BEF_WD")`, in the first year of a contract issued at or
after the valuation date. `VA_US_S` takes that last value wherever the anniversary precedes
its frame, which is wrong on a contract in force once a premium has been credited after the
anniversary and before the valuation month. The year's withdrawal flag answers from
`wd_this_year_init` where the year opened before `t_entry()`, and scans the year's months on
the books for the rest. The step-up base takes the quarter ends at or after `t_entry()`
from the frame, and the column at the anniversary closing the year under way at the
valuation date. And the VIX-linked rate's clip takes `phi_glwb_init` as its prior in the
quarter under way at `t_entry()`, so no quarter before it is read.

The depleted status takes no column. `depleted_flag` is absorbing, and from the month after
it is set every subaccount is held at 0, so at each month end the flag is set exactly where
the account value is at or below `av_depletion_threshold`, half a cent **[std]**. So a
contract in force enters month 0 depleted exactly where its opening account value, the sum
of its subaccount values, is at or below the threshold, and new business never does, the
rounding of either sign about 0 that a depletion can close on among them (above): the test
is the threshold's, never 0's, and the rules of `proj_len()` that turn on depletion read the
same test, the first of them holding the account of a contract that opens depleted to 0
within 1e-8. `depleted_open(t)` is that test at `t_entry()` and `depleted_flag(t − 1)` after
it, and every cell that `VA_US_S` writes with `depleted_flag(t − 1)` reads it, `VA_US_S`
reading below `t = 0` in its first month. Points 13 and 18 open depleted. Point 13, valued
at a contract year's start, is paid at `t = 0`, from the GAWA and the GWB its row carries,
where `VA_US_S` reads the month before its frame; point 18, valued mid-year, is first paid
at `t = 4`, the start of contract year 48: 11,160.00, 6.2% of its GWB of 180,000.00.

The withdrawal status is a column, not derived. `VA_US_S` infers it from a GAWA% above 0,
which holds until a contract's account value runs out before its first withdrawal: the
GAWA% locks at depletion too, at the attained age then, while `VA_US_S`'s own frame keeps
`has_wd_by` `False`. Once the account is exhausted no cash flow reads the status, but the
GWB Adjustment, which `result_bases()` reports, does, until its date: a withdrawal voids it,
and a depletion does not. So `has_wd_init` carries `VA_US_S`'s own `has_wd_by` entering the
month, and `Data` ties it to the Adjustment, the year's withdrawal flag and the GAWA%.

## Departures from VA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
issue event keyed on `t == 0` falls in the issue month, and every recursion begins at
`t_entry()`. Where `VA_US_S`'s test would have stayed correct on the valuation clock, it
moved anyway, so that cover has one definition. Of `VA_US_S`'s 200 cells, 74 are
unchanged, 15 have a new docstring only and 111 are rewritten; none is removed, and 31
cells are new, 231 in all.

| Cells | `VA_US_S` | `VA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth_init`, `proj_len`, `maturity_mth`, `t_entry`, `is_active` | `duration_mth_init()` the column of the name, 0 or a month in force; `proj_len() = 12 × policy_term() − duration_mth_init()` | `duration_mth_init()` from `duration_mth`, negative for a contract issued later; `proj_len() = maturity_mth() − duration_mth_init()`, refusing a point at or past the end of cover or with no cover from issue, and on a contract in force an opening state that the depletion threshold, `phi_glwb_curr` or the VIX corridor forbids; `maturity_mth`, `t_entry` and `is_active` new | Every frame starts at the valuation date and knows where the contract's cover starts and ends, and a rule of the opening state that needs a `Projection` Reference runs where its frame is defined |
| `anniv_mth`, `year_open_mth` | — : the year's edges are policy months, `12(y − 1) − 1` and `12(y − 1)`, each converted by `t_of_month` where it is read | new: `t + 11 − duration_mth(t) % 12` and `t − 1 − duration_mth(t) % 12` | The edges of a contract year as months of the frame |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_new_biz`, `policy_count` | `pols_if(t) = pols_if_at(t − 1, "AFT_DECR")`, from `pols_if_init()`, the column's 1, at `t = 0`: two cells a month | `pols_if_at(t, "BEF_DECR")`, from `t_entry()`, one cell a month, with `"BEF_NB"` added; `pols_if_init()` 0 unless in force; `pols_new_biz` and `policy_count` new | Contracts in force at the valuation date open the count; new business joins it in its issue month |
| `sa_pp`, `sa_pp_at`, `av_pp`, `av_pp_at`, `adj_pp` | `sa_pp(t, i)` is `sa_pp_at(t, i, "EOM")`, which reads `sa_pp(t − 1, i)`: two cells a month, from `alloc(i) × av_pp_init()` at `t = 0`; `adj_pp` reads `adj_pp_bef_anniv`, which reads `adj_pp(t − 1)`; the sums over subaccounts generators | each month's steps inline, one cell a month, from `sa_pp_init(i)` and `adj_pp_init()` at `t_entry()`; explicit loops over `sub_ids()` | One cell a month, and the subaccounts as they stand. The values are `VA_US_S`'s bit for bit |
| `av_pp_init`, `sa_pp_init` and the seven bases' `_init` cells | `av_pp_init()` the column `av_init`, which `sa_pp_at` splits by `alloc(i)` at `t = 0`; the bases' columns | `av_pp_init()` the sum of the new `sa_pp_init(i)`, through `Data.fund_values_init()`; the renamed columns | The account value as its subaccounts hold it |
| `has_wd_init` | `gawa_pct_init() > 0` | the column | The inference fails after a depletion without a withdrawal |
| `sum_wd_pp`, `free_wd_avail`, `free_wd_used_cum_pp`, `gmdb_wd_dfd_pp`, `gmdb_dfd_acc_pp`, `gmdb_factor_acc` | restart at `t == 0` as at a contract year's start | three ways: empty at a year's start, the month before after `t_entry()`, the new `_ytd_init` accessors at `t_entry()` | A contract valued mid-year carries its year to date |
| `is_wd_year` | `any` over the year's months from `t = 0` | the new `wd_this_year_init()` for the year's months before `t = 0`, and an explicit loop over its months on the books | The year's withdrawal before the valuation date is history |
| `rb_prior_anniv_pp` | `rb_pp` at the anniversary, or `rb_pp_at(0, "BEF_WD")` where the anniversary precedes the frame | three ways: from the frame at `year_open_mth(t)`, from the new `rb_pp_prev_anniv_init()` in force, by the issue rule on new business | A premium after the anniversary is not part of the year's allowance base |
| `stepup_base_pp` | the largest account value at `t − 3j` for `j = 0 … 3`, `t − 3j ≥ 0`, by a generator | the quarter ends at or after `t_entry()`, by an explicit loop, and the new `stepup_base_pp_ytd_init()` at the anniversary closing the year under way at the valuation date | The year's quarter ends before the valuation month are history |
| `phi_glwb_vix` | recurses from the first contract quarter | the new `phi_glwb_init()` as the clip's prior in the quarter under way at `t_entry()`, the quarter `max(duration_mth_init(), 0) // 3 + 1`, a key the model point fixes, not a clock read | The quarters before the books are history |
| `depleted_open`, `depleted_flag`, `glwb_payment_pp` and every cell that read `depleted_flag(t − 1)` | `depleted_flag(t − 1)`, below `t = 0` in the first month; `glwb_payment_pp` reads `gawa_pp(t − 1)` and `gwb_pp(t − 1)` | the new `depleted_open(t)`, derived from the opening account value at `t_entry()`; `glwb_payment_pp` reads `gawa_pp_init()` and `gwb_pp_init()` there | No month before the books is read, and a contract depleted at a year's start is paid at `t = 0` |
| `premium_pp`, `expenses` | the single premium and acquisition at `t == 0` | in the month with `duration_mth(t) = 0` | A point in force paid its premium before the valuation date, and one issued later pays it in its issue month |
| `pols_maturity` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `inv_return_mth`, `scenario_rate` | `VA_US_S`'s readers' tables at `max(duration_mth(t), 0)`, by a list comprehension | the checked companions at `t`, by an explicit loop, raising where no level is set | The scenarios run on the valuation clock |
| `inflation_factor` | `1.025^(valuation_year − 2015 + duration(t))`, from issue | `1.025^(valuation_year − 2015 + t // 12)` | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_pols_roll_fwd`, `check_charge_split`, their residuals, `av_at` | `all(abs(r) < tol)` over a generator, the tolerance fixed; `pols_if(t + 1)`, guarded below `t = 0` only | loops over `t = 0 … proj_len() − 1` that fail at the first residual not inside the bound, two of the tolerances scaled by `max(policy_count(), 1)`; `pols_if_at(t + 1, "BEF_NB")`; 0.0 outside cover, before `t + 1` is read | A residual is rounding on that many contracts, next month's new business is no part of month `t`'s movement, and no month past the frame is read |
| `stepup_base_pp`, `rb_pp`, `rb_pp_at`, `gmdb_wd_dfd_pp`, `gmdb_wd_excess_pp`, `gmdb_guarantee_pp`, `phi_gmdb`, `phi_glwb`, `rollup_rate` | branch on the text of `stepup_basis()`, `gmdb_option()`, `fee_reset_rule()` and `rollup_rule()` | branch on the ten new `is_*` cells, one bool for each value `VA_US_S` tests, decoded once a point, in `VA_US_S`'s order; a value `VA_US_S` does not know raises `VA_US_S`'s message | No projection cell compares a model point column's text or calls a label accessor, which are left to reporting; Phase 2 moves the decodes into `Data` |
| `sub_ids`, `alloc`, `fund_expense_rate`, `gawa_pct_at_age`, `surr_charge_rate`, `prem_scheduled_pp`, `wd_scheduled_pp`, `mort_rate` | read `VA_US_S`'s readers' tables per call, the GAWA% band by a list comprehension, the schedule's last year by `int()` of the raw keys and the mortality table's last age by a generator | read `Data`'s checked tables, through the new keyed readers `surr_charge_rate_at(k)`, `prem_scheduled_pm(m)`, `wd_scheduled_pm(m)` and `mort_rate_base_at(x)`, and `gawa_pct_at_age(a)` by an explicit loop | A key the table cannot be read by is refused by name before a value is read, and each table is read through cells of its own, one a table but the fund table's three and the programme's two |
| every guarded cell | `t < 0` and `t ≥ proj_len()`, or `t >= 0`; `lapse_dyn_mult`, `lapse_wd_factor`, the bases' chains, mortality and the surrender charge rate unguarded | outside cover 0.0, `False`, 1.0 for the four factors, the int 0 for `bonus_end`, `PRE_ISSUE` or `EXPIRED` for the phase, before any table or rate is read | No month outside cover is the contract's (above) |
| `lapse_wd_factor` | `is_wd_year(t)`, a scan of the year up to 11 months on | `is_wd_year(anniv_mth(t))` | The one read ahead of the month, at the anniversary closing the year (above) |
| `phase` | `EXPIRED` from `proj_len()` | `PRE_ISSUE` before issue too | Nothing is active before issue |
| `result_pols` | five columns | `pols_new_biz` second | The count issued in the issue month |

The 31 new cells all appear above: the clock's five, `maturity_mth`, `t_entry`,
`is_active`, `anniv_mth` and `year_open_mth`; the count's two; the nine opening-state
accessors; `depleted_open`; the ten `is_*` decodes, two of `glwb_stepup_basis`, three of
`gmdb_option`, three of `fee_reset_rule` and two of `rollup_rule`; and the four keyed
readers. The docstring-only changes rewrite the time-axis prose, say which cells are labels
for reporting, called by no projection cell, and that a contract's single premium falls in
its issue month. Three References are new, `check_tol_av`, `check_tol_pols` and
`check_tol_charge`, `VA_US_S`'s three tolerances. In `Data`, `model_point_table` reads
`model_point_table_sec.csv` and checks it, `return_scenario_file` and `rate_scenario_file`
name the two companions, `future_horizon_mth` is new, the two scenario readers'
docstrings name the clock their `t` is on, and eleven cells are new: the seven checked
tables, `fund_values_init`, `mort_last_age`, and `gawa_pct_zero_band` with
`gawa_pct_zero_by_point`, which read the GAWA% grid at the ages a contract in force
reached before the valuation month, for the rules of the locked GAWA%. `VA_US_S`'s seven
readers of the assumption tables are unchanged in code.

Seven joins on text keys stay `VA_US_S`'s, each in the cells that read its table: the fund
set on the model point's `fund_set`, in `sub_ids`, `alloc` and `fund_expense_rate`; the
two scenarios on its `scenario_id`, in `inv_return_mth` and `scenario_rate`; the programme
on its `txn_id`, in `prem_scheduled_pm` and `wd_scheduled_pm`; the GAWA% grid on its
`glwb_option`, in `gawa_pct_at_age`; the withdrawal charge scale on its `cdsc_schedule`, in
`surr_charge_rate_at`; and mortality on its `sex`, in `mort_rate_base_at`. With the timing
and kind strings, which Phase 2 turns into int codes, and the ten decodes, each comparing
its column once, they are the only text a projection cell compares, and the phase, a leaf,
the only text one returns. Phase 2 re-keys the joins, as it turns the decodes into `Data`
vectors. `Data` checks each key before a projection joins on it.

The mortality rate is the table's, read at the attained age and sex, with no factor
applied, as in `VA_US_S`, so no rate past 1 can arise and none is capped, and there is no
cap to depart from; `Data` refuses a rate outside 0 to 1, blank or text. The shipped table
reaches 1.0 at age 120, past every frame: cover ends with attained age 119. The surrender
rate's bound of 1 is `VA_US_S`'s `min(1.0, ...)`, kept in its order.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
and `net_cf_ga` with it. A point in force carries that expense in valuation-date dollars,
so point 2's `expenses(t)` is `VA_US_S`'s with the per-contract term divided by `1.025^2`
in the first ten months of each projection year and by `1.025^3` in the last two. Its
other cash flows, its counts and every value per contract are `VA_US_S`'s from the
valuation date on. Point 23 is `VA_US_S`'s point 1 fifteen months on in those columns too.
Its maintenance expense is inflated from the valuation date rather than from its issue,
the per-contract term `1.025` times `VA_US_S`'s in the first nine months of each contract
year and `1.025^2` times it in the last three, and its acquisition, uninflated in both, is
`VA_US_S`'s. Acquisition, 0 as shipped, would also move on point 2, which `VA_US_S`
charges at its `t = 0`.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 and 3 to 9,
  issued at the valuation date, every cell of `VA_US_S`'s agrees at every argument
  `VA_US_S` evaluates in its own sweep, but for `pols_if_init`, `model_point` and
  `result_pols`, whose meaning changed. So the goldens `tests/test_variable_annuity_us.py`
  asserts on those points hold here with no number restated, and those on point 2 hold
  through the splice (below). The identity holds on any count, since `VA_US_S` already
  weights its premium by the contracts in force and charges acquisition in the issue month
  of its new business. The same suite holds the model to the conventions every `_SEC` model
  meets: every frame starts at `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business
  enters once at its `policy_count`, nothing happens before issue, and the in-force columns
  are present; and to `VA_US_S`'s own fact on the valuation clock, both roll-forward
  residuals inside the model's own tolerances, scaled by the count, at `t = 0`, 60, 120 and
  299 wherever the frame has them.
- **The splice**, in `tests/test_variable_annuity_us_sec.py`: each `VA_US_S` point restated
  in force at a month either side of its events continues the S projection, in `result_cf`
  and `result_pols`, column by column, and in every other cell the two share, to 1e-9
  relative with no absolute floor, but those the twin identity skips and those a restated
  row changes by design: the opening-state cells, which read the row's columns; `proj_len`,
  a frame on the valuation clock; `duration_mth_init`, `is_inforce` and `t_of_month`, which
  read the months in force; `scenario_id`, which names the row's own scenario copy; and
  `policy_id`. The cells whose exact value can be 0 while the computed one is rounding about
  it keep a floor of 1e-9: the roll-forward residuals, and the GWB a contract not for life
  runs down to 0, with the payment a contract on it and its moneyness, where an opening
  state the CSV gives back an ulp off leaves the two models 1e-11 apart. The payments in
  force, a payment a contract times a count that falls to 1e-12 late in a long frame, fall
  to about 1e-8, where that floor would pass an error of several per cent, so they are
  compared with none, in the cell and in `result_cf`'s column, but at the months where both
  models pay less than the floor a contract, the GWB's rounding about 0. `VA_US_S`'s own
  point 2 continues it too, at offset 0, the cells its acquisition at `t = 0` moves compared
  from `t = 1`, and the worked example's goldens hold on it at `t = 0` and on point 1 at
  `t = 26`. The anchor is restated at the starts of contract years 2 and 3, in the Bonus
  Period; at the worked example's month; at policy months 40, 60 and 71; at 119 and 120,
  either side of the start of the year of its first withdrawal, and in that year's middle
  and last months; in the last month of contract year 12, where its GWB Adjustment Date
  falls; and at the month its account value runs out and twice after it, mid-year and at a
  year's start. `VA_US_S`'s point 2 is restated at four of its months, each copy of its
  scenarios moving by `26 + d`, and the other points either side of their own events: the
  decline's depletion, valued in the month it runs out, and the year's start after it, the
  excess withdrawal and the premium after it, valued in the premium's month, the
  highest-quarterly step-up, a quarter's last month on the VIX-linked fee, the Adjustment
  Date where the Adjustment binds, the depletion without a withdrawal, valued in its month,
  and the last policy month. Seventeen variants of S's points, in a copy of S's table that
  is never committed, carry what S's own points do not, each with input rows of their own: a
  programme that pays a premium of 10,000 at policy month 62 and withdraws 12,000 at 66,
  3,000 at 69 and 2,000 at 83, the last month of contract year 7, restated around each, so
  that the year's opening Benefit Base, the year to date and the withdrawal year read ahead
  are compared where they differ from what `VA_US_S` assumes before its frame; a path that
  exhausts a never-withdrawing account at 56, the Adjustment carried to its date; the female
  table; a second fund set and a second GAWA% grid; issue ages 55, restated at a contract
  year's start depleted not for life with its GWB below its GAWA, so that the first payment
  on the books is the GWB its row carries, and 72; a path whose quarter ends swing, so that
  the year's highest quarterly value falls before the valuation month and wins the step-up;
  two never-withdrawing points at issue ages 55 and 56, for the Bonus Period's restart age;
  issue ages 69 and 70, either side of the roll-up rate's split, the first with a premium of
  60,000 at policy month 100, the second on a GAWA% grid of 60%, a path that falls through
  its first contract year and gains 10% a month through its second, and withdrawals that
  take the GWB to its floor of 0 inside the limit and past it and the GAWA to the GWB; a CMT
  that falls mid-year below the year's dollar-for-dollar use; a contract not for life at 59,
  withdrawing 130% of its limit from 62, whose GWB runs down to rounding about 0; the
  never-withdrawing roll-up and return of premium with no premium tax, whose accounts run
  out at policy months 524 and 659 on a rounding of 5.7e-15 and of −2.3e-14, each restated
  the month after, depleted on what is left, the first of which only the threshold, not 0,
  reads as depleted; and the anchor on a fund set of three subaccounts, a third that the
  shipped fund table lacks, whose value column the generator takes from the fund table of
  the S model it reads. Each variant's twin, issued at the valuation date, is compared with
  its S point cell by cell, as a restated row is: on variant 16's, which withdraws in its
  first contract year on the roll-up death benefit, the year's opening Benefit Base comes by
  the issue rule at `t = 0`. 88 cases in all. Inflation, on the valuation clock, is set to 0
  in both models; the acquisition expense, the commission and the premium tax, which ship at
  zero, are switched on in both; and the GWB Adjustment is raised to 200%, at which it binds
  at policy month 143 on points 7 and 8. A second set of References, read into the same pair
  of models in turn, switches what ships idle, each where it binds with an effect: a current
  GLWB charge of 0.7%, so that the VIX-linked rate meets its corridor's floor and the
  step-ups it leaves the account value to make raise the Bonus Base at attained age 81, the
  restart age, which restarts the Bonus Period, at 82, which does not, and later; a GWB cap
  of 151,000, which a premium after issue also meets; and a shock-year surrender rate of
  125%, which the bound of 1 caps: 11 cases. The quarters before a row's books are history
  on the restated row, which reads the last one's rate from its column, so `VA_US_S`'s
  VIX-linked rates of those quarters are not compared.
- **The core grid and the full one.** By default the splice runs 26 of its 88 cases, the
  future business 8 of its 27 and the switched References 6 of their 11, which between
  them reach every branch, every opening-state column, every kind of valuation month and
  every category of input the full grids reach, and a test asserts that they do; line
  coverage of the grids showed the default rows executing every line of `Projection`'s
  formulas that the full grids' rows execute. Line coverage cannot tell `>=` from `>`, so
  each boundary of the step-up base's two reads, the frame's quarter ends and the year's
  column, and of the year-open Benefit Base's has a core row on each side of it, and so
  does each age boundary of the contract: the Bonus Period's restart age and the roll-up
  rate's split. The same test checks every bound by the values it bounds: each side of
  every `min` and `max` in `Projection` wins, the other below it, in some call the sweep or
  the comparison of a core row makes, but ten sides it names idle, each with its reason,
  two `VA_US_SEC`'s own tolerances scaled by a count above 1 and eight that cannot bind by
  a premise the cells hold, and two it names bound elsewhere, each by a test that compares
  its rows with `VA_US_S` and asserts the side wins there: the GWB above the GWB
  Adjustment on its date, at the shipped 105% on the committed rows, and the mortality's
  age clamp, on a table that stops below cover. The other cases carry the `sec_full`
  marker and show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of
  the CI matrix sets it, so every CI run runs the full grid too.
- **Future new business**: S's eight points issued at the valuation date and the seventeen
  variants, each issued a month after it, and the anchor and the VIX-fee point, issued 15
  and 13 months after it, are each the S projection moved on, with zeros before issue in
  every report, every decrement rate the float 0.0 there, and no table read at an age, a
  contract year, a quarter or a policy month the contract does not have; their scenario
  copies set nothing before issue, so a scenario read there would raise. A point issued
  more than a year on reads contract year −1 before issue, which is what shows a missing
  guard.
- **How it computes**: on every row the splice and the future business compare, under both
  sets of References, after every report, no cell has been called at a negative month, none
  evaluated from `t_entry()` on has read a month before it, and none evaluated at month `t`
  has read a month later than `t + 1`, directly or through a cell keyed by a year, an age, a
  quarter or a policy month, but the withdrawal-year factor's reads at `anniv_mth(t)`, each
  admitted by reader, cell and month, inside the frame, with what it reads walked for a
  count, a decrement or a later month; and no table is read at an age, a year, a quarter or
  a policy month before the books. On a fresh read of the committed model `duration_mth`,
  `anniv_mth` and `year_open_mth` are closed forms, and every point is swept under a
  recursion limit lowered to 600, which a recursion backward over the frame would exceed
  on every committed frame but nine short ones. And a cold last-month call runs one cell a
  month back to `t_entry()` and at most 20 more, the count alone at most 11 more again, on
  the committed points and at the longest cover, 1,020 months from issue age 35, at the
  valuation date and 120 months on.
- **Counts, validation and regeneration**: the roll-forward closes, `"AFT_DECR"` is the next
  month's `"BEF_NB"`, and `pols_if_at` refuses a timing it does not have; `result_pols()` is
  `VA_US_S`'s, column for column, with `pols_new_biz` beside it; scaling `policy_count` by
  2.5 on seven committed rows, with the zero-shipped assumptions switched on and the premium
  tax charged, scales every cash flow and every counted cell and moves no per-contract
  value, and at a million contracts on three rows the roll-forward checks close on their
  scaled tolerance, where the fixed one would fail; each of 118 malformed model point tables
  is refused naming its column or its point, by the one check it is built for, as the table
  is read and through a projection, a key that the table it joins lacks among them, a GWB
  with its GAWA zeroed where the GAWA% is locked, a subaccount value just past a cent below
  0, and a withdrawal status with no GAWA% locked at each end of the ages its grid is read
  at, issued at the shipped grid's first age and, on a grid paying 0% from 60, issued at 59
  and valued at 12 months, its month before the valuation month still at 59; each of 61
  assumption tables and companions whose keys or values cannot be read, a key written as
  text in each, is refused naming the file and the lines, by `Data` and by a projection that
  reads it; every refusal of `Data`'s eight checking cells, entry by entry, 138 entries, is
  the first refusal of some case; a step-up basis, a GMDB election, a fee rule and a roll-up
  rule that no decode knows each raise `VA_US_S`'s own message, in both models; a scenario
  that sets nothing by the first month a point on it is on the books is refused for that
  point; keys and integer columns written as floats are read by value, and the two flags
  written as 1 and 0, or as 1.0 and 0.0, as the flags they hold; the horizon is a Reference,
  which refuses a point issued past it, at 0 any future business, saying so, and below 0
  itself; a point issued at the age cover ends, or valued at the end of cover, is refused by
  `proj_len()`, while one issued a year before that age, or valued in its last covered
  month, projects, and `run_sec.py --block` refuses such a point before printing anything;
  so is each opening state a rule needing a `Projection` Reference forbids: a GAWA% locked
  with neither a withdrawal nor depletion, on an account value of 0.6 cents, just above the
  depletion threshold, too, none on a contract depleted without a withdrawal, no step-up
  history three and eleven months into the year, and one at the threshold itself, a VIX
  prior other than `phi_glwb_curr` in the second quarter's first month and its last, and one
  outside the corridor from the third, while the months either side of each window, two
  months into the year and the next year's first with no history, and the first quarter's
  last month with no prior and the third's first with a prior other than `phi_glwb_curr`,
  project; the edges of the interface are accepted: the first contract year at both ends and
  the second year's first month, amounts a part of a cent inside their tolerance, the
  step-up history and the VIX prior from their first months, the history just above the
  depletion threshold, the VIX prior at both ends of the corridor, a withdrawal status with
  no GAWA% locked where the grid gave 0%, below its first band or in a band at 0%, at both
  ends of the ages the grid is read at, issued a year below the shipped grid's first age
  and, on the grid paying 0% from 60, issued at 59 and valued at 13 months, its month before
  the valuation month its first at 60, a contract depleted without one there, and a GWB and
  a GAWA% above 0 with no GAWA there; an opening account value of exactly the depletion
  threshold, and of part of it, each read as depleted; a depleted contract marked as one
  that withdrew, a count of 0, and a rate scenario that no point reads left out; and, on a
  first quarter's rate of 0.1%, below the corridor's foot, a VIX prior below the foot in the
  third quarter, which the clip gives there; each value column holds the bounds of its
  range, an allocation, a fund expense, a GAWA%, a withdrawal charge and a mortality rate of
  0 and 1, a return and a CMT just above −1, a VIX average, a premium, a withdrawal
  intensity and a premium tax of 0, a locked GAWA% of 1 and a year's proportional factor of
  0, a subaccount value a cent below 0 on a depleted contract, and, on a first quarter's
  rate of 100%, a VIX prior of 1; the committed table with every amount of its opening state
  rounded to the cent, as an extract carries it, reads, and each point passes `proj_len()`
  and enters its first month depleted exactly where it did; a mortality table stopped at 110
  and a charge schedule stopped at three years on 5.5% are read past their ends as `VA_US_S`
  reads them; and the committed tables are what `VA_US_S` generates, their text `VA_US_S`'s
  or composed from its keys.
- **The opening state and the rest**: each derived row's opening state is what `VA_US_S`
  carries into its month, and at the shipped assumptions each row in force, point 2 among
  them, is S's from that month on, in every cell but those expense inflation moves;
  `policy_count` and each of the twenty state columns, changed on a copy of a committed row
  that reads it, against a baseline that differs from it in that column alone, changes what
  the row reports, and three controls change nothing; the year under way reads its opening
  state; depletion is derived from the opening account value, and point 18 carries
  `has_wd_init` `False` with a GAWA% locked; the scenarios run on the valuation clock and
  the programmes on the policy clock; expense inflation runs on the valuation clock at the
  shipped 2.5%, which only this test sees, since the splice sets the rate to 0; the single
  premium and acquisition fall in the issue month alone, per contract issued, never on a row
  in force, and the commission and the premium tax on each premium as it is paid; the
  surrender rate reads the withdrawal year at its anniversary; a depleted row projects its
  whole frame at a zero account value; a NaN mortality rate reaches the count and its
  residual as NaN, and a NaN asset charge the account value's and the charge split's
  residuals, and each check whose residual is not a number fails; each keyed reader returns
  `VA_US_S`'s own lookup at every key the contract can ask for; every guarded cell holds its
  value outside cover and reads no rate there; the points of a block sum row by row; an
  extract without the generator's three columns, labelled apart from its positions, projects
  the same numbers, and `run_sec.py` finds its points by label; the docstrings describe the
  valuation clock, the symbol map names every cell running in force adds and no row of it
  leaves a column blank, no row of a docstring's table runs into a column gap, and, where
  docutils is installed, every docstring parses without a warning; the model reads
  `VA_US_S`'s tables in place, but for its model point table and its two scenario
  companions, and every Reference of either Space is `VA_US_S`'s but the four it adds; each
  Reference a rewritten cell reads that ships equal to another, the M&E charge and the CMT
  spread, the charge years' surrender rate and the CMT floor, the bonus and the younger
  roll-up rate, the VIX formula's offset and the Bonus Period, and the GWB Adjustment's age
  and the roll-up rate's split, is read as itself: with each pair set apart, the twins of
  `VA_US_S`'s points are `VA_US_S`'s in every cell; and `run_sec.py` prints the model's
  numbers, for the anchor issued at the valuation date, the worked example in force, a
  depleted point and a point issued later, and the block, writes "1 month" for a point a
  month either side of the valuation date, and refuses a label the table lacks, a number or
  not, naming the labels it has.

```bash
python -m pytest tests/test_variable_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_variable_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k VA_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[std]: #uslib-std
<!-- END generated citation links -->
