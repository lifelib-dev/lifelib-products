# Product Specification

**Status:** Draft, 2026-08-29 (all sources dated 2026-08-29; **none was retrieved**).

**Scope note.** A *representative composite specification* assembled for reference liability
cash-flow modeling of a German **sofortbeginnende private Rentenversicherung** — the *Sofortrente*:
a single *Einmalbeitrag* (single premium) buys a *Leibrente* (life annuity) that begins at once and
is paid for as long as the annuitant lives. **It is not any single insurer's contract**, and no
clause of any German AVB for this product was read. [S#] tags name primary product documents
(*Verbraucherinformation*, *Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*,
*Basisinformationsblatt*, *Überschussverteilung*) and [R#] product-specific regulatory and actuarial
references, both numbered per `_research/sofortrente.md` and resolved in `sources.md` (frozen, never
renumbered); [REG-R#] tags the cross-product library
`references/regulatory-and-actuarial-references.md`, whose R1–R56 numbering is separately frozen.
**[std]** marks a standardization introduced for the reference implementation, each with a numbered
footnote giving its rationale and, where one exists, the observed range; claims no search
corroborated are flagged [unverified]. German terms of art stay in German, italicised on first use.

**Retrieval conditions, stated first because they govern every line below.** Direct HTTP egress is
blocked by an organisation network policy: `WebFetch` and `curl` are refused with HTTP 403 for
`gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `destatis.de`, `eur-lex.europa.eu` and
every insurer host named here; and the session's 200-call `WebSearch` budget was **exhausted before
work on this product began**, so **not one search was run for the *Sofortrente***. Every source is
therefore either a **known reference** — a document class and carrier that exists and is the right
kind of thing to cite — or a fact carried over with attribution from a sibling delib research file
whose searches ran earlier, principally `_research/klassische_rentenversicherung.md`, which shares
this product's *Rechnungsgrundlagen* (calculation bases), its surplus chassis and, at two carriers,
its tariff. **A delib citation is a pointer, not a certificate.** The consequence: the corpus
establishes this product's **mechanics** well and its **levels** hardly at all, *no annuity rate,
charge, envelope, option menu or surplus declaration having been observed at any German carrier for
any year*. There is therefore **no insurer-level quantitative comparison anywhere below**, the
variations section is structural rather than numeric, and every euro and percentage describing the
representative design is either **[std]** with its derivation printed or tagged to a cross-product
reference.

**Out of scope.** The **accumulation phase** of a deferred annuity is the separate delib product
`klassische_rentenversicherung`; premium accumulation, the *Deckungskapital* recursion, the
*Rückkaufswert*, *Beitragsfreistellung* and the *Kapitalwahlrecht* belong there. **Schicht 1**
(*Basisrente*) and **Schicht 2** (*Riester-Rente*, bAV) run the same payout machinery under
completely different tax rules [REG-R38]. *Fondsgebundene* and *indexgebundene* payout annuities,
*Sterbegeldversicherung*, *Pflegerentenversicherung*, *Gruppenversicherung*, private
*Krankenversicherung* and institutional pension-risk transfer are all outside this file.

---

## Product overview and market role

A *Sofortrente* is an ordinary German **life insurance contract** under the
*Versicherungsvertragsgesetz* (VVG) [REG-R22], written on the insurer's general account
(*Sicherungsvermögen*) [REG-R7], in the classic (*konventionell*) non-unit-linked form [S2] [S6].
Structurally it is one sentence long: **one payment in at inception; a stream of payments out until
death**, floored by a *Rentengarantiezeit* (guarantee period) or a *Kapitalrückgewähr* (refund of
the unconsumed capital on death) and lifted by a declared, non-guaranteed *Überschussrente* (surplus
annuity). What it sells is the transfer of *Langlebigkeitsrisiko* to an insurer. The
*Versicherungsnehmer* contracts and pays; the *versicherte Person* is the life the annuity depends
on; a *mitversicherte Person* may be named for a *Hinterbliebenenrente*; a *Bezugsberechtigter*
receives whatever falls due after death [REG-R26]. Usually the first three are one person; where
they are not, § 150 VVG requires the insured person's written consent above a threshold expressed in
ordinary funeral costs, and the designation is revocable unless made irrevocably [REG-R26].

**Schicht 3, and why the tax rule is the product.** The *Sofortrente* is a third-layer, unsubsidised
private contract in the *Drei-Schichten-Modell* [REG-R38]: nothing is deductible going in, and only
the ***Ertragsanteil*** — a fixed statutory fraction of each payment, set once by the annuitant's
age at *Rentenbeginn* and never changed — is taxable coming out [R13] [REG-R41]. **For an annuity
commencing at 65 that fraction is 18 %** [R13], the only cell of the statutory table any delib
search corroborated. The asymmetry against the subsidised layers is total: a Schicht-1
*Rentenfreibetrag* is frozen in euros for life, so every later increase — including every increase
in the *Überschussrente* — is fully taxable, whereas in Schicht 3 it is the *percentage* that is
frozen, so surplus increases are taxed at the same light rate [REG-R41]. That is the whole economic
case for the product, and the reason it is bought with money already taxed: an inheritance, a
property sale, a matured endowment, a severance payment, or a *Kapitalwahlrecht* lump sum.

**Its structural role: the pricing primitive of every other German annuity.** Two carriers state
independently that the *aktueller Rentenfaktor* at which a deferred contract converts is the tariff
the insurer is then writing **for immediately beginning annuities** — Zurich Deutscher Herold
comparing a second *Rentenfaktor* at *Rentenbeginn* with the guaranteed one and guaranteeing the
higher [S3], and Allianz stating that the calculation bases at *Rentenbeginn* "relate to the
interest rate and mortality table that the company uses at that time for immediately beginning
annuities" [S7]. A model of this product is therefore also the conversion engine of
`klassische_rentenversicherung`, `fondsgebundene_rentenversicherung`, `indexpolice`, `basisrente`
and `riester_rente`.

**Market size.** No figure isolates this product: the GDV series separates *Einmalbeiträge* from
*laufende Beiträge* in new business, but that line aggregates *Sofortrenten* with single-premium
endowments, bAV contributions and *Zuzahlungen* [R25]. On the cross-product aggregates, German life
premium income was **+2,8 % to 94,6 Mrd €** in 2024, of which *laufende Beiträge* were
**66,3 Mrd €**, roughly flat, while the ***Einmalbeitragsgeschäft* grew about 10 % to 28 Mrd €**;
the contract count fell 1,4 % to **80,3 Mio** [REG-R53]. Single premium is now roughly **30 %** of
German life premium income and growing an order of magnitude faster than regular premium — the
structural reason this product is live. **No number of *Sofortrente* contracts, no average
*Einmalbeitrag* and no average purchase age was established** (research gap 7).

**The 2025 interest step, which matters more here than anywhere else.** The *Höchstrechnungszins* —
the statutory maximum discount rate for the *Deckungsrückstellung*, and through § 138 Abs. 1 VAG the
effective cap on a new tariff's technical rate [REG-R8] [REG-R14] — fell for thirty years to
**0,25 %** and rose to **1,00 % on 1 January 2025**, the first increase since 1994 [REG-R15]; the
DAV recommended 1,0 % again for 2026 and 2027 [R8] [REG-R56]. For a deferred contract the rate
matters over a thirty-year accumulation; for a *Sofortrente*, **the rate at which the tariff is
struck fixes the buyer's whole income, permanently, on the day of purchase** — worth about **+10 %**
on the guaranteed annuity at 65 and **+12 %** at 60, tapering to **+6 %** at 80 on the [std]
arithmetic below. The direction falls out of the tariff formula [S6] and the statutory rate history
[REG-R15]; **the magnitude is constructed, not observed** (gap 5).

**What it is bought against.** The standard German comparator is a ***Bankauszahlplan***: the same
capital drawn down at a bank until exhausted. The plan **ends** — 100 000 € drawn at 400 € a month
at 2 % is exhausted after 26,9 years, at about age 92 **[std]** (14) — whereas the annuity does not;
the annuity is taxed on 18 % of each instalment [R13] while the plan's interest is taxable in full;
and the annuitant gives up the capital irreversibly and does badly by dying early. The honest
framing: a *Sofortrente* **is insurance against outliving one's money, priced like insurance**. One
market fact does *not* transfer here: the classic **deferred** annuity was withdrawn by Debeka in
2016 and by Allianz, Zurich and Generali before it [S7] [S8], but **no equivalent retreat from the
immediate annuity was established** — and there is a structural reason not to expect one, the
objection to the deferred contract having been a thirty-year interest guarantee where an immediate
annuity's real risk is longevity, which no design removes. An argument, not a finding (gap 14).

---

## Representative specification

**What "representative" means here.** In the sister libraries a composite is the mode of an observed
range across retrieved carriers. That method is **unavailable** here: the corpus holds two documents
whose titles name the immediate annuity — Zurich Deutscher Herold's *Verbraucherinformation … Sofort
beginnende Rentenversicherung*, Fassung 01/2022 [S2], and NÜRNBERGER's AVB `gn331303_p` [S4] — and
**neither yielded a single clause**. Each value below is argued from one of exactly three things and
the *Basis* column says which: a mechanic the corpus establishes at clause level at a named carrier;
a statutory or professional rule from the cross-product library; or the modeller's construction,
tagged **[std]** with its arithmetic printed. Where the third applies and no observed range exists
the footnote says so in those words: a **[std]** with no range is weaker than one with a range.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium immediate life annuity on the general account, *konventionell*, profit-participating | [S2] [S6]; participation statutory [REG-R24] |
| Legal form | German *Lebensversicherung* under the VVG; *Neubestand* (concluded after 29 July 1994) | [REG-R22]; [REG-R11] |
| Tax layer | Schicht 3 — no *Sonderausgabenabzug*, no *Zulage*, no certification; *Ertragsanteil* on payout | [REG-R38] [REG-R41] [R13] |
| Lives basis | Single life; a second life may be added as a *Hinterbliebenenrenten-Zusatzversicherung* | [S9] |
| Premium form | **One** *Einmalbeitrag*, paid once at inception. No premium stream, no *Beitragsdynamik*, no *Ratenzahlungszuschlag* | [S2] [S6]; structural |
| Entry ages | **60 to 85** | envelope **[std]** (1) |
| *Einmalbeitrag* | Minimum **10 000 €**; working range **25 000 € – 500 000 €**; representative case **100 000 €** | envelope **[std]** (2) |
| *Aufschubzeit* (deferment) | **0 years** representative; **0 to 15 years** offered | **[std]** (3) |
| Underwriting | **None.** No medical evidence, no *Gesundheitsprüfung* | **[std]** (4), [unverified] |
| Sex | Tariff **unisex** for business written from 21 December 2012; the profession's tables are sex-distinct | [REG-R34]; [REG-R49] |
| *Rechnungszins* | **1,00 %** for a 2025 or 2026 contract, at or below the *Höchstrechnungszins* of the contract's own vintage | [REG-R14] [REG-R15]; below-cap pricing observed [S6] |
| Anchor model cell | 100 000 €, annuitant male aged 65 (born 1960), inception 2025, *Rechnungszins* 1,00 %, *Rentengarantiezeit* 10 years, monthly *vorschüssig*, *teildynamische Überschussrente* | **[std]** (5) |

1. **Nothing was established about entry ages at any carrier**; a typical window in the sixties and
   issue into the eighties are [unverified]. **60 to 85** is adopted because below 60 the
   *Ertragsanteil* is high enough (22 % at 60 against 18 % at 65 [REG-R41]) to weaken the tax case the
   product exists for, and above 85 the *Rentengarantiezeit* options collapse — a 20-year guarantee at
   85 costs a quarter of the annuity. The boundaries claim to be no carrier's.
2. **Nothing was established.** The convention is a five-figure minimum, the fixed per-policy
   administration cost swamping a small annuity, with an upper limit set by reinsurance rather than
   tariff. **100 000 €** is the unit German annuities are quoted in — *Rente je 100 000 €
   Einmalbeitrag*, not the *Rentenfaktor* per 10 000 € the deferred market uses.
3. The variant exists but **no carrier's terms, minimum, maximum or deferment death benefit were
   established** (gap 17). The design takes **0** — which is what makes the contract a *Sofortrente*
   rather than a single-premium deferred annuity — and carries the deferment as a model-point column
   so it can be switched on.
4. A *Sofortrente* is normally written **without medical underwriting**, because the exposure runs
   the wrong way: medical evidence would be used by the applicant, not the insurer, so the selection
   sits in the tariff margin rather than in an individual assessment. **No source states this**, hence
   [unverified]; its converse, the impaired-life *enhanced annuity*, is **not established to exist in
   the German retail market**, and § 19 VVG's *Anzeigepflicht* [REG-R30] is inert where the insurer
   asks nothing.
5. Age 65 is where the corroborated *Ertragsanteil* applies [R13] and where the [std] annuity table
   is anchored; the 10-year guarantee sits at the short end of the market's typical band (15 years to
   age 70, 10 thereafter, most choosing 10 to 20 [R23]) so the certain window fits a readable
   worked-example table; and the 2025 inception puts the cell on the current 1,00 % rate [REG-R15].

### Premiums — the *Einmalbeitrag*

| Parameter | Representative value | Basis |
|---|---|---|
| Premium structure | One *Einmalbeitrag* at inception; **one inflow, at `t = 0`** | [S2] [S6]; structural |
| *Nettoeinmalbeitrag* | `Einmalbeitrag × (1 − α)`. Debeka's definition of the accumulation quantity — the *Deckungskapital* is the sum of contributions accumulated at the *Rechnungszins* insofar as they are not required for risk and expense cover [S8] — collapses for a single premium into exactly this netting step | [S8]; α **[std]** (6) |
| Acquisition loading α | **2,5 %** of the *Einmalbeitrag*, taken once | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| *Zillmerung* | **Does not apply.** § 4 DeckRV caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme*; there is no premium stream to amortise against | [REG-R16]; structural |
| Further premiums | **None.** No *Zuzahlung* in the representative design | **[std]** (7) |
| Cancellation | *Widerrufsrecht* of 30 days for life insurance, against 14 days generally | [REG-R23] |

6. **No charge parameter was established at any carrier** — not the *Abschluss- und
   Vertriebskosten*, not the administration loading, not an *Effektivkosten* figure [REG-R31], not a
   *Renditeminderung* [REG-R32] (gap 8). The product has exactly three charge points, fewer than any
   other delib product: an acquisition charge on the *Einmalbeitrag*, taken once; a running loading
   on each annuity payment, covering the payment run, the annual *Standmitteilung* [REG-R25] and
   proof of life; and an implicit margin inside the *Rechnungsgrundlagen*, pricing at 0 % when the
   cap is 1,00 % [S6] [REG-R14] being a charge in economic substance. α = 2,5 % is argued from a
   single-premium annuity's cost base — a one-off commission plus issue expense, materially below the
   *Zillmerung* of a recurring-premium contract; β = 2,0 % from a per-policy running cost roughly
   constant in euros, which is why 2 % is of the right order on a 100 000 € case and too small on a
   25 000 € one, itself the reason minimum *Einmalbeiträge* exist. **Both are the modeller's view with
   no observed range, because nothing was observed.** The only market benchmark is an insurer-level
   *Verwaltungskostenquote* of 2,4 % or 2,19 % depending on measurement, spread from under 2 % to over
   4 % [REG-R53] — a ratio on premium income, not a product charge.
7. Whether carriers permit a *Zuzahlung* after inception **was not established**. Economically a
   top-up is a second annuity purchase at the then-current tariff, and the design treats it that way
   by excluding it: a second *Einmalbeitrag* is a second model point.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Main benefit | A *Leibrente*: a level **guaranteed** monthly annuity for as long as the annuitant lives | [S6] [S7] [R23] |
| Determination | `R = Einmalbeitrag × (1 − α) / (12 × a12(x, i) × (1 + β))`, `a12` the monthly annuity-due factor at attained age x and *Rechnungszins* i on the **first-order** DAV 2004 R basis for the annuitant's birth cohort | [S6] [R10]; α, β **[std]** (6) |
| Guarantee | The *garantierte Rente* is guaranteed **for life** and is not adjustable; § 163 VVG is the only channel and it is narrow | [S6]; [REG-R27] [R4] |
| Payment frequency | **Monthly** standard; quarterly, half-yearly, annual exist | [S7] [R23]; others [unverified] |
| Payment timing | ***Vorschüssig*** — in advance; first instalment at inception | **[std]** (8) |
| *Überschussrente* | Declared annually out of surplus actually earned; **not guaranteed and reducible** | [R19] [R20] [R21] [R23]; levels **[std]** |
| *Überschussverwendung* | Four forms — *konstant*, *teildynamisch*, *volldynamisch*, *Bonusrente* — elected at *Rentenbeginn*, here at inception, once | [R19] [R20] [R21] [R23]; irrevocability [unverified] |
| *Bewertungsreserven* | Participation **continues during the annuity payment period**, currently *hälftig* under § 153 Abs. 3 VVG | [S3]; [REG-R24] |
| *Rentengarantiezeit* | **10 years** representative; 5 / 10 / 15 / 20 / 25 / 30+ offered, or none | [R23] [S5] [S7]; choice **[std]** (5) |
| Death inside it | The annuity **continues to the beneficiaries** until the agreed number of years has expired | [R23] |
| Death after it | **Nothing is payable** unless a *Kapitalrückgewähr* or *Hinterbliebenenrente* was bought | [R23]; structural |
| *Kapital-/Beitragsrückgewähr* | Optional: the *Einmalbeitrag* **less the instalments already paid**, floored at zero | [R23]; measured against the **guaranteed** annuity **[std]** (9) |
| *Hinterbliebenenrente* | Optional rider: 60 % or 100 % to a named second life, for that life's remaining lifetime | [S9]; percentages [unverified] |
| Capital option | **None** after *Rentenbeginn*; the annuity may not be commuted at the policyholder's election | [R1]; [REG-R28] |
| Settlement on death | To the *Bezugsberechtigter*, not automatically to the estate | [REG-R26] |

8. **The payment timing was not established by any source in the delib corpus**, for this product or
   the deferred one, and it is first-order: advance against arrears moves the annuity value by roughly
   half a month's interest *and* shifts every payout cash flow by one period. On the [std] basis at
   1,00 %, `a12_due − a12_arrears = 1`, so the annuity per 100 000 € at 65 would be
   `100 000 / (12 × 19.426) = 428,99 €` in arrears against **407,98 €** in advance — **5,1 %** from a
   single convention. *Vorschüssig* is adopted **[std]** as the German market convention and because
   every arithmetic in the research file uses an annuity-due, but it is a convention stated as one,
   not a finding (gap 11); the first payment date was likewise not established.
9. **Whether the refund counts the *guaranteed* or the *total* annuity paid is a live contractual
   question, not established at any carrier**, and the readings diverge materially over twenty years.
   The design measures it against the **guaranteed** annuity, on the argument that a guaranteed
   benefit cannot be defined by reference to a discretionary quantity (gap 10).

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Medical evidence | **None** | **[std]** (4), [unverified] |
| Rating factors | Attained age at *Rentenbeginn*; birth cohort; the elected options; the *Einmalbeitrag*. **Sex may not be a rating factor** for business written from 21 December 2012 | [S6]; unisex [REG-R34] |
| Mortality basis | **DAV 2004 R**: the annuity factor is calculated "on the basis of a recognised mortality table (currently DAV 2004 R) and an underlying interest rate (currently 0 percent p.a.)" — quoted from a search summary of [S6], not from the document | [S6] [R10] [REG-R49] |
| Table type | A ***Generationentafel*** — a two-dimensional basis `q(x, τ)` in attained age and calendar year, **not** a period table; the improvement is **inside** the table | [R10] [REG-R49] |
| First against second order | First-order probabilities carry safety margins relative to the second-order ("realistic") ones. For an annuity, prudent means **lighter** mortality **and a stronger improvement trend** — safety in two dimensions | [R10] [REG-R47] |
| Interest basis | The insurer's own choice **at or below** the cap, never automatically the cap; **0 % p.a.** observed at one carrier at an unestablished vintage | [S6] [REG-R14] |
| Anti-selection | Real, and not underwritten away; the table is understood to carry ***Selektionsfaktoren*** for exactly that | [REG-R49]; [unverified] |
| *Altersverschiebung* | DAV 2004 R carries an age-adjustment component; **its convention was not established** | [R10]; gap 12 |

**What delib ships instead of the table.** DAV 2004 R and DAV 2004 R-Bestand are the property of the
Deutsche Aktuarvereinigung, distributed to members rather than published, and **not
redistributable**; `delib` ships **no version of either** and quotes no `q_x`, no improvement rate
and no annuity factor from them [REG-R47] [REG-R49]. The decrement CSV shipped with `Sofort_DE_S` is
a **[std] proxy**, anchored so the worked example reproduces exactly, and **a replacement must
preserve three things**: the **generational** structure — a `q(x, cohort)` surface, because a
period-table proxy applied to a forty-year annuity understates the liability by a margin that dwarfs
every other assumption in the model [REG-R49]; the **first-order margin in both dimensions**, level
and trend [REG-R47]; and the *Altersverschiebung* convention [R10]. Destatis's
*Generationensterbetafeln* are the free public analogue and the intended base [REG-R52]. Of the
*Bestand* variant **nothing beyond the pairing was established** (gap 12) — though it matters here, a
*Sofortrente* being priced once on the new-business table and then spending thirty years in the
*Bestand*.

**The unisex tension bites harder here than on any other delib product.** German annuity tables are
built sex-distinctly while a tariff sold since 21 December 2012 must be unisex [REG-R34] [REG-R49],
and a *Sofortrente* is the purest longevity bet in the market, so a unisex tariff must be struck on
an **assumed portfolio sex mix no insurer publishes**. The realised mix drives the *Risikoergebnis*
the MindZV then shares [REG-R18], and the reference implementation's decrement table is a **unisex
[std] proxy** with a stated mix assumption, described as one (gap 13).

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* α | **2,5 %** of the *Einmalbeitrag*, once | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| *Stornoabzug* | **None, ever.** § 169 Abs. 5 VVG permits a deduction only where agreed, quantified and appropriate — and there is no surrender to deduct from | [REG-R28]; structural |
| *Effektivkosten* (VVG-InfoV) | **Not established** for this product at any carrier | [REG-R31]; gap 8 |
| *Renditeminderung* (PRIIPs) | **Not established**, and whether a payout-only *Sofortrente* is within PRIIPs scope is itself unresolved | [S12] [REG-R32]; gap 8 |
| Effect of both [std] charges | On the [std] gross annuity of 407,98 € at 65 and 1,00 %: `407,98 × 0,975 / 1,02 = 389,99 €` per month per 100 000 €; a 10-year guarantee takes it to about **381 €** | **[std]** (10) |

10. A **constructed illustration**, not a market rate: printing the construction is the only honest
    alternative to printing a fabricated quotation, and **no German carrier's quotation, at any age,
    for any year, appears anywhere in this specification** (gap 5). BaFin's *Merkblatt 01/2023 (VA)*
    on *Wohlverhaltensaufsicht* — which polices *Effektivkosten* against a sector comparison and
    requires a return target for the target market [REG-R35] — **is addressed to *kapitalbildende*
    products**, and whether the supervisor scrutinises *Rentenhöhe* or surplus declarations on a
    payout annuity **was not established** [R18].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender (*Rückkauf*) | **None once the *Rentenbezug* has begun.** For a *Sofortrente*, whose *Rentenbeginn* is at or within weeks of inception, **the contract is irrevocable from the outset** | [R1] [R2] [REG-R28]; see the discrepancy note |
| *Rückkaufswert* | **None.** § 169 VVG is displaced: no surrender-value table, no *Stornoabzug*, no five-year cost-spreading rule to implement | [R2] [REG-R28] |
| Lapse | **None.** A policyholder cannot lapse a contract they cannot terminate and on which no premium is due | [R1]; structural |
| *Beitragsfreistellung* | **None.** § 165 VVG has no application: there is no premium to stop | [R5] [REG-R28] |
| Termination of the contract | On the annuitant's death, subject to any *Rentengarantiezeit* still running, any *Kapitalrückgewähr* then due and any *Hinterbliebenenrente* then beginning | [R23]; structural |
| Insolvency of the insurer | Contracts transfer to **Protektor Lebensversicherungs-AG**, the statutory *Sicherungsfonds* | [REG-R12] |
| *Aufschubzeit* qualification | A deferment gives a pre-*Rentenbeginn* window in which the bar does not yet bite, so a surrender right **may** exist. **No carrier's terms established**; the base run switches the variant off | [R1] [R2]; gap 17 |

**A discrepancy between two delib documents, named rather than resolved.** The research file states
that **§ 168 Abs. 3 VVG** confines the right of termination in a *Rentenversicherung ohne
Kapitalwahlrecht* to the period before the annuity payments start [R1], flagging the paragraph number
as [unverified] (gap 9); the cross-product library, from nine queries touching §§ 165–170, reports
**§ 168 Abs. 3** as the carve-out excluding Abs. 1 and 2 for a *Basisrentenvertrag* certified under
§ 5a AltZertG and where realisation before retirement was irrevocably excluded [REG-R28]. **Neither
was read at article level.** The readings are not necessarily inconsistent — one *Absatz* may carry
more than one exclusion — but the corpus cannot choose between them and this specification does not
pretend to. What matters is the **substance**, on which both entries, the consumer literature [R21]
[R23] and the economics agree: **once the *Rentenbezug* has begun there is no termination right and
no *Rückkaufswert*.** A surrenderable life annuity would be surrendered by exactly those annuitants
expecting to die soon, leaving the insurer with the long-lived; the bar is what makes the mortality
pooling possible. Consequently `Sofort_DE_S` publishes **no surrender-value cells, no lapse
decrement, no paid-up state and no *Stornoabzug***; the only decrement is **death**, and the
behavioural assumption set every other delib product needs is **empty** — a **specification, not a
simplification**.

---

## Contractual mechanics

### The *Einmalbeitrag* and the *Nettoeinmalbeitrag*

**The rule.** The insurer deducts the acquisition and distribution loading and annuitises the
remainder: `Nettoeinmalbeitrag = Einmalbeitrag × (1 − α)` [S8]. **What it does:** it fixes, once and
for all, the capital the annuity is struck against — no later accumulation, no *Beitragsdynamik*, no
second netting, so everything downstream is a division of this one number by an annuity factor. It
is also the whole of the product's new-business strain, the acquisition cost falling at `t = 0`
against a single inflow, so the first period carries a large positive `net_cf` and every later
period a negative one.

### *Rentenhöhe* — how the guaranteed annuity is struck

**The rule.** `R_garantiert = Einmalbeitrag × (1 − α) / (12 × a12(x, i) × (1 + β))`, with `a12(x, i)`
the monthly annuity-due factor at attained age `x` and *Rechnungszins* `i` on the **first-order**
DAV 2004 R basis for the annuitant's birth cohort [S6] [R10]. **It settles three things.** The
**mortality basis is DAV 2004 R**, named in an insurer's own AVB [S6]. The **interest basis need not
be the *Höchstrechnungszins***: the same clause continues "and an underlying interest rate (currently
0 percent p.a.)" [S6] — a carrier pricing a *guaranteed* factor at zero while the statutory maximum
was positive, the *Sicherheitszuschlag* made concrete on the interest side, establishing that the
tariff rate is the insurer's choice **at or below** the cap. And the factor is **fixed at
inception**, here once and never revisited, inception and *Rentenbeginn* being the same date.

**The [std] annuity table.** No annuity level was established at any carrier for any year, so the
research file **constructs** one on a stated Gompertz–Makeham proxy `mu(x) = A + B·c^x` with
**A = 0,0002**, **B = 1,5 × 10⁻⁵**, **c = 1,10** — life expectancy 24,29 years at 65, `q(65) =
0,00789`, `q(75) = 0,02001`, `q(85) = 0,05078` — a **prudent annuitant** shape of the right order for
a first-order German basis, and **not** DAV 2004 R [R10]. Monthly-in-advance via
`a12 = a_due − 11/24`; charges excluded. Gross annuity per 100 000 €, monthly in advance
**[std]** (11):

| Age at *Rentenbeginn* | 60 | 65 | 70 | 75 | 80 |
|---|---|---|---|---|---|
| i = 0,25 % | 314.43 | 369.64 | 443.58 | 544.89 | 687.02 |
| i = 1,00 % | 352.08 | 407.98 | 482.84 | 585.32 | 728.86 |
| i = 1,75 % | 391.63 | 447.93 | 523.40 | 626.75 | 771.44 |
| `a12` at 1,00 % | 23.669 | 20.426 | 17.259 | 14.237 | 11.433 |
| uplift 0,25 % → 1,00 % | +12.0 % | +10.4 % | +8.9 % | +7.4 % | +6.1 % |

Any cell checks as `100 000 / (12 × a12)`.

11. **[std]**, reproducible from the printed parameters, and **not any carrier's quotation.** Two
    forces move a real tariff away from it in both directions — carriers price below the cap [S6],
    and their first-order margin differs from this proxy — and two move it over time: improvement
    inside the *Trendfunktion* raises annuity values for each successive cohort, and any strengthening
    of the first-order margin does the same [R10] [REG-R49]. **Two cohorts buying ten years apart at
    the same *Rechnungszins* would not get the same annuity.**

**What is guaranteed.** The *garantierte Rente* is guaranteed **for life** and is not adjustable.
§ 163 VVG is the only channel for changing a term after conclusion and needs three cumulative
conditions — a change in the *Leistungsbedarf* that is neither temporary nor foreseeable, a new term
appropriate and necessary to secure permanent fulfilment, and an independent *Treuhänder*'s
confirmation — while excluding adjustment to the extent the benefits were insufficiently calculated
in the first place [REG-R27]; the Landgericht Köln held the low-interest phase **not** a sufficient
ground, being entrepreneurial risk (case reference not established) [R4]. A delib model treats the
*garantierte Rente* as **immutable** and records § 163 as a model risk.

### *Rentengarantiezeit*

**The rule.** A guaranteed payment period runs from *Rentenbeginn*. **If the annuitant dies inside
it, the annuity continues to be paid to the beneficiaries until the agreed number of years has
expired** — the corpus's illustration is a 10-year period with death after six years, the spouse
receiving the remaining four [R23]; if the annuitant survives it, it lapses silently. **What it
does:** it converts the first `n` years from a contingent payment into a **certain** one, which is
the whole modelling consequence — during the guarantee the payment must **not** be decremented for
survival, and after it, it must be. A model applying survival probabilities across the whole stream
understates the liability; one applying none overstates it.

**Where it sits in the market.** A tariff-level design feature carried in the product name at
NÜRNBERGER — "… mit aufgeschobener Rentenzahlung **und Rentengarantiezeit** nach Tarif NIR3301"
[S5] — and a selectable parameter with a contractual floor at Allianz, where the period "can be set
to a minimum" [S7], so a *Sofortrente* with **no** guarantee period is a configuration, not the
default. Durations offered are **5, 10, 15, 20, 25 or more than 30 years**, typically **15 years for
retirement ages 61–70 and 10 years for 71 and above**, **most choosing 10 to 20** [R23]. What it
costs, on the [std] basis at 1,00 %, age 65, per 100 000 € **[std]** (12):

| *Rentengarantiezeit* | none | 5 y | 10 y | 15 y | 20 y | 25 y | 30 y |
|---|---|---|---|---|---|---|---|
| `a12` | 20.426 | 20.530 | 20.897 | 21.624 | 22.821 | 24.591 | 26.972 |
| Monthly annuity | 407.98 | 405.92 | 398.78 | 385.38 | 365.16 | 338.87 | 308.97 |
| Reduction | — | 0.51 % | 2.26 % | 5.54 % | 10.50 % | 16.94 % | 24.27 % |

12. **[std]**, same basis, `a12` replaced by an annuity-certain-due of `n` years plus an
    `n`-year-deferred life annuity. **The cost rises steeply with age, because the guarantee bites
    sooner**: a 10-year guarantee costs 2,26 % at 65, 4,10 % at 70 and 7,42 % at 75, a 20-year one
    10,50 %, 17,20 % and 26,71 % — which is why the market's typical duration falls with age [R23].
    The corpus's consumer illustration on a *deferred* contract puts the same three at roughly 0,5 %,
    2,6 % and 8,0 % [R23]: consistent in shape, different in level, **neither a tariff**.

**Two settlement forms exist and only one is modelled.** On death inside the period the instalments
may continue as they fall due, or the *Restgarantiezeit* may be commuted; **which form German
carriers use, and on what basis, was not established** (gap 10), and the model pays the instalments.

### *Kapital-* und *Beitragsrückgewähr*

**The rule.** On death the insurer refunds the *Einmalbeitrag* **less the annuity instalments already
paid**, floored at zero — so the benefit starts at the full *Einmalbeitrag* and runs to nothing over
roughly the period in which the annuitant recovers the capital nominally, on the [std] basis about
**21,5 years** at 65. **The trap inside it:** a *larger* refund means a *smaller* annuity, and a
smaller annuity means the refund runs off more slowly, so the pricing equation is **implicit in R**:

    Einmalbeitrag = 12 × R × a12(x, i) + PV( max(Einmalbeitrag − 12 × R × t, 0) payable on death at t )

It must be **solved**, not evaluated: computing the plain annuity first and then subtracting a refund
cost gets a different — and wrong — answer. On the [std] basis at 1,00 %, age 65, per 100 000 €, the
monthly annuity falls from **407,98 €** to **335,48 €**, **−17,8 %** **[std]** (13) — materially more
than a 20-year guarantee period, and the honest answer to a buyer who asks why the "money-back"
version pays so much less.

13. **[std]**, solving the equation above with deaths at mid-year and the refund discounted from
    mid-year. Market variants — ***volle Beitragsrückgewähr***, a stated percentage, a refund capped
    at a number of years' payments — exist, but **no carrier's variant was established.** The refund
    and the *Rentengarantiezeit* protect the same risk in different shapes and are usually offered as
    alternatives; **which carriers permit the combination was not established** (gap 10), so the design
    treats them as **mutually exclusive [std]** and the model asserts that exclusivity rather than
    silently permitting an unsupported configuration.

### *Hinterbliebenenrente* and its *Anwartschaft*

**The rule.** A second life — the *mitversicherte Person* — is named at inception. While the
annuitant lives, the main annuity is paid and the second life holds an ***Anwartschaft***: a
contingent, not-yet-payable entitlement. On the annuitant's death, if the second life is then alive,
the *Hinterbliebenenrente* begins at a stated percentage and is paid for that life's remaining
lifetime. **If the second life predeceases the annuitant the entitlement lapses and nothing is
refunded** — the cover has been consumed. **What it does:** it makes the contract a
**joint-life-last-survivor** annuity, the liability running
until *both* lives are dead, so the second life's age and sex matter as much as the annuitant's, and
that life is fixed at inception [unverified]. The German market treats the survivor's annuity as a
***Zusatzversicherung*** — a rider with its own condition set — and the GDV publishes model
conditions for exactly that [S9], so in the reference implementation it is a **separate module with
its own insured life, off in the base run**. Typical percentages are **60 % and 100 %** [unverified]; **no
carrier's menu was established**. On the [std] basis at 1,00 %, annuitant 65 and second life 62 on
the same mortality, per 100 000 € **[std]** (14): 60 % gives `a12` 23.838 and **349,58 €**, −14,3 %;
100 % gives `a12` 26.113 and **319,12 €**, −21,8 %.

14. **[std]**, applying the same mortality to both lives and assuming independence — real joint-life
    pricing uses sex-distinct or portfolio-mix bases and a dependence allowance. The overview's
    payout-plan exhaustion figures are on the same basis.

### Payment frequency and timing

**The rule.** The annuity is **monthly** [S7] [R23] and ***vorschüssig*** — payable in advance, at
the start of each payment period — with the first instalment at or within a month of inception;
quarterly, half-yearly and annual frequencies exist as options [unverified]. **What it does:** it
fixes the grid of the whole model, a monthly-in-advance stream being an annuity-**due**. **No source
in the delib corpus states the timing convention in terms**, so *vorschüssig* is a **[std]**
convention with the gap stated beside it — worth about 5 % of the annuity (footnote 8, gap 11); nor
was any loading for a non-monthly frequency established.

### *Überschussbeteiligung* in the *Rentenbezug*

**The rule.** The annuity paid is `garantierte Rente + Überschussrente`. Only the first is a promise;
the second is declared annually out of surplus actually earned and **can move down as well as up**.
Participation is a **statutory right, not a marketing feature**: § 153 VVG entitles the policyholder
to a share of the *Überschuss* and of the *Bewertungsreserven* unless excluded by express agreement,
names the principle — a *verursachungsorientiertes Verfahren* — and **does not prescribe the
algorithm**, which is precisely why every level below is **[std]** [REG-R24]. It **does not stop at
*Rentenbeginn***: Zurich Deutscher Herold's deferred pack states that policyholders **also
participate during the annuity payment period**, § 153 Abs. 3 VVG currently providing *hälftige*
participation [S3] [REG-R24] — the only clause-level evidence in the delib corpus for that, and
load-bearing for this section.

**The four *Überschussverwendung* forms**, elected at *Rentenbeginn* — here at inception, once,
irrevocably [unverified]:

| Form | Mechanic | Payment stream |
|---|---|---|
| ***konstante Überschussrente*** | The insurer fixes the total annuity at *Rentenbeginn* from the *garantierte Rente* plus a surplus share **projected for the whole annuity period**, and intends to hold it level [R21] | Highest at outset; flat thereafter **in intention only** |
| ***steigende (volldynamische)*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R21] | Lowest at outset; rises each year surplus is declared |
| ***teildynamische*** | Part of the expected surplus is applied under the constant system and part under the dynamic one, so the annuity rises by a **fixed percentage** provided the insurer earns corresponding surpluses [R21] [R23] | Intermediate at outset; rises at a stated rate, subject to surplus |
| ***Bonusrente*** | Declared surplus **buys a paid-up increment of annuity**, permanently added to the payment [R23] | Ratchets: each increment, once bought, does not come off |

**The *Bonusrente* is the mechanism underneath the rising forms, not a fourth alternative** [R23]:
what makes a *volldynamische Rente* **ratchet rather than fluctuate** is that its increments are
bought as paid-up annuity, so a model treats it as the crediting mechanism and the three dynamics as
the profile. **The single most important thing to understand about this product: the constant form is not
constant.** The total annuity under it is set from a **projection** of surplus over the whole
remaining lifetime; if the insurer earns less than projected, **the annuity is reduced** [R21]. Only
the *garantierte Rente* inside it is guaranteed, and the gap between the two — on typical market
designs of the order of 15 % to 25 % of the payment [unverified] — is the amount at risk. The
trade-off across the four forms is one of timing, not of amount: the constant form front-loads the
same expected surplus and carries reduction risk, the volldynamic form back-loads it and carries the
risk of dying before collecting. Franke und Bornberg titled its treatment "Die Qual der Wahl" [R20].

**Nothing about the level was established** — no *Überschussrentensatz*, no *laufende Verzinsung*, no
*Zinsüberschussanteil* on the *Deckungsrückstellung* of annuities in payment, no dynamic percentage,
at any carrier, for any year (gap 4). [S10] establishes the document class that publishes them,
current to 2026, and [R22] the 24th edition of the study that aggregates them; nothing inside either.
The cross-product library's accumulation-side average must be read carefully: the German declared
rate is the ***laufende Verzinsung***, the *Garantieverzinsung* **plus** the *laufende
Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee** — 2,53 % Klassik / 2,58 %
Neue Klassik for 2025, with three incompatible figures for 2026 [REG-R53]. Adding a declared rate to
a guaranteed rate is the commonest arithmetic error in describing a German contract.

### Where the surplus comes from

**Three sources, unequally important for an annuity in payment.** The ***Zinsüberschuss*** — actual
investment return over the *Rechnungszins* on the *Deckungsrückstellung* — dominates, the reserve
being large from day one and running off slowly over decades. The ***Risikoüberschuss*** is, for an
annuity, a **longevity** result: positive when annuitants die **faster** than the first-order table
assumed, negative when they live longer, and the one source that can go the wrong way for a whole
cohort at once. The ***Kostenüberschuss*** is small. The statutory floor beneath the insurer's
discretion is the MindZV's 90 / 90 / 50 and the RfB machinery above it, under *Regulatory context*.

**The competition for the same money is first-order here.** The *Überschussrente* is paid from the
same *Rückstellung für Beitragsrückerstattung* that financed the ***Zinszusatzreserve*** (ZZR), the
additional HGB reserve arising when the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's
tariff rate [REG-R17]; the build-up suppressed declarations across the market for a decade and the
release should work the other way. On trade-press figures — **never a supervisory source** — the ZZR
stood at about **84 Mrd €** at the 2024 balance-sheet date against a **96 Mrd €** peak at end-2021,
**2024 was the first year since introduction in which insurers had to add nothing at all**, and about
5 Mrd € flowed back with a further 4 Mrd € for 2025, reaching policyholders **through a higher
*Überschussbeteiligung*** [REG-R17]. That release profile is the largest single driver of what a
German annuitant cohort will actually receive over the next decade, and a model projecting a flat
surplus rate is ignoring it.

### The *Aufschubzeit* variant

**The rule.** The *Einmalbeitrag* is paid now and the annuity begins **after a short deferment**,
typically one to fifteen years. **No carrier's terms were established**; the Mecklenburgische "Rente
flex" is the corpus's only candidate and its feature is unestablished [S14]. **What it does — three
things at once, which must not be conflated:** interest accrues at the
*Rechnungszins*, so more capital is annuitised; **mortality accrues**, so survivors share the fund of
those who died — the survivorship credit that makes deferral powerful, and the reason the deferment
death benefit is a first-order design question; and the annuity starts at an older age, so `a12` is
smaller for two reasons at once. Two death-benefit forms exist — a **pure deferred annuity** with no
death benefit, and a *Beitragsrückgewähr* form refunding the *Einmalbeitrag* on death before
*Rentenbeginn*, much the more common retail form — and **neither was established for this product**.
On the [std] basis at 1,00 %, age 65, 100 000 €, a five-year deferment raises the monthly annuity
from 407,98 € to **532,48 €** without a deferment death benefit and **508,12 €** with full
*Beitragsrückgewähr* — about +31 % and +25 %, the 4,6 % gap between them being **the price of the
death benefit**, widening to 11,1 % at ten years **[std]** (15: same basis, gross of charges).

### No surrender, no lapse, no *Beitragsfreistellung*

**The rule** and its consequences are set out under *Termination and values*; the **positive**
statement a projection model needs is that the *Sofortrente* is the one German retail life product
whose only decrement is death. Everything else a liability model would ordinarily carry — a
*Rückkaufswert* table, a *Stornoabzug*, a five-year cost-spreading floor [REG-R28], a
*Beitragsfreistellung* conversion, a lapse rate, a dynamic surrender formula, a duration-12 tax
threshold driving surrender behaviour [REG-R45] — is **absent by specification**, and the consumer
warning that follows is the first thing every German consumer page says: the *Einmalbeitrag* is
**irreversibly committed** [R21] [R23].

---

## Riders and options

**In scope, carried as model-point parameters** and specified above: the *Rentengarantiezeit* as an
annuity-certain floor; the *Kapital-/Beitragsrückgewähr*, solved implicitly and **[std]** mutually
exclusive with the guarantee period and the survivor's annuity; the *Hinterbliebenenrente*, **off in
the base run** because the market treats it as a rider with its own condition set [S9]; the
*Aufschubzeit*, its deferment death benefit taking the same refund form, **off in the base run**; the
*Überschussverwendung* form, as an opening surplus percentage and an annual growth rate, both
**[std]**; and payment frequency and timing, so that footnote 8's unestablished convention can be
switched and its 5 % effect measured rather than assumed away.

**Out of scope, said rather than left to be discovered.** ***Bewertungsreserven* participation**
continues throughout the payout phase and is a statutory entitlement [S3] [REG-R24], but it is path-
and balance-sheet-dependent in a way a gross liability cash-flow model cannot reproduce, being
recomputed annually on the HGB accounts and reduced by the *Sicherungsbedarf* test of § 139 VAG and
MindZV §§ 11–13, whose fifteen-year window "bites hardest on annuity business" [REG-R9] [REG-R18];
the reference implementation models the declared *Überschussrente* explicitly and treats the
*Bewertungsreserven* share as an **explicitly excluded component**. Also out: a commuted settlement
of the *Restgarantiezeit* (gap 10); a *Kapitalwahlrecht* or partial commutation after *Rentenbeginn*,
of which there is none [R1]; indexed or inflation-linked annuities and impaired-life (*enhanced*)
annuities, neither established to exist in the German retail market; proof of life, whose failure
suspends payment until the certificate arrives; and the *fondsgebundene Sofortrente*, which belongs
to `fondsgebundene_rentenversicherung`.

---

## Variations across insurers

**This specification supports no numeric variation table, and the reason is stated rather than worked
around.** No search was run for this product, so no carrier's *Rentenhöhe*, charge, envelope, option
menu or surplus rate was observed, and a table with a column per carrier would be fabrication. The
research file names **twenty-eight** German life insurers as writers of the right kind of business —
Allianz, R+V, Debeka, Generali and CosmosDirekt, NÜRNBERGER, Swiss Life, Zurich Deutscher Herold,
ERGO, AXA, HDI, Alte Leipziger, LV 1871, Volkswohl Bund, Konzern Versicherungskammer and thirteen
others [S13] — and **not one has a rate, a charge, an envelope or an option menu attached**; naming a
carrier asserts only that it is a German life insurer of the right kind. The GDV maintains
*Musterbedingungen* for the deferred annuity, the *Basisrente*, two Riester wrappers and the
*Hinterbliebenenrenten-Zusatzversicherung* [S1] [S9] [REG-R37], and **no model condition set for a
*Rentenversicherung mit sofort beginnender Rentenzahlung* appears in that list**; whether one exists
under another title, or the market drafts from the deferred template with the *Aufschubzeit* set to
zero, was **not established** (gap 3).

| Carrier | Document | What it establishes for this product |
|---|---|---|
| Zurich Deutscher Herold | [S2] immediate annuity, Fassung 01/2022; [S3] deferred, Fassung 01/2026 | that a conventional immediate-annuity pack exists in the same series as the deferred one (**no clause content**); and from [S3] the two-factor rule at *Rentenbeginn* and that *Bewertungsreserven* participation **continues in the payout phase** |
| NÜRNBERGER | [S4] AVB `gn331303_p`, *mit sofort beginnender Rentenzahlung* | that an insurer AVB for exactly this product exists, in the same numbered family as the deferred and unit-linked ones — so German insurers draft the immediate annuity as a member of the deferred series, not as a separate line |
| NÜRNBERGER | [S5] AVB tariff NIR3301 | the *Rentengarantiezeit* as a **tariff-level feature carried in the product name** |
| CosmosDirekt (Generali) | [S6] AVB LA 904 A | the conversion basis: **DAV 2004 R**, interest **0 % p.a.** at an unestablished vintage; and the standard surplus disclaimer |
| Allianz | [S7] KomfortDynamik page | that the current annuity factor **is** the carrier's immediate-annuity tariff; that the *Rentengarantiezeit* has a settable minimum |
| Debeka | [S8] B LV series, *Privatrente* page | the *Deckungskapital* definition the *Nettoeinmalbeitrag* degenerates from; the *Ertragsanteil* framing from an insurer's own page |
| GDV | [S1] [S9] | the model-conditions taxonomy, the **absence** of an immediate-annuity model set from it, and the survivor's annuity as a **rider with its own conditions** |
| Konzern Versicherungskammer | [S10] *Überschussverteilung 2026* | the annual surplus-declaration document class, current to 2026; **no rate** |

| Feature | Variants that exist | Evidence |
|---|---|---|
| *Rentengarantiezeit* | 5 / 10 / 15 / 20 / 25 / 30+ years, or none; typical 15 years to age 70 and 10 thereafter; most choose 10–20 | [R23]; tariff-level [S5]; settable minimum [S7] |
| Settlement inside the guarantee period | instalments continue, **or** the *Restgarantiezeit* is commuted | mechanic recorded; **which carriers use which, not established** |
| Death benefit menu | *Rentengarantiezeit*, *Kapital-/Beitragsrückgewähr*, *Hinterbliebenenrente*, or none | **no carrier's menu established** |
| Survivor's annuity | a *Zusatzversicherung* with its own condition set; 60 % and 100 % are the standard levels [unverified] | [S9] |
| *Überschussverwendung* in payout | konstant / teildynamisch / volldynamisch / *Bonusrente* | [R19] [R20] [R21] [R23] |
| *Bewertungsreserven* in payout | continue, currently at equal participation | [S3] [REG-R24] |
| Interest basis of the guarantee | at or **below** the *Höchstrechnungszins*; **0 %** observed at one carrier | [S6] [REG-R14] |
| *Aufschubzeit* | 0 years (pure *Sofortrente*) or a short deferment | [S14]; **no carrier's range established** |

**Parameters whose range is unknown.** *Rentenhöhe* per 100 000 € at any age, carrier or year; the
spread between the best and worst quotation; α and β; *Effektivkosten* or *Renditeminderung*; the
*Einmalbeitrag* and entry-age envelopes; every surplus rate and every *Rentenanpassung* actually
declared; the split of new business between the four *Überschussverwendung* forms; the take-up of
*Kapitalrückgewähr* against *Rentengarantiezeit*; the market's size and average ticket. **Every one
is a gap, not an omission.** A reader who needs to know how German carriers differ should start with
a *Produktinformationsblatt* [S11], Stiftung Warentest's periodic *Sofortrente* comparison [R21] and
the dedicated comparison portals [R23] — in that order, and none was located.

---

## Regulatory context

**Contract law — the VVG.** The contract is an ordinary *Lebensversicherung* under Kapitel 5, whose
provisions are largely *halbzwingend* [REG-R22]. **§ 153** gives the statutory
*Überschussbeteiligung*, names the principle — a *verursachungsorientiertes Verfahren* — without
prescribing the algorithm, and requires the *Bewertungsreserven* to be recomputed annually and
shared, currently *hälftig*, subject to the LVRG's *Sicherungsbedarf* override [REG-R24] [REG-R20]
[S3]. **§ 154** requires a *Modellrechnung* wherever the insurer quantifies benefits beyond the
guaranteed ones — which a *Produktinformationsblatt* quoting a *Gesamtrente* does — at **three rates
fixed by § 2 Abs. 3 VVG-InfoV as the *Höchstrechnungszins* × 1,67, that rate ± one point**, so at
1,00 % the statutory triple is **1,67 % / 2,67 % / 0,67 %** [REG-R25] [REG-R15]. **§ 155** requires
an annual *Standmitteilung* disclosing the current claims including profit participation and **how
much of it is guaranteed**, which makes a published specimen a legitimate primary source class and
its absence here a real gap [REG-R25] [S15]. **§§ 165–170** — *Beitragsfreistellung*, termination,
*Rückkaufswert*, *Stornoabzug* — **do not operate once the *Rentenbezug* has begun** [REG-R28] [R1]
[R2] [R5]; §§ 150 and 159–162 carry consent and the *Bezugsberechtigung* [REG-R26]; and the
*Widerrufsrecht* is 30 days for life insurance [REG-R23].

**Tariff bases — the DeckRV and the DAV.** § 2 DeckRV fixes the *Höchstrechnungszins* and, through
§ 138 Abs. 1 VAG's requirement that premiums fund the reserve, caps the rate at which a new tariff
may be priced [REG-R14] [REG-R8]. **The rate applies at conclusion and stays with the contract for
its whole term** — which is why the German book is a stack of cohorts and every delib model point
carries its cohort's rate: 3,50 % to mid-1994; 4,00 % to mid-2000; 3,25 %; 2,75 %; 2,25 %; 1,75 %;
1,25 %; 0,90 %; 0,25 % for 2022–2024; **1,00 % from 2025**, by the *Sechste Verordnung zur Änderung
von Verordnungen nach dem VAG* of 19 July 2024, BGBl. 2024 I Nr. 250 [REG-R15]. The ministry sets it
on an annual DAV recommendation — **practice, not law** — carrying a ***Sicherheitsabschlag* of
40 %** [REG-R56]. **§ 4 DeckRV's *Höchstzillmersatz* of 25 ‰ does not reach this product**, there
being no *Beitragssumme* [REG-R16]. No statute names a table: the gap between "prudent" and a
specific `q_x` is closed by the *Verantwortlicher Aktuar* under § 141 VAG [REG-R56] [REG-R11], so
**a German biometric basis is soft law with hard consequences** and DAV 2004 R is a benchmark, not a
mandate [REG-R47] [REG-R49]. The unisex rule of C-236/09 and §§ 19, 20 and 33 AGG [REG-R34] binds
the tariff from 21 December 2012 and is set out under *Underwriting and rating*.

**Surplus, the RfB and the supervisor.** The arithmetic floor under the insurer's discretion is the
MindZV: **90 % of the *Kapitalanlageergebnis* less the *Rechnungszinsen*** — the guarantee funded
first, only the excess shared — **90 % of the *Risikoergebnis***, raised from 75 % by the LVRG from
7 August 2014, and **50 % of the *übrige Ergebnis*** [REG-R18] [REG-R20]; the *Direktgutschrift* is
**deducted** and a negative minimum replaced by zero, making it a minimum **transfer to the RfB, not
a minimum payout**. Above it sit § 140 VAG's ring fence [REG-R10], the RfBV's ceiling on the
*ungebundene* part and its *kollektiver Teil* [REG-R19], the § 139 VAG *Sicherungsbedarf* test
[REG-R9], and the § 138 Abs. 2 VAG equal-treatment rule the BGH tied to § 153 VVG in IV ZR 436/22 of
18 September 2024 [REG-R8] [REG-R36] — all computed on the **HGB** accounts [REG-R54], with assets in
the *Sicherungsvermögen* under § 124 VAG's prudent-person principle rather than the AnlV quotas
German market writing routinely misapplies [REG-R7].

**Disclosure and distribution.** The VVG-InfoV prescribes the pre-contractual pack — the
*Verbraucherinformation* / *Vertragsinformationen* / *Allgemeine Informationen* class [S2] [S3]
[S14] — and carries the *Effektivkosten* disclosure [REG-R31]. PRIIPs generates the
*Basisinformationsblatt* with its *Risikoindikator*, four performance scenarios and
*Renditeminderung* [REG-R32] [S12], but **whether a payout-only *Sofortrente* falls inside PRIIPs
scope was not established** (gap 8): it reads as an insurance-based investment product, while its
payout-only character and the absence of a surrender value make the holding-period and "what you
might get back" sections awkward. If one exists it is the **only** public document giving this
product's cost in standardised form, and none was located. Distribution runs under the IDD as
transposed on 20 July 2017 and § 34d GewO [REG-R33].

**Taxation.** The whole cash flow is taxed under **§ 22 EStG** on the *Ertragsanteil* and **none of
it under § 20** [R13] [R14] [REG-R41] [REG-R45]: only the "Ertrag des Rentenrechts" is income, and
the fraction is fixed once by the age at *Rentenbeginn* — **18 % at 65** [R13], 22 % at 60
[REG-R41], the rest of the schedule [unverified] with the 65 value as its only check. On the
constructed 389,99 € monthly annuity of footnote 10 the taxable amount is 70,20 €, so the tax is
**17,55 €, 4,5 % of the annuity**, at a 25 % marginal rate and 29,48 €, **7,6 %**, at 42 % **[std]**.
The § 20 Abs. 1 Nr. 6 *Halbeinkünfteverfahren* requires twelve contract years and payment after the
62nd birthday and reaches only lump sums and payout-plan withdrawals [REG-R45] — **the boundary that
is the product's main quantitative selling point** against a *Bankauszahlplan* taxed in full at the
*Abgeltungsteuer* rate. A death benefit to a named beneficiary is an ordinary *Erwerb von Todes
wegen* under § 3 Abs. 1 Nr. 4 ErbStG, and a Schicht-3 annuity is **not** a *Versorgungsbezug* under
§ 229 SGB V — though **§ 240 SGB V reverses that for *freiwillig versicherte* members** [REG-R46].
**Not established:** whether *Rentengarantiezeit* payments to a beneficiary keep the original
*Ertragsanteil*, whether a *Kapitalrückgewähr* refund is taxable, whether a *Hinterbliebenenrente* is
re-based on the survivor's commencement age, and the *Solidaritätszuschlag* (gap 15).

**Prudential and accounting — cited, never specified.** BaFin supervises under Solvabilität II as
transposed into the VAG [REG-R1] [REG-R2] [REG-R5] [REG-R6], with Directive (EU) 2025/2 amending the
regime [REG-R3] and EIOPA publishing the curves [REG-R4]. A German insurer values this book
**twice**: the HGB *Deckungsrückstellung* on the first-order bases, increased by the ZZR [REG-R14]
[REG-R17] [REG-R54], on which the whole surplus system operates; and the Solvency II best estimate at
the EIOPA curve plus a risk margin [REG-R6]. IFRS 17 is a third, group-reporting measure [REG-R55].
**`delib` computes none of them:** the models publish gross best-estimate-style liability cash flows
per model point, income-positive and **undiscounted**, and the discounting, the margins, the
*Deckungsrückstellung* recursion, the ZZR, the RfB stock and the CSM belong to a layer above.
