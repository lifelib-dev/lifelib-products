# Regulatory and Actuarial References — German Life Insurance

**Status:** Draft, 2026-08-29.

Curated reference library for the Germany section of the reference-product library. It covers the prudential layer (Solvabilität II as
transposed into the *Versicherungsaufsichtsgesetz*, the statutory *Deckungsrückstellung* and the *Zinszusatzreserve*), the surplus
regulations that put an arithmetic floor under the *Überschussbeteiligung*, the contract law of the *Versicherungsvertragsgesetz*,
conduct and disclosure, the case law and the market's model conditions, the tax architecture of the *Drei-Schichten-Modell*, the
biometric bases and market statistics, and the accounting and professional standards that the ten reference cash-flow-model
implementations rely on.

**The ten products this page serves**, by slug: `kapitallebensversicherung`, `klassische_rentenversicherung`,
`fondsgebundene_rentenversicherung`, `indexpolice`, `basisrente`, `riester_rente`, `sofortrente`, `risikolebensversicherung`,
`berufsunfaehigkeit`, `pflegerentenversicherung`.

Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R1]`); the **R1–R56 numbering below is frozen — do not renumber
and do not reuse a number**, because product documentation cites against it and a renumbering silently changes what every one of those
citations means. Unused ids are simply omitted downstream, leaving gaps, and each product's `sources.md` records which ids are absent
and why. Within this page, plain `[R#]` refers to the same entries. All URLs accessed **2026-08-29**.

**Citation discipline.** `[S#]` marks a fact from a primary product document listed in a product's own `sources.md`; `[R#]` a fact
from a product-specific regulatory or actuarial reference in that same file; `[REG-R#]` a fact from this page. **[std]** marks a
standardization introduced for the reference implementation — a parameter or convention chosen where sources vary, are proprietary or
are silent, each carrying a rationale and, where one could be established, the observed range across insurers. **[unverified]** marks
a claim from general knowledge or a secondary snippet that no search result corroborated. The hard rule the library runs on: **every
quantitative parameter is either source-tagged or marked [std]. No number anywhere in `delib` is untagged.**

---

## Retrieval conditions — read this before relying on a single line below

This section is stated first, in full, and prominently, because it is the single most important thing about this page and it is unlike
anything the sister libraries `uslib`, `uklib`, `jplib` and `frlib` had to record. Two independent limits applied while `delib` was
built.

**1. Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl` are refused with **HTTP 403 at the
egress gateway** for every host outside a short package-registry allowlist. The hosts that matter for German life insurance were all
tried and all refused:

| Host | What it would have served | Result |
|---|---|---|
| `gesetze-im-internet.de` | VAG, VVG, DeckRV, MindZV, RfBV, RechVersV, BerVersV, HGB, EStG, AltZertG, ZPO, SGB V/XI | refused, HTTP 403 |
| `bafin.de` | Rundschreiben, Auslegungsentscheidungen, Merkblätter, Erstversicherungsstatistik | refused, HTTP 403 |
| `aktuar.de` | DAV press releases, Zinsberichte, Fachwissen fact sheets | refused, HTTP 403 |
| `gdv.de` | *Die deutsche Lebensversicherung in Zahlen*, statistics pages, Musterbedingungen | refused, HTTP 403 |
| `bundesfinanzministerium.de` | Referentenentwürfe, BMF-Schreiben, Muster-Produktinformationsblatt | refused, HTTP 403 |
| `destatis.de` | Sterbetafeln, Generationensterbetafeln, Pflegestatistik | refused, HTTP 403 |
| `dejure.org` | statute mirrors, BGBl citations, case-law cross-references | refused, HTTP 403 |
| `eur-lex.europa.eu` | Solvency II, the Delegated Regulation, PRIIPs, the IDD | refused, HTTP 403 |
| `de.wikipedia.org` | general-reference corroboration | refused, HTTP 403 |

Not one statutory text, not one BaFin circular, not one DAV table, not one BGH judgment and not one statistical release was opened.
**No document cited anywhere on this page was retrieved, and every entry below records `Fetched: no` for that reason.**

**2. The only research channel was `WebSearch`, and its 200-call budget was exhausted during the build.** `WebSearch` returns titles,
URLs and a search-engine summary of the matched pages. That is real evidence — several long German sentences of statutory wording
reached this library that way — but it is a *secondary summary*, never a retrieved document. The budget was consumed by a prudential
and supervisory sweep of roughly 35 German-language queries, a contract-law and conduct sweep of roughly 45, and the ten per-product
sweeps. **The tax sweep and the biometric sweep each ran zero successful searches**; both of their opening queries were refused for
budget, as was a confirming query issued while compiling this page and a further query issued while writing it.

**The consequence, stated plainly: every entry on this page was established from search-result summaries, and a reader must re-verify
against the instrument itself before relying on any of it.** A `delib` citation is a **pointer, not a certificate**. It names the
instrument a claim should be checked against; it does not assert that anyone checked it. That is a weaker thing than an `frlib`
citation, where Légifrance served in full, and the difference is stated here rather than glossed.

What follows from it, exactly:

- **No verbatim quotation on this page is attributed to an instrument.** Where a German sentence appears in quotation marks, the
  quotation is **of a search-result summary**, and the entry says so. What an instrument *provides* is written in the compiler's own
  words.
- **No URL on this page is fabricated.** A URL appears only where a search result actually returned it — which is true of the great
  majority of the URLs in R1–R37 — or where it is the obvious canonical `gesetze-im-internet.de` section form
  `https://www.gesetze-im-internet.de/<slug>/__<section>.html`, whose pattern dozens of returned pages confirm, in which case it is
  marked `[unverified canonical form]`. Where neither holds, the entry says **not established**. No Bundesgesetzblatt citation,
  document reference number or page count is invented anywhere.
- **`[unverified]` is used generously and means what it says.** It is applied to every specific paragraph number, effective date,
  monetary amount, percentage and market figure that no search result confirmed. It is *not* applied to the general shape of a
  well-established mechanic, because that would drown the signal — but the moment a claim becomes *specific and numeric* it carries
  either a corroborated source or the tag.
- **The five domains of this page are not equally supported and must not be read as if they were.** Prudential and supervisory
  (R1–R21) rests on ~35 German queries, with statutory titles corroborated across five to ten independent publishers and substance
  across one to three. Contract law and conduct (R22–R37) is the strongest block, on ~45 queries, several of whose summaries reproduce
  statutory wording. **Tax and the three layers (R38–R46) and biometric bases and market statistics (R47–R53) rest on zero successful
  searches**: what corroboration they carry is second-hand from the two sweeps above, named per entry, and everything else is general
  knowledge. Accounting and professional standards (R54–R56) is partial — HGB, RechVersV, BerVersV and IFRS 17 came from the
  prudential sweep; the DAV standards did not.
- **Where a figure is needed by a reference implementation and cannot be confirmed, the honest form downstream is a [std] parameter
  with a stated rationale and an argued plausible range — not a [REG-R#] citation.** A `[std]` number is honest; a wrong `[REG-R#]`
  number is not.

**One structural warning that governs the whole biometric section.** The five tables at the centre of German life pricing — **DAV 2008
T**, **DAV 2004 R**, **DAV 2004 R-Bestand**, **DAV 1997 I / RI / TI** and **DAV 2008 P** — are the property of the Deutsche
Aktuarvereinigung, are distributed to members and licensees rather than published, and are **not redistributable**. `delib` ships
**none of them** and quotes **no $q_x$, no incidence rate, no improvement rate and no annuity factor from any of them**. Every
decrement CSV in the library is a **[std]** proxy, anchored so that the product's own worked example reproduces exactly. That is the
same posture `frlib` took towards TH 00-02 and TGH05, and it is not a workaround: it is the only lawful and honest way to ship a
public reference library against a proprietary basis.

---

**Regulatory architecture in one line:** BaFin supervises German life insurers under Solvabilität II as transposed into the **VAG**,
and there is no second national supervisor — conduct and prudential supervision sit inside one authority — while the **VVG** carries
the contract law in a *separate statute with a different addressee*, and the arithmetic of the guarantee and the surplus is delegated
to two ministerial regulations, the **DeckRV** (the *Höchstrechnungszins*, the *Höchstzillmersatz*, the *Referenzzins* behind the
*Zinszusatzreserve*) and the **MindZV** (the 90 / 90 / 50 minimum allocation to the *Rückstellung für Beitragsrückerstattung*); which
is why a German model reads four instruments where a French model reads one code.

**Ten German terms carry the whole library** and are used untranslated after first use, because several have no English equivalent and
two are routinely mistranslated.

***Überschussbeteiligung*** — the policyholder's participation in the insurer's surplus. It is **not** the French *participation aux
bénéfices* and must never be rendered that way in a comparative sentence: the French version is a collective statutory minimum
computed from a regulated account, the German one an **individual contractual entitlement** (§ 153 VVG, [R24]) with a **statutory
minimum transfer to a reserve** on top (the MindZV, [R18]). ***Deckungs- rückstellung*** — the German statutory (HGB) reserve,
prospective, computed on the *Rechnungsgrundlagen* of the premium calculation (§ 341f HGB, [R54]; DeckRV, [R14]). It is **not** the
Solvency II best estimate, and the whole German picture depends on keeping the two apart: an insurer carries **two liability
measures**, and the *Überschussbeteiligung*, the *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side.
***Rückkaufswert*** — the surrender value (§ 169 VVG, [R28]), floored at the *Deckungskapital* that results from spreading the charged
acquisition and distribution costs evenly over the first five contract years. ***Zillmerung*** — offsetting a contract's one-off
acquisition costs against its first premiums, capped at **25 ‰** of the *Beitragssumme* by § 4 DeckRV since 1 January 2015 ([R16]).
***Höchstrechnungszins*** — the maximum rate at which the *Deckungsrückstellung* may be discounted, fixed in § 2 DeckRV ([R14]);
market language calls it the *Garantiezins*, but the two are not legally identical, because § 2 caps the **reserving** rate while the
rate a policy guarantees is a tariff decision that may be lower. ***Zinszusatzreserve*** — the additional HGB reserve that arises when
the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's tariff rate ([R17]); it exists in no other jurisdiction in this
repository. ***Rentenfaktor*** — euros of monthly annuity per €10,000 of accumulated capital, the number that converts a unit-linked
or index account value into an annuity; the BGH struck down asymmetric unilateral reduction clauses in 2025 ([R36]).
***Beitragsgarantie*** — a guarantee that at least the contributions paid are available at the start of the payout phase, statutory
for a certified Riester contract ([R43]). ***Berufsunfähigkeit*** — inability to pursue **the last occupation as it was structured
before the impairment** (§ 172 Abs. 2 VVG, [R29]); it is *not* "disability" in the general-labour-market sense, and the statutory
scheme's *Erwerbsminderung* is that other thing. ***Pflegegrad*** — one of the five care levels of § 15 SGB XI, which replaced the
three *Pflegestufen* on 1 January 2017 ([R51]); the replacement is a **definitional break**, not a change in the underlying risk, and
the BGH has refused to map the two scales ([R36]).

Four more terms recur throughout. ***laufende Verzinsung*** is the declared annual credited rate and equals the *Garantieverzinsung*
**plus** the *laufende Zinsüberschussbeteiligung* — **not** a surplus rate on top of the guarantee; adding the two is the commonest
arithmetic error in describing a German contract and is a numbered pitfall in every affected product ([R53]). ***Direktgutschrift***
is surplus credited immediately rather than parked in the RfB, and is **deducted** from the MindZV minimum, which is why the MindZV is
a minimum *transfer*, not a minimum *payout* ([R18]). ***Bruttobeitrag*** and ***Zahlbeitrag*** are the tariff premium and the premium
actually collected after surplus is applied as a *Beitragsverrechnung*; the gap is large and persistent in *Berufsunfähigkeit* and the
*Zahlbeitrag* is **not guaranteed** ([R37], [R53]). ***Altbestand*** / ***Neubestand*** are contracts concluded before / from **29
July 1994**, the deregulation date ([R11]); **all ten delib products are Neubestand business**.

**Scope note on capital.** The SCR and the MCR exist under Solvabilität II [R1] [R2] as transposed by §§ 96–110 VAG [R6], and the
German statutory balance sheet carries its own *Deckungsrückstellung* and *Zinszusatzreserve* [R14] [R17] [R54] — but this library
treats the capital layer as **cited-not-specified**. The reference models produce **gross, undiscounted, best-estimate-style liability
cash flows and stop short of the discounting**. The Solvency II balance sheet, the SCR and MCR, the risk margin, the
*Deckungsrückstellung*, the *Zinszusatzreserve*, the RfB as a balance-sheet stock and the IFRS 17 measurement are referenced, never
specified. No risk-free curve value, no volatility adjustment and no cost-of-capital rate on this page was read from a retrieved
instrument, so **any discount rate, asset return or declared rate in a product document is `**[std]**`** with a rationale rather than
a citation.

---

## Product-relevance matrix

`x` = load-bearing for that product's specification, technical notes or model; `(x)` = qualified, conditional or background relevance
— the entry governs the product but does not shape its cash flows, or reaches it only through an option or a rider; blank = not
relevant.

**Column key.** `KLV` = kapitallebensversicherung · `RV` = klassische_rentenversicherung · `FRV` = fondsgebundene_rentenversicherung ·
`IDX` = indexpolice · `BAS` = basisrente · `RIE` = riester_rente · `SOF` = sofortrente · `RLV` = risikolebensversicherung · `BU` =
berufsunfaehigkeit · `PFL` = pflegerentenversicherung.

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
| R56 | DAV Fachgrundsätze; the Höchstrechnungszins recommendation | x | x | x | x | x | x | x | x | x | x |

**One instrument is deliberately absent from the matrix and is recorded here instead.** BaFin *Rundschreiben 11/2017 (VA)*, the
*Kapitalanlagerundschreiben*, and the **Anlageverordnung (AnlV)** it interprets apply to **small insurers under §§ 212–217 VAG and to
domestic Pensionskassen and Pensionsfonds** — **not** to the Solvency II life insurers that write the ten delib products, which are
governed by the qualitative § 124 VAG prudent person principle [R7]. German market writing routinely cites AnlV quotas as if they
bound all insurers; since 1 January 2016 they do not bind the large life insurers at all. The circular is discussed inside R7 so that
no delib author misapplies an AnlV quota, and it carries no id of its own.

---

## 1. Prudential — the European layer

The Solvency II layer reaches German life business **through the VAG**, not directly. That is why this page cites VAG sections
throughout and directive articles only where the European layer is itself the point, and it is why **no Solvency II article number in
this library was read from the instrument**: `eur-lex.europa.eu` is refused at the egress gateway and every article number below comes
from a secondary summary.

(delib-reg-r1)=

### R1. Richtlinie 2009/138/EG — Solvabilität II

- **Publisher:** European Parliament and Council (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32009L0138 (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (one query,
  four publishers, two substantive and agreeing)
- **Annotation:** The Level 1 directive Germany transposes into the VAG, and therefore the instrument behind every valuation rule a
  German modeller actually reads as a VAG section. Established from the summaries: **the value of technical provisions equals the sum
  of a best estimate and a risk margin, calculated separately**; the risk-free yield curve for the best estimate is that of **Article
  77(2)**, a reference independently confirmed by BaFin's interpretive decision on capital-market models [R21]; the **risk margin of
  Article 77(5)** excludes any capital add-on; and **Article 76** appears in its usual role as the article cited for the
  best-estimate-plus-risk-margin rule. Governs the valuation basis of all ten delib products, which produce the gross best-estimate
  cash flows and stop short of the measurement the directive prescribes. **Unverified:** no article number here was read from the
  instrument; the three-pillar structure, the **99.5 % one-year VaR** confidence level and the adoption date are commonly reported but
  **were not returned by any search in this sweep**.

(delib-reg-r2)=

### R2. Delegierte Verordnung (EU) 2015/35

- **Publisher:** European Commission (EUR-Lex)
- **URL:** https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32015R0035&from=DE (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries,
  four publishers, two substantive on the risk-margin articles)
- **Annotation:** The Level 2 implementing measures, directly applicable without national transposition, and where the operative
  Solvency II detail lives — which is why a German modeller looking for contract boundaries, expense rules or standard-formula
  stresses reads this rather than the VAG. Established: **Art. 37** governs the risk margin, resting on the assumption that the
  **entire portfolio of obligations is transferred to another undertaking**; **Art. 38** defines that hypothetical
  *Referenzunternehmen*; **Art. 39** sets the *Kapitalkostensatz*; and the title carries the adoption date of **10 October 2014**.
  **Unverified, and it is most of what a modeller would want.** The **6 % cost-of-capital rate was never confirmed from any text** —
  one summary notes explicitly that the figure did not appear in the returned results, the only support being the 2025 review's
  "reduced from 6 to 4.75 per cent" wording [R3].

(delib-reg-r3)=

### R3. Richtlinie (EU) 2025/2 — the Solvency II review

- **Publisher:** European Parliament and Council, Official Journal
- **URL:** https://aktuare.de/de/presse/pressemitteilungen/2682-pm-risikomarge-solvencyii.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries,
  five professional-services analyses agreeing on the title, the date, the first application and the cost-of-capital cut)
- **Annotation:** The amending directive from the 2019–2021 review, **dated 27 November 2024** and **published in the Official Journal
  on 8 January 2025**. **The new rules apply for the first time on 30 January 2027**, and Member States must transpose within two
  years, so German transposition into the VAG is due before that date. Two changes matter to a liability model: the
  **Kapitalkostensatz underlying the risk margin falls from 6 % to 4.75 %**; and an **exponential, time-dependent lambda factor** is
  to be introduced through the Level 2 regulation, reducing the level and volatility of the risk margin for long-term business, with
  **no lower bound** and an effect on **projected years ≥ 28** — a reduction most beneficial to insurers with long-term business,
  which is exactly the German life book. Otherwise the reform combines proportionality relief for small and non-complex undertakings
  with tightened qualitative requirements on governance, risk management and sustainability. **Unverified: the summaries conflict on
  entry into force.** The consistent reading is entry into force twenty days after publication and first application 30 January 2027,
  but **the entry-into-force date itself was never stated by any search result**; only the 30 January 2027 first application is safe
  to assert.

(delib-reg-r4)=

### R4. EIOPA — risk-free interest rate term structures, the UFR and the Volatilitätsanpassung

- **Publisher:** EIOPA
- **URL:** https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries)
- **Annotation:** EIOPA **publishes the relevant risk-free interest-rate term structures monthly**, and **§ 83 VAG makes their use
  binding on German undertakings** [R6] — the hook by which a European technical publication becomes German law, and the reason delib
  cites a VAG section for a European curve. Established: technical documentation updated **24 September 2024**, effective **1 January
  2025**; the **UFR for the euro is 3.30 %, applicable from 1 January 2026, unchanged from 2025**; the packages carry the risk-free
  rates, the **volatility adjustment**, the matching-adjustment fundamental spreads and the UFR; and the **reference portfolios behind
  the volatility adjustment were updated on 9 December 2025**. A secondary commentary — not EIOPA — describes the curve as
  interpolated below a **Last Liquid Point of 20 years** and extrapolated to the UFR over a 60-year horizon by Smith–Wilson; that
  rests on one source and is `[unverified]`. **Unverified:** no German volatility-adjustment value, for any date, was established, and
  **no numeric curve point was extracted**.

---

## 2. Prudential — the Versicherungsaufsichtsgesetz

The VAG 2016 is the German transposition of Solvency II and the single statute a German life model is held to. Its architecture
matters for citation: **Teil 1** carries the general prudential rules (valuation, technical provisions, own funds, SCR, MCR,
investments, the public solvency report); **Teil 2 Kapitel 3 Abschnitt 1** the *besondere Vorschriften* for life insurance (§§
138–145); **Teil 3** the *Sicherungsfonds* (§§ 221 ff.); **Teil 4** the supervisory powers including § 314; **Teil 8** the
transitional provisions (§§ 351–353). That layout is why a German product document cites §§ 138–141 for the contract-side mechanics
and §§ 74–88 for the balance sheet, and why the two rarely appear in the same paragraph.

(delib-reg-r5)=

### R5. VAG 2016 — the statute, its architecture and Anlage 1 (die Sparten)

- **Publisher:** Bundesamt für Justiz via `gesetze-im-internet.de`
- **URL:** https://www.gesetze-im-internet.de/vag_2016/BJNR043410015.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (multiple
  queries; **eight independent publishers** carry the same section titles)
- **Annotation:** *Gesetz über die Beaufsichtigung der Versicherungsunternehmen*, in the version in force since **1 January 2016** —
  the Solvency II transposition. **Anlage 1** is the *Einteilung der Risiken nach Sparten*, and it decides which supervisory regime a
  product sits in and which undertakings must join the *Sicherungsfonds* [R12]. The life-relevant *Sparten* established from
  summaries: **19 Leben**, "soweit nicht unter den Nummern 20 bis 24 aufgeführt"; 20 Heirats- und Geburtenversicherung; **21
  Fondsgebundene Lebensversicherung**; 22 Tontinengeschäfte; **23 Kapitalisierungsgeschäfte**. The relevance to delib is direct:
  **eight of the ten products sit in Sparte 19**; `fondsgebundene_rentenversicherung` sits in **Sparte 21** and therefore carries the
  separate *Anlagestock* rule of § 125 VAG [R7]. **Unverified:** the date of promulgation; the title of the Sparte 24 the
  cross-reference implies; **§ 294 VAG as the general statement of supervisory objectives**, which German commentary usually cites but
  no result confirmed.

(delib-reg-r6)=

### R6. VAG §§ 74–110 and § 40 — valuation, best estimate, risk margin, the LTG measures, SCR/MCR and the SFCR

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__88.html (returned); further URLs in `_research/regulatory-actuarial.md`; some
  section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries;
  section titles from four to seven publishers)
- **Annotation:** The block that makes the German *Solvabilitätsübersicht* a different object from the HGB accounts. **§ 74** is the
  market-consistent valuation rule — assets at exchange value and liabilities at transfer or settlement value between knowledgeable,
  willing and independent business partners, with, quoted from a summary, *"eine Anpassung der Bewertung zur Berücksichtigung der
  Bonität des Versicherungsunternehmens findet nicht statt"*, i.e. **no own-credit adjustment**. **§ 76** makes technical provisions
  the **best estimate plus a risk margin**, calculated separately; **§ 77** defines the best estimate and **§ 78** the risk margin;
  **§ 83** obliges undertakings to use the technical information EIOPA publishes — the hook that makes the EIOPA curve binding German
  law [R4]. **§§ 80–82 are the long-term-guarantee measures**: a ***Volatilitätsanpassung*** and a ***Matching-Anpassung***, both on
  approval and **mutually exclusive on the same obligations**; their presence moves a German solvency ratio by hundreds of percentage
  points, which is why **no delib document quotes a ratio without saying whether it is *mit* or *ohne Volatilitätsanpassung und
  Übergangsmaßnahmen*** [R53]. **§ 88 matters most to delib, because it is the legal root of the DeckRV**: **§ 88 Abs. 3** empowers
  the Bundesministerium der Finanzen to fix by *Rechtsverordnung* **Höchstwerte für den Rechnungszins bei Versicherungsverträgen mit
  Zinsgarantie** and the actuarial bases for the *Deckungsrückstellung* — **which is why the *Höchstrechnungszins* is a ministerial
  regulation rather than a supervisory circular, and why the DAV's annual recommendation is a recommendation and not a decision**
  [R14] [R15] [R56]. **§§ 96–110** carry the SCR, § 96 allowing a *Standardformel* or an *internes Modell*; the **MCR** is a separate
  Unterabschnitt. **§ 40** obliges publication of an annual **SFCR**, the practical route to a named insurer's SCR ratio and
  transitional use. **Unverified:** § 74 Abs. 3 and § 78 were not returned; **the MCR section numbers were not established** — §§
  122–124 is commonly cited but § 124 is demonstrably *Anlagegrundsätze* [R7], so **delib cites the MCR by name, not by section**; §
  234g VAG, which surfaced in the same search, is the *Pensionsfonds* provision and is out of scope.

(delib-reg-r7)=

### R7. VAG §§ 124 and 125 — Anlagegrundsätze, Sicherungsvermögen and the Anlagestock

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__124.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries)
- **Annotation:** **§ 124** — since 1 January 2016 a Solvency II undertaking has **no quantitative investment limits**; the
  qualitative standard requires that all assets be invested so that the **security, quality, liquidity and profitability of the
  portfolio as a whole** are ensured, that assets covering technical provisions be invested **appropriately to the nature and
  duration** of the liabilities, and that conflicts of interest resolve in policyholders' favour. **This is why a German life
  insurer's asset mix — and hence the *Kapitalanlageergebnis* that drives the *Überschussbeteiligung* [R18] — is not derivable from a
  rulebook, and why every asset-return assumption in delib is `**[std]**`.** **§ 125** — the ***Sicherungsvermögen*** is the
  ring-fenced pool covering policyholder claims, **administered separately**, held within the Member or Contracting States, with
  **independent sections** formable on approval. **The *Anlagestock*:** a **separate section of the Sicherungsvermögen** must be
  formed for each *Anlageart* where life contracts provide benefits in units of an open fund under § 1 Abs. 4 KAGB, in shares issued
  by an investment company, or **directly linked to a share index or other reference value**. That makes FRV structurally different
  from the general-account products — the unit fund is segregated, the policyholder bears its result, and the MindZV base differs
  [R21] — and supplies the statutory hook under which IDX sits. **The AnlV boundary**, recorded so no delib author misapplies it:
  BaFin *Rundschreiben 11/2017 (VA)* of **12 December 2017** interprets the **Anlageverordnung 2016** and applies to **small insurers
  under §§ 212–217 VAG and to Pensionskassen and Pensionsfonds only** — **not** to the insurers writing the ten delib products.
  **Unverified:** the Absatz numbering of the Anlagestock rule, which rests on one summary; the *Mindestumfang* definition. **The
  AnlV's own content — the *Anlageformen* and the *Mischungs-* und *Streuungsquoten* — was not established and nothing in delib may
  state an AnlV quota.** Whether German index products are written inside an *Anlagestock* or in the general account was **not
  established** and is an open question for IDX.

(delib-reg-r8)=

### R8. VAG § 138 — Prämienkalkulation in der Lebensversicherung; Gleichbehandlung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__138.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries)
- **Annotation:** **Absatz 1** is the pricing-sufficiency rule and the reason a German tariff is priced on **prudent, not
  best-estimate, bases**: premiums must be calculated *auf der Grundlage angemessener versicherungsmathematischer Annahmen* and set
  **high enough** that the undertaking can meet all its obligations and in particular form **adequate *Deckungsrückstellungen*** for
  the individual contracts; the undertaking's own financial position may be taken into account, but **funds not deriving from premium
  payments may not be used systematically and permanently** to support the tariff. That clause forbids permanent cross-subsidy of a
  loss-making tariff out of shareholder funds; it is why the first-order bases carry margins that later emerge as *Überschuss* [R47],
  and it is the statutory root of the *dauernde Erfüllbarkeit* standard that reappears in § 341e HGB [R54] and in BaFin's stated
  supervisory objective [R21]. **Absatz 2** is the equal-treatment rule, quoted by a summary: *"Bei gleichen Voraussetzungen dürfen
  Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden."* Search results establish that the **BGH, on 18 September
  2024, Az. IV ZR 436/22**, tied § 138 Abs. 2 VAG to the contractual entitlement of **§ 153 Abs. 2 VVG** [R24]. Together they mean the
  German *Überschussbeteiligung* is **discretionary in level but not in method**: an insurer may set the declaration, but the split
  between *Abrechnungsverbände* must follow causation. **Unverified:** the Absätze beyond 1 and 2; **whether the
  *verursachungsorientiert* charging rule sits in § 138 or in § 140 is ambiguous across the summaries**, so a delib document
  attributes the causation principle to § 153 Abs.

(delib-reg-r9)=

### R9. VAG § 139 — Überschussbeteiligung and the Sicherungsbedarf test on Bewertungsreserven

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__139.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; nine publishers on the title)
- **Annotation:** **Absatz 1**, quoted by a summary: *"Die für die Überschussbeteiligung der Versicherten bestimmten Beträge sind,
  soweit sie den Versicherten nicht unmittelbar zugeteilt wurden, in der Bilanz in eine Rückstellung für Beitragsrückerstattung
  einzustellen."* This is the structural fact behind the whole German surplus chassis: **surplus earmarked for policyholders either
  goes out immediately as *Direktgutschrift* or into the RfB, and nowhere else.** A delib model of a profit-participating product must
  carry both a direct credit and an RfB stock, or it has not modelled the product. **Absatz 3** is the LVRG's *Bewertungsreserven*
  restriction [R20]: valuation reserves from **festverzinsliche Anlagen und Zinsabsicherungsgeschäfte** count toward policyholders'
  participation **only to the extent that they exceed any *Sicherungsbedarf* aus Versicherungsverträgen mit Zinsgarantien**. **Absatz
  4** defines the test: the *Sicherungsbedarf* is the sum over contracts whose applicable interest rate exceeds the applicable Euro
  swap rate at the time the valuation reserves are determined, a single contract's being its **actuarially calculated interest
  obligation on that reference rate, less the Deckungsrückstellung**; the reference rate and the fifteen-year look-forward are in
  MindZV §§ 11–12 [R18]. **The practical consequence for delib:** for a contract written on a 3.25 % or 4.00 % *Höchstrechnungszins*
  [R15] the *Sicherungsbedarf* has for most of the last decade exceeded the fixed-income valuation reserves outright, so the
  *Bewertungsreserven* component of a maturity payout has often been **zero**. Any delib document that models such a payment must say
  which side of the test it assumes, and the assumption is `**[std]**`. **Unverified:** Absätze 2 and 5 onwards; the predecessor **§
  56a VAG a.F.**, which most German commentary still names, was not confirmed.

(delib-reg-r10)=

### R10. VAG §§ 140 and 145 — Rückstellung für Beitragsrückerstattung and the Verordnungsermächtigung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__140.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; seven publishers on § 140 with two closely agreeing substantive summaries)
- **Annotation:** **§ 140 — the use restriction.** Amounts allocated to the RfB may be used **only** for the *Überschussbeteiligung*
  of the insured, **including the participation in Bewertungsreserven prescribed by § 153 VVG** [R24]. That is a hard ring fence: RfB
  money cannot be released to shareholders. **The two escape hatches**, both requiring the supervisor's consent and both confined to
  the part of the RfB **not** attributable to already-declared profit shares: the RfB may be drawn on in the policyholders' interest
  (1) to offset **unforeseen losses from profit-participating contracts arising from general changes in circumstances**, and (2) to
  **increase the Deckungsrückstellung where the calculation bases must be adjusted because of an unforeseen and not merely temporary
  change in circumstances**. **Escape hatch (2) is the statutory route by which the German industry financed the *Zinszusatzreserve*
  out of the free RfB during the low-rate decade** [R17], and it is why a German life insurer's RfB stock and its ZZR stock move
  against each other. The supervisor may require a **Zuführungsplan** where the allocation falls short of the MindZV minimum [R18] and
  a **Verteilungsplan** where the *ungebundener* RfB exceeds the RfBV cap [R19]. **§ 140 Abs. 1 Satz 2** permits a **kollektiver
  Teil** of the RfB, assigned to all profit-participating contracts collectively rather than to a *Teilbestand* [R19]. **§ 145
  *Verordnungsermächtigung*** empowers the Bundesministerium der Finanzen to regulate the *Zuführung zur Rückstellung für
  Beitragsrückerstattung* and is therefore the statutory root of the **MindZV** [R18] and, with § 140 Abs. 1 Satz 2, of the **RfBV**
  [R19]. Recording the chain **§ 145 VAG → MindZV** correctly matters because delib product documents cite the MindZV percentages
  constantly. **Unverified:** the ***gebundene*** / ***freie*** RfB distinction — the vocabulary every German market commentary uses —
  is **not in the statutory text any search returned**; it emerges from § 28 RechVersV [R54] together with the RfBV's *ungebundene
  RfB* [R19], and delib defines the terms from those.

(delib-reg-r11)=

### R11. VAG §§ 141–143 — Verantwortlicher Aktuar, Treuhänder, Anzeigepflichten, and the deregulation of 29 July 1994

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__142.html (returned); further URLs in `_research/regulatory-actuarial.md`;
  some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries;
  seven publishers on the titles)
- **Annotation:** **§ 141 *Verantwortlicher Aktuar*.** Every life insurer must appoint one, *zuverlässig und fachlich geeignet*,
  **sufficient experience regularly assumed at three years' actuarial activity**, appointed and dismissed by the *Aufsichtsrat*. The
  duties that matter: an *Erläuterungsbericht zur versicherungsmathematischen Bestätigung* and an *Angemessenheitsbericht* go to the
  supervisor; and the actuary **makes a proposal on the Überschussbeteiligung**, which the undertaking must **submit to the
  supervisor** and from which it may depart only on **written or electronic notification with reasons**. **That last item is the
  governance reason German declared rates cluster as tightly as the market data show** [R53]. **§ 142** — for life contracts concluded
  after 28 July 1994 where premiums can be changed for existing contracts, changes take effect only with an **unabhängiger
  Treuhänder**'s consent; it is the supervisory counterpart of § 163 VVG [R27]. **§ 143** is the German equivalent of a tariff filing:
  after authorisation the undertaking must **unverzüglich** notify the supervisor of the **Grundsätze für die Berechnung der Prämien
  und der Deckungsrückstellungen**, including the *verwendeten Rechnungsgrundlagen, mathematischen Formeln, kalkulatorischen
  Herleitungen und statistischen Nachweise*, and again whenever they change. **This is why a German tariff's first-order bases exist
  as a documented, supervisor-visible object — and equally why they are not public, which is the structural reason delib's decrement
  tables must be `**[std]**` proxies** [R47]. **The 29 July 1994 boundary.** German life business splits into ***Altbestand*** and
  ***Neubestand***. Until deregulation the AVB were part of a *genehmigungspflichtiger Geschäftsplan*; in the *Altbestand* that plan
  **continues to apply and changes still require approval**, while in the *Neubestand* contract design and premium calculation are
  **free within the statutory frame**. At deregulation **the entire RfB accumulated to 1994 was allocated exclusively to the
  Altbestand**, which is why the MindZV computes the minimum **getrennt für Alt- und Neubestand** [R18].

(delib-reg-r12)=

### R12. VAG §§ 221–236 and § 314, with Protektor — the Sicherungsfonds and the supervisor's crisis powers

- **Publisher:** Bundesamt für Justiz for the VAG and the SichLVV/SichLVFinV
- **URL:** https://www.gesetze-im-internet.de/vag_2016/__222.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (six queries)
- **Annotation:** The outer boundary of every guarantee in the library. **§ 221 *Pflichtmitgliedschaft*:** undertakings authorised to
  write **Sparten 19 to 23 of Anlage 1** [R5] **must belong to a Sicherungsfonds**; **Pensions- und Sterbekassen are excepted** —
  exactly the vehicles delib puts out of scope. **§ 222 — the five-per-cent haircut:** where the fund's *Sicherungsvermögen* plus
  collectable *Sonderbeiträge* is insufficient to secure continuation of the contracts, **the supervisor may reduce the obligations
  under the life contracts by at most 5 per cent of the contractually guaranteed benefits**. **§ 226 *Finanzierung*:** the annual
  contributions sum to **0.2 per mille of the members' versicherungstechnische Netto-Rückstellungen** measured **according to §§ 341e
  to 341h HGB** [R54] — the statutory accounts, not the Solvency II balance sheet. **Protektor Lebensversicherungs-AG** carries the
  statutory fund's tasks, transferred by the SichLVV, and **the Mannheimer case is the only time it has been used**: a commitment
  declaration in **June 2003** for the portfolio of *Mannheimer Lebensversicherungs-AG*, negotiations concluded **18 September 2003**
  with economic effect from 1 July 2003, and **BaFin's approval of the Bestandsübertragungsvertrag on 1 October 2003**; the statutory
  fund itself was created by VAG amendments of **15 December 2004**. For delib, Protektor is the answer to "what happens if the
  insurer fails" in every product document, and the precedent is **a portfolio transferred and continued, not a payout**. **§ 314** is
  the crisis power and the single most important qualification on the word "guarantee". **Abs. 1:** where an undertaking is
  **permanently unable to meet its obligations** the supervisor may **temporarily prohibit all kinds of payments**, the summary naming
  *Versicherungsleistungen*, *Gewinnverteilungen* and, for life insurance, **den Rückkauf oder die Beleihung des
  Versicherungsscheins** — so **a delib document modelling a surrender option says the option is suspendable by the supervisor**.
  **Abs. 2:** the supervisor may **reduce the obligations of a life insurer in accordance with its Vermögenslage**,
  *Deckungsrückstellungen* first and *Versicherungssummen* recomputed, **while the duty to keep paying premiums is unaffected**, and
  **may proceed unequally where special circumstances justify it**. German life guarantees therefore sit under **two distinct
  write-down powers**: a fund-level 5 % cap and an uncapped, asset-position-driven reduction.

(delib-reg-r13)=

### R13. VAG §§ 351–353 — the Solvency II transitional measures and the 2024 recalculation

- **Publisher:** Bundesamt für Justiz
- **URL:** https://dejure.org/gesetze/VAG/352.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries;
  the three section titles from four publishers)
- **Annotation:** **§ 352** is the *Rückstellungstransitional*: a deduction that temporarily reduces technical provisions on the
  Solvency II balance sheet, and thereby raises eligible own funds, for business written before the regime began. **The maximum
  deductible portion falls linearly from 100 per cent in the year beginning 2016 to 0 per cent on 1 January 2032** — a sixteen-year
  run-off. **§ 351** is the parallel transitional on the risk-free rates. **§ 353:** an undertaking that would not meet the SCR
  without either transitional must **within two months** submit a plan restoring compliance by the end of the transitional period.
  **The 2024 recalculation is the single most consequential supervisory event in the German life market since the LVRG, and it is well
  corroborated.** In **Q2 2024** BaFin ordered life insurers to **recalculate** the *Rückstellungstransitional*, on the ground that
  the rate rise which ended the low-rate phase from 2022 had made the existing deduction amounts inappropriate: higher rates sharply
  reduced Solvency II technical provisions and hence raised own funds, while the SCR also fell. A BaFin spokesman is quoted to the
  effect that **for most companies the Rückstellungstransitional takes the value 0 after recalculation**; the effect on published
  ratios is in [R53]. For delib the discipline is simple: **no delib model implements a transitional**, and any German solvency ratio
  quoted in a delib document must state whether it is before or after the 2024 recalculation, because the two are not comparable.
  **Unverified:** **the legal instrument by which BaFin "ordered" the recalculation** — a general administrative act, individual
  orders, or an interpretation of § 352 itself — was not established, nor was the exact wording of the § 352 linear formula read.

---

## 3. Prudential — reserving, the Höchstrechnungszins and the Zinszusatzreserve

The DeckRV is made under § 88 Abs. 3 VAG [R6] and fixes the *Rechnungsgrundlagen* of the German statutory *Deckungsrückstellung* — the
HGB reserve of § 341f HGB [R54], **not** the Solvency II best estimate. This distinction is the axis of the whole German reserving
picture and every delib document keeps it: an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
*Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all run on the **HGB** side.

(delib-reg-r14)=

### R14. DeckRV — the reserving regulation and its § 2, the Höchstrechnungszins

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/BJNR076700016.html (returned); further URLs in
  `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (five queries;
  the title and 18 April 2016 date from three independent publishers)
- **Annotation:** *Verordnung über Rechnungsgrundlagen für die Deckungsrückstellungen*, of **18 April 2016**. Three sections matter:
  **§ 2** (the *Höchstrechnungszins*), **§ 4** (*Höchstzillmersätze*, [R16]) and **§ 5 Abs. 3** (the *Referenzzins* behind the
  *Zinszusatzreserve*, [R17]). **§ 2 fixes the maximum interest rate at which a German life insurer may discount its statutory
  *Deckungsrückstellung* for contracts carrying an interest guarantee**, and therefore — through § 138 Abs. 1 VAG's requirement that
  premiums be adequate to fund that reserve [R8] — the maximum rate at which a new tariff may be priced. It is the *Garantiezins* of
  market language, but the two are not legally identical: § 2 caps the **reserving** rate, and the rate a policy guarantees is a
  tariff decision that may be lower. BaFin's FAQ title states the operative change: *"Zum 1. Januar 2025 wird der Höchstrechnungszins
  in § 2 der Deckungsrückstellungsverordnung (DeckRV) von 0,25 Prozent auf 1,0 Prozent angehoben"* — quoted from the search result,
  not from BaFin. Two structural facts a delib document needs: the rate applies **at the time of contract conclusion** and then
  **stays with the contract for its whole term**, which is why the German in-force book is a stack of cohorts [R15] and why the ZZR
  exists at all. **Unverified:** **the wording of § 2 was not read**; whether § 2 caps the reserving rate only or the guaranteed rate
  directly is inference from § 88 Abs.

(delib-reg-r15)=

### R15. The Höchstrechnungszins rate history and the Sechste Verordnung of 19 July 2024

- **Publisher:** `recht.bund.de` for the BGBl
- **URL:** https://www.recht.bund.de/bgbl/1/2024/250/VO.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; the BGBl citation from two independent sources)
- **Annotation:** The rate history is the most-used table in the library, because a German in-force book is a stack of cohorts and
  **every delib model point carries its cohort's rate rather than today's**: **3.50 %** 1987 – 06/1994; **4.00 %** 07/1994 – 06/2000;
  **3.25 %** 07/2000 – 2003; **2.75 %** 2004 – 2006; **2.25 %** 2007 – 2011; **1.75 %** 2012 – 2014; **1.25 %** 2015 – 2016; **0.90
  %** 2017 – 2021; **0.25 %** 2022 – 2024; **1.00 %** from 2025. Two facts are separately corroborated: the **1994 move was an
  increase**, from 3.50 % to 4.00 %, the summary stating the rate "only increased in 1994 … and has only been reduced since then"; and
  the **2025 move to 1.00 % is the first increase in about thirty years**. **The instrument:** the Bundesministerium der Finanzen
  amended the DeckRV by the **Sechste Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz of 19 July
  2024**, published as **BGBl. 2024 I Nr. 250**, setting the rate at **1.00 % with effect from 1 January 2025**; a *Referentenentwurf
  of 27 June 2024* is on the BMF site, and the same regulation updated the absolute floors for the *Mindestkapitalanforderung*. For
  delib the operative number for a new-business tariff written today is **1.00 %**, and all ten products' `**[std]**` guaranteed rates
  are anchored to this table. **Unverified:** the precise within-year effective dates for the 2000, 2004, 2007, 2012, 2015, 2017 and
  2022 steps beyond the half-year granularity shown; the MCR absolute floors, for which no euro figure was returned.

(delib-reg-r16)=

### R16. DeckRV § 4 — Höchstzillmersätze

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/__4.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries)
- **Annotation:** *Zillmerung* is the mechanism by which an insurer offsets a contract's one-off acquisition costs against its first
  premiums, and it is why a German endowment or annuity has a very low surrender value in its early years. **§ 4 DeckRV caps it: the
  *Zillmersatz* may not exceed 25 per mille (25 ‰, i.e. 2.5 %) of the *Beitragssumme***, the sum of all premiums payable under the
  contract. The claim for reimbursement may be covered individually, from the highest possible premium components up to the height of
  the *Zillmersatz*, **from the inception of the insurance**; and **the rate an undertaking uses at conclusion applies for the whole
  term**, so a pre-2015 contract keeps its 40 ‰ basis. **The 2015 cut:** from **40 ‰ to 25 ‰ with effect from 1 January 2015** by the
  LVRG [R20]; summaries state the pre-reform figure both as "40 Promille" and as "bis zu 4 Prozent", which are the same number. For
  delib this parameter sets the shape of the guaranteed surrender-value curve in the first years of every regular-premium product, and
  it **interacts with § 169 VVG's independent five-year-spread floor** [R28]: the DeckRV governs what the insurer may **reserve**, §
  169 VVG what it must **pay**, and a model carrying a zillmerised reserve applies both separately, the tighter binding. **Unverified
  — and here there is a real conflict.** One rendering states the cap applies to premiums paid that are not used for insurance
  coverage and administration cost coverage; a second states that in the *Barwert der Prämien* no more than 2.5 % of premium
  components above the current value of the obligation may be applied; a third states plainly "25 ‰ der Beitragssumme".

(delib-reg-r17)=

### R17. DeckRV § 5 Abs. 3 — the Referenzzins, the Zinszusatzreserve and the Korridormethode

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/deckrv_2016/__5.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (five queries;
  the corridor reform date and mechanism from four independent sources)
- **Annotation:** The ***Zinszusatzreserve*** is the additional German statutory reserve arising when the discount rate applicable
  under § 5 DeckRV must be reduced below a contract's tariff rate, producing a **higher *Deckungsrückstellung* than the tariff rate
  alone would give**. It is an **HGB** reserve, financed out of the result and, under § 140 VAG's second escape hatch, out of the free
  RfB [R10], and it exists in no other jurisdiction in this repository. **How the *Referenzzins* is built:** from the **month-end
  zero-coupon Euro interest-rate swap rates at ten years published by the Deutsche Bundesbank under § 7 der
  Rückstellungsabzinsungsverordnung** — for each of the **nine preceding calendar years** the annual mean of month-end levels rounded
  up to two decimals, and for the current year the mean of the first nine months, with **2009 to 2013 fixed by statute at 3.81, 3.13,
  3.15, 2.14 and 1.96 per cent** — the reference rate being the **arithmetic mean over the ten-year period**. **The Korridormethode**,
  newly regulated with effect from **23 October 2018**: the current year's rate must lie **within a corridor around the previous
  year's**, limiting the annual change in both directions; the reform touched **only the reference rate**, not the ZZR calculation.
  **The 2018 counterfactual, corroborated twice:** under the old method the rate would have fallen from 2.21 % (2017) to about 1.9 %;
  under the corridor it fell only to **2.10 %**, worth **about ten billion euros of relief industry-wide for 2018**. The rate was
  **1.57 % at 31 December 2022 and 1.57 % in 2025**, reportedly unchanged since 2021 — pinned flat for five years while market swap
  rates moved sharply. **The ZZR in quantum**, all of it trade press and **never a supervisory source**: about **€84 bn at the 2024
  balance-sheet date**, from a **€96 bn peak at end-2021**; **2024 was the first year since introduction in which insurers had to add
  nothing at all**, with about €5 bn flowing back industry-wide and releases among the fifty largest summing to about €3.4 bn; a
  further €4 bn for 2025. **The released funds reach policyholders through a higher *Überschussbeteiligung***, the mechanical link to
  the declared rates in [R53].

---

## 4. Prudential — the surplus regulations, the LVRG and the supervisor

(delib-reg-r18)=

### R18. MindZV — the minimum allocation to the RfB, and §§ 11–13

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html (returned); further URLs in
  `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries)
- **Annotation:** *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*, of 18 April 2016, made under § 145
  VAG [R10] — the arithmetic floor under the German *Überschussbeteiligung*. **The three result sources and their minimum shares.**
  **§ 6 *Kapitalanlageergebnis* — 90 %**: the minimum allocation is **90 per cent of the Kapitalerträge to be credited under § 3 Abs.
  1, less the Rechnungszinsen**. **The subtraction of the *Rechnungszinsen* is the crucial detail: the guarantee is funded first, and
  only the excess is shared 90/10.** **§ 7 *Risikoergebnis* — 90 %**, raised from 75 % by the LVRG with effect from **7 August 2014**
  [R20]. **§ 8 *Übriges Ergebnis* — 50 %**, the cost result. **§ 4 — assembly:** from the sum the ***Direktgutschrift*** attributable
  to profit-participating contracts is **deducted**; **Alt- and Neubestand are treated separately throughout** [R11]; and **a
  mathematically negative minimum allocation is replaced by zero**. Those two rules make the MindZV a **minimum transfer to the RfB,
  not a minimum payout**. **§§ 11–13 — the Sicherungsbedarf machinery** behind § 139 Abs. 3/4 VAG [R9]. **§ 11:** the reference rate
  is the ten-year zero-coupon Euro swap rate published by the Bundesbank, **at the end of the month preceding the date on which the
  Bewertungsreserven are determined** — **note the difference from the ZZR rate** [R17], which is a **ten-year average** damped by the
  corridor where this is a **single month-end spot**: different numbers from the same Bundesbank series, and **confusing them is one
  of the standard errors in describing a German life balance sheet**. **§ 12:** that rate is compared with **the highest Rechnungszins
  applicable to the contract over the next fifteen years**, and where it is lower the contract generates a *Sicherungsbedarf*; the
  fifteen-year window is why the test bites hardest on annuity business. **Why this entry is the centre of the library:** six of the
  ten products are profit-participating general-account contracts whose credited return is the guarantee plus a discretionary share of
  these three results, so any delib model of the surplus chassis represents at least the three result sources, the 90/90/50 floor, the
  direct-credit-versus-RfB split, and the fact that the floor binds on the **HGB** accounts.

(delib-reg-r19)=

### R19. RfBV — the collective part of the Rückstellung für Beitragsrückerstattung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/rfbv/BJNR030000015.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries)
- **Annotation:** A *Rechtsverordnung* at **BGBl. I 2015 S. 300** implementing § 140 Abs. 1 Satz 2 VAG [R10], applying to life
  insurers except *Sterbekassen* and *regulierte Pensionskassen*. **§ 2 — the cap on the *ungebundene* RfB:** on establishing a
  *kollektiver Teil* the undertaking must set an ***Obergrenze*** for the *ungebundene* RfB of the *Teilbestände*, expressed as a
  percentage; the percentage is **at least 100**, is **identical for all Teilbestände**, and **may be changed from the prior year only
  with the supervisor's consent**; where a *Teilbestand*'s *ungebundene* RfB exceeds the ceiling and no *Rückführungen* take place at
  the balance-sheet date, **the excess is transferred to the kollektiver Teil**. **§ 3** requires an *Obergrenze* for the collective
  part itself. **Why it exists:** the collective part lets an insurer hold surplus committed to policyholders as a class but not yet
  attributed to any *Teilbestand*, which is what makes cross-cohort smoothing legally possible without breaching the § 138 Abs. 2 VAG
  equal-treatment rule [R8]; BaFin's interpretive decision of **19 April 2011** governs how the MindZV floor interacts with it [R21].
  **Vocabulary for delib:** the statutory term is *ungebundene* RfB; German market writing says *freie RfB* for the same thing and
  *gebundene RfB* for the part already committed to declared shares and to the *Schlussüberschussanteilfonds* of § 28 RechVersV [R54].
  **Unverified:** **the percentage base in § 3 was not established**, and the summaries **conflate §§ 2 and 3** in a way this page
  does not resolve; § 1 and any further sections were not retrieved; **whether the German market actually uses the collective part,
  and how large it is, was not established.** Load-bearing for the surplus chassis of KLV, RV, BAS, RIE, IDX and SOF.

(delib-reg-r20)=

### R20. LVRG 2014 — the Lebensversicherungsreformgesetz

- **Publisher:** Bundesgesetzblatt / `dejure.org` for the citation
- **URL:** https://dejure.org/BGBl/2014/BGBl._I_S._1330 (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries)
- **Annotation:** *Gesetz zur Absicherung stabiler und fairer Leistungen für Lebensversicherte*, **BGBl. I 2014 S. 1330**, of **1
  August 2014**, on **BT-Drs. 18/1772** of 18 June 2014 — the reform that reshaped the German *Überschussbeteiligung* for the low-rate
  era. Three of its changes are load-bearing. **(1) Bewertungsreserven restricted:** the distribution restriction applies **only to
  valuation reserves from festverzinsliche Wertpapiere**, and participation by departing policyholders is limited where an insurer's
  provisions are, at prevailing low rates, insufficient to fund the guarantees given to remaining policyholders — the
  *Sicherungsbedarf* test now in § 139 Abs. 3/4 VAG [R9] and MindZV §§ 11–12 [R18]. **(2) *Höchstzillmersatz* cut from 40 ‰ to 25 ‰**
  of the *Beitragssumme*, effective **1 January 2015** [R16]. **(3) *Risikoüberschuss* share raised from 75 % to 90 %**, effective **7
  August 2014**, now § 7 MindZV [R18] — the single change that most affects delib's biometric products, since a German term, BU or
  Pflege tariff's surplus is predominantly a risk surplus. Alongside them, **distributions to shareholders may be prohibited** where
  needed to secure the guaranteed benefits. The constitutionality of the LVRG's insertion into § 153 Abs. 3 Satz 3 VVG was litigated
  and upheld [R36]. **Unverified:** the LVRG amended the **old** VAG (§ 56a a.F. and others) and **the mapping from those sections
  onto the 2016 VAG was not established**, so delib cites the current sections and describes the LVRG as the reform that introduced
  the rules, not as the current legal source; whether the LVRG also introduced a commission cap (*Provisionsdeckel*) was **not
  established and is not asserted**.

(delib-reg-r21)=

### R21. BaFin — the FinDAG, the MaGo and the Auslegungsentscheidungen

- **Publisher:** Bundesamt für Justiz for the FinDAG
- **URL:** https://www.gesetze-im-internet.de/findag/BJNR131010002.html (returned); further URLs in
  `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries)
- **Annotation:** **The institution.** BaFin was created in **2002** by the *Finanzdienstleistungsaufsichtsgesetz of 22 May 2002*,
  merging the three predecessor *Bundesaufsichtsämter* into a single *Allfinanzaufsicht*; the merger was organisational and **created
  no new competences**. BaFin sits under the *Rechts- und Fachaufsicht* of the Bundesministerium der Finanzen (§ 2 FinDAG) and
  supervises under the KWG, the VAG and the WpHG, its objective being to ensure the **permanent fulfilment capability of insurance
  contracts** — the *dauernde Erfüllbarkeit* standard that also appears in § 341e HGB [R54] and § 138 Abs. 1 VAG [R8]. There is **no
  second national insurance supervisor**: Germany runs conduct and prudential supervision inside one authority. **The MaGo.**
  *Rundschreiben 2/2017 (VA) — Mindestanforderungen an die Geschäftsorganisation von Versicherungsunternehmen*, **published 25 January
  2017, in force 1 February 2017**, interprets the business-organisation provisions of the VAG and of Delegated Regulation (EU)
  2015/35 and **binds BaFin's own application of them**; a **revised version was published 14 July 2025**. For delib the MaGo is why
  the ***versicherungsmathematische Funktion*** exists alongside the § 141 VAG *Verantwortlicher Aktuar* [R11] — **two distinct
  actuarial roles, which delib does not conflate.** **The Auslegungsentscheidungen** are BaFin's published statements of how it will
  apply a provision: not law, but binding on BaFin's own practice and carrying much of the operative detail the regulations leave
  open. Established, each from one or two sentences: (1) ***Wechselwirkungen zwischen Überschussbeteiligung und Neugeschäft*** (4
  December 2015) — German life insurance is characterised by **collective mechanisms**, so new business can affect the existing
  portfolio's future *Überschussbeteiligung*. (2) ***Ausweis der Beteiligung an den Bewertungsreserven in der Standmitteilung*** (10
  June 2016) — the annual statement must disclose the **full** allocation, a guaranteed *Sockelbeteiligung* alone **not being
  sufficient** for § 155 Satz 1 VVG [R25]. (3) ***Mindestzuführung in der fondsgebundenen Lebensversicherung*** (22 December 2009) —
  **load-bearing for FRV**, whose MindZV base is not the general account's. (4) ***Zusammenwirken von Mindestzuführung zur RfB und
  Teilkollektivierung*** (19 April 2011) [R19]. (5) ***Auswirkung von passiver Rückversicherung auf die Angemessenheit der Zuführung
  zur RfB***. (6) ***Anforderungen an Kapitalmarktmodelle*** (11 November 2016) — calibration must be consistent with the risk-free
  curve of **Art. 77(2)** of Directive 2009/138/EC [R1]. (7) ***Latente Steuern auf versicherungstechnische Rückstellungen*** (22
  February 2016). (8) ***Projektion des Referenzzinses gemäß § 5 Abs. 3 DeckRV*** [R17].

---

## 5. Contract law — the Versicherungsvertragsgesetz

German life contract law is a single statute whose **Kapitel 5 (§§ 150–171) is *halbzwingend***: §§ 152 Abs. 1 and 2, 153 to 155, 157,
158, 161 and 163 to 170 may not be varied to the policyholder's detriment (§ 171 VVG). That one sentence is why a delib model may
treat the surrender-value floor, the paid-up right, the suicide clause and the profit-participation entitlement as **contractual facts
rather than insurer choices**, and why the discretionary layer sits only where the statute leaves room. This block carries the
strongest search corroboration in the library: roughly 45 German-language queries, with six to ten independent publishers returning
each of §§ 8, 152, 153, 154, 155, 161, 163, 165, 168, 169, 171 and 172.

(delib-reg-r22)=

### R22. VVG 2008 — the statute, Kapitel 5 and § 171 (halbzwingende Vorschriften)

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/BJNR263110007.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (the index
  page plus every single-paragraph query in this block)
- **Annotation:** The VVG 2008, of **23 November 2007**, replaced the VVG of 1908 with effect from 1 January 2008. **Teil 1** carries
  the general provisions (§§ 1–73: advice and information §§ 6, 7, 7a–7d; withdrawal § 8; pre-contractual disclosure §§ 19–22; premium
  default §§ 33, 37, 38); **Teil 2** the branches, of which **Kapitel 5 Lebensversicherung** runs §§ 150–171 and **Kapitel 6
  Berufsunfähigkeitsversicherung** §§ 172–177; **Teil 3** the final provisions including § 214. A single statute therefore supplies
  the death-cover, savings-contract and disability-income rules, and **§ 176 imports §§ 150–170 into the BU chapter *entsprechend***
  [R29]. **§ 171**, quoted by a summary: *"Von § 152 Abs. 1 und 2 und den §§ 153 bis 155, 157, 158, 161 und 163 bis 170 kann nicht zum
  Nachteil des Versicherungsnehmers … abgewichen werden."* A *halbzwingende* provision may be varied in the policyholder's favour; a
  detrimental variation is not void as such, but **the insurer may not rely on it**. Note what is **not** listed: §§ 150, 156, 159,
  160, 162 — so beneficiary designation and the consent rule are freely variable. **§ 170 *Eintrittsrecht*:** on attachment or
  insolvency a named beneficiary may, with the policyholder's consent, step into the contract, satisfying creditors **up to the amount
  the policyholder could have demanded on termination**, within **one month**. **Two chapters have no VVG home at all, and this
  matters for delib:** there is no statutory chapter for *Pflegerentenversicherung* (reached, if at all, through the contested § 177
  Abs. 1 — [R29], [R36]) and none for *indexgebundene* Rentenversicherung, which in law is a *fondsgebundene* or *klassische* contract
  with the index participation living entirely inside § 153 [R24]. **Unverified:** no consolidated-version date and no "last amended
  by" line; the **VVG a.F.** numbering (§ 5a, § 176 Abs. 3/4) was confirmed only through case-law summaries [R36]; **§ 156 VVG was
  never searched**. Load-bearing for all ten.

(delib-reg-r23)=

### R23. VVG §§ 8 and 152 — the 14-day and 30-day Widerrufsrechte

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__8.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (five queries)
- **Annotation:** **§ 8** — the policyholder may withdraw within **14 days**, in *Textform*, without reasons, and **timely dispatch
  suffices**; the period does **not begin** before the policyholder has received, in Textform, the *Versicherungsschein*, the contract
  terms including the AVB, and the VVG-InfoV information [R31], with a general cut-off a summary reported as *"zwölf Monate und 14
  Tage nach dem Vertragsschluss"*. **§ 152 makes three deviations for life insurance.** **Abs. 1:** the period is **30 days**, and the
  right **lapses at the latest 24 months and 30 days after conclusion**. **Abs. 2:** where withdrawal is effective the insurer owes
  the ***Rückkaufswert einschließlich der Überschussanteile nach § 169***. **Abs. 3:** the single or first premium falls due
  **immediately after the expiry of 30 days from receipt of the Versicherungsschein**. This is the most model-relevant conduct rule in
  the German life chapter: **a withdrawal exercised after cover has begun is settled at the surrender value, not at premiums-paid**,
  so the § 169 floor [R28] reaches into the withdrawal window. For delib it fixes a **first-duration decrement legally distinct from
  lapse**, and a model that lumps the two into one lapse rate must say so. **Unverified:** the Absatz structure of § 8 is partly
  contradictory across summaries, so **the Absatz-to-rule mapping inside § 8 is `[unverified]`** while the substantive rules are
  corroborated; **§ 9 VVG (Rückabwicklung) was never searched** and the *Fernabsatz* interaction is not established.

(delib-reg-r24)=

### R24. VVG § 153 — Überschussbeteiligung and the hälftige Beteiligung an den Bewertungsreserven

- **Publisher:** Bundesamt für Justiz
- **URL:** https://dejure.org/gesetze/VVG/153.html (returned); further URLs in `_research/regulatory-actuarial.md`; some section pages
  only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries,
  nine and eight hosts, with the BGH press release [R36] and a general-reference article corroborating the Abs. 3 mechanics
  independently)
- **Annotation:** The article the whole KLV / RV / IDX chassis hangs on, and the German counterpart to the French *participation aux
  bénéfices* — but **an individual contractual entitlement with a statutory default, not a collective minimum computed from a
  regulated account**. **(1) The entitlement.** The policyholder has a **right** to participate in the *Überschuss* and in the
  *Bewertungsreserven* **unless participation is excluded by express agreement**, and such an exclusion **can only be made for the
  whole of the profit participation** — there is no partial opt-out. **(2) The method.** The insurer must operate the participation by
  a ***verursachungsorientiertes Verfahren***, or by *"andere vergleichbare angemessene Verteilungsgrundsätze"*. The statute names the
  principle and **does not prescribe the algorithm**, which is precisely why the three surplus sources (*Zinsüberschuss*,
  *Risikoüberschuss*, *Kostenüberschuss*) and their declared rates are insurer-discretionary and **every level in delib is `**[std]**`
  unless a *Tarifblatt* supplies it**; the BGH tied this Absatz to § 138 Abs. 2 VAG in **IV ZR 436/22 of 18 September 2024** [R8].
  **(3) Bewertungsreserven.** The insurer must **recompute them annually** and allocate them by a cause-oriented method; **on
  termination of the contract, half of the amount then determined is allocated and paid to the policyholder**. **(4) The LVRG
  override.** § 153 Abs. 3 Satz 3, in the version in force 7 August 2014 [R20], preserves the supervisory rules securing permanent
  fulfilment, with the effect that *Bewertungsreserven* from fixed-interest securities and hedging instruments count toward the
  policyholder's share **only to the extent that they exceed a *Sicherungsbedarf*** [R9] [R18]; in a low-rate environment this reduced
  the payable half to zero for many portfolios, and the BGH held the rule constitutional [R36]. **For delib:** the
  *Bewertungsreserven* leg is path- and balance-sheet-dependent in a way a gross liability cash flow model cannot reproduce, so the
  reference implementations model the declared *laufende Überschussbeteiligung* and the *Schlussüberschussanteil* explicitly and treat
  the *Bewertungsreserven* share as an explicitly excluded component, saying so. **Unverified:** the Absatz/Satz numbering of the
  entitlement and the method was inferred from the ordering in the summaries and from the BGH's citation of "§ 153 Abs.

(delib-reg-r25)=

### R25. VVG §§ 154 and 155 — Modellrechnung and Standmitteilung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__154.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; eight and nine hosts)
- **Annotation:** **§ 154 *Modellrechnung*.** Where the insurer makes **quantified statements about possible benefits beyond the
  contractually guaranteed benefits**, it must give the policyholder a *Modellrechnung* showing the possible *Ablaufleistung* computed
  **on the calculation bases used for the premium calculation** at **three different interest rates**; the duty does not apply to
  *Risikoversicherungen*. The three rates are set by **§ 2 Abs. 3 VVG-InfoV**, quoted by a summary as *"a) Der
  Höchstrechnungszinssatz, multipliziert mit 1,67; b) der Zinssatz nach a) zuzüglich eines Prozentpunkts und c) der Zinssatz nach a)
  abzüglich eines Prozentpunkts."* **The arithmetic consequence for delib is sharp:** at a *Höchstrechnungszins* of **1.00 %** [R15]
  the statutory triple is **1.67 % / 2.67 % / 0.67 %**, so a `product-spec.md` reproducing a published *Modellrechnung* reproduces
  that triple, and a technical note projecting an illustrative surplus scenario either uses those rates or says explicitly that it
  does not and why. **§ 155 *Standmitteilung*.** For profit-participating insurance the insurer must inform the policyholder
  **annually in Textform** about the current status of their claims including profit participation, and must **disclose to what extent
  that profit participation is guaranteed**; a second limb requires it to report **deviations of the actual development from any
  statements it made about the future development**, making the *Modellrechnung* a benchmark it keeps reporting against. For delib
  this is not a cash flow: it is the reason **published Standmitteilung specimens are a legitimate `[S#]` source class** for declared
  surplus rates and for the guaranteed/non-guaranteed split. **Unverified:** the § 124 Abs. 2 Satz 2 VAG carve-out (one summary only);
  the *Satz* numbering within § 155 except "§ 155 Satz 1"; the instrument of the *Jährliche Unterrichtung* → *Standmitteilung* rename.

(delib-reg-r26)=

### R26. VVG §§ 150, 159, 160, 161 and 162 — Einwilligung, Bezugsberechtigung, Selbsttötung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__159.html (returned); some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries;
  nine or ten hosts on §§ 150, 159, 161 and 162; **zero** on § 160)
- **Annotation:** **§ 150** — where a policy is taken out **on the death of another person** and the benefit **exceeds the amount of
  ordinary funeral costs** (*gewöhnliche Beerdigungskosten*), that person's **written consent** is required for validity; where a
  parent insures a **minor child**, consent is required only if the insurer is also to pay on death **before age seven** above that
  threshold. For delib this is an **issue-rule constraint** rather than a cash flow, and the funeral-cost boundary is what makes
  *Sterbegeldversicherung* a distinct product in German law rather than a small RLV — which is why delib excludes it. **§ 159
  *Bezugsberechtigung*** — the policyholder may designate and substitute a beneficiary **without the insurer's consent**; a
  **widerruflich** designated third party acquires the right **only on occurrence of the insured event**, an **unwiderruflich**
  designated one **already on designation**, so **an irrevocable designation removes the unilateral disposal and a model point
  carrying one should not carry a surrender assumption**. **§ 161 *Selbsttötung*** — in *Todesfallversicherung* the insurer is **not
  liable if the insured person intentionally took their own life within three years of conclusion**, unless the act was committed in a
  state excluding free determination of the will; the period may be **extended** by agreement, and where the insurer is not liable it
  must nevertheless **pay the Rückkaufswert einschließlich der Überschussanteile nach § 169** [R28]. **§ 162** — no liability where
  the policyholder intentionally and unlawfully brought about the death of the insured. **Model consequence for RLV and the death
  cover inside KLV:** the first three policy years carry a benefit that is the **surrender value rather than the sum assured for the
  suicide sub-cause of death** — a *duration-dependent benefit definition*, not a rate adjustment, and therefore a listed modeling
  pitfall even in a model that does not split the death decrement by cause. **Unverified:** **no search result supplied a figure or
  case law fixing *gewöhnliche Beerdigungskosten***, so any euro threshold in a delib document is `**[std]**`; the age-seven rule
  rests on one summary; **§ 160 VVG was never returned by any search** and its default interpretation rules for several beneficiaries
  and for an "Erben" designation are **not established**.

(delib-reg-r27)=

### R27. VVG § 163 — Prämien- und Leistungsänderung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__163.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (one query,
  ten hosts, with the three cumulative conditions reported consistently)
- **Annotation:** The insurer may adjust the agreed premium where **three cumulative conditions** are met: (1) the **Leistungsbedarf**
  has changed in a way that is **not merely temporary and was not foreseeable** relative to the calculation bases of the agreed
  premium; (2) the newly set premium, on the corrected bases, is **appropriate and necessary** to secure the permanent fulfilment of
  the benefit; and (3) an **unabhängiger Treuhänder** has reviewed and confirmed the bases and those conditions — the contractual
  counterpart of the supervisory trustee of § 142 VAG [R11]. Two limits: the adjustment is **excluded** to the extent the benefits
  were **insufficiently calculated at the original or a previous calculation and a diligent and conscientious actuary should have
  recognised this** — i.e. **the insurer may not reprice its way out of its own mispricing** — and the trustee step falls away where
  supervisory approval is required. The article also permits a **reduction of the insurance benefit** on the same conditions as an
  alternative to raising the premium. **For delib:** this is why a German BU or Pflegerente premium is *not* unconditionally
  guaranteed even where it is level, and why the correct description is a ***Bruttobeitrag* with a *Zahlbeitrag* below it**, the gap
  being a discretionary surplus rebate withdrawable **without invoking § 163 at all** [R53]; a model that treats the *Zahlbeitrag* as
  guaranteed for the whole term is making a behavioural assumption and the notes must label it as one. **Unverified:** whether § 163
  reaches *kapitalbildende* premiums in practice, or is effectively confined to biometric covers, **was not settled by any summary**;
  the legal characterisation of the *Zahlbeitrag* mechanism as operating through § 153 rather than § 163 is the compiler's synthesis.

(delib-reg-r28)=

### R28. VVG §§ 165–170 — prämienfreie Versicherung, Kündigung, Rückkaufswert and the Stornoabzug

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__165.html (returned); some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (**nine
  queries touched this block**)
- **Annotation:** The most model-relevant entry in the contract layer. **§ 165 *Prämienfreie Versicherung*:** the policyholder may
  **at any time, for the end of the current insurance period, demand conversion into a prämienfreie Versicherung**, provided the
  agreed ***Mindestversicherungsleistung*** is reached; if not, the insurer pays the *Rückkaufswert* under § 169. The paid-up benefit
  is computed **on the basis of the Rückkaufswert under § 169 Abs. 3 to 5** and **must be stated in the contract for each insurance
  year**. **§ 166:** where the **insurer** terminates, the insurance is **automatically converted to prämienfrei**, and in the § 38
  Abs. 2 premium-default case [R30] the insurer owes the benefit it would have owed had the contract been paid-up at the date of the
  claim. **German lapse is therefore a three-way decrement** — surrender, *Beitragsfreistellung*, and premium-default conversion — the
  last two keeping the policy in force with a reduced benefit and a continuing expense loading. A delib model implementing only
  surrender says so and states what the paid-up path would do; one implementing *Beitragsfreistellung* anchors the paid-up sum to the
  **same § 169 value** the surrender path uses, or the two will not reconcile. **§ 167** lets the policyholder demand conversion into
  an insurance meeting § 851c Abs. 1 ZPO [R40]. **§ 168:** Abs. 1 — termination at any time for the end of the current insurance
  period where *laufende Prämien* are payable; Abs. 2 — the same on a single premium where the occurrence of the insurer's obligation
  is certain; **Abs. 3** — the carve-out that defines the German pension products: Abs. 1 and 2 do **not** apply to a
  **Basisrentenvertrag certified under § 5a AltZertG** with *Verwertung* excluded under § 10 Abs. 1 Nr. 2 Satz 1 Buchst. b EStG [R39]
  [R43], nor where the parties irrevocably excluded realisation before retirement. **Model consequence, the sharpest product
  distinction in delib: BAS has no surrender value and no lapse-to-surrender decrement.** **§ 169 *Rückkaufswert*.** The base measure
  is the ***Deckungskapital*** computed by recognised actuarial rules **on the calculation bases of the premium calculation**. **The
  floor — Abs. 3**, quoted from the summary: *"bei Kündigung des Vertrags mindestens der Betrag des Deckungskapitals, der sich bei
  gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt"*, with the
  supervisory Zillmer rules unaffected [R16] — **a floor on the value, not a cap on the charge**. **Abs. 4:** where the benefit is not
  guaranteed at a fixed amount the *Rückkaufswert* is the ***Zeitwert***. **Abs. 5 — the Stornoabzug**, quoted: *"Der Versicherer ist
  zu einem Abzug … nur berechtigt, wenn er vereinbart, beziffert und angemessen ist"*, with a deduction for untilgte acquisition costs
  expressly ineffective and the **burden of proof on the insurer**. A delib model carrying an acquisition charge implements the
  **five-year floor as a `max()` against the tariff surrender value** and is tested on points that surrender where the floor binds and
  where it does not. **Unverified:** only Abs. 3 and Abs.

(delib-reg-r29)=

### R29. VVG §§ 172–177 — Kapitel 6, Berufsunfähigkeitsversicherung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__172.html (returned); some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries)
- **Annotation:** **§ 172 Abs. 1** — the insurer must render the agreed benefits for a *Berufsunfähigkeit* that arose **after the
  start of the insurance**. **§ 172 Abs. 2 — the statutory definition**, quoted by the summary: *"Berufsunfähig ist, wer seinen
  zuletzt ausgeübten Beruf, so wie er ohne gesundheitliche Beeinträchtigung ausgestaltet war, infolge Krankheit, Körperverletzung oder
  mehr als altersentsprechendem Kräfteverfall ganz oder teilweise voraussichtlich auf Dauer nicht mehr ausüben kann."* Four elements
  matter for a model: the reference occupation is **the last occupation as it was structured before the impairment**; the causes are
  illness, bodily injury or more-than-age-appropriate decline of strength; the incapacity may be **whole or partial**; and the
  standard is ***voraussichtlich auf Dauer***. **§ 172 Abs. 3** permits the additional condition that the insured cannot pursue
  another activity corresponding to their previous *Lebensstellung* — the statutory basis of the ***abstrakte Verweisung*** [R37]. **§
  173 *Anerkenntnis*:** the insurer must declare in Textform whether it acknowledges its obligation, and the acknowledgement may be
  **time-limited only once**. **§ 174 *Leistungsfreiheit*:** where the conditions of liability have ceased, cessation takes effect
  **only after prior notice in Textform and only from the end of the third month following that notice** — the *Nachprüfung*
  mechanism. **§ 176**, quoted: *"Die §§ 150 bis 170 sind auf die Berufsunfähigkeitsversicherung entsprechend anzuwenden, soweit die
  Besonderheiten dieser Versicherung nicht entgegenstehen."* **§ 177 Abs. 1** applies §§ 173 to 176 to **all contracts promising a
  benefit for a lasting impairment of working capacity**. **Model consequences for BU:** the **three-month notice** is a real monthly
  cash-flow item — a reactivation recognised in month *t* still pays through *t+3*; the **once-only time-limited acknowledgement** is
  why a claims-in-payment model needs a distinct "acknowledged" state; and § 176 is the authority for giving a BU model a
  *Rückkaufswert*, a *Beitragsfreistellung* and an *Überschussbeteiligung* at all.

(delib-reg-r30)=

### R30. VVG §§ 19, 37, 38, 157 and 158 — Anzeigepflicht, Zahlungsverzug, Altersangabe, Gefahränderung

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__19.html (returned); some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; ten hosts across §§ 157/158 and across §§ 37/38)
- **Annotation:** **§ 19** — the policyholder must disclose the risk circumstances known to them for which the insurer has **asked in
  Textform**; on breach the insurer may **rescind**, rescission being **excluded** where the breach was neither intentional nor
  grossly negligent (termination on one month's notice instead), and the obligation to perform falls away where the breach was
  ***arglistig***. The rights **lapse five years after conclusion**, extended to **ten years** on intent or fraud. **§ 157** — where
  the **age of the insured person was misstated**, the benefit **changes in the ratio of the premium corresponding to the true age to
  the agreed premium**. **§ 158** — an **increase in risk** counts as such **only where it has been expressly agreed to count as
  one**, in Textform. **§ 37** — the insurer is not liable if the insured event occurs while the first premium is unpaid, but only if
  it drew attention to that consequence. **§ 38** — for a *Folgeprämie* the reported requirements for a valid *qualifizierte Mahnung*
  are **Textform**, an itemised statement of arrears, and a **minimum period of two weeks**; but **§ 166 overrides the general § 38
  consequence for life insurance**: cover does not simply cease, the contract converts to *prämienfrei* [R28]. **Model consequences:**
  § 157's pro-rata benefit adjustment is a clean, implementable rule and a natural test for RLV and KLV; § 158's default — **no
  risk-increase consequence unless expressly agreed** — is why German life and BU contracts carry no general occupation-change clause
  and why a delib BU model needs no mid-term reunderwriting state; and **German lapse is not instantaneous**: due date → qualified
  reminder with a two-week period → expiry → conversion to paid-up, so a monthly model applying a lapse decrement in the month of the
  missed premium is off by at least one month and applies the wrong benefit basis. The **five-year contestability window** is a real
  first-duration mortality and morbidity effect a model may fold into a select period, provided it says so. **Unverified:** the § 19
  Absatz numbering; whether § 38 Abs.

---

## 6. Conduct, disclosure and distribution

(delib-reg-r31)=

### R31. VVG §§ 6, 7, 1a, 7b, 7c and 214, with the VVG-InfoV — advice, information, cost disclosure and Effektivkosten

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/vvg_2008/__6.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (seven
  queries)
- **Annotation:** **§ 6** — the insurer must **question and advise** so far as the offer or the policyholder's situation gives
  occasion, **state the reasons** and **document** it. **§ 7** — the contract terms including the AVB and the VVG-InfoV information
  must be communicated **in Textform and in good time before the policyholder makes the contract declaration**. **§ 1a**, quoted from
  a summary: *"Der Versicherer muss bei seiner Vertriebstätigkeit … stets ehrlich, redlich und professionell in deren bestmöglichem
  Interesse handeln"*; **OLG Stuttgart rejected the argument that this obliges an insurer to adapt or redesign its own products** —
  the limit that keeps § 1a a conduct standard rather than a product-design mandate, and the counterweight to Merkblatt 01/2023 [R35].
  **§ 7b** requires, for *Versicherungsanlageprodukte*, information on the distribution and on **all costs and charges**; **§ 7c**
  that only products **geeignet** for the policyholder be recommended. **§ 214** recognises the **Versicherungsombudsmann e.V.** as a
  *Schlichtungsstelle* **since August 2016**. **The VVG-InfoV settles three things for delib.** **(a) Cost disclosure, § 2 Abs. 1 Nr.
  1:** the **costs included in the premium** must be disclosed — *Abschlusskosten* as a **single total amount**, other included costs
  as a percentage of the annual premium with the duration stated, and the *Verwaltungskosten* separately, with the amounts **stated in
  euro**. **This is why a German *Produktinformationsblatt* can be read as a source of actual charge levels in a way a French
  *encadré* cannot**: the *encadré* discloses maxima, the German PIB the amounts in the premium. **(b) The three Modellrechnung rates,
  § 2 Abs. 3** [R25]. **(c) Effektivkosten:** for life contracts covering a risk whose occurrence is certain, the ***Minderung der
  Wertentwicklung durch Kosten in Prozentpunkten bis zum Beginn der Auszahlungsphase*** must be disclosed, introduced by the LVRG and
  a general information duty from **January 2015**, later aligned to the **total-cost-indicator method of Annex VI to Delegated
  Regulation (EU) 2017/653** [R32]. **(d) § 4** requires the *Informationsblatt zu Versicherungsprodukten* to follow **Commission
  Implementing Regulation (EU) 2017/1469**. **For delib the Effektivkosten figure is a validation target for a product's charge
  parameterisation, not an input** — reproducing it exactly needs the PRIIPs Annex VI algorithm and a specified holding period,
  neither of which delib implements.

(delib-reg-r32)=

### R32. PRIIPs — Verordnung (EU) Nr. 1286/2014 and the delegated technical standards

- **Publisher:** European Parliament and Council
- **URL:** https://eur-lex.europa.eu/legal-content/DE/ALL/?uri=CELEX:32017R0653 (returned); further URLs in
  `_research/regulatory-actuarial.md`; otherwise **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries;
  four independent sources agreeing on the 1 January 2023 application date)
- **Annotation:** Regulation 1286/2014 introduced a standardised ***Basisinformationsblatt* (KID)** for packaged retail investment
  products **and *Versicherungsanlageprodukte***. Uniform requirements apply to delivery of the KID for **all** insurance-based
  investment products, **regardless of whether the underlying investment options are themselves PRIIPs** — the rule that pulls a
  German *fondsgebundene Rentenversicherung* with a fund menu wholly into scope. Delegated Regulation **(EU) 2017/653** of 8 March
  2017 lays down the RTS on presentation, content, review and revision; **(EU) 2021/2268** amended them with application from **1
  January 2023**. Two content elements are corroborated: the ***Gesamtrisikoindikator* (SRI)** with explanations **including a
  possible maximum loss**; and **four performance scenarios** under the 2021/2268 regime — **optimistic, moderate, pessimistic and
  stress**. The **total cost indicator method of Annex VI** is the method German third-layer *Effektivkosten* are now aligned with
  [R31]. **Unverified:** the **SRI 1–7 scale** is asserted in the market but **no search summary returned the numbers 1 to 7**; the
  recommended-holding-period rule, the RIY presentation, the cost tables at 1 year / half the RHP / RHP and the biometric-risk premium
  treatment were all sought and **none was returned**.

(delib-reg-r33)=

### R33. IDD — Richtlinie (EU) 2016/97, the transposition act of 20 July 2017 and § 34d GewO

- **Publisher:** European Parliament and Council
- **URL:** https://kanzlei-michaelis.de/umsetzung-der-eu-vermittlerrichtlinie-2016-97-idd-in-deutsches-recht/ (returned); further URLs
  in `_research/regulatory-actuarial.md`; otherwise **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries;
  eight and nine **secondary** hosts, **no primary source for either instrument**)
- **Annotation:** The IDD was transposed by the act of **20 July 2017**, in force **23 February 2018** with exceptions; because the
  European roll-out slipped, Member States were free to apply the directive from **1 October 2018**. The useful part is the
  architecture: the transposition spreads the directive across **three statutes** — **GewO** (licensing and conduct of intermediaries,
  § 34d), **VAG** (distribution, remuneration and the *Provisionsabgabeverbot*), and **VVG** (information duties and product
  assessment, via §§ 1a, 6a, 7a, 7b, 7c and 7d, [R31]). **§ 34d GewO:** a *Versicherungsvermittler* or *Versicherungsberater* needs a
  trade licence on four reported conditions — ***Sachkunde***, *Zuverlässigkeit*, *geordnete Vermögensverhältnisse* and a
  ***Berufshaftpflichtversicherung*** — with **15 hours of continuing education per calendar year**. For delib this is background with
  **no cash-flow consequence**, but it is the reason a German product's acquisition cost is structurally a **commission to a § 34d
  intermediary that the customer cannot be rebated**, which is why the *Abschlusskosten* disclosure [R31] and the Zillmerung case law
  [R36] are as prominent as they are. **Unverified:** the directive's article numbering, the **IPID** requirement, the
  demands-and-needs test, the suitability and appropriateness tests for IBIPs and the remuneration and conflicts provisions were
  **never read** — exactly the gap frlib records for the DDA at its R32.

(delib-reg-r34)=

### R34. Unisex — EuGH C-236/09 (Test-Achats), and §§ 19, 20 and 33 AGG

- **Publisher:** Court of Justice of the European Union
- **URL:** https://datenbank.nwb.de/Dokument/Anzeigen/443611/ (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; six, seven and eight hosts)
- **Annotation:** The ECJ held on **1 March 2011** in **C-236/09** that using sex as a risk factor in insurance is incompatible with
  equality between men and women under **Articles 21 and 23 of the Charter of Fundamental Rights**, and **invalidated the derogation
  in Article 5(2) of the Gender Directive with effect from 21 December 2012**. From that date sex may **no longer** lead to different
  premiums or benefits for **new** contracts; insurers must offer ***Unisex-Tarife***. On the German side **§ 19 AGG** carries the
  civil-law non-discrimination prohibition and expressly names private insurance; **§ 20 AGG** permits objectively justified
  differential treatment; and **§ 20 Abs. 2 Satz 1 AGG — the provision that allowed sex-differentiated pricing on actuarial data — was
  repealed**, leaving the rule that **costs connected with pregnancy and maternity may under no circumstances lead to different
  premiums or benefits**. **§ 33 Abs. 5 AGG** preserves sex-differentiated treatment for relationships concluded before 21 December
  2012. **Model consequence, and it is a hard one: every delib model prices unisex.** An RLV, BU or PFL model point may carry a `sex`
  attribute for **decrement** purposes — the underlying DAV tables are sex-specific [R47] — but **must not** let sex enter the
  premium. The standard market resolution is a **portfolio sex-mix assumption** applied to the best-estimate decrements; that mix is a
  modeller's assumption and is `**[std]**`. Letting a sex field leak into pricing reproduces a tariff unlawful in Germany since 2012
  and is a numbered pitfall. **Unverified:** the amending instrument and date for the § 20 Abs.

(delib-reg-r35)=

### R35. BaFin Merkblatt 01/2023 (VA) — Wohlverhaltensaufsicht and angemessener Kundennutzen

- **Publisher:** Bundesanstalt für Finanzdienstleistungsaufsicht
- **URL:** https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html
  (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (one query,
  eight hosts, **six of them BaFin's own**)
- **Annotation:** BaFin **consulted on 31 October 2022** and **published in May 2023** a *Merkblatt zu wohlverhaltensaufsichtlichen
  Aspekten bei kapitalbildenden Lebensversicherungsprodukten* setting out what it expects so that such products offer an
  ***angemessener Kundennutzen*** and distribution conflicts of interest are avoided. **Two supervisory tests are reported explicitly
  and both are quantitative in kind if not in level.** **Cost:** BaFin will particularly examine insurers whose **Effektivkosten** for
  *kapitalbildende* products are **very high in a sector comparison**, and whose **expenses for insurance intermediaries are
  noticeably high**. **Return:** producers must **formulate a return target for the relevant target market**, and a retirement product
  must be **likely to achieve a real investment success over its term — a return after costs above a justified inflation rate**. BaFin
  reports outcomes: **some products offering no appropriate customer benefit were taken off the market**, and cost reductions in
  existing portfolios and retroactive compensation measures were achieved. For delib this is the German *Value for Money* regime and
  it matters twice: a KLV, RV, FRV or IDX charge parameterisation should be **plausible against a sector Effektivkosten distribution**
  rather than merely internally consistent, because the supervisor now polices the level; and it explains why the German market moved
  to lower guarantees and lower acquisition costs after 2023 — context a product specification's market-role section needs.
  **Unverified:** **no Effektivkosten threshold, sector benchmark or numerical test appears in any summary**. Whether the Merkblatt
  applies to *fondsgebundene* and *indexgebundene* products as well as classical ones is **not established**.

---

## 7. The case law and the market's model conditions

(delib-reg-r36)=

### R36. The BGH line of authority on German life contracts

- **Publisher:** Bundesgerichtshof (press releases and case captions)
- **URL:** https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2018/2018107.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (thirteen
  queries)
- **Annotation:** Six lines of authority, each of which changes what a delib model must do. **(1) Zillmerung and the
  Mindestrückkaufswert.** **BGH 12 October 2005 — IV ZR 162/03**: clauses setting off *Abschlusskosten* against the first premiums are
  an *unangemessene Benachteiligung* and **invalid**. **BGH 25 July 2012 — IV ZR 201/10**: the same, plus clauses failing to
  distinguish the *Rückkaufswert* under § 176 Abs. 3 VVG a.F. from the *Stornoabzug* under Abs. 4 are ineffective under § 307 Abs. 1
  Satz 2 BGB. **BGH 11 September 2013 — IV ZR 17/13 and IV ZR 114/13**: for contracts concluded **up to the end of 2007**, *ergänzende
  Vertragsauslegung* gives a minimum that **may not fall below half of the ungezillmertes Deckungskapital**; **IV ZR 216/13** applies
  the floor, with reported worked figures of **15,694.12 € paid against 29,587.75 € of premiums**. **Why this matters although delib
  models new business:** the *hälftig* floor and the five-year-spread floor of § 169 Abs. 3 VVG [R28] are **different rules for
  different vintages**, so **delib must not silently apply § 169 Abs. 3 to a pre-2008 issue year**. **(2) The Widerrufsjoker.** Where
  the withdrawal instruction was defective the period never started; its home is **§ 5a VVG a.F.**, the *Policenmodell*, in force 1
  January 1995 – 31 December 2007, held incompatible with Union law by the CJEU in **2013** and decided fundamentally by the **BGH on
  7 May 2014, IV ZR 76/11**, bounded by **IV ZR 40/21** (15 March 2023) and **IV ZR 268/21**. A successful *Widerspruch* unwinds on
  **bereicherungsrechtlich** terms — premiums back plus *Nutzungen*, less risk cover consumed — **a different payout from either
  surrender or maturity; delib does not implement it**, and the notes say the pre-2008 book carries a legal option the model does not
  value. **(3) Bewertungsreserven.** **BGH 27 June 2018 — IV ZR 201/17**: **§ 153 Abs. 3 Satz 3 VVG in the LVRG version is not
  unconstitutional**, the legislature's reason being that a prolonged low-interest environment would threaten insurers' ability to
  deliver the guarantees promised. **For delib:** the statutory half is conditional on a portfolio-level test the model does not
  perform and the highest court has confirmed the insurer may reduce it to zero, so a KLV or RV model either excludes the component
  explicitly or carries it as a `**[std]**` scalar citing this decision. **(4) The Rentenfaktor.** **BGH 10 December 2025 — IV ZR
  34/25**: a clause in the AVB of a *fondsgebundene Rentenversicherung* letting the insurer **reduce the *Rentenfaktor* named in the
  Versicherungsschein** — the monthly annuity per **10,000 € of Vertragsguthaben** — **without a corresponding duty to restore it if
  circumstances improve** is **void** under **§ 308 Nr. 4 BGB** and **§ 307 Abs. 1 Satz 1 BGB**, the principles reportedly reaching
  all comparable clauses. **The single most model-relevant German decision of the last year:** the *garantierter Rentenfaktor* is a
  **hard guarantee** unless the AVB gives a **symmetric** adjustment right, so an FRV model annuitising at a fixed guaranteed factor
  implements the legally correct default rather than a simplification. **(5) The Stornoabzug.** **BGH 18 March 2026 — IV ZR 184/24**,
  overturning OLG Koblenz 2 UKl 1/23: a *kapitalmarktabhängiger Stornoabzug* does **not** infringe the *Bezifferung* requirement of §
  169 Abs. 5 Satz 1 VVG — the insurer may specify a ***Berechnungsverfahren*** rather than a concrete amount at conclusion. The
  clause: a deduction of **up to 15 % of the Deckungskapital**, depending on the **Null-Kupon-Euro-Zinsswapsatz with a ten-year term
  published by the Deutsche Bundesbank**, accepted as suitable to protect the insured community against *zinsinduzierte
  Stornierungen*. **The case was remitted on *Angemessenheit*, so that limb is open**; a delib model may implement a *Stornoabzug* of
  that shape citing this decision as the observed upper end while stating that the appropriateness of 15 % has not been decided. **(6)
  The Pflegestufe gap.** **BGH — IV ZR 126/23**, reported 30 April 2025: older AVB still refer to *Pflegestufen* and that is an
  **unintended Regelungslücke**; **Pflegegrad 2 may not automatically be equated with Pflegestufe I**, because the 2017 reform
  **materially widened** the definition of care need [R51].

(delib-reg-r37)=

### R37. GDV-Musterbedingungen and German Berufsunfähigkeit market practice

- **Publisher:** Gesamtverband der Deutschen Versicherer e.V.
- **URL:** https://www.gdv.de/gdv/service/musterbedingungen (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (three
  queries; the GDV index page and two GDV-hosted ALB PDFs)
- **Annotation:** The GDV publishes ***unverbindliche Musterbedingungen*** — model conditions that are **non-binding** for insurers
  and whose use is **purely optional**. Two facts about the BU models are established: an earlier set was dated **28 April 2021**, and
  the current ones are **MB BUV 22** and **MB BUZ 22**, dated **15 November 2022** — MB BUV the standalone *selbständige* BU, MB BUZ
  the *Zusatzversicherung* rider form. **For delib the Musterbedingungen are the natural `[S#]` primary product source class** for a
  reference product — published, free, non-proprietary and the thing most insurers' AVB derive from — provided a product specification
  that follows them also says they are **non-binding** and that real AVB differ. **BU market practice above the statutory floor**
  [R29]. Under an ***abstrakte Verweisung*** the insured does not necessarily receive benefits merely because they cannot perform
  their last occupation, provided they **could theoretically** perform another activity; under a ***konkrete Verweisung*** the insurer
  examines whether the insured **actually performs** another activity corresponding to their previous *Lebensstellung*. The reported
  market position: **almost all new contracts waive the abstrakte Verweisung**, nowadays even in basic tariffs. **The thresholds:** a
  broker summary reports the practical test as being unable to perform the last occupation **for at least six months** at **50 percent
  or more**. **Both numbers are AVB conventions, not statute.** **Model consequences for BU, and these are the operative ones:** the
  benefit is a **binary step at 50 %**, not a proportional payment, so a model must decide whether it projects incidence of ≥50 %
  incapacity or a graded state; the **six-month qualification** is a deferred period in cash-flow terms, so a monthly BU model needs
  an explicit *Karenzzeit* parameter and the worked example must show whether the first payment is in month 7 and whether it is
  backdated; and with the abstrakte Verweisung waived, **reactivation is driven only by konkrete Verweisung or recovery**, which
  materially raises expected claim duration. **Unverified — and this is the largest single gap in the contract-law layer: no clause
  text from any GDV model was retrieved.** The provisions a delib model needs — the *Rückkaufswert* clause, the *Beitragsfreistellung*
  clause and its *Mindestversicherungssumme*, the *Stornoabzug* clause and the *Verweisung* wording — are all not established, which
  blocks `[S#]` sourcing for six products; and **whether the six months operates as a retroactive fiction or as a waiting period was
  not addressed by any summary, so the choice is currently `**[std]**`.**

---

## 8. Tax and the three-layer state-subsidised pension architecture

**Read the evidence warning first.** The tax sweep ran **zero successful searches** — the shared `WebSearch` budget was exhausted
before it opened, and both queries it issued were refused. Every entry in this section rests on **second-hand corroboration**
inherited from the prudential and contract sweeps, named per entry, or on **general knowledge of German tax law**. Structural claims —
which provision carries which rule, what the mechanic is — are stated plainly because they are well established and because hedging
every clause would destroy the section's usefulness. **But every figure, effective date, percentage and paragraph number in this
section is `[unverified]` unless the entry names a sweep that corroborated it, and downstream documents must carry that tag through.**
The entries with real second-hand corroboration are **R39**, **R43**, **R44** and **R45**; everything else is general knowledge.
**delib computes no tax anywhere**: all benefit cash flows are gross of *Kapitalertragsteuer*, *Solidaritätszuschlag* and
*Kirchensteuer*.

(delib-reg-r38)=

### R38. AltEinkG — the Alterseinkünftegesetz and the Drei-Schichten-Modell

- **Publisher:** Deutscher Bundestag / Bundesrat
- **URL:** **not established.** A BGBl citation commonly reported as *vom 5. Juli 2004, BGBl. I S. 1427* is `[unverified]` and is
  recorded as a lead, not a citation
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries only at second
  hand — the act's *name* and its **1 January 2005** boundary are corroborated by the KLV product sweep, where several secondary hosts
  identify that date as the *Alterseinkünftegesetz* cut-off for the taxation of endowment proceeds
- **Annotation:** With effect from **1 January 2005** the act replaced *vorgelagerte* taxation of pensions with a ***nachgelagerte***
  system — qualifying contributions deducted during accumulation, the pension taxed as income in payment — and, because a wholesale
  switch would have doubly taxed the cohorts in the middle, introduced **two long linear transitions running in parallel**: a rising
  deductible percentage of Schicht-1 contributions [R39] and a rising taxable percentage keyed to the **year the pension starts**
  [R41]. Both are still running. The ***Drei-Schichten-Modell*** sorts retirement products by *what the state buys with the relief it
  gives*: **Schicht 1 — Basisversorgung** (the statutory scheme, *Versorgungswerke* and the private **Basisrente**), contributions
  deductible under § 10 Abs. 1 Nr. 2 EStG, benefits taxed on a cohort *Besteuerungsanteil*, the price of admission being that the
  product must look like a state pension; **Schicht 2 — kapitalgedeckte, staatlich geförderte Zusatzversorgung** (**Riester** and the
  *betriebliche Altersversorgung*), relief granted as a **direct payment into the contract** (the *Zulage*, a real cash flow) or as a
  *Sonderausgabenabzug*; **Schicht 3 — private, ungeförderte Vorsorge** (KLV, RV, FRV, IDX, SOF), contributions not deductible as
  retirement provision at all, benefits lightly taxed under § 20 Abs. 1 Nr. 6 [R45] or on the *Ertragsanteil* [R41]. **For delib the
  layer is the first classifying attribute of every product**: it decides whether a state *Zulage* appears as an inflow, whether a
  surrender decrement is legally possible at all, and whether the payout documentation discusses a *Besteuerungsanteil* or an
  *Ertragsanteil*. **Unverified:** the act's date, BGBl citation and article structure; whether the act itself introduced the
  *Basisrente* label; and **every element of the constitutional origin** — the BVerfG judgment of 6 March 2002, 2 BvL 17/99, its
  docket number, date and deadline are general knowledge.

(delib-reg-r39)=

### R39. EStG § 10 Abs. 1 Nr. 2 Buchst. b and § 10 Abs. 3 — the Basisrente deduction, the ceiling and the five prohibitions

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__10.html (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries at second hand
  (the contract sweep records **three queries** touching this provision and reproduces the five-prohibition formula as a summary
  quotation). **The prohibitions are the best-corroborated fact in the tax section**, because [R40] reaches the same product shape
  from a different statute in a different sweep
- **Annotation:** **Buchst. a** covers the compulsory systems, which delib does not model but which **consume the same ceiling a
  Basisrente contribution competes for** — the single most important behavioural fact about Basisrente demand. **Buchst. b** creates
  the private product: contributions to a contract providing **exclusively** a **monthly, lifelong *Leibrente*** on the taxpayer's own
  life, commencing **not before completion of the 62nd year of age** (60 for contracts concluded before 1 January 2012), optionally
  with supplementary cover for *Berufsunfähigkeit*, *verminderte Erwerbsfähigkeit* and *Hinterbliebene*; and only if the claims are,
  in the words a sibling search summary returned, ***nicht vererblich, nicht übertragbar, nicht beleihbar, nicht veräußerbar und nicht
  kapitalisierbar***. **Each prohibition is a model instruction:** *nicht kapitalisierbar* removes the lump-sum option and any partial
  commutation; *nicht veräußerbar* removes the surrender value and the lapse-to-cash decrement; *nicht übertragbar* removes
  assignment; *nicht beleihbar* removes the policy loan; and *nicht vererblich* means that **on death before annuitisation the fund
  does not pass to the estate** — a Basisrente **without** a *Hinterbliebenenabsicherung* rider produces **no benefit at all** on
  pre-retirement death, which is why insurers sell the rider almost universally and why a delib BAS model must either carry it or say
  loudly that the base run assumes no death benefit. **The ceiling, § 10 Abs. 3**, is not a fixed euro amount: since a reform reported
  as effective 1 January 2015 it is the contribution that would be payable to the ***knappschaftliche Rentenversicherung*** on that
  scheme's own *Beitragsbemessungsgrenze*, doubled for spouses assessed jointly. **For delib the deduction is not a cash flow of the
  contract** and no model computes it; it belongs in `product-spec.md` as the economic driver of premium behaviour, in particular the
  **year-end single-premium *Zuzahlung*** sized to the remaining headroom — so a BAS model that offers only a level regular premium
  models the wrong product.

(delib-reg-r40)=

### R40. ZPO §§ 850b and 851c — Pfändungsschutz and the shape it imposes on a Basisrente

- **Publisher:** Bundesamt für Justiz
- **URL:** https://www.gesetze-im-internet.de/zpo/__850b.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **in the
  contract sweep** (three queries; eight hosts on § 851c and nine on § 850b)
- **Annotation:** **§ 851c Abs. 1** — claims to benefits may be attached **only as earnings from employment** where **all** of the
  following hold: the benefit is granted **at regular intervals, for life, and not before the completion of the 60th year of age, or
  only on the occurrence of Berufsunfähigkeit**; the claims **may not be disposed of**; the **designation of third parties other than
  survivors as beneficiaries is excluded**; and **no capital payment other than on death has been agreed**. **§ 851c Abs. 2** —
  amounts saved in performance of such a contract are not attachable, subject to an **aggregate ceiling of 340,000 euro** and to
  annual limits. **§ 850b Abs. 1 Nr. 1** — pensions payable on account of injury to body or health, **including claims from a private
  Berufsunfähigkeitsversicherung**, are ***bedingt pfändbar***. **Model consequence: BAS is defined by these conditions, not merely
  protected by them.** The four requirements of § 851c Abs. 1 are the same four features § 10 Abs. 1 Nr. 2 Buchst. b EStG demands
  [R39] and that § 168 Abs. 3 VVG makes non-terminable [R28]. Together — **three instruments, two research sweeps, one product
  description** — they mean a BAS model has **no surrender, no capital option except a death benefit, no third-party beneficiary
  except survivors, annuity commencement not before 60 in ZPO terms and not before 62 in tax terms, and no assignment**. That is a
  complete behavioural specification, and it is why BAS is the one delib product with **no lapse-to-cash decrement at all**. For BU, §
  850b means a BU annuity in payment is conditionally attachable, which does not change the cash flow — and the notes should say so
  rather than leave the reader wondering. **Unverified:** **the annual savings allowances of § 851c Abs. 2 are contradicted across
  summaries** — a 6,000 €/7,000 € two-band ladder reported as current law since 1 January 2022 versus a 2,000 €–9,000 € age-graded
  ladder reported as pre-2022; both are recorded, both `[unverified]` on the precise bands, while the 340,000 € aggregate is agreed.

(delib-reg-r41)=

### R41. EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV — Besteuerungsanteil, Rentenfreibetrag and Ertragsanteil

- **Publisher:** Bundesministerium der Justiz. Statutory section plus the implementing regulation's § 55
- **URL:** https://www.gesetze-im-internet.de/estg/__22.html; further URLs in `_research/regulatory-actuarial.md`; some section pages
  only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration at all (session search budget exhausted)**. **Every figure in this
  entry is `[unverified]` and both tables below are reconstructions**
- **Annotation:** **Doppelbuchst. aa — the Schicht-1 rule.** Three mechanics, and the third is the one models and product documents
  get wrong. **(1) The *Besteuerungsanteil* is fixed by the year the pension starts, not by the year of receipt**, and one cohort
  table applies to the gesetzliche Rente, a Versorgungswerk pension and a private Basisrente alike; the reported path is 50 % for
  pensions beginning in or before 2005, rising to 80 % for the 2020 cohort and then more slowly. **(2) The path was flattened in
  2024** by the *Wachstumschancengesetz*, reducing the annual step to **0.5 point** with effect from the 2023 cohort and moving the
  100 % endpoint to 2058. **(3) The untaxed remainder is frozen in euro, for life.** The ***Rentenfreibetrag*** is computed **once**,
  in the year following the first full calendar year of receipt, and **stays at that euro amount for the whole duration** — so every
  subsequent increase, **including every increase in the *Überschussrente*, is fully taxable**. **Doppelbuchst. bb — the Schicht-3
  *Ertragsanteil*.** Only a fixed percentage of each payment, determined **once by the annuitant's completed age at annuity
  commencement and never changed**, is taxable; the two anchors most often quoted are **age 65 → 18 %** and **age 60 → 22 %**. The
  table is an actuarial artefact, not a policy dial — a present-value split of a life annuity on an assumed interest rate — and,
  unlike the *Rentenfreibetrag*, **it is the percentage that is frozen**, so surplus increases to a Schicht-3 annuity are taxed at the
  same light rate. **That asymmetry is the whole economic case for SOF** [R38]. **§ 55 EStDV** supplies a **second table keyed to the
  annuity's remaining term** for an ***abgekürzte Leibrente*** — which is what a *Berufsunfähigkeitsrente* from a *selbständige* BU
  contract is — while a BU annuity written inside a Basisrente falls into Schicht 1 instead, so **the same biometric benefit is taxed
  two different ways depending on the wrapper**. **Unverified: the entire Besteuerungsanteil cohort table, the entire Ertragsanteil
  row and every row of the § 55 EStDV table are reconstructions corroborated by no search result.** Whether the *Ertragsanteil* age is
  the completed year at commencement or at the start of the calendar year is not established and would shift a boundary case by one
  row.

(delib-reg-r42)=

### R42. EStG § 10a and Abschnitt XI (§§ 79–99) — the Riester subsidy machinery

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/estg/__10a.html (returned); some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no first-hand search corroboration (budget exhausted)**; second-hand only for the
  *Kleinbetragsrente* carve-out. **Every euro figure below is `[unverified]`**
- **Annotation:** **§ 10a — the deduction and the *Günstigerprüfung*.** Contributions to a certified *Altersvorsorgevertrag*, **plus
  the Zulagen credited to it**, are deductible as *Sonderausgaben* up to a reported **2,100 € a year**; the tax office computes both
  the tax saved and the *Zulagenanspruch* of its own motion and grants the better. **This split is the single most important thing a
  RIE model author must understand: only the Zulage is a contract cash flow; the Günstigerprüfung top-up is a personal tax refund and
  never touches the policy.** **§ 79 — entitlement.** Broadly those compulsorily insured in the statutory scheme plus *Beamte*; **the
  self-employed not compulsorily insured are excluded** — precisely the population Basisrente serves, so **the two subsidised products
  are complements addressed to different people, not competitors**. *Mittelbar Zulageberechtigte* are the spouse of an entitled person
  holding their **own** certified contract, who must pay at least a reported ***Sockelbeitrag* of 60 € a year** — producing a real
  contract type, **a 60 € annual premium receiving a 175 € Grundzulage**, whose omission would leave a RIE model point table missing
  an economically extreme part of the book. **§§ 83–85 — the Zulagen:** ***Grundzulage*** **175 €**; ***Kinderzulage*** **185 €**, or
  **300 €** where the child was born on or after 1 January 2008, credited by default to the **mother's** contract; a one-off
  ***Berufseinsteiger-Bonus*** of **200 €**. **§ 86 — the *Mindesteigenbeitrag***: `min(4 % × previous year's beitragspflichtige
  Einnahmen, 2,100 €)` **less the *Zulagenanspruch***, floored at 60 €. Three features drive behaviour: the **prior-year income
  base**; the **subtraction of the Zulage**; and — the real trap — **the Kürzung is proportional, not a cliff**, the Zulage being
  reduced in the ratio of the contribution paid to the *Mindesteigenbeitrag*, so a model treating it as all-or-nothing produces a
  discontinuity that does not exist. **The Zulage for year *t* is typically credited in *t+1***, so an annual-step model must state
  its choice **in the processing order**. **§§ 93–94 — *schädliche Verwendung*.** Using subsidised capital other than as permitted
  triggers repayment of the Zulagen and the § 10a advantage. **This is the behavioural heart of a RIE model**: the contract is legally
  terminable, unlike BAS, but terminating costs the entire subsidy history, so **the RIE lapse assumption should be materially below
  the RV/FRV assumption with this rule stated as the reason**; a lapse produces a *Rückkaufswert* **net of the Rückzahlungsbetrag**, a
  different quantity from the § 169 VVG value; and **a paid-up election is not *schädlich***, so the natural RIE decrement is *ruhend
  stellen*, not surrender. **§ 93 Abs. 3 — the *Kleinbetragsrente***: an annuity below a threshold expressed as a percentage of the
  ***monatliche Bezugsgröße nach § 18 SGB IV*** may be commuted at the start of the payout phase without being *schädlich*, for
  Riester and Basisrente alike. **The threshold is contested:** 1 % of the monthly Bezugsgröße (39.55 €/month on a 2026 figure of
  3,955 €) with 1.5 % only from 2027, versus **1.5 % from June 2026** (59.33 €/month). **They cannot both be right; delib picks one,
  tags it `**[std]**` and prints both.** For a small contract the commutation branch is the **modal outcome**, so both RIE and BAS
  need a commutation test at annuitisation and a model point that trips it.

(delib-reg-r43)=

### R43. AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/altzertg/BJNR132200001.html (returned); further URLs in
  `_research/regulatory-actuarial.md`; some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **in the
  contract and prudential sweeps** (six queries, thirteen hosts, including **two BZSt commentary PDFs**, the BMF Muster PIB and the
  PIA's own *Allgemeinverfügung*)
- **Annotation:** Riester and Basisrente are **certified product categories under a statute of their own**, and certification is a
  *product* approval, not a *tax* ruling: the AltZertG defines what an *Altersvorsorgevertrag* (§ 1) and a *Basisrentenvertrag* (§ 5a)
  must contain, the **BZSt** issues the certificate, and §§ 10a and 79 ff. EStG then hang the subsidy on it. **§ 1 fixes four features
  that are all model instructions.** **(a) *Beitragsgarantie* (§ 1 Abs. 1 Nr. 3):** the provider must guarantee that **at the
  beginning of the payout phase at least the paid-in *Altersvorsorgebeiträge* are available**, with **up to 20 % of total
  contributions** left out of account where they secure *Erwerbsminderung*, *Berufsunfähigkeit* or *Hinterbliebene*. This is a **100 %
  money-back guarantee at retirement**, and it is why a German Riester insurance contract is invested so conservatively and became
  hard to sell at a 0.25 % *Höchstrechnungszins* [R15]. For a RIE model it is a **floor on the fund at annuitisation**, evaluated as
  `max(fund, sum(premiums) + sum(zulagen) − biometric_carve_out)`. **(b) Earliest payout: age 62** (60 before 2012), the same boundary
  as [R39] and [R45]. **(c) The payout shape (§ 1 Abs. 1 Nr. 4):** a **lebenslange Leibrente**, or an *Auszahlungsplan* followed by a
  **Teilkapitalverrentung from at the latest age 85**, with a **Teilkapitalauszahlung of up to 30 % of the available capital** at the
  beginning of the payout phase only. **(d) Cost structure and switching:** § 2a enumerates the cost types that may be charged and
  requires the individual PIB to break them down, so **a certified product's charge structure is enumerated by statute and a RIE
  charge table can be built from published PIBs in a way a Schicht-3 charge table cannot**; a ***Wechselrecht*** to transfer the
  *Altersvorsorgevermögen* to another certified contract is expressly **not** a *schädliche Verwendung*. **The AltvPIBV and the PIA.**
  Since **1 January 2017** providers of Basisrente and Riester must use a **uniform, individual *Produktinformationsblatt***,
  delivered before the customer's declaration of intent, disclosing ***Effektivkosten*** computed **individually for each contract
  offer** — a stronger duty than the product-level VVG-InfoV figure [R31] — and assigning the product to **one of five
  *Chancen-Risiko-Klassen***, CRK 1 least risky to CRK 5 high opportunity and high risk, determined **by the PIA on behalf of the
  BMF** by examining the product for a *Modellkunde* under various capital-market scenarios. **This is a genuinely unusual feature of
  the German market with no counterpart in `uslib`, `uklib`, `jplib` or `frlib`: a public body assigns a risk class using a stochastic
  model the insurer does not control.** **delib does not implement the PIA simulation**; a RIE or BAS specification may **report** a
  published CRK and Effektivkosten as `[S#]` facts and must say that reproducing either requires the PIA's scenario set, which is
  neither public nor in scope. **Unverified:** **the text of § 5a AltZertG was never retrieved by any sweep** — only its existence and
  its § 168 Abs.

(delib-reg-r44)=

### R44. The Altersvorsorgereformgesetz 2026 and the Altersvorsorgedepot

- **Publisher:** Deutscher Bundestag / Bundesrat / Bundesministerium der Finanzen
- **URL:** https://dserver.bundestag.de/btd/21/040/2104088.pdf (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **in the
  contract sweep** (two queries, nine hosts, **four of them official** — Bundestag ×2, DRV, BMF, Bundesregierung; the 8 May 2026
  Bundesrat date and the 1 January 2027 start each from two independent sources). **This is the strongest external corroboration
  available anywhere in the tax section**
- **Annotation:** **Riester is closed.** The **Bundesrat approved the *Altersvorsorgereformgesetz* on 8 May 2026**, and **the new
  state-subsidised private provision starts on 1 January 2027**. From 2027 the Riester-Rente is **replaced by a new subsidised
  model**, described by the Federal Government as more flexible, cheaper and higher-yielding, whose central new vehicle the
  Bundestag's own text archive names the ***Altersvorsorgedepot***. A provider-side page discusses whether to let an existing Riester
  contract lie dormant or switch, which **implies grandfathering**. **This changes what a delib `riester_rente` model *is***: a model
  of a product **closed to new business from 1 January 2027** with a very large in-force book whose contractual rights survive. That
  is worth building — a closed book is exactly what a liability cash flow model is for — but the `product-spec.md` must say it plainly
  rather than present the product as current, and it means the *Beitragsgarantie* of [R43] is a feature of the **legacy** contract.
  **Unverified:** **the enactment date is contradictory** — one summary refers to an act "vom 26.05.2026" while these sources give
  Bundesrat consent on 8 May 2026; reconcilable, but neither the BGBl citation nor the promulgation date is established.

(delib-reg-r45)=

### R45. EStG § 20 Abs. 1 Nr. 6 — the Unterschiedsbetrag, the 12/62 rule and the Mindesttodesfallschutz

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://esth.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-22a/I/inhalt.html (returned); further URLs in
  `_research/regulatory-actuarial.md`; some section pages only in `[unverified canonical form]`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **in the KLV
  product sweep** (the *Unterschiedsbetrag* base, the half-income rule, the 60→62 tightening and the § 32d Abs. 2 Nr. 2 interaction
  from the BMF handbook annex plus five commentary hosts)
- **Annotation:** The tax rule that decides when a German endowment or unit-linked contract is cashed in, and therefore the shape of
  every Schicht-3 lapse assumption in delib. **The base:** the taxable amount is the ***Unterschiedsbetrag* between the
  *Versicherungsleistung* and the sum of the *Beiträge* paid on it** — a gain measure taking no account of inflation. **The
  half-income rule:** where the benefit is paid **after completion of the 60th year of life** and **at least twelve years after
  conclusion**, **only half the *Unterschiedsbetrag*** is taxable; for contracts concluded **after 31 December 2011** the age is
  **62**. **The rate:** where the halving applies to a benefit accruing from 1 January 2009 the flat *Abgeltungsteuer* does **not**
  apply — **§ 32d Abs. 2 Nr. 2 EStG** puts the half amount into the **personal marginal rate**. **The Mindesttodesfallschutz:** a
  contract concluded from **1 April 2009** qualifies for the half-income treatment **only if the *Todesfallleistung* is at least 50 %
  of all premiums payable over the whole term**; failing the test the earnings are taxed **in full** under the Abgeltungsteuer. **What
  this does to a model:** it creates a **duration-12 and age-60/62 double threshold** that policyholders wait for, so a KLV, RV, FRV
  or IDX lapse assumption that is flat in duration has ignored the strongest single driver of German surrender behaviour — surrenders
  are suppressed approaching duration 12 and spike at it, and again at the age threshold. The effect is directly analogous to the
  eight-year threshold that drives French *assurance vie* behaviour, and **delib models it the same way frlib does — as a
  duration-dependent lapse shape with the threshold named and the level `**[std]**`**. The rule reaches RV, FRV and IDX too, because a
  deferred annuity whose *Kapitalwahlrecht* is exercised for cash is taxed here while the same contract annuitised is taxed on the
  *Ertragsanteil* [R41] — **the annuitise-or-commute election is therefore a tax election**, and a model treating it as a fixed
  take-up rate says that the rate stands in for a tax comparison it does not perform. And the 50 %-Regel is a **model-point design
  constraint**: **a model point that would fail the German tax test is not representative of a real sold contract.** **Unverified:**
  whether the twelve years run from *Vertragsschluss* or from the first premium; a reported **second condition** that on death the
  agreed benefit must exceed the *Deckungskapital* by at least 10 %, whose base and time profile do not parse from the summary; and
  the **pre-2005 cohort's qualifying conditions**, which **are not asserted anywhere in delib** — what can be said is that for
  contracts concluded before 1 January 2005 the *rechnungsmäßige und außerrechnungsmäßige Zinsen* were entirely free of income tax on
  maturity, which is why an *Altvertrag* has an almost nil lapse rate and why a KLV document must say the reference model does not
  represent that cohort.

(delib-reg-r46)=

### R46. ErbStG and SGB V §§ 226, 229 and 240 — death benefits and contributions on an annuity in payment

- **Publisher:** Bundesministerium der Justiz
- **URL:** https://www.gesetze-im-internet.de/erbstg_1974/__3.html`; further URLs in `_research/regulatory-actuarial.md`; some section
  pages only in `[unverified canonical form]`; otherwise **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration (session search budget exhausted)**, except the 2026 monthly
  *Bezugsgröße* of 3,955 €, which the contract sweep records from two secondary sources, neither official. **Every figure is
  `[unverified]`**
- **Annotation:** **Germany has no insurance-specific death-benefit tax regime.** Unlike France, where CGI arts. 990 I and 757 B carve
  life insurance out of ordinary succession, a German *Todesfallleistung* paid to a named beneficiary is simply an ***Erwerb von Todes
  wegen*** under § 3 Abs. 1 Nr. 4 ErbStG — a benefit acquired under a contract for the benefit of a third party — and falls into
  ordinary inheritance tax at the beneficiary's own *Steuerklasse* and *Freibetrag*. **Two structuring facts the German market
  actually uses**, and they change who a model's beneficiary is: the ***Über-Kreuz-Versicherung***, where *Versicherungsnehmer* and
  *versicherte Person* are different people — spouses each owning a policy on the other's life — so that death triggers a payment to a
  *surviving policyholder* rather than an acquisition from a deceased one and **no inheritance tax arises**, which is standard advice
  for couples buying RLV cover and means a real RLV book contains a large share of cross-owned policies; and the **gift limb**, under
  which granting an *unwiderrufliches Bezugsrecht* during life is a *Schenkung* under § 7 ErbStG at the time of the grant [R26].
  **Social insurance is the asymmetry that can reverse the tax argument.** § 229 SGB V makes certain retirement incomes
  ***Versorgungsbezüge***, contributory in the *Krankenversicherung der Rentner* and the *soziale Pflegeversicherung* **at the full
  rate borne entirely by the pensioner**, and the class covers **betriebliche Altersversorgung** in all five *Durchführungswege*.
  **What is not a Versorgungsbezug is the point**: a **private Riester annuity**, a **Basisrente** and **every Schicht-3 annuity**
  (RV, FRV, IDX, SOF) attract **no health or long-term-care contribution at all** for a compulsorily insured pensioner. **But § 240
  SGB V reverses the result for *freiwillig versicherte* members**, for whom the whole of the member's economic capacity is
  contributory, expressly including private annuities — and **the self-employed, the core Basisrente market and a large part of the
  private annuity market, are overwhelmingly freiwillig or privately insured**, so the exposed population is precisely the one buying
  the products. Three delib parameters hang off one annual regulation, the *Sozialversicherungsrechengrößen-Verordnung*: the
  Basisrente ceiling [R39], the *Kleinbetragsrente* threshold [R42] and the § 226 *Freibetrag* — so **delib carries them as
  `**[std]**` parameters in one place, with the year stated, and every product document references that one place**.

---

## 9. Biometric bases and market statistics

**Read the evidence warning first.** The biometric sweep also ran **zero successful searches**; both queries it issued were refused
for budget. **No value from any DAV table is known to this library, at any age, for any of the five tables**, and none may appear
anywhere in delib attributed to one. The market aggregates in R53 are second-hand from the prudential sweep and carry its caveats.
Every decrement CSV in delib is a `**[std]**` proxy, anchored so the product's own worked example reproduces exactly, and each
product's `sources.md` names the DAV table the proxy stands in for and says what a replacement must preserve.

(delib-reg-r47)=

### R47. Rechnungsgrundlagen erster und zweiter Ordnung, and the DAV as owner of the tables

- **Publisher:** Deutsche Aktuarvereinigung e.V. (DAV)
- **URL:** https://aktuar.de/` (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and with **no search-result summaries of its own**;
  **no search corroboration by the biometric sweep (budget exhausted)**; the host and path shapes are second-hand from the prudential
  sweep
- **Annotation:** The DAV occupies a position with **no equivalent in frlib, uklib or uslib**: it is at once the professional body
  whose members sign the statutory certifications [R11], the standard-setter whose *Fachgrundsätze* bind them [R56], **the body that
  derives and owns the market's biometric tables**, and the body that makes the annual *Höchstrechnungszins* recommendation [R56]. In
  France the mortality tables are homologated by *arrêté* and printed in the *Code des assurances* annexe, so a modeller can read
  them; in Germany the equivalent tables are a **members' deliverable of a private association**. That single institutional difference
  is why this section is shaped the way it is: **every table citation in delib is a citation to a document the library has not read
  and cannot ship.** **The mechanic that does not depend on having a PDF open.** German life actuarial practice runs **two parallel
  sets of assumptions** over the same contract. ***Rechnungsgrundlagen erster Ordnung*** are the pricing and reserving bases — the
  *Rechnungszins* capped by the *Höchstrechnungszins*, a biometric table carrying explicit safety margins, and cost loadings; they are
  deliberately **prudent**, which is a statutory requirement [R8], and they determine the *Bruttobeitrag* and the
  *Deckungsrückstellung*. ***Rechnungsgrundlagen zweiter Ordnung*** are the best-estimate assumptions and determine what actually
  happens. **The *Sicherheitszuschlag* is the wedge between them, and its direction depends on which way the risk runs**: for a
  **death benefit** prudence means assuming mortality **higher** than expected; for a **survival benefit or annuity** it means
  **lower** mortality **and a stronger assumed improvement trend**, so a generational annuity table carries safety in **two
  dimensions** and a proxy reproducing only the level is not a proxy for the table; for **disability** it means higher incidence and
  lower reactivation; for **care**, higher incidence, longer duration in care and lower mortality of care recipients. **The wedge is
  not waste — it is the profit-sharing engine**: its systematic release as experience emerges is the *Risikoüberschuss*, one of the
  three *Überschussquellen* fed into the RfB and distributed under the MindZV [R10] [R18]. **A delib model that projects only
  best-estimate cash flows must still know the first-order basis**, because that is what fixes the *Bruttobeitrag* and the guaranteed
  benefits — the numbers the contract states — while the second-order basis drives the projection; the technical notes' three-way
  assumption split is this distinction wearing different clothes. **An insurer may use its own table**, so the DAV table is a **market
  default and benchmark, not a legal mandate**.

(delib-reg-r48)=

### R48. DAV 2008 T and its predecessors — the death-benefit mortality basis

- **Publisher:** Deutsche Aktuarvereinigung e.V., 2008 `[unverified]`. Proprietary actuarial table. **Not public, not redistributable;
  delib ships no version
- **URL:** **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration (budget exhausted)**. The table's *name* is corroborated only at
  one remove, from the commissioning brief and the prudential sweep's gap register, not from an independent search hit
- **Annotation:** The market-standard first-order mortality basis for **German death-benefit business** — *Risikolebensversicherung*,
  the death component of a *Kapitallebensversicherung*, death cover in a deferred annuity's accumulation phase, and the
  *Beitragsrückgewähr* death benefit of a BAS or RIE contract. It succeeded **DAV 1994 T** and is understood to derive from pooled
  German insured-lives experience rather than population data — the substantive difference from a Destatis table [R52], since insured
  lives are **selected** and their mortality is materially lighter than the general population's at the working ages term cover lives
  at. Structural features a `**[std]**` proxy must reproduce, each `[unverified]`: **sex-specific base tables** (raw material even
  though a tariff may not price on sex since 2012, [R34]); a **smoker/non-smoker split**, which German term insurers use heavily and
  which produces the roughly two-to-one premium spread in the RLV market; **selection factors** for the first years after
  underwriting; and **no projected mortality improvement**, because for death cover improvement is favourable to the insurer, so a
  prudent first-order basis does not project it. **That is the exact opposite of DAV 2004 R [R49], and it is why a single "German
  mortality table" does not exist: the direction of prudence forks by product.** Model consequences: an RLV model built on a
  population table without a selection adjustment **overstates claims by a wide margin at issue ages 25–45**, so the RLV proxy is
  documented as insured-lives-shaped with its anchor stated; and where a KLV carries both a death and a survival benefit, **using one
  table for both is a numbered pitfall**. **Unverified:** the publication year (2008 is inferred from the name), the data window, the
  age range, whether smoker/non-smoker and selection tables are part of the published set, the size of the loading, and whether a
  first- and second-order pair is distributed — **all not established**, as are the names and dates of DAV 1994 T and ADSt 1986.

(delib-reg-r49)=

### R49. DAV 2004 R and DAV 2004 R-Bestand — the generational annuity tables

- **Publisher:** Deutsche Aktuarvereinigung e.V., 2004 `[unverified]`. Proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version
- **URL:** **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration**; the two queries the biometric sweep was permitted to attempt
  were both aimed at this table and both were refused
- **Annotation:** The market-standard first-order basis for **every German annuity promise** — RV and SOF directly, and FRV, IDX, BAS
  and RIE through annuitisation of the accumulated fund. Its defining property is that it is a ***Generationentafel***: a
  two-dimensional basis $q(x,\\tau)$ in attained age and calendar year, **not a period table**. That is the one structural fact a
  delib annuity model must reproduce, and reproducing it is not optional — **a period-table proxy priced at a 40-year-old's
  annuitisation in 2055 understates the liability by a margin that dwarfs every other assumption in the model**. The construction, as
  the German market describes it and `[unverified]` in every detail: a **Basistafel** of second-order mortality for a stated base
  year, sex-specific; a ***Trendfunktion*** supplying age-dependent annual improvement rates; and safety loadings applied to **both**
  the level and the trend. The trend is not constant over time — the German construction uses a **Starttrend** fitted to recent
  experience **converging to a weaker Zieltrend** — so **a proxy applying one flat improvement rate forever is qualitatively wrong in
  long deferrals**. For single-premium immediate annuities buyers self-select for good health and the table is understood to carry
  ***Selektionsfaktoren***, the mirror image of the underwriting selection in DAV 2008 T, running the same direction for the opposite
  reason; **a SOF model that ignores it understates the annuity cost**. **DAV 2004 R-Bestand** is the variant for the
  *Deckungsrückstellung* of annuities **already in force**: when DAV 2004 R was introduced it revealed that the book priced on DAV
  1994 R was reserved on mortality that had proved far too heavy, and the strengthening (*Nachreservierung*) was permitted to be
  financed over a transition period. **Modelling consequences:** every delib annuity model needs **two indices** on the mortality
  cells, with the calendar year stated as `issue_year + t`; the `**[std]**` proxy must be **generational**, built as a base table
  times a cumulative improvement factor anchored to Destatis's own generational tables [R52], which are the free and redistributable
  analogue; and the guaranteed *Rentenfaktor* of an FRV or IDX contract is the arithmetic image of this table plus the guaranteed
  rate, so a model publishing a `[std]` *Rentenfaktor* **and** a `[std]` annuity table must state whether the two are consistent and,
  if not, which is authoritative.

(delib-reg-r50)=

### R50. DAV 1997 I / RI / TI — the Berufsunfähigkeit decrement family

- **Publisher:** Deutsche Aktuarvereinigung e.V., 1997 `[unverified]`. Proprietary actuarial tables. **Not public, not
  redistributable; delib ships no version
- **URL:** **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration (budget exhausted)**
- **Annotation:** **The naming is recorded here as a question, not a settled fact.** A German BU model needs **three** decrements and
  the market names a family of **three** tables — **I** for *Invalidisierung* (incidence), **RI** for *Reaktivierung*, and **TI** for
  the *Sterbewahrscheinlichkeiten der Invaliden*. Reading "TI" as the reactivation table would leave disabled-life mortality
  unspecified, which no multi-state BU model can do; the three-table reading is `[unverified]`, and **a delib document should not
  repeat a two-table pairing without checking.** **The multi-state structure the tables serve.** A BU model is a three-state process —
  *aktiv* → *invalide* → *tot*, with a return arc *invalide* → *aktiv* — needing, per age and sex: $i_x$ (incidence), $q_x^{aa}$
  (active-life mortality, from DAV 2008 T or its predecessor, [R48]), $q_x^{ii}$ (disabled-life mortality, materially heavier than
  active mortality especially in the first year after disablement) and $r_x$ (reactivation, concentrated in the first two years of a
  claim and near zero thereafter). **This is the most data-hungry product in delib and the one whose `[std]` proxies carry the least
  support.** **The age of the basis is itself a finding:** these tables date from 1997 and rest on older experience, while German BU
  claims experience has shifted decisively — the causes mix has moved towards psychiatric diagnoses and the statutory
  *Berufsunfähigkeitsrente* was abolished for cohorts born from 1961, changing both the insured population and its incentives. A
  thirty-year-old first-order basis with a heavy safety loading is **why the German BU market runs a large and persistent
  *Bruttobeitrag*/*Zahlbeitrag* gap** [R37]. **Modelling consequences:** the BU model must publish an **explicit reactivation
  assumption** — setting it to zero is a choice with a large, one-directional effect that must be argued, not defaulted;
  **disabled-life mortality must be separate from active-life mortality**, using one rate for both being a numbered pitfall; and the
  six-month qualification and the 50 % degree threshold are **AVB conventions, not table properties** [R37].

(delib-reg-r51)=

### R51. DAV 2008 P, § 15 SGB XI and the Pflegegrad break

- **Publisher:** Deutsche Aktuarvereinigung e.V., 2008 `[unverified]`, for the table
- **URL:** https://dejure.org/gesetze/SGB_XI/15.html (returned); further URLs in `_research/regulatory-actuarial.md`; some section
  pages only in `[unverified canonical form]`; otherwise **not established**
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and with **no search-result summaries of its own**;
  **no search corroboration for the table**; the **five Pflegegrade, § 15 SGB XI as their home and the points-based assessment are
  corroborated at one remove by the contract sweep (three independent sources)**
- **Annotation:** **DAV 2008 P** is the market-standard first-order basis for private long-term-care business —
  *Pflegerentenversicherung*, and in the health sector *Pflegetagegeld* and *Pflegekosten* cover, which delib treats as out of scope.
  It is understood to supply, by age and sex, **transition probabilities into care**, **mortality of people in care** and
  **transitions between care levels** `[unverified]`. **The finding that matters most is a mismatch, not a number.** A table published
  in 2008 is necessarily defined on the **three *Pflegestufen*** of the pre-2017 social care insurance. The *Zweites
  Pflegestärkungsgesetz* replaced them on **1 January 2017** with the **five *Pflegegrade*** of § 15 SGB XI, assessed by a
  points-based *Begutachtungsinstrument* that deliberately **widened** the definition of care need, particularly on cognitive and
  mental grounds — and the BGH has **refused to map the two scales** [R36]. **If the courts will not map the grades, a modeller may
  not silently do so either.** Therefore, for delib's PFL product: the model **states which trigger scale it implements** —
  *Pflegegrade*, an ADL points system, or a combination — and **any incidence proxy calibrated to Pflegegrade data is explicitly not a
  proxy for DAV 2008 P**, because the two are defined on different state spaces separated by a definitional break that raised measured
  prevalence. **The social scheme is the benchmark the private product is sold against:** it pays *Pflegegeld*, *Pflegesachleistung*
  and a fixed contribution to residential care, with **Pflegegrad 1 receiving none of the three**; the amounts rise steeply with grade
  and are capped and partly in kind, which is why **the private *Pflegerente* — uncapped cash, paid irrespective of setting — is the
  product's entire selling proposition** and why its benefit is modelled as an annuity rather than a reimbursement. The private
  benefit ladder is conventionally a **percentage of the full *Pflegerente* per Pflegegrad**, and **no market standard was
  established**, so it is `**[std]**` in delib unless a *Tarifblatt* supplies it.

(delib-reg-r52)=

### R52. Destatis — Sterbetafeln, Generationensterbetafeln, Pflegestatistik and the reuse licence

- **Publisher:** Statistisches Bundesamt (Destatis), Wiesbaden
- **URL:** **not established** for any of them; no Destatis path was returned to any sweep
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy, and — unlike the rest of this page — **not established
  from search-result summaries either**; **no search corroboration (budget exhausted)**
- **Annotation:** The **free, redistributable, population-level German mortality basis**, and therefore the raw material behind every
  `**[std]**` decrement CSV delib ships — exactly the role INSEE plays in frlib. **Two distinct products, and confusing them is a real
  error:** the *Sterbetafel 20xx/20yy* is a **period table** computed annually from three years of deaths and population; the
  *Allgemeine Sterbetafel* is computed once per census cycle on census-corrected denominators, is the more accurate, and is the one
  usually used as a base table. **Why a population table is the wrong shape:** insured lives are selected, so population mortality is
  heavier than insured mortality at the ages term and endowment business lives at, and lighter than annuitant mortality is light —
  **it sits between the two insured populations and matches neither**. A delib proxy built from it therefore carries an explicit,
  `[std]`-tagged adjustment with a stated direction: **downward for a term or endowment death leg** (medical selection) and **downward
  again and generationally for an annuity** (voluntary anti-selection plus improvement). **The *Generationensterbetafeln für
  Deutschland* are the single most useful public document in this section**: cohort life tables built from historical German mortality
  plus a projected improvement, normally in more than one variant — **exactly the structure DAV 2004 R has** [R49], and therefore the
  right public basis for delib's `[std]` generational annuity proxy, built as
  $q(x,\\tau)=q_{\\text{base}}(x)\\cdot\\prod(1-\\lambda(x))$ over the calendar years from the base year, with $\\lambda(x)$ a `[std]`
  age-dependent improvement rate anchored so the worked example reproduces exactly and documented as a **simplification** of the
  Starttrend/Zieltrend structure rather than a replication of it. The ***Pflegestatistik*** is the **only public German prevalence
  data for long-term care** and therefore the calibration target for every `[std]` PFL incidence assumption; **the series contains a
  definitional break at the 2017 reform that is not a change in the underlying risk** [R51], so any delib document quoting a
  prevalence trend says so and **no incidence proxy is calibrated across the break**. **The licence question, and why delib's position
  does not depend on it:** German official statistics are understood to be released under a permissive attribution licence — the same
  assumption frlib records as `[unverified]` for INSEE — but **delib's ruling is safe under either answer**, because the shipped CSVs
  are **constructed, anchored, documented `[std]` proxies**, not reproductions of any published series, each carrying a `provenance`
  column naming what it stands in for. **It does depend on never shipping a DAV table**, which is not a licence question at all.

(delib-reg-r53)=

### R53. The German life market in numbers — GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen and Franke und Bornberg

- **Publisher:** Gesamtverband der Deutschen Versicherungswirtschaft e.V.
- **URL:** https://www.bafin.de/SharedDocs/Downloads/DE/Statistik/Erstversicherer/neu/dl_st_24_erstvu_lv_va.html (returned); further
  URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **in the
  prudential sweep** (six queries; the GDV aggregates from two independent reports of the same publication)
- **Annotation:** **Volumes, 2024, GDV basis** (Lebensversicherer, Pensionskassen and Pensionsfonds together): premium income **+2.8 %
  to €94.6 bn**; *laufende Beiträge* **€66.3 bn**, roughly flat; *Einmalbeitragsgeschäft* about **+10 % to €28 bn**; **contract count
  −1.4 % to 80.3 m**. The operative reading is the **Einmalbeitrag shift**: single premium is now roughly 30 % of income and growing
  an order of magnitude faster than regular premium, which is why SOF is a live product and why KLV and RV model point tables include
  single-premium points. **Volumes, 2024, BaFin basis**: life-segment *verdiente Bruttobeiträge* **€90.4 bn**. **The GDV and BaFin
  figures measure different populations on different bases and must never appear in the same table in delib.** **The GDV taxonomy** is
  the vocabulary any German market figure comes in: *Kapitalversicherungen* → KLV, *Risikoversicherungen* → RLV,
  *Rentenversicherungen* → RV and SOF, *fondsgebundene* → FRV, *sonstige Lebensversicherungen* (where index business sits and is **not
  separately visible**), and *Zusatzversicherungen* (BU as a **rider**, while delib models the *selbständige* form); Riester and
  Basisrente **cut across** it. **Declared rates.** For **2025**, average *laufende Verzinsung* **2.53 % Klassik / 2.58 % Neue
  Klassik**; for **2026** the sources give **2.6–2.7 %**, **2.87 %** and **2.54 %** — three incompatible averages. **The *laufende
  Verzinsung* is the *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung***, so a declared 2.5 % on a 1.0 % guarantee
  implies a 1.5 pp surplus credit and **a delib model must never add the declared rate on top of the guarantee** — a numbered pitfall
  for every general-account product. **Cost ratios, 2024:** *Verwaltungskostenquote* **2.4 %** on one measurement and **2.19 %** on
  another, with a market spread **from under 2 % to over 4 %**. **The 2024 solvency reset** [R13]: the life industry's SCR ratio
  **including** transitionals was **340.3 % at end-2024 against 663.6 % at end-2023**, a fall **driven by the recalculation rather
  than by economics**; **three life insurers failed to reach 100 % without Hilfs- und Übergangsmaßnahmen at 31 December 2024**; base
  ratios **excluding** transitionals stayed largely stable — the recalculation removed an accounting cushion, not capital. **The
  survey houses** supply what no statutory source does: Assekurata's annual *Überschussdeklaration* tracks the declared rates and the
  shift from full *Beitragsgarantie* through "Neue Klassik" partial guarantees to levels below 100 % of premiums — the premise of
  delib's IDX product; *map-report* draws insurer-level series from the statutory accounts [R54] and gives the **spread** as well as
  the average, which is what a `**[std]**` parameter needs; and MORGEN & MORGEN and Franke und Bornberg publish the two standard **BU
  claims-practice** studies. **The BU consequence is specific:** a model paying every incident claim in full is modelling a 100 %
  acceptance rate, so **delib's BU incidence assumption is `**[std]**` net of declinature, stated as such**, with a pitfall recorded
  that applying a gross incidence table *and* an acceptance ratio double-counts.

---

## 10. Accounting and professional standards

(delib-reg-r54)=

### R54. HGB §§ 341–341o, RechVersV and BerVersV — the German statutory accounts and supervisory returns

- **Publisher:** Bundesamt für Justiz
- **URL:** https://dejure.org/gesetze/HGB/341f.html (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (four queries)
- **Annotation:** **§ 341e — the standard of prudence.** Insurers must form technical provisions **to the extent necessary according
  to reasonable commercial judgement (*nach vernünftiger kaufmännischer Beurteilung*) to ensure the *dauernde Erfüllbarkeit* of the
  obligations** — the same standard § 138 Abs. 1 VAG imposes on premiums [R8] and BaFin states as its supervisory objective [R21], and
  the reason the German statutory reserve is deliberately conservative rather than best-estimate. **§ 341f — the
  *Deckungsrückstellung*.** One must be formed for obligations from **life insurance and from insurance business conducted in the
  manner of life insurance** — the hook that brings a *Pflegerente* or a stand-alone BU annuity inside the same reserving rule — at
  the amount of its ***versicherungsmathematisch berechneter Wert***, **including profit shares already allocated** but **excluding
  *verzinslich angesammelte Überschussanteile***, and **after deducting the actuarially calculated present value of future premiums**:
  the **prospective method**, with a retrospective fallback where a prospective calculation is not possible. **The RechVersV** is the
  statutory-accounts rulebook: insurers use **Formblatt 1 instead of § 266 HGB** for the balance sheet and **Formblatt 3** for the
  life/health profit and loss account, both following the ***Nettoprinzip***. **§ 28 gives the German surplus system its published
  anatomy:** within the RfB a ***Schlussüberschussanteilfonds*** is formed for *Schlussüberschussanteile*, *Schlusszahlungen*,
  *Gewinnrenten* and the minimum participation in *Bewertungsreserven*. **§ 28 Abs. 8 is the disclosure that makes the chassis
  auditable from outside:** the *Anhang* must give, in tabular form, the **development of the RfB**; the portions attributable to its
  components **including the Schlussüberschussanteilfonds**; for **individual *Abrechnungsverbände*** the ***festgelegte
  Überschussanteile*** and where applicable the ***Ansammlungszinssatz***; and the **procedures used to calculate the
  Schlussüberschussanteilfonds together with the chosen actuarial assumptions**. **This is the single most useful published source on
  a named insurer's surplus system**, and the reason a delib product document can cite a declared *Überschussanteilsatz* at all. **The
  BerVersV** governs the national, HGB-based returns beyond the Solvency II templates: life insurers must prepare *formgebundene
  Erläuterungen* including the ***Zerlegung des Rohergebnisses nach Ergebnisquellen*** under **Nachweisungen 213 bis 219**, filed as
  forms **F.213.01 to F.219.01** — the **source-of-earnings split** (*Kapitalanlageergebnis*, *Risikoergebnis*, *übriges Ergebnis*)
  that is exactly the three-way split the MindZV's 90/90/50 minima operate on [R18], the MindZV cross-referring into these forms **by
  named cell**. **A German minimum allocation is therefore computed from named cells of a named supervisory form**, which is unusually
  concrete and worth saying in a delib technical note. **delib computes none of this:** no model produces a *Deckungsrückstellung*, an
  RfB stock or a P&L, and the accounting layer is cited, never specified.

(delib-reg-r55)=

### R55. IFRS 17 — Versicherungsverträge and the Variable Fee Approach

- **Publisher:** IASB
- **URL:** https://www.drsc.de/projekte/insurance-contracts/ (returned); further URLs in `_research/regulatory-actuarial.md`
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries (two queries)
- **Annotation:** The EU published **Verordnung (EU) 2021/2036 in November 2021**, taking IFRS 17 into EU law; the application date
  had been **deferred by one year to 1 January 2023**, and the standard applies **for financial years beginning on or after 1 January
  2023**. **Scope:** insurance contracts, reinsurance contracts and **investment contracts with discretionary participation features**
  — the last category matters in Germany because it catches savings vehicles that are not insurance in the risk-transfer sense. **The
  Variable Fee Approach** is an adaptation of the building-block approach for contracts with **direct participation features** and is
  **mandatory** for them: it explicitly reflects the value development of the underlying items, and the difference between the value
  computed at the first step and the value the actuaries compute at the second is **recorded in the Contractual Service Margin** —
  which is what "variable fee" names. Under the VFA, **investment returns on the underlying portfolio no longer hit the income
  statement immediately; they flow through the CSM, which is released progressively.** German life contracts qualifying for the VFA
  typically include the HGB gross-surplus participation — i.e. **the *Überschussbeteiligung* chassis of [R9], [R10] and [R18] is
  precisely what makes them direct-participating.** For delib IFRS 17 is **cited, never specified**: no model produces a CSM, a risk
  adjustment or a fulfilment cash flow, and the models produce gross liability cash flows that an IFRS 17 measurement would take as
  one input. **Unverified:** the CSM, the risk adjustment, the coverage units and the transition approaches beyond the sentences
  above; which German life insurers report under IFRS 17 (only listed groups do; solo German statutory accounts remain HGB); and
  **whether Riester and Basisrente contracts qualify as direct-participating**.

(delib-reg-r56)=

### R56. DAV Fachgrundsätze and the annual Höchstrechnungszins recommendation

- **Publisher:** Deutsche Aktuarvereinigung e.V.
- **URL:**
  https://aktuar.de/de/newsroom/detail/dav-empfiehlt-auch-fuer-2027-einen-hoechstrechnungszins-fuer-lebensversicherungs-neuvertraege-in-hoehe-von-10-prozent/
  (returned)
- **Accessed:** 2026-08-29
- **Fetched:** no — direct HTTP egress blocked by organisation network policy; established from search-result summaries **for the
  recommendation** (four queries; the mechanism described consistently by three independent sources and the 2026 and 2027
  recommendations each by two); **no search corroboration for the Fachgrundsätze**
- **Annotation:** **The recommendation and its method.** The *Höchstrechnungszins* is set by the Bundesministerium der Finanzen as the
  DeckRV's *Verordnungsgeber* [R14]; **the DAV submits an annual proposal**, and **the ministry has in the past mostly followed it** —
  a soft-law channel with no statutory anchoring any search result identified, so delib describes it as **practice rather than law**.
  The method: model calculations on a representative *Neuanlageportfolio*; scenarios for the development of returns **weighted
  stochastically**; a **five-year average** to damp short-term fluctuations; and a ***Sicherheitsabschlag* of 40 %** applied to the
  smoothed return. The 40 % haircut is the residue of the statutory **60 % ceiling** that bound the German rate from the mid-1990s
  until Solvency II — derived from **Article 17 of the Third Life Directive of 1992**, carried forward as **Article 20 of Directive
  2002/83/EC**, under which the reserving rate could not exceed 60 % of the rate on bonds issued by the State in whose currency the
  contract is denominated. **That rule was repealed without replacement when Solvency II took effect on 1 January 2016**, which is why
  the current German rate rests on a ministerial judgment informed by an actuarial recommendation rather than on a formula. The DAV
  recommended the increase from **0.25 % to 1.00 % for 2025**, which the ministry adopted [R15], then recommended keeping **1.0 % for
  2026** and again **1.0 % for 2027** (press release of 26 November 2025). **The asymmetry that matters for delib:** the interest
  haircut is **documented and quantified at 40 %**; the biometric haircuts [R47] are **neither, for any of the five tables**, and this
  library must not present the two legs of the *Rechnungsgrundlagen* as equally supported. **The professional standards.** The German
  actuarial standards system is understood to be a three-tier hierarchy — *Grundsätze*, *Richtlinien* and *Hinweise*, together the
  ***Fachgrundsätze***, binding on DAV members through the association's conduct rules — plus non-binding *Ergebnisberichte*,
  `[unverified]` throughout. The mechanism that matters for a cash flow model is the chain from standard to tariff: § 138 VAG requires
  prudent actuarial assumptions [R8] and § 2 DeckRV prudently chosen bases [R14], and **neither instrument names a table**; the gap
  between "prudent" and "this specific $q_x$" is closed by the *Verantwortlicher Aktuar* under § 141 VAG [R11] exercising professional
  judgement. **A German biometric basis is therefore soft law with hard consequences:** no statute mandates DAV 2008 T, and yet
  essentially every German term tariff is priced on it or on an insurer table justified against it. **The delib convention that
  follows:** cite the **named document or nothing** — a delib document that cites "a DAV standard" without saying which tier it
  belongs to is making a claim it cannot support.

---

### The two liability measures one projection feeds

A German life insurer values the same book twice, on two different bases, and both valuations consume the same per-policy projection
of premiums, claims, expenses and discretionary benefits. Keeping them apart is the single discipline this page exists to enforce.

**The HGB *Deckungsrückstellung*.** A prospective, deliberately prudent reserve computed on the *Rechnungsgrundlagen erster Ordnung*
of the premium calculation — the contract's own *Rechnungszins*, capped at conclusion by § 2 DeckRV [R14] [R15], and a first-order
biometric table [R47] — formed to the extent necessary to ensure *dauernde Erfüllbarkeit* [R54], increased by the *Zinszusatzreserve*
where the § 5 Abs. 3 DeckRV *Referenzzins* falls below the tariff rate [R17], and reduced by the actuarial present value of future
premiums. **This is the balance sheet the German surplus system actually operates on:** the MindZV 90/90/50 minimum allocation [R18],
the RfB ring fence and its two escape hatches [R10], the RfBV ceiling on the *ungebundene* part [R19] and the § 139 VAG
*Sicherungsbedarf* test on *Bewertungsreserven* [R9] are all computed on the HGB accounts, not on the Solvency II ones — which is why
a document describing a German contract must name the HGB measure even though no delib model computes it.

**The Solvency II *Solvabilitätsübersicht*.** A market-consistent balance sheet under §§ 74–88 VAG [R6], transposing Directive
2009/138/EG [R1] and elaborated by Delegated Regulation (EU) 2015/35 [R2], on which technical provisions are a **best estimate**
discounted at the EIOPA risk-free term structure [R4] plus a **risk margin**, with the long-term-guarantee measures and the §§ 351–353
transitionals [R13] sitting on top. Contract boundaries, the cost-of-capital rate and the standard-formula shocks were **never read
from a retrieved instrument**, so every one of them is `**[std]**` in this library, and the SCR and MCR layers are
cited-not-specified. **IFRS 17** [R55] is a third measure but a group-reporting one: German solo statutory accounts remain HGB, and no
delib model produces a CSM.

**What this library computes: none of them.** The delib models publish gross best-estimate-style liability cash flows per model point,
income-positive, undiscounted, on a declared annual or monthly grid. The discounting, the margins, the *Deckungsrückstellung*
recursion, the *Zinszusatzreserve*, the RfB stock and the CSM layer belong to a layer above — which is the only honest way to serve
two statutory bases and one international standard from a single projection, and the reason every product document says so in its own
scope note.

**And one last time, because it governs every line above.** No document cited on this page was retrieved: direct HTTP egress is
blocked by organisation network policy, every host in the table above refused with HTTP 403, and the `WebSearch` budget that supplied
every summary behind these fifty-six entries was exhausted before the biometric and tax sweeps could run at all. **Re-verify against
the instrument before relying on anything here.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-reg-r1
[R10]: #delib-reg-r10
[R11]: #delib-reg-r11
[R12]: #delib-reg-r12
[R13]: #delib-reg-r13
[R14]: #delib-reg-r14
[R15]: #delib-reg-r15
[R16]: #delib-reg-r16
[R17]: #delib-reg-r17
[R18]: #delib-reg-r18
[R19]: #delib-reg-r19
[R2]: #delib-reg-r2
[R20]: #delib-reg-r20
[R21]: #delib-reg-r21
[R24]: #delib-reg-r24
[R25]: #delib-reg-r25
[R26]: #delib-reg-r26
[R27]: #delib-reg-r27
[R28]: #delib-reg-r28
[R29]: #delib-reg-r29
[R3]: #delib-reg-r3
[R30]: #delib-reg-r30
[R31]: #delib-reg-r31
[R32]: #delib-reg-r32
[R34]: #delib-reg-r34
[R35]: #delib-reg-r35
[R36]: #delib-reg-r36
[R37]: #delib-reg-r37
[R38]: #delib-reg-r38
[R39]: #delib-reg-r39
[R4]: #delib-reg-r4
[R40]: #delib-reg-r40
[R41]: #delib-reg-r41
[R42]: #delib-reg-r42
[R43]: #delib-reg-r43
[R45]: #delib-reg-r45
[R47]: #delib-reg-r47
[R48]: #delib-reg-r48
[R49]: #delib-reg-r49
[R5]: #delib-reg-r5
[R51]: #delib-reg-r51
[R52]: #delib-reg-r52
[R53]: #delib-reg-r53
[R54]: #delib-reg-r54
[R55]: #delib-reg-r55
[R56]: #delib-reg-r56
[R6]: #delib-reg-r6
[R7]: #delib-reg-r7
[R8]: #delib-reg-r8
[R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
