# Technical Notes

**Status:** Draft, 2026-08-29 (access date for every citation: 2026-08-29).

**Retrieval conditions.** **No document cited in these notes was retrieved.** Direct HTTP egress from
the build environment is blocked and the session's `WebSearch` budget was exhausted before this
product was reached, so a delib citation is a **pointer, not a certificate** — it names the instrument
a claim must be checked against, not a document anyone read. Nothing here is quoted from a German
statutory or contractual text, and every specific number carries [unverified] or **[std]**. See
`product-spec.md` for the full statement.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Basis_DE_A`**, **annual** grid — for the standardized composite German *Basisrente* defined in
`product-spec.md` (same directory). This is not any single insurer's product. [S#]/[R#] tags refer to
the source list in `sources.md` (numbering carried from `_research/basisrente.md`; frozen); [REG-R#]
tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen numbering). **[std]** marks a
standardization introduced for the reference implementation; [unverified] a claim no search result
confirmed. Parameter values are identical to those in `product-spec.md`. Cells names, model-point
columns and CSV headers are English `lower_snake_case`; German terms of art keep their German form in
prose, where they are the name of the thing.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — *laufende
  Beiträge* and *Zuzahlungen* in; death benefits, annuity payments, survivor benefits, insurer expenses
  and commission out — for a single model point on an expected (probability-weighted) basis, with the
  state variables that make the product what it is: the ***Deckungskapital*** of the premium-paying and
  premium-free cohorts, and the annuity secured at *Rentenbeginn*.
- **Out of scope, and said so.** No discounting; no *Deckungsrückstellung*, *Zinszusatzreserve*
  [REG-R17], Solvency II technical provision, risk margin or SCR — all cited, none computed. **No
  tax**: the *Sonderausgabenabzug* [R2] [R7] and the *Besteuerungsanteil* [R4] [REG-R41] shape the
  product's economics, belong to `product-spec.md`, and are not cash flows of the contract. **No BUZ
  cash flows**: a BUZ written inside the contract is represented only by its **premium share**, its
  disability mechanics belonging to `BU_DE_S` (delib product 9). No *Versorgungsausgleich*, no provider
  transfer, no *Wiederinkraftsetzung*, no unit-linked or hybrid asset form.
- **The absences are the product.** There is **no surrender-value cells, no `claims_lapse` column, no
  `cv_pp`, no `loan_pp`, no commutation and no lump sum anywhere in this model**, because the
  entitlement is *nicht kapitalisierbar*, *nicht veräußerbar* and *nicht beleihbar* [R1] [R14]
  [REG-R39] [REG-R40] — structural absences, not switched-off options, and `check_no_capital()`
  asserts them in code rather than in prose.
- **Projection grid: annual.** `t` counts **projection years from the valuation date**, and the frame
  is **1-based**: `t = 1 … proj_len()`. Policy duration at the start of year `t` is
  `duration(t) = duration_init + t − 1` completed policy years; attained age is
  `age(t) = entry_age + duration_init + t − 1`; calendar year is
  `cal_year(t) = conclusion_year + duration_init + t − 1`. A new-business model point has
  `duration_init = 0`, so `t = 1` is the first policy year; an in-force point opens at whatever
  duration it has already run, and **the frame still starts at `t = 1`**.
- **The annual grid is a choice, and here is the argument for it.** Every contractual event lands on
  a policy anniversary: the *Beitragsdynamik* step, the *Zuzahlung*, the annual declaration of
  *Überschussbeteiligung*, the *Beitragsfreistellung* effective at the end of the current premium
  period [R14], and the conversion at *Rentenbeginn*. The one genuinely sub-annual mechanic — the
  annuity is paid **monthly** [R1] — is compressed to twelve instalments booked at the start of the
  payout year, a **[std]** convention and pitfall 12.
- **Projection horizon.** The annuity is lifelong, so the projection runs to the end of the mortality
  table: `proj_len() = omega_age() − age(1) + 1`, where `omega_age()` is the last age in
  `mort_table.csv`, where `qx = 1.0`. **The terminal age is absorbing**: `mort_rate(t) = 1.0`
  wherever `age(t) ≥ omega_age()`, whatever `mort_be_factor` says, so `pols_if(proj_len() + 1) = 0`
  exactly and the decrement closure identity holds to the last euro. Without that rule the
  generational trend would carry the table's own terminal rate below 1 and leave a residue in force
  after the end of the table. `omega_age = 121` **[std]**, the terminal age German annuity tables
  are conventionally carried to. For the anchor cell `proj_len() = 121 − 45 + 1 = 77`.
- **`proj_len()` is the last projected period index**, not a row count: `result_cf().index[-1] ==
  proj_len()`. This is frlib's ruling and delib adopts and asserts it. Where the frame *starts* is a
  product fact and is not asserted; contiguity is.
- **Timing conventions [std].** The *laufender Beitrag* and the *Zuzahlung* are taken at the **start**
  of the projection year (annual in advance; a fractionated mode changes the amount through the
  *Ratenzahlungszuschlag*, not the grid), and the charges on them are struck at the same moment.
  Interest is credited at the **end** of the year; deaths fall after crediting, so a dying policy
  carries a full year's interest; the *Beitragsfreistellung* transition falls after the death
  decrement. Annuity instalments are booked at the **start** of the payout year on the opening
  in-force count. Acquisition expense and initial commission fall at inception, maintenance expense
  and renewal commission at the start of each year.
- **Charges are not cash flows.** The *Zillmerung* amortisation, the premium charge β, the reserve
  charge γ and the *Stückkosten* are **deductions from the policyholder's *Deckungskapital***, hence
  insurer income; the insurer's own **outgo** is the acquisition expense, the commission, the
  maintenance expense and the annuity administration. A charge affects `net_cf` only through the
  benefit it shrinks; booking one as both is pitfall 4.
- **Two cohorts, one model point.** A *Beitragsfreistellung* does not remove a policy; it moves it to
  the premium-free cohort, where its *Deckungskapital* is still credited and still converts at
  *Rentenbeginn* [R14]. The two cohorts' account values diverge from the first freeze, so the model
  carries the paying cohort **per policy** and the premium-free cohort **at fund level** — exact,
  because every paying policy in one model point is identical.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  benefits and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents and `pols_if` to six decimals **[std]**. Totals are summed at full precision and then rounded.
- **Age basis.** Age last birthday at conclusion (*Eintrittsalter*), stepping on the policy
  anniversary **[std]**: no German convention was established, and here mortality drives the annuity's
  duration rather than any benefit amount, so a half-year offset is second order. `mort_rate` is
  generational and depends on the **calendar** year as well as the age [R17] [REG-R49], which is why
  `cal_year(t)` is carried.

### External input files

Inputs are **external CSVs in the model folder's parent**, read once per model by unparameterized
reader cells in the `Data` Space (the `annuallife/TradLife_A` layout). Every file but
`model_point_table.csv` carries a final **`provenance`** column, one tag per row — delib's second
ruling, asserted by the conventions suite.

| File | Index columns | Value columns | What it is |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the 25 attributes below | The policies. Exempt from the provenance rule: a model point is a configuration, not an assumption |
| `mort_table.csv` | `age` | `qx`, `trend` | The **[std]** DAV 2004 R-shaped **first-order** proxy: `qx` at the base calendar year and the annual improvement `trend` that makes it generational |
| `surplus_table.csv` | `scenario_id`, `t` | `decl_rate`, `ann_bonus_rate` | The declared *laufende Verzinsung* in the *Aufschubphase* and the *Überschussrente* uplift in the *Rentenphase*, by scenario and projection year |
| `rentenfaktor_table.csv` | `rf_scenario_id`, `age` | `rf_curr` | The insurer's *aktueller Rentenfaktor* at each conversion age, by scenario |
| `charge_table.csv` | `tariff_id` | `zill_rate`, `alpha_zuz_rate`, `beta_prem`, `gamma_av`, `unit_cost_pp`, `terminal_bonus_rate`, `acq_expense_pp`, `comm_init_rate`, `comm_renew_rate`, `maint_expense_pp`, `annuity_admin_pp`, `expense_infl` | One row per tariff: the charge scale and the insurer's own expense and commission scale |
| `behaviour_table.csv` | `beh_table_id`, `dur` | `bf_rate`, `zuz_take_up` | The two behavioural assumptions that vary by policy duration: the *Beitragsfreistellung* rate and the *Zuzahlung* take-up. **`dur` is the policy year, `duration(t) + 1`**, so "durations 1–5" below reads off the file directly |
| `option_table.csv` | `option_id`, `option_key` | `factor` | One multiplicative factor per contractual option: `prem_mode` → the *Ratenzahlungszuschlag* on the premium; `guarantee_period` and `survivor` → the reduction in the *Rentenfaktor* |

Scalar assumptions that are single numbers rather than tables are `Projection` References and are
tagged in *Assumption inputs* below: `mort_be_factor`, `elig_surv_prob`, `mort_base_year`,
`zill_spread_y`, `rf_unit`, `ann_freq`, `roll_fwd_tol`.

---

## Model point attributes

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Index into `model_point_table.csv`; `Projection`'s only parameter | all |
| `policy_id` | str | The carrier's own reference, carried for reporting | all |
| `sex` | enum {M, F} | Reporting only. **Must not enter pricing**: unisex is mandatory for contracts concluded from 21 December 2012 [REG-R34] | 1–13 |
| `entry_age` | int | Age last birthday at conclusion (*Eintrittsalter*) | all |
| `conclusion_year` | int | Calendar year the contract was concluded. Fixes the age-floor cohort (60 before 2012, 62 after) [R1] [R8], the guarantee vintage [REG-R15] and the generational mortality cohort [R17] | 6, 7, 8 (pre-2012 / pre-2015 / pre-2010) |
| `duration_init` | int | Completed policy years at the valuation date; 0 = new business | 6, 7, 8 |
| `ret_age` | int | Attained age at *Rentenbeginn* | 6 (60, the pre-2012 floor), 12 (70) |
| `pols_if_init` | float | Policies the model point represents | all |
| `prem_form` | enum {regular, single} | *laufender Beitrag* against *Einmalbeitrag* | 5 (single) |
| `prem_base_pp` | EUR p.a. | The contractual *laufender Beitrag* at inception, before the *Ratenzahlungszuschlag* and before any *Dynamik*; for `single`, the *Einmalbeitrag* | all but 7, 8 |
| `prem_mode` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency; keys `option_table.csv` for the *Ratenzahlungszuschlag* | 1, 5, 7, 8, 9, 13 annual · 4 half-yearly · 3, 11 quarterly · 2, 6, 10, 12 monthly |
| `prem_dyn_rate` | rate p.a. | *Beitragsdynamik*, the contractual annual escalation | 1, 2, 3, 4, 6, 9, 11, 12 |
| `zuzahlung_pp` | EUR p.a. | The nominal annual *Zuzahlung* before take-up | 1, 3, 11 |
| `zuzahlung_end_dur` | int | Last policy duration at which a *Zuzahlung* is assumed | 1, 3, 11 |
| `paidup_at_init` | bool | The model point is already *beitragsfrei* at the valuation date | 7 |
| `av_pp_init` | EUR | *Deckungskapital* per policy at the valuation date | 6, 7 |
| `ann_pp_init` | EUR p.a. | Annual annuity already in payment, for a point that opens in the *Rentenphase* | 8 |
| `gtd_rate` | rate p.a. | The contract's *Rechnungszins*, the cohort's guarantee vintage [REG-R15] | 6 (2,25 %), 7 (1,75 %), 8 (2,75 %), rest 1,00 % |
| `rentenfaktor_gtd` | EUR per month per 10 000 € | *Garantierter Rentenfaktor*, fixed at inception [R17] [S1] | 6, 13 (both set above the current-factor scenario at their conversion age, so the guarantee binds) |
| `guarantee_period_y` | int | *Rentengarantiezeit* in years from *Rentenbeginn*; 0 = none | 4 (10), 12 (20) |
| `surv_annuity_rate` | rate | Survivor's annuity as a fraction of the main annuity; 0 = **rider off**, which is the base design | 3 (0.60), 12 (0.60) |
| `buz_prem_share` | rate | Share of the **total** contribution attributable to a BUZ. Must satisfy `buz_prem_share < 0.50` [R1] | 11 (0.49, the boundary) |
| `tariff_id` | str | Key into `charge_table.csv` | all |
| `beh_table_id` | str | Key into `behaviour_table.csv` | all |
| `surplus_scenario_id` | str | Key into `surplus_table.csv` | all |
| `rf_scenario_id` | str | Key into `rentenfaktor_table.csv` | 13 (`low`) |

**There is no `surr_rate`, no `lapse_rate` and no `kapitalwahl` column**, and their absence is a
statutory fact rather than a modelling simplification [R1] [R14] [REG-R39]. `lapse_rate` is the name a
modeller reusing the endowment or Schicht-3 chassis reaches for first; the decrement it names does not
exist here, and `bf_rate` — which is **not** a lapse — takes its place.

**An in-force paid-up point is represented wholly, not partly.** A model point opens either entirely
premium-paying (`paidup_at_init = 0`) or entirely premium-free (`paidup_at_init = 1`, the whole of
`pols_if_init` opening in the premium-free cohort with
`av_pu_at(1, "BEF_PREM") = av_pp_init × pols_if_init`). A part-paid-up book is **two model points**,
which is the honest arrangement: averaging the two cohorts' reserves is pitfall 3.

### The shipped model point table

| # | What it is for | Key settings |
|---|---|---|
| 1 | **Anchor** — the worked example. A self-employed buyer at the product's typical entry age | 45 → 67, 2026, 6 000 € annual + 4 000 € *Zuzahlung*, 2 % *Dynamik*, no riders |
| 2 | Monthly premium, long deferment | 35 → 67, 3 000 € p.a. monthly, 3 % *Dynamik*, no *Zuzahlung* |
| 3 | Quarterly premium with the **survivor's annuity** switched on | 48 → 67, quarterly, `surv_annuity_rate = 0.60` |
| 4 | Half-yearly premium with a **10-year *Rentengarantiezeit*** | 52 → 67, half-yearly, `guarantee_period_y = 10` |
| 5 | ***Einmalbeitrag*** — the late-career deferral of a high-income year | 58 → 67, `prem_form = single`, 60 000 € once |
| 6 | **In-force, pre-2012 cohort, at the 60 age floor** | concluded 2009, `duration_init = 17`, `ret_age = 60`, `gtd_rate = 2,25 %` |
| 7 | **In-force and already *beitragsfrei*** | concluded 2014, `duration_init = 12`, `paidup_at_init = 1`, `gtd_rate = 1,75 %` |
| 8 | **In-force and already in payment** — opens in the *Rentenphase*, `ret_t() ≤ 0` | concluded 2006, `entry_age = 48`, `duration_init = 20`, `ret_age = 65`, `ann_pp_init > 0` |
| 9 | **Boundary — the whole *Höchstbetrag*** | 50 → 67, 30 826 € p.a. annual [R2] [unverified] |
| 10 | **Boundary — the *Kleinbetragsrente* that may not be commuted** | 30 → 67, 300 € p.a. monthly (25 €/month) |
| 11 | **Boundary — the 50 % rule** | 42 → 67, quarterly, `buz_prem_share = 0.49` |
| 12 | Deferral to 70 with **both options on** | 55 → 70, monthly, `surv_annuity_rate = 0.60`, `guarantee_period_y = 20` |
| 13 | **Boundary — the guaranteed *Rentenfaktor* binds** | 46 → 67, `rentenfaktor_gtd = 34.00`, `rf_scenario_id = low` |

Between them the thirteen exercise both premium forms, all four payment frequencies, all three
in-force shapes (accumulating, paid-up, in payment), both option modules separately and together, both
age-floor cohorts, four guarantee vintages and four boundary cases.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | Last projected period index, `omega_age() − age(1) + 1` | once per model point |
| `ret_t` | The projection year in which *Rentenbeginn* falls, `ret_age − age(1) + 1`; **≤ 0 for a point that opens in payment** | once per model point |
| `age(t)`, `duration(t)`, `cal_year(t)` | Attained age, completed policy years and calendar year at the start of year `t` | annual |
| `pols_if(t)` | Policies in force at the **start** of year `t`, paying and premium-free together; the weight on that same `result_cf()` row | annual recursion |
| `pols_paying(t)` | The premium-paying subset at the start of year `t` | annual recursion |
| `pols_paidup(t)` | The premium-free subset, `pols_if(t) − pols_paying(t)` | annual |
| `pols_if_at(t, timing)` | End-of-period state: `"BEF_DECR"`, `"AFT_DEATH"`, `"AFT_FREEZE"` | within year `t` |
| `pols_death(t)` | Expected deaths in year `t`, split as `pols_death_paying(t)` and `pols_death_paidup(t)` | annual |
| `pols_freeze(t)` | Policies going premium-free during year `t` (the *Beitragsfreistellung* transition) | annual |
| `pols_gtd(t)` | *Rentengarantiezeit* continuations running at the start of year `t` | annual recursion |
| `av_pp_at(t, timing)` | *Deckungskapital* **per premium-paying policy**: `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_INT"` | within year `t` |
| `av_pp(t)` | `av_pp_at(t, "BEF_PREM")` | annual |
| `av_pu_at(t, timing)` | *Deckungskapital* of the **premium-free cohort, at fund level**, same three timings | within year `t` |
| `av_at(t, timing)` | The whole *Deckungskapital* at fund level, `av_pp_at(t, ·) × pols_paying(t) + av_pu_at(t, ·)` | within year `t` |
| `av(t)` | `av_at(t, "BEF_PREM")`; **zero for every `t > ret_t()`** | annual |
| `cred_rate(t)` | The rate credited to the *Deckungskapital*, `max(gtd_rate, decl_rate(t))` | annual |
| `ann_pp(t)` | Annual annuity per surviving annuitant in year `t`, in the *Rentenphase* only | annual recursion |
| `beitragssumme_pp` | The contract's *Beitragssumme* at inception, the base of the 25 ‰ *Zillmerung* cap | once per model point |

There is **no** account value in the *Rentenphase*: the whole fund converts at `ret_t()` into an
annuity obligation, and the reserve that stands behind that obligation is a
*Deckungsrückstellung*, which delib cites and does not compute.

---

## Assumption inputs

Three classes are distinguished and every entry is tagged. Class (a) is contractual, statutory or
tariff-fixed and is cited; class (b) is the insurer's current discretionary scale, revisable annually;
class (c) is the modeller's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Annuity form | Monthly, lifelong, on the taxpayer's own life; **no lump sum of any kind at any date** | [R1] [REG-R39] |
| Earliest *Rentenbeginn* | Completion of the 62nd year for contracts concluded after 31 December 2011; the 60th for earlier ones | [R1] [R8] [REG-R39]; both [unverified] |
| Surrender value | **None at any duration.** § 169 VVG inoperative; no *Stornoabzug* | [R1] [R14] [REG-R28] |
| *Beitragsfreistellung* | Exercisable at any time for the end of the current premium period; converts to a premium-free entitlement to a reduced annuity | [R14] [REG-R28] |
| Death benefit, base design | **Nothing** before *Rentenbeginn*; the annuity simply ends after it | [R1] [REG-R39] |
| Death benefit, rider on | The *Deckungskapital*, payable **only where an eligible survivor exists**, and applied as the single premium of a survivor's annuity | [R1] |
| Permitted survivors | Spouse or registered partner; children while *Kindergeld* or the *Kinderfreibetrag* runs | [R1] [REG-R39] |
| *Rentengarantiezeit* | Remaining instalments to the end of the guaranteed period, **only to an eligible survivor**, **never commutable** | [R1] |
| BUZ premium share | Supplementary covers strictly **below 50 %** of the total contribution | [R1]; address [unverified] |
| Conversion rule | `ann_pp = fund / 10 000 × max(rentenfaktor_gtd, rf_curr) × 12`, reduced by the option factors | [R17] [S1] |
| *Rechnungszins* (`gtd_rate`) | The cohort's *Höchstrechnungszins*: 1,00 % from 1 January 2025; 0,25 % 2022–2024; 0,90 % 2017–2021; 1,25 % 2015–2016; 1,75 % 2012–2014; 2,25 % 2007–2011; 2,75 % 2004–2006. **Fixed at conclusion for the whole term** | [R16] [REG-R14] [REG-R15] |
| *Höchstzillmersatz* (`zill_rate`) | **25 ‰ of the *Beitragssumme***, from 1 January 2015 (40 ‰ before) | [R16] [REG-R16] [REG-R20] |
| *Überschussbeteiligung* entitlement | Statutory, on the same terms as any German life contract; MindZV floor 90 % / 90 % / 50 % | [R15] [REG-R24] [REG-R18] |
| Mortality basis | **DAV 2004 R**, generational; first order for pricing and the guaranteed *Rentenfaktor*, second order for the best estimate. **Not public, not redistributed** | [R17] [REG-R47] [REG-R49] |
| Unisex | Mandatory from 21 December 2012; `sex` is reporting only | [REG-R34] |

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

| Input | Base-run value | Basis |
|---|---|---|
| Declared *laufende Verzinsung* `decl_rate(t)` | **2,60 %** p.a. for `t = 1…10`, **2,40 %** for `t = 11…20`, **2,20 %** thereafter, in scenario `base` | **[std]** (i) |
| Credited rate | `cred_rate(t) = max(gtd_rate, decl_rate(t))` — the declared rate is the total credited rate, **not** a spread over the *Rechnungszins* | **[std]** (ii) |
| *Schlussüberschussanteil* `terminal_bonus_rate` | **4,0 %** of the fund, allocated **only at *Rentenbeginn*** | **[std]** (iii); single-date allocation [R15] |
| *Überschussrente* `ann_bonus_rate(t)` | **1,0 %** p.a., compounding — a *teildynamische Rente* | **[std]** (iv) |
| *Aktueller Rentenfaktor* `rf_curr(age)` | **31,50 €** at age 67 in scenario `base`; scenario `low` runs about 12 % below it | **[std]** (v) |
| *Verwaltungskosten* β on premium | **7,5 %** of each *laufender Beitrag* and *Zuzahlung* | **[std]**; band 5 %–10 %, product-spec |
| *Verwaltungskosten* γ on the reserve | **0,35 %** p.a. of the *Deckungskapital* | **[std]**; band 0,2 %–0,6 % |
| *Stückkosten* `unit_cost_pp` | **36,00 €** per policy p.a., inflating at `expense_infl` | **[std]** |
| Acquisition charge on a *Zuzahlung* `alpha_zuz_rate` | **2,5 %** of each *Zuzahlung*, charged in the year it is paid | **[std]**; gap 8 |
| *Ratenzahlungszuschlag* | 1,000 annual · 1,020 half-yearly · 1,030 quarterly · 1,050 monthly, on the *laufender Beitrag* only | **[std]**; market convention |
| Option cost on the *Rentenfaktor* | `guarantee_period` 0 → 1,000; 10 → 0,995; 20 → 0,974. `survivor` 0,00 → 1,000; 0,60 → 0,930 | **[std]** (vi) |

(i) **No declared rate specific to a Basisrente was established anywhere in the delib corpus**, and
the market-average rates in sibling delib files are Schicht-3 and endowment figures that must not be
relabelled. The path is a scenario, not a forecast: it starts above the 1,00 % *Höchstrechnungszins*
by a plausible surplus margin and grades down, so the guarantee does not bind on the base run.
(ii) German declared rates are quoted as the **total** credited rate including the *Rechnungszins*, so
`cred_rate` is a `max`, not a sum. Adding the declared rate **on top of** the guarantee is pitfall 6.
(iii) The single-date allocation is a **contract fact** [R15] — no surrender means no early-exit
trigger — while the 4,0 % level is **[std]** with nothing behind it.
(iv) A *volldynamische Rente* would consume the whole first-order margin released in the payout phase
and a *konstante Rente* none; 1,0 % is deliberately in between, and it decides how much of the
conversion-basis wedge (see *Key sensitivities*) is given back.
(v) **No *Rentenfaktor* level, range or time series exists anywhere in the delib corpus** (gap 4). The
base scenario is set **above** the guaranteed factor so `max(gtd, curr)` is visibly operative, and the
`low` scenario below it so model point 13 exercises the other branch.
(vi) Anchored on the sibling corpus's Schicht-3 illustration — a 10-year *Rentengarantiezeit* at about
0,5 % of the annuity, 20 years at 2,6 %, 30 years at 8,0 % — **[unverified] and explicitly not
transferable** to Schicht 1. The survivor factor has no anchor at all.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std] and none of it has a source.** No German insurer publishes a
*Beitragsfreistellung* rate, a *Zuzahlung* take-up, an eligible-survivor probability or a
best-estimate factor for a Basisrente, and the research file records the absence as gap 3.

| Input | Base-run value | Rationale |
|---|---|---|
| Mortality best-estimate factor `mort_be_factor` | **0.85** of the shipped first-order table | The first-order table carries the DAV's prudential margins [R17] [REG-R47]; 0.85 is a round **[std]** step to a best estimate and is the single largest unanchored number in the payout phase |
| Mortality improvement `trend` | **1,5 % p.a.** at every age, applied from `mort_base_year = 2005` | Keeps the table **generational**, which is what a replacement must preserve [REG-R49]. A flat trend across ages is a simplification; DAV 2004 R's own trends are age-dependent |
| *Beitragsfreistellung* rate `bf_rate(dur)` | **4,0 %** at durations 1–5, **3,0 %** at 6–10, **2,0 %** at 11+ | Higher than a Schicht-3 lapse rate early — the buyer's income is volatile by construction and going premium-free is free of penalty and reversible — and lower late, because there is no realisable value to tempt anyone out. That **shape** is argued in `product-spec.md`; the levels are invented |
| *Zuzahlung* take-up `zuz_take_up(dur)` | **0.70** at durations 1–5, **0.85** at 6–15, **0.90** at 16+ | The *Zuzahlung* is paid out of a profit not known until the year end, so it is behavioural, not contractual. Rising with duration because the contract and the habit bed in |
| Eligible-survivor probability `elig_surv_prob` | **0.55** | The probability that a spouse or registered partner, or a *Kindergeld*-eligible child, exists at the moment of death [R1]. On a contract taken at 45 and running to 67 the child channel has usually closed, so this is in substance a marriage-survival probability. **One of the most consequential [std] numbers in the whole delib library** |
| Acquisition expense `acq_expense_pp` | **250,00 €** at inception | Round-number placeholder |
| Initial commission `comm_init_rate` | **2,5 % of `beitragssumme_pp`**, paid at inception | Sized to the *Zillmerung* cap [R16], the German design in which what the insurer pays out is what it may write into the reserve. [S2]'s 1 575 € specimen *Abschlussprovision* is the corpus's only datum and is [unverified] |
| Renewal commission `comm_renew_rate` | **1,5 %** of premiums plus *Zuzahlungen* from year 2 | Market convention; no level established |
| Maintenance expense `maint_expense_pp` | **60,00 €** per in-force policy p.a., inflating | Placeholder |
| Annuity administration `annuity_admin_pp` | **36,00 €** per annuitant p.a., inflating | Placeholder; the payout phase is administratively cheaper than the accumulation phase |
| Expense inflation `expense_infl` | **1,5 %** p.a. | Placeholder |
| *Zillmerung* spread `zill_spread_y` | **5** years | The LVRG-era German market shape; **whether the AltZertG's five-year spreading reaches Basisrentenverträge was not established** (gap 8) |

**No decrement other than death and the *Beitragsfreistellung* transition exists in this model.** No
surrender, no assignment, no provider transfer, no commutation. That is the product [R1] [REG-R39]
[REG-R40], and pitfall 1 is what happens when a modeller carries one across by habit.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | projection year, `t = 1 … n`, `n = proj_len()` |
| `x(t)`, `d(t)`, `y(t)` | `age(t)`, `duration(t)`, `cal_year(t)` | attained age, completed policy years, calendar year at the start of year `t` |
| `T` | `ret_t()` | the projection year in which *Rentenbeginn* falls; `T ≤ 0` for a point that opens in payment |
| `l(t)`, `lᵖ(t)`, `lᶠ(t)` | `pols_if(t)`, `pols_paying(t)`, `pols_paidup(t)` | in force, premium-paying and premium-free at the start of year `t`; `l = lᵖ + lᶠ` |
| `q(t)` | `mort_rate(t)` | best-estimate annual death rate, `mort_rate_base(t) × mort_be_factor` |
| `qᵗ(x, y)` | `mort_rate_at_age(x, y)` | the first-order table rate at age `x` in calendar year `y` |
| `f(t)` | `bf_rate(t)` | *Beitragsfreistellung* rate, applied **after** the death decrement |
| `g(t)` | `pols_gtd(t)` | *Rentengarantiezeit* continuations running at the start of year `t` |
| `A(t)`, `Aᵖ(t)`, `Aᶠ(t)` | `av_at(t, ·)`, `av_pp_at(t, ·)`, `av_pu_at(t, ·)` | *Deckungskapital*: fund level, per paying policy, and premium-free block at fund level |
| `P(t)`, `Z(t)` | `prem_pp(t)`, `zuz_pp(t)` | the *laufender Beitrag* charged and the *Zuzahlung* paid, per paying policy |
| `P₀`, `δ`, `φ` | `prem_base_pp`, `prem_dyn_rate`, `prem_freq_load()` | base premium at inception, *Beitragsdynamik*, *Ratenzahlungszuschlag* |
| `S` | `beitragssumme_pp()` | the *Beitragssumme* at inception |
| `α`, `α_z`, `β`, `γ`, `u(t)` | `alpha_amort_pp(t)`, `alpha_zuz_pp(t)`, `beta_prem`, `gamma_av`, `unit_cost_pp(t)` | the four charges struck against the account |
| `N(t)` | `prem_to_av_pp(t)` | premium credited to the account after all four charges |
| `i(t)` | `cred_rate(t)` | credited rate, `max(gtd_rate, decl_rate(t))` |
| `σ` | `terminal_bonus_rate` | *Schlussüberschussanteil* rate at *Rentenbeginn* |
| `F` | `fund_at_conv()` | the fund converted at *Rentenbeginn*, including the terminal bonus |
| `R` | `rentenfaktor_applied()` | `max(rentenfaktor_gtd, rf_curr(ret_age)) × rf_option_factor()` |
| `a(t)` | `ann_pp(t)` | annual annuity per surviving annuitant in year `t` |
| `b(t)` | `ann_bonus_rate(t)` | the *Überschussrente* uplift applied at the end of payout year `t` |
| `π` | `elig_surv_prob` | probability an eligible survivor exists at the moment of death |
| `s` | `surv_annuity_rate` | the survivor's annuity as a fraction of the main annuity; `0` = rider off |
| `G` | `guarantee_period_y` | *Rentengarantiezeit* in years from *Rentenbeginn* |
| `E(t)`, `C(t)` | `expenses(t)`, `commissions(t)` | insurer expense and commission outgo, fund level |

`q`, `f`, `i`, `b` are per-annum rates; `A`, `P`, `Z`, `F`, `a`, `E`, `C` are EUR; `R` is euro of
monthly annuity per 10 000 € of capital.

### Premiums

The *Beitragsdynamik* compounds on the base premium from inception, so it is keyed to the **policy
duration**, not the projection year — which is what makes an in-force point work:

```
prem_base_pp(t) = prem_base_pp × (1 + δ)^d(t)                for prem_form = "regular"
P(t)            = prem_base_pp(t) × φ        if t < T and not paid-up and premiums are due
                = 0                          otherwise
```

with `φ = factor("prem_mode", prem_mode)` from `option_table.csv`. For `prem_form = "single"` the
*Einmalbeitrag* is paid once, at `t = 1` and only when `duration_init = 0`, and `φ = 1` — a single
payment carries no *Ratenzahlungszuschlag* (pitfall 8).

The *Zuzahlung* is behavioural and carries no frequency loading:

```
Z(t) = zuzahlung_pp × zuz_take_up(d(t))      if t < T and d(t) < zuzahlung_end_dur and not paid-up
     = 0                                     otherwise
```

Fund-level premium income is `premiums(t) = P(t) × lᵖ(t)` and `zuzahlungen(t) = Z(t) × lᵖ(t)`. The
BUZ appears only through a reporting cells that reconstructs the **total** contribution the
policyholder pays:

```
prem_total_pp(t) = ( P(t) + Z(t) ) / ( 1 − buz_prem_share )
```

`prem_total_pp` **never enters `net_cf`** — the BUZ premium buys a cover this model does not project —
and `buz_prem_share < 0.50` is the statutory invariant [R1] the test module asserts (pitfall 17).

### Charges and the premium credited to the account

The *Beitragssumme* is struck once, at inception, on the contractual *laufender Beitrag* including its
*Dynamik* and **excluding** *Zuzahlungen*, which is the conservative reading of an unresolved question
(gap 8):

```
S = Σ_{u=0}^{m−1} prem_base_pp × (1 + δ)^u          for prem_form = "regular", m = ret_age − entry_age
  = prem_base_pp                                    for prem_form = "single"
```

The zillmerised acquisition charge is capped at `zill_rate × S` and amortised in `zill_spread_y`
equal instalments over the first premium-paying years of the **contract**, not of the projection —
so an in-force point that is past duration 5 sees none of it:

```
alpha_total_pp = zill_rate × S
α(t)           = alpha_total_pp / zill_spread_y     if d(t) < zill_spread_y and premiums are due
               = 0                                  otherwise
α_z(t)         = alpha_zuz_rate × Z(t)
u(t)           = unit_cost_pp × (1 + expense_infl)^(t − 1)
N(t)           = ( P(t) + Z(t) ) × (1 − β) − α(t) − α_z(t) − u(t)
```

`N(t)` may be negative in the first years of a heavily zillmerised contract; that is correct and is
the reason a German *Deckungskapital* starts near zero. It is **not** floored, because there is no
*Rückkaufswert* for a floor to protect [R1] [R14].

### The Deckungskapital recursion

Per premium-paying policy, in the *Aufschubphase* (`t < T`):

```
Aᵖ(t, "BEF_PREM") = av_pp(t)
Aᵖ(t, "AFT_PREM") = Aᵖ(t, "BEF_PREM") + N(t)
Aᵖ(t, "AFT_INT")  = Aᵖ(t, "AFT_PREM") × ( 1 + i(t) − γ )
av_pp(t + 1)      = Aᵖ(t, "AFT_INT")
```

The premium-free block is carried at **fund level**, because a policy that froze at duration 5 and one
that froze at duration 15 hold different reserves and only the aggregate is meaningful:

```
Aᶠ(t, "BEF_PREM") = av_pu_at(t, "BEF_PREM")
Aᶠ(t, "AFT_PREM") = Aᶠ(t, "BEF_PREM") − u(t) × lᶠ(t)
Aᶠ(t, "AFT_INT")  = Aᶠ(t, "AFT_PREM") × ( 1 + i(t) − γ )
Aᶠ(t + 1)         = Aᶠ(t, "AFT_INT") × ( 1 − q(t) ) + pols_freeze(t) × Aᵖ(t, "AFT_INT")
```

A premium-free policy keeps paying the *Stückkosten* and the reserve charge and stops paying β and α,
which is the whole economic content of *Beitragsfreistellung*. The fund level closes:

```
A(t, timing) = Aᵖ(t, timing) × lᵖ(t) + Aᶠ(t, timing)
A(t + 1)     = A(t, "AFT_INT") × ( 1 − q(t) )
```

and that last line is `check_av_roll_fwd()`. It holds **whether or not** the survivor rider is on,
because the reserve of a policy terminated by death leaves the fund either way: as a claim where an
eligible survivor exists, as a mortality profit where none does. That single identity is the
arithmetic content of *nicht vererblich* [R1].

For `t ≥ T` the *Deckungskapital* is zero: the fund has become an annuity obligation.

### Decrements and the two policy ledgers

Death first, then the *Beitragsfreistellung* on survivors **[std]**:

```
pols_death_paying(t) = lᵖ(t) × q(t)
pols_death_paidup(t) = lᶠ(t) × q(t)
pols_death(t)        = pols_death_paying(t) + pols_death_paidup(t)
pols_freeze(t)       = lᵖ(t) × ( 1 − q(t) ) × f(t)          for t < T, else 0
lᵖ(t + 1)            = lᵖ(t) × ( 1 − q(t) ) × ( 1 − f(t) )
lᶠ(t + 1)            = lᶠ(t) × ( 1 − q(t) ) + pols_freeze(t)
l(t + 1)             = l(t) × ( 1 − q(t) )
```

The last line is the one to stare at: **`f(t)` does not appear in it**. A *Beitragsfreistellung* is a
transfer between the two ledgers, not an exit [R14], and `check_pols_roll_fwd()` asserts both that
`lᵖ + lᶠ = l` and that `l` decrements on mortality alone. The closure identity is therefore simply

```
Σ_{t=1..n} pols_death(t) + l(n + 1) = pols_if_init            with l(n + 1) = 0
```

because `mort_rate_at_age(omega_age, ·) = 1`.

### The conversion at Rentenbeginn

The conversion happens at the **start** of projection year `T`, on the fund carried out of year
`T − 1`, and it is the model's only single-date event:

```
fund_at_conv()          = av_at(T, "BEF_PREM") × ( 1 + σ )
rentenfaktor_applied()  = max( rentenfaktor_gtd , rf_curr(ret_age) ) × rf_option_factor()
rf_option_factor()      = factor("guarantee_period", G) × factor("survivor", s)
ann_pp(T)               = fund_at_conv() / pols_if(T) / rf_unit × rentenfaktor_applied() × ann_freq
```

with `rf_unit = 10 000` and `ann_freq = 12`. `ann_pp(T)` is the **cohort-average** annual annuity per
annuitant, which is exact at fund level even though the paying and premium-free cohorts arrive with
different per-policy reserves. `check_conversion()` inverts the identity:

```
check_conversion_resid(T) = ann_pp(T) × pols_if(T) × rf_unit / ( rentenfaktor_applied() × ann_freq )
                            − fund_at_conv()
```

and is zero at every other `t`. For a model point that opens in payment (`T ≤ 0`) the conversion never
occurs inside the projection, `ann_pp(1) = ann_pp_init`, and the check is vacuously true.

**The conversion basis is not the projection basis, and that is deliberate.** `rentenfaktor_gtd` was
struck at inception on **first-order** mortality with a prudential margin and a conservative interest
basis [R17] [S1]; the projection runs on the **second-order** best estimate. The wedge between them is
the *Risikoüberschuss* of the payout phase, and `ann_bonus_rate` is the mechanism that gives it back
to the annuitant. A model that converted on its own best-estimate mortality would abolish the wedge
and, with it, the whole German payout-phase surplus mechanic (pitfall 11).

### The annuity in payment, and the Rentengarantiezeit ledger

```
ann_pp(t)    = ann_pp_init                              if t = 1 and T ≤ 0
             = fund_at_conv() / l(T) / rf_unit × R × ann_freq       if t = T ≥ 1
             = ann_pp(t − 1) × ( 1 + b(t − 1) )         if t > max(1, T)
             = 0                                        otherwise
```

The *Rentengarantiezeit* runs `G` years from *Rentenbeginn*, so every continuation ends on the same
date, `gtd_end_t() = max(1, T) + G − 1`, which makes the ledger a one-line recursion:

```
g(t + 1) = 0                                            if t + 1 > gtd_end_t()
         = g(t) + pols_death(t) × π                     if t ≥ max(1, T) and G > 0
         = 0                                            otherwise
```

`π` is what makes this a Schicht-1 guarantee rather than a Schicht-3 one: the instalments continue
**only to an eligible survivor** [R1], and where none exists the payments simply cease. They are also
**never commutable** — `g(t)` is a stream, never a discounted lump sum (pitfall 14).

### Benefits and cash flows

```
db_pp(t)             = Aᵖ(t, "AFT_INT")                            per dying paying policy
db_pu_pp(t)          = Aᶠ(t, "AFT_INT") / lᶠ(t)                    per dying premium-free policy
claims(t, "DEATH")   = 1{s > 0} × 1{t < T} × π
                       × [ db_pp(t) × pols_death_paying(t) + db_pu_pp(t) × pols_death_paidup(t) ]
claims(t, "ANNUITY") = ann_pp(t) × l(t)                            for t ≥ max(1, T), else 0
claims(t, "SURVIVOR")= ann_pp(t) × g(t)                            the Rentengarantiezeit stream
expenses(t)          = acq_expense_pp × pols_if_init × 1{t = 1 and duration_init = 0}
                       + maint_expense_pp × (1 + expense_infl)^(t−1) × l(t)   for t < T
                       + annuity_admin_pp × (1 + expense_infl)^(t−1) × ( l(t) + g(t) ) for t ≥ T
commissions(t)       = comm_init_rate × S × pols_if_init × 1{t = 1 and duration_init = 0}
                       + comm_renew_rate × ( premiums(t) + zuzahlungen(t) )   for t ≥ 2
net_cf(t)            = premiums(t) + zuzahlungen(t)
                       − claims(t, "DEATH") − claims(t, "ANNUITY") − claims(t, "SURVIVOR")
                       − expenses(t) − commissions(t)
liability_cf(t)      = − net_cf(t)
```

**The death benefit is booked as a single amount and is not a lump sum to a beneficiary.** [R1]
requires everything paid to a survivor to be paid **as an annuity**; what the model books at the
moment of death is the *Deckungskapital* leaving this contract as the **single premium of a survivor's
annuity**, which is itself a new liability — an immediate annuity, delib product 7 — that this model
does not project. That is stated here rather than left to be inferred, because a reader who takes
`claims_death` for a payable lump sum has misread the product (pitfall 10).

Where the rider is on, the survivor's annuity fraction `s` reduces the *Rentenfaktor* through
`rf_option_factor()` rather than scaling the death benefit: the cover is paid for out of the annuity,
which is how a German tariff prices it.

### The published frame

`result_cf()` returns a `DataFrame` indexed by `t` (`df.index.name == "t"`), contiguous from `t = 1`
to `proj_len()`, with these columns **in this order**:

| # | Column | Content |
|---|---|---|
| 1 | `pols_if` | policies in force at the start of the year — the weight on this row |
| 2 | `pols_paying` | the premium-paying subset; the weight on the two premium columns |
| 3 | `av` | *Deckungskapital* at the start of the year, fund level — a **state variable, reported not summed** |
| 4 | `premiums` | *laufende Beiträge* |
| 5 | `zuzahlungen` | *Zuzahlungen*, kept separate because they are a distinct premium form on a distinct charge basis |
| 6 | `claims_death` | death benefits in the *Aufschubphase*; **structurally 0** where `surv_annuity_rate = 0` |
| 7 | `claims_annuity` | annuity instalments in the *Rentenphase* |
| 8 | `claims_survivor` | *Rentengarantiezeit* continuations; **structurally 0** where `guarantee_period_y = 0` |
| 9 | `expenses` | acquisition, maintenance and annuity administration |
| 10 | `commissions` | *Abschluss-* and *Bestandsprovision* |
| 11 | `net_cf` | income-positive |
| 12 | `liability_cf` | `−net_cf`, the orientation these notes print |

Columns 4 and 5 enter `net_cf` positively and 6 to 10 negatively; columns 1 to 3 are counts and a
balance, published because a reader cannot follow the projection without them, and named in
`check_net_cf()`'s docstring as excluded from the identity.

### The published checks

| Check | The identity it closes |
|---|---|
| `check_net_cf()` | `net_cf(t) = premiums + zuzahlungen − claims_death − claims_annuity − claims_survivor − expenses − commissions` at every `t`. **delib ruling 1**, mandatory on every model in the library |
| `check_pols_roll_fwd()` | `pols_paying(t) + pols_paidup(t) = pols_if(t)`, and `pols_if(t+1) = pols_if(t) × (1 − mort_rate(t))` — the *Beitragsfreistellung* rate does **not** appear |
| `check_av_roll_fwd()` | `av_at(t+1) = av_at(t, "AFT_INT") × (1 − mort_rate(t))` for `t < ret_t()`; `av_at(ret_t(), "AFT_INT") = 0`, the conversion having emptied the account; and `av(t) = 0` for every `t > ret_t()`. **`av(ret_t())` is not zero** — it is the pre-conversion fund the annuity is struck on, and it is what the `av` column publishes in the conversion year |
| `check_conversion()` | The whole fund converts exactly once, at `ret_t()`, at `rentenfaktor_applied()`; residual zero at every other `t` |
| `check_no_capital()` | The *nicht kapitalisierbar* invariant: no payment to the policyholder at any `t` other than an annuity instalment or a permitted survivor benefit; `claims_death = 0` wherever the rider is off and wherever `t ≥ ret_t()` |
| `check_annuity_roll_fwd()` | `ann_pp(t) = ann_pp(t−1) × (1 + ann_bonus_rate(t−1))` for `t > ret_t()`, and `pols_gtd(t) = 0` for `t > ret_t() + guarantee_period_y − 1` |

Each returns a `bool` over all `t` and has a per-`t` residual companion `check_*_resid(t)`, compared
against `roll_fwd_tol = 1e-9`.

---

## Annual processing order

For `t = 1 … n`, in exactly this order:

1. **Open the year.** Compute `age(t)`, `duration(t)`, `cal_year(t)`; determine the phase from
   `t < ret_t()` (*Aufschubphase*) or `t ≥ ret_t()` (*Rentenphase*).
2. **Open the ledgers.** `pols_paying(t)` and `pols_paidup(t)` from the previous year's recursion;
   `pols_if(t)` is their sum. Open the accounts at `"BEF_PREM"`: `av_pp_at(t, "BEF_PREM")` per paying
   policy and `av_pu_at(t, "BEF_PREM")` at fund level; `av_at(t, "BEF_PREM")` is the total.
3. **If `t = ret_t()`, convert.** Add the *Schlussüberschussanteil* to the fund carried out of year
   `t − 1`, strike `rentenfaktor_applied()`, set `ann_pp(t)`, and **zero the account** — from here on
   there is no *Deckungskapital* in this model. There is no lump sum, no election and no notice
   period [R1].
4. ***Aufschubphase* — take the premiums, in advance.** `prem_pp(t)` with its *Ratenzahlungszuschlag*,
   and `zuz_pp(t)` with its take-up. Weight both by `pols_paying(t)`.
5. ***Aufschubphase* — strike the charges and credit the account.** β on premium and *Zuzahlung*, the
   *Zillmerung* instalment α, the *Zuzahlung* acquisition charge α_z, the *Stückkosten* u; the residue
   `prem_to_av_pp(t)` goes to `av_pp_at(t, "AFT_PREM")`. The premium-free block pays only u.
6. **Charge the insurer's own expenses and commission.** Acquisition expense and initial commission at
   inception; maintenance expense per in-force policy; renewal commission on the year's premium and
   *Zuzahlung*; annuity administration per annuitant and per guarantee continuation in the payout
   phase.
7. ***Rentenphase* — pay the year's annuity.** Twelve monthly instalments booked at the start of the
   year on `pols_if(t)`, plus the *Rentengarantiezeit* stream on `pols_gtd(t)`.
8. **End of year — credit interest** (*Aufschubphase* only). `cred_rate(t) = max(gtd_rate,
   decl_rate(t))`, applied net of γ in one step to both blocks, giving `"AFT_INT"`.
9. **End of year — death.** `pols_death_paying(t)` and `pols_death_paidup(t)` on the opening counts.
   Where the survivor rider is on and `t < ret_t()`, book `claims(t, "DEATH")` as
   `elig_surv_prob ×` the released reserve; where it is off, the whole released reserve is a mortality
   profit and **nothing is paid**.
10. **End of year — *Beitragsfreistellung*.** `pols_freeze(t)` on the survivors of the death
    decrement, carrying `av_pp_at(t, "AFT_INT")` per policy from the paying block into the premium-free
    block. Zero in the *Rentenphase* and zero on a single-premium contract.
11. **Roll forward.** The two policy ledgers, the two account blocks, the *Rentengarantiezeit* ledger
    and, in the payout phase, the annuity: `ann_pp(t+1) = ann_pp(t) × (1 + ann_bonus_rate(t))`.
12. **Assemble.** `net_cf(t)` from the published parts; `liability_cf(t) = −net_cf(t)`.

At `t = n` the last survivor dies (`mort_rate(n) = 1`), `pols_if(n + 1) = 0`, and there is no tail
state, no maturity payment and nothing left to pay.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong; each becomes
a test.

1. **Carrying a surrender value across from the endowment or Schicht-3 chassis.** There is none, at
   any duration [R1] [R14] [REG-R28] [REG-R39]. Assert that `result_cf()` has no `claims_lapse`
   column, that no `cv_pp`, `surr_value_pp`, `loan_pp` or `lapse_rate` cells exists, and that
   `check_no_capital()` is `True` on every model point. The mirror error is subtler: computing a
   *Rückkaufswert* internally "for reference" and then floor**ing** the *Deckungskapital* at it, which
   changes the account in the early years even though nothing is ever paid.
2. **Treating *Beitragsfreistellung* as a lapse.** It removes the premium, not the policy [R14].
   Assert `pols_if(t+1) = pols_if(t) × (1 − mort_rate(t))` **exactly**, with `bf_rate` absent from the
   identity, and that a model point run with `bf_rate ≡ 0` has the same `pols_if` series as the base
   run while its `premiums` series is strictly larger from `t = 2`.
3. **Averaging the paying and premium-free account values into one per-policy figure.** They diverge
   from the first freeze, because one keeps receiving `prem_to_av_pp` and the other does not. Assert
   `av_pp(t) > av_pu_at(t, "BEF_PREM") / pols_paidup(t)` for every `t` after the first freeze on the
   anchor, and that `check_av_roll_fwd()` fails if the two blocks are collapsed.
4. **Double-counting a charge as an expense.** β, γ, the *Stückkosten* and the *Zillmerung*
   amortisation are **account deductions**, i.e. insurer income; the insurer's outgo is the acquisition
   expense, the commission, the maintenance expense and the annuity administration. Assert that
   `expenses(t)` is invariant to `beta_prem`, `gamma_av` and `zill_rate`, and that changing `gamma_av`
   moves `net_cf` **only** through the annuity that the smaller fund buys at `ret_t()`.
5. **Charging the whole *Zillmerung* in year one.** It is spread over `zill_spread_y = 5` premium-paying
   years **[std]** and capped at 25 ‰ of the *Beitragssumme* [R16] [REG-R16]. Assert
   `alpha_amort_pp(t)` is equal for `t = 1 … 5` and zero from `t = 6`, that
   `Σ_t alpha_amort_pp(t) = zill_rate × beitragssumme_pp()` to 1e-9, and that an in-force point past
   duration 5 (model point 6) sees `alpha_amort_pp(t) = 0` at every `t`.
6. **Stacking the declared rate on top of the guarantee.** A German *laufende Verzinsung* is the
   **total** credited rate, so `cred_rate(t) = max(gtd_rate, decl_rate(t))`, not `gtd_rate +
   decl_rate(t)` [R15] [R16]. Assert that on model point 8 (`gtd_rate = 2,75 %`, above the whole
   declared path) `cred_rate(t) = gtd_rate` at every `t`, while on the anchor it equals `decl_rate(t)`.
7. **Letting premiums or *Zuzahlungen* run past *Rentenbeginn*, or the *Dynamik* run off the policy
   duration.** Assert `prem_pp(t) = 0` and `zuz_pp(t) = 0` for every `t ≥ ret_t()`, that
   `zuz_pp(t) = 0` once `duration(t) ≥ zuzahlung_end_dur`, and that on an in-force point the
   *Beitragsdynamik* is keyed to `duration(t)` and not to `t` — model point 6, at `duration_init = 17`,
   must open at `prem_base_pp × 1.02^17`, not at `prem_base_pp`.
8. **Applying the *Ratenzahlungszuschlag* twice, or to the wrong thing.** It multiplies the *laufender
   Beitrag* only. Assert `prem_pp(t) / (prem_base_pp × (1+δ)^d(t)) = φ` exactly at every `t`, that
   `zuz_pp(t)` is invariant to `prem_mode`, and that a single-premium point carries `φ = 1`.
9. **Paying a death benefit with the rider off.** Death before *Rentenbeginn* pays **nothing** in the
   base design; the reserve is released as a mortality profit [R1] [REG-R39]. Assert
   `claims_death(t) == 0.0` at every `t` on every model point with `surv_annuity_rate == 0`, including
   the anchor, and that `check_av_roll_fwd()` still closes — the released reserve leaves the fund
   whether or not anything is paid.
10. **Paying the death benefit to the estate, or as a lump sum.** With the rider on it is payable only
    where an **eligible survivor** exists and must buy an **annuity** [R1]. Assert
    `claims_death(t) = elig_surv_prob × av_at(t, "AFT_INT") × mort_rate(t)` on model point 3, that
    setting `elig_surv_prob = 0` reproduces the rider-off run cash flow for cash flow, and that the
    model publishes no lump-sum column of any kind.
11. **Converting on the projection's own mortality.** The *Rentenfaktor* is a **contractual** rate
    struck on first-order bases [R17] [S1]; the projection runs on the best estimate. Assert
    `ann_pp(ret_t())` is invariant to `mort_be_factor` while `claims_annuity` is not, so that the wedge
    between the two bases shows up as payout-phase margin rather than being silently removed.
12. **Booking the annuity as one payment a year at the wrong end of the year.** The annuity is
    **monthly in advance** [R1]; the model books twelve instalments at the **start** of the payout
    year on `pols_if(t)` **[std]**, so a life that dies during the year has been paid for the whole of
    it. That is a stated approximation, not an accident (gap 21). Assert
    `claims_annuity(t) = ann_pp(t) × pols_if(t)` exactly, and that switching to an end-of-year booking
    is a documented variant rather than the base.
13. **Taking the guaranteed *Rentenfaktor* when the current one is higher, or the reverse.** The rule
    is `max(garantiert, aktuell)` [R17] [S1]. Assert the anchor converts at `rf_curr(67)` and model
    point 13 at `rentenfaktor_gtd`, and that `rentenfaktor_applied()` is monotone in both inputs.
14. **Getting the *Rentengarantiezeit* wrong in either of two ways.** It runs `G` years **from
    *Rentenbeginn***, not from each death, and it pays **only to an eligible survivor** and is **never
    commutable** [R1]. Assert `pols_gtd(t) = 0` for every `t > ret_t() + guarantee_period_y − 1` on
    model point 4, that `pols_gtd` is monotone non-decreasing inside the window, and that no cash flow
    anywhere discounts a continuation into a lump sum.
15. **Using a period table where the basis is generational.** DAV 2004 R is a *Generationentafel* and
    the improvement lives inside it [R17] [REG-R49]. Assert
    `mort_rate_at_age(x, y2) < mort_rate_at_age(x, y1)` for `y2 > y1` at every age, and that two model
    points at the same attained age but different `conclusion_year` — 6 and 9 both reach age 60 — see
    different `mort_rate`.
16. **Applying today's *Höchstrechnungszins* to an in-force contract.** The rate attaches at
    conclusion and stays with the contract [REG-R14] [REG-R15]. Assert that the shipped model points
    carry four distinct `gtd_rate` values and that `cred_rate(t) ≥ gtd_rate` at every `t` on every
    point.
17. **Modelling the BUZ as premium income with no benefit.** `prem_base_pp` is the **old-age**
    contribution; the BUZ premium and the *BU-Rente* belong to `BU_DE_S`. Assert `buz_prem_share < 0.50`
    for every model point [R1], that `prem_total_pp(t) > prem_pp(t) + zuz_pp(t)` exactly where
    `buz_prem_share > 0`, and that `prem_total_pp` appears in **no** `result_cf()` column and in
    `net_cf` at no `t`.

---

## Policyholder behaviour modelling

All formulas here are **[std]** reference constructions; there is no German calibration evidence for
any of them, and the research file records the absence as gap 3.

- **The exit.** This product has **one** behavioural exit and it pays nothing: the
  *Beitragsfreistellung* [R14]. `bf_rate(dur)` is a duration table — 4,0 % / 3,0 % / 2,0 % — whose
  **shape** is argued from the product's structure (an income-volatile buyer, a penalty-free and
  reversible option early; nothing realisable to leave for, late) and whose **levels** are invented.
  There is no dynamic component, because there is no competing product a Basisrente holder can move to
  and no cash to move.
- **What a *Beitragsfreistellung* does and does not do.** It stops the premium and moves the policy to
  the premium-free cohort. It does **not** end the contract, release any value, change the
  *Rentenbeginn* or release any of the § 10 constraints: a paid-up Basisrente is still certified,
  still protected, still payable only as an annuity [R1] [R9] [R14]. **No *Wiederinkraftsetzung*** is
  modelled — premiums can in practice be resumed within a window [R14], but none was established
  (gap 8), so the premium-free block is absorbing, which is conservative on premium income.
- **The *Zuzahlung* take-up** is the second behavioural assumption and the more distinctive one. The
  contribution the tax ceiling makes possible is paid out of a profit not known until the year end, so
  `zuz_take_up(dur)` is a **utilisation rate**, not a contract term: 0.70 early, 0.85 in mid-term,
  0.90 late. A model that treats the *Zuzahlung* as contractual has hard-coded an assumption.
- **Selection on the annuitant pool is not modelled, and the direction is known.** A Basisrente cannot
  be surrendered or commuted, so a policyholder in poor health has no exit and nobody leaves the pool —
  which argues for **lighter** mortality than a comparable Schicht-3 portfolio, where the
  *Kapitalwahlrecht* lets an impaired life leave [R17]. **No evidence for this was found**; it is a
  **[std]** view and a stated model risk, and `mort_be_factor` is the single lever that would carry it.
- **No dynamic annuitisation behaviour, because there is none to model**: no *Kapitalwahlrecht*, no
  *Teilkapitalauszahlung*, no *Kleinbetragsrenten-Abfindung*, no election of any kind at *Rentenbeginn*
  [R1] [R23]. The Schicht-3 chassis needs a take-up assumption and a declaration window; this product
  needs neither, which is the cleanest simplification the layer buys. Deferral of *Rentenbeginn* is
  likewise a model-point input rather than a behaviour: no carrier's permitted range was established
  (gap 8), and model point 12 exercises a deferral to 70 as a configuration.

---

## Worked example

**Configuration.** Model point 1, the anchor cell, exactly as shipped in `model_point_table.csv`:
`point_id = 1`; `policy_id = DE-BAS-0001`; `sex = M` (reporting only; pricing is unisex [REG-R34]);
`entry_age = 45`; `conclusion_year = 2026`; `duration_init = 0`; `ret_age = 67`;
`pols_if_init = 1.0`; `prem_form = regular`; `prem_base_pp = 6,000.00 €` p.a.; `prem_mode = annual`,
so `prem_freq_load = 1.000`; `prem_dyn_rate = 0.02`; `zuzahlung_pp = 4,000.00 €` p.a.;
`zuzahlung_end_dur = 22`; `paidup_at_init = 0`; `av_pp_init = 0.00 €`; `ann_pp_init = 0.00 €`;
`gtd_rate = 0.0100`; `rentenfaktor_gtd = 28.00 €` per month per 10 000 €; `guarantee_period_y = 0`;
`surv_annuity_rate = 0.00`, so the survivor rider is **off** and `claims_death(t) = 0` at every `t`;
`buz_prem_share = 0.00`; `tariff_id = de_basis_std`; `beh_table_id = base`;
`surplus_scenario_id = base`; `rf_scenario_id = base`. Hence `age(1) = 45`,
`ret_t() = 67 − 45 + 1 = 23`, `omega_age() = 121` and `proj_len() = 121 − 45 + 1 = 77`: twenty-two
years of *Aufschubphase* at attained ages 45 to 66, then fifty-five years of *Rentenphase* at attained
ages 67 to 121. The table below therefore shows **selected rows** — every year of the first five, the
years in which a lever changes, the conversion year and its neighbours, and a decade sample of the
payout phase — together with full-precision totals over all seventy-seven.

**Assumptions, each tagged.** *Mortality*: the shipped `mort_table.csv` is a **[std]** DAV 2004
R-shaped **first-order** proxy, anchored so that `mort_rate_at_age(67, 2005) = 0.014000` exactly, with
a flat improvement `trend = 0.015` at every age applied from `mort_base_year = 2005`, so that
`mort_rate_base(t) = qx(age(t)) × (1 − 0.015)^(cal_year(t) − 2005)`; the best-estimate factor is
`mort_be_factor = 0.85` **[std]**, giving `mort_rate(t) = 0.85 × mort_rate_base(t)`. The real basis is
**DAV 2004 R**, which is the property of the Deutsche Aktuarvereinigung and is **cited by name and
never shipped** [R17] [REG-R47] [REG-R49]; a replacement must preserve the generational structure, the
first-order margin and the *Altersverschiebung* convention, and must reproduce the anchor above if the
worked example is to close. *Interest*: `gtd_rate = 1.00 %` p.a., the *Höchstrechnungszins* for new
business from 1 January 2025 [R16] [REG-R14] [REG-R15]; declared `decl_rate(t) = 2.60 %` for
`t = 1…10`, `2.40 %` for `t = 11…20`, `2.20 %` for `t ≥ 21` **[std]**, so
`cred_rate(t) = max(0.0100, decl_rate(t)) = decl_rate(t)` throughout and the guarantee never binds on
this cell. *Surplus at and after conversion*: `terminal_bonus_rate = 4.0 %` of the fund at
*Rentenbeginn* **[std]**, allocated at that single date because the contract has no earlier exit
trigger [R15]; `ann_bonus_rate(t) = 1.0 %` p.a. compounding **[std]**, a *teildynamische Rente*.
*Conversion*: `rf_curr(67) = 31.50 €` in scenario `base` **[std]** against the guaranteed 28,00 €
**[std]**, so `rentenfaktor_applied() = max(28.00, 31.50) × 1.000 = 31.50` — the **current** factor
binds on this cell, and model point 13 exercises the other branch [R17] [S1]. *Charges*:
`zill_rate = 25 ‰` of the *Beitragssumme* [R16] [REG-R16] [REG-R20], amortised over
`zill_spread_y = 5` years **[std]**; `alpha_zuz_rate = 2.5 %` of each *Zuzahlung* **[std]**;
`beta_prem = 7.5 %` **[std]**; `gamma_av = 0.35 %` p.a. **[std]**; `unit_cost_pp = 36.00 €` p.a.
inflating at `expense_infl = 1.5 %` **[std]**. *Insurer expense and commission*, all **[std]**:
`acq_expense_pp = 250.00 €` at inception; `comm_init_rate = 2.5 %` of `beitragssumme_pp()` at
inception; `comm_renew_rate = 1.5 %` of premiums plus *Zuzahlungen* from `t = 2`;
`maint_expense_pp = 60.00 €` per in-force policy p.a. inflating; `annuity_admin_pp = 36.00 €` per
annuitant p.a. inflating. *Behaviour*, all **[std]**: `bf_rate = 4.0 %` at durations 1–5, `3.0 %` at
6–10, `2.0 %` at 11+; `zuz_take_up = 0.70` at durations 1–5, `0.85` at 6–15, `0.90` at 16+;
`elig_surv_prob = 0.55`, which is **inert on this cell** because the survivor rider is off and is
carried only so that model points 3 and 12 can exercise it. No BUZ, no *Rentengarantiezeit*, no
survivor's annuity, no provider transfer, no *Wiederinkraftsetzung*.

All amounts in euros; `pols_if`, `pols_paying` and `av` to the precision shown; cash flows to the
cent. The **Total** row is summed at full precision and then rounded, which is not in general the same
as adding the rounded cells.

### The frame

Selected rows of `Projection[1].result_cf()`, transcribed from the model's own output. The two
columns not shown — `claims_death` and `claims_survivor` — are **structurally zero at every one of
the seventy-seven years** on this cell, because the survivor rider is off and there is no
*Rentengarantiezeit*; they are published as zero columns rather than dropped, because a column of
zeros states the product fact where a missing column would only hide it. `liability_cf` is omitted
for the same reason it is trivial: it is `−net_cf` to the last bit.

`pols_if`, `pols_paying` and `av` are a count, a count and a balance. They are **reported and not
summed**, which is why the Total row carries an em dash for all three.

| t | age | `pols_if` | `pols_paying` | `av` | `premiums` | `zuzahlungen` | `claims_annuity` | `expenses` | `commissions` | `net_cf` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 45 | 1.000000 | 1.000000 | 0.00 | 6,000.00 | 2,800.00 | 0.00 | 310.00 | 4,094.85 | 4,395.15 |
| 2 | 46 | 0.998560 | 0.958618 | 7,366.75 | 5,866.74 | 2,684.13 | 0.00 | 60.81 | 128.26 | 8,361.80 |
| 3 | 47 | 0.997024 | 0.918857 | 14,688.72 | 5,735.87 | 2,572.80 | 0.00 | 61.63 | 124.63 | 8,122.42 |
| 4 | 48 | 0.995385 | 0.880653 | 21,968.46 | 5,607.33 | 2,465.83 | 0.00 | 62.45 | 121.10 | 7,889.61 |
| 5 | 49 | 0.993635 | 0.843941 | 29,208.23 | 5,481.05 | 2,363.03 | 0.00 | 63.28 | 117.66 | 7,663.15 |
| 6 | 50 | 0.991769 | 0.808662 | 36,410.00 | 5,356.97 | 2,749.45 | 0.00 | 64.11 | 121.60 | 7,920.71 |
| 11 | 55 | 0.980403 | 0.686467 | 78,013.70 | 5,020.79 | 2,333.99 | 0.00 | 68.27 | 110.32 | 7,176.19 |
| 16 | 60 | 0.964766 | 0.610615 | 119,589.52 | 4,930.84 | 2,198.21 | 0.00 | 72.37 | 106.94 | 6,949.75 |
| 21 | 65 | 0.943366 | 0.539704 | 162,771.09 | 4,811.83 | 1,942.94 | 0.00 | 76.23 | 101.32 | 6,577.21 |
| 22 | 66 | 0.938235 | 0.526033 | 171,114.15 | 4,783.75 | 1,893.72 | 0.00 | 76.96 | 100.16 | 6,500.35 |
| **23** | **67** | 0.932780 | 0.512516 | **179,426.24** | 0.00 | 0.00 | **7,053.60** | 46.59 | 0.00 | −7,100.20 |
| 24 | 68 | 0.926985 | 0.509331 | 0.00 | 0.00 | 0.00 | 7,079.88 | 47.00 | 0.00 | −7,126.88 |
| 33 | 77 | 0.856165 | 0.470419 | 0.00 | 0.00 | 0.00 | 7,151.60 | 49.63 | 0.00 | −7,201.23 |
| 43 | 87 | 0.724266 | 0.397948 | 0.00 | 0.00 | 0.00 | 6,682.78 | 48.73 | 0.00 | −6,731.51 |
| 53 | 97 | 0.521776 | 0.286689 | 0.00 | 0.00 | 0.00 | 5,318.10 | 40.74 | 0.00 | −5,358.84 |
| 63 | 107 | 0.272931 | 0.149962 | 0.00 | 0.00 | 0.00 | 3,072.84 | 24.73 | 0.00 | −3,097.57 |
| 73 | 117 | 0.074193 | 0.040765 | 0.00 | 0.00 | 0.00 | 922.70 | 7.80 | 0.00 | −930.50 |
| 77 | 121 | 0.032209 | 0.017697 | 0.00 | 0.00 | 0.00 | 416.84 | 3.60 | 0.00 | −420.43 |
| **Total** | | — | — | — | **113,761.91** | **51,236.28** | **270,016.08** | **3,731.36** | **6,437.82** | **−115,187.08** |

**The Total row is summed over all seventy-seven years at full precision and then rounded**, which
is not in general the same as adding the rounded cells. Here it differs in three of the six money
columns: adding the seventy-seven rounded `claims_annuity` cells gives 270 016,09 € against
270 016,08 €, the rounded `expenses` cells 3 731,38 € against 3 731,36 €, and the rounded
`commissions` cells 6 437,83 € against 6 437,82 €. `premiums`, `zuzahlungen` and `net_cf` happen to
agree at the cent. The differences are one and two cents and they are not errors; they are what
rounding seventy-seven times before adding costs, and a test that asserted the sum of the printed
cells would be asserting the wrong number.

Four things in the frame are worth reading before the checks below.

- **Year 1's strain is the commission, not the *Zillmerung*.** The 818,97 € instalment is a
  deduction from the policyholder's account and hence insurer income; it is absent from `expenses`
  and visible only in `av(2)` being 7 366,75 € rather than the 8 140,00 € that 8 800,00 € less the
  7,5 % premium charge would otherwise have bought.
- **`pols_paying` falls far faster than `pols_if`.** By `t = 23` the in-force count has fallen only
  to 0,932780 while the premium-paying count has fallen to 0,512516: 0,441765 of the cohort has
  passed through a *Beitragsfreistellung* by then, and the 0,420265 of it that has not since died
  is sitting in the premium-free ledger, where it is still in force, still credited and still
  converts. Not one policy has left through a surrender, there being none to leave through.
- **The `av` column ends at `t = 23` and does not taper.** The whole fund converts in one step;
  from `t = 24` there is no *Deckungskapital* in this model, only an annuity obligation that a
  *Deckungsrückstellung* stands behind and that delib does not compute.
- **The annuity rises and the claim falls.** `ann_pp(t)` compounds at 1,0 % — 7 561,91 €,
  7 637,53 €, 7 713,91 € — while `claims_annuity(t)` peaks at `t = 31` and then falls away as
  mortality outruns the *Überschussrente*. Nothing is paid at `t = 77`: the last survivor dies at
  the terminal age, and there is no maturity value and no tail state.

### Three independent checks and a closure identity

Each of these rebuilds a cell of the table a different way, in arithmetic that can be followed with
a calculator. They are what makes this example a check rather than a printout.

**Check 1 — the first year's account, from the charge scale up.** The *Beitragssumme* is the sum of
twenty-two escalating premiums,

```
S = 6,000.00 x (1.02^22 - 1) / 0.02 = 6,000.00 x 27.2989835388 = 163,793.9012327640
```

so the zillmerised acquisition charge is `0.025 x S = 4,094.8475308191` and its annual instalment
`alpha(1) = 4,094.8475308191 / 5 = 818.9695061638`. The *Zuzahlung* actually paid is
`4,000.00 x 0.70 = 2,800.00` — the take-up at policy years 1 to 5 — and it carries its own 2,5 %
charge rather than a share of the *Zillmerung*. So

```
N(1) = (6,000.00 + 2,800.00) x (1 - 0.075) - 818.9695061638 - 0.025 x 2,800.00 - 36.00
     = 8,140.00 - 818.9695061638 - 70.00 - 36.00
     = 7,215.0304938362
```

and crediting it at the declared 2,60 % net of the 0,35 % reserve charge,

```
A^p(1, "AFT_INT") = 7,215.0304938362 x (1 + 0.026 - 0.0035) = 7,377.3686799475
```

The table's `av` at `t = 2` is 7 366,75 €, which is **not** that number: it is that number after the
year's death decrement, `7,377.3686799475 x (1 - 0.0014396389) = 7,366.7479330812`. That is the
fund-level roll-forward `check_av_roll_fwd()` closes, and the fact that it closes with `bf_rate` at
4 % is the point — a *Beitragsfreistellung* moves reserve between the two blocks and removes none.

**Check 2 — the year-1 decrement split, and the rate behind it.** The shipped table's rate at age
45 is `0.014000 x 1.085^(45 - 67) = 0.0023263433`, improved from the 2005 base to the 2026 calendar
year by `(1 - 0.015)^21 = 0.7280493868`, giving a first-order `0.0016936928`; the best-estimate
factor takes it to `q(1) = 0.85 x 0.0016936928 = 0.0014396389`. Then

```
pols_death(1)  = 1.000000 x 0.0014396389                    = 0.0014396389
pols_freeze(1) = 1.000000 x (1 - 0.0014396389) x 0.04       = 0.0399424144
pols_paying(2) = 1.000000 x (1 - 0.0014396389) x (1 - 0.04) = 0.9586179467
pols_paidup(2) = 0.0000000000 + 0.0399424144                = 0.0399424144
pols_if(2)     = 0.9586179467 + 0.0399424144                = 0.9985603611
```

and `0.9985603611 = 1.000000 - 0.0014396389` exactly. **The 4 % *Beitragsfreistellung* rate has
cancelled out of `pols_if` entirely**, which is what distinguishes this product's decrement
structure from a Schicht-3 annuity's and is what `check_pols_roll_fwd()` asserts at every `t`.

**Check 3 — the conversion, and the branch of the `max` that binds.** The fund at the start of year
23 is 179 426,2405488701 €; the *Schlussüberschussanteil* grosses it up once, at this single date,

```
F = 179,426.2405488701 x 1.04 = 186,603.2901708250
```

and it is shared over the 0,932780 policies still in force, giving 200 050,6219643070 € per
annuitant. The applied *Rentenfaktor* is `max(28.00, 31.50) x 1.000 = 31.50` — the **current**
factor binds on this cell — and 31,50 € a month per 10 000 € of capital is 378,00 € a year, so

```
ann_pp(23) = 200,050.6219643070 / 10,000 x 378.00 = 7,561.9135102508
```

The table's `claims_annuity(23)` is that annuity weighted by the opening in-force count,
`7,561.9135102508 x 0.9327803550 = 7,053.6043684572`, and the next year's is the same annuity
compounded once and re-weighted, `7,561.9135102508 x 1.01 x 0.9269849437 = 7,079.8777690934`. Had
the guaranteed 28,00 € bound instead the annuity would have been 6 721,70 €, 11,1 % lower.

**Closure identity — the decrements sum to one, and the cash flow statement closes.** Over the
whole projection,

```
sum_{t=1..77} pols_death(t) + pols_if(78) = 1.0000000000 + 0.0000000000 = 1.0000000000
```

because the terminal age is absorbing. Not one policy leaves by any other route: there is no lapse
decrement, no surrender and no commutation on this product, and the 0,441765 of the cohort that
went *beitragsfrei* is inside that 1,000000 rather than beside it. And on the money side, the Total
row itself closes,

```
113,761.9053943146 + 51,236.2751085046 - 270,016.0832025837 - 3,731.3612934038 - 6,437.8202383614
    = -115,187.0842315298
```

which is `check_net_cf()` — delib's first ruling — evaluated over all seventy-seven years at once
rather than one year at a time. A last arithmetic coincidence that is not a coincidence:
`commissions(1) = 0.025 x S = 4,094.8475308191` is **the same number** as
`alpha_total_pp() = 0.025 x S`, because the initial commission rate and the *Höchstzillmersatz* are
both 2,5 %. That is the German design rather than an accident — what the insurer pays out at
inception is sized to what it may write into the reserve — and it is why moving `comm_init_rate`
without moving `zill_rate` opens a hole in the first year that nothing closes.

### The variant: the *Einmalbeitrag* (model point 5)

The notes' model point table promises a second premium form, and this is it: model point 5, a
58-year-old paying a single 60 000,00 € *Einmalbeitrag* and deferring to 67, on the same tariff,
behaviour and surplus scenario as the anchor. `prem_form = single`, so `prem_freq_load() = 1.000`
— a single payment carries no *Ratenzahlungszuschlag* — `bf_rate(t) = 0` at every `t`, there being
no premium left to stop, and `ret_t() = 10`, `proj_len() = 64`.

| t | age | `pols_if` | `av` | `premiums` | `claims_annuity` | `expenses` | `commissions` | `net_cf` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 58 | 1.000000 | 0.00 | 60,000.00 | 0.00 | 310.00 | 1,500.00 | 58,190.00 |
| 2 | 59 | 0.995842 | 56,170.68 | 0.00 | 0.00 | 60.65 | 0.00 | −60.65 |
| 3 | 60 | 0.991418 | 56,838.16 | 0.00 | 0.00 | 61.28 | 0.00 | −61.28 |
| 5 | 62 | 0.981702 | 58,157.41 | 0.00 | 0.00 | 62.52 | 0.00 | −62.52 |
| 9 | 66 | 0.958317 | 61,584.00 | 0.00 | 0.00 | 64.77 | 0.00 | −64.77 |
| **10** | **67** | 0.951537 | **62,484.63** | 0.00 | **2,456.40** | 39.17 | 0.00 | −2,495.56 |
| 11 | 68 | 0.944341 | 0.00 | 0.00 | 2,462.20 | 39.45 | 0.00 | −2,501.65 |
| 20 | 77 | 0.857193 | 0.00 | 0.00 | 2,444.36 | 40.95 | 0.00 | −2,485.31 |
| 40 | 97 | 0.468265 | 0.00 | 0.00 | 1,629.32 | 30.13 | 0.00 | −1,659.45 |
| 64 | 121 | 0.014921 | 0.00 | 0.00 | 65.92 | 1.37 | 0.00 | −67.29 |
| **Total** | | — | — | **60,000.00** | **86,163.14** | **2,321.22** | **1,500.00** | **−29,984.36** |

Again summed at full precision and then rounded; adding the sixty-four rounded `net_cf` cells gives
−29 984,39 € against −29 984,36 €, a three-cent difference.

Two features are the whole point of the variant. **The *Beitragssumme* of a single-premium contract
is the single premium**, so `S = 60,000.00`, the *Zillmerung* is `0.025 x 60,000.00 = 1,500.00` and
the initial commission is the same 1 500,00 € — an order of magnitude below the anchor's, because
the anchor's twenty-two escalating premiums sum to 163 793,90 €. And **the five *Zillmerung*
instalments still run**, 300,00 € a year at `t = 1 ... 5`, so from `t = 2` the account is debited by
an acquisition charge that the one premium has already come and gone without covering. That is
visible in the first year's account, which checks in one line:

```
N(1)      = 60,000.00 x (1 - 0.075) - 300.00 - 0.00 - 36.00 = 55,164.0000000000
av_pp(2)  = 55,164.0000000000 x (1 + 0.026 - 0.0035)        = 56,405.1900000000
av(2)     = 56,405.1900000000 x 0.9958424243                = 56,170.6811550510
```

the last line being the fund-level value the table publishes — `av_pp` is per **paying** policy and
`av` is at fund level, and on this cell the two differ only by the death decrement, because there
is no premium-free block at all.

### The other branch of the *Rentenfaktor* (model point 13)

Pitfall 13 promises a cell on which the guaranteed factor binds, and model point 13 is it: the same
6 000,00 € annual premium as the anchor, no *Dynamik*, no *Zuzahlung*, entry at 46 and
`rf_scenario_id = low`, so that `rentenfaktor_curr()` is 27,72 € against a guaranteed 34,00 €.

| Cell | `av(T)` | `fund_at_conv()` | per annuitant | `rentenfaktor_gtd` | `rentenfaktor_curr()` | applied | `ann_pp(T)` |
|---|---:|---:|---:|---:|---:|---:|---:|
| Anchor, `T = 23` | 179,426.24 | 186,603.29 | 200,050.62 | 28.00 | 31.50 | **31.50** | **7,561.91** |
| Point 13, `T = 22` | 98,185.81 | 102,113.25 | 109,428.02 | 34.00 | 27.72 | **34.00** | **4,464.66** |

On the anchor the guarantee is worth nothing and would have given 6 721,70 €; on model point 13 it
is worth 824,65 € a year, the current factor alone giving 3 640,01 €. The projection is sensitive to
whichever factor is higher and **completely insensitive to the other**, which is why a sensitivity
run on the guaranteed *Rentenfaktor* over a whole book returns zero until it crosses the current
one and then moves in a straight line.

### What changed in these notes when the model was built

The specification above was written before the model existed. Building it settled eight points the
prose had left ambiguous or got wrong; each was resolved in favour of the arithmetic that closes and
each is now written into the notes at its source rather than only here.

1. **The terminal age is absorbing.** The horizon bullet asserted `mort_rate_at_age(omega, ·) = 1`,
   but the generational trend carries the table's terminal rate below 1 in every calendar year after
   the base year and `mort_be_factor` would take it to 0,85 in any case. The rule now sits on
   `mort_rate(t)`, where it belongs.
2. **`av(ret_t())` is the pre-conversion fund, not zero.** `check_av_roll_fwd()` now asserts
   `av_at(ret_t(), "AFT_INT") = 0` — the conversion empties the account — and `av(t) = 0` for every
   `t > ret_t()`. The old wording would have hidden the one number the conversion is struck on.
3. **The acquisition expense is a fund-level amount**, `acq_expense_pp × pols_if_init × 1{…}`,
   matching the initial commission beside it. Nothing moves on the shipped points, all of which
   carry `pols_if_init = 1.0`.
4. **`omega_age_max` is not a Reference.** `omega_age()` is read off the last row of
   `mort_table.csv` and needs no separate cap, so the name is dropped from the scalar list.
5. **`zuz_take_up(t)` is published as a cells**, alongside `bf_rate(t)`: pitfall 7 turns on it, and
   hiding it inside `zuz_pp` would have made it untestable.
6. **`behaviour_table.csv` is keyed by the policy year**, `duration(t) + 1`, so the notes'
   "durations 1–5" reads off the file directly. `duration(t)` itself stays **completed** policy
   years and is 0 in the first projected year of a new-business point.
7. **Model point 9 carries no *Zuzahlung*.** It exists to sit at the whole *Höchstbetrag*, and a
   top-up above a contribution that already consumes the ceiling would model relief the deduction
   could not absorb. `zuzahlung_pp` is exercised by points 1, 3 and 11.
8. **The guaranteed *Rentenfaktor* binds on two cells, not one.** Model point 6 is a 2009 tariff
   converting at 60, and an older tariff's guaranteed factor standing above today's current factor
   at that age is the realistic case rather than a contrivance.

Nothing in the shipped model contradicts a cited fact. Every figure in the tables above is the
model's own output, and every parameter behind them is **[std]** except the 25 ‰ *Höchstzillmersatz*
[R16] [REG-R16] and the 1,00 % *Rechnungszins* [R16] [REG-R15].

---

## Valuation and reserve pointers

This library projects **gross best-estimate-style liability cash flows, undiscounted**, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The German statutory *Deckungsrückstellung*.** An HGB reserve of § 341f HGB [REG-R54], computed on
  the *Rechnungsgrundlagen* the DeckRV fixes [REG-R14]: the contract's own *Rechnungszins* — capped at
  the *Höchstrechnungszins* in force at conclusion and fixed for the whole term [REG-R15] — and
  first-order DAV 2004 R [REG-R49], with acquisition costs entering through the *Zillmerung* of
  § 4 DeckRV [REG-R16]. The model's `av_at(t, ·)` and, after conversion, the annuity obligation
  `ann_pp(t) × pols_if(t)` are what a *Deckungsrückstellung* stands behind; **neither is a reserve and
  delib computes none**.
- **The *Zinszusatzreserve*.** The additional HGB reserve arising where the *Referenzzins* of
  § 5 Abs. 3 DeckRV falls below a contract's tariff rate [REG-R17]. It exists in no other jurisdiction
  in this repository and bites hardest on annuity business, because the § 12 MindZV test looks at the
  highest *Rechnungszins* applicable over the next fifteen years [REG-R18]. **A long-dated Basisrente
  is exactly the business it bites on**, and nothing here represents it.
- ***Überschussbeteiligung* and the MindZV floor.** The credited rate here is a **[std]** scenario, not
  a derivation: a real declaration runs through the four surplus sources, the MindZV 90 / 90 / 50 floor
  [REG-R18], the RfBV [REG-R19] and the § 139 VAG *Sicherungsbedarf* test [REG-R9]. Making the
  declaration endogenous would need the insurer's whole HGB result — a fund model, not a policy model.
- **Solvency II.** Technical provisions are a best estimate — the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure — plus a risk margin
  [REG-R1] [REG-R2] [REG-R6], with EIOPA publishing the curves monthly [REG-R4].
  `BEL = Σ_t v(t) × liability_cf(t)` over the recursions above. **No cost-of-capital rate,
  contract-boundary rule or standard-formula shock anywhere in this library was read from a retrieved
  instrument**, so every such figure would be **[std]** [REG-R2].
- **Contract boundary.** The premium is contractually variable — the *Beitragsdynamik* may be declined
  and the *Zuzahlung* is discretionary — which raises a boundary question this library does not
  resolve: whether the projected *Zuzahlungen* and *Dynamik* increments fall inside the contract
  boundary at all. The model projects the whole stream and publishes it; a boundary-truncated view is
  obtained by zeroing `zuzahlung_pp` and `prem_dyn_rate` on the model point, not by editing formulas.
- **IFRS 17.** A profit-participating Basisrente is a direct-participating contract that would be
  measured under the variable fee approach [REG-R55]; the same expected-cash-flow engine feeds it, and
  grouping, CSM and risk adjustment are out of scope.
- **The guarantees are options and this model prices none of them.** The guaranteed *Rechnungszins* is
  a written floor on the credited rate; the guaranteed *Rentenfaktor* is a written option on the
  annuity conversion, and on **this** product it is worth materially more than on its Schicht-3 sibling
  because the policyholder has no *Kapitalwahlrecht* to fall back on [R1] [R17]. A deterministic path
  prices neither. A stochastic-on-deterministic run — the crediting rule and the `max(gtd, curr)`
  conversion re-evaluated per scenario — is what a time-value-of-options-and-guarantees calculation
  consumes.

---

## Key sensitivities and model risks

In rough order of leverage for a German Schicht-1 block:

1. **The *Rentenfaktor*.** It converts the entire accumulated fund into the entire payout-phase
   liability, so it is the single largest lever in the model — and **no *Rentenfaktor* level, range or
   time series exists anywhere in the delib corpus, for this or any product** (gap 4). Both the
   guaranteed 28,00 € and the current 31,50 € are **[std]**, and the `max` of the two means the
   projection is sensitive to whichever is higher and completely insensitive to the other. Model point
   13 exists to make that discontinuity visible.
2. **The conversion-basis wedge.** The fund is converted on a **first-order** *Rentenfaktor* and then
   run off on **second-order** mortality, so the payout phase carries a structural margin that
   `ann_bonus_rate` gives back. Both levers are **[std]** independently, so the payout phase's
   profitability here is an artefact of two unanchored numbers rather than a result — the most
   important thing to understand before quoting any figure from it.
3. **Mortality level and the generational trend.** A 1,5 % annual improvement compounded over a
   22-year deferment and a 40-year payout is worth far more than it looks, and the trend is flat across
   ages here where DAV 2004 R's own are not [REG-R49] — the more dangerous of the two on a long run.
4. **The *Beitragsfreistellung* rate.** It governs how much premium is ever collected and how large
   the premium-free block grows, and on this product it is the **only** behavioural exit. The base
   table takes about a third of the cohort out of premium payment before *Rentenbeginn*; nothing in
   the corpus supports any level (gap 3).
5. **The declared surplus path.** A 20 bp difference in `decl_rate` compounded over the anchor's
   22-year deferment moves the fund at conversion by several per cent, and the annuity with it. The
   path is a scenario and is labelled one; the guarantee at 1,00 % never binds on it, and a path that
   fell below the guarantee would make `cred_rate`'s `max` operative and change the shape.
6. **The charge levels, all of them [std].** The § 7 AltZertG *Produktinformationsblatt* exists
   precisely to publish this product's total charge burden as a single comparable *Effektivkosten*
   number, per quotation, and **not one was reached** (gap 2). The charge set lands inside the argued
   0,6 %–1,2 % band for a *klassisch* tariff, but that is a construction, not a calibration.
7. **The *Zuzahlung* take-up.** The product's signature premium form is entirely a modeller's view.
   Setting `zuz_take_up ≡ 0` removes about two fifths of the anchor's contribution stream and is a
   legitimate variant, not a bug — and a projection that treats the *Zuzahlung* as contractual has
   quietly made the opposite assumption.
8. **The eligible-survivor probability.** Inert on the anchor and decisive on model points 3, 4 and
   12: it scales the whole death benefit and the whole *Rentengarantiezeit* stream. 0.55 has nothing
   behind it.
9. **The annual grid against a monthly annuity, and the living texts around it.** Booking twelve
   instalments at the start of the payout year is generous to the year of death by up to a full year's
   annuity, concentrated in the high-mortality tail — a convention, not a result. Separately, the
   *Höchstbetrag* moves every year with the *Sozialversicherungsrechengrößen-Verordnung* [R20], the
   *Besteuerungsanteil* every year by construction [R4] [R6], and the *Höchstrechnungszins* moved in
   2025 for the first time in about thirty years [REG-R15]: none is a cash flow of this contract, and
   all three decide what a realistic model point looks like.
10. **Data provenance.** Two carrier artefacts stand behind this entire product, neither a
    *Bedingungswerk*, and **not one carrier's Basisrente contract terms were established** (gap 1).
    Every parameter that would normally be sourced to a carrier is **[std]**. A calibration pass
    against a real *Produktinformationsblatt*, a real *Bedingungswerk* and a real declared-rate history
    is required before any quantitative use of this model.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-basisrente-r1
[R14]: #delib-basisrente-r14
[R15]: #delib-basisrente-r15
[R16]: #delib-basisrente-r16
[R17]: #delib-basisrente-r17
[R2]: #delib-basisrente-r2
[R20]: #delib-basisrente-r20
[R23]: #delib-basisrente-r23
[R4]: #delib-basisrente-r4
[R6]: #delib-basisrente-r6
[R7]: #delib-basisrente-r7
[R8]: #delib-basisrente-r8
[R9]: #delib-basisrente-r9
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R39]: #delib-reg-r39
[REG-R4]: #delib-reg-r4
[REG-R40]: #delib-reg-r40
[REG-R41]: #delib-reg-r41
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R6]: #delib-reg-r6
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
