# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/fondsgebundene_rentenversicherung/technical-notes.md`](technical-notes.md);
the product it implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing, reserving or disclosure result.**
> The *mechanics* are common ground in German practice and several of them are cited: the
> *Beitragsverrechnung* order and the purchase of *Anteileinheiten* at the *Anteilspreis*
> [S1], the *Höchstzillmersatz* of 25 ‰ of the *Beitragssumme* [R12] [R13] [REG-R16] and
> the even spreading of the acquisition charge over the first five contract years [R1]
> [REG-R28], the *Beitragsrückgewähr* death benefit [S2], the *Zeitwert* *Rückkaufswert*
> and the conditions on a *Stornoabzug* [R1] [REG-R28] [REG-R36], the survival of the
> fund-based charges into a *beitragsfrei* contract [R3], the `max(guaranteed, current)`
> *Rentenfaktor* rule [S4] [R22], and the unisex tariff [REG-R34]. The **levels** are
> almost entirely **[std]**: **no charge rate, no *Rentenfaktor*, no lapse rate and no
> expense loading was established at any carrier**, and **no document cited anywhere in
> this library was retrieved** — direct HTTP egress was blocked and the session's search
> budget was exhausted before this product's research began. The DAV tables behind both
> mortality bases — DAV 2008 T for the *Risikobeitrag* [R17] [REG-R48], DAV 2004 R behind
> the *Rentenfaktor* [R16] [REG-R49] — are the property of the Deutsche Aktuarvereinigung,
> are not public and are **cited by name, never shipped**. Replace the charge scale, the
> decrement tables and the fund path with a real tariff and company data before drawing any
> conclusion from a number. Nothing this model produces is an *Effektivkostenquote*, and
> nothing it produces may be compared with a PRIIPs performance scenario [R8] [R9]
> [REG-R32].

## Run it

```bash
python products/fondsgebundene_rentenversicherung/run.py
python products/fondsgebundene_rentenversicherung/run.py 7    # the beitragsfrei cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/fondsgebundene_rentenversicherung/FRV_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per
cash flow line, and `result_fund()` the per-policy unit side beside it — the *Anteilspreis*,
the unit count, the four within-month *Fondsguthaben* balances, the *Beitragsrückgewähr*
base, the net amount at risk and the three decrement rates. That second frame is roughly
what a German *Standmitteilung* reports [S17], which is not a coincidence: the statement's
line items are this model's state vector.

The model and both its Spaces carry docstrings. `model.doc` describes the product and the
projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` says what each input file is, what
the two shipped decrement proxies are anchored on, and what a replacement must preserve.

## The insurer guarantees the number of units, not their value

Everything else follows from that sentence, and it is what makes this model different from
the four general-account models beside it in the library rather than a translation of one.
There is no *Rechnungszins* in the accumulation phase, no *Deckungskapital*, no
*Zinsüberschuss*, no *Bewertungsreserven* worth speaking of — and, because § 125 VAG makes
the covering assets a segregated *Anlagestock* held in the very units the liability is
denominated in [R15] [REG-R7], **no investment-mismatch term anywhere in the model**.

So the state variable is the unit count and euro are derived from it:

```
units_pp(t + 1) = units_pp(t) + units_bought_pp(t) − units_cancelled_pp(t)
av_pp(t)        = units_pp(t) × unit_price(t − 1)
```

`check_units_roll_fwd()` asserts the first line and `check_av_roll_fwd()` the account
identity that carries the price. They look redundant and are not, which is why both ship:
**the unit identity has no price term in it at all**, so it fails when a charge is taken in
euro without the matching units being cancelled while every euro total in the frame still
looks plausible; the account identity fails when the month's return is applied at the wrong
point in the order. An implementation can pass either one alone.

The fund's **TER** is a third category again and the model deliberately gives it no
`charge_*` cells: it is borne inside the *Anteilspreis*, accrues to the fund manager and
never appears in a policy ledger, so `fund_return_net_ann(t) = gross − ter` nets it off the
assumed return instead. Charging it explicitly double-counts the fund's costs; ignoring it
overstates the policyholder's return. On the base path 5.00 % gross less a 0.45 % TER is
4.55 % p.a. and `(1.0455)^(1/12) − 1 = 0,371482 %` a month.

## `net_cf` is the non-unit stream

Every benefit this contract pays before *Rentenbeginn* — the death benefit up to the fund,
the *Rückkaufswert*, the *Teilentnahme*, the capital released at *Rentenbeginn* — is funded
by cancelling the policyholder's **own** units, so a gross presentation would count the same
money twice. **delib's first ruling** requires every model to publish `check_net_cf()`, and
here the identity it closes is one line:

```
net_cf = charge_acq + charge_admin_prem + charge_admin_fund + charge_policy_fee
         + charge_risk + stornoabzug − expenses − death_strain
```

Charges in, the insurer's own expenses and the death strain out, and nothing else.
`check_net_cf_resid(t)` does not restate that formula: it rebuilds the first two terms **by
a different route**, as `premiums − prem_to_av`, which is exactly what the
*Beitragsverrechnung* leaves behind — so the check crosses the unit / non-unit boundary
instead of asserting the code against itself.

The gross flows are published beside it rather than dropped. `premiums`, `prem_to_av`,
`claims_death`, `claims_lapse`, `claims_maturity`, `withdrawals` and `av_releases` are all
`result_cf()` columns and all **excluded** from `net_cf`, and `check_benefit_funding()`
asserts that they net exactly:

```
claims_death + claims_lapse + claims_maturity + withdrawals + stornoabzug
    = av_releases + death_strain
```

Booking the whole *Fondsguthaben* as an insurer outgo is this product's first-order failure
mode — it leaves every column in the frame looking reasonable and the liability overstated
by the entire fund — and publishing the excluded columns is what lets a reader see what was
excluded. On the anchor cell the scale of it is 64 869,36 € of benefits against 40 586,28 €
of premiums, of which **4,39 € is an insurer cost**; the rest is the policyholder's own
units coming back.

Seven `check_*()` cells travel with the model, each a `bool` over all `t` with a
`check_*_resid(t)` companion: `check_net_cf`, `check_prem_split`, `check_units_roll_fwd`,
`check_av_roll_fwd`, `check_benefit_funding`, `check_pols_roll_fwd` and `check_acq_charge`.
All seven are `True` on all thirteen model points.

## Withheld from the premium, or cancelled out of the fund

This is the distinction the product turns on and the model's most easily-hidden error. The
*Beitragsverrechnung* withholds the acquisition instalment and the premium-based
administration charge **before** any unit exists:

```
prem_to_av_pp(t) = B(t) + Z(t) − charge_acq_pp(t) − beta_rate × B(t)
units_bought_pp(t) = prem_to_av_pp(t) / unit_price(t − 1)
```

while the *kapitalbezogene Verwaltungskosten*, the *Stückkosten* and the *Risikobeitrag* are
levied **after** the month's return, by cancelling units that already exist.
`check_prem_split()` asserts that the premium splits exactly three ways — into
`prem_to_av`, `charge_acq` and `charge_admin_prem` — so a model that also netted the
*Stückkosten* or the fund-based charge out of the *Beitrag* fails there.

What the model does **not** do is take a shortcut that looks identical while premiums are
paid: netting `gamma` out of the *Beitrag* gives the right answer until the premium stops
and the wrong answer from then on. Model point 7 goes *beitragsfrei* at month 121 on a
zero-return fund, and from there `premiums(t)` is zero while `charge_admin_fund(t)`,
`charge_policy_fee(t)` and `charge_risk(t)` continue and the fund decays — which is the
product fact § 165 VVG makes possible [R3] [REG-R28], not a modelling artefact.

A *Zuzahlung* pays its own *Zuzahlungskosten* and **no** *beitragsbezogene* charge, because
it is not a regular *Beitrag*; it is booked in `charge_acq`, which is why `charge_acq(121)`
is non-zero on model point 9.

## The acquisition charge, its window, and the in-force cell

`charge_acq_total() = alpha_rate × beitragssumme()` — **2,50 % of the sum of premiums
payable, the *Höchstzillmersatz* itself** [R12] [REG-R16] — spread in equal instalments over
`acq_window_months() = min(alpha_spread_months, 12 × prem_term_y)` months at the policy's
own premium frequency [R1] [REG-R28]. The composite takes the cap rather than a guessed
interior point, on the ground that a reference implementation should demonstrate the binding
constraint. On the anchor cell that is 1 800,00 € over 60 instalments of **30,00 €**, which
is 15 % of each of the first sixty premiums and **nothing from month 61**, where the
*Anlagebeitrag* steps from 162,00 € to 192,00 €. That cliff is the characteristic shape of a
German unit-linked contract's early values and it is why this model runs monthly: an annual
grid cannot place month 60.

The instalment **count** is the window divided by the frequency — 60 monthly, 20 quarterly,
10 half-yearly, 5 annual, and **24** on model point 12, whose premium term is two years. A
shortened term spread over sixty months regardless would understate every instalment and
leave the ledger short. `check_acq_charge()` closes the ledger against an expectation
**counted rather than accumulated** — instalment dates elapsed times the instalment, plus
the *Zuzahlungskosten* on any *Zuzahlung* received — so a window running one month too long
fails there.

`beitragssumme()` is the sum of premiums **payable at the initial level** and is invariant:
it does not shrink on lapse or *Beitragsfreistellung* and does not grow with a
*Beitragsdynamik* increment or a *Zuzahlung*. A real tariff re-zillmers each accepted
increment over its own sixty months and an increment cannot be assumed at inception; the
bias that leaves — an understated acquisition charge on a dynamic contract — is stated
rather than hidden. Letting `S` follow the premiums actually paid would make the acquisition
charge a function of the lapse assumption, which is both wrong and circular.

An **in-force** model point opens after the window has closed. Model point 6 starts at
`t = 97`, so `charge_acq(t)` is zero at every projected month **and** `expenses(97)` carries
no acquisition commission — `expense_acq_pp` falls at `t = 1` and only there, and `t = 1` is
not in that model point's frame. That is the whole of the difference between an in-force
cell and a new-business one on this chassis.

## The *Beitragsrückgewähr*, and two mortality bases at once

The composite death benefit is `max(Fondsguthaben, Summe der gezahlten Beiträge)` [S2], so
the net amount at risk is `max(cum_prem_pp(t) − F, 0)` — positive early, vanishing once the
fund overtakes the premiums paid (month 95 on the anchor cell), and returning after a market
fall. That makes `cum_prem_pp` a genuine **state variable** of this product rather than a
reporting convenience, and it makes the risk charge a quantity that has to be recomputed
every month. It is the premiums **paid**, gross: `cum_prem_pp(60) = 12 000,00 €` against
9 720,00 € actually invested, so reading the floor off the invested amount would understate
the death benefit by 19 %.

The floor at zero in `nar_pp()` is load-bearing rather than decorative. Without it the
contract would pay the insurer a negative charge in every month the fund is above the floor
and `death_strain` would turn negative, silently booking the fund's growth as insurance
profit.

`db_pp(t) = av_pp_at(t, "BEF_DECR") + nar_pp(t)` rather than `max(floor, fund)`: writing it
as a sum is what keeps the unit and non-unit sides apart, the first term being the
policyholder's own money and the second the insurer's.

**The *Risikobeitrag* is priced on a death table and the conversion guarantee on an annuity
table.** `mort_rate_tariff_at_age` reads `mort_table.csv` — a **[std]** first-order DAV 2008 T
proxy [R17] [REG-R48] — and `rentenfaktor_guar` reads `rentenfaktor_table.csv`, which stands
in for DAV 2004 R [R16] [REG-R49]. **No cells reads both files**, which is the arithmetic
form of the statement that a German fondsgebundene contract carries two mortality bases at
once; a model pricing the death charge on an annuitant table understates it.

The projection then decrements on a **third** rate, the second-order best estimate
`mort_be_factor = 0.75` times the tariff rate [REG-R47]. The wedge is the *Risikoergebnis*,
and because the factor is flat it is exactly 25 % of the *Risikobeitrag* collected — 5,849973
less 4,387480 = 1,462493 € on the anchor cell — a closed-form check a reader can do with a
calculator. A model using one basis for both makes the risk result identically zero and
deletes the mechanic.

The two monthly conversions are deliberately different. Mortality is split **linearly**,
`mort_rate_mth = mort_rate / 12`, because the tariff's own *Risikobeitrag* is `q(x)/12` times
the *riskiertes Kapital* and the charge and the decrement must rest on the same split, or the
model manufactures a risk result out of a rounding convention. Lapse is split
**geometrically**, `1 − (1 − lapse_rate)^(1/12)`, because nothing is priced off it and the
annual rate is the observable twelve monthly steps must reproduce. The fund return is
compounded geometrically for the same reason the lapse rate is: it is an effective annual
rate, while a German tariff's charge rates are nominal, which is why `gamma_rate_mth()` is
`gamma_rate_ann() / 12`.

## The *Rückkaufswert* is the *Fondsguthaben*

§ 169 VVG sends a fondsgebundene contract to the *Zeitwert*, and on a pure unit-linked
contract with no insurer-given guarantee the *Zeitwert* **is** the fund [R1] [REG-R28].
There is no discounting, no *Rechnungszins*, no mortality basis, no *Zillmerung* residue and
no second-basis *Mindestrückkaufswert* anywhere in this model — the cleanest surrender rule
of the ten delib products, and the reason this product is a good vehicle for demonstrating
unit mechanics. The protection for the policyholder sits earlier, in the sixty-month
spreading, which is why the surrender value is positive from the first month.

A *Stornoabzug* is permissible only if *vereinbart*, *beziffert* and *angemessen*, and
**never for unamortised acquisition costs** [R1] [REG-R36]. `stornoabzug_pp(t)` is therefore
a flat rate on the *Fondsguthaben* and is deliberately **not** a function of
`charge_acq_total() − cum_charge_acq_pp(t)`: a deduction of that kind is what stops an
insurer recovering through the deduction what the five-year spreading denies it. Only the
`std_high` scale carries a non-zero rate and only model point 5 uses it.

*Beitragsfreistellung* is a **model point election**, `pup_month`, and not a cohort
decrement — the one place the model reproduces a mechanic exactly on one cell rather than
approximately on all of them. A paid-up policy's fund and its *Beitragsrückgewähr* base both
depend on the month it went paid-up, so a cohort-level paid-up rate would need one
sub-cohort per month: a two-dimensional recursion over 360 months for a second-order effect.
The **[std]** 1 % p.a. paid-up rate a cohort implementation would use is recorded and not
implemented, and the omission biases projected charge income **upward**. *Storno* and
*Beitragsfreistellung* stay two different things: one is an exit paying the *Rückkaufswert*,
the other a change of state paying nothing [R2] [R3].

## The last month, the age at *Rentenbeginn*, and the reduction in yield

`lapse_rate_mth(proj_len()) = 0` **[std]**. The end of the last projected month is
*Rentenbeginn*, so a surrender and an annuitisation are the same event releasing the same
*Fondsguthaben*, and the whole surviving cohort is booked as `pols_maturity`. No cash flow
moves either way; the convention only decides the split between the lapse total and the
maturity count, and it is what the closure identity reproduces — deaths 0,04377181 plus
lapses 0,65322937 plus maturity 0,30299882 = 1,00000000. It is frlib's convention on
`TD_FR_A` and delib adopts it.

`age(proj_len()) = annuity_age − 1`, because the annuity begins at the **end** of that
month, and the *Rentenfaktor* is read at `annuity_age`: **25,00 at 67 on the anchor cell,
not the 24,45 an off-by-one would fetch at 66**, a 2,2 % understatement of the pension. The
rule applied is `max(rentenfaktor_guar(), rentenfaktor_curr())` [S4] [R22] — a guarantee
**with upside**, so a model applying only the guaranteed factor understates the benefit
whenever the current tariff is richer. On `std_2026` the two are equal, so the `max()` is
exercised without injecting an unsourced uplift; model point 13 carries `rich_current`,
where the current factor is 12 % higher and the `max()` visibly bites.

Only the **conversion terms** are guaranteed; the capital they multiply is the market's. A
guaranteed *Rentenfaktor* is not a guaranteed pension, and any document implying otherwise
is wrong.

`reduction_in_yield()` is the product's defining metric, because on a contract with no
*Rechnungszins* the charge stack **is** the economics. It is `gross_return_ref() −
irr_ann()`, computed on a **single persisting contract** — no survivorship, no lapse —
because a reduction in yield is a statement about one policy. On the anchor cell 5,0000 %
less 3,6593 % = **1,3407 % p.a.**, and the same measure across the four shipped charge
scales moves by a factor of five. **It is a delib-defined measure and it is not the
statutory *Effektivkostenquote***: the German figure is aligned to the total-cost-indicator
method of the PRIIPs RTS over a specified recommended holding period [R7] [R9] [REG-R31]
[REG-R32], and this model implements neither.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `FRV_DE_S/` holds nothing but formulas:

```
products/fondsgebundene_rentenversicherung/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  charge_table.csv
  fund_scenario_table.csv
  rentenfaktor_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  FRV_DE_S/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input files beside the model
and reads them at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
policy. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many policies are
projected. The conventions suite counts the reads over a full sweep of the model point
table and asserts the file set, not merely the count.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_file` | `mort_table()` | `mort_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `charge_file` | `charge_table()` | `charge_table.csv` |
| `fund_scenario_file` | `fund_scenario_table()` | `fund_scenario_table.csv` |
| `rentenfaktor_file` | `rentenfaktor_table()` | `rentenfaktor_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `FRV_DE_S/` without the CSVs
and it will read fine, then fail on first evaluation. What you gain is that a diff of the
model shows logic changes only, and an input can be swapped in place — point
`Data.mort_file` at another same-schema file and the projection follows, with no formula
change. Tests cover both halves of that bargain.

**Every file but `model_point_table.csv` carries a `provenance` column**, one tag per row,
and the conventions suite asserts it: that is delib's second ruling, the citation discipline
reaching the data files rather than stopping at the prose. The model point table is the one
exemption, because a model point is a *configuration* — one policy's own terms — and not an
assumption.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points. **Point 1 is the worked-example anchor cell** (M37 / monthly 200,00 € / 30 years / *Rentenbeginn* at 67 / *Beitragsrückgewähr* / `std_gross` / `base`). Points 2–13 exercise the *Einmalbeitrag*, all four frequencies, a `pct_fund` and a `sum_assured` death benefit, an in-force cell opening at duration 96, a *beitragsfrei* cell on a zero-return fund, a *Zuzahlung* and a *Teilentnahme*, a *Beitragsdynamik*, a *Nettotarif* on an ETF, a two-year premium term on a stress path, a non-zero *Stornoabzug*, and a *Rentenbeginn* at 70 where the `max()` bites | anchor cell **[std]**, the technical notes' worked example |
| `mort_table.csv` | First-order annual death rates, ages 18–100 | **[std]** Gompertz-form proxy `0.00080 × 1.10^(age − 37)`, **anchored at `q(37) = 0.00080`** — the value the worked example rests on. *Not* DAV 2008 T, which is DAV property and is cited, never shipped [R17] [REG-R48]. A replacement must preserve the anchor, an insured-lives gradient, and a first-order margin **above** best estimate |
| `lapse_table.csv` | Annual lapse by policy year: 6 % in years 1–5, 3 % in 6–10, 2 % in 11–12, 3 % from 13 | **[std]** — **no German unit-linked *Stornoquote* was established anywhere**. The front-loading is a structural inference from the exit terms [R1] [R2] [REG-R45]; the ×2.5 tax step is applied in `Projection`, not stored here, because it depends on the attained age as well as the duration |
| `charge_table.csv` | Four tariffs: `std_gross`, `std_netto`, `std_high`, `std_low` | **[std]** throughout but for `alpha_rate` on `std_gross`, which is the 25 ‰ cap [R12] [R13] [REG-R16], and the 60-month spread [R1] [REG-R28]. **No charge level of any kind was established at any carrier**; the gap between `std_gross` and `std_netto` is the acquisition load [S18] |
| `fund_scenario_table.csv` | Gross return and TER by `(scenario_id, policy_year)`: `base`, `etf`, `zero`, `stress` | **[std]** deterministic paths. Not forecasts and **not PRIIPs scenarios** — those are derived from an underlying's own return history [R8] [R9] [REG-R32] — so nothing here may be compared with one |
| `rentenfaktor_table.csv` | Guaranteed and current factors by `(factor_id, annuity_age)`, ages 60–75 | **[std] and derived, not observed**: `10 000 / (12 · T_eff(x))` with `T_eff(x) = 100/3 − 0.75 (x − 67)` at a 0 % *Rechnungszins* [S10] [R16] [R22] [REG-R49], exactly **25,00 at 67**. `std_2026` sets the current factor equal to the guaranteed one; `rich_current` sets it 12 % higher |

## Modules that are off in the base run

Three constructions are implemented and switched off, so the base run reproduces the worked
example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Dynamic lapse | `lapse_dyn_beta` | `0.0` | `lapse_dyn_add(t) = β · max(0, 1 − av_pp(t)/cum_prem_pp(t))` raises the lapse rate while the contract is under water against the premiums paid — unit-linked lapse is market-sensitive precisely because the exit is at fund value on short notice [R1] [R2]. 0.15 is the reference value; **no German calibration for a coefficient of any size exists in this corpus**. Switched on it bites hardest on model point 12, whose stress path leaves the fund far below premiums paid for years |
| *Ablaufmanagement* | `ablauf_flag` (model point) | `False` on twelve of thirteen | A linear ramp of the **gross** return from the scenario's rate to `mmkt_return_ann = 1.50 %` over the last `glide_months = 60` months. With one fund and a deterministic return a reallocation and a change of assumed return are the same thing, so this is the honest representation of what is known — and **nothing about a real *Ablaufmanagement* was established**, not whether it is opt-in, not the ramp length, not the destination. Model point 8 switches it on |
| *Überschussbeteiligung* | — | not implemented | A unit-linked contract's surplus arises from the risk and cost results only [R5] [R14] [REG-R9] [REG-R18]; the model computes the risk result and credits none of it back. The omission biases the projected *Fondsguthaben* **downward**, which is the honest direction for a charge demonstration |

Hybrid and guarantee designs — *statisches* and *dynamisches Hybrid*, *Zwei-* and
*Drei-Topf-Hybride*, i-CPPI, *Wertsicherungsfonds* — are described in the product
specification and are **deliberately not implemented**. Each is a rule for reallocating
between a guaranteed pot and a risky pot along a path, and its entire content is what it
does when the risky pot falls. A deterministic projection has one path and it is a smooth
one, so a guarantee mechanism modelled inside it either never triggers — dead code presented
as a feature — or triggers on a hand-chosen shock the model has no basis for. What would
have to be added is named instead: a multi-scenario or stochastic asset model, a monthly
reallocation rule, a guaranteed pot accreting at a *Rechnungszins*, and a
*Wertsicherungsfonds* return model. That is a different model.

`kapitalwahl` is a fourth switch and changes no cash flow by design: both routes release the
same *Fondsguthaben* from this model, the annuity being published rather than projected. It
is carried because the two tax regimes genuinely differ [R19] [R20] [REG-R41] [REG-R45] and
because take-up is the largest behavioural unknown in the product; **no take-up rate was
established**, so the base run annuitises.

## Sign convention

`net_cf` is **income positive** — charges in, expenses and the death strain out — which is
the notes' own orientation and the library-wide sign. `liability_cf` publishes the same
stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of
`result_cf()` so the identity is verifiable in the frame rather than only in prose. A
Solvency II best estimate of the non-unit liability is `Σ v(t) × liability_cf(t)` over the
relevant risk-free term structure, with the unit liability — the *Fondsguthaben* itself,
backed one-for-one by the *Anlagestock* — added at market value [R15] [REG-R6] [REG-R7];
nothing in this library discounts.

`expenses` is the notes' **total** and **includes commission**: the acquisition commission
and issue expense at `t = 1`, the inflating monthly maintenance expense, the renewal
commission on each gross *Beitrag*, and the per-event expenses of a death, a surrender and
an annuitisation. Commission is a *part* of that column, not a further line, so subtracting
both from the charge income would charge it twice. The worked example fixes the reading:
`expenses(1) = 1 800,00 + 200,00 + 4,00 + 3,00 + 0,0075 + 0,2571 = 2 007,26 €`, and the
first of those is the acquisition commission.

The shape to expect on a new-business cell is a large negative `net_cf` in month 1 —
−1 966,22 € on the anchor, because the 2,50 % commission and the issue expense both fall
there while the acquisition charge that funds them arrives over sixty months — then a thin
positive margin that grows with the fund as the *kapitalbezogene* charge compounds against
it. On the *Einmalbeitrag* cell the sign reverses: month 1 is **+1 060,45 €**, because the
3 250,00 € withheld at inception more than covers the acquisition cost and there is no
sixty-month recovery to wait for.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue and
`savings/CashValue_SE` for the account-value vocabulary: `pols_*` for policy counts, `av_*`
for the account value, `*_pp` for per-policy amounts, `*_rate` for rates, `claims(t, kind)`
with an uppercase `kind` string, and `av_pp_at(t, timing)` / `pols_if_at(t, timing)` for the
within-month reads. The technical notes use compact actuarial symbols; the full mapping
lives in the `Projection` Space docstring.

The chassis is shared with `frlib/products/assurance_vie_uc/UC_FR_S`, the French *unités de
compte* contract, and the shared names mean the same thing on both:

| Notes | Cells | Also on `UC_FR_S` | Why |
|---|---|---|---|
| `F(t)`, `F_τ(t)` | `av_pp` / `av_pp_at(t, timing)` / `av_at` | yes | The *Fondsguthaben* at the start of the month, at four named points inside it, and weighted by `pols_if`. The four timings are the processing order made addressable |
| `u(t)`, `Δu(t)` | `units_pp` / `units_bought_pp` / `units_cancelled_pp` | `units` / `fee_units` / `wd_units` | The state variable and its two movements. delib splits the cancellations into one cells because the identity that checks them has no price term |
| `K(t)` | `nar_pp` | `nar` | The *riskiertes Kapital* / the French *garantie plancher* net amount at risk, floored at zero in both |
| — | `death_strain` | `plancher_strain` | The only part of a death benefit the insurer funds |
| — | `av_releases` | `av_releases` | The unit-side total the benefit-funding identity reconciles against |
| `W(t)` | `withdrawals` | `withdrawals` | An owner election, never `claims_wd`: a *Teilentnahme* is not a claim |
| `A(t)` | `prem_to_av_pp` | `prem_to_av_pp` | The *Anlagebeitrag* — what is left of the month's money to buy units |

Three German terms of art keep their German form in the cells names, because each names a
quantity with a statutory or contractual definition and no English equivalent that would not
mislead: `beitragssumme()`, the base of the *Höchstzillmersatz* and not "total premiums";
`stornoabzug()`, a deduction whose validity conditions are statutory and not a "surrender
charge"; and `rentenfaktor_guar()` / `rentenfaktor_curr()` / `rentenfaktor_applied()`, euro
per 10 000 € and not an annuity factor in the actuarial sense.

Four cases needed care beyond the mapping:

| Notes | Cells | Why |
|---|---|---|
| `qᴵ(t)`, `q(t)` | `mort_rate_tariff` / `mort_rate` and their `_mth` forms | Two different rates: the first-order table prices the *Risikobeitrag*, the second-order one produces the claims, and the difference is the *Risikoergebnis*. `mort_rate` is the projection's own decrement, per the library's shared vocabulary |
| `w(t)` | `lapse_rate_base` / `lapse_tax_step` / `lapse_dyn_add` / `lapse_rate` / `lapse_rate_mth` | The library requires an annual `lapse_rate` beside the monthly one. The table rate, the tax-threshold multiplier and the dynamic addition are separate cells so each is testable on its own |
| `α(t)` | `charge_acq_pp` / `cum_charge_acq_pp` / `charge_acq_total` | The instalment, the ledger and the total the ledger must reach. `check_acq_charge` needs all three |
| `D(t)` | `db_floor_pp` / `db_pp` | The guaranteed floor and what a death actually pays. They differ by the fund, and keeping them apart is what makes `death_strain` exactly the net amount at risk |

`sex` and `kapitalwahl` are carried and drive no formula — the tariff is unisex from
21 December 2012 [REG-R34] and the capital option is a reporting split — but both are exposed
as documented cells rather than dropped, because the notes' model point attribute table lists
them and a silently missing column is worse than an inert one.

## Standardizations used

Every entry here is **[std]**. The rationale is what makes it honest; a guessed figure
dressed as an observation would not be.

| Standardization | Value | Rationale |
|---|---|---|
| Acquisition rate on the composite | 2.50 % of the *Beitragssumme* | The rate is the *Höchstzillmersatz* [R12] [REG-R16] — the only anchor in the whole stack. Taking **the cap** rather than an interior point demonstrates the binding constraint instead of inventing a level |
| Premium-based admin `beta_rate` | 4.00 % | Middle of an argued 2 %–10 % range; **no carrier level was established** |
| Fund-based admin `gamma_rate_ann` | 0.30 % p.a., taken as `/12` monthly | Middle of an argued 0.10 %–1.20 % range. Divided rather than compounded because a German tariff quotes a nominal monthly charge |
| *Stückkosten* `policy_fee_mth` | 3.00 € per month | Middle of an argued 0–5 € range. A euro amount, which is why it is the charge that consumes a small paid-up fund |
| *Zuzahlungskosten* | 2.50 % | Set equal to the regular acquisition rate; on a single premium it is the whole acquisition charge, there being no *Beitragssumme* to zillmer against |
| *Stornoabzug* on the composite | 0.00 % | Many unit-linked tariffs have none, and a non-zero one would be an unsourced number attached to a contested clause [R1] [REG-R36]. 2.00 % on `std_high` so the machinery is exercised |
| The three charge variants | `std_netto`, `std_high`, `std_low` | The ends of the argued range plus the commission-free tariff [S18]; the `std_netto`-to-`std_gross` gap **is** the acquisition load |
| Mortality proxy | `0.00080 × 1.10^(x − 37)`, ages 18–100 | DAV 2008 T is DAV property and is not redistributed [R17] [REG-R48]. Anchored at `q(37) = 0.00080` so the worked example reproduces exactly; the 10 % gradient is an insured-lives one |
| Best-estimate ratio `mort_be_factor` | 0.75, flat | Crude, and said to be. What it buys is a *Risikoergebnis* that is exactly 25 % of the *Risikobeitrag*, checkable with a calculator [REG-R47] |
| Monthly conversions | mortality `/12`, lapse and return geometric | The charge and the decrement must share a split; the lapse and return annual rates are the observables to reproduce |
| Lapse table | 6 / 3 / 2 / 3 % by duration band | **No German unit-linked *Stornoquote* exists in this corpus.** The front-loading is inferred from the exit terms [R1] [R2] |
| Tax-threshold lapse step | ×2.5 for twelve months from `max(13, 62 − entry_age + 1)` | The 12/62 rule [R20] [REG-R45] is the strongest single driver of German surrender behaviour. Keying it on duration alone would fire fourteen years early on the anchor cell |
| Lapse cap / final-month lapse | 40 % / `lapse_rate_mth(n) = 0` | A cap so a dynamic module cannot produce an absurd rate; a zero final month because a surrender and an annuitisation are then the same event |
| Fund paths and TER | 5.00 % gross, 0.45 % TER on `base`; `etf`, `zero`, `stress` | Round, clearly-labelled assumptions. **Not forecasts and not PRIIPs scenarios** [R8] [R9] [REG-R32] |
| *Kickback* credited back | 0.00 % p.a. | The composite's fund is passive and pays no trail, which sidesteps two unresolved questions at once — whether an insurer may retain a *Bestandsprovision* [R15], and how a credited rebate enters the PRIIPs cost calculation [R7] [R8] |
| *Ausgabeaufschlag* | fully waived | German insurers are understood to buy at the *Rücknahmepreis*; no wording confirming it was seen |
| Guaranteed *Rentenfaktor* | 25,00 € per 10 000 € at 67, from `10 000/(12 T_eff)` | **Derived arithmetic, not a market observation.** A 0 % *Rechnungszins* [S10] on a generational annuitant basis [R16] is the *Sicherheitsabschlag* made concrete |
| Current *Rentenfaktor* | equal to the guaranteed one (`std_2026`); +12 % (`rich_current`) | Exercises the `max()` without injecting an unsourced uplift, and makes it visibly bite on one cell |
| Expenses and commission | acquisition commission 2.50 % of `S` + 200,00 € issue; 4,00 €/month inflating at 2 %; renewal 1.5 %; 150 / 50 / 100 € per event | **No German commission scale was established.** The acquisition commission is set **equal to the acquisition charge** so the model shows the financing problem the *Höchstzillmersatz* and the five-year spread exist to regulate. `comm_acq_rate` is a flat scalar, so on `std_netto` and `std_low` the assumed commission exceeds the tariff's own charge and those cells carry a projected loss — the flat assumption showing, not a product fact |
| Timing and processing order | premium in advance, return, fund charges, *Teilentnahme*, *Risikobeitrag*, deaths before lapses | The *Bewertungsstichtag* lag disappears on a monthly grid. Observing the net amount at risk before the charge that prices it is what makes `death_strain` exactly the *riskiertes Kapital* |
| Negative-fund safeguards | `min(.., remaining)` on the *Stückkosten* and the *Risikobeitrag* | A floor, not a tariff term; **no shipped model point triggers one**, and a contract that did would in practice have had its cover terminated |
| *Beitragsfreistellung* as an election | `pup_month`, no cohort paid-up rate | A cohort rate needs one sub-cohort per paid-up month for a second-order effect. The **[std]** 1 % p.a. is recorded and not implemented; the omission biases charge income upward |
| Modules off in the base run | `lapse_dyn_beta = 0`, `ablauf_flag = False`, no *Überschuss* credit | Base-run values, so the worked example reproduces with the machinery still there |
| The thirteen model points | see the input table above | Configurations, not assumptions — which is why they are the one provenance-exempt file |

The quantities in this model that are **not** standardizations are the acquisition-charge
cap and its five-year spreading [R1] [R12] [R13] [REG-R16] [REG-R28], the
*Beitragsverrechnung* order [S1], the *Beitragsrückgewähr* shape [S2], the
`max(guaranteed, current)` factor rule [S4] [R22], the *Zeitwert* *Rückkaufswert* and the
conditions on a *Stornoabzug* [R1] [REG-R36], the survival of the fund-based charges into a
*beitragsfrei* contract [R3], the unisex tariff [REG-R34], and the structural rule that the
insurer guarantees units and not their value [S1] [R15] [REG-R7].

## Tests

`tests/test_fondsgebundene_rentenversicherung_de.py` asserts the notes' worked example — all
seventeen printed rows of Panel A to the cent and `pols_if` to six decimals, Panel B's
benefit columns, Panel C's per-policy unit side, and every column total at full precision —
the notes' three independent rebuilds (month 1 from the tariff alone, month 61 at the cliff,
and the reduction in yield as a savings account), the four closure identities, the
*Einmalbeitrag* variant's printed table, the four-tariff reduction-in-yield comparison, and
**one test per listed modeling pitfall**: the fund-based charge cancelling units rather than
netting off the premium, the TER never appearing as a policy charge, the two mortality
bases living in two files, the risk result being exactly a quarter of the risk charge, the
two monthly conversions staying different, the net amount at risk floored at zero, the
acquisition instalment stopping at its window, an in-force cell never being charged again
for acquisition, the *Beitragssumme* being invariant, *Storno* and *Beitragsfreistellung*
staying two decrements, the *Rückkaufswert* being the fund itself, the *Stornoabzug* not
being built out of unamortised acquisition costs, no account-value benefit reaching
`net_cf`, the age at *Rentenbeginn* not being off by one, the `max()` factor rule biting,
the *Ratenzahlungszuschlag* not being applied twice, the *Beitragsrückgewähr* base being the
premiums paid, and no fixed charge driving the fund negative. The seven `check_*()`
identities and their residuals are asserted on the anchor and on every model point the
pitfall tests touch.

The library-wide house style — layout, docstrings, naming, the retired-name register, the
`check_net_cf` ruling, the `provenance` ruling, the model point sweep and the round trip —
is asserted separately, once, in `tests/test_model_conventions_de.py`, which owns the only
whole-table sweep in the library.

```bash
python -m pytest lifelib/libraries/delib/tests -q
```
