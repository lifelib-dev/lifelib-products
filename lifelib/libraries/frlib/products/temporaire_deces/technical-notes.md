# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model — model
name **`TD_FR_A`**, **annual** grid — for the standardized composite French *assurance
temporaire décès* defined in `product-spec.md` (same directory). This is not any single
insurer's product. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried
from `_research/temporaire-deces.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own R-numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified]
marks claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. Cells names, model-point columns and CSV headers are English
`lower_snake_case`; French terms of art keep their French form in prose.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — cotisations, death claims,
  PTIA claims, expenses and commission — for a single-policy model point, on an expected
  (probability-weighted) basis. Discounting, the *provision mathématique* recursion, the
  Solvabilité II risk margin and the capital layers are out of scope (see Valuation and reserve
  pointers).
- **Projection frequency.** **Annual grid.** The contract is itself annual — a one-year cover
  renewed by *tacite reconduction*, repriced at each renewal [S1] [S2] [S3] [S6] [S8] [S9] — so
  the annual grid is the contract's own grid, not an approximation of a finer one. The opposite
  holds in `products/assurance_emprunteur/`, where a monthly loan schedule forces a monthly grid.
- **Projection horizon.** `proj_len = cover_end_age − issue_age`, so policy year `t` covers
  attained age `issue_age + t − 1` and the last covered year is the one at attained age
  `cover_end_age − 1`. For the worked configuration, `proj_len = 75 − 58 = 17`.
- **Timing conventions [std].** Cotisations at the **start** of each policy year (annual in
  advance, the contracts' base mode [S1] [S2] [S6] [S7] [S8] [S9]); maintenance expense and
  renewal commission at the start of the year; death and PTIA claims at the **end** of the
  policy year of claim; lapses at the end of the year, **after** the insured decrements;
  acquisition expense and initial commission at issue.
- **Age basis.** *Différence de millésime* — calendar year minus year of birth, irrespective of
  birth month [S1] [S2] [S6] [S7]. In this annual model the age steps at the **policy
  anniversary**; the real millésime age steps on 1 January, so an implementation on real dates
  carries a fractional offset of at most one year **[std]**.
- **Termination.** All states terminate at `t = proj_len`: cover ceases at the age limit,
  nothing is payable, there is no maturity value and no conversion [S3] [S5] [S11] [S15] [S16].
  `pols_if(proj_len + 1)` is never a weight on a cash flow, but it is **not** unused: it is the
  survivor term of the closure identity below, and it is what the lapse rate in the final policy
  year — zero, by the convention set out under *Lapse* — decides.
- **No cash value anywhere.** Art. L. 132-23 forbids both *rachat* and *réduction* on a
  temporaire décès [R3]. The model has **no account value, no surrender cells, no paid-up
  state**, and `claims_lapse(t)` is structurally zero at every `t`.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive**
  (cotisations +, claims and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `premium_form` | enum {revisable, constante} | revisable |
| `benefit_shape` | enum {constant, decreasing} | constant |
| `benefit_schedule_id` | str (key into `benefit_schedule.csv`) | constant |
| `sex` | enum {M, F} — reporting only; pricing is unisex [R10] | M |
| `smoker` | enum {N, S} — feeds `rating_factor`, no published level | N |
| `issue_age` | int (*différence de millésime*) | 58 |
| `sum_assured` | EUR | 150,000 |
| `cover_end_age` | int (death cover ceases at this attained age) | 75 |
| `ptia_end_age` | int (PTIA cover ceases at this attained age) | 65 |
| `premium_rate_id` | str (key into `premium_rate_table.csv`) | maif_2019 |
| `rating_factor` | float (*surprime* multiplier on the tariff rate) | 1.00 |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | annual |
| `level_premium` | EUR; 0 = derive by equivalence (`constante` form only) | 0 |
| `waiting_period_y` | int (*délai d'attente*, years) | 0 |
| `accident_multiplier` | float (additional accidental capital, 1.00 = option off) | 1.00 |
| `issue_date` | date | — |

`premium_form` is the column a UK or US reader is most likely to get wrong, and it is the
first entry in Known modeling pitfalls. `sex` is carried but **must not** enter pricing:
art. L. 111-7 forbids sex-based premium and benefit differences for contracts written from
21 December 2012 [R10], while the homologated valuation tables remain sex-specific
[R6] [REG-R22] — the same tension `products/rente_viagere/` faces from the other side.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len` | Number of projection steps = `cover_end_age − issue_age` | once per model point |
| `age(t)` | Attained age in policy year t = `issue_age + t − 1` | annual |
| `pols_if(t)` | In-force probability at the start of policy year t; `pols_if(1) = 1` | annual recursion |
| `prem_rate(t)` | Tariff rate at `age(t)`, read from `premium_rate_table.csv` | lookup |
| `prem_freq_load(t)` | Fractionation multiplier for `prem_freq`, from `freq_loading_table.csv` | lookup |
| `prem_pp(t)` | Cotisation per in-force policy for year t | annual |
| `benefit_pp(t)` | Capital payable on a year-t death or PTIA claim | annual (schedule) |
| `mort_rate(t)` | Annual **dependent** rate of the death decrement at `age(t)` | lookup |
| `ptia_rate(t)` | Annual **dependent** rate of the PTIA decrement; **0** once `age(t) ≥ ptia_end_age` | lookup |
| `lapse_rate(t)` | Annual lapse rate, applied after the insured decrements; **0** at `t = proj_len` | lookup |
| `suicide_factor(t)` | Death-benefit exclusion factor; < 1 in year 1 only, never applied to PTIA | annual |
| `pols_death(t)` | Expected deaths in year t = `pols_if(t) × mort_rate(t)` | annual |
| `pols_ptia(t)` | Expected PTIA claims in year t = `pols_if(t) × ptia_rate(t)` | annual |
| `pols_lapse(t)` | Expected lapses in year t, on survivors of both decrements | annual |
| `premiums(t)` | `prem_pp(t) × pols_if(t)` | annual |
| `claims_death(t)` | `benefit_pp(t) × pols_death(t) × suicide_factor(t)` | annual |
| `claims_ptia(t)` | `benefit_pp(t) × pols_ptia(t)` | annual |
| `claims_lapse(t)` | **Structurally 0** — a lapse pays nothing [R3] | annual |
| `expenses(t)` | Acquisition + maintenance + claim expense + commission | annual |
| `net_cf(t)` | Net liability cash flow, income-positive | annual |

There is **no** account-value state variable, **no** surrender-value state variable and **no**
paid-up state. That is a statutory fact about the product, not a modeling simplification
[R3] [S7] [S9].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Cotisation rule | `sum_assured × prem_rate(age(t)) × rating_factor × prem_freq_load`, **plus the fixed *frais d'échéance* once a year** where the mode is fractionated | [S1] [S2] [S3] [S4] [S6] [S7] [S9]; fee [S1] |
| Tariff rate table | The published attained-age grid below, ages 18–74 | [S3] |
| Repricing | At the effective date and again at **every annual renewal**, on attained age | [S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10] |
| Death benefit | `sum_assured`, constant, from any cause | [S1] [S2] [S3] [S6] [S7] [S9] |
| PTIA benefit | The **same** capital, paid early to the insured; payment ends the contract | [S1] [S2] [S3] [S6] [S8] |
| Death/PTIA cumulation | Prohibited; the PTIA capital is due only if the insured is alive at payment | [S1] [S2] |
| PTIA cessation | At `ptia_end_age`, earlier than `cover_end_age` at five of the eight carriers but equal at one [S1] and absent at one [S9], so the two ages are separate model-point columns | [S3]; pattern [S2] [S6] [S7] [S8]; exceptions [S1] [S9] |
| Premium cessation | On death and on recognition of PTIA | [S3] [S7] |
| Suicide | Death cover "de nul effet" in the **first year**; covered from the second; clock restarts on an increase, for the increment only. The alinéa 4 immediate cover with its 120 000 € floor is confined to principal-residence loan cover and **does not apply here** | [R1] [R2] |
| Surrender / paid-up value | **None**, by statute; expiry at `cover_end_age` pays nothing | [R3] [S3] [S5] [S7] [S9] [S11] |
| Fractionation loading `prem_freq_load` | Annual 1.000 (with a 1 % direct-debit discount at one carrier); half-yearly 1.0250; quarterly 1.0400; monthly 1.0400, plus a fixed *frais d'échéance* of 3 € / 6 € / 15 € (10 instalments) or 18 € (12) | [S1] |
| Age basis | *Différence de millésime* | [S1] [S2] [S6] [S7] |

**The attained-age tariff table** [S3] — *tarif de base annuel*, in per cent of the guaranteed
capital, by attained age. The only complete French standalone temporaire décès rate card in the
corpus; shipped as `premium_rate_table.csv` under `rate_id = maif_2019`:

| Age | Rate | Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|---|---|---|---|---|---|---|---|---|---|
| 18–34 | 0,15 % | 42 | 0,32 % | 50 | 0,64 % | 58 | 1,05 % | 66\* | 2,55 % |
| 35 | 0,17 % | 43 | 0,36 % | 51 | 0,69 % | 59 | 1,13 % | 67\* | 2,78 % |
| 36 | 0,17 % | 44 | 0,40 % | 52 | 0,74 % | 60 | 1,56 % | 68\* | 2,88 % |
| 37 | 0,19 % | 45 | 0,44 % | 53 | 0,79 % | 61 | 1,68 % | 69\* | 3,14 % |
| 38 | 0,20 % | 46 | 0,48 % | 54 | 0,85 % | 62 | 1,81 % | 70\* | 3,43 % |
| 39 | 0,22 % | 47 | 0,52 % | 55 | 0,91 % | 63 | 1,97 % | 71\* | 3,74 % |
| 40 | 0,24 % | 48 | 0,56 % | 56 | 0,93 % | 64 | 2,14 % | 72\* | 4,09 % |
| 41 | 0,29 % | 49 | 0,60 % | 57 | 0,99 % | 65 | 2,33 % | 73\* | 4,46 % |
| | | | | | | | | 74\* | 4,86 % |

\* Entry is capped at 65, so ages 66–74 are in-force rates only — the carrier's own footnote
reads "la dernière colonne vous indique donc le tarif de base, **en cours de contrat**, pour
couvrir le risque de décès entre 65 et 75 ans" [S3]. The carrier's own two worked examples fix
the rule: 20 000 € at age 34 → 20 000 × 0,15/100 = **30 €** for one year; 150 000 € at age 49 →
150 000 × 0,60/100 = **900 €** for one year [S3]. **Vintage caveat:** the grid is a 2019–2021
edition; use it for shape, not level (product spec, footnote 7) [S3] [S4] [S10].

### (b) Insurer-discretionary current elements

Thin, but not empty — and thinner than it looks, because the discretion on this product bites
through the **rate card**, not through a bonus or a charge scale.

| Input | Snapshot value | Basis |
|---|---|---|
| Tariff drift (experience repricing of the class) | **0 % p.a.** — the rate card is frozen at its retrieved vintage in the base run **[std]** (1) | discretion cited at **two** carriers: "l'accroissement de la fréquence et/ou du coût moyen des sinistres" [S1] and "les résultats des garanties Assurance Décès" [S6]. A third reserves repricing for legislative or regulatory change only, with 15 days to terminate on a tariff change [S7] |
| *Revalorisation* / indexation of capital and cotisation | **Off** in the base run **[std]** (1) | PASS-linked [S1] [S7]; insurer-set rate [S2] [S6] |
| *Surprime* level (`rating_factor`) | **1.00** (standard rates) **[std]** (2) | mechanics [S1] [S2] [S3] [S6]; no published scale |
| Participation aux bénéfices | **None at policy level.** Computed globally across the insurer's life book where it exists at all | [S1] [S2]; none at all [S9] |
| Post-death revalorisation | Not projected — a sub-annual window between death and settlement | [S1] [S2] [S3] [S6]; [REG-R39] |

1. Both levers reprice the contract in force, and both are exogenous to the liability model: an
   experience re-rating multiplies `prem_rate`, an indexation multiplies `sum_assured` and
   `prem_pp` together. Setting both to zero keeps the base run reproducible from cited data
   alone. Note the asymmetry the contracts record: an increase decided by the insurer gives the
   member 30 days (15 at one carrier) to terminate, while an increase arising from age, index
   or law "n'ouvre droit ni à contestation ni à résiliation" [S1] [S7].
2. No insurer publishes a *surprime* scale [S1] [S2] [S3] [S6] [S7]. The only public French
   price evidence on rated lives is on borrower cover — average 1,01 % of initial capital before
   *écrêtement* and 0,65 % after [REG-R37] — which bounds a standard rate from above.

### (c) Behavioral / experience assumptions (modeler's view)

**Every input in this class is [std].** No French insurer publishes a mortality table, an A/E
factor, a PTIA incidence rate, an expense loading, a commission scale or a lapse rate for this
product [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12].

**Mortality.** The regulatory non-annuity tables are **TH 00-02** (male) and **TF 00-02**
(female), homologated by the arrêté du 20 décembre 2005 with effect from 1 January 2006 and
built by INSEE on French mortality observed over 2000–2002 [R6] [R9] [REG-R22]. They are annexed
to an *arrêté* and are **cited by name, never shipped** in this library [REG-R22] [REG-R23].
Where a single homologated table is used for all insureds it must be the one giving the most
prudent tariff — the male table for a death cover [R4]; the alternative in market practice is a
blend, and the Institut des actuaires' working group uses **60 % TH 00-02 / 40 % TF 00-02** as
its unisex death basis [R13]. Neither choice is prescribed by any retrieved text, so adopting
one is **[std]**. The shipped `mort_table.csv` is therefore a **[std] Gompertz-form
proxy**, not a fitted table:

    mort_rate(x) = 0.00400 × 1.09^(x − 58),   ages 18–74

The 9 % per year of age is measured against the one observable French artefact, the published
tariff grid, and it sits at the **top** of what that grid shows rather than inside a tight band.
The grid rises at roughly **7–9 % per year of age from age 35** [S3]; over ages 42–58 the
step-by-step ratio `r(x+1)/r(x)` runs from **1,022** (the flat step 55 → 56, 0,91 % → 0,93 %) to
**1,125** (42 → 43) with a **median near 1,076** [S3]. Compounded, the same grid gives
`(1,05/0,32)^(1/16) − 1 = 7,7 %` a year over 42–58, `(4,86/2,55)^(1/8) − 1 = 8,4 %` over 66–74,
and `(4,86/0,17)^(1/39) − 1 = 8,98 %` over the whole rated span 35 → 74 — the last of which is
what 9 % is anchored to. It is a tariff gradient, not a mortality gradient, so the choice remains
**[std]**, and of the two unsourced numbers in this basis the slope is the more exposed on a
17-year run (see the sensitivities section). INSEE's national series [REG-R24] is the intended base for a
user-supplied replacement; it is *population*, not insured, mortality, and the reference library
records that the INSEE page **states no licence or reuse conditions** — standard open-data terms
are assumed there and that assumption is [unverified], so confirm before redistributing derived
CSVs [REG-R24]. **The anchor a substitute table must preserve is `mort_rate` at age 58 = 0.00400**,
so the worked example still closes.

*Décalages d'âge — and why they do not reach this product.* The annexed age shifts are imposed
by a clause whose scope excludes a death cover: "pour les contrats **en cas de vie** autres que
les contrats de rente viagère, les tables mentionnées au a sont utilisées en corrigeant l'âge de
l'assuré conformément aux décalages d'âge ci-annexés" [R4] [R6] [REG-R23]. A temporaire décès is
a contract *en cas de décès*, so on the retrieved texts **no shift applies to it**, and a user
who replaces `mort_table.csv` with TH 00-02 should load that table unshifted. Where the shifts do
bite, the profession recommends applying them **to the q(x), not to the l(x)**, because shifting
l(x) produces erratic q(x) growth and hence erratic provisions [R9]. The numeric annexe to the
current art. A. 132-18 was not retrieved [R4]; the abrogated A. 335-1 annexe carried shifts from
−11 years at ages 16–32 to 0 at 94+ for TF 00-02 and from −13 years at ages 16–38 to −3 at 75+
for TH 00-02 [REG-R23] — a −13-year shift is worth a factor of about 3 on this proxy's slope,
which is why applying one where it is not required is not a rounding error. The **[std]** proxy
therefore carries **no shift**, for both reasons: the rule does not reach a death cover, and a
shift applied to a proxy that was never a homologated table would be theatre.

**PTIA incidence.** No retrieved French source gives a PTIA incidence rate at any age. The model
uses `ptia_rate(x) = ptia_ratio × mort_rate(x)` with `ptia_ratio = 0.20` **[std]** for
`age(t) < ptia_end_age`, and **0** thereafter. The only public French figure that touches PTIA at
all is an underwriting-outcome statistic — 87 % of aggravated-risk applications received a PTIA
offer with no surprime and no exclusion, against 65 % for death [REG-R37] — which says nothing
about incidence. 0.20 is a placeholder chosen so PTIA is a visible but clearly secondary
decrement; it is the assumption in this file most in need of a real source.

**Lapse.** No insurer publishes a lapse rate and nothing in the corpus supports one
[S1] [S2] [S3] [S6] [S7] [S8] [S9]. The reference table is **[std]**, shaped by the one thing the
contracts do tell us — that voluntary exit is easy and cheap, because there is nothing to forfeit
[R3] and notice periods run from "at any time" to one month before the échéance
[S1] [S2] [S3] [S8] [S9]:

| Policy year | 1 | 2 | 3 | 4+ |
|---|---|---|---|---|
| `lapse_rate(t)` **[std]** (3) | 12 % | 10 % | 8 % | 6 % |

**In the final policy year the lapse rate is zero: `w(n) = 0` [std].** Lapses fall at the *end*
of the policy year (processing order, step 7), and the end of policy year `n` is the moment the
cover expires — a lapse and an expiry are then the same event paying the same nothing, so the
whole surviving cohort is booked as an expiry, `l(n+1)`. **No cash flow moves either way**, but
the convention is load-bearing for the closure identity: it decides the split between
`Σ pols_lapse` and `l(n+1)`, and it is what the worked example's 0,64637711 / 0,27886852
reproduces. Taking the table rate literally in year 17 instead — `w(17) = 6 %` — gives
0,66310922 lapses and 0,26213641 survivors, the same total and a different split.

3. **No observed range exists** — not one of the eight retrieved carriers, and neither
   secondary guide, publishes a lapse rate [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S13] [S16]. The
   shape is a modeler's construction: elevated in the first three years to absorb the 30-day
   *renonciation* window [REG-R29] [S1] [S2] [S3] and early-duration attrition, then flat.
   Nothing about the levels is sourced, and a user with experience data should replace the whole
   table.

**Suicide-exclusion factor.** Art. L. 132-7 makes the death cover void for suicide in the first
year [R1]. The model applies

    suicide_factor(1) = 0.98,   suicide_factor(t) = 1.000 for t ≥ 2   **[std]**

to **death claims only**. No retrieved source gives a suicide share of deaths at any age — INSEE
cause-of-death data was not fetched for this research — so 0.98 is a placeholder standing for
"about 2 % of first-year deaths are excluded suicides". Setting it to 1.000 is a defensible
variant; what is **not** defensible is applying it to PTIA, or applying it beyond year 1, both
of which are pitfalls below.

**Expenses and commission (all levels [std]; the structures are cited where they exist).**

| Input | Value | Basis |
|---|---|---|
| Acquisition expense `acq_expense` | 250 € per policy at issue | **[std]** (4) |
| Initial commission rate `comm_rate_init` | 40 % of the first-year cotisation | **[std]** (4) |
| Renewal commission rate `comm_rate_renew` | 5 % of the cotisation from year 2 | **[std]** (4) |
| Maintenance expense `maint_expense` | 25 € per policy p.a., inflating at `expense_infl` | **[std]** (4) |
| Expense inflation `expense_infl` | 2 % p.a. flat | **[std]** (4) |
| Claim expense `claim_expense` | 150 € per death or PTIA claim | **[std]** (4) |
| Association subscription | 0 € (individual wrapper); 1,30 € per member per year in a group wrapper | [S1]; wrapper choice **[std]** (4) |
| Technical rate `tech_rate` | 0,5 % p.a., used **only** for the `constante` equivalence, never to discount the published cash flows | **[std]** (5) |

4. **No observed range exists.** No French insurer publishes an expense loading, an acquisition
   cost or a commission scale for this product [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12]; the
   *chargements de gestion* are built into the tariff and are not separately disclosed anywhere,
   which is precisely why art. R. 343-3 has to require the *provision mathématique* to carry them
   [R11]. The **only** disclosed charge figures in the whole corpus are the fractionation
   loadings and *frais d'échéance* [S1], the 1,30 € association subscription [S1] and the 3 %
   annuity conversion charge [S3], and none of them is an expense assumption. The levels above
   are round-number placeholders sized so that year-one acquisition cost (250 € + 40 % of the
   cotisation) is of the same order as the year-one cotisation at the anchor age.
5. The Institut des actuaires' own illustrations for a death cover use technical rates of
   **0,5 %** and **0 %** against a 1 % interest assumption [R13]; art. A. 132-1 caps a French
   tariff rate at min(3,5 %, 60 % TME) for contracts *à primes périodiques* of any duration
   [R5] [REG-R17], so 0,5 % is well inside the cap. Adopting 0,5 % rather than 0 % is **[std]**.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, `t = 1 … n`, `n = proj_len = cover_end_age − issue_age` |
| `x(t)` | attained age in year t = `issue_age + t − 1` |
| `SA` | `sum_assured` |
| `r(x)` | tariff rate at attained age x, from `premium_rate_table.csv` |
| `f` | `rating_factor`; `φ` = `prem_freq_load` |
| `F` | `prem_freq_fee`, the fixed annual *frais d'échéance* — a euro amount, not a rate, and nil on the annual mode [S1] |
| `P_tar(t)` | `prem_tariff_pp(t)`, the tariff cotisation for year t **before** `F` |
| `P(t)` | `prem_pp(t)`, the cotisation actually charged per in-force policy for year t, `= P_tar(t) + F` |
| `P_lev` | the level cotisation of the `constante` form, also before `F` |
| `B(t)` | `benefit_pp(t)`, the capital payable on a year-t claim |
| `q_d(t)` | `mort_rate(t)`, dependent annual rate of the death decrement |
| `q_p(t)` | `ptia_rate(t)`, dependent annual rate of the PTIA decrement |
| `w(t)` | `lapse_rate(t)`, applied after both decrements **[std order]**; `w(n) = 0` in the final policy year **[std]** |
| `σ(t)` | `suicide_factor(t)` |
| `l(t)` | `pols_if(t)`, in force at the start of year t; `l(1) = 1` |
| `p_τ(t)` | tariff survivorship, decrements only, no lapse: `p_τ(1) = 1`, `p_τ(t+1) = p_τ(t)(1 − q_d(t) − q_p(t))` |
| `v` | `1 / (1 + tech_rate)` |
| `E0`, `e(t)` | acquisition expense; maintenance expense = `25 × 1.02^(t−1)` |
| `c0`, `c_r` | initial commission rate (0.40); renewal commission rate (0.05) |
| `ec` | claim expense (150) |

`q_d` and `q_p` are per-annum probabilities (dimensionless); `SA`, `B`, `P` are EUR; every
cash-flow component is EUR per policy year.

### Cotisation by premium form

**`revisable`** — the French default, and the product's signature.
`P_tar(t) = SA × r(x(t)) × f × φ`, which changes at every `t` because `r` is read at the new
attained age [S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10].

**`constante`** — a **[std]** construction (product spec, footnote 2). If `level_premium > 0` it
is used directly; otherwise `P_lev` is derived by actuarial equivalence with the revisable stream
over the whole cover period, on **tariff survivorship** (insured decrements only, no lapse) and
the technical rate:

    P_lev = [ Σ_{t=1..n} v^(t−1) · p_τ(t) · SA · r(x(t)) · f · φ ] / [ Σ_{t=1..n} v^(t−1) · p_τ(t) ]

i.e. a survivorship-and-discount-weighted average of the same grid rates; `P_tar(t) = P_lev` for
all `t`.

**Then the fee, once, under either form:**

    P(t) = P_tar(t) + F

`F` is the fixed annual *frais d'échéance* attached to the payment frequency — 0 € annual,
3 € half-yearly, 6 € quarterly, 18 € monthly [S1]. It is a **euro amount, not a second
percentage**: `φ` is already a multiplier inside `P_tar`, and billing `F` as a further percentage
load, or loading the already-loaded cotisation with it, overstates premium income (pitfall 13).
`P(t)` is what the policyholder is charged, so it is what enters `premiums(t)` and the commission
base, while the `constante` equivalence above is struck on `P_tar` alone — `F` is the same amount
under either form, so it neither belongs in the equivalence nor changes it. The worked example
runs on the **annual** mode, where `F = 0` and `P(t) = P_tar(t)`; the three fractionated model
points are where the two differ, e.g. 933,20 € against 915,20 € in year 1 of model point 4.

### Decrements and the in-force recursion

`q_d` and `q_p` are **dependent** rates — rates of decrement in a two-decrement table, not
independent single-decrement rates. Therefore they are **additive**:

    pols_death(t) = l(t) × q_d(t)
    pols_ptia(t)  = l(t) × q_p(t)
    pols_lapse(t) = l(t) × (1 − q_d(t) − q_p(t)) × w(t)
    l(t+1)        = l(t) × (1 − q_d(t) − q_p(t)) × (1 − w(t)),    l(1) = 1

with `q_d(t) + q_p(t) < 1` required at every `t`, and the PTIA switch-off a hard gate on the
attained age rather than a taper: `q_p(t) = ptia_ratio × q_d(t)` if `x(t) < ptia_end_age`, else
`0`. This is what "the PTIA capital is an anticipated payment of the death capital, and its
payment ends the contract" means arithmetically [S1] [S2] [S3] [S6]: a life that leaves through
the PTIA decrement is gone from `l` and can never generate a death claim. **Closure identity**,
which a test should assert:

    Σ_{t=1..n} [ pols_death(t) + pols_ptia(t) + pols_lapse(t) ] + l(n+1) = 1

### Benefit amounts and claims

`B(t) = SA × benefit_factor(benefit_schedule_id, t)`, with `benefit_factor ≡ 1.0` for
`benefit_schedule_id = constant`, the only schedule shipped [S1] [S2] [S3] [S6] [S7] [S8] [S9]:

    claims_death(t) = B(t) × pols_death(t) × σ(t)
    claims_ptia(t)  = B(t) × pols_ptia(t)
    claims_lapse(t) = 0                                   [R3]

`σ` never touches `claims_ptia`: art. L. 132-7 voids the **death** cover for suicide in year one
[R1], and PTIA is not death. With `accident_multiplier > 1` an additional capital
`(accident_multiplier − 1) × B(t) × acc_share` is payable on the accidental share of claims
[S1] [S2] [S6] [S7] [S9] [S12]; `acc_share` has **no source in the corpus** and the base run sets
it to 0 **[std]**.

### Expenses, commission and net cash flow

    premiums(t)    = P(t) × l(t)               with P(t) = P_tar(t) + F
    commissions(t) = c0 × P(1) × l(1)          for t = 1
                   = c_r × P(t) × l(t)          for t ≥ 2
    expenses(t)    = E0 · 1{t = 1} + e(t) × l(t) + ec × (pols_death(t) + pols_ptia(t))
                     + commissions(t)
    net_cf(t)      = premiums(t) − claims_death(t) − claims_ptia(t) − expenses(t)
    liability_cf(t) = −net_cf(t)

`result_cf()` publishes, indexed by `t`: `pols_if`, `premiums`, `claims_death`, `claims_ptia`,
`claims_lapse`, `expenses`, `commissions`, `net_cf`.

### Annual processing order

For `t = 1 … n`, in this order:

1. Set `x(t) = issue_age + t − 1`. If `x(t) ≥ cover_end_age`, stop — the projection is over.
2. Look up `r(x(t))`, compute `P_tar(t)` per the premium form and add the fee once,
   `P(t) = P_tar(t) + F`. Take the cotisation in advance: `premiums(t) = P(t) × l(t)`.
3. Charge start-of-year expenses on the in-force: `e(t) × l(t)`, plus `E0` and the initial
   commission at `t = 1`, plus the renewal commission for `t ≥ 2`.
4. Compute `B(t)` from the benefit schedule.
5. Look up `q_d(t)`; set `q_p(t) = 0` if `x(t) ≥ ptia_end_age`, else `ptia_ratio × q_d(t)`.
6. **End of year — claims:** `claims_death(t)` (with `σ(t)`) and `claims_ptia(t)`, plus the
   claim expense on both. Claimants have already paid the year's cotisation in step 2; this is
   the model's reading of "premium payment ceases at death and at PTIA" [S3] [S7] on an
   annual-in-advance grid **[std]**.
7. **End of year — lapses:** apply `w(t)` to the survivors of both decrements. A lapse pays
   nothing [R3]. At `t = n`, `w(n) = 0` **[std]**: the end of the last policy year is also the
   moment the cover expires, so the survivors leave as an expiry rather than as a lapse. The two
   events pay the same nothing, and no cash flow moves — but they land on different sides of the
   closure identity.
8. Update `l(t+1) = l(t) × (1 − q_d(t) − q_p(t)) × (1 − w(t))`.

At `t = n` the projection ends with no maturity payment and no tail state.

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each
one is a test.

1. **Assuming a level cotisation.** The French default is `revisable`, not `constante`
   [S1] [S2] [S3] [S6] [S7] [S9] [S10]. Assert that `prem_pp(t)` varies with `t` on the
   revisable form, and specifically that `prem_pp(3) / prem_pp(2) = 1.56 / 1.13 = 1.380531`
   in the worked configuration.
2. **Paying the capital twice.** PTIA is an acceleration, not an addition [S1] [S2] [S3] [S6].
   Assert `Σ(pols_death + pols_ptia) ≤ 1` and
   `Σ(claims_death + claims_ptia) = SA × Σ(pols_death + pols_ptia) − (1 − σ(1)) × SA ×
   pols_death(1)` exactly. A life removed by the PTIA decrement must not appear in `l(t+1)`.
3. **Forgetting that PTIA cover stops first.** `ptia_end_age < cover_end_age` in five of the
   eight retrieved carriers [S2] [S3] [S6] [S7] [S8]. Assert `claims_ptia(t) = 0` for every
   `t` with `x(t) ≥ ptia_end_age` — in the worked configuration, exactly zero for `t = 8 … 17`.
4. **Mixing the competing-risk conventions.** These notes use **additive dependent rates**
   (`q_d + q_p`). An implementation using independent rates,
   `1 − (1 − q_d)(1 − q_p)`, gets 0.00479680 against 0.00480000 in year 1 — a 3.2 × 10⁻⁶
   difference in the rate and 0.48 € in year-1 expected claims per 150 000 € of capital.
   Immaterial here, material at older ages and higher rates. Declare the convention and test it.
5. **Inventing a surrender value.** There is none, by statute [R3] [S7] [S9]. Assert
   `claims_lapse(t) == 0.0` at every `t`, and that no `av_pp_at` / cash-value cells exist.
6. **Getting the age basis wrong.** *Différence de millésime*, not age nearest birthday
   [S1] [S2] [S6] [S7]. A one-year shift moves `prem_pp(1)` from 1 575,00 € (age 58) to
   1 695,00 € (age 59) — a 7,6 % error in year one that compounds through the whole projection.
7. **Smoothing the tariff away.** The grid steps +38 % from age 59 to 60 against a trend of
   about +8 % [S3]. Assert `prem_rate` is a table lookup and that `r(60)/r(59) = 1.380531`
   survives; a fitted curve will not reproduce it.
8. **Misapplying the suicide factor.** `σ` applies to `claims_death` in year 1 only, and never
   to `claims_ptia` [R1]. Assert `claims_death(1) = 0.98 × B(1) × pols_death(1)`,
   `claims_death(2) = B(2) × pols_death(2)` with no factor, and
   `claims_ptia(1) = B(1) × pols_ptia(1)` with no factor. Also assert the model does **not**
   carry the art. R. 132-5 immediate-cover ceiling of 120 000 €, which belongs to
   principal-residence loan cover only [R1] [R2].
9. **Double-counting the premium-cessation rule.** Cotisations are in advance and claims are at
   year end, so a claimant has already paid the year's cotisation. Do **not** additionally
   multiply `premiums(t)` by `(1 − q_d − q_p)` — that applies the rule twice and understates
   year-t premium income by about 0,5 % at the anchor age.
10. **Running past the age limit.** `proj_len = cover_end_age − issue_age`. There is no
    benefit, no cotisation and no maturity value at `t = proj_len + 1`, and `l(proj_len + 1)`
    is never used in a cash flow [S3] [S5] [S11] — but it is used in the closure identity, and
    it is only well defined once `w(n) = 0` is stated. Assert both: `lapse_rate(n) = 0` while
    `lapse_rate_base(n)` is still the table's 6 %, and that the four closure terms sum to 1.
11. **Expecting the two premium forms to collect the same total.** The `constante` equivalence
    is struck on **tariff survivorship** (no lapse). Once lapses truncate the expensive late
    years, the projected premium total under `constante` **exceeds** the revisable one —
    36 367,46 € against 31 999,13 € in the worked configuration. That is correct, not a bug;
    a test that asserts equality of projected premium totals is testing the wrong identity.
    The identity that *does* hold is `Σ v^(t−1) p_τ(t) P(t)` equal across the two forms.
12. **Applying `rating_factor` to the benefit.** A *surprime* scales the cotisation only, never
    the capital [S1] [S2] [S3] [S6]. Assert `claims_death` is invariant to `rating_factor`.
13. **Double-charging the fractionation loading.** `prem_freq_load` (`φ`) is a multiplier
    embedded in the cotisation TTC; the *frais d'échéance* (`F`) are a separate fixed fee, in
    euros [S1]. Applying both as percentage loads, or applying the loading and then also billing
    the fee as a percentage, overstates premium income. The fee is charged **once a year** and it
    **is** part of what the policyholder pays, so it enters `premiums(t)` and the commission base
    but stays out of the `constante` equivalence. Assert `P(1) = 915,20 + 18,00 = 933,20 €` on
    model point 4 (monthly, 200 000 € at attained age 45) and `P(t) − P_tar(t) = 18,00 €` at
    every `t`.
14. **Treating the accidental option as a benefit multiplier.** It pays an *additional* capital
    on the accidental share of claims [S1] [S2] [S6] [S7], not a uniform uplift on every claim.
    With `acc_share = 0` in the base run, `accident_multiplier` must have **no** effect on any
    cash flow — a good invariance test.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; there is no French calibration
evidence for any of them.

- **Base lapse [std].** The duration table above. Channel and wrapper matter and are not
  modeled: a *bancassurance* contract terminates when the bank account closes [S8], which is a
  lapse driver with no actuarial counterpart in the mutual contracts.
- **Premium-shock lapse [std] (optional module, off in the base run).** The revisable form
  hands the policyholder a rising bill, and the grid's own +38 % step at age 60 [S3] is exactly
  where an affordability response would show. Reference multiplier on `w(t)`:

      M_shock(t) = 1 + β × max(0, P(t)/P(t−1) − 1 − g0)

  with `g0 = 0.10` and `β = 1.5` **[std]**. Base run `β = 0`, so `M_shock ≡ 1`. Switched on in
  the worked configuration it would bite at `t = 3` (ratio 1.380531) and nowhere else.
- **Selective lapsation [std] (optional module, off in the base run).** Lapsers are healthier on
  average, so persisters' mortality is loaded:

      q_d_eff(t) = q_d(t) × [ 1 + λ × max(0, w_cum(t) − w_ref) ]

  with `w_ref = 0.30` and `λ = 0.25` **[std]**. Base run `λ = 0`. On this product the effect is
  larger than on a UK level-premium term policy, because cumulative lapse reaches 64,6 % of the
  original cohort over the worked configuration's 17 years.
- **No dynamic surrender behavior, no renonciation decrement, no indexation take-up.** There is
  nothing to surrender [R3], so the whole of the exit machinery is lapse and a lapse pays
  nothing; the 30-day *renonciation* window [REG-R29] [S1] [S2] [S3] sits inside the year-1 lapse
  rate **[std]**; and indexation is not modeled because it reprices capital and cotisation
  together on an exogenous index [S1] [S2] [S6] [S7], with refusal definitive at three carriers
  [S2] [S6] [S7] — a one-way absorbing state if it were modeled.

---

## Worked example

**Configuration.** `premium_form = revisable`, `benefit_shape = constant`
(`benefit_schedule_id = constant`, factor 1.0 at every `t`), `issue_age = 58`,
`sum_assured = 150 000 €`, `cover_end_age = 75`, `ptia_end_age = 65`,
`premium_rate_id = maif_2019`, `rating_factor = 1.00`, `prem_freq = annual`
(`prem_freq_load = 1.000`), `waiting_period_y = 0`, `accident_multiplier = 1.00`. Hence
`proj_len = 75 − 58 = 17` and the table below is the **entire** projection.

**Assumptions, each tagged.** Tariff rates `r(x)` for ages 58–74 read from the published grid
[S3] — 1,05 / 1,13 / 1,56 / 1,68 / 1,81 / 1,97 / 2,14 / 2,33 / 2,55 / 2,78 / 2,88 / 3,14 /
3,43 / 3,74 / 4,09 / 4,46 / 4,86 %. Mortality `q_d(t) = 0.00400 × 1.09^(t−1)` **[std]**. PTIA
`q_p(t) = 0.20 × q_d(t)` for `t ≤ 7` (attained ages 58–64) and **0** from `t = 8` (attained age
65 = `ptia_end_age`) **[std]**. Lapse 12 % / 10 % / 8 % / 6 % from year 4 **[std]**, with
`w(17) = 0` because the last policy year ends at expiry (processing order, step 7) — the
assumption that fixes the lapse/survivor split in the closure check below, though it moves no
cash flow. Suicide factor `σ(1) = 0.98`, `σ(t ≥ 2) = 1.000`,
applied to death claims only **[std]** [R1]. Expenses **[std]**: `E0 = 250 €` at issue,
`e(t) = 25 × 1.02^(t−1)` per in-force policy, initial commission 40 % of `P(1)`, renewal
commission 5 % of `P(t)` from `t = 2`, claim expense 150 € per death or PTIA claim. No accident
option, no indexation, no tariff drift, no behavior modules.

`expenses` below is the total of acquisition, maintenance, claim expense and commission.
All amounts in euros; `pols_if` to six decimals; cash flows to the cent.

| t | age | r(x) | pols_if | premiums | claims_death | claims_ptia | expenses | net_cf |
|---|---|---|---|---|---|---|---|---|
| 1 | 58 | 1,05 % | 1.000000 | 1,575.00 | 588.00 | 120.00 | 905.72 | −38.72 |
| 2 | 59 | 1,13 % | 0.875776 | 1,484.44 | 572.76 | 114.55 | 97.24 | 699.89 |
| 3 | 60 | 1,56 % | 0.784075 | 1,834.73 | 558.94 | 111.79 | 112.80 | 1,051.21 |
| 4 | 61 | 1,68 % | 0.717235 | 1,807.43 | 557.30 | 111.46 | 110.07 | 1,028.60 |
| 5 | 62 | 1,81 % | 0.670010 | 1,819.08 | 567.46 | 113.49 | 109.77 | 1,028.35 |
| 6 | 63 | 1,97 % | 0.625542 | 1,848.48 | 577.48 | 115.50 | 110.38 | 1,045.11 |
| 7 | 64 | 2,14 % | 0.583667 | 1,873.57 | 587.32 | 117.46 | 110.82 | 1,057.97 |
| 8 | 65 | 2,33 % | 0.544230 | 1,902.08 | 596.92 | 0.00 | 111.33 | 1,193.83 |
| 9 | 66 | 2,55 % | 0.507836 | 1,942.47 | 607.14 | 0.00 | 112.61 | 1,222.73 |
| 10 | 67 | 2,78 % | 0.473561 | 1,974.75 | 617.11 | 0.00 | 113.50 | 1,244.13 |
| 11 | 68 | 2,88 % | 0.441280 | 1,906.33 | 626.80 | 0.00 | 109.39 | 1,170.14 |
| 12 | 69 | 3,14 % | 0.410875 | 1,935.22 | 636.14 | 0.00 | 110.17 | 1,188.91 |
| 13 | 70 | 3,43 % | 0.382236 | 1,966.60 | 645.06 | 0.00 | 111.09 | 1,210.45 |
| 14 | 71 | 3,74 % | 0.355260 | 1,993.01 | 653.49 | 0.00 | 111.79 | 1,227.72 |
| 15 | 72 | 4,09 % | 0.329849 | 2,023.62 | 661.36 | 0.00 | 112.72 | 1,249.54 |
| 16 | 73 | 4,46 % | 0.305913 | 2,046.56 | 668.57 | 0.00 | 113.29 | 1,264.70 |
| 17 | 74 | 4,86 % | 0.283369 | 2,065.76 | 675.04 | 0.00 | 113.69 | 1,277.03 |
| **Total** | | | | **31,999.13** | **10,396.90** | **804.25** | **2,676.38** | **18,121.59** |

`claims_lapse(t) = 0.00` at every `t` and is omitted from the table for space; it is a required
column of `result_cf()`. The **Total** row is the sum **at full precision, then rounded** — for
`claims_death` that is 10 396,90 € against 10 396,89 € if the seventeen already-rounded cells are
added, a one-cent accumulation. Assert the full-precision total.

**Level-premium variant.** The same cell with `premium_form = constante` and
`level_premium = 0`, so `P_lev` is derived by equivalence at `tech_rate = 0,5 %`:

    P_lev = 60,476.2476 / 15.449728 = 3,914.3891 €   (displayed 3,914.39)

The variant table below carries `P_lev` **unrounded**. Every displayed row is stable at two
decimals under either treatment; only the premium total moves, to 36 367,47 € if `P_lev` is
rounded to the cent before projecting.

Selected rows of the resulting projection — decrements, benefits and `pols_if` are identical to
the table above, only the premium and the commission change, and the **Total** row covers all
seventeen years, not only the five displayed:

| t | age | prem_pp | premiums | claims_death | claims_ptia | expenses | net_cf |
|---|---|---|---|---|---|---|---|
| 1 | 58 | 3,914.39 | 3,914.39 | 588.00 | 120.00 | 1,841.48 | 1,364.91 |
| 2 | 59 | 3,914.39 | 3,428.13 | 572.76 | 114.55 | 194.43 | 2,546.39 |
| 3 | 60 | 3,914.39 | 3,069.17 | 558.94 | 111.79 | 174.52 | 2,223.93 |
| 8 | 65 | 3,914.39 | 2,130.33 | 596.92 | 0.00 | 122.74 | 1,410.66 |
| 17 | 74 | 3,914.39 | 1,109.22 | 675.04 | 0.00 | 65.86 | 368.32 |
| **Total** | | | **36,367.46** | **10,396.90** | **804.25** | **3,713.59** | **21,452.72** |

The two forms are the whole point of this product. The revisable premium runs from 1 575,00 €
to 7 290,00 € — a factor of **4,6286**, exactly `r(74)/r(58) = 4,86/1,05` and independent of
the capital — while the level premium is flat at 3 914,39 €, above the tariff until year 8 and
below it thereafter. The revisable form has almost no new-business strain (year 1 `net_cf` is
−38,72 €); the level form is strongly positive in year 1 (+1 364,91 €) and would carry a real
*provision mathématique* against the later years [R11] [R13].

**Checks.**

*The cotisation rule, from the source's own example.* The carrier publishes "150 000 € ×
(0,60 : 100) = 900 € pour un an" at attained age 49 [S3]. The same rule at attained age 58
gives `P(1) = 150 000 × 1,05/100 = 1 575,00 €`, and the year-17 rate reproduces
`150 000 × 4,86/100 = 7 290,00 €`. The ratio 7 290,00 / 1 575,00 = 4,6286 equals
4,86 / 1,05 = 4,6286 — the premium multiple over the contract depends only on the grid, not on
the capital, which is a one-line test of the whole premium engine.

*Year 3 rebuilt from scratch, a different way.* `l(3)` from two decrement steps:
`l(2) = (1 − 0,00400 − 0,00080)(1 − 0,12) = 0,99520 × 0,88 = 0,875776`;
`q_d(2) = 0,00400 × 1,09 = 0,004360`, `q_p(2) = 0,000872`, so
`l(3) = 0,875776 × (1 − 0,005232) × 0,90 = 0,875776 × 0,8952912 = 0,78407455`, matching the
table's 0.784075. Then `q_d(3) = 0,00400 × 1,09² = 0,0047524` and `q_p(3) = 0,00095048`, giving
`claims_death(3) = 150 000 × 0,78407455 × 0,0047524 = 558,94` and
`claims_ptia(3) = 150 000 × 0,78407455 × 0,00095048 = 111,79`. Expenses:
`25 × 1,02² × 0,78407455 = 20,3938` maintenance, `0,05 × 2 340,00 × 0,78407455 = 91,7367`
renewal commission, `150 × 0,78407455 × 0,00570288 = 0,6707` claim expense — total 112,80. And
`1 834,73 − 558,94 − 111,79 − 112,80 = 1 051,21`, the table's `net_cf(3)`.

*The decrements close, and nothing is paid twice.* Summing the three exits over the 17 years:
deaths 0,06939268, PTIA claims 0,00536169, lapses 0,64637711, plus `l(18) = 0,27886852` —
total **1,00000000** exactly. The last two figures are the ones `w(17) = 0` decides: at the
table's 6 % they would read 0,66310922 and 0,26213641, still summing to one. Multiplying total claim events by the capital,
`150 000 × (0,06939268 + 0,00536169) = 11 213,155 €`, against claims actually paid of
`10 396,90 + 804,25 = 11 201,155 €`. The difference is **12,00 €**, which is precisely the
first-year suicide withholding `150 000 × 0,00400 × 0,02 = 12,00 €` [R1] — so the exclusion
factor is the *only* thing standing between expected claim events and expected claim amounts,
which is what "PTIA is an acceleration, not an addition" means arithmetically.

*The level premium is a weighted average of the grid.* Independently of the equivalence
formula, `P_lev / SA` should be the `v^(t−1) p_τ(t)`-weighted mean of the seventeen grid rates.
That mean is **2,60959276 %**, and `150 000 × 0,0260959276 = 3 914,3891 €` — the same figure,
reached without ever forming the premium stream. The weights sum to `15,449728`, the annuity-due
factor, and `P_lev × 15,449728 = 60 476,25 €` equals the present value of the revisable stream
on the same basis. Note what this identity does **not** say: the *projected* premium totals
differ (36 367,46 € against 31 999,13 €), because lapses remove policies before the expensive
late years that the level premium has already been charging for. Pitfall 11.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a
declared grid. The valuation layers consume them and are cited, not reproduced.

- **The French statutory *provision mathématique*.** Art. R. 343-3 defines it as the difference
  between the present values of the two parties' commitments and requires it to **include an
  estimate of future management costs** equal to the *chargements de gestion* built into the
  tariff [R11] [REG-R6]. On the **revisable** form the PM is close to nil at each anniversary —
  the year's cotisation buys the year's risk, so what remains is an unearned-premium and
  outstanding-claims position [R11] [R13]. On the **constante** form it builds and releases in
  the classic way: where the premium rate is flat while the death rate rises, "un montant de PRC
  est toujours constitué pendant la durée" [R13]. That contrast is the reason the `constante`
  form is carried at all. The *provision pour risques croissants* of art. R. 343-7 is defined for
  *maladie* and *invalidité*, not death [R12]; the death-cover analogue is the R. 343-3 PM —
  "la même provision de prime s'appelle PM en vie et PRC en non-vie" [R13]. Art. A. 343-1-1
  requires acquisition loadings to enter the premium-payer's commitment and floors the result at
  zero, at the surrender value and at the reduced-capital provision; the last two are **zero**
  here [R3] [R13], so the operative floor is non-negativity. Art. 142-3 of ANC 2015-11 (as
  amended by ANC 2016-12) fixes the rate at no more than the tariff rate and the table at the one
  in force when the tariff was applied, with the option to migrate in-force contracts at each
  annual inventory and to spread a change of basis over at most eight years [R13].
- **Medical selection.** The Institut's illustrative claims abatement for a selected book is
  **70 % in year 1, 50 % in year 2, 20 % in year 3** [R13]. It is not applied in the base run —
  stacking a selection abatement on an already-[std] mortality proxy would compound two unsourced
  choices — but it is the first refinement a user with real experience should make, and it
  changes the sign of the early-duration provision [R13].
- **Solvabilité II best estimate.** Probability-weighted future cash flows discounted at the
  relevant risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R4], with EIOPA
  publishing the curves monthly [REG-R5]. `BEL = Σ_t v(t) × liability_cf(t)` over the recursion
  above. **No cost-of-capital rate, contract-boundary rule or standard-formula shock in this
  library was read from a retrieved instrument**, so every such figure is **[std]** [REG-R2].
- **Contract boundary — the open question on this product.** The contract is a one-year cover
  renewed by *tacite reconduction* whose tariff the insurer recomputes at every renewal
  [S1] [S2] [S3] [S6] [S7] [S9] and, at two of them, may also reprice for class experience
  [S1] [S6]. Whether
  the Solvabilité II contract boundary therefore ends at the next renewal — as it would for a
  reviewable-premium contract — could **not** be determined: the Delegated Regulation's boundary
  rules were not retrievable [REG-R2] and the point is **[unverified]**. The model's posture:
  project to the age limit and publish the full stream; a boundary-truncated view is obtained by
  truncating `result_cf()` at `t = 1`. Do not bake the truncation into the projection.
- **IFRS 17 and professional standards.** Fulfilment cash flows plus a contractual service
  margin, effective from 1 January 2023 with no French carve-out [REG-R45]; the same
  expected-cash-flow engine feeds it, and grouping, CSM and risk adjustment are out of scope.
  *Norme de Pratique Actuarielle 2 — Modèles actuariels*, adopted 15 June 2015 with effect from
  1 January 2016, expressly covers pricing models and the technical studies attached to new
  products [REG-R44]; NPA 4, on best-estimate life provisions, was not retrieved and is
  [unverified] [REG-R44].

---

## Key sensitivities and model risks

In rough order of leverage for a French protection block:

1. **The premium form.** Switching `revisable` → `constante` moves projected premium income by
   +13,7 % (31 999,13 € → 36 367,46 €) and `net_cf` by +18,4 % on the worked configuration,
   with no change to a single claim. It is the largest single structural lever in the model, and
   the `constante` side of it is **[std]** — no French standalone contract in the corpus uses it
   [S1] [S2] [S3] [S6] [S7] [S9] [S10].
2. **Mortality basis.** The reference basis is a **[std]** Gompertz proxy because TH 00-02 /
   TF 00-02 are annexed to an *arrêté* and not redistributed here [R6] [REG-R22] [REG-R23], and
   no French insurer publishes a basis [S1]–[S9]. Both the level (`q_d` at 58) and the slope
   (9 % per year of age) are unsourced; the slope is the more dangerous of the two on a
   17-year run, since it compounds. It is calibrated to the published tariff grid's own
   gradient and sits at the top of it — the grid compounds at 7,7 % a year over ages 42–58 and
   8,98 % over the whole rated span 35 → 74 [S3] — and a tariff gradient is not a mortality
   gradient.
3. **Lapse.** Nothing in the corpus supports any lapse rate. Cumulative lapse reaches **64,6 %**
   of the original cohort over the worked configuration, so the assumption governs how much of
   the rising-premium tail is ever collected — and on a revisable contract the late years are
   the profitable ones, which inverts the usual protection intuition that early lapse is what
   hurts.
4. **PTIA incidence ratio.** `ptia_ratio = 0.20` is a pure placeholder with **no source at
   all**. It moves 804,25 € of claims in the worked configuration — 7,2 % of total claims — and
   it interacts with `ptia_end_age`, since the whole of that exposure sits in the first seven
   years.
5. **Contract boundary.** If the boundary is one year rather than the full cover period, the
   entire projection beyond `t = 1` leaves the technical provision. Nothing in this library
   resolves it [REG-R2].
6. **Tariff drift.** The base run freezes the rate card at its retrieved vintage, but the same
   carrier's current page implies about 0,189 % at age 35 against the grid's 0,17 % [S3] [S4],
   and two of the eight carriers reserve an explicit right to reprice on class experience
   [S1] [S6]. A
   drift assumption is a premium-income assumption, not a mortality one.
7. **Expense levels on small capitals, and the suicide factor.** Minimum capitals run from
   6 097,96 € [S9] to 100 000 € [S8]; at the representative carrier's 20 000 € minimum [S3] [S4]
   the year-one cotisation at age 58 is 210 € against 250 € of acquisition expense **[std]**, so
   the per-policy expense assumption, not mortality, decides whether the cell is viable. The
   suicide factor is worth only 12,00 € here — immaterial to the result, material to correctness,
   because an implementation that applies it to PTIA, or to every year, or that imports the
   120 000 € immediate-cover ceiling from loan business [R1] [R2], is wrong in a way the totals
   will not reveal.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-temporaire_deces-r1
[R10]: #frlib-temporaire_deces-r10
[R11]: #frlib-temporaire_deces-r11
[R12]: #frlib-temporaire_deces-r12
[R13]: #frlib-temporaire_deces-r13
[R2]: #frlib-temporaire_deces-r2
[R3]: #frlib-temporaire_deces-r3
[R4]: #frlib-temporaire_deces-r4
[R5]: #frlib-temporaire_deces-r5
[R6]: #frlib-temporaire_deces-r6
[R9]: #frlib-temporaire_deces-r9
[REG-R1]: #frlib-reg-r1
[REG-R17]: #frlib-reg-r17
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R37]: #frlib-reg-r37
[REG-R39]: #frlib-reg-r39
[REG-R4]: #frlib-reg-r4
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
