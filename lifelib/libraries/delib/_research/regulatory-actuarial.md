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

