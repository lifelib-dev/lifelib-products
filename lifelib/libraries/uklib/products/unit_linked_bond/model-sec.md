# In-Force Implementation Notes

**Status:** Draft, 2026-11-23. `ULB_UK_SEC` is [`ULB_UK_S`](model.md) taught to project
from a valuation date. Besides bonds issued at that date, it takes bonds already in force
there, in any month of their policy year, and bonds to be written in the ten years after
it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is
the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model (UKLIB-SEC-PLAN.md U2).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `ULB_UK_S` on another time axis, and it reads `ULB_UK_S`'s assumption tables in place,
> every assumption unchanged: the contractual mechanics are sourced, and every rate is a
> **[std]** standardization, the mortality basis a placeholder for the CMI's assured-lives
> tables, which are restricted to Authorised Users [R8] [REG-R30]. Replace them with
> company data and licensed tables before drawing any conclusion from the numbers.

## Run it

```bash
python products/unit_linked_bond/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/unit_linked_bond/run_sec.py 7          # point 7: the anchor cell in force 30 months
python products/unit_linked_bond/run_sec.py --block    # every model point, summed row by row
python products/unit_linked_bond/run_sec.py 7 --cython # point 7 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the library's own `build_sec_cy.py` the first time, in about a minute, and
again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. Nothing the build leaves there is committed, and `.gitignore`
covers it.

The first prints the anchor cell's first twelve rows of cash flows, with the policy
counts behind them. Three lines to the same thing for point 7:

```python
import modelx as mx
model = mx.read_model("products/unit_linked_bond/ULB_UK_SEC")
model.Projection[6].result_cf()      # point 7, the table's seventh row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `ULB_UK_S`'s takes a `point_id`: `Projection[6]` is point 7, and its
`point_id()` says so. `result_cf()` has `ULB_UK_S`'s columns — `pols_if`, `av_pp`,
`amc_charges`, `gmdb_charges`, `further_costs`, `tax_provisions`, `withdrawals`,
`claims_death`, `claims_surrender`, `unit_releases`, `death_strain`, `expenses` and
`net_cf` — with one row per month from the valuation date, `t = 0 … proj_len() − 1`, and
`result_uf()` the unit fund recursion on the same rows, per policy, column for column as
`ULB_UK_S`'s. `result_pols()` sets out the counts behind them: `pols_if`, `pols_new_biz`,
then the month's deaths and surrenders in processing order, and the survivors of the
frame's last month.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[6]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`. The block leaves out `av_pp`, the unit
fund per policy, which summed over the points is no amount of anything; every other
column is a flow of the month or the count that weights it. The runner is uslib Term's,
and `--build DIR` runs a build made elsewhere (*The compiled model*). The tool goes with
the library, into lifelib and into a `lifelib.create()` copy, so `--cython` builds there as
here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the bond, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the frame: the limiting age, or the month the fund runs out.
- **`duration_mth(t)`, the policy clock**, counts the months the bond has been in force at
  time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the key of the surrender table, of the 5% allowance
  and of the allowance-exhaustion step, and `age(t) = age_at_entry() + duration(t)`, age
  last birthday, the mortality table's, as in `ULB_UK_S`. `BasicTerm_SE` reaches the same
  numbers by adding one a month, a recursion as long as the frame; the closed form needs
  no such chain of calls.

Point 7 is the anchor cell in force 30 months. At `t = 0` it is in policy year 3 at
attained age 67, with a fund of 94,328.86 a policy, and its frame has 323 rows,
`t = 0 … 322`; S projects the same months as its rows 30 to 352. Point 11 is the GMDB
point to be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is on
the books from `t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 366 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the mortality table at the attained age; the surrender table by policy year, its last year for every later one; the allowance-exhaustion step from policy year 21; the 5% allowance, accrued by policy year for twenty years; the limiting age, the end of cover | expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

Expense inflation alone runs on `t`, stepping on each anniversary of the valuation date, so
the maintenance charge is in valuation-date pounds, for every point alike. Acquisition,
£300 per bond issued, is charged in the issue month and not inflated, as in
`basiclife/BasicTerm_SE`. The fund return, the return shock and every other Reference is a
flat rate, the same on either clock, and the rolling withdrawal cap is a twelfth of the
annual one each month, so no input reads a month before the valuation date.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
points = range(len(model.Data.model_point_table()))
frames = [model.Projection[i].result_cf() for i in points]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`ULB_UK_S` computes: every cell the two models share agrees, but two whose meaning
changed, `pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table; on S's point 3, whose fund the
depletion threshold ends a month before `ULB_UK_S` does (*Where the fund runs out*), over
the months both frames run alike. `ULB_UK_S` charges acquisition on the count in force at
`t = 0`, which on such a point is the count issued, so the two agree at any count.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `ULB_UK_S`'s columns, its
count restated as the in-force interface under `basiclife/BasicTerm_SE`'s names, its fund
at outset under the name of the cell that reads it, and two columns of opening state more.
Each state column is per policy in force, so that `policy_count` is the one weight on
every flow, and each is measured at the valuation instant, the start of month 0, before
any month-0 event (USLIB-SEC-PLAN.md D6). Each is history: what the bond has earned, borne
and paid out since issue, never re-derived from a Reference, which is an assumption from
the valuation date on, so that a Reference changed there reaches back over no month
already run (UKLIB-SEC-PLAN.md K14, §9 item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | bonds, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the bonds in force at the valuation date, for a point already in force; the bonds issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the bond's age in months: positive in force, 0 for a bond issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | pounds per bond, above 0 | for a point in force, the start of month 0, before the month's growth, charges and cancellations; for any other, its issue month | the unit fund, the bid value of units the frame opens with: `av_pp(0)` in force, the fund at outset otherwise, the premium on every shipped point |
| `wd_cum_pp_init` | pounds per bond, 0 or more | the end of month −1, after its cancellations: the start of month 0 | the withdrawals and adviser charges cancelled since issue, the total the 5% allowance is measured against and the guaranteed minimum death benefit is net of; 0 on a point not yet in force |
| `allowance_cum_pp_init` | pounds per bond, 0 or more | the start of month 0, before any month-0 event: through the policy year of month −1, so that on an anniversary the year beginning in month 0 accrues in month 0, at the valuation date's References | the 5% allowance accrued since issue, which the excess gain is measured against; 0 on a point not yet in force |

`ULB_UK_S` re-derives all three from References where its frame opens, which a Reference
changed at the valuation date would rewrite back to issue. Its fund is the premium grown
at `fund_return` and charged at the bond's rates from issue, so a market that has fallen
since issue, which no flat return set at the valuation date gives, is in the column and
not in S: a test projects point 7 on 60% of the fund S carries there, and its fund runs out
years earlier. And its withdrawals since issue are its pattern run from issue, so a
withdrawal taken once, or a pattern changed since, is in the column and not in S: the
guarantee opens from it, `max(0, P − wd_cum_pp_init)`, so a test opens point 9, whose
pattern has drawn its whole premium, at half of it withdrawn, and the guarantee is in the
money from its first month. And its allowance is `P × min(y, 20) × 5%` from issue, the
rate and the twenty years Projection References, so that an allowance rate changed at the
valuation date would rewrite every year already accrued, and the excess gain with it: at
4%, point 8's excess gain at `t = 0` would be 6,415.35 and point 9's 20,333.33, where the
history makes them 415.35 and 333.33. Here the years through the one month −1 falls in,
`y₀ = (d − 1) // 12 + 1`, are the column, and each later year accrues at the References,
`CumAllow(t) = CumAllow₀ + P × (min(y, 20) − min(y₀, 20)) × r`. Mid-year that is the year
under way; on an anniversary the year that begins in month 0 is month 0's own accrual,
which reads the valuation date's References as every month-0 event does
(USLIB-SEC-PLAN.md D6, precised at M7): at 4% the anchor cell restated at its month 12
opens with its first year's 5,000 and accrues 4,000 in month 0, as its twin issued at
`t = 0` accrues its first. A test changes the rate at the valuation date, mid-year and on
an anniversary, and writes the column off any path of it.

Nothing else of the contract is rebuilt from the References of the day. The excess gain
is the withdrawals since issue less the allowance, and the allowance-exhaustion step reads
the policy year. The withdrawal cap is a twelfth of `7.5% × max(UF′, P)` each month, which
reads no withdrawal of the twelve months before. The trailing return that drives the
performance multiplier is `fund_return + return_shock`, two flat References; a projection
that drew it from a path of returns would carry the last twelve months' as state.

`wd_allowance_rate` is one Reference with two uses, as in `ULB_UK_S`: the statutory 5%
allowance, a share of the premium a year, and the rate the `allowance_5pct` pattern
withdraws at, the pattern being "withdraw what the allowance allows". So a rate changed at
the valuation date moves that pattern's withdrawals from the valuation date on and the
allowance from the next policy year on, together, and moves neither the withdrawals since
issue nor the allowance accrued, which are columns. A bond on that pattern then withdraws
the new rate against an allowance that is the old one's to date and the new one's after: a
change of the tax rule and of the policyholder's election at once. A custom pattern reads
`wd_rate_custom` and only the allowance moves; to change the election alone, a point is
moved onto it.

| `ULB_UK_S` | `ULB_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months, any month of a policy year |
| `uf_init` | `av_pp_init` | The fund the frame opens with, under the name of the cell that reads it; S's accessor, `av_init_pp`, is gone |
| — | `wd_cum_pp_init` | `ULB_UK_S` restarts the withdrawals since issue at 0 where its frame opens, and so the guarantee at the premium |
| — | `allowance_cum_pp_init` | `ULB_UK_S` rebuilds the allowance from issue at the References of the day |

The columns carried over are read as `ULB_UK_S` reads them. For a bond in force, the
facts they record are still those at issue, or the elections that run from the valuation
date on:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age last birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `lives` | codes, as in `ULB_UK_S`'s table | issue |
| `premium` | pounds | issue: the single premium, which the withdrawal cap's floor, the allowance, the guarantee and the scheduled withdrawal are measured on |
| `n_segments` | a whole number, 1 or more | the segments held; reported only, in `av_per_segment_pp` |
| `db_uplift` | a factor, 1 or more | issue |
| `amc_rate`, `further_costs_rate`, `tax_provision_rate`, `oac_rate` | rates a year | the rates charged from the valuation date on |
| `wd_pattern`, `wd_rate_custom` | a code, a rate a year | the election from the valuation date on |
| `gmdb_flag` | True or False | issue |

Four more columns, `row_kind`, `source_policy_id`, `source_mth` and `source_refs`, record
where the generator took each shipped row from (below): `source_refs` names the References
a row was read from `ULB_UK_S` under, `fund_return 0.0` on point 12, and is blank on every
row read at those `ULB_UK_S` ships. No formula reads them, and an in-force extract need
not carry them: without them the model projects the same numbers, and `run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the five in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, which set to 0 refuses future new
business altogether; `av_pp_init` is a number above 0, and `wd_cum_pp_init` and
`allowance_cum_pp_init` numbers, zero or more, and 0 on a point not yet in force; the flag
is True or False; each code is
one `ULB_UK_S` knows; the issue age is a finite number, the premium and the custom rate
amounts zero or more, the uplift 1 or more, the four charge rates from 0 to 1, and the
segments a whole number, 1 or more. `ULB_UK_S` meets most of these only when a projection
reaches them, and some never: a blank fund or charge rate reads as NaN, which every flow
then carries, and a blank flag reads as True.

A bond whose cover had ended by the valuation date, `duration_mth ≥ horizon_mths()`, the
limiting age, reads, but `proj_len()` refuses it, naming the point: the end of cover is
the product's rule, not the table's. So does a bond the contract does not issue
([`product-spec.md`](product-spec.md)): one issued below 18, `Projection.issue_age_min`,
the youngest age the mortality table rates, though the product admits issue from 3
months, or at or past `omega_age`. Each bound is a lower-case Reference, the contract the
compiled model's caches are sized from (*The sample and the spec*): a frame of at most
1,236 months and the horizon, and ages from 18 to `omega_age`, at most `omega_age_max`,
on the mortality table. So does a point read
under a Reference outside its domain, each named, NaN and the infinities outside every
one, since `ULB_UK_S` reads several of them through a `min` or a `max` whose bound comes
first, which keeps the bound where a NaN meets it:

| Reference | Domain | Outside it |
|---|---|---|
| `issue_age_min` | a whole number of years below `2**53`, 0 or more | a NaN switches the bound off, every comparison with it failing; past `2**53` the compiled model's `long long` cannot hold it |
| `omega_age` | a whole number of years below `2**53`, above `issue_age_min`, at most a year past the table's last age, `Data.mort_age_last() + 1`, 121 | it sizes every frame: a NaN, an infinity or a fraction raises in the fund's search; cover reads attained ages to `omega_age − 1`, so past a year beyond the table's last age a rate would be read beyond the table |
| `omega_age_max` | a whole number of years below `2**53`, and `omega_age` at most it, 121 as shipped, the shipped table's last age plus one | the compiled model's caches hold frames to this limiting age and no further, so a longer mortality table, which would admit a later `omega_age`, bounds no frame; past `2**53` its `long long` cannot hold it |
| `fund_return`, `inflation_rate` | finite, −1 or more | the monthly return `(1 + g)^(1/12) − 1` has no real value, and the inflation factor changes sign each year |
| `return_shock` | finite, and `fund_return + return_shock`, the trailing year's return, above −1 | a trailing return of −100% or less is a fund lost whole; a NaN reads as no shock |
| `mort_be_factor` | finite, 0 or more | a mortality rate is negative |
| `wd_allowance_rate` | finite, 0 or more | the allowance and the anchor pattern's withdrawal are negative |
| `allowance_years` | a whole number of years below `2**53`, 0 or more | the allowance is negative, a NaN lets it accrue without end, and past `2**53` the compiled model's `long long` cannot hold it |
| `depletion_threshold` | finite, 0 or more | no fund, floored at 0, would count as exhausted |
| `surr_rate_cap`, `wd_cap_rate` | 0 to 1 | no probability, and no share of the fund or the premium; a NaN or negative withdrawal cap pays no withdrawal, so the anchor cell projects 660 months, not 353 |
| `perf_factor_cap`, `perf_factor_slope`, `allow_step` | finite, 0 or more | a negative surrender rate; a NaN is lost in the bound-first `min`, and the surrender rate reads the cap in every month |

Each check is a comparison written out, a finite bound the largest float and a whole one
`2**53`, so that the compiled model runs it in C; the four integer References are printed
through `int()` once they are whole. A value a formula computes past the floats from
References each in its domain is refused in the cell where it first is, naming the
References: the fund, where a `fund_return` or an opening fund near the largest float
grows it past them, at `av_pp_at(t, AFT_GROWTH)`, naming both, where `ULB_UK_S` makes
`inf − inf` a NaN, floors it to 0 and
reads it as exhaustion; and the allowance, under a `wd_allowance_rate` that large, which
the excess gain's `max(0, …)` would read as no gain. And so does a bond whose opening fund
is at or below the threshold (*Where the fund runs out*). A loop over the
block meets such a row only when it reaches it, after projecting the points before it,
so `run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

`surr_rate` keeps `ULB_UK_S`'s `min(surr_rate_cap, w_base × M_perf × M_allow)`. With the
table's rates held to 0 to 1 by `Data`, and the cap and the multipliers to their domains by
`proj_len()`, no frame reaches a rate outside 0 to 1, where S's monthly rate is a complex
number past 1 and its surrenders add policies below 0; the cell still refuses one, or NaN,
in the month it first leaves, naming the point, the month, the rate and the References
that make it, for a caller that reads it outside a frame. A rate of exactly 1, the cap at 1
binding, is in range: every bond left after the month's deaths surrenders.

The assumption tables are checked before a value of them is read, each in the cell the
projection takes its extent from: `Data.mort_age_first` and `mort_age_last` for the
mortality table, whose two sexes must run over the same ages, one row an age, without a
gap or a repeat, each rate a number from 0 to 1; and `Data.surr_last_year` for the
surrender table, policy years from 1 without a gap, each rate from 0 to 1. A key is read
by its value, so an age written `35.0` is 35. Each refusal names the file, the column and
the lines at fault: the mortality table's check reads the file as it stands, one read
that `ULB_UK_S`'s reader then sorts. No frame reads past the table's last age: cover
reads attained ages to `omega_age − 1`, and `proj_len()` holds `omega_age` to a year past
that age, and to `omega_age_max`, so that the contract, not the table's length, bounds
every frame. A read below the table's first age, a bond issued at an age the
table does not rate, is refused by the one cell that reads it, naming the point and the
age, where `ULB_UK_S`'s lookup raised `KeyError`. The surrender table takes its last year
for every later one, as `ULB_UK_S` does, so no read is beyond it.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`ULB_UK_S` and its table by `tests/uk_sec_support.py`, from the `ULB_UK_SEC` entry in its
`SEC_SPECS`, and the tests regenerate it and compare, so an edit to a `ULB_UK_S` row
reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py ULB_UK_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 6 | twin | S points 1 to 6 | issued at `t = 0`: `ULB_UK_S`'s anchor cell and its variants, the accumulation cell, the adviser charge, the GMDB, the 101% uplift and the custom 3% |
| 7 | derived | S point 1 at S month 30 | the anchor cell mid-way through policy year 3, 12,500.00 withdrawn and 15,000.00 of allowance accrued |
| 8 | derived | S point 3 at S month 66 | the adviser charge mid-way through policy year 6, its withdrawals and charges since issue 498.69 past the allowance |
| 9 | derived | S point 4 at S month 240 | the GMDB point in policy year 21, its whole premium withdrawn and its guarantee 0, the step on and the allowance spent |
| 10 | derived | S point 1 at S month 352 | in the last month before its fund is exhausted: a one-row frame |
| 11 | future | S point 4, 13 months on | to be issued at `t = 13` |
| 12 | derived | S point 4 at S month 66, S run under a `fund_return` of 0 | the GMDB point mid-way through policy year 6, its fund earning nothing since issue: its guarantee in the money and the rider charging |

A derived row's `policy_count` is the count `ULB_UK_S` carries into that month, its
`pols_if(d)`, and its state what S carries there, so the row continues the S projection
from there: point 7 opens with 0.901766 bonds, a fund of 94,328.86 a bond and 12,500.00
withdrawn since issue, and point 9 with 0.107986 bonds, a fund of 41,262.73 and the whole
premium withdrawn. Its `policy_id` is the S row's with the month appended,
`ULB-000001-M30`, and a future row's carries the months to issue, `ULB-000004-F13`. Row `t`
of a generated point is month `t + source_mth` of its S point.

No state `ULB_UK_S` reaches at its shipped References has the rider charging after the
issue month: its GMDB point's fund grows faster than its 5% withdrawals erode the
guarantee, and in its issue month the guarantee exceeds the uplifted fund after the
month's withdrawal by £82.88, on the death benefit alone; the rider charge, on the fund
before the withdrawal, is 0 throughout. So point 12 is read from S run under a
`fund_return` of 0, a fund that has earned nothing since issue, the spec's `derived_refs`:
at month 66 it holds 0.729798 bonds, as at the shipped return, since no decrement reads a
return, a fund of 67,232.39 and the withdrawals and the allowance the pattern gives, and
its guarantee, 72,500, stands above the uplifted fund after charges, 67,457.08. Set on the
model too, that return gives the row S's path over the whole of both frames, 143 months to
policy month 209. At today's return, which takes over from the valuation date, the paths
part in month 0's growth: the row's frame runs 203 months, to policy month 269, the rider
charging in its first 36 and the death benefit paying the guarantee in its first 39, and
only its opening state and its counts, which read no return, are S's. C2 freezes it, so
that the rider charge is in every later version's fingerprint; the splice's GMDB point at
a 4% AMC and a K14 test, which writes point 9's withdrawals since issue at half its
premium, as T4's table does, reach the charge too.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` keeps
`ULB_UK_S`'s three timings and adds `basiclife/BasicTerm_SE`'s `BEF_NB`, each an int code
named as `ULB_UK_S`'s text, in the order of its instant within the month (*The compiled
model*):

- `BEF_NB`, 0, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, 1, that count plus `pols_new_biz(t)`, before month `t`'s decrements, which
  `pols_if(t)` returns;
- `BEF_SURR`, 2, after the month's deaths, before its surrenders;
- `AFT_DECR`, 3, the end of the month, after its deaths and surrenders, which is `BEF_NB`
  at `t + 1` exactly, and 0 in the frame's last month.

Any other timing raises, the fund's four among them. The survivors carried into month `t`
are those of month `t − 1`'s `BEF_DECR` count, which `BEF_NB` forms itself, as its own
value at `t − 1` plus that month's new business, exactly the sum `BEF_DECR` returns. So
within a policy year the chain of calls from month `t` back is one cell a month, where
`ULB_UK_S`'s `pols_if` chain runs three; and in a year's first month after `t_entry()`,
`BEF_NB` reads the year's opening, `pols_if_py(y)`, which walks the year before in
ascending order, a cell a month, and returns its last month's `AFT_DECR` count, the same
float. The unit fund and the withdrawals since issue are blocked by policy year the same
way, the fund one cell a month within a year where `ULB_UK_S`'s runs four (*Departures*),
so that a compiled run's chains fit its stack (*What a compiled run needs*). On a model
just read, a cold `net_cf` in the frame's last month runs one cell a month back to its
policy year's first month, two cells a year before that, back to `t_entry()`'s year, and
at most 16 cells more, at each shape's longest cover, issued at 18 now and 120 months
on, the limiting age at the contract's largest, 121: 1,236 months on the accumulation
cell, whose cold `net_cf` runs 228 deep on a chain of 215, where at the shipped limiting
age one cell a month ran 1,232 deep and `ULB_UK_S`'s fund alone would run about 4,900;
each other chain, the excess gain and the guarantee, reads the withdrawals since issue,
and runs no deeper. The deepest is the GMDB point's with no withdrawals, the rider to the
limiting age: its unit-funding residual 16 cells beyond its chain, 231 deep, its death
strain 15 and its `net_cf` 14. The bound of 16 is `Term_UK_SEC`'s, met here with nothing
to spare: one cell a month, the deepest call ran 12 beyond, and the year walk's steps at
the chain's foot add four. A model that copies the walk measures its own overhead and
derives its bound from that, rather than copy 16.

The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_surr(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. `pols_maturity` holds the survivors of the frame's last month: those still
holding a bond whose fund has just been drawn to nothing, or the population at the
limiting age. It pays nothing.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < horizon_mths()`, issued and short of the
limiting age, and outside it, before issue and from the limiting age on, the unit fund and
every count are zero, and so every cash flow. No count evaluates a decrement rate there,
and no table is read at a policy year or an attained age the bond does not have:
`mort_rate`, `surr_rate_base`, `allow_factor`, the allowance, the guarantee, the
withdrawal and its cap are zero outside cover, before any table or rate is read. Cover
reads the limiting age alone, not `proj_len()`: the frame also ends where the fund runs
out, which `fund_exhaust_mth()` finds by projecting the fund, and the fund reads cover. So
in the months after the fund is exhausted and before the limiting age a bond is in cover
and holds no units, and there the counts are zero because the frame has ended.

## Where the fund runs out

`ULB_UK_S` ends its frame at the first month whose fund opens on 0 or less. The withdrawal
cap draws a fund to nothing on a subtraction whose exact value is 0: the month's fund
after charges, less the adviser and rider charges and the withdrawal, which the cap sets
to what those leave. Where nothing but the withdrawal is cancelled, as on S's points 1, 4
and 5, the float is 0 exactly. Where an adviser charge or a rider charge is cancelled
beside it, the float is a rounding of either sign, floored at 0, and which it is turns on
the fund's last bit. S's point 3, its adviser charge beside its withdrawal, closes its
fund on 3.39e-15 at the end of policy month 322, so S projects month 323 on that: 0.0194
bonds, a maintenance charge of £0.18 against an AMC of 6e-20, and its survivors maturing
a month later. A fund read back from a CSV an ulp off, or the same model compiled with
another order of operations, closes it on 0 instead, and ends a month sooner.

So this model ends the frame at the first month whose fund opens at or below
`depletion_threshold`, half a pence, uslib `VA_US_SEC`'s value (UKLIB-SEC-PLAN.md §9 item
10; USLIB-SEC-PLAN.md §7.7, *Record — M9*): far above any rounding of a fund in pounds and
far below any fund worth projecting. `fund_exhaust_mth()` searches the fund from
`t_entry()`, ascending, the one loop that reads beyond `t + 1`, which R2 admits; from 0 it
would find a bond issued later exhausted before its issue. `proj_len()` refuses a bond in
force whose fund opens at or below the threshold, which has nothing to project, and one
not yet in force whose fund at outset does.

Its effect on each of S's points, which a test holds:

| S point | `ULB_UK_S`'s frame | `ULB_UK_SEC`'s | Why |
|---|---|---|---|
| 1, 4, 5 | 353 | 353 | the fund closes on 0 exactly at the end of policy month 352 |
| 2, 6 | 660, 780 | 660, 780 | the fund never runs out, and the frame runs to the limiting age |
| 3 | 324 | 323 | the fund closes on 3.39e-15, at or below the threshold |

On point 3 every cell agrees with `ULB_UK_S`'s in each of the 322 months before the SEC
frame's last; in its last, every cell but where its survivors go, which leave here as
`pols_maturity(322)` and in S carry on into month 323; and the frame's net cash flow moves
by S's month 323 alone, −£0.18. The twin identity, in `tests/test_model_conventions_uk.py`,
names point 3 alone, with its two frames, 323 and 324 (`TWIN_FRAME_ENDS`, beside
`TWIN_FLOORS`): it asserts them, and that S's month 323 opens on a fund above 0 and at or
below the threshold, compares the months before the last, and leaves the frame's end to
that test. Every other twin's frames must end together, so a frame cut short on any other
point fails there.

## Departures from ULB_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a month passed as `t` is a read at the policy month or year, and each recursion
opens at `t_entry()` from the opening state. Where `ULB_UK_S`'s test would have stayed
correct on the valuation clock, it moved anyway, so that cover has one definition. Nine
cells are new with running in force, and seven more with compiling, `point_id`,
`mort_schedule`, `wd_pattern_code`, the three years' openings, `av_pp_py`,
`wd_cum_pp_py` and `pols_if_py`, and `av_pp_grown_refusal` (*The compiled model*); one of
`ULB_UK_S`'s,
`av_init_pp`, is gone, `av_pp_init` replacing it. The twin identity names it as dropped,
and a cell of `ULB_UK_S`'s that this model lacked without saying so would fail it.

| Cells | `ULB_UK_S` | `ULB_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `t_entry`, `is_active`, new | — | `max(0, −duration_mth_init())`; `0 ≤ duration_mth(t) < horizon_mths()` | The first month on the books, and cover, read from the limiting age alone |
| `fund_exhaust_mth` | the first `t` from 0 whose fund is 0 or less | the first month from `t_entry()` whose fund is at or below `depletion_threshold`, as a policy month | *Where the fund runs out* |
| `proj_len` | `min(horizon_mths(), fund_exhaust_mth())`, from issue | the same less `duration_mth_init()`, from the valuation date; raises past cover, outside the contract's bounds, under any of fifteen References outside its domain, and on an opening fund at or below the threshold | The frame starts at the valuation date |
| `av_pp`, `av_pp_at`; `av_pp_py`, new | `av_pp(t) = av_pp_at(t − 1, "AFT_WD")`, four cells a month, from `uf_init` at 0 | `av_pp_init()` at `t_entry()`; in a policy year's first month after it, the year's opening, `av_pp_py(y)`, which walks the year before in ascending order and returns `av_pp_at(t − 1, AFT_WD)`; in any other month, month `t − 1`'s growth, tax provision, charges and cancellations inline, in `av_pp_at`'s order and floats; `av_pp_at` reads `av_pp`; 0 outside cover | One cell a month within a policy year and two a year before it (D5), so that the compiled chain fits its stack (*What a compiled run needs*); the same float as S's in every month |
| `wd_cum_pp`, `gmdb_guarantee_pp`; `wd_cum_pp_py`, new | 0 before `t = 0`, one cell a month | `wd_cum_pp_init()` before `t_entry()`, and in a policy year's first month after it, before the month's withdrawal, the year's opening, `wd_cum_pp_py(y)`, which walks the year before and returns `wd_cum_pp(t − 1)` | The withdrawals since issue are history, and the guarantee opens from them; blocked by policy year as the fund is |
| `allowance_cum_pp` | `P × min(y, n) × r`, every year from issue | `allowance_cum_pp_init()`, then `P × (min(y, n) − min(y₀, n)) × r` for the years after the one month −1 falls in; refused past the floats | The allowance accrued is history; the same float on a point not yet in force |
| `pols_if`, `pols_if_at`, `pols_if_init`; `pols_if_py`, new | a recursion through `"AFT_DECR"`, three cells a month, from the column's 1.0 at 0 | `BEF_DECR`, one cell a month within a policy year through `BEF_NB`, which in a year's first month after `t_entry()` reads the year's opening, `pols_if_py(y)`, the year before walked and its last `AFT_DECR` count; `pols_if_init()` is 0 unless in force | Bonds in force at the valuation date open the count; new business joins it in its issue month; blocked by policy year as the fund is |
| `pols_death`, `pols_surr`, `BEF_SURR` | unguarded | zero outside cover and the frame, before a rate is read | No count evaluates a rate outside cover |
| `mort_rate`, `surr_rate_base`, `allow_factor`, `allowance_cum_pp`, `wd_cap_pp`, `wd_pp`, `gmdb_charge_pp` | unguarded: no `ULB_UK_S` frame has a month outside cover | zero outside cover, before any table or rate is read; the tables' extents from `Data`, a read past the mortality table refused by name | Before issue S's tables raise `KeyError`, and its allowance is negative |
| `surr_rate` | `min(cap, w_base × M_perf × M_allow)` | the same, and a rate outside 0 to 1, or NaN, refused in its month, which with the domains no frame reaches | Past 1 S's monthly rate is complex; below 0 its surrenders add policies |
| `inflation_factor` | `1.025^duration(t)`, from issue | `1.025^(t // 12)`, from the valuation date | Unit costs in valuation-date pounds (D7) |
| `expenses` | acquisition on `pols_if(t)` at `t = 0` | on `pols_new_biz(t)` | A bond in force bears no acquisition, one issued later bears it in its issue month, per bond issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `check_pols_roll_fwd_resid` | `pols_if(t + 1)` | `pols_if_at(t + 1, BEF_NB)` | The next month's new business is no part of month `t`'s movement |
| `check_pols_roll_fwd` | tolerance on `pols_if_init()` | tolerance on `policy_count()` | S's `pols_if_init` is 0 on new business here |
| `result_pols`, new | — | `pols_if`, `pols_new_biz`, `pols_death`, `pols_surr`, `pols_maturity` | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `policy_count`, `duration_mth_init`, `av_pp_init`, `wd_cum_pp_init`, `allowance_cum_pp_init`, `pols_new_biz`, new | — | the interface's columns, and the new business of each month | *The in-force interface*; *Counts and timings* |

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. Point 7 carries that expense in valuation-date pounds, so its `expenses(t)` is
`ULB_UK_S`'s `expenses(30 + t)` with S's factor, `1.025^((30 + t) // 12)`, taken out and
`1.025^(t // 12)` put in: 1.025² less at `t = 0`. Its `pols_if`, its fund, its charges, its
withdrawals, both claims columns, `unit_releases` and `death_strain` are `ULB_UK_S`'s from
month 30 on. Point 11 is `ULB_UK_S`'s point 4 thirteen months on in those columns too; its
maintenance expense is `1.025^(t // 12 − (t − 13) // 12)` above S's at each `t`, and its
acquisition £300 exactly.

`mort_rate` caps the annual rate at 1, written `min(q, 1.0)`, the product first and the
bound second, as `ULB_UK_S` writes it, so that a NaN stays NaN where `min(1.0, q)` would
read it as certain death; wherever `q` is a number the two are the same float. At the
shipped `mort_be_factor` of 0.8 the rate stays at or below 0.8 to the end of every frame,
and `Data` refuses a table rate past 1; the product passes 1 through the factor, from
attained age 111 at 1.25, which a test shows. The surrender rate's bound keeps
`ULB_UK_S`'s order, `min(cap, …)`: it is no cap on mortality.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and how three of its chains reach back in
time, and no number: what the model computed on each committed point was frozen before
the change, and it still computes it, to the last bit (*Tests*, below). Cell by cell, at
every argument a full modelx sweep evaluates, the compiled model computes what modelx
computes, bit for bit, on the committed points, on the points of the splice grid, which
take the branches they do not, at the contract's longest covers, where the cap on
mortality binds, at the depletion threshold's edges, on every value a decoded column
holds, on keys written as floats, and on the committed row in the money under the fund
return it was read from. The compile tests hold it so on x86-64, and to 1e-12 relative
elsewhere, where no run has shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py unit_linked_bond                  # in place, beside the model
python build_sec_cy.py unit_linked_bond --out /tmp/ulb   # elsewhere, with the CSVs
```

The tool exports the model to `ULB_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `ULB_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/unit_linked_bond")    # the directory holding the build
from ULB_UK_SEC_nomx_cy import mx_model as model
model.Projection[6].result_cf()                    # point 7, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about a minute with gcc, 53 to 64 s here, and needs modelx-cython, which
needs a C compiler, so the models do not require it: `pip install modelx-cython`, or
`pip install -r requirements-cython.txt` in the source repository, which pins the release
the compile tests run. `run_sec.py --cython` builds in place when it finds no build, or one
older than the model, the sample, the spec or the tool, and `--build DIR` runs a build made
with `--out DIR`. Nothing a build writes is committed. All of it derives from committed
files, and an extension module is built for one operating system, processor and Python
(`_mx_classes.cpython-313-x86_64-linux-gnu.so` here); in place, `.gitignore` covers all of
it. The tool is the library's own, so lifelib and a `lifelib.create()` copy build as the
source repository does.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so: a cell
whose body still looks a value up in a DataFrame or compares text runs Python under its C
declaration. So each input now reaches a cell as a number, as uslib's `Term_US_SEC` was
taught first (USLIB-SEC-PLAN.md R1 to R17), and `Term_UK_SEC` here:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[6]` is point 7, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `premium()` is `float(data.premium()[idx])`. Compiled, the vector is a typed memoryview,
  and the read is a load from memory. The three columns of opening state are vectors too.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the number it selects, for every point at once: the sex into the row of the mortality
  table it selects, `mort_schedule`, M 0 and F 1; the withdrawal pattern into its code,
  `wd_pattern_code`, `NONE` 0, `ALLOWANCE_5PCT` 1 and `CUSTOM` 2, a code rather than the
  rate it selects, because the anchor pattern's rate is `Projection.wd_allowance_rate`, a
  Reference `Data` cannot read; and the rider's True or False, `gmdb_flag`, into a 0/1
  flag. Each decodes as `ULB_UK_S` reads the column, which a test holds on every value a
  column can hold, and what it cannot hold it refuses (below). `lives` decodes into
  nothing: `Data` refuses any value but `single` as it reads the table, where `ULB_UK_S`'s
  guard, which no formula calls, would let a joint row project as single.
- **Tables indexed by integers.** The mortality table is `mort_table_array`, by sex and
  attained age, padded from age 0 so that the index is the age; the surrender rates are
  `surr_table_array`, by policy year 1 to 11, padded at year 0, beside the last year,
  `surr_last_year`, an int cell. The padding holds NaN, and nothing reads it: the one cell
  that reads each table checks its key first, `mort_rate` against the mortality table's
  ages either side, and `surr_rate_base` holds the policy year at the table's last above,
  as `ULB_UK_S` does, and reads in cover alone, where the year is 1 or more.
- **Codes.** A timing or a kind, which `ULB_UK_S` spells as text, is an int Reference
  named as the text. The count's four timings and the fund's four are numbered as one
  family, the count's first, so that a timing of one is refused by the other's cell:
  `BEF_NB = 0`, `BEF_DECR = 1`, `BEF_SURR = 2` and `AFT_DECR = 3`, in the order of their
  instants within the month, then `BEF_GROWTH = 4`, `AFT_GROWTH = 5`, `AFT_CHARGE = 6` and
  `AFT_WD = 7`, in the fund's; and `DEATH = 0` and `SURRENDER = 1`. A call reads as
  before, less the quotes: `av_pp_at(t, AFT_WD)`. A string argument would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap.
- **The claims total, a code of its own.** `ULB_UK_S` totals the two kinds as
  `claims(t)`, its `kind` defaulted to `None`, with Python's `sum`. A default compiles as
  a keyword parameter the typing guard refuses, and `None` is no C integer, so the total
  is `claims(t, ALL)`, `ALL = 2`, which the unit-funding residual reads. It is written
  out, `0.0 + claims(t, DEATH) + claims(t, SURRENDER)`, left to right, which is `sum`'s
  float wherever at most two kinds are non-zero, and there are only two: `sum`
  compensates since Python 3.12, and the error of a single addition, added back, rounds to
  the sum it came from. A test holds the total to `ULB_UK_S`'s by its bits.
- **Three chains blocked by policy year.** The fund, `av_pp`, the withdrawals since
  issue, `wd_cum_pp`, and the count carried in, `pols_if_at(t, BEF_NB)`, each run one cell
  a month within a policy year, as at the in-force step, and in a year's first month read
  the year's opening, `av_pp_py(y)`, `wd_cum_pp_py(y)` and `pols_if_py(y)`. Each opening
  walks the year before in ascending order, asking the monthly cell of each of its months,
  so that each finds the month before cached, and returns the year's last month's closing
  value: `av_pp_at(t - 1, AFT_WD)`, `wd_cum_pp(t - 1)` and `pols_if_at(t - 1, AFT_DECR)`,
  which are the month's own floats, so no number moves. A cold read then runs one cell a
  month back to its year's first month and two cells a year before that, where one cell a
  month ran the whole cover on the C stack (*What a compiled run needs*, below).
- **No refusal formatted on a chain.** A compiled cell's C frame holds the code that
  formats each of its messages, whether a run reaches it or not, and a chain holds a frame
  of each cell it recurses through at each level: on CI's Ubuntu runner, a refusal
  formatted in `Term_UK_SEC`'s recursive waiver cell had its cold call need 512 KiB to 1
  MiB, and 256 to 384 KiB without it (UKLIB-SEC-PLAN.md K12). So `av_pp_at`, which the
  fund's deepest path holds three times at each end, formats nothing: where the fund it
  grows has left the floats it calls `av_pp_grown_refusal(t)`, which computes the fund
  grown again from the same cells, the same float, and raises `av_pp_at`'s message, naming
  the month, `fund_return` and `av_pp_init`. The cell takes the month alone, since a float
  parameter would give it a dictionary for a cache, and returns the fund grown where it is
  finite, which the sample asks for to type it. A test holds every cell that a cold call's
  deepest path holds more than once to building no text and raising only a constant. The
  allowance's refusal
  stays in `allowance_cum_pp`, and the surrender rate's and the mortality table's in
  theirs: no chain recurses through them, each read once, at a path's foot or off it.
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `lives()` and `wd_pattern()`, and the three reports return a table row, text and
  DataFrames, for a reader, for `run_sec.py` and for the comparison with `ULB_UK_S`. No
  other cell calls them, so they cost the projection nothing. Each label refuses any value
  but its column's codes, as `ULB_UK_S`'s `lives` and `wd_pattern` do, and as `sex` now
  does where `ULB_UK_S`'s returns the column as read, so each returns text or raises, and
  compiles to `str`.

The `Data` docstring lists its 20 vectors and arrays and its three extents, each with the
column or file it comes from. The five readers stay Python, returning DataFrames and a
path, and no `Projection` cell but `model_point()` reads them. Every other cell of
`Projection`, 82 of its 89, returns a C `bint`, `long long` or `double`, and caches a single
value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,358 by `t`, of `double`, `long long` or `bint` | the 47 cells of `t` alone: every count, rate, charge, fund, withdrawal and cash flow, and the fund grown's refusal; the policy clock, its years and the attained age; the checks' residuals; and the flag `is_active` |
| a C array of 1,358 by 8 | `pols_if_at(t, timing)`, `av_pp_at(t, timing)` and `claims(t, kind)` |
| a C array of 104 by policy year | `av_pp_py(y)`, `wd_cum_pp_py(y)` and `pols_if_py(y)` |
| one `bint`, `long long` or `double` | the 29 other cells without a parameter: the point's numbers, codes and flag, its opening state, the ends of its frame, the three monthly rates, and the three checks |
| a Python object, or `str` | the seven reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three reports
and the three checks on every committed point, and then the cells no report reaches:
`model_point()` and the three label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; `av_pp_grown_refusal(t)`, which only `av_pp_at`'s error path
calls, where the fund has left the floats, and which returns the fund grown elsewhere, so
that the sample's call of it in every month types it; `av_per_segment_pp`, with
`n_segments`, which only it reads; and two codes, the count at `AFT_DECR`, which
`ULB_UK_S`'s count chain read in every month and this model's reads only where a year's
opening ends, and the fund at `BEF_GROWTH`, which is `av_pp`, each monthly one in every
month of the frame and the month after it. It runs the committed points alone: the export
reads the CSVs of the directory the build is made in, which in place is the product
directory. The committed points leave branches untaken: the custom pattern above the 7.5%
cap, the cap binding net of an adviser charge, the rider beside an adviser
charge, the surrender cap and the performance multiplier binding, the cap on mortality.
That still types every cell, because every branch of a cell returns the one type its
others return, a count or an amount a float in every branch, and on points that take those
branches the compiled model computes modelx's numbers (above). The labels need no trace
beyond the committed points: each refuses what is not its codes, so each returns text
alone. The sample also raises the recursion limit, which modelx raises and its export does
not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,358 | 1,357. The longest frame is the longest cover, a bond issued at 18, `issue_age_min`, whose fund lasts to the largest limiting age, 121, `omega_age_max`, issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × (121 − 18) + 120 = 1,356 months, `t = 0 … 1,355`, and the month after, 1,356, whose roll-forward residual reads the count carried into 1,357 |
| `t`, `timing`; `t`, `kind` | 1,358 by 8 | `t` as above, by the eight timings, and by the two kinds and the total. Every 2-D cache of a model shares one inner width, the widest: Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `y` | 104 | 103, the policy year of the longest cover's last month, 1,235 months from issue, whose first month reads its opening |

**The limiting age the caches hold.** `omega_age` may be set to a year past the mortality
table's last age, 121 on the shipped table, as `ULB_UK_S` and the in-force step allow, and
the frame then runs a year longer than at the shipped 120. A longer table would let it run
longer still, so the contract has its own bound, `omega_age_max`, 121, the shipped table's
last age plus one: every limiting age the shipped table admits projects, in modelx as
compiled, and `proj_len()` refuses an `omega_age` above the bound, naming the point
(*What it refuses*), so that no table bounds the caches. `proj_len()`
refuses an issue age below `issue_age_min`, and `Data` a point issued more than
`future_horizon_mth` months ahead, so no report on a point the model projects runs past
these caches. Those three References are the contract the sizes are derived from; the ages
bound none, since an age indexes `Data`'s mortality table, not a cache. Raise
`omega_age_max` or the horizon, or lower `issue_age_min`, and a report runs past the caches
in the compiled model alone: `t` or `y` past its size raises `IndexError`, naming nothing,
where modelx projects. Each needs the sizes derived again, as `spec_sec.py` derives them,
and a rebuild; a longer horizon, `t` raised to 12 × (`omega_age_max` − `issue_age_min`) +
the horizon + 2.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as the year walks' month counter, stays a Python object, though the
cell is typed `double`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of each
decrement here, and the fund's monthly return, `(1 + g)^(1/12) − 1`, are complex powers,
which gcc computes with `cpow` rather than `pow`, and whose last bits can differ from
Python's; and gcc fuses a multiply and an add where the target has the instruction, one
rounding where Python rounds twice. The tool's docstring has the detail, and uslib's
[`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the measurements
that put each there. With all four, every compiled value here agrees with modelx bit for
bit. The compile tests hold each directive in the module's first line, and a static test
holds the tool's line to the two and no other.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
1,156,248 bytes, the type's basic size, which holds every cell's cache, and deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a test runs the compiled runner on a block of the committed points repeated and finds
no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 24. What it needs
is stack. That call is a cold one in the last month of the longest cover, a bond issued at
18 whose fund lasts to the limiting age, now or 120 months on: 1,236 months from issue at
the contract's largest limiting age, 121, and 1,224 at the shipped 120. One cell a month,
as the in-force step left the fund, the count and the withdrawals since issue, the call at
the shipped limiting age ran 1,236 cells deep in modelx, and compiled with gcc a cold
`net_cf` needed 288 KiB of C stack: it ran on a thread of 288 KiB and not of 284. The
count's chain needed that, at about 240 bytes a month, a cell's formula frame of 96 bytes
beside its two-dimensional cache's wrapper of 128, and the fund's 248 to 252 KiB, at about
210: past, or all but at, the 256 KiB the C step allows itself, so that the 1 MiB thread
holds on every runner, where `Term_UK_SEC`'s cold call needed two to four times as much on
CI's Ubuntu runner as here (UKLIB-SEC-PLAN.md §6.1, *Record — M2*). No cell those chains
recurse through month by month builds text. `av_pp_at`'s refusal of a fund past the
floats took its formula's frame from 96 bytes to 208, and the deepest path holds six such
frames, three timings at each end of the fund's chain, so moving it into a cell of its own
(*What compiling changed*, above) saves 672 bytes of the 288 KiB: one cell a month, the
call still runs on 288 KiB and not on 284 with it moved, as before. So the three chains
are blocked by policy year as well. Blocked, the call runs 229 cells deep in modelx at
120 and 231 at 121, on a chain of 213 and 215, one cell a month within its year and two
cells a year before it, and 16 more, which a test holds. Compiled, on the three shapes
whose cover runs a century, to or near the limiting age, the deepest chain heads,
`net_cf`, the count, the unit-funding residual and the death strain, run on a thread of
60 KiB and not of 56, at 120 and at 121 alike, the refusal in `av_pp_at` or moved, each
head cold in an ItemSpace of its own; the fund on 56 or 60, and the withdrawals since issue
and the excess gain on 52 or 56. The
GMDB point withdrawing 5% and the adviser charge, whose funds run out at 353 and 323
months, run on 36 KiB and not on 32. A test runs each shape at its longest cover in a
thread of 1 MiB, the stack Windows gives a program's main thread unless the program is
linked for more, and again on the main thread, which is where `run_sec.py --cython` runs,
and records the smallest of its sizes each ran on. MSVC's frames may be larger than
gcc's, and the `cython_uk` CI job, which runs the test on Windows too, is the check on
them. The export recurses in Python instead: the same call needs a recursion limit of 477
there at 121, and the reports and checks, which run in ascending `t`, need 128, so
`sample_sec.py` sets 2,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message: each
malformed row of the table, each assumption table a reader cannot read, each point the
frame refuses, each Reference outside its domain that the compiled model can hold, each
exhausted fund, each surrender rate outside 0 to 1, a key read beyond the mortality table,
either side, the fund and the allowance past the floats, and what the vectors cannot hold,
in a cell typed `long long` or `double` as in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, and an
age or a count of years as an int. So a rate written as an int, 2, gives one message in
both engines. An int Reference, `issue_age_min`, `omega_age`, `omega_age_max` or
`allowance_years`, is a C `long long` compiled, and a float set on it is truncated as it is
set, 18.5 to 18, where modelx refuses 18.5 as not a whole number, and a NaN or an infinity
cannot be set on it at all; so set each as a whole number.

- What `Data` cannot decode or hold, when the vector is first read, naming every point or
  line at fault: a `point_id` that is not a whole number, or is `2**53` or more in size; an
  issue age `2**53` or more in size, which an int64 vector cannot hold whole and numpy
  would cast without a word; a mortality age or a surrender policy year as large, before
  its table is cast; and, as since the in-force step, a code that names no sex or pattern,
  a joint bond and a flag that is not True or False. A key written as a float, an age
  `35.0`, is read by its value, as `ULB_UK_S`'s lookups match it. The tables' checks find
  a gap from the keys a table holds, so that a key far from the rest, `2**53 − 1`, is
  refused as a gap at once.
- A key beyond the mortality table, by the one cell that reads it, where `ULB_UK_S`'s
  lookup raised `KeyError`: `point_id 1: mort_table.csv has no rate at attained age 18`,
  from `mort_rate`, on a table that starts at 20. No frame reads past the table's last
  age, which `proj_len()` holds `omega_age` to.
- An `omega_age` above `omega_age_max`, by `proj_len()`, which only a mortality table
  longer than the shipped one, or the bound lowered, can bring about: `point_id 1:
  omega_age, 121, is above omega_age_max, 120`, under a bound lowered to 120. Raised past
  121, the bound lets a longer table's frames run past the caches, in the compiled model
  alone (*The sample and the spec*).
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: expense inflation calls Python's own
  power where its own is infinite from a finite base, so that the compiled model raises the
  platform's message as modelx does (uslib's *Record — M22* form), rather than carry an
  infinity on. Only an inflation above about 600 a year reaches it within the longest
  frame; a test does, at 1e20, from `t = 192`, the month before computing in both.
- A timing or a kind no cell takes, by the cell, as `ULB_UK_S`'s are: `invalid timing`
  and `invalid kind`. Each 2-D cache is 8 wide, so a code inside it that its cell does not
  take, a fund's timing in the count's cell, a count's in the fund's or a code past the
  kinds' three, reaches the formula, which refuses it in both engines, as a test holds.

An argument outside a cache raises `IndexError` in the compiled model alone:
`net_cf(1358)` or `net_cf(-1)`, which modelx answers with 0, the month being outside
cover; `pols_if_at(t, 8)`, `av_pp_at(t, 8)` and `claims(t, 8)`, which modelx refuses as a
timing and a kind it does not take; and a year's opening at policy year 104, past the `y`
cache, which modelx computes as it computes any year's opening, the closing value of the
year before: 0 once that year is past the point's cover, as on the test's point, issued at
65, and the fund that year closes on for a bond whose cover reaches it, one issued at 18
under a limiting age of 121. No frame asks for it: a frame's last month is in policy year
103 at most. An `idx` past the last row is refused in both, with an `IndexError` at the
first read of a vector, and `Projection[-1]` reads every vector at its last element in
both, so it is the table's last point, under that point's own `point_id()`; the compiled
refusal test holds both against modelx.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
product at 1, as `ULB_UK_S` does, and a compile test holds the two equal on points where
the cap binds, new business and in force. A NaN product would stay NaN through the cap, in
both, which the compiled model computes as a comparison that keeps the value unless the
bound is smaller.

### Speed

`python tools/bench_sec_cy.py unit_linked_bond` builds the model into a temporary
directory and times one block run on three engines: modelx, the export and the compiled
model. Each engine runs the committed table repeated, in a process of its own, as
`run_sec.py --block` runs a block, each point projected and then released. `net_cf` is
`net_cf(t)` summed over the frame, the projection alone, as `basiclife/BasicTerm_SC` is
timed on its `pv_net_cf()`; `result_cf` is the report `run_sec.py` prints, which builds a
DataFrame for each point. Each run of the tool takes the fastest of three runs of each
engine and loop. The tool was run three times, and each time below is the median of its
three, with the range of the three beside it:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,000 | 0.236 ms (0.236–0.240) | 0.813 ms (0.796–0.854) | 86 MB |
| export | 600 | 3.13 ms (3.08–3.25) | 4.54 ms (4.37–4.56) | 86 MB |
| modelx | 120 | 111 ms (105–113) | 163 ms (150–172) | 135–137 MB |

On `net_cf` the compiled model runs 13.1 times its export (13.1 to 13.8 over the three),
and on `result_cf`, where building the DataFrame takes most of its time, 5.5 times (5.3
to 5.6); it runs 470 times modelx on `net_cf` (436 to 481) and 191 on `result_cf` (188 to
212). The ranges are the noise of a machine other builds were using, its 1-minute load
between 2.5 and 4.0 as the runs started: about −5% to +2% on modelx's `net_cf`, −8% to
+6% on its report and −2% to +5% on the compiled report. `Term_UK_SEC`, timed the same
way on its own points on the same day, ran 12.8 and 4.5 times its export. A point here
costs more on every engine, its frame being longer: 340 months on average over the
committed points, against Term's 244. The release keeps a
block flat: the compiled model's peak and the export's grew by less than 0.1 MB over
their 6,000 and 600 points in every run, where modelx's rose by 22 to 38 MB in its loop.
Reading the three files and building every `Data` vector and array for the compiled block
took 0.022 s, and asking every point for its frame, the runner's first pass, 0.55 to
0.56 s. Every engine, loop and run summed `net_cf` over a copy of the table to the same
87,156.19325, to 1e-9 relative.

Measured on 2026-11-23 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.30 GHz), a 1-minute load average between 2.52 and 3.96 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`, made at `4fbc404`,
before `omega_age_max` rose to 121 and every `t` cache with it by 12 elements.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1 to 6, every
  cell of `ULB_UK_S`'s agrees at every argument `ULB_UK_S` evaluates in its own sweep, to
  1e-9 relative with no absolute floor, but for `pols_if_init` and `model_point`, and
  `av_init_pp`, which the spec names with its reason; a cell this model lacked would fail
  it. On point 3 it holds the two frames, 323 and 324, S's month 323 opening on a fund
  above 0 and at or below the threshold, and every month but the SEC frame's last, which
  the threshold's test holds; on every other twin the frames end together. So `ULB_UK_S`'s worked example, which `tests/test_unit_linked_bond_uk.py`
  asserts to the penny, holds here with no number restated. The kinds and timings are
  compared as the codes of the same names, and `ULB_UK_S`'s claims total, `claims(t)`,
  with `claims(t, ALL)`. The same suite holds the model to the conventions every `_SEC`
  model meets: every frame starts at `t = 0`, `pols_if` is the `BEF_DECR` count, new
  business enters once at its `policy_count`, nothing happens before issue, and the
  in-force columns are present.
- **The splice**, in `tests/test_unit_linked_bond_uk_sec.py`: each `ULB_UK_S` point
  restated in force at months 1, 11, 12, 23, 24, 37, 59, 60, 119, 120 and 125, about the
  surrender bands' edges, 239, 240 and 241, about policy year 21, where the step starts,
  the allowance stops accruing and the GMDB of the anchor's pattern runs out, and 322, 352,
  659 and 779, each frame's last month, continues the S projection in every cell the two
  share but `proj_len`, and in both reports, to 1e-9 relative with no absolute floor, but
  the residuals and an exhausted frame's last month, which closes a fund on a subtraction
  whose exact value is 0, at a floor of 1e-9. Every switch that ships off is on in both
  models: a return shock of −0.75, which takes the performance multiplier to its cap of 2,
  and a surrender cap of 0.25, which binds from policy year 21; inflation, the one input on
  the valuation clock, is 0 in both. Four variants of S's points, in a copy of S's table
  that is never committed, reach what S's own cannot: the GMDB point at a 4% AMC, in the
  money; the custom pattern at 9%, above the 7.5% cap; the adviser charge with the GMDB
  beside it; and the custom 9% with a 0.5% adviser charge, the cap binding net of the
  charge. A core of 29 of the 114 splice cases and 7 of the 18 future ones runs by
  default, and the full grid with `UKLIB_SEC_FULL=1`; a test asserts the core reaches every
  branch, opening-state column, kind of valuation month and side of every `min` and `max`
  the full grid reaches.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point is
  the S projection moved on, with zeros before issue and no rate evaluated there, and so is
  each variant issued a month on, the GMDB point 13 months on and the custom 3% 25.
- **How it computes**: on every row of the splice's grid, after its reports, its checks
  and every monthly cell at every month, no cell has been called at a negative month, none
  on the books read a month before `t_entry()`, none read a month later than `t + 1` but
  the exhaustion search's reads of the fund to the frame's end, and none raised; the
  search reads the fund alone, from `t_entry()`. On a fresh read of the committed model,
  `duration_mth(500)` evaluates `duration_mth` once, the policy clock being a closed form,
  and every point's reports and checks run under modelx's recursion limit lowered to 40,
  which a recursion backward over the frame would exceed. Each chain, called cold in the
  last month at each shape's longest cover, at the limiting age of 121, runs one cell a
  month back to its policy
  year's first month, two cells a year back to `t_entry()`'s, and at most 16 more; the
  inline fund is `av_pp_at`'s, bit for bit, and each year's opening, of the fund, the
  withdrawals since issue and the count, is the closing value of the month before it, the
  one cell a year that the month reads; and no cell that a cold call's deepest path holds
  more than once, at the limiting age of 121, builds text anywhere in its
  formula, at a raise, in an error branch or into a local, or raises other than one
  exception on one string constant.
- **Counts**: the roll-forward closes; `result_pols()` is S's counts with `pols_new_biz`
  beside them; multiplying `policy_count` by 2.5, with every switch that ships off on,
  multiplies every flow and counted cell and moves no per-policy value, the fund at each
  timing, the withdrawals since issue and the guarantee among them, on a table where every
  flow is nonzero on some point, the rider charge on point 9 written at half its premium
  withdrawn; each point in force, restated a month on with the count and the state it
  carries there, continues its own flows, each weighted by the count in force, not the
  count the point opened with; and the check, its tolerance scaled by the count, closes on
  a million bonds.
- **Validation and regeneration**: each malformed row of the table, 60 cases, each `2**53`
  bound at the bound among them, is refused naming its point; the horizon is a Reference;
  a point past its cover or outside the contract's bounds, 6 cases, an issue age of
  `2**53 − 1` among them, is refused by `proj_len()`, each bound just inside it and each
  moved past a committed point, and `run_sec.py --block` refuses such a point before
  printing anything; each of fifteen References is held to its domain, 115 cases, each
  edge accepted and the nearest value past it refused, NaN, the infinities, a fraction and
  `2**53` too, an `omega_age` of 121 accepted, as at stage E, and refused under an
  `omega_age_max` lowered to 120, the fund and the allowance refused where they would pass
  the floats; so is a fund at or below the threshold, at exactly it, part of it and a
  rounding above 0, where the least fund past it projects; a surrender rate of exactly 1 is accepted, and one just
  above 1 or below 0 refused in its month and by the frame; each assumption table a reader
  cannot read, 26 cases, a key of `2**53` and of `2**53 − 1` among them, is refused naming
  its lines, and a read beyond the mortality table naming the point; keys written as
  floats
  read as `ULB_UK_S` reads them; the edges of the interface and of each bound are
  accepted; every state `ULB_UK_S` reaches, as shipped and under the splice's switches, is
  accepted in force, but the fund S runs on at 3.39e-15, which is refused as exhausted;
  and the committed table is what `ULB_UK_S` generates.
- **The product's own facts**: the two clocks on the shipped points; the committed rows,
  in force and issued later, continuing their S points at the shipped assumptions but for
  inflation; each history column read, not recomputed, the fund written at 60% of S's and
  the withdrawals since issue at half the premium and at 10,000 more, each projected
  through, and the allowance accrued kept at its history under an allowance rate changed
  at the valuation date and written off its path (UKLIB-SEC-PLAN.md K14); the threshold's
  effect on each S point, and a fund that
  reaches the threshold exactly exhausted there; the surrender bands, the step and the
  allowance on the policy clock; expense inflation on the valuation clock at the shipped
  2.5%, which only this test sees; acquisition on new business alone; every guarded cell's
  value outside cover, and after an exhausted frame; the block; an extract without the
  generator's columns, labelled otherwise, projecting the same numbers;
  `run_sec.py`'s numbers, for a point and for the block, and its sum, and its `--cython`
  stopping where no repository is above it; no cell's parameter defaulted; the
  docstrings, read through docutils as the docs build reads them where docutils is
  installed; and the shared input tables.
- **The cap**: on the accumulation cell under the splice's References and a
  `mort_be_factor` of 1.25, the product of the table rate and the factor passes 1 from
  attained age 111, policy month 552. In both models `mort_rate` and `mort_rate_mth` are
  the float 1.0 there; every bond in force at the start of that month dies in it, and none
  is in force after it; the reports hold finite floats; and every cell the two models
  share agrees, issued now and 12 months on, and restated in force the month before the
  cap, to 1e-9 relative with no absolute floor. And a NaN sent to the cap, through
  `mort_be_factor`, stays NaN.
- **The C step's representation**, in modelx, in seconds: `claims(t, ALL)` is the sum of
  its two kinds by its bits on every committed point's month, and `ULB_UK_S`'s total by its
  bits on every twin's, both kinds and the guarantee paying in some month; every value each
  text column can hold decodes as `ULB_UK_S` reads it; each padded array holds NaN where no
  file does and nothing else, and the mortality table's one reader refuses an age below
  it, on an extract labelled otherwise than by position; each `Data`
  vector is the int64 or float64 the `Data` docstring's table states, and each
  parameterless cell returns a Python number; each label refuses a value that is not its
  codes; `spec_sec.py`'s sizes and `sample_sec.py`'s recursion limit are what their
  comments derive; `run_sec.py --cython` rebuilds exactly when a source is newer; and a
  label the vectors cannot hold, or a timing or a kind no cell takes, a timing of each
  family in the other's cell among them, is refused.
- **C2, the fingerprint**: every committed point computes what the model computed when
  its E step ended, every cell at every argument, frozen at the end of the module by
  `tools/gen_sec_fingerprint.py` before the C step changed anything, and refrozen once
  since, alone, when point 12, the GMDB in the money, was committed, which moved no number
  of points 1 to 11.
- **Compiled**, the tests marked `cython`, which compile the model once a session into a
  temporary directory and run it in child processes: in
  `tests/test_compiled_conventions_uk.py`, C3, the typing guard, on the declarations, the
  spec and the generated C; C4 on the committed points; and the release. In this model's
  module, C4, every cell at every argument a full modelx sweep evaluates, with every code
  no swept cell reads (`_ulb_c4_also`, the spec's `c4_also`, which a test holds to asking
  each in every month, row by row, the codes each cell takes derived in modelx, not read
  from the test's own lists), on the splice grid, at the contract's longest covers, issued
  now and 120 months on at the limiting age of 121, the longest 1,356 months, where the
  cap binds, at the depletion threshold's edges, on every value a decoded column holds, on
  keys written as floats, and on the committed row in the money under its own return; the
  refusals, message for message, the fund, the allowance and the inflation factor past the
  floats among them, each code no cell takes inside the caches, the `IndexError`s past the
  caches and an `idx` past the table and of −1; each shape's deepest cold call on a 1 MiB
  thread and on the main thread; a Reference set late, which clears no cache; and
  `run_sec.py --cython`, which prints what modelx prints.

```bash
python -m pytest tests/test_unit_linked_bond_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_unit_linked_bond_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k ULB_UK_SEC
UKLIB_CYTHON_SHARD=unit_linked_bond python -m pytest -m cython tests -q     # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R8]: #uklib-unit_linked_bond-r8
[REG-R30]: #uklib-reg-r30
[std]: #uklib-std
<!-- END generated citation links -->
