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
search corroboration (session budget exhausted)**, except where an entry states an inherited
corroboration from a sibling delib research file. Canonical `gesetze-im-internet.de` URLs are given
in the form `.../vvg_2008/__<n>.html`, which the sibling research confirmed the host uses
[inherited: `kapitallebensversicherung.md` R1–R5]; where such a URL was **not** itself returned by a
search it is marked `[unverified]`.

### R1 — VVG § 161, *Selbsttötung*

- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` — **this URL was returned by a search
  during the sibling research** [inherited: `kapitallebensversicherung.md` R4]
- **Inherited corroboration — the strongest single item in this file.** The sibling research
  established the following, and it applies to a *Risikolebensversicherung* with more force than to
  the endowment it was established for:
  - In an insurance **for the event of death** the insurer is ***leistungsfrei*** if the *versicherte
    Person* **intentionally takes her own life before three years have elapsed since conclusion of
    the contract**.
  - **Exception**: not so where the act was committed **in a state excluding free determination of
    the will, caused by a *krankhafte Störung der Geistestätigkeit***.
  - **The three-year period may be extended by individual agreement** — a statutory minimum window,
    extendable and by implication not shortenable.
  - **Where the insurer is *leistungsfrei* it must nevertheless pay the *Rückkaufswert*, including
    *Überschussanteile*, under § 169.** The German rule is a **benefit substitution**, not a
    forfeiture.
  - The section sits in **Chapter 5** of the VVG.
- **Why it bites harder here than on an endowment.** On a *Kapitallebensversicherung* the
  substitution is soft: the *Rückkaufswert* after three years is a real sum. On a
  *Risikolebensversicherung* the *Rückkaufswert* is nil or nominal (mechanic 11), so the
  substitution is, in economic substance, **a forfeiture with a rounding error attached**. A model
  of this product must therefore carry the *Selbsttötung* rule as a **benefit switch**, not as a
  decrement adjustment, and the substituted amount is what the model's `Rückkaufswert` cell returns —
  which for the base design is zero.
- The three-year clock's behaviour on an **increase** of the *Versicherungssumme* — whether it
  restarts for the increment, as the French one-year clock does under art. L. 132-7 alinéa 2 — is
  **not established from the statute**. German AVB practice is understood to restart it for the
  increment, which is also what the statutory words "seit Vertragsschluss" imply for a genuinely new
  cover increment; **the AVB practice is `[unverified]`** (gap 9).

### R2 — VVG § 169, *Rückkaufswert*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R2]
- **Inherited corroboration**, from the endowment research: the section governs the surrender value
  payable when a life contract is terminated by the policyholder; **Abs. 3** provides the
  ***Mindestrückkaufswert***, computed on the basis that acquisition costs are spread over the
  **first five years** rather than charged at once; the value is the *Deckungskapital* computed by
  recognised actuarial rules, and a *Stornoabzug* may be deducted only where it is **agreed,
  reasonable and quantified in the contract** [inherited: `kapitallebensversicherung.md` R2, R22,
  R24].
- **The scope limitation that decides this product.** § 169 Abs. 1 confines the surrender-value duty
  to a life insurance **whose insured event is certain to occur** — the German formulation turns on
  whether the *Eintritt der Leistungspflicht* is *gewiss*. A *Kapitallebensversicherung*, a
  *Rentenversicherung* and a whole-of-life *Todesfallversicherung* all satisfy that test; a
  ***Risikolebensversicherung* does not**, because the insured may survive the term and the insurer
  may never owe anything. **The consequence is that the RLV has no statutory *Rückkaufswert*.**
  This scope limitation is asserted from knowledge of the section's structure and was **not**
  established by any search: it is `[unverified]` at the level of the statutory wording, and it is
  the single most consequential `[unverified]` claim in this file (gap 2). Its practical result —
  that a German RLV pays nothing on *Kündigung* — is corroborated independently by uniform market
  practice and is not itself in doubt.

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R3]
- **Inherited corroboration**: the policyholder may **at any time, for the end of the current
  *Versicherungsperiode*, demand conversion into a *prämienfreie Versicherung***; the reduced benefit
  is calculated by recognised actuarial rules for the end of that period; the insurer may make the
  same *Stornoabzug* as on surrender; and the right is subject to a **minimum benefit test** — where
  the resulting *beitragsfreie Versicherungsleistung* would fall below an agreed minimum, the
  insurer pays the *Rückkaufswert* instead [inherited: `kapitallebensversicherung.md` R3].
- **Effect on this product.** The right exists in form and is empty in substance: the *Deckungskapital*
  of a level-premium RLV is small and, after *Zillmerung*, is zero or negative through much of the
  term (mechanic 10), so the *beitragsfreie Versicherungssumme* it would buy fails the minimum test
  in most durations, and the fallback — payment of the *Rückkaufswert* — is a payment of nil. Whether
  § 165's own scope carries the same *gewiss* limitation as § 169 Abs. 1 was **not established**
  (gap 2); it makes no practical difference, because both routes terminate in nil on this product.
- What German carriers offer instead of *Beitragsfreistellung* on an RLV — *Beitragsstundung*, a
  temporary *Ruhen* of the contract with reduced or suspended cover, or a reduction of the
  *Versicherungssumme* — is **market practice and is `[unverified]`** (gap 10).

### R4 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and *Anfechtung*

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R5]; `__20.html`, `__21.html` and
  `__22.html` are the canonical forms for the neighbouring sections and are `[unverified]`
- **Inherited corroboration on § 19** [`kapitallebensversicherung.md` R5]:
  - **Abs. 1 Satz 1** obliges the policyholder to disclose the *gefahrerhebliche Umstände* known to
    her **which the insurer has asked about in *Textform***. **The duty is question-bounded** — there
    is no free-standing duty to volunteer.
  - The provision gives the insurer the right to put health questions in order to assess the risk and
    decide whether to accept **with restrictions** or **only at an increased premium**.
  - **Remedies.** On a breach the insurer may **adjust the contract retrospectively** — excluding the
    undisclosed risk from cover, or raising the premium by a ***Risikozuschlag*** — instead of
    refusing to perform; for simple or gross negligence this is reported as the usual outcome.
  - **Time limits.** The adjust / terminate / rescind rights **lapse five years** after conclusion
    for negligent breach and **ten years** for **intentional or *arglistig*** breach.
- **Not inherited, asserted from knowledge and `[unverified]`**: that § 19 Abs. 5 conditions the
  insurer's remedies on having advised the applicant of the consequences of a breach **in a separate
  communication in *Textform***; that § 21 Abs. 2 makes the insurer's remedy ineffective as against
  a claim where the undisclosed circumstance caused neither the occurrence of the insured event nor
  the extent of the benefit; and that § 22 preserves the insurer's right of ***Anfechtung wegen
  arglistiger Täuschung*** alongside the § 19 remedies. All three matter for a term product, where
  the whole of the underwriting decision is a health questionnaire and the whole of the claim risk
  is whether the answers were true.

### R5 — VVG § 153, *Überschussbeteiligung*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — returned by a search during the
  sibling research [inherited: `kapitallebensversicherung.md` R1]
- **Inherited corroboration**: the policyholder is **entitled to share in the surplus and in the
  *Bewertungsreserven***; participation may be excluded only by express agreement; the surplus is to
  be allocated by a method that is ***verursachungsorientiert*** — attributed according to how the
  contract caused it — under a procedure recognised by actuarial rules; **Abs. 3** governs the share
  in *Bewertungsreserven*, allocated at least annually and payable on termination [inherited:
  `kapitallebensversicherung.md` R1, R8].
- **Why *verursachungsorientiert* is the load-bearing word for this product.** A
  *Risikolebensversicherung* causes essentially **one** kind of surplus — the *Risikoüberschuss*,
  the difference between the prudent first-order mortality it was priced on and the mortality the
  portfolio actually experiences. A cause-oriented allocation therefore returns to the RLV book what
  the RLV book earned, and returns it as a **reduction of the premium** rather than as an addition
  to a reserve the product does not have. The German market's *Beitragsverrechnung* is § 153
  operating on a product with no savings element (mechanic 5).
- Participation in *Bewertungsreserven* under Abs. 3 is, on this product, **structurally negligible**:
  the *Bewertungsreserven* attributable to a contract scale with its *Deckungsrückstellung*, and an
  RLV's is nil or nominal. **That inference is structural and `[unverified]`.**

### R6 — VVG § 163, *Anpassung der Prämie* (the *Treuhänder* clause)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`. The sibling research
  recorded the section as governing premium and condition adjustment in life insurance and located
  contemporaneous market commentary on the *Treuhänderklausel* [inherited:
  `klassische_rentenversicherung.md` R3, R17, R18]
- Content: the insurer may raise the premium of a life contract only under narrow conditions — an
  **unforeseen and not merely temporary** change in the circumstances underlying the calculation,
  where the adjustment is necessary to safeguard the permanent fulfilment of the obligation, and
  where an **independent *Treuhänder*** confirms the calculation bases. The policyholder may respond
  by demanding a corresponding reduction of the benefit instead.
- **Effect on this product, and the distinction that must not be blurred.** § 163 governs increases
  of the ***Bruttobeitrag***. On a German RLV that route is essentially never used: the
  *Bruttobeitrag* is guaranteed for the term and stays where it was struck. What actually moves the
  customer's bill is **the *Überschussdeklaration*** — a reduction of the *Beitragsverrechnung*
  raises the *Zahlbeitrag* toward the *Bruttobeitrag* with **no § 163 procedure, no *Treuhänder* and
  no policyholder remedy**, because no guaranteed term of the contract has changed. **This is the
  single most important legal fact about the German term-life premium** and it is the reason the
  *Bruttobeitrag* is the number that matters (mechanic 5). The statement that § 163 is not used in
  practice on RLV *Bruttobeiträge* is `[unverified]`.

### R7 — VVG §§ 150, 159, 162 — *versicherte Person*, *Bezugsberechtigung*, *Herbeiführung des Versicherungsfalles*

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__150.html`, `__159.html`, `__162.html`, all
  canonical forms and all `[unverified]`
- Content, asserted from knowledge and `[unverified]` in every particular:
  - **§ 150** permits a life insurance on the life of another. Where the agreed benefit **exceeds the
    ordinary funeral costs**, the ***schriftliche Einwilligung*** (written consent) of that person is
    required. **This is the provision that makes the *Über-Kreuz-Versicherung* work and constrains
    it**: each partner must consent in writing to the other insuring his life (mechanic 14). It is
    also why a *verbundene Leben* contract needs both lives' consent.
  - **§ 159** governs the *Bezugsberechtigung*: the policyholder may name a beneficiary and may make
    the nomination **revocable** (the default) or **unwiderruflich**. An unwiderrufliches Bezugsrecht
    vests the claim in the beneficiary immediately and takes it out of the policyholder's disposal —
    with consequences for insolvency protection and for tax.
  - **§ 162** makes the insurer *leistungsfrei* where the **policyholder** intentionally brings about
    the death of the *versicherte Person* by an unlawful act, and strips the **beneficiary** who does
    so of his entitlement (his share falling to the others or to the estate).
- All three are structural to a product where *Versicherungsnehmer*, *versicherte Person* and
  *Bezugsberechtigter* are routinely three different people — which on a *Risikolebensversicherung*
  is the normal case, not the exception.

### R8 — VVG § 152 (*Widerruf*), § 166 (*Beitragsverzug*), § 168 (*Kündigung*)

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__152.html`, `__166.html`, `__168.html`, all
  canonical forms and all `[unverified]`
- Content, asserted from knowledge and `[unverified]`:
  - **§ 152** extends the general *Widerrufsfrist* of § 8 from 14 days to **30 days** for life
    insurance, and provides that where the contract is withdrawn the insurer returns the premiums,
    less in some circumstances the cost of cover actually enjoyed.
  - **§ 166** governs non-payment of a *Folgeprämie* in life insurance and replaces the general
    § 38 machinery. The insurer's *Zahlungsaufforderung* must be in *Textform*, must set a deadline
    of **at least one month**, and must state the consequences. The distinctive German step is what
    happens next: **the insurer's termination converts the contract into a *prämienfreie
    Versicherung*** rather than simply ending it — **unless** the *beitragsfreie
    Versicherungsleistung* falls short of the agreed minimum, in which case the contract ends.
  - **§ 168** gives the policyholder a right to **terminate at the end of each current
    *Versicherungsperiode*** on a contract with running premiums; the *Versicherungsperiode* follows
    the *Zahlweise*, so a monthly-paying contract is terminable monthly.
- **Effect on this product.** § 166's paid-up conversion is the general German lapse path, and on an
  RLV it **collapses into simple termination** because the minimum test fails (R3). So an RLV lapse
  is a pure exit: cover stops, nothing is paid, and — because the premium is paid in advance — at
  most an unearned fraction is returned. That makes `claims_surr` structurally zero in the model
  and makes the lapse assumption a pure decrement with no benefit attached.

### R9 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` ·
  `https://www.buzer.de/gesetz/12013/a198221.htm` — both returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R6]
- **Inherited corroboration — the second load-bearing item in this file**
  [`kapitallebensversicherung.md` R6]:
  - The minimum allocation to the *Rückstellung für Beitragsrückerstattung* in respect of the
    ***Risikoergebnis*** attributable to *überschussberechtigte* contracts is **90 % of that
    result**.
  - The minimum in respect of the **investment result** is **90 % of the *anzurechnende
    Kapitalerträge***, struck **after** deducting the *Aufwand für die Diskontierung der
    Deckungsrückstellung* — the mechanism by which the guaranteed interest is taken off the top
    before the policyholder's share is computed.
  - The minimum in respect of the ***übriges Ergebnis*** — which carries the expense result — is
    **50 %**.
  - The aggregate test combines the three; the minimum is computed and complied with **separately
    for *Altbestand* and *Neubestand***.
  - **Section attribution is not settled.** The sibling entry attributes the investment-result rule
    to § 6 MindZV; the author's own recollection places the investment result at § 4, the
    *Risikoergebnis* at § 5 and the *übriges Ergebnis* at § 6. **The three percentages —
    90 % / 90 % / 50 % — are inherited and used; the section numbers are `[unverified]` and are not
    cited anywhere in the delib library** (gap 4).
- **Why this regulation is the engine of the German term-life product.** An RLV has no meaningful
  investment result and a modest expense result. Its technical outcome is almost entirely
  *Risikoergebnis*, and **90 % of that must go back to policyholders**. The insurer prices on a
  prudent first-order mortality basis, earns a large mortality margin against a medically selected
  portfolio, and is then obliged to return the overwhelming majority of it. The *Beitragsverrechnung*
  is the mechanism by which it does so, and the width of the *Brutto*/*Zahlbeitrag* spread is, to a
  first approximation, **a direct function of how prudent the first-order basis is** (mechanic 5).

### R10 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.buzer.de/gesetz/12006/index.htm` — returned by a search during the sibling
  research, which used it for the amendment history [inherited: `kapitallebensversicherung.md` R7]
- **Inherited corroboration** [`kapitallebensversicherung.md` R7]:
  - The ***Höchstrechnungszins*** was raised **from 0,25 % to 1,00 % with effect from 1 January
    2025**. Three independent search results agreed on the sequence **4 % in 1994 → 0,25 % in 2022 →
    1,00 % in 2025**, the 2025 move being the **first increase since 1994**.
  - The ***Höchstzillmersatz*** may not exceed **25 ‰ of the *Beitragssumme*** — the sum of all
    premiums payable over the term — cut **from 40 ‰** by the LVRG with effect from **1 January
    2015**, so an undertaking may recognise at most **2,5 % of the *Beitragssumme*** as
    *Abschluss- und Vertriebskosten*.
- **Effect on this product.** The *Rechnungszins* is close to irrelevant to an RLV: the contract's
  own *Deckungsrückstellung* is small and short-lived, so a 75-basis-point change in the discount
  rate moves the *Bruttobeitrag* by very little. The *Höchstzillmersatz* is the opposite — it is
  **highly relevant**, because 25 ‰ of the *Beitragssumme* of a term contract is a large number
  relative to that contract's tiny reserve, and it is the reason a *gezillmerte*
  *Risikolebensversicherung*'s *Deckungskapital* is **negative or nil for much of its term**
  (mechanic 10). The application of the 25 ‰ cap to a term product specifically was **not
  established** and is `[unverified]` (gap 11).

### R11 — VAG §§ 138–140 — *Gleichbehandlung*, *Überschussbeteiligung*, RfB

- Publisher: Bundesministerium der Justiz (Versicherungsaufsichtsgesetz 2016)
- URL: `https://dejure.org/gesetze/VAG/139.html` — returned by a search during the sibling research
  [inherited: `kapitallebensversicherung.md` R8]; the § 138 and § 140 forms are `[unverified]`
- **Inherited corroboration on § 139** [`kapitallebensversicherung.md` R8]: policyholders are **in
  principle to share in the *Bewertungsreserven* to the extent of one half**; participation by
  **exiting** policyholders is permitted **only to the extent that the *Bewertungsreserven* exceed
  the *Sicherungsbedarf*** arising from contracts with an interest guarantee; and *Sicherungsbedarf*
  is the sum, over contracts with an *überhöhter Rechnungszins*, of the actuarially valued interest
  obligation less the *Deckungsrückstellung*.
- **Not inherited, asserted and `[unverified]`**: that § 138 imposes the ***Gleichbehandlungsgrundsatz***
  — equal treatment of policyholders in equal circumstances in the fixing of premiums and in the
  allocation of surplus — and that § 140 governs the *Rückstellung für Beitragsrückerstattung*,
  including the conditions under which the undertaking may withdraw from it.
- **Effect on this product.** The *Bewertungsreserven* mechanics of § 139 are, on an RLV,
  economically empty (R5). The § 138 equal-treatment principle is the one that binds: it is why an
  insurer declares **one *Beitragsverrechnung* rate per tariff generation and per rating cell**
  rather than negotiating individual discounts, and it is the reason the *Zahlbeitrag* can be
  modelled as a deterministic function of the *Bruttobeitrag* and a declared rate.

### R12 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"

- Publisher: Deutsche Aktuarvereinigung e. V. (DAV). Doc type: *DAV-Richtlinie* / *Fachgrundsatz*,
  with a 2008 derivation paper and a 2022 restatement
- URLs, all returned by a search during the sibling research [inherited:
  `kapitallebensversicherung.md` R14]:
  `https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/` ·
  `https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` ·
  `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf`
- **Inherited corroboration — the third load-bearing item, and this is *the* table for this
  product** [`kapitallebensversicherung.md` R14]:
  - The DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* investigated mortality in life insurance
    **with *Todesfallcharakter*** over **2006 to 2008**, using **German insurers' own policy data**
    together with **German population statistics**, and compared the result against international
    developments.
  - After cleansing, the insured data covered **60 % of the German market in the
    *Kapitallebensversicherung* segment**; the corresponding figure for the term-assurance segment
    **was truncated in the search summary and is not established** (gap 12).
  - The *Richtlinie* **regulates the methodology for deriving mortality tables for reserving and the
    procedure for setting the *Sicherheitszuschläge***.
  - ***DAV 2008 T R*** and ***DAV 2008 T NR*** — smoker and non-smoker — are in principle **also
    suitable for premium calculation** differentiated by smoking status, **but not for policies
    written without a *Gesundheitsprüfung***.
  - **First adopted as a DAV-Richtlinie on 4 December 2008**; restated as a *Fachgrundsatz* dated
    **29 November 2022**.
  - **The table values are not public and delib does not redistribute them.**
- **What this establishes for the delib model.** Four things, and they shape the whole assumption
  set: (i) the German first-order mortality basis for a term product is DAV 2008 T and its smoker /
  non-smoker variants; (ii) the *Sicherheitszuschlag* is **part of the table's own construction**,
  not an extra the insurer bolts on — so "first-order" and "second-order" are two levels of the same
  DAV framework and the model must publish both; (iii) the smoker/non-smoker split is **actuarially
  sanctioned for pricing**, which is why the German market rates on it; (iv) the split is **not**
  available for policies written without medical underwriting, which is why simplified-issue and
  guaranteed-issue German death covers are aggregate-rated. **The magnitude of the
  *Sicherheitszuschlag* was not established and is a `[std]` parameter here** (mechanic 15, gap 6).

### R13 — Unisex pricing: the EU Gender Directive, CJEU C-236/09 (*Test-Achats*) and AGG § 20

- Publisher: Court of Justice of the European Union; Bundesministerium der Justiz (Allgemeines
  Gleichbehandlungsgesetz)
- URL: **not established** for any of them
- Content, asserted from knowledge and `[unverified]` in every particular except the date:
  - The Court's judgment struck down the derogation that had permitted sex-differentiated insurance
    premiums, with effect for contracts concluded **from 21 December 2012**. The frlib research
    reached the same cut-off from the French implementing article, which states the derogation
    survives only for contracts concluded "au plus tard le 20 décembre 2012" [`frlib` R10] — an
    independent arrival at the same boundary, and the closest thing to corroboration this entry has.
  - German implementation runs through the amendment of **§ 20 AGG**, which since that date no longer
    permits sex as a rating factor in new private insurance contracts.
- **Effect on this product, which is larger than on any other delib product.** Female mortality at
  the ages a term contract is sold — 25 to 55 — is roughly **half** male mortality
  `[unverified]`, so a unisex tariff is a blend whose position depends entirely on the **assumed
  sex mix of the tariff's own new business**. A carrier that expects to sell mostly to men prices
  near the male table; one selling mostly to women prices near the female table; and the mix
  assumption is proprietary, unpublished, and re-estimated as experience emerges. **The DAV 2008 T
  variants are sex-distinct** [R12], so every German RLV tariff written since 2013 uses a
  **carrier-chosen mixing ratio** that no source discloses. The delib model therefore carries a
  `[std]` unisex mix (mechanic 15), and this is one of the largest single sources of unexplained
  spread between German carriers' rates.

### R14 — EStG § 20 Abs. 1 Nr. 6 and § 10 Abs. 1 Nr. 3a — income tax on the benefit, deductibility of the premium

- Publisher: Bundesministerium der Justiz (Einkommensteuergesetz); Bundesfinanzministerium
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — returned by a search during the sibling
  research [inherited: `kapitallebensversicherung.md` R10]
- **Inherited corroboration** [`kapitallebensversicherung.md` R10, R11, R12]: § 20 Abs. 1 Nr. 6
  taxes the ***Unterschiedsbetrag*** between the benefit and the premiums paid on a life insurance
  as investment income; the **half-income treatment (*Halbeinkünfteverfahren*)** applies where the
  contract has run at least **twelve years** and the benefit is paid after the policyholder's **62nd**
  birthday (the "12/62 rule"); a **BMF-Schreiben of 1 October 2009, IV C 1 - S 2252/07/0001** is the
  administrative guidance; and for contracts concluded from **1 April 2009** a
  ***Mindesttodesfallschutz*** of **50 %** of the *Beitragssumme* is required for the favourable
  treatment to apply at all.
- **Why it matters here that this section does *not* apply.** § 20 Abs. 1 Nr. 6 taxes the
  *Erlebensfall* — the sum received on maturity or surrender — because that is where an
  *Unterschiedsbetrag* can arise. **A pure death benefit is not taxed under it**: the payment is made
  on death, to a third party, and is not investment income of the policyholder. So the
  *Todesfallleistung* of a *Risikolebensversicherung* is **free of Einkommensteuer**, and the tax
  question moves entirely to the *Erbschaftsteuer* [R15]. **The non-application to a death benefit is
  asserted from knowledge and is `[unverified]`** (gap 16) — though it is corroborated indirectly by
  the *Mindesttodesfallschutz* rule itself, which exists precisely because the legislator wanted to
  stop savings contracts dressing themselves as death covers to escape this section.
- ***Sonderausgaben*.** Premiums for a *Risikolebensversicherung* fall among the *sonstige
  Vorsorgeaufwendungen* deductible under § 10 Abs. 1 Nr. 3a EStG, **within an annual ceiling that
  is in practice already exhausted by the taxpayer's health and long-term-care contributions**, so
  the effective deduction for most taxpayers is **nil**. Both the classification and the practical
  consequence are `[unverified]`, and the ceiling figures are **not stated** in this file (gap 17).

### R15 — ErbStG §§ 3, 15, 16, 19 — the *Erbschaftsteuer* treatment of the death benefit

- Publisher: Bundesministerium der Justiz (Erbschaftsteuer- und Schenkungsteuergesetz)
- URL: `https://www.gesetze-im-internet.de/erbstg_1974/` `[unverified]`; the per-section forms are
  **not established**
- Content, asserted from knowledge and `[unverified]` in every particular:
  - **§ 3 Abs. 1 Nr. 4** brings within *Erwerb von Todes wegen* every asset acquired by a third party
    **on the death of the deceased by virtue of a contract concluded by the deceased**. A
    *Todesfallleistung* paid to a *Bezugsberechtigter* under a policy the deceased took out **on his
    own life and paid for himself** is the textbook case. **It is therefore subject to
    *Erbschaftsteuer*.**
  - **§ 15** sorts beneficiaries into three *Steuerklassen* by relationship: I (spouse, registered
    partner, children, grandchildren, parents on death), II (siblings, nieces and nephews,
    step-parents, parents-in-law, divorced spouse), III (**everyone else, including an unmarried
    partner**).
  - **§ 16** sets the *Freibeträge*: **500 000 €** for a spouse or registered partner, **400 000 €**
    per child, **200 000 €** per grandchild, **100 000 €** for parents and grandparents on a death
    acquisition, **20 000 €** for *Steuerklasse* II, and **20 000 €** for *Steuerklasse* III. These
    are the figures the author believes to be current; **every one of them is `[unverified]`** and is
    carried in the delib product documents as a `[std]` illustration rather than as a citation
    (gap 18).
  - **§ 19** sets the rate by *Steuerklasse* and by the size of the taxable acquisition, on a banded
    scale that begins at **7 %** in class I and at **30 %** in class III, rising with the band.
    Again `[unverified]`.
- **The arithmetic that drives German term-life contracting.** Take the sum insured this file's
  representative design uses, **300 000 €**. Paid to a **spouse**, the 500 000 € allowance absorbs
  it entirely and the tax is nil. Paid to an **unmarried partner**, the allowance is 20 000 €, the
  taxable acquisition is 280 000 €, and *Steuerklasse* III applies from 30 % — a tax bill on the
  order of **84 000 €**, or **28 % of the sum insured**. That single comparison is why the
  *Über-Kreuz-Versicherung* exists (mechanic 14), and it is the strongest reason a German term-life
  product specification must model the contracting structure and not only the cash flows. **The
  arithmetic is arithmetic; the allowance and the rate it uses are `[unverified]` [R15].**

### R16 — VersStG § 4 — *Versicherungsteuer* exemption for life insurance

- Publisher: Bundesministerium der Justiz (Versicherungsteuergesetz)
- URL: `https://www.gesetze-im-internet.de/verststg_1996/__4.html` `[unverified]`
- Content, asserted from knowledge and `[unverified]`: the *Versicherungsteuer* — the German
  insurance premium tax, at a general rate of 19 % for most non-life lines — **does not apply to
  life insurance**. A German RLV premium is therefore quoted and billed **without insurance premium
  tax**, unlike a French *cotisation* quoted "TTC" or a UK IPT-bearing premium. The delib model
  carries **no premium-tax line** for this product, and the reason is recorded here so that a reader
  does not conclude the line was forgotten. The exemption's precise statutory location is
  `[unverified]` (gap 19).

### R17 — VVG-InfoV, and the PRIIP boundary for a pure protection product

- Publisher: Bundesministerium der Justiz (VVG-Informationspflichtenverordnung); European
  Parliament and Council (PRIIPs Regulation)
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`. The sibling research recorded
  § 2 VVG-InfoV as the source of the pre-contractual information duties and of the *Effektivkosten*
  disclosure [inherited: `kapitallebensversicherung.md` R9]
- **Inherited corroboration** [`kapitallebensversicherung.md` R9]: § 2 VVG-InfoV lists the
  information an insurer must give before conclusion of a life contract, and the *Effektivkosten*
  (reduction-in-yield) disclosure sits in that machinery.
- **The boundary this product sits on, asserted and `[unverified]`.** A ***Basisinformationsblatt***
  (PRIIP-KID) is required for a **packaged retail investment product** — one whose return is exposed
  to the performance of reference values or assets. A **pure *Risikolebensversicherung* has no
  investment component and is therefore not a PRIIP**, so no *Basisinformationsblatt* is produced for
  it; the applicable pre-contractual summary is the ***Produktinformationsblatt*** under the
  VVG-InfoV [S2]. **Two consequences for delib**: (i) the brief's expectation of finding
  *Basisinformationsblätter* for this product is misplaced, and the gaps register records that
  rather than pretending the documents were merely unreachable; (ii) there is **no *Effektivkosten*
  figure for a term product**, because a reduction in yield presupposes a yield, and an RLV has
  none. The absence of a published cost ratio is therefore **structural, not a research failure** —
  and it is a large part of why German term-life charge levels are invisible (gap 8).

### R18 — GDV, *Die deutsche Lebensversicherung in Zahlen* and the *Risikoversicherung* statistics

- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V.
- URL: **not established** for the term-assurance breakdown. The sibling research located the GDV
  statistics landing page and the ten-year *Neugeschäft und Bestand* series [inherited:
  `kapitallebensversicherung.md` R20, R21]
- **Inherited corroboration** [`kapitallebensversicherung.md` R20, R21]: the GDV publishes an annual
  statistical volume and a ten-year new-business and in-force series for German life insurers, broken
  down by product family; from it the sibling research took a whole-market ***Stornoquote* of
  2,72 % for 2024 and 2,56 % for 2023** on the main GDV measure, which counts contracts terminated
  early, surrendered or converted to *beitragsfrei* as a percentage of the *Bestand*, and a second
  measure of **1,2 % for 2024** counting contracts and covering surrenders and other early
  terminations. **The two measures are not reconcilable from the evidence and both are recorded**
  [inherited: `kapitallebensversicherung.md` R20, gap 10 there].
- **What is *not* established, and it is the whole of what this product needed**: the size of the
  German *Risikoversicherung* segment — number of contracts in force, new business per year, premium
  income, aggregate *versicherte Summe*, average sum insured, average premium — and any
  *Risikoversicherung*-specific lapse rate. **No such figure appears anywhere in this file** (gap 13).
  The whole-market *Stornoquote* is **not** used as a term-life lapse assumption: a term contract's
  lapse profile is dominated by its first three durations and by the absence of any surrender value
  to lose, both of which push it above a book average heavily weighted by long-dated savings
  contracts. The delib lapse assumption is `[std]` (mechanic 17).

### R19 — BaFin supervisory material on life insurance conduct and product governance

- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- URLs: **not established** for any term-life-specific item. The sibling research located BaFin's
  **Merkblatt 01/2023 (VA)** *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden
  Lebensversicherungsprodukten*, published **May 2023**, and the *Risiken im Fokus 2026* item on the
  cost of *kapitalbildende* products [inherited: `kapitallebensversicherung.md` R17, R18]
- **Inherited corroboration and its limit** [`kapitallebensversicherung.md` R17]: the *Merkblatt*'s
  subject is expressly ***kapitalbildende*** life products — those with a capital-formation element —
  and its central concern is that costs be justified by customer value. **A pure
  *Risikolebensversicherung* is outside its stated subject matter.** Recorded here so that a reader
  does not import an endowment-conduct standard into a term product; the supervisory literature
  specific to German term assurance was **not located** (gap 14).

### R20 — Rating and analysis houses on German term-life tariff design

- Publisher: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA — see S17, which is the same corpus
  seen from the product side
- URL: **not established**
- Content: recorded as the reference class for two market-design facts that no statute supplies —
  that the ***Brutto*/*Zahlbeitrag* spread is a rated criterion**, and that the
  ***Nachversicherungsgarantie* event list, caps and age limits are rated criteria**. Both
  `[unverified]` [S17]. **No rating, no criterion weight and no observed distribution is asserted.**

### R21 — HGB § 341f and RechVersV — statutory reserving for a term contract

- Publisher: Bundesministerium der Justiz (Handelsgesetzbuch; Verordnung über die Rechnungslegung von
  Versicherungsunternehmen)
- URL: `https://www.gesetze-im-internet.de/hgb/__341f.html` `[unverified]`
- Content, asserted from knowledge and `[unverified]`: § 341f requires the *Deckungsrückstellung* to
  be computed prospectively on the bases used to determine the premium, with a prudent margin, and
  to include a provision for future administration costs where the premium-paying period is shorter
  than the cover period. The RechVersV governs the presentation. Whether a **negative** individual
  *Deckungsrückstellung* arising from *Zillmerung* must be floored at zero for balance-sheet purposes
  — the *Nullstellung* question — is **not established** and matters for this product specifically,
  because a *gezillmerte* term contract sits below zero for a long stretch (gap 11).
- The delib library's posture, stated once in every product: **the models publish gross
  best-estimate-style liability cash flows, undiscounted. Discounting, the *Deckungsrückstellung*,
  Solvency II technical provisions and the SCR are referenced, never specified.** R21 is a pointer
  for a reader who needs the reserving layer, not an input to any model.

### R22 — Solvency II and the German prudential layer

- Publisher: European Insurance and Occupational Pensions Authority; BaFin
- URL: **not established**
- Content: recorded as a pointer only, on the same posture as R21. Nothing product-specific for
  German term assurance was located, and **no capital, risk-margin or stress figure appears anywhere
  in the delib `risikolebensversicherung` documents.**

### R23 — German case law on *vorvertragliche Anzeigepflicht* and *Selbsttötung* in life insurance

- Publisher: Bundesgerichtshof and the *Oberlandesgerichte*
- URL: **not established.** No decision is cited by date or file number anywhere in this file, and
  **none is invented**
- Content: recorded as a known reference class rather than as a source. The German litigation that
  actually decides term-life claims clusters on two questions: whether the applicant's answers to the
  *Gesundheitsfragen* were complete and whether the insurer complied with the § 19 Abs. 5 warning
  requirement [R4]; and whether a *Selbsttötung* inside the three-year window was committed in a
  state excluding free will [R1]. The sibling research located BGH authority on adjacent life-
  insurance questions — the *Stornoabzug* *Bezifferung* requirement and the post-LVRG
  *Bewertungsreserven* judgment of **20 January 2021, IV ZR 318/19** [inherited:
  `kapitallebensversicherung.md` R22, R23] — which establishes that the court decides this area
  regularly, and establishes nothing about term assurance. **No holding is asserted** (gap 20).

---
