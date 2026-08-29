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

## Regulatory and actuarial references

Same retrieval status throughout: **Retrieved: no — egress blocked; no search corroboration
(session search budget exhausted).** The content blocks state what each instrument provides, in
this file's own words, from general knowledge of German law and practice. **They are pointers to be
checked, not readings.** Every paragraph number, date and figure below is `[unverified]` unless the
entry says otherwise, and the register at the foot of the file lists what that leaves open.

### R1 — EStG § 10 Abs. 1 Nr. 2 Buchst. b — the definition of a Basisrentenvertrag
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, `[unverified]`
- Content — **the single most important instrument for this product, and the source of every
  constraint in it**:
  - The provision makes deductible, as *Sonderausgaben*, the taxpayer's own contributions **to
    build a funded old-age provision of the taxpayer's own**, where the contract provides for the
    payment of a **monthly, lifelong annuity on the life of the taxpayer**, not commencing before
    the completion of a stated year of life; and, as permitted supplements, cover against
    **Berufsunfähigkeit**, against **verminderte Erwerbsfähigkeit**, and for **Hinterbliebene**.
  - The **age floor is the completion of the 62nd year of life**, applying to contracts concluded
    **after 31 December 2011**; contracts concluded on or before that date retain the earlier floor
    of the **completion of the 60th year of life** [R8]. `[unverified]` as to both the paragraph
    address and the transition date, but the substance — 62 now, 60 for the older cohort — is a
    settled point of German practice. **It is not 63; see gap 22, which records a contrary
    statement in this file's own commissioning brief and resolves it against 60.**
  - **The five prohibitions.** The entitlements arising under the contract must be **nicht
    vererblich** (not inheritable), **nicht übertragbar** (not transferable), **nicht beleihbar**
    (not chargeable as security or borrowable against), **nicht veräußerbar** (not saleable) and
    **nicht kapitalisierbar** (not convertible into capital). This five-limb sentence is the
    definition of the product. Each limb has a direct modelling consequence and they are worked
    through one at a time in mechanic 3.
  - The permitted *Hinterbliebenenabsicherung* is confined to the **spouse or registered partner**
    and to **children for so long as the taxpayer is entitled to *Kindergeld* or to the
    *Kinderfreibetrag*** in respect of them. No other beneficiary may be named — not a cohabiting
    partner, not a sibling, not an estate. `[unverified]` as to the statutory address; settled as
    substance.
  - The supplementary covers are subject to a **majority test**: the contributions are deductible
    under this provision only if **more than 50 % of the total contribution is attributable to the
    old-age provision**, i.e. the disability and survivor components together must stay **below
    50 %**. `[unverified]` as to whether the test sits in § 10 itself or in the administrative
    guidance at [R18]; the 50 % level itself is settled market practice and is the constraint
    mechanic 13 is built on.

### R2 — EStG § 10 Abs. 3 — the Höchstbetrag, its peg, and the reductions for employees
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, `[unverified]`
- Content:
  - Contributions under § 10 Abs. 1 Nr. 2 — **letters a and b together**, i.e. statutory pension,
    *Versorgungswerk*, *Alterskasse* **and** Basisrente — are deductible up to a **single annual
    *Höchstbetrag***, doubled for spouses assessed jointly.
  - **The ceiling is not a fixed euro figure.** Since 2015 it tracks the **maximum annual
    contribution to the *knappschaftliche Rentenversicherung*** — the miners' branch, which has both
    a higher *Beitragsbemessungsgrenze* and a higher contribution rate than the general branch. The
    ceiling therefore moves every year with the *Sozialversicherungsrechengrößen-Verordnung* [R20],
    which is what makes a Basisrente premium a **naturally indexed** stream (mechanic 7).
  - The arithmetic is `Höchstbetrag = BBG_knappschaftlich(year) × Beitragssatz_knappschaftlich(year)`,
    rounded. The inputs and results are tabulated in mechanic 6; every figure there is
    `[unverified]`.
  - **The deductible percentage.** From 2005 the deductible share of the (capped) contributions rose
    from 60 % by two percentage points a year, and was scheduled to reach 100 % in 2025. The
    **Jahressteuergesetz 2022 brought the 100 % forward to the assessment period 2023** [R7], so
    **for 2023 onwards the capped contribution is deductible in full**. `[unverified]` as to the
    instrument; settled as substance.
  - **The employee reductions, which are what make this a self-employed product.** Two distinct
    mechanisms operate and they must not be conflated:
    1. **Consumption of the ceiling.** An employee's own *and* employer's contributions to the
       *gesetzliche Rentenversicherung* count **against the same ceiling**. A Basisrente contribution
       is deductible only inside whatever headroom is left.
    2. **Subtraction of the tax-free employer share.** The employer's contribution to the GRV is
       already tax-free in the employee's hands, so it is **deducted from the resulting deductible
       amount** rather than being relieved twice. `[unverified]` as to the paragraph; the
       double-mechanism structure is settled.
  - **A third reduction applies to taxpayers with a non-contributory pension entitlement** —
    *Beamte*, judges, soldiers, and controlling shareholder-directors with a *Pensionszusage*. For
    them the ceiling is reduced by a **notional total contribution** to the general statutory scheme
    computed on their remuneration up to the general BBG. `[unverified]` as to the address; settled
    as substance, and it is why a *Beamter* has very little Basisrente headroom.

### R3 — EStG § 10 Abs. 2 and Abs. 2a — certification and data transmission as conditions of relief
- Publisher: Bundesministerium der Justiz / juris
- URL: not established
- Content: the *Sonderausgabenabzug* for a Basisrente is conditional on the contract being
  **certified under the AltZertG** [R9] and on the provider **transmitting the contribution data
  electronically** to the tax administration, which requires the taxpayer's consent. Two
  consequences: an uncertified contract, however economically identical, gets **no relief at all**;
  and the *Zertifizierungsnummer* printed on the *Versicherungsschein* is the operative link between
  the contract and the deduction. `[unverified]` as to the paragraph addresses.

### R4 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. aa — the Besteuerungsanteil
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — canonical form, `[unverified]`
- Content — **the payout-side rule, and the second defining feature of the layer**:
  - Annuities and other benefits from a Basisrentenvertrag, and from the statutory scheme and the
    *Versorgungswerke*, are *sonstige Einkünfte* taxed on a ***Besteuerungsanteil*** — a percentage
    of the annuity fixed by the **calendar year in which the annuity begins**, not by the taxpayer's
    age, income or contribution history. This is the *Kohortenprinzip*.
  - **The complement is frozen in euro.** The untaxed part is computed once, in the **first full
    calendar year of receipt**, as a euro amount — the ***Rentenfreibetrag*** — and then stays at
    that euro amount for life. Every later increase in the annuity is therefore **fully taxable**.
    This is the mechanic most often got wrong and it matters for delib: the model's tax overlay, if
    it ever has one, must freeze an amount, not a percentage.
  - The cohort schedule and its 2058 endpoint are set out in mechanic 15. The schedule's construction
    — 50 % for 2005, rising two points a year to 80 % for 2020, then one point a year, then **half a
    point a year from 2023** after the amendment at [R6] — is settled as substance; **every
    individual percentage in the table is `[unverified]`**.
  - The same provision catches a **Berufsunfähigkeitsrente paid out of a Basisrentenvertrag**, which
    is why a BUZ inside a Basisrente is taxed far more heavily than a standalone *selbständige
    Berufsunfähigkeitsversicherung* (mechanic 13). `[unverified]`, and gap 16.

### R5 — Alterseinkünftegesetz (AltEinkG), 2004
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given, because none could be confirmed.**
- Content: the enabling statute. It responded to the *Bundesverfassungsgericht*'s 2002 decision that
  the unequal taxation of *Beamtenpensionen* and statutory pensions was unconstitutional
  `[unverified]` as to the year and the case, and it did three things at once: it introduced
  ***nachgelagerte Besteuerung*** for the first layer, it built the three-layer architecture, and it
  created the **Basisrente** as the private, funded member of the first layer, so that the
  self-employed — who have no access to the statutory scheme — would have a vehicle with the same
  tax treatment. **Effective 1 January 2005**, which is the boundary that divides the German life
  book into two tax cohorts for every product in delib. The commission whose report it followed was
  chaired by **Bert Rürup**, from which the market name.

### R6 — Wachstumschancengesetz (2024) — the half-point step and the move of the 100 % year to 2058
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Content: the amendment that **reduced the annual increase in the *Besteuerungsanteil* from one
  percentage point to half a percentage point**, with effect from the cohort year **2023**, and
  thereby moved the year in which the *Besteuerungsanteil* first reaches **100 %** from **2040 to
  2058**. It was enacted in **2024** and applied **retrospectively to the 2023 cohort**, which is
  the reason the 2023 figure is **82,5 %** rather than the 83 % the original schedule would have
  given. `[unverified]` as to the instrument's name and date; the substance — the half-point step,
  the retrospective 2023 start and the 2058 endpoint — is settled and is corroborated by simple
  arithmetic on the schedule itself (mechanic 15).
- The motive matters for delib's framing: the change, together with [R7], was the legislator's
  response to the *Doppelbesteuerung* litigation at [R19]. It is a **slowing of the transition, not
  a change of principle**: full *nachgelagerte Besteuerung* is still the destination.

### R7 — Jahressteuergesetz 2022 — the full Sonderausgabenabzug from 2023
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Content: brought forward the **100 % deductibility of Schicht-1 contributions** from the scheduled
  2025 to the assessment period **2023**, two years early. Before it, the deductible share was
  94 % in 2021 and 96 % in 2022 `[unverified]`. Same motive as [R6]: closing the double-taxation
  gap from the contribution side. **For any delib model point written at 2023 or later, the
  deductible share is 100 % of the capped contribution and no phase-in factor is needed** — which
  is a genuine simplification of the product-spec's tax section relative to how it would have had
  to be written five years earlier.

### R8 — Jahressteuergesetz 2007 — the age floor from 60 to 62
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established
- Content: raised the earliest permitted *Rentenbeginn* for a Basisrentenvertrag from the completion
  of the **60th** to the completion of the **62nd** year of life, **for contracts concluded after
  31 December 2011**. The same amendment made the parallel change to the § 20 EStG "12/62" rule for
  Schicht-3 capital payments, which is why 62 appears in two unrelated places in German life tax law.
  `[unverified]` as to the instrument and its year; the **60/62 split at the end of 2011** is settled
  and is the answer to the question the commissioning brief put (gap 22).

### R9 — AltZertG § 5a — certification of Basisrentenverträge
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/altzertg/__5a.html` — canonical form, `[unverified]`
- Content:
  - **§ 5a is the Basisrente's certification provision.** The *Altersvorsorgeverträge-
    Zertifizierungsgesetz* was written for Riester; § 5a was inserted later to bring Basisrenten-
    verträge into the same certification machinery, with effect for contracts concluded from
    **1 January 2010** `[unverified]` as to that date.
  - The certifying authority is the **Bundeszentralamt für Steuern (BZSt)**. Certification is a
    **formal conformity check** — does the contract meet the § 10 Abs. 1 Nr. 2 Buchst. b conditions
    and the AltZertG's own information requirements — and each certified tariff receives a
    *Zertifizierungsnummer*.
  - **What § 5a does not import from § 1 is as important as what it does.** The Riester
    requirements at [R10] — above all the **guarantee that at least the nominal contributions and
    *Zulagen* are available at the start of the payout phase** — **do not apply to a
    Basisrentenvertrag**. That single omission is why a Basisrente may be sold as a pure unit-linked
    contract with no guarantee at all, and it is the most consequential structural difference
    between the two subsidised layers (mechanic 9). `[unverified]` as to the drafting mechanism;
    settled as substance and universally relied on by the market.

### R10 — AltZertG § 1 and § 2 Abs. 2 — what certification is, and the Riester guarantee it does not extend
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/altzertg/__1.html` — canonical form, `[unverified]`
- Content:
  - § 1 lists the conditions a **Riester** *Altersvorsorgevertrag* must satisfy, including the
    **Beitragserhaltungsgarantie** (nominal preservation of contributions and *Zulagen* at the start
    of the payout phase), a payout phase in the form of a lifelong annuity or an instalment plan with
    a subsequent annuity, an **earliest payout age**, and the **spreading of acquisition and
    distribution costs over at least five years** `[unverified]` as to which of these § 5a picks up
    for the Basisrente — and gap 8 records that the five-year spreading question was not resolved.
  - § 2 Abs. 2, or a provision to that effect, states expressly that **certification is not a seal of
    quality**: it says nothing about the economic soundness of the product, the level of its charges,
    or the financial standing of the provider. Downstream documents must repeat that; a
    *Zertifizierungsnummer* on a *Versicherungsschein* is a tax fact, not a value judgement.

### R11 — AltZertG § 7 and the *Produktinformationsstelle Altersvorsorge*
- Publisher: Bundesministerium der Justiz / juris; Produktinformationsstelle Altersvorsorge gGmbH
  (PIA), Kaiserslautern
- URL: `https://www.gesetze-im-internet.de/altzertg/__7.html` — canonical form, `[unverified]`
- Content: the pre-sale information regime for certified contracts. It requires the provider to hand
  over a **standardised *Produktinformationsblatt*** before conclusion [S13], on a common form, so
  that products can be compared across providers and across product types. The **PIA** computes and
  maintains the two standardised comparators — the ***Chancen-Risiko-Klasse*** and the projection
  methodology behind the scenarios — using a common capital-market model, and the provider computes
  the ***Effektivkosten***. **The current statutory field list, the number of risk classes and the
  scenario set were not established** and are gap 7. What is settled and load-bearing for delib is
  that a comparable total-charge figure for this product **exists and is public per quotation**, and
  that delib could not obtain one.

### R12 — ZPO § 851c — Pfändungsschutz bei Altersrenten
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/zpo/__851c.html` — canonical form, `[unverified]`
- Content — **the third leg of the product, alongside the tax relief and the prohibitions**:
  - The provision gives **attachment protection to private pension entitlements** that satisfy a
    set of conditions closely modelled on the § 10 EStG definition: the benefit must be payable
    **periodically and for life**, not before a stated age or on the occurrence of disability; the
    entitlement must **not be disposable**; **third parties may not be named as beneficiaries other
    than survivors**; and **no capital payment other than a death benefit may be agreed**. A
    compliant contract's **income stream is then attachable only on the scale that applies to
    earnings**, i.e. with the *Pfändungsfreigrenzen*.
  - **The age condition in § 851c is the completion of the 60th year of life**, not 62. Because the
    EStG floor for post-2011 contracts is 62, a Basisrente written today **clears the § 851c age
    condition with room to spare**; but the two thresholds are genuinely different provisions with
    different histories and a reader must not assume they were harmonised. `[unverified]` on the 60,
    and gap 10.
  - **A second limb protects the accumulated capital, not merely the income.** The provision allows
    the debtor to have accumulated a capped amount free of attachment, on an **age-graduated annual
    allowance** — a small allowance in the twenties rising in steps to a larger one in the early
    sixties — subject to an **overall ceiling**. **The individual annual allowances and the overall
    ceiling are `[unverified]` and are deliberately not reproduced in this file**: practitioner
    sources give a schedule in six age bands and an overall cap in the low hundreds of thousands of
    euro, and this file could not confirm a single one of those numbers. See gap 9. What is settled,
    and what the product-spec needs, is the **shape**: protection of the fund is capped, the cap is
    age-graduated, and it is not unlimited.
  - **This is the reason the product is sold to the self-employed.** A Schicht-3 annuity with a
    *Rückkaufswert* is realisable and therefore attachable; a Basisrente is not, because there is
    nothing to realise. The protection is a **by-product of the prohibitions**, not an add-on.

### R13 — ZPO § 851d, SGB II § 12, SGB XII § 90 — insolvency and means-testing
- Publisher: Bundesministerium der Justiz / juris
- URL: not established
- Content: the surrounding protection. **§ 851d ZPO** extends comparable protection to Riester
  *Altersvorsorgevermögen*; **§ 12 SGB II** (*Bürgergeld*, formerly Hartz IV) and **§ 90 SGB XII**
  exempt from the means test old-age provision whose realisation is contractually excluded. The
  practical claim the market makes — that a Basisrente is *Hartz-IV-fest* and *insolvenzfest* — rests
  on these provisions together with [R12]. **All three paragraph addresses are `[unverified]`** and
  the precise conditions were not established (gap 9). The **direction** is not in doubt and it is a
  first-order selling point of the product.

### R14 — VVG § 165 (Beitragsfreistellung), § 168 (Kündigung), § 169 (Rückkaufswert)
- Publisher: Bundesministerium der Justiz / juris
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__165.html`,
  `.../__168.html`, `.../__169.html` — canonical forms, `[unverified]`. § 165 and § 169 were
  established at a higher level of detail in the sibling delib files
  `_research/kapitallebensversicherung.md` [R2] [R3] and `_research/klassische_rentenversicherung.md`
  [R1] [R2], which corroborated them by search
- Content — **the provisions that would give an ordinary German life contract its exits, and what
  becomes of them here**:
  - **§ 165 — *Beitragsfreistellung*.** The policyholder of a contract with periodic premiums may at
    any time, for the end of the current premium period, demand conversion into a **premium-free
    contract with a reduced benefit**, provided the reduced benefit reaches a
    *Mindestversicherungsleistung* agreed in the contract. **This right survives intact in a
    Basisrente** and is the product's only real exit (mechanic 17).
  - **§ 168 — *Kündigung*.** The policyholder may terminate a contract with periodic premiums for
    the end of the current premium period. **The right survives, but it has nothing to pay out**:
    because the contract may not be capitalised [R1], termination cannot produce a
    *Rückkaufswert*, and in practice a purported *Kündigung* of a Basisrente operates as a
    *Beitragsfreistellung*. `[unverified]` as to how individual AVB word this; the outcome is
    settled and universal.
  - **§ 169 — *Rückkaufswert*.** The statutory surrender-value regime — the *Zeitwert* rule, the
    *Mindestrückkaufswert* computed with acquisition costs spread over five years, the requirement
    that a *Stornoabzug* be agreed, appropriate and quantified. **It is inoperative on this product.**
    A Basisrente has a *Deckungskapital* but no *Rückkaufswert* cash flow at any duration. This is
    the single most important thing a modeller coming from the delib endowment or Schicht-3 chassis
    has to unlearn (mechanic 17).

### R15 — VVG § 153 — Überschussbeteiligung
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — canonical form; established by
  search in `_research/kapitallebensversicherung.md` [R1]
- Content: the policyholder's statutory entitlement to a share of the *Überschuss* and of the
  *Bewertungsreserven*, unless participation is expressly excluded. **A Basisrente participates on
  exactly the same terms as any other German life contract** — the layer changes the tax and the
  exits, not the surplus machinery. The four surplus sources (*Zins-*, *Risiko-*, *Kosten-* and
  *übriger Überschuss*), the *RfB*, the MindZV minimum allocation and the *Bewertungsreserven* share
  are all as established for the endowment chassis in the sibling file and are not re-derived here;
  mechanic 11 records only what is different for this product.

### R16 — Deckungsrückstellungsverordnung (DeckRV) — Höchstrechnungszins and Höchstzillmersatz
- Publisher: Bundesministerium der Justiz / juris; amendment by the Bundesministerium der Finanzen
- URL: not established. No delib session established a `gesetze-im-internet.de` address for the
  DeckRV and none is guessed
- Content, carried over from `_research/klassische_rentenversicherung.md` [R7]–[R11], where it was
  corroborated across five independent search results:
  - The ***Höchstrechnungszins*** — the maximum rate a German life insurer may guarantee on the
    savings part of the premium — **rose from 0,25 % to 1,00 % with effect from 1 January 2025**,
    the first increase since 1994; the DAV has recommended **1,0 % for 2026** as well, so the rate
    applicable to new business at this file's access date is **1,00 %**.
  - **The increase applies only to new contracts.** A German life book is a **layered stack of
    guarantee vintages**, and a Basisrente book written since 2005 spans the whole of the decline
    from 2,75 % to 0,25 % and the 2025 recovery. The full ladder — 2,75 %, 2,25 %, 1,75 %, 1,25 %,
    0,90 %, 0,25 %, 1,00 % — is `[unverified]` in delib except for the 0,25 % and the 1,00 %.
  - The ***Höchstzillmersatz*** caps the acquisition costs that may be written into the reserve at
    **25 ‰ of the *Beitragssumme***, reduced from 40 ‰ by the LVRG in 2015 `[unverified]`. On a
    Basisrente the *Beitragssumme* of a long-dated contract with a *Beitragsdynamik* is large, so
    this cap binds in euro terms far above what the same percentage would allow on a short contract.

### R17 — DAV 2004 R — the annuity table
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln
- URL: not established; the DAV's own host refuses this environment
- Content, carried over from `_research/klassische_rentenversicherung.md` [R12]–[R14], where it was
  corroborated by search:
  - **DAV 2004 R is the German annuity table** and is a ***Generationentafel*** — mortality by birth
    cohort, with the improvement trend inside the table rather than applied on top of it. In use
    since June 2004, intended for new business from 2005, and the derivation guideline was
    **reissued on 28 June 2023** — evidence that no successor has displaced it.
  - Component structure: a second-order base table, a first-order base table, second- and
    first-order trends, and an *Altersverschiebung* convention. **First-order probabilities carry
    prudential margins and are used for premiums and reserves**; second-order is the best estimate.
  - **The table is not public and delib does not redistribute it.** A `[std]` proxy is shipped,
    anchored so the worked example reproduces exactly, and a replacement must preserve the
    generational structure, the first-order margin and the age-adjustment convention.
  - **The Basisrente uses the same table as every other German annuity.** There is no Schicht-1
    mortality basis. What differs is the **selection**: mechanic 12 argues that a Basisrente
    portfolio should be expected to be somewhat *lighter* than a Schicht-3 portfolio on mortality,
    because it cannot be surrendered and cannot be commuted, so nobody in poor health has any reason
    to leave it — but **no evidence for that was found and it is a `[std]` view**.

### R18 — BMF-Schreiben on the income-tax treatment of Vorsorgeaufwendungen and Altersbezüge
- Publisher: Bundesministerium der Finanzen
- URL: not established. **No BMF file number is given, because none could be confirmed.**
- Content: the Federal Finance Ministry maintains a consolidated administrative circular — the
  practitioner's "Rentenerlass" — on the deduction of *Vorsorgeaufwendungen* under § 10 EStG and the
  taxation of *Altersbezüge* under § 22 EStG. It is where the operational detail of this product
  lives that the statute does not spell out: how the 50 % majority test for supplementary covers is
  computed, what happens on a change of provider, how the *Rentenfreibetrag* is fixed, and what
  administrative tolerances exist for very small annuities. **Not one of those points could be
  established.** It is the single most valuable document a checker with a working network should
  retrieve, after the statute itself. See gaps 8, 13 and 19.

### R19 — BFH, 19 May 2021 — the Doppelbesteuerung judgments
- Publisher: Bundesfinanzhof
- URL: not established
- Content: two decisions of the same day, commonly cited as **X R 33/19** and **X R 20/19**
  `[unverified]` as to both file numbers, in which the court accepted **in principle** that a
  double taxation of pensions is unconstitutional where the contributions were made from taxed
  income and the benefits are taxed again, and set out a **nominal-value comparison method** for
  testing it: the sum of the tax-free parts of the expected benefits against the sum of the
  contributions paid from taxed income. On the facts before it the court found no double taxation,
  but it identified the transition schedule as capable of producing one for later cohorts —
  particularly for **self-employed taxpayers whose contributions during the phase-in were only
  partly deductible**, which is precisely the Basisrente's own buyer. The legislative response was
  [R7] and [R6]. **The case numbers, the date and the method are `[unverified]`**; the substance —
  that a court-driven concern about double taxation is why the schedule was twice softened — is the
  correct framing for the product-spec's tax section.

### R20 — Sozialversicherungsrechengrößen-Verordnung — the BBG series
- Publisher: Bundesministerium für Arbeit und Soziales, with the consent of the Bundesrat
- URL: not established
- Content: the annual regulation that sets the *Beitragsbemessungsgrenzen* and other social-insurance
  parameters for the following calendar year, made in the autumn of the preceding year. It is the
  instrument that moves the Basisrente *Höchstbetrag* [R2], and it therefore has to be re-read every
  year for this product in a way that is not true of any other delib product. From 2025 the general
  and *knappschaftliche* ceilings are **uniform across the former East and West** `[unverified]`,
  which removed a distinction that had complicated the *Höchstbetrag* for two decades. The series
  itself is tabulated in mechanic 6 and every figure there is `[unverified]`.

### R21 — BaFin — Wohlverhaltensaufsicht and value for money
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- URL: not established; the host refuses this environment
- Content, carried over from `_research/kapitallebensversicherung.md` [R17]–[R19]: BaFin's
  **Merkblatt 01/2023 (VA)** on conduct-supervision aspects of capital-forming life insurance
  products, its *Risiken im Fokus* treatment of the cost of such products, and its published
  articles on excessive costs and on PRIIPs disclosure. **A Basisrente is squarely within that
  supervisory perimeter** — it is a capital-forming life product sold overwhelmingly through
  intermediaries with a commission attached — and the *Effektivkosten* on the § 7 AltZertG
  *Produktinformationsblatt* [S13] is the number the supervision runs on. **Nothing
  Basisrente-specific was established** and gap 15 records it.

### R22 — GDV and BMF statistics on the Basisrente stock and new business
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft; Bundesministerium der Finanzen
- URL: not established
- Content: the GDV publishes annual *Bestand* and *Neugeschäft* statistics for German life insurance
  broken down by product line, including the Basisrente, and the BMF publishes subsidy statistics
  for the certified layers. **No figure from either was established in this session.** The
  order-of-magnitude statements in mechanic 21 are general knowledge, are tagged `[unverified]`
  individually, and are the weakest material in this file. See gap 3.

### R23 — EStG § 93 Abs. 3 — the Kleinbetragsrente, and its absence from Schicht 1
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__93.html` — canonical form, `[unverified]`
- Content — recorded because **the interesting fact is its non-application**:
  - For a **Riester** contract, the provision permits the **commutation of a *Kleinbetragsrente***
    at the start of the payout phase without loss of the subsidy, where the monthly annuity would
    fall below a threshold expressed as **1 % of the monthly *Bezugsgröße* of § 18 SGB IV**
    `[unverified]` as to the fraction and the reference. It is a de-minimis rule that exists because
    administering a trivially small lifelong annuity costs more than it pays.
  - **There is no Schicht-1 equivalent.** § 10 Abs. 1 Nr. 2 Buchst. b [R1] forbids capitalisation
    without qualification and admits no de-minimis. A Basisrente entitlement of two euros a month
    is paid as two euros a month. Mechanic 19 works through what the market does instead.

### R24 — Independent rating and market-analysis houses
- Publishers: **Institut für Vorsorge und Finanzplanung (IVFP)**, Altenstadt; **Franke und
  Bornberg**, Hannover; **Morgen & Morgen**, Hofheim; **Assekurata**, Köln
- URL: not established for any of them
- Content: these four are the German market's standing sources for comparative product analysis in
  this layer. The IVFP publishes the best-known **Basisrente rating**, scoring tariffs on company
  strength, flexibility, transparency, cost and return; Franke und Bornberg rates old-age provision
  products and analyses *Basisinformationsblätter*; Morgen & Morgen rates and models; Assekurata
  publishes the annual *Überschussbeteiligungen und Garantien* market study, whose 2026 edition was
  established in a sibling delib file. **Not one rating, score, ranking or figure was established
  for the Basisrente.** They are named so a checker knows where to go, and so that no downstream
  document invents a ranking.

---
