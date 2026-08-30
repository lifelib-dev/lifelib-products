# Technical Notes

**Status:** Draft, 2026-08-29 (access date for every citation below).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Riester_DE_A`**, **annual** grid — for the standardized composite German **klassische
Riester-Rentenversicherung** defined in `product-spec.md` (same directory). This is not any single
insurer's product; **no carrier-specific parameter was established for any German Riester product,
at any house, for any year**, so every carrier parameter below is **[std]** and every statutory one
is cited. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried from
`_research/riester_rente.md`; frozen); [REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R56 numbering). [unverified]
marks a claim no search result corroborated. Parameter values are identical to those in
`product-spec.md`. Cells names, model-point columns and CSV headers are English `lower_snake_case`;
German terms of art keep their German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — the saver's
  *Eigenbeitrag*, the state *Zulage*, death, surrender, transfer, lump-sum, commutation and annuity
  benefits, expenses and commission — for a single-policy model point on an expected
  (probability-weighted) basis, together with the two state variables that make the product what it
  is: the account (*Deckungskapital* plus *Überschussguthaben*) and the **Beitragsgarantie
  accumulator**. Discounting, the *Deckungsrückstellung*, the *Zinszusatzreserve*, Solvency II
  technical provisions, the risk margin and capital are **out of scope** and are referenced rather
  than specified (see *Valuation and reserve pointers*).
- **Projection grid and what `t` counts.** **Annual**, **1-based**: `t = 1 … proj_len()`, one
  policy year per step, `t = 1` being the policy year that opens at the **valuation date**. The
  valuation date is **1 January 2027** [std] — the first day on which the product is closed to new
  business [REG-R44] — so `calendar_year(t) = 2026 + t`. The contract is itself annual in every
  respect that matters here: the Zulage is an annual entitlement determined on a calendar year
  [R9] [R10], the *Überschuss* is declared annually, and the *Beitragsgarantie* is tested once. The
  one genuinely sub-annual element, the **monthly** annuity in payment, is compressed to an annual
  amount and the compression is stated below and tested.
- **`proj_len()` is the last projected period index**, per the library ruling asserted in
  `tests/test_model_conventions_de.py`: `result_cf().index[-1] == proj_len()`.
  `proj_len() = omega_age − age(1) + 1`, with `age(1) = issue_age + duration_init` and
  `omega_age = 110` **[std]**. The frame is contiguous `1 … proj_len()` on every model point,
  including a point that commutes at *Rentenbeginn* and therefore carries zeros to the end — a
  uniform frame is what lets two model points be read side by side, and truncating a commuted point
  is a numbered pitfall.
- **Two phases in one projection.** `t_conv() = rentenbeginn_age − age(1) + 1` is the **conversion
  year**. `is_accum(t)` holds for `t < t_conv()`, `is_payout(t)` for `t ≥ t_conv()`. The
  accumulation recursions stop at `t_conv()`; the annuity liability runs from `t_conv()` to
  `proj_len()`. A model that stops at *Rentenbeginn* has not modelled a lifelong annuity, which is
  the benefit the AltZertG requires [R1] [REG-R43].
- **Timing conventions [std].** The *Eigenbeitrag* and any unsubsidised contribution are received
  at the **start** of the policy year; the *Zulage* earned in year `t − 1` is credited at the
  **start** of year `t`, alongside that year's own contribution; charges are deducted from the
  contribution at the start; interest is credited at the **end** of the year on the account plus the
  year's *Sparbeitrag*; decrements act at the **end** of the year, **after** crediting, so an
  exiting policy takes the full year's interest; and death, surrender and transfer benefits are
  struck on `av_total_pp(t + 1)`. Conversion happens at the **start** of `t_conv()`, after the final
  Zulage has been credited and before any payout-phase mortality. Annuity instalments are paid at the
  **start** of each payout year.
- **The monthly annuity on an annual grid [std].** The contract pays a monthly *Leibrente* in
  advance [R1]. The model pays **twelve instalments as one annual amount at the start of the payout
  year**, to those alive at the start. Undiscounted, the two agree for a survivor; they differ for a
  life that dies during the year, to whom the model pays a full year and the contract pays only the
  instalments falling due — an overstatement of roughly `½ · q(x) · 12R` a year, about 0,7 % of the
  annuity at attained age 70 on the shipped proxy. The *level* of the annuity is nonetheless right,
  because the conversion factor carries the Woolhouse `−11/24` correction. `products/sofortrente/`
  runs monthly for exactly this reason.
- **Age basis.** Age last birthday, `age(t) = issue_age + duration_init + t − 1`. Riester tariffs
  are **unisex** from a 2006 vintage [R23] [REG-R34], so `sex` is carried for reporting only and
  must not enter any rate.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** — contributions
  and Zulagen positive, benefits and expenses negative — with the outgo-positive orientation
  published as `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash
  flows to the cent, `pols_if` to six decimals **[std]**.
- **Out of scope, and said so rather than left to be discovered.** No unit-linked funds and no
  rebalancing algorithm (that chassis is `fondsgebundene_rentenversicherung`); no *Auszahlungsplan
  mit Restverrentung*; no Wohn-Riester in either limb — no *Eigenheimbetrag* withdrawal decrement,
  no certified *Darlehen*, no *Wohnförderkonto* [R13] [R19]; no *Berufsunfähigkeits-*
  *Zusatzversicherung* liability (only the guarantee carve-out its premium creates); no
  *Versorgungsausgleich*; no surplus in payment; no *Günstigerprüfung* and no policyholder tax of
  any kind; and no apportionment of investment return between the two contribution pools, which a
  real *Leistungsmitteilung* must perform [R12].

---

## Model inputs

Inputs are **external CSVs beside `run.py`**, in the `annuallife/TradLife_A` layout: the model folder
holds `__init__.py`, `_system.json` and the two Space directories and nothing else. `Data` holds
`input_dir()`, one reader cells per file and one `*_file` string Reference per file, takes no
parameters, and is therefore read **once per model** rather than once per model point; `Projection`
reaches it through a `data` Reference and holds no `*_file` Reference and no `input_dir`.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the twenty-six attributes tabulated below |
| `mort_table_accum.csv` | `age` (16–110) | `qx`, `provenance` |
| `annuity_mort_table.csv` | `age` (55–110) | `qx_base`, `improvement`, `provenance` |
| `lapse_table.csv` | `duration` (1–60) | `lapse_rate`, `transfer_rate`, `provenance` |
| `zulage_schedule.csv` | `zulage_id`, `t` | `unmittelbar`, `n_kinder_pre2008`, `n_kinder_post2008`, `bonus`, `provenance` |
| `income_schedule.csv` | `income_id`, `t` | `income`, `provenance` |
| `surplus_scenario.csv` | `scenario_id`, `t` | `decl_rate`, `provenance` |
| `freq_loading.csv` | `prem_freq` | `load`, `provenance` |

**Every file except `model_point_table.csv` carries a per-row `provenance` column**, delib's second
ruling: a model point is a configuration, every other row is an assumption and says where its number
came from. The two decrement tables are **[std] proxies** for proprietary DAV tables that this
library does not ship [REG-R47] [REG-R48] [REG-R49], anchored so that the worked example reproduces
exactly; what a replacement must preserve is stated in assumption class (c) and in `sources.md`.

### Cells vocabulary

`Data` publishes `input_dir`, `model_point_table`, `mort_table_accum`, `annuity_mort_table`,
`lapse_table`, `zulage_schedule`, `income_schedule`, `surplus_scenario` and `freq_loading`.

`Projection` publishes the library's shared names — **`model_point`, `proj_len`, `age`, `pols_if`,
`mort_rate`, `claims`, `expenses`, `net_cf`, `result_cf`** — plus, in the same lifelib spelling:
`pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse`, `pols_transfer`, `pols_conv`,
`pols_annuity_pay`; `mort_rate_at_age`, `annuity_mort_rate`, `lapse_rate`, `transfer_rate`;
`duration`, `calendar_year`, `t_conv`, `is_accum`, `is_payout`; `income_ref`,
`zulage_entitlement_pp`, `zulage_granted_pp`, `zulage_pp`, `zulage_cum_pp`,
`mindesteigenbeitrag_pp`, `eigenbeitrag_pp`, `eigenbeitrag_paid_pp`, `contrib_total_pp`;
`acq_charge_pp`, `admin_charge_pp`, `prem_to_av_pp`; `dk_pp`, `surplus_acct_pp`, `av_total_pp`,
`av_total_pp_at`, `av_total_at`, `int_guar_pp`, `int_surplus_pp`, `int_credited_pp`, `decl_rate`;
`guar_pp`, `guar_carve_out_pp`, `garantieluecke_pp`, `pool_gefoerdert_pp`, `pool_ungefoerdert_pp`;
`slueb_pp`, `bewres_pp`, `account_conv_pp`, `capital_conv_pp`, `garantieluecke_conv_pp`,
`ann_factor`, `rentenfaktor_curr`, `rentenfaktor_applied`, `annuity_month_pp`, `is_kleinbetrag`,
`teilkapital_pp`, `annuity_capital_pp`, `commutation_pp`, `annuity_pp`; `db_pp`, `cv_pp`,
`transfer_value_pp`, `exit_charge_pp`; `premiums`, `zulagen`, `int_credited`, `commissions`,
`liability_cf`; and the six `check_*` cells with their `check_*_resid` companions. `claims(t, kind)`
takes an uppercase `kind` in `{DEATH, LAPSE, TRANSFER, LUMPSUM, COMMUTATION, ANNUITY}` and produces
the `claims_<lowercase kind>` columns. **No retired name is used**: there is no `lapse_rate_ann`, no
`prem_net_pp`, no `mort_ae_factor`, no `check_pols_if`, no `claims_wd` and no bare `claims` column.

---

## Model point attributes

`model_point_table.csv` is indexed by `point_id` and carries the columns below. It is the one input
file exempt from the provenance rule, because a model point is a **configuration** rather than an
assumption. The right-hand column names the points that exercise each attribute away from its base
value; the thirteen points are described under *Worked example*.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection` is parameterized by it | all |
| `sex` | enum {M, F} | Reporting only. Pricing, the conversion and every rate are **unisex** [R23] | all |
| `issue_age` | int | Attained age at conclusion of the contract | all |
| `duration_init` | int | Completed contract years at the valuation date; 0 for a point projected from issue | 2, 6, 13 at 0 or 1 |
| `pols_if_init` | float | Policies represented; `result_cf()`'s first `pols_if` equals it exactly | all |
| `rentenbeginn_age` | int | Attained age at which the payout phase starts; bounded below by 62 for a contract concluded from 2012 [R1] | 13 (at the statutory floor, 62) |
| `rechnungszins` | float | The tariff's guaranteed rate, at or below the *Höchstrechnungszins* of the vintage [R22] [REG-R15] | 3 (0,90 %), others 0,25 % |
| `beitragssumme` | EUR | The *Beitragssumme* fixed at conclusion; the acquisition-charge and initial-commission base | all |
| `contrib_form` | enum {mindest, fixed} | `mindest` recomputes the § 86 amount every year; `fixed` is a level contractual contribution | 5, 8 |
| `contrib_fixed_pp` | EUR p.a. | The level contribution under `fixed`; 0 under `mindest` | 5 (60,00), 8 |
| `contrib_ratio` | float | Fraction of the *Mindesteigenbeitrag* actually paid; drives the proportional Kürzung [R10] | 7 (0.50) |
| `contrib_extra_pp` | EUR p.a. | Unsubsidised contribution above the § 10a ceiling; enters the account **and** the guarantee, draws no Zulage [R12] | 8 (900,00) |
| `rider_prem_pp` | EUR p.a. | Contribution applied to a biometric rider. **Not a cash flow of this model**; it appears only in the guarantee carve-out, capped at 20 % of total contributions [REG-R43] | 9 (400,00) |
| `income_id` | str | Key into `income_schedule.csv` | all |
| `income_init` | EUR | Contribution-liable earnings in the calendar year **before** the projection starts; the reference income for `t = 1` | all |
| `zulage_id` | str | Key into `zulage_schedule.csv` | all |
| `zulage_init_pp` | EUR | The Zulage credited in projection year 1, earned in the year before it | 6 (375,00, including the bonus) |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency; keys `freq_loading.csv` | 3, 4, 6, 7, 10, 13 |
| `bfs_year` | int | Projection year from which contributions stop (*Beitragsfreistellung*); 0 = never | 10 (year 4) |
| `dk_pp_init` | EUR | *Deckungskapital* at the valuation date | all |
| `surplus_pp_init` | EUR | *Überschussguthaben* at the valuation date | all |
| `guar_pp_init` | EUR | *Beitragsgarantie* accumulator at the valuation date | all |
| `teilkapital_share` | float | Elected *Teilkapitalauszahlung*, 0 to the statutory 0.30 [R1] | 12 (0.00) |
| `rentenfaktor_guar` | float | Guaranteed *Rentenfaktor*, € of monthly annuity per 10 000 € of capital, struck at inception | all |
| `rentengarantie_years` | int | *Rentengarantiezeit*; payments continue to beneficiaries for this many years from *Rentenbeginn* | 12 (0) |
| `scenario_id` | str | Key into `surplus_scenario.csv`; names the `decl_rate` path | 11 (`low`) |

Three of these are the ones a reader from another market is most likely to mis-set. `zulage_init_pp`
exists **only** because the Zulage arrives a year late [R11], so an in-force point opens owing one;
`rider_prem_pp` is a contribution the model deliberately does **not** see as cash; and
`contrib_ratio` is not a lapse or a premium holiday but the § 86 proportional Kürzung, which reduces
the **subsidy** and not only the contribution.

### The thirteen model points

Between them they exercise both contribution forms, all four payment frequencies, every option the
contract carries, an at-issue point beside the in-force ones, and four boundary cases.

| # | Cell | What it exercises |
|---|---|---|
| **1** | **Anchor** — F, issue age 47 in 2024, in force at duration 3, attained 50, *Rentenbeginn* 67, 0,25 %, one child born 2010, annual | The worked example. A live acquisition-charge window, a falling Zulage step, the 2 100 € ceiling binding from year 13, a 30 % lump sum, a 10-year *Rentengarantiezeit*, and an account opening **below** the guarantee |
| **2** | The same contract **at its own inception** — `duration_init = 0`, 2024 | Acquisition charge from contract year 1, the acquisition expense and initial commission cash at issue, and the **reconciliation of point 1's opening balances** |
| **3** | Family with children born **2006 and 2010** — M, issue age 38 in 2018, 0,90 %, monthly | Both *Kinderzulage* rates running **simultaneously** (660,00 € entitlement); an older *Rechnungszins* vintage; the monthly frequency loading |
| **4** | **§ 86 case D** — income 20 000 €, two post-2008 children, quarterly | The *Sockelbeitrag* **floor** binding (boundary); a 12,92× subsidy multiple; and a *Kleinbetragsrente* **commutation** at *Rentenbeginn* |
| **5** | ***Mittelbar* eligible spouse** — `contrib_form = fixed`, 60,00 € a year, *Grundzulage* only | The `fixed` contribution form; the economically extreme corner of the book; a second commutation |
| **6** | **Berufseinsteiger** — M, issue age 23 in 2026, attained 24, monthly | The once-in-a-lifetime **200 € bonus** inside `zulage_init_pp`; the longest projection in the table |
| **7** | **Under-payer** — `contrib_ratio = 0.50`, half-yearly | The § 86 **proportional Kürzung**: half the contribution, half the Zulagen |
| **8** | **Two pools** — `contrib_form = fixed` at the ceiling plus `contrib_extra_pp = 900,00 €` | `pool_ungefoerdert_pp`; unsubsidised money entering the **guarantee** while drawing no Zulage |
| **9** | **Rider carve-out at the cap** — `rider_prem_pp = 400,00 €` on a 1 200,00 € contribution | The **20 % cap** on the biometric carve-out binding (boundary) |
| **10** | ***Beitragsfreistellung*** — `bfs_year = 4`, monthly | The book's dominant exit as a state change: guarantee frozen, Zulagen stopped, account rolling, acquisition charge still biting |
| **11** | **Low declared rate on a short deferral** — F, issue age 57 in 2024, in force at duration 3, attained 60, *Rentenbeginn* 67, income 60 000 € so the 2 100 € ceiling binds, `scenario_id = low` (0,50 %) | A **positive *Garantielücke*** at *Rentenbeginn* — the product's signature output. The deferral is seven years rather than seventeen because on the anchor's own term 0,50 % still does not open a gap; that result is reported under *Worked example* as the sensitivity it is |
| **12** | **No lump sum, no guarantee period** — `teilkapital_share = 0`, `rentengarantie_years = 0` | The pure lifelong annuity, and the invariance of `annuity_pp` to the guarantee period |
| **13** | **Late entrant at the statutory floor** — issue age 60 in 2026, *Rentenbeginn* **62**, monthly | The earliest certifiable payout age for a post-2012 contract (boundary); the shortest accumulation and the least guarantee headroom |

**Model point 1 is the worked example's anchor cell** and is `Projection[1]`.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len()` | Last projected period index, `omega_age − age(1) + 1` | once per model point |
| `t_conv()` | The conversion year, `rentenbeginn_age − age(1) + 1` | once |
| `age(t)`, `duration(t)`, `calendar_year(t)` | Attained age, completed contract years, and the calendar year of period `t` | annual |
| `pols_if(t)` | Policies in force at the **start** of period `t`; `pols_if(1) = pols_if_init()` | annual recursion |
| `pols_if_at(t, timing)` | `"BEF_DECR"` = `pols_if(t)`, `"AFT_DECR"` = `pols_if(t+1)` | within year |
| `pols_death(t)`, `pols_lapse(t)`, `pols_transfer(t)` | Expected deaths, surrenders and *Anbieterwechsel* exits in year `t` | annual |
| `pols_conv()`, `pols_annuity_pay(t)` | Policies reaching *Rentenbeginn*; policies on which an annuity instalment is actually paid, which during the *Rentengarantiezeit* is `pols_conv()` rather than `pols_if(t)` | annual |
| `income_ref(t)` | The **previous** calendar year's contribution-liable earnings driving year `t`'s entitlement | annual (lag 1) |
| `zulage_entitlement_pp(t)`, `zulage_granted_pp(t)`, `zulage_pp(t)` | Full § 84/85 entitlement; entitlement after the § 86 proportional Kürzung; the amount actually **credited** in year `t`, which is the previous year's grant | annual (lag 1) |
| `mindesteigenbeitrag_pp(t)`, `eigenbeitrag_pp(t)`, `eigenbeitrag_paid_pp(t)` | The § 86 minimum; the contribution before the frequency loading; the amount actually collected | annual |
| `prem_to_av_pp(t)` | The *Sparbeitrag* — the part of the contribution credited to the account, after charges. **May be negative** in a *beitragsfrei* year | annual |
| `dk_pp(t)`, `surplus_acct_pp(t)`, `av_total_pp(t)` | *Deckungskapital*, *Überschussguthaben*, and their sum at the start of year `t` | annual recursion |
| `av_total_pp_at(t, timing)`, `av_total_at(t, timing)` | `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_INT"`; the second form is the first times `pols_if(t)` | within year |
| `int_guar_pp(t)`, `int_surplus_pp(t)`, `int_credited_pp(t)` | Guaranteed interest at the *Rechnungszins*, declared surplus above it, and their sum | annual |
| `guar_pp(t)`, `guar_carve_out_pp(t)`, `garantieluecke_pp(t)` | The *Beitragsgarantie* accumulator; the biometric carve-out capped at 20 %; the running shortfall `max(0, guar_pp(t) − av_total_pp(t))`, a **diagnostic**, since the guarantee is tested only at *Rentenbeginn* | annual |
| `pool_gefoerdert_pp(t)`, `pool_ungefoerdert_pp(t)` | Cumulative subsidised and unsubsidised contributions credited. **Contributions only** — the model does not apportion investment return between the pools and says so | annual |
| `zulage_cum_pp(t)` | Cumulative Zulagen credited: the ZfA-reclaimable limb of the *Rückzahlungsbetrag*. A diagnostic, never netted from a benefit | annual |
| `capital_conv_pp()`, `garantieluecke_conv_pp()` | Conversion capital and the *Garantielücke* the insurer funds at *Rentenbeginn* — the product's signature output | once, at `t_conv()` |
| `ann_factor()`, `rentenfaktor_curr()`, `rentenfaktor_applied()` | `ä⁽¹²⁾` on the **first-order** annuity basis; the current factor derived from it; the higher of it and `rentenfaktor_guar` | once |
| `is_kleinbetrag()`, `teilkapital_pp()`, `annuity_capital_pp()`, `annuity_pp(t)` | The commutation test and its consequences | once |
| `db_pp(t)`, `cv_pp(t)`, `transfer_value_pp(t)`, `exit_charge_pp(t)` | Death benefit, *Rückkaufswert*, *Anbieterwechsel* transfer value, and the *Stornoabzug* plus transfer charge the insurer retains | annual |

---

## Assumption inputs

Three classes, and the split is not cosmetic: class (a) is what the contract or the statute obliges,
class (b) is what the insurer decides afresh each year, class (c) is the modeller's view. On this
product class (a) is unusually large — most of the product is statute — and class (b) is unusually
consequential, because the declared rate is what decides whether the guarantee costs anything.

### (a) Contractual and guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| *Grundzulage* | **175.00** per year | [R9] [REG-R42] `[unverified]` |
| *Kinderzulage* | **185.00** for a child born before 1 Jan 2008; **300.00** for one born on or after | [R9] [R19] [REG-R42] `[unverified]` |
| *Berufseinsteiger-Bonus* | **200.00**, once in a lifetime, in the first subsidised year | [R9] [REG-R42] `[unverified]` |
| *Mindesteigenbeitrag* rate, ceiling, floor | **4 %** of the previous year's contribution-liable earnings, capped at **2 100.00**, less the entitlement, floored at the **60.00** *Sockelbeitrag* | [R10] [REG-R42] `[unverified]` |
| Proportional Kürzung | The Zulage is reduced in the ratio of the contribution paid to the *Mindesteigenbeitrag* — never lost outright | [R10] [REG-R42] |
| Zulage cash lag | Contribution year `t` is credited by the ZfA in `t + 1` | [R11] [REG-R42]; one-year convention **[std]** (1) |
| *Beitragsgarantie* | At *Rentenbeginn*, at least contributions plus Zulagen credited must be available | [R1] [REG-R43] |
| Guarantee carve-out | Biometric-rider contributions excluded, up to **20 %** of total contributions | [REG-R43] |
| Earliest *Rentenbeginn* | Completed 62nd year for contracts from 1 Jan 2012, 60th before | [R1] [REG-R43] `[unverified]` |
| *Teilkapitalauszahlung* cap | **30 %** of the conversion capital | [R1] [REG-R43] `[unverified]` |
| Acquisition-cost spreading | At least **five years** | [R1] [REG-R43] `[unverified]`; *Höchstzillmersatz* 25 ‰ [REG-R16] |
| *Kleinbetragsrente* threshold | **39.55** per month — 1 % of a 2026 monthly *Bezugsgröße* of 3 955.00. The competing reading is 1,5 % from June 2026, **59.33**; both are printed and one is chosen | [R15] [REG-R42] [REG-R46] `[unverified]`; choice **[std]** (2) |
| *Rückkaufswert* floor | The *Deckungskapital* on five-year cost spreading — satisfied by construction here | [REG-R28] |
| Annuity form | Lifelong, monthly, constant or rising; a falling annuity is not certifiable | [R1] [REG-R43] |
| Unisex | No sex-distinct rate anywhere, including the *Rentenfaktor* | [R23] [REG-R34] |

1. [R11] establishes that the ZfA pays the **provider** and that the application deadline runs to the
   end of the **second** calendar year after the contribution year, but not **when in the following
   year** the money lands, nor how often an entitlement is later reversed (gap 6). One year is the
   shortest lag consistent with the statute and is the convention [REG-R42] itself reports.
2. The two readings cannot both be right [REG-R42]. The model takes the **lower** trigger, so fewer
   contracts commute, more of the book stays a lifelong annuity, and the projected liability is the
   longer-tailed of the two. The threshold is held **flat in nominal terms** at its 2026 value; the
   *Bezugsgröße* is reset annually, so holding it flat **understates** the commutation rate on a
   long deferral, and that direction is stated rather than hidden (sensitivity 7).

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

| Input | Value | Basis |
|---|---|---|
| *Rechnungszins* | **0,25 %** on the anchor, a 2024-vintage tariff; 0,90 % on one older point | cap [R22] [REG-R14] [REG-R15]; carrier's own choice **not established** (gap 12) — **[std]** (3) |
| *Laufende Verzinsung* `decl_rate(t)` | Scenario path in `surplus_scenario.csv`: `base` **2,30 %** level, `low` **0,50 %** level | **[std]** (4) |
| Surplus system in accumulation | *Verzinsliche Ansammlung*: declared surplus accrues in a **second account** beside the *Deckungskapital* and bears the declared rate | market practice; level **[std]** (4) |
| *Risikoüberschuss* and *Kostenüberschuss* | **Zero** in the base run | **[std]** (5) |
| *Schlussüberschussanteil* | **2,0 %** of contributions credited, declared at *Rentenbeginn*, and **counted toward the guarantee** | **[std]** (6), gap 9 |
| *Bewertungsreserven* share | **1,0 %** of the account at *Rentenbeginn*, the *hälftige* participation of § 153 Abs. 3 VVG | [REG-R24]; level **[std]** (6) |
| Acquisition charge | **2,5 %** of `beitragssumme`, in five equal instalments in contract years 1 to 5, **whether or not contributions are paid** | [R1] [REG-R16]; level **[std]** (7) |
| Administration charge | **4,0 %** of each contribution credited, Zulagen **included**, plus a fixed **12,00** per year | **[std]** (7), gap 14 |
| Frequency loading | 1.0000 / 1.0100 / 1.0200 / 1.0300 for annual / half-yearly / quarterly / monthly, treated as a **charge** and never credited to the account | **[std]** (7) |
| *Risikobeitrag* | **Zero** — the death benefit is the account value, so there is no sum at risk | design consequence **[std]** |
| *Stornoabzug*; transfer charge | **2,0 %** of the account on surrender; **50,00** flat on an *Anbieterwechsel*, with **no** *Stornoabzug* | [REG-R28]; [R1] [R20] cap the transfer charge, level not established (gap 8) — **[std]** (7) |
| *Rentenfaktor* margin | **30 %** off the actuarially fair factor, carrying the *Sicherheitsabschlag* and the whole payout-phase loading | **[std]** (8) |
| Annuitisation interest basis | **1,00 %**, the *Höchstrechnungszins* in force from 1 January 2025 | [REG-R15]; use of the cap **[std]** (8) |

3. The *Höchstrechnungszins* caps the **reserving** rate, not the rate a policy guarantees [REG-R14];
   a tariff may guarantee less. Using the cap of the vintage is the highest defensible value and so
   makes the guarantee **cheapest**; a lower tariff rate widens the *Garantielücke*.
4. **No declared rate was established for any Riester tariff at any carrier** (gap 12). 2,30 % is a
   round number in the region German life insurers declared in the mid-2020s [REG-R53]
   `[unverified]`, and 0,50 % is a stress, not a forecast. This is the single most consequential
   **[std]** in the file, because — as the product spec argues — **the guarantee's realised cost is
   a declared-rate question, not a *Rechnungszins* question**, and model point 11 exists to make
   that visible.
5. The accumulation-phase risk result is nil by construction here (no sum at risk), and no cost
   result was established. Setting both to zero keeps the surplus mechanic to the one component the
   corpus does establish, the *Zinsüberschuss*, and states the omission rather than burying it.
6. **Which surplus components may close a guarantee shortfall was not established** (gap 9). The
   model counts all of them, the provider-favourable reading. Counting only the vested
   *Deckungskapital* and *Überschussguthaben* raises the projected guarantee cost, and that variant
   is sensitivity 4.
7. **No charge figure exists anywhere in this corpus** (gap 13); the one inherited datum [S5] is
   third-party commentary on a specimen quotation and is not a tariff sheet. Every level here is a
   round-number placeholder, sized so that the acquisition charge on the anchor is of the same order
   as one year's contribution and so that the total charge load is broadly consistent with the
   *Effektivkosten* a certified product must disclose [R4] [S14].
8. German market *Rentenfaktoren* sit materially below the actuarially fair factor. Rather than
   deduct a percentage from each annuity payment **and** apply a conservative factor, which
   double-counts, the whole loading sits in the factor, and the insurer's real payout-phase
   administration is a per-policy expense cash flow. The consequence to check is that
   `rentenfaktor_curr()` and the annuity table are **consistent by construction**, while
   `rentenfaktor_guar` is an independent contract term — so the model states which is authoritative
   when they disagree: the **higher** applies, which is the German market's own construction and is
   **[std]** here because it was not established for any Riester tariff (gap 9).

### (c) Behavioural and experience assumptions (the modeller's view)

**Every input in this class is [std]. No behavioural rate was established for any German Riester
book, for any year** — no *Stornoquote*, no *Beitragsfreistellung* rate, no transfer-out rate, no
commutation take-up (gap 16). Each rationale below is an argument from the statutory consequences,
not from data.

| Input | Value | Rationale |
|---|---|---|
| Accumulation mortality `mort_table_accum.csv` | **[std]** proxy standing in for **DAV 2008 T** [REG-R48], applied with `mort_be_factor = 0.80` | The DAV tables are proprietary and **not redistributed** [REG-R47]. A death-benefit basis carries **no** improvement projection, because for death cover improvement favours the insurer |
| Annuity mortality `annuity_mort_table.csv` | **[std]** **generational** proxy standing in for **DAV 2004 R** [REG-R49]: `q(x, τ) = qx_base(x) · (1 − improvement(x))^(τ − 2027)`, applied with `annuity_mort_be_factor = 1.15` | The one structural property that is **not optional** is that the basis is two-dimensional in age and calendar year; a period-table proxy understates a twenty-year-deferred annuitisation by a margin that dwarfs every other assumption [REG-R49] |
| Why two factors, in opposite directions | 0.80 on the death basis, 1.15 on the annuity basis | The direction of prudence **forks by product** [REG-R47]: a first-order death table assumes mortality **higher** than expected, a first-order annuity table **lower**. The best estimate therefore sits below the one and above the other |
| Surrender `lapse_rate(t)` | **0,8 %** p.a. at contract durations 1–5, **0,6 %** at 6–10, **0,4 %** from 11 | Materially **below** a Schicht-3 rate, because a *Kündigung* repays all Zulagen and all § 10a relief and taxes the growth [R14] [REG-R42], and because the subsidised capital is protected from execution [R16] [REG-R40] |
| Transfer out `transfer_rate(t)` | **1,2 %** p.a. at durations 1–5, **0,9 %** at 6–10, **0,6 %** from 11 | Set **above** surrender, because the *Wechselrecht* is free of subsidy consequences [R1] and is therefore the rational exit; a model carrying only a lapse rate has mis-specified the book |
| *Beitragsfreistellung* | A **model-point switch** (`bfs_year`), not a decrement | (9) |
| Income growth | **2,0 %** p.a. on the anchor's `income_schedule` path | A round real-plus-inflation number; it decides when the 2 100 € ceiling binds and so the shape of the contribution stream |
| Commutation take-up | **Computed, not assumed** — the model tests the annuity against the threshold | The one behavioural quantity here that does not need a rate |
| *Teilkapitalauszahlung* take-up | **30 %** on the anchor, 0 % on model point 12 | German commentary reports the lump sum as usual `[unverified]`; **gap 10 records that this rests on nothing** |
| Expenses `expense_maint`, `expense_annuity`, `expense_claim`, `expense_acq` | **30.00** p.a. per in-force policy inflating at **2,0 %**; **24.00** p.a. per annuitant; **80.00** per claim; **150.00 + 2,0 %** of `beitragssumme` at issue | No German insurer publishes a unit cost. The per-policy maintenance figure carries the Zulage administration — the *Dauerzulageantrag*, the annual data exchange with the ZfA and the *Leistungsmitteilung* [R11] [R12] — which is a real and product-specific cost |
| Commission | **2,5 %** of `beitragssumme` at issue, **1,5 %** of contributions thereafter | The initial rate is set at the *Höchstzillmersatz* [REG-R16] [REG-R20]. **The cash leaves at issue while the charge is recovered over five years** [R1]; that gap is the new-business strain and it is carried by the insurer |

9. ***Beitragsfreistellung* is the German Riester book's dominant exit** [R25], and the model
   represents it as a **switch on the model point** rather than as a decrement. The reason is
   structural, not laziness: a paid-up policy and a premium-paying one have **different account
   values and different guarantee accumulators** from the moment they diverge, so a
   *Beitragsfreistellung* **rate** would require the projection to carry two account values and two
   guarantee accumulators per model point, and then four, and so on. A scalar single-model-point
   projection cannot do that without doubling every recursion. The honest representation is a
   dedicated model point (10) that goes paid-up in year 4, plus this statement that a real book
   needs a paid-up cohort split. It is listed again under *Key sensitivities*.

---

## Cash flow components and recursions

### Notation, defined once and used throughout

| Symbol | Cells | Meaning |
|---|---|---|
| `t`, `n` | — | Policy year, `1 … n`, `n = proj_len()` |
| `T` | `t_conv()` | The conversion year |
| `x(t)`, `τ(t)`, `d(t)` | `age`, `calendar_year`, `duration` | Attained age, calendar year, completed contract years |
| `l(t)` | `pols_if(t)` | Policies in force at the **start** of year `t`; `l(1) = pols_if_init()` |
| `q(t)`, `w(t)`, `θ(t)` | `mort_rate`, `lapse_rate`, `transfer_rate` | Annual decrement rates in year `t` |
| `Y(t)`, `E(t)` | `income_ref(t)`, `eigenbeitrag_pp(t)` | Reference income; the *Eigenbeitrag* before the frequency loading |
| `M(t)` | `mindesteigenbeitrag_pp(t)` | The § 86 minimum own contribution |
| `Z*(t)`, `Ẑ(t)`, `Z(t)` | `zulage_entitlement_pp`, `zulage_granted_pp`, `zulage_pp` | Full entitlement; entitlement after the Kürzung; the amount **credited** in year `t` |
| `φ` | `prem_freq_load` | Frequency loading, a **charge** and not a credit |
| `C(t)` | `contrib_total_pp(t)` | `E(t) + Z(t) + contrib_extra_pp` while in accumulation |
| `K_a(t)`, `K_v(t)` | `acq_charge_pp`, `admin_charge_pp` | Acquisition and administration charges |
| `S(t)` | `prem_to_av_pp(t)` | The *Sparbeitrag*, `C(t) − K_a(t) − K_v(t)`; **may be negative** |
| `D(t)`, `U(t)`, `A(t)` | `dk_pp`, `surplus_acct_pp`, `av_total_pp` | *Deckungskapital*, *Überschussguthaben*, and `A = D + U` |
| `i`, `j(t)` | `rechnungszins`, `decl_rate(t)` | Guaranteed rate; declared *laufende Verzinsung*, with `j ≥ i` |
| `G(t)`, `κ(t)` | `guar_pp`, `guar_carve_out_pp` | The *Beitragsgarantie* accumulator; the biometric carve-out |
| `Λ` | `garantieluecke_conv_pp()` | The *Garantielücke* funded at *Rentenbeginn* |
| `V` | `capital_conv_pp()` | The conversion capital |
| `ä` | `ann_factor()` | `ä⁽¹²⁾(x(T), τ(T))` on the **first-order** annuity basis at `annuity_rechnungszins` |
| `R`, `R_g`, `R_c` | `rentenfaktor_applied`, `rentenfaktor_guar`, `rentenfaktor_curr` | Applied, guaranteed and current *Rentenfaktor* |
| `a(t)` | `annuity_pp(t)` | The annual annuity, twelve monthly instalments |

### The subsidy chain

    Y(t)   = income_init                       for t = 1
           = income(t − 1) from income_schedule for t ≥ 2

    Z*(t)  = 175·unmittelbar(t) + 185·n_pre(t) + 300·n_post(t) + 200·bonus(t)
    M(t)   = max( 60 , min( 0.04 · Y(t) , 2 100 ) − Z*(t) )
    E(t)   = contrib_ratio · M(t)        (contrib_form = mindest)
           = contrib_fixed_pp            (contrib_form = fixed)
           = 0                           (t ≥ bfs_year > 0, or t ≥ T)
    Ẑ(t)   = Z*(t) · min( 1 , E(t) / M(t) )
    Z(t)   = zulage_init_pp   for t = 1;   Ẑ(t − 1)   for 2 ≤ t ≤ T;   0 for t > T

**Two lags, and they are different lags.** `Y(t)` looks back one calendar year because the statute
says the base is the previous year's earnings [R10]; `Z(t)` looks back one projection year because
the ZfA pays in arrear [R11]. Collapsing them into one is pitfall 1. Note also that `Z(T)` is
**non-zero** — the final contribution year's Zulage lands in the conversion year and must be
credited, guaranteed and converted before the guarantee is tested (pitfall 2).

### Contributions, charges and the *Sparbeitrag*

    B(t)   = E(t) + Z(t) + contrib_extra_pp · 1{is_accum(t)}        charge base, unloaded
    C(t)   = E(t)·φ + Z(t) + contrib_extra_pp · 1{is_accum(t)}      cash actually received
    K_a(t) = acq_charge_rate · beitragssumme / 5      if d(t) ≤ 5 and t ≤ T, else 0
    K_v(t) = admin_charge_prem_rate · B(t) + admin_charge_fixed + E(t)·(φ − 1)
    S(t)   = C(t) − K_a(t) − K_v(t)
           = B(t) − K_a(t) − admin_charge_prem_rate · B(t) − admin_charge_fixed

`E(t)·(φ − 1)` is the frequency loading: the saver pays `E(t)·φ` and only `E(t)` reaches the
*Sparbeitrag* base, so the loading is a charge and never enlarges the account or the guarantee
(pitfall 11). **`C(t)` is the cash received and therefore carries the loading, which `K_v(t)`
then takes straight back out; the administration charge's percentage base `B(t)` is the
unloaded contribution.** The second line above is the algebraic consequence: `S(t)` is
independent of `φ`, which is what pitfall 11 asserts. An earlier draft of these notes wrote
`S = C − K_a − K_v` with an **unloaded** `C` and a `K_v` that already carried `E(φ − 1)`, and so
deducted the loading twice; see *Changes the model stage made to these notes*. `K_a` continues for its five contract years **whether or not contributions are paid**,
so on a *beitragsfrei* contract `S(t)` is negative and the *Deckungskapital* falls — which is the
mechanic model point 10 exists to show. The administration charge falls on the **Zulagen as well as
the *Eigenbeitrag*** [std]; whether German tariffs do that **was not established** (gap 14) and it
is material, because in the low-income cases the Zulagen are the majority of `C(t)`.

### The account: two balances, one credited rate

    D(1) = dk_pp_init,  U(1) = surplus_pp_init,  A(t) = D(t) + U(t)

    int_guar_pp(t)    = i · ( D(t) + S(t) )
    int_surplus_pp(t) = ( j(t) − i ) · ( D(t) + S(t) )  +  j(t) · U(t)
    int_credited_pp(t)= int_guar_pp(t) + int_surplus_pp(t)

    D(t + 1) = ( D(t) + S(t) ) · ( 1 + i )
    U(t + 1) = U(t) + int_surplus_pp(t)
    A(t + 1) = A(t) + S(t) + int_credited_pp(t)

The split is **guarantee accounting, not two investment strategies**: the whole account grows at
`j(t)`, and `D` is carved out of it as the part the *Rechnungszins* guarantees. The German
arithmetic error this prevents is adding the declared *laufende Verzinsung* **to** the
*Rechnungszins*: `j` already **includes** `i`, and `j − i` is the *laufende
Zinsüberschussbeteiligung* [REG-R53] (pitfall 10). Within-year points are
`av_total_pp_at(t, "BEF_PREM") = A(t)`, `av_total_pp_at(t, "AFT_PREM") = A(t) + S(t)` and
`av_total_pp_at(t, "AFT_INT") = A(t + 1)`, with `av_total_at(t, timing) = av_total_pp_at(t, timing) · l(t)`.

### The *Beitragsgarantie* accumulator

    κ(t) = min( rider_prem_pp , 0.20 · ( E(t) + Z(t) + contrib_extra_pp + rider_prem_pp ) )
    G(1) = guar_pp_init
    G(t + 1) = G(t) + E(t) + Z(t) + contrib_extra_pp·1{is_accum(t)} − κ(t)   for t ≤ T
             = G(T + 1)                                                      for t > T

    garantieluecke_pp(t) = max( 0 , G(t) − A(t) )      diagnostic only

Three things this encodes and a test asserts. The accumulator counts **Zulagen credited**, in the
year they are credited, not entitlements in the year they are earned [R1]. It counts
**unsubsidised** contributions too, because the guarantee is on the *Altersvorsorgebeiträge* paid in
and does not distinguish the pools [R1] (pitfall 9). And the biometric carve-out is **capped at
20 % of total contributions** [REG-R43], so raising `rider_prem_pp` beyond the cap does **not**
shrink the guarantee further (pitfall 8). `garantieluecke_pp(t)` is published because it is
positive in the early durations of any charged contract and closes later — a fact about the product
that a reader should see — but it is a diagnostic: **the guarantee is tested once, at `T`**.

### Conversion at *Rentenbeginn*

    account_conv_pp() = D(T) + S(T) + U(T) + slueb_pp() + bewres_pp()
    slueb_pp()        = slueb_rate · ( G(T + 1) − guar_pp_init + contributions credited before t = 1 )
    bewres_pp()       = bewres_rate · ( D(T) + S(T) + U(T) )
    V                 = max( account_conv_pp() , G(T + 1) )
    Λ                 = max( 0 , G(T + 1) − account_conv_pp() )

    ä    = Σ_{k ≥ 0} v^k · k p( x(T), τ(T) )  −  11/24,     v = 1 / (1 + annuity_rechnungszins)
    R_c  = ( 1 − rentenfaktor_margin ) · 10 000 / ( 12 · ä )
    R    = max( R_g , R_c )

    monthly test annuity  = ( 1 − teilkapital_share ) · V / 10 000 · R
    is_kleinbetrag()      = monthly test annuity ≤ kleinbetrag_threshold_mth

    if is_kleinbetrag():  teilkapital_pp() = 0 ; annuity_capital_pp() = 0 ; commutation_pp() = V
    else:                 teilkapital_pp() = teilkapital_share · V ;
                          annuity_capital_pp() = V − teilkapital_pp() ; commutation_pp() = 0

    a(t) = 12 · annuity_capital_pp() / 10 000 · R          for is_payout(t) and not commuted

`k p(x, τ)` is survivorship on the **first-order** annuity basis — the same basis the market's
*Rentenfaktor* is struck on — while the projection's own survivorship uses the **second-order**
basis, `annuity_mort_rate(x, τ) · annuity_mort_be_factor`. The wedge between them is the
*Risikoüberschuss* in payment [REG-R47], which this model does not distribute (assumption class (b),
footnote 5). The commutation test is applied to the annuity **actually payable after the elected
lump sum**, which is a **[std]** reading of a statute that does not settle the point (gap 7); the
alternative — testing the annuity the whole capital would buy — trips less often and is sensitivity
6. If the contract commutes there is **no** *Teilkapitalauszahlung*: the whole capital is one
payment.

### Decrements

    Accumulation (t < T):
      pols_death(t)    = l(t) · q(t)
      pols_lapse(t)    = l(t) · ( 1 − q(t) ) · w(t)
      pols_transfer(t) = l(t) · ( 1 − q(t) ) · ( 1 − w(t) ) · θ(t)
      l(t + 1)         = l(t) − pols_death(t) − pols_lapse(t) − pols_transfer(t)

    Payout (t ≥ T):
      pols_death(t)    = l(t) · q(t) ;  pols_lapse(t) = pols_transfer(t) = 0
      l(t + 1)         = l(t) − pols_death(t)          and 0 at t = T if commuted

    pols_conv()          = l(T)
    pols_annuity_pay(t)  = pols_conv()   if 0 ≤ t − T < rentengarantie_years
                         = l(t)          otherwise

with `q(t) = mort_rate_at_age(x(t)) · mort_be_factor` in accumulation and
`annuity_mort_rate(x(t), τ(t)) · annuity_mort_be_factor` in payout, and `q(t) = 1` at `x = omega_age`
so the closure identity closes exactly. The lapse and transfer decrements are applied **in that
order to the survivors of mortality**, a stated **[std]** ordering. `pols_annuity_pay` is the whole
of the *Rentengarantiezeit*: the guarantee period changes **who is paid**, never **how much**
(pitfall 17).

### Benefits, expenses and the cash flow statement

    db_pp(t)            = A(t + 1)                                    death, gross
    cv_pp(t)            = A(t + 1) · ( 1 − stornoabzug_rate )         surrender, gross
    transfer_value_pp(t)= max( 0 , A(t + 1) − transfer_charge )       Anbieterwechsel
    exit_charge_pp(t)   = stornoabzug_rate · A(t + 1) · pols_lapse(t)
                          + min( transfer_charge, A(t + 1) ) · pols_transfer(t)

    claims(t, "DEATH")       = db_pp(t) · pols_death(t)
    claims(t, "LAPSE")       = cv_pp(t) · pols_lapse(t)
    claims(t, "TRANSFER")    = transfer_value_pp(t) · pols_transfer(t)
    claims(t, "LUMPSUM")     = teilkapital_pp() · pols_conv()        at t = T only
    claims(t, "COMMUTATION") = commutation_pp() · pols_conv()        at t = T only
    claims(t, "ANNUITY")     = a(t) · pols_annuity_pay(t)

    premiums(t)   = ( E(t)·φ + contrib_extra_pp·1{is_accum(t)} ) · l(t)
    zulagen(t)    = Z(t) · l(t)
    expenses(t)   = expense_acq · 1{t = 1 and duration_init = 0}
                    + expense_maint · (1 + expense_infl)^(d(t) − 1) · l(t) · 1{is_accum(t)}
                    + expense_annuity · pols_annuity_pay(t)
                    + expense_claim · ( pols_death(t) + pols_lapse(t) + pols_transfer(t) )
    commissions(t)= comm_rate_init · beitragssumme · l(1) · 1{t = 1 and duration_init = 0}
                    + comm_rate_renew · ( E(t) + Z(t) ) · l(t)   otherwise, while is_accum(t)

    net_cf(t)     = premiums(t) + zulagen(t)
                    − claims_death(t) − claims_lapse(t) − claims_transfer(t)
                    − claims_lumpsum(t) − claims_commutation(t) − claims_annuity(t)
                    − expenses(t) − commissions(t)
    liability_cf(t) = − net_cf(t)

**Death and surrender benefits are published gross of the *Rückzahlungsbetrag***: the provider
withholds all Zulagen and all § 10a relief and remits them to the ZfA [R14], but that is a **tax
collection, not a reduction in the insurer's obligation**, and netting it would understate the outgo
(pitfall 18). `zulage_cum_pp(t)` publishes the reclaimable Zulage limb as a diagnostic; the § 10a
limb depends on the saver's marginal rate and cannot be computed from contract data at all.

**`result_cf()` returns a `DataFrame` indexed by `t` (`df.index.name == "t"`), contiguous, ending at
`proj_len()`, with these columns in this order:**

    pols_if, pols_annuity_pay, premiums, zulagen, int_credited,
    claims_death, claims_lapse, claims_transfer, claims_lumpsum, claims_commutation,
    claims_annuity, expenses, commissions, net_cf, liability_cf

`int_credited` is a **state movement, reported and not summed into `net_cf`** — money moving inside
the account, not across the insurer's boundary. The separation of `zulagen` from `premiums` is the
single most important reporting decision in this model: **the Zulage is a contribution with a
different payer** [R8], and a statement that folds it into `premiums` cannot answer the one question
the product is about.

### The check identities the model publishes

| Check | Identity |
|---|---|
| **`check_net_cf()`** (delib ruling 1) | On `result_cf()` row `t`: `net_cf` equals `premiums + zulagen` less the six `claims_*` less `expenses` less `commissions`, every term read from the **published frame** rather than from the cells behind it, for every `t`; residual at `check_net_cf_resid(t)`. `int_credited` is outside the identity |
| `check_av_roll_fwd()` | `av_total_at(t+1, "BEF_PREM") = av_total_at(t, "BEF_PREM") + prem_to_av_pp(t)·l(t) + int_credited(t) − claims_death − claims_lapse − claims_transfer − exit_charge(t)` for `t < t_conv()`, and `av_total_pp(t) = 0` for `t > t_conv()` |
| `check_guar_roll_fwd()` | `guar_pp(t+1) = guar_pp(t) + eigenbeitrag_pp(t) + zulage_pp(t) + contrib_extra_pp − guar_carve_out_pp(t)` while `t ≤ t_conv()`, frozen thereafter, and `guar_carve_out_pp(t) ≤ 0.20 ×` total contributions |
| `check_pols_roll_fwd()` | The decrement recursion closes each year, and `Σ(pols_death + pols_lapse + pols_transfer) + pols_conv()·1{is_kleinbetrag()} + pols_if(proj_len()+1) = pols_if_init()`. The commuted cohort is a fourth exit: a *Kleinbetragsrenten-Abfindung* discharges the contract, so `pols_if(t_conv()+1) = 0` without any decrement having removed the population |
| `check_conversion()` | `capital_conv_pp() = max(account_conv_pp(), guar_pp(t_conv()+1))`; `capital_conv_pp() = teilkapital_pp() + annuity_capital_pp() + commutation_pp()`; and `rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000`, the identity that ties the current factor to the annuity basis whether or not it is the factor applied |
| `check_zulage_lag()` | `zulage_pp(1) = zulage_init_pp`, `zulage_pp(t) = zulage_granted_pp(t−1)` for `2 ≤ t ≤ t_conv()`, and `zulage_pp(t) = 0` thereafter |

Each returns a **`bool`** over all `t` and has a `check_*_resid(t)` companion, and the conventions
suite calls all six on **every** model point.

---

## Annual processing order

For `t = 1 … proj_len()`, in this order. The order is a **[std]** decision — no source in this
corpus fixes the ordering of premium credit, charge deduction and interest accrual inside a period —
and it is stated here so that an implementation can be compared against it line by line.

1. Set `x(t)`, `d(t)`, `τ(t)`. Decide `is_accum(t)` / `is_payout(t)` from `t_conv()`.
2. **Accumulation only.** Read `Y(t)` — `income_init` at `t = 1`, otherwise the schedule's
   `income(t − 1)`. Compute the entitlement `Z*(t)` from the Zulage schedule and the statutory
   rates, then `M(t)`, then `E(t)` from the contribution form, `bfs_year` and `contrib_ratio`, then
   the granted entitlement `Ẑ(t)`.
3. **Credit the Zulage earned last year**: `Z(t) = zulage_init_pp` at `t = 1`, else `Ẑ(t − 1)`. This
   happens **before** anything else touches the account, and it happens in the conversion year too.
4. Form `C(t)`, deduct `K_a(t)` and `K_v(t)`, and credit the *Sparbeitrag* `S(t)` to the account:
   `av_total_pp_at(t, "AFT_PREM") = A(t) + S(t)`. Collect `premiums(t)` and `zulagen(t)` on `l(t)`.
5. Roll the guarantee accumulator: `G(t + 1) = G(t) + E(t) + Z(t) + contrib_extra_pp − κ(t)`, and
   the two contribution pools alongside it.
6. Charge start-of-year expenses and commission on the in-force, plus the acquisition expense and
   initial commission at `t = 1` on a point issued at the valuation date.
7. **If `t = t_conv()`**: strike `account_conv_pp()`, `V`, `Λ`; compute `ä`, `R_c`, `R`; apply the
   *Kleinbetragsrente* test; pay `claims_lumpsum` or `claims_commutation` on `pols_conv()`; and fix
   the annuity `a(t)`. The account is extinguished — `av_total_pp(t) = 0` for `t > t_conv()`. **Nothing in
   steps 8 and 9 applies to the account after this point.**
8. **Accumulation only, end of year.** Credit interest: `int_guar_pp(t)` at `i` and
   `int_surplus_pp(t)` at `j(t) − i` on `D(t) + S(t)`, plus `j(t)` on `U(t)`;
   `av_total_pp_at(t, "AFT_INT") = A(t + 1)`.
9. **Accumulation only, end of year.** Apply the decrements to `l(t)`: mortality first, then
   surrender on the survivors, then transfer on the survivors of both. Strike `claims_death`,
   `claims_lapse` and `claims_transfer` on `A(t + 1)`, and retain `exit_charge_pp(t)`.
10. **Payout only.** Pay `claims_annuity(t) = a(t) · pols_annuity_pay(t)` at the **start** of the
    year, charge `expense_annuity` on the same count, then apply annuitant mortality at the end of
    the year: `l(t + 1) = l(t) · (1 − q(t))`.
11. Assemble `expenses(t)`, `commissions(t)`, `net_cf(t)` and `liability_cf(t)`.

At `t = proj_len()` the projection ends with `q = 1`, so `l(proj_len() + 1) = 0` and the closure
identity is exact.

---

## Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is wrong. Each one
becomes a test in `tests/test_riester_rente_de.py`.

1. **Collapsing the two subsidy lags into one.** The entitlement looks back one **calendar** year
   for income [R10]; the cash arrives one **projection** year late [R11]. Assert
   `income_ref(1) = income_init`, `income_ref(t) = income_schedule[t − 1]`, and
   `zulage_pp(t) = zulage_granted_pp(t − 1)` — two distinct offsets, not one applied twice.
2. **Dropping the final contribution year's Zulage.** Contributions stop at `t_conv() − 1`; the
   Zulage they earned is credited at `t_conv()`. Assert `zulage_pp(t_conv()) > 0` on the anchor,
   that it enters `guar_pp(t_conv() + 1)`, and that it is inside `account_conv_pp()`. Stopping the
   Zulage with the contribution silently removes a full year's subsidy from both.
3. **Treating the *Mindesteigenbeitrag* as a cliff.** § 86 reduces the Zulage **in proportion** to
   the shortfall [R10] [REG-R42]. Assert on model point 7 that `contrib_ratio = 0.50` gives exactly
   `0.50 × zulage_entitlement_pp(t)` — not zero, and not the full amount.
4. **Treating the Zulage as a benefit, or netting it against the contribution.** It is a
   **contribution paid by the ZfA to the provider** [R8] [R11]. Assert `zulagen(t) > 0` as a
   separate positive column, that it never appears with a negative sign, and that
   `premiums(t)` excludes it.
5. **Modelling the *Günstigerprüfung* top-up as a contract cash flow.** Only the Zulage reaches the
   policy; the § 10a advantage is a personal tax refund [R6] [REG-R42]. Assert that no cells and no
   column corresponds to it.
6. **Using a single *Kinderzulage* rate.** The 185 € / 300 € split is a permanent **birth-cohort**
   rule, not a transition [R9] [R19]. Assert on model point 3 that both rates run **simultaneously**
   in years 1 and 2, giving `zulage_entitlement_pp = 175 + 185 + 300 = 660,00 €`.
7. **Testing the *Beitragsgarantie* anywhere but at *Rentenbeginn*.** It is tested **once** [R1].
   Assert that `db_pp(t)`, `cv_pp(t)` and `transfer_value_pp(t)` are **not** floored at `guar_pp`,
   and that the anchor has `garantieluecke_pp(1) > 0` — an account below the contributions paid —
   without that affecting any benefit.
8. **Enlarging the guarantee with a rider premium, or forgetting the 20 % cap.** Assert on model
   point 9 that `guar_carve_out_pp(t) = 0.20 × (E + Z + extra + rider)` and is **strictly less
   than** `rider_prem_pp = 400,00 €`, and that raising `rider_prem_pp` further does not reduce
   `guar_pp` further.
9. **Excluding unsubsidised contributions from the guarantee.** The guarantee is on the
   *Altersvorsorgebeiträge* paid in and does not distinguish the pools [R1]. Assert on model
   point 8 that `guar_pp(t + 1) − guar_pp(t)` includes `contrib_extra_pp`, while
   `zulage_entitlement_pp(t)` is unaffected by it.
10. **Adding the declared rate to the guaranteed rate.** `decl_rate` **includes** the
    *Rechnungszins* [REG-R53]. Assert `int_credited_pp(t) = j(t) · (D(t) + S(t)) + j(t) · U(t)`
    exactly, and that setting `j = i` makes `int_surplus_pp(t)` zero on the *Deckungskapital* leg.
11. **Crediting the frequency loading to the account.** The *Ratenzuschlag* is a charge. Assert that
    on model point 3 (monthly) `premiums(t)` exceeds the annual-mode amount by exactly
    `E(t) · 0.03` while `prem_to_av_pp(t)`, `guar_pp(t)` and every benefit are **unchanged**.
12. **Charging acquisition costs in one year, or stopping them on *Beitragsfreistellung*.** The
    AltZertG requires spreading over at least five years [R1]. Assert `acq_charge_pp(t)` is equal in
    contract years 1 to 5 and zero afterwards, and on model point 10 that it **continues** after
    `bfs_year`, driving `prem_to_av_pp(t)` negative.
13. **Collapsing *Anbieterwechsel* into surrender.** A transfer is a full-value exit with **no**
    *Stornoabzug* [R1]. Assert `transfer_value_pp(t) = A(t + 1) − 50,00 €` while
    `cv_pp(t) = 0.98 · A(t + 1)`, and that the two decrements are separate columns.
14. **Treating *Beitragsfreistellung* as a termination.** It is a state change [R14] [REG-R28].
    Assert on model point 10 that `pols_if(t)` is **continuous** across `bfs_year`, that `guar_pp`
    freezes, that `zulage_pp` goes to zero, and that `av_total_pp` keeps rolling.
15. **Using one mortality table for both phases, or a period table for the annuity.** The direction
    of prudence forks by product [REG-R47], and DAV 2004 R is generational [REG-R49]. Assert that
    `mort_rate(t)` switches basis at `t_conv()`, that `annuity_mort_rate(x, τ)` depends on **both**
    arguments, and that `annuity_mort_rate(x, τ + 1) < annuity_mort_rate(x, τ)`.
16. **Testing the *Kleinbetragsrente* on the wrong annuity, or hiding the flat threshold.** The test
    is applied after the elected lump sum **[std]**, and the threshold is held flat in nominal terms
    **[std]**. Assert both explicitly, assert that model points 4 and 5 commute while the anchor does
    not, and that a commuted point pays `claims_commutation` and **no** `claims_lumpsum` and **no**
    `claims_annuity`.
17. **Applying the *Rentengarantiezeit* to the annuity amount.** The guarantee period changes the
    **payment count**, never the payment. Assert `pols_annuity_pay(t) = pols_conv()` for
    `t − t_conv() < rentengarantie_years` and `= pols_if(t)` afterwards, and that `annuity_pp(t)` is
    invariant to `rentengarantie_years` — model point 12, at zero, must pay the **same annuity** to
    a smaller count.
18. **Netting the *Rückzahlungsbetrag* out of a benefit.** It is a tax collection the provider
    withholds and remits [R14]. Assert `claims_death(t) = A(t + 1) · pols_death(t)` gross, that
    `zulage_cum_pp(t)` is published and never subtracted from a claim, and that no cells attempts a
    § 10a repayment, which contract data cannot support.

---

## Policyholder behaviour modelling

Every formula here is **[std]**; there is no German Riester calibration evidence for any of them
(gap 16), and each rests on an argument from the statutory consequences.

- **Surrender is deliberately small and flat-ish.** 0,8 % / 0,6 % / 0,4 % by duration band. A
  *Kündigung* repays **all** Zulagen and **all** § 10a relief and taxes the accumulated growth on
  the subsidised part [R14] [REG-R42], against a surrender value that is already below the
  contributions paid in the early years. The German market's own description is that a Riester
  contract is effectively unsurrenderable in economic terms, and the assumption says so numerically.
- **Transfer out is set above surrender.** 1,2 % / 0,9 % / 0,6 %. The *Wechselrecht* is free of
  subsidy consequences [R1], so it dominates surrender for any saver who wants out but not out of
  the system. **A model carrying only a lapse rate has mis-specified this book**, and the ordering
  `transfer_rate > lapse_rate` at every duration is itself an assertion worth making.
- **No dynamic behaviour is modelled, and the omission is deliberate.** There is no rate-driven
  surrender function, because there is nothing to arbitrage into: the subsidy, not the credited
  rate, is what holds the contract. There is no *Teilkapitalauszahlung* take-up model, because the
  decision is a tax comparison the model does not perform — the lump sum is taxed **in full in its
  year with no *Fünftelregelung*** [R12] [R15] — and a fixed take-up rate standing in for a tax
  calculation should be labelled as such rather than dressed up.
- **What is computed rather than assumed.** The *Kleinbetragsrente* commutation. The model tests the
  annuity it has actually produced against the statutory threshold, so the commutation rate on a
  book is an **output**, not an input. Given how much of the German Riester book runs at the
  *Sockelbeitrag*, that is the right way round.
- **What a real book needs and this model does not have.** A *Beitragsfreistellung* **decrement**
  moving policies from a premium-paying to a paid-up cohort, each with its own account value and
  guarantee accumulator (assumption class (c), footnote 9). Model point 10 shows the mechanic on one
  policy; a book-level projection needs the split.

---

## Worked example

**Configuration.** Model point 1, the anchor: an in-force *klassische Riester-Rentenversicherung* at
the **1 January 2027** valuation date. `point_id = 1`; `sex = F` (reporting only — the tariff and the
conversion are unisex [R23]); `issue_age = 47`, the contract having been concluded on 1 January
**2024**; `duration_init = 3`, so `age(1) = 50`, `duration(1) = 4` and `calendar_year(1) = 2027`;
`pols_if_init = 1.0`; `rentenbeginn_age = 67`; `rechnungszins = 0.0025`, the *Höchstrechnungszins* of
the 2024 vintage [R22] [REG-R15]; `beitragssumme = 33,600.00`; `contrib_form = mindest` with
`contrib_fixed_pp = 0.00`; `contrib_ratio = 1.00`, the full *Mindesteigenbeitrag* paid;
`contrib_extra_pp = 0.00`, so the two contribution pools coincide; `rider_prem_pp = 0.00`, so the
guarantee carries no carve-out; `income_id = grow2` and `income_init = 42,000.00`;
`zulage_id = k1_2010`, a household with **one child born in 2010** drawing *Kindergeld* to 2028, so
the entitlement is 475,00 € in contribution years 2027 and 2028 and 175,00 € thereafter;
`zulage_init_pp = 475.00`, the Zulage earned in 2026 and credited in projection year 1;
`prem_freq = annual`, so `prem_freq_load = 1.0000`; `bfs_year = 0`; `dk_pp_init = 3,860.50`;
`surplus_pp_init = 150.48`, so `av_total_pp(1) = 4,010.98`; `guar_pp_init = 4,369.92` — three
*Eigenbeiträge* on the same income path plus the two Zulagen of 475,00 € credited in 2025 and 2026 —
which is **above** the account, so the anchor opens with a positive `garantieluecke_pp(1)` of
358,94 €;
`teilkapital_share = 0.30`, the statutory maximum lump sum; `rentenfaktor_guar = 29.00`;
`rentengarantie_years = 10`; and `scenario_id = base`. Hence `t_conv() = 67 − 50 + 1 = 18`, so
accumulation runs `t = 1 … 17` (attained ages 50 to 66, calendar 2027 to 2043), conversion falls at
`t = 18` (age 67, calendar 2044), the payout phase runs `t = 18 … 61`, and
`proj_len() = 110 − 50 + 1 = 61`. The opening balances are **[std]** seeds produced by the same
charge basis over contract years 2024 to 2026. **Model point 2 is this contract projected from its
own inception. It reconciles the two account seeds to the cent — `dk_pp_init` to 3 860,499285 €
and `surplus_pp_init` to 150,483132 € — and from its own `t = 4` onward reproduces every
per-policy quantity of the anchor's `t = 1` onward exactly; it does *not* reconcile
`guar_pp_init`, because the two seeds were struck on different income paths.** The discrepancy is
195,08 € and is set out in full under *Changes the model stage made to these notes*.

**Assumptions, each tagged.** *Grundzulage* **175,00 €**, *Kinderzulage* **300,00 €** for the child
born in 2010, no *Berufseinsteiger-Bonus* — all [R9] [REG-R42] `[unverified]`. *Mindesteigenbeitrag*
**4 %** of the previous calendar year's contribution-liable earnings, capped at **2 100,00 €**, less
the entitlement, floored at the **60,00 €** *Sockelbeitrag*, with the Kürzung proportional — [R10]
[REG-R42] `[unverified]`. Zulage cash lag **one year** [R11] [REG-R42], the one-year convention
**[std]**. Income path **2,0 %** p.a. from `income_init = 42 000,00 €` **[std]**, so the 2 100 €
ceiling first binds in projection year 13. *Rechnungszins* **0,25 %** [R22] [REG-R15], the carrier's
own choice **[std]**. *Laufende Verzinsung* **2,30 %** level on the `base` scenario **[std]**, so
`int_surplus_pp` runs at **2,05 %** above the guaranteed leg. Acquisition charge **2,5 %** of the
33 600,00 € *Beitragssumme* — 840,00 €, in five equal instalments of **168,00 €** in contract years
1 to 5, so projection years 1 and 2 carry it and years 3 onward do not — [R1] [REG-R16], level
**[std]**. Administration charge **4,0 %** of each contribution credited, Zulagen **included**
`[std]` (gap 14), plus a fixed **12,00 €** a year **[std]**. Frequency loading **1.0000** (annual)
**[std]**. *Risikobeitrag* **zero**, the death benefit being the account value. *Schlussüberschuss*
**2,0 %** of contributions credited and *Bewertungsreserven* share **1,0 %** of the account, both at
*Rentenbeginn*, both counted toward the guarantee — [REG-R24], levels and the counting convention
**[std]** (gap 9). Accumulation mortality: the shipped **[std]** proxy for **DAV 2008 T** [REG-R48]
at `mort_be_factor = 0.80`. Annuity mortality: the shipped **[std]** **generational** proxy for
**DAV 2004 R** [REG-R49], `q(x, τ) = qx_base(x) · (1 − improvement(x))^(τ − 2027)`, at
`annuity_mort_be_factor = 1.15` for the projection and at **1.00** — the first-order basis — inside
`ann_factor()`. Annuitisation interest **1,00 %** [REG-R15] **[std]**, with the Woolhouse
`−11/24` correction **[std]**; *Rentenfaktor* margin **30 %** **[std]**; guaranteed *Rentenfaktor*
**29,00 €** per 10 000 € per month **[std]** (gap 9). *Kleinbetragsrente* threshold **39,55 €** per
month **[std]** [REG-R42] [REG-R46], the competing 59,33 € reading printed and not used. Surrender
**0,8 % / 0,6 % / 0,4 %** and transfer out **1,2 % / 0,9 % / 0,6 %** by duration band, both
**[std]**; *Stornoabzug* **2,0 %** [REG-R28] **[std]**; transfer charge **50,00 €** **[std]**
(gap 8). Expenses **[std]**: maintenance 30,00 € per in-force policy per year inflating at **2,0 %**,
annuity administration 24,00 € per annuitant per year, claim expense 80,00 € per death, surrender or
transfer; no acquisition expense and no initial commission, because `duration_init = 3` puts them in
the past. Renewal commission **1,5 %** of the contributions credited **[std]**. `omega_age = 110`
**[std]**, with `q = 1` at that age so the decrements close exactly.

All amounts in euros; `pols_if` and `pols_annuity_pay` to six decimals, cash flows to the cent.
Totals are summed at **full precision and then rounded**, not summed from rounded cells.

### The cash flow statement — `Projection[1].result_cf()`, accumulation and conversion

Transcribed from the model's own output. `claims_commutation` is **0.00** at every `t` on this
cell — the anchor's annuity clears the *Kleinbetragsrente* threshold — and is omitted for space;
it is a required column of `result_cf()`. `liability_cf` is omitted for the same reason: it is
`−net_cf` exactly. `pols_annuity_pay` is zero throughout the accumulation and is carried in the
payout table below.

| t | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_lumpsum | claims_annuity | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 1,205.00 | 475.00 | 125.21 | 6.68 | 43.61 | 65.62 | 0.00 | 0.00 | 33.52 | 25.20 | 1,505.37 |
| 2 | 0.978920 | 1,212.49 | 464.99 | 158.37 | 9.30 | 55.15 | 83.16 | 0.00 | 0.00 | 33.45 | 25.16 | 1,471.25 |
| 3 | 0.958169 | 1,507.08 | 455.13 | 201.64 | 13.02 | 52.66 | 79.69 | 0.00 | 0.00 | 32.99 | 29.43 | 1,754.41 |
| 4 | 0.942478 | 1,515.34 | 164.93 | 239.74 | 17.03 | 62.60 | 94.82 | 0.00 | 0.00 | 33.09 | 25.20 | 1,447.53 |
| 5 | 0.926909 | 1,523.36 | 162.21 | 278.17 | 21.74 | 72.62 | 110.07 | 0.00 | 0.00 | 33.18 | 25.28 | 1,422.67 |
| 6 | 0.911451 | 1,531.11 | 159.50 | 316.90 | 27.24 | 82.72 | 125.44 | 0.00 | 0.00 | 33.27 | 25.36 | 1,396.58 |
| 7 | 0.896093 | 1,538.55 | 156.82 | 355.91 | 33.65 | 92.88 | 140.92 | 0.00 | 0.00 | 33.35 | 25.43 | 1,369.13 |
| 8 | 0.880824 | 1,545.66 | 154.14 | 395.18 | 41.10 | 68.74 | 104.53 | 0.00 | 0.00 | 33.08 | 25.50 | 1,426.86 |
| 9 | 0.869997 | 1,560.24 | 152.25 | 436.87 | 49.98 | 75.97 | 115.56 | 0.00 | 0.00 | 33.32 | 25.69 | 1,411.96 |
| 10 | 0.859103 | 1,574.53 | 150.34 | 479.17 | 60.30 | 83.31 | 126.75 | 0.00 | 0.00 | 33.56 | 25.87 | 1,395.07 |
| 11 | 0.848126 | 1,588.46 | 148.42 | 522.04 | 72.27 | 90.74 | 138.08 | 0.00 | 0.00 | 33.80 | 26.05 | 1,375.95 |
| 12 | 0.837051 | 1,602.01 | 146.48 | 565.45 | 86.11 | 98.25 | 149.53 | 0.00 | 0.00 | 34.03 | 26.23 | 1,354.34 |
| 13 | 0.825864 | 1,589.79 | 144.53 | 608.79 | 101.98 | 105.75 | 160.96 | 0.00 | 0.00 | 34.25 | 26.01 | 1,305.36 |
| 14 | 0.814546 | 1,568.00 | 142.55 | 651.80 | 120.10 | 113.17 | 172.29 | 0.00 | 0.00 | 34.46 | 25.66 | 1,244.86 |
| 15 | 0.803079 | 1,545.93 | 140.54 | 694.42 | 140.75 | 120.52 | 183.50 | 0.00 | 0.00 | 34.67 | 25.30 | 1,181.73 |
| 16 | 0.791444 | 1,523.53 | 138.50 | 736.58 | 164.23 | 127.78 | 194.57 | 0.00 | 0.00 | 34.86 | 24.93 | 1,115.67 |
| 17 | 0.779621 | 1,500.77 | 136.43 | 778.20 | 190.86 | 134.94 | 205.48 | 0.00 | 0.00 | 35.04 | 24.56 | 1,046.34 |
| 18 | 0.767588 | 0.00 | 134.33 | 0.00 | 0.00 | 0.00 | 0.00 | 10,536.61 | 855.57 | 18.81 | 0.00 | −11,276.67 |
| **Total, t = 1 … 61** | | **25,631.84** | **3,627.10** | **7,544.45** | **1,156.35** | **1,481.42** | **2,250.97** | **10,536.61** | **20,154.82** | **1,069.29** | **436.87** | **−7,827.39** |

**The Total row covers all sixty-one periods, not only the eighteen displayed**, and is summed
**at full precision and then rounded**. Nine of its eleven columns differ from the sum of the
already-rounded cells: `premiums` 25 631,84 € against 25 631,85 €, `zulagen` 3 627,10 € against
3 627,09 €, `int_credited` 7 544,45 € against 7 544,44 €, `claims_death` 1 156,35 € against
1 156,34 €, `claims_lapse` 1 481,42 € against 1 481,41 €, `claims_annuity` 20 154,82 € against
20 154,83 €, `expenses` 1 069,29 € against 1 069,32 €, `commissions` 436,87 € against 436,86 €,
and `net_cf` −7 827,39 € against −7 827,43 €, a four-cent accumulation over sixty-one rows.
Only `claims_transfer` and `claims_lumpsum` agree. **Assert the full-precision totals.**

Four things to read off before the checks. **`zulagen` steps down between `t = 3` and `t = 4`**,
455,13 € to 164,93 €, while `premiums` *rises*: *Kindergeld* for the child born in 2010 stops
after the 2028 contribution year, so the entitlement falls at `t = 3` and the credit follows one
year later at `t = 4`, while the *Eigenbeitrag* jumps at `t = 3` because the § 86 minimum is 4 %
of income **less the entitlement** — a Zulage that stops is a contribution the saver must make
good. Two lags, two offsets, one table: pitfall 1. **The acquisition charge stops after `t = 2`**,
contract year 5; it never appears in the frame, being a deduction before the account, but
168,00 € of the 488,90 € rise in the *Sparbeitrag* between `t = 2` and `t = 3` is the charge
ending rather than the contribution rising, and it is why `garantieluecke_pp(t)` peaks at
**567,69 €** at `t = 3` and reaches zero at `t = 7`. **`claims_transfer` exceeds `claims_lapse`
at every `t` by about half again**, because the *Anbieterwechsel* rate is set above the surrender
rate at every duration and a transfer pays the full account less a flat 50,00 € against a
surrender's 98 %; both fall at `t = 8`, where contract duration passes 10 and the bands step
down. And **`net_cf` is positive in every accumulation year** before −11 276,67 € in the
conversion year: an in-force Riester cell is a positive cash flow to the insurer for as long as
it accumulates, and the whole liability is the conversion year and the annuity tail.

### The payout phase — selected rows, `t = 18 … 61`

`premiums`, `int_credited`, `claims_death`, `claims_lapse` and `claims_transfer` are **0.00 at
every `t` from 18 onward**: the account is extinguished at conversion, so there is no interest to
credit and a death pays nothing outside the *Rentengarantiezeit*. `zulagen` is 134,33 € at
`t = 18` — the final contribution year's subsidy, landing in the conversion year — and zero
thereafter.

| t | age | pols_if | pols_annuity_pay | claims_annuity | expenses | net_cf |
|---|---|---|---|---|---|---|
| 18 | 67 | 0.767588 | 0.767588 | 855.57 | 18.81 | −11,276.67 |
| 19 | 68 | 0.762677 | 0.767588 | 855.57 | 18.85 | −874.43 |
| 27 | 76 | 0.701403 | 0.767588 | 855.57 | 19.33 | −874.91 |
| 28 | 77 | 0.690013 | 0.690013 | 769.11 | 17.56 | −786.67 |
| 29 | 78 | 0.677530 | 0.677530 | 755.19 | 17.35 | −772.55 |
| 35 | 84 | 0.574463 | 0.574463 | 640.31 | 15.60 | −655.91 |
| 45 | 94 | 0.273819 | 0.273819 | 305.21 | 9.43 | −314.63 |
| 55 | 104 | 0.016013 | 0.016013 | 17.85 | 0.94 | −18.79 |
| 61 | 110 | 0.000079 | 0.000079 | 0.09 | 0.01 | −0.10 |
| **Subtotal, t = 19 … 61** | | **17.024474** | **17.314559** | **19,299.25** | **476.56** | **−19,775.81** |

The *Rentengarantiezeit* is the whole of the difference between the two count columns. From
`t = 18` to `t = 27` — ten years from *Rentenbeginn* — `pols_annuity_pay` is frozen at
`pols_conv() = 0.767588` while `pols_if` decays to 0.701403, so `claims_annuity` is **exactly
855,57 € in each of those ten years** although a tenth of the annuitants have died; at `t = 28`
the columns join and the outgo falls with the survivors. `annuity_pp(t)` is **1 114,625493 € in
every payout year**, guarantee period or not — the guarantee changes who is paid, never how much
(pitfall 17) — and the subtotals say the same in aggregate: 17.314559 instalments paid against
17.024474 policy-years in force.

### Independent checks

*Projection year 1 rebuilt from the statute up, in one pass.* The reference income is the
previous calendar year's, so `Y(1) = income_init = 42 000,00 €`. The entitlement is the
*Grundzulage* plus one post-2008 *Kinderzulage*, `Z*(1) = 175,00 + 300,00 = 475,00 €`. The § 86
minimum is `max(60, min(0,04 × 42 000, 2 100) − 475) = max(60, 1 680 − 475) = 1 205,00 €`, and
`contrib_ratio = 1.00` pays it in full, so `E(1) = 1 205,00 €`; the frequency is annual, so
`φ = 1` and `premiums(1) = 1 205,00 €`. The Zulage **credited** in year 1 is the one earned in
2026, `zulage_init_pp = 475,00 €`, so `zulagen(1) = 475,00 €`. Charges:
`K_a = 0,025 × 33 600 / 5 = 168,00 €` (contract year 4, inside the five-year window),
`K_v = 0,04 × 1 680,00 + 12,00 = 79,20 €`, so `S(1) = 1 680,00 − 168,00 − 79,20 = 1 432,80 €`.
Interest at the declared 2,30 % on the *Deckungskapital* plus the *Sparbeitrag* plus the
*Überschussguthaben*: `0,023 × (3 860,50 + 1 432,80 + 150,48) = 0,023 × 5 443,78 = 125,206940 €`,
the table's 125,21 €, and `A(2) = 5 568,986940 €`. Decrements at attained age 50, contract
duration 4: `q = 0,001500 × 1,10⁰ × 0,80 = 0,001200`, `w = 0,008`, `θ = 0,012`, applied in that
order, so `pols_death = 0,001200`, `pols_lapse = 0,9988 × 0,008 = 0,0079904` and
`pols_transfer = 0,9988 × 0,992 × 0,012 = 0,0118897152`. Benefits struck on `A(2)`:
`claims_death = 5 568,986940 × 0,001200 = 6,682784 €`;
`claims_lapse = 0,98 × 5 568,986940 × 0,0079904 = 5 457,607201 × 0,0079904 = 43,608465 €`;
`claims_transfer = (5 568,986940 − 50,00) × 0,0118897152 = 65,619183 €`. Expenses:
`30,00 × 1,02³ = 31,836240 €` of maintenance, inflated on **contract** duration and not on
projection year, plus `80,00 × (0,001200 + 0,0079904 + 0,0118897152) = 1,686409 €` of claim
expense — 33,52 €. Commission `0,015 × (1 205,00 + 475,00) = 25,20 €`. And
`1 680,00 − 6,682784 − 43,608465 − 65,619183 − 33,522649 − 25,200000 = 1 505,366919 €`, the
table's `net_cf(1) = 1 505,37 €`.

*The conversion year rebuilt a different way.* At `t = 18` the *Deckungskapital* is
36 172,815098 €, the *Überschussguthaben* 8 224,490372 €, and the *Sparbeitrag* is the last
Zulage net of its charge, `175,00 − (0,04 × 175,00 + 12,00) = 156,00 €` — the acquisition charge
is long over. The raw account is therefore **44 553,305470 €**. On top of it the
*Schlussüberschussanteil* is 2 % of the contributions credited over the life of the contract,
which is exactly the guarantee accumulator: `0,02 × 37 877,2308 = 757,544616 €`; and the
*Bewertungsreserven* share is 1 % of the raw account, 445,533055 €. So
`account_conv_pp() = 45 756,383140 €`. The guarantee itself can be rebuilt without the recursion:
`guar_pp_init + pool_gefoerdert_pp(18) = 4 369,92 + 33 507,3108 = 37 877,2308 €`, which is
**7 879,15 € below** the account, so `capital_conv_pp() = 45 756,383140 €` and the
*Garantielücke* is zero on the `base` scenario. The annuity factor at age 67 in calendar 2044 on
the first-order generational basis is `ä = 20,8722287915`, so the current *Rentenfaktor* is
`0,70 × 10 000 / (12 × 20,8722287915) = 7 000 / 250,466746 = 27,947822`, **below** the
guaranteed 29,00, and the guaranteed factor applies. The lump sum is
`0,30 × 45 756,383140 = 13 726,914942 €`, leaving 32 029,468198 € to annuitise; the monthly
instalment is `32 029,468198 / 10 000 × 29,00 = 92,885458 €`, comfortably above the 39,55 €
*Kleinbetragsrente* threshold, so the contract annuitises and the annual annuity is
`12 × 92,885458 = 1 114,625493 €`. Weighted on `pols_conv() = 0,7675876849`, that is
`claims_lumpsum(18) = 10 536,61 €` and `claims_annuity(18) = 855,57 €` — the table's row 18.

*The aggregate account rolls forward, and the charge the insurer keeps is what closes it.* The
account at the start of `t = 2` is `A(2) × l(2) = 5 568,986940 × 0,9789198848 = 5 451,592054 €`.
Rebuilt from year 1's own published parts: the opening account 4 010,98 €, plus the *Sparbeitrag*
1 432,80 €, plus the interest 125,206940 €, less the three exit benefits 6,682784 €, 43,608465 €
and 65,619183 €, less the **exit charge the insurer retains** —
`0,02 × 5 568,986940 × 0,0079904 = 0,889966 €` of *Stornoabzug* plus
`50,00 × 0,0118897152 = 0,594486 €` of transfer charge, 1,484454 € — gives
`5 568,986940 − 117,394886 = 5 451,592054 €`. The two agree to the last printed digit. Dropping
the exit charge — which looks like income rather than like account released — leaves a residual
of 1,48 € in year 1, and is the usual way this identity fails.

*Closure: the decrements sum to one.* Over the whole sixty-one-year projection, expected deaths
in accumulation are **0,04132833**, deaths in payout **0,76758768**, surrenders **0,07668891**
and transfers out **0,11439508**. They sum to **1,00000000** exactly, and `pols_if(62) = 0`
because `mort_rate` is forced to 1 at `omega_age = 110`. Nothing is left in force and no exit is
counted twice. Note what the split says about the product: **23,24 % of the cohort leaves before
*Rentenbeginn*, and of those, 49,2 % leave by *Anbieterwechsel* against 33,0 % by *Kündigung*
and 17,8 % by death** — half again as many transfers as surrenders, at every duration and in
aggregate. A book modelled with a lapse rate alone would have mis-specified where the money goes
as well as how much of it goes.

*Closure: the statement reconciles.* On the Total row,
`25 631,84 + 3 627,10 − 35 580,17 − 1 069,29 − 436,87 = −7 827,39 €`, where 35 580,17 € is the
sum of all six `claims_*` columns. `int_credited` of 7 544,45 € is **not** in that sum: it moves
money inside the account rather than across the insurer's boundary, and adding it would report
the cell's undiscounted deficit as 282,94 € instead of 7 827,39 €. This is `check_net_cf()`,
delib's first ruling, evaluated on the totals rather than period by period.

### Variant 1 — the `low` scenario and a binding *Beitragsgarantie* (model point 11)

`scenario_id = low` declares 0,50 % a year instead of 2,30 %. Model point 11 is a **shorter
deferral** than the anchor and that is deliberate: on a seventeen-year accumulation even 0,50 %
does not open a *Garantielücke*, and the reason is worth stating rather than hiding. Model
point 11 is `F`, `issue_age = 57`, `duration_init = 3`, so `age(1) = 60` and
`t_conv() = 8`; `income_id = grow2_60k` with `income_init = 60 000,00`, so the 2 100 € ceiling
binds from year 1 and `E(t) = 2 100 − Z*(t)`; `zulage_id = k1_2010` and
`zulage_init_pp = 475,00` as on the anchor; `beitragssumme = 17 500,00`; `prem_freq = annual`;
opening balances `dk_pp_init = 4 900,00`, `surplus_pp_init = 200,00`, `guar_pp_init = 5 825,00`,
so the cell opens 725,00 € under water; `teilkapital_share = 0.30`,
`rentenfaktor_guar = 29,00`, `rentengarantie_years = 10`; `proj_len() = 51`.

| t | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_lumpsum | claims_annuity | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 1,625.00 | 475.00 | 35.08 | 21.95 | 55.11 | 83.09 | 0.00 | 0.00 | 33.67 | 31.50 | 1,874.68 |
| 2 | 0.977045 | 1,587.70 | 464.10 | 43.81 | 30.15 | 68.80 | 103.89 | 0.00 | 0.00 | 33.55 | 30.78 | 1,784.63 |
| 3 | 0.954320 | 1,837.07 | 453.30 | 53.94 | 40.83 | 63.51 | 96.21 | 0.00 | 0.00 | 33.03 | 34.36 | 2,022.42 |
| 4 | 0.936516 | 1,802.79 | 163.89 | 62.58 | 52.11 | 73.66 | 111.65 | 0.00 | 0.00 | 33.07 | 29.50 | 1,666.69 |
| 5 | 0.918697 | 1,768.49 | 160.77 | 70.91 | 64.95 | 83.42 | 126.51 | 0.00 | 0.00 | 33.09 | 28.94 | 1,592.36 |
| 6 | 0.900842 | 1,734.12 | 157.65 | 78.90 | 79.50 | 92.79 | 140.77 | 0.00 | 0.00 | 33.10 | 28.38 | 1,517.25 |
| 7 | 0.882930 | 1,699.64 | 154.51 | 86.57 | 95.94 | 101.75 | 154.41 | 0.00 | 0.00 | 33.09 | 27.81 | 1,441.15 |
| 8 | 0.864938 | 0.00 | 151.36 | 0.00 | 0.00 | 0.00 | 0.00 | 5,449.11 | 442.47 | 21.28 | 0.00 | −5,761.50 |
| 9 | 0.858363 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 442.47 | 21.33 | 0.00 | −463.80 |
| 20 | 0.731563 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 374.24 | 19.04 | 0.00 | −393.28 |
| 51 | 0.000061 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | 0.01 | 0.00 | −0.04 |
| **Total, t = 1 … 51** | | **12,054.81** | **2,180.59** | **431.80** | **385.43** | **539.04** | **816.52** | **5,449.11** | **10,121.79** | **776.66** | **211.26** | **−4,064.43** |

Again the Total is summed at full precision and then rounded; summing the rounded cells gives
2 180,58 €, 431,79 €, 816,53 €, 10 121,82 €, 776,69 €, 211,27 € and −4 064,45 € on the seven
columns where the two differ.

**The guarantee binds, and this is the number the product exists to produce.** At `t = 8` the
raw account is 19 863,088636 €; the *Schlussüberschussanteil* adds 420,00 € and the
*Bewertungsreserven* share 198,630886 €, giving `account_conv_pp() = 20 481,719523 €`. The
guarantee accumulator is `guar_pp(9) = 21 000,000000 €` — the ceiling binds in every contribution
year, so the contributions credited are a round 2 100,00 € a year and the accumulator lands on a
round number. So `capital_conv_pp() = 21 000,000000 €` and
**`garantieluecke_conv_pp() = 518,280477 €`**: the insurer funds 518,28 € per policy out of its
own resources, 2,5 % of the capital, so that the saver receives at least what was paid in. The
annuity is then struck on the guaranteed capital rather than on the account —
`teilkapital_pp() = 6 300,00 €`, `annuity_capital_pp() = 14 700,00 €`, monthly instalment
`14 700 / 10 000 × 29,00 = 42,63 €`, annual 511,56 € — and `claims_lumpsum(8) = 6 300,00 ×
0,8649383502 = 5 449,11 €`.

Two sensitivities follow, both reproducible by flipping `scenario_id` in
`model_point_table.csv`. On `base` this same cell's account reaches 22 271,80 € against the same
21 000,00 € guarantee, so the *Garantielücke* is **zero**: 1,80 percentage points of declared
interest over seven years is the whole difference between a guarantee that costs nothing and one
that binds — sensitivity 1, made arithmetic. And on the **anchor's** seventeen-year deferral the
`low` scenario still does not bind, but only just: the raw account at conversion is 37 370,67 €
against a guarantee of 37 877,23 €, a **raw shortfall of 506,56 €** closed only by the
*Schlussüberschussanteil* of 757,54 € and the *Bewertungsreserven* share of 373,71 €. Counting
those two toward the *Beitragserhaltungszusage* is the provider-favourable reading of an
unsettled question (gap 9); on the conservative reading the anchor's own low-rate *Garantielücke*
is 506,56 € rather than zero. That is sensitivity 4, and on this cell it is the larger of the
two.

### Variant 2 — the `fixed` contribution form (model point 5, the *mittelbar* spouse)

The second contribution form, at the economically extreme corner of the book: `contrib_form =
fixed` with `contrib_fixed_pp = 60,00`, the *Sockelbeitrag*, and `income_id = zero` because a
*mittelbar zulageberechtigt* spouse has no contribution-liable earnings of their own — so
`M(t) = max(60, min(0, 2 100) − 175) = 60,00 €`, the floor binds by construction, `E(t) = M(t)`
and the full *Grundzulage* is granted. `F`, `issue_age = 50`, `duration_init = 6`, so
`age(1) = 56` and `t_conv() = 12`; `beitragssumme = 1 020,00`; opening balances 1 150,00 €,
60,00 € and 1 400,00 €; `proj_len() = 55`. `claims_lumpsum` and `claims_annuity` are 0.00
throughout and `claims_commutation` replaces them.

| t | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_commutation | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 60.00 | 175.00 | 32.74 | 3.10 | 8.55 | 12.55 | 0.00 | 35.15 | 3.52 | 172.13 |
| 2 | 0.982960 | 58.98 | 172.02 | 37.75 | 3.93 | 9.85 | 14.55 | 0.00 | 35.23 | 3.46 | 163.97 |
| 11 | 0.856985 | 51.42 | 149.97 | 81.96 | 20.10 | 14.21 | 21.41 | 0.00 | 36.35 | 3.02 | 106.29 |
| 12 | 0.843758 | 0.00 | 147.66 | 0.00 | 0.00 | 0.00 | 0.00 | 3,828.31 | 0.00 | 0.00 | −3,680.65 |
| 13 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 55 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **Total, t = 1 … 55** | | **609.80** | **1,926.26** | **631.80** | **108.72** | **123.71** | **184.87** | **3,828.31** | **391.21** | **35.83** | **−2,136.59** |

The saver pays 609,80 € over the whole projection and the state pays 1 926,26 € — **the Zulage
is 76 % of the contribution**, which is why a statement that folded `zulagen` into `premiums`
would be describing a different product. The contract never produces an annuity: at `t = 12` the
capital is 4 537,217342 €, and the annuity after the elected 30 % lump sum would be
`0,70 × 4 537,217342 / 10 000 × 29,00 = 9,21 €` a month against a 39,55 € threshold, so the
*Kleinbetragsrente* test commutes it and the whole capital is paid as an *Abfindung*,
`3 828,31 € = 4 537,217342 × 0,84375772`. There is **no** *Teilkapitalauszahlung* beside it,
`pols_if` is zero from `t = 13` because the *Abfindung* discharges the contract outright — an
exit `check_pols_roll_fwd()` counts as a commuted cohort rather than as a decrement — and the
frame carries zeros to `t = 55` rather than being truncated.

### Changes the model stage made to these notes

Six, each because the model and the notes as drafted disagreed and the model was right.

1. **The frequency loading was deducted twice.** The drafted `S = C − K_a − K_v` had an
   *unloaded* `C` and a `K_v` already carrying `E(t)(φ − 1)`, so `prem_to_av_pp` **fell** with
   the payment frequency, contradicting pitfall 11. `C(t)` is now the cash **received** and the
   administration charge's percentage base is the unloaded `B(t)`; model point 3 (monthly) now
   has `premiums` larger by exactly `E(t) × 0,03` and an identical `prem_to_av_pp`, `guar_pp`
   and benefit set.
2. **`check_conversion()`'s third identity was inconsistent with the *Rentenfaktor* margin.**
   `12 · annuity_month_pp() · ann_factor() = annuity_capital_pp()` cannot hold when the factor
   carries a 30 % loading — it is short by exactly that margin. It is replaced by
   `rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000`, which says the
   same thing about the annuity basis, holds on every model point rather than only where the
   current factor applies, and still catches a Woolhouse correction applied twice.
3. **`check_pols_roll_fwd()` did not account for a commuted cohort.** An *Abfindung* discharges
   the contract, so `pols_if(t_conv() + 1) = 0` with no decrement having removed the population.
   The identity now carries `pols_conv()` as a fourth exit in the conversion year of a commuted
   contract; without it the check is false on model points 4, 5, 10 and 13.
4. **The guarantee accumulator's unsubsidised limb is gated on `is_accum(t)`**, matching
   `premiums(t)`. As drafted it added `contrib_extra_pp` in the conversion year, in which no
   contribution is paid.
5. **Model point 11 is a shorter-deferral cell than first drafted**, and its row in the model
   point table has been rewritten. Specified as the anchor with `scenario_id = low`, it did not
   bind: on that cell seventeen years of 0,50 % interest plus the two terminal surplus
   components exceed the charges by 624,69 €. The anchor-at-`low` figures are reported in
   Variant 1 as the sensitivity they are, because the 506,56 € raw shortfall they show is the
   more interesting of the two results.
6. **Model point 2 reconciles the anchor's account seeds and not its guarantee seed.** Projected
   from its own inception on the contract-clock income path `grow2_pre`, it reproduces
   `dk_pp_init` as 3 860,499285 € against 3 860,50 €, `surplus_pp_init` as 150,483132 € against
   150,48 € and `av_total_pp(1)` as 4 010,982418 € against 4 010,98 €, and from its `t = 4` onward every
   per-policy quantity coincides with the anchor's from `t = 1`. Its guarantee accumulator at the
   same point is **4 565,00 €** against the seed's 4 369,92 €. The two seeds were struck on
   different income paths — the account seed on earnings level at 42 000 € over the three
   pre-valuation contribution years, which reproduces 3 860,50 € to the cent, and the guarantee
   seed on a 2 %-declining back-path, which reproduces 4 369,92 € to the cent — and they cannot
   both be right. The seeds are kept as specified, because they are **[std]** opening balances of
   an in-force cell rather than derived quantities and because `garantieluecke_pp(1) = 358,94 €`
   depends on the pair; the 195,08 € discrepancy is recorded rather than papered over, and a
   calibration pass should restrike both on one path.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** Prospective, computed on the
  *Rechnungsgrundlagen erster Ordnung* of the premium calculation — the tariff's own *Rechnungszins*
  and its first-order biometric basis — under § 341f HGB and the DeckRV [REG-R14] [REG-R54]. It is
  **not** the Solvency II best estimate, and the whole German picture depends on keeping the two
  apart: an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
  *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side. `dk_pp(t) ×
  pols_if(t)` is this model's contribution to the first of them; the second-order path above is what
  feeds the Solvency II side.
- **The *Zinszusatzreserve*.** Where the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's
  tariff rate, an additional HGB reserve arises [REG-R17]. On a **0,25 %** tariff it is small or nil;
  on the 1,75 % and 2,25 % vintages that dominate the older Riester book it is not, which is one
  reason a model of this product should carry `rechnungszins` as a **model-point** attribute rather
  than a library constant.
- **The guarantee is an option, and this projection prices none of it.** The *Beitragsgarantie* is a
  written put on the accumulation, struck at the contributions paid and exercisable once. The
  deterministic path above reports the *Garantielücke* on **one** declared-rate scenario;
  a time-value-of-options-and-guarantees calculation re-evaluates the crediting rule and the
  guarantee test per stochastic scenario, and the two scenarios shipped (`base`, `low`) are a
  sensitivity, not a distribution.
- **Solvabilität II.** Best estimate plus risk margin under the Directive as transposed by
  §§ 74–110 VAG [REG-R5] [REG-R6], with EIOPA publishing the curves. `BEL = Σ_t v(t) ·
  liability_cf(t)` over the recursion above. **No risk-free curve value, volatility adjustment,
  cost-of-capital rate or standard-formula shock in this library was read from a retrieved
  instrument**, so every such figure would be **[std]**.
- **Contract boundary.** A Riester contract's future contributions are not unilaterally variable by
  the insurer, and the *Wechselrecht* is the policyholder's [R1] — but whether the Solvency II
  boundary extends to the whole future contribution stream **could not be determined** here, because
  the Delegated Regulation's boundary rules were not retrievable. The model's posture is to project
  the full stream and publish it; a boundary-truncated view is obtained by truncating `result_cf()`.
- **The surplus regulations.** The MindZV puts an arithmetic floor under the transfer to the
  *Rückstellung für Beitragsrückerstattung* [REG-R18] [REG-R19] and § 153 VVG gives the individual
  entitlement and the *hälftige* participation in the *Bewertungsreserven* [REG-R24]. This model
  takes `decl_rate` as an **exogenous management action** and does not derive it from a
  distributable surplus; `frlib/products/assurance_vie_euro/` derives its credited rate from a
  statutory account, and the difference between the two treatments is a real difference between the
  two jurisdictions' surplus law, not a modelling shortcut.
- **IFRS 17.** A participating contract of this kind would be measured under the variable fee
  approach [REG-R55]; the same expected-cash-flow engine feeds it, and grouping, the CSM and the risk
  adjustment are out of scope.

---

## Key sensitivities and model risks

In rough order of leverage on a German Riester block.

1. **The declared *laufende Verzinsung*.** It is the largest single lever in the model and the least
   supported: it sets the account's growth, hence whether the *Garantielücke* is positive at all,
   hence the whole cost of the product's defining feature. Moving the `base` scenario from 2,30 % to
   the `low` scenario's 0,50 % is the difference between a guarantee that costs nothing and one that
   binds — model point 11 exists to show it. **No declared rate at any carrier was established**
   (gap 12).
2. **The charge basis, and whether the Zulagen are charged.** Every charge is **[std]** (gap 13), and
   the **charge base for the Zulagen is unknown** (gap 14). On the low-income model points the
   Zulagen are the majority of the contribution, so this one unestablished convention moves the
   account value by tens of per cent on exactly the cells the product was designed for.
3. **The annuity basis and its generational structure.** A twenty-year deferral means the conversion
   happens on `τ = 2044` mortality. The improvement function, not the base table's level, is what
   decides the annuity factor, and it is entirely **[std]** [REG-R49]. The `rentenfaktor_margin` of
   30 % compounds the same uncertainty in the opposite direction.
4. **Which surplus components close the guarantee.** Counting the *Schlussüberschussanteil* and the
   *Bewertungsreserven* share toward the *Beitragsgarantie* is the provider-favourable reading and
   is unestablished (gap 9). Excluding them raises `garantieluecke_conv_pp()` by their whole amount
   on any cell where the guarantee binds.
5. **The absence of a *Beitragsfreistellung* decrement.** The dominant exit in the real book is
   represented as a per-model-point switch. A book projection built from these model points will
   therefore over-state future contributions and Zulagen unless the point weights carry the paid-up
   share — and **there is no official statistic for that share at all** (gap 2).
6. **The *Kleinbetragsrente* test.** Two things are unestablished: the threshold itself, where two
   irreconcilable readings exist [REG-R42], and whether the test applies before or after the elected
   lump sum (gap 7). The model takes the lower threshold and the post-lump-sum reading, both of
   which push toward **fewer** commutations and a longer-tailed liability.
7. **Holding the *Kleinbetragsrente* threshold flat in nominal terms.** The *Bezugsgröße* is reset
   annually; on a seventeen-year deferral a flat threshold **understates** the commutation rate, and
   the direction of the error is stated rather than hidden.
8. **The monthly annuity on an annual grid.** The model pays a full year to a life that dies in the
   payout year, overstating the annuity outgo by roughly `½ · q(x) · 12R` a year. It is small at 67
   and grows with attained age; `products/sofortrente/` runs monthly for that reason.
9. **Everything statutory is `[unverified]` at the paragraph level** (gap 4), and the two most
   consequential figures in the whole subsidy — the 175 €/300 € Zulagen and the 4 % / 2 100 € / 60 €
   arithmetic — rest on general knowledge corroborated only at one remove [REG-R42]. A calibration
   pass against the statute and against a real *Produktinformationsblatt* [S14] is required before
   any quantitative use of this model.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-riester_rente-r1
[R10]: #delib-riester_rente-r10
[R11]: #delib-riester_rente-r11
[R12]: #delib-riester_rente-r12
[R13]: #delib-riester_rente-r13
[R14]: #delib-riester_rente-r14
[R15]: #delib-riester_rente-r15
[R16]: #delib-riester_rente-r16
[R19]: #delib-riester_rente-r19
[R20]: #delib-riester_rente-r20
[R22]: #delib-riester_rente-r22
[R23]: #delib-riester_rente-r23
[R25]: #delib-riester_rente-r25
[R4]: #delib-riester_rente-r4
[R6]: #delib-riester_rente-r6
[R8]: #delib-riester_rente-r8
[R9]: #delib-riester_rente-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R20]: #delib-reg-r20
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R40]: #delib-reg-r40
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R44]: #delib-reg-r44
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
