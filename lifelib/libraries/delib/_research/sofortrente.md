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
