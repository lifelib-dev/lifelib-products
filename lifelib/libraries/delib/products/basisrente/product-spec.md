# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation: 2026-08-29).

**Retrieval conditions — read this first.** **No document cited anywhere in this specification was
retrieved.** Direct HTTP egress from the build environment is blocked by an organisation network
policy, and the session's `WebSearch` budget was exhausted before this product was reached, so this
document rests on a research file (`_research/basisrente.md`) written with **no research channel of
any kind**. A delib citation is a **pointer, not a certificate**: an [R1] tag names the instrument a
claim must be checked against; it does not assert that anyone read it. Nothing below is quoted from a
German statutory or contractual text. Every specific paragraph number, date, amount, percentage and
market figure carries [unverified] unless a sibling delib research file corroborated it by search
while search was still available. Where a mechanic is certain and its level is not, this document
ships a **[std]** parameter with its rationale rather than a fabricated source tag.

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modelling of a German **Basisrente** (*Rürup-Rente*) — the *Basisrentenvertrag* of
§ 10 Abs. 1 Nr. 2 Buchst. b EStG, the privately written, funded member of *Schicht 1* of the German
three-layer retirement architecture. **It does not describe any single insurer's product**, and here
that disclaimer is stronger than usual: the corpus contains **two** carrier artefacts, neither of
them a *Bedingungswerk*, so the composite is built from the **statute and the market's settled
mechanics** rather than from a comparison of contracts. [S#] tags mark primary product documents and
[R#] product-specific regulatory and actuarial references, both numbered per
`_research/basisrente.md` and resolved in `sources.md` (numbering frozen); [REG-R#] refers to the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose own
numbering is distinct and also frozen. **[std]** marks a standardization introduced for the reference
implementation, each with a rationale and an argued plausible range where the research recorded one.

**Out of scope.** The *Riester-Rente* (Schicht 2, delib product 6) and the *klassische private
Rentenversicherung* (Schicht 3, delib product 2) share this chassis and appear only as contrasts. The
competing Schicht-1 vehicles of § 10 Abs. 1 Nr. 2 Buchst. **a** are not modelled, but they **consume
the same annual ceiling** and that is treated below as a first-order fact about demand. The
*Fonds-Basisrente*, *betriebliche Altersversorgung*, *Gruppenversicherung*, *private
Krankenversicherung* and *Sterbegeldversicherung* are outside delib entirely.

---

## Product overview and market role

A Basisrente is an **ordinary German life insurance contract governed by the VVG** [R14] [R15]
[REG-R22], on a single life, which additionally satisfies the definitional conditions of
§ 10 Abs. 1 Nr. 2 Buchst. b EStG [R1] [REG-R39] and holds a certificate under § 5a AltZertG [R9]
[REG-R43]. It is not a separate legal species: everything true of a German deferred annuity is true
of it — the same *Deckungskapital* recursion, the same *Überschussbeteiligung*, the same
*Rentenfaktor*, the same DAV 2004 R basis — unless the § 10 conditions displace it.

**The product is defined by prohibitions, not by benefits.** Its accumulation and payout mechanics
are those of the delib `klassische_rentenversicherung` product. What makes it a distinct product, and
what a projection model has to get right, is a closed list of five things it may **not** do: the
entitlement must be *nicht vererblich* (not inheritable), *nicht übertragbar* (not transferable),
*nicht beleihbar* (not chargeable as security), *nicht veräußerbar* (not saleable) and *nicht
kapitalisierbar* (not convertible into capital) [R1] [REG-R39]. Everything below follows from that
sentence, and three consequences change the shape of the projected cash flows:

1. **There is no *Rückkaufswert* at any duration.** The § 169 VVG surrender-value regime [R14]
   [REG-R28] is **inoperative**: the contract has a *Deckungskapital* like any other and **there is
   no duration at which any part of it is payable to the policyholder as capital**. This is the
   single most important thing a modeller coming from the delib endowment or Schicht-3 chassis has
   to unlearn.
2. ***Beitragsfreistellung* is the only exit, and it is not a lapse.** § 165 VVG's right to convert
   to a premium-free contract with a reduced benefit survives intact [R14]; § 168 VVG's termination
   right survives too but **produces no payment**. The policyholder facing a cash crisis has exactly
   one lever, and the paid-up cohort is a **large permanent part of the book, not a residue**.
3. **Death before *Rentenbeginn* pays nothing in the base design.** *Nicht vererblich* means the
   entitlement forms no part of the estate and may not be directed by will [R1]; with no
   *Hinterbliebenenabsicherung* the reserve is released to the *Versichertengemeinschaft* as a
   mortality profit. Where the rider is present the permitted beneficiaries are **closed** and
   **everything paid to a survivor must be paid as an annuity**.

**The layer is a tax wrapper, not a chassis.** [S2] is the direct evidence: one large insurer sells
the same design — the same premium split, the same selectable guarantee levels, the same
*Rentenfaktor* machinery — as PrivatRente (Schicht 3), BasisRente (Schicht 1) and RiesterRente
(Schicht 2), differing only in the wrapper. A Basisrente model should therefore reuse the Schicht-3
chassis with the constraint set bolted on.

**What the buyer is buying** is three things at once, and the model point makes no sense without all
three. The ***Sonderausgabenabzug***: from the assessment period 2023 the capped contribution is
deductible **in full** [R7] [REG-R39], inside an annual ceiling — the ***Höchstbetrag*** — pegged
since 2015 to the maximum contribution to the *knappschaftliche Rentenversicherung* [R2] [R20].
***Pfändungsschutz***: a compliant entitlement is attachable only on the scale that applies to
earnings, and the fund is protected up to an age-graduated annual allowance subject to an **aggregate
ceiling of 340 000 €** [R12] [REG-R40] [unverified]. And ***nachgelagerte Besteuerung*** on the way
out [R4] [REG-R41]. **The protection is a by-product of the prohibitions, not an added feature** —
there is nothing to attach because there is nothing to realise.

**Two buyer populations, and the model point table represents both.** The **self-employed person with
no compulsory scheme** — the buyer the product was designed for: the entire *Höchstbetrag* is free,
the *Pfändungsschutz* matters as much as the relief, and the income is volatile, which is what the
*Zuzahlung* structure is for. And the **high-earning employee or partner using residual headroom** as
a late-career deferral vehicle, frequently by *Einmalbeitrag*, entering at 50 or later with a short
deferment. In both cases the entry age is **materially higher than for a Riester or Schicht-3
contract** — the mid-forties rather than the early thirties [unverified] — because the product only
makes sense once income is high enough for the relief to be worth the illiquidity. **The commercial
problem** follows: the relief is real and large, but **the contract is irreversible**. That is not a
defect; it is the consideration for the *Pfändungsschutz* and the relief.

**Market size — the weakest material in this document.** No statistic from the GDV, the BMF or any
consumer or comparison source was established [R22] [S16] (gap 3). The orders of magnitude, every one
[unverified] general knowledge: **of the order of two and a half million** contracts in force against
**fifteen to sixteen million** Riester contracts and falling; **of the order of a hundred thousand**
new contracts a year on a declining count trend; an **average contribution of two to four thousand
euro a year** against roughly eight hundred for a Riester contract. Its share of new business by
**premium** is much higher than by count. **Nothing downstream may cite a delib figure for the size of
the Basisrente market.** For context, the *Altersvorsorgereformgesetz* — Bundesrat consent **8 May
2026**, new subsidised model from **1 January 2027** [REG-R44] — closes *Riester* to new business and
leaves the Basisrente untouched.

---

## Representative specification

The representative design is a **single-life, individual, *klassisch* (general-account)
Basisrentenvertrag on an annual grid**, certified under § 5a AltZertG, with a level *laufender
Beitrag* plus an annual *Zuzahlung*, priced and reserved at the current *Höchstrechnungszins* on a
DAV 2004 R first-order basis, *gezillmert* toward the 25 ‰ cap, converting at *Rentenbeginn* into a
monthly lifelong annuity at `max(garantierter, aktueller) Rentenfaktor`, with **no *Kapitalwahlrecht*,
no *Teilkapitalauszahlung*, no *Rückkaufswert*, no policy loan and no assignment**. The one
commutation Schicht 1 does permit — the *Kleinbetragsrenten-Abfindung* [REG-R42] — is **left out of
the base run as a stated standardization** (**[std]**), not as a prohibition; the distinction is drawn
out under *The ban on capitalisation* below, because an earlier reading of this product had it as a
prohibition and that was wrong.

**Why *klassisch* rather than *fondsgebunden*.** The market's centre of gravity has moved decisively
to *fondsgebundene* Basisrenten since the *Höchstrechnungszins* fell below 1 % [R16] [REG-R15] — a
judgement that is [unverified] general knowledge unsupported by any figure in this corpus (gap 3).
The composite nevertheless models the *klassisch* form: **the Schicht-1 constraints are the subject of
this product and are clearest against a general-account chassis whose reserve recursion the library
already has**, while the unit-linked machinery is carried by delib product 3 and the hybrid guarantee
mechanics by delib product 4.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type and wrapper | Individual single-life deferred annuity, general account (*klassisch*), profit-participating, certified *Basisrentenvertrag*; the policyholder and the insured life are the **same person**, because the annuity must be on the taxpayer's own life | [R1] [R9] [R15] [REG-R39]; form choice **[std]** (1) |
| Certification | *Zertifizierungsnummer* issued by the **Bundeszentralamt für Steuern** under § 5a AltZertG, required for contracts concluded from **1 January 2010**. A **formal conformity check**, expressly **not a quality mark**: it says nothing about charges, investment quality or the provider's strength | [R9] [R10] [REG-R43]; date [unverified] |
| Asset form | (i) `klassisch` — general account, modelled; (ii) `fondsgebunden ohne Garantie`; (iii) `fondsgebunden mit Beitragsgarantie` (hybrid) | (i) **[std]** (1); (ii) [S7] [unverified]; (iii) [S2] [S8] |
| Lives basis | Single life. A second life may enter only through the permitted *Hinterbliebenenabsicherung* | [R1] |
| Entry ages | 18 to the low sixties; no statutory floor or ceiling on entry, only on *Rentenbeginn* | **[std]** (2) |
| Earliest *Rentenbeginn* | Completion of the **62nd** year of life for contracts concluded **after 31 December 2011**; the **60th** for contracts concluded on or before that date | [R1] [R8] [REG-R39]; both [unverified] (3) |
| Latest and representative *Rentenbeginn* | **No statutory ceiling**; contracts commonly allow deferral past the statutory retirement age. Representative attained age **67** | [R1]; **[std]** (2) (4) |
| Annuity form | **Monthly, lifelong, on the taxpayer's own life.** No term-certain annuity, no *Auszahlungsplan* of the Riester type, no annuity on any other single life | [R1] [REG-R39] |
| Anchor model cell | Entry age 45, *Rentenbeginn* 67, conclusion year 2026, *laufender Beitrag* 6 000,00 € p.a. annual in advance with a 2 % *Beitragsdynamik*, *Zuzahlung* 4 000,00 € p.a., *Rechnungszins* 1,00 %, guaranteed *Rentenfaktor* 28,00 €, no riders | **[std]** (5) |

Footnotes to **[std]** rows:

1. **All three asset forms are sold**, and the absence of a statutory *Beitragsgarantie* is what makes
   the third optional rather than mandatory [R9] [R10] [REG-R43] — the sharpest structural contrast
   with Riester. A fourth form, an **index-linked Basisrente**, is plausible from one carrier's tariff
   naming [S10] but **was not established** (gap 12).
2. **No carrier's entry-age or permitted *Rentenbeginn* range was established** (gap 8): twenty named
   German life writers publish this and none was reached [S11]. The envelope is the market shape, not
   an observation.
3. The commissioning brief for the research file stated the pre-2012 floor as **63**; the research
   file resolved it against **60** and this document adopts that. Both figures are [unverified] — no
   source in this session confirmed them — but the 60/62 split is settled German practice and 63
   corresponds to no threshold in this statute. **The § 851c ZPO age condition is 60, not 62** [R12]
   [REG-R40]: different provisions, different histories, and a reader must not merge them (gap 10).
4. Age 67 sits above both statutory floors, matches the *Regelaltersgrenze*, and gives a 22-year
   deferment from the anchor's entry age — long enough for the *Zillmerung*, the *Beitragsdynamik* and
   the compounded surplus to be visible at once.
5. Argued in full under *Worked example* in `technical-notes.md`. In outline: entry at 45 is the
   research's own reading of the buyer's age distribution [unverified]; 6 000 € plus a 4 000 €
   *Zuzahlung* is about a third of the 2026 *Höchstbetrag* [R2] [unverified]; 1,00 % is the
   *Höchstrechnungszins* for new business [R16] [REG-R15]; and the guaranteed *Rentenfaktor* is
   **[std]** because **no *Rentenfaktor* level, range or time series exists anywhere in the delib
   corpus** (gap 4).

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium forms | (i) ***laufender Beitrag*** — a level recurring premium; (ii) ***Zuzahlung*** — a one-off top-up into an existing contract; (iii) ***Einmalbeitrag*** — a single-premium contract. All three are common and all three are modelled | [S1] [R2]; offering [unverified] (6) |
| Representative form | A **level base *Beitrag* plus an annual *Zuzahlung***, split 60 / 40 at the anchor; the market minimum recurring premium is of the order of **25 € per month** [unverified] | **[std]** (7) (9) |
| Payment frequency | Annual, half-yearly, quarterly or monthly; annual in advance is the base case | **[std]** (8) |
| *Ratenzahlungszuschlag* | Annual 0 %; half-yearly **2 %**; quarterly **3 %**; monthly **5 %**, as a multiplier on the *laufender Beitrag* only | **[std]** (8) |
| Maximum contribution and maximum *Zuzahlung* | Not a contractual limit but a tax one: the **shared annual *Höchstbetrag*** of § 10 Abs. 3 EStG, `BBG_knappschaftlich × Beitragssatz_knappschaftlich`, doubled on joint assessment. No carrier's *Zuzahlung* ceiling was established (gap 8) | [R2] [R20] [REG-R39]; **[std]** |
| *Höchstbetrag*, single / joint | 2023 **26 528 / 53 056 €**; 2024 **27 566 / 55 132 €**; 2025 **29 344 / 58 688 €**; 2026 **30 826 / 61 652 €** | [R2] [R20]; every figure [unverified] (10) |
| Deductible share of the capped contribution | **100 %** from the assessment period **2023**, brought forward from 2025; 94 % in 2021 and 96 % in 2022 | [R7]; [unverified] |
| ***Beitragsdynamik*** | Contractual annual escalation with a right to decline individual increases; representative **2 % p.a.**, sized to the drift of the ceiling series rather than to any carrier's offering, because the *Höchstbetrag* rises annually with the *knappschaftliche* BBG so a static premium loses relief capacity each year | mechanics [R2] [R20]; rate **[std]** |
| Suspension, resumption, cessation | Suspension is a *Beitragsfreistellung*; resumption is a *Wiederinkraftsetzung* within a stated window (**not established**, gap 8). Premiums cease at *Rentenbeginn*, at death and on *Beitragsfreistellung* | [R1] [R14]; gap 8 |
| Misstatement and payment default | §§ 19, 37, 38, 157 and 158 VVG apply as to any German life contract | [REG-R30] |

6. **No carrier's actual offering was established.** ***Beitragsflexibilität* is the product's
   defining commercial feature** and the reason it fits a self-employed income: a small mandatory
   recurring premium with an open capacity for *Zuzahlungen* up to the year's *Höchstbetrag*.
7. The delib Schicht-3 annuity carries a level premium. **A Basisrente model that offers only a level
   regular premium models the wrong product** [REG-R39]: the year-end *Zuzahlung* sized to the
   remaining headroom is the mechanism the tax ceiling creates. The 60 / 40 split is **[std]**.
8. **No carrier's frequency loading was established.** The 2 % / 3 % / 5 % ladder is carried from the
   sibling delib corpus as a German market convention and is **[std]** throughout the library. It
   loads the *laufender Beitrag*; a *Zuzahlung* is a single payment and carries none.
9. Minimum premiums exist partly to stop a contract reaching *Rentenbeginn* with a capital too small
   to administer as a lifelong annuity. A *Kleinbetragsrenten-Abfindung* **is** available in Schicht 1
   [REG-R42], but only at the start of the payout phase and only below a threshold whose level is
   contested, so the minimum premium is still doing work. No level was established.
10. **The series is arithmetic, not evidence.** Each line reproduces itself from its own inputs —
    107 400 × 24,7 % = 26 527,80 → 26 528; 111 600 × 24,7 % = 27 565,20 → 27 566; 118 800 × 24,7 % =
    29 343,60 → 29 344; 124 800 × 24,7 % = 30 825,60 → 30 826 — and the rounding convention is
    inferred from that arithmetic and is itself [unverified]. **The 2026 line is the least secure**
    (gap 11). From 2025 the ceilings are uniform across the former East and West [R20] [unverified].

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Old-age benefit | A **monthly lifelong annuity** on the taxpayer's own life, from *Rentenbeginn* until death, paid **in advance** — no German market convention on *vorschüssig* against *nachschüssig* was established (gap 21). Conversion rule: `monthly_annuity = Kapital(Rentenbeginn) / 10 000 × Rentenfaktor`, `Rentenfaktor_applied = max(garantierter, aktueller)` | [R1] [R17] [S1] [REG-R39]; timing **[std]** |
| ***Garantierter Rentenfaktor*** | Fixed at inception on the *Rechnungsgrundlagen* then in force, with a deliberate prudential margin — one carrier's Schicht-3 sibling wording computes it on **DAV 2004 R at an interest basis of 0 % p.a.**, [unverified] as a Basisrente fact (gap 4). Representative **28,00 €** per month per 10 000 € at age 67 | mechanics [R17] [S1]; level **[std]** (11) |
| ***Aktueller Rentenfaktor*** | The carrier's then-current immediate-annuity tariff at *Rentenbeginn*; the **higher of the two applies** — a guarantee with upside | [R17]; level **[std]** (11) |
| ***Schlussüberschussanteil*** | Allocated **only at *Rentenbeginn***, because the contract has no surrender and therefore no early-exit trigger — a cleaner single-date cash flow than anywhere else in delib | [R15] [REG-R24]; level **[std]** |
| Death benefit, *Aufschubphase*, base design | **Nothing.** The reserve is released as a mortality profit | [R1] [REG-R39] |
| Death benefit, *Aufschubphase*, with the rider | The *Deckungskapital* must **buy a survivor's annuity** for an eligible survivor; with no eligible survivor, **nothing is paid** | [R1] |
| Death benefit, *Rentenphase* | The annuity ends. With a *Rentengarantiezeit*, remaining instalments continue **only to an eligible survivor** and are **not commutable** | [R1] |
| Permitted survivors | The **spouse or registered partner**, and **children while *Kindergeld* or the *Kinderfreibetrag* runs**. Nobody else — not a cohabiting partner, not a parent, not a sibling, not the estate | [R1] [REG-R39] |
| Lump sums | **None, to anyone, at any time.** No *Kapitalwahlrecht*, no *Teilkapitalauszahlung*, no death lump sum, no commutation | [R1] [R23] [REG-R39] |
| Disability benefit | Only through a BUZ written inside the same contract, subject to the 50 % rule. **Its cash flows belong to delib product 9** | [R1] [REG-R29] |
| Surplus in payment | The declared *Überschussrente*, in one of *konstante*, *teildynamische* or *volldynamische Rente*. Representative: **teildynamisch**, a compounding annual uplift | [R15] [REG-R18]; system and level **[std]** (12) |

11. **No *Rentenfaktor* level, range or time series was established anywhere in the delib corpus**
    (gap 4). The argued plausible band for a *klassisch* tariff converting at 67 is **24 € to 34 €**
    per month per 10 000 €, guaranteed factor at the bottom and current factor above it. **The
    guaranteed factor is worth materially more here than on the Schicht-3 sibling**: there a
    policyholder facing a poor conversion can take the *Kapitalwahlrecht* instead; here there is no
    alternative, so it is the **only** protection against a bad conversion. The § 163 VVG channel
    [REG-R27] and the historic *Treuhänderklausel*, both narrowed by the courts [REG-R36], apply as in
    Schicht 3; delib treats the guaranteed factor as fixed and records the channel as a model risk.
12. **No carrier's *Überschussverwendung* option list was established** (gap 17); that *verzinsliche
    Ansammlung* and *Bonusrente* are the natural *Aufschubphase* forms — cash-paying systems sitting
    awkwardly with *nicht kapitalisierbar* — is the research file's own inference. The payout-phase
    choice has a **tax dimension it lacks in Schicht 3**: the *Rentenfreibetrag* is frozen in euro, so
    every increase in the annuity is fully taxable.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Underwriting of the main contract | **None in substance.** A deferred annuity with no death benefit carries no anti-selection the insurer needs to underwrite; the annuity risk runs the other way | [R17]; **[std]** |
| Underwriting of the riders | A *Hinterbliebenenabsicherung* and, decisively, a **BUZ** are fully underwritten, under the §§ 19 ff. VVG *Anzeigepflicht* regime | [R1] [REG-R29] [REG-R30] |
| Rating factors, main contract | Entry age, deferment term, premium form and frequency, chosen *Rentenbeginn*, option set. **Sex may not be a rating factor** for contracts concluded from 21 December 2012 and is carried for reporting only | [R1]; unisex [REG-R34] |
| Mortality basis | **DAV 2004 R**, a ***Generationentafel*** — mortality by birth cohort, with the improvement trend inside the table rather than applied on top. First-order probabilities carry prudential margins and price the contract and the guaranteed *Rentenfaktor*; second order is the best estimate. The DAV tables are the association's property, **not public and not redistributed by delib** | [R17] [REG-R47] [REG-R49] |
| Selection | **Lighter than a comparable Schicht-3 portfolio**, because the contract cannot be surrendered or commuted, so a policyholder in poor health has no exit and nobody leaves the annuitant pool. **No evidence for this was found**; the direction is arguable from the product's own structure, but no German experience study was reached, so it is a stated model risk rather than a parameter this document asserts | [R17]; **[std]** view |
| Interest basis | The ***Höchstrechnungszins***: **1,00 %** for new business from 1 January 2025, the first increase in about thirty years, recommended at 1,00 % for 2026 | [R16] [REG-R14] [REG-R15] [REG-R56] |
| Guarantee vintages in force | 2,75 % (2004–2006), 2,25 % (2007–2011), 1,75 % (2012–2014), 1,25 % (2015–2016), 0,90 % (2017–2021), 0,25 % (2022–2024), 1,00 % (from 2025). **The rate applies at conclusion and stays with the contract for its whole term** | [REG-R14] [REG-R15] |

### Charges

**The charge structure is that of any German life contract and is not modified by the layer**, with
two Basisrente-specific points on top of it.

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* | Financed by ***Zillmerung***, capped at **25 ‰ (2,5 %) of the *Beitragssumme*** by § 4 DeckRV, reduced from 40 ‰ with effect from 1 January 2015 by the LVRG. The rate used at conclusion applies for the whole term | [R16] [REG-R16] [REG-R20]; level **[std]** (13) |
| Acquisition-cost amortisation | Charged to the *Deckungskapital* in **five equal annual instalments** over the first five premium-paying years; a *Zuzahlung* carries its own percentage charge in the year it is paid | **[std]** (14); gap 8 |
| *Verwaltungskosten*, % of premium (β) | Representative **7,5 %**; argued band 5 % – 10 % | **[std]** (13) |
| *Verwaltungskosten*, % of the *Deckungskapital* (γ) | Representative **0,35 % p.a.**; argued band 0,2 % – 0,6 % | **[std]** (13) |
| *Stückkosten* | A fixed euro amount per policy per year, inflating | **[std]** (13) |
| Annuity administration | A per-annuitant amount in the *Rentenphase* | **[std]** (13) |
| ***Effektivkosten***, *klassisch* | Argued band **0,6 % – 1,2 % p.a.** | **[std]** (13) (15) |
| *Effektivkosten*, other forms | *fondsgebunden* with commission **1,0 % – 1,8 % p.a.**; *Nettotarif* (fee-based) **0,3 % – 0,8 % p.a.**, a real and growing segment on this product | **[std]** (13) |
| The one charge datum in the corpus | Total costs relative to the capital formed of **at most 0,95 € per 100 €** in one carrier's BasisRente and RiesterRente variants, and an ***Abschlussprovision* of 1 575 €** on a specimen quotation | [S2]; both [unverified], both from third-party commentary rather than a tariff sheet |

13. **Every charge level in this document is [std].** No *Effektivkosten* figure and no charge
    schedule was obtained for any carrier (gap 2), the most consequential gap in the corpus: the
    § 7 AltZertG *Produktinformationsblatt* exists **precisely** to publish a comparable total-charge
    number for this product, per quotation, and not one was reached. The bands are the reference
    implementation's parameter set with its reasoning attached, **not a market survey**.
14. **Whether the AltZertG's five-year spreading of acquisition costs reaches *Basisrentenverträge*
    was not established** (gap 8) — § 1 imposes it on Riester contracts and what § 5a picks up is
    unresolved [R10] [REG-R43]. The spread is adopted as **[std]** because it is the LVRG-era German
    market shape and because § 169 VVG's independent five-year floor [REG-R28] produces the same
    profile on every other German regular-premium contract. Note that § 169 VVG is itself
    **inoperative here** — it governs what must be *paid* on surrender — so the spread is adopted for
    its effect on the *Deckungskapital*, not because a surrender-value floor requires it.
15. **The *Beitragssumme* is large on this product**, so a 25 ‰ cap permits a large **euro** amount of
    acquisition cost, far above what the same percentage allows on a short contract. **How
    *Zuzahlungen* enter the *Beitragssumme* for the cap was not established** (gap 8); the composite
    excludes them and charges them a separate percentage, the conservative reading and **[std]**.

### Termination and values

**There is no exit that pays money.** That is the operative summary, and it is the first sentence of
this section for a reason.

| Parameter | Representative value | Basis |
|---|---|---|
| ***Rückkaufswert*** | **None, at any duration.** § 169 VVG is inoperative because the entitlement may not be capitalised. There is a *Deckungskapital*; there is no duration at which any part of it is payable as capital | [R1] [R14] [REG-R28] [REG-R39] |
| *Stornoabzug* | **Not applicable** — no surrender payment exists for a deduction to be made from | [R14] [REG-R28] |
| ***Kündigung*** | § 168 VVG's termination right survives, but **produces no payment**; in practice it is administered as a *Beitragsfreistellung* | [R14] [REG-R28]; AVB wording [unverified] |
| ***Beitragsfreistellung*** | Exercisable **at any time**, effective at the end of the current premium period; converts to a **premium-free entitlement to a reduced annuity** computed from the *Deckungskapital* reached | [R14] [REG-R28] |
| *Mindestversicherungsleistung* | The reduced benefit must reach a threshold agreed in the contract. **No carrier's threshold was established** | [R14]; gap 8; **[std]** |
| Status of a paid-up contract | **Still a Basisrente**: still certified, still protected, still taxed on the *Besteuerungsanteil*, still payable only as an annuity from the statutory floor age | [R1] [R9] [R14] |
| Policy loan, assignment, sale | **Prohibited** — *nicht beleihbar*, *nicht übertragbar*, *nicht veräußerbar*. The German life secondary market, which exists for Schicht-3 endowments, cannot touch this product | [R1] [REG-R39] |
| Transfer to another provider | **Unresolved.** The market understanding is that a transfer to another *Basisrentenvertrag of the same person* is tax-neutral, but the conditions live in the BMF guidance and could not be established | [R18]; gap 13; **must not be asserted** |
| *Versorgungsausgleich* | The **one permitted transfer**: on divorce, pension-sharing law splits entitlements acquired during the marriage, and the receiving spouse's entitlement remains subject to the same prohibitions. The mechanism was not established and delib does not model it | [R1]; gap 14 |
| *Widerruf* and expiry | The 30-day life-assurance withdrawal right applies as to any German life contract [REG-R23]. **There is no expiry**: the contract runs from conclusion to the death of the annuitant, with no maturity date and no maturity value | [REG-R23]; [R1] |

---

## Contractual mechanics

Each subsection states one operative rule in this document's own words — **nothing here is quoted
from an instrument** — and says what it does to a cash-flow model.
### The five prohibitions, taken one at a time

The rule: the entitlements arising under the contract must be **not inheritable, not transferable,
not chargeable as security, not saleable and not convertible into capital** [R1] [REG-R39].

| Limb | What it forbids | Modelling consequence |
|---|---|---|
| ***nicht vererblich*** | The entitlement forms no part of the estate; on death capital does not pass to heirs | With no rider, **death before *Rentenbeginn* pays nothing**; the reserve is released as a mortality profit |
| ***nicht übertragbar*** | Assignment to a third party | No assignment decrement, no third-party interest; the only permitted transfer is the *Versorgungsausgleich* |
| ***nicht beleihbar*** | Pledge, mortgage, borrowing against | **No policy loan** — delib's retired name `loan_bal` must not reappear on this product |
| ***nicht veräußerbar*** | Sale of the contract | No secondary market, no sale decrement |
| ***nicht kapitalisierbar*** | Turning the entitlement into capital | **No *Rückkaufswert*, no *Kapitalwahlrecht*, no *Teilkapitalauszahlung***. The prohibition has **one express statutory exception**, the *Kleinbetragsrenten-Abfindung* of § 10 Abs. 1 Nr. 2 Satz 3 EStG [REG-R42], which this model does not implement (**[std]**) |

**The prohibitions bind the insurer's product design, not merely the policyholder's rights.** A
contract offering any of these features is not a *Basisrentenvertrag*, cannot be certified [R9], and
attracts no relief [R3] — a condition of the tax status of the whole contract, which is why the model
carries these as **structural absences** rather than switched-off options. **What *nicht vererblich*
does not mean**: it does not forbid a payment on death, only that the entitlement is not part of the
estate and may not be directed by will. A death benefit is permitted inside the narrow channel below,
**provided it is itself paid as an annuity**.

### Certification under § 5a AltZertG, and what it does not import

The rule: certification by the **Bundeszentralamt für Steuern** is a condition of the *relief*, not
of the contract's validity [R3] [R9] [REG-R43]. It is a **formal conformity check** and each
certified tariff receives a *Zertifizierungsnummer*. § 2 Abs. 2, or a provision to that effect, states
expressly that **certification is not a seal of quality** [R10]: it is a tax fact, not a value
judgement, and every delib document repeats that.

**What § 5a does not import from § 1 is as important as what it does.** The Riester
***Beitragserhaltungsgarantie*** — at least the paid-in contributions and *Zulagen* available at the
start of the payout phase, with up to 20 % of contributions left out of account where they secure
biometric cover [REG-R43] — **has no Schicht-1 counterpart**. A Basisrente may be sold with a 100 %
*Beitragsgarantie*, a partial one, or **none at all**. That omission is why the two subsidised layers
diverged so sharply after the interest-rate collapse: Riester writers had to hold a nominal guarantee
that became unaffordable at a 0,25 % *Höchstrechnungszins* and withdrew; Basisrente writers dropped
the guarantee and kept selling. The drafting mechanism is [unverified]; the substance is settled.

The regime also carries the § 7 AltZertG pre-sale obligations [R11] [REG-R43]: a standardised,
**quotation-specific** *Produktinformationsblatt* carrying the ***Effektivkosten*** and a
***Chancen-Risiko-Klasse*** from **CRK 1 to CRK 5**, computed by the *Produktinformationsstelle
Altersvorsorge* on a common capital-market model the insurer does not control. **delib does not
implement the PIA simulation.** That document's field list was not established (gap 7), and how it
interacts with the PRIIPs *Basisinformationsblatt* is unresolved (gap 6) and must not be asserted
[S13] [S14] [REG-R32].

### The Höchstbetrag, the knappschaftliche peg, and the employee reductions

The rule: contributions under § 10 Abs. 1 Nr. 2 **letters a and b together** — statutory pension,
*Versorgungswerk*, *Alterskasse* **and** Basisrente — are deductible up to a **single annual
*Höchstbetrag***, doubled for spouses assessed jointly [R2] [REG-R39]. Since 2015
`Hoechstbetrag(year) = BBG_knappschaftlich(year) x Beitragssatz_knappschaftlich(year)`: the
*knappschaftliche* branch is used rather than the general one because it has both a higher
*Beitragsbemessungsgrenze* and a higher contribution rate. The inputs come from the annual
*Sozialversicherungsrechengrößen-Verordnung* [R20], **which has to be re-read every year for this
product in a way that is not true of any other delib product**.

**The ceiling is shared, and that is the constraint that bites.** A *Freiberufler* in a
*Versorgungswerk*, or a *Handwerker* with compulsory GRV membership, has most of it consumed under
letter a; the buyer with the whole ceiling free is the **genuinely non-insured self-employed person**.
And **the ceiling moves every year, so the premium should too** — which is why *Beitragsdynamik* and
year-end *Zuzahlungen* are far more prominent here than on a Schicht-3 annuity.

**Two further mechanisms operate on an employee and are routinely conflated** [R2] [REG-R39]. **The
GRV contributions consume the ceiling**, employee and employer alike; **the tax-free employer share is
then subtracted from the deductible amount**, never having been taxed in the employee's hands:

    base       = min( GRV_employee + GRV_employer + Basisrente_contribution , Hoechstbetrag )
    deductible = base x 1.00                      # 100 % from 2023  [R7]
    allowed    = deductible - GRV_employer        # the tax-free employer share  [R2]

**A third reduction applies to taxpayers with a non-contributory entitlement** — *Beamte*, judges,
soldiers, controlling shareholder-directors with a *Pensionszusage* — whose ceiling is reduced by a
**notional** contribution computed on their remuneration [R2] [unverified], which is why the product
is effectively closed to *Beamte*. **None of this is a liability cash flow**: the relief accrues
through the tax system, never through the insurer, and its place in a delib model is **upstream of the
model point** — it determines how large the premium is and why it is shaped the way it is.

### Premium flexibility — the operative shape of the contribution stream

The rule, in the composite's own terms: the contract carries a small mandatory ***laufender
Beitrag***, escalating under a ***Beitragsdynamik*** the policyholder may decline individually, plus
an open capacity for ***Zuzahlungen*** up to the year's remaining *Höchstbetrag* headroom, plus the
right to go premium-free at any time [R14]. For the model the premium is a **stream with three
components** — a level base, a contractual escalation and a behavioural top-up — and **only the first
is a contract fact**: the *Zuzahlung* take-up is a modeller's view, because the buyer pays it out of a
profit not known until the year end.

### The Rechnungszins, the guarantee vintages and the Zillmerung cap

The rule: § 2 DeckRV fixes the maximum rate at which a German life insurer may discount its statutory
*Deckungsrückstellung* for a contract carrying an interest guarantee, and therefore — through
§ 138 Abs. 1 VAG's requirement that premiums be adequate to fund that reserve [REG-R8] — the maximum
rate at which a new tariff may be priced [R16] [REG-R14]. **The rate applies at the time of conclusion
and then stays with the contract for its whole term**, so a Basisrente book written since 2005 is a
**layered stack of guarantee vintages** [REG-R15] and an in-force model point carries its cohort's
rate rather than today's. The *Zinszusatzreserve* [REG-R17] and the § 139 VAG *Bewertungsreserven*
test [REG-R9] run on the **HGB** side of the balance sheet, and neither is a cash flow of this
contract. The parallel rule on acquisition cost: § 4 DeckRV caps the *Zillmersatz* at **25 ‰ of the
*Beitragssumme***, reduced from 40 ‰ from 1 January 2015 by the LVRG, and the rate used at conclusion
applies for the whole term [R16] [REG-R16] [REG-R20].

### Überschussbeteiligung — unchanged by the layer, with two differences

The rule: the policyholder is statutorily entitled to a share of the *Überschuss* and of the
*Bewertungsreserven* unless participation is expressly excluded [R15] [REG-R24]. **A Basisrente
participates on exactly the same terms as any other German life contract** — the layer changes the
tax and the exits, not the surplus machinery: the four surplus sources, the *RfB*, the MindZV minimum
allocation of **90 % of the investment result net of the *Rechnungszinsen*, 90 % of the risk result
and 50 % of the cost result** [REG-R18], the RfBV [REG-R19] and the annual declaration at the balance
date all apply unchanged.

**Two things are different, and both follow from the prohibitions.** First, **the
*Überschussverwendung* options are narrower in the *Aufschubphase***: cash-paying systems sit
awkwardly with *nicht kapitalisierbar*, so *verzinsliche Ansammlung* and *Bonusrente* are the natural
forms — the research file's own inference, not a sourced fact (gap 17). Second, **the
*Schlussüberschussanteil* has no early-exit trigger**: a Basisrente has no surrender, so it is
allocated **only at *Rentenbeginn***, a cleaner single-date cash flow than anywhere else in delib.
**No declared rate specific to a Basisrente was established**, and the market-average rates in sibling
delib files are Schicht-3 and endowment figures that **must not be relabelled**.

### The conversion at Rentenbeginn

The rule [R17] [S1]:

    monthly_annuity      = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor
    Rentenfaktor_applied = max( Rentenfaktor_garantiert , Rentenfaktor_aktuell(Rentenbeginn) )

Three things happen at *Rentenbeginn* on a German deferred annuity and **only two survive into
Schicht 1**: the capital is converted at a *Rentenfaktor*; the *Überschussverwendung* system for the
payout phase is fixed; and the *Kapitalwahlrecht* is exercised or allowed to lapse — which **does not
exist here** [R1]. That third absence is what makes the guaranteed factor load-bearing: **the
policyholder bears conversion risk with no way out**, so it is this product's most valuable guarantee,
and a specification that treats the conversion as the Schicht-3 one has missed the product. For the
model the conversion is a **single-date event**: the whole fund, including the terminal bonus, leaves
the *Deckungskapital* and becomes an annuity obligation, with no election switch, no take-up
assumption and no notice-period parameter — three simplifications that are consequences of the ban
rather than modelling choices.

### The annuity in payment, and the Besteuerungsanteil

The rule: benefits from a *Basisrentenvertrag* are *sonstige Einkünfte* taxed on a
***Besteuerungsanteil*** fixed by the **calendar year in which the annuity begins** — the
*Kohortenprinzip* — the taxpayer's age, income and contribution history being irrelevant to the
percentage [R4] [REG-R41]. The schedule: 50 % for annuities beginning in or before 2005, rising **two
points per cohort year to 80 % for 2020**, **one point per year for 2021 and 2022**, and **half a
point per year from 2023** after the *Wachstumschancengesetz* [R6], reaching **100 % for 2058**.
Selected values, **every one [unverified]**: 2023 **82,5 %**; 2024 **83,0 %**; 2025 **83,5 %**; 2026
**84,0 %**; 2040 **91,0 %**; 2058 **100,0 %** — internally consistent, since 82,5 + 35 × 0,5 = 100,0
and 82,5 + 17 × 0,5 = 91,0, which is the only corroboration this library can offer.

***Der Rentenfreibetrag ist ein Euro-Betrag.*** The untaxed complement is computed **once**, in the
first full calendar year of receipt, and is then **frozen for life** [R4] [REG-R41]. So **every
subsequent increase in the annuity is fully taxable**, a *volldynamische Rente* is taxed at an
effective rate climbing towards 100 % of the increment, and **the choice of *Überschussverwendung*
system in the payout phase has a tax dimension it lacks in Schicht 3**, where the *Ertragsanteil*
percentage is what is frozen. **A delib model does not compute tax**: the *Besteuerungsanteil* belongs
here, not in the projection, and its role is to explain the economics and justify the model point.

### Beitragsfreistellung against Kündigung — the exits

The rule: § 165 VVG gives the policyholder of a contract with periodic premiums the right at any
time, for the end of the current premium period, to demand conversion into a **premium-free contract
with a reduced benefit**, provided the reduced benefit reaches a *Mindestversicherungsleistung* agreed
in the contract [R14] [REG-R28]. **This right survives intact and is the product's only real exit.**
§ 168 VVG's termination right survives too **but has nothing to pay out**: because the contract may
not be capitalised [R1], termination cannot produce a *Rückkaufswert*, and a purported *Kündigung*
operates as a *Beitragsfreistellung*. The AVB wording is [unverified]; the outcome is settled.

**Why this matters more here than anywhere else in delib.** Elsewhere *Kündigung* and
*Beitragsfreistellung* are two exits competing for the same policyholder; here **there is only one**.
The *Beitragsfreistellung* rate should therefore sit **above** a Schicht-3 lapse rate at short
durations — the buyer's income is volatile by construction and going premium-free is free of penalty
and reversible — and **below** it at long durations, because there is no realisable value to tempt
anyone out. That shape is **[std]**; **no *Beitragsfreistellung* rate or market *Stornoquote* specific
to the Basisrente was established** (gap 3).

### The ban on capitalisation — Kapitalwahl, Teilkapital and the Kleinbetragsrente

The rule: *nicht kapitalisierbar* forbids a capital election outright [R1] [REG-R39]. **There is no
*Kapitalwahlrecht*** — the policyholder has no election at *Rentenbeginn*. **There is no
*Teilkapitalauszahlung* either**: a Riester contract may pay up to **30 %** of the capital as a lump
sum at the start of the payout phase [R23] [REG-R43] [unverified]; a Schicht-3 contract may pay
100 %; a Basisrente may pay **nothing**. A third absence follows: **the § 20 Abs. 1 Nr. 6 EStG regime
never engages** — the *Unterschiedsbetrag* and the 12/62 rule [REG-R45] are Schicht-3 mechanics that
reach a Basisrente at no point in its life.

**The *Kleinbetragsrente* is the one de-minimis exception the ban carries, and Schicht 1 has it.**
For a **Riester** contract § 93 Abs. 3 EStG permits **commutation of a *Kleinbetragsrente*** at the
start of the payout phase without loss of the subsidy, where the monthly annuity would fall below a
threshold expressed as a percentage of the monthly *Bezugsgröße* of § 18 SGB IV [R23] [REG-R42]
[unverified] — a de-minimis rule that exists because administering a trivially small lifelong annuity
costs more than it pays. **Schicht 1 is not excluded from it.** The *Kapitalisierungsverbot* of
§ 10 Abs. 1 Nr. 2 Buchst. b EStG is qualified by **§ 10 Abs. 1 Nr. 2 Satz 3 EStG**, which makes an
*Abfindung* of a *Kleinbetragsrente* out of a *Basisrentenvertrag* — on the § 93 Abs. 3 Satz 2 and 3
EStG mechanics — harmless to the contract's Schicht-1 status, so a certified tariff may pay one at the
start of the payout phase without forfeiting relief; since the *Wachstumschancengesetz* the relief
reaches, in addition, an annuity pushed below the threshold **during** the payout phase by a
*Versorgungsausgleich* [R1] [REG-R42] [unverified]. **Both the Satz numbering and the amending statute
are [unverified]** — no search corroborated either — and the threshold's level is contested in the
same way it is for Riester: 1 % of the monthly *Bezugsgröße* against 1,5 % [REG-R42] [unverified].
An earlier reading of this product asserted the opposite, that Schicht 1 admitted no de-minimis
exception whatever; that reading is withdrawn and this section is the correction. It follows that
**"a Basisrente entitlement of two euros a month is paid as two euros a month, for life" is wrong as a
statement of law**, though it remains true of contracts whose AVB offers no *Abfindung*.

The rest of what the market does is [unverified] throughout: **minimum premiums**; **minimum annuity
thresholds in the AVB**, below which the insurer may pay quarterly or annually rather than monthly,
whose compatibility with the statutory requirement of a *monatliche* annuity **was not established**
(gap 19); and **consolidation** before *Rentenbeginn*, which depends on the unresolved transfer
question (gap 13).

**The modelling consequence is a decision rather than a deduction, and is [std].** The reference
implementation **does not implement the commutation branch**: at *Rentenbeginn* every model point,
model point 10 included, converts its whole capital into an annuity. Three reasons, in order of
weight. The threshold level is contested and no Basisrente-specific figure was established, so a
commutation test would turn on an invented number. **Whether any German Basisrente AVB actually
offers the *Abfindung*, and whether it is the insurer's election or the policyholder's, was not
established at any carrier** (gap 19) — and the *Abfindung* is a contract term, not an automatic
statutory consequence. And the mechanic is already carried once in this library, on `Riester_DE_A`,
where the § 93 Abs. 3 threshold is native, is computed rather than assumed, and a model point trips
it. **This is a named model risk, not a claim about the law**: a Basisrente model asked to value a
book of very small contracts needs the branch, and a delib user adding it should take
`Riester_DE_A`'s `is_kleinbetrag()` / `commutation_pp()` pair as the pattern. Model point 10 — 300,00 €
a year, the market's minimum recurring premium — is the boundary case that would trip it, and in the
base run it projects a small annuity.

### Pfändungsschutz, insolvency and means-testing

The rule: § 851c Abs. 1 ZPO makes claims to benefits attachable **only as earnings from employment**
where all of the following hold — the benefit is granted at **regular intervals, for life, and not
before the completion of the 60th year of age**, or only on *Berufsunfähigkeit*; the claims **may not
be disposed of**; the **designation of third parties other than survivors as beneficiaries is
excluded**; and **no capital payment other than on death has been agreed** [R12] [REG-R40].
§ 851c Abs. 2 protects amounts saved under such a contract, subject to annual limits and an
**aggregate ceiling of 340 000 €** [REG-R40] [unverified].

**The four requirements of § 851c Abs. 1 are the same four features § 10 Abs. 1 Nr. 2 Buchst. b
demands** — three instruments, one product description. Two cautions: the **age condition in § 851c
is 60, not 62** (gap 10); and **the annual savings allowances are contradicted across summaries** — a
two-band 6 000 € / 7 000 € ladder reported as current law since 1 January 2022 against a
2 000 € – 9 000 € age-graded ladder reported as pre-2022 [REG-R40] — so this document states the
**shape** and **prints no annual band** (gap 9). **§ 12 SGB II and § 90 SGB XII** exempt from
means-testing old-age provision whose realisation is contractually excluded [R13]; taken with § 851c
that is the market's *insolvenzfest* and *Hartz-IV-fest* claim, and the principal non-tax reason a
self-employed person buys the product. All three addresses are [unverified]; the **direction** is not
in doubt.

---

## Riders and options

**In scope and parameterized in the model, off in the base run.**
***Hinterbliebenenabsicherung* (survivor's annuity)**: the permitted beneficiaries are closed to the
**spouse or registered partner** and to **children while *Kindergeld* or the *Kinderfreibetrag* runs**
— in practice to the 18th year, or the 25th while in education [R1] [unverified] on the ages. And
**everything paid to a survivor must be paid as an annuity** [R1], which converts the two familiar
German death-benefit designs into something different:

| Design | In Schicht 3 | In Schicht 1 |
|---|---|---|
| ***Beitragsrückgewähr*** in the *Aufschubphase* | Premiums paid, or the *Deckungskapital*, returned as a **lump sum** to any named beneficiary | The same amount must **buy a survivor's annuity** for an eligible survivor; with no eligible survivor, **nothing is paid** |
| ***Rentengarantiezeit*** in the *Rentenphase* | Remaining instalments continue to any named beneficiary, often commutable | Remaining instalments continue **only to an eligible survivor**, and are **not commutable**; with none, payments cease |
| **Spouse's / survivor's annuity** | An optional rider on a freely chosen life | The **natural** form here, because it is the only form that fits the channel |

**The consequence for a model is a conditional probability, not a benefit.** The value of any
*Hinterbliebenenschutz* is the value of the benefit **multiplied by the probability that an eligible
survivor exists at the moment of death**. On a contract taken at 45 and running to 67 the child
channel has usually closed long before *Rentenbeginn*, so in practice the cover is a spouse cover.
That probability is **[std]** with no evidence behind it and is one of the more consequential **[std]**
choices in the whole delib library. **The cover also costs annuity**: the sibling delib corpus's
Schicht-3 illustration put a 10-year *Rentengarantiezeit* at roughly **0,5 %** of the annuity, 20
years at **2,6 %** and 30 years at **8,0 %** — [unverified], **Schicht-3 figures, not transferable**,
and **no Basisrente-specific cost was established**. The composite carries the *Rentenfaktor*
reduction as a **[std]** table keyed by the option, anchored on those figures.

***Rentengarantiezeit*** is a guaranteed payment period measured from *Rentenbeginn*, representative
values 0, 10 or 20 years, payable only to an eligible survivor and never commutable [R1].

***Berufsunfähigkeits-Zusatzversicherung* (BUZ), and the 50 % rule.** § 10 Abs. 1 Nr. 2 Buchst. b
permits, inside the same contract, cover against *Berufsunfähigkeit* and against *verminderte
Erwerbsfähigkeit* [R1] [REG-R29], and the premium for it is deductible **inside the Schicht-1
*Höchstbetrag*** at 100 % [R2] [R7]. **The 50 % rule**: the contributions qualify only if **more than
half of the total contribution is attributable to the old-age provision**, so the supplementary covers
together must stay **below 50 %** of the total [R1] [unverified] as to the statutory address, settled
as substance. Hence **a standalone Basisrenten-BU does not exist**, the rule **caps the achievable
disability annuity** for a given total premium — exactly the legislator's intention — and it is a
**hard constraint on a model point**, `buz_prem_share < 0.50` being an invariant the test module
asserts.

**Why anyone does this, and what it costs.** The premium for a *selbständige
Berufsunfähigkeitsversicherung* (delib product 9) falls into *sonstige Vorsorgeaufwendungen* under
§ 10 Abs. 1 Nr. 3a EStG, whose small ceiling is in practice already exhausted by health and
long-term-care contributions, so it is **effectively not deductible at all**; the same cover as a BUZ
is deductible in full inside a much larger ceiling. **The counterweight is the tax on the benefit**: a
*BU-Rente* from a *Basisrentenvertrag* is taxed with the **full cohort *Besteuerungsanteil***
[R4] [REG-R41], not at the *Ertragsanteil* of the *abgekürzte Leibrente* from a standalone SBU
[unverified] (gap 16). **The buyer is trading relief now for a heavily taxed benefit later, at a
moment — disability — when income has collapsed and the marginal rate may be low.** That is the whole
of the BUZ-versus-SBU argument, stated here as a trade rather than an advantage. Further constraints,
[unverified] in every particular: the cover ends at the latest at the main contract's *Rentenbeginn*;
the *BU-Rente* is itself subject to the non-capitalisation rule; a premium waiver is the normal
companion cover. **No carrier's BUZ wording was reached** [S5] (gap 18).

***Beitragsdynamik*** and ***Zuzahlung*** are contractual options rather than riders and are **on** in
the base run, because they are the shape of the product's premium.

**Out of scope.** Everything a Schicht-3 or Riester contract offers and this one may not: the
*Kapitalwahlrecht*, the *Teilkapitalauszahlung*, the policy loan, assignment, the secondary-market
sale, and any death lump sum. These are not switched-off options; they are **structural absences**,
and the model carries no cells for them. **The *Kleinbetragsrenten-Abfindung* is deliberately not in
that list**: Schicht 1 has it [REG-R42], and its absence from the model is a **[std]** decision
recorded in `model.md` rather than a prohibition. It is the one absence in this model that German law
does not compel, and it is labelled that way everywhere it appears.

---

## Variations across insurers

**An honest variations table for this product is almost entirely a record of what could not be
compared.** Two carriers produced any artefact at all and neither produced a term; presenting a rich
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
what a tariff family looks like when *klassisch*, *fondsgebunden* and vintage editions coexist.
**Everything else a variations table would normally carry has no observation at all**: entry ages,
minimum premiums, maximum *Zuzahlung*, permitted *Rentenbeginn* range, *Rentengarantiezeit* durations,
survivor-cover forms, BUZ terms, *Effektivkosten*, guarantee levels beyond one carrier,
*Mindestversicherungsleistung*, fund universes. Twenty named German life writers whose Basisrente
documents exist were not reached and **not one contributes a single fact** [S11] (gap 1). They are
named so a checker knows where to go, with nothing attached beyond what each is named for: **Alte
Leipziger** (*AL_RoyalBasisRente*, repeatedly at the top of independent ratings) [S4] [R24];
**NÜRNBERGER** (a principal *Berufsunfähigkeit* writer, and so the natural place to look for a **BUZ
written inside a Basisrente** — **the single most valuable document this corpus could not reach**)
[S5]; **Volkswohl Bund** [S6]; **LV 1871** (the best-known ***fondsgebundene* Basisrente with an open
fund and ETF universe and no *Beitragsgarantie***) [S7] [unverified]; **Swiss Life** [S8];
**Continentale** [S9]; **Stuttgarter** (whose *index-safe* naming, if right, would be an
**index-linked Basisrente**; gap 12) [S10]; and the carriers of [S11], for which **nothing whatever**
was established.

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
and the *Besteuerungsanteil* cohort table are **statutory** [R1] [R4] [R8] [R23] [REG-R39] [REG-R41],
and no carrier can vary them and remain certified. That is unusual in this repository: elsewhere a
delib composite argues a representative choice against an observed spread, whereas here **the
product's defining features are the ones no insurer may choose**, and the **[std]** parameters are
confined to levels — charges, the *Rentenfaktor*, the surplus path, the behavioural rates.

---

## Regulatory context

**Tax — the layer.** The *Alterseinkünftegesetz* of 2004, effective **1 January 2005**, built the
three-layer architecture, introduced ***nachgelagerte Besteuerung*** for the first layer and created
the Basisrente so that the self-employed — who have no access to the statutory scheme — would have a
vehicle with the same tax treatment [R5] [REG-R38]. It responded to a *Bundesverfassungsgericht*
decision on the unequal taxation of *Beamtenpensionen* and statutory pensions [unverified] as to the
year and the case, and followed the report of the commission chaired by **Bert Rürup**. **No
*Bundesgesetzblatt* citation is given for the AltEinkG, the *Wachstumschancengesetz* [R6], the
*Jahressteuergesetz 2022* [R7] or the *Jahressteuergesetz 2007* [R8], because none could be
confirmed** (gap 23).

**Tax — the two amendments that softened the transition.** The *Jahressteuergesetz 2022* brought
**100 % deductibility** forward from 2025 to the assessment period **2023** [R7]; the
*Wachstumschancengesetz* of 2024 cut the annual step in the *Besteuerungsanteil* from one percentage
point to **half a point**, retrospectively for the **2023** cohort — which is why 2023 is 82,5 % and
not 83 % — and moved the 100 % year from **2040 to 2058** [R6] [REG-R41]. Both answered the
***Doppelbesteuerung*** litigation: two Bundesfinanzhof decisions of 19 May 2021, commonly cited as
**X R 33/19** and **X R 20/19** [unverified] as to both file numbers, which accepted **in principle**
that double taxation is unconstitutional where contributions were made from taxed income and benefits
taxed again, found none on the facts, but identified the transition schedule as capable of producing
one for later cohorts — **particularly for self-employed taxpayers whose phase-in contributions were
only partly deductible**, precisely this product's own buyer [R19]. **It is a slowing of the
transition, not a change of principle.**

**Tax — the remaining pieces, none of them a liability cash flow.** A *Hinterbliebenenrente* is taxed
in the survivor's hands on the same cohort basis, with the cohort year determined by the start of that
annuity — **not established** (gap 20). A private annuity is not a *Versorgungsbezug*, so a pensioner
compulsorily insured in the *Krankenversicherung der Rentner* is generally not subject to health and
long-term-care contributions on it while a **voluntarily insured** pensioner pays [R13] [REG-R46]
[unverified] (gap 21) — a difference of the order of **18 % of the annuity**.

**Contract law.** The VVG governs throughout [REG-R22], with § 171's *halbzwingende* character meaning
the listed provisions may not be varied to the policyholder's detriment. The operative sections are
**§ 153** (*Überschussbeteiligung*, half-share in the *Bewertungsreserven*) [R15] [REG-R24];
**§§ 165, 168 and 169** (*Beitragsfreistellung*, *Kündigung*, *Rückkaufswert* — the last inoperative
here) [R14] [REG-R28]; **§ 163** [REG-R27]; **§§ 154 and 155** [REG-R25]; **§§ 8 and 152**
(*Widerruf*) [REG-R23]; **§§ 19, 37, 38, 157 and 158** [REG-R30]; and **§§ 172–177** for a BUZ
[REG-R29]. Certified contracts carry an **annual statement** under § 7a AltZertG [S15] [unverified]
as to the paragraph, whose interest for delib is that it names side by side the state variables a
projection model must carry — contributions paid in the year, accumulated value, guaranteed benefit
and projected annuity. **The field list was not established.**

**Prudential.** The insurer is a Solvency II undertaking supervised under the VAG [REG-R5] [REG-R6],
writing in the *Lebensversicherung* Sparte, with the *Sicherungsvermögen* and the prudent-person
principle of § 124 VAG governing the assets [REG-R7]. Premium calculation runs under § 138 VAG
[REG-R8]; the *Überschussbeteiligung* and the *Sicherungsbedarf* test under § 139 VAG [REG-R9]; the
*RfB* under §§ 140 and 145 VAG with the MindZV and the RfBV beneath [REG-R10] [REG-R18] [REG-R19].
The statutory *Deckungsrückstellung* runs on the DeckRV [REG-R14] [REG-R16] [REG-R17] and the HGB
accounts on §§ 341–341o HGB and the RechVersV [REG-R54]; the *Zinszusatzreserve* exists in no other
jurisdiction in this repository and is an **HGB** reserve. **AnlV investment quotas do not bind this
insurer** — since 1 January 2016 they reach only small undertakings and domestic Pensionskassen and
Pensionsfonds [REG-R7].

**Conduct and disclosure.** The § 7 AltZertG *Produktinformationsblatt* with its individually computed
*Effektivkosten* [R11] [REG-R43] sits on top of the VVG-InfoV product-level regime [REG-R31]; PRIIPs
reaches the unit-linked and hybrid forms [REG-R32]; the IDD and § 34d GewO govern the distribution
this product depends on [REG-R33]. **A Basisrente is squarely inside BaFin's conduct-supervision
perimeter** for capital-forming life products sold through commissioned intermediaries [R21]
[REG-R35], and **nothing Basisrente-specific was established from BaFin** (gap 15).

**Actuarial, professional, and comparative.** The *Rechnungsgrundlagen erster und zweiter Ordnung*
distinction and the DAV's ownership of the tables are at [REG-R47]; **DAV 2004 R and DAV 2004
R-Bestand** are the annuity bases [R17] [REG-R49], **DAV 1997 I / RI / TI** the *Berufsunfähigkeit*
family a BUZ would need [REG-R50], and Destatis the only freely reusable German mortality series
[REG-R52]. The DAV's *Fachgrundsätze* and its annual *Höchstrechnungszins* recommendation govern the
practice [REG-R56]. IFRS 17 applies to IFRS reporters and this is a direct-participating contract that
would be measured under the variable fee approach [REG-R55]; nothing in this library implements it.
Four houses are the market's standing sources for comparative analysis in this layer — **IVFP**,
**Franke und Bornberg**, **Morgen & Morgen**, **Assekurata** [R24] [REG-R53], the first publishing the
best-known Basisrente rating — but **not one rating, score, ranking or figure was established**, and
no downstream document may invent one.

**Living texts.** The *Höchstrechnungszins* is 1,00 % for 2025 and recommended at 1,00 % for 2026
[R16]; the *Besteuerungsanteil* for a 2026 cohort is 84,0 % [unverified]; the *Höchstbetrag* for 2026
is 30 826 € [unverified]; the deductible share has been 100 % since 2023; the full-taxation year is
2058. **Every one of those moves** — the *Höchstbetrag* annually with the
*Sozialversicherungsrechengrößen-Verordnung* [R20], the *Besteuerungsanteil* annually by construction.
Check both, and every paragraph number in this document, before relying on anything here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-basisrente-r1
[R10]: #delib-basisrente-r10
[R11]: #delib-basisrente-r11
[R12]: #delib-basisrente-r12
[R13]: #delib-basisrente-r13
[R14]: #delib-basisrente-r14
[R15]: #delib-basisrente-r15
[R16]: #delib-basisrente-r16
[R17]: #delib-basisrente-r17
[R18]: #delib-basisrente-r18
[R19]: #delib-basisrente-r19
[R2]: #delib-basisrente-r2
[R20]: #delib-basisrente-r20
[R21]: #delib-basisrente-r21
[R22]: #delib-basisrente-r22
[R23]: #delib-basisrente-r23
[R24]: #delib-basisrente-r24
[R3]: #delib-basisrente-r3
[R4]: #delib-basisrente-r4
[R5]: #delib-basisrente-r5
[R6]: #delib-basisrente-r6
[R7]: #delib-basisrente-r7
[R8]: #delib-basisrente-r8
[R9]: #delib-basisrente-r9
[REG-R10]: #delib-reg-r10
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R20]: #delib-reg-r20
[REG-R22]: #delib-reg-r22
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R30]: #delib-reg-r30
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R38]: #delib-reg-r38
[REG-R39]: #delib-reg-r39
[REG-R40]: #delib-reg-r40
[REG-R41]: #delib-reg-r41
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R44]: #delib-reg-r44
[REG-R45]: #delib-reg-r45
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R50]: #delib-reg-r50
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R7]: #delib-reg-r7
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
