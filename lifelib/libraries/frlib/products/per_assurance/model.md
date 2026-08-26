# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/per_assurance/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> mechanics are sourced — the *blocage* and the seven `L. 224-4` early-release cases
> [R3], release paid as a single payment of all or part of the eligible rights
> [R5 D. 224-4](#frlib-per_assurance-r5), the 1 % transfer indemnity nil after five years from the first
> *versement* [R3 L. 224-6](#frlib-per_assurance-r3), the 0 % maximum technical rate for a PER tariff
> [R9 A. 142-1](#frlib-per_assurance-r9), the regulatory de-risking grid and its four qualified profiles
> [R6 art. 1](#frlib-per_assurance-r6), the euro capital floor stated net of loading and net of charges levied
> [S1] [S3] [S7], death closing the plan [R3 L. 224-4 II](#frlib-per_assurance-r3), the compartment-3
> annuity-only rule [R3 L. 224-5](#frlib-per_assurance-r3) [S2], and the €110 monthly *quittance* commutation
> threshold [R10 A. 160-2](#frlib-per_assurance-r10). Every **rate** is a **[std]** standardization: the *encadré*
> requires charge **maxima** to be disclosed and caps no level [REG-R30], no sampled
> insurer publishes an annuity rate card [S1] [S2] [S4] [S7], TH 00-02 / TF 00-02 and
> TGH05 / TGF05 are cited and not shipped [REG-R21] [REG-R22] [REG-R23], and no public
> French experience exists for PER early-release, transfer or annuitisation behaviour.

## Run it

```bash
python products/per_assurance/run.py            # the notes' worked example
python products/per_assurance/run.py 6          # the annuity that is not commuted
python products/per_assurance/run.py 10         # the cell whose death floor bites
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/per_assurance/PER_FR_A")
model.Projection[1].result_cf()
```

`result_state()` gives the glide path and the two supports — the technical notes'
worked-example table, whose `pols_if_eoy` column is the notes' end-of-year `l(t)`.
`result_settlement()` gives the settlement at the horizon, down to the commutation test.
`result_cf()` gives the cash flows, and its `pols_if` column is the count each row
**opens** with, which is the weight that row's flows carry.

## Accumulation with a two-way exit

That sentence is the product, and it is the reason this model looks unlike the other
savings models in the library.

The plan is **blocked** until the `L. 224-1` maturity [R3]. There is no surrender right,
no surrender charge and no market value adjustment, and the contracts say so in terms:
the accumulation phase carries "no surrender right except in the statutory cases"
[S2] [S3] [S4] [S7]. So there is **no `lapse_rate` and no `claims_lapse` anywhere in
`PER_FR_A`**, and `test_there_is_no_lapse_machinery_anywhere` asserts their absence
rather than leaving it to inspection.

What leaves the book instead are two decrements that are not the same event and do not
pay the same amount:

| | `early_release_rate` | `transfer_out_rate` |
|---|---|---|
| What it is | *Déblocage anticipé* on one of the seven `L. 224-4` cases [R3] | Transfer of acquired rights to another PER [R3 L. 224-6](#frlib-per_assurance-r3) |
| Trigger | A listed event — death of a spouse, invalidity, serious illness of a dependent child, over-indebtedness, exhaustion of unemployment rights, business liquidation, purchase of the main residence | The holder's election, at any time |
| Charge | **None** [S2] [S3] [S7] | 1 % of acquired rights while `duration < 5`, nil after [R3 L. 224-6](#frlib-per_assurance-r3) |
| Pays | The **whole** account value | `A(t) · (1 − ι(t))` |
| Compartment 3 | Reduced — the main-residence limb is closed to it [R3 L. 224-4 I 6°](#frlib-per_assurance-r3) | Unchanged |
| Where the money goes | Out of the regime | Stays in the regime: the *blocage*, the compartments and the exit conditions travel with it |

Using one decrement for both, or naming either a lapse, silently attaches the wrong
payment formula to half the exits — and they dominate the run-off. At 2.60 % a year
combined they remove about a quarter of the book over the anchor cell's twelve years, far
more than mortality; the aggregate anchor is 2.62 % of accumulation-phase provisions
leaving every year [R22].

Only the main-residence case of the seven is discretionary, and none of them responds to
investment performance, so a dynamic moneyness multiplier would be a category error on
`early_release_rate`. The behavioural lever that does exist on this product — the holder
moving the declared retirement date, which re-cuts the whole allocation immediately
[R5 D. 224-3](#frlib-per_assurance-r5) [S3] [S4] — has no public calibration and is not modelled.

## The glide path is an input table

`allocation_grid.csv` is keyed by (`allocation_profile`, `years_to_horizon`) and gives
`euro_share` and `uc_share`. `alloc_euro(t)` is a lookup, not a formula.

```
k(t) = n − t + 1
a(t) = allocation_grid[allocation_profile, k(t)].euro_share
```

That is deliberate, and it is the single most important design decision in this model.
*Gestion pilotée par horizon* is the **default management by law** [R3 L. 224-3](#frlib-per_assurance-r3), the
arrêté fixes four qualified profiles and a minimum low-risk share by distance to the
declared liquidation date [R6 art. 1](#frlib-per_assurance-r6), and **in this market the regulatory grid is not a
floor insurers beat; it is the product** — Suravenir reproduces it verbatim [S7] and
Generali's profiles hit exactly those percentages over exactly those bands [S2]. But the
anchor contract sits above it on **twenty one-year bands** rather than four [S1], and an
insurer may restate a profile's allocation unilaterally [S3] [S4]. A published grid is a
snapshot. Putting it in a file makes substituting one a table edit.

| Profile | `k > 10` | `10 ≥ k > 5` | `5 ≥ k > 2` | `k ≤ 2` |
|---|---|---|---|---|
| `prudent` | 30 % | 60 % | 80 % | 90 % |
| `equilibre` | — | 20 % | 50 % | 70 % |
| `dynamique` | — | — | 30 % | 50 % |
| `offensif` | — | — | 30 % | 50 % |

`dynamique` and `offensif` are shipped **identical**, which is what the arrêté says
[R6 art. 1](#frlib-per_assurance-r6) rather than an oversight.

**The boundary belongs to the tighter band** **[std]**: `k = 10` reads 20 %, `k = 5` reads
50 %, `k = 2` reads 70 %. R6's part (a) grid *was* extracted — percentages and band
headings both [research §5] — but the headings as rendered read "≥ 10 years out" and
"from 10 years out", which overlap at `k = 10`, and the same at 5 and at 2. The text
therefore does not say which band a boundary year falls in, the conservative rule is the
model's own, and the looser reading understates the euro share for a full year at each of
three transitions.

"Low risk" is realised wholly as the euro support **[std]**. The definition of *actifs
présentant un profil d'investissement à faible risque* is delegated to an arrêté that was
not retrieved [R5 D. 224-3](#frlib-per_assurance-r5), and the two contract definitions found disagree — SRRI ≤ 3
[S7] against ≤ 2 including the euro fund [S3]. Realising the bucket as the euro support is
the most conservative reading of both and keeps the model to two supports. The unlisted
minimum that bites since 24 October 2024 [R6 part (b)](#frlib-per_assurance-r6) [R7] is not carved out of the UC
bucket.

## The rebalancing, and which support pays for it

```
m(t)   = a(t)·A(t−1) − av_euro_pp(t−1)
arb(t) = arb_rate·|m(t)|
E_eu   = av_euro_pp(t−1) + m(t)          + a(t)·V_net              (m ≥ 0)
E_uc   = av_uc_pp(t−1)   − m(t) − arb(t) + (1 − a(t))·V_net
```

with the roles of the two supports exchanged when `m(t) < 0`. Two conventions, both
**[std]** and both load-bearing.

**The arbitrage charge comes off the *source* support.** The destination receives the
switch in full, so on a de-risking switch the post-rebalancing euro share lands at or just
above the regulatory minimum rather than just below it. On the anchor cell's year-8 band
crossing the BOY euro share is 50.04 % against a 50 % target; taking the charge from the
destination instead would put it under, at every crossing, by `(1 − a)·arb`.
`check_euro_share_min()` asserts it.

**The *versement* is not a switch.** New money is allocated directly at the target mix and
bears no arbitrage charge, which is what "allocation of both contributions and existing
balance" means in the one contract publishing its ladder [S1].
`arbitrage_charge_pp(t) = 0` in years 1 and 2 of the anchor cell, where the *équilibré*
grid asks for no euro support at all, even though €3 000 was paid in each.

**The minimum binds at the rebalancing date, not continuously.** Between dates the mix
drifts with relative performance: the anchor cell is at 70.00 % euro after its year-12
rebalancing and 69.67 % at the year end. Nothing in the model reads the year-end share,
because re-imposing the target there would invent a rebalancing frequency the annual grid
does not have. Real contracts rebalance quarterly to semi-annually [S1] [S3] [S7], and the
annual grid concentrates each step into one switch.

### The one case the convention cannot cover

The two halves of "charge the source" and "land at or above the minimum" come apart on a
**reverse** switch, and the notes do not say which half wins. Model point 2 arrives
holding 40 % euro against a 20 % minimum nine years out — which is what an incoming
transfer can do — so its first rebalancing sells euro down to the grid, the euro support
is itself the source, and charging the source takes €12.00 out of the very balance the
minimum is measured on. The share lands €9.60 below the line on €19 988, or 0.05 % of the
balance.

This model implements the notes' formula literally, symmetric in the two supports, rather
than quietly charging the UC side in both directions. `check_euro_share_min()` therefore
measures against `euro_share_min_bound(t)` — zero on a de-risking switch and
`−(1 − a)·arb` on a reverse one — so it states the property that is actually true in each
direction and still fails if the charge is taken from the destination on a de-risking
switch. A firm resolving the gap the other way changes one branch of `av_euro_pp_at` and
nothing else.

## The garantie plancher is not a floor at gross premiums

```
g(t) = g(t−1) + V_net − arb(t) − mgmt_charge_pp(t)
```

*Versements* net of entry loading, less the management charges levied over the plan's
life, less benefits already paid — **[S1]'s drafting**, and [S7] states expressly of its
own guarantee that it is not a floor at gross premiums. [S3] drafts the same guarantee
with euro-fund interest net of charges **added**, which is a different quantity and not
what this model computes; see *The garantie plancher base* in the technical notes, which
is the source of truth for the recursion. It follows that

```
A(t) − g(t) = [A(0) − g(0)] + Σ gross investment return credited to date
```

so the floor bites only where cumulative investment return is negative.
`check_floor_identity()` asserts it in every projected year. That check is zero by
construction given the recursion — which is why it is written out. What it catches is the
*wrong* recursion: a base accumulated at gross `V`, a base that forgets the arbitrage
charge, or a base charged something other than what the account was actually charged. Each
breaks the identity in the first year in which it is wrong.

On the anchor cell the floor never bites: the gap is €22 821.04 at the horizon against an
opening gap of €600.00, so the guarantee sits 32.6 % below the account value throughout.
Model point 10 is the same cell with a €19 000 opening base — a plan whose accumulated
investment return to date is negative — where the floor sets the death benefit for two
years and then stops.

The cover ceases at the member's **70th birthday** [S1] [S3] and the floor is capped at
€762 245 across contracts [S3]. Model point 9 retires at 70 and crosses it in its final
plan year. The age-70 cliff is not incidental: it is also the age at which a PER death
benefit stops being taxed under CGI art. 990 I and enters the inheritance-duty base **in
its entirety** under art. 757 B [R15] [REG-R41], and from 2026 the age at which
contributions stop being deductible [R20] [R21]. One birthday, three consequences.

The *garantie plancher* charge is folded into the 0.70 % management charge **[std]**;
neither published figure — 0.10 % p.a. on UC balances [S3], 0.12 % inside a 1 % charge
[S1] — is separable in a way that transfers to a composite.

## Settlement: a capital leg, and a rente that usually is not one

At `t = n` the survivors settle. The capital leg bears **no exit charge** [S1] [S2] [S3]
[S7] [S8]. The annuity leg is converted at `annuity_factor()`, charged the *frais
d'arrérages* at 1.50 % **[std]** [S8], and tested against the commutation threshold.

Two things follow from the 0 % maximum technical rate [R9 A. 142-1](#frlib-per_assurance-r9).

**`a_x` is an undiscounted expected-instalment count**, not a discounted annuity factor.
Nothing in the model discounts it and `rente_gross_pp()` is a plain division; 22.0000
asserts 22 further annual payments to a male aged 64 **[std]**. A 2 % rate would shorten
the factor to about 17.66 and inflate the annuity by roughly a quarter.

**Commuting at the conversion basis is nearly value-neutral**:

```
commuted = rente_net · a_x = annuity_cap · (1 − c_arr)
```

`check_commutation_identity()` asserts it. Commuting at a *book* value instead
manufactures a gain out of nothing. The mechanism is not marginal — €272 m of 2024
individual-PER benefits at an average €16 200 [R22] — and the €110 threshold is a
**monthly** *quittance* scaled by the months in the payment period [R10 A. 160-2](#frlib-per_assurance-r10), so an
annual frequency tests against €1 320. Testing €110 against an annual instalment would
commute almost nothing.

The anchor cell's annuity is €78.45 a month and duly commutes; the cliff sits at
`annuity_share = 42.06 %`, and model point 6 is the same cell at 50 %, whose €130.75 a
month is paid as a *rente*. That is a live instance of the market pattern: the average PER
annuity in payment is €1 300 a year, about €108 a month, just under the threshold
[R22] [R10].

## What is simplified, and where the rest of it lives

**The rente is cross-referenced, not re-implemented.** Where the annuity is not commuted
this model hands `annuity_conversion` to `Rente_FR_S` and records the amount. The annuity
reserve, the 0.80 % p.a. charge on annuity reserves [S7], reversion, *annuités garanties*
and revaluation through the profit-sharing account are specified in
[`../rente_viagere/technical-notes.md`](../rente_viagere/technical-notes.md). Duplicating
the payout chassis here would give the library two of them to keep in step.

**Staged capital is settled at the horizon** **[std]**. The *capital fractionné* option
[R3 L. 224-5](#frlib-per_assurance-r3) changes *when* the capital leg is paid, not how much: there is no exit
charge, and the technical notes fix `proj_len` at the declared horizon. The model records
the whole capital leg at `t = n`, publishes the instalment as `capital_instalment_pp()`,
and credits nothing to the unpaid balance. Exact on an undiscounted gross-cash-flow basis;
not exact for anything that discounts, and a discounting layer needs the schedule.

**No PPB stock** **[std]**. The euro support is credited at the asset return [S9] and
charged on the post-crediting balance [S3]. The effective euro rate net of charge is
`1.0338 × 0.9930 − 1 = 2.6563 %` — not `3.38 − 0.70 = 2.68 %`, and not the 2.75 % actually
served in 2025, whose extra seven basis points came from a *provision pour participation
aux bénéfices* release [S9]. A PER's PPB release horizon is fifteen years rather than
eight, because the commitments sit in a *comptabilité auxiliaire d'affectation*
[REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8); modelling that stock is a fund-level scenario extension, and four
of the seven sampled contracts have no contractual profit-sharing clause at all
[S4] [S5] [S6] [S7]. The machinery this stands in for is implemented next door in
`Euro_FR_A` and specified in
[`../assurance_vie_euro/technical-notes.md`](../assurance_vie_euro/technical-notes.md) —
the *compte de participation aux résultats*, the PPB dotation-and-release lever and its
vintage clock. Two cautions before lifting it: the release deadline there is eight years
and here it is fifteen, and a PER euro fund is not an assurance vie euro fund. See *The
euro leg is cross-referenced, not re-implemented* in this product's technical notes.

**Tax is outside the projection.** `deduction_elected` is carried on the model point and
enters no recursion. The election is the pivot of the whole exit tax treatment
[R19] [R20] [R21], but it changes what the holder keeps, not what the insurer pays.
`test_the_deduction_election_is_carried_and_inert` projects the anchor cell with the flag
flipped and asserts an identical cash flow table.

Also out of scope, per the notes: partial early release leaving the plan in force
[R5 D. 224-4](#frlib-per_assurance-r5); the 15 % transfer-value reduction on euro-denominated rights
[R5 R. 224-6](#frlib-per_assurance-r5) [S8]; profile and horizon changes during the projection; and the *provision
de diversification* supports [S4] [S6], which are the `eurocroissance` product.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `PER_FR_A/` holds nothing but formulas:

```
products/per_assurance/
  model_point_table.csv        <- inputs live here
  allocation_grid.csv
  mort_table.csv
  exit_table.csv
  annuity_factor.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  PER_FR_A/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `allocation_grid_file` | `allocation_grid()` | `allocation_grid.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `exit_table_file` | `exit_table()` | `exit_table.csv` |
| `annuity_factor_file` | `annuity_factor_table()` | `annuity_factor.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Twelve model points. **Point 1 is the technical notes' worked example** — M 52, horizon 64, `duration_ifo` 2, c1, *équilibré*, €16 600 all in UC against a €16 000 floor base, €3 000 a year, 70/30 exit. Point 2 is a c3 annuity-only cell arriving with a reverse switch; 3, 4 and 5 are the *prudent*, *dynamique* and *offensif* ladders; 6 is the anchor at a 50 % annuity share, above the commutation threshold; 7 and 8 are the two capital forms; 9 crosses the 70th birthday; 10 is the anchor with a floor that bites; 11 is a c2 cell with no floor and no contributions; 12 is a 32-year *prudent* annuity cell | anchor cell **[std]**, technical notes' worked example; €16 600 is the published average accumulation-phase balance [R22] |
| `allocation_grid.csv` | Target `euro_share` and `uc_share` by (`allocation_profile`, `years_to_horizon`), four profiles, `k` = 1 to 45 | the regulatory minimum grid [R6 art. 1](#frlib-per_assurance-r6); band edges **[std]** |
| `mort_table.csv` | Annual mortality by sex and age 18–120, capped at 1 | **[std]** proxy shaped on French population mortality [REG-R24]; **level** anchored so that `mort_be_factor × q(M, 52)` is the notes' 0.00500 placeholder exactly — *not* TH 00-02 / TF 00-02 [REG-R22] [REG-R23] |
| `exit_table.csv` | `early_release_rate` and `transfer_out_rate` by (`compartment`, `duration`); 1.60 % / 1.00 % on c1 and c2, reduced release on c3 | **[std]**, split of the 2.62 % aggregate of [R22]; c3 loses the main-residence case [R3 L. 224-4 I 6°](#frlib-per_assurance-r3) |
| `annuity_factor.csv` | Undiscounted conversion factors by sex and age 55–80, anchored at 22.0000 for a male 64 | **[std]** placeholder; TGH05 / TGF05 cited and not shipped [R12] [REG-R21] |

**What is deliberately not in a file.** The charge levels — the entry loading, the two
management charges, the arbitrage rate, the *frais d'arrérages* — are `Projection`
References. The *encadré* requires maxima to be disclosed and caps nothing [REG-R30], and
the sampled range is wide: entry loadings 0 % to 4.80 %, euro management charges 0.50 % to
2.30 % [S1]–[S8]. Every adopted level is a standardization, and putting them where a reader
trips over them is better than filing them in a table that looks like data.

## Sign convention

`liability_cf(t)` is the technical notes' orientation, **outgo-positive**: claims, plus the
capital handed to `Rente_FR_S`, plus expenses, less *versements*. `net_cf(t)` is exactly
its negative, **income-positive**, which is the house sign across the library, so
`result_cf()["net_cf"]` can be summed alongside any other model's without checking which
product it came from. `test_both_signs_of_the_net_flow_are_published` asserts the two are
negatives to 1e-9 and that the outgo columns rebuild `liability_cf`.

A contributing plan is cash-positive in every year but the settlement one, where the whole
account value leaves at once.

`annuity_conversion` is an **outgo**, not a memo item: where the annuity is not commuted
the converted capital leaves this projection. It and `commuted_pp` are mutually exclusive
by construction, and only one of them is ever non-zero on a cell.

## Naming

Cells names follow `basiclife.BasicTerm_S` and `savings.CashValue_SE` wherever those
models have an analogue. Six needed care, and the in-force count needed two entries
because the notes and the library index it at opposite ends of the year.

| Notes symbol | Cells | Why it needed care |
|---|---|---|
| `lapse_rate` | **does not exist** | There is no surrender right [R3 L. 224-4](#frlib-per_assurance-r3) [S2] [S3] [S4] [S7]. `early_release_rate` and `transfer_out_rate` are named for the events they are, and `claims_early_release` and `claims_transfer` for the amounts they pay |
| `l(t−1)` | `pols_if(t)` | The count the year **opens** with, `pols_if(1) = 1`, and the weight on that same `result_cf()` row. This is the library's settled convention, shared with `MYGA_US_S` and `WP_UK_A`: divide a flow by its own row's `pols_if` and you get a per-policy amount for the same period |
| `l(t)` | `pols_if_at(t, "AFT_DECR")` | The count the year **ends** with — the notes' own indexing, and the column their worked-example table prints. It is published as the `pols_if_eoy` column of `result_state()` and it is one period ahead of `pols_if`: `pols_if_at(t, "AFT_DECR") == pols_if(t + 1)`. It carried the bare name `pols_if` in an earlier draft, which put the next period's exposure on every cash flow row — silently, since nothing raised — and the rename is what fixed it. `pols_if_at` also exposes the two intermediate steps, `"BEF_RELEASE"` and `"BEF_TRANSFER"` |
| `m(t)` | `switch_pp(t)` | **Signed**, because the sign decides which support bears the arbitrage charge. Positive on the ordinary de-risking switch; negative where a cell arrives above the grid's minimum |
| `a_x` | `annuity_factor()` | An **undiscounted expected-instalment count**, not a discounted annuity factor [R9 A. 142-1](#frlib-per_assurance-r9). Named for what it is so nothing discounts it twice |
| `A(t)` | `av_pp(t)` | **Per policy**, and published as a `result_cf()` column beside aggregate flows so that the difference is visible. `av_at(t, timing)` is the in-force weighted quantity, and no cash flow reads it: every claim is already a decrement times a per-policy amount |

`claims(t, kind)` takes `"DEATH"`, `"EARLY_RELEASE"`, `"TRANSFER"` and `"MATURITY"`, and
the `result_cf()` columns are named for the `kind` that produces them. There is no
`claims` subtotal column beside them.

## Standardizations used

Everything in this list is **[std]**: the annual projection frequency and the annual
rebalancing; the BOY *versement* and rebalancing, EOY crediting, charge, decrement and
benefit ordering; the glide-path band edges and realising "low risk" wholly as the euro
support; taking the arbitrage charge from the source support and allocating the
*versement* at the target mix; the entry loading of 2.50 %, the euro and UC management
charges of 0.70 %, the arbitrage rate of 0.30 % and the *frais d'arrérages* of 1.50 %; the
UC gross return of 5.00 % and the euro-fund gross asset return of 3.38 %, which has a
source for its 2025 level [S9] but none for carrying it flat over twelve years; the whole
mortality table, its anchored level and the
`mort_be_factor` of 0.85, and the flat 0.00500 placeholder the worked example runs on; the
early-release rate of 1.60 %, the transfer-out rate of 1.00 % and the reduced c3 release
rate; the ordered dependent-decrement convention; folding the *garantie plancher* charge
into the management charge; the annuity factor ladder and its 22.0000 anchor; the annuity
election of 30 % and deterministic commutation whenever the test passes; maintenance
expense of €30 a plan a year inflating at 1.80 %; settling staged capital at the horizon;
and carrying no PPB stock, no partial early release, no 15 % transfer-value reduction and
no profile or horizon change.

## Tests

`tests/test_per_assurance_fr.py` asserts every row of the notes' worked example to the
cent and `l(t)` to six decimals, the settlement table and the commutation identity, and
then one test per listed modelling pitfall — the glide-path band edge, the *versement*
that is not a switch, the source-charging convention and the reverse-switch bound, the
minimum binding at the rebalancing date, the floor identity and the two cells where the
floor bites and where it ceases, the absence of lapse machinery, the transfer indemnity
window measured from the first *versement*, the three decrements not double-counting, the
undiscounted conversion factor, the monthly commutation threshold and its cliff, the
per-policy against aggregate distinction, and the projection stopping at the horizon with
tax outside it. It asserts the exposure convention separately and over every model point,
because breaking it is silent: `result_cf()` has to open at `pols_if_init()`, each row's
`pols_if` has to be the count that row opens with, and the notes' `l(t)` has to sit one
period ahead of it at `pols_if_at(t, "AFT_DECR")`. It also asserts that a compartment-3
cell electing capital raises, that a contradictory `annuity_share` raises, that the glide
path can be swapped without touching a formula, and that the model round-trips.

```bash
python -m pytest lifelib/libraries/frlib/tests/test_per_assurance_fr.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-per_assurance-r10
[R12]: #frlib-per_assurance-r12
[R15]: #frlib-per_assurance-r15
[R19]: #frlib-per_assurance-r19
[R20]: #frlib-per_assurance-r20
[R21]: #frlib-per_assurance-r21
[R22]: #frlib-per_assurance-r22
[R3]: #frlib-per_assurance-r3
[R7]: #frlib-per_assurance-r7
[REG-R16]: #frlib-reg-r16
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R30]: #frlib-reg-r30
[REG-R41]: #frlib-reg-r41
[std]: #frlib-std
<!-- END generated citation links -->
