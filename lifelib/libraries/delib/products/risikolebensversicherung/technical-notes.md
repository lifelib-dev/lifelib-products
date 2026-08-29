# Technical Notes

**Status:** Draft, 2026-08-29 (all sources dated 2026-08-29; **none retrieved**).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`RLV_DE_A`**, **annual** grid — for the standardized composite German *Risikolebensversicherung*
defined in `product-spec.md` (same directory). This is not any single insurer's product. [S#]/[R#]
tags refer to the source list in `sources.md` (numbering carried from
`_research/risikolebensversicherung.md`; frozen); [REG-R#] tags refer to the cross-product reference
library `references/regulatory-and-actuarial-references.md` (its own R-numbering). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks claims no search
corroborated. Parameter values are identical to those in `product-spec.md`. Cells names,
model-point columns and CSV headers are English `lower_snake_case`; German terms of art keep their
German form in prose.

**Retrieval conditions.** **No document cited anywhere in these notes was retrieved**: direct HTTP
egress from the build environment is blocked, and the session's `WebSearch` budget was exhausted
before this product's research began. The only evidence in the file is **inherited corroboration**
from sibling delib research files, named where it applies. **A delib citation is a pointer, not a
certificate**, and **every price, charge, margin and behavioural level below is [std]**.

**One vocabulary decision, made once and used throughout.** Three unrelated things are called
"netto" in this product, and confusing them is the classic implementation error [mechanic 4]:

| Term as used | Means | Name used here |
|---|---|---|
| *Nettoprämie* / *Nettobeitrag* (**actuarial**) | The risk premium from the mortality and interest bases, **before** expense loadings | `prem_net_level_pp`, symbol `Gn` |
| *Nettobeitrag* / *Zahlbeitrag* (**consumer**) | The premium billed = *Bruttobeitrag* less the *Beitragsverrechnung*. **The market's dominant usage** | `prem_paid_pp`, symbol `P` |
| *Nettotarif* / *Honorartarif* (**distribution**) | A commission-free tariff sold through fee-based advice | not modelled |

**The bare word *Nettobeitrag* is never a parameter name in this library**, and `prem_net_pp` is on
the library's retired-names register.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — the billed
  *Zahlbeitrag*, death claims, expenses and commission — for a single-policy model point on an
  expected (probability-weighted) basis. **Discounting, the *Deckungsrückstellung*, Solvency II
  technical provisions and the SCR are referenced, never specified** (see *Valuation and reserve
  pointers*). The one place a discount rate appears is inside the **pricing** equivalence that
  strikes the *Bruttobeitrag* and the *Beitragsverrechnungssatz*, and inside the first-order
  *Deckungskapital* published as a pricing diagnostic. **Neither discounts a published cash flow.**
- **Projection frequency.** **Annual grid**, matching the contract's level annual *Bruttobeitrag*
  and its annual *Überschussdeklaration* [R5] [R6]. It is an approximation in exactly one respect
  that is worth naming: § 168 VVG makes the *Versicherungsperiode* follow the *Zahlweise*, so a
  monthly-paying contract is terminable monthly and its exits are **not** concentrated at
  anniversaries [R8] [REG-R28]. The annual grid books them at anniversaries and says so.
- **The frame is 1-based, and `t` counts policy years from issue.** Policy year `t` runs from the
  policy anniversary at duration `t − 1` to the anniversary at duration `t`, and covers attained age
  `x(t) = issue_age + t − 1`. A new-business model point opens at `t = 1`; **an in-force model point
  opens at `t = duration_y + 1`**, so that everything keyed to duration — the § 161 three-year
  window, the lapse table, the *Zillmerung* run-off — reads off `t` directly and needs no second
  clock. That is why `duration_y` is a model-point column rather than a re-based issue age.
- **`proj_len()` is the last projected period index**, equal to `policy_term`, the
  *Versicherungsdauer* in whole years — not a row count. `result_cf()` is indexed by `t` from
  `duration_y + 1` to `proj_len()` inclusive, contiguously, so the frame has
  `policy_term − duration_y` rows. This is frlib's ruling, which delib adopts and asserts in
  `tests/test_model_conventions_de.py`.
- **Cover ends at attained age `issue_age + policy_term`**, and the last covered policy year is the
  one at attained age `issue_age + policy_term − 1`. `cover_end_age` is **derived**, not carried, so
  the two cannot disagree.
- **Timing conventions [std].** *Zahlbeitrag* at the **start** of the policy year (annual in
  advance); acquisition cost and initial commission at issue, i.e. in the first projected period of
  a new-business point and **never** on an in-force point, where they are sunk; maintenance,
  collection and renewal commission at the start of the year on the opening in-force; **death claims
  and the claim expense at the end** of the policy year of claim; lapses at the end of the year,
  **after** the death decrement; expiry at the end of policy year `n`.
- **Age basis.** *Alter am Jahrestag* — the attained age at the policy anniversary, which is also
  the projection step. Germany has no counterpart to the French *différence de millésime*, where the
  rating age steps on 1 January irrespective of birth month; on a real-date implementation the offset
  here is at most a few months **[std]**.
- **No cash value anywhere.** § 169 Abs. 1 VVG confines the surrender-value duty to a life insurance
  whose insured event is certain to occur, which a term assurance's is not [R2] [REG-R28]. The model
  therefore has **no account value, no `av_pp_at`, no surrender cells and no paid-up state**, and
  `claims(t, "LAPSE")` and `claims(t, "MATURITY")` are structurally zero at every `t` — asserted by
  a published `check_no_cash_value()` rather than left to prose.
- **What is deliberately not modelled**, each stated so a reader does not go looking for it: the
  *Kriegsklausel* and the ABC clause, which are catastrophe-scenario provisions rather than
  best-estimate ones; the § 162 VVG forfeitures; the mental-illness exception to § 161; selective
  lapse and premium-shock lapse, which ship as switchable modules that are **off** in the base run;
  the *Summenzuwachs*, *verzinsliche Ansammlung* and *Todesfallbonus* surplus forms; every rider
  (UZV, BUZ, *Beitragsbefreiung*, *vorgezogene Todesfallleistung*, *Verlängerungs-* and
  *Umtauschoption*, *vorläufiger Versicherungsschutz*); and all taxation, which is documented in
  `product-spec.md` and computed nowhere.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  claims and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents and `pols_if` to six decimals **[std]**. Totals are summed **at full precision and then
  rounded**, never summed from rounded cells.

### External inputs

Inputs are **external CSVs in the model folder's parent** — the `annuallife/TradLife_A` layout, not
`basiclife/BasicTerm_S`'s embedded IOSpec — read by an unparameterized `Data` Space so each file is
read **once per model** rather than once per model point. **Every file but the model point table
carries a per-row `provenance` column**, which is delib's second ruling and is machine-checked.

| File | Index columns | Value columns | Provenance |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the 18 model-point attributes below | **exempt** — a model point is a configuration, not an assumption |
| `mort_table.csv` | `table_id`, `sex`, `smoker`, `age` | `mort_rate` (second-order annual death rate) | per row |
| `benefit_schedule.csv` | `schedule_id`, `policy_year` | `benefit_factor` | per row |
| `nvg_schedule.csv` | `nvg_id`, `policy_year` | `sum_uplift` (cumulative multiplier on the sum insured) | per row |
| `lapse_table.csv` | `policy_year` | `lapse_rate` | per row |
| `freq_loading_table.csv` | `prem_freq` | `instalments`, `prem_freq_load` | per row |

Six files, no orphans: the conventions suite asserts that every CSV beside the model backs a
filename Reference in `Data` and that the set read by a full sweep is exactly the set registered in
`tests/de_registry.py`. Scalar assumptions are **References on `Projection`**, not rows in a table,
following `TradLife_A`; their values and tags are the assumption tables below.

---

## Model point attributes

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection` is parameterized by it | all |
| `policy_id` | str | Human-readable policy reference | all |
| `issue_age` | int | *Eintrittsalter* of the first *versicherte Person* | all |
| `sex` | enum {M, F} | Sex of the first life. **Decrement only — must never enter pricing** [R13] [REG-R34] | 1 vs 2 |
| `smoker` | enum {N, R} | *Nichtraucher* / *Raucher* of the first life; the largest rating split after age | 1 vs 3 |
| `sum_assured` | float EUR | Initial *Versicherungssumme*, `S0` | all |
| `policy_term` | int | *Versicherungsdauer* in whole years; equals `proj_len()` | all |
| `prem_term` | int | *Beitragszahlungsdauer* in whole years, `≤ policy_term` | 6 (12 < 20) |
| `premium_form` | enum {laufend, einmal} | Level *Bruttobeitrag* over `prem_term`, or a single *Einmalbeitrag* at issue | 7 |
| `prem_freq` | enum {jaehrlich, halbjaehrlich, vierteljaehrlich, monatlich} | *Zahlweise*; drives the *Ratenzahlungszuschlag* | 4, 5, 6, 10 |
| `benefit_schedule_id` | str | Key into `benefit_schedule.csv`: `konstant`, `linear_fallend`, `annuitaet_fallend_3pct` | 4, 5 |
| `nvg_schedule_id` | str | Key into `nvg_schedule.csv`: `keine`, `nvg_zwei_erhoehungen` | 9 |
| `surplus_form` | enum {beitragsverrechnung, keine} | Participating with *Beitragsverrechnung*, or the § 153-excluded non-participating tariff [R5] | 12 |
| `lives` | int {1, 2} | Single life, or *verbundene Leben* paying on the **first** death | 10 |
| `issue_age2` | int | *Eintrittsalter* of the second life; `0` where `lives = 1` | 10 |
| `smoker2` | enum {N, R, -} | Smoker status of the second life; `-` where `lives = 1` | 10 |
| `rating_factor` | float | *Risikozuschlag*: a multiplier on the **mortality basis**, both orders. 1.00 standard | 11 |
| `mort_table_id` | str | Key into `mort_table.csv`; one table shipped, `dav2008t_proxy` | all |
| `duration_y` | int | Completed policy years at the valuation date; `0` for new business | 8 |
| `issue_date` | date | Reporting only; the model runs on integer durations | none |

Three of these are worth a sentence each. **`sex` is carried and must not be priced on**: art. 5(2)
of the Gender Directive was struck down with effect from 21 December 2012 [R13] [REG-R34], while the
underlying DAV 2008 T tables remain sex-distinct [R12] [REG-R48]. The model resolves the tension the
only way § 138 VAG allows — **the tariff blends the two tables 50/50 and the projection uses the
policy's own sex** [R11] [REG-R8] — so the unisex cross-subsidy appears in the cash flows rather
than in the price. **`rating_factor` scales the mortality basis, not the price**: an impaired life
pays more *and* is expected to claim more, so the *Zahl/Brutto* ratio is nearly invariant to it; the
alternative reading, in which the loading is pure price and falls through to surplus, is pitfall 17.
**`duration_y` is the only thing that moves where the frame starts**, and it is what makes the § 161
window, the lapse table and the acquisition-cost switch all read off one clock.

### Model points shipped

Fourteen, covering both premium forms, all four payment frequencies, all three benefit schedules, an
in-force point, three options and three boundary cases. **Model point 1 is the worked example's
anchor cell.**

| # | Configuration | What it exercises |
|---|---|---|
| 1 | 35 M N, 300 000 € `konstant`, 25/25 y, `laufend`, `jaehrlich`, participating | **The anchor.** The representative composite |
| 2 | As 1 but `sex = F` | The unisex cross-subsidy: identical tariff, different projected claims |
| 3 | As 1 but `smoker = R` | The smoker split; the derived premium ratio against point 1 |
| 4 | 40 M N, 250 000 € `linear_fallend`, 20/20 y, `monatlich` | Falling sum; the 5 % *Ratenzahlungszuschlag* |
| 5 | 33 F N, 400 000 € `annuitaet_fallend_3pct`, 30/30 y, `vierteljaehrlich` | *Darlehensabsicherung* schedule; the 3 % loading |
| 6 | 45 M N, 200 000 € `konstant`, 20/**12** y, `halbjaehrlich` | *Abgekürzte Beitragszahlungsdauer*; the largest *Deckungskapital*; the 2 % loading |
| 7 | 50 M N, 100 000 € `konstant`, 10/**1** y, `einmal`, `jaehrlich` | The second premium form; the equivalence at its boundary |
| 8 | 30 F N, 150 000 € `konstant`, 30/30 y, `duration_y = 12` | **In force.** The frame opens at `t = 13`; past the § 161 window and the elevated lapse durations |
| 9 | 32 M N, 200 000 € `konstant`, 28/28 y, `nvg_zwei_erhoehungen` | *Nachversicherungsgarantie*; the § 161 clock restarting per increment |
| 10 | 38 M N + 36 F N, 300 000 € `konstant`, 22/22 y, `monatlich`, `lives = 2` | *Verbundene Leben*; the first-death rate |
| 11 | 42 M R, 250 000 € `konstant`, 18/18 y, `rating_factor = 1.75` | *Risikozuschlag* on an impaired smoker |
| 12 | 36 F N, 300 000 € `konstant`, 25/25 y, `surplus_form = keine` | The § 153-excluded tariff: `prem_rebate ≡ 0`, billed = guaranteed |
| 13 | 60 M N, 50 000 € `konstant`, 5/5 y | **Boundary.** Oldest entry, shortest term; the § 161 window covers three of five years |
| 14 | 18 M N, 100 000 € `konstant`, 40/40 y | **Boundary.** Youngest entry, longest term; cumulative lapse at its largest |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | `policy_term`; the last projected period index | once per model point |
| `age(t)` | Attained age of the first life in policy year `t` = `issue_age + t − 1` | annual |
| `age2(t)` | Attained age of the second life = `issue_age2 + t − 1`; unused where `lives = 1` | annual |
| `pols_if(t)` | In-force count at the **start** of policy year `t`; `pols_if(duration_y + 1) = pols_if_init() = 1` | annual recursion |
| `benefit_pp(t)` | *Versicherungssumme* in force in policy year `t` = `sum_assured × benefit_factor(t) × sum_uplift(t)` | schedule lookup |
| `benefit_paid_pp(t)` | The benefit actually payable on a year-`t` death, after the § 161 switch | annual |
| `mort_rate(t)` | **Second-order** annual death rate actually projected: policy's own sex, smoker, rated, first-death where `lives = 2` | lookup |
| `mort_rate_tar(t)` | **First-order** tariff rate: unisex 50/50 blend, `× (1 + m) × rating_factor` | lookup |
| `lapse_rate(t)` | Annual lapse rate applied after the death decrement; **0** at `t = proj_len()` | lookup |
| `suicide_factor(t)` | § 161 benefit switch, `< 1` inside three years of issue and of each increment | annual |
| `prem_gross_pp(t)` | *Bruttobeitrag* billed per in-force policy, loaded for frequency; **0** for `t > prem_term` | annual |
| `prem_rebate_pp(t)` | *Beitragsverrechnung* per in-force policy | annual |
| `prem_paid_pp(t)` | *Zahlbeitrag* per in-force policy = `prem_gross_pp − prem_rebate_pp` | annual |
| `res_pp_at(t, timing)` | First-order **net** *Deckungskapital* per policy — a **pricing diagnostic**, not a balance-sheet provision | prospective |
| `res_zill_pp_at(t, timing)` | The same reserve less the unamortised Zillmer balance; **negative for much of the term** | prospective |
| `pols_death(t)` | Expected deaths in policy year `t` = `pols_if(t) × mort_rate(t)` | annual |
| `pols_lapse(t)` | Expected lapses in policy year `t`, on survivors of the death decrement | annual |
| `pols_maturity(t)` | Expiring survivors; **0** except at `t = proj_len()` | annual |
| `premiums(t)` | `prem_paid_pp(t) × pols_if(t)` — the billed stream, the one inside `net_cf` | annual |
| `prem_gross(t)` | `prem_gross_pp(t) × pols_if(t)` — the **guaranteed** stream, published beside it | annual |
| `claims(t, kind)` | `kind ∈ {DEATH, LAPSE, MATURITY}`; the last two are structurally zero | annual |
| `expenses(t)` | Acquisition + maintenance + collection + claim expense | annual |
| `commissions(t)` | Initial *Abschlussprovision* + *Bestandspflegeprovision* | annual |
| `net_cf(t)` | Net liability cash flow, income-positive | annual |

There is **no** account-value state variable, **no** surrender-value state variable and **no**
paid-up state. That is a statutory fact about the product, not a modelling simplification
[R2] [R3] [R8] [REG-R28].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Death benefit | `benefit_pp(t)`, from any cause, subject only to the § 161 window | [R1] [R2] [S5] [S15] |
| Survival benefit | **None.** Nothing is paid at expiry | [R1] [R2] [S5] [S15] |
| Surrender / paid-up value | **None**, by the scope of § 169 Abs. 1 VVG; § 165 and § 166 both terminate in nil through the minimum-benefit test | [R2] [R3] [R8] [REG-R28]; scope [unverified] |
| Premium form | A **level *Bruttobeitrag*** over the *Beitragszahlungsdauer*, guaranteed for the term as the maximum the policyholder can ever be required to pay | [R6] [R10] [REG-R27] |
| What is billed | The *Zahlbeitrag* = *Bruttobeitrag* less the declared *Beitragsverrechnung*. **Not guaranteed**; § 153 confers an entitlement to participate, not to a level | [R5] [R6] [R9] [S5] [REG-R24] |
| Minimum surplus allocation | **90 % of the *Risikoergebnis***, from the MindZV. **No section number is cited**, the numbering being unsettled between the sibling research and the reference library | [R9] [REG-R18]; inherited corroboration; gap 4 |
| Equal treatment | *Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden* — one declared rate per tariff generation and rating cell | [R11] [REG-R8] |
| *Selbsttötung* | Insurer *leistungsfrei* where the *versicherte Person* intentionally takes her own life **within three years of conclusion**, unless in a state excluding free determination of the will; extendable by agreement; the substitute payment is the *Rückkaufswert*, which here is **nil** | [R1] [REG-R26]; inherited corroboration |
| Premium cessation | On death, and at the end of the *Beitragszahlungsdauer* | mechanics 4, 17 |
| *Rechnungszins* | **1,00 %** for new business from 1 January 2025, from the *Sechste Verordnung* of 19 July 2024 | [R10] [REG-R14] [REG-R15] |
| *Höchstzillmersatz* | **25 ‰ of the *Beitragssumme***, cut from 40 ‰ with effect from 1 January 2015; the rate at conclusion applies for the whole term | [R10] [REG-R16] [REG-R20] |
| Unisex | Sex may not enter the premium for contracts concluded from 21 December 2012 | [R13] [REG-R34] |
| Mortality table family | DAV 2008 T, with *R* and *NR* variants, **suitable for premium calculation** but not without a *Gesundheitsprüfung*; **values proprietary, not redistributed** | [R12] [REG-R48]; inherited corroboration |
| Premium tax | **None** — life insurance is exempt from *Versicherungsteuer*, so there is no premium-tax line | [R16] [unverified] |

### (b) Insurer-discretionary current elements

Thin, but decisive — on this product the discretion **is** the customer's bill.

| Input | Snapshot value | Basis |
|---|---|---|
| Declaration scaling `decl_scale` | **1.00**, i.e. the insurer declares exactly the MindZV minimum | **[std]** (1) |
| Surplus share `surplus_share` | **0.90** of the tariff mortality margin | [R9] [REG-R18]; choice of the minimum **[std]** (1) |
| Resulting `v_decl` (*Beitragsverrechnungssatz*) | **Derived, not assumed** — see the recursion section. Lands at about 0.43 on the anchor, so `Zahl / Brutto ≈ 0.57` | derived; inputs **[std]** |
| Cap on the declared rate `v_max` | **0.95** — a rebate may not exceed the premium | **[std]** (2) |
| *Kostenüberschuss* | **Not returned.** The tariff's β is 5,0 % and the modelled collection cost 3,0 %, so a cost result emerges in `net_cf` and stays there | **[std]** (3) |
| *Summenzuwachs*, *verzinsliche Ansammlung*, *Todesfallbonus* | **Off.** Only *Beitragsverrechnung* is implemented | mechanic 6; **[std]** |
| § 163 premium adjustment | **Off.** The *Bruttobeitrag* is fixed for the term | [R6] [REG-R27]; non-use [unverified] |

1. **Modelling the statutory minimum is the conservative choice for the *Zahlbeitrag***, and it is
   the only level any instrument fixes: no German carrier publishes a declaration for this product,
   and none was located (research gap 1). `decl_scale` is the stress lever — setting it to **0**
   raises the billed premium to the guaranteed one with no change to any claim, which is precisely
   the move § 163 does not govern [R6], and it is the model's representation of the product's single
   largest policyholder risk.
2. `v_max` binds nowhere in the shipped model points; it exists so that an extreme `m` cannot drive
   the billed premium negative, and so that `check_prem_split()` has a stated domain.
3. **The tariff loading and the modelled cost are deliberately different numbers, and the gap is the
   *Kostenüberschuss*.** Returning it would require splitting the *übriges Ergebnis* limb of the
   MindZV, whose minimum share is different and for which the research file gives no basis [R9]
   [REG-R18]. Not returning it is a **stated simplification** and pitfall 15, not an oversight.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German insurer publishes a mortality table, a
*Sicherheitszuschlag*, a best-estimate factor, an expense loading, a commission scale or a lapse rate
for this product, and none was retrieved [S3]–[S13] [R12] [R17].

**Mortality.** The regulatory basis is **DAV 2008 T** with its *R* and *NR* variants [R12]
[REG-R48], which is **cited by name and never shipped** — the tables are the property of the
Deutsche Aktuarvereinigung, are not public, and are not redistributed here. `mort_table.csv` is a
**[std] Gompertz-form proxy** for a medically selected insured-lives population:

    mort_rate(sex, smoker, x) = base(sex) × smoker_mult(smoker) × 1.095^(x − 30),   ages 18–80

    base(M) = 0.00040      base(F) = 0.00020
    smoker_mult(N) = 1.00  smoker_mult(R) = 2.20

Three anchors a replacement table must preserve, so that the worked example still closes. **The
50/50 unisex non-smoker blend is `0.00030 × 1.095^(x − 30)`**, which is the [std] best-estimate
scale the research file constructed and froze; **the female-to-male ratio is 0.50** at every age,
the order of magnitude reported for insured lives at the ages this product is sold [unverified]; and
**the smoker multiplier is 2.20**, the mid-point of the two-to-three range reported for insured-lives
smoker mortality at working ages [unverified], which reproduces a *premium* ratio near 2.04 once
sum-related and per-policy expenses are added back. The 9,5 % per year of age is the slope of the
research's construction; it is a fitted-in-spirit gradient with **no German source**, and on a
40-year run (model point 14) it is the single most exposed number in the file. **Population tables
are the wrong starting point for a replacement**: an RLV model built on a Destatis table without a
selection adjustment overstates claims by a wide margin at issue ages 25–45 [REG-R48] [REG-R52].

**The two-order split.** The first-order (tariff) rate is

    mort_rate_tar(t) = (1 + m) × [ ω·q_tab(M, smoker, x(t)) + (1 − ω)·q_tab(F, smoker, x(t)) ]
                       × rating_factor

with the *Sicherheitszuschlag* `m = 1.25` **[std]** and the unisex mix `ω = sex_mix_male = 0.50`
**[std]**. So `q1 = 2.25 × q2` **for the tariff's own unisex life**, and for a real policy the ratio
is `2.25 × (unisex blend / own-sex rate)` — **1.5 for a male and 3.0 for a female** on the shipped
proxy. That asymmetry is the unisex cross-subsidy, and it is a product fact, not a modelling
artefact. `m` is the single parameter that sets the *Brutto*/*Zahlbeitrag* spread; **its level is not
public** — the DAV *Richtlinie* regulates the **procedure** for setting the *Sicherheitszuschläge*,
not the level [R12] — and the argued range is **1.0 to 1.5** (research gap 6).

**Lapse.** No *Risikoversicherung*-specific rate exists anywhere in the research file (gap 13). The
inherited whole-market *Stornoquote* — 2,72 % (2024) and 2,56 % (2023) on the main GDV measure, with
a second irreconcilable measure at 1,2 % (2024) [R18] — is a book average dominated by long-dated
savings contracts and is **deliberately not used**. The shipped table is argued from three structural
features instead: **there is nothing to lose by lapsing**, no surrender value and no accumulated
bonus, so the financial friction that suppresses savings-contract lapse is absent; **the contract is
terminable at the end of each *Versicherungsperiode***, monthly for a monthly payer [R8], so exit is
frictionless in time as well as in money; and **the need that motivated the purchase amortises**.

| Policy year | 1 | 2–3 | 4+ | `proj_len()` |
|---|---|---|---|---|
| `lapse_rate(t)` **[std]** | 6 % | 4 % | 3 % | **0** |

**In the final policy year the lapse rate is zero.** Lapses fall at the end of the policy year, and
the end of policy year `n` is the moment cover expires — a lapse and an expiry are then the same
event paying the same nothing, so the whole surviving cohort is booked as `pols_maturity(n)`. **No
cash flow moves either way**, but the convention decides the split between `Σ pols_lapse` and
`pols_maturity(n)` and is load-bearing for the closure identity. The argued plausible range in the
early durations is **2 % to 8 %**, and **no German figure supports any of it**. Note the shape
argument the shipped table does *not* follow: because the need amortises, term-life lapse arguably
should **rise** in later durations rather than flatten, the opposite of a savings product's shape.
The research file ships the flat 3 % tail; that tension is recorded here and is a listed sensitivity
rather than a silent choice.

**Suicide share.** § 161 makes the insurer *leistungsfrei* for an intentional self-inflicted death
inside three years, substituting a *Rückkaufswert* that is nil here [R1] [R2]. The model applies

    suicide_factor(t) = 1 − suicide_share   for the first three policy years of a cover tranche
                      = 1                   thereafter,           suicide_share = 0.03  **[std]**

to **death claims only**. No German cause-of-death share was retrieved, and none is asserted; 0,03
stands for "about three per cent of deaths at these ages are suicides", with an argued range of
**0,01 to 0,05** [unverified]. It carries **three times the weight of the French one-year factor**
[`frlib` R1] simply because the window is three times as long, which is why the parameter is stated
rather than buried.

**Expenses and commission (all levels [std]; the structures are cited where they exist).**

| Input | Value | Basis |
|---|---|---|
| Acquisition cost, total | `zillmer_rate × prem_term × G` = **25 ‰ of the *Beitragssumme***, at issue | ceiling [R10] [REG-R16]; level **[std]** (4) |
| — of which initial commission `comm_rate_init` | **20 ‰ of the *Beitragssumme*** | **[std]** (4) |
| — of which other acquisition cost | **5 ‰ of the *Beitragssumme*** | **[std]** (4) |
| Tariff premium loading `beta_tariff` | **5,0 %** of each *Bruttobeitrag*, inside the equivalence | **[std]** (4) |
| Modelled collection cost `maint_prem_pct` | **3,0 %** of each *Zahlbeitrag* | **[std]** (4) |
| Renewal commission `comm_rate_renew` | **1,0 %** of each *Zahlbeitrag* from policy year 2 | **[std]** (4) |
| Sum-related admin `gamma_rate` | **0,30 ‰** of `benefit_pp(t)` a year | **[std]** (4) |
| Expense inflation `expense_infl` | **2,0 %** a year, on the sum-related admin only; the tariff's γ is level | **[std]** (5) |
| Claim expense `claim_expense` | **250 €** per death claim | **[std]** (4) |
| Best-estimate mortality factor `mort_be_factor` | **1.00** | **[std]** (6) |
| *Ratenzahlungszuschlag* `prem_freq_load` | 1.000 annual · **1.02** half-yearly · **1.03** quarterly · **1.05** monthly | convention **[std]** (7) |

4. **German term-life charge levels are structurally undisclosed, not merely unretrieved** (research
   gap 8): no *Effektivkostenquote*, because a reduction in yield presupposes a yield; no
   *Basisinformationsblatt*, because the product is not a PRIIP [R17]; and the
   *Produktinformationsblatt* quotes premiums, not loadings. The only figure any instrument fixes is
   the 25 ‰ Zillmer **ceiling**, and the composite **assumes a term tariff runs at the cap** — which
   **may well be wrong**, a slim direct-channel acquisition cost sitting far below it [S3] [S12].
   This is the single [std] charge most likely to be overstated, and the notes say so rather than
   letting a reader discover it from a sensitivity.
5. Inflating the modelled γ while the tariff's γ is level means the cost result narrows over a long
   term and eventually reverses — a real feature of a 25-year contract, and the reason model point 14
   (40 years) is worth its place.
6. Set to 1.00 so that the shipped proxy *is* the best estimate and there is exactly one unsourced
   mortality level rather than two stacked on each other. A user with experience data should move
   this rather than editing the table.
7. **2 % / 3 % / 5 % is a market convention with no carrier attribution**, inherited from the sibling
   delib research (gap 21). Whether German carriers strike it on the *Bruttobeitrag* or the
   *Zahlbeitrag* was not established; the model loads the **billed** amount, so the split identity
   holds at every frequency (pitfall 10).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, `t = t0 … n`, with `t0 = duration_y + 1` and `n = proj_len() = policy_term` |
| `x(t)`, `x₂(t)` | attained ages, `issue_age + t − 1` and `issue_age2 + t − 1` |
| `k` | `prem_term`, the *Beitragszahlungsdauer* in years |
| `S0` | `sum_assured` |
| `f(t)` | `benefit_factor(t)` from `benefit_schedule.csv` |
| `u(t)` | `sum_uplift(t)` from `nvg_schedule.csv`; `u ≡ 1` for `nvg_schedule_id = keine` |
| `B(t)` | `benefit_pp(t) = S0 · f(t) · u(t)` |
| `q̃(x)` | `mort_rate_at_age(table_id, sex, smoker, x)`, the shipped second-order table rate |
| `ω` | `sex_mix_male` = 0.50, the tariff's unisex mix **[std]** |
| `m` | `sicherheitszuschlag_m` = 1.25 **[std]** |
| `rf` | `rating_factor` |
| `q₂(t)` | `mort_rate(t)`, the projected second-order rate |
| `q₁(t)` | `mort_rate_tar(t)`, the first-order tariff rate |
| `w(t)` | `lapse_rate(t)`; `w(n) = 0` **[std]** |
| `σ(t)` | `suicide_factor(t)`, the § 161 benefit switch |
| `l(t)` | `pols_if(t)`, in force at the **start** of policy year `t`; `l(t0) = pols_if_init() = 1` |
| `p₁(t)` | tariff survivorship, mortality only: `p₁(1) = 1`, `p₁(t+1) = p₁(t)·(1 − q₁(t))` |
| `i`, `v` | `rechnungszins` = 1,00 %; `v = 1/(1 + i)` |
| `G`, `Gn` | `prem_gross_pp` before frequency loading; `prem_net_level_pp`, the actuarial *Nettoprämie* |
| `φ` | `prem_freq_load`, the *Ratenzahlungszuschlag* multiplier |
| `v_d` | `beitragsverrechnung_rate()`, the declared *Beitragsverrechnungssatz*, struck once at issue |
| `z`, `β`, `γ` | `zillmer_rate` = 0.025; `beta_tariff` = 0.05; `gamma_rate` = 0.00030 |
| `c₀`, `c_r` | `comm_rate_init` = 0.020 of the *Beitragssumme*; `comm_rate_renew` = 0.010 of the *Zahlbeitrag* |
| `a`, `π`, `ec` | `maint_prem_pct` = 0.03; `expense_infl` = 0.02; `claim_expense` = 250 |

`q₁`, `q₂` and `w` are dimensionless annual probabilities; `S0`, `B`, `G`, `P` and every cash-flow
component are EUR.

### The two mortality bases

    q₂(t) = mort_be_factor · rf · Q̃(t),        Q̃(t) = q̃(sex, smoker, x(t))                 lives = 1
    q₁(t) = (1 + m) · rf · [ ω·q̃(M, smoker, x(t)) + (1 − ω)·q̃(F, smoker, x(t)) ]

For `lives = 2` the two lives are combined **at table level, before any loading**, on an
independence assumption **[std]**:

    Q̃(t) = q̃_A(t) + q̃_B(t) − q̃_A(t)·q̃_B(t)

and the same combination is applied to the two unisex blends before `(1 + m)·rf`. Combining after
loading instead inflates the cross term and is pitfall 14. The independence assumption **understates**
the true first-death rate for a couple sharing a household, a vehicle and a lifestyle, and no German
figure bounds the understatement (research gap 15).

### The *Bruttobeitrag*, by first-order equivalence

Struck once, at issue, on first-order bases and tariff survivorship — never on the projection's own
lapse or best-estimate mortality, and therefore acyclic with respect to everything behavioural.
Write

    A  = Σ_{t=1..n} v^t · p₁(t) · q₁(t) · B(t)          APV of death benefits, paid at year end
    ä  = Σ_{t=1..k} v^(t−1) · p₁(t)                     premium annuity-due over the paying term
    Γ  = Σ_{t=1..n} v^(t−1) · p₁(t) · B(t)              sum-exposure annuity, for the γ loading

The equivalence, with the α loading a per-mille of the *Beitragssumme* `k·G` incurred at issue,

    G·ä  =  A  +  z·k·G  +  β·G·ä  +  γ·Γ

is linear in `G` and solves in closed form:

    G = ( A + γ·Γ ) / ( (1 − β)·ä − z·k )

For `premium_form = einmal`, `k = 1` and `ä = 1`, so the same expression returns the
*Einmalbeitrag* — the second premium form is the same engine at a boundary, not a second engine. The
actuarial *Nettoprämie* is `Gn = A / ä`, and it is what the reserve recursion below uses; it is
**not** a cash flow and never appears in `result_cf()`.

### The *Zahlbeitrag*, by the MindZV allocation

The tariff's own mortality margin in policy year `t`, per in-force policy, is the difference between
the first-order rate and the tariff's best estimate:

    margin_pp(t) = ( q₁(t) − q₁(t)/(1 + m) ) · B(t) = (m/(1+m)) · q₁(t) · B(t)

so its actuarial value at issue is exactly `(m/(1+m))·A`. The declared *Beitragsverrechnungssatz* is
struck once, at issue, to return `surplus_share` of it over the premium-paying term:

    v_d = min( v_max,  decl_scale · surplus_share · (m/(1+m)) · A / (G · ä) )

and is **0** where `surplus_form = keine`. Then, at every `t ≤ k`,

    prem_gross_pp(t)  = G · φ
    prem_rebate_pp(t) = v_d · G · φ
    prem_paid_pp(t)   = (1 − v_d) · G · φ

and all three are **0** for `t > k`. Substituting the equivalence into `v_d` gives the identity that
explains the whole German term-life spread in one line:

    v_d = decl_scale · surplus_share · (m/(1+m)) · [ 1 − β − ( γ·Γ + z·k·G ) / ( G·ä ) ]

— **the surplus share, times the margin fraction of the risk element, times the risk share of the
gross premium.** On the anchor's calibration the bracket is about 0.85, so
`v_d ≈ 1 × 0.90 × 0.5556 × 0.85 ≈ 0.43` and `Zahl / Brutto ≈ 0.57`, reproducing the research file's
frozen [std] ratio from the mechanic rather than assuming it. **Raising `m` raises `G` and `v_d`
together, which is why the *Bruttobeitrag* moves far more than the *Zahlbeitrag*** (product spec,
contractual mechanics).

### The § 161 benefit switch, and increments

The base cover's three-year window runs from issue, so it bites at `t ≤ 3`. A
*Nachversicherungsgarantie* increment granted at the start of policy year `t_j` carries **its own**
three-year window, `t_j ≤ t < t_j + 3` [R1] [unverified] (research gap 9). With
`Δu(t) = u(t) − u(t − 1)` and `u(0) = 0`, the effective benefit is

    benefit_paid_pp(t) = S0 · f(t) · Σ_{j : t_j ≤ t} Δu(t_j) · σ_j(t)
    σ_j(t) = 1 − suicide_share   if  t < t_j + 3,  else 1        (the base tranche has t_j = 1)

so `suicide_factor(t) = benefit_paid_pp(t) / benefit_pp(t)` is a **weighted average** across
tranches, strictly between `1 − suicide_share` and `1` in a year when one tranche is inside its
window and another is not. On an in-force model point with `duration_y ≥ 3` and no increments,
`σ ≡ 1` at every projected `t`. The switch **never** touches lapses or the expiry, both of which pay
nothing in any event.

### Decrements and the in-force recursion

Two decrements, applied in the stated order at the end of the policy year:

    pols_death(t)    = l(t) · q₂(t)
    pols_lapse(t)    = l(t) · (1 − q₂(t)) · w(t)                    with w(n) = 0
    pols_maturity(t) = 0  for t < n;   l(n)·(1 − q₂(n))  at t = n
    l(t+1)           = l(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t),    l(t0) = 1

so `l(n+1) = 0` exactly: **every exit lands inside the frame**, which is what lets `result_cf()` end
at `proj_len()` with nothing left over. **Closure identity**, which a test asserts:

    Σ_{t=t0..n} [ pols_death(t) + pols_lapse(t) + pols_maturity(t) ] = pols_if_init() = 1

### Benefits, expenses and net cash flow

    claims(t, "DEATH")    = benefit_paid_pp(t) · pols_death(t)
    claims(t, "LAPSE")    = 0                                        [R2] [R3] [R8]
    claims(t, "MATURITY") = 0                                        a term contract pays nothing at expiry
    claims(t)             = Σ_kind claims(t, kind)

    acq_pp   = z·k·G                                                  incurred once, at issue
    comm_pp  = c₀·k·G                                                 of which commission
    maint(t) = γ · B(t) · (1 + π)^(t−1)      +  a · prem_paid_pp(t)

    expenses(t)    = (acq_pp − comm_pp)·1{t = 1 and duration_y = 0}
                     + maint(t)·l(t) + ec·pols_death(t)
    commissions(t) = comm_pp·1{t = 1 and duration_y = 0} + c_r·prem_paid_pp(t)·l(t)·1{t ≥ 2}

    premiums(t)    = prem_paid_pp(t)·l(t)
    prem_gross(t)  = prem_gross_pp(t)·l(t)
    prem_rebate(t) = prem_rebate_pp(t)·l(t)

    net_cf(t)      = premiums(t) − claims(t) − expenses(t) − commissions(t)
    liability_cf(t) = −net_cf(t)

**Acquisition cost is a year-one outgo, not an annualised loading.** The tariff amortises it through
the equivalence; the cash flow incurs it at issue, which is the economic reason an early lapse hurts
on a product with no surrender value to forfeit (mechanic 10). On an **in-force** model point it is
sunk and is not incurred at all — which is why the switch tests `duration_y = 0` and not merely
`t = 1`.

### The first-order *Deckungskapital* — a pricing diagnostic

Published because mechanic 11's central claim is checkable and a naive implementation fails it, and
labelled a pricing quantity because it is one: it is **not** a *Deckungsrückstellung*, it is not
*gezillmert*, it enters no cash flow, and nothing in this library discounts a published cash flow.

    res_pp_at(t,"BEF_PREM") = Σ_{u≥t} v^(u−t+1)·(p₁(u)/p₁(t))·q₁(u)·B(u)
                              − Gn · Σ_{u=t..k} v^(u−t)·(p₁(u)/p₁(t))

with `res_pp_at(1,"BEF_PREM") = 0` by the equivalence, `res_pp_at(n+1,"BEF_PREM") = 0` by exhaustion,
and a strictly positive interior. `res_pp_at(t,"AFT_PREM") = res_pp_at(t,"BEF_PREM") + Gn·1{t ≤ k}`.
The Thiele recursion the check asserts is

    ( res_pp_at(t,"BEF_PREM") + Gn·1{t ≤ k} ) · (1 + i)
        = q₁(t)·B(t) + (1 − q₁(t))·res_pp_at(t+1,"BEF_PREM")

The *gezillmert* companion subtracts the unamortised Zillmer balance,

    res_zill_pp_at(t, timing) = res_pp_at(t, timing) − z·k·G · [ Σ_{u=t..k} v^(u−t)(p₁(u)/p₁(t)) ] / ä

which is **`−z·k·G` at `t = 1`** — negative from the first day, exactly as mechanic 10 describes, and
back to zero at expiry. Whether a negative individual reserve must be floored at zero for
balance-sheet purposes — the *Nullstellung* question — was **not established** [R21] [REG-R54]
(research gap 11), and because the model publishes no balance-sheet reserve, the question does not
reach its cash flows.

### What `result_cf()` publishes

Indexed by `t`, contiguous from `duration_y + 1` to `proj_len()`, in this order:

    pols_if, prem_gross, premiums, prem_rebate,
    claims_death, claims_lapse, claims_maturity,
    expenses, commissions, net_cf

`prem_gross` is the **guaranteed** stream and does not enter `net_cf`; `premiums` is the **billed**
stream and does. Publishing both is required by the product — a model carrying one premium stream
cannot represent a German RLV [R6] — and `check_net_cf()` names exactly which columns enter the
identity, so there is no ambiguity about which to skip.

### The published `check_*` identities

Five, each with a per-`t` residual companion `check_*_resid(t)`, each returning a `bool` over all
`t`, and all five called on **every** model point by the conventions suite.

| Check | Identity | Why it earns its place |
|---|---|---|
| `check_net_cf()` | `net_cf(t) = premiums(t) − claims(t) − expenses(t) − commissions(t)` | delib's first ruling: the headline number is reconciled in code, not only in prose |
| `check_pols_roll_fwd()` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t)`, and the three exits sum to `pols_if_init()` | The decrement roll-forward and its closure |
| `check_prem_split()` | `prem_gross_pp(t) = prem_paid_pp(t) + prem_rebate_pp(t)`, with `0 ≤ prem_rebate_pp(t) < prem_gross_pp(t)` where a premium is due and all three zero where none is | The product's signature identity, at every `t` and every *Zahlweise* |
| `check_res_roll_fwd()` | The Thiele recursion above, plus `res_pp_at(1) = 0` and `res_pp_at(n+1) = 0` | The reserve mechanic 11 says a naive implementation gets wrong |
| `check_no_cash_value()` | `claims(t,"LAPSE") = 0` and `claims(t,"MATURITY") = 0` at every `t` | A statutory fact [R2] [R3] [R8], checked on every model point rather than asserted in prose |

Two further identities are **scalar rather than per-period** and are therefore asserted in
`tests/test_risikolebensversicherung_de.py` instead of published as `check_*` cells: the first-order
premium equivalence `G·ä = A + z·k·G + β·G·ä + γ·Γ`, and the surplus equivalence
`v_d·G·ä = decl_scale·surplus_share·(m/(1+m))·A`. Forcing a scalar identity into a per-`t` residual
would mean inventing a per-period decomposition the product does not have, which is worse than
putting it in the test module and saying so.

---

## Annual processing order

For `t = t0 … n`, in exactly this order:

1. Set `x(t) = issue_age + t − 1` (and `x₂(t)` where `lives = 2`). If `t > n`, stop.
2. Read the schedules: `f(t)` from `benefit_schedule.csv`, `u(t)` from `nvg_schedule.csv`; form
   `B(t) = S0·f(t)·u(t)`.
3. Read the table rates for each life at its own attained age; combine to a first-death rate where
   `lives = 2`, **before** any loading; form `q₂(t)` on the policy's own sex and `q₁(t)` on the
   tariff's unisex blend.
4. **Start of year — premium in advance.** For `t ≤ k`, set `prem_gross_pp(t) = G·φ`,
   `prem_rebate_pp(t) = v_d·G·φ`, `prem_paid_pp(t)` as their difference; else all three zero. Take
   `premiums(t) = prem_paid_pp(t)·l(t)`.
5. **Start of year — expenses on the opening in-force.** Collection `a·prem_paid_pp(t)·l(t)` and
   sum-related admin `γ·B(t)·(1+π)^(t−1)·l(t)`; at `t = 1` **and only where `duration_y = 0`**, the
   acquisition cost and the initial commission; for `t ≥ 2`, the renewal commission.
6. Apply the § 161 switch tranche by tranche to get `benefit_paid_pp(t)`.
7. **End of year — death.** `pols_death(t) = l(t)·q₂(t)`;
   `claims(t,"DEATH") = benefit_paid_pp(t)·pols_death(t)`; claim expense on the deaths. Claimants
   have already paid the year's premium at step 4 — that is what "premium payment ceases at death"
   means on an annual-in-advance grid **[std]**, and applying a second `(1 − q₂)` factor to
   `premiums(t)` charges the rule twice (pitfall 11).
8. **End of year — lapse.** For `t < n`, `pols_lapse(t) = l(t)·(1 − q₂(t))·w(t)`;
   `claims(t,"LAPSE") = 0`. At `t = n`, `w(n) = 0` **[std]**.
9. **End of year — expiry.** At `t = n` only, `pols_maturity(n) = l(n)·(1 − q₂(n))`;
   `claims(n,"MATURITY") = 0`.
10. Roll forward `l(t+1)` and form `net_cf(t)`.

At `t = n` the projection ends with no maturity payment, no tail state and `l(n+1) = 0`.

---

## Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is wrong. **Each
one becomes a test** in `tests/test_risikolebensversicherung_de.py`.

1. **Confusing the three "netto"s.** *Nettoprämie* (actuarial), *Nettobeitrag*/*Zahlbeitrag*
   (consumer) and *Nettotarif* (distribution) are unrelated [mechanic 4]. Assert
   `prem_net_level_pp() < prem_paid_pp(1)/φ < prem_gross_pp(1)/φ` on the anchor, and that no cells
   is named `prem_net_pp` or `nettobeitrag`.
2. **Carrying only one premium stream.** A model with a single premium cannot represent this product
   [R6]. Assert `prem_gross(t) > premiums(t)` at every `t` with a premium due on model point 1, and
   `prem_gross(t) == premiums(t)` exactly on model point 12, where `surplus_form = keine`.
3. **Treating the *Zahlbeitrag* as guaranteed.** Only the *Bruttobeitrag* is [R6] [REG-R27]. Assert
   that setting `decl_scale = 0` raises `premiums` to `prem_gross` at every `t` and changes **no**
   claim, no decrement and no expense other than the collection cost that scales with the billed
   premium.
4. **Inventing a *Rückkaufswert*.** There is none [R2] [R3] [R8]. Assert
   `claims(t,"LAPSE") == 0.0` and `claims(t,"MATURITY") == 0.0` at every `t` and every model point,
   that `check_no_cash_value()` is `True`, and that no `av_pp_at`, `surr_value` or paid-up cells
   exists in `Projection`.
5. **Concluding there is no *Deckungskapital*.** A level premium against a rising death rate builds
   one (mechanic 11). Assert `res_pp_at(1,"BEF_PREM") == 0` and `res_pp_at(n+1,"BEF_PREM") == 0` to
   1e-9, that `res_pp_at(t,"BEF_PREM") > 0` at some interior `t` on the anchor, that
   `res_zill_pp_at(1,"BEF_PREM") == −z·k·G` exactly, and that `check_res_roll_fwd()` is `True`.
6. **Letting `sex` into the price.** Unlawful in Germany since 21 December 2012 [R13] [REG-R34].
   Model points 1 and 2 differ **only** in `sex`: assert their `prem_gross_pp(t)`,
   `prem_paid_pp(t)` and `beitragsverrechnung_rate()` are identical to 1e-12, while their
   `claims_death` totals differ by a factor near two.
7. **Applying the *Sicherheitszuschlag* to the projection.** `q₁` prices, `q₂` projects. Assert that
   `claims_death` is invariant to `sicherheitszuschlag_m` while `prem_gross` is not, and that
   `mort_rate_tar(t) / mort_rate(t)` equals `2.25 × (unisex blend / own-sex rate)` — 1.5 for a male,
   3.0 for a female on the shipped proxy — rather than 2.25 for both.
8. **Applying the § 161 switch beyond three years, or to the wrong things.** Assert
   `suicide_factor(t) == 1 − suicide_share` exactly for `t ∈ {1,2,3}` and `== 1` for `t ≥ 4` on model
   point 1; that it is `1` at every projected `t` on the in-force point 8 (`t0 = 13`); and that it
   touches neither `claims_lapse` nor `claims_maturity`, both of which are zero anyway.
9. **Forgetting that the clock restarts for a *Nachversicherungsgarantie* increment.** On model
   point 9, in the year of and the two years after each increase, assert
   `1 − suicide_share < benefit_paid_pp(t)/benefit_pp(t) < 1` strictly — the base tranche out of its
   window and the increment inside it.
10. **Mishandling the *Ratenzahlungszuschlag*.** `φ` multiplies the billed amount, so both premium
    streams and the rebate carry it. Assert `check_prem_split()` on every model point, and that
    `prem_gross_pp(1)` on model point 4 (monthly) is exactly `1.05 ×` the same cell recomputed at
    `jaehrlich` — a single loading, not one applied to each stream separately.
11. **Double-counting premium cessation at death.** Premiums are in advance and claims at year end,
    so a claimant has already paid. Assert `premiums(t) == prem_paid_pp(t) * pols_if(t)` exactly,
    with no `(1 − q₂)` factor anywhere.
12. **Running the premium past the *Beitragszahlungsdauer*.** On model point 6 (`k = 12`,
    `n = 20`) assert `prem_gross_pp(t) == premiums(t) == prem_rebate_pp(t) == 0` for `t = 13…20`,
    while `claims_death(t) > 0` there and `res_pp_at(t,"BEF_PREM")` is falling.
13. **Hard-coding a constant sum insured.** Two of the three German shapes fall (mechanic 3). Assert
    `benefit_pp(t)` is flat on point 1; falls linearly to `S0/n` on point 4; and on point 5 falls
    **slowly then fast**, `benefit_pp(2) − benefit_pp(1) < benefit_pp(n) − benefit_pp(n−1)` in
    absolute size — the property a linear schedule gets backwards.
14. **Combining two lives after loading instead of before.** On model point 10 assert
    `Q̃ == q̃_A + q̃_B − q̃_A·q̃_B` exactly and `Q̃ < q̃_A + q̃_B` strictly, and that `q₁` is
    `(1+m)·rf` times the combined **blend**, not the combination of two separately loaded rates.
15. **Returning the *Kostenüberschuss* as well as the *Risikoüberschuss*.** The model returns only
    the mortality margin; the cost result emerges in `net_cf` and stays there. Assert that
    `prem_rebate` is invariant to `maint_prem_pct` and `comm_rate_renew`, while `net_cf` is not.
16. **Taking the whole-market *Stornoquote* as the term-life lapse rate.** Structurally wrong
    [R18] (research gap 13). Assert `lapse_rate(1) == 0.06`, `lapse_rate(2) == lapse_rate(3) ==
    0.04`, `lapse_rate(4) == 0.03`, and that `lapse_rate(n) == 0` while the table's own row for
    year `n` still reads 0.03.
17. **Letting `rating_factor` scale the benefit.** A *Risikozuschlag* is a mortality loading, not a
    benefit uplift (mechanic 9). On model point 11 assert `benefit_pp(t)` is invariant to
    `rating_factor` while `prem_gross_pp` and `claims_death` both scale with it, and that the ratio
    `prem_paid_pp(1)/prem_gross_pp(1)` moves by less than one percentage point when `rating_factor`
    goes from 1.00 to 1.75 — the invariance that follows from loading both bases.
18. **Treating the *Über-Kreuz-Versicherung* as a different product.** It is a contracting structure
    with identical cover and identical cash flows; only the *Erbschaftsteuer* outcome changes [R15]
    [REG-R46]. Assert that no model-point column, no cells and no CSV in this product refers to it,
    and that the notes say why.

---

## Policyholder behaviour modelling

All dynamic formulas are **[std]** reference constructions; **there is no German calibration
evidence for any of them** (research gap 13).

- **Base lapse [std].** The duration table above, 6 % / 4 % / 3 %, with `w(n) = 0`. Its whole
  argument is structural: nothing is forfeited by lapsing, exit is frictionless in time as well as in
  money because the *Versicherungsperiode* follows the *Zahlweise* [R8], and the need amortises.
- **Premium-shock lapse [std] (optional module, off in the base run).** The product's distinctive
  behavioural risk is that the insurer can raise the bill without changing a guaranteed term, simply
  by cutting the declaration [R6]. The reference multiplier on `w(t)`:

      M_shock(t) = 1 + λ_s · max( 0, prem_paid_pp(t)/prem_paid_pp(t−1) − 1 )

  with `λ_s = 2.0` **[std]** and base run `λ_s = 0`, so `M_shock ≡ 1`. It is inert in the base run
  because `prem_paid_pp` is level there — it bites only when `decl_scale` is stressed, which is
  exactly when it should. **A model that raises the *Zahlbeitrag* toward the *Bruttobeitrag* in a
  stress and leaves the lapse assumption unchanged is understating the stress.**
- **Selective lapse [std] (optional module, off in the base run).** Healthy lives can re-underwrite
  into a cheaper contract; impaired lives cannot, so persisters' mortality drifts up:

      q₂_eff(t) = q₂(t) · [ 1 + λ · max(0, w_cum(t) − w_ref) ]

  with `w_ref = 0.25` and `λ = 0.30` **[std]**, base run `λ = 0`. **delib does not model selective
  lapse in the base run** — one basis for stayers and leavers — which is a known simplification and
  pitfall-adjacent rather than a pitfall: it is stated here so it is not discovered.
- **No dynamic surrender, no *Widerruf* decrement, no option take-up.** There is nothing to surrender
  [R2], so the whole of the exit machinery is lapse and a lapse pays nothing; the 30-day § 152
  *Widerrufsfrist* [R8] [REG-R23] sits inside the year-one lapse rate **[std]**; and
  *Nachversicherungsgarantie* and *Dynamik* take-up is **exogenous**, supplied as a schedule rather
  than modelled as a decision, because no event list, cap, window or age limit was established
  (research gap 7).

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `point_id = 1`,
`policy_id = RLV-000001`, `issue_age = 35`, `sex = M`, `smoker = N`,
`sum_assured = 300 000 €`, `policy_term = 25`, `prem_term = 25`,
`premium_form = laufend`, `prem_freq = jaehrlich` (`prem_freq_load = 1.000`,
`instalments = 1`), `benefit_schedule_id = konstant` (`benefit_factor = 1.0` at every `t`),
`nvg_schedule_id = keine` (`sum_uplift = 1.0` at every `t`),
`surplus_form = beitragsverrechnung`, `lives = 1`, `issue_age2 = 0`, `smoker2 = -`,
`rating_factor = 1.00`, `mort_table_id = dav2008t_proxy`, `duration_y = 0`,
`issue_date = 2026-01-01`. Hence `t0 = 1`, `proj_len() = 25`, cover to attained age 60, and the
table below is the **entire** projection.

**Assumptions, each tagged.** *Mortality*: the shipped [std] proxy
`mort_rate(M, N, x) = 0.00040 × 1.095^(x − 30)` at attained ages 35 to 59, so
`mort_rate(1) = 0.00040 × 1.095^5` and `mort_rate(25) = 0.00040 × 1.095^29` **[std]**;
`mort_be_factor = 1.00` **[std]**. *Tariff mortality*: the unisex 50/50 blend
`0.00030 × 1.095^(x − 30)` **[std]** loaded by `1 + m` with `sicherheitszuschlag_m = 1.25`
**[std]**, and `sex_mix_male = 0.50` **[std]** [R13] [REG-R34]. *Interest*:
`rechnungszins = 1,00 %` **[R10] [REG-R14] [REG-R15]**, used only in the premium equivalence and
the first-order reserve and **never** to discount a published cash flow. *Loadings*:
`zillmer_rate = 0.025` of the *Beitragssumme* at the *Höchstzillmersatz* ceiling **[R10] [REG-R16]**,
level **[std]**; `comm_rate_init = 0.020` of the *Beitragssumme* **[std]**;
`beta_tariff = 0.05` of each *Bruttobeitrag* **[std]**; `gamma_rate = 0.00030` of the
*Versicherungssumme* a year **[std]**. *Surplus*: `surplus_share = 0.90`, the MindZV minimum
allocation from the *Risikoergebnis* **[R9] [REG-R18]** with the choice of the minimum **[std]**;
`decl_scale = 1.00` **[std]**; `v_max = 0.95` **[std]**; so `v_d` is derived, not assumed.
*Modelled expenses*: `maint_prem_pct = 0.03` of each *Zahlbeitrag* **[std]**;
`comm_rate_renew = 0.010` of each *Zahlbeitrag* from `t = 2` **[std]**;
`expense_infl = 0.02` on the sum-related admin only **[std]**; `claim_expense = 250 €` per death
claim **[std]**. *Behaviour*: lapse 6 % in year 1, 4 % in years 2 and 3, 3 % from year 4, with
`lapse_rate(25) = 0` because the last policy year ends at expiry **[std]**;
`suicide_share = 0.03` applied to death claims in policy years 1 to 3 only **[std]** [R1]
[REG-R26]. *Modules*: premium-shock lapse `λ_s = 0` and selective lapse `λ = 0`, both **off**
**[std]**. No *Nachversicherungsgarantie*, no *Dynamik*, no rider, no premium tax [R16], no
discounting of any published cash flow.

`expenses` below is the total of acquisition, sum-related admin, collection and claim expense;
`commissions` is the initial *Abschlussprovision* plus the *Bestandspflegeprovision*. All amounts in
euros; `pols_if` to six decimals; cash flows to the cent. The **Total** row is summed at full
precision and then rounded, which can differ in the last cent from adding the displayed cells.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects **gross best-estimate-style liability cash flows, undiscounted**, on a declared
grid. The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** HGB § 341f requires it to be computed
  prospectively on the bases used to determine the premium, with a prudent margin, including a
  provision for future administration costs where the premium-paying period is shorter than the cover
  period — which is exactly model point 6's situation; the RechVersV governs presentation [R21]
  [REG-R54]. The DeckRV caps the *Rechnungszins* at the *Höchstrechnungszins* in force at conclusion
  (**1,00 %** from 1 January 2025) and the *Zillmersatz* at **25 ‰ of the *Beitragssumme***, the rate
  at conclusion applying for the whole term [R10] [REG-R14] [REG-R15] [REG-R16]. The model's
  `res_pp_at` is the **net, ungezillmert, first-order** reserve and is a **pricing diagnostic**: it is
  not floored, not *gezillmert* and not a statutory provision. The *Nullstellung* question — whether
  a negative individual reserve must be floored at zero — was **not established** (research gap 11),
  and because no reserve of any kind enters `result_cf()`, it does not reach these cash flows.
- **The *Zinszusatzreserve*.** DeckRV § 5 Abs. 3's *Referenzzins* and *Korridormethode* [REG-R17]
  reach this product only nominally: the reserve is small and short-lived, so a reader expecting the
  *Zinszusatzreserve* discussion that dominates `products/kapitallebensversicherung/` and
  `products/klassische_rentenversicherung/` will not find one here, and that is a product fact.
- **The *Überschuss* layer.** The MindZV's minimum allocation binds on the **HGB** accounts and is a
  transfer to the RfB, not a payout [R9] [REG-R18] [REG-R19]; § 139 VAG's *Bewertungsreserven*
  participation and its *Sicherungsbedarf* test are **economically empty** here, the attributable
  amount scaling with a *Deckungsrückstellung* that is nil or nominal [R11] [REG-R9] [unverified].
  The model's `prem_rebate` is the **contract-level** consequence of the allocation, not the
  allocation itself; a reader wanting the RfB mechanics should read
  `products/kapitallebensversicherung/technical-notes.md`.
- **Solvency II best estimate.** Probability-weighted future cash flows discounted at the relevant
  risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6], reaching German business
  **through the VAG** rather than directly. `BEL = Σ_t v(t) · liability_cf(t)` over the recursion
  above. **No cost-of-capital rate, contract-boundary rule or standard-formula shock in this library
  was read from a retrieved instrument**, so every such figure would be **[std]**, and none appears
  [R22]. Directive (EU) 2025/2 takes effect 30 January 2027 and nothing here implements a 2027 basis
  [REG-R3].
- **Contract boundary — and here the German product is easier than the French one.** The
  *Bruttobeitrag* is guaranteed for the whole term and the insurer's only unilateral lever is the
  declaration, which is not a repricing of a guaranteed term [R6] [REG-R27]. So there is none of the
  ambiguity `frlib`'s annually revisable *temporaire décès* faces, where the boundary may end at the
  next renewal. The model's posture is the same either way: project to expiry and publish the full
  stream; a boundary-truncated view is a truncation of `result_cf()`, never something baked into the
  projection.
- **IFRS 17.** Fulfilment cash flows plus a contractual service margin, applying to IFRS reporters
  from 1 January 2023 with no German carve-out [REG-R55]. The same expected-cash-flow engine feeds
  it; grouping, CSM and risk adjustment are out of scope. Professional standards sit with the DAV's
  *Fachgrundsätze* and its annual *Höchstrechnungszins* recommendation [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German term-life block.

1. **The *Sicherheitszuschlag* `m`, and the reason it is not the lever it looks like.** `m` sets the
   *Bruttobeitrag* almost by itself, and its level is **not public** — the DAV *Richtlinie* regulates
   the procedure, not the level [R12] (research gap 6). But because 90 % of the extra margin is
   returned as *Beitragsverrechnung*, moving `m` across its argued range of 1.0 to 1.5 moves the
   *Bruttobeitrag* by about **23 %** and the *Zahlbeitrag* by about **6 %** (product spec,
   contractual mechanics). **So the parameter with the widest uncertainty has the narrowest effect on
   the cash flow that matters**, which is the most useful single result in this product and the
   reason the *Zahlbeitrag* is derived rather than assumed.
2. **`decl_scale` — the declaration, and the product's largest policyholder risk.** Setting it to 0
   raises `premiums` to `prem_gross` at every `t`, with **no § 163 procedure, no *Treuhänder* and no
   policyholder remedy** [R6] [REG-R27]. On the anchor that is roughly a **75 % increase in the
   billed premium** with no change to any benefit. Nothing in the corpus bounds how far or how often
   a German carrier has actually moved a declaration on this product (research gap 1), and the
   premium-shock lapse module exists precisely because a stress that ignores the behavioural response
   understates itself.
3. **Mortality level and slope.** Both are **[std]** and unsourced. The level anchors on the research
   file's constructed unisex scale; the slope, 9,5 % per year of age, compounds — over model point
   14's 40 years it is worth a factor of about 36 between the first and last year's death rate, so a
   one-point error in the slope is worth far more than a one-point error in the level. The **DAV 2008
   T tables are the intended replacement and are not redistributable** [R12] [REG-R48]; a Destatis
   population table is **not** a substitute without a selection adjustment [REG-R52].
4. **The unisex mix `ω`.** It moves the tariff a great deal — female mortality at these ages is
   roughly half male [unverified] — and **no German carrier discloses its own mix**, which makes it
   one of the largest single sources of unexplained rate spread between carriers [R13] [REG-R34].
   Because the mix enters the tariff and not the projection, it is also the parameter that decides
   how large the cross-subsidy between model points 1 and 2 is.
5. **Lapse.** Nothing in the corpus supports any rate, and the whole-market *Stornoquote* is
   deliberately not used [R18] (gap 13). Cumulative lapse over the anchor's 25 years is large enough
   that the assumption governs how much of the profitable later term is ever reached — and note the
   direction: on a level-premium product the **early** years are the strained ones, so early lapse
   hurts, which inverts the intuition a reader arriving from the French annually-revisable product
   brings with him.
6. **Acquisition cost at the Zillmer ceiling.** The composite assumes a term tariff runs at 25 ‰ of
   the *Beitragssumme*, and a slim direct-channel cost would sit far below it [S3] [S12]. It is the
   single largest year-one cash flow after the premium, it is entirely **[std]**, and it decides
   whether small model points such as point 13 (50 000 €, five years) are viable at all.
7. **The suicide share, and the § 161 window's length.** Worth little in the totals and much in
   correctness: the German window is **three years** against France's one [R1] [`frlib` R1], so the
   parameter carries three times the weight, and an implementation that applies the switch to every
   year, or to a lapse, or that omits the restart on a *Nachversicherungsgarantie* increment, is
   wrong in a way the totals will not reveal.
8. **What the model deliberately cannot represent.** The *Kriegsklausel* is a catastrophe-scenario
   clause and is documented, not modelled; the § 161 mental-illness exception is the ground on which
   German suicide claims are actually litigated [R23] and cannot be a best-estimate switch; selective
   lapse is real and is off by default; and the *Kostenüberschuss* emerges in `net_cf` and is not
   returned, because the MindZV's *übriges Ergebnis* limb carries a different minimum share and the
   research file gives no basis on which to split a German term tariff's expense result [R9]
   [REG-R18]. Each is a stated choice, and each is stated here rather than left to be discovered from
   a number that looks wrong.
