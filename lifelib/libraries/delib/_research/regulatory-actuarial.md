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

