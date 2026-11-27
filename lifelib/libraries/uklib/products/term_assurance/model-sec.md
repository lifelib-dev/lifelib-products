# In-Force Implementation Notes

**Status:** Draft, 2026-11-22. `Term_UK_SEC` is [`Term_UK_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year, and policies to be written in the ten
years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The
product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model (UKLIB-SEC-PLAN.md U2).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `Term_UK_S` on another time axis, and it reads `Term_UK_S`'s assumption tables in place,
> every assumption unchanged: the contractual mechanics are sourced, and every
> quantitative assumption is a **[std]** standardization, the mortality basis a proxy for
> the subscriber-restricted CMI "16" Series tables [R11]. Replace them with company data
> and licensed tables before drawing any conclusion from the numbers.

## Run it

```bash
python products/term_assurance/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/term_assurance/run_sec.py 8          # point 8: the anchor cell in force 5 years
python products/term_assurance/run_sec.py --block    # every model point, summed row by row
python products/term_assurance/run_sec.py 8 --cython # point 8 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the library's own `build_sec_cy.py` the first time, in about a minute, and
again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. Nothing the build leaves there is committed, and `.gitignore`
covers it.

The first prints the twelve rows `run.py` prints for `Term_UK_S`'s point 1, with the
policy counts behind them. Three lines to the same thing for point 8:

```python
import modelx as mx
model = mx.read_model("products/term_assurance/Term_UK_SEC")
model.Projection[7].result_cf()      # point 8, the table's eighth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `Term_UK_S`'s takes a `point_id`: `Projection[7]` is point 8, and its
`point_id()` says so. `result_cf()` has `Term_UK_S`'s columns — `pols_if`, `premiums`,
`claims_death`, `claims_fib`, `claims_lapse`, `claim_expenses`, `expenses`, `commissions`
and `net_cf` — with one row per month from the valuation date, `t = 0 … proj_len() − 1`.
`result_pols()` sets out the counts behind it on the same rows: `pols_if`,
`pols_new_biz`, then the month's deaths and lapses in processing order, the expiries of the
last covered month, and `Term_UK_S`'s other four columns, the policies paying premium, the
deaths since issue, `fib_cum`, and the two monthly rates.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[7]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`, as below. The runner is uslib Term's,
and `--build DIR` runs a build made elsewhere (*The compiled model*). The tool goes with
the library, into lifelib and into a `lifelib.create()` copy, so `--cython` builds there as
here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the term.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index `k`, and the contract runs
  on it: `duration(t) = duration_mth(t) // 12`, the select duration,
  `policy_year(t) = duration(t) + 1`, the lapse table's key, and
  `age(t, life) = age_at_entry(life) + duration(t)`, the mortality table's, as in
  `Term_UK_S`. `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion
  as long as the frame; the closed form needs no such chain of calls.

Point 8 is the anchor cell in force 60 months, `Term_UK_S`'s own point 8. At `t = 0` it is
in policy year 6 at attained age 40, and its frame has 240 rows, `t = 0 … 239`; S projects
the same months as its rows 60 to 299. Point 14 is the waiver point to be issued 13 months
after the valuation date: `duration_mth(0) = −13`, it is on the books from
`t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 253 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the mortality table at the attained age and the select factor at the select duration; the lapse table by policy year; the decreasing schedule `B(k)` and the family income benefit's commuted value `I a(N − k)` at the policy month; an annual premium on the policy anniversary; the RPI increase on each anniversary; renewal commission from the second policy year; the clawback window from issue; the end of cover | expense inflation, `inflation_factor(t) = 1.03^(t // 12)` |

Expense inflation alone runs on `t`, stepping on each anniversary of the valuation date, so
the maintenance charge is in valuation-date pounds, for every point alike. Acquisition, £150
per policy issued, and the initial commission, 150% of the issue premium's year, are
charged in the issue month and not inflated, as in `basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf()
          for i in range(len(model.Data.model_point_table()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`Term_UK_S` computes: every cell the two models share agrees, but two whose meaning
changed, `pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table. `Term_UK_S` charges acquisition and
the initial commission on the count in force at `t = 0`, which on such a point is the count
issued, so the two agree at any count.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `Term_UK_S`'s columns, two
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s names, and
seven columns of opening state. Each state column is per policy in force, or a ratio, so
that `policy_count` is the one weight on every flow, and each is measured at the valuation
instant, the start of month 0, before any month-0 event. An event that falls at the
valuation date itself is month 0's, the projection's first, made at the References of the
valuation date, as it is on a policy issued then, and is not history (USLIB-SEC-PLAN.md
D6, precised at its M7): on a point valued on its anniversary, that anniversary's RPI
increase is made at `t = 0` at the `rpi_rate` of the day, and the factors carried in are
those of the policy year it closes. Each column is history: what the policy has had or
paid, never re-derived from a Reference, which is an assumption from the valuation date
on, so that a Reference changed there reaches back over no month already run
(UKLIB-SEC-PLAN.md K14, §9 item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `lapse_cum_init` | a share of the policies issued, 0 to below 1 | the start of month 0 | the selective-lapse ratio `w_cum`: the share of the issued cohort that has lapsed |
| `fib_cum_init` | deaths per policy in force, 0 or more | the start of month 0 | the deaths since issue, for each policy still in force, on every shape, which `cohort_frac` opens from |
| `fib_streams_init` | streams per policy in force, 0 to `fib_cum_init` | the start of month 0 | on the family income benefit, the streams in payment: the deaths since issue whose instalments were not commuted, at the take-up of the month each fell in; 0 on the other shapes |
| `idx_factor_init` | a factor, 1 or more | the start of month 0: mid-year, the policy year under way; on an anniversary, the one it closes | the RPI cover increases given before month 0, on the sum assured at issue; 1 on a policy in force 12 months or fewer |
| `idx_prem_factor_init` | a factor, 1 or more | as `idx_factor_init` | the RPI premium increases given before month 0, on the premium at issue |
| `wop_waived_frac_init` | a share of the policies in force, 0 to 1 | the start of month 0 | the policies whose premium the waiver of premium rider waives; 0 while the policy has been in force no longer than the deferred period |
| `comm_init_pp_init` | pounds per policy, 0 or more | issue | the initial commission the policy paid when it was written, which the clawback recovers; 0 on a point issued at or after the valuation date, which pays `comm_init_rate` in its issue month |

`Term_UK_S` re-derives two of them from References, which a Reference changed at the
valuation date would rewrite back to issue. It pays the family income benefit on
`(1 − c)` of every death since issue at the take-up `c` of the day, so a take-up of 0.5 set
at the valuation date of the point in force at 66 would commute half the streams long in
payment, and pay 49.6% low at `t = 0`; here the streams in payment are a column, and each
later death adds its `(1 − c)` share, `fib_streams(t)`, so that the payment is
`I [(1 − c) D(t) + streams(t)]`, `Term_UK_S`'s number at a take-up that never changes. On
new business it is S's bit for bit at the take-ups the shipped points hold, 0 and 1, and at
0.5; at another, such as 0.3, a sum of scaled deaths and a scaled sum round apart, and T1
compares the ledger's residual, a rounding about zero, at a floor of 1e-9. And it rebuilds
the commission paid at issue from `comm_init_rate`, which the clawback recovers; here a
point in force reads it.

`Term_UK_S` re-derives the two indexation factors from `rpi_rate` too, every increase from
issue at the rate of the day; here they are history up to month 0. So the indexed point
valued on its fifth anniversary carries the factors of policy year 5, `1.03^4` and
`1.045^4`, and its frame takes the fifth step at `t = 0`: at the shipped 3% that is
`Term_UK_S`'s own `1.03^5` from month 60, and with the RPI set to 5% at the valuation date
it is `1.03^4 × 1.05`, its cover 177,267.64 in month 0, where a column that held the year
the anniversary opens would carry the step made at 3%, and pay 173,891.11. A policy in
force 12 months or fewer has been given no increase, its first anniversary falling in
month 0 or later, so `Data` holds its factors to 1. An extract written under the old
rule, its factors those after an anniversary at the valuation date, is refused only at
month 12; on a later anniversary it passes every rule and takes the month-0 step twice,
so an extract must give the factors before it.

The waiver's deferred period is a vector whose length is a Reference,
`Projection.wop_defer_mths`, six months as shipped, so it goes in a companion,
`wop_pipeline_sec.csv`, keyed by `point_id` and `lag`, as uslib's indexed UL keys its
segment ladder by slot:

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `point_id` | a label of the model point table | — | the point the row belongs to, and the only column that names one |
| `lag` | whole months, 1 to `min(wop_defer_mths, duration_mth)` | — | the policy month `lag` months before the valuation date in which the lives became incapacitated |
| `wop_deferred_init` | a share of the policies in force, 0 to 1 | the start of month 0, after the recoveries of the `lag − 1` months since | the lives still in the deferred period from that month: its incidence, `inc_m act` of the lives active then, less those who have recovered since |

That is what `Term_UK_S`'s `wop_waived_frac(t)` carries into a month a later month reads:
the waived share itself, `u(t − 1)`, and the incidence of the month `wop_defer_mths + 1`
months back, whose lives enter waiver once the deferred period has run, those who have not
recovered. At the valuation date the waived share is `wop_waived_frac_init`, and the
cohorts of the six months before it are still in the deferred period: in the frame's
first six months, the entrants of month `t` are the share at lag `7 − t`, carried through
the `t` months of its deferred period still to run at the recovery rate, `(1 − rec_m)^t`.
Each later month's incidence falls on the lives active then, `wop_active_frac`, which at
the valuation date are what the waived share and the pipeline leave,
`1 − wop_waived_frac_init − Σ wop_deferred_init`, and which follow their own chain from
there: the three shares are one in-force, and `Data` refuses a point whose waived and
deferred shares sum past 1.
UKLIB-SEC-PLAN.md §6.1 names the pipeline's state "the incidence of the deferral months not
yet waived"; it is precised here as the share still in the deferred period at the valuation
instant. Held as the incidence, the `lag − 1` months of each deferred period already run
would be run again at the recovery rate of the day, so that a rate changed at the
valuation date would reach back over them; held so, only the months still to run take it.
Income protection's claim cohorts take the same form.

A cohort seven months back or more has entered the waived share already; one before issue
there is none of. A point in force with the rider holds one row for each of its last
`min(6, duration_mth)` months, and none otherwise; `Data` refuses a row for a point the
table lacks, without the rider, at a lag before issue, twice, or with a share that is not
one, and a point whose waived share and deferred shares sum past 1, naming it, summed as
the active share sums them, so that what it passes opens the active share at 0 or more;
and `proj_len()` refuses a point that does not hold exactly its lags, by their count and
by its last, naming it, since the deferred period is the product's Reference. The
pipeline and the waived share are history, read from the extract: a model that
recomputed them from `wop_inc_rate` would pass the splice, which recomputes them alike, so
a test writes them off the rate's path and projects through them, another changes the
recovery rate at the valuation date (UKLIB-SEC-PLAN.md K14), and a third holds the
committed ones to a three-state ladder rebuilt month by month from the rates.

`lapse_cum_init` is the selective-lapse ratio as `Term_UK_S` defines it, a share of the
policies issued, so the count does not move it. Its increments are a share of the issued
cohort too, which a point in force does not count; `Term_UK_S` divides each month's lapses
by the count its frame opened with, which on a point it restates in force is the count in
force, not the cohort issued, and its deaths under the loading part from the projection
from issue by up to 10% (UKLIB-SEC-PLAN.md G2). Here `cohort_frac(t)`, the share of the
issued cohort in force, rebuilds the cohort from the opening state: every policy issued is
still in force, has died or has lapsed, since none expires before the end of cover, so the
policies issued are those in force with the deaths since issue, `1 + fib_cum_init` per
policy in force, over the share that has not lapsed, `1 − lapse_cum_init`. The ratio then
grows by `cohort_frac(t) (1 − q_m) w_m` a month, with no count in it, which is
`Term_UK_S`'s `pols_lapse(t) / pols_if_init()` on a point that counts one policy issued.

| `Term_UK_S` | `Term_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_inforce` (whole years) | `duration_mth` | The policy clock, in months, any month of a policy year; the S column is dropped |
| — | the seven state columns and the pipeline | `Term_UK_S` restarts each where its frame opens: the lapse ratio at 0, the ledger and its streams at 0, the waiver with none waived and none in the deferred period, and the factors at 1; and re-derives the commission paid at issue from today's rate |

The columns carried over are read as `Term_UK_S` reads them. For a policy in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry`, `joint_age` | years, age nearest birthday | issue, not the valuation date: `age(0, life)` is the attained age there |
| `shape`, `sex`, `smoker`, `joint_sex`, `joint_smoker`, `mort_basis` | codes, as in `Term_UK_S`'s table | issue |
| `policy_term` | whole years | issue |
| `sum_assured`, `fib_income`, `premium_mth` | pounds, the amounts at issue | issue: on an indexed point the year's cover and premium are these times the factors |
| `sched_rate` | a rate a year | issue: the decreasing schedule runs from issue on the policy clock |
| `joint_first_death`, `indexation`, `wop` | True or False | issue |
| `premium_mode` | monthly or annual | the mode billed over the frame; an annual premium falls on the policy anniversary |
| `fib_commute_rate` | a share | an assumption, not a fact about the policy |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the seven in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, which set to 0 refuses future new
business altogether; each state column is a number in its range; a point not yet in force
holds the issue values, 0 for the ratio, the deaths, the streams, the waived share and the
commission, and 1 for the factors; a point in force 12 months or fewer holds factors of 1;
each flag is True or False; each code is one `Term_UK_S` knows; the ages and the term are
finite numbers, the amounts and the schedule rate zero or more, and the commutation share
from 0 to 1; a joint point has a second life; indexation is elected on the level shape
alone; the factors are 1 without indexation, the waived share 0 without the waiver, and
the streams 0 off the family income benefit; and the streams in payment are no more than
the deaths since issue. `Term_UK_S` meets most of these only when a projection reaches
them, and some never: a blank flag reads as True, and one stray word in a flag column
turns every `False` in it to text that reads as True.

A point whose cover had ended by the valuation date, `duration_mth ≥ 12 × policy_term`,
reads, but `proj_len()` refuses it, naming the point: the end of cover is the product's
rule, not the table's. So does a point the contract does not write
([`product-spec.md`](product-spec.md)): a term above 50 years, `Projection.policy_term_max`,
or 40 on the family income benefit, `policy_term_max_fib`; a life issued below 18,
`issue_age_min`; or a life whose cover runs past attained age 90, `expiry_age_max`, or 70
on the family income benefit, `expiry_age_max_fib`. Each is a lower-case Reference, the
contract the compiled model's caches are sized from (*The compiled model*): a frame of at
most 600 months and the horizon, ages from 18 to 89 on the mortality table, a schedule of
600 months and an annuity-certain of 480. None is `expiry_age`, the U.S. tail's name,
which `Term_UK_S`'s tests hold absent. A loop over the block meets such a row only when it
reaches it, after projecting the points before it, so `run_sec.py --block` asks every
point for its frame before it projects any, and stops before it prints anything.

The assumption tables are checked before a value of them is read, each in the cell the
projection takes its extent from: `Data.mort_age_first` and `mort_age_last` for the
mortality table, whose four groups, M and F by N and S, must run over the same ages
without a gap or a repeat, each rate a number from 0 to 1; `Data.select_last_duration` for
the select factors, durations from 0 without a gap, each factor a number, zero or more;
and `Data.lapse_last_year` for the lapse table, policy years from 1 without a gap, each
rate from 0 to 1. A key is read by its value, so an age written `35.0` is 35. Each refusal
names the file, the column and its lines. A read past a table, an attained age outside the
mortality table or a select duration past the select table, is refused by the one cell
that reads the table, naming the point, where `Term_UK_S`'s lookup raised `KeyError`.

## The model points

No row of `model_point_table_sec.csv` or of `wop_pipeline_sec.csv` is typed by hand. Every
one is generated from `Term_UK_S` and its table by `tests/uk_sec_support.py`, from the
`Term_UK_SEC` entry in its `SEC_SPECS`, and the tests regenerate both and compare, so an
edit to a `Term_UK_S` row reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py Term_UK_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 7 | twin | S points 1 to 7 | issued at `t = 0`: `Term_UK_S`'s worked example and its shapes, bases and options |
| 8 | twin | S point 8, in force at S month 60 | in force five years, opened where `Term_UK_S` opens it: nothing lapsed, no ledger, no waiver, no index step |
| 9 | derived | S point 5 at S month 60 | the indexed point on its fifth anniversary, its factors those of policy year 5, the anniversary's step its month 0's |
| 10 | derived | S point 3 at S month 66 | the family income benefit mid-year, its streams in payment |
| 11 | derived | S point 7 at S month 66 | the waiver point after its select period, a share waived and six months of deferred lives in the pipeline |
| 12 | derived | S point 7 at S month 4 | the waiver point inside its deferred period, four months of deferred lives and none waived |
| 13 | derived | S point 1 at S month 299 | in its last covered month: a one-row frame |
| 14 | future | S point 7, 13 months on | to be issued at `t = 13` |

A derived row's `policy_count` is the count `Term_UK_S` carries into that month, its
`pols_if(d)`, and its state what S carries there, so the row continues the S projection
from there: point 9 opens with 0.685393 policies, 31.2% of the cohort lapsed, and cover
and premium factors of `1.03^4` and `1.045^4`, which it steps at `t = 0`, as S steps them
in month 60. Its `policy_id` is the S row's with the month appended, `TA-000005-M60`, and
a future row's carries the months to issue, `TA-000007-F13`. Row `t` of a generated point
is month `t + source_mth` of its S point. The pipeline holds point 11's six lags and point
12's four.

An indexed point that `Term_UK_S` opens in force has no twin. S opens an in-force frame
on an anniversary only, at index factors of 1, and takes its first step at the next
anniversary; this model takes an anniversary at the valuation date as month 0's own step,
from factors `Data` holds to 1 or more, so the twin would be one step above S in every
month of its frame: made indexed, S's point 8 would have a twin paying 154,500 at
`t = 0` against S's 150,000. So the generator refuses to write it, naming the point, and a
test holds the refusal. S's own point 8 is not indexed, and a row restated from such a
point at a later month is S's, its factors read in the month before.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` keeps
`Term_UK_S`'s three timings and adds `basiclife/BasicTerm_SE`'s `BEF_NB`, each an int code
named as `Term_UK_S`'s text, in the order of its instant within the month (*The compiled
model*):

- `BEF_NB`, 0, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, 1, that count plus `pols_new_biz(t)`, before month `t`'s decrements, which
  `pols_if(t)` returns;
- `BEF_LAPSE`, 2, after the month's deaths, before its lapses;
- `AFT_DECR`, 3, the end of the month, after its deaths and lapses, which is `BEF_NB` at
  `t + 1` exactly, and 0 from the last covered month on.

Any other timing raises. The survivors carried into month `t` are those of month `t − 1`'s
`BEF_DECR` count, which `BEF_NB` forms itself, as its own value at `t − 1` plus that
month's new business, exactly the sum `BEF_DECR` returns. So the chain of calls from
month `t` back to `t_entry()` is one cell a month, where `Term_UK_S`'s `pols_if` chain
runs three. On a model just read, a cold `net_cf` in the last month runs 11 cells deeper
than one a month, on every committed point and at the contract's longest cover, a 50-year
term from issue age 18, issued now and 120 months on; each other chain, the lapse ratio,
the cohort's share, the active and the waived shares and the deaths since issue, is one
cell a month too.

The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. Joint first death is still one policy decremented by `1 − (1 − q1)(1 − q2)`,
and the policies paying premium are `pols_if(t) (1 − u(t))`.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < term_mths()`, `Term_UK_S`'s own frame from
issue on the policy clock, and outside it, before issue and from the end of the term on,
every count is zero, and so every cash flow. No count evaluates a decrement rate there,
and no table is read at a select duration, a policy year or an attained age the policy
does not have: `select_factor`, `mort_rate_base`, `lapse_rate_base`, the benefit, the
commuted value, the premium and the factors are zero outside cover, before any table or
rate is read.

## Departures from Term_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read of a contractual schedule at a month passed as `t` is a read at the policy month or
year, and each recursion opens at `t_entry()` from the opening state. Where `Term_UK_S`'s
test would have stayed correct on the valuation clock, it moved anyway, so that cover has
one definition. Fifteen cells are new with running in force, and seven more with
compiling, `point_id`, the shape's three flags, `mort_group`, `prem_cycle` and
`is_select_basis` (*The compiled model*); two of `Term_UK_S`'s, `proj_start` and
`duration_inforce`, are gone, `duration_mth` replacing both. The twin identity names them
as dropped, and a cell of `Term_UK_S`'s that this model lacked without saying so would
fail it.

| Cells | `Term_UK_S` | `Term_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len` | `term_mths()`, from issue | `term_mths() − duration_mth_init()`, from the valuation date; raises past cover, outside the contract's bounds, on a short pipeline and, on a waiver point, on a waiver rate outside 0 to 1 or a share waived before the deferred period has run | The frame starts at the valuation date |
| `age_at_entry`, `sex`, `smoker`, `age`, `mort_rate_base`, `mort_rate_life`; `mort_group`, new | `life=1`, a default | `life`, no default; every call passes 1 or 2, positionally | A compiled model declares a defaulted parameter as `long long life=*`, which the C step's typing guard would read as a parameter of that name; modelx keys `Term_UK_S`'s `age(t)` as `(t, 1)`, so the twin identity pairs the cells as before |
| `pols_if`, `pols_if_at`, `pols_if_init` | a recursion through `"AFT_DECR"`, three cells a month, from the column's 1.0 at `proj_start()` | `BEF_DECR`, one cell a month from `t_entry()`; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `pols_maturity`, `AFT_DECR` | at `t = proj_len() − 1` | at `duration_mth(t) = term_mths() − 1` | One definition of cover, on the policy clock |
| `lapse_cum` | 0 at `proj_start()`, then lapses over the count S opened with | `lapse_cum_init()` at `t_entry()`, then `cohort_frac(t − 1)` times the month's lapse probability | The ratio carried in, and a share of the cohort issued, which no count moves |
| `fib_cum` | 0 at `proj_start()` | `fib_cum_init() × pols_if_init()` at `t_entry()` | The deaths since issue at the valuation date |
| `claims(t, FIB)`; `fib_streams`, new | `(1 − c) I [D(t) + FIBcum(t)]` | `I [(1 − c) D(t) + fib_streams(t)]`, the streams opening at `fib_streams_init() × pols_if_init()` | The streams in payment are history, which a take-up changed at the valuation date does not commute; S's number at a take-up that never changes |
| `wop_active_frac` | 1 at `proj_start()`, then `act(t − 1)(1 − inc_m) + (1 − act(t − 1)) rec_m` | `1 − wop_waived_frac_init() − Σ wop_deferred_init(lag)` at `t_entry()`, 1 on a point not yet in force, then the same chain; 0 outside cover | The lives active at the valuation date are what the waived share and the deferred period leave |
| `wop_waived_frac` | 0 at `proj_start()`, no entrants from before it | `wop_waived_frac_init()` at `t_entry()`; entrants from before it, `wop_deferred_init(lag) (1 − rec_m)^t`, from after issue | The waived share and the deferred period carried in, at the valuation instant |
| `idx_factor`, `idx_prem_factor` | a step per anniversary since `proj_start()`'s, from 1 | `idx_factor_init()` and `idx_prem_factor_init()`, then a step for each anniversary from month 0 on, month 0's own among them | The increases given before month 0 are history; an anniversary at the valuation date is the projection's, at the day's `rpi_rate` (*The in-force interface*). So an indexed point S opens in force, on an anniversary, at factors of 1 and with no step there, has no twin, one step above S throughout, and the generator refuses to write one (*The model points*) |
| `premium_pp` | an annual premium where `t % 12 == 0` | where `duration_mth(t) % 12 == 0` | An anniversary is a policy month |
| `fib_commute_pp` | `I a(N − t)` | `I a(N − duration_mth(t))` | The months left to the end of the term |
| `benefit_pp`, `select_factor`, `mort_rate_base`, `lapse_rate_base`, the counts | unguarded: no `Term_UK_S` frame has a month outside cover | zero outside cover, before any table or rate is read; the tables' extents from `Data`, a read past them refused by name | Before issue S raises `KeyError` on the tables, and `B(k)` at a negative month exceeds the sum assured without a word |
| `inflation_factor` | `1.03^duration(t)`, from issue | `1.03^(t // 12)`, from the valuation date | Unit costs in valuation-date pounds |
| `expenses`, `commissions` | acquisition and the initial commission on `pols_if(t)` at `t = 0`; renewal from `t ≥ 12` | on `pols_new_biz(t)`; renewal from `duration_mth(t) ≥ 12` | A point in force bears no acquisition, one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `comm_init_pp` | `comm_init_rate × 12 P_m × idx_prem_factor(0)` | on new business `comm_init_rate × 12 P_m`; in force, `comm_init_pp_init()` | The issue premium, S's month 0 not being the issue month on a point in force; and what a policy in force paid is history, which a rate changed at the valuation date does not move |
| `comm_clawback` | `t + 1` months in force | `duration_mth(t) + 1` | The window runs from issue |
| `check_pols_roll_fwd_resid` | `pols_if(t + 1)` | `pols_if_at(t + 1, BEF_NB)` | The next month's new business is no part of month `t`'s movement |
| `check_fib_ledger_resid` | `(1 − c)` of the deaths summed from `proj_start()` | the opening streams, then `(1 − c)` of the deaths summed from `t_entry()` | The rebuild starts from the streams in payment at the valuation date |
| `check_pols_roll_fwd`, `check_fib_ledger` | `range(proj_start(), proj_len())`, tolerance on `pols_if_init()` | `range(proj_len())`, tolerance on `policy_count()` | The frame from the valuation date; S's `pols_if_init` is 0 on new business here |
| `result_cf` | `range(proj_start(), proj_len())` | `range(proj_len())` | Row 0 is the valuation month |
| `result_pols` | — | `pols_new_biz` added, the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `claims` | `claims(t, kind=None)`, the kinds by name and, with no kind, their total by `sum` | `claims(t, kind)`, no default: the codes `DEATH`, `FIB` and `LAPSE`, and the total `ALL`, written left to right | A default and `None` do not compile, and the total is `sum`'s to the last bit (*The compiled model*); the twin identity compares `Term_UK_S`'s `claims(t)` with `claims(t, ALL)` |
| `sex(2)`, `smoker(2)` | `invalid life` on a single life | the column as read, NaN where blank | Reporting cells, whose type the sample traces on a blank second life, so that each compiles to a Python object; no projection cell reads them, `mort_group` taking each life's row of the mortality table |
| `annuity_certain_factor` | `m` where the annual rate is 0, else the closed form | `m` where the monthly rate is 0, else the closed form; a rate not a finite number above −1 refused on a family income benefit point by `proj_len()` | At a rate whose monthly equivalent rounds to 0, S divides by zero: 1e-17, where `1 + r` is 1, and 1.1e-16, where it is not; at −1 or below, or not finite, it raises, goes complex or gives 0 or NaN without a word |
| `select_factor` | `.loc` on the table, `KeyError` past it | an array read by the select duration, checked against the table's extent either side first, and refused by name | A negative duration, under a negative `select_period`, would read the array from its end without a word |

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. Point 8 carries that expense in valuation-date pounds, so its `expenses(t)` is
`Term_UK_S`'s `expenses(60 + t)` divided by `1.03^5`. Its `pols_if`, `premiums`, the three
claims columns, `claim_expenses` and `commissions` are `Term_UK_S`'s from month 60 on.
Point 14 is `Term_UK_S`'s point 7 thirteen months on in those columns too; its maintenance
expense is `1.03^(t // 12 − (t − 13) // 12)` above S's at each `t`, and its acquisition
£150 exactly.

`mort_rate_life` caps the annual rate at 1, written `min(q, 1.0)`, the product first and
the bound second, as `Term_UK_S` writes it, so that a NaN stays NaN where `min(1.0, q)`
would read it as certain death; wherever `q` is a number the two are the same float. No
shipped rate comes near it, the largest being 0.0077, and `Data` refuses a table rate past
1; the product can pass 1 through the selective-lapse loading, which a test shows. The
lapse rate's bound keeps `Term_UK_S`'s order, `min(1.0, …)`: it is no cap on mortality.

The waiver's incidence and recovery, `wop_inc_rate` and `wop_rec_rate`, are each one
Reference, with no factor and no annual-rate cell, so no cap reaches them, in `Term_UK_S`
or here, and this model keeps `Term_UK_S`'s formulas, `1 − (1 − r)^(1/12)`. Past 1 that
has no real value, and `Term_UK_S` projects a complex number; below 0 it is negative. So on
a waiver point `proj_len()` refuses either rate outside 0 to 1, or NaN, naming the point
and the Reference, where it refuses a negative deferred period; 0 and 1 are accepted, and
a point without the rider reads neither.

The family income benefit's commutation discount, `fib_commute_disc_rate`, is one
Reference too, which `Term_UK_S` reads unchecked in `annuity_certain_factor`,
`[1 − (1 + r)^(−m/12)] / [(1 + r)^(1/12) − 1]`: at −1 the power divides by zero, below it
has no real value, which S projects as a complex number, and an infinite rate gives a
factor of 0, and NaN one of NaN, without a word. So on a family income benefit point
`proj_len()` refuses a rate that is not a finite number above −1, NaN and both infinities
among them, naming the point and the Reference; a point of another shape reads no
discount. And the factor tests the monthly rate for 0, where S tests the annual one, as
`benefit_sched` tests its own monthly rate: at 0 both give `m`, the closed form's limit,
and so does this model at a rate whose monthly equivalent rounds to 0, where S divides
by zero: 1e-17, where `1 + r` is 1, and the least float whose `1 + r` is not 1,
1.1102230246251568e-16, whose twelfth root still rounds to 1. Within about 2e-8 of −1 the
power passes the largest float at the longest commutation, and S and this model raise
Python's `OverflowError`.

**The incidence falls on the active lives, in both models.** The waiver recursion of
`Term_UK_S`'s technical notes took each month's incidence from `1 − u(t − 6)`, which
counts the lives already in their deferred period among those who can fall ill, and both
models kept it, so that the twin identity and the splice held, until the repository's
owner decided to fix it in both (UKLIB-SEC-PLAN.md §6.1, *Record — M1*). Each life in
force is active, deferred or waived, and a deferred life and a waived one recover to
active alike, so the active share, `wop_active_frac`, follows a chain of its own,
`act(t + 1) = act(t)(1 − inc_m) + (1 − act(t)) rec_m`, and the entrants of month `t + 1`
are `inc_m act(t − 6) (1 − rec_m)^6`. Here the active share opens at what the waived
share and the pipeline leave, and each lag of the pipeline is
`inc_m act (1 − rec_m)^(lag − 1)` of its month, `Term_UK_S`'s fixed incidence, so the
twin identity and the splice hold with no exemption. A three-state ladder rebuilt month by
month from the rates, the deferred lives lag by lag, is both models' to rounding: within
1e-15 on S's waiver point at the shipped rates and at incidences of 0.856 and 1. Against
the old base, on the four waiver points, the twin of S's point 7, the rows restated at 66
and at 4 and the row issued 13 months on, the waived share falls by up to 1.38e-5, 0.182%,
and the entrants by up to 0.184%; premiums rise by £0.0702 over each frame, 0.0011%,
renewal commission by £0.0018 and `net_cf` by £0.0684, and on the row at 66, whose frame
is 66 months shorter, by £0.0545, £0.0014 and £0.0532. No other point moves.

The waived share no longer leaves 0 to 1, and `wop_waived_frac` no longer refuses one. The
three shares partition the in-force, so at rates from 0 to 1, which `proj_len()` holds
them to, and from an opening state whose waived and deferred shares `Data` holds to 1 or
less, the share stays inside 0 to 1: at an incidence of 1 and no recovery, the worst the
rates allow, every waiver point's share reaches 1 and stays there, to the last bit, and
no premium is collected after. On the old base the share passed 1 from an incidence of
about 0.8552 and reached 7.9e12 at 1, and the cell refused it; now it peaks at 0.652 at an
incidence of 0.856 and at 0.806 at 1, and the twin of S's waiver point is S's in every
cell. Rounding alone can take the share past 1, by a few units in the last place, at an
incidence near 1 with no recovery, 1.0000000000000002 at 0.999999 a year, in `Term_UK_S`
too: a refusal would refuse those inputs for their last bit and reach no other, so it is
dropped, not kept unreachable. Restated in force, such a state is refused, by that last
bit, by `Data`, whose rules hold the waived share, and its sum with the deferred shares,
to 1 (*Tests*).

A waived share is also refused on a point in force no longer than the deferred period, a
state `Term_UK_S` cannot reach: its first incapacity has not yet run the six months. The
deferred period is a Reference of the projection, which `Data` cannot read, so the rule
is `proj_len()`'s, beside the pipeline's length, which reads it too.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and no number: what its reports computed on
each committed point was frozen before the change, and they still compute it, to 1e-12 of
each column's largest value (*Tests*, below), refrozen once since for the waiver's
incidence on the active lives, a change of numbers on the four waiver points alone; and
every value the in-force model cached on the committed points and on the full splice grid
was this one's, bit for bit, when the change was made. Cell by cell, at every argument a full
modelx sweep evaluates, the compiled model computes what modelx computes, bit for bit, on
the committed points, on the points of the splice grid, which take the branches they do
not, at the contract's longest covers, on points where the cap on mortality binds and at a
commutation discount of 0, of 1e-17 and of 1.1e-16. The compile tests hold it so on
x86-64, and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py term_assurance                    # in place, beside the model
python build_sec_cy.py term_assurance --out /tmp/term    # elsewhere, with the CSVs
```

The tool exports the model to `Term_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `Term_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/term_assurance")      # the directory holding the build
from Term_UK_SEC_nomx_cy import mx_model as model
model.Projection[7].result_cf()                    # point 8, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about a minute with gcc, 62 s here, and needs modelx-cython, which needs a C
compiler, so the models do not require it: `pip install modelx-cython`, or
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
taught first (USLIB-SEC-PLAN.md R1 to R17):

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[7]` is point 8, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `policy_term()` is `int(data.policy_term()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The seven columns of opening state are
  vectors too, and so is the waiver's pipeline, by point and lag.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the number it selects, for every point at once: the shape into three flags,
  `is_level`, `is_decreasing` and `is_fib`; each life's sex and smoker status into the
  row of the mortality table they select, `mort_group` and `joint_mort_group`, M N 0,
  M S 1, F N 2 and F S 3; the premium mode into the months between instalments,
  `prem_cycle`, 12 annual and 1 monthly; the mortality basis into `is_select_basis`;
  each true-or-false column, `joint_first_death`, `indexation` and `wop`, into a 0/1
  flag; and a single life's blank second age into 0 beside the flag `joint_first_death`,
  so that no formula tests for NaN. Each decodes as `Term_UK_S` reads the column, which a
  test holds on every value a column can hold, and what it cannot hold it refuses (below).
- **Tables indexed by integers.** The mortality table is `mort_table_array`, by group and
  attained age, padded from age 0 so that the index is the age; the select factors are
  `select_factor_array`, by select duration; the lapse rates `lapse_table_array`, by
  policy year, padded at year 0; and the pipeline `wop_deferred_init`, by point and lag,
  padded at lag 0 and past each point's last lag, beside each point's count of lags and
  its last. The padding holds NaN, and nothing reads it. The one cell that reads each
  table checks its key against the table's extent first: `mort_rate_base` and
  `select_factor` either side, and `wop_deferred_init` from lag 1 to the point's last.
  `lapse_rate_base` holds the policy year at the table's last above, as `Term_UK_S`
  does, and reads in cover alone, where the year is 1 or more.
- **Codes.** A timing or a kind, which `Term_UK_S` spells as text, is an int Reference
  named as the text: `BEF_NB = 0`, `BEF_DECR = 1`, `BEF_LAPSE = 2` and `AFT_DECR = 3`,
  in the order of their instants within the month, and `DEATH = 0`, `FIB = 1` and
  `LAPSE = 2`. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`. A
  string argument would give the cell a dictionary for a cache, where a code indexes a C
  array, so codes are numbered from 0 without a gap.
- **The claims total, a code of its own.** `Term_UK_S` totals the three kinds as
  `claims(t)`, its `kind` defaulted to `None`, with Python's `sum`. A default compiles as
  a keyword parameter the typing guard refuses, and `None` is no C integer, so the total
  is `claims(t, ALL)`, `ALL = 3`, and `net_cf` reads it. It is written out,
  `0.0 + claims(t, DEATH) + claims(t, FIB) + claims(t, LAPSE)`, left to right, which is
  `sum`'s float wherever at most two of the three are non-zero; `sum` compensates since
  Python 3.12, and so parts from the plain sum only where a third term is added. The lapse
  kind is 0.0 in every month, so the two cannot part, and a test holds the total to
  `Term_UK_S`'s by its bits, on a month where both the lump sum and the instalments are
  paid among others. The ledger check's residual sums the deaths since `t_entry()`,
  hundreds of non-zero terms, so it adds them in a loop compensated as `sum` compensates
  them, the Neumaier sum, and returns `Term_UK_S`'s number to the last bit too. On Python
  3.11, whose `sum` adds left to right as `Term_UK_S`'s ledger does, `Term_UK_S`'s
  residual is 0 in every month and parts from this one, and the test of its bits skips
  there, naming Python 3.11. Neither keeps the generator `Term_UK_S` passes to `sum`,
  which a compiled cell would run as a Python object.
- **Reporting cells stay Python.** `model_point()`, the label accessors `shape()`,
  `premium_mode()`, `mort_basis()`, `sex(life)` and `smoker(life)`, and the two reports
  return a table row, text and DataFrames, for a reader, for `run_sec.py` and for the
  comparison with `Term_UK_S`. No other cell calls them, so they cost the projection
  nothing. The first three validate their column, as `Term_UK_S`'s do, so each returns
  text or raises, and compiles to `str`. `sex(life)` and `smoker(life)` return each
  life's column as read, a single life's blank second life as NaN, and compile to Python
  objects, as the sample traces them (below), so that each returns what modelx returns.

The `Data` docstring lists its 39 vectors, arrays, extents and counts, each with the
column or file it comes from. The six readers stay Python, returning DataFrames and a
path, and no `Projection` cell but `model_point()` reads them. Every other cell of
`Projection`, 83 of its 91, returns a C `bint`, `long long` or `double`, and caches a single
value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 722 by `t`, of `double`, `long long` or `bint` | the 38 cells of `t` alone: every count, rate, factor, benefit, premium and cash flow; the policy clock, its years and the select duration; the checks' residuals; and the flag `is_active` |
| a C array of 722 by 4 | `pols_if_at(t, timing)`, `claims(t, kind)`, `age(t, life)`, `mort_rate_base(t, life)` and `mort_rate_life(t, life)` |
| a C array of 600 by policy month | `benefit_sched(k)` and `wop_deferred_init(k)` |
| a C array of 481 by months left | `annuity_certain_factor(m)` |
| a C array of 4 by life | `age_at_entry(life)` and `mort_group(life)` |
| one `bint`, `long long` or `double` | the 35 other cells without a parameter: the point's numbers, flags and opening state, the ends of its frame, and the two checks |
| a Python object, or `str` | the eight reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the two labels
of a life's.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the two reports
and the two checks on every committed point, and then the cells no report reaches:
`model_point()` and the five label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; and the count at `AFT_DECR`, which `Term_UK_S`'s count chain
read and this model's carries at `BEF_NB` instead, in every month of the frame and the
month after it. It runs the committed points alone: the export reads the CSVs of the
directory the build is made in, which in place is the product directory. The committed
points leave branches untaken: an annual payer, a family income benefit commuted in part,
an indexed waiver point, the decreasing shape at a schedule rate of 0, a joint life who
smokes, the clawback window open, the cap on mortality. That still types every cell,
because every branch of a cell returns the one type its others return, a count a float in
every branch, and on points that take those branches the compiled model computes
modelx's numbers (above). The two life labels are typed from more than the committed
points: the sample also calls `sex` and `smoker` of each life on a copy of the first
point, a single life, with its second life blank, written to a temporary directory and
read by a second instance of the export, so that each compiles to a Python object, which
a test holds in the sample's code. The sample also raises the recursion limit, which
modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 722 | 721. The longest frame is the longest term, 50 years, `policy_term_max`, issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 50 + 120 = 720 months, `t = 0 … 719`, and the month after, 720, whose roll-forward residual reads the count carried into 721 |
| `t`, `timing`; `t`, `kind`; `t`, `life` | 722 by 4 | `t` as above, by the four timings, by the three kinds and the total, and by the two lives. Every 2-D cache of a model shares one inner width, the widest: Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `life` | 4 | 2. Widened to the same 4, so that a life the cells refuse by their own formula, 0 or 3, is refused as in modelx, `ValueError("invalid life")`, in every per-life cache |
| `k` | 600 | 599, the decreasing schedule's last policy month on a 50-year term; the waiver's pipeline reads a lag below the months of cover |
| `m` | 481 | 480, the months left in the issue month of the family income benefit's longest term, 40 years, `policy_term_max_fib`, where `fib_commute_pp` reads the annuity certain |

`proj_len()` refuses a term above `policy_term_max` or, on the family income benefit,
`policy_term_max_fib`, in modelx as compiled, and `Data` a point issued more than
`future_horizon_mth` months ahead, so no report on a point the model projects runs past
these caches. Those three References are the contract the sizes are derived from; the
ages bound none, since an age indexes `Data`'s mortality table, not a cache. Raise a
maximum term or the horizon, and a report runs past the caches in the compiled model
alone: `t`, `k` or `m` past its size raises `IndexError`, naming nothing, where modelx
projects. Each needs the sizes derived again, as `spec_sec.py` derives them, and a
rebuild; a longer horizon, `t` raised to 12 × 50 + the horizon + 2.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as `held` in `proj_len()`, stays a Python object, though the cell is
typed `long long`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of every
decrement here, is a complex power, which gcc computes with `cpow` rather than `pow`, and
its last bits can differ from Python's; and gcc fuses a multiply and an add where the
target has the instruction, one rounding where Python rounds twice. The tool's docstring
has the detail, and uslib's
[`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the measurements
that put each there. With all four, every compiled value here agrees with modelx bit for
bit. The compile tests hold each directive in the module's first line, and a static test
holds the tool's line to the two and no other: `cdivision=True` would make `//` on C
integers truncate where Python floors, which only a full sweep met, through point 14's
`duration(t)` before issue, and `boundscheck=False` or `wraparound=False` would change what
an `idx` outside the table reads.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 520,912
bytes, the type's basic size, which holds every cell's cache, and deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a test runs the compiled runner on the committed points, whose pipeline names them,
and finds no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 26. What it needs
is stack. That call, a cold `net_cf` in the last month of the longest cover, the waiver
point on the select basis issued at 18 on a 50-year term, now or 120 months on, runs the
count chain back to `t_entry()`, 611 cells deep in modelx, one cell a month and 11 more,
which a test holds, and compiled with gcc, at the shipped References or with every switch
that ships off on, it needs between 144 and 160 KiB: it ran on a thread of 160 KiB and not
of 144. So do the decreasing shape and the joint point, 50 years from 18, and the family
income benefit, 40 years from 30, which runs 491 cells deep in modelx, needs between 96
and 128. The waiver point needed between 192 and 208 KiB until its waived share stopped
refusing a share outside 0 to 1, with the fix of the waiver's incidence base: the
refusal's message, built in the cell, enlarged the C frame of each month of the waived
share's chain. The active share's chain, which the waived share reads one cell deep, after
its own month before, adds no depth, in modelx or compiled. A test runs every shape at its
longest cover in a thread of 1 MiB, the stack Windows gives a program's main thread unless
the program is linked for more, and again on the main thread, which is where
`run_sec.py --cython` runs. MSVC's frames may be larger than gcc's, and the `cython_uk` CI
job, which runs the test on Windows too, is the check on them. The export recurses in
Python instead: the same call needs a recursion limit of 1,246 there, and the reports and
checks, which run in ascending `t`, need 128, so `sample_sec.py` sets 5,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message: each
malformed row of the table or the pipeline, each opening state whose waived and deferred
shares sum past 1, each assumption table a reader cannot read, each point the frame
refuses, each waiver rate and commutation discount refused, a key read beyond a table,
either side, and what the vectors cannot hold, in a cell typed `long long` or `double` as
in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, and a
term, an age or a count of months as an int. So a rate written as an int, 2, or a bound
written as a float, 24.0, gives one message in both engines, which a test holds for each
Reference a refusal prints. A `select_period` written as a float, 3.0, reads the select
table at 3 in both. An int Reference is a C `long long` compiled, and a float set on it is
truncated as it is set, 48.5 to 48, where modelx computes with 48.5, so set each as a
whole number.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault: a `point_id` that is not a whole number, or is `2**53` or more in size; an issue
  age, a term or, on a joint first-death point, a second age `2**53` or more in size,
  which an int64 vector cannot hold whole and numpy would cast without a word; and, as
  since the in-force step, a code that names no shape, sex, smoker status, premium mode or
  basis, and a flag that is not True or False. A key written as a float, an age `35.0`,
  is read by its value, as `Term_UK_S`'s lookups match it.
- A key beyond a table, by the one cell that reads it, where `Term_UK_S`'s lookup raised
  `KeyError`: `point_id 1: mort_table.csv has no rate at attained age 18`, from
  `mort_rate_base`, on a table that starts at 20; a select duration past the table, or
  below it under a negative `select_period`, from `select_factor`; and a lag a point's
  pipeline does not hold, below 1 or past its last, from `wop_deferred_init`.
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: expense inflation, the two index
  factors, the decreasing schedule and the annuity certain each call Python's own power
  where theirs is infinite from a finite base, so that the compiled model raises the
  platform's message as modelx does (uslib's *Record — M22* form), rather than carry an
  infinity on. Only an input far outside the product reaches one: an inflation above
  about 140,000 a year, an index increase or step above about 2 million, a schedule rate
  above about 1.5 million, or a discount within about 2e-8 of −1; a test reaches each.
- A timing, a kind or a life no cell takes, by the cell, as `Term_UK_S`'s are:
  `invalid timing`, `invalid kind`, `invalid life`.

An argument outside a cache raises `IndexError` in the compiled model alone:
`net_cf(722)` or `net_cf(-1)`, which modelx answers with 0, the month being outside
cover; `pols_if_at(t, 4)` and `claims(t, 4)`, which modelx refuses as a timing and a kind
it does not take; `age_at_entry(4)`; `benefit_sched(600)` and
`annuity_certain_factor(481)`, which modelx computes. An `idx` past the last row is
refused in both, with an `IndexError` at the first read of a vector, and `Projection[-1]`
reads every vector at its last element in both, so it is the table's last point, under
that point's own `point_id()`; the compiled refusal test holds both against modelx.

An annual mortality above 1 is not refused but capped, in both: `mort_rate_life` caps the
product at 1, as `Term_UK_S` does (*Departures from Term_UK_S*, above), and a compile test
holds the two equal on points where the cap binds, new business and in force. A NaN
product would stay NaN through the cap, in both, which the compiled model computes as a
comparison that keeps the value unless the bound is smaller.

### Speed

`python tools/bench_sec_cy.py term_assurance` builds the model into a temporary directory
and times one block run on three engines: modelx, the export and the compiled model. Each
engine runs the committed table repeated, in a process of its own, as `run_sec.py --block`
runs a block, each point projected and then released, and the waiver's pipeline repeated
with it, each copy's rows under its own points. `net_cf` is `net_cf(t)` summed over the
frame, the projection alone, as `basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`;
`result_cf` is the report `run_sec.py` prints, which builds a DataFrame for each point.
Each run of the tool takes the fastest of three runs of each engine and loop. The tool was
run three times, and each time below is the median of its three, with the range of the
three beside it:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,006 | 0.181 ms (0.173–0.183) | 0.588 ms (0.567–0.634) | 87–88 MB |
| export | 602 | 2.31 ms (2.17–2.35) | 2.57 ms (2.50–2.76) | 87–88 MB |
| modelx | 126 | 76.8 ms (74.5–80.6) | 73.9 ms (73.2–78.2) | 100–101 MB |

On `net_cf` the compiled model runs 12.8 times its export (12.0 to 13.3 over the three),
and on `result_cf`, where building the DataFrame takes most of its time, 4.5 times (3.9
to 4.7); it runs 419 times modelx on `net_cf` (412 to 465) and 129 on `result_cf` (116 to
133). The ranges are the noise of a shared machine, about −3% to +6% on modelx and −4%
to +8% on the compiled report: within it modelx's `result_cf`, which does more, came out
faster than its `net_cf` in each of the three. uslib's `Term_US_SEC`, timed the same way
on its own points on 2026-11-02, ran 9.5 and 4.7 times its export. The release keeps a block flat: the compiled model's
peak grew by less than 0.1 MB over its 6,006 points in every run. Reading the five files
and building every `Data` vector and array for those points took 0.046 to 0.052 s, 858 of
the points with a pipeline that rule 8 sums in one walk, and asking every point for its
frame, the runner's first pass, 0.06 to 0.07 s. Every engine, loop and run summed `net_cf`
over a copy of the table to the same −33,525.29268, to 1e-9 relative.

Measured on 2026-11-23 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.30 GHz), a 1-minute load average between 0.79 and 1.24 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1 to 7, every
  cell of `Term_UK_S`'s agrees at every argument `Term_UK_S` evaluates in its own sweep,
  to 1e-9 relative with no absolute floor, but for `pols_if_init` and `model_point`, and
  `proj_start`, `duration_inforce` and `result_pols`, which the spec names with its
  reasons; a cell this model lacked would fail it. The ledger's residual,
  `check_fib_ledger_resid`, a rounding about zero, is compared at an absolute floor of
  1e-9, since at a take-up such as 0.3 the two models' sums round apart (*The in-force
  interface*). So `Term_UK_S`'s worked example, which
  `tests/test_term_assurance_uk.py` asserts to the penny and the in-force to six decimals,
  holds here with no number restated. The kinds and timings are compared as the codes of
  the same names, and `Term_UK_S`'s claims total, `claims(t)`, with `claims(t, ALL)`. The
  same suite holds the model to the conventions
  every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the `BEF_DECR`
  count, new business enters once at its `policy_count`, nothing happens before issue,
  and the in-force columns are present.
- **The splice**, in `tests/test_term_assurance_uk_sec.py`: each `Term_UK_S` point
  restated in force at months 1, 6 and 7 (the waiver's first entrants), 11, 12 and 13 (the
  first anniversary), 22, 23 and 30 (the selective-lapse ratio's crossing), 47 and 48 (the
  clawback window's end), 59 and 60 (the select period's end), 66, 120, 239 and 299,
  continues the S projection in every cell the two share but `proj_len`, and in both
  reports, to 1e-9 relative with no absolute floor; so does S's own point 8, in force at
  60, and restated at 66, 120 and 299. Every switch that ships off is on in both models:
  the selective-lapse loading at 0.25, rebroking at a market ratio of 1.25 and the
  four-year clawback; inflation, the one input on the valuation clock, is 0 in both. Five
  variants of S's points, in a copy of S's table that is never committed, reach what S's
  own cannot: an annual payer on the indexed point and a male smoker, the family income
  benefit commuted in half, the waiver point indexed, the decreasing shape at a schedule
  rate of 0, and a joint point whose second life is a male smoker. A core of 34 of the
  139 splice cases and 8 of the 21 future ones runs by default, and the full grid with
  `UKLIB_SEC_FULL=1`; a test asserts the core reaches every branch, opening-state
  column, kind of valuation month and side of every `min` and `max` the full grid
  reaches.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point is
  the S projection moved on, with zeros before issue and no rate evaluated there, and so is
  each variant issued a month on, the waiver point 13 months on and the indexed point 25.
- **How it computes**: on every row of the splice's grid, after its reports, its checks
  and every monthly cell at every month, no cell has been called at a negative month, none
  on the books read a month before `t_entry()`, none read a month later than `t + 1`, and
  none raised. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, the policy clock being a closed form, and every point's reports and
  checks run under modelx's recursion limit lowered to 40, which a recursion backward over
  the frame would exceed. And each chain, called cold in the last month at the contract's
  longest cover, runs one cell a month back to `t_entry()` and at most 16 more.
- **Counts**: the roll-forward closes; `result_pols()` is S's report with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, with every switch that ships off on,
  multiplies every flow and counted cell and moves no per-policy value, bit for bit, the
  lapse ratio and the cohort's share among them; and both checks, their tolerances scaled
  by the count, close on a million policies.
- **Validation and regeneration**: each malformed row of the table, 78 cases, each `2**53`
  bound at the bound among them, and an increase given on the first anniversary, the
  first-year rule's edge, which one month on is read, and of the pipeline, 18, is refused
  naming its point or its line, and so is a waiver point whose waived and deferred shares
  sum past 1, 4 cases more, by as little as a unit in the last place, where a sum of
  exactly 1 opens the active share at 0 and projects; the horizon is a Reference; a point
  past its cover, outside the contract's bounds or with a pipeline not exactly its lags, 8
  cases, among them none at all and a gap, is refused by `proj_len()`, each bound just
  inside it and each moved past a committed point, and `run_sec.py --block` refuses such a
  point before printing anything; so is a share waived before the deferred period has run,
  at its last month among them; a waiver point under a waiver rate a float outside 0 to 1,
  or NaN, is refused by the frame, where at 0 and 1 for either rate and at incidences of
  0.855 and 0.856 every waiver point projects its share inside 0 to 1 and the twin of S's
  waiver point is S's in every cell, and at an incidence of 1 with no recovery, the worst,
  every waiver point's share reaches 1 and no more; a family income benefit point under a
  commutation discount that is not a finite number above −1 is refused by the frame, S's
  own outcome beside it, where at 0 and −0.99 the twins of S's family income benefit
  points are S's in every cell, at 1e-17 and 1.1e-16 the factor is `m`, and at the float
  above −1 S and this model raise the same `OverflowError`; each assumption table a reader
  cannot read, 28 cases, is refused naming its lines, a repeated key with each of its
  lines, and a read beyond a table naming the point; keys written as floats read as
  `Term_UK_S` reads them; the edges of the interface and of each bound are accepted; every
  state `Term_UK_S` reaches, as shipped, under the splice's switches and where the cap
  binds, is accepted in force; and the committed table and pipeline are what `Term_UK_S`
  generates. Not every state S reaches at any rates is accepted: at an incidence of
  0.999999 a year with no recovery, far outside the product, rounding takes S's waived
  share a unit in the last place past 1, alone or with the deferred shares, and
  `Data.model_point_table`'s rule 6 and `Data.wop_pipeline`'s rule 8 refuse S point 7
  restated at 208 of its 239 months, from month 32. The rules are not widened for it: each
  refuses a state no policy can be in, by its last bit.
- **The product's own facts**: the two clocks on the shipped points; the committed rows,
  in force and issued later, continuing their S points at the shipped assumptions but for
  inflation; the lapse ratio carried on from the issued cohort, and the deaths it loads;
  each history column read, not recomputed, the index factors, the streams in payment, the
  commission paid at issue, the waived share and the pipeline's deferred lives, each
  written off its References' path and projected through, the active share opening at what
  they leave, the committed waiver state a three-state ladder's, rebuilt month by month
  from the rates, and the take-up, the commission rate and the recovery rate each changed
  at the valuation date reaching back over no month already run (UKLIB-SEC-PLAN.md K14);
  the RPI set to 5% at the valuation date of the indexed point on its fifth anniversary,
  whose factors are `Term_UK_S`'s at 3% in month 59, before the event, and whose fifth
  step is made at 5% at `t = 0`, each figure recomputed by hand, and of the same point
  restated on its first, which is `Term_UK_S`'s at 5% from month 12 in every cell;
  expense inflation on the valuation clock at the shipped 3%, which only this test sees;
  acquisition and the initial commission on new business alone; renewal commission and the
  clawback on the policy clock; an annual premium on the anniversary of a point valued
  mid-year; every guarded cell's value outside cover; the block; an extract without the
  generator's three columns, labelled otherwise, projecting the same numbers;
  `run_sec.py`'s numbers, for a point, the joint life among them, and for the block, and
  its sum, and its `--cython` stopping where no repository is above it; no cell's
  parameter defaulted; the docstrings, read through docutils as the docs build reads them
  where docutils is installed; and the shared input tables.
- **The cap**: on the anchor cell with its male non-smoker rates from age 50 at 0.96, in a
  copy of the table, under the splice's References, the product of the rate and the
  selective-lapse loading passes 1 from attained age 50, policy month 180. In both models
  `mort_rate_life`, `mort_rate` and `mort_rate_mth` are the float 1.0 there; every policy
  in force at the start of that month dies in it, and none is in force after it; the
  reports hold finite floats; and every cell the two models share agrees, issued now and
  12 months on, and restated in force the month before the cap, to 1e-9 relative with no
  absolute floor. And a NaN sent to the cap, through `mort_scale` or the loading's
  multiple, or to the RPI's floor and caps, stays NaN.
- **The C step's representation**, in modelx, in seconds: `claims(t, ALL)` is
  `Term_UK_S`'s total by its bits on every twin's month and on the family income benefit
  commuted in half, and so is `check_fib_ledger_resid(t)`, the Neumaier sum's residual,
  on the twins of S's family income benefit points and that same point, skipped on
  Python 3.11, whose `sum` adds left to right; every value each
  text column can hold decodes as `Term_UK_S` reads it, each fraction above .5 so that a
  decode that rounded would part, the mortality group's row holding S's rate at every
  age; each padded array holds NaN where no file does and nothing else, and its one
  reader refuses a key outside it on an extract labelled otherwise than by position; each
  `Data` vector is the int64 or float64 the `Data` docstring's table states, and each
  parameterless cell returns a Python number; `spec_sec.py`'s sizes and `sample_sec.py`'s
  recursion limit are what their comments derive, and the sample traces each life's
  labels on a blank second life; `run_sec.py --cython` rebuilds exactly when a source is
  newer; and a label the vectors cannot hold, or a timing, kind or life no cell takes, a
  single life's second issue age among them, is refused.
- **C2, the fingerprint**: on every committed point, each column of `result_cf` and
  `result_pols`, its sum over the frame, its largest absolute value and its values in five
  months, the first, the last and the three quartiles between, is what the model computed
  when its E step ended, to 1e-12 of the column's largest value, frozen at the end of the
  module by `tools/gen_sec_fingerprint.py` before the C step changed anything, and refrozen
  once since, alone, when both models' waiver came to take its incidence from the active
  lives, which moved the waiver points 7, 11, 12 and 14 and no other number. Measuring the
  factors before an anniversary at the valuation date, rather than after it, moved point
  9's opening factors and none of its numbers but by rounding, at most 5.2e-15 of a value
  of `net_cf`, which the freeze holds unchanged.
- **Compiled**, the tests marked `cython`, which compile the model once a session into a
  temporary directory and run it in child processes: in
  `tests/test_compiled_conventions_uk.py`, C3, the typing guard, on the declarations, the
  spec and the generated C; C4 on the committed points; and the release. In this model's
  module, C4, every cell at every argument a full modelx sweep evaluates, with every code
  no swept cell reads and both lives of every cell of a life (`_term_c4_also`, the spec's
  `c4_also`, which a test holds to asking each in every month, row by row, the codes and
  the lives each cell takes derived in modelx, not read from the test's own lists, and
  another to leaving no call of a life that computes uncompared), on the splice grid, at
  the contract's longest covers, issued now and 120 months on and in force in their last
  month, where the cap binds and on keys written as floats, and at a commutation discount
  of 0, 1e-17 and 1.1e-16; each life's label that is not text; the refusals, message for
  message, the overflows among them, the `IndexError`s past the caches and an `idx` past
  the table and of −1; each shape's deepest cold call on a 1 MiB thread and on the main
  thread; a Reference set late, which clears no cache; and `run_sec.py --cython`, which
  prints what modelx prints. In `tests/test_compiled_conventions_uk.py`, a static test
  holds the build tool's directives to the two.

```bash
python -m pytest tests/test_term_assurance_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_term_assurance_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k Term_UK_SEC
UKLIB_CYTHON_SHARD=term_assurance python -m pytest -m cython tests -q       # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R11]: #uklib-term_assurance-r11
[std]: #uklib-std
<!-- END generated citation links -->
