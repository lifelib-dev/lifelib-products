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
  Beiträge* and *Zuzahlungen* in; death benefits, annuity payments and survivor benefits out; insurer
  expenses and commission out — for a single model point on an expected (probability-weighted) basis,
  together with the state variables that make the product what it is: the ***Deckungskapital*** of the
  premium-paying and the premium-free cohorts, and the annuity secured at *Rentenbeginn*.
- **Out of scope, and said so.** No discounting. No *Deckungsrückstellung*, no *Zinszusatzreserve*
  [REG-R17], no Solvency II technical provision, no risk margin, no SCR — all cited, none computed
  (see *Valuation and reserve pointers*). **No tax**: the *Sonderausgabenabzug* [R2] [R7] and the
  *Besteuerungsanteil* [R4] [REG-R41] shape the product's economics and belong to `product-spec.md`,
  and neither is a cash flow of the contract. **No BUZ cash flows**: a *Berufsunfähigkeits-Zusatz\
  versicherung* written inside the contract is represented only by its **premium share**, and its
  disability mechanics belong to `BU_DE_S` (delib product 9). **No *Versorgungsausgleich***, no
  provider transfer, no *Wiederinkraftsetzung* after *Beitragsfreistellung*, no unit-linked or hybrid
  asset form.
- **The absences are the product.** There is **no surrender value cells, no `claims_lapse` column, no
  `cv_pp`, no `loan_pp`, no commutation and no lump sum anywhere in this model**, because the
  entitlement is *nicht kapitalisierbar*, *nicht veräußerbar* and *nicht beleihbar* [R1] [R14]
  [REG-R39] [REG-R40]. These are structural absences, not switched-off options, and
  `check_no_capital()` asserts them in code rather than in prose.
- **Projection grid: annual.** `t` counts **projection years from the valuation date**, and the frame
  is **1-based**: `t = 1 … proj_len()`. Policy duration at the start of year `t` is
  `duration(t) = duration_init + t − 1` completed policy years; attained age is
  `age(t) = entry_age + duration_init + t − 1`; calendar year is
  `cal_year(t) = conclusion_year + duration_init + t − 1`. A new-business model point has
  `duration_init = 0`, so `t = 1` is the first policy year; an in-force point opens at whatever
  duration it has already run, and **the frame still starts at `t = 1`**.
- **The annual grid is a choice, and here is the argument for it.** Every contractual event this
  product has lands on a policy anniversary: the *Beitragsdynamik* step, the *Zuzahlung*, the
  declaration of the year's *Überschussbeteiligung* at the balance date, the *Beitragsfreistellung*
  effective at the end of the current premium period [R14], and the conversion at *Rentenbeginn*. The
  one genuinely sub-annual mechanic — the annuity is paid **monthly** [R1] — is compressed to twelve
  instalments booked at the start of the payout year, which is a **[std]** convention and pitfall 12.
- **Projection horizon.** The annuity is lifelong, so the projection runs to the end of the mortality
  table: `proj_len() = omega_age() − age(1) + 1`, where `omega_age()` is the last age in
  `mort_table.csv` and `mort_rate_at_age(omega_age, ·) = 1.0`, so `pols_if(proj_len() + 1) = 0`
  exactly. `omega_age = 121` **[std]**, the terminal age German annuity tables are conventionally
  carried to. For the anchor cell `proj_len() = 121 − 45 + 1 = 77`.
- **`proj_len()` is the last projected period index**, not a row count: `result_cf().index[-1] ==
  proj_len()`. This is frlib's ruling and delib adopts and asserts it. Where the frame *starts* is a
  product fact and is not asserted; contiguity is.
- **Timing conventions [std].** The *laufender Beitrag* and the *Zuzahlung* are taken at the **start**
  of the projection year (annual in advance; the *Ratenzahlungszuschlag* is the contractual price of
  paying otherwise, so a fractionated mode changes the amount, not the grid). Charges on the premium
  are struck at the same moment. Interest is credited at the **end** of the year. Deaths fall at the
  end of the year, **after** crediting, so a dying policy carries a full year's interest. The
  *Beitragsfreistellung* transition falls at the end of the year **after** the death decrement.
  Annuity instalments are booked at the **start** of the payout year on the opening in-force count.
  Acquisition expense and initial commission fall at inception; maintenance expense and renewal
  commission at the start of each year.
- **Charges are not cash flows.** The *Zillmerung* amortisation, the premium charge β, the
  reserve charge γ and the *Stückkosten* are **deductions from the policyholder's *Deckungskapital***
  and hence insurer income; the insurer's own **outgo** is the acquisition expense, the commission,
  the maintenance expense and the annuity administration. A charge affects `net_cf` only through the
  benefit it shrinks. Booking a charge as both an account deduction and an expense outflow is
  pitfall 4.
- **Two cohorts, one model point.** A *Beitragsfreistellung* does not remove a policy; it moves it
  from the premium-paying cohort to the premium-free one, where its *Deckungskapital* continues to be
  credited and still converts at *Rentenbeginn* [R14]. The two cohorts' account values diverge from
  the first freeze, so the model carries the paying cohort **per policy** and the premium-free cohort
  **at fund level**, which is exact because every paying policy in one model point is identical and
  the premium-free block is a weighted average by construction.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  benefits and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents and `pols_if` to six decimals **[std]**. Totals are summed at full precision and then rounded.
- **Age basis.** Age last birthday at the contract's conclusion (*Eintrittsalter*), stepping on the
  policy anniversary **[std]** — no German market convention was established, and on this product
  mortality drives the annuity's duration rather than any benefit amount, so a half-year offset is
  second order. `mort_rate` is generational and depends on the **calendar** year as well as the age
  [R17] [REG-R49], which is why `cal_year(t)` is carried.

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
| `behaviour_table.csv` | `beh_table_id`, `dur` | `bf_rate`, `zuz_take_up` | The two behavioural assumptions that vary by policy duration: the *Beitragsfreistellung* rate and the *Zuzahlung* take-up |
| `option_table.csv` | `option_id`, `option_key` | `factor` | One multiplicative factor per contractual option: `prem_mode` → the *Ratenzahlungszuschlag* on the premium; `guarantee_period` and `survivor` → the reduction in the *Rentenfaktor* |

Scalar assumptions that are single numbers rather than tables are `Projection` References and are
tagged in *Assumption inputs* below: `mort_be_factor`, `elig_surv_prob`, `mort_base_year`,
`zill_spread_y`, `omega_age_max`, `rf_unit`, `ann_freq`, `roll_fwd_tol`.

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
| `prem_mode` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency; keys `option_table.csv` for the *Ratenzahlungszuschlag* | 1, 5, 9, 13 annual · 4 half-yearly · 3, 11 quarterly · 2, 10, 12 monthly |
| `prem_dyn_rate` | rate p.a. | *Beitragsdynamik*, the contractual annual escalation | 1, 2, 3, 4, 6, 9, 11, 12 |
| `zuzahlung_pp` | EUR p.a. | The nominal annual *Zuzahlung* before take-up | 1, 3, 9, 11 |
| `zuzahlung_end_dur` | int | Last policy duration at which a *Zuzahlung* is assumed | 1, 3, 9, 11 |
| `paidup_at_init` | bool | The model point is already *beitragsfrei* at the valuation date | 7 |
| `av_pp_init` | EUR | *Deckungskapital* per policy at the valuation date | 6, 7 |
| `ann_pp_init` | EUR p.a. | Annual annuity already in payment, for a point that opens in the *Rentenphase* | 8 |
| `gtd_rate` | rate p.a. | The contract's *Rechnungszins*, the cohort's guarantee vintage [REG-R15] | 6 (2,25 %), 7 (1,75 %), 8 (2,75 %), rest 1,00 % |
| `rentenfaktor_gtd` | EUR per month per 10 000 € | *Garantierter Rentenfaktor*, fixed at inception [R17] [S1] | 13 (set above the current-factor scenario, so the guarantee binds) |
| `guarantee_period_y` | int | *Rentengarantiezeit* in years from *Rentenbeginn*; 0 = none | 4 (10), 12 (20) |
| `surv_annuity_rate` | rate | Survivor's annuity as a fraction of the main annuity; 0 = **rider off**, which is the base design | 3 (0.60), 12 (0.60) |
| `buz_prem_share` | rate | Share of the **total** contribution attributable to a BUZ. Must satisfy `buz_prem_share < 0.50` [R1] | 11 (0.49, the boundary) |
| `tariff_id` | str | Key into `charge_table.csv` | all |
| `beh_table_id` | str | Key into `behaviour_table.csv` | all |
| `surplus_scenario_id` | str | Key into `surplus_table.csv` | all |
| `rf_scenario_id` | str | Key into `rentenfaktor_table.csv` | 13 (`low`) |

**There is no `surr_rate`, no `lapse_rate` and no `kapitalwahl` column**, and their absence is a
statutory fact about the product rather than a modelling simplification [R1] [R14] [REG-R39].
`lapse_rate` would be the name a modeller reusing the delib endowment or Schicht-3 chassis reaches for
first; the decrement it names does not exist here, and `bf_rate` — which is **not** a lapse — is what
takes its place.

**An in-force paid-up point is represented wholly, not partly.** A model point either opens entirely
premium-paying (`paidup_at_init = 0`, `av_pp_init` the paying cohort's per-policy reserve) or entirely
premium-free (`paidup_at_init = 1`, the whole of `pols_if_init` opening in the premium-free cohort
with `av_pu_at(1, "BEF_PREM") = av_pp_init × pols_if_init`). A book that is part paid-up is
represented by **two model points**, which is the honest arrangement: the two cohorts have different
reserves per policy and averaging them is pitfall 3.

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
age-floor cohorts, four guarantee vintages, and four boundary cases.

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
the market-average rates carried in sibling delib files are Schicht-3 and endowment figures that must
not be relabelled. The path is a scenario, not a forecast: it starts above the 1,00 %
*Höchstrechnungszins* by a plausible surplus margin and grades down, so the guarantee does not bind on
the base run and the *Zinsüberschuss* is visible.
(ii) German declared rates are quoted as the **total** credited rate including the *Rechnungszins*, so
`cred_rate` is a `max`, not a sum. Adding the declared rate **on top of** the guarantee is pitfall 6.
(iii) The single-date allocation is a **contract fact** on this product [R15] — no surrender means no
early-exit trigger — while the 4,0 % level is **[std]** with nothing behind it.
(iv) A *volldynamische Rente* would consume the whole first-order margin released in the payout phase;
a *konstante Rente* would consume none. 1,0 % is deliberately in between, and it is the parameter that
decides how much of the conversion-basis wedge (see *Key sensitivities*) is given back.
(v) **No *Rentenfaktor* level, range or time series exists anywhere in the delib corpus, for this or
any product** (gap 4). The base scenario is set **above** the guaranteed factor so that
`max(gtd, curr)` is visibly operative and the `low` scenario is set below it, so model point 13
exercises the other branch.
(vi) Anchored on the sibling corpus's Schicht-3 illustration — a 10-year *Rentengarantiezeit* at about
0,5 % of the annuity, 20 years at 2,6 %, 30 years at 8,0 % — which is **[unverified] and explicitly
not transferable** to Schicht 1. The survivor factor has no anchor at all.

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

`q`, `f`, `i`, `b` are per-annum probabilities or rates; `A`, `P`, `Z`, `F`, `a`, `E`, `C` are EUR;
`R` is euro of monthly annuity per 10 000 € of capital.

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

`prem_total_pp` **never enters `net_cf`** — the BUZ premium buys a cover this model does not project
— and `buz_prem_share < 0.50` is the statutory invariant [R1] the test module asserts (pitfall 17).

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
expenses(t)          = acq_expense_pp × 1{t = 1 and duration_init = 0}
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

Columns 4 and 5 enter `net_cf` positively, 6 to 10 negatively, and column 3 does not enter it at all.
`pols_paying` is a count, not a cash flow, and `av` is a balance; both are published because a reader
cannot follow the projection without them, and both are named in `check_net_cf()`'s docstring as
excluded from the identity.

### The published checks

| Check | The identity it closes |
|---|---|
| `check_net_cf()` | `net_cf(t) = premiums + zuzahlungen − claims_death − claims_annuity − claims_survivor − expenses − commissions` at every `t`. **delib ruling 1**, mandatory on every model in the library |
| `check_pols_roll_fwd()` | `pols_paying(t) + pols_paidup(t) = pols_if(t)`, and `pols_if(t+1) = pols_if(t) × (1 − mort_rate(t))` — the *Beitragsfreistellung* rate does **not** appear |
| `check_av_roll_fwd()` | `av_at(t+1) = av_at(t, "AFT_INT") × (1 − mort_rate(t))` for `t < ret_t()`, and `av(t) = 0` for `t ≥ ret_t()` |
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

These are the specific ways an implementation of *this* product looks right and is wrong. Each one
becomes a test.

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
  *Rentenbeginn*, or release any of the § 10 constraints: a paid-up Basisrente is still certified,
  still protected, still payable only as an annuity [R1] [R9] [R14].
- **The *Zuzahlung* take-up** is the second behavioural assumption and the more distinctive one. The
  contribution the tax ceiling makes possible is paid out of a profit not known until the year end, so
  `zuz_take_up(dur)` is a **utilisation rate**, not a contract term: 0.70 early, 0.85 in mid-term,
  0.90 late. A model that treats the *Zuzahlung* as contractual has hard-coded an assumption.
- **No *Wiederinkraftsetzung*.** Premiums can in practice be resumed within a window [R14], and the
  base model does not resume them: the premium-free block is absorbing. That is deliberately
  conservative on premium income and is stated rather than hidden; **no carrier's window was
  established** (gap 8).
- **Selection on the annuitant pool is not modelled, and the direction is known.** A Basisrente cannot
  be surrendered or commuted, so a policyholder in poor health has no exit and nobody leaves the pool —
  which argues for **lighter** mortality than a comparable Schicht-3 portfolio, where the
  *Kapitalwahlrecht* lets an impaired life leave [R17]. **No evidence for this was found**; it is a
  **[std]** view and a stated model risk, and `mort_be_factor` is the single lever that would carry it.
- **No dynamic annuitisation behaviour, because there is none to model.** There is no
  *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no *Kleinbetragsrenten-Abfindung* and no election of
  any kind at *Rentenbeginn* [R1] [R23]. The Schicht-3 chassis needs a take-up assumption and a
  declaration window; this product needs neither, and that is the cleanest simplification the layer
  buys.
- **Deferral of *Rentenbeginn* is not modelled either.** Contracts commonly permit it and the tax
  arithmetic often favours it, but no carrier's permitted range was established (gap 8), so
  `ret_age` is a model-point input and model point 12 exercises a deferral to 70 as a configuration
  rather than as a behaviour.

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

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects **gross best-estimate-style liability cash flows, undiscounted**, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The German statutory *Deckungsrückstellung*.** An HGB reserve of § 341f HGB [REG-R54], computed on
  the *Rechnungsgrundlagen* the DeckRV fixes [REG-R14]: the contract's own *Rechnungszins* — capped at
  the *Höchstrechnungszins* in force at conclusion and fixed for the whole term [REG-R15] — and
  first-order DAV 2004 R [REG-R49]. The model's `av_at(t, ·) × 1` and, after conversion, the annuity
  obligation `ann_pp(t) × pols_if(t)` are what a *Deckungsrückstellung* stands behind; **neither is a
  reserve and delib computes none**. Acquisition costs enter it through the *Zillmerung* of § 4 DeckRV,
  capped at 25 ‰ of the *Beitragssumme* [REG-R16].
- **The *Zinszusatzreserve*.** The additional HGB reserve arising where the *Referenzzins* of
  § 5 Abs. 3 DeckRV falls below a contract's tariff rate [REG-R17]. It exists in no other jurisdiction
  in this repository, it is financed out of the result and, at need, out of the free *RfB* [REG-R10],
  and it bites hardest on annuity business because the § 12 MindZV test looks at the highest
  *Rechnungszins* applicable over the next fifteen years [REG-R18]. **A long-dated Basisrente is
  exactly the business it bites on**, and nothing in this model represents it.
- ***Überschussbeteiligung* and the MindZV floor.** The credited rate in this model is a **[std]**
  scenario, not a derivation: a real declaration runs through the four surplus sources, the MindZV
  minimum allocation of 90 % / 90 % / 50 % [REG-R18], the RfBV's constraints on the collective part of
  the *RfB* [REG-R19] and the § 139 VAG *Sicherungsbedarf* test on *Bewertungsreserven* [REG-R9]. A
  model that needed the declaration to be endogenous would have to carry the insurer's whole HGB
  result, which is a fund model, not a policy model.
- **Solvency II.** Technical provisions are a best estimate — the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure — plus a risk margin
  [REG-R1] [REG-R2] [REG-R6], with EIOPA publishing the curves monthly [REG-R4].
  `BEL = Σ_t v(t) × liability_cf(t)` over the recursions above. **No cost-of-capital rate,
  contract-boundary rule or standard-formula shock anywhere in this library was read from a retrieved
  instrument**, so every such figure would be **[std]** [REG-R2].
- **Contract boundary.** The premium is contractually variable — the *Beitragsdynamik* may be declined
  and the *Zuzahlung* is discretionary — which raises a real boundary question this library does not
  resolve: whether the projected *Zuzahlungen* and *Dynamik* increments fall inside the contract
  boundary at all. The model's posture is to project the whole stream and publish it; a
  boundary-truncated view is obtained by zeroing `zuzahlung_pp` and `prem_dyn_rate` on the model point
  rather than by editing the projection.
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
   `ann_bonus_rate` gives back. Move `mort_be_factor` and the margin moves; move `ann_bonus_rate` and
   the giving-back moves; and the two are **[std]** independently, which means the payout phase's
   profitability in this model is an artefact of two unanchored numbers rather than a result. This is
   the most important thing to understand before quoting any figure from the payout phase.
3. **Mortality level and the generational trend.** The liability is a lifetime annuity, so a 1,5 %
   annual improvement compounded over a 22-year deferment and a 40-year payout is worth far more than
   it looks. The trend is flat across ages here, which DAV 2004 R's own trends are not [REG-R49], and
   the flatness is the more dangerous of the two simplifications on a long run.
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
   number, per quotation, and **not one was reached** (gap 2). The reference implementation's charge
   set lands inside the argued 0,6 %–1,2 % band for a *klassisch* tariff, but that is a construction,
   not a calibration.
7. **The *Zuzahlung* take-up.** The product's signature premium form is entirely a modeller's view.
   Setting `zuz_take_up ≡ 0` removes about two fifths of the anchor's contribution stream and is a
   legitimate variant, not a bug — and a projection that treats the *Zuzahlung* as contractual has
   quietly made the opposite assumption.
8. **The eligible-survivor probability.** Inert on the anchor and decisive on model points 3, 4 and
   12: it scales the whole death benefit and the whole *Rentengarantiezeit* stream. 0.55 has nothing
   behind it.
9. **The annual grid against a monthly annuity.** Booking twelve instalments at the start of the
   payout year is generous to the year of death by up to a full year's annuity, concentrated in the
   high-mortality tail. The direction is known and the size is small relative to the assumption risks
   above; it is stated because it is a convention, not a result.
10. **Living texts, and what they do to a model point.** The *Höchstbetrag* moves every year with the
    *Sozialversicherungsrechengrößen-Verordnung* [R20], the *Besteuerungsanteil* moves every year by
    construction [R4] [R6], and the *Höchstrechnungszins* moved in 2025 for the first time in about
    thirty years [REG-R15]. None of the three is a cash flow of this contract, and all three decide
    what a realistic model point looks like. Re-read them before using any configuration here.
11. **Data provenance.** Two carrier artefacts stand behind this entire product, neither of them a
    *Bedingungswerk*, and **not one carrier's Basisrente contract terms were established** (gap 1).
    Every parameter that would normally be sourced to a carrier is **[std]**. A calibration pass
    against a real *Produktinformationsblatt*, a real *Bedingungswerk* and a real declared-rate history
    is required before any quantitative use of this model.
