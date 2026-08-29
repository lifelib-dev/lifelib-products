# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation below).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a German **klassische Riester-Rentenversicherung** — the
general-account deferred annuity, sold to an individual, **certified** as an
*Altersvorsorgevertrag* (the statutory contract type of the AltZertG) and therefore drawing the
state *Zulage* (subsidy) and carrying the statutory 100 % *Beitragsgarantie*. It describes no
single insurer's contract. [S#] and [R#] tags refer to the source list in `sources.md` (numbering
carried from `_research/riester_rente.md` and frozen — never renumbered, with unused ids simply
omitted); [REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R56 numbering is separately
frozen. **[std]** marks a standardization introduced for the reference implementation; each
**[std]** row carries a numbered footnote giving the rationale and, where one exists, the observed
range. [unverified] marks a claim no search result corroborated.

**How this composite is built, and why it is built the other way round from `frlib`'s.** In
`frlib/products/temporaire_deces` the representative design was the carrier whose document
published the most. Here that is impossible and, unusually, largely unnecessary. **No
carrier-specific parameter was established for any German Riester product, at any house, for any
year** — not one AVB, tariff code, *Rechnungszins*, *Rentenfaktor*, charge or *Überschuss*
declaration (gaps 12, 13, 14). But the half of this product that makes it a *Riester* contract
rather than a private annuity is **not a composite at all**: the Zulagen, the eligibility rules,
the *Mindesteigenbeitrag*, the guarantee, the earliest payout age, the 30 % lump-sum cap, the
five-year cost spreading, the *Wechselrecht* and the taxation are **statute, identical for every
provider and every chassis** [R1] [R6] [R7] [R9] [R10] [R12] [R14] [REG-R42] [REG-R43]. The
composite takes **every statutory parameter as fact and makes every carrier parameter [std]**,
anchored so the model's own worked example reproduces exactly, and argues each choice in those
terms.

**Retrieval conditions, stated because a reader of this page alone must learn them here.** No
document cited anywhere in this product's documentation was retrieved: direct HTTP egress is
blocked by an organisation network policy, and the session's `WebSearch` budget was exhausted
before this product's research began. Three facts carry corroboration inherited from a sibling
`delib` research session and say so at the point of use [S3] [S4] [S5]; the two recent
*Höchstrechnungszins* values [R22] and the 2026 reform [REG-R44] likewise. Everything else rests
on general knowledge of German pension law, disciplined by tagging every specific number. A
`delib` citation is a **pointer, not a certificate**.

**Out of scope, named so the boundary is explicit:** *Wohn-Riester* in both limbs [R3] [R13] [R19]
[S13]; the **Riester-Fondssparplan** and **Riester-Banksparplan** [S9]–[S12]; the
**fondsgebundene** Riester wrapper [S1], whose chassis is
`products/fondsgebundene_rentenversicherung/`; the **Basisrente** of Schicht 1,
`products/basisrente/`; Riester inside the *betriebliche Altersversorgung*; and
*Gruppenversicherung*.

---

## Product overview and market role

A Riester contract is an ordinary **private-law contract** — here a *Lebensversicherungsvertrag*
governed by the VVG [REG-R22] — that has additionally been **certified** under the
*Altersvorsorgeverträge-Zertifizierungsgesetz* [R1] [R2] [REG-R43]. Certification does not change
the contract's legal nature; every VVG mechanic that reaches a Schicht-3 deferred annuity reaches
this one too, **subject to** three AltZertG overrides. Those three overrides are the whole product:

1. **Money comes in from the state, as a contribution rather than a benefit** [R8] [R9]. The
   *Zulage* is paid by the *Zentrale Zulagenstelle für Altersvermögen* (ZfA) **to the provider**,
   credited to the contract, counted in the guarantee, invested, and taxed at the end like any
   other contribution [R11]. It never reaches the saver's bank account.
2. **A guarantee is compulsory.** The provider must undertake that at the beginning of the payout
   phase **at least the sum of the *Altersvorsorgebeiträge* paid in** — the saver's own
   contributions **plus** the Zulagen credited — is available for the benefit [R1] [REG-R43]. A
   contract without it cannot be certified, and without certification there is no subsidy, so the
   *Beitragsgarantie* is not a competitive feature a provider may drop: it is the entry ticket.
3. **The exit is closed.** Surrender is permitted by contract law and punished by tax law: a
   *schädliche Verwendung* triggers repayment of **all Zulagen credited and all § 10a tax
   reductions granted**, and the investment return on the subsidised part becomes taxable [R14]
   [REG-R42].

In the *Alterseinkünftegesetz* taxonomy [R18] [REG-R38] this is **Schicht 2** — subsidised
supplementary provision, relieved on the way in and taxed **in full** on the way out under
§ 22 Nr. 5 EStG [R12], with no *Ertragsanteil*. Schicht 1 (*Basisrente*) is relieved more
generously and is completely illiquid; Schicht 3 is unrelieved and liquid. Riester sits between
them on both axes, and is in the German market's own description the layer designed for the
employed household of modest income with children. **The subsidy is the product**: stripped of the
Zulagen and the § 10a deduction, a Riester annuity is a *worse* Schicht-3 annuity — the same
general-account chassis, more constraints, full taxation instead of the *Ertragsanteil*.

**Certification is not endorsement, and no document in this library may suggest otherwise.** The
certifying authority — the *Bundeszentralamt für Steuern*, which took the function over from the
BaFin [unverified] as to the date — confirms only that a contract's **terms** satisfy the § 1
criteria, and says nothing about the provider's financial standing, the product's cost or its
expected return [R2] [S15] [REG-R43]. The state pays a subsidy and certifies the terms; the
*Beitragsgarantie* is the **provider's own**, and its ability to honour it is an ordinary solvency
question under the VAG [REG-R5] [REG-R6].

### The four certified chassis, and which one this is

| Chassis | Provider | Accumulation | Guarantee met by | Payout | In `delib`? |
|---|---|---|---|---|---|
| **Klassische Riester-Rentenversicherung** | life insurer [S2] [S4]–[S8] [S16] | *Deckungskapital* at the *Rechnungszins*, plus *Überschussbeteiligung* | the general account and the guaranteed interest | lifelong annuity at a *Rentenfaktor* | **yes — `riester_rente`, `Riester_DE_A`** |
| Fondsgebundene Riester-Rentenversicherung | life insurer [S1] | unit funds plus a guarantee asset | dynamic reallocation (*statisches*/*dynamisches Hybridmodell*, i-CPPI) | lifelong annuity at a *Rentenfaktor* | chassis in `fondsgebundene_rentenversicherung` |
| Riester-Fondssparplan | *Kapitalverwaltungsgesellschaft* — Union Investment [S9], DWS [S10], Deka [S11] | fund units | rule-based reallocation between an equity and a bond fund | *Auszahlungsplan* then *Restverrentung* from 85 | no |
| Riester-Banksparplan | *Sparkassen*, *Volks- und Raiffeisenbanken* [S12] | deposit balance plus a bonus scale | trivially — a deposit cannot fall below its deposits | *Auszahlungsplan* then *Restverrentung* from 85 | no |
| Wohn-Riester (*Bausparvertrag*, *Darlehen*) | *Bausparkassen* [S13] | savings, then a loan | not applicable | property use plus the *Wohnförderkonto* | no [R13] [R19] |

The model represents the **first row**, for three reasons. The *Beitragsgarantie* there interacts
with an **actuarial** mechanic — the *Rechnungszins* — rather than with an asset-allocation
algorithm, so the guarantee's cost is visible in the recursion instead of hidden in a rebalancing
rule. The payout is an insurance annuity throughout, so the whole contract is one liability. And
the GDV still maintains a **2025-vintage** model wording for the classic form, "Stand:
21.07.2025" [S2] — a date established by a sibling `delib` session's search of the association's
*Musterbedingungen* index [S3] and recorded on that authority — which is itself the finding that
the classic chassis is a live, separately drafted contract type rather than a simplification of
the unit-linked one.

### Market role, and the fact that this is a closed book

**Riester is closed.** The *Altersvorsorgereformgesetz* was approved by the **Bundesrat on 8 May
2026**, and the new state-subsidised private provision — whose central vehicle the Bundestag's own
text archive names the ***Altersvorsorgedepot*** — **starts on 1 January 2027**, replacing the
Riester-Rente for new business [REG-R44]. Existing contracts are grandfathered: provider-side
commentary discusses whether to let an existing Riester contract lie dormant or switch, which
implies that contractual rights survive [REG-R44]. The enactment date is contradictory across
summaries and neither the BGBl citation nor the promulgation date is established [REG-R44].

**That changes what this specification is.** It describes a product with a very large in-force
book whose contractual rights survive — exactly what a liability cash-flow model is for — and it is
why the reference implementation's anchor cell is an **in-force** contract at a 1 January 2027
valuation date rather than a new policy. The product research file, written without a research
channel, recorded the reform status as its most important open question (gap 1); [REG-R44] closes
it from the cross-product sweep, and this document follows [REG-R44].

**Scale.** Everything in this paragraph is `[unverified]` order-of-magnitude recollection: **no
market figure was established**, the official series was neither retrieved nor searched, and gap 2
qualifies all of it. Of the order of **15 to 16 million** certified Riester contracts existed in
the mid-2020s, having peaked near **16,5 million** in the late 2010s; insurance contracts are
roughly two thirds of the count, fund savings plans roughly a fifth, Wohn-Riester contracts a
little over a tenth and bank savings plans the remainder [R25]. **New business had effectively
stopped before the statute closed it**, dating from the 0,25 % *Höchstrechnungszins* regime of 2022
[R22] [REG-R15], when the three large fund houses withdrew their savings plans and a substantial
number of insurers followed. A large minority of the book — commonly reported at a fifth to a
quarter, three to four million contracts — is ***beitragsfrei gestellt***: in force, certified,
guaranteed on what was paid, and receiving nothing further [R25] [unverified]. There is **no
official statistic for that figure at all**, and it is nonetheless the most model-relevant market
fact here: ***Beitragsfreistellung*, not surrender, is this product's characteristic exit**, and a
model carrying only a lapse rate has mis-specified the book. Two counting warnings follow. A
contract counted as "Riester" in an official statistic **may be a mortgage** [R19] [S13]. And a
Riester annuity of a given gross amount is worth materially **less** to the saver than a Schicht-3
annuity of the same gross amount, because it is taxed in full [R12] rather than on the
*Ertragsanteil* [REG-R41].

---

## Representative specification

Every statutory row below is a fact about the product; every carrier row is **[std]**, because
nothing carrier-specific was established (gap 12). Amounts in prose use German number formatting
(`1 575,00 €`); amounts inside tables and code use `1,575.00`.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-life **klassische Riester-Rentenversicherung**: deferred general-account annuity, certified as an *Altersvorsorgevertrag*, participating (*Überschussbeteiligung*) | [R1] [R2] [S2] [REG-R43] |
| Legal wrapper | Individual insurance contract under the VVG; certification is an administrative act on the **tariff**, not on the policy | [R2] [S15] [REG-R22] [REG-R43] |
| Layer | **Schicht 2** — *Zusatzversorgung*, relieved in, taxed in full out | [R12] [R18] [REG-R38] |
| Eligibility (a saver attribute, not a policy attribute) | *unmittelbar zulageberechtigt* — compulsorily insured in the *gesetzliche Rentenversicherung*, *Beamte* and equivalent office-holders, farmers, *Arbeitslosengeld* recipients, parents in *Kindererziehungszeiten*, full *Erwerbsminderungs-* and *Dienstunfähigkeitsrentner*, and *geringfügig Beschäftigte* who waived the exemption. *mittelbar* — the spouse of an eligible person, holding an **own** certified contract and paying the *Sockelbeitrag* | [R7] [R10] [R20] [REG-R42] `[unverified]` |
| Not eligible | The self-employed outside compulsory insurance, and members of the *berufsständische Versorgungswerke* — who are directed to the **Basisrente** instead. The two subsidised products are **complements addressed to different people, not competitors** | [R7] [REG-R42] |
| Entry ages | 16 to the low sixties in practice; no statutory ceiling, but the accumulation must end at or after the earliest payout age | envelope **[std]** (1) |
| Earliest start of the payout phase | Completed **62nd** year of life for contracts concluded from **1 January 2012**; completed **60th** before that date. The alternative trigger is the start of an old-age pension from a statutory scheme | [R1] [REG-R43] `[unverified]` |
| Representative *Rentenbeginn* | Attained age **67**, at or near the statutory retirement age | **[std]** (2) |
| Sex as a rating factor | **Prohibited.** Riester contracts have been **unisex** since **1 January 2006** — six years before *Test-Achats* reached the general German market on 21 December 2012 | [R1] [R23] [REG-R34] `[unverified]` on the 2006 date |
| Lives basis | Single life. A survivor's benefit is a rider, not a second life in the base design | [R1] [S16] |
| Benefit form | **Lifelong** *Leibrente* with **constant or rising** monthly payments. A falling annuity is not certifiable; nor is a pure drawdown with no lifelong element | [R1] [REG-R43] |
| Alternative payout topology | *Auszahlungsplan* with *Restverrentung* from at the latest the **85th** year of life — the fund and bank chassis's form, **not implemented here** | [R1] [REG-R43] `[unverified]` |
| New business | **Closed from 1 January 2027**; in-force contracts grandfathered | [REG-R44] |
| Anchor model cell | In force at 1 January 2027: female, entry age 47 in 2024, attained age 50, duration 3, *Rentenbeginn* 67, *Rechnungszins* 0,25 %, one child born 2010, full *Mindesteigenbeitrag*, 30 % *Teilkapitalauszahlung*, 10-year *Rentengarantiezeit* | **[std]** (3) |

Footnotes to **[std]** rows:

1. No entry-age envelope was established at any carrier (gap 12). Nothing statutory bounds it
   below; the arithmetic bounds it above, since at 0,25 % a short remaining term leaves almost no
   room for charges — so late entry is real but structurally hostile, and the model point table
   carries one.
2. German practice sets *Rentenbeginn* at or near the statutory retirement age [unverified].
   Whether any statutory **upper** bound applies to the start of the payout phase, as distinct from
   the age-85 bound on the *Restverrentung*, was **not established** (gap 10).
3. The anchor is an **in-force** cell for three reasons. The product is closed to new business from
   1 January 2027 [REG-R44], so an in-force cell is what the book contains. A **2024-vintage**
   tariff carries a *Rechnungszins* of **0,25 %** [R22] [REG-R15], the regime the whole guarantee
   argument turns on. And at duration 3 the contract is still inside the statutory **five-year**
   acquisition-cost spreading window [R1], so the anchor exercises the AltZertG charge rule rather
   than only describing it. Model point 2 is the *same contract projected from its own inception*,
   which reconciles the anchor's opening balances.

### Contributions

The contribution is the product's most distinctive mechanic and the one a foreign reader is most
likely to get wrong: **it is not a premium the insurer sets. It is a statutory minimum the saver
must reach to draw the subsidy, computed from the saver's own income, and the Zulagen are
subtracted from it.**

| Parameter | Representative value | Basis |
|---|---|---|
| *Mindesteigenbeitrag* | `min(4 % × previous calendar year's beitragspflichtige Einnahmen, 2 100 €) − Zulagenanspruch`, floored at the *Sockelbeitrag* | [R10] [REG-R42] `[unverified]` on all three inputs |
| Percentage | **4 %**, from contribution year 2008. Phased in at 1 % (2002–03), 2 % (2004–05), 3 % (2006–07) | [R10] [R17] `[unverified]` |
| Cap on the base | **2 100 €** — the same ceiling as the § 10a *Sonderausgabenabzug*, and **not raised since 2008** | [R6] [R10] [REG-R42] `[unverified]` |
| *Sockelbeitrag* | **60 €** per year | [R10] [REG-R42] `[unverified]` |
| Reference income | The **previous** calendar year's — so the entitlement for contribution year `t` is a function of income in `t − 1` | [R10] [REG-R42] |
| Under-payment | **Proportional, not a cliff.** Pay half the *Mindesteigenbeitrag* and receive **half** the Zulagen | [R10] [REG-R42] |
| Contribution form (model-point parameter) | (i) `mindest` — the § 86 amount recomputed every year; (ii) `fixed` — a level contractual contribution the saver chose, varied at will | (i) [R10]; (ii) practice [unverified]; both **[std]** (4) |
| Payment frequency | Annual, half-yearly, quarterly or monthly, normally by SEPA direct debit | practice [unverified]; loading **[std]** (5) |
| Fractionation loading | Annual 1.0000; half-yearly 1.0100; quarterly 1.0200; monthly 1.0300 | **[std]** (5) |
| Contribution movements | Three are routine and all three must be representable: an increase restoring the *Mindesteigenbeitrag* after a pay rise; a reduction to the *Sockelbeitrag*; and a complete stop (*Beitragsfreistellung*) | [R10] [R14] [REG-R28] |
| Unsubsidised contributions | Money paid **above** the § 10a ceiling, or in a year of ineligibility, may be paid into the same contract. It enters the account **and the guarantee**, draws **no** Zulage, and is taxed on the *Ertragsanteil* rather than in full | [R12] [REG-R41] |

4. `mindest` is the statutory arithmetic and is the base case. `fixed` is retained because German
   Riester insurance tariffs are in practice written with a nominal level annual or monthly
   contribution and a wide right to vary it [unverified], and because the *mittelbar* eligible
   spouse's contract is a **60 € flat contribution drawing a 175 € Grundzulage** [R7] [R10]
   [REG-R42] — an economically extreme part of the book whose omission would leave the model point
   table unrepresentative. Neither form was established at any carrier.
5. **No fractionation scale was established anywhere in this corpus** (gap 13). German life tariffs
   levy a *Ratenzuschlag* for sub-annual payment; the scale above is a round-number placeholder,
   and the reference implementation treats the loading as a **charge** rather than as money
   credited to the account, so raising it never enlarges the guarantee.

**Worked cases of the § 86 arithmetic**, at the 2018-and-later rates. All rows are `[std] derived`
— exact arithmetic on the [R9] and [R10] inputs, shown so that a reader can redo them:

| Case | Prior-year income | Zulagen | 4 % of income | *Mindesteigenbeitrag* | *Eigenbeitrag* paid | Total into the contract | Zulage share |
|---|---|---|---|---|---|---|---|
| A — single, no children | 40,000.00 | 175.00 | 1,600.00 | 1,425.00 | 1,425.00 | 1,600.00 | 10.94 % |
| B — single, at the cap | 60,000.00 | 175.00 | 2,400.00 → 2,100.00 | 1,925.00 | 1,925.00 | 2,100.00 | 8.33 % |
| C — one child born 2010 | 30,000.00 | 475.00 | 1,200.00 | 725.00 | 725.00 | 1,200.00 | 39.58 % |
| D — two children born from 2008 | 20,000.00 | 775.00 | 800.00 | 25.00 → floor 60.00 | 60.00 | 835.00 | 92.81 % |
| E — *mittelbar* eligible spouse | not applicable | 175.00 | not applicable | 60.00 | 60.00 | 235.00 | 74.47 % |

Three consequences, each of which the model must reproduce and a test must assert. **At the
*Mindesteigenbeitrag* the Zulagen do not raise the amount invested; they lower the amount the saver
pays** — the total into the contract is `min(4 % × income, 2 100 €)` and the Zulagen are a
**substitute** for the saver's own money, which is the single most misunderstood feature of the
product. **The *Sockelbeitrag* stops binding at an income of `(60 € + Zulagen) / 4 %`**
`[std] derived`: **5 875 €** for a childless single, **10 500 €** with one pre-2008 child,
**13 375 €** with one post-2008 child, **20 875 €** with two post-2008 children; below those
incomes the contribution is a flat 60 € plus the Zulagen and does not vary with income at all. Case
D is the product's political case and its actuarial oddity at once — a household paying **60,00 €**
of its own money draws **775,00 €** of Zulagen, a multiple of **12,92×** `[std] derived`. And **the
ceiling binds at `2 100 € / 4 % = 52 500 €`** `[std] derived`, above which the total contribution
is frozen regardless of earnings, so the product's subsidy value falls monotonically with income.

### The Zulagen

All amounts `[unverified]`: no search corroborated any of them; they are stated from general
knowledge of §§ 84 and 85 EStG [R9] and are corroborated at one remove by the cross-product
reference library's own second-hand entry [REG-R42], which reports the same figures.

| Component | Amount per year | From | Condition |
|---|---|---|---|
| *Grundzulage* | **175.00** | contribution year 2018 | one per eligible saver, own contract |
| *Grundzulage*, previous level | 154.00 | 2008–2017 | raised by the *Betriebsrentenstärkungsgesetz* [R21] |
| *Grundzulage*, phase-in | 38.00 / 76.00 / 114.00 | 2002–03 / 2004–05 / 2006–07 | [R17] |
| *Berufseinsteiger-Bonus* | **200.00**, **once in a lifetime** | contribution year 2008 | *unmittelbar* eligible, 25th year of life not completed at the start of the contribution year, first year a Zulage is claimed |
| *Kinderzulage*, child born **before** 1 Jan 2008 | **185.00** | 2008 | per child, while *Kindergeld* is drawn |
| *Kinderzulage*, child born **from** 1 Jan 2008 | **300.00** | 2008 | per child, while *Kindergeld* is drawn |
| *Kinderzulage*, phase-in | 46.00 / 92.00 / 138.00 | 2002–03 / 2004–05 / 2006–07 | [R17] |

**The two *Kinderzulage* rates are a permanent birth-cohort split, not a transition** [R9] [R19]:
a household with a child born in 2006 and one born in 2009 draws 185,00 € and 300,00 €
simultaneously, and a model treating the *Kinderzulage* as a single rate misprices every family
model point that straddles the 2008 boundary. It is **credited to the mother's contract** unless
the parents jointly elect otherwise `[unverified]` [R9] [REG-R42], and it **stops when *Kindergeld*
stops** — normally at the child's 18th birthday, later during education `[unverified]`. So the
Zulage stream on a family contract is a **step function that falls**, typically two or three times
over a contract running thirty or forty years, driven by a household variable the insurance
contract does not observe. That is the most awkward fact in the whole product for a per-policy
projection, and it is why the reference implementation carries the Zulage entitlement as an
**external schedule keyed by model point and projection year** rather than as a scalar.

**The Zulage arrives late.** The saver applies through the provider, normally once, by a
*Dauerzulageantrag*; the ZfA matches the provider's contribution data against the pension
insurance's earnings and *Kindergeld* data and **pays the provider**, who credits the contract
[R11]. The Zulage for contribution year `t` is therefore a cash inflow in a **later** period,
conventionally `t + 1` [REG-R42], and it is **provisional** until the data match settles — where
entitlement later proves wrong the ZfA reclaims and the provider debits the contract. Neither the
payment month nor the reversal frequency is established (gap 6).

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| **Beitragsgarantie** | At the beginning of the payout phase, the capital available for the benefit is **at least the sum of the *Altersvorsorgebeiträge* paid in** — own contributions **plus** Zulagen credited | [R1] [REG-R43] |
| Guarantee carve-out | Contributions securing *Erwerbsminderung*, *Berufsunfähigkeit* or *Hinterbliebene* are left out of account, up to **20 % of total contributions** | [REG-R43] |
| What the guarantee is **not** | Not a value at any other date; not a floor on the surrender value; not preserved in real terms; not a guarantee of the *annuity*, only of the *capital*; and not extended to the rider premiums | [R1]; see *Contractual mechanics* |
| Conversion capital | `max( Deckungskapital + Überschussguthaben + Schlussüberschussanteil + Bewertungsreserven-Anteil , Σ Eigenbeiträge + Σ Zulagen − carve-out )` | [R1]; which surplus components count **[std]** (6) |
| *Teilkapitalauszahlung* | Up to **30 %** of the capital available at the start of the payout phase, as a lump sum, **without** *schädliche Verwendung*. The remainder must be annuitised | [R1] [REG-R43] `[unverified]` on the percentage |
| Representative election | **30 %** taken | **[std]** (7) |
| Annuity | Lifelong monthly *Leibrente*, paid **monthly in advance**, constant or rising | [R1]; monthly-in-advance `[unverified]` |
| Conversion basis | The **guaranteed *Rentenfaktor*** struck at inception is compared at *Rentenbeginn* with the carrier's then-current factor, and the **higher** applies | construction documented for the German Schicht-3 market in a sibling `delib` file; **not established for any Riester tariff** — **[std]** (8), gap 9 |
| *Rentenfaktor* definition | Euros of **monthly** annuity per **10 000 €** of capital converted | [REG-R43-adjacent market usage]; level **[std]** (8) |
| Mortality basis for the annuity | The German annuitant table family — **DAV 2004 R**, generational, in its unisex application. **Proprietary, not public, not redistributed here** | [R21-adjacent]; [REG-R47] [REG-R49]; proxy **[std]** (9) |
| *Rentengarantiezeit* | Permitted and common; compatible with the "constant or rising" requirement, and the *förderunschädliche* route for an early death in payment | [R1] [R14] |
| Representative *Rentengarantiezeit* | **10 years** | **[std]** (10) |
| Surplus in payment | Permitted, but the AltZertG's **constant-or-rising** requirement constrains which surplus system a Riester contract may use: a system whose declared component can be reduced would make the total annuity fall | [R1]; legal reading `[unverified]` |
| Representative surplus in payment | **None in the base run** — a constant annuity | **[std]** (10) |
| Death before *Rentenbeginn* | The accumulated capital. Transfer to a **surviving spouse's own certified contract** is *förderunschädlich*; payment to any other heir is *schädlich* and the *Rückzahlungsbetrag* is deducted before payment | [R14]; benefit design `[unverified]`; **[std]** (11) |
| Death after *Rentenbeginn* | Continuation to a spouse under a survivor's option, or payments for the remainder of a *Rentengarantiezeit*. A lump-sum death benefit outside those forms is **not certifiable** | [R1] [R14] |
| *Kleinbetragsrente* | Where the monthly annuity would not exceed a percentage of the *monatliche Bezugsgröße* of § 18 SGB IV, the provider may commute the whole capital to a lump sum **without** *schädliche Verwendung*, taxed under the *Fünftelregelung* of § 34 EStG since 2018 | [R15] [R21] [REG-R42] |
| *Kleinbetragsrente* threshold | **1 % of the monthly Bezugsgröße — 39,55 € per month on a 2026 figure of 3 955 €**. A competing account gives **1,5 % from June 2026 — 59,33 €**. They cannot both be right | [REG-R42] [REG-R46] `[unverified]`; choice **[std]** (12), gap 7 |

6. **Which surplus components may be counted toward satisfying the *Beitragsgarantie* was not
   established for any Riester tariff** (gap 9), and in particular whether a
   *Schlussüberschussanteil* — declared at *Rentenbeginn* and not a vested balance before it — may
   be used to close a shortfall. The reference implementation **counts all of them**, which is the
   provider-favourable reading, and says so. The alternative — counting only the vested
   *Deckungskapital* and *Überschussguthaben* — raises the projected guarantee cost, and the
   technical notes carry it as a named sensitivity rather than leaving it implicit.
7. German consumer commentary reports the 30 % lump sum as the usual choice `[unverified]`, and
   **gap 10 records that this rests on nothing**. 30 % is adopted for the anchor because it
   exercises the option at its statutory maximum and because the decision is genuinely non-obvious:
   the lump sum is taxed **in full in the year it is paid, with no *Fünftelregelung***, which is
   available only for the *Kleinbetragsrenten-Abfindung* [R12] [R15]. Model point 12 takes none.
8. **No *Rentenfaktor* level, at any carrier, for any year, was established** (gap 9), so both the
   guaranteed factor and the construction that compares it with the current one are **[std]**. The
   sibling `delib` Schicht-3 file establishes the two-factor construction for the German market
   from that session's searches, and for one house that a guaranteed factor is computed on a
   recognised mortality table and a stated interest basis — that basis being **0 % per annum**,
   which is the *Sicherheitsabschlag* made concrete. Whether Riester tariffs use the same
   construction is the natural expectation and is not established.
9. The DAV tables are the property of the *Deutsche Aktuarvereinigung*, distributed to members and
   licensees rather than published, and **not redistributable**. `delib` ships none of them and
   quotes no `q(x)` from any of them [REG-R47] [REG-R49]. The shipped table is a **[std] proxy**
   anchored so the worked example reproduces exactly. The one structural property that is not
   optional is that the annuity basis is a ***Generationentafel*** — two-dimensional in attained
   age and calendar year — because a period-table proxy priced at an annuitisation twenty years out
   understates the liability by a margin that dwarfs every other assumption in the model [REG-R49].
10. No *Rentengarantiezeit* length and no payout-phase surplus system was established at any
    carrier (gaps 11, 12); ten years is the common German market length `[unverified]`. A constant
    annuity is the base run because the AltZertG constrains which surplus systems are available
    [R1]; model point 12 switches the guarantee period off, making its effect testable by
    difference.
11. The corpus establishes three death-benefit designs for the German deferred-annuity chassis —
    *Beitragsrückgewähr*, payment of the accumulated capital, and a *Hinterbliebenenrente* — and
    does not establish which a Riester tariff uses. The composite pays **the accumulated capital**,
    because the *Beitragsgarantie* is tested **only at *Rentenbeginn*** [R1] and importing it into
    the death benefit would create a guarantee the statute does not require.
12. The two readings of the *Kleinbetragsrente* threshold are irreconcilable and both are recorded
    [REG-R42]. The composite takes **1 %, 39,55 € per month** and prints the alternative, because
    it is the **lower** trigger: fewer contracts commute, more of the book stays a lifelong annuity,
    and the projected liability is the longer-tailed and therefore more prudent. Whether commutation
    is the provider's right, the saver's right or automatic **was not established at any carrier**
    (gap 7); the composite makes it the provider's and exercises it whenever the test trips.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence for the savings contract | **None.** A deferred annuity with a death benefit equal to the accumulated capital carries no positive sum at risk, so there is nothing to underwrite | design consequence; **[std]** |
| Health evidence for a rider | A *Berufsunfähigkeits-Zusatzversicherung* or a survivor's benefit is separately underwritten on the rider's own basis | [REG-R29]; rider inventory not established (gap 11) |
| Rating factors | **Entry age and *Rentenbeginn* only.** Sex may not be used [R23] [REG-R34]; smoker status, occupation and health do not enter a savings tariff | [R1] [R23] |
| Eligibility check | Performed by the **ZfA**, not by the insurer: the provider transmits contribution data and the ZfA determines entitlement against the pension insurance's earnings data | [R11] |
| Consequence of losing eligibility | **Nothing happens to the contract.** Contributions may continue, but they are **unsubsidised** and fall into the second tax pool | [R7] [R12] |
| *Rechnungszins* | Chosen by the carrier at or below the *Höchstrechnungszins* in force at conclusion: **0,25 %** from 1 January 2022, **1,00 %** from 1 January 2025 | [R22] [REG-R14] [REG-R15]; carrier's own choice not established (gap 12) |
| Representative *Rechnungszins* | **0,25 %** for the anchor (a 2024-vintage tariff) | **[std]** (13) |

13. The *Höchstrechnungszins* is a **cap on the reserving rate**, not the rate a policy guarantees
    [REG-R14] — a tariff may guarantee less. Nothing was established about any carrier's own
    choice, so the composite uses the cap in force at the tariff's vintage, which is the highest
    defensible value and therefore the one that makes the guarantee **cheapest**; a lower tariff
    rate widens the *Garantielücke*, and the technical notes carry that direction explicitly.

### Charges

**No charge figure exists anywhere in this corpus** (gap 13). The single number inherited from a
sibling `delib` session — total costs relative to the capital formed of at most **0,95 € per
100 €** in an Allianz *RiesterRente* variant, from a third-party analysis of a specimen quotation
[S5] — is `[unverified]`, is not from a tariff sheet, and is not enough to found a charge basis.
An *Abschlussprovision* of **1 575 €** appears in the same commentary but on a *BasisRente*
specimen, not a Riester one [S5]. **Every charge below is [std].**

| Parameter | Representative value | Basis |
|---|---|---|
| Acquisition and distribution costs | Must be **spread over at least five years** — the statutory cap on *Zillmerung* aimed at this product specifically, and materially tighter than anything the VVG imposes on a Schicht-3 contract | [R1] [REG-R43] `[unverified]` on the period |
| *Höchstzillmersatz* | **25 ‰** of the *Beitragssumme* under § 4 DeckRV since 1 January 2015 | [REG-R16] |
| Representative acquisition charge | **2,5 % of the *Beitragssumme*, levied in five equal instalments in contract years 1 to 5** | **[std]** (14) |
| Administration charge on contributions | **4,0 %** of each contribution credited | **[std]** (14) |
| Fixed policy fee | **12,00 € per year**, deducted from the *Sparbeitrag* while contributions are paid and from the *Deckungskapital* while the contract is *beitragsfrei* | **[std]** (14) |
| Charge base for the **Zulagen** | The Zulagen are charged **on the same basis as the *Eigenbeitrag*** | **[std]** (15), gap 14 |
| *Risikobeitrag* | **Zero.** The death benefit is the account value, so the sum at risk is nil by construction | design consequence; **[std]** (16) |
| Payout-phase loading | Carried **inside the *Rentenfaktor*** as a margin of **30 %** on the actuarially fair factor, not as a separate deduction from each annuity payment | **[std]** (17) |
| *Stornoabzug* on surrender | **2,0 %** of the account value | [REG-R28] permits an agreed and appropriate deduction; level **[std]** (14) |
| Transfer charge on an *Anbieterwechsel* | **50,00 €**, a fixed euro amount | [R1] [R20] cap the charge; the cap's level was **not established** (gap 8) — **[std]** (14) |
| Disclosed cost measure | ***Effektivkosten*** — the reduction in yield, computed **individually for each contract offer**, on the statutory *Produktinformationsblatt* | [R4] [R5] [S14] [REG-R43]; **no value established** (gap 13) |
| Risk/return class | ***Chancen-Risiko-Klasse*** 1 to 5, assigned by the *Produktinformationsstelle Altersvorsorge* from a common stochastic model the insurer does not control | [R4] [S14] [REG-R43]; **not implemented, not reproducible** (18) |

14. Round-number placeholders; **no observed range exists for any of them**. The acquisition rate
    is set at the § 4 DeckRV cap [REG-R16], which is a **cap and not a level**, on the argument
    that what binds this product is not the *Höchstzillmersatz* but the AltZertG's five-year
    spreading [R1] — so a tariff that zillmers to the cap and then spreads it is the honest worst
    case for the policyholder and the clearest demonstration of the rule.
15. **The charge base for the Zulagen is unknown** (gap 14) and it matters more than it looks: in
    the low-income cases of the § 86 table the Zulagen are the **majority** of the contribution, so
    charging them or not moves the account value by tens of per cent on exactly the model points
    the product was designed for. The composite charges them and says so; the technical notes carry
    a pitfall for the alternative rather than letting the choice be inferred from a formula.
16. A real product fact, not a simplification: with a death benefit equal to the accumulated
    capital there is no positive sum at risk in the accumulation phase and therefore no
    *Risikobeitrag* [REG-R47]. A *Beitragsrückgewähr* floor **would** create one, which is one
    reason the composite does not adopt it (footnote 11).
17. German market *Rentenfaktoren* sit materially below the actuarially fair factor implied by any
    plausible annuitant basis, because they carry the *Sicherheitsabschlag* of a guarantee given
    decades ahead **and** the payout phase's cost loading. Deducting a percentage from each annuity
    payment **and** applying a conservative factor double-counts, so the composite puts the whole
    loading in one place — the factor — and takes the insurer's real payout-phase administration as
    a per-policy expense cash flow.
18. The *Produktinformationsblatt* regime has **no counterpart in `uslib`, `uklib`, `jplib` or
    `frlib`**: a public body assigns a risk class using a stochastic model the provider does not
    control [REG-R43]. `delib` does not implement the PIA simulation. A specification may **report**
    a published CRK and *Effektivkosten* as [S#] facts; reproducing either needs the PIA's scenario
    set, which is neither public nor in scope.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| ***Beitragsfreistellung*** | Contributions stop, the contract stays in force and stays certified, the guarantee stands on what was paid, no further Zulagen arrive, and **no subsidy is repaid**. § 165 VVG gives the right generally | [R14] [REG-R28] |
| ***Anbieterwechsel*** | A **statutory** right: terminate and have the accumulated capital transferred directly to another certified contract. **Not** a *schädliche Verwendung*, no tax consequence | [R1] [R14] [REG-R43] |
| Notice period and transfer-charge cap | Stated as a period to a quarter end, with the ceding provider's charge capped at a fixed euro amount — **neither established** (gap 8) | [R1] [R20] `[unverified]` |
| ***Kündigung*** with payment of the *Rückkaufswert* | Permitted by the VVG and punished by the EStG: the saver receives the surrender value **less** the *Rückzahlungsbetrag* — **all** Zulagen credited and **all** § 10a relief granted — and the growth on the subsidised part becomes taxable | [R14] [REG-R28] [REG-R42] |
| *Rückkaufswert* floor | § 169 VVG floors the surrender value at the *Deckungskapital* computed with acquisition and distribution costs spread evenly over the **first five contract years** | [REG-R28] |
| Interaction worth naming | The AltZertG's own five-year spreading [R1] means the § 169 VVG floor is **satisfied by construction** on a certified contract: the statutory product rule has already done what the contract-law rule would have had to force | [R1] [REG-R28] |
| Early-duration reality | The surrender value can be, and in the early years of a charged contract usually **is**, **below** the contributions paid. The *Beitragsgarantie* does not floor it — it is tested **once**, at *Rentenbeginn* | [R1] |
| *Versorgungsausgleich* on divorce | Internal or external division, transfer to the other spouse's certified contract, *förderunschädlich* | [R14] `[unverified]` |
| Wohn-Riester withdrawal | An *Altersvorsorge-Eigenheimbetrag* is *förderunschädlich* and, from the insurer's side, an early and complete exit terminating the annuity liability. **Not implemented** | [R13] [R19] |
| Non-transferability | The Zulage entitlement and the subsidised capital are **not assignable** and are protected from attachment — so the contract cannot be pledged as loan collateral, a use a Schicht-3 endowment has | [R16] [REG-R40] `[unverified]` |
| Emigration | § 95 EStG historically triggered repayment on the end of unlimited tax liability; the rule was challenged under EU free-movement law and amended. **The judgment, the amending statute, the date and the current rule are all unknown** and nothing about a saver moving abroad may be asserted | [R14]; gap 15 |

---

## Contractual mechanics

Each subsection states an operative rule and what it does to the projection.

### Eligibility is annual, and it is an attribute of the saver

A saver can be *unmittelbar* eligible in one year, *mittelbar* in the next and not eligible at all
in a third, **without the contract changing** [R7]. Nothing happens to the policy when eligibility
lapses: contributions may continue, they are simply unsubsidised, and they move into the second tax
pool [R12]. The rule that decides the whole subsidy stream is therefore a property of the
**person**, not of the contract, and one the insurer does not itself observe — the ZfA does [R11].
The reference implementation carries eligibility as a per-period flag on an external schedule,
**[std]** default "*unmittelbar* eligible throughout", with a dedicated model point exercising a
mid-term lapse.

### The *Mindesteigenbeitrag*, and the proportional Kürzung

The operative rule [R10] [REG-R42], written as the model implements it:

    mindesteigenbeitrag(t) = max( 60 € ,
                                  min( 4 % × income(t − 1), 2 100 € ) − zulage_entitlement(t) )
    eigenbeitrag(t)        = contrib_ratio × mindesteigenbeitrag(t)
    zulage_granted(t)      = zulage_entitlement(t) × min( 1, contrib_ratio )

Three features of the statute drive behaviour and each is a distinct way to get the model wrong.
The base is the **previous** calendar year's contribution-liable earnings, so the entitlement for
contribution year `t` looks back one year. The **Zulage is subtracted** from the base, so a larger
subsidy reduces the saver's own payment rather than increasing what the contract receives. And the
sanction for under-payment is **proportional, not a cliff**: the Zulage is reduced in the ratio of
the contribution actually paid to the *Mindesteigenbeitrag*, so an implementation that treats the
minimum as all-or-nothing produces a discontinuity that does not exist in the statute — and the
German book is full of the paths that discontinuity would misprice [R10] [REG-R42].

### The one-year Zulage lag, and the second lag behind it

**Two distinct lags run in the subsidy chain and they are easy to collapse into one.** The
entitlement for contribution year `t` is computed from income in `t − 1` [R10]; the **cash** for
contribution year `t` arrives from the ZfA in `t + 1` [R11] [REG-R42]. The reference implementation
carries both explicitly: `income_ref(t) = income(t − 1)` for the entitlement, and
`zulage_credited(t) = zulage_granted(t − 1)` for the cash. The **[std]** one-year cash lag has a
stated rationale — [R11] establishes that the ZfA pays the provider and that the application
deadline runs to the end of the **second** calendar year after the contribution year, but not
**when in the following year** the money arrives (gap 6).

One consequence is load-bearing and is a numbered pitfall: **the Zulage for the final contribution
year arrives after contributions have stopped**, landing in the conversion year itself, where it
must be credited, counted in the guarantee and included in the conversion capital **before** the
guarantee is tested. An implementation that stops the Zulage stream when it stops the contribution
stream silently drops a full year's subsidy out of both.

### The § 10a *Sonderausgabenabzug* and the *Günstigerprüfung* — and why neither is a cash flow

Contributions **together with the Zulagen credited** are deductible as *Sonderausgaben* up to
**2 100 € a year** [R6] [REG-R42] `[unverified]`. The tax office performs the
***Günstigerprüfung*** of its own motion, granting the deduction only where it beats the Zulagen
entitlement and adding the Zulagen back to the assessed tax so that the saver receives the
**larger** of the two benefits and not their sum [R6] `[unverified]` on the precise expression.

**Only the Zulage is a contract cash flow. The *Günstigerprüfung* top-up is a personal tax refund
and never touches the policy** [REG-R42]. That distinction is the single most important thing a
model author must get right about the subsidy: the model publishes `zulagen` as a column of the
cash flow statement and publishes nothing at all for the § 10a route. The Zulagen route dominates
for low incomes and households with children, the § 10a route for high incomes with no children;
**the crossover was not established** and no crossover figure appears anywhere in this library
(gap 5). A *mittelbar* eligible spouse has no § 10a deduction of their own [R6] [R7]
`[unverified]`. The deduction reaches the projection in one indirect way only: it is part of what
is repaid on a *schädliche Verwendung* [R14], and therefore part of the reason a Riester lapse
assumption should sit materially **below** a Schicht-3 one.

### The 100 % *Beitragsgarantie*

**What is guaranteed** is that at the beginning of the payout phase the capital available for the
benefit is at least the sum of the *Altersvorsorgebeiträge* paid in — own contributions **plus**
Zulagen credited, less the biometric carve-out of up to 20 % of total contributions [R1]
[REG-R43]. In model terms it is a **running accumulator**, not a discounted quantity:

    guar(t + 1) = guar(t) + eigenbeitrag(t) + zulage(t) − carve_out(t),    guarantee frozen once
                                                                          contributions stop

and at *Rentenbeginn* the conversion capital is `max( account and its surplus components,
guar(T) )`. The excess of `guar(T)` over the account — the ***Garantielücke*** — is a **cost the
insurer bears out of its own funds**, and it is the product's signature output. A Riester model in
which the guarantee never binds on any model point has demonstrated nothing, which is why the model
point table carries a low-declared-rate cell on which it bites.

**Six things the guarantee is not**, each of them load-bearing:

- **Not a value at any other date.** It is tested **once**. Before *Rentenbeginn* the surrender
  value can be, and in the early years usually is, below the contributions paid.
- **Not a floor on surrender.** A saver who terminates for cash gets the *Rückkaufswert*, which the
  guarantee does not floor, **and** loses the subsidy [R14].
- **Not preserved on transfer.** A saver exercising the *Wechselrecht* transfers the capital as it
  stands; whether the guarantee survives is a design question of the **receiving** contract and is
  **not established** (gap 8). If the receiving contract's guarantee runs only on the transferred
  sum rather than on the original contributions, the *Wechselrecht* is materially less valuable
  than it appears, and this library cannot say which is right.
- **Not real.** It is **nominal**. Over a thirty-year contract at even moderate inflation the floor
  is worth a fraction of the contributions in real terms — the substance of the most serious
  criticism of the product's design.
- **Not a guarantee of the annuity.** It is on the **capital**; what that capital buys is a
  separate guarantee, the *garantierter Rentenfaktor*, and the two are routinely conflated.
- **Not extended to the risk-cover premiums**, within the statutory 20 % share [R1] [REG-R43] —
  which is why a Riester contract can carry a *Berufsunfähigkeits-Zusatzversicherung* without the
  guarantee reproducing its premiums, and why raising a rider premium must never enlarge it.

### Why the guarantee is the mechanical heart

The guarantee is a **nominal sum, due at a fixed future date, on money paid in over decades**, so
its cost is an interest-rate quantity and nothing else: **to guarantee one euro payable in `n`
years an insurer must immobilise `(1 + i)^−n` of it now**, where `i` is bounded by the
*Höchstrechnungszins* [R22] [REG-R14]. What is left, `1 − (1 + i)^−n`, is the entire budget for
risk assets **and** for every charge the contract will levy.

Stated on the whole contract: for level contributions in advance over `n` years the guaranteed
accumulation is `C × s̈(n, i)`, the guarantee is `C × n`, and the **headroom** is
`s̈(n, i)/n − 1`. All rows `[std] derived`, exact on the [R22] rates; the 0,90 %, 1,75 % and
2,25 % values and their effective dates are themselves `[unverified]` (gap 18):

| Term | 0,25 % (2022–24) | 0,90 % | 1,00 % (from 2025) | 1,75 % | 2,25 % |
|---|---|---|---|---|---|
| 12 years | **1.64 %** | 6.05 % | 6.74 % | 12.14 % | 15.90 % |
| 20 years | **2.67 %** | 10.01 % | 11.20 % | 20.58 % | 27.36 % |
| 30 years | **3.97 %** | 15.24 % | 17.11 % | 32.33 % | 43.82 % |
| 35 years | **4.63 %** | 17.98 % | 20.22 % | 38.76 % | 53.06 % |

On 1 200,00 € a year for thirty years — 36 000,00 € of contributions — the 0,25 % regime produces a
guaranteed accumulation of **37 429,31 €**, a headroom of **1 429,31 €**; the 1,00 % regime
produces **42 159,29 €**, a headroom of **6 159,29 €** `[std] derived`. So at 0,25 % a thirty-year
contract had **under 4 % of contributions** to pay for acquisition, administration, risk and any
margin — a multiple below typical German life charge levels, which made the guarantee not merely
expensive but **arithmetically unfinanceable** on a normally charged tariff. It bites hardest on
short terms and late money, so the product is structurally hostile to late entrants. It **dictates
the asset allocation** rather than leaving it to the provider, since the equity share is bounded
above by a headroom that is a function of `i` and `n` alone. And **a rate rise repairs it
mechanically**: the move to 1,00 % on 1 January 2025 roughly quadrupled the thirty-year headroom,
from 3,97 % to 17,11 % `[std] derived` — the arithmetic behind the GDV maintaining a 2025-vintage
classic Riester model wording [S2].

One warning about reading the table. It is the arithmetic of the **guaranteed** accumulation, which
is what the insurer must be able to promise. A **best-estimate** projection credits the declared
*laufende Verzinsung*, materially above the *Rechnungszins*, so on a healthy contract the
*Garantielücke* closes long before *Rentenbeginn*. **The guarantee's realised cost is a
declared-rate question, not a *Rechnungszins* question**, and a model that confuses the two reports
a guarantee cost of zero and concludes the mechanic does not matter.

### The five-year cost spreading

Acquisition and distribution costs must be **spread over at least five years** [R1] [REG-R43].
This is a statutory cap on *Zillmerung* aimed at this product specifically and is materially
tighter than anything the VVG imposes on a Schicht-3 contract; together with the *Wechselrecht* it
pushes a Riester tariff toward lower front-end charges and a thinner acquisition margin than a
comparable Schicht-3 tariff `[unverified]` as a market characterisation. Two model consequences.
The charge basis **cannot front-load the whole acquisition cost into year one**, which changes the
*shape* of the early-duration charge run-off and therefore of the early-duration surrender value.
And the **commission cash still leaves at issue** while the charge is recovered over five years —
the new-business strain is real and is carried by the insurer, not by the contract.

### *Rentenbeginn*: conversion, the lump sum and the *Rentenfaktor*

At the contractually fixed *Rentenbeginn*, bounded below by the statutory age [R1], four things
happen in order and the order matters. The **final Zulage** is credited. The **conversion capital**
is struck as the guarantee floor applied to the account's own parts. Up to **30 %** may be taken as
a ***Teilkapitalauszahlung*** [R1] [REG-R43]; it is taxed **in full in the year it is paid, with no
*Fünftelregelung*** [R12] [R15], and that asymmetry against the *Kleinbetragsrenten-Abfindung* is
why German consumer literature treats the decision as non-obvious. The **remainder is annuitised**
into a lifelong, constant-or-rising monthly *Leibrente* at the *Rentenfaktor*, the higher of the
guaranteed and the then-current factor applying:

    monthly_annuity = annuitised_capital / 10 000 € × Rentenfaktor

The Riester *Rentenfaktor* is **unisex from a 2006 vintage** [R23], earlier than the Schicht-3
market, so a Riester factor and a same-vintage Schicht-3 factor for a male life are **not
comparable** — a comparison German market commentary makes routinely and wrongly.

### The *Kleinbetragsrente*

Where the monthly annuity would not exceed the statutory threshold the provider may commute the
whole capital to a lump sum, **without** *schädliche Verwendung* [R15] [REG-R42]; the *Abfindung*
is taxable in full under § 22 Nr. 5 but, since 2018, under the ***Fünftelregelung*** of § 34 EStG,
with an election to have the payment made at the beginning of the following calendar year [R15]
[R21] `[unverified]`.

**This matters far more than the threshold suggests**, which is why the model carries it as a
switch on the anchor decrement rather than as a footnote. The book carries a long tail of small
contracts: those run at the *Sockelbeitrag* (§ 86 cases D and E above) and those that went *ruhend*
early. Case D contributes 835,00 € a year, so twenty years is **16 700,00 €** of contributions
`[std] derived`; case E contributes 235,00 €, so twenty years is **4 700,00 €**. At any plausible
*Rentenfaktor* both produce a monthly annuity in the tens of euros. **A material fraction of
Riester contracts will never pay an annuity at all.** One ordering question the statute does not
settle and the composite must: is the test applied to the annuity the **whole** conversion capital
would buy, or to the annuity payable after an elected *Teilkapitalauszahlung*? The composite tests
the **annuity actually payable**, on the argument that it is the annuity the provider would have to
administer, and prints the alternative; the choice is **[std]** and gap 7 records that neither
reading was established.

### Death, the *Rückzahlungsbetrag*, *Anbieterwechsel* and *Beitragsfreistellung*

Before *Rentenbeginn* the death benefit is the accumulated capital; the distinctive part is the
**subsidy treatment, not the benefit design** [R14]. Transfer to a **surviving spouse's own
certified contract** is *förderunschädlich*; payment to any other heir is *schädlich*, and the
*Rückzahlungsbetrag* — all Zulagen and all § 10a relief — is deducted before payment, with the
return on the subsidised part becoming taxable `[unverified]`. After *Rentenbeginn*, continuation
to a spouse or payments for the remainder of a *Rentengarantiezeit* are *förderunschädlich*; a
lump-sum death benefit outside those forms is not certifiable at all [R1]. **The model publishes
the death benefit gross**, because the *Rückzahlungsbetrag* is a deduction from what the
beneficiary receives and not a change in the insurer's obligation — the provider withholds and
remits it to the ZfA — so netting it inside the liability stream would understate the outgo and
confuse a tax collection with a benefit. The same applies to a surrender. The model does publish
the **cumulative Zulagen credited** as a diagnostic, which is the ZfA-reclaimable limb; the § 10a
limb depends on the saver's marginal rate and cannot be computed from contract data at all.

***Anbieterwechsel*** is a **statutory portability right with no Schicht-3 analogue**: terminate
and have the accumulated capital transferred directly to another certified contract, with no
*schädliche Verwendung* and no tax consequence [R1] [R14] [REG-R43]. Its cash-flow consequence is
that a Riester "lapse" is frequently a **transfer out at full value** rather than a surrender — for
the ceding insurer a full-value exit with no *Stornoabzug*, and for the model a **distinct
decrement** that must not be collapsed into the lapse rate. The notice period and the
transfer-charge cap were not established (gap 8).

***Beitragsfreistellung*** leaves the contract in force. § 165 VVG gives the right generally
[REG-R28]; the Riester overlay is that the contract stays **certified**, the guarantee stands on
what was paid, no further Zulagen arrive, and **no subsidy is repaid** [R14]. It is a **state
change, not a termination**: the guarantee accumulator freezes, the Zulage stream stops, the
account keeps rolling and the fixed policy charges keep biting. Against a surrender value already
below contributions in the early years, and a *Rückzahlungsbetrag* on the way out, that is why the
German book shows *Beitragsfreistellung* where another market would show surrender [R14] [R16].

### The two contribution pools

A single Riester contract can hold **subsidised** and **unsubsidised** contributions at once
[R12]. *Geförderte Beiträge* — own contributions up to the § 10a ceiling that attracted a Zulage or
a deduction, plus the Zulagen — are taxed **in full** on the way out. *Ungeförderte Beiträge* —
anything above the ceiling, or paid in a year of ineligibility — are taxed on the *Ertragsanteil*
for an annuity, or under § 20 Abs. 1 Nr. 6 for a lump sum [R12] [REG-R41] [REG-R45]. The provider
must track the two pools **and their investment return** separately for the life of the contract
and apportion every benefit between them in the annual *Leistungsmitteilung* `[unverified]`.

**Both pools count for the *Beitragsgarantie***: the guarantee is on the *Altersvorsorgebeiträge*
paid in and does not distinguish subsidised from unsubsidised money [R1] `[unverified]`. That is the
natural place for an implementer to go wrong and it is a numbered pitfall.

---

## Riders and options

**In scope, modelled or parameterized.** The ***Teilkapitalauszahlung***, a single lump-sum
election at one date, capped at 30 % [R1]. The ***Kleinbetragsrenten-Abfindung***, a switch on the
anchor decrement whose trigger the model computes rather than assumes [R15]. The
***Rentengarantiezeit***, which changes the payment obligation but not the annuity amount and is
the *förderunschädliche* route for an early death in payment [R1] [R14]. The
***Anbieterwechsel***, a full-value exit decrement distinct from surrender [R1].
***Beitragsfreistellung***, carried as a per-model-point switch on the year contributions stop.
**Unsubsidised over-ceiling contributions**, proving the two-pool split is representable. And a
**biometric rider premium**, carried **only** for its effect on the guarantee — the carve-out
capped at 20 % of total contributions [REG-R43].

**Out of scope, and why.** The ***Berufsunfähigkeits-Zusatzversicherung*** itself: its liability is
`products/berufsunfaehigkeit/`'s, its premium is not a cash flow of this model, and this model
carries only the statutory carve-out that premium creates. The **survivor's annuity** rider, which
needs a second life and has its own GDV condition set [S3]. The ***Auszahlungsplan mit
Restverrentung***, the fund and bank chassis's payout topology [S9]–[S12] — worth naming because it
is why a Riester fund savings plan still ends in an insurance annuity: **the insurance industry
receives the *Restverrentung* capital of the fund industry's contracts**. ***Wohn-Riester*** in
both limbs [R13] [R19] [S13], because the *Wohnförderkonto* is a notional tax memorandum carrying
**no cash whatsoever** and the certified *Darlehen* is a banking liability; what the model could
have represented and deliberately does not is the *Eigenheimbetrag* **withdrawal**, which from the
insurer's side is an early and complete exit at full value. And **surplus in payment**, because the
constant-or-rising requirement constrains which systems are available [R1] and no declaration level
was established.

---

## Variations across insurers

**No carrier-specific parameter was established for any Riester product, at any house, for any
year** (gap 12). That is stated first so that no reader takes a silence for a value. But the reason
the carrier table is empty is not only the failed research: **this product varies across carriers
far less than any other in `delib`**, because most of what a French *temporaire décès* leaves to
the insurer, German statute fixes for everyone.

### The observed range, parameter by parameter

| Parameter | Set by | Observed variation |
|---|---|---|
| Zulagen amounts; eligibility; *Mindesteigenbeitrag*; *Sockelbeitrag*; the proportional Kürzung | statute [R9] [R10] [REG-R42] | **none — identical for every provider and every chassis** |
| § 10a ceiling and the *Günstigerprüfung* | statute [R6] [REG-R42] | **none** |
| Earliest payout age; lifelong-annuity requirement; 30 % lump-sum cap; five-year cost spreading; *Wechselrecht*; unisex; the 20 % biometric carve-out | statute [R1] [R23] [REG-R43] | **none** |
| Taxation of the benefit; *schädliche Verwendung*; the *Rückzahlungsbetrag* | statute [R12] [R14] [REG-R42] | **none** |
| The 100 % *Beitragsgarantie* | statute [R1] [REG-R43] | **none in level**; the *mechanism* varies by chassis |
| *Kleinbetragsrente* threshold | statute [R15] [REG-R42] | **none in level**; whether commutation is mandatory, optional or the saver's right is a contract term — **not established** |
| Disclosure: PIB, *Effektivkosten*, CRK | statute [R4] [R5] [S14] [REG-R43] | **format none**; the disclosed values vary and **none was established** |
| *Rechnungszins* | carrier, capped by [R22] [REG-R14] | only the cap is known: 0,25 % from 2022, 1,00 % from 2025 [REG-R15]. **No carrier's choice established** (gap 12) |
| *Garantierter Rentenfaktor* | carrier | **not established at any house, for any year** (gap 9); the two-factor construction is documented for the German Schicht-3 market in a sibling `delib` file and is the natural expectation here |
| Charges: acquisition, administration, payout-phase, *Effektivkosten*; and the charge base for the Zulagen | carrier | **no figure exists in this corpus** (gaps 13, 14). The single inherited datum — at most **0,95 € per 100 €** of capital formed in an Allianz *RiesterRente* variant [S5] — is third-party commentary on a specimen quotation, not a tariff sheet |
| *Überschussbeteiligung* declarations and surplus system | carrier | **not established** (gap 12) |
| Guarantee **mechanism** | carrier and chassis | the taxonomy is established — general account; *statisches* and *dynamisches Hybridmodell*; i-CPPI; rule-based fund reallocation — but **no carrier's design** |
| Rider inventory (BUZ, survivor's benefit, *Rentengarantiezeit*) | carrier | **not established** (gap 11) |
| Whether the tariff is open to new business | carrier, and now statute | closed to new business from 1 January 2027 [REG-R44]; which houses had already withdrawn, and when, is **not established** |

### The carriers named, and what naming them does and does not assert

| Carrier or provider | Chassis | What is established |
|---|---|---|
| GDV *Musterbedingungen* [S1] [S2] [S3] | both insurance forms | That a **unit-linked** AltZertG model wording exists [S1], that a **non-unit-linked** one exists at "Stand: 21.07.2025" [S2], and that they are **separate condition sets**. Inherited from a sibling session's search [S3]. **No clause, edition or page count** |
| CosmosDirekt [S4] | classic insurance | That the house's Riester wording is tariff **LA 1005 A**, a **separate tariff family** from its Schicht-3 annuity (LA 904 A, LA 1204 A / LA 1201 A) and its Basisrente (LA 1100 A). Inherited [S4]. **No clause content** |
| Allianz Lebensversicherungs-AG [S5] | classic and unit-linked | The market-leader comparator and the source of the corpus's only cost datum [unverified]. **Product names, tariff codes and new-business status not established** (gap 12) |
| Debeka [S6]; R+V [S7]; Alte Leipziger [S8] | classic (and unit-linked at [S8]) | Why each is the right place to look: Debeka is Germany's largest writer of classically guaranteed life business with a membership weighted to *Beamte*, the most natural Riester constituency; R+V is the one group whose Riester offering spans an insurance and a fund chassis in the **same** distribution network as [S9]; Alte Leipziger is the broker-market comparator. **No document, tariff code or vintage for any of them** |
| Union Investment [S9], DWS [S10], Deka [S11] | Riester-Fondssparplan | The three large fund savings plans, all meeting the same guarantee by **rule-based reallocation** between an equity and a bond fund and all sharing the **cash-lock** pathology. **No reallocation rule, fund name, fee or new-business status** (gaps 11, 12) |
| *Sparkassen*; *Volks- und Raiffeisenbanken* [S12] | Riester-Banksparplan | The structurally simplest certified product and the one for which the guarantee costs **nothing at all**, since a deposit balance cannot fall below its deposits — the analytical control case, isolating the guarantee's cost as **return forgone** rather than as a capital charge. **No product, rate or bonus scale** |
| Twenty-plus further life offices [S16] | classic and unit-linked | Named so a follow-up research pass has a list. **Nothing carrier-specific is known for any of them**, and no parameter anywhere in this library may cite [S16] for a **level** |

---

## Regulatory context

**Two statutes doing different jobs.** The **AltZertG** says what a contract must contain to be
certifiable; the **EStG** says who gets what subsidy and how the benefit is taxed. A *product* rule
is in the first, a *money* rule in the second, and confusing the two is the commonest error in
secondary writing about this product. § 1 AltZertG fixes the payout age, the *Beitragserhaltungs-
zusage*, the payout shape, the 30 % lump-sum cap, the five-year cost spreading, the *Wechselrecht*,
the unisex rule, the information duties and the non-assignability [R1] [REG-R43]; §§ 2, 3 and 5
make certification an administrative act of the **BZSt** on the **contract type**, expressly not a
statement about the provider or the product's cost [R2] [S15] [REG-R43]; § 1 Abs. 1a extends
certification to a **loan** [R3]; and §§ 7 ff. with the **AltvPIBV** carry the disclosure regime
[R4] [R5] [S14] [REG-R43]. **Every statutory paragraph number in this library is `[unverified]`**
(gap 4): not one was confirmed against the statute, and no `delib` document may quote a paragraph as
though it had been read.

**The subsidy machinery** is EStG Abschnitt XI: § 79 (entitlement) [R7], §§ 82–83
(*Altersvorsorgebeiträge* and the *Altersvorsorgezulage*) [R8], §§ 84–85 (the amounts) [R9], §§ 86–87
(the *Mindesteigenbeitrag* and multiple contracts) [R10], §§ 89–91 (the ZfA and the administration)
[R11], §§ 92a–92b (Wohn-Riester and the *Wohnförderkonto*) [R13], §§ 93–95 (*schädliche Verwendung*
and its consequences) [R14], § 97 (non-transferability) [R16] — with § 10a carrying the deduction
and the *Günstigerprüfung* [R6] and § 22 Nr. 5 the taxation of the benefit [R12]. All of it is
consolidated for practitioners in the BMF *Anwendungsschreiben*, running to well over a hundred
paragraphs and reissued periodically [R24]; **its date, reference number and content are not
established** (gap 3), and it is the authoritative source for exactly the points this specification
has had to mark `[unverified]`.

**The statutes that shaped the product.** The *Altersvermögensgesetz* and
*Altersvermögensergänzungsgesetz* of 2001 created it for contribution years from 2002, in the same
breath as they **reduced the future replacement rate of the statutory pension** — the pairing is
the whole political logic of the product [R17]. The *Alterseinkünftegesetz* of 2004 created the
three-layer taxonomy [R18] [REG-R38]; the *Eigenheimrentengesetz* of 2008 created Wohn-Riester and
raised the *Kinderzulage* for children born from 2008 [R19]; the
*Altersvorsorge-Verbesserungsgesetz* of 2013 introduced the standardised PIB, capped the *Wechsel*
charge and closed the zero-contribution entitlement of a *mittelbar* eligible spouse [R20]; and the
*Betriebsrentenstärkungsgesetz* of 2017 raised the *Grundzulage* to 175 €, brought the
*Kleinbetragsrenten-Abfindung* under the *Fünftelregelung*, introduced a *Freibetrag* in the
*Grundsicherung im Alter* so that the annuity is no longer offset one-for-one against means-tested
basic security, and removed the double *Krankenversicherung* charge on a Riester annuity drawn from
a **bAV** vehicle [R21]. **Every one was a repair to a criticism rather than an extension, and none
changed the *Beitragsgarantie*** — which is what the 2023 *Fokusgruppe* said had to change [R26],
and what the 2026 reform did by replacing the product [REG-R44].

**Prudential, reserving and tax are cited, never specified.** The *Höchstrechnungszins* of § 2
DeckRV binds the rate at which the guarantee may be discounted and nothing else [R22] [REG-R14]
[REG-R15]; § 4 DeckRV caps *Zillmerung* at 25 ‰ of the *Beitragssumme* [REG-R16]; § 5 Abs. 3 DeckRV
drives the *Zinszusatzreserve* [REG-R17]; the MindZV floors the transfer to the *Rückstellung für
Beitragsrückerstattung* [REG-R18] [REG-R19]; § 153 VVG gives the individual entitlement to the
*Überschussbeteiligung* and the *hälftige* participation in the *Bewertungsreserven* [REG-R24]; and
above them sit the *Deckungsrückstellung* [REG-R54] and Solvabilität II as transposed by the VAG
[REG-R5] [REG-R6]. On the tax side the benefit is *sonstige Einkünfte* taxed in full under § 22
Nr. 5 to the extent it derives from subsidised contributions [R12], with a
*Werbungskosten-Pauschbetrag* of **102 €** `[unverified]`; a **private** Riester annuity is **not**
a *Versorgungsbezug* and attracts no health or long-term-care contribution for a compulsorily
insured pensioner, while a *freiwillig versichertes* member is assessed on their whole economic
capacity, private annuities expressly included [REG-R46]. **None of it is computed here.** This
library publishes gross, undiscounted, best-estimate-style liability cash flows and stops short of
the discounting, so every discount rate, asset return and declared rate in these documents is
**[std]**.

**Conduct, disclosure and the reform track.** The individual *Produktinformationsblatt* with its
individually computed *Effektivkosten* is a **stronger** duty than the product-level VVG-InfoV
figure [R4] [R5] [S14] [REG-R31] [REG-R43]; alongside sit the IDD as transposed [REG-R33], PRIIPs
for the unit-linked chassis [REG-R32], BaFin's *Wohlverhaltensaufsicht* and its expectation of
*angemessener Kundennutzen* [REG-R35], and the BGH line of authority — including its 2025 judgment
striking down asymmetric unilateral reduction of a *Rentenfaktor* [REG-R36], which bears directly on
the two-factor conversion adopted above. The *Fokusgruppe private Altersvorsorge* reported in 2023
recommending that the 100 % *Beitragsgarantie* be relaxed or removed, that a securities-account
product without an insurance wrapper be admitted, that the Zulage be simplified into a proportional
match and that eligibility be widened [R26] `[unverified]` on every element; a 2024 draft bill
creating an *Altersvorsorgedepot* followed and did not become law in that term [R26]. The product
research file recorded the position at its access date as unknown and as its most important gap
(gap 1); the cross-product reference library closes it [REG-R44]. This specification therefore
describes a **legacy** product, and no document in this library may assert a promulgation date or a
BGBl citation for that act, neither of which is established [REG-R44].
