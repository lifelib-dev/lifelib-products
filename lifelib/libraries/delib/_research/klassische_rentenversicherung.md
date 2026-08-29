# Klassische aufgeschobene private Rentenversicherung — research notes (Germany)

Research notes for the German **classic deferred private annuity** — *klassische aufgeschobene
private Rentenversicherung*, the Schicht-3 (third-layer, unsubsidised private) contract in which
premiums accumulate in the *Deckungskapital* (policy reserve) of the insurer's general account at
the guaranteed *Rechnungszins* (technical interest rate) with *Überschussbeteiligung* (profit
participation), and in which the accumulated capital is converted at the *Rentenbeginn* (annuity
commencement date) into a lifelong *Leibrente* at a guaranteed *Rentenfaktor* (annuity factor), or
taken instead as a lump sum under the *Kapitalwahlrecht* (lump-sum option).

**In scope.** The single-life, deferred, general-account ("konventionell", "klassisch") private
annuity sold to individuals outside any state subsidy, against a level recurring premium or a
single premium, with a deferment period ending at a contractually fixed *Rentenbeginn*; its
accumulation-phase reserve mechanics; its death benefit before *Rentenbeginn*; the annuity
conversion at the *Rentenfaktor*; the payout-phase annuity and its surplus systems; and the
statutory options (*Rückkaufswert*, *Beitragsfreistellung*, *Kapitalwahlrecht*, *Zuzahlung*,
*Dynamik*).

**Out of scope, and named here so the boundary is explicit.**

- **Schicht 1 — Basisrente (Rürup)** and **Schicht 2 — Riester-Rente and betriebliche
  Altersversorgung (bAV)**. Both are separate delib products (`basisrente`, `riester_rente`) or
  outside the library entirely (bAV: Direktversicherung, Pensionskasse, Pensionsfonds,
  Unterstützungskasse, Direktzusage). The GDV publishes a *separate* model-condition set for the
  Basisrente [S3], and the R+V Pensionskasse AG publishes its own AVB for a *Pensionskasse*
  annuity against single premium under tariff 970 — a Schicht-2 vehicle, not this product. Neither
  is used as a source for Schicht-3 mechanics here.
- **Fondsgebundene Rentenversicherung** (unit-linked, delib `fondsgebundene_rentenversicherung`)
  and **indexgebundene / "Neue Klassik"** hybrids (delib `indexpolice`), referenced only where a
  document covers both and the classic mechanics show through the contrast — the *Rentenfaktor*
  literature is dominated by unit-linked material [R16] [R19] [R24], because in a unit-linked
  contract the *Rentenfaktor* is the **only** guarantee, and the DEVK wording [S19] is used solely
  for that contrast.
- **Sofortbeginnende Rentenversicherung** (immediate annuity, delib `sofortrente`). The payout
  phase of this product and the whole of that one are the same machinery; the Zurich *sofort
  beginnende Rentenversicherung* consumer information [S16] is recorded here because German
  insurers derive the *aktueller Rentenfaktor* of a deferred contract from the tariff they are
  then writing for immediate annuities [S13] [R23], which makes the immediate-annuity document the
  direct evidence for the deferred contract's conversion basis.
- **Kapitalbildende Lebensversicherung** (endowment, delib `kapitallebensversicherung`), which
  shares the entire *Überschussbeteiligung* and *Deckungskapital* / *Rückkaufswert* chassis; the
  difference is only what happens at the end of the accumulation phase. Shared-chassis facts are
  recorded here anyway so this file stands alone, but the endowment file is the primary home for
  the four surplus components.
- **Gruppenversicherung**, **private Krankenversicherung**, **Sterbegeldversicherung** and
  institutional pension-risk transfer.

These notes are the citation ground truth for the delib `klassische_rentenversicherung` product
documents: source ids **S1..S19** and **R1..R24** below are **frozen — never renumber**. Unused
ids are simply omitted downstream, leaving gaps, and `sources.md` records which ids are absent and
why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

**No document listed in this file was retrieved.** Direct HTTP egress from this build environment
is blocked by an organisation network policy. `WebFetch` and `curl` are refused with HTTP 403 at
the egress gateway for every host outside a short package-registry allowlist. The hosts that
matter for this product — `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `de.wikipedia.org`, and every insurer host named below
(`zurich.de`, `cosmosdirekt.de`, `nuernberger.de`, `debeka.de`, `allianz.de`) — are all refused.

The **only** research channel available was the `WebSearch` tool, which returns titles, URLs and
search-engine summaries. Everything in this file rests on those summaries. They are real evidence
and they do return substantive content — several of the most load-bearing facts below (the
CosmosDirekt conversion basis, the Zurich two-factor comparison, the § 165 VVG paid-up formula)
came back as near-verbatim renderings of the document's own sentences — but a search summary is a
*secondary summary*, never a retrieved document.

This changes exactly two things:

1. **Every source entry records `Retrieved: no — direct HTTP egress blocked in the build
   environment; established from search-result summaries`.** Nothing here is marked retrieved. No
   quotation is invented. Where a short phrase is given in quotation marks, it is a phrase the
   search summary itself returned, and it is attributed to the summary rather than to the
   document.
2. **`[unverified]` keeps its normal meaning** — a claim that no search result corroborated. It is
   not applied to everything. A fact that several independent search results agree on is not
`[unverified]`; a paragraph number, an effective date, a tariff level or a market figure that no
search result confirmed **is**.

Every URL below is one a search result actually returned, or the obvious canonical
`gesetze-im-internet.de` form of a statutory article that several legal-database mirrors returned
(for example `https://www.gesetze-im-internet.de/vvg_2008/__169.html` for § 169 VVG). **No URL, no
document reference number, no paragraph number and no figure in this file was guessed.** Where a
URL is not available it says `URL: not established`.

**A second, harder constraint applies to this file specifically.** The session's `WebSearch`
budget was shared across fourteen parallel researchers and was **exhausted after eighteen queries
on this product**. The brief anticipated thirty to eighty. The consequence is recorded in full in
the gaps register (gap 1) and it is the single most important caveat on everything below: whole
areas the brief asked for — current *Rentenfaktor* market levels, charge levels, entry-age and
premium envelopes, the 2025/2026 *Überschussbeteiligung* declarations, the *Kapitalwahlrecht*
notice period, the *Zuzahlung* mechanics, the unisex rule — are recorded as **gaps, not as
facts**. Nothing was written to fill them.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss. The vocabulary this product needs:

| Term | Gloss |
|---|---|
| *Aufschubzeit* / *Aufschubdauer* | deferment period, from inception to *Rentenbeginn* |
| *Rentenbeginn* | annuity commencement date; the contractual boundary between accumulation and payout |
| *Rentenbezugsphase* / *Rentenphase* | payout phase, the period over which the annuity is in payment |
| *Leibrente* | life annuity: payable for as long as the annuitant lives |
| *Deckungskapital* | the policy's accumulated reserve; the per-policy quantity the recursion rolls forward |
| *Rechnungszins* | technical interest rate used in the tariff; the rate at which the *Deckungskapital* is guaranteed to accumulate |
| *Höchstrechnungszins* (*Garantiezins*) | the statutory maximum *Rechnungszins* for new business, set in the *Deckungsrückstellungsverordnung* |
| *Sparbeitrag* / *Risikobeitrag* | the savings portion of the premium — what is left after the risk and expense charges — and the risk portion |
| *Überschussbeteiligung* | profit participation: the policyholder's share of the insurer's surplus |
| *Schlussüberschussanteil* | terminal bonus, paid at *Rentenbeginn* or on earlier exit |
| *Bewertungsreserven* | unrealised capital gains in the insurer's assets; policyholders participate under § 153(3) VVG |
| *verzinsliche Ansammlung* | the surplus system in which declared surpluses are credited to a side account and accumulate with interest |
| *Ansammlungsguthaben* | the balance of that side account |
| *Bonusrente* | the surplus system in which declared surpluses buy additional paid-up annuity |
| *Beitragsverrechnung* | the surplus system in which surpluses are set against the premium due |
| *Überschussrente* | the surplus-financed part of the annuity in payment, as against the *garantierte Rente* |
| *garantierte Rente* | the guaranteed annuity, computed on the tariff bases alone |
| *Rentenfaktor* | annuity factor: the monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *garantierter Rentenfaktor* | the factor guaranteed at inception on the tariff bases, a floor |
| *aktueller Rentenfaktor* | the factor the insurer is currently applying, recomputed on current bases |
| *Treuhänderklausel* | trustee clause: a conditions clause letting the insurer change contract terms with an independent trustee's approval |
| *Rentengarantiezeit* | annuity guarantee period: the annuity keeps being paid to survivors if the annuitant dies inside it |
| *Beitragsrückgewähr* | return of premiums as the death benefit |
| *Kapitalwahlrecht* / *Kapitalabfindung* | the policyholder's option to take the accumulated capital as a lump sum instead of the annuity, and the lump sum itself |
| *Rückkaufswert* | surrender value |
| *Stornoabzug* (*Rückkaufsabschlag*) | the surrender charge deducted from the computed surrender value |
| *Zillmerung* | the reserving method that front-loads acquisition costs against the reserve |
| *Beitragsfreistellung* | conversion to a premium-free (paid-up) contract |
| *beitragsfreie Versicherungsleistung* | the reduced benefit after *Beitragsfreistellung* |
| *Zuzahlung* | an ad-hoc additional single premium into an existing contract |
| *Dynamik* / *Anpassungsversicherung* | the automatic annual premium-and-benefit increase option |
| *Ratenzahlungszuschlag* | the loading for paying the annual premium in instalments |
| *Ertragsanteil* | the taxable fraction of a private life annuity under § 22 EStG |
| *Schicht 1 / 2 / 3* | the three layers of the German retirement-provision architecture; this product is Schicht 3 |
| *Rechnungsgrundlagen* | the tariff bases: mortality table, interest rate and expense loadings |
| *Sicherungsvermögen* | the ring-fenced general account backing guarantees |

---

## Primary sources

Nineteen primary product documents and product pages. Four families dominate: the **GDV model
conditions** [S1] [S2] [S3] [S10], the industry's shared drafting template and the closest thing
German life insurance has to a canonical wording; the **Zurich Deutscher Herold
consumer-information series** [S4]–[S7] [S16] [S17], the only insurer corpus here that publishes
the *same* deferred-annuity document across several vintages, so drafting continuity is visible;
the **CosmosDirekt AVB** [S8], the only document whose conversion basis a search summary returned
explicitly; and the **Debeka** documents [S11] [S12], which matter because Debeka is the market's
largest classic-guarantee life writer and because it withdrew this exact product from sale [R22].

### S1 — GDV, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung" (Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: *Musterbedingungen* — model general policy conditions for a deferred annuity contract;
  the association's template wording, which individual insurers adopt, adapt or ignore.
- URL: https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from
  search-result summaries.
- Content: the GDV's model condition set for exactly the product in scope — a *Rentenversicherung
  mit aufgeschobener Rentenzahlung* — whose family addresses **Beitragsrückgewähr** (return of
  premiums as the death benefit), **contract values**, **minimum guarantees**, and the
  **conditions under which the annuity is paid**. It appeared in the result set for two independent
  queries, which fixes it as the reference wording for the mechanics extracted below. **No
  paragraph numbering, no clause text and no page count were established** — gap 2.

### S2 — GDV, "02 GDV-Musterbedingung LV — Rentenversicherung mit aufgeschobener Rentenzahlung" (2021 edition)
- Publisher: GDV
- Doc type: *Musterbedingungen*, 2021 edition of the same wording as [S1], on the same GDV resource
  path (blob id 6294 in both cases, distinct content hashes — two editions of one family).
- URL: https://www.gdv.de/resource/blob/6294/cacd502172fab87ad8859d194d9352c8/02-gdv-musterbedingung-lv-rentenversicherung-mit-aufgeschobener-rentenzahlung-2021-data.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the search result's own title line for this document is **"Diese Bedingungen sind
  unverbindlich"** — the GDV's standing disclaimer that the wording is non-binding and its use
  purely optional. That governs how [S1] and [S2] may be used downstream: they establish the
  **shape** of the German market's wording, not any insurer's obligation. The file name dates the
  edition to **2021**, i.e. drafted under the 0,90 % *Höchstrechnungszins* regime and before the
  1,00 % regime of 2025 [R7] [R8].

### S3 — GDV, "Musterbedingungen" service index
- Publisher: GDV
- Doc type: publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: establishes that the GDV maintains model conditions across product lines and that
  **their use is non-binding and optional**. The index also fixes the **product taxonomy** used in
  the scope note: separate model conditions exist for (a) *Rentenversicherung mit aufgeschobener
  Rentenzahlung* — this product [S1] [S2]; (b) *Rentenversicherung gemäß § 10 Absatz 1 Nr. 2
  Buchstabe b Doppelbuchstabe aa EStG* — the **Basisrente (Alter)**; (c) a *fondsgebundene*
  Riester wrapper under the *Altersvorsorgeverträge-Zertifizierungsgesetz*; (d) a non-unit-linked
  variant of the same, whose search result carried the date **"Stand: 21.07.2025"**; and (e) the
  *Hinterbliebenenrenten-Zusatzversicherung* rider [S10]. The statutory reference in (b) was
  returned inside the GDV's own file name and is recorded only as this product's **boundary**: a
  Schicht-3 contract takes no § 10 deduction.

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung, Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)", Fassung 01/2026
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — the consolidated pre-contractual pack a German life insurer
  must supply: general information, the AVB, the special conditions for riders and options, and
  the tax notes. Document code **521331262 2601** appears in the search result's title line.
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the **current-vintage anchor document of this file**. It is a *Verbraucherinformation für
  Konventionelle Versicherungen* — "konventionell" being the German market's word for the
  general-account, non-unit-linked chassis. Its scope line covers **"Aufgeschobene
  Rentenversicherung — Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)"** in
  the **Fassung 01/2026**; the *Schicht 3* label is the insurer's own placement of the product and
  is the direct source for the scope note above. Its structure is: **allgemeine Informationen**;
  the **Allgemeine Versicherungsbedingungen**; **Besondere Bedingungen für die
  Anpassungsversicherung in der Rentenversicherung** — the *Dynamik* option, therefore a documented
  contractual option with its own condition set; **allgemeine steuerliche Hinweise**; and
  **Besondere Bedingungen für die Berufsunfähigkeits-Zusatzversicherung**. On the *Rentenfaktor*:
  the guaranteed factor is described as carefully calculated, and **at the start of annuity payments
  a second *Rentenfaktor* is compared with it, the higher of the two being guaranteed for the
  annuity payment period** — the single most important mechanic in the file (section 8). On
  *Bewertungsreserven*: **the transition to annuity payment is a key point for participation**, and
  policyholders **also participate during the annuity payment period**, in accordance with the
  applicable VVG and supervisory provisions; the summary states that **§ 153 Absatz 3 VVG currently
  provides for equal (hälftige) participation**.

### S5 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2021 — 44 pages
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation für Konventionelle Versicherungen*, deferred annuity, private
  provision. Document code **521331422 1507**; title line "Seite 1 von 44" — **44 pages**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/330202101_aufgeschobene-rentenversicherung-private-vorsorge_verbraucherinformationen_2021_01.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: described as containing **"Versicherungsbedingungen für die aufgeschobene
  Rentenversicherung (Konsortialversicherung) — Private Vorsorge und Rückdeckungsversicherung"**,
  with sections on **the contract partners, the scope of cover, the design options and the
  *Überschussbeteiligung***. Same product as [S4] five years earlier; the pairing of vintages
  establishes the wording as continuously maintained. One document in the same result set was
  reported to **discuss the guarantee amounts and how the benefits are calculated at the end of the
  deferment period** — the conversion mechanic — but the summary did not say which, so it is
  recorded without a pinpoint.

### S6 — Zurich Gruppe, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung (Konsortial)" — 46 pages
- Publisher: Zurich Gruppe Deutschland
- Doc type: *Verbraucherinformation*, consortium (*Konsortialversicherung*) edition. Document code
  **521331432 1507**; title line "Seite 1 von 46" — **46 pages**.
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/docs/privatkunden/vorsorge-und-vermoegen/existenzsicherung/231_zurich_gruppe_vi_aufgeschobene_rentenversicherung_konsortial.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the same product underwritten by a consortium rather than one carrier; two pages longer
  than [S5]. Establishes that one carrier issues the **same wording in more than one distribution
  wrapper** — a wrapper variation, not a liability variation.

### S7 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation*, deferred annuity. Document code **521331392 2501**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/220202101_aufgeschobene-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the third vintage. Its value is chronological: with [S5] (2021), [S7] (2022) and [S4]
  (2026) this carrier is shown writing the product **across three *Höchstrechnungszins* regimes**
  [R7] [R8] [R11]. No clause-level content established from this edition.

### S8 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", LA 904 A
- Publisher: Cosmos Lebensversicherungs-AG (the direct-writing arm of Generali Deutschland)
- Doc type: *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**
- URL: https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **the most quantitatively load-bearing document in the corpus.** A search summary
  returned its conversion basis in terms: **"The annuity factor determined at the beginning of the
  contract is calculated on the basis of a recognised mortality table (currently DAV 2004 R) and an
  underlying interest rate (currently 0 percent p.a.)."** That establishes three things at once:
  the *garantierter Rentenfaktor* is fixed **at inception**; the table is **DAV 2004 R** [R12]
  [R13]; and at this document's vintage the guaranteed factor's **interest basis was 0 % p.a.** —
  below the then-current *Höchstrechnungszins*, and therefore a deliberate prudential margin rather
  than the statutory maximum. On *Überschussbeteiligung*, the standard AVB disclaimer: **"the
  amount of profit sharing depends on many influences which are unpredictable and only limitedly
  controllable by the company, with the most important influencing factor being capital-market
  developments."** The document also appeared in the result set for the death benefit before
  *Rentenbeginn*. **The vintage of LA 904 A was not established**, which matters because the
  "currently 0 percent p.a." clause is explicitly time-stamped — gap 5. Siblings in the same series
  fix the house numbering: **LA 1204 A (11.22)**, **LA 1201 A (11.22)** (8 pp.), **LA 1005 A**
  (Riester), **LA 1311 A** (FlexInvest), **LA 1100 A** and **LA 1079/936/1099 A** (Basisrente),
  **LA 1081 A** (Direktversicherung). LA 904 is the oldest number in that list.

### S9 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301"
- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**; publisher
  document id `gn331451_p`
- URL: https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the only document whose **title itself names the *Rentengarantiezeit***, establishing it
  as a **tariff-level design feature carried in the product name**, not merely a rider. The summary
  establishes that **the contract value used for annuitisation includes any *Überschussbeteiligung*
  and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general
  contract data** — the conversion input in one sentence. Siblings in the same result set:
  `gn331530_p` (fondsgebunden) and `gn331303_p` (*mit sofort beginnender Rentenzahlung*). No
  paragraph numbering established.

### S10 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung mit aufgeschobener Rentenzahlung"
- Publisher: GDV
- Doc type: *Musterbedingungen* for the **survivor's-annuity rider** attaching to this product
- URL: https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: establishes that the market treats the **survivor's annuity as a *Zusatzversicherung*
  (rider) with its own condition set**, attached to the base contract rather than a benefit of it —
  so a reference implementation carries it as a module **off in the base run**. No clause content
  established.

### S11 — Debeka Lebensversicherungsverein a. G., "Allgemeine Bedingungen für eine Rentenversicherung mit …" (B LV 85)
- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: AVB, house document code **B LV 85**
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the title was returned truncated ("… mit …"), so the exact product variant is **not
  established**. Siblings fix the house numbering and its currency: **B LV 100 (01.07.2026)**,
  16 pp., and **B LV 101 (01.01.2025)**, 17 pp., both in the *betriebliche Altersversorgung* folder
  and out of scope — but they establish that Debeka's AVB series was being reissued as recently as
  **1 July 2026** (gap 9). The related summary establishes Debeka's own definition of the
  accumulation quantity: **the *Deckungskapital* is the sum of the contributions accumulated at the
  *Rechnungszins*, insofar as those contributions are not required for risk and expense cover** —
  the cleanest statement of the recursion in the corpus, and the basis of section 5.

### S12 — Debeka, "Privatrente" product page
- Publisher: Debeka
- Doc type: insurer product page
- URL: https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the current-generation Debeka private annuity, and a **split-surplus design**: **"from
  the savings portion, Debeka forms a *Deckungskapital* for the guaranteed benefits; surplus shares
  of the accumulation phase are invested in an internal fund and can enable additional benefits"**,
  and **"fund holdings generally receive no *Überschussbeteiligung* from the earnings of Debeka's
  general *Sicherungsvermögen* before *Rentenbeginn*"**. On tax: **if a lifelong monthly annuity is
  chosen at *Rentenbeginn*, only part of the payout is taxed — the comparatively low
  *Ertragsanteil*, depending on age at *Rentenbeginn*** [R5]. The insurer **no longer offers the
  classical annuity product**; the offer is now the newer variants with a flexible allocation
  between guaranteed and fund-based components — corroborating [R22] from the insurer's own page.

### S13 — Allianz Lebensversicherungs-AG, "Vorsorgekonzept KomfortDynamik" / PrivatRente KomfortDynamik
- Publisher: Allianz Lebensversicherungs-AG
- Doc type: insurer product page, plus a distributed *persönlicher Vorschlag* specimen quotation for
  the BasisRente variant hosted by a broker at
  `privat.rh-insuranceservices.com/wp-content/uploads/2025/02/Berechnung-BasisRente-KomfortDyn.pdf`,
  dated by its path to **February 2025**
- URL: https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **the successor design that replaced the classic tariff at the market leader.** Premiums
  are **split between the Allianz *Sicherungsvermögen* and the KomfortDynamik *Spezialfonds***; the
  design "combines elements of a classic life insurance with a dynamics part, so-called asset-value
  investments". **Guarantee levels at *Rentenbeginn* of 60 %, 80 % or 90 % of the premiums paid**,
  selectable, 80 % standard. Customers receive **"only modest guarantees"** at inception: retention
  of the premiums paid at the selected level **and a minimum annuity**, provided the contract is
  held to the end of the term — the *garantierter Rentenfaktor* in another guise. **"The
  calculation bases at *Rentenbeginn* … relate to the interest rate and mortality table that the
  company uses at that time for immediately beginning annuities"** — the corroborating statement,
  from a second carrier, that the *aktueller Rentenfaktor* is the carrier's then-current
  immediate-annuity tariff. The **Rentengarantiezeit** "can be set to a minimum" — a
  policyholder-selectable parameter with a floor. Two charge figures were returned by commentary in
  the same result set and are recorded with their provenance stated: an **Abschlussprovision of
  1 575 €** on the specimen quotation, and, in the BasisRente and RiesterRente variants, **total
  costs relative to the capital formed of at most 0,95 € per 100 €**. Both come from third-party
  analyses rather than an Allianz tariff sheet, are `[unverified]` as market-representative levels,
  and are the **only** charge figures the whole corpus produced.

### S14 — Mecklenburgische Versicherungsgruppe, "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (Rente flex)
- Publisher: Mecklenburgische Lebensversicherungs-AG
- Doc type: *Vertragsinformationen* for the "Rente flex" private annuity
- URL: https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the title is truncated after "mit flexiblem", so the product's distinguishing feature —
  most plausibly a flexible *Rentenbeginn* — is **not established**. Recorded as a mid-sized-mutual
  data point and as evidence that *Vertragsinformationen* is a second common name for the same
  pre-contractual pack [S4]. No clause content established.

### S15 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher: Konzern Versicherungskammer (the Bavarian public-sector insurance group); the `BL_`
  path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity
- Doc type: the annual **surplus-declaration document** — the instrument by which a German life
  insurer publishes its declared *Überschussanteilsätze* for a calendar year
- URL: https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: establishes the **existence and the current vintage (2026)** of the annual declaration
  document type, which is the primary source class for every surplus rate a model of this product
  needs. **No rate, no percentage and no surplus-component split was established from it** — the
  summary returned only the title. This is gap 4, the largest hole in the file after gap 3: the
  corpus establishes the *machinery* of the *Überschussbeteiligung* thoroughly and its *current
  levels* not at all.

### S16 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation … Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* for the **immediate** annuity. Document code **521331402 2501**.
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the immediate-annuity sibling of [S4]–[S7] from the same carrier and series. It is in
  this file — despite belonging to delib's `sofortrente` — because [S13] establishes that the
  *aktueller Rentenfaktor* of a deferred contract is taken from the carrier's **then-current
  immediate-annuity tariff**. No clause content established from this edition.

### S17 — Zurich, "Private Rentenversicherung" product page
- Publisher: Zurich Gruppe Deutschland
- Doc type: insurer product page
- URL: https://www.zurich.de/de-de/pk/altersvorsorge/private-rentenversicherung
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the retail presentation of the family whose conditions are [S4]–[S7]. **No parameter,
  price point or envelope was established from it.**

### S18 — Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"
- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: general pre-contractual information on a retirement-provision system
- URL: https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the URL's `?t=1604038997833` parameter is a millisecond timestamp corresponding to
  **October/November 2020**, which dates the file. No clause content established. Recorded as a
  further carrier and as a second example of the *allgemeine Informationen* document type [S4].

### S19 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", 03101/07/2024
- Publisher: DEVK Lebensversicherungsverein a. G.
- Doc type: *Kundeninformation* for a **unit-linked** annuity, document code **03101**, **07/2024**
- URL: https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **out of scope as a product** — it is delib's `fondsgebundene_rentenversicherung` — and
  is recorded solely for the **contrast on the death benefit**: on death before *Rentenbeginn* the
  benefit is **the fund value at the date of death but at least the sum of the premiums paid
  (*Beitragsrückgewähr*)**. That `max(account value, premiums paid)` shape is the unit-linked form
  of what the classic product expresses as `max(Deckungskapital, premiums paid)` or as one or the
  other outright. It is used here as the contrast, **not** as the classic rule; see section 7.

---

## Regulatory and actuarial references

Twenty-four product-specific regulatory and actuarial references. Statutory articles carry the
canonical `gesetze-im-internet.de` URL where several legal-database mirrors returned the article;
where the canonical slug itself was not returned by any search, the URL is recorded as not
established and the mirrors are named instead. Cross-product references that belong to the delib
reference library (VAG, MindZV, LVRG, RechVersV, Solvency II, IFRS 17, Protektor) are **not**
duplicated here; they carry `[REG-R#]` tags downstream.

### R1 — VVG § 169, Rückkaufswert
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: https://www.gesetze-im-internet.de/vvg_2008/__169.html
- Retrieved: no — egress blocked; established from search-result summaries. The article was
  returned by eight independent mirrors — `dejure.org/gesetze/VVG/169.html`,
  `buzer.de/169_VVG.htm`, `juraforum.de/gesetze/vvg/169-rueckkaufswert`, `lxgesetze.de/vvg/169`,
  `sozialgesetzbuch-sgb.de/vvg/169.html`, `datenbank.nwb.de/Dokument/79238_169/`,
  `de.wikipedia.org/wiki/Rückkaufswert`, and the Deutsche Rentenversicherung's own commentary at `rvrecht.deutsche-rentenversicherung.de/…/VVG/0169/0169_2016_01_01.html` (whose path segment
dates the commentary version to **1 January 2016**).
- Content, as reported: for **unit-linked** contracts the *Rückkaufswert* is to be computed
  **according to recognised rules of actuarial mathematics as the *Zeitwert* of the insurance**,
  insofar as the insurer does not guarantee a particular benefit, and **the principles of the
  calculation must be stated in the contract**. **A deduction is permitted only if it is agreed,
  quantified (*beziffert*) and appropriate (*angemessen*)**, and **an agreement of a deduction in
  respect of not-yet-amortised *Abschluss- und Vertriebskosten* is void (*unwirksam*)**. The
  computed value may be reduced by a **contractually agreed and appropriate *Stornoabzug*
  (*Rückkaufsabschlag*)**; the result is the **statutory minimum surrender value**, below which a
  contractually agreed value may not fall. **§ 169 Abs. 6 VVG permits the insurer, in defined
  cases, to reduce surrender values that are to be paid out.** The **five-year spreading of
  *Abschluss- und Vertriebskosten*** that commentary associates with § 169 Abs. 3 was **not**
  returned by any summary and is `[unverified]` at article level; see gap 12.

### R2 — VVG § 165, Prämienfreie Versicherung (Beitragsfreistellung)
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__165.html — **returned directly by the search**
- Retrieved: no — egress blocked; established from search-result summaries. Also returned by
  `dejure.org/gesetze/VVG/165.html`, `buzer.de/165_VVG.htm`,
  `juraforum.de/gesetze/vvg/165-praemienfreie-versicherung`,
  `datenbank.nwb.de/Dokument/79238_165/` and `freirecht.de/g/VVG:165`.
- Content, as reported:
  - **The policyholder may at any time demand, for the end of the current insurance period, that
    the insurance be converted into a premium-free insurance, provided the agreed minimum
    insurance benefit is reached.**
  - **If that minimum benefit is not reached, the insurer must pay the surrender value
    attributable to the insurance, including profit shares, under § 169.**
  - **The premium-free benefit is calculated according to recognised principles of actuarial
    mathematics, using the calculation basis of the premium calculation, on the basis of the
    surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each
    insurance year.**
  - Applied to this product: **the policyholder always has the right to convert a running annuity
    contract into a premium-free annuity contract** — the conversion right is statutory, not a
    tariff concession, and it is exercisable at the end of the then-current insurance period.

### R3 — VVG § 163, Anpassung der Prämie / Bedingungsanpassung
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__163.html (canonical form; the article was
  reached in this session through commentary rather than through a statute mirror)
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the summaries establish § 163 VVG as **the operative statutory basis on which a German
  life insurer may today change a guaranteed *Rentenfaktor***, having replaced the contractual
  *Treuhänderklausel* route for new business. The two triggers the commentary attributes to the
  clause family are: **an unexpectedly strong increase in life expectancy, requiring an adjustment
  of the mortality bases**, and **a sustained reduction in capital-market returns, permitting an
  adjustment of the interest basis**. The commentary that carried this is
  `bavprofis.de/news-lesen/rentenfaktor-altersvorsorge-rente.html`, headed "RENTENFAKTOR ENTHÜLLT
  | DIE MACHT DES § 163 VVG", corroborated by [R17]. **The article's own paragraph structure and
its procedural requirements (trustee review, notice) were not established** — see gap 6.

### R4 — VVG § 153, Überschussbeteiligung, and § 153 Abs. 3, Beteiligung an den Bewertungsreserven
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/vvg_2008/__153.html (canonical form)
- Retrieved: no — egress blocked; established from search-result summaries — here, unusually, from
  an **insurer's** restatement rather than from a statute mirror.
- Content: the Zurich consumer-information summary [S4] [S5] states that **§ 153 Absatz 3 VVG
  currently provides for an equal (*hälftige*) participation in the *Bewertungsreserven***, and
  that the participation must be given effect "according to the legal and supervisory provisions".
  The same summary establishes two product-specific consequences: **the transition to annuity
  payment is a key point for the *Bewertungsreserven* participation**, and **policyholders also
  participate in the *Bewertungsreserven* during the annuity payment period**. The remainder of §
  153 — the *verursachungsorientiertes Verfahren* (cause-oriented allocation), the opt-out in §
  153 Abs. 1, and the LVRG 2014 *Sicherungsbedarf* restriction on the *Bewertungsreserven* share —
  was **not** established by any summary in this session and is `[unverified]` here; it belongs to
  the delib cross-product reference library.

### R5 — EStG § 22, Ertragsanteilsbesteuerung der Leibrente
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/estg/__22.html — **returned directly by the search**
- Retrieved: no — egress blocked; established from search-result summaries.
- Content, as reported:
  - Payments from private annuity contracts, and from life contracts converted into a classic
    monthly *Leibrente*, are taxed on the ***Ertragsanteil*** basis.
  - **Only the "Ertrag des Rentenrechts"** — the interest component contained in the annuity from
    the beginning of the payout phase — **is subject to tax**.
  - **The *Ertragsanteil* is determined by the annuitant's age at *Rentenbeginn*.** The earlier
    the annuity begins, the longer the remaining life expectancy and hence the annuity's duration,
    and **the higher the taxable *Ertragsanteil***.
  - **For an annuity commencing at age 65 the *Ertragsanteil* is 18 % of the annuity.** This is
    the only value on the statutory table that any summary in this session returned; every other
    age's percentage is `[unverified]` here (gap 8).
  - The precise statutory address usually given for the table — § 22 Nr. 1 Satz 3 Buchst. a
    Doppelbuchst. bb EStG — was **not** confirmed by any summary and is `[unverified]`.

### R6 — EStG § 20 Abs. 1 Nr. 6, taxation of a Kapitalabfindung (the 12/62 rule and the Halbeinkünfteverfahren)
- Publisher: Bundesministerium der Justiz / juris
- URL: https://www.gesetze-im-internet.de/estg/__20.html (canonical form; reached in this session
  through tax commentary rather than a statute mirror)
- Retrieved: no — egress blocked; established from search-result summaries.
- Content, as reported, and corroborated across five independent commentaries — IWW's *AStW*
  (`iww.de/astw/einkommensteuer/20-estg-rentenzahlungen-aus-einem-vor-dem-112005-abgeschlossenen-beguenstigten-versicherungsvertrag-mit-kapitalwahlrecht-f141638`),
  LV 1871 [R24], Finanzküche, GN Finanzpartner and Finanztip [R20]: **annuity contracts with a
  *Kapitalwahlrecht* against ongoing premium payments fall under § 20 EStG if the capital option
  cannot be exercised before 12 years from contract conclusion**; **the "12/62 rule" — at least
  12 years of contract duration and payment after completion of the 62nd year of life**; **where
  the rule is met only half of the gain (*Ertrag*) is taxable — the *Halbeinkünfteverfahren* — and
  it applies only to lump-sum payments and to multiple capital withdrawals on a payout plan, not
  to monthly annuity payments**; and **for contracts concluded before 1 January 2005 the
  half-income treatment of the lump sum is retained, while annuity payments continue uniformly to
  be taxed on the *Ertragsanteil* basis** [R5]. The *Mindesttodesfallschutz* condition that
  § 20 Abs. 1 Nr. 6 imposes on endowment contracts was not returned by any summary and is
  `[unverified]` here; it belongs to the delib `kapitallebensversicherung` file.

### R7 — Deckungsrückstellungsverordnung (DeckRV), § 2 — Höchstrechnungszins
- Publisher: Bundesministerium der Justiz / juris (instrument); Bundesministerium der Finanzen
  (amendment)
- URL: **not established.** No search result in this session returned a `gesetze-im-internet.de`
  address for the DeckRV, and no URL was guessed. The instrument is established instead from the
  four news and trade sources [R8] [R9] [R10] [R11].
- Retrieved: no — egress blocked; established from search-result summaries.
- Content, corroborated across five independent sources:
  - The *Höchstrechnungszins*, **also commonly called the *Garantiezins***, is **the maximum
    interest rate a life insurer may guarantee to customers on the savings portions of their
    premiums**. It is set in the **Deckungsrückstellungsverordnung**.
  - **With effect from 1 January 2025 it was raised from 0,25 % to 1,00 %** by an amendment of the
    DeckRV, announced in the *Bundesgesetzblatt* on **24 July** [R11] (the year is 2024 by
    construction but was not itself stated in the summary). **This is the first increase since
    1994**; every prior movement was downward.
  - **The increase applies to new contracts with guarantees concluded from the date of the increase
    onwards**; existing contracts keep the *Rechnungszins* they were written on. This is the single
    most important consequence for a model: a German life book is a **layered stack of guarantee
    vintages**, not one rate.
  - Process: the **DAV recommended in November 2023** that the rate be raised to 1 % as of 2025
    [R9]; the **Bundesministerium der Finanzen adopted the recommendation in late April 2024**
    [R9]; the **DAV recommends 1,0 % for 2026 as well** [R8].
  - **The full history of the rate — 4 % to 1994, then 3,25 %, 2,75 %, 2,25 %, 1,75 %, 1,25 %,
    0,90 % and 0,25 % from 2022 — was not established**; every figure in that sequence other than
    the 0,25 % and the 1,00 % is `[unverified]` here. See gap 7.

### R8 — DAV, "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0 Prozent"
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV), Köln
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the DAV's recommendation that the *Höchstrechnungszins* remain at **1,0 % for 2026**.
  Establishes that the rate applicable to new business at the access date of this file
  (2026-08-29) is **1,0 %**, on the profession's own recommendation, and that the recommendation
  mechanism — DAV recommends, BMF legislates — is the standing process [R9].

### R9 — DAV, "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins 2025"
- Publisher: DAV
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the DAV's statement on the BMF's move for 2025. Establishes the **November 2023 DAV
  recommendation** and the **late-April 2024 BMF adoption**, i.e. the roughly 14-month lead time
  between the profession's recommendation and the rate taking effect. This lead time is what makes
  the *Rechnungszins* of a tariff a **known-in-advance** parameter for pricing.

### R10 — GDV, media information on the Höchstrechnungszins increase (two releases)
- Publisher: GDV
- URLs:
  - https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848
  - https://www.gdv.de/gdv/medien/medieninformationen/versicherer-befuerworten-anhebung-des-hoechstrechnungszinses--157548
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the industry association's statements supporting the increase, headed
  "Höchstrechnungszins-Erhöhung ist eine 'angemessene Reaktion auf gestiegene Zinsen'" and
  "Versicherer befürworten Anhebung des Höchstrechnungszinses". The lower media id (157548) is the
  earlier, pre-legislation release; the higher (176848) follows the decision. Together they
  corroborate [R7] on the increase and its rationale. No figure beyond the 1,0 % was established.

### R11 — HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- Publisher: HDI Lebensversicherung AG (press/blog)
- URL: https://pm.hdi.de/blog/h%C3%B6chstrechnungszins-in-der-lebensversicherung-steigt-zum-01.01.2025
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: an **insurer's own** statement of the change, and the source of the wording "zum
  01.01.2025 wird der Höchstrechnungszins gemäß Deckungsrückstellungsverordnung von 0,25 % auf
  1,00 % angehoben", together with the *Bundesgesetzblatt* announcement date of **24 July**. Third
  independent corroboration of [R7], and the one that names the instrument.

### R12 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen" (DAV-Richtlinie)
- Publisher: Deutsche Aktuarvereinigung e. V.
- Doc type: **DAV-Richtlinie** (professional guideline). The file name carries the date
  **2023-06-28**, so the guideline was reissued or last revised on **28 June 2023** — nineteen
  years after the table itself.
- URL: https://aktuar.de/content/PDF/Fachwissen/2023-06-28_DAV-Richtlinie_Herleitung_DAV2004R.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the profession's derivation document for the table this product is priced on. The
  summaries establish the **component structure** — a **base table of second order**, a **base
  table of first order**, a **mortality trend of second order**, a **mortality trend of first
  order**, and an **age adjustment (*Altersverschiebung*) with a base table** — and that
  **first-order probabilities carry safety margins relative to the second-order ("realistic")
  probabilities, in order to assess the risk prudently**, the **second-order base tables
  representing the best estimate of period mortality in 1999 for insured lives, as
  three-dimensional selection tables**. The 2023 reissue date is significant on its own:
  DAV 2004 R was still the profession's maintained annuity basis **twenty years after its base
  year** — the fact behind the longevity trigger of the § 163 VVG adjustment right [R3].

### R13 — DAV, "DAV 2004 R: Stand 22.02.2005"
- Publisher: DAV
- Doc type: the table document itself. The title line returned reads **"- 1 - DAV 2004 R: Stand
  22.02.2005"**; the file name carries **2005-09-14**, so the document is **dated 22 February 2005
  and published (or re-posted) on 14 September 2005**.
- URL: https://aktuar.de/content/PDF/Fachwissen/2005-09-14-DAV_2004_R.pdf
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **DAV 2004 R is a *Generationentafel* used for annuity insurance calculations in
  Germany**; generation tables **contain mortality by birth cohort, including the expected future
  change in mortality** — the improvement is built into the table rather than applied on top of it.
  **It was intended for new business from 2005 onwards and has been in use since June 2004.** The
  numeric content is **not** in this file: the DAV tables are the property of the Deutsche
  Aktuarvereinigung, are not public, and are **not redistributed by delib**.

### R14 — Contemporaneous expositions of DAV 2004 R (DGVFM, Gen Re, qx-Club)
- Publishers: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik, in *Blätter der
  DGVFM* (hosted by Springer); General Reinsurance ("A Berkshire Hathaway Company"), presented to
  the Aktuarvereinigung Österreichs on **27 October 2004**; qx-Club Berlin, **16 August 2004**;
  qx-Club (Helmert), **14 September 2004**
- URLs:
  - https://link.springer.com/article/10.1007/BF02808312
  - https://www.avoe.at/archiv/nachlese-20041027.pdf
  - http://www.qx-club-berlin.de/material/pdf/20040816-qx-Club-Sterbetafel-DAV2004R.pdf
  - https://www.qx-club.de/.cm4all/uproc.php/0/Vortr%C3%A4ge/vortrag_helmert_14092004.pdf?_=173ca294dfb&cdp=a
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the peer-reviewed publication of the derivation, plus three practitioner accounts from
  **August to October 2004** — between the table's June 2004 first use and its 2005 general
  application [R13] — which date the market's adoption. The Helmert presentation is titled
  **"DAV 2004 R und RBx"**, RBx being the *Rentenbestandstafel* for the **existing annuity book**
  as against new business: the only evidence in the corpus that DAV 2004 R has a **companion
  in-force table**. Slide and abstract content were not established.

### R15 — Wikipedia (German), "Sterbetafel"
- Publisher: Wikimedia Foundation
- URL: https://de.wikipedia.org/wiki/Sterbetafel
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the general-encyclopaedia definition corroborating the generational characterisation of
  DAV 2004 R [R13]: **generation tables contain mortality per birth cohort including the expected
  future change in mortality**. A corroborating secondary source only; nothing in this file rests
  on it alone.

### R16 — Finanztip, "Urteil zum Rentenfaktor: Rentenkürzung verhindern"
- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH
- URL: https://www.finanztip.de/private-rentenversicherung/rentenfaktor/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the consumer organisation's account of the *Rentenfaktor* and of the litigation over
  its reduction; with [R17] and [R18] it establishes the *Treuhänderklausel* story of section 8. A
  companion consumer-press item in the same result set
  (`gegen-hartz.de/news/rente-nachtraegliche-absenkung-des-rentenfaktors-kann-rechtswidrig-sein-urteil`)
  reports that **a subsequent reduction of the *Rentenfaktor* can be unlawful**.

### R17 — versicherungenmitkopf.de, pages on the Treuhänderklausel, the Rentenfaktor, the Rentengarantiezeit and the Ertragsanteil
- Publisher: versicherungenmitkopf.de (independent broker's consumer pages)
- URLs:
  - https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung
  - https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor
  - https://www.versicherungenmitkopf.de/rente/rentengarantiezeit-rentenversicherung-riester-und-co
  - https://www.versicherungenmitkopf.de/ertragsanteilsbesteuerung
  - https://www.versicherungenmitkopf.de/rentenversicherung/besteuerung-private-rentenversicherung-wie-viel-bleibt-uebrig
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the densest secondary account in the corpus, and the source of the *Treuhänderklausel*
  narrative. **Insurers could previously change guaranteed *Rentenfaktoren* on the basis of a
  *Treuhänderklausel* contained in the insurance conditions, with the approval of an independent
  external *Treuhänder* (trustee)**; **that clause is now used only in older contracts, and today
  the guaranteed *Rentenfaktor* can be changed only on the basis of § 163 VVG** [R3]. **The clause
  allows the insurer to change essential contract components such as the *Rentenfaktor* if economic
  conditions deteriorate permanently and unexpectedly**, subject to the trustee's review and
  approval, on **two explicit triggers**: an **unexpectedly strong increase in life expectancy**
  (requiring adjustment of the mortality tables) and a **sustainable reduction in capital-market
  returns** (permitting adjustment of the interest rate). **The Landgericht Köln clarified that the
  low-interest phase is not sufficient ground for such an adjustment, because it must be treated as
  entrepreneurial risk that cannot be passed on to policyholders** — **the case reference, decision
  date and party names were not established** (gap 10). It is also the source, jointly with [R24],
  for the *Rentengarantiezeit* material in section 9 and, jointly with [R5] [R24], for the tax
  material in section 15.

### R18 — Versicherungswirtschaft-heute, "Treuhänderklausel: Allianz glaubt nicht, dass Kunden einer Anpassung des Rentenfaktors erfolgreich widersprechen können" (4 February 2021)
- Publisher: Versicherungswirtschaft-heute (trade press)
- URL: https://versicherungswirtschaft-heute.de/unternehmen-und-management/2021-02-04/treuhaenderklausel-allianz-glaubt-nicht-dass-kunden-einer-anpassung-des-rentenfaktors-erfolgreich-widersprechen-koennen/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: dated **4 February 2021** by its own URL path. Establishes that the *Treuhänderklausel*
  question was a **live commercial dispute at the market leader in 2021** — not a historical
  curiosity, but a mechanic carriers were actively defending inside the window in which the
  current in-force book was written. Body content beyond the headline was not established.

### R19 — Franke und Bornberg, "Was bedeutet der Rentenfaktor und wie hoch ist er?" and "Altersvorsorge: Überschüsse im Rentenbezug Teil 1 — Die Qual der Wahl"
- Publisher: Franke und Bornberg GmbH (independent product-rating house)
- URLs:
  - https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022
  - https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the rating house's treatment of the *Rentenfaktor* and of **surplus use in the payout
  phase** — the professional source behind section 9's three-system taxonomy. The first URL's slug
  dates that analysis to the **2021/2022** window; the second is explicitly "Teil 1" of a series.
  **No *Rentenfaktor* level, range or table was returned by the summary** — the very question the
  first title asks was not answered by anything the search returned. This is gap 3, the largest
  quantitative hole in the file.

### R20 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH
- URLs:
  - https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/
  - https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the consumer organisation's account of surplus participation and of life-insurance
  taxation. Source, jointly with [R19] [R21] [R24], of the **three payout-phase surplus systems**
  (*konstant*, *teildynamisch*, *volldynamisch*) recorded in section 9, including the observation
  that **under the constant system the annuity can still fall, because if the insurer earns less
  than expected the surplus-financed part is reduced**. Also a corroborating source for the 12/62
  rule [R6].

### R21 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher: GDV, under its consumer brand *Die Versicherer*
- URL: https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **the industry association's own consumer account of the payout options** of a private
  annuity, and therefore the closest thing in the corpus to an authoritative statement of the
  *Kapitalwahlrecht*-versus-annuity choice. It sits in the result set that established the three
  payout-phase surplus systems. **The notice period for exercising the *Kapitalwahlrecht* was not
  established from it** — gap 11.

### R22 — Versicherungsbote, "Debeka stellt klassische Rentenversicherung ein"
- Publisher: Versicherungsbote Verlag (trade press)
- URL: https://www.versicherungsbote.de/id/4842718/Debeka-Rentenversicherung-Garantiezins/
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: **the market-structure fact this whole file has to be read against.** **Debeka
  Lebensversicherung will no longer sell classic annuity insurance**, confirmed by a company
  spokesperson. **From 1 July 2016 Debeka introduced a new private-provision portfolio with five
  tariff variants under the name "Chance"**; in the safest variant **0,5 % interest is
  guaranteed**, and the riskiest variant is **effectively a fund policy with no guarantees**.
  **The decision was part of a broader industry trend: Allianz, Zurich and Generali had already
  stopped distributing classic annuity insurance before it.** The 0,5 % guarantee is a rare hard
  figure and sits **below** the *Höchstrechnungszins* then in force — a deliberately de-risked
  guarantee. A companion item in the same result set,
  `versicherungsbote.de/id/4949977/…/Lebensversicherung-Die-Marktfuehrer-im-Solvenzcheck-Teil-2/`,
  characterises the **Debeka group as "klassisches Garantiegeschäft"** in a solvency review, which
  is what makes its withdrawal from this product significant.

### R23 — Versicherungsjournal, "Allianz 'KomfortDynamik': Noch immer eine Rentenversicherung?"
- Publisher: Versicherungsjournal Verlag (trade press)
- URL: https://www.versicherungsjournal.de/versicherungen-und-finanzen/allianz-komfortdynamik-noch-immer-eine-rentenversicherung-123163.php
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the trade press's framing of the successor design — the headline itself asks whether
  the replacement is still an annuity contract in the classic sense. Corroborates [S13] on the
  KomfortDynamik construction and on the **60 / 80 / 90 % guarantee ladder**. Companion analyses
  in the same result set are
  `levelv-finanz.de/allianz-privatrente-komfortdynamik-im-test-finanzmathematische-analyse/`,
  `bsc-gmbh.com/blog/komfort-dynamik-der-allianz/`,
  `vorsorgekampagne.de/test-allianz-rentenversicherung-komfortdynamik/`,
  `hauke-simonsen.de/allianz-komfortdynamik-lohnt-sich-diese-rentenversicherung/` and
  `expertenmarkt.de/magazin/lohnt-sich-allianz-komfort-dynamik-was-die-betriebliche-altersvorsorge-wirklich-bringt`;
  the two Allianz charge figures recorded under [S13] come from that cluster and are
  `[unverified]` as market-representative levels.

### R24 — Consumer and comparison-portal cluster on the Rentenfaktor, the Rentengarantiezeit, the Überschussbeteiligung and the death benefit
- Publishers: LV 1871; NÜRNBERGER; Verivox; Gabler *Versicherungslexikon* and Gabler
  *Wirtschaftslexikon*; Wikipedia (German); Deutsche Rentenversicherung; fragfina.de;
  gn-finanzpartner.de; Finanzküche; Compeon; versicherung-vergleiche.de; Pensionskasse der
  Genossenschaftsorganisation; financedoor.de; prolife-gmbh.de; Volksbanken Raiffeisenbanken
  (vr.de); biac-vorsorgespezialist.de; R+V; lifefinance.de; vergleich-sofortrente.de
- URLs (a representative subset of what the searches returned; cited collectively as [R24] because
  no single member is load-bearing and every fact drawn from the cluster is corroborated by at
  least one other member — the omitted members are further pages of the same publishers):
  - https://www.lv1871.de/fondsgebundene-rentenversicherung/fragen/rentenfaktor/
  - https://www.lv1871.de/private-rentenversicherung/wiki/ertragsanteilsbesteuerung/
  - https://www.lv1871.de/private-rentenversicherung/fragen/todesfall/
  - https://www.lv1871.de/fondsgebundene-rentenversicherung/fragen/beitragsfreistellung/
  - https://www.nuernberger.de/themenwelt/beruf-vorsorge/rentenfaktor/
  - https://www.verivox.de/lebensversicherung/themen/ueberschussbeteiligung/
  - https://wirtschaftslexikon.gabler.de/definition/ueberschussbeteiligung-48786
  - https://de.wikipedia.org/wiki/%C3%9Cberschussbeteiligung
  - https://www.deutsche-rentenversicherung.de/SharedDocs/Glossareintraege/DE/E/ertragsanteil
  - https://www.fragfina.de/ratgeber/ueberschussbeteiligung-nach-rentenbeginn/
  - https://www.fragfina.de/research/rentenfaktor-check-2025/
  - https://www.gn-finanzpartner.de/blog/rentenfaktor-richtig-berechnen
  - https://www.finanzkueche.de/blog/garantierter-rentenfaktor
  - https://www.compeon.de/glossar/rentengarantiezeit/
  - https://www.versicherung-vergleiche.de/private_altersvorsorge/versprechen.htm
  - https://www.financedoor.de/blog/2025/10/der-garantierte-rentenfaktor/
  - https://www.vr.de/privatkunden/produkte/altersvorsorge/private-rentenversicherung/ueberschussbeteiligung.html
  - https://www.ruv.de/altersvorsorge/was-passiert-mit-versicherungen-im-todesfall
- Retrieved: no — egress blocked; established from search-result summaries.
- Content: the source of the *definitional* material in sections 5, 6, 7, 8, 9 and 15 — the
  *Rentenfaktor* arithmetic and the guaranteed/current distinction; the *Zinsüberschuss*
  hurdle-rate definition; the *verzinsliche Ansammlung* and *Bonusrente* mechanics; the surplus
  systems in both phases; the *Rentengarantiezeit* mechanics, durations and cost illustration; the
  three death-benefit forms before *Rentenbeginn*; and the *Ertragsanteil*. One member,
  `financedoor.de/blog/2025/10/der-garantierte-rentenfaktor/`, carries a **2025-10** date in its
  path, placing it inside the current *Höchstrechnungszins* regime; another,
  `fragfina.de/research/rentenfaktor-check-2025/`, is titled a **2025 *Rentenfaktor* check with
  data and analysis** and is the single most likely public source of the market range this file
  could not establish (gap 3).

## Extracted facts, by mechanic

### 1. Product structure, legal form and the Schicht-3 placing

- The product is a **life insurance contract** under the VVG, on a single life, in which the
  insurer's obligation is **an annuity payable for the annuitant's lifetime beginning at a
  contractually fixed date**, with an accumulation period before it [S1] [S4] [S8] [S9].
- The insurer's own placement is **Schicht 3 — "Private Vorsorge"**: the Zurich scope line is
  "Aufgeschobene Rentenversicherung — **Private Vorsorge (Schicht 3)** und Rückdeckungsversicherung
  (Schicht 2)" [S4]. Schicht 3 is the unsubsidised layer: no § 10 EStG deduction, no *Zulage*, no
  certification under the *Altersvorsorgeverträge-Zertifizierungsgesetz*.
- The boundary is visible in the GDV's own taxonomy: **separate** model conditions exist for the
  *Basisrente* (titled by reference to § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa EStG) and for
  *Altersvorsorgeverträge* under the certification act [S3]. This product is the one **without** a
  statutory qualification clause in its title [S1] [S2].
- **The GDV model conditions are non-binding.** "Diese Bedingungen sind unverbindlich" heads the
  set [S2] and the association's index states that use is optional [S3]. German AVB for this
  product are therefore **structurally very similar and textually distinct** — which is why a
  delib composite is the right unit of description and why no single carrier's wording is adopted
  wholesale.
- The German pre-contractual pack is issued under several names — *Verbraucherinformation* [S4]–
  [S7], *Vertragsinformationen* [S14], *Kundeninformation* [S19], *Allgemeine Informationen zu
  einem Altersversorgungssystem* [S18] — and is one object: general information, the AVB, the
  special conditions for options and riders, and the tax notes [S4].
- **The structure of that pack, from [S4], is the template for the delib documents**: (i)
  allgemeine Informationen; (ii) Allgemeine Versicherungsbedingungen; (iii) Besondere Bedingungen
  für die Anpassungsversicherung in der Rentenversicherung (*Dynamik*); (iv) allgemeine
  steuerliche Hinweise; (v) Besondere Bedingungen für die Berufsunfähigkeits-Zusatzversicherung.
- **The survivor's annuity is a rider, not a base benefit**: the GDV publishes it as a separate
  *Hinterbliebenenrenten-Zusatzversicherung* model condition set attaching to the deferred annuity
  [S10]. A reference implementation carries it as a module **off in the base run**. The **BUZ** is
  likewise a rider with its own special conditions inside the same pack [S4], and is delib's
  `berufsunfaehigkeit` product in its standalone form.
- One carrier issues the contract in more than one distribution wrapper — an ordinary edition [S4]
  [S5] [S7] and a *Konsortialversicherung* edition [S6]. Wrapper differences change the parties,
  not the cash flows.

### 2. The accumulation and payout phases, and the Rentenbeginn boundary

- The contract has **two phases separated by the *Rentenbeginn***: the *Aufschubzeit* (deferment
  period), over which premiums are paid and the *Deckungskapital* accumulates, and the
  *Rentenbezugsphase*, over which the annuity is paid [S1] [S4] [S8] [S11].
- **"Eine Aufschubzeit gibt es nur bei aufgeschobenen Rentenversicherungen"** — a deferment period
  exists only in a deferred annuity contract, which is the definitional line separating this
  product from delib's `sofortrente` [R24].
- The *Rentenbeginn* is **the pivot of the whole contract**, and three distinct things happen at
  it, all of which a model must sequence explicitly: (1) the accumulated value is struck, including
  surplus and *Bewertungsreserven* [S9]; (2) the *Rentenfaktor* to be applied is determined, by
  comparing the guaranteed factor with the then-current one [S4] [S13]; (3) the policyholder's
  *Kapitalwahlrecht* election, if any, takes effect [S12] [R21].
- **The transition to annuity payment is explicitly identified as a key point for the
  *Bewertungsreserven* participation** [S4]: the share is not a smooth accrual, it is crystallised
  at the boundary.
- **The participation in *Bewertungsreserven* does not stop at the *Rentenbeginn*.** Policyholders
  **also participate during the annuity payment period**, in accordance with the applicable VVG
  and supervisory provisions [S4] [R4]. A model that treats the payout phase as a closed,
  non-participating run-off is therefore wrong for this product.

### 3. Premium

- Two premium forms exist: a **laufender Beitrag** (level recurring premium over the
  *Aufschubzeit*) and an **Einmalbeitrag** (single premium); the recurring form is the one the
  accumulation mechanics in [S11] describe. **No search result established the market split, the
  minimum or maximum premium at any carrier, or the permitted range of the *Aufschubdauer*** — see
  gap 13.
- The premium is decomposed, in the insurer's own words, into the portion **required for risk and
  expense cover** and the remainder, the ***Sparbeitrag***, which is what accumulates: the
  *Deckungskapital* is "the sum of the contributions accumulated at the *Rechnungszins*, **insofar
  as these are not intended for risk and cost coverage**" [S11] — one sentence fixing the premium
  decomposition and the reserve recursion together. Debeka states the same split in the other
  direction: **"from the savings portion, Debeka forms a *Deckungskapital* for the guaranteed
  benefits"** [S12].
- **Payment frequency and the *Ratenzahlungszuschlag*.** German life tariffs load the annual
  premium for monthly, quarterly or half-yearly payment; **no loading percentage was established at
  any carrier** (gap 14), so any figure a delib document uses will be `[std]`.
- ***Zuzahlung*** — an ad-hoc additional single premium into a running contract — is a standard
  German option, but **nothing in the eighteen search results named it**; it is recorded as a gap,
  not a fact (gap 15).
- ***Dynamik* / *Anpassungsversicherung*** — the automatic annual increase of premium and benefit
  — **is established from a primary document**: the Zurich pack contains ***"Besondere Bedingungen
  für die Anpassungsversicherung in der Rentenversicherung"*** as a named section [S4], so the
  option exists, is documented at clause level, and has its own condition set. **Its parameters —
  the increase percentage, its basis, whether fresh underwriting applies, the number of refusals
  that end the option — were not established** (gap 15).

### 4. The Rechnungszins and the guarantee vintage stack

- The ***Rechnungszins*** is the rate at which the *Sparbeitrag* is guaranteed to accumulate in
  the *Deckungskapital* [S11]. It is capped for new business by the statutory
  ***Höchstrechnungszins***, set in the **Deckungsrückstellungsverordnung** [R7] [R11].
- The *Höchstrechnungszins* is **also commonly called the *Garantiezins*** and is defined as **the
  maximum interest rate a life insurer may guarantee on the savings portions of the premium** [R7]
  [R11].
- **From 1 January 2025 the *Höchstrechnungszins* is 1,00 %**, raised from **0,25 %** by an
  amendment to the DeckRV announced in the *Bundesgesetzblatt* on **24 July** [R7] [R10] [R11].
- **This was the first increase since 1994**; every movement in the intervening thirty years was
  downward [R7] [R11].
- **The DAV recommends 1,0 % for 2026 as well** [R8]. At this file's access date the rate
  applicable to new business is therefore **1,0 %**.
- The mechanism is: **DAV recommends → BMF legislates.** The DAV recommended the 1 % rate in
  **November 2023**; the **Bundesministerium der Finanzen adopted the recommendation in late April
  2024**; it took effect **1 January 2025** [R9]. The roughly fourteen-month lead time makes the
  *Rechnungszins* of a tariff a parameter that is known well before it binds.
- **The increase applies only to new contracts with guarantees concluded from the date of the
  increase onwards** [R7]. Existing contracts keep the rate they were written on. **The modelling
  consequence is decisive: a German life book is a layered stack of guarantee vintages, and the
  *Rechnungszins* is a model-point attribute, not a global assumption.**
- The full historical sequence of the rate is **not established here**; the only two levels any
  search confirmed are **0,25 %** (the immediately preceding rate) and **1,00 %** (from 2025),
  plus the fact that **4 %** applied until the 1994 change is `[unverified]` and comes from the
  bare phrase "first increase since 1994" [R7]. See gap 7.
- **An insurer may, and does, guarantee less than the statutory maximum.** Two independent data
  points establish this and both are hard figures:
  - **CosmosDirekt's *Rentenfaktor* is calculated on "an underlying interest rate (currently 0
    percent p.a.)"** [S8] — a zero interest basis for the conversion guarantee.
  - **Debeka's safest "Chance" variant guarantees 0,5 %** [R22]. Both sit below the
    *Höchstrechnungszins* in force at their vintage. A model must not assume the guaranteed rate
    equals the statutory cap.

### 5. The Aufschubphase: the Deckungskapital recursion

- **The definitional statement, from an insurer:** the *Deckungskapital* is **"the sum of the
  contributions accumulated at the *Rechnungszins*, insofar as these are not intended for risk and
  cost coverage"** [S11].
- Unpacked into the recursion a model implements — and this is a **reading** of [S11], not a
  clause the corpus supplied in this form:

  ```
  Deckungskapital(t) = ( Deckungskapital(t-1) + Sparbeitrag(t) ) x (1 + Rechnungszins)
  Sparbeitrag(t)     = Beitrag(t) - Risikobeitrag(t) - Kostenbeitrag(t)
  ```

  The ordering of premium credit, charge deduction and interest accrual within a period is **not
  established by any source in this corpus** and is a `[std]` decision for the delib
  implementation, stated explicitly in the processing order of `technical-notes.md`.
- **The *Deckungskapital* is the quantity everything else is defined off**: the death benefit in
  one of the two common designs (section 7), the basis of the *Rückkaufswert* (section 12) and of
  the *beitragsfreie Versicherungsleistung* (section 13), and — with surplus and
  *Bewertungsreserven* added — the capital the *Rentenfaktor* applies to (section 8).
- The conversion input is stated cleanly by NÜRNBERGER: **the contract value used for
  annuitisation includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a
  minimum guaranteed contract value stated in the general contract data** [S9]. In model terms:

  ```
  Kapital(Rentenbeginn) = max( garantiertes Vertragsguthaben,
                               Deckungskapital + Ueberschussguthaben + Bewertungsreserven )
  ```

- The *Zinsüberschuss* — the interest surplus — arises **when the insurer's investment income
  exceeds the *Rechnungszins***: "when investment income exceeds the calculation rate, the
  insurance company generates surpluses in the form of interest gains" [R24]. This is the direct
  statement that the *Rechnungszins* is the **hurdle rate** of the surplus mechanism, not merely a
  discount rate.

### 6. Überschussbeteiligung in the Aufschubphase

- ***Überschussbeteiligung*** is the **participation of policyholders in the surpluses of the
  insurance undertaking** [R24]. Its magnitude is, in an insurer's own contractual words, dependent
  on "many influences which are unpredictable and only limitedly controllable by the company, with
  the most important influencing factor being capital-market developments" [S8]. That disclaimer is
  why surplus is modelled as a **declaration** — an insurer-discretionary current assumption — and
  never as a guarantee.
- **The declaration instrument is an annual document**: the Konzern Versicherungskammer publishes
  its *"Überschussverteilung 2026"* as a standalone PDF [S15], and every German life insurer
  publishes an equivalent. **No rate from any such document was established** — gap 4.
- **Surplus systems in the accumulation phase.** Three are established, two in-scope designs and
  one successor design:
  1. ***Verzinsliche Ansammlung*** — the classic default. Declared surpluses are invested and bear
     interest, "similar to a classic capital life insurance or private pension insurance" [R24].
     The mechanics are explicit: **"the ongoing surplus portions are credited to the
     *Ansammlungsguthaben* and accrued with interest, with the interest credited at the end of each
     insurance year and upon termination of the insurance"** [R24]. The accumulation account is a
     **second, parallel account** to the *Deckungskapital*, with its own credited rate, settling at
     year end and at exit.
  2. ***Bonusrente* / *Bonussystem*** — declared surpluses buy **additional premium-free annuity**
     [R24]; in the payout phase the split is explicit (section 9).
  3. **Investment of surplus in an internal fund** — the successor design. Debeka: "surplus shares
     of the accumulation phase are invested in an internal fund and can enable additional
     benefits", and "fund holdings generally receive no *Überschussbeteiligung* from the earnings
     of Debeka's general *Sicherungsvermögen* before *Rentenbeginn*" [S12]. Guarantees on the
     general account, declared surplus on a fund — a **departure from the classic product**, and
     therefore a variation, not the representative design.
- ***Beitragsverrechnung*** — surplus applied to reduce the premium due — is the fourth system the
  German market uses. **No source in this corpus named it for this product** (gap 16).
- **Bewertungsreserven.** Under **§ 153 Abs. 3 VVG** policyholders participate **equally
  (*hälftig*)**, as restated by an insurer's own consumer information [S4] [R4]. Two
  product-specific consequences from the same source: the ***Rentenbeginn* is a key point for that
  participation**, and **participation continues during the payout phase**.
- **The four-component decomposition of surplus** — *Zinsüberschuss*, *Risikoüberschuss*,
  *Kostenüberschuss*, *Schlussüberschussanteil* — is **only partly established here**. The
  *Zinsüberschuss* is established directly ("when investment income exceeds the calculation rate …"
  [R24]); the other three were not named by any summary and are `[unverified]` (gap 17). They are
  the primary subject of the delib `kapitallebensversicherung` file, which shares this chassis.

### 7. Todesfallleistung before Rentenbeginn

- On death of the insured **during the *Aufschubzeit***, the contract pays a death benefit and
  ends. The corpus establishes **three distinct designs**, all in use [R24]:
  1. ***Beitragsrückgewähr*** — **"the insurer refunds all paid premiums after the death"**, with
     an optional extension: **"if the insured dies during the *Aufschubzeit*, repayment of the
     premiums plus the *Überschussbeteiligung* attributable to them can be agreed"**. So it comes
     in a bare form and a with-surplus form, and the choice is contractual.
  2. **Payment of the accumulated *Deckungskapital*** — "during the *Aufschubzeit*, the
     *Deckungskapital* accumulated up to that point is paid out".
  3. **A *Hinterbliebenenrente*** — survivors may receive, **depending on the contractual
     arrangement, a *Beitragsrückgewähr*, the accumulated capital, or a *Hinterbliebenenrente***.
     The survivor's annuity has its own GDV model condition set [S10] and is properly a rider.
- **The *Beitragsrückgewähr* is named in the GDV model conditions for this product** [S1] — the
  model wording's own term, not a marketing label.
- **The `max(...)` form is established for the unit-linked sibling, not for the classic product.**
  DEVK: the death benefit is "the fund value at the date of death, **but at least the sum of the
  premiums paid (*Beitragsrückgewähr*)**" [S19]. The classic analogue —
  `max(Deckungskapital, premiums paid)` — is the obvious counterpart, but **no classic-product
  document in this corpus stated it in that form**; it is `[unverified]` as the classic rule, and a
  representative design that adopts it must tag it `[std]`.
- **What the death benefit is *not*:** there is no separate sum insured. It is defined off the
  premiums paid or off the accumulated fund, never off an independently chosen *Versicherungssumme*
  [S19] [R24] — the structural difference from delib's `kapitallebensversicherung` and
  `risikolebensversicherung`.
- **Whether the benefit falls at the date of death or at the next policy anniversary, and whether
  the with-surplus form includes the *Ansammlungsguthaben* in full, were not established** — gap 18.

### 8. The Rentenfaktor

This is the mechanic the whole product turns on, and it is the best-evidenced thing in the file.

**Definition and arithmetic.** The *Rentenfaktor* **determines how much monthly annuity is
received per 10 000 € of accumulated capital** — "wie hoch die ausgezahlte monatliche Rente pro
10 000 Euro angespartem Vermögen ausfällt" [R24]. The arithmetic, as given: **capital of 100 000 €
with a *Rentenfaktor* of 25 yields 250 € per month**, computed as `100 000 / 10 000 × 25` [R24].
The factor 25 in that illustration is a **teaching example, not a market level** — see gap 3. In
model notation:

```
monthly_annuity = Kapital(Rentenbeginn) / 10 000 x Rentenfaktor
```

**Guaranteed at inception, on the tariff bases.**

- **The *garantierter Rentenfaktor* is fixed in the contract documents and rests on the
  *Rechnungsgrundlagen* as at the date of contract conclusion** [R24] — a guarantee given at issue
  about a conversion that will happen decades later.
- **The insurer applies a *Sicherheitsabschlag* in calculating it, which is why it comes out lower
  than the current factor** [R24].
- **The margin is quantifiable from one carrier.** CosmosDirekt: "the annuity factor determined at
  the beginning of the contract is calculated on the basis of a recognised mortality table
  (currently DAV 2004 R) and an underlying interest rate (**currently 0 percent p.a.**)" [S8]. A
  zero-percent interest basis, against a *Höchstrechnungszins* that has been positive throughout,
  is the *Sicherheitsabschlag* made concrete: the guaranteed factor is priced as though the insurer
  will earn nothing on the annuity fund.
- Allianz expresses the same guarantee as **"a minimum annuity"** available at inception [S13] —
  the *garantierter Rentenfaktor* stated as an amount rather than a factor.

**Current factor, and the comparison at Rentenbeginn.**

- **The *aktueller Rentenfaktor* is influenced by economic factors such as the interest level and
  the life expectancy of the insured person** [R24], and is recomputed on the bases in force when
  it is quoted.
- **Allianz states what "current" means operationally**: the calculation bases at *Rentenbeginn*
  "relate to the interest rate and mortality table that the company uses **at that time for
  immediately beginning annuities**" [S13]. The current factor is the carrier's then-current
  immediate-annuity tariff — which is why [S16] belongs in this file.
- **The rule at *Rentenbeginn* is a maximum of two factors.** Zurich: the guaranteed *Rentenfaktor*
  is carefully calculated, and **at the start of annuity payments a second *Rentenfaktor* is
  compared with it, the higher of the two being guaranteed for the annuity payment period** [S4].
  The consumer literature states the same rule from the other side: **the guaranteed factor is a
  floor and comes into play only if the current factor at *Rentenbeginn* is lower; otherwise the
  annuity is computed on the then-current factor** [R24]. In model notation:

  ```
  Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )
  ```

  This is a **guarantee with upside**, and a model that applies only the guaranteed factor
  understates the benefit whenever the current tariff is richer.

**Movement with the Höchstrechnungszins.** The factor moves with the *Rechnungszins* and with the
mortality basis, because those are the two things it is computed from [S8] [S13] [R24]. The
*Höchstrechnungszins* history therefore maps onto it: the thirty-year decline to 0,25 % [R7]
compressed guaranteed factors, and the 2025 increase to 1,00 % [R7] [R8] should have relieved that
compression for new business. **The magnitude was not established** — no search returned a level,
range or time series, not even from the rating house whose article asks "wie hoch ist er?" [R19].
See gap 3: a representative *Rentenfaktor* is the one parameter a delib worked example cannot
avoid choosing, and it will be `[std]`.

**Reduction of a factor: the Treuhänderklausel and § 163 VVG.**

- **Historically:** insurers could change guaranteed *Rentenfaktoren* on the basis of a
  ***Treuhänderklausel*** in the conditions, **with the approval of an independent external
  *Treuhänder***, where economic conditions deteriorated permanently and unexpectedly [R17].
- **Two explicit triggers**: an **unexpectedly strong increase in life expectancy**, requiring
  adjustment of the mortality tables, and a **sustainable reduction in capital-market returns**,
  permitting adjustment of the interest rate [R17].
- **Currently:** the clause **is used only in older contracts; today the guaranteed *Rentenfaktor*
  can be changed only on the basis of § 163 VVG** [R17] [R3].
- **The courts have narrowed it.** The **Landgericht Köln** held that **the low-interest phase is
  not a sufficient ground, because it must be assessed as entrepreneurial risk that cannot be
  passed on to policyholders** [R17]; consumer press reports that a subsequent reduction **can be
  unlawful** [R16]. **The case reference and decision date were not established** — gap 10.
- **It was a live commercial dispute at the market leader in 2021**: trade press of 4 February 2021
  reports Allianz's position that customers could not successfully object to an adjustment [R18].
- **Modelling consequence.** The guaranteed *Rentenfaktor* is a contractual guarantee with a
  narrow, contested statutory adjustment channel. A delib model treats it as **fixed for the life
  of the contract** and records § 163 VVG as a model risk rather than implementing it.

### 9. The Rentenphase

- The annuity in payment is **the sum of a *garantierte Rente* and an *Überschussrente***: the
  insurer sets a value at the start of the payout phase "composed of the *Garantierente* and a
  surplus share projected for the whole annuity period" [R20]. Only the guaranteed part is a
  promise.
- **Three *Überschussverwendung* systems exist in the payout phase**, and the choice is the
  policyholder's [R19] [R20] [R24]:

  | System | Mechanic |
  |---|---|
  | **konstante Rente** | The payout stays the same over the whole term. The insurer fixes a value at the start of the payout phase from the *Garantierente* plus a surplus share **projected for the whole annuity period**. In practice it can still fluctuate: **if the provider earns less than expected, the annuity falls** [R20]. |
  | **teildynamische Rente** | The annuity rises regularly by a **fixed percentage**, provided the insurer earns corresponding surpluses. It is **a combination of the constant and the dynamic system**: part of the expected surplus is used under the constant system and part under the dynamic system to form an additional annuity [R20] [R24]. |
  | **volldynamische (steigende) Rente** | The annuity **adjusts annually and flexibly to the actual surplus development** [R20]. It starts lowest and rises fastest. |

- The ***Bonusrente*** is the mechanism underneath the rising forms: "the ongoing surplus shares
  are used partly for an age-dependent *Überschussrente* and partly for an additional premium-free
  annuity (*Bonusrente*)" [R24]. The increment, once bought, is **premium-free and permanent** —
  which is what makes a *volldynamische Rente* ratchet rather than fluctuate.
- **The constant form is not actually constant.** Under it the annuity is set from a
  **projection**, and **if the insurer earns less than projected the annuity is reduced** [R20]. A
  model that treats the *konstante Rente* as a level guaranteed stream is wrong; only the
  *garantierte Rente* inside it is guaranteed.
- **Participation in *Bewertungsreserven* continues during the payout phase** [S4] [R4].
- ***Rentengarantiezeit***, established in detail [R17] [R24]: a guaranteed payment period
  beginning at *Rentenbeginn*; if the annuitant dies inside it, **the annuity continues to be paid
  to the survivors until the agreed years have expired** (worked illustration: a 10-year period,
  death after 6 years, **the spouse receives the remaining 4 years**). **Durations offered: 5, 10,
  15, 20, 25 or more than 30 years**; **typical durations 15 years for retirement ages 61–70 and
  10 years for 71 and above**; **most policyholders choose 10 to 20 years**. It is a selectable
  parameter with a floor at Allianz [S13] and a tariff-level feature carried in the product name at
  NÜRNBERGER [S9]. **It costs annuity**: on the corpus's own illustration — 200 € monthly premium
  over 30 years producing 573 € per month with no guarantee period — a 10-year guarantee costs
  **3 €** per month, a 20-year guarantee **15 €**, a 30-year guarantee **46 €** [R24], that is
  roughly 0,5 %, 2,6 % and 8,0 % of the annuity (arithmetic performed here on the source's own
  figures, offered as an order of magnitude, not a tariff).
- ***Beitragsrückgewähr* in the *Rentenbezugsphase*** — a refund on death after *Rentenbeginn* of
  premiums paid less annuity instalments received — **was not established by any source in this
  corpus** (gap 18) and must not be asserted downstream. What the corpus does establish for
  post-*Rentenbeginn* death is the *Rentengarantiezeit* [R24] and the survivor's-annuity rider
  [S10].
- **Payment timing.** The annuity is described throughout as **monthly** [S13] [R24]. **Whether it
  is payable in advance (*vorschüssig*) or in arrears was not established** (gap 19), despite being
  a first-order modelling parameter. A delib model adopts monthly-in-advance as a `[std]`
  convention with the gap stated beside it.

### 10. The Kapitalwahlrecht

- The ***Kapitalwahlrecht*** is the policyholder's right to take **the accumulated capital as a
  lump sum instead of the lifelong annuity** at *Rentenbeginn* [S12] [R6] [R21].
- It is exercised **at or before *Rentenbeginn***, and it is the third of the three things that
  happen at that boundary (section 2).
- **The notice period was not established.** The German market convention is a declaration a set
  period before *Rentenbeginn*, but **no document or search summary in this corpus named a period
  at any carrier** — gap 11. Downstream this is `[std]`.
- **The tax consequence of electing it is total, and it is established.** Electing the lump sum
  moves the contract from the ***Ertragsanteil*** regime of § 22 EStG [R5] to the **§ 20 EStG**
  regime [R6]:
  - **The *Halbeinkünfteverfahren* applies only to lump-sum payments and to multiple capital
    withdrawals under a payout plan; it does not apply to monthly annuity payments** [R6].
  - **It requires the "12/62 rule": the contract must have run at least 12 years and the payment
    must occur after completion of the 62nd year of life** [R6].
  - **Where the rule is met, half the *Ertrag* is taxable**; the other half is exempt [R6].
  - **The contract must be one in which the capital option cannot be exercised before 12 years
    from contract conclusion** for § 20 EStG to apply in this way [R6].
- Debeka states the annuity side of the same choice from the insurer's page: **if a lifelong
  monthly annuity is chosen at *Rentenbeginn*, only part of the payout is taxed — the
  comparatively low *Ertragsanteil*, depending on age at *Rentenbeginn*** [S12].
- **Modelling consequence.** The *Kapitalwahlrecht* is a **policyholder election at a single known
  date**, not a continuous option. In a reference implementation it is a model-point switch that
  changes the entire post-*Rentenbeginn* cash-flow shape from an annuity stream to a single
  payment, and the take-up rate is a behavioural assumption with **no public evidence in this
  corpus** (gap 20).

### 11. The Rechnungsgrundlagen: DAV 2004 R, generational, sex-distinct, unisex tariff

- **The mortality basis is DAV 2004 R.** CosmosDirekt names it in its own AVB: the *Rentenfaktor*
  is calculated "on the basis of a recognised mortality table (**currently DAV 2004 R**)" [S8].
- **DAV 2004 R is a *Generationentafel*** used for annuity insurance calculations in Germany
  [R13]; generation tables **contain mortality per birth cohort, including the expected future
  change in mortality** [R13] [R15] — the trend is inside the table.
- **Component structure** [R12]: a base table of second order; a base table of first order; a
  mortality trend of second order; a mortality trend of first order; and an age adjustment
  (*Altersverschiebung*) with a base table.
- **First against second order** [R12]: **first-order probabilities are used for premiums and
  reserves and carry safety margins relative to the second-order ("realistic") probabilities, in
  order to assess the risk prudently**; the **second-order base tables represent the best estimate
  of period mortality in 1999 for insured lives, as three-dimensional selection tables**.
- **Dates** [R13] [R14]: in use **since June 2004**, **intended for new business from 2005**, the
  DAV document itself dated **22 February 2005**; practitioner presentations of 16 August and
  14 September 2004 and a reinsurer's exposition of 27 October 2004 date the market's adoption.
- **The DAV reissued the derivation guideline on 28 June 2023** [R12] — nineteen years after first
  use and twenty-four after the 1999 base year. That the profession was still maintaining
  DAV 2004 R in 2023 is itself the evidence that no successor annuity table has displaced it.
- **A companion in-force table exists**: a 2004 presentation titled "DAV 2004 R und RBx" [R14],
  RBx being the *Rentenbestandstafel* for the existing annuity book as against new business. The
  corpus establishes the pairing and nothing more.
- **The table is not public and is not redistributed by delib.** delib cites it by name, ships a
  `[std]` proxy anchored so its own worked example reproduces exactly, and states the anchor in the
  `Data` docstring. A replacement must preserve the **generational structure** (a `q(x, cohort)`
  surface, not a period table), the **first-order margin over second order**, and the
  **age-adjustment convention** [R12] [R13].
- **Sex-distinct tables against a unisex tariff.** German annuity tables are constructed
  sex-distinctly while the tariff sold since *Test-Achats* must be unisex. **Neither half of that
  sentence was established by any search in this session**: no summary confirmed that DAV 2004 R is
  published by sex, and no summary touched the unisex rule, the ECJ case or the 21 December 2012
  German application date. Both are `[unverified]` here (gap 21); the unisex rule belongs to the
  delib cross-product reference library.

### 12. Rückkaufswert (§ 169 VVG)

- **The surrender right exists** and its value is governed by § 169 VVG [R1].
- **For unit-linked contracts** the *Rückkaufswert* is computed **as the *Zeitwert* of the
  insurance according to recognised rules of actuarial mathematics**, insofar as the insurer does
  not guarantee a particular benefit, and **the principles of the calculation must be stated in the
  contract** [R1]. For the classic contract the guaranteed benefit exists, so the *Zeitwert* clause
  is the boundary rather than the rule; **what the classic surrender value is computed as was not
  established at article level** (gap 12).
- **A deduction is permitted only if it is agreed, quantified (*beziffert*) and appropriate
  (*angemessen*)** — three cumulative conditions — and **a deduction for not-yet-amortised
  *Abschluss- und Vertriebskosten* is void (*unwirksam*)** [R1]. That is the statutory answer to
  *Zillmerung*: the front-loading may not be recovered from the surrendering policyholder as a
  named deduction.
- **The computed value may be reduced by a contractually agreed and appropriate *Stornoabzug*
  (*Rückkaufsabschlag*)**; the result is the **statutory minimum surrender value**, below which a
  contractually agreed value may not fall [R1]. **§ 169 Abs. 6 VVG permits the insurer, in defined
  cases, to reduce surrender values that are to be paid out** [R1] — a solvency valve, not an
  ordinary charge.
- **The five-year spreading of *Abschluss- und Vertriebskosten*** associated with § 169 Abs. 3 VVG
  was **not returned by any summary** and is `[unverified]`, even though § 165 VVG's own text refers
  to "§ 169 paragraphs 3 to 5" [R2] — which independently establishes that those paragraphs carry
  the calculation rules on which both the surrender value and the paid-up value are built. **No
  *Stornoabzug* percentage, surrender-value table or charge-recovery schedule was established at
  any carrier** (gap 12).

### 13. Beitragsfreistellung (§ 165 VVG)

- **The policyholder may at any time demand, for the end of the current insurance period, that the
  insurance be converted into a premium-free insurance, provided the agreed minimum insurance
  benefit is reached** [R2]. The right is statutory and unconditional apart from that threshold.
- **If the minimum benefit is not reached, the insurer must instead pay the surrender value
  attributable to the insurance, including profit shares, under § 169** [R2] — a small contract
  cannot be made paid-up; it is cashed out.
- **The premium-free benefit is calculated according to recognised principles of actuarial
  mathematics, using the calculation basis of the premium calculation, on the basis of the
  surrender value under § 169 paragraphs 3 to 5, and must be stated in the contract for each
  insurance year** [R2]. Three consequences: the paid-up value is **derived from the surrender
  value**; it uses the **premium basis**, not a current basis; and it must be **tabulated per
  insurance year in the policy document**.
- Applied to this product: **the policyholder always has the right to convert a running annuity
  contract into a premium-free annuity contract** [R2] — the contract does not lapse, it continues
  with a reduced guaranteed annuity. **The *Mindestversicherungsleistung* threshold was not
  established at any carrier** (gap 22) and will be `[std]`.
- **The difference from *Kündigung*** matters: *Beitragsfreistellung* keeps the contract, its
  guarantee vintage and its guaranteed *Rentenfaktor* alive on a reduced benefit; *Kündigung* ends
  it for the *Rückkaufswert* [R1] [R2]. Where old contracts carry a high legacy *Rechnungszins* and
  old guaranteed *Rentenfaktoren*, that difference is worth a great deal, and it is why paid-up
  conversion and lapse must be **separate decrements**.
- **Wiederinkraftsetzung** — reinstatement of a paid-up contract — appears in the corpus only as a
  Debeka specimen endorsement file name (`Muster-NachtragWiederinkraftsetzung…`). Its existence as
  a documented process is established at that level and nothing more.

### 14. Charges

The weakest area of the corpus.

- **The premium is split, with a portion "intended for risk and cost coverage" deducted before the
  *Sparbeitrag*** [S11]: charges are **premium-based deductions**, not asset-based ones, in the
  classic chassis.
- **Two Allianz figures, both from third-party analysis of a specimen quotation** [S13] [R23]: an
  **Abschlussprovision of 1 575 €**, and **in the BasisRente and RiesterRente variants total costs
  relative to the capital formed of at most 0,95 € per 100 €**. Both are `[unverified]` as
  representative levels; neither is for the Schicht-3 tariff.
- **§ 169 VVG forbids recovering unamortised acquisition costs as a named surrender deduction**
  [R1], which constrains how *Zillmerung* is expressed but not how it is charged.
- **Not established, at any carrier**: the *Abschluss- und Vertriebskosten* rate; the
  *Höchstzillmersatz* (the 25 ‰ of *Beitragssumme* ceiling introduced by the LVRG 2014 is
  `[unverified]` here and belongs to the cross-product reference library); the *Verwaltungskosten*
  in any form; the *Ratenzahlungszuschlag*; the payout-phase administration charge; and the
  *Effektivkosten* disclosure. See gaps 13 and 14. **Every charge figure in the delib product
  documents will therefore be `[std]`.**

### 15. Taxation

- **The annuity is taxed on the *Ertragsanteil* under § 22 EStG** [R5] [R24]. Payments from private
  annuity contracts, and from life contracts converted into a classic monthly *Leibrente*, fall
  under this regime, and **only the "Ertrag des Rentenrechts" is taxed** — the interest component
  contained in the annuity from the beginning of the payout phase, not the return of capital [R5].
- **The *Ertragsanteil* depends on the annuitant's age at *Rentenbeginn***; the earlier the annuity
  begins, the longer the expected duration and the **higher** the taxable fraction [R5] [R24].
  **At age 65 it is 18 %** [R5] — the only value on the statutory table this session established;
  every other age is `[unverified]` (gap 8).
- **Electing the *Kapitalabfindung* moves the contract to § 20 EStG** and the
  *Halbeinkünfteverfahren*, subject to the **12/62 rule** and to the condition that **the capital
  option cannot be exercised before 12 years from contract conclusion** [R6]. **Half the gain is
  taxable**, and the method applies **only to lump sums and payout-plan withdrawals, not to monthly
  annuities** [R6].
- **Contracts concluded before 1 January 2005 retain the half-income treatment of the lump sum, and
  annuity payments continue uniformly to be taxed on the *Ertragsanteil* basis** [R6]. The
  1 January 2005 boundary is the *Alterseinkünftegesetz* watershed: a German in-force book carries
  **two tax cohorts**.
- **The two regimes are why the *Kapitalwahlrecht* is an economically live choice**, not a
  formality: the annuitant compares 18 % of each annuity instalment taxed at the marginal rate [R5]
  against half of the total gain taxed once [R6].
- **Not established:** the rate applied to the taxable half (personal or flat), the
  *Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
  *Kleinbetragsrente* commutation threshold. See gap 23.

### 16. Decrements and policyholder behaviour

- **Mortality** in the accumulation phase pays the death benefit of section 7; in the payout phase
  it terminates the annuity. The pricing basis is DAV 2004 R first order [S8] [R12], the
  best-estimate basis DAV 2004 R second order [R12].
- **The two phases use the same table**, which is a German peculiarity worth stating: an annuity
  table is used to price a death benefit before *Rentenbeginn*, so that benefit is systematically
  **under**-reserved relative to a population basis — and the *Beitragsrückgewähr* design [R24]
  exists partly because it makes the mismatch immaterial, the benefit being the premiums rather
  than a sum insured.
- **Lapse (*Storno*)** produces the *Rückkaufswert* [R1]; **paid-up conversion** is a separate
  decrement producing a reduced benefit [R2]. They must not be modelled as one.
- **No lapse rate, no paid-up rate, no *Kapitalwahlrecht* take-up rate and no German life-market
  *Stornoquote* was established** (gap 20). Every behavioural assumption in the delib documents
  will be `[std]` and labelled a modeller's view.

### 17. Market context: the retreat from the classic tariff

- **The classic deferred annuity has been withdrawn from sale by several of the largest German
  writers.** Debeka "will no longer offer classical annuity insurance", confirmed by a company
  spokesperson [R22], and its own page states that the offer is now the newer variants with a
  flexible allocation between guaranteed and fund-based components [S12].
- **Debeka's replacement**: from **1 July 2016**, five tariff variants under the name **"Chance"**,
  the safest guaranteeing **0,5 % interest** and the riskiest **effectively a fund policy with no
  guarantees** [R22]. **Debeka was following, not leading: Allianz, Zurich and Generali had already
  stopped distributing classic annuity insurance** [R22].
- **Allianz's replacement is KomfortDynamik** [S13] [R23]: premiums split between the
  *Sicherungsvermögen* and a *Spezialfonds*; **guarantee levels of 60 %, 80 % or 90 % of the
  premiums paid** at *Rentenbeginn*, selectable, 80 % standard; and, at inception, "only modest
  guarantees" — the premium-retention level and **a minimum annuity** [S13]. The trade-press
  headline asks whether it is "noch immer eine Rentenversicherung" [R23].
- **Zurich, by contrast, still publishes a *Verbraucherinformation für Konventionelle
  Versicherungen* for the deferred annuity in the Fassung 01/2026** [S4], and CosmosDirekt still
  publishes AVB whose *Rentenfaktor* is fixed at inception on DAV 2004 R [S8]. **The two
  statements are in tension** with [R22]'s report that Zurich stopped distributing the classic
  annuity. The likely reconciliation — that the withdrawal was of a specific classic tariff family
  and not of the conventional chassis — **was not resolved** (gap 9), and it is why the delib
  representative design is a composite of a chassis rather than a currently-purchasable product.
- **The consequence for delib.** The classic deferred annuity is best described as **the German
  market's reference chassis** — the design every successor product is a modification of, and the
  design the large in-force book still runs on — rather than as a live new-business product. That
  is the role lifelib reference models are for, and it is the framing the product-spec adopts.

## Observed variation across insurers

The corpus supports **structural** variation tables. It does **not** support quantitative range
tables for the parameters that matter most — *Rentenfaktor* levels, charges, entry ages, premium
envelopes and surplus rates — because no search in this session returned a number for any of them
at any carrier. Where a row reads "not established", that is the finding, not an omission.

### Carriers in the corpus

| Carrier | Document(s) | Status of the classic deferred annuity |
|---|---|---|
| GDV (industry model wording) | [S1] [S2] [S3] [S10] | Model conditions maintained; 2021 edition seen; expressly non-binding [S2] |
| Zurich Deutscher Herold | [S4] [S5] [S6] [S7] [S16] [S17] | *Verbraucherinformation* published 2021, 2022 and **01/2026** [S4]; but reported among the carriers that stopped [R22] — unresolved, gap 9 |
| CosmosDirekt (Cosmos Leben, Generali) | [S8] | AVB LA 904 A published; vintage not established; Generali reported among those that stopped [R22] |
| NÜRNBERGER | [S9] | AVB for tariff NIR3301, *mit Rentengarantiezeit* |
| Debeka | [S11] [S12] | **Withdrawn.** Replaced from 1 July 2016 by five "Chance" variants [R22] [S12] |
| Allianz | [S13] | **Withdrawn.** Replaced by KomfortDynamik, a 60/80/90 % premium-guarantee hybrid [S13] [R22] [R23] |
| Mecklenburgische | [S14] | *Vertragsinformationen* for "Rente flex"; product feature not established |
| Konzern Versicherungskammer | [S15] | Annual *Überschussverteilung 2026*; rates not established |
| Stuttgarter | [S18] | *Allgemeine Informationen* pack dated 2020 |
| DEVK | [S19] | Unit-linked only; used for the death-benefit contrast |

### Death benefit before Rentenbeginn, and Rentenfaktor determination

| Item | Observation | Source |
|---|---|---|
| *Beitragsrückgewähr*, premiums only | named in the GDV model wording | [S1] [R24] |
| *Beitragsrückgewähr* plus attributable surplus | "can be agreed" — a contractual election | [R24] |
| Accumulated *Deckungskapital* | the alternative classic design | [R24] |
| *Hinterbliebenenrente* | own GDV model condition set — a rider | [S10] [R24] |
| `max(fund value, premiums paid)` | **unit-linked wording**; classic analogue `[unverified]` | [S19] |
| Guaranteed *Rentenfaktor* fixed at inception | yes | [S8] [R24] |
| Its mortality basis | **DAV 2004 R** | [S8] |
| Its interest basis | **0 % p.a.** at one carrier, at an unestablished vintage | [S8] |
| A *Sicherheitsabschlag* makes it lower than the current factor | yes | [R24] |
| Current factor = carrier's then-current immediate-annuity tariff | yes | [S13] |
| Rule at *Rentenbeginn* | **higher of the two** | [S4] [R24] |
| Typical level in € per 10 000 €, and its movement since 2025 | **not established** | gap 3 |

### Rentengarantiezeit, and the surplus systems

| Item | Observation | Source |
|---|---|---|
| Durations offered | 5, 10, 15, 20, 25, 30+ years | [R24] |
| Typical, retirement age 61–70 / 71+ | 15 years / 10 years | [R24] |
| Most commonly chosen | 10–20 years | [R24] |
| Cost (200 €/month, 30 years, 573 €/month base) | 10 y: −3 €; 20 y: −15 €; 30 y: −46 € per month | [R24] |
| Carried in the tariff name | NÜRNBERGER NIR3301 | [S9] |
| Policyholder-selectable with a floor | Allianz PrivatRente KomfortDynamik | [S13] |
| Accumulation: *verzinsliche Ansammlung* (*Ansammlungsguthaben*, interest at each year end and at exit) | established | [R24] |
| Accumulation: *Bonusrente* / *Bonussystem* | established | [R24] |
| Accumulation: surplus invested in an internal fund | established — Debeka's successor design | [S12] |
| Accumulation: *Beitragsverrechnung* | **not established** | gap 16 |
| Declared rates for any year | **not established** | gap 4 |
| Payout: *konstante Rente* | set from a whole-period projection; **falls if the insurer earns less** | [R20] |
| Payout: *teildynamische Rente* | rises by a fixed percentage if surpluses permit; part constant, part dynamic | [R20] [R24] |
| Payout: *volldynamische (steigende) Rente* | adjusts annually to actual surplus development | [R20] |
| Payout: *Bewertungsreserven* participation continues | yes | [S4] [R4] |

### Guarantee level at Rentenbeginn — classic against successor designs

| Design | Guarantee at *Rentenbeginn* | Source |
|---|---|---|
| Classic (this product) | *Sparbeiträge* accumulated at the *Rechnungszins*, ≥ 100 % by construction | [S11] |
| Debeka "Chance", safest variant (from 1 July 2016) | 0,5 % guaranteed interest | [R22] |
| Debeka "Chance", riskiest variant | none — effectively a fund policy | [R22] |
| Allianz KomfortDynamik | **60 %, 80 % or 90 % of premiums paid**, selectable, 80 % standard | [S13] [R23] |

### What the corpus supports as a representative design

1. A **single-life deferred annuity on the general account**, Schicht 3, against a level recurring
   premium over a fixed *Aufschubzeit* [S4] [S11].
2. A ***Deckungskapital* accumulating the *Sparbeitrag* at a contract-vintage *Rechnungszins***,
   the *Sparbeitrag* being the premium net of the risk and expense portions [S11]; the
   *Rechnungszins* a **model-point attribute**, not a global assumption [R7].
3. ***Verzinsliche Ansammlung*** as the accumulation-phase surplus system, with a separate
   ***Ansammlungsguthaben*** crediting interest at each year end [R24]; the credited rates `[std]`.
4. A ***Beitragsrückgewähr*** death benefit before *Rentenbeginn*, in the premiums-only form named
   by the GDV model wording [S1] [R24], with the *Deckungskapital* form available as a switch.
5. Conversion at *Rentenbeginn* of `max(guaranteed contract value, Deckungskapital +
   Ansammlungsguthaben + Bewertungsreserven)` [S9] at
   `max(garantierter Rentenfaktor, aktueller Rentenfaktor)` [S4] [R24], the guaranteed factor
   struck at inception on **DAV 2004 R** and a conservative interest basis [S8].
6. A payout phase of ***garantierte Rente* plus *Überschussrente***, monthly, with the three
   surplus systems selectable and **the constant system explicitly not level** [R20], and a
   ***Rentengarantiezeit*** of 10 to 20 years [R24].
7. A ***Kapitalwahlrecht*** at *Rentenbeginn* [R6] [R21], with the notice period and take-up rate
   `[std]`.
8. ***Rückkaufswert*** under § 169 VVG [R1] and ***Beitragsfreistellung*** under § 165 VVG [R2] as
   **separate decrements**, the paid-up value derived from the surrender value on the premium
   basis and tabulated per insurance year [R2].
9. ***Dynamik*** (*Anpassungsversicherung*) as a documented but parameter-less option [S4], off in
   the base run.
10. Taxation on the ***Ertragsanteil*** for the annuity, **18 % at age 65** [R5], and the
    ***Halbeinkünfteverfahren*** under the 12/62 rule for the *Kapitalabfindung* [R6].

Every number in that design that is not tagged above is `[std]`, for one reason: **the corpus
establishes the mechanics of this product thoroughly and its levels barely at all.**

---

## Gaps and caveats

1. **The research budget was exhausted after eighteen queries.** This file's `WebSearch` budget was
   shared across fourteen parallel researchers and ran out mid-session; the brief anticipated
   thirty to eighty queries and eighteen were available. The queries that *were* run covered:
   classic deferred-annuity AVB; the *Rentenfaktor* (twice); GDV *Musterbedingungen*; the
   *Höchstrechnungszins*; *Überschussbeteiligung* in accumulation and in payout; the
   *Treuhänderklausel*; DAV 2004 R; the *Ertragsanteil*; the *Kapitalwahlrecht*; § 169 VVG;
   § 165 VVG; Allianz; Debeka; the *Rentengarantiezeit*; the death benefit before *Rentenbeginn*;
   Zurich; NÜRNBERGER; CosmosDirekt. The queries that were **not** run, and would have been next:
   current *Rentenfaktor* levels and the Franke und Bornberg / Morgen und Morgen / Assekurata
   ratings; the 2025 and 2026 *Überschussbeteiligung* declarations; charge and *Effektivkosten*
   levels; entry-age, premium and *Aufschubdauer* envelopes; unisex and *Test-Achats*; the
   *Zuzahlung*; the *Kapitalwahlrecht* notice period; *Beitragsrückgewähr in der
   Rentenbezugsphase*; *Stornoquoten*; and twenty further named carriers (R+V, HDI, Alte
   Leipziger, LV 1871, Continentale, Swiss Life, ERGO, AXA, Barmenia, Hannoversche,
   Württembergische, Gothaer, Stuttgarter, Volkswohl Bund, Baloise, Universa, Signal Iduna,
   Provinzial, HUK-Coburg, Dialog). **Everything below follows from this one gap.** Nothing was
   written to fill it and no URL, figure or paragraph number was guessed.

2. **No clause-level text was established from any primary document.** Not one AVB paragraph
   number, section heading or sentence of contractual wording was returned. [S1] [S2] [S4]–[S7]
   [S9] [S11] are established as *documents that exist and address named topics*, and in three
   cases ([S8] [S9] [S11]) as documents whose summary returned one or two substantive sentences.
   **There is no § numbering anywhere in this file for any AVB, and none may be invented
   downstream.**

3. **No *Rentenfaktor* level, range or time series was established — at any carrier, for any
   year.** The only number in the corpus is the teaching illustration "*Rentenfaktor* 25 on
   100 000 € gives 250 € per month" [R24], which is arithmetic, not a market level. The rating
   house's own article "Was bedeutet der Rentenfaktor und wie hoch ist er?" [R19] returned no
   level, and the "Rentenfaktor-Check 2025" [R24] is titled as data and analysis but returned
   none. **Every *Rentenfaktor* downstream will be `[std]`**, anchored so the worked example
   reproduces exactly rather than presented as a market rate. That current factors "have moved
   with the *Höchstrechnungszins*" is directionally supported by the mechanics [S8] [S13] [R7] and
   is quantitatively `[unverified]`.

4. **No *Überschussbeteiligung* rate was established, for any year, at any carrier.** The corpus
   establishes the declaration document type and its 2026 vintage [S15] and nothing inside it: no
   *laufende Verzinsung*, no *Gesamtverzinsung*, no *Schlussüberschuss* rate, no
   *Bewertungsreserven* amount, no *Überschussrentensatz*. Every surplus rate downstream is
   `[std]` and must be labelled an insurer-discretionary current assumption.

5. **The CosmosDirekt AVB vintage is not established, and its "currently 0 percent p.a." clause is
   explicitly time-stamped.** [S8] reads "a recognised mortality table (**currently** DAV 2004 R)
   and an underlying interest rate (**currently** 0 percent p.a.)". The word *currently* means the
   figure is an as-at, and the as-at is unknown. Siblings in the same AVB series carry **11/2022**
   dates, so a vintage in or after 2022 is plausible; the LA 904 numbering is the oldest in the
   series, so an earlier vintage is equally plausible. **The hardest figure in the file has no
   date.**

6. **§ 163 VVG was not read at article level.** Its role as the operative adjustment channel is
   established from commentary [R3] [R17]; its paragraph structure, procedural conditions, trustee
   role and notice requirements are all `[unverified]`.

7. **The *Höchstrechnungszins* history is established only at its two most recent points.** 0,25 %
   before 2025 and 1,00 % from 1 January 2025 [R7] [R10] [R11], plus "the first increase since
   1994" [R7] and the DAV's 1,0 % recommendation for 2026 [R8]. The intermediate sequence — 4 %,
   3,25 %, 2,75 %, 2,25 %, 1,75 %, 1,25 %, 0,90 % — and every effective date in it is
   `[unverified]` here. A model point carrying a legacy *Rechnungszins* must cite the
   cross-product reference library, not this file.

8. **Only one value of the *Ertragsanteil* table was established:** 18 % at age 65 [R5]. Every
   other age is `[unverified]`, as is the precise statutory address of the table within § 22 EStG.

9. **Zurich's status is contradictory and unresolved.** [R22] reports Zurich among the carriers
   that stopped distributing classic annuity insurance before Debeka's 2016 withdrawal; [S4] is a
   Zurich *Verbraucherinformation für Konventionelle Versicherungen* for the deferred annuity in
   the **Fassung 01/2026**. Both cannot be read literally at once. The likely reconciliation —
   withdrawal of a specific classic tariff family rather than of the conventional chassis — **was
   not confirmed**, and the delib documents must not assert either reading.

10. **The Landgericht Köln *Rentenfaktor* decision has no case reference.** The holding — that the
    low-interest phase is entrepreneurial risk and not a ground for adjustment — is established
    from consumer material [R17] and corroborated at headline level by [R16]. **Case number,
    decision date, parties and appeal history are all unestablished.** No citation may be made
    beyond "a Landgericht Köln decision reported by [R17]".

11. **The *Kapitalwahlrecht* notice period was not established** at any carrier, including from the
    GDV's own consumer page on payout options [R21]. The brief asked for it specifically.
    Downstream it is `[std]`.

12. **§ 169 VVG paragraphs 3 to 5 were not read.** § 165 VVG's text refers to them [R2], which
    establishes that they carry the calculation rules for both the surrender value and the paid-up
    value; their content — including the five-year spreading of *Abschluss- und Vertriebskosten* —
    is `[unverified]`. No *Stornoabzug* percentage, surrender-value table or charge-recovery
    schedule was established at any carrier, and what the *classic* (as against unit-linked)
    surrender value is computed as, at article level, is likewise unestablished.

13. **The premium, duration and age envelope is entirely unestablished.** Minimum and maximum
    premium; single- versus recurring-premium market split; minimum and maximum *Aufschubdauer*;
    minimum and maximum entry age; minimum and maximum *Rentenbeginn* age. None was returned at
    any carrier. Every issue rule in the delib product-spec will be `[std]`.

14. **No charge parameter was established for this product at any carrier** — not the *Abschluss-
    und Vertriebskosten* rate, the *Höchstzillmersatz*, the *Verwaltungskosten* in any form, the
    *Ratenzahlungszuschlag*, the payout-phase administration charge, or the *Effektivkosten*. The
    only two figures in the corpus — an Abschlussprovision of 1 575 € and a maximum of 0,95 € per
    100 € of capital formed — come from third-party analyses of an Allianz specimen quotation for
    **Schicht-1 and Schicht-2** variants [S13] [R23] and are `[unverified]` as Schicht-3 levels.
    No *Produktinformationsblatt* and no *Basisinformationsblatt* (PRIIP-KID) for a classic
    deferred annuity appears in the corpus at all, although the brief listed both as target
    document types.

15. **The *Zuzahlung* was not established at all, and the *Dynamik* only as a heading.** The Zurich
    pack contains "Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung"
    [S4], which establishes that the option exists and has its own condition set — and nothing
    about its percentage, its basis, its underwriting or its termination rules. No source named
    the *Zuzahlung*. The brief asked for both.

16. **The *Beitragsverrechnung* surplus system was not established for this product.** Three
    systems are evidenced [R24] [S12]; the fourth, in which surplus is set against the premium
    due, was not named by any summary. Its absence here is a gap in the corpus, not evidence that
    it does not exist.

17. **The four-component surplus decomposition is only one-quarter established.** The
    *Zinsüberschuss* is established from its definition — surplus arises when investment income
    exceeds the *Rechnungszins* [R24]. The *Risikoüberschuss*, the *Kostenüberschuss* and the
    *Schlussüberschussanteil* were **not** named by any summary. They are the primary subject of
    the delib `kapitallebensversicherung` file, which shares this chassis; anything about them
    here must cite that file or be `[unverified]`.

18. **Death-benefit timing, composition and post-*Rentenbeginn* refund are unestablished.**
    Whether the benefit falls at the date of death or the next policy anniversary; whether the
    with-surplus *Beitragsrückgewähr* includes the whole *Ansammlungsguthaben*; whether the
    classic product uses the `max(Deckungskapital, premiums paid)` form the unit-linked wording
    uses [S19]; and, separately, the ***Beitragsrückgewähr in der Rentenbezugsphase*** — the
    refund of premiums less annuity instalments on death after *Rentenbeginn*, which the brief
    asked for and which **no source in this corpus mentions**. It must not be asserted downstream.
    What *is* established for post-*Rentenbeginn* death is the *Rentengarantiezeit* [R24] and the
    survivor's-annuity rider [S10].

19. **The annuity payment timing was not established.** Every source describes the annuity as
    monthly [S13] [R24]; **none states whether it is payable in advance or in arrears**. This is a
    first-order modelling parameter — it moves the annuity value by roughly half a month's
    interest and shifts every payout cash flow by one period. The model must adopt
    monthly-in-advance as an explicit `[std]` convention and state this gap beside it.

20. **No behavioural assumption is evidenced.** No lapse rate, no *Beitragsfreistellung* rate, no
    *Kapitalwahlrecht* take-up rate, no market *Stornoquote*, no annuitisation-versus-lump-sum
    split. All are `[std]` and all are the modeller's view.

21. **The sex-distinct table / unisex tariff pairing was not established at either end.** No
    summary confirmed that DAV 2004 R is published sex-distinctly, and no search touched the ECJ
    *Test-Achats* judgment, the German unisex application date, or the AGG. Both halves are
    `[unverified]` here; the unisex rule belongs to the delib cross-product reference library and
    must be cited from there.

22. **The *Mindestversicherungsleistung* threshold for *Beitragsfreistellung* was not
    established.** § 165 VVG makes the paid-up right conditional on it [R2] and no carrier's
    threshold was returned. It is a tariff parameter and will be `[std]`.

23. **The tax picture is incomplete beyond the two regimes.** Not established: the rate at which
    the taxable half of a *Kapitalabfindung* is charged (personal rate or flat rate), the
    *Solidaritätszuschlag*, the inheritance-tax treatment of the death benefit, and the
    *Kleinbetragsrente* commutation threshold. The two regimes themselves — § 22 EStG
    *Ertragsanteil* [R5] and § 20 EStG *Halbeinkünfteverfahren* under 12/62 [R6] — are
    well-corroborated.

24. **The corpus is carrier-thin and skewed to withdrawn products.** Nine carriers appear, of
    which **two — Allianz and Debeka — are evidenced principally by the products that replaced the
    classic tariff** [S12] [S13] [R22] [R23], and one — DEVK — appears only through a unit-linked
    document [S19]. The variation tables therefore describe **structural** variation reliably and
    **parameter** variation not at all.

25. **The GDV model conditions are non-binding and their edition history is only partly known.**
    "Diese Bedingungen sind unverbindlich" [S2]; use is optional [S3]. One edition is dated 2021
    by its file name [S2] and a sibling Riester model condition carries "Stand: 21.07.2025" [S3].
    The current edition date of the deferred-annuity model conditions themselves was **not
    established**, so nothing downstream may date [S1].

26. **Living texts.** § 169 VVG was reached through a commentary version dated **1 January 2016**
    [R1]; § 165, § 163, § 153 VVG and § 22, § 20 EStG were reached without any version date at all
    [R2]–[R6]. The DeckRV amendment is established as effective **1 January 2025** [R7] [R11] and
    the DAV's recommendation extends the 1,0 % rate to **2026** [R8]. The DAV 2004 R derivation
    guideline was reissued **28 June 2023** [R12]. Zurich's current pack is **Fassung 01/2026**
    [S4]; the Konzern Versicherungskammer declaration is **2026** [S15]; a Debeka AVB sibling is
    dated **1 July 2026** [S11]. **Check every article number and every figure for later amendment
    before relying on it.**
