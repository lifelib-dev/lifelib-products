# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/assurance_vie_euro/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The mechanics
> are sourced — the art. A132-11 allocation and which limb attaches to which account [R5]
> [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15], the art. A132-12 minimum benefit [R5] [REG-R15], the eight-year
> PPB release horizon [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6] [REG-R16], the `effet cliquet` [S1] [S9],
> the `garantie nette` capital floor and its measurement before levies [S3] [S5] [S6]
> [S7], the death benefit being the `épargne acquise` and nothing more [S3], the absence
> of a `frais de rachat` [S2] [S3] [S10] [S13], and the annual timing of the `prélèvements
> sociaux` on euro-denominated rights [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9). Every **rate** is a **[std]**
> standardization: no insurer publishes its dotation or release policy [R5] [REG-R16], no
> French euro-fund lapse experience is public [R15], no contract in the source set
> publishes a TMG [S1] [S2] [S3] [S4] [S11], and the statutory mortality tables annexed to
> the arrêté du 1er août 2006 [REG-R23] are cited but not redistributed — the shipped
> table is an INSEE-shaped proxy [REG-R24].

## Run it

```bash
python products/assurance_vie_euro/run.py            # the worked example's anchor cell
python products/assurance_vie_euro/run.py 7          # the same cell, low scenario
python products/assurance_vie_euro/run.py 8          # the high scenario, PPB building
```

```python
import modelx as mx
model = mx.read_model("products/assurance_vie_euro/Euro_FR_A")
model.Projection[1].result_cf()
```

`result_pb()` gives the crediting machinery — the `compte de participation aux résultats`,
the statutory floor rate it implies, the PPB dotation, release and balance, and the
`taux servi` credited. `result_cf()` gives the cash flows.

## The rate is an allocation, not an assumption

That sentence is the model.

```
fin_acct_pp(t)           = r_fin(t)·(pm_avg_pp(t) + ppb_pp(t))
tech_acct_pp(t)          = fee_pp(t) − expenses_pp(t)
insurer_tech_share_pp(t) = max(0.10·max(tech_acct_pp(t), 0), 0.045·prem_gross_pp(t))
pb_acct_pp(t)            = 0.85·fin_acct_pp(t) + tech_acct_pp(t) − insurer_tech_share_pp(t)
pb_min_pp(t)             = max(0, pb_acct_pp(t) − tmg_rate()·pm_avg_pp(t))
```

Every year the insurer builds the account art. A132-11 prescribes, and the whole of that
balance must reach policyholders [R5] [REG-R15]. What the insurer chooses is only *when*:
what it does not credit this year is carried to the `provision pour participation aux
bénéfices`, and what it carried in an earlier year it may credit now. Four points of
substance, each a listed pitfall in the notes:

| | The rule | The popular error |
|---|---|---|
| Which percentage, which account | 85% of the `compte financier`; the `compte technique` less the insurer's share [R5, art. A132-11](#frlib-assurance_vie_euro-r5) | "90% of the financial account and 85% of the technical result" — EUR 3,319.09 against the correct EUR 3,071.86 in worked-example year 1 |
| The insurer's technical share | The **greater** of 10% of the credit balance and 4.5% of annual premiums | Dropping the premiums limb — EUR 108.00 against EUR 28.43 in year 6 |
| The financial base | `pm_avg_pp + ppb_pp`, because art. A132-14 works on average technical provisions [REG-R15] and the PPB is one of them [REG-R6] | Omitting the PPB (−EUR 41.81 in year 6), or accreting the vintages as well, which pays its return twice |
| The charge | Subtracted **once**, between the PB amount and the rate | `av × (1 + ts_net) × (1 − c)`, which costs the policyholder 0.60% a year that was already taken [R14] |

Then the three levers on one rate:

```
pb_target_pp(t)     = ts_target()·pm_avg_pp(t) + fee_pp(t)
ppb_dotation_pp(t)  = max(0, pb_min_pp(t) − pb_target_pp(t))
ppb_discr_rel_pp(t) = min(max(0, pb_target_pp(t) − pb_min_pp(t)), ppb_pp(t))
ppb_forced_pp(t)    = Σ_v { ppb_vintage_pp(t, v) : v + 8 ≤ t }
ppb_release_pp(t)   = max(ppb_discr_rel_pp(t), ppb_forced_pp(t))
pb_credited_pp(t)   = pb_min_pp(t) − ppb_dotation_pp(t) + ppb_release_pp(t)
ts_net(t)           = max(tmg_rate(), ts_raw(t))
```

A dotation and a forced release **coexist** in the worked example's first three rows —
this year's excess goes in while an eight-year-old vintage comes out — and where the
forced release wins the credited rate goes *above* the target: year 6 wants EUR 426.99 and
must release EUR 500.00, so it credits 2.3589% against a 2.30% target.

Note what the invariant is not. `ts_net(t) ≥ ts_stat(t)` is **not** an invariant: a dotation
year credits less than the statutory floor rate and that is legal, because the balance goes
to the PPB and not to the insurer [R5] — model point 5, which opens with no PPB, does
exactly that in year 1. `check_pb_allocation()` therefore states an allocation identity,
`I(t) + F(t) + D(t) − R(t) − A⁺(t) − topup(t) = 0`, not a rate inequality.

## The PPB vintage ledger, and why it is a ledger

A dotation carried to the PPB in financial year `v` must be applied to mathematical
provisions or paid to policyholders **within the eight financial years following** the one
it was carried in [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6, art. A331-9](#frlib-assurance_vie_euro-r6) [REG-R16]. The model therefore
carries `ppb_vintage_pp(t, v)`, a per-vintage balance drawn down FIFO by
`ppb_vintage_release_pp(t, v)`, so `v + 8` is a real deadline on a real balance — a
single-pot PPB with an average age meets the rule on average and breaches it on every one.

The statute prescribes no release order **[std]**. FIFO is the only order that satisfies the
eight-year constraint without slack, and it is what makes the ledger testable: releasing
newest-first would satisfy the aggregate recursion `Q(t+1) = Q(t) + D(t) − R(t)` exactly
while letting an old vintage sit past its deadline behind young ones that keep being spent.
`check_ppb_clock()` catches that; `check_ppb_roll_fwd()` cannot. The two are deliberately
separate recursions — `ppb_pp(t)` runs the aggregate, `ppb_ledger_pp(t)` sums the vintages
— because nothing forces them to agree, and an off-by-one in the FIFO draw breaks the tie
while leaving both numbers plausible. The anchor cell's clock closes exactly:

| Year | Forced | Want, uncapped | Discretionary | Released | Drawn from |
|---|---|---|---|---|---|
| 1–3 | 500.00 | −137.06 → −32.52 | 0.00 | 500.00 | vintages −7 … −5, one a year |
| 4–6 | 500.00 | 77.81 → 426.99 | 77.81 → 426.99 | 500.00 | vintages −4 … −2, one a year |
| 7 | 500.00 | 606.30 | 606.30 | **606.30** | 500.00 from vintage −1, then 106.30 from vintage 0 |
| 8 | 393.70 | 736.57 | **650.58** | **650.58** | 393.70 from vintage 0, then the three dotations |
| 9–12 | 0.00 | 869.58 → 1,059.09 | 0.00 | 0.00 | the PPB is exhausted; `ts_net = ts_stat` |

The two middle columns are the two halves of `ppb_discr_rel_pp(t) = min(max(0,
pb_target_pp(t) − pb_min_pp(t)), ppb_pp(t))`. "Want, uncapped" is the raw difference
`s* B(t) + F(t) − A⁺(t)`; "Discretionary" is that difference floored at zero and capped
at the balance. They separate exactly twice on this cell and for different reasons — in
years 1–3 the want is *negative*, which is what a dotation year is (the three dotations
named below are its mirror image), and from year 8 the *cap* binds, partially and then
to nothing. Neither is the release: year 7 wants 606.30 and gets it, year 6 wants 426.99
and must release 500.00 because the clock outranks the target.

Twelve-year releases of EUR 4,256.88 against an opening EUR 4,000.00 plus three dotations
(137.06, 87.30, 32.52) of EUR 256.88. The opening balance is split into `ppb_vintages_init`
equal vintages carried in years `0, −1, … , 1 − ppb_vintages_init` **[std]** — a
steady-state construction, since a fund that has run the clock for eight years carries
roughly one eighth of its PPB in each open vintage, and no insurer publishes its own
profile. It matters: model point 6 carries the same EUR 4,000 in **four** vintages, and
nothing is forced out before year 5.

## The `effet cliquet` is not "the account never falls"

What is ratcheted is **credited PB**, not the balance [S1] [S9]. Under the `garantie
nette` the account falls by the management charge in a nil-PB year, and the minimum
surrender-value tables insurers publish for exactly that case prove it: Suravenir's
994.00 … 952.99 is `1 000 × (1 − 0.006)ⁿ` truncated to the cent [S3], and MACSF's
965.15 … 955.52 is `970 × 0.995ⁿ` [S2]. Conflating the two is a pitfall, so the model
publishes two separate checks:

- `check_cliquet()` — `pb_cum_pp` is non-decreasing, `int_credited_pp(t) ≥ 0` and
  `ts_net(t) ≥ tmg_rate()`. **Half of this is zero by construction**, because the
  `max(tmg_rate(), …)` in `ts_net` enforces the non-negativity; it is published because the
  constraint is a contractual fact, and a re-implementation that netted the charge against
  the revalorisation, or carried a negative `pb_acct_pp` through to the account, would break
  it. The ratchet half compares two independent recursions and is not by construction.
- `check_guar_floor()` — the weaker and correct statement about the balance,
  `av_pp(t) + soc_levy_cum_pp(t) ≥ guar_floor_pp(t)`: a genuine inequality that nothing in
  the recursions enforces, measured **before** cumulative social levies because the
  published minimum surrender-value tables are [S1] [S2] [S3]. On the anchor cell it reaches
  EUR 99,061.85 at `t = 13` against EUR 139,600.82 — it never binds on a path with a
  positive `taux servi`, and knowing that it does not bind is the reason to check it.

## `Prélèvements sociaux` are inside the account and outside `net_cf`

The 17.2% levy [S3] is withheld **as the interest is credited**, every year, whether or
not anything is withdrawn, because the rights are expressed in euros; only the UC part is
deferred to `dénouement` [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9). This is the euro fund's signature mechanic
and the commonest foreign-model error. It sits **inside the account roll-forward**,
because it is money that genuinely leaves the contract each year and a model that defers
it to surrender overstates the account and every benefit measured on it — and **outside
`net_cf`**, because it is a policyholder tax the insurer withholds and remits to the State
rather than a benefit or an insurer expense. Its own `soc_levy` column lets a fund-level
asset projection add it back in one step.

The base is the interest actually inscribed on the contract, i.e. **net** of the management
charge **[std]**: art. L136-7 fixes the timing but not the base [R9], and no retrieved
product document says which it is (product-spec footnote 13). The next error along is
levying it on the *account*: 17.2% of EUR 100,000 is EUR 17,200, while 17.2% of
worked-example year 1's EUR 2,827.60 is EUR 486.35.

## Behaviour keys on the gap, not on the level

```
lapse_dyn_add(t) = lapse_dyn_a·max(0, ref_rate(t) − ts_net(t) − lapse_dyn_tol)
lapse_rate(t)    = min(lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t))
```

**The duration-8 step** in `lapse_rate_base` is the tax threshold, not a behavioural
guess: the reduced 7.5% rate and the EUR 4,600 / EUR 9,200 annual allowance both switch on
at eight years [R10] [R11] [REG-R40]. It is indexed by `duration(t) = duration_init + t`,
the **contract's** completed years at the year end, not by `t` — the anchor cell is five
years in, so the step falls in projection year 3, and a model indexing by `t` would put it
five years late.

**The dynamic term** is additive in the gap between the market reference rate and the
`taux servi`, one-sided, and capped. The sign of the relationship is observed rather than
assumed: in 2025 the euro rate was 2.63% while the Livret A averaged 2.20% and fell to 1.7%
in August and 1.5% in February 2026 [R14] [R15], and euro supports turned to a
**+EUR 6.4 bn** net inflow after five consecutive years of net outflow [R15]. The magnitude
has no public calibration, and `lapse_dyn_a = 4.0`, `lapse_dyn_tol = 0.25` point and
`lapse_cap = 30%` are the most consequential **[std]** values in the model. Because the
credited rate and the surrender rate move together, the model carries a feedback loop the
deterministic run samples only once.

## What is out of scope, and why

**No positive-TMG model point is shipped**, and that is a decision rather than an omission.
No contract in the source set publishes a TMG: the two Suravenir notices state no
guaranteed interest rate at all [S3] [S4], BoursoVie names a TMG "annoncé en début d'année"
without its value [S1], MACSF names a board-set art. A132-3 rate without giving it [S2],
and Afer names a `Taux Plancher Garanti` without giving it [S11]. So the composite's TMG is
0.00% **[std]** and every model point carries it.

The lever is implemented as the notes specify, and at `tmg_rate() = 0` the two things the
notes call the TMG coincide: the art. A132-12 subtraction of "interest already credited to
mathematical provisions" [R5] [REG-R15], which belongs to a `taux technique` fixed at
subscription, and the floor on the year's *total* revalorisation, which is what art.
A132-2/A132-3 actually guarantees [R3] [R4] [REG-R18]. Above zero they are different
quantities, and the product specification is explicit that the ACPR's average `taux
technique` of 0.32% must not be substituted for a TMG [R14] (product-spec footnote 7). A
positive-TMG cell would have to choose, so none is shipped and `insurer_topup_pp` — the
cells that would carry the guarantee's cost to the insurer — is nil throughout. Also out of
scope, per the notes:

- **The HCSF surrender-suspension power** under art. L631-2-1 5° ter [R8] [REG-R13]. No
  published trigger a deterministic model could key off, and precisely what would change a
  mass-lapse answer — so a mass-lapse run here is a **pre-management-action** number.
- **The exceptional PPB `reprise`** of art. A132-16-1 [REG-R16], available only on a
  negative life technical account *and* an uncovered SCR: a solvency-stress management
  action, not a projection assumption.
- **`Avances`.** All three insurers push the terms into a separate document that was not
  retrieved [S1] [S2] [S3], so `avance_on()` validates rather than inventing a rate, a
  ceiling and a duration.
- **`Arbitrages` and the UC compartment**, which is the sibling product
  `assurance_vie_uc`; and the **UC-holding bonus**, often 100 bp and sometimes above 200 bp
  [R14], because no retrieved contract publishes its grid.
- **The in-year `pro rata temporis` rate.** Every insurer credits only a floor rate to a
  mid-year `dénouement` [S1] [S2] [S11]; at a nil TMG that is no in-year interest at all.
  The annual grid credits the full year's `taux servi` to exiting policies — generous by up
  to one year's rate, concentrated in the high-lapse years, and said so rather than hidden.

There is **no maturity decrement**: the euro support has no term, and the contract's stated
maturity, where one exists, is renewable annually without limit [S6]. The projection stops
at `proj_len()` and the survivors are paid nothing, because that ending is a modelling
truncation and not a contractual event.

## Inputs are external files

The four input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Euro_FR_A/` holds nothing but formulas:

```
products/assurance_vie_euro/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  fin_rate_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Euro_FR_A/                   <- formulas only
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
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `fin_rate_file` | `fin_rate_table()` | `fin_rate_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points. **Point 1 is the notes' worked example** — M55 at duration 5, EUR 100,000, EUR 2,400 p.a. in, EUR 3,000 p.a. out from year 6, 0.60% charge, 2.30% target, EUR 4,000 PPB in eight vintages. Point 2 is the same cell on the `garantie brute`; 3 targets 2.90%; 4 is paid up; 5 opens with no PPB; 6 carries four vintages instead of eight; 7 and 8 are the low and high scenarios; 9 is a small new-business cell with a 0.50% entry charge and a 0.80% management charge; 10 is a drawdown cell, F82, EUR 250,000 with EUR 6,000 a year out; 11 is point 1 carrying 250 policies | anchor cell **[std]**, product-spec "Anchor model cell"; variants from the notes' pitfalls and sensitivities |
| `mort_table.csv` | Base annual mortality by sex and age 18–120, capped at 1 | **[std]** Makeham proxy shaped like French population mortality [REG-R24], anchored so that the 80% best-estimate factor gives the notes' `q(M, 60) = 0.0060` placeholder exactly — *not* TH00-02/TF00-02 or TGH05/TGF05, which are cited [REG-R23] and not redistributed |
| `lapse_table.csv` | Base annual surrender by completed policy duration: 4% at 1–7, **8% at 8**, 5% at 9+ | levels **[std]**, no public French euro-fund lapse experience [R15]; the duration-8 step is the tax threshold [R10] [R11] [REG-R40] |
| `fin_rate_table.csv` | Three scenarios × 40 years of `r_fin` and `ref_rate`. Base 3.30% → 2.30% over twelve years then level; low 3.00% → 1.40%; high 4.00% level. `ref_rate` 2.20% throughout | **[std]** scenarios anchored to the ACPR's `taux de rendement de l'actif` — 2.8% in 2025, half of undertakings between 2.4% and 3.3% [R14] — and the 2025 average Livret A [R14]. Not forecasts |

Note what is **not** in a file. The crediting rule that actually drives this product — the
target `taux servi`, the dotation and release policy, the FIFO order, the expense loadings,
the dynamic-surrender coefficients — lives in model point columns and `Projection`
References rather than in a rate table. That is not an oversight: **none of it is
published.** Only the outer bounds of the discretion are public — at least 85% of the
`compte financier` and the A132-11 technical share must reach policyholders [R5], and the
PPB must be released within eight years [REG-R16] — and between those bounds every value is
a standardization. Putting them where a reader trips over them is better than filing them
in a table that looks like data. Each rate table does carry a `provenance` column saying in
words what its numbers are; no formula reads it, and it is there so a file lifted out of
this directory still says what it is.

## The worked example

`tests/test_assurance_vie_euro_fr.py` asserts every row of both tables to the cent and
every rate to the fourth decimal of a percentage. The year-6 trace, where every lever is
active at once:

| Step | Value |
|---|---|
| `pm_avg_pp` = 124,354.884701 + 1,200 − 1,500 | 124,054.884701 |
| `fee_pp` = 0.60% × base | 744.329308 |
| `expenses_pp` = 0.35% × base + 24 × 1.015⁵ | 460.046913 |
| `fin_acct_pp` = 2.80% × (base + 1,756.875780) | 3,522.729293 |
| 85% of it | 2,994.319899 |
| `tech_acct_pp` | 284.282396 |
| `insurer_tech_share_pp` = max(28.428, **108.000**) | 108.000000 |
| `pb_acct_pp` = `pb_min_pp` | 3,170.602295 |
| `ts_stat` | 1.955806% |
| `pb_target_pp` = 2.30% × base + `fee_pp` | 3,597.591656 |
| Discretionary release wanted / vintage falling due | 426.989361 / **500.000000** |
| `pb_credited_pp` | 3,670.602295 |
| **`ts_net`** | **2.358853%** |
| `int_credited_pp` | 2,926.272987 |
| `soc_levy_pp` | 503.318954 |
| `av_pp(7)` | 126,177.838734 |

The `taux servi` from a different direction —
`0.85·fin/base + (technical share)/base − fee_rate + (PPB flow)/base` — gives
`2.413706% + 0.142100% − 0.600000% + 0.403047% = 2.358853%` in year 6, and
`2.082500% + 0.145673% − 0.600000% + 0.000000% = 1.628173%` in year 9 with the PPB
exhausted. The twelve-year account identity: credited interest EUR 31,800.82 and social
levies EUR 5,469.74, whose ratio is `0.172000` exactly, and
`100,000.00 + 28,800.00 − 21,000.00 + 31,800.82 − 5,469.74 = 134,131.08` — the same total
reached the other way from PB credited gross of the charge, EUR 40,538.97, less `frais de
gestion` of EUR 8,738.15.

Read year 9 for what it says. At `r_fin = 2.45%` and a 0.60% charge the most the account
could grow by is 1.85%; the model credits 1.6282%, and the 0.2218-point wedge is exactly
`0.15 × 2.45% = 0.3675%` retained from the `compte financier` less the 0.1457% of the
technical account that flows back [R5, art. A132-11](#frlib-assurance_vie_euro-r5). **A 2.30% target is not payable on a
2.45% asset return without the PPB**, and the model steps down rather than pretending
otherwise. The two management actions that would soften it — realising capital gains into
the year's financial account, and the `réserve de capitalisation` [REG-R6] — are outside it.

## Sign convention

`net_cf` is **income-positive**, the library's convention. `liability_cf` is the notes'
outgo-positive `CF(t)`, published verbatim, and `net_cf(t) == −liability_cf(t)` exactly:
`liability_cf = claims_death + claims_lapse + withdrawals + expenses − premiums`. Two
things are reported beside the flows and are **not** in either: `int_credited`, a state
movement rather than a settlement, and `soc_levy`, a policyholder tax. `withdrawals` is an
**owner election, not a claim** — money the policyholder asked for out of a balance the
policyholder owns — while a `rachat total` ends the contract and appears as
`claims_lapse`. Both leave the fund; keeping them apart is what lets a reader see the
difference between elective drawdown and exit.

## Naming

Most names carry across from the notes unchanged; these needed care.

| Notes symbol | Cells | Why |
|---|---|---|
| `B(t)` | `pm_avg_pp(t)` | Not an average of anything the model computes: it is `AV(t) + 0.5·P(t) − 0.5·W(t)`, an assumption about *when* money moved. `av_avg_pp` would suggest it came out of `av_pp_at` |
| `ŝ(t)`, `σ(t)` | `ts_stat(t)`, `ts_net(t)` | Both are **net of the management charge**. `pb_min_pp` is gross of it, and the charge is subtracted once, on the way from a PB amount to a rate |
| (the `max`) | `ts_raw(t)`, `insurer_topup_pp(t)` | The two halves of `max(g, ·)`: what the allocation produces, and what the guarantee costs the insurer in euros when it cannot |
| `Q_v(t)` | `ppb_vintage_pp(t, v)`, `ppb_vintage_release_pp(t, v)`, `ppb_ledger_pp(t)` | The ledger, the FIFO draw and the ledger's total — the last computed independently of `ppb_pp` so that the check compares two things |
| `W(t)` | `withdrawals_pp(t)` / `withdrawals(t)` | An owner election; `wd_prog_pp()` is the *elected* amount before the start year and the balance cap apply |
| `claims(t, "LAPSE")` | `claims_lapse` | Named for the `kind` argument that produces it, and for the library's `pols_lapse` decrement — not `claims_surr` |
| `d + t` | `duration(t)` | The contract's completed years at the year end, which is what the tax threshold and the lapse table are keyed to — distinct from `t`, the projection year |

## Standardizations used

Everything in this list is **[std]**: the 2.30% target `taux servi` and holding it level;
the crediting rule itself — dotation of the excess over the target, discretionary release
up to the target, FIFO order, no year-on-year cap on the rate; the per-policy attribution
of a collective PPB and its split into eight equal vintages; the 0.60% management charge
level and the `pro rata temporis` charge base; the nil TMG and nil entry charge on the
composite; the `garantie nette` as the composite's guarantee form and its seeding at
`av_pp_init` for an in-force cell; the annual grid, the 0.5 weight on in-year movements and
the full year's credit to a mid-year exit; the levy base being interest net of the charge;
the mortality table, the 80% best-estimate factor and age last birthday; the lapse levels
and all three dynamic-surrender parameters; expenses of EUR 24 a policy a year inflating at
1.5% plus 0.35% of the average balance; the three financial scenarios; `proj_len() = 40`;
death before surrender as the processing order; and no `avance` take-up, no UC-holding
bonus and no PPB accretion on the vintages.

## Tests

`tests/test_assurance_vie_euro_fr.py` asserts both tables of the worked example row by row,
the year-6 trace at full precision, the `taux servi` decomposition from the other
direction, the twelve-year levy and account identities, the aggregate roll-forward, the
guarantee floor and the decrement extract — then one test per pitfall the notes list: the
charge deducted twice, the closing-balance crediting base, the statutory split reversed,
the 4.5%-of-premiums limb dropped, the PPB left out of the financial base or accreted, a
LIFO release or an overdue vintage, the statutory minimum lost rather than allocated, the
levy deferred to surrender or struck on the account, the cliquet tested as "the account
never falls", a death-benefit uplift, and the mid-year exit taking a full year's rate. Then
the variants each shipped model point carries, and all seven invariant checks on every one
of the eleven.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-assurance_vie_euro-r10
[R11]: #frlib-assurance_vie_euro-r11
[R14]: #frlib-assurance_vie_euro-r14
[R15]: #frlib-assurance_vie_euro-r15
[R3]: #frlib-assurance_vie_euro-r3
[R4]: #frlib-assurance_vie_euro-r4
[R5]: #frlib-assurance_vie_euro-r5
[R6]: #frlib-assurance_vie_euro-r6
[R8]: #frlib-assurance_vie_euro-r8
[R9]: #frlib-assurance_vie_euro-r9
[REG-R13]: #frlib-reg-r13
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R18]: #frlib-reg-r18
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R40]: #frlib-reg-r40
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
<!-- END generated citation links -->
