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
- **The one place a discount rate appears.** The contract's *Beitrag* is a **priced** quantity, and
  German practice strikes it by equivalence at the *Rechnungszins* on the first-order
  (*erster Ordnung*) bases [REG-R8] [REG-R47]. The model therefore carries a second, self-contained
  actuarial-value engine — the `tar_*` cells — whose only output is `premium_mth_pp()`. **That
  engine discounts; the projection does not.** Keeping the two apart is what makes the projected
  cash flows a clean best-estimate stream while the premium in them is still the contract's own.
- **Projection frequency.** **Monthly grid.** The *Pflegerente* is a monthly annuity, the *Beitrag*
  is normally a monthly instalment, and the *Pflegegrad* can change in any month, so the monthly grid
  is the contract's own grid rather than a refinement of an annual one. The `_S` suffix follows
  lifelib (`basiclife/BasicTerm_S`, `savings/CashValue_SE`).
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
  of age so the model is a closed system rather than a truncated one: every life either dies or
  lapses inside the frame, and the decrement closure identity holds exactly. Setting the terminal
  age is a modelling choice, not a table fact; the DAV tables run higher [R15] [REG-R51], and the
  parameter is exposed. The truncation costs nothing material: the probability that an active life
  aged 45 survives to 110 is of the order of 1e-4 on the shipped basis.
- **Timing conventions [std].** Within month `t`: the *Beitrag* is collected **at the start** of the
  month, in advance, from the lives then in the premium-paying states; the *Pflegerente* is paid
  **at the start** of the month, in advance, to the lives then in a paying *Pflegegrad*; per-policy
  and premium-related expenses are charged at the start of the month; transitions act **over** the
  month; and death and surrender benefits fall **at the end** of the month. `pols_if(t)` is the
  count at the **start** of month `t` and is the weight on that same `result_cf()` row's cash flows,
  as the house style requires; end-of-period state is reached through `pols_if_at(t, "END")`.
- **Why the annuity is in advance.** German *Renten* — *Pflegerente* and
  *Berufsunfähigkeitsrente* alike — are conventionally *monatlich vorschüssig*, and paying in
  advance puts the annuity on the same weight as the premium it replaces, which is what lets
  `check_waiver()` reconcile the two streams against one ledger. An arrears convention would move
  the annuity one month later and the waiver would no longer line up with it.
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

**The three attributes a reader is most likely to get wrong**, and each is a numbered pitfall.
`sex` is a *projection* input and must not touch the price [REG-R34]. `premium_mth = 0.0` is a
sentinel, not a free contract. And `duration_mth_init` shifts where the frame **starts** without
changing `proj_len()`, because `proj_len()` is a property of the contract and not of the valuation
date.

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

Between them the fourteen exercise both premium forms (*laufender Beitrag* and *Einmalbeitrag*),
all four instalment frequencies, both *Leistungsstaffeln*, every switchable option, two in-force
points — one active, one in claim — and both ends of the entry-age band.

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

Nine files, and every one of them is read by a reader cells in `Data` — the conventions suite
asserts that there are no orphans in either direction.

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

Forward moves are *Verschlechterung* (deterioration), backward moves are *Herabstufung* and, out of
PG1, *Reaktivierung*. Death is reachable from every state. **Lapse is reachable only from `aktiv`**
[std]: a claimant whose premium is waived has nothing to lapse from and everything to lose, and the
PG1 population that does still pay is small; the choice is stated, and pitfall 12 tests it.

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

There is **no account value** and **no paid-up state**. The *Deckungskapital* is a real object of
this contract and is deliberately **not** a state variable of this model: the library publishes
undiscounted cash flows and leaves the reserve to the layer that consumes them, and the guaranteed
*Rückkaufswert* enters as data rather than as a computed reserve (product spec, footnote 21).

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

**What is *not* in this table, and why it matters.** There is **no cited premium**, no cited charge,
no cited transition rate and no cited *Rückkaufswert* level anywhere in this product's corpus. The
contractual column above is unusually thin compared with
`frlib/products/temporaire_deces/technical-notes.md`, which could tabulate a complete published
attained-age rate card. Everything numeric that is missing here appears in class (c) as **[std]**,
and that displacement is the single most important thing to know about this model.

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

**Why they cannot be a proxy for DAV 2008 P.** DAV 2008 P is the market-standard first-order basis
for German LTC business on the life chassis [R15] [REG-R51]. It is the property of the Deutsche
Aktuarvereinigung, is not public, and **is not redistributed by this library**; no value from it
appears anywhere in delib and none may. It was moreover built on the pre-2017 *Pflegestufen*, and
the BGH has refused to map those to the *Pflegegrade* [REG-R36] [REG-R51] — so a table calibrated on
*Pflegegrad* data is not a DAV 2008 P proxy even in principle. **A replacement table must preserve
four properties**, and a user substituting one should check each: (a) incidence by attained age, sex
and *grade of entry*, because entry is not uniformly at the lowest grade — a stroke or a fracture
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

The three consequences the research file draws from those multiples all show up in the projection
and all three are pitfalls. **The annuity in payment is short**, of the order of three to five
years, not the fifteen to twenty of a healthy-life pension at the same age — so pricing it on an
annuity table such as DAV 2004 R would be prudent in exactly the wrong direction and would
materially overprice the benefit [R16] [REG-R49]. **Grade and mortality are correlated**, so the
highest-paying state is also the shortest-lived, and a model that applies an average benefit
percentage to a survival curve computed at an average mortality is wrong in a way the totals will
not reveal. And **a deferred period bites harder than its length suggests**, because a material
share of new claimants die inside it.

**Lapse [std].** From the **active** state only, and zero once the premium-paying period has ended:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–10 | 11–20 | 21–40 |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate` | 6.0 % | 5.0 % | 4.0 % | 3.5 % | 3.0 % | 2.5 % | 2.0 % | 1.5 % |

Year 40's rate applies to every later policy year. **No lapse rate for this product at any duration
was established** (research gap 20). The shape is a modeller's construction with a stated argument:
*Zillmerung* makes an early lapse expensive to the policyholder — the *Rückkaufswert* is near zero
for the first years — so the profile is lower and flatter than a savings product's and declines with
duration, and a paid-up contract with no further premium has no premium-driven exit at all. The
monthly rate is `lapse_rate_mth(t) = 1 - (1 - lapse_rate(t)) ** (1/12)`, which the conventions suite
checks is strictly below the annual rate wherever that is positive.

**The guaranteed *Rückkaufswert* [std].** Expressed as a fraction of premiums paid to date, by
completed policy year — the scale-free form, and the form in which a German contract states the
values [REG-R28]:

| Policy year | 1 | 2 | 3 | 4 | 5 | 10 | 15 | 20 | 25 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rkw_prem_ratio` | 0.00 | 0.00 | 0.05 | 0.12 | 0.20 | 0.42 | 0.50 | 0.56 | 0.60 | 0.64 | 0.70 |

with the intermediate years interpolated in the shipped file and year 40's ratio applying
thereafter. The shape encodes exactly two cited facts and nothing else: the 25 ‰ *Zillmerung*
allowance [REG-R16], which is why the first two years are zero, and the § 169 Abs. 3 five-year
spread **floor** [REG-R28], which is why it turns positive in year three and rises steeply to year
five. It never approaches 1.00, because the contract has been consuming risk premium throughout.

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

All five are **[std]**. Only the *direction* of each is cited; no German source in this corpus gives
a *Sicherheitszuschlag* level for a *Pflegetafel*, and the responsible actuary's own judgment sets
it in practice [REG-R11] [REG-R56]. The **first-order basis carries no lapse at all**, which is
both German practice and what keeps the model acyclic: a pricing quantity may not depend on a
behavioural assumption that depends on the path that depends on the premium.

**Unisex blending [std].** Pricing uses `unisex_mix_male = 0.50`, so every first-order rate is
`0.5 × male + 0.5 × female`. The projection uses the model point's own sex. The mix is a modelling
choice with no source; "pricing unisex on a 50 / 50 mix while writing 60 / 40" is model risk 7.
