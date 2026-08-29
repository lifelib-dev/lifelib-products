# Sofortbeginnende private Rentenversicherung — research notes (Germany)

Research notes for the German **immediate payout annuity** — *sofortbeginnende private
Rentenversicherung*, commonly *Sofortrente*: a single *Einmalbeitrag* (single premium) is paid
once, and the insurer pays a *Leibrente* (life annuity) for as long as the annuitant lives,
beginning immediately. The annuity is *monatlich vorschüssig* (monthly in advance) in the market's
standard form, is guaranteed at a level struck at inception on the tariff bases, and is topped up
by a declared, non-guaranteed *Überschussrente*. The contract normally carries a
*Rentengarantiezeit* (guarantee period), may carry a *Kapital-* or *Beitragsrückgewähr* (refund of
the unconsumed single premium on death) and may carry a *Hinterbliebenenrente* (survivor's
annuity). It is a Schicht-3 (third-layer, unsubsidised private) contract, and its distinguishing
commercial feature is that its payments are taxed only on the *Ertragsanteil* — the small
statutory income fraction of § 22 EStG — which makes it the most lightly taxed regular income a
German private investor can buy.

**In scope.** The single-life and joint-life **payout** annuity bought with a single premium by an
individual outside any state subsidy: the determination of the guaranteed annuity from the
*Einmalbeitrag*; the *Rentengarantiezeit*; the death-benefit options (*Kapitalrückgewähr /
Beitragsrückgewähr*, *Hinterbliebenenrente* and its *Anwartschaft*); the payment frequency and
timing; the short-*Aufschubzeit* variant in which the annuity is bought now and starts a few years
later; the *Überschussbeteiligung* in the *Rentenbezugsphase* and its four *Überschussverwendung*
forms; the *Rechnungsgrundlagen* (DAV 2004 R, the *Höchstrechnungszins*); the impossibility of
surrender once the *Rentenbezug* has begun; and the *Ertragsanteil* taxation.

**Out of scope, and named here so the boundary is explicit.**

- **The accumulation phase of a deferred annuity.** *Klassische aufgeschobene private
  Rentenversicherung* is a separate delib product (`klassische_rentenversicherung`) with its own
  research file, and everything about premium accumulation, the *Deckungskapital* recursion, the
  *Rückkaufswert*, *Beitragsfreistellung* and the *Kapitalwahlrecht* belongs there. The two
  products meet at exactly one point and it is an important one: the *aktueller Rentenfaktor* a
  deferred contract converts at is, at two carriers, explicitly **the tariff the insurer is then
  writing for immediately beginning annuities** [S3] [S7]. The immediate annuity is therefore the
  *pricing primitive* of the deferred one, and this file is where that primitive is documented.
- **Schicht 1 (*Basisrente* / Rürup) and Schicht 2 (*Riester-Rente*, *betriebliche
  Altersversorgung*).** Both are separate delib products or outside the library entirely. Their
  payout phases are annuities on the same machinery, but their tax treatment is completely
  different — full *nachgelagerte Besteuerung* under § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. aa
  EStG for Schicht 1 and § 22 Nr. 5 EStG for Schicht 2, against the *Ertragsanteil* here — and
  Schicht 1 and Schicht 2 annuities may not be commuted, refunded to an estate or (in Schicht 1)
  even bequeathed except to a spouse. The *Sofortrente* is the only one of the three in which the
  policyholder owns the capital outright until the moment it is annuitised.
- **Fondsgebundene** (unit-linked) and **indexgebundene** payout annuities, including the
  *fondsgebundene Sofortrente* in which the annuity is expressed in *Renten-Bezugseinheiten*
  (annuity units) that rise and fall with a fund. Separate delib products
  (`fondsgebundene_rentenversicherung`, `indexpolice`). The classic general-account
  (*konventionell*) form is what is specified here.
- **Sterbegeldversicherung**, **Pflegerentenversicherung** (delib `pflegerentenversicherung`),
  **Gruppenversicherung**, **private Krankenversicherung**, and institutional pension-risk
  transfer, including *Rentnergesellschaften* and buy-outs.
- The **gesetzliche Rentenversicherung** (state pension) and the **Deutsche Rentenversicherung**'s
  own *Ausgleichszahlungen*. Referenced only where the consumer literature compares them.

These notes are the citation ground truth for the delib `sofortrente` product documents: source
ids **S1..S15** and **R1..R25** below are **frozen — never renumber**. Unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which ids are absent and why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

Read this section before reading any citation in this file, because a delib citation is a weaker
object than a citation in the four sister libraries and the difference is stated rather than
glossed.

**No document listed in this file was retrieved.** Direct HTTP egress from this build environment
is blocked by an organisation network policy. `WebFetch` and `curl` are refused with HTTP 403 at
the egress gateway for every host outside a short package-registry allowlist. The hosts that
matter for this product were all tried across the delib build and all refused:
`gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`,
`destatis.de`, `dejure.org`, `eur-lex.europa.eu`, `de.wikipedia.org`, and every insurer host named
below (`zurich.de`, `cosmosdirekt.de`, `nuernberger.de`, `debeka.de`, `allianz.de`,
`konzern-versicherungskammer.de`). **Nothing in this file rests on a document anyone opened.**

**A second, independent limit applied to this product.** The session's `WebSearch` budget — 200
calls, shared across the parallel delib researchers — was **already exhausted before work on this
product began**. Not one search was run for the *Sofortrente*. The brief anticipated thirty to
eighty German-language queries covering *Rentenfaktor* levels from comparison portals, insurer
*Versicherungsbedingungen*, *Produktinformationsblätter*, *Basisinformationsblätter*, the
*Überschussbeteiligung* declarations, Stiftung Warentest's *Sofortrente* tests and twenty named
carriers. **Zero were available.** This is gap 1 and everything in this file follows from it.

What that means, exactly, and it is applied without exception below:

1. **Every source entry records `Retrieved: no — egress blocked; no search corroboration (session
   search budget exhausted)`.** Nothing here is marked retrieved, and nothing here is marked
   corroborated by a search run for this product. Where an entry *does* carry corroboration, it is
   corroboration recorded by a **sibling delib research file** whose searches ran earlier in the
   same session — principally `_research/klassische_rentenversicherung.md`, which shares this
   product's *Rechnungsgrundlagen*, its surplus chassis and, at two carriers, its tariff. Those
   entries say so in terms and name the sibling file's own source id. That is a real and
   traceable provenance chain, and it is still one step weaker than a retrieval.
2. **No document reference number, no URL, no edition, no page count and no publication date was
   guessed.** Where a URL was recorded by a sibling file from a search result, it is reproduced and
   attributed. Where a URL is the obvious canonical `gesetze-im-internet.de` form of a statutory
   provision, it is given and marked `[unverified]`. Everywhere else the entry reads
   `URL: not established`.
3. **No verbatim quotation is invented.** Where a short phrase appears in quotation marks below it
   is a phrase a sibling file recorded from a search summary, and it is attributed to that summary
   rather than to the document.
4. **`[unverified]` is used generously and keeps its normal meaning.** Every specific paragraph
   number, effective date, monetary amount, percentage, tariff level and market figure that no
   search result confirmed carries the tag. It is not applied to the general shape of a
   well-established mechanic — that would drown the signal — but the moment a claim becomes
   *specific and numeric* it carries either a corroborated source or the tag.
5. **Uncertain numbers are `[std]` parameters, not citations.** This is the most consequential
   rule for this product, because the *Sofortrente* is a product whose entire commercial character
   is a number — the euros per month per 100 000 € of *Einmalbeitrag* — and that number could not
   be established at any carrier for any year. Rather than guess it, section 4 below **constructs**
   it from annuity mathematics on an explicitly stated proxy basis, prints the construction so a
   reader can reproduce it with a calculator, and labels every resulting figure `[std]`. A `[std]`
   number with a printed derivation is honest. A fabricated `[S6]` number is not.

**Prefer to say less, precisely, than more, loosely.** Where the corpus establishes a mechanic and
not its level — which is the normal case here — the mechanic is written long and the level is a
`[std]` parameter with an argued range. The gaps register at the end is not a formality; it is a
substantial part of this file's value, and a reader who needs a market figure should start there.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss. The vocabulary this product needs, beyond the shared annuity vocabulary of
`_research/klassische_rentenversicherung.md`:

| Term | Gloss |
|---|---|
| *Sofortrente* / *sofort beginnende Rentenversicherung* | immediate annuity: annuity payments begin at once, or after a short deferment |
| *Einmalbeitrag* | single premium: the whole consideration, paid once at inception |
| *Rentenbeginn* | annuity commencement date; for this product, at or shortly after inception |
| *Rentenbezugsphase* / *Rentenbezug* | the payout phase — for this product, the whole of the contract |
| *Leibrente* | life annuity: payable for as long as the annuitant lives, and not one day longer |
| *versicherte Person* | the life on which the annuity depends; not necessarily the *Versicherungsnehmer* |
| *Versicherungsnehmer* | the policyholder: the party to the contract, who pays and who elects |
| *garantierte Rente* | the guaranteed annuity, computed on the tariff bases alone |
| *Überschussrente* | the surplus-financed increment to the annuity in payment; declared, not guaranteed |
| *Gesamtrente* | the sum of the two, the amount actually paid in a given year |
| *Rentenfaktor* | annuity factor: monthly annuity per 10 000 € of capital. For an immediate annuity the market more often quotes *Rente je 100 000 € Einmalbeitrag* |
| *Rentenhöhe* | the level of the annuity — the quantity a *Sofortrente* is bought and compared on |
| *vorschüssig* / *nachschüssig* | payable in advance / in arrears, at the start or the end of the payment period |
| *Rentengarantiezeit* | annuity guarantee period: payments continue to survivors if the annuitant dies inside it |
| *Restgarantiezeit* | the unexpired part of the *Rentengarantiezeit* at the date of death |
| *Kapitalrückgewähr* / *Beitragsrückgewähr* | refund on death of the *Einmalbeitrag* less the annuity instalments already paid |
| *Hinterbliebenenrente* | survivor's annuity, payable to a named second life after the annuitant's death |
| *Anwartschaft* | the contingent entitlement of the survivor while the annuitant is alive |
| *mitversicherte Person* | the second life whose survival triggers the *Hinterbliebenenrente* |
| *Aufschubzeit* | deferment period: the gap between payment of the *Einmalbeitrag* and *Rentenbeginn* |
| *Überschussbeteiligung* | profit participation: the policyholder's share of the insurer's surplus |
| *Überschussverwendung* | the *use* the declared surplus is put to — the four payout-phase forms of section 9 |
| *konstante Überschussrente* | the form in which the total annuity is set once and intended to stay level |
| *steigende* / *dynamische Überschussrente* | the form in which the annuity starts low and rises each year with declared surplus |
| *teildynamische Überschussrente* | the intermediate form: part of the surplus taken up front, part left to finance increases |
| *Bonusrente* | surplus applied as a paid-up increment of annuity, permanently added to the payment |
| *Zinsüberschuss* / *Risikoüberschuss* / *Kostenüberschuss* | the interest, mortality and expense components of surplus |
| *Bewertungsreserven* | unrealised capital gains; policyholders participate under § 153 Abs. 3 VVG |
| *Rechnungszins* | the technical interest rate in the tariff |
| *Höchstrechnungszins* (*Garantiezins*) | the statutory maximum *Rechnungszins* for new business, set in the *Deckungsrückstellungsverordnung* |
| *Deckungsrückstellung* | the statutory reserve for the contract; for an annuity in payment, the reserve for the remaining payments |
| *Zinszusatzreserve* | the additional interest reserve German insurers built against legacy guarantees |
| *Rechnungsgrundlagen* | the tariff bases: mortality table, interest rate, expense loadings |
| *Generationentafel* | generation table: mortality by year of birth, with the future trend inside the table |
| *Trendfunktion* | the mortality-improvement function of a generation table |
| *Sicherheitszuschlag* | the prudential margin added to the best-estimate basis to make a first-order basis |
| *Rechnungsgrundlagen erster / zweiter Ordnung* | first-order (prudent, tariff) and second-order (best-estimate) bases |
| *Altersverschiebung* | age shift: the device by which one table is adapted to another cohort |
| *Ertragsanteil* | the taxable fraction of a private life annuity under § 22 EStG |
| *Bankauszahlplan* / *Entnahmeplan* | bank payout plan: a capital drawdown with a fixed term, the *Sofortrente*'s standard comparator |
| *Langlebigkeitsrisiko* | longevity risk — the risk the annuity is written to remove from the annuitant |
| *Kapitalverzehr* | the consumption of capital: what a payout plan does and an annuity does not |
| *Rentenanpassung* | the annual adjustment of the annuity in payment following a new declaration |
| *Standmitteilung* | the annual statement the insurer must send |
| *Sicherungsvermögen* | the ring-fenced general account backing guarantees |
| *Schicht 1 / 2 / 3* | the three layers of German retirement provision; this product is Schicht 3 |

---

## Primary sources

Fifteen entries. Only three are *documents whose existence and identity a search result actually
returned* — [S2], [S4] and [S6], all three recorded by the sibling delib research file
`_research/klassische_rentenversicherung.md` while search was still available, and all three
carrying a URL that a search returned. The remaining twelve are **known references**: document
classes and carriers that exist and are the right kind of thing to cite for this product, recorded
so that a later build with a working retrieval channel knows exactly what to fetch and in what
order. They carry no URL unless one was recorded by a sibling file, and nothing quantitative is
cited from them. The order below is the order in which they should be fetched.

### S1 — GDV, "Musterbedingungen" service index, and the immediate-annuity model conditions
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: publisher index page listing the association's *Musterbedingungen* (model general
  policy conditions) — the industry's shared drafting template, which individual insurers adopt,
  adapt or ignore
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` — recorded by the sibling file
  `_research/klassische_rentenversicherung.md` [S3 there] from a search result
- Retrieved: no — egress blocked; no search corroboration in this session (budget exhausted);
  URL and taxonomy carried over from the sibling file's search record
- Content, and a **negative finding that matters**. The sibling file established from the index
  that the GDV maintains model conditions for: (a) *Rentenversicherung mit aufgeschobener
  Rentenzahlung* — the deferred annuity; (b) *Rentenversicherung gemäß § 10 Abs. 1 Nr. 2 Buchst. b
  Doppelbuchst. aa EStG* — the *Basisrente*; (c) a *fondsgebundene* Riester wrapper under the
  *Altersvorsorgeverträge-Zertifizierungsgesetz*; (d) a non-unit-linked variant of the same,
  carrying "Stand: 21.07.2025"; and (e) the *Hinterbliebenenrenten-Zusatzversicherung* rider
  [S9]. **No model condition set for a *Rentenversicherung mit sofort beginnender Rentenzahlung*
  appears in that list.** Whether the GDV maintains one under a title the index listing did not
  surface, or whether the market drafts immediate-annuity conditions from the deferred-annuity
  template with the *Aufschubzeit* set to zero, **was not established** — gap 3. The second
  reading is the more likely on the evidence of [S4], whose title places the immediate annuity in
  the same AVB series as the deferred one at the same carrier, but it is not established and must
  not be asserted downstream.
- The GDV's standing disclaimer applies to the whole family: "Diese Bedingungen sind
  unverbindlich" — the wording is non-binding and its use optional [S1, via the sibling file's S2].
  Model conditions establish the **shape** of German wording, never an insurer's obligation.

### S2 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — the consolidated pre-contractual pack a German life insurer
  must supply under the VVG-Informationspflichtenverordnung [R17]: general information, the
  *Allgemeine Versicherungsbedingungen* (AVB), the special conditions for riders and options, and
  the tax notes. Document code **521331402 2501**.
- URL:
  `https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf`
  — returned by a search recorded in the sibling file [S16 there]
- Retrieved: no — egress blocked; the document's existence, title, document code, vintage and URL
  are corroborated by the sibling file's search record; **no clause content was established from
  it**
- Content: **the single most important document to fetch for this product, and the only one whose
  identity is corroborated.** It is the immediate-annuity member of Zurich Deutscher Herold's
  *Verbraucherinformation für Konventionelle Versicherungen* series, the same series whose deferred
  annuity editions of 01/2021, 01/2022 and 01/2026 the sibling file records [S3]. "Konventionell"
  is the German market's word for the general-account, non-unit-linked chassis, so the title alone
  establishes that this is the classic product and not a *fondsgebundene Sofortrente*. Its
  deferred-annuity siblings are structured as: *allgemeine Informationen*; the AVB; *Besondere
  Bedingungen* for each option; *allgemeine steuerliche Hinweise*; and the rider conditions [S3].
  The immediate-annuity edition should be expected to carry the same structure with the
  accumulation-phase material removed and the *Rentengarantiezeit*, *Kapitalrückgewähr* and
  *Hinterbliebenenrente* options in its place — **an expectation, not a finding**.
- Vintage matters here. **Fassung 01/2022** places this edition inside the **0,25 %
  *Höchstrechnungszins*** regime [R7], one year before the increase to 1,00 % took effect. Any
  *Rentenhöhe* it contains is a 0,25 %-era figure and is not comparable with a current quotation.
  Whether a 2025 or 2026 edition exists **was not established**; the deferred-annuity sibling
  reached **Fassung 01/2026** [S3], so one probably does.

### S3 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung", Fassung 01/2026
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation*, deferred annuity, document code **521331262 2601**
- URL:
  `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf`
  — recorded by the sibling file [S4 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record, reproduced
  with attribution
- Content, and **why a deferred-annuity document is a primary source for the payout product**.
  Two of the three payout-phase facts the delib corpus establishes at clause level come from this
  document:
  - **The two-factor rule at *Rentenbeginn*.** The guaranteed *Rentenfaktor* is described as
    carefully calculated, and **at the start of annuity payments a second *Rentenfaktor* is
    compared with it, the higher of the two being guaranteed for the annuity payment period**. The
    "second factor" is the carrier's then-current immediate-annuity tariff [S7] — that is,
    **this product**. The deferred contract's upside is priced off the *Sofortrente* rate card.
  - ***Bewertungsreserven* participation continues in the *Rentenbezug*.** The transition to
    annuity payment is described as a key point for participation in *Bewertungsreserven*, and
    policyholders **also participate during the annuity payment period**, in accordance with the
    applicable VVG and supervisory provisions; the summary states that **§ 153 Abs. 3 VVG currently
    provides for equal (*hälftige*) participation** [R3].
  This is the only clause-level evidence in the whole delib corpus that surplus participation does
  not stop at *Rentenbeginn*, and it is load-bearing for section 9.

### S4 — NÜRNBERGER Lebensversicherung AG, AVB for the *Rentenversicherung mit sofort beginnender Rentenzahlung*, publisher document id `gn331303_p`
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender
  Rentenzahlung* — an insurer's own AVB for exactly the product in scope
- URL: `https://www.nuernberger.de/medien/4allportal/gn331303_p.pdf` — the **document id
  `gn331303_p` was returned by a search** and is recorded by the sibling file [S9 there] as a
  sibling of tariff NIR3301's AVB; the URL is the carrier's established `4allportal` path form
  applied to that id and is `[unverified]` as a working address
- Retrieved: no — egress blocked; no search corroboration in this session; **document id
  corroborated, URL constructed, no clause content established**
- Content: **the only insurer AVB in the corpus whose title names this product.** The sibling
  file's search returned three members of the same NÜRNBERGER AVB family from one result set:
  `gn331451_p` (deferred, *mit Rentengarantiezeit*, tariff NIR3301) [S5], `gn331530_p`
  (*fondsgebunden*) and `gn331303_p` (*mit sofort beginnender Rentenzahlung*) — this document.
  That the three sit in one numbered family establishes what [S1] could not: German insurers draft
  the immediate annuity as **a member of the same AVB series as the deferred annuity**, not as a
  separate product line. Nothing inside it was established. It is the first document a later build
  should fetch after [S2].

### S5 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301", document id `gn331451_p`
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**
- URL: `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` — recorded by the sibling file
  [S9 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record
- Content: recorded here for two reasons. First, it is the **only document in the delib corpus
  whose title itself names the *Rentengarantiezeit***, which establishes the guarantee period as a
  **tariff-level design feature carried in the product name**, not merely a rider bolted on — and
  the guarantee period is a payout-phase mechanic, so the evidence belongs here as much as in the
  deferred file. Second, its search summary established that **the contract value used for
  annuitisation includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum
  guaranteed contract value stated in the general contract data** — which is the deferred
  contract's version of the *Einmalbeitrag* this product starts from. No paragraph numbering was
  established.

### S6 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", tariff LA 904 A
- Publisher: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland
- Doc type: *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**
- URL:
  `https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf`
  — recorded by the sibling file [S8 there] from a search result
- Retrieved: no — egress blocked; content below is the sibling file's search record, reproduced
  with attribution
- Content: **the most quantitatively load-bearing document in the whole delib annuity corpus, and
  the only one that names a conversion basis.** A search summary returned the clause in terms:
  **"The annuity factor determined at the beginning of the contract is calculated on the basis of
  a recognised mortality table (currently DAV 2004 R) and an underlying interest rate (currently 0
  percent p.a.)."** For this product that sentence establishes three things:
  1. the mortality basis of a German annuity tariff is **DAV 2004 R** [R10];
  2. the interest basis of a *guaranteed* annuity factor can be set **below** the statutory
     *Höchstrechnungszins* — at this carrier, at this vintage, at **0 % p.a.** — so the guarantee
     is priced as though the insurer will earn nothing on the annuity fund. That is the
     *Sicherheitszuschlag* made concrete on the interest side;
  3. the factor is fixed **at inception**, which for a *Sofortrente* means it is fixed once and
     never revisited, because inception and *Rentenbeginn* are the same date.
- The same summary returned the carrier's standard surplus disclaimer: **"the amount of profit
  sharing depends on many influences which are unpredictable and only limitedly controllable by
  the company, with the most important influencing factor being capital-market developments."**
- **The vintage of LA 904 A was not established**, and the clause is explicitly time-stamped by
  its own word *currently*. Siblings in the house numbering (LA 1204 A and LA 1201 A, both 11.22;
  LA 1005 A; LA 1311 A; LA 1100 A; LA 1081 A) place LA 904 as the oldest number in the series, so
  the "0 percent p.a." reading may belong to the 0,25 %-*Höchstrechnungszins* era rather than to
  the current one. See gap 6.

### S7 — Allianz Lebensversicherungs-AG — the immediate-annuity tariff statement, and the Allianz immediate-annuity product documents
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: (a) the "Vorsorgekonzept KomfortDynamik" product page, recorded by the sibling file
  [S13 there] from a search result; (b) Allianz's own *Sofortrente* product documents —
  *Produktinformationsblatt*, AVB, *Basisinformationsblatt* — **not established**
- URL: (a) `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`, recorded by the
  sibling file; (b) not established
- Retrieved: no — egress blocked; (a) is the sibling file's search record; (b) is a known
  reference only
- Content: (a) contains the second, independent statement of the fact that makes this product the
  pricing primitive of the deferred one. On the *Rentenfaktor* applied at *Rentenbeginn*: **"the
  calculation bases at *Rentenbeginn* … relate to the interest rate and mortality table that the
  company uses at that time for immediately beginning annuities."** Read with [S3]'s two-factor
  rule, the pair establishes the market convention: the *aktueller Rentenfaktor* of any deferred
  German annuity **is** the carrier's current *Sofortrente* tariff, so the *Sofortrente* rate card
  is the price of the deferred contract's upside. The same page establishes that the
  ***Rentengarantiezeit* "can be set to a minimum"** — a policyholder-selectable parameter with a
  contractual floor.
- (b) Allianz is the largest German life writer and certainly sells an immediate annuity against
  *Einmalbeitrag*; the market name commonly given for it is *Allianz SofortRente* `[unverified]`,
  and no document, tariff code, envelope or rate was established. Fetching Allianz's
  *Produktinformationsblatt* and *Basisinformationsblatt* for that product is the second-highest
  value action a later build can take, after [S2].

### S8 — Debeka Lebensversicherungsverein a. G. — AVB series B LV, and the "Privatrente" product page
- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: AVB in the house **B LV** series (e.g. **B LV 85**, and the more recent **B LV 100**
  of 01.07.2026 and **B LV 101** of 01.01.2025, both in the *betriebliche Altersversorgung*
  folder and out of scope), plus the insurer's *Privatrente* product page
- URLs: `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf`
  and `https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html` — both
  recorded by the sibling file [S11] [S12 there] from search results
- Retrieved: no — egress blocked; content below is the sibling file's search record
- Content: two facts carry over to the payout product. First, Debeka's own definition of the
  accumulation quantity — **the *Deckungskapital* is the sum of the contributions accumulated at
  the *Rechnungszins*, insofar as those contributions are not required for risk and expense
  cover** — which for a single-premium immediate annuity degenerates to "the *Einmalbeitrag* less
  the acquisition and administration loadings", the quantity section 2 calls the *Nettoeinmal-
  beitrag*. Second, the tax statement from the product page: **if a lifelong monthly annuity is
  chosen, only part of the payout is taxed — the comparatively low *Ertragsanteil*, depending on
  age at *Rentenbeginn*** [R13]. **Whether Debeka writes a stand-alone *Sofortrente* against
  *Einmalbeitrag* was not established**; the carrier withdrew its classic deferred tariff in 2016
  [R21], which says nothing either way about the payout product.

### S9 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung"
- Publisher: GDV
- Doc type: *Musterbedingungen* for the **survivor's-annuity rider**
- URL:
  `https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf`
  — recorded by the sibling file [S10 there] from a search result. Note that the URL slug names
  the **deferred** annuity; whether a separate model set exists for the immediate annuity's
  survivor's rider was **not established**.
- Retrieved: no — egress blocked; no clause content established
- Content: establishes the single structural fact this file needs about the *Hinterbliebenenrente*:
  **the German market treats the survivor's annuity as a *Zusatzversicherung* — a rider with its
  own condition set, attached to the base contract rather than being a benefit of it.** That has a
  direct modelling consequence (section 7): the survivor's annuity is a **separate module, off in
  a reference implementation's base run**, with its own *Anwartschaft* period, its own insured life
  and its own reserve, rather than a term in the main annuity's benefit formula.

### S10 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher: Konzern Versicherungskammer, the Bavarian public-sector insurance group; the `BL_`
  path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity
- Doc type: the annual ***Überschussverteilung*** document — the instrument by which a German life
  insurer publishes its declared *Überschussanteilsätze* for a calendar year, separately for each
  tariff generation and separately for the accumulation and payout phases
- URL: `https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf`
  — recorded by the sibling file [S15 there] from a search result
- Retrieved: no — egress blocked; **the title and the 2026 vintage are corroborated; nothing
  inside the document was established**
- Content: this document class is **the** primary source for every surplus rate a projection of
  this product needs — the *laufende Verzinsung*, the *Grundüberschussanteil*, the
  *Zinsüberschussanteil* on the *Deckungsrückstellung* of annuities in payment, the
  *Schlussüberschuss* where one applies, and the *Überschussrentensatz* that converts the declared
  surplus into euros of monthly annuity. **No rate, no percentage and no component split was
  established from it, for any carrier, for any year.** That is gap 4, and it is why every surplus
  parameter downstream is `[std]` and labelled insurer-discretionary.

### S11 — *Produktinformationsblatt* (PIB) for a sofort beginnende Rentenversicherung — document class
- Publisher: each insurer, individually
- Doc type: the short pre-contractual product summary required by German insurance-distribution
  law [R17]. For an annuity it is the document that states, on one or two pages, the
  *Einmalbeitrag*, the *garantierte Rente*, the *Gesamtrente* including the currently declared
  surplus, the *Rentengarantiezeit*, the death benefit, and the costs
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: **known reference only.** This is the document class that would settle almost every
  quantitative gap in this file at a stroke, because a PIB for a *Sofortrente* prints the
  guaranteed and total annuity for a stated *Einmalbeitrag* and a stated age — the exact figure
  section 4 has to construct. **Not one PIB for this product was located.** A later build should
  fetch three or four across carriers of different types (a large stock company, a mutual, a
  direct writer, a public-sector insurer) before writing any *Rentenhöhe* into the product-spec.

### S12 — *Basisinformationsblatt* (PRIIP-KID) for a sofort beginnende Rentenversicherung — document class
- Publisher: each insurer, individually
- Doc type: the three-page key information document required by the PRIIPs Regulation for
  insurance-based investment products, with the standard sections *Um welche Art von Produkt
  handelt es sich?*, *Welche Risiken bestehen und was könnte ich im Gegenzug dafür bekommen?*
  (with the *Risikoindikator* and four performance scenarios), *Was geschieht, wenn … nicht in der
  Lage ist, die Auszahlung vorzunehmen?*, *Welche Kosten entstehen?* (with the
  *Reduction in Yield* / *Renditeminderung* figures) and *Wie lange sollte ich die Anlage halten …?*
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration
- Content: **known reference only, with a scope question attached.** Whether a classic
  *Sofortrente* falls inside PRIIPs at all was **not established** — an immediate annuity with a
  guaranteed payment and a discretionary surplus is an insurance-based investment product on the
  usual reading, but the *Sofortrente*'s payout-only character and the absence of a surrender value
  after *Rentenbeginn* [R1] make the "recommended holding period" and "what you might get back"
  sections awkward, and some carriers may rely on an exemption. If a BIB does exist for the
  product it is the **only** public document that would give a cost figure in the standardised
  *Renditeminderung* form, which is the single most useful charge datum a model could have. See
  gap 8.

### S13 — Carriers writing the product, recorded without documents
- Publishers: Allianz [S7]; R+V; Debeka [S8]; Generali and its direct arm CosmosDirekt [S6];
  Dialog; HDI; Alte Leipziger; LV 1871; Continentale and its direct arm Europa; NÜRNBERGER [S4]
  [S5]; Swiss Life; Zurich Deutscher Herold [S2] [S3]; ERGO; AXA; Barmenia; Hannoversche;
  Württembergische; Gothaer; Stuttgarter [S14]; Volkswohl Bund; Baloise; Universa; DEVK; Signal
  Iduna; Provinzial; HUK-Coburg; Konzern Versicherungskammer [S10]; Mecklenburgische [S14]
- Doc type: none — carrier names only
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Content: **a list of where to look, and nothing more.** The *Sofortrente* is a commodity product
  in Germany: the great majority of the carriers above write one, comparison portals rank them on
  the single dimension of *Rentenhöhe*, and the spread between the best and the worst quotation for
  identical terms is the market's own measure of pricing variation. **No carrier's product name,
  tariff code, envelope, rate or document was established here**, and this file therefore contains
  **no insurer-level quantitative comparison at all** — which is the honest statement of gap 2,
  and the reason section 18's "observed variation" table is a structural table rather than a
  numeric one. Naming a carrier in this entry asserts only that it is a German life insurer of the
  right kind; it does not assert that it sells this product today.

### S14 — Stuttgarter Lebensversicherung a. G. and Mecklenburgische Lebensversicherungs-AG — further pre-contractual packs
- Publishers: Stuttgarter Lebensversicherung a. G.; Mecklenburgische Lebensversicherungs-AG
- Doc types: "Allgemeine Informationen zu einem Altersversorgungssystem" (Stuttgarter);
  "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (Mecklenburgische,
  product "Rente flex", title truncated in the search record)
- URLs: `https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833`
  and `https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf`
  — both recorded by the sibling file [S18] [S14 there] from search results
- Retrieved: no — egress blocked; no clause content established from either
- Content: recorded to establish that ***Verbraucherinformation*, *Vertragsinformationen* and
  *Allgemeine Informationen* are three names for the same pre-contractual pack**, so a later build
  searching for one should search for all three. The Stuttgarter URL's `?t=1604038997833` query
  parameter is a millisecond timestamp corresponding to **October/November 2020**, which dates that
  file. The Mecklenburgische title is truncated after "mit flexiblem", so its distinguishing
  feature — most plausibly a flexible *Rentenbeginn*, which would make it a near neighbour of the
  *Aufschubzeit* variant of section 3 — is **not established**.

### S15 — The annual *Standmitteilung* and *Rentenanpassungsmitteilung* in the *Rentenbezug* — document class
- Publisher: each insurer; the GDV publishes a *Muster-Standmitteilung*
- Doc type: the annual statement a German life insurer must send. For a contract in the
  *Rentenbezug* it reports the *garantierte Rente*, the current *Überschussrente*, the resulting
  *Gesamtrente*, and — where the *Überschussverwendung* is a rising form — the amount by which the
  annuity has been increased with effect from the anniversary
- URL: not established for the payout form. The sibling file records the GDV *Muster-Standmitteilung*
  for the **endowment** at `_research/kapitallebensversicherung.md` [S2 there]
- Retrieved: no — egress blocked; no search corroboration
- Content: **known reference only.** This document class is the direct evidence of what a
  *Rentenanpassung* looks like in practice — whether the annuity moved up, stayed flat or moved
  down after a declaration, and by how much — which is exactly the question section 9's "the
  constant form is not actually constant" turns on. **No specimen was located and no anniversary
  adjustment was established, at any carrier, for any year.**

---

## Regulatory and actuarial references

Twenty-five entries. The statutory ones carry the canonical `gesetze-im-internet.de` address where
that form is unambiguous, marked `[unverified]` because no search in this session returned it; the
professional and market ones carry a URL only where a sibling delib file recorded one. **None was
retrieved.** Where a provision's *content* is stated below, it is stated as what the provision
provides, in this file's own words, and the paragraph number carries `[unverified]` unless a
sibling file's search corroborated it.

### R1 — VVG § 168, *Kündigung des Versicherungsnehmers* — and the rule that ends surrender at *Rentenbeginn*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: **the provision that decides the single most important modelling question about this
  product.** § 168 VVG governs the policyholder's right to terminate a life insurance contract:
  a contract with recurring premiums may be terminated at the end of the current insurance period,
  and a single-premium contract on stated conditions. The paragraph that matters here is
  **§ 168 Abs. 3 VVG**, which provides that **in the case of a *Rentenversicherung* without a
  *Kapitalwahlrecht* the right of termination exists only up to the start of the annuity payments**
  `[unverified]` — after *Rentenbeginn* there is no right to terminate and therefore no
  *Rückkaufswert* to pay. For a *Sofortrente*, whose *Rentenbeginn* is at or within weeks of
  inception, the practical effect is that **the contract is irrevocable from the outset**: the
  *Einmalbeitrag* is gone, and the only thing the policyholder holds thereafter is the annuity
  itself and whatever death benefit was bought with it.
- The paragraph number, the exact scope of the "*ohne Kapitalwahlrecht*" qualifier, and the
  treatment of a contract that carries a *Kapitalwahlrecht* exercisable during a short
  *Aufschubzeit* are all `[unverified]` here. The **substance** — no surrender in the
  *Rentenbezug* — is not seriously in doubt: it is the uniform statement of the German consumer
  literature [R21] [R23], it is the economic precondition for a life annuity to be writable at all
  (a surrenderable annuity would be selected against by every annuitant in poor health), and it is
  the exact rule French law states in the same words for the same reason. See gap 9.

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — recorded by the sibling file
  [R1 there] as returned by a search
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the general surrender-value provision. It obliges the insurer to pay the *Rückkaufswert*
  where a contract is terminated by the policyholder; for unit-linked contracts the value is the
  *Zeitwert* computed by recognised actuarial rules; paragraphs 3 to 5 carry the calculation rules
  and the rule spreading *Abschluss- und Vertriebskosten* over the first five years `[unverified]`.
  **Recorded here for its boundary, not its content**: § 169 is displaced for this product by
  § 168 Abs. 3 [R1] the moment the *Rentenbezug* begins. A delib `Sofort_DE_S` model therefore
  publishes **no surrender-value cells and no lapse decrement in the payout phase**, and the
  absence is a specification, not an omission.

### R3 — VVG § 153, *Überschussbeteiligung*, and § 153 Abs. 3, *Beteiligung an den Bewertungsreserven*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — recorded by the sibling files
  [R4 in the RV file, R1 in the KLV file] as returned by searches
- Retrieved: no — egress blocked; content is the sibling files' search record
- Content: the statutory right to participate in surplus. The policyholder is entitled to a share
  of the *Überschuss* and of the *Bewertungsreserven* unless participation is excluded by express
  agreement; the surplus must be determined by a method appropriate under recognised actuarial
  principles; and **§ 153 Abs. 3 currently provides for equal (*hälftige*) participation in the
  *Bewertungsreserven***, allocated at the times the contract specifies [S3]. Two consequences for
  this product: participation is a **statutory right, not a marketing feature**, and it **does not
  stop at *Rentenbeginn*** — [S3] states in terms that policyholders also participate during the
  annuity payment period. The level of participation is entirely at the insurer's discretion within
  the statutory minimum [R15], which is why every surplus figure downstream is `[std]`.

### R4 — VVG § 163, *Anpassung der Prämie oder der Vertragsbestimmungen*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; established at commentary level only, from the sibling file
  [R3, R17 there]
- Content: the statutory channel through which a German life insurer may change a contract term
  after conclusion — the successor to the contractual *Treuhänderklausel*. The sibling file
  establishes from consumer commentary that **the *Treuhänderklausel* is used only in older
  contracts and that today a guaranteed *Rentenfaktor* can be changed only on the basis of
  § 163 VVG**, and that the **Landgericht Köln** held **the low-interest phase not to be a
  sufficient ground, because it is entrepreneurial risk that cannot be passed to policyholders**
  (case reference, date and parties **not established**). For this product the provision is close
  to inert: the guaranteed annuity of a *Sofortrente* is struck once, at inception, on bases that
  are then fixed for life, and no adjustment channel that survives judicial scrutiny reaches it.
  A delib model treats the *garantierte Rente* as **immutable** and records § 163 as a model risk.

### R5 — VVG § 165, *Prämienfreie Versicherung*, and § 166, *Kündigung des Versicherers*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — recorded by the sibling file
  [R2 there] as returned by a search
- Retrieved: no — egress blocked
- Content: § 165 gives the policyholder of a contract with recurring premiums the right to convert
  it to a premium-free contract, the reduced benefit being derived from the surrender value on the
  premium basis and tabulated per insurance year, subject to a *Mindestversicherungsleistung*
  threshold. **Recorded purely for its boundary**: a *Sofortrente* is bought with a single
  *Einmalbeitrag*, so there is no future premium to cease and **§ 165 has no application to this
  product at all**. A reference implementation carries **no `Beitragsfreistellung` decrement**, and
  that is a specification rather than a simplification.

### R6 — VVG §§ 150, 159, 160 — *versicherte Person*, *Bezugsberechtigung*, *Auslegung der Bezugsberechtigung*
- Publisher: Bundesministerium der Justiz / juris
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__150.html`,
  `.../__159.html`, `.../__160.html` — canonical forms, all `[unverified]`
- Retrieved: no — egress blocked; no search corroboration
- Content: the provisions that make the *Rentengarantiezeit* and the *Hinterbliebenenrente*
  work as a matter of contract law. § 150 distinguishes the *Versicherungsnehmer* from the
  *versicherte Person* and requires the insured person's written consent where a life other than
  the policyholder's own is insured for a benefit above a threshold; § 159 gives the policyholder
  the right to designate a *Bezugsberechtigter* (beneficiary), revocably or irrevocably; § 160
  supplies default construction rules where several beneficiaries are named or a designation
  fails. All three are `[unverified]` as to paragraph number and content. They matter here because
  the payments made *after* the annuitant's death under a *Rentengarantiezeit* or a
  *Kapitalrückgewähr* go to a **designated beneficiary**, not automatically to the estate, and the
  designation is a live contractual element that a policyholder may change. A model treats the
  beneficiary as a pass-through and the payment as a liability of the same contract.

### R7 — Deckungsrückstellungsverordnung (DeckRV) § 2 — the *Höchstrechnungszins*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/deckrv/__2.html` — recorded by the sibling file
  [R7 there] as returned by a search
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the statutory maximum technical interest rate for new German life business. Established
  points: the rate was **0,25 %** before 2025 and is **1,00 % from 1 January 2025**, and the 2025
  increase was **the first increase since 1994** — every earlier move having been downwards. The
  DAV recommended **1,0 % for 2026 as well** [R8]. **The intermediate sequence — 4 %, 3,25 %,
  2,75 %, 2,25 %, 1,75 %, 1,25 %, 0,90 %, 0,25 % — and every effective date in it is
  `[unverified]` here**; a model point carrying a legacy *Rechnungszins* must cite the delib
  cross-product reference library rather than this file.
- **Why the rate is the whole product.** For a *Sofortrente* the *Höchstrechnungszins* is not a
  background parameter; it is close to being the price. The annuity is the reciprocal of an
  annuity value, and the annuity value at these ages and durations is dominated by the discount
  rate. Section 4 computes the sensitivity on a stated proxy basis and finds that moving the
  interest basis from 0,25 % to 1,00 % raises the annuity at age 65 by about **10 %** `[std]` —
  a change of the same order as a decade of mortality improvement, delivered in one legislative
  step on 1 January 2025.

### R8 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Cologne
- URL: not established; the sibling file [R8, R9 there] records the two press items by title —
  "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0
  Prozent" and "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins
  2025"
- Retrieved: no — egress blocked; titles corroborated by the sibling file's search record
- Content: the profession's own recommendations, which the *Bundesministerium der Finanzen*
  converts into the DeckRV figure. Establishes that **1,0 % was recommended for 2026** as well as
  applying from 2025, so a contract written in 2026 is on the same interest basis as one written
  in 2025 — which matters for a *Sofortrente*, where the tariff vintage and the contract vintage
  are the same thing. The DAV's methodology, the *Referenzzins* it derives the recommendation
  from, and any figure inside the releases are **not established**.

### R9 — GDV media information on the *Höchstrechnungszins* increase
- Publisher: GDV; and HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- URL: not established; titles recorded by the sibling files [R10, R11 there; R16 in the KLV file]
- Retrieved: no — egress blocked
- Content: the industry's framing of the 2025 increase as "eine angemessene Reaktion auf gestiegene
  Zinsen" and a carrier's own customer-facing note of the same change. Corroborates the **1 January
  2025** effective date and the direction of travel. **No figure for the effect on annuity levels
  was established from either**, which is the figure this product most needs; see gap 5.

### R10 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen"
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: *DAV-Richtlinie* — the profession's derivation guideline for the annuity table
- URL: not established; the sibling file [R12 there] records the document and its 2023 reissue
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: **the mortality basis of this product.** Established from the sibling file:
  - DAV 2004 R is a ***Generationentafel***: mortality is given per **birth cohort**, and the
    expected future improvement is **inside the table**, not applied on top of it.
  - Its **component structure** is: a **base table of second order**; a **base table of first
    order**; a **mortality trend of second order**; a **mortality trend of first order**; and an
    **age adjustment (*Altersverschiebung*) with a base table**. The trend is therefore a named,
    separately-parameterised object — the *Trendfunktion* — and it exists in both a best-estimate
    and a prudent version.
  - **First-order probabilities are used for premiums and reserves and carry safety margins
    relative to the second-order ("realistic") probabilities, in order to assess the risk
    prudently**; the **second-order base tables represent the best estimate of period mortality in
    1999 for insured lives, as three-dimensional selection tables**. For an annuity, "prudent"
    means **lower** mortality than best estimate: the first-order basis assumes annuitants live
    longer, which raises the annuity value and lowers the annuity bought by a given
    *Einmalbeitrag*.
  - **Dates**: in use since **June 2004**, intended for new business from **2005**, the DAV
    document dated **22 February 2005**; the derivation guideline was **reissued on 28 June 2023**.
    That the profession was still maintaining DAV 2004 R in 2023 — nineteen years after first use,
    twenty-four years after its 1999 base year — is itself the evidence that **no successor annuity
    table has displaced it**.
- **The table is not public and delib does not redistribute it.** It is the property of the DAV.
  delib cites it by name, ships a `[std]` proxy anchored so its own worked example reproduces
  exactly, and states the anchor in the model's `Data` docstring. A replacement must preserve the
  **generational structure** (a `q(x, cohort)` surface, not a period table), the **first-order
  margin over second order**, and the **age-adjustment convention**.

### R11 — DAV 2004 R-Bestand and the *Rentenbestandstafel* RBx
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: no — egress blocked; the pairing is recorded by the sibling file [R14 there] from a
  2004 presentation titled "DAV 2004 R und RBx"
- Content: the corpus establishes **that a companion in-force table exists and nothing more.**
  DAV 2004 R is the **new-business** table; the ***Bestand*** variant is the table for the
  **existing annuity book**, reflecting the different composition and selection history of
  annuities already in payment. **The distinction between "DAV 2004 R" and "DAV 2004 R-Bestand"
  is established only as a naming pairing**; the difference in level, in trend, in age range or in
  application rule was **not established** and nothing about it may be asserted downstream — see
  gap 12. For a *Sofortrente* the distinction is nevertheless conceptually central: a contract is
  priced on the new-business table at inception and then, for the whole of its long life, sits in
  the *Bestand* to which the other table applies.

### R12 — Contemporaneous expositions of DAV 2004 R
- Publishers: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik (DGVFM); General
  Reinsurance AG; the *qx-Club* actuarial seminar series
- URL: not established; the sibling file [R14 there] records presentations of **16 August 2004**,
  **14 September 2004** and a reinsurer's exposition of **27 October 2004**
- Retrieved: no — egress blocked
- Content: the profession's contemporaneous explanation of the table at the moment of its
  introduction, which is where the *Sicherheitszuschlag* structure and the trend construction were
  set out for practitioners. **No content was established** beyond the fact of the presentations
  and their dates. Recorded because these are the documents a later build should fetch to
  substantiate anything specific about the first-order margin, which this file can describe only
  qualitatively.

### R13 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb — the *Ertragsanteil* table
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — recorded by the sibling file [R5
  there] as **returned directly by a search**
- Retrieved: no — egress blocked; the general content below is the sibling file's search record;
  the table values in section 15 are from general knowledge and are `[unverified]`
- Content, as established by the sibling file:
  - Payments from private annuity contracts, and from life contracts converted into a classic
    monthly *Leibrente*, are taxed on the ***Ertragsanteil*** basis.
  - **Only the "Ertrag des Rentenrechts"** — the interest component contained in the annuity from
    the beginning of the payout phase — **is subject to tax**. The return-of-capital element is not
    income at all.
  - **The *Ertragsanteil* is determined by the annuitant's age at *Rentenbeginn*.** The earlier the
    annuity begins, the longer its expected duration, and **the higher the taxable fraction**.
  - **For an annuity commencing at age 65 the *Ertragsanteil* is 18 % of the annuity.** This is
    the only value of the statutory table that any delib search corroborated.
  - The statutory address usually given for the table — **§ 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst.
    bb EStG** — was **not** confirmed by any search summary and is `[unverified]`.
- The fraction is **fixed for life at the annuity's commencement age** and does not fall as the
  annuitant ages, which is the feature that makes a deferred start economically attractive
  (section 3) and is easy to model wrongly.

### R14 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalabfindung* regime, and its boundary
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — recorded by the sibling file [R6
  there]
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the regime that taxes a **lump sum** from a life or annuity contract. The
  *Halbeinkünfteverfahren* — half the *Ertrag* taxable, half exempt — applies where the "12/62
  rule" is met: **the contract must have run at least 12 years and the payment must occur after
  completion of the 62nd year of life**, and the contract must be one in which the capital option
  **cannot be exercised before 12 years** from conclusion. **The method applies only to lump-sum
  payments and to multiple capital withdrawals under a payout plan; it does not apply to monthly
  annuity payments.** Contracts concluded before 1 January 2005 retain the earlier treatment.
- **Recorded here for its boundary, and the boundary is sharp.** A *Sofortrente* bought at, say,
  age 65 has by construction **not** run twelve years when its first payment falls due, so § 20
  Abs. 1 Nr. 6 could never apply to it favourably even if it paid a lump sum. It pays no lump sum
  in any event. **The whole of a *Sofortrente*'s cash flow is taxed under § 22 [R13] and none of it
  under § 20** — which is precisely the tax arbitrage the product is sold on, and the reason a
  *Sofortrente* is compared with a *Bankauszahlplan* whose interest is taxed in full at the
  *Abgeltungsteuer* rate (section 17).

### R15 — Mindestzuführungsverordnung (MindZV)
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/mindzv/` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; recorded at existence level by the sibling file [R6 in the KLV
  file]
- Content: the regulation fixing the **minimum share of each surplus source that must be credited
  to policyholders** — the floor beneath the insurer's discretion under § 153 VVG [R3]. It
  operates separately on the *Kapitalanlageergebnis* (investment result), the *Risikoergebnis*
  (mortality and biometric result) and the *übriges Ergebnis* (expense and other result), and it
  permits deductions for the *Sicherungsbedarf* arising from legacy guarantees [R16]. **No
  percentage in the regulation was established by any delib search** — the commonly quoted
  90 % / 90 % / 50 % structure is `[unverified]` and does not appear here as a figure. For this
  product MindZV matters because **the annuitant's *Risikoergebnis* is a longevity result**: when
  annuitants die faster than the first-order table assumed, the *Risikoüberschuss* is positive and
  a minimum share of it must flow back into the *Überschussrente*.

### R16 — VAG §§ 138–140 — *Überschussbeteiligung*, *Sicherungsbedarf*, and the *Zinszusatzreserve*
- Publisher: Bundesministerium der Justiz / juris
- URL: `https://www.gesetze-im-internet.de/vag_2016/__139.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; recorded at existence level by the sibling file [R8 in the KLV
  file]
- Content: the supervisory side of the surplus rules — the *Rückstellung für
  Beitragsrückerstattung* (RfB), the conditions under which it may be drawn down, and the
  *Sicherungsbedarf* deduction that let German insurers withhold *Bewertungsreserven* from
  maturing and surrendered contracts during the low-interest years. The ***Zinszusatzreserve***
  — the additional reserve built against legacy guarantees on a *Referenzzins* mechanism — belongs
  to the same complex. **Nothing specific was established**: not the paragraph numbers, not the
  *Referenzzins* formula, not the ZZR's size in any year, not whether it is now being released.
  It is recorded because a *Sofortrente*'s *Überschussrente* is paid out of the same RfB that the
  ZZR competes with, so the reserve's release profile is a first-order driver of the surplus a
  cohort of annuitants will actually receive — and it is entirely `[unverified]` here.

### R17 — VVG-Informationspflichtenverordnung (VVG-InfoV), and the PRIIPs Regulation
- Publisher: Bundesministerium der Justiz / juris; European Union
- URLs: `https://www.gesetze-im-internet.de/vvg-infov/` — canonical form, `[unverified]`; the
  PRIIPs Regulation (Regulation (EU) No 1286/2014) `[unverified]` as to number
- Retrieved: no — egress blocked; the VVG-InfoV *Effektivkosten* point is recorded at existence
  level by the sibling file [R9 in the KLV file]
- Content: the two disclosure regimes that generate [S11] and [S12]. VVG-InfoV § 2 lists the
  pre-contractual information a German life insurer must supply and is the source of the
  *Verbraucherinformation* document class [S2] [S3] [S14]; it also carries the ***Effektivkosten***
  disclosure — a reduction-in-yield figure — for products in scope. The PRIIPs Regulation generates
  the *Basisinformationsblatt* [S12] with its *Risikoindikator*, four performance scenarios and
  *Renditeminderung* cost figures, and the DAV maintains a standard method for category 4 products
  (the sibling KLV file records an *Ergebnisbericht* of **1 July 2025** [R27 there]). **Whether
  either regime's cost disclosure applies to a payout-only *Sofortrente* was not established** —
  gap 8 — and **no *Effektivkosten* or *Renditeminderung* figure for this product was established
  at any carrier.**

### R18 — BaFin material on life-insurance product oversight
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin)
- URL: not established; the sibling KLV file [R17, R18, R19 there] records **Merkblatt 01/2023 (VA)
  *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten***,
  the *Risiken im Fokus 2026* section on "Kosten von kapitalbildenden Lebensversicherungen", and
  *Fachartikel* including "Wenn Lebensversicherungen zu viel kosten" (2022) and "Kundennutzen im
  Fokus" (2024)
- Retrieved: no — egress blocked
- Content: the supervisor's *Wohlverhaltensaufsicht* (conduct supervision) of life products —
  value-for-money expectations, cost scrutiny and the *Kundennutzen* framing. **All of the recorded
  material is addressed to *kapitalbildende* (capital-forming) products, i.e. the accumulation
  side.** Whether BaFin has published anything specific to payout annuities, and in particular
  whether it scrutinises *Rentenhöhe* or *Überschussrente* declarations for value, **was not
  established**. Recorded so a later build knows the supervisor's material exists and is
  accumulation-shaped.

### R19 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher: GDV, under its consumer brand *Die Versicherer*
- URL: `https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750`
  — recorded by the sibling file [R21 there] from a search result
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: the industry association's own consumer account of the payout options of a private
  annuity, and part of the result set from which the payout-phase surplus taxonomy of section 9
  was established. It is the closest thing in the delib corpus to an authoritative German-industry
  statement of the annuity-versus-lump-sum choice. **No notice period, no rate and no envelope was
  established from it.**

### R20 — Franke und Bornberg, "Altersvorsorge: Überschüsse im Rentenbezug — Teil 1: Die Qual der Wahl", and "Was bedeutet der Rentenfaktor und wie hoch ist er?"
- Publisher: Franke und Bornberg GmbH, Hannover — independent product-rating house
- URLs: `https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl`
  and `https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022` —
  recorded by the sibling file [R19 there] from search results
- Retrieved: no — egress blocked; content is the sibling file's search record
- Content: **the professional source behind section 9.** The first title is explicitly about
  ***Überschüsse im Rentenbezug*** — surplus in the payout phase — which is the exact subject of
  this product, and it is titled "Teil 1" of a series, so at least one further part exists and was
  not located. It is the rating house's treatment of the choice between the *Überschussverwendung*
  forms. The second is the rating house's *Rentenfaktor* article, whose slug dates it to the
  **2021/2022** window. **Neither returned a level, a range or a table**: the very question the
  second title asks — "und wie hoch ist er?" — was not answered by anything any delib search
  returned. That is gap 5, the largest quantitative hole in this file.

### R21 — Consumer-organisation material on the *Sofortrente*
- Publishers: Finanztip Verbraucherinformation gemeinnützige GmbH; Stiftung Warentest
  (*Finanztest*); the *Verbraucherzentralen*
- URLs: `https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/`
  and `https://www.finanztip.de/lebensversicherung-versteuern/` — recorded by the sibling file
  [R20 there] from search results. **Finanztip's, Stiftung Warentest's and the Verbraucherzentrale's
  *Sofortrente*-specific pages were not located and no URL for them is given.**
- Retrieved: no — egress blocked
- Content: what the sibling file established from the two located Finanztip pages is the surplus
  taxonomy used in section 9 — the *konstant* / *teildynamisch* / *volldynamisch* division, and the
  observation that **under the constant system the annuity can still fall, because if the insurer
  earns less than expected the surplus-financed part is reduced** — together with the 12/62 rule
  [R14]. **Stiftung Warentest's periodic *Sofortrente* comparison is the single most valuable
  unlocated document for this product**: it is the German market's standard published table of
  guaranteed and total monthly annuities per 100 000 € by carrier, and it would settle gaps 2, 5
  and 7 together. Its existence is asserted here from general knowledge and is `[unverified]`; no
  issue, date, price point or ranking is claimed.

### R22 — Assekurata, "Marktstudie Überschussbeteiligungen und Garantien"
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH, Cologne
- URL: not established; the sibling KLV file [R25 there] records the **24. Marktstudie
  "Überschussbeteiligungen und Garantien 2026"**
- Retrieved: no — egress blocked; the title and 2026 edition number are the sibling file's search
  record
- Content: the German market's annual survey of declared surplus rates — the document that
  aggregates what [S10] publishes carrier by carrier. That it has reached a **24th edition** dates
  the series to the early 2000s and establishes it as the market's standard reference. **No rate,
  no average, no range and no payout-phase breakdown was established from it.** For this product
  the relevant series would be the *laufende Verzinsung* and, more specifically, the surplus
  credited to annuities in payment, which the study is likely to report separately from the
  accumulation figure. Locating it is the third-highest-value action for a later build, after
  [S2] and Stiftung Warentest [R21].

### R23 — Comparison-portal and broker cluster specific to the *Sofortrente*
- Publishers: `vergleich-sofortrente.de`; `lifefinance.de`; Verivox; CHECK24; and the broader
  German broker-blog cluster the sibling file records as [R24] there —
  `versicherungenmitkopf.de`, `fragfina.de`, `gn-finanzpartner.de`, `finanzkueche.de`,
  `compeon.de`, `financedoor.de`, `versicherung-vergleiche.de`, LV 1871's and NÜRNBERGER's own
  wiki pages, `vr.de`, `ruv.de`
- URLs: the two product-specific hosts `vergleich-sofortrente.de` and `lifefinance.de` were
  returned inside the sibling file's [R24] publisher list; **no individual page URL for either was
  recorded**, and none is given here
- Retrieved: no — egress blocked; no search corroboration in this session
- Content: **the class of source that would supply the price points this file lacks, and did not.**
  A German *Sofortrente* comparison portal exists precisely to rank carriers by monthly annuity per
  100 000 € for a stated age and set of options, and `vergleich-sofortrente.de` is by its domain
  name dedicated to exactly that. **Nothing from it was established.** What the wider cluster did
  establish, through the sibling file, is the definitional material this file relies on: the
  *Rentenfaktor* arithmetic and the guaranteed/current distinction; the *Rentengarantiezeit*
  mechanics, durations and cost illustration (section 5); the *Zinsüberschuss* hurdle-rate
  definition; the *Bonusrente* mechanic; and the *Ertragsanteil*. Every fact drawn from the cluster
  below is corroborated by at least two of its members in the sibling file's record, and none of
  it is a price.

### R24 — The unisex rule: CJEU *Test-Achats* and its German application
- Publisher: Court of Justice of the European Union; the German *Allgemeines
  Gleichbehandlungsgesetz* (AGG) and the VVG's implementing provisions
- URL: not established
- Retrieved: no — egress blocked; **no delib search touched this topic at all**
- Content: **`[unverified]` in both directions and recorded as a known reference only.** The
  established German market position is that life and annuity tariffs written for new business
  from **21 December 2012** must be **unisex** — premiums and benefits may not differ by sex —
  while the actuarial tables the profession publishes, DAV 2004 R among them, are constructed
  **sex-distinctly**. Neither half of that sentence was corroborated by any delib search: no
  summary confirmed that DAV 2004 R is published by sex, and no search reached the CJEU judgment,
  its case number, or the German application date. The tension is real and this product is where
  it bites hardest — a *Sofortrente* is the purest longevity bet in the German market, female
  annuitants are materially longer-lived, and a unisex tariff on sex-distinct tables must
  therefore be struck on an assumed **portfolio sex mix**, which is a pricing assumption the
  insurer chooses and never publishes. The unisex rule belongs to the delib cross-product
  reference library `references/regulatory-and-actuarial-references.md` and must be cited from
  there, not from this file. See gap 13.

### R25 — GDV statistics on *Einmalbeiträge* and the German annuity market
- Publisher: GDV
- URL: not established; the sibling KLV file [R20, R21 there] records "Die deutsche
  Lebensversicherung in Zahlen 2024" and the statistical series "Neugeschäft und Bestand der
  Lebensversicherer für die letzten zehn Geschäftsjahre"
- Retrieved: no — egress blocked
- Content: the industry statistics that would size this product. The GDV series separates
  ***Einmalbeiträge*** from *laufende Beiträge* in new business, which is the split that would
  reveal how large single-premium annuity business is — but the *Einmalbeitrag* line aggregates
  *Sofortrenten* with single-premium endowments, bAV single contributions and *Zuzahlungen* into
  existing contracts, so even a retrieved figure would not isolate this product. **No figure of any
  kind was established.** There is therefore **no sourced number anywhere in this file for the
  size of the German *Sofortrente* market, the number of contracts in force, the average
  *Einmalbeitrag*, or the average age at purchase** — see gap 7.

---
