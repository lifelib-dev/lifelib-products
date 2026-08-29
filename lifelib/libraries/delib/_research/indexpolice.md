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
