# German regulatory and actuarial reference library — annotated bibliography

Cross-product references for Germany life insurance liability cash flow modeling. Compiled
**2026-08-29** (all access dates 2026-08-29). Citation ids **R1–R56 are frozen**: the ten delib
product documents and the library's `references/regulatory-and-actuarial-references.md` cite
these tags verbatim as `[REG-R#]`; **never renumber**. Unused ids are omitted downstream,
leaving gaps, and each `sources.md` records which ids are absent and why.

This file is the citation ground truth for everything in `delib` that is not a primary product
document. It carries no `S#` sources: an insurer's *Allgemeine Versicherungsbedingungen*, its
*Produktinformationsblatt*, its *Basisinformationsblatt* and its *Tarifblatt* belong in the ten
per-product research files and are cited there. What is here is the *law, the regulation, the
supervisory practice, the professional standards, the tax architecture and the market
aggregates* that all ten products sit inside.

The file is organised into five domains — prudential and supervisory (R1–R21), contract law and
conduct (R22–R37), tax and the three-layer state-subsidised pension architecture (R38–R46),
biometric bases and market statistics (R47–R53), and accounting and professional standards
(R54–R56) — and then, after the entries, into *extracted specifications organised by mechanic*,
*variations across insurers*, and a **gaps and caveats register** that is a substantial part of
the document's value rather than a formality.

---

## Retrieval conditions — read this before using a single line below

This is the most important section in the file and it is unlike anything the sister libraries
`uslib`, `uklib`, `jplib` and `frlib` had to record. Two independent limits applied while
`delib` was built, and both are stated here without softening.

**1. No document cited anywhere in this file was retrieved.** Direct HTTP egress from this
build environment is blocked by an organisation network policy: `WebFetch` and `curl` are
refused with **HTTP 403 at the egress gateway** for every host outside a short
package-registry allowlist. The hosts that matter for German life insurance were all tried and
all refused:

| Host | What it would have served | Result |
|---|---|---|
| `gesetze-im-internet.de` | VAG, VVG, DeckRV, MindZV, RfBV, RechVersV, BerVersV, HGB, EStG, AltZertG, ZPO, SGB V/VI/XI | refused, HTTP 403 |
| `bafin.de` | Rundschreiben, Auslegungsentscheidungen, Merkblätter, Erstversicherungsstatistik, Jahresbericht | refused, HTTP 403 |
| `aktuar.de` | DAV press releases, Zinsberichte, Fachwissen fact sheets | refused, HTTP 403 |
| `gdv.de` | *Die deutsche Lebensversicherung in Zahlen*, statistics pages, Musterbedingungen | refused, HTTP 403 |
| `bundesfinanzministerium.de` | Referentenentwürfe, BMF-Schreiben, Muster-Produktinformationsblatt | refused, HTTP 403 |
| `destatis.de` | Sterbetafeln, Generationensterbetafeln, Pflegestatistik | refused, HTTP 403 |
| `dejure.org` | statute mirrors, BGBl citations, case-law cross-references | refused, HTTP 403 |
| `eur-lex.europa.eu` | Solvency II, the Delegated Regulation, PRIIPs, the IDD | refused, HTTP 403 |
| `de.wikipedia.org` | general-reference corroboration | refused, HTTP 403 |

Not one statutory text, not one BaFin circular, not one DAV table, not one BGH judgment and not
one statistical release was opened. **A delib citation is a pointer, not a certificate.** It
names the instrument a claim should be checked against; it does not assert that anyone checked
it. That is a weaker thing than an frlib citation, where Légifrance served in full, and the
difference is stated rather than glossed.

**2. The only research channel was `WebSearch`, and its budget ran out mid-build.** The session
carries a 200-call `WebSearch` budget. `WebSearch` returns titles, URLs and a search-engine
summary of the matched pages — real evidence, which does return substantive content (several
long German sentences of statutory wording reached this library that way), but a *secondary
summary*, never a retrieved document. The budget was consumed as follows and was **exhausted**
before the sweep finished:

- the **prudential, supervisory and accounting** sweep ran roughly **35** German-language
  queries and recorded, per fact, how many independent publishers agreed;
- the **contract law, conduct and disclosure** sweep ran roughly **45** German-language queries
  on the same discipline;
- the ten **per-product** sweeps consumed most of the remainder;
- the **tax** sweep issued two queries and **both were refused** for budget — it ran **zero**
  successful searches;
- the **biometric bases and market statistics** sweep issued two queries and **both were
  refused** — it also ran **zero** successful searches;
- the compilation of this file issued one confirming query, which was likewise refused.

**What follows, exactly, and it applies to every entry below.**

- **Every entry records its retrieval status honestly.** The form is
  `Retrieved: no — direct HTTP egress blocked in the build environment`, followed by
  `; corroborated by web search` with the query and publisher counts where a sweep recorded
  them, or `; no search corroboration (session search budget exhausted)` where none exists.
  **The words `Retrieved: yes` appear nowhere in this library.**
- **No verbatim quotation below is attributed to an instrument.** Where a German sentence
  appears in quotation marks, the quotation is **of a search-result summary**, not of the
  statute, and the entry says so. What an instrument *provides* is written in the compiler's
  own words.
- **No URL below is fabricated.** A URL appears only where (a) a search result actually
  returned it — the great majority of the URLs in R1–R37 are of this kind — or (b) it is the
  obvious canonical `gesetze-im-internet.de` section form
  `https://www.gesetze-im-internet.de/<slug>/__<section>.html`, whose pattern dozens of
  returned pages confirm, in which case it carries `[unverified]`. Where neither holds the
  entry says **not established**. No Bundesgesetzblatt citation, document reference number or
  page count is invented.
- **`[unverified]` is used generously and means what it says.** It is applied to every specific
  paragraph number, effective date, monetary amount, percentage and market figure that no
  search result confirmed. It is *not* applied to the general shape of a well-established
  mechanic, because that would drown the signal — but the moment a claim becomes *specific and
  numeric* it carries either a corroborated source or the tag.
- **Corroboration is graded, and the grades are not equal.** Statutory *titles and section
  numbers* that came back identically from five to ten independent publishers
  (`gesetze-im-internet.de`, `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`,
  `freirecht.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `rewis.io`, `haufe.de`) are
  **strongly corroborated** — those are mirrors of one official text but independent
  publishers, so agreement on a title is strong. Statutory *substance* summarised by one to
  three of them is **moderately corroborated**. A figure from a single trade-press page is
  **single-source**. A claim with no search behind it at all is **general knowledge**, and
  every one of those is tagged.
- **Prefer to say less, precisely, than more, loosely.** Where a figure is needed by the
  reference implementation and cannot be confirmed, the honest form downstream is a `**[std]**`
  parameter with a stated rationale and, where possible, an argued plausible range — **not** a
  `[REG-R#]` citation. A `[std]` number is honest; a wrong `[REG-R#]` number is not.

**The uneven evidence base, stated once.** The five domains of this file are **not** equally
supported, and the reference library must not present them as if they were:

| Domain | Entries | Evidence behind it |
|---|---|---|
| Prudential and supervisory | R1–R21 | ~35 German queries; statutory titles across 5–10 publishers; substance across 1–3 |
| Contract law and conduct | R22–R37 | ~45 German queries; the strongest block in the library, with several summaries reproducing statutory wording |
| Tax and the three layers | R38–R46 | **zero successful searches**; second-hand corroboration from the two sweeps above, otherwise general knowledge |
| Biometric bases and market statistics | R47–R53 | **zero successful searches**; the market aggregates are second-hand from the prudential sweep, the tables are general knowledge |
| Accounting and professional standards | R54–R56 | partial: HGB/RechVersV/BerVersV and IFRS 17 came from the prudential sweep; the DAV standards did not |

The **tax layer and the biometric layer are the least-verified parts of `delib`**, and every
product document that touches them says so in its own header.

**One structural warning that governs the whole biometric section.** The five tables at the
centre of German life pricing — **DAV 2008 T**, **DAV 2004 R**, **DAV 2004 R-Bestand**,
**DAV 1997 I / RI / TI** and **DAV 2008 P** — are the property of the Deutsche
Aktuarvereinigung, are distributed to members and licensees rather than published, and are
**not redistributable**. `delib` ships **none of them**, quotes **no $q_x$ or incidence value
from any of them**, and every decrement CSV in the library is a `**[std]**` proxy anchored so
that the product's own worked example reproduces exactly. That is the same posture `frlib`
took towards TH 00-02 and TGH05, and it is not a workaround: it is the only lawful and honest
way to ship a public reference library against a proprietary basis.

---

## A note on German terminology

`delib` is written in **English prose about German products**. Product names, statutory terms
and document titles stay German, italicised on first use with a gloss, and are then used
untranslated. Tables and headings are in English. The following terms carry the library and are
worth fixing here once, because several of them have no English equivalent and two of them are
routinely mistranslated.

**The surplus chassis.**

- ***Überschussbeteiligung*** — the policyholder's participation in the insurer's surplus. It
  is **not** the French *participation aux bénéfices* and should never be rendered that way in
  a comparative sentence: the French version is a *collective statutory minimum* computed from
  a regulated account, whereas the German version is an **individual contractual entitlement**
  (§ 153 VVG, R24) with a **statutory minimum transfer to a reserve** on top (the MindZV, R18).
  Two instruments, two mechanics.
- ***Rückstellung für Beitragsrückerstattung (RfB)*** — the balance-sheet provision into which
  surplus earmarked for policyholders goes if it is not credited immediately (§ 139 Abs. 1 VAG,
  R9). Market writing splits it into ***gebundene*** and ***freie RfB***; the statutory
  vocabulary is ***ungebundene*** RfB (RfBV, R19) and the ***Schlussüberschussanteilfonds***
  (§ 28 RechVersV, R54). `delib` defines both pairs once and then uses the market terms.
- ***Direktgutschrift*** — surplus credited to the contract immediately rather than parked in
  the RfB. It is **deducted** from the MindZV minimum (R18), which is why the MindZV is a
  minimum *transfer*, not a minimum *payout*.
- ***Abrechnungsverband*** — the sub-portfolio for which a declaration is made. Declared
  *Überschussanteilsätze* are published per *Abrechnungsverband* in the *Anhang* of the German
  statutory accounts by force of § 28 Abs. 8 RechVersV (R54).
- ***laufende Verzinsung*** — the declared annual credited rate. It is the ***Garantieverzinsung
  plus the laufende Zinsüberschussbeteiligung***, **not** a surplus rate on top of the
  guarantee. Adding a declared *laufende Verzinsung* to the guaranteed rate is the single most
  common arithmetic error in describing a German contract and it is a numbered pitfall in every
  affected product. ***Gesamtverzinsung*** adds the *Schlussüberschussanteil* and any
  *Bewertungsreserven* share.
- ***Schlussüberschussanteil*** — the terminal bonus, declared but not vested until maturity.
- ***Bewertungsreserven*** — unrealised gains on the insurer's assets. § 153 Abs. 3 VVG (R24)
  gives the policyholder half of the amount attributed to the contract on termination; § 139
  Abs. 3 and 4 VAG (R9) then subtracts a ***Sicherungsbedarf*** from the fixed-income pool
  first, and the BGH has held that constitutional (R36).

**Reserving and pricing.**

- ***Deckungsrückstellung*** — the German statutory (HGB) reserve, prospective, computed on the
  *Rechnungsgrundlagen* of the premium calculation (§ 341f HGB, R54; DeckRV, R14). It is **not**
  the Solvency II best estimate, and the whole German picture depends on keeping the two apart:
  an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
  *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side.
- ***Deckungskapital*** — the contract-level reserve, the base measure of the *Rückkaufswert*
  under § 169 VVG (R28).
- ***Höchstrechnungszins*** — the maximum rate at which the *Deckungsrückstellung* may be
  discounted, fixed in § 2 DeckRV (R14). Market language calls it the *Garantiezins*; the two
  are not legally identical, because § 2 caps the **reserving** rate and the guaranteed rate a
  policy carries is a tariff decision that may be lower.
- ***Rechnungszins*** — the rate a particular tariff actually uses, at or below the cap; it
  stays with the contract for its whole term, which is why a German in-force book is a stack of
  cohorts (R15).
- ***Zillmerung*** — offsetting a contract's one-off acquisition costs against its first
  premiums, capped at **25 ‰** of the *Beitragssumme* by § 4 DeckRV since 1 January 2015 (R16).
- ***Zinszusatzreserve (ZZR)*** — the additional HGB reserve that arises when the § 5 Abs. 3
  DeckRV *Referenzzins* falls below a contract's tariff rate (R17). It exists in no other
  jurisdiction in this repository.
- ***Rechnungsgrundlagen erster / zweiter Ordnung*** — first-order (prudent, pricing and
  reserving) and second-order (best-estimate) bases. The wedge between them is the
  ***Sicherheitszuschlag***, and its systematic release is the *Risikoüberschuss* (R47). This
  distinction is the German name for the three-way assumption split every delib
  `technical-notes.md` uses.

**Contract mechanics.**

- ***Rückkaufswert*** — the surrender value (§ 169 VVG, R28), floored at the *Deckungskapital*
  that results from spreading the charged acquisition and distribution costs evenly over the
  **first five contract years**.
- ***Stornoabzug*** — the surrender deduction, permitted only if *vereinbart, beziffert und
  angemessen* (§ 169 Abs. 5 VVG, R28).
- ***Beitragsfreistellung*** / ***prämienfreie Versicherung*** — conversion to a paid-up policy
  (§ 165 VVG, R28). In Germany this is a **distinct decrement from surrender**, not a variant
  of it, and a model that implements only surrender has modelled the wrong book.
- ***Bruttobeitrag*** and ***Zahlbeitrag*** — the tariff premium and the premium actually
  collected after surplus is applied as a *Beitragsverrechnung*. The gap is large and
  persistent in *Berufsunfähigkeit* (R53) and the *Zahlbeitrag* is **not guaranteed**.
- ***Rentenfaktor*** — euros of monthly annuity per €10,000 of accumulated capital; the number
  that converts a unit-linked or index account value into an annuity. The BGH struck down
  asymmetric unilateral reduction clauses in 2025 (R36).
- ***Beitragsgarantie*** — a guarantee that at least the contributions paid are available at
  the start of the payout phase; statutory for a certified Riester contract (R43).
- ***Berufsunfähigkeit*** — inability to pursue **the last occupation as it was structured
  before the impairment** (§ 172 Abs. 2 VVG, R29). It is *not* "disability" in the
  general-labour-market sense; the statutory scheme's *Erwerbsminderung* is that, and the two
  use different definitions of the same event (R53).
- ***Pflegegrad*** — one of the five care levels of § 15 SGB XI, which replaced the three
  ***Pflegestufen*** on 1 January 2017 (R51). The replacement is a **definitional break**, not
  a change in the underlying risk, and the BGH has refused to map the two scales (R36).

**Institutional vocabulary.**

- ***Altbestand*** / ***Neubestand*** — contracts concluded before / from **29 July 1994**, the
  deregulation date (R11). All ten delib products are **Neubestand** business and every product
  document says so.
- ***Verantwortlicher Aktuar*** — the statutory responsible actuary of § 141 VAG (R11), who
  makes the written proposal on the *Überschussbeteiligung*. Distinct from the Solvency II
  ***versicherungsmathematische Funktion*** of the MaGo (R21); `delib` does not conflate them.
- ***Sicherungsvermögen*** — the ring-fenced asset pool (§ 125 VAG, R7); ***Anlagestock*** is
  the segregated section of it that backs unit-linked benefits.
- ***Sicherungsfonds*** — the statutory guarantee scheme (§§ 221 ff. VAG), whose tasks are
  carried by **Protektor Lebensversicherungs-AG** (R12).
- ***Drei-Schichten-Modell*** — the three-layer sorting of retirement products introduced by
  the *Alterseinkünftegesetz* with effect from 1 January 2005 (R38). Schicht 1 is the
  *Basisversorgung* including the ***Basisrente*** (Rürup); Schicht 2 the subsidised
  supplementary layer including the ***Riester-Rente***; Schicht 3 everything unsubsidised.

---

## The German regulatory architecture in one page

**Who supervises what.** German insurance supervision is exercised by the **Bundesanstalt für
Finanzdienstleistungsaufsicht (BaFin)**, created in **2002** by the *Finanzdienstleistungs-
aufsichtsgesetz* of **22 May 2002** out of the three predecessor authorities for banking,
securities and insurance; the merger was organisational and did not create new competences
[R21]. BaFin is subject to the *Rechts- und Fachaufsicht* of the **Bundesministerium der
Finanzen**, and supervises under the KWG, the **VAG** and the WpHG. Its stated main objective
in insurance is to *ensure the permanent fulfilment capability of insurance contracts* — the
***dauernde Erfüllbarkeit*** standard, which reappears verbatim in § 138 Abs. 1 VAG on premium
adequacy [R8] and in § 341e HGB on technical provisions [R54] — together with the protection of
the insured and beneficiaries [R21]. German usage splits the function into *Finanzaufsicht*
(solvency), *Rechtsaufsicht* (proper conduct of business) and *Missstandsaufsicht*.

There is **no second national insurance supervisor**. Unlike France, where the ACPR and the AMF
share competence over unit-linked distribution, and unlike the United Kingdom's twin peaks,
Germany runs conduct and prudential supervision inside one authority. The consequences are
visible in this file: the same body issues the *Auslegungsentscheidungen* that govern how the
MindZV minimum allocation works in unit-linked business [R21] and the *Merkblatt* that tells
insurers their savings products must deliver an *angemessener Kundennutzen* [R35]. Above BaFin
sits **EIOPA**, whose published risk-free curves are made binding on German undertakings by
§ 83 VAG [R6][R4].

**Why a German life model reads VAG and VVG and DeckRV and MindZV together.** This is the
single most important structural fact about the German market, and it has no counterpart in the
sister libraries. France puts prudential rules and contract law in **one** code — the *Code des
assurances*, Livre III and Livre I. Germany splits them across **two statutes with different
addressees**, and then delegates the arithmetic to **two regulations**:

- The **VAG** (*Versicherungsaufsichtsgesetz* 2016) is **supervisory law**. It binds the
  undertaking to the supervisor. It says how the balance sheet is valued (§§ 74–88), how much
  capital is required (§§ 96–110), how the assets must be invested (§§ 124–125), that premiums
  must be *auf der Grundlage angemessener versicherungsmathematischer Annahmen* and adequate to
  fund the *Deckungsrückstellung* (§ 138), that surplus earmarked for policyholders goes into
  the RfB (§ 139) and may be used only for them (§ 140), and that a named
  *Verantwortlicher Aktuar* proposes the declaration (§ 141). It gives the policyholder no
  claim.
- The **VVG** (*Versicherungsvertragsgesetz* 2008) is **contract law**. It binds the insurer to
  the policyholder. Its Kapitel 5 (§§ 150–171) supplies the entitlement to
  *Überschussbeteiligung* (§ 153), the right to convert to paid-up (§ 165), the right to
  surrender and the surrender-value floor (§§ 168–169) and the withdrawal right (§ 152); and
  § 171 makes almost all of them ***halbzwingend*** — variable in the policyholder's favour
  only. Kapitel 6 (§§ 172–177) does the same for *Berufsunfähigkeit*.
- The **DeckRV** (*Deckungsrückstellungsverordnung*, 18 April 2016) is made under **§ 88 Abs. 3
  VAG** and fixes the *Rechnungsgrundlagen* of the statutory *Deckungsrückstellung*: the
  *Höchstrechnungszins* (§ 2), the *Höchstzillmersatz* (§ 4) and the *Referenzzins* that
  generates the *Zinszusatzreserve* (§ 5 Abs. 3).
- The **MindZV** (*Mindestzuführungsverordnung*, 18 April 2016) is made under **§ 145 VAG** and
  turns § 139's "put it in the RfB" and § 140's "use it only for policyholders" into an
  arithmetic floor: at least **90 %** of the investment result net of the *Rechnungszinsen*,
  **90 %** of the risk result and **50 %** of the remaining result, less the *Direktgutschrift*,
  computed separately for *Alt-* and *Neubestand*, and floored at zero.

**What each contributes to a cash flow model.** Read alone, none of the four gives a modeller a
projection. Read together they do, and each supplies a different kind of quantity:

| Instrument | Kind of rule | What the model gets from it |
|---|---|---|
| **VVG** [R22–R31] | contractual, one-way mandatory | the *benefits and options that must exist*: the surrender-value floor, the paid-up right, the profit-participation entitlement, the suicide window, the BU definition and the *Nachprüfung* notice period |
| **DeckRV** [R14–R17] | reserving arithmetic | the *ceilings that shape the tariff*: the discount rate a guarantee may be priced at, the acquisition cost that may be zillmered, the reserve that low rates force |
| **VAG** [R5–R13] | supervisory | the *constraints on the insurer's discretion*: adequacy of premiums, equal treatment, the RfB ring fence, the actuary's proposal, the *Bewertungsreserven* test |
| **MindZV / RfBV** [R18][R19] | distribution arithmetic | the *floor under the discretionary declaration*, expressed on the three result sources a German P&L is decomposed into |

The join is tighter than a list suggests, and three joins in particular are where a delib model
lives:

1. **§ 138 VAG → § 2 DeckRV → the guarantee.** Premiums must be adequate to form adequate
   *Deckungsrückstellungen*; the DeckRV caps the rate at which those may be discounted;
   therefore the *Höchstrechnungszins* caps what a new tariff may guarantee. The rate has been
   **1.00 % since 1 January 2025** [R15], the first increase in about thirty years, and it stays
   with a contract for its whole term — which is why a German book is a stack of cohorts at
   4.00 %, 3.25 %, 2.75 %, 2.25 %, 1.75 %, 1.25 %, 0.90 %, 0.25 % and now 1.00 % [R15].
2. **§ 153 Abs. 3 VVG → § 139 Abs. 3/4 VAG → MindZV §§ 11–12.** The contract entitles the
   policyholder to *half* the *Bewertungsreserven* attributed to it; the VAG then removes from
   the fixed-income pool any *Sicherungsbedarf* arising from contracts with interest
   guarantees; the MindZV defines the reference rate — a **single month-end ten-year zero-coupon
   Euro swap rate** — and the fifteen-year look-forward against which a contract's highest
   applicable *Rechnungszins* is tested. In the low-rate decade that chain reduced the payable
   half to **zero** for many portfolios, and the BGH held the rule constitutional in 2018 [R36].
3. **§ 4 DeckRV ∥ § 169 Abs. 3 VVG.** The DeckRV governs what the insurer may **reserve** for
   acquisition costs (25 ‰ of the *Beitragssumme*); § 169 governs what it must **pay** on
   surrender (the value on a five-year even spread of the charged costs). They are independent
   constraints and the tighter one binds. A model that applies only one of them has an early-
   duration surrender curve that is wrong in a way a German reviewer will see immediately.

**What sits outside the four.** The **statutory accounts** are HGB §§ 341–341o plus the
**RechVersV**, whose *Formblatt 1* replaces § 266 HGB for the balance sheet and whose § 28
Abs. 8 forces the RfB development, the *Schlussüberschussanteilfonds* and the declared
*Überschussanteile* per *Abrechnungsverband* into the published *Anhang* [R54] — which is the
practical reason a delib product document can cite a named insurer's declaration at all. The
**BerVersV** carries the national supervisory returns, including the *Zerlegung des
Rohergebnisses nach Ergebnisquellen* on forms F.213.01 to F.219.01, which is the three-way
split the MindZV minima operate on [R54]. The **Solvency II layer** — Directive 2009/138/EG,
Delegated Regulation (EU) 2015/35, the 2025 review and the EIOPA curves [R1–R4] — reaches
German life business through the VAG rather than directly, which is why delib cites VAG
sections throughout and directive articles only where the European layer is itself the point.
The **guarantee** is bounded at the bottom by the *Sicherungsfonds* and § 314 VAG [R12]: a
supervisory power to cut guaranteed benefits by up to 5 % where the fund steps in, and an
uncapped, asset-position-driven reduction where it does not. **No delib document describes a
German guarantee as unconditional.**

**And what delib does not model.** All ten models publish gross, undiscounted,
best-estimate-style liability cash flows. The Solvency II balance sheet, the SCR and MCR, the
risk margin, the *Deckungsrückstellung*, the *Zinszusatzreserve*, the RfB stock as a
balance-sheet item and the IFRS 17 measurement are **cited, never specified**. Where a document
needs a discount rate, an asset return or a declared rate to make a worked example run, that
number is `**[std]**` with a rationale, not a citation.

---

## Product key and product-relevance matrix

**Product key**, used in the `Products` line of every entry and as the matrix columns:

`KLV` kapitallebensversicherung · `RV` klassische_rentenversicherung ·
`FRV` fondsgebundene_rentenversicherung · `IDX` indexpolice · `BAS` basisrente ·
`RIE` riester_rente · `SOF` sofortrente · `RLV` risikolebensversicherung ·
`BU` berufsunfaehigkeit · `PFL` pflegerentenversicherung.

`x` = load-bearing for that product's specification, technical notes or model; `(x)` =
qualified, conditional or background relevance — the entry governs the product but does not
shape its cash flows, or reaches it only through an option or a rider; blank = not relevant.

| R# | Reference (short name) | KLV | RV | FRV | IDX | BAS | RIE | SOF | RLV | BU | PFL |
|----|------------------------|-----|----|-----|-----|-----|-----|-----|-----|----|-----|
| R1 | Richtlinie 2009/138/EG — Solvabilität II | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R2 | Delegierte Verordnung (EU) 2015/35 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R3 | Richtlinie (EU) 2025/2 — the Solvency II review | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R4 | EIOPA — RFR term structures, UFR, Volatilitätsanpassung | (x) | (x) | | (x) | (x) | (x) | (x) | | (x) | (x) |
| R5 | VAG 2016 and Anlage 1 — the Sparten | x | x | x | x | x | x | x | x | x | x |
| R6 | VAG §§ 74–110 and § 40 — balance sheet, SCR/MCR, SFCR | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R7 | VAG §§ 124–125 — Anlagegrundsätze, Anlagestock | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R8 | VAG § 138 — Prämienkalkulation; Gleichbehandlung | x | x | (x) | x | x | x | x | x | x | x |
| R9 | VAG § 139 — Überschussbeteiligung; Sicherungsbedarf | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R10 | VAG §§ 140 and 145 — the RfB and its Verordnungen | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R11 | VAG §§ 141–143; Altbestand/Neubestand 1994 | x | x | x | x | x | x | x | x | x | x |
| R12 | VAG §§ 221–236 and § 314; Protektor | x | x | x | x | x | x | x | x | x | x |
| R13 | VAG §§ 351–353 — Übergangsmaßnahmen | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | DeckRV and § 2 — the Höchstrechnungszins provision | x | x | (x) | x | x | x | x | x | x | x |
| R15 | Höchstrechnungszins history; Sechste VO 19.07.2024 | x | x | (x) | x | x | x | x | x | x | x |
| R16 | DeckRV § 4 — Höchstzillmersätze | x | x | x | x | x | x | | x | x | x |
| R17 | DeckRV § 5 Abs. 3 — Referenzzins, ZZR, Korridor | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R18 | MindZV — the 90/90/50 minima and §§ 11–13 | x | x | (x) | x | x | x | x | x | x | x |
| R19 | RfBV — the collective part of the RfB | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R20 | LVRG 2014 | x | x | (x) | x | x | x | (x) | x | x | x |
| R21 | BaFin — FinDAG, MaGo, Auslegungsentscheidungen | (x) | (x) | x | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R22 | VVG 2008 — the statute, Kapitel 5, § 171 | x | x | x | x | x | x | x | x | x | x |
| R23 | VVG §§ 8 and 152 — Widerruf | x | x | x | x | x | x | x | x | x | x |
| R24 | VVG § 153 — Überschussbeteiligung, Bewertungsreserven | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R25 | VVG §§ 154–155 — Modellrechnung, Standmitteilung | x | x | (x) | x | x | x | (x) | | (x) | (x) |
| R26 | VVG §§ 150, 159–162 — consent, beneficiary, suicide | x | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R27 | VVG § 163 — Prämien- und Leistungsänderung | (x) | (x) | | | | | | (x) | x | x |
| R28 | VVG §§ 165–170 — paid-up, surrender, Rückkaufswert | x | x | x | x | (x) | x | (x) | (x) | x | x |
| R29 | VVG §§ 172–177 — Berufsunfähigkeitsversicherung | (x) | (x) | | | (x) | | | (x) | x | (x) |
| R30 | VVG §§ 19, 37, 38, 157, 158 | x | x | (x) | (x) | (x) | (x) | (x) | x | x | x |
| R31 | VVG §§ 6, 7, 1a, 7b, 7c, 214 and the VVG-InfoV | x | x | x | x | x | x | x | x | x | x |
| R32 | PRIIPs — VO (EU) 1286/2014 and the RTS | (x) | (x) | x | x | (x) | (x) | (x) | | | |
| R33 | IDD — RL (EU) 2016/97, transposition, § 34d GewO | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R34 | Unisex — EuGH C-236/09 and the AGG | x | x | x | x | x | x | x | x | x | x |
| R35 | BaFin Merkblatt 01/2023 — Wohlverhaltensaufsicht | x | x | x | x | (x) | (x) | (x) | | | |
| R36 | The BGH line of authority | x | x | x | x | (x) | x | (x) | (x) | (x) | x |
| R37 | GDV-Musterbedingungen; BU market practice | x | x | (x) | (x) | (x) | (x) | (x) | x | x | (x) |
| R38 | AltEinkG and the Drei-Schichten-Modell | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R39 | EStG § 10 Abs. 1 Nr. 2 b and Abs. 3 — Basisrente | | | | | x | (x) | | (x) | (x) | |
| R40 | ZPO §§ 850b and 851c — Pfändungsschutz | (x) | (x) | (x) | | x | (x) | | | x | (x) |
| R41 | EStG § 22 Nr. 1 S. 3 a and § 55 EStDV | (x) | x | x | x | x | (x) | x | | x | (x) |
| R42 | EStG § 10a and §§ 79–99 — the Riester machinery | | | (x) | | (x) | x | | | | |
| R43 | AltZertG, BZSt, AltvPIBV and the PIA | | (x) | (x) | (x) | x | x | | | | |
| R44 | Altersvorsorgereformgesetz 2026; Altersvorsorgedepot | | (x) | (x) | | (x) | x | | | | |
| R45 | EStG § 20 Abs. 1 Nr. 6 — 12/62, Mindesttodesfallschutz | x | x | x | x | | (x) | (x) | (x) | | |
| R46 | ErbStG and SGB V §§ 226, 229, 240 | x | (x) | (x) | (x) | (x) | x | (x) | x | (x) | (x) |
| R47 | Rechnungsgrundlagen 1./2. Ordnung; the DAV tables | x | x | x | x | x | x | x | x | x | x |
| R48 | DAV 2008 T and its predecessors | x | (x) | (x) | (x) | (x) | (x) | | x | (x) | (x) |
| R49 | DAV 2004 R and DAV 2004 R-Bestand | (x) | x | x | x | x | x | x | | | (x) |
| R50 | DAV 1997 I / RI / TI | (x) | | | | | | | (x) | x | (x) |
| R51 | DAV 2008 P, § 15 SGB XI and the Pflegegrad break | (x) | (x) | | | | | | | (x) | x |
| R52 | Destatis — Sterbetafeln, Generationentafeln, Pflege | x | x | x | x | x | x | x | x | x | x |
| R53 | The German life market in numbers | x | x | x | x | x | x | x | x | x | x |
| R54 | HGB §§ 341–341o, RechVersV, BerVersV | x | x | (x) | x | x | x | x | (x) | (x) | (x) |
| R55 | IFRS 17 and the Variable Fee Approach | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R56 | DAV Fachgrundsätze and the Höchstrechnungszins recommendation | x | x | x | x | x | x | x | x | x | x |

**One row is deliberately absent from the matrix and is recorded here instead.** BaFin
*Rundschreiben 11/2017 (VA)*, the *Kapitalanlagerundschreiben*, and the **Anlageverordnung
(AnlV)** it interprets apply to **small insurers under §§ 212–217 VAG and to domestic
Pensionskassen and Pensionsfonds** — **not** to the Solvency II life insurers that write the
ten delib products, which are governed by the qualitative § 124 VAG prudent person principle
[R7]. German market writing routinely cites AnlV quotas as if they bound all insurers; since
1 January 2016 they do not bind the large life insurers at all. The circular is discussed
inside R7 so that no delib author misapplies an AnlV quota, and it carries no id of its own.

---

## 1. Prudential — the European layer

The Solvency II layer reaches German life business **through the VAG**, not directly. That is
why delib cites VAG sections throughout and directive articles only where the European layer is
itself the point, and it is why **no Solvency II article number in this library was read from
the instrument**: `eur-lex.europa.eu` is refused at the egress gateway, and the article numbers
below come from secondary summaries.

### R1. Richtlinie 2009/138/EG — Solvabilität II
- Publisher: European Parliament and Council (EUR-Lex); German mirrors at `lexparency.de` and
  `kpmg-lexlinks.de`
- Doc type: Level 1 directive (consolidated text)
- URL: https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32009L0138 (returned by
  search); consolidated PDF
  https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:02009L0138-20190113 (returned);
  https://lexparency.de/eu/32009L0138/ (returned)
- Retrieved: **no** — direct HTTP egress blocked in the build environment; corroborated by web
  search (one query, four independent publishers, two with substantive summaries that agree)
- Content: the directive Germany transposes into the VAG. The substance established from the
  summaries: **the value of technical provisions equals the sum of a best estimate and a risk
  margin, calculated separately**; the relevant risk-free yield curve for the best estimate is
  that of **Article 77(2)** — a reference independently confirmed by BaFin's own interpretive
  decision on capital-market models [R21] — and the **risk margin of Article 77(5)** is
  calculated excluding any capital add-on. **Article 76** appears in the search results in its
  usual role as the article cited for the best-estimate-plus-risk-margin rule. For a delib model
  the operative point is the boundary: all ten models publish gross, undiscounted liability cash
  flows and stop short of the measurement this directive prescribes.
- Not established: **no article number here was read from the instrument itself** and all are
  therefore `[unverified]`. The three-pillar structure, the **99.5 % one-year VaR** confidence
  level and the directive's adoption date are commonly reported but were **not returned by any
  search in this sweep** and are `[unverified]`. One secondary source states that Solvency II
  stress scenarios are calibrated to a **0.5 % probability of occurrence**, which is consistent
  with the 99.5 % VaR but is a secondary restatement, not the directive.
- Products: all ten (cited-not-specified).

### R2. Delegierte Verordnung (EU) 2015/35
- Publisher: European Commission (EUR-Lex); mirrors at `lexparency.de`, `gesetze.legal`,
  `umwelt-online.de`
- Doc type: Level 2 delegated regulation, directly applicable
- URL: https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32015R0035&from=DE
  (returned); https://lexparency.de/eu/32015R0035/ (returned);
  https://gesetze.legal/eu/vo_eu_2015_35 (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries, four
  independent publishers, two substantive summaries on the risk-margin articles)
- Content: where the operative Solvency II detail lives, which is why a German modeller looking
  for contract boundaries, expense rules or standard-formula stresses reads this rather than the
  VAG. Established from summaries: **Art. 37** governs the calculation of the risk margin, which
  rests on the assumption that the **entire portfolio of obligations is transferred to another
  undertaking**; **Art. 38** defines that hypothetical *Referenzunternehmen*; **Art. 39** sets
  the *Kapitalkostensatz*. The instrument's own title carries its adoption date of **10 October
  2014**.
- Not established: **the 6 % cost-of-capital rate was never confirmed from any text.** One
  search summary explicitly notes the figure did not appear in the returned results; the only
  support is the 2025 review's "reduced from 6 to 4.75 per cent" wording [R3], so 6 % is
  **corroborated only indirectly** and is `[unverified]`. **Art. 18 (Vertragsgrenzen / contract
  boundaries) returned nothing** and its content is entirely `[unverified]`. The **life
  underwriting sub-modules (Art. 136 ff.)** — mortality, longevity, disability, lapse, mass
  lapse, expense, revision and catastrophe — and their calibrations, **including the 40 %
  mass-lapse shock**, were **not established**; the query that would have addressed them was cut
  by the exhausted budget. Only the *names* of the sub-modules are corroborated, from a
  secondary source listing longevity, disability, lapse and expenses as the material SCR drivers
  for German business. The publication date of **17 January 2015** was not returned in this
  sweep. Consequence for delib: **no cost-of-capital rate, no contract-boundary rule and no
  lapse or expense stress in this library rests on a retrieved text**, and any such figure in a
  product document is `**[std]**` or `[unverified]`.
- Products: all ten (cited-not-specified).

### R3. Richtlinie (EU) 2025/2 — the Solvency II review
- Publisher: European Parliament and Council, Official Journal; secondary analysis from BDO,
  KPMG, Deloitte, PwC, Meyerthole Siems Kohlruss and the AVÖ
- Doc type: amending directive
- URL: https://www.bdo.de/de-de/insights/weitere-veroffentlichungen/versicherungen/solvency-ii-reform-ab-2027-entlastung-durch-proportionalitaet
  (returned);
  https://klardenker.kpmg.de/financialservices-hub/regulatory-update/ueberarbeitete-solvency-ii-richtlinie-im-eu-amtsblatt-veroeffentlicht/
  (returned); https://aktuare.de/de/presse/pressemitteilungen/2682-pm-risikomarge-solvencyii.html
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries, five
  independent professional-services analyses agreeing on the title, the date, the first
  application and the cost-of-capital cut)
- Content: the amending directive from the 2019–2021 review, **dated 27 November 2024** and
  **published in the Official Journal on 8 January 2025**. **The new rules apply for the first
  time on 30 January 2027**, two years after entry into force, and Member States must transpose
  within those two years — so German transposition into the VAG is due before that date. What
  changes and matters to a liability model: the **Kapitalkostensatz underlying the risk margin
  falls from 6 % to 4.75 %**, with the next review of the rate at the earliest five years after
  entry into force; and an **exponential, time-dependent lambda factor** is to be introduced
  through the Level 2 regulation, reducing the level and the volatility of the risk margin for
  long-term business, with **no lower bound** and an effect on **projected years ≥ 28**. The net
  effect is a risk-margin reduction most beneficial to insurers with long-term business — which
  is exactly the German life book. Otherwise the reform combines targeted proportionality relief
  for small and non-complex undertakings with tightened qualitative requirements on governance,
  risk management, sustainability and crisis prevention.
- Not established: **a wording conflict across the summaries.** One states "das Inkrafttreten
  ist für den 30. Januar 2027 vorgesehen"; another states the rules apply "zwei Jahre nach ihrem
  Inkrafttreten am 30. Januar 2027"; a third gives publication on 8 January 2025 and application
  from 30 January 2027. The consistent reading is entry into force twenty days after publication
  and first application 30 January 2027, but **the entry-into-force date itself was never stated
  by any search result** and is `[unverified]`. Only the **30 January 2027 first application**
  is safe to assert. The lambda formula, the proportionality thresholds and the macroprudential
  tools were not established.
- Products: all ten, forward-looking only. **No delib model implements a 2027 basis and none
  should be read as doing so.**

### R4. EIOPA — risk-free interest rate term structures, the UFR and the Volatilitätsanpassung
- Publisher: European Insurance and Occupational Pensions Authority; republished on
  `data.europa.eu`; secondary commentary from PwC, KPMG and addactis
- Doc type: data hub, technical documentation and news releases
- URL: https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en
  (returned);
  https://www.eiopa.europa.eu/eiopa-publishes-ultimate-forward-rate-ufr-2026-2025-03-31_en
  (returned);
  https://www.eiopa.europa.eu/eiopa-updates-reference-portfolios-used-calculate-volatility-adjustment-solvency-ii-risk-free-rate-2025-12-09_en
  (returned); the *Report on the Calculation of the UFR for 2026*, **EIOPA-BoS-25-114**, at
  https://www.eiopa.europa.eu/document/download/16f852f9-919d-49fe-a691-b9eb9e3285bd_en?filename=EIOPA-BoS-25-114-Report+on+the+Calculation+of+the+UFR+for+2026.pdf
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries;
  EIOPA's own pages plus three independent secondary commentaries agreeing on the monthly cadence
  and the 2026 UFR)
- Content: EIOPA **publishes the relevant risk-free interest-rate term structures monthly**, and
  **§ 83 VAG makes their use binding on German undertakings** [R6] — which is the hook by which a
  European technical publication becomes German law. Established specifics: updated technical
  documentation published **24 September 2024**, taking effect **1 January 2025**, with the first
  calculation on that basis at the **end of January 2025**; the **UFR for the euro is 3.30 %,
  applicable from 1 January 2026, unchanged from 2025**; the published packages carry the
  risk-free rates, the **volatility adjustment**, the matching-adjustment fundamental spreads and
  the UFR; and the **reference portfolios behind the volatility adjustment were updated on
  9 December 2025**. A secondary commentary — not EIOPA — describes the curve as interpolated
  below a **Last Liquid Point of 20 years** and then extrapolated to the UFR over a **60-year
  horizon by the Smith–Wilson method**.
- Not established: **no German volatility-adjustment value, for any date, was established** —
  the query was cut by the exhausted budget; the one Germany-specific number any search returned
  was a **fundamental spread of 0 basis points on the German government bond in May 2016**, from
  a secondary summary, which is a different quantity and nearly a decade stale. **No numeric
  curve point was extracted.** The Smith–Wilson / LLP-20 / 60-year description rests on **one
  secondary source** and is `[unverified]` against EIOPA's own documentation. For delib: **no
  curve value is used in any model**; the models publish undiscounted cash flows and a reader
  wanting a market-consistent valuation applies a curve from this source. Any discount rate in a
  delib document is `**[std]**`.
- Products: all ten (discounting, cited-not-specified); most materially the long-duration
  guaranteed books — RV, SOF, BAS, RIE, KLV, IDX, PFL.

---

## 2. Prudential — the Versicherungsaufsichtsgesetz

The VAG 2016 is the German transposition of Solvency II and the single statute a German life
model is held to. Its architecture matters for citation: **Teil 1** carries the general
prudential rules (valuation, technical provisions, own funds, SCR, MCR, investments, the public
solvency report); **Teil 2 Kapitel 3 Abschnitt 1** the *besondere Vorschriften* for life
insurance (§§ 138–145); **Teil 3** the *Sicherungsfonds* (§§ 221 ff.); **Teil 4** the
supervisory powers including § 314; **Teil 8** the transitional provisions (§§ 351–353). That
layout is why a German product document cites §§ 138–141 for the contract-side mechanics and
§§ 74–88 for the balance sheet, and why the two rarely appear in the same paragraph.

### R5. VAG 2016 — the statute, its architecture and Anlage 1 (die Sparten)
- Publisher: Bundesministerium der Justiz / Bundesamt für Justiz, via `gesetze-im-internet.de`;
  mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`, `anwalt.de`,
  `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`
- Doc type: federal statute (consolidated text) with annexes
- URL: https://www.gesetze-im-internet.de/vag_2016/BJNR043410015.html (returned); full text PDF
  https://www.gesetze-im-internet.de/vag_2016/VAG.pdf (returned); Anlage 1
  https://www.gesetze-im-internet.de/vag_2016/anlage_1.html (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (multiple queries;
  **eight independent publishers** carry the same section titles)
- Content: *Gesetz über die Beaufsichtigung der Versicherungsunternehmen*, in the version in
  force since **1 January 2016** — the Solvency II transposition. **Anlage 1** to the Act is the
  *Einteilung der Risiken nach Sparten*, and it decides which supervisory regime a product sits
  in and which undertakings must join the *Sicherungsfonds* [R12]. The life-relevant *Sparten*
  established from summaries: **19 Leben**, "soweit nicht unter den Nummern 20 bis 24
  aufgeführt"; 20 Heirats- und Geburtenversicherung; **21 Fondsgebundene Lebensversicherung**;
  22 Tontinengeschäfte; **23 Kapitalisierungsgeschäfte**, described as business in which,
  applying a mathematical procedure, premiums fixed in advance and the obligations assumed are
  fixed in duration and amount. The relevance to delib is direct: **eight of the ten products
  sit in Sparte 19**; the `fondsgebundene_rentenversicherung` sits in **Sparte 21** and
  therefore carries the separate *Anlagestock* rule of § 125 VAG [R7].
- Not established: the date of promulgation (1 April 2015 is the figure usually given) was **not
  returned by any search** and is `[unverified]`. A **Sparte 24** exists — the cross-reference
  "Nummern 20 bis 24" implies it — and is reported elsewhere as *Geschäfte der Verwaltung von
  Versorgungseinrichtungen*, but that title was not returned and is `[unverified]`. **§ 294 VAG
  as the general statement of supervisory objectives**, which German commentary usually cites,
  was not confirmed by any result and is `[unverified]`; BaFin's own page states the objective in
  prose without a section number [R21]. **The supervisory Sparte classification of a stand-alone
  *selbständige Berufsunfähigkeitsversicherung* and of a *Pflegerentenversicherung* — whether
  they are Sparte 19 business or fall to the health regime — was not established**; the query
  was cut by the exhausted budget, and it is an open question for BU and PFL.
- Products: all ten.

### R6. VAG §§ 74–110 and § 40 — valuation, best estimate, risk margin, the LTG measures, SCR/MCR and the SFCR
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`,
  `freirecht.de`, `juraforum.de`, `haufe.de`, `datenbank.nwb.de`,
  `sozialgesetzbuch-sgb.de`
- Doc type: statutory sections
- URL: https://www.gesetze-im-internet.de/vag_2016/__88.html (returned);
  https://dejure.org/gesetze/VAG/78.html (returned); https://lxgesetze.de/vag/88 (returned);
  https://www.buzer.de/88_VAG.htm (returned); https://freirecht.de/g/VAG:75 (returned);
  https://dejure.org/gesetze/VAG/82.html (returned); https://dejure.org/gesetze/VAG/80.html
  (returned); https://dejure.org/gesetze/VAG/96.html (returned);
  https://freirecht.de/g/VAG:100 (returned);
  https://www.haufe.de/id/norm/versicherungsaufsichtsgesetz-96-110-unterabschnitt-2-solvabilitaetskapitalanforderung-HI7709851.html
  (returned); https://dejure.org/gesetze/VAG/40.html (returned).
  §§ 74 and 77 in the canonical `__74.html` / `__77.html` form `[unverified]` — the pattern is
  evidenced by the returned pages for §§ 82, 88, 124, 125, 138–143 and 221–222.
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (four queries; the
  section titles from four to seven independent publishers; the § 88 Abs. 3 summary in
  near-identical form from two)
- Content: this block is where the German text says what Solvency II says, and it contains the
  single most load-bearing enabling power in German life insurance.
  **§ 74 *Bewertung der Vermögenswerte und Verbindlichkeiten*** is the market-consistent
  valuation rule that makes the *Solvabilitätsübersicht* a different object from the HGB
  accounts: per the summary, assets are valued at the amount for which they could be exchanged
  between knowledgeable, willing and independent business partners, liabilities at the amount
  for which they could be transferred or settled between such partners, and — quoted by the
  summary — *"eine Anpassung der Bewertung zur Berücksichtigung der Bonität des
  Versicherungsunternehmens findet nicht statt"*, i.e. **no own-credit adjustment**. **§ 75**
  carries the principles of § 74 Abs. 3 into the calculation of technical provisions.
  **§ 76** provides that the value of technical provisions is the **best estimate plus a risk
  margin**, the two calculated separately; **§ 77 *Bester Schätzwert*** defines the first and
  **§ 78 *Risikomarge*** the second; **§ 79** carries the general calculation principles.
  **§ 83** obliges undertakings to use the technical information EIOPA publishes — the hook by
  which the EIOPA curve, the volatility adjustment and the fundamental spreads become binding
  German law [R4]. **§ 84** covers further matters to be reflected.
  **§§ 80–82** are the long-term-guarantee measures. § 82: an undertaking may, **with the
  supervisor's approval**, apply a ***Volatilitätsanpassung*** to the risk-free curve used for
  the best estimate under § 77. § 80: with approval, it may apply a ***Matching-Anpassung*** to
  that curve for a portfolio of life obligations, including annuities arising from non-life
  contracts. The two are **mutually exclusive on the same obligations**, and the matching
  adjustment is additionally excluded where the curve already carries a *Übergangsmaßnahme für
  risikofreie Zinssätze* under § 351 [R13]. These are the measures whose presence or absence
  moves a German life insurer's published solvency ratio by hundreds of percentage points, which
  is why **no delib document quotes a German solvency ratio without saying whether it is *mit*
  or *ohne Volatilitätsanpassung und Übergangsmaßnahmen*** [R53].
  **§ 88 is the entry that matters most to delib, because it is the legal root of the DeckRV.**
  Per the summaries, § 88 places on the undertaking the burden of demonstrating the adequacy of
  the level of its technical provisions, the suitability and materiality of the methods used and
  the adequacy of the underlying statistical data, and lets the supervisor order an increase
  where the calculation does not comply with §§ 75–87. **§ 88 Abs. 3** empowers the
  Bundesministerium der Finanzen, in agreement with the Bundesministerium der Justiz und für
  Verbraucherschutz and observing the *Grundsätze ordnungsmäßiger Buchführung*, to fix by
  *Rechtsverordnung* **Höchstwerte für den Rechnungszins bei Versicherungsverträgen mit
  Zinsgarantie**, further requirements for determining the discount rates, and the actuarial
  calculation bases and valuation methods for the *Deckungsrückstellung*. That single sentence
  is why the *Höchstrechnungszins* is a ministerial regulation rather than a supervisory
  circular, and why the DAV's annual recommendation is a recommendation and not a decision
  [R14][R15][R56].
  **§§ 96–110** form *Unterabschnitt 2 Solvabilitätskapitalanforderung*: § 96 allows the SCR to
  be determined by a **Standardformel** or an **internes Modell**, with § 97 governing the
  determination and the supervisor able to order an internal model where the risk profile
  deviates materially from the standard formula's assumptions; § 100 sets out the structure of
  the *Basissolvabilitätskapitalanforderung*. The **Mindestkapitalanforderung (MCR)** is a
  separate Unterabschnitt of the same Kapitel: one general-reference source establishes that it
  has been in force in Germany since **1 January 2016** and that, with the SCR, it forms a
  **two-tier ladder**, the MCR being the lower threshold below which the risk level for
  policyholders is deemed unacceptable. **§ 40** obliges the undertaking to publish an annual
  ***Bericht über Solvabilität und Finanzlage (SFCR)***, released for publication by the
  *Vorstand* under § 40 Abs. 1 Satz 3 — the practical route by which a delib reader obtains a
  named insurer's SCR ratio, technical provisions and transitional-measure use.
- Not established: the text of **§ 74 Abs. 3** (the principles § 75 imports) was not returned,
  nor the text of **§ 78** (how the risk margin is computed, and whether the cost-of-capital rate
  is national or in the Delegated Regulation — it is the latter, see [R2]). **The MCR section
  numbers in the VAG were not established.** §§ 122–124 is the range commonly cited in
  commentary, but § 124 is demonstrably *Anlagegrundsätze* [R7], so that citation cannot be right
  as stated; **any delib document must cite the MCR by name, not by section.** One search result
  showed **§ 234g VAG** *Solvabilitätskapitalanforderung, Mindestkapitalanforderung und
  Eigenmittel* — that is the **Pensionsfonds** provision, out of delib scope, recorded here only
  so a later reader does not mistake it for the life rule. The **absolute euro floors for the
  MCR**, amended by the Sechste Verordnung of 19 July 2024 [R15] following a European Commission
  notification, were **not established** — no figure was returned. The Solvency II article
  numbers §§ 76–78 transpose are `[unverified]` [R1]. **No German volatility-adjustment value
  was established, for any date**; which German life insurers use the matching adjustment
  (generally reported to be none, the German book being unsuitable) was not established.
- Products: all ten (cited-not-specified — the models publish the cash flows this block would be
  applied to, and perform no § 74 valuation, no SCR and no MCR).

### R7. VAG §§ 124 and 125 — Anlagegrundsätze, Sicherungsvermögen and the Anlagestock
- Publisher: Bundesamt für Justiz; BaFin for the topic page; mirrored by `buzer.de`,
  `lxgesetze.de`, `anwalt.de`, `lexetius.com`, `sozialgesetzbuch-sgb.de`; Gabler
  *Versicherungslexikon* on *Anlagestock*
- Doc type: statutory sections; supervisory topic page; lexicon entry
- URL: https://www.gesetze-im-internet.de/vag_2016/__124.html (returned);
  https://www.buzer.de/124_VAG.htm (returned);
  https://www.bafin.de/DE/Aufsicht/VersichererPensionsfonds/Kapitalanlagen/PrudentPersonPrinciple/prudent_person_principle_artikel.html
  (returned); https://www.gesetze-im-internet.de/vag_2016/__125.html (returned);
  https://dejure.org/gesetze/VAG/125.html (returned);
  https://www.versicherungsmagazin.de/lexikon/anlagestock-1944505.html (returned).
  Related and deliberately kept outside the matrix: BaFin **Rundschreiben 11/2017 (VA)** at
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1711_hinweise_anlage_sicherungsvermoegen_va.html
  (returned).
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (three queries;
  five independent publishers on each section plus BaFin's own page, with two substantive
  summaries per section that agree)
- Content: **§ 124 *Anlagegrundsätze*.** Since 1 January 2016 a Solvency II undertaking has **no
  quantitative investment limits**; § 124 replaces them with a qualitative standard. Per the
  summaries: all assets must be invested such that the **security, quality, liquidity and
  profitability of the portfolio as a whole** are ensured and their location guarantees their
  availability; assets covering technical provisions must be invested in a manner **appropriate
  to the nature and duration** of the liabilities; those assets must be invested in the interest
  of all policyholders and beneficiaries in accordance with the disclosed investment policy; and
  where a conflict of interest arises it must be ensured the investment is made in the interest
  of policyholders and beneficiaries. **For delib this is why a German life insurer's asset mix
  — and hence the *Kapitalanlageergebnis* that drives the *Überschussbeteiligung* [R18] — is not
  derivable from a rulebook, and why every asset-return assumption in a delib model is
  `**[std]**`.**
  **§ 125 *Sicherungsvermögen*.** The ring-fenced asset pool covering policyholder claims. Per
  the summaries: the *Vorstand* must allocate amounts to it during the financial year and invest
  them in line with the expected growth of the *Mindestumfang*; it must be **administered
  separately** from any other assets and held within the territory of the Member or Contracting
  States; and with the supervisor's approval **independent sections (*unabhängige Abteilungen*)**
  may be formed, everything prescribed for the *Sicherungsvermögen* applying to each. **The
  Anlagestock**: for each *Anlageart* a **separate section of the Sicherungsvermögen
  (*Anlagestock*)** must be formed where life contracts provide benefits in units of an open
  investment fund under § 1 Abs. 4 KAGB, in shares issued by an investment company, in assets
  under § 2 Abs. 4 of the Investmentgesetz as it stood until 21 July 2013 excluding cash, or
  **directly linked to a share index or other reference value**. One summary places this in
  **§ 125 Absatz 5**. This is the provision that makes FRV structurally different from the
  general-account products: the unit fund is a segregated *Anlagestock*, the policyholder bears
  its investment result, and the MindZV base is computed differently [R18][R21]. The final clause
  — benefits **directly linked to a share index or other reference value** — is equally the
  statutory hook under which IDX sits.
  **The AnlV boundary, recorded so no delib author gets it wrong.** BaFin *Rundschreiben 11/2017
  (VA)*, the *Kapitalanlagerundschreiben*, was published **12 December 2017**, replacing the
  circular of **15 April 2011**, and interprets the **Anlageverordnung (AnlV) 2016**. **Its scope
  is small insurers under §§ 212–217 VAG and domestic Pensionskassen and Pensionsfonds.** It does
  **not** apply to the Solvency II life insurers that write the ten delib products. German market
  writing routinely cites AnlV quotas as if they bound all insurers; since 1 January 2016 they do
  not bind the large life insurers at all. One substantive point from the circular is worth
  carrying: BaFin clarified that **investments bearing zero or negative interest may be admitted
  to the Sicherungsvermögen provided the profitability of the portfolio as a whole is ensured** —
  a low-rate-era ruling echoing § 124's "portfolio as a whole" standard.
- Not established: whether § 124 contains a derivatives clause or a non-admitted-asset clause.
  The **Absatz numbering of the Anlagestock rule (Abs. 5) rests on one search summary** and is
  `[unverified]`; the *Mindestumfang* definition, and where it is set, were not established.
  **The AnlV's own content — the *Anlageformen*, the *Mischungs-* and *Streuungsquoten* — was
  not established**; the query was cut by the exhausted budget, and **nothing in delib may state
  an AnlV quota**. Whether German index products are in practice written inside an *Anlagestock*
  or in the general account was **not established** and is an open question for IDX. § 244c VAG
  surfaced in the same search and was not investigated.
- Products: FRV and IDX load-bearing (the *Anlagestock*); KLV, RV, BAS, RIE, SOF load-bearing
  (§ 124 and the general *Sicherungsvermögen*); RLV, BU, PFL qualified.

### R8. VAG § 138 — Prämienkalkulation in der Lebensversicherung; Gleichbehandlung
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`,
  `juraforum.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `haufe.de`, `lexsoft.de`
- Doc type: statutory section
- URL: https://www.gesetze-im-internet.de/vag_2016/__138.html (returned);
  https://dejure.org/gesetze/VAG/138.html (returned); https://lxgesetze.de/vag/138 (returned);
  https://www.juraforum.de/gesetze/vag/138-praemienkalkulation-in-der-lebensversicherung-gleichbehandlung
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries; eight
  independent publishers on the title, three with substantive summaries that agree on both
  Absätze)
- Content: **Absatz 1** is the pricing-sufficiency rule and the reason a German tariff is priced
  on **prudent, not best-estimate, bases**: premiums in life insurance must be calculated *auf
  der Grundlage angemessener versicherungsmathematischer Annahmen* and set **high enough** that
  the undertaking can meet all its obligations and in particular form **adequate
  *Deckungsrückstellungen*** for the individual contracts. The undertaking's own financial
  position may be taken into account, but **funds not deriving from premium payments may not be
  used systematically and permanently** to support the tariff. That clause forbids permanent
  cross-subsidy of a loss-making tariff out of shareholder funds; it is why the first-order bases
  carry margins that later emerge as *Überschuss* [R47], and it is the statutory root of the
  *dauernde Erfüllbarkeit* standard that also appears in § 341e HGB [R54] and in BaFin's stated
  supervisory objective [R21].
  **Absatz 2** is the equal-treatment rule, quoted by a search summary: *"Bei gleichen
  Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden."*
  This is the supervisory half of the fairness constraint on discretionary profit sharing. Search
  results establish that the **BGH, in a judgment of 18 September 2024, Az. IV ZR 436/22**, tied
  the supervisory equal-treatment principle of § 138 Abs. 2 VAG to the contractual entitlement of
  **§ 153 Abs. 2 VVG** [R24], under which policyholders must participate in surplus *nach einem
  verursachungsorientierten Verfahren*. Together they mean the German *Überschussbeteiligung* is
  **discretionary in level but not in method**: an insurer may set the declaration, but the split
  between *Abrechnungsverbände* must follow causation. Search summaries also record that § 138
  contains an exception mechanism under which, when measures are taken, the policyholders'
  *Bestände* must be charged *verursachungsorientiert*, and that the provision addresses
  offsetting costs not covered by the premium calculation against surpluses from a more
  favourable risk or investment result.
- Not established: the number and content of the Absätze beyond 1 and 2. **Whether the
  *verursachungsorientiert* charging rule sits in § 138 or in § 140 is ambiguous across the two
  summaries and is `[unverified]`**; a delib document should attribute the causation principle to
  § 153 Abs. 2 VVG and § 138 Abs. 2 VAG **jointly**, as the BGH did, rather than to a single
  Absatz.
- Products: all ten; qualified only for FRV, whose investment result is the policyholder's, so
  that only the risk and cost results are shared.

### R9. VAG § 139 — Überschussbeteiligung and the Sicherungsbedarf test on Bewertungsreserven
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`,
  `juraforum.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`, `lexsoft.de`, `gesatz.de`
- Doc type: statutory section
- URL: https://www.gesetze-im-internet.de/vag_2016/__139.html (returned);
  https://dejure.org/gesetze/VAG/139.html (returned); https://lxgesetze.de/vag/139 (returned);
  https://www.buzer.de/139_VAG.htm (returned);
  https://www.juraforum.de/gesetze/vag/139-ueberschussbeteiligung (returned);
  https://gesatz.de/link.aspx?lnk=31094 (returned, carrying the Abs. 3/4 text)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (three queries; nine
  independent publishers on the title; the Absatz 1 sentence quoted back verbatim by one and
  paraphrased identically by two more; the Abs. 3/4 content from two independent sources)
- Content: **Absatz 1**, quoted by a search summary: *"Die für die Überschussbeteiligung der
  Versicherten bestimmten Beträge sind, soweit sie den Versicherten nicht unmittelbar zugeteilt
  wurden, in der Bilanz in eine Rückstellung für Beitragsrückerstattung einzustellen."* This is
  the structural fact behind the whole German surplus chassis: **surplus earmarked for
  policyholders either goes out immediately as *Direktgutschrift* or into the RfB, and nowhere
  else.** A delib model of a profit-participating product must carry both a direct credit and an
  RfB stock, or it has not modelled the product.
  **Absatz 3** is the LVRG's *Bewertungsreserven* restriction [R20]: valuation reserves from
  **festverzinsliche Anlagen und Zinsabsicherungsgeschäfte**, held directly or indirectly, may be
  taken into account in policyholders' participation in valuation reserves **only to the extent
  that they exceed any *Sicherungsbedarf* aus Versicherungsverträgen mit Zinsgarantien**.
  Departing policyholders therefore share only in the excess.
  **Absatz 4** defines the test. Per the returned text: the *Sicherungsbedarf* from contracts
  with interest guarantees is the **sum of the Sicherungsbedarfe of those contracts whose
  applicable interest rate exceeds the applicable Euro interest-rate swap rate at the time the
  valuation reserves are determined**; and a single contract's *Sicherungsbedarf* is its
  **actuarially calculated interest obligation, computed using that reference rate, less the
  Deckungsrückstellung**. The mechanics of the reference rate and the fifteen-year look-forward
  are in MindZV §§ 11–12 [R18].
  The practical consequence for delib: for a German contract written on a 3.25 % or 4.00 %
  *Höchstrechnungszins* [R15], the *Sicherungsbedarf* has for most of the last decade exceeded
  the fixed-income valuation reserves outright, so the *Bewertungsreserven* component of a
  maturity payout has often been **zero**. Any delib product document that models a
  *Bewertungsreserven* payment must say which side of this test it assumes, and the assumption is
  `**[std]**`.
- Not established: the full text of Absätze 2 and 5 onwards. The predecessor provision (**§ 56a
  VAG a.F.**), which most German commentary still names when describing the *Bewertungsreserven*
  rule, was **not confirmed by any search result** and is `[unverified]`. **A correction carried
  from the prudential sweep and stated here so it is not repeated:** § 139 VAG is
  *Überschussbeteiligung*, **not** the *Rückkaufswert* and **not** the Zillmerung cap; the
  *Rückkaufswert* is § 169 VVG [R28] and the *Höchstzillmersatz* is § 4 DeckRV [R16].
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL qualified (the risk and cost
  results are shared, and the *Bewertungsreserven* rule reaches them only where the tariff
  carries a savings element); FRV qualified — see BaFin's interpretive decision on minimum
  allocation in unit-linked business [R21].

### R10. VAG §§ 140 and 145 — Rückstellung für Beitragsrückerstattung and the Verordnungsermächtigung
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`,
  `haufe.de`, `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`
- Doc type: statutory sections
- URL: https://www.gesetze-im-internet.de/vag_2016/__140.html (returned);
  https://dejure.org/gesetze/VAG/140.html (returned); https://www.buzer.de/140_VAG.htm
  (returned); https://lxgesetze.de/vag/140 (returned);
  https://www.haufe.de/id/norm/versicherungsaufsichtsgesetz-140-rueckstellung-fuer-beitragsrueckerstattung-HI7710187_p140.html
  (returned); https://dejure.org/gesetze/VAG/145.html (returned);
  https://www.buzer.de/gesetz/11544/b28432.htm (returned, the Abschnitt 1 *Lebensversicherung*
  table of contents)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (three queries;
  seven independent publishers on § 140 with two substantive summaries that agree closely; § 145
  multi-source on the title and **single-source on its content**)
- Content: **§ 140 — the use restriction.** Amounts allocated to the RfB may be used **only** for
  the *Überschussbeteiligung* of the insured, **including the participation in Bewertungsreserven
  prescribed by § 153 VVG** [R24]. That is a hard ring fence: RfB money cannot be released to
  shareholders.
  **The two escape hatches**, both requiring the supervisor's consent and both confined to the
  part of the RfB **not** attributable to already-declared profit shares (*soweit sie nicht auf
  bereits festgelegte Überschussanteile entfällt*): the RfB may be drawn on **in the interest of
  the policyholders** (1) to offset **unforeseen losses from profit-participating contracts
  arising from general changes in circumstances**, and (2) to **increase the
  Deckungsrückstellung where the calculation bases must be adjusted because of an unforeseen and
  not merely temporary change in circumstances**. **Escape hatch (2) is the statutory route by
  which the German industry financed the *Zinszusatzreserve* out of the free RfB during the
  low-rate decade** [R17], and it is why a German life insurer's RfB stock and its ZZR stock move
  against each other. When such a measure is taken, the policyholders' *Bestände* are charged
  *verursachungsorientiert*.
  **Supervisory plans.** The supervisor may require a **Zuführungsplan** where the allocation to
  the RfB does not meet the minimum requirements (the MindZV, [R18]) and a **Verteilungsplan**
  where the *ungebundener* part of the RfB exceeds the maximum amount (the RfBV cap, [R19]).
  **The collective part.** § 140 Abs. 1 Satz 2 permits a life insurer to establish within the RfB
  **einen kollektiven Teil oder mehrere kollektive Teile**, assigned to all profit-participating
  contracts collectively rather than to a *Teilbestand*; the RfBV governs it [R19].
  **§ 145 *Verordnungsermächtigung*** empowers the Bundesministerium der Finanzen to make
  regulations concerning the **Zuführung zur Rückstellung für Beitragsrückerstattung in der
  Lebensversicherung**. It is therefore the statutory root of the **MindZV** [R18] and, with
  § 140 Abs. 1 Satz 2, of the **RfBV** [R19] — the pair that turns § 139's "put it in the RfB"
  and § 140's "use it only for policyholders" into an arithmetic minimum. Recording the chain
  **§ 145 VAG → MindZV** correctly matters because delib product documents cite the MindZV
  percentages constantly and a reader needs to know why a ministry may set them.
- Not established: the distinction between ***gebundene*** and ***freie*** RfB — the vocabulary
  every German market commentary uses — is **not in the statutory text any search returned**; it
  emerges from § 28 RechVersV's *Schlussüberschussanteilfonds* and *festgelegte Überschussanteile*
  [R54] together with the RfBV's *ungebundene RfB* [R19], and delib defines the terms from those
  two instruments rather than from § 140. Whether the supervisor's consent under the escape
  hatches has ever been granted, and how often, was not established. The **precise wording of
  § 145 and the list of matters the regulation may cover were not established**, and whether
  § 145 also underpins the RfBV or the RfBV rests on § 140 alone is `[unverified]`. **A
  correction carried forward:** § 145 VAG is a *Verordnungsermächtigung*, **not** the
  *Sicherungsvermögen*; the *Sicherungsvermögen* is § 125 VAG [R7].
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL, FRV qualified.

### R11. VAG §§ 141–143 — Verantwortlicher Aktuar, Treuhänder, Anzeigepflichten, and the deregulation of 29 July 1994
- Publisher: Bundesamt für Justiz; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`,
  `juraforum.de`, `anwalt.de`, `anwalt24.de`, `lexetius.com`, `freirecht.de`,
  `sozialgesetzbuch-sgb.de`, `datenbank.nwb.de`. For the deregulation: `de.wikipedia.org`
  (*Neubestand*), the Gabler *Versicherungslexikon* entries on `versicherungsmagazin.de`,
  `versicherungsbote.de` and `haufe.de`
- Doc type: statutory sections; lexicon and commentary entries for the deregulation
- URL: https://www.gesetze-im-internet.de/vag_2016/__141.html `[unverified canonical form]`;
  https://dejure.org/gesetze/VAG/141.html (returned); https://lxgesetze.de/vag/141 (returned);
  https://www.gesetze-im-internet.de/vag_2016/__142.html (returned);
  https://www.gesetze-im-internet.de/vag_2016/__143.html (returned);
  https://dejure.org/gesetze/VAG/143.html (returned); https://freirecht.de/g/VAG:128 (returned);
  https://freirecht.de/g/VAG:129 (returned); https://de.wikipedia.org/wiki/Neubestand
  (returned); https://www.versicherungsmagazin.de/lexikon/altbestand-1944472.html (returned);
  https://www.versicherungsmagazin.de/lexikon/neubestand-1946031.html (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (four queries; seven
  independent publishers on the § 141–143 titles; **the 29 July 1994 date from four independent
  sources agreeing**, which is good corroboration for a date that is otherwise easy to get wrong)
- Content: **§ 141 *Verantwortlicher Aktuar in der Lebensversicherung*.** Every life insurer must
  appoint one; the appointee must be *zuverlässig und fachlich geeignet*, professional
  qualification requiring sufficient knowledge of actuarial mathematics and professional
  experience, with **sufficient experience regularly assumed where at least three years' activity
  as an actuary can be demonstrated**. Appointment and dismissal are by the *Aufsichtsrat*. The
  duties that matter to delib: the undertaking must supply all information needed; an
  ***Erläuterungsbericht zur versicherungsmathematischen Bestätigung*** and an
  ***Angemessenheitsbericht*** are submitted to the supervisor; the actuary **attends the
  Aufsichtsrat meeting on the annual accounts** and reports the essential results there; and the
  actuary **makes a proposal on the Überschussbeteiligung**, which the undertaking must **submit
  to the supervisor**, and must **notify the supervisor, with written or electronic reasons, if
  it intends to declare a rate deviating from the actuary's proposal**. That last item is the
  single most consequential fact in this entry: **the German declaration is set by the board, but
  it passes through a named actuary's written proposal and a supervisory notification if the
  board departs from it** — which is the governance reason declared rates cluster as tightly as
  the market data show [R53].
  **§ 142 *Treuhänder in der Lebensversicherung*.** For life contracts **concluded after 28 July
  1994** where premiums can be changed with effect for existing contracts, such changes take
  effect only after an **unabhängiger Treuhänder** has consented; § 157 Abs. 1 and 2 apply to the
  trustee; the trustee's involvement is dispensed with where the change requires supervisory
  approval. (The separate **§ 128** trustee guards the *Sicherungsvermögen* and holds its assets
  *unter Mitverschluss*; **§ 129** governs the securing of the *Sicherungsvermögen*.) § 142 is
  the supervisory counterpart of the contractual repricing right of § 163 VVG [R27].
  **§ 143 *Besondere Anzeigepflichten in der Lebensversicherung*** is the German equivalent of a
  tariff filing. After authorisation the undertaking must **unverzüglich** notify the supervisor
  of the **Grundsätze für die Berechnung der Prämien und der Deckungsrückstellungen**, including
  the *verwendeten Rechnungsgrundlagen, mathematischen Formeln, kalkulatorischen Herleitungen und
  statistischen Nachweise*; the same applies whenever new or modified principles are used. **This
  is why a German tariff's first-order bases exist as a documented, supervisor-visible object —
  and equally why they are not public, which is the structural reason delib's decrement tables
  must be `**[std]**` proxies** [R47].
  **The 29 July 1994 boundary.** German life business splits into ***Altbestand*** (contracts
  concluded before 29 July 1994) and ***Neubestand*** (from that date). Until deregulation the
  AVB were part of a *genehmigungspflichtiger Geschäftsplan* approved by the Bundesaufsichtsamt
  für das Versicherungswesen; in the *Altbestand* the approved *Geschäftsplan* **continues to
  apply and changes still require supervisory approval**. In the *Neubestand* contract design,
  and in particular premium calculation, is **free within the statutory frame**, with no prior
  approval. At deregulation **the entire RfB accumulated to 1994 was allocated exclusively to the
  Altbestand**, which is why German life insurers still run separate surplus accounts for the two
  — and why the MindZV requires the minimum allocation to be computed **getrennt für Alt- und
  Neubestand** [R18]. **All ten delib products are Neubestand business and every product document
  says so**, because a reader encountering a 4.00 % guarantee in a German data set is almost
  always looking at pre-2000 *Neubestand*, and a reader encountering an approved-*Geschäftsplan*
  tariff is looking at *Altbestand*, which delib does not model.
- Not established: the text of the ***versicherungsmathematische Bestätigung*** — the formula the
  responsible actuary signs under the balance sheet — was **not returned** and is `[unverified]`;
  its connection to §§ 341e–341h HGB is inferred from [R54] and from § 226 VAG's use of the same
  range, not read. The exact one-day gap between § 142's "after **28** July 1994" and the
  deregulation date of **29** July 1994 is real in the sources and is not an error here, but no
  source explained it; treat both dates as given rather than reconciling them. § 157 VAG's
  content (which § 142 imports) was not established. Whether the DAV's professional standards
  bind the *Verantwortlicher Aktuar* as a matter of law was not established [R56].
- Products: all ten. § 143 is load-bearing for every product's `sources.md` provenance
  discussion.

### R12. VAG §§ 221–236 and § 314, with Protektor — the Sicherungsfonds and the supervisor's crisis powers
- Publisher: Bundesamt für Justiz for the VAG and the two regulations; Protektor
  Lebensversicherungs-AG; Wissenschaftliche Dienste des Deutschen Bundestages for the background
  paper; mirrored by `dejure.org`, `buzer.de`, `lxgesetze.de`, `juraforum.de`,
  `rechtsportal.de`, `lexetius.com`, `sozialgesetzbuch-sgb.de`, `anwalt.de`, `datenbank.nwb.de`
- Doc type: statutory sections; two Rechtsverordnungen; corporate and parliamentary documents
- URL: https://www.gesetze-im-internet.de/vag_2016/__222.html (returned);
  https://dejure.org/gesetze/VAG/221.html (returned); https://dejure.org/gesetze/VAG/226.html
  (returned); https://lxgesetze.de/vag/226 (returned); https://dejure.org/gesetze/VAG/314.html
  (returned); https://www.buzer.de/gesetz/11544/a192048.htm (returned, § 314);
  https://www.gesetze-im-internet.de/sichlvv/BJNR117000006.html (returned);
  https://www.gesetze-im-internet.de/sichlvfinv_2016/BJNR082800016.html (returned);
  https://www.protektor-ag.de/de/sicherungsfonds/dokumente (returned);
  https://www.bundestag.de/resource/blob/412602/04b5e6635cb5cdea18c3b7bcd94dbcac/WD-4-256-12-pdf.pdf
  (returned, Bundestag WD 4 – 256/12)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (six queries; §§ 221
  and 222 returned by nine and ten independent publishers respectively, the § 222 five-per-cent
  rule quoted back in near-identical wording by two; § 314 from five publishers with one detailed
  summary and two shorter ones that agree; the Mannheimer chronology from three independent
  sources with dates that agree)
- Content: **§ 221 *Pflichtmitgliedschaft*.** Undertakings authorised under § 8 Abs. 1 or § 67
  Abs. 1 to write the business of **Sparten 19 to 23 of Anlage 1** [R5] — or substitutive
  Krankenversicherung under § 146 — **must belong to a Sicherungsfonds** protecting the claims of
  their policyholders, insured persons, beneficiaries and other persons benefiting from the
  contract. **Pensions- und Sterbekassen are excepted**, and those are exactly the vehicles delib
  puts out of scope.
  **§ 222 — the five-per-cent haircut.** If an examination shows that the existing
  *Sicherungsvermögen* under § 226 Abs. 3, together with the *Sonderbeitrag* collectable under
  § 226, is insufficient to secure the continuation of the contracts, **the supervisor may reduce
  the obligations under the life insurance contracts by at most 5 per cent of the contractually
  guaranteed benefits**. The supervisor may additionally issue orders to prevent an extraordinary
  increase in early contract terminations — a run-stopping power that pairs with § 314.
  **§ 226 *Finanzierung*.** The **sum of the annual contributions** of all undertakings belonging
  to the life *Sicherungsfonds* is **0.2 per mille of the sum of their versicherungstechnische
  Netto-Rückstellungen**, those provisions measured **according to §§ 341e to 341h HGB** [R54] —
  the German statutory accounts, not the Solvency II balance sheet. The **fund's
  Sicherungsvermögen should not fall below 1 per mille** of the same aggregate, and
  **Sonderbeiträge** may be levied **up to 1 per mille** of it. Each undertaking's individual
  annual contribution is determined by the fund under the **SichLVFinV**.
  **Protektor.** *Protektor Lebensversicherungs-AG* is the German life guarantee scheme: the
  statutory *Sicherungsfonds* whose **tasks and powers were transferred to it by the SichLVV**,
  with the SichLVFinV setting the contribution mechanics. Membership is compulsory for life
  insurers and for branches writing life business in Germany. **The Mannheimer case is the only
  time it has been used, and its chronology is established**: in **June 2003** Protektor received
  a commitment declaration for the transfer of the portfolio of the insolvency-threatened
  *Mannheimer Lebensversicherungs-AG*; negotiations concluded **18 September 2003** and were
  notarised **26/27 September 2003**, Protektor taking the portfolio over economically from
  **1 July 2003**; **BaFin approved the Bestandsübertragungsvertrag on 1 October 2003**, and
  **138 Mannheimer employees became Protektor employees on that date**. At that time Protektor
  was a **voluntary** industry vehicle; the **statutory** *Sicherungsfonds* was created by VAG
  amendments of **15 December 2004** and its administration then given to Protektor. For delib,
  Protektor is the answer to "what happens if the insurer fails" in every product document, and
  the Mannheimer case is the one concrete precedent: **a portfolio transferred and continued, not
  a payout.**
  **§ 314 *Zahlungsverbot; Herabsetzung von Leistungen*** is the supervisor's crisis power and
  the single most important qualification on the word "guarantee" in any delib document.
  **Absatz 1 — the payment ban.** Where an undertaking is **permanently unable to meet its
  obligations** but avoiding insolvency proceedings appears to be in the interest of the insured,
  the supervisor may take the necessary measures; **all kinds of payments may be temporarily
  prohibited**, and the summary names in particular **Versicherungsleistungen**,
  **Gewinnverteilungen** and — specifically for life insurance — **den Rückkauf oder die
  Beleihung des Versicherungsscheins sowie Vorauszahlungen darauf**. A delib document that models
  a surrender option should say that the option is **suspendable by the supervisor** under this
  provision. **Absatz 2 — the benefit reduction.** Under the same conditions the supervisor may
  **reduce the obligations of a life insurer in accordance with its Vermögenslage**: where
  *Deckungsrückstellungen* exist for individual contracts, **the Deckungsrückstellungen are
  reduced first and the Versicherungssummen then recomputed**; where that is not possible, **the
  Versicherungssummen are reduced directly**. **The policyholder's obligation to continue paying
  premiums at the previous level is unaffected.** The supervisor **may proceed unequally where
  special circumstances justify it**, in particular where the distress is rooted more in one
  group of insurances than another.
  Read together, German life guarantees sit under **two distinct write-down powers**: a
  **fund-level 5 % cap** under § 222 where the *Sicherungsfonds* steps in, and an **uncapped,
  asset-position-driven reduction** under § 314 where it does not. **No delib document describes
  a German guarantee as unconditional.**
- Not established: the three § 226 financing figures (0.2 ‰ annual, 1 ‰ target, 1 ‰ special) came
  from summaries of the same query and **there is a real risk the "1 ‰" appears twice because two
  distinct Absätze use the same number, or because one summary conflated them**; both readings
  are recorded and **neither is resolved** — the *Sonderbeitrag* figure is `[unverified]`. The
  fund's member count and current asset stock were not established, nor § 336 VAG's content, nor
  the exact date the statutory fund began operating. **Whether § 314 has ever been applied to a
  German life insurer was not established**, and **the relationship between § 314 and the § 222
  five-per-cent cap — which applies first, and whether the § 314 reduction is bounded — was not
  established and must not be asserted.** Whether Protektor still holds the Mannheimer portfolio
  was not established. A draft **VSAAG** (*Versicherungssanierungs-, -abwicklungs- und
  -aufsichtsänderungsgesetz*) surfaced on the DAV site and would change the resolution framework;
  its content and status are `[unverified]` and it should be checked before this entry is relied
  on. **A correction carried forward:** § 146 VAG is **not** the *Sicherungsfonds*; it concerns
  substitutive Krankenversicherung, which delib treats as out of scope.
- Products: all ten (the outer boundary of every guarantee in the library).

### R13. VAG §§ 351–353 — the Solvency II transitional measures and the 2024 recalculation
- Publisher: Bundesamt für Justiz; BaFin; mirrored by `dejure.org`, `buzer.de`,
  `rechtsportal.de`, `lexsoft.de`, `sozialgesetzbuch-sgb.de`
- Doc type: statutory sections; supervisory application pages; a BaFin *Fachartikel*
- URL: https://dejure.org/gesetze/VAG/351.html (returned);
  https://dejure.org/gesetze/VAG/352.html (returned); https://dejure.org/gesetze/VAG/353.html
  (returned); https://www.buzer.de/352_VAG.htm (returned);
  https://www.bafin.de/DE/Aufsicht/VersichererPensionsfonds/Antraege/Uebergangsmassnahmen/uebergangsmassnahmen_node.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/fa_bj_0702_Solvency_II_Uebergangsmassnahmen.html
  (returned — BaFin *Fachartikel* "Neu rechnen, bitte!")
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries; the
  three section titles from four independent publishers; the sixteen-year linear run-off from one
  summary, consistent with the 2016/2032 dates two others give)
- Content: **§ 352** is the *Rückstellungstransitional*: a deduction that temporarily reduces
  technical provisions on the Solvency II balance sheet, and thereby raises eligible own funds,
  for business written before the regime began. **The maximum deductible portion falls linearly
  from 100 per cent in the year beginning 2016 to 0 per cent on 1 January 2032** — a sixteen-year
  run-off. **§ 351** is the parallel transitional on the risk-free rates. **§ 353**: an
  undertaking that determines it would not meet the SCR without the § 351 or § 352 transitional
  must, **within two months**, submit a plan setting out the gradual introduction of measures to
  raise eligible own funds or reduce the risk profile so that SCR compliance is restored **by the
  end of the transitional period**.
  **The 2024 recalculation is the single most consequential supervisory event in the German life
  market since the LVRG, and it is well corroborated.** In **Q2 2024** BaFin ordered life insurers
  to **recalculate** the *Rückstellungstransitional*, on the ground that the interest-rate rise
  which ended the low-rate phase from 2022 had made the existing deduction amounts inappropriate:
  higher rates sharply reduced Solvency II technical provisions and hence raised own funds, while
  the SCR also fell. A BaFin spokesman is quoted to the effect that **for most companies the
  Rückstellungstransitional takes the value 0 after recalculation**. The effect on published
  ratios is in [R53].
  For delib the discipline is simple: **no delib model implements a transitional**, and any
  German solvency ratio quoted in a delib document must state whether it is before or after the
  2024 recalculation, because the two are not comparable.
- Not established: **the legal instrument by which BaFin "ordered" the recalculation** — a general
  administrative act, individual orders, or an interpretation of § 352 itself — was **not
  established**. How many undertakings held a § 351 transitional as opposed to a § 352 one was not
  established. The exact wording of the § 352 linear formula was not read.
- Products: all ten (cited-not-specified).

---

## 3. Prudential — reserving, the Höchstrechnungszins and the Zinszusatzreserve

The DeckRV is made under § 88 Abs. 3 VAG [R6] and fixes the *Rechnungsgrundlagen* of the German
statutory *Deckungsrückstellung* — the HGB reserve of § 341f HGB [R54], **not** the Solvency II
best estimate. This distinction is the axis of the whole German reserving picture and every
delib document keeps it: an insurer carries **two liability measures**, and the
*Überschussbeteiligung*, the *Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all
run on the **HGB** side.

### R14. DeckRV — the reserving regulation and its § 2, the Höchstrechnungszins
- Publisher: Bundesamt für Justiz; mirrored by `buzer.de`, `umwelt-online.de`, `jurawelt.com`,
  `gesatz.de`, `de.wikipedia.org`; BaFin for the FAQ that states the 2025 change
- Doc type: Rechtsverordnung of **18 April 2016**, and its § 2
- URL: https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html (returned); PDF
  https://www.gesetze-im-internet.de/deckrv_2016/DeckRV.pdf (returned);
  https://www.gesetze-im-internet.de/deckrv_2016/__2.html (returned);
  https://www.buzer.de/gesetz/12006/a198101.htm (returned);
  https://www.bafin.de/SharedDocs/FAQs/DE/VA/Pensionskassen/01_Frage.html (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (five queries; the
  instrument's title and 18 April 2016 date from three independent publishers; the 2025 rate
  change from BaFin's own FAQ title)
- Content: *Verordnung über Rechnungsgrundlagen für die Deckungsrückstellungen*. The sections
  that matter to delib are **§ 2** (the *Höchstrechnungszins*), **§ 4** (*Höchstzillmersätze und
  versicherungsmathematische Berechnungsmethode*, [R16]) and **§ 5**, whose **Absatz 3** carries
  the *Referenzzins* that generates the *Zinszusatzreserve* [R17]. **§ 2 fixes the maximum
  interest rate at which a German life insurer may discount its statutory
  *Deckungsrückstellung* for contracts carrying an interest guarantee**, and therefore — through
  § 138 Abs. 1 VAG's requirement that premiums be adequate to fund that reserve [R8] — the
  maximum rate at which a new tariff may be priced. It is the *Garantiezins* of market language,
  although the two are not legally identical: § 2 caps the **reserving** rate; the guaranteed
  rate a policy carries is a tariff decision that may be lower. BaFin's FAQ title states the
  operative change in terms: *"Zum 1. Januar 2025 wird der Höchstrechnungszins in § 2 der
  Deckungsrückstellungsverordnung (DeckRV) von 0,25 Prozent auf 1,0 Prozent angehoben"* (Stand
  09.09.2024) — quoted from the search result, not from BaFin. Two structural facts a delib
  document needs: the rate applies **to new business at the time of contract conclusion** and
  then **stays with the contract for its whole term**, which is why the German in-force book is a
  stack of cohorts [R15] and why the *Zinszusatzreserve* exists at all; and the same rate applies
  to Pensionskassen, which delib puts out of scope, so the FAQ is cited for the life rate only.
- Not established: the **wording of § 2 was not read**; whether it states a single rate or a rate
  plus qualifications is `[unverified]`. Whether § 2 caps the reserving rate only, or the
  guaranteed rate directly, is **inference from § 88 Abs. 3 VAG's wording, not retrieval**. The
  **section titles disagree between publishers** — `buzer.de` titles § 2 *"Höchstzinssatz"* while
  BaFin, the BMF and the DAV all speak of the *Höchstrechnungszins*; delib writes
  *Höchstrechnungszins* and cites § 2 DeckRV. The full section list of the DeckRV (§ 1, § 3, § 6
  and beyond) was **not established**; one summary attributes a historic 60 %/85 % yield cap to
  "§ 3 DeckRV", which must be the **pre-2016** regulation and must not be carried forward [R56].
- Products: all ten; qualified for FRV, where it bites on the *Rentenphase* and any guarantee
  component rather than on the unit fund.

### R15. The Höchstrechnungszins rate history and the Sechste Verordnung of 19 July 2024
- Publisher: Bundesministerium der Justiz / `recht.bund.de` for the BGBl; Bundesministerium der
  Finanzen for the Referentenentwurf; Deutsche Aktuarvereinigung for the fact sheet; VPV,
  Wikipedia, cecu.de, bavprofis.de and ihre-vorsorge.de for the rate table
- Doc type: amending Rechtsverordnung; professional fact sheet; secondary rate tables
- URL: https://www.recht.bund.de/bgbl/1/2024/250/VO.html (returned);
  https://aktuar.de/content/PDF/Fachwissen/H%C3%B6chstrechnungszins_in_der_Lebensversicherung.pdf
  (returned); https://de.wikipedia.org/wiki/H%C3%B6chstrechnungszins (returned);
  https://www.bundesfinanzministerium.de/Content/DE/Gesetzestexte/Gesetze_Gesetzesvorhaben/Abteilungen/Abteilung_VII/20_Legislaturperiode/2024-06-27-Sechste-VO-VAG/1-Referentenentwurf.pdf?__blob=publicationFile&v=2
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (three queries; the
  BGBl citation from two independent sources; the rate table returned in full by one source and
  corroborated at the endpoints 4.00 %, 0.25 % and 1.00 % by four others)
- Content: **the full rate history**, as returned by the search summary of the rate table. Every
  figure carries its period:

  | Period | Höchstrechnungszins |
  |---|---|
  | 1987 – 06/1994 | **3.50 %** |
  | 07/1994 – 06/2000 | **4.00 %** |
  | 07/2000 – 2003 | **3.25 %** |
  | 2004 – 2006 | **2.75 %** |
  | 2007 – 2011 | **2.25 %** |
  | 2012 – 2014 | **1.75 %** |
  | 2015 – 2016 | **1.25 %** |
  | 2017 – 2021 | **0.90 %** |
  | 2022 – 2024 | **0.25 %** |
  | from 2025 | **1.00 %** |

  Two facts about the table are load-bearing and separately corroborated: the **1994 move was an
  increase**, from 3.50 % to 4.00 %, and the summary states the rate "only increased in 1994 …
  and has only been reduced since then"; and the **2025 move to 1.00 % is the first increase in
  about thirty years**, described in the sources as the first since deregulation in 1994 [R11].
  **The instrument.** The Bundesministerium der Finanzen amended the DeckRV by the **Sechste
  Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz of 19 July
  2024**, published as **BGBl. 2024 I Nr. 250**, setting the *Höchstrechnungszins* at **1.00 %
  with effect from 1 January 2025**; the DeckRV amendment is Article 1 of that regulation, and a
  **Referentenentwurf of 27 June 2024** is on the BMF site. The same regulation **updated the
  absolute floors for the Mindestkapitalanforderung** following a European Commission
  notification. For delib the operative number for a new-business tariff written today is
  **1.00 % (2025 onwards)**, and every model point representing an older cohort carries its
  cohort's rate; all ten products' `**[std]**` guaranteed rates are anchored to this table.
- Not established: the precise **within-year effective dates** for the 2000, 2004, 2007, 2012,
  2015, 2017 and 2022 steps were not established beyond the half-year granularity shown. The
  **MCR absolute floors** set by the Sechste Verordnung are `[unverified]` — no euro figure was
  returned. Two later instruments in the same series were located and **not investigated**: the
  **Siebte Verordnung** (`https://www.recht.bund.de/bgbl/1/2024/414/VO.html`, returned) and the
  **Achte Verordnung** (`https://www.recht.bund.de/bgbl/1/2025/31/VO.html`, returned); their
  content is `[unverified]` and either could have moved the rate again.
- Products: all ten.

### R16. DeckRV § 4 — Höchstzillmersätze
- Publisher: Bundesamt für Justiz; `buzer.de`; `haufe.de` (pre-2016 version under the same
  section number); secondary explanations at `verivox.de`, `ivwkoeln.web.th-koeln.de`,
  `versicherungsbote.de`, `versicherungs-wiki.de`
- Doc type: section of a Rechtsverordnung
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__4.html (returned);
  https://www.verivox.de/lebensversicherung/themen/zillmerung/ (returned);
  https://ivwkoeln.web.th-koeln.de/versicherungslexikon/2015/08/11/zillmerung/ (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries; the
  25 ‰ figure and the 40 ‰ → 25 ‰ cut effective 1 January 2015 from four independent sources)
- Content: *Zillmerung* is the mechanism by which an insurer offsets a contract's one-off
  acquisition costs against its first premiums, which is why a German endowment or annuity has a
  very low surrender value in its early years. **§ 4 DeckRV caps it: the *Zillmersatz* may not
  exceed 25 per mille (25 ‰, i.e. 2.5 %) of the *Beitragssumme***, the sum of all premiums
  payable under the contract. The claim for reimbursement of one-off acquisition costs may be
  covered individually, from the highest possible premium components up to the height of the
  *Zillmersatz*, **from the inception of the insurance**; and **the *Zillmersatz* an undertaking
  uses at the time of contract conclusion applies for the whole term**, so a pre-2015 contract
  keeps its 40 ‰ basis. **The 2015 cut**: the maximum was reduced from **40 ‰ to 25 ‰ with
  effect from 1 January 2015** by the LVRG [R20]; summaries state the pre-reform figure both as
  "40 Promille" and as "bis zu 4 Prozent", which are the same number. For delib this parameter
  sets the shape of the guaranteed surrender-value curve in the first years of every
  regular-premium product, and it **interacts with § 169 VVG's independent five-year-spread
  floor** [R28]: the DeckRV governs what the insurer may **reserve**, § 169 VVG governs what it
  must **pay**, and a delib model carrying a zillmerised reserve applies both separately, the
  tighter binding.
- Not established: **a real conflict in the summaries about what the percentage is a percentage
  of.** One rendering states the cap applies to premiums paid that are *not used for insurance
  coverage and administration cost coverage*; a second, closer to the DeckRV text, states that in
  the *Barwert der Prämien* no more than **2.5 % of premium components above the current value of
  the obligation** may be applied; a third states plainly "25 ‰ der Beitragssumme". **The plain
  reading is the one German market documents use and the one delib adopts, but the exact
  statutory base is not established**, and any restatement of the mechanism beyond "25 ‰ of the
  Beitragssumme" is `[unverified]`. Whether the cap applies to single-premium contracts, and how
  the *Beitragssumme* is defined for them, was not established. The statement that the § 169
  five-year spread and the 25 ‰ cap are **independent constraints** is the compiler's inference;
  no source says so explicitly.
- Products: every regular-premium product load-bearing — KLV, RV, BAS, RIE, FRV, IDX, RLV, BU,
  PFL. Not relevant to SOF, a single-premium payout annuity that is not zillmered in this sense.

### R17. DeckRV § 5 Abs. 3 — the Referenzzins, the Zinszusatzreserve and the Korridormethode
- Publisher: Bundesamt für Justiz; BaFin for the interpretive decision; `buzer.de`, `jurion.de`,
  `de.wikipedia.org`; technical commentary at `heistermannconsulting.de` and
  `msg-insurance-suite.com`; trade press (`cash-online.de`, Versicherungsbote, Pfefferminzia,
  GDV, Allianz Global Investors) for the quantum
- Doc type: section of a Rechtsverordnung; a BaFin *Auslegungsentscheidung*; trade-press analysis
- URL: https://www.gesetze-im-internet.de/deckrv_2016/__5.html (returned);
  https://www.buzer.de/gesetz/12006/a198104.htm (returned);
  https://www.bafin.de/SharedDocs/Downloads/DE/Auslegungsentscheidung/dl_ae_151204_projektion_referenzzins_va.html
  (returned); https://heistermannconsulting.de/referenzzinsatz-fuer-die-zzr-zum-31-12-2022-betraegt-157/
  (returned); https://msg-insurance-suite.com/de/blog/reform-der-zinszusatzreserve-neuregelung/
  (returned);
  https://www.cash-online.de/a/zinszusatzreserve-korridormethode-bringt-zehn-milliarden-euro-entlastung-allein-2018-430796/
  (returned);
  https://www.versicherungsbote.de/id/4939216/Zinszusatzreserve-2024-Milliarden-fliessen-zurueck---und-vieles-bleibt-offen/
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (five queries; the
  corridor reform date and mechanism from four independent sources; the 2018 counterfactual from
  two; the 1.57 % reference rate from three, for three different dates; the 2024 turn from three
  independent outlets)
- Content: **What the ZZR is.** The *Zinszusatzreserve* is the additional German statutory
  reserve that arises when the discount rate applicable under § 5 DeckRV must be reduced below a
  contract's tariff rate, producing a **higher *Deckungsrückstellung* than the tariff rate alone
  would give**. It is an **HGB** reserve, financed out of the insurer's result and, under § 140
  VAG's second escape hatch, out of the free RfB [R10].
  **How the *Referenzzins* is built.** It uses the **month-end levels of the zero-coupon Euro
  interest-rate swap rates with a maturity of ten years published by the Deutsche Bundesbank
  under § 7 der Rückstellungsabzinsungsverordnung**. For each of the **nine preceding calendar
  years** the annual mean of the month-end levels is taken, **rounded up to two decimal places**;
  for the **current calendar year**, the mean of the month-end levels of the **first nine
  months**, likewise rounded up. For **2009 to 2013** the regulation **fixes the annual means by
  statute at 3.81, 3.13, 3.15, 2.14 and 1.96 per cent**. The reference rate is the **arithmetic
  mean over the ten-year reference period**.
  **The Korridormethode.** The calculation was **newly regulated with effect from 23 October
  2018**, published in Bundesgesetzblatt Teil I of **22 October 2018**. The current year's
  reference rate must lie **within a corridor around the previous calendar year's reference
  rate**, limiting the annual change **in both directions**. The reform touched **only the
  determination of the reference rate**; the ZZR calculation itself was unchanged. **The 2018
  counterfactual, corroborated twice**: under the old method the reference rate would have fallen
  from **2.21 % (2017)** to about **1.9 % in 2018**; under the corridor method it fell only to
  **2.10 %**, and the corridor alone meant relief of **about ten billion euros for the industry
  in 2018**. **The reference rate has been 1.57 % at 31 December 2022 and 1.57 % in 2025**, and
  the sources state it has been **unchanged since 2021** — the corridor has pinned it flat for
  five years while market swap rates moved sharply. BaFin's *Auslegungsentscheidung* **Projektion
  des Referenzzinses gemäß § 5 Abs. 3 DeckRV** tells undertakings how to project it forward,
  which is what makes a multi-year ZZR projection auditable [R21].
  **The ZZR in quantum**, all from trade press and rating-agency reporting, never from a
  supervisory source: the industry-wide stock was about **€84 bn at the 2024 balance-sheet
  date**, down from a **peak of €96 bn at end-2021**; about **€8.5 bn was added in 2021**; in
  **2022 and 2023** the stock fell by **more than €3 bn each year**; **2024 was the first year
  since the ZZR was introduced in which life insurers had to add nothing at all**, with about
  **€5 bn flowing back industry-wide** and releases among the **fifty largest providers summing
  to about €3.4 bn**; for **2025** a further **€4 bn** reduction through *Bestandsveränderung*,
  with capacity to release **around €5 bn a year in 2025 and 2026**. **The released funds benefit
  policyholders through a higher *Überschussbeteiligung***, which is the mechanical link between
  this entry and the declared rates in [R53], and the reason German declarations have risen since
  2023 despite the reference rate being pinned at 1.57 %. An earlier projection had the ZZR
  rising to **€225 bn**; that path was made obsolete by the 2022 rate rise and the corridor and
  is recorded only so a reader can date it.
- Not established: **the width of the corridor was not established** — no search result gave the
  percentage-point or relative bound, and it is the single most important missing number in this
  entry; **any delib statement of the corridor width is `[unverified]`**. Whether the ZZR itself
  uses the same fifteen-year look-forward as MindZV § 12 [R18] was **not established**, and the
  two must not be conflated. The rest of § 5 beyond Absatz 3 was not read. The **€5 bn and
  €3.4 bn 2024 figures are different cuts** (whole industry vs the fifty largest) and are
  consistent, but no source reconciles them; likewise the €4 bn realised and €5 bn capacity
  figures for 2025. **None of the quantum figures comes from a supervisory source**; the BaFin
  *Erstversicherungsstatistik* [R53] would carry the audited aggregate and should be preferred
  once retrievable, and every ZZR figure quoted from this entry in a delib document is attributed
  to the trade press.
- Products: KLV, RV, BAS, RIE, SOF, IDX load-bearing; BU and PFL qualified (annuities in payment
  carry a tariff rate and therefore a ZZR); RLV and FRV background. **Cited-not-specified: no
  delib model builds a ZZR.**

---

## 4. Prudential — the surplus regulations, the LVRG and the supervisor

### R18. MindZV — the minimum allocation to the RfB, and §§ 11–13
- Publisher: Bundesamt für Justiz; mirrored by `buzer.de`, `lxgesetze.de`, `freirecht.de`,
  `anwalt.de`, `gesetze.legal`, `de.wikipedia.org`, `bundestag.github.io`
- Doc type: Rechtsverordnung of **18 April 2016**, made under § 145 VAG [R10]
- URL: https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html (returned);
  https://www.gesetze-im-internet.de/mindzv_2016/__4.html (returned);
  https://www.gesetze-im-internet.de/mindzv_2016/__6.html (returned);
  https://www.buzer.de/gesetz/12013/a198221.htm (returned, § 6);
  https://www.gesetze-im-internet.de/mindzv_2016/__11.html (returned);
  https://www.buzer.de/gesetz/12013/a198226.htm (returned, § 11);
  https://lxgesetze.de/mindzv/11 (returned); https://freirecht.de/g/MindZV:11 (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (four queries; the
  **90 / 90 / 50** split returned by two independent queries with identical percentages and
  identical assignment to the three result sources; § 6's detailed wording from one source in
  near-statutory form; § 11's title from five independent publishers)
- Content: *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung* — the
  arithmetic floor under the German *Überschussbeteiligung*. It applies to life insurers **except
  Pensionskassen**, which have their own § 5.
  **The three result sources and their minimum shares.** **§ 6 *Kapitalanlageergebnis* — 90 %**:
  per the returned wording, the minimum allocation to the RfB from investment income for
  profit-participating contracts is **90 per cent of the Kapitalerträge to be credited under § 3
  Abs. 1, less the Rechnungszinsen**, without reducing the externally financed provision
  component under § 3 Abs. 7 Satz 5 and without the pro-rata interest on *Pensionsrückstellungen*
  attributable to profit-participating contracts. **The subtraction of the *Rechnungszinsen* is
  the crucial detail: the guarantee is funded first, and only the excess is shared 90/10.**
  **§ 7 *Risikoergebnis* — 90 %**, raised from 75 % by the LVRG with effect from **7 August
  2014** [R20]. **§ 8 *Übriges Ergebnis* — 50 %**, the cost result, shared half and half.
  **§ 4 — how the minimum is assembled.** From the sum of the amounts under § 6 Abs. 1, § 7 and
  § 8, the ***Direktgutschrift*** attributable to profit-participating contracts is **deducted** —
  including *Schlusszahlungen* from participation in *Bewertungsreserven* insofar as those are
  distributed as a direct credit. **Alt- and Neubestand are treated separately throughout** [R11].
  **A mathematically negative minimum allocation is replaced by zero.** Those two rules are what
  make the MindZV a **minimum transfer to the RfB rather than a minimum payout**.
  **§§ 11–13 — the Sicherungsbedarf machinery** behind § 139 Abs. 3/4 VAG [R9], i.e. the test
  that decides whether a departing policyholder receives any share of the fixed-income
  *Bewertungsreserven*. **§ 11**: the reference rate is the **zero-coupon Euro interest-rate swap
  rate published by the Deutsche Bundesbank under § 7 der Rückstellungsabzinsungsverordnung, with
  a maturity of ten years, at the end of the month preceding the date on which the
  Bewertungsreserven are determined**. Note the difference from the ZZR reference rate [R17]: the
  ZZR rate is a **ten-year average of ten-year swap rates**, damped by the corridor; the
  *Sicherungsbedarf* rate is a **single month-end spot** ten-year swap rate. **They are different
  numbers computed from the same Bundesbank series, and confusing them is one of the standard
  errors in describing a German life balance sheet.** **§ 12**: at each determination date the
  § 11 rate is **compared with the highest Rechnungszins applicable to the contract over the next
  fifteen years**; where the reference rate is lower, the contract generates a *Sicherungsbedarf*
  and to that extent the fixed-income valuation reserves are locked away from departing
  policyholders. The fifteen-year window is what makes the test bite on annuity business in
  particular: a deferred annuity whose *Rentenphase* guarantee runs at 3.25 % keeps generating a
  *Sicherungsbedarf* long after a comparable endowment has matured.
  **Why this is the centre of the delib library.** Six of the ten products are
  profit-participating general-account contracts whose credited return is the guarantee plus a
  discretionary share of these three results. Any delib model of the *Überschussbeteiligung*
  chassis represents at least the three result sources, the 90/90/50 floor, the
  direct-credit-versus-RfB split, and the fact that the floor binds on the **HGB** accounts.
- Not established: **§ 7 and § 8 were never returned in their own words** — the 90 % and 50 %
  come from summaries of § 4 and of the regulation as a whole, twice and consistently, but the
  section texts were not read. **§ 3's definition of the *zuzurechnende Kapitalerträge* — the
  base the 90 % bites on — was not established, and it is the number that actually matters for a
  projection.** § 2 (definitions, including *Direktgutschrift*) was not retrieved. Whether the
  50 % on the *übriges Ergebnis* applies symmetrically to a negative cost result was not
  established. **§ 13 was not retrieved**; its title and content are `[unverified]` and it is
  named only because the numbering implies further provisions. The **valuation formula in § 12**
  — how the *Zinsverpflichtung* is computed from the reference rate — was not returned. The
  *Rückstellungsabzinsungsverordnung* itself was not researched beyond the cross-reference.
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing; RLV, BU, PFL load-bearing **on the risk
  result** — the 90 % share of the *Risikoergebnis* is what funds a German term, BU or Pflege
  tariff's *Beitragsrückerstattung*; FRV qualified, see [R21].

### R19. RfBV — the collective part of the Rückstellung für Beitragsrückerstattung
- Publisher: Bundesamt für Justiz; `dejure.org` for the BGBl citation; `jurawelt.com`; Bundesrat
  Drucksache 585/16 as background; BaFin for the interpretive decision on *Teilkollektivierung*
- Doc type: Rechtsverordnung, **BGBl. I 2015 S. 300**
- URL: https://www.gesetze-im-internet.de/rfbv/BJNR030000015.html (returned);
  https://www.gesetze-im-internet.de/rfbv/__3.html (returned);
  https://dejure.org/BGBl/2015/BGBl._I_S._300 (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_110419_mindestzufuehrung_rfb_va.html
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (two queries; three
  independent publishers plus the Bundesrat papers, with one substantive summary of §§ 2 and 3
  that reads close to the statutory wording)
- Content: implements § 140 Abs. 1 Satz 2 VAG [R10]. It applies to life insurers **except
  Sterbekassen and regulierte Pensionskassen**. **§ 2 — the cap on the *ungebundene* RfB.** On
  establishing a *kollektiver Teil*, the undertaking must set an ***Obergrenze* for the
  ungebundene Rückstellung für Beitragsrückerstattung of the *Teilbestände*, expressed as a
  percentage**; the percentage is **at least 100**, is **identical for all Teilbestände**, and
  **may be changed from the prior year only with the supervisor's consent**. Where a
  *Teilbestand*'s *ungebundene* RfB **exceeds** that ceiling and no *Rückführungen* into the
  *Teilbestände* take place at the balance-sheet date, **the excess is transferred to the
  kollektiver Teil**. **§ 3** requires an *Obergrenze* for the collective part itself, as a
  percentage of an amount. **Why it exists**: the collective part lets an insurer hold surplus
  committed to policyholders as a class but not yet attributed to any *Teilbestand*, which is what
  makes cross-cohort smoothing legally possible without breaching the § 138 Abs. 2 VAG equal
  treatment rule [R8]. BaFin's interpretive decision on the *Zusammenwirken von Mindestzuführung
  zur RfB und Teilkollektivierung* (**19 April 2011**) governs how the MindZV floor interacts with
  it [R21]. **Vocabulary for delib**: the statutory term is *ungebundene* RfB; German market
  writing says *freie RfB* for the same thing and *gebundene RfB* for the part already committed
  to declared shares and to the *Schlussüberschussanteilfonds* of § 28 RechVersV [R54].
- Not established: **the percentage base in § 3 was not established**; one summary of § 140 VAG
  describes the ceiling as "a percentage of declared profit shares and the expected expenses for
  declared Direktgutschriften, with a minimum percentage of 100", which appears to describe
  **§ 2**, not § 3 — **the two are conflated in the summaries and the conflation is not
  resolved**. § 1 (*Geltungsbereich*) and any further sections were not retrieved. **Whether the
  German market actually uses the collective part, and how large it is, was not established.**
- Products: KLV, RV, BAS, RIE, IDX, SOF load-bearing for the surplus chassis; the other four
  qualified.

### R20. LVRG 2014 — the Lebensversicherungsreformgesetz
- Publisher: Bundesgesetzblatt / `dejure.org` for the citation; Deutscher Bundestag for the
  Drucksache and the plenary record; Gabler and Haufe for the summaries; DIA/ITA for the impact
  study
- Doc type: federal statute, **BGBl. I 2014 S. 1330**, of **1 August 2014**; Gesetzentwurf
  **BT-Drs. 18/1772** of 18 June 2014
- URL: https://dejure.org/BGBl/2014/BGBl._I_S._1330 (returned);
  https://dserver.bundestag.de/btd/18/017/1801772.pdf (returned);
  https://www.haufe.de/steuern/gesetzgebung-politik/aenderungen-im-ueberblick-das-neue-lebensversicherungsreformgesetz_168_265064.html
  (returned); https://wirtschaftslexikon.gabler.de/definition/lebensversicherungsreformgesetz-54407
  (returned); https://www.dia-vorsorge.de/wp-content/uploads/2019/07/150519_DIA_Studie_final_LVRG.pdf
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (three queries; the
  three headline changes from four independent sources with identical figures and dates)
- Content: *Gesetz zur Absicherung stabiler und fairer Leistungen für Lebensversicherte* — the
  reform that reshaped the German *Überschussbeteiligung* for the low-rate era. Three of its
  changes are load-bearing for delib. **(1) Bewertungsreserven restricted**: the distribution
  restriction applies **only to valuation reserves from festverzinsliche Wertpapiere**, and
  participation by departing policyholders is limited where an insurer's provisions are, at
  prevailing low rates, insufficient to fund the guarantees given to remaining policyholders —
  this is the *Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG [R9] and MindZV §§ 11–12 [R18].
  **(2) *Höchstzillmersatz* cut from 40 ‰ to 25 ‰** of the *Beitragssumme*, effective **1 January
  2015** [R16]. **(3) *Risikoüberschuss* share raised from 75 % to 90 %**, effective **7 August
  2014**, now § 7 MindZV [R18] — the single change that most affects delib's biometric products,
  since a German term, BU or Pflege tariff's surplus is predominantly a risk surplus. Alongside
  them, **distributions to shareholders may be prohibited** where needed to secure the guaranteed
  benefits (an *Ausschüttungssperre*). The constitutionality of the LVRG's insertion into
  **§ 153 Abs. 3 Satz 3 VVG** was litigated and upheld [R36].
- Not established: the LVRG amended the **old** VAG (§ 56a a.F. and others) and **the mapping
  from those old sections onto the 2016 VAG sections was not established**; delib cites the
  current sections and describes the LVRG as the reform that introduced the rules, not as the
  current legal source. Whether the LVRG also introduced a commission cap
  (*Provisionsdeckel*) — trade press in the results discusses one as a later, separate proposal —
  was **not established and is not asserted**.
- Products: all ten; most materially RLV, BU and PFL (the 90 % risk-result share) and KLV, RV,
  BAS, RIE (the *Bewertungsreserven* restriction and the Zillmerung cut).

### R21. BaFin — the FinDAG, the MaGo and the Auslegungsentscheidungen
- Publisher: Bundesamt für Justiz for the FinDAG; Bundesanstalt für Finanzdienstleistungsaufsicht
  for the circulars, interpretive decisions and topic pages; Gabler, KPMG, Wavestone and Fincon
  as secondary
- Doc type: federal statute; supervisory circular; a cluster of *Auslegungsentscheidungen*
- URL: https://www.gesetze-im-internet.de/findag/BJNR131010002.html (returned);
  https://www.bafin.de/DE/die-bafin/ueber-die-bafin/aufgaben/versicherungsaufsicht/versicherungsaufsicht_node.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/EN/Rundschreiben/2017/rs_1702_mago_va_en.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Konsultation/2025/kon_05_2025_konsultation_ueberarbeitung_mago_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_151204_wechselwirkung_ueberschussbeteiligung_neugeschaeft_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_160610_beteiligung_an_bewertungsreserven.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_091222_mzffglv_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_110419_mindestzufuehrung_rfb_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_161111_kapitalmarktmodelle_va.html
  (returned);
  https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Auslegungsentscheidung/VA/ae_160222_latente_steuern_auf_versicherungstechnische_rueckstellungen.html
  (returned)
- Retrieved: **no** — direct HTTP egress blocked; corroborated by web search (four queries;
  BaFin's own pages plus five independent secondary sources agreeing on the 2002 founding, the
  FinDAG date, the MaGo dates and the supervisory objective; the interpretive decisions returned
  as URLs with **one or two sentences of summary each**)
- Content: **The institution.** BaFin was created in **2002** by the
  *Finanzdienstleistungsaufsichtsgesetz of 22 May 2002*, merging the Bundesaufsichtsämter for
  banking, securities and insurance into a single *Allfinanzaufsicht*; the merger was
  organisational and **did not create new or extended competences**. BaFin is subject to the
  *Rechts- und Fachaufsicht* of the Bundesministerium der Finanzen (§ 2 FinDAG) and supervises
  under the KWG, the VAG and the WpHG. **The objective**: the stated main objective of German
  insurance supervision is to ensure the **permanent fulfilment capability of insurance
  contracts** — the *dauernde Erfüllbarkeit* standard that also appears in § 341e HGB [R54] and
  § 138 Abs. 1 VAG [R8] — together with the protection of the insured and beneficiaries.
  Supervision splits into *Finanzaufsicht/Solvenzaufsicht*, *Rechtsaufsicht* and, in German
  usage, *Missstandsaufsicht*.
  **The MaGo.** *Rundschreiben 2/2017 (VA) — Mindestanforderungen an die Geschäftsorganisation
  von Versicherungsunternehmen* was **published 25 January 2017 and in force from 1 February
  2017**. It **interprets the business-organisation provisions of the VAG and of Delegated
  Regulation (EU) 2015/35 and binds BaFin's own application of them**. Its content covers
  *Aufbauorganisation*, internal guidelines, the Solvency II *Schlüsselfunktionen*, the risk
  management system, undertaking-specific stress tests and *Ausgliederung*. A **revised version
  was published on 14 July 2025** following **Konsultation 05/2025** opened 29 January 2025, its
  **Chapter 8** specifying group-level requirements. For delib the MaGo is the reason the
  ***versicherungsmathematische Funktion*** exists alongside the § 141 VAG *Verantwortlicher
  Aktuar* [R11] — **two distinct actuarial roles, one from Solvency II governance and one from
  German life law, which delib does not conflate.**
  **The Auslegungsentscheidungen.** These are BaFin's published statements of how it will apply a
  provision. They are not law, but they bind BaFin's own practice and carry much of the operative
  detail the regulations leave open. Established, each from one or two sentences of summary:
  (1) ***Wechselwirkungen zwischen Überschussbeteiligung und Neugeschäft*** (4 December 2015) —
  German life and health insurance is characterised by **collective mechanisms**, so new business
  can affect the future *Überschussbeteiligung* of the existing portfolio, and BaFin addresses
  when that interaction is acceptable. (2) ***Ausweis der Beteiligung an den Bewertungsreserven
  in der Standmitteilung*** (10 June 2016) — the annual statement must disclose the **full**
  allocation of the participation in *Bewertungsreserven*, and showing only a guaranteed minimum
  share (*Sockelbeteiligung*) **is not sufficient**, because without full disclosure the
  policyholder cannot obtain clarity about the development of their claims as § 155 Satz 1 VVG
  requires [R25]. (3) ***Mindestzuführung in der fondsgebundenen Lebensversicherung***
  (22 December 2009) — directly load-bearing for FRV, whose investment result belongs to the
  policyholder and whose MindZV base is therefore not the general account's. (4)
  ***Zusammenwirken von Mindestzuführung zur RfB und Teilkollektivierung*** (19 April 2011)
  [R19]. (5) ***Auswirkung von passiver Rückversicherung auf die Angemessenheit der Zuführung zur
  RfB*** — the design of reinsurance treaties affects the minimum allocation but **must not lead
  to an inappropriate reduction of policyholders' Überschussbeteiligung**. (6) ***Anforderungen
  an Kapitalmarktmodelle für die Bewertung der versicherungstechnischen Rückstellungen unter
  Solvency II*** (11 November 2016) — calibration of parameters and scenarios must be consistent
  with the relevant risk-free curve used for the best estimate under **Art. 77(2) of Directive
  2009/138/EC** [R1]. (7) ***Latente Steuern auf versicherungstechnische Rückstellungen unter
  Solvency II*** (22 February 2016). (8) ***Projektion des Referenzzinses gemäß § 5 Abs. 3
  DeckRV*** [R17].
- Not established: **none of these documents was read.** Each is represented by one or two
  sentences of search summary; the operative wording, the thresholds and the worked examples are
  all unknown, and **the interpretive decisions are the weakest-evidenced supervisory material in
  this file relative to their importance**. The date of item (5), and a 2020 decision on the same
  subject that the summaries mention, were **not established**. Whether any of them has been
  withdrawn or superseded was not checked. The four Solvency II **Schlüsselfunktionen** are named
  only generically in the returned summaries; their individual names and VAG section numbers were
  **not established**. Whether the 2025 MaGo revision is already in force, or applies from a
  stated date, was not established.
- Products: FRV load-bearing (item 3); KLV, RV, BAS, RIE, IDX, SOF for items 1, 2, 4, 5; all ten
  for the institutional context and items 6 and 7.

