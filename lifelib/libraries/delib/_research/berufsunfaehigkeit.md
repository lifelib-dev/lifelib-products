# Selbständige Berufsunfähigkeitsversicherung (SBU) — research notes (Germany)

Research notes for the German individual *selbständige Berufsunfähigkeitsversicherung* — the
standalone occupational-disability contract that pays a monthly *BU-Rente* for as long as the
*versicherte Person* is *berufsunfähig*, waives the premium (*Beitragsbefreiung*) for the same
period, and pays nothing at all if the insured remains able to work. It is the flagship German
biometric product: the one contract the German market itself treats as indispensable, sold on a
statutory definition that is unusually favourable to the insured by international standards, and
priced on occupational classes whose spread is wider than in any other retail life product.

**In scope.** The individual, privately written, standalone (*selbständig*) BU contract on a single
life, sold by a *Lebensversicherungsunternehmen* under §§ 172–177 VVG, with a level *Bruttobeitrag*
guaranteed for the whole term, a *Zahlbeitrag* below it funded out of the *Überschussbeteiligung*,
an agreed monthly *BU-Rente*, an agreed *Endalter* for both cover and benefit, and the standard
option set (*Beitragsdynamik*, *Leistungsdynamik*, *Nachversicherungsgarantie*,
*Verlängerungsoption*, *Karenzzeit*, and — for medical occupations — the *Infektionsklausel*). The
*Berufsunfähigkeits-Zusatzversicherung* (BUZ), the same cover sold as a rider on a
*Rentenversicherung*, a *Kapitallebensversicherung* or a *Basisrente*, is treated here as a wrapper
variant of the same liability, because it is: the BU risk, the claim procedure, the *Nachprüfung*
and the *Beitragsbefreiung* are identical, and only the tax treatment and the interaction with the
host contract's premium differ.

**Out of scope, and said so where it matters.** *Erwerbsunfähigkeitsversicherung* (EU cover, keyed
to any occupation rather than the last one) and *Grundfähigkeitsversicherung* (keyed to the loss of
defined basic abilities — seeing, speaking, walking, using the hands) are different products with
different definitions and different pricing bases; they are named below only where they bound the
BU market from beneath. *Dread-disease* / *schwere Krankheiten* cover, *Unfallversicherung*,
*Krankentagegeld*, and the *Pflegerentenversicherung* (delib product 10) are separate liabilities.
*Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* (including
the *Kollektiv-BU* and *bAV-BU* forms), *private Krankenversicherung* and the statutory
*Erwerbsminderungsrente* itself are outside the delib library; the last of these is nevertheless
described at length in section 25, because the German BU contract is designed as a top-up on it and
its level is the reason the private product exists at all.

These notes are the **citation ground truth** for the delib `berufsunfaehigkeit` product documents.
Source ids **S1..S16** and **R1..R30** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.
Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

**No document in this file was retrieved. Not one.** Two independent limits applied while it was
written, and they compound.

**Limit 1 — direct HTTP egress is blocked.** An organisation network policy refuses `WebFetch` and
`curl` (HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist.
The hosts that matter for this product were all tried and all refused:
`gesetze-im-internet.de` (VVG, VAG, SGB VI, EStG, DeckRV, MindZV, IfSG), `bafin.de`, `gdv.de`,
`aktuar.de` (Deutsche Aktuarvereinigung), `deutsche-rentenversicherung.de`,
`bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `buzer.de`, `bundesgerichtshof.de` and
`de.wikipedia.org`. No *Bedingungswerk*, no *Produktinformationsblatt*, no *Basisinformationsblatt*,
no statutory text, no DAV *Ergebnisbericht* and no BaFin publication was opened.

**Limit 2 — the session's `WebSearch` budget was already exhausted before this product was
reached.** The 200-call cap is shared across the whole delib build and was consumed by the
regulatory and contract-law research and by the two products written before this one. **This file
therefore had no research channel at all — neither retrieval nor search.** It is written from the
author's own knowledge of German insurance law and market practice, under the discipline that the
delib house rules impose for exactly this case.

What follows from that, and it governs every line below:

1. **An `[S#]` or `[R#]` tag in this file is a pointer, not a certificate.** It names the document a
   claim must be checked against before it is relied on. It does **not** assert that anyone read
   that document. Every source entry carries
   `Retrieved: no — direct HTTP egress blocked in the build environment; no search corroboration
   (session search budget exhausted)`, and none of them says anything else.
2. **There are no quotations.** Not one German sentence in this file is presented as verbatim
   statutory or contractual wording, because no wording was read. Where the substance of a provision
   is given it is given in the author's own words, in English, with the German terms of art kept in
   German. Any reader who needs the wording must go to the instrument.
3. **No URL, document number, edition date, *Bundesgesetzblatt* citation or page count is invented.**
   Where a canonical URL form is confidently known — `https://www.gesetze-im-internet.de/vvg_2008/__172.html`
   for § 172 VVG — it is given and marked `[unverified]`, because no search returned it. Everywhere
   else the entry says `URL: not established`.
4. **`[unverified]` is used generously.** Every specific paragraph number, effective date, monetary
   amount, percentage, market share, table name and statistic below carries it, because nothing
   confirmed any of them. It is *not* applied to the general shape of a well-established mechanic —
   that the *Nachprüfung* exists, that the market waives the *abstrakte Verweisung*, that the
   premium is quoted as a *Brutto*/*Zahlbeitrag* pair — because tagging those would drown the
   signal. The rule is: the moment a claim becomes **specific and numeric**, it needs the tag.
5. **Uncertain levels are `[std]` parameters, not citations.** Where the mechanic is certain and the
   level is not — a lapse rate, an occupational rating factor, a *Beitragsverrechnung* ratio, a
   *Wiedereingliederungshilfe* amount — this file ships a `[std]` value with a stated rationale and
   an argued plausible range, and the product documents carry it forward as `[std]`. A `[std]`
   number is honest about being a construction. A guessed `[S4]` number is not, and there are none.

**Consequence for the downstream documents.** `product-spec.md` and `technical-notes.md` for this
product will be unusually `[std]`-heavy and unusually explicit about it. That is the correct
outcome, not a defect: the *mechanics* of the German BU contract are well established and are set
out below in full, and it is only the *levels* — the rating factors, the charge loadings, the
decrement tables, the market statistics — that this file cannot source. The gaps register at the
foot of this file is a substantial part of its value and should be read before any figure in it is
used.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Berufsunfähigkeit* (BU) | Occupational disability: inability to follow the **last exercised occupation**, as it was arranged before the impairment |
| *Selbständige Berufsunfähigkeitsversicherung* (SBU) | The standalone BU contract, sold on its own rather than as a rider |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | The same cover written as a rider on a *Renten-*, *Kapitallebens-* or *Basisrentenversicherung* |
| *BU-Rente* | The monthly disability annuity, the product's only substantive benefit |
| *Versicherte Person* / *Versicherungsnehmer* | The life insured / the policyholder — frequently the same person here, but not necessarily |
| *Zuletzt ausgeübter Beruf* | The last exercised occupation — the reference occupation for the whole test |
| *Lebensstellung* | Standing in life: the income level and social position the reference occupation conferred. The limiting concept for any *Verweisung* |
| *Abstrakte Verweisung* | Referring the insured to an occupation they *could* take up, without their actually doing so |
| *Konkrete Verweisung* | Referring the insured to an occupation they **actually** exercise |
| *Prognosezeitraum* | The forward-looking period over which the inability must be expected to last — six months in the market standard |
| *Karenzzeit* | An agreed deferment between the onset of BU and the first benefit payment |
| *Rückwirkende Leistung* | Benefit paid retroactively to the onset of BU once the claim is recognised |
| *Leistungsantrag* | The claim application |
| *Anerkenntnis* | The insurer's declaration that it accepts liability. *Befristetes Anerkenntnis* = a time-limited one |
| *Leistungsprüfung* | The insurer's assessment of the claim |
| *Nachprüfung* / *Nachprüfungsverfahren* | The periodic re-examination of a claim already accepted |
| *Einstellungsmitteilung* / *Änderungsmitteilung* | The notice by which the insurer ends benefit after a *Nachprüfung* |
| *Reaktivierung* | Recovery: the insured ceases to be *berufsunfähig* and the contract reverts to premium-paying cover |
| *Beitragsbefreiung* | Waiver of premium while the BU benefit is in payment |
| *Leistungsdauer* / *Versicherungsdauer* | The period benefits may run for / the period during which a BU may incept and be covered |
| *Endalter* / *Leistungsendalter* | The attained age at which the *Leistungsdauer* ends — 65 or 67 in the market |
| *Wiedereingliederungshilfe* | A lump sum paid to support a return to work |
| *Umorganisationspflicht* | The self-employed insured's duty to reorganise the business before claiming |
| *AU-Klausel* / *Arbeitsunfähigkeitsklausel* | Benefit triggered by a certificate of six months' *Arbeitsunfähigkeit*, without a BU determination |
| *Infektionsklausel* | Treats an official ban on practising imposed for infection reasons as BU, for medical occupations |
| *Beitragsdynamik* / *Leistungsdynamik* | Annual pre-claim escalation of premium and *BU-Rente* / annual escalation of the *BU-Rente* in payment |
| *Nachversicherungsgarantie* | The right to increase the *BU-Rente* on defined life events without renewed underwriting |
| *Verlängerungsoption* | The right to extend the *Endalter* without renewed underwriting |
| *Berufsgruppe* | Occupational rating class |
| *Gesundheitsprüfung* / *Gesundheitsfragen* | Medical underwriting / the application's health questions |
| *Risikozuschlag* / *Ausschlussklausel* | Extra-risk premium loading / exclusion of a named condition |
| *Risikovoranfrage* | Anonymous pre-application enquiry, made to avoid a recorded decline |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure, § 19 VVG |
| *Bruttobeitrag* (*Tarifbeitrag*) / *Zahlbeitrag* (*Nettobeitrag*) | The guaranteed maximum premium / the premium actually charged after surplus is applied |
| *Beitragsverrechnung* | Applying surplus as an immediate reduction of the premium charged — the standard *Überschussverwendung* in BU |
| *Überschussbeteiligung* | Participation in surplus, § 153 VVG, applied to BU through § 176 VVG |
| *Deckungsrückstellung* / *Rückkaufswert* | The actuarial reserve / the surrender value, § 169 VVG via § 176 |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs through the reserve / its statutory cap |
| *Rechnungsgrundlagen erster / zweiter Ordnung* | Prudent (pricing and reserving) bases / best-estimate bases |
| *Invalidisierungswahrscheinlichkeit* / *Reaktivierungswahrscheinlichkeit* | Probability of becoming BU / of recovering from it |
| *Anerkennungsquote* | The proportion of decided claims the insurer accepts |
| *Erwerbsminderungsrente* (EM-Rente) | The statutory disability pension, §§ 43, 240 SGB VI — *volle* and *teilweise* |
| *Versorgungslücke* | The gap between the statutory pension and the income it has to replace |
| *Angemessenheitsgrenze* | The insurer's cap on the insurable *BU-Rente* as a fraction of income |

---

## Primary sources

Every entry below carries the same retrieval status, stated once here rather than repeated sixteen
times: **Retrieved: no — direct HTTP egress blocked in the build environment; no search
corroboration (session search budget exhausted).** Each entry is therefore a **known reference**:
publisher, document type, and a statement of what that class of document contains and why this
product needs it. Where a *Content* block records a specific parameter, that parameter is the
author's recollection of German market practice and is tagged `[unverified]`; it is recorded here
so that a later reader knows **which document to open to check it**, which is the whole function of
this section under the delib retrieval conditions.

Insurer names below are real German life insurers, all of which write BU business. **Tariff and
product names are recalled, not confirmed**, and every one carries `[unverified]`; where the
recollection is weak the entry says so and names only the insurer and the document type.

### S1 — GDV, *Allgemeine Bedingungen für die selbständige Berufsunfähigkeitsversicherung* (unverbindliche Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: *unverbindliche Musterbedingungen* — non-binding model conditions circulated to member
  undertakings, which most German insurers use as the drafting skeleton for their own AVB
- URL: not established
- Content: the single most important document for this product, and the one whose absence hurts
  most. The GDV maintains model AVB for the standalone BU cover; individual insurers depart from
  them in the direction of the policyholder (waiving the *abstrakte Verweisung*, shortening the
  *Prognosezeitraum*, adding an *AU-Klausel*) and rarely against. The model conditions are the
  reason the German BU market is structurally uniform: the definition of *Berufsunfähigkeit*, the
  50 % threshold, the six-month *Prognosezeitraum*, the six-month retrospective fiction, the
  *Anerkenntnis* and *Nachprüfung* clauses, the *Mitwirkungspflichten* and the exclusion list all
  read alike across carriers because they descend from a common model text. **Note carefully**: the
  GDV model conditions are *unverbindlich* — non-binding — precisely because binding recommended
  conditions would be a cartel; every insurer's own AVB is the operative document, and a claim made
  from the model text alone is `[unverified]` against any particular contract.

### S2 — GDV, *Allgemeine Bedingungen für die Berufsunfähigkeits-Zusatzversicherung* (Muster-BUZ)
- Publisher: GDV
- Doc type: *unverbindliche Musterbedingungen* for the rider form
- URL: not established
- Content: the rider counterpart of S1. The substantive BU definition, *Anerkenntnis* and
  *Nachprüfung* clauses are the same; the rider text adds the interaction with the host contract —
  that the *Beitragsbefreiung* covers the **whole** premium of the host contract and not merely the
  rider premium, that the rider ends when the host contract ends, that the rider may not be
  continued alone if the host is surrendered, and that a *beitragsfreie* host contract carries a
  correspondingly reduced or extinguished rider. Needed here because delib's `basisrente` product
  (product 5) and `klassische_rentenversicherung` (product 2) may both carry this rider, and because
  the tax treatment of a BUZ inside a *Basisrente* is materially different from that of an SBU
  (section 24).

### S3 — Allianz Lebensversicherungs-AG, *Allgemeine Versicherungsbedingungen für die selbständige Berufsunfähigkeitsversicherung*, with the associated *Produktinformationsblatt*
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: AVB (*Bedingungswerk*) plus *Produktinformationsblatt*
- URL: not established
- Content: Allianz is the largest German life insurer by premium income and its BU wording is the
  most widely read in the market. Expected to contain: the standard 50 % / six-month definition;
  waiver of the *abstrakte Verweisung*; a *Nachversicherungsgarantie* on a defined event list; a
  *Beitragsdynamik* option; occupational classification into a small number of *Berufsgruppen*; and
  the *Brutto*/*Zahlbeitrag* pair. Allianz also writes BU as a rider inside its *Rentenversicherung*
  and *Basisrente* ranges. **No product name, tariff code, edition date or parameter from any
  Allianz document is asserted in this file.**

### S4 — Alte Leipziger Lebensversicherung a. G., AVB for the *selbständige Berufsunfähigkeitsversicherung*
- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: AVB plus *Tarifbestimmungen*
- URL: not established
- Content: Alte Leipziger is one of the small group of carriers the German broker market treats as
  BU specialists, alongside Nürnberger, LV 1871, Swiss Life, HDI and Volkswohl Bund. The tariff
  family is recalled as carrying a `BV` prefix `[unverified]`. This is the class of document that
  would settle the *Berufsgruppen* count, the *Nachversicherungsgarantie* event list and caps, the
  *Verlängerungsoption* window, and the *Karenzzeit* menu — none of which this file can source.

### S5 — LV 1871 (Lebensversicherung von 1871 a. G. München), AVB for its BU range
- Publisher: Lebensversicherung von 1871 a. G. München
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Content: LV 1871 markets a BU range under a "Golden BU" family name `[unverified]`, with tiers
  differing chiefly in the option set (*Nachversicherungsgarantie* breadth, *AU-Klausel*,
  *Leistungsdynamik*) rather than in the core definition. Recorded because a tiered range is the
  normal German shape — a base tariff and one or two enhanced tariffs on the same risk basis — and a
  reference implementation should model the base tariff and treat the enhancements as switchable
  options.

### S6 — NÜRNBERGER Lebensversicherung AG, AVB for the *selbständige Berufsunfähigkeitsversicherung*
- Publisher: NÜRNBERGER Lebensversicherung AG, Nürnberg
- Doc type: AVB plus *Tarifbestimmungen* plus *Berufsgruppenverzeichnis*
- URL: not established
- Content: historically the largest BU book in Germany by number of contracts `[unverified]`. The
  document class that matters most here is the **Berufsgruppenverzeichnis** — the occupational
  classification list, running to hundreds of named occupations mapped to rating classes. No German
  insurer's full list was retrievable, and the classification is the single largest driver of the
  premium (section 16). Nürnberger also writes BU cover for occupations other carriers decline, and
  publishes claims statistics for its own book.

### S7 — Swiss Life AG, Niederlassung für Deutschland, AVB for its BU range
- Publisher: Swiss Life AG, Niederlassung für Deutschland, München
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Content: Swiss Life's German BU range is regarded in the broker market as a benchmark for
  wording quality `[unverified]`, in particular on the *Verweisung* clauses and on the treatment of
  the self-employed (*Umorganisationspflicht*). Needed for the *Umorganisation* rules, which are the
  most product-specific part of the German BU definition and the part least visible from consumer
  material.

### S8 — HDI Lebensversicherung AG, AVB for its BU range
- Publisher: HDI Lebensversicherung AG, Köln (Talanx group)
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Content: HDI markets its BU under an "EGO" family name `[unverified]`, with a tier structure and
  a strong academic/office proposition. Recorded as one of the carriers whose wording would settle
  the *AU-Klausel* parameters — the certified duration required, the maximum benefit period under
  the clause, and whether payment under it is set off against a later BU recognition (section 11).

### S9 — VOLKSWOHL BUND Lebensversicherung a. G., AVB for its BU range
- Publisher: VOLKSWOHL BUND Lebensversicherung a. G., Dortmund
- Doc type: AVB plus *Tarifbestimmungen*
- URL: not established
- Content: a broker-channel BU specialist. Recorded because its range is one of those that publishes
  a *Bruttobeitrag* and *Zahlbeitrag* side by side in the quotation, which is the practice this file
  needs documented (section 18) and which no retrieved document confirms.

### S10 — Barmenia Lebensversicherung a. G., AVB for its standalone BU cover
- Publisher: Barmenia Lebensversicherung a. G., Wuppertal (now within the Barmenia Gothaer group)
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Content: Barmenia has sold standalone BU under a "SoloBU" name `[unverified]`. Recorded chiefly
  as the carrier most associated with the standalone rather than rider form, and as a reminder that
  the German market's word for the standalone contract — *selbständige* BU — is itself a product
  name in some ranges.

### S11 — Dialog Lebensversicherungs-AG (Generali Deutschland), AVB for its BU range
- Publisher: Dialog Lebensversicherungs-AG, Augsburg — the Generali group's broker-channel
  biometric-risk carrier
- Doc type: AVB plus *Tarifbestimmungen*
- URL: not established
- Content: Dialog is the German market's clearest example of a carrier writing **only** biometric
  risk — *Risikolebensversicherung* and BU — with no savings business at all. Recorded because that
  makes its *Überschussbeteiligung* pure risk and expense surplus with no interest component, which
  is the cleanest illustration of where the *Brutto* / *Zahlbeitrag* gap in a BU tariff comes from
  (section 18). A BU tariff name with a "professional" suffix is recalled `[unverified]`.

### S12 — Further German BU carriers, *Bedingungswerke* and *Produktinformationsblätter* (document class)
- Publishers, all real German life insurers writing BU: R+V Lebensversicherung AG; Debeka
  Lebensversicherungsverein a. G.; Continentale Lebensversicherung AG; Gothaer Lebensversicherung
  AG; Die Stuttgarter Lebensversicherung a. G.; Zurich Deutscher Herold Lebensversicherung AG;
  ERGO Vorsorge Lebensversicherung AG; AXA Lebensversicherung AG; Hannoversche Lebensversicherung
  AG; CosmosDirekt (Generali Deutschland Lebensversicherung AG); Württembergische
  Lebensversicherung AG; Baloise Lebensversicherung AG Deutschland; die Bayerische (Bayerische Beamten
  Lebensversicherung a. G.); universa Lebensversicherung a. G.; DEVK; SIGNAL IDUNA
  Lebensversicherung a. G.; Provinzial; HUK-COBURG-Lebensversicherung AG
- Doc type: AVB, *Tarifbestimmungen*, *Produktinformationsblätter*, *Berufsgruppenverzeichnisse*
- URL: not established for any of them
- Content: recorded as a class so that the breadth of the German market is on the record and so that
  a later researcher has the target list. The commercially significant split inside this list is
  **channel**, not wording: the direct writers (CosmosDirekt, Hannoversche, HUK-COBURG) and the
  bank/*Öffentliche* channels (Provinzial, Sparkassen-Versicherung, R+V through the *Volksbanken*)
  sell simpler tariffs with narrower occupational coverage and fewer options, while the broker
  channel (Alte Leipziger, LV 1871, Nürnberger, Swiss Life, HDI, Volkswohl Bund, Continentale,
  Stuttgarter, die Bayerische) sells the full option set. **Nothing quantitative is cited from any
  document in this class.**

### S13 — *Produktinformationsblatt* (PIB) for a *selbständige Berufsunfähigkeitsversicherung* (document class)
- Publisher: each insurer, for each tariff
- Doc type: the short pre-contractual product information sheet required by the *VVG-Informations­pflichten­verordnung* (VVG-InfoV) `[unverified]` as to the precise article
- URL: not established
- Content: the German retail life market's standard two-page disclosure. For a BU tariff it states
  the type of contract, the insured risk (in a single sentence naming the 50 % and six-month
  criteria), the *BU-Rente* and its escalation, the *Bruttobeitrag* and the *Zahlbeitrag* with an
  explicit warning that the *Zahlbeitrag* may rise as far as the *Bruttobeitrag*, the term and
  *Endalter*, the principal exclusions, the consequences of non-disclosure, and the surrender and
  paid-up positions. **This is the single most useful public document for a modeller**, because it
  is the only one that routinely puts a *Bruttobeitrag* and a *Zahlbeitrag* on the same page for a
  named age, occupation and *BU-Rente*. None was retrieved, and that is gap 4 in the register.

### S14 — *Basisinformationsblatt* (PRIIP-KID) — and why an SBU normally does not have one
- Publisher: each insurer, where the product is in scope
- Doc type: PRIIPs key information document
- URL: not established
- Content: recorded as a **negative** finding of substance. The PRIIPs regime covers
  *insurance-based investment products* — contracts offering a maturity or surrender value exposed
  to market fluctuations. A pure biometric protection contract with no investment element is
  outside it. A standalone SBU is therefore normally documented by a *Produktinformationsblatt*
  [S13] and **not** by a *Basisinformationsblatt*, which is the opposite of the position for delib's
  savings products (products 1–7), where the *Basisinformationsblatt* is the richest public
  document. Where BU is written as a **rider on a savings contract**, the host contract's
  *Basisinformationsblatt* covers the package and the BU premium sits inside its cost figures. The
  precise PRIIPs scope boundary is `[unverified]` here and must be checked before it is relied on;
  what is certain is that this product family does not hand the modeller the cost table that the
  savings products do.

### S15 — Comparison portals and consumer press (document class)
- Publishers: Verivox; CHECK24; Finanztip; Stiftung Warentest / *Finanztest*; Handelsblatt;
  Morgen & Morgen (M&M Rating Berufsunfähigkeit); Franke und Bornberg (BU-Rating and
  BU-Leistungspraxis); ASSEKURATA
- Doc type: comparison pages, consumer guides, periodical product tests and rating publications —
  **secondary throughout**
- URL: not established
- Content: this class is where every published German BU **price point** and every published
  **wording-quality rating** lives, and it is the class this file most needed and least could reach.
  What it would supply: indicative *Zahlbeiträge* by age, occupation, *BU-Rente* and *Endalter*
  across carriers; the *Brutto*/*Zahlbeitrag* ratio by carrier; the number of *Berufsgruppen* per
  carrier; scoring of the *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* wordings;
  the periodic *Finanztest* BU rankings; and Morgen & Morgen's annual analysis of the **causes of
  BU** (section 26). All of the figures in sections 26 and 27 below are of the kind this class
  publishes, and none of them is sourced to it — they are the author's recollection, tagged
  `[unverified]`, and they must be re-established before use.

### S16 — Verbraucherzentrale material on the *Berufsunfähigkeitsversicherung*
- Publisher: the *Verbraucherzentralen* and the *Verbraucherzentrale Bundesverband* (vzbv)
- Doc type: consumer-advice pages and brochures — **secondary**
- URL: not established
- Content: the consumer-protection view of the product: that the statutory *Erwerbsminderungsrente*
  is not a substitute (section 25), that the *Gesundheitsfragen* must be answered completely and
  that incomplete answers are the commonest reason a claim later fails, that a *Risikovoranfrage*
  should precede any application, that the *Bruttobeitrag* rather than the *Zahlbeitrag* is the
  figure a buyer should compare across carriers, and that *Karenzzeiten* and reduced *Endalter*
  are the two levers that cut the premium at a real cost in cover. Recorded because these are
  exactly the behavioural facts a lapse and option-take-up assumption has to reflect, and because
  the "compare the *Bruttobeitrag*" advice is the clearest external statement of why the
  *Brutto*/*Zahlbeitrag* pair is a modelling issue and not a presentational one.

---

## Regulatory and actuarial references

Same retrieval status throughout: **Retrieved: no — direct HTTP egress blocked in the build
environment; no search corroboration (session search budget exhausted).** Where a URL is given it is
the canonical form of a `gesetze-im-internet.de` address and is marked `[unverified]`; the paragraph
numbering it encodes is itself part of what is unverified.

### R1 — VVG § 172, *Leistung des Versicherers* (the statutory definition of *Berufsunfähigkeit*)
- Publisher: Bundesministerium der Justiz / Bundesamt für Justiz, via `gesetze-im-internet.de`
- Doc type: statute — *Gesetz über den Versicherungsvertrag* (VVG) of 2008, Kapitel 5 (Lebens-,
  Berufsunfähigkeits- und Unfallversicherung), Teil 2, Abschnitt 3
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__172.html` `[unverified]`
- Content: the anchor provision of the whole product. Three limbs, as the author recalls them and
  each `[unverified]` as to its exact numbering and wording:
  1. **Abs. 1** obliges the insurer, in a *Berufsunfähigkeitsversicherung*, to render the agreed
     benefits for a *Berufsunfähigkeit* that arises **after the inception of the cover**. The
     temporal condition is the reason a BU contract is a genuine risk contract and not a health
     indemnity: a condition that had already produced BU before inception is not covered, and the
     *vorvertragliche Anzeigepflicht* [R7] polices the boundary.
  2. **Abs. 2** defines *berufsunfähig* as a person who, as a consequence of *Krankheit*,
     *Körperverletzung* or *mehr als altersentsprechender Kräfteverfall*, is prospectively
     permanently (*voraussichtlich auf Dauer*) unable, wholly or in part, to exercise **the last
     occupation actually exercised, as it was arranged before the impairment**
     (*den zuletzt ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet
     war*). Three features of that definition drive everything downstream: the reference occupation
     is the **last one actually exercised**, not any occupation and not the trained one; it is taken
     **as actually arranged**, so that the concrete duties, hours and physical demands of the
     insured's own job are the measure; and the impairment must be **medically caused**, which
     excludes economic inability to work.
  3. **Abs. 3** permits the parties to **agree as a further condition** of the insurer's liability
     that the insured neither exercises nor is able to exercise another activity which, given her
     training and abilities, she is in a position to take up and which corresponds to her previous
     *Lebensstellung*. This is the statutory basis of the *abstrakte Verweisung*: it is **permitted
     but not implied**, it operates only if agreed, and the German market has almost universally
     stopped agreeing it (section 4).
- **What is *not* in § 172**: neither the **six-month** period nor the **50 %** threshold appears in
  the statute. Both are contractual standards carried in the AVB [S1] and are the market's own
  concretisation of the statutory words *voraussichtlich auf Dauer* and *ganz oder teilweise*. This
  correction matters and is made explicitly in section 3, because a brief that attributes the six
  months and the 50 % to § 172 VVG would mislead every downstream document.

### R2 — VVG § 173, *Anerkenntnis*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__173.html` `[unverified]`
- Content: on a *Leistungsantrag*, the insurer must declare in *Textform*, when the claim falls due,
  whether it acknowledges its liability. The second limb restricts the **time-limited
  acknowledgement** (*befristetes Anerkenntnis*): the acknowledgement may be limited in time **only
  once** `[unverified]` as to whether the statute frames this as "only once" or as "only once and
  only with the policyholder's agreement". The economic effect is what matters and is not in doubt:
  once an *Anerkenntnis* has been given, whether limited or not, **the insurer is bound by it and
  can escape only through the *Nachprüfung* route of § 174** [R3] — the burden of proof reverses
  from the insured to the insurer. Before the 2008 VVG reform insurers used repeated time-limited
  acknowledgements to keep that burden on the insured indefinitely; § 173 exists to stop that.

### R3 — VVG § 174, *Leistungsfreiheit* (the *Nachprüfung* and its notice period)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__174.html` `[unverified]`
- Content: where the insurer establishes that the conditions of its liability have ceased, it
  remains obliged to pay **only to the end of the third month following receipt by the policyholder
  of the notice** to that effect. The three-month run-off is the single most model-relevant number
  in the statutory frame: a recovery does not stop the annuity on the day it happens, it stops it at
  a quarter-end measured from a notice. A second limb `[unverified]` addresses the case where the
  insured's occupational position has changed since the *Anerkenntnis* — the insurer may rely on a
  new occupation actually taken up (*konkrete Verweisung*, section 4) — and imposes on the insurer
  the duty to demonstrate a **change** relative to the state of affairs on which the *Anerkenntnis*
  was based, not merely to re-decide the original claim.

### R4 — VVG § 175, *Abweichende Vereinbarungen*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__175.html` `[unverified]`
- Content: §§ 173 and 174 are *halbzwingend* — no departure to the disadvantage of the policyholder
  is effective. This is why the *Anerkenntnis* and *Nachprüfung* mechanics are uniform across the
  market: they are not a competitive variable. Insurers may only improve on them, and some do (for
  example by binding themselves to a longer run-off, or by waiving the *Nachprüfung* after a stated
  benefit duration).

### R5 — VVG § 176, *Anzuwendende Vorschriften*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__176.html` `[unverified]`
- Content: applies the life-assurance provisions of the VVG **mutatis mutandis** to the
  *Berufsunfähigkeitsversicherung*. The range is recalled as **§§ 150 to 170** `[unverified]`. This
  single cross-reference is what makes an SBU a life contract in everything but its trigger, and it
  is load-bearing for the model, because it carries across:
  - § 153 *Überschussbeteiligung* [R10] — hence the *Brutto* / *Zahlbeitrag* pair;
  - § 161 *Selbsttötung* [R11] — hence the three-year suicide window, which in a BU context bites on
    a self-inflicted injury producing disability;
  - § 165 *Prämienfreie Versicherung* [R8] — hence a right to a *beitragsfreie BU-Rente*;
  - § 168 *Kündigung* and § 169 *Rückkaufswert* [R9] — hence a surrender value, and hence a
    *Deckungsrückstellung* that is genuinely material for a level-premium BU contract;
  - § 169 Abs. 3's five-year spreading of acquisition costs, and the *Mindestrückkaufswert*.
  The verification task here is precise: **confirm the range of sections § 176 imports**, because
  every one of the five bullets above depends on it.

### R6 — VVG § 177, *Ähnliche Versicherungsverträge*
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__177.html` `[unverified]`
- Content: extends the *Anerkenntnis* / *Nachprüfung* frame of §§ 173–176 to cover of **reduced
  earning capacity** (*verminderte Erwerbsfähigkeit*) and of *Arbeitsunfähigkeit*, and to accident
  covers that pay for a lasting impairment of the ability to work `[unverified]` as to the exact
  enumeration. Recorded because it is the provision under which an *AU-Klausel* benefit (section 11)
  and a *Grundfähigkeitsversicherung* inherit the same procedural protections, and because it marks
  the outer boundary of the delib product: everything § 177 reaches is a neighbouring product, not
  this one.

### R7 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and its consequences
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` `[unverified]`
- Content: the applicant must disclose the risk circumstances known to her which the insurer has
  asked about in *Textform*. Breach gives the insurer, graded by fault: *Rücktritt* (rescission) for
  intent or gross negligence; contract amendment (retroactive imposition of the terms the insurer
  would have required) for simple negligence; *Kündigung*; and *Anfechtung* for fraudulent
  misrepresentation. The insurer's remedies lapse **five years** after conclusion — **ten years**
  where the breach was intentional or fraudulent `[unverified]` as to both figures and to whether
  the ten-year period attaches to intent or only to fraud. This is the most practically important
  legal provision in German BU after § 172 itself, because the commonest reason an otherwise valid
  BU claim fails is an *Anzeigepflichtverletzung* discovered during the *Leistungsprüfung*. The
  market's behavioural response — the anonymous *Risikovoranfrage*, made through a broker so that a
  decline is never recorded against the applicant in the industry's *Hinweis- und
  Informationssystem* (HIS) — is a direct consequence and is described in section 17.

### R8 — VVG § 165, *Prämienfreie Versicherung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Content: the policyholder may at any time require the contract to be converted to a paid-up
  contract; the insurer computes a reduced sum insured on recognised actuarial principles, with the
  costs of the conversion deductible. For BU the reduced benefit is a **beitragsfreie BU-Rente**,
  and it is small: a BU contract's *Deckungsrückstellung* is a fraction of the present value of the
  remaining risk, so the paid-up *BU-Rente* is a small fraction of the original. § 165 also carries
  the rule that the paid-up benefit must reach a stated minimum or the contract is instead treated
  as terminated with payment of the *Rückkaufswert* `[unverified]`.

### R9 — VVG § 169, *Rückkaufswert* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Content: on termination by notice the insurer must pay the surrender value, computed as the
  *Deckungsrückstellung* calculated on recognised actuarial principles; **acquisition and
  distribution costs must be spread over at least the first five years** for the purpose of the
  *Mindestrückkaufswert*; a *Stornoabzug* is permissible only if agreed, appropriate and
  **quantified in the contract** `[unverified]` as to the exact conditions. Applied to BU through
  § 176 [R5]. The practical consequence is a genuine one and is easy to get wrong: a level-premium
  SBU to age 67 **does** build a substantial reserve, because the *Invalidisierungswahrscheinlichkeit*
  rises far more steeply with age than mortality does, so the level premium heavily overcharges in
  the early years. The surrender value is nevertheless modest relative to premiums paid, because
  the reserve is a risk reserve and not a savings account, and because *Zillmerung* [R13] absorbs the
  early years of it.

### R10 — VVG § 153, *Überschussbeteiligung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Content: the policyholder is entitled to a share of the *Überschuss* and of the
  *Bewertungsreserven* unless participation is expressly excluded; the allocation must follow a
  *verursachungsorientiertes Verfahren* (a method oriented to the origin of the surplus). For BU the
  surplus is overwhelmingly **risk surplus** (actual *Invalidisierungen* below the first-order
  assumption) and **expense surplus**, with an interest component that is small because the reserve
  is small relative to the premium. § 153 is the legal reason a German BU tariff is quoted as a pair
  of numbers (section 18): the *Bruttobeitrag* is the price on first-order bases, and the
  *Zahlbeitrag* is what is actually charged after the anticipated surplus is credited in advance by
  *Beitragsverrechnung*.

### R11 — VVG § 161, *Selbsttötung* (applied via § 176)
- Publisher: as R1
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` `[unverified]`
- Content: in a life contract the insurer is free of liability where the insured takes her own life
  within **three years** of conclusion `[unverified]`, unless the act was committed in a state of
  pathological mental disturbance excluding free determination of will; in that case the
  *Rückkaufswert* is paid. Applied to BU via § 176, the analogue is an **intentionally self-inflicted
  impairment**: the AVB exclude BU caused by the insured's deliberate act, and the three-year window
  applies to the attempted-suicide case. `[unverified]` whether the market's AVB run the three-year
  window or exclude deliberate self-harm without a time limit; both forms are recalled.

### R12 — VVG-Informationspflichtenverordnung (VVG-InfoV)
- Publisher: Bundesministerium der Justiz
- Doc type: statutory instrument prescribing pre-contractual information duties, including the
  *Produktinformationsblatt*
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`
- Content: prescribes what must be given to the applicant before conclusion and mandates the
  *Produktinformationsblatt* [S13] for life and BU contracts, in a prescribed order and at a
  prescribed brevity. For a savings contract it also mandates the disclosure of *Effektivkosten*
  (reduction in yield); **for a pure risk contract there is no yield to reduce**, so a BU
  *Produktinformationsblatt* discloses costs only through the *Brutto* / *Zahlbeitrag* pair and not
  as a percentage figure. That absence is why the delib BU charge assumptions are entirely `[std]`
  (section 20) while the delib endowment's are not.

### R13 — Deckungsrückstellungsverordnung (DeckRV) — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Finanzen
- Doc type: statutory instrument
- URL: `https://www.gesetze-im-internet.de/deckrv/` `[unverified]`
- Content: sets the maximum technical interest rate for the *Deckungsrückstellung* of new German life
  business — and, in practice, for pricing — and caps the acquisition costs that may be zillmered
  into the reserve at **25 ‰ (2,5 %) of the *Beitragssumme*** `[unverified]`. The
  *Höchstrechnungszins* was **0,25 %** for contracts written from 2022 to 2024 and was raised to
  **1,00 %** with effect from 1 January 2025 `[unverified] on both the figures and the date`. Both
  numbers matter here: the *Rechnungszins* discounts a BU liability whose duration is long (a claim
  incepting at 45 on a contract to 67 runs 22 years), and the *Höchstzillmersatz* applied to the
  *Beitragssumme* of a 37-year BU contract produces an acquisition-cost allowance that is large in
  absolute terms even though the annual premium is small. delib's cross-product reference library
  carries the DeckRV in full; this entry exists so that the BU product's own `sources.md` can point
  at it locally.

### R14 — Mindestzuführungsverordnung (MindZV)
- Publisher: Bundesministerium der Finanzen
- Doc type: statutory instrument on the minimum allocation of surplus to policyholders
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Content: prescribes the minimum share of *Rohüberschuss* that must be allocated to the
  *Rückstellung für Beitragsrückerstattung*, separately by source — interest, risk and expense. The
  **risk-result minimum allocation** is the one that governs BU, and it is recalled as **90 % of the
  risk result** `[unverified]`. This is the quantitative link between a BU book's claims experience
  and the *Zahlbeitrag* the market charges: an insurer whose *Invalidisierungen* run well below the
  first-order table must pass most of that back, and the *Beitragsverrechnung* is how it does so
  (section 18).

### R15 — VAG §§ 138, 139, 141 — *Gleichbehandlung*, *Überschussbeteiligung*, *Verantwortlicher Aktuar*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Versicherungsaufsichtsgesetz*
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]` as to the section numbers
- Content: § 138 requires premiums to be calculated on actuarial principles sufficient to meet the
  obligations permanently and requires **equal treatment of equal risks**; § 139 governs the
  *Überschussbeteiligung* on the supervisory side and is the counterpart of § 153 VVG; § 141 places
  the pricing and reserving bases in the hands of the *Verantwortlicher Aktuar*, who must confirm
  that the *Deckungsrückstellung* is properly calculated and that the premiums are sufficient. For
  BU the *Gleichbehandlungsgrundsatz* is what legitimises *Berufsgruppen*: differentiating price by
  occupation is not discrimination but the recognition that the risks are not equal. The same
  principle **forbids** differentiating by sex — see the unisex rule below.
- **Unisex.** Since 21 December 2012 German insurers may not differentiate premiums or benefits by
  sex, following the CJEU's *Test-Achats* judgment `[unverified]` as to the case reference and the
  transposing instrument. This bites unusually hard in BU, because the underlying
  *Invalidisierungswahrscheinlichkeiten* differ materially by sex — female incidence is higher at
  most ages `[unverified]` — so a unisex BU tariff embeds a mix assumption that the insurer bears
  the risk of. Any delib BU decrement table must be a **unisex** table for pricing, whatever the
  underlying research bases are.

### R16 — DAV 1997 I, DAV 1997 RI and DAV 1997 TI — the *Rechnungsgrundlagen* for BU
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln
- Doc type: actuarial tables and the accompanying *Herleitung* (derivation) report of the DAV's
  working party on BU bases
- URL: not established
- Content: the German BU pricing and reserving standard, and — critically — **not public**. The
  package as the author recalls it comprises three tables `[unverified]` on the names:
  - **DAV 1997 I** — *Invalidisierungswahrscheinlichkeiten*: the probability that an active life
    aged x becomes *berufsunfähig* within a year, by age and sex, before occupational loading.
  - **DAV 1997 RI** — *Reaktivierungswahrscheinlichkeiten*: the probability that a disabled life
    recovers, **by age at disablement and by duration since disablement**. The duration dimension is
    the essential one: reactivation is concentrated in the first one to two years of a claim and
    falls close to zero thereafter.
  - **DAV 1997 TI** — *Sterbewahrscheinlichkeiten der Invaliden*: mortality of disabled lives, which
    is materially heavier than active mortality and itself select on duration.
  The bases are *erster Ordnung*, i.e. deliberately prudent, and are used with insurer-specific
  **occupational loading factors** and **safety margins**; second-order (best-estimate) versions are
  derived by each insurer from its own experience. The brief that commissioned this file attributed
  both the entry and the reactivation probabilities to "DAV 1997 I and DAV 1997 TI"; **the
  correction is that DAV 1997 TI is the disabled-lives mortality table and the reactivation
  probabilities sit in a third table**, recalled as DAV 1997 RI. That correction is itself
  `[unverified]` and is gap 8 in the register.
- **Is there a newer table?** No successor in general market use could be established. The DAV's
  working parties have published *Ergebnisberichte* on the adequacy of the 1997 bases and on the
  drift in BU experience since — in particular the rise in psychiatric causes (section 26) — but
  this file cannot confirm that a "DAV 20xx I" exists, is homologated, or is used. **Treat
  DAV 1997 I / RI / TI as the current first-order standard and the existence of any successor as
  unresolved** (gap 9).
- **Redistribution.** The DAV tables are the property of the Deutsche Aktuarvereinigung, are not
  published, and **are not redistributed by delib**. The delib BU model ships `[std]` proxy tables
  and states, in its `Data` docstring and in `model.md`, what a replacement built from the real
  tables must preserve: the age shape of the inception rate, the duration shape of reactivation, and
  the excess of disabled-lives mortality over active mortality.

### R17 — DAV 2008 T — active-lives mortality
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: mortality table for contracts with death-benefit character, with its *Herleitung* report
- URL: not established
- Content: the first-order mortality table for German risk business. Relevant to BU as the **active
  state's** mortality decrement: an active life leaves the model by becoming BU, by lapsing, or by
  dying, and the last of these uses a *Todesfall*-character table. Not public; delib ships a `[std]`
  proxy. Also carried in the delib cross-product reference library for the
  `risikolebensversicherung` product, whose research file is the primary place it is described.

### R18 — DAV *Ergebnisberichte* and *Fachgrundsätze* on biometric bases and BU
- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung* / working parties on
  biometric bases (*AG Biometrische Rechnungsgrundlagen*) and on *Berufsunfähigkeit*
- Doc type: *Ergebnisberichte* (results reports) and *Fachgrundsätze* (professional standards)
- URL: not established
- Content: the DAV publishes results reports on the derivation and periodic review of biometric
  bases, on the treatment of *Reaktivierung*, on *Storno* in biometric products, and on the
  best-estimate assumptions used for Solvency II technical provisions. These are the documents that
  would supply the shape of the German BU inception curve, its trend over time and the second-order
  reactivation pattern — the three things this file most lacks quantitatively. They are freely
  downloadable in normal conditions and were unreachable here.

### R19 — BaFin material on the *Berufsunfähigkeitsversicherung*
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- Doc type: *Merkblätter*, *Rundschreiben*, *BaFinJournal* articles, *Risiken im Fokus*
- URL: not established (`bafin.de` refused)
- Content: BaFin supervises the *Leistungsprüfung* practice of German BU insurers as a conduct
  matter (*Wohlverhaltensaufsicht*) and has published on the duration of claims decisions, on the
  quality of *Nachprüfung* notices, and on the *Brutto*/*Zahlbeitrag* disclosure. It also collects
  and publishes the industry's *Beschwerdestatistik*, in which BU is persistently over-represented
  relative to its premium share `[unverified]`. Nothing specific is cited from BaFin in this file.

### R20 — GDV statistics on the *Berufsunfähigkeitsversicherung*
- Publisher: GDV
- Doc type: *Statistisches Taschenbuch der Versicherungswirtschaft*, *Die deutsche
  Lebensversicherung in Zahlen*, and GDV press material on BU
- URL: not established
- Content: the source that would give the **size of the German BU market** — number of in-force
  contracts, new business, premium income, and the industry-wide *Anerkennungsquote*, which the GDV
  began publishing in recent years `[unverified]` as to the year and the figure. An order of
  magnitude often quoted is that roughly **17 million** BU contracts are in force in Germany
  `[unverified]`, counting standalone and rider forms together, against a working population of
  about 45 million — i.e. cover is far from universal, which is the market's own framing of the
  product. **None of these figures is sourced here.**

### R21 — Franke und Bornberg, *BU-Leistungspraxis* and the *BU-Rating*
- Publisher: Franke und Bornberg GmbH, Hannover
- Doc type: recurring market study of BU claims practice, based on data supplied and audited at
  participating insurers, plus the firm's ratings of BU *Bedingungen*
- URL: not established
- Content: **the usual publisher of the German *Anerkennungsquote***, and the reference this file's
  section 26 points at. The study reports, per participating insurer and in aggregate: the
  proportion of decided BU claims accepted; the breakdown of declines by reason (BU degree not
  reached, *Anzeigepflichtverletzung*, *Anfechtung*, failure to co-operate, claim withdrawn); the
  average duration of a claims decision; the proportion of decisions reached without a medical
  examination; and the proportion of disputes. It also rates BU wordings clause by clause, which is
  where the market's ranking of *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* terms
  comes from. Every figure in section 26 attributed to an *Anerkennungsquote* should be checked
  against this study.

### R22 — Morgen & Morgen, *M&M Rating Berufsunfähigkeit* and the annual causes analysis
- Publisher: MORGEN & MORGEN GmbH, Hofheim am Taunus
- Doc type: annual rating of BU tariffs and an accompanying analysis of the **causes of BU**
- URL: not established
- Content: **the usual publisher of the German causes-of-BU distribution** — the percentages in
  section 26. The analysis groups causes into roughly six classes (*Nervenkrankheiten* including
  psychiatric conditions; *Erkrankungen des Skelett- und Bewegungsapparates*; *Krebs und andere
  bösartige Geschwülste*; *Unfälle*; *Erkrankungen des Herzens und des Gefäßsystems*; *sonstige
  Erkrankungen*) and publishes the split annually, so the series shows the long rise of the
  psychiatric share. The rating side scores tariffs on wording, on the insurer's financial strength
  and on the stability of its *Zahlbeitrag* relative to its *Bruttobeitrag* — the last of these
  being the market's own recognition that the *Brutto*/*Zahlbeitrag* gap is a risk to the buyer.

### R23 — ASSEKURATA, market studies on *Überschussbeteiligung* and on biometric products
- Publisher: ASSEKURATA Assekuranz Rating-Agentur GmbH, Köln
- Doc type: annual market studies and insurer ratings
- URL: not established
- Content: ASSEKURATA's annual study of declared *Überschussbeteiligung* is the standard reference
  for German surplus declarations. For BU the relevant content is the **stability of the
  *Beitragsverrechnung***: which insurers have had to raise the *Zahlbeitrag* toward the
  *Bruttobeitrag*, and by how much. That history is the empirical content of the risk the
  *Bruttobeitrag* represents, and it is not established in this file (gap 6).

### R24 — SGB VI § 43, *Rente wegen Erwerbsminderung*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Sozialgesetzbuch, Sechstes Buch*
- URL: `https://www.gesetze-im-internet.de/sgb_6/__43.html` `[unverified]`
- Content: the statutory disability pension the private BU contract sits on top of. Two tiers, both
  measured against the **general labour market** (*allgemeiner Arbeitsmarkt*) rather than the
  insured's own occupation:
  - **Rente wegen teilweiser Erwerbsminderung** — the insured can work at least **three but less
    than six hours** a day under normal labour-market conditions `[unverified]`.
  - **Rente wegen voller Erwerbsminderung** — the insured can work **less than three hours** a day
    `[unverified]`.
  Both require the general *Wartezeit* of **five years** of contributions and, in addition, **three
  years of compulsory contributions in the last five years** before the onset `[unverified]`.
  Pensions are normally granted for a limited period (*Zeitrente*), typically three years, renewable,
  and become permanent only in defined circumstances `[unverified]`.

### R25 — SGB VI § 240 — the abolished statutory *Berufsunfähigkeitsrente*
- Publisher: as R24
- URL: `https://www.gesetze-im-internet.de/sgb_6/__240.html` `[unverified]`
- Content: the transitional provision preserving a *Rente wegen teilweiser Erwerbsminderung bei
  Berufsunfähigkeit* for insured persons **born before 2 January 1961** `[unverified]`. For everyone
  born on or after that date the statutory scheme contains **no occupational-disability pension at
  all** — only the general-labour-market *Erwerbsminderungsrente* of § 43. This is the historical
  fact that created the modern German private BU market: the 2001 reform removed occupational
  protection from the statutory scheme for the whole post-1960 cohort, and the private SBU is its
  replacement. Any delib document explaining why this product exists should cite this provision.

### R26 — Deutsche Rentenversicherung statistics on *Erwerbsminderungsrenten*
- Publisher: Deutsche Rentenversicherung Bund
- Doc type: *Rentenversicherung in Zahlen*, *Rentenzugangsstatistik*, and the annual press material
  on new *Erwerbsminderungsrenten*
- URL: not established (`deutsche-rentenversicherung.de` refused)
- Content: the source for the **average level** of the statutory disability pension — the figure
  that quantifies the *Versorgungslücke* the private product fills — and for the number of new
  awards per year, the average age at award, and the distribution of awards by diagnosis. The DRV's
  diagnosis distribution is an independent check on the insurers' causes-of-BU distribution [R22]
  and is known to show an even higher psychiatric share, because the statutory test is harder to
  meet for musculoskeletal conditions `[unverified]`. Figures quoted in section 25 are recalled and
  tagged, not sourced.

### R27 — EStG § 10 and § 22 — deductibility of the premium and taxation of the *BU-Rente*
- Publisher: Bundesministerium der Justiz
- Doc type: statute — *Einkommensteuergesetz*
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` and `.../__22.html` `[unverified]`
- Content: two distinct regimes, and the difference between them is the main reason to write BU as a
  *Basisrente* rider rather than standalone:
  - **Standalone SBU (Schicht 3).** The premium is a *sonstige Vorsorgeaufwendung* under
    § 10 Abs. 1 Nr. 3a EStG, deductible only inside an annual ceiling — recalled as **1 900 €** for
    employees and civil servants and **2 800 €** for the self-employed `[unverified]` — which is in
    practice already exhausted by statutory health and long-term-care contributions, so the
    effective deduction is **nil** for most buyers. The *BU-Rente* is then taxed under
    § 22 Nr. 1 EStG as an *abgekürzte Leibrente* on its **Ertragsanteil**, determined by the
    annuity's **remaining term** at the time it starts rather than by the recipient's age.
  - **BU inside a *Basisrente* (Schicht 1).** The premium is an *Altersvorsorgeaufwendung* under
    § 10 Abs. 1 Nr. 2 EStG, deductible in full within the much larger *Basisrente* ceiling, provided
    the BU component satisfies the conditions of R28. The *BU-Rente* is then fully taxable as
    *sonstige Einkünfte* at the cohort *Besteuerungsanteil* — a far heavier taxation of the benefit
    in exchange for a far larger deduction of the premium.
  All specific figures here are `[unverified]`, and the *Ertragsanteil* table is reproduced in
  section 24 with the same tag.

### R28 — BMF-Schreiben on the *Basisrente* and the conditions for a BU component
- Publisher: Bundesministerium der Finanzen
- Doc type: administrative circular (*BMF-Schreiben*) on the tax treatment of *Altersvorsorge* and
  *Basisrenten* contracts
- URL: not established (`bundesfinanzministerium.de` refused)
- Content: the instrument that sets the conditions a BU rider must satisfy for the whole premium to
  qualify as an *Altersvorsorgeaufwendung*. The recalled conditions are: the BU benefit must be paid
  **as an annuity**, not a lump sum; it must run at most to the end of the host contract's deferment;
  and **more than 50 % of the total premium must be attributable to the old-age provision**, i.e.
  the BU rider premium may not exceed **49 %** of the total `[unverified] on the percentage`. That
  threshold is the reason a *Basisrente* with a large BU rider must carry a correspondingly large
  savings premium, and it is a genuine product-design constraint that delib's `basisrente` product
  must respect if it ever carries this rider.

### R29 — BGH case law on *Verweisung*, *Anerkenntnis* and *Nachprüfung*
- Publisher: Bundesgerichtshof, IV. Zivilsenat (the insurance senate)
- Doc type: judgments
- URL: not established; **no docket number is given anywhere in this file**, because none could be
  confirmed and inventing one is barred
- Content: four settled lines, each recalled in substance and each `[unverified]` in every detail:
  1. **Binding effect of the *Anerkenntnis*.** A declaratory *Anerkenntnis* binds the insurer; it
     may free itself only by the *Nachprüfung* route, and only prospectively. It cannot simply
     re-decide the original claim.
  2. **The *Nachprüfung* requires a demonstrated change.** The insurer must compare the insured's
     state at the *Nachprüfung* with the state on which the *Anerkenntnis* rested and demonstrate a
     material improvement; a mere re-assessment of the same facts, or a corrected earlier error,
     does not entitle it to stop paying. The *Einstellungsmitteilung* must set out that comparison
     intelligibly, and one that does not is ineffective — so the three-month period of § 174 never
     starts to run.
  3. **Lebensstellung.** A *Verweisungsberuf* must correspond to the previous occupation in income
     **and** in social standing. A noticeable drop in income breaks the correspondence; the market's
     working threshold of **about 20 %** `[unverified]` is a rule of thumb drawn from the case law
     rather than a figure the BGH has fixed.
  4. **Umorganisation for the self-employed.** A self-employed insured must, before being treated as
     *berufsunfähig*, consider whether the business can be reorganised so that she can continue to
     run it within her remaining capacity — but only where the reorganisation is economically
     sensible and does not require a substantial loss of income or a loss of the leading position.

### R30 — Infektionsschutzgesetz (IfSG) — the basis of the *Infektionsklausel*
- Publisher: Bundesministerium der Justiz
- Doc type: statute
- URL: `https://www.gesetze-im-internet.de/ifsg/` `[unverified]`
- Content: empowers the competent authority to impose a *Tätigkeitsverbot* — a prohibition on
  practising — on a person who is infected, is suspected of being infected or is a carrier, where
  practising would risk transmission. For medical, dental, nursing and laboratory occupations such a
  ban ends the ability to earn without the person being ill in the sense of § 172 VVG. The
  *Infektionsklausel* (section 14) is the market's contractual answer: it deems the ban to be BU.
  The clause is essentially standard for doctors and dentists and common for nursing and medical
  assistants.

### R31 — Versicherungsteuergesetz (VersStG) § 4 — exemption of life and BU premiums
- Publisher: Bundesministerium der Justiz
- Doc type: statute
- URL: `https://www.gesetze-im-internet.de/versstg/` `[unverified]`
- Content: German insurance premium tax exempts life-assurance premiums, and the exemption extends
  to *Berufsunfähigkeitsversicherung* written by a life insurer `[unverified]` as to the paragraph
  and the precise scope. The practical consequence for the model is simply that **the BU premium
  carries no premium tax**, unlike a German non-life premium at 19 %. This should be confirmed
  before any delib document states it as a fact; it is recorded here because a modeller coming from
  a non-life background will otherwise wonder where the tax line is.

---

## Extracted facts, organised by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. Under the
retrieval conditions of this build it is also the section that carries the file's weight: the
**mechanics** of the German BU contract are well established and are set out here in full, and the
`[S#]` / `[R#]` tags name the document each statement must be checked against. Every **level** is
either `[std]` with a rationale or `[unverified]` with a warning.

### 1. Product structure and legal form

- An SBU is a **life-assurance contract** written by a *Lebensversicherungsunternehmen*, governed by
  §§ 172–177 VVG for its own mechanics and, through § 176, by the general life provisions
  §§ 150–170 VVG for everything else [R1] [R5]. It is not health business and not accident business,
  even though its trigger is a health event.
- The contract is a **pure risk contract with a reserve**. It pays only on the insured event, has no
  maturity benefit, and returns nothing if the insured stays healthy. It nevertheless carries a
  material *Deckungsrückstellung*, because the premium is level and the risk rises steeply with age
  [R9]. That combination — no savings intent, substantial reserve — is the structural fact that
  distinguishes BU from every other product in delib.
- Two commercial forms, one liability:
  - **Selbständige BU (SBU)** — standalone. The premium buys BU cover and nothing else. This is
    delib product 9 and the subject of this file.
  - **BU-Zusatzversicherung (BUZ)** — a rider on a *Renten-*, *Kapitallebens-* or
    *Basisrentenversicherung* [S2]. The BU risk, definition, claim procedure and *Nachprüfung* are
    identical; what differs is that the *Beitragsbefreiung* waives the **whole** premium of the host
    contract, and that the tax treatment follows the host (section 24).
  - A third form, the **BU-Rente as a benefit inside an occupational pension** (*bAV-BU*), is out of
    delib's scope entirely.
- The German market's own hierarchy of biometric income protection, from broadest trigger to
  narrowest, is worth stating because it bounds the product: *Berufsunfähigkeit* (last occupation,
  50 %) → *Grundfähigkeitsversicherung* (loss of defined basic abilities) → *Erwerbsunfähigkeit*
  (any occupation) → statutory *Erwerbsminderungsrente* (general labour market, hours-based) [R24].
  BU is the **broadest and most expensive** of the four and is the one the market sells first.

### 2. The statutory definition — § 172 VVG

- A person is *berufsunfähig* who, **as a consequence of illness, bodily injury or more than
  age-appropriate decline in strength**, is **prospectively permanently** unable, wholly or in part,
  to exercise **the occupation last actually exercised, as it was arranged before the impairment**
  [R1].
- Four things follow, and all four are model-relevant:
  1. **The reference occupation is the last one actually exercised.** Not the trained occupation,
     not an average occupation, not "any occupation". A trained lawyer working as a warehouse
     supervisor is tested against warehouse supervision. This is why the German BU trigger is so
     much more generous than an "any occupation" disability definition, and why the price is so much
     more sensitive to the insured's actual job.
  2. **It is taken as actually arranged** (*so wie er ohne gesundheitliche Beeinträchtigung
     ausgestaltet war*). The concrete duties, working hours and physical demands of this insured's
     own post are the yardstick. Two people with the same job title can have different tests.
  3. **The cause must be medical.** Illness, bodily injury, or a decline in strength beyond what the
     age would explain. Loss of the job, loss of a licence for non-medical reasons, or an economic
     inability to find work is not BU — with the single contractual exception of the
     *Infektionsklausel* (section 14).
  4. **Prospectively permanent** — *voraussichtlich auf Dauer*. The statute does not put a number on
     it; the market does (section 3).
- **§ 172 Abs. 3 permits, but does not imply, the *abstrakte Verweisung*** [R1]. Absent an express
  agreement, the insurer may **not** refer the insured to an occupation she does not actually
  exercise. Section 4 records what the market does with that permission.

### 3. The contractual definition — six months, 50 per cent, and the two routes to a claim

**This section corrects the brief that commissioned the file.** The six-month period and the 50 %
threshold are **not** in § 172 VVG. They are contractual standards, carried in the AVB [S1] [S3]–[S12]
and near-uniform across the market, which concretise the statutory words *voraussichtlich auf Dauer*
and *ganz oder teilweise*. A downstream document that attributes them to the statute is wrong, and
this file's product-spec must not.

- **The market-standard AVB definition** (substance, not wording, and `[unverified]` in every
  detail): the insured is *vollständig berufsunfähig* if, as a consequence of illness, bodily injury
  or more than age-appropriate decline in strength — **each to be demonstrated medically** — she is
  **prospectively for at least six months continuously** unable to exercise her last occupation, as
  it was arranged before the impairment, **to at least 50 %** [S1].
- **The 50 % threshold is all-or-nothing.** At 50 % or more inability, the **full** *BU-Rente* is
  payable. At 49 %, nothing is payable. There is no proportional benefit in the market standard.
  Some tariffs historically offered a *Staffelregelung* paying a partial *BU-Rente* between 25 % and
  50 % inability `[unverified]`, and a few modern tariffs offer a "Teil-BU"; both are minority
  designs and delib models the all-or-nothing form.
- **Measuring the 50 %** is done on **working time**, on the share of the occupation's essential
  tasks the insured can still perform, or on both, depending on the AVB. Where a residual capacity
  exists, the test is whether the insured could still perform her own job for at least half a normal
  working day, or perform at least half of its defining tasks. Practically the assessment is a
  medical report plus a detailed description of the actual job, and the burden of proof on the
  initial claim is on the **insured** [R21].
- **Two routes to a claim, and both matter to the model.**
  - **The prognosis route.** A doctor certifies that the 50 % inability is expected to last at
    least six months from now. Benefit is due from the onset of the BU (subject to any
    *Karenzzeit*), without waiting for the six months to elapse.
  - **The six-month fiction route.** Where the insured **has actually been** unable, continuously,
    for six months to exercise the occupation to at least 50 %, the **continuation of that state
    counts as BU** without any further prognosis. This is the clause the German market calls the
    *Sechs-Monats-Regelung* or the *BU-Fiktion*, and it exists because a forward-looking prognosis
    is hard to obtain and easy to contest.
  - **Retroactivity is the difference between good and bad wordings.** The modern market standard
    pays **retroactively from the beginning of the six-month period** once the fiction is
    established. Older and weaker wordings paid only **from the end** of the six months, i.e. the
    insured lost half a year of benefit `[unverified]` as to how much of the current market still
    does this. delib models retroactive payment from onset and records the alternative as a switch
    (section 7).
- **Prognosezeitraum variants.** Six months is the standard. Some tariffs shorten the prognosis to
  **three months** as a competitive feature `[unverified]`; a shorter prognosis makes a claim easier
  to establish and therefore raises the effective inception rate without changing the definition.

### 4. Abstrakte and konkrete Verweisung

The two *Verweisung* clauses are the most distinctive feature of German BU and the ones a
non-German modeller most often gets wrong.

- ***Abstrakte Verweisung*** — the insurer refers the insured to an occupation she **could**
  take up, given her training and abilities, corresponding to her previous *Lebensstellung* —
  **whether or not she actually does so** [R1 Abs. 3]. If agreed and applicable, no benefit is
  payable at all, however unable she is to do her own job. It is the clause that made German BU
  cover much less valuable than it looked, because almost any insured can be pointed at *some*
  theoretically available occupation.
  - **The market standard is now to waive it.** Essentially every quality tariff sold in the
    contemporary German market contains a *Verzicht auf die abstrakte Verweisung* [S1] [S3]–[S12].
    The waiver is not a legal requirement — § 172 Abs. 3 still permits the clause — it is a
    competitive standard, and a tariff that retains the *abstrakte Verweisung* is not sold in the
    broker channel. `[unverified]` as to when the waiver became universal; the shift is recalled as
    having taken place over the late 1990s and 2000s.
  - **Legacy books still carry it.** Contracts written before the waiver became standard remain in
    force with it, which is why the *Verweisung* still generates litigation. delib models the
    modern, waived form and notes the legacy form as a variant.
- ***Konkrete Verweisung*** — the insurer refers the insured to another occupation she **actually
  exercises**. This is **retained** by the market, and it is retained on both sides of the claim:
  - **At the initial claim**, if the insured has already taken up another occupation which
    corresponds to her training, abilities and previous *Lebensstellung*, she is not *berufsunfähig*.
  - **In the *Nachprüfung***, if the insured takes up such an occupation after benefit has started,
    the insurer may end the benefit — subject to the three-month run-off of § 174 [R3].
  - **The limit is *Lebensstellung***. The new occupation must correspond in **income** and in
    **social standing** to the old. The working market threshold is that an income drop of more than
    about **20 %** breaks the correspondence `[unverified]`; that figure comes from lower-court
    practice and market wordings rather than from a fixed statutory or BGH rule [R29].
  - Some tariffs go further and **waive the konkrete Verweisung as well**, or waive it where the new
    occupation pays materially less. That is a genuine competitive variable and one of the things a
    *Bedingungsrating* scores [R21] [R22].
- **Model consequence.** *Konkrete Verweisung* is not a separate decrement. In a cash-flow model it
  is **indistinguishable from recovery**: both end the benefit, both operate through the
  *Nachprüfung*, and both carry the same three-month run-off. delib therefore folds recovery and
  *konkrete Verweisung* into a single duration-dependent **claim-termination-other-than-death**
  rate, and says so explicitly rather than pretending to separate two things no public data
  separates.

### 5. The claim procedure — *Leistungsantrag*, *Leistungsprüfung* and *Anerkenntnis* (§ 173 VVG)

- The insured files a *Leistungsantrag* with a detailed description of the occupation as actually
  exercised, medical reports, and releases allowing the insurer to obtain records. The insurer runs
  a *Leistungsprüfung*, which routinely involves its own medical assessment and, for the
  self-employed, an analysis of the business [R21].
- **The insurer must declare in *Textform* whether it acknowledges liability** [R2]. The declaration
  is an *Anerkenntnis*.
- **The *Anerkenntnis* binds.** Once given, the insurer cannot revisit the same facts; it can only
  stop paying prospectively through a *Nachprüfung* in which the **burden of proof is on the
  insurer** [R3] [R29]. This reversal of the burden is the most valuable thing an insured obtains
  from a BU claim, and it is why § 173's restriction on the *befristetes Anerkenntnis* matters.
- ***Befristetes Anerkenntnis*.** A time-limited acknowledgement may be given **only once** [R2].
  Within the period it binds absolutely. Market practice limits it to a stated maximum, recalled as
  **6 or 12 months** `[unverified]`; a few tariffs waive the *befristetes Anerkenntnis* entirely as a
  selling point. When the period ends, the insurer must either continue paying or run a proper
  *Nachprüfung* — it cannot simply stop.
- **Time to decision.** The German market's own claims studies report an average decision time
  measured in months, with a figure of the order of **five to six months** recalled `[unverified]`,
  and a meaningful tail of much longer cases. **Model consequence**: the benefit is paid
  retroactively to onset, so a decision delay produces a **lump catch-up payment**, not a lost
  payment. A monthly cash-flow model that pays from onset and ignores the decision delay is
  understating the timing but not the amount; delib takes that simplification and records it as a
  pitfall.
- **Not every incepted BU becomes a paid claim.** The proportion accepted is the *Anerkennungsquote*
  (section 26). For a projection model this is an **acceptance factor** applied to the inception
  rate, not a separate state.

### 6. Nachprüfung, Leistungsfreiheit and Reaktivierung (§ 174 VVG)

- Once benefit is in payment the insurer may **periodically re-examine** whether its conditions
  still hold. Market practice is an annual or biennial *Nachprüfung*, with the AVB imposing
  *Mitwirkungspflichten* on the insured — to supply medical evidence, to notify a change in health
  or occupation, and to submit to examination `[unverified]` as to frequency.
- **What the insurer must show.** A *change* relative to the state on which the *Anerkenntnis*
  rested: either a medical improvement lifting the insured above the 50 % threshold in her old
  occupation, or a new occupation **actually taken up** that satisfies *konkrete Verweisung*
  (section 4) [R3] [R29].
- **The three-month run-off.** Where the insurer establishes that the conditions have ceased, it
  remains liable to the **end of the third month after the notice reaches the policyholder** [R3].
  A defective notice — one that does not intelligibly set out the comparison — does not start the
  period at all [R29]. **Model consequence**: a claim termination other than death is followed by
  three further monthly payments. In a monthly model this is a three-month tail on every
  reactivation, and it is a real cash-flow effect, not a rounding detail: at a reactivation rate
  concentrated in the first two years of a claim, the tail adds a measurable amount to the expected
  benefit.
- ***Reaktivierung*** — the insured recovers and the cover **revives**. The contract does not end:
  the *Beitragsbefreiung* stops, the premium resumes at the same *Zahlbeitrag*, and a fresh BU may
  be claimed later. This bidirectional structure is what makes BU a genuine multi-state model rather
  than a decrement model, and it is the single most important structural difference from the
  `risikolebensversicherung` product.
- **Reactivation is strongly duration-dependent.** The probability of recovery is highest in the
  first year of a claim, falls sharply over the second and third, and is close to zero after about
  five years [R16]. The corollary is the one that governs the reserve: a claim that survives its
  first two years is very likely to run to the *Endalter*. Any delib reactivation proxy must
  reproduce that shape, and a flat reactivation rate is a modelling error the tests should catch.
- **Some tariffs waive the *Nachprüfung*** after a stated benefit duration, or promise not to
  invoke *konkrete Verweisung* after a stated period `[unverified]`. Treated by delib as an option
  switch, off in the base run.

### 7. Karenzzeit, rückwirkende Leistung and the start of benefit

- ***Karenzzeit*** — an **agreed deferment** between the onset of BU and the first payment. It is a
  contractual option chosen at inception, not a standard feature. Menus observed in the market are
  recalled as **0, 3, 6, 12, 18 and 24 months** `[unverified]`. The standard sale is **no
  Karenzzeit**; a *Karenzzeit* is taken to cut the premium, typically by a buyer who has employer
  sick pay or a professional scheme covering the first period.
- **The *Karenzzeit* is not the six-month prognosis.** They are independent and frequently confused.
  The prognosis period is part of the **definition** of BU (section 3); the *Karenzzeit* is a
  deferment of **payment** on a BU that is already established. A contract with no *Karenzzeit* still
  needs a six-month prognosis or the six-month fiction before anything is due.
- ***Rückwirkende Leistung*** — once the claim is recognised, the benefit is paid **back to the
  onset of BU** (after any *Karenzzeit*), not from the date of the decision. Combined with the
  six-month fiction this means the first payment on a typical claim is a lump sum covering the
  elapsed months plus the current month.
- **The premium keeps being paid in the meantime**, and is **refunded** for the period covered by
  the retroactive benefit when the *Beitragsbefreiung* is applied retroactively `[unverified]` as to
  whether all AVB do this. delib models the *Beitragsbefreiung* as starting at the same date as the
  benefit and treats the interim premium and its refund as netting to zero.
- **Model consequence and the delib choice.** delib's monthly model pays the *BU-Rente* from the
  first month after onset plus the *Karenzzeit*, at a `[std]` *Karenzzeit* of **0 months** in the
  base run, and does **not** model the decision delay or the catch-up lump. That is a timing
  simplification, stated in `technical-notes.md` as a known pitfall with a test asserting that the
  benefit stream starts where the notes say it does.

### 8. Leistungsdauer, Versicherungsdauer and the Endalter

- Two ages, and they are not the same thing:
  - ***Versicherungsdauer*** — the period during which a BU can incept and be covered. A BU
    beginning after it ends is not covered at all.
  - ***Leistungsdauer*** — the period over which benefit is paid on a covered claim. Payment stops
    at the *Leistungsendalter* even if the insured is still *berufsunfähig*.
- In the market standard the two are **equal**, and both end at the agreed *Endalter*. Where they
  differ, the *Leistungsdauer* is the shorter — a cheaper design in which cover runs to 67 but
  benefit stops at, say, 60 `[unverified]` as to how common that is.
- **The *Endalter* is 65 or 67**, and the market's advice is 67 because that is the statutory
  retirement age for cohorts born from 1964 `[unverified]`. Anything earlier leaves a gap between
  the end of the *BU-Rente* and the start of the old-age pension. Lower *Endalter* — 60, 62, 63 —
  are sold as budget options and are heavily discounted, because the last years before retirement
  carry by far the highest *Invalidisierungswahrscheinlichkeiten*.
- **The premium is extremely sensitive to the *Endalter*.** Moving the *Endalter* from 67 to 60
  removes the seven most expensive years of cover and, on the shape of the DAV 1997 I curve,
  removes a large share of the expected claim cost `[unverified]` as to the magnitude. This is the
  single most effective premium lever in the product and the one consumer advice warns hardest
  against using.
- **A claim in payment at the *Leistungsendalter* simply stops.** There is no commutation, no
  residual value and no conversion to an old-age annuity in the standalone product. In a BUZ on a
  *Rentenversicherung* the host contract's annuity then begins, which is exactly why the rider form
  is sold.

### 9. Beitragsbefreiung

- While the *BU-Rente* is in payment, the **premium is waived**. This is not an option; it is part
  of the core cover in every German BU contract.
- In an **SBU** the waiver covers the SBU's own premium. In a **BUZ** it covers the **entire**
  premium of the host contract as well — which is the rider form's main attraction, because it keeps
  the retirement provision running through a disability [S2].
- The waiver starts with the benefit and ends with it, including through the three-month run-off:
  during the run-off the insured is still receiving benefit and is still premium-free `[unverified]`
  as to whether all AVB align the two exactly.
- On *Reaktivierung* the premium **resumes at the same *Zahlbeitrag***, not at a repriced one. The
  insured has not aged into a higher tariff, because the tariff is level.
- **Model consequence.** The *Beitragsbefreiung* is not a benefit cash flow; it is the **absence of
  a premium cash flow** in the disabled state. In a multi-state monthly model this falls out
  automatically once premiums are weighted by the active-state count rather than by total in-force.
  Getting it wrong — weighting premiums by all surviving policies — is the classic BU modelling
  error and is pitfall 1 in delib's `technical-notes.md`.
- The *Beitragsbefreiung* is economically **large**. On a claim incepting at age 45 on a contract to
  67, it removes 22 years of premium as well as adding 22 years of annuity. For a typical office
  tariff the waived premium is of the order of 5 % of the annuity paid `[std]`, but for a manual
  trade, where the premium is three times as large for the same *BU-Rente*, it can approach 15 %.

### 10. Wiedereingliederungshilfe and the assistance benefits

- ***Wiedereingliederungshilfe*** — a **one-off lump sum** paid to support a return to work after a
  period of BU. Typical form: a payment equal to a stated number of monthly *BU-Renten*, recalled as
  up to **six** `[unverified]`, payable once, on *Reaktivierung* or on the insured taking up work
  again.
- Related benefits that appear in the better wordings, all small relative to the annuity and all
  optional or tariff-specific:
  - ***Umorganisationshilfe*** for the self-employed — a payment toward reorganising the business so
    that the insured can continue to run it, which is the commercial counterpart of the
    *Umorganisationspflicht* [R29].
  - ***Reha-Hilfe*** / *Rehabilitationsleistung* — support for rehabilitation measures.
  - ***Soforthilfe*** / *Überbrückungsleistung* — an advance paid while the *Leistungsprüfung* runs,
    set against the eventual benefit.
  - ***Pflegeleistung*** — a *Pflegerente* triggered by care need, sold as an add-on inside a BU
    contract by some carriers.
- **Model consequence and the delib choice.** delib models the *Wiedereingliederungshilfe* as a
  `[std]` lump of **6 × the monthly *BU-Rente*** paid on each *Reaktivierung*, switchable off, and
  models none of the others. Rationale: it is the only one of the group that is both common enough
  to be representative and simple enough to attach to an existing transition. The others are either
  discretionary, tiny, or duplicate a benefit already modelled. The 6-month level is `[std]`,
  observed range recalled as **3 to 12 monthly Renten** `[unverified]`.

### 11. The Arbeitsunfähigkeits-Klausel (AU-Klausel)

- **What it does.** The *AU-Klausel* pays the full *BU-Rente* on production of a **doctor's
  certificate of continuous *Arbeitsunfähigkeit*** — inability to work in the current job — of a
  stated duration, **without the insurer determining that BU exists**. The certified duration is
  normally **six months**, either already elapsed or elapsed plus certified to continue
  `[unverified]`.
- **Why it exists.** The *Leistungsprüfung* for BU takes months (section 5) and the insured has no
  income in the meantime. The *AU-Klausel* converts a long, contested, prognosis-based assessment
  into a short, documentary one. It has become the principal wording-quality differentiator in the
  contemporary German BU market and is heavily weighted in the ratings [R21] [R22].
- **How it is bounded.** Insurers limit the exposure in three ways, and the combination varies by
  tariff `[unverified]` throughout:
  1. **A maximum benefit period under the clause** — recalled as **18, 24 or 36 months**, or in some
     tariffs an unlimited AU benefit for as long as the certificates continue.
  2. **Set-off.** Payments under the clause are set against the eventual BU decision; if BU is later
     denied, the payments are usually **not** reclaimed, which is what makes the clause valuable.
  3. **A requirement to continue pursuing the BU claim** in parallel, and to supply certificates at
     stated intervals.
- **Model consequence.** The *AU-Klausel* raises the **effective inception rate** and shifts the
  **timing** of payment forward, without changing the annuity amount. delib models it as an option
  switch that (a) multiplies the inception rate by a `[std]` factor and (b) removes any decision
  delay — and, because delib already pays from onset (section 7), in the base parameterisation the
  second effect is nil and only the first survives. The `[std]` inception uplift is set at
  **1.00 in the base run (clause off)** with the switched-on value left as a model-point parameter,
  because no public data quantifies the uplift and inventing one would be worse than declaring it
  unknown (gap 12).

### 12. Options — Beitragsdynamik and Leistungsdynamik

Two escalations, on different quantities, at different times, and routinely confused.

- ***Beitragsdynamik*** (also *Anwartschaftsdynamik*, *Dynamik in der Anwartschaftszeit*) — a
  **pre-claim** annual increase of the **premium**, with a corresponding increase of the insured
  *BU-Rente*, **without renewed *Gesundheitsprüfung***.
  - Agreed rate: commonly **3 % or 5 %** of the premium a year, with menus from **1 % to 10 %**
    `[unverified]`.
  - The *BU-Rente* increase corresponding to a given premium increase is **less than proportional
    and falls with age**, because the additional premium buys cover at the attained age for the
    remaining term.
  - The policyholder may **decline** an individual increase. Declining a stated number of
    consecutive increases — recalled as **two or three** `[unverified]` — extinguishes the option
    permanently, which is the insurer's protection against anti-selection.
  - **Model consequence.** A *Beitragsdynamik* makes both the premium and the sum at risk
    time-varying and introduces a **take-up assumption**. delib ships it off in the base run and
    available as a model-point switch with a `[std]` take-up.
- ***Leistungsdynamik*** (*Rentendynamik im Leistungsfall*, *Leistungsdynamik im Leistungsbezug*) —
  an **in-claim** annual increase of the *BU-Rente* **while it is being paid**, protecting the
  benefit against inflation over what can be a 30-year payment period.
  - Agreed rate: commonly **1 %, 2 % or 3 %** a year `[unverified]`; some tariffs index to a
    published inflation measure instead of a fixed rate.
  - It is paid for in the premium from inception, not on claim.
  - **This is the more important of the two for a liability projection**, because it compounds over
    the whole benefit period. On a claim incepting at 40 and running to 67, a 2 % *Leistungsdynamik*
    raises the final payment to about **1.70×** the initial one and the total benefit paid by roughly
    a third relative to a level annuity `[std]` — arithmetic, not a source.
  - **delib's base run carries a *Leistungsdynamik* of 2 % a year** `[std]`, applied annually on the
    anniversary of the benefit start, because a BU model without in-claim escalation misses the
    product's dominant long-duration sensitivity. The 2 % is the midpoint of the recalled
    1 %–3 % menu, and the level is a `[std]` choice, not a citation.

### 13. Options — Nachversicherungsgarantie and Verlängerungsoption

- ***Nachversicherungsgarantie*** — the right to **increase the insured *BU-Rente*** without a fresh
  *Gesundheitsprüfung*, on the occurrence of a defined event. It is the single most valuable option
  in the German BU product, because it lets a healthy 25-year-old lock in insurability cheaply and
  build the cover later as income grows.
  - **Event-linked** (*ereignisabhängig*) triggers, near-uniform across the market: marriage or
    registered partnership; birth or adoption of a child; completion of studies or vocational
    training; a first job or a substantial pay rise; purchase of a property or taking out a
    mortgage; starting self-employment; the birth of a child in the insured's household; and, in
    some tariffs, the death of a partner or a divorce.
  - **Event-independent** (*ereignisunabhängig*) windows exist in some tariffs — a right to increase
    in each of the first N years regardless of any event `[unverified]`.
  - **Caps**, all `[unverified]` in level: a maximum increase per event (often expressed as a
    percentage of the original *BU-Rente*); an aggregate cap (often that the *BU-Rente* may at most
    be **doubled** relative to the original); an absolute ceiling on the resulting *BU-Rente*; an
    age limit for exercise; and an *Angemessenheitsgrenze* requiring the total *BU-Rente* to stay
    within a stated fraction of income (section 17).
  - **Anti-selection is controlled by the event list and the exercise window** — typically a right
    exercisable within **6 or 12 months** of the event `[unverified]` — not by underwriting.
  - **Model consequence.** delib ships the *Nachversicherungsgarantie* **off** in the base run. Any
    on-run needs a take-up assumption and an anti-selection loading on the incremental cover, and
    neither is sourceable. It is described in `product-spec.md` and named in `technical-notes.md` as
    an unmodelled option, which is the honest treatment.
- ***Verlängerungsoption*** — the right to **extend the *Versicherungs-* and *Leistungsdauer***, for
  example from 63 to 65 or from 65 to 67, without renewed underwriting. Sold to protect against a
  further rise in the statutory retirement age. Exercise is normally confined to a window before the
  original *Endalter* `[unverified]`. Modelled by delib as a model-point parameter on the *Endalter*
  rather than as a dynamic option.

### 14. The Infektionsklausel

- **The problem it solves.** A doctor, dentist, nurse or laboratory worker who is infected or is a
  carrier may be forbidden by the competent authority to practise, under a *Tätigkeitsverbot*
  imposed by the *Infektionsschutzgesetz* [R30]. She then cannot earn in her occupation — but she is
  not necessarily unable to work in the sense of § 172 VVG, so the ordinary BU definition may not
  bite.
- **What the clause does.** It **deems** the official prohibition to be BU, so that the *BU-Rente*
  becomes payable for as long as the ban lasts, without a 50 % medical test.
- **Who gets it.** Standard for physicians and dentists; common for nursing staff, medical and
  dental assistants, midwives and laboratory personnel; not offered outside the medical field.
  Tariffs marketed specifically at medical professions treat it as a headline feature
  `[unverified]`.
- **Bounding.** Some wordings require the ban to be **complete** rather than partial, or to have
  lasted a stated period; some pay only for the duration of the ban and end the benefit when it is
  lifted, which makes the *Nachprüfung* mechanical rather than medical `[unverified]`.
- **Model consequence.** delib does **not** model the *Infektionsklausel* separately. It is
  described in the product specification as a rating and definition variant applying to a specific
  occupational segment, and its effect on the model is a higher inception rate in that segment —
  which is already how *Berufsgruppen* enter (section 16). Modelling it as a distinct trigger would
  require a ban-incidence assumption that no public source supplies.

---
