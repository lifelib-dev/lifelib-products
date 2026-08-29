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
