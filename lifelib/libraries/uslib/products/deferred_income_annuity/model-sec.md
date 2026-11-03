# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `DIA_US_SEC` is [`DIA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already in
force there, in their deferral or in their income phase, and contracts to be issued in the
ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
The product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models, and its income phase is the payout
chassis that [`SPIA_US_SEC`](../immediate_annuity/model-sec.md) runs in force; this page
says what running in force changes. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`,
which is still to come.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `DIA_US_S` on another time axis, and it reads `DIA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements — the paid-up income slice each
> premium buys at then-current rates, the 100% return-of-premium deferral death benefit,
> the one-time ±5-year income start date adjustment, six months of payment acceleration,
> commutation with the life-contingent tail preserved, the QLAC restriction set and its
> $210,000 2026 premium limit, the $50 maintenance expense escalated at 2.5%, and the
> absence of any lapse or annuitization decrement — are sourced. **The entire pricing
> kernel is not.** No purchase-rate table exists: the Insurance Compact expressly relieves
> the insurer of disclosing the deferral-period mortality and interest basis
> [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13), so the 4.75% pricing rate,
> the 6.0% expense and profit load, the mortality table, the illustrative payout and
> return-of-premium factors, the 100 bp repricing spread and the 50 bp commutation margin
> are all **[std]** constructions. Replace them with company data before drawing any
> conclusion from the numbers.

## Run it

```bash
python products/deferred_income_annuity/run_sec.py            # point 1: the anchor cell
python products/deferred_income_annuity/run_sec.py 19         # the anchor, in payout
python products/deferred_income_annuity/run_sec.py --block    # every model point, summed
```

The first prints what `run.py` prints for `DIA_US_S`'s point 1, the worked example's anchor
cell, issued here at the valuation date: its terms, its frame, its pricing factors and its
income, the technical notes' annual display grid for policy years 1 to 25 and the monthly
cash flows around the income start date, every number the same, with the first fifteen rows
of `result_cf()` and `result_pols()` between them. The second prints the same cell in force
241 months, a month into its income phase, its cash refund running. At `t = 0` it pays what
`DIA_US_S` pays in its month 241: the instalment of 3,688.30 weighted by survival, 2,615.39,
and refund claims of 430.52 on a refund balance of 150,000 − 3,688.30 = 146,311.70. Its
expenses are in valuation-date dollars, 2.97 at `t = 0` where `DIA_US_S`'s month 241 carries
4.86, twenty years' inflation more, and `liability_cf` and `net_cf` move with them. Its
annual grid opens at policy year 21, the one the valuation date falls in, whose row holds
that year's months from the valuation date on: refund claims of 4,059.21 over policy months
241 to 251, where `DIA_US_S`'s policy year 21 holds 4,502.42 over its twelve. Three lines to
the same thing for point 19:

```python
import modelx as mx
model = mx.read_model("products/deferred_income_annuity/DIA_US_SEC")
model.Projection[19].result_cf()
```

`Projection` takes a `point_id`, as in `DIA_US_S`. `result_cf()` has `DIA_US_S`'s eight
columns — `pols_if`, `premiums`, `annuity_payments`, `claims`, `commutations`, `expenses`,
and the net stream under both signs, `liability_cf` and `net_cf` — with one row per month
from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out what lies behind
it on the same rows: `pols_if` and `pols_new_biz`, the contracts issued in the month, then
`DIA_US_S`'s survival and payment-factor columns in `DIA_US_S`'s order, the survival read
at the start of each month, and every column 0 before a point is issued. `result_annual()`
is the notes' annual display grid, keyed by the policy year as in `DIA_US_S`, from the
policy year the valuation date falls in.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once read (`del model.Projection[point_id]`, then a collection), so
the run holds the cells of one point at a time. It freezes what is alive once the model and
its table are read (`gc.freeze()`), and again before the projections, so that each
collection scans only what the run has made since. It prints a line per point on where it
stands at the valuation date, then the block's first fifteen rows and the block summed into
projection years, `t // 12 + 1`. The shipped table is a set of test cases standing at
different calendar dates (*Two clocks*, below), so the block shows how the frames add, and
nothing more.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however long the contract has been in force,
  month `t` runs from time `t` to time `t + 1`, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the stop rule. The projection's survival is indexed by a **time point** on this
  clock: `lives_if(t, life)` and `lives_if_last(t)` are survival *at* time `t`, the start
  of month `t`, so the deaths of month `t` are `lives_if(t, life) − lives_if(t + 1, life)`
  and an arrears instalment is paid on survival to time `t + 1`, as in `DIA_US_S`.
- **`duration_mth(t)`, the policy clock**, counts the months elapsed from issue at the
  start of month `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is the technical notes' month index,
  and the contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, `age(t, life) = age_at_entry(life) + duration(t)`
  and `calendar_year(t) = issue_year() + duration(t)`, as in `DIA_US_S`, and through them
  the premium months, the income start month `T`, the three option months, the payment
  months, the COLA anniversaries and the certain period. `T`, the premium months and the
  option months stay policy months, compared with `duration_mth(t)`: converted to `t` they
  would collide with the `−1` the option accessors return for "never", and turn negative on
  a contract past them. A cell keyed on this clock takes `k`, a policy month or the time
  point that opens it, or `y`, a policy year: `premium_pm(k)`, the premium of a policy
  month; `lives_if_pm(k, life)`, the pricing kernel's survival from issue; the pricing
  cells, keyed by the premium's or the exercise's month; and `mort_rate_py(y, life)`, the
  annual mortality rate of a policy year. The two table readers,
  `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)`, take an attained age,
  `x`. `BasicTerm_SE` reaches the policy clock by adding one a month, a recursion as long
  as the frame; the closed form needs no such chain of calls.

The months from the income start month, the payout phase's own count, are the policy clock
less `T`, and no cell is keyed by them. `is_payment_pm(k)`, `cola_factor_pm(k)`,
`annuity_pp_sched_pm(k)` and `certain_floor_pm(k)` take a policy month and form `k − T`
inside, so that the payment schedule, the COLA, the certain floor, the premiums and the
options share one key, and `cum_annuity_pp(k)`, the notes' `G(k)`, the instalments
scheduled through the end of policy month `k`, keeps `DIA_US_S`'s key. A key counted from
`T` would be negative throughout the deferral.

The **stop rule** ends every frame where it ends `DIA_US_S`'s. `stop_mth()` is
`DIA_US_S`'s frame length from issue, `max(horizon_mths(), T + certain_mths_eff())`: the
month the youngest covered life attains the limiting age, 120, or the end of the guarantee
period if that is later. A month is in the contract's frame when
`0 ≤ duration_mth(t) < stop_mth()`, which is `is_active(t)`, and the frame ends with the
last such month, `proj_len() = stop_mth() − duration_mth_init()`. A contract's own end, its
last death or the end of its guarantee, is a probability or a floor reaching zero inside the
frame, which runs on with zeros, as `DIA_US_S`'s does.

Point 19 is the worked example's anchor cell in force 241 months. At `t = 0` it is in
policy year 21, at attained age 80, a month after its income start month, policy month 240;
its next anniversary, policy month 252, falls at `t = 11`, and its frame has 479 rows,
`t = 0 … 478`, to the anchor's last month, policy month 719. Point 18 is the
payment-acceleration contract in force 59 months, in its deferral: its second premium falls
at policy month 60, `t = 1`, its income starts at policy month 240, `t = 181`, and it
accelerates its payments at policy month 252, `t = 193`. Point 26 is the joint contract
issued 13 months after the valuation date: `duration_mth(0) = −13`, it is on the books from
`t_entry() = 13`, rows 0 to 12 are zeros, `policy_year(0)` is −1, its premiums fall at
`t = 13` and `t = 73`, and its frame has 733 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium months and the premiums still due, the income start month and its adjustment, the pricing survival from issue and every purchase rate, payout factor and return-of-premium factor priced on it, the payment months and the instalment schedule, the COLA anniversaries, the certain period and an installment refund's derived period, the instalments scheduled to date that a refund nets, the acceleration and its blackout, the commutation month and the guaranteed months it commutes, the attained ages that key the mortality table, the improvement scale and the two factor tables, the calendar year that dates the improvement, the age stop rule | expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

Expense inflation alone runs on `t`. `DIA_US_S`'s annual steps,
`(1 + g)^(policy_year(t) − 1)`, keep their shape and move onto the valuation clock, so the
maintenance charge is in valuation-date dollars for every point alike and steps on each
anniversary of the valuation date. The commutation discount rate reads neither clock: it
moves with the reference rate's change since issue, on one path of the reference rate that
every point shares. For a contract on the books at the valuation date that is the change to
the valuation date, an opening-state column, plus `ref_rate_shift`, a change made at the
valuation date; a contract issued later, after it, has seen none (*The opening state*,
below). The repricing of a start-date adjustment reads `baa_yield`, a level that reads
neither clock either. There is no acquisition cost in either model.

**Mortality improvement stays on the policy clock**, because it is already dated by the
calendar. Its exponent is the calendar year less `mort_table_year`, and the calendar year,
`issue_year() + duration(t)`, is the one the contract reaches, whatever the valuation date.
So a contract in force reads the improvement of its own calendar years, and nothing is
re-based: restated from `DIA_US_S` at month `d`, its month `t` is `DIA_US_S`'s month
`d + t` and the same calendar year, and point 16, the generational point, restated at month
240 reads `DIA_US_S`'s `mort_rate(240 + t, life)` exactly. Moving it onto the valuation
clock would need a calendar valuation date, which the model point table does not carry, and
would step a generational basis on the valuation date's anniversaries rather than the
contract's.

That has a consequence for the shipped table. Every row keeps the issue year of the
`DIA_US_S` point it was taken from, 2026, so the rows are test cases standing at different
calendar dates at their common `t = 0`: the twins at issue, point 19 241 months later,
point 26 thirteen months earlier. A real block carries each contract's actual issue year,
and its points then share one valuation date.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`DIA_US_S` computes, whatever the point's count: neither model charges acquisition, and
every cash flow is the count times an amount per contract. On `DIA_US_S`'s seventeen points
every cash flow and every count agrees, and so does every other cell the two models share
but three whose meaning changed: `pols_if_init()`, now the count already in force at the
valuation date, 0 for such a point; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz` and sets `pols_if` first.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `DIA_US_S`'s columns, and
ten of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and eight
that open a contract's state. Every amount is per contract. The premiums still due are in a
second file, `premium_schedule_sec.csv` (*The premium schedule*, below).

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a contract in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts the point stands for: in force at the valuation date, or issued at or after it. A count of contracts on the books, never weighted by survival |
| `duration_mth` | whole months | the valuation date | the months elapsed from issue: positive in force, in the deferral or the income phase, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `lives_if_init_1` | a probability, 0 to 1 | for a contract in force, the valuation date, the start of month 0, before any month-0 death; for any other, issue, where each covered life is 1 | the primary annuitant's survival: 1 or 0 on a real record |
| `lives_if_init_2` | a probability, 0 to 1 | the same | the joint annuitant's survival; 0 on a single-life contract |
| `cum_premium_pp_init` | dollars per contract | the start of month 0, before the premium, if any, received at its start | `CP`, the premiums paid before the valuation date, without interest: the base of the deferral death benefit and, with the premiums still due, of the refund |
| `annual_income_init` | dollars a year per contract, before COLA | the start of month 0, before the slice, if any, bought at its start | `B`, the guaranteed annual income the premiums paid have bought, a start-date adjustment exercised before the valuation date included; past the income start month, the income of every instalment |
| `guarantee_mths_pricing_init` | months, not necessarily whole; blank where not read | fixed by the whole premium schedule, the slices bought and those still due | on a cash or installment refund in force, `n_g` as the pricing kernel takes it, equation (5)'s fixed point, with which every slice still due and a start-date adjustment still to come are priced; blank on every other point |
| `surv_to_payout_init` | a probability above 0, at most 1; blank where not read | from issue to the income start month in force, `T` | on a contract valued after `T`, `l_last(T)`, the cohort that reached the income phase, which weights every guaranteed instalment: 1 on a real record in payout; blank on every other point |
| `commute_weight_init` | a probability above 0, at most 1; blank where not read | from issue to the commutation month, `t_c` | on a contract valued after `t_c`, `l_last(t_c)`, the cohort that commuted, whose guaranteed instalments the commutation extinguished: 1 on a real record of a commuted contract; blank on every other point |
| `ref_rate_shift_init` | a change in a rate, as a decimal: 0.005 for a rise of 50 basis points, of either sign | the valuation date | the reference rate at the valuation date less the reference rate at issue, which moves the commutation discount rate; 0 for a contract issued at or after the valuation date |

At issue each covered life is 1, the premiums paid, the income bought and the reference
rate's change are 0, and the three other columns are blank, so a point issued at or after
the valuation date carries those values, and the twins carry `DIA_US_S`'s own: 1 and 1 on a
joint contract, 1 and 0 on a single-life one, nothing paid or bought, no change. Where
`WholeLife_US_SEC`'s opening state is 0 at issue, an annuitant's survival opens at 1.

The count is a count of contracts, not of lives. A joint contract whose two annuitants have
died inside its guarantee period is one contract on the books, with both its lives at 0,
and is still paying, to a beneficiary. Survival is carried by the two life columns alone:
the lives are independent, as in `DIA_US_S`, so their two probabilities are the whole
survival state, which a count weighted by survival could not carry. On a real record each
life is 1 or 0, and a joint contract may carry one life already dead; a death that has
happened but has not reached the record carries 1, and the model then projects that life as
alive, as the record does. Restated from `DIA_US_S` at month `d`, each is `DIA_US_S`'s
probability, `lives_if(d, life)`.

`CP` and `B` hold the premium history the projection reads. `DIA_US_S` builds both from
issue, each premium adding its amount to `CP` and buying its slice of `B` at the purchase
rate of its own month, and a start-date adjustment repricing `B` in its exercise month.
Entering month 0 they are what the premiums paid before the valuation date have made of
them, an exercised adjustment included: what an administration record of a deferred income
annuity holds, the premiums paid without interest and the guaranteed income bought. The
premiums still due are priced at their own months, as `DIA_US_S` prices them, and added to
both (*Pricing on the policy clock*, below). One quantity of the pricing kernel's also
depends on every premium, paid and due: on the two refund forms `DIA_US_S` prices each
slice with the guarantee period `n_g = CP(T) / B`, a fixed point over the whole schedule,
iterated from a life-only start. The premiums still due cannot recover it, nor can `CP` and
`B`, since the iteration depends on its path, so it is a column, which the record of the
pricing holds. `Data` requires it on every refund form in force, a rule a record meets
without the schedule, though once nothing is left to price, in payout say, no cell the
reports reach reads it, only `payout_factor_calc`.

The frozen weights are where a contract open is not a life alive. A guarantee period pays
the cohort that reached the income phase, `l_last(T)`, whether or not a covered life is
still alive: in a certain period the contract stays open after the last death, its
guarantee running on to a beneficiary. Restated from `DIA_US_S`, that cohort is a
probability, 0.715 on point 20 in force 300 months, against survivors of 0.5577; on a real
record of a contract in payout it is 1, the contract having reached its income phase, and a
record whose lives are 0 inside its guarantee then pays the beneficiary the full instalment.
A commutation, one exercise named on the model point, extinguishes the guaranteed
instalments of the cohort alive to exercise it, `l_last(t_c)`; the rest of the cohort that
reached the income phase, the contracts whose annuitant died between `T` and `t_c`, keeps
its guarantee. On a real record of a commuted contract it is 1. Where either instant is at
or after the valuation month the column is blank, and the projection derives the weight
from the lives, as `DIA_US_S` does: `lives_if_last` at that month on the valuation clock,
time 0 on a contract valued at its income start month. `surv_to_payout_init` is required on
every contract past its income start month, a rule a record meets without the certain
period, though on a cash refund or a life-only form, which have no certain floor, nothing
reads it.

The reference rate's change is a fact of the market, not of the contract's history: the
reference rate on the valuation date less the reference rate on the contract's issue date,
the same for every contract issued on one date, from a published series.

| `DIA_US_S` | `DIA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months. `DIA_US_S` projects every contract from issue |
| — | `lives_if_init_1`, `lives_if_init_2` | `DIA_US_S` opens every contract with each covered life alive, `lives_if(0, life) = 1` |
| — | `cum_premium_pp_init`, `annual_income_init` | `DIA_US_S` builds `CP` and `B` from 0 at issue, through every premium in its schedule |
| — | `guarantee_mths_pricing_init` | `DIA_US_S` takes its fixed point over the whole premium schedule, which for a contract in force the schedule no longer holds |
| — | `surv_to_payout_init`, `commute_weight_init` | `DIA_US_S` reads `l_last(T)` and `l_last(t_c)` off its own survival from issue, whatever month reads them |
| — | `ref_rate_shift_init` | `DIA_US_S` reads the change since issue from one Reference, `ref_rate_shift`, which every point shares because every one is issued at its `t = 0`. Contracts issued at different dates have seen different changes, which one Reference cannot hold |

Four things `DIA_US_S` computes from issue need no column:

- **The instalments scheduled to date**, `G`, which a cash refund nets on death and an
  installment refund searches for its derived period. The income is level from the income
  start month on, so `G` is a deterministic as-if-alive schedule, fixed by the income at
  that month, the COLA, the frequency and the timing, and the model sums it by policy month
  (*The opening state*, below).
- **The acceleration's weight**, the payment factor the five instalments pulled forward
  carry. `DIA_US_S` reads it in the exercise month alone; a contract valued after its
  exercise paid the lump sum before the valuation date, and its blackout months pay nothing.
- **The commuted fraction**, `commute_frac_cum`. The commutation is one exercise named on
  the model point, so the fraction follows from the policy clock,
  `duration_mth(t) ≥ t_c`, and there is no withdrawal to carry.
- **The certain months left**, `T + certain_mths_eff() − duration_mth`, and none once
  `duration_mth` reaches the end of the guarantee.

The columns carried over are read as `DIA_US_S` reads them. For a contract in force, the
facts they record are those of issue, and the three options are exercises named on the
model point, as in `DIA_US_S`: deterministic, off by default, and, once past, in the
opening state, an adjustment in `annual_income_init`, a commutation in
`commute_weight_init`.

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `issue_age`, `joint_age` | years, age nearest birthday; `joint_age` blank on a single-life contract | issue, not the valuation date: `age(0, life)` is the attained age there |
| `sex`, `joint_sex` | `M` or `F` | — |
| `joint`, `survivor_pct`, `reduction_trigger` | the joint flag, the survivor percentage, `either` or `primary` | issue |
| `market_type` | `NQ`, `TradIRA`, `RothIRA` or `QLAC` | issue |
| `income_form`, `db_form`, `certain_period` | `LO`, `LO_ROP`, `CR`, `IR` or `PC`; `ROP` or `NONE`; years, 10 to 30 on `PC` and 0 otherwise | issue |
| `income_start_mth` | a policy month: the income starts at the start of month `T` | issue, the elected `T`; an exercised adjustment moves it to `adjust_start_mth` |
| `frequency`, `timing` | payments a year, 12, 4, 2 or 1; `arrears` or `advance` | issue; the payment months fall on the policy clock |
| `cola_rate` | a rate a year, compound | issue; the income steps on each anniversary of the income start date |
| `issue_year` | a calendar year | issue: the anchor of the generational improvement |
| `mort_basis`, `factor_basis`, `purchase_rate_dp` | `anchor` or `generational`; `table` or `formula`; decimal places, blank for full precision | modelling switches and a **[std]** convention of the pricing kernel, not facts about the contract |
| `adjust_mth`, `adjust_start_mth`, `accel_mth`, `commute_mth` | policy months, blank for never | the exercise named on the model point |
| `commute_frac` | the fraction of the remaining guaranteed payments commuted, 0 to 1 | the commutation |
| `other_qlac_premium` | dollars paid to any other intended QLAC | the owner's representation, read by the QLAC overlay alone |
| `provenance` | text: `DIA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The first
check that fails raises `ValueError`, naming the missing column or every point that fails
it. First the table's own shape:

- the ten in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, read by value, so that `12.0` is 12;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than the
  stop rule from issue plus ten years: 840 months on the anchor's life at 60, and 1,296 at
  22, the youngest issue age the product allows. Set to 0, the Reference refuses future new
  business altogether, and a negative horizon is itself refused.

Then the contract's terms, the income start month in force first, because the later checks
read it:

- `income_start_mth` is a whole number of months, 0 or more, a policy month, read by value;
- each option month, `adjust_mth`, `adjust_start_mth`, `accel_mth` and `commute_mth`, is
  blank or a whole number of months, read by value, a negative month reading as never, as
  `DIA_US_S` reads −1;
- the start-date adjustment's two months go together, both blank or both given, and the
  new start month follows the exercise, so that the income start month in force,
  `adjust_start_mth` where an adjustment is named and `income_start_mth` otherwise, comes
  after every premium priced to the old one;
- a start-date adjustment is a deferral option: `adjust_mth` precedes the
  `income_start_mth` it moves, where `DIA_US_S` would pay nothing from that month to the
  exercise;
- an acceleration and a commutation, payout-phase options, fall at or after the income
  start month in force, and six months apart or more, the product's interlock between them
  [S4]: inside the acceleration's blackout, `DIA_US_S`'s commuted value counts the
  instalments the lump sum has paid;
- `joint` is a flag, read by value: `True` or `False`, or 1 or 0, where `DIA_US_S`'s
  `bool()` reads any text, a blank among them, as `True`; `sex` is `M` or `F`, and so is
  `joint_sex` on a joint contract, the two values the tables keyed by sex hold;
- `issue_age`, `certain_period` and, on a joint contract, `joint_age` are whole numbers of
  years, 0 or more, `frequency` a whole number of payments a year and `issue_year` a whole
  calendar year, and `purchase_rate_dp` is blank or a whole number of decimal places, 0 or
  more, each read by value, so that `60.0` is 60;
- `survivor_pct` is a probability, and `cola_rate` and `other_qlac_premium` are numbers,
  zero or more, each reaching a `max` or a comparison that would lose a blank, the payment
  factor's, the refund balance's or the QLAC limit's; `commute_frac` is blank, for none, or
  a fraction, 0 to 1;
- a joint contract is on the formula basis: the table basis, equation (1), factors a single
  life's survival out of the payout factor.

Then the opening state:

- each life column is a probability, 0 to 1; the premiums paid and the income bought are
  numbers, zero or more; the guarantee period is blank or a number of months, zero or more;
  each frozen weight is blank or a probability; the reference rate's change is a number, of
  either sign, the floor applying to the whole change since issue (*The opening state*);
- a single-life contract has no second life: `lives_if_init_2` is 0;
- a contract not yet in force, `duration_mth` 0 or less, holds its values at issue: each
  covered life 1, no premium paid, no income bought and no change in the reference rate;
- `guarantee_mths_pricing_init` is given exactly on a contract in force on a refund form,
  `CR` or `IR`: on new business the kernel derives it from the whole schedule, and the
  other forms fix it, at the elected certain period or at 0;
- `surv_to_payout_init` is given exactly where `duration_mth` is after the income start
  month in force, and `commute_weight_init` exactly where the commutation month precedes
  `duration_mth`;
- a commutation is taken in the income phase by part of the cohort that reached it, so
  `commute_weight_init` is at most `surv_to_payout_init`, and each frozen weight is at least
  the probability that a covered life is alive at the valuation date, the cohort it weighs
  including every life still alive;
- each frozen weight, where given, is above 0: a contract in force past its income start
  month reached it, and a commutation is exercised by an owner alive to exercise it, so
  neither cohort is empty. At 0 the guarantee of a contract whose lives have all died would
  pay nothing, a contract owing nothing that would project.

The table is returned with the columns those checks read by value, the policy months and
the contract's whole numbers and rates, as the numbers they were checked as, int64 where a
whole-number column has no blank and float64 otherwise, and `joint` as the flags it was
checked as, which is what the projection reads. A frequency other than 12, 4, 2 or 1, and
a text column outside its categories, pass `Data` and are refused by the cell that decodes
them, with `DIA_US_S`'s message, wherever the model first reads them (`invalid frequency`,
`invalid income_form`, …).

A point at or past the stop rule, `duration_mth ≥ stop_mth()`, reads, but `proj_len()`
refuses it, naming the point. So does a contract in force that owes nothing after the
valuation date because every covered life has died, with one message for each way it can:
before the income start month, its death benefit, if any, paid; after it, with its certain
period over; or on a form with no certain period, its refund, if any, paid at the last
death. Such a contract made its last payment before the valuation date, and an in-force
extract should not carry it; it is `Term_US_SEC`'s point past its cover, for a product whose
cover can end with a death. The rule needs the certain period, which an installment refund
derives from the payout schedule, so it is the product's rule and not the table's. A
contract inside its guarantee with every covered life dead pays the beneficiary, and
projects: point 20 with its life at 0 still pays 2,259.69 at `t = 0`.

`proj_len()` also refuses, naming the point, one combination of the two payout options,
which neither model prices: an acceleration on the books, at or after the valuation date,
whose lump sum pulls forward instalments of a guarantee that a commutation before it has
reduced. The lump sum pays each instalment it pulls forward at the payment factor,
unreduced, as `DIA_US_S`'s does, so the cohort that commuted would be paid those
instalments again: `DIA_US_S`'s point 15 accelerating six months after its full
commutation pays 8,282.92 in the exercise month, 7,805.70 of it instalments the cohort
commuted, and its commutation check fails. The guarantee's end needs the certain period,
so this too is the product's rule. An acceleration that pulls forward only the
life-contingent instalments after the guarantee projects, and so does one paid before the
valuation date.

A loop over the block meets a refused row only when it reaches it, after projecting the
points before it, so `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

## The premium schedule

A deferred income annuity takes any number of premiums during its deferral [S2] [S3] [S4]
[R13], so `DIA_US_S` reads a contract's premiums from a long table, `premium_schedule.csv`,
one row per premium slice, matched to its point by `point_id`. That file knows
`DIA_US_S`'s seventeen points alone, and a point with no rows projects silently, with no
premium and no income: point 1 copied under a new `point_id` totals −1,985.46 in `net_cf`,
its expenses, against point 1's −277,363.94.

So `DIA_US_SEC` reads its own, `premium_schedule_sec.csv`, through the same reader's
Reference, `Data.premium_schedule_file`. It has `DIA_US_S`'s columns — `point_id`, `slice`,
`premium_mth`, the policy month at whose start the premium is paid, `premium_amt`, the
amount per contract, and `provenance` — and nothing but `point_id` names a point. It holds
the premiums **still due** at the valuation date:

- for a twin, `DIA_US_S`'s rows as they stand. The file opens with `premium_schedule.csv`,
  in its order, so that a twin's `premium_schedule()` is `DIA_US_S`'s, row labels and all;
- for a point in force, the premiums of policy months `duration_mth` and later: those paid
  before are in its opening state, in `cum_premium_pp_init` and, through the slices they
  bought, `annual_income_init`. Point 18, in force 59 months, holds the 50,000 of policy
  month 60, and points 19 to 25, past their last premium, hold none;
- for a point issued later, its whole schedule: point 26 holds point 8's two premiums, at
  policy months 0 and 60.

Premium months stay policy months. No row is typed by hand: the file is generated with the
table, from `DIA_US_S`'s schedule, by the same spec (*The model points*, below), and the
tests regenerate it and compare. `Data.premium_schedule_table()` checks it as it reads it,
against the model point table as checked, and the first check that fails raises
`ValueError`, naming the column, the label or every point at fault:

- the `point_id`, `premium_mth` and `premium_amt` columns are present;
- each `point_id` is a whole number, a model point's label, and labels a point of the model
  point table;
- each `premium_mth` is a whole number of months, 0 or more, read by value, so that `60.0`
  is 60, where `DIA_US_S` takes `int()` of the raw month, so that `60.5` is 60 there and
  text raises Python's own message;
- each `premium_amt` is a number, zero or more;
- no premium falls before the valuation date on a point in force: those paid are in its
  opening state;
- no premium falls at or after the income start month in force. The product takes none
  within 13 months of the income start date [S2] [S4], and the payout schedule rests on an
  income level from that month on (*Pricing on the policy clock*), as `DIA_US_S`'s refund
  base, `CP(T)`, does, which a premium after it would leave out;
- every point buys an income: a point with no income bought by the valuation date,
  `annual_income_init` 0, has a positive premium due. `DIA_US_S`'s silent case is refused,
  naming the point.

The table is returned with `point_id` and `premium_mth` as integers and `premium_amt` as
floats, the numbers checked. `premium_schedule()` and `premium_by_mth()` keep `DIA_US_S`'s
formulas. The projection reads them through `premium_pm(k)`, the premium of policy month
`k`, and the pricing kernel's fixed point sums them on a contract issued at or after the
valuation date.

## The model points

No row of `model_point_table_sec.csv` or `premium_schedule_sec.csv` is typed by hand. Every
one is generated from `DIA_US_S`, its table and its premium schedule by
`tests/sec_support.py`, from the `DIA_US_SEC` entry in its `SEC_SPECS`, and the tests
regenerate both files and compare, so an edit to a `DIA_US_S` row reaches them or fails the
suite. In the source repository, `python tools/gen_sec_points.py DIA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–17 | twin | S points 1–17 | issued at `t = 0`: `DIA_US_S`'s worked example and its two readings, the death-benefit fork, every payout form, both joint triggers, the COLA, two QLACs, the three options, generational mortality and advance timing |
| 18 | derived | S point 14 at S month 59 | the payment-acceleration contract in its deferral, the month before its second premium: 100,000 paid, 32,024.03 a year bought, `n_g` 40.810288; the 50,000 due at `t = 1` takes the income to 44,106.53 |
| 19 | derived | S point 1 at S month 241 | the anchor cell a month into its income phase, its cash refund running: a refund balance of 146,311.70 at `t = 0` |
| 20 | derived | S point 7 at S month 300 | the 10-year period certain with 60 certain months left: the floor pays the cohort that reached the income phase, 0.715, the lives being 0.5577 |
| 21 | derived | S point 15 at S month 253 | the month after its 100% commutation: 79.54 a month, the beneficiaries' residual, to policy month 359, and the life tail, 919.16, from `t = 107` |
| 22 | derived | S point 13 at S month 121 | the month after its start-date adjustment: an income of 82,907.43, the repricing by 1.8797 included, from policy month 300, `t = 179` |
| 23 | derived | S point 8 at S month 672 | the joint contract with its joint annuitant dead with certainty since policy month 661: lives 4.25e-05 and 0, the survivor's two thirds paid from `t = 0` |
| 24 | derived | S point 5 at S month 270 | the installment refund inside its derived period, 11 of its 41 certain months left |
| 25 | derived | S point 1 at S month 719 | the anchor cell in its last month, a one-row frame: the life at 6.13e-08 |
| 26 | future | S point 8, 13 months on | issued at `t = 13`, its premiums at `t = 13` and `t = 73` |

A derived row's opening state is what `DIA_US_S` carries into its month `d`, each column
read as `DIA_US_S`'s own formulas read it: each life's survival to time `d`,
`lives_if(d, life)`, before month `d`'s deaths; the premiums paid and the income bought
entering month `d`, `DIA_US_S`'s `cum_premium_pp(d − 1)` and `annual_income(d − 1)`, which
hold that month's premium; on a refund form, `DIA_US_S`'s `guarantee_mths_pricing()`;
`l_last(T)`, `DIA_US_S`'s `surv_to_payout()`, where `T` precedes `d`, and `l_last(t_c)`
where the commutation month does; and the reference rate's change since issue,
`DIA_US_S`'s `ref_rate_shift`, which it applies from month 0 on, so that a row restated at
`d` has seen all of it, 0 on every shipped row, as `ref_rate_shift` ships. Its
`policy_count` is `DIA_US_S`'s `pols_if_init()`, the contracts the point stands for, and
not `DIA_US_S`'s `pols_if(d)`, which is weighted by survival: the survival is in the life
columns. So the row continues the S projection from there. Its `policy_id` is the S row's
with the month appended, `DIA-000014-M59`, and a future row's carries the months to issue,
`DIA-000008-F13`. Row `t` of a generated point is month `t + source_mth` of its S point,
and its premium schedule holds, under its own `point_id`, the S point's premiums of months
`d` and later. All 26 are at issue age 60 and, where joint, 63, as `DIA_US_S`'s points
are. The mortality table and the improvement scale carry ages 20 to 120, every issue age the
product allows, but the two factor tables carry a handful of keys, so a point on the table
basis at another age, sex, form or deferral needs them extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other: new business in
`basiclife/BasicTerm_SE`'s sense, a contract entering the books, which brings its premium
schedule and no acquisition cost, as in `DIA_US_S`, which has none.
`pols_if_at(t, timing)` has two timings, `basiclife/BasicTerm_SE`'s:

- `"BEF_NB"`, the contracts carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the whole
  `policy_count` after it, to the stop rule;
- `"BEF_DECR"`, that count plus `pols_new_biz(t)`, which weights every cash flow of month
  `t`.

Any other timing raises. **The count is not decremented.** `DIA_US_S` weights every flow by
its constant `pols_if_init()` and carries mortality in each life's `lives_if`, and this
model does the same on the count on the books: every cash flow is
`pols_if_at(t, "BEF_DECR")` times an amount per contract weighted by survival, the premium
by `l_last(t)`, the income by the payment factor, the death benefit and the refund by the
last-death density. So `"BEF_NB"` is a closed form, the same float that a recursion
`BEF_NB(t − 1) + pols_new_biz(t − 1)`, as `Term_US_SEC`'s, would give, with no chain of
calls behind it. The count leaves the books only at the stop rule:
`pols_if_at(t, "BEF_DECR") − pols_if_at(t + 1, "BEF_NB")` is 0 at every `t` of every frame
but the last, where it is the whole count, at the end of the last projected month.
`DIA_US_S` has no maturity, and neither has this model. This is `SPIA_US_SEC`'s count, the
payout chassis', carried back into the deferral.

`pols_if(t)` keeps `DIA_US_S`'s definition, on the count on the books:
`pols_if_at(t, "BEF_DECR") × lives_if_last(t)`, the contracts weighted by the probability
that a covered life is alive at the start of month `t`, `DIA_US_S`'s
`pols_if_init() × l_last(t)` bit for bit on every twin. It carries the maintenance expense,
which the notes weight by `l(t)`, where the payout chassis weights it by
`max(C(t), l_alive(t))`. It is not the count before decrements, which mortality never
moves: on point 20, the 10-year period certain in force 300 months, `pols_if(0)` is 0.5577
against a count of 1, as `DIA_US_S`'s `pols_if(300)` is. Nor is it `SPIA_US_SEC`'s closing
measure. So the registry marks the model `survival_pols_if`, a key of its own, and the
convention every other `_SEC` model but `SPIA_US_SEC` meets,
`pols_if(t) = pols_if_at(t, "BEF_DECR")`, skips it; the conventions suite confines the key
to `DIA_US_SEC`, as it confines `closing_pols_if` to `SPIA_US_SEC`. The count on the books
is not a column of `result_pols()`: it is the table's `policy_count`, from issue to the stop
rule.

**`pols_new_biz`, and no lapse.** `DIA_US_S`'s tests forbid every name that looks like a
lapse decrement, a surrender charge or an account value: the contract has none, VM-22
declaring its standard-projection lapse section not applicable to contracts with no
account value or surrender benefit [R9]. `pols_new_biz` is not among them, and here it
means only a contract entering the books. The model has no `pols_lapse`, no `lapse_rate`,
no surrender value and no account value.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < stop_mth()`, and outside it, before issue
and from the stop rule on, every count is zero, and so every cash flow. No count evaluates
a rate there, and no cell reads a policy year or an attained age the contract does not
have: `is_payout`, `is_payment_mth` and `accel_blackout` are false, `cola_factor` is 1, and
the premium, the cumulative premium, the income, the mortality and improvement rates, the
deaths, the scheduled instalment, the certain floor, the payment factors, the refund
balance, the commuted fraction, the commutation's weight and value, the acceleration's
weight and the death and refund claims are zero before any table or schedule is read.
`lives_if` and `lives_if_last` are zero before the contract is on the books.

Four chains of calls run back a cell a month, as in `DIA_US_S`: the projection's survival,
`lives_if`, and the premiums paid and the income bought, `cum_premium_pp` and
`annual_income`, each to `t_entry()`; and on a refund form the instalments scheduled to
date, `cum_annuity_pp`, to the policy month before the valuation month, or to the income
start month if that is later. The longest sets how deep a cold call runs, counted as
modelx's stack trace counts it; `mx.set_recursion` admits a call one level deeper than the
limit it is given. A cold `net_cf` in the last month of the anchor's 720-month frame, point
1, runs 728 cells deep, 719 of them `lives_if`, against 729 in `DIA_US_S`; on the cash
refund in payout 241 months, point 19, 487 deep, 479 of them `cum_annuity_pp`; and on point
26, issued 13 months on, 728 again, because its chains stop at `t_entry()`. Every committed
point runs one cell a month back to `t_entry()` and 7 to 9 more, and point 25's one-row
frame 12 cells in all. At the longest cover the product allows, issue age 22, the youngest
[S2] [S4], with the income from policy month 360, the thirty-year deferral, 1,176 months
from issue, it runs 1,182 cells deep on an installment refund and 1,184 on a cash refund, at
the valuation date and issued 120 months on alike; the shipped tables carry age 22, so none
is extended. Each report evaluates its columns in ascending `t`, and a sweep of the
committed points that way, every report and check, runs at most 16 cells deep, on the
installment refund's twin, point 5, a recursion limit of 15. The figures count the count
cell each table's join asks first. In the model's export, `model.export()`, which runs the
cells as Python functions, about two frames a cell, the cold call in the last month needs
a Python recursion limit of 1,482 on the anchor's twin, 1,454 on the installment refund's,
1,000 on point 19 and 2,366 at the longest cover, and the ascending sweep 52 on the
committed points and 62 on the longest cover's two rows.

## The opening state

`DIA_US_S` projects every contract from issue, with each covered life alive, nothing paid,
no income bought and the reference rate where it stood at issue. A contract valued in force
needs what those have become by the valuation date. Read cell by cell, `DIA_US_S`'s
recursions carry three quantities along the contract's life — survival per life, the
cumulative premium and the income — which are four state columns, and one that follows from
the contract's terms alone, the instalments scheduled to date, which needs none. Three more
cannot be re-derived at the valuation date: the guarantee period the kernel prices with, a
fixed point over the whole premium schedule, which the premiums still due cannot recover,
and the two cohort weights `DIA_US_S` reads at a fixed past instant, `l_last(T)` and
`l_last(t_c)`, which the lives at the valuation date cannot say. And one input is a
point-to-point quantity on a market path that began before `t = 0`, the reference rate's
change since issue, whose value at the valuation date is the eighth column. The rows show
each, with what it gives when the column is wrong:

- **Survival per life.** Each life column opens `lives_if` at `t_entry()`, and from there
  the monthly rate decrements it, as in `DIA_US_S`. Point 23, the joint contract in force
  672 months, opens with lives 4.25e-05 and 0, its joint annuitant, aged 118 at policy month
  660, having died there with certainty, the shipped rate being 1 at that age. On the
  *either* trigger it pays two thirds of the instalment weighted by the primary's survival
  from `t = 0`: a payment factor of 2.56e-05, `0.666667 × lives_if(1, 1)`. Point 25 opens
  with its life at 6.13e-08, in the last month of its frame.
- **The premiums paid and the income bought.** Point 18 opens in its deferral with 100,000
  paid and 32,024.03 a year bought. Its premium still due, 50,000 at policy month 60, is
  received at `t = 1` weighted by survival to that month, the notes' five-year anchor of
  0.975, so 48,750.00, and buys income at `DIA_US_S`'s purchase rate for policy month 60,
  taking `B` to 44,106.53 and `CP` to 150,000, `DIA_US_S`'s figures. Point 22 opens with
  82,907.43 a year, the 44,106.53 its premiums bought repriced by 1.8797 when its income
  start date was deferred five years at policy month 120: the repricing is in the column,
  and the model does not run it again. Point 19 opens in payout with 150,000 paid, the
  refund base: its refund balance at `t = 0` is
  `150,000 − G(240) = 150,000 − 3,688.30 = 146,311.70`.
- **The guarantee period the kernel prices with.** Point 18, a cash refund, carries
  `n_g` = 40.810288 months, `DIA_US_S`'s fixed point over both its slices, and its slice
  still due is priced with it, at `DIA_US_S`'s purchase rate to the last bit. With the
  column at 0 the slice would buy income to 44,455.74; recomputed over the premiums still
  due alone, the 50,000 slice, the fixed point would be 50.351006 months, and the income
  43,940.38. Neither is `DIA_US_S`'s.
- **The cohort that reached the income phase.** Point 20, the 10-year period certain in
  force 300 months, has 60 certain months left. Its floor pays the instalment of 3,160.41
  at `surv_to_payout_init`, 0.715, so 2,259.69 a month through `t = 59`, while
  `lives_if_last(0)` is 0.5577: the difference is the guarantee running on to the
  beneficiaries of contracts whose annuitant has died. At the life value, 0.5577, the
  floor would pay 1,762.56 a month, 29,827.97 less over the 60 months; from `t = 60`, policy
  month 360, both pay the life-contingent instalment, 1,265.95. Point 24, the installment
  refund with 11 of its 41 derived certain months left, pays 2,628.01 at the same 0.715
  through `t = 10`, and 2,208.48 on the life from `t = 11`.
- **The cohort that commuted.** Point 21, a month after its 100% commutation at policy
  month 252, carries `commute_weight_init` 0.680338 beside `surv_to_payout_init` 0.715. It
  pays the beneficiaries' residual, `2,294.65 × (0.715 − 0.680338) = 79.54` a month, through
  policy month 359, 8,510.40 in all, and the life tail, 919.16, from `t = 107`, policy month
  360, each `DIA_US_S`'s figure. With the column at 0.715 it would pay nothing before
  `t = 107`: the commutation would extinguish the guarantee of the contracts whose
  annuitant died between the income start month and the exercise, which could not have
  commuted.
- **The reference rate's change since issue.** The commutation discount rate is
  `i_c = i_p + max(0, r_ref(t) − r_ref(0)) + m_c`, `0` the issue date: the pricing rate,
  4.75%, plus the reference rate's rise since issue, floored at 0, plus a 50 bp margin
  **[std]**. `DIA_US_S` reads the change from one Reference, `ref_rate_shift`, and every one
  of its points is issued at its own `t = 0`, so one value fits them all. Contracts in force
  at a valuation date were issued at different dates and have seen different changes, which
  no one value holds. So every contract of a block reads the change on one path of the
  reference rate, which every point shares, each from its own issue date. A contract on the
  books at the valuation date, in force or issued then, has seen `ref_rate_shift_init` by
  that date, and sees `ref_rate_shift`, the change made at the valuation date, from month 0
  on, as `DIA_US_S`'s contract sees its `ref_rate_shift` from issue: its rate is
  `i_p + max(0, ref_rate_shift_init() + ref_rate_shift) + m_c`, the two parts added before
  the floor, so that a fall before the valuation date offsets a rise at it. A contract
  issued later is bought after the change and has seen none of it, so its rate is
  `i_p + m_c`. The column ships at 0 on every row, as `ref_rate_shift` does, and no
  committed row in force is valued before its commutation; the tests add the rows. Point 15
  restated at policy month 240, twelve months before its commutation, with the column at
  0.005, discounts at 5.75%, its commuted value 195,192.02, `DIA_US_S`'s point 15's with its
  `ref_rate_shift` at 0.005, while in the same read its twin, issued at the valuation date,
  discounts at 5.25%, its commuted value 199,020.42, `DIA_US_S`'s on the shipped 0, and so
  does the same contract issued 13 months later. With `ref_rate_shift` at 0.005, the
  reference rate up 50 basis points more at the valuation date, the first discounts at
  6.25%, 191,483.27, `DIA_US_S`'s at 0.01, and the twin at 5.75%, while the contract issued
  later, bought after the rise, still discounts at 5.25%. With the column at −0.01 and the
  Reference at 0.005 the first discounts at 5.25%, and with the column at 0.01 and the
  Reference at −0.005 at 5.75%, where a floor on each part would give 5.75% and 6.25%. The
  rate is level: it reads neither clock. A path of the reference rate would be another input
  table, read on the valuation clock, each contract taking the change on it from the later
  of its issue date and the valuation date.

**The instalments scheduled to date** need no column. `cum_annuity_pp(k)`, the notes'
`G(k)`, is the instalments scheduled through the end of policy month `k`, from the income
start month: a deterministic as-if-alive schedule, fixed by the income there, the COLA, the
frequency and the timing, which a cash refund nets on death and an installment refund
searches for its derived period. It stays on the policy clock, keyed as `DIA_US_S` keys it,
and only its recursion's base moves: at the policy month before the valuation month, or
before issue on a contract issued later, `max(duration_mth_init(), 0) − 1`, a key the model
point fixes, one loop sums the instalments scheduled from the income start month to it,
the same additions in the same order as the recursion, so `G` is `DIA_US_S`'s to the last
bit, and a later key recurses back to that one, a month at a time. Point 19 reads
`G(240) = 3,688.30` at `t = 0`, and its `result_cf()` on a fresh read evaluates `G` at
keys 240 to 718 alone, where `DIA_US_S`'s `G` recurses back to issue. That base serves the
refund balance, the one other reader of `G`. An installment refund's derived period,
`n_R`, is a fixed point of the whole payout schedule, which its stop rule needs, so
`certain_mths_refund()` searches `G` upward from the income start month, a cell deep at
each key: point 24, valued 30 months into its income phase, reads `G` at keys 240 to 280,
the end of its derived period, and at no other. A cash refund asks for no key before the
valuation date's.

**The acceleration's weight** needs no column either. `DIA_US_S` pays the five instalments
pulled forward in the exercise month at the survival of that month, and reads the weight
there alone. Point 18, valued before its acceleration, pays its lump sum at `t = 193`; a
contract valued in its blackout or later paid the lump sum before the valuation date, and
its blackout months pay nothing, which the policy clock decides. `accel_payment_factor(t)`
is `DIA_US_S`'s weight in a blackout month whose exercise is on the books, and 0 where the
lump sum was paid before the valuation date; no projection cell calls it.

**The certain months left** need no column: `certain_floor(t)` is
`1{0 ≤ duration_mth(t) − T < n_eff}` on the policy clock, and the effective certain period
`n_eff` is fixed at the income start month: the elected one, or an installment refund's,
which `certain_mths_refund()` derives from the payout schedule.

## Pricing on the policy clock

`DIA_US_S` uses one survival curve, `lives_if`, for two jobs: pricing each premium's paid-up
slice at its own date, and projecting. On the valuation clock the two part. The projection's
survival, `lives_if(t, life)`, opens at the valuation date from the life columns. Pricing
stays anchored at issue and at the premium dates, deterministic from the contract's terms,
whatever the valuation date: `lives_if_pm(k, life)`, the probability that a life survives
from issue to the policy time point `k`, is one explicit loop from issue over the monthly
rates, `DIA_US_S`'s recursion unrolled, the same products in the same order, so it is
`DIA_US_S`'s `lives_if(k, life)` to the last bit, at every key of all seventeen twins. The
rate comes from one place, `mort_rate_py(y, life)`, the annual rate of policy year `y`,
whose attained age and calendar year are the year's, and `mort_rate_mth_py(y, life)`, its
monthly rate. The projection's `mort_rate(t, life)` is `mort_rate_py` at the policy year of
month `t`, so the two curves use one rate, as `DIA_US_S`'s one curve did. So pricing shares
the valuation's mortality basis, its A/E and its improvement, as `DIA_US_S`'s does: a
mortality sensitivity moves the purchase rate of every premium still due, and every twin's
and future row's guarantee period and income, while a contract in force keeps the guarantee
period it was priced with, `guarantee_mths_pricing_init`. At an A/E of 0.9, point 18's slice
still due buys 0.229129 a year per dollar rather than 0.241650, taking its income to
43,480.50, while its column keeps the 40.810288 months priced at the shipped 1.0; the twin
of point 14 prices with 43.352185 months and buys 41,520.40.

Every pricing cell is keyed by the premium's or the exercise's policy month `k`,
`DIA_US_S`'s `t` renamed: `income_start_mth_at`, `deferral_yrs`, `surv_to_income_start`,
`rop_factor_calc`, `rop_factor`, `annuity_factor_def` and `purchase_rate`.
`annuity_factor` keeps `DIA_US_S`'s arguments, policy months with a rate and a guarantee,
and carries the survival forward from its start month in one pass; `adjust_income_factor`
and `accel_cost` price at the exercise's policy month on the same curve. So a premium still
due at the valuation date is priced as `DIA_US_S` prices it: point 18's 50,000 at policy
month 60 buys 0.241650 of income a year per dollar, `DIA_US_S`'s `purchase_rate(60)` bit for
bit. The kernel reads the curve at a handful of keys: on the anchor's twin at policy months
0, 60 and 240, its two premium months and `T`; on point 18, priced on the formula basis, at
60, 120, 180 and 240, its slice still due and the five-year bands of its return-of-premium
factor; and on a contract past its last premium, none. Pricing never reads the projection,
so a cold `net_cf(0)` runs 13 cells deep on the anchor's twin, on point 13's and on point
18, 12 on the points in payout, 21 on the installment refund's twin, point 5, through its
refund-period search, and 8 on point 26, issued later, once `Data`'s table is read, where
`DIA_US_S`'s runs 251 on points 1 and 5 and 311 on point 13, recursing through survival to
the income start month.

**The payout schedule is fixed at the income start month.** Five things read the income
ahead of `t`: the installment refund's search for its derived period, which the stop rule
reads, the refund balance, the commuted value, the acceleration's lump sum and the realized
guarantee period, `guarantee_yrs()`. On the valuation clock the income `B` and the
cumulative premium `CP` are recursions, `annual_income(t)` and `cum_premium_pp(t)`, and
reading them far ahead would open a chain as long as the deferral. So
`annual_income_payout()`, `B(T)`, is `annual_income_init()`, then one loop over the policy
months from the valuation date's to `T`, applying the repricing at the exercise month and
adding each premium's slice at its purchase rate, the recursion's operations in its order;
and `cum_premium_payout()`, `CP(T)`, the refund base, is `cum_premium_pp_init()` plus the
same loop's premiums. Each is `DIA_US_S`'s `annual_income(T)` and `cum_premium_pp(T)` to the
last bit on every twin, and on a contract past its income start month the loop is empty and
both are the opening state. `annuity_pp_sched_pm(k)`, the instalment of policy month `k`,
is `B(T)/m` times the COLA of its payout year, and `cum_annuity_pp(k)` sums it (*The opening
state*). This rests on `B` being level from `T` on, which the product guarantees — no
premium within 13 months of the income start date [S2] [S4], the adjustment exercised in the
deferral — and which `DIA_US_S` assumes without checking: its refund base is `CP(T)` while
its instalments read `B(t)`, so a premium after `T` would raise the instalments and not the
refund base. `Data` refuses a premium at or after `T`, and an adjustment whose new start
month is not after its exercise.

## Departures from DIA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read of a schedule at a month is a read by policy month, every recursion on the valuation
clock begins at `t_entry()`, and pricing has a survival curve of its own. Of `DIA_US_S`'s
113 `Projection` cells, 26 are unchanged, 24 have a new docstring only and 63 are
rewritten, and 36 cells are new, 149 in all. Of its seven `Data` cells, `input_dir` and the
four readers of `DIA_US_S`'s assumption tables are unchanged, and the readers of this
model's two files, `model_point_table` and `premium_schedule_table`, are rewritten; `Data`
gains four count cells, one beside each assumption table's reader, `model_point_file` and
`premium_schedule_file` name this model's two files, and `Data` gains one Reference,
`future_horizon_mth`. None is removed or renamed, which the twin identity asserts: a cell
of `DIA_US_S`'s that this model lacked would fail it.

| Cells | `DIA_US_S` | `DIA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len`, `stop_mth` | `max(horizon_mths(), T + certain_mths_eff())`, the months from issue | `stop_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the stop rule, and for a contract owing nothing | The frame starts at the valuation date. `stop_mth()` is new and keeps `DIA_US_S`'s formula |
| `pols_if_init` | the column's 1.0, the weight of every flow | `policy_count()` for a point in force at the valuation date, 0 otherwise | Contracts in force open the count; new business joins it in its issue month |
| `premiums`, `annuity_payments`, `claims`, `commutations`, `pols_if` | `pols_if_init()` times an amount per contract | `pols_if_at(t, "BEF_DECR")` times the same amount | The count on the books weights every flow |
| `lives_if` | indexed by `t` from issue: 1 at `t ≤ 0` | indexed by `t` from the valuation date: `lives_if_init(life)` at `t_entry()` and 0 before | Survival is carried forward from the valuation date, from the contract's state there |
| `deferral_yrs`, `surv_to_income_start`, `rop_factor_calc`, `annuity_factor`, `annuity_factor_def`, `purchase_rate`, `income_start_mth_at` | keyed by the premium's month passed as `t`, and, where they read survival, reading the projection's, `lives_if` and `lives_if_last` | keyed by its policy month `k`, `DIA_US_S`'s `t` renamed, and priced on the pricing curve from issue, `lives_if_pm` and `lives_if_last_pm`, which `annuity_factor` carries forward in one pass | Pricing stays at issue and premium dates and reads no projection, to the last bit `DIA_US_S`'s; a cold `net_cf(0)` runs 13 cells deep, not 251 |
| `mort_rate`, `mort_rate_base`, `improvement_rate` | the table joined on age and sex in the monthly cell, improved and capped there | the annual rate built once a policy year, `mort_rate_py(y, life)`, improved and capped there as `DIA_US_S` caps it, and read at `policy_year(t)`; the two monthly table cells keep the limiting-age test and read through `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)` | One rate for the projection and the pricing curve, built in one cell; one reader per table, keyed by attained age, which asks its table's count cell first |
| `guarantee_mths_pricing` | the fixed point over the whole premium schedule | the same on a point issued at or after the valuation date; `guarantee_mths_pricing_init()` on a contract in force | The schedule holds only the premiums still due |
| `payout_factor`, `rop_factor`, `qlac_flags`, `accel_cost` | keyed by `age(T, 1)` and `age(t, 1)`, policy months passed as `t`, and by the label accessors `sex(1)` and `payout_form()`; `accel_cost` on `lives_if` and `annual_income(a)` | keyed by `age_at_entry(1) + T // 12` and `+ k // 12`, the model point's `sex` column and the form decodes; `accel_cost` on `lives_if_pm` and the payout schedule | On the valuation clock `T` is not a month of the frame, and a projection cell calls no label accessor |
| `premium_pp`, `cum_premium_pp`, `annual_income`, `check_income_roll_fwd_resid` | the premium at `t`, a policy month passed as `t`; recursions from 0 at `t ≤ 0`, the adjustment at `t == adjust_mth()` and the purchase rate at `t` | the premium at `duration_mth(t)`, through `premium_pm(k)`; recursions from `cum_premium_pp_init()` and `annual_income_init()` at `t_entry()`, the adjustment at `duration_mth(t) == adjust_mth()` and the purchase rate at `duration_mth(t)` | The premium history before the valuation date is opening state |
| `guarantee_yrs`, `certain_mths_refund`, `refund_balance` | `annual_income(T)` and `cum_premium_pp(T)`, read at `T` passed as `t` | `annual_income_payout()` and `cum_premium_payout()`, `B(T)` and `CP(T)`, one loop each from the valuation date's policy month | A static payout schedule, read ahead of `t` without a chain as long as the deferral |
| `is_payout`, `is_payment_mth`, `annuity_pp_sched`, `cola_factor`, `certain_floor`, `phase` | `t` tested against `T`, the payment step, the COLA anniversaries and the certain period; `TERMINATED` from `t = proj_len()` | the same tests on `duration_mth(t)`, through `is_payment_pm(k)`, `annuity_pp_sched_pm(k)`, `cola_factor_pm(k)` and `certain_floor_pm(k)`, keyed by policy month; `phase` gains `PRE_ISSUE` | On the valuation clock month `t` is not a policy month |
| `cum_annuity_pp` | `G(t − 1) + annuity_pp_sched(t)` from `t = 0` | keyed by policy month, `G(k − 1) + annuity_pp_sched_pm(k)` from `T`, based at the policy month before the valuation month by one loop in the recursion's order | A contract long in payout reads its instalments to date without recursing back to `T`, to the last bit the same |
| `surv_to_payout`, `payment_factor`, `check_payment_factor_resid` | `lives_if_last(T)` | `surv_to_payout_init()` where `T` precedes the valuation month, otherwise `lives_if_last(T − duration_mth_init())`; read only where the certain floor is positive | The cohort that reached the income phase is not the lives at the valuation date |
| `accel_blackout`, `accel_payment_factor`, `annuity_payments` | `t_a < t ≤ t_a + 5`; the lump sum at `t == t_a` reads `annuity_pp_sched(t_a + j)` and `accel_payment_factor(t_a + j)`, five months ahead | the same test on `duration_mth(t)`; the lump sum reads `annuity_pp_sched_pm(t_a + j)` and `certain_floor_pm(t_a + j)` by policy month; `accel_payment_factor` is 0 outside its blackout and where the lump sum was paid before the valuation date, and no projection cell calls it | The lump sum reads no month of the frame ahead of the exercise, and a contract valued after it needs no weight |
| `commute_frac_cum`, `commute_weight`, `commuted_value` | `t < t_c`, `t != t_c`, `lives_if_last(t_c)`, the remaining guaranteed instalments `annuity_pp_sched(s)` for `s` ahead of `t` | the same tests on `duration_mth(t)`; the weight `commute_weight_init()` where `t_c` precedes the valuation month, otherwise `lives_if_last(t_c − duration_mth_init())`; the instalments by policy month, `annuity_pp_sched_pm(k)`, in one loop | On the valuation clock `t_c` is not a month of the frame, and a contract valued after the exercise carries its cohort |
| `commute_disc_rate` | `i_p + max(0, ref_rate_shift) + m_c`, the change since issue from one Reference | on a contract on the books at the valuation date, `i_p + max(0, ref_rate_shift_init() + ref_rate_shift) + m_c`, the floor on the whole change; `i_p + m_c` on a contract issued later | Contracts issued at different dates have seen different changes, which one Reference cannot hold; on the one path a block shares, a contract issued after the valuation date has seen none of a change made at it |
| `check_lives_roll_fwd_resid` | `l(t) − d(t) − l(t + 1)`, the telescoping identity | the recursion restated month by month from the opening state, `l(t − 1)(1 − q(t − 1))`, with `lives_if_init(life)` at `t_entry()` | `lives_death` is defined as that difference, so the identity is zero whatever `lives_if` returns; the restated recursion fails on a misindexed or mis-based one, a cell a month |
| `check_commutation_value_resid` | at the commutation month, reading the guaranteed months still to come | at the guarantee's last month, reading back to the commutation month; 0 where the commutation preceded the valuation month | Every month it reads is at or before its own. The sum is the same, discounted from the exercise month, so the residual is `DIA_US_S`'s |
| `certain_mths_eff`, `certain_mths_refund`, `payment_surv_mth`, `payment_factor_life`, `is_payment_mth`, `refund_balance`, `annuity_factor`, `guarantee_mths_pricing`, `guarantee_yrs`, `payout_factor`, `rop_factor`, `rop_factor_calc`, `annuity_factor_def`, `mort_rate`, `claim_pp`, `qlac_flags`, `is_qlac` | branch on the text of `payout_form()`, `db_form()`, `payment_timing()`, `reduction_trigger()`, `market_type()`, `mort_basis()` and `factor_basis()` | branch on ten flags, `is_life_only`, `is_cash_refund`, `is_installment_refund`, `is_period_certain`, `is_rop`, `is_arrears`, `is_trigger_either`, `is_generational`, `is_formula_basis` and `is_qlac`, each reading and validating its column as `DIA_US_S`'s accessor does, with its message | No projection formula compares text or calls a label accessor, which are left to reporting, so that the compiled form can type every cell |
| `mort_rate`, `lives_death`, `lives_death_last`, `premium_pp`, `cum_premium_pp`, `annual_income`, `is_payout`, `is_payment_mth`, `annuity_pp_sched`, `certain_floor`, `refund_balance`, `accel_blackout`, `commute_frac_cum`, `commuted_value`, `commutations`, `claim_pp`, `pols_if`, `check_income_roll_fwd_resid` | unguarded: no `DIA_US_S` frame has a month outside it | zero or false outside the frame, `is_active(t)`, before any table, rate or policy year is read; `cola_factor` 1 there | A month before issue has `t ≥ 0`, a negative policy month and a policy year of 0 or less |
| `inflation_factor` | `(1 + g)^(policy_year(t) − 1)` | `(1 + g)^(t // 12)` | Unit costs in valuation-date dollars, stepping on the valuation date's anniversaries |
| `lives_if_ann`, `claims_ann`, `annuity_payments_ann`, `result_annual` | policy years 1 to `proj_len() // 12`, the year's months passed as `t` | from the valuation date's policy year to `stop_mth() // 12`, the months on the books alone, on the valuation clock | An in-force point's first row holds the rest of its current policy year, and the years before it are left out, as `Term_US_SEC`'s annual report leaves them |
| `result_pols` | `DIA_US_S`'s seven survival and payment-factor columns, then `pols_if` | `pols_if` first and `pols_new_biz` second, then the seven; zeros before issue | The counts first, after `basiclife/BasicTerm_SE`'s `result_pols()` |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_if_at`, `pols_new_biz`, `mort_rate_mth_py`, the pricing curve's monthly rate, and
three opening-state accessors, `lives_if_init(life)`, `cum_premium_pp_init` and
`annual_income_init`.

`Data`'s two readers of this model's own files check them (*The in-force interface*, *The
premium schedule*). Its four readers of `DIA_US_S`'s assumption tables, read in place, are
`DIA_US_S`'s, unchanged, and a count cell beside each checks its table once, before any
value is read: `mort_table_count`, `improvement_scale_count`, `payout_factor_count` and
`rop_factor_count`, each the table's rows, an int. Each reads its table's keys by value, as
the join matches them, so that an age written `70.0` is 70, and refuses, naming the file,
the column and the lines at fault: a key that is blank, text or not whole; a sex other than
`M` or `F`, or a payout form other than `LO`, `CR`, `IR` or `PC`, which no join reads; a
key on two rows; and, on the mortality table and the improvement scale, read at every age
from a life's issue age, a gap in a sex's ages. It refuses a value that is blank, text or
infinite, or outside its table's range — a mortality rate below 0, an improvement rate of 1
or more, a payout factor of 0 or less, a return-of-premium factor below 0 — because through
survival and the purchase rates it reaches a floor that would lose it: the refund balance's
`max(0, ·)` and the payment factor's `max`, where `max(0.0, nan)` is 0.0; mortality's cap,
with its bound second, keeps a NaN until then. A mortality rate above 1 is accepted, and
capped, and so is a negative improvement rate, a deterioration, which the generational
basis projects as `DIA_US_S` does. Each join, `mort_rate_base_at`, `improvement_rate_at`,
`payout_factor` and `rop_factor`, asks its table's count before it reads a value, so a
projection meets the checks first. A key a point needs that the table lacks still raises
where `DIA_US_S`'s does.

`Data` also refuses, naming the point, what `DIA_US_S` projects without a word or
inconsistently: a premium at or after the income start month, which the product does not
accept and which, after it, would raise the instalments and not the refund base; an
adjustment with one of its two months blank, which `DIA_US_S` ignores or turns into an
income start month of −1, or with a new start month not after the exercise; an acceleration
or a commutation before the income start month, where `DIA_US_S`'s commutation weight
exceeds the payment factor and its expected instalment goes negative; a point that buys no
income; a joint contract on the table basis, which `DIA_US_S` refuses only when a premium is
priced, naming no point; an integer column that is not whole, which `DIA_US_S` reads with
`int()`, so that 60.5 is 60 and text raises Python's own message; a blank, text or
out-of-range value in the columns a `max` or a comparison reads; a start-date adjustment
exercised at or after the income start month it moves, which pays nothing from that month
to the exercise; an acceleration and a commutation within six months of each other, the
product's interlock, where `DIA_US_S`'s commuted value counts the instalments the lump sum
has paid; a `joint` flag other than `True` or `False`, which `DIA_US_S`'s `bool()` reads
as `True` whatever the text; a sex other than `M` or `F`; and a frozen weight of 0, which
on a contract whose lives have all died zeroes the guarantee it still owes. And
`proj_len()` refuses an acceleration whose lump sum pulls forward instalments of a
guarantee a commutation has reduced, which both models pay unreduced. Each is a recorded
departure: `DIA_US_S` projects such a point.

Of the cash flows, the change of clock moves the maintenance expense alone, and
`liability_cf` and `net_cf` with it. A contract in force carries that expense in
valuation-date dollars, and its steps fall on the valuation date's anniversaries rather
than the contract's, so point 19's `expenses(t)` is `DIA_US_S`'s `expenses(241 + t)`
divided by `1.025^20`, about 1.639, in some months and by `1.025^21` in others. Its other
cash flows and its counts are `DIA_US_S`'s from its month 241 on. Point 26 is `DIA_US_S`'s
point 8 thirteen months on in those columns too, its premiums included, and its maintenance
expense is `DIA_US_S`'s times 1.025 or `1.025^2`.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 17, issued at
  the valuation date, every cell of `DIA_US_S`'s agrees at every argument `DIA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose
  meaning changed, and a cell this model lacked would fail it. So the goldens
  `tests/test_deferred_income_annuity_us.py` asserts on those points — the projection table
  of the worked example, the two slice purchase rates and the income they buy, the derived
  guarantee period, the death-benefit fork, the certain floor's conditioning on reaching the
  income phase, the joint return-of-premium pricing, the three options, the QLAC overlay and
  the generational construction — hold here with no number restated. The identity holds on
  any count, since neither model charges acquisition. The same suite holds the model to the
  conventions every `_SEC` model meets: every frame starts at `t = 0`, new business joins
  the `"BEF_NB"` count and enters once at its `policy_count`, nothing happens before issue,
  and the in-force columns are present; and to `DIA_US_S`'s product fact, that the income
  actually starts, read on the policy clock: the income in force at the income start month,
  or at the valuation date on a contract past it, is positive, and is the payout schedule's.
  The convention that `pols_if` is the `"BEF_DECR"` count is skipped, because `pols_if` is
  that count weighted by survival (*Counts and timings*).
- **The splice**, in `tests/test_deferred_income_annuity_us_sec.py`: each `DIA_US_S` point
  restated in force at months either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share, to
  1e-9 relative with no absolute floor, which would hide the survival near the limiting age,
  the roll-forward residuals apart, which are rounding around 0 and keep a floor of 1e-9. It
  skips the cells the twin identity skips, and those whose value is a frame length, a time
  point on the valuation clock or a part of a file: `proj_len`, `payment_surv_mth`, the
  premium schedule's two readers, which hold only the premiums still due, and
  `result_annual`, whose first row holds part of a policy year; and on a row valued after
  its acceleration, `accel_payment_factor`, which nothing reads from the valuation date on.
  The months are those S's events need: around point 14's second premium, the income start
  month and the months either side of it, each option month and the months either side of
  it, the anniversaries, the last month of each refund period, derived period and guarantee
  and the first after it, inside a guarantee after the last death, the month before a cap on
  mortality binds, and a frame's last month. So do eighteen variants of S's points, each
  with its premium rows, in copies of S's table and schedule that are never committed, for
  branches S's own points do not reach: every category of every text column `DIA_US_S`
  branches or joins on, each frequency on both timings valued off its payment period, a
  guarantee that outlasts the age stop, both lives dead inside a guarantee, a commutation
  inside a derived period, an acceleration that straddles the end of a guarantee, valued in
  its deferral too, where the lump sum's floor reads a derived `l_last(T)`, an acceleration
  in a commuted guarantee's last month, and a QLAC failing each of its conditions.
  Inflation, the one input on the valuation clock, is set to 0 in both models. The
  reference rate's change, which ships at 0, is switched on in `DIA_US_S`, where it is each
  point's change since its own issue; this model reads the splice's table once, as a block
  is read, on one path of the reference rate: a point restated in force has seen
  `DIA_US_S`'s change by the valuation date, and carries it as `ref_rate_shift_init`, so
  this model's `ref_rate_shift` is 0, and a point issued later has seen none, so it is
  compared with `DIA_US_S` read again with its `ref_rate_shift` at 0, the same contract on
  that path. The A/E factor, which ships at a neutral 1.0, and the Baa yield, which ships so
  that the repricing rate equals the pricing rate, are set apart in both models, and so, in
  both copies, are the mortality table and the improvement scale, by age and sex: the
  shipped rates are band-constant over ages 60 to 84 and the male rates are the female
  rates three years on, where a join on the wrong age or sex would read the same number.
  Improvement itself is not neutralized: it is dated by the calendar on the policy clock.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch the full grid reaches, every
  opening-state column, every kind of valuation month and every frequency and timing, and a
  test asserts that they do. The other cases carry the `sec_full` marker and show as
  skipped, with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets
  it, so every CI run runs the full grid too.
- **Future new business**: issued 13 months after the valuation date, more than a year on
  and off every payment step, eighteen of S's points and variants are each the S projection
  moved on, with its whole premium schedule, zeros before issue in `result_cf` and
  `result_pols`, the contracts arriving as new business with their first premium, no
  decrement rate evaluated before issue and neither table read below an issue age; and so
  are the anchor cell issued a month on, the joint point issued 12 months on, on the
  valuation date's anniversaries, and the commuting point issued 120 months on, at the
  horizon.
- **How it computes**: on every row the splice and the future business compare, after every
  report, no cell has been called at a negative argument, none evaluated from `t_entry()` on
  has read a month before it, and none evaluated at month `t` has read a month later than
  `t + 1`, directly or through a cell keyed by no month, such as `surv_to_payout()`, with no
  exception: the commutation residual reads back from the guarantee's end.
  Every policy-month, policy-year and age argument is one the contract has. On a fresh read
  of the committed model, `duration_mth(500)` evaluates `duration_mth` once, because the
  policy clock is a closed form, and every point is swept under modelx's recursion limit
  lowered to 40, which a recursion backward over the frame would exceed. A cold `net_cf` in
  the last month runs no deeper than one cell a month back to `t_entry()`, plus a fixed
  overhead, on the twins of the anchor, the installment refund and the joint point, on the
  cash refund a month into its income phase, on the joint point issued 13 months on, and at
  the longest cover the product allows; and a cold `net_cf(0)` runs a few cells deep, where
  `DIA_US_S`'s recurses through survival to the income start month.
- **Counts, validation and regeneration**: the count is on the books from issue to the stop
  rule, and `pols_if_at` refuses a timing it does not have; `pols_if` is that count weighted
  by survival; `result_pols()` is `DIA_US_S`'s, column for column, with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, a count that is not whole, with the
  reference rate's change switched on, multiplies every cash flow and the counts at each
  timing, and moves no per-contract value. Each malformed row is refused naming its point,
  each on a model read for it and again through a projection, and each by the one rule under
  test: among them a count, a duration, a month, a probability, an amount, a guarantee
  period, a frozen weight or a change that is not a number, an integer column that is not
  whole, the adjustment's months apart or out of order, an option before the income start
  month, a second life on a single-life contract, a state other than issue's on a contract
  not yet in force, a frozen weight or guarantee period missing where it is read, given
  where it is not, out of order, or a weight of 0, an adjustment at or after the income
  start month, an acceleration within six months of a commutation, and a `joint` flag or a
  sex that is not one of its values. Each malformed premium schedule is refused the same
  way, naming its point, and each malformed assumption table by the count cell beside its
  reader, naming the file's lines: a key blank, text or not whole, a sex or payout form no
  join reads, a key on two rows and a gap in a sex's ages, and a value blank, text,
  infinite or out of range, where a negative improvement rate projects as `DIA_US_S`
  projects it. Each kind of contract owing nothing, a point at or past the stop rule, and
  an acceleration inside a commuted guarantee are refused by `proj_len()` with their
  messages, and `run_sec.py --block` refuses such a table before printing anything; the
  horizon is a Reference, which at 0 refuses any future business, saying so; an unknown
  form, trigger, timing, basis, frequency or market type is refused where the model first
  reads it, the market type by the QLAC overlay alone, and so are a third life, a claim kind
  and a timing neither model knows; a zero count, integer columns written as floats, a
  contract issued 120 months on, an option month written −1, a fall in the reference rate
  since issue, a premium due between the elected income start month and a later adjusted
  one, a contract inside its guarantee with every life dead, and the assumption tables'
  keys written as floats are accepted; and the committed table and premium schedule are what
  `DIA_US_S` generates, and each derived and future row in them, projected at the shipped
  assumptions, is its `DIA_US_S` point from its month on, frame by frame and cell by cell,
  to 1e-9 relative with no absolute floor, the future row's premiums by month and annual
  display included, and only what the shipped expense inflation moves left out.
- **The opening state and the rest**: the derived rows carry the worked example over at the
  valuation date, with the figures above; pricing stays at issue and premium dates, the
  pricing survival `DIA_US_S`'s at every key and a slice still due priced at `DIA_US_S`'s
  rate; the payout schedule is `DIA_US_S`'s, bit for bit, and a fresh read of a cash refund
  in payout reads the instalments to date from the valuation date's key on alone, an
  installment refund from its income start month to the end of its derived period; each
  life's survival opens at its column; a contract open in its guarantee pays above the
  lives alive, and a commutation before the valuation date leaves its weight, a copy whose
  weight is the whole cohort paying nothing until the tail; the commutation residual closes
  at the guarantee's last month, where it is `DIA_US_S`'s at the exercise, an acceleration
  in that month included; an acceleration needs no column; three contracts in one table, in
  force, issued at the valuation date and issued later, read each the reference rate's
  change since its own issue, at `ref_rate_shift` 0 and 0.005, the last unmoved by it, and
  the floor applies to the whole change, the column and the Reference of opposite signs;
  improvement is dated by the calendar on the policy clock; where the cap on mortality
  binds, `DIA_US_S`'s own product passes 1, both models' annual and monthly rates are the
  float 1.0, every life alive at the start of the month dies in it, every report is float64
  and finite and every cell agrees with S, and a lost rate stays NaN; a check fails a
  residual that is not a number: with the A/E factor NaN, the survival check fails on every
  twin, and all four checks on the commuting point's twin, each on a residual NaN in some
  month and 0.0 in every other; expense inflation runs on the valuation clock at the
  shipped 2.5%, which only this test sees, since the splice sets the rate to 0; a contract
  issued later brings its premiums and no acquisition cost; the model has `pols_new_biz`
  and no lapse; the stop rule ends every frame; every guarded cell holds its value outside
  the frame and reads no rate there, `phase` reading `PRE_ISSUE` before issue and
  `TERMINATED` after the stop rule; the points of a block sum row by row; `result_annual`
  keeps the policy-year key; an extract without the generator's three columns, relabelled
  with its premium schedule and reversed, projects the same numbers; `run_sec.py` prints
  the model's numbers, for a point issued at the valuation date, points in payout, a
  one-row frame, a point issued later and the block; the docstrings describe the valuation
  clock and map every cell running in force adds; and the model reads `DIA_US_S`'s
  assumption tables in place.
```bash
python -m pytest tests/test_deferred_income_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_deferred_income_annuity_us_sec.py -q  # full
python -m pytest tests/test_model_conventions.py -q -k DIA_US_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R13]: #uslib-deferred_income_annuity-r13
[R9]: #uslib-deferred_income_annuity-r9
[std]: #uslib-std
<!-- END generated citation links -->
