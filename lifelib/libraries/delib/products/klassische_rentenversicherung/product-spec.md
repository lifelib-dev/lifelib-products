# Product Specification

**Status:** Draft, 2026-08-29 (all cited sources accessed 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a German **klassische aufgeschobene private
Rentenversicherung** — the classic deferred private annuity of *Schicht 3*, in which a premium
accumulates in the *Deckungskapital* (policy reserve) of the insurer's general account at a
guaranteed *Rechnungszins* (technical interest rate), participates in the
*Überschussbeteiligung* (profit participation), and is converted at a contractually fixed
*Rentenbeginn* (annuity commencement date) into a lifelong *Leibrente* at a *Rentenfaktor*
(annuity factor) — or taken instead as a lump sum under the *Kapitalwahlrecht*. **It does not
describe any single insurer's contract.** Facts carrying a source tag — [S#] (primary product
documents: *Allgemeine Versicherungsbedingungen*, *Verbraucherinformation*, *Kundeninformation*,
GDV *Musterbedingungen*, insurer product pages, surplus declarations) and [R#]
(product-specific regulatory and actuarial references), both numbered per
`_research/klassische_rentenversicherung.md` and resolved in `sources.md` (same directory;
**numbering frozen, never renumbered**), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is separate and also
frozen) — are attributed to the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each carries a numbered footnote giving the
rationale and, where the research file recorded one, the observed range. Claims no search result
corroborated are flagged [unverified].

**Retrieval conditions — read this before relying on a single number below.** Direct HTTP egress
from the build environment is blocked by an organisation network policy: `WebFetch` and `curl`
are refused with HTTP 403 for `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de` and
every insurer host named here. **No document cited anywhere in this file was retrieved.**
Everything rests on `WebSearch` result summaries, and the session's shared budget was exhausted
after eighteen queries on this product. A delib citation is a **pointer, not a certificate**: it
names the instrument a claim should be checked against; it does not assert that anyone checked
it. The consequence here is concentrated and must be said plainly — **the corpus establishes the
mechanics of this product thoroughly and its levels barely at all.** No *Rentenfaktor* level, no
declared surplus rate, no charge parameter, no entry-age or premium envelope and no behavioural
rate was established at any carrier for any year. Every one of those is **[std]** below, and none
is presented as a market rate.

**The composite draws on ten carriers and one industry body.** The GDV *Musterbedingungen* for
this exact product [S1] [S2] [S3] and for its survivor's-annuity rider [S10] give the market's
shared drafting template; the Zurich Deutscher Herold *Verbraucherinformation* series [S4]–[S7]
[S16] [S17] gives the same document across three vintages and is the only source for the
*Rentenfaktor* comparison rule; the CosmosDirekt AVB LA 904 A [S8] is the only document whose
conversion basis a summary returned in terms; NÜRNBERGER tariff NIR3301 [S9] carries the
*Rentengarantiezeit* in its own title; Debeka [S11] [S12] states the *Deckungskapital* definition
and has withdrawn the product; Allianz [S13] and the trade press [R22] [R23] record the successor
designs; Mecklenburgische [S14], Konzern Versicherungskammer [S15], Stuttgarter [S18] and DEVK
[S19] fill in the document taxonomy and the unit-linked contrast. Where a row below reads "not
established", **that is the finding, not an omission**.

**Out of scope**, and named so the boundary is explicit: the *Basisrente* (Schicht 1), the
*Riester-Rente* and *betriebliche Altersversorgung* (Schicht 2); the *fondsgebundene* and
*indexgebundene* variants; the *sofort beginnende Rentenversicherung*, whose machinery is this
product's payout phase and which is why an immediate-annuity document [S16] is cited here at all;
the *kapitalbildende Lebensversicherung*, which shares this surplus and reserve chassis and is the
primary home of the four-component surplus decomposition; and *Gruppenversicherung*, *private
Krankenversicherung*, *Sterbegeldversicherung* and institutional pension-risk transfer.

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
   is determined by comparing two factors [S4] [S13]; and the *Kapitalwahlrecht* election, if any,
   takes effect [S12] [R21].
2. **The guarantee is a rate, and a property of the contract's vintage rather than of the
   market.** The *Rechnungszins* at which the *Sparbeitrag* accumulates is capped for new business
   by the statutory *Höchstrechnungszins* of § 2 *Deckungsrückstellungsverordnung* [R7] [R11]
   [REG-R14], **and the rate applicable at conclusion then stays with the contract for its whole
   term** [REG-R14]. A German life book is a layered stack of guarantee vintages — 4,00 % for
   07/1994–06/2000 down to 0,25 % for 2022–2024 and back to 1,00 % from 2025 [REG-R15] — so the
   *Rechnungszins* is a **model-point attribute, not a global assumption**. An insurer may also
   guarantee less than the cap, and does: CosmosDirekt's conversion basis is "an underlying
   interest rate (currently 0 percent p.a.)" [S8]; Debeka's safest post-2016 variant guarantees
   0,5 % [R22].
3. **The *Rentenfaktor* is a guarantee with upside, not a fixed conversion rate.** The
   *garantierter Rentenfaktor* is fixed at inception on the *Rechnungsgrundlagen* then in force
   [R24]; at *Rentenbeginn* a second, current factor is computed and **the higher of the two is
   guaranteed for the annuity payment period** [S4]. A model applying only the guaranteed factor
   understates the benefit whenever the current tariff is richer.
4. **The classic tariff is the market's reference chassis rather than a live new-business
   product.** Debeka "will no longer offer classical annuity insurance", replacing it from 1 July
   2016 with five "Chance" variants [R22] [S12]; Allianz replaced it with KomfortDynamik, a
   60/80/90 % premium-guarantee hybrid [S13] [R23]; and the trade press reports Allianz, Zurich and
   Generali as having stopped before Debeka did [R22]. Yet Zurich still publishes a
   *Verbraucherinformation für Konventionelle Versicherungen* for the deferred annuity in the
   **Fassung 01/2026** [S4] and CosmosDirekt still publishes AVB whose *Rentenfaktor* is struck on
   DAV 2004 R [S8]. **The two statements are in tension and this file does not resolve them**
   (gap 9). That is exactly why the right unit of description is a **composite of a chassis**, and
   it is the role a lifelib reference model is for: the in-force book still runs on this design.

**Market size.** German life insurers, *Pensionskassen* and *Pensionsfonds* together took premium
income of **94,6 Mrd €** in 2024, up 2,8 %, of which *laufende Beiträge* were **66,3 Mrd €**, roughly
flat, and *Einmalbeitragsgeschäft* about **28 Mrd €**, up about 10 %; the contract count fell 1,4 %
to **80,3 Mio** [REG-R53]. On the BaFin basis the life segment's *verdiente Bruttobeiträge* were
**90,4 Mrd €** — a different population on a different basis, and the two must never appear in one
table [REG-R53]. The GDV taxonomy reports *Rentenversicherungen* as one class covering both this
product and the immediate annuity, so **no figure isolating the classic deferred annuity was
established** [REG-R53]. The reading that matters is the *Einmalbeitrag* shift, which is why the
model point table carries a single-premium point. For credited-rate context, the average *laufende
Verzinsung* for **2025** was **2,53 % Klassik / 2,58 % Neue Klassik**; for **2026** the sources give
2,6–2,7 %, 2,87 % and 2,54 % — three incompatible averages [REG-R53].

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
| Sparte | Life insurance under Anlage 1 VAG; BaFin supervision under the VAG as transposed Solvabilität II | [REG-R5] [REG-R21] |
| Lives basis | Single life. The survivor's annuity is a separate *Zusatzversicherung* with its own GDV model conditions, not a benefit of the base contract | [S10] |
| Premium form (model-point parameter) | (i) `laufend` — level recurring premium over the *Aufschubzeit*; (ii) `einmal` — *Einmalbeitrag* | (i) [S11]; (ii) [REG-R53]; split **[std]** (1) |
| Entry ages | 18 to 62 | **[std]** (2) |
| *Aufschubdauer* | 5 to 40 years | **[std]** (2) |
| *Rentenbeginn* age | 62 to 72; representative **67** | **[std]** (2) |
| Age basis | Age last birthday at inception, stepping at the policy anniversary | **[std]** (3) |
| Sex | Recorded, and **may not enter the tariff**: sex-based premium and benefit differences are prohibited for contracts concluded from 21 December 2012 | [REG-R34] |
| Premium envelope | 600 € to 24 000 € a year recurring; 5 000 € to 250 000 € single | **[std]** (2) |
| Vintage | *Neubestand* — concluded from 29 July 1994 | [REG-R11] |
| Anchor model cell | Male, issue age 50, issue year 2026, *Aufschubdauer* 17 years (*Rentenbeginn* at 67), 3 000,00 € recurring annual premium, *Rechnungszins* 1,00 %, *Beitragsrückgewähr* death benefit, *Rentengarantiezeit* 10 years, *Kapitalwahlrecht* take-up 30 % | **[std]** (4) |

1. **The market split between recurring and single premium was not established for this product**
   (gap 13). What is established is the aggregate: *Einmalbeitragsgeschäft* is about 30 % of German
   life premium income and grew about 10 % in 2024 against a flat recurring book [REG-R53]. The
   recurring form is the one [S11]'s accumulation mechanics describe and is therefore
   representative; the single-premium form is carried as a model-point value because the aggregate
   says it cannot be ignored.
2. **The entire issue envelope is unestablished at every carrier** (gap 13): no minimum or maximum
   premium, no *Aufschubdauer* limits, no entry ages and no *Rentenbeginn* window was returned for
   any German carrier. These are round-number placeholders chosen so the model point table can
   carry an interior anchor and boundary points either side, and should be replaced wholesale by
   anyone with a *Tarifblatt*. The one age with an external anchor is **67**, the
   *Regelaltersgrenze* of the statutory scheme.
3. No German source in the corpus states an age convention for this product. Age last birthday,
   stepping at the anniversary, is the delib-wide convention registered as `age_basis = "ALB"` in
   `tests/de_registry.py`. It matters less here than in a protection product, because the
   *Rentenfaktor* rather than a mortality lookup fixes the benefit amount.
4. Issue age 50 with a 17-year *Aufschubzeit* puts four things inside one projection: the whole
   accumulation phase in seventeen rows; the § 20 Abs. 1 Nr. 6 EStG **twelve-year** threshold at
   duration 12 and its **age-62** partner at duration 13 [REG-R45], together the strongest driver
   of German Schicht-3 surrender behaviour; the *Rentenbeginn* at 67; and a payout phase long
   enough for the *Rentengarantiezeit* to expire inside it. The 3 000,00 € premium is a round
   number; the 30 % *Kapitalwahlrecht* take-up is a pure modeller's view (gap 20).

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
| Premium cessation | On death, on *Beitragsfreistellung*, on surrender and at *Rentenbeginn* | [S1] [R2] |
| Non-payment path | Life insurance does not lose cover on a missed *Folgeprämie*: after a *qualifizierte Mahnung* in Textform with a minimum two-week period, § 166 VVG converts the contract to *prämienfrei* rather than terminating it | [REG-R28] [REG-R30] |

5. **No *Ratenzahlungszuschlag* percentage was established at any German carrier** (gap 14). The
   mechanic is standard and not in doubt; the levels are a monotone [std] ladder in which the
   monthly mode costs 5 % more than the annual one. Note the interaction with *Zillmerung*: § 4
   DeckRV takes the *Zillmersatz* on the *Beitragssumme*, the sum of all premiums payable
   [REG-R16], so the loading enters the acquisition-charge base as well as the premium.
6. No source establishes whether German deferred-annuity tariffs commonly permit a paying term
   shorter than the deferment. The representative design equates them; the model carries
   `prem_term_y` separately so an abbreviated-premium point can be built.
7. The *Dynamik* option is **established from a primary document** — a named section of the Zurich
   pack with its own condition set [S4] — so its existence and its documentary form are facts.
   **Its increase percentage, its basis, whether fresh underwriting applies and how many refusals
   end it are all unestablished** (gap 15). The implementation carries `dynamik_rate`, base 0, with
   5 % on one point purely to exercise the mechanic.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Main benefit | A *Leibrente* payable for the annuitant's lifetime from *Rentenbeginn*, monthly | [S1] [S4] [S13] [R24] |
| Payment timing | Monthly **in advance**. **Whether the market pays in advance or in arrears was not established** (gap 19), and this is a first-order modelling parameter | **[std]** (8) |
| Conversion capital | The contract value used for annuitisation **includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general contract data** | [S9] |
| Conversion rule | `monthly annuity = conversion capital / 10 000 × Rentenfaktor` | [R24] |
| *Rentenfaktor* applied | `max(garantierter, aktueller)` — at the start of annuity payments a second factor is compared with the guaranteed one and **the higher of the two is guaranteed for the annuity payment period** | [S4]; restated from the other side by [R24] |
| *garantierter Rentenfaktor* | Fixed at inception on the *Rechnungsgrundlagen* then in force, with a *Sicherheitsabschlag* making it lower than the current factor. Representative 28,00 € per month per 10 000 € at *Rentenbeginn* 67 | mechanic [R24] [S8]; **level [std]** (9) |
| Its mortality basis | **DAV 2004 R**, named in an insurer's own AVB: calculated "on the basis of a recognised mortality table (currently DAV 2004 R)" | [S8] [R12] [R13] [REG-R49] |
| Its interest basis | **0 % p.a.** at one carrier — a deliberate prudential margin below the *Höchstrechnungszins* | [S8]; vintage unestablished (gap 5) |
| *aktueller Rentenfaktor* | The carrier's **then-current immediate-annuity tariff**: the bases at *Rentenbeginn* "relate to the interest rate and mortality table that the company uses at that time for immediately beginning annuities" | [S13]; [R24]; **level [std]** (9) |
| Annuity in payment | The sum of a *garantierte Rente* and an *Überschussrente*; only the guaranteed part is a promise | [R20] |
| *Überschussverwendung* in payment | Policyholder's choice of *konstante*, *teildynamische* or *volldynamische Rente* | [R19] [R20] [R24] |
| *Bewertungsreserven* in payment | Participation **continues during the annuity payment period** | [S4] [R4] |
| *Rentengarantiezeit* | 10 years representative; 5, 10, 15, 20, 25 or 30+ offered; typically 15 years for retirement ages 61–70 and 10 for 71 and above; most choose 10 to 20 | [R24]; in the tariff name at NÜRNBERGER [S9]; selectable with a floor at Allianz [S13] |
| Its cost | Against 573 € a month with no guarantee period, a 10-year period costs **3 €**, 20 years **15 €**, 30 years **46 €** — roughly 0,5 %, 2,6 % and 8,0 % of the annuity | [R24] (percentages computed here from the source's own figures) |
| Death benefit before *Rentenbeginn* | ***Beitragsrückgewähr*** — the insurer refunds all premiums paid — in the premiums-only form. Two documented alternatives: premiums **plus the attributable *Überschussbeteiligung***, which "can be agreed"; and payment of the accumulated *Deckungskapital* | [S1] names the term in the model wording; three forms [R24] |
| A `max(...)` death benefit | Established for the **unit-linked** sibling — "the fund value at the date of death but at least the sum of the premiums paid (*Beitragsrückgewähr*)" — its classic analogue is **[unverified]** | [S19]; classic form **[std]** (10) |
| What it is **not** | There is no separate *Versicherungssumme*. The benefit is defined off the premiums paid or off the accumulated fund, never off an independently chosen sum insured | [S19] [R24] |
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
   (gap 3). The only figure the corpus contains is a teaching illustration: 100 000 € at a factor
   of 25 gives 250 € a month [R24]. The rating house's own article "Was bedeutet der Rentenfaktor
   und wie hoch ist er?" returned no level [R19], and the "Rentenfaktor-Check 2025" is titled as
   data and returned none [R24]. The values used here — guaranteed 28,00 €; current 32,00 € base,
   25,50 € low, 35,00 € high, all at *Rentenbeginn* 67 — are **anchors chosen so the worked example
   reproduces exactly and the `max()` rule is exercised in both directions**. They are not market
   rates. That current factors have moved with the *Höchstrechnungszins* is directionally supported
   by the mechanics [S8] [S13] [R7] and quantitatively [unverified].
10. The `max` form is offered as a model-point value because it is the shape the market's
    unit-linked wording uses [S19] and the obvious classic counterpart, and because a German
    contract is not eligible for the § 20 Abs. 1 Nr. 6 half-income treatment unless the
    *Todesfallleistung* meets the *Mindesttodesfallschutz* test [REG-R45] — a constraint that
    pushes designs towards the larger of two measures. **No classic document in this corpus states
    it**, so the base case is the plain *Beitragsrückgewähr* the GDV wording names [S1].
11. The market convention is a declaration a set period before *Rentenbeginn*, and no document or
    summary named a period at any carrier (gap 11). The implementation treats the election as
    taking effect **at** *Rentenbeginn* with no notice modelling, because on an annual grid a
    notice period inside the last policy year moves nothing.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence | **None for the annuity itself.** A deferred annuity's biometric risk is longevity, which underwriting cannot select against in the insurer's favour; the pre-*Rentenbeginn* death benefit is the premiums paid or the accumulated fund, so there is no sum at risk to underwrite | structure [S19] [R24]; **[std]** (12) |
| Rider underwriting | The *Berufsunfähigkeits-Zusatzversicherung* in the same pre-contractual pack has its own special conditions and its own underwriting | [S4] |
| Rating factors | Entry age and *Aufschubdauer* through the tariff; **sex may not be a rating factor** from 21 December 2012 | [REG-R34] |
| *Anzeigepflicht* | Disclosure of the risk circumstances the insurer asks about in Textform; the insurer's rights lapse five years after conclusion, ten on intent or fraud | [REG-R30] |
| Age misstatement | § 157 VVG: the benefit changes in the ratio of the premium for the true age to the agreed premium | [REG-R30] |
| Consent of the insured | § 150 VVG requires written consent where a policy is on another person's death above ordinary funeral costs; reaches this product only through the death benefit | [REG-R26] |
| *Selbsttötung* | § 161 VVG excludes intentional suicide within three years, the insurer then still paying the *Rückkaufswert* including profit shares. **No source applies it to a *Beitragsrückgewähr***, where the benefit is the premiums back rather than a sum at risk | [REG-R26]; application here [unverified], not modeled (12) |

12. The absence of underwriting is a structural consequence of the benefit shape rather than a
    documented carrier practice: no source in this corpus states an underwriting rule for a German
    deferred annuity. It is [std] because the implementation acts on it — there is no rating
    factor, no select period and no substandard loading anywhere in the model. A carrier writing a
    *Beitragsrückgewähr* **plus surplus** death benefit has a small sum at risk and might well ask
    a question; nothing here establishes that it does.

### Charges

**This is the weakest area of the corpus.** No charge parameter was established for this product at
any German carrier (gap 14): not the *Abschluss- und Vertriebskosten* rate, not the
*Verwaltungskosten* in any form, not the *Ratenzahlungszuschlag*, not the payout-phase
administration charge and not the *Effektivkosten* disclosure. No *Produktinformationsblatt* and no
*Basisinformationsblatt* (PRIIP-KID) for a classic deferred annuity appears in the corpus at all.
The two figures the corpus does contain — an *Abschlussprovision* of **1 575 €** on an Allianz
specimen quotation, and total costs relative to the capital formed of **at most 0,95 € per 100 €** —
come from third-party analyses of **Schicht-1 and Schicht-2** variants and are [unverified] as
Schicht-3 levels [S13] [R23].

| Parameter | Representative value | Basis |
|---|---|---|
| Charge structure | **Premium-based deductions, not asset-based ones**, in the classic chassis: a portion of the premium is "intended for risk and cost coverage" and is deducted before the *Sparbeitrag* | [S11] |
| *Abschluss- und Vertriebskosten* (α) | **25 ‰ of the *Beitragssumme***, zillmered — charged against the earliest premiums until exhausted | cap [REG-R16]; use of the cap **[std]** (13) |
| Legacy α vintage | **40 ‰** for contracts concluded before 1 January 2015; the rate used at conclusion applies for the whole term | [REG-R16] [REG-R20] |
| *Verwaltungskosten* on premium (β) | 4,0 % of each gross premium | **[std]** (13) |
| *Verwaltungskosten* on the reserve (γ) | 0,20 % p.a. of the *Deckungskapital* | **[std]** (13) |
| *Risikobeitrag* (ρ) | The tariff mortality rate on the net amount at risk, `max(0, death benefit − Deckungskapital)` | structure [S11]; level follows the table |
| *Stornoabzug* | 2,0 % of the computed surrender value. A deduction is permitted **only if agreed, quantified (*beziffert*) and appropriate (*angemessen*)**, and **a deduction for not-yet-amortised acquisition and distribution costs is void** | [R1] [REG-R28]; level **[std]** (13) |
| Payout-phase administration | 1,5 % of each annuity instalment | **[std]** (13) |
| *Effektivkosten* | Required by the German disclosure regime; **no value established for this product** | gap 14 |

13. **Every charge level above is a placeholder and none is a market rate.** Two have an anchor of
    a kind. The α rate is set at the **statutory ceiling** of § 4 DeckRV — 25 ‰ of the
    *Beitragssumme* since 1 January 2015, 40 ‰ before [REG-R16] [REG-R20] — which is a real number
    in German law, but using the ceiling as the tariff rate is a modelling choice, not an
    observation. The *Stornoabzug* is 2,0 % because § 169 Abs. 5 requires it to be *beziffert* and
    *angemessen* [R1] [REG-R28], so a percentage is the right shape, and because it must not
    recover unamortised acquisition costs — which is what makes the § 169 Abs. 3 five-year-spread
    floor, not the deduction, the operative constraint on early surrender values. The β, γ and
    annuity-administration rates have no anchor at all and are sized so that the total load is of
    the order the one Schicht-1/2 figure implies (0,95 € per 100 € [S13] [R23]) without being
    presented as equal to it.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Kündigung* / *Rückkaufswert* | Available at any time for the end of the current insurance period while recurring premiums are payable. The base measure is the *Deckungskapital* computed by recognised actuarial rules **on the calculation bases of the premium calculation** | [R1] [REG-R28] |
| **The statutory floor** | § 169 Abs. 3 VVG: **at least the *Deckungskapital* that results from spreading the charged acquisition and distribution costs evenly over the first five contract years** — a floor on the value, not a cap on the charge, and independent of the supervisory *Zillmer* rules | [REG-R28]; at article level [unverified] here (gap 12) |
| *Stornoabzug* | Permitted only if agreed, quantified and appropriate; a deduction for unamortised acquisition costs is void; the burden of proof is on the insurer | [R1] [REG-R28] |
| § 169 Abs. 6 | The insurer may in defined cases reduce surrender values to be paid out — a solvency valve, **not modeled** | [R1] |
| Surrender in the payout phase | **None.** § 168 Abs. 1 gives the right where *laufende Prämien* are payable, Abs. 2 on a single premium where the occurrence of the obligation is certain; a life annuity already in payment is neither | [REG-R28]; reading **[std]** (14) |
| *Beitragsfreistellung* | The policyholder may **at any time, for the end of the current insurance period**, demand conversion into a premium-free insurance, **provided the agreed *Mindestversicherungsleistung* is reached** | [R2] [REG-R28] |
| Its value | Calculated by recognised actuarial principles **on the calculation basis of the premium calculation, on the basis of the *Rückkaufswert* under § 169 Abs. 3 to 5**, and **stated in the contract for each insurance year** | [R2] [REG-R28] |
| Below the minimum | The insurer must instead pay the surrender value attributable to the insurance, **including profit shares**, under § 169 — a small contract cannot be made paid-up; it is cashed out | [R2] |
| The *Mindestversicherungsleistung* | **Not established at any carrier.** Representative threshold: a guaranteed annuity of 30,00 € a month | gap 22; **[std]** (15) |
| Premium-default conversion | § 166 VVG converts automatically to *prämienfrei* rather than terminating cover — German lapse is a **three-way** decrement | [REG-R28] [REG-R30] |
| *Wiederinkraftsetzung* | Reinstatement of a paid-up contract exists as a documented process at one carrier and nothing more. **Not modeled** | [S11] |
| *Widerruf* | §§ 8 and 152 VVG. **Not modeled**; it sits inside the first-year lapse rate | [REG-R23] |
| Expiry | There is none. The contract ends on death after *Rentenbeginn*, on surrender, or on payment of the *Kapitalabfindung* | structure |

14. No German source in this corpus says whether a deferred annuity in payment may be surrendered.
    The reading follows from the text of § 168 VVG as recorded in the cross-product library
    [REG-R28] and from the fact that the insurer's obligation in the payout phase has already
    occurred; it is a reading, not a retrieved rule, and the implementation acts on it by setting
    the lapse rate to zero from *Rentenbeginn*.
15. § 165 VVG makes the paid-up right conditional on a *Mindestversicherungsleistung* [R2] and **no
    carrier's threshold was returned** (gap 22). 30,00 € a month is a round number chosen so one
    model point trips it and is cashed out instead of being made paid-up, which is the branch the
    statute actually cares about.

---

## Contractual mechanics

### The two phases and the *Rentenbeginn* boundary

The contract has two phases separated by the *Rentenbeginn*: the *Aufschubzeit*, over which
premiums are paid and the *Deckungskapital* accumulates, and the *Rentenbezugsphase*, over which
the annuity is paid [S1] [S4] [S8] [S11]. "Eine Aufschubzeit gibt es nur bei aufgeschobenen
Rentenversicherungen" — a deferment period exists only in a deferred annuity contract, the
definitional line separating this product from delib's `sofortrente` [R24].

**Three distinct things happen at the boundary** and a model that collapses them into one step
will get at least one wrong: the accumulated value is struck including surplus and
*Bewertungsreserven* [S9]; the *Rentenfaktor* is determined by comparing the guaranteed factor
with the then-current one [S4] [S13]; and the *Kapitalwahlrecht* election takes effect [S12]
[R21]. The technical notes therefore give the boundary its own numbered position in the processing
order rather than folding it into the year-end decrements.

Two further established facts cut against the obvious simplification. **The transition to annuity
payment is explicitly a key point for the *Bewertungsreserven* participation** [S4]: the share is
crystallised at the boundary rather than accruing smoothly. And **participation does not stop
there** — policyholders **also participate during the annuity payment period** [S4] [R4]. A model
treating the payout phase as a closed, non-participating run-off is wrong for this product.

### The *Deckungskapital* recursion

The definitional statement comes from an insurer: the *Deckungskapital* is **"the sum of the
contributions accumulated at the *Rechnungszins*, insofar as these are not intended for risk and
cost coverage"** [S11]. Debeka states the same split from the other direction [S12]. Unpacked into
the recursion an implementation carries — and this unpacking is a **reading** of [S11], not a
clause the corpus supplied in this form:

    Deckungskapital(t) = ( Deckungskapital(t-1) + Sparbeitrag(t) ) x (1 + Rechnungszins)
    Sparbeitrag(t)     = Beitrag(t) - Risikobeitrag(t) - Kostenbeitrag(t)

**The ordering of premium credit, charge deduction and interest accrual within a period is not
established by any source in this corpus** and is a [std] decision, stated explicitly in the
technical notes. The implementation credits the premium first, takes the charges next, and accrues
interest on the balance after both — the reading that makes the year-one interest credit largest,
and therefore the one that must be argued rather than assumed.

The *Deckungskapital* is what everything else is defined off: the death benefit in one of the two
common designs; the basis of the *Rückkaufswert* [R1] and of the *beitragsfreie
Versicherungsleistung* [R2]; and, with surplus and *Bewertungsreserven* added, the capital the
*Rentenfaktor* applies to [S9].

### The *Rechnungszins* and the guarantee-vintage stack

The *Rechnungszins* is the rate at which the *Sparbeitrag* is guaranteed to accumulate [S11]. It is
capped for new business by the *Höchstrechnungszins* of § 2 DeckRV [R7] [R11] [REG-R14] — the rate
market language calls the *Garantiezins*, although the two are not legally identical, because § 2
caps the **reserving** rate while the rate a policy guarantees is a tariff decision that may be
lower [REG-R14].

**From 1 January 2025 the rate is 1,00 %**, raised from **0,25 %** by the *Sechste Verordnung zur
Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024, BGBl. 2024 I
Nr. 250 [REG-R15], announced in the *Bundesgesetzblatt* on 24 July [R7] [R10] [R11]. **This was the
first increase since 1994**; every movement in the intervening thirty years was downward. The DAV
recommends 1,0 % for 2026 as well [R8]. The mechanism is standing — DAV recommends in November
2023, BMF adopts in late April 2024, effect from 1 January 2025 [R9] — a lead time of about
fourteen months, which makes the *Rechnungszins* of a tariff a parameter known well before it
binds. The full history is carried in the cross-product library, only its two most recent points
having been corroborated in this product's own research (gap 7): **3,50 %** to 06/1994; **4,00 %**
07/1994–06/2000; **3,25 %** 07/2000–2003; **2,75 %** 2004–2006; **2,25 %** 2007–2011; **1,75 %**
2012–2014; **1,25 %** 2015–2016; **0,90 %** 2017–2021; **0,25 %** 2022–2024; **1,00 %** from 2025
[REG-R15].

**The modelling consequence is decisive.** The increase applies only to contracts concluded from
the date of the increase onwards; existing contracts keep the rate they were written on [R7]
[REG-R14]. A German life book is a layered stack of guarantee vintages, and **the *Rechnungszins*
is a model-point attribute**. Two hard figures establish that an insurer may guarantee **less** than
the cap: CosmosDirekt's *Rentenfaktor* rests on "an underlying interest rate (currently 0 percent
p.a.)" [S8], and Debeka's safest "Chance" variant guarantees **0,5 %** [R22]. A model assuming the
guaranteed rate equals the statutory cap is wrong in the same direction at every carrier.

### *Überschussbeteiligung* in the *Aufschubphase*

*Überschussbeteiligung* is the participation of policyholders in the surpluses of the undertaking
[R24]. Its magnitude depends, in an insurer's own contractual words, on "many influences which are
unpredictable and only limitedly controllable by the company, with the most important influencing
factor being capital-market developments" [S8]. **That disclaimer is why surplus is modelled as a
declaration — an insurer-discretionary current assumption — and never as a guarantee.** The
declaration instrument is an annual document: the Konzern Versicherungskammer publishes its
*"Überschussverteilung 2026"* as a standalone PDF [S15] and every German life insurer publishes an
equivalent. **No rate from any such document was established** (gap 4).

The *Zinsüberschuss* arises **when investment income exceeds the *Rechnungszins***: "when
investment income exceeds the calculation rate, the insurance company generates surpluses in the
form of interest gains" [R24]. That is the direct statement that the *Rechnungszins* is the
**hurdle rate** of the surplus mechanism, and it is the fact behind the commonest arithmetic error
in describing a German contract. The declared ***laufende Verzinsung*** is the *Garantieverzinsung*
**plus** the *laufende Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee**
[REG-R53]. On the 1,00 % vintage a declared 2,55 % means a surplus credit of 1,55 %; on the 2,75 %
vintage of 2004 the same declaration means a surplus credit of **nothing at all**, and the contract
simply receives its guarantee. Adding the declared rate to the guaranteed one overstates a modern
contract by more than half and a legacy contract by all of it.

**Three accumulation-phase surplus systems are established**, two in-scope designs and one
successor design. ***Verzinsliche Ansammlung*** is the classic default and the representative
system: declared surpluses are credited to a separate ***Ansammlungsguthaben*** and accrue with
interest, "with the interest credited at the end of each insurance year and upon termination of the
insurance" [R24] — a **second, parallel account** to the *Deckungskapital*, with its own credited
rate, settling at year end and at exit. ***Bonusrente*** buys **additional premium-free annuity**
with the declared surplus [R24]; it is established and **not implemented**, because it is a second
full mechanic on the same declaration and carrying both would double the accumulation-phase state
for a choice no source quantifies — the *volldynamische Rente* of the payout phase is the same idea
where the corpus supports it with more detail. **Investment of surplus in an internal fund** is the
Debeka successor design: "surplus shares of the accumulation phase are invested in an internal fund
and can enable additional benefits", and "fund holdings generally receive no *Überschussbeteiligung*
from the earnings of Debeka's general *Sicherungsvermögen* before *Rentenbeginn*" [S12] —
guarantees on the general account, declared surplus on a fund, and therefore a variation rather than
the representative design. ***Beitragsverrechnung*** — surplus set against the premium due — is the
fourth system the German market uses, and **no source in this corpus named it for this product**
(gap 16); its absence is a gap in the corpus, not evidence that it does not exist.

The **four-component decomposition** — *Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss*,
*Schlussüberschussanteil* — is only one quarter established in this product's research (gap 17):
the *Zinsüberschuss* directly [R24], the other three not named by any summary. They are the primary
subject of the delib `kapitallebensversicherung` file, and the arithmetic floor under all of them is
the MindZV's **90 % of the investment result net of the *Rechnungszinsen*, 90 % of the risk result
and 50 % of the remaining result**, with the *Direktgutschrift* deducted and *Alt-* and *Neubestand*
treated separately [REG-R18]. The implementation models the credited outcome, not the source
decomposition, and says so.

### *Bewertungsreserven*

Under **§ 153 Abs. 3 VVG** policyholders participate in the *Bewertungsreserven* — unrealised gains
in the insurer's assets — and an insurer's own consumer information restates the rule as providing
for **equal (*hälftige*) participation** [S4] [R4] [REG-R24]. Two product-specific consequences
follow from the same source: the **transition to annuity payment is a key point** for that
participation [S4], so the share crystallises at the boundary; and **participation continues during
the payout phase** [S4] [R4]. The LVRG 2014 restricted the distribution to reserves from
*festverzinsliche Wertpapiere* and subjected departing policyholders' share to the
*Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG and §§ 11–12 MindZV [REG-R20] [REG-R18]. The
implementation carries the crystallisation at *Rentenbeginn* as a [std] rate on the accumulated
value and does **not** implement the *Sicherungsbedarf* test, whose inputs are balance-sheet
quantities a single-policy liability projection does not have.

### The *Todesfallleistung* before *Rentenbeginn*

On death during the *Aufschubzeit* the contract pays a death benefit and ends. **Three designs are
established, all in use** [R24]: ***Beitragsrückgewähr*** — "the insurer refunds all paid premiums
after the death" — with an optional extension, "repayment of the premiums plus the
*Überschussbeteiligung* attributable to them can be agreed", so it comes in a bare form and a
with-surplus form and the choice is contractual; **payment of the accumulated *Deckungskapital***;
and a ***Hinterbliebenenrente***, which has its own GDV model condition set [S10] and is properly a
rider. **The term *Beitragsrückgewähr* is named in the GDV model conditions for this product** [S1]
— the model wording's own word, not a marketing label.

The `max(...)` form is established for the **unit-linked sibling and not for the classic product**:
DEVK's wording gives the fund value at the date of death "but at least the sum of the premiums paid
(*Beitragsrückgewähr*)" [S19]. Its classic analogue is the obvious counterpart, no classic document
in this corpus states it, and any design adopting it must tag it [std].

**What the death benefit is not:** there is no separate sum insured anywhere in this product. It is
defined off the premiums paid or off the accumulated fund, never off an independently chosen
*Versicherungssumme* [S19] [R24]. That is the structural difference from delib's
`kapitallebensversicherung` and `risikolebensversicherung`, and it is why this product carries no
underwriting and no rating factor. **Whether the benefit falls at the date of death or at the next
policy anniversary, and whether the with-surplus form includes the *Ansammlungsguthaben* in full,
were not established** (gap 18); the implementation pays at the end of the policy year of death and
offers the surplus inclusion as a model-point switch.

### The *Rentenfaktor*

This is the mechanic the whole product turns on and the best-evidenced thing in the corpus. The
factor determines how much monthly annuity is received per 10 000 € of accumulated capital [R24];
the illustration the corpus supplies is capital of 100 000 € at a factor of 25 yielding 250 € a
month, computed as `100 000 / 10 000 × 25` [R24], where the 25 is a **teaching example, not a
market level** (gap 3):

    monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor

**Guaranteed at inception.** The *garantierter Rentenfaktor* is fixed in the contract documents and
rests on the *Rechnungsgrundlagen* as at the date of conclusion [R24] — a guarantee given at issue
about a conversion decades later. The insurer applies a ***Sicherheitsabschlag***, which is why it
comes out lower than the current factor [R24], and **the margin is quantifiable from one carrier**:
CosmosDirekt's factor is computed "on the basis of a recognised mortality table (currently DAV 2004
R) and an underlying interest rate (currently 0 percent p.a.)" [S8]. A zero-percent interest basis,
against a *Höchstrechnungszins* positive throughout, is the *Sicherheitsabschlag* made concrete: the
guaranteed factor is priced as though the insurer will earn nothing on the annuity fund. Allianz
expresses the same guarantee as "a minimum annuity" available at inception [S13] — the same object
stated as an amount rather than a factor.

**Current, and the comparison.** The *aktueller Rentenfaktor* is influenced by economic factors such
as the interest level and the life expectancy of the insured person [R24] and is recomputed on the
bases in force when quoted. Allianz states what "current" means operationally: the bases at
*Rentenbeginn* "relate to the interest rate and mortality table that the company uses **at that time
for immediately beginning annuities**" [S13] — which is why an immediate-annuity document [S16]
belongs in this product's source list. **The rule at *Rentenbeginn* is a maximum of two factors.**
Zurich: at the start of annuity payments a second *Rentenfaktor* is compared with the guaranteed
one, **the higher of the two being guaranteed for the annuity payment period** [S4]; the consumer
literature states the same rule from the other side [R24].

    Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )

This is a **guarantee with upside**, and it is the mechanic an implementation is most likely to get
wrong in the direction that understates the liability. The factor moves with the *Rechnungszins* and
with the mortality basis, because those are the two things it is computed from [S8] [S13] [R24], so
the rate history maps onto it: the thirty-year decline to 0,25 % compressed guaranteed factors and
the 2025 increase should have relieved that compression for new business [R7] [R8] [REG-R15].
**The magnitude was not established** — no search returned a level, a range or a time series, not
even from the rating house whose article asks "wie hoch ist er?" [R19].

### Reduction of a guaranteed factor: the *Treuhänderklausel* and § 163 VVG

Historically, insurers could change guaranteed *Rentenfaktoren* on the basis of a
***Treuhänderklausel*** in the conditions, with the approval of an independent external
*Treuhänder*, where economic conditions deteriorated permanently and unexpectedly, on two explicit
triggers: an **unexpectedly strong increase in life expectancy** and a **sustainable reduction in
capital-market returns** [R17] [R3]. **Currently the clause is used only in older contracts, and the
guaranteed factor can be changed only on the basis of § 163 VVG** [R17] [R3], which permits
adjustment on **three cumulative conditions**: the *Leistungsbedarf* has changed in a way that is
not merely temporary and was not foreseeable; the newly set premium on the corrected bases is
appropriate and necessary to secure permanent fulfilment; and an *unabhängiger Treuhänder* has
reviewed and confirmed the bases and those conditions [REG-R27]. Two limits matter: the adjustment
is **excluded** to the extent the benefits were insufficiently calculated at the original
calculation and a diligent actuary should have recognised it — **the insurer may not reprice its way
out of its own mispricing** — and the article permits a **reduction of the benefit** as an
alternative to raising the premium [REG-R27].

**The courts have narrowed it.** The Landgericht Köln held that the low-interest phase is **not** a
sufficient ground, because it must be assessed as entrepreneurial risk that cannot be passed on to
policyholders [R17]; consumer press reports that a subsequent reduction **can be unlawful** [R16].
**The case reference, decision date and party names were not established** (gap 10) and no citation
beyond "a Landgericht Köln decision reported by [R17]" may be made. It was a live commercial dispute
at the market leader: trade press of 4 February 2021 reports Allianz's position that customers could
not successfully object [R18]. The BGH has separately struck down asymmetric unilateral
*Rentenfaktor* reduction clauses in 2025 [REG-R36]. **The implementation treats the guaranteed
factor as fixed for the life of the contract and records § 163 VVG as a model risk.**

### The *Rentenphase*

The annuity in payment is **the sum of a *garantierte Rente* and an *Überschussrente***: the insurer
sets a value at the start of the payout phase "composed of the *Garantierente* and a surplus share
projected for the whole annuity period" [R20]. **Only the guaranteed part is a promise.** Three
*Überschussverwendung* systems exist and the choice is the policyholder's [R19] [R20] [R24]:

| System | Mechanic |
|---|---|
| ***konstante Rente*** | The payout stays the same over the whole term; the insurer fixes a value at the start of the payout phase from the *Garantierente* plus a surplus share **projected for the whole annuity period**. In practice it can still fluctuate: **if the provider earns less than expected, the annuity falls** [R20]. |
| ***teildynamische Rente*** | The annuity rises regularly by a **fixed percentage** provided the insurer earns corresponding surpluses — a combination in which part of the expected surplus is used under the constant system and part under the dynamic system [R20] [R24]. |
| ***volldynamische (steigende) Rente*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R20]. It starts lowest and rises fastest. |

The ***Bonusrente*** is the mechanism underneath the rising forms: "the ongoing surplus shares are
used partly for an age-dependent *Überschussrente* and partly for an additional premium-free annuity
(*Bonusrente*)" [R24]. The increment, once bought, is **premium-free and permanent** — which is what
makes a *volldynamische Rente* ratchet rather than fluctuate. **The constant form is not actually
constant**, which is worth its own sentence because it is exactly what a model gets wrong by taking
a product name literally: under it the annuity is set from a **projection**, and if the insurer
earns less than projected the annuity is reduced [R20].

### The *Rentengarantiezeit*

A guaranteed payment period beginning at *Rentenbeginn*: if the annuitant dies inside it, **the
annuity continues to be paid to the survivors until the agreed years have expired** [R17] [R24].
The corpus's own illustration is a 10-year period with death after 6 years, the spouse receiving the
remaining 4. Durations offered are 5, 10, 15, 20, 25 or more than 30 years; typical durations are 15
years for retirement ages 61–70 and 10 for 71 and above; most policyholders choose 10 to 20 [R24].
It is selectable with a floor at Allianz [S13] and a tariff-level feature carried in the product name
at NÜRNBERGER, whose AVB title reads "…mit aufgeschobener Rentenzahlung **und Rentengarantiezeit**
nach Tarif NIR3301" [S9]. **It costs annuity**: against 573 € a month with no guarantee period, a
10-year period costs 3 €, a 20-year 15 € and a 30-year 46 € a month [R24].

**The modelling consequence is a decrement-weighting one and it is the pitfall this product hides
best.** Inside the guarantee period the payment obligation does not depend on survival: the
instalment is due to the annuitant or to the survivors either way, so it must be weighted by the
**count that annuitised**, not by the count still alive. Outside the period it is weighted by
survivors. The two counts differ by exactly the deaths inside the window, and a model that weights
everything by survivors understates the annuity outgo by that amount while never producing a number
that looks wrong.

### The *Kapitalwahlrecht*

The right to take **the accumulated capital as a lump sum instead of the lifelong annuity** at
*Rentenbeginn* [S12] [R6] [R21], and the third of the three things that happen at that boundary.
**The notice period was not established at any carrier** (gap 11).

**The tax consequence of electing it is total, and it is the established part.** The lump sum moves
the contract from the *Ertragsanteil* regime of § 22 EStG [R5] [REG-R41] to § 20 Abs. 1 Nr. 6 EStG
[R6] [REG-R45]. Annuity contracts with a *Kapitalwahlrecht* against ongoing premiums fall under
§ 20 EStG if the capital option cannot be exercised before 12 years from conclusion; where the
**"12/62 rule"** is met — at least 12 years of duration and payment after completion of the 62nd
year of life — **only half the gain is taxable**, and the *Halbeinkünfteverfahren* applies **only to
lump sums and to payout-plan withdrawals, not to monthly annuity payments** [R6]. The base is the
*Unterschiedsbetrag* between the *Versicherungsleistung* and the premiums paid, and the half amount
goes to the **personal marginal rate** under § 32d Abs. 2 Nr. 2 EStG rather than the flat
*Abgeltungsteuer* [REG-R45]. Contracts concluded before 1 January 2005 retain the half-income
treatment of the lump sum while annuity payments continue on the *Ertragsanteil* basis [R6], so a
German in-force book carries **two tax cohorts** divided by the *Alterseinkünftegesetz* watershed
[REG-R38]. On the annuity side, Debeka states that only part of the payout is taxed — the
comparatively low *Ertragsanteil*, depending on age at *Rentenbeginn* [S12] — and **at age 65 the
*Ertragsanteil* is 18 %** [R5], the only value of the statutory table any search established, every
other age being [unverified] (gap 8). Unlike the Schicht-1 *Rentenfreibetrag*, which is frozen in
euro so that every later increase is fully taxable, **the *Ertragsanteil* percentage is what is
frozen**, so surplus increases to a Schicht-3 annuity are taxed at the same light rate [REG-R41].

**The two regimes are why the election is economically live** rather than a formality: the annuitant
compares 18 % of each instalment at the marginal rate against half of the total gain taxed once.
**delib computes no tax anywhere** [REG-R38], so the implementation carries the election as a
**take-up rate** and says explicitly that the rate stands in for a tax comparison the model does not
perform.

### The *Rückkaufswert* under § 169 VVG

The surrender right exists and its value is governed by § 169 VVG [R1] [REG-R28]. The base measure
is the ***Deckungskapital*** computed by recognised actuarial rules **on the calculation bases of
the premium calculation** [REG-R28]. For unit-linked contracts, where the insurer does not guarantee
a particular benefit, the value is instead the *Zeitwert* and the principles of the calculation must
be stated in the contract [R1]; for the classic contract the guaranteed benefit exists, so the
*Zeitwert* clause is the boundary rather than the rule, and **what the classic surrender value is
computed as was not established at article level in this product's own research** (gap 12).

**The floor is the operative constraint, and it is not the *Stornoabzug*.** § 169 Abs. 3 requires at
least the *Deckungskapital* that results from **spreading the charged acquisition and distribution
costs evenly over the first five contract years**, with the supervisory *Zillmer* rules unaffected
[REG-R28]. That is a floor on the **value**, not a cap on the **charge**: the DeckRV governs what the
insurer may reserve and § 169 VVG what it must pay, so a model carrying a zillmered reserve applies
both separately, the tighter binding [REG-R16] [REG-R28]. In the first five contract years of a
zillmered tariff the floor binds by a wide margin, and it is the whole reason a German surrender
value in year two is not simply zero.

**The *Stornoabzug*** may then be deducted, and only if **agreed, quantified (*beziffert*) and
appropriate (*angemessen*)** — three cumulative conditions, the burden of proof on the insurer —
while **an agreement of a deduction in respect of not-yet-amortised *Abschluss- und
Vertriebskosten* is void** [R1] [REG-R28]. That is the statutory answer to *Zillmerung*: the
front-loading may not be recovered from the surrendering policyholder as a named deduction. § 169
Abs. 6 separately permits reductions of surrender values to be paid out [R1] — a solvency valve, not
an ordinary charge, and not modeled. **No *Stornoabzug* percentage, surrender-value table or
charge-recovery schedule was established at any carrier** (gap 12).

### *Beitragsfreistellung* under § 165 VVG

The policyholder may **at any time, for the end of the current insurance period, demand that the
insurance be converted into a premium-free insurance, provided the agreed minimum insurance benefit
is reached** [R2] [REG-R28]. The right is statutory and unconditional apart from that threshold.
**If the minimum benefit is not reached, the insurer must instead pay the surrender value
attributable to the insurance, including profit shares, under § 169** [R2] — a small contract cannot
be made paid-up; it is cashed out. **The premium-free benefit is calculated according to recognised
principles of actuarial mathematics, using the calculation basis of the premium calculation, on the
basis of the surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for
each insurance year** [R2]. Three consequences reach the model: the paid-up value is **derived from
the surrender value**, so a model computing them independently will not reconcile; it uses the
**premium basis**, so the paid-up contract keeps its guarantee vintage; and it is **tabulated per
insurance year**, which is why a German policy schedule carries two value columns.

**The difference from *Kündigung* is the point.** *Beitragsfreistellung* keeps the contract alive —
its guarantee vintage, its *Rechnungszins* and its guaranteed *Rentenfaktor* all survive on a reduced
benefit — while *Kündigung* ends it for the *Rückkaufswert* [R1] [R2]. Where an old contract carries
a high legacy *Rechnungszins* and an old guaranteed factor, that difference is worth a great deal,
and it is why paid-up conversion and lapse **must be separate decrements**. German lapse is in fact
three-way, because § 166 VVG converts automatically to *prämienfrei* on the insurer's termination and
in the § 38 premium-default case rather than ending cover [REG-R28] [REG-R30]. **The
*Mindestversicherungsleistung* threshold was not established at any carrier** (gap 22).

---

## Riders and options

**In scope and modeled.** The ***Rentengarantiezeit*** as a selectable term in years, base value 10
[R24] [S9] [S13]; the ***Kapitalwahlrecht*** as a take-up rate at *Rentenbeginn* [S12] [R6] [R21];
the death-benefit **form** switch across the three documented designs [S1] [R24] and the
with-surplus variant [R24]; the ***Dynamik*** as an annual premium-and-benefit increase rate, base 0
and switched on for one model point [S4]; ***Beitragsfreistellung*** as a deterministic election at
a stated policy year, with the *Mindestversicherungsleistung* cash-out branch [R2]; and the three
payout-phase *Überschussverwendung* systems [R19] [R20] [R24].

**Documented and deliberately not modeled**, each with its reason. The
***Hinterbliebenenrenten-Zusatzversicherung***, which the GDV publishes as a **separate model
condition set attaching to this contract** [S10] — it needs a second life and no model point carries
one. The ***Berufsunfähigkeits-Zusatzversicherung***, a named section with its own special
conditions inside the same pack [S4] and delib's `berufsunfaehigkeit` product in standalone form.
***Zuzahlung***: **no source in this corpus named it** (gap 15), so there is nothing to
parameterize — the one option the research brief asked for that the corpus does not support at all.
***Bonusrente*** as the accumulation-phase surplus system [R24], left to the *volldynamische Rente*
where the same idea is better evidenced. ***Beitragsverrechnung***, not established for this product
(gap 16). Surplus **invested in an internal fund** [S12], a departure from the classic chassis. The
§ 163 VVG / *Treuhänderklausel* **adjustment of the guaranteed *Rentenfaktor*** [R3] [R17]
[REG-R27], recorded as a model risk. And § 169 Abs. 6 **reduction of surrender values** [R1], a
supervised solvency measure with no published trigger a deterministic model could key off.

---

## Variations across insurers

The corpus supports **structural** variation tables. It does **not** support quantitative range
tables for the parameters that matter most — *Rentenfaktor* levels, charges, entry ages, premium
envelopes and surplus rates — because **no search in this session returned a number for any of them
at any carrier**. Where a row reads "not established", that is the finding.

| Carrier | Documents | Status of the classic deferred annuity |
|---|---|---|
| GDV (industry model wording) | [S1] [S2] [S3] [S10] | Model conditions maintained; a 2021 edition seen; **expressly non-binding** — "Diese Bedingungen sind unverbindlich" [S2], use optional [S3] |
| Zurich Deutscher Herold | [S4] [S5] [S6] [S7] [S16] [S17] | *Verbraucherinformation* published 2021, 2022 and **Fassung 01/2026** [S4]; but reported among the carriers that stopped [R22] — **unresolved**, gap 9 |
| CosmosDirekt (Cosmos Leben, Generali) | [S8] | AVB **LA 904 A** published; vintage not established (gap 5); Generali reported among those that stopped [R22] |
| NÜRNBERGER | [S9] | AVB for tariff **NIR3301**, *mit Rentengarantiezeit* in the title |
| Debeka | [S11] [S12] | **Withdrawn.** Replaced from 1 July 2016 by five "Chance" variants [R22] [S12] |
| Allianz | [S13] | **Withdrawn.** Replaced by KomfortDynamik, a 60/80/90 % premium-guarantee hybrid [S13] [R22] [R23] |
| Mecklenburgische | [S14] | *Vertragsinformationen* for "Rente flex"; the distinguishing feature is not established |
| Konzern Versicherungskammer | [S15] | Annual *Überschussverteilung 2026* published; **no rate established** |
| Stuttgarter | [S18] | *Allgemeine Informationen* pack dated 2020 |
| DEVK | [S19] | Unit-linked only; used here for the death-benefit contrast |

### Death benefit and *Rentenfaktor* determination

| Item | Observation | Source |
|---|---|---|
| *Beitragsrückgewähr*, premiums only | Named in the GDV model wording | [S1] [R24] |
| *Beitragsrückgewähr* plus attributable surplus | "can be agreed" — a contractual election | [R24] |
| Accumulated *Deckungskapital* | The alternative classic design | [R24] |
| *Hinterbliebenenrente* | Own GDV model condition set — a rider | [S10] [R24] |
| `max(fund value, premiums paid)` | **Unit-linked wording**; the classic analogue is [unverified] | [S19] |
| Guaranteed *Rentenfaktor* fixed at inception | Yes | [S8] [R24] |
| Its mortality basis | **DAV 2004 R** | [S8] |
| Its interest basis | **0 % p.a.** at one carrier, at an unestablished vintage | [S8] |
| A *Sicherheitsabschlag* makes it lower than the current factor | Yes | [R24] |
| Current factor = the carrier's then-current immediate-annuity tariff | Yes | [S13] |
| The rule at *Rentenbeginn* | **The higher of the two** | [S4] [R24] |
| Typical level in € per 10 000 €, and its movement since 2025 | **Not established** | gap 3 |

### *Rentengarantiezeit* and the surplus systems

| Item | Observation | Source |
|---|---|---|
| Durations offered | 5, 10, 15, 20, 25, 30+ years | [R24] |
| Typical, retirement age 61–70 / 71+ | 15 years / 10 years | [R24] |
| Most commonly chosen | 10–20 years | [R24] |
| Cost (200 €/month over 30 years, 573 €/month base) | 10 y: −3 €; 20 y: −15 €; 30 y: −46 € a month | [R24] |
| Carried in the tariff name | NÜRNBERGER NIR3301 | [S9] |
| Selectable with a floor | Allianz PrivatRente KomfortDynamik | [S13] |
| Accumulation: *verzinsliche Ansammlung* | Established — interest at each year end and at exit | [R24] |
| Accumulation: *Bonusrente* / *Bonussystem* | Established | [R24] |
| Accumulation: surplus invested in an internal fund | Established — Debeka's successor design | [S12] |
| Accumulation: *Beitragsverrechnung* | **Not established** | gap 16 |
| Declared rates for any year | **Not established** for this product; market averages only | gap 4; [REG-R53] |
| Payout: *konstante Rente* | Set from a whole-period projection; **falls if the insurer earns less** | [R20] |
| Payout: *teildynamische Rente* | Rises by a fixed percentage if surpluses permit | [R20] [R24] |
| Payout: *volldynamische Rente* | Adjusts annually to actual surplus development | [R20] |
| Payout: *Bewertungsreserven* participation continues | Yes | [S4] [R4] |

### The guarantee level at *Rentenbeginn* — classic against successor designs

| Design | Guarantee at *Rentenbeginn* | Source |
|---|---|---|
| Classic (this product) | *Sparbeiträge* accumulated at the *Rechnungszins*, ≥ 100 % of the savings portions by construction | [S11] |
| Debeka "Chance", safest variant (from 1 July 2016) | **0,5 %** guaranteed interest | [R22] |
| Debeka "Chance", riskiest variant | None — effectively a fund policy | [R22] |
| Allianz KomfortDynamik | **60 %, 80 % or 90 % of the premiums paid**, selectable, 80 % standard | [S13] [R23] |

### What does not vary

Three things are the same everywhere in the corpus and all three are legal facts rather than
commercial ones. The **two-phase structure with a fixed *Rentenbeginn*** is definitional [S1] [S4]
[S8] [S9] [R24]. The ***Rückkaufswert*** and ***Beitragsfreistellung*** rights are statutory and
*halbzwingend* — §§ 165 to 170 VVG may not be varied to the policyholder's detriment under § 171 VVG
[REG-R22] [REG-R28] — so a carrier may improve on them and may not remove them. And the **unisex
tariff** has been compulsory for contracts concluded from 21 December 2012 [REG-R34], which is why
sex appears nowhere in the pricing of this composite even though the underlying annuity tables are
sex-specific raw material [REG-R47] [REG-R49].

Two limbs of the composite's core rest on a single carrier each and are flagged accordingly. The
***Rentenfaktor* comparison rule** is stated in terms by **one** carrier's consumer information [S4]
and restated from the other side by secondary material [R24]; no second primary document states it.
And the **conversion basis** — DAV 2004 R at a 0 % interest basis — is stated by **one** carrier's
AVB [S8], at a vintage that document itself marks as time-dependent ("currently") and that the
corpus could not date (gap 5).

---

## Regulatory context

**Contract law — the VVG.** German life contract law sits in a separate statute from the prudential
one, with a different addressee, and its **Kapitel 5 (§§ 150–171) is *halbzwingend***: §§ 152 Abs. 1
and 2, 153 to 155, 157, 158, 161 and 163 to 170 may not be varied to the policyholder's detriment
under § 171 VVG [REG-R22]. That is why a model may treat the surrender-value floor, the paid-up
right and the profit-participation entitlement as **contractual facts** rather than tariff options.
The operative articles here are **§ 153** (*Überschussbeteiligung*, and *Bewertungsreserven* under
Abs. 3) [R4] [REG-R24]; **§§ 154 and 155** (the *Modellrechnung* at three statutory interest rates,
and the annual *Standmitteilung* disclosing how much of the profit participation is guaranteed)
[REG-R25]; **§ 163** (*Prämien- und Leistungsänderung*, the only current channel for adjusting a
guaranteed *Rentenfaktor*) [R3] [R17] [REG-R27]; **§ 165** (*prämienfreie Versicherung*) [R2]
[REG-R28]; **§ 166** (automatic conversion to *prämienfrei*) [REG-R28]; **§ 168** (*Kündigung*, and
the Abs. 3 carve-out that defines the Schicht-1 products) [REG-R28]; **§ 169** (*Rückkaufswert*, the
five-year-spread floor and the *Stornoabzug*) [R1] [REG-R28]; **§§ 8 and 152** (*Widerruf*)
[REG-R23]; and **§§ 150, 157, 158 and 161** on consent, age misstatement, risk increase and suicide
[REG-R26] [REG-R30].

The **§ 154 *Modellrechnung*** fixes what a published German illustration looks like: quantified
statements about benefits beyond the guaranteed ones must be accompanied by the possible
*Ablaufleistung* computed on the premium calculation bases at three rates set by § 2 Abs. 3
VVG-InfoV — the *Höchstrechnungszins* times 1,67, that rate plus one point, and that rate minus one
[REG-R25], so at a *Höchstrechnungszins* of 1,00 % the statutory triple is
**1,67 % / 2,67 % / 0,67 %**. The reference implementation does **not** use those rates — its
declared-rate path is a [std] scenario anchored on observed market averages — and says so.

**Prudential — the VAG, the DeckRV and the MindZV.** BaFin supervises German life insurers under
Solvabilität II as transposed into the VAG, with no second national supervisor [REG-R21] [REG-R5]
[REG-R6]. Two ministerial regulations carry the arithmetic. The **DeckRV** fixes the
*Höchstrechnungszins* in § 2 [REG-R14] [REG-R15], the *Höchstzillmersätze* in § 4 — **25 ‰ of the
*Beitragssumme*** since 1 January 2015, 40 ‰ before, the rate at conclusion applying for the whole
term [REG-R16] — and the *Referenzzins* behind the ***Zinszusatzreserve*** in § 5 Abs. 3 [REG-R17].
The **MindZV** puts the arithmetic floor under the *Überschussbeteiligung*: **90 %** of the
investment result **less the *Rechnungszinsen***, **90 %** of the risk result and **50 %** of the
remaining result, with the *Direktgutschrift* deducted, *Alt-* and *Neubestand* separate, and a
negative minimum replaced by zero — a minimum **transfer to the RfB**, not a minimum payout
[REG-R18] [REG-R10] [REG-R19]. The **LVRG 2014** produced the current shape: it restricted
*Bewertungsreserven* distribution to reserves from fixed-income securities and subjected it to the
*Sicherungsbedarf* test, cut the *Höchstzillmersatz* to 25 ‰ from 1 January 2015, and raised the
*Risikoüberschuss* share from 75 % to 90 % from 7 August 2014 [REG-R20]. The ***Zinszusatzreserve***
exists in no other jurisdiction in this repository and is why a book of high-vintage annuity
contracts is expensive: it arises where the § 5 Abs. 3 *Referenzzins* falls below a contract's tariff
rate, and the MindZV *Sicherungsbedarf* test compares a Bundesbank month-end swap rate with **the
highest *Rechnungszins* applicable to the contract over the next fifteen years** — a window that
"bites hardest on annuity business" [REG-R17] [REG-R18]. **delib does not compute it**; this document
cites it rather than specifying it.

**Biometric bases.** The mortality basis for every German annuity promise is **DAV 2004 R**, named
in an insurer's own AVB for exactly this product [S8]. It is a ***Generationentafel*** — a
two-dimensional basis in attained age and calendar year containing mortality by birth cohort
including the expected future change [R13] [R15] [REG-R49] — built from a second-order base table, a
first-order base table, second- and first-order mortality trends and an age adjustment
(*Altersverschiebung*) [R12]. **First-order probabilities carry safety margins relative to the
second-order ("realistic") probabilities in order to assess the risk prudently**, the second-order
base tables being the best estimate of period mortality in 1999 for insured lives [R12]. It has been
in use since June 2004, was intended for new business from 2005, and the DAV **reissued its
derivation guideline on 28 June 2023** [R12] [R13] — nineteen years after first use, which is itself
the evidence that no successor has displaced it and the fact behind the longevity trigger of the
§ 163 VVG adjustment right. A companion in-force table, **DAV 2004 R-Bestand**, exists for annuities
already in payment [R14] [REG-R49].

**The table is the property of the Deutsche Aktuarvereinigung, is not public and is not redistributed
by delib.** The library cites it by name and ships a [std] proxy anchored so its own worked example
reproduces exactly. A replacement must preserve three things: the **generational structure** — a
`q(x, τ)` surface, not a period table, because a period-table proxy priced at a 40-year-old's
annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the
model [REG-R49]; the **first-order margin over second order**, which for an annuity runs in **two
dimensions**, level and trend, so a proxy reproducing only the level is not a proxy for the table
[REG-R47] [REG-R49]; and the **age-adjustment convention** [R12]. The free, redistributable public
analogue is Destatis's *Generationensterbetafeln für Deutschland* [REG-R52]. The tables are
sex-distinct while the tariff sold since *Test-Achats* must be unisex — the ECJ held on 1 March 2011
in C-236/09 that sex may not be a risk factor and invalidated the Article 5(2) derogation **with
effect from 21 December 2012**, and § 20 Abs. 2 Satz 1 AGG was repealed [REG-R34]. **Neither half of
that sentence was established by any search in this product's own research** (gap 21). The model
consequence is hard: a model point may carry `sex` for **decrement** purposes and **must not** let it
enter the premium or the *Rentenfaktor*.

**Taxation.** The annuity is taxed on the ***Ertragsanteil*** under § 22 EStG — only the "Ertrag des
Rentenrechts" is taxed, and the fraction is fixed by the annuitant's age at *Rentenbeginn*, at
**18 % for age 65** [R5] [R24] [REG-R41]. Electing the *Kapitalabfindung* moves the contract to § 20
Abs. 1 Nr. 6 EStG, the *Unterschiedsbetrag* base and the *Halbeinkünfteverfahren* under the 12/62
rule, with the half amount at the personal marginal rate under § 32d Abs. 2 Nr. 2 [R6] [REG-R45].
Contracts concluded before 1 January 2005 keep the half-income treatment of the lump sum [R6]
[REG-R38]. **Not established, and not asserted anywhere in this library**: the rate on the taxable
half in the general case, the *Solidaritätszuschlag*, the inheritance-tax treatment of the death
benefit, and the *Kleinbetragsrente* commutation threshold for this product (gap 23). **delib
computes no tax**: every benefit cash flow it publishes is gross of *Kapitalertragsteuer*,
*Solidaritätszuschlag* and *Kirchensteuer* [REG-R38].

**Conduct, disclosure and accounting.** The pre-contractual pack is issued under several names —
*Verbraucherinformation* [S4]–[S7], *Vertragsinformationen* [S14], *Kundeninformation* [S19],
*Allgemeine Informationen* [S18] — and is one object: general information, the AVB, the special
conditions for options and riders, and the tax notes [S4]. Its statutory basis is §§ 6, 7 and 7a–7c
VVG with the VVG-InfoV [REG-R31]; distribution sits under the IDD as transposed and § 34d GewO
[REG-R33]; BaFin's *Merkblatt 01/2023* on *Wohlverhaltensaufsicht* governs product governance and
value for money for this class of contract [REG-R35]. The statutory balance sheet is the HGB one of
§§ 341–341o HGB with the RechVersV and BerVersV [REG-R54], and its *Deckungsrückstellung* is **not**
the Solvency II best estimate — an insurer carries two liability measures, and the
*Überschussbeteiligung*, the *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the
**HGB** side [REG-R14] [REG-R54]. IFRS 17 would measure this contract under the variable fee approach
[REG-R55]. Actuarial work sits under the DAV *Fachgrundsätze* and the § 141 VAG *Verantwortlicher
Aktuar*, a role the MaGo keeps distinct from the *versicherungsmathematische Funktion* [REG-R56]
[REG-R11] [REG-R21]; policyholder protection in a failure runs through **Protektor** under
§§ 221–236 VAG [REG-R12].
