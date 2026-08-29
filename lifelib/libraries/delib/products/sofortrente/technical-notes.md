# Technical Notes

**Status:** Draft, 2026-08-29 (all sources dated 2026-08-29; **none was retrieved**).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Sofort_DE_S`**, **monthly** grid — for the representative composite German *sofortbeginnende
private Rentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's product, and no clause of any German AVB for it was read. [S#] and [R#] tags refer to
`sources.md` (numbering carried from `_research/sofortrente.md`; frozen); [REG-R#] tags the
cross-product reference library `references/regulatory-and-actuarial-references.md` (its own frozen
R1–R56 numbering). **[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims no search corroborated. Parameter values are identical to those in
`product-spec.md`. Cells names, model-point columns and CSV headers are English `lower_snake_case`;
German terms of art keep their German form in prose.

**Retrieval conditions.** Direct HTTP egress was blocked and the session's `WebSearch` budget was
exhausted before work on this product began, so **not one search was run for the *Sofortrente***.
Every level in class (b) and class (c) below is therefore **[std]**, and several in class (a) are
too. That is stated once here and tagged at every occurrence rather than repeated in prose.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for one *Sofortrente* — the
  *Einmalbeitrag* in, the guaranteed annuity and the *Überschussrente* out, the guaranteed
  instalments continuing to beneficiaries inside a *Rentengarantiezeit*, the *Kapitalrückgewähr* on
  death, the *Hinterbliebenenrente*, and insurer expenses — on an expected, probability-weighted
  basis, for a single model point. **Undiscounted.** Discounting, the *Deckungsrückstellung*
  recursion, the *Zinszusatzreserve*, the Solvency II best estimate and risk margin and the IFRS 17
  measurement are **out of scope** and are cited, not computed (see *Valuation and reserve
  pointers*).
- **Mortality is the model.** After *Rentenbeginn* the contract has **no premium stream, no
  surrender value, no lapse decrement, no paid-up state and no policyholder option of any kind**
  [R1] [R2] [R5] [REG-R28]. The only decrement is death; where a *Hinterbliebenenrente* is in force
  there are two lives and the liability runs to the second death. **There is no lapse machinery
  anywhere in this model, and that is a cited product feature rather than an omission.**
- **Projection frequency and origin.** **Monthly grid**, `t = t_start() … proj_len()`, counted in
  complete months from *Vertragsbeginn*. Month `t` is the civil month beginning at the `t`-th
  month-start after inception. The frame is **0-based**: a new-business model point opens at
  `t = 0`, which is both the month the *Einmalbeitrag* is received and — under the representative
  *vorschüssig* convention — the month the first instalment is paid. An in-force model point opens
  at `t = duration_mth_init()`, the number of months the contract has already run.
- **The model carries duration, not the calendar.** Every step in this product falls on a **policy
  anniversary**: the *Überschussrente* increase [S15], the expense inflation index, the attained-age
  step. Nothing happens on 31 December, so — unlike `frlib`'s `Rente_FR_S`, where revalorisation is
  a calendar event — no cells needs the civil month. `entry_year` is carried all the same, for two
  reasons that are not cash flows: it is the **cohort key** of the generational mortality surface,
  and it selects the **contract's own *Höchstrechnungszins* vintage** [REG-R14] [REG-R15].
- **Timing conventions [std].** The *Einmalbeitrag* arrives at the **start of month 0**. Instalments
  are paid at the **start** of a payment month; under `advance` (*vorschüssig*) the first falls at
  `t = defer_mths()`, under `arrears` (*nachschüssig*) at `t = defer_mths() + 12/payment_freq`. A
  payment is made if the payee is alive at the **start** of that month — the same instant — so the
  survival index of a payment is always `t` and the two timings differ **only in which months carry
  an instalment**. Deaths fall **during** month `t`, so a life dying in month `t` has already
  received the instalment due at `t`; the *Kapitalrückgewähr* is settled net of it. Expenses accrue
  at the start of the month.
- **Age basis and generation [std].** `age(t, life) = entry_age(life) + t // 12`: age last birthday
  at inception, incrementing at each 12-month multiple of it. The **birth year is a separate model
  point attribute and is never derived from the projection year**, because the mortality surface is
  generational and the cohort is its key [REG-R49]. The shipped model points satisfy
  `entry_year == birth_year(1) + entry_age(1)`, which is a **[std]** internal-consistency
  convention, not a contract fact; a real book will carry a fractional offset of up to a year.
- **Unisex pricing.** The tariff annuity factor is computed on a **unisex blend** of the sex-distinct
  proxy tables, at a **[std]** portfolio male share; the model point's own `sex` drives only the
  best-estimate decrement path [REG-R34] [REG-R49]. Letting `sex` reach the annuity factor
  reproduces a tariff unlawful in Germany since 21 December 2012 and is pitfall 10.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (the
  *Einmalbeitrag* +, annuity payments, death benefits and expenses −), with the outgo-positive
  orientation of these notes published as `liability_cf(t) = −net_cf(t)`. No intermediate rounding;
  displayed cash flows to the cent and probabilities to six decimals **[std]**.
- **Out of scope and said so.** The *Bewertungsreserven* share, which continues in the payout phase
  [S3] [REG-R24] but is path- and balance-sheet-dependent on the HGB accounts [REG-R9] [REG-R18]; a
  commuted settlement of the *Restgarantiezeit*, whose basis was not established (research gap 10);
  taxation, which falls on the annuitant rather than on the insurer's liability [REG-R41]; and any
  management action on the declared surplus.

---

## Model point attributes

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Key; `Projection` is parameterized by it | all |
| `policy_id` | str | Reference, reporting only | all |
| `single_prem` | EUR | The *Einmalbeitrag*, `SP` | all |
| `entry_age` | int | Annuitant's age last birthday at *Vertragsbeginn* | all |
| `entry_year` | int | Calendar year of *Vertragsbeginn*; the *Höchstrechnungszins* vintage | 10, 13 |
| `birth_year` | int | Annuitant's *Geburtsjahr* — the generational table key | all |
| `sex` | enum {M, F} | **Decrement only**; the tariff is unisex [REG-R34] | 11, 12 (F) |
| `defer_years` | int | *Aufschubzeit*, 0 for a pure *Sofortrente* | 6 |
| `guar_years` | int | *Rentengarantiezeit*, 0 = none | 1, 5, 7–10, 12–14 |
| `refund_form` | enum {none, full} | *Kapital-/Beitragsrückgewähr* | 3, 6 |
| `surv_pct` | float 0–1 | *Hinterbliebenenrente* as a fraction of the annuitant's annuity; 0 = rider off | 4, 5 |
| `surv_age` | int | Second life's age last birthday at *Vertragsbeginn* | 4, 5 |
| `surv_birth_year` | int | Second life's *Geburtsjahr* | 4, 5 |
| `surv_sex` | enum {M, F} | Second life's sex, decrement only | 4, 5 |
| `payment_freq` | int {12, 4, 2, 1} | Instalments per year, `m` | 7 (4), 8 (1), 11 (2) |
| `payment_timing` | enum {advance, arrears} | *vorschüssig* / *nachschüssig* **[std]** | 9 |
| `tariff_int_rate` | float | The tariff *Rechnungszins* `i`, at or below the vintage cap | 10, 13 |
| `surplus_form` | enum {none, konstant, teildynamisch, volldynamisch} | *Überschussverwendung* | 5, 8, 11, 13 (konstant); 6, 12 (voll); 14 (none) |
| `annuity_pp_init` | EUR | Guaranteed instalment carried on an in-force point; **0 = derive by equivalence** | 10 |
| `duration_mth_init` | int | Months already elapsed at the valuation date; the frame's first `t` | 10 |
| `pols_if_init` | float | Policies the point represents | all |

**Two configurations, not two premium forms.** A *Sofortrente* has exactly one premium form — a
single *Einmalbeitrag* — so the pair of shapes this model must serve is not `level`/`revisable` but
**derived** against **given**: a new-business point (`annuity_pp_init == 0`) whose guaranteed annuity
the model strikes from `single_prem` by equivalence on the tariff basis, and an in-force point
(`annuity_pp_init > 0`) whose annuity was struck years ago on a basis the model does not reproduce
and is therefore carried. Model point 10 is the second kind. On it the pricing identity
`check_equivalence()` is not asserted, and the notes say so rather than letting the check pass
vacuously without explanation.

`surv_age`, `surv_birth_year` and `surv_sex` are ignored where `surv_pct == 0`, and the shipped table
carries zeros there. `sex` is carried but **must not** enter the annuity factor [REG-R34].

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `t_start()` | First projected month = `duration_mth_init()`; 0 for new business | once |
| `proj_len()` | **Last** projected month index, so `result_cf().index[-1] == proj_len()` | once |
| `horizon_mths(life)` | `12 × (omega_age − entry_age(life))`, the month at which that life's survival reaches zero | once |
| `age(t, life)` | Attained age = `entry_age(life) + t // 12` | monthly |
| `policy_year(t)` | Completed policy years = `t // 12` | monthly |
| `calendar_year(t)` | `entry_year() + t // 12`; reporting and the cohort cross-check | monthly |
| `mort_rate(t, life)` | **Annual** second-order rate at `age(t, life)` for that life's cohort and sex | monthly |
| `mort_rate_mth(t, life)` | `1 − (1 − mort_rate)^(1/12)` **[std]** | monthly |
| `mort_rate_tariff(t, life)` | **Annual** first-order rate on the **unisex** blend, used only for pricing | monthly |
| `lives_if(t, life)` | Second-order probability alive at the **start** of month `t`; `lives_if(0) = 1` | recursion |
| `lives_death(t, life)` | `lives_if(t) − lives_if(t + 1)`, deaths **during** month `t` | monthly |
| `tariff_lives(k, life)` | First-order survival to the start of month `k`, used only inside the pricing sums | recursion |
| `first_pay_mth()` | `defer_mths()` under `advance`, `defer_mths() + pay_period_mths()` under `arrears` | once |
| `guar_end_mth()` | `first_pay_mth() + 12 × guar_years()`; the first month after the guarantee | once |
| `certain_floor(t)` | 1 while the *Rentengarantiezeit* runs, else 0 | monthly |
| `is_payment_mth(t)` | Whether an instalment falls due at the start of month `t` | monthly |
| `annuity_pp_derived()` | The guaranteed instalment struck by equivalence from `SP` | once |
| `annuity_guar_pp(t)` | The *garantierte Rente* in force in month `t`; level for life | monthly |
| `annuity_surp_pp(t)` | The *Überschussrente* instalment in month `t`; steps at the anniversary | monthly |
| `annuity_pp(t)` | `annuity_guar_pp(t) + annuity_surp_pp(t)`, the total instalment | monthly |
| `cum_annuity_guar_pp(t)` | Cumulative **guaranteed** instalments paid to and including month `t` | recursion |
| `refund_pp(t)` | `max(SP − cum_annuity_guar_pp(t), 0)` where the refund is elected, else 0 | monthly |
| `payment_factor(t)` | `max(certain_floor, l_a) + δ (1 − l_a) l_s (1 − certain_floor)` at the payment instant | monthly |
| `infl_factor(t)` | `(1 + expense_infl)^(t // 12)` **[std]**, stepping at the policy anniversary | monthly |
| `pols_if(t)` | Probability that any payment obligation remains at the start of month `t` | monthly |

There is **no account value, no surrender-value, no paid-up and no lapse state variable**, and no
`av_pp_at` / `lapse_rate` / `lapse_rate_mth` cells anywhere in the model. That is a statutory fact
about the product [R1] [R2] [R5] [REG-R28], not a modeling simplification, and it is asserted by
pitfall 17 rather than left to inspection.

`pols_if(t)` is **not a policy count**: it is the probability that a payment obligation of any kind
still stands — the guarantee period running, the annuitant alive, or the survivor's annuity in
payment — and it is the weight the maintenance expense is carried on. It keeps the library's name
for the expense weight, and its docstring says what it is so the shared conventions suite can apply
the payout-product exemption. At the frame's first row it is `pols_if_init()` exactly, on a
new-business point and on an in-force one alike.

---

## Assumption inputs

Three classes. Class (a) is contractual or statutory and is cited where the corpus supports it;
class (b) is the insurer's current discretionary scale, revisable annually within the statutory
minimum [REG-R18] [REG-R24]; class (c) is the modeller's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Premium | One *Einmalbeitrag* at `t = 0`; no premium stream | [S2] [S6]; structural |
| *Nettoeinmalbeitrag* | `SP × (1 − α)` | [S8]; α **[std]**, class (c) |
| Equivalence | `SP_net = R × ä × (1 + β) + PV(refund)` on the **first-order** basis at the tariff `i` | [S6] [R10] |
| Mortality basis, pricing | DAV 2004 R, **first order**, generational, unisex tariff | [S6] [R10] [REG-R34] [REG-R49] |
| Tariff *Rechnungszins* | Model-point attribute; **1,00 %** for 2025–2026 business, at or below the vintage cap | [REG-R14] [REG-R15]; below-cap pricing observed [S6] |
| Guarantee | The *garantierte Rente* is immutable for life; § 163 VVG is the only channel and it is narrow | [S6] [REG-R27] [R4] |
| Payment frequency and timing | Monthly, *vorschüssig*, first instalment at inception | [S7] [R23]; timing **[std]** |
| *Rentengarantiezeit* | `guar_years × payment_freq` instalments payable **regardless of survival** from *Rentenbeginn* | [R23] [S5] [S7] |
| *Kapital-/Beitragsrückgewähr* | `max(SP − guaranteed instalments already paid, 0)` on death | [R23]; measured on the **guaranteed** annuity **[std]** |
| *Hinterbliebenenrente* | `surv_pct` of the annuitant's annuity to a named second life, from the annuitant's death, for that life's remaining lifetime; lapses if the second life predeceases | [S9]; percentages [unverified] |
| Death-benefit exclusivity | The refund is **not** combined with a guarantee period or a survivor's annuity | **[std]**, research gap 10 |
| Surrender / paid-up / lapse | **None**, once the *Rentenbezug* has begun | [R1] [R2] [R5] [REG-R28] |
| *Überschussbeteiligung* | A statutory entitlement continuing through the payout phase; method not prescribed | [S3] [REG-R24] |
| Limiting age | `omega_age = 121`; the proxy table closes with `q = 1` at attained age 120 | **[std]** |

### (b) Insurer-discretionary current elements

**No *Überschussbeteiligung* rate was established for this product, at any carrier, for any year**
(research gap 4). [S10] establishes the document class that publishes them and [R22] the market study
that aggregates them; nothing inside either. Every figure below is therefore **[std]**, and the class
is labelled (b) rather than (a) precisely because the insurer may reduce it — the *konstante
Überschussrente* included [R21].

| Input | Snapshot value | Basis |
|---|---|---|
| `surplus_init_pct` — *Überschussrente* at outset, as a fraction of the *garantierte Rente* | `none` 0 %; `konstant` **20 %**; `teildynamisch` **10 %**; `volldynamisch` **0 %** | **[std]** (b1) |
| `surplus_growth` — annual increase in the *Überschussrente* | `none` 0 %; `konstant` **0 %**; `teildynamisch` **1,0 %**; `volldynamisch` **2,0 %** | **[std]** (b1) |
| Crediting mechanic | The *Bonusrente* ratchet: an increment, once bought, is not taken back, so `annuity_pp(t)` is non-decreasing | [R23]; levels **[std]** |
| Increase date | The **policy anniversary**, not a calendar date | [S15]; **[std]** |
| *Bewertungsreserven* share | **Excluded**, explicitly | [S3] [REG-R24]; see *Model scope* |
| Reduction of a declared *Überschussrente* | **Not modelled**; the projection is a central estimate, and the sensitivity section prices the downside instead | [R21]; **[std]** |

(b1) The market's own description gives the *shape* and nothing else: the constant form is highest at
outset and flat in intention only, the volldynamic form lowest at outset and rising with each
declaration, the teildynamic form intermediate on both axes [R20] [R21] [R23]. The opening percentage
of 20 % for the constant form sits in the middle of the 15 %–25 % gap between guaranteed and total
annuity that the market is [unverified] said to run at, and the growth rates are round numbers
consistent with a *Zinsüberschuss* of one to two points over a 1,00 % *Rechnungszins*. **The three
forms are not calibrated to equal present value in this implementation**, and a user who needs them
to be must do that calibration; asserting equality is a wrong test, not a right one.

### (c) Behavioural / experience assumptions (modeller's view)

**The behavioural set is empty, and that is the product.** There is no lapse rate, no paid-up rate,
no dynamic surrender formula and no option take-up rate, because there is no option to take up after
*Rentenbeginn* [R1] [R2] [R5]. What remains in class (c) is the **basis** — mortality and expenses —
and every level in it is **[std]**.

**Mortality — the shipped [std] proxy.** DAV 2004 R and DAV 2004 R-Bestand are DAV property, are not
public and are **not redistributed here** [REG-R47] [REG-R49]. `mort_table.csv` ships a constructed
proxy in four series — `{FIRST, SECOND} × {M, F}` — over attained ages 50 to 120, built as follows
**[std]**:

    q_base(x) = 1 − exp( −( A + B·c^x·(c − 1)/ln c ) ),   A = 0.0002,  B = 1.5e-5,  c = 1.10
    FIRST/M  = 1.250000 × q_base(x)      SECOND/M = 1.20 × FIRST/M
    FIRST/F  = 0.795455 × q_base(x)      SECOND/F = 1.20 × FIRST/F

`q_base` is the Gompertz–Makeham law the research file constructs and prints, with life expectancy
24,29 years at 65 and `q(65) = 0.00789`, `q(75) = 0.02001`, `q(85) = 0.05078`. **The anchor is that
the 45 % / 55 % unisex blend of the FIRST series reproduces `q_base(x)` exactly at every age** —
`0.45 × 1.250000 + 0.55 × 0.795455 = 1.000000` — so the model's tariff basis is the research file's
own basis and any figure printed there can be traced into the model. The identity holds at ages 50 to
119; age 120 is the closing row, where all four series are set to `1.0` and the survival path
therefore reaches zero exactly. The `Data` docstring states this anchor.

**The generational surface.** A period table is the wrong object for a forty-year annuity [REG-R49].
`improvement_table.csv` ships `λ(x)` in two series **[std]**:

    λ_SECOND(x) = 0.0150                        for x ≤ 70
                = 0.0150 × (105 − x) / 35       for 70 < x < 105
                = 0.0000                        for x ≥ 105
    λ_FIRST(x)  = 1.25 × λ_SECOND(x)

and the model constructs

    q(x, sex, cohort, basis) = q_table(x, sex, basis) × (1 − λ(x, basis))^(cohort + x − mort_base_year)

with `mort_base_year = 2025` **[std]**, so the base tables are the period tables of calendar year
2025 and the exponent is simply the calendar year in which the life attains age `x`, less 2025. The
exponent may be **negative** for a cohort attaining an age before 2025 — an in-force point issued in
2012 reads pre-2025 mortality, which is correct and is not floored.

**The *Sicherheitszuschlag* is two-dimensional and both dimensions are shipped.** For an annuity,
prudence means **lighter** mortality **and a stronger assumed improvement trend**, so a proxy
reproducing only the level is not a proxy for the table [REG-R47]. Here the first-order basis is
**20 % lighter** in level (`SECOND = 1.20 × FIRST`) and improves **25 % faster** (`λ_FIRST = 1.25 λ_SECOND`),
both **[std]** with no observed range (research gap 12). The wedge between the two bases is the
systematic *Risikoüberschuss* this product's surplus is largely financed from [REG-R47] [REG-R18];
collapsing them destroys both halves of the mechanic and is pitfall 9.

**Unisex blend.** `mort_rate_at_age(x, "U", basis) = ρ_M · q(x, "M", basis) + (1 − ρ_M) · q(x, "F", basis)`
with `ρ_M = mix_male = 0.45` **[std]**. The direction is argued rather than observed: a unisex tariff
struck on sex-distinct tables is a better deal for women than for men, so the realised female share of
a voluntary annuitant portfolio sits above the population share [REG-R34]. **No German carrier
publishes a portfolio mix** (research gap 13).

**Expenses and loadings.** The two *loadings* are tariff parameters and enter the pricing identity;
the two *expenses* are best-estimate cash flows and do not. Keeping them apart is the point of the
three-class split, and confusing them is pitfall 12's neighbour.

| Input | Value | Basis |
|---|---|---|
| `expense_load_alpha` α — acquisition loading in the tariff | **2,5 %** of `SP` | **[std]** (c1) |
| `expense_load_beta` β — administration loading on the annuity value | **2,0 %** | **[std]** (c1) |
| `expense_acq_rate`, `expense_acq_fixed` — acquisition expense actually incurred at `t = 0` | **2,0 %** of `SP` **plus 200 €** | **[std]** (c1) |
| `expense_maint_pp` — maintenance expense per annum, per unit of `pols_if` | **60 €**, accrued monthly | **[std]** (c1) |
| `expense_pay_pp` — cost of running one instalment | **1,50 €** per instalment paid | **[std]** (c1) |
| `expense_infl` — expense inflation | **1,5 %** p.a., stepping at the policy anniversary | **[std]** (c1) |
| `mix_male` ρ_M | **0.45** | **[std]** |
| `mort_base_year` | **2025** | **[std]** |
| `omega_age` ω | **121** | **[std]** |
| `roll_fwd_tol` | **1e-8**, the tolerance every `check_*` closes to | **[std]** |
| `solve_tol`, `solve_max_iter` | **1e-10**, **200** — the bisection controls for the refund solve | **[std]** |

(c1) **No charge or expense parameter was established at any carrier** (research gap 8), so none of
these has an observed range. The loadings are argued in `product-spec.md` footnote 6. The incurred
expenses are sized so that the tariff **over-recovers modestly**, which is the right direction and
the source of the *Kostenüberschuss*: on the anchor cell the acquisition loading takes 2 500 € against
2 200 € incurred, and the β loading collects roughly 2 % of the *Nettoeinmalbeitrag* against a
maintenance-plus-payment stream of about 78 € a year. A user with real expense data should replace all
six numbers; the two loadings and the four expenses must be replaced **together**, because moving one
without the other silently changes the modelled profit rather than the modelled cost.

### Input files

Inputs are **external CSVs in the model folder's parent**, read once per model by an unparameterized
`Data` Space — the `annuallife/TradLife_A` layout. Five files, and every one of them is read:

| File | Index columns | Value columns | Read by |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the 21 attributes above | `Data.model_point_table()` |
| `mort_table.csv` | `basis`, `sex`, `age` | `mort_rate` | `Data.mort_table()` |
| `improvement_table.csv` | `basis`, `age` | `improve_rate` | `Data.improvement_table()` |
| `surplus_scale_table.csv` | `surplus_form` | `surplus_init_pct`, `surplus_growth` | `Data.surplus_scale_table()` |
| `hoechstrechnungszins_table.csv` | `year_from` | `year_to`, `max_rate` | `Data.hoechstrechnungszins_table()` |

`basis` takes `FIRST` or `SECOND`, `sex` takes `M` or `F` — the unisex blend is a model construction,
not a table row, so the CSV never carries a rate no real table would. Every file **except**
`model_point_table.csv` carries a final `provenance` column, one tag per row, per the library's second
ruling; a model point is a configuration rather than an assumption and is the only exemption. The
scalar assumptions of class (c) are `Projection` References rather than a sixth CSV, and are tagged in
the tables above.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | month index from *Vertragsbeginn*, `t = t₀ … n` |
| `t₀`, `n` | `t_start`, `proj_len` | first and last projected month index |
| `m`, `p` | `payment_freq`, `pay_period_mths` | instalments per year; months between them, `p = 12/m` |
| `D`, `G` | `defer_mths`, `guar_years` | deferment in months; guarantee period in years |
| `SP`, `SP_net` | `single_prem`, `net_single_prem` | *Einmalbeitrag*; `SP(1 − α)` |
| `α`, `β` | `expense_load_alpha`, `expense_load_beta` | acquisition and annuity-administration loadings |
| `i`, `v` | `tariff_int_rate` | tariff *Rechnungszins*; `v = 1/(1 + i)` |
| `R` | `annuity_pp_derived`, `annuity_guar_pp(t)` | the *garantierte Rente* per instalment |
| `U(t)`, `A(t)` | `annuity_surp_pp`, `annuity_pp` | *Überschussrente* instalment; total instalment `R + U(t)` |
| `u₀`, `ψ` | `surplus_init_pct`, `surplus_growth` | opening surplus fraction; its annual growth |
| `x_a(t)`, `x_s(t)` | `age(t, 1)`, `age(t, 2)` | attained ages of annuitant and second life |
| `g_a`, `g_s` | `birth_year(1)`, `birth_year(2)` | birth years — the generational keys |
| `λ(x)` | `improve_rate_at_age` | annual mortality improvement rate at age `x` |
| `q⁽¹⁾`, `q⁽²⁾` | `mort_rate_tariff`, `mort_rate` | annual first-order and second-order rates |
| `l_a`, `l_s` | `lives_if(t, 1)`, `lives_if(t, 2)` | second-order survival to the **start** of month `t` |
| `l̃` | `tariff_lives` | first-order survival, used only in the pricing sums |
| `d_a`, `d_s` | `lives_death(t, life)` | deaths during month `t`, `= l(t) − l(t + 1)` |
| `γ(t)` | `certain_floor` | 1 while the *Rentengarantiezeit* runs, else 0 |
| `δ` | `surv_pct` | survivor's percentage; 0 when the rider is off |
| `F(t)` | `payment_factor` | expected instalments payable at `t`, per unit of `pols_if_init` |
| `C(t)`, `K(t)` | `cum_annuity_guar_pp`, `refund_pp` | cumulative guaranteed instalments; the refund then due |
| `ä` | `annuity_factor` | value at `t = 0` of one unit of instalment on the tariff basis |
| `ω`, `ρ_M` | `omega_age`, `mix_male` | limiting age; portfolio male share |
| `c_e`, `c_p`, `π` | `expense_maint_pp`, `expense_pay_pp`, `expense_infl` | maintenance p.a.; per-instalment cost; inflation |
| `E₀` | — | acquisition expense incurred at `t = 0` |

`q`, `λ`, `l`, `γ`, `F` are dimensionless; `SP`, `R`, `U`, `A`, `K`, `C` and every cash flow are EUR;
`ä` is dimensionless (a value per unit of instalment). Note that `ä` is **not** the market's `a12`:
`a12 = ä / m`, so the research file's `a12(65, 1,00 %) = 20.426` corresponds to `ä = 245.11`.

### The projection frame, `t` and `proj_len()`

    horizon_mths(life) = 12 × ( omega_age − entry_age(life) )
    t_start()          = duration_mth_init()
    proj_len()         = max( horizon_mths(1) − 1,
                              first_pay_mth() + 12 × guar_years() − 1,
                              horizon_mths(2) − 1   if surv_pct > 0 )

`proj_len()` is the **last projected month index**, so `result_cf()` is indexed `t₀ … n` inclusive and
`result_cf().index[-1] == proj_len()` — the library's ruling, asserted for every model point. The
three terms are the annuitant's survival horizon, the guarantee period's own end, and the second
life's horizon where a *Hinterbliebenenrente* is in force. **All three are needed.** Stopping on the
annuitant's horizon alone truncates a younger survivor's tail (pitfall 18); stopping on the
guarantee alone truncates the life annuity. On the anchor cell `horizon_mths(1) = 12 × (121 − 65) =
672`, the guarantee ends at month 120, and `proj_len() = 671`, so the frame carries **672 rows**.

The frame **starts** at `t₀`, which is a product fact and is not asserted by the conventions suite:
a new-business point opens at 0 and an in-force point at the duration it has already run. What is
asserted is **contiguity** — a gap in `t` means a period was dropped, and no reading of `proj_len()`
would catch it.

### Generational mortality construction

    q(x, s, g, b) = mort_rate_at_age(x, s, b) × ( 1 − improve_rate_at_age(x, b) )^( g + x − 2025 )

    mort_rate_at_age(x, "U", b) = ρ_M · q_tab(x, "M", b) + (1 − ρ_M) · q_tab(x, "F", b)

    mort_rate(t, life)          = q( x(t, life), sex(life), g(life), "SECOND" )        — projection
    mort_rate_tariff(t, life)   = q( x(t, life), "U",       g(life), "FIRST"  )        — pricing
    mort_rate_mth(t, life)      = 1 − (1 − mort_rate(t, life))^(1/12)                  **[std]**
    lives_if(t, life)           = lives_if(t − 1, life) × (1 − mort_rate_mth(t − 1, life)),  lives_if(0) = 1
    lives_death(t, life)        = lives_if(t, life) − lives_if(t + 1, life)
    tariff_lives(k, life)       = tariff_lives(k − 1, life) × (1 − mort_rate_tariff_mth(k − 1, life)),  = 1 at k = 0

Three properties matter and each is a test. **`q` depends on `t` only through the attained age and on
the model point only through the cohort**, so two points with the same entry age and different birth
years read different rates at the same age (pitfall 7). **The improvement is inside the surface**, not
applied on top of a period rate as a separate factor keyed to the projection year — that would walk
diagonally across cohorts and is the classic error (pitfall 8). And **the pricing basis and the
projection basis are different objects**: `mort_rate_tariff` is first order and unisex,
`mort_rate` second order and sex-specific, and `mort_rate_tariff(t, life) < mort_rate(t, life)` at
every `t` (pitfall 9).

Because `q(120) = 1` in every series and `λ(120) = 0`, `lives_if` reaches exactly zero at
`horizon_mths(life)` and the decrements close: `Σ_t lives_death(t, life) = lives_if(t₀, life)` with
`lives_if(n + 1, life) = 0`. That is `check_lives_roll_fwd()`.

### Payment months, the certain floor and the payment factors

    pay_period_mths()   = 12 // payment_freq()                                  ( p )
    first_pay_mth()     = defer_mths()                    under `advance`
                        = defer_mths() + pay_period_mths()  under `arrears`
    is_payment_mth(t)   = ( t ≥ first_pay_mth() )  and  ( (t − first_pay_mth()) mod p == 0 )
    guar_end_mth()      = first_pay_mth() + 12 × guar_years()
    certain_floor(t)    = 1 if first_pay_mth() ≤ t < guar_end_mth() else 0

    payment_factor(t)   = max( γ(t), l_a(t) )  +  δ · (1 − l_a(t)) · l_s(t) · (1 − γ(t))

**The survival index of a payment is `t` under both timings.** With month starts as the payment
instants, an advance instalment for month `t` and an arrears instalment covering `[t − p, t)` are both
paid at the start of month `t` and both require the payee to be alive then. So the two conventions
differ **only in which months carry an instalment**, and a `G`-year guarantee covers `G × m`
instalments under either — which is exactly what `guar_end_mth()` encodes, since `G · m · p = 12G`
regardless of `m` (pitfall 13).

**The `max` is what makes the *Rentengarantiezeit* a certain floor rather than a second stream.**
While the guarantee runs the full instalment is payable whether the annuitant is alive or not [R23];
an additive `γ + l_a` would pay `1 + l_a` for the whole guarantee, nearly doubling the outgo in the
first years (pitfall 3). The survivor leg is gated by `(1 − γ(t))` for the same reason: inside the
guarantee the full instalment already goes out, so adding the survivor's percentage on top would pay
`1 + δ` (pitfall 4).

The survivor gate is `(1 − l_a(t)) · l_s(t)` — the probability that the annuitant is dead and the
second life alive at the payment instant, **assuming independence [std]**. The *Anwartschaft* lapsing
on the second life's prior death needs no separate rule: `l_s(t)` is already zero then.

### Conversion — the guaranteed annuity struck at inception

    ä  =  Σ over payment months k  of  v^(k/12) · F̃(k)

where `F̃(k)` is `payment_factor(k)` computed on the **first-order** survival path `l̃` rather than on
`l`. Then, where the refund is not elected,

    net_single_prem() = SP × (1 − α)
    annuity_pp_derived() = SP_net / ( ä × (1 + β) )

and `annuity_guar_pp(t) = annuity_pp_init()` where that is positive, else `annuity_pp_derived()`,
level for the whole of the annuity's life [S6] [REG-R27].

`ä` is a **pricing quantity and must stay acyclic**: it depends on the tariff basis, the elected
options and the tariff interest rate, and on nothing that depends on the path. In particular it does
**not** depend on `surplus_form` — the *Überschussrente* is financed out of surplus actually earned,
not priced into the guarantee (pitfall 1's neighbour), so `annuity_pp_derived()` is invariant to
`surplus_form` and `check_equivalence()` closes on every derived point regardless of it.

`check_tariff_int_rate()` asserts `tariff_int_rate() ≤ max_tariff_int_rate() + roll_fwd_tol`, the cap
being read from `hoechstrechnungszins_table.csv` at `entry_year()` [REG-R14] [REG-R15]. The cap binds
the *reserving* rate and, through § 138 Abs. 1 VAG, the rate a new tariff may be priced at [REG-R8];
a carrier may price below it and one is observed doing so [S6], which is why the check is an
inequality.

### The *Kapitalrückgewähr* and its implicit equation

Where `refund_form == "full"`, the death benefit at a death during month `t` is

    C(t) = C(t − 1) + ( R  if is_payment_mth(t) else 0 ),   C(−1) = 0
    K(t) = max( SP − C(t), 0 )

— the *Einmalbeitrag* less the **guaranteed** instalments already paid, floored at zero **[std]**
(research gap 10). `C(t)` includes the instalment due at `t` itself, because that instalment was paid
at the start of the month in which the death occurred.

The pricing equation is then **implicit in `R`**, because `K` depends on `R` and the point at which
`K` reaches zero depends on `R` too:

    g(R) = R · ä · (1 + β)  +  Σ_t v^(t/12) · d̃_a(t) · max( SP − n(t)·R, 0 )   =   SP_net

with `n(t)` the number of instalments paid by month `t` and `d̃_a` the first-order death density.
`g` is increasing in `R` on `(0, R_max]` where `R_max = SP_net / (ä (1 + β))` is the no-refund
annuity, and `g(0) = SP · Σ v^(t/12) d̃_a(t) < SP_net` on any basis with a positive interest rate, so
a root exists and **bisection on `[0, R_max]` converges**. The reference implementation bisects to
`solve_tol` in at most `solve_max_iter` steps, evaluating the sum inline from the cached
`tariff_lives` path rather than through a cells parameterized by the trial `R`.

**Computing `R_max` and then subtracting a refund cost is a different — and wrong — answer** (pitfall
5). `refund_pv()` is published so the identity can be seen: `check_equivalence()` asserts
`SP_net == annuity_pp_derived() · ä · (1 + β) + refund_pv()` to `roll_fwd_tol`.

During an *Aufschubzeit* no instalment has been paid, so `C(t) = 0` and `K(t) = SP`: the same
machinery gives the *Beitragsrückgewähr* on death before *Rentenbeginn* without a second mechanic,
and `refund_form == "none"` on a deferred point gives the pure deferred annuity in which the fund of
those who die is forfeited to the survivors.

### The *Überschussrente*

    U(t) = R · u₀ · (1 + ψ)^( policy_year(t) − defer_years() )      for t ≥ first_pay_mth()
         = 0                                                        otherwise
    A(t) = R + U(t)

with `u₀` and `ψ` read from `surplus_scale_table.csv` at `surplus_form()`. Two properties are
asserted. **It steps at the policy anniversary, not monthly**: `U(t)` is constant across each block of
twelve months (pitfall 14). And **it ratchets**: `A(t) ≥ A(t − 1)` at every `t`, which is what the
*Bonusrente* crediting mechanic means arithmetically — an increment bought as paid-up annuity does not
come back off [R23] (pitfall 15). Both are `check_annuity_roll_fwd()`.

`U(t)` is an **insurer-discretionary current** quantity, never a guaranteed cash flow. A projection is
a central estimate of a stream the insurer may reduce [R21]; the sensitivity section prices the
downside rather than the model reserving for it.

### Expected cash flows in month `t`

**Premium.** One inflow, and only on a new-business point, because an in-force point's frame does not
contain `t = 0`:

    premiums(t) = SP × pols_if_init      if t == 0,  else 0

**Annuity payments and guarantee claims.** The instalment splits into a payment to a living payee and
a payment to a beneficiary inside the guarantee:

    annuity_payments(t, "ANNUITANT") = pols_if_init · A(t) · l_a(t)                        · 1{payment month}
    annuity_payments(t, "SURVIVOR")  = pols_if_init · A(t) · δ (1 − l_a(t)) l_s(t) (1 − γ(t)) · 1{payment month}
    claims(t, "GUARANTEE")           = pols_if_init · A(t) · γ(t) · (1 − l_a(t))            · 1{payment month}

so that, at every payment month,

    annuity_payments(t) + claims(t, "GUARANTEE") = pols_if_init · A(t) · payment_factor(t)

which is `check_payment_factor()`, and inside the guarantee `payment_factor(t) = 1` exactly, which is
`check_guarantee_certain()`. Splitting the stream this way is not cosmetic: it separates annuity outgo
from death outgo, which is the shape of the product, and it makes the two commonest errors — the
additive certain floor and the survivor paid on top of the guarantee — visible in a column rather than
buried in a total.

**Refund claims.**

    claims(t, "REFUND") = pols_if_init · K(t) · lives_death(t, 1)

**Expenses.**

    expenses(t) = 1{t = 0} · pols_if_init · ( expense_acq_rate · SP + expense_acq_fixed )
                + ( c_e / 12 ) · infl_factor(t) · pols_if(t)
                + 1{payment month} · c_p · infl_factor(t) · pols_if_init · payment_factor(t)

The acquisition term appears only at `t = 0` and therefore only on a new-business point. The
per-instalment term is weighted by `payment_factor(t)`, not by `pols_if(t)`: a survivor's annuity in
payment is a **second** payment run, and inside the guarantee the beneficiary's instalment costs the
same to pay as the annuitant's.

**Obligation weight and the net flow.**

    pols_if(t)      = pols_if_init · min( 1, max( γ(t), l_a(t) ) + 1{δ > 0} (1 − l_a(t)) l_s(t) )
    liability_cf(t) = annuity_payments(t) + claims(t) + expenses(t) − premiums(t)
    net_cf(t)       = − liability_cf(t)

`net_cf` is **income-positive**, the library-wide convention, and `liability_cf` carries these notes'
outgo-positive orientation; both are published as columns rather than one standing for the other.

`result_cf()` publishes, indexed by `t`, in this order: **`pols_if`, `premiums`, `annuity_payments`,
`claims_guarantee`, `claims_refund`, `expenses`, `liability_cf`, `net_cf`**. A second frame
`result_pols()` publishes `lives_if_1`, `lives_if_2`, `certain_floor`, `payment_factor`,
`annuity_guar_pp`, `annuity_surp_pp`, `annuity_pp`, `refund_pp`, `cum_annuity_guar_pp` and `pols_if`.

### Published `check_*` identities

Nine, each returning a `bool` over all `t` and, where a per-period residual exists, publishing it at
`check_*_resid(t)`. The library's first ruling makes `check_net_cf()` mandatory; the rest are this
product's own roll-forward and pricing identities.

| Check | Identity |
|---|---|
| `check_net_cf` | `net_cf(t) == premiums(t) − pols_if_init·A(t)·payment_factor(t) − claims(t,"REFUND") − expenses(t)`. **Not a restatement of the definition**: it rebuilds the annuity outgo through the `max()` payment factor rather than through the two published legs, so it asserts that the split into `annuity_payments` and `claims_guarantee` is exhaustive and non-overlapping |
| `check_lives_roll_fwd` | `lives_if(t + 1, life) == lives_if(t, life)·(1 − mort_rate_mth(t, life))`, and `Σ_t lives_death(t, life) + lives_if(n + 1, life) == lives_if(t₀, life)` for each life in scope |
| `check_annuity_roll_fwd` | `annuity_surp_pp(t) == annuity_surp_pp(t − 1) · (1 + ψ)^{1 if t % 12 == 0 else 0}` inside the payment phase, and `annuity_pp(t) ≥ annuity_pp(t − 1)` at every `t` — the *Bonusrente* ratchet |
| `check_refund_run_off` | `refund_pp(t) == max(refund_pp(t − 1) − R·1{payment month}, 0)`, non-increasing and reaching zero at `⌈SP / R⌉` instalments; identically zero where `refund_form == "none"` |
| `check_payment_factor` | `annuity_payments(t) + claims(t,"GUARANTEE") == pols_if_init · A(t) · payment_factor(t)` at every payment month, and zero at every other |
| `check_guarantee_certain` | `payment_factor(t) == 1 + δ·0 == 1` at every payment month with `t < guar_end_mth()` — the instalment is certain inside the *Rentengarantiezeit* [R23] |
| `check_equivalence` | `net_single_prem() == annuity_pp_derived()·ä·(1 + β) + refund_pv()` to `roll_fwd_tol`. Returns `True` where `annuity_pp_init() > 0`, the annuity having been struck on a basis this model does not reproduce; the notes say so rather than letting it pass silently |
| `check_death_option_xor` | `refund_form() == "none"` **or** (`guar_years() == 0` **and** `surv_pct() == 0`) — the **[std]** exclusivity of research gap 10, asserted rather than assumed |
| `check_tariff_int_rate` | `tariff_int_rate() ≤ max_tariff_int_rate() + roll_fwd_tol`, the cap read at `entry_year()` [REG-R14] [REG-R15]. An inequality, not an equality: a carrier may price below the cap and one is observed doing so [S6] |

### Monthly processing order

For `t = t₀ … n`, in this order:

1. **Once, before the loop:** read the model point; check `tariff_int_rate()` against the vintage cap
   [REG-R15]; compute `first_pay_mth()`, `guar_end_mth()` and `pay_period_mths()`; build the tariff
   survival path `l̃` on the first-order unisex basis; compute `ä`; and strike `R` — directly where
   `annuity_pp_init() > 0`, by `SP_net / (ä (1 + β))` where no refund is elected, and by bisection on
   the implicit equation where one is.
2. Set the attained ages `x_a(t)`, `x_s(t)` from `entry_age + t // 12`, and read `q⁽²⁾` from the
   generational surface at each life's own cohort and sex.
3. Advance the second-order survival: `l_a(t)`, `l_s(t)` from `l(t − 1)` and `mort_rate_mth(t − 1)`.
4. Set `γ(t)` and `is_payment_mth(t)`.
5. Set the instalment: `U(t)` from the surplus form and the completed policy year, then
   `A(t) = R + U(t)`. Accumulate `C(t)` and set `K(t) = max(SP − C(t), 0)`.
6. Compute `payment_factor(t)` at the payment instant `t`.
7. **Start of month — premium.** At `t = 0` only, `premiums(0) = SP · pols_if_init`.
8. **Start of month — instalments.** `annuity_payments(t, ·)` and `claims(t, "GUARANTEE")` on the
   factors of step 6.
9. **During the month — deaths.** `lives_death(t, life) = l(t) − l(t + 1)`; settle
   `claims(t, "REFUND")` on `K(t)`, which is already net of the instalment paid at step 8.
10. **Expenses.** Acquisition at `t = 0`; maintenance on `pols_if(t)`; the per-instalment cost on
    `payment_factor(t)` where step 4 found a payment month.
11. Form `liability_cf(t)` and `net_cf(t)`; roll `l`, `C` and `U` forward to `t + 1`.

At `t = n` the projection ends with no maturity payment and no tail state: `l_a(n + 1) = 0` and the
guarantee has expired, so nothing remains to be paid.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one
becomes a test.

1. **Projecting only the guaranteed annuity.** The *Überschussrente* is not guaranteed, but it **is** a
   projected cash flow — on typical market designs 15 % to 25 % of the payment [unverified] [R21]. A
   model publishing only `annuity_guar_pp` models less than the payment. Assert `annuity_pp(t) >
   annuity_guar_pp(t)` at every `t` on any point with `surplus_form != "none"`, and exact equality on
   model point 14, which switches surplus off.
2. **Decrementing the guaranteed instalments during the *Rentengarantiezeit*.** Inside the guarantee
   the payment is **certain** [R23]. Assert `annuity_payments(t) + claims(t, "GUARANTEE") ==
   pols_if_init() × annuity_pp(t)` for every payment month with `t < guar_end_mth()`, exactly.
3. **Adding the certain floor instead of taking a max.** `γ + l_a` pays `1 + l_a` for the whole
   guarantee — on the anchor cell, nearly double the outgo for ten years. Assert `payment_factor(t)
   == 1.0` inside the guarantee where `surv_pct == 0`, and `≤ 1 + surv_pct` everywhere.
4. **Paying the survivor's annuity on top during the guarantee.** The survivor leg carries a
   `(1 − γ(t))` gate. Assert `annuity_payments(t, "SURVIVOR") == 0` for every `t < guar_end_mth()` on
   model point 5, and `> 0` for some `t` after it.
5. **Evaluating the *Kapitalrückgewähr* instead of solving it.** The equation is implicit in `R`.
   Assert `check_equivalence()` on model point 3, and that `annuity_pp_derived()` there differs from
   the naive `SP_net/(ä(1 + β))` less a refund cost computed at that annuity — the two answers are
   not the same number and the difference is not a rounding.
6. **Measuring the refund against the total annuity.** It is netted against the **guaranteed**
   instalments [std]. Assert `refund_pp(t)` is invariant to `surplus_form` — compare model point 3
   against a copy of it with the surplus switched off.
7. **Indexing the mortality surface by projection year instead of by birth year.** A period-table
   implementation reads age 66 in calendar year 2026 and walks diagonally across cohorts; a
   generational one reads `(g = 1960, x = 66)` whatever the projection year. Assert that two points
   with the same `entry_age` and different `birth_year` give **different** `mort_rate` at the same
   attained age.
8. **Shipping a period-table proxy at all.** A period proxy applied to a forty-year annuity
   understates the liability by a margin that dwarfs every other assumption [REG-R49]. Assert
   `mort_rate_gen(x, s, g, b) != mort_rate_at_age(x, s, b)` wherever `g + x != mort_base_year` and
   `improve_rate_at_age(x, b) > 0`, and that `ä` computed with `λ ≡ 0` is strictly smaller than `ä`.
9. **Applying the first-order margin to the level only.** For an annuity, prudence reaches the
   **trend** as well [REG-R47]. Assert `mort_rate_tariff(t, life) < mort_rate(t, life)` at every `t`,
   and that the ratio `mort_rate_tariff / mort_rate` **falls** with `t` — a level-only margin would
   hold it constant.
10. **Letting `sex` into the tariff.** German new business has been unisex since 21 December 2012
    [REG-R34]. Assert that two points identical but for `sex` produce the **same**
    `annuity_pp_derived()` and **different** `lives_if`.
11. **Counting the *Einmalbeitrag* on an in-force model point.** Assert `premiums(t) == 0` for every
    `t` in model point 10's frame, and `Σ premiums == single_prem() × pols_if_init()` on model
    point 1.
12. **Opening an in-force point at `t = 0`.** The frame starts at the duration already run. Assert
    `result_cf().index[0] == duration_mth_init()` and `pols_if(t_start()) == pols_if_init()` on model
    point 10, and that the acquisition expense appears nowhere in its frame.
13. **Getting the arrears offset wrong.** Under `arrears` the first instalment falls at
    `defer_mths() + p`, and a `G`-year guarantee still covers `G × m` instalments. Assert that model
    point 9 has no payment at `t = 0`, has one at `t = 1`, and carries the **same number** of
    guaranteed instalments as model point 1.
14. **Compounding the *Überschussrente* monthly.** It steps at the policy anniversary [S15]. Assert
    `annuity_surp_pp(t) == annuity_surp_pp(t − 1)` whenever `t % 12 != 0`, and that the step at
    `t % 12 == 0` is exactly `(1 + surplus_growth)`.
15. **Letting the total annuity fall.** The *Bonusrente* ratchets [R23]. Assert `annuity_pp(t) ≥
    annuity_pp(t − 1)` at every `t` — `check_annuity_roll_fwd()`.
16. **Discounting the published cash flows at the tariff *Rechnungszins*.** `i` reaches the projection
    **only** through `ä` and `refund_pv()`; the model publishes undiscounted flows and a best estimate
    discounts at the EIOPA curve [REG-R4]. Assert that `net_cf` for a given `annuity_pp_init` is
    invariant to `tariff_int_rate`, which isolates the one legitimate channel.
17. **Inventing a lapse, a surrender value or a paid-up state.** There are none [R1] [R2] [R5]
    [REG-R28]. Assert that no `lapse_rate`, `lapse_rate_mth`, `av_pp_at`, `cv_pp` or surrender cells
    exists, and that the decrements close: `Σ_t lives_death(t, life) + lives_if(n + 1, life) ==
    lives_if(t₀, life)` for each life in scope.
18. **Running the projection past the annuitant but not past the second life.** `proj_len()` takes the
    **maximum** of the two horizons and the guarantee's end. Assert that on model point 4 — annuitant
    65, second life 62 — `proj_len() == 12 × (omega_age − surv_age) − 1`, the survivor's horizon and
    not the annuitant's, and that `annuity_payments(proj_len())` is finite and non-negative there.

---

## Policyholder behaviour modelling

**There is none to model, and this is a cited product feature.** Once the *Rentenbezug* has begun the
policyholder has no right of termination, no *Rückkaufswert*, no *Beitragsfreistellung*, no capital
option and no transfer [R1] [R2] [R5] [REG-R28]. Every option this product has is elected **once, at
inception** and is thereafter a parameter rather than a decision: the *Rentengarantiezeit*, the
*Kapitalrückgewähr*, the *Hinterbliebenenrente*, the payment frequency and the *Überschussverwendung*
form. The model therefore carries **no lapse decrement, no dynamic behaviour formula and no
take-up rate**, and that absence is the reason its result depends more purely on the mortality basis
and the surplus assumption than any other model in this library.

Behaviour enters the **basis**, not the projection, as selection effects **[std]**:

- **Annuitisation anti-selection.** A *Sofortrente* is bought voluntarily, disproportionately by
  people who expect to live long, and the German market does **not** medically underwrite it
  (`product-spec.md` footnote 4, [unverified]). DAV 2004 R is an annuitant-experience table understood
  to carry *Selektionsfaktoren* for exactly that [REG-R49], so the effect belongs inside the basis
  rather than beside it — which is why this model applies **no annuitant adjustment factor** on top of
  the first-order table. A projection applying population mortality to an annuity book overstates
  deaths by a wide margin [REG-R52].
- **Sex self-selection and the direction of `ρ_M`.** A unisex tariff struck on sex-distinct tables is
  a better deal for women, so the realised female share of a voluntary annuitant portfolio sits above
  the population share. That is the direction, not the magnitude, of `ρ_M = 0.45`; **no carrier
  publishes a portfolio mix** (research gap 13).
- **Option selection.** The *Rentengarantiezeit* and the *Kapitalrückgewähr* are chosen
  disproportionately by buyers who expect to die early, the *Hinterbliebenenrente* by those with a
  younger spouse. Both push realised experience away from the tariff basis and **no source quantifies
  either** [unverified].
- **Two behaviours at the boundary, handled outside the projection.** *Proof of life*: failure to
  return the annual certificate suspends payment until it arrives — a timing effect on an unchanged
  obligation, **not modelled [std]**. And the *Aufschubzeit* window, in which a surrender right may
  survive because the termination bar has not yet bitten [R1] [R2]: **no carrier's terms were
  established** (research gap 17), and the base run switches the deferment off.

---

## Worked example

**Configuration.** Model point 1, the anchor cell, is the representative design of `product-spec.md`
with every attribute stated: `policy_id = SOF-000001`; `single_prem = 100,000.00 €`;
`entry_age = 65`; `entry_year = 2025`; `birth_year = 1960`; `sex = M`; `defer_years = 0`, so
`defer_mths() = 0` and `first_pay_mth() = 0`; `guar_years = 10`, so `guar_end_mth() = 120` and the
first 120 monthly instalments are certain; `refund_form = none`; `surv_pct = 0.00`, with `surv_age`,
`surv_birth_year` and `surv_sex` unused and carried as zeros; `payment_freq = 12` and
`payment_timing = advance`, so an instalment falls at the start of every month from `t = 0`;
`tariff_int_rate = 0.0100`, the *Höchstrechnungszins* in force for 2025 business [REG-R15];
`surplus_form = teildynamisch`; `annuity_pp_init = 0.00`, so the guaranteed annuity is **derived by
equivalence**; `duration_mth_init = 0`, so the frame opens at `t = 0`; and `pols_if_init = 1.0`.
Hence `horizon_mths(1) = 12 × (121 − 65) = 672`, `proj_len() = 671`, and the frame runs
`t = 0 … 671` — **672 monthly rows**, the whole of the projection.

**Assumptions, each tagged.** *Tariff.* Acquisition loading `α = 2,5 %` of the *Einmalbeitrag*
**[std]** and annuity administration loading `β = 2,0 %` of the annuity value **[std]**, so
`net_single_prem() = 97,500.00 €`. Tariff *Rechnungszins* `i = 1,00 %` [REG-R15], discounting monthly
at `v^(k/12)` with `v = 1/1.01`. *Mortality.* The base tables are the research file's Gompertz–Makeham
law `q_base(x) = 1 − exp(−(A + B·c^x·(c − 1)/ln c))` with `A = 0.0002`, `B = 1.5 × 10⁻⁵`, `c = 1.10`
**[std]**, split by sex as `FIRST/M = 1.250000 × q_base` and `FIRST/F = 0.795455 × q_base` so that the
`mix_male = 0.45` **[std]** unisex blend reproduces `q_base` exactly, and the second-order series
`SECOND = 1.20 × FIRST` **[std]**; improvement `λ_SECOND(x) = 1,5 %` to age 70, tapering linearly to
zero at 105, with `λ_FIRST = 1.25 × λ_SECOND` **[std]**; base year `mort_base_year = 2025` **[std]**,
so the annuitant's cohort exponent at age 65 is `1960 + 65 − 2025 = 0` and the anchor's first-year
tariff rate is the base rate unmodified; limiting age `omega_age = 121` **[std]** with `q = 1` at
attained age 120. Monthly rates by `1 − (1 − q)^(1/12)` **[std]**. The tariff factor `ä` is computed
on the **first-order unisex** path and the projection decrements on the **second-order male** path
[REG-R34] [REG-R47]. *Surplus.* `surplus_form = teildynamisch` gives `surplus_init_pct = 10 %` and
`surplus_growth = 1,0 %` p.a. **[std]**, so the *Überschussrente* opens at a tenth of the *garantierte
Rente* and steps up 1 % at each policy anniversary, ratcheting under the *Bonusrente* mechanic [R23].
*Expenses.* Acquisition `2,0 % of single_prem + 200 € = 2,200.00 €` at `t = 0` **[std]**; maintenance
`60 €` a year accrued monthly on `pols_if(t)` **[std]**; `1,50 €` per instalment paid **[std]**; all
three inflating at `expense_infl = 1,5 %` p.a., stepping at the policy anniversary **[std]**.
*Decrements.* Death only — no lapse, no surrender, no paid-up, no option exercise [R1] [R2] [R5].
*Tolerances.* `roll_fwd_tol = 1e-8`; the refund solve is not exercised on this cell.

All amounts in euros; `pols_if` and the survival probabilities to six decimals, cash flows to the
cent, and every total summed **at full precision and then rounded** rather than accumulated from
rounded cells.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are **cited, not reproduced**.

- **The HGB *Deckungsrückstellung*.** A prospective, deliberately prudent reserve on the
  *Rechnungsgrundlagen erster Ordnung* of the premium calculation — this contract's own
  *Rechnungszins*, capped at conclusion by § 2 DeckRV [REG-R14] [REG-R15], and a first-order
  biometric table [REG-R47] — formed to the extent necessary to ensure *dauernde Erfüllbarkeit*
  [REG-R54]. For a *Sofortrente* it is simply the actuarial present value of the remaining guaranteed
  annuity, since there are no future premiums to deduct: the same `ä` this model computes, evaluated
  at the attained age rather than at inception. **This is the balance sheet the German surplus system
  actually operates on** — the MindZV 90/90/50 floor [REG-R18], the RfB ring fence [REG-R10], the
  RfBV ceiling [REG-R19] and the § 139 VAG *Bewertungsreserven* test [REG-R9] are all computed on the
  HGB accounts, not the Solvency II ones.
- **The *Zinszusatzreserve*.** Where the § 5 Abs. 3 DeckRV *Referenzzins* falls below the contract's
  tariff rate, an additional HGB reserve arises [REG-R17]. It bites hardest on long-duration annuity
  business and on legacy cohorts: a model point written in 2012 at 1,75 % carries a very different ZZR
  from one written in 2025 at 1,00 %, which is one reason the shipped table carries both vintages. The
  ZZR is **not computed here**, and its release profile is the largest single driver of what a cohort
  of annuitants will actually be credited [REG-R17].
- **Solvency II best estimate.** Probability-weighted future cash flows discounted at the relevant
  risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6], with EIOPA publishing the
  curves [REG-R4]. `BEL = Σ_t v(t) × liability_cf(t)` over the recursions above. **No risk-free rate,
  cost-of-capital rate, contract-boundary rule or standard-formula shock in this library was read from
  a retrieved instrument**, so every such figure is **[std]** [REG-R2].
- **The contract boundary is not an open question on this product**, and that is worth saying because
  it is one on most of the others. A *Sofortrente* has a single premium already paid and no
  unilateral right on either side to alter or terminate the contract [R1] [REG-R28], so the whole
  projected stream sits inside the boundary. The one qualification is the *Aufschubzeit* variant,
  where a pre-*Rentenbeginn* surrender right may exist [R1] [R2] and no carrier's terms were
  established (research gap 17).
- **Longevity risk in the standard formula.** The life underwriting module's longevity shock is a
  permanent reduction in mortality rates, and it bites on this product harder than on any other in
  the library, there being no offsetting death benefit beyond a refund that *shrinks* as the annuity
  is paid. **No shock parameter was read from a retrieved instrument** [REG-R2].
- **IFRS 17.** Fulfilment cash flows plus a contractual service margin, effective for financial years
  beginning on or after 1 January 2023 [REG-R55]; a *Sofortrente* with an *Überschussbeteiligung* is
  a direct-participating contract and would fall under the Variable Fee Approach. The same
  expected-cash-flow engine feeds it; grouping, CSM, risk adjustment and coverage units are out of
  scope, and no delib model produces a CSM.

---

## Key sensitivities and model risks

In rough order of leverage for a German payout-annuity block:

1. **The mortality basis, in both dimensions.** This is a pure longevity bet and the basis is a
   **[std]** proxy, because DAV 2004 R is not public [REG-R47] [REG-R49]. Two numbers with no observed
   range decide most of the answer: the **first-order level margin** (`SECOND = 1.20 × FIRST`) and the
   **trend margin** (`λ_FIRST = 1.25 × λ_SECOND`). The trend is the more dangerous of the two over a
   fifty-six-year projection, because it compounds: at the anchor's `λ = 1,5 %` a 25 % change in the
   improvement rate moves the surviving cohort at age 90 by several per cent, and the annuity factor
   by more than a 25 % change in the level would. A user substituting a real table must replace the
   **surface**, not the level.
2. **The *Überschussrente* assumption.** On the anchor cell the *Überschussrente* opens at 10 % of the
   guaranteed annuity and grows 1 % a year, so by the twentieth policy year it is running at
   materially more than a tenth of the payment — and **none of it is guaranteed** [R21]. Two stresses
   matter and neither is in the base run: the constant form being reduced, which the consumer
   literature says happens when the insurer earns less than projected [R21]; and the ZZR release
   working the other way [REG-R17]. A model projecting a flat surplus rate has taken a view.
3. **The tariff *Rechnungszins* and the vintage.** On the [std] basis the 0,25 % → 1,00 % step is
   worth about +10 % on the guaranteed annuity at age 65 (`product-spec.md`, *Rentenhöhe*). Model
   points 1 and 13 differ in almost nothing else, so the pair isolates the effect; **the magnitude is
   constructed, not observed** (research gap 5).
4. **The payment timing convention.** *Vorschüssig* is **[std]** and unestablished (research gap 11),
   and it is worth about **5 %** of the annuity — larger than most assumption changes anyone would
   argue about. Model point 9 is the same cell in arrears and exists to make the difference
   measurable rather than assumed.
5. **The *Kapitalrückgewähr* solve.** Model point 3's guaranteed annuity is about 18 % below the plain
   life annuity on the [std] basis, and the reduction is sensitive to the interest rate in a way the
   plain annuity is not, because the refund is a *death* benefit discounted from an earlier date than
   the annuity payments it displaces. It is also the only place in the model where a numerical solve
   sits inside the pricing, so a change of `solve_tol` is a change of answer, not of runtime.
6. **The second life and the independence assumption.** The *Hinterbliebenenrente* is priced with both
   lives independent **[std]**; real joint lives are positively dependent, so the model **overstates**
   the joint-life annuity value and understates the cost of the rider. No delib source quantifies the
   dependence.
7. **`mix_male` and the unisex tariff.** The realised portfolio mix drives the *Risikoergebnis* the
   MindZV then shares [REG-R18] [REG-R34], and `ρ_M = 0.45` is a direction with no magnitude behind
   it. It moves the tariff annuity factor directly, so it moves every derived annuity in the table.
8. **Expense levels on small tickets.** At model point 11's 25 000 € the [std] acquisition expense of
   `2,0 % + 200 €` is 700 € against a monthly annuity of the order of 175 €, and the fixed
   per-instalment cost is a materially larger share of the payment than at 100 000 €. That is the
   arithmetic behind the minimum *Einmalbeitrag*, and it means the per-policy expense assumption —
   not mortality — decides whether a small cell is viable.
9. **What is deliberately absent, and would change the answer.** The *Bewertungsreserven* share [S3]
   [REG-R24]; a commuted *Restgarantiezeit* settlement (research gap 10); a reduction of a declared
   *Überschussrente* [R21]; and any *Rentenanpassung* actually observed, of which the corpus contains
   **no specimen at any carrier for any year** [S15] (research gap 16). Each is named here so that a
   reader knows the projection's silence about it is a decision rather than an oversight.
