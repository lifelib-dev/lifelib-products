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
