# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/fondsgebundene_rentenversicherung.md`
(the citation ground truth for this product) and are **frozen — never renumber**. Unused ids
are normally omitted, leaving gaps; **this product has none.** All eighteen primary sources
S1–S18 and all twenty-six product-specific references R1–R26 are cited at least once by
`product-spec.md` or `technical-notes.md`, so the numbering below is unbroken. That is a
property of a small, deliberately-assembled corpus and not a sign of thoroughness: the reason
nothing was dropped is that nothing in the list is a document anyone read, so no entry failed
on inspection. Access date for all sources: **2026-08-29**. No sources were newly added at
drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before relying on a single line below.** Two limits applied
to this product at full strength, and both were absolute rather than partial.

1. **Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl`
   are refused with HTTP 403 at the egress gateway for every host outside a short
   package-registry allowlist. `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
   `bundesfinanzministerium.de`, `dejure.org`, `eur-lex.europa.eu`, `de.wikipedia.org` and
   every insurer host named below were tried in the course of building this library and every
   one was refused. **Not one *Bedingungswerk*, not one *Basisinformationsblatt*, not one
   *Produktinformationsblatt*, not one *Verbraucherinformation* was opened.**
2. **The session's `WebSearch` budget — 200 calls, shared across the ten delib products — was
   already exhausted when this product's research began.** Every search attempted for it
   returned the budget-exhausted response, so there was **no research channel of any kind**
   for this file: not even the weak one, search summaries, that the `kapitallebensversicherung`
   and `klassische_rentenversicherung` files had.

What follows, and it is applied without exception below: **every entry records
`Retrieved: no`**, with the reason. Where a document was corroborated by a search run for a
**sibling** delib research file, that is said explicitly and the corroboration is attributed to
the sibling rather than claimed here. No verbatim quotation is invented; German wording that
appears is a term of art, not a quotation. No URL, document number, edition, tariff code, page
count or publication date is guessed — where a URL is not available the entry says `URL: not
established`, and a canonical `gesetze-im-internet.de` form of a statutory paragraph is marked
`[unverified]`. The five URLs that do appear were returned by searches run for sibling files
and are attributed to them.

**A delib citation is therefore a pointer, not a certificate.** It names the instrument a claim
should be checked against; it does not assert that anyone checked it. The **mechanics** in the
product documents are common ground in German practice and are written without hedging. The
**levels** are almost entirely **[std]**: not one *Abschlusskostenquote*, not one
*Verwaltungskostensatz*, not one *Stückkosten* amount, not one *Effektivkostenquote* and not
one *Rentenfaktor* was established at any carrier.

---

## Primary product sources

(delib-fondsgebundene_rentenversicherung-s1)=

### S1 — GDV, *Musterbedingungen* for the fondsgebundene Rentenversicherung
- Publisher / doc type: Gesamtverband der Deutschen Versicherer e. V.; *Musterbedingungen* — non-binding model policy conditions from which member insurers derive their own *Allgemeine Versicherungsbedingungen*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted). The **document type** is established indirectly: the sibling delib research on `klassische_rentenversicherung` corroborated the GDV *Musterbedingungen* index and a model-conditions set for the *Rentenversicherung mit aufgeschobener Rentenzahlung*; a companion set for the fondsgebundene form is the ordinary structure of that index, and its title, edition and clause numbering are `[unverified]`
- Used for: the market-standard **clause inventory** the specification is organised around — that the insurer guarantees the number of *Anteileinheiten* and not their value; the *Beitragsverrechnung* order and the purchase of units at the *Anteilspreis* on a *Bewertungsstichtag*; the *Risikobeitrag* on the net amount at risk; the *garantierte Mindesttodesfallleistung* as one of the four death-benefit shapes; the *Beitragsdynamik* mechanic; and the structural interchangeability of German insurer wordings. **No clause text and no numeric parameter rests on it.**

(delib-fondsgebundene_rentenversicherung-s2)=

### S2 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", document 03101, edition 07/2024
- Publisher / doc type: DEVK Lebensversicherungsverein a. G.; *Kundeninformation* — the consolidated pre-contractual document carrying the AVB, the *Produktinformationsblatt* content and the consumer information in one file
- URL: `https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf` — **returned by a search run for the sibling delib research on `klassische_rentenversicherung`, and recorded there as its S19**; not a search result of this file's own
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: **the single best-evidenced fact in this corpus and the one the model's death benefit rests on** — that on death before *Rentenbeginn* the benefit is the fund value at the date of death **but at least the sum of the premiums paid**, i.e. the *Beitragsrückgewähr* shape `max(Fondsguthaben, Summe der gezahlten Beiträge)`. That is why `db_form = prem_return` is the composite, why `cum_prem_pp` is a state variable, and why the net amount at risk is positive early and vanishes later. Also cited for the recurring-premium form and the general design type. **Nothing else about the DEVK contract — charges, *Rentenfaktor*, fund range, option set, entry ages — is established**, and the document code and edition come from the URL's own filename.

(delib-fondsgebundene_rentenversicherung-s3)=

### S3 — Allianz Lebensversicherungs-AG, AVB and *Verbraucherinformation* for the fondsgebundene Rentenversicherung ("InvestFlex")
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart — the German market leader in life; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* with the matching *Verbraucherinformation*, *Produktinformationsblatt* and *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the design type, and the market leader's stated rule that the bases applied at *Rentenbeginn* are those the company uses **at that time for immediately beginning annuities** — carried in the specification's *Rentenfaktor* section beside [R22] and attributed to the sibling research that corroborated it. The product name "InvestFlex" is `[unverified]`. Also one of the eleven carriers behind the negative finding that **no charge level of any kind was established** [S3]–[S14].

(delib-fondsgebundene_rentenversicherung-s4)=

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Fondsgebundene Versicherungen"
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* — a consolidated pre-contractual document issued per product family and per *Fassung*, typically 40–50 pages
- URL: not established for the fondsgebundene series. The sibling delib research corroborated the **companion** series, "Verbraucherinformation für **Konventionelle** Versicherungen — Aufgeschobene Rentenversicherung", in four editions
- Retrieved: **no** — egress blocked; no search corroboration for the fondsgebundene series
- Used for: the ***Rentenfaktor* rule at *Rentenbeginn*** — that a second, current factor is compared with the guaranteed one and **the higher of the two applies**, which is the `max(rentenfaktor_guar(), rentenfaktor_curr())` the model implements and the reason the rule is described as a guarantee *with upside*. That statement comes from the corroborated **conventional** series and its transfer to the fondsgebundene form is an inference. The existence of a parallel fondsgebundene series is itself inferred from the companion's title naming itself "Konventionelle"; its title, edition and content are `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s5)=

### S5 — Alte Leipziger Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* plus *Tarifblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: one row of the specification's carrier table, and there **only negatively** — a large mutual understood to offer both a commission tariff and a *Nettotarif* on the same unit-linked chassis `[unverified]`, the pairing that would isolate what the *Abschlusskosten* do to the *Effektivkosten*. **Nothing is established: no tariff code, no charge rate, no fund list, no factor.**

(delib-fondsgebundene_rentenversicherung-s6)=

### S6 — LV 1871, AVB for the fondsgebundene Rentenversicherung ("MeinPlan")
- Publisher / doc type: Lebensversicherung von 1871 a. G., München; AVB, *Produktinformationsblatt*, *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the **option catalogue** as a mechanic — that German unit-linked contracts carry a *Zuzahlung* subject to a minimum, a *Teilentnahme* subject to a minimum and to a minimum remaining *Fondsguthaben*, a *Beitragsdynamik*, and a flexible *Rentenbeginn* — and, with [S13], the observation that real tariffs offer a fund range of 50–300 *Investmentfonds* and ETFs against the model's one. **Every level in those rows is `[unverified]` and every one is a [std] parameter in the model.** The product name "MeinPlan" is `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s7)=

### S7 — Stuttgarter Lebensversicherung a. G., AVB for a hybrid fondsgebundene Rentenversicherung ("FlexRente performance-safe")
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; AVB for a **hybrid** unit-linked annuity, plus *Basisinformationsblatt*
- URL: not established. The sibling delib research corroborated a different Stuttgarter document, establishing only that the carrier publishes pre-contractual information PDFs
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the **hybrid comparator** in the riders-and-options section — a *dynamisches Hybrid* in which premium and capital are reallocated periodically between the *Sicherungsvermögen*, a *Wertsicherungsfonds* and free funds to secure a chosen *Beitragsgarantie* — and, with [S8] and [S9], for the point that **delib's no-guarantee chassis is a real market form and not a simplification of the only form sold**. The product name is `[unverified]`; **no reallocation rule, guarantee level or charge is established** and none is implemented.

(delib-fondsgebundene_rentenversicherung-s8)=

### S8 — Volkswohl Bund Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Volkswohl Bund Lebensversicherung a. G., Dortmund; AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the second named carrier behind the **two-pot hybrid** entry in the guarantee taxonomy, so that the taxonomy rests on more than one carrier, and one row of the negative carrier table. **No parameter is established.**

(delib-fondsgebundene_rentenversicherung-s9)=

### S9 — WWK Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung with i-CPPI guarantee
- Publisher / doc type: WWK Lebensversicherung a. G., München; AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted). The carrier is named **from general knowledge rather than any search result**, and that is stated rather than hidden
- Used for: the **i-CPPI** entry in the guarantee taxonomy — exposure to the risky fund set per policy and continuously as a multiplier times the cushion between the policy value and the present value of the guarantee, the most efficient of the three technologies and the most path-dependent. It is the entry whose **exclusion** from the model needs the most explicit justification, which the specification and `model.md` give. **No algorithm, multiplier, floor or charge is established.**

(delib-fondsgebundene_rentenversicherung-s10)=

### S10 — Cosmos Lebensversicherungs-AG (CosmosDirekt), AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Cosmos Lebensversicherungs-AG (Generali group), Saarbrücken, sold direct as CosmosDirekt; *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*
- URL: not established. The sibling delib research corroborated by search the **classic** Cosmos AVB, tariff LA 904 A, recorded there as its S8
- Retrieved: **no** — egress blocked; no search corroboration for the fondsgebundene tariff
- Used for: **the conversion basis behind the whole *Rentenfaktor* derivation** — the corroborated statement that the annuity factor fixed at inception rests on a recognised mortality table (currently DAV 2004 R) and an underlying interest rate of **currently 0 percent p.a.** That zero rate is what the `[std]` factor `10 000 / (12 · T_eff(x))` is built on, and it is what makes the *Sicherheitsabschlag* concrete. The statement is about the carrier's **classic** tariff and its transfer to the fondsgebundene one is an inference, tagged as one wherever it is used. Also the direct-writer cost comparator that bounds the *Effektivkosten* range from below, with [S13] and [S18].

(delib-fondsgebundene_rentenversicherung-s11)=

### S11 — NÜRNBERGER Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB with a tariff code in the *NIR*/*N* series, plus *Verbraucherinformation*
- URL: not established. The sibling delib research corroborated the classic NÜRNBERGER AVB under tariff NIR3301, establishing the carrier's document naming convention
- Retrieved: **no** — egress blocked; no search corroboration for the fondsgebundene tariff
- Used for: one row of the carrier table, recording that the carrier publishes **per-tariff AVB** with codes in an `NIR`/`N` series — the German pattern that makes a tariff code worth recording when it can be established and worth omitting when it cannot. **No fondsgebundene tariff code is asserted anywhere in these documents**, because inventing one is the failure mode the retrieval conditions forbid.

(delib-fondsgebundene_rentenversicherung-s12)=

### S12 — Continentale Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("Rente Invest")
- Publisher / doc type: Continentale Lebensversicherung AG (Continentale Versicherungsverbund); AVB plus *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: one row of the negative carrier table, widening the carrier set behind the variation section. The product name "Rente Invest" is `[unverified]`. **No parameter is established.**

(delib-fondsgebundene_rentenversicherung-s13)=

### S13 — HDI Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("CleverInvest")
- Publisher / doc type: HDI Lebensversicherung AG (Talanx group); AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the **low-cost, ETF-capable** comparator beside [S10] and the *Nettotarife* of [S18] — the reason `std_low` and the `etf` fund path ship at all — and, with [S6], the 50–300 fund range against the model's single fund. The product name and the low-cost characterisation are both `[unverified]`; **no charge level is established**, which is the gap the whole `[std]` charge stack sits in.

(delib-fondsgebundene_rentenversicherung-s14)=

### S14 — Debeka Lebensversicherungsverein a. G., AVB for the fondsgebundene Rentenversicherung
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; *Bedingungswerk* in the carrier's `B LV` series
- URL: not established. The sibling delib research corroborated several Debeka *Bedingungswerke* (B LV 85, B LV 86, B LV 97) and the trade-press report that Debeka **discontinued its classic annuity tariff**
- Retrieved: **no** — egress blocked; no search corroboration for the fondsgebundene tariff
- Used for: **the market-structure fact in the specification's opening** — that Germany's largest life mutual by policy count withdrew its classic annuity tariff, which is what puts the unit-linked and hybrid forms at the centre of German new business. It is one of only two corroborated supports for the claim of dominance, the other being the supervisor's cost agenda [R10] [R11]; the claim itself carries `[unverified]` because no GDV new-business split was established [R25]. The Debeka fondsgebundene *Bedingungswerk* number, edition and content are `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s15)=

### S15 — *Basisinformationsblatt* (PRIIP-KID) for a fondsgebundene Rentenversicherung — document-type entry
- Publisher / doc type: each insurer, for each *Anlageoption* / product variant; *Basisinformationsblatt* under the PRIIPs Regulation [R8] — three pages, prescribed order and prescribed headings
- URL: not established for any fondsgebundene Rentenversicherung. The sibling delib research located **one** German PRIIP-BIB PDF, for an **endowment** — the wrong product, the right document type, and confirmation of the three-page format
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the **disclosure frame** the specification's cost section is written against — a summary risk indicator, the possible maximum loss, four graded performance scenarios, the costs the investor bears, and the *Reduction in Yield* per year, all shown at **three time points: one year, half the recommended holding period, and the end of it**, which for a 30-year *Aufschubzeit* is roughly years 1, 15 and 30. This is the document a delib product specification would most want and does not have: **no scenario return, no total-cost figure and no RIY value in these documents comes from an actual BIB**, which is why `reduction_in_yield()` is labelled a delib measure everywhere it appears.

(delib-fondsgebundene_rentenversicherung-s16)=

### S16 — *Produktinformationsblatt* / *Verbraucherinformation* — document-type entry
- Publisher / doc type: each insurer; the German pre-contractual information set required by § 7 VVG with the *VVG-Informationspflichtenverordnung* [R7]
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the second disclosure class the specification's cost section rests on, and the one that carries the figures PRIIPs does not — that the insurer must disclose the ***Abschluss- und Vertriebskosten* included in the premium as a euro amount**, must disclose the other costs, and must state the ***Effektivkostenquote*** in the quotation; and that such a document normally shows the guaranteed benefits (for this product, the *Rentenfaktor* and little else), the ongoing costs, the *Rückkaufswerte* by year and the *Modellrechnung*. **No instance was located and no figure is established**; the entry is also one of the eleven behind the negative charge-level finding.

(delib-fondsgebundene_rentenversicherung-s17)=

### S17 — *Standmitteilung* (annual statement) — document-type entry
- Publisher / doc type: each insurer, with a GDV model; *Jährliche Mitteilung zum Stand der Versicherung*
- URL: not established. The sibling delib research corroborated a **GDV Muster-Standmitteilung for the kapitalbildende Lebensversicherung, edition 02/2017**, establishing that the GDV publishes model statements per line
- Retrieved: **no** — egress blocked; no search corroboration for the fondsgebundene model
- Used for: **the model's state vector, and the definition of the *Fondsguthaben***. What an in-force German unit-linked policy reports — units held per fund, the *Anteilspreis* at the statement date, the resulting *Fondsguthaben*, premiums paid in the year, the current *Rückkaufswert* and the projected benefit at *Rentenbeginn* — is almost exactly the column list of `result_fund()`, and that correspondence is stated in `model.md` rather than left as coincidence. The existence of a fondsgebundene model statement is inferred from the corroborated endowment one and is `[unverified]`.

(delib-fondsgebundene_rentenversicherung-s18)=

### S18 — *Nettotarife* / *Honorartarife* (myLife and the net variants of full-range carriers)
- Publisher / doc type: myLife Lebensversicherung AG and the *Nettotarif* variants of full-range carriers ([S5], [S6], [S13] and others); AVB and *Basisinformationsblatt* of a commission-free tariff
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: **the `std_netto` charge scale and what its existence proves** — that a *Nettotarif* is the same unit-linked contract with the *Abschluss- und Vertriebskosten* removed from the tariff, the adviser being paid a fee by the client under a separate *Vergütungsvereinbarung*, so that **the difference between a gross tariff's reduction in yield and the same chassis's net one is the acquisition load**. That is the parameter this library most needs and cannot source, and the four-tariff comparison in the technical notes exists to display the gap rather than to quote a level. myLife's business model is `[unverified]`; **no net-tariff or gross-tariff RIY figure is established.**

---

## Regulatory and actuarial references (product research numbering)

(delib-fondsgebundene_rentenversicherung-r1)=

### R1 — VVG § 169, *Rückkaufswert*, and the *Zeitwert* branch
- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Retrieved: **no** — egress blocked. The substance was **corroborated by search in the sibling delib research** on `kapitallebensversicherung` and `klassische_rentenversicherung`, not here
- Used for: **the pivot of the whole product.** That for *fondsgebundene Versicherungen* the *Rückkaufswert* is the ***Zeitwert*** computed by recognised actuarial rules, which on a pure unit-linked contract with no insurer-given guarantee **is the *Fondsguthaben*** — so `claims(t, "LAPSE")` has no discounting, no *Rechnungszins*, no mortality basis and no second-basis *Mindestrückkaufswert* behind it. That the *angesetzte Abschluss- und Vertriebskosten* are spread **evenly over the first five contract years**, which is `alpha_spread_months = 60` and the sixty-month cliff the worked example turns on. And that a ***Stornoabzug*** is permissible only if *vereinbart*, *beziffert* and *angemessen* and **never for unamortised acquisition costs**, which is why `stornoabzug_pp(t)` is a flat rate on the fund and deliberately not a function of the unrecovered charge. The internal paragraph designation of the *Zeitwert* branch is **`[unverified]`** and no delib document cites a subsection number for it.

(delib-fondsgebundene_rentenversicherung-r2)=

### R2 — VVG § 168, *Kündigung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the policyholder's right to terminate a recurring-premium life contract **for the end of the current *Versicherungsperiode***, which on a monthly-premium contract is a short notice period. Paired with [R1] it is what makes *Storno* on a German unit-linked policy a near-frictionless exit at fund value, and it is the structural basis — not an observation — for the front-loaded and market-sensitive lapse shape the `[std]` `lapse_table.csv` carries and for the dynamic-lapse module. Paragraph number, notice period and any single-premium restriction are `[unverified]`.

(delib-fondsgebundene_rentenversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `klassische_rentenversicherung` and `kapitallebensversicherung`, including the paid-up formula for a conventional contract
- Used for: the right to demand conversion to a paid-up contract, and — the point the model turns on — that on a fondsgebundene contract **nothing is converted**: the units stay, premium payment stops, the *beitragsbezogene* charges stop with it, and the ***kapitalbezogene* charges, the *Stückkosten* and the *Risikobeitrag* continue by cancelling units**, so a paid-up policy decays. That is model point 7 exactly, and it is why the fund-based charge must cancel units rather than be netted out of the premium. The minimum *Fondsguthaben* below which insurers refuse *Beitragsfreistellung* is `[unverified]` and is a `[std]` parameter.

(delib-fondsgebundene_rentenversicherung-r4)=

### R4 — VVG § 163, *Anpassung der Prämie* / adjustment with a *Treuhänder*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated in the sibling delib research** on `klassische_rentenversicherung`
- Used for: the statutory channel through which a life insurer may adjust a contract where the calculation bases have changed permanently and unforeseeably, subject to an independent trustee's confirmation — **the only remaining route by which a *garantierter Rentenfaktor* can be reduced**, the contractual *Treuhänderklausel* being confined to older contracts [R22]. The model treats the guaranteed factor as fixed for the life of the contract and records § 163 as a model risk rather than implementing it. The paragraph number and the conditions' formulation are `[unverified]`.

(delib-fondsgebundene_rentenversicherung-r5)=

### R5 — VVG § 153, *Überschussbeteiligung* and the *Bewertungsreserven*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated in the sibling delib research** on `kapitallebensversicherung`
- Used for: the entitlement to a share of the surplus and of the *Bewertungsreserven* unless excluded by express agreement — and its particular application here, that a fondsgebundene contract's investment result belongs to the policyholder by construction, so its *Überschussbeteiligung* arises from the **risk and cost results only** and the *Bewertungsreserven* limb has almost nothing to attach to. It is the authority behind the model's stated omission of the surplus credit and behind the statement that the omission biases the projected *Fondsguthaben* downward. Whether an insurer may exclude participation on a unit-linked tariff is `[unverified]`.

(delib-fondsgebundene_rentenversicherung-r6)=

### R6 — VVG § 152, *Widerruf*, and §§ 7–8 VVG (pre-contractual information)
- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__152.html` · `https://www.gesetze-im-internet.de/vvg_2008/__7.html` — both `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: that § 7 VVG requires the terms and the *VVG-InfoV* information in text form before the policyholder is bound — the statutory hook under which the *Effektivkosten* disclosure sits [R7] — and that § 152 gives a life policyholder a cancellation period of 30 days `[unverified]`, with the amount repayable on a unit-linked contract tied to the **unit value at the date of cancellation** rather than being a full premium refund. delib does not project the window; it is absorbed into the year-1 lapse rate.

(delib-fondsgebundene_rentenversicherung-r7)=

### R7 — VVG-InfoV § 2 — cost disclosure, the *Effektivkosten* and the *Modellrechnung*
- Publisher: Bundesministerium der Justiz (*Verordnung über Informationspflichten bei Versicherungsverträgen*)
- URL: `https://www.gesetze-im-internet.de/vvg-infov/__2.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `kapitallebensversicherung`, which established the heading, the statutory basis and the introduction date
- Used for: the disclosure of the ***Abschluss- und Vertriebskosten* included in the premium as a euro amount** — not as a percentage, not netted into a yield; the ***Effektivkostenquote*** required in quotations from 1 January 2015 `[unverified]` following the LVRG [R13]; that **for a fondsgebundene contract the *Effektivkosten* must include the fund's own costs**, which is what makes the TER a policy parameter and why the model nets it off the return rather than ignoring it; and the *Modellrechnung* requirement, whose number of assumed rates and levels are `[unverified]`. It is also one of the two authorities for the statement that `reduction_in_yield()` **is not** the statutory figure.

(delib-fondsgebundene_rentenversicherung-r8)=

### R8 — PRIIPs Regulation (EU) 1286/2014 and the RTS, Delegated Regulation (EU) 2017/653 as amended
- Publisher: European Parliament and Council; European Commission
- URL: not established (EUR-Lex is among the blocked hosts)
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the requirement of a ***Basisinformationsblatt*** for every packaged retail and insurance-based investment product, a fondsgebundene Rentenversicherung being the paradigm German IBIP; and the RTS statement that performance scenarios are **derived from the underlying's own return history** rather than chosen by the insurer — which is why the `[std]` 5.00 % fund path is labelled a scenario and not a forecast and why **nothing this model produces may be compared with a PRIIPs scenario**. The regulation numbers, the amending regulation and the Category 2 / Category 4 assignment are all `[unverified]`.

(delib-fondsgebundene_rentenversicherung-r9)=

### R9 — BaFin *Fachartikel*, "PRIIPs-Verordnung: Wie Versicherer Verbraucher informieren" (2022)
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFinJournal)
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html` — recorded in the sibling delib research on `kapitallebensversicherung` as a search result; **not a search result of this file's own**
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: **the most precisely established regulatory fact available to this product**, and the frame of the specification's disclosure section: that a *Basisinformationsblatt* must carry a total risk indicator, the possible maximum loss, **four graded scenarios — *Stress*, *pessimistisch*, *moderat*, *optimistisch* — as annualised average returns in per cent**, the costs the investor bears and complaint information; that scenarios, total costs and the *Reduction in Yield* per year are shown at **three time points**, with costs split into one-off and ongoing; and that the *Effektivkosten* of a specimen contract must be stated, published on the insurer's website and provided before conclusion.

(delib-fondsgebundene_rentenversicherung-r10)=

### R10 — BaFin, Merkblatt 01/2023 (VA) on *wohlverhaltensaufsichtliche Aspekte bei kapitalbildenden Lebensversicherungsprodukten*
- Publisher: BaFin; published **May 2023** `[unverified]`
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html` — recorded in the sibling delib research; not a search result of this file's own
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: the supervisory frame this product's charge stack sits in — that such products must offer an appropriate ***Kundennutzen***; that *Effektivkosten* **differ considerably** between providers and products, with close examination of undertakings whose costs or intermediary remuneration are notably high; and that the manufacturer must formulate a ***Renditeziel*** achievable with sufficient probability, with a real return net of costs for retirement-provision products. It is why delib treats the charge level as a **supervised** rather than a free parameter and states its `[std]` stack as a design decision. **No numerical threshold was established** and none is quoted.

(delib-fondsgebundene_rentenversicherung-r11)=

### R11 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"
- Publisher: BaFin; annual supervisory risk-focus publication, consumer-protection chapter
- URL: `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html` — recorded in the sibling delib research; not a search result of this file's own
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: the single fact that **"Kosten von kapitalbildenden Lebensversicherungen" is a named focus risk in BaFin's 2026 agenda** — three years after the *Merkblatt* [R10], the supervisor still treats the charge level of this family as an open problem. With [S14] it is one of the two corroborated supports for the specification's market framing. **No text of the chapter is established.**

(delib-fondsgebundene_rentenversicherung-r12)=

### R12 — DeckRV — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Justiz / Bundesministerium der Finanzen (*Deckungsrückstellungsverordnung*)
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `kapitallebensversicherung` and `klassische_rentenversicherung`
- Used for: **the one anchor in the entire charge stack** — the *Höchstzillmersatz* of **25 ‰ (2,5 %) of the *Beitragssumme*** `[unverified]`, cut from 40 ‰ by the LVRG [R13], which is `alpha_rate` on `std_gross` and therefore the 1 800,00 € and the 30,00 € monthly instalment of the worked example. And the asymmetry that the *Höchstrechnungszins* — 1,00 % from 1 January 2025 `[unverified]` — **does not bind the accumulation phase of a pure fondsgebundene contract at all**, there being no guaranteed accumulation rate to cap, and reaches the product only through the *Rentenfaktor* and through hybrid designs. That asymmetry is the structural reason unit-linked new business grew through the low-interest decade.

(delib-fondsgebundene_rentenversicherung-r13)=

### R13 — LVRG 2014, *Lebensversicherungsreformgesetz*
- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given** — inventing one is exactly what the retrieval conditions forbid
- Retrieved: **no** — egress blocked; corroborated in outline by search in the sibling delib research
- Used for: the reform that **cut the *Höchstzillmersatz* from 40 ‰ to 25 ‰** [R12] and **introduced the *Effektivkosten* disclosure** in quotations from 1 January 2015 [R7] — the two facts the `[std]` acquisition charge and the cost-disclosure section rest on. All dates are `[unverified]`, and the 40 ‰ → 25 ‰ cut is corroborated only at the level of a secondary consumer page in a sibling file; the reported post-LVRG fall in *Abschlusskosten* is `[unverified]` and is not used.

(delib-fondsgebundene_rentenversicherung-r14)=

### R14 — MindZV, *Mindestzuführungsverordnung*
- Publisher: Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Retrieved: **no** — egress blocked; corroborated in outline by search in the sibling delib research
- Used for: the minimum share of each surplus source credited to policyholders, and specifically that for a unit-linked contract the relevant sources are the ***Risikoergebnis*** and the ***übriges Ergebnis*** only, the investment result never entering the insurer's *Rohüberschuss*. With [R5] it is the authority behind the model's decision to compute the risk result and credit none of it back. **The minimum percentages are `[unverified]`** and none is quoted.

(delib-fondsgebundene_rentenversicherung-r15)=

### R15 — VAG — *Sparteneinteilung*, asset congruence and the *Zuwendungen* rules
- Publisher: Bundesministerium der Justiz (*Versicherungsaufsichtsgesetz* 2016)
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: three things, all with `[unverified]` paragraph numbers. That Anlage 1 lists ***fonds- und indexgebundene Lebensversicherung* as a *Versicherungssparte* in its own right**. That assets covering unit-linked liabilities must be held **in the corresponding units** in a segregated *Anlagestock* and not in the general *Sicherungsvermögen* pool — so the unit liability and the unit assets move together exactly and **the model has no investment-mismatch term**, which is the single most consequential structural statement in `model.md`. And that the IDD-derived ***Zuwendungen*** rules govern whether an insurer may retain a *Kickback* out of a fund's TER, which the model sidesteps with a passive fund.

(delib-fondsgebundene_rentenversicherung-r16)=

### R16 — DAV 2004 R, *Sterbetafel für Rentenversicherungen*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `klassische_rentenversicherung`, including its derivation document and its generational character
- Used for: the **annuity** basis behind the *Rentenfaktor* — generational, per birth cohort, with first- and second-order versions — and therefore the second of the product's two mortality bases. It is what `rentenfaktor_table.csv` stands in for and what makes the derivation `T_eff` in the range 25–28 years plausible on a generational table. **DAV tables are DAV property, are not public and are not redistributed by this library**: the table is cited by name, a `[std]` proxy ships in its place, and what a replacement must preserve — a generational annuitant basis with a first-order margin — is stated in the `Data` docstring.

(delib-fondsgebundene_rentenversicherung-r17)=

### R17 — DAV 2008 T, *Sterbetafel für Lebensversicherungen mit Todesfallcharakter*
- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `kapitallebensversicherung`, which located the DAV derivation document by title
- Used for: the **death** basis on which the *Risikobeitrag* is priced — first order — and therefore the statement that **a German FRV carries two mortality bases at once** and that a model pricing the death charge on the annuity table misprices it. `mort_table.csv` is the `[std]` Gompertz proxy that stands in for it, anchored at `q(37) = 0.00080` so the worked example reproduces exactly; the table itself is cited and not shipped, and a replacement must preserve an insured-lives gradient and a first-order margin **above** best estimate.

(delib-fondsgebundene_rentenversicherung-r18)=

### R18 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025)
- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung*
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf` — recorded in the sibling delib research; not a search result of this file's own
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: the existence of a **profession-agreed standard method for PRIIP *Kategorie 4***, which is why the specification can say that two *Basisinformationsblätter* for economically similar products may show very different scenario returns — a guarantee-bearing or profit-participating contract's scenarios coming from the standard method, a pure unit-linked contract's from the funds' own history — and therefore why **no scenario return is cited anywhere in these documents**. **No content of the report is established.**

(delib-fondsgebundene_rentenversicherung-r19)=

### R19 — EStG § 22 — *Ertragsanteilsbesteuerung* of the annuity
- Publisher: Bundesministerium der Justiz (*Einkommensteuergesetz*)
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** on `klassische_rentenversicherung`
- Used for: that a private annuity arising from the conversion of a fondsgebundene contract is taxed on its ***Ertragsanteil***, a statutory percentage depending on the annuitant's age at *Rentenbeginn* — **18 % at 65**, every other age `[unverified]` and the table not reproduced. The point the specification draws from it is that the tax treatment is **identical** for a fondsgebundene and a classic annuity once in payment: the fund wrapper affects the accumulation phase's taxation, not the payout phase's. Nothing in the model computes tax; the rules enter only through the lapse shape and through the `kapitalwahl` reporting split.

(delib-fondsgebundene_rentenversicherung-r20)=

### R20 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalwahlrecht*, the 12/62 rule and the *Teilfreistellung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` `[unverified]`
- Retrieved: **no** — egress blocked. **Corroborated by search in the sibling delib research** as to the 12/62 rule and the half-income method
- Used for: **the behavioural driver the lapse assumption is shaped around** — that on a lump sum the taxable amount is the excess of the payment over the premiums paid, and that where the contract has run **at least twelve years and payment falls after completion of the 62nd year of age only half that gain is taxable**. That is the `lapse_tax_step` of ×2.5 in the policy year `max(13, 62 − entry_age + 1)`, and it is why keying the step on duration alone is a listed pitfall. Also for the ***Teilfreistellung*** specific to a fondsgebundene wrapper, commonly stated as 15 % `[unverified]`, and for the accumulation-phase point that inside the wrapper there is **no annual taxation of fund income, no *Vorabpauschale* and no taxable disposal on a *Fondswechsel*** — the product's central commercial argument against a direct fund holding.

(delib-fondsgebundene_rentenversicherung-r21)=

### R21 — InvStG — *Investmentsteuergesetz* and the *Teilfreistellung*
- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/invstg_2018/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: nothing quantitative. It is cited beside [R20] so that the 15 % *Teilfreistellung* figure is at least attached to the regime it derives from — the 2018 reform taxing the fund on certain German income and compensating the investor with a partial exemption graded by equity quota. **All percentages, thresholds and the interaction with the insurance wrapper are `[unverified]`**, and the specification says so where the figure appears.

(delib-fondsgebundene_rentenversicherung-r22)=

### R22 — The *Rentenfaktor* / *Treuhänderklausel* cluster (consumer and trade press, LG Köln)
- Publisher: Finanztip; versicherungenmitkopf.de; Versicherungswirtschaft-heute
- URLs: `https://www.finanztip.de/private-rentenversicherung/rentenfaktor/` · `https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung` · `https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor` — all recorded in the sibling delib research on `klassische_rentenversicherung`; **not search results of this file's own**
- Retrieved: **no** — egress blocked; corroborated by search **in the sibling file only**
- Used for: **the consumer definition the whole conversion section is built on** — that the *Rentenfaktor* is the monthly annuity per 10 000 € of accumulated capital, so 100 000 € at a factor of 25 yields 250 € a month, **the 25 being a teaching example and not a market level**, which is exactly the status the `[std]` 25,00 carries in the model. The `max(guaranteed, current)` rule beside [S4]. And the *Treuhänderklausel* history: that insurers could previously reduce a guaranteed factor with an independent trustee's approval on two triggers, that today the route is § 163 VVG [R4] alone, that the **Landgericht Köln** held the low-interest phase to be an insufficient ground, and that the market leader's position was publicly disputed in February 2021. **The LG Köln case reference, date and parties were not established** and no delib document cites a docket.

(delib-fondsgebundene_rentenversicherung-r23)=

### R23 — Rating houses and market studies: Franke und Bornberg, Morgen & Morgen, Assekurata
- Publisher: Franke und Bornberg GmbH; Morgen & Morgen GmbH; ASSEKURATA Assekuranz Rating-Agentur GmbH
- URL: not established for any fondsgebundene study. The sibling delib research corroborated the existence of Franke und Bornberg's *Rentenfaktor* and *Basisinformationsblätter* commentary and of Assekurata's 24th *Marktstudie*
- Retrieved: **no** — egress blocked; no search corroboration for any fondsgebundene study
- Used for: **a negative finding, twice.** These are the houses where German unit-linked cost and *Rentenfaktor* levels are actually published, and they are the documents this product most needed and did not have — the sibling research recorded that even the Franke und Bornberg article *titled* "Was bedeutet der Rentenfaktor und wie hoch ist er?" returned no level, range or table. **No figure from any of them is used anywhere in these documents**, and the entry is cited to say so rather than to support a claim. Also for the market fact that German AVB are structurally interchangeable because they follow the GDV skeleton [S1].

(delib-fondsgebundene_rentenversicherung-r24)=

### R24 — Consumer bodies and comparison portals
- Publisher: Stiftung Warentest (*Finanztest*); Verbraucherzentrale Bundesverband and the *Länder* *Verbraucherzentralen*; Verivox; CHECK24; Finanztip
- URL: not established for any fondsgebundene Rentenversicherung page
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: the same negative finding as [R23] — the secondary literature is normally the only public place where price points appear (a monthly premium, an *Effektivkostenquote*, a *Rentenfaktor*, a tariff comparison at a stated model point), and **nothing from any of them is cited**. It is recorded so a later reader knows where to look first, and it is one of the two references behind the statement that `reduction_in_yield()` **must never be quoted as a market figure**.

(delib-fondsgebundene_rentenversicherung-r25)=

### R25 — GDV statistics on German life new business and in-force by *Versicherungsart*
- Publisher: Gesamtverband der Deutschen Versicherer e. V.
- URL: not established. The sibling delib research corroborated the existence of the series "Die deutsche Lebensversicherung in Zahlen" and "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre"
- Retrieved: **no** — egress blocked; no search corroboration for any unit-linked breakdown
- Used for: the series that **would** establish the share of German life new business written as fondsgebundene Rentenversicherung — the market figure the specification's opening asserts and cannot source. The claim of dominance therefore carries `[unverified]` and rests on what is corroborated instead: the withdrawal of a classic tariff at a major carrier [S14] and the framing of the supervisor's cost agenda [R10] [R11]. **No number is taken from this entry.**

(delib-fondsgebundene_rentenversicherung-r26)=

### R26 — BGH case law on *Rückkaufswert*, *Kostenverrechnung* and *Stornoabzug*
- Publisher: Bundesgerichtshof
- URL: not established. **No case number, decision date or docket is given for any decision in this entry**
- Retrieved: **no** — egress blocked; no search corroboration (session search budget exhausted)
- Used for: recording that a long and well-known German line of authority exists — on *Zillmerung*, on the transparency of *Rückkaufswert* clauses before the VVG 2008 reform, on the validity of *Stornoabzug* clauses, and on the post-2008 rules — and that **no decision from it is cited**. Any statement in these documents about what a court has held on a *Rückkaufswert* clause carries `[unverified]` and no docket, and **nothing in the model rests on a court holding**.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **Every entry in that library
carries the same retrieval conditions as this file**, and none of the documents behind them
was retrieved either. Entries cited by the fondsgebundene Rentenversicherung documents:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the frame in which the projected cash flows would be discounted, and the statement that this library does not discount.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: contract boundaries and the standard formula, referenced and never applied.
- **REG-R3** — Richtlinie (EU) 2025/2, the Solvency II review: recorded as a live change to the valuation frame.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve a valuation layer would supply to `liability_cf`.
- **REG-R5** — VAG 2016 and Anlage 1: **fonds- und indexgebundene Lebensversicherung as a *Sparte* of its own**, which is why German statistics report it separately.
- **REG-R6** — VAG §§ 74–110: best estimate plus risk margin, and the shape of the liability this model's output feeds.
- **REG-R7** — VAG §§ 124 and 125, the *Anlagestock*: **the asset-congruence rule that removes the investment-mismatch term from the model.**
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the pricing frame the charge stack sits in.
- **REG-R9** — VAG § 139, *Überschussbeteiligung*: with [R5], why an FRV's surplus is a risk-and-cost result only.
- **REG-R11** — VAG §§ 141–143, *Verantwortlicher Aktuar* and *Treuhänder*: the office behind the § 163 adjustment route.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the rate that does **not** bind this product's accumulation phase.
- **REG-R15** — the *Höchstrechnungszins* rate history: the low-interest decade that unit-linked new business grew through.
- **REG-R16** — **DeckRV § 4, the *Höchstzillmersätze*: the cross-product carrier of the 25 ‰ cap that `alpha_rate` takes.**
- **REG-R17** — DeckRV § 5 Abs. 3, the *Zinszusatzreserve*: a general-account mechanic this product does not have, recorded to say so.
- **REG-R18** — MindZV: with [R14], the minimum allocation of the risk and cost results.
- **REG-R20** — LVRG 2014: the cross-product carrier of the 40 ‰ → 25 ‰ cut and the *Effektivkosten* introduction.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the 30-day window absorbed into the year-1 lapse rate.
- **REG-R24** — VVG § 153: the cross-product carrier of the *Überschussbeteiligung* entitlement.
- **REG-R25** — VVG §§ 154 and 155, *Modellrechnung* and *Standmitteilung*: what an in-force policy must be told, which is [S17]'s statutory basis.
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: the only route by which a guaranteed *Rentenfaktor* may now be reduced.
- **REG-R28** — **VVG §§ 165–170: the cross-product carrier of the *Zeitwert* branch, the five-year spreading, the *Kündigung* right and the *Stornoabzug* conditions.**
- **REG-R31** — VVG §§ 6, 7 and the VVG-InfoV: advice, information, cost disclosure and the *Effektivkosten*.
- **REG-R32** — **PRIIPs and the delegated technical standards: why the TER is a return item and why nothing here may be compared with a performance scenario.**
- **REG-R33** — IDD and § 34d GewO: the inducement rules behind the *Kickback* question.
- **REG-R34** — Unisex, EuGH C-236/09 (Test-Achats) and the AGG: why `sex` reaches neither the tariff nor the *Rentenfaktor*.
- **REG-R35** — BaFin Merkblatt 01/2023, *angemessener Kundennutzen*: the cross-product carrier of the supervisory cost agenda.
- **REG-R36** — the BGH line of authority: the cross-product carrier for the *Stornoabzug* prohibition, cited without a docket.
- **REG-R37** — GDV-Musterbedingungen and market practice: why insurer wordings are structurally interchangeable.
- **REG-R41** — EStG § 22 and § 55 EStDV, *Ertragsanteil*: the payout-phase tax treatment the *Kapitalwahlrecht* is compared against.
- **REG-R45** — **EStG § 20 Abs. 1 Nr. 6, the 12/62 rule: the reference library's statement that the tax threshold is the strongest single driver of German surrender behaviour, which is why `lapse_tax_step` exists.**
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*: the first-order / second-order distinction that makes the *Risikoergebnis* a number rather than zero.
- **REG-R48** — **DAV 2008 T: the death basis the *Risikobeitrag* is priced on, cited and not shipped.**
- **REG-R49** — **DAV 2004 R: the generational annuity basis behind the *Rentenfaktor*, cited and not shipped.**
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: the intended base for a user-supplied replacement decrement table, and the reason a population proxy overstates insured-lives claims.
- **REG-R53** — the German life market in numbers: the series that would size the unit-linked segment, and does not.
- **REG-R54** — HGB §§ 341–341o and RechVersV: the statutory-accounts layer this projection feeds and does not compute.
- **REG-R55** — IFRS 17 and the **Variable Fee Approach**: the measurement model a unit-linked contract falls into, referenced and not implemented.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional-standards frame.

---

## Provenance note

Extraction details — which fact was read from which document, the eighteen-section mechanics
account written from the author's knowledge of German practice, and the twenty-eight-item gaps
and caveats register — live in `_research/fondsgebundene_rentenversicherung.md`. That file is
the citation ground truth for the S# and R# numbering used here.

The caveats that most affect what these product documents can claim, in the order they bite:
**no document was retrieved and no search was run for this product**, so this corpus is weaker
than its two delib siblings, which at least had search summaries; **no charge level of any kind
was established at any carrier** — not one *Abschlusskostenquote*, not one
*Verwaltungskostensatz* in either form, not one *Stückkosten* amount, not one commission rate —
so the entire charge stack is `[std]` and its only anchor is the 25 ‰ *Höchstzillmersatz*
[R12], itself corroborated only at the level of a secondary consumer page in a sibling file;
**no *Rentenfaktor* level, range or time series was established anywhere**, so the 25,00 € per
10 000 € at 67 is derived arithmetic and not a market observation; **no *Basisinformationsblatt*
for a fondsgebundene Rentenversicherung was located**, so no performance-scenario return, no
total-cost figure and no *Effektivkostenquote* in these documents comes from an actual BIB;
**no lapse rate, paid-up rate or *Kapitalwahlrecht* take-up was established**, so every
behavioural assumption is `[std]`; **the *Beitragsrückgewähr* fact is single-sourced** [S2] and
the source is a search summary read by a sibling researcher rather than by this one; **the DAV
tables are cited and never shipped**, so both mortality bases in the model are `[std]` proxies;
**the internal paragraph structure of § 169 VVG is unverified**, so no delib document cites a
subsection number for the *Zeitwert* branch; **the Landgericht Köln *Rentenfaktor* decision and
the BGH *Rückkaufswert* line could not be identified**, so nothing here rests on a court
holding; and **every statute cited is a living text** — VVG, VVG-InfoV, DeckRV, MindZV, VAG,
EStG and InvStG all change, the PRIIPs RTS was reworked with effect from 1 January 2023
`[unverified]`, and the *Höchstrechnungszins* changed on 1 January 2025 `[unverified]` — so
every paragraph number and every date must be re-checked against the instrument before anything
in these documents is relied on.
