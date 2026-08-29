# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`technical-notes.md`](technical-notes.md); the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The *mechanics* are
> the established German ones and each carries the instrument it must be checked against — the
> benefit trigger being the statutory *Pflegegrad* of §§ 14, 15 SGB XI rather than a definition the
> insurer writes [R2] [R6], the five-grade *Leistungsstaffel* scaling one *vereinbarte Pflegerente*
> [S4], *Beitragsbefreiung im Leistungsfall* as a contractual term [S4], the level *Beitrag* that a
> *Lebensversicherer* may adjust only on the narrow § 163 VVG route and never under § 203 VVG
> [R11] [REG-R27], the 1,00 % *Höchstrechnungszins* and the 25 ‰ *Höchstzillmersatz* of the DeckRV
> [R13] [REG-R14] [REG-R16], the § 169 VVG *Rückkaufswert* with its five-year cost spread and its
> *Stornoabzug* conditions [R11] [REG-R28], and the unisex pricing rule [REG-R34].
> **Every level is a standardization.** No *Bedingungswerk*, no *Produktinformationsblatt*, no
> *Basisinformationsblatt*, no *Verbraucherinformation*, no *Tarifblatt* and no premium quotation
> for any German *Pflegerentenversicherung* was retrieved for this library, and the session's
> search budget was exhausted before this product was researched; **DAV 2008 P**, the German
> market's standard multi-state *Pflegetafel*, is the property of the Deutsche Aktuarvereinigung,
> is not public and is **not redistributed here** [R15] [REG-R51], and neither is DAV 2008 T or
> DAV 2004 R [R16] [REG-R48] [REG-R49]. So **every biometric rate, every charge, every lapse rate
> and the premium itself is [std]**, and the premium is an output of a stated first-order basis
> rather than a table lookup. Replace the decrement, expense and surrender tables with company data
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/pflegerentenversicherung/run.py
python products/pflegerentenversicherung/run.py 5      # the statutory bahr Leistungsstaffel
python products/pflegerentenversicherung/run.py 7      # a Wartezeit and a Karenzzeit
python products/pflegerentenversicherung/run.py 12     # an in-force policy already in claim
```

```python
import modelx as mx
mx.read_model("products/pflegerentenversicherung/Pflege_DE_S").Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell. `result_cf()`
returns a tidy `DataFrame` indexed by **policy month** `t` carrying `pols_if` first, the three-way
split of it a reader follows the projection with, and one column per cash flow line;
`result_states()` publishes the five *Pflegegrad* ledgers, the *Karenz* ledger, the flows between
them and the four annual rates beside it. `model.Projection.doc` holds the full symbol mapping and
`model.Data.doc` says what a replacement for each shipped table must preserve.

The grid is **monthly** and `t` is **0-based**: `t = 0` is the month of issue and
`age(t) = age_at_entry + t // 12`, so the attained age steps at the policy anniversary. The frame
**starts** at `duration_mth_init()` — `0` for new business, the elapsed duration for an in-force
point — and `proj_len()` is the **last** projected index, `12 × (110 − 45) − 1 = 779` on the anchor
cell: 780 rows, attained ages 45 to 109, in about seven seconds. It depends on the entry age and
the terminal age alone, so an in-force point publishes a **shorter** frame ending at the same
index; reading it as a row count, or as a horizon `duration_mth_init` shifts, is a listed pitfall.

## Nine states, and only two of them absorbing

This is what a reader arriving from `RLV_DE_A`, `BasicTerm_S` or any single-decrement protection
model will get wrong, and it is the reason the product is worth modelling at all. A *Pflegerente*
is a **multi-state contract whose benefit is a step function of the state**, not a cover that pays
on an event:

```
   aktiv ──►  PG1  ⇄  PG2  ⇄  PG3  ⇄  PG4  ⇄  PG5
     │  ▲      │        │        │        │       │
     │  └──────┘  Reaktivierung / Herabstufung     │
     ▼           ▼        ▼        ▼        ▼      ▼
   storno                    tot   (absorbing)
```

The model carries the *Pflegegrad* **explicitly**, in `pols_pg(t, g)` for `g = 1 … 5`, with a
second ledger `pols_karenz(t, g, z)` for lives inside a deferred period and a third, `pols_act(t)`,
for active lives. Every transition inside that picture is **internal to `pols_if`**: lives leave
the in-force population only by death or by surrender, which `check_pols_roll_fwd()` asserts and
`check_states()` asserts a second, independent way. Two consequences drive the implementation.

**The paying state has three exits and only death is absorbing.** A life in *Pflegegrad* `g` can
die, deteriorate to `g + 1` or be downgraded to `g − 1`; out of grade 1 the downgrade is a
*Reaktivierung* back to the active state, where the life resumes paying its *Beitrag* and becomes
exposed to lapse again. A model that lets the paying state be exited only by death **overstates**
the liability; one that treats every downgrade as a termination **understates** it, and both errors
produce a plausible-looking frame. On the anchor cell the *Reaktivierung* flow is 0,013768 of a
policy over the whole projection and the *Herabstufung* flow out of grade 2 — the flow that ends an
annuity and revives a premium on the `delib_std` grid — is 0,020835: both small, both non-zero,
which is why the tests assert the **flow** and never a non-monotone stock.

**The transitions are allocated, not added.** Every shipped rate is annual; every month is stepped
with **forces held constant over the month**, the competing transitions sharing one survival
probability in proportion to their forces — `p_stay = exp(−Σμ/12)` and
`p_j = (μ_j / Σμ) × (1 − p_stay)` — so `p_stay + Σ p_j = 1` **exactly, by construction**. That is
what makes `check_states()` an identity rather than an approximation, and why `p_pg_stay`,
`p_pg_death`, `p_pg_worse` and `p_pg_better` are published as four cells rather than folded into
the recursion. Adding monthly rates instead, or applying `q/12`, gives different answers wherever
the forces are large — which on this product is exactly where the money is.

## Grade and mortality are correlated, and the highest-paying state is the shortest-lived

In-care mortality is **not tabulated**. `mort_force_care(t, g)` is `mort_mult(g)` times the
**force** of active mortality at the same age — 1,5 at *Pflegegrad* 1 rising to 9,0 at grade 5 —
and `mort_rate_care(t, g)` is `1 − exp(−mort_force_care(t, g))`. The multiple is on the force and
not on the rate, and that is load-bearing rather than cosmetic: on forces the ratio is exactly
`mort_mult(g)` at every age below the limiting one, while on rates it compresses towards 1 as the
rate saturates — at grade 5 the *rate* ratio falls from 8,972 at age 45 to 6,854 at 85, 4,308 at 95
and exactly 1,000 at the limiting age. That compression is the scale, not the basis, and a model
stating its LTC mortality loading as a rate multiple has a different basis at every age.

What it buys is the product's central fact: **the annuity in payment is short**, three to five
years rather than the fifteen to twenty a healthy-life annuity would run at the same age, so
pricing it on an annuity table — DAV 2004 R is built to be prudent about people living *longer*
[R16] [REG-R49] — would be prudent in exactly the wrong direction. And because grade and mortality
are correlated, `claims(t, "ANNUITY")` is a **grade-by-grade sum**, `R × Σ_g π_g × esc_pg(t, g)`,
and never an average benefit percentage on an average survival curve. Applying the entry-mix mean
percentage of 0.3815 to `Σ_t pols_care(t) = 24.241784` gives 9 248,24 € against the model's
13 200,11 €, a **30 % understatement of the whole benefit** that no total in the frame would
reveal. The substitution is *exact* at `t = 1`, where the stock still is the entry mix; the error
opens as deterioration moves the stock to a stock-weighted mean of 0.544519.

## The *Wartezeit* and the *Karenzzeit* are different devices

They are routinely conflated in consumer material and they are implemented in two different places.

The ***Wartezeit*** runs from **inception** and denies cover: `inc_force(t)` is exactly zero while
`t < wartezeit_months()`, and `inc_rate(t)` is left alone so it stays the tariff-comparable table
rate at every age. A gate on the force, one line, no ledger.

The ***Karenzzeit*** runs from **onset** and defers an admitted claim, so it is a clock **per
onset** rather than a gate on the aggregate — which is why it needs its own ledger dimension,
`pols_karenz(t, g, z)` with `1 ≤ z ≤ K`. Lives in it are subject to the **same** transitions as a
served life: they die, deteriorate and recover exactly as if the annuity were running, they simply
are not paid, and the clock is **discarded on reactivation**, because a recovered life who relapses
starts a new onset. Where `karenz_months() == 0` the ledger is empty and `pols_grad` degenerates to
`pols_entry`, which is the base run. The cost of the device is the gap between the two: over model
point 7's projection graduations are 0.228177 against entries of 0.253723, **89,9 %**, the
shortfall being deaths and recoveries recorded *inside* the six-month deferral — larger than six
months of a four-year spell suggests, because mortality is highest immediately after onset. The
model uses an aggregate in-care mortality with no select period after onset, so **it understates
how much a *Karenzzeit* removes**, and point 7's reduction is a floor rather than an estimate.

## The waiver runs with the *Leistungsstaffel*, not with the diagnosis

`pols_waived(t)` is the *Beitragsbefreiung* population and it is **not** everyone in care. It is
`Σ_{g : waiver_flag(g)} pols_pg(t, g)`, restricted to the premium term, and `waiver_flag(g)` is
`benefit_pct(g) > 0`. Three consequences fall straight out of the benefit schedule, and each is a
distinct way to get the premium stream wrong:

- a life inside its *Karenzzeit* is **not** waived, because no annuity is yet payable;
- a *Pflegegrad* 1 life is **not** waived on `delib_std`, where `π_1 = 0`, and **is** waived on
  `bahr`, where it is 10 % — the same life, two schedules, opposite answers;
- a life downgraded out of the insured grades **leaves** the waived population and starts paying
  again, so `pols_prem` is structurally non-monotone.

Wiring the waiver to membership of the care ledger instead gets all three wrong at once and still
closes every count. `check_waiver()` asserts the split — `pols_prem + pols_waived = pols_in_term` —
and is arithmetically trivial while `pols_prem` is a difference; it is published because the
failure it guards is not a slip in the subtraction but a disagreement about who belongs on which
side, and it is read together with the tests that assert the membership itself. The waiver is also
**in the price**, through `tar_pols_prem(t)`: on a contract issued at 45 and claiming at 82 it
removes the remaining premium stream for the whole paying period, of the order of four years of
*Beitrag*, and that cost sits inside the level premium.

## Two ledgers for one population: `pols_pg` and `esc_pg`

`esc_pg(t, g)` is the **escalation-weighted** counterpart of `pols_pg(t, g)`: the identical
recursion with one extra factor of `(1 + d)^(1/12)` on the surviving weights, entrants joining at
weight 1. Carrying the *Leistungsdynamik* as a **value ledger** rather than as a
duration-since-onset cohort dimension keeps the model `O(n)` instead of `O(n²)`; the price is that
it reports only the aggregate escalation, which is all the cash flow needs. The annuity is weighted
on `esc_pg` and **never** on `pols_pg` — using the head count would silently drop the escalation on
every model point that carries one, and no total in the frame would look wrong. With
`leistungsdynamik = 0` the two ledgers are identical at every `t` and `g`, which
`check_esc_ledger()` asserts as an exact equality on the base run and as a domination
(`esc_pg ≥ pols_pg`) wherever the dynamic is positive.

The dynamic costs more than a four-year spell suggests. On model point 8, `d = 2 %` raises the
projected annuity total from 13 200,11 € to 15 101,44 € — **+14,4 %** — and the equivalence premium
from 64,198409 € to 72,038378 €, **+12,2 %**. `ln(1.144) / ln(1.02) = 6,8` years of
payment-weighted elapsed duration against a mean spell in an insured grade of 5,45 years, because
the escalation compounds over elapsed time in **care** — *Pflegegrad* 1 months included, where
nothing is paid — and because deterioration puts the largest benefit percentages at the end of a
spell, where the escalation factor is largest.

## The *Beitrag* is a priced quantity, and the pricing engine is a separate ledger

The library publishes **undiscounted** cash flows. The *Beitrag* is nevertheless a *priced*
quantity, so the model carries a second, self-contained actuarial-value engine — the `tar_*` cells
— whose only output is `premium_mth_pp()`. **That engine discounts; the projection does not**, and
`rechnungszins()` and `disc_factor(t)` are read by nothing else. Where `premium_mth` is positive on
the model point that is the premium and the engine is never consulted, which is how model points
10, 11 and 12 carry the premium they were actually sold at. Where it is `0.0` — a sentinel, not a
free contract — `P` is struck by equivalence on the
**first-order** (*erster Ordnung*) bases: every rate multiplied by its prudence margin, the sexes
blended at `unisex_mix_male = 0.50` because sex may not enter a German premium [REG-R34], and **no
lapse at all**. The absence of lapse is both German first-order practice and what keeps the model
acyclic. Everything on the benefit side that scales with `P` is linear in it, so

```
P·U = A + P·D1 + P·a1 + β·P·U + G + C   →   P = (A + G + C) / [U(1 − β) − D1 − a1]
    = (17,789.761930 + 892.884210 + 69.389246) / (313.500018 x 0.970 − 12.000000)
    = 18,752.035386 / 292.095018 = 64.198409 EUR a month
```

`prem_net_level_pp() = A / U = 56.745649`, so the whole expense loading is **13,13 %**, of which
the *Zillmerung* allowance `a1 = 0.025 × 12 × (85 − 45) = 12.000000` units of `P` alone is 2,53 € a
month: strike `a1` out of the denominator and the premium falls to 61,665 €. `U` is **26,13 years'**
worth of discounted premium.

`check_prem_equiv()` closes the same equivalence **from the tariff ledgers month by month** rather
than from the closed form, which is what makes it a real identity: substituting a best-estimate
rate into one leg, dropping the *Zillmerung* term, forgetting the waiver in `tar_pols_prem` or
valuing the annuity on `tar_pols_pg` instead of `tar_esc_pg` all make the sum miss zero. Individual
months are large and of both signs, so only the **sum** is the identity; on the anchor cell it is
−9,3e−12 against a premium leg of 20 125 €. Where the model point supplies its own *Beitrag* no
equivalence was struck and the residual is zero by construction. The *Risikozuschlag* multiplies
the **gross** premium and never the benefit, so `claims` is invariant to it: model point 13 prices
at 283,130286 € against an unrated 188,753524 €, exactly 1,50 ×, on an identical claim stream.

**There is no published German rate card for this product to reproduce** — the single largest
difference between this model and frlib's `TD_FR_A`, which reproduces a real attained-age grid. The
premium here is computed, and the notes sanity-check its level against an argued 50,00–100,00 €
band rather than against a citation.

## The *Zillmerung* is charged on the *Beitragssumme*, not on the annual premium

`acq_expense_pp()` is `acq_permille / 1000 × beitragssumme()`, with the per-mille set **exactly at**
the § 4 DeckRV *Höchstzillmersatz* of 25 ‰ so that the ceiling binds visibly [REG-R16] [REG-R20].
A lifelong-premium contract has no finite *Beitragssumme* without a convention, and
`beitragssumme_cap_age = 85` **[std]** is that convention:
`P × 12 × (min(prem_end_age, 85) − age_at_entry)`, and the *Einmalbeitrag* itself where there is
one. On the anchor cell that is 30 815,24 € and a charge of 770,38 €, all of it at `t = 0`.
Charging the per-mille on an *annual* premium instead understates it by a factor of the paying term
— here forty-fold — and is a listed pitfall. Because the charge falls at `t = 0` only, an
**in-force model point never incurs it**: its frame opens at `duration_mth_init() > 0` and the cost
was incurred before the valuation date, which is worth knowing before comparing an in-force point's
first row with a new-business point's.

## Inputs are external files

The nine input CSVs live **in this directory**, beside `run.py`, and `Pflege_DE_S/` holds nothing
but formulas — `__init__.py`, `_system.json`, `Data/__init__.py` and `Projection/__init__.py`, no
`_data/`, no IOSpec, no embedded values. This follows lifelib's `annuallife/TradLife_A`, which
keeps its inputs beside the model; it is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs inside the model through modelx's IOSpec machinery.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace with
its own cells cache; readers placed there would re-read every file for every policy. They live
instead in an unparameterized **`Data`** Space that `Projection` reaches through a `data`
Reference, so each file is read once per model however many policies are projected, and a test
counts the reads against a registered file set. `Data.input_dir()` resolves the location from
`_model.path.parent` when the model is read, so it works from any checkout. **The trade-off:** the
model is not portable on its own — copy `Pflege_DE_S/` without the CSVs and it reads fine, then
fails on first evaluation. What you gain is that a diff of the model shows logic changes only, and
an input can be swapped in place: point `Data.mort_table_file` at another same-schema file and the
projection follows, with no formula change.

| Reference | Cells | File | Contents and provenance |
|---|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` | Fourteen model points. **Point 1 is the worked-example anchor cell** (F / entry 45 / aktiv / 1 000 € a month at PG5 / `delib_std` / lifelong monthly *Beitrag* derived by equivalence / every option off). Points 2–14 exercise the unisex twin, quarterly, half-yearly, annual and single instalments, the `bahr` grid, an *abgekürzte Beitragszahlungsdauer*, a *Wartezeit* with a *Karenzzeit*, a *Leistungsdynamik*, a *Beitragsrückgewähr*, a supplied premium with a *Stornoabzug*, two in-force points — one of them already in claim — and both ends of the entry-age band. **The one file with no `provenance` column**: a model point is a configuration, not an assumption, and it is the only exemption from delib's second ruling |
| `benefit_scale_file` | `benefit_scale_table()` | `benefit_scale_table.csv` | The *Leistungsstaffel* by schedule and *Pflegegrad*. `delib_std` is 0 / 30 / 50 / 75 / 100 % **[std]**, the flatter, higher shape a *Pflegerente* aimed at the residential funding gap tends to use; `bahr` is the statutory 10 / 20 / 30 / 40 / 100 % minimum grid of § 127 SGB XI [R8], the only *Leistungsstaffel* fixed by German statute, carried for comparison because a *Pflegerente* cannot be a *geförderter Tarif* |
| `mort_table_file` | `mort_table()` | `mort_table.csv` | Annual **active-life** mortality by sex, ages 18–109. **[std]** Gompertz proxy `1 − exp(−B c^age)`; **not** DAV 2008 T and **not** the DAV 2008 P active-life table [R15] [R16]. **The anchors a replacement must preserve are `q(65) = 1.35 %` and `q(85) = 10.5 %` male, `q(65) = 0.75 %` and `q(85) = 7.0 %` female**, with `mort_rate = 1.0` at age 109 |
| `incidence_file` | `incidence_table()` | `incidence_table.csv` | Annual incidence into **any** *Pflegegrad* by sex and age. **[std]** `min(I0 exp(g(age − 65)), 0.50)` with `I0_F = 0.0110`, `g_F = 0.1400`, `I0_M = 0.0085`, `g_M = 0.1380`. The slope is anchored on the one shape the research states with confidence — prevalence roughly doubling every five years of age above 75, `ln 2 / 5 = 0.1386` [R18] `[unverified]` |
| `care_file` | `care_table()` | `care_table.csv` | The whole in-care basis in five rows: `entry_share` 0.20 / 0.38 / 0.24 / 0.13 / 0.05, `det_rate` 0.28 / 0.24 / 0.20 / 0.16 / 0.00, `rec_rate` 0.10 / 0.06 / 0.04 / 0.02 / 0.01 and `mort_mult` 1.5 / 2.5 / 3.5 / 6.0 / 9.0 on the **force**. All **[std]**. `entry_share` is deliberately **not** the stock distribution of about 9 / 44 / 27 / 14 / 6 % [R18]: entrants skew lower than the stock because deterioration moves people up over a spell |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` | Annual lapse from the **active** state by policy year 1–40, year 40's rate applying thereafter: 6,0 / 5,0 / 4,0 / 3,5 / 3,0 % then 2,5 / 2,0 / 1,5 %. **[std]**, and **no lapse rate for a German *Pflegerente* at any duration was established**; the shape is argued from the *Zillmerung*, and the 14-day *Widerruf* sits inside year 1 [REG-R23] |
| `surrender_file` | `surrender_table()` | `surrender_table.csv` | The guaranteed *Rückkaufswert* as a fraction of premiums paid to date, by completed policy year 1–40. **[std]** shape encoding two cited facts and no cited level — the 25 ‰ *Zillmerung* allowance, which is why years 1 and 2 are zero [REG-R16], and the § 169 Abs. 3 VVG five-year cost spread, which is why it turns positive in year 3 [REG-R28] |
| `expense_file` | `expense_table()` | `expense_table.csv` | `acq_permille` 25,000 ‰ of *Beitragssumme*, `admin_prem_pct` 3,0 %, `admin_mth_pp` 2,00 € a month, `claim_expense_pp` 1,50 € per annuity payment, `expense_infl` 1,5 % a year. All levels **[std]**; only the 25 ‰ ceiling the first sits exactly at is cited |
| `basis_file` | `basis_table()` | `basis_table.csv` | `rechnungszins` 1,00 %, `omega_age` 110, `unisex_mix_male` 0.50, `rec_age_ref` 75, `rec_age_decay` 0.10, `inc_cap` 0.50, `beitragssumme_cap_age` 85, `roll_fwd_tol` 1e−10 and the five first-order margins `inc_margin` 1.25, `det_margin` 1.15, `rec_margin` 0.80, `care_mort_margin` 0.85, `act_mort_margin` 0.90. **Only the *Rechnungszins* is cited** [REG-R14] [REG-R15]; everything else is **[std]** |

Every file but the model point table carries a **`provenance` column**, one tag per row — delib's
second ruling, and it is machine-checked.

**What a replacement biometric basis must preserve**, in four properties, whether it is DAV 2008 P
under licence or a company table: **(a)** incidence by attained age, sex **and grade of entry**,
because a stroke or a fracture enters directly at grade 3 or 4; **(b)** deterioration dominating
recovery above age 75; **(c)** mortality in care as a grade-increasing multiple of active mortality;
and **(d)** transition probabilities out of each state summing, with the stay probability, to one.

## The published identities

Six `check_*()` cells, each a no-argument `bool` over all `t` with a per-`t` residual
`check_*_resid(t)`, all six scaled by `roll_fwd_tol` from `basis_table.csv`.

**`check_net_cf` — delib ruling 1, in one line:**
`net_cf(t) = premiums(t) − claims(t,"ANNUITY") − claims(t,"LAPSE") − claims(t,"DEATH") − expenses(t) − claim_expenses(t)`.

Every term of that is a **column of `result_cf()`**, and the residual re-derives the headline number
from the three `claims` **kinds** separately rather than from their subtotal, so a benefit that
stops being included in `claims(t)`, or a column added to the frame without being subtracted, fails
here instead of silently changing the answer. The largest residual in the anchor frame is 1,4e−14.

| Check | Identity |
|---|---|
| `check_pols_roll_fwd` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t)`: lives leave the in-force population **only** by death or surrender, and every *Pflegegrad* transition is internal to it |
| `check_states` | `pols_act(t) + Σ_{g,z} pols_karenz(t,g,z) + Σ_g pols_pg(t,g) + pols_dead_cum(t) + pols_lapse_cum(t) = pols_if_init()`: the three live ledgers and the two absorbing counts partition the initial cohort at every `t` |
| `check_waiver` | `pols_prem(t) + pols_waived(t) = pols_in_term(t)`: the *Beitragsbefreiung* splits the in-term population and neither loses nor creates a policy |
| `check_esc_ledger` | `esc_pg(t,g) ≥ pols_pg(t,g)` for every `t, g`, with **exact equality** when `leistungsdynamik = 0` |
| `check_prem_equiv` | `Σ_t check_prem_equiv_resid(t) ≈ 0`: the gross premium closes the first-order equivalence, re-assembled from the tariff ledgers rather than from the closed form |

`check_pols_roll_fwd` and `check_states` are not the same statement made twice. The first is a
telescope over the three ledgers' own recursions; the second is assembled by **direct summation**
with no reference to the recursion that produced any of them, so it catches a wrong seeding of an
in-force point, a life counted in two grades at once, an entrant into care who never leaves the
active ledger and a *Karenz* cohort that graduates twice. Because `mort_rate` is forced to 1,0 at
the limiting age it also closes at the far end: `pols_dead_cum(780) = 0.493968` and
`pols_lapse_cum(780) = 0.506032` sum to 1,000000000000 with `pols_if(780) = 1,5e−23`.

## Modules that are off in the base run

Five constructions are implemented and switched off **through the model point**, so the base run
reproduces the worked example while the machinery stays visible and testable.

| Module | Switch | Off value | On at | What it does |
|---|---|---|---|---|
| *Wartezeit* | `wartezeit_months` | `0` | point 7 (36) | Zeroes `inc_force(t)` while `t < wartezeit_months()`, so care beginning inside it is not covered at all. Near-universal in the subsidised *Pflege-Bahr* product, near-absent in the underwritten one, because the *Gesundheitsprüfung* does the same screening [R8] |
| *Karenzzeit* | `karenz_months` | `0` | point 7 (6) | Populates `pols_karenz(t, g, z)`. With `K = 0` the ledger is empty and `pols_grad` degenerates to `pols_entry` |
| *Leistungsdynamik* | `leistungsdynamik` | `0.00` | point 8 (0.02) | Escalates the annuity **in payment** at `(1 + d)^(1/12)` a month through `esc_pg`. Not a *Beitragsdynamik*, which is not modelled at all |
| *Beitragsrückgewähr* | `beitragsrueckgewaehr` | `False` | point 9 (`True`) | Makes `claims(t,"DEATH") = cum_prem_max_pp(t) × pols_death(t)`, structurally zero otherwise, and adds the `D1` leg to the equivalence |
| *Stornoabzug* | `stornoabzug` | `0.00` | point 10 (0.05) | Reduces the *Rückkaufswert* by a contractual fraction. Zero in the base run because a deduction is admissible only if agreed, appropriate and **quantified in the contract** [R11] [REG-R28], and no level for any German *Pflegerenten* tariff was established |

Model point 9 is the option worth reading twice. The *Beitragsrückgewähr* is not a modest loading:
at a *Rechnungszins* of 1,00 % a gross return of nominal premiums on a death forty years away is
close to the whole premium, and written with a lifelong *Beitragszahlungsdauer* the equivalence's
denominator collapses to 3,6 of 313,5 units. The point therefore pays to age 65, which is how the
German market writes such a tariff, and its premium is **622,92 € a month — 9,7 times the
anchor's**. The implemented form is the **gross** one, with no offset for annuity already paid:
the market's more common form nets the annuity off, but that netting is floored at zero *per life*
and these ledgers are aggregates, so netting in aggregate would let a life that received a large
annuity subsidise one that received none. The option therefore overstates the death benefit
relative to the market-standard form, and that is stated rather than hidden.

Four constructions the notes describe are **not** implemented, each for a stated reason. No
***Überschussbeteiligung*** in any application form — the surplus chassis belongs to
`products/kapitallebensversicherung/`, and a *Beitragsverrechnung* here would need a declared-rate
assumption this corpus supplies nothing for [R11] [REG-R24]. No ***Beitragsdynamik***, whose
acceptance rate on each offer is a behavioural assumption with nothing behind it. No
***Beitragsfreistellung*** [R11] [REG-R28], so every voluntary exit is a surrender and the
direction of that bias is stated. And no **§ 163 VVG re-rating** [REG-R27], which is a management
action conditional on emerging experience rather than a projected assumption.

## Sign convention

`net_cf` is **income positive** — *Beitrag* in, *Pflegerente*, *Rückkaufswert*, any
*Beitragsrückgewähr* and both expense lines out — the notes' own orientation and the library-wide
sign. `liability_cf` publishes the same stream outgo-positive, `liability_cf(t) = −net_cf(t)`
exactly, and both are columns of `result_cf()` so the identity is verifiable in the frame rather
than only in prose. A Solvency II best estimate is `Σ v(t) × liability_cf(t)` over the relevant
risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R4]; **nothing in this library
discounts**, and `rechnungszins` appears only inside the equivalence.

The shape to expect on the anchor cell is the product's whole economic story in three phases. Month
0 is **−710,11 €**, almost all of it the 25 ‰ *Zillmerung* allowance charged in one go —
`expenses(0) = 770,380907 + 2,000000 + 1,925952 = 774,306859 €` against a 64,20 € instalment. From
`t = 1` the contract runs positive, the level *Beitrag* far above the risk premium, and the monthly
margin decays from 59,93 € to 3,45 € by age 65. **`net_cf` crosses zero between `t = 251` and
`t = 252`, attained age 66**, and the last three decades are run-off: annuity outgo peaks at
49,82 € in month 407 (age 78) and the population in care at 0.092120 in month 417 (age 79).
Undiscounted the contract collects 15 857,95 € and pays 17 385,60 € of benefit and expense, for
**−1 527,65 €** — not a loss but the consequence of publishing an *undiscounted* stream whose income
falls thirty years before its outgo. That crossing is where the *Deckungskapital* this model does
not compute peaks, and it is the whole economic content of an ageing reserve on a life chassis.

`expenses` is acquisition and administration only. The *Leistungsbearbeitungskosten* are
`claim_expenses`, a separate column because they scale with **annuity payments made** rather than
with policies: a *Pflegegrad* 1 life on `delib_std` generates none, and neither does a life inside
its *Karenzzeit*. Its level is set low, and that is a product fact rather than optimism — the
*Pflegegrad* is determined by the *Medizinischer Dienst* or by MEDICPROOF and not by the insurer
[R6], so the *Nachprüfung* is a documentation exercise rather than the adversarial re-assessment
that drives a *Berufsunfähigkeitsrente*'s claims cost [REG-R29].

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those models
have an analogue: `pols_*` for policy counts, plural nouns for cash flows, `*_rate` for **annual**
rates with `*_rate_mth` for their monthly equivalents, `*_pp` for per-policy amounts,
`claims(t, kind)` with an uppercase `kind` string, `pols_if_at(t, timing)` for the end-of-month
read, and `check_*()` / `check_*_resid(t)` for the identities. The technical notes use compact
actuarial symbols; the full mapping lives in the `Projection` Space docstring. The **monthly
multi-state biometric chassis** is shared with frlib's `Dep_FR_S` (*assurance dépendance*) and,
inside this library, with `BU_DE_S` — three models that are not interchangeable, and whose
differences are worth naming rather than glossing:

| This model | `Dep_FR_S` | `BU_DE_S` | Note |
|---|---|---|---|
| `pols_pg(t, g)`, `g = 1 … 5` | `pols_part` / `pols_tot` | `pols_dis_dur(t, z)` | The **ledger dimension** differs: a *Pflegegrad* here, a two-level French severity there, a claim-duration cohort in BU. Only this model's is a benefit *schedule* |
| `wartezeit_months` | `carence_months(cause)` | — | Both run from **inception**; the French one forks by cause of onset |
| `karenz_months` | `franchise_months` | `karenz_months` | All three run from **onset** and defer an admitted claim |
| `leistungsdynamik` | in-claim revalorisation | `leistungsdyn_rate` | The escalation of the annuity in payment |
| `pols_prem` | `pols_prem` | `pols_prem` | In force less waived: the difference **is** the *Beitragsbefreiung* |
| `mort_force_care(t, g)` | `mort_rate_partial` / `mort_rate_total` | `mort_rate_dis(t, z)` | Impaired-life mortality by state; only this model states it as a multiple of the active **force** |
| `check_net_cf`, `check_pols_roll_fwd`, `check_states` | same names | same names | The three identities mean the same thing on all three models |

Five names needed care:

| Notes | Cells | Why |
|---|---|---|
| `l_g(t)` vs `E_g(t)` | `pols_pg` / `esc_pg` | The **same population** counted two ways: a head count and an escalation-weighted value. The annuity is weighted on the second and never on the first |
| `l(t)` vs the waived split | `pols_if` / `pols_in_term` / `pols_waived` / `pols_prem` | In force, in force inside the premium term, waived, and paying. `pols_care` is a fifth thing again and is **none** of them: it includes the *Karenz* ledger and a grade-1 life on `delib_std` |
| `q_A(x)` vs `q_g(x)` | `mort_rate` / `mort_rate_care(t, g)` | The active-life table rate and the in-care rate derived from its force. Publishing one rate for both states is the error the pair exists to prevent |
| `i(x)` vs `ι(t)` | `inc_rate` / `inc_force` | The table rate, which stays tariff-comparable at every age, and the force the *Wartezeit* gates to zero |
| `pols_entry` vs `pols_grad` | `pols_entry(t, g)` / `pols_grad(t, g)` | Onsets and graduations out of the *Karenz* ledger. Equal when `K = 0`; their gap **is** the cost of a *Karenzzeit* |

`policy_id`, `duration_mth(t)` and `pols_if_init()` drive little or nothing in the base
parameterization and are exposed as documented cells rather than dropped: a silently missing
column is worse than an inert one.

## Standardizations used

Everything in this table is **[std]**. The product is unusually **[std]**-heavy, which is the
correct outcome rather than a defect: the *mechanics* are well established and cited in the
blockquote above, and it is only the *levels* that no retrievable document supplies.

| Standardization | Value | Rationale |
|---|---|---|
| *Leistungsstaffel* `delib_std` | 0 / 30 / 50 / 75 / 100 % | Inside the observed 0–10 / 10–30 / 30–50 / 60–75 / 100 % market range `[unverified]`. Grade 1 pays nothing because grade 1 is not a funding event in the statutory scheme either [R3] [R4]; the middle steps are set mid-to-upper range because grades 2 and 3 carry most of the time in care |
| *Vereinbarte Pflegerente* | 1 000,00 € a month | The round number at the lower end of the 1 000–1 500 € the market sells, sized against the residual a *Pflegeheim* resident funds after the statutory contribution and an average pension [R4] [R20] `[unverified]` |
| Active-life mortality | Gompertz `1 − exp(−B c^age)`, anchored `q_M(65) = 1.35 %`, `q_M(85) = 10.5 %`, `q_F(65) = 0.75 %`, `q_F(85) = 7.0 %` | DAV 2008 T and the DAV 2008 P active-life table are DAV property and are not shipped [R15] [R16]. The **anchors** are what a replacement must preserve, not the functional form |
| Incidence | `min(I0 exp(g(age − 65)), 0.50)`, `g_F = 0.1400`, `g_M = 0.1380` | DAV 2008 P is not shipped [R15]. The slope is anchored on the one shape the research states with confidence — prevalence doubling every five years above 75, `ln 2 / 5 = 0.1386` [R18] — and the level on the sex-specific lifetime-risk order of magnitude |
| `entry_share` | 0.20 / 0.38 / 0.24 / 0.13 / 0.05 | Entrants skew **lower** than the 9 / 44 / 27 / 14 / 6 % stock [R18], because deterioration moves people up over a spell. Using the stock as the entry mix is a listed pitfall, and the model's own stock share at grades 4 and 5 (21,0 % and 17,6 %) exceeding the entry share is the arithmetic statement of it |
| `det_rate` / `rec_rate` | 0.28 / 0.24 / 0.20 / 0.16 / 0.00 and 0.10 / 0.06 / 0.04 / 0.02 / 0.01 a year | Deterioration dominating recovery is property (b) a replacement must preserve. Levels are construction; there is **no age-at-onset dimension**, which a real *Pflegetafel* has |
| Recovery damping | `exp(−0.10 × max(0, age − 75))` | Encodes the one thing about *Reaktivierung* not in doubt: real after acute events at younger ages, small at the ages where most claims arise [R6] |
| `mort_mult` | 1.5 / 2.5 / 3.5 / 6.0 / 9.0 on the **force** | Carries the research file's order of magnitude — two to three times an active life at grade 2, five to ten at grade 5 `[unverified]`. On the force, so the multiple means the same at every age; on rates it would compress to 1 at the oldest ages |
| Terminal age | `omega_age = 110`, with `mort_rate = 1.0` forced at 109 and the force capped at `−ln(1e−12)` | A modelling choice, not a table fact — the DAV tables run higher. It buys a **closed** system: `check_states()` closes exactly instead of leaving a truncation residue |
| Monthly step | constant forces over the month, exits allocated in proportion to them | One convention applied uniformly to mortality, incidence, deterioration, recovery and lapse. `p_stay + Σ p_j = 1` exactly |
| Processing order | classify → collect *Beitrag* → pay *Rente* → start-of-month expenses → transitions → advance the *Karenz* clock → **lapse last**, on the survivors of the insured decrements **and** the reactivation inflow | Both orderings close `check_pols_roll_fwd()`, which is exactly why the order has to be **declared**. Applying lapse to the opening cohort instead moves `pols_lapse(0)` by 6,2e−7 of a policy and materially more once the decrements are large |
| Lapse table | 6,0 % falling to 1,5 % by year 21, **active state only**, zero after the premium term | **No lapse rate for a German *Pflegerente* at any duration was established.** The shape is argued from the *Zillmerung*; nothing in care lapses, because a claimant with a waived premium has no premium to default on and a live annuity to forfeit |
| *Rückkaufswert* table | 0 / 0 / 0.05 / 0.12 / 0.20 of premiums paid, rising to 0.70 by year 40 | The **shape** encodes the 25 ‰ *Zillmerung* allowance [REG-R16] and the § 169 Abs. 3 five-year spread [REG-R28]; **no level was established**. Whether a *pure-risk* *Pflegerente* falls inside § 169 at all is an open question the library states rather than assumes away |
| `beitragssumme_cap_age` | 85 | A lifelong-premium contract has no finite *Beitragssumme* without a convention. The **ceiling** the per-mille sits at is cited [REG-R16]; the base it is struck on is not |
| Expense levels | 25 ‰ once, 3,0 % of premium, 2,00 € a month inflating at 1,5 %, 1,50 € per annuity payment | **No charge level of any kind was established for any German *Pflegerenten* tariff.** The acquisition rate sits *exactly at* the § 4 DeckRV ceiling so the ceiling binds visibly; the rest are placeholders, and the instalment loading is folded into `admin_prem_pct` rather than shipped as a *Ratenzahlungszuschlag* no source supports |
| First-order margins | incidence × 1.25, deterioration × 1.15, recovery × 0.80, in-care mortality × 0.85, active mortality × 0.90, **no lapse** | Only the **direction** is cited [REG-R8] [REG-R47]; no German *Sicherheitszuschlag* level for a *Pflegetafel* was established. Prudence forks by risk: more claims, faster progression, fewer recoveries, longer annuities, and *more* active lives surviving to claim |
| `unisex_mix_male` | 0.50 | Sex may not enter a premium concluded from 21 December 2012 [REG-R34]. Pricing a 50 / 50 mix while writing 60 / 40 is a named model risk — the mismatch **is** the cross-subsidy, and the mix is endogenous to the price |
| `rechnungszins` | **1,00 % a year** | The *Höchstrechnungszins* for new business from 1 January 2025, which attaches to the cohort at issue [REG-R14] [REG-R15] `[unverified as to the date]`. Used only in the equivalence — **the one genuinely cited pricing assumption in the model** |
| No *Ratenzahlungszuschlag* | — | The consequence runs the wrong way and is stated rather than hidden: annual mode prices very slightly **below** monthly here, through the discounting alone, which is the opposite sign to a real German tariff |
| Age basis | age last birthday advancing at the **policy anniversary** | The model carries no dates; a date-based implementation carries a fractional offset of at most one year |
| Timing | *Beitrag* and *Pflegerente* both **in advance**; surrender and death benefits at the end of the month | German *Renten* are *monatlich vorschüssig*, and paying in advance puts the annuity on the same weight as the premium it replaces, which is what lets `check_waiver()` reconcile the two streams against one ledger |
| The fourteen model points | — | Configuration rather than observation: no rate card, no commercial envelope and no carrier wording was obtained for this product |

The only quantities in the model that are **not** standardizations are the structural rules and the
two cited numbers: the *Pflegegrad* trigger and its five-grade scale [R2] [REG-R51], the
*Beitragsbefreiung* running with the annuity [S4], the level *Beitrag* adjustable only under § 163
VVG [R11] [REG-R27], the unisex rule [REG-R34], the `bahr` grid's own 10 / 20 / 30 / 40 / 100 %
[R8], the § 169 VVG surrender frame [R11] [REG-R28], the 25 ‰ *Höchstzillmersatz* the acquisition
charge sits at [REG-R16], and the 1,00 % *Höchstrechnungszins* [REG-R14] [REG-R15].

## Tests

`tests/test_pflegerentenversicherung_de.py` asserts the fourteen printed rows of the notes' worked
example to the cent and the policy counts to six decimals, the full-precision totals against the
sum-of-rounded-cells the notes also print, the equivalence premium of 64,198409 € reached two
independent ways from `A`, `U`, `G` and `C`, month 0 rebuilt term by term with a calculator, the
first month's decrements from the annual rates through the forces, the first annuity payment grade
by grade, the closure identity, the male twin's ten printed rows and totals, the four-cell variant
table, the six `check_*` identities with their residuals, and **one test per numbered modeling
pitfall** — seventeen of them. The whole-model-point-table sweep is **not** here:
`tests/test_model_conventions_de.py` owns the library's single sweep, because a model point's first
evaluation is the most expensive thing in the run.

```bash
python -m pytest lifelib/libraries/delib/tests/test_pflegerentenversicherung_de.py -q
python -m pytest lifelib/libraries/delib/tests/test_model_conventions_de.py -q -k Pflege_DE_S
```
