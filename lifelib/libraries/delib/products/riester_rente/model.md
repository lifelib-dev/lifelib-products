# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/riester_rente/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md); the sources both rest on
are listed in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** What is
> sourced here is the *statute*: who is *zulageberechtigt* [R7], the *Grundzulage*,
> *Kinderzulage* and *Berufseinsteiger-Bonus* structure [R9], the § 86
> *Mindesteigenbeitrag* with its 4 % rate, its 2 100 € ceiling, its 60 € *Sockelbeitrag*
> floor and its **proportional** Kürzung [R10], the ZfA payment lag [R11], the
> *Beitragserhaltungszusage* and the 30 % *Teilkapitalauszahlung* cap [R1], the five-year
> floor under acquisition-cost spreading [R1], the *Wechselrecht* [R1], the
> *Kleinbetragsrenten-Abfindung* [R15] and the *schädliche Verwendung* consequences of a
> *Kündigung* [R14]. What is **not** sourced is everything a carrier chooses. **No
> carrier-specific parameter was established for any German Riester product, at any house,
> for any year** [S4] [S5] [S6] [S7] [S8] [S16] — no *Rechnungszins*, no declared rate, no
> charge, no *Rentenfaktor*, no *Stornoquote* — so every one of those is a **[std]**
> standardization, and the DAV tables the decrements stand in for (DAV 2008 T, DAV 2004 R)
> are the property of the Deutsche Aktuarvereinigung, are not public and are cited by name
> rather than shipped [REG-R47] [REG-R48] [REG-R49]. Replace the charge, surplus and
> decrement tables with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/riester_rente/run.py
python products/riester_rente/run.py 11     # the cell on which the guarantee binds
python products/riester_rente/run.py 5      # the cell that commutes instead of annuitising
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/riester_rente/Riester_DE_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell — a
female life aged 50 at the 1 January 2027 valuation date, three contract years in force,
*Rentenbeginn* at 67, one child born in 2010. `result_cf()` returns a tidy `DataFrame`
indexed by policy year `t`, `1 … 61`, with fifteen columns; `result_acct()` puts the
account, the guarantee accumulator and the subsidy chain beside it, which is the frame the
technical notes' worked example reads its per-policy columns from.

The model and both its Spaces carry docstrings. `model.doc` describes the product, the two
phases and the projection basis; `model.Projection.doc` holds the full mapping between the
technical notes' symbols and the cells names, together with the six names that needed care;
`model.Data.doc` says what each input file is and, for the two decrement tables, what a
replacement must preserve.

## The Zulage is a contribution, and it arrives a year late

This is the thing a reader arriving from `RV_DE_A` or `Term_UK_A` will get wrong, and it is
visible in the cash flows rather than buried in a parameter. The *Zulage* is paid by the
*Zentrale Zulagenstelle für Altersvermögen* to the **provider**, credited to the contract,
counted in the *Beitragsgarantie*, invested, and taxed at the end like any other
contribution [R8] [R11]. It never reaches the saver's bank account. So `zulagen` is a
positive income column of `result_cf()`, published **beside** `premiums` and never folded
into it: on model point 5 the state pays 1 926,26 € against the saver's 609,80 € over the
whole projection — **76 % of the contribution** — and a statement that netted the two could
not say so.

Three cells carry the entitlement and they are three different quantities:

| Cells | On the anchor at `t = 3` | What it is |
|---|---|---|
| `zulage_entitlement_pp(t)` | 175,00 € | The full § 84/85 entitlement of contribution year `t` [R9] |
| `zulage_granted_pp(t)` | 175,00 € | The same after the § 86 **proportional** Kürzung [R10] |
| `zulage_pp(t)` | **475,00 €** | The cash actually **credited** in year `t`, which is `zulage_granted_pp(t − 1)` [R11] |

At `t = 3` the entitlement has already fallen — *Kindergeld* for the child born in 2010
stops after the 2028 contribution year — while the credit has not, because the credit is
last year's grant. The two move a year apart and that is the whole of pitfall 1. **There
are two lags and they are different lags:** `income_ref(t)` looks back one *calendar* year
because § 86 strikes the minimum on the previous year's contribution-liable earnings [R10],
and `zulage_pp(t)` looks back one *projection* year because the ZfA pays in arrear [R11].
An implementation with one offset applied twice reproduces neither.

The consequence is visible in the anchor's own frame. Between `t = 3` and `t = 4` `zulagen`
falls from 455,13 € to 164,93 € while `premiums` **rises** from 1 507,08 € to 1 515,34 €:
the § 86 minimum is 4 % of income *less the entitlement*, so a Zulage that stops is a
contribution the saver must make good. The two lines move in opposite directions for one
reason, and a model that folds them into a single premium shows neither.

`zulage_pp(t_conv())` is **not** zero. Contributions stop at `t_conv() − 1`; the Zulage they
earned lands in the conversion year — 134,33 € on the anchor at `t = 18` — where it is
credited, guaranteed and converted before the guarantee is tested. Stopping the Zulage with
the contribution silently removes a full year's subsidy from both the account and the
*Beitragsgarantie*. `check_zulage_lag()` pins all three cases: `zulage_init_pp()` at
`t = 1`, `zulage_granted_pp(t − 1)` for `2 ≤ t ≤ t_conv()`, and zero after.

The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* top-up have **no cells and no
column** [R6]. Only the Zulage reaches the policy; the § 10a advantage is a personal tax
refund between the saver and the tax office, and modelling it as a contract cash flow would
credit the contract with money that never arrives.

## The 100 % Beitragsgarantie, and the one moment it is tested

`guar_pp(t)` is a running accumulator of **contributions** — the *Eigenbeitrag*, the Zulagen
credited, and any unsubsidised contribution above the § 10a ceiling — less the biometric
carve-out. It never accrues interest: the *Beitragserhaltungszusage* is nominal [R1].

```
G(t+1) = G(t) + E(t) + Z(t) + contrib_extra_pp − κ(t),   κ(t) = min(rider_prem_pp, 0.20 · (E + Z + extra + rider))
```

Three things that encoding gets right and an implementation usually gets wrong. It counts
Zulagen **credited**, in the year they are credited, not entitlements in the year they are
earned. It counts **unsubsidised** contributions too, because the undertaking is on the
*Altersvorsorgebeiträge* paid in and does not distinguish the tax pools [R1] — on model
point 8 the accumulator steps by 3 000,00 € a year against an entitlement that never moves
off 175,00 €. And the biometric carve-out is **capped**: model point 9 carries a 400,00 €
rider premium on a 1 200,00 € total contribution, and `guar_carve_out_pp(t)` is
`0.20 × 1 200,00 = 240,00 €`, strictly less than the premium, so raising `rider_prem_pp`
further does not shrink the guarantee any further [REG-R43].

**The guarantee is tested exactly once, at `t_conv()`.** `capital_conv_pp()` is
`max(account_conv_pp(), guar_pp(t_conv() + 1))` and `garantieluecke_conv_pp()` is the
shortfall the insurer funds out of its own resources. On model point 11 — a seven-year
deferral on the `low` declared-rate path — the account reaches 20 481,72 € against a
21 000,00 € guarantee, so **`garantieluecke_conv_pp() = 518,28 €`**, 2,5 % of the capital.
That number is the product's signature output, and a Riester model on which it is never
positive has demonstrated nothing.

`garantieluecke_pp(t)` is published at every `t` and is a **diagnostic**. The anchor opens
at 358,94 € under water, peaks at 567,69 € at `t = 3` and reaches zero at `t = 7`; that is
the normal state of a charged contract in its early durations. `db_pp`, `cv_pp` and
`transfer_value_pp` are **not** floored at it, and flooring them would misstate every
early-duration exit — the guarantee is a promise about *Rentenbeginn*, not about the value
of a policy that leaves before it.

Two of the surplus components counted toward the guarantee — the *Schlussüberschussanteil*
of `slueb_pp()` and the *Bewertungsreserven* share of `bewres_pp()` — sit on an unsettled
question (gap 9). Counting them is the provider-favourable reading; excluding them raises
the projected guarantee cost by their whole amount, and on the anchor's own seventeen-year
deferral at the `low` rate that is the difference between a *Garantielücke* of zero and one
of 506,56 €.

## The account is two balances and one credited rate

`dk_pp` is the *Deckungskapital* and `surplus_acct_pp` the *Überschussguthaben*; `av_pp` is
their sum. The split is **guarantee accounting, not two investment strategies**: the whole
account grows at the declared *laufende Verzinsung* `j(t)`, and `D` is carved out of it as
the part the *Rechnungszins* `i` guarantees.

```
int_guar_pp(t)    = i · (D(t) + S(t))
int_surplus_pp(t) = (j(t) − i) · (D(t) + S(t)) + j(t) · U(t)
int_credited_pp(t)= j(t) · (D(t) + S(t) + U(t))     exactly
```

**`j` already includes `i`.** Adding the declared rate to the guaranteed one is the German
arithmetic error this arrangement exists to make impossible, and setting `j = i` collapses
`int_surplus_pp` on the *Deckungskapital* leg to zero, which is the check that they are not
being added. On the anchor `j = 2,30 %` and `i = 0,25 %`, so the *Zinsüberschussbeteiligung*
runs at 2,05 % above the guaranteed leg [REG-R53].

`int_credited` is a column of `result_cf()` and is **reported, not summed into `net_cf`**:
it moves money inside the account rather than across the insurer's boundary. On the anchor
it totals 7 544,45 € over sixty-one years; adding it to the net would report the cell's
undiscounted deficit as 282,94 € instead of 7 827,39 €, which is the single largest way to
get this statement wrong.

## Charges, and a *Sparbeitrag* that can go negative

The AltZertG requires acquisition and distribution costs to be spread over **at least five
years** [R1] — a materially tighter cap on *Zillmerung* than anything the VVG imposes on a
Schicht-3 contract. `acq_charge_pp(t)` is therefore one fifth of `acq_charge_rate ×
beitragssumme` in contract years 1 to 5 and zero afterwards: on the anchor, 168,00 € in
projection years 1 and 2, which are contract years 4 and 5, and nothing from year 3. It
never appears in `result_cf()`, being a deduction *before* the account, but 168,00 € of the
488,90 € rise in the *Sparbeitrag* between `t = 2` and `t = 3` is the charge ending rather
than the contribution rising.

The charge runs for its five contract years **whether or not contributions are paid**. On
model point 10, which goes *beitragsfrei* at `t = 4`, the acquisition charge and the fixed
12,00 € administration charge continue against a contribution of nothing, so
`prem_to_av_pp(4) = 175,00 − 168,00 − 19,00 = −12,00 €` and the *Deckungskapital* falls.
That is a property of the German cost-spreading rule, not a modelling artefact, and it is
why `prem_to_av_pp` is documented as possibly negative rather than clamped at zero.

The *Ratenzuschlag* is a **charge and never a credit**. The saver pays `E(t) × φ` and only
`E(t)` reaches the *Sparbeitrag* base and the guarantee, so the loading enlarges `premiums`
and leaves `prem_to_av_pp`, `guar_pp` and every benefit untouched. The arrangement that
makes that true is worth stating because the notes originally got it wrong:
`contrib_total_pp` is the cash **received** and therefore carries `E(t)·φ`, and
`admin_charge_pp` takes the loading straight back out while striking its percentage on the
**unloaded** base `E + Z + extra`. Deducting the loading in both places — which the drafted
`S = C − K_a − K_v` did, with an unloaded `C` — makes the *Sparbeitrag* fall with the
payment frequency, which is the opposite of the product fact.

## Conversion: the *Rentenfaktor*, the lump sum and the *Kleinbetragsrente*

Everything at *Rentenbeginn* is struck once, at `t_conv()`, and the conversion is a single
event rather than a recursion.

```
ä    = Σ_{k ≥ 0} v^k · k p(x(T), τ(T)) − 11/24        first-order basis, factor 1.00
R_c  = (1 − rentenfaktor_margin) · 10 000 / (12 · ä)
R    = max(R_g, R_c)
```

On the anchor `ä = 20,87222879` at age 67 in calendar **2044** — the annuity basis is
generational, so the conversion happens on its own conversion year's mortality — and
`R_c = 27,947822`, which is **below** the guaranteed `R_g = 29,00`, so the guaranteed
factor applies. The two are independent by construction: `R_g` is a contract term struck at
inception and `R_c` is a function of the shipped table, so the model says which is
authoritative when they disagree rather than leaving it to be inferred.

The whole payout-phase loading sits in `rentenfaktor_margin` — 30 % **[std]** — rather than
being taken partly in the factor and partly out of each instalment, which would
double-count; the insurer's real payout administration is an explicit `expense_annuity`
cash flow instead. `check_conversion()` asserts the consequence,
`rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000`, which holds
on every model point whether or not the current factor is the one applied, and which
catches a Woolhouse correction applied twice or a factor struck on the second-order basis.

`teilkapital_pp()` is the elected share of the conversion capital, clamped at the statutory
30 % [R1]: 13 726,91 € on the anchor, leaving 32 029,47 € to annuitise at 92,885458 € a
month, 1 114,625493 € a year.

**The *Kleinbetragsrente* commutation is computed, not assumed.** `is_kleinbetrag()` tests
the annuity the model has actually produced against the threshold, so the commutation rate
on a book is an **output** rather than an input — which, given how much of the German book
runs at the *Sockelbeitrag*, is the right way round. Two standardizations sit inside it and
both are stated rather than buried: the test is applied to the annuity payable **after**
the elected lump sum, which trips less often (gap 7); and the threshold of 39,55 € a month
is held **flat in nominal terms** while the *Bezugsgröße* is reset annually, which on a
seventeen-year deferral **understates** the commutation rate. Model points 4, 5, 10 and 13
commute; the anchor's 92,89 € clears the threshold comfortably. A commuted contract pays
`claims_commutation` and **no** `claims_lumpsum` and **no** `claims_annuity`: an *Abfindung*
is the whole capital in one payment, and `pols_if` is zero from `t_conv() + 1` because the
payment discharges the contract outright.

## The payout phase, and the *Rentengarantiezeit*

The projection does not stop at *Rentenbeginn*. `is_payout(t)` holds from `t_conv()`, the
account is extinguished there, and the lifelong *Leibrente* runs to `omega_age = 110` on the
**second-order** generational annuitant basis at `annuity_mort_be_factor = 1.15`. A model
that stopped at conversion would not have modelled the benefit the AltZertG requires [R1].

The *Rentengarantiezeit* changes **who is paid**, never **how much**. `pols_annuity_pay(t)`
is `pols_conv()` while `t − t_conv() < rentengarantie_years()` and `pols_if(t)` afterwards;
`annuity_pp(t)` does not read `rentengarantie_years()` at all. On the anchor the two count
columns are apart for exactly ten years:

| t | 18 | 19 | … | 27 | 28 | 29 |
|---|---|---|---|---|---|---|
| `pols_if` | 0.767588 | 0.762677 | … | 0.701403 | 0.690013 | 0.677530 |
| `pols_annuity_pay` | 0.767588 | 0.767588 | … | 0.767588 | 0.690013 | 0.677530 |
| `claims_annuity` | 855,57 | 855,57 | … | 855,57 | 769,11 | 755,19 |

`claims_annuity` is **exactly 855,57 € in each of those ten years** although a tenth of the
annuitants have died, and falls with the survivors from `t = 28`. Model point 12 carries no
guarantee period at all and pays the same annuity per policy to a smaller count.

The one genuinely sub-annual element of the contract is compressed. The *Leibrente* is
monthly in advance; the model pays twelve instalments as one annual amount at the start of
the payout year, to those alive at the start. Undiscounted, the two agree for a survivor and
differ for a life that dies during the year — an overstatement of roughly `½ · q(x) · 12R`,
about 0,7 % of the annuity at attained age 70 on the shipped proxy. The *level* is right
because the conversion factor carries the Woolhouse `−11/24` correction.
`products/sofortrente/` runs monthly for exactly this reason.

## Four exits, and why a transfer is not a surrender

| Cells | Decrement | Benefit | Charge retained |
|---|---|---|---|
| `pols_death(t)` | `q(t)` | `db_pp(t) = A(t + 1)`, gross | none |
| `pols_lapse(t)` | `w(t)` on the survivors of mortality | `cv_pp(t) = 0.98 · A(t + 1)` | the 2 % *Stornoabzug* |
| `pols_transfer(t)` | `θ(t)` on the survivors of both | `max(0, A(t + 1) − 50,00 €)` | the flat 50,00 € |
| the commuted cohort | — | `commutation_pp()` at `t_conv()` | none |

A *Kündigung* and an *Anbieterwechsel* are **separate decrements, not two spellings of
one**. The transfer pays the full account less a flat charge with **no** *Stornoabzug*, and
carries none of the *schädliche Verwendung* consequences a surrender does [R1] [R14] — so
`transfer_rate` is set **above** `lapse_rate` at every duration, and over the anchor's whole
projection 11,44 % of the cohort transfers out against 7,67 % that surrenders. Collapsing
the two would apply a percentage charge where a flat one belongs and, far worse, would
attribute a repayment of every Zulage and every § 10a relief to an exit that has none.

`exit_charge_pp(t)` is the residue that makes the account roll forward exactly: the account
an exiting policy releases either leaves as a benefit or stays with the insurer as this
charge. On the anchor at `t = 1` it is 1,48 €, and dropping it — because a *Stornoabzug*
looks like income rather than like account released — leaves exactly that residual in
`check_av_roll_fwd_resid(1)`. It is the usual way that identity fails.

*Beitragsfreistellung* is **not** a decrement. It is the German Riester book's dominant exit
[R25] and it is a **state change**: `pols_if` is continuous across it, the account keeps
rolling, the guarantee accumulator freezes once the last Zulage has landed, and the Zulage
stream stops. It is carried as a per-model-point switch (`bfs_year`) rather than as a rate,
because a paid-up policy and a premium-paying one have different account values and
different guarantee accumulators from the moment they diverge, and a scalar
single-model-point projection cannot carry two of each without doubling every recursion.
Model point 10 shows the mechanic on one policy; a book projection needs the cohort split,
and that limitation is stated in the notes' sensitivities rather than left to be found.

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Riester_DE_A/` holds nothing but formulas:

```
products/riester_rente/
  model_point_table.csv        <- inputs live here
  mort_table_accum.csv
  annuity_mort_table.csv
  lapse_table.csv
  zulage_schedule.csv
  income_schedule.csv
  surplus_scenario.csv
  freq_loading.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Riester_DE_A/                <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
policy. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many policies are
projected. The conventions suite counts the reads.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_accum_file` | `mort_table_accum()` | `mort_table_accum.csv` |
| `annuity_mort_file` | `annuity_mort_table()` | `annuity_mort_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `zulage_file` | `zulage_schedule()` | `zulage_schedule.csv` |
| `income_file` | `income_schedule()` | `income_schedule.csv` |
| `surplus_file` | `surplus_scenario()` | `surplus_scenario.csv` |
| `freq_loading_file` | `freq_loading()` | `freq_loading.csv` |

**The trade-off:** the model is not portable on its own. Copy `Riester_DE_A/` without the
CSVs and it will read fine, then fail on first evaluation. What you gain is that a diff of
the model shows logic changes only, and an input can be swapped in place — point
`Data.annuity_mort_file` at another same-schema file and the conversion follows, with no
formula change. Tests cover both halves of that bargain.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points, twenty-six columns. **Point 1 is the worked-example anchor cell**; points 2–13 exercise the at-inception reconciliation, both *Kinderzulage* rates at once, the *Sockelbeitrag* floor, the `fixed` form, the *Berufseinsteiger-Bonus*, the § 86 Kürzung, an unsubsidised second pool, the 20 % carve-out cap, a *Beitragsfreistellung*, a binding *Garantielücke*, a pure lifelong annuity, and the statutory earliest *Rentenbeginn* | configuration, and the **one file exempt** from the provenance rule |
| `mort_table_accum.csv` | Accumulation death rates by attained age 16–110 | **[std]** proxy for **DAV 2008 T** [REG-R48], `qx = 0.001500 × 1.10^(age − 50)`, with **no** improvement dimension — on a death cover improvement favours the insurer. **The anchor a replacement must preserve is `qx` at age 50 = 0.001500** |
| `annuity_mort_table.csv` | Annuitant base rates and an improvement scale, ages 55–110 | **[std]** **generational** proxy for **DAV 2004 R** [REG-R49]. The property a replacement may not drop is that it is **two-dimensional**. **The anchor is `ann_factor() = 20.87222879`** at age 67 in 2044, which is what puts `rentenfaktor_curr()` below the guaranteed 29,00 |
| `lapse_table.csv` | `lapse_rate` and `transfer_rate` by contract duration 1–60 | **[std]**, and **no observed range exists** — no German Riester *Stornoquote* was established for any year (gap 16). Transfer is set above surrender at every duration, and that ordering is itself the assertion |
| `zulage_schedule.csv` | `unmittelbar`, `n_kinder_pre2008`, `n_kinder_post2008`, `bonus` by schedule id and `t` | [R9] [REG-R42] for the entitlement pattern. Exogenous because *Kindergeld* is a household fact the insurance contract does not observe — the most awkward feature of this product for a per-policy projection |
| `income_schedule.csv` | Contribution-liable earnings by schedule id and `t` | **[std]** 2 % nominal growth paths plus a `zero` path for the *mittelbar* eligible spouse. It decides when the 2 100 € ceiling binds and so the whole shape of the contribution stream |
| `surplus_scenario.csv` | `laufende_verz` by scenario id and `t`; `base` 2,30 % level, `low` 0,50 % level | **[std]**, and the **largest single lever in the model**: no declared rate at any carrier was established (gap 12). The rate **includes** the *Rechnungszins* [REG-R53] |
| `freq_loading.csv` | The *Ratenzuschlag* multiplier by payment frequency | **[std]** 1.0000 / 1.0100 / 1.0200 / 1.0300, a charge and never a credit |

## The identities the model checks

`check_net_cf()` — **delib's first ruling** — states the cash flow statement's own
reconciliation in one line:

```
net_cf(t) = premiums(t) + zulagen(t) − claims_death − claims_lapse − claims_transfer
            − claims_lumpsum − claims_commutation − claims_annuity − expenses(t) − commissions(t)
```

with `int_credited` deliberately outside it. Five more sit beside it, each a `bool` over all
`t` with a `check_*_resid(t)` companion, and the conventions suite calls all six on every
model point:

| Check | What it would catch |
|---|---|
| `check_av_roll_fwd()` | The account released by an exit not being counted — the *Stornoabzug* and the transfer charge look like income rather than like account released |
| `check_guar_roll_fwd()` | The entitlement added instead of the credit; interest added to a nominal guarantee; the unsubsidised limb dropped; the 20 % carve-out cap not binding |
| `check_pols_roll_fwd()` | A misindexed decrement recursion, and — through the closure identity, built by direct summation over the exit cells — a commuted cohort that leaves without being counted |
| `check_conversion()` | The guarantee not applied; the capital not fully disposed of between lump sum, annuity capital and *Abfindung*; a *Rentenfaktor* inconsistent with the annuity basis |
| `check_zulage_lag()` | The two lags collapsed into one, and the final contribution year's Zulage dropped |

## Modules that are off in the base run

Everything the product carries is implemented; what varies is which model point switches it
on. The anchor is deliberately the plain cell, so the worked example reproduces while the
machinery stays visible and testable.

| Module | Switch | Off value on the anchor | On at | What it does |
|---|---|---|---|---|
| Unsubsidised second contribution pool | `contrib_extra_pp` | `0.00` | point 8, at 900,00 € | Enters the account **and** the guarantee while drawing no Zulage, so `pool_ungefoerdert_pp` diverges from `pool_gefoerdert_pp` and the contract carries two tax regimes [R12] |
| Biometric-rider carve-out | `rider_prem_pp` | `0.00` | point 9, at 400,00 € | Excludes rider contributions from the *Beitragserhaltungszusage*, capped at 20 % of total contributions [REG-R43]. Never a cash flow of this model |
| *Beitragsfreistellung* | `bfs_year` | `0` (never) | point 10, at year 4 | Stops the contribution and the Zulage while the account keeps rolling and the acquisition charge keeps biting |
| § 86 proportional Kürzung | `contrib_ratio` | `1.00` | point 7, at 0.50 | Halves the contribution and, in the same proportion, the subsidy [R10] |
| *Ratenzuschlag* | `prem_freq` | `annual`, `φ = 1.0000` | points 3, 4, 6, 7, 10, 13 | Raises `premiums` by `E(t)(φ − 1)` and nothing else |
| *Berufseinsteiger-Bonus* | the `bonus` column of `zulage_schedule.csv`, and `zulage_init_pp` | `0` / 475,00 € | point 6, 200,00 € inside a 375,00 € opening credit | The once-in-a-lifetime addition to the *Grundzulage* [R9] |
| The low declared-rate stress | `scenario_id` | `base`, 2,30 % | point 11, `low` at 0,50 % | Opens a *Garantielücke* of 518,28 € — the only lever that decides whether the guarantee costs anything |
| *Teilkapitalauszahlung* election | `teilkapital_share` | `0.30`, the statutory cap — **on** by default | point 12, at 0.00 | The pure lifelong annuity, with the whole capital annuitised |
| *Rentengarantiezeit* | `rentengarantie_years` | `10` — **on** by default | point 12, at 0 | Pays the instalment to `pols_conv()` rather than `pols_if(t)`, and never changes the instalment |

Two Space-level References are worth naming because a user will want to move them:
`zulage_lag = 1`, the ZfA payment convention, which is the shortest lag consistent with the
statute (gap 6); and the pair `mort_be_factor = 0.80` and `annuity_mort_be_factor = 1.15`,
which run in **opposite** directions because the direction of prudence forks by product — a
first-order death table assumes mortality higher than expected, a first-order annuity table
lower [REG-R47].

Three constructions are described in the sources and are **not** implemented, rather than
being implemented and switched off. The *Auszahlungsplan mit Restverrentung* [R1] is the
fund and bank chassis's payout topology, not the insurance one. Wohn-Riester is absent in
both limbs — no *Eigenheimbetrag* decrement, no certified *Darlehen*, and no
*Wohnförderkonto*, the last because it is a notional tax-bookkeeping account carrying no
cash flow at all [R13]. And there is no surplus in payment: the wedge between the
first-order and second-order annuity bases is a *Risikoüberschuss* this model does not
distribute.

## Sign convention

`net_cf` is **income positive** — contributions and Zulagen in, the six kinds of benefit,
expenses and commission out — which is the notes' own orientation and the library-wide sign.
`liability_cf` publishes the same stream outgo-positive, `liability_cf(t) = −net_cf(t)`
exactly, and both are columns of `result_cf()` so the identity is verifiable in the frame
rather than only in prose. A Solvency II best estimate is `Σ v(t) × liability_cf(t)` over
the relevant risk-free term structure, plus a risk margin [REG-R5] [REG-R6]; nothing in this
library discounts.

`expenses` and `commissions` are **separate** columns and `net_cf` subtracts each exactly
once — the frlib reading, where `expenses` contained the commission, is not the reading
here, and the notes' worked example prints both. `int_credited` is a state movement and is
in neither.

The shape to expect on an in-force accumulation cell is a modest positive `net_cf` in every
accumulation year — 1 505,37 € at `t = 1` on the anchor — then a very large negative in the
conversion year, −11 276,67 €, as the *Teilkapitalauszahlung* leaves in one payment, then a
long thin negative tail of annuity instalments. The undiscounted total is −7 827,39 €.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue and
`savings/CashValue_SE` for the account-value chassis: `pols_*` for policy counts, plural
nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)`
with an uppercase `kind` string, `pols_if_at(t, timing)` and `av_pp_at(t, timing)` for the
within-year reads, `prem_to_av_pp` for the part of the contribution credited to the account.
The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `Z*(t)`, `Ẑ(t)`, `Z(t)` | `zulage_entitlement_pp` / `zulage_granted_pp` / `zulage_pp` | Three different amounts and the product turns on the difference: the § 84/85 entitlement, the same after the § 86 Kürzung, and the cash actually credited a year later |
| `C(t)` | `contrib_total_pp` | The notes' `C` is the contribution *credited*; the cells is the cash **received**, so it carries the *Ratenzuschlag* that `admin_charge_pp` deducts back out |
| `S(t)` | `prem_to_av_pp` | The lifelib name for the premium credited to an account value. **May be negative**, which is the point of model point 10 |
| `D`, `U` | `dk_pp` / `surplus_acct_pp` | Guarantee accounting, not two investment strategies. Named separately because `check_av_roll_fwd` needs both and because the `j` ≥ `i` relation is only visible when they are apart |
| `G(t)`, `Λ` | `guar_pp` / `garantieluecke_conv_pp` | An accumulator tested once, and the shortfall it produces. `garantieluecke_pp(t)` is a third name for the *running* gap, and it is a diagnostic that no benefit reads |
| `l(t)` in payout | `pols_if` / `pols_annuity_pay` | During the *Rentengarantiezeit* the instalment is paid on a count that is **not** the in-force, so the two are different columns of `result_cf()` |

Three sister models share a chassis with this one and the names mean the same thing on all
of them. `RV_DE_A`, the *klassische aufgeschobene private Rentenversicherung*, is the same
general-account accumulation and the same conversion at a guaranteed *Rentenfaktor* with
none of the Schicht-2 apparatus — it is the primary home for the `dk_pp` / `surplus_acct_pp`
recursion and for § 169 VVG. `Basis_DE_A` is the Schicht-1 sibling: the same
*nachgelagerte Besteuerung* and the same annuitisation constraint, with no Zulagen, no
*Beitragsgarantie* and no lump sum at all. And `Sofort_DE_S` is the payout contract this
model's second phase compresses onto an annual grid.

Two model point columns drive nothing and are carried anyway. `sex` is reporting only —
Riester tariffs have been unisex since a 2006 vintage [R23], six years before the general
rule, so no rate in this model may read it, and its **absence** from every formula is the
assertion worth making. `issue_age` enters only through `age(1) = issue_age +
duration_init`; no rate here is struck at issue.

## Standardizations used

Everything in this list is **[std]**. The statutory half of the product is not a composite
at all; the carrier half is entirely one, because nothing carrier-specific was established.

| Standardization | Value | Rationale |
|---|---|---|
| Accumulation mortality table and its slope | `qx = 0.001500 × 1.10^(age − 50)` at `mort_be_factor = 0.80` | DAV 2008 T is proprietary and is not redistributed [REG-R47] [REG-R48]. The 10 % slope is a placeholder; the anchor is the rate at age 50 |
| Annuity table, improvement scale and base year | `qx_base = 0.006000 × 1.115^(age − 65)`, improvement 1,8 % tapering to 0,2 %, base 2027, at `annuity_mort_be_factor = 1.15` | DAV 2004 R is proprietary [REG-R49]. What is **not** optional is the generational structure; the anchor is `ann_factor() = 20.87222879` |
| *Rechnungszins* | 0,25 % on the anchor, 0,90 % on point 3 | The *Höchstrechnungszins* caps the reserving rate, not the rate a policy guarantees [REG-R14]; using the cap of the vintage is the highest defensible value and makes the guarantee cheapest |
| *Laufende Verzinsung* | `base` 2,30 %, `low` 0,50 %, both level | No carrier declaration was established (gap 12). `low` is a stress, not a forecast |
| *Risikoüberschuss*, *Kostenüberschuss* | zero | The accumulation risk result is nil by construction — the death benefit is the account value, so there is no sum at risk — and no cost result was established |
| *Schlussüberschussanteil*; *Bewertungsreserven* share | 2,0 % of contributions credited; 1,0 % of the account, both counted toward the guarantee | Levels unestablished; **whether they may close a guarantee shortfall is unsettled** (gap 9), and counting them is the provider-favourable reading |
| Acquisition charge | 2,5 % of `beitragssumme` over five contract years | The five-year floor is statutory [R1]; the level is a round number, sized so the charge is of the same order as one year's contribution |
| Administration charge, and its base | 4,0 % of each contribution credited **including the Zulagen**, plus 12,00 € a year | **Whether German tariffs charge the Zulagen was not established** (gap 14), and on the low-income cells the Zulagen are the majority of the contribution. Stated explicitly rather than left to be inferred from a formula |
| Frequency loading | 1.0000 / 1.0100 / 1.0200 / 1.0300 | No *Ratenzuschlag* scale was established. Treated as a charge |
| *Stornoabzug*; transfer charge | 2,0 % of the account; 50,00 € flat | The transfer charge is capped by statute but the cap was not established (gap 8) |
| *Rentenfaktor* margin; annuitisation interest; the guaranteed factor | 30 %; 1,00 %; 29,00 € per 10 000 € per month | No *Rentenfaktor* at any carrier for any year was established (gap 9). The whole payout loading sits in the margin rather than being split |
| The two-*Rentenfaktor* construction | `max(R_g, R_c)` | Documented for the German Schicht-3 market in a sibling research file; **not established for any Riester tariff** |
| *Kleinbetragsrente* threshold, and the test's basis | 39,55 € a month, flat in nominal terms, applied **after** the lump sum | Two irreconcilable readings of the threshold exist [REG-R42] [REG-R46]; the lower is taken. Both choices push toward fewer commutations and a longer-tailed liability (gap 7) |
| Zulage cash lag | one year | [R11] establishes the arrear but not the month (gap 6); one year is the shortest lag consistent with the statute |
| Surrender and transfer rates | 0,8 / 0,6 / 0,4 % and 1,2 / 0,9 / 0,6 % by duration band | **No German Riester behavioural rate was established for any year** (gap 16). The ordering — transfer above surrender — is an argument from the statutory consequences, not from data |
| Income growth | 2,0 % p.a. nominal | A round real-plus-inflation number. It decides when the 2 100 € ceiling binds |
| *Teilkapitalauszahlung* take-up | 30 % on the anchor | German commentary reports the lump sum as usual, and **gap 10 records that this rests on nothing** |
| Expenses and commission | 30,00 € maintenance inflating at 2,0 %; 24,00 € per annuitant; 80,00 € per claim; 150,00 € + 2,0 % of `beitragssumme` at issue; 2,5 % initial and 1,5 % renewal commission | No German insurer publishes a unit cost. The maintenance figure carries the Zulage administration — the *Dauerzulageantrag*, the annual ZfA data exchange and the *Leistungsmitteilung* — which is a real product-specific cost |
| Timing and processing order | Contribution and Zulage at the start of the year, interest at the end, decrements after crediting, conversion at the start of `t_conv()` | No source in the corpus fixes the ordering inside a period |
| Decrement ordering | mortality, then surrender on the survivors, then transfer on the survivors of both | Stated so an implementation can be compared line by line |
| The monthly annuity on an annual grid | twelve instalments as one payment at the start of the payout year | The level is right because the factor carries the Woolhouse correction; the timing overstates by roughly `½ · q(x) · 12R` |
| `omega_age = 110`, with `q = 1` there | — | Makes the closure identity exact rather than approximate |
| Opening balances and the model points themselves | — | The anchor's seeds are **[std]**, and the notes record that `guar_pp_init` and the account seeds were struck on different income paths, a 195,08 € discrepancy kept rather than papered over |

The only quantities in the model that are **not** standardizations are the statutory ones:
the 175,00 € / 185,00 € / 300,00 € Zulagen and the 200,00 € bonus [R9], the 4 % / 2 100,00 €
/ 60,00 € *Mindesteigenbeitrag* arithmetic and the proportional Kürzung [R10], the one-year
ZfA arrear [R11], the *Beitragserhaltungszusage* itself and the 20 % biometric carve-out
[R1] [REG-R43], the 30 % *Teilkapitalauszahlung* cap [R1], the five-year cost-spreading
floor [R1], the earliest *Rentenbeginn* of 62 [R1], the *Wechselrecht*'s existence [R1], and
the structural rules — the Zulage as a contribution, the guarantee tested once, benefits
gross of the *Rückzahlungsbetrag*, and unisex pricing [R23].

## Tests

`tests/test_riester_rente_de.py` asserts every row of the notes' worked-example table to the
cent and `pols_if` to six decimals, the payout phase's selected rows, the full-precision
totals over all sixty-one periods against the four-cent difference a sum of rounded cells
would give, the notes' four independent rebuilds — projection year 1 from the statute up,
the conversion year, the aggregate account roll-forward with its exit charge, and the
four-way decrement closure to 1.00000000 — and the two variants, the binding *Garantielücke*
of model point 11 and the commuting *Sockelbeitrag* cell of model point 5.

Beyond the worked example it asserts **one test per numbered modeling pitfall**: the two
subsidy lags kept apart; the final contribution year's Zulage credited at `t_conv()`; the
§ 86 Kürzung proportional and not a cliff; the Zulage published as a separate positive
income column; no *Günstigerprüfung* cells anywhere; both *Kinderzulage* rates running at
once; the guarantee tested only at *Rentenbeginn* and no benefit floored at it; the 20 %
carve-out cap binding; unsubsidised contributions inside the guarantee; the declared rate
including and not added to the *Rechnungszins*; the frequency loading charged and never
credited; the acquisition charge spread over five contract years and continuing through a
*Beitragsfreistellung*; transfer separated from surrender; *Beitragsfreistellung* as a state
change; two mortality bases in opposite directions with a generational annuity table; the
*Kleinbetragsrente* tested on the post-lump-sum annuity against a flat threshold; the
*Rentengarantiezeit* changing the count and never the amount; and every benefit published
gross of the *Rückzahlungsbetrag*. The `check_*` identities and their residuals are asserted
on the anchor and on the two variants; the whole-model-point-table sweep belongs to
`tests/test_model_conventions_de.py`, which owns the library's single sweep.

```bash
python -m pytest lifelib/libraries/delib/tests/test_riester_rente_de.py -q
```
