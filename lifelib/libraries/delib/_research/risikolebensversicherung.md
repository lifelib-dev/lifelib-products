# Risikolebensversicherung (term life) — research notes (Germany)

Research notes for the German individual *Risikolebensversicherung* (RLV) — the pure protection
contract that pays a *Todesfallleistung* (death benefit) equal to the agreed *Versicherungssumme*
if the *versicherte Person* dies inside the *Versicherungsdauer*, and pays **nothing at all**
otherwise. It is the German market's cheapest and structurally simplest life contract, and it is
the only one of the ten delib products with no accumulation phase, no *Erlebensfallleistung* and,
in the ordinary case, no *Rückkaufswert*.

**In scope.** The individual, privately written, *selbständige* (standalone) term assurance on one
or two lives, with a **level *Bruttobeitrag*** over the whole *Beitragszahlungsdauer*, an
*Überschussbeteiligung* applied as ***Beitragsverrechnung*** so that the customer pays a
***Zahlbeitrag*** materially below the *Bruttobeitrag*, a *Versicherungssumme* that is **konstant**,
**linear fallend** or **annuitätisch fallend**, medical underwriting through *Gesundheitsfragen*
with *Raucher*/*Nichtraucher* differentiation and *Risikozuschläge*, the three-year *Selbsttötung*
window of § 161 VVG, and a *Nachversicherungsgarantie* on named life events. Both the single-life
form and the *verbundene Leben* (two lives, one payment on the first death) form are treated as one
chassis parameterised by the number of lives. The *Über-Kreuz-Versicherung* — the same economic
cover arranged so that each partner insures the other's life and is his own *Bezugsberechtigter* —
is a **contracting structure**, not a different product, and is covered here because it changes the
tax outcome and nothing else.

**Out of scope, and said so where it matters.**

- *Restschuldversicherung* / *Restkreditversicherung* (RSV) — the single-premium, bank-sold,
  loan-linked group death-and-unemployment cover. It shares the falling sum insured of the
  *annuitätisch fallende* RLV and nothing else: it is sold as *Gruppenversicherung* through the
  lender, is underwritten by a health declaration or not at all, and its charge structure and
  mis-selling history are a separate subject. Where this file names a falling sum insured, it means
  a **standalone** RLV whose schedule was chosen to shadow a loan, not an RSV.
- *Sterbegeldversicherung* — small-sum whole-of-life funeral cover with a *Wartezeit* and no
  *Gesundheitsprüfung*. It has an *Erlebensfall*-like certainty of payment, builds a
  *Deckungskapital* and carries a *Rückkaufswert*; it is out of the delib library entirely.
- *Risikolebensversicherung mit Beitragsrückgewähr* — the variant returning premiums on survival.
  It has a savings element by construction and is economically a *Kapitallebensversicherung*
  (delib product 1) with an unequal death and survival sum.
- The *Berufsunfähigkeits-Zusatzversicherung* (BUZ) and *Unfalltod-Zusatzversicherung* (UZV) riders
  that are commonly attached to an RLV. The standalone *Berufsunfähigkeitsversicherung* is delib
  product 9; the rider forms are described here only as options, and neither is modelled.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung*, and
  *Kollektivverträge* through associations or employers, which are outside the delib library.
- Austrian and Swiss *Risikoversicherung* documents. The VVG, the DeckRV, the MindZV and the ErbStG
  do not apply to them.

These notes are the **citation ground truth** for the delib `risikolebensversicherung` product
documents — `product-spec.md`, `technical-notes.md`, `model.md` and `sources.md`. Source ids
**S1..S17** and **R1..R23** below are **frozen — never renumber**; unused ids are simply omitted
downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

This section states, in the same terms used in every other delib document, the two limits under
which this file was written. A reader who picks up only this file must learn them from this file.

**No document named in this file was retrieved.** Direct HTTP egress from this build environment is
blocked by an organisation network policy: `WebFetch` and `curl` are refused (HTTP 403 at the egress
gateway) for every host outside a short package-registry allowlist. The hosts that matter for this
product were tried and refused — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de` and `de.wikipedia.org`. Not
one *Allgemeine Versicherungsbedingungen* PDF, not one *Produktinformationsblatt*, not one
*Verbraucherinformation*, not one statutory text and not one comparison-portal rate table was
opened.

**The session's `WebSearch` budget was already exhausted before this product's research began.**
The session shares a hard cap of 200 `WebSearch` calls across all its work. That cap was reached
during the research for the two products written before this one — `kapitallebensversicherung` and
`klassische_rentenversicherung` — and **zero searches were available for `risikolebensversicherung`**.
Every search attempted returns the budget-exhausted message. This is materially worse than the
position of the two sibling files, which at least had search-result summaries to work from, and it
is worse again than `frlib/_research/temporaire-deces.md`, where the French *notices d'information*
were downloaded and read in full.

**What this file therefore is.** It is a statement of German term-assurance law, product structure
and market practice written from the author's own knowledge, disciplined in three ways:

1. **Documents are named as known references, not as evidence.** Each `S#` and `R#` entry names a
   document that **exists and is the right kind of document** for the claim beside it — an insurer's
   AVB, a GDV *Musterbedingung*, a statutory section, a DAV *Fachgrundsatz*. Each carries
   `Retrieved: no — direct HTTP egress blocked; no search corroboration (session search budget
   exhausted)` unless it inherits a search corroboration through the route in point 2. **No document
   number, edition date, page count or *Bundesgesetzblatt* citation is stated unless it is
   inherited**; where a URL is not known it says `URL: not established`, and a canonical form given
   from confident knowledge is marked `[unverified]`.
2. **One inherited evidentiary spine.** Several instruments this product turns on — § 161, § 169,
   § 165 and § 19 VVG, the MindZV, the DeckRV, VAG § 139 and the DAV 2008 T *Richtlinie* — **were
   search-corroborated for the two sibling products while budget remained**, and their findings are
   recorded in `delib/_research/kapitallebensversicherung.md` and
   `delib/_research/klassische_rentenversicherung.md`. Where a fact here rests on that inherited
   corroboration the entry says **"inherited corroboration"** and names the sibling file and its
   source id. This is a real, if second-hand, evidentiary chain and it is the strongest evidence in
   this file. Everything not so marked has **no** corroboration.
3. **Numbers become `[std]`, not citations.** Where the mechanic is certain and the level is not —
   the *Brutto*/*Zahlbeitrag* ratio, the *Sicherheitszuschlag* in the first-order mortality basis,
   the *Ratenzahlungszuschlag*, the *Stornoquote*, the premium rates themselves — this file ships a
   **`[std]` parameter with a stated rationale and an argued plausible range**, and puts the missing
   figure in the gaps register. A `[std]` number is honest. A guessed `[S7]` number is not, and
   there are none in this file.

**`[unverified]` keeps its normal meaning and is used generously.** It marks any specific paragraph
number, effective date, monetary amount, percentage, price point or market figure that no search
result confirmed. It is **not** applied to the general shape of a well-established mechanic — that
would drown the signal — but the moment a claim becomes specific and numeric it carries either an
inherited corroboration or the tag.

**What is not in this file, and would be in a properly researched one.** No insurer's AVB text. No
*Produktinformationsblatt*. No published *Bruttobeitrag* / *Zahlbeitrag* pair. No comparison-portal
price point. No *Nachversicherungsgarantie* event list taken from a wording. No smoker/non-smoker
price ratio taken from a rate card. No GDV market statistic for the *Risikoversicherung* segment.
Each of these is a numbered gap at the foot of this file, and the product specification built from
these notes must carry the corresponding `[std]` tag rather than a citation.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. Tables and headings are
in English; the prose is English about German products. The terms this product turns on:

| Term | Gloss |
|---|---|
| *Risikolebensversicherung* (RLV), *Risikoversicherung* | Term assurance: death cover for a fixed period, no survival benefit |
| *Todesfallleistung* | The death benefit, payable to the *Bezugsberechtigter* on death inside the term |
| *Versicherungssumme* (VS) | Sum insured. May be *konstant*, *linear fallend* or *annuitätisch fallend* |
| *Versicherungsdauer* / *Beitragszahlungsdauer* | Cover period / premium-paying period; equal in the ordinary tariff, the second optionally shorter |
| *Eintrittsalter* / *Endalter* | Age at entry / age at which cover ends |
| *Bruttobeitrag*, *Tarifbeitrag* | The tariff premium: the **guaranteed maximum** the policyholder can ever be asked to pay |
| *Zahlbeitrag*, *Nettobeitrag* (consumer sense) | The premium actually billed = *Bruttobeitrag* less the *Beitragsverrechnung*. **Not guaranteed** |
| *Nettoprämie* / *Nettobeitrag* (actuarial sense) | The risk premium before expense loadings. **A different quantity from the consumer *Nettobeitrag*** — see the warning in mechanic 4 |
| *Nettotarif*, *Honorartarif* (distribution sense) | A commission-free tariff sold through fee-based advice. **A third, unrelated sense of "netto"** |
| *Beitragsverrechnung*, *Sofortverrechnung*, *Sofortrabatt* | The *Überschussverwendung* form that nets the declared surplus against the *Bruttobeitrag* |
| *Überschussbeteiligung* / *Überschussanteile* | The statutory entitlement to share in the insurer's surplus (§ 153 VVG) / the amounts actually allocated |
| *Deklaration* | The insurer's annual declaration of the surplus rates for the coming year |
| *Risikoüberschuss* / *Kostenüberschuss* / *Zinsüberschuss* | Mortality surplus / expense surplus / interest surplus. On an RLV the first dominates and the third is negligible |
| *Rückstellung für Beitragsrückerstattung* (RfB) | The provision through which surplus is held before allocation |
| *Rechnungsgrundlagen erster / zweiter Ordnung* | First-order (prudent, tariff and reserving) / second-order (best-estimate) bases |
| *Sicherheitszuschlag* | The prudential margin loaded onto the best-estimate decrement to give the first-order one |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate / its statutory maximum for new business |
| *Deckungsrückstellung* / *Deckungskapital* | The balance-sheet actuarial provision / the reserve of one contract |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs through the reserve / the statutory cap on the amount so financed |
| *Rückkaufswert* | Surrender value. **Absent on the ordinary RLV** — see mechanic 11 |
| *Beitragsfreistellung*, *prämienfreie Versicherung* | Making the contract paid-up; the resulting reduced sum is the *beitragsfreie Versicherungssumme* |
| *Gesundheitsprüfung* / *Gesundheitsfragen* | Medical underwriting / the health questions asked in the application |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure (§ 19 VVG) |
| *Risikozuschlag* / *Leistungsausschluss* | Extra-mortality premium loading / an exclusion written into the individual contract |
| *Berufsgruppe* | Occupation class used for rating |
| *Raucher* / *Nichtraucher* | Smoker / non-smoker, the market's largest single rating split after age |
| *Nachversicherungsgarantie* | The right to raise the sum insured on a named life event **without a new *Gesundheitsprüfung*** |
| *Dynamik*, *Beitragsdynamik*, *Summendynamik* | Automatic annual escalation of premium and sum insured, with a right of *Widerspruch* |
| *Verbundene Leben* | Two *versicherte Personen* on one contract, one payment on the first death |
| *Über-Kreuz-Versicherung* | The cross-contracting structure: each partner is *Versicherungsnehmer* on the other's life and his own beneficiary |
| *Versicherungsnehmer* (VN) / *versicherte Person* (vP) / *Bezugsberechtigter* | Policyholder / life insured / beneficiary. On an RLV these are routinely three different roles |
| *Selbsttötung* | Suicide (§ 161 VVG) |
| *Kriegsklausel* | The war clause in the AVB, restricting the benefit where death is connected with war |
| *Vorläufiger Versicherungsschutz* | Provisional cover between application and acceptance |
| *Wartezeit* | Waiting period before cover attaches. **Normally absent on an RLV** |
| *Restschuldabsicherung* / *Darlehensabsicherung* | Cover shaped to a loan's outstanding balance |
| *Erbschaftsteuer* / *Freibetrag* / *Steuerklasse* | Inheritance tax / personal allowance / relationship class determining allowance and rate |
| *Erwerb von Todes wegen* | Acquisition by reason of death — the ErbStG charging concept the *Über-Kreuz* structure is built to avoid |
| *Stornoquote* | Lapse rate |
| *Allgemeine Versicherungsbedingungen* (AVB) / *Verbraucherinformation* / *Produktinformationsblatt* (PIB) | The policy conditions / the consumer information pack / the short pre-contractual product summary |

---

## Primary sources

Every entry below carries the same retrieval status, stated once here rather than repeated
seventeen times: **Retrieved: no — direct HTTP egress blocked in the build environment; no search
corroboration (the session `WebSearch` budget was exhausted before this product's research began).**
Where an entry inherits corroboration from a sibling delib research file, that is stated in the
entry.

The entries are ordered: GDV model wordings (S1–S2), carrier documents (S3–S13), then secondary
consumer, comparison and rating material (S14–S17). **Every carrier named below sells a
*Risikolebensversicherung* in Germany; that much is asserted from knowledge. Nothing about the
content of any particular wording is asserted, because nothing was read.**

### S1 — GDV, "Allgemeine Bedingungen für die Risikoversicherung" (*Musterbedingungen*)

- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: *Musterbedingungen* — model AVB published by the industry association for member
  undertakings to adopt, adapt or ignore
- URL: **not established** for the term-assurance wording itself. The GDV *Musterbedingungen* index
  at `https://www.gdv.de/gdv/service/musterbedingungen` was returned by a search during the sibling
  research and is recorded there [inherited: `kapitallebensversicherung.md` S1]; the per-document
  blob path for the *Risikoversicherung* wording is **not established** and is not guessed
- Content — what this document is, and what weight an `[S1]` tag carries:
  - The GDV maintains model conditions for the main German life lines, and the *Risikoversicherung*
    is one of them. The model wordings address the customer in the second person with
    question-headed sections ("Welche Leistungen erbringen wir?", "Wann beginnt Ihr
    Versicherungsschutz?"), the style the GDV adopted for post-2008-VVG wordings [inherited:
    `kapitallebensversicherung.md` S1].
  - The GDV states its model conditions are ***unverbindlich*** for undertakings and their use
    **purely optional** — a competition-law disclaimer that is load-bearing for citation weight
    [inherited: `kapitallebensversicherung.md` S1]. **An `[S1]`-tagged fact is a market template,
    weaker evidence about any carrier than the same fact taken from that carrier's own AVB.**
  - **No article text of the term-assurance model wording was established.** Every benefit,
    surplus, exclusion or termination rule attributed anywhere in this file to "the model
    conditions" is attributed instead to the statute it implements [R1]–[R8] or is carried as
    `[std]`, never to S1.

### S2 — GDV, *Produktinformationsblatt* pattern for the *Risikoversicherung*

- Publisher: GDV. Doc type: model *Produktinformationsblatt* (PIB) — the short pre-contractual
  summary required for life products by the VVG-InfoV [R17]
- URL: **not established**
- Content: recorded at the level of identity only. The PIB is the German counterpart of the French
  *document d'information sur le produit d'assurance*: a short document naming the product type, the
  insured risk, the *Versicherungssumme*, the *Beitrag*, the exclusions and the term. For a
  *Risikolebensversicherung* it is the natural place a carrier states the ***Bruttobeitrag* and the
  *Zahlbeitrag* side by side**, which is why it matters here more than for any other delib product.
  **No specimen was located and no field list is asserted**; the inference from the document's
  purpose is `[unverified]` (gap 3).

### S3 — CosmosDirekt (Cosmos Lebensversicherungs-AG), *Risikolebensversicherung* — AVB, *Verbraucherinformation* and product page

- Publisher: Cosmos Lebensversicherungs-AG (Generali Deutschland group), the direct-writing arm
- Doc type: *Allgemeine Bedingungen für die Risikoversicherung* plus the *Verbraucherinformation*
  pack and the public product page
- URL: **not established.** The carrier's AVB naming convention runs `LA <number> <letter>` — the
  sibling research recorded `LA 904 A` for its *Rentenversicherung* wording [inherited:
  `klassische_rentenversicherung.md` S8] — but **the term-assurance tariff code is not established
  and is not guessed**
- Content: named as the German market's highest-volume direct-written RLV and one of the two or
  three carriers a German price comparison returns first. Relevant because the direct channel is
  where the ***Brutto*/*Zahlbeitrag* spread is widest**: no *Abschlussprovision* is paid to an
  intermediary, so more of the *Bruttobeitrag* is available for *Beitragsverrechnung*. **That
  reasoning is structural, not sourced**, and the spread itself is `[std]` (mechanic 5).

### S4 — Hannoversche Lebensversicherung AG, *Risikolebensversicherung* — AVB and product page

- Publisher: Hannoversche Lebensversicherung AG (VHV group)
- Doc type: AVB for the *Risikoversicherung*; *Verbraucherinformation*; product page
- URL: **not established**
- Content: the other long-standing German direct writer of term assurance, historically a fixture
  near the top of consumer-magazine RLV rankings [S16]. Recorded for the same structural reason as
  S3. **No wording, no tariff code, no rate and no edition date is asserted.**

### S5 — HUK-COBURG / HUK24, *Risikolebensversicherung* — product pages and the *Überschussbeteiligung* guide

- Publisher: HUK-COBURG-Lebensversicherung AG / HUK24 AG
- Doc type: insurer guide page **about term assurance specifically**, plus the product pages
- URL: `https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung`
  — **this URL was returned by a search during the sibling research and is recorded there**
  [inherited: `kapitallebensversicherung.md` S17]
- Content — **the single most useful inherited item in this file**, because it is a carrier's own
  account of the *Überschussbeteiligung* **in this product**, not in the endowment:
  - The page is titled "Überschussbeteiligung der Risikolebensversicherung", so the carrier itself
    treats surplus participation as a **central feature of term assurance**, not as an endowment
    peculiarity. That alone contradicts the intuition an Anglophone modeller brings to a "term life"
    product [inherited: `kapitallebensversicherung.md` S17].
  - The sibling entry records that the page sets out the **four-component surplus vocabulary**
    — *Zins-*, *Risiko-*, *Kosten-* and *übrige Überschüsse* — and that this vocabulary is used
    **by carriers themselves across product lines**, not only by journalists [inherited:
    `kapitallebensversicherung.md` S17].
  - **The sibling file took nothing endowment-specific from it and recorded no figures.** What is
    inherited here is therefore: the existence of the page, its title, and the four-component
    vocabulary. **No rate, no *Beitragsverrechnung* percentage and no *Brutto*/*Zahlbeitrag* ratio is
    inherited**, and none is asserted (gap 1).

### S6 — Debeka Lebensversicherungsverein a. G., *Bedingungswerk* for the *Risikoversicherung*

- Publisher: Debeka Lebensversicherungsverein a. G.
- Doc type: *Bedingungswerk* (Debeka's name for its AVB booklets), in the carrier's public
  *Vertragsgrundlagen* library
- URL: **not established.** The library's path pattern is
  `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/<code>.pdf`,
  established from the sibling research where three endowment wordings were located under it
  [inherited: `kapitallebensversicherung.md` S3–S6]. **The term-assurance wording code is not
  established and no path is guessed.**
- Content: recorded because Debeka is the largest German life mutual by contract count and because
  its *Vertragsgrundlagen* library is one of the few carrier document sets that is fully public and
  indexed by product family [inherited: `kapitallebensversicherung.md` S6]. Two things inherited
  from the sibling research bear on this product: Debeka maintains **several parallel wordings of
  different vintages within one product family** [inherited: `kapitallebensversicherung.md` S3–S5],
  and its *Überschussbeteiligung* clause numbering is **tariff-dependent**, so any specific section
  number is `[unverified]` [inherited: `kapitallebensversicherung.md` S3]. Both cautions transfer
  directly. **No Debeka term-assurance figure is asserted.**

### S7 — Dialog Lebensversicherungs-AG, *Risikolebensversicherung* — AVB and product material

- Publisher: Dialog Lebensversicherungs-AG (Generali Deutschland group)
- Doc type: AVB for the *Risikoversicherung*; *Verbraucherinformation*; broker-facing tariff
  material
- URL: **not established**
- Content: named because Dialog positions itself in the German market as the **specialist term-life
  carrier for the broker channel** — a monoline whose whole book is biometric risk. That matters for
  this file in one specific way: a monoline's *Risikoergebnis* is its entire technical result, so the
  MindZV minimum allocation from the *Risikoergebnis* [R9] binds its surplus policy directly rather
  than being one of three competing calls on it. **The positioning is asserted from knowledge; no
  wording, tariff, rate, *Berufsgruppen* table or surplus declaration is asserted** (gap 5).

### S8 — Allianz Lebensversicherungs-AG, *Risikolebensversicherung* — AVB and product page

- Publisher: Allianz Lebensversicherungs-AG
- Doc type: AVB for the *Risikoversicherung*; *Produktinformationsblatt*; product page
- URL: **not established**
- Content: the German market leader by premium income, and the natural reference point for the
  **narrow-spread** end of the *Brutto*/*Zahlbeitrag* distribution — a large composite with a broker
  and tied-agent distribution has less room to net surplus against the tariff premium than a direct
  writer. **That is a structural argument, not an observation** (gap 1). One inherited fact bears on
  the whole family of Allianz life wordings: the sibling research established Allianz's declared
  *laufende Verzinsung* for 2026 at **2.70 %** for the classic book, above the market average
  [inherited: `kapitallebensversicherung.md` S11] — a **savings-side** rate, of no direct use for an
  RLV, where the *Zinsüberschuss* is negligible (mechanic 5).

### S9 — R+V Lebensversicherung AG, *Risikolebensversicherung*

- Publisher: R+V Lebensversicherung AG (cooperative banking group)
- Doc type: AVB; *Produktinformationsblatt*; product page
- URL: **not established**
- Content: named as one of the largest German life carriers and the bank-channel comparator.
  **Nothing about its term-assurance wording, rating structure or surplus declaration is asserted.**

### S10 — Nürnberger Lebensversicherung AG, *Risikolebensversicherung*

- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB; *Verbraucherinformation*
- URL: **not established.** The carrier's tariff-code convention is visible in the sibling research,
  which recorded an annuity wording headed "…nach Tarif NIR3301" [inherited:
  `klassische_rentenversicherung.md` S9]. **The term-assurance tariff code is not established.**
- Content: named as a broker-channel carrier with a long biometric-risk book. Recorded for the
  variations table only; **no parameter is asserted**.

### S11 — LV 1871 (Lebensversicherung von 1871 a. G.), *Risikolebensversicherung*

- Publisher: Lebensversicherung von 1871 a. G. München
- Doc type: AVB; *Produktinformationsblatt*
- URL: **not established**
- Content: named as a mutual with a broker distribution and a product range that emphasises
  *Nachversicherungsgarantien* and occupational differentiation. **The emphasis is asserted from
  market knowledge; no event list, no age cap, no increase cap and no *Berufsgruppen* table is
  asserted** (gap 7).

### S12 — Continentale Lebensversicherung AG and Europa Lebensversicherung AG, *Risikolebensversicherung*

- Publisher: Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG (same group)
- Doc type: AVB; *Produktinformationsblatt*; product pages
- URL: **not established**
- Content: recorded as a **single entry deliberately**, because the pair is the clearest German
  instance of one group running a broker-channel carrier and a low-cost direct-channel carrier side
  by side in the same product. If a *Brutto*/*Zahlbeitrag* comparison were ever to be made from
  public documents, this pair is where the channel effect would be visible with the underwriting and
  the reserving basis held constant. **No such comparison was made and no figure is asserted.**

### S13 — Further carriers selling a *Risikolebensversicherung* in Germany (located as products, not as documents)

- Publishers: Alte Leipziger Lebensversicherung a. G.; Volkswohl Bund Lebensversicherung a. G.;
  Swiss Life Deutschland; Zurich Deutscher Herold Lebensversicherung AG; ERGO Vorsorge
  Lebensversicherung AG; AXA Lebensversicherung AG; Barmenia Lebensversicherung a. G.;
  Württembergische Lebensversicherung AG; Gothaer Lebensversicherung AG; Die Stuttgarter
  Lebensversicherung a. G.; Baloise Lebensversicherung AG (Deutschland); uniVersa Lebensversicherung
  a. G.; DEVK; SIGNAL IDUNA Lebensversicherung a. G.; Provinzial; Generali Deutschland; HDI
  Lebensversicherung AG
- Doc type: AVB and *Produktinformationsblätter* for the *Risikoversicherung*, one set per carrier
- URL: **not established for any of them**
- Content: **this entry asserts one thing only — that each of these carriers offers an individual
  *Risikolebensversicherung* in Germany.** It is recorded so that the variations table below can
  state honestly that a market of this breadth exists and that **none of it was sampled**. Nothing
  else is taken from S13, and no `[S13]` tag appears on any parameter anywhere in the delib library.
  Two of these carriers appear in the sibling research with located documents in **other** product
  families — Zurich Deutscher Herold with a *Verbraucherinformation* series for annuities
  [inherited: `klassische_rentenversicherung.md` S4–S7] and Gothaer with an endowment AVB [inherited:
  `kapitallebensversicherung.md` S7] — which establishes that their document libraries are public,
  and nothing about their term-assurance wordings.

### S14 — Comparison portals: Check24, Verivox, Tarifcheck

- Publisher: CHECK24 Vergleichsportal GmbH; Verivox GmbH; and comparable portals — **secondary**,
  not product documents
- Doc type: price-comparison result pages and accompanying *Ratgeber* articles
- URL: **not established** for the term-assurance comparison pages. The sibling research recorded
  Verivox *Ratgeber* pages on `Kapitallebensversicherung`, `Überschussbeteiligung` and `Zillmerung`
  [inherited: `kapitallebensversicherung.md` S15], which establishes that the portal publishes
  explanatory pages of this kind; it establishes nothing about its term-assurance pages
- Content: **these portals are the only public source of German RLV price points**, because no
  German carrier publishes a rate card for this product and the *Produktinformationsblatt* quotes
  only the individual applicant's own premium. That is precisely why the brief asked for several
  price points from them, and **precisely what could not be obtained**: a comparison result is
  generated per query and is not a static document, so it cannot be reached without live egress in
  any event. **No price point of any kind is recorded in this file from S14** (gap 1).

### S15 — Finanztip, "Risikolebensversicherung"

- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH — **secondary**
- Doc type: consumer guide article with a periodically refreshed carrier recommendation
- URL: **not established** for the term-assurance article. The sibling research recorded Finanztip
  articles on `Überschussbeteiligung Lebensversicherung` and `Steuer auf Lebensversicherung`
  [inherited: `kapitallebensversicherung.md` S16], establishing the publisher's coverage of this
  subject area and nothing about the term-assurance article
- Content: named because Finanztip is the German consumer publication that most consistently makes
  the ***Brutto*/*Zahlbeitrag* distinction the headline of its term-life advice** — the standing
  recommendation being to compare the *Bruttobeitrag* and not only the *Zahlbeitrag*, because the
  second is what you pay and the first is what you can be made to pay. **The existence of that
  editorial line is asserted from knowledge; no figure, no carrier ranking and no spread statistic
  is asserted** (gap 1).

### S16 — Stiftung Warentest / Finanztest, term-life comparison tests

- Publisher: Stiftung Warentest (*Finanztest*) — **secondary**
- Doc type: periodic comparison test of *Risikolebensversicherung* tariffs, published behind a
  paywall with a free summary
- URL: **not established**
- Content: named as the German market's most influential comparison test for this product. Its test
  design is the reason it matters here: *Finanztest* rates on the **Zahlbeitrag for defined model
  customers** (a stated age, sum insured, term and smoking status) **and separately reports the
  *Bruttobeitrag***, so a published test is the one German document type that would supply exactly
  the paired figures this file lacks. **No edition, no date, no model-customer definition and no
  premium figure is asserted** (gap 1).

### S17 — Rating agencies and analysis houses: Franke und Bornberg, Morgen & Morgen, Assekurata

- Publisher: Franke und Bornberg GmbH; MORGEN & MORGEN GmbH; ASSEKURATA Assekuranz Rating-Agentur
  GmbH — **secondary**
- Doc type: tariff ratings (`FB-Unternehmensrating`, `M&M Rating Risikoleben`), market studies and
  *Bedingungsanalysen*
- URL: **not established** for any term-life rating. The sibling research located Assekurata's
  "24. Marktstudie *Überschussbeteiligungen und Garantien 2026*" and Franke und Bornberg commentary
  on *Basisinformationsblätter* [inherited: `kapitallebensversicherung.md` R25, R27], establishing
  that these houses publish in this field and nothing about their term-life work
- Content: named because these are the houses whose published criteria drive German RLV product
  design. Two of their criteria are load-bearing for a representative specification and are asserted
  from market knowledge, **not from any document**:
  - the ***Brutto*/*Zahlbeitrag* spread is itself a rated criterion** — a tariff whose *Zahlbeitrag*
    sits far below its *Bruttobeitrag* is marked down relative to one with a narrow spread, because
    the spread measures the insurer's unilateral headroom to raise the billed premium;
  - the ***Nachversicherungsgarantie* event list, its caps and its age limit are rated criteria**,
    which is why the market has converged on a recognisable list (mechanic 8).
  Both statements are `[unverified]`, and neither is used as a numeric parameter anywhere.

---

## Regulatory and actuarial references

Same retrieval status as the primary sources: **Retrieved: no — direct HTTP egress blocked; no
search corroboration (session budget exhausted)**, except where an entry states an **inherited
corroboration** from a sibling delib research file. Canonical `gesetze-im-internet.de` URLs are given
in the form `.../vvg_2008/__<n>.html`, which the sibling research confirmed the host uses; where such
a URL was **not** itself returned by a search it is marked `[unverified]`.

### R1 — VVG § 161, *Selbsttötung*

- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008). URL:
  `https://www.gesetze-im-internet.de/vvg_2008/__161.html` — **returned by a search during the
  sibling research** [inherited: `kapitallebensversicherung.md` R4]
- **Inherited corroboration — the strongest single item in this file.** In an insurance **for the
  event of death** the insurer is ***leistungsfrei*** if the *versicherte Person* **intentionally
  takes her own life before three years have elapsed since conclusion of the contract**;
  **exception** where the act was committed **in a state excluding free determination of the will,
  caused by a *krankhafte Störung der Geistestätigkeit***; **the three-year period may be extended by
  individual agreement**, so it is a statutory minimum, extendable and by implication not
  shortenable; and **where the insurer is *leistungsfrei* it must nevertheless pay the
  *Rückkaufswert*, including *Überschussanteile*, under § 169**. Located in **Chapter 5** of the VVG.
- **Why it bites harder here than on an endowment.** On a *Kapitallebensversicherung* the
  substitution is soft — the *Rückkaufswert* after three years is a real sum. On a
  *Risikolebensversicherung* it is nil or nominal (mechanic 11), so the substitution is in economic
  substance **a forfeiture with a rounding error attached**. The model must carry the rule as a
  **benefit switch**, not as a decrement adjustment.
- Whether the three-year clock **restarts on an increase** of the sum insured, as the French one-year
  clock expressly does, is **not established from the statute**; German AVB practice is understood to
  restart it for the increment. `[unverified]` (gap 9).

### R2 — VVG § 169, *Rückkaufswert*

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R2]
- **Inherited corroboration**: the section governs the surrender value payable on the policyholder's
  termination; **Abs. 3** provides the ***Mindestrückkaufswert***, computed on the basis that
  acquisition costs are spread over the **first five years**; the value is the *Deckungskapital*
  computed by recognised actuarial rules; a *Stornoabzug* may be deducted only where it is **agreed,
  reasonable and quantified in the contract** [inherited: `kapitallebensversicherung.md` R2, R22, R24].
- **The scope limitation that decides this product.** § 169 Abs. 1 confines the surrender-value duty
  to a life insurance whose insured event is **certain to occur** — the German formulation turns on
  whether the *Eintritt der Leistungspflicht* is *gewiss*. An endowment, an annuity and a
  whole-of-life cover satisfy it; **a *Risikolebensversicherung* does not**, because the insured may
  survive the term and the insurer may never owe anything. **The consequence is that the RLV has no
  statutory *Rückkaufswert*.** This limitation is asserted from knowledge of the section's structure
  and **no search returned that wording**: it is `[unverified]` and is **the most consequential such
  tag in this file** (gap 2). Its practical result — nothing is paid on *Kündigung* — is corroborated
  by uniform market practice and is not in doubt.

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R3]
- **Inherited corroboration**: the policyholder may **at any time, for the end of the current
  *Versicherungsperiode*, demand conversion into a *prämienfreie Versicherung***; the reduced benefit
  is computed by recognised actuarial rules; the insurer may make the same *Stornoabzug* as on
  surrender; and the right is subject to a **minimum-benefit test** — where the resulting
  *beitragsfreie Versicherungsleistung* would fall below an agreed minimum, the insurer pays the
  *Rückkaufswert* instead.
- **Effect here: the right exists in form and is empty in substance.** The *Deckungskapital* of a
  level-premium RLV is small and, after *Zillmerung*, zero or negative through much of the term
  (mechanic 10), so the paid-up sum fails the minimum test in most durations and the fallback is a
  payment of nil. Whether § 165 carries the same *gewiss* limitation as § 169 Abs. 1 was **not
  established** (gap 2); it makes no practical difference, both routes terminating in nil. What
  carriers offer instead — *Beitragsstundung*, a temporary *Ruhen*, a reduction of the sum insured —
  is `[unverified]` (gap 10).

### R4 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and *Anfechtung*

- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R5]; the `__20`, `__21`, `__22` forms
  are `[unverified]`
- **Inherited corroboration on § 19**: **Abs. 1 Satz 1** obliges the policyholder to disclose the
  *gefahrerhebliche Umstände* known to her **which the insurer has asked about in *Textform*** — **the
  duty is question-bounded**, with no free-standing duty to volunteer. The provision gives the insurer
  the right to put health questions and to decide whether to accept **with restrictions** or **only at
  an increased premium**. **Remedies**: on a breach the insurer may **adjust the contract
  retrospectively** — excluding the undisclosed risk, or raising the premium by a ***Risikozuschlag***
  — instead of refusing to perform, and for simple or gross negligence this is the usual outcome.
  **Time limits**: the adjust / terminate / rescind rights **lapse five years** after conclusion for
  negligent breach and **ten years** for **intentional or *arglistig*** breach.
- **Asserted, not inherited, and `[unverified]`**: that § 19 Abs. 5 conditions the insurer's remedies
  on having warned the applicant of the consequences in a separate *Textform* communication; that
  § 21 Abs. 2 defeats the remedy against a claim where the undisclosed circumstance caused neither the
  event nor the extent of the benefit; and that § 22 preserves ***Anfechtung wegen arglistiger
  Täuschung*** alongside the § 19 remedies. On a term product these are the whole of the claims-risk
  story: the underwriting is a questionnaire and the claim risk is whether the answers were true.

### R5 — VVG § 153, *Überschussbeteiligung*

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R1]
- **Inherited corroboration**: the policyholder is **entitled to share in the surplus and in the
  *Bewertungsreserven***; participation may be excluded only by express agreement; the allocation must
  be ***verursachungsorientiert*** — attributed according to how the contract caused the surplus —
  under a procedure recognised by actuarial rules; **Abs. 3** governs the *Bewertungsreserven* share,
  allocated at least annually and payable on termination.
- **Why *verursachungsorientiert* is the load-bearing word here.** An RLV causes essentially **one**
  kind of surplus — the *Risikoüberschuss*. A cause-oriented allocation returns to the RLV book what
  the RLV book earned, and returns it as **a reduction of the premium**, there being no account to
  credit. German *Beitragsverrechnung* is § 153 operating on a product with no savings element
  (mechanic 5). Participation in *Bewertungsreserven* is **structurally negligible** here, because the
  attributable amount scales with a *Deckungsrückstellung* that is nil or nominal `[unverified]`.

### R6 — VVG § 163, *Anpassung der Prämie* (the *Treuhänder* clause)

- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`. The sibling research
  recorded the section as governing premium and condition adjustment in life insurance and located
  market commentary on the *Treuhänderklausel* [inherited: `klassische_rentenversicherung.md` R3, R17,
  R18]
- The insurer may raise a life premium only on an **unforeseen and not merely temporary** change in
  the circumstances underlying the calculation, where the adjustment is necessary to safeguard
  permanent fulfilment, and where an **independent *Treuhänder*** confirms the bases; the policyholder
  may demand a corresponding benefit reduction instead.
- **The distinction that must not be blurred.** § 163 governs increases of the ***Bruttobeitrag***,
  and on a German RLV that route is essentially never used — the *Bruttobeitrag* is guaranteed for the
  term. What moves the customer's bill is the ***Überschussdeklaration***: cutting the
  *Beitragsverrechnung* raises the *Zahlbeitrag* toward the *Bruttobeitrag* with **no § 163 procedure,
  no *Treuhänder* and no policyholder remedy**, because no guaranteed term has changed. **This is the
  single most important legal fact about the German term-life premium** (mechanic 5). That § 163 is
  not used in practice on RLV *Bruttobeiträge* is `[unverified]`.

### R7 — VVG §§ 150, 159, 162 — *versicherte Person*, *Bezugsberechtigung*, *Herbeiführung des Versicherungsfalles*

- URLs: `.../vvg_2008/__150.html`, `__159.html`, `__162.html`, canonical forms, all `[unverified]`
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 150** permits insurance on the life of another; where the benefit **exceeds ordinary funeral
    costs**, the ***schriftliche Einwilligung*** of that person is required. **This is the provision
    the *Über-Kreuz-Versicherung* runs on, and it also binds *verbundene Leben*** (mechanic 14).
  - **§ 159** governs the *Bezugsberechtigung*, revocable by default or ***unwiderruflich***; an
    irrevocable nomination vests the claim immediately and takes it out of the policyholder's
    disposal, with insolvency and tax consequences.
  - **§ 162** makes the insurer *leistungsfrei* where the **policyholder** intentionally and
    unlawfully brings about the death of the *versicherte Person*, and strips a **beneficiary** who
    does so of his entitlement.
- All three are structural on a product where *Versicherungsnehmer*, *versicherte Person* and
  *Bezugsberechtigter* are routinely three different people — the normal case here, not the exception.

### R8 — VVG § 152 (*Widerruf*), § 166 (*Beitragsverzug*), § 168 (*Kündigung*)

- URLs: `.../vvg_2008/__152.html`, `__166.html`, `__168.html`, canonical forms, all `[unverified]`
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 152** extends the general 14-day *Widerrufsfrist* of § 8 to **30 days** for life insurance.
  - **§ 166** governs non-payment of a *Folgeprämie* in life insurance, replacing the general § 38
    machinery: the *Zahlungsaufforderung* must be in *Textform*, must set a deadline of **at least one
    month** and must state the consequences; and the distinctive German step is that **the insurer's
    termination converts the contract into a *prämienfreie Versicherung*** rather than ending it —
    **unless** the paid-up benefit falls below the agreed minimum, when the contract ends.
  - **§ 168** gives the policyholder a right to terminate **at the end of each current
    *Versicherungsperiode*** on a running-premium contract; the period follows the *Zahlweise*, so a
    monthly-paying contract is terminable monthly.
- **Effect here.** § 166's paid-up conversion is the general German lapse path and on an RLV it
  **collapses into simple termination**, because the minimum test fails [R3]. A lapse is a pure exit:
  cover stops, nothing is paid, at most an unearned fraction of a prepaid premium is returned. So
  `claims_surr` is structurally zero, and § 168's period rule means exits are not concentrated at
  policy anniversaries.

### R9 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*

- URLs: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` ·
  `https://www.buzer.de/gesetz/12013/a198221.htm` — both returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R6]
- **Inherited corroboration — the second load-bearing item in this file.** The minimum allocation to
  the *Rückstellung für Beitragsrückerstattung* is **90 % of the *Risikoergebnis*** attributable to
  *überschussberechtigte* contracts; **90 % of the *anzurechnende Kapitalerträge***, struck **after**
  deducting the *Aufwand für die Diskontierung der Deckungsrückstellung*, which is how the guaranteed
  interest is taken off the top before the policyholder's share; and **50 % of the *übriges
  Ergebnis***, which carries the expense result. An aggregate test combines the three, and the
  minimum is computed **separately for *Altbestand* and *Neubestand***.
- **Section attribution is not settled.** The sibling entry places the investment-result rule at § 6;
  the author's recollection places the investment result at § 4, the *Risikoergebnis* at § 5 and the
  *übriges Ergebnis* at § 6. **The three percentages are inherited and used; the section numbers are
  `[unverified]` and are cited nowhere in the delib library** (gap 4).
- **Why this regulation is the engine of the German term product.** An RLV has no meaningful
  investment result and a modest expense result; its technical outcome is almost entirely
  *Risikoergebnis*, and **90 % of that must go back to policyholders**. The insurer prices on a
  prudent first-order mortality basis, earns a large margin against a medically selected portfolio,
  and must return the overwhelming majority of it. *Beitragsverrechnung* is how it does so, and the
  width of the *Brutto*/*Zahlbeitrag* spread is to a first approximation **a direct function of how
  prudent the first-order basis is** (mechanic 5).

### R10 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*

- URL: `https://www.buzer.de/gesetz/12006/index.htm` — returned by a search during the sibling
  research, which used it for the amendment history [inherited: `kapitallebensversicherung.md` R7]
- **Inherited corroboration**: the ***Höchstrechnungszins*** was raised **from 0,25 % to 1,00 % with
  effect from 1 January 2025**, three independent search results agreeing on the sequence **4 % in
  1994 → 0,25 % in 2022 → 1,00 % in 2025**, the 2025 move being the **first increase since 1994**. The
  ***Höchstzillmersatz*** may not exceed **25 ‰ of the *Beitragssumme***, cut **from 40 ‰** by the
  LVRG with effect from **1 January 2015**.
- **Effect here.** The *Rechnungszins* is close to irrelevant to an RLV — the *Deckungsrückstellung*
  is small and short-lived, so a 75-basis-point change moves the *Bruttobeitrag* very little. The
  *Höchstzillmersatz* is the opposite: 25 ‰ of the *Beitragssumme* of a term contract is a large
  number relative to that contract's tiny reserve, and it is why a *gezillmerte*
  *Risikolebensversicherung*'s *Deckungskapital* is **negative or nil for much of its term** (mechanic
  10). Whether the cap applies to a term product in the same way as to a savings contract was **not
  established** `[unverified]` (gap 11).

### R11 — VAG §§ 138–140 — *Gleichbehandlung*, *Überschussbeteiligung*, RfB

- URL: `https://dejure.org/gesetze/VAG/139.html` — returned by a search during the sibling research
  [inherited: `kapitallebensversicherung.md` R8]; the § 138 and § 140 forms are `[unverified]`
- **Inherited corroboration on § 139**: policyholders are **in principle to share in the
  *Bewertungsreserven* to the extent of one half**; participation by **exiting** policyholders is
  permitted **only to the extent that the *Bewertungsreserven* exceed the *Sicherungsbedarf*** arising
  from contracts with an interest guarantee; and *Sicherungsbedarf* is the sum, over contracts with an
  *überhöhter Rechnungszins*, of the actuarially valued interest obligation less the
  *Deckungsrückstellung*.
- **Asserted and `[unverified]`**: that § 138 imposes the ***Gleichbehandlungsgrundsatz*** — equal
  treatment of policyholders in equal circumstances in premium-setting and surplus allocation — and
  that § 140 governs the RfB, including withdrawals from it.
- **Effect here.** § 139's *Bewertungsreserven* mechanics are economically empty on this product
  [R5]. **§ 138 is the one that binds**: it is why an insurer declares **one *Beitragsverrechnung*
  rate per tariff generation and rating cell** rather than negotiating individual discounts, and
  therefore why the *Zahlbeitrag* can be modelled as a deterministic function of the *Bruttobeitrag*
  and a declared rate.

### R12 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"

- Publisher: Deutsche Aktuarvereinigung e. V. Doc type: *DAV-Richtlinie* / *Fachgrundsatz*, with a
  2008 derivation paper and a 2022 restatement. URLs, all returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R14]:
  `https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/` ·
  `https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf`
- **Inherited corroboration — the third load-bearing item, and *the* table for this product**:
  - The DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* investigated mortality in life insurance
    **with *Todesfallcharakter*** over **2006 to 2008**, using **German insurers' own policy data**
    with **German population statistics**, compared against international developments.
  - After cleansing, the insured data covered **60 % of the German market in the
    *Kapitallebensversicherung* segment**; **the term-assurance figure was truncated in the search
    summary and is not established** (gap 12).
  - The *Richtlinie* **regulates the methodology for deriving mortality tables for reserving and the
    procedure for setting the *Sicherheitszuschläge***.
  - ***DAV 2008 T R*** and ***DAV 2008 T NR*** — smoker and non-smoker — are in principle **also
    suitable for premium calculation** differentiated by smoking status, **but not for policies
    written without a *Gesundheitsprüfung***.
  - **First adopted as a DAV-Richtlinie on 4 December 2008**; restated as a *Fachgrundsatz* dated
    **29 November 2022**. **The table values are not public and delib does not redistribute them.**
- **What this establishes for the model**: (i) the German first-order basis for a term product is
  DAV 2008 T with its smoker/non-smoker variants; (ii) the *Sicherheitszuschlag* is **part of the
  table's construction**, so first-order and second-order are two levels of one DAV framework and the
  model must publish both; (iii) the smoker split is **actuarially sanctioned for pricing**, which is
  why the market rates on it; (iv) it is **not** available without medical underwriting, which is why
  simplified-issue German death covers are aggregate-rated. **The magnitude of the loading was not
  established and is `[std]` here** (mechanic 15, gap 6).

### R13 — Unisex pricing: the EU Gender Directive, CJEU C-236/09 (*Test-Achats*), AGG § 20

- Publisher: Court of Justice of the European Union; Bundesministerium der Justiz. URL: **not
  established** for any of them
- Asserted from knowledge, `[unverified]` except the date: the judgment struck down the derogation
  permitting sex-differentiated insurance premiums with effect for contracts concluded **from
  21 December 2012**; German implementation runs through the amendment of **§ 20 AGG**. The frlib
  research reached the same cut-off independently from the French implementing article, which
  preserves the derogation only for contracts concluded "au plus tard le 20 décembre 2012"
  [`frlib` R10] — the closest thing to corroboration this entry has.
- **Effect here, larger than on any other delib product.** Female mortality at the ages a term
  contract is sold — 25 to 55 — is roughly **half** male mortality `[unverified]`, so a unisex tariff
  is a blend whose position depends entirely on the **assumed sex mix of the tariff's own new
  business**, a proprietary and periodically re-estimated number. **The DAV 2008 T variants are
  sex-distinct** [R12], so every German RLV tariff written since 2013 uses a **carrier-chosen mixing
  ratio that no source discloses**. The delib model carries a `[std]` 50/50 blend, and this is one of
  the largest single sources of unexplained spread between German carriers' rates.

### R14 — EStG § 20 Abs. 1 Nr. 6 and § 10 Abs. 1 Nr. 3a — income tax on the benefit, deductibility of the premium

- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R10]
- **Inherited corroboration**: § 20 Abs. 1 Nr. 6 taxes the ***Unterschiedsbetrag*** between the
  benefit and the premiums paid on a life insurance as investment income; the **half-income treatment
  (*Halbeinkünfteverfahren*)** applies where the contract has run at least **twelve years** and the
  benefit is paid after the policyholder's **62nd** birthday; a **BMF-Schreiben of 1 October 2009,
  IV C 1 - S 2252/07/0001** is the administrative guidance; and for contracts concluded from **1 April
  2009** a ***Mindesttodesfallschutz*** of **50 %** of the *Beitragssumme* is required for the
  favourable treatment [inherited: `kapitallebensversicherung.md` R10, R11, R12].
- **Why it matters that this section does *not* apply.** § 20 Abs. 1 Nr. 6 taxes the *Erlebensfall* —
  maturity or surrender — because that is where an *Unterschiedsbetrag* can arise. **A pure death
  benefit paid to a third party is not investment income of the policyholder and is not caught**, so
  the *Todesfallleistung* of an RLV is **free of Einkommensteuer** and the tax question moves entirely
  to the *Erbschaftsteuer* [R15]. The non-application is asserted and `[unverified]` (gap 16), though
  corroborated indirectly by the *Mindesttodesfallschutz* rule itself, which exists precisely to stop
  savings contracts dressing themselves as death covers to reach this section.
- ***Sonderausgaben***: RLV premiums fall among the *sonstige Vorsorgeaufwendungen* deductible under
  § 10 Abs. 1 Nr. 3a EStG, **within an annual ceiling in practice already exhausted by health and
  long-term-care contributions**, so the effective deduction for most taxpayers is **nil**. Both
  statements `[unverified]`; **no ceiling figure is stated in this file** (gap 17).

### R15 — ErbStG §§ 3, 15, 16, 19 — the *Erbschaftsteuer* treatment of the death benefit

- URL: `https://www.gesetze-im-internet.de/erbstg_1974/` `[unverified]`; per-section forms **not
  established**
- Asserted from knowledge, `[unverified]` throughout:
  - **§ 3 Abs. 1 Nr. 4** brings within ***Erwerb von Todes wegen*** every asset acquired by a third
    party on the death of the deceased **by virtue of a contract concluded by the deceased**. A
    *Todesfallleistung* paid to a *Bezugsberechtigter* under a policy the deceased took out **on his
    own life and paid for himself** is the textbook case, and is **subject to *Erbschaftsteuer***.
  - **§ 15** sorts beneficiaries into three *Steuerklassen*: I (spouse, registered partner, children,
    grandchildren, parents on death), II (siblings, nieces and nephews, in-laws, divorced spouse),
    III (**everyone else, including an unmarried partner**).
  - **§ 16** sets the *Freibeträge*: **500,000 EUR** spouse or registered partner, **400,000 EUR** per
    child, **200,000 EUR** per grandchild, **100,000 EUR** parents and grandparents on a death
    acquisition, **20,000 EUR** in classes II and III. **Every figure is `[unverified]`** and is
    carried downstream as a `[std]` illustration (gap 18).
  - **§ 19** sets banded rates by class, beginning at **7 %** in class I and **30 %** in class III.
    `[unverified]`.
- **The arithmetic that drives German term-life contracting.** On the representative sum insured,
  **300 000 €**: paid to a **spouse**, the 500 000 € allowance absorbs it and the tax is nil; paid to
  an **unmarried partner**, the allowance is 20 000 €, the taxable acquisition 280 000 €, class III
  applies from 30 %, and the liability is on the order of **84 000 € — 28 % of the sum insured**. That
  comparison is why the *Über-Kreuz-Versicherung* exists (mechanic 14) and why a German term-life
  specification must document a contracting structure alongside the cash flows. **The arithmetic is
  arithmetic; its inputs are `[unverified]`.**

### R16 — VersStG § 4 — *Versicherungsteuer* exemption for life insurance

- URL: `https://www.gesetze-im-internet.de/verststg_1996/__4.html` `[unverified]`
- Asserted and `[unverified]`: the *Versicherungsteuer* — at a general rate of 19 % for most non-life
  lines — **does not apply to life insurance**. A German RLV premium is quoted and billed **without
  insurance premium tax**, unlike a French *cotisation* quoted "TTC". The delib model carries **no
  premium-tax line**, and the reason is recorded here so a reader does not conclude it was forgotten
  (gap 19).

### R17 — VVG-InfoV, and the PRIIP boundary for a pure protection product

- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`. The sibling research recorded
  § 2 VVG-InfoV as the source of the pre-contractual information duties and of the *Effektivkosten*
  disclosure [inherited: `kapitallebensversicherung.md` R9]
- **The boundary this product sits on, asserted and `[unverified]`.** A ***Basisinformationsblatt***
  (PRIIP-KID) is required for a **packaged retail investment product** — one whose return is exposed
  to the performance of reference values or assets. A **pure *Risikolebensversicherung* has no
  investment component and is therefore not a PRIIP**, so none is produced for it; the applicable
  pre-contractual summary is the ***Produktinformationsblatt*** under the VVG-InfoV [S2].
- **Two consequences for delib.** (i) The brief's expectation of finding *Basisinformationsblätter*
  for this product is misplaced, and the gaps register records that rather than pretending the
  documents were merely unreachable. (ii) There is **no *Effektivkosten* figure for a term product**,
  because a reduction in yield presupposes a yield. **The absence of a published cost ratio is
  structural, not a research failure**, and it is a large part of why German term-life charge levels
  are invisible (gap 8).

### R18 — GDV, *Die deutsche Lebensversicherung in Zahlen* and the *Risikoversicherung* statistics

- URL: **not established** for the term-assurance breakdown. The sibling research located the GDV
  statistics landing page and the ten-year *Neugeschäft und Bestand* series [inherited:
  `kapitallebensversicherung.md` R20, R21]
- **Inherited corroboration**: the GDV publishes an annual statistical volume and a ten-year series
  broken down by product family; from it the sibling research took a whole-market ***Stornoquote* of
  2,72 % for 2024 and 2,56 % for 2023** on the main GDV measure — counting contracts terminated early,
  surrendered or made *beitragsfrei* as a percentage of the *Bestand* — and a second measure of
  **1,2 % for 2024** counting contracts and covering surrenders and other early terminations. **The
  two are not reconcilable from the evidence and both are recorded.**
- **What is *not* established is the whole of what this product needed**: the size of the German
  *Risikoversicherung* segment — contracts in force, new business, premium income, aggregate
  *versicherte Summe*, average sum insured, average premium — and any segment-specific lapse rate
  (gap 13). The whole-market *Stornoquote* is **deliberately not used** as a term-life assumption: a
  term contract's lapse is dominated by its first three durations and by the absence of any surrender
  value to lose, both of which push it above a book average weighted by long-dated savings contracts.

### R19 — BaFin supervisory material on life insurance conduct and product governance

- URL: **not established** for any term-life-specific item. The sibling research located BaFin's
  **Merkblatt 01/2023 (VA)** *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden
  Lebensversicherungsprodukten*, published **May 2023**, and the *Risiken im Fokus 2026* item on the
  cost of *kapitalbildende* products [inherited: `kapitallebensversicherung.md` R17, R18]
- **Inherited corroboration and its limit**: the *Merkblatt*'s subject is expressly
  ***kapitalbildende*** life products, and its concern is that costs be justified by customer value.
  **A pure *Risikolebensversicherung* is outside its stated subject matter.** Recorded so that a
  reader does not import an endowment-conduct standard into a term product; supervisory literature
  specific to German term assurance was **not located** (gap 14).

### R20 — Rating and analysis houses on German term-life tariff design

- Publisher: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA — the same corpus as S17, seen from the
  product side. URL: **not established**
- The reference class for two market-design facts no statute supplies: that the ***Brutto*/*Zahlbeitrag*
  spread is a rated criterion**, and that the ***Nachversicherungsgarantie* event list, caps and age
  limits are rated criteria**. Both `[unverified]` [S17]. **No rating, criterion weight or observed
  distribution is asserted.**

### R21 — HGB § 341f and RechVersV — statutory reserving for a term contract

- URL: `https://www.gesetze-im-internet.de/hgb/__341f.html` `[unverified]`
- Asserted and `[unverified]`: § 341f requires the *Deckungsrückstellung* to be computed prospectively
  on the bases used to determine the premium, with a prudent margin, including a provision for future
  administration costs where the premium-paying period is shorter than the cover period; the RechVersV
  governs presentation. Whether a **negative** individual *Deckungsrückstellung* arising from
  *Zillmerung* must be floored at zero — the *Nullstellung* question — was **not established**, and it
  matters here because a *gezillmert* term contract sits below zero for a long stretch (gap 11).
- The delib posture, stated once in every product: **the models publish gross best-estimate-style
  liability cash flows, undiscounted. Discounting, the *Deckungsrückstellung*, Solvency II technical
  provisions and the SCR are referenced, never specified.** R21 is a pointer, not a model input.

### R22 — Solvency II and the German prudential layer

- Publisher: EIOPA; BaFin. URL: **not established**
- A pointer only, on the same posture as R21. Nothing product-specific for German term assurance was
  located, and **no capital, risk-margin or stress figure appears anywhere in the delib
  `risikolebensversicherung` documents.**

### R23 — German case law on *vorvertragliche Anzeigepflicht* and *Selbsttötung* in life insurance

- Publisher: Bundesgerichtshof and the *Oberlandesgerichte*. URL: **not established.** **No decision
  is cited by date or file number anywhere in this file, and none is invented**
- A known reference class, not a source. German term-life litigation clusters on two questions:
  whether the applicant's answers to the *Gesundheitsfragen* were complete and whether the insurer
  complied with the § 19 Abs. 5 warning requirement [R4]; and whether a *Selbsttötung* inside the
  three-year window was committed in a state excluding free will [R1]. The sibling research located
  BGH authority on adjacent life-insurance questions — the *Stornoabzug* *Bezifferung* requirement and
  the *Bewertungsreserven* judgment of **20 January 2021, IV ZR 318/19** [inherited:
  `kapitallebensversicherung.md` R22, R23] — establishing that the court decides this area regularly
  and nothing about term assurance. **No holding is asserted** (gap 20).

---
## Extracted facts, organised by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. It carries the
weight of the file, because it is the part that does not depend on having a PDF open. Every claim
carries an `[S#]` or `[R#]` tag, an inherited-corroboration note, `[unverified]`, or `[std]`.

### 1. Product structure and legal form

- A German *Risikolebensversicherung* is a **life insurance contract under Chapter 5 of the VVG**
  (*Lebensversicherung*, §§ 150–171), not an accident or health contract, even though it pays only on
  death [R1] [R7] [R8]. Every general life-insurance provision of that chapter — the *Widerrufsfrist*
  of § 152, the *Anzeigepflicht* of § 19, the *Selbsttötung* rule of § 161, the *Bezugsberechtigung*
  of § 159 — applies to it unmodified [R1] [R4] [R7] [R8].
- It is **individual business** (*Einzelversicherung*) in the delib scope: one contract, one
  *Versicherungsnehmer*, one or two *versicherte Personen*. Group and occupational forms are out of
  scope (opening section).
- **Three roles, routinely three different people.** The *Versicherungsnehmer* owns the contract and
  pays; the *versicherte Person* is the life at risk; the *Bezugsberechtigter* receives the benefit.
  On a savings product these collapse into one or two people. On a term product they systematically
  do not, and the tax outcome depends on **which** of them is which [R7] [R15] (mechanic 14).
- Where the *Versicherungsnehmer* insures **another person's** life and the benefit exceeds ordinary
  funeral costs, that person's ***schriftliche Einwilligung*** is required [R7] `[unverified]`. Every
  *verbundene Leben* and every *Über-Kreuz* arrangement is built on that consent.
- The product is ***überschussberechtigt*** — surplus-participating — as a matter of course, and the
  participation is the mechanism through which the customer's bill is set (mechanic 5) [R5] [R9]
  [S5]. A non-participating German term tariff is possible in law (§ 153 permits exclusion by express
  agreement [R5]) and is **not the market form**; no such tariff was located `[unverified]`.
- The contract documents delivered are the ***Allgemeine Versicherungsbedingungen***, the
  ***Verbraucherinformation*** pack and the ***Produktinformationsblatt*** [S2] [R17]. There is
  **no *Basisinformationsblatt***, because a pure protection contract has no investment component and
  is not a PRIIP [R17] `[unverified]`. That is a structural absence, not a missing document.

### 2. The benefit

- **One benefit, one event.** The insurer pays the ***Versicherungssumme*** as a *Todesfallleistung*
  if the *versicherte Person* dies within the *Versicherungsdauer*. If she survives it, **nothing is
  paid and the contract simply ends** [R1] [R2] [S5] [S15]. There is no *Erlebensfallleistung*, no
  maturity value, no return of premium and no conversion right into a savings contract in the base
  design.
- The benefit is a **lump sum**, paid to the *Bezugsberechtigter* directly and not through the estate
  where the nomination is effective [R7]. Payment outside the estate is the practical point of the
  *Bezugsberechtigung*: the beneficiary is paid without waiting for probate, and the sum is beyond
  the reach of the estate's creditors in the ordinary case `[unverified]`.
- Death **from any cause** is covered — accident or illness alike — subject only to the short
  exclusion list of mechanic 13. **There is no *Wartezeit*** on a medically underwritten German RLV:
  cover attaches from the agreed *Versicherungsbeginn* and the insurer's protection against
  anti-selection is the *Gesundheitsprüfung*, not a deferral of cover `[unverified]` (mechanic 9).
  This is a sharp contrast with the German *Sterbegeldversicherung*, which is written without
  underwriting and therefore carries a *Wartezeit* of typically several years — and with the French
  market, where two of the eight carriers in the frlib corpus impose a *délai d'attente* of 3 or 12
  months where medical formalities are waived [`frlib` S6, S9].
- **No living benefits in the base design.** The German market does bolt them on as options
  (mechanic 8) — an *Unfalltod-Zusatzversicherung* doubling the sum on accidental death, a
  *Berufsunfähigkeits-Zusatzversicherung*, and a growing "vorgezogene Todesfallleistung" paying the
  sum early on a diagnosis of terminal illness — but none of them is part of the core cover. There is
  **no German equivalent of the French *PTIA* acceleration**, which in France is present in seven of
  eight standalone contracts and is compulsorily attached to the death cover at one carrier
  [`frlib` S1–S8]. **The absence of a standard acceleration is the second-largest structural
  difference between the German and French term products** and it simplifies the German model
  considerably: one decrement produces one benefit, and there is no interlock to get wrong.

### 3. *Versicherungssumme* shapes

Three shapes are standard, and a German tariff normally offers all three on the same underwriting and
the same *Rechnungsgrundlagen*. All three statements are `[unverified]` as to any carrier and are
asserted from market knowledge; they are structural and are not numeric.

- ***Konstante Versicherungssumme*** — the sum insured is the same throughout the term. The default
  and the majority form. Used for family protection, where the need does not amortise.
- ***Linear fallende Versicherungssumme*** — the sum insured falls by a **fixed amount each year**,
  normally the initial sum divided by the term, so that it reaches zero (or a stated residual) at
  expiry. Cheap, simple, and a poor match to an annuity loan because a repayment loan's balance falls
  slowly at first and quickly at the end, while a linear schedule does the opposite.
- ***Annuitätisch fallende Versicherungssumme*** — the sum insured follows the **outstanding balance
  of an annuity loan** at a stated nominal rate agreed at issue. This is the *Darlehensabsicherung*
  or *Restschuldabsicherung* form of a standalone RLV. The agreed rate is a **contractual schedule
  parameter, not the borrower's actual loan rate**: the schedule is fixed at issue and does not
  follow the loan if the loan is refinanced, repaid early or rolled onto a new fixed rate. The
  standard rates offered cluster in the low single digits; **no specific rate is asserted** (gap 15).
- **The modelling consequence is that all three are one mechanic**: a *Versicherungssumme* schedule
  `S(t) = S(0) × f(t)` with `f(0) = 1`, driven by an external table. `konstant` is `f(t) = 1`;
  `linear fallend` is `f(t) = 1 − t/n`; `annuitätisch fallend` is the outstanding-balance factor of
  an `n`-year annuity at the agreed rate. **A model that hard-codes a constant sum insured cannot
  represent two of the three shapes the German market actually sells**, which is why the delib model
  carries the schedule as a first-class input.
- A fourth, **rising** shape exists and is a different mechanic: the ***Dynamik***, where the sum
  insured **and the premium** rise together each year by an agreed percentage without a new
  *Gesundheitsprüfung*, subject to a right of *Widerspruch* (mechanic 8).
- German carriers price the falling shapes at a materially lower premium than the constant shape for
  the same initial sum, because the expected claim is lower — mechanically, not as a discount. **No
  ratio is asserted**; the model computes it from the schedule.

### 4. The premium: a level *Bruttobeitrag*, and three unrelated meanings of "netto"

- **The German term-life premium is level over the whole *Beitragszahlungsdauer***, struck at issue
  from the entry age and held there. It does **not** step up with attained age. This is the largest
  single structural difference from the French *temporaire décès*, where every one of the eight
  carriers in the frlib corpus whose basis is stated prices on an **annually revisable attained-age**
  basis and none prices level [`frlib` S1, S2, S3, S6, S7, S9, S10; `frlib` gap 1]. The German
  contract is the one the Anglo-American reader expects; the French one is not. The statement that the
  German level form is universal is `[unverified]` at carrier level, but it follows directly from the
  existence of a guaranteed *Bruttobeitrag* [R6] and from the *Zillmerung* regime [R10], neither of
  which makes sense on an annually repriced contract.
- *Beitragszahlungsdauer* normally equals *Versicherungsdauer*. An ***abgekürzte
  Beitragszahlungsdauer*** — premiums stopping before cover does — is offered by some tariffs and
  raises the level premium correspondingly `[unverified]`.
- **Three unrelated things are called "netto" in this market, and confusing them is the classic
  implementation error.** They must be kept apart by name in every delib document:

| Term as used | Means | Where it appears |
|---|---|---|
| *Nettoprämie* / *Nettobeitrag* (**actuarial** sense) | The risk premium computed from the mortality basis and the interest rate, **before** expense loadings. The *Bruttobeitrag* is this quantity plus α, β and γ loadings | Actuarial texts, DAV material, the sibling delib glossary [inherited: `kapitallebensversicherung.md` terminology] |
| *Nettobeitrag* / *Zahlbeitrag* (**consumer** sense) | The premium actually billed = *Bruttobeitrag* **less** the *Beitragsverrechnung* out of *Überschussanteile*. **This is the market's dominant usage for this product** | Insurer product pages, *Produktinformationsblätter*, comparison portals, consumer press [S5] [S14] [S15] [S16] |
| *Nettotarif* / *Honorartarif* (**distribution** sense) | A **commission-free** tariff sold through fee-based advice, where the *Abschlussprovision* is stripped out of the premium and paid separately as a fee | Broker and fee-adviser market `[unverified]` |

  The delib documents use ***Zahlbeitrag*** for the consumer sense throughout and reserve
  ***Nettoprämie*** for the actuarial sense, and say so once in each document. **The word
  "*Nettobeitrag*" alone is never used as a delib parameter name.**

### 5. *Bruttobeitrag* → *Zahlbeitrag*: the *Überschussbeteiligung* as *Beitragsverrechnung*

**This is the central mechanic of the German term product and the one an implementation gets wrong.**

- **The tariff premium is the *Bruttobeitrag*.** It is computed on **first-order
  *Rechnungsgrundlagen*** — a prudent mortality table with *Sicherheitszuschläge* [R12], the
  *Rechnungszins* [R10], and the expense loadings — and it is **the amount the contract guarantees**.
  It is the maximum the policyholder can ever be required to pay, and it does not change over the
  term [R6].
- **The customer is billed the *Zahlbeitrag*.** The insurer declares an *Überschussanteil* and
  applies it as ***Beitragsverrechnung*** — netting it directly against the *Bruttobeitrag* before
  billing, rather than crediting it to an account. Also marketed as *Sofortverrechnung* or
  *Sofortrabatt*. The *Zahlbeitrag* is therefore

  ```
  Zahlbeitrag(t) = Bruttobeitrag × (1 − v(t))
  ```

  where `v(t)` is the declared *Beitragsverrechnungssatz* for the year, `0 ≤ v(t) < 1`. The mechanic
  is corroborated in kind by a carrier's own guide page dedicated to the *Überschussbeteiligung* of
  this product [S5] and follows directly from § 153 VVG's requirement of a
  *verursachungsorientiert* allocation on a product with no reserve to credit [R5]. **The functional
  form and the name are asserted; no value of `v` is asserted anywhere in this file** (gap 1).
- **Only the *Bruttobeitrag* is guaranteed. The *Zahlbeitrag* is not, and the insurer may raise it up
  to the *Bruttobeitrag*.** The *Überschussbeteiligung* is declared **annually** and is not
  guaranteed for the future — the sibling research established that statement in a carrier's own
  words for the endowment [inherited: `kapitallebensversicherung.md` S3], and § 153 VVG confers an
  entitlement to *participate*, not an entitlement to a level [R5]. A reduction of `v` raises the
  billed premium **without any § 163 procedure, without a *Treuhänder* and without a policyholder
  right of objection**, because no guaranteed term of the contract has moved [R6]. **This asymmetry
  is the whole reason the German market publishes both numbers, and it is what makes the spread a
  rated criterion** [S17] [R20].
- **The spread's economics, and why it is wide.** An RLV's technical result is almost entirely
  *Risikoergebnis*, and the MindZV obliges the insurer to allocate at least **90 %** of that result to
  policyholders [R9]. So:
  1. the insurer prices on a prudent first-order mortality basis `q1 = (1 + m) · q2`, with `q2` the
     best estimate for a medically selected portfolio and `m` the aggregate *Sicherheitszuschlag*
     [R12];
  2. the portfolio's actual claims run at roughly `q2`, so the mortality margin earned per annum is
     `m/(1 + m)` of the *Bruttobeitrag*'s risk element;
  3. **at least 90 % of that margin must go back**, and *Beitragsverrechnung* is the way it goes back
     on a product with no account to credit.
  A wide spread is therefore **evidence of a prudent first-order basis, not of a generous insurer**,
  and a narrow spread is evidence of a basis struck close to expected experience. Both readings are
  structurally sound; **neither is a quality judgement**, which is the nuance the consumer press
  tends to lose [S15] [S17].
- **The counter-intuitive consequence, and the most useful single result in this file.** Because
  90 % of the extra margin is returned, **increasing the prudence of the first-order basis moves the
  *Bruttobeitrag* a great deal and the *Zahlbeitrag* hardly at all.** Working the `[std]` calibration
  of mechanic 16 through three levels of `m`, holding everything else fixed, at entry age 35, sum
  insured 300,000 EUR, 25-year term:

| Sicherheitszuschlag `m` | First-order / best-estimate ratio | Bruttobeitrag p.a. | Zahlbeitrag p.a. | Zahl / Brutto |
|---|---|---|---|---|
| 1.00 | 2.00 | 1,180 EUR | 730 EUR | 0.62 |
| 1.25 | 2.25 | 1,316 EUR | 753 EUR | 0.57 |
| 1.50 | 2.50 | 1,451 EUR | 775 EUR | 0.53 |

  The *Bruttobeitrag* moves by **23 %** across that range; the *Zahlbeitrag* moves by **6 %**. All
  six figures are **[std]** constructions from mechanic 16 and are **not market observations**. The
  result they demonstrate is not a construction: it follows from the MindZV 90 % rule [R9] and is the
  reason two German carriers can quote nearly identical *Zahlbeiträge* on very different
  *Bruttobeiträge*.
- **Modelling ruling that follows.** The delib model **derives** the *Zahlbeitrag* from the
  first-order premium and the MindZV allocation rather than treating `v` as a free input. The
  *Beitragsverrechnungssatz* becomes an **output of the surplus mechanic**, which is exactly what it
  is in the real product, and the model then publishes **both premium streams** — a guaranteed
  `prem_gross` and a billed `prem_paid` — with `net_cf` built from the billed one and the guaranteed
  one available as the stress. **A model that carries only one premium stream cannot represent this
  product.**
- **The observed range of `Zahl / Brutto` across the German market could not be established** (gap 1).
  What can be said with confidence about its shape: it is **below 1 for essentially every
  participating tariff**, it is **wider in the direct channel than in the tied-agent channel** because
  less of the *Bruttobeitrag* is committed to acquisition costs [S3] [S12], and a small number of
  tariffs are marketed on a deliberately **narrow** spread as a selling point [S17]. The delib
  representative design uses the derived value of mechanic 16, **0.57**, tagged **[std]**.

### 6. Other *Überschussverwendung* forms

The *Beitragsverrechnung* is the dominant form on this product but not the only one. Four forms are
used in the German market for a death-benefit contract; all four statements are `[unverified]` as to
prevalence and are asserted from market knowledge, with the four-component surplus vocabulary itself
inherited from a carrier's own page about this product [S5].

| Form | Mechanic | Effect on the model |
|---|---|---|
| ***Beitragsverrechnung*** (*Sofortverrechnung*) | Surplus netted against the *Bruttobeitrag*; the customer pays less | Reduces `prem_paid`; sum insured unchanged. **The base design** |
| ***Summenzuwachs*** / *Bonussumme* | Surplus buys additional **paid-up death cover**; the *Versicherungssumme* grows year by year | Raises the benefit; premium unchanged. A second benefit stream the model would have to carry |
| ***Verzinsliche Ansammlung*** | Surplus accumulates with interest in a side account, paid **in addition** on death | Creates an account value on a product that otherwise has none |
| ***Todesfallbonus*** | A declared bonus sum payable in addition to the *Versicherungssumme* on death | Raises the benefit only in the year of claim |
- **Sources of surplus on this product, in order of size**: ***Risikoüberschuss*** first and by a
  wide margin; ***Kostenüberschuss*** second and modest; ***Zinsüberschuss*** third and negligible,
  because the contract's *Deckungskapital* is small and short-lived [R9] [R10]. That ordering is the
  mirror image of the endowment, where the interest result dominates [inherited:
  `kapitallebensversicherung.md` mechanics 3, 6]. The *Bewertungsreserven* share of § 153 Abs. 3 VVG
  and § 139 VAG is, on this product, **economically empty** for the same reason [R5] [R11]
  `[unverified]`.
- **The delib model implements *Beitragsverrechnung* only**, and states in `model.md` that the other
  three are off. `Summenzuwachs` is the one worth implementing next, because it is the only one that
  changes the benefit rather than the premium.

### 7. *Zahlweise* and the *Ratenzahlungszuschlag*

- Premiums are payable **annually, half-yearly, quarterly or monthly**, annually in advance being the
  actuarial base case and monthly by *SEPA-Lastschrift* being the market's normal choice
  `[unverified]`.
- Paying other than annually attracts a ***Ratenzahlungszuschlag***. The German market convention is
  a loading on the annual premium of **2 % half-yearly, 3 % quarterly, 5 % monthly** — a figure the
  sibling research recorded as a market convention with no carrier attribution [inherited:
  `kapitallebensversicherung.md` R28]. It is carried here as **[std]** with that provenance, not as a
  citation (gap 21).
- The loading applies to the ***Zahlbeitrag*** as billed. Whether German carriers strike it on the
  *Bruttobeitrag* or the *Zahlbeitrag* — a difference of a few euros a year but a real one for a
  model that must reproduce a *Produktinformationsblatt* figure — was **not established**
  `[unverified]`. The delib model applies it to the *Zahlbeitrag* and says so.
- The ***Versicherungsperiode*** follows the *Zahlweise*, and with it the policyholder's termination
  right under § 168 VVG [R8]: a monthly-paying contract can be terminated monthly. **This is the
  reason German term-life lapse is not concentrated at policy anniversaries** the way an annual-mode
  book's is, and it is a caution for any model that assumes anniversary-only exits.
- **No *Versicherungsteuer* is charged**: life insurance is exempt [R16] `[unverified]`. There is no
  premium-tax line anywhere in the delib model for this product.

### 8. Options and guarantees

- ***Nachversicherungsgarantie*** — **the most important option on the product.** The policyholder may
  raise the *Versicherungssumme* **without a new *Gesundheitsprüfung*** on the occurrence of a named
  life event. The events that recur across the German market, asserted from market knowledge and
  `[unverified]` in every particular (gap 7):
  - marriage or entry into a *eingetragene Lebenspartnerschaft*;
  - birth or adoption of a child;
  - purchase of a property, or drawing a loan secured on one;
  - completion of vocational training or of a degree, and the start of employment;
  - a substantial rise in income;
  - taking up self-employment;
  - divorce, or the ending of a partnership;
  - the loss or reduction of other death cover, including an employer-provided one.
  The standard restrictions, likewise `[unverified]`: a **window** after the event within which the
  right must be exercised; a **cap per event** and a **cumulative cap**, expressed as a percentage of
  the original sum insured and/or as an absolute amount; a **maximum age** beyond which the right
  lapses; and an **exclusion where the *versicherte Person* is already unable to work or is in
  treatment**. Some tariffs additionally grant an ***ereignisunabhängige Nachversicherung*** in the
  first years of the contract, exercisable without any event at all `[unverified]`.
  - **No event list, no cap and no age limit is asserted from any document** (gap 7). The option is
    carried in the delib specification as a described option with `[std]` parameters, and is **off in
    the base run**.
  - **Why it matters actuarially**: an increase without underwriting is an increase in expected
    claims that the tariff for the increment does not reflect, and the anti-selection is bounded only
    by the event trigger and the caps. It is also the point at which the § 161 three-year
    *Selbsttötung* clock is understood to restart for the increment [R1] `[unverified]` (gap 9).
- ***Dynamik*** (*Beitragsdynamik* / *Summendynamik*) — an agreed annual escalation of the premium,
  with the sum insured rising by the actuarially corresponding amount, without a new
  *Gesundheitsprüfung*. The policyholder may object (*Widerspruch*) to any individual increase, and
  the right typically lapses after a stated number of consecutive objections `[unverified]`. **Off in
  the base run.**
- ***Verlängerungsoption* / *Verlängerungsgarantie*** — the right to extend the *Versicherungsdauer*
  at expiry without renewed underwriting, at the tariff then in force for the attained age. Offered by
  some carriers `[unverified]`. **Not modelled.**
- ***Umtauschoption*** — the right to convert into a *kapitalbildende Lebensversicherung* without a
  new *Gesundheitsprüfung*. Historically common in the German market, now rare `[unverified]`. **Not
  modelled.**
- ***Vorgezogene Todesfallleistung*** — early payment of the sum insured on medical evidence of a
  terminal illness with a limited life expectancy. A growing option in the German market and **not a
  *PTIA*-style disability acceleration**: the trigger is prognosis, not incapacity `[unverified]`.
  **Not modelled.**
- ***Unfalltod-Zusatzversicherung*** (UZV) — an additional sum, commonly equal to the base sum,
  payable where death results from an accident within a stated period of it `[unverified]`. The
  German analogue of the French *doublement accidentel*, which is present at five of the eight
  carriers in the frlib corpus [`frlib` S1, S2, S6, S7, S9]. **Not modelled**, and recorded so that a
  reader knows the omission is deliberate.
- ***Berufsunfähigkeits-Zusatzversicherung*** (BUZ) and ***Beitragsbefreiung bei
  Berufsunfähigkeit*** — a disability rider and a waiver of premium. Common attachments; the
  standalone form is delib product 9. **Not modelled here.**
- ***Vorläufiger Versicherungsschutz*** — provisional cover between application and acceptance,
  capped in amount and in duration and sometimes limited to accidental causes `[unverified]`. The
  German analogue of the French *garantie provisoire* [`frlib` S2, S3]. **Not modelled**: it is a
  sub-annual window on an annual-step model.

### 9. Underwriting

- **The whole of German term-life risk selection is the *Gesundheitsprüfung***, and its legal frame
  is § 19 VVG: the applicant must disclose the *gefahrerhebliche Umstände* known to her **that the
  insurer has asked about in *Textform***, and **nothing else** — the duty is question-bounded
  [inherited: `kapitallebensversicherung.md` R5] [R4].
- ***Gesundheitsfragen*** are asked in the application and typically cover: outpatient treatment and
  consultations over a recent look-back period; inpatient treatment, operations and psychotherapy
  over a longer one; current complaints, medication and pending investigations; height and weight;
  and nicotine consumption. **The look-back periods are `[unverified]`** and no figure is asserted
  (gap 22). The insurer may follow up with an ***ärztliche Untersuchung***, a *Hausarztbericht*, blood
  tests, an ECG or a *Belastungs-EKG*, escalating with the sum insured and the entry age
  `[unverified]`.
- ***Vereinfachte Gesundheitsprüfung*** — a shortened question set — is offered below a stated sum
  insured, and full medical examination is required above a higher one. **No threshold is asserted**
  (gap 22). The corresponding French thresholds *are* published by two carriers and are recorded in
  the frlib file — no medical formality below 40,000 EUR and age 50, and simplified underwriting to
  age 40 for up to 250,000 EUR [`frlib` S6, S3] — which shows the disclosure is possible and that the
  German market simply does not make it.
- ***Finanzielle Angemessenheit***. Above a threshold the insurer also underwrites the **financial
  justification** for the sum insured — income, existing cover, the loan being protected — to bound
  over-insurance and the moral hazard on a contract whose whole benefit is payable on death
  `[unverified]`.
- ***Raucher* / *Nichtraucher*** — **the largest single rating split after age**. The market
  definition of a *Nichtraucher* is no consumption of nicotine-containing products for a stated
  qualifying period before application, with a duty to notify a resumption; carriers commonly allow a
  *Nichtraucher* reclassification after the qualifying period has been served on an in-force
  contract. **The qualifying period is `[unverified]`** and is commonly one or two years (gap 22).
  The split is **actuarially sanctioned**: the DAV publishes *DAV 2008 T R* and *DAV 2008 T NR* and
  states they are suitable for premium calculation differentiated by smoking status, **but not for
  policies written without a *Gesundheitsprüfung*** [inherited: `kapitallebensversicherung.md` R14]
  [R12].
  - **Price ratio.** The German market's rule of thumb is that a smoker pays **roughly twice** a
    non-smoker's premium at the ages this product is sold, and more at older ages. **No published
    ratio was obtained** (gap 1). The delib specification carries a **[std]** smoker/non-smoker
    **mortality** ratio of **2.20** at ages 30–55, which reproduces a **premium** ratio of about
    **2.0** once the sum-related and per-policy expense loadings are added back — the arithmetic is
    in mechanic 16, and the rationale is that the smoker/non-smoker gap in insured-lives mortality at
    working ages is consistently reported in the two-to-three range across markets `[unverified]`.
- ***Berufsgruppen***. Occupation is a rating factor, but **far less powerful here than on a
  *Berufsunfähigkeitsversicherung***, where it is decisive. Most German RLV tariffs use a small
  number of classes, or apply no differentiation at all below a listed set of hazardous occupations
  — roofers, scaffolders, professional divers, explosives handlers, aircrew, deployed soldiers —
  which attract a *Risikozuschlag* or a decline `[unverified]`. **No class list, no class count and
  no loading is asserted** (gap 22).
- ***Risikozuschläge***. Where the health evidence discloses an impairment, the German outcome is
  normally a **premium loading expressed as a percentage of the risk premium** — not a benefit
  exclusion. Life *Leistungsausschlüsse* are used sparingly, unlike in disability business. Hazardous
  **hobbies** — parachuting, technical diving, motorsport, mountaineering, combat sports — and
  extended stays in high-risk regions are handled the same way, by a *Risikozuschlag* or, less often,
  by an individually agreed exclusion `[unverified]`. **No German carrier publishes a *Risikozuschlag*
  scale**, and neither does any French one [`frlib` mechanic 10]. The delib model carries a
  `rating_factor` applied to the mortality basis, **[std]** at 1.00 for the base run.
- ***Vorvertragliche Anzeigepflicht* remedies**, all inherited [`kapitallebensversicherung.md` R5]
  [R4]: the insurer may **adjust the contract retrospectively** — writing in the *Risikozuschlag* or
  the exclusion that would have applied — instead of refusing to perform, and for negligent breach
  this is the usual outcome; the adjust, terminate and rescind rights **lapse after five years**, or
  **ten** for intentional or *arglistig* breach. **On a term contract these limits are the whole of
  the claims-risk story**: a claim in the first five years is exposed to the full remedy set, and one
  after ten years is essentially not.
- **Underwriting outcomes** are the same four as everywhere: accept at standard rates; accept with a
  *Risikozuschlag* and/or an individually agreed exclusion, subject to the applicant's acceptance;
  defer; decline `[unverified]` [R4].

### 10. Charges, and the *Zillmerung* of a contract with almost no reserve

- **German carriers do not disclose their charge structure for this product.** There is no
  *Effektivkostenquote* for a term contract, because a reduction in yield presupposes a yield [R17];
  there is no *Basisinformationsblatt* with a cost table, because the product is not a PRIIP [R17];
  and the *Produktinformationsblatt* quotes premiums, not loadings [S2]. **The absence is structural**
  and is the reason every charge parameter in the delib specification is `[std]` (gap 8).
- The charge structure the *Bruttobeitrag* is built from is nevertheless the standard German
  three-part one, and its shape is not in doubt:
  - ***Abschluss- und Vertriebskosten*** (α) — acquisition and distribution, expressed as a per-mille
    of the ***Beitragssumme*** (the sum of all premiums payable over the term). The
    ***Höchstzillmersatz*** caps the amount that may be financed through the reserve at **25 ‰ of the
    *Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015 [inherited:
    `kapitallebensversicherung.md` R7] [R10].
  - ***Verwaltungskosten*** (β and γ) — administration, normally split between a percentage of each
    premium and a per-policy or per-mille-of-sum annual amount `[unverified]`.
  - **No level for any of them is public.** The delib model ships **[std]** values with the
    calibration of mechanic 16 and an explicit statement that they are placeholders.
- ***Zillmerung* on a term product is a peculiar thing and worth stating plainly.** The
  *Höchstzillmersatz* is a fraction of the ***Beitragssumme***, which for a 25-year term contract is
  25 times the annual premium — a large number. The contract's own *Deckungskapital*, by contrast,
  is tiny: it exists only because the level premium exceeds the rising natural risk premium in the
  early years (mechanic 11). **So the Zillmer charge is large relative to the reserve it is written
  into, and the *gezillmerte Deckungsrückstellung* of a term contract is negative for a long stretch
  of its term and never becomes large.** Whether a negative individual reserve must be floored at
  zero for balance-sheet purposes — the *Nullstellung* question — was **not established** [R21]
  (gap 11).
- **The one charge consequence that reaches the cash flows**: acquisition cost is incurred at issue
  and recovered over the term, so a lapse in the first years is a loss to the insurer. That is the
  economic reason lapse matters on a product with no surrender value, and it is why the delib model
  carries acquisition cost as a **year-0 outgo** rather than as an annualised loading (mechanic 17).

### 11. No *Rückkaufswert* — why, and what actually happens on *Kündigung*

- **What every consumer source says.** Terminating a German *Risikolebensversicherung* returns
  nothing: the cover ends and the premiums paid stay with the insurer [S5] [S15]. The French market
  says the same thing about its own product, in its own words — "les cotisations versées restent
  acquises à l'assureur", "le contrat ne comprend pas de faculté de rachat" [`frlib` S5, S9].
- **Why, precisely.** Two reasons, and only the second is legal:
  1. **There is almost nothing to pay out.** A *Risikolebensversicherung* has **no *Sparanteil*** in
     the sense a *Kapitallebensversicherung* has: no part of the premium is set aside to build a sum
     that will certainly be paid. But it is **not** true that nothing accumulates. A level premium
     charged against a **rising** mortality rate necessarily overcharges in the early years and
     undercharges in the late ones, and the difference is held as a *Deckungskapital* that builds,
     peaks near the middle of the term and **runs off to exactly zero at expiry**. On the `[std]`
     calibration of mechanic 16 that reserve peaks at a low single-digit percentage of the sum
     insured. After *Zillmerung* (mechanic 10) it is **negative or nil through much of the term**.
     **Stating "there is no *Sparanteil*, therefore no reserve" is wrong, and a model built on it
     will fail its own closure check.** The correct statement is that the reserve exists, is small,
     is fully consumed by expiry, and is often negative on a *gezillmert* basis.
  2. **The statute does not require it to be paid out.** § 169 Abs. 1 VVG confines the
     surrender-value duty to a life insurance whose insured event is **certain to occur**; a term
     assurance's is not [R2]. **This scope limitation is `[unverified]` at the level of the statutory
     wording and is the most consequential such tag in this file** (gap 2). Its practical result is
     not in doubt.
- **What happens on *Kündigung*.** The policyholder may terminate at the end of the current
  *Versicherungsperiode* under § 168 VVG [R8]; cover ends on that date; **nothing is paid**; and at
  most an unearned fraction of a premium paid in advance is returned. On the model this is a **pure
  decrement with no benefit attached**, and `claims_surr` is **structurally zero** — a fact worth
  asserting in a test rather than leaving to prose.
- **The *Beitragsfreistellung* question, answered.** § 165 VVG gives the right in form [R3]. On this
  product it is empty in substance: the *beitragsfreie Versicherungssumme* the tiny (or negative)
  reserve would buy fails the minimum-benefit test in most durations, and the statutory fallback is
  payment of the *Rückkaufswert*, which is nil [R3] [R2]. **The same collapse happens on the
  non-payment path**: § 166 VVG converts a lapsed life contract into a *prämienfreie Versicherung*
  rather than ending it, **unless** the paid-up benefit falls below the minimum — which here it does,
  so the contract simply ends [R8] `[unverified]`. German carriers answer the customer's real
  question with something other than *Beitragsfreistellung*: a *Beitragsstundung*, a temporary
  *Ruhen*, or a reduction of the *Versicherungssumme* `[unverified]` (gap 10).
- **Consequence for the § 161 *Selbsttötung* rule.** The statutory substitution — *leistungsfrei*,
  but pay the *Rückkaufswert* [R1] — substitutes **nil**. So the German three-year rule, which on an
  endowment is a softening, is on a term contract **an exclusion in all but name** (mechanic 12).

### 12. *Selbsttötung* — § 161 VVG, and how it differs from the French rule

- **The German rule** [R1], inherited corroboration: the insurer is ***leistungsfrei*** where the
  *versicherte Person* **intentionally takes her own life before three years have elapsed since
  conclusion of the contract**; **unless** the act was committed **in a state excluding free
  determination of the will caused by a *krankhafte Störung der Geistestätigkeit***; the three-year
  period **may be extended by agreement**; and where the insurer is *leistungsfrei* it must
  nevertheless **pay the *Rückkaufswert*, including *Überschussanteile*, under § 169**.
- **The French rule**, for contrast, from the frlib research where the article was retrieved in full
  [`frlib` R1]: art. L. 132-7 of the Code des assurances makes the death cover "**de nul effet**" if
  the insured takes his own life **in the first year of the contract**, and **requires** cover from
  the second year; on an increase, the clock restarts **for the additional cover only**; there is no
  surrender value to fall back on, because art. L. 132-23 forbids one on a temporaire décès
  [`frlib` R3].
- **The four differences that matter, side by side:**

| | Germany [R1] | France [`frlib` R1, R3] |
|---|---|---|
| Window | **Three years** from conclusion | **One year** from conclusion |
| Legal effect inside the window | Insurer *leistungsfrei*; **pays the *Rückkaufswert* instead** | Cover "de nul effet" — **nothing is paid** |
| What that substitution is worth on a term product | **Nil or nominal** — there is no surrender value (mechanic 11) | Nil by construction — the product may not have one |
| Extension by agreement | **Expressly permitted** by the statute | Not provided for; the statutory minimum is the rule |

  So the two systems reach **nearly the same economic answer by opposite routes**, and the German
  answer applies for **three times as long**. A modeller porting a French term-life model to Germany
  who changes only the window length has got the mechanic right by accident; one who ports the German
  model to France and keeps the *Rückkaufswert* substitution has introduced a benefit that French law
  forbids.
- **The mental-illness exception is not a formality.** It is the ground on which German
  *Selbsttötung* claims are actually litigated [R23], and it means the rule is not a clean
  contractual switch: a claim inside the window is paid if the claimant establishes the excluded
  state. **A best-estimate cash-flow model cannot represent that**, and delib does not try: the model
  applies the rule as a benefit switch over the first three policy years and records the exception as
  a known simplification.
- **On an increase.** German AVB practice is understood to restart the three-year clock **for the
  increment only**, as the French statute expressly does [`frlib` R1]. **This is `[unverified]` for
  Germany** (gap 9) and matters because the *Nachversicherungsgarantie* (mechanic 8) makes increments
  a routine event on this product.

### 13. Exclusions — the *Kriegsklausel*, and how short the German list is

- **The German exclusion list is remarkably short.** Beyond the statutory *Selbsttötung* window
  [R1] and the statutory forfeitures of § 162 VVG [R7], a German RLV wording carries essentially one
  substantive exclusion — the ***Kriegsklausel*** — plus a nuclear/ABC clause. **There is no list of
  hazardous sports, no aviation exclusion, no alcohol or narcotics exclusion, no occupational
  exclusion and no pre-existing-condition exclusion in the ordinary German wording.** Hazardous
  activities are handled at **underwriting**, by a *Risikozuschlag* or an individually agreed
  exclusion, not by a standing clause (mechanic 9) `[unverified]`.
- **The contrast with France is stark and is worth carrying into the specification.** The French
  *notices* retrieved for frlib carry exclusion lists running to a dozen or more heads — war,
  nuclear, riots and terrorism with active participation, intentional acts, alcohol above the Code de
  la route threshold, driving without a licence, non-prescribed narcotics, air sports, motor
  competition, solo ocean racing, diving below 20 metres, mountaineering above 3,000 metres,
  professional sport, federated competition, pre-existing conditions, and occupational death for
  firefighters, military and police [`frlib` mechanic 9]. **A German wording covers all of that by
  pricing it.** The modelling consequence is that the German product's claim rate is a mortality
  question and the French product's is partly a coverage question.
- **The *Kriegsklausel*, as the German market writes it** `[unverified]` in every particular:
  - Where death is **causally connected with war or war-like events** the insurer's benefit is
    **restricted rather than excluded**: the wording pays the *Deckungskapital* or the value computed
    for the date of death instead of the *Versicherungssumme*. On a term contract that is, again,
    **nil or nominal** (mechanic 11).
  - The restriction standardly bites only where the *versicherte Person* took an ***aktive
    Beteiligung*** in the events. **Passive war risk — a civilian killed in a conflict he took no part
    in — remains covered**, which is the opposite of the drafting instinct an English-language reader
    brings to a war exclusion.
  - A parallel restriction applies to death connected with ***innere Unruhen*** where the person
    actively participated, and to death from the use of ***ABC-Waffen*** (atomic, biological,
    chemical) and from nuclear energy released deliberately.
  - Some wordings carve **out** of the restriction a person present abroad who is **overtaken** by
    war and who does not participate, sometimes with a notification requirement.
- **§ 162 VVG's statutory forfeitures** sit alongside: the insurer is *leistungsfrei* where the
  **policyholder** intentionally and unlawfully brings about the death of the *versicherte Person*,
  and a **beneficiary** who does so loses his entitlement [R7] `[unverified]`.
- **Delib's treatment.** The base model applies **no exclusion decrement at all** beyond the § 161
  window (mechanic 12). The *Kriegsklausel* is recorded in the specification, is not modelled, and
  the reason is stated: it is a catastrophe-scenario clause, not a best-estimate one.

### 14. *Verbundene Leben* and the *Über-Kreuz-Versicherung*

Two different things that are routinely confused. The first is a **product form**; the second is a
**contracting structure** with identical cover and a different tax outcome.

- ***Risikolebensversicherung auf verbundene Leben*** — **one contract, two *versicherte Personen***.
  The *Versicherungssumme* is paid **once, on the first death**, and the contract then **ends**. The
  survivor is left with no cover. All of this is `[unverified]` as to any carrier and is asserted
  from market knowledge.
  - **Both lives are underwritten**, and both must give the § 150 written consent [R7].
  - **The premium is materially below the cost of two single contracts of the same sum**, because
    only one benefit is ever paid — but it is **above** the premium for one single contract, because
    the first-death rate exceeds either single rate. **No ratio is asserted** (gap 15); the model
    computes it, and the identity `q_first = q_A + q_B − q_A·q_B` under an independence assumption is
    what it computes it from — the independence assumption itself being a **[std]** modelling choice
    that understates the true first-death rate for a couple sharing a household, a vehicle and a
    lifestyle.
  - **The separation problem.** On divorce or separation the contract covers two people who no
    longer want a joint benefit, and it cannot simply be halved. Some carriers offer a **conversion
    right into two single contracts without a new *Gesundheitsprüfung***; where they do not, the
    couple's only exit is termination with nothing back (mechanic 11) `[unverified]`. This is the
    standard consumer-press criticism of the form.
  - **Modelling.** Two lives, one benefit, one termination. The delib model carries it as a
    `lives = 2` variant on the same chassis with a first-death decrement, and it is **off in the base
    run**.
- ***Über-Kreuz-Versicherung*** — **two contracts, crossed.** Partner A is the *Versicherungsnehmer*
  and the *Bezugsberechtigter* of a contract on **B's** life; partner B is the *Versicherungsnehmer*
  and *Bezugsberechtigter* of a contract on **A's** life. Each pays the premium on **his own**
  contract out of **his own** funds.
  - **The cover is identical to two ordinary single contracts.** Nothing about the benefit, the
    premium, the underwriting or the cash flows changes. **The model is indifferent to the
    structure**, and that is worth saying explicitly so a reader does not go looking for a mechanic
    that is not there.
  - **The tax outcome is not identical, and that is the whole point.** Under the ordinary structure —
    A insures his own life, names B — the benefit paid to B on A's death is an ***Erwerb von Todes
    wegen*** under § 3 Abs. 1 Nr. 4 ErbStG and is charged to *Erbschaftsteuer* against B's
    *Freibetrag* [R15] `[unverified]`. Under the *Über-Kreuz* structure, **A receives a payment under
    a contract A himself owns and paid for**; nothing passes from B's estate; and there is **no
    *Erwerb von Todes wegen*** [R15] `[unverified]`.
  - **Two conditions the structure must actually satisfy**, both `[unverified]`: the premiums must be
    paid **from the surviving partner's own funds**, verifiably — a joint account from which only one
    partner's income flows, or payment by the insured partner, exposes the arrangement to being
    recharacterised as a gift; and the **§ 150 written consent** of the insured partner is required
    [R7].
  - **Who needs it.** The arithmetic of mechanic R15: a 300,000 EUR benefit to a **spouse** is
    absorbed by the 500,000 EUR *Freibetrag* and bears no tax; the same benefit to an **unmarried
    partner** falls in *Steuerklasse* III with a 20,000 EUR *Freibetrag* and a rate from 30 %, giving
    a liability on the order of **84,000 EUR — 28 % of the sum insured** `[unverified]` [R15]. **So
    the *Über-Kreuz* structure is close to compulsory for unmarried couples and close to pointless
    for married ones with a sum insured below the spousal allowance.** That single sentence is why the
    German market talks about the structure at all, and it is the reason the delib product
    specification documents a contracting structure alongside the cash flows.

### 15. *Rechnungsgrundlagen*: DAV 2008 T, the *Sicherheitszuschläge*, and unisex

- **The mortality basis for a German term product is *DAV 2008 T*** and its variants
  ***DAV 2008 T NR*** (non-smoker) and ***DAV 2008 T R*** (smoker) [R12], inherited corroboration.
  Established about it: derived by the DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* over
  **2006 to 2008** from German insurers' own policy data together with German population statistics;
  the *Richtlinie* **regulates both the derivation methodology and the procedure for setting the
  *Sicherheitszuschläge***; the smoker and non-smoker variants are **suitable for premium
  calculation** but **not for policies written without a *Gesundheitsprüfung***; first adopted
  **4 December 2008** and restated as a *Fachgrundsatz* dated **29 November 2022** [inherited:
  `kapitallebensversicherung.md` R14].
- ***The table values are not public and delib does not redistribute them.*** The DAV tables are the
  property of the Deutsche Aktuarvereinigung. The delib model ships a **[std] proxy** and states what
  a replacement must preserve: an age-graded death rate for medically selected lives, separable into
  smoker and non-smoker variants, and separable into a first-order and a second-order level.
- **The *Sicherheitszuschlag* is part of the table's construction, not a bolt-on.** The DAV
  *Richtlinie* sets the **procedure** for determining it [R12]; the resulting first-order table is
  what a tariff is priced and reserved on, and the second-order table is the best estimate. **The
  magnitude of the loading was not established** (gap 6), and it is the parameter that determines
  the *Brutto*/*Zahlbeitrag* spread almost by itself (mechanic 5). The loading exists to cover
  three named risks — ***Zufallsrisiko*** (random fluctuation), ***Änderungsrisiko*** (change in the
  underlying level) and ***Irrtumsrisiko*** (error in estimating it) `[unverified]`.
- **Three reasons the effective first-order margin on a term contract written today is large**, all
  structural and none of them a criticism of the insurer:
  1. the table was derived on **2006–2008** experience, and German mortality has improved since —
     an 18-year drift on a table used for pricing today;
  2. it is applied to a **medically selected** portfolio in its early durations, where selection
     effects are strongest and the table's own selection allowance is generic;
  3. the *Sicherheitszuschläge* are added on top of both.
  Together these make a first-order to second-order ratio in the **region of two** entirely
  plausible, which is exactly what the *Brutto*/*Zahlbeitrag* spread implies (mechanic 5). **The
  ratio is `[std]`; the reasoning is not numeric.**
- ***Unisex*.** New business written from **21 December 2012** may not use sex as a rating factor
  [R13]. But **DAV 2008 T is sex-distinct**, so every German unisex term tariff is a **blend of the
  male and female tables at a mixing ratio the carrier chooses from its own expected new-business
  mix** — a proprietary, unpublished, periodically re-estimated number [R13] `[unverified]`. Female
  mortality at the ages this product is sold is roughly half male `[unverified]`, so the mixing ratio
  moves the tariff a great deal. **This is one of the largest single sources of unexplained rate
  spread between German carriers**, and it has no French analogue in the frlib corpus beyond the
  Institut des actuaires' 60 % / 40 % working-group mix [`frlib` R13]. The delib model uses a
  **[std]** 50/50 blend, stated as such.
- ***Rechnungszins*.** Priced and reserved at at most the ***Höchstrechnungszins***, **1,00 % for
  new business from 1 January 2025**, raised from 0,25 % and the first increase since 1994
  [inherited: `kapitallebensversicherung.md` R7] [R10]. **On this product it barely matters**: the
  *Deckungskapital* is small and short-lived, so the discounting effect on the level premium is
  second-order. That is a genuine difference from every other delib product and is stated in the
  specification so that a reader does not expect a *Zinszusatzreserve* discussion that does not
  apply.
- ***Lapse is not a pricing basis element.*** German first-order bases are mortality, interest and
  expenses. A *Stornowahrscheinlichkeit* is a second-order, best-estimate quantity used for
  projection and profit-testing, not for the tariff `[unverified]`.
- ***No German insurer publishes its own basis.*** Not the table, not the *Sicherheitszuschlag*, not
  the A/E factor, not the expense loading, not the assumed unisex mix, not the lapse assumption. The
  AVB say the calculation follows "die anerkannten Regeln der Versicherungsmathematik" and stop
  there `[unverified]`. **This is the same position the frlib research reached for France**, where no
  carrier published a table, an A/E factor, an expense loading or a lapse assumption either
  [`frlib` gap 12] — with the one difference that a French carrier did publish a **complete
  attained-age gross rate card** [`frlib` S3], and **no German carrier publishes anything comparable**
  (gap 1).

### 16. Price points — what could not be established, and the `[std]` scale built instead

- **The brief asked for annual *Zahlbeiträge* for 100,000 EUR and 300,000 EUR at ages 30 and 40 for a
  non-smoker, from comparison sites, on the ground that these are the only public German price data
  for this product. That ground is correct and the data could not be obtained.** No German carrier
  publishes a rate card [S3]–[S13]; the *Produktinformationsblatt* quotes the individual applicant's
  own premium [S2]; and a comparison-portal result is generated per query rather than published as a
  document [S14], so it is unreachable without live egress in any event. **Not one price point
  appears in this file** (gap 1).
- **What is shipped instead is an explicit `[std]` construction**, given in full so that a reviewer
  can replace any part of it with a real observation and re-derive the rest. **Every number in this
  sub-section is `[std]`. None is a market observation, and none may be cited downstream as one.**
- **Basis of the construction:**

| Element | `[std]` value | Rationale |
|---|---|---|
| Best-estimate mortality `q2(x)` | `0.00030 x 1.095^(x-30)` per annum, unisex, non-smoker, medically selected | Gompertz proxy. Anchored to give roughly 0.70 of an approximate German unisex population rate at ages 30–60, the order of magnitude of a medically selected insured-lives table `[unverified]` |
| Smoker multiplier | 2.20 on `q2` | Mid-point of the two-to-three range consistently reported for insured-lives smoker/non-smoker mortality at working ages `[unverified]` |
| Sicherheitszuschlag `m` | 1.25, so first-order `q1 = 2.25 x q2` | Calibrated so the derived Zahl/Brutto ratio lands near the market's rule of thumb of "about half". Sensitivity is tabulated in mechanic 5 |
| Rechnungszins | 0.00 % in this illustration | Set to zero deliberately so the arithmetic is reproducible with a calculator. The real 1.00 % [R10] changes the premium by well under 5 % on these terms |
| Acquisition cost | 25 permille of the Beitragssumme, incurred at issue | The Höchstzillmersatz ceiling [R10]; the assumption is that a term tariff runs at the cap |
| Collection / premium-related admin | 5.0 % of each Bruttobeitrag | Placeholder; no German figure is public [R17] |
| Per-policy annual admin | 0.30 permille of the Versicherungssumme | Placeholder; expresses the fixed cost as a sum-related amount so it scales sensibly across the table |
| Surplus return | 90 % of the mortality margin, per the MindZV minimum | [R9], inherited corroboration. Modelling the statutory **minimum** is the conservative choice for the Zahlbeitrag |
| Lapse | none in this illustration | Deliberate: including it would change the level and obscure the mechanic being demonstrated |

- **Resulting `[std]` premium scale**, level annual premiums, unisex non-smoker, *Versicherungsdauer*
  as stated, deaths assumed at the end of the year, no lapse:

| Entry age | Term | Versicherungssumme | Bruttobeitrag p.a. | Zahlbeitrag p.a. | Zahl / Brutto | Brutto as permille of sum |
|---|---|---|---|---|---|---|
| 30 | 30 | 100,000 EUR | 386 EUR | 222 EUR | 0.58 | 3.86 |
| 30 | 30 | 300,000 EUR | 1,157 EUR | 667 EUR | 0.58 | 3.86 |
| 35 | 25 | 100,000 EUR | 439 EUR | 251 EUR | 0.57 | 4.39 |
| 35 | 25 | 300,000 EUR | 1,316 EUR | 753 EUR | 0.57 | 4.38 |
| 40 | 25 | 100,000 EUR | 664 EUR | 373 EUR | 0.56 | 6.64 |
| 40 | 25 | 300,000 EUR | 1,993 EUR | 1,117 EUR | 0.56 | 6.64 |

- **Smoker comparison at the anchor cell** (entry age 35, 300,000 EUR, 25 years): *Bruttobeitrag*
  2,777 EUR and *Zahlbeitrag* 1,539 EUR, giving a **smoker/non-smoker *Zahlbeitrag* ratio of 2.04**
  against a mortality ratio of 2.20 — the gap being the sum-related and per-policy expense elements,
  which do not scale with mortality. **All `[std]`.**
- **How to read these numbers honestly.** They are internally consistent and they reproduce three
  qualitative features the German market is known to have — a *Zahlbeitrag* near half the
  *Bruttobeitrag*, a smoker premium near double the non-smoker one, and a premium per unit sum rising
  steeply with entry age. They are **not** evidence about any carrier. Against a live German
  comparison the constructed level would very likely sit **above the cheapest direct-written
  tariffs**, because the construction runs acquisition cost at the statutory ceiling and takes no
  credit for an expense surplus. **The delib specification uses them as the reference
  implementation's parameters, tagged `[std]`, and says in terms that they are a construction.**
- **What a single real observation would buy.** One published *Bruttobeitrag* / *Zahlbeitrag* pair at
  a known age, sum and term would pin `m` directly through the identity of mechanic 5, and everything
  else in the table would follow. **That is the highest-value missing datum in this file** (gap 1).

### 17. Decrements and policyholder behaviour

- **Two decrements only: death and lapse.** No disability acceleration, no surrender benefit, no
  paid-up state, no partial withdrawal. This is the simplest decrement structure of the ten delib
  products.
- **Lapse.** No *Risikoversicherung*-specific lapse rate was established (gap 13). The whole-market
  German *Stornoquote* inherited from the sibling research — **2,72 % for 2024, 2,56 % for 2023** on
  the main GDV measure, and **1,2 % for 2024** on a second, irreconcilable measure [inherited:
  `kapitallebensversicherung.md` R20] [R18] — is a **book average dominated by long-dated savings
  contracts** and is **not used** as a term-life assumption. The delib lapse assumption is `[std]`
  and is argued from three structural features of this product rather than from a statistic:
  1. **there is nothing to lose by lapsing** — no surrender value, no accumulated bonus — so the
     financial friction that suppresses savings-contract lapse is absent;
  2. **the contract is terminable at the end of each *Versicherungsperiode***, which for a
     monthly-paying contract is monthly [R8], so exit is frictionless in time as well as in money;
  3. **the need that motivated the purchase amortises** — a mortgage is repaid, children become
     independent — so lapse should **rise** in the later durations of a long term, which is the
     opposite of the savings-product shape.
  The `[std]` assumption shipped is **6 % in policy year 1, 4 % in years 2 and 3, and 3 % thereafter**,
  with the rationale above and an argued plausible range of **2 % to 8 %** in the early years. **No
  German figure supports any of it** (gap 13).
- **Anti-selective lapse.** Healthy lives can re-underwrite into a cheaper contract; impaired lives
  cannot. So the lapsing population is **healthier than the remaining one**, and a term book's
  mortality drifts up relative to a table calibrated on the whole cohort. **Delib does not model
  selective lapse** — the base run uses one mortality basis for stayers and leavers — and this is
  recorded as a known simplification and as a listed modelling pitfall.
- **The *Zahlbeitrag* is itself a lapse driver.** A cut in the *Beitragsverrechnung* raises the bill
  without any change the policyholder agreed to, and the policyholder's remedy is to leave [R6]
  (mechanic 5). **A model that raises the *Zahlbeitrag* toward the *Bruttobeitrag* in a stress and
  leaves the lapse assumption unchanged is understating the stress.** This is a listed pitfall.
- **Death.** One decrement, one benefit, no interlock (mechanic 2). The only complication is the
  three-year *Selbsttötung* window, which changes the **benefit** and not the decrement (mechanic 12).
- **Premium cessation.** Premiums stop on death and at the end of the *Beitragszahlungsdauer*, and
  the *Beitragszahlungsdauer* may be shorter than the *Versicherungsdauer* (mechanic 4). The
  processing order in the technical notes must put premium collection before the death decrement in
  the year of death if the tariff collects in advance, and the model must say which it does.

### 18. Taxation

- **The *Todesfallleistung* is free of *Einkommensteuer*.** § 20 Abs. 1 Nr. 6 EStG taxes the
  *Unterschiedsbetrag* on a life-insurance **survival or surrender** payment [inherited:
  `kapitallebensversicherung.md` R10] [R14]; a pure death benefit paid to a third party is not
  investment income of the policyholder and is **not caught** [R14] `[unverified]` (gap 16). The
  12/62 rule, the *Halbeinkünfteverfahren* and the **50 % *Mindesttodesfallschutz*** requirement for
  post-1 April 2009 contracts [inherited: `kapitallebensversicherung.md` R10, R12] are all rules
  about **savings** contracts, and the last of them exists precisely to stop savings contracts
  presenting themselves as death covers. **None of them applies to a pure RLV.**
- **The *Erbschaftsteuer* is the only tax that reaches this product**, and it reaches it hard for the
  wrong beneficiary [R15]:
  - the benefit is an ***Erwerb von Todes wegen*** under § 3 Abs. 1 Nr. 4 ErbStG where the deceased
    concluded and paid for the contract on his own life;
  - the *Freibetrag* depends on the relationship — **500,000 EUR** spouse or registered partner,
    **400,000 EUR** per child, **200,000 EUR** per grandchild, **20,000 EUR** in *Steuerklasse* III,
    which includes an **unmarried partner** — and the rate schedule begins at **7 %** in class I and
    at **30 %** in class III;
  - **every one of those figures is `[unverified]`** (gap 18) and is carried downstream as a `[std]`
    illustration.
  - **The planning response is the *Über-Kreuz-Versicherung*** (mechanic 14), which removes the
    benefit from the charge entirely by making the recipient the owner and payer of the contract.
- **A *unwiderrufliches Bezugsrecht* changes the timing** of the charge and the policyholder's power
  to alter the nomination [R7] `[unverified]`. Not modelled.
- **Premiums.** *Sonderausgabenabzug* is available in principle under § 10 Abs. 1 Nr. 3a EStG among
  the *sonstige Vorsorgeaufwendungen*, and is in practice worth **nothing** to most taxpayers because
  the annual ceiling is already consumed by health and long-term-care contributions [R14]
  `[unverified]` (gap 17). **No ceiling figure is stated in this file.**
- **No *Versicherungsteuer***: life insurance is exempt [R16] `[unverified]`. The German premium is
  therefore quoted gross of nothing, unlike a French *cotisation* quoted "TTC" [`frlib` mechanic 13].
- **Nothing in this section is modelled.** The delib model publishes **gross** liability cash flows;
  tax on the beneficiary is a policyholder-side consequence and is documented, not computed.

### 19. Market context

- **The size of the German *Risikoversicherung* segment was not established** — no contract count, no
  new-business volume, no premium income, no aggregate *versicherte Summe*, no average sum insured
  and no average premium [R18] (gap 13). This is the single largest evidential hole in the file after
  the price points.
- What can be said, and is structural rather than statistical: a term contract's **premium** is tiny
  relative to its **sum insured**, so the segment is far larger measured by risk carried than by
  premium earned, and any market ranking by premium income systematically understates it. That is
  arithmetic, not an observation.
- **Distribution.** Germany runs a genuinely three-channel market in this product — tied agents and
  bank branches [S8] [S9], independent brokers [S7] [S10] [S11], and direct writers [S3] [S4] [S12] —
  and the channel is visible in the ***Brutto*/*Zahlbeitrag* spread** because acquisition cost is the
  largest thing that differs between them (mechanic 5). **The Continentale / Europa pair is the
  cleanest natural experiment** in the German market, one group running a broker carrier and a direct
  carrier on the same product [S12], and **it was not sampled** (gap 5).
- **The comparison-portal layer is a market participant, not just an observer.** Because no German
  carrier publishes a rate card, the portals [S14] are where price competition actually happens, and
  a tariff's design is shaped by how it will rank in a portal's default query — which is a
  *Zahlbeitrag* query. **That is a plausible structural explanation for why the *Zahlbeitrag* is
  marketed and the *Bruttobeitrag* is disclosed**, and it is `[unverified]`.
- **The consumer-protection line** runs the other way: compare the *Bruttobeitrag*, because that is
  what you can be made to pay [S15] [S16] [S17]. The spread is a rated criterion [S17] [R20]
  `[unverified]`.

### 20. What a projection model needs, and what the corpus supplies

| Model input | Status | Tag |
|---|---|---|
| Benefit definition | established in full — sum insured on death inside the term, nothing otherwise | [R1] [R2] [S5] [S15] |
| Versicherungssumme shapes | three shapes established structurally; no schedule parameter established | mechanic 3, gap 15 |
| Premium form | level Bruttobeitrag over the term, established structurally | [R6] [R10], mechanic 4 |
| Bruttobeitrag / Zahlbeitrag mechanic | **established in kind** — Beitragsverrechnung, guaranteed gross, non-guaranteed billed | [R5] [R6] [R9] [S5] |
| Beitragsverrechnungssatz `v` | **not established at any level** | **[std]** 0.57, gap 1 |
| MindZV minimum allocation from the Risikoergebnis | established, 90 % | [R9] inherited |
| Mortality table family | established — DAV 2008 T, with R and NR variants, medically underwritten only | [R12] inherited |
| Mortality table values | **not public; not redistributed** | **[std]** proxy, mechanic 16 |
| Sicherheitszuschlag magnitude | **not established** | **[std]** m = 1.25, gap 6 |
| Unisex mixing ratio | mechanism established; carrier ratios proprietary | **[std]** 50/50, [R13] |
| Smoker / non-smoker mortality ratio | split established and actuarially sanctioned; **no ratio established** | **[std]** 2.20, gap 1 |
| Berufsgruppen structure | rating factor established; **no class list or loading established** | gap 22 |
| Risikozuschlag scale | mechanism established; **no scale is public in Germany or France** | **[std]** 1.00, mechanic 9 |
| Rechnungszins | established, 1.00 % for new business from 2025; immaterial here | [R10] inherited |
| Höchstzillmersatz | established, 25 permille of the Beitragssumme | [R10] inherited |
| Actual acquisition and admin cost levels | **not established; structurally undisclosed** | **[std]**, gap 8 |
| Ratenzahlungszuschlag | market convention 2 / 3 / 5 % | **[std]**, gap 21 |
| Rückkaufswert | **none** — established in substance, `[unverified]` in statutory wording | [R2], gap 2 |
| Beitragsfreistellung | right exists, benefit collapses to nil | [R3] [R8] |
| Selbsttötung window | established in full, three years, benefit substitution | [R1] inherited |
| Selbsttötung clock on an increment | **not established** | gap 9 |
| Kriegsklausel | shape established structurally; no wording established | mechanic 13 |
| Nachversicherungsgarantie parameters | event families known; **no caps, window or age limit established** | gap 7 |
| Lapse rate | **no term-specific figure of any kind** | **[std]** 6/4/3 %, gap 13 |
| Premium rates | **none public anywhere in the German market** | **[std]** scale, gap 1 |
| Erbschaftsteuer parameters | charge established structurally; **every figure `[unverified]`** | [R15], gap 18 |
| Market size | **not established** | gap 13 |

---

## Observed variation across insurers

**The honest headline: no carrier was sampled.** The frlib term-life file could put eight carriers
side by side because eight *notices d'information* were downloaded and read [`frlib` variations
table]. The sibling delib endowment file could put six carriers side by side, thinly, because six
produced a document in a search result [`kapitallebensversicherung.md` variations table]. **This file
can put none side by side, because no search was available and no document was retrieved.** What
follows therefore states what a variations table would have contained, and records for every cell
that it is empty.

### Carrier coverage actually achieved

| Carrier | Sells an individual RLV | AVB located | Product document content established | Any parameter established |
|---|---|---|---|---|
| CosmosDirekt [S3] | asserted | no | no | no |
| Hannoversche [S4] | asserted | no | no | no |
| HUK-COBURG / HUK24 [S5] | asserted | no | **one guide page URL inherited**, title and four-component surplus vocabulary only | no |
| Debeka [S6] | asserted | no — document library path pattern inherited only | no | no |
| Dialog [S7] | asserted | no | no | no |
| Allianz [S8] | asserted | no | no | no |
| R+V [S9] | asserted | no | no | no |
| Nürnberger [S10] | asserted | no | no | no |
| LV 1871 [S11] | asserted | no | no | no |
| Continentale / Europa [S12] | asserted | no | no | no |
| Seventeen further carriers [S13] | asserted | no | no | no |

### Parameter ranges — what is argued, and what is observed

Every "observed range" below is **argued from structure or from market knowledge**, not observed in a
document. The "who sits where" column is the point of a variations table and it is empty throughout.

| Parameter | Range carried in the delib specification | Who sits where | Tag |
|---|---|---|---|
| Zahl / Brutto ratio | 0.45 to 1.00, representative 0.57 | **not established** | **[std]**, gap 1 |
| Sicherheitszuschlag `m` implied | 1.0 to 1.5 | **not established** | **[std]**, gap 6 |
| Smoker / non-smoker premium ratio | about 1.8 to 2.5 | **not established** | **[std]** 2.04 derived, gap 1 |
| Eintrittsalter | 18 to 65, some carriers to 70 or 75 | **not established** | **[std]**, gap 22 |
| Endalter | 75, with 80 and 85 offered | **not established** | **[std]**, gap 22 |
| Versicherungsdauer | 5 to 40 years | **not established** | **[std]**, gap 22 |
| Mindestversicherungssumme | 10,000 to 50,000 EUR | **not established** | **[std]**, gap 22 |
| Maximum sum without special underwriting | high six to low seven figures | **not established** | **[std]**, gap 22 |
| Vereinfachte Gesundheitsprüfung threshold | **not established at all** | **not established** | gap 22 |
| Berufsgruppen count | small, or none below a hazardous-occupation list | **not established** | gap 22 |
| Nachversicherung event list | nine recurring event families | **not established** | gap 7 |
| Nachversicherung cap and age limit | **not established at all** | **not established** | gap 7 |
| Ratenzahlungszuschlag | 2 % / 3 % / 5 % | market convention, no attribution | **[std]**, gap 21 |
| Rückkaufswert | none, market-wide | uniform | [R2], gap 2 |
| Selbsttötung window | three years, statutory minimum, extendable | statutory | [R1] |
| Versicherungssumme shapes offered | all three at most carriers | **not established** | mechanic 3 |
| Verbundene Leben offered | widely | **not established** | mechanic 14 |
| Lapse rate | 2 % to 8 % early durations | **not established** | **[std]**, gap 13 |

### What the corpus supports as a representative design

The design below is what the **mechanics** support. It is a **composite**, not a copy of any carrier's
tariff, and it could not be otherwise, because no carrier's tariff was read.

- **Single life, individual, participating *Risikolebensversicherung***, written on medical
  underwriting, in the *Neubestand* [R9] [R12].
- ***Konstante Versicherungssumme*** of **300,000 EUR** as the base shape, with `linear fallend` and
  `annuitätisch fallend` available as external schedule tables on the same chassis (mechanic 3).
  **[std]**; 300,000 EUR is chosen because it is the sum at which the *Erbschaftsteuer* contrast of
  mechanic 14 becomes the decisive product-design fact.
- **Entry age 35, term 25 years, cover to age 60**, level *Bruttobeitrag* over the whole term
  (mechanic 4). **[std]**; the term is long enough for the *Deckungskapital* to build and run off
  visibly and short enough to fit one worked-example table.
- ***Bruttobeitrag* struck on first-order bases** — a DAV 2008 T-shaped `[std]` proxy at
  `q1 = 2.25 x q2`, unisex 50/50, non-smoker, *Rechnungszins* 1,00 %, *gezillmert* at the 25 ‰
  ceiling [R10] [R12] [R13].
- ***Zahlbeitrag* derived, not assumed**: the model computes the mortality margin against the
  second-order basis, returns the MindZV minimum of **90 %** of it as *Beitragsverrechnung*, and
  publishes **both** premium streams [R9] (mechanic 5). The derived ratio is **0.57 [std]**.
- **No *Rückkaufswert*, no *beitragsfreie Versicherungssumme*, no maturity value.** Lapse is a pure
  decrement and `claims_surr` is structurally zero [R2] [R3] [R8] (mechanic 11).
- **Three-year *Selbsttötung* window** applied as a benefit switch paying the (nil) *Rückkaufswert*
  [R1] (mechanic 12).
- **No exclusion decrement.** The *Kriegsklausel* is documented and not modelled (mechanic 13).
- **Options off in the base run**: *Nachversicherungsgarantie*, *Dynamik*, *verbundene Leben*, UZV,
  BUZ, *vorgezogene Todesfallleistung* (mechanics 8, 14).
- **Lapse `[std]` at 6 % / 4 % / 3 %**, with selective lapse deliberately not modelled and recorded
  as a pitfall (mechanic 17).
- **Gross cash flows, undiscounted.** No *Deckungsrückstellung*, no Solvency II, no tax computation
  [R21] [R22].

---

## Gaps and caveats

1. **No price point of any kind was obtained, and this is the largest gap in the file.** The brief
   asked for annual *Zahlbeiträge* at 100,000 EUR and 300,000 EUR, ages 30 and 40, non-smoker, from
   comparison portals, on the correct ground that these are the only public German price data for
   this product. No German carrier publishes a rate card [S3]–[S13]; the *Produktinformationsblatt*
   quotes the applicant's own premium [S2]; a portal result is generated per query rather than
   published [S14]; and no search or fetch was available. **Not one *Bruttobeitrag*, *Zahlbeitrag*,
   spread ratio or smoker ratio in this file is an observation.** The whole premium scale of mechanic
   16 is a `[std]` construction. **One published *Bruttobeitrag* / *Zahlbeitrag* pair at a known age,
   sum and term would pin the *Sicherheitszuschlag* directly and re-derive the rest**, and is the
   single highest-value datum a later researcher could add.

2. **The statutory basis for the absence of a *Rückkaufswert* is `[unverified]`.** The claim that
   § 169 Abs. 1 VVG confines the surrender-value duty to a life insurance whose insured event is
   **certain to occur**, and therefore does not reach a term assurance, is asserted from knowledge of
   the section's structure [R2]. **No search returned that wording.** The practical result — that a
   German RLV pays nothing on *Kündigung* — is corroborated by uniform market practice and is not in
   doubt; the route to it is. A reader relying on the legal analysis must check § 169 Abs. 1 at
   source. The same `[unverified]` applies to whether § 165 carries the same limitation [R3].

3. **No *Produktinformationsblatt* was located, in specimen or in model form** [S2]. The PIB is the
   one German document type that routinely shows the *Bruttobeitrag* and the *Zahlbeitrag* side by
   side, which makes its absence the direct cause of gap 1. Its field list is asserted from the
   document's purpose and is `[unverified]`.

4. **MindZV section numbering is unsettled.** The three percentages — **90 % of the *Risikoergebnis*,
   90 % of the investment result, 50 % of the *übriges Ergebnis*** — are inherited from a
   search-corroborated sibling entry and are used [R9]. **The section numbers are not**: the sibling
   file places the investment result at § 6, and the author's recollection places it at § 4, the
   *Risikoergebnis* at § 5 and the *übriges Ergebnis* at § 6. No MindZV section number is cited
   anywhere in the delib `risikolebensversicherung` documents.

5. **The Continentale / Europa natural experiment was not run** [S12]. One group runs a broker-channel
   and a direct-channel carrier on the same product with the same underwriting and reserving basis,
   which is the cleanest available way to isolate the channel effect on the *Brutto*/*Zahlbeitrag*
   spread. Neither carrier's documents were reached. The same applies to Dialog as a monoline
   comparator [S7].

6. **The magnitude of the DAV 2008 T *Sicherheitszuschlag* was not established.** The *Richtlinie*
   regulates the **procedure** for setting it [R12]; the level is not public. It is the parameter that
   determines the *Brutto*/*Zahlbeitrag* spread almost by itself (mechanic 5), and it is shipped as
   **[std] `m = 1.25`** with the calibration and sensitivity of mechanic 16 stated in full.

7. **No *Nachversicherungsgarantie* parameters were established** [S11] [S17]. The nine recurring
   event families of mechanic 8 are asserted from market knowledge and are `[unverified]`; **no
   exercise window, no per-event cap, no cumulative cap and no maximum age comes from any document.**
   The option is off in the base run, so the gap does not affect the reference implementation's
   numbers — but it does mean the specification's option section is entirely `[std]`.

8. **German term-life charge levels are structurally undisclosed, not merely unretrieved.** There is
   no *Effektivkostenquote* because there is no yield; no *Basisinformationsblatt* because the product
   is not a PRIIP; and the *Produktinformationsblatt* quotes premiums, not loadings [R17]. So
   acquisition, collection and administration cost levels would have been missing even with full
   egress. Every charge parameter is **[std]** (mechanic 16). **The `[std]` α at the 25 ‰ Zillmer
   ceiling is an assumption that a term tariff runs at the cap, and it may well be wrong**; a carrier
   with a slim direct-channel acquisition cost would sit far below it.

9. **Whether the § 161 three-year clock restarts on an increase is not established** [R1]. The French
   statute expressly restarts its one-year clock for the increment [`frlib` R1]; German AVB practice
   is understood to do the same, and **no wording was seen**. This matters because the
   *Nachversicherungsgarantie* makes increments routine (mechanic 8).

10. **What German carriers actually offer in place of *Beitragsfreistellung* was not established**
    [R3]. *Beitragsstundung*, a temporary *Ruhen*, and a reduction of the *Versicherungssumme* are
    asserted from market knowledge and are `[unverified]`. The analysis that § 165 and § 166 both
    collapse to nil on this product [R3] [R8] is structural and does not depend on the gap.

11. **The *Zillmerung* treatment of a term contract is only half established.** The 25 ‰ cap on the
    *Beitragssumme* is inherited and firm [R10]; **whether that cap is applied to a *Risikoversicherung*
    in the same way as to a savings contract was not established**, and neither was the
    *Nullstellung* question — whether a negative individual *Deckungsrückstellung* must be floored at
    zero for balance-sheet purposes [R21]. Both matter for this product specifically, because a
    *gezillmert* term contract sits below zero for a long stretch (mechanic 10). The delib model does
    not publish a reserve, so neither gap reaches its cash flows.

12. **The DAV 2008 T data coverage for the term-assurance segment is not established.** The sibling
    research established that the cleansed insured data covered **60 % of the German market in the
    *Kapitallebensversicherung* segment**; the corresponding term-assurance figure **was truncated in
    the search summary** [R12] [inherited: `kapitallebensversicherung.md` R14]. Since this is the
    table for **this** product, that is the one number of the two that mattered.

13. **The German *Risikoversicherung* market has no numbers in this file.** No contract count, no new
    business, no premium income, no aggregate *versicherte Summe*, no average sum insured, no average
    premium, and — most consequentially for the model — **no segment-specific *Stornoquote*** [R18].
    The inherited whole-market *Stornoquote* of **2,72 % (2024) / 2,56 % (2023)**, with a second and
    irreconcilable measure at **1,2 % (2024)** [inherited: `kapitallebensversicherung.md` R20], is a
    book average dominated by long-dated savings contracts and is **deliberately not used**. The
    delib lapse assumption is **[std] 6 % / 4 % / 3 %** on the structural argument of mechanic 17,
    with an argued range of 2 % to 8 %, and **no German figure supports any of it.**

14. **No BaFin material specific to term assurance was located.** *Merkblatt* 01/2023 (VA) is
    expressly about ***kapitalbildende*** products and does not reach a pure protection contract
    [R19] [inherited: `kapitallebensversicherung.md` R17]. So this file carries **no supervisory
    conduct standard** for the product, and a reader must not import the endowment one.

15. **Falling-sum schedule parameters were not established** (mechanic 3). The nominal rate a German
    *annuitätisch fallende* tariff amortises at, the residual sum at expiry, and the premium
    reduction relative to the constant shape are all absent. The model computes the reduction from
    the schedule, so the gap affects the schedule table only, which is **[std]**. The same applies to
    the *verbundene Leben* premium relative to two single contracts.

16. **The non-application of § 20 Abs. 1 Nr. 6 EStG to a pure death benefit is `[unverified]`**
    [R14]. It is asserted from the section's own subject matter — an *Unterschiedsbetrag* on a
    survival or surrender payment — and is corroborated indirectly by the existence of the
    *Mindesttodesfallschutz* rule, which exists to stop savings contracts posing as death covers
    [inherited: `kapitallebensversicherung.md` R12]. **No search confirmed it directly.**

17. **The *Sonderausgaben* ceiling figures are deliberately omitted** [R14]. The classification of RLV
    premiums among the *sonstige Vorsorgeaufwendungen* under § 10 Abs. 1 Nr. 3a EStG, and the
    practical result that the ceiling is already consumed by health and long-term-care contributions,
    are asserted and `[unverified]`. **No ceiling amount is stated anywhere in this file**, because
    the amounts differ by taxpayer category and none could be confirmed.

18. **Every *Erbschaftsteuer* figure is `[unverified]`** [R15]. The *Freibeträge* (500,000 /
    400,000 / 200,000 / 100,000 / 20,000 EUR), the three *Steuerklassen*, and the rate schedule
    beginning at 7 % in class I and 30 % in class III are stated from knowledge and confirmed by no
    source. **The 84,000 EUR illustration of mechanic 14 is arithmetic performed on unverified
    inputs** and is carried downstream as a `[std]` illustration, never as a citation. The
    *structural* conclusion — that an unmarried partner faces a large charge a spouse does not, and
    that this is why the *Über-Kreuz* structure exists — does not depend on the exact figures.

19. **The *Versicherungsteuer* exemption's statutory location is `[unverified]`** [R16]. That German
    life insurance premiums bear no insurance premium tax is not in doubt; the section reference is
    not confirmed. The delib model carries no premium-tax line and states why.

20. **No case law is cited by name anywhere in this file** [R23]. German term-life litigation
    clusters on the completeness of the *Gesundheitsfragen* answers, on the § 19 Abs. 5 warning
    requirement, and on the mental-illness exception to § 161 — and **not one decision was located,
    so none is named and none is invented.**

21. **The *Ratenzahlungszuschlag* of 2 % / 3 % / 5 % is a market convention with no carrier
    attribution**, inherited from the sibling research [inherited: `kapitallebensversicherung.md`
    R28]. Whether German RLV carriers strike it on the *Bruttobeitrag* or the *Zahlbeitrag* was not
    established; the delib model applies it to the *Zahlbeitrag* and says so (mechanic 7).

22. **No underwriting parameter was established at any level.** Health-question look-back periods;
    the sum insured above which a medical examination is required; the sum below which a simplified
    question set applies; the smoker qualifying period; the *Berufsgruppen* count and their loadings;
    the entry-age and cover-age envelopes; the minimum and maximum sums insured — **none of it comes
    from any document** (mechanic 9). Every one is **[std]** in the specification. This is the second
    largest evidential hole after the price points, and it is the one a single retrieved AVB would
    close almost entirely.

23. **Comparison with the sister libraries, stated so the difference is not glossed.** `frlib`'s
    term-life file rests on eight *notices d'information* and five Légifrance articles **downloaded
    and read**. The two sibling delib files rest on search-result summaries. **This file rests on
    neither.** Its `[S#]` and `[R#]` tags are pointers to documents that exist and were not opened;
    its inherited-corroboration notes are the only evidence in it that anyone checked anything; and
    its numbers are `[std]` constructions with their arithmetic shown. That is a weaker document than
    its siblings, it is weaker in a way that is visible on every page, and the alternative — a
    confident-looking file full of invented figures — would have been worse.
