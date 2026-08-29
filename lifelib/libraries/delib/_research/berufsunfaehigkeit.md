# Selbständige Berufsunfähigkeitsversicherung (SBU) — research notes (Germany)

Research notes for the German individual *selbständige Berufsunfähigkeitsversicherung* — the
standalone occupational-disability contract that pays a monthly *BU-Rente* for as long as the
*versicherte Person* is *berufsunfähig*, waives the premium (*Beitragsbefreiung*) for the same
period, and pays nothing at all if the insured remains able to work. It is the flagship German
biometric product: the one contract the German market itself treats as indispensable, sold on a
statutory definition that is unusually favourable to the insured by international standards, and
priced on occupational classes whose spread is wider than in any other retail life product.

**In scope.** The individual, privately written, standalone (*selbständig*) BU contract on a single
life, sold by a *Lebensversicherungsunternehmen* under §§ 172–177 VVG, with a level *Bruttobeitrag*
guaranteed for the whole term, a *Zahlbeitrag* below it funded out of the *Überschussbeteiligung*,
an agreed monthly *BU-Rente*, an agreed *Endalter* for both cover and benefit, and the standard
option set (*Beitragsdynamik*, *Leistungsdynamik*, *Nachversicherungsgarantie*,
*Verlängerungsoption*, *Karenzzeit*, and — for medical occupations — the *Infektionsklausel*). The
*Berufsunfähigkeits-Zusatzversicherung* (BUZ), the same cover sold as a rider on a
*Rentenversicherung*, a *Kapitallebensversicherung* or a *Basisrente*, is treated here as a wrapper
variant of the same liability, because it is: the BU risk, the claim procedure, the *Nachprüfung*
and the *Beitragsbefreiung* are identical, and only the tax treatment and the interaction with the
host contract's premium differ.

**Out of scope, and said so where it matters.** *Erwerbsunfähigkeitsversicherung* (EU cover, keyed
to any occupation rather than the last one) and *Grundfähigkeitsversicherung* (keyed to the loss of
defined basic abilities — seeing, speaking, walking, using the hands) are different products with
different definitions and different pricing bases; they are named below only where they bound the
BU market from beneath. *Dread-disease* / *schwere Krankheiten* cover, *Unfallversicherung*,
*Krankentagegeld*, and the *Pflegerentenversicherung* (delib product 10) are separate liabilities.
*Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung* (including
the *Kollektiv-BU* and *bAV-BU* forms), *private Krankenversicherung* and the statutory
*Erwerbsminderungsrente* itself are outside the delib library; the last of these is nevertheless
described at length in section 25, because the German BU contract is designed as a top-up on it and
its level is the reason the private product exists at all.

These notes are the **citation ground truth** for the delib `berufsunfaehigkeit` product documents.
Source ids **S1..S16** and **R1..R30** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.
Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

**No document in this file was retrieved. Not one.** Two independent limits applied while it was
written, and they compound.

**Limit 1 — direct HTTP egress is blocked.** An organisation network policy refuses `WebFetch` and
`curl` (HTTP 403 at the egress gateway) for every host outside a short package-registry allowlist.
The hosts that matter for this product were all tried and all refused:
`gesetze-im-internet.de` (VVG, VAG, SGB VI, EStG, DeckRV, MindZV, IfSG), `bafin.de`, `gdv.de`,
`aktuar.de` (Deutsche Aktuarvereinigung), `deutsche-rentenversicherung.de`,
`bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `buzer.de`, `bundesgerichtshof.de` and
`de.wikipedia.org`. No *Bedingungswerk*, no *Produktinformationsblatt*, no *Basisinformationsblatt*,
no statutory text, no DAV *Ergebnisbericht* and no BaFin publication was opened.

**Limit 2 — the session's `WebSearch` budget was already exhausted before this product was
reached.** The 200-call cap is shared across the whole delib build and was consumed by the
regulatory and contract-law research and by the two products written before this one. **This file
therefore had no research channel at all — neither retrieval nor search.** It is written from the
author's own knowledge of German insurance law and market practice, under the discipline that the
delib house rules impose for exactly this case.

What follows from that, and it governs every line below:

1. **An `[S#]` or `[R#]` tag in this file is a pointer, not a certificate.** It names the document a
   claim must be checked against before it is relied on. It does **not** assert that anyone read
   that document. Every source entry carries
   `Retrieved: no — direct HTTP egress blocked in the build environment; no search corroboration
   (session search budget exhausted)`, and none of them says anything else.
2. **There are no quotations.** Not one German sentence in this file is presented as verbatim
   statutory or contractual wording, because no wording was read. Where the substance of a provision
   is given it is given in the author's own words, in English, with the German terms of art kept in
   German. Any reader who needs the wording must go to the instrument.
3. **No URL, document number, edition date, *Bundesgesetzblatt* citation or page count is invented.**
   Where a canonical URL form is confidently known — `https://www.gesetze-im-internet.de/vvg_2008/__172.html`
   for § 172 VVG — it is given and marked `[unverified]`, because no search returned it. Everywhere
   else the entry says `URL: not established`.
4. **`[unverified]` is used generously.** Every specific paragraph number, effective date, monetary
   amount, percentage, market share, table name and statistic below carries it, because nothing
   confirmed any of them. It is *not* applied to the general shape of a well-established mechanic —
   that the *Nachprüfung* exists, that the market waives the *abstrakte Verweisung*, that the
   premium is quoted as a *Brutto*/*Zahlbeitrag* pair — because tagging those would drown the
   signal. The rule is: the moment a claim becomes **specific and numeric**, it needs the tag.
5. **Uncertain levels are `[std]` parameters, not citations.** Where the mechanic is certain and the
   level is not — a lapse rate, an occupational rating factor, a *Beitragsverrechnung* ratio, a
   *Wiedereingliederungshilfe* amount — this file ships a `[std]` value with a stated rationale and
   an argued plausible range, and the product documents carry it forward as `[std]`. A `[std]`
   number is honest about being a construction. A guessed `[S4]` number is not, and there are none.

**Consequence for the downstream documents.** `product-spec.md` and `technical-notes.md` for this
product will be unusually `[std]`-heavy and unusually explicit about it. That is the correct
outcome, not a defect: the *mechanics* of the German BU contract are well established and are set
out below in full, and it is only the *levels* — the rating factors, the charge loadings, the
decrement tables, the market statistics — that this file cannot source. The gaps register at the
foot of this file is a substantial part of its value and should be read before any figure in it is
used.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Berufsunfähigkeit* (BU) | Occupational disability: inability to follow the **last exercised occupation**, as it was arranged before the impairment |
| *Selbständige Berufsunfähigkeitsversicherung* (SBU) | The standalone BU contract, sold on its own rather than as a rider |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | The same cover written as a rider on a *Renten-*, *Kapitallebens-* or *Basisrentenversicherung* |
| *BU-Rente* | The monthly disability annuity, the product's only substantive benefit |
| *Versicherte Person* / *Versicherungsnehmer* | The life insured / the policyholder — frequently the same person here, but not necessarily |
| *Zuletzt ausgeübter Beruf* | The last exercised occupation — the reference occupation for the whole test |
| *Lebensstellung* | Standing in life: the income level and social position the reference occupation conferred. The limiting concept for any *Verweisung* |
| *Abstrakte Verweisung* | Referring the insured to an occupation they *could* take up, without their actually doing so |
| *Konkrete Verweisung* | Referring the insured to an occupation they **actually** exercise |
| *Prognosezeitraum* | The forward-looking period over which the inability must be expected to last — six months in the market standard |
| *Karenzzeit* | An agreed deferment between the onset of BU and the first benefit payment |
| *Rückwirkende Leistung* | Benefit paid retroactively to the onset of BU once the claim is recognised |
| *Leistungsantrag* | The claim application |
| *Anerkenntnis* | The insurer's declaration that it accepts liability. *Befristetes Anerkenntnis* = a time-limited one |
| *Leistungsprüfung* | The insurer's assessment of the claim |
| *Nachprüfung* / *Nachprüfungsverfahren* | The periodic re-examination of a claim already accepted |
| *Einstellungsmitteilung* / *Änderungsmitteilung* | The notice by which the insurer ends benefit after a *Nachprüfung* |
| *Reaktivierung* | Recovery: the insured ceases to be *berufsunfähig* and the contract reverts to premium-paying cover |
| *Beitragsbefreiung* | Waiver of premium while the BU benefit is in payment |
| *Leistungsdauer* / *Versicherungsdauer* | The period benefits may run for / the period during which a BU may incept and be covered |
| *Endalter* / *Leistungsendalter* | The attained age at which the *Leistungsdauer* ends — 65 or 67 in the market |
| *Wiedereingliederungshilfe* | A lump sum paid to support a return to work |
| *Umorganisationspflicht* | The self-employed insured's duty to reorganise the business before claiming |
| *AU-Klausel* / *Arbeitsunfähigkeitsklausel* | Benefit triggered by a certificate of six months' *Arbeitsunfähigkeit*, without a BU determination |
| *Infektionsklausel* | Treats an official ban on practising imposed for infection reasons as BU, for medical occupations |
| *Beitragsdynamik* / *Leistungsdynamik* | Annual pre-claim escalation of premium and *BU-Rente* / annual escalation of the *BU-Rente* in payment |
| *Nachversicherungsgarantie* | The right to increase the *BU-Rente* on defined life events without renewed underwriting |
| *Verlängerungsoption* | The right to extend the *Endalter* without renewed underwriting |
| *Berufsgruppe* | Occupational rating class |
| *Gesundheitsprüfung* / *Gesundheitsfragen* | Medical underwriting / the application's health questions |
| *Risikozuschlag* / *Ausschlussklausel* | Extra-risk premium loading / exclusion of a named condition |
| *Risikovoranfrage* | Anonymous pre-application enquiry, made to avoid a recorded decline |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure, § 19 VVG |
| *Bruttobeitrag* (*Tarifbeitrag*) / *Zahlbeitrag* (*Nettobeitrag*) | The guaranteed maximum premium / the premium actually charged after surplus is applied |
| *Beitragsverrechnung* | Applying surplus as an immediate reduction of the premium charged — the standard *Überschussverwendung* in BU |
| *Überschussbeteiligung* | Participation in surplus, § 153 VVG, applied to BU through § 176 VVG |
| *Deckungsrückstellung* / *Rückkaufswert* | The actuarial reserve / the surrender value, § 169 VVG via § 176 |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs through the reserve / its statutory cap |
| *Rechnungsgrundlagen erster / zweiter Ordnung* | Prudent (pricing and reserving) bases / best-estimate bases |
| *Invalidisierungswahrscheinlichkeit* / *Reaktivierungswahrscheinlichkeit* | Probability of becoming BU / of recovering from it |
| *Anerkennungsquote* | The proportion of decided claims the insurer accepts |
| *Erwerbsminderungsrente* (EM-Rente) | The statutory disability pension, §§ 43, 240 SGB VI — *volle* and *teilweise* |
| *Versorgungslücke* | The gap between the statutory pension and the income it has to replace |
| *Angemessenheitsgrenze* | The insurer's cap on the insurable *BU-Rente* as a fraction of income |

---
