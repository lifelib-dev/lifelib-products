# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`products/indexpolice/technical-notes.md`](technical-notes.md); the product it implements
is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result**, and for this
> product the gap between those two things is wider than for any other model in the library.
> The *mechanics* are firm and are cited to the instruments that govern them: the index
> participation is a form of *Überschussverwendung* under § 153 VVG with **no independent
> statutory footing** [R1]; the capital sits in the *Sicherungsvermögen* and the contract is a
> conventional profit-participating one, **not** an *indexgebundene Lebensversicherung* in the
> balance-sheet sense [R15]; the guarantee falls due at *Rentenbeginn* in the *Neue Klassik*
> architecture [S6] [R12]; the option budget is the declared surplus and is bounded by the same
> MindZV minimum that bounds a classic contract's declared rate [R8]; the *Rückkaufswert* is a
> reserve floored by the five-year acquisition-cost spread of § 169 VVG [R2]; and the annual
> *Cap-Festlegung* is a unilateral determination reviewable under § 315 BGB [R22], not an
> adjustment of the contract under § 163 VVG [R4]. **Every number here was chosen as a [std] with
> a stated rationale, and none was fitted to a market observation.** The library was drafted under
> a blocked-egress policy with an exhausted `WebSearch` budget; that policy has since been lifted
> and the citations re-verified against the primary documents, and **32 of this product's 38 source
> entries now read `Retrieved: yes`**. Retrieval produced carrier levels the shipped parameters can
> be judged against but were not built from — Allianz's illustrative Cap of 3,2 % with a 75,00 %
> *Partizipationssatz* [S2] [S5], Stuttgarter's published *Partizipationsquote* of 70 % and
> *sichere Verzinsung* of 2,16 % [S8], Assekurata's 2026 index-segment declared average of 3,07 %
> [R20], and two carriers' cost disclosures [S4] [S11] — and **nothing here has been changed on the
> strength of them**: the standardization table below records, row by row, what each retrieved
> figure does to each value. What retrieval did not supply is a market panel of cap levels [R21] or
> any published entry-age band or minimum premium [S3] [S15]; and the DAV tables (DAV 2008 T, DAV
> 2004 R) are proprietary, are cited by name and are never shipped [REG-R48] [REG-R49]. Replace
> the decrement, charge and index tables with company data before drawing any conclusion from the
> output.

## Run it

```bash
python products/indexpolice/run.py
python products/indexpolice/run.py 8      # the in-force cell that reproduces Examples A and B
python products/indexpolice/run.py 11     # the same contract in the sichere Verzinsung arm
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/indexpolice/Index_DE_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy year `t` with twelve columns: the
five-line cash flow statement, the three credits and the balance beside it, and `net_cf` in
both orientations. The model and both its Spaces carry docstrings — `model.doc` describes the
product and what makes it *not* unit-linked, `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names, and `model.Data.doc` says what each
input file is, how each index path was built and which rows a replacement must preserve.

## The capital is in the *Sicherungsvermögen*, not an *Anlagestock*

This is the one thing a reader arriving from `FRV_DE_S`, `CashValue_SE` or `FIA_US_S` will get
wrong, and it is a fact about the product rather than a modelling choice. There is **no unit
account, no unit price and no fund value anywhere in this model**. The policyholder holds a
claim on the insurer measured in euros; `av_pp(t)` is a *Deckungskapital* that rolls forward by
a recursion; and `cv_pp(t)` is that reserve, floored by § 169 Abs. 3 VVG and less the
*Stornoabzug* — not a *Zeitwert* of units [R2] [R15]. Three consequences follow, and a
unit-linked reading gets each of them wrong:

- **The account cannot fall because of the index.** A bad *Indexjahr* credits zero; it never
  takes anything away. `av_pp_at(t, "AFT_CREDIT") ≥ av_pp_at(t, "AFT_GUAR")` at every `t` on
  every model point, the two differing by two non-negative credits.
- **There is no unit-pricing timing.** Values are struck once a year at the *Indexjahr*
  boundary, which is why this model is **annual** while the unit-linked `FRV_DE_S` is monthly.
- **The policyholder's downside is the opportunity cost of one year's surplus** and nothing
  more — the antidote to both usual misreadings, that the product can lose capital and that it
  is a cheap way to be long equities.

What the model deliberately does not carry: no *Anlagestock*, no unit fund, no bid-offer
spread, no *Zeitwert*, no market value reduction, no asset share.

## The payoff is a sum of capped monthly returns, floored once at the year

The contractual formula, implemented literally against an external table of monthly index
returns rather than approximated by an assumed credit rate:

```
x(t, m) = min( r(t, m), C(t) )          no floor on the month
S(t)    = sum over m = 1..12 of x(t, m) summed, not compounded
rho(t)  = max( S(t), 0 )                the floor is on the year
X(t)    = rho(t) . w(t) . G(t)          struck on the opening balance
```

Each of those four lines is a place an implementation goes wrong while still printing a
plausible number, and each is a numbered pitfall with its own test. The shipped equity path
`eqidx_vol17` carries the research file's two constructed *Indexjahre* at `t = 9` and
`t = 10` for exactly that reason, so the model **reproduces** them rather than restating
them:

| | `t = 9` (Example A) | `t = 10` (Example B) |
|---|---|---|
| raw monthly sum | +13.10 % | +7.00 % |
| `index_sum` (capped, summed) | **+8.90 %** | **−2.60 %** |
| `index_return_year` (compounded raw) | +13.4548 % | **+6.4402 %** |
| `index_credit_rate` | 8.90 % | **0.00 %** |

**Example B is the product's whole reputation in one row.** The index rose 6,4402 % over
the year and the credit was nothing. An implementation that floors each *month* at zero
gets `S = +12,60 %` here; one that compounds the capped returns gets 8,9599 % at `t = 9`
instead of 8,90 %; one that applies the floor to the compounded raw return credits 6,44 %;
one that applies the *Partizipationsquote* to it credits 3,86 %. All four are wrong and all
four look entirely plausible in a printout.

The *Partizipationsquote* design is not a variant of the Cap design but a different payoff that
fails differently, and both ship: `payoff_form = "quote"` computes `max(q(t) . Y(t), 0)` on the
compounded year return. Model points 1 and 2 run the two against the **identical** twelve
monthly returns in every year, so the difference is visible rather than argued — at `t = 10` the
Cap design credits nothing and the *Quote* design credits 3,8641 % of `G`, and at `t = 9` the
ranking reverses. `check_index_credit()` guards the arithmetic from the outside:
`0 ≤ rho(t) ≤ 12 . C(t)` in the Cap form, `0 ≤ rho(t) ≤ q(t) . max(Y(t), 0)` in the *Quote* form.

## One budget, two arms, and the *Wahlrecht* between them

The declared *Überschussanteilsatz* `b(t)` **is** the option budget. For a contract in the
index arm the same amount a classic contract would receive as interest is **spent** on the
option package instead of credited [R1] [R8]. It is therefore allocated exactly once, and
`check_surplus_alloc()` is the line that says so:

```
opt_budget_pp(t) + surplus_credit_pp(t) = surplus_rate(t) . index_base_pp(t)
```

An implementation that credits the declared rate *and* runs the index participation has spent
one budget twice; the result looks entirely plausible until this residual is taken, and the
residual is exactly the surplus that was double-counted. The same rule is why `guar_int_pp(t)`
credits the *Rechnungszins* and nothing more: in the index arm the contract credits the
guarantee and the index payoff, never the declared rate as well.

`elect_index(t)` — the notes' `w(t)` — is the *Wahlrecht*, a fraction in [0, 1] rather than a
flag, because some tariffs permit a partial election and all-or-nothing is then the special
case. It is a **behavioural** assumption and not a contractual one, and its path is read from
an external table: `always_index` (the base run), `always_safe`, `half_half`, `switch_at_15`.
The base run's `w = 1` is a **modelling choice made so that the model demonstrates the index
mechanic**, not a claim about behaviour: a base run in the safe arm would reduce this model to
`RV_DE_A`, and model point 11 is exactly that comparison. The model deliberately carries no
optimal-election rule, no inertia model, no distribution over paths and no within-year
switching: none is established for this product family, and a switching rule would put an
unevidenced behavioural assumption at the centre of the result.

## The lock-in ratchets the ledger, not the balance

*Höchststandsicherung*: a credit, once made, is permanently part of the guaranteed capital,
enters the base of every later *Indexjahr* and can never be lost. What the model ratchets is
`credit_cum_pp(t)` — the ledger of every credit, index and safe-arm alike — and hence
`guar_cap_pp(t) = guar_floor_pp(t) + credit_cum_pp(t)`.

**It is not the account balance that ratchets, and asserting that it does is a numbered
pitfall.** With the reserve charge `γ` at or above the guaranteed rate `i_g` the balance
*falls* in a year that credits nothing: model point 13 is a 0,25 % *Rechnungszins* cohort
whose premiums stop at year 12, and its `av_pp(t)` declines in every year from 14 to 22
while `guar_cap_pp(t)` is still monotone. `check_lock_in()` is therefore written on
`guar_cap_pp` and on the sign of the two credits, and says nothing about `av_pp`. Written on
the balance instead it would fail a correct implementation and pass a wrong one — one that
let a bad *Indexjahr* claw back a credit.

## The guarantee falls due at *Rentenbeginn*, and at no earlier date

That is what *Neue Klassik* means [S6], and it is the reason the insurer can hold a riskier
asset mix behind the guarantee and generate the surplus that becomes the option budget. In
the model:

- `guar_cap_pp(t)` enters **one** benefit, `mat_pp(n) = max(av_pp(n+1), guar_cap_pp(n+1))`,
  and no other. A death benefit and a surrender value are struck on the account.
- `av_pp(t) < guar_cap_pp(t)` at intermediate `t` is permitted and ordinary — on the anchor
  it holds at `t = 2 … 7`, while the *Zillmer* charge is still being recovered.
- The floor **binds nowhere on the anchor**: at `t = 28` the account stands at 73 511,39 €
  against a guaranteed capital of 63 171,44 €. Model point 9 exists so that it does bind — a
  100 % *Beitragsgarantie* against `zero_path` — because a model with no floor and one with a
  floor that never binds look identical on twelve of the thirteen points.

## Two exits at the same instant take different amounts

This is the product's own rule and a model that pays them alike has lost it. The credit
lands **after** the decrements and goes to the survivors, so:

| Exit | Struck on | Includes the year's *Indexjahr*? |
|---|---|---|
| death | `av_pp_at(t, "AFT_GUAR")`, floored at `death_min_rate . BS` | no |
| surrender | `max(av_pp_at(t, "AFT_GUAR"), min_surr_pp(t))` less the *Stornoabzug* | no |
| maturity | `av_pp(n+1)`, floored at `guar_cap_pp(n+1)` | **yes** |

A mid-year exit forfeits the running *Indexjahr*, and that is the rule in both retrieved AVB
rather than a standardization: the participation is credited only "zu Beginn des folgenden
→Indexjahres" ([S2] Ziffer 3.3, [S7] § 3 Ziffer 5), no unspent budget is refunded, and on
surrender Allianz adds only a pro-rata *Schlussüberschussanteil* and *Sockelbetrag* [S2]
Ziffer 9.2 Absatz 4 [R2]. The annual grid also silently gives every exit the *favourable* date — the
product rewards surrendering just after an *Indexjahr* ends — and that is a stated model risk
rather than a neutral convention. `av_released(t)` is the account the exits carry **out of the
fund**, deliberately not what they are *paid*: the death floor pays more than the account
releases, the *Stornoabzug* pays less, the *Beitragsgarantie* pays more. Those three differences
are insurer money and belong in `net_cf`, not in the roll-forward — which is what makes
`check_av_roll_fwd()` an exact identity rather than an approximate one.

## Charges are not expenses

A **charge** is a deduction from the policyholder's *Deckungskapital* (`prem_charge_acq_pp`,
`prem_charge_adm_pp`, `av_charge_pp`); an **expense** is the insurer's own cash outgo and is
the only one of the two that reaches `net_cf` (`exp_acq_pp`, `exp_maint_pp`). They are of the
same order here by construction, so the *Kostenüberschuss* is small. The model does **not**
close the MindZV loop — it does not compute a cost result, return half of it to the
policyholder and raise the declared rate [R8] — so changing an expense assumption changes
`net_cf` without changing what the policyholder receives. That is a stated limitation and the
one place where the model's economics are knowingly incomplete.

`av_min_pp(t)` is a **shadow** account carrying the same recursion with the acquisition
charge on the statutory five-year spread of § 169 Abs. 3 VVG, and it exists only to produce
`min_surr_pp(t)`. It is not the reserve, it is not published in the cash flow statement, and
it never touches a death or a maturity benefit. With `zill_years = 5` the two accounts
coincide exactly and the floor is a no-op — which is the point, delib's charge profile
already sitting at the statutory floor. The DeckRV *Höchstzillmersatz* and the § 169 VVG
spread are two different rules with two different functions — what may be **reserved**
against what must be **paid** — and conflating them is a numbered pitfall [R2] [R7].

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Index_DE_A/` holds nothing but formulas:

```
products/indexpolice/
  model_point_table.csv        <- inputs live here
  index_return_table.csv
  index_param_table.csv
  surplus_rate_table.csv
  election_table.csv
  mort_table.csv
  lapse_table.csv
  freq_load_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Index_DE_A/                  <- formulas only
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

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache. Readers placed there would re-read every file for every policy. They
live instead in an unparameterized **`Data`** Space, which `Projection` references as `data` —
so each file is read once per model no matter how many policies are projected, and the
conventions suite counts the reads and asserts the file set. `Data.input_dir()` resolves the
location from `_model.path.parent` when the model is read, so it works wherever the repository
is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `index_return_file` | `index_return_table()` | `index_return_table.csv` |
| `index_param_file` | `index_param_table()` | `index_param_table.csv` |
| `surplus_rate_file` | `surplus_rate_table()` | `surplus_rate_table.csv` |
| `election_file` | `election_table()` | `election_table.csv` |
| `mort_file` | `mort_table()` | `mort_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `freq_load_file` | `freq_load_table()` | `freq_load_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `Index_DE_A/` without the CSVs
and it will read fine, then fail on first evaluation. What you gain is that a diff of the
model shows logic changes only, and an input can be swapped in place — point
`Data.index_return_file` at another same-schema file and the whole *Indexjahr* mechanic
follows, with no formula change. That is the honest way to represent a fact established
qualitatively and not quantitatively, and it is how the volatility sensitivity of the
technical notes is run.

**Every file but `model_point_table.csv` carries a populated `provenance` column** — delib's
second ruling, machine-checked. A model point is a *configuration* rather than an
assumption, and that exemption is the library's only one.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points. **Point 1 is the worked-example anchor cell** (M40 → 67, 2 400,00 € a year for 27 years, Cap design, `eqidx_vol17`, `always_index`, 90 % *Beitragsgarantie* at `i_g = 1,00 %`). Points 2–13 exercise the *Quote* design, the house index, all four payment frequencies, a single premium, two in-force cells, the flat path where the guarantee binds, all four election paths, both *Kapitalwahlrecht* elections, both *Stornoabzug* settings and four *Rechnungszins* cohorts | anchor cell **[std]**, the technical notes' worked example |
| `index_return_table.csv` | Twelve monthly returns per `(index_id, t)`, 40 years, three paths | **[std]**. `eqidx_vol17` from `default_rng(20260829).normal(0.0060, 0.0500, size=(40, 12))` rounded to 4 dp, **with `t = 9` and `t = 10` overwritten by the research file's Examples A and B**; `houseidx_vol5` from `default_rng(20260830).normal(0.0025, 0.0144, …)`; `zero_path` all zeros. The anchors a substitute must preserve are the two example rows: `t = 9` must sum, capped at 3 %, to **+8,90 %** and `t = 10` to **−2,60 %** on a compounded raw return of **+6,4402 %** |
| `index_param_table.csv` | `cap` and `quote` by `(index_id, t)` | **[std]**, 3,00 % monthly and 60 % on the equity path, 6,00 % and 100 % on the house path; 3,00 % is the midpoint of an argued 1,5–5,0 % band. **Two carrier figures are now on record and neither is a market panel** [R21]: Allianz's worked illustration runs at a Cap of **3,2 %** with a *Partizipationssatz* of 75,00 % [S2] [S5], and Stuttgarter **publishes** a *Partizipationsquote* of **70 %** on its house multi-asset index for 1.2.2026–31.1.2027 [S8] — below the 100 % this file ships on the house path. Per year because the insurer redetermines them each *Indexjahr*; level here only because nothing else could be established |
| `surplus_rate_table.csv` | The declared *Überschussanteilsatz* by `t` | **[std]** 2,50 % level — **below the 2026 evidence**, Assekurata's survey giving *Indexpolicen* an average declared 3,07 % and classic private annuities 2,62 % [R20], and Stuttgarter publishing 2,16 % for its own safe arm [S8]. **This rate is the option budget**; the model consumes a declared rate and does not derive one from an investment result under the MindZV minimum [R8] |
| `election_table.csv` | `w` by `(elect_id, t)`, four paths | **[std]** and **behavioural**. No election distribution for this product family is established, in either direction |
| `mort_table.csv` | `qx` by sex and attained age 20–100 | **[std]** Gompertz proxy `0.001200 × 1.095^(age − 40)` with `qx(F) = 0.65 × qx(M)`. **Not** DAV 2008 T or DAV 2004 R: those are proprietary, are cited by name and are never shipped [REG-R48] [REG-R49]. **The anchor a replacement must preserve is `qx(M, 40) = 0.001200`.** It is a period table with no selection effect, and here mortality is a *timing* assumption rather than an amount one — but both properties matter greatly to the *Rentenfaktor*, which is why that is an input and not a computed quantity |
| `lapse_table.csv` | Base surrender by policy year: 5 % in years 1–2, 3 % in 3–11, **6 % in year 12**, 2 % from 13 | **[std]**. The year-12 step is the § 20 Abs. 1 Nr. 6 EStG threshold [R14] and is the shape's whole point; **no index-specific *Stornoquote* exists**, and the two market-wide GDV measures are irreconcilable [R19] |
| `freq_load_table.csv` | The *Ratenzahlungszuschlag* multiplier by frequency: 1,000 / 1,020 / 1,030 / 1,050 | **[std]** market convention; no carrier tariff established |

## The published identities

Six `check_*()` cells travel with the model. Each takes no argument and returns a `bool`
over all `t`, and each has a per-`t` `check_*_resid(t)` companion that gives the signed
residual of the year that failed.

**delib ruling 1 — `check_net_cf()` is mandatory, and this is its identity in one line:**

```
net_cf(t) = premiums(t) - claims(t, "DEATH") - claims(t, "LAPSE") - claims(t, "MATURITY") - expenses(t)
```

`net_cf` names the three kinds one by one while `check_net_cf_resid` takes the kind-less
total `claims(t)`, so the two agree only if the `claims(t, kind)` dispatch and the cash flow
statement carry the same list of kinds. Read against `result_cf()` it catches the pitfall
this product invites above all: adding `guar_int`, `surplus_credit` or `index_credit` into
`net_cf`. Those are movements of the policyholder's account and reach the insurer's cash
flow only later, through a benefit; any of them entering here would leave a residual the
size of the credit — 9 139,74 € over the anchor's projection.

| Check | What it asserts |
|---|---|
| `check_net_cf()` | the identity above, at every `t` |
| `check_av_roll_fwd()` | `av(t+1) = av(t) + prem_to_av(t) − av_charge(t) + guar_int(t) + surplus_credit(t) + index_credit(t) − av_released(t)`, every term on its own population |
| `check_pols_roll_fwd()` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t)`, **and** the three exits summed equal `pols_if_init()` |
| `check_surplus_alloc()` | `opt_budget_pp(t) + surplus_credit_pp(t) = surplus_rate(t) · index_base_pp(t)` |
| `check_lock_in()` | `guar_cap_pp` monotone, `index_credit_pp ≥ 0`, `surplus_credit_pp ≥ 0` |
| `check_index_credit()` | `0 ≤ index_credit_rate(t) ≤ 12 · index_cap(t)`, or `≤ index_quote(t) · max(Y(t), 0)` |

Tolerance is `roll_fwd_tol = 1e-8`, relative to the balance being checked.

## Modules that are off in the base run

Four constructions are implemented and switched off, so the base run reproduces the worked
example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| The *Partizipationsquote* payoff | `payoff_form` (model point column) | `"cap"` | Credits `max(q(t)·Y(t), 0)` on the compounded year return instead of the capped monthly sum. Model points 2 and 3 switch it on; the two designs fail differently and a specification may not describe one and price the other |
| The *sichere Verzinsung* arm | `elect_id` → `elect_index(t)` | `1.0` (full index) | Directs `1 − w(t)` of the declared surplus to `surplus_credit_pp`, guaranteed from the moment it is credited. At `w = 0` (model point 11) the contract *is* a `RV_DE_A` |
| The *Stornoabzug* | `surr_charge_on` (model point column) | `1` on twelve points, `0` on point 13 | 2 % of the floored base **[std]**. A tariff without the clause is a real configuration, not a special case: a deduction is effective only if agreed, appropriate and **quantified in the contract** [R2] |
| The max-of-two *Rentenfaktor* | `rentenfaktor_curr` | `25.0`, equal to `rentenfaktor_guar` | `max(guaranteed, current)` — a guarantee with upside. The two are set equal in the base run **[std]** so the rule is exercised by a test rather than by the base path |

Three further constructions are described in the technical notes and are **not** implemented,
each for a stated reason. **Dynamic surrender**: the account cannot fall from the index, so the
usual driver is absent, and the driver that *is* present — a run of zero *Indexjahre* — has no
published calibration. **A pro-rata credit on a mid-year exit**: unestablished at clause level
[R2], and a real cash-flow difference rather than a rounding. **The MindZV feedback loop**: the
model consumes a declared rate and does not derive one, so the *Garantieniveau* sensitivity it
reports is only the maturity-floor effect [R8] [R12].

## Sign convention

`net_cf` is **income positive** — premiums in, benefits and expenses out — which is the
notes' own orientation and the library-wide sign. `liability_cf` publishes the same stream
outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of `result_cf()`
so the identity is verifiable in the frame rather than only in prose. A Solvency II best
estimate is `Σ v(t) × liability_cf(t)` over the relevant risk-free term structure, plus a
risk margin [REG-R1] [REG-R2] [REG-R4]; nothing in this library discounts.

The shape to expect is the one a *Zillmer*-financed savings contract has and no other: a first
year that is almost the whole story of the strain — 1 620,00 € of acquisition expense against
2 400,00 € of premium, so `net_cf(1) = 606,31 €` — then twenty-five thin positive years while
the account builds, then one very large negative year when the whole surviving cohort's capital
falls due at once. `guar_int`, `surplus_credit`, `index_credit` and `av` are published beside
the statement because a reader cannot follow this product without them, and are **not** summed
into `net_cf`; `av` is a balance and its column is deliberately not totalled, twenty-seven
opening balances added together not being a quantity.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` first and `savings/CashValue_SE` second
wherever those models have an analogue: `pols_*` for policy counts, `av_pp` and
`av_pp_at(t, timing)` for the account value and its within-year reads, `prem_to_av_pp` for
the premium credited to one, plural nouns for cash flows, `*_rate` for rates, `*_pp` for
per-policy amounts, and `claims(t, kind)` with an uppercase `kind` string whose
`result_cf()` column is `claims_<lowercase kind>`. The technical notes use compact actuarial
symbols; the full mapping lives in the `Projection` Space docstring. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `P_b(t)`, `P(t)`, `BS` | `prem_base_pp` / `prem_gross_pp` / `prem_sum` | Three different amounts. The *Ratenzahlungszuschlag* multiplies what is **collected** and does not enter the *Beitragssumme*, so it may not inflate the acquisition charge or the *Mindesttodesfallschutz* floor: on model point 4 the premium collected is 2 520,00 € a year while `prem_sum()` is 76 800,00 € |
| `G(t)` | `index_base_pp` | The participating capital is the **opening** balance, before the year's premium — a separate cells rather than an inline `av_pp(t)`, because it is the quantity the whole payoff is struck on and the [std] reading that a different source would rescale |
| `B(t)`, `U(t)`, `X(t)` | `opt_budget_pp` / `surplus_credit_pp` / `index_credit_pp` | One budget, two destinations, one payoff. Named separately so `check_surplus_alloc()` can be written on the parts |
| `S(t)`, `Y(t)`, `rho(t)` | `index_sum` / `index_return_year` / `index_credit_rate` | The capped **sum**, the compounded **raw** year return and the rate actually credited are three different numbers, and confusing any two of them is a numbered pitfall |
| `K(t)`, `Γ(t)` | `credit_cum_pp` / `guar_cap_pp` | The ledger of credits and the guaranteed capital. `av_pp` is neither, and the lock-in check is written on `guar_cap_pp` |
| `w_l(t)` | `lapse_rate` / `lapse_rate_base` | The table rate and the rate applied are different in the final policy year, where a surrender and a maturity would be the same event at the same instant — and here, unlike on a term product, they pay different amounts |

**The chassis this model shares.** Inside delib, `RV_DE_A` (*klassische aufgeschobene
Rentenversicherung*) is the same accumulation chassis with the surplus credited as interest,
and `KLV_DE_A` is the *Überschussbeteiligung* chassis both inherit; model point 11 is the
`RV_DE_A` comparison run inside this model. `FRV_DE_S` is the contrast rather than the
sibling — it is genuinely unit-linked, and treating this product as that one is pitfall 1.
Across the repository the nearest relatives are `uslib`'s `FIA_US_S` and `RILA_US_S`, which
share the cap/participation-rate vocabulary and the annual reset but not the German
financing identity: an FIA's index budget is the insurer's option budget on a fixed-annuity
chassis, while here it is the **declared *Überschuss*** and is bounded by the MindZV [R8].

## Standardizations used

Every quantity below was introduced as a **[std]** — a standardization for the reference
implementation, chosen when no German carrier document could be reached. Carrier documents can
now be reached, and the Rationale column records for each row what the retrieved evidence does
to it: **two rows are no longer standardizations at all** (the base `G` of the participation
and the mid-year exit treatment, both of which turn out to be the rule in the two retrieved
AVB), **three are confirmed at their shipped value** (the acquisition charge, the
*Garantieniveau* and the *Rentenfaktor*), and **three are now known to sit off the evidence**
(the declared surplus rate, low; the equity *Partizipationsquote*, low; the house-index
*Partizipationsquote*, high). **No value in this table has been changed** — every one is a
shipped input backing a worked example and a golden test, and moving one is a decision to take
deliberately, not a side effect of a provenance pass. The list is complete.

| Standardization | Value | Rationale |
|---|---|---|
| Monthly Cap | 3,00 % on `eqidx_vol17`, 6,00 % on `houseidx_vol5` | Midpoint of an argued 1,5–5,0 % market band, and now beside one carrier figure: Allianz's own worked illustration runs at **3,2 %** [S2] [S5]. **No market panel of cap levels was found** [R21]. The house-index cap is higher because a low-volatility underlying is cheap to buy options on |
| *Partizipationsquote* | 60 % equity, 100 % house index | Midpoints of argued 50–80 % and 80–120 % bands. The retrieved figures sit differently: Allianz illustrates **75,00 %** on the EURO STOXX 50 [S2], and Stuttgarter **publishes 70 %** on its house multi-asset index for 1.2.2026–31.1.2027 [S8] — so the shipped equity rate is low and the shipped house rate is high against the one published house figure |
| Declared surplus rate `b` | 2,50 % a year, level | **Below the 2026 evidence**, which now reports the index segment separately: Assekurata gives *Indexpolicen* an average declared 3,07 % against 2,62 % for classic private annuities [R20], and Stuttgarter publishes 2,16 % for its own safe arm [S8]. Reported, not changed — see *What a retrieved document would change* below. Held level and exogenous, the model's largest single simplification |
| Guaranteed rate `i_g` | 1,00 % (0,90 % and 0,25 % on the in-force points) | The *Höchstrechnungszins* for 2025–2026 and two earlier cohorts [R7] [R18] |
| *Garantieniveau* | 90 % of *Beitragssumme* (60 %, 80 %, 100 % on other points) | **90 % is the modal retrieved level**: Allianz IndexSelect 90 % and IndexSelect Plus 80 % [S4], R+V 90 % [S7] § 1 Ziffer 2, Stuttgarter *BasisRente index-safe* 85 % [S11]. 100 % is statutory only for *Riester* [R12]; 60 % is unretrieved recollection |
| Index paths | three, constructed and reproducible from their seeds | Still constructed. **Two documented *Indexjahre* were located** — Allianz's published 2020/2021 and 2021/2022 tables at Cap 3,2 % [S2] — and they confirm the mechanic the two wired-in example rows assert, but they are not shipped: the golden tests are anchored on the research file's Examples A and B |
| Base `G` of the participation | the whole *Deckungskapital* at the year start | **No longer a standardization — it is the rule in both retrieved AVB.** "Bezugsgröße für die →Indexpartizipation ist der →Policenwert zu Beginn des →Indexjahres" [S2] Ziffer 3.3 Absatz 2 e), and [S7] § 3 Ziffer 2 likewise, both excluding that year's premiums. The sub-account and *Überschussguthaben* readings are withdrawn |
| *Indexjahr* alignment | aligned with the policy year | R+V's rule exactly ([S7] § 3 Ziffer 3), and a simplification against the other two: Allianz contemplates an *Indexjahr* that does not start with a *Versicherungsjahr* [S2] Ziffer 3.5, and Stuttgarter runs a common 1.2.–31.1. window for all contracts [S8]. An annual-grid model has no other defensible alignment |
| Mid-year exit treatment | no credit in the year of exit | **No longer a standardization.** Both retrieved AVB credit the participation only at the start of the following *Indexjahr* and refund no unspent budget; on surrender Allianz adds a pro-rata *Schlussüberschussanteil* and *Sockelbetrag* only [S2] Ziffer 3.3 and 9.2, [S7] § 3 Ziffer 5 [R2] |
| Election path | `w = 1` in the base run | A modelling choice so the model demonstrates the index arm, not a claim about behaviour |
| Mortality | Gompertz proxy anchored at `qx(M, 40) = 0.001200` | DAV 2008 T and DAV 2004 R are proprietary and are never shipped [REG-R48] [REG-R49] |
| Surrender | 5 / 5 / 3 … 6 (year 12) / 2 %, zero in the final year | No index-specific rate exists; the year-12 step is the EStG threshold [R14], and the terminal zero is a convention that moves real money here |
| Decrement order | death, then surrender on the survivors of death | Sequential rather than competing rates; declared rather than assumed |
| *Abschlusskosten* | 2,5 % of `BS`, zillmerised over 5 years | At the DeckRV § 4 Abs. 1 ceiling ("25 Promille der Summe aller Prämien") [R7] — **and equal to both retrieved carrier disclosures**: Allianz's *Einstiegskosten* of "2,5% der kumulierten Anlagen" [S4] and Stuttgarter's *Abschluss- und Vertriebskosten* of 2,50 % of premiums [S11] |
| *Verwaltungskosten* | `β = 3 %` of premium, `γ = 0,25 %` of the account a year | Inherited from delib products 1 and 2, and **below both retrieved comparators**: Allianz charges 3,5 % of the annual payment plus 1,0 % of value a year plus 0,1 % transaction costs, and a second entry charge of 1,5 % of the payment from year 6 [S4]; Stuttgarter 9,00 % of premiums plus 0,04 % of capital monthly [S11]. Total disclosed cost is 1,6 % a year and 1,80 points respectively |
| Acquisition expense | 2,5 % of `BS` at inception | Set equal to the charge, so the *Zillmer* strain is visible in `net_cf` rather than assumed away |
| Maintenance expense | 36,00 € a year inflating at 1,5 % | *Stückkosten*, inflated from **issue** so an in-force point carries its accumulated inflation |
| *Stornoabzug* | 2 % of the floored base | Deliberately mild inside an observed 0–20 % band [R2] |
| *Ratenzahlungszuschlag* | 1,000 / 1,020 / 1,030 / 1,050 | Market convention; no carrier tariff established |
| *Mindesttodesfallschutz* | 50 % of `BS` | The EStG condition applies to contracts concluded after 31 March 2009 (§ 52 Abs. 28 Satz 8) — **but § 20 Abs. 1 Nr. 6 Satz 6 Buchst. a states it for a *Kapitallebensversicherungsvertrag***, so reading its 50 % across to a *Rentenversicherung mit Kapitalwahlrecht* is an inference, not the statute [R14]. R+V's own floor is 90 % of premiums [S7] § 1 Ziffer 5 |
| *Rentenfaktor* | 25,00 € per 10 000 € per month, guaranteed = current | Inherited from delib product 2, and **within 3 % of a published index-tariff figure**: Stuttgarter discloses a guaranteed 25,74 € per 10.000 € on a 30-year age-37-to-67 case [S11]. Still **not** mutually calibrated with the mortality proxy, which is why the annuity is reported and not computed. R+V prices its guaranteed factor at a *Rechnungszins* of 0,1 % p. a. on a company table derived from DAV 2004 R [S7] § 1 Ziffer 3 |
| The thirteen model points | — | Pure construction: no *Produktinformationsblatt* was located, so no commercial envelope was established at all [S3] [S11] |

The only things in this model that are **not** standardizations are the structural rules —
the payoff formula and its three separable features, the annual floor and the lock-in, the
one-budget allocation, the guarantee falling due at *Rentenbeginn*, the § 169 Abs. 3
five-year spread under the surrender value, the *Stornoabzug*'s quantification requirement,
and the election being a right of the policyholder exercisable each year without the
insurer's consent — to which the retrieved AVB add the base of the participation and the
mid-year exit treatment.

### What a retrieved document would change, and has not

Three findings from the retrieved carrier documents bear on **modelled** facts. They are
recorded and **not acted on**, because each would move the worked example and the golden tests
with it.

1. **The declared surplus rate is low.** `surplus_rate = 2,50 %` against an Assekurata 2026
   index-segment average of **3,07 %** [R20]. Because the rate *is* the option budget, every
   index credit in the model scales with it.
2. **The option budget is defined more widely in both AVB than in the model.** It is the
   declared surplus **plus** the year's minimum share of the *Bewertungsreserven*, and at
   Allianz net of *Verwaltungskosten* ([S2] Ziffer 3.3 Absatz 1, [S7] § 3 Ziffer 9).
   `check_surplus_alloc()` asserts `opt_budget_pp(t) + surplus_credit_pp(t) = surplus_rate(t) ·
   index_base_pp(t)`, which is the model's own identity and stays true; it is the *mapping* to
   the contractual budget that is incomplete.
3. **The Cap form cannot express the Allianz tariff.** Allianz applies a monthly Cap **and** a
   *Partizipationssatz* to the capped sum — `X = q · max(S, 0) · G` [S2] Ziffer 3.3 Absatz 2 —
   while `payoff_form = "cap"` has no `q` (its `w` is the election share) and
   `payoff_form = "quote"` has no cap. A `cap` arm with a participation factor would be a small
   change to `index_credit_rate` and a large change to every printed row.

None of these is a defect in the arithmetic the tests assert; each is a statement about what
the shipped parameters and the shipped payoff form represent.

## Tests

`tests/test_indexpolice_de.py` asserts every one of the twenty-seven rows of the notes' worked
example to the cent and `pols_if` to six decimals, the totals at full precision (three of which
differ by a cent from the sum of the rounded cells), the notes' six independent checks — year 1
rebuilt end to end, the *Indexjahr* of year 9 rebuilt on its own terms, the decrement closure,
the account roll-forward at `t = 9`, the cash flow statement on the Total row, and the guarantee
at *Rentenbeginn* — the *Partizipationsquote* variant's printed rows and totals, the four
designs at *Rentenbeginn*, the product's own invariants and each `check_*()` identity with its
residual, and **one test per listed modeling pitfall**, named for the pitfall. The
whole-model-point sweep belongs to the conventions suite and is not repeated here.

```bash
python -m pytest lifelib/libraries/delib/tests/test_indexpolice_de.py -q
python -m pytest lifelib/libraries/delib/tests/test_model_conventions_de.py -q -k Index_DE_A
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-indexpolice-r1
[R12]: #delib-indexpolice-r12
[R14]: #delib-indexpolice-r14
[R15]: #delib-indexpolice-r15
[R18]: #delib-indexpolice-r18
[R19]: #delib-indexpolice-r19
[R2]: #delib-indexpolice-r2
[R20]: #delib-indexpolice-r20
[R21]: #delib-indexpolice-r21
[R22]: #delib-indexpolice-r22
[R4]: #delib-indexpolice-r4
[R7]: #delib-indexpolice-r7
[R8]: #delib-indexpolice-r8
[REG-R1]: #delib-reg-r1
[REG-R2]: #delib-reg-r2
[REG-R4]: #delib-reg-r4
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[std]: #delib-std
<!-- END generated citation links -->
