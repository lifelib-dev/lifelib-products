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
2. **No verbatim quotation appears anywhere in this file.** Statutory and contractual content is
   described in this author's own words as *what the instrument provides*; no sentence is placed in
   quotation marks and attributed to any *Bedingungswerk*, statute or supervisory document, because
   there is neither a retrieval nor a search summary to attribute one to. That is the sharpest
   difference from `frlib/_research/temporaire-deces.md`, whose PDFs were downloaded and read, and
   from the two sibling delib files, whose search summaries reproduced German sentences.
3. **`[unverified]` is used generously.** Every specific paragraph number, effective date, amount,
   percentage, cap level, participation rate, product name and market figure is tagged unless it is
   a structural fact of the product that is not in dispute. The general shape of a well-established
   mechanic — surplus finances an option, monthly returns are capped and summed, the year cannot end
   negative — is *not* tagged, because tagging it would drown the signal.
4. **Uncertain numbers become `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — the Cap, the *Partizipationsquote*, the *Beitragsgarantie*, the
   *Rentenfaktor*, the charges, the lapse rate — the file states a `[std]` value with a rationale and
   an argued range. **A `[std]` number is honest; a fabricated `[S4]` number is not.** `indexpolice`
   carries a higher proportion of `[std]` parameters than any other delib product, and section 22
   and the gaps register say exactly which.
5. **Product names are the weakest class of claim here.** Every carrier product name below is
   recalled from general market knowledge and tagged `[unverified]`; gap 2 records this as the
   file's largest single defect. **No downstream document may present one as established.**

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
- Content: one of the few German consumer publishers that explains the sum-of-capped-monthly-returns
  mechanic in enough detail for a lay reader to see the asymmetry. Its standing argument — that the
  cap, the price-index basis and the charges together leave a return well short of a direct index
  investment — is reproduced as an argument, not as a citation, in mechanics section 21.
  **Not retrieved**; nothing numeric is taken from it.

### S13 — Stiftung Warentest / *Finanztest*, comparative tests of *Indexpolicen*
- Publisher: Stiftung Warentest — **secondary**
- Doc type: comparative product test with scoring and a cost analysis
- URL: not established (Stiftung Warentest content is largely paywalled in any case).
- Retrieved: no — egress blocked; no search corroboration.
- Content: a comparative test of this class would supply cap levels, cost quotas and modelled
  outcomes for a named panel of carriers in a named year — precisely the evidence gaps 3 and 6
  record. **Not retrieved, nothing cited.**

### S14 — Verbraucherzentrale (federal association and Länder consumer centres), pages on *Indexpolicen*
- Publisher: Verbraucherzentrale Bundesverband e. V. and the Länder centres — **secondary**
- Doc type: consumer-advice pages
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the sector's standing criticisms — that the payoff formula is not comprehensible to a
  normal purchaser, that the Cap is redetermined annually at the insurer's discretion, and that a
  zero year is a frequent outcome — are recorded as **positions**, not findings, in section 21.
  **Not retrieved.**

### S15 — Comparison portals: Verivox, Check24
- Publisher: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**
- Doc type: product-comparison and explainer pages
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: the usual public source for the commercial envelope — minimum premium, entry ages, term
  bands — when insurer *Produktinformationsblätter* are not reachable. **Not retrieved**; the
  envelope parameters in section 22 are `[std]`.

### S16 — German insurance trade press: *procontra*, *Versicherungsbote*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft*, *Handelsblatt*
- Publisher: various — **secondary**
- Doc type: trade and financial press reporting
- URL: not established.
- Retrieved: no — egress blocked; no search corroboration.
- Content: where cap changes, index switches and the repricing or withdrawal of index tariffs are
  reported, and the practical route by which a cap level for a named carrier and year reaches the
  public record [S5]. **Not retrieved**; every figure that would have come from it is a gap.

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
  interest assumption drives the **option budget**, which drives the **Cap**, which drives the payoff
  non-linearly. How carriers discharge § 154 for this product **is not established**. Gap 13.

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
- **Why the rate history is the reason this product exists.** At a *Höchstrechnungszins* of 0,25 %
  the guaranteed component of a conventional annuity's return is negligible and the discretionary
  component is the whole story. An Indexpolice takes that same discretionary component and, instead
  of crediting it as a modest certain interest amount, converts it into a bounded lottery on an
  index. **The product is a direct commercial response to a near-zero guaranteed rate.** The 2025
  rise to 1,00 % raises the guaranteed component again and makes the *sichere Verzinsung* arm
  relatively more attractive; whether that has shifted observed elections is `[unverified]`.

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
- Why it matters here: buying index options to back an index-participation obligation is the
  paradigm of a derivative **hedging a liability the insurer has itself written** — liability and
  hedge matched by construction, month for month and cap for cap. The insurer does **not** take an
  equity view for the policyholder; it buys the exact payoff it promised, and the Cap is whatever
  level makes that purchase cost the option budget. Sections 3 and 8 develop this. `[unverified]` at
  section level; the substance is standard practice.

### R10 — PRIIPs: Regulation (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653
- Publisher: EUR-Lex (the host refused the fetch)
- URL: not established.
- Content: requires a three-page *Basisinformationsblatt* for every packaged retail investment and
  insurance-based investment product, with a prescribed structure: what the product is, the risk
  indicator on a 1-to-7 scale, four performance scenarios (stress, unfavourable, moderate,
  favourable), the costs over time and the composition of costs including the reduction in yield,
  and the recommended holding period. The delegated regulation prescribes the methodology and the
  **product categories** that determine how scenarios are computed.
- Why it matters here: an Indexpolice is a **Category 4** PRIIP — its value depends in part on a
  factor not observed in the market, the insurer's discretionary surplus declaration — rather than a
  Category 3 derivative product; `[unverified]` for any specific carrier's KID. Category 4 permits
  the insurer's own model for the discretionary component, which is why two Indexpolicen with
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
- Relevance and delta: identical to product 2, with one wrinkle. Exercising the annual *Wahlrecht*
  is not a change of contract and does not restart the twelve-year clock `[unverified]`, whereas a
  *Vertragsänderung* that materially alters the contract can. Where the line falls is not settled.

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
- Relevance: an Indexpolice is squarely within scope and raises the *Kundennutzen* question in its
  sharpest form — a design that credits zero in a substantial fraction of years while carrying a full
  acquisition-cost load is what a value-for-money regime exists to interrogate. **Whether the
  *Merkblatt* names index products is not established.** Gap 15.

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

## Extracted facts, organised by mechanic

This is the section the delib `indexpolice` product specification and technical notes are written
from, and under the retrieval conditions above it is where the file earns its place. The mechanics
of the product are not in dispute; the levels are. Structural statements are made plainly; every
level is either `[unverified]` or `[std]`.

### 1. Product structure and legal form

- An *Indexpolice* is a **deferred annuity contract** (*aufgeschobene Rentenversicherung*) on a
  single life, with an *Aufschubphase* running from inception to *Rentenbeginn* and a *Rentenphase*
  paying a lifelong *Leibrente* thereafter. Everything about the chassis — premium, reserve, death
  benefit before *Rentenbeginn*, *Rückkaufswert*, *Beitragsfreistellung*, *Rentenfaktor*,
  *Kapitalwahlrecht*, *Rentengarantiezeit* — is the chassis of delib product 2 and is documented
  there [S9].
- **The delta is one clause set**: how the annually declared *Überschuss* is applied. In product 2 it
  is credited as interest to the *Deckungskapital*. In an Indexpolice the policyholder may elect,
  each year, to have it spent on a one-year index-linked payoff instead.
- Legally the index participation is therefore a form of ***Überschussverwendung*** under § 153 VVG
  [R1] and has **no independent statutory footing**. The policyholder's statutory right is to a
  share of surplus; the contract says how the share is applied; the index formula is a contract
  term, reviewable as such.
- The contract is a **conventional profit-participating contract** in regulation and accounting, not
  an *indexgebundene Lebensversicherung* in the balance-sheet sense, because the policyholder does
  not bear the investment risk [R15]. This classification decides how it is reserved, how it is
  reported, and which Solvency II line of business it falls in.
- **Wrappers.** The same index module is written on four chassis in the German market: *Schicht 3*
  private annuity (the delib scope), *Basisrente* (*Schicht 1*, delib product 5), *Riester*
  (*Schicht 2*, delib product 6), and *Direktversicherung* in *bAV* (out of delib scope). The
  wrapper changes the guarantee requirement [R12], the tax treatment [R13][R14] and the accessibility
  of the capital, and **not the index mechanics**.

### 2. Where the money sits — *Sicherungsvermögen*, not *Anlagestock*

- **The accumulated capital of an Indexpolice sits in the insurer's *Sicherungsvermögen*** — the
  ring-fenced general-account cover pool that backs all of the insurer's guaranteed obligations —
  in exactly the same way as the capital of a *klassische Rentenversicherung*. There is no
  *Anlagestock*, no unit account, no fund, and no policyholder-level asset allocation.
- The policyholder therefore owns a **claim on the insurer measured in euros**, not a number of
  units. The reserve is a *Deckungskapital* and rolls forward by a recursion, not by a unit price.
- **What the index does is define a payoff, not an investment.** The policyholder is not invested in
  the index at any moment. The insurer buys the option package that hedges the payoff it has
  promised [R9]; the policyholder never holds it.
- Three consequences a modeller who thinks of the product as unit-linked will get wrong:
  (i) **the capital cannot fall** — there is no mark-to-market of an account, a bad year credits zero
  rather than taking anything away; (ii) **there is no unit-pricing timing** — values are struck at
  the *Indexjahr* boundary, annually, which is why the delib model is on an **annual** grid
  (`Index_DE_A`) while the genuinely unit-linked product 3 is monthly; (iii) **the surrender value is
  a reserve, not a unit value** [R2].
- **What the policyholder actually risks is the opportunity cost of one year's surplus**: if the
  *Indexjahr* ends at or below zero, the surplus that would have been credited under the *sichere
  Verzinsung* is gone, spent on an option that expired worthless. That, and nothing more, is the
  downside — and stating it precisely is the antidote to both usual misreadings, that the product can
  lose capital and that it is a cheap way to be long equities.

### 3. The financing identity — the *Überschuss* as an option budget

This is the mechanical core of the product and everything else follows from it.

- Each year the insurer declares an *Überschussanteilsatz* out of the surplus the MindZV [R8] and its
  own results permit. For a contract in the *sichere Verzinsung* arm, that declared rate is credited
  to the *Deckungskapital* as interest, on top of the guaranteed *Rechnungszins*, exactly as in
  product 2.
- For a contract in the *Indexbeteiligung* arm, **the same amount is not credited. It is spent.** It
  becomes the ***Optionsbudget*** with which the insurer buys, for the coming *Indexjahr*, the option
  package that replicates the promised index payoff.
- Written as an identity, with `G` the participating capital at the start of the *Indexjahr* and `b`
  the declared surplus rate for that year:

  ```
  option budget          =  b x G
  price of the promised   =  b x G          <-- the Cap (or the Partizipationsquote) is set to
    index payoff on G                            make this equation hold
  ```

- **The Cap is not a marketing parameter. It is the solution of a pricing equation.** Given the
  option budget, the index's forward level, its implied volatility, its dividend yield and the
  interest rate, there is exactly one Cap at which the twelve-month capped-sum payoff costs the
  budget. That is why caps move from year to year without any change in the contract, and why they
  move in the directions described in section 8.
- Two corollaries that belong on the first page of any honest description of the product:
  (i) **an Indexpolice does not have a larger risk budget than a *Klassik* contract of the same
  vintage** — it has the identical budget, the same declared surplus from the same
  *Sicherungsvermögen* under the same MindZV minimum, and spends it differently; (ii) **priced
  risk-neutrally, the index arm is worth exactly what the safe arm is worth** — the whole difference
  between them is the equity risk premium earned on the option's delta, less dealing costs. The
  product is a redistribution of one year's surplus across states of the world, not extra return.
- **The budget can be zero.** If the insurer declares no surplus for a year, there is nothing to buy
  an option with, and the *Indexbeteiligung* for that year is worthless whatever the index does
  [R1][R8]. No German carrier's AVB, as far as this author knows, guarantees a minimum option
  budget; some guarantee a minimum Cap, which is a different and weaker promise (section 8). Gap 10.

### 4. The annual *Wahlrecht*

- **The policyholder elects, once a year and for the coming *Indexjahr* only, between
  *Indexbeteiligung* and *sichere Verzinsung*.** The election is a contractual right, exercisable
  without the insurer's consent, without medical evidence and without charge.
- **What each arm delivers**:

  | Arm | The year's surplus is | Outcome |
  |---|---|---|
  | *Sichere Verzinsung* | credited to the *Deckungskapital* as interest | certain, positive, immediately guaranteed |
  | *Indexbeteiligung* | spent on the index option package | zero in a bad year; a multiple of the surplus in a good one; never negative |

- **Timing.** The election must reach the insurer before the *Indexjahr* begins, typically with a
  notice period of a few weeks; a policyholder who does nothing continues in the arm they were in.
  The specific notice period is a carrier-level term and **is not established** — market practice as
  this author understands it is of the order of **four to six weeks** before the *Indexstichtag*
  `[unverified]`. Gap 11.
- **The interaction with the Cap announcement is the substantive question**, and it decides whether
  the *Wahlrecht* is an informed choice or a blind one. The insurer determines the Cap for the coming
  *Indexjahr* on market conditions shortly before it starts; the policyholder must elect before it
  starts. If the Cap is announced **before** the election deadline, the policyholder chooses knowing
  the terms; if **after**, they do not. **Which practice prevails is not established** and it is one
  of the two or three most consequential unestablished facts in this file. Gap 11.
- **Partial election.** Some tariffs permit the surplus to be split between the two arms — for
  instance half to the index and half to the safe rate — rather than requiring an all-or-nothing
  choice `[unverified]`. delib treats the election as a **fraction `w` in [0, 1]** of the surplus
  directed to the index arm, which makes the all-or-nothing case `w ∈ {0, 1}` a special case and
  costs nothing to implement.
- **Index choice.** Where a carrier offers more than one index, the annual election is normally also
  the occasion to switch between them `[unverified]`.
- **Survival of the right.** The *Wahlrecht* attaches to the capital, so it survives
  *Beitragsfreistellung* [R3] and persists to *Rentenbeginn*. In the *Rentenphase* it normally
  ceases, because the surplus is then applied to the annuity in payment by whichever of the payout
  surplus systems the contract uses; **whether any carrier offers index participation in the payout
  phase is not established** `[unverified]`. Gap 17.
- **Modelling.** The *Wahlrecht* is a **policyholder election**, which in delib's three-way
  assumption split makes it a *behavioural* assumption, not a contractual or an insurer-discretionary
  one. The delib base run sets `w = 1` (full index participation every year) as a `[std]` choice,
  because the product exists to demonstrate the index mechanic and a base run in the safe arm would
  reduce it to product 2. The specification exposes `w` per year and the technical notes list
  "election path assumed constant" as a model risk.

### 5. The Cap mechanic — the sum of capped monthly returns

**This is the single most important and most misunderstood feature of the product, and it deserves
to be stated in full and without hedging.**

- The *Indexjahr* is divided into **twelve monthly observation periods**. For each month `m` the
  index level is read at the two *Beobachtungstage* bounding the month, and the month's return is

  ```
  r_m = I(m) / I(m-1) - 1
  ```

- Each month's return is then **capped above at the Cap `C`**, and **not floored below**:

  ```
  x_m = min(r_m, C)
  ```

- The twelve capped monthly returns are **summed, not compounded**:

  ```
  S = sum over m = 1..12 of x_m
  ```

- The *Indexrendite* credited for the year is the sum **floored at zero**:

  ```
  Indexrendite = max(S, 0)
  ```

- The credit is that rate applied to the participating capital at the start of the *Indexjahr*:

  ```
  Indexgutschrift = max(S, 0) x G
  ```

- **The three features that together define the payoff, and that must never be separated**:
  1. **Upside is capped monthly.** A month in which the index rises 8 % contributes `C`, not 8 %.
  2. **Downside is not capped at all.** A month in which the index falls 8 % contributes the whole
     −8 %. There is no floor on `x_m`, only on `S`.
  3. **The twelve are summed, not compounded.** Summation is close to compounding for small numbers,
     but it is not the same, and the contractual formula is a sum.
- **Why this asymmetry is the whole story.** The payoff is a *capped cliquet*: the policyholder is
  short a strip of twelve monthly call options struck at `C` and long the index's monthly returns,
  with an annual floor. Truncating the right tail of each month while leaving the left tail intact
  removes far more expected return than the cap level suggests, because monthly equity returns are
  volatile: with a monthly standard deviation of the order of 5 % — an annualised volatility of
  about 17 %, an ordinary level for a broad European equity index — a 3 % monthly cap gives away
  roughly **1 percentage point of expected return per month**, twelve times a year, against an
  expected monthly return of well under 1 %. Section 20 does that arithmetic explicitly.
- **The floor is what makes it a life-insurance product rather than a bet**, and it is genuine: the
  worst *Indexjahr* imaginable credits zero, and the capital is untouched.
- **A trap for the modeller and for the reader.** The `max(S, 0)` floor operates on the *sum*, not on
  each month. It is therefore **not** true that a year with more up-months than down-months credits
  something; it is perfectly ordinary for a year in which the index finished **higher** to credit
  **zero**, because the up-months were capped and the down-months were not. The second worked example
  in section 19 is exactly that case, and it is the case a delib test must assert.
- **Interpretation questions the corpus does not settle**, each of which changes a credited amount and
  each of which is a carrier-level clause:
  - Whether the monthly observation dates are calendar month-ends or the monthly recurrences of the
    *Indexstichtag*. Gap 18.
  - Whether the index level used is a closing level, an average of a few days, or an average over the
    month (an "Asian" reading, which lowers the effective volatility and so buys a higher cap).
    Gap 18.
  - Whether `G`, the participating capital, is the whole *Deckungskapital* at the start of the
    *Indexjahr*, or only a defined index-participating part of it, or the accumulated
    *Überschussguthaben* alone. Different carriers do different things and **none is established**.
    Gap 19. delib takes `G` = the whole accumulated capital at the start of the *Indexjahr* as a
    `[std]` choice, because it is the reading under which the arithmetic in the customer-facing
    material of this product family works.
  - Whether a contract that begins or ends mid-*Indexjahr* participates pro rata or not at all.
    Gap 12.

### 6. The floor and the annual lock-in — *Höchststandsicherung*

- **An *Indexjahr* can never end below zero.** `max(S, 0)` is contractual, universal in this product
  family, and is the feature the product is sold on.
- **Whatever is credited is locked in.** At the end of the *Indexjahr* the *Indexgutschrift* is added
  to the capital and becomes **part of the guaranteed capital**: it is no longer at risk in any later
  year, it earns the guaranteed *Rechnungszins* thereafter like any other part of the
  *Deckungskapital*, and it enters the base `G` of every subsequent *Indexjahr*. This is the
  ***Höchststandsicherung*** / *Lock-in* / ratchet, and it is what makes the year-by-year floor add
  up to a path-independent guarantee.
- Formally, with `K(t)` the accumulated capital at the end of policy year `t`, `P(t)` the premium
  allocated, `i_g` the guaranteed rate and `b(t)` the declared surplus rate:

  ```
  index arm :  K(t) = ( K(t-1) + P(t) ) x (1 + i_g)  +  max( S(t), 0 ) x G(t)
  safe arm  :  K(t) = ( K(t-1) + P(t) ) x (1 + i_g + b(t))
  ```

  with `G(t)` the participating capital at the start of the *Indexjahr* (section 5). The monotonicity
  `K(t) >= K(t-1)` holds in both arms and is the invariant a delib `check_*()` should assert.
- **A monthly *Höchststandsicherung* is a different and rarer feature.** Some designs in the wider
  European market lock in the highest index level reached *within* the year rather than only the
  year-end sum. **No German carrier is established as offering it on this product**, and it should
  not be assumed. `[unverified]`; gap 20.
- **What the lock-in costs.** A ratchet is not free: the option package that must be bought each year
  is a fresh at-the-money strip on a *larger* base every year the previous year credited something.
  That is financed automatically, because the surplus is declared as a rate on the same larger base
  — which is the reason the financing identity of section 3 is written as rates and not as amounts.
- **The guarantee is a floor on the path, not only on the maturity value.** This distinguishes an
  Indexpolice from a plain maturity guarantee: with a maturity guarantee the insurer can recover a
  bad year with a good one, whereas here every credited amount is permanent. That is what a modeller
  should carry into the reserving discussion, and it is why the product's guarantee cost rises with
  every good year.

### 7. The *Partizipationsquote* alternative, and other payoff variants

The Cap is the classic design. It is not the only one, and by the 2020s it was not obviously the
dominant one.

- ***Partizipationsquote* (participation rate).** Instead of capping each month, the contract credits
  a fixed fraction `q` of the *year's* index movement, floored at zero:

  ```
  Indexrendite = max( q x ( I(12)/I(0) - 1 ), 0 )
  ```

  There is no monthly cap and no monthly asymmetry: a down-month is not penalised relative to an
  up-month, because only the year's net movement matters. The whole of the give-up is in `q`.
- **The two designs are not equivalent and they fail in different ways.** The Cap design gives away
  the *large* monthly moves and is therefore hurt by volatility even when the year ends well; the
  *Quote* design gives away a constant fraction and is hurt in exactly the same proportion in every
  state. For a policyholder, the *Quote* design is far easier to understand and to compare with a
  direct investment; for an insurer, the Cap design has historically bought a higher headline number
  out of the same budget, because the strip of monthly caps is a cheaper package than a fraction of
  a one-year call when volatility is high.
- **Typical levels, all `[unverified]` and all `[std]` downstream**: participation rates on a broad
  price index of the order of **50 % to 80 %**; participation rates on a low-volatility house
  multi-asset index (section 9) of the order of **80 % to above 100 %**, the latter being possible
  precisely because the index is engineered to be cheap to buy options on. Gap 9.
- **Other variants in this product family**, none established for any named German carrier, all
  `[unverified]`: **Cap and Quote in combination** (monthly returns capped *and* the sum multiplied
  by a participation rate); **a choice of variant each year**, making the *Wahlrecht* a three-way
  election; a ***Mindest-Cap***, a contractually guaranteed floor under the Cap the insurer may
  declare — a meaningful feature, because it converts an unbounded discretion into a bounded one, but
  no level for any carrier is established (gap 10); and **averaging**, an Asian reading of the index
  that lowers the effective volatility and so buys a higher cap or quote at the cost of tracking the
  index less closely.
- **delib's choice.** The reference implementation carries the **Cap design as the base** — because
  it is the design the product's reputation and its criticism both rest on, and because it is the one
  whose mechanic a model can demonstrate non-trivially — and the *Partizipationsquote* as a
  switchable variant. Both are `[std]` in their levels.

### 8. The *Cap-Festlegung* — who sets it, when, and on what

- **The Cap is fixed by the insurer, for one *Indexjahr* at a time, before that *Indexjahr* begins,
  and is then binding for its whole length.** It is not adjustable during the year, and a change in
  market conditions during the year does not change it.
- **The determination is a pricing calculation, not a discretion in substance** (section 3): the Cap
  is the level at which the option package costs the declared option budget. The inputs are the
  option budget, the index's implied volatility, its dividend yield, the risk-free rate and the
  dealing spread the insurer faces.
- **The directions of movement follow from that, and they are the useful part**:

  | If this rises | the Cap | because |
  |---|---|---|
  | the declared surplus rate (option budget) | rises | more money buys more upside |
  | the index's implied volatility | falls | monthly caps are strips of options; volatility makes them dearer |
  | the index's dividend yield | falls | options are on the price index; a higher dividend yield lowers the forward |
  | the risk-free rate | rises, indirectly | it raises the investment return and hence the surplus available |

- **Historical direction of travel**, stated qualitatively because no level is established: caps were
  compressed hard through the low-interest decade to the early 2020s, as the surplus available to buy
  them shrank with the *Höchstrechnungszins* and the run-off of high-yielding assets [R7]; the rise in
  interest rates from 2022 and the increase of the *Höchstrechnungszins* to 1,00 % for 2025 [R18]
  restored surplus and, with it, room in the caps. **No cap value for any named insurer in any named
  year is established in this file**, and none is guessed. Gap 3.
- **The plausible range, as a `[std]` band with a stated rationale**: monthly caps in this product
  family have been observed in the market over the 2010s and 2020s between roughly **1,5 % and
  5,0 %**, with the typical band around **2,5 % to 4,0 %** `[unverified]`. The delib reference
  implementation uses **`Cap = 3,0 % per month` as a `[std]` parameter**, chosen as the midpoint of
  that band, and the technical notes are required to run the worked example's sensitivity across the
  band rather than presenting the midpoint as a fact.
- **Announcement.** The Cap is communicated to the policyholder in the annual notification [S5] and
  in the *Standmitteilung* [S10]. Neither document class was located.
- **Legal review.** The *Cap-Festlegung* is a unilateral determination of a contractual term and is
  reviewable under § 315 BGB for *billiges Ermessen* [R22] — not under § 163 VVG, which governs
  adjustments of the contract itself [R4]. This distinction matters commercially as well as
  doctrinally: an insurer that set caps below what its option budget bought would be exposed under
  § 315 BGB, and that, rather than any specific supervisory rule, is the discipline on the
  determination. **No decided German case on the point is known to this author.** Gap 16.

### 9. The index — EURO STOXX 50, and the move to house multi-asset indices

- **The classic underlying is the EURO STOXX 50**, the blue-chip index of the euro area, and it was
  the underlying of the first German index-participation products. Two properties of it drive the
  product's economics:
  1. **It is quoted, and used, as a *price index*** — a *Kursindex*, from which dividends are
     excluded. Options are written on the price index. The euro-area dividend yield, of the order of
     **3 % per year** `[unverified]`, therefore never reaches the policyholder in any state of the
     world. This is a permanent, structural give-up that sits on top of the cap and is invisible to a
     purchaser comparing the product to "the index".
  2. **It is volatile** — an annualised volatility of the order of 18 % to 22 % in ordinary
     conditions `[unverified]` — which makes the monthly cap strip expensive and therefore forces the
     Cap down.
- **The shift to house indices.** From the mid-2010s a substantial part of the German market replaced
  the EURO STOXX 50 in these tariffs with **bespoke multi-asset indices** built for the insurer by an
  investment bank or index provider. Their common features: **multi-asset** composition (equities,
  bonds, sometimes commodities and money market) so that volatility is structurally lower than an
  equity index's; **volatility targeting**, a rule scaling exposure to hold realised volatility at a
  target often around **5 %** `[unverified]` — the decisive engineering step, because at a 5 % target
  the option package costs a fraction of what it costs on a 20 %-volatility equity index, so the same
  budget buys a **participation rate near or above 100 %**, a far better headline than 55 % of the
  EURO STOXX 50; an **excess-return construction with an embedded fee**, the index defined net of a
  funding rate and net of an index-level deduction of the order of **0,5 % to 1,5 % per year**
  `[unverified]`, which reduces the policyholder's return without appearing in any cost disclosure;
  and **a short live history behind a long backtest**, which makes published "historical" performance
  of the product weaker evidence than it appears.
- **The honest summary of the shift**: it moved the give-up from a place the purchaser can see (a
  55 % participation rate; a 3 % cap) to places the purchaser cannot (an index rule, a volatility
  target, a fee inside the index level, a backtest). The headline numbers improved and the expected
  outcome did not necessarily improve with them, because the financing identity of section 3 still
  binds: **the payoff still costs the option budget, whatever the underlying is called.**
- **No specific German house index is named in this file.** This author cannot name one with
  confidence, and naming one wrongly would be worse than not naming one. Gap 21.
- **Modelling consequence.** delib parameterises the index by **an assumed annualised volatility and
  an assumed drift**, both `[std]`, and by an explicit monthly return path supplied as an external
  CSV, and shows the outcome under a high-volatility equity index and a low-volatility multi-asset
  index side by side. That is the honest way to represent a fact the corpus establishes
  qualitatively and not quantitatively.

### 10. Index substitution, *Ersatzindex* and adjustment clauses

- Every contract of this family needs a clause for what happens if the index ceases to be published,
  is materially restructured, or ceases to be available on terms on which the insurer can buy the
  hedge. The standard solution is an ***Ersatzindex*** clause: the insurer may substitute a
  comparable index, on notice to the policyholder.
- Two questions on which carriers differ and on which **nothing is established**:
  - Whether the substitution requires the confirmation of an **unabhängiger Treuhänder** [R4]. Some
    German AVB in adjacent product families do require it; whether index tariffs do is not
    established. Gap 22.
  - Whether the policyholder gets a **special termination right** (*Sonderkündigungsrecht*) or at
    least an unscheduled right to switch to the *sichere Verzinsung* when the index changes. Gap 22.
- The distinction from § 163 VVG matters again here: substituting the index is a change to a
  contractual term and therefore lives in the § 164 VVG / *Treuhänder* / express-clause world, while
  redetermining the Cap is not [R4][R22].
- **Modelling consequence**: none directly, but it belongs in the technical notes' model-risk list.
  A model that projects thirty *Indexjahre* on one index rule is assuming no substitution over a
  period in which the market has already substituted once.

### 11. The guarantee at *Rentenbeginn*, and *Beitragsgarantie* levels below 100 %

- **The guarantee of an Indexpolice is an end-of-accumulation guarantee.** What the contract promises
  is a *garantiertes Kapital zu Rentenbeginn*, normally expressed as a percentage of the premiums
  paid — the ***Beitragsgarantie*** or *Garantieniveau* — plus every index credit locked in along the
  way (section 6), and a *garantierter Rentenfaktor* converting that capital into an annuity.
- **It is not a guaranteed annual interest rate on the reserve.** That is the defining feature of
  ***Neue Klassik*** and the reason index products are grouped under that label [S6]: by owing the
  guarantee only at one future date rather than at every balance date, the insurer can hold a
  materially riskier asset mix behind it and generate the surplus that becomes the option budget.
  A model that reserves an Indexpolice as though it guaranteed `i_g` every year overstates the
  guarantee.
- **Why guarantee levels fell below 100 %.** A 100 % nominal guarantee of gross premiums over, say,
  30 years is trivially affordable at a 3,5 % technical rate and close to impossible at 0,25 % once
  acquisition and administration costs are financed out of the same premiums. Through the 0,90 % and
  0,25 % years [R7], carriers responded by offering a **choice of *Garantieniveau*** — commonly
  **60 %, 80 %, 90 % or 100 %** of premiums paid `[unverified]` — and by making 80 % or 90 % the
  recommended default. The arithmetic is direct and worth stating because it explains the whole
  design generation: **every euro of guarantee that is not promised is a euro that can back risk
  assets, and therefore a larger option budget.**
- **The wrapper decides the floor** [R12]: a *Riester* index variant must guarantee 100 % of
  contributions and allowances and therefore has the smallest option budget of the four wrappers; a
  *Basisrente* or *Schicht 3* index variant may guarantee less; *Direktversicherung* under a
  *Beitragszusage mit Mindestleistung* has its own statutory floor and is out of scope.
- **`[std]` for delib**: *Garantieniveau* **90 % of *Beitragssumme***, on the reasoning that it is the
  level at which a 1,00 % *Höchstrechnungszins* contract can still finance a visible option budget
  over a 30-year term, and that it sits inside the observed 60–100 % band. The specification exposes
  the level and the technical notes show the option budget as a function of it — that dependency is
  the most instructive single sensitivity this product has.
- **Interaction with the lock-in.** The effective guarantee at any time is
  `max( Beitragsgarantie, guaranteed capital including all locked-in index credits )`, and after a
  few good years the second term dominates. A projection must carry both and take the maximum, and a
  test should assert that the guaranteed capital is monotone non-decreasing.

### 12. Premium

- **Level *Beitrag*, payable monthly, quarterly, half-yearly or annually** over a
  *Beitragszahlungsdauer* which may be shorter than the *Aufschubdauer*; single premium
  (*Einmalbeitrag*) versions exist; *Zuzahlungen* (ad-hoc top-ups) are commonly permitted.
- A ***Ratenzahlungszuschlag*** applies for paying other than annually; the market convention
  recorded in the sibling delib file is of the order of **2 % half-yearly, 3 % quarterly, 5 %
  monthly** `[unverified]`, and delib carries it as `[std]`.
- A ***Dynamik*** option (automatic annual premium increase, with a matching benefit increase, and a
  right to decline) is normal on this chassis. It interacts with the guarantee: each increment is a
  new tranche with its own guarantee basis `[unverified]`.
- **The premium does not enter the index formula.** Premiums build the capital `K`; the index payoff
  is struck on the participating capital `G` at the *start* of the *Indexjahr*. Premiums paid during
  an *Indexjahr* therefore, in the natural reading, participate only from the following *Indexjahr*.
  **Whether carriers pro-rate them is not established** — gap 12 — and delib adopts the natural
  reading as `[std]`: `G(t)` is the capital at the start of the year, premiums of year `t` join `G`
  at `t+1`.
- **`[std]` model point**: *Beitrag* **200 € per month**, entry age **40**, *Aufschubdauer* **27
  years** to *Rentenbeginn* at **67**, premiums payable throughout. Rationale in section 22.

### 13. Charges

Nothing about the charge structure of an Indexpolice is special; nothing about its levels is
established.

- **Abschluss- und Vertriebskosten**, financed by *Zillmerung*, capped by the DeckRV
  *Höchstzillmersatz* at **25 ‰ of the *Beitragssumme*** `[unverified]` [R7], and required by
  § 169 VVG to be spread over at least the first five years for the purpose of the
  *Mindestrückkaufswert* [R2]. The two rules are different rules with different functions and delib
  keeps them apart.
- **Verwaltungskosten**, typically a percentage of each premium (`β`) plus a percentage of the
  *Deckungskapital* (`γ`), sometimes with a fixed *Stückkosten* amount per year.
- **The index-specific charges are the ones that do not appear in the charge tables**:
  - the **dealing cost and spread** on the option package, which is inside the Cap rather than in a
    charge line — a wider spread simply produces a lower Cap;
  - for house indices, the **index-level deduction and the volatility-target drag** (section 9),
    which are inside the index and therefore inside neither the Cap nor the disclosed costs;
  - the **dividend yield of a price index** (section 9), which is not a charge at all but is a
    permanent give-up of the same order of magnitude as one.
  Together these mean that the disclosed *Effektivkosten* of an Indexpolice **understate** the
  economic give-up relative to holding the index, by an amount that is not disclosed anywhere. This
  is the most substantive fair-criticism point in the file and it is a structural fact, not a claim
  about any carrier.
- **No charge level of any kind is established for any German index product.** Every charge in delib
  is `[std]`. The `[std]` set the reference implementation uses, with the sibling files' reasoning:
  *Abschlusskosten* **2,5 % of *Beitragssumme*** zillmerised over five years; *Verwaltungskosten*
  **β = 3 % of each premium** and **γ = 0,25 % of the *Deckungskapital* per year**. Gap 6.

### 14. *Rückkaufswert* and *Beitragsfreistellung*

- **Surrender** delivers the *Rückkaufswert* under § 169 VVG [R2]: the actuarial reserve, floored by
  the five-year-spread *Mindestrückkaufswert*, less any contractually quantified *Stornoabzug*.
- **Locked-in index credits are inside the reserve** and are therefore inside the surrender value —
  they are guaranteed capital by then (section 6), not a contingent entitlement.
- **The running *Indexjahr* is not.** A surrender in month 7 of an *Indexjahr* forfeits that year's
  option payoff, because the payoff exists only at the year end. Whether the unspent option budget is
  refunded, whether a pro-rata payoff is computed, or whether the policyholder simply loses it, is a
  carrier-level clause and **is not established**. Gap 12. delib's `[std]` is the simple and, in this
  author's understanding, usual treatment: **no index credit in the year of exit**.
- **This is a real behavioural incentive and belongs in the lapse discussion**: an Indexpolice
  rewards surrendering just after an *Indexjahr* end and penalises surrendering just before one. A
  model on an annual grid with exits at year end is implicitly assuming the favourable convention;
  the technical notes must say so.
- **Beitragsfreistellung** under § 165 VVG [R3] leaves the accumulated capital in place, continues the
  index participation on it, and preserves the *Wahlrecht* (section 4). It converts the contract to a
  reduced guaranteed benefit computed on recognised actuarial principles.
- **Stornoabzug** must be agreed, appropriate and quantified [R2]; the sibling KLV file records one
  carrier's structure of a **5 % base deduction plus a capital-market-dependent component of 5 %,
  10 % or 15 % of the *Deckungskapital*** `[unverified]`, established there by search. delib's
  `[std]` is a **flat 2 % of the *Deckungskapital*, floored so the *Mindestrückkaufswert* is never
  breached**, with the observed range recorded beside it.

### 15. The death benefit before *Rentenbeginn*

- The standard *Todesfallleistung* in the *Aufschubphase* of a German deferred annuity is the
  **return of the accumulated capital** — variously the *Deckungskapital*, the *Rückkaufswert*
  without *Stornoabzug*, or the premiums paid if higher — rather than a sum at risk. Carrier practice
  varies and is documented for the chassis in delib product 2 [S9].
- **Index-specific point**: whether death mid-*Indexjahr* attracts a pro-rata index credit is the same
  unestablished question as for surrender (gap 12); the `[std]` treatment is the same, no credit in
  the year of exit.
- Because the sum at risk is close to zero, the *Risikoüberschuss* on this product is small, the
  underwriting is light (section 17), and § 161 VVG [R6] is close to inoperative.
- The **50 % *Mindesttodesfallschutz*** condition of the tax rules [R14] bites on the *Kapitalwahlrecht*
  treatment, not on the annuity, and is a reason some tariffs carry a death benefit above the plain
  return of capital `[unverified]`.

### 16. The *Rentenphase* — *Rentenfaktor* and *Kapitalwahlrecht*

Inherited wholesale from delib product 2; recorded here only as the delta.

- At *Rentenbeginn* the accumulated capital `K` — guaranteed capital plus all locked-in index credits
  plus any *Schlussüberschuss* and *Bewertungsreserven* share — is converted at the *Rentenfaktor*:

  ```
  monthly annuity = K / 10 000 x Rentenfaktor
  ```

- The applied factor is the **maximum of the guaranteed factor fixed at issue and the insurer's
  current factor at *Rentenbeginn***, a guarantee with upside, established for the chassis in
  product 2's research from two independent carrier documents.
- **The index mechanic ends at *Rentenbeginn***: the capital is fixed, the *Wahlrecht* lapses, and
  surplus in the *Rentenphase* is applied to the annuity in payment by whichever payout surplus
  system the contract uses. Whether any carrier offers index participation in payment is **not
  established**; gap 17.
- The ***Kapitalwahlrecht*** — taking the capital as a lump sum instead of the annuity, normally
  exercisable in a window before *Rentenbeginn* — applies unchanged, with the tax consequence in
  [R14].
- **`[std]` for delib**: a *garantierter Rentenfaktor* of **25,00 € per 10 000 € per month** at
  *Rentenbeginn* 67, taken over from product 2's `[std]`, with the current factor set equal to it in
  the base run so the max-of-two rule is exercised by a test rather than by the base path.

### 17. Decrements, underwriting and policyholder behaviour

- **Underwriting is light or absent.** The sum at risk before *Rentenbeginn* is close to zero, so a
  savings-form deferred annuity is normally issued on a short declaration or none at all
  `[unverified]`. The mortality basis for the accumulation phase matters little; the basis for the
  *Rentenphase* matters greatly and is **DAV 2004 R**, the generational annuitant table, documented
  in product 2's research.
- **DAV tables are the property of the Deutsche Aktuarvereinigung, are not public and are not
  redistributed in this library.** delib ships `[std]` proxies anchored so the worked example
  reproduces exactly, and says what a replacement must preserve.
- **Lapse.** No index-product-specific *Stornoquote* is established. The market-wide GDV measures
  recorded in the sibling file are of the order of **2,7 % on the main measure and 1,2 % per contract
  for 2024** `[unverified]`, and the two are not reconcilable from the available evidence. delib's
  lapse assumption is `[std]`, with the section-14 timing incentive noted as a model risk.
- **The election path is the behavioural assumption unique to this product** (section 4). Real
  policyholders in this product family are widely believed to be inert — to elect once at inception
  and never revisit — which if true makes the annual *Wahlrecht* far less valuable than its
  description suggests. **This is not established** and is flagged as `[unverified]`; delib's base
  run assumes full index participation in every year and treats the alternative as a sensitivity.

### 18. Taxation

- ***Schicht 3* annuity**: taxed on the *Ertragsanteil* only, by age at *Rentenbeginn* [R13] —
  about 17 % of the annuity at age 67 `[unverified]`.
- **Lump sum under the *Kapitalwahlrecht***: the excess of the payment over premiums paid is
  investment income; if the contract has run twelve years and the payment falls after age 62, **half
  the difference** is taxable at the personal rate, subject to the *Mindesttodesfallschutz*
  condition for contracts from 1 April 2009 [R14]. All figures `[unverified]`.
- **The index credits are not separately taxed.** They are absorbed into the capital as they are
  credited; there is no annual tax event, no *Abgeltungsteuer* on the year's index gain, and no
  *Teilfreistellung* under the *Investmentsteuergesetz* — the latter because there is no fund. This
  **tax deferral inside the wrapper is one of the two genuine advantages the product has over
  holding an index fund directly**, the other being the guarantee. It should be stated in the
  product specification alongside the criticism in section 21, because a fair comparison has to carry
  both sides.
- *Basisrente* and *Riester* wrappers change the tax treatment entirely (full deductibility of
  contributions and full taxation of the annuity; allowances and *Sonderausgabenabzug* respectively)
  and are documented under delib products 5 and 6.
- No German tax rule turns on the index mechanic itself. delib's model publishes gross cash flows and
  does not compute tax; the tax section of the product specification is context.

### 19. Two worked *Indexjahre* — constructed, `[std]` throughout

**The brief asked for a documented worked example of an *Indexjahr* from insurer material or the
consumer press, with the twelve monthly index movements and the resulting credit. None was located**
— see gap 4 and [S10]. The two examples below are therefore **constructed by this author** to
exhibit the mechanic exactly, and every number in them is `[std]`. They are not evidence about any
carrier or any year. They are, however, arithmetically exact, and they are the pattern the delib
worked example and its tests should follow.

Common assumptions, all `[std]`: participating capital at the start of the *Indexjahr*
`G = 50,000.00 €`; monthly Cap `C = 3.00 %`; declared surplus rate (option budget) `b = 2.50 %`;
guaranteed rate `i_g = 1.00 %`; *Partizipationsquote* variant `q = 60 %`.

**Example A — a strong year. The cap costs 4,20 points and the year still credits well.**

| Month | Index return `r_m` (%) | Capped `x_m = min(r_m, 3.00)` (%) | Given away (%) |
|---|---|---|---|
| 1 | 1.80 | 1.80 | 0.00 |
| 2 | -2.40 | -2.40 | 0.00 |
| 3 | 4.60 | 3.00 | 1.60 |
| 4 | 0.90 | 0.90 | 0.00 |
| 5 | -3.70 | -3.70 | 0.00 |
| 6 | 2.20 | 2.20 | 0.00 |
| 7 | 3.40 | 3.00 | 0.40 |
| 8 | -1.10 | -1.10 | 0.00 |
| 9 | 0.40 | 0.40 | 0.00 |
| 10 | 5.20 | 3.00 | 2.20 |
| 11 | -0.80 | -0.80 | 0.00 |
| 12 | 2.60 | 2.60 | 0.00 |
| **Sum** | **13.10** | **8.90** | **4.20** |

- Sum of capped monthly returns `S = +8.90 %`; positive, so `Indexrendite = 8.90 %`.
- ***Indexgutschrift* = 8.90 % x 50,000.00 = 4,450.00 €**, credited and locked in.
- Cross-checks a reader can do with a calculator:
  - the **compounded** index return over the year is `prod(1 + r_m) - 1 = +13.4548 %`, against the
    **sum** of `+13.10 %` — the two differ by 0.35 points, which is the compounding effect the
    contractual formula does not give;
  - the cap bound in exactly three months and cost **4.20 points**, which is `13.10 - 8.90`;
  - the *sichere Verzinsung* arm would have credited `b x G = 2.50 % x 50,000.00 = 1,250.00 €`. The
    index arm therefore paid **3.56 times** the safe arm in this year;
  - the *Partizipationsquote* variant would have credited
    `max(60 % x 13.4548 %, 0) x 50,000.00 = 4,036.44 €` — **less** than the cap variant here,
    because the cap variant's give-up was concentrated in three months.

**Example B — the case the product is criticised for. The index rises 6,44 % and the credit is zero.**

| Month | Index return `r_m` (%) | Capped `x_m = min(r_m, 3.00)` (%) | Given away (%) |
|---|---|---|---|
| 1 | 6.50 | 3.00 | 3.50 |
| 2 | -2.10 | -2.10 | 0.00 |
| 3 | 5.80 | 3.00 | 2.80 |
| 4 | -1.90 | -1.90 | 0.00 |
| 5 | -2.40 | -2.40 | 0.00 |
| 6 | 4.20 | 3.00 | 1.20 |
| 7 | -3.10 | -3.10 | 0.00 |
| 8 | 0.60 | 0.60 | 0.00 |
| 9 | -2.80 | -2.80 | 0.00 |
| 10 | 5.10 | 3.00 | 2.10 |
| 11 | -1.70 | -1.70 | 0.00 |
| 12 | -1.20 | -1.20 | 0.00 |
| **Sum** | **7.00** | **-2.60** | **9.60** |

- Sum of capped monthly returns `S = -2.60 %`; negative, so `Indexrendite = max(-2.60 %, 0) = 0`.
- ***Indexgutschrift* = 0.00 €.** Nothing is credited, nothing is lost, the capital is untouched, and
  the year's surplus of 1,250.00 € has been spent on options that expired worthless.
- Cross-checks:
  - the **compounded index return for the year was `+6.4402 %`** and the sum of raw monthly returns
    was `+7.00 %` — **the index rose, and the credit was zero**;
  - the cap bound in four months and cost **9.60 points**, which is `7.00 - (-2.60)`;
  - the *sichere Verzinsung* arm would have credited **1,250.00 €**;
  - the *Partizipationsquote* variant would have credited
    `max(60 % x 6.4402 %, 0) x 50,000.00 = 1,932.06 €` — **more than the safe arm and infinitely more
    than the cap variant**, which is the cleanest possible demonstration that the two designs are not
    interchangeable.
- **This example is the delib pitfall test.** An implementation that floors each month at zero, or
  that compounds rather than sums, or that applies the floor to the compounded return rather than to
  the sum of capped returns, will credit something here. The correct answer is zero, and a test must
  assert it.

**The two years together.** Over the two *Indexjahre*, on an unchanged base of 50,000.00 € for
clarity, the index arm credits `4,450.00 + 0.00 = 4,450.00 €`; the safe arm credits
`1,250.00 + 1,281.25 = 2,531.25 €` (the second year's 2,50 % struck on 51,250.00 €). The index arm
wins over these two constructed years by **1,918.75 €**, and it does so entirely on the strength of
one year in three-and-a-half-times territory while losing the other outright. That shape — a
minority of large years carrying a majority of zero years — is the product's real return
distribution, and section 20 puts a number on it.

### 20. What the cap costs — an expected-value calculation, `[std]` throughout

The single most useful thing this file can supply downstream, given that no market cap level or
outcome distribution could be established, is the arithmetic that turns an assumed volatility and an
assumed cap into an expected credit. It is elementary and it is decisive.

**Assumptions, all `[std]`, and all of them exposed as parameters in the delib technical notes**:
monthly index returns independent and normally distributed; monthly mean `mu = 0.60 %` (an
arithmetic 7,2 % per year, a plausible real-world equity drift on a price index); monthly standard
deviation `sigma = 5.00 %` (an annualised 17,3 %, ordinary for a broad European equity index);
monthly Cap `C = 3.00 %`.

**Step 1 — what one month gives away.** With `d = (C - mu) / sigma = 0.48`:

```
E[ max(r - C, 0) ]  =  sigma x phi(d)  -  (C - mu) x (1 - Phi(d))
                    =  5.00 x 0.35551  -  2.40 x 0.31561
                    =  1.7776 - 0.7575  =  1.0201 %
```

**Step 2 — what one month is worth after the cap.**

```
E[ min(r, C) ]  =  mu - E[ max(r - C, 0) ]  =  0.60 - 1.02  =  -0.42 % per month
```

**Read that line twice.** With a 3 % monthly cap and a 17 % index, **the expected value of a capped
month is negative**, because the cap removes more expected return than the month has. The
policyholder's expected sum over the year is `12 x (-0.42) = -5.04 %`.

**Step 3 — what the annual floor is worth.** The floor is the only reason the product has a positive
expectation at all. With `Var[min(r, C)] = 13.62` per month and independence, `S` has mean `-5.04 %`
and standard deviation `sqrt(12 x 13.62) = 12.79 %`, and

```
E[ max(S, 0) ]  =  mu_S x Phi(mu_S / sigma_S)  +  sigma_S x phi(mu_S / sigma_S)
                =  -5.04 x 0.3467  +  12.79 x 0.36912
                =  -1.747 + 4.719  =  2.97 % per year

P( S <= 0 )     =  Phi( 5.04 / 12.79 )  =  0.65
```

**The three numbers to carry downstream**, all `[std]` and all conditional on the assumptions above:

| Quantity | Value | Meaning |
|---|---|---|
| Expected annual credit | about 2.97 % | what the index arm is worth per year |
| Probability of a zero year | about 65 % | roughly two years in three credit nothing |
| The safe arm | 2.50 % | what the same surplus credits with certainty |

- **The index arm's expected credit exceeds the safe arm's by a modest margin and does so with a very
  high probability of zero.** That is the product's true risk-return profile under these assumptions,
  and it is very far from how it is normally described. The excess over the safe arm is not free
  money: it is the **equity risk premium earned on the option package's delta**, and it is the only
  economic reason the index arm can be worth more than the safe arm at all (section 3).
- **A consistency check the delib technical notes must run, and which is instructive because it
  fails at these numbers.** Repeating the calculation under a risk-neutral drift on a price index —
  drift `r - q`, with a 2,5 % risk-free rate and a 3 % dividend yield, so `mu = -0.04 %` per month —
  gives an option-package value of the order of **1,7 % of `G`**. That is **below** the assumed
  option budget of 2,5 %, which means the assumed pair (`C = 3,0 %`, `b = 2,5 %`) is **not mutually
  consistent**: at that volatility, a 2,5 % budget would buy a cap somewhat **above** 3,0 %.
- **The instruction that follows is the important one.** A delib model must **calibrate the Cap to
  the option budget**, not choose the two independently, or it will publish a product that is either
  free money or a swindle depending on which way the inconsistency falls. The technical notes are
  required to state the calibration explicitly, to run it, and to report the calibrated cap beside
  the `[std]` 3,0 % headline.
- **Sensitivity, which is the real point**: the expected credit is extremely sensitive to the assumed
  volatility, because volatility enters twice — it makes the cap bind more often (lowering the
  expectation) and it makes the floor worth more (raising it). At a 5 % annualised volatility, the
  low-volatility house-index case of section 9, the same cap almost never binds and the payoff
  approaches the index return; at 25 % the expected credit is dominated by the floor. **Any single
  expected-return number quoted for this product without its volatility assumption is meaningless**,
  and that is worth saying in the product specification.

### 21. Criticism of the product

Recorded as arguments, with their strength assessed, because no consumer test or academic paper was
retrieved and none is cited.

1. **The cap's effect on the expected credit is large and is not disclosed in a form a purchaser can
   use.** Section 20 quantifies it: at ordinary equity volatility a 3 % monthly cap can make a
   capped month's expected value negative, and the product's positive expectation then rests
   entirely on the annual floor. The purchaser is told the cap, is not told the volatility, and is
   in no position to do this calculation. **This is the strongest criticism of the product and it is
   structural, not a matter of any carrier's conduct.**
2. **Negative months are uncapped and this is genuinely counter-intuitive.** A symmetric-sounding
   description — "you get the index's monthly moves, up to 3 % a month" — conceals that the
   asymmetry runs entirely one way. Example B in section 19 is the demonstration: the index rose
   6,44 % and the credit was zero. **This is the feature most often misdescribed in secondary
   material**, including by intermediaries.
3. **The comparison with a direct index investment is unfavourable on every axis except the
   guarantee and the tax deferral.** A direct holding of a total-return index fund receives the
   dividends (some 3 % per year on euro-area equity, `[unverified]`), has no cap, no participation
   rate, no annual reset and charges of a few basis points. The Indexpolice gives up the dividends
   (section 9), gives up the tail of every good month, adds acquisition and administration costs
   (section 13), and possibly adds an index-level fee that is not disclosed. **What it gives back is
   real**: the capital cannot fall, credits are locked in permanently, the guarantee is the
   insurer's, and the accumulation is tax-deferred inside the wrapper with a favourable treatment on
   exit [R14]. A fair statement puts both sides, and the delib product specification is required to.
4. **The Cap is redetermined annually at the insurer's discretion.** The purchaser signs a contract
   whose economic terms for year 12 are unknown at inception and will be set by the counterparty.
   § 315 BGB [R22] constrains that discretion in principle; **no decided case tests it** (gap 16),
   and no carrier is established as guaranteeing a *Mindest-Cap* (gap 10).
5. **The move to house indices moved the give-up out of sight** (section 9): a participation rate
   near 100 % on a volatility-targeted excess-return index with an embedded fee is not obviously a
   better deal than 55 % of the EURO STOXX 50, and it is much harder to evaluate.
6. **Complexity as a defect in itself.** A retail savings product whose payoff requires the reader to
   understand a strip of capped monthly returns, an annual floor, an option budget financed by a
   discretionary surplus declaration and an annual election, is a product most purchasers cannot
   evaluate. That is a conduct-supervision concern in the terms of BaFin's value-for-money framing
   [R16][R17], and it is the reason this product, more than any other in delib, deserves a
   mechanically exact reference implementation.
7. **The counter-argument, stated fairly.** The relevant comparison for most purchasers is not with
   an index fund but with the *sichere Verzinsung* arm of the same contract — the classic annuity
   they would otherwise have bought. Against that benchmark the index arm has a higher expected
   value (section 20), cannot do worse than zero in any year, and costs nothing extra. On that
   comparison the product is defensible, and the annual *Wahlrecht* means the purchaser can retreat
   to the benchmark at any anniversary.

### 22. Typical parameter levels

**Every level in this section is `[unverified]` or `[std]`. Not one was established from a
document.** The `[std]` column is what the delib reference implementation uses; the range column is
this author's assessment of the plausible market band and is itself `[unverified]`.

| Parameter | `[std]` for delib | Plausible market range | Basis for the choice |
|---|---|---|---|
| Monthly Cap | 3.00 % | 1.5 % – 5.0 % | midpoint of the band; must be calibrated to the budget (section 20) |
| *Partizipationsquote*, equity price index | 60 % | 50 % – 80 % | midpoint; variant design only |
| *Partizipationsquote*, house multi-asset index | 100 % | 80 % – 120 % | the design's selling point (section 9) |
| Declared surplus rate = option budget `b` | 2.50 % | 2.0 % – 3.0 % | consistent with the 2026 declared rates recorded at [R20] |
| Guaranteed rate `i_g` | 1.00 % | 0.25 % – 1.00 % by cohort | the *Höchstrechnungszins* for 2025–2026 [R7][R18] |
| *Garantieniveau* (*Beitragsgarantie*) | 90 % of *Beitragssumme* | 60 %, 80 %, 90 %, 100 % | section 11; 100 % is statutory for *Riester* [R12] |
| Index volatility (annualised) | 17.3 % | 15 % – 22 % equity; 5 % – 8 % house index | section 9 and section 20 |
| Dividend yield forgone (price index) | 3.0 % | 2.5 % – 3.5 % | euro-area equity; section 9 |
| *Beitrag* | 200.00 € per month | 50 € – 1,000 € | a plausible mass-market monthly savings premium |
| *Eintrittsalter* | 40 | 25 – 55 | mid-career, the segment this product is sold into |
| *Rentenbeginn* | 67 | 62 – 70 | the German statutory retirement age; 62 is the tax boundary [R14] |
| *Aufschubdauer* | 27 years | 12 – 40 years | 12 is the tax minimum [R14]; 27 follows from 40 to 67 |
| *Rentenfaktor*, guaranteed | 25.00 € per 10,000 € per month | not established | inherited `[std]` from delib product 2 |
| *Abschlusskosten* | 2.5 % of *Beitragssumme* | ceiling 25 ‰ [R7] | at the *Höchstzillmersatz* |
| *Verwaltungskosten* | 3 % of premium + 0.25 % of reserve p.a. | not established | inherited `[std]` from delib products 1 and 2 |
| *Ratenzahlungszuschlag* | 5 % monthly | 2 % / 3 % / 5 % | market convention `[unverified]` |
| *Stornoabzug* | 2 % of *Deckungskapital* | 0 % – 20 % | inherited `[std]`; observed range at [R2] discussion |
| *Stornoquote* | 3 % per year, level | 1.2 % – 2.7 % market-wide | inherited `[std]`; no index-specific rate exists |
| *Wahlrecht* election `w` | 1.00 (full index) every year | 0.00 – 1.00 | the product exists to demonstrate the index arm |

- **The one parameter that cannot be chosen freely is the Cap**, because it is determined by the
  budget (sections 3, 8 and 20). delib's 3,00 % is the headline; the calibrated value is what the
  model must actually use, and the technical notes must publish both.
- **The *Eintrittsalter*, the *Beitrag* and the term are pure `[std] `construction.** No
  *Produktinformationsblatt* was located [S3][S11] and therefore no commercial envelope was
  established. Gap 5.

### 23. Market context

- **No figure for the size of the German index-participation segment exists in this file, and this
  author does not believe a published one exists at all**, because GDV's product statistics count
  these contracts within conventional annuity business, which is what they are [R15][R19]. Gap 8.
- What can be said qualitatively, and is not in doubt: the product family emerged in the second half
  of the 2000s, grew through the low-interest decade as the guaranteed component of a conventional
  contract shrank towards nothing [R7], became a standard offering across the large and mid-sized
  carriers, and was one of the main vehicles of the ***Neue Klassik*** generation of designs that
  replaced the annually-accruing guarantee with a *Rentenbeginn* guarantee [S6].
- **The rise in interest rates from 2022 and the *Höchstrechnungszins* increase to 1,00 % for 2025
  changed the product's relative position** [R7][R18]: a larger guaranteed component makes the safe
  arm of the *Wahlrecht* more attractive and reduces the pressure that created the product. Whether
  index tariffs have lost share as a result **is not established** `[unverified]`.
- **Carrier inventory.** This author can name, with moderate confidence and tagged `[unverified]`,
  three carriers and product names in this family — **Allianz IndexSelect** [S2], **R+V-IndexInvest**
  [S7] and **Stuttgarter index-safe** [S8] — and is confident, without being able to name products,
  that the family extends across much of the large and mid-sized German market. **The rest of the
  carrier inventory the brief asked for could not be assembled**, and inventing product names would
  have been worse than admitting it. Gap 2.

### 24. What a projection model needs, and what this file supplies

| The model needs | Status | Where it comes from |
|---|---|---|
| Contract chassis (premium, reserve, death benefit, surrender, paid-up, annuitisation) | established | delib product 2, inherited unchanged |
| The payoff formula `max(sum of min(r_m, C), 0) x G` | **established**, structurally certain | section 5 |
| The annual lock-in and the guarantee architecture | **established** | sections 6, 11 |
| The financing identity between surplus and option budget | **established** | section 3 |
| The annual *Wahlrecht* as a policyholder election | **established** as a mechanic | section 4 |
| The Cap level | **not established** — `[std]` 3,00 %, band 1,5–5,0 % | sections 8, 22 |
| The declared surplus rate | **not established** — `[std]` 2,50 % | sections 3, 22 |
| The *Garantieniveau* | **not established** — `[std]` 90 % | sections 11, 22 |
| The base `G` of the participation | **not established** — `[std]` whole capital at year start | section 5 |
| The mid-year exit treatment | **not established** — `[std]` no credit in the year of exit | sections 5, 14 |
| Charges, lapse rates, entry age, premium, term | **not established** — all `[std]` | sections 13, 17, 22 |
| A real *Indexjahr* to reproduce | **not established** — constructed | section 19 |

**The design recommendation this research leads to, and the reason it is defensible under these
retrieval conditions.** Because no real *Indexjahr* could be obtained, the delib model should not
model the index credit as an assumed rate. It should **implement the contractual formula literally,
against an explicit table of monthly index returns supplied as an external CSV** beside the model,
one row per projection year and twelve columns of monthly returns, with the `provenance` column
recording the path as `[std]`. The annual-step model then reads twelve monthly returns per year,
caps each at `C`, sums them, floors at zero, and credits. That way:

- the mechanic — the thing this product **is** — is reproduced exactly rather than approximated;
- the worked example of section 19 becomes the model's anchor cell and is asserted cell by cell;
- the pitfall in Example B (index up, credit zero) becomes a test rather than a remark;
- every unestablished level stays a visible `[std]` parameter rather than being buried in an assumed
  credit rate;
- and the volatility sensitivity of section 20 is demonstrable by swapping the CSV.

This is the strongest thing a research file written with no research channel can hand downstream: not
a set of numbers it could not obtain, but the exact arithmetic the numbers would have gone into.

---

## Observed variation across insurers

**An honest variations table for this product is almost entirely a record of what could not be
compared.** No carrier document was retrieved and no search corroborated any carrier-level term, so
there is no per-insurer evidence to tabulate. What follows is therefore the *structure* of the
comparison a later researcher must fill in, with the delib `[std]` in the last column, and the
parameter bands from section 22 restated as ranges.

| Feature to compare | Allianz [S2][S3][S4][S5] | R+V [S7] | Die Stuttgarter [S8] | Anyone else | delib `[std]` |
|---|---|---|---|---|---|
| Index AVB located | no | no | no | no | composite [S1] |
| Product name | IndexSelect `[unverified]` | IndexInvest `[unverified]` | index-safe `[unverified]` | not established | n/a |
| Payoff design (Cap / Quote / both) | not established | not established | not established | not established | Cap, Quote as variant |
| Cap level, any year | **not established** | **not established** | **not established** | **not established** | 3.00 % monthly |
| *Mindest-Cap* guaranteed | not established | not established | not established | not established | none |
| Underlying index | not established | not established | not established | not established | generic, by volatility |
| *Wahlrecht* notice period | not established | not established | not established | not established | annual, at year end |
| Cap announced before the election deadline | not established | not established | not established | not established | assumed yes |
| Base `G` of the participation | not established | not established | not established | not established | whole capital |
| *Garantieniveau* choices | not established | not established | not established | not established | 90 % |
| Mid-year exit treatment | not established | not established | not established | not established | no credit |
| Charges / *Effektivkosten* | not established | not established | not established | not established | `[std]`, section 13 |

Parameter bands, restated — every one `[unverified]`, and the reason section 22 exists:

| Parameter | Band | Who sits where |
|---|---|---|
| Monthly Cap | 1.5 % – 5.0 %, typically 2.5 % – 4.0 % | **no carrier placed** |
| *Partizipationsquote* | 50 % – 80 % on an equity price index; 80 % – 120 % on a house index | **no carrier placed** |
| *Garantieniveau* | 60 % / 80 % / 90 % / 100 % of premiums | 100 % statutory for *Riester* [R12]; otherwise not placed |
| Declared surplus rate 2026 | of the order of 2.5 % – 2.7 % | market averages via the sibling file's [R20] |
| *Höchstrechnungszins* by cohort | 0.25 % – 4.00 %, 1.00 % for 2025–2026 | market-wide [R7][R18] |
| Underlying | EURO STOXX 50 historically; house multi-asset indices increasingly | **no carrier placed** [R21] |

**Representative design the research supports.** A single-life *Schicht 3* deferred annuity, capital
in the *Sicherungsvermögen*, guaranteed at the 1,00 % *Höchstrechnungszins* with a **90 %
*Beitragsgarantie* falling due at *Rentenbeginn*** and no annually accruing guarantee beyond the
technical rate; the annually declared *Überschuss* spent, at the policyholder's **annual election**,
as an **option budget** buying a one-year index participation; the credit computed as the **sum of
twelve monthly index returns each capped at a monthly Cap, with negative months entering in full,
floored at zero**, applied to the accumulated capital at the start of the *Indexjahr*; the credit
**locked in permanently** into the guaranteed capital; a *Partizipationsquote* design available as a
switchable variant; conversion at *Rentenbeginn* at the **greater of the guaranteed and the current
*Rentenfaktor***; *Rückkaufswert* and *Beitragsfreistellung* on the ordinary § 169 / § 165 VVG
footing, with **no index credit in the year of exit**. Every level in that design is `[std]` and is
listed in section 22.

---

## Gaps and caveats

This register is not a formality. Under the retrieval conditions stated at the head of the file it
is a substantial part of the document's value, and it is written so that a later researcher with a
working network knows exactly what to go and get, and in what order.

1. **No carrier *Bedingungswerk* for an index tariff was obtained, and that is the file's central
   defect.** The AVB is the document that settles the *Indexjahr* definition, the observation dates,
   the payoff formula's exact wording, the base of the participation, the *Wahlrecht* timing, the
   *Cap-Festlegung* clause, the *Mindest-Cap* if any, the *Lock-in* clause and the *Ersatzindex*
   clause [S2]. Everything this file says about those is written from knowledge of the design family,
   not from a document. **Get one AVB and half of this register closes.**

2. **The carrier and product-name inventory could not be assembled.** The brief named twenty-six
   German carriers. This file can name three products with moderate confidence — Allianz IndexSelect,
   R+V-IndexInvest, Stuttgarter index-safe — **all tagged `[unverified]`**, and cannot say for any
   other named carrier whether it writes the product at all. No downstream document may present any
   of the three as established, and none may add a fourth.

3. **No cap level, for any insurer, in any year, was established.** Not one. The range quoted
   throughout (1,5 %–5,0 %, typically 2,5 %–4,0 %) is this author's recollection of the market band
   and is `[unverified]`; the delib 3,00 % is `[std]`. The documents that carry real cap levels are
   the annual customer notification [S5], the *Standmitteilung* [S10] and the rating-house
   compilations [R21], none of which was reachable.

4. **No documented worked *Indexjahr* was found** — no *Standmitteilung*, no insurer illustration, no
   consumer-press example with twelve monthly index movements and a resulting credit. The brief
   identified this as the gold document and it is absent. The two examples in section 19 are
   **constructed** and are labelled `[std]` in every cell.

5. **The commercial envelope is entirely `[std]`.** No entry-age band, minimum premium, term band,
   maximum sum, *Garantieniveau* menu or *Rentenfaktor* level was established for any carrier,
   because no *Produktinformationsblatt* was located [S3][S11].

6. **No charge level of any kind was established**, and no PRIIP *Basisinformationsblatt* was located
   [S4]. Every charge in delib is `[std]`. The index-specific give-ups — the option dealing spread
   inside the Cap, the index-level fee inside a house index, the volatility-target drag — are
   **structurally invisible in any disclosure**, which is a finding rather than a gap, but their
   magnitude is a gap.

7. **The AltZertG *Produktinformationsblatt* with the *Chancen-Risiko-Klasse* was not located**
   [S11][R12]. This is the most frustrating single absence, because it is the German market's one
   standardised, mandatory, comparable disclosure, and for a *Basisrente* index variant it would have
   supplied cost quota, projected benefits and risk class on one page.

8. **There is no market-size figure for the index-participation segment, and probably none exists.**
   GDV counts these contracts within conventional annuity business [R15][R19]. Any statement in delib
   about how large the segment is, or how it has moved, is `[unverified]`.

9. **Participation-rate levels are `[unverified]` throughout.** The 50–80 % band on an equity price
   index and the 80–120 % band on a house index are this author's assessment, not an observation.

10. **No carrier is established as guaranteeing a *Mindest-Cap*, and none as guaranteeing a minimum
    option budget.** These are different promises — the first bounds the Cap given a budget, the
    second bounds the budget — and the difference matters, because a *Mindest-Cap* is worthless in a
    year in which no surplus is declared [R1][R8]. delib assumes neither.

11. **The *Wahlrecht*'s notice period, and whether the Cap is announced before the election deadline,
    are both unestablished.** The second is the more important: it decides whether the annual election
    is informed or blind, and therefore whether the *Wahlrecht* is worth anything. delib assumes the
    Cap is known at election time and flags the assumption in the technical notes.

12. **The mid-year exit treatment is unestablished** — whether surrender, death or annuitisation
    inside an *Indexjahr* attracts a pro-rata credit, a refund of the unspent option budget, or
    nothing [R2]. delib's `[std]` is nothing. This is a real cash-flow difference and it interacts
    with the lapse-timing incentive noted in section 14.

13. **How German carriers discharge § 154 VVG (*Modellrechnung*) for this product is unestablished**
    [R5]. The prescribed three-interest-rate model does not map onto a payoff whose relationship to
    the interest assumption runs through the option budget and the Cap.

14. **The DAV's PRIIP Category 4 *Standardverfahren* was not obtained** [R11], so nothing can be said
    about how the disclosed performance scenarios of a German Indexpolice are actually computed.

15. **Whether BaFin's conduct *Merkblatt* addresses index products specifically is unestablished**
    [R16][R17]. The product is plainly within scope; whether the supervisor has said anything about
    the cap mechanic is not known.

16. **No German court decision on the *Cap-Festlegung* is known to this author and none was
    established** [R22]. The § 315 BGB framing in section 8 is doctrinally sound but untested in the
    sources available here. Likewise, no decision on an *Ersatzindex* substitution.

17. **Whether index participation is ever offered in the *Rentenphase* is unestablished.** delib
    assumes it is not, and that the *Wahlrecht* lapses at *Rentenbeginn*.

18. **The observation convention is unestablished** — calendar month-ends versus monthly recurrences
    of the *Indexstichtag*, closing levels versus averages. An averaging (Asian) reading materially
    changes the effective volatility and therefore the fair Cap, so this is not a detail.

19. **The base `G` of the participation is unestablished** — whole *Deckungskapital*, an
    index-participating sub-account, or the accumulated *Überschussguthaben* alone. delib takes the
    whole capital as `[std]`; a different reading rescales every credit in the model.

20. **A within-year monthly *Höchststandsicherung* is not established for any German carrier** and
    should not be assumed. delib implements the annual lock-in only.

21. **No house multi-asset index is named in this file.** The shift away from the EURO STOXX 50 is
    described qualitatively in section 9 and is not in doubt as a market development; no specific
    index name, rulebook, volatility target or fee level is asserted, because none could be
    established and a wrong name would be worse than none.

22. **The *Ersatzindex* clause's mechanics are unestablished** — whether a *Treuhänder* must confirm
    a substitution, and whether the policyholder gets a *Sonderkündigungsrecht* or an unscheduled
    right to move to the *sichere Verzinsung* [R4][R10 discussion in section 10].

23. **Nothing in this file is quoted.** There is no verbatim statutory or contractual wording
    anywhere in it, because no document was opened and no search summary was available to attribute
    one to. Every description of a statute or a clause is a paraphrase from this author's knowledge,
    and every paragraph number is `[unverified]`. That is a weaker evidentiary position than either
    sibling delib research file, and materially weaker than any frlib file.

24. **Living texts.** The VVG, the DeckRV, the MindZV, the VAG, the AltZertG, the EStG and the PRIIPs
    delegated regulation all change. The *Höchstrechnungszins* is reset by regulation and was last
    moved, on the evidence of the sibling delib files, to 1,00 % with effect from 1 January 2025 and
    confirmed for 2026 [R7][R18]. Every date, rate and paragraph number in this file must be
    re-checked against the instrument before it is relied on. **A delib citation is a pointer, not a
    certificate.**
