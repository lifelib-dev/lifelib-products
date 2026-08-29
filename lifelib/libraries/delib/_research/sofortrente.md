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
