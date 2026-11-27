# In-Force Implementation Notes

**Status:** Draft, 2026-11-24. `IP_UK_SEC` is [`IP_UK_S`](model.md) taught to project from
a valuation date. Besides policies issued at that date, it takes policies already in force
there, in any month of their policy year, with lives in health and lives in claim at any
claim duration, and policies to be written in the ten years after it, as lifelib's
`basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is the one
[`product-spec.md`](product-spec.md) specifies and [`technical-notes.md`](technical-notes.md)
models; this page says what running in force changes, and what compiling it changed. The
suffix adds lifelib's letters to `S`: `E` for in force, as in `BasicTerm_SE`, and `C` for
the compiled form, as in `basiclife/BasicTerm_SC`: the model runs in modelx and compiles
under modelx-cython to C, which computes the same numbers (*The compiled model*, below).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `IP_UK_S` on another time axis, and it reads `IP_UK_S`'s assumption tables in place,
> every assumption unchanged: the contractual mechanics are sourced, and every rate is a
> **[std]** standardization, the inception and termination bases proxies shaped like the
> CMI IP11 Series, whose values are restricted to the CMI's Authorised Users, the
> mortality a proxy shaped like the ONS national life tables, and the lapse table a
> placeholder no public study anchors. Replace them with licensed tables and company
> experience before drawing any conclusion from the numbers.

## Run it

```bash
python products/income_protection/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/income_protection/run_sec.py 9          # point 9: the anchor cell in force 60 months
python products/income_protection/run_sec.py --block    # every model point, summed row by row
python products/income_protection/run_sec.py 9 --cython # point 9 on the compiled model
```

The first prints the twelve rows `run.py` prints for `IP_UK_S`'s point 1, with the policy
counts behind them. Three lines to the same thing for point 9:

```python
import modelx as mx
model = mx.read_model("products/income_protection/IP_UK_SEC")
model.Projection[8].result_cf()          # point 9, the table's ninth row
```

`Projection` takes `idx`, a point's position in the table, from 0, as `basiclife`'s
`BasicTerm_SC` does, and `point_id()` returns the point's label; the runner takes points
by their `point_id`, and its key from the model. `result_cf()` has `IP_UK_S`'s columns —
`pols_if`, `pols_active`, `pols_sick`, `premiums`, `claims_benefit`, `claims_death`,
`claims_lapse`, `expenses` and `net_cf` — with one row per month from the valuation date,
`t = 0 … proj_len() − 1`, and
`result_states()` `IP_UK_S`'s ten columns of the states, their transitions and the annual
rates. `result_pols()`, new, sets out the counts behind them on the same rows: `pols_if`,
`pols_new_biz`, the healthy and the sick counts, then the month's movements in the
notes' processing order, out of health the deaths, the lapses and the inceptions, out of
claim the recoveries and the deaths, the recoveries that leave the model and the expiry;
then the benefit and the premium per policy.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[9]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`. Its projection years carry the counts
of their first month, in force, healthy and in claim, and the flows of all twelve.

`--cython` runs the compiled model in place of modelx and prints the same lines, building
it first with the library's own `build_sec_cy.py` where no build is current, and
`--build DIR` runs a build made elsewhere (*The compiled model*, below). The tool goes with
the library, into lifelib and into a `lifelib.create()` copy, so `--cython` builds there as
here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to; the
claim clock, `z`, is a third, which only the termination rates read.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the policy end date.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the lapse table's key and the escalation's, and
  `age(t) = age_at_entry() + duration(t)`, the inception and mortality tables', as in
  `IP_UK_S`. Cover ends at the policy end date, policy month
  `expiry_mth() = 12 × (expiry_age − entry_age)`, `IP_UK_S`'s frame from issue.
  `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion as long as the
  frame; the closed form needs no such chain of calls.
- **`z`, the claim clock**, counts the months a claim has run: the lives in claim at the
  start of month `t` are held by claim duration, cohort `z = 1` the claims that incepted at
  the end of month `t − 1`, not yet paid. `claim_dur_year(z)` keys the termination table.
  It is `IP_UK_S`'s, unchanged.

Point 9 is the anchor cell in force 60 months, its fifth anniversary falling at the
valuation date. At `t = 0` it is in policy year 6 at attained age 40, 0.683305 of its
policy in force, 0.680544 healthy and 0.002761 in claim, and its frame has 300 rows,
`t = 0 … 299`; `IP_UK_S` projects the same months as its rows 60 to 359. Point 17 is the
female cell to be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is
on the books from `t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 229 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the inception and mortality tables at the attained age; the lapse table by policy year; the escalation of the benefit and premium on each policy anniversary, and the lapse shock from policy year 2; the policy end date | expense inflation, `inflation_factor(t) = 1.03^(t // 12)`; discounting, `disc_factor(t) = 1.03^(−(t + 1) / 12)` |

Expense inflation runs on `t`, stepping on each anniversary of the valuation date, for
every point alike (USLIB-SEC-PLAN.md D7): the maintenance and claim-management loads are
then in valuation-date pounds. `IP_UK_S` inflates from issue, `1.03^(y − 1)`, which on a
point in force would inflate a load stated today by the years the policy has already run;
on its `in_claim` cells, which it opens at the valuation date, the two are one.
Discounting was already on `t`, to the start of `IP_UK_S`'s frame, the valuation date on
every point here. The RPI is a flat Reference, the rate assumed from the valuation date on,
and `cycle_factor` a scenario overlay on inception and recovery from it. Neither model
charges an acquisition expense or a commission.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[p].result_cf() for p in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`IP_UK_S` computes: every cell the two models share agrees, but two whose meaning changed,
`pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `IP_UK_S`'s columns, one
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s name, a policy
clock column and three columns of opening state, and beside it a companion,
`inforce_cohorts_sec.csv`, which holds the lives in claim by claim duration. The count is
the only weight on the flows, and every state is per policy, a share of the count or an
amount. Each is measured at the valuation instant, the start of month 0, before any
month-0 event, recoveries of month −1 already returned to health (USLIB-SEC-PLAN.md D6;
UKLIB-SEC-PLAN.md §6.3). An anniversary that falls at the valuation date is month 0's
event, the projection's first: the benefit and premium columns hold the policy year it
closes, and its increase is made at `t = 0` at today's References, as a fixing at month 0
reads the assumptions of the valuation date (D6, as precised at uslib's M7). Each state is
history, what the contract has given and what the lives have done, never re-derived from
a Reference, which is an assumption from the valuation date on (UKLIB-SEC-PLAN.md K14):

| Column | Unit | Meaning |
|---|---|---|
| `policy_count` | policies, not necessarily whole | the policies in force at the valuation date, healthy and in claim together, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most `Data.future_horizon_mth`, 120 as shipped |
| `pols_active_init` | a share of the count, 0 to 1 | the lives in health, those sick but still inside the deferred period among them, and the recoveries of month −1 back in health; 1 on a point not yet in force, which is issued healthy |
| `benefit_pp_init` | pounds a month | the benefit entering month 0, `IP_UK_S`'s `benefit_pp(d − 1)`: the policy year of month −1, after every increase the RPI has given; the benefit at issue on a point not yet in force, and in its first policy year |
| `premium_pp_init` | pounds a month | the premium entering month 0, as `benefit_pp_init` |

| `inforce_cohorts_sec.csv` | | |
|---|---|---|
| `point_id`, `z` | whole numbers, the key | a point in force and a claim duration at which it holds lives in claim, 1 to its `duration_mth` |
| `pols_sick_dur_init` | a share of the count, 0 to 1 | the lives in claim at claim duration `z`, `IP_UK_S`'s `sick_cohorts(d)` element `z − 1` over its `pols_if(d)` |

The companion is sparse: a claim duration a point holds no row for holds no lives, so a
point all healthy holds no row, and a claims extract one row per claim in payment. The
anchor cell at its month 359 holds 359 cohorts, one for each month's inceptions still in
claim; under the contract's bounds a cohort vector runs to 624. The rejected shapes were
624 columns, and one model point per state, exact since the model is linear but a
projection per cohort.

`IP_UK_S` holds none of the state. Its `status` column says whether a point is in health
or in claim, and an `in_claim` point puts its whole count into cohort
`claim_duration_months + 1`, with its policy clock restarted at the valuation date and its
`entry_age` the attained age there: a healthy policy months after issue cannot be
represented, and it rebuilds the benefit and premium from issue at today's flat
`rpi_rate`. Here:

- `pols_active(t)` opens at `t_entry()` at `policy_count × pols_active_init` plus the
  month's new business, which enters healthy, and `sick_cohorts(t)` at `policy_count ×
  pols_sick_dur_init(z)` for each `z`; from there each runs `IP_UK_S`'s recursion, one cell
  a month;
- `benefit_pp(t)` and `premium_pp(t)` open at `benefit_pp_init()` and `premium_pp_init()`
  and take `1 + j` and `1 + 1.5 j` for each anniversary since the columns' year,
  `duration(t) − duration_init()`, `duration_init()` being the policy years of month −1, so
  that an anniversary at the valuation date steps them at `t = 0`. The benefit escalates
  for everyone in health and in claim alike, so no cohort carries an amount of its own.

`status` stays, a label no formula reads, which an extract may leave out, and
`claim_duration_months` is gone, the companion its successor. On a point issued at the
valuation date each state holds its
issue value, and the model is `IP_UK_S`. A model that dropped the columns and recomputed
them from the References and the status would pass the splice, since `IP_UK_S` and the
splice recompute them alike, so the tests write each off that path and project through
it.

### What `Data` refuses

`Data.model_point_table()` checks the table as it reads it, the first rule that fails
raising `ValueError` and naming the missing column or every point it fails on, by its
`point_id`: the five in-force columns present, and the eleven of `IP_UK_S`'s the projection
reads, `status`, a label, not among them; no `point_id` twice; a count that is a number, 0
or more; a `duration_mth` that is a whole number below `2**53` and no further from the
valuation date than the horizon, itself a whole number 0 or more below `2**53`; a healthy
share from 0 to 1 and amounts 0 or more; the codes `IP_UK_S` branches on, `status`'s where
the table has it, and a `premium_basis` of `guaranteed`, the one the model prices, which
`IP_UK_S` checks in a cell no formula calls; an occupation class from 1 to 4 and a
deferred period of 4, 8, 13, 26 or 52 weeks; finite ages below `2**53`; and the history
from below: a policy not yet in force all healthy and at its issue amounts, a policy in
force 12 months or fewer at its issue amounts, a level policy at them always, and an
escalating policy at them or above, to half a cent, each increase floored at 0. The
history's upper bounds read References, so `proj_len()` holds them. Rule 12 refuses one
state `IP_UK_S` cannot reach either: a policy whose escalation option has lapsed after
increases refused, its benefit above its benefit at issue and its escalation `none`. The
model cannot represent a lapsed option, which would keep the increases already given and
take no more, so such a policy is not one it projects.

`Data.inforce_cohorts()` checks the companion by eight rules, naming the lines, the header
line 1: the three columns; keys whole and below `2**53`; a point of the table; one row a
point and duration; a point in force, `duration_mth` above 0, since a point not yet in
force is issued healthy; a duration from 1 to the point's `duration_mth`, since a claim
incepts at the end of a month the policy is in force; a share from 0 to 1; and on every
point in force the healthy share and the cohort shares summing to 1 within 1e-10, the
tolerance `check_states` holds the population identity to.

Each assumption table is checked before a value of it is read, in the cell the projection
first asks of it: `Data.inception_table()` itself, and `Data.termination_last_year()`,
`Data.mort_age_first()` and `Data.lapse_last_year()`, which give the extents
`IP_UK_S`'s lookups took from the table. Each key is a whole number below `2**53`; the
termination and lapse years run from 1 without a gap or a repeat, each sex of the
mortality table over the table's ages, and each of the forty inception schedules holds two
pivot ages or more; and every rate is a number from 0 to 1. A fault is named by its lines.

### What `proj_len()` refuses

Whether a point is still in cover and whether the contract issues it are rules of the
product, not of the table, so the frame applies them, naming the point: a point at or past
its policy end date at the valuation date; an issue age outside `issue_age_min` to
`issue_age_max`, 18 to 59, or an expiry age outside `expiry_age_min` to `expiry_age_max`,
50 to 70, the bounds the compiled caches will be sized from; and an issue age at or past
the expiry age. So is an escalation history the contract cannot have, after the
anniversaries before the valuation date: a benefit above the benefit at issue increased by
`esc_cap` at each, a premium above the premium at issue increased by `esc_prem_mult` times
`esc_cap` at each, or a premium outside the range its benefit's increases allow, each
increase `j` of the benefit's raising the premium by `esc_prem_mult × j`, least when the
benefit's increases fell at the cap, one part-way and the rest none, most when they were
equal. Each holds to half a cent, the benefit's own half cent carried into the premium's
range, for an extract rounded to the cent; a level point, at its amounts at issue, meets
them, and so does every state `IP_UK_S` reaches. And each Reference off its domain, NaN
and both infinities outside every one:

| Reference | Domain | Off it |
|---|---|---|
| `cycle_factor` | a finite number above 0 | 0 divides the recovery rate by zero; below 0.4 `IP_UK_S`'s in-claim survival is silently 0 |
| `mort_active_factor`, `esc_cap`, `esc_prem_mult`, `esc_lapse_slope`, `esc_lapse_threshold`, `ben_breakpoint`, `ben_cap_mth`, `ben_guarantee_mth`, `expense_maint`, `expense_claim` | a finite number, 0 or more | a negative rate, step or load; a NaN threshold is lost through the shock's `max`, a NaN cap through the escalation's `min` |
| `ap_ratio`, `claim_severity`, `ben_band1_rate`, `ben_band2_rate` | a number from 0 to 1 | a benefit paid above its amount, or of the wrong sign |
| `ben_tolerance` | a number above 0, at most 1 | a maximum-benefit check that passes or fails every point |
| `rpi_rate` | a finite number | the escalation reads an infinity as no increase or as the cap |
| `inflation_rate` | a finite number, −1 or more | a factor that changes sign each year |
| `disc_rate` | a finite number above −1 | −1 divides by zero |
| `issue_age_min`, `issue_age_max`, `expiry_age_min`, `expiry_age_max` | a whole number below `2**53`; the minimum issue age 0 or more, each maximum its minimum or more, and the latest expiry at most a year past the mortality table's last age | a NaN bound refuses nothing and an infinite one bounds nothing, where the compiled caches will be sized from them; past the table the frame reads an age it lacks |

At each edge of its domain a Reference projects its reports in finite floats, but where
the edge takes a value past the floats: an escalation, a load, a count or a rate each in
its domain can, and the cell where such a value first is refuses it, naming the point,
the month and what makes it, where `IP_UK_S` would carry an infinity into every report and
pass its checks. A power that would pass the largest float, the benefit's and premium's
steps, the inflation factor and the discount factor, is refused by name where Python's
power raises `OverflowError`, naming neither.

## The model points

No row of `model_point_table_sec.csv` or `inforce_cohorts_sec.csv` is typed by hand. Every
one is generated from `IP_UK_S` and its table by `tests/uk_sec_support.py`, from the
`IP_UK_SEC` entry in its `SEC_SPECS`, and the tests regenerate them and compare, so an edit
to an `IP_UK_S` row reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py IP_UK_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 3, 4, 6 | twin | S points 1, 3, 4, 6 | issued at `t = 0`: the active-lives anchor cell, its level-cover variant, the female cell and the older male cell |
| 2, 5, 7 | twin | S points 2, 5, 7 | in claim, on policy clocks of whole years since issue: the claims-in-payment worked example, issued at 34 and in force 12 months, its claim at duration 1; the claim at duration 30, issued at 47 and in force 36 months; and the worked example's claim on the active-lives basis, as point 2 |
| 8 | derived | S point 1 at S month 12 | the anchor cell on its first anniversary, at its first year's amounts, its first escalation at `t = 0` |
| 9 | derived | S point 1 at S month 60 | the anchor cell in policy year 6, the lapse table's last, at attained age 40, an inception pivot |
| 10 | derived | S point 1 at S month 359 | the anchor cell in its last month, 359 cohorts in claim |
| 11 | derived | S point 2 at S month 24 | the claims-in-payment cell at claim duration 25, in claim year 3 |
| 12 | derived | S point 5 at S month 6 | the claim at claim duration 37, in claim year 4 |
| 13 | derived | S point 7 at S month 12 | the claim on the active-lives basis, 0.391343 of its count recovered and healthy, some of it claiming again |
| 14 | derived | S point 4 at S month 13 | the female cell a month past its first anniversary, at £1,545 and £60.61 |
| 15 | derived | S point 6 at S month 118 | the older male cell in its last two months |
| 16 | derived | S point 3 at S month 30 | the level cell mid-year |
| 17 | future | S point 4, 13 months on | to be issued at `t = 13` |
| 18 | derived | S point 1 at S month 40, `IP_UK_S` run under an RPI of 5% | the anchor cell at `2,000 × 1.05^3` and `35 × 1.075^3`, its lapses shocked by 1.05 since policy year 2 |
| 19 | derived | S point 4 at S month 30, `IP_UK_S` run under an RPI of 12% | the female cell at the cap's `1,500 × 1.1^2` and `58 × 1.15^2` |

A derived row's `policy_count` is the count `IP_UK_S` carries into that month, its
`pols_if(d)`, and its state and cohorts what S carries there, so the row continues the S
projection from there. Where S carries no policy into the month, as on a claim on the exit
basis whose every life has recovered, which the recovery bound's splice set reaches, the
generator writes a point of no policies, all healthy, its share 1 and no cohort, which
projects nothing, as S does; no committed row is one. At the shipped 3% no state holds a
lapse shocked by escalation, nor
an increase capped, so two rows are read from `IP_UK_S` run under an RPI of their own,
which the spec's `derived_refs` records, their cohorts read under it too: points 18 and
19. The table records each row's RPI in a column of the generator's, `source_refs`,
`rpi_rate 0.05` and `rpi_rate 0.12`, blank on every row read at the shipped References,
which no formula reads. At the shipped References they step at today's 3% from their next
anniversary, and a test asserts each. A derived row's `policy_id` is the S row's with the
month appended, `IP-000001-M60`, and a future row's carries the months to issue,
`IP-000004-F13`. Row `t` of a generated point is month `t + source_mth` of its S point.

**The in-claim twins.** `IP_UK_S` opens its three `in_claim` points in claim at the
valuation date with their policy clock restarted there, so they have no policy clock to
copy (UKLIB-SEC-PLAN.md D8): S's row records no issue date. Each twin is given one, issued
`n` whole years before, the least whole number of years that holds the claim,
`n = ⌈(z0 + 1) / 12⌉` for a claim at duration `z0`, with `duration_mth = 12n` and issue
age `entry_age − n`: its anniversaries are then S's, a year apart, its attained ages S's,
and its claim cohort S's. That clock is the generator's choice, not the policy's: a claim
at duration 0 after a 26-week deferral fits a policy anywhere from 7 to 11 months old.
Points 2 and 5 then match S in every count, cash flow and check, since their healthy state
is empty and only the clock cells differ. On point 7 the recovered lives return to health
and lapse there, and the twin's clock runs a year ahead of S's restarted one: in each year
S lapses them at a policy year's rate, 10% in its first, where the twin lapses them at the
next year's, 8% in its second, so that 60 months on 0.8002 of the twin is in force against
`IP_UK_S`'s 0.7791. Neither is the policy's own clock, which S's row does not record; the
difference is the clock each model gives the claim, S's restarted one recorded below. So
the tests compare point 7 and its rows under a flat lapse table, on which the two clocks
lapse alike, and under which the twin equals S in every cell. An `in_claim` point with RPI
escalation has no twin: valued on an anniversary, it would escalate at `t = 0`, where
`IP_UK_S` takes no step, and the generator refuses it, naming the point. No shipped point
is one.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other; every policy issued starts in
health. `pols_if(t)` is `pols_active(t) + pols_sick(t)`, the count weighting month `t`,
healthy and in claim, D5's row weight with no exception. `pols_if_at(t, timing)` keeps
`IP_UK_S`'s two timings and adds `basiclife/BasicTerm_SE`'s `BEF_NB`, each an int code
since the C step, named as `IP_UK_S`'s text (*The compiled model*):

- `BEF_NB`, 0, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if(t)` less `pols_new_biz(t)`, exactly, since new business arrives only on an
  empty book;
- `BEF_DECR`, 1, the count before month `t`'s decrements, `pols_if(t)`;
- `AFT_DECR`, 2, the count after them: `BEF_NB` at `t + 1`, which counts none of that
  month's new business, and 0 in the last covered month and outside cover.

Any other timing raises. The roll-forward check reads the same `BEF_NB`, so it never
counts the next month's new business. The three cumulative counts, of deaths, lapses and
recoveries leaving the model, which only the population identity reads, restart at
`t_entry()`, the identity restated on the count on the books; `IP_UK_S`'s count from its
frame's start, and the splice compares their increments. Both checks scale their
tolerance with `policy_count()`, the policies on the books, which `IP_UK_S`'s
`pols_if_init()` is not here on a point issued at or after the valuation date.

`pv_benefits()` discounts the benefit outgo to the valuation date, and `annuity_dis()` is
it over the amount payable at `t_entry()` times `policy_count()`, per policy on the books;
`IP_UK_S` divides by `amount_payable_pp(0)` alone, the same number on its points, each of
one policy. On a point in claim on the exit basis the factor is the notes' `a_dis(a0, z0)`:
49.783 per £1 a month on the worked example's twin, as in `IP_UK_S`.

The caps are `IP_UK_S`'s since M0: active-life mortality, in-claim mortality and inception
`min(q, 1.0)`, the bound second, so that a NaN stays NaN; recovery and lapse
`min(1.0, w)`, the bound first, `IP_UK_S`'s order, which no NaN reaches, `Data` and
`proj_len()` holding every rate and Reference they read to a number. At the shipped
References none binds. The tests bind four: mortality at a factor of 100, inception at an
overlay of 50, the lapse rate at an RPI of 12% under a shock slope of 300 and the recovery
rate at an overlay of 0.35, which every splice under it crosses. The in-claim mortality's
cap no test binds, and none can: `Data` holds the termination table's rates to 0 to 1 and
no factor multiplies them, so the cap meets only a rate of 1 at most; a test holds its
order, a NaN rate staying NaN through it. The inception rate's floor at 0 binds on no
shipped schedule, each, one shape scaled, extrapolating to 0 only below age 13.3, under
the youngest issue age; but `Data` accepts a schedule that falls below 0 above it, and a
test splices one, a copy of the inception table whose schedule for variant 9, issued at
22, reads 0 until 30, where `IP_UK_S` and this model floor it alike.

## Departures from IP_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, and
each recursion opens at `t_entry()` from the opening state. Twelve cells are new —
`policy_count`, `duration_mth_init`, `duration_init`, `t_entry`, `is_active`,
`expiry_mth`, `pols_new_biz`, `result_pols` and the four accessors of the opening state,
`pols_active_init`, `pols_sick_dur_init`, `benefit_pp_init` and `premium_pp_init` — and
one of `IP_UK_S`'s 73 is gone, `claim_duration_months`, which the claim cohorts replace.
Four References are new, the contract's bounds `issue_age_min`, `issue_age_max`,
`expiry_age_min` and `expiry_age_max`, and in `Data` the future horizon; `Data` gains the
companion's reader and the four tables' checks, three of the readers reading their file
once through a `*_rows` cell that the check and the indexed reader share. The C step adds
seven cells more, `point_id`, the decodes `inception_schedule`, `mort_schedule`,
`is_escalating` and `recovery_code`, and the claim durations the cohorts' sums run to,
`claim_dur_init` and `claim_dur_live`, and drops `IP_UK_S`'s two tuple cells,
`sick_cohorts` and `claim_rate_vectors`, whose elements are cells here; with `idx` and the
codes, and in `Data` its vectors, arrays and two interpolated ages (*The compiled model*).

| Cells | `IP_UK_S` | `IP_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len`; `expiry_mth`, new | `12 × (expiry_age − entry_age)`, from issue | `expiry_mth() − duration_mth_init()`, from the valuation date; raises at or past the policy end date, outside the contract's bounds, on an escalation history past them and on a Reference off its domain | The frame starts at the valuation date |
| `pols_active`, `pols_sick_dur` | from `pols_if_init()` on an `active` cell, into cohort `claim_duration_months + 1` of the tuple `sick_cohorts` on an `in_claim` one | from `policy_count` split by the healthy share and the companion's cohort shares at `t_entry()`, new business healthy; each cohort a cell since the C step | Lives in health and in claim at once, at every claim duration, are history |
| `max_dur` | `proj_len() + claim_duration_months() + 1` | `expiry_mth() + 1`, the cover from issue and a cohort of headroom | A claim is no older than its policy; on a future row the horizon would size `z` |
| `pols_if`, `pols_if_at`, `pols_if_init` | `pols_if_at(t + 1)` read for the roll-forward; `pols_if_init()` the column | `BEF_NB` added, `pols_if(t) − pols_new_biz(t)`; the roll-forward and `AFT_DECR` read it at `t + 1`; `pols_if_init()` 0 unless in force | Next month's new business is not this month's survivors |
| `benefit_pp`, `premium_pp`; `duration_init`, new | the amounts at issue times `(1 + j)^(t // 12)` | `benefit_pp_init()` and `premium_pp_init()` times the step for each anniversary since the columns' year, an anniversary at the valuation date the first; a value past the floats refused in its month | The increases already given are history, and one at month 0 is the projection's, at today's References |
| `premiums`, `claims`, `expenses`, `net_cf`, `pv_benefits`, `esc_lapse_factor` | unchecked | a value past the floats refused in its month, naming the point and what makes it | An infinite flow would pass every check |
| `inflation_factor` | `1.03^(y − 1)`, from issue | `1.03^(t // 12)`, from the valuation date; past the floats refused | Unit costs in valuation-date pounds |
| `disc_factor` | `1.03^(−(t + 1) / 12)` | the same, on the valuation clock; past the floats refused | Values at the valuation date |
| `annuity_dis` | `pv_benefits() / amount_payable_pp(0)` | over `amount_payable_pp(t_entry()) × policy_count()`, refused where that is 0 | Per policy on the books, at the month the point is first on them |
| `pols_dead_cum`, `pols_lapse_cum`, `pols_exit_cum` | from the frame's start | from `t_entry()` | The identity restated on the count on the books |
| `check_pols_roll_fwd`, `check_states`, `check_states_resid` | tolerance `1e-10 × max(pols_if_init(), 1)`; the identity on `pols_if_init()` | tolerance on `policy_count()`; the identity on `policy_count()` in cover and 0 outside it | `pols_if_init()` is 0 on new business |
| `inception_rate`, `mort_rate`, `lapse_rate_base`, `lapse_rate` | evaluated before issue by `result_states()`, the lapse lookup raising there | 0.0 outside cover, without a read | No table read at a policy year or an age the policy does not have |
| `result_pols`, new | — | the counts and amounts behind the reports, row by row | D5's report |
| `status`, `premium_basis` | branched on; checked by a cell no formula calls | a label no formula reads, which an extract may leave out; refused by `Data` unless `guaranteed` | The shares are read, not decided by status; a reviewable premium is not priced |

Every cell outside cover holds 0, False or a vector of zeros, as its docstring says, and
reads no rate: no count evaluates a rate before issue or from the policy end date. The
generator, not the model, departs once more: a month at which `IP_UK_S` carries no policy
is written as a point of no policies, all healthy, where S's shares are 0 over 0.

**Defects of `IP_UK_S`** found in this work, which `IP_UK_SEC` does not share or, for the
first, compares around:

- an `in_claim` cell's policy clock restarts at the valuation date, its row recording no
  issue date, so point 7's recovered lives lapse at first-year rates in the year after
  it, whatever the policy's age: 0.7791 in force at month 60, against 0.8002 on its twin,
  whose clock, the least whole year that holds the claim, runs a year ahead;
- `premium_basis()` has no caller, so its check never runs, and a point set to
  `reviewable` projects as guaranteed;
- `annuity_dis()` divides by the amount payable alone, so on a point of more than one
  policy the factor is not per policy;
- a blank, text or infinite rate in any assumption table is read as NaN or infinity, which
  the caps keep and every flow carries, and a gapped or repeated key raises `KeyError`
  only where a projection reaches it, or reads a wrong row;
- the docstrings say restoring the age dimension to the termination basis touches only
  the lookups, but the cohort shift assumes the rates depend on `z` alone; and
  `claim_rate_vectors` recomputes the in-claim survival beside `claim_surv_step`, which
  only the tests read.

**From the plan and from uslib's rule**, the C step departs once more, in its caches'
widths (*What compiling changed, and why*, below). UKLIB-SEC-PLAN.md §9 item 11, §6.3's
first option, asks that the timings and the kinds become cells of `t` alone, so that only
the cohorts carry a cache 626 claim durations wide; and uslib holds one inner width a
model (USLIB-SEC-PLAN.md §6.1 step 6, as `WholeLife_US_SEC` met it at M15). Here the
timings and the kinds keep `IP_UK_S`'s cells of two parameters, `pols_if_at(t, timing)`
and `claims(t, kind)`, which T1 compares and the conventions read, R9's `pols_if_at(t,
BEF_DECR)` among them, and uslib's rule is one inner width an outer size: the cohorts'
cache takes an outer size of its own, 747, beside the timings' and kinds' 746. The end
item 11 asked is kept: the cohorts are `IP_UK_S`'s bit for bit, none pooled, and they
alone are 626 wide.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and how the claim cohorts are carried, and no
number: what its reports computed on each committed point was frozen before the change,
and they still compute it, to 1e-12 of each column's largest value (*Tests*, below), and
every value the in-force model cached was this one's, bit for bit, when the change was
made, each element of the cohort vector beside its cell here among them: 1,805,221 values
on the 19 committed points, and 10,986,993 on the 129 points of the full splice grid under
each set's References, none apart. 117 differ in type alone: where no cohort holds lives,
the in-force step's sum of no terms was the int 0, and is the C double 0.0 here.
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model
computes what modelx computes, bit for bit, on the committed points, on the points of
the splice grid, which take the branches they do not, at the contract's extremes, where
each cap, floor and bound binds, the inception floor's splice among them, on every
inception schedule, on keys written as floats, on the committed rows under the
References they were read from, and on the rows valued on an anniversary under References
that move its increase. The compile tests hold it so on x86-64, and to 1e-12 relative
elsewhere, where no run has shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py income_protection                 # in place, beside the model
python build_sec_cy.py income_protection --out /tmp/ip   # elsewhere, with the CSVs
```

The tool exports the model to `IP_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `IP_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/income_protection")    # the directory holding the build
from IP_UK_SEC_nomx_cy import mx_model as model
model.Projection[8].result_cf()                     # point 9, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about two minutes with gcc, 122 s here, and needs modelx-cython, which needs
a C compiler, so the models do not require it: `pip install modelx-cython`, or
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
whose body still looks a value up in a DataFrame, compares text or sums a tuple runs
Python under its C declaration. So each input now reaches a cell as a number, as uslib's
`Term_US_SEC` was taught first (USLIB-SEC-PLAN.md R1 to R17), and `WOL_UK_SEC` here:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[8]` is point 9, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `benefit_mth()` is `float(data.benefit_mth()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The opening state's three columns are
  vectors too, and the claim cohorts a table of them.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula reads into the number it selects, for every point at once: the sex, the
  occupation class and the deferred period into the point's row of the inception array,
  `inception_schedule`, `20 × sex + 5 × (class − 1) + deferred`, M before F and the
  deferred periods 4, 8, 13, 26 and 52 weeks 0 to 4, forty schedules; the sex into its
  row of the mortality array, `mort_schedule`; the escalation into a 0/1 flag,
  `escalation_rpi`, RPI 1, which `is_escalating()` reads; and the recovery basis into its
  code, `recovery_code`, `return_to_h` 0 and `exit` 1, `Projection`'s `RETURN_TO_H` and
  `EXIT`. Each decodes as `IP_UK_S` reads the column, which a test holds on every value a
  column can hold, and the flag is checked and decoded by its text alone, exactly `RPI` or
  `none`, so that `" True"`, `"RPI "` or `1` is refused as the table is read, in both
  engines, never read one way by the check and another by the decode. `status` is a label
  no formula reads, and `premium_basis` a `Data` refusal of anything but `guaranteed`.
- **Tables indexed by integers.** The inception table is `inception_array`, by schedule
  and attained age, padded from age 0 so that the index is the age, and holding at each
  age the contract admits, 18 to 69, `IP_UK_S`'s interpolation between the schedule's
  pivot ages, its extrapolation beyond them and its floor at 0, made once by `IP_UK_S`'s
  own formula, element by element, so that `inception_rate` multiplies it by the overlay
  and caps it, as `IP_UK_S` does; a test holds every schedule at every age to `IP_UK_S`'s
  rate, on the shipped table and on the floor's. The ages are two References of `Data`'s,
  `rate_age_min` and `rate_age_max`, which a test holds to the contract's issue age and
  latest expiry less one, since `Data` cannot read `Projection`'s. The mortality table is
  `mort_table_array`, by sex and attained age, padded from age 0; the termination table's
  two rates `recovery_rate_array` and `mort_rate_sick_array`, by claim duration year,
  clamped at the table's last year, `termination_last_year`, as `IP_UK_S`'s
  `tbl.index.max()` reads it; and the lapse table `lapse_rate_array`, by policy year,
  clamped at its last, 6. The padding holds NaN, and nothing reads it: the one cell that
  reads each array checks its key first, and the claim cohorts' column 0 is no claim
  duration.
- **The claim cohorts, a cell an element.** `IP_UK_S` carries a month's cohorts in one
  tuple, `sick_cohorts(t)`, and their rates in three, `claim_rate_vectors()`, which a C
  cell cannot hold. Here each cohort is a cell, `pols_sick_dur(t, z)`, a recursion of two
  parameters: cohort 1 is the previous month's inceptions, every other cohort the cohort
  one duration younger in the previous month times its month's survival, `claim_surv_step
  (z − 1)`, and at `t_entry()` the opening cohorts, `policy_count` times the companion's
  share at the point and claim duration, `Data.cohort_share`, a `[point, z]` array. Each is
  the float `IP_UK_S`'s tuple holds, the same products in the same order. The rates are
  the cells of one claim duration that `IP_UK_S` already had, `rec_rate_mth`,
  `mort_rate_sick_mth` and `claim_surv_step`, whose values are the tuples' elements. The
  cohorts past the termination table's last year are not pooled into one: pooling is
  exact in exact arithmetic and not bit for bit with `IP_UK_S`.
- **The sums, `sum` written out.** `pols_sick`, the lives in claim, and the month's three
  flows out of claim, `pols_sick_surv`, `pols_recovery` and `pols_death_sick`, sum the
  cohorts, and `pv_benefits` the discounted benefit, which `IP_UK_S` sums with Python's
  `sum`, compensated since Python 3.12, Neumaier's way. So each is that sum written out as
  a loop in `z` order, each addition's rounding error carried, the larger of the two in
  size first, and added back once at the end where it is finite and not 0, `sum`'s own
  test; the loop starts from `0.0`, whose first compensated addition is `sum`'s plain
  first one. Each stops at `claim_dur_live(t)`, the longest claim duration whose cohort
  can hold lives, `min(max_dur(), claim_dur_init() + t − t_entry())`, the companion's
  longest opening claim aged since `t_entry()`, or the claims incepted since: every cohort
  past it is 0.0, which `IP_UK_S`'s three filtered sums leave out and whose addition
  changes neither the compensated sum nor its carried error. A test holds every sum to
  `sum` by its bits in every month of every committed point, and to `IP_UK_S`'s own on
  its twins, and counts the months where a plain left-to-right sum parts from it. On
  Python 3.11, whose `sum` adds left to right, `IP_UK_S`'s sums part from these in their
  last bits, and so do the count's roll-forward residual and the states' residual, each
  a rounding about zero, by 1e-16 or less: there the conventions' twin test holds the
  two residuals to an absolute floor, and the product module's test of the sums, which
  CI runs on Python 3.13, holds the rest and skips their bits, naming Python 3.11. So the
  recursion forms the cohorts that can hold lives and no others, a triangle of the months
  by the claim durations on new business, where the whole vector would form the
  rectangle `IP_UK_S`'s tuples do.
- **Codes.** A timing or a kind, which `IP_UK_S` spells as text, is an int Reference
  named as the text: `BEF_NB = 0`, `BEF_DECR = 1` and `AFT_DECR = 2`, in the order of
  their instants within the month; and `claims`' kinds, `BENEFIT = 0`, `DEATH = 1` and
  `LAPSE = 2`, in `result_cf()`'s order, and `ALL = 3`. A call reads as before, less the
  quotes: `pols_if_at(t, BEF_DECR)`. A string argument would give the cell a dictionary
  for a cache, where a code indexes a C array, so codes are numbered from 0 without a gap;
  the timing 3, inside the cache's width of four, is a code `pols_if_at` refuses, as it
  refuses any other.
- **The claims total, a code of its own.** `IP_UK_S` totals the three kinds as
  `claims(t)`, its `kind` defaulted to `None`, with `sum` over a generator. A default
  compiles as a keyword parameter the typing guard refuses, `None` is no C integer and a
  generator is a Python object, so the total is `claims(t, ALL)`, which `net_cf` reads,
  written out left to right, `0.0 + claims(t, BENEFIT) + claims(t, DEATH) + claims(t,
  LAPSE)`: `sum`'s float wherever at most two kinds are non-zero, and here at most one is,
  the death and lapse kinds being 0 by the product's design. A test counts the kinds
  non-zero together in every month of every committed point, never two, and holds the
  total to `IP_UK_S`'s by its bits on every twin of its new business. On Python 3.11,
  whose `sum` adds left to right, `IP_UK_S`'s benefit claim, which reads its cohort sums,
  parts from this model's in its last bits, so the twins' bits skip there, naming Python
  3.11.
- **One inner width an outer size.** Cython's unpickle code reads each 2-D cache back
  through a C-array temporary, with a converter named by the inner type,
  `__Pyx_carray_from_py_double___5b_626_5d_` for `double[626]`. It pools its temporaries
  by C type, and its C-array types compare equal on the outer size and the element type,
  the inner size not compared: `int[746][4]` and `double[746][4]` are two types,
  `double[746][4]` and `double[746][626]` one. So the caches of one outer size share a
  temporary of the first one's shape for their values, and another for their flags. Two
  widths there hand a converter a temporary of the wrong shape, as uslib's
  `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2, *Record — M15*): gcc 14 refuses the
  build by default, and gcc and clang under `-Werror=incompatible-pointer-types`, which
  the library's `build_sec_cy.py` passes on Linux and macOS, but MSVC only warns, and the
  build would write 746 × 626 doubles into a temporary of 746 × 4 as a point is unpickled.
  uslib read that as one inner width a model, which here would widen `pols_if_at` and
  `claims` to the cohorts' 626 claim durations, three such caches of about 5.6 MB a point,
  values and flags. So the cohorts' cache takes an outer size of its own, `t`'s months and
  one more, 747, beside the timings' and kinds' 746 by 4: the unpickle code,
  `__pyx_unpickle__c_Projection__set_state`, shares a temporary of 746 by 4 between
  `claims` and `pols_if_at` for their values, a `double[746][4]`, and one for their flags,
  an `int[746][4]`, and gives the cohorts their own two of 747 by 626. That rests on an
  internal of Cython, 3.3.1 here, read in its `PyrexTypes.py` and `Code.py` (M8's review),
  which a later Cython may change: the spec test holds the sizes, and a compiled test reads
  the generated C, which Cython writes alike for every compiler, and holds each 2-D cache
  to a temporary of its own shape, the guard a build with MSVC has. So the timings and
  kinds keep their cells and their width of four, which every SEC model's conventions read,
  and the cohorts alone carry the wide cache (*Departures from IP_UK_S*, above).
- **No refusal formatted on a chain.** A compiled cell's C frame holds the code that
  formats each of its messages, whether a run reaches it or not, and a chain holds a frame
  of each cell it recurses through at each level (UKLIB-SEC-PLAN.md K12). The chains here,
  the healthy count `pols_active`, the cohorts' diagonal and the three cumulative counts,
  format nothing; `proj_len()`, the rates' reads of their tables and the cells that refuse
  a value past the floats are each held once on a path, at its head or its foot, which a
  test holds on every cold head's deepest path.
- **The checks' loops.** `IP_UK_S`'s `check_pols_roll_fwd` and `check_states` are `all()`
  over a generator, which compiles to a Python closure inside the cell; here each is a
  loop over the frame that returns False at the first month outside the tolerance, a NaN
  among them: the same verdict at the same month, in C.
- **Six powers raise as modelx does.** Past the largest float, Python's float power
  raises `OverflowError` where C's `pow` gives an infinity. So the benefit's and the
  premium's steps, expense inflation and the discount factor, each inside the `try` that
  names its refusal, and the premium history's two even paths in `proj_len()`, inside the
  `except` that reads their overflow as the cap's path, call Python's own power where
  theirs is infinite from a finite base (uslib's *Record — M22* form). Only inputs far
  outside the product reach them (*What it refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `escalation()`, `premium_basis()`, `recovery_basis()` and `status()`, and the three
  reports return a table row, text and DataFrames, for a reader, for `run_sec.py` and for
  the comparison with `IP_UK_S`. No other cell calls them, so they cost the projection
  nothing. Each label refuses any value but its column's codes, as `IP_UK_S`'s
  `escalation`, `premium_basis`, `recovery_basis` and `status` do, and as `sex` now does
  where `IP_UK_S`'s returns the column as read, so each returns text or raises, and
  compiles to `str`.

The `Data` docstring lists its 31 vectors, arrays and extents, each with the column or
file it comes from. The ten readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 80 of
its 89, returns a C `bint`, `long long` or `double`, and caches a single value, or a C
array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 746 by `t`, of `double`, `long long` or `bint` | the 39 cells of `t` alone: every count, rate, amount and cash flow, the cumulative counts, the residuals, the policy clock, its years, the attained age, the discount and inflation factors, the live claim durations and the flag `is_active` |
| a C array of 746 by 4 | `pols_if_at(t, timing)` and `claims(t, kind)` |
| a C array of 747 by 626 | `pols_sick_dur(t, z)`, the cohorts |
| a C array of 626 by `z` | the seven cells of one claim duration: its year, its recovery and in-claim mortality rates, annual and monthly, its survival, and the opening cohort |
| one `bint`, `long long` or `double` | the 31 other cells without a parameter: the point's numbers, codes, schedules and flag, its opening state, the ends of its frame, its longest claim durations, the escalation rate, the maximum benefit, the present value and the annuity factor, and the three checks |
| a Python object, or `str` | the nine reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary. A compiled
`Projection` ItemSpace is a C struct of 6,082,800 bytes, the cohorts' cache 5,611,464 of
them, a double and a C `int` flag for each of its 467,622 cohorts.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three
reports and the three checks on every committed point, and then the cells no report
reaches: `model_point()` and the five label accessors, which only a reader asks for;
`point_id()`, which only a refusal names; `occ_class()` and `deferred_weeks()`, which the
inception rate reads through its schedule instead; the present value, its discount factor
and the annuity factor, a companion no report reads; and the codes and keys the reports
leave: the count at `BEF_DECR` and `AFT_DECR`, which no cell reads, and the cohorts
outside the live ones, at claim duration 0 and past `claim_dur_live(t)`, which no sum
reads. It calls every timing and every kind, the claims total among them, in every month
of the frame and the month after it, and every cohort from 0 to `max_dur()` in each.
Every code inside the one width but the timing 3, which `pols_if_at` refuses, is one its
cell takes, so no call raises: a raise is not traced. It runs the committed points alone:
the export reads the CSVs of the directory the build is made in, which in place is the
product directory. The committed points leave branches untaken: a lapse rate at its
bound, the caps on mortality and inception, the RPI's floor and cap, the inception floor,
the recovery rate's bound. That still types every cell, because every branch of a cell
returns the one type its others return, a count or an amount a float in every branch,
and on points that take those branches the compiled model computes modelx's numbers
(above). The labels need no trace beyond the committed points: each refuses what is not
its codes, so each returns text alone. The sample also raises the recursion limit, which
modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more but the cohorts' month, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 746 | 745. The longest frame is the longest cover, a policy issued at 18, `issue_age_min`, to expire at 70, `expiry_age_max`, issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × (70 − 18) + 120 = 744 months, `t = 0 … 743`, and the month after, 744, whose roll-forward residual reads the count carried into 745 |
| `t`, `timing`; `t`, `kind` | 746 by 4 | `t` as above, by the three timings and by `claims`' three kinds and the total |
| `z` | 626 | 625, `max_dur()` at the longest cover, 624 months and a cohort of headroom, `IP_UK_S`'s: 12 × (70 − 18) + 2 sizes it, which the horizon does not move |
| `t`, `z` | 747 by 626 | the cohorts, at every month of `t` and every claim duration; `t`'s months and one more, an outer size no other 2-D cache has, so that it may hold its own width (above) |

The cohorts' cache is the model's one wide cache: 747 × 626 doubles, 3.7 MB a point, and
as many flags, 5.6 MB with them. No cell takes a year or an age: a claim duration year, a
policy year and an attained age each index a `Data` array, never a cache, so the 53 years
and 70 ages UKLIB-SEC-PLAN.md §6.3 sized for are no caches here.

**The contract the caches hold.** `proj_len()` refuses an issue age below
`issue_age_min` and an expiry above `expiry_age_max`, and `Data` a point issued more than
`future_horizon_mth` months ahead, so that no report on a point the model projects runs
past these caches at the shipped bounds. Moved, they could: a lower `issue_age_min`, a
higher `expiry_age_max` or a longer horizon lets a point's cover pass 624 months or its
frame 744, and the compiled model would read a claim duration or a month past its caches,
raising `IndexError` naming nothing, where modelx projects. So `proj_len()` refuses, in
either engine, naming the point, a cover longer than 624 months and a frame longer than
744, however the five are set: `point_id 1: its cover, 636 months from issue at 18 to
expiry at 71, is longer than 624, the longest the compiled model's caches are sized for
(spec_sec.py)`. That is a refusal the in-force step did not make, of points it projected,
which no shipped contract writes. A contract with longer covers needs the sizes derived
again, as `spec_sec.py` derives them, the two bounds moved with them, and a rebuild.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as a loop's claim duration, stays a Python object, though the cell is
typed `double`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of each decrement
here, is a complex power, whose last bits can differ from Python's; and gcc fuses a
multiply and an add where the target has the instruction, one rounding where Python rounds
twice, which the compensated sums would carry. The tool's docstring has the detail, and
uslib's [`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the
measurements that put each there. With all four, every compiled value here agrees with
modelx bit for bit.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
6,082,800 bytes, the type's basic size, which holds every cell's cache, the cohorts'
5.6 MB among it, and deleting it, `del model.Projection[idx]`, frees nothing by itself:
an ItemSpace sits in reference cycles, and only Python's cyclic collector frees it. That
is why `run_sec.py --block` collects after each release, in its frame pass and in its
projections (*Run it*, above), and a test runs the compiled runner on the committed table
and finds no ItemSpace but the base alive after each collection. A block of a thousand
points held at once would take about 6 GB; released, it holds one.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows is a cold one
in the last month of the longest cover, a policy issued at 18 to expire at 70, now or 120
months on, or in claim a year at the valuation date: one cell a month back to
`t_entry()`, 611 to 623 months, and in modelx 5 to 8 cells more, which a test holds head
by head (*Counts and timings*, above). Compiled with gcc, each head cold in an ItemSpace
of its own, every head ran on a thread of 136 KiB and not of 128, and the healthy count
and the cumulative count on 128, but the oldest cohort the last month can hold, whose
diagonal runs back to the month it opened and there into the healthy count's chain, which
needed 144 KiB and not 136: well inside the 256 KiB the C step allows itself here, which
keeps the 1 MiB thread with K12's margin of two to four on CI's Ubuntu runner. So no chain
is blocked by policy year. A test runs each shape at its longest cover in a thread of 1
MiB, the stack Windows gives a program's main thread unless the program is linked for
more, and again on the main thread, which is where `run_sec.py --cython` runs, and records
the smallest of its sizes each ran on. The export recurses in Python instead: the same
call needs a recursion limit of 1,282 there, two Python frames a cell, and the reports and
checks, which run in ascending `t`, need 36, so `sample_sec.py` sets 6,000.

**Pickling, a known limit.** A compiled point does not pickle:
`pickle.dumps(model.Projection[8])` fails, `Memoryview is not initialized`, from `Data`,
whose arrays are typed memoryviews. Its state alone, through Cython's `__reduce_cython__`
and `__setstate_cython__`, reads back exactly on a thread of 8 MiB of stack and crashes
the interpreter on 4, 2 and 1 MiB, since the unpickle function holds the cohorts' two
temporaries, values and flags, 5.6 MB, on the C stack (measured at M8's review). Nothing
in the library pickles a point: `run_sec.py` and the tests' children pass values, never
points.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message, on an
extract labelled otherwise than by position, its claim cohorts relabelled alike: each
malformed row of the table and of the companion, each writing of the escalation flag, each
assumption table a reader cannot read, each point the frame refuses, the contract moved
past the caches among them, each Reference off its domain, each escalation history the
contract cannot have, each value past the floats, by its cell and by a report, a key read
beyond the mortality table, `Data`'s References off their domains, and what the vectors
cannot hold, in a cell typed `long long` or `double` as in a Python one. Two engines that
agree could both name a point by its place in the table, so each refusal of a point's own,
by its frame, a Reference, its history, a value past the floats or a rate its tables do
not hold, must begin `ValueError: point_id <label>:`, the extract's label, in both
engines, and the test counts them; the modelx tests of those refusals run on such an
extract too.

A message prints each Reference as the compiled model holds it: a rate or an age bound as
a float, an age bound through `int()` once it is whole; and it names a timing or a kind by
its code, `claims(0, 0)` for the benefit, in both engines. Every Reference with a domain
is a float, the contract's four ages and `Data`'s horizon and interpolated ages among
them, so a fraction set on one is the fraction in either engine, refused as not whole in
both: 12.5 set on the horizon is refused compiled as in modelx, where an int Reference
would be truncated to 12 as it is set. The refusal test sets `Data`'s References as it
sets `Projection`'s.

- What `Data` cannot decode or hold, when the vector is first read, naming every point or
  line at fault: a `point_id` that is not a whole number, or is `2**53` or more in size;
  an age or a month `2**53` or more in size, which an int64 vector cannot hold whole and
  numpy would cast without a word; a key of an assumption table or of the companion as
  large, before its table is cast; and, as since the in-force step, a code that names no
  sex, escalation, premium basis, status or recovery basis. A key written as a float, an
  age `40.0`, is read by its value. The tables' checks find a gap from the keys a table
  holds, in one pass, so that a key far from the rest is refused as a gap at once.
- A key beyond a table, by the one cell that reads it, where `IP_UK_S`'s lookup raised
  `KeyError` or extrapolated: `point_id 1: mort_table.csv has no rate at attained age 35`
  on a table that starts at 40, and `point_id 1: inception_table.csv is interpolated at
  attained ages 36 to 69, Data's rate_age_min to rate_age_max, not at 35` under a first
  age raised to 36.
- A cover or a frame past the caches, by `proj_len()` (*The sample and the spec*).
- A value past the floats, in the cell where it first is, naming the point, the month
  and what makes it: the benefit, the premium, the lapse shock, the premiums, the claims,
  the expenses, the net cash flow and the present value.
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: the benefit's and the premium's steps,
  expense inflation and the discount factor each call Python's own power where theirs is
  infinite from a finite base, so that the compiled model refuses as modelx does (uslib's
  *Record — M22* form), rather than carry an infinity on; a test reaches each with a rate
  of 1e200, or a discount rate a hair above −1. The premium history's two even paths in
  `proj_len()` take the same form inside the `except` that reads their overflow as the
  cap's path, which a test reaches under a premium multiplier of 1e150, in both engines;
  there the cap's path is past the floats too, so C's infinity would read the same.
- A timing or a kind no cell takes, by the cell, as `IP_UK_S`'s are: `invalid timing`,
  the timing 3 inside the cache's width among them, and `invalid kind`.

An argument outside a cache raises `IndexError` in the compiled model alone: `net_cf(746)`
or `net_cf(-1)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(t, 4)` and `claims(t, 4)`, which modelx refuses as a timing and a kind it does
not take; `claim_dur_year(626)`, a claim duration past the `z` cache, whose year modelx
computes as it computes any; and `pols_sick_dur(747, 1)` or `pols_sick_dur(0, 626)`, past
the cohorts' cache, a cohort modelx answers with 0. No frame asks for any of them: a
frame's last month is at most 743, and its longest claim duration 625. An `idx` past the
last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's last
point, under that point's own `point_id()`, its cohorts the last row's; the compiled
refusal test holds both against modelx.

An annual mortality or inception rate above 1 is not refused but capped, in both, and so
is the recovery rate and the lapse rate, the RPI's steps floored and capped, and the
inception rate floored at 0: a compile test holds the two engines equal where each binds,
on its own rows.

### Speed

`python tools/bench_sec_cy.py income_protection` builds the model into a temporary
directory and times one block run on three engines: modelx, the export and the compiled
model. Each engine runs the committed table repeated, in a process of its own, as
`run_sec.py --block` runs a block, each point projected and then released. `net_cf` is
`net_cf(t)` summed over the frame, the projection alone, as `basiclife/BasicTerm_SC` is
timed on its `pv_net_cf()`; `result_cf` is the report `run_sec.py` prints, which builds a
DataFrame for each point. Each run of the tool takes the fastest of three runs of each
engine and loop. The tool was run three times, on one build, `--build`, with modelx's
block one copy of the table, since a modelx point takes a second and a half here, and
each time below is the median of its three, with the range of the three beside it:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,004 | 2.82 ms (2.73–2.82) | 3.36 ms (3.31–3.37) | 134 MB |
| export | 608 | 56.7 ms (56.1–57.1) | 57.0 ms (57.0–57.7) | 99 MB |
| modelx | 19 | 1,430 ms (1,420–1,460) | 1,470 ms (1,450–1,490) | 280 MB |

On `net_cf` the compiled model runs 20.2 times its export (19.9 to 20.8 over the three),
and on `result_cf` 17.2 times (16.9 to 17.2); it runs 508 times modelx on `net_cf` (504 to
534) and 437 on `result_cf` (431 to 451). The cohorts are the work: a point forms its
claim cohorts, a triangle of its months by the claim durations that can hold lives, and
sums them four times a month, so a point costs more on every engine than one of
`WOL_UK_SEC`'s, which ran 0.40 ms compiled, and modelx most, each cohort being a cell
whose dependencies it records. The release keeps a block flat: the compiled model's peak
grew by 0.3 MB at most over its 6,004 points, each ItemSpace's 6 MB freed as the next is
made, and the export's not at all, where modelx's rose by 181 MB over its 19. Reading the
six files and building every `Data` vector and array for the compiled block took 0.38 to
0.41 s, and asking every point for its frame, the runner's first pass, 1.47 to 1.52 s.
Every engine, loop and run summed `net_cf` over a copy of the table to the same
−834,758.3005, to 1e-9 relative.

Measured on 2026-11-24 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.10 GHz), a 1-minute load average between 3.8 and 5.8 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1, 3, 4 and 6,
  every cell of `IP_UK_S`'s agrees at every argument `IP_UK_S` evaluates in its own sweep,
  to 1e-9 relative with no absolute floor, but for `pols_if_init`, `model_point` and
  `claim_duration_months`, which the spec names with their reasons. So `IP_UK_S`'s worked
  example, which `tests/test_income_protection_uk.py` asserts, holds here with no number
  restated. The same suite holds the model to the conventions every `_SEC` model meets:
  every frame starts at `t = 0`, `pols_if` is the `"BEF_DECR"` count, new business enters
  once at its `policy_count`, nothing happens before issue, and the in-force columns are
  present.
- **The splice**, in `tests/test_income_protection_uk_sec.py`: each `IP_UK_S` point
  restated in force at months about its events — the anniversaries, 11 to 13; the lapse
  table's last year, 59 to 61; the inception table's pivot ages; the claim-duration years
  of the two claims on the exit basis; the first month and the last two — and the twins of
  S's claims on their policy clocks, continue the S projection in both reports and in every
  cell the two share, the cohort vector element by element among them, to 1e-9 relative
  with no absolute floor, the residuals at 1e-9. Four kinds of cell are compared otherwise:
  `proj_len`, which counts from the valuation date, by the frames ending together; the
  cumulative counts, which restart on the books, by their increments; away from month 0
  the discount factor, the present value and the annuity factor, which discount to each
  model's own start, by a test of their own; and on a row of one of S's claims the clock
  and cohort cells, by checks that its policy clock is S's plus `12n`, its issue age S's
  less `n`, and its cohort vector S's, with zeros past S's length. Every assumption that ships
  idle is on: the escalation lapse shock at an RPI of 5%, beside the cycle overlay at 1.25,
  the active-life mortality factor at 1.1, the amount-payable ratio at 0.9 and the claim
  severity at 0.95; and three more sets reach the escalation cap at 12%, the RPI's floor at
  −2% and the recovery rate's bound at an overlay of 0.35. Expense inflation, the one input
  on the valuation clock, is 0 in both. Three variants of S's points, in a copy of S's
  table that is never committed, reach an active cell on the exit basis, the youngest
  attained ages below the inception table's first pivot, and the oldest entry to the latest
  expiry, past its last. A core of 25 of the 95 splice cases and 5 of the 18 future ones
  runs by default, and the full grid with `UKLIB_SEC_FULL=1`; a test asserts the core
  reaches every branch, opening-state column, month-0 event and side of every `min` and
  `max` the full grid reaches. Point 7 and its rows are spliced under a flat lapse table,
  and their difference at the shipped table asserted, the twin's clock a year ahead of
  S's restarted one; and the inception rate's floor is spliced on a copy of the inception
  table with a schedule below 0, which no shipped schedule reaches.
- **Future new business**: issued 1, 12 and 120 months after the valuation date, each S
  point is the S projection moved on, with zeros before issue and no table read there, and
  so is each variant issued 13 months on.
- **How it computes**: on every row of the splice's grid, after its reports, its checks,
  every monthly cell at every month and the cells of a month and a timing, a kind or a
  claim duration at every argument C4 asks, the cohorts in the month a row is first on the
  books among them, no cell has been called at a negative month, none on the books read a
  month before `t_entry()`, none read a month later than `t + 1`, and none raised: a
  cohort base at `t == 0`, which moves no number, reads before issue on a row issued
  later. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, and every point's reports and checks run under modelx's recursion
  limit lowered to 40. And each chain, called cold in the last month at the contract's
  longest cover, 624 months, on four shapes, runs one cell a month back to `t_entry()`,
  the cohorts' down their diagonal, and at most its head's own measured overhead more: at
  the in-force step, the cohorts a tuple, a cold `net_cf` ran 8 or 9 more, 631 to 632
  deep; since the C step it runs 7 more, 630 deep, the healthy count 5, the oldest cohort
  5 or 6, the cumulative count and the population identity 6, the lives in claim, the
  roll-forward and the count by timing 7, and the benefit claims 8. No cell a chain
  recurses through builds text, which a test holds on each head's deepest path.
- **Counts**: the counts roll forward through the states; `result_pols()` is S's counts and
  amounts with `pols_new_biz` beside them; multiplying `policy_count` by 2.5, with every
  idle assumption on, multiplies every flow and counted cell, each cohort element among
  them, each nonzero on some point, and moves no per-policy value, bit for bit, but the
  annuity factor, the present value over the count, a ratio of two scaled sums, which
  agrees to 1e-12; a point restated a month on continues its own flows; and both checks
  close on ten million policies.
- **Validation and regeneration**: each malformed row of the table, 75 cases, a missing
  column among them, and of the companion, 23, is refused naming its point or its lines,
  and naming its label on an extract labelled otherwise, table and companion alike; the
  horizon is a Reference; a point past its policy end date is refused by `proj_len()`, and
  `run_sec.py --block` refuses it before printing anything; so is a point outside the
  contract's bounds, 9 cases; so is an escalation history past them, each bound a cent
  outside and accepted half a cent inside, beside two histories the contract cannot have
  and the committed history under a contract it was not written under, 11 cases; each of
  23 References off its domain, the value next outside each edge, NaN and both infinities,
  where each edge is accepted; a value past the floats, 12 cases, where it first is, the
  lives in claim among them, whose sum leaves the floats as `sum`'s infinity, as each
  cohort sum's does on an input that takes it there; each refusal of a point's own, by its
  frame, a Reference, its history or a value past the floats, on an extract labelled
  otherwise than by position, beginning by naming the point by the extract's label; each
  assumption table with one fault, 42 cases, before a value of it is read; the edges of
  the interface, the shares' tolerance pinned from both sides and an escalated amount half
  a cent below its issue value among them; and every state `IP_UK_S` reaches, under the
  shipped References and four sets more, at the edges of each frame's windows, or at every
  month with the full grid. The committed CSVs are what the generator makes of `IP_UK_S`
  today.
- **The product's own facts**: the two clocks; the present value and the annuity factor
  on the valuation clock; the committed rows continuing their S points, the two read
  under an RPI of their own continuing S under it; each history column read rather than
  rebuilt, the healthy share, the claim cohorts, the benefit and the premium; an
  anniversary at the valuation date as the projection's first event; the cumulative counts
  restarting on the books; expense inflation on the valuation clock; the RPI's floor, cap
  and lapse shock; the caps on mortality and inception and the lapse rate's bound, in both
  models; a NaN that reaches a cap; a check whose residual is NaN; the values outside
  cover; the block; an in-force extract, without the generator's columns or `status`; the
  runner; the static check the C step made; the docstrings; and the shared tables.
  The K14 tests open the anchor cell in force at 60 with histories the contract can have:
  the benefit and premium `IP_UK_S` gives it under an RPI of 5%, valued under today's 3%.
- **The fingerprint (C2)**: every committed point's `result_cf()` and `result_pols()`,
  frozen when the in-force step ended, in a commit of its own, which every later version
  must reproduce to 1e-12, and which the C step does.
- **The C step's representation**, in modelx, in seconds: the claims total by its bits,
  the twins' skipped on Python 3.11;
  the cohort sums and the present value against `sum` by theirs, on every committed point
  in every month, and against `IP_UK_S`'s own on its twins, the months a plain sum parts
  from `sum` counted, all of which skip on Python 3.11, whose `sum` adds left to right;
  the cohorts past the live ones 0 and the oldest of the live ones holding lives; each
  sum's order of reads by modelx's stack trace; every schedule at
  every age of the inception and mortality arrays against `IP_UK_S`'s rates, on the
  shipped inception table and on the floor's; every decode on every value, and the
  escalation flag written `" True"`, `"True "`, 1, 1.0, `True`, `" RPI"`, `"RPI "` or
  `rpi` refused as the table is read; the padded arrays; each `Data` vector's dtype
  against the `Data` docstring's table; the parameterless cells' Python numbers; the
  labels' refusals; the spec's sizes, the codes and `proj_len()`'s cache bounds against
  the spec's comment; the sample's recursion limit against its comment; the runner's
  rebuild; and what the vectors cannot hold.
- **Compiled**, the tests marked `cython`, which compile the model once a session and run
  the compiled package in a child process: C4, every cell at every argument a full modelx
  sweep evaluates, with every code and claim duration no swept cell reads (`_ip_c4_also`,
  which a test holds to asking each, row by row, the codes each cell takes derived in
  modelx on each row C4 compares, not read from the test's own lists), on the splice grid
  under each set of References, at the contract's extremes, where each cap, floor and
  bound binds, on every inception schedule, on keys written as floats, on every committed
  row, under the References two of its rows were read from, and on the rows valued on an
  anniversary, each grid in chunks sized by the squares of its frames, each chunk asserted
  to compare its own rows; the labels; the refusals and overflows, message for message,
  each refusal of a point's own naming the extract's label in both engines, 296 of them
  counted, with the refusals the compiled model alone makes and `idx` at the table's
  edges; each 2-D cache read back, as a point is unpickled, through a temporary of its own
  shape in the generated C; each shape's deepest cold calls on a 1 MiB stack and on the
  main thread; a Reference set late; and the runner.
  `tests/test_compiled_conventions_uk.py` adds C3, C5 and the release.

**Time and memory** (UKLIB-SEC-PLAN.md U6, K6). Measured at M8's rework, after its review,
on the shared 4-CPU machine, at a 1-minute load of 1.0 to 3.2, each peak the largest
resident size of the run's processes: the module's default run takes 1,603 s at a peak of
2,709 MiB, and without its compile tests, `-m "not cython"`, as the `sec_uk` job's legs
run it, having no compiler, 808 s at 2,564 MiB. On the full grid without them,
`UKLIB_SEC_FULL=1`, as the `sec_uk` job's Linux leg runs it, 1,967 s at 2,950 MiB, and the
`cython_uk` job's `income_protection` shard on the full grid, its Linux leg, 1,414 s at
3,537 MiB: each inside its job's hour. The in-force step's default took about 190 s alone
at 1.4 GB. Both defaults are past the five minutes U6 budgets, and the C step's
restructure is why: modelx records each cell's dependencies as it computes it, and the
claim cohorts, a tuple a month in the in-force step, are each a cell now, read by four
sums, so that a point costs modelx about five times what it did, the committed points'
fingerprint 42 s where it took 7.6. That cost memory too: as the C step left the module,
its peak was 5,884 MiB without the compile tests and 6,139 MiB with them (M8's review), 2
GB of it the committed points, swept once and held for the module at about 2.9 KB a cache
entry. So the module now keeps each committed point as its sweep left it, its values
alone, the cohorts an array of the months by the claim durations and the rest a dict,
about 0.2 GB for the 19, and releases its ItemSpace, collecting after some 700 MB of
released points (`sec_read`); every test on the committed model reads the kept values as
it read the swept points, and a call the sweep did not cache, of which the tests make few,
is computed on the point read afresh and released as the test ends. Kept, the model takes
no Reference: one set on its `Projection`, its `Data` or a point raises, naming K7, where
the swept model would have recomputed, and a test holds that. The sweep takes 63 s where
it took 43, and the peaks are 3,320 and 3,430 MiB lower. What sets the peak now is a
test's own models before Python's cyclic collector frees them, a closed model sitting in
reference cycles until it runs: the in-force interface's edges, a 624-month cover among
their rows, and the states S reaches, restated after them. Without the compile tests the
module peaks at about 2.5 GiB, leaving more than 4 GB of the 7 GB of the macOS `sec_uk`
legs, the smallest CI runners, before their system takes its share. The default run's cuts
are made already, each case on the full grid in full: the domain test's accepted edges
project on a frame of 120 months where their own point's is 360, the month-on restatement
and the cohort sums run on the core's points, the cold chains on one frame of the anchor
cell, the chain-text test reading the depth test's traces, and the compiled comparisons
under References of their own on the rows each binds on or was read for. What is left of
the modelx part is the splice's core, about 80 s; the cold chains at the longest cover, 87
s; the committed points' sweep, 63 s; the counts' scaling, the checks on ten million
policies, the restatements and the domains, under a minute each; and the rest, each test's
own rows. The compile tests take about 13 minutes, the build 2 of them, the contract's
extremes, the splice grid's core and the refusals near 2 each, and the committed rows, the
stack and the compiled runner about one each. A cut to five minutes would leave the
splice's core a few rows, take the longest cover's chains, and with them the stack's
chains, off the default run, and move the compile tests to the full grid, which the
`cython_uk` job's Linux legs run: its Windows legs, which run the default, would then run
no compiled comparison with MSVC.

```bash
python -m pytest tests/test_income_protection_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_income_protection_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k IP_UK_SEC
UKLIB_CYTHON_SHARD=income_protection python -m pytest -m cython tests -q     # compiled
```
