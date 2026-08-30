# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/basisrente/technical-notes.md`](technical-notes.md); the product it implements is
specified in [`product-spec.md`](product-spec.md), and the sources are in
[`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** What is sourced
> here is the *shape* of the product and almost none of its levels. The contractual mechanics
> are cited — the five prohibitions and the absence of any *Rückkaufswert* at any duration
> [R1] [R14] [REG-R39] [REG-R28]; the confinement of survivor cover to a spouse, registered
> partner or *Kindergeld*-eligible child, and the rule that everything paid to a survivor is
> paid as an annuity [R1]; the *Beitragsfreistellung* right of § 165 VVG [R14]; the
> *Höchstzillmersatz* of 25 ‰ of the *Beitragssumme* [R16] [REG-R16]; the
> *Höchstrechnungszins* ladder that fixes each cohort's `gtd_rate` [R16] [REG-R14] [REG-R15];
> the statutory *Überschussbeteiligung* [R15] [REG-R24]; and the `max(garantiert, aktuell)`
> conversion rule [R17] [S1] — and **every level is a standardization**. Not one carrier's
> Basisrente *Bedingungswerk*, *Produktinformationsblatt* or declared-rate history was reached
> [S1]–[S16]: direct HTTP egress is blocked in this build environment and the session's search
> budget was exhausted before this product. The DAV tables (DAV 2004 R here) are the property
> of the Deutsche Aktuarvereinigung, are not public, and are cited by name and never
> redistributed [R17] [REG-R47] [REG-R49]. Replace the decrement, charge and surplus tables
> with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/basisrente/run.py         # the anchor cell
python products/basisrente/run.py 5       # the Einmalbeitrag variant
python products/basisrente/run.py 13      # the cell where the guaranteed Rentenfaktor binds
```

Three lines to the same thing:
```python
import modelx as mx
model = mx.read_model("products/basisrente/Basis_DE_A")
model.Projection[1].result_cf()
```
`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by projection year `t` with one column per
cash flow line, and `result_pols()` the decrement, rate and per-policy side beside it, which
is what a reader needs to follow the worked example's independent checks. The model and both
its Spaces carry docstrings — `model.Projection.doc` holds the full mapping between the
technical notes' symbols and the cells names, and `model.Data.doc` says what each input file
is and, for the mortality table, what it is **not**.

## The product is a list of prohibitions, and the model is too

This is the one thing a reader arriving from `KLV_DE_A` or `RV_DE_A` will get wrong, and it is a
set of **absences** rather than a parameter, so nothing in the output points at it. The
entitlement is *nicht vererblich*, *nicht übertragbar*, *nicht beleihbar*, *nicht veräußerbar*
and *nicht kapitalisierbar* [R1] [REG-R39] — arithmetically:

| Limb | What the model does **not** have |
|---|---|
| *nicht kapitalisierbar* | No `cv_pp`, no `surr_value_pp`, no `claims_lapse` column, no *Kapitalwahlrecht* switch, no *Teilkapitalauszahlung*, no *Kleinbetragsrenten-Abfindung* |
| *nicht veräußerbar* | No surrender decrement and no `surr_rate`; § 169 VVG and its *Stornoabzug* are inoperative [R14] [REG-R28] |
| *nicht beleihbar* | No `loan_pp`, no `loan_bal` — a name delib's retired-name register bars in any case |
| *nicht übertragbar* | No assignment decrement; the *Versorgungsausgleich* is the one permitted transfer and is not modelled |
| *nicht vererblich* | No death benefit at all in the base run, and no lump sum to anyone at any date |

`check_no_capital()` asserts the consequence at every `t`: the total of `claims(t)` is
**exactly** the sum of its three permitted kinds, and `claims(t, "DEATH")` is zero wherever the
survivor rider is off or `t ≥ ret_t()`. The absences themselves cannot be asserted from inside
the model — a missing cells has no formula — so `tests/test_basisrente_de.py` asserts the name
list instead. The mirror error is subtler: computing a *Rückkaufswert* internally "for
reference" and flooring the *Deckungskapital* at it. `prem_to_av_pp(t)` is **negative** in the
first years of a heavily zillmerised contract and is **not** floored, because there is no
*Rückkaufswert* for a floor to protect — which is why a German *Deckungskapital* starts near
zero.

## A *Beitragsfreistellung* is not a lapse

§ 165 VVG survives intact on this contract and is its **only** behavioural exit [R14], but it
removes the *premium*, not the *policy*: the contract stays certified, stays protected, keeps
being credited and still converts at *Rentenbeginn*. So the model carries **two ledgers** and
`pols_if(t + 1) = pols_if(t) × (1 − mort_rate(t))` with `bf_rate` **absent from the identity**.
On the anchor the two series come apart completely: by `t = 23` the in-force count has fallen
only to 0,932780 while the premium-paying count has fallen to 0,512516, and the 0,441765
difference is a cohort still in force, still credited and still converting.
`check_pols_roll_fwd()` asserts both limbs — that the ledgers sum to `pols_if` and that
`pols_if` decrements on mortality alone. The two ledgers carry **different account values**, and that asymmetry is the whole economic
content of the freeze: `av_pp_at` is **per premium-paying policy**, `av_pu_at` is the
premium-free block **at fund level**, and a premium-free policy keeps paying the *Stückkosten*
and the reserve charge γ out of its own reserve while it stops paying β and the *Zillmerung*
instalment α. They must not be averaged into one per-policy figure — a policy that froze at
duration 5 and one that froze at duration 15 hold different reserves — and on the anchor
`av_pp(10)` is 82 934,50 € against 39 549,19 € for the premium-free block's average policy. Only
the fund-level total rolls forward on mortality alone,
`av_at(t + 1, "BEF_PREM") = av_at(t, "AFT_INT") × (1 − mort_rate(t))`, which is
`check_av_roll_fwd()`. It closes **across a freeze**, because a freeze moves reserve
between the blocks without removing any, and it closes **whether or not the survivor rider is
on**, because the reserve of a policy terminated by death leaves the fund either way: as a
claim where an eligible survivor exists, as a mortality profit where none does. That single
identity is the arithmetic content of *nicht vererblich*. A model point opens **entirely**
premium-paying or **entirely** premium-free (`paidup_at_init`, model point 7); a part-paid-up
book is two model points. And **no *Wiederinkraftsetzung* is modelled** — premiums can in
practice be resumed within a window [R14], but none was established, so the premium-free block
is absorbing: conservative on premium income, and a standardization rather than a contract
fact.

## The declared rate is the *total* credited rate

`cred_rate(t) = max(gtd_rate, decl_rate(t))` — a **maximum**, not a sum. A German *laufende
Verzinsung* is quoted as the total rate credited to the *Deckungskapital*, already including the
contract's *Rechnungszins* [R15] [R16] [REG-R24]; adding one to the other is the notes' sixth
pitfall and over a twenty-two-year deferment it is worth a great deal.
The guarantee is a **cohort fact fixed at conclusion** and carried on the model point, so a
book spanning the 2,75 % vintage of 2006 and the 1,00 % vintage of 2025 has both branches of
the `max` live at once [REG-R14] [REG-R15]. The shipped model points carry four distinct
vintages — 1,00 %, 1,75 %, 2,25 % and 2,75 % — and both branches are exercised: on the anchor
the declared path (2,60 % / 2,40 % / 2,20 %) binds at every `t`, while on model point 8 the
2,75 % guarantee stands above the whole declared path and binds at every `t`. The reserve
charge γ is netted **inside** the same crediting step, `(1 + cred_rate(t) − gamma_av)`, and
the *Stückkosten* are taken before it.

## Charges are insurer income; expenses are insurer outgo

Four amounts are struck against the policyholder's *Deckungskapital* — the *Zillmerung*
instalment α, the premium charge β, the reserve charge γ and the *Stückkosten* u — and all four
are **insurer income**. The insurer's own **outgo** is a different list: the acquisition
expense, the commission, the maintenance expense and the annuity administration. Booking a
charge as both is the notes' fourth pitfall, and it is why `expenses(t)` is invariant to
`beta_prem`, `gamma_av` and `zill_rate`: raising all three moves not one euro of `expenses` or
`commissions`, and moves `net_cf` **only** through the smaller annuity that a smaller fund buys
at *Rentenbeginn* — 249 887,21 € of annuity claims against 270 016,08 €.

The *Zillmerung* is **spread over five years and capped at 25 ‰ of the *Beitragssumme***
[R16] [REG-R16]. `alpha_amort_pp(t)` is equal at `t = 1 … 5`, zero from `t = 6`, and the five
instalments sum to `zill_rate × beitragssumme_pp()` exactly. The window is a window of the
**contract**, not of the projection, so model point 6 — in force at `duration_init = 17` —
sees `alpha_amort_pp(t) = 0` at every `t`; on a single-premium contract the five instalments
still run and the debit outlives the one premium that paid for it. One arithmetic coincidence
in the worked example is not a coincidence: `commissions(1) = 0.025 × S = 4 094,85 €` is the
same number as `alpha_total_pp()`, because the initial commission rate and the
*Höchstzillmersatz* are both 2,5 %. That is the German design — what the insurer pays out at
inception is sized to what it may write into the reserve — and it is why moving
`comm_init_rate` without moving `zill_rate` opens a first-year hole that nothing closes.

## The premium is a stream, not a level amount

A Basisrente model that offers only a level regular premium models the wrong product
[REG-R39]. The contribution has three components and only the first two are contract facts:

```
prem_base_pp(t) = prem_base_pp x (1 + prem_dyn_rate)^duration(t)    # contractual
prem_pp(t)      = prem_base_pp(t) x prem_freq_load()                # contractual
zuz_pp(t)       = zuzahlung_pp x zuz_take_up(duration(t) + 1)       # behavioural
```

The *Beitragsdynamik* compounds on the base premium from **inception**, so it is keyed to
`duration(t)` and not to `t` — which is what makes an in-force model point work: model point 6
opens at `3 600,00 × 1,02^17 = 5 040,87 €`, not at 3 600,00 €. The *Ratenzahlungszuschlag*
`prem_freq_load()` multiplies the *laufender Beitrag* and **nothing else**: not the *Zuzahlung*,
which is a single payment, and not an *Einmalbeitrag*, for which it is 1,000. Both streams stop
at `ret_t()`, and the *Zuzahlung* stops again once `duration(t) ≥ zuzahlung_end_dur`.
`zuz_take_up` is published as a cells of its own rather than hidden inside `zuz_pp`, because it
is a **utilisation rate and not a contract term** — the top-up is paid out of a profit not
known until the year end — and a model that treats the *Zuzahlung* as contractual has quietly
set it to 1.0. `prem_total_pp(t) = (prem_pp(t) + zuz_pp(t)) / (1 − buz_prem_share)` reconstructs
what the policyholder actually pays and is a **reporting cells that enters no cash flow**: the
BUZ premium buys a cover this model does not project, and `buz_prem_share < 0.50` is the
statutory invariant [R1], with model point 11 at 0.49, the boundary.

## The conversion at *Rentenbeginn*

One date in the contract's life, and nothing happens at it that the policyholder chooses:

```
fund_at_conv()         = av_at(ret_t(), "BEF_PREM") x (1 + terminal_bonus_rate)
rentenfaktor_applied() = max(rentenfaktor_gtd, rentenfaktor_curr()) x rf_option_factor()
ann_pp(ret_t())        = fund_at_conv() / pols_if(ret_t()) / rf_unit
                         x rentenfaktor_applied() x ann_freq
```

with `rf_unit = 10000` and `ann_freq = 12`. There is no lump sum, no election switch, no take-up
assumption and no notice period — three simplifications that follow from the ban on
capitalisation rather than from a modelling choice [R1]. The *Schlussüberschussanteil* is
allocated at this single date and at no other, which is a **contract fact**: with no surrender
there is no earlier exit for a terminal bonus to attach to [R15]. The `max` is a genuine
discontinuity, so the projection is sensitive to whichever factor is
higher and **completely insensitive to the other**. Both branches ship: the anchor converts at
the current 31,50 € against a guaranteed 28,00 € (which would have given 6 721,70 € instead of
7 561,91 €), while model point 13 converts at its guaranteed 34,00 € against a `low`-scenario
current 27,72 €, the guarantee there being worth 824,65 € a year against the current factor's
3 640,01 €. Model point 6, a 2009 tariff converting at 60, is the second such cell.

**The conversion basis is not the projection basis, and that is deliberate.**
`rentenfaktor_gtd` was struck at inception on **first-order** DAV 2004 R [R17] [S1]; the
projection runs on the best estimate, `mort_rate(t) = mort_be_factor × mort_rate_base(t)`. The
wedge between them is the payout phase's *Risikoüberschuss*, and `ann_bonus_rate` — a
*teildynamische Rente* — is what gives it back, so `ann_pp(ret_t())` is **exactly invariant** to
`mort_be_factor` while `claims_annuity` is not: dropping the factor from 0.85 to 0.70 leaves the
annuity at 7 561,9135 € to the last bit and lifts the annuity claims from 270 016,08 € to
296 364,48 €. A model that converted on its own best-estimate mortality would abolish the wedge,
and with it the whole German payout-phase surplus mechanic. `check_conversion()` inverts the
identity at `ret_t()` and is zero at every other `t`, so it catches a factor applied per policy
instead of per fund, an `ann_freq` of 1, an `rf_unit` of 1 000 — and a second conversion, of
which there can be none.

## Death, the survivor channel and the *Rentengarantiezeit*

With the survivor rider off — `surv_annuity_rate = 0`, the base design and the anchor's setting
— a death in the *Aufschubphase* pays **nothing**, and `claims_death` is a column of zeros,
published rather than dropped, because a column of zeros states the product fact where a missing
column would only hide it. With the rider on, `claims(t, "DEATH") = elig_surv_prob × mort_rate(t) × av_at(t, "AFT_INT")` —
the released reserve, weighted by the probability that an eligible survivor exists at the moment
of death [R1]. It is **not a lump sum to a beneficiary**: everything paid to a survivor must be
paid as an annuity, so what is booked is the reserve leaving this contract as the **single
premium of a survivor's annuity**, itself a new liability — an immediate annuity, `Sofort_DE_S` —
that this model does not project. The cover is paid for through `rf_option_factor()`, a
reduction in the *Rentenfaktor*, rather than by scaling the death benefit, which is how a German
tariff prices it: model point 3 converts at `31.50 × 0.930 = 29,295 €`.

A *Rentengarantiezeit* runs `guarantee_period_y` years **from *Rentenbeginn***, not from each
death, so every continuation ends on the same date and `pols_gtd` is a one-line recursion
closing at `gtd_end_t()` — `t = 25` on model point 4, with `pols_gtd(26) = 0` however late the
death that started it. Each death contributes `elig_surv_prob` of a continuation, and where none
exists the payments simply cease. They are **never commutable**:
`claims(t, "SURVIVOR") = ann_pp(t) × pols_gtd(t)` is a stream, and nothing in this model
discounts a continuation into a capital sum.

## Mortality is generational, and the terminal age is absorbing

DAV 2004 R is a *Generationentafel*: the improvement lives **inside** the basis rather than
being applied on top of it [R17] [REG-R49]. So `mort_rate_at_age(x, y)` takes a calendar year as
well as an age, `cal_year(t)` is carried on every model point, and two points that reach the
same attained age in different calendar years see different rates — model points 6 and 9 both
reach age 60, in 2029 and 2036, at 0.00467744 and 0.00420787. Treating the basis as a period
table is the notes' fifteenth pitfall.

`mort_rate(t)` is **1.0 wherever `age(t) ≥ omega_age()`**, whatever `mort_be_factor` says.
Without that rule the generational trend carries the shipped table's own terminal rate below 1
in every calendar year after the base year — 0.19920354 at age 120 in 2101 — and would leave a
residue in force after the end of the table; with it, `pols_if(proj_len() + 1) = 0` exactly, the
decrements sum to 1,000000, and there is no tail state and nothing left to pay.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py`; `Basis_DE_A/` holds only
formulas:

```
products/basisrente/
  model_point_table.csv  mort_table.csv  surplus_table.csv    <- inputs live here
  rentenfaktor_table.csv  charge_table.csv  behaviour_table.csv  option_table.csv
  run.py  model.md  product-spec.md  technical-notes.md  sources.md
  Basis_DE_A/  <- formulas only: __init__.py  _system.json  Data/  Projection/
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the model and
reads it at run time, and is the opposite of `basiclife/BasicTerm_S`, which stores its inputs
*inside* the model through modelx's IOSpec machinery — hence no `_data/` and no embedded values.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache, and readers placed there would re-read every file for every policy.
They live instead in an unparameterized **`Data`** Space, which `Projection` references as `data`
— so each file is read once per model however many policies are projected, and the conventions
suite counts the reads and asserts the file set.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `surplus_file` | `surplus_table()` | `surplus_table.csv` |
| `rentenfaktor_file` | `rentenfaktor_table()` | `rentenfaktor_table.csv` |
| `charge_file` | `charge_table()` | `charge_table.csv` |
| `behaviour_file` | `behaviour_table()` | `behaviour_table.csv` |
| `option_file` | `option_table()` | `option_table.csv` |
`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read, so it
works wherever the repository is checked out. **The trade-off:** the model is not portable on its
own — copy `Basis_DE_A/` without the CSVs and it reads fine, then fails on first evaluation —
and what you gain is that a diff shows logic changes only and an input can be swapped in place.
**Every file but `model_point_table.csv` carries a final `provenance` column**, one tag per row —
delib's second ruling, asserted by the conventions suite; a model point is a *configuration*
rather than an assumption, and that is the only exemption.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points, 25 attributes each. **Point 1 is the worked-example anchor cell** (M45 → 67, concluded 2026, 6 000 € annual + 4 000 € *Zuzahlung*, 2 % *Dynamik*, `gtd_rate` 1,00 %, no riders). Points 2–13 exercise the *Einmalbeitrag*, all four payment frequencies, all three in-force shapes, the survivor's annuity and the *Rentengarantiezeit* separately and together, both age-floor cohorts, four guarantee vintages, and four boundary cases | anchor cell **[std]**, the technical notes' worked example |
| `mort_table.csv` | First-order `qx` and the improvement `trend` by age 20–121 | **[std]** DAV 2004 R-shaped proxy `min(1, 0.014000 × 1.085^(age − 67))` with a flat `trend = 0.015`. *Not* DAV 2004 R, which is the DAV's property and is cited, never shipped [R17] [REG-R47] [REG-R49]. **The anchor a replacement must preserve is `qx(67) = 0.014000`**, because the worked example converts at 67; it must also stay generational, stay first order, and end at an age where `qx = 1.0` |
| `surplus_table.csv` | `decl_rate` and `ann_bonus_rate` by scenario and `t` | **[std]** — 2,60 % / 2,40 % / 2,20 % declared, 1,0 % *Überschussrente*. A scenario, not a forecast: **no declared rate specific to a Basisrente was established anywhere in the delib corpus**, and the sibling files' rates are Schicht-3 and endowment figures that must not be relabelled |
| `rentenfaktor_table.csv` | `rf_curr` by scenario and conversion age 60–75 | **[std]** — 31,50 € at 67, graded 3,5 % per year of age; the `low` scenario is 0.88 of it, and exists so model point 13 exercises the other branch of the `max`. **No *Rentenfaktor* level, range or time series exists anywhere in the delib corpus**, for this or any product (gap 4) |
| `charge_table.csv` | One row per tariff: the four account charges, the *Schlussüberschussanteil*, and the insurer's own expense and commission scale | `zill_rate` 25 ‰ (and 40 ‰ pre-LVRG) is [R16] [REG-R16] [REG-R20]; **everything else on the row is [std]**. Two tariffs ship, differing only in `zill_rate`, so the in-force cohorts carry their own cap |
| `behaviour_table.csv` | `bf_rate` and `zuz_take_up` by `dur`, the **policy year** `duration(t) + 1` | **[std]**, and **no observed range exists**: no German insurer publishes a *Beitragsfreistellung* rate or a *Zuzahlung* take-up for this product (gap 3). The shape is argued from the product's structure; the levels are invented |
| `option_table.csv` | One multiplicative factor per option key | **[std]** — the *Ratenzahlungszuschlag* on the *laufender Beitrag* alone, and the *Rentenfaktor* reductions for a *Rentengarantiezeit* and a survivor's annuity, anchored on a Schicht-3 illustration that is [unverified] and expressly not transferable |

## The published checks

Six identities, each a `bool` over all `t` with a per-`t` residual companion
`check_*_resid(t)`, compared against `roll_fwd_tol = 1e-9` scaled by the run's own magnitude so
the tolerance means the same thing on a 300 € contribution and on a 30 826 € one.

**delib ruling 1 — the `check_net_cf()` identity, in one line:** `net_cf(t) = premiums +
zuzahlungen − claims_death − claims_annuity − claims_survivor − expenses − commissions`, read
from `result_cf()`'s **own published columns** rather than from the cells that produced them, so
a column added to the frame but not to `net_cf`, a mis-signed column, or one whose cells and
frame entry have drifted apart all leave a residual; `pols_if`, `pols_paying` and `av` are two
counts and a balance and are excluded by construction. The headline number of a cash flow model
must not be the one quantity nothing checks.

| Check | The identity it closes |
|---|---|
| `check_net_cf()` | the line above, at every `t` |
| `check_pols_roll_fwd()` | `pols_paying + pols_paidup = pols_if`, and `pols_if(t+1) = pols_if(t) × (1 − mort_rate(t))` — `bf_rate` absent |
| `check_av_roll_fwd()` | `av_at(t+1, "BEF_PREM") = av_at(t, "AFT_INT") × (1 − mort_rate(t))` before `ret_t()`; the account emptied at `ret_t()`; `av(t) = 0` after it |
| `check_conversion()` | the whole fund converts **exactly once**, at `ret_t()`, at `rentenfaktor_applied()`; residual zero at every other `t` |
| `check_no_capital()` | no payment other than an annuity instalment, a guarantee continuation or a survivor's single premium; `claims_death = 0` where the rider is off or `t ≥ ret_t()` |
| `check_annuity_roll_fwd()` | `ann_pp(t) = ann_pp(t−1) × (1 + ann_bonus_rate(t−1))` in payment, nothing in payment before `ret_t()`, and `pols_gtd = 0` past `gtd_end_t()` |

`check_no_capital()` is **structural rather than arithmetic** — trivially zero on the anchor by
construction, and published anyway, because what it guards against is not a slip but an edit.

## Modules that are off in the base run

Three constructions are implemented and inert on the anchor, so the base run reproduces the
worked example while the machinery stays visible and testable.

| Module | Switch | Off | What it does |
|---|---|---|---|
| Survivor's annuity | `surv_annuity_rate` (model point) | `0.00` | Turns on `claims_death` at `elig_surv_prob × mort_rate(t) × av_at(t, "AFT_INT")` and reduces the *Rentenfaktor* through `rf_option_factor()`. Model points 3 and 12 set it to 0.60 |
| *Rentengarantiezeit* | `guarantee_period_y` (model point) | `0` | Turns on the `pols_gtd` ledger and `claims_survivor`, and reduces the *Rentenfaktor*. Model points 4 and 12 set it to 10 and 20 years |
| BUZ | `buz_prem_share` (model point) | `0.00` | Read by `prem_total_pp` alone, which enters no cash flow. Model point 11 sits at 0.49, the statutory boundary [R1] |

`elig_surv_prob = 0.55` is a `Projection` Reference and is **inert on the anchor**, carried so
that model points 3, 4 and 12 can exercise it: on model point 3, setting it to zero removes the
whole of `claims_death` and moves no other column, the annuity staying reduced by the option
factor because a German tariff pays for the cover out of the annuity whether or not a survivor
is ever found. Three further constructions are **not** implemented and each absence is a
decision: the *Wiederinkraftsetzung* (no window was established), a provider transfer (gap 13)
and the *Versorgungsausgleich* (gap 14).

## Sign convention

`net_cf` is **income positive** — *laufende Beiträge* and *Zuzahlungen* in, death benefits,
annuity instalments, survivor continuations, expenses and commission out — which is the
library-wide sign. `liability_cf` publishes the same stream outgo-positive,
`liability_cf(t) = −net_cf(t)` exactly, and both are columns of `result_cf()` so the identity is
verifiable in the frame rather than only in prose. A Solvency II best estimate is
`Σ v(t) × liability_cf(t)` over the relevant risk-free term structure, plus a risk margin
[REG-R1] [REG-R2] [REG-R6]; nothing here discounts, and no *Deckungsrückstellung*,
*Zinszusatzreserve* or SCR is computed [REG-R14] [REG-R17]. Unlike `TD_FR_A`, `expenses` does
**not** include the commission: the notes' cash flow statement carries them as two lines and
`net_cf` subtracts each once. The shape to expect on the anchor is a first-year strain that is
**all commission** — the *Zillmerung* instalment of 818,97 € is an account deduction and costs
the insurer nothing — then twenty-one years of positive accumulation-phase margin, then a long
negative payout tail from `t = 23`.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue and
`savings/CashValue_SE` for the account-value vocabulary: `pols_*` for policy counts, plural
nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with
an uppercase `kind` string, `pols_if_at(t, timing)` and `av_pp_at(t, timing)` for the within-year
reads, and `check_*()` as a bool over all `t` with `check_*_resid(t)` beside it. The notes use
compact actuarial symbols; the mapping lives in the `Projection` docstring, and four cases
needed care:

| Notes | Cells | Why |
|---|---|---|
| `A^p(t, ·)` vs `A^f(t, ·)` | `av_pp_at` / `av_pu_at` / `av_at` | Per **paying policy**, the premium-free block at **fund** level, and the fund-level total. Not three spellings of one quantity: only the third rolls forward on mortality alone, and collapsing the first two is the third pitfall |
| `f(t)` | `bf_rate` | Emphatically **not** `lapse_rate`. There is no lapse decrement on this product and no cells of that name anywhere in the model; a freeze is a transfer between ledgers, not an exit |
| `P(t)`, `Z(t)` | `prem_pp` / `zuz_pp` / `prem_total_pp` | Three different amounts: the *laufender Beitrag* with its frequency loading, the behavioural *Zuzahlung* with its take-up, and the total contribution including a BUZ premium that enters no cash flow |
| `q^t(x, y)`, `q(t)` | `mort_rate_at_age` / `mort_rate_base` / `mort_rate` | The generational table rate at an age and calendar year, that rate in projection year `t`, and the best estimate after `mort_be_factor`. The conversion is struck on the first family and the projection runs on the last |

**The chassis, and who else in delib is on it.** The mechanics here are those of an ordinary
German deferred annuity: `RV_DE_A` (`klassische_rentenversicherung`) is the same chassis
without the Schicht-1 constraints — full *Kapitalwahlrecht*, a *Rückkaufswert*, free
beneficiary designation — and `KLV_DE_A` carries the *Überschussbeteiligung* machinery both
inherit. The survivor's single premium this model books and does not project is an immediate
annuity, `Sofort_DE_S`; the BUZ it carries only as a premium share is `BU_DE_S`; the asset
forms it does not model are `FRV_DE_S` and `Index_DE_A`. `Riester_DE_A` is the other certified
layer and the useful contrast: a statutory *Beitragserhaltungsgarantie*, a permitted 30 %
*Teilkapitalauszahlung* and a *Kleinbetragsrenten* commutation, of which this product has none.
The model point's `policy_id` and `sex` drive no formula — pricing is unisex for contracts
concluded from 21 December 2012 [REG-R34] — and are exposed rather than dropped, because a
silently missing column is worse than an inert one.

## Standardizations used

Every row is **[std]** — a parameter or convention chosen where the sources are silent,
proprietary or unreachable. Nothing here is a market observation.

| Standardization | Value | Rationale |
|---|---|---|
| Mortality table | `qx = min(1, 0.014000 × 1.085^(age − 67))`, ages 20–121 | DAV 2004 R is the DAV's property and is cited, never shipped [R17]. Anchored at `qx(67) = 0.014000` so the worked example reproduces exactly |
| Improvement trend, and the terminal age | 1,5 % p.a. flat across ages from `mort_base_year = 2005`; `omega_age = 121`, absorbing | The trend keeps the basis generational, which is what a replacement must preserve; DAV 2004 R's own trends are age-dependent, so this is a simplification and a stated model risk. 121 is the age German annuity tables are conventionally carried to, and the absorbing rule is what makes the decrements sum to one |
| Best-estimate factor | `mort_be_factor = 0.85` | A round step from the shipped first-order table to a best estimate; the single largest unanchored number in the payout phase |
| Declared *laufende Verzinsung* | 2,60 % (t 1–10), 2,40 % (11–20), 2,20 % after | A scenario set above the 1,00 % *Höchstrechnungszins* by a plausible surplus margin and graded down, so the guarantee does not bind on the anchor. **No Basisrente declared rate exists anywhere in the corpus** |
| *Schlussüberschussanteil* and *Überschussrente* | 4,0 % of the fund at *Rentenbeginn*; `ann_bonus_rate = 1,0 %` p.a. compounding | The single-date allocation is a contract fact [R15] and the 4,0 % has nothing behind it. The uplift makes a *teildynamische Rente*: *volldynamisch* would consume the whole first-order margin and *konstant* none, and 1,0 % is deliberately in between |
| *Aktueller Rentenfaktor* | 31,50 € at 67, graded 3,5 % per year; `low` = 0.88 × base | Set **above** the guaranteed 28,00 € so `max(gtd, curr)` is visibly operative, and the `low` scenario below model point 13's 34,00 € so the other branch ships |
| Guaranteed *Rentenfaktoren* | 26,00 € to 34,00 € across the model points | Inside the argued 24 € – 34 € band for a *klassisch* tariff converting at 67 (gap 4) |
| Account charges β, γ, u | 7,5 % of each *Beitrag* and *Zuzahlung*; 0,35 % p.a. of the *Deckungskapital*; 36,00 € p.a. per policy, inflating | Mid-points of the argued 5 % – 10 % and 0,2 % – 0,6 % bands, and a placeholder *Stückkosten* charged to **both** ledgers, which is the economic content of a freeze |
| *Zuzahlung* acquisition charge | 2,5 % of each *Zuzahlung* | A top-up carries its own single charge instead of a share of the *Zillmerung*; whether *Zuzahlungen* enter the *Beitragssumme* at all was not established (gap 8) |
| *Zillmerung* spread, and the *Beitragssumme* it runs on | `zill_spread_y = 5` years of the **contract**; `S` = the escalating premiums to `ret_age`, **excluding** *Zuzahlungen* | The LVRG-era German market shape. Whether the AltZertG's five-year spreading reaches *Basisrentenverträge*, and whether *Zuzahlungen* enter `S` at all, were not established (gap 8); excluding them is the conservative reading, and `S` is the base of both the 25 ‰ cap and the initial commission |
| The option factors | *Ratenzahlungszuschlag* 1,000 / 1,020 / 1,030 / 1,050; `guarantee_period` 1,000 / 0,995 / 0,974; `survivor` 1,000 / 0,930 | The frequency ladder is a German market convention carried from the sibling delib corpus, with no tariff sheet behind it. The two *Rentenfaktor* reductions are anchored on a Schicht-3 illustration that is [unverified] and expressly not transferable, and the survivor factor has no anchor at all |
| Insurer expense scale | Acquisition 250,00 € at inception; maintenance 60,00 € and annuity administration 36,00 € p.a., inflating at 1,5 % | Round-number placeholders; the payout phase is administratively cheaper than the accumulation phase |
| Commission scale | 2,5 % of `beitragssumme_pp()` at inception, 1,5 % of premiums plus *Zuzahlungen* from `t = 2` | The initial rate is sized to the *Zillmerung* cap, which is the German design. [S2]'s 1 575 € specimen is the corpus's only datum and is [unverified]; no renewal level was established |
| *Beitragsfreistellung* rate | 4,0 % (years 1–5), 3,0 % (6–10), 2,0 % (11+) | Shape argued from the product's structure — penalty-free and reversible early, nothing realisable to leave for late. **The levels are invented** (gap 3) |
| *Zuzahlung* take-up | 0.70 (1–5), 0.85 (6–15), 0.90 (16+) | A utilisation rate, not a contract term. Rising because the contract and the habit bed in |
| Eligible-survivor probability | `elig_surv_prob = 0.55` | In substance a marriage-survival probability. **One of the most consequential [std] numbers in the whole delib library** |
| Annuity timing | Twelve instalments booked at the **start** of the payout year on `pols_if(t)` | A monthly annuity on an annual grid; generous to the year of death by up to a full year's annuity, concentrated in the tail. No German *vorschüssig*/*nachschüssig* convention was established (gap 21) |
| Processing order and age basis | Premiums in advance, interest at year end, death after interest, freeze after death; age last birthday at conclusion, stepping on the anniversary | The order is declared once and asserted, because every roll-forward identity depends on it. No German age convention was established, and mortality here drives the annuity's duration rather than a benefit amount, so a half-year offset is second order |
| The thirteen model points | — | Configurations, not observations: no carrier's entry ages, premium minima, permitted *Rentenbeginn* range or option terms were established (gap 1, gap 8) |

The only quantities that are **not** standardizations are the 25 ‰ and 40 ‰ *Höchstzillmersätze*
[R16] [REG-R16] [REG-R20], the `gtd_rate` ladder of *Höchstrechnungszins* vintages [R16]
[REG-R14] [REG-R15], and the structural rules — the five prohibitions and the absences they
impose, the *Beitragsfreistellung* right, the closed list of permitted survivors, the
annuity-only payout, the `max` conversion, the single-date terminal bonus and the 50 % BUZ
ceiling.

## Tests

`tests/test_basisrente_de.py` asserts the eighteen printed rows of the notes' worked example to
the cent and `pols_if` to six decimals, the totals over all seventy-seven years at full
precision (and that the sum of the rounded cells really does differ, in three of the six money
columns), the *Einmalbeitrag* variant's ten printed rows and its own totals, the model point 13
conversion table with both branches of the `max`, the notes' three independent checks rebuilt
from the charge scale up, the two closure identities — decrements summing to 1,000000 and the
Total row reconciling — and all six `check_*` identities with their residuals. Beyond the worked
example it asserts **one test per listed modeling pitfall**: no surrender value at any duration
and none of the names that would carry one; the *Beitragsfreistellung* absent from the in-force
roll-forward; the two account blocks not averaged; the account charges invariant in `expenses`;
the *Zillmerung* spread over five contract years and capped; the declared rate as a `max` and
not a sum; the premium stream keyed to the policy duration and stopping at *Rentenbeginn*; the
*Ratenzahlungszuschlag* on the *laufender Beitrag* alone; no death benefit with the rider off;
the death benefit conditional on an eligible survivor and never a lump sum; the conversion
invariant to `mort_be_factor`; the annuity booked in advance on the opening count; both branches
of `max(garantiert, aktuell)`; the *Rentengarantiezeit* running from *Rentenbeginn* and never
commuted; the generational table; the guarantee vintage attaching at conclusion; and the BUZ
carried as a premium share that reaches no cash flow.

```bash
python -m pytest lifelib/libraries/delib/tests/test_basisrente_de.py -q
python -m pytest lifelib/libraries/delib/tests/test_model_conventions_de.py -q -k Basis_DE_A
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-basisrente-r1
[R14]: #delib-basisrente-r14
[R15]: #delib-basisrente-r15
[R16]: #delib-basisrente-r16
[R17]: #delib-basisrente-r17
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R39]: #delib-reg-r39
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
