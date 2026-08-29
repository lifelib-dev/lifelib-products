# Fondsgebundene Rentenversicherung — research notes (Germany)

Research notes for the German **unit-linked deferred private annuity** — *fondsgebundene
Rentenversicherung* (FRV), the contract in which the accumulating capital is not a
*Deckungskapital* in the insurer's general account but a holding of *Anteileinheiten* (units) in
*Investmentfonds* selected by the policyholder, so that **the insurer guarantees the number of
units and not their value**; in which every charge is taken by cancelling units or by withholding
premium before units are bought; and in which the single hard guarantee given at inception is the
*Rentenfaktor* — a number of euro of monthly annuity per 10 000 € of *Fondsguthaben* — applied at
*Rentenbeginn* to whatever the fund is then worth.

This is the dominant German new-business savings form. It is also the product where the German
market's whole cost vocabulary is visible on one page, because PRIIPs forces it there: a
fondsgebundene contract has no *Rechnungszins* to hide charges inside, so the charge stack, the
fund's own *TER* and the *Effektivkosten* (reduction in yield) are the product.

**In scope.**

- The single-life, deferred, **Schicht 3** (unsubsidised private, third-layer) unit-linked annuity
  sold to individuals against a **level recurring monthly premium** (the *Sofortrente* and the
  single-premium form are noted where they differ), with an *Aufschubzeit* ending at a
  contractually fixed *Rentenbeginn*.
- The **unit / non-unit split**: *Fondsguthaben*, *Anteileinheiten*, *Anteilspreis*, and the
  *Beitragsverrechnung* by which a gross monthly *Beitrag* becomes units.
- The **charge stack** and its German names — *Abschluss- und Vertriebskosten*, beitragsbezogene
  and kapitalbezogene *Verwaltungskosten*, *Stückkosten*, the fund *TER*, *Kickbacks* /
  *Bestandsprovision* — and the *Effektivkosten* disclosed in the *Basisinformationsblatt*.
- The **Todesfallleistung** before *Rentenbeginn* in its four observed shapes, and the
  *Risikobeitrag* levied by unit cancellation on the net amount at risk.
- The in-force **options**: *Fondswechsel* (Shift and Switch), *Ablaufmanagement*, *Zuzahlung*,
  *Teilentnahme*, *Beitragsfreistellung*, *Beitragsdynamik*, *Kapitalwahlrecht*, the *Abrufphase*.
- The **Rentenfaktor** at *Rentenbeginn*, the guaranteed-versus-current comparison, and the
  *Treuhänder* adjustment clause.
- ***Rückkaufswert*** as a *Zeitwert* under § 169 VVG, *Storno* and the *Stornoabzug*.
- Taxation of the *Rentenphase* and of the *Kapitalwahlrecht*, and the accumulation-phase tax
  deferral that is the product's principal selling argument against a direct fund holding.

**Out of scope, and named here so the boundary is explicit.**

- **Hybrid and guarantee designs** — *statische* and *dynamische Hybride*, *Zwei-* und
  *Drei-Topf-Hybride*, **i-CPPI**, *Wertsicherungsfonds* — are named in section 13 and are
  **deliberately not implemented** by the delib model. They are the same unit-linked chassis
  wrapped in a path-dependent reallocation rule whose whole content is a guarantee mechanism; a
  deterministic gross best-estimate cash-flow projection cannot demonstrate a guarantee mechanism
  honestly, because the reallocation rule only does anything along paths the projection does not
  generate. Section 13 says exactly what would have to be added.
- **Indexgebundene Rentenversicherung / "Neue Klassik"** index participation — delib
  `indexpolice`. It shares the "insurer holds the assets, policyholder takes a formula" idea but
  is a general-account product with an *Indexpartizipation* bought out of the surplus, not a
  unit-linked one.
- **Fondsgebundene Basisrente (Rürup)** and **fondsgebundene Riester-Rente**. Both exist and are
  common — the Riester form is the reason i-CPPI was built in Germany at all, because Riester
  carries a **statutory 100 % *Beitragsgarantie*** — but they are delib `basisrente` and
  `riester_rente`, with their own subsidy, guarantee and payout rules.
- **bAV**: *fondsgebundene Direktversicherung*, *Pensionskasse*, *Pensionsfonds*. Out of the
  library.
- **Fondsgebundene Kapitallebensversicherung** (the endowment form, benefit at a fixed *Ablauf*
  rather than an annuity) and **fondsgebundene Risikoversicherung**. The accumulation mechanics
  are identical; only the terminal event differs.
- **Sofortbeginnende fondsgebundene Rentenversicherung** (unit-linked annuity in payment) — delib
  `sofortrente` owns the payout phase. This file carries the payout phase only as far as the
  *Rentenfaktor* conversion, which is where the FRV's own liability ends and the classic annuity
  begins.
- **Nettopolicen / Honorartarife** are in scope as a **charge variant**, not as a separate
  product: the same contract with the *Abschlusskosten* stripped out and a fee paid separately to
  the adviser. They matter here because they bracket the *Effektivkosten* range from below.
- **Fondssparpläne, ETF-Sparpläne and Fondsdepots** are not insurance and are out of scope, but
  they are the product's competitor and the reason the tax-deferral argument of section 16 exists.

These notes are the citation ground truth for the delib `fondsgebundene_rentenversicherung`
product documents: source ids **S1..S18** and **R1..R26** below are **frozen — never renumber**.
Unused ids are simply omitted downstream, leaving gaps, and `sources.md` records which ids are
absent and why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

Read this section before reading anything else in the file. It is the difference between what this
document is and what a reader will assume it is.

**No document listed in this file was retrieved, and no web search was run for it.** Two
independent limits applied, and both were absolute rather than partial.

**Limit 1 — direct HTTP egress is blocked.** An organisation network policy refuses `WebFetch` and
`curl` with HTTP 403 at the egress gateway for every host outside a short package-registry
allowlist. Every host that matters for this product was tried in the course of building this
library and every one was refused: `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `eur-lex.europa.eu`, `de.wikipedia.org`, and every
insurer host named below. **Not one PDF of a *Bedingungswerk*, not one *Basisinformationsblatt*,
not one *Produktinformationsblatt*, not one *Verbraucherinformation* was opened.**

**Limit 2 — the session's `WebSearch` budget was already exhausted when this file was begun.** The
budget of 200 calls was shared across the parallel researchers building the ten delib products and
was consumed by the regulatory and contract-law research and by the two products written first.
Every search attempted for this product returned the budget-exhausted response. **There was
therefore no research channel of any kind for this file** — not the weak one (search summaries)
that the `kapitallebensversicherung` and `klassische_rentenversicherung` files had.

What follows from that, exactly, and it is applied without exception below:

1. **Every source entry is a *known reference*, not a citation of a read document.** Each records
   `Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)`.
   Where a document was corroborated by search **in a sibling delib research file**, that is said
   explicitly, with the sibling's own id, and the corroboration is attributed to that file rather
   than claimed here. **Never `Retrieved: yes`.**
2. **No verbatim quotation is invented.** Nothing in this file is presented as the wording of an
   instrument or of a *Bedingungswerk*. Where German wording appears it is a **term of art** —
   *Fondsguthaben*, *Anteileinheiten*, *Beitragsverrechnung* — not a quotation, and the
   terminology table below says so.
3. **No URL, document number, edition, tariff code, page count or publication date is guessed.**
   Where a URL is not available the entry says `URL: not established`. Where a canonical
   `gesetze-im-internet.de` form of a statutory article is given it is marked `[unverified]`,
   because no search in this session returned it. Two URLs below are exceptions and are labelled
   as such: they were returned by searches run for the sibling files and are recorded there.
4. **`[unverified]` is used generously and keeps its normal meaning.** It is applied to **every**
   specific paragraph number, effective date, monetary amount, percentage, tariff level, product
   name and market figure in this file. It is **not** applied to the general shape of a mechanic
   that is common ground in German life-insurance practice — that the *Beitrag* is reduced by
   charges before units are bought, that charges in force are taken by cancelling units, that a
   *Rentenfaktor* converts capital into annuity — because tagging those would drown the signal.
   The rule that separates the two: **the moment a claim becomes specific and numeric, it carries
   `[unverified]` or it becomes `[std]`.**
5. **Uncertain numbers are `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — an *Abschlusskostensatz*, a *Verwaltungskostensatz*, a *Rentenfaktor*, a
   *Stornoquote*, a fund return — this file ships a **`[std]` value with a stated rationale and an
   argued plausible range**, and says on what arithmetic the value rests. A `[std]` number is
   honest. A `[S4]` number that no one read is not. Section 19 and the gaps register together
   record every figure that had to be handled this way, and it is most of them.

**The consequence for the reader.** The **mechanics** in sections 1–18 are the part of this file
that is load-bearing and the part that does not depend on having a PDF open: how a monthly premium
becomes units, in what order the charges bite, how a *Risikobeitrag* is levied by cancellation, why
the *Rückkaufswert* of a fondsgebundene policy is a *Zeitwert* and what that removes from the
calculation, what the *Rentenfaktor* guarantee actually promises. Those are written long and
precise, and they are correct as descriptions of German market practice. The **levels** are not
sourced and are not presented as if they were. A delib citation is a pointer to the instrument a
claim should be checked against; it is not a certificate that anyone checked it.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss, per the library's house rules. This product carries the largest vocabulary of the ten, and
much of it has no clean English equivalent because the German market invented the concepts.

| Term | Gloss |
|---|---|
| *fondsgebunden* | unit-linked: the benefit is expressed in units of an investment fund, not in euro |
| *Fondsguthaben* | fund credit — the euro value of the policy's units at a valuation date; the account value |
| *Anteileinheiten* / *Anteile* | units; the quantity the insurer guarantees, as distinct from their value |
| *Anteilspreis* / *Anteilwert* | unit price; the fund's *Rücknahmepreis* (redemption price) at the *Bewertungsstichtag* |
| *Ausgabepreis* / *Ausgabeaufschlag* | offer price / front-end load charged by the fund company on purchase |
| *Rücknahmepreis* | redemption price = net asset value per unit; the price at which policy units are normally bought and cancelled |
| *Bewertungsstichtag* | valuation date on which units are bought, cancelled or valued |
| *Beitrag* / *Bruttobeitrag* | premium / gross premium as billed to the policyholder |
| *Beitragsverrechnung* | the allocation of a gross premium: which deductions are taken, in what order, before the remainder buys units |
| *Anlagebeitrag* / *Sparbeitrag* | the part of the premium that actually buys units, after charges and the *Risikobeitrag* |
| *Risikobeitrag* | risk premium: the charge for the death cover, levied on the *riskiertes Kapital* |
| *riskiertes Kapital* | net amount at risk: death benefit less *Fondsguthaben*, floored at zero |
| *Abschluss- und Vertriebskosten* | acquisition and distribution costs — commission, underwriting, issue |
| *Zillmerung* / *Höchstzillmersatz* | financing acquisition costs against future premiums / the statutory cap on the costs so financed |
| *Verwaltungskosten* | administration charges; split into *beitragsbezogen* and *kapitalbezogen* |
| *beitragsbezogene Kosten* | premium-based charge: a percentage of each gross premium (actuarial *β*-Kosten) |
| *kapitalbezogene Kosten* / *Gammakosten* | fund-based charge: a percentage per annum of the *Fondsguthaben* (actuarial *γ*-Kosten) |
| *Stückkosten* | per-policy fixed charge, a euro amount per month or per year regardless of premium size |
| *Ratenzahlungszuschlag* | instalment loading for paying more often than annually |
| *TER* (*Gesamtkostenquote*) | the fund's own total expense ratio, borne inside the unit price and invisible in the policy ledger |
| *Kickback* / *Bestandsprovision* | trail commission paid by the fund company to the insurer out of the TER, and normally credited back to the contract |
| *Effektivkosten* / *Effektivkostenquote* | reduction in yield (RIY): all charges expressed as the annual percentage by which they reduce the contract's return |
| *Basisinformationsblatt* (BIB) | the PRIIPs key information document (PRIIP-KID) |
| *Produktinformationsblatt* (PIB) | the German pre-contractual product information sheet |
| *Verbraucherinformation* | the consolidated pre-contractual consumer information document |
| *Modellrechnung* | the statutory illustration of maturity values at prescribed assumed returns |
| *Todesfallleistung* | death benefit |
| *Beitragsrückgewähr* | return of premiums: a death benefit of at least the premiums paid |
| *garantierte Mindesttodesfallleistung* | a guaranteed minimum death benefit above the fund value |
| *Aufschubzeit* / *Aufschubdauer* | deferment period, inception to *Rentenbeginn* |
| *Rentenbeginn* | annuity commencement date; the boundary at which the fund is converted |
| *Abrufphase* | the window inside which the policyholder may bring the *Rentenbeginn* forward or defer it |
| *Rentenfaktor* | annuity factor: euro of monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *garantierter* / *aktueller Rentenfaktor* | the factor guaranteed at inception / the factor on the insurer's tariff at *Rentenbeginn* |
| *Treuhänder* / *Treuhänderklausel* | independent trustee / the clause permitting an adjustment of contract terms with the trustee's approval |
| *Rentengarantiezeit* | guaranteed annuity period: instalments continue to the beneficiary if the annuitant dies inside it |
| *Kapitalwahlrecht* | the option to take the capital as a lump sum instead of an annuity |
| *Fondswechsel* (*Shift* / *Switch*) | fund change: reallocating the existing *Fondsguthaben*, and/or redirecting future premiums |
| *Ablaufmanagement* | automatic phased de-risking of the fund holding in the years before *Rentenbeginn* |
| *Zuzahlung* | an additional single premium paid into an existing contract |
| *Teilentnahme* / *Entnahme* | partial withdrawal of the *Fondsguthaben* |
| *Beitragsdynamik* | contractual annual increase of the premium, with a corresponding benefit increase |
| *Beitragsfreistellung* | conversion to a paid-up contract; premiums cease, the fund stays invested |
| *Beitragspause* / *Stundung* | temporary suspension or deferral of premium payment |
| *Rückkaufswert* | surrender value |
| *Zeitwert* | current value: the § 169 VVG basis for a fondsgebundene surrender value |
| *Stornoabzug* | surrender deduction |
| *Storno* / *Stornoquote* | lapse / lapse rate |
| *Überschussbeteiligung* | profit participation; in an FRV it arises from risk and cost results, not investment return |
| *Schlussüberschussanteil* | terminal bonus |
| *Sicherungsvermögen* | the insurer's segregated general-account assets — where a hybrid's guaranteed pot sits |
| *Wertsicherungsfonds* | a fund with a contractual limit on its loss over a period, used as the middle pot of a three-pot hybrid |
| *Beitragsgarantie* | premium guarantee: the percentage of premiums paid guaranteed to be available at *Rentenbeginn* |
| *Deckungsrückstellung* | the statutory reserve; for a fondsgebundene contract it is essentially the unit reserve plus a non-unit part |
| *Rechnungsgrundlagen* | the pricing bases: mortality table, interest rate, cost loadings |
| *Rechnungszins* / *Höchstrechnungszins* | technical interest rate / its statutory maximum for new business |
| *Ertragsanteil* | the taxable fraction of an annuity instalment under § 22 EStG |
| *Teilfreistellung* | the partial exemption of fund income under the *Investmentsteuergesetz* |

---

## Primary sources

Eighteen known references to primary product documents. **None was retrieved and none was
corroborated by a search run for this file** (see the retrieval-conditions section). Two entries —
[S2] and [S4] — carry a URL that a search returned during the sibling delib research and that is
recorded in that sibling file; those two are the only URLs in this section, and they are attributed
to the sibling rather than claimed here. Every other entry says `URL: not established`.

Each entry answers two questions honestly: **does a document of this kind exist for this product,
and what does that kind of document establish?** Where a product name or tariff code is given it is
tagged `[unverified]` — it is the author's recollection of the German market, not a search result.

### S1 — GDV, Musterbedingungen for the fondsgebundene Rentenversicherung

- Publisher: Gesamtverband der Deutschen Versicherer e. V. (GDV)
- Doc type: *Musterbedingungen* — non-binding model policy conditions published by the industry
  association for a line of business, from which member insurers derive their own *Allgemeine
  Versicherungsbedingungen* (AVB)
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted). The
  **existence and the document type** are established indirectly: the sibling delib research on
  `klassische_rentenversicherung` corroborated by search both the GDV *Musterbedingungen* service
  index and a specific model-conditions set for the *Rentenversicherung mit aufgeschobener
  Rentenzahlung*, recorded there as S1–S3. A companion set for the **fondsgebundene** form is the
  ordinary structure of that index; **its exact title, edition and clause numbering are
  `[unverified]`**.
- Content — what a GDV *Musterbedingung* for this line establishes, and why it is the right first
  source: it is the **skeleton every German insurer's AVB for the product follows**, clause order
  included, which is why insurer wordings across the market are structurally interchangeable even
  where the numbers differ. The clauses a model needs are, in the order they normally appear:
  what benefits are provided (annuity from *Rentenbeginn*, death benefit before it); how the
  *Beitrag* is applied (*Beitragsverrechnung*, the deduction of costs, the purchase of
  *Anteileinheiten* at the *Anteilspreis* on a *Bewertungsstichtag*); how the *Fondsguthaben* is
  determined; what happens on death before and after *Rentenbeginn*; the *Rentenfaktor* and the
  guaranteed-versus-current rule; the policyholder's rights to *Fondswechsel*, *Zuzahlung*,
  *Teilentnahme*, *Beitragsfreistellung* and *Kündigung*; the *Rückkaufswert* and any
  *Stornoabzug*; the *Überschussbeteiligung*; and the *Anpassungsklausel*. **No clause text and no
  numeric parameter is established here.** The delib documents use this entry as the statement
  that a market-standard clause inventory exists, not as authority for any clause's content.

### S2 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", document 03101, edition 07/2024

- Publisher: DEVK Lebensversicherungsverein a. G.
- Doc type: *Kundeninformation* — the consolidated pre-contractual customer information document
  for a unit-linked annuity, carrying the AVB, the *Produktinformationsblatt* content and the
  consumer information in one file
- URL: `https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf`
  — **this URL was returned by a search run for the sibling delib research on
  `klassische_rentenversicherung` and is recorded there as its S19.** It is not a search result of
  this file's own.
- Retrieved: no — egress blocked; corroborated by search **in the sibling file only**, not here.
- Content: the **single best-evidenced fact in this whole corpus**, and it is exactly on point for
  this product. The sibling research established from the search summary of this document that, on
  death **before** *Rentenbeginn*, the benefit is **the fund value at the date of death but at
  least the sum of the premiums paid** — the *Beitragsrückgewähr* form of the death benefit, in
  its `max(Fondsguthaben, Summe der gezahlten Beiträge)` shape. That is one of the four death
  benefit shapes catalogued in section 6, and it is the one delib adopts as representative,
  precisely because it is the only one with corroboration anywhere in the delib corpus. The
  document code **03101** and the edition **07/2024** come from the URL's own filename and are
  recorded as such. **Nothing else about the DEVK contract — its charges, its *Rentenfaktor*, its
  fund range, its option set, its entry ages — is established.**

### S3 — Allianz Lebensversicherungs-AG, AVB and *Verbraucherinformation* for the fondsgebundene Rentenversicherung ("InvestFlex")

- Publisher: Allianz Lebensversicherungs-AG, Stuttgart — the German market leader in life
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*, plus the matching
  *Verbraucherinformation*, *Produktinformationsblatt* and *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the market leader's unit-linked annuity is sold under the product name **"InvestFlex"**
  `[unverified]`, within the *PrivatRente* family whose classic and index members the sibling
  delib research covers (Allianz *KomfortDynamik* and *IndexSelect*). Recorded because **any
  representative German FRV design has to be checkable against the largest writer's wording**, and
  because Allianz is the carrier at which the *Treuhänderklausel* dispute over the *Rentenfaktor*
  was publicly live in 2021 [R22]. **No clause, charge, factor or age limit of this contract is
  established here**; every Allianz figure in the delib product documents is `[std]` or comes from
  the sibling files' own corroborated entries.

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Fondsgebundene Versicherungen"

- Publisher: Zurich Deutscher Herold Lebensversicherung AG
- Doc type: *Verbraucherinformation* — a consolidated pre-contractual information document issued
  per product family and per *Fassung* (edition), typically 40–50 pages
- URL: not established for the fondsgebundene series. The sibling delib research corroborated by
  search the **companion** series, "Verbraucherinformation für **Konventionelle** Versicherungen —
  Aufgeschobene Rentenversicherung", in four editions (*Fassung* 01/2021, 01/2022, 01/2026 and a
  *Konsortial* variant), recorded there as its S4–S7.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene series
- Content: the title of the corroborated companion series — "für **Konventionelle**
  Versicherungen" — is itself the evidence that a **parallel fondsgebundene series exists at the
  same carrier**: a document that has to name itself "conventional" does so to distinguish itself
  from the unit-linked one. That inference is recorded as an inference and the parallel document's
  title, edition and content are `[unverified]`. The **value of the document type** is high and is
  why it is listed: a *Verbraucherinformation* of that length is the one German document class that
  states, in one place, the benefit definitions, the *Beitragsverrechnung*, the cost clauses, the
  *Rentenfaktor* rule, the option catalogue and the *Rückkaufswert* rule — the exact inventory a
  product-spec needs. The sibling file's corroborated Zurich material also establishes the
  **conventional carrier's *Rentenfaktor* rule** — that at *Rentenbeginn* a second factor is
  compared with the guaranteed one and **the higher of the two applies** — and that rule is
  carried over here in section 9 as market practice, tagged to the sibling's evidence rather than
  to a fondsgebundene document.

### S5 — Alte Leipziger Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung* plus *Tarifblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: Alte Leipziger is one of the carriers a German broker market treats as a reference point
  for **fund range and option flexibility** in unit-linked pensions, and one of the few large
  mutuals offering both a commission tariff and a **Nettotarif** (fee-based, *Abschlusskosten*
  stripped out) on the same product chassis `[unverified]`. That pairing is the cleanest available
  demonstration of what *Abschlusskosten* do to the *Effektivkosten*, which is why the carrier is
  listed. **No tariff code, charge rate, fund list or factor is established.**

### S6 — LV 1871 (Lebensversicherung von 1871 a. G.), AVB for the fondsgebundene Rentenversicherung ("MeinPlan")

- Publisher: Lebensversicherung von 1871 a. G., München
- Doc type: AVB, *Produktinformationsblatt*, *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: LV 1871 sells its unit-linked pension under the product name **"MeinPlan"**
  `[unverified]`, a *Schicht 3* fondsgebundene Rentenversicherung with a *Fondsauswahl* including
  ETFs and a *Nettotarif* variant `[unverified]`. Recorded as a mid-sized specialist comparator
  for the **option catalogue** — *Zuzahlung*, *Teilentnahme*, flexible *Rentenbeginn* — which is
  the dimension on which German unit-linked contracts differ most and the one section 8 has to
  bound. **No parameter is established.**

### S7 — Stuttgarter Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung with guarantee ("FlexRente performance-safe")

- Publisher: Stuttgarter Lebensversicherung a. G.
- Doc type: AVB for a **hybrid** unit-linked annuity, plus *Basisinformationsblatt*
- URL: not established for the fondsgebundene product. The sibling delib research corroborated by
  search a different Stuttgarter document, "Allgemeine Informationen zu einem
  Altersversorgungssystem" (its S18), which establishes only that the carrier publishes
  pre-contractual information PDFs.
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: recorded as the **hybrid comparator**. The Stuttgarter markets its guarantee-bearing
  unit-linked pension under the name **"FlexRente performance-safe"** `[unverified]`, a design
  belonging to the *dynamische Hybride* family of section 13, in which the premium and the
  accumulated capital are reallocated periodically between the *Sicherungsvermögen*, a
  *Wertsicherungsfonds* and free funds so as to secure a chosen *Beitragsgarantie*. It is listed
  to make the point that **the delib model's no-guarantee chassis is a real market form and not a
  simplification of the only form available** — both are sold, and the guarantee is an option with
  a price, not an inherent feature. **No reallocation rule, guarantee level or charge is
  established.**

### S8 — Volkswohl Bund Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Volkswohl Bund Lebensversicherung a. G., Dortmund
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a broker-channel carrier associated in the German market with **two-pot hybrid**
  designs sold alongside a pure fondsgebundene tariff `[unverified]`. Listed as a second hybrid
  comparator so that section 13's taxonomy rests on more than one named carrier. **No parameter is
  established.**

### S9 — WWK Lebensversicherung a. G., AVB for the fondsgebundene Rentenversicherung with i-CPPI guarantee

- Publisher: WWK Lebensversicherung a. G., München
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: WWK is the German carrier most closely identified with the **i-CPPI** (individual
  Constant Proportion Portfolio Insurance) implementation of a unit-linked guarantee, marketed
  under a *Protect* product name `[unverified]`. It is not on the insurer list in this file's own
  brief and is named from general knowledge of the market rather than from any search result;
  that is stated here rather than hidden. It is recorded because section 13 must be able to name
  the three guarantee technologies — static hybrid, dynamic hybrid, i-CPPI — against a real
  carrier each, and because the i-CPPI form is the one whose exclusion from the delib model needs
  the most explicit justification. **No algorithm, multiplier, floor definition or charge is
  established.**

### S10 — Cosmos Lebensversicherungs-AG (CosmosDirekt), AVB for the fondsgebundene Rentenversicherung

- Publisher: Cosmos Lebensversicherungs-AG (Generali group), Saarbrücken; sold direct as
  CosmosDirekt
- Doc type: *Allgemeine Bedingungen für die fondsgebundene Rentenversicherung*
- URL: not established. The sibling delib research corroborated by search the **classic** Cosmos
  AVB, tariff **LA 904 A** (its S8), together with that document's statement that the annuity
  factor fixed at inception rests on a recognised mortality table (**currently DAV 2004 R**) and
  an underlying interest rate of **currently 0 percent p.a.**
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: recorded for two reasons. First, as the **direct-writer cost comparator**: a
  no-commission direct channel is the low end of the *Effektivkosten* range and bounds it from
  below along with the *Nettotarife*. Second, because the sibling's corroborated statement of the
  **conversion basis — DAV 2004 R at 0 % p.a.** — is the single most useful number in the delib
  corpus for calibrating a *garantierter Rentenfaktor*, and section 9 uses it as the basis of the
  `[std]` factor. That statement is about the carrier's **classic** tariff; applying it to the
  fondsgebundene tariff is an inference, and it is tagged as one wherever it is used.

### S11 — NÜRNBERGER Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung

- Publisher: NÜRNBERGER Lebensversicherung AG
- Doc type: AVB with a tariff code in the *NIR*/*N*-series, plus *Verbraucherinformation*
- URL: not established. The sibling delib research corroborated by search the classic NÜRNBERGER
  AVB for the *Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit* under
  **tariff NIR3301** (its S9), which establishes the carrier's document naming convention.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: listed as a full-range carrier publishing per-tariff AVB, which is the German pattern
  that makes tariff codes worth recording when they can be established and worth omitting when
  they cannot. **No fondsgebundene tariff code is asserted here** — inventing one would be exactly
  the failure mode the retrieval-conditions section forbids.

### S12 — Continentale Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("Rente Invest")

- Publisher: Continentale Lebensversicherung AG (Continentale Versicherungsverbund)
- Doc type: AVB plus *Produktinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a broker-channel mutual whose unit-linked pension is sold under a *Rente Invest* name
  `[unverified]`. Recorded to widen the carrier set behind the variation table in section 20.
  **No parameter is established.**

### S13 — HDI Lebensversicherung AG, AVB for the fondsgebundene Rentenversicherung ("CleverInvest")

- Publisher: HDI Lebensversicherung AG (Talanx group)
- Doc type: AVB plus *Basisinformationsblatt*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: HDI's unit-linked pension is sold under the name **"CleverInvest"** `[unverified]` and
  is one of the tariffs the German broker market cites as a **low-cost, ETF-capable** fondsgebundene
  Rentenversicherung `[unverified]`. Recorded as a second low-cost comparator alongside [S10] and
  the *Nettotarife* of [S18]. **No charge level is established** — and the absence of any
  corroborated charge level anywhere in this corpus is gap 6, the largest hole in the file.

### S14 — Debeka Lebensversicherungsverein a. G., AVB for the fondsgebundene Rentenversicherung

- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: *Bedingungswerk* in the carrier's `B LV` series
- URL: not established. The sibling delib research corroborated by search several Debeka
  *Bedingungswerke* (**B LV 85**, **B LV 86**, **B LV 97**) and the trade-press report that Debeka
  **discontinued its classic annuity tariff**.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene tariff
- Content: recorded because the corroborated discontinuation of the classic tariff at Germany's
  largest life mutual by policy count is **the market-structure fact that puts this product at the
  centre of the library**: when the classic tariff closes, the new-business flow goes to the
  fondsgebundene and hybrid forms. The Debeka fondsgebundene *Bedingungswerk* number, edition and
  content are `[unverified]`.

### S15 — *Basisinformationsblatt* (PRIIP-KID) for a fondsgebundene Rentenversicherung — document-type entry

- Publisher: each insurer, for each *Anlageoption* / product variant
- Doc type: *Basisinformationsblatt* under the PRIIPs Regulation [R8]; three pages, prescribed
  order and prescribed headings
- URL: not established for any fondsgebundene Rentenversicherung. The sibling delib research
  located **one** German PRIIP-BIB PDF, for an **endowment** (its S10, a three-page BIB for a
  regular-premium capital-forming product), which is the wrong product but the right document type
  and confirms the three-page format.
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: this is the **document a delib product-spec would most want and does not have**. Its
  prescribed content, established from the BaFin explanation corroborated in the sibling research
  [R9], is: a **summary risk indicator**; the **possible maximum loss** of invested capital;
  **four performance scenarios** — *Stress*, *pessimistisch*, *moderat*, *optimistisch* — expressed
  as annualised average returns in per cent; the **costs the investor bears**; and complaint
  information. The scenarios and the costs must be shown at **three time points — after one year,
  after half the recommended holding period, and at the end of it** — and the cost disclosure
  splits **one-off from ongoing costs** and states the ***Reduction in Yield* per year**. For an
  FRV the recommended holding period is the *Aufschubzeit*, so those three points are typically
  1 year, ~15 years and ~30 years. **No actual BIB for this product was located, so no scenario
  return, no cost figure and no RIY value is established from one.** Gap 5.

### S16 — *Produktinformationsblatt* / *Verbraucherinformation* — document-type entry

- Publisher: each insurer
- Doc type: the German pre-contractual information set required by § 7 VVG together with the
  *VVG-Informationspflichtenverordnung* [R7]
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the second document class a product-spec needs, and the one that carries the figures
  PRIIPs does not. Established from the corroborated statutory material [R7]: the insurer must
  disclose the ***Abschluss- und Vertriebskosten* included in the premium as a euro amount**, must
  disclose the other costs, and — since **1 January 2015** `[unverified]`, following the LVRG
  [R13] — must state the ***Effektivkostenquote*** in the quotation. A German *Produktinformations-
  blatt* for an FRV therefore normally shows, on two pages: the guaranteed benefits (which for
  this product means the *Rentenfaktor* and little else), the *Abschluss- und Vertriebskosten* in
  euro, the ongoing costs, the *Effektivkosten*, the *Rückkaufswerte* by year, and the
  *Modellrechnung*. **No instance was located and no figure is established.**

### S17 — *Standmitteilung* (annual statement) for a fondsgebundene Rentenversicherung — document-type entry

- Publisher: each insurer; GDV publishes a model
- Doc type: *Jährliche Mitteilung zum Stand der Versicherung*
- URL: not established. The sibling delib research corroborated by search a **GDV
  Muster-Standmitteilung for the kapitalbildende Lebensversicherung, edition 02/2017** (its S2),
  establishing that the GDV publishes model statements per line.
- Retrieved: no — egress blocked; no search corroboration for the fondsgebundene model
- Content: recorded because the *Standmitteilung* is the document that shows **what an in-force
  German unit-linked policy actually reports**, and therefore what a model's state variables should
  correspond to: the number of *Anteileinheiten* held per fund, the *Anteilspreis* at the statement
  date, the resulting *Fondsguthaben*, the premiums paid in the year, the current *Rückkaufswert*,
  and the projected benefit at *Rentenbeginn*. That list is the delib model's state vector almost
  exactly. The **fondsgebundene** model statement's existence is inferred from the corroborated
  endowment one and is `[unverified]`.

### S18 — Nettotarife / Honorartarife — carrier-type entry (myLife and the net variants of full-range carriers)

- Publisher: myLife Lebensversicherung AG and the *Nettotarif* variants of full-range carriers
  ([S5], [S6], [S13] and others)
- Doc type: AVB and *Basisinformationsblatt* of a commission-free tariff
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: a *Nettotarif* (also *Honorartarif*, *Nettopolice*) is **the same unit-linked contract
  with the *Abschluss- und Vertriebskosten* removed from the tariff**, the adviser being paid a
  separate fee by the client under a *Vergütungsvereinbarung*. myLife Lebensversicherung AG is the
  German carrier built entirely on that model `[unverified]`. The class matters here for one
  reason only, and it is a modelling reason: **it isolates the acquisition-cost component of the
  *Effektivkosten*.** The difference between a gross tariff's RIY and the same chassis's net RIY
  *is* the acquisition-cost load, which is the parameter a delib worked example most needs and
  which no document in this corpus supplies. **No net-tariff or gross-tariff RIY figure is
  established**; the observation that the gap exists is structural, not numeric.

---
