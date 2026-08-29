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
