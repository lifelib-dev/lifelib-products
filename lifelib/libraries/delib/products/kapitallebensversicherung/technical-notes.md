# Technical Notes

**Status:** Draft, 2026-08-29 (all cited sources accessed 2026-08-29).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`KLV_DE_A`**, **annual** grid — for the standardized composite German *kapitalbildende
Lebensversicherung* defined in `product-spec.md` (same directory). **This is not any single insurer's
product.** [S#] / [R#] tags refer to the source list in `sources.md` (numbering carried from
`_research/kapitallebensversicherung.md`; frozen); [REG-R#] tags refer to the cross-product library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R56 numbering). **[std]** marks
a standardization introduced for the reference implementation; [unverified] marks a claim no search
result corroborated. Parameter values are identical to those in `product-spec.md`. **No document
cited anywhere in this library was retrieved** — direct HTTP egress from the build environment is
blocked and everything rests on `WebSearch` result summaries — so a delib citation names the
instrument a claim should be checked against and does not assert that anyone checked it. Cells names,
model-point columns and CSV headers are English `lower_snake_case`; German terms of art keep their
German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — *Beiträge* in;
  *Todesfallleistungen*, *Erlebensfallleistungen* and *Rückkaufswerte* out; insurer expenses and
  commission — for a single-policy model point on an expected (probability-weighted) basis, together
  with the three state variables that make the product what it is: the guaranteed *Deckungskapital*,
  the accumulated *Überschussguthaben* and the accrued *Schlussüberschussanteil*.
- **Out of scope, and said so.** No discounting. **No *Deckungsrückstellung***: the model projects the
  contract's *Deckungskapital* — the amount that should be held — not the balance-sheet quantity of
  § 341f HGB [REG-R54]. No *Zinszusatzreserve* [REG-R17], no RfB stock [REG-R10] [REG-R19], no MindZV
  allocation [R6] [REG-R18], no P&L, no Solvency II technical provision, risk margin, SCR or MCR
  [REG-R1] [REG-R2] [REG-R6]. No *Beteiligung an den Bewertungsreserven* in the base run — the
  parameter exists and is zero [R1] [R8]. No tax: delib publishes gross benefits, and the tax rules
  enter only as design constraints. No premium-default path, §§ 37 and 38 VVG never having been
  researched (gap 20); no supervisory write-down under § 222 or § 314 VAG [REG-R12]; no
  *Zusatzversicherungen*, *Kapitalwahlrecht*, *Dynamik* or *Beleihung*.
- **Projection frequency.** **Annual grid**, which is the contract's own operative clock: the surplus
  is declared once a year and allocated at the *Bilanzstichtag* [S9], the *Rückkaufswert* is struck at
  the end of the current *Versicherungsperiode* [R2], the *beitragsfreie Versicherungssumme* is
  tabulated *für jedes Versicherungsjahr* [R3], and the *Ablauf* falls on an anniversary [S7].
- **What `t` counts.** `t` is the **policy year**, **1-based**, measured from **issue**: policy year
  `t` runs from the (`t`−1)-th policy anniversary to the `t`-th, and `age(t) = issue_age + t − 1` is
  the attained age at the start of it. `duration(t) = t − 1` is the number of completed policy years
  at the start of year `t`, and it is what every duration-keyed schedule — the *Stornoabzug*, the
  lapse table, the § 169 Abs. 3 five-year spreading, the *beitragsfreie Versicherungssumme* — is
  indexed on. **Counting `t` from issue rather than from the valuation date is the choice that makes
  every one of those lookups direct.**
- **Where the frame starts, and `proj_len()`.** `proj_len() = policy_term`: the **last projected
  period index**, which is the policy year in which the *Ablauf* falls and the *Erlebensfallleistung*
  is paid. The frame runs `t = t_start() … proj_len()` contiguously, with
  `t_start() = duration_init + 1`, so a new-business point (`duration_init = 0`) opens at `t = 1` and
  an in-force point opens at the duration the policy has already run. Hence
  `result_cf().index[-1] == proj_len()` on every model point, `result_cf().index[0] == t_start()`, and
  `pols_if(t_start()) == pols_if_init()`. **There is no `t = proj_len() + 1` row**: the contract ends
  when the maturity benefit is paid.
- **Timing conventions [std].** *Beiträge* at the **start** of the policy year (annual in advance);
  acquisition expense and initial commission at issue; maintenance expense and renewal commission at
  the start of the year on the in-force; the guaranteed *Deckungskapital* rolls forward over the year
  at the *Rechnungszins*; the surplus is declared and credited **at the end** of the year, on the
  closing reserve; death claims and the maturity claim at the **end** of the year; surrender at the
  end of the year, **after** the mortality decrement and **after** the surplus credit.
- **The Bilanzstichtag becomes the policy anniversary [std].** The sources put the allocation at the
  *Bilanzstichtag*, 31 December [S9]; on a policy-year grid that date falls inside a policy year for
  every contract not written on 1 January, so the model allocates at the **policy-year end**. The
  effect is a timing shift of up to one year in the surplus credit relative to a real book, stated
  rather than hidden; a calendar-year model would need a two-part first year.
- **Age basis.** Age last birthday at issue, stepping at the policy anniversary **[std]** — no located
  German endowment wording states one (`product-spec.md`, footnote 6).
- **Unisex pricing is a hard constraint.** `sex` is carried and drives the **decrement** lookup, but
  **must not enter the premium**: § 20 Abs. 2 Satz 1 AGG was repealed and new business has been unisex
  since 21 December 2012 [REG-R34]. The pricing basis is a fixed portfolio blend, and letting `sex`
  leak into `prem_gross_pp` reproduces a tariff unlawful in Germany since 2012 (pitfall 17).
- **No account value in the unit-linked sense.** The house vocabulary's `prem_to_av_pp` has **no
  counterpart here** and is not published: a *Beitrag* funds the *Deckungskapital* through the tariff,
  not a policyholder account, and the only true account is the *Überschussguthaben*, which receives
  surplus and never premium. `withdrawals` is likewise absent — a classic German endowment has no
  partial-withdrawal right in any located wording.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  claims, expenses and commission −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents and `pols_if` to six decimals **[std]**.

---

## Model point attributes

Every column of `model_point_table.csv` is published as a cells of the same name.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection`'s only parameter | all |
| `policy_id` | str | Human-readable identifier | all |
| `sex` | enum {M, F} | Decrement lookup only; **never** a pricing input [REG-R34] | 7 (F) |
| `smoker` | enum {N, S} | Feeds `rating_factor`; no published scale [R14] | 14 (S) |
| `issue_year` | int | Cohort identity: fixes the DeckRV ceilings [REG-R15] and the tax cohort [R10] | 10 (2012) |
| `issue_age` | int | Age last birthday at issue | all |
| `duration_init` | int | Completed policy years at the valuation date; 0 = new business | 10 (14) |
| `pols_if_init` | float | Policies represented at `t_start()` | all |
| `policy_term` | int | *Versicherungsdauer*, in years; equals `proj_len()` | all |
| `prem_term` | int | *Beitragszahlungsdauer* ≤ `policy_term`; **1 = *Einmalbeitrag*** | 2 (1), 3 (15) |
| `sum_assured` | EUR | Guaranteed *Erlebensfallleistung* (*Versicherungssumme*) | all |
| `death_ratio` | float | *Todesfallleistung* ÷ *Erlebensfallleistung*; 1.00 = the endowment proper | 14 (0.60) |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency | 4–7 |
| `unterjaehrig_form` | enum {echt, unecht} | Whether the sub-annual premium is a genuine sub-annual *Versicherungsperiode* (**no** loading) or an instalment of an annual one (loaded) [R28] | 4 / 5 |
| `rechnungszins` | rate | The contract's own guaranteed technical rate, fixed at conclusion [REG-R14] | 10 (1.75%) |
| `zillmer_on` | 0/1 | Whether the *Deckungskapital* is *gezillmert* [S9] | 13 (0) |
| `cost_id` | str | Key into `cost_table.csv`: the tariff loadings and the expense basis | all |
| `surplus_use` | enum {ansammlung, bonus, beitragsverrechnung} | *Überschussverwendung* [R28] | 8, 9 |
| `scenario_id` | str | Key into `surplus_rate_table.csv`: the declared-rate path | 3 (low), 14 (nil) |
| `rating_factor` | float | *Risikozuschlag* multiplier on the risk premium; 1.00 at standard rates [R5] | 14 (1.50) |
| `av_pp_init` | EUR | *Überschussguthaben* carried at the valuation date | 10 |
| `bonus_si_init` | EUR | Bonus sum insured already bought (*Bonussystem*, in force) | — |
| `bfz_year` | int | Policy year at whose end *Beitragsfreistellung* is elected; 0 = never; ≤ `duration_init` = already paid-up | 11 (10), 12 (3) |

`sum_assured` and `death_ratio` are the two halves of the *gemischte Versicherung*: the guaranteed
survival sum is `sum_assured`, the guaranteed death sum is `sum_assured × death_ratio`, and the
*Mindesttodesfallschutz* of [R12] [REG-R45] requires the latter to be at least 50 % of the
*Beitragssumme* — a **model-point design constraint**, checked when the table is built, not a model
formula. `rechnungszins` is a contract term and not a market rate: it is fixed at conclusion and stays
with the contract for its whole term [REG-R14], which is why the in-force point carries 1,75 % while
new business carries 1,00 %.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | Policies in force at the **start** of policy year `t`; `pols_if(t_start()) = pols_if_init()`. `pols_if_at(t, timing)` gives `"BEF_DECR"` / `"AFT_MORT"` / `"AFT_LAPSE"` | annual decrements |
| `res_pp(t)` | Guaranteed *Deckungskapital* per policy at the **start** of year `t` (= at duration `t − 1`), on the first-order basis. `res_pp_at(t, timing)` gives `"BEF_PREM"` / `"AFT_PREM"` / `"AFT_INT"` | annual, prospective, with a roll-forward check |
| `av_pp(t)` | *Überschussguthaben* per policy at the start of year `t`; nil unless `surplus_use = ansammlung`. `av_pp_at(t, timing)` and `av_at(t, timing)` follow the house convention | annual recursion |
| `bonus_si_pp(t)` | Bonus sum insured bought out of surplus at the start of year `t`; nil unless `surplus_use = bonus` | annual recursion |
| `term_bonus_pp(t)` | Accrued *Schlussüberschussanteil* at the start of year `t`, payable at the *Ablauf* and on death, not on surrender in the base run | annual accrual |
| `is_paid_up(t)` | Whether the contract is *beitragsfrei* at the start of year `t` | set once, at `bfz_year` |
| `bfz_si_pp` | *Beitragsfreie Versicherungssumme* bought at the *Beitragsfreistellung*, or 0 where the *Mindestversicherungsleistung* test fails and the election became a surrender | once per model point |

There is **no** unit fund, **no** policyholder account fed by premium and **no** partial-withdrawal
ledger. The *Überschussguthaben* is a genuine account, but it is fed by declared surplus alone, and
§ 341f HGB confirms the separation from the other direction: the *Deckungsrückstellung* is formed
**excluding *verzinslich angesammelte Überschussanteile*** [REG-R54].

---

## Assumption inputs

**The external CSVs.** Every input is a plain UTF-8 CSV in the model folder's **parent**, read once per
model by a reader cells in `Data` — the `annuallife/TradLife_A` layout, not `basiclife/BasicTerm_S`'s
embedded IOSpec. Every file but `model_point_table.csv` carries a final **`provenance`** column, one
tag per row, which is delib's second ruling and is machine-checked.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the 22 further attributes of the table above (exempt from `provenance`) |
| `mort_table.csv` | `sex`, `age` | `mort_rate_1st`, `provenance` |
| `lapse_table.csv` | `policy_year` | `lapse_rate`, `storno_rate`, `provenance` |
| `surplus_rate_table.csv` | `scenario_id`, `policy_year` | `decl_rate`, `term_rate`, `ans_rate`, `provenance` |
| `cost_table.csv` | `cost_id` | `alpha_rate`, `beta_rate`, `gamma_rate`, `acq_expense`, `maint_expense`, `expense_infl`, `claim_expense`, `comm_init_rate`, `comm_renew_rate`, `provenance` |
| `freq_loading_table.csv` | `prem_freq` | `instalments`, `prem_freq_load`, `provenance` |
| `deckrv_table.csv` | `issue_year` | `hoechstrechnungszins`, `hoechstzillmersatz`, `provenance` |

`cost_table.csv` deliberately carries the **first-order tariff loadings and the second-order expense
assumptions on the same row**, because the difference between them *is* the *Kostenüberschuss*.
`deckrv_table.csv` carries both DeckRV ceilings — § 2's *Höchstrechnungszins* and § 4's
*Höchstzillmersatz* — keyed by `issue_year`, because both are cohort facts that travel with the
contract [REG-R14] [REG-R15] [REG-R16]. The scalar assumptions that are not tables — `mort_be_factor`,
`suicide_share`, `bfz_min_si`, `term_surr_share`, `bwr_rate` and the two behaviour-module switches —
are `Projection` References, and their values and tags are in this section.

Three classes. Class (a) is contractual or statutory and is cited; class (b) is the insurer's current
discretionary declaration, revisable annually and capable of being zero [S3] [S9]; class (c) is the
modeller's view of experience. The split is the German ***Rechnungsgrundlagen erster und zweiter
Ordnung*** distinction wearing different clothes [REG-R47]: (a) is the first-order basis, which fixes
the *Bruttobeitrag* and the guaranteed benefits — the numbers the contract states — while (c) is the
second-order basis, which drives the projection, and (b) is the output of the insurer's policy for
distributing the wedge between them.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| *Rechnungszins* `rechnungszins` | Model-point column; 1.00% for new business from 1 January 2025, the cohort's rate otherwise | [R7] [R15] [REG-R14] [REG-R15] |
| *Höchstrechnungszins* ceiling by cohort | 3.50% to 06/1994; 4.00% to 06/2000; 3.25% to 2003; 2.75% to 2006; 2.25% to 2011; 1.75% to 2014; 1.25% to 2016; 0.90% to 2021; 0.25% to 2024; **1.00% from 2025** | [REG-R15]; the split-year convention **[std]** (1) |
| *Höchstzillmersatz* ceiling by cohort | **40 ‰** of the *Beitragssumme* to 2014, **25 ‰** from 1 January 2015; the rate used at conclusion applies for the whole term | [R7] [S15] [REG-R16] [REG-R20] |
| *Zillmersatz* `alpha_rate` | 25 ‰ of the *Beitragssumme*, at the ceiling | ceiling [R7] [REG-R16]; the level **[std]**, `product-spec.md` (15) |
| Premium form | Level *Bruttobeitrag* over the *Beitragszahlungsdauer*, in advance; ceases on death [S7], on *Beitragsfreistellung* [R3] and at the end of the *Beitragszahlungsdauer* | [S3] [S7] [R3] [R28-family] |
| *Ratenzahlungszuschlag* | 2% half-yearly, 3% quarterly, 5% monthly, applied **only** to `unterjaehrig_form = unecht` | market levels [R28]; the *echt*/*unecht* gate [R28]; single values **[std]** |
| *Erlebensfallleistung* | `sum_assured` at the *Ablauf* if the insured is then alive, plus the accumulated surplus and the accrued *Schlussüberschussanteil* | [S7] [S11] [R1] |
| *Todesfallleistung* | `sum_assured × death_ratio` on death before the *Ablauf*, plus the accumulated surplus and the accrued *Schlussüberschussanteil* | [R18-family] [S11] |
| *Rückkaufswert* | The *Deckungskapital* on the *Rechnungsgrundlagen der Prämienkalkulation*, at the **end of the current *Versicherungsperiode***, floored on *Kündigung* by the five-year-spread *Mindestrückkaufswert*, less a *vereinbart*, *beziffert* and *angemessen* *Stornoabzug*, plus the *Überschussguthaben* | [R2] [R22] [R24] [REG-R28]; even-spread reading **[std]** (2) |
| *Beitragsfreistellung* | At the end of the current *Versicherungsperiode*, **if** the *Mindestversicherungsleistung* is reached; otherwise the insurer pays the § 169 value and the election **becomes a surrender**. The paid-up sum is computed on the § 169 value | [R3] [REG-R28] |
| *Selbsttötung* | Within three years of conclusion the insurer is *leistungsfrei* but **must pay the *Rückkaufswert* including *Überschussanteile*** — a benefit **substitution**, not a forfeiture | [R4] [REG-R26] |
| Surplus allocation base and timing | A percentage of the *Deckungskapital* at the allocation date [S3]; allocated at the *Bilanzstichtag* and booked into the *Deckungskapital* [S9]; entitlement from inception [S9] | [S3] [S9] [R1] |
| *Beteiligung an den Bewertungsreserven* | Half of the amount determined on termination, but only to the extent it exceeds the *Sicherungsbedarf*. **Zero in the base run** | [R1] [R8] [REG-R9] [REG-R24]; zero **[std]** |

1. The published history splits 1994 and 2000 mid-year [REG-R15] and a year-keyed table cannot. Both
   split years take the **higher** of the two rates — 4,00 % — which makes `check_rechnungszins_cap()`
   permissive rather than strict in exactly the two years where the model cannot know which half of
   the year a contract was written in. Years after 2026 carry 1,00 %, the DAV having recommended it
   for 2026 [R15], held flat thereafter **[std]**.
2. § 169 Abs. 3 VVG's "gleichmäßige Verteilung … auf die ersten fünf Vertragsjahre" [R2] is
   implemented as a **straight-line** amortisation of `alpha_cost` in five equal instalments. The
   alternative reading — a five-year *Zillmerung*, annuitising the cost over a five-year premium
   period — gives a slightly lower floor at durations 1 to 4 and the same value from duration 5, and
   is pitfall 5.

### (b) Insurer-discretionary current elements (snapshot; revisable annually, and may be zero)

| Input | Base value | Basis |
|---|---|---|
| Declared *laufende Verzinsung* `decl_rate` | **2.70% p.a., level** | Allianz's 2026 rate for its classic book — the only declared rate in the corpus attached to a classic **endowment** book by its manufacturer [S11]; the level-forever assumption **[std]** (3) |
| *Zinsüberschussanteilsatz* `zins_ueberschuss_rate` | **Derived**, `max(0, decl_rate − rechnungszins)`; 1.70% on the anchor cell | [REG-R53]; never an input, and never added on top of the guarantee (pitfall 1) |
| *Schlussüberschussanteilsatz* `term_rate` | **0.40% p.a.** of the *Deckungskapital*, accrued and paid at the *Ablauf* and on death | **[std]** (4) — **no rate of any kind was established** (gap 1) |
| *Ansammlungszinssatz* `ans_rate` | **2.70% p.a.**, equal to the declared rate | mechanism [R28]; the § 28 RechVersV disclosure names the rate as a published quantity [REG-R54]; the level **[std]** (5) |
| Scenario `low` | `decl_rate` 1.20%, `term_rate` 0.10%, `ans_rate` 1.20% | **[std]** |
| Scenario `nil` | `decl_rate`, `term_rate`, `ans_rate` all **0.00%** | the sourced statement that the surplus "may also be zero euros" [S9]; the scenario **[std]** |
| *Stornoabzug* `storno_rate` | 10% of the guaranteed value in years 1–5, 7.5% in 6–10, 5% in 11–15, 2.5% from 16 | observed range 5%–20% of the *Deckungskapital*, **one carrier, sub judice** [S3] [R22] [R30]; schedule **[std]** |
| *Bewertungsreserven* rate `bwr_rate` | **0.00%** | [R1] [R8] [REG-R9]; zero **[std]** |

3. Level for the whole projection is a modelling choice, not a forecast. The corpus supports a
   **direction** — about one in three insurers raised the rate for 2026, Allianz did not, the caution
   being attributed to remaining *stille Lasten* [R25] [R26] — and no path. Two alternative paths ship
   as scenarios so the sensitivity is exercisable rather than argued.
4. **Nothing in the corpus fixes a terminal-bonus level, for any insurer, in any year** (gap 1). 0.40 %
   p.a. on the *Deckungskapital* is sized so the terminal share is a visible but clearly secondary part
   of the maturity benefit; the base run pays it at the *Ablauf* and on death and **not** on surrender,
   which is the choice that does not invent an entitlement the sources do not describe (`product-spec.md`,
   footnote 12).
5. Setting `ans_rate = decl_rate` is a market convention rather than a sourced fact. It matters for one
   reason and the notes state it: because `ans_rate > rechnungszins`, **the *verzinsliche Ansammlung*
   out-accumulates the *Bonussystem* at maturity while the *Bonussystem* pays more on an early death**
   — exactly the asymmetry [R28] records, and the discriminating test between the two systems
   (pitfall 15). Setting `ans_rate = rechnungszins` would destroy it.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German insurer publishes a mortality basis, an expense
loading, a commission scale or a lapse rate for this product, and the DAV tables are not public.

**Mortality — two bases, one table.** The first-order basis is the shipped `mort_table.csv`, a
**[std] Makeham-form proxy**, sex-specific, for ages 0 to 120:

```
mort_rate_1st(M, x) = 0.00022 + B · 1.10^x          with B fixed by the anchor below
mort_rate_1st(F, x) = 0.00016 + B · 1.10^(x − 3)     a three-year setback on the same curve
```

**The anchor is `mort_rate_1st(M, 37) = 0.001200` exactly**, which fixes `B` and is what makes the
worked example reproduce; the `Data` docstring states it. The best-estimate basis is the same table
scaled: `mort_rate(t) = mort_rate_base(t) × mort_be_factor` with **`mort_be_factor = 0.75` [std]**,
so the first-order table carries a 33 % safety loading over the best estimate. That wedge is the
***Sicherheitszuschlag*** and its systematic release **is** the *Risikoüberschuss* [REG-R47] — the
model does not compute the surplus from it, but the two must not be confused, and using one basis
where the other belongs is pitfall 14.

The table this proxy stands in for is **DAV 2008 T**, the market-standard first-order basis for German
death-benefit business, derived over 2006–2008 from German insurers' own policy data, the cleansed
insured data covering **60 % of the German market in the *Kapitallebensversicherung* segment** [R14].
**It is the property of the Deutsche Aktuarvereinigung, is not public and is not redistributed here**
[R14] [REG-R47] [REG-R48]. A replacement must preserve four things: an **insured-lives**, not
population, level, materially lighter than Destatis at the working ages [REG-R52]; **sex-specific**
base tables, which are the raw material even though a tariff may not price on sex [REG-R34]; **no
projected improvement**, because for a death cover improvement favours the insurer and a prudent
first-order basis does not project it [REG-R48]; and an explicit *Sicherheitszuschlag* whose direction
is *upward* for the death leg. **The proxy carries no selection factors**, which DAV 2008 T is
understood to have [REG-R48]; a book of newly underwritten lives will therefore show more early deaths
in this model than a real one, and that is stated rather than corrected by a second unsourced factor.
And DAV 2008 T R / NR are **not suitable for business written without a *Gesundheitsprüfung*** [R14],
so the whole basis presupposes the underwriting the composite specifies.

**One table for two legs — and why that is a compromise.** This is an endowment: the death leg wants
a prudent basis with mortality *higher* than expected, and the survival leg wants one with mortality
*lower*. The direction of prudence forks, and a single first-order table cannot be prudent for both
[REG-R47] [REG-R48]. German practice resolves it in the tariff rather than in the table, and the model
follows: one first-order table, applied to both legs, with the compromise named here and asserted as
pitfall 13 rather than papered over. A user pricing the survival leg seriously needs the second table.

**Lapse [std].** The decrement is **surrender only**. `lapse_table.csv`:

| Policy year | 1–2 | 3–8 | 9–11 | 12 | 13+ | final year |
|---|---|---|---|---|---|---|
| `lapse_rate` | 5.0% | 3.5% | 2.0% | 6.0% | 2.5% | **0** |

The **shape** is the one thing the evidence supports: the half-income tax rule needs twelve years and
age 60 or 62 [R10] [REG-R45], so surrenders are suppressed approaching duration 12 and spike at it,
exactly as the eight-year threshold drives French *assurance vie* [REG-R45]. **The levels are not
sourced.** The only German lapse data are market aggregates — 2,72 % on the GDV headline measure for
2024 and 1,2 % on its head-count measure, irreconcilable and neither endowment-specific nor by
duration [R20] — and **the headline measure counts conversions to *beitragsfrei* as well as
surrenders** [R20], so calibrating a surrender decrement to it double-counts (pitfall 10). In the
**final policy year the rate is zero**: the end of policy year `n` is the *Ablauf*, so the survivors
leave as a maturity rather than as a surrender. No cash flow moves either way — a year-`n` surrender
would pay the § 169 value while a maturity pays the sum insured plus surplus, and those are **not**
the same — so unlike frlib's term product this convention is not merely a bookkeeping split; it
decides a real payment. That is why it is stated as an assumption and asserted as pitfall 18.

**Expenses, commission and the tariff loadings, side by side.** `cost_table.csv` carries both, on one
row per `cost_id`, because the difference between them **is** the *Kostenüberschuss*:

| Input | Basis `std_2026` | Class | Tag |
|---|---|---|---|
| `alpha_rate` | 25 ‰ of the *Beitragssumme*, zillmered | first order | ceiling [R7] [REG-R16]; level **[std]** |
| `beta_rate` | 3.0% of the *Bruttobeitrag*, over the *Beitragszahlungsdauer* | first order | form [R28]; level **[std]** |
| `gamma_rate` | 1.5 ‰ of the *Versicherungssumme* p.a., over the *Versicherungsdauer* | first order | form **not established**, gap 17; **[std]** |
| `acq_expense` | 300 EUR per policy at issue | second order | **[std]** |
| `comm_init_rate` | 2.5% of the *Beitragssumme* at conclusion | second order | anchored to the 25 ‰ ceiling and Die Stuttgarter's reported 25 ‰ [R7] [R29]; **[std]** |
| `comm_renew_rate` | 1.5% of the *Bruttobeitrag* from year 2 (*Bestandsprovision*) | second order | mechanism [R29]; level **[std]** |
| `maint_expense` | 45 EUR per in-force policy p.a. | second order | **[std]** |
| `expense_infl` | 1.8% p.a. | second order | **[std]** |
| `claim_expense` | 120 EUR per death, maturity or surrender claim | second order | **[std]** |

**No charge level of any kind was established for any German carrier** (gap 7). The levels are
round-number placeholders sized so the first-year acquisition outgo — 300 EUR plus 2,5 % of the
*Beitragssumme* — modestly exceeds what the *Zillmerung* recovers, so the anchor cell carries the
new-business strain a real German endowment carries. **The *Effektivkosten* these produce is a
validation target, not an input**: reproducing one exactly needs the PRIIPs Annex VI algorithm and a
specified holding period, neither of which delib implements [R9] [R19] [REG-R31] [REG-R32].

**Suicide share `suicide_share` = 0.02 [std].** § 161 VVG substitutes the *Rückkaufswert* for the sum
insured on the suicide sub-cause of death in the first three policy years [R4] [REG-R26]. No source
gives a suicide share of deaths at any age, so 2 % is a pure placeholder standing for "about one death
in fifty in the window is an excluded suicide". Setting it to zero is a defensible variant; **paying
nil instead of the *Rückkaufswert* is not** (pitfall 7).

**Bewertungsreserven, and dynamic behaviour.** Both off. The *Bewertungsreserven* share is zero and
the reason is in `product-spec.md`, footnote 13. There is no dynamic lapse formula in the base run;
the optional module is below.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t`, `k` | — | policy year, `t = t_start … n`; completed years `k = t − 1` |
| `n`, `m` | `policy_term`, `prem_term` | *Versicherungsdauer*; *Beitragszahlungsdauer* |
| `x(t)` | `age(t)` | attained age at the start of year `t` = `issue_age + t − 1` |
| `SE`, `SD` | `sum_assured`, `sum_death` | guaranteed survival sum; guaranteed death sum `= SE × death_ratio` |
| `i₁`, `v₁` | `rechnungszins` | first-order interest rate; `v₁ = 1/(1 + i₁)` |
| `q₁(t)`, `q(t)` | `mort_rate_base(t)`, `mort_rate(t)` | first-order and best-estimate annual mortality; `q = q₁ × mort_be_factor` |
| `w(t)`, `σ(t)` | `lapse_rate(t)`, `storno_rate(t)` | annual surrender rate; *Stornoabzug* rate at duration `k` |
| `l(t)` | `pols_if(t)` | policies in force at the **start** of year `t` |
| `α`, `β`, `γ` | `alpha_rate`, `beta_rate`, `gamma_rate` | *Zillmersatz*; premium loading; sum-insured loading |
| `φ` | `prem_freq_load` | *Ratenzahlungszuschlag*, 1.000 where `unterjaehrig_form = echt` |
| `B`, `BS` | `prem_gross_pp`, `beitragssumme` | annual *Bruttobeitrag* before `φ`; *Beitragssumme* `= B × m` |
| `A` | `alpha_cost` | zillmered acquisition cost `= zillmer_on × α × BS` |
| `P^n`, `P^Z` | `prem_net_level_pp`, `prem_zill_pp` | net level premium; Zillmer premium |
| `V(t)`, `V^n`, `V^Z`, `V^min` | `res_pp(t)`, `res_net_pp`, `res_zill_pp`, `res_min_pp` | *Deckungskapital* at the start of year `t`, and its three constructions |
| `G(t)` | `res_guar_pp(t)` | the § 169 guaranteed value at the **end** of year `t` |
| `RK(t)` | `surr_value_pp(t)` | *Rückkaufswert* actually payable at the end of year `t` |
| `U(t)`, `Z(t)`, `S(t)` | `av_pp(t)`, `bonus_si_pp(t)`, `term_bonus_pp(t)` | *Überschussguthaben*; bonus sum insured; accrued *Schlussüberschussanteil* |
| `d(t)`, `z(t)`, `a(t)`, `s(t)` | `decl_rate`, `zins_ueberschuss_rate`, `ans_rate`, `term_rate` | declared rate; interest-surplus rate; *Ansammlungszinssatz*; terminal rate |
| `C(t)` | `surplus_credit_pp(t)` | surplus allocated to the contract for year `t` |

`q₁`, `q`, `w`, `σ`, `d`, `z`, `a`, `s` are dimensionless annual rates; `SE`, `SD`, `B`, `V`, `U`, `Z`,
`S` are EUR per policy; every cash-flow component is EUR per policy year.

### The first-order basis and the pricing equivalence

First-order survival from issue and the two annuities-due, computed by summation on the model point's
own `sex` and `rechnungszins`:

```
tpx_1st(k)        = Π_{j=0}^{k-1} ( 1 − q₁(x_0 + j) ),  tpx_1st(0) = 1
pv_death_1st      = SD · Σ_{k=0}^{n-1} v₁^(k+1) · tpx_1st(k) · q₁(x_0 + k)
pv_maturity_1st   = SE · v₁^n · tpx_1st(n)
pv_benefit_1st    = pv_death_1st + pv_maturity_1st
ann_due_prem_1st  = Σ_{k=0}^{m-1} v₁^k · tpx_1st(k)
ann_due_term_1st  = Σ_{k=0}^{n-1} v₁^k · tpx_1st(k)
```

The *Bruttobeitrag* is struck by equivalence, which is linear in `B` because `BS = B · m`:

```
B · ann_due_prem_1st = pv_benefit_1st + α · B · m
                       + β · B · ann_due_prem_1st + γ · SE · ann_due_term_1st

⇒  prem_gross_pp = ( pv_benefit_1st + γ · SE · ann_due_term_1st )
                   / ( (1 − β) · ann_due_prem_1st − α · m )
```

`check_equivalence()` asserts that identity closes. **Note that the acquisition cost `α · BS` is in
the premium whether or not the contract is zillmered**: *Zillmerung* decides where the cost sits in the
**reserve**, not whether it is charged (`zillmer_on` enters `alpha_cost`, not the pricing equation).
That is why die Bayerische can publish two editions of one tariff [S9] and why the two editions do not
differ in price. The risk element carries the *Risikozuschlag*: `rating_factor` multiplies `q₁` in the
**death** leg of `pv_death_1st` only, never the survival leg, never the benefit, and never a
best-estimate rate (pitfall 12).

Then the two reserving premiums, and the zillmered cost:

```
beitragssumme     = prem_gross_pp · m
alpha_cost        = zillmer_on · alpha_rate · beitragssumme
prem_net_level_pp = pv_benefit_1st / ann_due_prem_1st
prem_zill_pp      = prem_net_level_pp + alpha_cost / ann_due_prem_1st
```

**Single premium.** `prem_term = 1` gives `ann_due_prem_1st = 1`, `BS = B`, and a *Beitragssumme*
equal to the single premium — so the 25 ‰ *Zillmersatz* buys almost nothing and the § 169 floor is
slack from the first anniversary. That is the correct answer, not a degenerate case.

### The Deckungskapital

Prospectively, at the start of year `t` (duration `k = t − 1`), on the first-order basis, over the
remaining term and the remaining premium period:

```
pv_benefit_fut(t)    = SD · Σ_{j=0}^{n-k-1} v₁^(j+1) · jp(x(t)) · q₁(x(t)+j)  +  SE · v₁^(n-k) · (n-k)p(x(t))
ann_due_prem_fut(t)  = Σ_{j=0}^{max(0, m-k)-1} v₁^j · jp(x(t))

res_net_pp(t)   = pv_benefit_fut(t) − prem_net_level_pp · ann_due_prem_fut(t)
res_zill_pp(t)  = res_net_pp(t) − alpha_cost · ann_due_prem_fut(t) / ann_due_prem_1st
res_min_pp(t)   = res_net_pp(t) − alpha_cost · max(0, 1 − (t − 1) / 5)
res_pp(t)       = res_zill_pp(t)                       while premium-paying
                = bfz_si_pp · pu_single_prem(t)        once paid-up
```

Three facts about those three lines. **`res_zill_pp(1) = −alpha_cost`** exactly: the *gezillmerte
Deckungskapital* is **negative at issue** and stays negative for several years, which is the
arithmetic of [R28] and the reason § 169 Abs. 3 needs a floor at all. **`res_min_pp` is the § 169
Abs. 3 floor** and it is the straight-line reading of the five-year spreading. And **the floor
normally binds**: `ann_due_prem_fut(t)/ann_due_prem_1st` falls roughly linearly over `m` years while
`max(0, 1 − k/5)` reaches zero after five, so `res_min_pp(t) ≥ res_zill_pp(t)` at every duration on a
long *gezillmert* contract, with equality only at duration 0 and at duration `m`. **A model that
publishes only the Zillmer reserve as the surrender value understates it at essentially every
duration, and one that publishes only the floor loses the quantity the *Deckungsrückstellung* and the
paid-up sum are built on** (pitfall 4). With `zillmer_on = 0` all three coincide and the floor is
slack, which is a useful invariance test.

### Rückkaufswert, Beitragsfreistellung and the paid-up sum

`G(t)` is struck at the **end** of policy year `t`, i.e. on the reserve at the start of year `t + 1`,
because that is what "zum Schluss der laufenden Versicherungsperiode" requires [R2]:

```
res_guar_pp(t)     = max( res_zill_pp(t+1), res_min_pp(t+1), 0 )
surr_value_pp(t)   = res_guar_pp(t) · (1 − storno_rate(t))
                     + av_pp_at(t, "AFT_CREDIT")
                     + term_surr_share · term_bonus_pp(t+1)
pu_single_prem(t)  = SD/SE · Σ_{j} v₁^(j+1) · jp(x(t)) · q₁(x(t)+j)  +  v₁^(n-k) · (n-k)p(x(t))
bfz_si_pp          = res_guar_pp(bfz_year) / pu_single_prem(bfz_year + 1)
```

`pu_single_prem(t)` is the first-order single premium for **one unit** of paid-up endowment over the
remaining term, so `bfz_si_pp` is the *beitragsfreie Versicherungssumme* the § 169 value will buy —
which is exactly what § 165 prescribes, "auf der Grundlage des Rückkaufswertes nach § 169 Abs. 3 bis
5" [R3]. Three rules ride on those four lines:

- **The *Stornoabzug* bites on the guaranteed value only**, not on the *Überschussguthaben*: Debeka's
  published deduction is a percentage of the *Deckungskapital* [S3] [R30] (pitfall 6).
- **`term_surr_share = 0` in the base run [std]**, so the accrued *Schlussüberschussanteil* is paid at
  the *Ablauf* and on death and not on surrender (`product-spec.md`, footnote 12). The parameter is
  exposed.
- **The *Mindestversicherungsleistung* test**: if `bfz_si_pp < bfz_min_si` (**2,500 EUR [std]**) the
  election is **not** a *Beitragsfreistellung*. § 165 VVG then obliges the insurer to pay the § 169
  value instead, so the model converts the whole model point to a **surrender at the end of
  `bfz_year`** and the projection terminates there [R3] (pitfall 8). Model point 12 exercises exactly
  this branch.

Where the election succeeds the contract stays in force with `bfz_si_pp` in place of `SE`, no further
premium, and a reserve `bfz_si_pp · pu_single_prem(t)`. Because the § 169 floor generally exceeds the
Zillmer reserve, the paid-up sum bought is worth more than the Zillmer reserve released; the
difference is published as `bfz_uplift_pp` and enters the roll-forward identity so that
`check_res_roll_fwd()` still closes in the election year.

### The Überschussbeteiligung

Declared annually, as a percentage of the *Deckungskapital* at the allocation date [S3], allocated at
the period end [S9]:

```
zins_ueberschuss_rate(t) = max( 0, decl_rate(t) − rechnungszins )
surplus_base_pp(t)       = max( res_pp_at(t, "AFT_INT"), 0 )
surplus_credit_pp(t)     = zins_ueberschuss_rate(t) · surplus_base_pp(t)
term_bonus_pp(t+1)       = term_bonus_pp(t) + term_rate(t) · surplus_base_pp(t)
```

`res_pp_at(t, "AFT_INT")` is the closing guaranteed reserve of policy year `t`, before this year's
surplus is applied — the *Deckungskapital* "calculated at the allocation date" [S3]. **The `max(0, ·)`
on the base is load-bearing**: the *gezillmerte Deckungskapital* is negative in the early years, and a
positive rate on a negative base would credit a negative surplus (pitfall 3). It follows that a
*gezillmert* contract earns **no** interest surplus in its first years even though § 153 entitlement
runs from inception [S9] — which is economically right, because there is no fund to earn on, and is
worth saying out loud because it looks like a bug. **The `max(0, ·)` on the rate** is the other half:
in the `nil` scenario the declared rate is below the guarantee, and the guarantee is still met in full
by the reserve roll-forward — the surplus is zero, not negative (pitfall 1).

Then the three *Überschussverwendung* systems:

```
ansammlung:           av_pp(t+1)      = av_pp(t) · (1 + ans_rate(t)) + surplus_credit_pp(t)
bonus:                bonus_si_pp(t+1)= bonus_si_pp(t) + surplus_credit_pp(t) / pu_single_prem(t+1)
beitragsverrechnung:  prem_offset_pp(t) = min( prem_charged_pp(t), surplus_credit_pp(t-1) )
```

Under `ansammlung` the surplus compounds at `ans_rate` and raises the maturity benefit; under `bonus`
it buys paid-up insurance at first-order rates, which raises the **death** benefit immediately by the
full bonus sum but accumulates only at `rechnungszins`; under `beitragsverrechnung` it reduces the
*Zahlbeitrag* and neither balance grows. Because `ans_rate > rechnungszins`, the first gives a higher
maturity benefit and the second a higher death benefit — **exactly the asymmetry [R28] states**, and
the test that distinguishes them (pitfall 15).

### Premium, decrements, benefits and cash flows

```
prem_charged_pp(t) = prem_gross_pp · prem_freq_load        if t ≤ prem_term and not is_paid_up(t)
                   = 0                                      otherwise
prem_paid_pp(t)    = prem_charged_pp(t) − prem_offset_pp(t)
premiums(t)        = prem_paid_pp(t) · pols_if(t)

pols_death(t)      = pols_if(t) · mort_rate(t)
pols_lapse(t)      = pols_if(t) · (1 − mort_rate(t)) · lapse_rate(t)
pols_maturity(t)   = pols_if(t) · (1 − mort_rate(t))        at t = n, else 0
pols_if(t+1)       = pols_if(t) − pols_death(t) − pols_lapse(t)

benefit_full_pp(t)     = sum_death + av_pp(t+1) + bonus_si_pp(t+1) + term_bonus_pp(t+1)
benefit_death_pp(t)    = (1 − suicide_share) · benefit_full_pp(t) + suicide_share · surr_value_pp(t)
                                                            for t ≤ 3, else benefit_full_pp(t)
benefit_maturity_pp(n) = sum_assured + av_pp(n+1) + bonus_si_pp(n+1) + term_bonus_pp(n+1)
                         + bwr_rate · res_guar_pp(n)

claims(t, "DEATH")    = pols_death(t)    · benefit_death_pp(t)
claims(t, "MATURITY") = pols_maturity(t) · benefit_maturity_pp(t)
claims(t, "LAPSE")    = pols_lapse(t)    · surr_value_pp(t)

expenses(t)    = acq_expense · 1{t = t_start and duration_init = 0}
                 + maint_expense · inflation_factor(t) · pols_if(t)
                 + claim_expense · ( pols_death(t) + pols_lapse(t) + pols_maturity(t) )
commissions(t) = comm_init_rate · beitragssumme · 1{t = t_start and duration_init = 0}
                 + comm_renew_rate · prem_charged_pp(t) · pols_if(t)   for t > t_start
net_cf(t)      = premiums(t) − claims(t,"DEATH") − claims(t,"MATURITY") − claims(t,"LAPSE")
                 − expenses(t) − commissions(t)
liability_cf(t)= − net_cf(t)
```

Two orientations worth naming. **`sum_death` is `sum_assured × death_ratio`, and the surplus is added
to it whole**: the *Überschussguthaben*, the bonus sum and the accrued terminal bonus are payable on
death as well as at maturity [S11] [S16], so the two benefits differ only in their guaranteed leg.
**The renewal commission is charged on `prem_charged_pp`, not `prem_paid_pp`**: under
*Beitragsverrechnung* the intermediary is paid on the tariff premium, and the surplus offset is a
policyholder rebate, not a smaller sale.

`result_cf()` is a `DataFrame` indexed by `t` (`df.index.name == "t"`), contiguous from `t_start()` to
`proj_len()`, with columns **in this order**:

```
pols_if, premiums, claims_death, claims_maturity, claims_lapse, expenses, commissions, net_cf
```

Every column but `pols_if` is a euro flow and the six flows sum to `net_cf` exactly, which is what
`check_net_cf()` asserts. Note the deliberate difference from frlib, where commission sits **inside**
`expenses` and is also published beside it: here `expenses` **excludes** commission, so a reader
summing the columns gets `net_cf` rather than a double count. `result_surplus()` is a second frame
reporting the surplus machinery — `decl_rate`, `zins_ueberschuss_rate`, `surplus_base_pp`,
`surplus_credit_pp`, `res_pp`, `av_pp`, `term_bonus_pp`, `surr_value_pp` — which are state, not cash
flow, and are therefore kept out of `result_cf()`.

### Published identities

Nine `check_*()` cells, each taking no argument and returning a `bool` over all `t`, each with a
per-`t` residual at `check_*_resid(t)`. The conventions suite calls every one of them on every model
point and requires `True`.

| Identity | What it asserts |
|---|---|
| `check_net_cf()` | **delib's first ruling.** `net_cf(t)` equals `premiums − claims_death − claims_maturity − claims_lapse − expenses − commissions`, rebuilt from `result_cf()`'s own published columns |
| `check_pols_roll_fwd()` | `pols_if(t+1) == pols_if(t) − pols_death(t) − pols_lapse(t)`, and at `t = n` the survivors of mortality are exactly `pols_maturity(n)` |
| `check_decrement_closure()` | `Σ_t ( pols_death + pols_lapse + pols_maturity ) == pols_if_init()` |
| `check_res_roll_fwd()` | The Fackler recursion on the guaranteed *Deckungskapital*: `( res_pp(t) + prem_zill_charged(t) ) · (1 + i₁) + bfz_uplift_pp(t) == q₁(t) · sum_death + (1 − q₁(t)) · res_pp(t+1)`. This is the strongest single check in the model: it proves the premium, the first-order mortality, the interest and the prospective formula are mutually consistent |
| `check_surplus_roll_fwd()` | The active surplus vehicle's ledger closes: `av_pp(t+1) == av_pp(t)·(1 + a(t)) + C(t)` under `ansammlung`, the bonus-purchase identity under `bonus`, and `prem_offset_pp(t) == min(prem_charged_pp(t), C(t−1))` under `beitragsverrechnung` |
| `check_surr_floor()` | § 169 Abs. 3: `res_guar_pp(t) ≥ res_zill_pp(t+1)`, `≥ res_min_pp(t+1)` and `≥ 0` at every `t`, and `surr_value_pp(t) ≥ 0` |
| `check_equivalence()` | The first-order pricing equivalence closes: `B·(1 − β)·ann_due_prem_1st − α·BS == pv_benefit_1st + γ·SE·ann_due_term_1st` |
| `check_rechnungszins_cap()` | § 2 DeckRV: `rechnungszins ≤ hoechstrechnungszins(issue_year)` [REG-R14] [REG-R15] |
| `check_zillmer_cap()` | § 4 DeckRV: `alpha_rate ≤ hoechstzillmersatz(issue_year)`, and `alpha_cost ≤ hoechstzillmersatz · beitragssumme` [R7] [REG-R16] |

The last two are parameter invariants rather than roll-forward identities, and they are here rather
than in a build script because a German model point's cohort **is** an assumption: a 4,00 % guarantee
on a 2026 issue year is not a stress, it is a data error.

### Annual processing order

For `t = t_start() … proj_len()`, in this order:

1. **Open the year.** `x(t) = issue_age + t − 1`, `k = t − 1`; carry in `pols_if(t)`, `res_pp(t)`,
   `av_pp(t)`, `bonus_si_pp(t)`, `term_bonus_pp(t)`, `is_paid_up(t)`.
2. **Decide whether a premium is due**: `t ≤ prem_term` **and** not `is_paid_up(t)`. Apply `φ` only
   where `unterjaehrig_form = unecht`.
3. **Apply the *Beitragsverrechnung* offset**, where elected: last year's declared surplus reduces this
   year's *Zahlbeitrag*, floored at zero.
4. **Collect the premium in advance**: `premiums(t) = prem_paid_pp(t) × pols_if(t)`. A life that dies
   or surrenders later in the year **has already paid** this year's premium; do not net it again
   (pitfall 12 of the frlib chassis, pitfall 11 here).
5. **Charge start-of-year expenses and commission** on the in-force; the acquisition expense and
   initial commission fall at `t = t_start()` and only for a new-business point.
6. **Roll the guaranteed *Deckungskapital* forward** one year on the first-order basis — interest at
   `rechnungszins`, mortality release at `mort_rate_base` — to `res_pp_at(t, "AFT_INT")`, the closing
   guaranteed reserve. This is the **allocation-date** *Deckungskapital*.
7. **Declare and credit the surplus**: `z(t) = max(0, d(t) − i₁)`, base
   `max(res_pp_at(t, "AFT_INT"), 0)`, credit `C(t)`, and accrue `term_rate(t)` on the same base.
8. **Apply the surplus** per `surplus_use` — accumulate it, buy bonus sum insured, or carry it forward
   as next year's premium offset.
9. **End of year, deaths** at the **best-estimate** `mort_rate(t)`: the benefit is the guaranteed death
   sum plus the *Überschussguthaben*, the bonus sum and the accrued terminal bonus, with the § 161
   substitution of the *Rückkaufswert* on the suicide share for `t ≤ 3`.
10. **End of year, maturity or surrender.** At `t = n` the survivors of mortality mature and take the
    *Erlebensfallleistung*; the projection stops. Otherwise `lapse_rate(t)` applies to the survivors of
    mortality and pays `surr_value_pp(t)`.
11. **The *Beitragsfreistellung* election**, where `t = bfz_year`: strike `res_guar_pp(t)`, buy
    `bfz_si_pp`, and test it against `bfz_min_si` — **below the minimum the election becomes a
    surrender** and the projection terminates as at step 10.
12. **Roll forward** `pols_if(t+1)`, `res_pp(t+1)`, `av_pp(t+1)`, `bonus_si_pp(t+1)`,
    `term_bonus_pp(t+1)`, `is_paid_up(t+1)`.

The order of steps 6, 7 and 9 is the one thing a reader should check first. The surplus is declared on
the reserve **after** the year's interest and **before** the decrements, so a policy that dies at the
end of year `t` receives year `t`'s declared surplus. That follows the sources — the allocation is
made at the *Bilanzstichtag* to the contracts then in force [S9] — and it is the generous reading; the
alternative, allocating after the decrements, would deny the year's surplus to a decedent.

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one is
a test in `tests/test_kapitallebensversicherung_de.py`.

1. **Adding the declared rate on top of the guarantee.** The ***laufende Verzinsung*** **is** the
   *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53], so a declared 2,70 %
   on a 1,00 % guarantee is a **1,70 pp** surplus credit and not 2,70 pp on top of 1,00 pp. Assert
   `zins_ueberschuss_rate(t) == max(0, decl_rate(t) − rechnungszins)` at every `t`, and that on the
   `nil` scenario it is exactly 0 while the reserve still rolls forward at the full `rechnungszins`.
2. **Applying the surplus rate to the sum insured or to the premium.** The base is the
   ***Deckungskapital* at the allocation date** [S3]. Assert
   `surplus_credit_pp(t) == zins_ueberschuss_rate(t) · max(res_pp_at(t, "AFT_INT"), 0)` and that
   `surplus_credit_pp` is invariant to `sum_assured` **once the reserve is held fixed** — the quickest
   way to catch a `× sum_assured` where a `× res_pp` belongs.
3. **Crediting surplus on an un-floored negative reserve.** The *gezillmerte Deckungskapital* is
   negative in the early years [R28]. Assert `surplus_base_pp(t) ≥ 0` at every `t`, and specifically
   that `surplus_credit_pp(t) == 0` for every `t` in which `res_pp_at(t, "AFT_INT") < 0` on the anchor
   cell. **Entitlement from inception [S9] does not mean a positive credit from inception.**
4. **Implementing one reserve where the product has three.** `res_zill_pp` is what the insurer
   reserves; `res_min_pp` is the § 169 Abs. 3 floor and it **normally binds**; `res_guar_pp` is their
   maximum and is what the customer gets. Assert `res_guar_pp(t) ≥ res_zill_pp(t+1)` and
   `≥ res_min_pp(t+1)` at every `t`, that the floor is **strictly** binding at some duration on the
   anchor cell, and that on model point 13 (`zillmer_on = 0`) all three coincide.
5. **Conflating the § 169 five-year spreading with the § 4 DeckRV 25 ‰ cap.** They are different rules
   with different functions: § 169 Abs. 3 VVG fixes **how** the acquisition cost is spread for the
   surrender floor — a floor on the **value** — while § 4 DeckRV fixes **how much** may be zillmered at
   all — a cap on the **charge** [R2] [R7] [REG-R16] [REG-R28] (gap 5). Assert `check_zillmer_cap()`
   against the cohort ceiling **and** `check_surr_floor()` against the five-year schedule, separately,
   and that the five-year schedule is *not* a function of `alpha_rate`'s ceiling.
6. **Deducting the *Stornoabzug* from the *Überschussguthaben*.** Debeka's published deduction is a
   percentage of the *Deckungskapital* [S3] [R30]. Assert
   `surr_value_pp(t) − av_pp_at(t, "AFT_CREDIT") == res_guar_pp(t) · (1 − storno_rate(t))` at every `t`
   in the base run, so the accumulated surplus passes through undeducted.
7. **Paying nil on a suicide inside the three-year window.** § 161 VVG makes the insurer
   *leistungsfrei* **and** obliges it to pay the *Rückkaufswert* including *Überschussanteile* under
   § 169 [R4] [REG-R26]: the German rule is a **benefit substitution**, not a forfeiture, unlike art.
   L. 132-7 of the French code. Assert
   `benefit_death_pp(t) == 0.98 · benefit_full_pp(t) + 0.02 · surr_value_pp(t)` for `t ≤ 3` and
   `== benefit_full_pp(t)` for `t ≥ 4`, and that `benefit_death_pp(1) > 0` even where `surr_value_pp(1)`
   is nil.
8. **Offering *Beitragsfreistellung* without the *Mindestversicherungsleistung* test.** § 165 VVG makes
   the election a **surrender** where the minimum is not reached [R3]. Assert that model point 11
   (`bfz_year = 10`) continues in force to `proj_len()` with `prem_paid_pp(t) == 0` from `t = 11`, and
   that model point 12 (`bfz_year = 3`, small sum) instead **terminates** at `t = 3` with a
   `claims_lapse` payment and nothing thereafter.
9. **Removing the paid-up policy from `pols_if`.** *Beitragsfreistellung* keeps the contract alive with
   a reduced sum insured [R3] [S7]; only a *Kündigung* removes it. Assert `pols_if(t)` is unaffected by
   `bfz_year` on model point 11 relative to the anchor, while `prem_paid_pp` and
   `benefit_maturity_pp` both fall.
10. **Calibrating the surrender decrement to GDV's headline *Stornoquote*.** The 2,72 % measure counts
    contracts terminated early, surrendered **or converted to *beitragsfrei*** as a share of the
    *Bestand*; a second GDV measure by contract count gives 1,2 % for the same year and the two are
    irreconcilable from the search evidence [R20]. Neither is a surrender rate and neither is
    endowment-specific or by duration. Assert that `lapse_rate` comes from `lapse_table.csv` and that
    the table's provenance column says [std], not [R20].
11. **Double-counting the premium-cessation rule.** Premiums are in advance and decrements are at the
    period end, so a decedent has already paid the year's premium [S7]. Assert
    `premiums(t) == prem_paid_pp(t) · pols_if(t)` with **no** `(1 − q)` factor; multiplying by it again
    understates premium income by about one year's mortality.
12. **Letting the *Risikozuschlag* reach the wrong quantity.** `rating_factor` scales the first-order
    mortality in the **death** leg of the pricing only [R5]. Assert that `benefit_death_pp` is invariant
    to `rating_factor`, that `mort_rate(t)` (the best estimate) is invariant to it, and that
    `prem_gross_pp` rises with it.
13. **Using one mortality table as if it were prudent for both legs.** The direction of prudence forks:
    a death benefit wants mortality assumed **higher** than expected, a survival benefit **lower**
    [REG-R47] [REG-R48]. The model uses one first-order table for both and says so; assert that the
    single table is in fact used for both legs and that the notes' compromise is not silently replaced
    by two tables without a second source.
14. **Crossing the first- and second-order bases.** `mort_rate_base` prices and reserves;
    `mort_rate` projects. Assert `mort_rate(t) == mort_rate_base(t) · mort_be_factor` with
    `mort_be_factor = 0.75`, that `res_pp` is invariant to `mort_be_factor`, and that `pols_death`
    moves with it. A model that reserves on the best estimate has thrown away the *Sicherheitszuschlag*
    that is the source of the *Risikoüberschuss* [REG-R47].
15. **Expecting the two surplus systems to give the same benefits.** "Compared with the *Bonussystem*,
    the *verzinsliche Ansammlung* leads to a higher payment at maturity, while the *Bonussystem*
    produces higher death benefits" [R28]. Assert exactly that between model point 1 (`ansammlung`) and
    model point 8 (`bonus`): higher `claims_maturity` on 1, higher `benefit_death_pp(t)` on 8 at every
    `t` after the first credit. It holds because `ans_rate > rechnungszins`, and a model that sets them
    equal will fail it — correctly.
16. **Treating the *Zahlbeitrag* as guaranteed.** Under *Beitragsverrechnung* the policyholder pays the
    *Bruttobeitrag* less a **discretionary** surplus offset, withdrawable without invoking § 163 VVG at
    all [REG-R27] [REG-R53]. Assert on model point 9 that `prem_paid_pp(t) < prem_charged_pp(t)` while
    surplus is being declared, that `prem_charged_pp(t)` is unchanged from the anchor, and that on the
    `nil` scenario the offset is zero and the two coincide.
17. **Letting `sex` into the premium.** Unisex since 21 December 2012 [REG-R34]. Assert that
    `prem_gross_pp` is identical for two otherwise-identical model points differing only in `sex`, while
    `mort_rate` differs. The pricing basis is a fixed portfolio blend and that blend is **[std]**.
18. **Running past the *Ablauf*, or letting a final-year surrender collide with the maturity.**
    `proj_len() = policy_term` and there is no `t = proj_len() + 1` row. `lapse_rate(n) = 0` **[std]**,
    so the survivors of mortality in year `n` all leave as a maturity. Unlike a term product, the two
    exits do **not** pay the same thing — a surrender pays the § 169 value, a maturity pays the sum
    insured plus surplus — so this is a real payment decision, not a bookkeeping split. Assert
    `lapse_rate(proj_len()) == 0`, `pols_maturity(n) == pols_if(n) · (1 − mort_rate(n))`, and that the
    decrement closure `Σ(pols_death + pols_lapse + pols_maturity) == pols_if_init()` holds to 1e-12.

---

## Policyholder behaviour modelling

All formulas are **[std]**; no German calibration evidence exists for any of them.

- **Base surrender.** The duration table above, with the shape driven by the tax thresholds — twelve
  years and age 60 or 62 [R10] [REG-R45] — and the levels unsourced. The anchor cell's *Ablauf* at
  attained age 62 makes the two thresholds coincide, which is exactly why a German buyer is sold that
  term and exactly why the surrender rate collapses in the run-up to it.
- **The *Beitragsfreistellung* election is deterministic** — a model-point column, not a decrement.
  The corpus establishes the right in full [R3] and gives **no take-up rate at all**, and the one
  aggregate that would bear on it mixes the paid-up route in with surrenders and cannot be split [R20].
  Modelling it as a scheduled election keeps the unsourced number out of the base run; what that costs
  is stated — a real book converts a material, duration-dependent share to *beitragsfrei*, and this
  model shows that path only where a model point elects it.
- **Premium-shock lapse [std] (optional module, off in the base run).** Not applicable to the base
  contract, whose *Bruttobeitrag* is level, but live under *Beitragsverrechnung*, where a fall in the
  declared rate raises the *Zahlbeitrag*:

  ```
  M_shock(t) = 1 + β_shock · max(0, prem_paid_pp(t)/prem_paid_pp(t-1) − 1 − g0)
  ```

  with `g0 = 0.05` and `β_shock = 1.5` **[std]**; base run `β_shock = 0`.
- **Rate-gap lapse [std] (optional module, off in the base run).** German surrender behaviour on a
  savings contract keys on the gap between the declared rate and what is available elsewhere:
  `lapse_add(t) = a · max(0, ref_rate − decl_rate(t) − tol)` with `a = 3.0`, `tol = 0.5 pp` and
  `ref_rate` a model Reference **[std]**; base run `a = 0`. **No German calibration of any of these
  numbers exists in the corpus**, which is why the module ships off. **Selective lapsation is not
  modelled** either: surrenders on an endowment are wealth- and tax-driven rather than health-driven.
- **What the model deliberately does not do.** No premium-default path (§§ 37/38 VVG unresearched, gap
  20); no *Widerruf* decrement (§ 152 VVG unresearched); no dynamic *Beitragsverrechnung* take-up; and
  no management action on the declared rate — the rate is a scenario, and the RfB and its
  *Schlussüberschussanteilfonds* [REG-R54] that would smooth it are outside this model.

---

## Worked example

**Configuration.** Model point 1, the anchor cell of `model_point_table.csv`: `policy_id`
`DE-KLV-0001`; `sex` **M**; `smoker` **N**; `issue_year` **2026**; `issue_age` **37**;
`duration_init` **0**, so `t_start() = 1` and the projection opens at issue; `pols_if_init` **1.0**;
`policy_term` **25**, so `proj_len() = 25` and the table below is the **entire** projection, with the
*Ablauf* at attained age **62** — the age the half-income tax rule requires for a contract concluded
after 31 December 2011 [R10] [REG-R45]; `prem_term` **25**, the full term, so the contract is
premium-paying to the *Ablauf*; `sum_assured` **50,000.00 EUR**; `death_ratio` **1.00**, so the
guaranteed death sum equals the guaranteed survival sum and the contract is the *gemischte Versicherung
auf den Todes- und Erlebensfall* proper; `prem_freq` **annual** and `unterjaehrig_form` **unecht**, so
`prem_freq_load = 1.000` and the *Ratenzahlungszuschlag* is inert; `rechnungszins` **1.00%**, the
*Höchstrechnungszins* for new business written from 1 January 2025 [R7] [REG-R15]; `zillmer_on` **1**;
`cost_id` **`std_2026`**; `surplus_use` **`ansammlung`**; `scenario_id` **`base`**; `rating_factor`
**1.00**; `av_pp_init` **0.00**; `bonus_si_init` **0.00**; `bfz_year` **0**, so no
*Beitragsfreistellung* is elected. The *Bruttobeitrag* is **not** a model point column: it is derived
by the equivalence principle above and reported in the table, because **no German endowment premium
rate table is public, for any carrier** (gap 16).

**Assumptions, each tagged.** *First order.* Interest `i₁ = 1.00%` [R7] [R15] [REG-R14] [REG-R15].
Mortality `mort_rate_1st(M, x) = 0.00022 + B · 1.10^x`, `B` fixed by the anchor
`mort_rate_1st(M, 37) = 0.001200` exactly **[std]**, standing in for **DAV 2008 T**, which is not
public and is not shipped [R14] [REG-R47] [REG-R48]. *Zillmersatz* `alpha_rate = 25 ‰` of the
*Beitragssumme* — the § 4 DeckRV ceiling [R7] [REG-R16], the level **[std]**. Premium loading
`beta_rate = 3.0%` of the *Bruttobeitrag* over the *Beitragszahlungsdauer* — the form is the one the
corpus establishes [R28], the level **[std]**. Sum loading `gamma_rate = 1.5 ‰` of the
*Versicherungssumme* p.a. over the *Versicherungsdauer* — **the form itself is not established** (gap
17) and both form and level are **[std]**. *Ratenzahlungszuschlag* `prem_freq_load = 1.000` on the
annual mode [R28].

*Insurer-discretionary.* Declared *laufende Verzinsung* `decl_rate = 2.70%` p.a. level — Allianz's 2026
rate for its classic endowment book [S11], the only such rate in the corpus, the level-forever
assumption **[std]**; hence `zins_ueberschuss_rate = max(0, 2.70% − 1.00%) = 1.70%`, **derived and
never added on top of the guarantee** [REG-R53]. *Schlussüberschussanteilsatz* `term_rate = 0.40%` p.a.
of the *Deckungskapital*, accrued and paid at the *Ablauf* and on death, **not** on surrender
(`term_surr_share = 0`) — **[std]**, no rate of any kind having been established (gap 1).
*Ansammlungszinssatz* `ans_rate = 2.70%`, equal to the declared rate — **[std]**. *Stornoabzug*
`storno_rate` 10% of the guaranteed value in policy years 1–5, 7.5% in 6–10, 5% in 11–15 and 2.5% from
16 — **[std]**, against an observed range of 5% to 20% of the *Deckungskapital* from **one carrier**,
under collective action and a BGH remittal [S3] [R22] [R30]. *Bewertungsreserven* `bwr_rate = 0.00%` —
**[std]** [R1] [R8] [REG-R9].

*Second order.* Mortality `mort_rate(t) = mort_rate_base(t) × 0.75`, `mort_be_factor = 0.75` **[std]**
— a 33 % first-order safety loading, whose systematic release is the *Risikoüberschuss* [REG-R47].
Surrender `lapse_rate` 5.0% in policy years 1–2, 3.5% in 3–8, 2.0% in 9–11, **6.0% in year 12** — the
twelve-year tax threshold [R10] [REG-R45] — 2.5% from year 13, and **0 in year 25**, the *Ablauf*
year — all **[std]**, no endowment-specific or duration-specific German lapse rate having been
established (gap 10). Suicide share `suicide_share = 0.02` for policy years 1 to 3, with the
*Rückkaufswert* substituted for the sum insured on that share [R4] [REG-R26] — the share **[std]**.
Expenses **[std]** throughout: `acq_expense = 300.00 EUR` at issue, `comm_init_rate = 2.5%` of the
*Beitragssumme* at issue — anchored to the 25 ‰ ceiling and Die Stuttgarter's reported 25 ‰ [R7]
[R29] — `maint_expense = 45.00 EUR` per in-force policy p.a. inflating at `expense_infl = 1.8%` p.a.,
`comm_renew_rate = 1.5%` of the *Bruttobeitrag* from year 2, and `claim_expense = 120.00 EUR` per
death, maturity or surrender claim. No behaviour modules: `β_shock = 0`, `a = 0`.

All amounts in euros; `pols_if` to six decimals, cash flows and balances to the cent. Totals are summed
**at full precision and then rounded**, not summed from the rounded cells.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared grid.
The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** § 341f HGB requires it to be formed at the
  *versicherungsmathematisch berechneter Wert*, **including profit shares already allocated** but
  **excluding *verzinslich angesammelte Überschussanteile***, and after deducting the present value of
  future premiums, by the **prospective method** [REG-R54]. `res_pp(t) × pols_if(t)` is this model's
  contribution to that line and `av_pp(t) × pols_if(t)` is explicitly **not** part of it. Three things
  the model does not do: it does not floor the reserve at zero, as the balance sheet does, so the
  negative early *gezillmert* values are visible; it does not cap the *Zillmersatz* at the § 4 DeckRV
  ceiling as a reserving constraint separate from the tariff, because the shipped `alpha_rate` already
  sits at it; and it does not carry a *Verwaltungskostenrückstellung* for the period after the
  *Beitragszahlungsdauer*, where the `gamma_rate` cost runs on with no `beta_rate` income — the
  pricing equation funds it, and the classical reserve convention used here assumes the ongoing
  loadings exactly meet the ongoing costs. On a full HGB basis that provision would be separate.
- **The *Zinszusatzreserve*.** An HGB reserve arising when the § 5 Abs. 3 DeckRV *Referenzzins* falls
  below a contract's tariff rate, financed out of the result and, under § 140 VAG's second escape hatch,
  out of the free RfB [REG-R10] [REG-R17]. It exists in no other jurisdiction in this repository and
  **this model does not compute it**, but it matters here: the ZZR is how a high-guarantee cohort
  consumes the surplus that would otherwise be declared, which is why a delib path is a scenario and
  not a forecast.
- **The RfB, the *Schlussüberschussanteilfonds* and the MindZV.** The surplus this model credits is the
  **output** of the insurer's declaration policy, not the MindZV minimum, which is a transfer to the RfB
  — 90 % of the *Kapitalanlageergebnis* after deducting the *Rechnungszinsen*, 90 % of the
  *Risikoergebnis*, 50 % of the *übriges Ergebnis*, *Direktgutschrift* deducted, *Alt-* and *Neubestand*
  separate [R6] [REG-R18] — with the RfB [REG-R10], its collective part [REG-R19] and the
  *Schlussüberschussanteilfonds* of § 28 RechVersV [REG-R54] between it and the policy. **None of that
  is modelled**, and a delib document must not present the quotas as if they determined a declared rate.
- **Solvabilität II.** Technical provisions are a best estimate — the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure — plus a risk margin [REG-R1]
  [REG-R2] [REG-R6], with EIOPA publishing the curves monthly and § 83 VAG making their use binding
  [REG-R4]. `BEL = Σ_t v(t) · liability_cf(t)` over the recursion above. The **future discretionary
  benefits** — the declared *Zinsüberschuss*, the *Schlussüberschussanteil* and the *Ansammlung* — are
  the substance of the best estimate for this product, and the crediting rule above is exactly the
  management action a market-consistent valuation must model. **No cost-of-capital rate, contract
  boundary rule or standard-formula shock in this library was read from a retrieved instrument**, so
  every such figure is **[std]** [REG-R2].
- **The guarantee is an option.** A guaranteed sum insured plus a guaranteed *Rechnungszins* is a
  written put on the *Sicherungsvermögen*, and the deterministic path above prices none of it; a
  stochastic-on-deterministic run is what a time-value-of-options-and-guarantees calculation consumes.
  The outer boundary is the *Sicherungsfonds*: a fund-level 5 % haircut under § 222 VAG and an
  uncapped reduction under § 314 VAG, which also lets the supervisor **temporarily prohibit the
  *Rückkauf*** [REG-R12]. **A mass-surrender run here produces the values the contract owes, not the
  ones that would be paid if § 314 were in force.**
- **IFRS 17.** The archetypal direct-participating contract, measured under the variable fee approach;
  the fulfilment-cash-flow engine is this same projection, and grouping, CSM and risk adjustment are out
  of scope [REG-R55].

---

## Key sensitivities and model risks

In rough order of leverage on this product.

1. **The declared-rate path.** `decl_rate` sets `zins_ueberschuss_rate` one-for-one above the guarantee,
   and the credit compounds at `ans_rate` for up to twenty-five years, so it dominates the maturity
   benefit and every surrender value after the early durations. The base run is **one carrier's 2026
   rate held level forever** [S11]; the `low` and `nil` scenarios exist so the range is exercisable.
   And the base rate is for an **endowment** book while the only market averages available are for the
   **annuity** [R25] — the identity of the two is plausible and [unverified] (gap 2).
2. **The *Zillmerung* and the § 169 floor together.** `alpha_rate` at the 25 ‰ ceiling drives the
   negative early reserve, the whole early-duration surrender-value profile, the year-one strain and
   the duration at which the contract first earns any interest surplus at all. The ceiling is cited
   [R7] [REG-R16]; **the level is [std] and no German carrier's actual acquisition cost is public**
   (gap 7). Halving it moves the first five surrender values by more than any other single parameter.
3. **The mortality basis, in two directions at once.** The proxy's level and slope are both unsourced,
   and the same table serves a death leg and a survival leg whose directions of prudence are opposite
   [REG-R47] [REG-R48]. On a twenty-five-year endowment the survival leg dominates the reserve, so a
   level error matters less than on a term cover — but `mort_be_factor` moves the *Risikoüberschuss*
   the model does **not** compute, so the sensitivity is understated by construction, and the proxy
   carries **no selection**, which overstates early deaths on newly written business.
4. **The lapse shape.** Cumulative surrender over twenty-five years removes a large part of the cohort
   before the *Ablauf*, and on an endowment the late years are the profitable ones, so the assumption
   governs how much of the loaded tail is ever collected. The duration-12 spike is the one feature the
   evidence supports [R10] [REG-R45]; **the levels are unsourced**, the market aggregates are not
   surrender rates [R20], and a user with experience data should replace the whole table.
5. **The terminal bonus.** `term_rate = 0.40%` has **no source at all** (gap 1) and it accrues on the
   reserve for the whole term, so it is a visible share of the maturity benefit built entirely on a
   [std] number. Its payability on surrender — zero here — is a second unsourced choice, and it is the
   one that would change surrender values most.
6. **The *Überschussverwendung* choice.** Switching `ansammlung` → `bonus` moves benefit **between**
   death and maturity without changing the surplus credited, and `→ beitragsverrechnung` moves it out of
   the benefit stream into the premium stream, changing the sign of the surplus in the cash flow
   statement. The corpus does not establish which system the market uses [R28] (gap 4), so the base
   case is **[std]** and this is a structural rather than a parametric sensitivity.
7. **The *Beitragsfreistellung* take-up.** Modelled as a deterministic election because no take-up rate
   exists in the corpus. A real German book converts a material share of contracts to *beitragsfrei*
   [R20] [REG-R28], and a projection that shows none is not conservative in either direction: it
   overstates future premium income and overstates future benefits together.
8. **The *Bewertungsreserven* and the ZZR, both unmodelled.** The first is set to zero on the reasoning
   that the *Sicherungsbedarf* has routinely exhausted it [R8] [REG-R9]; the second is the mechanism by
   which a high-guarantee cohort depresses the declared rate for everyone [REG-R17]. Both are
   balance-sheet quantities a gross liability model cannot produce, and both would move the answer.
9. **Data provenance.** Every charge level, every behavioural rate, the terminal bonus, the
   *Ansammlungszinssatz*, the *Stornoabzug* schedule, the entry age, the sum insured and the mortality
   proxy are **[std]**; the corpus's only quantified carrier terms are Debeka's *Stornoabzug*, sub
   judice [S3] [R22] [R30], and Allianz's declared rate [S11]. **A calibration pass against a
   *Produktinformationsblatt*, a PRIIP-*Basisinformationsblatt* and a named insurer's § 28 RechVersV
   *Anhang* disclosure [REG-R54] is required before any quantitative use.**
