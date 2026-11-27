# In-Force Implementation Notes

**Status:** Draft, 2026-11-23. `WP_UK_SEC` is [`WP_UK_S`](model.md) taught to project from
a valuation date. Besides policies issued at that date, it takes policies already in force
there, in any month of their policy year, and policies to be written in the ten years after
it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is
the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes. The suffix adds lifelib's letters to `S`: `E` for in force, as in `BasicTerm_SE`,
and `C` for the compiled form, as in `basiclife/BasicTerm_SC`: the model compiles under
modelx-cython, and runs in modelx as before (*The compiled model*, below).

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `WP_UK_S` on another time axis, and it reads `WP_UK_S`'s assumption tables in place,
> every assumption unchanged: the with-profits mechanics are sourced, and every rate is a
> **[std]** standardization. Bonus declarations, MVR scales and lapse experience are not
> published, and the mortality table is an ONS-shaped proxy, not a CMI table. A
> deterministic run understates the cost of guarantees, which is convex in the fund
> return. Replace the assumptions with licensed tables and company experience, and the
> run with a market-consistent stochastic one, before drawing any conclusion from the
> numbers.

## Run it

```bash
python products/with_profits/run_sec.py            # point 1: the worked example's bond, in force 60 months
python products/with_profits/run_sec.py 7          # point 7: the down-market bond issued at t = 0
python products/with_profits/run_sec.py --block    # every model point, summed row by row
python products/with_profits/run_sec.py --cython   # point 1, compiled
```

The first prints the first twelve rows of point 1's cash flows, which `WP_UK_S` projects as
its rows 60 to 71, with the policy counts behind them. Three lines to the same thing for
point 7:

```python
import modelx as mx
model = mx.read_model("products/with_profits/WP_UK_SEC")
model.Projection[6].result_cf()                 # idx 6 is point 7
```

`Projection` takes `idx`, a point's position in the table, from 0, as
`basiclife/BasicTerm_SC` does, where `WP_UK_S`'s takes its `point_id`: `Projection[6]` is
point 7, and `point_id()` gives the label. `result_cf()` has `WP_UK_S`'s columns —
`pols_if`, `asset_share`, `premiums`, `claims_death`, `claims_surrender`,
`claims_maturity`, `withdrawals`, `expenses`, `shareholder_transfers`, `smoothing_cost`
and `net_cf` — and `result_payout()` `WP_UK_S`'s payout machinery, each with one row per
month from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out the
counts behind them on the same rows: `pols_if`, `pols_new_biz`, then the month's deaths
and surrenders in processing order, and the survivors of the frame's last month.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[6]`, is not
enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector frees,
so the runner collects after each release. It freezes everything alive (`gc.freeze()`)
once the model and its table are read, and again once it has asked every point for its
frame, so that each collection scans only what the block has made since. It keeps the
block's sum as it goes, compensated as pandas sums a `groupby`, so that the block is, bit
for bit, the frames concatenated and summed by `t`. It leaves out `asset_share`, an amount
per policy, which no sum of the points makes a block's. Its projection years carry the
count of their first month and the flows of all twelve.

`--cython` runs the compiled model in place of modelx, building it first with the
library's own `build_sec_cy.py` where it finds no build, or one older than the model, the
sample, the spec or the tool (*The compiled model*, below), and `--build DIR` runs a build
made elsewhere; either prints what modelx prints. The tool goes with the library, into
lifelib and into a `lifelib.create()` copy, so `--cython` builds there as here.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection: the endowment's maturity, the bond's limiting age, or
  the month a withdrawal election exhausts the bond's units, whichever comes first.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. The contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1`, the lapse table's key and the guarantee dates',
  `age(t) = age_at_entry() + duration(t)`, the mortality table's, age nearest birthday, as
  in `WP_UK_S`; the declaration in the twelfth month of each policy year; the
  guarantee-imminent window; the single premium in the issue month; and the end of cover,
  `cover_end_mth()`, `12 × policy_term()` on the endowment and `12 × (omega_age −
  age_at_entry())` on the bond, `WP_UK_S`'s frame from issue but for the exhaustion.
  `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion as long as
  the frame; the closed form needs no such chain of calls.

Point 1 is the worked example's bond, in force 60 months. At `t = 0` it is in its sixth
policy year at attained age 60, and its frame has 720 rows, `t = 0 … 719`; `WP_UK_S`
projects the same months as its rows 60 to 779, opening its frame late, on an
anniversary, `proj_start() = 12 × duration_inforce()`. Point 19 is the down-market bond to
be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is on the books
from `t_entry() = 13`, rows 0 to 12 are zeros, and its frame has 280 rows, its units running
out at policy month 267.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the mortality table at the attained age; the lapse table by policy year; the declaration, in the twelfth month of each policy year; the guarantee dates and the twelve months before each; the single premium, in the issue month; the endowment's maturity and the bond's limiting age; the bonus rule's remaining term | expense inflation, `inflation_factor(t) = 1.03^(t // 12)` |

Expense inflation runs on `t`, stepping on each anniversary of the valuation date, for
every point alike (USLIB-SEC-PLAN.md D7; UKLIB-SEC-PLAN.md §9 item 4). The maintenance
charge is then in valuation-date pounds: `WP_UK_S` inflates from issue, so its bonds in
force carry five years of it in their first projected month and its endowment in force
twenty. The fund return and the bonus rate are levels of the model point, the same on
either clock, so nothing is re-based. WP has no acquisition expense and no commission.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in range(len(model.Data.point_id()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`WP_UK_S` computes: every cell the two models share agrees, but three whose meaning
changed, `pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, `model_point()`, a row of another table, and `fund_exhaust_mth()`, whose
"never" is no longer 0 (*Where the units run out*, below).

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `WP_UK_S`'s columns, one
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s name, a policy
clock column, three renamed to D6's vocabulary and two columns of state `WP_UK_S` lacks.
The count is the only weight on the flows, and every state column is per policy. Each is
measured at the valuation instant, the start of month 0, before any month-0 event, which
is `WP_UK_S`'s close of the month before (USLIB-SEC-PLAN.md D6). A declaration falls at the
end of a policy year's twelfth month, so on a point valued on an anniversary the
declaration that closed the year before is in the columns, and the first declaration the
projection makes is the one that closes the year under way. Each state column is history:
what the contract has accumulated, declared, charged or paid, never re-derived from a
Reference, which is an assumption from the valuation date on, so that a Reference changed
there reaches back over no month already run (UKLIB-SEC-PLAN.md K14, §9 item 5):

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `asset_share_init` | pounds per policy | the start of month 0 | the asset share, the retrospective accumulation, floored at 0 as `WP_UK_S` floors it: `WP_UK_S`'s `asset_share` of month −1 |
| `units_init` | units per policy | the start of month 0 | on the bond, the units held, which the premium bought and the withdrawals have cancelled; 0 on the endowment |
| `unit_price_init` | pounds per unit | the start of month 0 | on the bond, the with-profits unit price the declarations have raised the seed price to; on a policy not yet in force, the seed price its premium buys units at, an issue value |
| `attaching_bonus_init` | pounds per policy | the start of month 0 | on the endowment, the reversionary bonuses already added to the sum assured; 0 on the bond |
| `smoothed_payout_init` | pounds per policy | the start of month 0 | the smoothed payout the year-on-year cap works from; 0 where the asset share has floored at 0 |
| `bonus_rate_init` | a rate a year | the last declaration before the valuation date, at the end of policy month `12 × duration(0) − 1` | the bonus rate declared there: of every year with the bonus rule off, and with it on the rate the first declaration in the frame starts from; on a policy not yet in force, the rate its first declaration starts from |
| `guar_charge_cum_pp_init` | pounds per policy | the end of month −1 | the guarantee charges taken since issue, which the charge's lifetime cap of 2% of the asset share is measured against |
| `smoothing_account_init` | pounds per policy in force | the end of month −1 | the estate's smoothing and guarantee cost on the exits since issue, over the policies in force: of either sign |

`WP_UK_S` carries the first five in its own columns on its in-force rows, and holds no
column for the last two. It restarts both cumulants at 0 where its frame opens, so a bond
it reopens in force charges on where its own projection from issue has stopped: the
down-market bond issued at the valuation date, point 7, stops charging at month 88, and
reopened at 60 without its charges it would charge again, its asset share parting from
`WP_UK_S`'s from issue. Its twins of `WP_UK_S`'s own in-force rows carry 0 in both, which is
what `WP_UK_S` assumes there. Here:

- `asset_share(t)` opens at `asset_share_init()` at `t_entry()`, `units(t)` at
  `units_init()`, `unit_price(t)` at `unit_price_init()`, the endowment's guarantee at
  `sum_assured() + attaching_bonus_init()` and `smoothed_payout(t)` at
  `smoothed_payout_init()`, each the balance the month opens with;
- `guar_charge_cum_pp(t)` opens at `guar_charge_cum_pp_init()`, which the cap's test reads
  in month 0;
- `smoothing_account(t)` opens at `smoothing_account_init() × pols_if_init()`;
- `bonus_rate(t)` is `bonus_rate_init()` in every policy year with the rule off. With it
  on, every declaration in the frame is the rule's, at today's References, from this
  model's own asset share and guarantee: a declaration at or after the valuation date is
  the projection's own event (D6), and one at the end of month 0 is month 0's. The first
  starts from `bonus_rate_init()`, each later one from the rate declared a year before, and
  every month of a policy year reads its year's declaration.

No balance is needed at a second instant: a declaration costs the month's own opening
values, and no annual quantity reads the balance entering the policy year, so there is no
`_prev_anniv_init` column and no `_ytd_init`.

On a point issued at the valuation date each history column holds its issue value, and the
model is `WP_UK_S`. A model that dropped a column and rebuilt it from the References would
pass the splice wherever `WP_UK_S` and the splice rebuild it alike, so the tests write each
off its References' path and project through it.

| `WP_UK_S` | `WP_UK_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_inforce` (years) | `duration_mth` (months) | The policy clock, in months, any month of a policy year |
| `units`, `attaching_bonus`, `bonus_rate` | `units_init`, `attaching_bonus_init`, `bonus_rate_init` | D6's vocabulary: each is the value the projection opens with |
| — | `guar_charge_cum_pp_init`, `smoothing_account_init` | The cumulants `WP_UK_S` restarts at 0 where its frame opens |

The columns carried over are read as `WP_UK_S` reads them. For a policy in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `chassis`, `sex`, `tax_basis` | codes, as in `WP_UK_S`'s table | issue |
| `age_at_entry` | whole years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `premium_single`, `premium_regular`, `sum_assured` | pounds, the amounts at issue | issue |
| `policy_term` | whole years | issue: 0 on the whole-of-life bond |
| `guarantee_dates` | policy anniversaries, `;`-separated | issue: blank on the endowment |
| `wd_rate`, `fund_return` | rates a year | the withdrawal election and the scenario's level |
| `asset_share_init`, `unit_price_init`, `smoothed_payout_init` | as above | `WP_UK_S`'s columns of these names, measured at the valuation instant |

Four more columns, `row_kind`, `source_policy_id`, `source_mth` and `source_refs`, record
where the generator took each shipped row from (below): `source_refs` names the References
a row was read from `WP_UK_S` under, `guar_charge_rate_base 0.002` on points 20 and 21,
`bonus_rule_on True` on 22 and 23 and `smooth_cap 0.05` on 24, and is blank on every row
read at those `WP_UK_S` ships. No formula reads them, and an in-force extract need not
carry them: without them the model projects the same numbers, and `run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it: the ten in-force columns are present; no `point_id` appears twice;
`policy_count` is a number, zero or more; `duration_mth` is a whole number of months,
below `2**53`, and −120 or more, future new business being written over a horizon,
`Data.future_horizon_mth`, 120 months as shipped, itself a whole number of months below
`2**53`, which set to 0 refuses future new business altogether; each code is one
`WP_UK_S` knows, the chassis `UWP_bond` or `CWP_endowment`, the sex `M` or `F` and the tax
basis `life_net` or `pension_gross`; the age and the term are whole numbers, the amounts
zero or more, the withdrawal rate from 0 to 1 and the fund return a finite number above
−1, where the monthly return has a real value; the guarantee dates are blank or whole
anniversaries, 1 or more, and blank on the endowment, which has none; the endowment has a
term of a year or more and no units, the bond no term and no attaching bonus. Then the
opening state: the asset share, the units, the attaching bonus, the payout and the
guarantee charges are amounts, zero or more; the unit price a finite number above 0; the
bonus rate a finite number, zero or more, a declared bonus being floored at 0 by the
contract; and the smoothing account a finite number of either sign. A point not yet in
force holds no opening state, its seed price and its first year's bonus rate excepted,
which are issue values; a bond in force holds units, a bond whose units are spent being
encashed; a point in force with an asset share above a cent has a payout above 0, to the
cent, since the smoothing cap is skipped only from a payout of 0, which `WP_UK_S` holds only
beside an asset share of 0, so that an extract carrying £0.006 and its payout of £0.0048
to the cent, 0.01 beside 0.00, reads; and an endowment in force 11 months or fewer has no
attaching bonus, to the cent, its first declaration falling at the end of policy month 11.
Each holds of every
state `WP_UK_S` reaches, as shipped and under the splice's References, which a test
asserts. `WP_UK_S` meets most of these only when a projection reaches them, and some
never: a guarantee date on the endowment would gate an exercise and the imminent window
there, and a fraction of a year in the age would be truncated by `int()`.

A point at or past the end of cover at the valuation date,
`duration_mth ≥ cover_end_mth()`, reads, but `proj_len()` refuses it, naming the point:
the end of cover is the product's rule, keyed on the policy clock, not the table's. So
does a point the contract does not write ([`product-spec.md`](product-spec.md)): one
issued below 18, `Projection.issue_age_min`, the youngest age the mortality table rates,
though the bond admits issue from 3 months; a bond issued at or past the limiting age,
`omega_age`; and an endowment maturing past it,
`age_at_entry() + policy_term() > omega_age`, whose last attained ages the table may not
rate, where `WP_UK_S` bounds no term and reads them at `omega_age`. `omega_age` itself
must lie above `issue_age_min` and at most a year past the mortality table's last age.
Each is a lower-case Reference. The compiled model's caches are sized from the shipped
References and table: a cover of at most 1,236 months, from issue at 18 to 121, the
table's last age plus one, and a frame of at most 1,356 months, that cover issued 120
months after the valuation date. So `proj_len()` refuses a point whose cover or frame is
longer, naming it, in modelx as compiled, and each Reference keeps its domain (*The bounds
the caches hold*, below). A whole limiting age written as a float, `120.0`, is read as the
`int` it is, so that the frame is a whole number of months, as it is compiled. And
`proj_len()` refuses a bond whose units run out in its first month on the books, which
would leave no month to project. On every point `proj_len()` also refuses a Reference off
its domain (below). A loop over the block meets such a row only when it reaches it, so
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

The assumption tables are checked before a value of them is read, each by the cell the
projection takes its extent from, reading the file as it stands, so that a fault is named
by its line. The mortality table is checked by `Data.mort_age_first`: each age a whole
number, each sex `M` or `F`, each running from the table's first age to its last, one row
an age, none below 0, and each rate from 0 to 1. The lapse table is checked by
`Data.lapse_last_year`: policy years from 1 without a gap or a repeat on each chassis, each
chassis `UWP_bond` or `CWP_endowment`, each rate from 0 to 1. A key is read by its value,
so an age written `70.0` is 70. Each refusal names the file, the column and its lines. An
attained age outside the mortality table, which only a lowered `issue_age_min` admits, is
refused by `mort_rate`, naming the point and the age, where `WP_UK_S`'s lookup raised
`KeyError`.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`WP_UK_S` and its table by `tests/uk_sec_support.py`, from the `WP_UK_SEC` entry in its
`SEC_SPECS`, and the tests regenerate it and compare, so an edit to a `WP_UK_S` row reaches
it or fails the suite. In the source repository, `python tools/gen_sec_points.py WP_UK_SEC`
writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 to 4, 6 | twin | S points 1 to 4 and 6 | in force, as `WP_UK_S` opens them: the worked example's bond at +7% and −15%, on a 5% return, with the 5% withdrawal election, all in force 60 months; and the endowment, in force 240 months on a gross pension basis |
| 5, 7 | twin | S points 5 and 7 | issued at `t = 0`: the endowment, and the down scenario's bond with the withdrawal election, the one bond `WP_UK_S` issues at the valuation date |
| 8 | derived | S point 1 at S month 71 | the bond in its sixth year's last month, the declaration at the end of month 0 |
| 9 | derived | S point 2 at S month 68 | the down scenario as its market value reduction turns on, the smoothing cap's floor binding |
| 10 | derived | S point 2 at S month 92 | the down scenario as the corridor's ceiling binds |
| 11 | derived | S point 2 at S month 119 | the down scenario on its guarantee date, the MVR-free encashment in month 0 |
| 12 | derived | S point 2 at S month 242 | the down scenario with its asset share floored at 0, and its payout 0 with it |
| 13 | derived | S point 3 at S month 487 | the 5% bond in a month its charge cap binds |
| 14 | derived | S point 4 at S month 402 | the withdrawing bond in its last month, 99.10 units left: a one-row frame, ended by forced encashment |
| 15 | derived | S point 5 at S month 11 | the endowment at its first declaration, no bonus yet attaching |
| 16 | derived | S point 5 at S month 299 | the endowment's last month: a one-row frame, maturing |
| 17 | derived | S point 1 at S month 779 | the bond in its last month before the limiting age: a one-row frame, paying nothing |
| 18 | derived | S point 7 at S month 100 | the down-market bond past its charge cap, its charges stopped at 88 |
| 19 | future | S point 7, 13 months on | to be issued at `t = 13` |
| 20 | derived | S point 7 at S month 60, `WP_UK_S` run under a guarantee charge of 0.2% | its charges taken at twice today's rate, 147.88, where today's would have taken 74.05 |
| 21 | derived | S point 3 at S month 300, under a guarantee charge of 0.2% | the 5% bond past its charge cap from 207, where today's rate caps it from 487 |
| 22 | derived | S point 1 at S month 150, under the bonus rule | a unit price of 1.486230 and a rate last declared of 5.66%, at its month 143, where rates held level give 1.268242 and 2% |
| 23 | derived | S point 5 at S month 150, under the bonus rule | the endowment with 2,091.61 of bonus attaching and a rate last declared of 0.62%, at its month 143 |
| 24 | derived | S point 1 at S month 156, under a smoothing cap of 5% | the payout held to 43,584.94 below an asset share of 46,540.48, its smoothing account below 0 |

A derived row's `policy_count` is the count `WP_UK_S` carries into that month, its
`pols_if(d)`, and its state what S carries there, so the row continues the S projection from
there. At the shipped References no state carries a cumulant or a history that today's
References would not rebuild, so five rows are read from `WP_UK_S` run under References of
their own, which the spec's `derived_refs` records: points 20 to 24. At the shipped
References the committed model projects each from that history at today's, and a test
asserts that each continues `WP_UK_S` under its own References with them set in both. A
derived row's `policy_id` is the S row's with the month appended, `WP-000002-M119`, and a
future row's carries the months to issue, `WP-000007-F13`. Row `t` of a generated point is
month `t + source_mth` of its S point.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` keeps
`WP_UK_S`'s three timings, as codes (*The compiled model*, below), and adds
`basiclife/BasicTerm_SE`'s `BEF_NB`:

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1`'s deaths and surrenders after it, and 0 outside the frame;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, which
  `pols_if(t)` returns;
- `BEF_SURR`, after the month's deaths, before its surrenders;
- `AFT_DECR`, the end of the month, which is `BEF_NB` at `t + 1` exactly, and 0 in
  the frame's last month, where the survivors leave as `pols_maturity(t)`.

Any other timing raises. The survivors of the frame's last month are paid `G + TB` on the
endowment's maturity and `FV + FB` on the bond's forced encashment, and nothing at the
bond's limiting age. The roll-forward closes as

```
pols_if(t) − pols_if(t + 1) + pols_new_biz(t + 1)
    = pols_death(t) + pols_surr(t) + pols_maturity(t)
```

at every `t` of every frame, and its check scales its tolerance with `policy_count()`,
where `WP_UK_S` scales with `pols_if_init()`, which here is 0 on new business.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < cover_end_mth()`, and outside it, before
issue and from the end of cover on, every count is zero, and so every cash flow; so is
every balance, every rate read at a policy year or an age, and every flag false. Between a
bond's exhaustion and its limiting age it is in cover, holding no count, its frame having
ended.

## Each chain one cell a month within its policy year

Four chains carry the state forward, coupled: the count; the asset share; the smoothed
payout, which reads the asset share and feeds the withdrawal's share of it back through
`wd_as_pp` and `policy_value_open`; and the endowment's guarantee. `WP_UK_S` runs the
asset share through seven cells a month, its `asset_share_at` timings, the payout through
three and the guarantee through two: a cold read of `asset_share(779)` on the worked
example's bond runs 5,042 cells deep. Here each is written in the cell that carries it,
reading that chain's own month before first and the month's other cells after:
`asset_share(t)` writes the month's premium and withdrawal, return, charges, shareholder
transfer, mortality charge and estate distribution inline, in `asset_share_at`'s order and
its floats, `smoothed_payout(t)` the cap and the corridor, the endowment's
`guar_benefit_pp(t)` the declaration, and `pols_if_at(t, BEF_NB)` the month before's
deaths and surrenders, so that each chain from month `t` back to `t_entry()` is one cell a
month, whichever chain a call meets first (USLIB-SEC-PLAN.md D5). `asset_share_at` and
`smoothed_payout_capped` read them, a step at a time, as `WP_UK_S`'s do, and a test holds
each inline cell to them, bit for bit. The units, the unit price and the two cumulants were
one cell a month already.

One cell a month, the eight chains, the four above and the units, the unit price and the
two cumulants, ran the whole cover on a cold call, 1,236 cells at the contract's longest,
which the compiled model runs on the C stack, past what the C step allows (*What a compiled
run needs*, below). So each is blocked by policy year, as `ULB_UK_SEC`'s fund and
`WOL_UK_SEC`'s counts are: in a year's first month after `t_entry()` a chain reads the
year's opening, `pols_if_py(y)`, `asset_share_py(y)`, `smoothed_payout_py(y)`,
`guar_benefit_pp_py(y)`, `units_py(y)`, `unit_price_py(y)`, `guar_charge_cum_pp_py(y)` or
`smoothing_account_py(y)`, which walks the year before in ascending order, asking the
monthly cell of each month, and returns the value its last month closes on, bit for bit;
a test holds each opening to the month before's close, and each chain's precedents in
modelx's graph to its opening there and to its month before elsewhere.

Called cold on a model just read, at the contract's longest cover, 1,236 months from issue
age 18 to the largest limiting age, 121, on the bond, on an endowment maturing there and on
a bond withdrawing 1% a year, whose exhaustion search runs its chains first, each chain
runs one cell a month within its policy year and two cells a year before it, back to
`t_entry()`, 215 cells, and a few more, measured with the bonus rule and the estate
distribution on, on a point issued now and one issued 120 months on alike, each head's own
overhead, at most over the shapes: the asset share 8; the payout and the asset share's
residual 9; the guarantee charges and the smoothing account 12; the count 13 and its
residual 16; the units 20; the guarantee and the unit price 22; the claims total 24; and a
cold `net_cf` 25, on the endowment, whose first month's declaration discounts its bonus
cost at the foot of the chain. The rule's own chain, `bonus_rate` through each year's
declaration, is one cell a year and 20 more.

## Where the units run out

A level withdrawal election runs a bond's units down, and against a fund whose growth is
only the declared bonus it cancels the last of them. `fund_exhaust_mth()` finds the month,
as a policy month: the first whose closing units are at or below `1e-9`, `WP_UK_S`'s test,
the month the withdrawal, capped at the unit fund, takes the last of it. The frame ends
the month before, and its survivors are paid `FV + FB` there, a forced encashment. The
search is one loop over the units' own months, from `t_entry()` to the end of cover,
ascending, so that each month's units are read once the month before's are known: the far
read R2 admits, as uslib's `DIA_US_SEC` reads its survival to its payout date and
`ULB_UK_SEC` its fund to exhaustion. It starts at `t_entry()`, because a bond issued later
holds no units before its issue month, which a search from 0 would read as exhausted at
once, and it reads the units of the month they run out, the month after the frame's last.

`WP_UK_S`'s "never" was 0, safe there because its month 0 is a bond's issue month, which
the single premium funds. On the valuation clock month 0 is any month of a bond's life,
the one its last units are withdrawn in among them, and a policy month of 0 is the issue
month, so here "never" is a month past cover, `cover_end_mth() + 1`. A bond whose units
run out in its first month on the books has no month to project, and `proj_len()` refuses
it. The search reads the units' chain, and through the bonus rule the asset share's, so
nothing they read may read the frame: `is_active(t)` reads the end of cover alone.

## Departures from WP_UK_S

Each formula that tested `t` against a contractual event now tests the policy clock, and
each recursion opens at `t_entry()` from the opening state. Where `WP_UK_S`'s test would
have stayed correct on the valuation clock, it moved anyway, so that cover has one
definition. Fifteen cells are new — `policy_count`, `duration_mth_init`, `t_entry`,
`is_active`, `cover_end_mth`, `pols_new_biz`, `result_pols`, the accessors of the three
columns renamed and of the two cumulants, and the refusal cells of five chains — and three
of `WP_UK_S`'s are gone, `proj_start` and `duration_inforce`, which the valuation clock
replaces, and `attaching_bonus`, renamed. One Reference is new, `issue_age_min`.

| Cells | `WP_UK_S` | `WP_UK_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration`, `age`, `policy_year` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len`; `cover_end_mth`, new | `12 × policy_term()`, or `min(12 × (omega_age − x), fund_exhaust_mth())`, from issue | `min(cover_end_mth(), fund_exhaust_mth()) − duration_mth_init()`, from the valuation date; raises past cover, outside the contract's bounds, on a Reference off its domain, on units spent in the first month and on a cover or a frame longer than the compiled model's caches are sized for | The frame starts at the valuation date |
| `fund_exhaust_mth` | the first `t` from `proj_start()` whose units are at or below 1e-9, 0 if none | the same as a policy month, from `t_entry()` to month 1,356 at most; `cover_end_mth() + 1` if none | 0 is a real month on either clock; no frame the compiled model's caches hold ends later |
| `is_forced_encashment` | `fund_exhaust_mth() > 0` and the frame ends there | `fund_exhaust_mth()` inside cover | The new "never" |
| `is_declaration_month`, `declaration_month` | `(t + 1) % 12 == 0`; the policy month `12 × duration(t) + 11` | `(duration_mth(t) + 1) % 12 == 0`; the valuation month `t + 11 − duration_mth(t) % 12`, `WholeLife_US_SEC`'s `anniv_mth` | A declaration falls in a policy year's twelfth month, and `bonus_rate` passed the policy month back as `t` |
| `guarantee_imminent` | `0 < 12g − 1 − t ≤ 12` | `0 < 12g − 1 − duration_mth(t) ≤ 12` | A guarantee date is a policy anniversary |
| `premium_pp` | the single premium at `t == 0` | at `duration_mth(t) == 0` | On the valuation clock every bond in force would pay its single premium again |
| `asset_share`, `asset_share_at` | seven cells a month from `asset_share_init()` at `proj_start()` | inline, one cell a month, from `asset_share_init()` at `t_entry()`; a balance past the floats refused before its floor | D5's one cell a month; the floor would read `−inf` or NaN as an exhausted share |
| `smoothed_payout`, `smoothed_payout_open` | three cells a month from the column at `proj_start()` | inline, one cell a month, from the column at `t_entry()` | D5 |
| `guar_benefit_pp`, `guar_benefit_open` | the endowment's guarantee two cells a month | inline, one cell a month; a guarantee past the floats refused | D5 |
| `units`, `unit_price` | from the columns at `proj_start()` | from the columns at `t_entry()`; past the floats refused | The opening state |
| `guar_charge_cum_pp`, `guar_charge_rate` | from 0 at `proj_start()` | from `guar_charge_cum_pp_init()` at `t_entry()` | A cumulant `WP_UK_S` restarts at 0 |
| `smoothing_account` | from 0 at `proj_start()` | from `smoothing_account_init() × pols_if_init()`; 0 outside the frame | A cumulant `WP_UK_S` restarts at 0 |
| `bonus_rate` | the column, or with the rule on its column through its first projected year and the rule from its second, each month reading its year's declaration, past the frame where a forced encashment ends it mid-year | the column, or with the rule on the rule at every declaration in the frame, the first from `bonus_rate_init()`, each month reading its year's declaration where the frame reaches it, and the year before's rate where it does not | D6: a declaration at or after the valuation date is made at today's References, so under the rule `WP_UK_S`'s points in force, its new business and a point valued inside its first projected year part from it at their first declaration in the frame, where it keeps its column; and R2's read bounded by the frame, which changes the `bonus_rate` column of `result_payout` in a cut year alone |
| `bonus_supportable` | the growth to the horizon unchecked | refused past the largest float and, from a return net of charges below 0, below the smallest, where a horizon of 4,500 years would read as no asset share at all | An underflowed factor declared 0.5% where 4,000 years declares 0 |
| `pols_if`, `pols_if_at`, `pols_if_init` | `pols_if` a recursion of its own, three cells a month, from the column's 1.0 at `proj_start()` | `pols_if` is `BEF_DECR`, the `BEF_NB` chain plus the month's new business, one cell a month within a policy year from `t_entry()`; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `inflation_factor` | `1.03^duration(t)`, from issue | `1.03^(t // 12)`, from the valuation date | Unit costs in valuation-date pounds |
| `mort_rate`, `surr_rate_base`, `surr_rate`, `premium_pp`, `wd_pp`, the balances, the counts | no `WP_UK_S` frame has a month before issue | zero outside cover, before any table or rate is read; an age past the table refused by name; the lapse table's extent from `Data` | Before issue `WP_UK_S` reads the tables at ages and policy years the policy never has |
| `cost_of_bonus_pp`, the flows, `net_cf` | unchecked | a value past the floats refused in its month | From inputs each in its domain, a bonus rate past every amount of money made the cost, and so the asset share, infinite with every check passing |
| `inflation_factor`, `bonus_supportable`, `cost_of_bonus_pp`'s discount | Python's `OverflowError`, naming nothing | a power past the floats refused, naming the point and the References | `PA_UK_SEC`'s form (*Record — M11*) |
| `check_pols_roll_fwd_resid`, `check_pols_roll_fwd` | `pols_if(t + 1)`; tolerance `1e-10 × max(pols_if_init(), 1)` | adds `pols_new_biz(t + 1)`; tolerance `1e-10 × max(policy_count(), 1)` | The next month's new business is no part of month `t`'s movement, and `pols_if_init` is 0 on new business here |
| `check_declaration_is_annual` | the months of S's frame | the months on the books, from `t_entry()` | Before issue a policy holds no price to move |
| `result_cf`, `result_payout` | `range(proj_start(), proj_len())` | `range(proj_len())`, from the valuation date | Row 0 is the valuation month |
| `result_pols`, new | — | the counts behind `result_cf()` | After `basiclife/BasicTerm_SE`'s `result_pols()` |

Of the cash flows, the change of clock moves the maintenance expense alone at the shipped
assumptions, and `net_cf` with it. The twins of `WP_UK_S`'s bonds in force carry that
expense in valuation-date pounds, so their `expenses(t)` is `WP_UK_S`'s `expenses(60 + t)`
divided by `1.03^5`; every other column is `WP_UK_S`'s from month 60 on. The endowment in
force divides by `1.03^20`.

**The caps, as `WP_UK_S` has them since UKLIB-SEC-PLAN.md's M0.** `mort_rate` caps the
annual mortality rate at 1, written `min(q, 1.0)`, the product first and the bound second,
so that a NaN stays NaN where `min(1.0, q)` would read it as certain death; wherever `q` is
a number the two are the same float. The table reaches 1 at male age 113 and female 118,
so at the shipped factor of 0.6 the cap never binds, and its test takes a factor above 1.
The surrender rates keep `WP_UK_S`'s order, `min(1.0, w)`: they are no cap on a mortality
rate, and the multipliers that feed them are held to domains no NaN is in.

**Domains `WP_UK_S` leaves unchecked.** `WP_UK_S` raises a Reference to a power, bounds a
rate or a balance with it, or reads it as a share, a factor or an amount, and checks none.
Off its domain it projects a negative rate or charge, or a NaN that a `min` or a `max`
loses: a NaN smoothing cap or corridor is lost through the clamps, which then read the
corridor's ceiling; a NaN deterrent or exercise rate reads as certain surrender through
`min(1.0, ...)`; a NaN estate distribution is lost in the asset share's floor; and a NaN
charge cap switches the cap off. Here `proj_len()` refuses each Reference off its domain,
naming the point, the Reference, the domain and the value, on every point, as a model-wide
assumption:

| Reference | Domain | Off it |
|---|---|---|
| `issue_age_min`, `omega_age` | a whole number below `2**53`; the first 0 or more, the second above the first and at most a year past the mortality table's last age | a NaN bound refuses nothing and an infinite one bounds nothing |
| `mort_be_factor`, `misc_surplus_rate`, `death_benefit_factor`, `mvr_deterrent_factor`, `guarantee_imminent_factor`, `guar_fill_target`, `bonus_change_cap`, `expense_maint` | a finite number, 0 or more | a negative rate, charge, uplift or expense; a NaN lost in a `min` or a `max` |
| `amc_rate`, `guar_charge_rate_base`, `guar_charge_cap`, `prem_alloc_rate`, `smooth_cap`, `corridor_lo`, `bonus_speed`, `guarantee_exercise_rate` | a number from 0 to 1 | past 1 a monthly rate `1 − (1 − c)^(1/12)` has no real value, or a share is more than the whole |
| `amc_rate` and `guar_charge_rate_base` together | their monthly rates summing to 1 or less | the charges' factor on the balance, `1 − c_amc_m − c_g_m`, turns negative |
| `corridor_hi` | a finite number, 1 or more | the corridor must include 100% of the asset share |
| `shareholder_transfer_divisor` | a finite number above 0 | the cost of bonus is divided by it |
| `surr_disc_rate` | a finite number above −1 | the endowment's bonus cost is discounted at `(1 + i)^years` |
| `bonus_rule_on` | True or False | the switch |
| `bonus_horizon` | a whole number of years, 1 or more, below `2**53` | the rule divides by it |
| `inflation_rate` | a finite number, −1 or more | the inflation factor changes sign each year |

Each domain is a comparison no NaN passes, a finite one bounded by the largest float, and
a whole number one of which `x == x // 1` holds below `2**53`, which an infinity fails, and
each Reference is printed as the compiled model types it, the three integers through
`int()` once whole and every other through `float()`. `Data.future_horizon_mth` is held to
a whole number of months, 0 or more, below `2**53`, by `Data` itself, as it reads the
table, and printed as a float.

**Values past the floats, refused in their cell.** From an opening state and References
each in its domain, a return can take the asset share past the largest float, a bonus
rate the unit price, the guarantee or the cost of bonus, a premium at a tiny price the
units, a long run the two cumulants, a count any flow, and the flows' sum the net cash
flow, where `WP_UK_S` would floor an infinite or NaN asset share at 0 and read it as
exhausted, every check passing. Here each value is refused with `ValueError` in the cell
and the month where it first leaves the floats, naming the point, the month and what
makes it: the premium, the guarantee the books open with, the asset share and the parts
of its month a Reference multiplies, the withdrawal's share of it, the estate
distribution and the shareholder transfer, the units, the unit price, the guarantee, the
death uplift and the death claim, the cost of bonus, the two cumulants, each flow, the
claims of each kind and their total, and the net cash flow. Each chain's refusal is
formatted in a cell of its own, `asset_share_refusal`, `units_refusal`,
`unit_price_refusal`, `guar_benefit_refusal`, `guar_charge_cum_refusal` and
`smoothing_account_refusal`, which the chain calls only on its error path, so that no
frame a chain holds formats a message (UKLIB-SEC-PLAN.md §6.6, *Record — M10*); each
returns its chain's value, under its chain's guards, wherever it is called.

A power is refused the same way. modelx runs a formula as Python does, and Python's float
`**` raises `OverflowError`, naming neither the point nor the Reference, where its result
would pass the largest float, and C's `pow` gives an infinity there. So the inflation
factor, the bonus rule's growth to its horizon and the endowment's discount on its bonus
cost each catch the one and test for the other, and raise `ValueError` naming the point
and the References, `PA_UK_SEC`'s form (*Record — M11*); the discount is refused below the
smallest float too, since the cost divides by it. The bonus rule's growth factor is
refused below the smallest float as well, since a long horizon decays a negative net return
to 0.0 and the rule would read no asset share. Compiled, C's `pow` gives an infinity where
Python's raises, so each calls Python's own power where its result is infinite from a
finite base, inside the same `try`, uslib's M22 form, and the compiled model raises the
same message (*The compiled model*, below).

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC`
does, and modelx reads and runs the same formulas as before. Compiling changed how each
cell reads its inputs and spells its codes, and how its eight chains reach back in time,
and no number: what its reports computed on each committed point was frozen before the
change, and they still compute it, to 1e-12 of each column's largest value (*Tests*,
below), and every value the in-force model cached was this one's, bit for bit, when the
change was made: 825,438 on the committed points, and 6,227,401 on the 175 points of the
full splice grid under its three sets of References. Cell by cell, at every argument a
full modelx sweep evaluates, the compiled model computes what modelx computes, bit for
bit, on the committed points, on the points of the splice grid, which take the branches
they do not, at the contract's longest covers, where the cap on mortality and the
surrender rate's bound bind, on every value a decoded column holds, on keys written as
floats, on the committed rows under the References they were read from, on the rule's
declarations in the frame and on the bonds whose units run out. The compile tests hold it
so on x86-64, and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

The library carries the tool at its root, so a model builds wherever the library is: in the
source repository, in lifelib or in a `lifelib.create()` copy. From the library's folder:

```bash
python build_sec_cy.py with_profits                  # in place, beside the model
python build_sec_cy.py with_profits --out /tmp/wp    # elsewhere, with the CSVs
```

The tool exports the model to `WP_UK_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `WP_UK_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/with_profits")     # the directory holding the build
from WP_UK_SEC_nomx_cy import mx_model as model
model.Projection[6].result_cf()                 # point 7, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So a Reference set on `Projection` after it has computed,
`inflation_rate` say, leaves every value computed before as it was, in the base
`Projection` and in every ItemSpace made before, and only an ItemSpace made afterwards
computes with it. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about two minutes with gcc, 113 to 131 s here, and needs modelx-cython, which
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
taught first (USLIB-SEC-PLAN.md R1 to R17), and `Term_UK_SEC`, `CI_UK_SEC`, `ULB_UK_SEC`
and `WOL_UK_SEC` here:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[6]` is point 7, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `sum_assured()` is `float(data.sum_assured()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The eight columns of opening state are
  vectors too.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula reads into the number it selects, for every point at once: the chassis into its
  code, `chassis_code`, `UWP_bond` 0 and `CWP_endowment` 1, a code rather than what it
  selects, because the rules of a chassis are `Projection`'s formulas and References,
  which `Data` cannot read, and the chassis's row of the lapse table; and the sex into the
  point's row of the mortality table, `mort_schedule`, M 0 and F 1. The tax basis is read
  by no formula, the fund return being supplied on it, and stays a label. Each decodes as
  `WP_UK_S` reads the column, which a test holds on every value a column can hold, and
  what it cannot hold it refuses (below).
- **The guarantee dates, a flag by policy year.** `WP_UK_S` parses the column, the text of
  one policy anniversary or a `;` list of them, into a tuple of years, `guarantee_years()`,
  each time a month asks, and tests a year's membership of it, in `is_guarantee_date` and
  in `guarantee_imminent`'s generator over the tuple. A tuple and a generator are Python
  objects, so `Data` decodes the column once into `guarantee_flags`, int64 by point and
  policy year, 1 where the anniversary closing that year is a guarantee date, as wide as
  every year a frame can read, `Data.guarantee_year_last()`, the mortality table's last
  age plus 2; and `is_guarantee_year(y)`, the one cell that reads it, is `y in
  guarantee_years()`. `guarantee_imminent(t)`'s window, the twelve months before a date,
  is the one year whose date is 1 to 12 months ahead, `(duration_mth(t) + 13) // 12`, a
  closed form where `WP_UK_S` tries every date. The check of the column and its decode read
  each part alike, stripped and read by its value, a blank part skipped, so that ` 10`,
  `10 `, `10` and `10.0` name year 10 in both, which a test holds against `WP_UK_S`.
- **Tables indexed by integers.** The mortality table is `mort_table_array`, by schedule
  and attained age, padded from age 0 so that the index is the age; the lapse rates are
  `lapse_table_array`, by the chassis's code and policy year, padded at year 0, beside
  each chassis's last year, `Data.lapse_last_year`, an int64 vector of two, which
  `Projection`'s `lapse_last_year()` reads at the point's chassis. The padding holds NaN,
  and nothing reads it: `mort_rate` reads the attained age in cover alone, which
  `proj_len()` holds to the table's ages, and `surr_rate_base` holds the policy year at
  the chassis's last above, as `WP_UK_S`'s `tbl.index.max()` on the chassis's rows does.
- **Codes.** A timing or a kind, which `WP_UK_S` spells as text, is an int Reference named
  as the text: the count's timings `BEF_NB = 0` to `AFT_DECR = 3`, in the order of their
  instants within the month, and the asset share's `BEF_PREM = 4` to `AFT_MC = 9`, in
  its order, one numbering for the two families, so that both fit one width of ten; and
  the claims' kinds `DEATH = 0`, `SURRENDER = 1`, `GUARANTEE = 2` and `MATURITY = 3`, and
  `ALL = 4`, the total. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`.
  A string argument would give the cell a dictionary for a cache, where a code indexes a C
  array, so codes are numbered from 0 without a gap; a code inside the width that a cell
  does not take, another family's timing, a payout's `ALL` or the claims' `GUARANTEE`, it
  refuses, `invalid timing` or `invalid kind`.
- **The claims total, a code of its own, compensated.** `WP_UK_S` totals the three kinds
  as `claims(t)`, its `kind` defaulted to `None`, with Python's `sum` over a generator. A
  default compiles as a keyword parameter the typing guard refuses, `None` is no C integer
  and a generator is a Python object, so the total is `claims(t, ALL)`, which `net_cf`
  reads. The deaths, the surrenders and the maturity are non-zero together in a frame's
  last month, and `sum` compensates since Python 3.12, so a total written left to right
  could part from it in the last bit: the total is `sum`'s Neumaier summation written out,
  as `CI_UK_SEC`'s is, each kind's rounding error carried and added back where it is a
  finite number. A test counts the kinds non-zero together in every month of every
  committed point, three in seven months, each a frame's last, and holds the total to
  `WP_UK_S`'s by its bits on every twin and to `sum` of the row's own kinds on every
  committed point; there a total left to right never parts, the maturity outweighing the
  rest, so the test reads rows whose three kinds are of a size too, a lapse table of 99%
  and a heavier mortality, where one left to right parts in 7 to 11 rows of 60, and
  where a total past the largest float, each kind finite, is refused as `inf`, the carried
  error, a NaN, left out. On Python 3.11, whose `sum` adds left to right, `WP_UK_S`'s
  total and `sum` part from this one where the three kinds are of a size, so the test
  holds the rest there and skips the bits, naming Python 3.11.
- **Eight chains blocked by policy year.** The count carried in, `pols_if_at(t, BEF_NB)`,
  the asset share, the smoothed payout, the endowment's guarantee, the bond's units and
  unit price, and the two cumulants each run one cell a month within a policy year, as at
  the in-force step, and in a year's first month after `t_entry()` read the year's
  opening, `pols_if_py(y)`, `asset_share_py(y)`, `smoothed_payout_py(y)`,
  `guar_benefit_pp_py(y)`, `units_py(y)`, `unit_price_py(y)`, `guar_charge_cum_pp_py(y)`
  and `smoothing_account_py(y)`, as `ULB_UK_SEC`'s and `WOL_UK_SEC`'s do. Each opening
  walks the year before in ascending order, asking the monthly cell of each of its months,
  so that each finds the month before cached, and returns the value carried out of the
  year's last month, the count's survivors formed as `BEF_NB` forms them within a year and
  each other the monthly cell's own float, so no number moves. A cold read then runs one
  cell a month back to its year's first month and two cells a year before that, where one
  cell a month ran the whole cover on the C stack (*What a compiled run needs*, below). The
  bonus rate's rule already ran a cell a year. The exhaustion search stays one loop, over
  the units' months ascending, so that it reads each month's units, and through the rule
  the asset share, once the month before's are known.
- **No refusal formatted on a chain.** A compiled cell's C frame holds the code that
  formats each of its messages, whether a run reaches it or not, and a chain holds a frame
  of each cell it recurses through at each level: on CI's Ubuntu runner, a refusal
  formatted in `Term_UK_SEC`'s recursive waiver cell had its cold call need 512 KiB to 1
  MiB, and 256 to 384 KiB without it (UKLIB-SEC-PLAN.md K12). So the six chains whose
  value can leave the floats format nothing: where it has, `asset_share`, `unit_price`,
  `units`, `guar_benefit_pp`, `guar_charge_cum_pp` and `smoothing_account` each call a
  refusal cell of their own, `asset_share_refusal(t)` and its kind, which computes the
  value again from the same cells, the same float, branch by branch, the year's opening
  among them, and raises the chain's message, naming the month and what makes it. Each
  takes the month alone, since a float parameter would give it a dictionary for a cache,
  and returns the value where it is finite, which the sample asks for to type it. A test
  holds every cell that a cold call's deepest path holds more than once to building no
  text and raising only a constant, and another holds each refusal cell to its chain, bit
  for bit, in every month of every committed point. The count and the payout refuse
  nothing a value makes, and the flows' refusals stay in their cells: no chain recurses
  through them, each held once on a path, but the claims total's, which holds `claims`
  twice at the top of any path, the total over its death kind.
- **The checks' loops.** `WP_UK_S`'s seven checks are `all()` over generators, which
  compile to Python closures inside the cell; here each is a loop over the frame that
  returns False at the first month outside its tolerance, a NaN among them: the same
  verdict at the same month, in C.
- **Three powers raise as modelx does.** Past the largest float, Python's float power
  raises `OverflowError` where C's `pow` gives an infinity; below the smallest both give
  0, which each cell's own test refuses. So the inflation factor, the bonus rule's
  growth to its horizon and the endowment's discount on its bonus cost each call Python's
  own power where theirs is infinite from a finite base, inside the `try` that already
  turned Python's `OverflowError` into a refusal naming the point and the References, so
  that the compiled model raises the in-force step's message, word for word (uslib's
  *Record — M22* form); the test that refuses a result past the floats, or below the
  smallest, stays beside it. Only inputs far outside the product reach them (*What it
  refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `chassis()`,
  `sex()` and `tax_basis()`, and the three reports return a table row, text and
  DataFrames, for a reader, for `run_sec.py` and for the comparison with `WP_UK_S`. No
  other cell calls them, so they cost the projection nothing. Each label refuses any value
  but its column's codes, as `WP_UK_S`'s `chassis` and `tax_basis` do, and as `sex` now
  does where `WP_UK_S`'s returns the column as read, so each returns text or raises, and
  compiles to `str`. The seven checks compile to a `bint` each.

The `Data` docstring lists its 27 vectors, arrays and extents, each with the column or
file it comes from. The six readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 117 of
its 124, returns a C `bint`, `long long` or `double`, and caches a single value, or a C
array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,358 by `t`, of `double`, `long long` or `bint` | the 64 cells of `t` alone: every count, rate, factor, amount, balance, payout and cash flow, the chains and their six refusal cells; the policy clock, its years, the attained age and the declaration month; the two roll-forwards' residuals; and the flags `is_active`, `is_declaration_month` and `is_guarantee_date` |
| a C array of 1,358 by 10 | `pols_if_at(t, timing)`, `asset_share_at(t, timing)`, `claim_pp(t, kind)`, `smoothing_cost_pp(t, kind)` and `claims(t, kind)` |
| a C array of 105 by policy year | the eight openings, `pols_if_py(y)` to `smoothing_account_py(y)`, and `is_guarantee_year(y)` |
| one `bint`, `long long` or `double` | the 39 other cells without a parameter: the point's numbers, codes and flags, its opening state, the ends of its frame and the search for its exhaustion, the monthly charges and its chassis's last lapse year, and the seven checks |
| a Python object, or `str` | the seven reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three reports
and the seven checks on every committed point, twice, at the shipped References and with
the bonus rule on, each point's ItemSpace made afresh, and then the cells no report
reaches: `model_point()` and the three label accessors, which only a reader asks for;
`point_id()`, which only a refusal names; `bonus_supportable` and `declaration_month`,
which only the rule reads, and which the second pass reaches; `policy_value_pp` and
`smoothed_payout_capped`, which no cell reads, the payout writing the cap inline;
`unit_price` on the endowment; the six refusal cells, which only their chains' error paths
call, where a value has left the floats, and which return the value elsewhere, so that
the sample's call of each in every month types it; and the codes the reports leave: the
count at `AFT_DECR`, which no cell reads, the asset share at `AFT_MC`, which only its
refusal reads, and `smoothing_cost_pp` at `GUARANTEE`, which no flow reads. It calls
every timing and every kind, the claims total among them, in every month of the frame and
the month after it. Each call is of a code its cell takes, so none raises: a raise is not
traced. It runs the committed points alone: the export reads the CSVs of the directory
the build is made in, which in place is the product directory. They reach every branch
that fixes a type: both chassis, the rule off and on, the smoothing cap's floor and
ceiling and the corridor's, the market value reduction applied and waived on a guarantee
date, the guarantee charge's cap, the asset share floored at 0, the forced encashment,
the endowment's maturity and the limiting age's last month. They leave branches untaken: a
woman, the pension basis on a bond, a binding mortality cap, the surrender rate at its
bound, a value past the floats. That still types every cell, because every branch of a
cell returns the one type its others return, a count or an amount a float in every branch,
and on points that take those branches the compiled model computes modelx's numbers
(above). The labels need no trace beyond the committed points: each refuses what is not
its codes, so each returns text alone. The sample also raises the recursion limit, which
modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and no more, which a test holds to the spec's own derivation:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,358 | 1,357. The longest frame `proj_len()` admits is the longest cover, a bond issued at 18, the shipped `issue_age_min`, to the largest limiting age the shipped table admits, 121, or an endowment maturing there, issued 120 months after the valuation date, the shipped `Data.future_horizon_mth`: 12 × (121 − 18) + 120 = 1,356 months, `t = 0 … 1,355`, and the month after, 1,356, whose roll-forward residual reads the count carried into 1,357. The exhaustion search reads the units of the month they run out, one past a frame it ends, to month 1,356 at most |
| `t`, `timing`; `t`, `kind` | 1,358 by 10 | `t` as above, by the ten timings of the two families, and by the four kinds and the total, widened to ten. Every 2-D cache of a model shares one inner width, the widest: Cython's unpickle code converts them with one function, and two widths are refused by gcc 14, as uslib's `WholeLife_US_SEC` found (USLIB-SEC-PLAN.md §7.2) |
| `y` | 105 | 104: the policy year of the longest cover's last month, 1,235 months from issue, is 103, whose first month reads the eight openings, and that month's guarantee-imminent window waits for the date closing policy year 104 |

**The bounds the caches hold.** The sizes are derived from the shipped References and
table, and the in-force step projected whatever its References admitted: an
`issue_age_min` below 18, a mortality table rating ages past 120, which lets `omega_age`
run to a year past its last age, and a `future_horizon_mth` past 120 each admit a longer
cover or frame. Each Reference keeps its in-force domain, and `proj_len()` refuses, by
point, in modelx as compiled, a cover longer than 1,236 months, which reads the policy
years past the `y` cache, and a frame longer than 1,356 months, which reads the months
past the `t` cache, each naming the point: `point_id 302: the frame is longer than 1356
months, the longest the compiled model's caches hold: cover ends 1357 months after the
valuation date`, and `point_id 303: the cover, 1248 months from issue, is longer than 1236
months, issue at 18 to 121, the longest the compiled model's caches hold`. Covers are
whole years, so the next past 1,236 is 1,248, and a frame is refused a month past 1,356.
The exhaustion search reads no month past 1,356, so a bond whose units last past it is
refused whichever month they would run out in, and its "never" there is "not by
month 1,356". So no report on a point the model projects runs past these caches, raising a
bare `IndexError` where modelx projects, as a `PA_UK_SEC` edge did (UKLIB-SEC-PLAN.md
§6.7, *Record — M12*), and every point whose cover and frame they hold projects, whatever
the References. The cover's bound is conservative: it refuses a cover past 1,236 months
even where a bond's units would run out within the caches. A bond issued at 17 under an
`issue_age_min` of 17, to 121, in force at 24 and withdrawing 3% at +5%, has a cover of
1,248 months, but its units run out at policy month 798, a frame of 774 months, whose
reads stay at `t` 775 and policy year 67 and which the in-force step projects; this one
refuses it, by its cover, a departure from the in-force step reachable only through a
lowered `issue_age_min` or a longer table. The bound is kept because it is read before the
exhaustion search, whose own months it bounds and would otherwise need bounding by the
cover; a test holds that bond refused in both engines, message for message. A test runs
the longest frame and the longest cover compiled against modelx, under References that
admit longer, and refuses a month and a year past them in both, message for message. To
lengthen a bound, derive the sizes again, as `spec_sec.py` derives them, move the bound in
`proj_len()` and in the spec test with them, and rebuild: `t` to the frame's bound + 2 and
`y` to the cover's bound in years + 2. The ages bound no cache: an age indexes `Data`'s
mortality table, not a cache, and `mort_rate` refuses one the table does not rate.

**The frames the in-force step projected that this refuses.** Only those two, each reached
through a Reference set past its shipped value or a longer table, never at the shipped
ones: a cover longer than 1,236 months, a policy issued below 18 under a lowered
`issue_age_min` and in force past the table's first age, a bond issued at 15 to 120, say,
1,260 months, or one issued at 18 to a limiting age past 121 on a longer table, refused
even where a bond's units run out within the caches, as above; and a frame longer than
1,356 months, a policy issued more than 120 months after the valuation date under a longer
horizon whose frame then runs past it, the bond issued at 18 to 121 and 121 months on,
say. The caches cannot hold a frame longer than 1,356 months, nor the policy years of a
cover longer than 1,236 run to its end, and a cache sized to the longest any value of a
Reference admits would have no size, so the frame refuses them by point, naming the point
and the bound, as `PA_UK_SEC` refuses, on its scenario basis, a frame past its table
basis's longest (*Record — M12*).

### Two compiler directives

The library's `build_sec_cy.py` puts `# cython: infer_types=True, cpow=True` at the top of
the module mx2cy translates, before it compiles it, and on Linux and macOS compiles with
`-ffp-contract=off` and `-Werror=incompatible-pointer-types`. Without `infer_types` an
integer local, such as the year walks' month counter, stays a Python object, though the
cell is typed `double`; without `cpow`, `1 − (1 − q)^(1/12)`, the monthly rate of each
decrement and charge here, is a complex power, which gcc computes with `cpow` rather than
`pow`, and whose last bits can differ from Python's; and gcc fuses a multiply and an add
where the target has the instruction, one rounding where Python rounds twice. Twelve powers
here run under it. The tool's docstring has the detail, and uslib's
[`term_life/model-sec.md`](../../../uslib/products/term_life/model-sec.md) the measurements
that put each there. With all four, every compiled value here agrees with modelx bit for
bit. The compile tests hold each directive in the module's first line, and a static test
holds the tool's line to the two and no other: `cdivision=True` would make `//` on C
integers truncate where Python floors, which `duration(t)` meets before issue, where the
policy clock is negative; and `boundscheck=False` or `wraparound=False` would change what
an `idx` outside the table reads.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
1,853,528 bytes, the type's basic size, which holds every cell's cache, an array of 1,358
for each of the 64 cells of `t` and of 13,580 for each of the five of a code, and deleting
it, `del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a compile test runs the compiled runner on a block of 120 points, the committed table
copied five times, and finds no ItemSpace but the base alive after each collection.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows is a cold one
in the last month of the longest cover, a bond or an endowment issued at 18, now or 120
months on, 1,236 months from issue to 121, the longest cover `proj_len()` admits, with the
bonus rule and the estate's distribution on. One cell a month, as the in-force step left
the eight chains, compiled with gcc and issued now, each head cold in an ItemSpace of its
own, on the bond, the endowment and a bond withdrawing 1% a year alike: the count's heads,
a cold `net_cf`, the count, its roll-forward residual and the claims total, ran on a
thread of 292 KiB and not of 288; the asset share, the payout and the asset share's
residual on 232 and not 228; the guarantee and the smoothing account on 216 and not 212;
the units, the unit price and the guarantee charges on 212 and not 208; the bonus rule's
chain, a cell a year, on 40; with no refusal formatted on a chain. The count's chain was
past the 256 KiB the C step allows itself here, and every other within it; but CI's
Ubuntu runner needed two to four times this machine's stack for `Term_UK_SEC`'s cold call
(UKLIB-SEC-PLAN.md K12; §6.1, *Record — M2*), which puts the 212 KiB chains at 424 KiB to
848 KiB there, at or near the 1 MiB thread, beside the count's 584 KiB to 1.1 MiB. So all
eight chains are blocked by policy year. Blocked, the call runs on a chain of 215, one cell
a month within its year and two cells a year before it, where one cell a month ran 1,236,
and 8 to 25 cells more in modelx, which a test holds head by head. Compiled, the count's
heads on every shape, issued now and 120 months on, ran on a thread of 64 KiB and not of
60, and every other head on 56 and not 52, the bonus rule's on 40: a quarter of the 256
KiB. A test runs the count's heads and the smoothing account cold at each shape's longest
cover in a thread of 1 MiB, the stack Windows gives a program's main thread unless the
program is linked for more, and again on the main thread, which is where `run_sec.py
--cython` runs, and records the smallest of its sizes each ran on: 64 KiB here. MSVC's
frames may be larger than gcc's, and the `cython_uk` CI job, which runs the test on
Windows too, is the check on them. That test cannot see the blocking undone: one cell a
month, the deepest call needed 292 KiB here, which a 1 MiB thread holds, so only the
modelx depth test, which counts the chain cell by cell, guards the blocking, here and on
every runner. The export recurses in Python instead: the same call needs a recursion
limit of 490 there, and the reports and checks, which run in ascending `t`, need 128, so
`sample_sec.py` sets 2,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates. A
test holds the in-force suite's refusals to modelx's, compiled, message for message, on an
extract labelled otherwise than by position: each malformed row of the table, each
assumption table a reader cannot read, each point the frame refuses, each Reference off
its domain that the compiled model can hold, each value past the floats, by its cell and
by a report, each chain past the floats after its first month, mid-year, on a declaration
and on an anniversary, the claims total past the floats, a key read beyond the mortality
table, what the vectors cannot hold and each code a cell does not take inside its cache,
in a cell typed `long long` or `double` as in a Python one.

A message prints each Reference as the compiled model holds it: a rate as a float, an
age or a count of years as an int, and the horizon, which `Data` refuses before it is
read as one, as a float, `not 9007199254740992.0` whether it was set as `2**53` or as
`2.0**53`; and it names a timing or a kind by its code, `claims(19, 1)` for the
surrenders, in both engines. An int Reference, `issue_age_min`, `omega_age` or
`bonus_horizon`, and `Data`'s `future_horizon_mth`, is a C `long long` compiled, and a
float set on it is truncated as it is set, 120.5 to 120, or a horizon of 12.5 to 12,
where modelx refuses 120.5 and 12.5 as not whole numbers, and a NaN or an infinity
cannot be set on it at all; so set each as a whole number. The switch, `bonus_rule_on`,
is a C `bint`, which takes any value's truth as it is set, 2 and `"yes"` as True and
`None` as False, where modelx refuses each; so set it as True or False. The compiled
refusal test sets `Data`'s References as it sets `Projection`'s: the horizon is refused
at −1 and at `2**53`, as ints and as floats, as in modelx, read at 121 and 121.0, and at
12.5 does what 12 does.

- What `Data` cannot decode or hold, when the vector is first read, naming every point or
  line at fault: a `point_id` that is not a whole number, or is `2**53` or more in size; a
  mortality age or a lapse policy year as large, before its table is cast; and, as since
  the in-force step, a code that names no chassis, sex or tax basis, guarantee dates that
  are no anniversaries or that an endowment carries, and an age, a term or an amount the
  contract cannot have. A key written as a float, an age `70.0`, is read by its value, as
  `WP_UK_S`'s lookups match it. The tables' checks find a gap from the keys a table holds,
  so that a key far from the rest, `2**53 − 1`, is refused as a gap at once.
- A key beyond the mortality table, by the one cell that reads it, where `WP_UK_S`'s
  lookup raised `KeyError`: `point_id 7: mort_table.csv has no rate at attained age 18`,
  from `mort_rate`, on a table that starts at 20.
- A cover or a frame longer than the caches are sized for, by `proj_len()`, naming the
  point and the bound (*The bounds the caches hold*, above), under References each in its
  domain, the cover's bound even where a bond's units would run out within the caches.
- A value past the floats, in the cell where it first is, naming the point, the month and
  what makes it (*Departures from WP_UK_S*), the six chains' through their refusal cells,
  each in its opening month and, from an opening state, columns and References each in its
  domain, mid-year, on a declaration month and on an anniversary where its chain moves
  there. The unit price and the endowment's guarantee move on a declaration alone. The
  cumulant of the charges stops growing at its cap, a share of the asset share the month
  opens with, but the cap is not tested on a nil asset share: an endowment with a nil
  asset share, `guar_charge_rate_base` 1, `amc_rate` 0 and premiums of 6e307 a year, with
  no estate distribution, has its whole premium charged each month and closes each month
  at nil, and a cumulant carried in near the largest float is refused mid-year at month 3,
  on its declaration at 5 and on its anniversary at 6. Each refusal cell repeats its
  chain's formula, branch by branch, and a test holds it to its chain, bit for bit, in
  every month of every committed point, since C4 compares two engines that would share a
  drift.
- A power past the largest float, or below the smallest, which Python's float power
  refuses with `OverflowError` where C's `pow` gives an infinity: the inflation factor,
  the bonus rule's growth and the endowment's discount call Python's own power where
  theirs is infinite from a finite base, inside the `try` that names the point and the
  References, so that the compiled model raises the in-force step's own message as modelx
  does (uslib's *Record — M22* form), rather than carry an infinity on; and each tests its
  result for 0 where a long horizon or a rate a hair above −1 decays it below the smallest
  float. Only inputs far outside the product reach them: an inflation of 1e200 at the
  second anniversary, a fund return of 1e20 over a horizon of 20 years, a discount rate of
  1e200, and the largest horizon on the down scenario.
- A timing or a kind no cell takes, by the cell, as `WP_UK_S`'s are: `invalid timing` and
  `invalid kind`, each code inside the width of ten that a cell does not take among them.

An argument outside a cache raises `IndexError` in the compiled model alone:
`net_cf(1358)`, or `net_cf(-1)` on a point issued at the valuation date, which modelx
answers with 0, the month being outside cover; a timing and a kind of 10, which modelx
refuses as codes it does not take; and policy year 105 on each opening and on
`is_guarantee_year`, past the `y` cache, which modelx computes as it computes any year's,
0 on the test's point, the worked example's bond, that year long past its cover, and -1
on `is_guarantee_year`, no year at all. No frame asks for any of them. An `idx` past the
last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's last
point, under that point's own `point_id()`; the compiled refusal test holds both against
modelx.

An annual mortality above 1 is not refused but capped, in both, and so is a surrender
rate, and the smoothing cap and the corridor clamp the payout: a compile test holds the
two engines equal where the mortality cap and the surrender rate's bound bind, and the
splice grid where the corridor, the smoothing cap, the guarantee charge's cap, the asset
share's floor and the MVR's bound do. A NaN product would stay NaN through the mortality
cap, in both, which the compiled model computes as a comparison that keeps the value
unless the bound is smaller.

### Speed

`python tools/bench_sec_cy.py with_profits` builds the model into a temporary directory
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
| compiled | 6,000 | 0.803 ms (0.791–0.822) | 1.615 ms (1.586–1.671) | 88–89 MB |
| export | 600 | 10.70 ms (10.69–10.77) | 11.21 ms (11.14–11.29) | 88–89 MB |
| modelx | 120 | 302 ms (285–322) | 344 ms (335–349) | 145–152 MB |

On `net_cf` the compiled model runs 13.3 times its export (13.1 to 13.5 over the three),
and on `result_cf`, where building the DataFrame takes half its time, 6.9 times (6.7 to
7.1); it runs 368 times modelx on `net_cf` (355 to 408) and 207 on `result_cf` (206 to
220). The ranges are the noise of a machine other builds were using, its 1-minute load
between 3.0 and 4.4 as the runs started: about −6% to +7% on modelx's `net_cf`, −3% to +2%
on its report and −2% to +2% on the compiled `net_cf`. `WOL_UK_SEC`, timed the same way,
ran 13.0 and 5.9 times its export. A point here costs more on every engine than one of
`WOL_UK_SEC`'s for its frame, 398 months on average over the committed points against its
617, two and a half to three times as much a month: eight chains a month, where it carries
four, and a payout machinery, the smoothing cap, the corridor, the final bonus and the
market value reduction, beside them. The release keeps a block flat: the compiled model's
peak and the export's grew by less than 0.1 MB over their 6,000 and 600 points in every
run, where modelx's rose by 56 to 63 MB in its loop. Reading the three files and building
every `Data` vector and array for the compiled block took 0.10 to 0.21 s, and asking every
point for its frame, the runner's first pass, 0.38 to 0.50 s. Every engine, loop and run
summed `net_cf` over a copy of the table to the same −644,540.6467, to 1e-9 relative.

Measured on 2026-11-24 on a machine shared with other work: 4 CPUs (an Intel Xeon at
2.10 GHz), a 1-minute load average between 3.03 and 4.36 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1,
numpy 2.5.3 and pandas 3.0.5, on one build of the model, `--build`.

## Tests

**The default run and the full grid.** The default run takes the core of the splice grid
and the default cases of the slower tests; the full grid, `UKLIB_SEC_FULL=1`, runs the
rest, and one leg of the `sec_uk` job runs it. Only on the full grid: the splice's other
cases; the every-state test's sets but S as shipped, the splice's main and rule sets and
the two sets of the committed rows' own References; the depth test's row of each shape
issued 120 months on; the other committed points of the scaling, ten million, extract and
month-on tests; and the whole-limit test's later rows. The every-state test restates each
S point by default at every month of its first policy year and the first anniversary, the
declaration and the anniversary of every fifth policy year, policy months 106 to 120 and
the frame's last month, and on the full grid at every month. UKLIB-SEC-PLAN.md U6 asks for
about five minutes by default (K6). The default run took about 316 s at the M13 review, at
a peak of 3.4 GiB, and after the review's rework, which adds the splice's third set and
seven core rows, about 406 s at a peak of 4.7 GB. Each splice set now reads S with the
points its cases compare alone, where it read all 16, the generator writing a twin of each
and the rule's exhaustion searches projecting them: the default run takes about 321 s
here, at a peak of 3.4 GB, and the full grid about 1,030 s, at a peak of 3.6 GB, on a
machine shared with other builds, each comparing what it did. So the default run is about
half a minute over. Moving the every-state test's main and rule sets to the full grid
saved about 30 s; moving the splice's rule and bound sets there too would save about a
minute more, but leave no core row declaring under the rule or holding the surrender rate
at its bound, which the review asked for. The C step (M14) adds the representation's
tests, about half a minute, which hold the compiled form in a run with no compiler and so
stay in the default run, and the compile tests, which run in the default run too where
modelx-cython and a compiler are at hand. Without them, `-m "not cython"`, as the `sec_uk`
legs run it, the default run took about 380 s here, at a peak of 3.6 GB, and after the
review's rework, which adds the withdrawing bond's chains to the default run, about half a
minute, two core rows whose units run out at the end of cover, and the caches' bounds,
about 440 s, at a peak of 3.8 GB; with them, the model built once, about 840 s, at a peak
of 4.2 GB, the build two minutes of it; and the full grid, its compile tests comparing the
whole grid, about 1,850 s before the rework, at a peak of 4.2 GB, on a machine shared with
other builds, the rework's runs beside another session's tests. So the run the `sec_uk`
legs make is about 140 s over: the representation's tests about half a minute of it, the
withdrawing bond's chains another, and a busier machine than M13's the rest. Moving either
to the full grid would leave a run without a compiler no hold on the compiled form, or the
default run none on the depth of the withdrawing bond's chains, which the review asked
for, so the cuts that remain are M13's, at the cost above.

**Branches the core reaches.** A test asserts the core reaches each branch, keyed by the
set of References it runs under where the set matters. A withdrawal is capped at the unit
fund in every withdrawing bond's issue month, whose fund opens at 0, as well as in the
month its units run out, which the frame does not project. The surrender rate reaches its
bound inside the domains, under an MVR deterrent of 25, on the down scenario from policy
month 68, which the splice's third set of References holds. The rule's cut held to its cap
above the floor is reached by a 6% rate on the down scenario, and the MVR held to its
contractual bound by a 20% bonus on a 12% return, two variants of S's points.

- **The twin identity**, in `tests/test_model_conventions_uk.py`: on points 5 and 7, the
  endowment and the bond issued at the valuation date, every cell of `WP_UK_S`'s agrees at
  every argument `WP_UK_S` evaluates in its own sweep, to 1e-9 relative with no absolute
  floor, but for `pols_if_init` and `model_point`, and the four cells the spec names with
  its reasons; a cell this model lacked would fail it. So `WP_UK_S`'s goldens on its new
  business hold here with no number restated. The same suite holds the model to the
  conventions every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the
  `"BEF_DECR"` count, new business enters once at its `policy_count`, nothing happens
  before issue, and the in-force columns are present.
- **The splice**, in `tests/test_with_profits_uk_sec.py`: each `WP_UK_S` point restated in
  force at months about its events — the declarations at the end of each policy year's
  twelfth month, the month after each and mid-year; on the down scenario the smoothing
  cap's floor from 61, the market value reduction from 68, the corridor's ceiling from 92,
  the guarantee window, 106, 107 and 118 to 120, the charge's cap from 160 and the asset
  share's floor from 242; the 5% bond's cap from 504, where it flickers; the withdrawing
  bond's cap from 284 and its last month, 402; the endowment's cap at 289 and 290 and its
  maturity, 299; the bond variant's cap from 88, its floor from 196 and its last month,
  266; and the limiting age's last month, 779 — continues the S projection in every cell
  the two share but the frame's length, S's accessors of the columns its frame opens with,
  and the declaration month, a valuation month here, and in `result_cf`, `result_payout`
  and `result_pols`, to 1e-9 relative with no absolute floor, the residuals and the
  smoothing cost of an exit, a difference rounding about 0 where the payout is the asset
  share, at 1e-9. `WP_UK_S`'s own in-force rows are spliced as twins, at 60 and 240. The
  splice runs on two sets of References: an estate distribution on, which ships off, and
  the MVR deterrent and the guarantee-imminent factor set apart from the factors they ship
  equal to; and the same with the bonus rule on, on fewer rows, its own months about the
  rule's declarations. Inflation, the input on the valuation clock, is 0 in both. Variants
  of S's points, in a copy of S's table that is never committed, reach what S's own
  cannot: a female life, a −40% crash for the corridor's ceiling, the pension tax basis on
  a bond, three bonds issued at the valuation date, at 5% with and without withdrawals and
  at −15% without, whose charges stop at 442, 197 and 101, and two withdrawing bonds whose
  units run out in the last month of cover, 779, which the exhaustion search reads last,
  and in 778, each restated at 777 and encashed the month before. The default run takes a
  core of the grid; a test asserts the core reaches every branch, opening-state column,
  kind of valuation month and side of every `min` and `max` the full grid reaches. The
  binding mortality cap is held by a test of its own, under a mortality factor of 2.
- **Future new business**: the bond and the endowment issued 1, 12 and 120 months on, and
  the variants 13 months on, each S's projection moved on, with zeros before issue and no
  table read there.
- **How it computes**: on every row of the splice's grid, after its reports, its checks
  and every monthly cell at every month, no cell has been called at a negative month, none
  on the books read a month before `t_entry()`, none read a month later than `t + 1` but
  the bonus rate's declaration read, inside the frame, and none raised; the exhaustion
  search reads the units to the month they run out and no further. On a fresh read of the
  committed model the policy clock is a closed form, and every point's reports and checks
  run under a lowered recursion limit, which a recursion backward over the frame would
  exceed. And each chain, called cold in the last month at the contract's longest cover on
  each shape, runs one cell a month within its policy year and two cells a year before it,
  back to `t_entry()`, and its head's own measured overhead more; each opens a policy year
  with the year before's close, bit for bit; and no cell a cold call's deepest path holds
  twice builds text.
- **Counts**: the roll-forward closes; `result_pols()` holds the counts; multiplying
  `policy_count` by 2.5, with the rule and the estate distribution on, multiplies every flow
  and counted cell, each nonzero on some point, and moves no per-policy value; a point
  restated a month on, opened with what the model carries into its month 1, continues its
  own flows; and the roll-forward, its tolerance scaled by the count, closes on ten million
  policies.
- **Validation and regeneration**: each malformed row of the table refused naming its
  point, and naming its label on an extract labelled otherwise than by position; the
  horizon a Reference; a point past its cover, one the contract does not issue, a bond
  spent in its first month, and a cover or a frame longer than the compiled model's caches
  hold refused by `proj_len()`; each Reference off its domain, at the value next outside
  each edge, NaN and both infinities, where each edge is accepted and projects its
  reports; each value past the floats refused in its cell, the powers' among them; each of
  these refusals naming the label of an extract labelled otherwise than by position, as
  the compiled model's must too; each assumption table a reader cannot read refused naming
  its lines; keys written as floats read as `WP_UK_S` reads them; the edges of the
  interface accepted; every state `WP_UK_S` reaches accepted in force; and the committed
  table is what `WP_UK_S` generates.
- **The product's own facts**: the two clocks on the shipped points; the committed rows
  continuing their S points at the shipped assumptions but for inflation, and the rows read
  under References of their own continuing `WP_UK_S` under them; each history column read,
  not recomputed (UKLIB-SEC-PLAN.md K14): the asset share, the units, the unit price, the
  attaching bonus, the payout, the bonus rate and both cumulants, each on a state whose
  history departs from what today's References give; the single premium paid in the issue
  month alone; the declaration, the guarantee dates and the guarantee-imminent window on the
  policy clock; the bonus rate's read bounded by the frame; the new "never"; expense
  inflation on the valuation clock; the cap on mortality and a NaN that reaches a bound; a
  check whose residual is NaN; the values outside cover; the block; an in-force extract;
  the runner; the docstrings; the shared input tables; each pair of parameters a formula
  could confuse, equal somewhere, apart on some core row; and no computed cell building a
  Python object, nor any taking a default, a generator, a keyword, a text comparison or
  `len()` of a `Data` array, each exemption checked by the check itself.
- **The representation**, which holds the compiled form in modelx, in seconds: the claims
  total `WP_UK_S`'s `sum` to the last bit, its kinds counted and the rows where a total
  left to right would part read, the bits skipped on Python 3.11, whose `sum` adds left to
  right; each refusal cell its chain, bit for bit, every month; each
  chain past the floats after its first month refused there; every decode `WP_UK_S`'s own
  on every value a column holds, the guarantee dates' written forms among them; the padded
  arrays NaN and read inside their keys alone; each `Data` vector the dtype its docstring
  states; every parameterless cell a Python number; each label refusing what is not its
  codes; the spec's sizes as its comment derives them, and the bounds they are derived from
  held; the sample's recursion limit and its calls; the runner's rebuild; and what the
  vectors cannot hold and the codes a cell does not take, refused.
- **The compiled model**, in `tests/test_compiled_conventions_uk.py` and here, each marked
  `cython`, compiled once a session into a temporary directory: every cell C-typed, the
  caches the spec's, C4 on the committed points and the release of a block, the
  conventions'; and here C4, every value modelx caches compiled bit for bit, with every code
  of every coded cell asked on every row, which a test holds row by row, on the splice grid
  under its three sets, at the contract's extremes, where the mortality cap and the
  surrender rate's bound bind, on every decoded value, on keys written as floats, on the
  committed rows under their own References, on the rule's declarations in the frame and
  on the bonds whose units run out, in chunks of frame months; the labels; the refusals and
  the overflows, message for message; the deepest cold calls on a 1 MiB stack; a Reference
  set late; and the runner. They skip without modelx-cython or a C compiler, and the
  `cython_uk` CI job's `with_profits` shard fails a skip.

```bash
python -m pytest tests/test_with_profits_uk_sec.py -q
UKLIB_SEC_FULL=1 python -m pytest tests/test_with_profits_uk_sec.py -q   # the full grid
python -m pytest tests/test_with_profits_uk_sec.py -q -m "not cython"    # no compiler
python -m pytest tests/test_model_conventions_uk.py -q -k WP_UK_SEC
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uklib-std
<!-- END generated citation links -->
