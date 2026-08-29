# Technical Notes

**Status:** Draft, 2026-08-29 (all cited sources accessed 2026-08-29).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`RV_DE_A`**, **annual** grid — for the standardized composite German *klassische aufgeschobene
private Rentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's contract. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried from
`_research/klassische_rentenversicherung.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own frozen numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified] marks
claims no search result corroborated. Parameter values are identical to those in `product-spec.md`.
Cells names, model-point columns and CSV headers are English `lower_snake_case`; German terms of art
keep their German form in prose.

**Retrieval conditions.** No document cited here was retrieved — direct HTTP egress from the build
environment is blocked and everything rests on `WebSearch` result summaries, whose budget was
exhausted after eighteen queries on this product. The consequence for these notes is specific and
large: **the corpus establishes this product's mechanics thoroughly and its levels barely at all.**
No *Rentenfaktor*, no declared surplus rate, no charge parameter and no behavioural rate was
established at any German carrier for any year, so **every number in assumption classes (b) and (c)
below, and most of class (a)'s levels, is [std]**. What the citations do establish is the shape of
each recursion, and that is what this file is for.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — premiums in;
  death benefits, surrender values, the *Kapitalabfindung*, annuity instalments and insurer expenses
  out — for a single-policy model point on an expected (probability-weighted) basis, together with
  the two account balances that make the product what it is: the *Deckungskapital* and the
  *Ansammlungsguthaben*.
- **Out of scope, and said so rather than left to be discovered.** Discounting; the statutory
  *Deckungsrückstellung* [REG-R54]; the *Zinszusatzreserve* [REG-R17]; the RfB and the MindZV
  arithmetic [REG-R18] [REG-R19]; the *Sicherungsbedarf* test [REG-R20]; the Solvency II best
  estimate, risk margin, SCR and MCR [REG-R6]; IFRS 17 [REG-R55]; and **all taxation** — every cash
  flow is gross of *Kapitalertragsteuer*, *Solidaritätszuschlag* and *Kirchensteuer* [REG-R38]. Also
  not modeled, each for a stated reason: the *Bonusrente* surplus system [R24]; *Zuzahlung*, which no
  source names (gap 15); the survivor's-annuity and BU riders [S10] [S4]; § 163 VVG adjustment of the
  guaranteed *Rentenfaktor* [R3] [R17] [REG-R27]; and § 169 Abs. 6 [R1].
- **Projection frequency.** **Annual grid.** The contract's own natural period is the *Versicherungs-
  jahr*: the *Rechnungszins* is credited annually, the *Überschussbeteiligung* is declared annually
  and the *Ansammlungsguthaben*'s interest is "credited at the end of each insurance year and upon
  termination of the insurance" [R24], the § 165 paid-up value is "stated in the contract for each
  insurance year" [R2], and *Kündigung* and *Beitragsfreistellung* both take effect "for the end of
  the current insurance period" [R1] [R2]. The one sub-annual mechanic is the **monthly annuity**
  [S13] [R24], compressed onto the annual grid as described below and listed as a pitfall.
- **What `t` counts.** `t` is the **policy year**, counted from inception: policy year `t` runs from
  the anniversary at attained age `issue_age + t − 1` to the next. The frame is **1-based**: a
  new-business model point opens at `t = 1`. An **in-force** model point that has already run
  `duration_init` complete policy years opens at `t = duration_init + 1`, carrying its opening
  balances on the model point, so the calendar year of every row is `issue_year + t − 1` for every
  point in the table — which is what lets one generational mortality surface and one declared-rate
  path serve a book of mixed vintages [REG-R14] [REG-R49].
- **`proj_len()`** is the **last projected policy year index**, per this library's ruling
  (`tests/test_model_conventions_de.py`), so `result_cf().index[-1] == proj_len()`:

      proj_len() = omega_age − issue_age

  with `omega_age = 121` **[std]** the terminal age of the shipped mortality proxy, at which
  `mort_rate = 1`. The projection therefore ends when the annuitant cannot survive further, not at a
  fixed horizon: a life annuity has no term, and truncating one at, say, 40 years silently drops the
  tail the *Rentenfaktor* was priced for. For the anchor cell, `proj_len() = 121 − 50 = 71`.
- **The *Rentenbeginn* is the end of policy year `n = aufschub_y`**, which is the same instant as the
  start of policy year `n + 1`. Accumulation-phase rows are `t ≤ n`; payout-phase rows are `t > n`.
  The *Kapitalabfindung* is paid in row `n`; the first annuity instalment falls in row `n + 1`.
- **Timing conventions [std].** Premiums at the **start** of the policy year; charges deducted
  immediately after; the *Rechnungszins* credited on the post-premium, post-charge balance at the
  **end** of the year; the declared surplus credited to the *Ansammlungsguthaben* at the end of the
  year; death and surrender at the **end** of the year, deaths before surrenders; the *Rentenbeginn*
  events after both; and annuity instalments at the **start** of the payout year (monthly in advance,
  compressed). **The ordering of premium credit, charge deduction and interest accrual is not
  established by any source in this corpus** [S11] and is the single most consequential [std] in this
  file (processing order, and pitfall 2).
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  benefits and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents, `pols_if` to six decimals **[std]**.
- **Unisex pricing is a hard constraint, not a convention.** A model point carries `sex` for the
  **decrement** — the underlying DAV tables are sex-specific raw material [REG-R47] [REG-R49] — and
  `sex` must not enter the premium, the charge scale or the *Rentenfaktor*, sex-based differences
  being prohibited for contracts concluded from 21 December 2012 [REG-R34].

---

## Model point attributes

Thirty columns. `model_point_table.csv` is indexed by `point_id` and is the one input file exempt
from the `provenance` rule, because a model point is a *configuration* rather than an assumption.
The right-hand column names the points that exercise each attribute away from its base value.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Key; `Projection` is parameterized by it | all |
| `policy_id` | str | Label, `DE-RV-nnnn` | all |
| `sex` | enum {M, F} | Decrement only; **never** priced [REG-R34] | 2, 4, 7, 9, 11, 13 are F |
| `issue_age` | int | Age last birthday at inception | all |
| `issue_year` | int | Calendar year of inception; drives the generational mortality index and fixes the guarantee vintage [REG-R14] [REG-R49] | 6 (2005), 14 (2017) |
| `duration_init` | int | Complete policy years already elapsed; 0 = new business. The frame opens at `t = duration_init + 1` | 6 (20), 14 (8) |
| `pols_if_init` | float | Policies represented; `pols_if(t0)` | all (1.0) |
| `premium_form` | enum {laufend, einmal} | Recurring or single premium [S11] [REG-R53] | 2 (`einmal`) |
| `prem_gross_pp` | EUR p.a. | Annual *Bruttobeitrag* before the frequency loading | all but 2 |
| `premium_single_pp` | EUR | *Einmalbeitrag* | 2 |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | *Zahlweise*; keys `freq_load_table.csv` | 3 (monthly), 4 (quarterly), 5 (half-yearly) |
| `prem_term_y` | int | Premium-paying years from inception | 4 (20 of 22), 5 (25 of 27) |
| `aufschub_y` | int | Deferment in years; *Rentenbeginn* at the end of policy year `aufschub_y` | all |
| `int_rate_guar` | rate | The contract's *Rechnungszins* — **a model-point attribute, not a global assumption** [R7] [REG-R14] [REG-R15] | 6 (2,75 %), 14 (0,90 %) |
| `charge_id` | str | Key into `charge_table.csv`; `zillmer_25` or the pre-2015 `zillmer_40` [REG-R16] | 6 (`zillmer_40`) |
| `annuity_rate_guar` | EUR/month per 10 000 € | *garantierter Rentenfaktor*, fixed at inception [S8] [R24] | all (levels **[std]**) |
| `rf_scenario_id` | str | Key into `rentenfaktor_table.csv` for the *aktueller Rentenfaktor* | 5 (`high`), 13 (`low`) |
| `decl_scenario_id` | str | Key into `decl_rate_table.csv` for the declared *laufende Verzinsung* | 14 (`low`) |
| `guar_capital_pp` | EUR | Minimum guaranteed contract value at *Rentenbeginn* [S9]; 0 = not stated | 13 (60 000) |
| `death_benefit_form` | enum {prem_refund, deckungskapital, max} | The three documented designs [S1] [R24]; `max` **[std]** [S19] | 2, 12 (`deckungskapital`); 5, 13 (`max`) |
| `db_incl_surplus` | int 0/1 | Whether the *Ansammlungsguthaben* is added to the death benefit [R24] | 4, 12 |
| `rgz_years` | int | *Rentengarantiezeit* in years [R24] [S9] [S13] | 9 (0), 11 (5), 3/14 (15), 5/10 (20) |
| `kapitalwahl_rate` | float | Fraction electing the *Kapitalwahlrecht* at *Rentenbeginn* [S12] [R6] [R21] | 9 (1.00), 2/10 (0.00), 5 (0.20) |
| `pup_year` | int | Policy year of *Beitragsfreistellung*; 0 = never [R2] | 7 (10), 8 (3, trips the minimum) |
| `dynamik_rate` | rate | *Dynamik* annual premium increase [S4]; 0 = option off | 12 (5 %) |
| `payout_system` | enum {konstant, teildynamisch, volldynamisch} | *Überschussverwendung* in payment [R19] [R20] [R24] | 4, 11 (`teildynamisch`); 5, 10 (`volldynamisch`) |
| `av_pp_init` | EUR | Opening *Deckungskapital* | 6, 14 |
| `av_sur_pp_init` | EUR | Opening *Ansammlungsguthaben* | 6, 14 |
| `prem_cum_pp_init` | EUR | Premiums paid before the valuation date — the *Beitragsrückgewähr* base | 6, 14 |
| `alpha_amort_pp_init` | EUR | Acquisition charge already amortised before the valuation date | 6 (2 592), 14 (900) |

**The fourteen model points.** Point 1 is the worked example's anchor cell. Between them the points
carry both premium forms, all four payment frequencies, two in-force cells on two legacy guarantee
vintages, both charge sets, all three death-benefit forms with and without surplus, all three payout
systems, five *Rentengarantiezeit* durations including zero, *Kapitalwahlrecht* take-ups of 0 %,
20 %, 30 % and 100 %, the *Dynamik*, both *Beitragsfreistellung* branches, and four boundary cases:
the paid-up conversion that fails the *Mindestversicherungsleistung* and is cashed out (8), full
commutation at *Rentenbeginn* (9), the guaranteed *Rentenfaktor* binding over a lower current one
together with a binding `guar_capital_pp` (13), and a *Rentengarantiezeit* of zero (9).

**One constraint the table must satisfy and the model asserts.** `av_spread_pp` (below) is seeded
equal to `av_pp_init` on an in-force point, which is exact only once the acquisition charge is
amortised under both treatments, so every in-force point has `duration_init ≥ alpha_spread_years = 5`
**[std]**. Points 6 and 14 open at durations 20 and 8.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | `omega_age − issue_age`, the last projected policy year | once per model point |
| `age(t)` | Attained age at the start of policy year `t` = `issue_age + t − 1` | annual |
| `calendar_year(t)` | `issue_year + t − 1`; the second index of the generational mortality surface | annual |
| `pols_if(t)` | Policies in force at the **start** of policy year `t`; `pols_if(t0) = pols_if_init()` | annual recursion |
| `pols_annuity(t)` | The count the annuity instalment is **paid on** — the annuitised count inside the *Rentengarantiezeit*, survivors after it, zero before *Rentenbeginn* | annual |
| `av_pp(t)` | *Deckungskapital* per policy at the start of year `t` | annual recursion |
| `av_pp_at(t, timing)` | `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_INT"` | within year `t` |
| `av_sur_pp(t)`, `av_sur_pp_at(t, timing)` | *Ansammlungsguthaben* per policy, and its within-year points | annual recursion |
| `av_spread_pp(t)`, `av_spread_pp_at(t, timing)` | The parallel *Deckungskapital* in which the acquisition charge is spread evenly over the first five contract years — the § 169 Abs. 3 VVG floor [REG-R28] | annual recursion |
| `spread_diff_pp(t)` | `av_spread_pp(t) − av_pp(t)`; the only quantity by which the two accounts differ | annual recursion |
| `capital_conv_pp` | Conversion capital struck at *Rentenbeginn* | once |
| `annuity_rate_appl` | `max(annuity_rate_guar, annuity_rate_curr)` [S4] | once |
| `annuity_guar_mth_pp` | *garantierte Rente*, monthly, struck at *Rentenbeginn* | once |
| `annuity_sur_mth_pp(t)` | *Überschussrente*, monthly, by payout system | annual |
| `mort_rate_guar(t)`, `mort_rate(t)` | First-order (tariff) and second-order (best-estimate) annual mortality | lookup |
| `lapse_rate(t)` | Annual surrender rate; **0** from *Rentenbeginn* | lookup |

There is **no** paid-up sub-population state: *Beitragsfreistellung* is a deterministic election at a
stated policy year rather than a continuous decrement, for the reason given under *Policyholder
behaviour modelling*. There is **no** *Bonusrente* ledger in the accumulation phase, and **no**
survivor's-annuity state.

---

## Assumption inputs

**The eight input files.** All inputs are **external CSVs beside `run.py`**, read once per model by
the unparameterized `Data` Space (the `annuallife/TradLife_A` layout). Every file but the model point
table carries a per-row `provenance` column, this library's second ruling.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the thirty model-point attributes above (**provenance-exempt**) |
| `mort_table.csv` | `sex`, `age` | `q_base`, `improve`, `provenance` |
| `decl_rate_table.csv` | `scenario_id`, `calendar_year` | `decl_rate`, `provenance` |
| `rentenfaktor_table.csv` | `rf_scenario_id`, `age` | `annuity_rate_curr`, `provenance` |
| `charge_table.csv` | `charge_id`, `item` | `value`, `provenance` |
| `lapse_table.csv` | `duration` | `lapse_rate`, `provenance` |
| `freq_load_table.csv` | `prem_freq` | `freq_load`, `n_instalments`, `provenance` |
| `param_table.csv` | `item` | `value`, `provenance` |

`param_table.csv` holds every scalar [std] assumption that is neither a charge nor a rate table:
`expense_acq_pp`, `expense_maint_pp`, `expense_annuity_pp`, `expense_claim_pp`, `expense_infl`,
`mort_be_factor`, `mort_base_year`, `omega_age`, `val_reserve_rate`, `sur_ann_rate`,
`sur_ann_growth`, `sur_ann_theta` and `roll_fwd_tol`. Keeping them in a file rather than in
`Projection` References is what gives each of them its own provenance tag.

### (a) Contractual and guaranteed elements (cited)

| Input | Value / rule | Basis |
|---|---|---|
| *Deckungskapital* recursion | The *Sparbeitrag* — the premium net of the portions "intended for risk and cost coverage" — accumulated at the *Rechnungszins* | [S11]; ordering **[std]** |
| *Rechnungszins* | A model-point attribute; 1,00 % for 2026 issues, 2,75 % and 0,90 % on the two legacy points | [R7] [R11] [REG-R14] [REG-R15] |
| *Höchstzillmersatz* | **25 ‰** of the *Beitragssumme* from 1 January 2015, **40 ‰** before, the rate at conclusion applying for the whole term | [REG-R16] [REG-R20] |
| § 169 Abs. 3 surrender floor | At least the *Deckungskapital* that results from spreading the charged acquisition and distribution costs **evenly over the first five contract years** | [REG-R28]; article level [unverified] here (gap 12) |
| § 169 Abs. 5 *Stornoabzug* | Permitted only if **agreed, quantified and appropriate**; a deduction for unamortised acquisition costs is void | [R1] [REG-R28] |
| § 165 paid-up value | Computed on the premium calculation basis, **on the basis of the § 169 Abs. 3–5 surrender value**, and tabulated per insurance year | [R2] [REG-R28] |
| § 165 minimum benefit | Below the *Mindestversicherungsleistung* the contract is **cashed out at the surrender value including profit shares**, not made paid-up | [R2] |
| Death benefit before *Rentenbeginn* | *Beitragsrückgewähr* (premiums paid), the accumulated *Deckungskapital*, or the larger of the two; optionally plus the attributable surplus | [S1] [R24]; `max` **[std]** [S19] |
| Conversion capital | Includes *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value | [S9] |
| Conversion rule | `monthly annuity = capital / 10 000 × Rentenfaktor` | [R24] |
| *Rentenfaktor* applied | `max(garantierter, aktueller)`, guaranteed for the annuity payment period | [S4]; [R24] |
| *Bewertungsreserven* | *hälftige* participation under § 153 Abs. 3 VVG, **crystallised at the transition to annuity payment** and continuing in payment | [S4] [R4] [REG-R24] |
| Annuity | Monthly, for life, from *Rentenbeginn*; *garantierte Rente* plus *Überschussrente*, only the first guaranteed | [S13] [R20] [R24] |
| *Rentengarantiezeit* | Payment continues to survivors until the agreed years expire | [R17] [R24] |
| Surrender in payment | None | [REG-R28]; reading **[std]** |
| Mortality basis | **DAV 2004 R**, a *Generationentafel*, first order carrying safety margins over second order | [S8] [R12] [R13] [REG-R47] [REG-R49] |
| Unisex tariff | Sex may not enter premium or benefit for contracts from 21 December 2012 | [REG-R34] |

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

Everything in this class is a **declaration**, not a promise: an insurer's own AVB says the amount of
profit sharing depends on "many influences which are unpredictable and only limitedly controllable by
the company, with the most important influencing factor being capital-market developments" [S8].
**No rate in this class was established for this product at any carrier for any year** (gap 4). The
declaration instrument exists and its 2026 vintage is evidenced [S15]; nothing inside it is.

| Input | Value | Basis |
|---|---|---|
| Declared *laufende Verzinsung* `decl_rate` | **2,55 % p.a.** level on the `base` path; **1,50 %** on the `low` path | **[std]** (i) |
| Surplus rate `bonus_rate(t)` | `max(0, decl_rate(t) − int_rate_guar)` — **1,55 %** on the 1,00 % vintage, **0 %** on the 2,75 % vintage | mechanic [R24] [REG-R53]; **[std]** level |
| Interest credited on the *Ansammlungsguthaben* | at `decl_rate(t)`, the full declared rate | mechanic [R24]; **[std]** (ii) |
| *Bewertungsreserven* rate at *Rentenbeginn* `val_reserve_rate` | **1,5 %** of the accumulated value | mechanic [S4] [R4]; level **[std]** (iii) |
| *aktueller Rentenfaktor* at *Rentenbeginn* | **32,00 €** per month per 10 000 € at age 67 on the `base` path; **25,50 €** `low`; **35,00 €** `high` | mechanic [S13] [R24]; level **[std]** (iv) |
| *Überschussrente* rate `sur_ann_rate` (`konstant`) | **12 %** of the *garantierte Rente*, level | mechanic [R20]; level **[std]** (v) |
| *Überschussrente* growth `sur_ann_growth` (`volldynamisch`) | **1,5 % p.a.** compound on the *garantierte Rente* | mechanic [R20] [R24]; level **[std]** (v) |
| `teildynamisch` split `sur_ann_theta` | **0,5** — half the constant increment plus half the growth rate | mechanic [R20] [R24]; **[std]** (v) |

(i) Anchored on the only public figures the library has: the average *laufende Verzinsung* for 2025
was **2,53 % Klassik / 2,58 % Neue Klassik**, and for 2026 the sources give 2,6–2,7 %, 2,87 % and
2,54 % — three incompatible averages [REG-R53]. 2,55 % sits inside the 2025 pair and is a market
average, not a carrier's declaration. **The declared rate is the *Garantieverzinsung* plus the
*laufende Zinsüberschussbeteiligung*, never a surplus on top of the guarantee** [REG-R53]; that is
what the `max(0, ·)` in `bonus_rate` implements, and it is why the 2,75 % legacy point receives no
interest surplus at all — a real and important German result, not a modelling artefact.
(ii) [R24] establishes that the *Ansammlungsguthaben* "accrues with interest, with the interest
credited at the end of each insurance year and upon termination of the insurance" and says nothing
about the rate. Crediting the full declared rate rather than the *Rechnungszins* is [std]; the
alternative is a documented variant and moves the anchor cell's final *Ansammlungsguthaben*
materially.
(iii) The mechanic is cited twice over — participation is *hälftig* and the *Rentenbeginn* is "a key
point" for it [S4] [R4] — and **no amount, ratio or reserve level was established** anywhere.
1,5 % of the accumulated value is a placeholder sized to be visible without dominating.
(iv) See product spec footnote 9. Chosen so that the anchor cell's `max()` resolves **upward** (the
current factor wins) and point 13's resolves **downward** (the guarantee binds), because a rule with
one branch never exercised is a rule no test covers.
(v) The three systems are established and their *directions* are established — the constant form is
set from a whole-period projection and **falls if the insurer earns less**, the fully dynamic form
adjusts annually to actual surplus development, and the partial form is a stated combination of the
two [R20] [R24]. No level, rate or split was established for any of them.

### (c) Behavioural and experience assumptions (the modeller's view)

**Every input in this class is [std] and none has any evidence behind it** (gap 20): no German lapse
rate, no *Beitragsfreistellung* rate, no *Kapitalwahlrecht* take-up rate and no market *Stornoquote*
was returned by any search for this product.

**Mortality.** The first-order basis is **DAV 2004 R**, a *Generationentafel* which is the property
of the Deutsche Aktuarvereinigung, is not public and is **not shipped** [S8] [R12] [R13] [REG-R49].
`mort_table.csv` is a **[std] proxy** with the structure the real table has and none of its values:
a sex-distinct base table `q_base(sex, x)` for base year **2005** — the year DAV 2004 R was intended
for new business [R13] — and an age-dependent annual improvement rate `improve(x)`, combined as

    mort_rate_guar(t) = q_base(sex, x(t)) × (1 − improve(x(t)))^( calendar_year(t) − 2005 )

which is the generational form the reference library requires of any annuity proxy, built the way it
recommends: a base table times a cumulative improvement factor, anchored to Destatis's own
*Generationensterbetafeln* as the free redistributable analogue [REG-R49] [REG-R52]. The proxy is
anchored so that **`q_base(M, 50) = 0.002000` exactly**, and that anchor is stated in the model's
`Data` docstring; a substitute table must preserve it if the worked example is still to close.
`improve(x)` is **1,5 % p.a. below age 60, grading linearly to 0,5 % at age 100 and to zero at 110**
**[std]** — a deliberate simplification of the *Starttrend* / *Zieltrend* structure the German
construction actually uses, and documented as one rather than presented as a replication [REG-R49].

The second-order (best-estimate) basis is the first-order one loaded:

    mort_rate(t) = mort_rate_guar(t) × mort_be_factor,    mort_be_factor = 1.15  [std]

**The factor is above one and that is the whole point.** For an annuity, prudence means assuming
mortality **lower** than expected, so the first-order table sits below best estimate, and the safety
margin runs in **two dimensions** — level and trend [REG-R47] [REG-R49]. The same table is used for
the accumulation-phase death benefit, which is the German peculiarity worth naming: an annuity table
prices a death benefit, so that benefit is systematically **under**-charged relative to a
death-business basis such as DAV 2008 T [REG-R48], and the *Beitragsrückgewähr* design exists partly
because it makes the mismatch immaterial — the benefit is the premiums, not a sum insured.

**Lapse (*Storno*).** `lapse_table.csv`, by policy duration, and **zero from *Rentenbeginn***:

| Duration | 1 | 2 | 3 | 4–7 | 8–11 | **12** | 13+ | payout |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 6,0 % | 5,0 % | 4,5 % | 4,0 % | 3,5 % | **6,0 %** | 3,0 % | 0 % |

The **duration-12 step is the only shaped feature and it is the one with a reason**: § 20 Abs. 1
Nr. 6 EStG makes half the gain taxable only where the contract has run **at least twelve years** and
payment falls after completion of the **62nd year of life**, so German Schicht-3 surrenders are
suppressed approaching duration 12 and spike at it [R6] [REG-R45]. That is the German analogue of the
eight-year threshold that drives French *assurance vie* behaviour, and delib models it the same way
frlib does — as a duration-dependent shape with the threshold named and the level [std]. The level of
every cell is unsourced.

**Election rates.** `kapitalwahl_rate` is a **model-point attribute**, base **30 %** [std]. It is not
a behavioural formula, and the notes say why: the annuitise-or-commute decision is a **tax
comparison** — 18 % of each instalment at the marginal rate against half the *Unterschiedsbetrag*
taxed once [R5] [R6] [REG-R41] [REG-R45] — and this model computes no tax, so the rate stands in for
a calculation it does not perform. `pup_year` is likewise a deterministic election rather than a
rate.

**Expenses (all levels [std]; no German carrier publishes any of them, gap 14).**

| Input | Value | Note |
|---|---|---|
| Acquisition `expense_acq_pp` | **400,00 €** per policy at issue, new business only | **[std]** |
| Maintenance, accumulation `expense_maint_pp` | **45,00 €** per policy p.a., inflating | **[std]** |
| Administration, payout `expense_annuity_pp` | **30,00 €** per policy p.a., inflating | **[std]** |
| Settlement `expense_claim_pp` | **120,00 €** per death, surrender or commutation event | **[std]** |
| Inflation `expense_infl` | **2,0 % p.a.** | **[std]** |

**Charges — and the distinction from expenses is load-bearing.** A *charge* is a deduction the tariff
makes from the premium or the *Deckungskapital*; it moves money **inside** the contract and produces
**no cash flow**. An *expense* is the insurer's actual outgo and is a cash flow. Confusing them is
pitfall 6. `charge_table.csv` is keyed by `(charge_id, item)` so each number carries its own
`provenance` tag:

| Item | `zillmer_25` | `zillmer_40` | Basis |
|---|---|---|---|
| `alpha_rate` | 0,025 of the *Beitragssumme* | 0,040 | cap [REG-R16]; use of the cap **[std]** |
| `alpha_spread_years` | 5 | 5 | § 169 Abs. 3 [REG-R28] |
| `beta_rate` | 0,040 of each gross premium | 0,040 | **[std]** |
| `gamma_rate` | 0,0020 p.a. of the *Deckungskapital* | 0,0020 | **[std]** |
| `gamma_pup_rate` | 0,0030 p.a. while premium-free | 0,0030 | **[std]** |
| `stornoabzug_rate` | 0,020 of the pre-deduction value | 0,000 | conditions [R1] [REG-R28]; level **[std]** |
| `min_annuity_mth` | 30,00 € a month | 30,00 € | § 165 threshold [R2]; level **[std]** |
| `annuity_admin_rate` | 0,015 of each instalment | 0,015 | **[std]**; **recorded, not applied** — see pitfall 12 |

`freq_load_table.csv` carries the *Ratenzahlungszuschlag* **[std]** (gap 14): annual 1,000 (1
instalment), half-yearly 1,020 (2), quarterly 1,030 (4), monthly 1,050 (12).

---

## Cash flow components and recursions

### Notation, defined once and used throughout

| Symbol | Cells | Meaning |
|---|---|---|
| `t`, `t0`, `N` | — | policy year; `t0 = duration_init + 1`; `N = proj_len()` |
| `x(t)`, `τ(t)` | `age`, `calendar_year` | attained age `issue_age + t − 1`; calendar year `issue_year + t − 1` |
| `n`, `m`, `κ` | `aufschub_y`, `rgz_years`, `kapitalwahl_rate` | deferment years; guarantee period; commutation take-up |
| `l(t)` | `pols_if` | policies in force at the start of year `t`; `l(t0) = pols_if_init()` |
| `a(t)` | `pols_annuity` | the count the annuity instalment is paid on |
| `V(t)` | `av_pp` | *Deckungskapital* per policy at the start of year `t` |
| `A(t)` | `av_sur_pp` | *Ansammlungsguthaben* per policy at the start of year `t` |
| `Ṽ(t)`, `Δ(t)` | `av_spread_pp`, `spread_diff_pp` | the five-year-spread parallel account, and `Ṽ(t) − V(t)` |
| `P(t)` | `prem_pp` | gross premium per policy for year `t`, after the frequency loading |
| `α(t)`, `α̃(t)` | `charge_acq_pp`, `charge_acq_spread_pp` | zillmered and evenly-spread acquisition charge |
| `β(t)`, `γ(t)`, `ρ(t)` | `charge_prem_pp`, `charge_admin_pp`, `charge_risk_pp` | premium, reserve-based and risk charges |
| `S(t)` | `prem_to_av_pp` | *Sparbeitrag* — the premium net of what the charges take from it |
| `C(t)` | `charge_from_av_pp` | the part of the charges the premium could not meet, taken from `V` |
| `i`, `d(t)`, `b(t)` | `int_rate_guar`, `decl_rate`, `bonus_rate` | *Rechnungszins*; declared rate; `max(0, d(t) − i)` |
| `D(t)`, `Ď(t)` | `db_pp`, `db_base_pp` | death benefit paid in year `t`; its start-of-year measure, used only for `ρ` |
| `R(t)`, `R̄(t)`, `R̲(t)` | `cv_pp`, `cv_tariff_pp`, `cv_floor_pp` | surrender value; the tariff value net of the *Stornoabzug*; the § 169 Abs. 3 floor |
| `q*(t)`, `q(t)`, `w(t)` | `mort_rate_guar`, `mort_rate`, `lapse_rate` | first-order and best-estimate mortality; surrender rate |
| `K`, `f_g`, `f_c`, `f` | `capital_conv_pp`, `annuity_rate_guar`, `annuity_rate_curr`, `annuity_rate_appl` | conversion capital; the two *Rentenfaktoren* and the applied one |
| `G`, `U(t)` | `annuity_guar_mth_pp`, `annuity_sur_mth_pp` | *garantierte Rente* and *Überschussrente*, monthly |

Rates are per annum and dimensionless; `V`, `A`, `P`, `D`, `R`, `K` are EUR per policy; every cash
flow in `result_cf()` is EUR for the model point as a whole.

### The premium and the *Beitragssumme*

    P(t) = 0                                                   if t > n, or t > prem_term_y,
                                                               or (pup_year > 0 and t ≥ pup_year)
         = premium_single_pp                                   if premium_form = einmal and t = 1
         = prem_gross_pp × freq_load × (1 + dynamik_rate)^(t−1) if premium_form = laufend

    beitragssumme_pp = Σ_{u=1..min(prem_term_y, n)} P_sched(u)
    alpha_total_pp   = alpha_rate × beitragssumme_pp

`P_sched` is the premium schedule **as written at inception**, ignoring any later
*Beitragsfreistellung*: § 4 DeckRV takes the *Zillmersatz* on the sum of all premiums payable under
the contract [REG-R16], and a later election does not retrospectively shrink that base. The
frequency loading is inside `P`, so it is inside the *Beitragssumme* too.

### The premium decomposition

    α(t)  = min( P(t), max(0, alpha_total_pp − alpha_cum_pp(t)) )        zillmered
    α̃(t)  = alpha_total_pp / alpha_spread_years   for t ≤ 5, else 0      § 169 Abs. 3 [REG-R28]
    β(t)  = beta_rate × P(t)
    γ(t)  = (paid_up(t) ? gamma_pup_rate : gamma_rate) × V(t)
    Ď(t)  = prem_cum_pp(t) + P(t)                     if death_benefit_form = prem_refund
          = V(t)                                      if death_benefit_form = deckungskapital
          = max(of the two)                           if death_benefit_form = max
    ρ(t)  = q*(t) × max(0, Ď(t) − V(t))               for t ≤ n, else 0
    charge_due_pp(t)      = α(t) + β(t) + γ(t) + ρ(t)
    charge_from_prem_pp(t)= min( P(t), charge_due_pp(t) )
    C(t)                  = charge_due_pp(t) − charge_from_prem_pp(t)
    S(t)                  = P(t) − charge_from_prem_pp(t)

Two conventions are doing work here and both are [std]. First, **the risk charge is struck on
start-of-year quantities**, `Ď(t)` and `V(t)`, rather than on the post-premium balance — otherwise
`ρ` depends on `V` after `ρ`, and the recursion is circular. Second, **charges are met from the
premium where there is one and from the *Deckungskapital* where there is not**: [S11] describes
premium-based deductions, but a premium-free contract still bears administration and mortality cost,
and `C(t)` is what makes *Beitragsfreistellung* cost something instead of being free. Note that for
`death_benefit_form = deckungskapital` the net amount at risk is identically zero, so `ρ ≡ 0` — which
is correct, and is a good invariance test.

### The *Deckungskapital* and the *Ansammlungsguthaben*

    av_pp_at(t,"BEF_PREM") = V(t)
    av_pp_at(t,"AFT_PREM") = V(t) + S(t) − C(t)
    int_credited_pp(t)     = i × av_pp_at(t,"AFT_PREM")
    av_pp_at(t,"AFT_INT")  = av_pp_at(t,"AFT_PREM") + int_credited_pp(t)

    bonus_credited_pp(t)      = b(t) × av_pp_at(t,"AFT_PREM") + d(t) × A(t)
    av_sur_pp_at(t,"AFT_INT") = A(t) + bonus_credited_pp(t)

The *Ansammlungsguthaben* is a **second, parallel account** with its own credited rate, settling at
year end and at exit [R24]. Its interest-surplus credit is `b(t) = max(0, d(t) − i)` applied to the
same base the guarantee is applied to, so the two together deliver the declared *laufende Verzinsung*
`d(t)` and never more — the arithmetic the reference library names as the commonest error in
describing a German contract [REG-R53].

### The § 169 Abs. 3 floor, as a difference recursion

The two accounts differ **only** in the acquisition charge, so the model carries the difference
rather than a second full recursion:

    Δ(t0) = 0
    spread_diff_pp_at(t,"AFT_INT") = ( Δ(t) + α(t) − α̃(t) ) × (1 + i)
    Δ(t+1) = spread_diff_pp_at(t,"AFT_INT")
    av_spread_pp_at(t,"AFT_INT") = av_pp_at(t,"AFT_INT") + spread_diff_pp_at(t,"AFT_INT")

with `γ` and `ρ` deliberately taken at the same euro amount in both accounts **[std]**, which is what
makes the difference exact. Two consequences are worth stating because they are not obvious. The
difference is **large in the first five years** — on the anchor cell the whole 25 ‰ is taken in year 1
against one fifth of it — and it **never returns to zero**, because the spread account earns the
*Rechnungszins* on the amounts not yet deducted. So on a zillmered tariff with a positive
*Rechnungszins* the § 169 Abs. 3 floor is above the tariff *Deckungskapital* at **every** duration,
not only in the first five years.

### Surrender, and the *Beitragsfreistellung* election

    surr_charge_pp(t) = stornoabzug_rate × ( av_pp_at(t,"AFT_INT") + av_sur_pp_at(t,"AFT_INT") )
    R̄(t) = av_pp_at(t,"AFT_INT") + av_sur_pp_at(t,"AFT_INT") − surr_charge_pp(t)
    R̲(t) = av_spread_pp_at(t,"AFT_INT")
    R(t) = max( R̄(t), R̲(t) )

The floor is the § 169 Abs. 3 *Deckungskapital* alone, because Abs. 3 speaks of the
*Deckungskapital*; profit shares sit **on top of** the statutory minimum rather than inside it, which
is the reading § 165 Abs. 2's "surrender value … including profit shares" [R2] supports. **The
alternative reading, in which the floor also carries the *Ansammlungsguthaben*, is not implemented
and would make the floor bind at every duration**; the chosen reading lets the floor bind early and
stop binding once the surplus account has outgrown the interest residual and the *Stornoabzug*, so
both branches of the `max()` are exercised on the anchor cell alone.

*Beitragsfreistellung* is a deterministic election at `t = pup_year`, tested at the end of the
preceding year:

    pup_value_pp = max( av_pp_at(pup_year−1,"AFT_INT"), av_spread_pp_at(pup_year−1,"AFT_INT") )
    pup_cashout  = ( pup_value_pp / 10 000 × f_g ) < min_annuity_mth

If `pup_cashout` is false the contract continues premium-free: `P(t) = 0` from `pup_year`, the
*Deckungskapital* is **reset to `pup_value_pp`** — the § 165 rule that the paid-up benefit is
computed on the § 169 Abs. 3–5 value, on the premium basis [R2] [REG-R28] — the *Ansammlungsguthaben*
is untouched, `Δ` is set to zero because the two accounts have merged, and the reserve-based charge
switches to `gamma_pup_rate`. **The uplift is real money and it is published**, as
`pup_uplift(t) = (pup_value_pp − av_pp_at(pup_year−1,"AFT_INT")) × l(t)`, so that the fund-level
roll-forward still closes. If `pup_cashout` is true the contract is **cashed out instead**, the whole
surviving cohort leaving at the end of year `pup_year − 1` through the surrender decrement at `R(t)`
[R2]. **No *Stornoabzug* is applied on the paid-up route [std]**: Abs. 5 is drafted for a payout on
*Kündigung*, and here the contract continues. The alternative is a documented variant.

### Decrements and the in-force recursion

Accumulation phase, `t ≤ n`, deaths before surrenders **[std]**:

    pols_death(t) = l(t) × q(t)
    pols_lapse(t) = ( l(t) − pols_death(t) ) × w(t)
    D(t)          = ( prem_refund ? prem_cum_pp(t) + P(t)
                    : deckungskapital ? av_pp_at(t,"AFT_INT")
                    : max(of the two) )  + ( db_incl_surplus ? av_sur_pp_at(t,"AFT_INT") : 0 )
    claims(t,"DEATH") = D(t) × pols_death(t)
    claims(t,"LAPSE") = R(t) × pols_lapse(t)
    l(t+1)        = l(t) − pols_death(t) − pols_lapse(t) − pols_commutation(t)

Payout phase, `t > n`: mortality only, no surrender, no premium.

    pols_death(t) = l(t) × q(t)
    pols_lapse(t) = 0
    l(t+1)        = l(t) − pols_death(t)

Note that `D(t)` uses **end-of-year** balances while `Ď(t)` in the risk charge uses start-of-year
ones; they are different quantities with deliberately similar names, and the model publishes both.

### The *Rentenbeginn*

All of it happens at the end of policy year `n`, on the survivors of that year's decrements:

    capital_gross_pp = av_pp_at(n,"AFT_INT") + av_sur_pp_at(n,"AFT_INT")
    val_reserve_pp   = val_reserve_rate × capital_gross_pp
    K                = max( guar_capital_pp, capital_gross_pp + val_reserve_pp )
    f                = max( f_g, f_c )
    G                = K / 10 000 × f

    pols_surv_rb          = l(n) − pols_death(n) − pols_lapse(n)
    pols_commutation(n)   = κ × pols_surv_rb
    pols_annuitization(n) = (1 − κ) × pols_surv_rb
    claims(n,"COMMUTATION") = K × pols_commutation(n)
    l(n+1)                = pols_annuitization(n)

`f_c` is read from `rentenfaktor_table.csv` at `(rf_scenario_id, issue_age + n)` — the annuitant's
attained age at *Rentenbeginn*. The commuting policyholders receive `K`, the same capital the
annuitants convert, *Bewertungsreserven* included [S9]: the corpus gives no basis for paying them
less, and inventing one would be a charge no source supports.

### The annuity in payment

    U(t) = sur_ann_rate × G                                                  konstant
         = G × ( (1 + sur_ann_growth)^(t − n − 1) − 1 )                      volldynamisch
         = θ·sur_ann_rate·G + G × ( (1 + θ·sur_ann_growth)^(t−n−1) − 1 )     teildynamisch, θ = 0.5

    annuity_pp(t)   = 12 × ( G + U(t) )
    a(t)            = 0                        for t ≤ n
                    = pols_annuitization(n)    for n < t ≤ n + m      inside the Rentengarantiezeit
                    = l(t)                     for t > n + m
    annuity_payments(t) = annuity_pp(t) × a(t)

`a(t)` is the mechanic the *Rentengarantiezeit* consists of: inside the guarantee window the
instalment is due whether or not the annuitant is alive, so it is weighted by the **annuitised**
count and not by survivors [R17] [R24]. Because `l(t) ≤ pols_annuitization(n)` throughout the payout
phase, `a(t) = max(l(t), 1{n < t ≤ n+m} × pols_annuitization(n))`, which is how
`check_annuity_guarantee()` states it. The twelve is the compression of monthly-in-advance onto the
annual grid **[std]** (gap 19).

### Expenses and the cash flow statement

    base(t)      = l(t)  for t ≤ n,   a(t)  for t > n
    expenses(t)  = expense_acq_pp × 1{t = t0 and duration_init = 0}
                 + ( t ≤ n ? expense_maint_pp : expense_annuity_pp ) × (1+expense_infl)^(t−1) × base(t)
                 + expense_claim_pp × ( pols_death(t) + pols_lapse(t) + pols_commutation(t) )

    net_cf(t)      = premiums(t) − claims_death(t) − claims_lapse(t) − claims_commutation(t)
                     − annuity_payments(t) − expenses(t)
    liability_cf(t) = − net_cf(t)

`result_cf()` returns a `DataFrame` indexed by `t` (`index.name == "t"`), contiguous from
`duration_init + 1` to `proj_len()`, with these columns **in this order**:

    pols_if, pols_annuity, av, av_sur, premiums, prem_to_av, int_credited, bonus_credited,
    claims_death, claims_lapse, claims_commutation, annuity_payments, expenses, liability_cf, net_cf

`av`, `av_sur`, `prem_to_av`, `int_credited` and `bonus_credited` are **state movements reported, not
cash flows summed**: the *Sparbeitrag* and the two credits move money inside the contract and never
cross the boundary. The cash flows are `premiums`, the three `claims_*`, `annuity_payments` and
`expenses`, and those six are exactly what `check_net_cf()` reconciles.

### The published identities

| Cells | Identity |
|---|---|
| `check_net_cf()` | `net_cf(t) = premiums − claims_death − claims_lapse − claims_commutation − annuity_payments − expenses`, and `liability_cf(t) = −net_cf(t)` |
| `check_pols_roll_fwd()` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_commutation(t)`, and `pols_if(t) ≥ 0` |
| `check_decrement_closure()` | `Σ_t (pols_death + pols_lapse + pols_commutation) + pols_if(N+1) = pols_if_init()`, with `pols_if(N+1) = 0` because `mort_rate(omega_age − 1) = 1` |
| `check_av_roll_fwd()` | `av(t) + prem_to_av(t) − charge_from_av(t) + int_credited(t) + pup_uplift(t) − av_release(t) = av(t+1)` |
| `check_av_sur_roll_fwd()` | `av_sur(t) + bonus_credited(t) − av_sur_release(t) = av_sur(t+1)` |
| `check_prem_split()` | `prem_pp(t) = prem_to_av_pp(t) + charge_from_prem_pp(t)` and `charge_due_pp(t) = charge_from_prem_pp(t) + charge_from_av_pp(t)` |
| `check_cv_floor()` | `cv_pp(t) = max(cv_tariff_pp(t), cv_floor_pp(t))` and `cv_pp(t) ≥ cv_floor_pp(t)` [REG-R28] |
| `check_annuity_conv()` | `annuity_guar_mth_pp × 10 000 = capital_conv_pp × annuity_rate_appl()`, `annuity_rate_appl() = max(f_g, f_c) ≥ f_g`, and `capital_conv_pp ≥ guar_capital_pp` [S4] [S9] |
| `check_annuity_guarantee()` | `pols_annuity(t) = max(pols_if(t), 1{n < t ≤ n+m} × pols_annuitization(n))` for `t > n`, and `= 0` for `t ≤ n` |

Each has a per-`t` residual companion `check_*_resid(t)`; each takes no argument and returns a
`bool`. `check_net_cf()` is required of every delib model by the library's first ruling and is
asserted in `tests/test_model_conventions_de.py`.

---

## Annual processing order

For `t = t0 … N`, in this order. Steps 4 to 9 run only in the accumulation phase, step 10 only at
the boundary, step 11 only in the payout phase.

1. **Open the year.** `age(t) = issue_age + t − 1`, `calendar_year(t) = issue_year + t − 1`. The
   opening state is `pols_if(t)`, `av_pp(t)`, `av_sur_pp(t)`, `spread_diff_pp(t)`, `alpha_cum_pp(t)`
   and `prem_cum_pp(t)`.
2. **Test the phase and the elections.** Accumulation if `t ≤ n`, payout if `t > n`;
   `paid_up(t)` is true if `pup_year > 0 and t ≥ pup_year`. If `t = pup_year` and the contract is
   converting, `av_pp(t)` has already been reset to `pup_value_pp` by step 1's recursion and
   `spread_diff_pp(t)` to zero; `pup_uplift(t)` records the difference.
3. **Look up the year's rates.** `mort_rate_guar(t)` from the generational surface at
   `(sex, age(t), calendar_year(t))`, `mort_rate(t) = mort_rate_guar(t) × mort_be_factor`,
   `lapse_rate(t)` from the duration table (zero if `t > n`), `decl_rate(t)` from the declared-rate
   path and `bonus_rate(t) = max(0, decl_rate(t) − int_rate_guar)`.
4. **Premium in advance.** `prem_pp(t)`; `premiums(t) = prem_pp(t) × pols_if(t)`.
5. **Decompose it.** `charge_acq_pp`, `charge_prem_pp`, `charge_admin_pp` and `charge_risk_pp` — the
   last two on **start-of-year** balances — then `charge_from_prem_pp`, `charge_from_av_pp` and the
   *Sparbeitrag* `prem_to_av_pp`.
6. **Credit the *Deckungskapital*.** `av_pp_at(t,"AFT_PREM") = av_pp(t) + prem_to_av_pp(t) −
   charge_from_av_pp(t)`.
7. **Accrue the guarantee.** `int_credited_pp(t) = int_rate_guar × av_pp_at(t,"AFT_PREM")`;
   `av_pp_at(t,"AFT_INT")` follows. **This is the [std] ordering** — premium, then charges, then
   interest on what is left — and no source in the corpus fixes it [S11].
8. **Credit the surplus.** `bonus_credited_pp(t)` to the *Ansammlungsguthaben*, at year end [R24].
9. **Roll the spread account.** `spread_diff_pp_at(t,"AFT_INT")`, and hence
   `av_spread_pp_at(t,"AFT_INT")` and the surrender value `cv_pp(t)`.
10. **End of year — decrements, accumulation phase.** Death at `mort_rate(t)` paying `db_pp(t)`;
    then surrender on the survivors at `lapse_rate(t)` paying `cv_pp(t)`. Where `t = pup_year − 1`
    and `pup_cashout` is true, the **whole surviving cohort** leaves through the surrender decrement.
11. **End of policy year `n` — the *Rentenbeginn*.** Strike `capital_gross_pp`, add
    `val_reserve_pp`, apply `max(guar_capital_pp, ·)` to get `K`; determine
    `f = max(annuity_rate_guar, annuity_rate_curr)`; split the survivors between
    `pols_commutation(n)` and `pols_annuitization(n)`; pay `claims(n,"COMMUTATION")`; strike `G`.
    Both account balances go to zero.
12. **Payout phase, start of year.** `annuity_pp(t) = 12 × (G + U(t))` paid on `pols_annuity(t)`,
    which is the annuitised count inside the *Rentengarantiezeit* and survivors after it.
13. **Expenses.** Acquisition at `t = t0` for new business; maintenance or annuity administration per
    policy on `base(t)`, inflated; settlement expense on deaths, surrenders and commutations.
14. **Roll forward.** `pols_if(t+1)`, `av_pp(t+1)`, `av_sur_pp(t+1)`, `spread_diff_pp(t+1)`,
    `alpha_cum_pp(t+1)`, `prem_cum_pp(t+1)`.
15. **Publish.** `net_cf(t) = premiums − claims_death − claims_lapse − claims_commutation −
    annuity_payments − expenses`, and `liability_cf(t) = −net_cf(t)`.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one
becomes a test in `tests/test_klassische_rentenversicherung_de.py`.

1. **Adding the declared rate on top of the guarantee.** The *laufende Verzinsung* **is** the
   *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53]. Assert
   `int_credited_pp(t) + bonus_rate(t)·av_pp_at(t,"AFT_PREM") = decl_rate(t)·av_pp_at(t,"AFT_PREM")`
   whenever `decl_rate(t) ≥ int_rate_guar`, and that on model point 6 — a 2,75 % vintage against a
   2,55 % declaration — `bonus_rate(t) = 0` at every `t` while `int_credited_pp(t) > 0`. A model that
   credits 1,00 % **and** 2,55 % overstates the anchor cell's *Deckungskapital* by more than half.
2. **Getting the within-year order wrong.** Premium, then charges, then interest on the balance
   [std]. Crediting interest before the charges, or on the opening balance only, changes year-one
   interest by the whole of `i × (S(1) − C(1))`. Assert `int_credited_pp(t)` equals
   `int_rate_guar × av_pp_at(t,"AFT_PREM")` exactly, and that
   `av_pp_at(t,"AFT_INT") ≠ (av_pp(t))·(1+i) + S(t)` on the anchor cell.
3. **Applying only the guaranteed *Rentenfaktor*.** The rule is `max(guaranteed, current)` [S4]
   [R24]. Assert `annuity_rate_appl() = 32.00` on the anchor (the current factor wins) and
   `= annuity_rate_guar` on point 13 (the guarantee binds), and that
   `annuity_rate_appl() ≥ annuity_rate_guar` on every point. A model taking the guaranteed factor
   alone understates the anchor's annuity by 12,5 %.
4. **Weighting the guaranteed annuity by survivors.** Inside the *Rentengarantiezeit* the instalment
   is due whether the annuitant lives or not [R17] [R24]. Assert
   `pols_annuity(t) = pols_annuitization(n)` for `n < t ≤ n + m` and `= pols_if(t)` after, and that
   the two differ at `t = n + m` on the anchor. Assert also that point 9, with `rgz_years = 0`, has
   `pols_annuity(t) = pols_if(t)` at every payout `t`.
5. **Treating *Beitragsfreistellung* as a lapse.** They are separate decrements with different
   consequences: the paid-up contract keeps its guarantee vintage and its guaranteed *Rentenfaktor*
   and pays a reduced benefit; the surrendered one is gone for cash [R1] [R2]. Assert that on point 7
   `pols_if` is unbroken through `pup_year`, `prem_pp(t) = 0` from it, `int_rate_guar` is unchanged,
   and `claims_lapse(pup_year) = 0`.
6. **Booking the *Kostenbeitrag* as an expense.** The charges are internal deductions that move money
   inside the contract; `expenses` is the insurer's best-estimate outgo. Assert
   `expenses(t) ≠ charge_due_pp(t) × pols_if(t)` and that `expenses(t)` is invariant to
   `beta_rate` and `gamma_rate`, while `av_pp(t+1)` is not. Double-counting them inflates outgo by
   the whole charge load and is the commonest way to make a German model look conservative.
7. **Computing the surrender value off the zillmered reserve.** § 169 Abs. 3 floors it at the reserve
   with acquisition costs spread evenly over the first five contract years [REG-R28]. Assert
   `cv_pp(t) = max(cv_tariff_pp(t), cv_floor_pp(t))`, that the floor **binds** in the anchor's early
   years and **stops binding** later, and that omitting it changes `claims_lapse` in year 2 by the
   whole of `spread_diff_pp_at(2,"AFT_INT")`.
8. **Letting the *Stornoabzug* recover acquisition costs.** § 169 Abs. 5 permits a deduction only if
   agreed, quantified and appropriate, and voids one for unamortised acquisition costs [R1]
   [REG-R28]. Assert that `surr_charge_pp(t)` is a flat percentage of the pre-deduction value and
   carries **no** duration term, and that `cv_pp(t)` never falls below `cv_floor_pp(t)` however large
   `stornoabzug_rate` is set.
9. **Using one mortality basis where the product uses two.** The first-order basis fixes the risk
   charge and the guaranteed benefits; the second-order basis drives the projection [REG-R47].
   Assert `mort_rate(t) = mort_rate_guar(t) × mort_be_factor` with `mort_be_factor > 1`, that
   `charge_risk_pp` uses `mort_rate_guar` and `pols_death` uses `mort_rate`, and that swapping them
   changes `net_cf`.
10. **Using a period mortality table.** DAV 2004 R is a *Generationentafel*; a period-table proxy
    priced at an annuitisation decades ahead understates the liability by a margin that dwarfs every
    other assumption [REG-R49]. Assert `mort_rate_guar` depends on `calendar_year(t)` as well as
    `age(t)`: on the anchor, `mort_rate_guar` at attained age 67 in 2043 must be **strictly below**
    the same age's rate for a life reaching 67 in 2026.
11. **Charging the risk premium on a zero net amount at risk.** With
    `death_benefit_form = deckungskapital` the death benefit **is** the reserve, so there is nothing
    at risk. Assert `charge_risk_pp(t) = 0` at every `t` on points 2 and 12, and that
    `charge_risk_pp(t) > 0` early and falls towards zero on the anchor as the *Deckungskapital*
    catches up with the premiums paid.
12. **Deducting the payout-phase administration charge from the annuity.** The *Rentenfaktor* is
    exogenous here and already carries the tariff's payout loading, so `annuity_admin_rate` is
    recorded in `charge_table.csv` and **not applied**. Assert
    `annuity_payments(t) = 12 × (G + U(t)) × pols_annuity(t)` exactly, with no charge term, and that
    the model's `expenses` in the payout phase are the per-policy `expense_annuity_pp` only.
13. **Paying a death benefit after *Rentenbeginn*.** *Beitragsrückgewähr in der Rentenbezugsphase*
    **was not established by any source in this corpus** and must not be asserted (gap 18); what the
    corpus establishes for post-*Rentenbeginn* death is the *Rentengarantiezeit* and the survivor's
    annuity rider [R24] [S10]. Assert `claims_death(t) = 0` for every `t > n` on every model point.
14. **Letting the *Kapitalwahlrecht* leave the account behind.** Commuting policyholders receive
    `capital_conv_pp` — the same capital annuitants convert, *Bewertungsreserven* included [S9].
    Assert `claims_commutation(n) = capital_conv_pp × kapitalwahl_rate × pols_surv_rb`, that both
    account balances are zero from `t = n + 1`, and that on point 9 (`kapitalwahl_rate = 1.00`)
    `pols_if(t) = 0` and every cash flow is zero for `t > n`.
15. **Forgetting that the guarantee vintage is a model-point attribute.** Existing contracts keep the
    *Rechnungszins* they were written on [R7] [REG-R14]. Assert that points 1, 6 and 14 credit
    1,00 %, 2,75 % and 0,90 % respectively, and that a single global rate would change point 6's
    *Deckungskapital* at `Rentenbeginn` by more than a fifth.
16. **Letting `sex` reach the tariff.** Unisex has been compulsory since 21 December 2012
    [REG-R34]. Assert that two model points identical but for `sex` produce identical `prem_pp`,
    identical `charge_*` except through `mort_rate_guar`, and identical `annuity_rate_appl()`.
17. **Amortising the acquisition charge against a shrunken *Beitragssumme*.** The § 4 DeckRV base is
    the sum of all premiums payable under the contract as written [REG-R16], not the premiums a later
    *Beitragsfreistellung* leaves behind. Assert `alpha_total_pp` on point 7 is unchanged by
    `pup_year`, and that `alpha_cum_pp` never exceeds `alpha_total_pp`.
18. **Truncating the payout phase.** A life annuity has no term; `proj_len() = omega_age −
    issue_age`. Assert `result_cf().index[-1] == proj_len()`, that `pols_if(proj_len()+1) = 0`, and
    that the decrement closure sums to `pols_if_init()` exactly. A 40-year horizon on the anchor cell
    would drop a real, if small, tail of annuity payments beyond attained age 90.

---

## Policyholder behaviour modelling

Every formula here is **[std]**; nothing in the corpus calibrates any of it (gap 20).

- **Base surrender.** The duration table above, with the **duration-12 step** at the § 20 Abs. 1
  Nr. 6 EStG twelve-year threshold [R6] [REG-R45]. The shape is the assumption; the levels are
  placeholders. A German Schicht-3 projection with a lapse rate flat in duration has ignored the
  strongest single driver of German surrender behaviour.
- **No dynamic surrender.** The obvious German dynamic term would key the surrender rate on the gap
  between a market rate and the declared *laufende Verzinsung*, as frlib's euro-fund model keys it on
  the Livret A gap. It is **not implemented here**, for a reason worth stating: on this product the
  policyholder who surrenders forfeits a *guaranteed Rentenfaktor* struck on bases decades old, and
  the value of that forfeited option is exactly what a rate-gap formula does not capture. A model
  that adds a naive rate-gap term to a book of 4,00 % vintages will lapse precisely the contracts a
  real policyholder would never surrender.
- ***Beitragsfreistellung* as an election, not a rate.** A scalar per-policy account cannot carry two
  sub-populations with different *Deckungskapital*, and splitting the account would double the
  accumulation-phase state for a mechanic whose rate no source establishes. The model therefore
  carries `pup_year` as a **deterministic election** on the model point, exercises both of its
  statutory branches (conversion, and cash-out below the *Mindestversicherungsleistung*) on points 7
  and 8, and says here that a portfolio model needs the sub-population split this one does not have.
- **The *Kapitalwahlrecht* as a take-up rate.** `kapitalwahl_rate` is a model-point attribute, base
  30 % [std]. The decision it stands for is a tax comparison — the *Ertragsanteil* at 18 % of each
  instalment against half the *Unterschiedsbetrag* once [R5] [R6] [REG-R41] [REG-R45] — and **this
  model computes no tax**, so the rate is a stand-in for a calculation it does not perform, not an
  estimate of one.
- **What is deliberately absent.** No *Widerruf* decrement (it sits inside the year-1 lapse rate,
  [REG-R23]); no premium-default path, although § 166 VVG makes German lapse a **three-way**
  decrement in reality [REG-R28] [REG-R30]; no *Wiederinkraftsetzung* [S11]; no selective-lapsation
  mortality loading; and no take-up modelling for the *Dynamik*, whose parameters are unestablished
  (gap 15).

---

## Worked example

**Configuration.** Model point 1, `point_id = 1`, `policy_id = DE-RV-0001`: `sex = M`;
`issue_age = 50`; `issue_year = 2026`; `duration_init = 0`, so the frame opens at `t = 1`;
`pols_if_init = 1.0`; `premium_form = laufend`; `prem_gross_pp = 3 000,00 €`;
`premium_single_pp = 0,00 €`; `prem_freq = annual`, hence `freq_load = 1,000`; `prem_term_y = 17`;
`aufschub_y = 17`, so the *Rentenbeginn* falls at the end of policy year 17, at attained age 67;
`int_rate_guar = 1,00 %`, the 2026 vintage [REG-R15]; `charge_id = zillmer_25`;
`annuity_rate_guar = 28,00 €` per month per 10 000 €; `rf_scenario_id = base`;
`decl_scenario_id = base`; `guar_capital_pp = 0,00 €`, so the guaranteed-contract-value floor is
inoperative on this cell; `death_benefit_form = prem_refund`; `db_incl_surplus = 0`;
`rgz_years = 10`; `kapitalwahl_rate = 0,30`; `pup_year = 0`; `dynamik_rate = 0,0000`;
`payout_system = konstant`; `av_pp_init = 0,00 €`; `av_sur_pp_init = 0,00 €`;
`prem_cum_pp_init = 0,00 €`; `alpha_amort_pp_init = 0,00 €`. Hence `proj_len() = 121 − 50 = 71`, the
accumulation phase is `t = 1 … 17`, the *Rentengarantiezeit* covers `t = 18 … 27`, and the
survivor-weighted annuity runs from `t = 28` to `t = 71`.

**Assumptions, each tagged.** *Contractual and cited:* the *Rechnungszins* `i = 1,00 % p.a.`
[REG-R15]; the *Höchstzillmersatz* `alpha_rate = 25 ‰` of the *Beitragssumme* [REG-R16], giving
`beitragssumme_pp = 17 × 3 000,00 = 51 000,00 €` and `alpha_total_pp = 1 275,00 €`, zillmered — taken
in full from the year-1 premium and nil thereafter; the § 169 Abs. 3 five-year spread,
`alpha_spread_years = 5`, giving `α̃(t) = 255,00 €` for `t = 1 … 5` [REG-R28]; the § 165
*Mindestversicherungsleistung* test, not triggered on this cell [R2]; the death benefit
*Beitragsrückgewähr*, the premiums paid to date, premiums only [S1] [R24]; the conversion rule
`monthly annuity = capital / 10 000 × Rentenfaktor` [R24]; and the applied factor
`max(garantiert, aktuell)` [S4] [R24]. *Insurer-discretionary current:* the declared *laufende
Verzinsung* `decl_rate = 2,55 % p.a.` level on the `base` path **[std]**, hence
`bonus_rate = max(0; 2,55 % − 1,00 %) = 1,55 % p.a.` **[std]**, with the *Ansammlungsguthaben*
itself credited at the full 2,55 % **[std]**; the *Bewertungsreserven* crystallisation
`val_reserve_rate = 1,5 %` of the accumulated value at *Rentenbeginn* **[std]** [S4] [R4]; the
*aktueller Rentenfaktor* at age 67 on the `base` path, `32,00 €` per month per 10 000 € **[std]**,
which exceeds the guaranteed `28,00 €` and therefore wins the `max()`; and the *Überschussrente*
under the `konstant` system, `sur_ann_rate = 12 %` of the *garantierte Rente*, level **[std]**.
*Charges (all levels [std]):* `beta_rate = 4,0 %` of each gross premium; `gamma_rate = 0,20 % p.a.`
of the *Deckungskapital*; the *Risikobeitrag* `ρ(t) = mort_rate_guar(t) × max(0, prem_cum_pp(t) +
prem_pp(t) − av_pp(t))`; `stornoabzug_rate = 2,0 %` of the pre-deduction value, subject to the
§ 169 Abs. 3 floor [R1] [REG-R28]; `annuity_admin_rate = 1,5 %`, recorded and **not applied**
(pitfall 12). *Behavioural and experience (all [std]):* first-order mortality from the shipped
generational proxy, `mort_rate_guar(t) = q_base(M, x(t)) × (1 − improve(x(t)))^(τ(t) − 2005)` with
the anchor `q_base(M, 50) = 0,002000` and `improve(x) = 1,5 %` below age 60 grading to 0,5 % at 100
and to zero at 110; best-estimate mortality `mort_rate(t) = mort_rate_guar(t) × 1,15`; surrender
6,0 % / 5,0 % / 4,5 % / 4,0 % (durations 4–7) / 3,5 % (8–11) / **6,0 % at duration 12** / 3,0 %
thereafter, and **zero from *Rentenbeginn***; the *Kapitalwahlrecht* take-up 30 %; and expenses of
400,00 € acquisition at issue, 45,00 € per policy p.a. in the accumulation phase and 30,00 € p.a. in
the payout phase, both inflating at 2,0 % p.a., plus 120,00 € per death, surrender or commutation
event. `omega_age = 121` **[std]**. No *Dynamik*, no *Beitragsfreistellung*, no
*guar_capital_pp* floor, no behavioural modules.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library publishes gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, never reproduced.

- **The German statutory *Deckungsrückstellung*.** The HGB reserve of § 341f HGB, computed
  prospectively **on the *Rechnungsgrundlagen* of the premium calculation** [REG-R54] and discounted
  at no more than the § 2 DeckRV rate applicable when the contract was concluded [REG-R14]. It is
  **not** the Solvency II best estimate: an insurer carries two liability measures, and the
  *Überschussbeteiligung*, the *Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all
  run on the **HGB** side [REG-R14] [REG-R54]. `av_pp(t) × pols_if(t)` is this model's contribution
  to that line, not the line itself — a statutory *Deckungskapital* is a prospective reserve on
  first-order bases while `av_pp` is a retrospective account roll-forward, and the two coincide only
  under assumptions this model does not impose.
- **The *Zinszusatzreserve*.** Arises where the § 5 Abs. 3 DeckRV *Referenzzins* falls below a
  contract's tariff rate, and the § 12 MindZV *Sicherungsbedarf* test compares a Bundesbank month-end
  swap rate with **the highest *Rechnungszins* applicable to the contract over the next fifteen
  years** — a window that bites hardest on annuity business [REG-R17] [REG-R18]. Model points 6 and
  14, on 2,75 % and 0,90 % vintages, are exactly the cells that would carry one. **Not computed.**
- **The surplus layer.** The MindZV's 90 / 90 / 50 minima are a minimum **transfer to the RfB**, not
  a minimum payout [REG-R18] [REG-R10] [REG-R19]. This model represents the **credited outcome** —
  `decl_rate` and the *Ansammlungsguthaben* — not the three result sources that fund it; a model of
  the surplus chassis itself belongs in delib's `kapitallebensversicherung`.
- **Solvency II.** Best estimate plus risk margin [REG-R6], `BEL = Σ_t v(t) × liability_cf(t)` over
  the stream this model publishes, with the future discretionary benefits — the surplus credit and
  the *Bewertungsreserven* crystallisation — the substance of the calculation. **No risk-free curve,
  cost-of-capital rate or contract-boundary rule in this library was read from a retrieved
  instrument** [REG-R2] [REG-R4], so every such figure would be [std]. And **the guarantees are
  options**: the `max(guaranteed, current) Rentenfaktor` [S4] is a written option on the insurer's
  own future annuity tariff and the *Rechnungszins* floor a written interest guarantee, neither of
  which the deterministic path prices. A stochastic-on-deterministic run — this recursion, the
  crediting rule and the conversion rule re-evaluated per scenario — is what a
  time-value-of-options-and-guarantees calculation consumes.
- **IFRS 17 and professional standards.** A profit-participating deferred annuity would be measured
  under the variable fee approach [REG-R55], on this same fulfilment-cash-flow engine; actuarial work
  sits under the DAV *Fachgrundsätze* and the § 141 VAG *Verantwortlicher Aktuar*, distinct from the
  MaGo's *versicherungsmathematische Funktion* [REG-R56] [REG-R11] [REG-R21].

---

## Key sensitivities and model risks

In rough order of leverage on a German deferred-annuity block.

1. **The *Rentenfaktor*, and the fact that it is not calibrated to the shipped mortality table.**
   The annuity amount is `K / 10 000 × f`, so the whole payout phase scales linearly with `f`, and
   `f` is **[std]** with no market anchor of any kind (gap 3). The reference library warns that a
   model publishing a [std] *Rentenfaktor* **and** a [std] annuity table must say whether the two are
   consistent and which is authoritative [REG-R49]. **They are not calibrated to each other, and the
   *Rentenfaktor* is authoritative**: it fixes the benefit amount, while the mortality proxy fixes
   only how long that amount is paid. The model publishes `annuity_due_factor()` — the annuity-due
   present value on the shipped proxy at the guarantee interest basis — purely as a diagnostic, so
   the gap is visible rather than hidden. Anyone substituting a real DAV 2004 R must re-strike the
   *Rentenfaktoren* with it or accept an inconsistency the model will not flag.
2. **The declared rate and the guarantee vintage together.** `bonus_rate = max(0, decl_rate −
   int_rate_guar)` is a difference of two numbers of similar size, so a 25 bp move in `decl_rate`
   moves the *Ansammlungsguthaben*'s accrual by about 16 % on the 1,00 % vintage and by **all of it**
   on the 2,75 % vintage, where the rate is already clipped at zero. The declared path is a level
   [std] scenario, not a forecast, and the market's own 2026 averages disagree with each other by
   33 bp [REG-R53].
3. **Mortality, in two dimensions.** For a deferred annuity the improvement trend matters more than
   the level, because the conversion happens decades out: on the anchor cell the annuitant reaches 67
   in 2043, 38 improvement years after the proxy's 2005 base. Both `q_base` and `improve` are [std],
   and the trend is the more dangerous of the two — the German construction uses a *Starttrend*
   converging to a weaker *Zieltrend* and the proxy uses a single age-graded rate, which is a
   documented simplification and not a replication [REG-R49].
4. **The surrender assumption, and the option it ignores.** Cumulative surrender over the anchor's
   seventeen accumulation years is material, and every surrendering policy forfeits a guaranteed
   *Rentenfaktor* struck on bases that will look generous by 2043. The model's lapse rates are
   unconditional; a policyholder who valued the forfeited option would surrender less. The
   direction of the error is therefore known and one-sided.
5. **The *Kapitalwahlrecht* take-up rate.** At 30 % it removes nearly a third of the annuity block at
   `t = 17` and replaces it with a single payment. It is a pure [std] with no evidence (gap 20), and
   it substitutes for a tax comparison the model does not perform [R6] [REG-R45].
6. **The charge set, and the § 169 Abs. 3 floor it collides with.** `alpha_rate` at the statutory
   ceiling makes the year-one *Sparbeitrag* small and the early *Deckungskapital* correspondingly
   thin, but the floor then reverses most of that for surrender purposes [REG-R16] [REG-R28], so the
   two parameters must be moved together.
7. **The annual grid against a monthly annuity.** Neither the annuity's payment timing nor its
   in-advance/in-arrears basis was established [S13] [R24] (gap 19). Compressing twelve monthly-in-advance instalments into one start-of-year payment is
   generous to the payout phase by roughly half a year's interest on one year's annuity, every year.
8. **Everything the model does not do.** No *Bonusrente*, no *Zuzahlung*, no survivor's annuity, no
   § 163 VVG adjustment, no *Zinszusatzreserve*, no MindZV allocation, no *Sicherungsbedarf* test, no
   tax. Each is named where it belongs above; together they are the reason this is a mechanics
   demonstration and not a valuation.
