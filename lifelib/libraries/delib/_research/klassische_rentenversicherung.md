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
  and **indexgebundene / "Neue Klassik"** hybrids (delib `indexpolice`). These are referenced only
  where a document covers both and the classic mechanics are visible through the contrast — the
  *Rentenfaktor* literature in particular is dominated by unit-linked marketing material [R19]
  [R22] [R29], because in a unit-linked contract the *Rentenfaktor* is the **only** guarantee, and
  the DEVK and Zurich unit-linked wordings [S19] are used solely for that contrast.
- **Sofortbeginnende Rentenversicherung** (immediate annuity, delib `sofortrente`). The payout
  phase of this product and the whole of that one are the same machinery; the Zurich
  *sofort beginnende Rentenversicherung* consumer information [S16] is recorded here because
  German insurers derive the *aktueller Rentenfaktor* of a deferred contract from the tariff they
  are then writing for immediate annuities [S13] [R27], which makes the immediate-annuity document
  the direct evidence for the deferred contract's conversion basis.
- **Kapitalbildende Lebensversicherung** (endowment, delib `kapitallebensversicherung`). It shares
  the entire *Überschussbeteiligung* chassis and the entire *Deckungskapital* / *Rückkaufswert*
  chassis with this product; the difference is only what happens at the end of the accumulation
  phase. Facts that belong to the shared chassis are recorded here anyway, because this file must
  stand alone, but the endowment file is the primary home for the four surplus components.
- **Gruppenversicherung**, **private Krankenversicherung**, **Sterbegeldversicherung** and
  institutional pension-risk transfer.

These notes are the citation ground truth for the delib `klassische_rentenversicherung` product
documents: source ids **S1..S18** and **R1..R28** below are **frozen — never renumber**. Unused
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
   `[unverified]`; a paragraph number, an effective date, a tariff level or a market figure that
   no search result confirmed **is**.

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
| *aufgeschobene Rentenversicherung* | deferred annuity contract: premiums are paid over an accumulation period and the annuity starts later |
| *Aufschubzeit* / *Aufschubdauer* | deferment period, from inception to *Rentenbeginn* |
| *Rentenbeginn* | annuity commencement date; the contractual boundary between accumulation and payout |
| *Rentenbezugsphase* / *Rentenphase* | payout phase, the period over which the annuity is in payment |
| *Leibrente* | life annuity: payable for as long as the annuitant lives |
| *Deckungskapital* | the policy's accumulated reserve; the per-policy quantity the recursion rolls forward |
| *Deckungsrückstellung* | the statutory technical provision held for the contract (HGB/VAG); referenced, never specified in delib |
| *Rechnungszins* | technical interest rate used in the tariff; the rate at which the *Deckungskapital* is guaranteed to accumulate |
| *Höchstrechnungszins* (*Garantiezins*) | the statutory maximum *Rechnungszins* for new business, set in the *Deckungsrückstellungsverordnung* |
| *Sparbeitrag* | the savings portion of the premium — what is left after the risk and expense charges |
| *Risikobeitrag* | the risk portion of the premium |
| *Überschussbeteiligung* | profit participation: the policyholder's share of the insurer's surplus |
| *Überschussanteile* | the declared surplus amounts credited to a contract |
| *laufende Überschussbeteiligung* | the annually declared, running surplus |
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
| *Kapitalwahlrecht* | the policyholder's option to take the accumulated capital as a lump sum instead of the annuity |
| *Kapitalabfindung* | the lump sum itself |
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
| *Verantwortlicher Aktuar* | the appointed actuary |
| *Sicherungsvermögen* | the ring-fenced general account backing guarantees |
| *Zinszusatzreserve* | the additional interest reserve German insurers built against legacy guarantees |

---
