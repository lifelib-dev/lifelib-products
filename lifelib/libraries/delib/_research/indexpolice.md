# Indexgebundene Rentenversicherung (*Indexpolice*, "Neue Klassik") — research notes (Germany)

Research notes for the German individual *indexgebundene Rentenversicherung* — the deferred private
annuity, marketed as an *Indexpolice*, in which the accumulated capital sits in the insurer's
*Sicherungsvermögen* (the general-account cover pool) under a guarantee, and the annually declared
*Überschuss* (surplus) is **not credited as interest** but spent as an **option budget** buying a
one-year participation in a share index. The participation is bounded above by a **Cap** on each
month's index return or by a **Partizipationsquote** on the year's return; the capped monthly
returns are **summed** over the *Indexjahr*, with negative months entering **in full and uncapped**;
the year's credit can never be negative; whatever is credited is **locked in** (*Ratchet*,
*Höchststandsicherung*); and the policyholder holds an **annual Wahlrecht** to switch between
*Indexbeteiligung* and *sichere Verzinsung* for the coming year.

**In scope.** The individual, privately written *aufgeschobene Rentenversicherung* of *Schicht 3*
whose *Überschussverwendung* is an index participation: single life, level *Beitrag* over a
*Beitragszahlungsdauer*, capital held in the general account and not in an *Anlagestock*, a
*Beitragsgarantie* or guaranteed capital falling due at *Rentenbeginn*, conversion into a lifelong
*Leibrente* at a *Rentenfaktor*, with a *Kapitalwahlrecht*. The same index module is written on the
*Basisrente* and *Riester* chassis and, in the market, on *Direktversicherung*; those wrappers are
named here only where the wrapper changes the index mechanics (it changes the guarantee level, and
that matters).

**Out of scope, and said so where it matters.**
- The *fondsgebundene Rentenversicherung* (delib product 3) is a genuinely unit-linked contract:
  the policyholder's money buys fund units in an *Anlagestock*, the *Rückkaufswert* is a *Zeitwert*
  of units, and the investment risk sits with the policyholder. **An Indexpolice is not that**, and
  the single most common misunderstanding of the product is to treat it as one.
- The *klassische Rentenversicherung* (product 2) is the same chassis with the surplus credited as
  interest. This file treats product 2's accumulation phase, *Rentenfaktor* and *Rentenphase* as
  the inherited chassis and documents only the delta.
- Structured retail products with the same payoff shape sold outside an insurance wrapper
  (*Indexzertifikate*, *Aktienanleihen*, *Bonuszertifikate*) are outside the library.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung*, *private
  Krankenversicherung* and *Sterbegeldversicherung* are outside the delib library entirely.
- Austrian and Swiss index products are excluded: the VVG, the DeckRV, the MindZV and the AltZertG
  do not apply to them.

These notes are the **citation ground truth** for the delib `indexpolice` product documents
(`product-spec.md`, `technical-notes.md`, `model.md`, `sources.md`). Source ids **S1..S16** and
**R1..R22** below are **frozen — never renumber**; unused ids are simply omitted downstream, leaving
gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this before reading anything else in the file, because it changes what every citation below
means.

**No document in this file was retrieved.** Direct HTTP egress from this build environment is
blocked by an organisation network policy: `WebFetch` and `curl` are refused with HTTP 403 at the
egress gateway for every host outside a short package-registry allowlist. The hosts that matter for
this product were tried and refused: `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de`, `de.wikipedia.org`. No
*Bedingungswerk*, no *Produktinformationsblatt*, no *Basisinformationsblatt*, no statutory text, no
BaFin *Merkblatt* and no index rulebook was opened.

**The session's `WebSearch` budget was exhausted before this product was researched.** The library
shares a hard cap of 200 search calls; the cap had been reached during the regulatory and
contract-law research and during products 1 and 2. Every search attempted for this product returned
the budget-exhausted message. **This file therefore had no research channel at all**: it was written
from the author's own knowledge of German insurance law, German life-insurance product design and
German market practice, disciplined by the rules below.

What that means for every claim here:

1. **Source entries are known references, not evidence.** Each `S#` and `R#` below names a document
   that exists and is the right kind of document for this product — an insurer's *Allgemeine
   Versicherungsbedingungen*, a *Produktinformationsblatt*, a PRIIP *Basisinformationsblatt*, a
   statutory instrument, a supervisory *Merkblatt*. The entry records publisher and document type,
   says `URL: not established` unless the canonical form is one this author is confident of, and
   records `Retrieved: no — direct HTTP egress blocked; no search corroboration (session search
   budget exhausted)`. **No document number, edition date, page count or publication date is
   asserted anywhere in this file**, because none could be established, and none is guessed.
2. **No verbatim quotation appears anywhere in this file.** Where German contractual or statutory
   wording is described, it is described in this author's own words as *what the instrument
   provides*. There is no sentence in quotation marks attributed to any *Bedingungswerk*, statute or
   supervisory document, because there is no summary and no retrieval to attribute one to. This is
   the sharpest difference from `frlib/_research/temporaire-deces.md`, where the PDFs were
   downloaded and read, and from the two sibling delib files, where search summaries reproduced
   German sentences.
3. **`[unverified]` is used generously and means what it always means.** Every specific paragraph
   number, effective date, monetary amount, percentage, cap level, participation rate, product name
   and market figure in this file is tagged `[unverified]` unless it is a structural fact of the
   product that is not in dispute. The general shape of a well-established mechanic — that surplus
   finances an option, that monthly returns are capped and summed, that the year cannot end
   negative — is *not* tagged, because tagging it would drown the signal. The moment a claim becomes
   specific and numeric, it is tagged.
4. **Uncertain numbers become `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — the Cap, the *Partizipationsquote*, the *Beitragsgarantie* percentage, the
   *Rentenfaktor*, the charge levels, the lapse rate — the file states a `[std]` value with a
   rationale and, where one can be argued, a plausible range. **A `[std]` number is honest; a
   fabricated `[S4]` number is not.** The delib product specification and technical notes for
   `indexpolice` are expected to carry a higher proportion of `[std]` parameters than any other
   product in the library, and section 22 and the gaps register say exactly which.
5. **Product names are the weakest class of claim in this file.** Where a carrier's index product is
   named below, the name is recalled from general knowledge of the German market and is tagged
   `[unverified]`. Gap 2 records this as the file's largest single defect. **A downstream document
   must not present any product name in this file as established.**

The consequence, stated plainly: a delib `indexpolice` citation is a **pointer, not a certificate**.
It names the instrument a claim should be checked against. It does not assert that anyone checked
it. Where this file is more confident than that, it says so in the sentence itself.

**What the file is nevertheless worth.** The mechanics of an *Indexpolice* are not in doubt and do
not depend on having a PDF open: the financing identity between the declared surplus and the option
budget, the sum-of-capped-monthly-returns payoff with uncapped negative months, the zero floor, the
annual lock-in, the annual *Wahlrecht*, and the way each of those lands in a cash-flow projection.
The weight of this file is deliberately placed in the extracted-facts-by-mechanic sections and in
the two constructed worked examples, which is where a research file written under these conditions
earns its place.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on, over and above the vocabulary inherited from products 1 and 2:

| Term | Gloss |
|---|---|
| *Indexpolice*, *Indexrente*, *indexgebundene Rentenversicherung* | The market's names for this product: a general-account annuity whose surplus buys an index participation |
| *Indexbeteiligung*, *Indexpartizipation* | Index participation: the form of *Überschussverwendung* in which the year's surplus is spent on an index-linked payoff |
| *Sichere Verzinsung*, *klassische Verzinsung*, *Zinsvariante* | The alternative use of the same surplus: credit it as interest to the *Deckungskapital*, guaranteed once credited |
| *Wahlrecht*, *Umschichtungsrecht*, *jährliches Wechselrecht* | The policyholder's annual right to elect between the two, for the coming *Indexjahr* |
| *Indexjahr* | The twelve-month observation period over which the index participation is measured |
| *Indexstichtag*, *Beobachtungstag*, *Bewertungstag* | The date at which the index level is read — one at the start of the *Indexjahr* and one per month |
| *Cap*, *Höchstgrenze*, *Obergrenze der monatlichen Indexveränderung* | The ceiling applied to each month's index return before the twelve are summed |
| *Partizipationsquote*, *Partizipationsrate*, *Indexquote* | The alternative design: a fixed fraction of the year's index movement, without a monthly cap |
| *Indexrendite*, *Indexbeteiligungssatz* | The rate resulting from the payoff formula, applied to the participating capital |
| *Höchststandsicherung*, *Lock-in*, *jährliche Sicherung*, *Ratchet* | The rule that a credited index amount is permanently added and can never be lost |
| *Optionsbudget*, *Risikobudget* | The insurer's internal name for the amount of surplus spent on the option package |
| *Sicherungsvermögen* | The ring-fenced cover pool backing the insurer's guaranteed obligations; the general account |
| *Anlagestock* | The separate unit-linked asset pool of a *fondsgebundene* contract — what an Indexpolice does **not** use |
| *Neue Klassik* | Post-2013 conventional designs with a modified guarantee: the guarantee is due at *Rentenbeginn* rather than accruing year by year |
| *Beitragsgarantie*, *Beitragserhalt*, *Garantieniveau* | The guarantee expressed as a percentage of premiums paid, due at *Rentenbeginn* |
| *Garantiekapital*, *garantiertes Kapital zu Rentenbeginn* | The guaranteed capital at the end of the accumulation phase |
| *Rechnungszins*, *Höchstrechnungszins* | The technical interest rate the guarantee is priced and reserved on / its statutory maximum |
| *Überschussbeteiligung*, *Überschussanteile* | The statutory entitlement to a share of surplus / the amounts allocated to one contract |
| *Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss* | Interest, mortality and expense surplus |
| *Schlussüberschussanteil*, *Bewertungsreserven* | Terminal bonus / unrealised gains, shared under § 153 Abs. 3 VVG |
| *Deckungskapital*, *Deckungsrückstellung* | The contract's actuarial reserve / the balance-sheet provision |
| *Rentenfaktor* | Monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *Rentenbeginn*, *Aufschubphase*, *Rentenphase* | Annuity commencement / accumulation phase / payout phase |
| *Kapitalwahlrecht* | The right to take a lump sum instead of the annuity |
| *Rückkaufswert*, *Stornoabzug*, *Beitragsfreistellung* | Surrender value / the deduction from it / making the contract paid-up |
| *Ersatzindex*, *Indexanpassung* | The replacement index, and the clause permitting the substitution |
| *Treuhänder*, *Treuhänderklausel* | The independent trustee whose approval some contractual adjustments require |
| *Billiges Ermessen* | Reasonable discretion, § 315 BGB: the standard against which a discretionary determination such as a Cap is reviewable |
| *Preisindex*, *Kursindex* / *Performanceindex* | Price index (dividends excluded) / total-return index (dividends reinvested) — the distinction that decides how much of the equity return reaches the policyholder |
| *Multi-Asset-Index*, *Volatilitätssteuerung*, *Excess-Return-Index* | The house index families that replaced the EURO STOXX 50 in many tariffs |
| *Chancen-Risiko-Klasse* (CRK) | The 1-to-5 risk class assigned to certified *Basisrente* and *Riester* products by the *Produktinformationsstelle Altersvorsorge* |
| *Basisinformationsblatt* (PRIIP-KID), *Produktinformationsblatt* (PIB) | The EU key information document / the German pre-contractual product summary |
| *Standmitteilung* | The annual statement to the policyholder; the document in which an *Indexjahr* result is reported |

---

## Primary sources

Every entry below carries the same retrieval status, stated once here rather than repeated sixteen
times: **Retrieved: no — direct HTTP egress blocked in the build environment; no search
corroboration, the session's `WebSearch` budget having been exhausted before this product was
researched.** Each entry is therefore a **known reference**: a document that exists and is the right
kind of document, named so that a later reader with a working network can go and check the claims
this file attaches to it. No entry asserts an edition, a document number, a page count or a
publication date. Where the `Content` block records what the document establishes, it is recording
what a document of that kind **contains and would settle** — written from knowledge of the product,
not from the document — and every specific number inside it carries `[unverified]`.

### S1 — GDV, *Musterbedingungen* for the *Rentenversicherung mit aufgeschobener Rentenzahlung*
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: *Musterbedingungen* — model AVB published by the industry association for members to
  adopt, adapt or ignore. They are not binding and are not a regulation.
- URL: not established. (The GDV *Musterbedingungen* index is a service page on `gdv.de`, which
  refused the fetch.)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted).
- Content — the chassis, and a finding about what is *not* in it:
  - The GDV model wording for the deferred annuity supplies the clause skeleton every German
    deferred annuity shares and which the Indexpolice inherits unchanged: the *Erlebensfall*
    obligation at *Rentenbeginn*, the *Todesfallleistung* in the *Aufschubphase*, the
    *Überschussbeteiligung* clause, *Rückkaufswert* and *Beitragsfreistellung*, the *Rentenphase*
    clauses including *Rentengarantiezeit*, the duty of disclosure, and *Selbsttötung*.
  - **The GDV publishes no *Musterbedingungen* for an index participation module.** The
    *Indexbeteiligung* clause set is a carrier-specific construction throughout the market. This is
    the structural reason why the wording varies more across insurers for this product than for any
    other in the delib library, and why an "industry standard" formulation of the Cap mechanic does
    not exist to be cited. `[unverified]` as to whether some later GDV model set has added one;
    nothing in this author's knowledge indicates it has.
  - Consequence for delib: the *Indexbeteiligung* clauses in the delib product specification are a
    **composite** reconstructed from the market-wide mechanics in the extracted-facts sections
    below, and are labelled as such, not attributed to any carrier.

### S2 — Allianz Lebensversicherungs-AG, *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: AVB / *Bedingungswerk* for a deferred annuity tariff with *Indexbeteiligung*
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content — the single most important missing document in this file:
  - Allianz **IndexSelect** `[unverified]` is, on this author's knowledge, the German market's
    flagship *Indexpolice* and the design most other carriers were measured against. It is written
    on the *Schicht 3* deferred-annuity chassis and, in the market, also on the *Basisrente* and
    *Direktversicherung* chassis under variant names `[unverified]`.
  - The AVB is the document that would settle, for one carrier and with authority, every one of the
    following: the definition of the *Indexjahr* and its start date; the definition of the monthly
    *Indexveränderung* and the observation dates; the exact payoff formula (summation of capped
    monthly changes, negative months in full, floor at zero); the base to which the resulting rate
    is applied; the timing and notice period of the annual *Wahlrecht*; who determines the Cap, on
    what standard and by when it is announced; whether a *Mindest-Cap* is guaranteed; the *Lock-in*
    clause; and the *Ersatzindex* clause.
  - **None of that is established from the document.** Every statement about it in this file's
    mechanics sections is written from knowledge of the design family, not from this AVB, and the
    numeric parts are `[unverified]` or `[std]`.
  - Gap 1 and gap 2 record this.

### S3 — Allianz Lebensversicherungs-AG, *Produktinformationsblatt* / IPID for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: *Produktinformationsblatt* (the German pre-contractual product summary required by
  VVG-InfoV, in the market also labelled with the EU IDD term **IPID**)
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: a document of this class is the shortest route to the product's commercial envelope —
  minimum and maximum *Eintrittsalter*, minimum *Beitrag*, minimum and maximum *Aufschubdauer*,
  available *Garantieniveaus*, the *Rentenfaktor* guarantee, and the headline description of the
  index mechanic in consumer language. **No instance was located**; every one of those parameters
  is `[std]` in delib. Gap 5.

### S4 — Allianz Lebensversicherungs-AG, *Basisinformationsblatt* (PRIIP-KID) for **Allianz IndexSelect**
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: *Basisinformationsblatt* under Regulation (EU) No 1286/2014 [R10] — three pages, fixed
  structure, with four performance scenarios and the full cost table including the *Reduktion der
  Wertentwicklung* (reduction in yield)
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: this is the **only public document class that puts a number on the cost of a German
  Indexpolice** and on its modelled return distribution. It would supply: the product's PRIIP
  category (an Indexpolice with discretionary profit participation is a **Category 4** product,
  because part of its value depends on factors not observed in the market — the insurer's declared
  surplus — and the DAV has published a *Standardverfahren* for exactly that case [R11]); the
  stress, unfavourable, moderate and favourable scenarios at the recommended holding period; the
  one-off, ongoing and transaction costs; and the RIY. **No instance was located.** Every charge
  level and every return assumption in delib is `[std]`. Gap 6.

### S5 — Allianz Lebensversicherungs-AG, annual customer notification of the *Indexbeteiligung* parameters for the coming *Indexjahr*
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: annual policyholder letter / online customer-portal notice announcing, before the start
  of each *Indexjahr*, the **Cap** (or the *Partizipationsquote*) that will apply and inviting the
  *Wahlrecht* election
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the document class in which the **actual Cap level for a named insurer and a named year**
  lives. It is normally sent to policyholders rather than published, which is why cap levels reach
  the public domain mainly through the trade and consumer press [S16] and the rating houses [R21]
  rather than through insurer documents. **No instance, and no cap value for any insurer in any
  year, was established.** This is the file's second-largest defect after the missing AVB. Gap 3.

### S6 — Allianz Lebensversicherungs-AG, **Allianz Perspektive** documents (the *Neue Klassik* comparator)
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: AVB, *Produktinformationsblatt* and *Basisinformationsblatt* for a *Neue Klassik*
  deferred annuity **without** index participation
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: **Perspektive** `[unverified]` is the reference point for what "Neue Klassik" means
  without the index module: a guarantee that falls due at *Rentenbeginn* rather than accruing as a
  guaranteed annual interest rate on the reserve, permitting a materially riskier asset mix behind
  it. The Indexpolice is the same guarantee architecture with the surplus spent on an option instead
  of credited. Recorded here because the delib product specification must draw exactly that
  distinction and should point at the comparator rather than blur the two.

### S7 — R+V Lebensversicherung AG, AVB and product documents for **R+V-IndexInvest**
- Publisher: R+V Lebensversicherung AG, Wiesbaden
- Doc type: AVB / *Bedingungswerk*, *Produktinformationsblatt* and *Basisinformationsblatt* for a
  deferred annuity with *Indexbeteiligung*
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: R+V is one of the large mutual-sector carriers writing this product, and the product name
  **IndexInvest** `[unverified]` is recalled from general market knowledge. Its documentary value
  would be as the second carrier wording, allowing the *Indexbeteiligung* clause set to be compared
  across two houses — the minimum needed before any statement of the form "the market does X" can be
  made about a clause. **Not established.** Gap 2.

### S8 — Stuttgarter Lebensversicherung a. G., AVB and product documents for **Stuttgarter index-safe**
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB / *Bedingungswerk*, *Produktinformationsblatt* and *Basisinformationsblatt* for a
  deferred annuity with *Indexbeteiligung*
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: Die Stuttgarter is a mid-sized carrier with a long-standing index family, the product
  name **index-safe** `[unverified]`. Its interest for this file is that mid-sized carriers were the
  most active adopters of **house multi-asset indices** in place of the EURO STOXX 50 — the shift
  documented in mechanics section 9 — because a lower-volatility bespoke index buys a higher
  *Partizipationsquote* out of a smaller option budget. **Not established.**

### S9 — Zurich Deutscher Herold Lebensversicherung AG, *Verbraucherinformation* series for konventionelle Rentenversicherungen
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — a long combined document (AVB plus the VVG-InfoV § 1
  pre-contractual information) covering a family of conventional annuity tariffs
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: this series is established as existing by the sibling research file for delib product 2
  (`klassische_rentenversicherung`), where it supplied the *Rentenfaktor* max-of-two rule and the
  surplus-allocation timing. **Whether the series contains an index variant is not established.** It
  is listed here because the *Verbraucherinformation* format — one document combining conditions and
  statutory information — is the most useful single document class for this product after the AVB,
  and because the chassis facts delib `indexpolice` inherits from product 2 trace to it.

### S10 — GDV, *Muster-Standmitteilung* for a *Rentenversicherung*, and carriers' own *Standmitteilungen*
- Publisher: GDV (model), individual carriers (actual)
- Doc type: annual statement of contract status
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the *Standmitteilung* is where an *Indexjahr* result is reported to the policyholder: the
  capital at the start of the *Indexjahr*, the Cap that applied, the resulting *Indexrendite* (or the
  statement that it was zero), the amount credited and locked in, and the resulting guaranteed
  capital. **A real Standmitteilung showing a completed Indexjahr with its twelve monthly index
  movements is the single "gold" document this brief asked for, and none was located.** Gap 4. The
  constructed worked examples in mechanics sections 19 and 20 exist because of this gap and are
  labelled `[std]` throughout.

### S11 — *Produktinformationsblatt* under the AltZertG, with the *Chancen-Risiko-Klasse*, for a *Basisrente* or *Riester* index variant
- Publisher: the certifying carrier; the class assignment by the *Produktinformationsstelle
  Altersvorsorge gGmbH* (PIA)
- Doc type: the standardised *Produktinformationsblatt* prescribed for certified *Altersvorsorge*
  products, carrying the product's **Chancen-Risiko-Klasse** on a scale of 1 to 5 [R12]
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the German market has one standardised, mandatory, comparable, publicly filed product
  disclosure — and it exists only for *Schicht 1* and *Schicht 2* products. For an index variant of
  a *Basisrente* it would supply the effective cost quota, the guaranteed and projected benefits on
  a prescribed set of return assumptions, and the CRK. Index products, having a guarantee and a
  bounded upside, sit at the low end of the CRK scale `[unverified]`. **No instance was located**,
  and this is the most frustrating gap in the file, because the document class is designed to be
  exactly the comparable evidence this research needed. Gap 7.

### S12 — Finanztip, guidance pages on *Indexpolicen* / index-linked annuities
- Publisher: Finanztip Verbraucherinformation gGmbH — **secondary**, not a product document
- Doc type: consumer guidance page
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: Finanztip's editorial position on German life-insurance savings products is
  well-established and consistently sceptical, and it is one of the few German consumer publishers
  that explains the sum-of-capped-monthly-returns mechanic in enough detail for a lay reader to see
  the asymmetry. Its typical argument — that the cap plus the price-index basis plus the charges
  leave a return well short of a direct index investment — is reproduced, as an argument rather than
  as a citation, in mechanics section 21. **Not retrieved**; nothing numeric is taken from it.

### S13 — Stiftung Warentest / *Finanztest*, comparative tests of *Indexpolicen*
- Publisher: Stiftung Warentest — **secondary**
- Doc type: comparative product test with scoring and a cost analysis
- URL: not established (Stiftung Warentest content is largely paywalled in any case).
- Retrieved: no — egress blocked; no search corroboration.
- Content: *Finanztest* is the German market's most authoritative independent comparative tester of
  retail savings insurance and has covered index-linked annuities. A test of this class would supply
  cap levels, cost quotas and modelled outcomes for a named panel of carriers in a named year —
  precisely the evidence gaps 3 and 6 record. **Not retrieved, nothing cited.**

### S14 — Verbraucherzentrale (federal association and Länder consumer centres), pages on *Indexpolicen*
- Publisher: Verbraucherzentrale Bundesverband e. V. and the Länder centres — **secondary**
- Doc type: consumer-advice pages
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the consumer-advice sector's standing criticisms of the product are: that the payoff
  formula is not comprehensible to a normal purchaser; that the Cap is redetermined annually at the
  insurer's discretion so the purchaser cannot know the future terms of their own contract; and that
  a zero year is a real and frequent outcome. These are recorded as **positions**, not as findings,
  in mechanics section 21. **Not retrieved.**

### S15 — Comparison portals: Verivox, Check24
- Publisher: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**
- Doc type: product-comparison and explainer pages
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: portals of this class publish explainer pages on *Indexpolicen* and, for some products,
  indicative premium and benefit quotations. They are the usual public source for the commercial
  envelope (minimum premium, entry ages, term bands) when insurer *Produktinformationsblätter* are
  not reachable. **Not retrieved**; the envelope parameters in section 22 are `[std]`.

### S16 — German insurance trade press: *procontra*, *Versicherungsbote*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft*, *Handelsblatt*
- Publisher: various — **secondary**
- Doc type: trade and financial press reporting
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the trade press is where cap changes, index switches and the withdrawal or repricing of
  index tariffs are reported, and it is the practical route by which cap levels for a named carrier
  and year reach the public record [S5]. It is also where the "Klassik wird zur Nische" narrative
  around the retreat from guaranteed products, and the 2022 collapse of new *Riester* business, were
  documented. **Not retrieved**; every figure that would have come from it is a gap.

---

## Regulatory and actuarial references

Same retrieval status as the primary sources, stated once: **Retrieved: no — direct HTTP egress
blocked; no search corroboration (session search budget exhausted).** Where a URL is given it is the
**canonical form** of the address on `gesetze-im-internet.de`, which this author is confident of for
the German federal codes; every such URL is tagged `[unverified]` because no search returned it and
no fetch confirmed it. Statutory content is described in this author's own words. Every paragraph
number is `[unverified]`.

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Content: the statutory hinge of this product. § 153 Abs. 1 gives the policyholder an entitlement
  to participate in the surplus and in the *Bewertungsreserven* unless participation is excluded by
  agreement. Abs. 2 requires the insurer to allocate the surplus by a **verursachungsorientiertes
  Verfahren** — a causation-oriented procedure — or by another comparable appropriate method agreed
  in the contract. Abs. 3 governs the *Bewertungsreserven*: they are determined annually, allocated
  by a causation-oriented procedure, and half of the amount so determined is paid out on
  termination, subject to a proviso for supervisory rules introduced by the LVRG.
- Why it matters here, and it matters more than for any other delib product: **the index
  participation is a form of *Überschussverwendung*, not a separate investment.** What the
  policyholder is legally entitled to is a share of the insurer's surplus; the AVB then say how that
  share is applied, and this product's AVB say it is applied by buying a bounded index-linked payoff
  for one year. The *Wahlrecht* is therefore an *Überschussverwendungswahlrecht*, and the
  *Indexbeteiligung* has no independent statutory footing — it stands or falls on the contract
  clause. **This is the correct legal characterisation of the product and it is not in doubt.**
  `[unverified]` as to the subsection numbering.
- A consequence a model must respect: because the *Überschuss* is discretionary and may be zero
  [R8][R16], the **option budget may be zero**, in which case the *Indexbeteiligung* for that year
  buys nothing and the year's credit is necessarily zero regardless of what the index does.

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Content: on termination by *Kündigung* the insurer owes the *Rückkaufswert*, computed as the
  *Zeitwert* / the actuarial reserve on recognised actuarial principles; acquisition and
  distribution costs must be spread over **at least the first five years** so that an early
  surrender value cannot be extinguished by front-loaded costs (the *Mindestrückkaufswert*); a
  *Stornoabzug* is permitted only if it is agreed, appropriate and **quantified in the contract**.
- Delta for this product: the *Rückkaufswert* of an Indexpolice is a **general-account reserve**,
  not a unit value. It includes any index credits already locked in, because those have become part
  of the guaranteed capital. It does **not** include an accrued fraction of the current *Indexjahr*:
  a mid-year surrender loses the running year's option payoff entirely, because the payoff is only
  determined at the *Indexjahr* end. Whether the contract instead refunds the unspent option budget
  is a carrier-level clause question and **is not established**. Gap 12.

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Content: the policyholder may at any time demand conversion of the contract to a paid-up
  (*prämienfrei*) contract for the reduced insured benefit computed on recognised actuarial
  principles for the end of the current insurance period; the same *Stornoabzug* discipline applies.
- Delta for this product: a paid-up Indexpolice **keeps its index participation** on the capital
  already accumulated. The *Wahlrecht* survives *Beitragsfreistellung*. `[unverified]` at clause
  level; the general rule follows from the fact that the participation attaches to the capital and
  not to the premium.

### R4 — VVG § 163 (*Anpassung der Prämie*) and § 164 (*Ersetzung von Bedingungen*)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html`, `.../__164.html` `[unverified]`
- Content: § 163 permits an adjustment of the premium, or of the benefit at unchanged premium, for
  life contracts where the calculation bases have changed in a way that is not merely temporary and
  the change was unforeseeable, **with the confirmation of an independent trustee** (*unabhängiger
  Treuhänder*). § 164 permits an ineffective clause to be replaced by a new one, again with the
  trustee's confirmation, where the gap would otherwise not be closable.
- Why it matters here: these are the two statutory channels through which anything about an
  Indexpolice's terms can be changed against the policyholder's will after issue. **The annual
  redetermination of the Cap is not one of them**: the Cap is not an adjustment of the contract, it
  is the exercise of a discretion the contract itself confers, and it is therefore governed by
  § 315 BGB [R22], not by § 163 VVG. Keeping those two apart is the single most important legal
  distinction in this product and downstream documents must not blur it.
- The *Treuhänder* does appear in this product in two other places: the *Ersatzindex* clause, where
  some carriers require trustee confirmation for a substitution `[unverified]`, and the historic
  *Treuhänderklausel* on the *Rentenfaktor*, inherited from product 2.

### R5 — VVG § 154 (*Modellrechnung*) and VVG-InfoV § 2 (pre-contractual information)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__154.html`;
  `https://www.gesetze-im-internet.de/vvg-infov/__2.html` `[unverified]`
- Content: § 154 requires, where the insurer quotes possible benefits beyond the contractually
  agreed ones, a *Modellrechnung* on three prescribed interest assumptions, with a warning that it
  is only a model and that the values are not guaranteed. VVG-InfoV § 2 sets out the catalogue of
  pre-contractual information the insurer must supply, which for life insurance includes the
  benefits and their guarantee status, the surrender and paid-up values, the costs, and — the item
  that matters most for cost transparency — the ***Effektivkosten*** (reduction in yield).
- Why it matters here: a *Modellrechnung* for an Indexpolice is intrinsically awkward, because the
  product's return does not scale linearly with an assumed interest rate: the interest assumption
  drives the **option budget**, which drives the **Cap**, which drives the payoff non-linearly. How
  German carriers discharge § 154 for this product **is not established**. Gap 13.

### R6 — VVG § 161, *Selbsttötung*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` `[unverified]`
- Content: where death is caused by suicide, the insurer is not liable on a death cover within
  **three years** of the conclusion (or reinstatement) of the contract; where the exclusion applies,
  the insurer owes the *Rückkaufswert*.
- Relevance: inherited unchanged from products 1 and 2. It bites only on the death benefit in the
  *Aufschubphase*, which for this product is normally a return of capital rather than a sum at risk,
  so the clause is close to inoperative in economic terms. Recorded so the delib documents can say
  so rather than leave it out.

### R7 — *Deckungsrückstellungsverordnung* (DeckRV): *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Content: the DeckRV caps the technical interest rate used in the *Deckungsrückstellung*, and hence
  in practice the rate a new contract's guarantee may be priced on, and caps the acquisition costs
  that may be zillmerised into the reserve (the *Höchstzillmersatz*, **25 ‰ of the *Beitragssumme***
  `[unverified]`).
- The rate history, **entirely `[unverified]` at the level of individual steps**, as this author
  recalls it: 4,00 % to mid-2000; 3,25 %; 2,75 %; 2,25 %; 1,75 %; 1,25 %; 0,90 %; **0,25 % for
  2022–2024**; **1,00 % from 1 January 2025**. The sibling delib research files establish the
  0,25 % → 1,00 % move and the 1,00 % level for 2025 and 2026 from search evidence; the earlier
  steps are recalled and tagged.
- **Why the rate history is the reason this product exists.** At a *Höchstrechnungszins* of 0,25 %,
  a conventional annuity credits a guaranteed 0,25 % and hands everything above it to the
  policyholder as declared surplus — so the *guaranteed* component of the return is negligible and
  the *discretionary* component is the whole story. An Indexpolice takes that same discretionary
  component and, instead of paying it out as a modest and certain interest credit, converts it into
  a bounded lottery on an equity index. **The product is a direct commercial response to a
  near-zero guaranteed rate**, and the reason it was launched in the mid-2000s and grew through the
  2010s. Correspondingly, the 2025 rise to 1,00 % raises the guaranteed component again and makes
  the *sichere Verzinsung* arm of the *Wahlrecht* relatively more attractive `[unverified]` as to
  whether that has shifted observed elections.

### R8 — *Mindestzuführungsverordnung* (MindZV)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Content: prescribes the minimum share of each source of surplus that must be allocated to the
  policyholders, through the *Rückstellung für Beitragsrückerstattung* (RfB). The shares, as
  established in the sibling delib files: **90 % of the *anzurechnende Kapitalerträge*** after the
  charge for discounting the *Deckungsrückstellung*; **90 % of the *Risikoergebnis***; and **50 % of
  the *übriges Ergebnis***.
- Why it matters here: **this is where the option budget comes from.** The insurer earns a return on
  the *Sicherungsvermögen*; the MindZV forces at least 90 % of the excess over the guarantee into
  the policyholders' share; the insurer declares an *Überschussanteilsatz* out of that; and for a
  contract that has elected *Indexbeteiligung*, that declared amount is spent on options instead of
  credited as interest. **The size of the option budget is therefore bounded by the same investment
  performance and the same statutory minimum that bound a classic contract's declared rate** — an
  Indexpolice does not have a bigger risk budget than a *Klassik* contract of the same vintage, it
  spends the identical budget differently. This is the most under-appreciated fact about the product
  and it belongs in the delib product specification's first page.

### R9 — VAG § 139 (*Überschussbeteiligung*, *Sicherungsbedarf*), § 124 (*Anlagegrundsatz*), and the *Sicherungsvermögen* provisions
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Content: § 139 VAG governs the surplus participation from the supervisory side and contains the
  *Sicherungsbedarf* rule that limits exiting policyholders' share of the *Bewertungsreserven* to
  the excess over the reserve strengthening need on contracts with a high guaranteed rate. § 124
  states the **prudent person** investment principle; the derivative provisions of the same part
  permit derivatives that contribute to a reduction of risk or facilitate efficient portfolio
  management `[unverified]` at section level.
- Why it matters here: the insurer's purchase of index options to back an index-participation
  obligation is the paradigm of a derivative used to **hedge a liability it has itself written** —
  the liability and the hedge are matched by construction, month for month and cap for cap. That is
  the supervisory frame in which the product is written, and it explains an important design fact:
  the insurer does **not** take an equity view on the policyholder's behalf; it buys the exact
  payoff it has promised, and the Cap is set at whatever level makes that purchase cost exactly the
  option budget. Sections 3 and 8 develop this. `[unverified]` at section level; the substance is
  standard practice and is not in doubt.

### R10 — PRIIPs: Regulation (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653
- Publisher: EUR-Lex (the host refused the fetch)
- URL: not established.
- Content: requires a three-page *Basisinformationsblatt* for every packaged retail investment and
  insurance-based investment product, with a prescribed structure: what the product is, the risk
  indicator on a 1-to-7 scale, four performance scenarios (stress, unfavourable, moderate,
  favourable), the costs over time and the composition of costs including the reduction in yield,
  and the recommended holding period. The delegated regulation prescribes the methodology and the
  **product categories** that determine how scenarios are computed.
- Why it matters here: an Indexpolice is a **Category 4** PRIIP — a product whose values depend in
  part on factors not observed in the market, namely the insurer's discretionary surplus
  declaration — rather than a Category 3 derivative-based product `[unverified]` as to the category
  assignment in any specific carrier's KID. The distinction is not academic: Category 4 permits the
  use of the insurer's own model for the discretionary component, which is why two Indexpolicen with
  similar mechanics can publish very different favourable scenarios.

### R11 — DAV, *Ergebnisbericht* of the *Ausschuss Lebensversicherung* on the PRIIP Category 4 *Standardverfahren*
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- URL: not established (`aktuar.de` refused the fetch).
- Content: the German actuarial profession's standard procedure for computing PRIIP performance
  scenarios for Category 4 products — i.e. for exactly the discretionary-surplus component that makes
  an Indexpolice a Category 4 product. Established as existing by the sibling `kapitallebensversicherung`
  research file. **Its content for the index case is not established**, and it is the document a
  serious attempt to model an Indexpolice's disclosed scenarios would have to start from. Gap 14.

### R12 — *Altersvorsorgeverträge-Zertifizierungsgesetz* (AltZertG), and the *Produktinformationsstelle Altersvorsorge*
- Publisher: Gesetze im Internet (statute); Produktinformationsstelle Altersvorsorge gGmbH (the
  classification body)
- URL: `https://www.gesetze-im-internet.de/altzertg/` `[unverified]`
- Content: the AltZertG defines the criteria a *Riester* or *Basisrente* contract must satisfy to be
  certified. For *Riester*, the decisive one is the ***Beitragserhaltungszusage***: the provider must
  guarantee that at the start of the payout phase **at least the contributions paid in (including
  the state allowances) are available** — a **100 % nominal guarantee** `[unverified]` as to the
  subsection. For *Basisrente* there is no equivalent statutory guarantee requirement. The AltZertG
  also mandates the standardised *Produktinformationsblatt* [S11], on which the PIA's
  **Chancen-Risiko-Klasse** (1 to 5) appears.
- Why it matters here, and it is the sharpest single fact in this file about guarantee levels:
  **the guarantee level of an index product is set by its wrapper, not by its index module.** A
  *Schicht 3* Indexpolice may be sold with an 80 % or 90 % *Beitragsgarantie*; a *Riester*
  Indexpolice may not, because 100 % is statutory. That difference is the reason a *Riester* index
  variant has a structurally smaller option budget than a *Schicht 3* one of the same vintage and
  term. It is also the reason the *Riester* market effectively closed to new business when the
  *Höchstrechnungszins* fell to 0,25 % in 2022: at that rate a 100 % nominal guarantee over a normal
  term could not be calculated with room left for costs, let alone for an option budget
  `[unverified]` as to the year and the extent of the withdrawal, though the episode itself is
  well-established market history.

### R13 — EStG § 22 Nr. 1 Satz 3, *Ertragsanteilsbesteuerung* of a *Leibrente*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` `[unverified]`
- Content: a *Leibrente* from a privately funded *Schicht 3* annuity is taxed only on its
  ***Ertragsanteil*** — a fixed percentage of the annuity determined once and for all by the
  annuitant's age at *Rentenbeginn* and set out in a statutory table. Illustrative values from the
  table, all `[unverified]`: about 22 % at age 60, about 20 % at 63, about 18 % at 65, about 17 % at
  67.
- Relevance: identical to product 2. The index mechanic does **not** change the tax treatment of the
  annuity, because the credits have been absorbed into the capital before conversion.

### R14 — EStG § 20 Abs. 1 Nr. 6, taxation of a *Kapitalabfindung*, and the *Mindesttodesfallschutz*
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` `[unverified]`
- Content: where the *Kapitalwahlrecht* is exercised, the difference between the payment and the sum
  of premiums paid is investment income. If the contract has run at least **twelve years** and the
  payment is taken after the policyholder's **62nd** birthday (60th for contracts concluded before
  2012), **only half the difference is taxable** and it is taxed at the personal rate rather than by
  final withholding `[unverified]` on the ages and the year boundary. For contracts concluded from
  **1 April 2009** the favourable treatment additionally requires a minimum death cover
  (*Mindesttodesfallschutz*) — in the standard formulation, a death benefit of at least **50 %** of
  the premiums payable over the term `[unverified]`.
- Relevance and delta: identical to product 2, with one wrinkle worth stating. The *twelve-year /
  age-62* test interacts with the **annual *Wahlrecht***: exercising the *Wahlrecht* is not a change
  of contract and does not restart the twelve-year clock `[unverified]`, but a *Vertragsänderung*
  that materially alters the contract can. Nothing in the corpus settles where the line falls.

### R15 — RechVersV and the VAG *Sparten*: what "indexgebundene Lebensversicherung" means in regulation
- Publisher: Gesetze im Internet (RechVersV, VAG); BaFin (statistical classifications)
- URL: not established.
- Content, and this is a terminological trap that a careless downstream document will fall into:
  in the regulatory and accounting vocabulary, **"Lebensversicherungen, bei denen das Anlagerisiko
  vom Versicherungsnehmer getragen wird"** — the class that contains *fondsgebundene* and
  *indexgebundene* life insurance in the balance-sheet sense — means contracts where the
  **policyholder bears the investment risk**. An *Indexpolice* of the kind this file describes
  **does not belong there**: the capital is in the *Sicherungsvermögen*, the guarantee is the
  insurer's, and the policyholder's downside is limited to forgoing one year's surplus. It is booked
  and reserved as a **conventional profit-participating contract**. In the Solvency II lines of
  business the same distinction appears as *insurance with profit participation* versus
  *index-linked and unit-linked insurance*, and an Indexpolice sits in the former `[unverified]` as
  to the line-of-business numbering.
- Consequence for delib: the market word *indexgebunden* and the regulatory word *indexgebunden*
  denote different things. The delib documents use *Indexpolice* / *Indexbeteiligung* for the
  product and reserve *indexgebunden* in its regulatory sense, and say so.

### R16 — BaFin, *Merkblatt* 01/2023 (VA) on conduct-supervision aspects of capital-forming life insurance products
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin)
- URL: not established (`bafin.de` refused the fetch).
- Content: BaFin's statement of what it expects of the product-governance and value-for-money of
  capital-forming life products — established as existing by the sibling `kapitallebensversicherung`
  research file, where it supported the propositions that *Effektivkosten* differ considerably
  across the market and that BaFin will examine outliers.
- Relevance here: an Indexpolice is squarely within the *Merkblatt*'s scope, and the product raises
  the *Kundennutzen* question in its sharpest form, because a design that returns zero in a
  substantial fraction of years while charging a full acquisition-cost load is exactly the kind of
  product a value-for-money supervision regime exists to interrogate. **Whether the *Merkblatt*
  names index products specifically is not established.** Gap 15.

### R17 — BaFin, *Risiken im Fokus* (annual risk report) and BaFin *Fachartikel* on costs and PRIIPs
- Publisher: BaFin
- URL: not established.
- Content: BaFin's annual statement of supervisory focus risks; the sibling file establishes that
  the cost of capital-forming life insurance is a named focus. The *Fachartikel* series has covered
  how insurers discharge the PRIIPs information duties.
- Relevance: context for the charge discussion in mechanics section 13, where every level is `[std]`.

### R18 — DAV recommendations on the *Höchstrechnungszins*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established.
- Content: the DAV recommends a *Höchstrechnungszins* to the Bundesfinanzministerium, which sets it
  by regulation. The sibling delib files establish the recommendation of **1,0 %** for 2025 and again
  for 2026.
- Relevance: fixes the guarantee basis for a contract issued at the access date, and therefore the
  split between the guaranteed and the discretionary component of the return — which for this
  product is the split between the guaranteed capital and the option budget.

### R19 — GDV statistics: *Die deutsche Lebensversicherung in Zahlen*, and the new-business and in-force series
- Publisher: GDV
- URL: not established.
- Content: the industry association's annual statistics — new business by *Beitragssumme* and APE,
  in-force contracts, *Stornoquote*, and the split of new business across product families.
- Relevance, and a limitation that must be stated: **the GDV product split does not isolate
  Indexpolicen.** They are counted within conventional annuity business, because that is what they
  are [R15]. There is therefore **no published figure for the size of the German index-participation
  segment**, either from GDV or from anywhere else this author knows of. Gap 8.

### R20 — Assekurata, *Marktstudie* on *Überschussbeteiligungen und Garantien*
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH
- URL: not established.
- Content: the annual survey of declared surplus rates and guarantee designs across the German life
  market, established as existing by the sibling delib files, which take from it the 2026 market
  averages for the classic annuity and for *Neue Klassik*.
- Relevance: the declared surplus rate **is** the option budget [R8], so an Assekurata declared-rate
  series is the closest public proxy for the size of the option budget. The sibling file records a
  *Neue Klassik* declared rate of the order of 2,65 % for 2026 and a classic annuity market average
  of the order of 2,62 % `[unverified]` — figures established there by search and reproduced here as
  cross-references, not as findings of this file. Whether Assekurata publishes cap levels as such is
  **not established**.

### R21 — Rating houses on *Indexpolicen*: Institut für Vorsorge und Finanzplanung (IVFP), Franke und Bornberg, Morgen & Morgen
- Publisher: IVFP GmbH; Franke und Bornberg GmbH; MORGEN & MORGEN GmbH
- URL: not established.
- Content: the three German houses that rate retirement-savings products. IVFP in particular
  maintains a rating of index-linked annuities `[unverified]`, and a rating of that kind is the only
  systematic public compilation this author is aware of that puts **cap levels and participation
  rates for a panel of named carriers side by side**.
- Relevance: this is the document class that would have closed gaps 2, 3 and 9 in one go — the
  product-name inventory, the cap levels and the observed parameter ranges. **Nothing from it was
  established.**

### R22 — BGB § 315, *Bestimmung der Leistung durch eine Partei* (*billiges Ermessen*)
- Publisher: Gesetze im Internet
- URL: `https://www.gesetze-im-internet.de/bgb/__315.html` `[unverified]`
- Content: where a contract leaves the determination of a term to one party, that party must in case
  of doubt exercise the determination according to **reasonable discretion** (*billiges Ermessen*);
  a determination made otherwise is not binding and, on application, is made by the court.
- Why it matters here: the annual **Cap-Festlegung** is a unilateral determination by the insurer of
  a term that decides the policyholder's return for the coming year. It is therefore reviewable
  under § 315 BGB, and the standard the insurer must meet is that the Cap be set on the basis it
  says it is set on — the option budget and the market price of the option package — rather than
  arbitrarily. **No German decision on the Cap-Festlegung of an Indexpolice is known to this author,
  and none was established.** Gap 16. The legal frame is nevertheless clear enough to state, and it
  is the correct frame: § 315 BGB, not § 163 VVG [R4].

---
