# Basisrente (Rürup-Rente), Schicht 1 — research notes (Germany)

Research notes for the German **Basisrente** — the *Basisrentenvertrag* of § 10 Abs. 1 Nr. 2
Buchstabe b EStG, created by the *Alterseinkünftegesetz* of 2004 and sold under the popular name
*Rürup-Rente* after Bert Rürup, who chaired the commission that proposed it. It is the first layer
(*Schicht 1*) of the German three-layer retirement architecture: a privately written, funded,
individually owned contract that is nevertheless treated for tax purposes like the *gesetzliche
Rentenversicherung* — contributions deductible as *Sonderausgaben* on the way in, benefits taxed
as *sonstige Einkünfte* on the way out, at a *Besteuerungsanteil* fixed by the cohort year of
*Rentenbeginn*.

**The product is defined by prohibitions, not by benefits.** Its accumulation and payout mechanics
are those of an ordinary German deferred annuity — the same *Deckungskapital* recursion, the same
*Überschussbeteiligung*, the same *Rentenfaktor*, the same DAV 2004 R basis as the delib
`klassische_rentenversicherung` product. What makes it a distinct product, and what a projection
model has to get right, is a closed list of things it may **not** do: the entitlement may not be
inherited, transferred, charged as security, sold or turned into capital, and no *Rückkaufswert*
may be paid on termination. Everything else in this file follows from that sentence.

**In scope.** The individual, privately written *Basisrentenvertrag (Alter)* on a single life
against a *laufender Beitrag*, a *Zuzahlung* or a *Einmalbeitrag*, certified under § 5a AltZertG,
in all three of its asset forms — *klassisch* (general account), *fondsgebunden* (unit-linked) and
*fondsgebunden mit Beitragsgarantie* (hybrid) — together with the two riders the statute permits
inside the same contract: *Hinterbliebenenabsicherung* and *Berufsunfähigkeits-Zusatzversicherung*.

**Out of scope, and said so where it matters.**

- **The other two layers.** *Riester-Rente* (Schicht 2, delib product 6) shares the AltZertG
  certification regime but has a different subsidy (*Zulage* plus § 10a EStG), a mandatory
  *Beitragserhaltungsgarantie*, a permitted 30 % *Teilkapitalauszahlung* and a *Kleinbetragsrenten*
  commutation — four things the Basisrente does not have. *Klassische private Rentenversicherung*
  (Schicht 3, delib product 2) has the same chassis with none of the constraints: full
  *Kapitalwahlrecht*, a *Rückkaufswert*, free beneficiary designation, and *Ertragsanteil* taxation.
  Both are separate delib products and are referenced here only as contrasts.
- **The competing Schicht-1 vehicles.** The *gesetzliche Rentenversicherung*, the
  *berufsständische Versorgungswerke* and the *landwirtschaftliche Alterskasse* sit in
  § 10 Abs. 1 Nr. 2 **Buchstabe a** EStG and share the **same annual *Höchstbetrag*** as the
  Basisrente. They are not modelled, but the shared ceiling is a first-order fact about the product
  and is treated in mechanic 6.
- **The *Fonds-Basisrente*.** A Basisrentenvertrag may also be written by a
  *Kapitalverwaltungsgesellschaft* as a fund savings plan whose payout phase is bought in from a
  life insurer. It meets the same § 10 and § 5a AltZertG tests and competes for the same buyer, but
  its accumulation phase is not an insurance liability and delib does not model it.
- **Betriebliche Altersversorgung** in all five *Durchführungswege*, *Gruppenversicherung*, *private
  Krankenversicherung* and *Sterbegeldversicherung* are outside the delib library entirely.
- Austrian and Swiss documents are excluded even where a search would return them: the EStG, the
  AltZertG and the DeckRV do not apply to them.

These notes are the **citation ground truth** for the delib `basisrente` product documents. Source
ids **S1..S16** and **R1..R24** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this before reading anything else in the file. It is what separates a delib citation from an
frlib one.

**No document in this file was retrieved.** Direct HTTP egress from this build environment is
blocked by an organisation network policy. `WebFetch` and `curl` are refused at the egress gateway
for every host outside a short package-registry allowlist. The hosts that matter for this product
were tried again while writing this file and every one of them was refused with the identical
error — `curl: (56) CONNECT tunnel failed, response 403`:

| Host | What it holds for this product | Result |
|---|---|---|
| `gesetze-im-internet.de` | EStG § 10, § 22; AltZertG; ZPO § 851c; VVG; DeckRV | 403 at the gateway |
| `bafin.de` | supervisory material, *Merkblätter*, statistics | 403 at the gateway |
| `gdv.de` | *Musterbedingungen*, market statistics | 403 at the gateway |
| `de.wikipedia.org` | the encyclopaedic overview | 403 at the gateway |
| `aktuar.de` | DAV, *Höchstrechnungszins*, DAV 2004 R | 403 at the gateway |
| `bundesfinanzministerium.de` | BMF-Schreiben, *Sonderausgabenabzug* guidance | 403 at the gateway |
| `bzst.de` | the certifying authority for Basisrentenverträge | 403 at the gateway |

Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not
one statutory text, not one BMF-Schreiben and not one insurer *Verbraucherinformation* was opened.

**There was also no search channel.** The session's `WebSearch` budget — a hard cap of 200 calls
shared across all delib work — was **exhausted before this product was reached**. The two delib
research files written earlier (`kapitallebensversicherung.md`, `klassische_rentenversicherung.md`)
consumed it. This file was therefore written with **no research channel of any kind**: no fetch, no
search, no snippet, no summary. That is a materially weaker evidential position than either sibling
file, and it is stated on every source entry rather than glossed.

What follows from that, exactly, and it is applied without exception below:

1. **Every source entry carries the honest retrieval line.** The standard line in this file is
   `Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)`. A
   small number of entries carry a stronger line because their **identity** was established in a
   sibling delib research file while search was still available; those say so and name the file.
   **`Retrieved: yes` appears nowhere in this document.**
2. **Nothing is quoted.** Not one sentence of German statutory or contractual wording appears here
   in quotation marks as though it were read. Where the substance of a provision is given, it is
   given in English, in this file's own words, as *what the provision does*. A reader who needs the
   wording must go to the instrument.
3. **No URL, document number, edition, page count or publication date is invented.** Where a
   canonical `gesetze-im-internet.de` form is obvious — `.../estg/__10.html` for § 10 EStG — it is
   offered and marked `[unverified]`. Everywhere else the entry says `URL: not established`. No
   *Bundesgesetzblatt* citation and no BMF-Schreiben file number appears anywhere in this file,
   because none could be confirmed.
4. **`[unverified]` is used generously and means what it always means.** Every specific paragraph
   number, every effective date, every monetary amount, every percentage and every market figure in
   this file carries it, because no search result confirmed any of them. The general *shape* of a
   well-established mechanic — that a Basisrente cannot be surrendered, that contributions are
   deductible, that the annuity is taxed on a cohort percentage — is not tagged, because tagging it
   would drown the signal. **The moment a claim becomes specific and numeric, it is tagged.**
5. **Uncertain numbers became `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — a charge, a *Rentenfaktor*, a *Beitragsfreistellung* rate, a market share —
   this file ships a `[std]` value with a stated rationale and an argued plausible range rather than
   a fabricated source tag. A `[std]` number is honest. A guessed `[S4]` number is not.
6. **The weight of the file is in the mechanics.** Sections 1 to 22 below are the part that does not
   depend on having a PDF open, and they are written long and precise. The source blocks are
   correspondingly short: they name the documents a checker must go to, and they say plainly what
   they do and do not establish.

**A delib citation is a pointer, not a certificate.** An `[R1]` tag on a sentence about
§ 10 Abs. 1 Nr. 2 Buchst. b EStG means *this is the instrument this claim must be checked against*.
It does not mean anyone read it. Downstream documents must not upgrade that.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Basisrente*, *Rürup-Rente*, *Basisrentenvertrag* | The Schicht-1 private pension of § 10 Abs. 1 Nr. 2 Buchst. b EStG. "Rürup" is a market nickname; the statute and the certifying authority say *Basisrentenvertrag* |
| *Schicht 1 / 2 / 3* | The three layers of German retirement provision: basic (GRV, Versorgungswerk, Basisrente); subsidised supplementary (Riester, bAV); unsubsidised private |
| *Alterseinkünftegesetz* (AltEinkG) | The 2004 statute that created the layer architecture, the *nachgelagerte Besteuerung* and the Basisrente |
| *Nachgelagerte Besteuerung* | Deferred taxation: relief on contributions, tax on benefits — the design principle of Schicht 1 |
| *Sonderausgabenabzug* | Deduction of contributions from taxable income as *Sonderausgaben* under § 10 EStG |
| *Höchstbetrag* | The annual ceiling on deductible Schicht-1 contributions, pegged to the maximum contribution to the *knappschaftliche Rentenversicherung* |
| *Beitragsbemessungsgrenze* (BBG) | Contribution assessment ceiling of a social-insurance branch; the *knappschaftliche* BBG is what the *Höchstbetrag* tracks |
| *Knappschaftliche Rentenversicherung* | The miners' branch of the statutory pension scheme, with its own higher BBG and higher contribution rate |
| *Besteuerungsanteil* | The percentage of the annuity that is taxable, fixed by the calendar year of *Rentenbeginn* and constant for life |
| *Rentenfreibetrag* | The euro complement of the *Besteuerungsanteil*, frozen in the year after *Rentenbeginn* and never re-indexed |
| *Ertragsanteil* | The much lower taxable fraction applied to Schicht-3 annuities under § 22 EStG — the comparator, not this product's rule |
| *Kohortenprinzip* | The cohort principle: the taxable share depends on the year the annuity starts, not on the taxpayer |
| *Vererblichkeit*, *Übertragbarkeit*, *Beleihbarkeit*, *Veräußerbarkeit*, *Kapitalisierbarkeit* | The five properties a Basisrente entitlement must **not** have |
| *Hinterbliebenenabsicherung* | Survivor cover; permitted only for the spouse or registered partner and for children while *Kindergeld* runs |
| *Kindergeldberechtigung* | Entitlement to child benefit; the statutory test that defines an eligible child beneficiary |
| *Beitragsrückgewähr* | Return of contributions on death; in Schicht 1 it can only fund a survivor's annuity, never a lump sum |
| *Rentengarantiezeit* | Guaranteed payment period after *Rentenbeginn*; in Schicht 1 payable only to permitted survivors |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | Occupational-disability rider written inside the main contract |
| *Berufsunfähigkeit* / *verminderte Erwerbsfähigkeit* | Occupational disability / reduced earning capacity — the two disability risks the statute permits inside a Basisrente |
| *Beitragsfreistellung* | Making the contract paid-up; the Basisrente's only exit |
| *Kündigung* / *Rückkaufswert* | Termination / surrender value — both effectively unavailable on this product |
| *Zuzahlung* / *Einmalbeitrag* | A one-off top-up into an existing contract / a single-premium contract |
| *Beitragsdynamik* | Contractual annual premium escalation |
| *Rentenbeginn* | Vesting date; the boundary at which the accumulated capital becomes an annuity |
| *Aufschubphase* / *Rentenphase*, *Rentenbezugsphase* | Deferment (accumulation) phase / payout phase |
| *Rentenfaktor* | Monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *Deckungskapital* / *Deckungsrückstellung* | The actuarial reserve of one contract / the balance-sheet provision covering it |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business |
| *Überschussbeteiligung* / *Schlussüberschussanteil* | Participation in surplus / terminal bonus |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs into the reserve / the statutory cap on the amount so financed |
| *Effektivkosten* | Reduction in yield: the annualised return give-up caused by all charges, disclosed on the *Produktinformationsblatt* |
| *Chancen-Risiko-Klasse* (CRK) | The standardised risk class shown on the *Produktinformationsblatt* |
| *Pfändungsschutz* | Protection from attachment by creditors; § 851c ZPO for this product |
| *Zertifizierung* | Certification of the contract by the *Bundeszentralamt für Steuern* under AltZertG |
| *Produktinformationsblatt* (PIB) | The standardised pre-sale document required for certified contracts |
| *Basisinformationsblatt* (BIB) | The PRIIP key information document |
| *Versorgungsausgleich* | Pension rights sharing on divorce — the one transfer the statute permits |
| *Kleinbetragsrente* | A trivially small annuity; commutable in Schicht 2, **not** in Schicht 1 |

---

## Primary sources

Every entry below carries the same retrieval status unless it says otherwise, stated once here
rather than repeated sixteen times: **Retrieved: no — egress blocked; no search corroboration
(session search budget exhausted).** Nothing in this section is quoted from a document. Where an
entry establishes something, it says what and from where; where it establishes nothing beyond the
document's existence and kind, it says that too, which is the honest majority case in this file.

Two entries — [S1] and [S2] — are stronger than the rest, because their **identity** was
established by search in a sibling delib research file while the budget was still available. They
are the only carrier-level Basisrente artefacts anywhere in the delib corpus, and they are the two
entries a checker should verify first.

### S1 — Cosmos Lebensversicherungs-AG (CosmosDirekt), *Allgemeine Bedingungen* for the Basisrente — tariffs **LA 1100 A** and **LA 1079 A / LA 936 A / LA 1099 A**
- Publisher: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland
- Doc type: *Allgemeine Versicherungsbedingungen* (AVB) for Basisrente tariffs, in the carrier's
  `LA nnnn A` house numbering
- URL: not established. The carrier's sibling Schicht-3 wording **LA 904 A** was returned at
  `https://www.cosmosdirekt.de/resource/blob/89106/…/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf`,
  so the Basisrente wordings are expected to sit under the same `resource/blob` scheme; **no blob
  path for a Basisrente wording was returned and none is guessed**
- Retrieved: no — egress blocked; **no search corroboration in this file (budget exhausted)**;
  document identity carried over from the sibling delib research file
  `_research/klassische_rentenversicherung.md` [S8], which established the carrier's tariff-number
  list from a search-result summary while search was still available
- Content:
  - **Four tariff codes are attributed to the Basisrente** in the carrier's own numbering —
    **LA 1100 A**, **LA 1079 A**, **LA 936 A**, **LA 1099 A** — against LA 1005 A (Riester),
    LA 1311 A (unit-linked *FlexInvest*), LA 1081 A (*Direktversicherung*) and LA 904 A / LA 1201 A
    / LA 1204 A (Schicht-3 annuity). This is the single most useful structural fact the corpus
    yields about the product's market form: **one direct writer maintains at least four parallel
    Basisrente wordings**, which is what a tariff family looks like when *klassisch*, *fondsgebunden*
    and vintage editions coexist.
  - **No edition date, no page count and no clause text was established** for any of the four. The
    numbers themselves are the whole of what this entry supports.
  - The carrier's Schicht-3 sibling LA 904 A establishes the house's conversion convention — the
    *garantierter Rentenfaktor* fixed at inception on **DAV 2004 R** and, at that document's
    vintage, an interest basis of **0 % p.a.** [R17] — and that convention is almost certainly
    shared with the Basisrente wordings, **but the inference is not evidence** and is `[unverified]`
    as a Basisrente fact (gap 4).

### S2 — Allianz Lebensversicherungs-AG, **BasisRente KomfortDynamik** — specimen *persönlicher Vorschlag*
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: a distributed specimen quotation ("Berechnung BasisRente KomfortDyn"), hosted by a
  broker rather than by the carrier, dated by its path to **February 2025** `[unverified]`; together
  with the Allianz *Vorsorgekonzept KomfortDynamik* product page
- URL: page `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`; the specimen at
  `privat.rh-insuranceservices.com/wp-content/uploads/2025/02/Berechnung-BasisRente-KomfortDyn.pdf`
- Retrieved: no — egress blocked; **no search corroboration in this file (budget exhausted)**;
  identity and the two figures below carried over from
  `_research/klassische_rentenversicherung.md` [S13]
- Content — **the only Basisrente-specific charge evidence in the delib corpus**:
  - The **BasisRente is a variant of the KomfortDynamik chassis**, not a separate product line: the
    same design is sold as PrivatRente (Schicht 3), BasisRente (Schicht 1) and RiesterRente
    (Schicht 2). That is the German market's normal arrangement and it is worth stating plainly —
    **the layer is a wrapper around a common chassis**, and an insurer's Basisrente shares its
    fund range, its guarantee mechanics and its *Rentenfaktor* machinery with its Schicht-3 sibling.
  - The chassis: premiums **split between the Allianz *Sicherungsvermögen* and a *Spezialfonds***;
    selectable guarantee levels of **60 %, 80 % or 90 % of premiums paid** at *Rentenbeginn*, 80 %
    standard `[unverified]`; at inception the customer is given only the premium-retention level and
    a **minimum annuity** — a *garantierter Rentenfaktor* expressed as an amount.
  - Two charge figures were returned by third-party commentary in the same result set: an
    **Abschlussprovision of 1 575 €** on the specimen quotation, and, **in the BasisRente and
    RiesterRente variants, total costs relative to the capital formed of at most 0,95 € per 100 €**
    `[unverified]`. Both come from third-party analyses rather than an Allianz tariff sheet. The
    second is the more useful: expressed as a reduction-in-yield-like ratio it is of the order of
    **0,95 %** of the capital formed, which is consistent with the *Effektivkosten* band a
    *Produktinformationsblatt* would show for a hybrid Basisrente [S13], and it is the only number
    in this file that behaves like a charge level rather than a guess.

### S3 — Allianz Lebensversicherungs-AG, the **BasisRente** product family
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: AVB, *Produktinformationsblätter* and *Verbraucherinformationen* for the carrier's
  Basisrente tariffs — marketed as **BasisRente Klassik**, **BasisRente Perspektive** (the
  "Neue Klassik" design) and **BasisRente InvestFlex** (unit-linked) `[unverified]` as to the exact
  current line-up
- URL: not established
- Content: **nothing established beyond the family's existence and the market position of its
  publisher.** Named here because Allianz is the largest German life writer and its Basisrente
  wordings are the single most consequential set of primary documents this file could not reach.
  Any downstream statement about Allianz Basisrente terms must be sourced to [S2] or dropped.

### S4 — Alte Leipziger Lebensversicherung a. G., **AL_RoyalBasisRente** (Klassik and Fonds)
- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: AVB, *Produktinformationsblatt*, *Verbraucherinformation*
- URL: not established
- Content: **nothing established beyond existence.** Alte Leipziger is one of the carriers most
  consistently placed at the top of independent Basisrente ratings [R24] and is the natural first
  target for a checker with a working network. Product names are `[unverified]`.

### S5 — NÜRNBERGER Lebensversicherung AG, **Basis-Rente** with **Berufsunfähigkeits-Zusatzversicherung**
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for the Basisrente main contract and separate AVB for the BUZ rider
- URL: not established. The carrier's Schicht-3 wordings were returned in a sibling delib file under
  `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` and siblings `gn331530_p`,
  `gn331303_p`, so its Basisrente wordings sit in the same `4allportal` document scheme; **no
  Basisrente document id was returned and none is guessed**
- Retrieved: no — egress blocked; no search corroboration; the `4allportal` scheme carried over from
  `_research/klassische_rentenversicherung.md` [S9]
- Content: **nothing established beyond existence and the document scheme.** Named because
  NÜRNBERGER is one of the German market's principal *Berufsunfähigkeit* writers and therefore the
  natural place to look for a **BUZ written inside a Basisrente** and for the 50 % *Beitragsanteil*
  constraint expressed in contractual terms (mechanic 13). That wording is the single most valuable
  document this file could not reach.

### S6 — Volkswohl Bund Lebensversicherung a. G., **Basisrente**
- Publisher: Volkswohl Bund Lebensversicherung a. G., Dortmund
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** Named because Volkswohl Bund is a
  broker-channel carrier with a large Basisrente book and is repeatedly named in rating
  commentary [R24]; the broker channel is where this product is predominantly sold (mechanic 21).

### S7 — LV 1871 (Lebensversicherung von 1871 a. G.), Basisrente
- Publisher: Lebensversicherung von 1871 a. G., München
- Doc type: AVB, *Produktinformationsblatt*. Marketed under the names **Golden Basic** and
  **MeinPlan Basis** `[unverified]`
- URL: not established
- Content: **nothing established beyond existence.** Named because LV 1871's Basisrente is the
  market's best-known example of a **fondsgebundene Basisrente with an open fund and ETF universe
  and no *Beitragsgarantie*** `[unverified]` — the form mechanic 9 argues is the commercial default
  of the modern Schicht-1 market, and therefore the form a checker should verify first.

### S8 — Swiss Life Deutschland, Basisrente (**Swiss Life Maximo** family)
- Publisher: Swiss Life AG, Niederlassung für Deutschland
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** Named because Swiss Life is a large
  broker-channel Schicht-1 writer and because its *Maximo* line is a hybrid with a selectable
  guarantee level, i.e. the third of the three asset forms in mechanic 9. Product name
  `[unverified]`.

### S9 — Continentale Lebensversicherung AG, Basisrente (**Rente Invest Basis** family)
- Publisher: Continentale Lebensversicherung AG, Dortmund
- Doc type: AVB, *Produktinformationsblatt*
- URL: not established
- Content: **nothing established beyond existence.** Product name `[unverified]`.

### S10 — Stuttgarter Lebensversicherung a. G., Basisrente
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB, *Produktinformationsblatt*. Marketed in *performance-safe* and *index-safe*
  variants `[unverified]`
- URL: not established
- Content: **nothing established beyond existence.** Named because the *index-safe* variant, if the
  name is right, would be an **index-linked Basisrente** — a fourth asset form beyond the three of
  mechanic 9, and a bridge to delib product 4 (`indexpolice`). That this could not be checked is
  gap 12.

### S11 — The carriers for which nothing whatever was established
- Publishers: **Debeka**, **R+V**, **HDI**, **Gothaer**, **Zurich Deutscher Herold**, **ERGO**,
  **AXA**, **Generali / Dialog**, **Barmenia**, **Universa**, **Württembergische**,
  **Signal Iduna**, **Baloise**, **DEVK**, **Provinzial**, **HUK-Coburg**, **Hannoversche**,
  **CosmosDirekt** (beyond [S1]), **die Bayerische**, **Condor**
- Doc type: each of these carriers writes, or has written, a Basisrente and therefore publishes AVB,
  a *Produktinformationsblatt* and a *Verbraucherinformation* for it
- URL: not established for any of them
- Content: **nothing.** This entry exists so that the corpus's coverage is stated as a fact rather
  than implied by omission: **twenty named German life writers whose Basisrente documents exist were
  not reached, and not one of them contributes a single fact to this file.** Naming them without
  attaching claims is the honest form. See gap 1.

### S12 — GDV, *Musterbedingungen* service index
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: the association's index of model conditions
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` — established in a sibling delib file
- Retrieved: no — egress blocked; index URL carried over from
  `_research/klassische_rentenversicherung.md` [S3]
- Content: the GDV publishes *Musterbedingungen* for the deferred annuity and for the
  *Riester* annuity (a sibling model condition set carrying "Stand: 21.07.2025" was seen in that
  file). **Whether the GDV publishes a Basisrente model condition set at all was not established**
  and must not be assumed (gap 5). Two things about GDV model conditions carry over regardless and
  matter for how any such document would be weighted: they are expressly **unverbindlich** and their
  use by member undertakings is **optional**, so a GDV-tagged fact is evidence about a market
  template and weaker evidence about any particular carrier.

### S13 — *Produktinformationsblatt* under § 7 AltZertG (the standardised PIB)
- Publisher: each provider, on a form and a computational method prescribed by law and administered
  by the **Produktinformationsstelle Altersvorsorge gGmbH (PIA)**, Kaiserslautern
- Doc type: the mandatory two-page pre-sale document for a certified Basisrentenvertrag
- URL: not established (there is no single URL; every provider publishes its own, per tariff and per
  model point)
- Content — **the document type a delib reader must understand even though none was opened**:
  - It is **product-specific and quotation-specific**: the figures on it are computed for the
    prospect's own age, term and contribution, not for the tariff in the abstract.
  - It carries the three standardised comparators the German legislator built for this layer: the
    ***Effektivkosten*** (reduction in yield — the annualised return give-up caused by all charges),
    the ***Chancen-Risiko-Klasse*** (a standardised risk class computed by PIA on a common
    capital-market model), and a set of **standardised projection scenarios** `[unverified]` as to
    the exact current field list.
  - It is the **only public document in the German market that states a Basisrente's total charge
    burden as a single comparable number.** That is why gap 2 — that not one PIB was reached — is
    the most consequential gap in this file: every charge parameter downstream is `[std]`.

### S14 — *Basisinformationsblatt* (PRIIP key information document)
- Publisher: each provider
- Doc type: the PRIIPs KID for an insurance-based investment product
- URL: not established
- Content: **the document type exists for unit-linked and hybrid Basisrenten.** It carries a
  summary risk indicator, performance scenarios and a cost table split into one-off, ongoing and
  incidental costs, with *reduction in yield* figures at several holding periods. **How the PRIIPs
  KID and the § 7 AltZertG *Produktinformationsblatt* interact for a certified Basisrentenvertrag —
  whether both are required, or one substitutes for the other — was not established and is gap 6.**
  Nothing downstream may assert either arrangement.

### S15 — Annual statement to the policyholder (*jährliche Information*, § 7a AltZertG)
- Publisher: each provider
- Doc type: the statutory annual information for a certified contract
- URL: not established
- Content: the statute requires an annual statement to a Basisrente saver `[unverified]` as to the
  precise paragraph. Its interest for delib is the same as the *Standmitteilung*'s for the endowment
  chassis: it names, side by side, the state variables a projection model must carry — the
  contributions paid in the year, the accumulated value, the guaranteed benefit and the projected
  annuity. **The field list was not established.**

### S16 — Consumer, comparison and rating material
- Publishers: **Finanztip**, **Stiftung Warentest / Finanztest**, the **Verbraucherzentralen**,
  **Verivox**, **CHECK24**, **Handelsblatt**, and the rating houses at [R24]
- Doc type: consumer guides, comparison-portal pages, product ratings — **secondary in every case**,
  and in frlib's convention they would still be S-numbered because they describe the product rather
  than regulate it
- URL: not established for any of them
- Content: **nothing established.** These are the sources that in a normal research session would
  supply price points, market variation and the buyer profile. **None was reached.** Every price
  point, every market share and every buyer-profile statement in this file is therefore either
  general knowledge marked `[unverified]` or a `[std]` construction, and is marked as such at the
  point of use.

---
