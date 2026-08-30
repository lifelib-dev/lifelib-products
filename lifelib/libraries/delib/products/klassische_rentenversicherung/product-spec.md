# Product Specification

**Status:** Draft, 2026-08-29 (all cited sources accessed 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modeling of a German **klassische aufgeschobene private Rentenversicherung** — the classic
deferred private annuity of *Schicht 3*, in which a premium accumulates in the *Deckungskapital*
(policy reserve) of the insurer's general account at a guaranteed *Rechnungszins* (technical interest
rate), participates in the *Überschussbeteiligung* (profit participation), and is converted at a
contractually fixed *Rentenbeginn* (annuity commencement date) into a lifelong *Leibrente* at a
*Rentenfaktor* (annuity factor) — or taken instead as a lump sum under the *Kapitalwahlrecht*. **It
does not describe any single insurer's contract.** Facts carrying a source tag — [S#] (primary
product documents: AVB, *Verbraucherinformation*, *Kundeninformation*, GDV *Musterbedingungen*,
insurer product pages, surplus declarations) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/klassische_rentenversicherung.md` and resolved in
`sources.md` (**numbering frozen, never renumbered**), and [REG-R#] (the cross-product reference
library, whose own numbering is separate and also frozen) — are attributed to the cited document.
Values marked **[std]** are standardizations introduced for the reference implementation, each with
a numbered footnote giving the rationale and, where the research file recorded one, the observed
range. Claims no search result corroborated are flagged [unverified].

**Retrieval conditions — read this before relying on a single number below.** Direct HTTP egress
from the build environment is blocked by an organisation network policy: `WebFetch` and `curl` are
refused with HTTP 403 for `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de` and every
insurer host named here. **No document cited anywhere in this file was retrieved.** Everything rests
on `WebSearch` result summaries, and the session's shared budget was exhausted after eighteen
queries on this product. A delib citation is a **pointer, not a certificate**: it names the
instrument a claim should be checked against; it does not assert that anyone checked it. The
consequence is concentrated — **the corpus establishes the mechanics of this product thoroughly and
its levels barely at all.** No *Rentenfaktor* level, no declared surplus rate, no charge parameter,
no issue envelope and no behavioural rate was established at any carrier for any year; every one of
those is **[std]** below and none is presented as a market rate.

**The composite draws on ten carriers and one industry body** — the GDV [S1] [S2] [S3] [S10],
Zurich [S4]–[S7] [S16] [S17], CosmosDirekt [S8], NÜRNBERGER [S9], Debeka [S11] [S12], Allianz [S13],
Mecklenburgische [S14], Konzern Versicherungskammer [S15], Stuttgarter [S18] and DEVK [S19] — each
of which is listed with what it establishes, and what it does not, in *Variations across insurers*
below. Where a row there reads "not established", **that is the finding, not an omission**.

---

## Product overview and market role

A *klassische aufgeschobene private Rentenversicherung* is a life insurance contract under the
VVG on a single life in which the insurer's obligation is **an annuity payable for the annuitant's
lifetime, beginning at a contractually fixed date**, with an accumulation period before it [S1]
[S4] [S8] [S9]. The insurer's own placement is *Schicht 3 — Private Vorsorge*: Zurich's scope line
reads "Aufgeschobene Rentenversicherung — **Private Vorsorge (Schicht 3)** und
Rückdeckungsversicherung (Schicht 2)" [S4]. Schicht 3 is the unsubsidised layer of the
*Drei-Schichten-Modell* introduced by the *Alterseinkünftegesetz* from 1 January 2005 [REG-R38]:
no § 10 EStG deduction, no state *Zulage*, no certification under the
*Altersvorsorgeverträge-Zertifizierungsgesetz*. The boundary is visible in the GDV's own taxonomy,
which maintains **separate** model conditions for the *Basisrente* and for certified
*Altersvorsorgeverträge* [S3]; this product is the one **without** a statutory qualification
clause in its title [S1] [S2].

Four features make the German chassis what it is, and each changes the shape of the projected cash
flows.

1. **Two phases with a hard boundary.** The *Aufschubzeit* accumulates a *Deckungskapital*; the
   *Rentenbezugsphase* pays an annuity; the *Rentenbeginn* separates them [S1] [S4] [S8] [S11].
   Three distinct things happen at that one date and a model must sequence all three: the
   accumulated value is struck including surplus and *Bewertungsreserven* [S9]; the *Rentenfaktor*
   is determined by comparing two factors [S4] [S13]; and the *Kapitalwahlrecht* election takes
   effect [S12] [R21].
2. **The guarantee is a rate, and a property of the contract's vintage rather than of the market.**
   The *Rechnungszins* is capped for new business by the *Höchstrechnungszins* of § 2
   *Deckungsrückstellungsverordnung* [R7] [R11] [REG-R14], **and the rate applicable at conclusion
   then stays with the contract for its whole term** [REG-R14]. A German life book is a layered
   stack of guarantee vintages — 4,00 % for 07/1994–06/2000 down to 0,25 % for 2022–2024 and back
   to 1,00 % from 2025 [REG-R15] — so the *Rechnungszins* is a **model-point attribute, not a
   global assumption**. An insurer may also guarantee less than the cap, and does: CosmosDirekt's
   conversion basis is "an underlying interest rate (currently 0 percent p.a.)" [S8]; Debeka's
   safest post-2016 variant guarantees 0,5 % [R22].
3. **The *Rentenfaktor* is a guarantee with upside, not a fixed conversion rate.** It is fixed at
   inception on the *Rechnungsgrundlagen* then in force [R24]; at *Rentenbeginn* a second, current
   factor is computed and **the higher of the two is guaranteed for the annuity payment period**
   [S4]. A model applying only the guaranteed factor understates the benefit whenever the current
   tariff is richer.
4. **The classic tariff is the market's reference chassis rather than a live new-business
   product.** Debeka, Allianz, Zurich and Generali are all reported to have stopped distributing the
   classic form, Debeka replacing it from 1 July 2016 with five "Chance" variants and Allianz with
   the KomfortDynamik premium-guarantee hybrid [R22] [S12] [S13] [R23] — yet Zurich still publishes a
   *Verbraucherinformation für Konventionelle Versicherungen* for the deferred annuity in the
   **Fassung 01/2026** [S4] and CosmosDirekt still publishes AVB whose *Rentenfaktor* is struck on
   DAV 2004 R [S8]. **The two statements are in tension and this file does not resolve them**
   (gap 9). That is exactly why the right unit of description is a **composite of a chassis**, and it
   is the role a lifelib reference model is for: the in-force book still runs on this design.

**Market size.** German life insurers, *Pensionskassen* and *Pensionsfonds* together took premium
income of **94,6 Mrd €** in 2024, up 2,8 %, of which *laufende Beiträge* were **66,3 Mrd €**, roughly
flat, and *Einmalbeitragsgeschäft* about **28 Mrd €**, up about 10 %; the contract count fell 1,4 %
to **80,3 Mio** [REG-R53]. On the BaFin basis the life segment's *verdiente Bruttobeiträge* were
**90,4 Mrd €** — a different population on a different basis, and the two must never appear in one
table [REG-R53]. The GDV taxonomy reports *Rentenversicherungen* as one class covering both this
product and the immediate annuity, so **no figure isolating the classic deferred annuity was
established** [REG-R53]. For credited-rate context, the average *laufende Verzinsung* for **2025**
was **2,53 % Klassik / 2,58 % Neue Klassik**; for **2026** the sources give 2,6–2,7 %, 2,87 % and
2,54 % — three incompatible averages [REG-R53].

---

## Representative specification

The representative design is the chassis the corpus supports as a whole: a single-life deferred
annuity on the general account, Schicht 3, against a level recurring premium over a fixed
*Aufschubzeit* [S4] [S11], with *verzinsliche Ansammlung* as the accumulation-phase surplus system
[R24], a *Beitragsrückgewähr* death benefit in the premiums-only form named by the GDV model
wording [S1] [R24], conversion at `max(garantierter, aktueller Rentenfaktor)` [S4] [R24], and
*Rückkaufswert* and *Beitragsfreistellung* as separate decrements under §§ 169 and 165 VVG [R1]
[R2]. **Every number in it that is not source-tagged is [std].**

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-life deferred annuity on the general account (*konventionell*, *klassisch*); profit-participating; Schicht 3 | [S1] [S4] [S8] [S9] [S11] |
| Legal wrapper | Individual contract on the insurer's own AVB. A *Konsortialversicherung* edition of the same wording exists and changes the parties, not the cash flows | [S4] [S5] [S7]; [S6] |
| Lives basis | Single life. The survivor's annuity is a separate *Zusatzversicherung* with its own GDV model conditions, not a benefit of the base contract | [S10] |
| Premium form (model-point parameter) | (i) `laufend` — level recurring premium over the *Aufschubzeit*; (ii) `einmal` — *Einmalbeitrag* | (i) [S11]; (ii) [REG-R53]; split **[std]** (1) |
| Entry ages | 18 to 62 | **[std]** (2) |
| *Aufschubdauer* | 5 to 40 years | **[std]** (2) |
| *Rentenbeginn* age | 62 to 72; representative **67** | **[std]** (2) |
| Age basis | Age last birthday at inception, stepping at the policy anniversary | **[std]** (3) |
| Sex | Recorded, and **may not enter the tariff**: sex-based premium and benefit differences are prohibited for contracts concluded from 21 December 2012 | [REG-R34] |
| Premium envelope | 600 € to 24 000 € a year recurring; 5 000 € to 250 000 € single | **[std]** (2) |
| Anchor model cell | Male, issue age 50, issue year 2026, *Aufschubdauer* 17 years (*Rentenbeginn* at 67), 3 000,00 € recurring annual premium, *Rechnungszins* 1,00 %, *Beitragsrückgewähr* death benefit, *Rentengarantiezeit* 10 years, *Kapitalwahlrecht* take-up 30 % | **[std]** (4) |

1. **The market split between recurring and single premium was not established** (gap 13). The
   aggregate is that *Einmalbeitragsgeschäft* is about 30 % of German life premium income and grew
   about 10 % in 2024 against a flat recurring book [REG-R53]. The recurring form is the one
   [S11]'s accumulation mechanics describe; the single-premium form is a model-point value because
   the aggregate says it cannot be ignored.
2. **The entire issue envelope is unestablished at every carrier** (gap 13): no premium limits, no
   *Aufschubdauer* limits, no entry ages, no *Rentenbeginn* window. These are round-number
   placeholders chosen so the model point table can carry an interior anchor and boundary points
   either side, and should be replaced wholesale by anyone with a *Tarifblatt*. The one age with an
   external anchor is **67**, the *Regelaltersgrenze*.
3. No German source states an age convention for this product; age last birthday, stepping at the
   anniversary, is the delib-wide convention registered as `age_basis = "ALB"` in
   `tests/de_registry.py`, and it matters less here than in a protection product because the
   *Rentenfaktor* rather than a mortality lookup fixes the benefit amount.
4. Issue age 50 with a 17-year *Aufschubzeit* puts four things inside one projection: the whole
   accumulation phase in seventeen rows; the § 20 Abs. 1 Nr. 6 EStG **twelve-year** threshold at
   duration 12 and its **age-62** partner at duration 13 [REG-R45], together the strongest driver of
   German Schicht-3 surrender behaviour; the *Rentenbeginn* at 67; and a payout phase long enough
   for the *Rentengarantiezeit* to expire inside it.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level *Bruttobeitrag* over the *Aufschubzeit*, or a single *Einmalbeitrag* at inception | [S11]; [REG-R53] |
| Premium decomposition | The premium splits into the portion **required for risk and expense cover** and the remainder, the ***Sparbeitrag***, which is what accumulates: the *Deckungskapital* is "the sum of the contributions accumulated at the *Rechnungszins*, **insofar as these are not intended for risk and cost coverage**" | [S11]; from the other side, "from the savings portion, Debeka forms a *Deckungskapital* for the guaranteed benefits" [S12] |
| Payment frequency | Annual, half-yearly, quarterly or monthly | [S4]; **[std]** (5) |
| *Ratenzahlungszuschlag* | Annual 1,000; half-yearly 1,020; quarterly 1,030; monthly 1,050 | **[std]** (5) |
| Premium term | Equal to the *Aufschubdauer* in the representative design; a shorter paying term is a model-point parameter | **[std]** (6) |
| *Dynamik* / *Anpassungsversicherung* | Automatic annual increase of premium and benefit; a documented option with its own condition set, "Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung" | [S4]; parameters **[std]** (7) |
| *Zuzahlung* | An ad-hoc additional single premium into a running contract. **Not established by any source in this corpus**; therefore not specified and not modeled | gap 15 |
| Non-payment path | Life insurance does not lose cover on a missed *Folgeprämie*: after a *qualifizierte Mahnung* in Textform with a minimum two-week period, § 166 VVG converts the contract to *prämienfrei* rather than terminating it | [REG-R28] [REG-R30] |

5. **No *Ratenzahlungszuschlag* percentage was established at any German carrier** (gap 14); the
   levels are a monotone [std] ladder in which the monthly mode costs 5 % more than the annual one.
   Note the interaction with *Zillmerung*: § 4 DeckRV takes the *Zillmersatz* on the
   *Beitragssumme*, the sum of all premiums payable [REG-R16], so the loading enters the
   acquisition-charge base as well as the premium.
6. No source establishes whether German tariffs permit a paying term shorter than the deferment; the
   representative design equates them and the model carries `prem_term_y` separately.
7. The *Dynamik* option is **established from a primary document** — a named section of the Zurich
   pack with its own condition set [S4] — but **its increase percentage, its basis, whether fresh
   underwriting applies and how many refusals end it are all unestablished** (gap 15). The
   implementation carries `dynamik_rate`, base 0, with 5 % on one point to exercise the mechanic.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Payment timing | Monthly **in advance**. **Whether the market pays in advance or in arrears was not established** (gap 19), and this is a first-order modelling parameter | **[std]** (8) |
| Conversion capital | The contract value used for annuitisation **includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general contract data** | [S9] |
| *Rentenfaktor* applied | `max(garantierter, aktueller)` — at the start of annuity payments a second factor is compared with the guaranteed one and **the higher of the two is guaranteed for the annuity payment period** | [S4]; restated from the other side by [R24] |
| *garantierter Rentenfaktor* | Fixed at inception on the *Rechnungsgrundlagen* then in force, with a *Sicherheitsabschlag* making it lower than the current factor. Representative 28,00 € per month per 10 000 € at *Rentenbeginn* 67 | mechanic [R24] [S8]; **level [std]** (9) |
| Its interest basis | **0 % p.a.** at one carrier — a deliberate prudential margin below the *Höchstrechnungszins* | [S8]; vintage unestablished (gap 5) |
| *aktueller Rentenfaktor* | The carrier's **then-current immediate-annuity tariff**: the bases at *Rentenbeginn* "relate to the interest rate and mortality table that the company uses at that time for immediately beginning annuities" | [S13]; [R24]; **level [std]** (9) |
| Annuity in payment | The sum of a *garantierte Rente* and an *Überschussrente*; only the guaranteed part is a promise | [R20] |
| *Überschussverwendung* in payment | Policyholder's choice of *konstante*, *teildynamische* or *volldynamische Rente* | [R19] [R20] [R24] |
| *Bewertungsreserven* in payment | Participation **continues during the annuity payment period** | [S4] [R4] |
| *Rentengarantiezeit* | 10 years representative; 5, 10, 15, 20, 25 or 30+ offered; typically 15 years for retirement ages 61–70 and 10 for 71 and above; most choose 10 to 20 | [R24]; in the tariff name at NÜRNBERGER [S9]; selectable with a floor at Allianz [S13] |
| Death benefit before *Rentenbeginn* | ***Beitragsrückgewähr*** — the insurer refunds all premiums paid — in the premiums-only form. Two documented alternatives: premiums **plus the attributable *Überschussbeteiligung***, which "can be agreed"; and payment of the accumulated *Deckungskapital* | [S1] names the term in the model wording; three forms [R24] |
| A `max(...)` death benefit | Established for the **unit-linked** sibling — "the fund value at the date of death but at least the sum of the premiums paid (*Beitragsrückgewähr*)" — its classic analogue is **[unverified]** | [S19]; classic form **[std]** (10) |
| Death benefit timing | **Not established** — whether it falls at the date of death or at the next anniversary, and whether the with-surplus form includes the whole *Ansammlungsguthaben* | gap 18 |
| Death after *Rentenbeginn* | Nothing beyond the *Rentengarantiezeit* and the survivor's-annuity rider. ***Beitragsrückgewähr in der Rentenbezugsphase*** **was not established by any source and must not be asserted** | gap 18; [R24] [S10] |
| *Kapitalwahlrecht* | The policyholder may take the accumulated capital as a lump sum instead of the annuity at *Rentenbeginn* | [S12] [R6] [R21] |
| Its notice period | **Not established at any carrier**, including from the GDV's own consumer page on payout options | gap 11; **[std]** (11) |

8. Every source describes the annuity as monthly [S13] [R24]; **none states whether it is payable
   in advance or in arrears** (gap 19). The choice is worth about half a month's interest on the
   annuity's present value and shifts every payout cash flow by one period, so it is adopted
   explicitly: **monthly in advance**, compressed onto the annual grid as one payment at the start
   of each policy year.
9. **No *Rentenfaktor* level, range or time series was established — at any carrier, for any year**
   (gap 3); the only figure in the corpus is a teaching illustration, 100 000 € at a factor of 25
   giving 250 € a month [R24], and the rating house's own article "wie hoch ist er?" returned no
   level [R19]. The values used here — guaranteed 28,00 €; current 32,00 € base, 25,50 € low,
   35,00 € high, all at *Rentenbeginn* 67 — are **anchors chosen so the worked example reproduces
   exactly and the `max()` rule is exercised in both directions**, not market rates.
10. The `max` form is offered as a model-point value because it is the shape the unit-linked wording
    uses [S19], and because a German contract is not eligible for the § 20 Abs. 1 Nr. 6 half-income
    treatment unless the *Todesfallleistung* meets the *Mindesttodesfallschutz* test [REG-R45]. **No
    classic document states it**, so the base case is the plain *Beitragsrückgewähr* [S1].
11. No document named a *Kapitalwahlrecht* notice period at any carrier (gap 11). The election takes
    effect **at** *Rentenbeginn* with no notice modelling, because on an annual grid a notice period
    inside the last policy year moves nothing.

### Underwriting and rating

**There is no underwriting.** A deferred annuity's biometric risk is longevity, which underwriting
cannot select against in the insurer's favour, and the pre-*Rentenbeginn* death benefit is the
premiums paid or the accumulated fund, so there is no sum at risk to underwrite — a structural
consequence of the benefit shape [S19] [R24] rather than a documented carrier practice, since **no
source in this corpus states an underwriting rule for a German deferred annuity**. It is tagged
**[std]** because the implementation acts on it: no rating factor, no select period and no
substandard loading anywhere in the model. The *Berufsunfähigkeits-Zusatzversicherung* carried in the
same pre-contractual pack has its own special conditions and its own underwriting [S4]. Rating runs
on entry age and *Aufschubdauer* through the tariff, and **sex may not be a rating factor** for
contracts concluded from 21 December 2012 [REG-R34]. Four statutory rules reach the contract without
being tariff parameters: the *Anzeigepflicht* of § 19 VVG, whose remedies § 21 Abs. 3 VVG
extinguishes five years after conclusion and ten on intent or fraud [unverified]; § 157 VVG, under which an age misstatement changes the benefit
in the ratio of the premium for the true age to the agreed premium; § 150 VVG, requiring the written
consent of the insured where a policy is on another person's death above ordinary funeral costs; and
§ 161 VVG, excluding intentional suicide within three years while still requiring payment of the
*Rückkaufswert* including profit shares [REG-R26] [REG-R30]. **No source applies the suicide rule to
a *Beitragsrückgewähr***, where the benefit is the premiums back rather than a sum at risk; its
application here is [unverified] and it is not modeled.

### Charges

**This is the weakest area of the corpus.** No charge parameter was established for this product at
any German carrier (gap 14) — not the *Abschluss- und Vertriebskosten* rate, the *Verwaltungskosten*
in any form, the *Ratenzahlungszuschlag*, the payout-phase administration charge or the
*Effektivkosten* disclosure — and no *Produktinformationsblatt* or *Basisinformationsblatt*
(PRIIP-KID) for a classic deferred annuity appears in the corpus at all. The two figures it does
contain — an *Abschlussprovision* of **1 575 €** on an Allianz specimen quotation, and total costs
relative to the capital formed of **at most 0,95 € per 100 €** — come from third-party analyses of
**Schicht-1 and Schicht-2** variants and are [unverified] as Schicht-3 levels [S13] [R23].

| Parameter | Representative value | Basis |
|---|---|---|
| Charge structure | **Premium-based deductions, not asset-based ones**, in the classic chassis: a portion of the premium is "intended for risk and cost coverage" and is deducted before the *Sparbeitrag* | [S11] |
| *Abschluss- und Vertriebskosten* (α) | **25 ‰ of the *Beitragssumme***, zillmered — charged against the earliest premiums until exhausted | cap [REG-R16]; use of the cap **[std]** (12) |
| Legacy α vintage | **40 ‰** for contracts concluded before 1 January 2015; the rate used at conclusion applies for the whole term | [REG-R16] [REG-R20] |
| *Verwaltungskosten* on premium (β) | 4,0 % of each gross premium | **[std]** (12) |
| *Verwaltungskosten* on the reserve (γ) | 0,20 % p.a. of the *Deckungskapital* | **[std]** (12) |
| *Risikobeitrag* (ρ) | The tariff mortality rate on the net amount at risk, `max(0, death benefit − Deckungskapital)` | structure [S11]; level follows the table |
| *Stornoabzug* | 2,0 % of the computed surrender value. A deduction is permitted **only if agreed, quantified (*beziffert*) and appropriate (*angemessen*)**, and **a deduction for not-yet-amortised acquisition and distribution costs is void** | [R1] [REG-R28]; level **[std]** (12) |
| Payout-phase administration | 1,5 % of each annuity instalment | **[std]** (12) |
| *Effektivkosten* | Required by the German disclosure regime; **no value established for this product** | gap 14 |

12. **Every charge level above is a placeholder and none is a market rate.** Two have an anchor of a
kind: the α rate is the **statutory ceiling** of § 4 DeckRV — 25 ‰ of the *Beitragssumme* since
1 January 2015, 40 ‰ before [REG-R16] [REG-R20] — though using a ceiling as a tariff rate is a
modelling choice; and the *Stornoabzug* is a percentage because § 169 Abs. 5 requires it to be
*beziffert* and *angemessen* [R1] [REG-R28] and forbids it from recovering unamortised acquisition
costs, which is what makes the § 169 Abs. 3 floor rather than the deduction the operative constraint
on early surrender values. The β, γ and annuity-administration rates have no anchor at all and are
sized so the total load is of the order the one Schicht-1/2 figure implies (0,95 € per 100 € [S13]
[R23]).

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Kündigung* / *Rückkaufswert* | Available at any time for the end of the current insurance period while recurring premiums are payable. The base measure is the *Deckungskapital* computed by recognised actuarial rules **on the calculation bases of the premium calculation** | [R1] [REG-R28] |
| **The statutory floor** | § 169 Abs. 3 VVG: **at least the *Deckungskapital* that results from spreading the charged acquisition and distribution costs evenly over the first five contract years** — a floor on the value, not a cap on the charge, and independent of the supervisory *Zillmer* rules | [REG-R28]; at article level [unverified] here (gap 12) |
| *Stornoabzug* | Permitted only if agreed, quantified and appropriate; a deduction for unamortised acquisition costs is void; the burden of proof is on the insurer | [R1] [REG-R28] |
| § 169 Abs. 6 | The insurer may in defined cases reduce surrender values to be paid out — a solvency valve, **not modeled** | [R1] |
| Surrender in the payout phase | **None.** § 168 Abs. 1 gives the right where *laufende Prämien* are payable, Abs. 2 on a single premium where the occurrence of the obligation is certain; a life annuity already in payment is neither | [REG-R28]; reading **[std]** (13) |
| *Beitragsfreistellung* | The policyholder may **at any time, for the end of the current insurance period**, demand conversion into a premium-free insurance, **provided the agreed *Mindestversicherungsleistung* is reached** | [R2] [REG-R28] |
| Its value | Calculated by recognised actuarial principles **on the calculation basis of the premium calculation, on the basis of the *Rückkaufswert* under § 169 Abs. 3 to 5**, and **stated in the contract for each insurance year** | [R2] [REG-R28] |
| Below the minimum | The insurer must instead pay the surrender value attributable to the insurance, **including profit shares**, under § 169 — a small contract cannot be made paid-up; it is cashed out | [R2] |
| The *Mindestversicherungsleistung* | **Not established at any carrier.** Representative threshold: a guaranteed annuity of 30,00 € a month | gap 22; **[std]** (14) |
| Premium-default conversion | § 166 VVG converts automatically to *prämienfrei* rather than terminating cover — German lapse is a **three-way** decrement | [REG-R28] [REG-R30] |

13. No German source says whether a deferred annuity in payment may be surrendered; the reading
follows from § 168 VVG as recorded in the cross-product library
[REG-R28] and from the fact that the insurer's obligation in the payout phase has already occurred,
and the implementation acts on it by setting the lapse rate to zero from *Rentenbeginn*.
14. § 165 VVG makes the paid-up right conditional on a *Mindestversicherungsleistung* [R2] and **no carrier's
threshold was returned** (gap 22); 30,00 € a month is chosen so one model point trips it and is
cashed out instead of being made paid-up — the branch the statute cares about.

---

## Contractual mechanics

### The two phases and the *Rentenbeginn* boundary

The contract has two phases separated by the *Rentenbeginn*: the *Aufschubzeit*, over which premiums
are paid and the *Deckungskapital* accumulates, and the *Rentenbezugsphase*, over which the annuity
is paid [S1] [S4] [S8] [S11]. "Eine Aufschubzeit gibt es nur bei aufgeschobenen
Rentenversicherungen" — a deferment period exists only in a deferred annuity contract, the
definitional line separating this product from delib's `sofortrente` [R24].

**Three distinct things happen at the boundary** and a model that collapses them into one step will
get at least one wrong: the accumulated value is struck including surplus and *Bewertungsreserven*
[S9]; the *Rentenfaktor* is determined by comparing the guaranteed factor with the then-current one
[S4] [S13]; and the *Kapitalwahlrecht* election takes effect [S12] [R21]. The technical notes give
the boundary its own numbered position in the processing order for that reason.

### The *Deckungskapital* recursion

The definitional statement comes from an insurer: the *Deckungskapital* is **"the sum of the
contributions accumulated at the *Rechnungszins*, insofar as these are not intended for risk and cost
coverage"** [S11]; Debeka states the same split from the other direction [S12]. Unpacked into the
recursion an implementation carries — and this unpacking is a **reading** of [S11], not a clause the
corpus supplied in this form:

    Deckungskapital(t) = ( Deckungskapital(t-1) + Sparbeitrag(t) ) x (1 + Rechnungszins)
    Sparbeitrag(t)     = Beitrag(t) - Risikobeitrag(t) - Kostenbeitrag(t)

**The ordering of premium credit, charge deduction and interest accrual within a period is not
established by any source in this corpus** and is a [std] decision, stated explicitly in the
technical notes. The implementation credits the premium first, takes the charges next, and accrues
interest on the balance after both — the reading that makes the year-one interest credit largest, and
therefore the one that must be argued rather than assumed. The *Deckungskapital* is what everything
else is defined off: the death benefit in one of the two designs, the basis of the *Rückkaufswert*
[R1] and of the *beitragsfreie Versicherungsleistung* [R2], and — with surplus and
*Bewertungsreserven* added — the capital the *Rentenfaktor* applies to [S9].

### The *Rechnungszins* and the guarantee-vintage stack

The *Rechnungszins* is the rate at which the *Sparbeitrag* is guaranteed to accumulate [S11], capped
for new business by the *Höchstrechnungszins* of § 2 DeckRV [R7] [R11] [REG-R14] — the rate market
language calls the *Garantiezins*, although the two are not legally identical, because § 2 caps the
**reserving** rate while the rate a policy guarantees is a tariff decision that may be lower
[REG-R14]. **From 1 January 2025 the rate is 1,00 %**, raised from **0,25 %** by the *Sechste
Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024,
BGBl. 2024 I Nr. 250 [REG-R15], announced in the *Bundesgesetzblatt* on 24 July [R7] [R10] [R11].
**This was the first increase since 1994**, and the DAV recommends 1,0 % for 2026 as well [R8]. The
mechanism is standing — DAV recommends, BMF legislates, with a lead time of about fourteen months
[R9] — which makes the *Rechnungszins* of a tariff a parameter known well before it binds. The full
rate history is in the cross-product library [REG-R15]; only its two most recent points were
corroborated in this product's own research (gap 7).

**The modelling consequence is that the *Rechnungszins* is a model-point attribute, not a global
assumption**, and that a model assuming the guaranteed rate equals the statutory cap is wrong in the
same direction at every carrier (overview, point 2).

### *Überschussbeteiligung* in the *Aufschubphase*, and the *Bewertungsreserven*

*Überschussbeteiligung* is the participation of policyholders in the surpluses of the undertaking
[R24]. Its magnitude depends, in an insurer's own contractual words, on "many influences which are
unpredictable and only limitedly controllable by the company, with the most important influencing
factor being capital-market developments" [S8]. **That disclaimer is why surplus is modelled as a
declaration — an insurer-discretionary current assumption — and never as a guarantee.** The
declaration instrument is an annual document: the Konzern Versicherungskammer publishes its
*"Überschussverteilung 2026"* as a standalone PDF [S15] and every German life insurer publishes an
equivalent. **No rate from any such document was established** (gap 4).

The *Zinsüberschuss* arises **when investment income exceeds the *Rechnungszins***: "when investment
income exceeds the calculation rate, the insurance company generates surpluses in the form of
interest gains" [R24]. That is the direct statement that the *Rechnungszins* is the **hurdle rate**
of the surplus mechanism, and it is the fact behind the commonest arithmetic error in describing a
German contract. The declared ***laufende Verzinsung*** is the *Garantieverzinsung* **plus** the
*laufende Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee** [REG-R53]. On
the 1,00 % vintage a declared 2,55 % means a surplus credit of 1,55 %; on the 2,75 % vintage of 2004
the same declaration means a surplus credit of **nothing at all**, and the contract simply receives
its guarantee. Adding the declared rate to the guaranteed one overstates a modern contract by more
than half and a legacy contract by all of it.

**Three accumulation-phase surplus systems are established.** ***Verzinsliche Ansammlung*** is the
classic default and the representative system: declared surpluses are credited to a separate
***Ansammlungsguthaben*** and accrue with interest, "with the interest credited at the end of each
insurance year and upon termination of the insurance" [R24] — a **second, parallel account** to the
*Deckungskapital*, with its own credited rate, settling at year end and at exit. ***Bonusrente***
buys **additional premium-free annuity** with the declared surplus [R24]; it is established and
**not implemented**, because it is a second full mechanic on the same declaration and carrying both
would double the accumulation-phase state for a choice no source quantifies. **Investment of surplus
in an internal fund** is the Debeka successor design, a variation rather than the representative one
[S12]. ***Beitragsverrechnung*** is the fourth system the German market uses and **no source in this
corpus named it for this product** (gap 16) — a gap in the corpus, not evidence that it does not
exist. The **four-component decomposition** is only one quarter established here (gap 17), is the
primary subject of the delib `kapitallebensversicherung` file, and has the MindZV's 90 / 90 / 50
minima under it [REG-R18]; the implementation models the credited outcome, not the source
decomposition.

**Bewertungsreserven.** Under **§ 153 Abs. 3 VVG** policyholders participate in the unrealised gains
in the insurer's assets, restated by an insurer's own consumer information as **equal (*hälftige*)
participation** [S4] [R4] [REG-R24]; the **transition to annuity payment is a key point** for it, so
the share crystallises at the boundary, and **participation continues during the payout phase** [S4]
[R4]. The LVRG 2014 restricted distribution to reserves from *festverzinsliche Wertpapiere* and
subjected departing policyholders' share to the *Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG and
§§ 11–12 MindZV [REG-R20] [REG-R18]. The implementation carries the crystallisation at *Rentenbeginn*
as a [std] rate and does **not** implement the *Sicherungsbedarf* test, whose inputs are
balance-sheet quantities a single-policy liability projection does not have.

### The *Todesfallleistung* before *Rentenbeginn*

On death during the *Aufschubzeit* the contract pays a death benefit and ends. **Three designs are
established, all in use** [R24]: ***Beitragsrückgewähr*** — "the insurer refunds all paid premiums
after the death" — with an optional extension, "repayment of the premiums plus the
*Überschussbeteiligung* attributable to them can be agreed", so the choice between a bare and a
with-surplus form is contractual; **payment of the accumulated *Deckungskapital***; and a
***Hinterbliebenenrente***, which has its own GDV model condition set [S10] and is properly a rider.
**The term *Beitragsrückgewähr* is named in the GDV model conditions for this product** [S1] — the
model wording's own word. The `max(...)` form is established for the **unit-linked sibling and not
for the classic product**: DEVK gives the fund value at death "but at least the sum of the premiums
paid (*Beitragsrückgewähr*)" [S19]; no classic document in this corpus states the analogue, so any
design adopting it must tag it [std].

**What the death benefit is not:** there is no separate sum insured anywhere in this product — the
structural difference from delib's `kapitallebensversicherung` and `risikolebensversicherung`, and
why this product carries no underwriting and no rating factor [S19] [R24]. **Whether the benefit
falls at the date of death or at the next policy anniversary, and whether the with-surplus form
includes the *Ansammlungsguthaben* in full, were not established** (gap 18); the implementation pays
at the end of the policy year of death and offers the surplus inclusion as a model-point switch.

### The *Rentenfaktor*, and the narrow channel for reducing it

This is the mechanic the whole product turns on and the best-evidenced thing in the corpus. The
factor determines how much monthly annuity is received per 10 000 € of accumulated capital [R24];
the corpus's illustration is 100 000 € at a factor of 25 yielding 250 € a month [R24], where the 25
is a **teaching example, not a market level** (gap 3):

    monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor

**Guaranteed at inception.** The *garantierter Rentenfaktor* is fixed in the contract documents on
the *Rechnungsgrundlagen* as at the date of conclusion [R24] — a guarantee given at issue about a
conversion decades later — with a ***Sicherheitsabschlag*** that makes it lower than the current
factor [R24]. **The margin is quantifiable from one carrier**: CosmosDirekt's factor is computed "on
the basis of a recognised mortality table (currently DAV 2004 R) and an underlying interest rate
(currently 0 percent p.a.)" [S8]. A zero-percent interest basis, against a *Höchstrechnungszins*
positive throughout, is the *Sicherheitsabschlag* made concrete: the guaranteed factor is priced as
though the insurer will earn nothing on the annuity fund. Allianz expresses the same guarantee as "a
minimum annuity" available at inception [S13].

**Current, and the comparison.** The *aktueller Rentenfaktor* is recomputed on the bases in force
when quoted, and Allianz says what "current" means operationally: the bases at *Rentenbeginn* relate
to "the interest rate and mortality table that the company uses **at that time for immediately
beginning annuities**" [S13] — which is why an immediate-annuity document [S16] belongs in this
product's source list. **The rule at *Rentenbeginn* is a maximum of two factors.** Zurich: at the
start of annuity payments a second factor is compared with the guaranteed one, **the higher of the
two being guaranteed for the annuity payment period** [S4]; the consumer literature states the same
rule from the other side [R24].

    Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )

This is a **guarantee with upside**, and it is the mechanic an implementation is most likely to get
wrong in the direction that understates the liability. The factor moves with the *Rechnungszins* and
with the mortality basis, because those are the two things it is computed from [S8] [S13] [R24] — but
**the magnitude was not established**: no search returned a level, a range or a time series, not even
from the rating house whose article asks "wie hoch ist er?" [R19].

**Reducing a guaranteed factor.** Historically, insurers could change guaranteed *Rentenfaktoren* on
a ***Treuhänderklausel*** with an independent *Treuhänder*'s approval, on two triggers: an
**unexpectedly strong increase in life expectancy** and a **sustainable reduction in capital-market
returns** [R17] [R3]. **Currently the clause is used only in older contracts, and the guaranteed
factor can be changed only on the basis of § 163 VVG** [R17] [R3], which requires **three cumulative
conditions**: a change in the *Leistungsbedarf* that is neither temporary nor foreseeable; a newly
set premium that is appropriate and necessary to secure permanent fulfilment; and an *unabhängiger
Treuhänder* who has confirmed both [REG-R27]. Adjustment is **excluded** where the benefits were
insufficiently calculated originally and a diligent actuary should have recognised it — **the insurer
may not reprice its way out of its own mispricing** — and the article permits a **reduction of the
benefit** instead of a premium increase [REG-R27]. **The courts have narrowed it further**: the
Landgericht Köln held the low-interest phase **not** a sufficient ground, being entrepreneurial risk
that cannot be passed to policyholders [R17], and consumer press reports that a reduction **can be
unlawful** [R16]; **the case reference and decision date were not established** (gap 10) and no
citation beyond "a Landgericht Köln decision reported by [R17]" may be made. It was a live dispute at
the market leader in February 2021 [R18], and the BGH struck down asymmetric unilateral reduction
clauses in 2025 [REG-R36]. **The implementation treats the guaranteed factor as fixed and records
§ 163 VVG as a model risk.**

### The *Rentenphase* and the *Rentengarantiezeit*

The annuity in payment is **the sum of a *garantierte Rente* and an *Überschussrente***: the insurer
sets a value at the start of the payout phase "composed of the *Garantierente* and a surplus share
projected for the whole annuity period" [R20]. **Only the guaranteed part is a promise.** Three
*Überschussverwendung* systems exist and the choice is the policyholder's [R19] [R20] [R24]:

| System | Mechanic |
|---|---|
| ***konstante Rente*** | The payout stays the same over the whole term; the insurer fixes a value at the start of the payout phase from the *Garantierente* plus a surplus share **projected for the whole annuity period**. In practice it can still fluctuate: **if the provider earns less than expected, the annuity falls** [R20]. |
| ***teildynamische Rente*** | The annuity rises regularly by a **fixed percentage** provided the insurer earns corresponding surpluses — a combination in which part of the expected surplus is used under the constant system and part under the dynamic system [R20] [R24]. |
| ***volldynamische (steigende) Rente*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R20]. It starts lowest and rises fastest. |

The ***Bonusrente*** is the mechanism underneath the rising forms — "the ongoing surplus shares are
used partly for an age-dependent *Überschussrente* and partly for an additional premium-free annuity
(*Bonusrente*)" [R24] — and the increment, once bought, is **premium-free and permanent**, which is
what makes a *volldynamische Rente* ratchet rather than fluctuate. **The constant form is not
actually constant**, which is exactly what a model gets wrong by taking a product name literally: the
annuity is set from a **projection**, and if the insurer earns less than projected it is reduced
[R20].

The ***Rentengarantiezeit*** is a guaranteed payment period beginning at *Rentenbeginn*: if the
annuitant dies inside it, **the annuity continues to be paid to the survivors until the agreed years
have expired** [R17] [R24] — the corpus's illustration being a 10-year period with death after 6
years and the spouse receiving the remaining 4. Durations, typical choices and cost are in the
benefit-provisions table above; it is selectable with a floor at Allianz [S13] and carried in the
product name at NÜRNBERGER, tariff NIR3301 [S9].

**Its modelling consequence is a decrement-weighting one and it is the pitfall this product hides
best.** Inside the guarantee period the payment obligation does not depend on survival: the
instalment is due to the annuitant or to the survivors either way, so it must be weighted by the
**count that annuitised**, not by the count still alive; outside the period it is weighted by
survivors. The two counts differ by exactly the deaths inside the window, and a model that weights
everything by survivors understates the annuity outgo by that amount while never producing a number
that looks wrong.

### The *Kapitalwahlrecht*

The right to take **the accumulated capital as a lump sum instead of the lifelong annuity** at
*Rentenbeginn* [S12] [R6] [R21], and the third of the three things that happen at that boundary.
**The notice period was not established at any carrier** (gap 11).

**The tax consequence of electing it is total, and it is the established part.** The lump sum moves
the contract from the *Ertragsanteil* regime of § 22 EStG [R5] [REG-R41] to § 20 Abs. 1 Nr. 6 EStG
[R6] [REG-R45]: where the **"12/62 rule"** is met — at least 12 years of contract duration and
payment after completion of the 62nd year of life — **only half the *Unterschiedsbetrag* between the
*Versicherungsleistung* and the premiums paid is taxable**, at the **personal marginal rate** under
§ 32d Abs. 2 Nr. 2 EStG, and the *Halbeinkünfteverfahren* applies **only to lump sums and
payout-plan withdrawals, not to monthly annuity payments** [R6] [REG-R45]. The age limb is **60** for
contracts concluded up to **31 December 2011** and **62** for those concluded after it [R6] [REG-R45].

**Contracts concluded before 1 January 2005 are not in the *Halbeinkünfteverfahren* at all.** The
§ 20 Abs. 1 Nr. 6 EStG regime in its *Alterseinkünftegesetz* recast does not reach them; under the
predecessor regime, where the pre-AltEinkG conditions are met — a term of at least twelve years,
premiums paid for at least five, and a minimum death cover — the *rechnungsmäßige und
außerrechnungsmäßige Zinsen* contained in a *Kapitalabfindung* are **entirely free of income tax**
[R6] [REG-R45]. That is a better outcome than taxing half the *Unterschiedsbetrag*, not the same
one, and it is what makes an *Altvertrag*'s surrender and commutation rates close to nil. **The
pre-2005 conditions themselves were not established and are asserted nowhere in delib**
[unverified], which is why the reference model does not represent that cohort. Annuity payments run
on the *Ertragsanteil* basis in every cohort.

A German in-force book therefore carries **at least three tax cohorts** — pre-2005, 2005–2011 with
the age test at 60, and 2012 onwards with it at 62 — cut by the *Alterseinkünftegesetz* watershed of
1 January 2005 and the 31 December 2011 line [REG-R38] [REG-R45]. **delib's composite is a post-2011
contract**: `issue_year` is 2026 on the anchor, the table's earliest vintage is 2005, and the
pre-2005 cohort appears in it nowhere.

On the annuity side, **at age 65 the *Ertragsanteil* is 18 %** [R5] [S12] — the only value of the
statutory table any search established (gap 8) — and,
unlike the Schicht-1 *Rentenfreibetrag*, **the percentage is what is frozen**, so surplus increases
are taxed at the same light rate [REG-R41].

**The two regimes are why the election is economically live** rather than a formality. **delib
computes no tax anywhere** [REG-R38], so the implementation carries the election as a **take-up
rate** and says explicitly that the rate stands in for a tax comparison the model does not perform.

### The *Rückkaufswert* under § 169 VVG

The surrender right exists and its value is governed by § 169 VVG [R1] [REG-R28]. The base measure is
the ***Deckungskapital*** computed by recognised actuarial rules **on the calculation bases of the
premium calculation** [REG-R28]. The *Zeitwert* rule of Abs. 4 is the boundary rather than the rule
here, because the classic contract's benefit is guaranteed [R1], and **what the classic surrender
value is computed as was not established at article level in this product's own research** (gap 12).

**The floor is the operative constraint, and it is not the *Stornoabzug*.** § 169 Abs. 3 requires at
least the *Deckungskapital* that results from **spreading the charged acquisition and distribution
costs evenly over the first five contract years**, with the supervisory *Zillmer* rules unaffected
[REG-R28]. That is a floor on the **value**, not a cap on the **charge**: the DeckRV governs what the
insurer may reserve and § 169 VVG what it must pay, so a model carrying a zillmered reserve applies
both separately, the tighter binding [REG-R16] [REG-R28]. In the first five contract years of a
zillmered tariff the floor binds by a wide margin, and it is the whole reason a German surrender
value in year two is not simply zero. **The *Stornoabzug*** may then be deducted, and only if
**agreed, quantified (*beziffert*) and appropriate (*angemessen*)** — three cumulative conditions,
the burden of proof on the insurer — while **a deduction in respect of not-yet-amortised *Abschluss-
und Vertriebskosten* is void** [R1] [REG-R28]: the statutory answer to *Zillmerung*, which may not
be recovered from the surrendering policyholder as a named deduction. **No *Stornoabzug* percentage,
surrender-value table or charge-recovery schedule was established at any carrier** (gap 12).

### *Beitragsfreistellung* under § 165 VVG

The policyholder may **at any time, for the end of the current insurance period, demand that the
insurance be converted into a premium-free insurance, provided the agreed minimum insurance benefit
is reached** [R2] [REG-R28]; the right is statutory and unconditional apart from that threshold, and
**if the minimum is not reached the insurer must instead pay the surrender value attributable to the
insurance, including profit shares, under § 169** [R2] — a small contract cannot be made paid-up, it
is cashed out. **The premium-free benefit is calculated according to recognised principles of
actuarial mathematics, using the calculation basis of the premium calculation, on the basis of the
surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each insurance
year** [R2]. Three consequences reach the model: the paid-up value is **derived from the surrender
value**, so a model computing them independently will not reconcile; it uses the **premium basis**,
so the paid-up contract keeps its guarantee vintage; and it is **tabulated per insurance year**.

**The difference from *Kündigung* is the point.** *Beitragsfreistellung* keeps the contract alive —
its guarantee vintage, its *Rechnungszins* and its guaranteed *Rentenfaktor* all survive on a reduced
benefit — while *Kündigung* ends it for the *Rückkaufswert* [R1] [R2]. Where an old contract carries
a high legacy *Rechnungszins*, that difference is worth a great deal, and it is why paid-up
conversion and lapse **must be separate decrements**; German lapse is in fact three-way, § 166 VVG
converting automatically to *prämienfrei* on the insurer's termination and in the § 38
premium-default case rather than ending cover [REG-R28] [REG-R30]. **The
*Mindestversicherungsleistung* threshold was not established at any carrier** (gap 22).

---

## Riders and options

**In scope and modeled.** The ***Rentengarantiezeit*** as a selectable term in years, base 10 [R24]
[S9] [S13]; the ***Kapitalwahlrecht*** as a take-up rate at *Rentenbeginn* [S12] [R6] [R21]; the
death-benefit **form** switch across the three documented designs [S1] [R24] and the with-surplus
variant [R24]; the ***Dynamik*** as an annual increase rate, base 0 and on for one model point [S4];
***Beitragsfreistellung*** as a deterministic election with the *Mindestversicherungsleistung*
cash-out branch [R2]; and the three payout-phase *Überschussverwendung* systems [R19] [R20] [R24].

**Documented and deliberately not modeled**, each with its reason. The
***Hinterbliebenenrenten-Zusatzversicherung***, published by the GDV as a **separate model condition
set attaching to this contract** [S10] — it needs a second life and no model point carries one. The
***Berufsunfähigkeits-Zusatzversicherung***, a named section with its own conditions in the same
pack [S4] and delib's `berufsunfaehigkeit` product in standalone form. ***Zuzahlung***: **no source
in this corpus named it** (gap 15), the one option the research brief asked for that the corpus does
not support at all. ***Bonusrente*** [R24] and ***Beitragsverrechnung*** (gap 16) as
accumulation-phase surplus systems, and surplus **invested in an internal fund** [S12]. The § 163 VVG
/ *Treuhänderklausel* adjustment of the guaranteed *Rentenfaktor* [R3] [R17] [REG-R27], and § 169
Abs. 6 **reduction of surrender values** [R1] — both supervised or contested channels with no
published trigger a deterministic model could key off.

---

## Variations across insurers

The corpus supports **structural** variation tables but **not** quantitative range tables for the
parameters that matter most — *Rentenfaktor* levels, charges, entry ages, premium envelopes and
surplus rates — because no search in this session returned a number for any of them at any carrier.
Where a row reads "not established", that is the finding.

| Carrier | Documents | Status of the classic deferred annuity |
|---|---|---|
| GDV (industry model wording) | [S1] [S2] [S3] [S10] | Model conditions maintained; a 2021 edition seen; **expressly non-binding** — "Diese Bedingungen sind unverbindlich" [S2], use optional [S3] |
| Zurich Deutscher Herold | [S4] [S5] [S6] [S7] [S16] [S17] | *Verbraucherinformation* published 2021, 2022 and **Fassung 01/2026** [S4]; but reported among the carriers that stopped [R22] — **unresolved**, gap 9 |
| CosmosDirekt (Cosmos Leben, Generali) | [S8] | AVB **LA 904 A** published; vintage not established (gap 5); Generali reported among those that stopped [R22] |
| NÜRNBERGER | [S9] | AVB for tariff **NIR3301**, *mit Rentengarantiezeit* in the title |
| Debeka | [S11] [S12] | **Withdrawn.** Replaced from 1 July 2016 by five "Chance" variants, the safest guaranteeing **0,5 %** and the riskiest nothing [R22] [S12] |
| Allianz | [S13] | **Withdrawn.** Replaced by KomfortDynamik: **60 %, 80 % or 90 % of the premiums paid** guaranteed at *Rentenbeginn*, selectable, 80 % standard [S13] [R22] [R23] |
| Mecklenburgische | [S14] | *Vertragsinformationen* for "Rente flex"; the distinguishing feature is not established |
| Konzern Versicherungskammer | [S15] | Annual *Überschussverteilung 2026* published; **no rate established** |
| Stuttgarter | [S18] | *Allgemeine Informationen* pack dated 2020 |
| DEVK | [S19] | Unit-linked only; used here for the death-benefit contrast |

| Design item | Observed variation | Source |
|---|---|---|
| Death benefit | *Beitragsrückgewähr* premiums-only, named in the GDV wording; premiums **plus attributable surplus**, which "can be agreed"; the accumulated *Deckungskapital*; or a *Hinterbliebenenrente* as a rider. `max(fund, premiums)` is **unit-linked wording**, its classic analogue [unverified] | [S1] [S10] [R24]; [S19] |
| Guaranteed *Rentenfaktor* basis | DAV 2004 R at a **0 % interest basis** — one carrier, at an unestablished vintage | [S8]; gap 5 |
| *Rentengarantiezeit* | 5, 10, 15, 20, 25, 30+ years offered; typically 15 at retirement ages 61–70 and 10 at 71+; most choose 10–20; cost 3 € / 15 € / 46 € a month at 10 / 20 / 30 years on a 573 € base | [R24] [S9] [S13] |
| Accumulation surplus system | *Verzinsliche Ansammlung*, *Bonusrente* and internal-fund investment all established; *Beitragsverrechnung* **not established** | [R24] [S12]; gap 16 |
| *Rentenfaktor* levels, declared surplus rates, charge levels, issue envelopes, behavioural rates | **Not established at any carrier for any year** | gaps 3, 4, 13, 14, 20 |

**What does not vary.** Three things are the same everywhere in the corpus and all three are legal
rather than commercial facts: the **two-phase structure with a fixed *Rentenbeginn*** is definitional
[S1] [S4] [S8] [S9] [R24]; the ***Rückkaufswert*** and ***Beitragsfreistellung*** rights are
statutory and *halbzwingend*, §§ 165 to 170 VVG not being variable to the policyholder's detriment
under § 171 VVG [REG-R22] [REG-R28]; and the **unisex tariff** has been compulsory since 21 December
2012 [REG-R34], which is why sex appears nowhere in the pricing of this composite even though the
annuity tables behind it are sex-specific raw material [REG-R47] [REG-R49]. Against that, **two limbs
of the composite's core rest on a single carrier each**: the *Rentenfaktor* comparison rule [S4],
restated only by secondary material [R24], and the conversion basis [S8], at a vintage that document
itself marks as time-dependent and that the corpus could not date (gap 5).

---
## Regulatory context

**Contract law — the VVG.** German life contract law sits in a separate statute from the prudential
one, and its **Kapitel 5 (§§ 150–171) is *halbzwingend***: §§ 152 Abs. 1 and 2, 153 to 155, 157, 158,
161 and 163 to 170 may not be varied to the policyholder's detriment under § 171 VVG [REG-R22]. That
is why a model may treat the surrender-value floor, the paid-up right and the profit-participation
entitlement as **contractual facts** rather than tariff options. The operative articles are **§ 153**
(*Überschussbeteiligung*, *Bewertungsreserven* under Abs. 3) [R4] [REG-R24]; **§§ 154 and 155** (the
*Modellrechnung*, and the annual *Standmitteilung* disclosing how much of the profit participation is
guaranteed) [REG-R25]; **§ 163** [R3] [R17] [REG-R27]; **§ 165** [R2] [REG-R28]; **§ 166** [REG-R28];
**§ 168** [REG-R28]; **§ 169** [R1] [REG-R28]; **§§ 8 and 152** (*Widerruf*) [REG-R23]; and
**§§ 150, 157, 158 and 161** on consent, age misstatement, risk increase and suicide [REG-R26]
[REG-R30]. The **§ 154 *Modellrechnung*** fixes what a published German illustration looks like:
quantified statements about benefits beyond the guaranteed ones must be accompanied by the possible
*Ablaufleistung* computed on the premium calculation bases at three rates set by § 2 Abs. 3
VVG-InfoV — the *Höchstrechnungszins* times 1,67, that rate plus one point and that rate minus one
[REG-R25] — so at 1,00 % the statutory triple is **1,67 % / 2,67 % / 0,67 %**. The reference
implementation does **not** use those rates; its declared-rate path is a [std] scenario anchored on
observed market averages, and it says so.

**Prudential — the VAG, the DeckRV and the MindZV.** BaFin supervises German life insurers under
Solvabilität II as transposed into the VAG, with no second national supervisor [REG-R21] [REG-R5]
[REG-R6]. Two ministerial regulations carry the arithmetic. The **DeckRV** fixes the
*Höchstrechnungszins* in § 2 [REG-R14] [REG-R15], the *Höchstzillmersätze* in § 4 — **25 ‰ of the
*Beitragssumme*** since 1 January 2015, 40 ‰ before, the rate at conclusion applying for the whole
term [REG-R16] — and the *Referenzzins* behind the ***Zinszusatzreserve*** in § 5 Abs. 3 [REG-R17].
The **MindZV** puts the arithmetic floor under the *Überschussbeteiligung*: **90 %** of the
investment result **less the *Rechnungszinsen***, **90 %** of the risk result and **50 %** of the
remaining result, with the *Direktgutschrift* deducted, *Alt-* and *Neubestand* separate, and a
negative minimum replaced by zero — a minimum **transfer to the RfB**, not a minimum payout [REG-R18]
[REG-R10] [REG-R19]. The **LVRG 2014** produced that shape [REG-R20]. The ***Zinszusatzreserve***
exists in no other jurisdiction in this repository and is why a book of high-vintage annuity
contracts is expensive: it arises where the § 5 Abs. 3 *Referenzzins* falls below a contract's tariff
rate, and the MindZV *Sicherungsbedarf* test compares a Bundesbank month-end swap rate with **the
highest *Rechnungszins* applicable to the contract over the next fifteen years** — a window that
"bites hardest on annuity business" [REG-R17] [REG-R18]. **delib does not compute it**; this document
cites it rather than specifying it.

**Biometric bases.** The mortality basis for every German annuity promise is **DAV 2004 R**, named in
an insurer's own AVB for exactly this product [S8]. It is a ***Generationentafel*** — a
two-dimensional basis in attained age and calendar year containing mortality by birth cohort
including the expected future change [R13] [R15] [REG-R49] — built from a second-order base table, a
first-order base table, second- and first-order mortality trends and an age adjustment
(*Altersverschiebung*) [R12], with **first-order probabilities carrying safety margins relative to
the second-order ("realistic") probabilities in order to assess the risk prudently** [R12]. It has
been in use since June 2004, was intended for new business from 2005, and the DAV **reissued its
derivation guideline on 28 June 2023** [R12] [R13] — which is itself the evidence that no successor
has displaced it, and the fact behind the longevity trigger of the § 163 VVG adjustment right. A
companion in-force table, **DAV 2004 R-Bestand**, exists for annuities already in payment [R14]
[REG-R49].

**The table is the property of the Deutsche Aktuarvereinigung, is not public and is not redistributed
by delib.** The library cites it by name and ships a [std] proxy anchored so its own worked example
reproduces exactly. A replacement must preserve three things: the **generational structure** — a
`q(x, τ)` surface, not a period table, because a period-table proxy priced at a 40-year-old's
annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the
model [REG-R49]; the **first-order margin over second order**, which for an annuity runs in **two
dimensions**, level and trend [REG-R47] [REG-R49]; and the **age-adjustment convention** [R12]. The
free, redistributable public analogue is Destatis's *Generationensterbetafeln für Deutschland*
[REG-R52]. The tables are sex-distinct while the tariff sold since *Test-Achats* must be unisex —
C-236/09, 1 March 2011, invalidating the Article 5(2) derogation **with effect from 21 December
2012**, with § 20 Abs. 2 Satz 1 AGG repealed [REG-R34]; **neither half of that sentence was
established by any search in this product's own research** (gap 21). A model point may carry `sex`
for **decrement** purposes and **must not** let it enter the premium or the *Rentenfaktor*.

**Taxation, conduct and accounting.** The annuity is taxed on the ***Ertragsanteil*** under § 22
EStG at **18 % for age 65** [R5] [R24] [REG-R41]; the *Kapitalabfindung* falls under § 20 Abs. 1
Nr. 6 EStG and the *Halbeinkünfteverfahren* on the 12/62 rule [R6] [REG-R45]. **Not established, and
not asserted anywhere in this library**: the rate on the taxable half in the general case, the
*Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
*Kleinbetragsrente* threshold (gap 23). **delib computes no tax**: every benefit cash flow is gross
of *Kapitalertragsteuer*, *Solidaritätszuschlag* and *Kirchensteuer* [REG-R38]. The pre-contractual
pack — *Verbraucherinformation* [S4]–[S7], *Vertragsinformationen* [S14], *Kundeninformation* [S19],
*Allgemeine Informationen* [S18] — is one object under §§ 6, 7 and 7a–7c VVG with the VVG-InfoV
[REG-R31]; distribution sits under the IDD and § 34d GewO [REG-R33]; BaFin's *Merkblatt 01/2023* on
*Wohlverhaltensaufsicht* governs product governance and value for money [REG-R35]. The statutory
balance sheet is the HGB one of §§ 341–341o HGB with the RechVersV and BerVersV [REG-R54], and its
*Deckungsrückstellung* is **not** the Solvency II best estimate — an insurer carries two liability
measures, and the *Überschussbeteiligung*, the *Zinszusatzreserve* and the *Bewertungsreserven* test
all run on the **HGB** side [REG-R14] [REG-R54]. IFRS 17 would measure this contract under the
variable fee approach [REG-R55]; actuarial work sits under the DAV *Fachgrundsätze* and the § 141 VAG
*Verantwortlicher Aktuar*, a role the MaGo keeps distinct from the *versicherungsmathematische
Funktion* [REG-R56] [REG-R11] [REG-R21]; policyholder protection in a failure runs through
**Protektor** under §§ 221–236 VAG [REG-R12].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-klassische_rentenversicherung-r1
[R10]: #delib-klassische_rentenversicherung-r10
[R11]: #delib-klassische_rentenversicherung-r11
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R14]: #delib-klassische_rentenversicherung-r14
[R15]: #delib-klassische_rentenversicherung-r15
[R16]: #delib-klassische_rentenversicherung-r16
[R17]: #delib-klassische_rentenversicherung-r17
[R18]: #delib-klassische_rentenversicherung-r18
[R19]: #delib-klassische_rentenversicherung-r19
[R2]: #delib-klassische_rentenversicherung-r2
[R20]: #delib-klassische_rentenversicherung-r20
[R21]: #delib-klassische_rentenversicherung-r21
[R22]: #delib-klassische_rentenversicherung-r22
[R23]: #delib-klassische_rentenversicherung-r23
[R24]: #delib-klassische_rentenversicherung-r24
[R3]: #delib-klassische_rentenversicherung-r3
[R4]: #delib-klassische_rentenversicherung-r4
[R5]: #delib-klassische_rentenversicherung-r5
[R6]: #delib-klassische_rentenversicherung-r6
[R7]: #delib-klassische_rentenversicherung-r7
[R8]: #delib-klassische_rentenversicherung-r8
[R9]: #delib-klassische_rentenversicherung-r9
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R12]: #delib-reg-r12
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R20]: #delib-reg-r20
[REG-R21]: #delib-reg-r21
[REG-R22]: #delib-reg-r22
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R38]: #delib-reg-r38
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
