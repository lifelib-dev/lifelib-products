# In-Force Implementation Notes

**Status:** Draft, 2026-11-23. `WOL_UK_SEC` is [`WOL_UK_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year, on full cover or paid-up, and policies to
be written in the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes, and how the model compiles. The suffix adds lifelib's letters to
`S`: `E` for in force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model (UKLIB-SEC-PLAN.md U2).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `WOL_UK_S` on another time axis, and it reads `WOL_UK_S`'s assumption tables in place,
> every assumption unchanged: the contractual mechanics are sourced, and every rate is a
> **[std]** standardization, the two mortality bases proxies shaped like the tables the
> notes name, whose current editions are restricted to the CMI's Authorised Users
> [REG-R22] [R7]. Replace them with licensed tables and company experience before drawing
> any conclusion from the numbers.

## Run it

```bash
python products/whole_of_life/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/whole_of_life/run_sec.py 10         # point 10: the paid-up point in force 200 months
python products/whole_of_life/run_sec.py --block    # every model point, summed row by row
python products/whole_of_life/run_sec.py 10 --cython # point 10 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the library's own `build_sec_cy.py` the first time, in about a minute, and
again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. Nothing the build leaves there is committed, and `.gitignore`
covers it.

The first prints the twelve rows `run.py` prints for `WOL_UK_S`'s point 1, with the policy
counts behind them. Three lines to the same thing for point 10:

```python
import modelx as mx
model = mx.read_model("products/whole_of_life/WOL_UK_SEC")
model.Projection[9].result_cf()      # point 10, the table's tenth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `WOL_UK_S`'s takes a `point_id`: `Projection[9]` is point 10, and its
`point_id()` says so. `result_cf()` has `WOL_UK_S`'s columns — `pols_if`, `pols_pu`,
`premiums`, `claims_death`, `claims_death_pu`, `claims_lapse`, `expenses`, `commissions`
and `net_cf` — with one row per month from the valuation date, `t = 0 … proj_len() − 1`.
`result_pols()` sets out the counts behind it on the same rows, on both strands:
`pols_if`, `pols_new_biz`, `pols_pu`, then the month's deaths on full cover and paid-up,
its lapses and conversions to paid-up in processing order, the survivors at the limiting
age, and `WOL_UK_S`'s other five columns, the premiums paid, the cover, the benefit per
death and the annual mortality and lapse rates.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[9]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`. Its projection years carry the counts
of their first month, on full cover and paid-up, and the flows of all twelve.

The runner is uslib Term's, and `--build DIR` runs a build made elsewhere (*The compiled
model*). The tool goes with the library, into lifelib and into a `lifelib.create()` copy,
so `--cython` builds there as here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the limiting age.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the lapse table's key, and
  `age(t) = age_at_entry() + duration(t)`, the mortality table's, age last birthday, as in
  `WOL_UK_S`. Whole of life has no maturity, so cover runs to the limiting age, policy month
  `limit_mth() = 12 × (omega_age − age_at_entry())`, `WOL_UK_S`'s frame from issue.
  `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion as long as the
  frame; the closed form needs no such chain of calls.

Point 10 is the pro-rata paid-up point in force 200 months. At `t = 0` it is in policy year
17 at attained age 86, with 0.180202 policies on full cover and 0.057170 paid-up, and its
frame has 400 rows, `t = 0 … 399`; `WOL_UK_S` projects the same months as its rows 200 to
599. Point 14 is the RPI point to be issued 13 months after the valuation date:
`duration_mth(0) = −13`, it is on the books from `t_entry() = 13`, rows 0 to 12 are zeros,
and its frame has 613 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the mortality table at the attained age; the lapse table by policy year; the over-50s moratorium and the underwritten suicide window, each the first twelve policy months; the escalation on each policy anniversary; premium cessation, and with it the end of lapses; the payments made that the pro-rata paid-up value counts; the first year's commission; the crossover; the limiting age | expense inflation, `inflation_factor(t) = 1.03^(t // 12)`; mortality improvement, `mort_improve_factor(t) = (1 − r)^(t // 12)` |

Expense inflation and mortality improvement run on `t`, stepping on each anniversary of
the valuation date, for every point alike (USLIB-SEC-PLAN.md D7; UKLIB-SEC-PLAN.md §9
item 4). The maintenance charge is then in valuation-date pounds, and the mortality tables
state their basis at the valuation date, improved from there: `WOL_UK_S` improves from
issue, which on a point in force would improve a table stated today by the years the
policy has already run. Improvement ships at 0, where the two clocks agree. The RPI is a
flat Reference, the rate assumed from the valuation date on. The acquisition expense,
£150 or £300 per policy issued, is charged in the issue month and not inflated, as in
`basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[p].result_cf() for p in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`WOL_UK_S` computes: every cell the two models share agrees, but two whose meaning changed,
`pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table. `WOL_UK_S` charges the acquisition
expense on the count in force at `t = 0`, which on such a point is the count issued, so
the two agree at any count.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `WOL_UK_S`'s columns, one
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s name, a policy
clock column, a second count and five columns of opening state. The two counts are the
only weights on the flows, and every state column is per policy. Each is measured at the
valuation instant, the start of month 0, before any month-0 event (USLIB-SEC-PLAN.md D6).
An anniversary that falls at the valuation date is month 0's event, the projection's
first: the cover and premium columns hold the policy year it closes, and its increase is
made at `t = 0` at today's References, as a fixing at month 0 reads the assumptions of the
valuation date (D6, as precised at uslib's M7). Each state column is history: what the contract has given, charged or converted, never re-derived from a
Reference, which is an assumption from the valuation date on, so that a Reference changed
there reaches back over no increase, premium or conversion already made
(UKLIB-SEC-PLAN.md K14, §9 item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies on full cover, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies on full cover in force at the valuation date, for a point already in force, 0 if it is paid-up entirely; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `pols_pu_init` | paid-up policies, 0 or more | the start of month 0 | the policies already converted to paid-up by the pro-rata paid-up value, the second strand's count |
| `pu_benefit_pp_init` | pounds per paid-up policy | the start of month 0 | the paid-up cash sum each carries on average: each policy's `SA × N_paid / N_expected` at the month it converted, averaged over the strand |
| `prem_cum_pp_init` | pounds per policy on full cover | the end of month −1, before month 0's premium | the premiums paid since issue, which the moratorium and suicide refunds pay back and the crossover stress compares with the cover |
| `cover_pp_init` | pounds | the start of month 0, before its events: the policy year of month −1, which on an anniversary is the year it closes | the cash sum in force, after every increase the RPI or the fixed step has already given |
| `premium_pp_init` | pounds a month | as `cover_pp_init` | the premium of that policy year, after every increase already given; once premiums have ceased, the last premium paid |
| `crossover_mth_init` | a policy month, or −1 | the valuation date | the policy month the premiums paid first exceeded the cover, if that was before the valuation date, and −1 if it was not: a crossover in month 0 or later is the projection's |

`WOL_UK_S` holds none of them. It rebuilds the cover and the premium from issue at one
flat `rpi_rate`, or at `esc_fixed_cover`, `esc_fixed_prem` and `esc_take_up`; the
premiums paid by summing that schedule; the paid-up strand by converting every would-be
lapse since its halfway point at today's lapse table and crossover stress; and the
crossover by searching that schedule from issue. On a point in force those are facts of
the contract: an RPI set at the valuation date would reprice increases long given and move
a crossover already past, a take-up would reach back over increases already taken up or
declined, and a stress would convert lapses long past. Here an increase after the
valuation date steps at today's References, and one at or before it is the history the
columns carry:

- `cover_pp(t)` and `premium_pp(t)` open at `cover_pp_init()` and `premium_pp_init()` and
  take `1 + step` for each anniversary since the columns' year, `duration(t) −
  duration_init()`, `duration_init()` being the policy years of month −1, so that an
  anniversary at the valuation date steps them at `t = 0`;
- `prem_cum_pp(t)` opens at `prem_cum_pp_init()` plus month `t_entry()`'s premium and adds
  each month's after;
- `pols_pu(t)` and `pu_benefit(t)` open at `pols_pu_init()` and at
  `pols_pu_init() × pu_benefit_pp_init()`, and take in each month's conversions;
- `crossover_mth()` reports `crossover_mth_init()` where the crossover fell before the
  valuation date, and otherwise searches forward from it, the premiums paid accumulating
  from `prem_cum_pp_init()` and the premium and cover stepping from the columns.

The fixed variant carries its cover and premium columns as the RPI one does: its increases
are a fixed 5% and 10%, but at the take-up of their day. And the paid-up strand needs no
history of when its policies converted: paid-up policies neither lapse nor escalate, so the
count and the summed cover roll forward on the same survival factor, and the average is all
the strand needs.

On a point issued at the valuation date each history column holds its issue value, and the
model is `WOL_UK_S`. A model that dropped the columns and recomputed them from the
References would pass the splice, since `WOL_UK_S` and the splice recompute them alike, so
the tests write each off its References' path and project through it.

The crossover is reported, and no cell of the projection reads it: the crossover stress
compares the premiums paid with the cover month by month. Carried back from the columns at
today's increases, as the model first did, it was wrong wherever the history ran
otherwise: the RPI point restated after a crossover at 166 under an RPI of 0 reported 166,
150 and 137, and one at 201 under 8% reported 220. As a column it is the history's.

Nothing else is history `WOL_UK_S` rebuilds from a Reference: commission is paid in the
first policy year alone, on the premiums of that year still to come, with no clawback; the
acquisition expense falls at issue; the moratorium and the suicide window read the
premiums paid; and inflation and improvement run from the valuation date.

| `WOL_UK_S` | `WOL_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The full-cover count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months, any month of a policy year; every `WOL_UK_S` point is new business |
| — | `pols_pu_init`, `pu_benefit_pp_init` | The paid-up strand in force; `WOL_UK_S` builds it from issue at today's lapse table and stress |
| — | `prem_cum_pp_init`, `cover_pp_init`, `premium_pp_init`, `crossover_mth_init` | `WOL_UK_S` rebuilds each from issue at its References: the premiums from the schedule, the increases from `rpi_rate` or the fixed step and the take-up, and the crossover by searching both |

The columns carried over are read as `WOL_UK_S` reads them. For a policy in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `cell`, `sex`, `smoker`, `escalation` | codes, as in `WOL_UK_S`'s table | issue |
| `entry_age` | years, age last birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sum_assured`, `premium_mth` | pounds, the amounts at issue | issue: on an escalating point the month's cover and premium step from `cover_pp_init` and `premium_pp_init` |
| `cessation_months`, `moratorium_months` | whole policy months | issue: counts on the policy clock, 0 for premiums for life or no moratorium |
| `variant_adb_2x`, `variant_paid_up` | True or False | issue |

Four more columns, `row_kind`, `source_policy_id`, `source_mth` and `source_refs`, record
where the generator took each shipped row from (below): `source_refs` names the References
a row was read from `WOL_UK_S` under, `rpi_rate 0.05` on point 15, `esc_take_up 0.5` on
point 16 and `lapse_crossover_beta 100.0` on point 17, and is blank on every row read at
those `WOL_UK_S` ships. No formula reads them, and an in-force extract need not carry
them: without them the model projects the same numbers, and `run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the eight in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, itself a whole number of months below
`2**53`, which set to 0 refuses future new business altogether; each state column is a
number, zero or more, and the crossover a whole number of months, −1 or more; each flag is
True or False; each code is one `WOL_UK_S` knows, the smoker status `NS` or `S`, not term
assurance's `N`; the entry age is a finite number, the amounts zero or more and the month
counts whole, 0 or more; and a pro-rata paid-up point has a premium cessation date, which
its paid-up value is measured to. Then the history: a point not yet in force holds the
issue values, no paid-up policy, no paid-up cover, no premium paid and no crossover, the
sum assured and the premium at issue; a point in force 12 months or fewer holds the issue
cover and premium, its columns its first policy year's, the first anniversary's increase
being the projection's; a level point holds them always, and an escalating one those or more, each increase floored at 0; the paid-up strand
is empty without the variant, and before the earliest policy month a converted policy can
be in force at, half of `cessation_months` rounded up; and the paid-up cover per policy is
0 where no paid-up policy is in force. The amounts are held to the contract, to the cent,
within half a cent of each bound, so that an extract rounded to the cent reads:

- the premiums paid are the premiums due so far, `min(duration_mth, cessation_months)`, or
  `duration_mth` for life, times the premium at issue on a level point, and on an
  escalating one between that and the same count times `premium_pp_init`, the latest
  premium, each increase being floored at 0;
- where paid-up policies are in force, the paid-up cover per policy lies between the sum
  assured times the payments a conversion needs, half of `cessation_months` rounded up,
  and `cover_pp_init` times the payments made, each over `cessation_months`;
- a crossover before the valuation date fell in a premium-paying month before it; there
  was one where the premiums paid exceed the cover; and on a level point it is the month
  the contract puts it in, `P × t* ≤ SA < P × (t* + 1)`.

Each holds of every state `WOL_UK_S` reaches, as shipped, under the splice's stress,
under one that lapses every policy, under an RPI of 8% and under a take-up of a half,
which a test asserts. `WOL_UK_S` meets most of these only when a projection reaches them, and some
never: a blank flag reads as True, and one stray word in a flag column turns every `False`
in it to text that reads as True.

A point at or past the limiting age at the valuation date, `duration_mth ≥ limit_mth()`,
reads, but `proj_len()` refuses it, naming the point: the limiting age is the product's
rule, keyed on the policy clock, not the table's. So does a point the contract does not
write ([`product-spec.md`](product-spec.md)): one issued below 18,
`Projection.issue_age_min`, the youngest age the mortality table rates and the product
issues at, or at or past the limiting age, `omega_age`, which itself must lie above
`issue_age_min`, at most a year past the mortality table's last age, and at most
`omega_age_max`, 121, the shipped table's last age plus one. Each is a lower-case
Reference, the contract the compiled model's caches are sized from (*The sample and the
spec*): a frame of at most 1,236 months, from 18 to `omega_age_max`, and the horizon, and
attained ages from 18 to 120 on the mortality table. A whole limiting age written as a
float, `120.0`, is read as the `int` it is, so that the frame is a whole number of months,
as it is compiled. And `proj_len()` refuses a point whose premiums cease past the limiting
age, `cessation_months` above `limit_mth()`, which no contract writes: the crossover's
search runs the premium-paying months, and `Data` bounds a cessation below `2**53` alone,
so that a cessation of `2**52` months on a premium of 0 would run it about 4.5e15 times in
either engine. Refused, no point the frame accepts runs the search past the contract's
longest cover, 1,236 months; premiums ceasing at the limiting age itself are payable to
the end of cover, and read. `WOL_UK_S` projects such a point, and searches past its frame;
none of its points is one. On every point `proj_len()` also refuses a Reference off its
domain (below). The References are the projection's, which `Data` cannot read. A loop
over the block meets such a row only when it reaches it, after projecting the points
before it, so `run_sec.py --block` asks every point for its frame before it projects any,
and stops before it prints anything.

The assumption tables are checked before a value of them is read, each by the cell the
projection takes its extent from, reading the file as it stands, so that a fault is named
by its line. The mortality table is checked by `Data.mort_age_first`: each age a whole
number, each basis `population` or `assured`, sex `M` or `F` and smoker `NS` or `S`, each
of the eight groups running from the table's first age to its last, one row an age, none
below 0, and each rate from 0 to 1. The lapse table is checked by `Data.lapse_last_year`:
policy years from 1 without a gap or a repeat in each cell, each cell `O50` or `UW`, each
rate from 0 to 1. A key is read by its value, so an age written `70.0` is 70. Each refusal
names the file, the column and its lines. An attained age outside the mortality table,
which only a lowered `issue_age_min` admits, is refused by `mort_rate`, naming the point
and the age, where `WOL_UK_S`'s lookup raised `KeyError`.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`WOL_UK_S` and its table by `tests/uk_sec_support.py`, from the `WOL_UK_SEC` entry in its
`SEC_SPECS`, and the tests regenerate it and compare, so an edit to a `WOL_UK_S` row reaches
it or fails the suite. In the source repository, `python tools/gen_sec_points.py WOL_UK_SEC`
writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 7 | twin | S points 1 to 7 | issued at `t = 0`: `WOL_UK_S`'s worked example and its variants, the over-50s anchor cell, with the double accidental benefit, with the pro-rata paid-up value and with RPI increases, the underwritten cell, with fixed increases, and an over-50s male smoker |
| 8 | derived | S point 1 at S month 6 | the anchor cell inside its moratorium, £180 of premiums paid |
| 9 | derived | S point 1 at S month 166 | the anchor cell in its crossover month, £4,980 paid |
| 10 | derived | S point 3 at S month 200 | the paid-up point with its strand in force, each paid-up policy carrying £3,294.64 |
| 11 | derived | S point 4 at S month 186 | the RPI point past its crossover, its cover £7,789.84 and premium £58.06 |
| 12 | derived | S point 6 at S month 12 | the underwritten increasing point on its first anniversary, its columns the first year's and its first increase at `t = 0` |
| 13 | derived | S point 7 at S month 300 | the male smoker as its premiums cease |
| 14 | future | S point 4, 13 months on | to be issued at `t = 13` |
| 15 | derived | S point 4 at S month 120, `WOL_UK_S` run under an RPI of 5% | the RPI point with a cover of `5,000 × 1.05^9` and a premium of `30 × 1.075^9`, its tenth anniversary's increase at `t = 0` |
| 16 | derived | S point 6 at S month 120, `WOL_UK_S` run under a take-up of 0.5 | the underwritten increasing point with increases of 2.5% on the cover and 5% on the premium |
| 17 | derived | S point 3 at S month 180, `WOL_UK_S` run under a crossover stress of 100 | the paid-up point paid-up entirely: `policy_count` 0, and 0.285193 paid-up policies |

A derived row's `policy_count` is the count `WOL_UK_S` carries into that month on full
cover, its `pols_if(d)`, and its state what S carries there, so the row continues the S
projection from there: point 10 opens with 0.180202 policies on full cover, 0.057170
paid-up and £6,000 of premiums paid. At the shipped References the escalating rows'
history is what today's References rebuild, and no shipped point is paid-up entirely, so
three rows are read from `WOL_UK_S` run under References of their own, which the spec's
`derived_refs` records: points 15 to 17. Points 15 and 16 are valued on their tenth
anniversary, so at the shipped References they make its increase at `t = 0` at today's
References and part from `WOL_UK_S` under theirs there, their counts S's throughout; point
17, with no full cover for its stress to lapse, projects `WOL_UK_S` under its stress
throughout, but in the lapse rates themselves, which weight no policy. A test asserts each.
A derived row's `policy_id` is the S row's with the month appended, `WOL-000003-M200`, and a future row's carries the months to issue,
`WOL-000004-F13`. Row `t` of a generated point is month `t + source_mth` of its S point.

## Counts and timings

`pols_if_init()` is the full-cover count in force at the valuation date: `policy_count` for
a point already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue
month, the month with `duration_mth(t) = 0`, and 0 in every other; every policy issued
starts on full cover. `pols_if_at(t, timing)` keeps `WOL_UK_S`'s three timings and adds
`basiclife/BasicTerm_SE`'s `BEF_NB`, each an int code named as `WOL_UK_S`'s text, in the
order of its instant within the month (*The compiled model*):

- `BEF_NB`, 0, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1`'s deaths and would-be lapses after it;
- `BEF_DECR`, 1, that count plus `pols_new_biz(t)`, before month `t`'s decrements, which
  `pols_if(t)` returns;
- `BEF_LAPSE`, 2, after the month's deaths, before its lapses;
- `AFT_DECR`, 3, the end of the month, after its deaths and lapses, which is `BEF_NB` at
  `t + 1` exactly, and 0 from the last month before the limiting age on.

Any other timing raises. The survivors carried into month `t` are those of month `t − 1`'s
`BEF_DECR` count, which `BEF_NB` forms itself, as its own value at `t − 1` plus that
month's new business, exactly the sum `BEF_DECR` returns. So within a policy year the
chain of calls from month `t` back is one cell a month, as `WOL_UK_S`'s own `pols_if`
recursion is; and in a year's first month after `t_entry()`, `BEF_NB` reads the year's
opening, `pols_if_py(y)`, which walks the year before in ascending order, a cell a month,
and returns its last month's survivors, the same float.

The paid-up strand runs beside it. `pols_pu(t)` opens at `pols_pu_init()` at `t_entry()`
and rolls forward on mortality alone, taking in each month's conversions; `pu_benefit(t)`,
the strand's summed cover, opens at `pols_pu_init() × pu_benefit_pp_init()` and takes in
each conversion at its own paid-up value, `benefit_pp(t, PAID_UP)`. Each is blocked by
policy year as the count is, its year opened by `pols_pu_py(y)` and `pu_benefit_py(y)`,
and so are the premiums paid, `prem_cum_pp(t)`, from `prem_cum_pp_init()`, opened by
`prem_cum_pp_py(y)`: the model's four chains, blocked so that a compiled run's chains fit
its stack (*What a compiled run needs*). The cover, the premium and the improvement are
closed forms on their clocks. On a model just read, a cold call in the frame's last month
runs one cell a month back to its policy year's first month, two cells a year before
that, back to `t_entry()`'s year, and at most 24 cells more, at the contract's longest
cover, issued at 18 now and 120 months on, the limiting age at the contract's largest,
121: 1,236 months, on a chain of 215 on the anchor, paid-up, RPI and underwritten
increasing shapes alike, where one cell a month ran a chain of 1,236. The count's head
runs 8 beyond its chain, the premiums paid 5, `net_cf` 11 or 12, the roll-forward's
residual 12 and the claims total 13; the paid-up cover 23, and the paid-up count and its
deaths' claims 24, the most, at the foot of the paid-up chain, where the first walked
month's conversions read the full-cover count, its rates, the premiums paid and the cover
cold. A test holds each head to its own measured overhead, not to `Term_UK_SEC`'s 16,
which the paid-up chains' walk passes, nor to 24 for every head, under which a count chain
of two cells a month within its year, 11 cells more in the frame's last month, would pass.

`pols_all(t) = pols_if(t) + pols_pu(t)` carries the maintenance expense, a paid-up policy
costing money to administer though it pays no premium, and the roll-forward, which closes
as

```
pols_all(t) − (pols_if_at(t + 1, BEF_NB) + pols_pu(t + 1))
    = pols_death(t) + pols_death_pu(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_all(t + 1)` adds `pols_new_biz(t + 1)` to the counts
on the left. Conversions move policies between the strands and out of neither: the
full-cover count loses its deaths, its terminating lapses and its conversions, and the
paid-up count loses its deaths and gains the conversions. `pols_maturity(t)`, the survivors
in the last month before the limiting age, policy month `limit_mth() − 1`, is the
truncation residual, which pays nothing; `check_truncation()` asserts it is negligible.
Both checks scale their tolerance with the policies on the books, `policy_count() +
pols_pu_init()`, on both strands.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < limit_mth()`, and outside it, before issue
and from the limiting age on, every count on both strands is zero, and so every cash flow.
No count evaluates a rate there, and no table is read at a policy year or an attained age
the policy does not have: `mort_rate`, `lapse_rate_base`, `lapse_rate`, the cover, the
premium, the premiums paid, the benefits, the payments made, the moratorium and the paid-up
eligibility are zero or false outside cover, before any table or rate is read.

## Departures from WOL_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, and
each recursion opens at `t_entry()` from the opening state. Where `WOL_UK_S`'s test would
have stayed correct on the valuation clock, it moved anyway, so that cover has one
definition. Thirteen cells are new with running in force — `policy_count`,
`duration_mth_init`, `duration_init`, `t_entry`, `is_active`, `limit_mth`, `pols_new_biz`
and the six accessors of the opening state — and eleven more with compiling — `point_id`,
`cell_code`, `escalation_code`, `mort_schedule`, `lapse_last_year`, the four years'
openings, `pols_if_py`, `pols_pu_py`, `pu_benefit_py` and `prem_cum_pp_py`, and the two
refusals, `prem_cum_pp_refusal` and `pu_benefit_refusal` (*The compiled model*) — and none
of `WOL_UK_S`'s 61 is gone. Two References are new, `issue_age_min` and `omega_age_max`,
besides the codes.

| Cells | `WOL_UK_S` | `WOL_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len`; `limit_mth`, new | `12 × (omega_age − entry_age)`, from issue | `limit_mth() − duration_mth_init()`, from the valuation date, `limit_mth()` reading `omega_age` as an `int`; raises at or past the limiting age, outside the contract's bounds, on premiums ceasing past the limiting age and on a Reference off its domain | The frame starts at the valuation date; a whole float, `120.0`, makes the frame 120 does; no accepted point runs the crossover's search past the contract's longest cover |
| `pols_if`, `pols_if_at`, `pols_if_init`; `pols_if_py`, new | `pols_if` a recursion of its own, one cell a month, from the column's 1.0 at `t = 0`, which the timings read | `pols_if` is `BEF_DECR`, the `BEF_NB` chain plus the month's new business, one cell a month within a policy year from `t_entry()`; in a year's first month after it, `BEF_NB` reads the year's opening, `pols_if_py(y)`, which walks the year before in ascending order and returns its last month's survivors; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month; one cell a month within a policy year and two a year before it (D5), so that the compiled chain fits its stack (*What a compiled run needs*), the same float as before in every month |
| `pols_pu`, `pu_benefit`; `pols_pu_py`, `pu_benefit_py`, `pu_benefit_refusal`, new | from 0 at `t = 0` | from `pols_pu_init()` and `pols_pu_init() × pu_benefit_pp_init()` at `t_entry()`, blocked by policy year as the count is; a paid-up cover past the floats refused through `pu_benefit_refusal(t)` | The paid-up strand in force is history |
| `cover_pp`, `premium_pp`; `duration_init`, new | `SA` and `P` times `(1 + step)^(t // 12)` | `cover_pp_init()` and `premium_pp_init()` times `(1 + step)` for each anniversary since the columns' year, an anniversary at the valuation date the first; a value past the floats refused in its month | The increases already given are history, and one at month 0 is the projection's, at today's References |
| `benefit_pp`, `pu_benefit`, `premiums`, `claims`, `expenses`, `commissions`, `net_cf` | unchecked | a value past the floats refused in its month, naming the point and what makes it | An expense of 1.7e308 inflated at 100% a year, each in its domain, made `WOL_UK_S`'s expenses infinite at `t = 48` with every check passing |
| `prem_cum_pp`; `prem_cum_pp_py`, `prem_cum_pp_refusal`, new | the schedule summed from `t = 0` | from `prem_cum_pp_init()` at `t_entry()`, blocked by policy year as the count is; past the floats refused through `prem_cum_pp_refusal(t)` | The premiums already paid are history |
| `premium_pp`, `lapse_rate`, `in_moratorium`, `payments_made`, `benefit_pp` | cessation, the moratorium, the suicide window and the payments made on `t` | each on `duration_mth(t)` | A contractual event falls on a policy month |
| `crossover_mth`; `crossover_mth_init`, new | a search over `t` to cessation, reading `prem_cum_pp(t)` and `cover_pp(t)` | `crossover_mth_init()` where it fell before the valuation date; else one loop forward from the valuation date on the contractual schedule, from the opening state; `proj_len()` asked first | A crossover already past is history; a policy month passed as `t` would be negative before the valuation date; and the frame's refusals hold here too |
| `mort_improve_factor` | `(1 − r)^(y − 1)`, from issue | `(1 − r)^(t // 12)`, from the valuation date | Improvement on a basis stated at the valuation date |
| `inflation_factor` | `1.03^(y − 1)`, from issue | `1.03^(t // 12)`, from the valuation date | Unit costs in valuation-date pounds |
| `expenses` | the acquisition expense on `pols_if(t)` at `t = 0` | on `pols_new_biz(t)` | A point in force bears none, one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `commissions` | in policy year 1, `t < 12` | in policy year 1 on the policy clock | A point valued in its first year pays the rest of that year's commission |
| `mort_rate`, `lapse_rate_base`, `lapse_rate`, `benefit_pp`, `claims`, `payments_made`, `pu_eligible`, the counts | the rates and benefits unguarded, the two strands zero outside `0 ≤ t < proj_len()`: no `WOL_UK_S` frame has a month outside cover | zero outside cover, before any table or rate is read; an age past the table refused by name; the lapse table's extent from `Data` | Before issue `WOL_UK_S` reads the mortality table at ages the policy never has, or raises `KeyError` below its first, and raises `KeyError` on the lapse table, which has no policy year 0 |
| `pols_maturity`, `AFT_DECR` | at `t = proj_len() − 1` | at `duration_mth(t) = limit_mth() − 1` | One definition of cover, on the policy clock |
| `check_pols_roll_fwd_resid` | `pols_all(t + 1)` | `pols_all(t + 1) − pols_new_biz(t + 1)` | The next month's new business is no part of month `t`'s movement |
| `check_pols_roll_fwd`, `check_truncation` | `1e-10` and `1e-9` times `max(pols_if_init(), 1)` | times `max(policy_count() + pols_pu_init(), 1)` | `pols_if_init` is 0 on new business here, and the paid-up strand rounds too |
| `result_cf` | `range(proj_len())`, from issue | `range(proj_len())`, from the valuation date | Row 0 is the valuation month |
| `result_pols` | `WOL_UK_S`'s ten columns | `pols_new_biz`, `pols_death_pu` and `pols_maturity` added; the rates 0 outside cover | The counts behind `result_cf()` on both strands, after `basiclife/BasicTerm_SE`'s `result_pols()` |

Of the cash flows, the change of clock moves the maintenance expense alone at the shipped
assumptions, and `net_cf` with it, improvement shipping at 0. Point 12 carries that expense
in valuation-date pounds, so its `expenses(t)` is `WOL_UK_S`'s `expenses(12 + t)` divided
by `1.03`. Its `pols_if`, `premiums`, the claims columns and `commissions` are `WOL_UK_S`'s
from month 12 on. Point 14 is `WOL_UK_S`'s point 4 thirteen months on in those columns too;
its maintenance expense is `1.03^(t // 12 − (t − 13) // 12)` above S's at each `t`, and its
acquisition expense £150 exactly.

**The caps, as `WOL_UK_S` has them since UKLIB-SEC-PLAN.md's M0.** `mort_rate` caps the
annual mortality rate at 1, written `min(q, 1.0)`, the product first and the bound second,
so that a NaN stays NaN where `min(1.0, q)` would read it as certain death; wherever `q` is
a number the two are the same float. The shipped tables reach 1 in the tail, so the cap
binds on `WOL_UK_S`'s own points: on the anchor cell from attained age 110, policy month
480, where the population rate times the loading of 1.2 passes 1; on the male smoker from
101, policy month 432; and on the underwritten cell from 114, policy month 888. The RPI
steps take their floor and caps the same way, `min(max(rpi, 0.0), cap)`. The lapse rate's
bound keeps `WOL_UK_S`'s order, `min(1.0, w)`: it is no cap on a mortality rate, and the
stress and the table that feed it are held to domains no NaN is in.

**Improvement and the limiting age.** Improvement lowers every mortality rate, and the cap
with it, and carries survivors to the limiting age, which `check_truncation()` measures. At
0.2% a year it holds on every committed point, the largest residual 4.1e-12 of a policy;
at 0.4% it gives way on three underwritten points, and at 1% the underwritten twins hold
7.1e-6 of a policy at age 120. The tests switch improvement on at 0.2%, and record where it
gives way.

**Domains `WOL_UK_S` leaves unchecked.** `WOL_UK_S` raises a Reference to a power, bounds
a rate or an increase with it, or reads it as a share, a loading, a factor or an amount, and
checks none. Off its domain it projects a negative rate, benefit or expense with every
check passing, as an accidental share of 2, a mortality loading of −1 or an expense of −50
would. And a NaN fails every comparison it meets: a NaN cover cap is lost through the
`min` it bounds, written with the bound second; a NaN stress is switched off by its
comparison with 0; a NaN suicide window closes; and a NaN limiting age refuses nothing and
sizes no frame. An RPI of +∞ reads as the 10% cap, and one of −∞ as no increase. Here
`proj_len()` refuses each Reference off its domain, naming the point, the Reference, the
domain and the value, on every point, as a model-wide assumption:

| Reference | Domain | Off it |
|---|---|---|
| `issue_age_min`, `omega_age` | a whole number below `2**53`; the first 0 or more, the second above the first and at most a year past the mortality table's last age | a NaN bound refuses nothing and an infinite one bounds nothing, where the compiled caches are sized from them; past the table the frame reads an age it lacks |
| `omega_age_max` | a whole number of years below `2**53`, and `omega_age` at most it, 121 as shipped, the shipped table's last age plus one | the compiled model's caches hold frames to this limiting age and no further, so a longer mortality table, which would admit a later `omega_age`, bounds no frame; past `2**53` its `long long` cannot hold it |
| `mort_loading_o50`, `mort_loading_uw` | a finite number, 0 or more | a negative rate, or certain death at an infinity, through the cap |
| `mort_improvement` | a finite number, 1 or less | the factor `(1 − r)^n` changes sign each year |
| `acc_share`, `suicide_share` | a number from 0 to 1 | the shares blend two benefits, and outside them make a negative one or one past the cover |
| `suicide_mths` | a whole number of months below `2**53`, 0 or more | the window compares a policy month with it, and a NaN closes it |
| `rpi_rate` | a finite number | an infinity reads as the cap or as no increase, through the floor at 0 and the cap |
| `esc_rpi_cover_cap`, `esc_rpi_prem_cap`, `esc_rpi_prem_mult` | a finite number, 0 or more | an increase is a cut; a NaN cap is lost through `min` |
| `esc_fixed_cover`, `esc_fixed_prem` | a finite number, 0 or more | the source defines increases only |
| `esc_take_up` | a number from 0 to 1 | the share of each increase taken up: below 0 an increase is a cut, and past 1 more than the contract gives |
| `lapse_crossover_beta` | a finite number, 0 or more | a negative stress lowers lapses past the crossover, and an infinity reads as a certain lapse through the rate's `min` |
| `inflation_rate` | a finite number, −1 or more | the inflation factor changes sign each year |
| `expense_acq_o50`, `expense_acq_uw`, `expense_maint_o50`, `expense_maint_uw`, `comm_init_rate` | a finite number, 0 or more | an expense is income |

Each domain is a comparison no NaN passes, a finite one bounded by the largest float, and
a whole number one of which `x == x // 1` holds below `2**53`, which an infinity fails, and
each Reference is printed as the compiled model types it, the four integers through
`int()` once whole and every other through `float()`. `Data.future_horizon_mth` is held to
a whole number of months, 0 or more, by `Data` itself, as it reads the table.

**Values past the floats, refused in their cell.** From an opening state and References
each in its domain, an increase can take the cover or the premium past the largest float,
a premium the premiums paid, a multiple or a share of the cover a benefit or the paid-up
cover, a count an amount, an inflation rate an expense, a commission rate a commission,
and the flows' sum the net cash flow, where `WOL_UK_S` would pay an infinite claim, charge
an infinite expense or compare an infinite total, every report infinite and its checks
NaN or passing. Here `cover_pp`, `premium_pp`, `prem_cum_pp`, `benefit_pp`, `pu_benefit`,
`premiums`, `claims`, `expenses`, `commissions` and `net_cf` each raise `ValueError` in
the month its value first leaves the floats, naming the point, the month and what makes
it.

A power is different. modelx runs a formula as Python does, and Python's float `**` raises
`OverflowError`, with the platform's own message, "Numerical result out of range" on
Linux, where its result would pass the largest float, before the cell can look at it. So
the cover's and the premium's step to the policy years since the valuation date, the
inflation and improvement factors and the crossover's search, each raised from a step in
its domain but large enough, `1e200`, are refused by Python's error, which names neither
the point nor the Reference, and a test holds that. The compiled model's `pow` returns an
infinity there instead, so these five powers take uslib's M22 form, Python's own float
power where the compiled one gives an infinity, so that both engines raise the same error
(*The compiled model*).

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and how its four chains reach back in time,
and no number: what its reports computed on each committed point was frozen before the
change, and they still compute it, to 1e-12 of each column's largest value (*Tests*,
below), and every value the in-force model cached was this one's, bit for bit, when the
change was made: 483,748 on the committed points, and 3,973,566 on the 187 points of the
full splice grid under the splice's References. Cell by cell, at every argument a full
modelx sweep evaluates, the compiled model computes what modelx computes, bit for bit, on
the committed points, on the points of the splice grid, which take the branches they do
not, at the contract's longest covers, where the cap on mortality, the RPI's floor and
caps and the lapse rate's bound bind, on every value a decoded column holds, on keys
written as floats, on the committed rows under the References they were read from, and on
the rows valued on an anniversary under References that move its increase. The compile
tests hold it so on x86-64, and to 1e-12 relative elsewhere, where no run has shown it
yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py whole_of_life                  # in place, beside the model
python build_sec_cy.py whole_of_life --out /tmp/wol   # elsewhere, with the CSVs
```

The tool exports the model to `WOL_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `WOL_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/whole_of_life")    # the directory holding the build
from WOL_UK_SEC_nomx_cy import mx_model as model
model.Projection[9].result_cf()                 # point 10, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about a minute with gcc, 67 to 69 s here, and needs modelx-cython, which
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
  0, as `BasicTerm_SC` is: `Projection[9]` is point 10, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `sum_assured()` is `float(data.sum_assured()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The six columns of opening state are
  vectors too.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the number it selects, for every point at once: the cell into its code, `cell_code`,
  `O50` 0 and `UW` 1, and the escalation into its code, `escalation_code`, `LEVEL` 0,
  `FIXED_5PCT` 1 and `RPI` 2, codes rather than what they select, because the loadings,
  the expenses, the benefit rules and the steps are `Projection`'s References and rules,
  which `Data` cannot read; the basis the cell takes, the sex and the smoker status into
  the row of the mortality table they select, `mort_schedule`, `4 × basis + 2 × sex +
  smoker`, population before assured, M before F and NS before S; and each variant's
  True or False, `variant_adb_2x` and `variant_paid_up`, into a 0/1 flag. Each decodes as
  `WOL_UK_S` reads the column, which a test holds on every value a column can hold, and
  what it cannot hold it refuses (below).
- **Tables indexed by integers.** The mortality table is `mort_table_array`, by schedule
  and attained age, padded from age 0 so that the index is the age; the lapse rates are
  `lapse_table_array`, by the cell's code and policy year, padded at year 0, beside each
  cell's last year, `Data.lapse_last_year`, an int64 vector of two, which `Projection`'s
  `lapse_last_year()` reads at the point's cell. The padding holds NaN, and nothing reads
  it: the one cell that reads each table checks its key first, `mort_rate` against the
  mortality table's ages either side, and `lapse_rate_base` holds the policy year at the
  cell's last above, as `WOL_UK_S`'s `tbl.index.max()` on the cell's rows does, and reads
  in cover alone, where the year is 1 or more.
- **Codes.** A timing or a kind, which `WOL_UK_S` spells as text, is an int Reference
  named as the text: `BEF_NB = 0`, `BEF_DECR = 1`, `BEF_LAPSE = 2` and `AFT_DECR = 3`, in
  the order of their instants within the month; `benefit_pp`'s kinds, `DEATH = 0`,
  `NON_ACC = 1`, `ACC = 2` and `PAID_UP = 3`; and `claims`' kinds, `DEATH = 0`,
  `DEATH_PU = 1` and `LAPSE = 2`, in `result_cf()`'s order, and `ALL = 3`. `WOL_UK_S`
  spells `DEATH` in both families, the benefit per death and the outgo it pays, so it is
  one Reference, 0 in both, as uslib's `ULSG_US_SEC` names `GRACE` a kind and a status:
  `benefit_pp`'s kinds put it first, before the two it blends on the over-50s cell, in
  `WOL_UK_S`'s order, where `WOL_UK_S`'s docstring lists it after them, so that each
  family fits one width of four and `claims`' keep their report's order. A call reads as
  before, less the quotes: `pols_if_at(t, BEF_DECR)`. A string argument would give the
  cell a dictionary for a cache, where a code indexes a C array, so codes are numbered
  from 0 without a gap, and every code inside the width is one its cell takes.
- **The claims total, a code of its own.** `WOL_UK_S` totals the three kinds as
  `claims(t)`, its `kind` defaulted to `None`, with Python's `sum` over a generator. A
  default compiles as a keyword parameter the typing guard refuses, `None` is no C
  integer and a generator is a Python object, so the total is `claims(t, ALL)`, which
  `net_cf` reads. It is written out, `0.0 + claims(t, DEATH) + claims(t, DEATH_PU) +
  claims(t, LAPSE)`, left to right, which is `sum`'s float wherever at most two kinds are
  non-zero: `sum` compensates since Python 3.12, and the error of a single addition,
  added back, rounds to the sum it came from. Here at most two are: the lapse kind is 0
  in every month by the product's design, and the deaths on full cover and the paid-up
  deaths are non-zero together on a paid-up strand in force beside full cover. A test
  counts the kinds non-zero together in every month of every committed point, never
  three, two in some, and holds the total to `WOL_UK_S`'s by its bits on every twin; a
  product with three non-zero kinds takes `CI_UK_SEC`'s compensated sum written out.
- **Four chains blocked by policy year.** The full-cover count carried in,
  `pols_if_at(t, BEF_NB)`, the paid-up count, `pols_pu`, the paid-up cover, `pu_benefit`,
  and the premiums paid, `prem_cum_pp`, each run one cell a month within a policy year,
  as at the in-force step, and in a year's first month after `t_entry()` read the year's
  opening, `pols_if_py(y)`, `pols_pu_py(y)`, `pu_benefit_py(y)` and `prem_cum_pp_py(y)`,
  as `ULB_UK_SEC`'s do. Each opening walks the year before in ascending order, asking the
  monthly cell of each of its months, so that each finds the month before cached, and
  returns the value carried out of the year's last month: the survivors of
  `pols_if_at(t − 1, BEF_NB) + pols_new_biz(t − 1)`, the product `BEF_NB` forms within a
  year, the paid-up survivors and conversions, the paid-up cover surviving and converted,
  and `prem_cum_pp(t − 1)`, each the month's own float, so no number moves. A cold read
  then runs one cell a month back to its year's first month and two cells a year before
  that, where one cell a month ran the whole cover on the C stack (*What a compiled run
  needs*, below).
- **No refusal formatted on a chain.** A compiled cell's C frame holds the code that
  formats each of its messages, whether a run reaches it or not, and a chain holds a frame
  of each cell it recurses through at each level: on CI's Ubuntu runner, a refusal
  formatted in `Term_UK_SEC`'s recursive waiver cell had its cold call need 512 KiB to 1
  MiB, and 256 to 384 KiB without it (UKLIB-SEC-PLAN.md K12). So `prem_cum_pp` and
  `pu_benefit`, two of the chains, format nothing: where the value has left the floats
  each calls `prem_cum_pp_refusal(t)` or `pu_benefit_refusal(t)`, which computes the
  value again from the same cells, the same float, and raises the chain's message, naming
  the month and what makes it. Each takes the month alone, since a float parameter would
  give it a dictionary for a cache, and returns the value where it is finite, which the
  sample asks for to type it. A test holds every cell that a cold call's deepest path
  holds more than once to building no text and raising only a constant. The count's
  timings refuse a code with a constant, and the cover's, the premium's, the benefits',
  the claims' and the flows' refusals stay in their cells: no chain recurses through
  them, each held once on a path, at its head or its foot, but the claims total's, which
  holds `claims` twice at the top of any path, the total over its full-cover kind.
- **The check's loop.** `WOL_UK_S`'s `check_pols_roll_fwd` is `all()` over a generator,
  which compiles to a Python closure inside the cell; here it is a loop over the frame
  that returns False at the first month outside the tolerance, a NaN among them: the same
  verdict at the same month, in C.
- **Five powers raise as modelx does.** Past the largest float, Python's float power
  raises `OverflowError` where C's `pow` gives an infinity. So the cover's and the
  premium's steps, expense inflation, mortality improvement and the crossover's search
  call Python's own power where theirs is infinite from a finite base, as
  `Term_UK_SEC`'s do (uslib's *Record — M22* form). Only inputs far outside the product
  reach it (*What it refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `cell()`,
  `escalation()`, `mort_basis()`, `sex()` and `smoker()`, and the two reports return a
  table row, text and DataFrames, for a reader, for `run_sec.py` and for the comparison
  with `WOL_UK_S`. No other cell calls them, so they cost the projection nothing. Each
  label refuses any value but its column's codes, as `WOL_UK_S`'s `cell` and `escalation`
  do, and as `sex` and `smoker` now do where `WOL_UK_S`'s return the column as read, and
  `mort_basis` reads `cell`, so each returns text or raises, and compiles to `str`.

The `Data` docstring lists its 24 vectors, arrays and extents, each with the column or
file it comes from. The six readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 77 of
its 85, returns a C `bint`, `long long` or `double`, and caches a single value, or a C
array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,358 by `t`, of `double`, `long long` or `bint` | the 36 cells of `t` alone: every count, rate, factor, premium, benefit and cash flow on both strands, the premiums paid and the paid-up cover with their refusals; the policy clock, its years, the attained age and the payments made; the roll-forward's residual; and the flags `is_active`, `in_moratorium` and `pu_eligible` |
| a C array of 1,358 by 4 | `pols_if_at(t, timing)`, `benefit_pp(t, kind)` and `claims(t, kind)` |
| a C array of 104 by policy year | `pols_if_py(y)`, `pols_pu_py(y)`, `pu_benefit_py(y)` and `prem_cum_pp_py(y)` |
| one `bint`, `long long` or `double` | the 34 other cells without a parameter: the point's numbers, codes and flags, its opening state, the ends of its frame, the steps, the loading and the expenses of its cell, the payments expected, the crossover, its cell's last lapse year, and the two checks |
| a Python object, or `str` | the eight reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the two reports
and the two checks on every committed point, and then the cells no report reaches:
`model_point()` and the five label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; `crossover_mth()`, which no projection cell reads; the two
refusal cells, which only the error paths of `prem_cum_pp` and `pu_benefit` call, where a
value has left the floats, and which return the value elsewhere, so that the sample's
call of each in every month types it; and the codes the reports leave: the count at
`AFT_DECR`, which no cell reads, and on the underwritten cell the moratorium's and the
accidental benefit's kinds, which only the over-50s blend reads. It calls every timing and
every kind, the claims total among them, in every month of the frame and the month after
it. Every code inside the one width is one its cell takes, so no call raises: a raise is
not traced. It runs the committed points alone: the export reads the CSVs of the
directory the build is made in, which in place is the product directory. The committed
points leave branches untaken: the crossover stress, a lapse rate at its bound, the cap
on mortality with improvement on, the RPI's floor and caps, an odd cessation, an issue age
of 80. That still types every cell, because every branch of a cell returns the one type
its others return, a count or an amount a float in every branch, and on points that take
those branches the compiled model computes modelx's numbers (above). The labels need no
trace beyond the committed points: each refuses what is not its codes, so each returns
text alone. The sample also raises the recursion limit, which modelx raises and its
export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,358 | 1,357. The longest frame is the longest cover, a policy issued at 18, `issue_age_min`, to the largest limiting age, 121, `omega_age_max`, issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × (121 − 18) + 120 = 1,356 months, `t = 0 … 1,355`, and the month after, 1,356, whose roll-forward residual reads the count carried into 1,357 |
| `t`, `timing`; `t`, `kind` | 1,358 by 4 | `t` as above, by the four timings, by `benefit_pp`'s four kinds, and by `claims`' three and the total. Every 2-D cache of a model shares one inner width, the widest: Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `y` | 104 | 103, the policy year of the longest cover's last month, 1,235 months from issue, whose first month reads its four openings |

**The limiting age the caches hold.** `omega_age` may be set to a year past the mortality
table's last age, 121 on the shipped table, as `WOL_UK_S` and the in-force step allow, and
the frame then runs a year longer than at the shipped 120. A longer table would let it run
longer still, so the contract has its own bound, `omega_age_max`, 121, the shipped table's
last age plus one: every limiting age the shipped table admits projects, in modelx as
compiled, and `proj_len()` refuses an `omega_age` above the bound, naming the point
(*What it refuses*), so that no table bounds the caches. `proj_len()` refuses an issue age
below `issue_age_min`, and `Data` a point issued more than `future_horizon_mth` months
ahead, so no report on a point the model projects runs past these caches. Those three
References are the contract the sizes are derived from; the ages bound none, since an age
indexes `Data`'s mortality table, not a cache. Raise `omega_age_max` or the horizon, or
lower `issue_age_min`, and a report runs past the caches in the compiled model alone: `t`
or `y` past its size raises `IndexError`, naming nothing, where modelx projects. Each
needs the sizes derived again, as `spec_sec.py` derives them, and a rebuild; a longer
horizon, `t` raised to 12 × (`omega_age_max` − `issue_age_min`) + the horizon + 2.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as the year walks' month counter, stays a Python object, though the
cell is typed `double`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of each
decrement here, is a complex power, which gcc computes with `cpow` rather than `pow`, and
whose last bits can differ from Python's; and gcc fuses a multiply and an add where the
target has the instruction, one rounding where Python rounds twice. The tool's docstring
has the detail, and uslib's
[`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the measurements
that put each there. With all four, every compiled value here agrees with modelx bit for
bit. The compile tests hold each directive in the module's first line, and a static test
holds the tool's line to the two and no other: `cdivision=True` would make `//` on C
integers truncate where Python floors, which `duration(t)` meets before issue, where the
policy clock is negative; and `boundscheck=False` or `wraparound=False` would change what
an `idx` outside the table reads.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 771,992
bytes, the type's basic size, which holds every cell's cache, and deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a test runs the compiled runner on a block of 136 points, the committed table copied,
and finds no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 16. What it needs
is stack. That call is a cold one in the last month of the longest cover, a policy issued
at 18, now or 120 months on, 1,236 months from issue at the contract's largest limiting
age, 121. One cell a month, as the in-force step left the four chains, compiled with gcc
and issued now it needed 292 KiB of C stack on the anchor, paid-up, RPI and underwritten
increasing shapes alike: a cold `net_cf`, the count, the roll-forward's residual and the
claims total ran on a thread of 292 KiB and not of 288, at about 240 bytes a month; the
paid-up count, the paid-up cover and the paid-up deaths' claims on 240 and not 236, and
the premiums paid on 212 and not 208, with no refusal formatted on a chain. The count's
chain was past the 256 KiB the C step allows itself here, and the paid-up chains and the
premiums paid within it; but CI's Ubuntu runner needed two to four times this machine's
stack for `Term_UK_SEC`'s cold call (UKLIB-SEC-PLAN.md K12; §6.1, *Record — M2*), which
puts even the premiums paid's 212 KiB at 424 KiB to 848 KiB there, and the paid-up
chains' 240 at 480 KiB to 960 KiB, at or near the 1 MiB thread, beside the count's 584
KiB to 1.1 MiB. So all four chains are blocked by policy year. Blocked, the call runs on a
chain of 215, one cell a month within its year and two cells a year before it, where one
cell a month ran 1,236, and 5 to 24 cells more in modelx, which a test holds head by head
(*Counts and timings*, above). Compiled, every head on every shape, each cold in an
ItemSpace of its own, issued now and 120 months on, with the crossover stress and
improvement on, ran on a thread of 64 KiB and not of 60, the premiums paid on 52 and not
48: a quarter of the 256 KiB. A test runs each shape at its longest cover in a thread of 1
MiB, the stack Windows gives a program's main thread unless the program is linked for
more, and again on the main thread, which is where `run_sec.py --cython` runs, and records
the smallest of its sizes each ran on. MSVC's frames may be larger than gcc's, and the
`cython_uk` CI job, which runs the test on Windows too, is the check on them. That test
cannot see the blocking undone: one cell a month, the deepest call needed 292 KiB here,
which a 1 MiB thread holds, so only the modelx depth test, which counts the chain cell by
cell, guards the blocking, here and on every runner. The export
recurses in Python instead: the same call needs a recursion limit of 492 there, the
paid-up deaths' claims at 121, and the reports and checks, which run in ascending `t`, need
128, so `sample_sec.py` sets 2,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message: each
malformed row of the table, each assumption table a reader cannot read, each point the
frame refuses, each Reference off its domain that the compiled model can hold, each value
past the floats, by its cell and by a report, a point past the limiting age, a key read
beyond the mortality table, an `omega_age` past a shortened one, and what the vectors
cannot hold, in a cell typed `long long` or `double` as in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, and an
age or a count of months as an int; and it names a timing or a kind by its code,
`benefit_pp(12, 2)` for the accidental benefit, in both engines. So a rate written as an
int, 2, gives one message in both engines. An int Reference, `issue_age_min`,
`omega_age`, `omega_age_max` or `suicide_mths`, and `Data`'s `future_horizon_mth`, is a C
`long long` compiled, and a float set on it is truncated as it is set, 18.5 to 18, or a
horizon of 12.5 to 12, where modelx refuses 18.5 and 12.5 as not whole numbers, and a NaN
or an infinity cannot be set on it at all; so set each as a whole number. The compiled
refusal test sets `Data`'s References as it sets `Projection`'s: the horizon is refused at
−1 and at `2**53` as in modelx, and at 12.5 does what 12 does.

- What `Data` cannot decode or hold, when the vector is first read, naming every point or
  line at fault: a `point_id` that is not a whole number, or is `2**53` or more in size;
  an issue age `2**53` or more in size, which an int64 vector cannot hold whole and numpy
  would cast without a word; a mortality age or a lapse policy year as large, before its
  table is cast; and, as since the in-force step, a code that names no cell, escalation,
  sex or smoker status and a flag that is not True or False. A key written as a float, an
  age `70.0`, is read by its value, as `WOL_UK_S`'s lookups match it. The tables' checks
  find a gap from the keys a table holds, so that a key far from the rest, `2**53 − 1`, is
  refused as a gap at once.
- A key beyond the mortality table, by the one cell that reads it, where `WOL_UK_S`'s
  lookup raised `KeyError`: `point_id 5: mort_table.csv has no rate at attained age 18`,
  from `mort_rate`, on a table that starts at 20. No frame reads past the table's last
  age, which `proj_len()` holds `omega_age` to: on a table cut at 100 it refuses the
  shipped 120, naming the point.
- An `omega_age` above `omega_age_max`, by `proj_len()`, which only a mortality table
  longer than the shipped one, or the bound lowered, can bring about: `point_id 1:
  omega_age, 121, is above omega_age_max, 120`, under a bound lowered to 120. Raised past
  121, the bound lets a longer table's frames run past the caches, in the compiled model
  alone (*The sample and the spec*).
- Premiums ceasing past the limiting age, by `proj_len()`: `point_id 1: cessation_months
  601 is past the limiting age, policy month 600, omega_age 120`, and a cessation of
  `2**53 − 1`, which `Data` reads, so that the crossover's search never runs past the
  contract's longest cover, in either engine.
- A value past the floats, in the cell where it first is, naming the point, the month
  and what makes it: the cover, the premium, the premiums paid, a benefit, the paid-up
  cover, the premiums, the claims, the expenses, the commission and the net cash flow
  (*Departures from WOL_UK_S*), the premiums paid and the paid-up cover through their
  refusal cells, with the chain's own message, each in its opening month, in a month
  within a policy year and on an anniversary. Each refusal cell repeats its chain's
  formula, branch by branch, and a test holds it to its chain, bit for bit, in every
  month of every committed point, since C4 compares two engines that would share a drift.
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: the cover's and the premium's steps,
  expense inflation, mortality improvement and the crossover's search each call Python's
  own power where theirs is infinite from a finite base, so that the compiled model raises
  the platform's message as modelx does (uslib's *Record — M22* form), rather than carry
  an infinity on. Only an input far outside the product reaches one within the longest
  frame: a step of the order of a thousand a year, an inflation above about 533 a year or
  an improvement below about −533; a test reaches each with a base of about 1e200, at
  `t = 24`, the month before computing in both, and the search's four guards, the
  premium's and the cover's step from issue and in force, on the underwritten increasing
  point, issued now and in force 12 months. Compiled without its guard, the search
  returned −1 or 24 where modelx raises.
- A timing or a kind no cell takes, by the cell, as `WOL_UK_S`'s are: `invalid timing`
  and `invalid kind`. Each 2-D cache is 4 wide, and every code inside it is one its cell
  takes.

An argument outside a cache raises `IndexError` in the compiled model alone:
`net_cf(1358)` or `net_cf(-1)`, which modelx answers with 0, the month being outside
cover; `pols_if_at(t, 4)`, `benefit_pp(t, 4)` and `claims(t, 4)`, which modelx refuses as
a timing and a kind it does not take; and a year's opening at policy year 104, past the
`y` cache, which modelx computes as it computes any year's opening, the value the year
before closes on: 0 on the test's point, issued at 70, that year long past its cover. No
frame asks for it: a frame's last month is in policy year 103 at most. An `idx` past the
last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's last
point, under that point's own `point_id()`; the compiled refusal test holds both against
modelx.

An annual mortality above 1 is not refused but capped, in both, and so is a lapse rate,
and the RPI's steps are floored and capped: `mort_rate` caps the product at 1, as
`WOL_UK_S` does, and a compile test holds the two engines equal where each cap and bound
binds, new business and in force. A NaN product would stay NaN through the cap, in both,
which the compiled model computes as a comparison that keeps the value unless the bound
is smaller.

### Speed

`python tools/bench_sec_cy.py whole_of_life` builds the model into a temporary directory
and times one block run on three engines: modelx, the export and the compiled model. Each
engine runs the committed table repeated, in a process of its own, as `run_sec.py
--block` runs a block, each point projected and then released. `net_cf` is `net_cf(t)`
summed over the frame, the projection alone, as `basiclife/BasicTerm_SC` is timed on its
`pv_net_cf()`; `result_cf` is the report `run_sec.py` prints, which builds a DataFrame for
each point. Each run of the tool takes the fastest of three runs of each engine and loop.
The tool was run three times, and each time below is the median of its three, with the
range of the three beside it:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,001 | 0.396 ms (0.390–0.411) | 0.993 ms (0.972–1.020) | 86 MB |
| export | 612 | 5.10 ms (5.07–5.28) | 5.85 ms (5.80–5.85) | 86 MB |
| modelx | 136 | 187 ms (183–189) | 202 ms (200–212) | 125–131 MB |

On `net_cf` the compiled model runs 13.0 times its export (12.4 to 13.3 over the three),
and on `result_cf`, where building the DataFrame takes most of its time, 5.9 times (5.7
to 6.0); it runs 470 times modelx on `net_cf` (454 to 477) and 207 on `result_cf` (201 to
207). The ranges are the noise of a machine other builds were using, its 1-minute load
between 2.0 and 2.6 as the runs started: about −2% to +1% on modelx's `net_cf`, −1% to
+5% on its report and −2% to +4% on the compiled `net_cf`. `ULB_UK_SEC`, timed the same
way on its own points on the same day, ran 13.1 and 5.5 times its export. A point here
costs more on every engine than one of `ULB_UK_SEC`'s, its frame being longer: 617 months
on average over the committed points, against the bond's 340, and about the same a month.
The release keeps a block flat: the compiled model's peak and the export's grew by less
than 0.1 MB over their 6,001 and 612 points in every run, where modelx's rose by 39 to 45
MB in its loop. Reading the three files and building every `Data` vector and array for
the compiled block took 0.034 to 0.052 s, and asking every point for its frame, the
runner's first pass, 0.09 to 0.17 s. Every engine, loop and run summed `net_cf` over a
copy of the table to the same −79,123.3363, to 1e-9 relative.

Measured on 2026-11-23 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.30 GHz), a 1-minute load average between 2.02 and 2.64 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1 to 7, every
  cell of `WOL_UK_S`'s agrees at every argument `WOL_UK_S` evaluates in its own sweep, to
  1e-9 relative with no absolute floor, but for `pols_if_init` and `model_point`, and
  `result_pols`, which the spec names with its reason; a cell this model lacked would fail
  it. The kinds and timings are compared as the codes of the same names, and
  `WOL_UK_S`'s claims total, `claims(t)`, with `claims(t, ALL)`. So `WOL_UK_S`'s worked
  example, which `tests/test_whole_of_life_uk.py` asserts to the penny and the in-force to
  five decimals, holds here with no number restated. The same suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present. And
  `tests/test_whole_of_life_uk_sec.py` compares each twin with S in every cell again, with
  improvement at 0.2%, the RPI at 6%, the take-up at 0.8 and the crossover stress on in
  both models, which T1, at the shipped References, and the splice, at no improvement,
  cannot: a cell that dropped improvement fails there alone.
- **The splice**, in `tests/test_whole_of_life_uk_sec.py`: each `WOL_UK_S` point restated
  in force at months about its events — on the over-50s points 1, 6, 11 to 13 (the
  moratorium's end and the first anniversary), 60 (the lapse table's last year), 118 to 121
  (the first conversion to paid-up), 165 to 167 (the crossover), 239 to 241 (premium
  cessation), 479 to 481 (the cap) and 599, with 185 and 186 on the RPI point; on the
  underwritten points 11 to 13 (the suicide window's end), 642 and 643, 887 to 889 and 959;
  on the male smoker 222 and 223, 299 to 301, 431 to 433 and 659 — continues the S
  projection in every cell the two share but `proj_len`, and in both reports, to 1e-9
  relative with no absolute floor, the residual at 1e-9. The crossover stress, which ships
  at 0, is on in both models at 0.5, so that past the crossover the premiums paid move the
  lapses, the conversions and so every count; inflation and improvement, the inputs on the
  valuation clock, are 0 in both. A stress of 100, which takes the lapse rate to its bound
  and leaves the paid-up point paid-up entirely, is spliced on the anchor and paid-up points
  the same way. Six variants of S's points, in a copy of S's table that is never committed,
  reach what S's own cannot: the RPI point with the pro-rata paid-up value, the double
  accidental benefit with it, the anchor cell issued at 80 with its premiums ceasing at 90
  and no crossover, the underwritten increasing point as a female smoker, the paid-up
  point with an odd cessation, 239 months, its strand in force from 120, and the anchor
  cell with a cash sum of £7,180, which its 240th and last premium passes, so that its
  crossover falls in its last premium month, 239, the crossover's search's last, from
  issue and from the valuation date. A core of 25 of the 152 splice cases and 6 of the 27
  future ones runs by default, the RPI point after its premiums ceased and the crossover
  in the last premium month among them, and the full grid with `UKLIB_SEC_FULL=1`; a test
  asserts the core reaches every branch, opening-state column, kind of valuation month and
  side of every `min` and `max` the full grid reaches. The slower tests over every
  committed point, every shape or every cap run a part of it by default, six points among
  which every flow is nonzero, and the rest with the full grid.
- **Future new business**: issued 1, 12 and 120 months after the valuation date, each S
  point is the S projection moved on, with zeros before issue and no table read there, and
  so is each variant issued 13 months on, more than a year after the valuation date and
  off its anniversaries.
- **How it computes**: on every row of the splice's grid, after its reports, its checks
  and every monthly cell at every month, no cell has been called at a negative month, none
  on the books read a month before `t_entry()`, none read a month later than `t + 1`, and
  none raised. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, the policy clock being a closed form, and every point's reports and
  checks run under modelx's recursion limit lowered to 40, which a recursion backward over
  the frame would exceed; they pass at 12. Each chain, called cold in the last month at
  the contract's longest cover on four shapes, issued at 18 now and 120 months on at the
  limiting age of 121, runs one cell a month back to its policy year's first month, two
  cells a year back to `t_entry()`'s, and no more beyond them than its head's own measured
  overhead, from 5 cells to 24; each year's opening, of the full-cover count, the paid-up
  count, the paid-up cover and the premiums paid, is the value the month before carries
  out, bit for bit, and the one cell of its chain that a year's first month reads; and no
  cell that a cold call's deepest path holds more than once, on the paid-up shape at the
  limiting age of 121, builds text anywhere in its formula, at a raise, in an error branch
  or into a local, or raises other than one exception on one string constant.
- **Counts**: the roll-forward closes on both strands; `result_pols()` is S's report with
  `pols_new_biz`, the paid-up deaths and the truncation residual beside it; multiplying
  `policy_count` and `pols_pu_init` by 2.5 together, with the stress and improvement on,
  multiplies every flow and counted cell, each nonzero on some point, and moves no
  per-policy value, bit for bit; a point restated a month on, opened with what the model
  carries into its month 1, continues its own flows, its commission among them, which is
  what sees a paid-up flow weighted by the full-cover count; the roll-forward, its
  tolerance scaled by the policies on both strands, closes on ten million policies, the
  point paid-up entirely among them; and so does the truncation check, on that point with
  ten million paid-up policies at a loading under which survivors reach the limiting age.
- **Validation and regeneration**: each malformed row of the table, 95 cases, each `2**53`
  bound of the entry age, the cessation and the crossover at the bound among them, and the
  crossover at `2**53 − 1`, is refused naming its point, and naming its label on an extract
  labelled otherwise than by position,
  among them each bound of the premiums paid, the paid-up cover and the crossover a cent or
  a month outside, the first year's history a month after issue, and a paid-up strand at
  half an odd cessation rounded down; the horizon is a Reference, whole and below `2**53`;
  a point past the limiting age is refused by `proj_len()`, and `run_sec.py --block`
  refuses it before printing anything; so is a point outside the contract's bounds, 8
  cases, an issue age of `2**53 − 1` among them, each bound just inside it and each moved
  past a committed point, and premiums ceasing a month past the limiting age, at `2**53 −
  1` months and past a limiting age lowered to 89, where at the limiting age itself they
  read; each of 23 References off its domain, the value next outside
  each edge, NaN and both infinities, 162 cases, where each edge is accepted, an `omega_age`
  of 121 accepted, as at stage E, and refused under an `omega_age_max` lowered to 120, and
  a whole limiting age written `120.0` projects as 120 does, cell for cell; a value past
  the floats, 14 cases, from the cover to the net cash flow, each in its own cell, the
  premiums paid and the paid-up cover each in its opening month, within a policy year and
  on an anniversary, the three branches their refusal cells repeat; and each of the five
  powers raising `OverflowError`, 9 cases, each of the crossover search's four guards,
  the premium's and the cover's step from issue and in force, among them; each assumption table a reader cannot read, 28 cases, a key of `2**53`
  and of `2**53 − 1` among them, refused naming its lines, and an age past the mortality table refused by name; keys written as floats read
  as `WOL_UK_S` reads them; the edges of the interface are accepted, a point paid-up
  entirely, a zero count, the horizon, the first month a paid-up policy can be in force,
  an escalated point at its issue values, a point after cessation, each bound of the
  contract and each bound of the history at its edge among them; every state `WOL_UK_S`
  reaches, as shipped, under the splice's stress, under a stress that lapses every policy,
  under an RPI of 8% and under a take-up of a half, is accepted in force; and the
  committed table is what `WOL_UK_S` generates.
- **The product's own facts**: the two clocks on the shipped points; the committed rows, in
  force and issued later, continuing their S points at the shipped assumptions but for
  inflation, and the rows read under References of their own holding `WOL_UK_S`'s history
  under them, its counts throughout, and with those References set in both, `WOL_UK_S`
  throughout; each history column read, not recomputed, the cover and the premium on an
  RPI history no flat rate gives and on the fixed increases at a take-up of their day, the
  premiums paid, which move the stressed lapses and the crossover, and which the
  moratorium refunds as read, to the cent, the paid-up count and cover, and the crossover,
  on the RPI point restated after crossings under an RPI of 0 and of 8%; and the instant
  the columns are measured at, before month 0's events, so that point 12, valued on its
  first anniversary, makes its first increase at `t = 0` at a take-up of a half set at the
  valuation date, a cover of 153,750 and a premium of 106.31, where columns read after
  that step would hold 157,500 and 111.38 (UKLIB-SEC-PLAN.md K14); expense inflation and mortality improvement on the
  valuation clock, which only these tests see, and where improvement gives way to the
  truncation check; the crossover a policy month, `WOL_UK_S`'s on every row it reaches; the
  moratorium, the suicide window and commission on the policy clock; the acquisition
  expense on new business alone; the RPI's floor and caps; every guarded cell's value
  outside cover; the block; an extract without the generator's columns, labelled
  otherwise, projecting the same numbers; `run_sec.py`'s numbers, for a point and for the
  block, and its sum, and its `--cython` stopping where no repository is above it; no
  cell's parameter defaulted, `WOL_UK_S`'s `claims` total settled as a code of its own;
  the docstrings, read through
  docutils as the docs build reads them where docutils is installed; and the shared input
  tables.
- **The caps**: on the anchor cell, the male smoker and the underwritten point, under the
  splice's References, `WOL_UK_S`'s mortality rate reaches the float 1.0 in its first
  capped month and stays there, as does the monthly rate; every policy in force at its start
  dies in it, and none is in force after it; the reports hold finite floats; and every cell
  the two models share agrees, issued now and 12 months on, and restated in force the month
  before the cap, to 1e-9 relative with no absolute floor. A row restated five months into
  the capped year does the same from its first month. And a NaN sent to the cap, through
  either loading or improvement, or to the RPI's floor and caps, stays NaN in the cell,
  where the frame refuses the Reference; and each check is False where its residual's
  formula is replaced by one that is NaN in a single month, the only way left to give it
  one: the roll-forward's in the frame's first month and in its last, and the truncation
  residual in the last, so that a check's loop a month short or a month late fails.
- **The C step's representation**, in modelx, in seconds: `claims(t, ALL)` is the sum of
  its three kinds by its bits in every month of every committed point, never more than two
  of them non-zero, two in some, and `WOL_UK_S`'s total by its bits on every twin; every
  value each text column can hold decodes as `WOL_UK_S` reads it, each cell, each
  escalation on each cell, each of the eight mortality schedules and each variant's flag
  each way, an entry age with a fraction above .5 so that a decode that rounded would part,
  each point's row of the mortality table holding S's rates at every age and its cell's row
  of the lapse table S's at every policy year; each refusal cell is its chain's value by
  its bits, in every month of every committed point; each padded array holds NaN where no
  file does and nothing else, a cell's rows cut short read at their own last year, a
  cell's rows run longer than the other's widen the lapse array, the other's row NaN past
  its own last year, and the mortality table's one reader refuses an age below it, on an
  extract labelled otherwise than by position; each `Data` vector is the int64 or float64 the `Data` docstring's table
  states, and each parameterless cell returns a Python number; each label refuses a value
  that is not its codes; `spec_sec.py`'s sizes and `sample_sec.py`'s recursion limit are
  what their comments derive, the codes dense from 0 in each family, `DEATH` one code in
  two; `run_sec.py --cython` rebuilds exactly when a source is newer; and a label the
  vectors cannot hold, or a timing, a benefit or a kind no cell takes, is refused.
- **C2, the fingerprint**: on every committed point, each column of `result_cf` and
  `result_pols`, its sum over the frame, its largest absolute value and its values in five
  months, the first, the last and the three quartiles between, is what the model computed
  when its E step ended, to 1e-12 of the column's largest value, frozen at the end of the
  module by `tools/gen_sec_fingerprint.py` before the C step changed anything, and refrozen
  once, alone, when the in-force step's review moved the cover and premium columns before
  month 0's events, which moved points 15 and 16, valued on an anniversary.
- **Compiled**, the tests marked `cython`, which compile the model once a session into a
  temporary directory and run it in child processes: in
  `tests/test_compiled_conventions_uk.py`, C3, the typing guard, on the declarations, the
  spec and the generated C; C4 on the committed points; and the release. In this model's
  module, C4, each comparison calling every timing, benefit and kind in every month, which
  no swept cell reads otherwise, the count at `AFT_DECR` and the underwritten cell's
  accidental and non-accidental benefits among them: on the splice grid; at the contract's
  longest covers, six shapes issued at 18
  to the limiting age of 121, now, 120 months on and in force in their last month, the
  longest 1,356 months; where the cap on mortality, the RPI's floor and caps and the lapse
  rate's bound bind; on every value a decoded column holds; on keys written as floats; on
  the committed table under each of the three sets of References its rows were read from;
  and on the rows valued on an anniversary under an RPI of 8% and a take-up of a half,
  each stepping its cover and premium at `t = 0`. Each comparison under References other
  than the shipped ones reads by default some of the committed rows, and the whole table
  and every capped point with the full grid, as the `cython_uk` job's Linux legs run
  them: a compile test is never skipped, a skip failing that job. Under an RPI, the four
  RPI rows, every row an RPI moves, and under a take-up the seven escalating rows, every
  row it moves; under the stress of 100, which moves 15 of the 17, four, the paid-up rows,
  where a stressed lapse converts, and the RPI row past its crossover, where one
  terminates; under the anniversary's References, which move the seven escalating rows,
  the three valued on an anniversary, the other four being compared under an RPI and a
  take-up of their own; and at the mortality cap the male smoker's rows, restated about
  its cap, which no core row is. So the default leaves out combinations, rows whose every
  branch another default comparison reaches, on the Windows legs alone. A test derives each
  selection from the committed points in modelx, and holds `_wol_c4_also` to asking every
  code inside the one width in every month. Then the five labels' text; the refusals,
  message for message, each value past the floats, a kind named by its code, the overflows
  of the five powers, each of the crossover search's four guards among them, the future
  horizon at −1, 12.5 and `2**53`, set in the child as every space's References are, the
  `IndexError`s past the caches and an `idx` past the table and of −1 among them; each shape's deepest cold calls, `net_cf`, the roll-forward's residual
  and the paid-up deaths' claims, each in an ItemSpace of its own, on a 1 MiB thread and on
  the main thread; a Reference set late, which clears no cache; and `run_sec.py
  --cython`, which prints what modelx prints, for a point in force, a point paid-up
  entirely and the block.

**Time and memory** (UKLIB-SEC-PLAN.md U6). The module's default run takes 466 s here at a
peak of 3.4 GB of memory, and without its compile tests, `-m "not cython"`, 197 s at a
peak of 2.0 GB, on the shared 4-CPU machine at a 1-minute load of 2 to 3 (measured at the
C step's review). Without them it is inside the five minutes U6 budgets, as at the
in-force step, which recorded 207 s and 2.0 GB; with them it is past it. At the C step it
took 543 s to 587 s: the eight C4 comparisons of the whole committed table under
References other than the shipped ones, about 100 s of it, now compare by default the rows
each set is for, every row an RPI or a take-up moves and some of those the stress and the
anniversary's References move, and the whole table with the full grid, which the
`cython_uk` job's Linux legs run. What is left is the build, about 70 s, and about 200 s of
comparison: the splice grid's core, the contract's extremes, every decoded value, keys
written as floats, the caps' rows, the labels, the refusals and the stack. A compile test
is never skipped, since a skip fails that job, so a cut to the five minutes would take
most of these out of the default run, which `pytest` runs wherever modelx-cython and a
compiler are installed, and which the job's Windows legs run: the refusals, the extremes
and the decoded values would no longer run compiled with MSVC anywhere. The peak is the
module's swept models, the committed points, S's and the splice's, held for the module,
beside each comparison's values in both engines, inside the 7 GB of the smallest CI
runner.

```bash
python -m pytest tests/test_whole_of_life_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_whole_of_life_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k WOL_UK_SEC
UKLIB_CYTHON_SHARD=whole_of_life python -m pytest -m cython tests -q     # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R7]: #uklib-whole_of_life-r7
[REG-R22]: #uklib-reg-r22
[std]: #uklib-std
<!-- END generated citation links -->
