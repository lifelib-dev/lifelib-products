# Product Specification

**Status:** Draft, 2026-08-29 (access date for every citation below).

**Scope note.** This is a *standardized composite specification* assembled for reference liability
cash-flow modeling of a German **indexgebundene Rentenversicherung** — the *Indexpolice*: a deferred
private annuity of *Schicht 3* whose accumulated capital sits in the insurer's *Sicherungsvermögen*
(the ring-fenced general-account cover pool) under a guarantee, and whose annually declared
*Überschuss* (surplus) is **not credited as interest** but spent as an **option budget** buying a
one-year participation in a share index. It does not describe any single insurer's contract.

Facts carrying a source tag — [S#] (primary product documents: AVB, *Produktinformationsblatt*,
*Basisinformationsblatt* (PRIIP-KID), *Verbraucherinformation*, *Standmitteilung*) and [R#]
(product-specific regulatory and actuarial references), both numbered per `_research/indexpolice.md`
and resolved in `sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose own
R-numbering is distinct and also frozen) — name the instrument the claim should be checked against.
Values marked **[std]** are standardizations introduced for the reference implementation; each
**[std]** table row carries a numbered footnote giving the rationale and, where one could be assessed,
the plausible market band. Claims no retrieval and no search corroborated are flagged [unverified].

**Read this before reading any number below.** delib was built with **direct HTTP egress blocked** and,
for this product, **with the session's `WebSearch` budget already exhausted**. No AVB, no
*Produktinformationsblatt*, no *Basisinformationsblatt*, no statutory text and no index rulebook was
opened, and no search summary was available either. **A delib `indexpolice` citation is a pointer, not a
certificate**, and the consequence is unusually heavy here: **not one cap level, participation rate,
charge level, entry-age band or minimum premium was established for any German carrier**, so the
commercial envelope below is **[std] throughout**. What *is* established, and not in dispute, is the
**mechanics** — the financing identity between declared surplus and option budget, the
sum-of-capped-monthly-returns payoff with uncapped negative months, the annual floor at zero, the
permanent lock-in and the annual election — and this document puts its weight there. Three carrier
products are named — **Allianz IndexSelect** [S2], **R+V-IndexInvest** [S7] and **Stuttgarter
index-safe** [S8] — all [unverified], and no fourth is added.

---

## Product overview and market role

An *Indexpolice* is an **aufgeschobene Rentenversicherung**: a deferred annuity on a single life, with
an *Aufschubphase* running from inception to *Rentenbeginn* and a *Rentenphase* paying a lifelong
*Leibrente* thereafter [S1] [S9]. Premium, reserve, death benefit before *Rentenbeginn*,
*Rückkaufswert*, *Beitragsfreistellung*, *Rentenfaktor*, *Kapitalwahlrecht* and *Rentengarantiezeit* are
the chassis of a *klassische Rentenversicherung* and are documented for that product. **The delta is one
clause set**: how the annually declared *Überschuss* is applied. Three facts decide everything else, and
the first two are the ones secondary descriptions usually get wrong.

**1. The capital is in the general account, not in a fund.** The accumulated *Deckungskapital* sits in
the *Sicherungsvermögen* [REG-R7], exactly as a classic annuity's does: no *Anlagestock*, no unit
account, no policy-level asset allocation. The policyholder owns a **claim on the insurer measured in
euros**, not a number of units; the reserve rolls forward by a recursion, not by a unit price; and the
*Rückkaufswert* is a reserve, not a *Zeitwert* of units [R2] [REG-R28]. **What the index does is define
a payoff, not an investment** — the policyholder is never invested in the index at any moment, and the
insurer buys the option package that hedges the payoff it has itself written [R9] [REG-R7].

A terminological trap follows. In regulatory and accounting vocabulary, *"Lebensversicherungen, bei
denen das Anlagerisiko vom Versicherungsnehmer getragen wird"* — the balance-sheet class containing
*fondsgebundene* **and** *indexgebundene* life insurance — means contracts where the **policyholder
bears the investment risk**. An *Indexpolice* of the kind described here does not belong there, and is
booked and reserved as a **conventional profit-participating contract**, sitting in the Solvency II
line *insurance with profit participation* [R15], [unverified] as to the line-of-business numbering.
The cross-product reference library records the same question as open — whether German index products
sit inside an *Anlagestock* or in the general account "was not established" [REG-R7] — so this
specification takes the general-account reading, states it as a reading, and notes that the § 125 VAG
*Anlagestock* obligation is triggered by benefits **directly linked** to an index, which a payoff
financed out of declared surplus and payable in euros from the cover pool is not. delib therefore uses
*Indexpolice* / *Indexbeteiligung* for the product and reserves *indexgebunden* for its regulatory sense.

**2. The index participation is a form of *Überschussverwendung*, with no independent statutory
footing.** § 153 VVG gives the policyholder a right to participate in the surplus and in the
*Bewertungsreserven* unless participation is excluded, and requires allocation by a
*verursachungsorientiertes Verfahren* or another comparable appropriate method [R1] [REG-R24]. What the
policyholder is legally entitled to is a **share of surplus**; the AVB then say how that share is
applied, and this product's AVB say it is applied by buying a bounded index-linked payoff for one year.
The *Wahlrecht* is therefore an *Überschussverwendungswahlrecht*, and the *Indexbeteiligung* stands or
falls on the contract clause. **That is the correct legal characterisation and it is not in doubt**
[R1], [unverified] only as to subsection numbering.

**3. The option budget is the declared surplus, and nothing more.** The insurer earns a return on the
*Sicherungsvermögen*; the MindZV forces a minimum share of each result source to the policyholders —
**90 % of the *Kapitalanlageergebnis* after the *Rechnungszinsen* are deducted, 90 % of the
*Risikoergebnis*, 50 % of the *übrige Ergebnis*** [R8] [REG-R18]; the insurer declares an
*Überschussanteilsatz* out of that; and a contract in the index arm has that declared amount **spent on
options instead of credited as interest**. **An Indexpolice therefore does not have a larger risk budget
than a *Klassik* contract of the same vintage — it has the identical budget and spends it differently.**
That is the most under-appreciated fact about the product and it belongs on the first page.

**Why the product exists.** The *Höchstrechnungszins* fell from 4,00 % (1994–2000) through 3,25 %,
2,75 %, 2,25 %, 1,75 %, 1,25 % and 0,90 % to **0,25 % for 2022–2024**, and rose to **1,00 % from
1 January 2025** — the first increase in about thirty years, made by the *Sechste Verordnung zur
Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024, BGBl. 2024 I
Nr. 250 [R7] [R18] [REG-R14] [REG-R15]. At 0,25 % the guaranteed component of a conventional annuity's
return is negligible and the discretionary component is the whole story. An Indexpolice takes that
same discretionary component and, instead of crediting it as a modest certain amount, converts it
into a bounded lottery on an index. **The product is a direct commercial response to a near-zero
guaranteed rate**, and the 2025 rise makes the *sichere Verzinsung* arm relatively more attractive
again; whether observed elections have shifted is [unverified] [R7]. Qualitatively, and not in doubt:
the family emerged in the second half of the 2000s, grew through the low-interest decade as the
guaranteed component shrank towards nothing [R7], became a standard offering across the large and
mid-sized carriers, and was one of the main vehicles of the ***Neue Klassik*** generation [S6] [REG-R53].

**Market size.** There is none to quote: **no published figure for the German index-participation
segment exists**. GDV counts these contracts within conventional annuity business, because that is what
they are [R15] [R19], and index business sits inside *sonstige Lebensversicherungen*, **not separately
visible** [REG-R53]. The frame it sits in: German life premium income (life insurers, Pensionskassen and
Pensionsfonds, GDV basis) was **+2,8 % to 94,6 Mrd. €** in 2024 — *laufende Beiträge* **66,3 Mrd. €**,
roughly flat, *Einmalbeitragsgeschäft* about **+10 % to 28 Mrd. €** — with the contract count **−1,4 %
to 80,3 Mio.**; on the BaFin basis, life-segment *verdiente Bruttobeiträge* were **90,4 Mrd. €**
[REG-R53]. The two measure different populations on different bases and are never combined. The relevant
market rate is the declared one: for 2025 the average *laufende Verzinsung* was **2,53 % Klassik /
2,58 % Neue Klassik**, and the 2026 surveyed averages are mutually incompatible — 2,6–2,7 %, 2,87 % and
2,54 % [R20] [REG-R53]. That declared rate **is** the option budget [R8].

**The same index module is written on four chassis** — *Schicht 3* private annuity (this document),
*Basisrente*, *Riester* and *Direktversicherung* in *bAV* (outside delib). The wrapper changes the
guarantee requirement [R12] [REG-R43], the tax treatment [R13] [R14] [REG-R41] [REG-R45] and the
accessibility of the capital — and **not the index mechanics**.

---

## Representative specification

The representative design is a **composite**, and not one clause of it is quoted from any carrier's
AVB, because none was obtained. The GDV publishes *Musterbedingungen* for the deferred-annuity chassis
but **no model wording for an index-participation module** [S1] — the structural reason the clause set
varies more across insurers here than for any other delib product. Every representative choice below is
argued against the plausible band in *Variations across insurers*.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-life *aufgeschobene Rentenversicherung*, *Schicht 3*, profit-participating, general account; *Neue Klassik* guarantee architecture | [S1] [S6] [R15] |
| Where the capital sits | *Sicherungsvermögen*; no *Anlagestock*, no units, no policy-level asset allocation | [R15] [REG-R7]; reading argued above |
| *Überschussverwendung* | *Indexbeteiligung* or *sichere Verzinsung*, at the policyholder's **annual** election | [R1]; clause-level wording **[std]** (1) |
| Lives basis | Single life; no joint-life form in this family. Sex may not be a rating factor — unisex since 21 December 2012 | [S1]; [REG-R34] |
| *Eintrittsalter* | 25 to 55 | **[std]** (2) |
| *Rentenbeginn* age | 62 to 70; 67 representative | **[std]** (2) |
| *Aufschubdauer* | 12 to 40 years; 12 is the tax minimum | **[std]** (2); [R14] [REG-R45] |
| Age basis | Age last birthday at inception | **[std]** (3) |
| Underwriting | Light or absent — a short declaration or none, the sum at risk before *Rentenbeginn* being small | [unverified]; **[std]** (4) |
| *Garantieniveau* (*Beitragsgarantie*) | **90 % of the *Beitragssumme***, due at *Rentenbeginn* | **[std]** (5) |
| Guaranteed rate (*Rechnungszins*) | **1,00 %** — the *Höchstrechnungszins* for 2025 and 2026 | [R7] [R18] [REG-R14] [REG-R15] |
| Anchor model cell | *Eintrittsalter* 40, *Rentenbeginn* 67, *Jahresbeitrag* 2 400,00 €, annual mode, Cap design, 90 % *Beitragsgarantie*, full index election in every year | **[std]** (6) |

Footnotes to **[std]** rows:

1. **No index AVB was obtained** [S2] [S7] [S8], and the GDV publishes no model clause for the module
   [S1]. The clause set in *Contractual mechanics* below is reconstructed from the mechanics the research
   file establishes, is attributed to **no carrier**, and is labelled a composite wherever used.
2. **No *Produktinformationsblatt* was located** [S3] [S11] [S15], so no entry-age band, minimum
   premium, term band or maximum sum was established for any carrier. The envelope is an uncontroversial
   **[std]** construction: 25–55 is the mid-career segment this product is sold into, 67 is the German
   statutory retirement age, and the 12-year minimum is the tax threshold of § 20 Abs. 1 Nr. 6 EStG
   [R14] [REG-R45] rather than a product limit.
3. The German market's own *Eintrittsalter* convention is frequently the calendar year of inception less
   the year of birth, stepping on 1 January rather than on the birthday. delib runs **age last birthday**
   across all ten products, the registry fixing one age basis for the library; on an annual grid the two
   differ by at most one year, and mortality here is a **timing** rather than an amount assumption.
4. No underwriting rule of any carrier was established; the reasoning is structural. The *Aufschubphase*
   death benefit is a return of capital rather than a sum at risk, so the *Risikoüberschuss* is small and
   § 161 VVG (*Selbsttötung*, three years) is close to inoperative [R6] [REG-R26].
5. Through the 0,90 % and 0,25 % years carriers offered a **choice of *Garantieniveau*** — commonly
   60 %, 80 %, 90 % or 100 % [unverified] — because **every euro of guarantee not promised is a euro that
   can back risk assets, and therefore a larger option budget**. 90 % is the level at which a 1,00 %
   contract can still finance a visible option budget over a 30-year term. **The wrapper decides the
   floor**: a *Riester* variant must guarantee 100 % of contributions and allowances under the AltZertG
   *Beitragserhaltungszusage* and so has the smallest option budget of the four [R12] [REG-R43].
6. *Eintrittsalter* 40 with *Rentenbeginn* 67 gives a 27-year *Aufschubdauer*, long enough for the
   ratchet to compound visibly and short enough to print in one table. The 2 400,00 € *Jahresbeitrag*
   is the research file's 200,00 € per month, taken on the **annual** mode so the anchor is free of the
   *Ratenzahlungszuschlag* and the loading is exercised by the fractionated model points instead.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form | *Laufender Beitrag*, level, over a *Beitragszahlungsdauer* that may be shorter than the *Aufschubdauer*; an *Einmalbeitrag* form exists and *Zuzahlungen* are commonly permitted | [unverified] as to any carrier's menu; form **[std]** |
| Representative premium | **2 400,00 € per year** (200,00 € per month), payable throughout the *Aufschubdauer* | **[std]** (7) |
| Payment frequency and *Ratenzahlungszuschlag* | Annual (no load), half-yearly **2 %**, quarterly **3 %**, monthly **5 %** | menu [unverified]; levels **[std]** (8) |
| *Beitragssumme* | Sum of the premiums payable over the *Beitragszahlungsdauer*, on the **annual-mode** premium — the *Ratenzahlungszuschlag* is a charge for instalments and is not part of it | **[std]** (9) |
| *Dynamik* | Automatic annual increase with a matching benefit increase and a right to decline; each increment is a new tranche with its own guarantee basis | [unverified]; not modeled **[std]** (10) |
| Premium cessation | On death, on surrender, on *Beitragsfreistellung*, and at the end of the *Beitragszahlungsdauer* | [S1] [R3] [REG-R28] |

7. No minimum or maximum premium was established for any carrier [S3] [S15]. 200,00 € a month is a
   plausible mass-market monthly savings premium and is the research file's own **[std]**; the plausible
   band is 50 € to 1 000 € a month.
8. The market convention recorded in the sibling delib research is of this order and is [unverified];
   no carrier's table was seen. It is a **[std]** multiplier on the premium collected.
9. Whether a carrier computes the *Beitragssumme* on the loaded or the unloaded premium was not
   established. delib takes the unloaded reading because the *Beitragssumme* is the base of the
   *Höchstzillmersatz* [REG-R16] and of the *Mindesttodesfallschutz* test [REG-R45], both of which are
   about the substance of the contract rather than how it is billed. The alternative reading raises the
   acquisition charge on a monthly-paying policy by the loading, and is a named pitfall.
10. *Dynamik* is a premium-increase mechanic on an exogenous index, and each increment reopens the
    guarantee basis. Modeling it needs a tranche ledger; the reference implementation has none.

### The index participation module

This is the product, and it is the one table in this document where the mechanics are firm and every
level is **[std]**.

| Parameter | Representative value | Basis |
|---|---|---|
| *Indexjahr* | Twelve months, aligned in the model to the policy year | mechanic [S2] [S5]; alignment **[std]** (11) |
| Observation | The index level is read at thirteen *Beobachtungstage* — one at the start and one per month — and month `m`'s return is `I(m)/I(m−1) − 1` | mechanic firm; convention **[std]** (11) |
| Payoff design | **Cap**: each month's return capped above at `C`, **not floored below**; the twelve summed; the sum floored at zero, never the month | mechanic firm |
| Monthly Cap `C` | **3,00 % per month** | **[std]** (12) |
| *Partizipationsquote* variant | `max(q × (year's index movement), 0)`, no monthly cap | mechanic firm; level **[std]** (13) |
| *Partizipationsquote* `q` | **60 %** on an equity price index; **100 %** on a low-volatility house multi-asset index | **[std]** (13) |
| Base of the participation `G` | The accumulated capital at the **start** of the *Indexjahr*, before that year's premium | **[std]** (14) |
| *Höchststandsicherung* | Whatever is credited is permanently added to the guaranteed capital and enters the base of every later *Indexjahr* | mechanic firm |
| Declared surplus rate `b` (= the option budget) | **2,50 % per year** of `G` | **[std]** (15) |
| *Wahlrecht* | Annual election between the two arms, exercisable without the insurer's consent, without medical evidence and without charge; election as a fraction `w ∈ [0, 1]` of the surplus directed to the index arm | mechanic firm; `w` form **[std]** (16) |
| *Mindest-Cap* | **None** | **[std]** (17) |
| Minimum option budget | **None** — if no surplus is declared the *Indexbeteiligung* buys nothing and the year credits zero whatever the index does | [R1] [R8]; **[std]** (17) |
| Mid-year exit | **No index credit in the year of exit** — death, surrender or annuitisation inside an *Indexjahr* forfeits that year's payoff | **[std]** (18) |
| Index participation in the *Rentenphase* | **None** — the *Wahlrecht* lapses at *Rentenbeginn* | **[std]** (19) |
| Underlying | Parameterised by an explicit monthly-return path with a stated volatility, not by a named index | **[std]** (20) |
| *Ersatzindex* | The insurer may substitute a comparable index on notice if the index ceases to be published, is materially restructured, or ceases to be available on terms on which the hedge can be bought | mechanic firm; procedure **[std]** (21) |

11. Whether the observation dates are calendar month-ends or monthly recurrences of the
    *Indexstichtag*, and whether the level read is a closing level or an average, **were not
    established**. An averaging (Asian) reading lowers the effective volatility and so buys a higher
    Cap out of the same budget, which makes this a calibration question rather than a detail. delib
    aligns the *Indexjahr* with the policy year and reads closing levels, an annual-grid model having
    no other defensible alignment.
12. **No cap level, for any insurer, in any year, was established. Not one.** The documents carrying real
    cap levels are the annual customer notification [S5], the *Standmitteilung* [S10] and the
    rating-house compilations [R21], none of which was reachable. The band quoted throughout — **1,5 % to
    5,0 % per month, typically 2,5 % to 4,0 %** — is the research file's assessment and is [unverified];
    3,00 % is its midpoint. **The Cap is not a free parameter**: given the budget, the index's forward,
    its implied volatility, its dividend yield and the risk-free rate, there is exactly one Cap at which
    the capped-sum payoff costs the budget, and the technical notes must publish that consistency check.
13. 50–80 % on a broad equity price index and 80–120 % on a volatility-targeted house index are the
    research file's assessment and are [unverified]. The Cap design is the base because it is the
    design the product's reputation and its criticism both rest on; the *Quote* is a switchable variant.
14. Three readings of the base are possible — the whole *Deckungskapital* at the year's start, a defined
    index-participating sub-account, or the accumulated *Überschussguthaben* alone — and **none was
    established**. delib takes the whole capital at the start of the *Indexjahr*, **before** that year's
    premium, the natural reading of a payoff struck on a level observed at the *Indexstichtag*. A
    different reading rescales every credit in the model, which is why it is a named model risk.
15. The declared rate **is** the option budget [R8]. 2,50 % is consistent with the 2026 market
    averages above [R20] [REG-R53] and sits inside a 2,0–3,0 % band. It is **exogenous** in the
    reference implementation: the feedback from the *Garantieniveau* through the asset mix to the
    declared rate is real, is the whole design logic of *Neue Klassik*, and is **not modeled**.
16. Whether a carrier permits a split election or requires an all-or-nothing choice was not established.
    delib treats the election as a fraction `w`, making all-or-nothing the special case `w ∈ {0, 1}`. The
    notice period, and — far more consequentially — **whether the Cap is announced before the election
    deadline**, were both unestablished; delib assumes it is.
17. These are different promises: a *Mindest-Cap* bounds the Cap given a budget, a minimum budget
    bounds the budget — and a *Mindest-Cap* is worthless in a year in which no surplus is declared
    [R1] [R8]. **Neither is established for any carrier**, and delib assumes neither.
18. Whether a mid-year exit attracts a pro-rata credit, a refund of the unspent budget, or nothing, **was
    not established**. delib's **[std]** is nothing — the simple treatment and, on the research file's
    understanding, the usual one. It has a behavioural consequence: **the product rewards surrendering
    just after an *Indexjahr* end and penalises surrendering just before one**, so an annual grid with
    exits at year end implicitly assumes the favourable convention.
19. Whether any carrier offers index participation in the payout phase was not established; delib
    assumes not, and that payout-phase surplus is applied to the annuity in payment.
20. **No German house multi-asset index is named anywhere in delib**, because none could be named with
    confidence and a wrong name would be worse than none. The model parameterises the underlying by an
    explicit table of monthly returns with a stated drift and volatility, shipping an equity case, a
    low-volatility house case and an all-zero case.
21. Whether substitution requires an *unabhängiger Treuhänder*'s confirmation, and whether the
    policyholder gets a *Sonderkündigungsrecht* or an unscheduled right to move to the *sichere
    Verzinsung*, were both unestablished; the legal frame is under *Contractual mechanics*.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit at *Rentenbeginn* | The accumulated capital, floored at the **greater of** the *Beitragsgarantie* and the guaranteed capital including every locked-in credit | [R11] [R12]; composition **[std]** |
| Conversion | Lifelong *Leibrente* at the ***greater* of the guaranteed *Rentenfaktor* fixed at issue and the insurer's current factor at *Rentenbeginn*** | chassis fact, two carrier documents in the sibling research; level **[std]** (22) |
| Guaranteed *Rentenfaktor* | **25,00 € per month per 10 000 € of capital** at *Rentenbeginn* 67 | **[std]** (22) |
| *Kapitalwahlrecht* | Lump sum instead of the annuity, exercisable in a window before *Rentenbeginn* | chassis fact; window [unverified] |
| Death benefit in the *Aufschubphase* | The accumulated capital **excluding the running *Indexjahr***, floored at **50 % of the *Beitragssumme*** | [S9] chassis; floor **[std]** (23) |
| *Selbsttötung* | No liability on a death cover within three years of conclusion or reinstatement; the *Rückkaufswert* is then owed | [R6] [REG-R26] |
| *Schlussüberschussanteil* / *Bewertungsreserven* | Half of the *Bewertungsreserven* determined at termination, subject to the *Sicherungsbedarf* restriction | [R1] [REG-R9] [REG-R24]; **not modeled** (24) |

22. Taken over from the sibling *klassische Rentenversicherung* **[std]**; no *Rentenfaktor* level was
    established for any index tariff. The base run sets the current factor equal to the guaranteed one,
    so the max-of-two rule is exercised by a test rather than by the base path. A *Rentenfaktor* is the
    arithmetic image of an annuity table plus a guaranteed rate, and the market-standard table is
    **DAV 2004 R**, a *Generationentafel* in attained age **and calendar year** [REG-R49] — the property
    of the Deutsche Aktuarvereinigung, **not public and not redistributed here**. delib ships **[std]**
    proxies and states what a replacement must preserve.
23. The standard *Todesfallleistung* on this chassis is a return of the accumulated capital [S9]. The
    50 % floor is a **[std]** representative choice with a statutory reason: for contracts concluded from
    1 April 2009 the favourable half-income treatment of a *Kapitalabfindung* requires a
    *Mindesttodesfallschutz* of at least **50 % of all premiums payable over the term**, failing which the
    earnings are taxed in full under the *Abgeltungsteuer* [R14] [REG-R45]. **A model point that would
    fail the German tax test is not representative of a sold contract**, so the floor is on in the base
    run and off on one model point, keeping the plain return-of-capital form testable.
24. The *Bewertungsreserven* leg is path- and balance-sheet-dependent in a way a gross liability
    cash-flow model cannot reproduce, and the *Sicherungsbedarf* test [REG-R9] [REG-R18] has for most of
    the last decade reduced the payable half to zero on high-guarantee portfolios. delib models the
    declared *laufende* surplus explicitly and **excludes** these two components, saying so.

### Charges

Nothing about the charge structure is special; **nothing about its levels was established for any
German index product**, and every charge below is **[std]**.

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* | **2,5 % of the *Beitragssumme***, financed by *Zillmerung*, against a DeckRV § 4 *Höchstzillmersatz* of **25 ‰**, cut from 40 ‰ on 1 January 2015 | **[std]** (25); ceiling [R7] [REG-R16] [REG-R20] |
| Acquisition-cost spread | Over the **first five years** | **[std]** (25); [REG-R28] |
| *Verwaltungskosten*, premium-based `β` | **3 % of each gross premium** | **[std]** (26) |
| *Verwaltungskosten*, reserve-based `γ` | **0,25 % of the *Deckungskapital* per year** | **[std]** (26) |
| *Stückkosten* | **36,00 € per policy per year**, inflating at 1,5 % | **[std]** (26) |
| *Stornoabzug* | **2 % of the *Deckungskapital***, subject to the § 169 Abs. 3 floor | **[std]** (27) |
| Option dealing cost and spread | **Inside the Cap**, not a charge line — a wider spread simply produces a lower Cap | structural (28) |
| House-index level fee and volatility-target drag | **Inside the index**, and therefore inside neither the Cap nor the disclosed costs | structural (28) |
| Dividend yield of a price index | **Not a charge at all**, but a permanent give-up of the same order — of the order of 3 % a year on euro-area equity | [unverified]; structural (28) |
| *Effektivkosten* | Required to be disclosed as the *Minderung der Wertentwicklung* to the start of the payout phase; a validation target, not a model input | [R5] [REG-R31] |

25. **Two different rules with two different functions, and delib keeps them apart: the DeckRV governs
    what the insurer may *reserve*** (the *Höchstzillmersatz*, 25 ‰) [REG-R16], while **§ 169 Abs. 3 VVG
    governs what it must *pay*** — at least the *Deckungskapital* obtained by spreading acquisition and
    distribution costs evenly over the first five contract years [REG-R28]. delib's charge profile uses
    the five-year spread, so the floor is satisfied by construction; it is nevertheless computed and
    applied, so a user who shortens the spread sees it bite.
26. Inherited **[std]** from the sibling delib endowment and classic-annuity products; no charge level of
    any kind was established here [S3] [S4] [S11]. The market frame: the 2024 *Verwaltungskostenquote* was
    **2,4 %** on one measurement and **2,19 %** on another, spread **from under 2 % to over 4 %**
    [REG-R53], and BaFin makes cost a supervisory focus [R16] [R17] [REG-R35] — so a charge
    parameterisation should be plausible against a sector distribution, not merely self-consistent.
27. § 169 Abs. 5 VVG permits a deduction **only if it is agreed, quantified and appropriate**, with the
    burden of proof on the insurer and a deduction for unredeemed acquisition costs expressly
    ineffective [R2] [REG-R28]. The sibling endowment research records one carrier's 5 % base deduction
    plus a capital-market component of 5 %, 10 % or 15 % [unverified]; delib's flat 2 % is a
    conservative **[std]** inside a 0–20 % band.
28. **These three are the index-specific give-ups, and none appears in any charge table**, so the
    disclosed *Effektivkosten* **understate** the economic give-up relative to holding the index by an
    amount disclosed nowhere — a structural fact about the product class, not a claim about any carrier,
    and the most substantive fair-criticism point in this specification.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* | The *Deckungskapital* on the calculation bases of the premium calculation, floored by the five-year-spread *Mindestrückkaufswert*, less the *Stornoabzug* | [R2] [REG-R28] |
| Locked-in credits | **Inside** the *Rückkaufswert* — they are guaranteed capital by then, not a contingent entitlement | [R2]; mechanic firm |
| The running *Indexjahr* | **Not** inside it — the payoff exists only at the year end | **[std]** (18) |
| *Beitragsfreistellung* | Conversion to a paid-up contract at any time for the end of the current insurance period, on the same § 169 value; the index participation continues on the capital and the *Wahlrecht* survives | [R3] [REG-R28]; **not modeled** (29) |
| Premium-default conversion | The insurer's termination converts to *prämienfrei* automatically | [REG-R28] [REG-R30] |
| *Widerruf* / *Kündigung* | 30 days' *Widerruf* for life insurance; *Kündigung* at any time for the end of the current insurance period where *laufende Prämien* are payable | [REG-R23]; [REG-R28] |
| Expiry | There is none — the *Aufschubphase* ends at *Rentenbeginn* with a benefit, not with a lapse | mechanic firm |

29. **German lapse is a three-way decrement** — surrender, *Beitragsfreistellung* and premium-default
    conversion — and the last two keep the policy in force with a reduced benefit and a continuing
    expense loading [REG-R28]. **The reference implementation models surrender only**, because a paid-up
    population's per-policy account diverges from the premium-paying one from the moment of conversion
    and tracking it needs a conversion-cohort ledger. The technical notes say so, state what the paid-up
    path would do, and expose a shortened *Beitragszahlungsdauer* as a model-point column, so the
    deterministic form of the same effect is exercised and tested.

---

## Contractual mechanics

Each subsection states the operative rule, in this document's own words, and says what it does to the
projection. **No sentence below quotes any carrier's AVB**; none was obtained.

### The *Überschuss* as an option budget — the financing identity

Each year the insurer declares an *Überschussanteilsatz* out of the surplus its results and the MindZV
permit [R8] [REG-R18]. In the *sichere Verzinsung* arm that rate is credited to the *Deckungskapital* as
interest, on top of the guaranteed *Rechnungszins*. In the *Indexbeteiligung* arm **the same amount is
not credited — it is spent**, becoming the ***Optionsbudget*** with which the insurer buys, for the
coming *Indexjahr*, the option package replicating the promised payoff. With `G` the participating
capital at the start of the *Indexjahr* and `b` the declared rate:

    option budget                       =  b × G
    price of the promised payoff on G   =  b × G      ← the Cap (or the Quote) is set to make this hold

**The Cap is not a marketing parameter. It is the solution of a pricing equation** — which is why caps
move from year to year with no change in the contract. Two corollaries: an Indexpolice does **not** have
a larger risk budget than a *Klassik* contract of the same vintage; and, priced risk-neutrally, the index
arm is worth exactly what the safe arm is worth, the whole difference being the equity risk premium
earned on the option package's delta, less dealing costs. **The product is a redistribution of one year's
surplus across states of the world, not extra return.** And the budget can be zero: if no surplus is
declared there is nothing to buy an option with, and the year credits nothing whatever the index does
[R1] [R8].

### The annual *Wahlrecht*

The policyholder elects, once a year and for the coming *Indexjahr* only, between *Indexbeteiligung* and
*sichere Verzinsung*. The election is a contractual right, exercisable without the insurer's consent,
without medical evidence and without charge; doing nothing leaves the policyholder in the arm they were
in.

| Arm | The year's surplus is | Outcome |
|---|---|---|
| *Sichere Verzinsung* | credited to the *Deckungskapital* as interest | certain, positive, immediately guaranteed |
| *Indexbeteiligung* | spent on the index option package | zero in a bad year; a multiple of the surplus in a good one; **never negative** |

**Whether the choice is informed depends on a fact nobody established.** The insurer fixes the Cap on
market conditions shortly before the *Indexjahr* starts; the policyholder must elect before it starts.
If the Cap is announced before the election deadline the choice is informed; if after, it is blind.
**Which prevails is not established**, and it is among the most consequential unestablished facts about
this product; delib assumes the Cap is known at election time. The *Wahlrecht* attaches to the capital,
so it survives *Beitragsfreistellung* [R3] and persists to *Rentenbeginn*, ceasing there. In delib's
assumption taxonomy the election is a **behavioural** assumption, not a contractual or an
insurer-discretionary one, and is exposed as a per-year path.

### The *Indexjahr* — the sum of capped monthly returns

**This is the single most important and most misunderstood feature of the product.** The *Indexjahr* is
divided into twelve monthly observation periods. For each month `m` the index level is read at the two
*Beobachtungstage* bounding the month, and

    r(m) = I(m) / I(m−1) − 1
    x(m) = min( r(m), C )              ← capped above at C; NOT floored below
    S    = Σ over m = 1…12 of x(m)     ← summed, NOT compounded
    Indexrendite   = max( S, 0 )       ← the floor is on the YEAR, not on the month
    Indexgutschrift = max( S, 0 ) × G

The three features that define the payoff and must never be separated:

1. **Upside is capped monthly.** A month in which the index rises 8 % contributes `C`, not 8 %.
2. **Downside is not capped at all.** A month in which the index falls 8 % contributes the whole −8 %.
   There is no floor on `x(m)`, only on `S`.
3. **The twelve are summed, not compounded.** Summation is close to compounding for small numbers but
   is not the same, and the contractual formula is a sum.

**Why the asymmetry is the whole story.** The payoff is a *capped cliquet*: the policyholder is long
the index's monthly returns, short a strip of twelve monthly calls struck at `C`, with an annual floor.
Truncating each month's right tail while leaving its left tail intact removes far more expected return
than the cap level suggests. At a monthly standard deviation of 5 % — about 17 % annualised, ordinary
for a broad European equity index — a 3 % cap gives away roughly **one percentage point of expected
return per month**, twelve times a year, against an expected monthly return well under 1 %. The
technical notes do that arithmetic: at those parameters the expected value of a capped month is
**negative**, and the product's positive expectation rests entirely on the annual floor.

**The trap.** The `max(S, 0)` floor operates on the *sum*, not on each month, so it is **not** true that
a year with more up-months than down-months credits something. **It is perfectly ordinary for a year in
which the index finished higher to credit zero** — the research file's constructed Example B is exactly
that case, the index rising 6,44 % and the credit being 0,00 € — and it is a required test.

### The floor and the *Höchststandsicherung*

An *Indexjahr* can never end below zero: `max(S, 0)` is contractual and universal in this family, and it
is the feature the product is sold on. **The floor is what makes it a life-insurance product rather
than a bet**, and it is genuine — the worst imaginable *Indexjahr* credits zero and leaves the capital
untouched. Whatever *is* credited is **locked in**: at the end of the *Indexjahr* the *Indexgutschrift*
is added to the capital and becomes part of the **guaranteed** capital, no longer at risk in any later
year, earning the guaranteed *Rechnungszins* thereafter like any other part of the *Deckungskapital*,
and entering the base `G` of every subsequent *Indexjahr*. That is the ***Höchststandsicherung***, and
it is what makes the year-by-year floor add up to a path-independent guarantee.

Two consequences. **The ratchet is not free**: each year's option package is a fresh strip on a larger
base whenever the previous year credited something — it finances itself automatically, because the
surplus is declared as a *rate* on that same larger base, which is why the financing identity is
written in rates. And **the guarantee is a floor on the path, not only on the maturity value**: under a
plain maturity guarantee the insurer can recover a bad year with a good one, whereas here every credited
amount is permanent, so the guarantee's cost rises with every good year. A **within-year**
*Höchststandsicherung*, locking in the highest level reached inside the year, is a different and rarer
feature; **no German carrier is established as offering it** and delib implements the annual lock-in only.

### The *Partizipationsquote* variant

Instead of capping each month, the contract credits a fixed fraction `q` of the *year's* index
movement, floored at zero: `Indexrendite = max( q × ( I(12)/I(0) − 1 ), 0 )`. There is no monthly cap
and no monthly asymmetry — a down-month is not penalised relative to an up-month because only the
year's net movement matters — and the whole of the give-up is in `q`. **The two designs are not
equivalent and they fail differently.** The Cap design gives away the *large* monthly moves and is hurt
by volatility even when the year ends well; the *Quote* design gives away a constant fraction in every
state. On the research file's Example A the Cap variant credited **more** (8,90 % against 60 % of a
compounded 13,4548 %); on Example B it credited **nothing** while the *Quote* variant credited 60 % of
6,4402 % — the cleanest possible demonstration that the two are not interchangeable.

### The *Cap-Festlegung* — who sets it, when, and on what

The Cap is fixed **by the insurer, for one *Indexjahr* at a time, before that *Indexjahr* begins**, and
is then binding for its whole length, not adjustable during the year. The determination is a pricing
calculation rather than a discretion in substance, and the directions of movement follow from that:

| If this rises | the Cap | because |
|---|---|---|
| the declared surplus rate (the option budget) | rises | more money buys more upside |
| the index's implied volatility | falls | monthly caps are strips of options, and volatility makes them dearer |
| the index's dividend yield | falls | options are written on the price index; a higher dividend yield lowers the forward |
| the risk-free rate | rises, indirectly | it raises the investment return and hence the surplus available |

**The legal frame, and the distinction this product turns on.** The *Cap-Festlegung* is a unilateral
determination by the insurer of a term deciding the policyholder's return for the coming year, and is
therefore reviewable under **§ 315 BGB** for *billiges Ermessen*: a determination made otherwise is not
binding and, on application, is made by the court [R22]. It is **not** an adjustment under **§ 163 VVG**,
which governs changes to the contract's own calculation bases and needs an *unabhängiger Treuhänder*'s
confirmation [R4] [REG-R27]. **Keeping the two apart is the most important legal distinction in this
product and no delib document may blur it**: redetermining the Cap exercises a discretion the contract
confers, while substituting the index or replacing an ineffective clause changes the contract and lives
in the § 163 / § 164 VVG world. **No decided German case on the *Cap-Festlegung* is known**, so the
§ 315 framing, doctrinally sound, is untested in the material available here.

### The underlying index, and the move to house indices

The classic underlying is the **EURO STOXX 50**, and two of its properties drive the economics. It is
quoted and used as a ***Kursindex*** — a price index, dividends excluded — and options are written on
the price index, so the euro-area dividend yield, of the order of 3 % a year [unverified], **never
reaches the policyholder in any state of the world**: a permanent structural give-up on top of the cap,
invisible to a purchaser comparing the product to "the index". And it is volatile, of the order of
18–22 % annualised [unverified], which makes the monthly cap strip expensive and forces the Cap down.

From the mid-2010s a substantial part of the market replaced it with **bespoke multi-asset indices**,
whose common features are: multi-asset composition, so volatility is structurally lower than an equity
index's; **volatility targeting**, a rule scaling exposure to hold realised volatility at a target often
around 5 % [unverified] — the decisive engineering step, because at a 5 % target the option package
costs a fraction of what it costs on a 20 %-volatility index, so the same budget buys a participation
rate near or above 100 %; an **excess-return construction with an embedded fee** of the order of
0,5–1,5 % a year [unverified], which reduces the return without appearing in any cost disclosure; and a
short live history behind a long backtest. **The honest summary**: the shift moved the give-up from
somewhere the purchaser can see — a 55 % participation rate, a 3 % cap — to somewhere they cannot.
Headline numbers improved; expected outcomes did not necessarily improve with them, because the
financing identity still binds. **No specific German house index is named anywhere in delib.**

### The guarantee at *Rentenbeginn* — *Neue Klassik*

What the contract promises is a ***garantiertes Kapital zu Rentenbeginn***, expressed as a percentage
of the premiums paid — the ***Beitragsgarantie*** — plus every index credit locked in along the way,
and a guaranteed *Rentenfaktor* converting that capital into an annuity. **It is not a guaranteed
annual interest rate on the reserve.** That is the defining feature of *Neue Klassik* and the reason
index products are grouped under that label [S6]: by owing the guarantee only at one future date rather
than at every balance date, the insurer can hold a materially riskier asset mix behind it and generate
the surplus that becomes the option budget. **A model that reserves an Indexpolice as though it
guaranteed the *Rechnungszins* every year overstates the guarantee.** The effective guarantee is
`max( Beitragsgarantie on the premiums paid , guaranteed capital including all locked-in credits )`,
with the second term dominating after a few good years. A projection must carry both, and a test must
assert that the guaranteed capital is monotone non-decreasing.

### Premium and the *Beitragssumme*

The premium is level over the *Beitragszahlungsdauer* and payable annually, half-yearly, quarterly or
monthly, with a *Ratenzahlungszuschlag* for anything but annual. **The premium does not enter the index
formula**: premiums build the capital, while the payoff is struck on `G`, the participating capital at
the *start* of the *Indexjahr*, so on the natural reading premiums paid during a year participate only
from the following one. Whether carriers pro-rate them was not established; delib adopts the natural
reading.

### Death before *Rentenbeginn*

The standard *Todesfallleistung* is the **return of the accumulated capital** rather than a sum at risk
[S9], so the *Risikoüberschuss* is small, underwriting is light, and § 161 VVG is close to inoperative
[R6]. The representative design floors it at 50 % of the *Beitragssumme*, for the tax reason at
footnote 23 [R14] [REG-R45]. Whether death mid-*Indexjahr* attracts a pro-rata credit is the same
unestablished question as for surrender, with the same answer: **no credit in the year of exit**.

### *Rückkaufswert* and *Beitragsfreistellung*

Surrender delivers the *Rückkaufswert* under § 169 VVG: the *Deckungskapital* computed by recognised
actuarial rules on the calculation bases of the premium calculation, floored at the value obtained by
spreading acquisition and distribution costs evenly over the first five contract years, less a
*Stornoabzug* effective only if agreed, quantified and appropriate [R2] [REG-R28]. **Locked-in index
credits are inside the reserve and therefore inside the surrender value** — they are guaranteed capital
by then. **The running *Indexjahr* is not**: a surrender in month 7 forfeits that year's payoff.
*Beitragsfreistellung* under § 165 VVG leaves the capital in place, continues the index participation on
it, preserves the *Wahlrecht*, and gives a reduced guaranteed benefit on the same § 169 value [R3].

### *Rentenbeginn* — *Rentenfaktor* and *Kapitalwahlrecht*

At *Rentenbeginn* the capital is converted at `monthly annuity = capital / 10 000 × Rentenfaktor`, and
the applied factor is the **maximum of the guaranteed factor fixed at issue and the insurer's current
factor at *Rentenbeginn*** — a guarantee with upside. **The index mechanic ends here**: the capital is
fixed, the *Wahlrecht* lapses, and payout-phase surplus is applied to the annuity in payment. The
*Kapitalwahlrecht* takes the capital as a lump sum instead. The annuity itself is out of scope for this
model and belongs to `products/sofortrente/`.

---

## Riders and options

**In scope (modeled or parameterized).** The **annual *Wahlrecht***, as a per-year election fraction `w`,
with four shipped paths — always index, always safe, a constant half-and-half split, and a switch from
the index arm to the safe arm mid-term. The **payoff design**, Cap or *Partizipationsquote*, as a
model-point column, so the two can be compared on an identical index path. The **choice of underlying**,
as a model-point key into an external monthly-return table, with an equity case, a low-volatility house
case and an all-zero case. The ***Kapitalwahlrecht***, deciding whether the terminal capital is reported
as a lump sum or as the annuity it buys. The ***Stornoabzug*** and the **50 % death-benefit floor**, as
model-point switches. And the **shortened *Beitragszahlungsdauer***, the deterministic form of
*Beitragsfreistellung*.

**Out of scope, and said so.** ***Beitragsfreistellung*** as a stochastic decrement (footnote 29);
***Dynamik*** (footnote 10); *Zuzahlungen*; the ***Rentengarantiezeit*** and every other payout-phase
feature, which belong to `products/sofortrente/`; ***Hinterbliebenenrente*** and *Beitragsrückgewähr*;
a ***Berufsunfähigkeits-Zusatzversicherung***, a rider on this chassis in the market and a stand-alone
product in delib (`products/berufsunfaehigkeit/`); the *Schlussüberschussanteil* and the
*Bewertungsreserven* share (footnote 24); and a within-year *Höchststandsicherung*.

---

## Variations across insurers

**An honest variations table here is very largely a record of what could not be compared.** No carrier
document was retrieved and no search corroborated any carrier-level term, so what follows is the
*structure* of the comparison a later researcher must fill in, with delib's **[std]** in the last
column. Three product names are given, all [unverified]; **no downstream document may present one as
established, and none may add a fourth**.

| Feature | Allianz [S2] [S3] [S4] [S5] | R+V [S7] | Die Stuttgarter [S8] | Anyone else | delib **[std]** |
|---|---|---|---|---|---|
| Index AVB obtained; product name | no; IndexSelect [unverified] | no; IndexInvest [unverified] | no; index-safe [unverified] | no; not established | composite [S1] |
| Payoff design (Cap / Quote / both) | not established | not established | not established | not established | Cap; Quote as a variant |
| Cap level, any year | **not established** | **not established** | **not established** | **not established** | 3,00 % monthly |
| *Mindest-Cap* guaranteed | not established | not established | not established | not established | none |
| Underlying index | not established | not established | not established | not established | generic, by volatility |
| *Wahlrecht* notice period | not established | not established | not established | not established | annual, at the year end |
| Cap announced before the election deadline | not established | not established | not established | not established | assumed yes |
| Base `G` of the participation | not established | not established | not established | not established | the whole capital |
| *Garantieniveau* menu | not established | not established | not established | not established | 90 % |
| Mid-year exit treatment | not established | not established | not established | not established | no credit |
| Charges / *Effektivkosten* | not established | not established | not established | not established | **[std]**, above |

Parameter bands, restated — **every one [unverified]**, and the reason this specification carries so
many **[std]** rows.

| Parameter | Band | Who sits where |
|---|---|---|
| Monthly Cap | 1,5 % – 5,0 %, typically 2,5 % – 4,0 % | **no carrier placed** |
| *Partizipationsquote* | 50 % – 80 % on an equity price index; 80 % – 120 % on a house index | **no carrier placed** |
| *Garantieniveau* | 60 % / 80 % / 90 % / 100 % of the *Beitragssumme* | 100 % is statutory for *Riester* [R12] [REG-R43]; otherwise not placed |
| Declared surplus rate, 2026 | of the order of 2,5 % – 2,7 %, on incompatible surveyed averages | market-wide [R20] [REG-R53] |
| *Höchstrechnungszins* by cohort | 0,25 % – 4,00 %; **1,00 % for 2025–2026** | market-wide [R7] [R18] [REG-R15] |
| Index volatility (annualised) | 15 % – 22 % equity; 5 % – 8 % house index | **no index named** |
| *Verwaltungskostenquote* 2024; *Ratenzahlungszuschlag* | under 2 % to over 4 %, average 2,19–2,4 %; 2 % / 3 % / 5 % | [REG-R53]; convention [unverified] |
| *Stornoabzug* | 0 % – 20 % of the *Deckungskapital* | one carrier's structure [unverified] |
| *Stornoquote*, market-wide | 1,2 % – 2,7 % on two irreconcilable measures | no index-specific rate exists [R19] |

**What does not vary.** Four things are firm across the family, and they are the reason a composite is
possible at all: the surplus finances the participation rather than sitting beside it; monthly returns
are capped above and not below; the year's sum is floored at zero; and what is credited is locked in
permanently. Everything else above is a level, and no level was established.

---

## Regulatory context

**Contract law — VVG.** The hinge is **§ 153**: the policyholder participates in the surplus and in the
*Bewertungsreserven* unless participation is excluded, and such an exclusion can only be made for the
whole of the profit participation; the insurer must allocate by a *verursachungsorientiertes Verfahren*
or another comparable appropriate method; the *Bewertungsreserven* are recomputed annually and half of
the amount determined is paid on termination, subject to the LVRG's *Sicherungsbedarf* override
[R1] [REG-R24] [REG-R9] [REG-R20]. **§§ 165–170** supply the exit machinery [R2] [R3] [REG-R28].
**§ 163** permits an adjustment of the premium or the benefit where the calculation bases have changed
unforeseeably and not merely temporarily, with an independent trustee's confirmation, and **§ 164**
permits an ineffective clause to be replaced on the same footing [R4] [REG-R27] — the two statutory
channels through which this contract's terms can be changed against the policyholder's will, and
**neither of them is the annual Cap**. **§ 161** excludes suicide within three years, the
*Rückkaufswert* then being owed [R6] [REG-R26]. **§ 155** requires an annual *Standmitteilung* stating
the current status of the policyholder's claims **including profit participation** and disclosing **to
what extent that participation is guaranteed** — which is why a *Standmitteilung* specimen is a
legitimate primary-source class here, and why the research file's gap 4 (no completed *Indexjahr* with
its twelve monthly movements was ever obtained) is its most frustrating absence [S10] [R5] [REG-R25].

**§ 154 and the *Modellrechnung*.** Where the insurer makes quantified statements about possible
benefits beyond the guaranteed ones it must give a *Modellrechnung* on **three** interest rates, which
§ 2 Abs. 3 VVG-InfoV fixes as the *Höchstrechnungszins* × 1,67, that rate plus one point and that rate
minus one point — at a 1,00 % *Höchstrechnungszins*, **1,67 % / 2,67 % / 0,67 %** [R5] [REG-R25]
[REG-R31]. **A *Modellrechnung* for an Indexpolice is intrinsically awkward**, because the interest
assumption drives the option budget, which drives the Cap, which drives the payoff non-linearly. How
German carriers discharge § 154 for this product was **not established**.

**Prudential.** § 124 VAG imposes the prudent-person standard with no quantitative investment limits
since 1 January 2016, and § 125 ring-fences the *Sicherungsvermögen*, requiring a separate *Anlagestock*
section where benefits are **directly linked** to a share index or other reference value [REG-R7].
Buying index options to back an index-participation obligation is the paradigm of a derivative
**hedging a liability the insurer has itself written** — liability and hedge matched by construction,
month for month and cap for cap [R9]. § 139 VAG governs the surplus participation from the supervisory
side and carries the *Sicherungsbedarf* rule [REG-R9]; §§ 140 and 145 govern the RfB [REG-R10]; the
**MindZV** sets the 90 % / 90 % / 50 % minima on the three result sources, deducting the
*Rechnungszinsen* before the 90 % on the investment result — **the guarantee is funded first and only
the excess is shared** [R8] [REG-R18]. The **DeckRV** caps the technical rate and the *Zillmersatz*
[R7] [REG-R14] [REG-R16], and its § 5 Abs. 3 *Zinszusatzreserve* machinery sits behind the declared rate
this product spends [REG-R17]. Above it all is Solvency II [REG-R1] [REG-R2] [REG-R13].

**Conduct and disclosure.** An Indexpolice is a *Versicherungsanlageprodukt* and therefore a **PRIIP**:
a three-page *Basisinformationsblatt* with a summary risk indicator, four performance scenarios and the
cost tables is required [R10] [REG-R32]. It is a **Category 4** PRIIP, part of its value depending on a
factor not observed in the market — the discretionary surplus declaration — for which the DAV has
published a *Standardverfahren* [R11]; Category 4 permits the insurer's own model for that component,
which is why two Indexpolicen with similar mechanics can publish very different favourable scenarios.
**No *Basisinformationsblatt* for any German index product was located**, so neither a charge level nor a
modelled return distribution reached this specification [S4]. The *Effektivkosten* duty [REG-R31] and
**BaFin's *Merkblatt* 01/2023 (VA)** on *angemessener Kundennutzen* [R16] [REG-R35] complete the frame;
whether the *Merkblatt* names index products was not established, though a design that credits zero in a
substantial fraction of years while carrying a full acquisition-cost load is exactly what a
value-for-money regime exists to interrogate.

**Taxation** — context, not a cash flow; delib publishes gross cash flows and computes no tax. A
*Schicht 3* *Leibrente* is taxed only on its ***Ertragsanteil***, a percentage fixed once and for all by
the annuitant's age at *Rentenbeginn* — about 18 % at 65 and 22 % at 60, both [unverified]
[R13] [REG-R41]. A lump sum under the *Kapitalwahlrecht* is taxed on the *Unterschiedsbetrag* between
the payment and the premiums paid; where the contract has run at least **twelve years** and the payment
falls after the **62nd** birthday, **only half** that difference is taxable and at the personal marginal
rate rather than by final withholding, subject for contracts concluded from 1 April 2009 to the **50 %
*Mindesttodesfallschutz*** condition [R14] [REG-R45]. **The index credits are not separately taxed**:
they are absorbed into the capital as credited, so there is no annual tax event, no *Abgeltungsteuer* on
the year's index gain and no *Teilfreistellung* under the *Investmentsteuergesetz* — the last because
there is no fund. **This tax deferral is one of the two genuine advantages over holding an index fund
directly**, the other being the guarantee. Exercising the *Wahlrecht* is not a change of contract and
does not restart the twelve-year clock [unverified]. The duration-12 / age-62 double threshold is the
strongest single driver of German surrender behaviour and shapes the lapse assumption in the technical
notes [REG-R45].

**The criticism, stated fairly, because a specification that omits it is not a specification.** Its home
is the German consumer publishers and trade press — Finanztip [S12], Stiftung Warentest [S13], the
Verbraucherzentralen [S14] and the trade titles [S16] — **none of which was retrieved**, so what follows
is the argument, not a citation of it. The cap's effect on the expected credit is large and is not
disclosed in a usable form: the purchaser is told the cap, is not told the volatility, and cannot do the
calculation. Negative months are uncapped, which is genuinely counter-intuitive. Against a direct index
investment the product loses on every axis but two — it gives up the dividends of a price index and the
tail of every good month, and adds acquisition, administration and possibly index-level costs — but
**what it gives back is real**: the capital cannot fall, credits lock in permanently, the guarantee is
the insurer's, and the accumulation is tax-deferred with a favourable exit. The Cap is redetermined
annually at the insurer's discretion, constrained in principle by § 315 BGB and by no decided case
[R22]; the move to house indices moved the give-up out of sight; and complexity is itself a defect in a
retail product. **The counter-argument, fairly stated**: the relevant benchmark for most purchasers is
not an index fund but the *sichere Verzinsung* arm of the same contract, and against that the index arm
has a higher expected value, cannot do worse than zero in any year, costs nothing extra, and can be
abandoned at any anniversary. The reference implementation lets a reader run that comparison.
