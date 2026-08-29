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

## Regulatory and actuarial references

Twenty-six product-specific regulatory and actuarial references. Statutory articles carry the
canonical `gesetze-im-internet.de` form of their URL **marked `[unverified]`**, because no search
in this session returned it; the form itself is a mechanical construction from the statute's
abbreviation and the paragraph number and is given so that a reader can check the claim, not as
evidence that it resolves. Where the substance of a provision was corroborated by search **in a
sibling delib research file**, that is stated and attributed.

### R1 — VVG § 169, *Rückkaufswert* — and the *Zeitwert* branch that governs this product

- Publisher: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008)
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Retrieved: no — egress blocked. **The substance below was corroborated by search in the sibling
  delib research on `kapitallebensversicherung` (its R2) and on `klassische_rentenversicherung`
  (its R1)**, including the German wording of the calculation rule; it is not corroborated here.
- Content, and this is the pivot of the whole product:
  - **Scope.** The article governs the claim to a *Rückkaufswert* where the insurance ends, in
    particular by *Kündigung*, *Rücktritt* or *Anfechtung*, and fixes the calculation principles,
    the limits on payment, the deduction power and the insurer's information duties.
  - **The general rule** (for a conventional contract) is that the *Rückkaufswert* is the
    *Deckungskapital* computed by recognised actuarial rules on the ***Rechnungsgrundlagen der
    Prämienkalkulation*** — the pricing basis, not a current or reserving basis — as at the end of
    the current *Versicherungsperiode*; and on *Kündigung* it is floored by the
    ***Mindestrückkaufswert***, the *Deckungskapital* that results when the *angesetzte Abschluss-
    und Vertriebskosten* are **spread evenly over the first five contract years**.
  - **The branch that governs delib product 3.** For ***fondsgebundene Versicherungen*** and other
    contracts providing benefits of the corresponding kind, the *Rückkaufswert* is instead **the
    *Zeitwert* of the insurance, computed by recognised actuarial rules**. The sibling's
    corroborated entry states that branch explicitly and says of it: "That branch governs delib
    product 3." The internal paragraph designation of the *Zeitwert* branch — whether it is Abs. 3
    Satz 2 or Abs. 4 — and the cross-reference it makes into the *Versicherungsaufsichtsgesetz*
    are **`[unverified]`**; the *substance* is corroborated.
  - **What the *Zeitwert* branch removes.** For a pure unit-linked contract with no insurer-given
    benefit guarantee, the *Zeitwert* is **the value of the units held** — there is no discounting,
    no mortality basis, no *Rechnungszins* and no *Zillmerung* residue in it, because there is no
    *Deckungskapital* in the general-account sense to compute. This is the single largest
    modelling simplification in the delib library: **`Rückkaufswert(t) = Fondsguthaben(t)`**, less
    a *Stornoabzug* if one is validly agreed.
  - ***Abzug* (*Stornoabzug*).** Permissible **only if *vereinbart*, *beziffert* and
    *angemessen*** — agreed, quantified in the contract, and appropriate. A deduction **for
    *noch nicht getilgte Abschluss- und Vertriebskosten* is unwirksam**, which is what prevents an
    insurer recovering through the deduction what the five-year spreading denies it.
  - **The open question for a fondsgebundene contract** is whether the *Mindestrückkaufswert*
    floor of the general rule reaches the *Zeitwert* branch at all, or whether the same protection
    operates instead through the tariff — by limiting the acquisition-cost deduction from premiums
    to one fifth per year over the first five years, so that the units are simply never removed in
    the first place. **The market implements the second**, and that implementation is what section
    4 models. Which of the two the statute requires is **`[unverified]`** and is gap 2.

### R2 — VVG § 168, *Kündigung* (the policyholder's termination right)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the provision giving the policyholder of a life contract with recurring premiums the
  right to terminate **for the end of the current *Versicherungsperiode***, which for a
  monthly-premium contract is a short notice period rather than an annual one. It is the pairing
  of this right with the § 169 valuation rule [R1] that makes *Storno* on a German unit-linked
  policy a **near-frictionless exit at the fund value** — which in turn is why unit-linked lapse
  experience is materially different from conventional lapse experience, and why the delib model
  treats *Storno* and *Beitragsfreistellung* as two separate decrements rather than one. **The
  paragraph number, the notice period and any restriction for single-premium contracts are
  `[unverified]`.**

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R2) and `kapitallebensversicherung` (its R3), including the
  paid-up formula for a conventional contract.
- Content: the policyholder of a recurring-premium life contract may **demand conversion to a
  paid-up contract** for the end of the current *Versicherungsperiode*. For a conventional
  contract the paid-up benefit is computed from the *Rückkaufswert* on the pricing basis. **For a
  fondsgebundene contract the mechanic is different and simpler, and this is the point section 12
  turns on**: nothing is converted. The units stay where they are, premium payment stops, the
  *beitragsbezogene* charges stop with it because there are no more premiums to charge them on,
  and the ***kapitalbezogene* charges, the *Stückkosten* and the *Risikobeitrag* continue to be
  taken by cancelling units**. A paid-up unit-linked policy therefore **decays**: on a small
  *Fondsguthaben* the fixed *Stückkosten* can consume it. Insurers accordingly set a **minimum
  *Fondsguthaben* below which *Beitragsfreistellung* is refused and the contract is surrendered
  instead** — the level is `[unverified]` and is a `[std]` parameter.

### R4 — VVG § 163, *Anpassung der Prämie* / adjustment with a *Treuhänder*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated in the sibling delib research** on
  `klassische_rentenversicherung` (its R3), where it is the statutory successor to the
  *Treuhänderklausel*.
- Content: the statutory channel through which a life insurer may adjust a contract where the
  calculation bases have changed in a way that is permanent and was not foreseeable, subject to an
  **independent trustee's confirmation** that the conditions are met. For this product it is the
  **only remaining route by which a *garantierter Rentenfaktor* can be reduced**, the contractual
  *Treuhänderklausel* being confined to older contracts [R22]. The paragraph number and the
  conditions' exact formulation are `[unverified]`.

### R5 — VVG § 153, *Überschussbeteiligung*, and the *Bewertungsreserven*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated in the sibling delib research** on
  `kapitallebensversicherung` (its R1).
- Content: the policyholder is entitled to a share of the surplus and of the *Bewertungsreserven*
  unless profit participation is excluded by express agreement. **The application to a
  fondsgebundene contract is the point worth recording**: the investment result belongs to the
  policyholder already, by construction, so the *Überschussbeteiligung* of an FRV arises from the
  **risk result and the cost result only**, and the *Bewertungsreserven* limb has almost nothing to
  attach to because the assets backing the unit liability are the units themselves. In practice
  surplus on an FRV is credited as **additional units** or as a **reduction of charges**, plus a
  *Schlussüberschuss* at *Rentenbeginn*. Whether an insurer may exclude participation altogether on
  a unit-linked tariff, and on what conditions, is `[unverified]`.

### R6 — VVG § 152, *Widerruf* (cancellation right) and §§ 7–8 VVG (pre-contractual information)

- Publisher: Bundesministerium der Justiz
- URLs: `https://www.gesetze-im-internet.de/vvg_2008/__152.html` ·
  `https://www.gesetze-im-internet.de/vvg_2008/__7.html` — both `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: § 7 VVG requires the insurer to supply the contract terms and the information specified
  by the *VVG-InfoV* [R7] in text form before the policyholder's declaration is bound; § 152 gives
  a life policyholder a **cancellation period of 30 days** `[unverified]` — longer than the general
  14 days — running from receipt of that information. Recorded because on a unit-linked contract
  the *Widerruf* has a mechanical consequence a conventional contract does not have: the amount
  repayable is tied to the **unit value at the date of cancellation**, so a *Widerruf* after a
  market fall is not a full premium refund. The exact rule is `[unverified]`; the delib model does
  not project the *Widerruf* window.

### R7 — VVG-InfoV § 2 — cost disclosure, the *Effektivkosten* and the *Modellrechnung*

- Publisher: Bundesministerium der Justiz (*Verordnung über Informationspflichten bei
  Versicherungsverträgen*)
- URL: `https://www.gesetze-im-internet.de/vvg-infov/__2.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R9), which established the provision's heading, the statutory
  basis and the introduction date of the *Effektivkosten*.
- Content, as corroborated there and applied here:
  - § 2 VVG-InfoV is headed *Informationspflichten bei der Lebensversicherung, der
    Berufsunfähigkeitsversicherung und der Unfallversicherung mit Prämienrückgewähr* — one
    provision covering all the savings-bearing personal lines, this product included.
  - The legal basis for the cost disclosure is **§ 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3
    VVG-InfoV**, requiring disclosure of the ***Abschluss- und Vertriebskosten* included in the
    premium, in euro amounts** — not as a percentage, not netted into a yield.
  - The ***Effektivkostenquote* (Reduction in Yield, RIY)** was introduced in quotations **with
    effect from 1 January 2015** `[unverified]`, following the **LVRG of 2014** [R13]. It
    discloses **all costs — acquisition, ongoing and investment — expressed as a reduction of the
    contract's yield**.
  - **For a fondsgebundene contract the *Effektivkosten* must include the fund's own costs**, not
    only the policy-level charges. That is what makes the metric meaningful on this product and
    what makes the fund's *TER* a policy parameter rather than a fund parameter. The precise
    treatment of *Kickbacks* credited back to the contract inside the calculation is
    `[unverified]` and is gap 8.
  - § 2 also requires a ***Modellrechnung*** — an illustration of the benefit at maturity on
    prescribed assumed returns. The **number of assumed rates and their level** are `[unverified]`;
    the German market convention of illustrating a fondsgebundene contract at three rates is
    recorded in section 17 as market practice, not as a statutory requirement.

### R8 — PRIIPs Regulation (EU) 1286/2014 and the RTS, Delegated Regulation (EU) 2017/653 as amended

- Publisher: European Parliament and Council; European Commission
- URL: not established (EUR-Lex is among the blocked hosts)
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the regulation that requires a ***Basisinformationsblatt*** (key information document)
  for every packaged retail and insurance-based investment product, a fondsgebundene
  Rentenversicherung being the paradigm German IBIP. The **regulation number 1286/2014**, the
  **RTS number 2017/653** and the **amending regulation that reworked the performance-scenario
  methodology with effect from 1 January 2023** are all `[unverified]` here — they are recalled,
  not searched. What is not in doubt, because BaFin's own explanation of it was corroborated in
  the sibling research [R9], is the **content** of the document: risk indicator, maximum loss,
  four performance scenarios, costs, complaints — at three time points, with the RIY stated per
  year. The RTS's **categorisation of PRIIPs** into four classes, under which a **pure unit-linked
  contract without profit participation falls in Category 2** (linear unleveraged exposure, with
  the scenarios derived from the underlying's own return history) while a **profit-participating
  or guarantee-bearing contract falls in Category 4** (values depend partly on factors not observed
  in the market), is `[unverified]` as to the category numbers but is corroborated as to the
  existence of Category 4 by [R18].

### R9 — BaFin *Fachartikel*, "PRIIPs-Verordnung: Wie Versicherer Verbraucher informieren" (2022)

- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFinJournal)
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html`
  — recorded in the sibling delib research on `kapitallebensversicherung` (its R19) as a search
  result; **not a search result of this file's own**
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there: the supervisor's own statement of what a *Basisinformationsblatt*
  must contain — a **total risk indicator**; the **possible maximum loss of invested capital**;
  **suitable performance scenarios**; the **costs the investor bears**; and how and where to
  complain. **Four graded scenarios — *Stress*, *pessimistisch*, *moderat*, *optimistisch* — must
  be given as annualised average returns in per cent**, at **three time points: after one year,
  after half the term, and at the end of the term**; **total costs and the *Reduction in Yield* per
  year are shown at those same points**, split into **one-off and ongoing costs**. The
  ***Effektivkosten* of a specimen contract must be stated in the BIB**, which must be **published
  on the insurer's website** and **provided before conclusion**. This is the most precisely
  established regulatory fact available to this file and it is the frame for section 17.

### R10 — BaFin, Merkblatt 01/2023 (VA) on *wohlverhaltensaufsichtliche Aspekte bei kapitalbildenden Lebensversicherungsprodukten*

- Publisher: BaFin; published **May 2023** `[unverified]`
- URL: `https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html`
  — recorded in the sibling delib research (its R17); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there, and it applies to this product with more force than to any
  other in the library because this product's charges are its whole economics:
  - **Purpose**: to ensure that *kapitalbildende Lebensversicherungsprodukte* offer an appropriate
    ***Kundennutzen*** (customer value).
  - **Cost**: the *Effektivkosten* of different providers and products **differ considerably**;
    BaFin will **closely examine** undertakings whose *Effektivkosten* are **very high compared
    with industry norms**, and whose ***Aufwendungen für Versicherungsvermittler*** are notably
    high.
  - **Return**: the manufacturer must formulate a ***Renditeziel*** for the defined target market,
    achievable with sufficient probability, and for retirement-provision products the product must
    **achieve a real investment success with sufficient probability — a return net of costs
    exceeding a justified inflation expectation**.
  - **No numerical threshold was established** — not for *Effektivkosten*, not for commission, not
    for the real return. Any figure attributed to the *Merkblatt* would be an invention.

### R11 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"

- Publisher: BaFin, annual supervisory risk-focus publication, consumer-protection chapter
- URL: `https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html`
  — recorded in the sibling delib research (its R18); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content: establishes that **"Kosten von kapitalbildenden Lebensversicherungen" is a named focus
  risk in BaFin's 2026 risk agenda** — three years after the *Merkblatt* [R10], the supervisor
  still treats the charge level of this product family as an open problem. **No text of the
  chapter is established.** Recorded here because it is the reason the delib documents treat
  charge levels as a **supervised** rather than a free parameter, and state their `[std]` charge
  stack as a design decision rather than as an observation.

### R12 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*

- Publisher: Bundesministerium der Justiz / Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R7) and `klassische_rentenversicherung` (its R7).
- Content, and its two quite different bearings on this product:
  - **The *Höchstrechnungszins*** — the statutory maximum technical interest rate for new
    business — was **1,00 % from 1 January 2025** `[unverified]`, raised from **0,25 %**, and the
    DAV recommended the same 1,00 % for 2026. **On the accumulation phase of a pure fondsgebundene
    contract this has no effect at all**, because there is no guaranteed accumulation rate to cap.
    It bears on the product **only** through the *Rentenfaktor*, which is priced with a
    *Rechnungszins*, and through hybrid designs whose guaranteed pot sits in the general account.
    That asymmetry is worth stating explicitly, because it is the reason unit-linked new business
    grew through the low-interest decade while classic new business collapsed.
  - **The *Höchstzillmersatz*** — the cap on acquisition costs that may be financed against future
    premiums — is **25 ‰ (2,5 %) of the *Beitragssumme*** `[unverified]`, cut from 40 ‰ by the LVRG
    2014 [R13]. The *Beitragssumme* is the sum of all premiums payable over the premium-paying
    term. **This is the single most useful number in the file**: combined with the five-year
    spreading rule of § 169 VVG [R1] it pins the shape *and* the maximum level of the acquisition
    charge in a German unit-linked tariff, and section 4 builds the `[std]` charge on it.

### R13 — LVRG 2014, *Lebensversicherungsreformgesetz*

- Publisher: Deutscher Bundestag / Bundesgesetzblatt
- URL: not established. **No Bundesgesetzblatt citation is given** — inventing one is exactly what
  the retrieval-conditions section forbids.
- Retrieved: no — egress blocked. Corroborated in outline by search in the sibling delib research
  (its R29 and its S15).
- Content: the 2014 reform package that, for this product, did three things. It **cut the
  *Höchstzillmersatz* from 40 ‰ to 25 ‰** [R12]; it **introduced the *Effektivkosten* disclosure**
  in quotations with effect from 1 January 2015 [R7]; and it changed the *Bewertungsreserven*
  participation rules. The sibling research also recorded an industry study reporting that
  ***Abschlusskosten* fell by almost 8 % after the LVRG** `[unverified]`. The effective dates and
  the 8 % figure are `[unverified]`. The 40 ‰ → 25 ‰ cut is corroborated at the level of a
  secondary consumer page in the sibling file and is the basis of the `[std]` acquisition charge
  here; a delib document must say that it rests on that and nothing stronger.

### R14 — MindZV, *Mindestzuführungsverordnung*

- Publisher: Bundesministerium der Finanzen
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Retrieved: no — egress blocked. Corroborated in outline by search in the sibling delib research
  on `kapitallebensversicherung` (its R6).
- Content: the regulation fixing the **minimum share of each surplus source that must be credited
  to policyholders**. For this product the relevant sources are the ***Risikoergebnis*** and the
  ***übriges Ergebnis*** (essentially the cost result), because the investment result of a
  unit-linked contract is the policyholder's by construction and never enters the insurer's
  *Rohüberschuss* in the first place. The **minimum percentages — commonly given as 90 % of the
  risk result and 50 % of the other result** — are `[unverified]`. The consequence for the delib
  model is recorded and then set aside: an FRV's *Überschussbeteiligung* is a **second-order
  credit** on a product whose first-order economics are fund return minus charges, and the model
  does not project it (section 15).

### R15 — VAG — *Sparteneinteilung*, asset congruence, and the *Zuwendungen* rules

- Publisher: Bundesministerium der Justiz (*Versicherungsaufsichtsgesetz* 2016)
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content, three distinct provisions, all with `[unverified]` paragraph numbers:
  - **Sparteneinteilung.** Anlage 1 to the VAG lists ***fonds- und indexgebundene
    Lebensversicherung* as a Versicherungssparte in its own right**, separate from ordinary
    *Lebensversicherung*. This is why German statistics report unit-linked new business separately
    and why a German insurer's accounts show a separate *Deckungsrückstellung* line for it.
  - **Asset congruence.** The assets covering unit-linked liabilities must be **held in the
    corresponding units** — the insurer does not take investment risk on them and does not hold
    them in the general *Sicherungsvermögen* pool. The practical consequence for the model is that
    **the unit liability and the unit assets move together exactly**, so a unit-linked projection
    has no investment-mismatch term at all; the whole of the insurer's economics is in the
    non-unit cash flows.
  - ***Zuwendungen*.** The IDD-derived conflict-of-interest and inducement rules govern
    **whether and how an insurer may retain a *Kickback* / *Bestandsprovision*** received from a
    fund company out of that fund's TER. German practice is that the insurer credits some or all
    of it to the contract; the statutory constraint on retaining it is `[unverified]` and is
    gap 8.

### R16 — DAV 2004 R, *Sterbetafel für Rentenversicherungen*

- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- URL: not established
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R12–R14), including its derivation document and its
  generational character.
- Content: the German annuity table, **generational** — mortality is given per birth cohort and
  includes the expected future improvement — with a first-order (loaded) and a second-order
  (best-estimate) version. It is **the table on which a *Rentenfaktor* is computed**, as
  corroborated at one carrier by the sibling research: the annuity factor fixed at inception rests
  on "a recognised mortality table (currently DAV 2004 R)" and an underlying interest rate of
  "currently 0 percent p.a." [S10]. **DAV tables are the property of the DAV, are not public and
  are not redistributed by this library** (house rules §6): delib ships a `[std]` proxy, cites the
  table by name, and states what a replacement must preserve — a generational structure, annuitant
  (not population) selection, and a first-order margin over the second-order basis.

### R17 — DAV 2008 T, *Sterbetafel für Lebensversicherungen mit Todesfallcharakter*

- Publisher: Deutsche Aktuarvereinigung e. V.
- URL: not established
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R14), which located the DAV derivation document by title.
- Content: the German mortality table for death-benefit business, again with first- and
  second-order versions. It matters to this product in one specific place: **the *Risikobeitrag*
  charged for a death benefit above the *Fondsguthaben*** is a death-risk charge and is priced on
  a death table, not on the annuity table used for the *Rentenfaktor*. **A German FRV therefore
  carries two mortality bases at once** — DAV 2008 T for the pre-*Rentenbeginn* risk charge, DAV
  2004 R for the conversion guarantee — and a model that uses one table for both will misprice one
  of them. Same redistribution rule as [R16]: cited, not shipped.

### R18 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025)

- Publisher: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung*
- URL: `https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf`
  — recorded in the sibling delib research (its R27); not a search result of this file's own
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content: identified by title and date — a **profession-agreed standard method for PRIIP
  *Kategorie 4***, the category for insurance-based products whose values depend partly on factors
  not observed in the market. Its existence establishes that **the performance scenarios in a
  German BIB for a guarantee-bearing or profit-participating contract come from a standard method
  rather than from each insurer's own model**. For a **pure** fondsgebundene contract the scenarios
  are instead derived from the underlying funds' own return history under the Category 2 method
  `[unverified]` — which is why two BIBs for economically similar products can show very different
  scenario returns, and why no scenario figure from one carrier transfers to another. **No content
  of the report is established.**

### R19 — EStG § 22 — *Ertragsanteilsbesteuerung* of the annuity

- Publisher: Bundesministerium der Justiz (*Einkommensteuergesetz*)
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `klassische_rentenversicherung` (its R5).
- Content: a private annuity — including one arising from the conversion of a fondsgebundene
  contract at *Rentenbeginn* — is taxed on its ***Ertragsanteil***, the interest component deemed
  contained in each instalment, and **not** on the return of capital. The *Ertragsanteil* is a
  **statutory percentage depending on the annuitant's age at *Rentenbeginn***, falling as the age
  rises. **At age 65 it is 18 %** — the single value corroborated in the sibling research; **every
  other age is `[unverified]`** and the table is not reproduced here. The tax treatment is
  identical for a fondsgebundene and a classic annuity once the annuity is in payment, which is
  the point: **the fund wrapper affects the accumulation phase's taxation, not the payout
  phase's**.

### R20 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalwahlrecht*, the 12/62 rule and the fondsgebunden *Teilfreistellung*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` `[unverified]`
- Retrieved: no — egress blocked. **Corroborated by search in the sibling delib research** on
  `kapitallebensversicherung` (its R10) and `klassische_rentenversicherung` (its R6) as to the
  12/62 rule and the half-income method.
- Content:
  - Electing a **lump sum** instead of the annuity moves the contract from § 22 [R19] to § 20:
    the taxable amount is **the excess of the payment over the premiums paid**, and where the
    contract has run **at least 12 years and the payment is made after the completion of the 62nd
    year of age**, **only half that gain is taxable** (the *Halbeinkünfteverfahren* /
    *Hälftedifferenzmethode*). Otherwise the whole gain is taxable and subject to
    *Kapitalertragsteuer*.
  - Contracts concluded **before 1 January 2005** sit in a different regime; the German in-force
    book carries **two tax cohorts**.
  - **The provision specific to this product**: for a ***fondsgebundene*** contract a
    ***Teilfreistellung*** applies to the fund income inside the wrapper — commonly stated as
    **15 %** for equity-fund exposure `[unverified]` — reflecting the fund-level taxation of the
    *Investmentsteuergesetz* [R21]. The **sentence number within § 20 Abs. 1 Nr. 6, the percentage
    and the conditions are all `[unverified]`** and are gap 22.
  - **The accumulation-phase point, which is the product's principal commercial argument**: inside
    the insurance wrapper there is **no annual taxation of fund income, no *Vorabpauschale*, and no
    taxable disposal on a *Fondswechsel***. A direct fund holding is taxed on both. That deferral
    is the reason the product exists in competition with an ETF *Sparplan*. Its statutory basis is
    the same provision and is `[unverified]` in its detail.

### R21 — InvStG — *Investmentsteuergesetz* and the *Teilfreistellung*

- Publisher: Bundesministerium der Justiz
- URL: `https://www.gesetze-im-internet.de/invstg_2018/` `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the 2018 reform of German fund taxation, which taxes the fund itself on certain German
  income and compensates the investor with a ***Teilfreistellung*** graded by the fund's equity
  quota. It reaches this product through [R20]: the *Teilfreistellung* available inside a
  fondsgebundene life contract is set by reference to this regime. **All percentages, equity-quota
  thresholds and the interaction with the insurance wrapper are `[unverified]`.** Recorded because
  a delib taxation section that mentions the 15 % figure without naming the statute it derives
  from would be citing nothing.

### R22 — The *Rentenfaktor* / *Treuhänderklausel* cluster (consumer and trade press, and the LG Köln line)

- Publisher: Finanztip Verbraucherinformation gemeinnützige GmbH; versicherungenmitkopf.de;
  Versicherungswirtschaft-heute
- URLs: `https://www.finanztip.de/private-rentenversicherung/rentenfaktor/` ·
  `https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung` ·
  `https://www.versicherungenmitkopf.de/rentenversicherung/rentenfaktor` — all recorded in the
  sibling delib research on `klassische_rentenversicherung` (its R16–R18); **not search results of
  this file's own**
- Retrieved: no — egress blocked; corroborated by search in the sibling file only
- Content, as corroborated there, and it transfers to this product **with more force than to the
  classic one**, because on a fondsgebundene contract the *Rentenfaktor* is the **only** guarantee
  the policyholder has:
  - Insurers **could previously change guaranteed *Rentenfaktoren* on the basis of a
    *Treuhänderklausel* in the conditions, with the approval of an independent external
    *Treuhänder***, where economic conditions deteriorated permanently and unexpectedly.
  - **Two explicit triggers**: an **unexpectedly strong increase in life expectancy**, requiring
    adjustment of the mortality tables; and a **sustainable reduction in capital-market returns**,
    permitting adjustment of the interest rate.
  - **The clause is now used only in older contracts; today the guaranteed *Rentenfaktor* can be
    changed only on the basis of § 163 VVG** [R4].
  - **The Landgericht Köln held that the low-interest phase is not a sufficient ground**, because
    it must be treated as entrepreneurial risk that cannot be passed on to policyholders. **The
    case reference, decision date and parties were not established** in the sibling research either
    — gap 15.
  - Trade press of **4 February 2021** reports the market leader's position that customers could
    not successfully object to an adjustment — establishing that this was a **live commercial
    dispute at the largest German life insurer**, inside the window in which the current in-force
    unit-linked book was written.
  - **The consumer definition of the factor**, from the same cluster: the *Rentenfaktor*
    determines **how much monthly annuity is received per 10 000 € of accumulated capital**, so
    that a capital of 100 000 € with a factor of 25 yields 250 € per month. **The 25 in that
    illustration is a teaching example, not a market level.**

### R23 — Rating houses and market studies: Franke und Bornberg, Morgen & Morgen, Assekurata

- Publisher: Franke und Bornberg GmbH; Morgen & Morgen GmbH; ASSEKURATA Assekuranz Rating-Agentur
  GmbH
- URLs: not established for any fondsgebundene study. The sibling delib research corroborated by
  search the existence of Franke und Bornberg's *Rentenfaktor* and *Basisinformationsblätter*
  commentary and of Assekurata's **24. Marktstudie "Überschussbeteiligungen und Garantien 2026"**.
- Retrieved: no — egress blocked; no search corroboration for any fondsgebundene study
- Content: these three houses are **where German unit-linked cost and *Rentenfaktor* levels are
  actually published** — in rating reports, annual market studies and product comparisons. They are
  the documents this file most needed and did not have. The sibling research recorded that even
  the Franke und Bornberg article **titled** "Was bedeutet der Rentenfaktor und wie hoch ist er?"
  returned no level, range or table in its search summary. **No figure from any of these houses is
  used anywhere in the delib documents**, and the consequence is that every *Rentenfaktor* and
  every charge level in this product's documents is `[std]`. Gaps 4 and 6.

### R24 — Consumer bodies and comparison portals: Stiftung Warentest / Finanztest, Verbraucherzentrale, Verivox, Check24, Finanztip

- Publisher: Stiftung Warentest; Verbraucherzentrale Bundesverband and the *Länder*
  *Verbraucherzentralen*; Verivox GmbH; CHECK24 Vergleichsportal GmbH; Finanztip
- URLs: not established for any fondsgebundene Rentenversicherung page
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: the secondary literature in which German consumers meet this product, and normally the
  only public place where **price points** appear — a monthly premium, an *Effektivkosten*
  percentage, a *Rentenfaktor*, a comparison of tariffs at a stated model point. Stiftung Warentest
  publishes periodic *Finanztest* comparisons of fondsgebundene Rentenversicherungen and
  Verbraucherzentrale publishes critical guidance on their cost. **Nothing from any of them is
  cited in this file, because nothing from any of them was retrieved or searched.** They are
  recorded so that a later reader knows where to look first, and so that the gaps register can say
  precisely what kind of source would close each gap.

### R25 — GDV statistics on German life new business and in-force by *Versicherungsart*

- Publisher: Gesamtverband der Deutschen Versicherer e. V.
- URL: not established. The sibling delib research corroborated by search the existence of the GDV
  statistical series "Die deutsche Lebensversicherung in Zahlen" and "Neugeschäft und Bestand der
  Lebensversicherer für die letzten zehn Geschäftsjahre".
- Retrieved: no — egress blocked; no search corroboration for any unit-linked breakdown
- Content: the series that would establish **the share of German life new business written as
  fondsgebundene Rentenversicherung** — the single market figure this file's opening sentence
  asserts and cannot source. The claim that the fondsgebundene form is the **dominant new-business
  savings form** is therefore `[unverified]` as to any number and rests on the structural
  observations that *are* corroborated: that the classic tariff has been withdrawn at major
  carriers [S14], and that the supervisor's cost agenda [R10] [R11] is framed around
  *kapitalbildende* products generally. Gap 25.

### R26 — BGH case law on *Rückkaufswert*, *Kostenverrechnung* and *Stornoabzug*

- Publisher: Bundesgerichtshof
- URL: not established. **No case number, decision date or docket is given for any decision in
  this entry** — the sibling delib research corroborated one docket (a 2021 decision on
  *Bewertungsreserven*) which is not on point for this product, and nothing else.
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Content: there is a long and well-known German line of authority on **whether and how an insurer
  may charge acquisition costs against the early values of a life contract**, running from
  decisions on *Zillmerung* and on the transparency of *Rückkaufswert* clauses before the VVG 2008
  reform, through decisions on the validity of *Stornoabzug* clauses, to decisions applying the
  post-2008 rules. **This file records that the line exists and cites no decision from it**, since
  no case reference could be established without a search. Any statement in a delib document about
  what a court has held on a *Rückkaufswert* clause must carry `[unverified]` and must not carry a
  docket number. Gap 16.

---

## Extracted facts, by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. It is written
long because it is the part that does not depend on having a PDF open. **Structure is described
without hedging where it is common ground in German practice; every level is either `[std]` with a
rationale or tagged `[unverified]`.**

### 1. Product structure and the unit-linked principle

- A *fondsgebundene Rentenversicherung* is a **deferred private annuity whose accumulating value is
  a holding of units in investment funds chosen by the policyholder**. The insurer administers the
  contract, bears the biometric risk, and gives one financial guarantee — the *Rentenfaktor* — but
  **does not guarantee the value of the fund holding at any point before *Rentenbeginn***.
- The defining sentence of the product, and the one every German wording expresses in some form:
  **the insurer guarantees the number of *Anteileinheiten*, not their value.** Everything else
  follows from it. There is no *Rechnungszins* in the accumulation phase, no *Deckungskapital* in
  the general-account sense, no *Zinsüberschuss*, no *Bewertungsreserven* worth speaking of, and no
  investment mismatch between the insurer's assets and its unit liability [R15].
- **It is a distinct supervisory class**: Anlage 1 to the VAG lists *fonds- und indexgebundene
  Lebensversicherung* as its own *Versicherungssparte* [R15] `[unverified]` as to the item number,
  which is why German statistics and German insurers' accounts report it separately.
- **It is *Schicht 3*** — unsubsidised private provision. There is no state allowance, no
  *Sonderausgabenabzug* of the premium, and correspondingly no *Beitragsgarantie* requirement, no
  restriction on the payout form and no *Förderschädlichkeit* on surrender. The fondsgebundene
  forms of *Basisrente* and *Riester* carry all of those and are separate delib products.
- **The contract is a life insurance contract, not a fund product**, and that has three
  consequences the model must respect: the death benefit is an insurance benefit and is priced with
  a *Risikobeitrag* (section 6); the conversion at *Rentenbeginn* is a **guaranteed** conversion at
  a factor fixed at issue (section 9); and the accumulation phase is not taxed (section 16).
- **Legal wrapper**: an individual contract between the policyholder and the insurer. There is no
  German equivalent of the French group-with-voluntary-membership wrapper in the retail Schicht 3
  market; group forms belong to bAV, which is out of scope.

### 2. The unit / non-unit split

- The policy's value is the ***Fondsguthaben***: the number of *Anteileinheiten* held in each fund,
  multiplied by that fund's *Anteilspreis* at the *Bewertungsstichtag*. Formally, with `n_j(t)` the
  units held in fund `j` and `P_j(t)` its unit price:

  ```
  Fondsguthaben(t) = sum_j n_j(t) x P_j(t)
  ```

- **Units are the state variable; euro are derived.** Every operation on the contract is expressed
  as a purchase or a cancellation of units at a price on a date. This is what makes the product a
  clean recursion: the model carries `units(t)` and `unit_price(t)` and derives everything else.
- **The *Anteilspreis* is the fund's *Rücknahmepreis*** — its net asset value per unit. German
  insurers normally buy policy units at the *Rücknahmepreis*, i.e. **with the *Ausgabeaufschlag*
  (front-end load) waived**, because they deal with the fund company at institutional terms; the
  policy's own acquisition charge takes the place of the retail load. Whether any given tariff
  waives it in full is `[unverified]`, and the delib model assumes a **full waiver** as a `[std]`
  simplification, which is the market norm.
- **The *Bewertungsstichtag*** is the dealing date on which a premium buys units or a charge
  cancels them. Wordings typically fix it as the next fund valuation after the premium is received
  or the event occurs. **On a monthly model grid this is the month boundary** and the timing detail
  disappears; it is recorded because it is the reason a real policy's unit count and a model's
  differ by a few days' price movement.
- **The non-unit side.** Everything that is not the unit holding is a cash flow in the insurer's
  own accounts: the charges it withholds or cancels, the *Risikobeitrag* it collects and the death
  benefits it pays, its expenses and its commission. **The delib model projects the non-unit cash
  flows and carries the unit fund only as the base on which they are computed**, which is the
  right emphasis for a liability cash-flow model: the unit fund is the policyholder's money passing
  through.
- **Multi-fund contracts are the norm** — the policyholder allocates the premium across several
  funds in stated percentages, and the *Fondsguthaben* is the sum over funds. The delib model uses
  **one fund** `[std]`, because the number of funds changes nothing in the mechanics and multiplies
  the state vector; the *Fondswechsel* mechanics of section 7 are still modelled, as a re-basing of
  the single fund's assumed return.

### 3. Premium and *Beitragsverrechnung*

- **Premium form**: a level recurring *Beitrag*, most commonly **monthly** and paid by direct debit;
  quarterly, half-yearly and annual frequencies exist, normally with a *Ratenzahlungszuschlag* for
  paying more often than annually `[unverified]` as to level. **The delib model is monthly**
  (`FRV_DE_S`), which matches the dominant frequency and makes the charge mechanics visible.
- **The *Beitragsverrechnung* is the operative rule of the accumulation phase**: what is taken out
  of each gross premium, in what order, before the remainder buys units. The German market order,
  which the delib model follows:

  1. **Gross premium** `B` received.
  2. Less the ***Abschluss- und Vertriebskosten* instalment** `alpha(t)` — non-zero only in the
     first five years (section 4).
  3. Less the ***beitragsbezogene Verwaltungskosten*** `beta x B` — a percentage of the gross
     premium, charged for the whole premium-paying term.
  4. Less the ***Stückkosten*** `SK` — a fixed euro amount per month.
  5. The remainder is the ***Anlagebeitrag***, which **buys units at the *Anteilspreis***.
  6. **Separately, and by cancelling units rather than by withholding premium**: the
     ***kapitalbezogene Verwaltungskosten*** `gamma` on the *Fondsguthaben*, and the
     ***Risikobeitrag*** on the net amount at risk.

- **The distinction between step 5 and step 6 matters and is easy to get wrong.** Premium-based
  charges are withheld *before* units exist; fund-based charges and the *Risikobeitrag* cancel
  units that already exist. A paid-up contract has no step 2–4 and a full step 6 — which is why it
  decays (section 12). A model that nets the fund-based charge out of the premium instead of
  cancelling units will produce the right answer while premiums are paid and the wrong answer the
  moment they stop.
- **Minimum premium**: German unit-linked tariffs typically set a minimum monthly premium of the
  order of **25 € to 50 €** `[unverified]`; the delib `[std]` is **25 €** as an issue-rule floor,
  not as a model parameter.
- ***Beitragsdynamik***: an optional contractual annual increase of the premium — a fixed
  percentage (commonly 3 % or 5 % `[unverified]`) or an index-linked step — with a corresponding
  increase in the *Beitragssumme* and therefore in the acquisition charge. The policyholder may
  normally decline individual increases, and the option lapses after a stated number of
  consecutive declinations `[unverified]`. **The delib model carries `dynamik_rate` as a model-point
  parameter with a `[std]` default of 0 %**, and section 4 records that a *Dynamik* increase
  attracts its own acquisition charge on the increment.
- ***Beitragspause* / *Stundung***: a temporary suspension of premium payment, usually for a
  limited period, after which the contract either resumes or becomes *beitragsfrei*. Not modelled;
  it is *Beitragsfreistellung* with a resumption option and the delib model treats it as one.

### 4. The charge stack, its German names, and the `[std]` levels

This is the most important table in the file, and every level in it is `[std]`. The **structure**
is German market practice; the **levels** were established nowhere in this corpus (gap 6).

| Charge | German name | Base | Timing | delib `[std]` level | Argued range |
|---|---|---|---|---|---|
| Acquisition | *Abschluss- und Vertriebskosten* (*Alpha-Kosten*) | *Beitragssumme* | spread evenly over the first 60 months | 2.5% of *Beitragssumme* | 0% (Nettotarif) to 2.5% (the statutory cap) |
| Premium admin | *beitragsbezogene Verwaltungskosten* (*Beta-Kosten*) | each gross premium | whole premium-paying term | 4.0% of each premium | 2% to 10% |
| Fund admin | *kapitalbezogene Verwaltungskosten* (*Gamma-Kosten*) | *Fondsguthaben* | monthly, by unit cancellation | 0.30% p.a. | 0.10% to 1.20% p.a. |
| Policy fee | *Stückkosten* | per policy | monthly, by withholding or cancellation | 3.00 EUR per month | 0 to 5 EUR per month |
| Risk charge | *Risikobeitrag* | *riskiertes Kapital* | monthly, by unit cancellation | q(x) based, DAV 2008 T proxy | n/a — a priced risk, not a load |
| Fund cost | *TER* / *Gesamtkostenquote* | fund assets | continuously, inside the unit price | 0.45% p.a. | 0.15% (ETF) to 2.00% (active) |
| Trail rebate | *Kickback* / *Bestandsprovision* | fund assets | credited to the *Fondsguthaben* | 0.00% p.a. | 0% to 0.50% p.a. |
| Annuity admin | *Rentenbezugskosten* | each annuity payment | in payment | 1.5% of each payment | 0% to 3% |
| Fund switch | *Fondswechselgebühr* | per switch beyond the free allowance | on election | 0 EUR (free allowance not exhausted) | 0 to 25 EUR |
| Single premium | *Zuzahlungskosten* | each *Zuzahlung* | on receipt | 2.5% of the *Zuzahlung* | 0% to 4% |

**Abschluss- und Vertriebskosten — the one charge whose level has a real anchor.**

- The charge covers commission to the intermediary, underwriting and issue. It is **incurred at
  inception and recovered over years**, which is the mismatch *Zillmerung* exists to finance.
- **The cap.** The *Höchstzillmersatz* is **25 ‰ (2,5 %) of the *Beitragssumme*** [R12], cut from
  40 ‰ by the LVRG 2014 [R13] `[unverified]`. The *Beitragssumme* is the sum of all premiums
  payable over the premium-paying term. **The delib `[std]` takes the cap as the level**, on the
  stated ground that a reference implementation should demonstrate the binding constraint rather
  than a guessed interior point, and that the cap is the only acquisition-cost number with any
  corroboration anywhere in the delib corpus.
- **The spreading.** § 169 VVG requires the *angesetzte Abschluss- und Vertriebskosten* to be
  spread **evenly over the first five contract years** [R1]. In a unit-linked tariff this is
  implemented in the *Beitragsverrechnung*: **only one fifth of the total acquisition charge may be
  withheld in each of the first five years**, so units are bought from the start rather than not at
  all.
- **The arithmetic, worked, because it is the shape the model reproduces.** Monthly premium 200 €,
  premium-paying term 30 years: *Beitragssumme* = 200 × 12 × 30 = **72 000,00 €**; acquisition
  charge at 2,5 % = **1 800,00 €**; spread over 60 months = **30,00 € per month for the first five
  years**, i.e. **15 % of each of the first 60 premiums** and **nothing thereafter**. That step —
  a large early charge that stops abruptly at month 60 — is the characteristic shape of a German
  unit-linked contract's early values and is what the worked example must show.
- **A *Zuzahlung* and a *Dynamik* increase each carry their own acquisition charge** on the
  increment, because each raises the *Beitragssumme*. The delib `[std]` charges 2,5 % of a
  *Zuzahlung* at receipt rather than spreading it, on the ground that a single premium has no
  future premium stream to spread against; whether German tariffs do the same is `[unverified]`.
- **The Nettotarif variant sets this charge to zero** [S18] and is the reason the argued range
  starts at 0 %.

**Verwaltungskosten — two of them, and the German market names them by their base.**

- ***Beitragsbezogene Verwaltungskosten*** are a **percentage of each gross premium** and continue
  for the whole premium-paying term. They stop when premiums stop. In actuarial notation these are
  the *β*-Kosten.
- ***Kapitalbezogene Verwaltungskosten*** are a **percentage per annum of the *Fondsguthaben***,
  taken monthly by cancelling units. The German market also calls them *Gammakosten* or
  *Fondsguthabenkosten*. They **continue after premiums stop** and they are the charge that makes a
  paid-up unit-linked policy decay. In a long contract they are the dominant component of the
  *Effektivkosten*, because they compound against the whole accumulated fund.
- ***Stückkosten*** are a **fixed euro amount per policy per month or per year**, sometimes
  indexed. They are regressive — trivial on a 500 € premium, material on a 25 € one — and they are
  the reason minimum premiums exist.
- **No level for any of the three was established at any carrier.** All three are `[std]`.

**The fund's own costs, and the *Kickback*.**

- The fund's ***TER*** is borne **inside the unit price** and never appears in the policy ledger.
  A model that charges it explicitly will double-count; a model that ignores it will overstate the
  policyholder's return. **The delib model handles it by netting it off the assumed gross fund
  return**, which is exactly what it is.
- ***Kickback* / *Bestandsprovision***: the fund company pays the insurer a trail commission out of
  the fund's TER. German practice is that the insurer **credits some or all of it back to the
  contract** as additional units, so that the policyholder's effective fund cost is the TER less
  the credited rebate. The IDD-derived inducement rules bear on whether it may be retained [R15]
  `[unverified]`.
- **The choice of fund is therefore a charge parameter.** A passive ETF has a low TER and pays no
  *Kickback*; an active fund has a high TER and pays one. The two can produce similar net costs and
  very different gross ones, and a PRIIPs cost disclosure that includes the fund's costs will show
  it. The delib `[std]` uses **a passive fund: 0,45 % p.a. TER, no *Kickback***, on the ground that
  it is the simpler and more transparent of the two and needs no assumption about rebate crediting.

### 5. *Effektivkosten* — the metric that ties the stack together

- The ***Effektivkostenquote*** (Reduction in Yield, RIY) states **all charges as the annual
  percentage by which they reduce the contract's return**. It is required in German quotations
  since 1 January 2015 under the *VVG-InfoV* [R7] `[unverified]` and, in its PRIIPs form, in the
  *Basisinformationsblatt* at **three time points — one year, half the recommended holding period,
  and the end of it** [R9].
- **It is the only single number that compares two unit-linked tariffs**, because it collapses a
  premium-based charge, a fund-based charge, a fixed fee and the fund's TER onto one scale. That is
  also its weakness: it depends on the assumed gross return, on the term and on the premium, so two
  quoted RIYs are comparable only at the same model point.
- **Supervisory context.** BaFin says *Effektivkosten* **differ considerably** between providers and
  will **closely examine** undertakings whose costs are very high against industry norms [R10]; the
  cost of *kapitalbildende Lebensversicherungen* is a **named focus risk for 2026** [R11]. **No
  numerical threshold was established** in this corpus or in the sibling files.
- **Order-of-magnitude check on the delib `[std]` stack**, given as arithmetic and not as an
  observation: on the section 4 levels at a 200 € monthly premium over 30 years, the premium-based
  charges take roughly 5,5 % of every premium plus the 15 % early instalment, and the fund-based
  charges take about 0,75 % p.a. of the fund including the TER. The resulting reduction in yield is
  **of the order of 1 % per annum**. The technical notes must compute it exactly from the model's
  own output rather than quote this estimate.
- **Market levels are `[unverified]` in their entirety.** The commonly stated picture — that
  broker-sold commission tariffs sit materially above direct and net tariffs, and that the spread
  across the market is more than a percentage point of annual yield — is consistent with BaFin's
  "differ considerably" [R10] but **no range, no median and no carrier-level figure is established
  anywhere in this corpus**. Gap 6.

### 6. *Todesfallleistung* before *Rentenbeginn*, and the *Risikobeitrag*

- **Four shapes are used in the German market.** Listed in ascending order of the risk they impose
  on the insurer:
  1. ***Fondsguthaben*** — the value of the units at the *Bewertungsstichtag* after the death is
     notified. **No net amount at risk, no *Risikobeitrag*.** The cheapest and, on a pure savings
     tariff, common.
  2. ***Beitragsrückgewähr*** — `max(Fondsguthaben, sum of premiums paid)`. **This is the shape
     corroborated at DEVK** [S2] and the one delib adopts as representative. The net amount at risk
     is positive only while the fund is below the premiums paid, i.e. **early, and after a market
     fall** — which makes the risk charge small in aggregate but strongly path-dependent.
  3. **A percentage of the *Fondsguthaben*** — commonly quoted as 100 %, 105 % or 110 %
     `[unverified]`. A percentage above 100 creates a proportional net amount at risk that grows
     with the fund.
  4. **A *garantierte Mindesttodesfallleistung*** — a stated sum insured, chosen at issue,
     independent of the fund. The most expensive, and the one that turns the contract into a
     savings-plus-term-cover package.
- **The *Risikobeitrag* is levied monthly by cancelling units.** With `TFL(t)` the death benefit
  and `FG(t)` the *Fondsguthaben*:

  ```
  riskiertes Kapital(t) = max( TFL(t) - FG(t), 0 )
  Risikobeitrag(t)      = q_mth(x + t) x riskiertes Kapital(t)
  units cancelled       = Risikobeitrag(t) / Anteilspreis(t)
  ```

  The charge is **recomputed every month** because both `TFL` and `FG` move. On the
  *Beitragsrückgewähr* shape the net amount at risk is `max(premiums paid - FG, 0)`, which is the
  quantity the model must carry: **cumulative premiums paid is a state variable of this product**,
  not a reporting convenience.
- **The mortality basis for the risk charge is a death table — DAV 2008 T** [R17] — **not** the
  annuity table used for the *Rentenfaktor* [R16]. A German FRV carries two mortality bases at
  once. A model that prices the death charge on the annuity table will understate it, because an
  annuitant table's mortality is lighter by selection and by projection.
- **The tax constraint that shapes the design.** German tax law imposes a **minimum death benefit**
  on capital-forming life contracts concluded from 1 April 2009 `[unverified]` — the rule the
  sibling delib research records as the "50 % rule" — under which a contract must provide a death
  benefit of at least a stated proportion of the *Beitragssumme* to keep its favourable treatment.
  **A pure *Rentenversicherung* without a *Kapitalwahlrecht* is outside that rule**, which is one
  reason the annuity form dominates; a contract with a *Kapitalwahlrecht* is exposed to it. The
  precise rule, threshold and date are `[unverified]` and are gap 21.
- **After *Rentenbeginn*** the death benefit is whatever the annuity form provides — a
  *Rentengarantiezeit*, a *Beitragsrückgewähr in der Rentenphase*, or nothing. That is section 10.

### 7. Fund selection, *Fondswechsel*, *Ablaufmanagement*

- **Fund universe.** The policyholder chooses from a list defined by the insurer — typically
  several dozen to a few hundred *Publikumsfonds* and ETFs, sometimes with insurer-managed
  portfolios and *Wertsicherungsfonds* alongside `[unverified]` as to any carrier's count. **The
  insurer may replace a fund** that is closed or merged, normally by transferring the holding to a
  comparable fund after notice.
- ***Fondswechsel*** covers **two distinct operations**, and German wordings use the English words
  *Shift* and *Switch* for them:
  - **reallocating the existing *Fondsguthaben*** from one fund to another — units are cancelled in
    the old fund and bought in the new one at the same *Bewertungsstichtag*; and
  - **redirecting future premiums** to a different fund or a different split, leaving the existing
    holding where it is.
  - **Which English word denotes which operation is not consistent across German insurers**, and
    this file does not assert a mapping. Each AVB defines its own terms. **The delib documents use
    the operations, not the labels**: `shift_existing` and `redirect_future` are the model's names,
    and the technical notes say why. Gap 11.
- **Free allowances.** Tariffs normally allow a number of free changes per year — commonly stated
  as a dozen, sometimes unlimited — and charge a flat fee beyond it `[unverified]`. The delib
  `[std]` is **free within the modelled behaviour**, since the modelled behaviour makes at most one
  reallocation per year.
- **Neither operation is a taxable event** inside the insurance wrapper [R20]. This is the
  product's central commercial argument against holding the same funds directly, where a switch
  realises a gain.
- ***Ablaufmanagement*** is **automatic phased de-risking in the run-up to *Rentenbeginn***: over
  the last few years the *Fondsguthaben* is moved in tranches out of equity funds into money-market
  or *Wertsicherungs* funds, or into the insurer's *Sicherungsvermögen*. It is normally **opt-in or
  opt-out with a default**, and the number of years and the tranche schedule are tariff parameters
  `[unverified]`. **A five-year monthly ramp is the shape most often described** `[unverified]`.
- **Why *Ablaufmanagement* matters to a cash-flow model**: it changes the assumed fund return in the
  final years, and therefore the *Fondsguthaben* at *Rentenbeginn*, and therefore the annuity. The
  delib model implements it as a **deterministic glide on the assumed return** — a `[std]` linear
  ramp from the equity assumption to a money-market assumption over the last 60 months, switchable
  off — rather than as a fund-level reallocation, because with one fund and a deterministic return
  the two are the same thing and the glide is the honest representation of what is known.

### 8. *Zuzahlungen*, *Teilentnahmen*, and the flexible *Rentenbeginn*

- ***Zuzahlung*** — an additional single premium into an existing contract. Subject to a minimum
  (commonly a few hundred euro `[unverified]`), sometimes to an annual maximum, and to its own
  acquisition charge (section 4). It buys units at the *Anteilspreis* on the *Bewertungsstichtag*
  following receipt. It **raises the *Beitragssumme*** and therefore the *Rückkaufswert* and the
  benefit at *Rentenbeginn*. **The delib model supports it as a model-point-driven schedule with a
  `[std]` default of none.**
- ***Teilentnahme* / *Entnahme*** — a partial withdrawal of the *Fondsguthaben* during the
  *Aufschubzeit*. Subject to a minimum withdrawal, a minimum remaining *Fondsguthaben*, and
  sometimes a fee `[unverified]`. It is a **partial surrender** and carries the tax consequences of
  one [R20]. Modelled as a unit cancellation at the *Anteilspreis*; delib's `withdrawals(t)`
  publishes it, per the house naming rules.
- ***Abrufphase* / flexible *Rentenbeginn*** — a window, commonly a few years either side of the
  agreed *Rentenbeginn*, inside which the policyholder may bring the conversion forward or defer it
  `[unverified]` as to width. **Deferring changes the *Rentenfaktor***, because the factor is
  age-dependent: a later start means a shorter expected payout and a higher factor. Whether the
  *guaranteed* factor is restated on deferral, or only the current one, is `[unverified]` and is
  gap 13. **The delib model fixes *Rentenbeginn*** and records the *Abrufphase* as an unmodelled
  option.
- ***Kapitalwahlrecht*** — the option to take the *Fondsguthaben* as a lump sum instead of the
  annuity, normally exercisable up to a notice period before *Rentenbeginn* `[unverified]`. It is
  the single most important behavioural assumption in the product and it has a tax driver
  (section 16).

### 9. The *Rentenfaktor*

**This is the product's only financial guarantee, and it is the reason the contract is insurance.**

- **Definition and arithmetic.** The *Rentenfaktor* is the **monthly annuity per 10 000 € of
  capital at *Rentenbeginn*** [R22]:

  ```
  monthly annuity = Fondsguthaben(Rentenbeginn) / 10 000 x Rentenfaktor
  ```

  A capital of 100 000 € at a factor of 25 yields 250 € per month [R22] — **a teaching example,
  not a market level**.
- **Guaranteed at inception, on the bases then in force.** The *garantierter Rentenfaktor* is fixed
  in the contract documents and rests on the *Rechnungsgrundlagen* at the date of conclusion
  [R22]: a mortality table — **DAV 2004 R** [R16] — and a *Rechnungszins*. The insurer applies a
  ***Sicherheitsabschlag***, which is why the guaranteed factor is lower than the factor the same
  insurer would quote for an immediate annuity today.
- **The margin is quantifiable from one corroborated statement.** The sibling delib research
  established that a large direct writer computes its inception factor on "a recognised mortality
  table (currently DAV 2004 R) and an underlying interest rate of **currently 0 percent p.a.**"
  [S10]. **A zero-per-cent interest basis on a guarantee that will be honoured in thirty years is
  the *Sicherheitsabschlag* made concrete**: the factor is priced as though the insurer will earn
  nothing on the annuity fund for the whole payout phase.
- **The rule at *Rentenbeginn* is a maximum of two factors**, and this is a **guarantee with
  upside**:

  ```
  Rentenfaktor_applied = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell(Rentenbeginn) )
  ```

  The sibling research corroborated this at a conventional carrier — at the start of annuity
  payments a second factor is compared with the guaranteed one and **the higher of the two is
  guaranteed for the payment period** — and at the market leader, whose current bases at
  *Rentenbeginn* are "the interest rate and mortality table that the company uses **at that time
  for immediately beginning annuities**". **A model that applies only the guaranteed factor
  understates the benefit whenever the current tariff is richer.**
- **On a fondsgebundene contract the guarantee bites differently than on a classic one.** On a
  classic contract both the capital and the factor are guaranteed, so the annuity is guaranteed. On
  this product **only the factor is** — the capital it multiplies is the market's. The guarantee is
  therefore a guarantee about the *conversion terms*, not about the *pension*, and any product
  document that implies otherwise is wrong. This is the sentence a delib `product-spec.md` must
  carry.
- **Reduction of a guaranteed factor.** Historically by a ***Treuhänderklausel*** with an
  independent trustee's approval, on two triggers — an unexpectedly strong increase in life
  expectancy, and a sustainable reduction in capital-market returns [R22]. **Today the clause
  survives only in older contracts and the route is § 163 VVG** [R4] [R22]. **The Landgericht Köln
  held that the low-interest phase is not a sufficient ground**, being entrepreneurial risk that
  cannot be passed to policyholders [R22]; the case reference was not established (gap 15). It was
  a live dispute at the market leader in **February 2021** [R22].
- **Modelling consequence**: the guaranteed *Rentenfaktor* is treated as **fixed for the life of
  the contract**, and § 163 VVG is recorded as a model risk rather than implemented.
- **The `[std]` level, and how it is derived rather than guessed.** No market level was established
  anywhere in this corpus (gap 4). Rather than invent one, delib derives it:

  - At a *Rechnungszins* of **0 %** [S10], a monthly annuity of `R` per month payable for an
    expected `T` years has present value `12 x T x R` per unit of capital, so
    `Rentenfaktor = 10 000 / (12 x T)` before costs.
  - On a **generational** annuitant table [R16] a 67-year-old of a cohort now in mid-career has an
    expected annuity duration materially longer than a period table implies; **taking `T` in the
    range 25 to 28 years** gives a pre-cost factor between **29,8 and 33,3** € per 10 000 €.
  - Deducting the payout-phase administration charge (section 4, 1,5 % of each payment) and a
    further explicit margin for the *Sicherheitsabschlag* and for a *Rentengarantiezeit* brings the
    **guaranteed** factor materially below that.
  - **The delib `[std]` guaranteed *Rentenfaktor* is 25,00 € per month per 10 000 € of
    *Fondsguthaben* at age 67**, chosen as a round number inside the band that arithmetic produces,
    and matching the illustrative value the consumer literature uses [R22]. **It is a `[std]`
    parameter with a derivation, not a market observation**, and the technical notes must say so
    wherever it appears.
  - **The `[std]` current factor at *Rentenbeginn*** is set equal to the guaranteed one, so that
    the `max()` is exercised in the model and is visible, but does not silently inject an
    unsourced uplift.

### 10. The *Rentenphase* and the *Kapitalwahlrecht*

- **At *Rentenbeginn* the fund holding is liquidated and the proceeds are converted.** The units
  are cancelled at the *Anteilspreis*, the *Fondsguthaben* passes into the insurer's general
  account, and a **classic annuity** begins — guaranteed at the applied *Rentenfaktor*, with an
  *Überschussrente* on top from the payout-phase surplus. **The unit-linked character of the
  contract ends at *Rentenbeginn***, which is the boundary of the delib model's scope: the payout
  phase's machinery belongs to `sofortrente`.
- **A fund-linked payout phase exists** at some carriers — the annuity continues to be expressed in
  units and varies with the fund — but it is a minority form `[unverified]` and delib does not
  model it.
- ***Rentengarantiezeit***: a guaranteed payment period, commonly 5, 10 or 15 years
  `[unverified]`, during which instalments continue to the beneficiary if the annuitant dies. It
  reduces the *Rentenfaktor*, because it is a second benefit paid for out of the same capital.
- ***Kapitalwahlrecht***: the option to take the *Fondsguthaben* as a lump sum at *Rentenbeginn*
  instead of the annuity, subject to a notice period `[unverified]`. **Its take-up is the largest
  behavioural unknown in the product** and it is economically live, because the two tax regimes are
  genuinely different (section 16). **No take-up rate was established** (gap 19); the delib `[std]`
  runs the annuity path and carries the lump-sum path as a switch.
- **A *Teilkapitalisierung*** — part lump sum, part annuity — is normally available and is modelled,
  if at all, as a proportional blend.

### 11. *Rückkaufswert* and *Storno*

- **The surrender value of a fondsgebundene policy is the *Zeitwert*** [R1], and for a pure
  unit-linked contract with no insurer-given guarantee **the *Zeitwert* is the *Fondsguthaben***:

  ```
  Rückkaufswert(t) = Fondsguthaben(t) - Stornoabzug(t)
  ```

- **What that removes from the calculation is the whole conventional apparatus**: no discounting,
  no *Rechnungszins*, no mortality basis, no *Zillmerung* residue, no *Mindestrückkaufswert*
  computation on a second basis. It is the cleanest surrender rule of the ten delib products, and
  it is the reason this product is a good vehicle for demonstrating unit mechanics.
- **The protection for the policyholder sits earlier, in the *Beitragsverrechnung***: because the
  acquisition charge may only be taken over the first five years [R1], the *Fondsguthaben* is never
  driven to zero by an up-front deduction, and the surrender value is positive from the first year.
  **Whether the statutory *Mindestrückkaufswert* floor formally applies to the *Zeitwert* branch,
  or whether the five-year spreading in the *Beitragsverrechnung* is what discharges the obligation,
  is `[unverified]`** — gap 2. Both readings produce the same numbers on the delib design.
- ***Stornoabzug***: permissible **only if agreed, quantified and appropriate**, and **never for
  unamortised acquisition costs** [R1]. Many unit-linked tariffs therefore have **no *Stornoabzug*
  at all**. **The delib `[std]` is a zero *Stornoabzug***, with the parameter present and
  switchable, on the ground that a non-zero one would be an unsourced number attached to a
  contested clause.
- **Early values are nevertheless poor, and for a structural reason worth stating**: at the section
  4 levels, a contract surrendered in year 3 has had 15 % of every premium taken for acquisition
  plus the ongoing charges, so the *Rückkaufswert* is well below premiums paid even with a flat
  market. **That is not a penalty and there is no deduction** — it is the acquisition charge
  already spent. The delib worked example must display the first five years explicitly, because
  that is where the product's economics are least intuitive.
- **Timing**: surrender is effective at the *Bewertungsstichtag*, and the policyholder's
  termination right is short-notice [R2], so a unit-linked *Storno* is close to a fund redemption.
  **Lapse experience on this product is therefore market-sensitive** in a way conventional lapse is
  not; nothing quantitative was established (gap 18).

### 12. *Beitragsfreistellung*

- The policyholder may convert to a **paid-up** contract [R3]. On a fondsgebundene contract:
  premium payment stops; the units stay; the *beitragsbezogene* charges and the *Stückkosten* that
  are withheld from premium stop with the premium; and the ***kapitalbezogene Verwaltungskosten*,
  any *Stückkosten* charged by cancellation, and the *Risikobeitrag* continue to be taken by
  cancelling units**.
- **The paid-up contract therefore decays** at the fund-based charge rate less the fund's return.
  If the death benefit is a *garantierte Mindesttodesfallleistung*, the *Risikobeitrag* accelerates
  the decay as the fund falls and the net amount at risk rises — a feedback the model reproduces
  automatically and a real product risk.
- **Insurers set a minimum *Fondsguthaben* for paid-up status**, below which the contract is
  surrendered instead `[unverified]` as to level. `[std]` in delib.
- ***Beitragsfreistellung* and *Storno* are two decrements, not one.** They have different
  triggers, different cash flows and different subsequent projections, and the delib model treats
  them separately. Conflating them is a listed modelling pitfall.

### 13. Hybrid and guarantee variants — named, and deliberately not implemented

German insurers wrap three distinct guarantee technologies around this same unit-linked chassis.
They are named here because a reader of the delib model must know what the model is *not* doing,
and because the vocabulary is a German market invention with no English equivalent.

- ***Statisches Hybrid* (*Zwei-Topf-Hybrid*, static form).** The premium is split **once, at
  inception**, between the *Sicherungsvermögen* — where a guaranteed pot accretes at the
  *Rechnungszins* to exactly the guaranteed amount at *Rentenbeginn* — and free funds. The split is
  computed from the guarantee level, the term and the *Rechnungszins* and does not change. Simple,
  transparent, and at a low *Rechnungszins* it consumes almost the whole premium for the guarantee.
- ***Dynamisches Hybrid* (*Zwei-* or *Drei-Topf-Hybrid*).** The split is **recomputed
  periodically**, normally monthly, so that the guarantee remains secured while as much as possible
  sits in the funds. The **three-pot** form adds a middle pot — a ***Wertsicherungsfonds***, a fund
  with a contractual limit on its loss over a defined period — between the *Sicherungsvermögen* and
  the free funds, so that money can be moved out of equities in two steps rather than one.
- ***i-CPPI*** — individual Constant Proportion Portfolio Insurance. The exposure to the risky fund
  is set, **per policy and continuously**, as a multiplier times the cushion between the policy
  value and the present value of the guarantee. Guarantees are secured by the algorithm rather than
  by a static allocation. It is the most efficient of the three and the most path-dependent.
- ***Beitragsgarantie* levels.** Schicht 3 contracts are sold at 100 %, 90 %, 80 %, 60 % and 0 %
  of premiums paid `[unverified]` as to any distribution; the market moved decisively toward lower
  guarantees during the low-interest decade, and **100 % remains statutory only for Riester**.
- **Why the delib model does not implement any of them.** Every one of the three is a **rule for
  reallocating between a guaranteed pot and a risky pot along a path**. Its entire content is what
  it does when the risky pot falls. A deterministic gross best-estimate projection has **one path,
  and it is a smooth one**, so a guarantee mechanism modelled inside it either never triggers — in
  which case it is dead code presented as a feature — or triggers on a hand-chosen shock, in which
  case the model is asserting a scenario it has no basis for. **delib therefore models the pure
  unit-linked chassis, states the guarantee variants here, and says what would have to be added**:
  a stochastic or at minimum multi-scenario asset model, a monthly reallocation rule, a guaranteed
  pot accreting at a *Rechnungszins*, and a *Wertsicherungsfonds* return model. That is a different
  model, and an honest reference implementation says so rather than gesturing at it.
- **What the model *does* keep from the hybrid world**: the *Ablaufmanagement* glide (section 7),
  which is de-risking without a guarantee and is representable deterministically.

### 14. *Rechnungsgrundlagen* — two mortality bases, no interest basis

- **The accumulation phase has no interest basis at all.** There is no *Rechnungszins*, and the
  *Höchstrechnungszins* — 1,00 % from 2025, raised from 0,25 % [R12] `[unverified]` — **does not
  bind it**. That is the structural reason unit-linked business grew through the low-interest
  decade while classic business shrank.
- **The death charge is priced on a death table** — DAV 2008 T [R17], first order — and **the
  conversion guarantee on an annuity table** — DAV 2004 R [R16], generational, first order.
- **Best-estimate projection uses the second-order versions.** delib's cash flows are gross
  best-estimate, so the projection's decrement is second-order while the *charge* the model levies
  is the first-order one the tariff specifies. **The difference between them is the risk result**,
  and it is the source of the *Überschussbeteiligung* of section 15. A model that uses one table
  for both makes the risk result identically zero and loses the mechanic.
- **Unisex.** German new business has been unisex since the *Test-Achats* rule took effect in
  December 2012 `[unverified]` as to the date and instrument; a unisex tariff is a blend whose mix
  the insurer chooses. **No mix was established** and delib's proxy is a `[std]` unisex table.
- **DAV tables are not redistributed by this library** (house rules §6). delib ships `[std]`
  proxies anchored so the worked example reproduces exactly, cites the tables by name, and states
  what a replacement must preserve: for DAV 2004 R, a generational annuitant basis with a
  first-order margin; for DAV 2008 T, a death-risk basis at insured-life selection levels.

### 15. *Überschussbeteiligung* on a fondsgebundene contract

- **The investment result is not a surplus source here** — it belongs to the policyholder by
  construction. The surplus sources are the ***Risikoergebnis*** and the ***übriges Ergebnis***
  (the cost result), with statutory minimum policyholder shares under the MindZV [R14]
  `[unverified]` as to percentages.
- **Credited in one of three ways** `[unverified]` as to which carrier does which: as **additional
  *Anteileinheiten*** bought for the contract; as a **reduction of the charges** taken; or
  accumulated and paid as a ***Schlussüberschuss*** at *Rentenbeginn*.
- **Second-order in size, and delib does not project it.** The first-order economics of this
  product are fund return minus charges; a risk-and-cost surplus on a contract whose death cover is
  a *Beitragsrückgewähr* is small. The model omits it, states the omission, and records that the
  omission biases the projected *Fondsguthaben* **downward** — the honest direction for a charge
  demonstration.
- **The *Bewertungsreserven* limb of § 153 VVG** [R5] has almost nothing to attach to on a
  unit-linked contract, because the assets backing the unit liability are the units.

### 16. Taxation

- **Accumulation phase: nothing is taxed.** No annual taxation of fund income, no *Vorabpauschale*,
  and **no taxable disposal on a *Fondswechsel*** [R20]. This deferral is the product's principal
  commercial argument against holding the same funds in a *Depot*, where both apply. It is also the
  reason the *Effektivkosten* comparison against a direct ETF holding is not a like-for-like one.
- **Annuity: the *Ertragsanteil*** [R19]. Only the deemed interest component of each instalment is
  taxable, at a statutory percentage set by the annuitant's age at *Rentenbeginn* — **18 % at age
  65**, every other age `[unverified]`.
- **Lump sum: § 20 EStG** [R20]. Taxable amount = payment less premiums paid; **half of it** if the
  contract has run **at least 12 years and payment is after age 62**; otherwise all of it.
  ***Kapitalertragsteuer* is withheld by the insurer** `[unverified]` as to rate and surcharges.
- ***Teilfreistellung*** for the fund income inside a fondsgebundene wrapper — commonly stated as
  **15 %** for equity exposure `[unverified]` [R20] [R21]. This is the provision that makes the
  lump-sum route from a fondsgebundene contract more favourable than from a classic one, and it has
  no counterpart in the sibling products.
- **Two tax cohorts** exist in the German in-force book, split at **1 January 2005** `[unverified]`.
- **The *Kapitalwahlrecht* is a real economic choice**, not a formality: 18 % of every instalment at
  the marginal rate for life, against half of the total gain once, less a *Teilfreistellung*. The
  delib documents state the comparison and do not model the election's tax consequences, since the
  library publishes gross liability cash flows.

### 17. Fund return assumptions, PRIIPs scenarios, and the *Modellrechnung*

- **The model needs one number the market does not supply: an assumed gross fund return.** Nothing
  in this corpus establishes one, and PRIIPs deliberately does not provide one — its scenarios are
  **derived from the underlying's own return history** under the RTS methodology [R8], not chosen
  by the insurer.
- **What the *Basisinformationsblatt* shows instead** [R9]: **four scenarios — *Stress*,
  *pessimistisch*, *moderat*, *optimistisch* — as annualised average returns in per cent**, at
  **one year, half the holding period, and the end of it**, with **total costs and the RIY** at the
  same three points. For a fondsgebundene Rentenversicherung with a 30-year *Aufschubzeit* those
  points are roughly year 1, year 15 and year 30.
- **Category matters.** A pure unit-linked contract's scenarios come from the funds' history
  (Category 2 `[unverified]`); a guarantee-bearing or profit-participating one from the DAV
  standard method for Category 4 [R18]. **Two BIBs for economically similar products can therefore
  show very different scenario returns**, and no scenario figure transfers between carriers or
  between products. This is why the delib documents cite **no** scenario return.
- **The German *Modellrechnung*** required by the *VVG-InfoV* [R7] illustrates the maturity benefit
  at prescribed assumed rates. **The number of rates and their levels are `[unverified]`**; the
  market convention of illustrating a fondsgebundene contract at three graded rates is recorded as
  convention, not as law. Gap 23.
- **The delib `[std]` fund return** is a **single deterministic gross rate of 5,00 % p.a., less the
  fund TER of 0,45 % p.a., giving 4,55 % p.a. net of fund costs**, applied monthly. Rationale: it
  is a round, clearly-labelled assumption in the middle of the range a long-horizon equity-tilted
  mixed fund is generally assumed to earn; it is **not** a PRIIPs scenario, is not attributed to any
  document, and is a parameter the reader is expected to change. The `Ablaufmanagement` glide steps
  it down to a `[std]` **1,50 % p.a.** money-market rate over the last 60 months when switched on.
- **The projection is deterministic and the model says so.** Nothing in delib produces a
  distribution, so nothing in delib may be compared with a PRIIPs scenario.

### 18. Decrements and policyholder behaviour

- **Decrements in the *Aufschubzeit***: death (pays the *Todesfallleistung*, section 6), *Storno*
  (pays the *Rückkaufswert*, section 11), and *Beitragsfreistellung* (a change of state, not an
  exit, section 12). **Three states, not two.**
- **No German unit-linked *Stornoquote* was established** (gap 18). What is structurally true and
  worth stating: unit-linked lapse is **front-loaded** — highest in the first five years, where the
  acquisition charge is being taken and the value is furthest below premiums paid — and is
  **market-sensitive**, because the exit is at fund value on short notice [R1] [R2].
- **No *Beitragsfreistellung* rate and no *Kapitalwahlrecht* take-up rate was established** (gaps
  18, 19). All three behavioural assumptions in the delib documents are `[std]` and are labelled a
  modeller's view, per the house rules' three-way split of assumptions.
- **`[std]` behavioural defaults**, stated with their rationale rather than a source: a monthly
  lapse rate equivalent to **6 % p.a. in years 1–5, 3 % p.a. thereafter**, chosen to make the
  front-loading visible in the worked example; a **paid-up rate of 1 % p.a.**; and a
  ***Kapitalwahlrecht* take-up of 0 %** in the base run, so that the annuity path — the path the
  *Rentenfaktor* exists for — is the one the worked example demonstrates.

### 19. What is `[std]` and why — the register

Every quantitative parameter of this product falls into one of three groups. The first is empty.

- **Group 1 — established from a document read for this file: nothing.** No document was read.
- **Group 2 — corroborated in a sibling delib file and carried here with attribution**: the
  *Beitragsrückgewähr* death benefit shape [S2]; the *Rentenfaktor* per 10 000 € arithmetic and the
  *Treuhänder*/§ 163 story [R22]; the conversion basis DAV 2004 R at 0 % p.a. [S10]; the § 169 VVG
  *Zeitwert* branch and the *Stornoabzug* rules [R1]; the five-year spreading [R1]; the 25 ‰
  *Höchstzillmersatz* [R12]; the BIB content and its three time points [R9]; the *Effektivkosten*
  disclosure duty [R7]; BaFin's cost supervision [R10] [R11]; the *Ertragsanteil* at 65 [R19]; the
  12/62 rule [R20].
- **Group 3 — `[std]`, everything else.** Every charge level; the *Rentenfaktor* level; the fund
  return; the TER; all three behavioural rates; every minimum and maximum in the issue rules; the
  *Ablaufmanagement* schedule; the *Stornoabzug*. **Each carries a rationale in section 4, 9, 17 or
  18 above, and each appears in the gaps register with the kind of document that would replace it.**

---

## Observed variation across insurers

**Read the first sentence of this section before reading the tables.** Nothing carrier-specific was
observed for this product. No AVB, no *Produktinformationsblatt*, no *Basisinformationsblatt* and
no rate card was retrieved or searched. What follows is therefore **not** a table of observations;
it is a table of the **dimensions along which German carriers are known to differ**, with the range
argued from the mechanics and from the statutory bounds, and a companion table recording — honestly
and mostly negatively — what is actually established about each named carrier.

### What is established, carrier by carrier

| Carrier | Established here | Source |
|---|---|---|
| DEVK | Publishes a *Kundeninformation* for a fondsgebundene Rentenversicherung, doc 03101, ed. 07/2024; death benefit before *Rentenbeginn* = fund value, at least premiums paid | [S2], via the sibling file |
| CosmosDirekt (Cosmos Leben) | Inception annuity factor computed on DAV 2004 R at an interest rate of currently 0 % p.a. — stated for the **classic** tariff | [S10], via the sibling file |
| Allianz Leben | Current bases at *Rentenbeginn* are those used at that time for immediately beginning annuities; *Treuhänderklausel* position publicly defended in Feb 2021 | [S3] [R22], via the sibling file |
| Zurich Deutscher Herold | The *Verbraucherinformation* series is titled "für Konventionelle Versicherungen", implying a fondsgebundene companion; at *Rentenbeginn* the higher of two factors applies | [S4], via the sibling file |
| Debeka | Discontinued its classic annuity tariff — the market-structure fact behind this product's dominance | [S14], via the sibling file |
| NÜRNBERGER | Publishes per-tariff AVB with codes in an `NIR`/`N` series | [S11], via the sibling file |
| Alte Leipziger, LV 1871, Continentale, HDI, Volkswohl Bund, Stuttgarter, WWK, myLife | **Nothing.** Named as real carriers of the right product with `[unverified]` product names | [S5]–[S9] [S12] [S13] [S18] |

### The dimensions of variation, and the argued range on each

| Parameter | Argued range across the German market | Where delib sits | Tag |
|---|---|---|---|
| Death benefit shape | *Fondsguthaben* / *Beitragsrückgewähr* / 100–110% of fund / guaranteed sum | *Beitragsrückgewähr* | [S2] for the shape; range [unverified] |
| Acquisition charge | 0% (Nettotarif) to 2.5% of *Beitragssumme* (the cap) | 2.5%, the cap | [R12] [R13] for the cap; interior [std] |
| Acquisition spreading | 5 years, uniform — statutory, no variation | 60 months | [R1] |
| Premium-based admin | 2% to 10% of each premium | 4.0% | [std] |
| Fund-based admin | 0.10% to 1.20% p.a. of *Fondsguthaben* | 0.30% p.a. | [std] |
| *Stückkosten* | 0 to 5 EUR per month | 3.00 EUR | [std] |
| Fund TER | 0.15% (ETF) to 2.00% p.a. (active) | 0.45% | [std] |
| *Kickback* crediting | none to full crediting of the trail | none (passive fund) | [std]; rule [unverified] |
| *Effektivkosten* | a spread BaFin calls "considerable"; no numeric range established | approx. 1% p.a. implied | [R10]; level [std] |
| Guaranteed *Rentenfaktor* | no level, range or time series established anywhere | 25.00 EUR per 10 000 EUR at 67 | [std], derived in section 9 |
| Factor rule at *Rentenbeginn* | max(guaranteed, current) — appears uniform | max(guaranteed, current) | [S4] [R22] |
| *Rentengarantiezeit* | 0, 5, 10, 15 years | 10 years, not priced separately | [std] |
| *Beitragsgarantie* | 0%, 60%, 80%, 90%, 100% of premiums | 0% — no guarantee | [std]; menu [unverified] |
| Guarantee technology | none / static hybrid / dynamic 2- or 3-pot / i-CPPI | none | section 13 |
| *Ablaufmanagement* | absent, opt-in, or opt-out default; 3 to 10-year ramps | 5-year monthly glide, switchable | [std] |
| Free fund switches | a fixed annual allowance to unlimited | unlimited within modelled behaviour | [std] |
| *Stornoabzug* | zero at many unit-linked tariffs; where present, must be quantified | zero | [R1]; level [std] |
| Minimum monthly premium | 25 to 50 EUR | 25 EUR | [unverified]; [std] |
| Entry ages | roughly 15/18 to the low 60s | 18 to 60 | [unverified]; [std] |
| *Rentenbeginn* age | commonly 62 (tax floor) to 85 | 67 | tax floor [R20]; choice [std] |

### What the corpus supports as a representative design

The representative delib contract is a **pure fondsgebundene Rentenversicherung with no
*Beitragsgarantie***: a single-life, Schicht-3, monthly-premium deferred annuity, one fund, units
bought monthly out of the premium after an acquisition instalment spread over 60 months, a
premium-based and a fund-based administration charge plus a monthly *Stückkosten*, a
*Beitragsrückgewähr* death benefit whose net amount at risk is charged monthly by unit
cancellation, a guaranteed *Rentenfaktor* applied at *Rentenbeginn* as the higher of the guaranteed
and the current factor, a *Rückkaufswert* equal to the *Fondsguthaben* with no *Stornoabzug*, and
*Fondswechsel*, *Zuzahlung*, *Teilentnahme*, *Ablaufmanagement* and *Beitragsfreistellung* as
switchable options.

**Why that design and not another**, in four points, each of which is an argument rather than an
observation because no observation was available:

1. **No guarantee**, because the guarantee technologies of section 13 cannot be demonstrated
   honestly in a deterministic projection, and because the guarantee-free form is a real and
   growing market form rather than a simplification of the only one sold.
2. ***Beitragsrückgewähr* death benefit**, because it is the only death benefit shape with
   corroboration anywhere in the delib corpus [S2], and because it is the shape that makes the
   *Risikobeitrag* mechanic non-trivial without making it dominant — the net amount at risk is
   positive early and vanishes later, so the model must compute it every month rather than once.
3. **Acquisition charge at the statutory cap, spread over five years**, because the cap [R12] and
   the spreading [R1] are the two acquisition-cost facts with corroboration, and a reference
   implementation should demonstrate the binding constraint rather than an unsourced interior
   point.
4. **A derived rather than a quoted *Rentenfaktor***, because no market level exists anywhere in
   this corpus and a quoted one would be an invention; the derivation in section 9 from a 0 %
   *Rechnungszins* [S10] and a generational annuitant table [R16] is checkable arithmetic and the
   result is labelled `[std]` at every appearance.

**What a delib reader must not take from this file**: any charge level, any *Rentenfaktor*, any
lapse rate, any fund return, any market share, or any carrier's parameters. Those are gaps, and
they are enumerated next.

---

## Gaps and caveats

1. **No document was retrieved and no search was run for this product.** Both limits applied at
   full strength: HTTP egress was blocked for every relevant host, and the session's 200-call
   `WebSearch` budget was already exhausted before this file was begun. This file is therefore
   **weaker than its two delib siblings**, which at least had search summaries. Every statement of
   *structure* below the source list is written from the author's knowledge of German insurance
   practice; every statement of *level* is `[std]` or `[unverified]`.

2. **Whether the *Mindestrückkaufswert* floor reaches the *Zeitwert* branch is unresolved.**
   § 169 VVG expresses the five-year spreading floor on the *Deckungskapital*, and separately sends
   fondsgebundene contracts to a *Zeitwert* [R1]. The market implements the same protection inside
   the *Beitragsverrechnung*. Which of the two the statute requires, and what happens where the two
   diverge, was not established. Both readings give the same numbers on the delib design.

3. **The internal paragraph structure of § 169 VVG is unverified.** Whether the *Zeitwert* rule is
   Abs. 3 Satz 2 or Abs. 4, and what it cross-refers to in the VAG since the 2016 recast, was not
   established. No delib document may cite a subsection number for it.

4. **No *Rentenfaktor* level, range or time series was established** — not for this product, not
   for the classic one in the sibling file, not from the rating house whose article is titled with
   the question [R23]. The `[std]` 25,00 € per 10 000 € at 67 is **derived arithmetic**, not a
   market observation, and a reader who needs a market level must go to a current
   *Produktinformationsblatt* or a Franke und Bornberg / Morgen & Morgen comparison.

5. **No *Basisinformationsblatt* for a fondsgebundene Rentenversicherung was located.** The one
   German PRIIP-BIB located anywhere in the delib corpus is for an endowment [S15]. Consequently
   **no performance-scenario return, no total-cost figure and no RIY value** in this file comes from
   an actual BIB. This is the single document that would close gaps 4, 6, 7 and 23 at once.

6. **No charge level of any kind was established at any carrier.** Not one *Abschlusskostenquote*,
   not one *Verwaltungskostensatz* in either form, not one *Stückkosten* amount, not one
   *Effektivkostenquote*, not one commission rate. **The entire charge stack of section 4 is
   `[std]`.** The only anchor is the 25 ‰ *Höchstzillmersatz* [R12], itself corroborated only at
   the level of a secondary consumer page in a sibling file.

7. **BaFin's "differ considerably" is qualitative** [R10]. No numeric *Effektivkosten* threshold,
   band, median or industry norm was established, in this file or in the sibling ones. The
   "of the order of 1 % per annum" in section 5 is **arithmetic on delib's own `[std]` stack**, not
   a market figure, and must never be quoted as one.

8. **The treatment of *Kickbacks* is unresolved on two axes**: whether and on what conditions an
   insurer may retain a *Bestandsprovision* under the IDD-derived inducement rules [R15], and how a
   rebate credited back to the contract is treated inside the PRIIPs cost calculation [R7] [R8].
   delib sidesteps both by using a passive fund that pays no trail.

9. **The *Ausgabeaufschlag* waiver is assumed, not established.** German insurers are understood to
   buy policy units at the *Rücknahmepreis*; no wording confirming a full waiver was seen. delib
   assumes a full waiver as `[std]`.

10. **The *Bewertungsstichtag* convention was not established** for any carrier — how many dealing
    days after premium receipt units are bought, and which price applies to a death, a surrender or
    a switch. On a monthly grid this is immaterial; on a daily one it is not.

11. **The *Shift* / *Switch* terminology is not consistent across German insurers** and this file
    asserts no mapping between the English words and the two operations. Each AVB defines its own.
    delib names the operations, not the labels. Any delib document that asserts "Shift means X"
    without a wording in front of it is wrong.

12. **Free-switch allowances, switch fees, *Zuzahlung* minima and maxima, *Teilentnahme* minima and
    the minimum remaining *Fondsguthaben* were not established** at any carrier. All are `[std]`.

13. **Whether deferring the *Rentenbeginn* inside the *Abrufphase* restates the guaranteed
    *Rentenfaktor* or only the current one was not established**, nor was the width of the
    *Abrufphase*. delib fixes the *Rentenbeginn* and records the option as unmodelled.

14. ***Ablaufmanagement* parameters were not established**: whether it is opt-in or a default, over
    how many years, in what tranches, and into what. The five-year monthly glide is `[std]`.

15. **The Landgericht Köln *Rentenfaktor* decision could not be identified.** No case number, no
    date, no parties — in this file or in the sibling one that reported it [R22]. Any delib document
    that mentions it must do so without a docket.

16. **No BGH decision on *Rückkaufswert*, *Kostenverrechnung* or *Stornoabzug* is cited** [R26].
    The line of authority is well known and no case reference could be established without a
    search. Nothing in delib rests on a court holding.

17. **The *Beitragsrückgewähr* fact is single-sourced**, and the source is a search summary read by
    a sibling researcher, not by this one [S2]. It is the best-evidenced fact in the file and it is
    still one summary of one carrier's document. The other three death-benefit shapes in section 6
    are `[unverified]` in their entirety.

18. **No lapse rate, no paid-up rate and no German unit-linked *Stornoquote* was established.**
    The front-loaded and market-sensitive character of unit-linked lapse is a structural inference
    from the exit terms [R1] [R2], not an observation. All behavioural rates are `[std]`.

19. **No *Kapitalwahlrecht* take-up rate was established**, and it is the largest behavioural
    unknown in the product. delib's base run takes the annuity, which is a modelling choice made to
    exercise the *Rentenfaktor*, not an estimate of behaviour.

20. **The two-mortality-table statement is an inference from practice**, not from a wording: that
    the *Risikobeitrag* is priced on DAV 2008 T [R17] while the *Rentenfaktor* rests on DAV 2004 R
    [R16] is how German tariffs are built, but no AVB confirming it was seen. The DAV 2004 R half is
    corroborated at one carrier for the classic tariff [S10].

21. **The tax *Mindesttodesfallschutz* rule was not established for this product.** The
    "50 % rule" for contracts from 1 April 2009 is recorded in a sibling file for endowments; how it
    applies to a *Rentenversicherung* with and without a *Kapitalwahlrecht* is `[unverified]`, and
    delib's death benefit is not designed to satisfy it.

22. **The fondsgebunden *Teilfreistellung* is unverified in every particular** — the sentence within
    § 20 Abs. 1 Nr. 6 EStG, the 15 % figure, the equity-quota conditions and the interaction with
    the InvStG [R20] [R21]. The *Ertragsanteil* table is unverified except at age 65.

23. **The *Modellrechnung* requirement was not pinned down**: how many assumed rates the VVG-InfoV
    prescribes for a fondsgebundene contract and at what levels [R7]. The three-rate market
    convention is recorded as convention.

24. **No entry-age, premium, term or sum-insured envelope was established** at any carrier. Every
    issue rule in the delib product-spec is `[std]`.

25. **The opening claim that this is the dominant German new-business savings form is unsourced.**
    No GDV new-business split by *Versicherungsart* was established [R25]. What is corroborated is
    only that a major carrier withdrew its classic tariff [S14] and that the supervisor's cost
    agenda is framed around capital-forming products generally [R10] [R11].

26. **Hybrid mechanics are named and not specified.** No reallocation rule, no CPPI multiplier, no
    *Wertsicherungsfonds* loss limit, no guarantee-pot accretion rule and no carrier's guarantee
    menu was established [S7] [S8] [S9]. Section 13's taxonomy is a description of a market, not a
    specification of any product, and delib implements none of it.

27. **The *Überschussbeteiligung* of a fondsgebundene contract is described structurally and not
    quantified.** No crediting mechanism was confirmed at any carrier, no declared rate was
    established, and the MindZV percentages are `[unverified]` [R14] [R5]. delib omits the credit and
    states the direction of the resulting bias.

28. **Living texts.** VVG, VVG-InfoV, DeckRV, MindZV, VAG, EStG and InvStG all change; the PRIIPs
    RTS was reworked with effect from 1 January 2023 `[unverified]`; the *Höchstrechnungszins*
    changed on 1 January 2025 `[unverified]`; BaFin's focus-risk agenda is annual [R11]. **Every
    paragraph number and every date in this file is `[unverified]`** and must be re-checked against
    the instrument before anything in the delib product documents relies on it.
