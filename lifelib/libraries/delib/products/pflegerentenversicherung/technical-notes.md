# Technical Notes

**Status:** Draft, 2026-08-29 (research access date 2026-08-29).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Pflege_DE_S`**, **monthly** grid — for the standardized composite German
*Pflegerentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's product, and **no product document of any kind was retrieved for it**: direct HTTP egress
from the build environment is blocked and the session's `WebSearch` budget was exhausted before work
on this product began. [S#] / [R#] tags refer to the source list in `sources.md` (numbering carried
from `_research/pflegerentenversicherung.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own R-numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified] marks
claims no source could corroborate. On this product **every biometric rate, every charge, every
lapse rate and the premium itself is [std]** — a fact stated here once and repeated at each
assumption table rather than left to be inferred. Parameter values are identical to those in
`product-spec.md`. Cells names, model-point columns and CSV headers are English `lower_snake_case`;
German terms of art keep their German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — *Beiträge*,
  *Pflegerente* payments, surrender payments, any *Todesfallleistung*, and expenses — for a
  single-policy model point, on an expected (probability-weighted) basis. The model publishes what
  a valuation layer consumes; it does **not** discount the projected stream, does not compute a
  *Deckungsrückstellung*, does not compute a *Zinszusatzreserve* and does not compute capital. Those
  layers are referenced under *Valuation and reserve pointers*, never reproduced.
- **The one place a discount rate appears.** The *Beitrag* is a **priced** quantity, struck by
  equivalence at the *Rechnungszins* on the first-order (*erster Ordnung*) bases [REG-R8] [REG-R47],
  so the model carries a second, self-contained actuarial-value engine — the `tar_*` cells — whose
  only output is `premium_mth_pp()`. **That engine discounts; the projection does not.**
- **Projection frequency.** **Monthly grid.** The *Pflegerente* is a monthly annuity, the *Beitrag* a
  monthly instalment, and the *Pflegegrad* can change in any month, so the monthly grid is the
  contract's own rather than a refinement of an annual one. The `_S` suffix follows lifelib.
- **What `t` counts, and the frame.** `t` is the **policy month index, 0-based**: `t = 0` is the
  month of issue, and `t` counts complete months elapsed since issue. `age(t) = age_at_entry + t //
  12`, so the attained age steps at the policy anniversary. The frame **starts** at
  `t = duration_mth_init()`, which is `0` for new business and the elapsed duration for an in-force
  model point, and **ends** at `proj_len()`. Where the frame starts is a product fact and is not
  asserted by the conventions suite; contiguity is.
- **`proj_len()` is the last projected period index**, not a row count — frlib's ruling, which delib
  adopts and asserts. Here

      proj_len() = 12 * (omega_age() - age_at_entry()) - 1

  which depends only on the entry age and the terminal age, **not** on `duration_mth_init()`. The
  anchor cell (entry age 45, `omega_age = 110`) therefore runs to `t = 779`, 780 monthly rows,
  attained ages 45 to 109.
- **Terminal age.** `omega_age = 110` **[std]**, with `mort_rate(t) = 1.0` forced in the final year
  of age so the model is a closed system rather than a truncated one and the decrement closure holds
  exactly. It is a modelling choice, not a table fact — the DAV tables run higher [R15] [REG-R51] —
  and it costs nothing material: an active life aged 45 survives to 110 with probability of the
  order of 1e-4 on the shipped basis.
- **Timing conventions [std].** Within month `t`: the *Beitrag* is collected **at the start** of the
  month, in advance, from the lives then in the premium-paying states; the *Pflegerente* is paid
  **at the start** of the month, in advance, to the lives then in a paying *Pflegegrad*; per-policy
  and premium-related expenses are charged at the start of the month; transitions act **over** the
  month; and death and surrender benefits fall **at the end** of the month. `pols_if(t)` is the
  count at the **start** of month `t` and is the weight on that same `result_cf()` row's cash flows,
  as the house style requires; end-of-period state is reached through `pols_if_at(t, "END")`.
- **Why the annuity is in advance.** German *Renten* are conventionally *monatlich vorschüssig*, and
  paying in advance puts the annuity on the same weight as the premium it replaces, which is what
  lets `check_waiver()` reconcile the two streams against one ledger.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  annuity, surrender, death benefit and expenses −), with the outgo-positive orientation published
  as `liability_cf(t) = -net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents and `pols_if` to six decimals **[std]**.
- **Out of scope, deliberately, and each said in one line.** No *Überschussbeteiligung* in any of
  its three application forms — the surplus chassis belongs to
  `products/kapitallebensversicherung/`. No *Beitragsdynamik*: the acceptance rate on each offer is
  a behavioural assumption this corpus cannot support. No *Beitragsfreistellung* and no § 38 VVG
  premium-default conversion: every voluntary exit is a surrender, and the direction of the
  resulting bias is stated in the product specification. No taxation of premium or benefit — the
  benefit's treatment is an open question [R23] [REG-R41]. No select mortality after onset of care:
  the shipped in-care mortality is an aggregate, and the consequence is pitfall 10 and model risk 9.
  No *Pflege-Bahr* *Zulage*, which is statutorily unavailable to this product [R8]. No three-month
  *Nachprüfung* notice tail: whether § 174 VVG reaches a *Pflegerente* through § 177 was not
  established [REG-R29] [unverified], and the model does not assume it does.

---

## Model point attributes

`model_point_table.csv` is indexed by `point_id` and is the **only** input file without a
`provenance` column, because a model point is a configuration rather than an assumption (delib
ruling 2). "Exercised by" names the model points that make the attribute do work.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Index; `Projection` is parameterized by it | all |
| `policy_id` | str | Human-readable identifier, `PFL-0000NN` | all |
| `sex` | enum {M, F} | The **projection** basis. Pricing is unisex [REG-R34], so this must not reach `premium_mth_pp()` | 1 (F) vs 2 (M), identical otherwise |
| `age_at_entry` | int | Age last birthday at issue; drives `proj_len()` and every rate lookup | 14 (18, the youngest permitted), 13 (65, the oldest) |
| `duration_mth_init` | int | Complete months elapsed at the projection start; `0` for new business. The frame opens at this `t` | 11 (240), 12 (336) |
| `status` | enum {aktiv, pg1…pg5} | State at the projection start | 12 (`pg3`, in claim) |
| `rente_mth` | float | The *vereinbarte Pflegerente* at *Pflegegrad* 5, EUR per month — the scaling constant of the whole benefit | 13 (1 500), 14 (500) |
| `staffel_id` | str | Key into `benefit_scale_table.csv`: `delib_std` or `bahr` | 5 (`bahr`) |
| `prem_end_age` | int | Attained age at which the *Beitrag* ceases; `110` (= `omega_age`) means lifelong | 4 (65, *abgekürzte Beitragszahlungsdauer*) |
| `prem_mode` | enum {monthly, quarterly, half_yearly, annual, single} | Instalment frequency; `single` is the *Einmalbeitrag* | 1, 3, 4, 5, 6 |
| `premium_mth` | float | The contractual monthly *Beitrag*. **`0.0` means "derive by equivalence"** | 10 (75.00 supplied), 11 and 12 (in-force premiums) |
| `rating_factor` | float | *Risikozuschlag* multiplier on the gross premium; `1.00` at standard rates | 13 (1.50) |
| `wartezeit_months` | int | *Wartezeit* from inception, in months | 7 (36) |
| `karenz_months` | int | *Karenzzeit* from onset, in months | 7 (6) |
| `leistungsdynamik` | float | Annual escalation of the annuity in payment; `0.0` = off | 8 (0.02) |
| `beitragsrueckgewaehr` | bool | *Beitragsrückgewähr* death benefit on/off | 9 (True) |
| `stornoabzug` | float | Deduction from the *Rückkaufswert*, as a fraction; `0.0` = off | 10 (0.05) |
| `pols_if_init` | float | Policy count at the frame's first `t`; `1.0` everywhere here | all |

**The three attributes most easily got wrong**, each a numbered pitfall: `sex` is a *projection*
input and must not touch the price [REG-R34]; `premium_mth = 0.0` is a sentinel, not a free
contract; and `duration_mth_init` shifts where the frame **starts** without changing `proj_len()`,
which is a property of the contract and not of the valuation date.

### The fourteen model points

| # | Configuration | What it exercises |
|---|---|---|
| 1 | **Anchor.** F, entry 45, aktiv, 1 000 €/mth, `delib_std`, lifelong, monthly, premium derived | The worked example |
| 2 | M, entry 45, otherwise identical to 1 | Unisex pricing against a sex-specific projection: same `premium_mth_pp()`, different claims |
| 3 | F, entry 55, quarterly, lifelong, `delib_std` | The upper half of the purchase cluster; quarterly instalments |
| 4 | M, entry 40, premiums to age 65, half-yearly | *Abgekürzte Beitragszahlungsdauer*; half-yearly instalments; the paid-up tail |
| 5 | F, entry 50, annual mode, `staffel_id = bahr` | The statutory 10/20/30/40/100 grid, where *Pflegegrad* 1 **is** insured and waived |
| 6 | F, entry 60, `prem_mode = single` | The *Einmalbeitrag*: one payment at `t = 0`, no premium-paying ledger thereafter |
| 7 | M, entry 50, `wartezeit_months = 36`, `karenz_months = 6`, monthly | Both waiting devices, and the *Karenz* ledger |
| 8 | F, entry 45, `leistungsdynamik = 0.02`, monthly | The escalation ledger; `esc_pg` diverges from `pols_pg` |
| 9 | M, entry 45, `beitragsrueckgewaehr = True`, monthly | The death-benefit stream, `claims_death` non-zero |
| 10 | F, entry 48, `premium_mth = 75.00`, `stornoabzug = 0.05` | A supplied premium instead of a derived one; a non-zero *Stornoabzug* |
| 11 | M, entry 42, `duration_mth_init = 240`, aktiv, monthly | An in-force point opening at `t = 240` with 20 years run |
| 12 | F, entry 55, `duration_mth_init = 336`, `status = pg3` | An in-force point **in claim**: waived premium and a paying state at the frame's first row |
| 13 | **Boundary.** M, entry 65 (top of the observed band), 1 500 €/mth, `rating_factor = 1.50` | Shortest pre-claim period, highest premium, a *Risikozuschlag* |
| 14 | **Boundary.** F, entry 18 (bottom of the band), 500 €/mth, monthly | Longest projection (`proj_len() = 1103`), smallest benefit, expense-dominated |

Between them the fourteen exercise both premium forms, all four instalment frequencies, both
*Leistungsstaffeln*, every switchable option, two in-force points — one active, one in claim — and
both ends of the entry-age band.

---

## Input files

Every file is a plain UTF-8 CSV in the model folder's **parent**, read once per model by a reader
cells in the `Data` Space (the `annuallife/TradLife_A` layout). Every file **except**
`model_point_table.csv` carries a final `provenance` column, one tag per row — delib ruling 2.

| File | Index columns | Value columns | Content |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the eighteen attributes above | The fourteen model points. **Exempt** from `provenance` |
| `benefit_scale_table.csv` | `staffel_id`, `pflegegrad` | `benefit_pct`, `provenance` | The *Leistungsstaffel*: 0/30/50/75/100 % for `delib_std`, 10/20/30/40/100 % for `bahr` [R8] |
| `mort_table.csv` | `sex`, `age` | `mort_rate`, `provenance` | Annual **active-life** mortality, ages 18–109, both sexes |
| `incidence_table.csv` | `sex`, `age` | `inc_rate`, `provenance` | Annual rate of entering **any** *Pflegegrad* from the active state, ages 18–109, both sexes |
| `care_table.csv` | `pflegegrad` | `entry_share`, `det_rate`, `rec_rate`, `mort_mult`, `provenance` | The whole in-care basis in five rows: the distribution of the grade first entered, the annual deterioration rate to the next grade, the annual recovery rate to the previous grade or to active, and the force-of-mortality multiple over an active life of the same age |
| `lapse_table.csv` | `policy_year` | `lapse_rate`, `provenance` | Annual lapse from the **active** state, policy years 1–40; year 40's rate applies to every later year |
| `surrender_table.csv` | `policy_year` | `rkw_prem_ratio`, `provenance` | The guaranteed *Rückkaufswert* as a fraction of premiums paid to date, policy years 1–40, clamped as for lapse |
| `expense_table.csv` | `item` | `value`, `unit`, `provenance` | `acq_permille`, `admin_prem_pct`, `admin_mth_pp`, `claim_expense_pp`, `expense_infl` |
| `basis_table.csv` | `param` | `value`, `provenance` | `rechnungszins`, `omega_age`, `unisex_mix_male`, `rec_age_ref`, `rec_age_decay`, `inc_cap`, `beitragssumme_cap_age`, `roll_fwd_tol`, and the five first-order prudence margins `inc_margin`, `det_margin`, `rec_margin`, `care_mort_margin`, `act_mort_margin` |

Nine files, each read by a reader cells in `Data`; the conventions suite asserts there are no
orphans in either direction.

---

## State variables

The contract is a **multi-state** risk. The state space is the one § 15 SGB XI defines [R2]
[REG-R51], plus the two absorbing exits a life-assurance contract adds:

```
   aktiv ──►  PG1  ⇄  PG2  ⇄  PG3  ⇄  PG4  ⇄  PG5
     │  ▲      │        │        │        │        │
     │  └──────┘ Reaktivierung / Herabstufung      │
     │         │        │        │        │        │
     ▼         ▼        ▼        ▼        ▼        ▼
   storno                    tot  (absorbing)
```

Forward moves are deterioration, backward moves are *Herabstufung* and, out of PG1,
*Reaktivierung*; death is reachable from every state. **Lapse is reachable only from `aktiv`**
[std]: a claimant whose premium is waived has nothing to lapse from and everything to lose. Pitfall
12 tests it.

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | Last projected month index, `12 * (omega_age - age_at_entry) - 1` | once per model point |
| `duration_mth(t)` | Complete months since issue at `t`; equal to `t` by construction, and published so the frame's own origin is explicit | monthly |
| `policy_year(t)` | `t // 12 + 1`, the *Versicherungsjahr* the month falls in | monthly |
| `age(t)` | Attained age, `age_at_entry + t // 12` | monthly |
| `pols_act(t)` | Lives in the active state at the start of month `t` | monthly recursion |
| `pols_karenz(t, g, z)` | Lives in *Pflegegrad* `g` at the start of month `t` whose *Karenzzeit* clock stands at `z`, `1 ≤ z ≤ karenz_months`. Empty when `karenz_months = 0` | monthly recursion |
| `pols_pg(t, g)` | Lives in *Pflegegrad* `g` at the start of month `t` whose *Karenzzeit* has been served — the ledger the annuity is paid on | monthly recursion |
| `esc_pg(t, g)` | The **escalation-weighted** counterpart of `pols_pg(t, g)`: the sum over those lives of `(1 + leistungsdynamik)^(months since the annuity began / 12)`. Equal to `pols_pg` exactly when the dynamic is off | monthly recursion |
| `pols_care(t)` | `Σ_z Σ_g pols_karenz + Σ_g pols_pg` — everyone in care, waiting or paid | monthly |
| `pols_if(t)` | `pols_act(t) + pols_care(t)` — the in-force count at the **start** of month `t` | monthly |
| `pols_if_at(t, timing)` | `"BEG"` = `pols_if(t)`; `"END"` = `pols_if(t + 1)`. End-of-period state goes through here and never through `pols_if` | monthly |
| `pols_in_term(t)` | In-force units still inside the premium-paying period (`age(t) < prem_end_age`) | monthly |
| `pols_waived(t)` | In-term units in a *Pflegegrad* whose `benefit_pct` is positive — the *Beitragsbefreiung* population | monthly |
| `pols_prem(t)` | `pols_in_term(t) - pols_waived(t)` — the units that actually pay | monthly |
| `pols_entry(t, g)` | Lives entering *Pflegegrad* `g` from the active state during month `t` | monthly |
| `pols_grad(t, g)` | Lives graduating out of the *Karenz* ledger into `pols_pg(·, g)` during month `t` | monthly |
| `pols_death(t)` | Deaths during month `t`, from every state | monthly |
| `pols_lapse(t)` | Lapses during month `t`, from the active state only, after the insured decrements | monthly |
| `pols_dead_cum(t)`, `pols_lapse_cum(t)` | Cumulative absorbing counts at the start of month `t` | monthly |
| `cum_prem_max_pp(t)` | Premiums payable to date on an uninterrupted path, per policy — the base of the *Rückkaufswert* and of the *Beitragsrückgewähr* | monthly |
| `tar_pols_act(t)`, `tar_pols_pg(t, g)`, `tar_pols_prem(t)` | The same ledgers on the **first-order** basis, without lapse — the pricing engine's own state | monthly |

There is **no account value** and **no paid-up state**, and the *Deckungskapital* — a real object of
this contract — is deliberately **not** a state variable: the library publishes undiscounted cash
flows and leaves the reserve to the layer that consumes them, with the guaranteed *Rückkaufswert*
entering as data (product spec, footnote 21).

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Benefit | A monthly *Pflegerente*, paid in advance, equal to `benefit_pct(g) × rente_mth` for the insured's current *Pflegegrad* `g` | [S4] |
| *Leistungsstaffel* `delib_std` | 0 / 30 / 50 / 75 / 100 % across grades 1 to 5 | **[std]**, product spec footnote 12 |
| *Leistungsstaffel* `bahr` | 10 / 20 / 30 / 40 / 100 % — the statutory *Pflege-Bahr* minimum grid, the only *Leistungsstaffel* fixed by German statute | [R8] [unverified] |
| Trigger | The statutory *Pflegegrad* of §§ 14, 15 SGB XI, determined by the *Medizinischer Dienst* or MEDICPROOF, not by the insurer | [R2] [R6]; [REG-R51] |
| Care setting | Irrelevant to the benefit; the same annuity is payable at home and in a *Pflegeheim* | **[std]**, product spec footnote 1 |
| *Beitragsbefreiung* | **Full**, from the first month in which any annuity is payable; revived on exit from the paying grades | [S4]; detail **[std]** |
| Premium form | Level monthly *Beitrag*, guaranteed for the life of the contract, adjustable only on the § 163 VVG route | [R11]; [REG-R27] |
| Premium cessation | On death; on the start of an insured annuity; at `prem_end_age` | [S4] [unverified] |
| Equivalence principle | The gross premium is struck so that, on the first-order bases at the *Rechnungszins*, the expected present value of premiums equals that of benefits plus expenses | [REG-R8] [REG-R47] |
| *Rechnungszins* | **1,00 %** p.a. — the *Höchstrechnungszins* of § 2 DeckRV for new business from 1 January 2025, which stays with the contract for its whole term | [REG-R14] [REG-R15] |
| *Höchstzillmersatz* | **25 ‰ (2,5 %) of the *Beitragssumme***, § 4 DeckRV, cut from 40 ‰ by the LVRG from 1 January 2015 | [REG-R16] [REG-R20] |
| *Rückkaufswert* | The *Deckungskapital* on the premium bases, floored by the value that results from spreading acquisition and distribution costs evenly over the first **five** contract years | [REG-R28] |
| *Stornoabzug* | Admissible only if agreed, quantified and appropriate; a deduction for unamortised acquisition costs is expressly ineffective | [REG-R28] |
| Unisex | Sex may not enter the premium for contracts concluded from 21 December 2012 | [REG-R34] |
| *Wartezeit* / *Karenzzeit* | Contractual, both **0** in the base run; the *Pflege-Bahr* statutory maximum *Wartezeit* is five years | [R8] [unverified]; base **[std]** |

**What is *not* in this table.** There is **no cited premium**, no cited charge, no cited transition
rate and no cited *Rückkaufswert* level anywhere in this corpus, so this class is unusually thin
beside `frlib/products/temporaire_deces`, which could tabulate a published rate card. Everything
numeric that is missing here appears in class (c) as **[std]**, and that displacement is the single
most important thing to know about this model.

### (b) Insurer-discretionary current elements

Thinner than on any savings product in delib, and thin for a structural reason: **a *Pflegerente*
is a life contract, so the insurer's discretion over price is confined to § 163 VVG and to the
surplus rebate** [REG-R27]. There is no bonus rate, no crediting rate and no charge scale to
declare.

| Input | Snapshot value | Basis |
|---|---|---|
| *Überschussbeteiligung* in any application form | **None.** No *Beitragsverrechnung*, no *verzinsliche Ansammlung*, no *Bonus* uplift of the *vereinbarte Rente* | mechanic [R11] [R12] [REG-R24]; omission **[std]** (1) |
| The *Bruttobeitrag* / *Zahlbeitrag* spread | **Zero.** The model projects the *Bruttobeitrag* | [REG-R27] [REG-R53]; **[std]** (1) |
| § 163 VVG re-rating | **Never invoked** in the projection | [REG-R27]; **[std]** (2) |
| Tariff drift on new business | **Not modelled.** The premium is struck once, at issue, on the bases shipped | **[std]** (2) |
| *Nachprüfung* intensity | **Not modelled** as a separate decrement. Recovery and downgrade are biometric transitions, not claims-management outcomes | [R6] [S4]; **[std]** (3) |

1. The delib library publishes gross undiscounted cash flows and demonstrates the
   *Überschussbeteiligung* chassis in full in `products/kapitallebensversicherung/`. Modelling a
   discretionary *Beitragsverrechnung* here would need a declared-rate assumption for which this
   corpus supplies nothing at all (research gap 18), and it would make the projected premium a
   discretionary quantity — which is precisely what the product's commercial proposition says it is
   not. The *Zahlbeitrag* is nevertheless what a customer actually pays, so a reader comparing this
   model's premium with a market quotation is comparing a *Bruttobeitrag* with a *Zahlbeitrag* and
   should expect the model to sit **above** the quotation.
2. § 163 requires a non-temporary, unforeseeable change in a calculation basis, an appropriate and
   necessary new premium and a trustee's confirmation, and is excluded where the original
   calculation was insufficient [REG-R27]. It is a management action conditional on emerging
   experience, not a projected assumption, and a model that built one in would be asserting that
   the guarantee it is demonstrating does not hold.
3. On a *Berufsunfähigkeitsrente* the insurer runs its own *Nachprüfung* and the claims-management
   intensity is a real assumption [REG-R29]. Here the evidence is the statutory determination
   [R6], so re-verification is a documentation exercise and the model treats every exit from a
   paying grade as biometric. That is the sharpest modelling difference between `Pflege_DE_S` and
   `BU_DE_S`.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German source in this corpus publishes a
*Pflegewahrscheinlichkeit*, a deterioration or recovery rate, an in-care mortality multiple, an
expense loading, a commission scale, a lapse rate or a surrender-value table for this product
(research gaps 2, 3, 10, 15, 19, 20). The proxies below are shaped to reproduce the *mechanics* the
research file establishes; they are **not** calibrations, and none of them is a proxy for DAV 2008 P.

**Why they cannot be a proxy for DAV 2008 P.** That table is the market-standard first-order basis
for German LTC business on the life chassis [R15] [REG-R51]; it is DAV property, is not public and
**is not redistributed by this library**; and it was built on the pre-2017 *Pflegestufen*, which the
BGH will not map to the *Pflegegrade* [REG-R36] [REG-R51] — so a table calibrated on *Pflegegrad*
data is not a DAV 2008 P proxy even in principle. **A replacement table must preserve four
properties**: (a) incidence by attained age, sex and *grade of entry*, because a stroke or a fracture
enters directly at grade 3 or 4; (b) deterioration dominating recovery above age 75; (c) mortality
in care as a grade-increasing multiple of active mortality; and (d) transition probabilities out of
each state summing, with the stay probability, to one.

**Active-life mortality [std].** A Gompertz proxy, sex-specific, German-population-shaped and
**not** DAV 2008 T or the DAV 2008 P active-life table [R16] [REG-R48] [REG-R52]:

    mort_rate(sex, x) = 1 - exp(-B_sex * c_sex ** x),     ages 18 to omega_age - 2
    mort_rate(sex, omega_age - 1) = 1.0                   the limiting-age convention

with `B_M = 1.47884e-05`, `c_M = 1.110680`, `B_F = 4.76290e-06`, `c_F = 1.119962`. The parameters
are fixed by two anchors per sex — `q(65) = 1.35 %` and `q(85) = 10.5 %` for males, `0.75 %` and
`7.0 %` for females **[std]** — and those anchors are what a substitute table must reproduce for the
worked example to close. The *Data* docstring states them.

**Incidence into care [std].** The rate at which an active life enters **any** *Pflegegrad*:

    inc_rate(sex, x) = min(I0_sex * exp(g_sex * (x - 65)), inc_cap)

with `I0_F = 0.0110`, `g_F = 0.1400`, `I0_M = 0.0085`, `g_M = 0.1380` and `inc_cap = 0.50`. The
slope is anchored to the one shape the research file states with confidence: **prevalence roughly
doubles every five years of age above 75** [R18] [unverified], which is a growth rate of
`ln 2 / 5 = 0.1386` a year. The level is anchored so that the model's own probability of reaching an
insured *Pflegegrad* before death, from the anchor cell's entry age, is of the order of the **45 %**
the research file argues, with a mean age at first insured grade in the low eighties
[unverified]. The female parameters are the higher pair, which is the sex differential the whole
unisex tension turns on. The cap is a shape device, not an observation: without it the exponential
exceeds one before age 100.

**The in-care basis [std]**, five rows of `care_table.csv`, and the single most consequential table
in the model:

| *Pflegegrad* | `entry_share` | `det_rate` (to `g+1`, annual) | `rec_rate` (to `g-1`/aktiv, annual) | `mort_mult` |
|---|---|---|---|---|
| 1 | 0.20 | 0.28 | 0.10 | 1.5 |
| 2 | 0.38 | 0.24 | 0.06 | 2.5 |
| 3 | 0.24 | 0.20 | 0.04 | 3.5 |
| 4 | 0.13 | 0.16 | 0.02 | 6.0 |
| 5 | 0.05 | 0.00 | 0.01 | 9.0 |

`entry_share` sums to 1.00 and is deliberately **not** the stock distribution: the stock is about
9 / 44 / 27 / 14 / 6 % [R18] [unverified], and entrants skew lower than the stock because
deterioration moves people up over a spell. Using the stock distribution as the entry mix is
pitfall 17. `mort_mult` is a multiple on the **force** of active mortality at the same age, and it
carries the research file's most load-bearing biometric statement: the mortality of a
*Pflegebedürftiger* is a large multiple of an active life's, **of the order of two to three times at
grade 2 and five to ten times at grade 5** [unverified]. `rec_rate` is further damped with age,

    rec_rate(g, x) = rec_rate_g * exp(-rec_age_decay * max(0, x - rec_age_ref))

with `rec_age_ref = 75` and `rec_age_decay = 0.10` **[std]**, which is what makes deterioration
dominate recovery above 75 — property (b) of a replacement table.

Three consequences follow, and all three are pitfalls. **The annuity in payment is short**, of the
order of three to five years, not the fifteen to twenty of a healthy-life pension at the same age —
so pricing it on an annuity table such as DAV 2004 R would be prudent in exactly the wrong direction
[R16] [REG-R49]. **Grade and mortality are correlated**, so the highest-paying state is also the
shortest-lived. And **a deferred period bites harder than its length suggests**, because a material
share of new claimants die inside it.

**Lapse [std].** From the **active** state only, and zero once the premium-paying period has ended:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–10 | 11–20 | 21–40 |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate` | 6.0 % | 5.0 % | 4.0 % | 3.5 % | 3.0 % | 2.5 % | 2.0 % | 1.5 % |

Year 40's rate applies to every later policy year. **No lapse rate for this product at any duration
was established** (gap 20). The shape is a modeller's construction: *Zillmerung* makes an early lapse
expensive to the policyholder, so the profile is lower and flatter than a savings product's, and a
paid-up contract has no premium-driven exit at all. The monthly rate is
`1 - (1 - lapse_rate(t)) ** (1/12)`, which the conventions suite checks is strictly below the annual
rate wherever that is positive.

**The guaranteed *Rückkaufswert* [std].** Expressed as a fraction of premiums paid to date, by
completed policy year — the scale-free form, and the form in which a German contract states the
values [REG-R28]:

| Policy year | 1 | 2 | 3 | 4 | 5 | 10 | 15 | 20 | 25 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rkw_prem_ratio` | 0.00 | 0.00 | 0.05 | 0.12 | 0.20 | 0.42 | 0.50 | 0.56 | 0.60 | 0.64 | 0.70 |

with the intermediate years interpolated in the shipped file and year 40's ratio applying
thereafter. The shape encodes exactly two cited facts: the 25 ‰ *Zillmerung* allowance [REG-R16],
which is why the first two years are zero, and the § 169 Abs. 3 five-year spread **floor**
[REG-R28], which is why it turns positive in year three. It never approaches 1.00, because the
contract has been consuming risk premium throughout.

**Expenses [std]**, all five levels placeholders, the structure cited:

| Item | Value | Unit | Rationale |
|---|---|---|---|
| `acq_permille` | 25.0 | ‰ of *Beitragssumme*, at `t = 0` | Set **exactly at** the § 4 DeckRV *Höchstzillmersatz* [REG-R16], so the ceiling binds visibly rather than notionally |
| `admin_prem_pct` | 0.030 | fraction of each premium collected | Round-number placeholder; absorbs the *Ratenzahlungszuschlag* the model does not charge separately |
| `admin_mth_pp` | 2.00 | EUR per policy in force per month, at `t = 0` prices | Round-number placeholder, a plausible fraction of a mass-market monthly premium |
| `claim_expense_pp` | 1.50 | EUR per annuity payment made | Set **low**, the one expense here with a real argument: the trigger is determined by a third party [R6], so claims cost is materially below a *Berufsunfähigkeitsrente*'s [REG-R29] |
| `expense_infl` | 0.015 | annual | Round-number placeholder; over a 65-year projection it is worth a factor of about 2.6 on the per-policy line, which is not a detail |

The *Beitragssumme* the acquisition charge is struck on is

    beitragssumme = premium_mth_pp() * 12 * (min(prem_end_age, beitragssumme_cap_age) - age_at_entry)

with `beitragssumme_cap_age = 85` **[std]**, for the single premium simply the *Einmalbeitrag*
itself. A lifelong-premium contract has no finite *Beitragssumme* without a convention, and the cap
is that convention; it is a parameter, not a citation.

**The first-order margins [std].** German practice runs two parallel bases over the same contract:
*Rechnungsgrundlagen erster Ordnung* — prudent, statutorily required [REG-R8], and what fixes the
*Bruttobeitrag* — and *zweiter Ordnung*, the best estimate, which is what the projection runs on.
The *Sicherheitszuschlag* is the wedge, and its **direction forks by risk** [REG-R47]. For care,
prudence means **higher incidence, faster deterioration, slower recovery, longer duration in care
(so lower mortality of care recipients) and lower active mortality**, because a life that survives
is a life that can claim:

| Margin | Value | Applied to | Direction |
|---|---|---|---|
| `inc_margin` | 1.25 | `inc_rate` | more claims |
| `det_margin` | 1.15 | `det_rate` | faster progression to the higher-paying grades |
| `rec_margin` | 0.80 | `rec_rate` | fewer recoveries, so longer spells |
| `care_mort_margin` | 0.85 | in-care mortality | longer annuities |
| `act_mort_margin` | 0.90 | active mortality | more lives survive to claim |

All five are **[std]**: only the *direction* of each is cited, no German source here gives a
*Sicherheitszuschlag* level for a *Pflegetafel*, and the responsible actuary's judgment sets it in
practice [REG-R11] [REG-R56]. The **first-order basis carries no lapse at all**, which is both German
practice and what keeps the model acyclic.

**Unisex blending [std].** Pricing uses `unisex_mix_male = 0.50`, so every first-order rate is
`0.5 × male + 0.5 × female`. The projection uses the model point's own sex. The mix is a modelling
choice with no source; "pricing unisex on a 50 / 50 mix while writing 60 / 40" is model risk 7.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month, 0-based, `t = d0 … n` with `d0 = duration_mth_init` and `n = proj_len` |
| `x(t)` | attained age in month `t` = `age_at_entry + t // 12` |
| `y(t)` | policy year = `t // 12 + 1` |
| `g` | *Pflegegrad*, `g = 1 … 5` |
| `π_g` | `benefit_pct(g)`, the *Leistungsstaffel* percentage |
| `R` | `rente_mth`, the *vereinbarte Pflegerente* at *Pflegegrad* 5 |
| `P` | `premium_mth_pp()`, the level monthly gross *Beitrag* per policy |
| `m` | `prem_mode_months()` — 1, 3, 6, 12, or 0 for the *Einmalbeitrag* |
| `μ_A(t)` | force of active-life mortality at `x(t)` |
| `μ_g(t)` | force of mortality in *Pflegegrad* `g` = `mort_mult(g) × μ_A(t)` |
| `ι(t)` | force of incidence into care, **0** while `t < wartezeit_months` |
| `s_g` | `entry_share(g)`, the distribution of the grade first entered |
| `δ_g(t)`, `ρ_g(t)` | forces of deterioration `g → g+1` and of recovery `g → g-1` (from PG1, to active) |
| `w(t)` | monthly lapse probability from the active state, `lapse_rate_mth`, **0** outside the premium term |
| `ℓ_A(t)` | `pols_act(t)` |
| `W_{g,z}(t)` | `pols_karenz(t, g, z)` |
| `ℓ_g(t)` | `pols_pg(t, g)` |
| `E_g(t)` | `esc_pg(t, g)`, the escalation-weighted counterpart of `ℓ_g` |
| `d` | `leistungsdynamik`, the annual escalation of the annuity in payment |
| `K` | `karenz_months` |
| `i` | `rechnungszins`; `v = (1 + i) ** (-1/12)`, used **only** in the pricing engine |
| `α`, `β`, `γ`, `c`, `f` | `acq_permille/1000`, `admin_prem_pct`, `admin_mth_pp`, `claim_expense_pp`, `expense_infl` |

Forces are per annum and dimensionless; `R`, `P` and every cash-flow component are EUR.

### Rates, forces and the monthly step

Every shipped rate is **annual**, and every transition inside a month is computed from **forces held
constant over the month**, with the competing transitions sharing one survival probability in
proportion to their forces. Writing `q` for an annual rate, the force is `μ = -ln(1 - q)`; the
probability of remaining in a state over one month, when the forces out of it are `μ_1 … μ_k`, is

    p_stay = exp(-(μ_1 + … + μ_k) / 12)

and the probability of leaving by route `j` is

    p_j = (μ_j / Σ_k μ_k) * (1 - p_stay)

so that `p_stay + Σ_j p_j = 1` exactly, by construction. This is the standard constant-force,
proportional-allocation convention, and **declaring it is not optional**: adding monthly rates
instead, or applying `q/12`, gives different answers wherever the forces are large, which on this
product means exactly the ages where the money is. Pitfalls 7 and 8 test it.

From the active state, with `μ_A`, `ι`:

    p_act_stay(t)  = exp(-(μ_A(t) + ι(t)) / 12)
    p_act_death(t) = (μ_A(t) / (μ_A(t) + ι(t))) * (1 - p_act_stay(t))
    p_act_care(t)  = (ι(t)   / (μ_A(t) + ι(t))) * (1 - p_act_stay(t))

From *Pflegegrad* `g`, with `μ_g`, `δ_g`, `ρ_g` (and `δ_5 = 0`, `ρ_1` leading to the active state):

    p_pg_stay(t, g)   = exp(-(μ_g(t) + δ_g(t) + ρ_g(t)) / 12)
    p_pg_death(t, g)  = (μ_g(t) / S) * (1 - p_pg_stay(t, g))
    p_pg_worse(t, g)  = (δ_g(t) / S) * (1 - p_pg_stay(t, g))
    p_pg_better(t, g) = (ρ_g(t) / S) * (1 - p_pg_stay(t, g)),   S = μ_g + δ_g + ρ_g

Both sets are published as cells, and `check_states()` uses their summation to one.

### The in-force recursions

**Active state.** Entrants leave, deaths leave, and the survivors of both are exposed to lapse:

    ℓ_A(t+1) = [ ℓ_A(t) * p_act_stay(t) + Σ_g ρ_1-recoveries into active ] * (1 - w(t))

written out, with `Rec(t) = Σ over the PG1 ledger of p_pg_better(t, 1)` the reactivation inflow:

    pols_entry(t, g) = ℓ_A(t) * p_act_care(t) * s_g
    pols_reactiv(t)  = [ ℓ_1(t) + Σ_z W_{1,z}(t) ] * p_pg_better(t, 1)
    pols_lapse(t)    = [ ℓ_A(t) * p_act_stay(t) + pols_reactiv(t) ] * w(t)
    ℓ_A(t+1)         = [ ℓ_A(t) * p_act_stay(t) + pols_reactiv(t) ] * (1 - w(t))

**Lapse acts after the insured decrements and after any reactivation**, on the survivors — the same
ordering frlib's term model uses, stated because the alternative orderings give different answers.

**The *Karenz* ledger**, present only when `K > 0`. Entrants join at `z = 1` and advance one month
at a time, subject to the same transitions as a served life; the clock is **discarded** on
reactivation, because the *Karenzzeit* runs from the onset of *Pflegebedürftigkeit* and a recovered
life who later relapses starts a new onset:

    W_{g,1}(t+1)   = pols_entry(t, g)
    W_{g,z+1}(t+1) = Σ_h W_{h,z}(t) * p_karenz(t, h → g),        1 ≤ z < K
    pols_grad(t, g) = Σ_h W_{h,K}(t) * p_karenz(t, h → g)

where `p_karenz(t, h → g)` is `p_pg_stay` for `h = g`, `p_pg_worse` for `g = h + 1`, `p_pg_better`
for `g = h - 1` and zero otherwise. When `K = 0` the ledger is empty and
`pols_grad(t, g) = pols_entry(t, g)`, which is the degenerate case the base run runs in.

**The paying ledger.**

    ℓ_g(t+1) = ℓ_g(t) * p_pg_stay(t, g)
             + ℓ_{g-1}(t) * p_pg_worse(t, g-1)
             + ℓ_{g+1}(t) * p_pg_better(t, g+1)
             + pols_grad(t, g)

with the `g = 1` recovery term flowing to the active state instead and the `g = 5` deterioration
term absent.

**The escalation ledger.** `E_g(t)` is the same population weighted by each life's own escalation
factor since its annuity began. It obeys the identical recursion with one extra factor and one
different seeding, entrants joining at weight 1:

    E_g(t+1) = (1 + d) ** (1/12) * [ E_g(t) * p_pg_stay(t, g)
                                   + E_{g-1}(t) * p_pg_worse(t, g-1)
                                   + E_{g+1}(t) * p_pg_better(t, g+1) ]
             + pols_grad(t, g)

When `d = 0` this is the `ℓ_g` recursion exactly, so `E_g ≡ ℓ_g` in the base run — an invariant
worth asserting, and `check_esc_ledger()` does. Carrying the escalation as a **value ledger** rather
than a duration-since-onset cohort dimension is what keeps the model O(n) instead of O(n²); the
price is that the model cannot report the distribution of escalation factors, only its aggregate,
which is all the cash flow needs.

**Deaths, and the closure.**

    pols_death(t)     = ℓ_A(t) * p_act_death(t)
                      + Σ_g [ ℓ_g(t) + Σ_z W_{g,z}(t) ] * p_pg_death(t, g)
    pols_dead_cum(t+1)  = pols_dead_cum(t) + pols_death(t)
    pols_lapse_cum(t+1) = pols_lapse_cum(t) + pols_lapse(t)

    pols_if(t) + pols_dead_cum(t) + pols_lapse_cum(t) = pols_if_init()   for every t

The last line is `check_states()`. Because `mort_rate` is forced to 1 in the final year of age, the
identity closes at `t = n + 1` with `pols_if = 0`, so the decrements sum to `pols_if_init()`
exactly — a closure a reader can check with a calculator on the worked example.

### Premium, waiver and the premium-paying population

    pols_in_term(t) = pols_if(t)                      if x(t) < prem_end_age else 0
    pols_waived(t)  = Σ_{g : π_g > 0} ℓ_g(t)          restricted to the in-term population
    pols_prem(t)    = pols_in_term(t) - pols_waived(t)

Three consequences follow directly from the *Leistungsstaffel*, and each is a test. A life in a
*Karenz* ledger **pays**, because no annuity is yet payable and the waiver runs with the annuity. A
life at *Pflegegrad* 1 on the `delib_std` grid **pays**, because `π_1 = 0`; on the `bahr` grid,
where `π_1 = 0.10`, the same life is **waived**. And a life that is downgraded out of the paying
grades **starts paying again**, so `pols_prem` is not monotone.

The instalment is charged only on due months:

    premium_due(t)  = (m > 0) and (t % m == 0) and (x(t) < prem_end_age)
    premium_pp(t)   = P * m           if premium_due(t) else 0
    premiums(t)     = premium_pp(t) * pols_prem(t)

For the *Einmalbeitrag* (`m = 0`), `premium_pp(0) = P_single` and zero thereafter. A waiver that
begins between two due dates therefore takes effect **at the next due date**, which is the German
convention for a *Beitragsbefreiung* on a fractionated contract and is stated because the
alternative — refunding the unearned instalment — is a different and equally arguable rule the model
does not implement.

`cum_prem_max_pp(t)` is the premium payable to date on an uninterrupted path, `P` times the number
of premium-months elapsed inside the term (for the single-premium form, `P_single` from `t = 0`).
It is a **deterministic** quantity, not a ledger, and it is what both the *Rückkaufswert* and the
*Beitragsrückgewähr* are struck on.

### Benefits

    claims(t, "ANNUITY") = R * Σ_g π_g * E_g(t)
    claims(t, "LAPSE")   = rkw_pp(t) * pols_lapse(t)
    claims(t, "DEATH")   = brg_pp(t) * pols_death(t)
    claims(t)            = claims(t, "ANNUITY") + claims(t, "LAPSE") + claims(t, "DEATH")

with

    rkw_pp(t) = rkw_prem_ratio(min(y(t), 40)) * cum_prem_max_pp(t) * (1 - stornoabzug)
    brg_pp(t) = cum_prem_max_pp(t)   if beitragsrueckgewaehr else 0.0

Note what `claims(t, "ANNUITY")` is weighted on: `E_g(t)`, the escalation ledger, **not** `ℓ_g(t)`.
In the base run they are identical; with the dynamic on they are not, and using `ℓ_g` would silently
drop the escalation. Note also that the *Karenz* ledger contributes nothing — a life inside its
deferred period is in care, is counted in `pols_if`, pays its premium and receives no annuity.

**The *Beitragsrückgewähr* implemented here is the gross form**: return of premiums payable to date,
with **no** offset for annuity already paid. The market's more common form nets the annuity off
[S4] [unverified], and the model does not, for a reason worth stating precisely: the netting is
floored at zero **per life**, and the model's ledgers are aggregates, so netting at the aggregate
level would let a life that received a large annuity subsidise one that received none. Implementing
the net form needs a paid-to-date value ledger per state *and* a per-life floor, which an aggregate
projection cannot supply. The consequence — the option overstates the death benefit relative to the
market-standard form — is stated rather than hidden, and pitfall 11 asserts the gross rule.

### Expenses and net cash flow

    expense_infl_factor(t) = (1 + f) ** (t / 12)
    acq_expense_pp()       = α * beitragssumme()
    expenses(t)            = acq_expense_pp() * 1{t = 0}
                           + γ * expense_infl_factor(t) * pols_if(t)
                           + β * premiums(t)
    claim_expenses(t)      = c * expense_infl_factor(t) * Σ_{g : π_g > 0} ℓ_g(t)
    net_cf(t)              = premiums(t) - claims(t) - expenses(t) - claim_expenses(t)
    liability_cf(t)        = -net_cf(t)

The acquisition charge falls at `t = 0` only, so **an in-force model point never incurs it** — its
frame opens at `t = duration_mth_init > 0`. That is correct (the cost was incurred before the
valuation date) and it is worth knowing before comparing an in-force point's first row with a
new-business point's.

`claim_expenses` is per **annuity payment made**, so it is weighted on the paying grades only and a
*Pflegegrad* 1 life on the `delib_std` grid generates none. It is published as its own `result_cf()`
column because it is a per-event cost rather than a per-policy one.

### The pricing engine — `premium_mth_pp()`

Where `premium_mth > 0` on the model point, that is the premium and the engine is not consulted.
Where it is `0.0`, `P` is struck by equivalence on the **first-order** bases: every rate multiplied
by its margin, blended 50 / 50 across the sexes, **no lapse**, discounted at `v = (1+i)^(-1/12)`.
The `tar_*` ledgers obey exactly the recursions above with `w ≡ 0` and the margined forces.

Define, over `t = 0 … n` on the tariff ledgers:

    A  = Σ_t v**t * R * Σ_g π_g * tar_esc_pg(t, g)                  EPV of the annuity
    U  = Σ_{t : premium_due(t)} v**t * m * tar_pols_prem(t)         EPV of premium in units of P
    G  = Σ_t v**t * γ * expense_infl_factor(t) * tar_pols_if(t)     EPV of per-policy admin
    C  = Σ_t v**t * c * expense_infl_factor(t) * Σ_{g:π_g>0} tar_pols_pg(t, g)
    D1 = Σ_t v**t * (premium-months elapsed at t) * tar_pols_death(t)    (0 unless BRG)
    a1 = α * 12 * (min(prem_end_age, beitragssumme_cap_age) - age_at_entry)

Everything on the benefit side that scales with `P` — the *Beitragsrückgewähr* and the *Zillmerung*
allowance — is linear in `P`, so the equivalence

    P * U = A + P * D1 + P * a1 + β * P * U + G + C

solves in closed form:

    P = (A + G + C) / [ U * (1 - β) - D1 - a1 ]
    premium_mth_pp() = rating_factor * P
    prem_net_level_pp() = A / U          the net level premium, benefits only

For the *Einmalbeitrag*, `U = 1` (one payment at `t = 0`) and the same expression gives the
*Einmalbeitrag* directly. The *Risikozuschlag* multiplies the **gross** premium, never the benefit.

`check_prem_equiv_resid(t)` publishes the per-month discounted imbalance

    v**t * [ premium_pp_tar(t) * tar_pols_prem(t) - benefit_tar(t) - expense_tar(t) ]

whose sum over `t` is zero when the equivalence holds; `check_prem_equiv()` is that sum against a
tolerance scaled by `P * U`. It is not a tautology: the two sides are assembled from the ledgers
rather than from the closed form, so substituting a best-estimate rate into one leg, or forgetting
the *Zillmerung* term, makes it fail.

### `result_cf()`

`result_cf()` returns a `DataFrame` indexed by `t` (`df.index.name == "t"`), contiguous from
`duration_mth_init()` to `proj_len()`, in this column order:

| # | Column | Meaning |
|---|---|---|
| 1 | `pols_if` | In force at the **start** of month `t`; first value equals `pols_if_init()` exactly |
| 2 | `pols_act` | Of which active |
| 3 | `pols_care` | Of which in care — the *Karenz* and paying ledgers together |
| 4 | `pols_prem` | Of which actually paying a *Beitrag* |
| 5 | `premiums` | *Beitrag* income, in advance |
| 6 | `claims_annuity` | *Pflegerente* paid, in advance |
| 7 | `claims_lapse` | *Rückkaufswert* paid on surrender, at month end |
| 8 | `claims_death` | *Beitragsrückgewähr* paid on death, at month end; structurally 0 in the base run |
| 9 | `expenses` | Acquisition, per-policy administration and premium-related administration |
| 10 | `claim_expenses` | Per-annuity-payment claims cost |
| 11 | `net_cf` | `premiums - claims_annuity - claims_lapse - claims_death - expenses - claim_expenses` |

A second frame, `result_states()`, publishes the ledgers and rates a reader needs to follow the
projection: `pols_pg1` … `pols_pg5`, `pols_karenz`, `pols_entry`, `pols_grad`, `pols_reactiv`,
`pols_death`, `pols_lapse`, `mort_rate`, `mort_rate_care_pg5`, `inc_rate`, `lapse_rate` and
`premium_pp`. It is not part of the house contract and carries no `check_*`.

### The published identities

`check_*()` takes no argument and returns a **`bool`** over all `t`; the per-`t` residual is
`check_*_resid(t)`. Six identities are published, and the conventions suite calls every one of them
on every model point.

| Check | Identity |
|---|---|
| **`check_net_cf`** (delib ruling 1) | `net_cf(t) = premiums(t) - claims(t, "ANNUITY") - claims(t, "LAPSE") - claims(t, "DEATH") - expenses(t) - claim_expenses(t)` — `net_cf` rebuilt from the statement's own published parts, so the headline number is reconciled in code and not only in prose |
| `check_pols_roll_fwd` | `pols_if(t+1) = pols_if(t) - pols_death(t) - pols_lapse(t)`: lives leave the in-force population only by death or surrender, and every *Pflegegrad* transition is internal |
| `check_states` | `pols_act(t) + Σ_{g,z} pols_karenz(t,g,z) + Σ_g pols_pg(t,g) + pols_dead_cum(t) + pols_lapse_cum(t) = pols_if_init()`: the ledgers plus the absorbed partition the initial cohort at every `t` |
| `check_waiver` | `pols_prem(t) + pols_waived(t) = pols_in_term(t)`: the *Beitragsbefreiung* splits the in-term population and neither loses nor creates a policy |
| `check_esc_ledger` | `esc_pg(t,g) ≥ pols_pg(t,g)` for every `t, g` when `leistungsdynamik ≥ 0`, with **equality** when it is zero |
| `check_prem_equiv` | `Σ_t check_prem_equiv_resid(t) ≈ 0`: the gross premium closes the first-order equivalence, assembled from the tariff ledgers rather than from the closed form |

`check_net_cf` is mandatory across the library; the other five are this product's own. All six use
`roll_fwd_tol` from `basis_table.csv`.

---

## Processing order

Inside month `t`, in this order. Nothing here is optional: several of the pitfalls below are simply
this list executed in a different sequence.

1. **Set the clocks.** `x(t) = age_at_entry + t // 12`; `y(t) = t // 12 + 1`. At
   `t = duration_mth_init()` seed the ledgers from `status` and `pols_if_init()` instead of rolling
   them in — an active point seeds `pols_act`, a point in claim seeds `pols_pg(·, g)` at its grade
   with the *Karenz* already served.
2. **Classify the in-force.** `pols_in_term(t)`, then `pols_waived(t)` from the paying grades, then
   `pols_prem(t)` as the difference. The *Karenz* ledger is in-term and unwaived.
3. **Collect the *Beitrag*, in advance.** If `premium_due(t)`, `premiums(t) = P × m × pols_prem(t)`;
   otherwise zero. Accumulate `cum_prem_max_pp(t)`.
4. **Pay the *Pflegerente*, in advance**, on the **escalation** ledger:
   `claims(t, "ANNUITY") = R × Σ_g π_g × esc_pg(t, g)`. The *Karenz* ledger receives nothing.
5. **Charge start-of-month expenses.** `acq_expense_pp()` at `t = 0` only; per-policy administration
   on `pols_if(t)`, inflated; premium-related administration on the premium just collected; and
   `claim_expenses(t)` on the annuity payments just made.
6. **Look up the month's forces at `x(t)`.** `μ_A`, and `ι` — **zero while `t < wartezeit_months`**;
   `μ_g = mort_mult(g) × μ_A`; `δ_g`; `ρ_g`, damped above `rec_age_ref`. Then `w(t)`, zero outside
   the premium term.
7. **Apply the transitions over the month**, constant forces, proportional allocation. From the
   active state: death, entry into care split by `entry_share`, or stay. From each grade, in both
   the *Karenz* and the paying ledger: death, deterioration, recovery, or stay.
8. **Advance the *Karenz* clock** by one month and graduate the `z = K` cohort into `pols_pg`.
9. **Apply lapse**, to the survivors of the active state **after** the insured decrements and after
   the reactivation inflow. `pols_lapse(t)` is the result; nothing in care lapses.
10. **Pay the end-of-month benefits.** `claims(t, "LAPSE") = rkw_pp(t) × pols_lapse(t)`, and
    `claims(t, "DEATH") = brg_pp(t) × pols_death(t)` where the option is on.
11. **Roll the escalation ledger**: escalate the surviving weights by `(1 + d)^(1/12)`, then add the
    graduating entrants at weight 1.
12. **Post the ledgers to `t + 1`** and form
    `net_cf(t) = premiums - claims_annuity - claims_lapse - claims_death - expenses - claim_expenses`.

The projection ends at `t = proj_len()`. There is **no maturity, no survival benefit and no tail
state**: the contract runs for life, and the closure identity is carried by the decrements.

---

## Known modeling pitfalls

The specific ways an implementation of *this* product looks right and is wrong. Each is a test in
`tests/test_pflegerentenversicherung_de.py`.

1. **Applying an average benefit percentage to an average survival curve.** Grade and mortality are
   correlated: *Pflegegrad* 5 pays most and is lived in shortest. Assert `claims(t, "ANNUITY")`
   equals `R × Σ_g π_g × esc_pg(t, g)`, and that replacing it by `π̄ × R × pols_care(t)`, with `π̄`
   the time-weighted mean percentage, moves the projected annuity total by more than 5 %.
2. **Pricing the annuity in payment on an annuity table.** DAV 2004 R is prudent about people living
   *longer* [REG-R49]; this annuity is paid to a heavily impaired population. Assert
   `mort_rate_care(t, g) > mort_rate(t)` for every `g` and `t`, strictly increasing in `g`, with the
   grade-5 ratio at least 5.
3. **Treating "in claim" as one state exited only by death.** There are three exits. Assert
   `Σ_t pols_reactiv(t) > 0`, that recovery moves lives down the grades, and that suppressing
   recovery and downgrade raises the projected annuity total.
4. **Insuring *Pflegegrad* 1 by accident.** On `delib_std`, `π_1 = 0`. Assert `claims(t, "ANNUITY")`
   is invariant to `pols_pg(t, 1)` and that a grade-1 life is counted in `pols_prem`, not
   `pols_waived`.
5. **Waiving the premium at the wrong grade.** Assert `pols_waived` excludes grade 1 on `delib_std`
   (point 1) and includes it on `bahr` (point 5), with `check_waiver()` closing on both.
6. **Forgetting that the premium revives on a *Herabstufung*.** Assert `pols_prem(t)` is **not**
   monotone decreasing over the ages where downgrades occur, and that `check_waiver()` still closes.
7. **Adding monthly transition probabilities instead of allocating one survival.** Assert
   `p_pg_stay + p_pg_death + p_pg_worse + p_pg_better == 1` to 1e-12 for every `t` and `g`, and the
   same for the three active-state probabilities.
8. **Dividing an annual rate by twelve.** Assert `mort_rate_mth(t) == 1 - (1 - mort_rate(t))**(1/12)`
   and the same form for lapse, and that twelve times the monthly rate is strictly below the annual
   rate wherever that is positive.
9. **Treating the *Karenzzeit* as a benefit gate on the aggregate.** It is a deferral clock per
   onset. On point 7 assert `Σ_t Σ_g pols_grad(t,g) < Σ_t Σ_g pols_entry(t,g)` strictly, the
   shortfall equalling deaths and recoveries recorded inside the *Karenz* ledger.
10. **Escalating the annuity at general-population duration.** With `d = 0.02` on point 8 the
    projected annuity total rises by **less than 5 %**, not the 15–20 % the same escalation buys on a
    healthy-life pension. Assert that, and `esc_pg == pols_pg` exactly on point 1.
11. **Netting the annuity off a *Beitragsrückgewähr* at the aggregate level.** The floor at zero is
    per life; the model pays the **gross** form. Assert
    `claims(t, "DEATH") == cum_prem_max_pp(t) × pols_death(t)` on point 9 and `== 0.0` on point 1.
12. **Paying a surrender value out of the paying state.** Assert `pols_lapse(t) ≤ pols_act(t)`,
    `claims(t, "LAPSE") == 0` wherever `pols_act(t) == 0`, and `lapse_rate(t) == 0` once
    `x(t) ≥ prem_end_age` (point 4).
13. **Charging the *Zillmerung* on the wrong base.** The 25 ‰ ceiling is a per-mille of the
    *Beitragssumme*, not of the annual premium [REG-R16]. Assert
    `acq_expense_pp() == 0.025 × premium_mth_pp() × 12 × (min(prem_end_age, 85) - age_at_entry)`,
    charged at `t = 0` only, so an in-force point never incurs it.
14. **Striking the equivalence premium on the projection basis.** Assert `check_prem_equiv()` is
    `True`, that `premium_mth_pp()` is invariant to every value in `lapse_table.csv`, and that the
    tariff incidence exceeds the best-estimate incidence at every age by exactly `inc_margin`.
15. **Pricing on the model point's own sex.** Assert points 1 and 2 — female and male, identical
    otherwise — have **equal** `premium_mth_pp()` and **unequal** projected annuity totals, the
    female point's being larger [REG-R34].
16. **Collecting a premium in a month that is not a due date.** Assert `premiums(t) == 0` at every
    non-due `t` on points 3, 4 and 5, and `premium_pp(t) == premium_mth_pp() × prem_mode_months()` at
    every due `t`.
17. **Using the *Pflegegrad* stock distribution as the entry mix.** The stock is about
    9 / 44 / 27 / 14 / 6 % [R18]; entrants are not. Assert `Σ_g entry_share(g) == 1.0` and that the
    model's own stock share at grades 4 and 5 over the whole projection **exceeds** `entry_share`.

Two further errors are worth naming because they are the ones a *user* will make. **Reading a
payment-frequency difference as a price difference**: the model folds the *Ratenzahlungszuschlag*
into the administration assumption, so annual mode prices slightly *below* monthly, the opposite
sign to a real tariff. And **treating `proj_len()` as a row count**: it is the last projected index,
and the frame starts at `duration_mth_init()`.

---

## Policyholder behaviour modelling

Every dynamic formula here is a **[std]** reference construction; **no German calibration evidence
for any of them exists in this corpus** (research gap 20).

- **Base lapse [std].** The duration table in class (c), from the active state only, zero after the
  premium term ends. The argument for the shape, not its level, is *Zillmerung*: the *Rückkaufswert*
  is near zero for the first years [REG-R16] [REG-R28], so an early lapse is expensive to the
  policyholder and the profile is flatter than a savings product's.
- **No lapse from a paying grade [std].** A claimant with a waived premium has no premium to default
  on and a live annuity to forfeit. A *Pflegegrad* 1 life on `delib_std` does still pay and could in
  principle lapse; the population is small and the model does not model it.
- **Premium-shock lapse [std], optional, off.** The *Beitrag* is level and guaranteed, so the
  affordability shock frlib's `temporaire_deces` models has no counterpart here. What could replace
  it is a *Zahlbeitrag* shock — a withdrawal of the surplus rebate raises the amount actually called
  without invoking § 163 [REG-R27] [REG-R53] — and the model carries no rebate, so the module is
  empty and is named only so that a user who adds a rebate knows what to add with it.
- **Selective lapsation [std], optional, off.** Lapsers are healthier, so persisters' incidence
  should be loaded: `inc_rate_eff(t) = inc_rate(t) × [1 + λ × max(0, w_cum(t) - w_ref)]` with
  `w_ref = 0.30`, `λ = 0.25` and base run `λ = 0`. The effect is **smaller** here than on a term
  cover, because cumulative lapse is largely complete decades before the risk period.
- **Not modelled at all, each for a stated reason.** *Beitragsfreistellung* take-up — no split
  between the three German exits exists in the corpus [REG-R28]. *Beitragsdynamik* acceptance — a
  behaviourally driven second premium path with no evidence behind it. *Höherstufung* application
  behaviour — the insured applies and the state re-assesses [R6], so grade change is biometric here
  rather than elective. And anti-selection at purchase, which underwriting removes [S4] and which
  decays long before the claims arrive.

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `point_id = 1`;
`policy_id = "PFL-000001"`; `sex = F`; `age_at_entry = 45`; `duration_mth_init = 0`;
`status = aktiv`; `rente_mth = 1,000.00` EUR per month, the *vereinbarte Pflegerente* at
*Pflegegrad* 5; `staffel_id = delib_std`, so the *Leistungsstaffel* is
0 / 30 / 50 / 75 / 100 % across grades 1 to 5; `prem_end_age = 110`, equal to `omega_age`, so the
*Beitrag* is payable for life; `prem_mode = monthly`, so `prem_mode_months = 1` and a *Beitrag* is
due in every month of the term; `premium_mth = 0.00`, the sentinel that makes the model strike the
*Beitrag* by equivalence; `rating_factor = 1.00`, standard rates; `wartezeit_months = 0`;
`karenz_months = 0`; `leistungsdynamik = 0.00`; `beitragsrueckgewaehr = False`;
`stornoabzug = 0.00`; `pols_if_init = 1.0`. Hence `proj_len() = 12 × (110 − 45) − 1 = 779`, the
frame runs from `t = 0` to `t = 779`, and the projection covers attained ages 45 to 109 — 780
monthly rows, of which the table below shows a representative selection together with the
full-precision totals.

**Assumptions, each tagged.** *Rechnungszins* `i = 1.00 %` p.a., used **only** in the pricing
engine [REG-R14] [REG-R15]. Active-life mortality
`mort_rate(F, x) = 1 − exp(−4.76290e−06 × 1.119962^x)` **[std]**, anchored at
`q(65) = 0.75 %` and `q(85) = 7.0 %`, with `mort_rate(F, 109) = 1.0` by the limiting-age convention
**[std]**. Incidence `inc_rate(F, x) = min(0.0110 × exp(0.1400 × (x − 65)), 0.50)` **[std]**,
anchored on prevalence doubling every five years of age above 75 [R18] [unverified]. Entry mix
0.20 / 0.38 / 0.24 / 0.13 / 0.05 across grades 1 to 5 **[std]**. Deterioration
0.28 / 0.24 / 0.20 / 0.16 / 0.00 and recovery 0.10 / 0.06 / 0.04 / 0.02 / 0.01 a year **[std]**, the
recovery rates damped by `exp(−0.10 × max(0, x − 75))` **[std]**. In-care mortality multiples
1.5 / 2.5 / 3.5 / 6.0 / 9.0 on the active force **[std]**. Lapse from the active state
6.0 / 5.0 / 4.0 / 3.5 / 3.0 % in policy years 1 to 5, 2.5 % in years 6–10, 2.0 % in 11–20 and 1.5 %
from year 21 **[std]**, converted by `1 − (1 − q)^(1/12)`. *Rückkaufswert*
0.00 / 0.00 / 0.05 / 0.12 / 0.20 of premiums paid in policy years 1 to 5, rising to 0.42 by year 10
and 0.70 by year 40 **[std]**, with `stornoabzug = 0`. Expenses **[std]**: acquisition
`25 ‰ × Beitragssumme` at `t = 0`, the *Beitragssumme* being `P × 12 × (85 − 45) = 480 P`;
administration 3.0 % of each *Beitrag* collected plus 2.00 € per policy in force per month;
claim expense 1.50 € per annuity payment; expense inflation 1.5 % a year. First-order margins
**[std]**: incidence × 1.25, deterioration × 1.15, recovery × 0.80, in-care mortality × 0.85,
active mortality × 0.90, and **no lapse** in the tariff basis. Pricing blended 50 / 50 male / female
**[std]** [REG-R34]; the projection runs on the female basis. No *Wartezeit*, no *Karenzzeit*, no
*Leistungsdynamik*, no *Beitragsrückgewähr*, no *Überschussbeteiligung* and no behaviour modules.

The band the research file argues for this configuration is **about 50,00 € to 100,00 € a month**
**[std]** (product spec, footnote 9). It is derived arithmetic, not a market observation: a model
premium well outside it indicates an error in the bases, and one inside it is not thereby
validated. The table below prints the model's own equivalence premium; the text under it says which
end of the band it lands at and why.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The *Deckungsrückstellung*.** § 341f HGB requires it prospectively on the tariff bases
  [R12] [REG-R54]; the DeckRV fixes the *Höchstrechnungszins* those bases may use — 1,00 % for new
  business from 1 January 2025, and whatever rate the cohort was written on, for the whole term
  [REG-R14] [REG-R15] — and caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme* [REG-R16]. Here
  the reserve rises for roughly thirty-five years, peaks where the incidence curve crosses the level
  premium, and runs off: an ageing reserve in economic function and a *Deckungsrückstellung* in law.
  **The model does not compute it**, and the *Rückkaufswert* enters as contractual data rather than
  as a derived reserve — which is what keeps `check_prem_equiv_resid(t)` a closure residual rather
  than a reserve in disguise.
- **The *Zinszusatzreserve*.** An HGB reserve with no counterpart elsewhere in this repository,
  driven by the ten-year *Referenzzins* of § 5 Abs. 3 DeckRV under the *Korridormethode* [REG-R17].
  A long-dated, interest-sensitive contract is exactly what attracts it. Not computed here.
- **The § 169 VVG floor.** A model carrying a zillmerised reserve applies **two** rules separately —
  what the DeckRV lets the insurer reserve, and what § 169 makes it pay with acquisition costs spread
  over at least five years — the tighter binding [REG-R16] [REG-R28]. `surrender_table.csv` encodes
  the *result* of both. Whether a pure-risk *Pflegerente* is inside § 169 at all is open (gap 9).
- **Solvency II best estimate.** Probability-weighted future cash flows discounted at the relevant
  risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6], reaching German life
  business through the VAG rather than directly: `BEL = Σ_t v(t) × liability_cf(t)`. **No
  cost-of-capital rate, contract-boundary rule or standard-formula shock in this library was read
  from a retrieved instrument.**
- **The contract boundary, easier here than on a *Pflegetagegeld*.** The premium is level and
  guaranteed, adjustable only on the narrow § 163 route [REG-R27], so the insurer has no unilateral
  right to reprice the individual contract — the usual trigger for a boundary at the next repricing
  date. The whole projected stream is therefore inside the boundary on the natural reading; a
  *Pflegetagegeld* under § 203 VVG is the opposite case [R14]. The point is [unverified].
- **Surplus, IFRS 17 and professional standards.** The *Risikoergebnis* — the release of the
  first-order margins as experience emerges — is the dominant surplus source here [REG-R47],
  distributed under the MindZV and the RfBV [REG-R10] [REG-R18] [REG-R19]; the model produces the
  best-estimate leg and the `tar_*` engine the first-order leg, and neither becomes a declared rate.
  IFRS 17 fulfilment cash flows plus a CSM [REG-R55] are fed by the same engine, with grouping, CSM
  and risk adjustment out of scope. The DAV's *Fachgrundsätze* bind the responsible actuary who
  signs the bases [REG-R11] [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German *Pflegerente* block.

1. **Duration in care — the in-care mortality multiples.** They are the direct multiplier on the
   liability and the weakest-evidenced quantity in the corpus (research gap 19). The research file's
   own arithmetic shows a mean spell moving from four years to five changing the premium by about a
   quarter. The shipped multiples (1.5 / 2.5 / 3.5 / 6.0 / 9.0) are **[std]** order-of-magnitude
   reasoning, and they carry the product.
2. **Incidence level and slope.** The slope is anchored to one qualitative statement — prevalence
   doubling every five years above 75 [R18] [unverified] — and compounds over sixty-five years, so
   it is the more dangerous of the two. A ±0.01 change in `g` moves the incidence at 90 by about a
   third.
3. **The *Pflegegrad* definitional break.** DAV 2008 P was built on the *Pflegestufen*, the BGH will
   not map the scales [REG-R36] [REG-R51], and the 2017 reform widened the insured population
   [R9]. **This is the largest basis risk in the product**, it is not a parameter of the model, and
   no sensitivity in this list captures it.
4. **The *Rechnungszins*.** Benefits fall on average some thirty-five years after issue, so this is
   the **most interest-sensitive product in delib**: a 100 bp change moves the equivalence premium
   far more than on a term assurance or an endowment. It is also the one assumption in the pricing
   engine that is genuinely cited [REG-R14] [REG-R15].
5. **The middle steps of the *Leistungsstaffel*.** Two tariffs with the same 100 % top step differ
   in expected cost by more than the headline suggests, because the time-weighted average benefit
   over a spell is about half of the top step. Compare model point 1 with model point 5.
6. **Lapse.** Nothing in the corpus supports any level (research gap 20). On this product lapse is
   *profitable* — an early lapser paid for years and never reached the risk period — so the usual
   protection intuition is inverted, and the pricing basis deliberately excludes it.
7. **The unisex mix.** Pricing blends 50 / 50 while the projection runs on the point's own sex. A
   book written 60 / 40 female against a 50 / 50 price is under-priced by the whole of that
   mismatch, and the mix is endogenous to the price [REG-R34].
8. **Expense levels and the *Zillmerung* base.** Every level is **[std]** (research gap 2). At the
   smallest benefit in the model point table — 500 € a month on point 14 — the per-policy expense
   line, not the biometrics, decides whether the cell is viable.
9. **No select mortality after onset.** Mortality is highest immediately after onset, especially at
   grades 4 and 5 [unverified]; the model uses an aggregate in-care mortality. The consequence is
   directional and worth stating: **the model understates how much a *Karenzzeit* removes**, so
   model point 7's reduction is a floor rather than an estimate.
10. **The terminal age and the payment convention.** `omega_age = 110` **[std]** with `q = 1` forced
    in the last year of age, and annuity and premium both in advance. Both are declared conventions
    rather than facts; moving the annuity to arrears would shift the whole benefit stream one month
    and break the waiver's alignment with it.
