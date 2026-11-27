# In-Force Implementation Notes

**Status:** Draft, 2026-11-23. `PA_UK_SEC` is [`PA_UK_S`](model.md) taught to project
from a valuation date. Besides annuities starting at that date, it takes annuities already
in payment there, in any month of their policy year, and annuities to start in the ten
years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. It
stands on the payout chassis of uslib's `SPIA_US_SEC`. The product is the one
[`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model (UKLIB-SEC-PLAN.md U2).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `PA_UK_S` on another time axis, and it reads `PA_UK_S`'s mortality table in place, every
> assumption unchanged: the contractual mechanics are sourced, and every rate is a
> **[std]** standardization, the mortality basis an ONS-shaped population proxy standing in
> for the annuitant tables, which are restricted to CMI Authorised Users [R10] [R11]
> [REG-R22] [REG-R27]. Replace them with company data and licensed tables before drawing
> any conclusion from the numbers.

## Run it

```bash
python products/pension_annuity/run_sec.py            # point 1: the worked example, starting at t = 0
python products/pension_annuity/run_sec.py 11         # point 11: the worked example in payment 17 months
python products/pension_annuity/run_sec.py --block    # every model point, summed row by row
python products/pension_annuity/run_sec.py 11 --cython # point 11 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the library's own `build_sec_cy.py` the first time, in about a minute and a
half, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer
than the build, and says so on stderr. Nothing the build leaves there is committed, and
`.gitignore` covers it.

The first prints the worked example's first twelve rows of cash flows, with the counts and
survival behind them. Three lines to the same thing for point 11:

```python
import modelx as mx
model = mx.read_model("products/pension_annuity/PA_UK_SEC")
model.Projection[10].result_cf()     # point 11, the table's eleventh row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `PA_UK_S`'s takes a `point_id`: `Projection[10]` is point 11, and its
`point_id()` says so. `result_cf()` has `PA_UK_S`'s columns — `pols_if`, `annuity_payments`,
`claims_vp`, `claims_prop`, `expenses`, `liability_cf` and `net_cf` — with one row per
month from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out the
counts first, `pols_if`, the closing obligation measure, and `pols_new_biz`, the annuities
starting in the month, then `PA_UK_S`'s other columns in its order: each life's survival,
the guarantee's floor, the two payment factors, the instalment, the payments to date and
the value-protection balance.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[10]`, is
not enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector
frees, so the runner collects after each release. It freezes everything alive
(`gc.freeze()`) once the model and its table are read, and again once it has asked every
point for its frame, so that each collection scans only what the block has made since. It
keeps the block's sum as it goes, compensated as pandas sums a `groupby`, so that the block
is, bit for bit, the frames concatenated and summed by `t`. Every column is summed: each is
a flow of the month or `pols_if`, the contracts with an obligation open at its end. The
runner is uslib Term's, and `--build DIR` runs a build made elsewhere (*The compiled
model*). The tool goes with the library, into lifelib and into a `lifelib.create()` copy,
so `--cython` builds there as here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however long the annuity has been in payment, and
  the frame runs `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from
  the valuation date to the stop rule.
- **`duration_mth(t)`, the policy clock**, counts the months from the annuity start date
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the year the income escalates by, `age(t, life) =
  age_at_entry(life) + duration(t)`, age last birthday, the mortality table's, and the
  calendar year, `start_year() + duration(t)`, which dates the improvement. The stop rule
  is a policy month, `stop_mth()`: `PA_UK_S`'s frame length, the age stop on the youngest
  covered life or the guarantee's end if later. `BasicTerm_SE` reaches the same clock by
  adding one a month, a recursion as long as the frame; the closed form needs no such chain
  of calls.

Point 11 is the worked example in payment 17 months. At `t = 0` it is in policy year 2 at
attained age 66, its annuitant dead since policy month 16 on the scenario basis and its
dependant paid half the income, £695.25 in month 0; its frame has 619 rows, `t = 0 … 618`,
and `PA_UK_S` projects the same months as its rows 17 to 635. Point 20 is the RPI catch-up
point to start 13 months after the valuation date: `duration_mth(0) = −13`, it is on the
books from `t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 649 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the payment months and the months since a payment; the policy year and its escalation, the RPI's anniversaries among them; the guarantee's end; the scenario's months of death; the attained age, the mortality table and the limiting age; the calendar year the improvement counts from; the annuitant's payments to date, which first-death value protection nets | survival and the expected payments to date on every stream, from the opening state; the value-protection balance; expense inflation, `inflation_factor(t) = 1.03^(t // 12)` |

Expense inflation alone of `PA_UK_S`'s inputs runs on `t`, stepping on each anniversary of
the valuation date, so the maintenance charge is in valuation-date pounds, for every point
alike (USLIB-SEC-PLAN.md D7). Improvement is dated by the calendar and stays on the policy
clock: a contract in payment reads the calendar years it reaches, whatever the valuation
date. `rpi_rate` is one flat rate, the assumed RPI from the valuation date on, the same on
either clock, so no index path is introduced (UKLIB-SEC-PLAN.md §9 item 4); the increases
given before the valuation date are opening state (*The RPI and the income's history*).

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
points = range(len(model.Data.model_point_table()))
frames = [model.Projection[i].result_cf() for i in points]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point starting at `t = 0` the two clocks coincide, and the model computes what
`PA_UK_S` computes: every cell the two models share agrees, but `pols_if_init()`, now the
count already in payment at the valuation date, 0 for new business, and `model_point()`,
a row of another table. `annual_income_init()` agrees too: it is now the income of the
year under way at the valuation date, which on such a point is the first year's, the
value `PA_UK_S`'s cell of that name returns, and which this model also gives as
`annual_income_first()`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `PA_UK_S`'s columns, its
count restated as the in-force interface under `basiclife/BasicTerm_SE`'s names, and six
columns of opening state. Each state column is per contract, so that `policy_count` is the
one weight on every flow, and each is measured at the valuation instant, the start of month
0, before any month-0 event (USLIB-SEC-PLAN.md D6). Each is history: what the contract has
survived, paid and been given since its start, never re-derived from a Reference, which is
an assumption from the valuation date on, so that a Reference changed there reaches back
over no month already run (UKLIB-SEC-PLAN.md K14, §9 item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in payment, the start of month 0; for any other, its start month | the contracts in payment at the valuation date, for a point already in payment; the annuities starting, for one starting at or after it |
| `duration_mth` | whole months | the valuation date | the months from the annuity start date: positive in payment, 0 for an annuity starting at the valuation date, `−k` for one to start `k` months later, with `k` at most 120 as shipped |
| `lives_if_init_1`, `lives_if_init_2` | probabilities | the start of month 0, before any month-0 death | each covered life's probability of being alive, the annuitant's and the dependant's: 1 or 0 on a record, `PA_UK_S`'s `lives_if(d, life)` on a restated point; the dependant's 0 on a single life |
| `cum_annuity_all_init` | pounds per contract, 0 or more | the start of month 0 | the instalments paid on every stream before the valuation date, the annuitant's, the guaranteed and the dependant's: what was paid on a record, the expectation on a restated point; last-survivor value protection nets it |
| `annual_income_init` | pounds a year, `annual_income` or more, to half a cent | the start of month 0, before any month-0 anniversary | read on RPI-linked escalation, `lpi5` and `rpi_catchup`: the annuitant's income of the policy year under way, before the dependant's percentage, the scale the dependant is paid `δ` times of after the annuitant's death; the increases the RPI has given since the start, never below the first year's; on a point valued on an anniversary the year the anniversary closes, month 0 escalating it at the valuation date's RPI |
| `rpi_peak_init` | a factor, 1 or more | the anniversary that opened the policy year under way | read on `rpi_catchup`: the ratchet's running peak of the reference index over the latest index, above 1 while the index stands below a past peak |
| `cum_annuity_pp_init` | pounds per contract, 0 or more | the start of month 0 | read on RPI-linked escalation with value protection on the first death: the annuitant's as-if-alive instalments before the valuation date, which the first-death balance nets |

The last three are blank on a point that does not read them. Every state column holds its
value at the start date on a point not yet in payment, each covered life alive, nothing
paid, the first year's income and a peak of 1; and in the first policy year, before any
anniversary, the income and the peak hold the first year's. On level and fixed escalation
the income and the annuitant's schedule are the contract's, re-derived at the valuation
date's key by one loop in `PA_UK_S`'s order, bit for bit (*The RPI and the income's
history*).

`PA_UK_S` rebuilds all six from References where its frame opens, which a Reference
changed at the valuation date would rewrite back to the start. Its survival is the
mortality basis run from the start, so an `annuitant_adj` changed at the valuation date
moves the survival and the payments of every month already run: here a test changes it and
the opening state stays the column. Its income on RPI-linked escalation is the flat
`rpi_rate` compounded from the start, so an increase capped at 5% under an RPI of 8%, or an
income the ratchet froze through a fall, which no flat rate set at the valuation date
gives, is in the column and not in S. A test writes each column off any path S makes and
projects it through.

| `PA_UK_S` | `PA_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in payment at the valuation date, 0 for a point starting at or after it |
| — | `duration_mth` | The policy clock, in months, any month of a policy year |
| — | `lives_if_init_1`, `lives_if_init_2` | `PA_UK_S` opens each life's survival at 1, at the start |
| — | `cum_annuity_all_init` | `PA_UK_S` opens the payments to date at 0 |
| — | `annual_income_init`, `rpi_peak_init`, `cum_annuity_pp_init` | `PA_UK_S` rebuilds the RPI's history from the flat rate of the day |

The columns carried over are read as `PA_UK_S` reads them. For a contract in payment, the
facts they record are those at the start date:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `annuitant_age`, `dependant_age` | years, age last birthday | the start date, not the valuation date: `age(0, life)` is the attained age there |
| `annuitant_sex`, `dependant_sex` | M or F | the start date |
| `rating_multiplier`, `dependant_rating` | factors, 1 or more | the start date |
| `dependant_present`, `overlap`, `proportion` | True or False | the start date |
| `purchase_price`, `annual_income` | pounds; pounds a year | the start date: the price value protection is measured on, and the first year's income |
| `frequency`, `timing` | 12, 4, 2 or 1 a year; arrears or advance | the start date |
| `escalation_type`, `escalation_rate` | a code; a rate a year | the start date |
| `guarantee_months` | whole months from the start date | the start date: the guarantee covers policy months 0 to `n − 1`, so the months of it left follow from `duration_mth` |
| `vp_pct`, `vp_basis` | a share of the price; a code | the start date |
| `mort_basis` | table or scenario | the basis from the valuation date on |
| `death_mth_1`, `death_mth_2` | policy months, or blank | the scenario's months of death, counted from the start date, so the same month whatever the valuation date |
| `start_year` | a calendar year | the year the annuity started, or will start |

Four more columns, `row_kind`, `source_policy_id`, `source_mth` and `source_refs`, record
where the generator took each shipped row from (below): `source_refs` names the References
a row was read from `PA_UK_S` under, `rpi_rate -0.02` on points 21 and 23 and
`rpi_rate 0.08` on point 22, and is blank on every row read at those `PA_UK_S` ships. No
formula reads them, and an in-force extract need not carry them: without them the model
projects the same numbers, and `run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the eight in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, which set to 0 refuses future new
business altogether; the two flags every point reads, `dependant_present` and
`proportion`, are True or False; the ages whole numbers below `2**53`, the income finite
and 0 or more, the frequency 12, 4, 2 or 1, the guarantee a whole number of months, 0 or
more, the value protection and the dependant's share from 0 to 1, the fixed escalation
finite and 0 or more; on the scenario basis each month of death blank
or a whole number, 0 or more; each survival a probability, the second 0 on a single life;
each state column in its domain where it is read; the start date's values on a point not
yet in payment, and the first year's in the first policy year; and on the scenario basis
each life's opening status its month of death's, alive while the death falls at the
valuation month or later; and on RPI-linked escalation the income of the year under way
is the first year's or more, to half a cent, the LPI's floor and the ratchet never letting
it fall: half a cent, so that an extract may carry it to the cent (USLIB-SEC-PLAN.md D6),
5,399.995 against a first year's 5,400 read and 5,399.99 refused.
`PA_UK_S` meets most of these only when a projection reaches them, and some never: `bool`
reads a blank flag as True, `int()` truncates an age, a frequency, a guarantee, a start
year and a month of death, and a negative month of death reads as a life that never dies
(UKLIB-SEC-PLAN.md §6.7, *S defects found*). Each window a rule reads, the start date's to
120 months on and the first policy year's, is held at both its ends.

Seven columns are read by a projection on some points and never on others, and each is
held on the points that read it alone, by the projection that reads it, as SPIA's C step
reworked its refusals (USLIB-SEC-PLAN.md §7.9, *Record — M23*, *Refusal by point*): each
sex, each rating and the start year, which the table basis reads and the scenario basis
never does, a sex M or F and one the mortality table rates, a rating a finite number 1 or
more, the dependant's on a contract with a dependant, and the start year a whole number
below `2**53`; the purchase price, finite and 0 or more, where value protection is
elected; and the overlap, True or False, on a contract with a dependant. The table reads,
and the point whose projection reads the value refuses it, naming itself, where no other
is refused for it: a scenario point whose rating is blank projects, as `PA_UK_S` projects
it, and a table point whose rating is blank is refused by its own projection (*The
compiled model*, *What it refuses*). The in-force step held each on every point as the
table was read. A value no projection reads may be text, so each column is read value by
value, never through the type pandas gives the whole column: one text in a column of
flags or numbers leaves pandas reading every value of it as text, where `bool("False")`
is True and `int("2026.0")` refuses, so that an overlap written `n.a.` on a single life
would read every joint contract's False as True. Each flag column is read by one rule,
`Data.flag_codes()`, which its check and its decode both read: True where `str()` of its
value, lowered, is `true`, False where it is `false`, and neither elsewhere, which the
check refuses, ` True`, `True `, 1 and 1.0 among it, each of which `PA_UK_S`'s `bool()`
reads as True. Each number is read through `float()`.

A contract at or past its stop rule, `duration_mth ≥ stop_mth()`, reads, but `proj_len()`
refuses it, naming the point: the stop is the product's rule, not the table's. So does a
contract owing nothing after the valuation date: in payment, its guarantee over and every
covered life dead, its last payment made before the valuation date, which an in-force
extract should not carry, as `SPIA_US_SEC` refuses it. The rule reads the lives and the
guarantee: a joint contract whose dependant is alive at a share of 0 projects, owing zeros,
which is no wrong number. So does a point the contract does not issue: a life issued below
`Projection.issue_age_min`, 0, since `PA_UK_S` projects any age on the scenario basis, a
negative one among them; on the table basis a limiting age above
`Projection.omega_age_max`, 116, the shipped table's last age plus one; a guarantee
longer than `12 × (omega_age − issue_age_min)` months, 1,380 as shipped and 1,392 at the
bound, the longest frame from the start date; and on either basis a frame longer than `12 ×
(omega_age_max − issue_age_min)` months, 1,392, from the start date, the longest the table
basis projects. Each bound is a lower-case Reference, the contract the compiled model's
caches are sized from: a frame of at most 1,392 months from the start and the horizon (*The
compiled model*). So does a point read under a Reference outside its domain, each named,
NaN and the infinities outside every one, since `PA_UK_S` reads several of them through a
`min` or a `max` whose bound comes first, which keeps the bound where a NaN meets it, or
through a power. Each is held on the points that read it:

| Reference | Read on | Domain | Outside it |
|---|---|---|---|
| `issue_age_min` | every point | a whole number of years below `2**53`, 0 or more | a NaN switches the bound off, every comparison with it failing; past `2**53` the compiled model's `long long` cannot hold it |
| `omega_age` | every point | a whole number of years below `2**53`, above `issue_age_min`; on the table basis at most a year past the last age the table rates each covered life's sex at, `Data.mort_age_last()` at its schedule, plus 1, 116, and at most `omega_age_max` | it sizes every frame; the table is read at attained ages to `omega_age − 1` |
| `omega_age_max` | every point | a whole number of years below `2**53` | the contract's largest limiting age, 116, which the caches are sized from: on the table basis it bounds `omega_age`, and on either basis the frame, at `12 × (omega_age_max − issue_age_min)` months; the scenario basis reads no table, and its `omega_age` is held to no bound |
| `expense_maint` | every point | finite, 0 or more | an expense |
| `inflation_rate` | every point | finite, −1 or more | the inflation factor changes sign each year |
| `annuitant_adj` | the table basis | finite, 0 or more | a mortality rate is negative; an infinity reads through the cap as certain death |
| `improve_rate_base` | the table basis | finite, below 1 | the improvement factor raises `1 − f` to a power, which at or below 0 has no real value or changes sign |
| `improve_flat_age`, `improve_taper_age` | the table basis | finite | the ages the scale is flat to and tapers to 0 at, shipped as floats, 90.0 and 110.0, so that a fraction reads in the compiled model as in modelx |
| `mort_table_year` | the table basis | a whole number below `2**53` | the calendar year the improvement counts from |
| `esc_fixed_cap` | fixed escalation | finite, 0 or more | a NaN switches the cap off, every comparison with it failing |
| `rpi_rate` | `lpi5` and `rpi_catchup` | finite, above −1 | the index, `(1 + r)^a`, is a price level, above 0; the LPI floor, `max(0, r)`, its bound first, reads a NaN as no increase |
| `esc_lpi_cap` | `lpi5` | finite, 0 or more | the cap, `min(cap, …)`, its bound first, which an infinity switches off |

Each check is a comparison written out, a finite bound the largest float and a whole one
`2**53`, so that the compiled model runs it in C; the four integer References are printed
through `int()` once they are whole, the others through `float()`, and a whole float,
`omega_age = 115.0`, is read as the whole number it is. Every accepted edge projects
through its reports. A value a formula computes past the floats from References and
columns each in its domain is refused in the cell where it first is, naming what made it,
where Python's power would raise `OverflowError`, naming nothing, and a product or C's power
would carry an infinity on: the income, in `annual_income` and in the valuation date's
loop in `annual_income_init`, under an escalation, an RPI or a history near the largest
float; the payments to date, in `cum_annuity_pp` and `cum_annuity_all`, where the
value-protection balance, `max(0, vP − G)`, its bound first, would read an infinity as no
balance; the three powers, the inflation factor under an `inflation_rate` of 1e200, the
catch-up's index under an `rpi_rate` of 1e200 and the improvement factor under an
`improve_rate_base` of −1e200, or of 0.999999 with `mort_table_year` 2100; and the
maintenance, in `expenses`, where the largest `expense_maint` inflates past them. A loop
over the block meets a refused row only when
it reaches it, after projecting the points before it, so `run_sec.py --block` asks every
point for its frame before it projects any, and stops before it prints anything.

The mortality table is checked before a value of it is read, in `Data.mort_sexes`, which
every array, extent and schedule of it asks first: each age a whole number below `2**53`
in size, checked before the ages are cast to int64, which would cast a larger float
without a word, each sex M or F, each sex running over the table's ages, 50 to 115, one
row an age, without a gap or a repeat, the gaps found in one pass over the ages each sex
holds, so that a key far from the rest costs no more than the rows, and each rate a
number from 0 to 1. A key is read by its
value, so an age written `65.0` is 65. Each refusal names the file, the column and the lines
at fault: the check reads the file as it stands, one read that `PA_UK_S`'s reader then
sorts. A read below the table's first age, a life issued younger than 50 on the table
basis, is refused by the one cell that reads it, `mort_rate_base_at`, naming the point and
the age, where `PA_UK_S`'s lookup raised `KeyError`; on the scenario basis, which reads no
mortality, the same age projects. No frame reads past the table's last age.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`PA_UK_S` and its table by `tests/uk_sec_support.py`, from the `PA_UK_SEC` entry in its
`SEC_SPECS`, and the tests regenerate it and compare, so an edit to a `PA_UK_S` row
reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py PA_UK_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 10 | twin | S points 1 to 10 | starting at `t = 0`: `PA_UK_S`'s worked example, its table basis, the guarantee without and with overlap, the single life in advance, the RPI catch-up, the LPI, the rated single life, the proportionate payment and last-survivor value protection |
| 11 | derived | S point 1 at S month 17 | the worked example in policy year 2, its annuitant dead in policy month 16, its dependant paid, 6,790.50 paid to date |
| 12 | derived | S point 9 at S month 16 | the proportionate payment's point in the month of its scenario death, value protection and the proportionate payment paid in month 0 |
| 13 | derived | S point 3 at S month 120 | the guarantee ended at the valuation date, the annuitant dead and the dependant's income starting |
| 14 | derived | S point 7 at S month 24 | the LPI on its second anniversary, opening with the income of the year it closes, 5,562.00, and escalating it in month 0 |
| 15 | derived | S point 6 at S month 30 | the RPI catch-up mid-way through policy year 3, an income of 5,728.86 and a peak of 1 |
| 16 | derived | S point 2 at S month 101 | the table basis in the last month of first-death value protection's balance, its survival 0.890787 and 0.944548 |
| 17 | derived | S point 10 at S month 170 | the last month of last-survivor value protection's balance, 471.67 left |
| 18 | derived | S point 8 at S month 575 | the rated life the month before the cap kills it, its survival 8.6e-10 |
| 19 | derived | S point 2 at S month 635 | the joint frame's last month, the annuitant past the limiting age: a one-row frame |
| 20 | future | S point 6, 13 months on | to start at `t = 13` |
| 21 | derived | S point 6 at S month 60, S run under an `rpi_rate` of −2% | the catch-up frozen: an income of 5,400, a peak of 1.0841658 over the index, and 27,000 of the annuitant's instalments to date |
| 22 | derived | S point 7 at S month 42, S run under an `rpi_rate` of 8% | the LPI capped at 5% each year: an income of 6,251.18 and 20,149.09 of the annuitant's instalments to date |
| 23 | derived | S point 7 at S month 54, S run under an `rpi_rate` of −2% | the LPI held at its floor: an income of 5,400 and 24,300 of the annuitant's instalments to date |

A derived row's `policy_count` is the count `PA_UK_S` weights every flow by, 1, which no
decrement moves, and its state what S carries into that month, so the row continues the S
projection from there. Its `policy_id` is the S row's with the month appended,
`PA-000001-M17`, and a future row's carries the months to the start, `PA-000006-F13`. Row
`t` of a generated point is month `t + source_mth` of its S point.

No state `PA_UK_S` reaches at its flat 3% holds a ratchet's peak above the index, nor an
LPI increase capped or floored: a monotone index never leaves the peak above it, and 3% is
inside the cap and above the floor. So points 21, 22 and 23 are read from S run under an
RPI of its own, the spec's `derived_refs`, and C2 freezes all three. Set on the model too,
that RPI gives each row S's path over the whole of both frames; at today's 3%, which takes
over from the valuation date, the income parts from S's at the row's next anniversary, and
survival, the floors and the counts, which read no RPI, stay S's. C2 projects every row at
the shipped References, under which the LPI's step is 3% on every row, so it freezes the
history the cap and the floor made, not the bounds themselves; a test projects the two LPI
rows under their own RPI, where the cap holds the increase at 5% and the floor at 0. A
committed row is one of S's points restated, so a contract term S's table never holds,
value protection apart from the dependant's share or on a single life, a dependant older
than the annuitant, is the splice's alone.

## Counts and timings

`PA_UK_S` weights every flow by a constant count, the contracts it was written for, and
carries mortality in each life's survival, so the count chassis is `SPIA_US_SEC`'s: the
count on the books is never decremented. `pols_if_init()` is the count in payment at the
valuation date: `policy_count` for a point already in payment, 0 for any other.
`pols_new_biz(t)` is `policy_count` in the start month, the month with
`duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` takes
`basiclife/BasicTerm_SE`'s two timings, each an int code named as `BasicTerm_SE`'s text
(*The compiled model*):

- `BEF_NB`, 0, the contracts carried in from month `t − 1`: `pols_if_init()` at
  `t_entry()`, the first month on the books, `policy_count()` after it, and 0 outside the
  frame, a closed form with no chain of calls back to `t_entry()`;
- `BEF_DECR`, 1, that count plus `pols_new_biz(t)`, the count that weights every cash flow
  of month `t`.

Any other timing raises. `pols_if(t)` is not the count: it is `PA_UK_S`'s closing
obligation measure on it, `pols_if_at(t, BEF_DECR) × min(1, max(C(t), l_a(t + 1)) +
1{δ > 0} (1 − l_a(t + 1)) l_d(t + 1))`, the guarantee certain, the annuitant alive, or the
dependant's pension in payment at the end of the month, the weight the maintenance expense
is carried on. It is 0.99999965 at `t = 0` on the twins of S's points 2, 6 and 7, against a
count of 1, so the registry marks the model `closing_pols_if`, as uslib's does
`SPIA_US_SEC`, and its conventions test reads the measure rather than the count there.

Each life's survival opens at `t_entry()` from the opening state and runs forward,
`l(t) = l(t − 1)(1 − q_m(t − 1))` on the table basis and the step function on the policy
clock on the scenario basis; the expected payments to date on every stream,
`cum_annuity_all(t)`, open from `cum_annuity_all_init()` and run forward; and the
annuitant's as-if-alive schedule, `cum_annuity_pp(k, ANNUITANT)`, keyed by the policy time
point, opens at the valuation date's key, `max(duration_mth_init(), 0)`, and runs forward
from there. So a contract valued late in life reads its balance without recursing back to
its start date, where `PA_UK_S`'s `G(k)` recurses from 0. Each of the three runs one cell
a month within a policy year, and in a year's first month after its opening reads the
year's opening, `lives_if_py(y, life)`, `cum_annuity_all_py(y)` or `cum_annuity_pp_py(y)`,
which walks the year before in ascending order, a cell a month, and returns its last
month's step, the same float, so that a compiled run's chains fit its stack (*The
compiled model*). On a model just read, a cold call in the frame's last month runs one
cell a month back to its policy year's first month, two cells a year before that, back to
`t_entry()`'s year, and at most 12 cells more, at each shape's longest cover, 1,392 months
from the start at the contract's largest limiting age, `omega_age_max`, 116, now, and as
deep 120 months on, which the full grid runs: on the scenario basis every life issued at
0; on the table basis every life issued at 50, the table's first age, whose age stop at
792 months a guarantee of 1,392 months, which `proj_len()` accepts at that limiting age,
carries to the longest frame. There the chain back to `t_entry()` is 241 cells, 11 within
the last policy year and two in each of the 115 before it, and the deepest call a
projection makes, a cold `cum_annuity_all(1391)` or claims total on the table basis, runs
253 cells deep, on the worked example's table twin, the RPI points and the rated life
alike, and 249 and 250 on the scenario basis's two shapes. At the shipped limiting age,
115, a year shorter, it ran 251 deep on a chain of 239, and one cell a month, as the
in-force step left the chains, `net_cf(1379)` ran 1,391 cells deep through survival.
The bound of 12 is the measure, every monthly cell called cold at every code, met with
nothing to spare, as `ULB_UK_SEC`'s 16 is: the walk's first month reads the year before's
opening and the table's first rate, as one cell a month did, and adds nothing. Issued
later, a chain runs the same cells over the same policy months, later on the valuation
clock: improvement, the income and the schedules are dated on the policy clock, and
inflation, the one cell the valuation clock dates, is a closed form outside every chain.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < stop_mth()`, started and short of the stop
rule, and outside it, before the start and from the stop rule on, every count is zero, and
so every cash flow. No cell reads a rate, a policy year or an attained age there that the
contract does not have: the mortality and improvement rates, the instalment, the floors,
the factors and the claims are zero outside cover, before any table or rate is read. A
contract's own end inside the frame, its last death or its last guaranteed instalment, is a
probability or a floor reaching zero, not the end of the frame, which runs on with zeros
as `PA_UK_S`'s does.

## The RPI and the income's history

`PA_UK_S` reads the RPI as one flat `rpi_rate` from the start: `rpi_catchup` indexes the
income to the running peak of `(1 + r)^a`, and `lpi5` escalates it each anniversary by
`min(5%, max(0, r))`. A flat rate is the same on either clock, so this model keeps it, the
assumed RPI from the valuation date on, and carries what the RPI did before the valuation
date in the opening state (USLIB-SEC-PLAN.md D7, as `SPIA_US_SEC`'s CMT change).

The income of the year under way, `annual_income_init()`, is the year `policy_year_init()`,
`(duration_mth_init() − 1) // 12 + 1` on a contract in payment, the year of the month
before the valuation date: on a contract valued on an anniversary it is the year the
anniversary closes, not the one it opens, because the anniversary's escalation is a month-0
event and applies at the valuation date's RPI, as every month-0 event reads the valuation
date's References (USLIB-SEC-PLAN.md D6, precised at M7). A test restates the LPI point at
its second anniversary under an RPI of 1%: it opens with its second year's income, 5,562.00,
and pays 5,562.00 × 1.01 from month 0. Each year after it escalates at today's References:

```
lpi5:         A(y) = A(y − 1)(1 + min(esc_lpi_cap, max(0, rpi_rate)))
rpi_catchup:  A(y) = A(y₀) × peak(y − 1) / peak(y₀ − 1)
```

with the index and its peak measured relative to the latest index, at the anniversary
`a₀ = y₀ − 1` that opened the year under way: `rpi_index(a) = (1 + rpi_rate)^(a − a₀)`,
and `rpi_peak(a₀) = rpi_peak_init()`, run forward from there. On a point starting at the
valuation date `a₀` is 0, and every index, peak and income is `PA_UK_S`'s, bit for bit.

The ratchet's catch-up branch, an index rising from below its peak, is unreachable in
`PA_UK_S` on a flat rate, so it gets goldens of its own on point 21: its income frozen at
5,400 through its sixth and seventh policy years, the index rising from 1 to 1.0609 under
a peak of 1.0842, and catching up in its eighth by the excess of the index over the peak,
5,442.64, then 5,605.92 and 5,774.10. Written at a peak of 1.2, the income stays frozen to
the eleventh year; at a peak of 1, read from the index, it would escalate at once, to
5,562.00 in the sixth.

On level and fixed escalation the income is the contract's schedule, re-derived at the
valuation date's key, `A(1)(1 + g)^(y₀ − 1)`, compounded in one loop in `PA_UK_S`'s order,
and the annuitant's payments to date are the schedule summed in one loop to the valuation
date's policy month, both bit for bit with `PA_UK_S`'s recursions. The six-month reference
lag of the source contract is not modelled, as in `PA_UK_S`.

## Departures from PA_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a month passed as `t` is a read at the policy month or year, and each recursion
opens at `t_entry()`, or at the valuation date's policy key, from the opening state. Where
`PA_UK_S`'s test would have stayed correct on the valuation clock, it moved anyway, so that
cover has one definition. Twenty-four cells are new with running in force, and nine more
with compiling, `point_id`, `mort_schedule`, the three chains' openings of a policy year,
`lives_if_py`, `cum_annuity_all_py` and `cum_annuity_pp_py`, the three refusals moved off
the chains, `annual_income_refusal`, `cum_annuity_all_refusal` and
`cum_annuity_pp_refusal`, and `cum_annuity_pp_all`, the payments on every stream by policy
time (*The compiled model*); none of `PA_UK_S`'s is gone.

| Cells | `PA_UK_S` | `PA_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `t_entry`, `stop_mth`, `is_active`, new | — | `max(0, −duration_mth_init())`; `max(horizon_mths(), guarantee_mths())`; `0 ≤ duration_mth(t) < stop_mth()` | The first month on the books, the stop rule on the policy clock, and cover |
| `proj_len` | `max(horizon_mths(), guarantee_mths())`, from the start | `stop_mth() − duration_mth_init()`, from the valuation date; raises at or past the stop, owing nothing, outside the contract's bounds, on a frame longer than the table basis's longest, 1,392 months from the start, on either basis, and under any of thirteen References outside its domain | The frame starts at the valuation date; no frame runs past the compiled model's caches. On the table basis the bound refuses nothing the in-force step accepted; on the scenario basis it refuses only frames longer than the table basis's longest, which the in-force step projected (*The compiled model*) |
| `is_payment_mth`, `is_payment_pm`, `annuity_pp`, `annuity_pp_pm` | `(t + 1) % step` and `t % step` on `t` | the schedule keyed by the policy month, read at `duration_mth(t)` | A contract in payment 17 months pays at policy months 17, 20, …, whatever `t` they fall at |
| `mths_since_payment`, `next_payment_mth` | on `t`; a scan month by month to the frame's end | on the policy month; a closed form, returning the policy month or −1 | The proportion rule's one far read, R2's look-ahead, gone |
| `claims(t, PROP)` | `inst(next(t))` | `A(policy_year(t)) / m` | On arrears the next payment falls in the policy year of month `t` |
| `claims`'s total | `claims(t)`, `kind` defaulted to `None`, Python's `sum` of the two kinds | `claims(t, ALL)`, `0.0 + claims(t, VP) + claims(t, PROP)`, left to right, the same float | A default compiles as a keyword the typing guard refuses, and `None` is no C integer (*The compiled model*) |
| `certain_floor`, `overlap_gate` | `t < n`, `t ≥ n` | `duration_mth(t) < n`, `duration_mth(t) ≥ n` | The guarantee counts from the start date |
| `lives_if`, `check_lives_roll_fwd_resid`; `lives_if_py`, new | 1 at `k ≤ 0`; the scenario step on `k`; the product from 0, one cell a month | `lives_if_init(life)` at `t_entry()`, 0 before it; the step on `duration_mth(t)`; the product from `t_entry()`, one cell a month within a policy year, and in a year's first month after it the year's opening, `lives_if_py(y, life)`, which walks the year before and returns its last month's step | Survival is history; the scenario's death months are policy months; blocked by policy year, so that the compiled chain fits its stack (*What a compiled run needs*) |
| `cum_annuity_pp`, `cum_annuity_all`, new; `cum_annuity_pp_py`, `cum_annuity_all_py`, `cum_annuity_pp_all`, `cum_annuity_pp_refusal`, `cum_annuity_all_refusal`, new | one recursion from `G(0) = 0` for both kinds, `"ANNUITANT"` and `"ALL"` | `ANNUITANT` on the policy clock, based at `max(duration_mth_init(), 0)` by one loop, or on RPI-linked escalation by `cum_annuity_pp_init()`; `ALL`, through `cum_annuity_pp_all(k)`, the new `cum_annuity_all(t)`, on the valuation clock from `cum_annuity_all_init()`, raising before the valuation date's key; each blocked by policy year through its `_py(y)` opening, and refused past the floats by its `_refusal` cell | Both parted by clock; the payments to date are history; codes for the kinds, and no message formatted on a chain (*The compiled model*) |
| `vp_balance` | keyed by S's time point | keyed by `t`: first death nets `cum_annuity_pp(duration_mth(t), ANNUITANT)`, last survivor `cum_annuity_all(t)`; 0 before `t_entry()` | The balance on the valuation clock |
| `annual_income_init`, `annual_income_first`, `policy_year_init`, new | `annual_income_init()`, the first year's income | `annual_income_first()`, the first year's; `annual_income_init()`, the year under way's, `policy_year_init()` | D6's name for the opening income |
| `annual_income`; `annual_income_refusal`, new | from `A(1)` at `y ≤ 1` | from `annual_income_init()` at `y₀`; refused past the floats, by `annual_income_refusal(y)` | The income's history is the contract's; no message formatted on a chain |
| `rpi_index`, `rpi_peak` | `(1 + r)^a`; the peak from `I(0)` | `(1 + r)^(a − a₀)`; the peak from `rpi_peak_init()` at `a₀`; the index refused past the floats | Relative to the latest index, the peak carried in |
| `inflation_factor`, `expenses` | `1.03^(policy_year(t) − 1)`, from the start | `1.03^(t // 12)`, from the valuation date; each refused past the floats | Unit costs in valuation-date pounds (D7) |
| `horizon_mths`, `payment_freq` | `12 × (omega_age − min x)`, `min` of a list; a tuple of the four frequencies | `omega_age` read through `int()`, the youngest life by one comparison; the four compared one by one | A whole float gives the int frame; no Python object in a computed cell |
| `mort_rate_base_at`, `mort_schedule`, new; `mort_rate_base`, `improve_rate`, `improve_factor`, `mort_rate`, `lives_death`, the floors and factors | unguarded: no `PA_UK_S` frame has a month outside cover | zero outside cover, before any table or rate is read; the table read in one cell, by the life's schedule and the age, its extents by schedule from `Data`, an age outside them refused by name; the improvement factor refused past the floats | Before the start S's lookup raises `KeyError` |
| `pols_if`, `pols_if_at`, `pols_new_biz`, `pols_if_init` | `pols_if_init() × min(1, …)` | `pols_if_at(t, BEF_DECR) × min(1, …)`, 0 outside the frame | The count enters once, in payment or in its start month |
| `result_pols` | `PA_UK_S`'s columns, `pols_if` last | `pols_if`, `pols_new_biz`, then `PA_UK_S`'s others in its order, 0 before the start | After `basiclife/BasicTerm_SE`'s `result_pols()` |
| `is_arrears`, `is_scenario`, `is_first_death`, `is_level`, `is_fixed`, `is_lpi5`, `is_rpi_catchup`, new | the label accessors, compared as text | `Data`'s decodes of `timing`, `mort_basis`, `vp_basis` and `escalation_type`, each read as its accessor reads the column, raising its message where the value is none it names | No projection cell compares text (UKLIB-SEC-PLAN.md §6.7, *C*) |
| `point_id`, new | the parameter | the label at position `idx`, read from `Data` | `Projection` takes the position (*The compiled model*) |
| `death_mth`; `sex` | the dependant's month of death read for any life but 1; `sex(2)` refused on a single life | life 1 or 2, any other refused, `invalid life`, as every cell of a life is; `sex(2)` the column as read, NaN on a single life | A life is a code of a 4-wide cache, and a cell refuses the codes it does not take; a label returns its column as read, as `SPIA_US_SEC`'s does (*The compiled model*) |
| `dependant_pct` | reads the column, then discards it on a single life | asks first whether the contract is joint | A single life's share is never read |
| `policy_count`, `duration_mth_init`, `lives_if_init`, `cum_annuity_all_init`, `rpi_peak_init`, `cum_annuity_pp_init`, new | — | the interface's columns | *The in-force interface* |

Of the cash flows, the change of clock moves the maintenance expense alone, and
`liability_cf` and `net_cf` with it. Point 11 carries that expense in valuation-date
pounds, so its `expenses(t)` is `PA_UK_S`'s `expenses(17 + t)` with S's factor,
`1.03^((17 + t) // 12)`, taken out and `1.03^(t // 12)` put in: 1.03 less at `t = 0`. Its
`pols_if`, its instalments, both claims columns and every survival are `PA_UK_S`'s from
month 17 on. Point 20 is `PA_UK_S`'s point 6 thirteen months on in those columns too; its
maintenance expense is `1.03^(t // 12 − (t − 13) // 12)` above S's at each `t`.

`mort_rate` caps the annual rate at 1, written `min(θ × q, 1.0)`, the product first and the
bound second, as `PA_UK_S` writes it, so that a NaN stays NaN where `min(1.0, θ × q)` would
read it as certain death. It binds on S's point 8, rated 1.35, from policy month 576 to the
end of its frame, where the rate is the float 1.0 in both models and every life alive at
the start of the month dies in it; so S's point 8 owes nothing after policy month 576, and
`proj_len()` refuses it restated later.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and how three of its chains reach back in time, and
no number: what the model computed on each committed point was frozen before the change,
and it still computes it, to the last bit (*Tests*, below). Cell by cell, at every argument
a full modelx sweep evaluates, the compiled model computes what modelx computes, bit for
bit, on the committed points, on the points of the splice grid, which take the branches
they do not, under each of the splice's RPIs, on the variants no committed row holds, at
the contract's longest covers, the 1,392-month guarantee at its largest limiting age among
them, at the frame's edge on the scenario basis past that limiting age, where the cap on
mortality binds, on every value a decoded column holds, on keys written as floats, and on
the LPI rows under the RPI they were read from. The compile tests hold it so on x86-64, and
to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py pension_annuity                  # in place, beside the model
python build_sec_cy.py pension_annuity --out /tmp/pa     # elsewhere, with the CSVs
```

The tool exports the model to `PA_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `PA_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/pension_annuity")     # the directory holding the build
from PA_UK_SEC_nomx_cy import mx_model as model
model.Projection[10].result_cf()                    # point 11, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`rpi_rate` say, leaves every value computed before as it was, in the base `Projection`
and in every ItemSpace made before, and only an ItemSpace made afterwards computes with
it. Set every Reference on a model just imported, before anything is computed, where
modelx would recompute; a test holds the compiled model to this, and the compile tests
project the LPI rows under their own RPI so.

A build takes about a minute and a half with gcc, 83 s here, and needs modelx-cython, which
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
taught first (USLIB-SEC-PLAN.md R1 to R17), and as `SPIA_US_SEC`, this model's chassis,
was at uslib's M23:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[10]` is point 11, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `annual_income_first()` is `float(data.annual_income()[idx])`. Compiled, the vector is a
  typed memoryview, and the read is a load from memory. The six columns of opening state
  are vectors too, and the three flags, `dependant_present`, `overlap` and `proportion`,
  are int64 vectors of 0 and 1, where a vector of bools would compile to a Python object.
- **A value, a flag and a sentinel.** A column a point may leave blank is read as `PA_UK_S`
  reads it, and where a vector cannot hold what a projection would read, a flag beside it
  says so (USLIB-SEC-PLAN.md R8). A single life's dependant age is 0, which no formula
  reads. A month of death left blank, the life surviving the projection, is −1, the
  sentinel `PA_UK_S`'s `death_mth` returns for it. And where a point's value is one its
  projection cannot use, its flag, `<column>_ok`, is 0, and the accessor that reads the
  value refuses it, naming the point (*What it refuses*). Every element is read by its own
  value, a flag by its column's one rule, `flag_codes()`, True where `str()` of it,
  lowered, is `true`, and a number through `float()`, never through `bool()` or `int()` of
  the value as pandas types it, since a text value one point holds leaves pandas reading
  the whole column as text (*The in-force interface*); a test writes such text where no
  projection reads it and holds every other point's every element, bit for bit.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the numbers it selects, for every point at once: `timing`, `escalation_type`,
  `vp_basis` and `mort_basis` into a 0/1 flag of each value a formula branches on,
  `is_arrears`, `is_level`, `is_fixed`, `is_lpi5`, `is_rpi_catchup`, `is_first_death` and
  `is_scenario`, beside a `has_*` flag that the value is one `PA_UK_S` names, which the
  decode reads first, raising `PA_UK_S`'s message where it is not; and each life's sex
  into the schedule of the mortality table it selects, `mort_schedule_1` and
  `mort_schedule_2`, the table's sexes numbered from 1 in sorted order, F 1 and M 2, and 0
  for a sex the table lacks, a blank among them, which `mort_schedule(life)` refuses
  where the table basis first reads it. Each decodes as `PA_UK_S` reads the column, which
  a test holds on every value a column can hold, and refuses what `PA_UK_S` refuses in its
  words, naming the point, as every refusal of a value the model point holds does: `point_id
  5: invalid timing`. A code a cell does not take, a call's error and no value's, keeps
  `PA_UK_S`'s constant, `invalid kind`, the chain cells raising nothing else.
- **The mortality table indexed by integers.** It is `mort_table_array`, by schedule and
  attained age, padded from age 0 so that the index is the age, beside each schedule's own
  first and last ages, `mort_age_first` and `mort_age_last`, 50 and 115 for both sexes as
  shipped. The padding holds NaN, and nothing reads it: the one cell that reads the table,
  `mort_rate_base_at(x, life)`, checks the age against its life's schedule's ages first,
  and is read in cover alone. Each sex has its own extents, so that a table whose sexes
  ran over different ages would read neither's padding, which a test holds on such a
  table; `Data` holds every sex to the table's ages, as the in-force step did.
- **Codes.** A timing or a kind, which `PA_UK_S` spells as text, is an int Reference
  named as the text. The count's two timings are `BEF_NB = 0` and `BEF_DECR = 1`; the
  kinds are numbered as one family, `claims`' first, `VP = 0` and `PROP = 1`, then
  `cum_annuity_pp`'s `ANNUITANT = 2`, and `ALL = 3`, either cell's total, so that a kind
  of one cell is refused by the other's: `claims(t, ANNUITANT)` raises `invalid kind`, as
  `cum_annuity_pp(k, VP)` does. A call reads as before, less the quotes:
  `pols_if_at(t, BEF_DECR)`. A string argument would give the cell a dictionary for a
  cache, where a code indexes a C array, so codes are numbered from 0 without a gap.
- **The claims total, a code of its own.** `PA_UK_S` totals the two kinds as
  `claims(t)`, its `kind` defaulted to `None`, with Python's `sum`. A default compiles as
  a keyword parameter the typing guard refuses, and `None` is no C integer, so the total
  is `claims(t, ALL)`, which `liability_cf` reads. It is written out,
  `0.0 + claims(t, VP) + claims(t, PROP)`, left to right, which is `sum`'s float wherever
  at most two kinds are non-zero, and there are only two: `sum` compensates since Python
  3.12, and the error of a single addition, added back, rounds to the sum it came from. A
  test holds the total to `PA_UK_S`'s by its bits.
- **The payments to date by code.** `cum_annuity_pp(k, kind)` keeps `PA_UK_S`'s key, the
  policy time point. `ANNUITANT` is the annuitant's as-if-alive schedule on the policy
  clock, from its static base at the valuation date's key. `ALL` is
  `cum_annuity_pp_all(k)`, a cell of its own, which reads `cum_annuity_all` on the
  valuation clock and refuses a key before the valuation date's, where the payments to
  date are one total; no cell reads it, the last death's balance reading
  `cum_annuity_all(t)` itself.
- **One comparison where a list was.** `horizon_mths()` finds the youngest covered life by
  one comparison, the dependant's issue age against the annuitant's on a joint contract,
  where `PA_UK_S` takes the `min` of a list; and `payment_freq()` compares the frequency
  with each of the four, where `PA_UK_S` asks whether it is in a tuple.
- **Three chains blocked by policy year.** Survival on the table basis, `lives_if(t,
  life)`, the expected payments to date on every stream, `cum_annuity_all(t)`, and the
  annuitant's as-if-alive schedule, `cum_annuity_pp(k, ANNUITANT)`, each run one cell a
  month within a policy year, as at the in-force step, and in a year's first month read
  the year's opening, `lives_if_py(y, life)`, `cum_annuity_all_py(y)` and
  `cum_annuity_pp_py(y)`. Each opening walks the year before in ascending order, asking
  the monthly cell of each of its months, so that each finds the month before cached, and
  returns the step across the year's last month, `l(t − 1)(1 − q_m(t − 1))`,
  `G_all(t − 1)` plus that month's expected instalments, and `G(k − 1) + inst(k − 1)`,
  the monthly cell's own floats in its own order, so no number moves. A cold read then
  runs one cell a month back to its year's first month and two cells a year before that,
  where one cell a month ran the whole cover on the C stack (*What a compiled run needs*,
  below). The income and the ratchet's peak recurse by the year already, and survival on
  the scenario basis is a step function, which recurses not at all.
- **No refusal formatted on a chain.** A compiled cell's C frame holds the code that
  formats each of its messages, whether a run reaches it or not, and a chain holds a frame
  of each cell it recurses through at each level (UKLIB-SEC-PLAN.md K12). So the cells the
  chains recurse through format nothing. Where the payments to date or the income have
  left the floats, `cum_annuity_all(t)` calls `cum_annuity_all_refusal(t)`,
  `cum_annuity_pp(k, ANNUITANT)` calls `cum_annuity_pp_refusal(k)`, and
  `annual_income(y)` calls `annual_income_refusal(y)`, each of which computes the value
  again from the same cells, the same float, and raises the in-force step's message,
  naming the month, the key or the year. Each takes the key alone, since a float
  parameter would give it a dictionary for a cache, and returns the value where it is
  finite, which the sample asks for to type it. A test holds every cell that a cold call's
  deepest path holds more than once to building no text and raising only a constant. The
  powers' refusals stay in `inflation_factor`, `rpi_index` and `improve_factor`, and the
  mortality table's in its reader: no chain recurses through them, each read once, at a
  path's foot or off it.
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex(life)`,
  `payment_timing()`, `escalation_type()`, `vp_basis()` and `mort_basis()`, and the two
  reports return a table row, text and DataFrames, for a reader, for `run_sec.py` and for
  the comparison with `PA_UK_S`. No other cell calls them, so they cost the projection
  nothing. The four that validate their column, as `PA_UK_S`'s do, return text or raise,
  and compile to `str`. `sex(life)` returns its column as read, as `SPIA_US_SEC`'s does,
  NaN on a single life's blank dependant, where `PA_UK_S`'s refuses a single life's second
  life, and compiles to a Python object. The registry names the column each label returns
  where it is not its own, `payment_timing` `timing` and `sex` the annuitant's or the
  dependant's by its argument, so that the compile tests compare each label with its
  column.

The `Data` docstring lists its 49 vectors by point, its mortality array and the two
extents by schedule, and its one check, `mort_sexes`, an int, each with the column or
file it comes from. The four readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 92 of
its 100, returns a C `bint`, `long long` or `double`, 17, 21 and 54 of them, and caches a
single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,514 by `t`, of `double`, `long long` or `bint` | the 29 cells of `t` alone: every count, factor and cash flow, the payments to date on every stream and their refusal, the balance, the policy clock, its years, the calendar year and the payment months, the checks' residuals, and the flag `is_active` |
| a C array of 1,514 by 4 | the eight cells of `t` and a life, each life's rates, survival, deaths and attained age; `pols_if_at(t, timing)`; and `claims(t, kind)` |
| a C array of 1,394 by policy time, or 1,394 by 4 | the schedule, `is_payment_pm(k)` and `annuity_pp_pm(k)`; the annuitant's payments to date and their refusal; `cum_annuity_pp_all(k)`; and `cum_annuity_pp(k, kind)` |
| a C array of 118 by policy year, or 118 by 4 | the income and its refusal, and the three chains' openings |
| a C array of 117 by anniversary | `rpi_index(a)` and `rpi_peak(a)` |
| a C array of 117 by 4, by attained age and life | `mort_rate_base_at(x, life)` |
| a C array of 4 by life | `age_at_entry`, `mort_schedule`, `rating_factor`, `death_mth` and `lives_if_init` |
| one `bint`, `long long` or `double` | the 35 other cells without a parameter: the point's numbers, decodes and flags, its opening state, the ends of its frame, the frequency and the guarantee, and the four checks |
| a Python object, or `str` | the eight reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the two reports
and the four checks on every committed point, and then the cells no report reaches:
`model_point()` and the five label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; the dependant's `lives_death`, which the last-death density
replaces in every flow; `is_payment_mth`, which value protection asks in advance alone,
and no committed point with value protection pays in advance; `next_payment_mth` and
`mths_since_payment`, which only the proportionate payment reads; `cum_annuity_pp` at
`ALL`, which no cell reads; and the three refusals moved off the chains, which only their
cells' error paths call, where a value has left the floats, and which return the value
elsewhere, so that the sample's calls of them type them: the monthly one in every month of
the frame and the month after it, the payments' at every key a projection reads, and the
income's in every year from the one under way at the valuation date to the frame's last.
It runs the committed points alone: the export reads the CSVs of the directory the build
is made in, which in place is the product directory. The committed points leave branches
untaken: semi-annual and annual payments, a dependant older than the annuitant, value
protection paid in advance, the LPI's cap and floor binding, a ratchet whose peak the
index passes, and a power, an income or a total past the largest float. That still types
every cell, because every branch of a cell returns the one type its others return, a
probability or an amount a float in every branch, `0.0` or `False` outside the frame, and
on points that take those branches the compiled model computes modelx's numbers (above).
The labels are typed from the committed points too, the three single lives among them, so
that `sex(2)` returns NaN beside the text of every other call, and `sex` is typed as the
reporting cell it is. The sample also raises the recursion limit, which modelx raises and
its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
at its closing time point, `t = proj_len()`, which survival and the payments to date read
and the compile tests' full sweep evaluates every monthly cell at; plus one because the
index starts at 0; and one of headroom where that leaves room, as `SPIA_US_SEC`'s spec
sizes its own, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,514 | 1,512. The longest frame is the longest cover, a life issued at 0, `issue_age_min`, to the age stop at the contract's largest limiting age, `omega_age_max`, 116, or a guarantee of as many months on the table basis, which `proj_len()` admits at that limiting age, starting 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × (116 − 0) + 120 = 1,512 months, `t = 0 … 1,511`, and its closing time point, 1,512. Nothing reads `t + 1` there |
| `t`, `life`; `t`, `timing`; `t`, `kind` | 1,514 by 4 | `t` as above, by the two lives, the two timings, and the two kinds and the total. Every 2-D cache of a model shares one inner width, the widest, the kinds' four: Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `k`; `k`, `kind` | 1,394; 1,394 by 4 | 1,392, the stop rule's policy month on the longest frame, 12 × (116 − 0), the payments to date's closing key; the schedule is read to 1,391 |
| `y`; `y`, `life` | 118; 118 by 4 | 117, the policy year of the longest frame's closing time point, 1,392 months from the start, whose opening the three chains read; the income is read to 116. No headroom: 117 is the largest a frame reaches |
| `a` | 117 | 115, the anniversary of the income's last policy year, read by the index and the peak |
| `x`, `life` | 117 by 4 | 115, the last attained age below the largest limiting age, read by the mortality table's one reader from an issue age of 0, below which the reader refuses the age by name |
| `life` | 4 | the two lives, widened to the inner width, so that a life of 0 or 3 is refused by the formula in both engines |

**The limiting age the caches hold.** The sizes are derived from three References, the
contract: `issue_age_min`, 0, below which `proj_len()` refuses a covered life's issue age,
and refuses itself below 0; `omega_age_max`, the largest limiting age, 116, the shipped
mortality table's last age plus one; and `Data.future_horizon_mth`, 120, past which `Data`
refuses an annuity to start. On the table basis `proj_len()` refuses an `omega_age` above
`omega_age_max`, after the table's own last age plus one, which is the same 116 on the
shipped table, so that every limiting age the shipped table admits projects, in modelx as
compiled, and a longer table's limiting age is held to the bound, as `ULB_UK_SEC`'s is
(UKLIB-SEC-PLAN.md §6.6, *Record — M10*). It refuses a guarantee longer than `12 ×
(omega_age − issue_age_min)` months, at most 1,392 there, so no frame the table basis
projects outruns the caches. The scenario basis reads no mortality, and the in-force step
projected it at any limiting age, so `proj_len()` holds its `omega_age` to no bound, as
`SPIA_US_SEC` holds its own to none. But it holds the frame, on either basis, to the table
basis's longest, `12 × (omega_age_max − issue_age_min)` months, 1,392, from the start date,
refusing a longer one, naming the point: `point_id 1: the frame, 1393 months from the start
date, is longer than 1392 months, 12 x (omega_age_max - issue_age_min), the longest the
table basis projects, which the compiled model's caches are sized from`. This departs from
the in-force step, and from `PA_UK_S`, which project such a frame, so that no frame either
engine accepts passes the caches. On the table basis the rules before it admit no longer
frame, so it refuses nothing the in-force step accepted; on the scenario basis it refuses
only frames longer than the table basis's longest, a covered life issued younger than
`omega_age` − 116 or a guarantee past 1,392 months, which compiled ran past the caches and
raised a bare `IndexError`, naming nothing. An `omega_age` above 116 projects there, in
both engines alike, wherever every covered life was issued at `omega_age` − 116 or older
under a guarantee of at most 1,392 months, and a test runs its longest frame compiled, at
the worst configuration the caches meet, value protection on the first death issued 120
months on, and refuses a month more alike in both. A larger bound or horizon needs the
sizes derived again, as `spec_sec.py` derives them, and a rebuild, `issue_age_min` being 0,
the least `proj_len()` admits: `t` raised to 12 × (`omega_age_max` − `issue_age_min`) + the
horizon + 2, `k` to 12 × (`omega_age_max` − `issue_age_min`) + 2, `y` to `omega_age_max` −
`issue_age_min` + 2, `a` to `omega_age_max` − `issue_age_min` + 1, and `x` to
`omega_age_max` + 1.

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as the year walks' month counter or the schedule's loop, stays a Python
object, though the cell is typed `double`; without `cpow`, `1 − (1 − q)^(1/12)`, the
monthly rate of each life's mortality, and the three powers, the inflation factor, the
RPI's index and the improvement factor, are complex powers, which gcc computes with `cpow`
rather than `pow`, and whose last bits can differ from Python's; and gcc fuses a multiply
and an add where the target has the instruction, one rounding where Python rounds twice.
The tool's docstring has the detail, and uslib's
[`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the measurements
that put each there. With all four, every compiled value here agrees with modelx bit for
bit. The compile tests hold each directive in the module's first line, and a static test
holds the tool's line to the two and no other.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
1,390,576 bytes, the type's basic size, which holds every cell's cache, and deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a test runs the compiled runner on a block of the committed points repeated and finds
no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 26. What it needs
is stack. That call is a cold one in the last month of the longest cover, now or 120
months on: on the scenario basis every life issued at 0, and on the table basis every life
issued at 50, under a guarantee to the limiting age's stop. At the shipped limiting age,
115, 1,380 months from the start, one cell a month, as the in-force step left survival
and the payments to date, the call ran 1,391 cells deep in modelx, and compiled with gcc
each chain head, cold in an ItemSpace of its own, needed 244 to 276 KiB of C stack,
measured to 4 KiB: `net_cf` 256 to 276, the
payments to date on every stream, the claims and the balance up to 276, and 33 of the 43
heads above the 256 KiB the C step allows itself, so that the 1 MiB thread holds on every
runner, where `Term_UK_SEC`'s cold call needed two to four times as much on CI's Ubuntu
runner as here (UKLIB-SEC-PLAN.md §6.1, *Record — M2*), and where `SPIA_US_SEC`, this
model's chassis, kept a margin of 1.33 to 1.6 times under 1 MiB on gcc (USLIB-SEC-PLAN.md
§7.9, *Record — M23*). So the three chains are blocked by policy year (*What compiling
changed*, above), and no cell they recurse through builds text. Blocked, the call runs
251 cells deep in modelx, on a chain of 239, one cell a month within its year and two
cells a year before it, and 12 more; at the contract's largest limiting age, 116, 1,392
months from the start, 253 on a chain of 241, which a test holds. Compiled, at 115,
every head runs on 52 to 76 KiB and not on 4 KiB less, issued now and 120 months on
alike: on the table basis,
survival, the payments to date on every stream and the claims on 76, `net_cf` and the
obligation measure on 72, the balance on 64 and the survival check's residual on 56; on
the scenario basis, every head on 52 to 64. A test runs each shape at its longest cover
in a thread of 1 MiB, the stack Windows gives a program's main thread unless the program
is linked for more, and again on the main thread, which is where `run_sec.py --cython`
runs, at the contract's largest limiting age, and records the smallest of its sizes each
ran on: 96 KiB here, and not 64. MSVC's frames may be larger than gcc's, and the
`cython_uk` CI job, which runs the test on Windows too, is the check on them. That test
holds the stack the call needs, not the blocking: with the three chains left one cell a
month the call runs on 384 KiB here and not on 256, well inside 1 MiB, and passes it, so
only the depth test, which counts the cells a cold call runs through in modelx, holds the
chains to their blocks. The export recurses in Python instead: the same call at 116 needs
a recursion limit of 521 there, its `net_cf` 500 to 507, and the reports and checks, which
run in ascending `t`, need 128, so `sample_sec.py` sets 3,000, four times the first
rounded up to the thousand.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message: each
malformed row of the table, each value refused by the point that reads it, each mortality
table a reader cannot read, each text value no decode knows, each point the frame refuses,
a point owing nothing among them, each Reference outside its domain that the compiled
model can hold, the income, the payments to date, the three powers and the maintenance
past the floats, a key read below the mortality table, and what the vectors cannot hold,
in a cell typed `long long` or `double` as in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, and an
age or a year as an int. So a rate written as an int, 2, gives one message in both
engines. An int Reference, `issue_age_min`, `omega_age`, `omega_age_max` or
`mort_table_year`, is a C `long long` compiled, and a float set on it is truncated as it
is set, 115.5 to 115, where modelx refuses 115.5 as not a whole number, and a NaN or an
infinity cannot be set on it at all; so set each as a whole number. The improvement ages,
which may be any finite number, ship as floats, 90.0 and 110.0, so that the compiled model
holds them as `double` and a fraction set on either reads as in modelx.

- What `Data` cannot decode or hold, when the vector is first read, naming every point or
  line at fault: a `point_id` that is not a whole number, or is `2**53` or more in size; an
  age `2**53` or more in size, which an int64 vector cannot hold whole and numpy would cast
  without a word; a mortality age as large, or 1e300, before the table is cast, and a key
  far from the rest, `2**53 − 1`, as a gap at once; and, as since the in-force step, each
  malformed value of a column every point reads, a flag spelt ` True`, `True `, 1 or 1.0
  among them, which `PA_UK_S`'s `bool()` reads as True, refused by the one rule its decode
  reads too, `flag_codes()`. A key written as a float, an age `65.0`, is read by its value,
  as `PA_UK_S`'s lookups match it.
- A value only some points read, by the point that reads it, naming that point, as it first
  reads the value (*The in-force interface*): `point_id 8: rating_multiplier must be a
  number, and a finite one, 1 or more, on the table basis, which reads it; it is not`, on
  the rated single life written at 0.9. An overlap spelt as above, on a contract with a
  dependant, is refused so, by the rule its decode reads. A start year that is not a number
  below `2**53` in size, read through `float()`, and a month of death `2**53` or more in
  size, are refused the same way, by its accessor, on a point that reads it. A text value
  of `timing`, `escalation_type`, `vp_basis` or `mort_basis` that is none of `PA_UK_S`'s, a
  proportionate payment in advance and a fixed escalation past its cap are refused in
  `PA_UK_S`'s words, naming the point, by the decode or the cell that reads them.
- A key beyond the mortality table, by the one cell that reads it, where `PA_UK_S`'s
  lookup raised `KeyError`: `point_id 2: mort_table.csv has no rate at attained age 49`,
  on the worked example's table twin issued at 49, a year younger than the table. No
  frame reads past the last age, which `proj_len()` holds `omega_age` to.
- A power past the largest float, which Python's float power refuses with
  `OverflowError` where C's `pow` gives an infinity: the inflation factor, the RPI's
  index and the improvement factor each call Python's own power where their own is
  infinite from a finite base, so that the compiled model raises the same `OverflowError`
  as modelx does (uslib's *Record — M22* form), and the one `except` around both turns it
  into the in-force step's message, naming the point and the Reference, in either engine.
  Only a rate past every rate of inflation reaches them: a test does, under an
  `inflation_rate` and an `rpi_rate` of 1e200 and an `improve_rate_base` of −1e200. And
  each power checks its result, as at stage E, so that a base that is NaN or an infinity,
  which `proj_len()` refuses as a Reference before any report reaches a power, is refused
  by the power too on a direct call, in both engines.
- An `omega_age` above `omega_age_max` on the table basis, by `proj_len()`, which only a
  mortality table longer than the shipped one, or the bound lowered, can bring about:
  `point_id 2: omega_age, 116, is above omega_age_max, 115, on the table basis`, under a
  bound lowered to 115.
- A frame longer than the table basis's longest, `12 × (omega_age_max − issue_age_min)`
  months, 1,392, from the start date, by `proj_len()`, on either basis, which only the
  scenario basis, whose `omega_age` no bound holds, or the bound lowered, can bring about:
  `point_id 1: the frame, 1393 months from the start date, is longer than 1392 months, …`,
  on the worked example issued 120 months on, both lives at 1 under a limiting age of 117
  and a guarantee of 1,393 months. The in-force step projected such a frame on the scenario
  basis, which ran past the caches compiled (*The limiting age the caches hold*).
- A timing, a kind or a life no cell takes, by the cell, as `PA_UK_S`'s are: `invalid
  timing`, `invalid kind` and `invalid life`. Each 2-D cache is 4 wide, so a code inside it
  that its cell does not take, a timing past `BEF_DECR`, a kind of the other cell or a
  life of 0 or 3, reaches the formula, which refuses it in both engines, as a test holds.

An argument outside a cache raises `IndexError` in the compiled model alone: `net_cf(1514)`
or `net_cf(-1)`, which modelx answers with 0, the month being outside the frame;
`pols_if_at(t, 4)`, `claims(t, 4)`, `cum_annuity_pp(k, 4)` and `lives_if(t, 4)`, which
modelx refuses as codes it does not take; and a key, a policy year, an anniversary or an
attained age past its cache, `cum_annuity_pp(1394, ANNUITANT)`, `annual_income(118)`,
`lives_if_py(118, 1)`, `rpi_peak(117)` or `mort_rate_base_at(117, 1)`, which modelx computes
or refuses as at any other. No frame `proj_len()` admits, on either basis, reads any of
them (*The sample and the spec*). An `idx` past
the last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's last
point, under that point's own `point_id()`; the compiled refusal test holds both against
modelx.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
product at 1, as `PA_UK_S` does, and a compile test holds the two equal on S's point 8,
rated 1.35, where the cap binds from policy month 576 to 599, as a twin and restated in
payment the month before and the month of it. A NaN product would stay NaN through the
cap, in both, which the compiled model computes as a comparison that keeps the value
unless the bound is smaller.

### Speed

`python tools/bench_sec_cy.py pension_annuity` builds the model into a temporary directory
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
| compiled | 6,003 | 0.364 ms (0.353–0.366) | 0.803 ms (0.793–0.842) | 87–88 MB |
| export | 621 | 5.31 ms (5.31–5.31) | 5.80 ms (5.54–5.86) | 87–88 MB |
| modelx | 138 | 152 ms (145–154) | 157 ms (146–160) | 121–122 MB |

On `net_cf` the compiled model runs 14.6 times its export (14.5 to 15.0 over the three),
and on `result_cf`, where building the DataFrame takes more than half its time, 7.2 times
(6.6 to 7.4); it runs 417 times modelx on `net_cf` (399 to 435) and 190 on `result_cf`
(184 to 196). The ranges are the noise of a machine other work was using, its 1-minute
load between 1.0 and 2.0 as the runs started. A point here costs more on every engine
than one of `Term_UK_SEC`'s or `ULB_UK_SEC`'s, its frame being longer: 552 months on
average over the committed points, against `ULB_UK_SEC`'s 340 and `Term_UK_SEC`'s 244.
The release keeps a block flat: the compiled model's peak and the export's grew by less
than 0.1 MB over their 6,003 and 621 points in every run, where modelx's rose by 34 to 35
MB in its loop. Reading the two files and building every `Data` vector and array for the
compiled block took 0.04 s, and asking every point for its frame, the runner's first
pass, 0.15 to 0.16 s. Every engine, loop and run summed `net_cf` over a copy of the table
to the same −5,946,586.352, to 1e-9 relative.

Measured on 2026-11-25 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.30 GHz), a 1-minute load average between 0.98 and 1.99 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`, at the caches
`omega_age_max` sets, its ItemSpace's struct 1,390,576 bytes. Timed on 2026-11-23, before
`omega_age_max` raised every cache by a year and grew that struct by 0.8%, at a load of
1.5 to 4.0, the model ran `net_cf` in 0.393 ms compiled, 5.92 ms as the export and 192 ms
in modelx; the load, more than the caches, moves these figures.

## Tests

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 1 to 10, every
  cell of `PA_UK_S`'s agrees at every argument `PA_UK_S` evaluates in its own sweep, to
  1e-9 relative with no absolute floor, but `pols_if_init`, `model_point` and
  `result_pols`, the harness's two and the one the spec names, with their reasons;
  `annual_income_init` is compared, and is the first year's income on a twin. A cell this
  model lacked would fail it. So `PA_UK_S`'s worked example, which
  `tests/test_pension_annuity_uk.py` asserts to the penny, holds here with no number
  restated. The kinds and timings are compared as the codes of the same names, and
  `PA_UK_S`'s claims total, `claims(t)`, with `claims(t, ALL)`. The same suite holds the
  model to the conventions every `_SEC` model meets: every frame starts at `t = 0`,
  `pols_if` is the closing measure on the `BEF_DECR` count, new business enters once at
  its `policy_count`, nothing happens before the start, and the in-force columns are
  present.
- **The splice**, in `tests/test_pension_annuity_uk_sec.py`: each `PA_UK_S` point
  restated in payment at months 1, 2 and 3, about the first quarterly payment in arrears,
  11 to 13 and 23 to 25, about the first two anniversaries, 15 to 17, about the scenario
  death, 101 and 102 and 170 and 171, where first-death and last-survivor value protection
  run out, 119 to 122, about the guarantee's end, 575 and 576, about the cap, 599 and 600,
  where the older life reaches the limiting age, and 635, continues the S projection in
  every cell the two share but `proj_len` and the survival point, a time point on each
  clock, and in both reports, to 1e-9 relative with no absolute floor but the residuals;
  the opening income is held to S's of the year under way, and the relative index and peak
  to S's over its index at the latest anniversary. Inflation, the one input on the
  valuation clock, is 0 in both. Sixteen variants of S's points, in a copy of S's table
  that is never committed, reach what S's own cannot: advance timing with value
  protection on either basis, the last survivor's on the table basis, where a claim is
  paid; semi-annual and annual payments; the dependant dying first; both lives dead with
  and without a guarantee; a guarantee past the age stop; a rated joint life; the
  proportionate payment on the table basis; the RPI points without first-death value
  protection; value protection of 30% beside a dependant's 50%, and on a single life; a
  dependant older than the annuitant; and a dependant's share of 0. The RPI points are
  spliced under RPIs of 8% and −2%, where the LPI's cap and floor bind and the ratchet
  freezes, and the worked example's table twin beside them, its fixed 3% apart from either
  RPI. A core of 44 of the 378 splice cases and 7 of the 46 future ones runs by default,
  and the full grid with `UKLIB_SEC_FULL=1`, the depth test's shapes issued 120 months on
  among it; a test asserts the core reaches every branch, opening-state column, kind of
  valuation month and side of every `min` and `max` the full grid reaches.
- **Future new business**: starting 1 and 12 months after the valuation date, each S point
  is the S projection moved on, with zeros before the start and no rate evaluated there,
  and so is each variant starting a month on, the catch-up point 13 months on and the
  worked example 25, and the RPI points under each RPI.
- **How it computes**: on every row of the splice's grid, after its reports, its checks and
  every monthly cell at every month, no cell has been called at a negative month, none on
  the books read a month before `t_entry()`, none read a month later than `t + 1`, none on
  RPI-linked escalation asked a year, an anniversary or a policy month before the valuation
  date of the cells keyed on the policy clock, none raised, and every check holds, the
  whole survival check among them. On a fresh read of the committed model,
  `duration_mth(500)` evaluates `duration_mth` once, the policy clock being a closed form,
  and every point's reports and checks run under modelx's recursion limit lowered to 40,
  which a recursion backward over the frame would exceed. Each chain, called cold in the
  last month at each shape's longest cover, at the contract's largest limiting age, runs
  one cell a month back to its policy year's first month, two cells a year back to
  `t_entry()`'s, and at most 12 more, each shape's deepest as measured, 253 on the table
  basis's; each year's opening, of survival
  and of the payments to date on either clock, is the step of the year's last month, by
  its bits; the schedules at the valuation date's key are S's, bit for bit, and a
  contract valued in its last month runs its reports within 10 cells; no computed cell
  but the reporting ones holds a Python object; and no cell that a cold call's deepest
  path holds more than once builds text anywhere in its formula, at a raise, in an error
  branch or into a local, or raises other than one exception on one string constant.
- **Counts**: the count is never decremented, `BEF_NB` a closed form, and `pols_if` the
  closing measure on it; `result_pols()` is S's report with `pols_new_biz` beside it;
  multiplying `policy_count` by 2.5 multiplies every flow and counted cell and moves no
  per-contract value, every flow nonzero on some point; and each point in payment, restated
  a month on with the state it carries there, continues its own flows.
- **Validation and regeneration**: each malformed row of the table, 70 cases, is refused
  naming its point, on the committed labels and on an extract's; each value no projection
  can use in a column only some points read, 16 cases, is refused by a point that reads it,
  naming it, on an extract's labels, where a point that never reads it projects as on the
  committed table, in both reports, exactly, and every other point reads every `Data`
  vector as on the committed table, bit for bit, start years written as floats beside a
  text one among them; an overlap written as text on the single lives leaves every joint
  contract's read as committed; each flag spelt ` True`, `True `, 1 or 1.0 on a point that
  reads it is refused by its check, or read as True by its decode, the two reading one
  rule, all four alike; each text value no decode knows raises `PA_UK_S`'s message, naming
  the point, on the committed labels and on an extract's; the horizon is a Reference; a
  point at its stop, one owing nothing and one the contract does not issue are refused by
  `proj_len()`, each bound just past it and each moved past a committed point, a frame a
  month past the table basis's longest on the scenario basis among them, and
  `run_sec.py --block` refuses such a point before printing anything; the table basis's
  longest frame projects on the scenario basis past `omega_age_max`, at the worst
  configuration the caches meet; each of thirteen References is held to its domain, 121
  cases, each edge accepted and its reports projected, and the nearest value past it
  refused, NaN, the infinities, a fraction, `2**53` and a whole float too, `omega_age_max`
  bounding the table basis's limiting age and every frame; the income, the payments to
  date, the three powers and the maintenance are refused where they would pass the floats,
  naming the References, the payments to date at an anniversary as in any other month; each
  power refuses a base that is no number on a direct call; each window of `Data`'s is held
  at both its ends; each mortality table a reader cannot read, 16 cases, an age of `2**53`,
  of 1e300 and one far from the rest among them, is refused naming its lines, and a read
  beyond it naming the point; keys written as floats read as `PA_UK_S` reads them; the
  edges of the interface and of each bound are accepted; every state `PA_UK_S` reaches, as
  shipped, with the variants and under each RPI, is accepted in payment, but a contract
  owing nothing, which is refused; and the committed table is what `PA_UK_S` generates.
- **The product's own facts**: the two clocks on the shipped points; the committed rows
  continuing their S points at the shipped assumptions but for inflation, and the three
  read under an RPI of their own continuing S under it, the two LPI rows projected under
  it to the cap's and the floor's goldens; each history column read, not
  recomputed: survival and the payments to date kept under an `annuitant_adj` changed at
  the valuation date and written off S's path, the LPI's capped income and an income no
  flat RPI gives, the ratchet's catch-up with its own goldens, and the annuitant's payments
  to date (UKLIB-SEC-PLAN.md K14); the income measured before month 0's anniversary; the
  RPI one flat rate on either clock; expense inflation on the valuation clock at the
  shipped 3%, which only this test sees; improvement and the payment schedule on the
  policy clock; no premium and no acquisition; every guarded cell's value outside cover;
  the block; an extract without the generator's columns, labelled otherwise,
  projecting the same numbers; `run_sec.py`'s numbers, for a point and for the block, and
  its sum, and its `--cython` stopping where no repository is above it; no cell's
  parameter defaulted, and `cum_annuity_pp`'s total refused before the valuation date's
  key; the
  docstrings, read through docutils as the docs build reads them where docutils is
  installed; and the shared input table.
- **The cap**: on S's point 8 the rated rate passes 1 from policy month 576 to 599; in
  both models `mort_rate` and `mort_rate_mth` are the float 1.0 there, every life in payment
  at the start of that month dies in it, none is alive after it, and the reports hold
  finite floats, on the twin and restated in payment the month before. A NaN sent to the
  cap, through `annuitant_adj`, stays NaN; and each check fails a residual that is not a
  number.
- **The C step's representation**, in modelx, in seconds: `claims(t, ALL)` is the sum of
  its two kinds by its bits on every committed point's month, and `PA_UK_S`'s total by its
  bits on every twin's; every value each text column can hold decodes as `PA_UK_S` reads
  it, 23 cases, each sex of each life and a sex the table lacks among them; the padded
  mortality array holds NaN where no file does and nothing else, each sex has its own
  extents, on a table whose sexes start at different ages, and the one reader refuses an
  age below its sex's; each `Data` vector is the int64 or float64 the `Data` docstring's
  table states, and each parameterless cell returns a Python number; each label returns its
  column as read or refuses what is not its codes; `spec_sec.py`'s sizes and
  `sample_sec.py`'s recursion limit are what their comments derive, and the sample traces
  `sex` on a blank; `run_sec.py --cython` rebuilds exactly when a source is newer; a value
  the vectors cannot hold, a timing, a kind or a life no cell takes, a kind of each cell in
  the other's and a third life's month of death among them, is refused; each refusal moved
  off a chain computes its chain's value, by `float.hex`, at every key of every committed
  point; and C4's sweep and its `also` ask every cell that takes a code at every code it
  takes, on a row of each basis and each kind, and on a single life.
- **C2, the fingerprint**: every committed point computes what the model computed when
  its E step ended, every cell at every argument, frozen at the end of the module by
  `tools/gen_sec_fingerprint.py` before the C step changed anything.
- **Compiled**, the tests marked `cython`, which compile the model once a session into a
  temporary directory and run it in child processes: in
  `tests/test_compiled_conventions_uk.py`, C3, the typing guard, on the declarations, the
  spec and the generated C; C4 on the committed points; and the release. In this model's
  module, C4 on the splice grid under each of its sets of References, the RPI rows and the
  fixed point 2 under each RPI among them; on the variants no committed row holds, which C2
  cannot freeze; at the contract's longest covers at its largest limiting age, 116, issued
  now and 120 months on and in payment in their last month, the 1,392-month guarantee among
  them; at the frame's edge on the scenario basis, 1,392 months under a limiting age of
  117, past `omega_age_max`, issued 120 months on with value protection on the first death;
  where the cap binds, on S's point 8 from policy month 576 to 599; on every value a
  decoded column holds; and on keys written as floats, each row with the cells and codes no
  swept cell reads, and every row of each table counted as compared; the LPI rows under
  their own RPI, each ItemSpace made after its References are set; the labels; the
  refusals, message for message, the income, the payments to date at an anniversary and the
  three powers past the floats and on a base that is no number among them, the frame a
  month past its edge, each flag spelt as only `bool()` reads it, each code no cell takes
  inside the caches, the `IndexError`s past the caches and an `idx` past the table and of
  −1; each shape's deepest cold call on a 1 MiB thread and on the main thread; a Reference
  set late, which clears no cache; and `run_sec.py --cython`, which prints what modelx
  prints.

Memory is the module's other cost. A swept point holds its cached values and modelx's
record of what each read, and `PA_UK_S`'s survival check, which rebuilds survival as a
product over every month before each time point, holds about 110 MB of that record on a
point on the table basis. So the module's sweeps evaluate the check's residual at every
25th time point and the frame's close, the whole check running on each splice row as it is
scanned, released once read; the splice keeps two S points swept at a time. The default
run, as CI's `sec_uk` job runs it, without the compile tests, 469 tests, peaks at 2.7 GB of
memory, inside the 7 GB of the smallest CI runner, macOS's, and takes 381 s on the shared
4-CPU machine under a 1-minute load of 2 to 3, a minute past the five minutes
UKLIB-SEC-PLAN.md U6 budgets (measured at M12, after its second review; after its first,
452 tests in 354 s at 2.7 GB; at M11, 410 tests in 284 s at 2.9 GB). The C step's tests add
the minute: the cold calls at the contract's largest limiting age, the representation's,
the refusals moved by point, each held on every other point, and the reviews', each the
only check of what it holds, C4's codes on a row of each basis and kind among them, 10 s.
It took 295 s to 330 s at M11, as the machine's load varied, until the depth test's shapes
issued 120 months on, which run as deep as those issued now, moved to the full grid. The
largest part is the core's 44 splice cases, about 110 s, each scanned whole, and none is
cut: the core-reach test's predicates are coarser than the faults the cases are there for,
and the review found that cutting by them would lose `rpi_high-point2-d24` and
`rpi_low-point7-d25`, which catch a fixed escalation compounded at the RPI and the LPI's
floor dropped. Then the 121 domain cases, about 30 s, each on a model just read, every
accepted edge projected, and the cold calls, about 20 s, a read of the model afresh for
each of 39, which the depth test and the chain-text test share rather than make twice.

The compile tests run where modelx-cython and a C compiler are installed, in a bare
`pytest` too, and in the `cython_uk` job's `pension_annuity` shard. A bare `pytest` of the
module, the build and its thirteen compile tests among its 482, took 930 s here at a peak
of 4.3 GB, under a load of 3 to 3.5, where after the first review it took 870 s at 4.4 GB
under a load of 2, and the review measured 864 s and 4.5 GB under a load of 4 to 5: the
compile tests are about 550 s of it, the build's 100 among them, and the peak is the
splice's swept models still held as C4 sweeps its chunks. The shard, as the `cython_uk` job
runs it on the full grid, took 1,116 s here, 679 s of it C4 on the full splice grid, at a
peak of 3.2 GB, under a load of 3.5 to 4, where after the first review it took 986 s, 585 s
of it the splice, at 3.1 GB under a load of 2 to 3. C4 sweeps ten rows at a time, and the
contract's extremes and the frame's edge one at a time, since a sweep's record grows as the
square of the frame: all eighteen extremes in one read took the module past 6 GB, and the
kernel ended it. They are not cut by default. U6's five minutes budget the `sec_uk` legs,
which install no compiler and skip them, and the `cython_uk` legs run them alone. A cut to
the rows each set of References moves would drop the fixed point 2's rows under the two
RPIs, which the RPI moves not at all, about 5 s; the rest is the splice grid's branches the
committed points miss, the caches' ends, the variants C2 cannot freeze and the decoded
values, each the only compiled check of what it reaches.

```bash
python -m pytest tests/test_pension_annuity_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_pension_annuity_uk_sec.py -q   # the full grid
python -m pytest tests/test_model_conventions_uk.py -q -k PA_UK_SEC
UKLIB_CYTHON_SHARD=pension_annuity python -m pytest -m cython tests -q      # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #uklib-pension_annuity-r10
[R11]: #uklib-pension_annuity-r11
[REG-R22]: #uklib-reg-r22
[REG-R27]: #uklib-reg-r27
[std]: #uklib-std
<!-- END generated citation links -->
