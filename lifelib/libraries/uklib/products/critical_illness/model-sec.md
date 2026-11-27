# In-Force Implementation Notes

**Status:** Draft, 2026-11-22. `CI_UK_SEC` is [`CI_UK_S`](model.md) taught to project from
a valuation date. Besides policies issued at that date, it takes policies already in force
there, in any month of their policy year, and policies to be written in the ten years after
it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is
the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model (UKLIB-SEC-PLAN.md U2).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `CI_UK_S` on another time axis, and it reads `CI_UK_S`'s assumption tables in place,
> every assumption unchanged: the benefit structure is sourced, and every rate is a
> **[std]** standardization, the diagnosis and mortality bases proxies shaped like the
> subscriber-restricted CMI tables [R8]. Replace them with company data and licensed tables
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/critical_illness/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/critical_illness/run_sec.py 9          # point 9: the reviewable point on its first review
python products/critical_illness/run_sec.py --block    # every model point, summed row by row
python products/critical_illness/run_sec.py 9 --cython # point 9 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the library's own `build_sec_cy.py` the first time, in about a minute, and
again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. Nothing the build leaves there is committed, and `.gitignore`
covers it.

The first prints the twelve rows `run.py` prints for `CI_UK_S`'s point 1, with the policy
counts behind them. Three lines to the same thing for point 9:

```python
import modelx as mx
model = mx.read_model("products/critical_illness/CI_UK_SEC")
model.Projection[8].result_cf()      # point 9, the table's ninth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `CI_UK_S`'s takes a `point_id`: `Projection[8]` is point 9, and its
`point_id()` says so. `result_cf()` has `CI_UK_S`'s columns — `pols_if`, `premiums`,
`claims_main`, `claims_ap`, `claims_child`, `claims_lapse`, `claim_expenses`, `expenses`
and `net_cf` — with one row per month from the valuation date, `t = 0 … proj_len() − 1`.
`result_pols()` sets out the counts behind it on the same rows: `pols_if`, `pols_new_biz`,
then the month's main claims and lapses in processing order, the expiries of the last
covered month, and `CI_UK_S`'s other six columns, the end-of-month count and the first
life's diagnosis and mortality rates, the policy's annual and monthly claim rates and the
annual lapse rate.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[8]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`. The runner is uslib Term's, and
`--build DIR` runs a build made elsewhere (*The compiled model*). The tool goes with the
library, into lifelib and into a `lifelib.create()` copy, so `--cython` builds there as
here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the term.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the lapse table's key, and
  `age(t, life) = age_at_entry(life) + duration(t)`, the pivot table's, as in `CI_UK_S`.
  `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion as long as the
  frame; the closed form needs no such chain of calls.

Point 9 is the reviewable point in force 60 months, valued on its first review. At `t = 0`
it is in policy year 6 at attained age 45, and its frame has 240 rows, `t = 0 … 239`;
`CI_UK_S` projects the same months as its rows 60 to 299. Point 13 is the indexed point to
be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is on the books
from `t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 313 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the diagnosis and mortality pivot rates at the attained age; the lapse table by policy year; the RPI increase on each anniversary; the premium reviews every 60 policy months from the fifth anniversary, and the shock lapse in the twelve policy months after each; the end of cover | expense inflation, `inflation_factor(t) = 1.03^(t // 12)`; the morbidity trend, `ci_trend_factor(t) = (1 + τ)^(t // 12)` |

Expense inflation and the morbidity trend run on `t`, stepping on each anniversary of the
valuation date, for every point alike (USLIB-SEC-PLAN.md D7; UKLIB-SEC-PLAN.md §9 item 4).
The maintenance charge is then in valuation-date pounds, and the diagnosis table states its
basis at the valuation date, trended from there: `CI_UK_S` trends it from issue, which on a
point in force would trend a basis stated today by the years the policy has already run.
The trend ships at 0, where the two clocks agree. The initial expense, £200 per policy
issued, is charged in the issue month and not inflated, as in `basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
points = range(len(model.Data.model_point_table()))
frames = [model.Projection[i].result_cf() for i in points]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`CI_UK_S` computes: every cell the two models share agrees, but two whose meaning changed,
`pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table. `CI_UK_S` charges the initial
expense on the count in force at `t = 0`, which on such a point is the count issued, so the
two agree at any count.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `CI_UK_S`'s columns, one
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s name, a policy
clock column, and six columns of opening state. Each state column is a factor, a rate or a flag,
so that `policy_count` is the one weight on every flow, and each is measured at the
valuation instant, the start of month 0, before any month-0 event. An event that falls at
the valuation date itself is month 0's, the projection's first, made at the References of
the valuation date, as it is on a policy issued then, and is not history (USLIB-SEC-PLAN.md
D6, precised at its M7): on a point valued on its anniversary, that anniversary's RPI
increase is made at `t = 0` at the `rpi_rate` of the day; on one valued in a review month,
that review is made at `t = 0` at the day's `review_prem_shock`, opens its window at that
change and closes the latch if the change passes the day's `review_lapse_threshold`, at
the day's `sel_lapse_ci_loading`; and the columns hold the state before it. Each column is
history: what the contract has given or charged before month 0, never re-derived from a
Reference, which is an assumption from the valuation date on, so that a Reference changed
there reaches back over no review or anniversary already made (UKLIB-SEC-PLAN.md K14, §9
item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `idx_factor_init` | a factor, 1 or more | the start of month 0: mid-year, the policy year under way; on an anniversary, the one it closes | the RPI cover increases given before month 0, on the sum assured at issue; 1 on a policy in force 12 months or fewer |
| `idx_prem_factor_init` | a factor, 1 or more | as `idx_factor_init` | the RPI premium increases given before month 0, on the premium at issue |
| `review_prem_factor_init` | a factor, 0 or more | the start of month 0: mid-period, the review period under way; on a review month, the one it closes | the premium changes the reviews made before month 0 have given, on the premium at issue; 1 on a policy in force no longer than the review period |
| `ci_sel_latched_init` | 0 or 1 | the start of month 0; on a review month, before that review | the select latch: 1 once a review before month 0 has raised premiums past the shock threshold of its day, and 0 before |
| `ci_sel_factor_init` | a multiple of the diagnosis rate, 0 or more | the start of month 0 | the factor the latch closed at, `1 + η` at the loading of its day, read only while the latch is closed: 1 on an open latch, and 1 or below 1 on one closed at a loading of 0 or less |
| `review_prem_shock_init` | a premium change, −1 or more | the last review before month 0 | the change that review made, which sets the shock lapse of its twelve-month window; read only while that window is still running, never on a review month, whose own review opens a window at the day's change, and 0 before the first review |

`CI_UK_S` holds none of them. It recomputes the premium at month `t` as
`P × idx_p(t) × (1 + ρ)^reviews`, one `review_prem_shock` for every review since issue;
the latch as closed once any review's `ρ` passes the threshold; the shock lapse in every
window from that one `ρ`; and the index factors from one flat `rpi_rate`. On a point in
force those are facts of the contract: a `review_prem_shock` set at the valuation date
would reprice premiums long collected, open or close the latch at reviews long past, and
lapse a window already closed. Here a review from the valuation instant on, one in the
valuation month the first, applies `review_prem_shock`, and one before it is the history
the columns carry, counted on the policy clock as the reviews before month 0,
`(duration_mth_init() − 1) // review_period_mths` on a point in force:

- `review_prem_factor(t)` opens at `review_prem_factor_init` and takes `1 + ρ` for each
  review from month 0 on, `reviews_passed(t)` less the reviews before month 0;
- `ci_sel_factor(t)` stays at `ci_sel_factor_init` where `ci_sel_latched_init` is 1, a
  latch already closed, whatever the factor, 1 among them, and otherwise closes at
  `1 + sel_lapse_ci_loading` at the first review from month 0 on whose `ρ` passes the
  threshold. The latch is a flag of its own because a latch closed at a loading of 0
  holds a factor of 1, which read as open would close again at today's loading;
- `review_prem_change(t)`, the change the review under way in month `t` made, is
  `review_prem_shock_init` for a review before month 0 and `review_prem_shock` for one
  from it on; `review_shock_active(t)` asks it inside a window alone, and the shock lapse
  reads it there.

So the reviewable point valued on its second review, from `CI_UK_S` run under a review
change of 10%, carries the first review's history, a factor of 1.1, the latch closed at
1.1 and that review's change of 10%, whose window has long closed. With a change of 15%, a
threshold of 8% and a loading of 20% set at the valuation date, its second review is made
at `t = 0` at 15%: its premium is `55 × 1.1 × 1.15 = 69.575`, where a column that held the
review would carry 10% and 66.55, the window opens at 15%, its lapse
`min(0.30, 0.04 + 2 × (0.15 − 0.08)) = 0.18`, and the latch keeps its 1.1. Valued on its
first review, it carries no history, and the review at `t = 0` closes the latch at the
day's 1.2. The index factors are history up to month 0 alike: the indexed point valued on
its third anniversary carries `1.03^2` and `1.045^2`, and takes its third step at `t = 0`.
An extract written under the old rule, its columns those after an anniversary or a review
at the valuation date, is refused only at month 12, at the review period, and at twice the
review period when the first review's change was not 0; on a later anniversary or review
it passes every rule and takes the month-0 step twice, so an extract must give the state
before it.

On a point issued at the valuation date each history column holds its issue value, and the
model is `CI_UK_S`. A model that dropped the columns and recomputed them from the
References would pass the splice, since `CI_UK_S` and the splice recompute them alike, so
the tests write each off its References' path and project through it.

Nothing else on this product is history `CI_UK_S` rebuilds from a Reference: there is no
commission to claw back, the initial expense falls at issue alone, the additional-payment
and children's benefits read today's indexed cover through the contract's shares and caps,
and the trend and the inflation run from the valuation date. The contractual claim-count
caps, one claim per additional-payment condition and two children's claims, are ignored by
`CI_UK_S`'s frequency loadings, and a point in force carries no count of the claims it has
used either.

| `CI_UK_S` | `CI_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months, any month of a policy year; every `CI_UK_S` point is new business |
| — | the six state columns | `CI_UK_S` recomputes each from its References, from issue: the index factors from `rpi_rate`, the review factor, the latch and the window's change from `review_prem_shock` |

The columns carried over are read as `CI_UK_S` reads them. For a policy in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry`, `joint_age` | years, age nearest birthday | issue, not the valuation date: `age(0, life)` is the attained age there |
| `contract_type`, `life_basis`, `sex`, `smoker`, `joint_sex`, `joint_smoker`, `cover_basis`, `premium_guarantee` | codes, as in `CI_UK_S`'s table | issue |
| `policy_term` | whole years | issue |
| `sum_assured`, `premium_mth` | pounds, the amounts at issue | issue: on an indexed or reviewed point the month's cover and premium are these times the factors |
| `children_cover`, `indexation` | True or False | issue |
| `premium_mode` | monthly or annual | inert, as in `CI_UK_S`: the premium is carried monthly either way |

Four more columns, `row_kind`, `source_policy_id`, `source_mth` and `source_refs`, record
where the generator took each shipped row from (below): `source_refs` names the References
a row was read from `CI_UK_S` under, `review_prem_shock 0.1` on point 14, and is blank on
every row read at those `CI_UK_S` ships. No formula reads them, and an in-force extract
need not carry them: without them the model projects the same numbers, and `run_sec.py`
runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the eight in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, which set to 0 refuses future new
business altogether; each state column is a number in its range, the latch 0 or 1 and its
factor 0 or more; a point not yet in force holds the issue values, 1 for the factors and 0
for the latch and the change; a point in force 12 months or fewer, whose first anniversary
falls in month 0 or later, holds index factors of 1; an open latch holds a factor of 1;
each flag is True or False; each code is one `CI_UK_S` knows, the smoker status `NS` or
`S`, not term assurance's `N`; the ages and the term are finite numbers, and the amounts
zero or more; a joint point has a second life, and is not on the standalone contract,
which `CI_UK_S` scopes out; and the index factors are 1 without indexation, and on a
guaranteed point the review factor 1, the latch open and the change 0. `CI_UK_S` meets
most of these only when a projection reaches them, and some never: a blank flag reads as
True, and one stray word in a flag column turns every `False` in it to text that reads as
True.

A point whose cover had ended by the valuation date, `duration_mth ≥ 12 × policy_term`,
reads, but `proj_len()` refuses it, naming the point: the end of cover is the product's
rule, not the table's. So does a point the contract does not write
([`product-spec.md`](product-spec.md)): a term below 5 years,
`Projection.policy_term_min`, or above 50, `policy_term_max`; a life issued below 18,
`issue_age_min`, or above 64, `issue_age_max`; or a life whose cover runs past the 75th
birthday, `expiry_age_max`, the issue age plus the term. Each is a lower-case Reference,
the contract a compiled model's caches will be sized from: a frame of at most 600 months
and the horizon, and attained ages from 18 to 74 on the pivot table. On every point
`proj_len()` also refuses a Reference off its domain (below), and on a reviewable point a
review history the point cannot have had: a review factor other than 1, a closed latch or
a change other than 0 while it has been in force no more months than `review_period_mths`,
since no review is made before the fifth anniversary and one in the valuation month is
month 0's; and from the month after its first review to its second review's month a review
factor other than `1 + review_prem_shock_init`, the one change made before month 0. What
depends on an assumption of its day is left alone: a latch left open after a change past
today's threshold, the threshold of its day perhaps higher, and the factor of two reviews
or more. The References are the projection's, which `Data` cannot read. A loop over the
block meets such a row only when it reaches it, after projecting the points before it, so
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

The assumption tables are checked before a value of them is read. The pivot table is
checked by its reader, `Data.ci_rate_table`, as it reads the file and before it indexes
and sorts it, so that a fault is named by its line: each age a whole number, each sex `M`
or `F` and smoker `NS` or `S`, each of the four groups holding two pivot ages or more, one
row an age, and each `i_ci` and `q_d` a number above 0 and at most 1, since the
interpolation, `CI_UK_S`'s `pivot_interp`, raises the ratio of two rates to a power. The
pivot ages need not run without a gap, nor be the same in each group. The lapse table is
checked by `Data.lapse_last_year`, the cell the projection takes its extent from: policy
years from 1 without a gap, each rate from 0 to 1. A key is read by its value, so an age
written `40.0` is 40. Each refusal names the file, the column and its lines. And the
interpolation is checked as `Data` makes it, at every attained age the contract admits:
two pivots far apart can extrapolate past the largest float at an age no point reaches,
and a pivot below about 5.6e-309 can make the ratio of two pivots infinite, so a table
whose rate is not a finite number at such an age is refused, naming the file, the column,
the group and the first such age (*Departures from CI_UK_S*).

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`CI_UK_S` and its table by `tests/uk_sec_support.py`, from the `CI_UK_SEC` entry in its
`SEC_SPECS`, and the tests regenerate it and compare, so an edit to a `CI_UK_S` row reaches
it or fails the suite. In the source repository, `python tools/gen_sec_points.py CI_UK_SEC`
writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 7 | twin | S points 1 to 7 | issued at `t = 0`: `CI_UK_S`'s worked example and its contracts, guarantees, lives and options |
| 8 | derived | S point 4 at S month 36 | the indexed point on its third anniversary, its factors those of policy year 3, the anniversary's step its month 0's |
| 9 | derived | S point 3 at S month 60 | the reviewable point on its first review, no review before it, that review its month 0's |
| 10 | derived | S point 3 at S month 66 | the reviewable point inside the window its first review opened |
| 11 | derived | S point 3 at S month 78 | the reviewable point mid-year after the window closed |
| 12 | derived | S point 1 at S month 299 | in its last covered month: a one-row frame |
| 13 | future | S point 4, 13 months on | to be issued at `t = 13` |
| 14 | derived | S point 3 at S month 124, `CI_UK_S` run under a review change of 10% | the reviewable point inside the window its second review opened, its latch closed at its first and its review factor `1.1^2` |

A derived row's `policy_count` is the count `CI_UK_S` carries into that month, its
`pols_if(d)`, and its state what S carries there, so the row continues the S projection from
there: point 8 opens with 0.772371 policies and cover and premium factors of `1.03^2` and
`1.045^2`, which it steps at `t = 0`, as S steps them in month 36. At the shipped review
change of 0 the reviewable rows' history is the issue
values, which the tests move off, so one row is read from `CI_UK_S` run under a change of
10%, which the spec's `derived_refs` records: point 14, with 0.458641 policies, a review
factor of `1.1^2`, the latch closed at 1.1 and its window's change of 10%. At the shipped
change of 0 it projects `CI_UK_S` under 10% up to its next review, at `t = 56`, policy month
180, and today's change from then on, which a test asserts. A derived row's `policy_id` is
the S row's with the month appended, `CI-000003-M60`, and a future row's carries the months
to issue, `CI-000004-F13`. Row `t` of a generated point is month `t + source_mth` of its S
point.

`CI_UK_S` has no point in force, so every twin opens at issue, where no anniversary or
review falls. None is the case `Term_UK_SEC`'s generator refuses, an indexed point its S
model opens in force on an anniversary at factors of 1 and with no step there, whose twin
would take that anniversary's step at `t = 0` and run one step above S.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` keeps
`CI_UK_S`'s three timings and adds `basiclife/BasicTerm_SE`'s `BEF_NB`, each an int
code named as `CI_UK_S`'s string (*The compiled model*):

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, which
  `pols_if(t)` returns;
- `BEF_LAPSE`, after the month's main claims, before its lapses;
- `AFT_DECR`, the end of the month, after its claims and lapses, which is `BEF_NB` at
  `t + 1` exactly, and 0 from the last covered month on.

Any other timing raises. The survivors carried into month `t` are those of month `t − 1`'s
`BEF_DECR` count, which `BEF_NB` forms itself, as its own value at `t − 1` plus that
month's new business, exactly the sum `BEF_DECR` returns. So the chain of calls from
month `t` back to `t_entry()` is one cell a month, where `CI_UK_S`'s `pols_if` chain runs
three. It is the model's one chain: the reviews, the latch and the factors are closed forms
on the policy clock. On a model just read, a cold `net_cf` in the last month runs 11 cells
deeper than one a month, on every committed point and at the contract's longest cover, a
50-year term from issue age 18, issued now and 120 months on, on the reviewable, the
standalone and the joint shapes alike.

The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_claim(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. The additional-payment and children's claims decrement nothing. Joint first
event is still one policy decremented by `1 − (1 − q1)(1 − q2)`.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < expiry_mth()`, `CI_UK_S`'s own frame from
issue on the policy clock, `expiry_mth()` its `12 × policy_term()`, and outside it, before
issue and from the end of the term on, every count is zero, and so every cash flow. No
count evaluates a rate there, and no table is read at a policy year or an attained age the
policy does not have: `ci_rate_base`, `mort_rate`, `lapse_rate_base`, the benefits, the
premium, the factors, the reviews and the latch are zero outside cover, before any table or
rate is read.

## Departures from CI_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, and
each recursion opens at `t_entry()` from the opening state. Where `CI_UK_S`'s test would
have stayed correct on the valuation clock, it moved anyway, so that cover has one
definition. Fourteen cells are new with running in force — `policy_count`,
`duration_mth_init`, `t_entry`, `is_active`, `expiry_mth`, `pols_new_biz`, the six
accessors of the opening state, `review_prem_factor` and `review_prem_change` — and four
more with compiling, `point_id`, `is_accelerated`, `is_reviewable` and `rate_group` (*The
compiled model*). One of `CI_UK_S`'s 63, `pivot_interp`, is gone, `Data`'s two arrays of
its interpolation replacing it. The twin identity exempts it, its spec saying why, and a
cell of `CI_UK_S`'s that this model lacked without saying so would fail it.

| Cells | `CI_UK_S` | `CI_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len` | `12 × policy_term()`, from issue | `expiry_mth() − duration_mth_init()`, from the valuation date; raises past cover, outside the contract's bounds, on a Reference off its domain, and on a review history before the first review | The frame starts at the valuation date |
| `age_at_entry`, `sex`, `smoker`, `age`, `ci_rate_base`, `mort_rate`, `ci_rate`, `claim_rate_life` | `life=1`, a default | `life`, no default; every call passes 1 or 2, positionally | A compiled model declares a defaulted parameter as `long long life=*`, which the C step's typing guard would read as a parameter of that name; modelx keys `CI_UK_S`'s `age(t)` as `(t, 1)`, so the twin identity pairs the cells as before |
| `pols_if`, `pols_if_at`, `pols_if_init` | a recursion through `"AFT_DECR"`, three cells a month, from the column's 1.0 at `t = 0` | `BEF_DECR`, one cell a month from `t_entry()`; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `pols_maturity`, `AFT_DECR` | at `t = proj_len() − 1` | at `duration_mth(t) = expiry_mth() − 1` | One definition of cover, on the policy clock |
| `reviews_passed`, `review_shock_active` | `t // review_period_mths`; the window `t % review_period_mths < 12`, after a review whose `review_prem_shock` passes the threshold | `duration_mth(t) // review_period_mths`; the window on `duration_mth(t)`, asked first, after a review whose own change, `review_prem_change(t)`, passes it | A review falls on a policy month, and a review made before the valuation date made its own change |
| `premium_pp`; `review_prem_factor`, new | `P × idx_p(t) × (1 + ρ)^reviews_passed(t)` | `P × idx_p(t) × review_prem_factor(t)`, the factor opening at `review_prem_factor_init()` and taking `1 + ρ` for each review from month 0 on, month 0's own among them | The reviews made before month 0 are history; one in the valuation month is the projection's, at the day's `ρ` (*The in-force interface*) |
| `ci_sel_factor` | `1 + η` once `reviews_passed(t) ≥ 1` while `ρ` passes the threshold | `ci_sel_factor_init()` while `ci_sel_latched_init()` is 1; else `1 + η` once a review from month 0 on has a `ρ` past the threshold | The latch closed before the valuation date is history, at the loading of its day, which may have been 0; one a review in the valuation month closes, closes at `t = 0` at the day's References |
| `lapse_rate`; `review_prem_change`, new | the shock `w + 2 max(0, ρ − 0.05)` | the shock from `review_prem_change(t)`, `review_prem_shock_init()` in the window of a review before the valuation date | A window open at the valuation date lapses at the change its review made; one a review in the valuation month opens lapses at the day's |
| `idx_factor`, `idx_prem_factor` | a step per anniversary since issue, from 1 | `idx_factor_init()` and `idx_prem_factor_init()`, then a step for each anniversary from month 0 on, month 0's own among them | The increases given before month 0 are history; an anniversary at the valuation date is the projection's, at the day's `rpi_rate` |
| `ci_trend_factor` | `(1 + τ)^(y − 1)`, from issue | `(1 + τ)^(t // 12)`, from the valuation date | A calendar trend on a basis stated at the valuation date |
| `inflation_factor` | `1.03^(y − 1)`, from issue | `1.03^(t // 12)`, from the valuation date | Unit costs in valuation-date pounds |
| `expenses` | the initial expense on `pols_if(t)` at `t = 0` | on `pols_new_biz(t)` | A point in force bears none, one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `ci_rate_base`, `mort_rate`, `lapse_rate_base`, `benefit_pp`, `claims`, `claim_expenses`, the counts | unguarded: no `CI_UK_S` frame has a month outside cover | zero outside cover, before any table or rate is read; the lapse table's extent from `Data` | Before issue `CI_UK_S` extrapolates the pivots to ages the policy never reaches, and raises `KeyError` on the lapse table |
| `check_pols_roll_fwd_resid` | `pols_if(t + 1)` | `pols_if_at(t + 1, BEF_NB)` | The next month's new business is no part of month `t`'s movement |
| `check_claim_split_resid` | any `q_exit` | zero outside cover; `q_exit` past 1 refused in the month it passes | Past 1 the independent conversion has no real value |
| `check_pols_roll_fwd` | `1e-10 × max(pols_if_init(), 1)` | `1e-10 × max(policy_count(), 1)` | `pols_if_init` is 0 on new business here; `check_claim_split` keeps `CI_UK_S`'s tolerance, `claim_split_tol`, a Reference, unscaled in both models, since the artefact it bounds is a rate no count moves |
| `result_cf` | `range(proj_len())`, from issue | `range(proj_len())`, from the valuation date | Row 0 is the valuation month |
| `result_pols` | — | `pols_new_biz` added, the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `claims` | `claims(t, kind=None)`, the kinds by name and, with no kind, their total by `sum` | `claims(t, kind)`, no default: the codes `MAIN`, `AP`, `CHILD` and `LAPSE`, and the total `ALL`, `sum`'s compensated addition written out | A default and `None` do not compile, and three kinds are non-zero together, where a total written left to right parts from `sum`'s in the last bit (*The compiled model*); the twin identity compares `CI_UK_S`'s `claims(t)` with `claims(t, ALL)` |
| `pivot_interp`; `ci_rate_base`, `mort_rate`; `rate_group`, new | `pivot_interp(x, sex, smoker, column)`, a `.loc`, a sorted generator and text keys at every call | gone: `Data.i_ci_array` and `Data.q_d_array`, S's formula at each age the contract admits, 18 to 74, read at a life's row, `rate_group(life)`, and its attained age, an age outside them refused by name, either side | A C cell takes no text and runs no pandas; the twin identity exempts `pivot_interp` and compares its two readers, and a test holds each array to S's call at every group and age, bit for bit |
| `Data.i_ci_array`, `Data.q_d_array` | a pivot table whose interpolation is past the largest float at an age raises `OverflowError` only when a point reaches that age, naming nothing, and, where the ratio of two pivots is itself infinite, gives an infinite rate its cap reads as a certain claim | the table refused when the arrays are made, `ValueError` naming the file, the column, the group and the first age whose rate is not a finite number | The arrays hold every age the contract admits, reached or not, and an infinite rate is refused here as one written in the file is |
| `sex(2)`, `smoker(2)` | `invalid life` on a single life | the column as read, NaN where blank | Reporting cells, whose type the sample traces on a blank second life, so that each compiles to a Python object; no projection cell reads them, `rate_group` taking each life's row of the pivot arrays |
| `premium_mode` | the column as read | the column, refusing any value but `monthly` and `annual` | A reporting cell that validates its column returns text or raises, and compiles to `str`, as `Term_UK_SEC`'s does; `Data` has refused any other mode since the in-force step, so the text is the same on every point it admits |

Of the cash flows, the change of clock moves the maintenance expense alone at the shipped
assumptions, and `net_cf` with it, the trend shipping at 0. Point 9 carries that expense in
valuation-date pounds, so its `expenses(t)` is `CI_UK_S`'s `expenses(60 + t)` divided by
`1.03^5`. Its `pols_if`, `premiums`, the four claims columns and `claim_expenses` are
`CI_UK_S`'s from month 60 on. Point 13 is `CI_UK_S`'s point 4 thirteen months on in those
columns too; its maintenance expense is `1.03^(t // 12 − (t − 13) // 12)` above S's at each
`t`, and its initial expense £200 exactly.

**The caps, as `CI_UK_S` has them since UKLIB-SEC-PLAN.md's M0.** `ci_rate` caps each
life's diagnosis rate, `claim_rate_life` each life's claim rate, `claim_rate` the policy's
and `claim_rate_paid` the standalone paid rate, each at 1, written `min(q, 1.0)`, the
product first and the bound second, so that a NaN stays NaN where `min(1.0, q)` would read
it as a certain claim; wherever `q` is a number the two are the same float. No shipped rate
comes near a cap, the largest claim rate being 0.0404, the joint point's in its last month,
and `Data` refuses a pivot rate past 1; the product passes 1 through the latch's loading, or the pivots' extrapolation, which a
test shows. The additional-payment and children's benefits take their caps the same way,
`min(share × SA(t), cap)`. The lapse rate's bounds keep `CI_UK_S`'s order,
`min(0.30, w + 2.0 max(0, ρ − 0.05))`: they are no cap on a claim rate.

**Domains `CI_UK_S` leaves unchecked.** `CI_UK_S` raises a Reference to a power, divides
by it, bounds a rate or a benefit with it, or reads it as a share, a loading, a frequency or
an amount, and checks none. Off its domain it projects a negative premium, rate, benefit or
expense with every check passing, as a trend of −3, an overlap of 3, a review change of
−150% or a cover cap of −2 would, or a complex lapse rate. And a NaN fails every
comparison it meets: a NaN threshold closes the latch at a review that changed nothing; a
NaN slope reads as the cap through the lapse rate's `min`; a NaN cap is lost through the
`min` it bounds, written with the bound second, so that the additional payment on point 6
is 37,500 and not its cap of 25,000; and a NaN bound of the contract refuses nothing. An
RPI of +∞ reads as the 10% cap, and one of −∞ as no increase.
Here `proj_len()` refuses each Reference off its domain, naming the point, the Reference,
the domain and the value, on every point that reads it:

| Reference | Read on | Domain | Off it |
|---|---|---|---|
| `policy_term_min`, `policy_term_max`, `issue_age_min`, `issue_age_max`, `expiry_age_max` | every point | a whole number, 0 or more | a NaN bound refuses nothing and an infinite one bounds nothing, where the compiled caches will be sized from them |
| `ci_trend` (τ), `inflation_rate` | every point | a finite number, −1 or more | the factors `(1 + τ)^n` and `(1 + i)^n` are negative, and so the diagnosis rate or the expense they multiply |
| `sel_lapse_ci_loading` (η) | every point | a finite number, −1 or more | a closed latch's factor, `1 + η`, is negative, and so the diagnosis rate |
| `overlap_k` (k), `survival_slip` (δ) | every point | a number from 0 to 1 | the shares of the deaths and of the diagnoses that do not pay make a negative claim, paid or exit rate |
| `ap_freq_factor`, `child_freq` | every point | a number from 0 to 12 | a month's additional payments, `ap_freq_factor × i_ci / 12` with `i_ci` capped at 1, or children's claims, `child_freq / 12`, number more than one per policy in force, or fewer than none |
| `rpi_rate` | every point | a finite number | an infinity reads as the cap or as no increase, through the floor at 0 and the cap |
| `idx_cover_cap`, `idx_prem_cap`, `idx_prem_mult` | every point | a finite number, 0 or more | an increase is a cut: at a cover cap of −2 the cover is −100,000 and the premium −440; a NaN cap is lost through `min` |
| `ap_share`, `child_share` | every point | a number from 0 to 1 | a share of the indexed cover makes a negative benefit, or one past the cover |
| `ap_cap`, `child_cap` | every point | a finite number, 0 or more | a negative cap is a negative benefit; a NaN one is lost through `min(share × SA(t), cap)`, as the children's benefit of 75,000 shows |
| `expense_acq`, `expense_maint`, `expense_claim` | every point | a finite number, 0 or more | an expense is income |
| `claim_split_tol` | every point | a finite number, 0 or more | at an infinity `check_claim_split` passes anything, and below 0 fails everything |
| `review_period_mths` | a reviewable point | a whole number of months, 1 or more | the reviews divide the policy months by it: at 0 by zero, below it counting reviews backward, off a whole number in parts |
| `review_lapse_cap` | a reviewable point | a number from 0 to 1 | the shock lapse is at most the cap: past 1 its monthly rate, `1 − (1 − w)^(1/12)`, has no real value, which `CI_UK_S` projects as a complex number, and below 0 the window lapses a negative share |
| `review_prem_shock` (ρ) | a reviewable point | a finite number, −1 or more | a review takes the premium below 0 |
| `review_lapse_threshold` | a reviewable point | a finite number | the latch and the window compare a change with it, and a NaN closes the latch at every review |
| `review_lapse_slope` | a reviewable point | a finite number, 0 or more | the window lapses fewer the more the premium rises; at NaN, at the cap |

Each domain is a comparison no NaN passes, a finite number one of which `x − x == 0`
holds, which an infinity fails too, and a whole number one of which `x % 1 == 0` holds,
which an infinity fails as well. A guaranteed point reads no review Reference, and
projects whatever they are. A whole review period written as a float, `60.0`, is read as
the int it is, so that it counts reviews as 60 does. The pivot rates, whose ratio the
interpolation raises to a power, are the table's, which `Data` holds above 0 and at most
1, and `Data.future_horizon_mth` is held to a whole number of months, 0 or more, by `Data`
itself, as it reads the table.

**The exit rate past 1, refused in its cell.** `check_claim_split_resid` converts the
notes' annual exit rate, `q_exit = q_d (1 − k) + i_ci δ`, independently, to bound the
standalone split's artefact, and `CI_UK_S` caps no part of it, since it is never a
decrement: past 1, which an extrapolated mortality rate reaches above the last pivot with
rates `Data` accepts, the conversion has no real value and `CI_UK_S`'s residual is a complex
number, whose magnitude its check compares without a word. Here the residual raises in the
month `q_exit` first passes 1, naming the point, the month, the rate, the two rates it is
made of and the References, rather than return a number with no real value. At rates that
high the artefact passes the shipped `claim_split_tol` some months earlier, where the check
returns False, as `CI_UK_S`'s does.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and no number: what its reports computed on
each committed point was frozen before the change, and they still compute it, to 1e-12 of
each column's largest value (*Tests*, below), and every value the in-force model cached on
the committed points and on the full splice grid was this one's, bit for bit, when the
change was made. Cell by cell, at every argument a full modelx sweep evaluates, the
compiled model computes what modelx computes, bit for bit, on the committed points, on the
points of the splice grid, which take the branches they do not, at the contract's
extremes, where the caps on the claim rates bind and on keys written as floats. The
compile tests hold it so on x86-64, and to 1e-12 relative elsewhere, where no run has
shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py critical_illness                  # in place, beside the model
python build_sec_cy.py critical_illness --out /tmp/ci    # elsewhere, with the CSVs
```

The tool exports the model to `CI_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `CI_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/critical_illness")    # the directory holding the build
from CI_UK_SEC_nomx_cy import mx_model as model
model.Projection[8].result_cf()                    # point 9, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about a minute with gcc, 58 s here, and needs modelx-cython, which needs a C
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
declaration. So each input now reaches a cell as a number, as `Term_UK_SEC` was taught
first (UKLIB-SEC-PLAN.md §6.1; USLIB-SEC-PLAN.md R1 to R17):

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[8]` is point 9, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `policy_term()` is `int(data.policy_term()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The six columns of opening state are
  vectors too, the latch an int64 of 0 and 1.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula reads into the number it selects, for every point at once: the contract type
  into `is_accelerated`, the life basis into `is_joint` and the premium guarantee into
  `is_reviewable`, each a flag; each life's sex and smoker status into the row of the
  pivot arrays they select, `rate_group` and `joint_rate_group`, M NS 0, M S 1, F NS 2 and
  F S 3; each true-or-false column, `children_cover` and `indexation`, into a 0/1 flag;
  and a single life's blank second age into 0 beside the flag `is_joint`, so that no
  formula tests for NaN. Each decodes as `CI_UK_S` reads the column, which a test holds on
  every value a column can hold, and what it cannot hold it refuses (below). The cover
  basis and the premium mode are checked, and not decoded: no projection cell reads
  either, the cover being level on every point `Data` admits and the premium carried
  monthly in either mode.
- **The pivot interpolation, made once.** `CI_UK_S`'s `pivot_interp(x, sex, smoker,
  column)` interpolates the pivot table log-linearly at every call, with a `.loc`, a
  sorted generator and text keys, none of which a C cell can run. `Data` makes it once:
  `i_ci_array` and `q_d_array`, by the group's row and the attained age, padded from age 0
  so that the index is the age, each element built by S's own formula on Python floats,
  at every attained age the contract admits, `Data.rate_age_min` to `rate_age_max`, 18 to
  74, and NaN below. `Data` cannot read `Projection`'s bounds, so it holds the two ages as
  References of its own, which a test holds to `issue_age_min` and `expiry_age_max` less
  one. `ci_rate_base` and `mort_rate`, the arrays' one reader each, read them at the
  life's row, `rate_group(life)`, and its attained age, checking the age against both ends
  first. A test holds every element to S's call by its bits, on the shipped table and on
  one whose groups hold other pivot ages, and `pivot_interp` is the one cell of `CI_UK_S`'s
  this model lacks, which the twin identity exempts.
- **Tables indexed by integers.** The lapse rates are `lapse_table_array`, by policy year,
  padded at year 0 with NaN, which nothing reads. `lapse_rate_base` holds the policy year
  at the table's last above, as `CI_UK_S` does, and reads in cover alone, where the year
  is 1 or more.
- **Codes.** A timing or a kind, which `CI_UK_S` spells as text, is an int Reference named
  as the text: `BEF_NB = 0`, `BEF_DECR = 1`, `BEF_LAPSE = 2` and `AFT_DECR = 3`, in the
  order of their instants within the month, and `MAIN = 0`, `AP = 1`, `CHILD = 2` and
  `LAPSE = 3`. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`.
  `benefit_pp` takes the first three kinds, and refuses the others. A string argument
  would give the cell a dictionary for a cache, where a code indexes a C array, so codes
  are numbered from 0 without a gap.
- **The claims total, a code of its own.** `CI_UK_S` totals the four kinds as
  `claims(t)`, its `kind` defaulted to `None`, with Python's `sum`. A default compiles as
  a keyword parameter the typing guard refuses, and `None` is no C integer, so the total
  is `claims(t, ALL)`, `ALL = 4`, and `net_cf` reads it. `sum` of floats compensates since
  Python 3.12: it carries the rounding error of each addition, Neumaier's way, and adds it
  back once at the end. The main claim, the additional payment and the children's claim
  are non-zero together in most months of cover, and there a total written left to right
  parts from `sum`'s: in 415 of the 2,040 months of the twins of `CI_UK_S`'s seven points.
  So the total is `sum`'s addition written out, in explicit statements: `0.0 +` the main
  claim, `sum`'s start, then each later kind added with its rounding error carried, and
  the carried error added once at the end, where it is finite and not 0. A test holds it
  to `CI_UK_S`'s total by its bits in every month of every twin, of S's points and of the
  splice's, and finds the months where a sum left to right would part. On Python 3.11,
  whose `sum` adds left to right, `CI_UK_S`'s total parts from this one in those months,
  so the test holds the rest there and skips the bits, naming Python 3.11.
- **Five powers raise as modelx does.** Past the largest float, Python's float power
  raises `OverflowError` where C's `pow` gives an infinity. So expense inflation, the
  morbidity trend, the two index factors and the review factor call Python's own power
  where theirs is infinite from a finite base, as `Term_UK_SEC`'s do (uslib's *Record —
  M22* form). Only inputs far outside the product reach it (*What it refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `contract_type()`,
  `life_basis()`, `cover_basis()`, `premium_guarantee()`, `premium_mode()`, `sex(life)` and
  `smoker(life)`, and the two reports return a table row, text and DataFrames, for a
  reader, for `run_sec.py` and for the comparison with `CI_UK_S`. No other cell calls
  them, so they cost the projection nothing. The first five validate their column, as
  `CI_UK_S`'s first four do and `premium_mode()` now does too, so each returns text or
  raises, and compiles to `str`. `sex(life)` and `smoker(life)` return each life's column
  as read, a single life's blank second life as NaN, and compile to Python objects, as
  the sample traces them (below), so that each returns what modelx returns.

The `Data` docstring lists its 27 vectors, arrays and extents, each with the column or
file it comes from. The four readers stay Python, returning DataFrames and a
path, and no `Projection` cell but `model_point()` reads them. Every other cell of
`Projection`, 70 of its 80, returns a C `bint`, `long long` or `double`, and caches a
single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 722 by `t`, of `double`, `long long` or `bint` | the 35 cells of `t` alone: every count, rate, factor, premium and cash flow; the policy clock and its years; the reviews, their window and the latch; the checks' residuals; and the flag `is_active` |
| a C array of 722 by 5 | `pols_if_at(t, timing)`, `benefit_pp(t, kind)`, `claims(t, kind)`, `age(t, life)`, `ci_rate_base(t, life)`, `mort_rate(t, life)`, `ci_rate(t, life)` and `claim_rate_life(t, life)` |
| a C array of 5 by life | `age_at_entry(life)` and `rate_group(life)` |
| one `bint`, `long long` or `double` | the 25 other cells without a parameter: the point's numbers, flags and opening state, the ends of its frame, and the two checks |
| a Python object, or `str` | the ten reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the two labels
of a life's.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the two reports
and the two checks on every committed point, and then the cells no report reaches:
`model_point()` and the seven label accessors, which only a reader asks for, and
`point_id()`, which only a refusal names. Every timing and every kind a cell takes the
reports reach, the total through `net_cf`. It runs the committed points alone: the export
reads the CSVs of the directory the build is made in, which in place is the product
directory. The committed points leave branches untaken: a review that changes the premium
in the frame, its window and the latch it closes, on every point but 14, the review
change shipping at 0; the reviewable standalone and joint contracts, a male smoker, cover
below the ancillary caps and ages past the last pivot; the caps on the claim rates. That
still types every cell, because every branch of a cell returns the one type its others
return, a count a float in every branch, and on points that take those branches the
compiled model computes modelx's numbers (above). The two life labels are typed from more
than the committed points: the sample also calls `sex` and `smoker` of each life on a copy
of the first point, a single life, with its second life blank, written to a temporary
directory and read by a second instance of the export, so that each compiles to a Python
object, which a test holds in the sample's code. The sample also raises the recursion
limit, which modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 722 | 721. The longest frame is the longest term, 50 years, `policy_term_max`, issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 50 + 120 = 720 months, `t = 0 … 719`, and the month after, 720, whose roll-forward residual reads the count carried into 721 |
| `t`, `timing`; `t`, `kind`; `t`, `life` | 722 by 5 | `t` as above, by the four timings, by the four kinds and the total, and by the two lives. Every 2-D cache of a model shares one inner width, the widest, here the kinds': Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `life` | 5 | 2. Widened to the same 5, so that a life the cells refuse by their own formula, 0, 3 or 4, is refused as in modelx, `ValueError("invalid life")`, in every per-life cache |

`proj_len()` refuses a term above `policy_term_max`, in modelx as compiled, and `Data` a
point issued more than `future_horizon_mth` months ahead, so no report on a point the
model projects runs past these caches. Those two References are the contract the sizes
are derived from; the ages bound none, since an age indexes `Data`'s pivot arrays, not a
cache. Raise the maximum term or the horizon, and a report runs past the caches in the
compiled model alone: `t` past its size raises `IndexError`, naming nothing, where modelx
projects. Each needs the sizes derived again, as `spec_sec.py` derives them, and a
rebuild; a longer horizon, `t` raised to 12 × 50 + the horizon + 2. Lower `issue_age_min`
or raise `expiry_age_max` past `Data.rate_age_min` or `rate_age_max`, and the arrays'
readers refuse the age, in both engines, naming the point, until the two are moved too.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as `d` in `proj_len()`, stays a Python object, though the cell is typed
`long long`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of every decrement
here, is a complex power, which gcc computes with `cpow` rather than `pow`, and its last
bits can differ from Python's; and gcc fuses a multiply and an add where the target has the
instruction, one rounding where Python rounds twice. The tool's docstring has the detail,
and uslib's [`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the
measurements that put each there. With all four, every compiled value here agrees with
modelx bit for bit. The compile tests hold each directive in the module's first line, and a
static test holds the tool's line to the two and no other: `cdivision=True` would make `//`
on C integers truncate where Python floors, which only `duration(t)` meets, before issue,
where the policy clock is negative; the reviews' `//` and `%` divide the policy clock
inside cover alone, where it is 0 or more. And `boundscheck=False` or `wraparound=False`
would change what an `idx` outside the table reads.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
645,072 bytes, the type's basic size, which holds every cell's cache, and deleting
it, `del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a test runs the compiled runner on a block of 126 points, the committed table copied,
and finds no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 26. What it needs
is stack. That call, a cold `net_cf` in the last month of the longest cover, a 50-year
term from 18, now or 120 months on, runs the count chain back to `t_entry()`, 611 cells
deep in modelx, one cell a month and 11 more, which a test holds, on the reviewable, the
standalone and the joint shape alike, and compiled with gcc, on each shape, at the shipped
References or with the review change and the trend on, it needs between 144 and 160 KiB:
it ran on a thread of 160 KiB and not of 144. A test runs each shape at its longest cover
in a thread of 1 MiB, the stack Windows gives a program's main thread unless the program
is linked for more, and again on the main thread, which is where `run_sec.py --cython`
runs. MSVC's
frames may be larger than gcc's, and CI's Ubuntu runner needed two to four times this
machine's stack for `Term_UK_SEC`'s chain (UKLIB-SEC-PLAN.md §6.1, *Record — M2*); the
`cython_uk` CI job runs the test on both, and records the sizes each ran on. The export
recurses in Python instead: the same call needs a recursion limit of 1,242 there, and the
reports and checks, which run in ascending `t`, need 128, so `sample_sec.py` sets 5,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message: each
malformed row of the table, each assumption table a reader cannot read, each point the
frame refuses, a review history among them, each Reference off its domain that the
compiled model can hold, an exit rate past 1, an age either side of the pivot arrays, and
what the vectors cannot hold, in a cell typed `long long` or `double` as in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, and a
term, an age or a count of months as an int, a whole number as an int where its domain is
refused. So a rate written as an int, 2, or a bound written as a float, 24.0, gives one
message in both engines, which a test holds for each. An int Reference is a C `long long`
compiled, so a value no C integer holds is refused as it is set, NaN with `ValueError` and
an infinity with `OverflowError`, and a fraction is truncated as it is set, 60.5 to 60,
where modelx computes with it, and its `proj_len()` refuses it as no whole number. So set
each int Reference as a whole number: the five bounds of the contract and
`review_period_mths`, which a test holds the compiled model to, and `Data`'s
`future_horizon_mth`, `rate_age_min` and `rate_age_max`.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault: a `point_id` that is not a whole number, or is `2**53` or more in size; an issue
  age, a term or, on a joint first-event point, a second age `2**53` or more in size,
  which an int64 vector cannot hold whole and numpy would cast without a word; and, as
  since the in-force step, a code that names no contract type, life basis, sex, smoker
  status, cover basis, premium guarantee or premium mode, and a flag that is not True or
  False. A key written as a float, an age `40.0`, is read by its value, as `CI_UK_S`'s
  lookups match it. And `Data.rate_age_min` and `rate_age_max` that are not whole, the
  first below 0 or the second below the first, by `Data.rate_age_first`, which the arrays
  and their readers ask first; and a pivot table whose interpolation is not a finite
  number at an age the contract admits, as the arrays are made.
- An attained age outside the pivot arrays, by the cell that reads them, where
  `CI_UK_S`'s interpolation extrapolated to any age: `point_id 1: ci_rate_table.csv is
  interpolated at attained ages 18 to 74, Data's rate_age_min to rate_age_max, not at
  17`, from `ci_rate_base` or `mort_rate`, on a contract whose bounds were moved past them.
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: expense inflation, the morbidity
  trend, the two index factors and the review factor each call Python's own power where
  theirs is infinite from a finite base, so that the compiled model raises the platform's
  message as modelx does, rather than carry an infinity on. Only an input far outside the
  product reaches one: an inflation or a trend above about 140,000 a year, an index
  increase or step above about 2 million, or a review change above about 1.8e34 at the
  shipped period of 60 months, or 2.3 at one of a month; a test reaches each.
- A timing, a kind or a life no cell takes, by the cell, as `CI_UK_S`'s are:
  `invalid timing`, `invalid kind`, `invalid life`.

An argument outside a cache raises `IndexError` in the compiled model alone:
`net_cf(722)` or `net_cf(-1)`, which modelx answers with 0, the month being outside
cover; `pols_if_at(t, 5)`, `claims(t, 5)` and `benefit_pp(t, 5)`, which modelx refuses as
a timing and a kind it does not take; and `age_at_entry(5)`. An `idx` past the last row is
refused in both, with an `IndexError` at the first read of a vector, and `Projection[-1]`
reads every vector at its last element in both, so it is the table's last point, under
that point's own `point_id()`; the compiled refusal test holds both against modelx.

An annual claim rate above 1 is not refused but capped, in both: `ci_rate`,
`claim_rate_life`, `claim_rate` and `claim_rate_paid` cap at 1, as `CI_UK_S` does
(*Departures from CI_UK_S*, above), and a compile test holds the two equal on points where
each cap binds, new business and in force. A NaN product would stay NaN through a cap, in
both, which the compiled model computes as a comparison that keeps the value unless the
bound is smaller.

### Speed

`python tools/bench_sec_cy.py critical_illness` builds the model into a temporary
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
| compiled | 6,006 | 0.207 ms (0.205–0.218) | 0.607 ms (0.555–0.623) | 86–87 MB |
| export | 602 | 2.74 ms (2.71–2.74) | 3.21 ms (3.15–3.29) | 86–87 MB |
| modelx | 126 | 85.2 ms (82.4–91.0) | 90.7 ms (90.1–91.0) | 104–106 MB |

On `net_cf` the compiled model runs 13.2 times its export (12.5 to 13.4 over the three),
and on `result_cf`, where building the DataFrame takes most of its time, 5.4 times (5.1
to 5.7); it runs 411 times modelx on `net_cf` (379 to 443) and 150 on `result_cf` (146 to
162). The ranges are the noise of a shared machine, about −3% to +7% on modelx's
`net_cf` and −8% to +3% on the compiled report. `Term_UK_SEC`, timed the same way on its
own points on the same day, ran 12.8 and 4.5 times its export. The release keeps a block
flat: the compiled model's peak did not grow over its 6,006 points in any run. Reading the
three files and building every `Data` vector and array for those points, the pivot arrays
among them, took 0.041 to 0.043 s, and asking every point for its frame, the runner's
first pass, 0.08 s. Every engine, loop and run summed `net_cf` over a copy of the table to
the same −41,825.43743, to 1e-9 relative.

Measured on 2026-11-23 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.30 GHz), a 1-minute load average between 1.38 and 2.23 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1 to 7, every
  cell of `CI_UK_S`'s agrees at every argument `CI_UK_S` evaluates in its own sweep, to
  1e-9 relative with no absolute floor, but for `pols_if_init` and `model_point`, and
  `result_pols` and `pivot_interp`, which the spec names with its reasons; a cell this
  model lacked would fail it. The kinds and timings are compared as the codes of the same
  names, and `CI_UK_S`'s claims total, `claims(t)`, with `claims(t, ALL)`. So
  `CI_UK_S`'s worked example, which `tests/test_critical_illness_uk.py` asserts to the
  penny and the in-force to six decimals, holds here with no number restated. The same
  suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present. And
  `tests/test_critical_illness_uk_sec.py` compares each twin with S in every cell again,
  with the trend and the review change on in both models, which T1 and the splice, each
  at a trend of 0, cannot: a cell that dropped the trend fails there alone.
- **The splice**, in `tests/test_critical_illness_uk_sec.py`: each `CI_UK_S` point
  restated in force at months 1, 11, 12 and 13 (the first anniversary), 59, 60 and 61 (the
  first review, pivot age 45 on the anchor cell, lapse year 6), 71 and 72 (the shock
  window's end), 119, 120 and 121 (the second review), 239 and 299, continues the S
  projection in every cell the two share but `proj_len`, and in both reports, to 1e-9
  relative with no absolute floor. The review change, which ships at 0, is on in both
  models at 12%, past the shock threshold and apart from the select loading of 10%, so
  that the reviews move premiums, open their windows and close the latch, and a latch or
  a review factor read from the other's value would show; inflation and the trend, the
  inputs on the valuation clock, are 0 in both. A change of 20%, whose shock lapse takes
  the cap, the threshold itself, where no window opens and no latch closes, and the float
  above it, where both do, are spliced on the reviewable point the same way. Four variants of S's points, in a copy of S's table that is never
  committed, reach what S's own cannot: the reviewable point indexed and a male smoker, the
  standalone contract reviewable, the anchor cell issued at 50 with cover of 40,000, whose
  pivots run past the table's last and whose ancillary benefits fall below their caps, and
  the joint point reviewable with a male smoker as its second life. A core of 29 of the 116
  splice cases and 7 of the 20 future ones runs by default, and the full grid with
  `UKLIB_SEC_FULL=1`; a test asserts the core reaches every branch, opening-state column,
  kind of valuation month and side of every `min` and `max` the full grid reaches.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point is
  the S projection moved on, with zeros before issue and no rate evaluated there, and so is
  each variant issued a month on, the reviewable point 13 months on, its reviews a month off
  the valuation years, and the indexed point 25.
- **How it computes**: on every row of the splice's grid, after its reports, its checks
  and every monthly cell at every month, no cell has been called at a negative month, none
  on the books read a month before `t_entry()`, none read a month later than `t + 1`, and
  none raised. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, the policy clock being a closed form, and every point's reports and
  checks run under modelx's recursion limit lowered to 40, which a recursion backward over
  the frame would exceed; they pass at 10. And the count's chain, called cold in the last
  month at the contract's longest cover on three shapes, runs one cell a month back to
  `t_entry()` and at most 16 more.
- **Counts**: the roll-forward closes; `result_pols()` is S's report with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, with the review change and the trend on,
  multiplies every flow and counted cell and moves no per-policy value, bit for bit, the
  factors, the reviews and the latch among them; and the roll-forward, its tolerance scaled
  by the count, closes on a million policies.
- **Validation and regeneration**: each malformed row of the table, 77 cases, each `2**53`
  bound at the bound among them, and an increase given on the first anniversary, the
  first-year rule's edge, is refused naming its point, and naming its label on an extract
  labelled otherwise than by position; the horizon is a Reference; a point past its cover
  or outside the contract's bounds, 15 cases, a bound set as a float among them, is
  refused by `proj_len()`, each bound just inside it and each moved past a committed
  point, and `run_sec.py --block` refuses such a point before printing anything; so is a
  review history on a point in force no longer than the review period, 9 cases, a review
  factor, a closed latch and a change each at both ends of the window, the first month and
  the first review's, and the edge at 61 under a period of 61, and a review factor from
  the month after the first review to the second review's month that is not 1 plus the one
  change made before month 0, 9 cases, the rule's tolerance and both ends of its window,
  61 and 120, among them, accepted at two reviews, past the window, within its tolerance
  and at both ends where the factor is the change's, and each of 29 References off its
  domain, the value next outside each edge, NaN and both infinities, on every point that
  reads it, each printed as the compiled model holds the Reference, an int set on a float
  Reference and a whole float on an int one among them, where at the edges the twin that
  reads it is S's in every cell; a whole review period written `60.0` projects as 60 does,
  cell for cell and type for type; an exit rate past 1 is refused in the month it passes,
  where S's residual is complex; each assumption table a reader cannot read, 25 cases, is
  refused naming its lines, or the group and the age where the pivots' interpolation
  passes the largest float, three tables on which `CI_UK_S` projects the anchor cell; keys
  written as floats read as `CI_UK_S` reads them; the edges of the interface and of each
  bound are accepted, a review that cut the premium, to 0 at the edge, a review history
  the month after the first review, an increase the month after the first anniversary, and
  a latch closed at a factor of 0 among them; every state `CI_UK_S` reaches, as shipped,
  under the splice's review change and where the cap binds, is accepted in force, at the
  months either side of each rule's edges; and the committed table is what `CI_UK_S`
  generates.
- **The product's own facts**: the two clocks on the shipped points; the committed rows,
  in force and issued later, continuing their S points at the shipped assumptions but for
  inflation, and the row read under a review change of 10% continuing `CI_UK_S` under it
  to its next review, and after it at that change in both; each history column read, not
  recomputed, the index factors, the review factor, the latch and the window's change,
  each written off its References' path, on a history a policy can have, and projected
  through; the latch read from its flag, so that one closed at a factor of 1, or below it,
  stays closed through a later shock review; the change read inside its window alone; and
  a review change set at the valuation date reaching back over no review already made
  (UKLIB-SEC-PLAN.md K14); an anniversary and a review at the valuation date made at the
  day's References, each figure recomputed by hand and the columns held to `CI_UK_S`'s
  state under the history's References in the month before: the RPI at 5% on the indexed
  point on its third anniversary, and on its first, where the row is `CI_UK_S`'s at 5%
  from month 12 in every cell; and a change of 15%, a threshold of 8% and a loading of 20%
  on the reviewable point on its first review and its second, read from `CI_UK_S` under a
  change of 10%, where on its first the row is `CI_UK_S`'s under the day's References from
  month 60 in every cell; expense inflation and the morbidity trend on the valuation
  clock, which only these tests see; the initial expense on new business alone; the
  reviews and their window on the policy clock; every guarded cell's value outside cover;
  the block; an extract without the generator's columns, labelled otherwise,
  projecting the same numbers; `run_sec.py`'s numbers, for a point, the joint life among
  them, and for the block, and its sum, and its `--cython` stopping where no repository is
  above it; no cell's parameter defaulted but the `claims` total's; the docstrings, read
  through docutils as the docs build reads them where docutils is installed; and the
  shared input tables.
- **The caps**: on the reviewable point, the anchor cell and the joint point, its second
  life a male non-smoker issued at 42, with the male non-smoker's diagnosis pivots at 60 and
  65 raised to 0.98 and 1.0, in a copy of the table, under the splice's References: on the
  reviewable point the latch's loading takes the diagnosis rate past 1 from attained age 60,
  policy month 240, and with it the claim rates; on the anchor cell the claim rate alone
  passes 1, from attained age 64, policy month 288; and on the joint point the second life's
  claim rate, from its attained age 64, policy month 264. In both models the capped rates
  and the monthly decrement are the float 1.0 there; every policy in force at the start of
  that month claims in it, and none is in force after it; the reports hold finite floats;
  and every cell the two models share agrees, issued now and 12 months on, and restated in
  force the month before the cap, to 1e-9 relative with no absolute floor. And a NaN sent to
  a cap, through the overlap, the trend, the latch's loading or the survival slippage, or to
  the RPI's floor and caps or the ancillary benefits' caps, stays NaN in the cell, where the
  frame refuses the Reference; and each check is False where its residual's formula is
  replaced by one returning NaN, the only way left to give it one.
- **The C step's representation**, in modelx, in seconds: `claims(t, ALL)` is `CI_UK_S`'s
  total by its bits in every month of every twin, of S's points and of the splice's, where
  a total written left to right parts from it in 415 of the 2,040 months of S's seven, and
  under 12 additional payments a year or a survival slippage of 1, where a later kind
  outweighs the main claim and its error is carried in `sum`'s second form, and by `repr`
  where the main claim is past the largest float in every month, the total inf as S's,
  the bits skipped on Python 3.11, whose `sum` adds left to right; each pivot array is
  S's `pivot_interp` by its bits at every group and every age it
  holds, on the shipped table and on one whose groups hold other pivot ages; every value
  each text column can hold decodes as `CI_UK_S` reads it, each fraction above .5 so that
  a decode that rounded would part, each life's row of the arrays holding S's rates at
  every age; each padded array holds NaN where it holds no rate and nothing else, and its
  one reader refuses an age outside it, either side, on an extract labelled otherwise than
  by position; the arrays' ages are the contract's, and each off its domain is refused;
  each `Data` vector is the int64 or float64 the `Data` docstring's table states, and each
  parameterless cell returns a Python number; `spec_sec.py`'s sizes and `sample_sec.py`'s
  recursion limit are what their comments derive, and the sample traces each life's labels
  on a blank second life; `run_sec.py --cython` rebuilds exactly when a source is newer;
  and a label the vectors cannot hold, or a timing, kind or life no cell takes, a single
  life's second issue age and the benefits' lapse kind and total among them, is refused.
- **C2, the fingerprint**: on every committed point, each column of `result_cf` and
  `result_pols`, its sum over the frame, its largest absolute value and its values in five
  months, the first, the last and the three quartiles between, is what the model computed
  when its E step ended, to 1e-12 of the column's largest value, frozen at the end of the
  module by `tools/gen_sec_fingerprint.py` before the C step changed anything. Measuring
  the opening state before an anniversary or a review at the valuation date, rather than
  after it, moved point 8's opening factors and none of its numbers but by rounding, at
  most 2.2e-15 of a value of `net_cf`, which the freeze holds unchanged; no review row
  moved, point 9's history being the issue values either way at the shipped change of 0,
  and point 14, at policy month 124, falling on neither.
- **Compiled**, the tests marked `cython`, which compile the model once a session into a
  temporary directory and run it in child processes: in
  `tests/test_compiled_conventions_uk.py`, C3, the typing guard, on the declarations, the
  spec and the generated C; C4 on the committed points; and the release. In this model's
  module, C4, every cell at every argument a full modelx sweep evaluates, with every code
  no swept cell reads and both lives of every cell of a life (`_ci_c4_also`, the spec's
  `c4_also`, which a test holds to asking each in every month, row by row, the codes and
  the lives each cell takes derived in modelx, not read from the test's own lists, and
  another to leaving no call of a life that computes uncompared), on the splice grid, at
  the contract's extremes, each shape at its longest cover and its oldest age, issued now
  and 120 months on and in force in its last month, where the caps on the claim rates bind
  and on keys written as floats, and on the total's two cases, a later kind outweighing
  the main claim and a main claim past the largest float; each life's label that is not
  text; the refusals, message for message, the overflows of the five powers, the
  `IndexError`s past the caches and an `idx` past the table and of −1 among them; what the
  compiled model does with a value an int Reference cannot hold; each shape's deepest cold
  call on a 1 MiB thread and on the main thread; a Reference set late, which clears no
  cache; and `run_sec.py --cython`, which prints what modelx prints.

```bash
python -m pytest tests/test_critical_illness_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_critical_illness_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k CI_UK_SEC
UKLIB_CYTHON_SHARD=critical_illness python -m pytest -m cython tests -q     # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R8]: #uklib-critical_illness-r8
[std]: #uklib-std
<!-- END generated citation links -->
