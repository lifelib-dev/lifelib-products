# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/riester_rente/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md); the sources both rest on
are listed in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced is
> the *statute*: who is *zulageberechtigt* [R7]; the *Grundzulage*, *Kinderzulage* and
> *Berufseinsteiger-Bonus* structure [R9]; the § 86 *Mindesteigenbeitrag* with its 4 % rate,
> 2 100 € ceiling, 60 € *Sockelbeitrag* floor and **proportional** Kürzung [R10]; the ZfA
> payment lag [R11]; the *Beitragserhaltungszusage*, the 30 % *Teilkapitalauszahlung* cap, the
> five-year floor under acquisition-cost spreading and the *Wechselrecht* [R1]; the
> *Kleinbetragsrenten-Abfindung* [R15]; and the consequences of a *Kündigung* [R14]. What is
> **not** sourced is everything a carrier chooses: **no carrier-specific parameter was
> established for any German Riester product, at any house, for any year** [S4] [S5] [S6] [S7]
> [S8] [S16] — no *Rechnungszins*, no declared rate, no charge, no *Rentenfaktor*, no
> *Stornoquote* — so each of those is a **[std]** standardization, and the DAV tables the
> decrements stand in for (DAV 2008 T, DAV 2004 R) are the property of the Deutsche
> Aktuarvereinigung, are not public, and are cited by name rather than shipped [REG-R47]
> [REG-R48] [REG-R49]. Replace the charge, surplus and decrement tables with company data
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/riester_rente/run.py
python products/riester_rente/run.py 11     # the cell on which the guarantee binds
python products/riester_rente/run.py 5      # the cell that commutes rather than annuitising
```
Three lines to the same thing:
```python
import modelx as mx
model = mx.read_model("products/riester_rente/Riester_DE_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell — a female
life aged 50 at the 1 January 2027 valuation date, three contract years in force, *Rentenbeginn*
at 67, one child born in 2010. `result_cf()` returns a `DataFrame` indexed by policy year `t`,
`1 … 61`, with fifteen columns; `result_acct()` puts the account, the guarantee accumulator and
the subsidy chain beside it. `model.doc` describes the product and its two phases,
`model.Projection.doc` maps the notes' symbols to the cells names, and `model.Data.doc` says
what each input file is and what a replacement must preserve.

## The Zulage is a contribution, and it arrives a year late

The *Zulage* is paid by the *Zentrale Zulagenstelle für Altersvermögen* to the **provider**,
credited to the contract, counted in the *Beitragsgarantie*, invested, and taxed at the end
like any other contribution [R8] [R11]; it never reaches the saver's bank account. So `zulagen`
is a positive income column of `result_cf()`, published **beside** `premiums` and never folded
into it: on model point 5 the state pays 1 926,26 € against the saver's 609,80 € over the whole
projection — 76 % of the contribution — and a statement that netted the two could not say so.

Three cells carry the subsidy and they are three different amounts, 175,00 €, 175,00 € and
475,00 € on the anchor at `t = 3`: `zulage_entitlement_pp(t)`, the full § 84/85 entitlement of
contribution year `t` [R9]; `zulage_granted_pp(t)`, the same after the § 86 **proportional**
Kürzung [R10]; and `zulage_pp(t)`, the cash **credited** in `t`, which is
`zulage_granted_pp(t − 1)` because the ZfA pays in arrear [R11].

**There are two lags and they are different lags.** `income_ref(t)` looks back one *calendar*
year, because § 86 strikes the minimum on the previous year's earnings; `zulage_pp(t)` looks
back one *projection* year, because the ZfA pays in arrear. One offset applied twice
reproduces neither. The consequence is in the anchor's frame: between `t = 3` and `t = 4`
`zulagen` falls from 455,13 € to 164,93 € while `premiums` **rises** from 1 507,08 € to
1 515,34 €, because the § 86 minimum is 4 % of income *less the entitlement* — a Zulage that
stops is a contribution the saver must make good.

`zulage_pp(t_conv())` is **not** zero: contributions stop at `t_conv() − 1` and the Zulage they
earned lands in the conversion year — 134,33 € on the anchor at `t = 18` — where it is
credited, guaranteed and converted before the guarantee is tested. `check_zulage_lag()` pins
all three cases. The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* top-up have **no
cells and no column** [R6]: only the Zulage reaches the policy, the § 10a advantage being a
personal tax refund, and modelling it here would credit the contract with money that never
arrives.

## The 100 % Beitragsgarantie, and the one moment it is tested

`guar_pp(t)` accumulates **contributions** — the *Eigenbeitrag*, the Zulagen credited, and any
unsubsidised contribution — less the biometric carve-out, and never accrues interest, the
*Beitragserhaltungszusage* being nominal [R1]:

```
G(t+1) = G(t) + E(t) + Z(t) + contrib_extra_pp − κ(t)
κ(t)   = min(rider_prem_pp, 0.20 · (E + Z + extra + rider))
```

It counts Zulagen **credited**, in the year they are credited, not entitlements in the year
they are earned; it counts **unsubsidised** contributions, because the undertaking is on the
*Altersvorsorgebeiträge* paid in and does not distinguish the tax pools [R1] — on model
point 8 it steps by 3 000,00 € a year against an entitlement stuck at 175,00 €; and the
carve-out is **capped**, so model point 9's 400,00 € rider premium on a 1 200,00 €
contribution carves out `0.20 × 1 200,00 = 240,00 €` and no more [REG-R43].

**The guarantee is tested exactly once, at `t_conv()`**, where `capital_conv_pp()` is
`max(account_conv_pp(), guar_pp(t_conv() + 1))`. On model point 11 — a seven-year deferral on
the `low` declared-rate path — the account reaches 20 481,72 € against a 21 000,00 € guarantee,
so **`garantieluecke_conv_pp() = 518,28 €`**, 2,5 % of the capital, funded out of the insurer's
own resources: the product's signature output, and a Riester model on which it is never
positive has demonstrated nothing.

`garantieluecke_pp(t)` is published at every `t` and is a **diagnostic**: the anchor opens
358,94 € under water, peaks at 567,69 € and closes at `t = 7`, the normal state of a charged
contract. `db_pp`, `cv_pp` and `transfer_value_pp` are deliberately **not** floored at it —
the guarantee is a promise about *Rentenbeginn*, not about a policy that leaves before it.
Whether the *Schlussüberschussanteil* and *Bewertungsreserven* share may close a shortfall is
unsettled (gap 9); counting them, as `account_conv_pp()` does, is the provider-favourable
reading, and on the anchor's own deferral at the `low` rate that choice is the difference
between a *Garantielücke* of zero and one of 506,56 €.

## The account is two balances and one credited rate

`dk_pp` is the *Deckungskapital*, `surplus_acct_pp` the *Überschussguthaben*, `av_total_pp` their
sum. The split is **guarantee accounting, not two investment strategies**: the whole account
grows at the declared `j(t)` and `D` is carved out of it as the part `i` guarantees.

```
int_guar_pp(t)     = i · (D(t) + S(t))
int_surplus_pp(t)  = (j(t) − i) · (D(t) + S(t)) + j(t) · U(t)
int_credited_pp(t) = j(t) · (D(t) + S(t) + U(t))      exactly
```

**`j` already includes `i`** [REG-R53]. Adding the declared rate to the guaranteed one is the
German arithmetic error this arrangement makes impossible; setting `j = i` collapses the
*Deckungskapital* leg of `int_surplus_pp` to zero, which is the check that they are not being
added. `int_credited` is a `result_cf()` column and is **reported, not summed into `net_cf`**:
it moves money inside the account, not across the insurer's boundary, and on the anchor it
totals 7 544,45 € — adding it would report the cell's undiscounted deficit as 282,94 € instead
of 7 827,39 €.

## Charges, and a *Sparbeitrag* that can go negative

The AltZertG requires acquisition costs to be spread over **at least five years** [R1] — a
tighter cap on *Zillmerung* than anything the VVG imposes on a Schicht-3 contract. So
`acq_charge_pp(t)` is one fifth of `acq_charge_rate × beitragssumme` in contract years 1 to 5
and zero after: on the anchor, 168,00 € in projection years 1 and 2 and nothing from year 3.
It never appears in `result_cf()`, being a deduction *before* the account, but 168,00 € of the
488,90 € rise in the *Sparbeitrag* between `t = 2` and `t = 3` is the charge ending rather
than the contribution rising.

The charge runs **whether or not contributions are paid**: on model point 10, *beitragsfrei*
from `t = 4`, `prem_to_av_pp(4) = 175,00 − 168,00 − 19,00 = −12,00 €` and the
*Deckungskapital* falls — the cost-spreading rule, not a modelling artefact, and the reason
`prem_to_av_pp` is documented as possibly negative rather than clamped at zero.

The *Ratenzuschlag* is a **charge and never a credit**: the saver pays `E(t) × φ`, only `E(t)`
reaches the *Sparbeitrag* base and the guarantee, `contrib_total_pp` is the cash **received**
and so carries the loading, and `admin_charge_pp` deducts it straight back out while striking
its percentage on the **unloaded** `E + Z + extra`. Deducting it in both places — which the
notes' drafted `S = C − K_a − K_v` with an unloaded `C` did — makes the *Sparbeitrag* fall with
the payment frequency, the opposite of the product fact.

## Conversion: the *Rentenfaktor*, the lump sum and the *Kleinbetragsrente*

```
ä    = Σ_{k ≥ 0} v^k · k p(x(T), τ(T)) − 11/24        first-order basis, factor 1.00
R_c  = (1 − rentenfaktor_margin) · 10 000 / (12 · ä)
R    = max(R_g, R_c)
```

On the anchor `ä = 20,87222879` at age 67 in calendar **2044** — the basis is generational, so
the conversion happens on its own conversion year's mortality — and `R_c = 27,947822`,
**below** the guaranteed `R_g = 29,00`, so the guaranteed factor applies. The two are
independent, one a contract term struck at inception and the other a function of the shipped
table, and the model states which is authoritative rather than leaving it to be inferred. The
whole payout loading sits in `rentenfaktor_margin` (30 % **[std]**) rather than being split
between the factor and each instalment, which would double-count; payout administration is an
explicit `expense_annuity` flow instead. `check_conversion()` asserts
`rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000` on every model
point, whether or not the current factor applies. `teilkapital_pp()` is the elected share
clamped at the statutory 30 % [R1]: 13 726,91 € on the anchor, leaving 32 029,47 € to annuitise
at 92,885458 € a month.

**The *Kleinbetragsrente* commutation is computed, not assumed.** `is_kleinbetrag()` tests
the annuity the model has actually produced, so the commutation rate on a book is an
**output** — which, given how much of the German book runs at the *Sockelbeitrag*, is the
right way round. Two standardizations sit inside it: the test is applied to the annuity
payable **after** the elected lump sum, which trips less often (gap 7), and the 39,55 €
threshold is held **flat in nominal terms** while the *Bezugsgröße* is reset annually, which
on a long deferral **understates** the commutation rate. Model points 4, 5, 10 and 13
commute. A commuted contract pays `claims_commutation` and **no** `claims_lumpsum` and **no**
`claims_annuity` — an *Abfindung* is the whole capital in one payment — and `pols_if` is zero
from `t_conv() + 1` because it discharges the contract outright.

## The payout phase, and the *Rentengarantiezeit*

The projection does not stop at *Rentenbeginn*: the account is extinguished there and the
lifelong *Leibrente* runs to `omega_age = 110` on the **second-order** generational annuitant
basis, because a model that stopped at conversion would not have modelled the benefit the
AltZertG requires [R1]. The *Rentengarantiezeit* changes **who is paid**, never **how much**:
`pols_annuity_pay(t)` is `pols_conv()` while `t − t_conv() < rentengarantie_years()` and
`pols_if(t)` afterwards, and `annuity_pp(t)` does not read `rentengarantie_years()` at all.

| t | 18 | 19 | … | 27 | 28 | 29 |
|---|---|---|---|---|---|---|
| `pols_if` | 0.767588 | 0.762677 | … | 0.701403 | 0.690013 | 0.677530 |
| `pols_annuity_pay` | 0.767588 | 0.767588 | … | 0.767588 | 0.690013 | 0.677530 |
| `claims_annuity` | 855,57 | 855,57 | … | 855,57 | 769,11 | 755,19 |

`claims_annuity` is **exactly 855,57 € in each of those ten years** although a tenth of the
annuitants have died; model point 12 carries no guarantee period and pays the same annuity per
policy to a smaller count. The one genuinely sub-annual element is compressed: the *Leibrente*
is paid as twelve instalments in one amount at the start of the payout year, to those alive at
the start, which overstates by roughly `½ · q(x) · 12R` for a life dying during the year — about
0,7 % at attained age 70 — while the *level* stays right, the factor carrying the Woolhouse
`−11/24` correction. `products/sofortrente/` runs monthly for exactly this reason.

## Four exits, and why a transfer is not a surrender

| Cells | Decrement | Benefit | Charge retained |
|---|---|---|---|
| `pols_death(t)` | `q(t)` | `db_pp(t) = A(t + 1)`, gross | none |
| `pols_lapse(t)` | `w(t)` on the survivors of mortality | `cv_pp(t) = 0.98 · A(t + 1)` | the 2 % *Stornoabzug* |
| `pols_transfer(t)` | `θ(t)` on the survivors of both | `max(0, A(t + 1) − 50,00 €)` | the flat 50,00 € |
| the commuted cohort at `t_conv()` | — | `commutation_pp()`, the whole capital | none |

A *Kündigung* and an *Anbieterwechsel* are **separate decrements, not two spellings of one**. The
transfer pays the full account less a flat charge with no *Stornoabzug* and carries none of the
*schädliche Verwendung* consequences a surrender does [R1] [R14], so `transfer_rate` sits
**above** `lapse_rate` at every duration: over the anchor's projection 11,44 % of the cohort
transfers out against 7,67 % that surrenders. Collapsing the two would apply a percentage charge
where a flat one belongs and would attribute a repayment of every Zulage and every § 10a relief
to an exit that has none. `exit_charge_pp(t)` is the residue that makes the account roll forward
exactly — 1,48 € on the anchor at `t = 1`, because the account an exiting policy releases either
leaves as a benefit or stays with the insurer; dropping it leaves exactly that residual in
`check_av_roll_fwd_resid(1)`, the usual way the identity fails.

*Beitragsfreistellung* is **not** a decrement. It is the book's dominant exit [R25] and a
**state change**: `pols_if` is continuous across it, the account keeps rolling, the guarantee
accumulator freezes once the last Zulage has landed, the Zulage stream stops. It is a
per-model-point switch (`bfs_year`) rather than a rate, because a paid-up policy and a
premium-paying one have different account values and different guarantee accumulators from the
moment they diverge, and a scalar projection cannot carry two of each without doubling every
recursion. Model point 10 shows the mechanic on one policy; a book projection needs the cohort
split, and the notes say so under *Key sensitivities*.

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Riester_DE_A/` holds nothing but formulas:

```
products/riester_rente/
  model_point_table.csv  mort_table_accum.csv  annuity_mort_table.csv   <- inputs live here
  lapse_table.csv  zulage_schedule.csv  income_schedule.csv
  surplus_scenario.csv  freq_loading.csv
  run.py  model.md  product-spec.md  technical-notes.md  sources.md
  Riester_DE_A/                <- formulas only
    __init__.py  _system.json
    Data/__init__.py            (reads the CSVs, once per model)
    Projection/__init__.py      (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its inputs beside the model and
reads them at run time — the opposite of `basiclife/BasicTerm_S`, which stores them *inside*
the model through modelx's IOSpec machinery, hence no `_data/` directory and no embedded
values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every policy. They
live instead in an unparameterized **`Data`** Space, reached through `Projection`'s `data`
Reference, so each file is read once per model however many policies are projected — the
conventions suite counts the reads. `Data.input_dir()` resolves the location from
`_model.path.parent` at run time, so the model works wherever the repository sits.

Each file has one string Reference and one reader cells on `Data`, named alike:
`model_point_file` → `model_point_table()`, `mort_accum_file` → `mort_table_accum()`,
`annuity_mort_file` → `annuity_mort_table()`, `lapse_file` → `lapse_table()`, `zulage_file` →
`zulage_schedule()`, `income_file` → `income_schedule()`, `surplus_file` →
`surplus_scenario()` and `freq_loading_file` → `freq_loading()`.

**The trade-off:** the model is not portable on its own — copy `Riester_DE_A/` without the CSVs
and it reads fine, then fails on first evaluation. What you gain is a diff that shows logic
changes only, and an input that can be swapped in place: point `Data.freq_loading_file` at
another same-schema file and the projection follows with no formula change, which is how the
frequency-loading invariance is tested.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points, twenty-six columns. **Point 1 is the worked-example anchor**; 2–13 exercise the at-inception reconciliation, both *Kinderzulage* rates at once, the *Sockelbeitrag* floor, the `fixed` form, the *Berufseinsteiger-Bonus*, the § 86 Kürzung, a second contribution pool, the 20 % carve-out cap, a *Beitragsfreistellung*, a binding *Garantielücke*, a pure lifelong annuity and the statutory earliest *Rentenbeginn* | configuration, and the **one file exempt** from the provenance rule |
| `mort_table_accum.csv` | Accumulation death rates by attained age 16–110 | **[std]** proxy for **DAV 2008 T** [REG-R48], `qx = 0.001500 × 1.10^(age − 50)`, with **no** improvement dimension — on a death cover improvement favours the insurer. **The anchor a replacement must preserve is `qx` at age 50 = 0.001500** |
| `annuity_mort_table.csv` | Annuitant base rates and improvement scale, ages 55–110 | **[std]** **generational** proxy for **DAV 2004 R** [REG-R49]. What a replacement may not drop is that it is two-dimensional. **The anchor is `ann_factor() = 20.87222879`**, which is what puts `rentenfaktor_curr()` below the guaranteed 29,00 |
| `lapse_table.csv` | `lapse_rate` and `transfer_rate` by contract duration 1–60 | **[std]**, and **no observed range exists** (gap 16). Transfer above surrender at every duration, and that ordering is itself the assertion |
| `zulage_schedule.csv` | `unmittelbar`, `n_kinder_pre2008`, `n_kinder_post2008`, `bonus` by schedule id and `t` | [R9] [REG-R42]. Exogenous because *Kindergeld* is a household fact the contract does not observe — the most awkward feature of this product for a per-policy model |
| `income_schedule.csv` | Contribution-liable earnings by schedule id and `t` | **[std]** 2 % nominal growth paths plus a `zero` path for the *mittelbar* eligible spouse. It decides when the 2 100 € ceiling binds |
| `surplus_scenario.csv` | `decl_rate` by scenario id and `t`: `base` 2,30 %, `low` 0,50 % | **[std]**, the **largest single lever in the model** and the least supported (gap 12). The rate **includes** the *Rechnungszins* [REG-R53] |
| `freq_loading.csv` | The *Ratenzuschlag* multiplier by payment frequency | **[std]** 1.0000 / 1.0100 / 1.0200 / 1.0300, a charge and never a credit |

## The identities the model checks

`check_net_cf()` — **delib's first ruling** — is the cash flow statement's own reconciliation,
in one line, on `result_cf()` row `t`:

```
net_cf = premiums + zulagen − claims_death − claims_lapse − claims_transfer
         − claims_lumpsum − claims_commutation − claims_annuity − expenses − commissions
```

Every term is read **from the published frame**, not from the cells behind it, which is what
makes it a reconciliation of what the model publishes rather than a restatement of `net_cf`'s
own expression: a column that is in the frame and not in the total, or in the total twice, or
that has drifted from the kind behind it, leaves a residual here. `int_credited` is
deliberately outside the identity — it moves money inside the account, not across the
insurer's boundary — and adding it is the tempting error, because it is the largest number on
an accumulation row. Five more checks sit beside it, each a `bool` over all `t` with a
`check_*_resid(t)` companion, and the conventions suite calls all six on every model point.

| Check | What it catches |
|---|---|
| `check_av_roll_fwd()` | The account an exit releases not being counted — a *Stornoabzug* looks like income rather than like account released |
| `check_guar_roll_fwd()` | The entitlement added instead of the credit; interest added to a nominal guarantee; the unsubsidised limb dropped; the 20 % carve-out cap not binding |
| `check_pols_roll_fwd()` | A misindexed decrement recursion, and — through a closure identity built by direct summation over the exit cells — a commuted cohort that leaves uncounted |
| `check_conversion()` | The guarantee not applied; the capital not fully disposed of between lump sum, annuity capital and *Abfindung*; a *Rentenfaktor* inconsistent with the annuity basis |
| `check_zulage_lag()` | The two lags collapsed into one, or the final contribution year's Zulage dropped |

## Modules that are off in the base run

Everything the product carries is implemented; the anchor is the plain cell, so the worked
example reproduces while the machinery stays visible and testable.

| Module | Switch | Off value on the anchor | On at |
|---|---|---|---|
| Unsubsidised second contribution pool — enters the account **and** the guarantee while drawing no Zulage [R12] | `contrib_extra_pp` | `0.00` | point 8, 900,00 € |
| Biometric-rider carve-out — capped at 20 % of total contributions [REG-R43]; never a cash flow here | `rider_prem_pp` | `0.00` | point 9, 400,00 € |
| *Beitragsfreistellung* — contribution and Zulage stop, the account rolls on, the acquisition charge keeps biting | `bfs_year` | `0` (never) | point 10, year 4 |
| § 86 proportional Kürzung — halves the contribution and, in proportion, the subsidy [R10] | `contrib_ratio` | `1.00` | point 7, 0.50 |
| *Ratenzuschlag* — raises `premiums` by `E(t)(φ − 1)` and nothing else | `prem_freq` | `annual`, `φ = 1.0000` | points 3, 4, 6, 7, 10, 13 |
| *Berufseinsteiger-Bonus* — the once-in-a-lifetime addition to the *Grundzulage* [R9] | the `bonus` column of `zulage_schedule.csv`, and `zulage_init_pp` | `0` | point 6, 200,00 € inside a 375,00 € opening credit |
| The low declared-rate stress — the only lever deciding whether the guarantee costs anything | `scenario_id` | `base`, 2,30 % | point 11, `low` at 0,50 % |
| *Teilkapitalauszahlung* election, and the *Rentengarantiezeit* that pays on `pols_conv()` rather than `pols_if(t)` — both **on** by default | `teilkapital_share`, `rentengarantie_years` | `0.30`, `10` | point 12, at 0.00 and 0 |

Two Space References are worth naming because a user will want to move them: `zulage_lag = 1`,
the ZfA payment convention and the shortest lag consistent with the statute (gap 6); and
`mort_be_factor = 0.80` beside `annuity_mort_be_factor = 1.15`, which run in **opposite**
directions because the direction of prudence forks by product — a first-order death table
assumes mortality higher than expected, a first-order annuity table lower [REG-R47].

Three constructions in the sources are **not** implemented rather than implemented and switched
off. The *Auszahlungsplan mit Restverrentung* [R1] belongs to the fund and bank chassis;
Wohn-Riester is absent in both limbs — no *Eigenheimbetrag* decrement, no certified *Darlehen*,
no *Wohnförderkonto*, the last because it is a notional tax-bookkeeping account carrying no
cash flow at all [R13]; and there is no surplus in payment, the wedge between the first- and
second-order annuity bases being a *Risikoüberschuss* this model does not distribute.

## Sign convention

`net_cf` is **income positive** — contributions and Zulagen in, the six kinds of benefit,
expenses and commission out — the notes' own orientation and the library-wide sign.
`liability_cf` publishes the same stream outgo-positive, `liability_cf(t) = −net_cf(t)`
exactly, and both are columns of `result_cf()` so the identity is verifiable in the frame. A
Solvency II best estimate is `Σ v(t) × liability_cf(t)` over the relevant risk-free term
structure plus a risk margin [REG-R5] [REG-R6]; nothing in this library discounts.

`expenses` and `commissions` are **separate** columns and `net_cf` subtracts each exactly once —
frlib's reading, where `expenses` was the total and contained the commission, is not the reading
here, because the notes' worked example prints both as parts; `int_credited` is a state movement
and is in neither. The shape to expect is a modest positive `net_cf` every
accumulation year — 1 505,37 € at `t = 1` — then −11 276,67 € in the conversion year as the
*Teilkapitalauszahlung* leaves in one payment, then a long thin annuity tail, for an
undiscounted total of −7 827,39 €.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` where that model has an analogue and
`savings/CashValue_SE` for the account-value chassis: `pols_*` for policy counts, plural nouns
for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an
uppercase `kind`, `pols_if_at(t, timing)` and `av_total_pp_at(t, timing)` for the within-year
reads, `prem_to_av_pp` for the contribution credited to the account. The full symbol map lives
in the `Projection` docstring. Seven cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `Z*(t)`, `Ẑ(t)`, `Z(t)`; `C(t)` | `zulage_entitlement_pp` / `zulage_granted_pp` / `zulage_pp`; `contrib_total_pp` | Three subsidy amounts and the product turns on the difference between them; and the notes' `C` is the contribution *credited* while the cells is the cash **received**, so it carries the *Ratenzuschlag* that `admin_charge_pp` takes back out |
| `S(t)` | `prem_to_av_pp` | The lifelib name for the premium credited to an account value. **May be negative**, which is the point of model point 10 |
| `D`, `U` | `dk_pp` / `surplus_acct_pp` | Guarantee accounting, not two strategies. Kept apart because `check_av_roll_fwd` needs both and because `j ≥ i` is only visible when they are |
| `A(t) = D(t) + U(t)` | `av_total_pp`, `av_total_pp_at`, `av_total_at` | **Not `av_pp`.** Library-wide `av_pp` is the *principal* balance on its own — `RV_DE_A`'s and `Basis_DE_A`'s *Deckungskapital*, `FRV_DE_S`'s *Fondsguthaben* — with the *verzinsliche Ansammlung* beside it as `av_sur_pp`. What this product's death, surrender and transfer benefits are struck on is the **sum** of the two, a third quantity, so it is named apart rather than reusing the column name `RV_DE_A` gives to one half of it |
| `G(t)`, `Λ` | `guar_pp` / `garantieluecke_conv_pp` | An accumulator tested once, and the shortfall it produces. `garantieluecke_pp(t)` is the *running* gap, a diagnostic no benefit reads |
| `l(t)` in payout | `pols_if` / `pols_annuity_pay` | Inside the *Rentengarantiezeit* the instalment is paid on a count that is not the in-force |

Three sister models share a chassis and the names mean the same thing on all of them.
`RV_DE_A`, the *klassische aufgeschobene private Rentenversicherung*, is the same
general-account accumulation and the same conversion at a guaranteed *Rentenfaktor* with none
of the Schicht-2 apparatus, and is the primary home for the `dk_pp` / `surplus_acct_pp`
recursion and for § 169 VVG. `Basis_DE_A` is the Schicht-1 sibling — same *nachgelagerte
Besteuerung*, same annuitisation constraint, no Zulagen, no *Beitragsgarantie*, no lump sum.
`Sofort_DE_S` is the payout contract this model's second phase compresses onto an annual grid.
Two model point columns drive nothing and are carried anyway: `sex`, which is reporting only
because Riester tariffs have been unisex since a 2006 vintage [R23] — its **absence** from
every formula is the assertion worth making — and `issue_age`, which enters only through
`age(1) = issue_age + duration_init`.

## Standardizations used

Everything in this list is **[std]**. The statutory half of this product is not a composite at
all; the carrier half is entirely one, because nothing carrier-specific was established.

| Standardization | Value | Rationale |
|---|---|---|
| Both decrement tables, their slopes and the two best-estimate factors | `qx = 0.001500 × 1.10^(age − 50)` at `mort_be_factor = 0.80`; `qx_base = 0.006000 × 1.115^(age − 65)` with improvement 1,8 % tapering to 0,2 % from base year 2027, at `annuity_mort_be_factor = 1.15` | DAV 2008 T and DAV 2004 R are proprietary and not redistributed [REG-R47] [REG-R48] [REG-R49]. The slopes are placeholders; the generational structure of the second is **not** optional; the anchors a replacement must preserve are `qx` at age 50 = 0.001500 and `ann_factor() = 20.87222879` |
| *Rechnungszins*; *laufende Verzinsung* | 0,25 % on the anchor and 0,90 % on point 3; `base` 2,30 % and `low` 0,50 %, level | The *Höchstrechnungszins* caps the reserving rate, not what a policy may guarantee [REG-R14], and the cap of the vintage is the highest defensible value, which makes the guarantee cheapest. No carrier declaration was established (gap 12); `low` is a stress, not a forecast |
| *Risikoüberschuss* and *Kostenüberschuss*; *Schlussüberschussanteil*; *Bewertungsreserven* share, and counting the last two toward the guarantee | zero; 2,0 % of contributions credited; 1,0 % of the account | The accumulation risk result is nil by construction — the death benefit is the account value, so there is no sum at risk — and no cost result was established; the two terminal levels are unestablished and **whether either may close a shortfall is unsettled** (gap 9), so counting them is the provider-favourable reading |
| Acquisition charge; administration charge **and its base** | 2,5 % of `beitragssumme` over five contract years; 4,0 % of each contribution credited, Zulagen **included**, plus 12,00 € a year | The five-year floor is statutory [R1] and the level is sized so the charge is of the order of one year's contribution. **Whether German tariffs charge the Zulagen is unknown** (gap 14), and on the low-income cells they are the majority of the contribution, so the choice is stated rather than inferred from a formula |
| Frequency loading, as a charge; *Stornoabzug*; transfer charge | 1.0000 / 1.0100 / 1.0200 / 1.0300; 2,0 % of the account; 50,00 € flat | No *Ratenzuschlag* scale was established, and the statutory cap on the transfer charge is unestablished (gap 8) |
| *Rentenfaktor* margin; annuitisation interest; the guaranteed factor; and `max(R_g, R_c)` | 30 %; 1,00 %; 29,00 € per 10 000 € per month | No *Rentenfaktor* at any carrier for any year was established (gap 9); the two-factor construction is documented for Schicht 3 and assumed here |
| *Kleinbetragsrente* threshold and the basis of the test; the one-year Zulage cash lag; 2,0 % p.a. nominal income growth | 39,55 € a month, flat in nominal terms, applied **after** the lump sum | Two irreconcilable readings of the threshold exist [REG-R42] [REG-R46]; the lower is taken, and both choices push toward fewer commutations and a longer-tailed liability (gap 7). [R11] establishes the ZfA arrear but not the month (gap 6), and the growth rate is a round real-plus-inflation number that decides when the 2 100 € ceiling binds |
| Surrender and transfer rates, 0,8 / 0,6 / 0,4 % and 1,2 / 0,9 / 0,6 % by duration band; expenses and commission; the 30 % *Teilkapitalauszahlung* take-up | 30,00 € maintenance inflating at 2,0 %; 24,00 € per annuitant; 80,00 € per claim; 150,00 € + 2,0 % of `beitragssumme` at issue; 2,5 % initial and 1,5 % renewal commission | **No German Riester behavioural rate was established** (gap 16), and the transfer-above-surrender ordering is an argument from the statutory consequences rather than from data. No German insurer publishes a unit cost. The maintenance figure carries the Zulage administration — *Dauerzulageantrag*, annual ZfA exchange, *Leistungsmitteilung* — a real product-specific cost. German commentary reports the lump sum as the usual election, and **gap 10 records that this rests on nothing** |
| Timing, processing and decrement order; the monthly annuity on an annual grid | Contribution and Zulage at the start, interest at the end, decrements after crediting, conversion at the start of `t_conv()`; mortality, then surrender, then transfer; twelve instalments in one payment | No source fixes the ordering inside a period, so it is stated to be compared line by line. The annuity's *level* is right because the factor carries the Woolhouse correction; the timing overstates by about `½ · q(x) · 12R` |
| `omega_age = 110` with `q = 1` there; the opening balances and the model points themselves | — | The omega forces the decrement closure to be exact rather than approximate; the seeds are **[std]**, and the notes record that `guar_pp_init` and the account seeds were struck on different income paths, a 195,08 € discrepancy kept rather than papered over |

The quantities that are **not** standardizations are the statutory ones: the 175,00 € /
185,00 € / 300,00 € Zulagen and the 200,00 € bonus [R9]; the 4 % / 2 100,00 € / 60,00 €
*Mindesteigenbeitrag* arithmetic and the proportional Kürzung [R10]; the one-year ZfA arrear
[R11]; the *Beitragserhaltungszusage* and the 20 % biometric carve-out [R1] [REG-R43]; the
30 % *Teilkapitalauszahlung* cap, the five-year cost-spreading floor, the earliest
*Rentenbeginn* of 62 and the *Wechselrecht* [R1]; and the structural rules — the Zulage as a
contribution, the guarantee tested once, benefits gross of the *Rückzahlungsbetrag*, and
unisex pricing [R23].

## Tests

`tests/test_riester_rente_de.py` asserts every row of the notes' worked-example table to the cent
and `pols_if` to six decimals, the payout phase's selected rows, the full-precision totals over
all sixty-one periods against the four-cent difference a sum of rounded cells gives, the notes'
four independent rebuilds — projection year 1 from the statute up, the conversion year, the
aggregate account roll-forward with its exit charge, and the four-way decrement closure to
1.00000000 — and the two variants, model point 11's binding *Garantielücke* and model point 5's
commuting *Sockelbeitrag* cell.

Beyond that it asserts **one test per numbered modeling pitfall**: the two subsidy lags kept
apart; the final contribution year's Zulage credited at `t_conv()`; the § 86 Kürzung
proportional; the Zulage as a separate positive income column; no *Günstigerprüfung* cells;
both *Kinderzulage* rates at once; the guarantee tested only at *Rentenbeginn* and no benefit
floored at it; the 20 % carve-out cap binding; unsubsidised contributions inside the guarantee;
the declared rate including and not added to the *Rechnungszins*; the frequency loading charged
and never credited; the acquisition charge spread over five contract years and continuing
through a *Beitragsfreistellung*; transfer separated from surrender; *Beitragsfreistellung* as
a state change; two mortality bases in opposite directions with a generational annuity table;
the *Kleinbetragsrente* tested on the post-lump-sum annuity against a flat threshold; the
*Rentengarantiezeit* changing the count and never the amount; and every benefit gross of the
*Rückzahlungsbetrag*. The whole-model-point-table sweep belongs to
`tests/test_model_conventions_de.py`, which owns the library's single sweep.

```bash
python -m pytest lifelib/libraries/delib/tests/test_riester_rente_de.py -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-riester_rente-r1
[R10]: #delib-riester_rente-r10
[R11]: #delib-riester_rente-r11
[R12]: #delib-riester_rente-r12
[R13]: #delib-riester_rente-r13
[R14]: #delib-riester_rente-r14
[R15]: #delib-riester_rente-r15
[R23]: #delib-riester_rente-r23
[R25]: #delib-riester_rente-r25
[R6]: #delib-riester_rente-r6
[R7]: #delib-riester_rente-r7
[R8]: #delib-riester_rente-r8
[R9]: #delib-riester_rente-r9
[REG-R14]: #delib-reg-r14
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R53]: #delib-reg-r53
[REG-R6]: #delib-reg-r6
[std]: #delib-std
<!-- END generated citation links -->
