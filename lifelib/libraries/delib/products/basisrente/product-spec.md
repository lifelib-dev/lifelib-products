# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation: 2026-08-29).

**Retrieval conditions — read this first.** **No document cited anywhere in this specification was
retrieved.** Direct HTTP egress from the build environment is blocked by an organisation network
policy, and the session's `WebSearch` budget was already exhausted when this product was reached, so
this document rests on a research file [`_research/basisrente.md`] that had **no research channel of
any kind**. A delib citation is therefore a **pointer, not a certificate**: an [R1] tag on a sentence
about § 10 Abs. 1 Nr. 2 Buchst. b EStG names the instrument the claim must be checked against; it
does not assert that anyone read it. Nothing below is quoted from a German statutory or contractual
text. Every specific paragraph number, effective date, monetary amount, percentage and market figure
carries [unverified] unless a sibling delib research file corroborated it by search while search was
still available. Where the mechanic is certain and the level is not, this document ships a **[std]**
parameter with its rationale rather than a fabricated source tag.

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modelling of a German **Basisrente** (*Rürup-Rente*) — the *Basisrentenvertrag* of
§ 10 Abs. 1 Nr. 2 Buchst. b EStG, the privately written, funded member of *Schicht 1* of the German
three-layer retirement architecture. **It does not describe any single insurer's product**, and on
this product that disclaimer is stronger than usual: the corpus behind it contains **two** carrier
artefacts, neither of which is a *Bedingungswerk*, so the composite is built from the **statute and
the market's settled mechanics** rather than from a comparison of contracts. Facts carrying [S#]
(primary product documents — *Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*,
*Basisinformationsblatt*, *Verbraucherinformation*) and [R#] (product-specific regulatory and
actuarial references) are numbered per `_research/basisrente.md` and resolved in `sources.md` (same
directory; numbering frozen, never renumbered). [REG-R#] tags refer to the cross-product reference
library `references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct and
also frozen. Values marked **[std]** are standardizations introduced for the reference
implementation; each carries a rationale and, where the research recorded one, an argued plausible
range.

**Out of scope, and said so where it matters.** The *Riester-Rente* (Schicht 2, delib product 6) and
the *klassische private Rentenversicherung* (Schicht 3, delib product 2) share this product's chassis
and are referenced only as contrasts. The competing Schicht-1 vehicles of § 10 Abs. 1 Nr. 2
Buchst. **a** — *gesetzliche Rentenversicherung*, *berufsständische Versorgungswerke*,
*landwirtschaftliche Alterskasse* — are not modelled, but they **consume the same annual ceiling**
and that is treated below as a first-order fact about demand. The *Fonds-Basisrente* written by a
*Kapitalverwaltungsgesellschaft*, *betriebliche Altersversorgung* in all five *Durchführungswege*,
*Gruppenversicherung*, *private Krankenversicherung* and *Sterbegeldversicherung* are outside delib
entirely.

---

## Product overview and market role

A Basisrente is an **ordinary German life insurance contract governed by the VVG** [R14] [R15]
[REG-R22], written on a single life, which additionally satisfies the definitional conditions of
§ 10 Abs. 1 Nr. 2 Buchst. b EStG [R1] [REG-R39] and holds a certificate under § 5a AltZertG [R9]
[REG-R43]. It is not a separate legal species. Everything true of a German deferred annuity is true
of it — the same *Deckungskapital* recursion, the same *Überschussbeteiligung*, the same
*Rentenfaktor*, the same DAV 2004 R basis — unless the § 10 conditions displace it.

**The product is defined by prohibitions, not by benefits.** Its accumulation and payout mechanics
are those of the delib `klassische_rentenversicherung` product. What makes it a distinct product, and
what a projection model has to get right, is a closed list of five things it may **not** do: the
entitlement must be *nicht vererblich* (not inheritable), *nicht übertragbar* (not transferable),
*nicht beleihbar* (not chargeable as security), *nicht veräußerbar* (not saleable) and *nicht
kapitalisierbar* (not convertible into capital) [R1] [REG-R39]. Every section below follows from that
sentence.

Three consequences make the German chassis behave differently here from its Schicht-3 sibling:

1. **There is no *Rückkaufswert* at any duration.** The statutory surrender-value regime of
   § 169 VVG [R14] [REG-R28] — the *Zeitwert* rule, the *Mindestrückkaufswert*, the requirement that
   a *Stornoabzug* be agreed, appropriate and quantified — is **inoperative**. The contract has a
   *Deckungskapital* like any other and **there is no duration at which any part of it is payable to
   the policyholder as capital**. This is the single most important thing a modeller coming from the
   delib endowment or Schicht-3 chassis has to unlearn.
2. ***Beitragsfreistellung* is the only exit, and it is not a lapse.** § 165 VVG's right to convert
   to a premium-free contract with a reduced benefit survives intact [R14] [REG-R28]; § 168 VVG's
   termination right survives too but **produces no payment**, so a purported *Kündigung* is
   administered as a *Beitragsfreistellung*. The policyholder facing a cash crisis has exactly one
   lever, and the paid-up cohort is a **large permanent part of the book rather than a residue**.
3. **Death before *Rentenbeginn* pays nothing in the base design.** *Nicht vererblich* means the
   entitlement forms no part of the estate and may not be directed by will [R1] [REG-R39]; with no
   *Hinterbliebenenabsicherung* the reserve is released to the *Versichertengemeinschaft* as a
   mortality profit. Where the rider is present the permitted beneficiaries are **closed** — the
   spouse or registered partner, and children while *Kindergeld* runs — and **everything paid to a
   survivor must be paid as an annuity**.

**The layer is a tax wrapper, not a chassis.** [S2] is the direct evidence: one large insurer sells
the same design — the same premium split between the *Sicherungsvermögen* and a *Spezialfonds*, the
same selectable guarantee levels, the same *Rentenfaktor* machinery — as PrivatRente (Schicht 3),
BasisRente (Schicht 1) and RiesterRente (Schicht 2), differing only in the wrapper. A Basisrente
model should therefore reuse the Schicht-3 chassis with the constraint set bolted on.

**What the buyer is buying** is three things at once, and the model point makes no sense without all
three. The ***Sonderausgabenabzug***: from the assessment period 2023 the capped contribution is
deductible **in full** [R7] [REG-R39], inside an annual ceiling — the ***Höchstbetrag*** — pegged
since 2015 to the maximum contribution to the *knappschaftliche Rentenversicherung* [R2] [R20].
***Pfändungsschutz***: a compliant entitlement is attachable only on the scale that applies to
earnings, and the fund is protected up to an age-graduated annual allowance subject to an **aggregate
ceiling of 340 000 €** [R12] [REG-R40] [unverified]. And ***nachgelagerte Besteuerung*** on the way
out: the annuity is *sonstige Einkünfte* taxed on a ***Besteuerungsanteil*** fixed by the calendar
year of *Rentenbeginn* and constant for life [R4] [REG-R41]. **The protection is a by-product of the
prohibitions, not an added feature** — there is nothing to attach because there is nothing to
realise, and the clause that makes the contract illiquid for the owner makes it invisible to the
owner's creditors.

**Two buyer populations, and the model point table represents both.** The **self-employed person with
no compulsory scheme** — the buyer the product was designed for: the entire *Höchstbetrag* is free,
the *Pfändungsschutz* matters as much as the relief, the income is volatile, which is what the
*Zuzahlung* structure is for. And the **high-earning employee or partner using residual headroom** as
a late-career deferral vehicle, frequently by *Einmalbeitrag* in a high-income year, entering at 50
or later with a short deferment. In both cases the entry age is **materially higher than for a
Riester or Schicht-3 contract** — the mid-forties rather than the early thirties [unverified] —
because the product only makes sense once income is high enough for the relief to be worth the
illiquidity. **The product's fundamental commercial problem** follows and should be stated rather
than engineered away: the relief is real and large, but **the contract is irreversible**. That is not
a defect; it is the consideration for the *Pfändungsschutz* and the relief.

**Market size — the weakest material in this document.** No statistic from the GDV, the BMF or any
consumer or comparison source was established [R22] [S16] (gap 3). The orders of magnitude, every one
[unverified] general knowledge: **of the order of two and a half million** contracts in force against
**fifteen to sixteen million** Riester contracts and falling; **of the order of a hundred thousand**
new contracts a year on a declining count trend; an **average contribution of two to four thousand
euro a year** against roughly eight hundred for a Riester contract. Its share of new life business by
**premium** is much higher than its share by count, because the ceiling is fifteen to thirty times
larger and the buyer is a higher earner. **Nothing downstream may cite a delib figure for the size of
the Basisrente market.** For context, the *Altersvorsorgereformgesetz* — Bundesrat consent **8 May
2026**, new subsidised model from **1 January 2027** [REG-R44] — closes *Riester* to new business and
leaves the Basisrente untouched, which if anything raises its relative weight in the certified
market.

---

## Representative specification

The representative design is a **single-life, individual, *klassisch* (general-account)
Basisrentenvertrag on an annual grid**, certified under § 5a AltZertG, with a level *laufender
Beitrag* plus an annual *Zuzahlung*, priced and reserved at the current *Höchstrechnungszins* on a
DAV 2004 R first-order basis, *gezillmert* toward the 25 ‰ cap, converting at *Rentenbeginn* into a
monthly lifelong annuity at `max(garantierter, aktueller) Rentenfaktor`, with **no *Kapitalwahlrecht*,
no *Teilkapitalauszahlung*, no *Kleinbetragsrenten-Abfindung*, no *Rückkaufswert*, no policy loan and
no assignment**.

**Why *klassisch* rather than *fondsgebunden*.** The market's centre of gravity has moved decisively
to *fondsgebundene* Basisrenten, with or without a partial guarantee, since the *Höchstrechnungszins*
fell below 1 % [R16] [REG-R15], and on a Schicht-1 contract there is nothing to stop a writer selling
a pure unit-linked policy — because § 5a AltZertG **does not import the Riester
*Beitragserhaltungsgarantie*** [R9] [R10] [REG-R43]. That judgement is [unverified] general knowledge
and unsupported by any figure in this corpus (gap 3). The composite nevertheless models the
*klassisch* form, for a stated reason: **the Schicht-1 constraints are the subject of this product
and they are clearest against a general-account chassis whose reserve recursion the library already
has**, while the unit-linked machinery is already carried by delib product 3
(`fondsgebundene_rentenversicherung`) and the hybrid guarantee mechanics by delib product 4
(`indexpolice`). Modelling the constraints twice would teach nothing; modelling them once, cleanly,
is the point of this product.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual single-life deferred annuity, general account (*klassisch*), profit-participating, certified *Basisrentenvertrag* | [R1] [R9] [R15]; form choice **[std]** (1) |
| Legal wrapper | Individual contract between policyholder and life insurer; the policyholder and the insured life are the **same person**, because the annuity must be on the taxpayer's own life | [R1] [REG-R39] |
| Certification | *Zertifizierungsnummer* issued by the **Bundeszentralamt für Steuern** under § 5a AltZertG; required for contracts concluded from **1 January 2010** | [R9] [REG-R43]; date [unverified] |
| What certification is not | A **formal conformity check**, expressly **not a quality mark**: it says nothing about charges, investment quality or the provider's strength | [R10] [REG-R43] |
| Asset form (model-point parameter, single value shipped) | (i) `klassisch` — general account, modelled; (ii) `fondsgebunden ohne Garantie`; (iii) `fondsgebunden mit Beitragsgarantie` (hybrid) | (i) modelled, **[std]** (1); (ii) [S7] [unverified]; (iii) [S2] [S8] |
| Lives basis | Single life. A second life may enter only through the permitted *Hinterbliebenenabsicherung* | [R1] |
| Entry ages | 18 to the low sixties; no statutory floor or ceiling on entry, only on *Rentenbeginn* | **[std]** (2) |
| Earliest *Rentenbeginn* | Completion of the **62nd** year of life for contracts concluded **after 31 December 2011**; completion of the **60th** for contracts concluded on or before that date | [R1] [R8] [REG-R39]; both [unverified] (3) |
| Latest *Rentenbeginn* | **No statutory ceiling.** Contracts commonly allow deferral well past the statutory retirement age | [R1]; envelope **[std]** (2) |
| Representative *Rentenbeginn* | Attained age **67**, the German statutory retirement age for the cohorts a new contract now serves | **[std]** (4) |
| Annuity form | **Monthly, lifelong, on the taxpayer's own life.** No term-certain annuity, no *Auszahlungsplan* of the Riester type, no annuity on any other single life | [R1] [REG-R39] |
| Currency | EUR | — |
| Unisex pricing | Mandatory for contracts concluded from **21 December 2012**; sex is carried for reporting only and must not enter pricing | [REG-R34] |
| Anchor model cell | Entry age 45, *Rentenbeginn* 67, conclusion year 2026, *laufender Beitrag* 6 000,00 € p.a. annual in advance with a 2 % *Beitragsdynamik*, *Zuzahlung* 4 000,00 € p.a., *Rechnungszins* 1,00 %, guaranteed *Rentenfaktor* 28,00 €, no riders | **[std]** (5) |

Footnotes to **[std]** rows:

1. **All three asset forms are sold**, and the absence of a statutory *Beitragsgarantie* is what makes
   the third one optional rather than mandatory [R9] [R10] [REG-R43] — the single sharpest structural
   contrast with Riester. The composite models the *klassisch* form for the reason given above. A
   fourth form, an **index-linked Basisrente**, is plausible from the naming of at least one carrier's
   tariff family [S10] but **was not established** (gap 12); if it exists it is a bridge to delib
   product 4.
2. **No carrier's entry-age range or permitted *Rentenbeginn* range was established** (gap 8). Twenty
   named German life writers publish this information in their *Allgemeine Versicherungsbedingungen*
   and *Produktinformationsblätter* and none was reached [S11]. The envelope stated is the market
   shape, not an observation.
3. The commissioning brief for the research file stated the pre-2012 floor as **63**; the research
   file resolved it against **60**, and this document adopts that resolution. The rule is **62 for
   contracts concluded after 31 December 2011, 60 for contracts concluded on or before that date**
   [R1] [R8]. Both figures are [unverified] in the sense that no source in this session confirmed
   them, but the 60/62 split is settled German practice and 63 corresponds to no threshold in this
   statute. **Note that the § 851c ZPO age condition is 60, not 62** [R12] [REG-R40]: two genuinely
   different provisions with different histories, and a reader must not merge them (gap 10).
4. Age 67 sits comfortably above both statutory floors, matches the *Regelaltersgrenze* the buyer's
   other provision is built around, and gives a 22-year deferment from the anchor's entry age — long
   enough for the *Zillmerung*, the *Beitragsdynamik* and the compounded surplus to be visible in one
   worked example.
5. The anchor is argued in full under *Worked example* in `technical-notes.md`. In outline: entry at
   45 is the research's own reading of the buyer's age distribution [unverified]; 6 000 € plus a
   4 000 € *Zuzahlung* is about a third of the 2026 *Höchstbetrag* of 30 826 € [R2] [unverified],
   which is what a self-employed buyer with a real but not extreme income does; 1,00 % is the
   *Höchstrechnungszins* in force for new business [R16] [REG-R15]; and the guaranteed *Rentenfaktor*
   is **[std]** because **no *Rentenfaktor* level, range or time series exists anywhere in the delib
   corpus, for this or any other product** (gap 4).

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium forms | (i) ***laufender Beitrag*** — a level recurring premium; (ii) ***Zuzahlung*** — a one-off top-up into an existing contract; (iii) ***Einmalbeitrag*** — a single-premium contract. All three are common and all three are modelled | [S1] [R2]; offering [unverified] (6) |
| Representative form | A **level base *Beitrag* plus an annual *Zuzahlung***, because that is the product's actual shape and it makes the *Höchstbetrag* indexation visible | **[std]** (7) |
| Payment frequency | Annual, half-yearly, quarterly or monthly, normally by SEPA direct debit; annual in advance is the base case | **[std]** (8) |
| *Ratenzahlungszuschlag* | Annual 0 %; half-yearly **2 %**; quarterly **3 %**; monthly **5 %**, as a multiplier on the *laufender Beitrag* only | **[std]** (8) |
| Minimum recurring premium | Of the order of **25 € per month** | [unverified]; level **[std]** (9) |
| Maximum contribution | Not a contractual limit but a tax one: the **shared annual *Höchstbetrag*** of § 10 Abs. 3 EStG, `BBG_knappschaftlich × Beitragssatz_knappschaftlich`, doubled on joint assessment | [R2] [R20] [REG-R39] |
| *Höchstbetrag*, single / joint | 2023 **26 528 € / 53 056 €**; 2024 **27 566 € / 55 132 €**; 2025 **29 344 € / 58 688 €**; 2026 **30 826 € / 61 652 €** | [R2] [R20]; every figure [unverified] (10) |
| Deductible share of the capped contribution | **100 %** from the assessment period **2023**, brought forward from 2025 by the *Jahressteuergesetz 2022*; 94 % in 2021 and 96 % in 2022 | [R7]; [unverified] |
| ***Beitragsdynamik*** | A contractual annual escalation with a right to decline individual increases; representative rate **2 % p.a.** | mechanics [R2] [R20]; rate **[std]** (11) |
| Maximum *Zuzahlung* | Not established for any carrier; in practice bounded by the year's remaining *Höchstbetrag* headroom | gap 8; **[std]** |
| Premium suspension and resumption | Suspension is a *Beitragsfreistellung* [R14]; resumption is a *Wiederinkraftsetzung*, usually within a stated window and possibly with renewed underwriting where a BUZ is attached. **No carrier's window was established** | [R14]; gap 8 |
| Premium cessation | At *Rentenbeginn*, at death, and on *Beitragsfreistellung* | [R1] [R14] |
| Age-error and misstatement | §§ 19, 157 and 158 VVG apply as to any German life contract | [REG-R30] |

6. Three premium forms exist and all three are common; **no carrier's actual offering was
   established**. ***Beitragsflexibilität* is the product's defining commercial feature**, and the
   reason it fits a self-employed income: a typical contract is written with a small mandatory
   recurring premium and an open capacity for *Zuzahlungen* up to the year's *Höchstbetrag*. In a good
   year the buyer tops up to the ceiling; in a bad year the buyer pays the minimum, or suspends.
7. The delib Schicht-3 annuity carries a level premium. **A Basisrente model that offers only a level
   regular premium models the wrong product** [REG-R39]: the year-end *Zuzahlung* sized to the
   remaining headroom is the mechanism the tax ceiling creates and the reason the contract is bought.
   The split between the base premium and the *Zuzahlung* is **[std]**; the composite takes 60 / 40 at
   the anchor.
8. **No carrier's frequency loading was established for this product.** The 2 % / 3 % / 5 % ladder is
   carried from the sibling delib corpus as a German market convention and is **[std]** throughout the
   library. The loading is a multiplier on the *laufender Beitrag*; a *Zuzahlung* is a single payment
   and carries none.
9. Minimum premiums exist partly to stop a contract reaching *Rentenbeginn* with a trivial capital,
   because **there is no *Kleinbetragsrenten-Abfindung* in Schicht 1** (see below). No carrier's
   threshold was established.
10. **The series is arithmetic, not evidence.** Each line reproduces itself from its own inputs —
    107 400 × 24,7 % = 26 527,80 → 26 528; 111 600 × 24,7 % = 27 565,20 → 27 566; 118 800 × 24,7 % =
    29 343,60 → 29 344; 124 800 × 24,7 % = 30 825,60 → 30 826 — and the rounding convention (up to the
    next full euro) is inferred from that arithmetic and is itself [unverified]. **The 2026 line is
    the least secure of the four** (gap 11). From 2025 the ceilings are uniform across the former East
    and West [R20] [unverified], which removed a two-decade complication.
11. The *Beitragsdynamik* appears here as on every German life contract, but with **a rationale it
    lacks elsewhere**: the *Höchstbetrag* itself rises every year with the *knappschaftliche* BBG
    [R2] [R20], so a static premium loses relief capacity each year. 2 % p.a. is **[std]**, sized to
    the wage-driven drift of the ceiling series above rather than to any carrier's offering.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Old-age benefit | A **monthly lifelong annuity** on the taxpayer's own life, commencing at *Rentenbeginn* and payable until death | [R1] [REG-R39] |
| Payment timing | Monthly **in advance**; no German market convention on *vorschüssig* against *nachschüssig* was established | gap 21; **[std]** |
| Conversion rule | `monthly_annuity = Kapital(Rentenbeginn) / 10 000 × Rentenfaktor`, with `Rentenfaktor_applied = max(garantierter, aktueller)` | [R17] [S1] |
| ***Garantierter Rentenfaktor*** | Fixed at inception on the *Rechnungsgrundlagen* then in force, with a deliberate prudential margin. Representative value **28,00 €** per month per 10 000 € of capital at age 67 | mechanics [R17] [S1]; level **[std]** (12) |
| ***Aktueller Rentenfaktor*** | The carrier's then-current immediate-annuity tariff at *Rentenbeginn*; the **higher of the two applies** — a guarantee with upside | [R17]; level **[std]** (12) |
| Conversion basis quoted in the corpus | One carrier's Schicht-3 sibling wording computes the guaranteed factor on **DAV 2004 R at an interest basis of 0 % p.a.** | [S1] [R17]; transfer to the Basisrente [unverified] (gap 4) |
| ***Schlussüberschussanteil*** | Allocated **only at *Rentenbeginn***, because the contract has no surrender and therefore no early-exit trigger — a cleaner single-date cash flow than anywhere else in delib | [R15] [REG-R24]; level **[std]** |
| Death benefit, *Aufschubphase*, base design | **Nothing.** The reserve is released to the *Versichertengemeinschaft* as a mortality profit | [R1] [REG-R39] |
| Death benefit, *Aufschubphase*, with the rider | The *Deckungskapital* must **buy a survivor's annuity** for an eligible survivor; with no eligible survivor, **nothing is paid** | [R1] |
| Death benefit, *Rentenphase* | The annuity ends. With a *Rentengarantiezeit*, the remaining instalments continue **only to an eligible survivor** and are **not commutable** | [R1] |
| Permitted survivors | The **spouse or registered partner**, and **children for so long as the taxpayer is entitled to *Kindergeld* or to the *Kinderfreibetrag***. Nobody else — not a cohabiting partner, not a parent, not a sibling, not the estate | [R1] [REG-R39] |
| Lump sums | **None, to anyone, at any time.** No *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no death lump sum, no commutation | [R1] [R23] [REG-R39] |
| Disability benefit | Only through a *Berufsunfähigkeits-Zusatzversicherung* written inside the same contract, subject to the 50 % rule below. **Its cash flows belong to delib product 9** | [R1] [REG-R29] |
| Surplus in payment | The declared *Überschussrente*, in one of the three German payout systems — *konstante*, *teildynamische* or *volldynamische Rente*. Representative: **teildynamisch**, a compounding annual uplift | [R15] [REG-R18]; system and level **[std]** (13) |

12. **No *Rentenfaktor* level, range or time series was established anywhere in the delib corpus, for
    any product** (gap 4). The composite must choose one and it is **[std]**. The argued plausible
    band for a *klassisch* tariff converting at 67 is **24 € to 34 €** per month per 10 000 €, with
    the guaranteed factor at the bottom of the band and the current factor above it. **The guaranteed
    factor is worth materially more on this product than on its Schicht-3 sibling**: in Schicht 3 a
    policyholder facing a poor conversion can take the *Kapitalwahlrecht* instead; here there is no
    alternative, so the guaranteed factor is the **only** protection against a bad conversion. A
    specification that treats the two as equivalent has missed the point. The § 163 VVG adjustment
    channel [REG-R27] and the historic *Treuhänderklausel*, both narrowed by the courts [REG-R36],
    apply here as in Schicht 3; delib treats the guaranteed factor as fixed for the life of the
    contract and records the channel as a model risk.
13. **No carrier's *Überschussverwendung* option list for a Basisrente was established** (gap 17). The
    argument that *verzinsliche Ansammlung* and *Bonusrente* are the natural *Aufschubphase* forms —
    because systems that pay surplus out in cash sit awkwardly with *nicht kapitalisierbar* — is the
    research file's own inference and is not sourced. The payout-phase choice has a **tax dimension it
    does not have in Schicht 3**: the *Rentenfreibetrag* is frozen in euro, so every increase in the
    annuity is fully taxable (see *Regulatory context*), and a rising annuity is worth less after tax
    than the same present value delivered flat.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Underwriting of the main contract | **None in substance.** A deferred annuity on a single life with no death benefit carries no anti-selection the insurer needs to underwrite; the annuity risk runs the other way | [R17]; **[std]** |
| Underwriting of the riders | A *Hinterbliebenenabsicherung* and, decisively, a **BUZ** are fully underwritten, with a health questionnaire, occupation class and the §§ 19 ff. VVG *Anzeigepflicht* regime | [R1] [REG-R29] [REG-R30] |
| Rating factors, main contract | Attained age at entry, deferment term, premium form and frequency, chosen *Rentenbeginn*, and the option set. **Sex may not be a rating factor** | [R1]; unisex [REG-R34] |
| Rating factors, BUZ | Occupation class, health, smoker status, term — all in delib product 9 | [REG-R29] [REG-R37] |
| Mortality basis | **DAV 2004 R**, a ***Generationentafel*** — mortality by birth cohort, with the improvement trend inside the table rather than applied on top of it. First-order probabilities carry prudential margins and are used for premiums, reserving and the guaranteed *Rentenfaktor*; second order is the best estimate | [R17] [REG-R47] [REG-R49] |
| Selection | **Lighter than a comparable Schicht-3 portfolio**, because a Basisrente cannot be surrendered or commuted, so a policyholder in poor health has no exit and nobody leaves the annuitant pool. **No evidence for this was found** | [R17]; **[std]** view (14) |
| Table availability | The DAV tables are the property of the **Deutsche Aktuarvereinigung**, are **not public and are not redistributed by delib** | [R17] [REG-R47] [REG-R49] |
| Interest basis | The ***Höchstrechnungszins***: **1,00 %** for new business from 1 January 2025, the first increase in about thirty years, recommended at 1,00 % for 2026 as well | [R16] [REG-R14] [REG-R15] [REG-R56] |
| Guarantee vintages in an in-force book | 2,75 % (2004–2006), 2,25 % (2007–2011), 1,75 % (2012–2014), 1,25 % (2015–2016), 0,90 % (2017–2021), 0,25 % (2022–2024), 1,00 % (from 2025). **The rate applies at conclusion and stays with the contract for its whole term** | [REG-R15] [REG-R14] |

14. This is a **[std]** view with nothing behind it, and it is stated as such. The direction is
    arguable from the product's own structure — the *Kapitalwahlrecht* is what lets an impaired life
    leave a Schicht-3 annuitant pool, and there is no such exit here — but no German experience study
    was reached. It is a stated model risk in `technical-notes.md`, not a parameter this document
    asserts.

### Charges

**The charge structure is that of any German life contract and is not modified by the layer.** Two
Basisrente-specific points sit on top of it, and both matter.

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* | Financed by ***Zillmerung***, capped at **25 ‰ (2,5 %) of the *Beitragssumme*** by § 4 DeckRV, reduced from 40 ‰ with effect from 1 January 2015 by the LVRG. The rate used at conclusion applies for the whole term | [R16] [REG-R16] [REG-R20]; level **[std]** (15) |
| Acquisition-cost amortisation | Charged to the *Deckungskapital* in **five equal annual instalments** over the first five premium-paying years | **[std]** (16) |
| Acquisition charge on a *Zuzahlung* | A percentage of each *Zuzahlung*, charged in the year it is paid | **[std]** (15); gap 8 |
| *Verwaltungskosten*, % of premium (β) | Representative **7,5 %**; argued band 5 % – 10 % | **[std]** (15) |
| *Verwaltungskosten*, % of the *Deckungskapital* (γ) | Representative **0,35 % p.a.**; argued band 0,2 % – 0,6 % | **[std]** (15) |
| *Stückkosten* | A fixed euro amount per policy per year, inflating | **[std]** (15) |
| *Ratenzahlungszuschlag* | 2 % half-yearly / 3 % quarterly / 5 % monthly | **[std]** (8) |
| Annuity administration | A per-annuitant amount in the *Rentenphase* | **[std]** (15) |
| ***Effektivkosten*** (reduction in yield), *klassisch* | Argued band **0,6 % – 1,2 % p.a.** | **[std]** (15) (17) |
| *Effektivkosten*, *fondsgebunden* with commission | Argued band **1,0 % – 1,8 % p.a.** | **[std]** (15) |
| *Effektivkosten*, *Nettotarif* (fee-based) | Argued band **0,3 % – 0,8 % p.a.**; a real and growing segment on this product | **[std]** (15) |
| The one charge datum in the corpus | Total costs relative to the capital formed of **at most 0,95 € per 100 €** in one carrier's BasisRente and RiesterRente variants, and an ***Abschlussprovision* of 1 575 €** on a specimen quotation | [S2]; both [unverified], both from third-party commentary rather than a tariff sheet |

15. **Every charge level in this document is [std].** No *Effektivkosten* figure and no charge
    schedule was obtained for any carrier (gap 2), which is the most consequential gap in the corpus:
    the § 7 AltZertG *Produktinformationsblatt* exists **precisely** to publish a comparable
    total-charge number for this product, per quotation, and not one was reached. The bands above are
    the reference implementation's parameter set with its reasoning attached, **not a market survey**,
    and must be labelled that way wherever they are reused.
16. **Whether the AltZertG's five-year spreading of acquisition and distribution costs reaches
    *Basisrentenverträge* was not established** (gap 8) — § 1 imposes it on Riester contracts and what
    § 5a picks up for Schicht 1 is unresolved [R10] [REG-R43]. The five-year spread is adopted as
    **[std]** because it is the LVRG-era German market shape and because § 169 VVG's independent
    five-year floor [REG-R28] produces the same profile on every other German regular-premium
    contract. Note that § 169 VVG itself is **inoperative here** — it governs what must be *paid* on
    surrender and nothing is ever paid — so the five-year spread is adopted for its effect on the
    *Deckungskapital*, not because a surrender-value floor requires it.
17. **The *Beitragssumme* is large on this product.** A long-dated contract with a *Beitragsdynamik*
    and regular *Zuzahlungen* accumulates a big *Beitragssumme*, so a 25 ‰ cap permits a large **euro**
    amount of acquisition cost — far above what the same percentage would allow on a short contract.
    **How *Zuzahlungen* enter the *Beitragssumme* for the cap — at all, or on a separate charge basis
    — was not established** (gap 8); the composite excludes them from the base *Beitragssumme* and
    charges them a separate percentage, which is the conservative reading and is **[std]**.

### Termination and values

**There is no exit that pays money.** That is the operative summary and it is the first sentence of
this section for a reason.

| Parameter | Representative value | Basis |
|---|---|---|
| ***Rückkaufswert*** | **None, at any duration.** § 169 VVG is inoperative because the entitlement may not be capitalised. There is a *Deckungskapital*; there is no duration at which any part of it is payable as capital | [R1] [R14] [REG-R28] [REG-R39] |
| *Stornoabzug* | **Not applicable** — there is no surrender payment for a deduction to be made from | [R14] [REG-R28] |
| ***Kündigung*** | § 168 VVG's termination right formally survives, but **termination produces no payment**; in practice a purported *Kündigung* is administered as a *Beitragsfreistellung* | [R14] [REG-R28]; AVB wording [unverified] |
| ***Beitragsfreistellung*** | Exercisable **at any time**, effective at the end of the current premium period; converts to a **premium-free entitlement to a reduced annuity** computed from the *Deckungskapital* reached, less any agreed deduction | [R14] [REG-R28] |
| *Mindestversicherungsleistung* | The reduced benefit must reach a threshold agreed in the contract. **No carrier's threshold was established** | [R14]; gap 8; **[std]** |
| Reversibility | Premiums can normally be resumed within a stated window (*Wiederinkraftsetzung*). **No window was established** | gap 8 |
| Status of a paid-up contract | **Still a Basisrente**: still certified, still protected, still taxed on the *Besteuerungsanteil*, still payable only as an annuity from the statutory floor age. Nothing about going premium-free releases the constraints | [R1] [R9] [R14] |
| Policy loan | **Prohibited** — *nicht beleihbar* | [R1] [REG-R39] |
| Assignment, sale, secondary market | **Prohibited** — *nicht übertragbar*, *nicht veräußerbar*. The German life secondary market, which exists for Schicht-3 endowments, cannot touch this product | [R1] [REG-R39] |
| Transfer to another provider | **Unresolved.** The market understanding is that a transfer to another *Basisrentenvertrag of the same person* is tax-neutral, the entitlement not passing to a third party, but the conditions live in the BMF guidance and could not be established | [R18]; gap 13; **must not be asserted** |
| *Versorgungsausgleich* | The **one permitted transfer**: on divorce, German pension-sharing law splits entitlements acquired during the marriage, and the receiving spouse's entitlement remains subject to the same prohibitions. The mechanism — *interne* or *externe Teilung* — was not established and delib does not model it | [R1]; gap 14 |
| *Widerruf* | The 30-day life-assurance withdrawal right applies as to any German life contract | [REG-R23] |
| Expiry | **There is none.** The contract runs from conclusion to the death of the annuitant; there is no maturity date and no maturity value | [R1] |

---

## Contractual mechanics

Each subsection states one operative rule, quotes it in this document's own words — **nothing here is
quoted from an instrument** — and says what it does to a cash-flow model.

### The five prohibitions, taken one at a time

The rule: the entitlements arising under the contract must be **not inheritable, not transferable,
not chargeable as security, not saleable and not convertible into capital** [R1] [REG-R39]. This
five-limb sentence is the definition of the product; each limb has a direct modelling consequence.

| Limb | What it forbids | Modelling consequence |
|---|---|---|
| ***nicht vererblich*** | The entitlement forms no part of the estate; on death, capital does not pass to heirs | With no rider, **death before *Rentenbeginn* pays nothing**; the reserve is released as a mortality profit |
| ***nicht übertragbar*** | The entitlement may not be assigned to a third party | No assignment decrement, no third-party-interest complication; the only permitted transfer is the *Versorgungsausgleich* |
| ***nicht beleihbar*** | The entitlement may not be pledged, mortgaged or borrowed against | **No policy loan** — delib's retired name `loan_bal` must not reappear on this product |
| ***nicht veräußerbar*** | The contract may not be sold | No secondary market, no assignment-to-a-buyer decrement |
| ***nicht kapitalisierbar*** | The entitlement may not be turned into capital | **No *Rückkaufswert*, no *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no *Kleinbetragsrenten-Abfindung*** |

**The prohibitions bind the insurer's product design, not merely the policyholder's rights.** A
contract offering any of these features is not a *Basisrentenvertrag*, cannot be certified [R9], and
attracts no relief [R3]. That is stronger than a contractual restriction: it is a condition of the tax
status of the whole contract, and it is why the model carries these as structural absences rather
than as switched-off options.

**What *nicht vererblich* does not mean.** It does not mean the contract may not pay on death; it
means the entitlement is not part of the estate and may not be directed by will. Within the narrow
channel described under *Riders and options* a death benefit is permitted, **provided it is itself
paid as an annuity**.

### Certification under § 5a AltZertG, and what it does not import

The rule: certification by the **Bundeszentralamt für Steuern** is a condition of the *relief*, not
of the contract's validity [R3] [R9] [REG-R43]. It is a **formal conformity check** — does the
contract meet the § 10 Abs. 1 Nr. 2 Buchst. b conditions and the AltZertG's own information
requirements — and each certified tariff receives a *Zertifizierungsnummer*. § 2 Abs. 2, or a
provision to that effect, states expressly that **certification is not a seal of quality** [R10]: a
*Zertifizierungsnummer* on a *Versicherungsschein* is a tax fact, not a value judgement, and every
delib document mentioning it repeats that.

**What § 5a does not import from § 1 is as important as what it does.** The Riester
***Beitragserhaltungsgarantie*** — the promise that at least the nominal contributions and *Zulagen*
are available at the start of the payout phase, with up to 20 % of total contributions left out of
account where they secure biometric cover [REG-R43] — **has no Schicht-1 counterpart**. A Basisrente
may be sold with a 100 % *Beitragsgarantie*, a partial one, or **none at all**. That single omission
is why the two subsidised layers have diverged so sharply in product design since the interest-rate
collapse: Riester writers had to hold a nominal guarantee that became unaffordable at a 0,25 %
*Höchstrechnungszins* and withdrew from the market; Basisrente writers simply dropped the guarantee
and kept selling. The drafting mechanism is [unverified]; the substance is settled and universally
relied on.

The certification regime also carries the pre-sale information obligations of § 7 AltZertG [R11]
[REG-R43]: a standardised, **quotation-specific** *Produktinformationsblatt* on a common form, carrying
the ***Effektivkosten*** — the total charge burden as a single annualised reduction in yield — and a
***Chancen-Risiko-Klasse*** from **CRK 1 to CRK 5**, computed by the *Produktinformationsstelle
Altersvorsorge* on a common capital-market model the insurer does not control. **delib does not
implement the PIA simulation**, and reproducing a CRK would require a scenario set that is neither
public nor in scope [REG-R43]. The document's current field list, its scenario set and the number of
risk classes beyond the five were not established (gap 7), and how the § 7 AltZertG PIB interacts
with the PRIIPs *Basisinformationsblatt* on a unit-linked Basisrente is unresolved (gap 6) and must
not be asserted [S13] [S14] [REG-R32].

### The Höchstbetrag, the knappschaftliche peg, and why the ceiling is shared

The rule: contributions under § 10 Abs. 1 Nr. 2 **letters a and b together** — statutory pension,
*Versorgungswerk*, *Alterskasse* **and** Basisrente — are deductible up to a **single annual
*Höchstbetrag***, doubled for spouses assessed jointly [R2] [REG-R39]. Since 2015 the ceiling equals
the maximum annual contribution to the ***knappschaftliche Rentenversicherung***:

    Hoechstbetrag(year) = BBG_knappschaftlich(year) x Beitragssatz_knappschaftlich(year)

The *knappschaftliche* branch is used, rather than the general one, because it has both a higher
*Beitragsbemessungsgrenze* and a higher contribution rate, so the Basisrente ceiling sits materially
above the general BBG contribution. The inputs come from the annual
*Sozialversicherungsrechengrößen-Verordnung* [R20], **which has to be re-read every year for this
product in a way that is not true of any other delib product**.

**The ceiling is shared, and that is the constraint that bites.** A *Freiberufler* in a
*Versorgungswerk*, or a *Handwerker* with compulsory GRV membership, has most of it consumed under
letter a before any Basisrente contribution is considered. The buyer with the whole ceiling free is
the **genuinely non-insured self-employed person** — the product's core market.

**The ceiling moves every year, and so should the premium.** It is indexed to a wage-driven
social-insurance parameter, which is why *Beitragsdynamik* and year-end *Zuzahlungen* are far more
prominent here than on a Schicht-3 annuity, and why the representative premium is a stream rather
than a level amount.

### The employee reductions — two mechanisms that must not be conflated

The rule: two distinct mechanisms operate on an employee [R2] [REG-R39], and they are routinely
confused.

1. **The GRV contributions consume the ceiling.** Employee **and** employer contributions to the
   statutory scheme both count toward the same *Höchstbetrag*. A Basisrente contribution is
   deductible only inside whatever headroom is left.
2. **The tax-free employer share is then subtracted from the deductible amount**, because it was
   never taxed in the employee's hands and may not be relieved twice.

In model notation, all figures for one calendar year:

    base       = min( GRV_employee + GRV_employer + Basisrente_contribution , Hoechstbetrag )
    deductible = base x 1.00                      # 100 % from 2023  [R7]
    allowed    = deductible - GRV_employer        # the tax-free employer share  [R2]

**A third reduction applies to taxpayers with a non-contributory pension entitlement** — *Beamte*,
judges, soldiers, and controlling shareholder-directors with a *Pensionszusage*. For them the ceiling
is reduced by a **notional total contribution** to the general statutory scheme computed on their
remuneration, leaving very little headroom [R2] [unverified]. That is why the product is effectively
closed to *Beamte* even though nothing forbids them buying it.

**None of this is a liability cash flow.** The relief accrues to the policyholder through the tax
system, never through the insurer. Its place in a delib model is **upstream of the model point**: it
determines how large the premium is and why it is shaped the way it is.

### Premium flexibility — the operative shape of the contribution stream

The rule, in the composite's own terms: the contract carries a small mandatory ***laufender
Beitrag***, escalating annually under a ***Beitragsdynamik*** the policyholder may decline
individually, plus an open capacity for ***Zuzahlungen*** up to the year's remaining *Höchstbetrag*
headroom, plus the right to convert the whole contract to premium-free at any time [R14].

For the model this means the premium is a **stream with three components** — a level base, a
contractual escalation, and a behavioural top-up — and only the first is a contract fact. The
*Zuzahlung* take-up is a **modeller's view**, because the buyer pays it out of a profit that is not
known until the year end. **No carrier's minimum premium, maximum *Zuzahlung* or suspension rule was
established** and all three are **[std]** (gap 8).

### The Rechnungszins, the guarantee vintages and the Zillmerung cap

The rule: § 2 DeckRV fixes the maximum interest rate at which a German life insurer may discount its
statutory *Deckungsrückstellung* for contracts carrying an interest guarantee, and therefore —
through § 138 Abs. 1 VAG's requirement that premiums be adequate to fund that reserve [REG-R8] — the
maximum rate at which a new tariff may be priced [R16] [REG-R14]. **The rate applies at the time of
conclusion and then stays with the contract for its whole term.**

Two consequences a Basisrente specification must carry. First, a Basisrente book written since 2005
is a **layered stack of guarantee vintages** spanning the whole decline from 2,75 % to 0,25 % and the
2025 recovery to 1,00 % [REG-R15], so an in-force model point carries its cohort's rate rather than
today's. Second, the *Zinszusatzreserve* [REG-R17] and the § 139 VAG *Bewertungsreserven* test
[REG-R9] both run on the **HGB** side of the balance sheet, not on the Solvency II side, and neither
is a cash flow of this contract.

The parallel rule on acquisition cost: § 4 DeckRV caps the *Zillmersatz* at **25 ‰ of the
*Beitragssumme***, reduced from 40 ‰ with effect from 1 January 2015 by the LVRG, and the rate used at
conclusion applies for the whole term [R16] [REG-R16] [REG-R20]. On a long-dated Basisrente with a
*Beitragsdynamik* the *Beitragssumme* is large, so the cap permits a large euro amount.

### Überschussbeteiligung — unchanged by the layer, with two differences

The rule: the policyholder is statutorily entitled to a share of the *Überschuss* and of the
*Bewertungsreserven* unless participation is expressly excluded [R15] [REG-R24]. **A Basisrente
participates on exactly the same terms as any other German life contract** — the layer changes the
tax and the exits, not the surplus machinery. The four surplus sources (*Zins-*, *Risiko-*, *Kosten-*
and *übriger Überschuss*), the *RfB*, the MindZV minimum allocation of **90 % of the investment result
net of the *Rechnungszinsen*, 90 % of the risk result and 50 % of the cost result** [REG-R18], the
RfBV [REG-R19] and the annual declaration at the balance date all apply unchanged.

**Two things are different, and both follow from the prohibitions.**

1. **The *Überschussverwendung* options are narrower in the *Aufschubphase*.** Systems that pay
   surplus out in cash sit awkwardly with *nicht kapitalisierbar*; *verzinsliche Ansammlung* and
   *Bonusrente*, which keep the value inside the contract and convert it into annuity at
   *Rentenbeginn*, are the natural forms. No carrier's option list was established (gap 17) and this
   is the research file's own inference.
2. **The *Schlussüberschussanteil* has no early-exit trigger.** On an endowment a terminal bonus is
   allocated at maturity and, partly, on surrender. A Basisrente has no surrender, so it is allocated
   **only at *Rentenbeginn*** — a cleaner single-date cash flow than anywhere else in delib.

**No declared rate specific to a Basisrente was established.** The market-average declared rates
carried in sibling delib files are Schicht-3 and endowment figures and **must not be relabelled**.

### The conversion at Rentenbeginn

The rule [R17] [S1]:

    monthly_annuity      = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor
    Rentenfaktor_applied = max( Rentenfaktor_garantiert , Rentenfaktor_aktuell(Rentenbeginn) )

Three things happen at *Rentenbeginn* on a German deferred annuity, and **only two of them survive
into Schicht 1**: the accumulated capital is converted at a *Rentenfaktor* — survives; the
*Überschussverwendung* system for the payout phase is fixed — survives; the *Kapitalwahlrecht* is
exercised or allowed to lapse — **does not exist here** [R1].

That third absence is what makes the guaranteed factor load-bearing. **The economic price of the ban
is that the policyholder bears conversion risk with no way out**, which is why the guaranteed
*Rentenfaktor* is the product's most valuable guarantee, and why a specification that treats this
conversion as the Schicht-3 one has missed the product.

For the model the conversion is a **single-date event**: the whole fund, including the terminal
bonus, leaves the *Deckungskapital* and becomes an annuity obligation. There is no election switch, no
take-up assumption, and no notice-period parameter — three simplifications relative to the Schicht-3
chassis, and all three are consequences of the ban rather than modelling choices.

### The annuity in payment, and the Besteuerungsanteil

The rule: benefits from a *Basisrentenvertrag* are *sonstige Einkünfte* taxed on a
***Besteuerungsanteil*** fixed by the **calendar year in which the annuity begins** — the
*Kohortenprinzip* — and the taxpayer's age, income and contribution history are irrelevant to the
percentage [R4] [REG-R41]. The schedule: 50 % for annuities beginning in or before 2005, rising **two
points per cohort year to 80 % for 2020**, **one point per year for 2021 and 2022**, and **half a
point per year from 2023** after the *Wachstumschancengesetz* [R6], reaching **100 % for 2058**.
Selected values, **every one [unverified]**: 2023 **82,5 %**; 2024 **83,0 %**; 2025 **83,5 %**; 2026
**84,0 %**; 2040 **91,0 %**; 2058 **100,0 %**. The table is internally consistent — 82,5 + 35 × 0,5 =
100,0 for 2058, and 82,5 + 17 × 0,5 = 91,0 for 2040 — and that arithmetic is the only corroboration
this library can offer for it.

***Der Rentenfreibetrag ist ein Euro-Betrag.*** The untaxed complement is computed **once**, in the
first full calendar year of receipt, as a euro amount, and is then **frozen for life** [R4]
[REG-R41]. Two consequences a specification must state. **Every subsequent increase in the annuity is
fully taxable**, so a *volldynamische Rente*, whose whole point is that it rises, is taxed at an
effective rate climbing towards 100 % of the increment. And **the choice of *Überschussverwendung*
system in the payout phase therefore has a tax dimension it does not have in Schicht 3**, where the
*Ertragsanteil* percentage is what is frozen and surplus increases are taxed at the same light rate.

**A delib model does not compute tax.** The *Besteuerungsanteil* belongs here, not in the projection:
delib models publish gross best-estimate liability cash flows. Its role is to explain the product's
economics and to justify the model point.

### Beitragsfreistellung against Kündigung — the exits

The rule: § 165 VVG gives the policyholder of a contract with periodic premiums the right at any
time, for the end of the current premium period, to demand conversion into a **premium-free contract
with a reduced benefit**, provided the reduced benefit reaches a *Mindestversicherungsleistung* agreed
in the contract [R14] [REG-R28]. **This right survives intact in a Basisrente and is the product's
only real exit.**

§ 168 VVG's termination right survives too, **but it has nothing to pay out**: because the contract
may not be capitalised [R1], termination cannot produce a *Rückkaufswert*, and in practice a purported
*Kündigung* operates as a *Beitragsfreistellung*. The AVB wording is [unverified]; the outcome is
settled and universal.

**Why this matters more here than anywhere else in delib.** Elsewhere *Kündigung* and
*Beitragsfreistellung* are two exits competing for the same policyholder and a model must not merge
them. Here **there is only one**, and that has two modelling consequences: the *Beitragsfreistellung*
rate should sit **above** a Schicht-3 lapse rate at short durations — the buyer's income is volatile
by construction and going premium-free is free of penalty and reversible — and **below** it at long
durations, because there is no realisable value to tempt anyone out. That shape is **[std]**; **no
lapse rate, no *Beitragsfreistellung* rate and no market *Stornoquote* specific to the Basisrente was
established** (gap 3).

### The ban on Kapitalwahl and Teilkapitalauszahlung

The rule: *nicht kapitalisierbar* forbids a capital election outright [R1] [REG-R39]. **There is no
*Kapitalwahlrecht*** — the policyholder has no election at *Rentenbeginn*, the capital becomes a
monthly lifelong annuity and that is the whole of it. **There is no *Teilkapitalauszahlung* either**:
a Riester contract may pay up to **30 %** of the capital as a lump sum at the start of the payout
phase [R23] [REG-R43] [unverified]; a Schicht-3 contract may pay 100 %; a Basisrente may pay
**nothing**.

A third absence follows: **the § 20 Abs. 1 Nr. 6 EStG regime never engages.** The *Unterschiedsbetrag*
and the 12/62 rule [REG-R45] are Schicht-3 mechanics that reach a Basisrente at no point in its life.

### Kleinbetragsrente — the answer is no

The rule, and it is stated here because the interesting fact is its **non-application**. For a
**Riester** contract § 93 Abs. 3 EStG permits the **commutation of a *Kleinbetragsrente*** at the
start of the payout phase without loss of the subsidy, where the monthly annuity would fall below a
threshold expressed as **1 % of the monthly *Bezugsgröße* of § 18 SGB IV** [R23] [unverified]. It is a
de-minimis rule that exists because administering a trivially small lifelong annuity costs more than
it pays.

**There is no Schicht-1 equivalent.** § 10 Abs. 1 Nr. 2 Buchst. b forbids capitalisation without
qualification and admits **no de-minimis exception whatever** [R1]. A Basisrente entitlement of two
euros a month is paid as two euros a month, for life.

What the market does instead — every item [unverified], because no carrier document was reached:
**minimum premiums**, so that a contract cannot easily reach *Rentenbeginn* with a trivial capital;
**minimum annuity thresholds in the AVB**, below which the insurer may pay at longer intervals,
quarterly or annually instead of monthly, whose compatibility with the statutory requirement of a
*monatliche* annuity lives in the BMF guidance and **was not established** (gap 19); and
**consolidation before *Rentenbeginn*** into one contract, which depends on the unresolved transfer
question (gap 13). **The modelling consequence is direct**: no commutation option anywhere, and a
model point representing a small paid-up contract must project a small annuity rather than a lump
sum.

### Pfändungsschutz, insolvency and means-testing

The rule: § 851c Abs. 1 ZPO makes claims to benefits attachable **only as earnings from employment**
where all of the following hold — the benefit is granted at **regular intervals, for life, and not
before the completion of the 60th year of age**, or only on the occurrence of *Berufsunfähigkeit*; the
claims **may not be disposed of**; the **designation of third parties other than survivors as
beneficiaries is excluded**; and **no capital payment other than on death has been agreed** [R12]
[REG-R40]. § 851c Abs. 2 protects amounts saved under such a contract, subject to annual limits and
an **aggregate ceiling of 340 000 €** [REG-R40] [unverified].

**The four requirements of § 851c Abs. 1 are the same four features § 10 Abs. 1 Nr. 2 Buchst. b
demands** — three instruments, one product description. Two cautions. The **age condition in § 851c
is 60, not 62**, so a contract written to the EStG standard clears § 851c with room to spare, but the
two are genuinely different provisions with different histories and must not be merged (gap 10). And
**the annual savings allowances are contradicted across summaries** — a two-band 6 000 € / 7 000 €
ladder reported as current law since 1 January 2022 against a 2 000 € – 9 000 € age-graded ladder
reported as pre-2022 [REG-R40] — so this document states the **shape** (age-graduated annual
allowance, aggregate ceiling) and **prints no annual band** (gap 9).

**§ 12 SGB II and § 90 SGB XII** exempt from means-testing old-age provision whose realisation is
contractually excluded [R13]. Taken with § 851c this is the market's *insolvenzfest* and
*Hartz-IV-fest* claim, and it is the principal non-tax reason a self-employed person buys the
product. All three paragraph addresses are [unverified] and the precise conditions were not
established; the **direction** is not in doubt.

---

## Riders and options

**In scope and parameterized in the model, off in the base run:**

***Hinterbliebenenabsicherung* (survivor's annuity).** The permitted beneficiaries are closed to the
**spouse or registered partner** and to **children while *Kindergeld* or the *Kinderfreibetrag* runs**
— in practice to the completion of the 18th year, or the 25th while in education [R1] [unverified] on
the ages. **Everything paid to a survivor must be paid as an annuity** [R1], which converts the two
familiar German death-benefit designs into something different:

| Design | In Schicht 3 | In Schicht 1 |
|---|---|---|
| ***Beitragsrückgewähr*** in the *Aufschubphase* | Premiums paid, or the *Deckungskapital*, returned as a **lump sum** to any named beneficiary | The same amount must **buy a survivor's annuity** for an eligible survivor; with no eligible survivor, **nothing is paid** |
| ***Rentengarantiezeit*** in the *Rentenphase* | Remaining instalments continue to any named beneficiary, often commutable | Remaining instalments continue **only to an eligible survivor**, and are **not commutable**; with none, payments cease |
| **Spouse's / survivor's annuity** | An optional rider on a freely chosen life | The **natural** form here, because it is the only form that fits the channel |

**The consequence for a model is a conditional probability, not a benefit.** The value of any
*Hinterbliebenenschutz* on a Basisrente is the value of the benefit **multiplied by the probability
that an eligible survivor exists at the moment of death** — a spouse alive and still married, or a
child still inside the *Kindergeld* window. On a contract taken at 45 and running to 67 the child
channel has usually closed long before *Rentenbeginn*, so in practice the cover is a spouse cover.
That probability is **[std]** with no evidence behind it, and it is one of the more consequential
**[std]** choices in the whole delib library.

**The cover costs annuity.** Every euro of survivor cover reduces the *Rentenfaktor* or raises the
premium. The sibling delib corpus's Schicht-3 illustration put a 10-year *Rentengarantiezeit* at
roughly **0,5 %** of the annuity, 20 years at **2,6 %** and 30 years at **8,0 %** — [unverified],
**Schicht-3 figures, not transferable**, and **no Basisrente-specific cost was established**. The
composite carries the *Rentenfaktor* reduction as a **[std]** table keyed by the option, anchored on
those figures and labelled as non-transferable.

***Rentengarantiezeit*.** A guaranteed payment period measured from *Rentenbeginn*, representative
values 0, 10 or 20 years, payable only to an eligible survivor and never commutable [R1].

***Berufsunfähigkeits-Zusatzversicherung* (BUZ), and the 50 % rule.** § 10 Abs. 1 Nr. 2 Buchst. b
permits, inside the same contract, cover against *Berufsunfähigkeit* and against *verminderte
Erwerbsfähigkeit* [R1] [REG-R29]. The premium for that cover is then deductible **inside the
Schicht-1 *Höchstbetrag*** at 100 % [R2] [R7]. **The 50 % rule**: the contributions qualify only if
**more than half of the total contribution is attributable to the old-age provision**, so the
supplementary covers — disability and survivor together — must stay **below 50 %** of the total
[R1] [unverified] as to the statutory address, settled as substance. Three consequences:

- **A standalone Basisrenten-BU does not exist.** The disability cover must ride on an old-age
  contract that is itself more than half the premium.
- The rule **caps the achievable disability annuity** for a given total premium, which is exactly the
  legislator's intention.
- It is a **hard constraint on a model point**: `buz_prem_share < 0.50` is an invariant the test
  module asserts.

**Why anyone does this, and what it costs.** The premium for a *selbständige
Berufsunfähigkeitsversicherung* (delib product 9) falls into *sonstige Vorsorgeaufwendungen* under
§ 10 Abs. 1 Nr. 3a EStG, whose small ceiling is in practice already exhausted by health and
long-term-care contributions, so it is **effectively not deductible at all**; the same cover as a BUZ
inside a Basisrente is deductible in full inside a much larger ceiling. **The counterweight is the tax
on the benefit**: a *BU-Rente* from a *Basisrentenvertrag* is taxed with the **full cohort
*Besteuerungsanteil*** [R4] [REG-R41], not at the *Ertragsanteil* of the *abgekürzte Leibrente* from a
standalone SBU [unverified] (gap 16). **The buyer is trading relief now for a heavily taxed benefit
later, at a moment — disability — when income has collapsed and the marginal rate may be low.** That
is the whole of the BUZ-versus-SBU argument and this document states it as a trade rather than as an
advantage. Further constraints, [unverified] in every particular: the cover ends at the latest at the
main contract's *Rentenbeginn*; the *BU-Rente* is itself subject to the non-capitalisation rule; and a
premium waiver is the normal companion cover. **No carrier's BUZ wording was reached** [S5] (gap 18).

***Beitragsdynamik*** and ***Zuzahlung***, treated above, are contractual options rather than riders
and are **on** in the base run, because they are the shape of the product's premium.

**Out of scope.** Everything a Schicht-3 or Riester contract offers and this one may not: the
*Kapitalwahlrecht*, the *Teilkapitalauszahlung*, the *Kleinbetragsrenten-Abfindung*, the policy loan,
the assignment, the secondary-market sale, and any death lump sum to any beneficiary. These are not
switched-off options; they are **structural absences**, and the model carries no cells for them.

---

## Variations across insurers

**An honest variations table for this product is almost entirely a record of what could not be
compared.** Two carriers produced any artefact at all, and neither produced a term. Presenting a rich
table here would be a fabrication, so what follows is the real state of the evidence.

| Feature | CosmosDirekt [S1] | Allianz [S2] [S3] | The other nineteen carriers [S4]–[S11] |
|---|---|---|---|
| Basisrente wording located | **yes — four tariff codes**, LA 1100 A, LA 1079 A, LA 936 A, LA 1099 A | no; the chassis is evidenced by a broker-hosted specimen and a product page | **no** |
| Edition date | not established | specimen dated by its path to 02/2025 [unverified] | not established |
| Asset form | not established | hybrid: *Sicherungsvermögen* plus *Spezialfonds* | not established |
| Guarantee level published | no | **yes** — 60 / 80 / 90 % of premiums paid, 80 % standard [unverified] | no |
| *Rentenfaktor* basis published | not for the Basisrente; the Schicht-3 sibling names DAV 2004 R at 0 % p.a. | expressed as a minimum annuity amount | no |
| Charge figure published | no | **yes** — 1 575 € *Abschlussprovision*; ≤ 0,95 € per 100 € of capital formed [unverified] | no |
| Layer sold on a common chassis | not established | **yes** — PrivatRente / BasisRente / RiesterRente are one design | not established |
| *Produktinformationsblatt* obtained | no | no | no |

**A range table needs two observations of one parameter and this corpus supplies exactly one:** at
least **four Basisrente tariff wordings maintained in parallel at one carrier** [S1] [unverified] —
which is what a tariff family looks like when *klassisch*, *fondsgebunden* and vintage editions
coexist, and is the single most useful structural fact the corpus yields about the product's market
form.

**Everything a variations table would normally carry has no observation at all**: entry ages, minimum
premiums, maximum *Zuzahlung*, permitted *Rentenbeginn* range, *Rentengarantiezeit* durations,
survivor-cover forms, BUZ terms, *Effektivkosten*, guarantee levels beyond one carrier,
*Mindestversicherungsleistung*, fund universes. Twenty named German life writers whose Basisrente
documents exist were not reached and **not one of them contributes a single fact** [S11] (gap 1).

The carriers are named so that a checker knows where to go, with nothing attached beyond what each is
named for: **Alte Leipziger** (*AL_RoyalBasisRente*, repeatedly placed at the top of independent
Basisrente ratings) [S4] [R24]; **NÜRNBERGER** (a principal *Berufsunfähigkeit* writer, and therefore
the natural place to look for a **BUZ written inside a Basisrente** and for the 50 % constraint in
contractual terms — **the single most valuable document this corpus could not reach**) [S5];
**Volkswohl Bund** [S6]; **LV 1871** (the best-known ***fondsgebundene* Basisrente with an open fund
and ETF universe and no *Beitragsgarantie***, and so the form a checker should verify first) [S7]
[unverified]; **Swiss Life** (a hybrid with a selectable guarantee level) [S8]; **Continentale** [S9];
**Stuttgarter** (whose *index-safe* naming, if right, would be an **index-linked Basisrente** — a
fourth asset form and a bridge to delib product 4; gap 12) [S10]; and the further carriers of [S11],
for which **nothing whatever** was established.

**What varies, on the reasoning rather than the evidence.** Four dimensions can be stated as ranges
because they follow from the statute and the market's structure rather than from a comparison:

| Dimension | Range the market is understood to show | Status |
|---|---|---|
| Asset form | *klassisch* · *fondsgebunden ohne Garantie* · *fondsgebunden mit Beitragsgarantie* at 60 / 80 / 90 % of premiums paid · possibly index-linked | [S2] [S7] [S8] [S10]; the distribution across them is [unverified] (gap 3) |
| Guarantee vintage in force | 2,75 % down to 0,25 % and back to 1,00 %, by conclusion year | [REG-R15]; a structural certainty, not a carrier variation |
| Distribution | Predominantly **brokers and independent advisers**; the fee-based ***Nettotarif*** segment is more developed here than on most German life products | [unverified] |
| Charge level | The *Effektivkosten* bands of the charge table above | **[std]**, argued not observed (gap 2) |

**What does not vary, and why.** The five prohibitions, the age floor, the ban on *Kapitalwahl* and
commutation, the absence of a *Rückkaufswert*, the closed list of permitted survivors, the 50 % rule
and the *Besteuerungsanteil* cohort table are **statutory** [R1] [R4] [R8] [R23] [REG-R39] [REG-R41].
No carrier can vary any of them and remain certified. That is unusual in this repository: on most
delib products the composite has to argue a representative choice against an observed spread, whereas
here **the product's defining features are the ones no insurer may choose**, and the [std] parameters
are confined to levels — charges, the *Rentenfaktor*, the surplus path, the behavioural rates.

---

## Regulatory context

**Tax — the layer.** The *Alterseinkünftegesetz* of 2004, effective **1 January 2005**, built the
three-layer architecture, introduced ***nachgelagerte Besteuerung*** for the first layer and created
the Basisrente so that the self-employed — who have no access to the statutory scheme — would have a
vehicle with the same tax treatment [R5] [REG-R38]. It responded to a *Bundesverfassungsgericht*
decision on the unequal taxation of *Beamtenpensionen* and statutory pensions [unverified] as to the
year and the case, and followed the report of the commission chaired by **Bert Rürup**, from which
the market name. **No *Bundesgesetzblatt* citation is given for the AltEinkG, the
*Wachstumschancengesetz* [R6], the *Jahressteuergesetz 2022* [R7] or the *Jahressteuergesetz 2007*
[R8], because none could be confirmed** (gap 23).

**Tax — the two amendments that softened the transition.** The *Jahressteuergesetz 2022* brought the
**100 % deductibility** of Schicht-1 contributions forward from 2025 to the assessment period **2023**
[R7]; the *Wachstumschancengesetz* of 2024 reduced the annual step in the *Besteuerungsanteil* from
one percentage point to **half a point**, retrospectively for the **2023** cohort — which is why 2023
is 82,5 % and not 83 % — and moved the 100 % year from **2040 to 2058** [R6] [REG-R41]. Both were the
legislator's response to the ***Doppelbesteuerung*** litigation: two Bundesfinanzhof decisions of
19 May 2021, commonly cited as **X R 33/19** and **X R 20/19** [unverified] as to both file numbers,
which accepted **in principle** that double taxation is unconstitutional where contributions were made
from taxed income and benefits are taxed again, found none on the facts, but identified the transition
schedule as capable of producing one for later cohorts — **particularly for self-employed taxpayers
whose contributions during the phase-in were only partly deductible**, which is precisely this
product's own buyer [R19]. **It is a slowing of the transition, not a change of principle.**

**Tax — the remaining pieces, none of them a liability cash flow.** A *Hinterbliebenenrente* is taxed
in the survivor's hands on the same cohort basis, with the cohort year determined by the start of that
annuity — **not established** (gap 20). A private annuity is not a *Versorgungsbezug*, so a pensioner
compulsorily insured in the *Krankenversicherung der Rentner* is generally not subject to health and
long-term-care contributions on it while a **voluntarily insured** pensioner pays [R13] [REG-R46]
[unverified] (gap 21) — a difference of the order of **18 % of the annuity**, large enough to flag as
a driver of the after-tax comparison without asserting the rule.

**Contract law.** The VVG governs the contract throughout [REG-R22], with § 171's *halbzwingende*
character meaning the listed provisions may not be varied to the policyholder's detriment. The
operative sections for this product are **§ 153** (*Überschussbeteiligung* and the half-share in the
*Bewertungsreserven*) [R15] [REG-R24]; **§ 165** (*Beitragsfreistellung*), **§ 168** (*Kündigung*) and
**§ 169** (*Rückkaufswert*, inoperative here) [R14] [REG-R28]; **§ 163** (*Prämien- und
Leistungsänderung*) [REG-R27]; **§§ 154 and 155** (*Modellrechnung* and *Standmitteilung*) [REG-R25];
**§§ 8 and 152** (*Widerruf*) [REG-R23]; **§§ 19, 37, 38, 157 and 158** (*Anzeigepflicht*, payment
default, misstatement of age) [REG-R30]; and **§§ 172–177** for a BUZ [REG-R29]. Certified contracts
carry an **annual statement** under § 7a AltZertG [S15] [unverified] as to the paragraph, whose
interest for delib is that it names side by side the state variables a projection model must carry —
contributions paid in the year, accumulated value, guaranteed benefit and projected annuity. **The
field list was not established.**

**Prudential.** The insurer is a Solvency II undertaking supervised under the VAG [REG-R5] [REG-R6],
writing this contract in the *Lebensversicherung* Sparte, with the *Sicherungsvermögen* and the
prudent-person principle of § 124 VAG governing the assets [REG-R7]. Premium calculation and equal
treatment run under § 138 VAG [REG-R8]; the *Überschussbeteiligung* and the *Sicherungsbedarf* test on
*Bewertungsreserven* under § 139 VAG [REG-R9]; the *RfB* under §§ 140 and 145 VAG with the MindZV and
the RfBV beneath them [REG-R10] [REG-R18] [REG-R19]. The statutory *Deckungsrückstellung* runs on the
DeckRV [REG-R14] [REG-R16] [REG-R17] and the HGB accounts on §§ 341–341o HGB and the RechVersV
[REG-R54]; the *Zinszusatzreserve* exists in no other jurisdiction in this repository and is an
**HGB** reserve, not a Solvency II one. **AnlV investment quotas do not bind this insurer** — since
1 January 2016 they reach only small undertakings under §§ 212–217 VAG and domestic Pensionskassen
and Pensionsfonds [REG-R7], and German market writing routinely misapplies them.

**Conduct and disclosure.** The § 7 AltZertG *Produktinformationsblatt* and the *Effektivkosten*
computed individually per contract offer [R11] [REG-R43] sit on top of the VVG-InfoV product-level
regime [REG-R31]; PRIIPs reaches the unit-linked and hybrid forms [REG-R32]; the IDD and § 34d GewO
govern the distribution this product depends on [REG-R33]. **A Basisrente is squarely inside BaFin's
conduct-supervision perimeter** for capital-forming life products sold through commissioned
intermediaries [R21] [REG-R35], and the *Effektivkosten* on the PIB is the number that supervision
runs on. **Nothing Basisrente-specific was established from BaFin** (gap 15).

**Actuarial and professional.** The *Rechnungsgrundlagen erster und zweiter Ordnung* distinction, and
the DAV's ownership of the tables, are set out at [REG-R47]; **DAV 2004 R and DAV 2004 R-Bestand** are
the annuity bases [R17] [REG-R49], **DAV 1997 I / RI / TI** the *Berufsunfähigkeit* family a BUZ would
need [REG-R50], and Destatis the only freely reusable German mortality series [REG-R52]. The DAV's
*Fachgrundsätze* and its annual *Höchstrechnungszins* recommendation govern the practice [REG-R56].
IFRS 17 applies to IFRS reporters and this contract is a direct-participating one that would be
measured under the variable fee approach [REG-R55]; nothing in this library implements it.

**Rating and comparison.** Four houses are the German market's standing sources for comparative
analysis in this layer — the **Institut für Vorsorge und Finanzplanung**, **Franke und Bornberg**,
**Morgen & Morgen** and **Assekurata** [R24] [REG-R53]. The IVFP publishes the best-known Basisrente
rating, scoring tariffs on company strength, flexibility, transparency, cost and return. **Not one
rating, score, ranking or figure was established for the Basisrente**, and no downstream document may
invent one.

**Living texts.** The *Höchstrechnungszins* is 1,00 % for 2025 and recommended at 1,00 % for 2026
[R16]; the *Besteuerungsanteil* for a 2026 cohort is 84,0 % [unverified]; the *Höchstbetrag* for 2026
is 30 826 € [unverified]; the deductible share has been 100 % since 2023; the full-taxation year is
2058. **Every one of those moves.** The *Höchstbetrag* moves annually with the
*Sozialversicherungsrechengrößen-Verordnung* [R20] and the *Besteuerungsanteil* moves annually by
construction. Check both, and every paragraph number in this document, before relying on anything
here.
