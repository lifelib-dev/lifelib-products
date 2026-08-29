# Product Specification

**Status:** Draft, 2026-08-29 (all sources dated 2026-08-29; **none was retrieved** — see the
retrieval note below).

**Scope note.** This is a *representative composite specification* assembled for reference
liability cash-flow modeling of a German **sofortbeginnende private Rentenversicherung** — the
*Sofortrente*: a single *Einmalbeitrag* (single premium) buys a *Leibrente* (life annuity) that
begins at once and is paid for as long as the annuitant lives. **It is not any single insurer's
contract**, and no clause of any German insurer's *Allgemeine Versicherungsbedingungen* (AVB)
for this product was read. Facts carrying a source tag — [S#] (primary product documents:
*Verbraucherinformation*, AVB, *Produktinformationsblatt*, *Basisinformationsblatt*,
*Überschussverteilung*) and [R#] (product-specific regulatory and actuarial references), both
numbered per `_research/sofortrente.md` and resolved in `sources.md` (same directory; numbering
frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R56 numbering is separately
frozen) — name the instrument a claim should be checked against. Values marked **[std]** are
standardizations introduced for the reference implementation; each **[std]** table row carries a
numbered footnote giving the rationale and, where one exists, the observed range. Claims no
search corroborated are flagged [unverified]. German terms of art stay in German, italicised on
first use with a gloss.

**Retrieval conditions, stated first because they govern every line below.** Two independent
limits applied while `delib` was built. Direct HTTP egress is blocked by an organisation network
policy: `WebFetch` and `curl` are refused with HTTP 403 for `gesetze-im-internet.de`,
`bafin.de`, `gdv.de`, `aktuar.de`, `destatis.de`, `eur-lex.europa.eu` and every insurer host
named here. And the session's 200-call `WebSearch` budget was **exhausted before work on this
product began**, so **not one search was run for the *Sofortrente***. Every source in this
product's `sources.md` is therefore either a **known reference** — a document class and carrier
that exists and is the right kind of thing to cite — or a fact carried over with attribution
from a sibling `delib` research file whose searches ran earlier in the session, principally
`_research/klassische_rentenversicherung.md`, which shares this product's *Rechnungsgrundlagen*
(calculation bases), its surplus chassis and, at two carriers, its tariff. **A delib citation is
a pointer, not a certificate.** It says where to check; it does not say that anyone checked.

**The direct consequence for this document.** The corpus establishes this product's **mechanics**
well and its **levels** hardly at all. *Not one annuity rate, charge, envelope, option menu or
surplus declaration was observed at any German carrier for any year.* So there is **no
insurer-level quantitative comparison anywhere in this specification**, the *Variations across
insurers* section is structural rather than numeric, and every euro and every percentage
describing the representative design is either **[std]** with its derivation printed or is
tagged to a cross-product reference. That is weaker than the `frlib` equivalents, where
Légifrance served in full, and it is said here rather than glossed.

**Out of scope, and named so the boundary is explicit.** The **accumulation phase** of a
deferred annuity — *klassische aufgeschobene private Rentenversicherung* — is the separate delib
product `klassische_rentenversicherung`, and everything about premium accumulation, the
*Deckungskapital* recursion, the *Rückkaufswert*, *Beitragsfreistellung* and the
*Kapitalwahlrecht* belongs there. **Schicht 1** (*Basisrente*/Rürup) and **Schicht 2**
(*Riester-Rente*, bAV) run the same payout machinery under completely different tax rules
[REG-R38] and are separate products. *Fondsgebundene* and *indexgebundene* payout annuities,
*Sterbegeldversicherung*, *Pflegerentenversicherung*, *Gruppenversicherung*, private
*Krankenversicherung* and institutional pension-risk transfer are all outside this file.

---

## Product overview and market role

A *Sofortrente* is an ordinary German **life insurance contract** (*Lebensversicherung*) under
the *Versicherungsvertragsgesetz* (VVG) [REG-R22], written on the insurer's general account
(*Sicherungsvermögen*) [REG-R7], in the classic (*konventionell*) non-unit-linked form
[S2] [S6]. Structurally it is one sentence long: **one payment in at inception; a stream of
payments out until death**, floored by a *Rentengarantiezeit* (guarantee period) or a
*Kapitalrückgewähr* (refund of the unconsumed capital on death) and lifted by a declared,
non-guaranteed *Überschussrente* (surplus annuity). It is not a savings product and not a
drawdown plan: what it sells is the transfer of *Langlebigkeitsrisiko* — the risk of outliving
one's money — to an insurer.

**The parties.** The *Versicherungsnehmer* (policyholder) contracts and pays the
*Einmalbeitrag*; the *versicherte Person* (annuitant) is the life the annuity depends on; a
*mitversicherte Person* may be named for a *Hinterbliebenenrente* (survivor's annuity); a
*Bezugsberechtigter* (designated beneficiary) receives whatever falls due after death
[REG-R26]. Usually the first three are one person. Where they are not, § 150 VVG requires the
insured person's written consent above a threshold expressed in terms of ordinary funeral costs
[REG-R26], and the designation is a live element the policyholder may change at will [REG-R26].

**Schicht 3, and why the tax rule is the product.** The *Sofortrente* is a third-layer,
unsubsidised private contract in the *Drei-Schichten-Modell* the *Alterseinkünftegesetz*
introduced [REG-R38]: nothing is deductible going in, and only the ***Ertragsanteil*** — a fixed
statutory fraction of each payment, determined once by the annuitant's age at *Rentenbeginn* and
never changed — is taxable coming out [R13] [REG-R41]. **For an annuity commencing at age 65
that fraction is 18 %** [R13], the only cell of the statutory table any delib search
corroborated. The asymmetry against Schicht 1 and Schicht 2 is total and it decides the product:
a Schicht-1 *Rentenfreibetrag* is frozen in euros for life, so **every later increase, including
every increase in the *Überschussrente*, is fully taxable**, whereas in Schicht 3 it is the
*percentage* that is frozen, so surplus increases are taxed at the same light rate [REG-R41].
That is the whole economic case for this product, and it is the reason it is bought with money
that has already been taxed — an inheritance, a property sale, a matured endowment, a severance
payment, or the *Kapitalwahlrecht* lump sum from a deferred contract.

**Its structural role: the pricing primitive of every other German annuity.** Two carriers state,
independently, that the *aktueller Rentenfaktor* at which a deferred contract converts is the
tariff the insurer is then writing **for immediately beginning annuities**. Zurich Deutscher
Herold's deferred pack describes a second *Rentenfaktor* compared at *Rentenbeginn* with the
guaranteed one, the higher of the two being guaranteed for the annuity payment period [S3];
Allianz states that the calculation bases at *Rentenbeginn* "relate to the interest rate and
mortality table that the company uses at that time for immediately beginning annuities" [S7].
Read together, the pair establishes the convention: **the current annuity factor of any German
deferred annuity is that carrier's current *Sofortrente* tariff.** A model of this product is
therefore also the conversion engine of `klassische_rentenversicherung`,
`fondsgebundene_rentenversicherung`, `indexpolice`, `basisrente` and `riester_rente`.

**Market size — what is known and what is not.** No figure isolates this product. The GDV's own
statistical series separates *Einmalbeiträge* from *laufende Beiträge* in new business, but that
line aggregates *Sofortrenten* with single-premium endowments, bAV contributions and
*Zuzahlungen*, so even a retrieved figure would not size the segment [R25]. What can be said, on
the cross-product aggregates: German life premium income (life insurers, Pensionskassen and
Pensionsfonds together) was **+2.8 % to 94,6 Mrd €** in 2024, of which *laufende Beiträge* were
**66,3 Mrd €**, roughly flat, while the ***Einmalbeitragsgeschäft* grew about 10 % to
28 Mrd €**; the contract count fell 1.4 % to **80,3 Mio** [REG-R53]. Single premium is now
roughly **30 %** of German life premium income and is growing an order of magnitude faster than
regular premium [REG-R53] — which is the structural reason this product is live. **No number of
*Sofortrente* contracts, no average *Einmalbeitrag* and no average purchase age was established,
at any carrier, for any year** (research gap 7).

**The 2025 interest step, and why it matters more here than anywhere else.** The
*Höchstrechnungszins* — the statutory maximum rate at which a German life insurer may discount
its *Deckungsrückstellung*, and through § 138 Abs. 1 VAG the effective cap on a new tariff's
technical rate [REG-R8] [REG-R14] — fell for thirty years to **0,25 %** and rose to **1,00 % on
1 January 2025**, the first increase since 1994 [REG-R14] [REG-R15]; the DAV recommended 1,0 %
again for 2026 and again for 2027 [R8] [REG-R56]. For a deferred contract the rate matters over
a thirty-year accumulation; for a *Sofortrente*, **the rate at which the tariff is struck is the
rate the buyer's whole income is fixed on, permanently, on the day of purchase**. On this file's
own **[std]** arithmetic that single step is worth about **+10 %** on the guaranteed annuity at
age 65 and **+12 %** at age 60, tapering to about **+6 %** at 80 (see *Rentenhöhe* below). The
direction is not in doubt — it falls out of the tariff formula itself [S6] and the statutory rate
history [REG-R15] — but **the magnitude is constructed, not observed** (research gap 5).

**What it is bought against.** The German consumer literature's standard comparator is a
***Bankauszahlplan*** (bank payout plan): the same capital held at a bank and drawn down at a
chosen monthly rate until exhausted. The comparison has three limbs and only the third is usually
put honestly. The payout plan **ends** — on the [std] arithmetic of section *Rentenhöhe*,
100 000 € drawn at 400 € a month at 2 % is exhausted after 26,9 years, at about age 92 [std] (14)
— whereas the annuity does not. The annuity's payments are taxed on 18 % of each instalment
[R13] [REG-R41] while the payout plan's interest is taxable in full as *Kapitalerträge*, so any
gross comparison is misleading. And the annuitant gives up the capital irreversibly, leaves no
residual estate beyond the *Rentengarantiezeit* or *Kapitalrückgewähr*, and does badly by dying
early. The honest framing is that a *Sofortrente* **is insurance against outliving one's money,
priced like insurance**: most buyers "lose" and the ones who need it are made whole.

**One market fact that does not apply here.** The classic **deferred** annuity was withdrawn by
Debeka in 2016 and by Allianz, Zurich and Generali before it, in favour of partial-guarantee
hybrids [S7] [S8]. **No equivalent retreat from the immediate annuity was established**, and
there is a structural reason not to expect one: the objection to the deferred contract was a
thirty-year interest guarantee, whereas an immediate annuity's guarantee is short-dated in
interest terms and its real risk is longevity, which no alternative design removes. That is an
argument, not a finding, and it must not be asserted downstream as market fact (research gap 14).

---

## Representative specification

**What "representative" means here, and how each choice is argued.** In the sister libraries a
composite is assembled by taking the mode of an observed range across retrieved carriers. That
method is **unavailable for this product**: the corpus contains two documents whose titles name
the immediate annuity — Zurich Deutscher Herold's *Verbraucherinformation für Konventionelle
Versicherungen — Sofort beginnende Rentenversicherung*, Fassung 01/2022 [S2], and NÜRNBERGER's
AVB `gn331303_p` [S4] — and **neither yielded a single clause**. So each representative value
below is argued from one of exactly three things, and the table says which: **(i)** a mechanic
the corpus establishes at clause level, at a named carrier; **(ii)** a statutory or professional
rule from the cross-product reference library; or **(iii)** the modeller's construction, tagged
**[std]**, with its arithmetic printed so a reader can reproduce or replace it. Where the third
applies and there is no observed range at all, the footnote says so in those words, because a
**[std]** with no range is a weaker object than a **[std]** with one.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | *Sofortbeginnende private Rentenversicherung*: single-premium immediate life annuity on the general account, *konventionell* (non-unit-linked), profit-participating | [S2] [S6]; participation statutory [REG-R24] |
| Legal form | German *Lebensversicherung* under the VVG; *Neubestand* (concluded after 29 July 1994) | [REG-R22]; [REG-R11] |
| Tax layer | Schicht 3 — no *Sonderausgabenabzug*, no *Zulage*, no certification; *Ertragsanteil* on payout | [REG-R38] [REG-R41] [R13] |
| Lives basis | Single life; a second life may be added as a *Hinterbliebenenrenten-Zusatzversicherung* | [S9] |
| Premium form | **One** *Einmalbeitrag*, paid once at inception. There is no premium stream, no *Beitragsdynamik* and no *Ratenzahlungszuschlag* | [S2] [S6]; structural |
| Entry ages | **60 to 85** | envelope **[std]** (1) |
| *Einmalbeitrag* | Minimum **10 000 €**; working range **25 000 € to 500 000 €**; representative case **100 000 €** | envelope **[std]** (2) |
| *Aufschubzeit* (deferment) | **0 years** in the representative design; **0 to 15 years** offered | **[std]** (3) |
| Underwriting | **None.** No medical evidence, no *Gesundheitsprüfung* | **[std]** (4), [unverified] |
| Sex | Tariff is **unisex** for business written from 21 December 2012; the profession's tables are sex-distinct | [REG-R34]; [REG-R49] |
| *Rechnungszins* (tariff technical rate) | **1,00 %** for a contract written in 2025 or 2026, at or below the *Höchstrechnungszins* of the contract's own vintage | [REG-R14] [REG-R15]; below-cap pricing observed at one carrier [S6] |
| Currency | EUR | — |
| Anchor model cell | *Einmalbeitrag* 100 000 €, annuitant male aged 65 (born 1960), inception 2025, *Rechnungszins* 1,00 %, *Rentengarantiezeit* 10 years, monthly *vorschüssig*, *teildynamische Überschussrente* | **[std]** (5) |

Footnotes to **[std]** rows:

1. **Nothing was established about entry ages at any carrier.** The product is sold at and around
   retirement, with a typical purchase window in the sixties and issue into the eighties at some
   carriers, all [unverified]. **60 to 85** is adopted because below 60 the *Ertragsanteil* is
   high enough (22 % at 60 against 18 % at 65 [REG-R41]) to weaken the tax case that is the
   product's reason to exist, and above 85 the *Rentengarantiezeit* options collapse — a 20-year
   guarantee at 85 costs a quarter of the annuity on the arithmetic below. The boundaries claim
   to be no carrier's.
2. **Nothing was established.** The market convention is a five-figure minimum, because the fixed
   per-policy administration cost would swamp a small annuity, with an upper limit set by
   reinsurance rather than tariff. The representative case of **100 000 €** is chosen because it
   is the unit German annuities are quoted in — the market quotes *Rente je 100 000 €
   Einmalbeitrag*, not the *Rentenfaktor* per 10 000 € the deferred market uses — so it is the
   figure a reader can compare against any published quotation they find.
3. The *Aufschubzeit* variant exists — the *Einmalbeitrag* is paid now and the annuity begins
   after a short deferment — but **no carrier's terms, minimum, maximum or deferment death
   benefit were established** (research gap 17). The representative design takes **0**, which is
   what makes the contract a *Sofortrente* rather than a single-premium deferred annuity, and
   carries the deferment as a model-point column so the variant can be switched on.
4. A *Sofortrente* is normally written **without medical underwriting**, because the exposure runs
   the wrong way: medical evidence would be used by the applicant, not the insurer, and the
   selection accordingly sits in the tariff margin rather than in an individual assessment. **No
   source in the corpus states this**, so it is [unverified]. Its converse, the impaired-life
   *enhanced annuity*, is **not established to exist in the German retail market** and nothing
   here asserts that it does. § 19 VVG's *Anzeigepflicht* [REG-R30] is inert where the insurer
   asks nothing.
5. Age 65 is the age at which the corroborated *Ertragsanteil* value applies [R13], the age the
   corpus's own consumer illustrations use, and the age at which the [std] annuity table below is
   anchored. The 10-year *Rentengarantiezeit* is inside the market's typical band — 15 years for
   retirement ages 61–70 and 10 years for 71 and above, with most policyholders choosing 10 to
   20 [R23] — and is chosen at the shorter end so that the certain window is visible inside a
   readable worked-example table. The 2025 inception puts the cell on the current 1,00 %
   *Höchstrechnungszins* [REG-R15].

### Premiums — the *Einmalbeitrag*

| Parameter | Representative value | Basis |
|---|---|---|
| Premium structure | A single *Einmalbeitrag*, paid once at inception; **one inflow, at `t = 0`** | [S2] [S6]; structural |
| *Nettoeinmalbeitrag* | `Einmalbeitrag × (1 − α)`, where α is the *Abschluss- und Vertriebskosten* charge. Debeka's own definition of the accumulation quantity — the *Deckungskapital* is the sum of the contributions accumulated at the *Rechnungszins*, insofar as they are not required for risk and expense cover [S8] — degenerates for a single premium to exactly this one netting step | [S8]; α **[std]** (6) |
| Acquisition loading α | **2,5 %** of the *Einmalbeitrag* | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| *Zillmerung* | **Does not apply.** § 4 DeckRV caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme*; a single-premium contract has no premium stream to amortise against and therefore no *Zillmerung* at all | [REG-R16]; structural |
| Further premiums | **None.** No *Zuzahlung*, no dynamic increase, no top-up in the representative design | **[std]** (7) |
| Premium refund on cancellation | *Widerrufsrecht*: 30 days for life insurance under § 152 VVG, against 14 days generally | [REG-R23] |
| Payment method | One transfer at inception; no *Ratenzahlungszuschlag*, because there are no instalments | structural |

6. **No charge parameter was established for this product at any carrier** — not the *Abschluss-
   und Vertriebskosten*, not the administration loading, not an *Effektivkosten* figure under the
   VVG-InfoV [REG-R31], not a *Renditeminderung* under PRIIPs [REG-R32] (research gap 8). The
   product has exactly three charge points, fewer than any other delib product: an acquisition
   charge on the *Einmalbeitrag*, taken once; a running loading on each annuity payment, covering
   the payment run, the annual *Standmitteilung* [REG-R25] and the proof-of-life process; and an
   implicit margin inside the *Rechnungsgrundlagen*, since pricing at 0 % when the cap is 1,00 %
   [S6] [REG-R14] is a charge in economic substance whatever any document calls it. α = 2,5 % is
   argued from a single-premium annuity's cost base being a one-off commission plus issue expense,
   materially lower than the *Zillmerung* of a recurring-premium contract; β = 2,0 % is argued
   from a per-policy running cost that is roughly constant in euros, which is why 2 % is of the
   right order on a 100 000 € case and too small on a 25 000 € one — itself the reason minimum
   *Einmalbeiträge* exist. **Both are the modeller's view with no observed range, because nothing
   was observed.** The market benchmark that does exist is a *Verwaltungskostenquote* for German
   life business of **2,4 %** on one measurement and **2,19 %** on another, with a spread from
   under 2 % to over 4 % [REG-R53] — an insurer-level ratio on premium income, not a product
   charge, and it bounds nothing here.
7. Whether German carriers permit a *Zuzahlung* into a *Sofortrente* after inception **was not
   established**. Economically a top-up is a second annuity purchase at the then-current tariff,
   and the representative design treats it that way by excluding it: a second *Einmalbeitrag* is a
   second model point.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Main benefit | A *Leibrente*: a level **guaranteed** monthly annuity, payable for as long as the annuitant lives | [S6] [S7] [R23] |
| Determination | `R = Einmalbeitrag × (1 − α) / (12 × a12(x, i) × (1 + β))`, where `a12(x, i)` is the monthly annuity-due factor at attained age x and *Rechnungszins* i on the **first-order** DAV 2004 R basis for the annuitant's birth cohort | [S6] [R10]; α, β **[std]** (6) |
| Guarantee | The *garantierte Rente* struck at inception is guaranteed **for life** and is not adjustable; § 163 VVG is the only channel and it is narrow | [S6]; [REG-R27] [R4] |
| Payment frequency | **Monthly** is the market standard; quarterly, half-yearly and annual exist as options | [S7] [R23]; other frequencies [unverified] |
| Payment timing | ***Vorschüssig*** — in advance, at the start of each payment period; first instalment at inception | **[std]** (8) |
| *Überschussrente* | Declared annually out of surplus actually earned, added to the guaranteed annuity; **not guaranteed and reducible** | [R19] [R20] [R21] [R23]; levels **[std]** (12) |
| *Überschussverwendung* | Four forms — *konstant*, *teildynamisch*, *volldynamisch (steigend)*, *Bonusrente* — elected at *Rentenbeginn*, here at inception, once | [R19] [R20] [R21] [R23]; irrevocability [unverified] |
| *Bewertungsreserven* | Participation **continues during the annuity payment period**, currently at *hälftige* (equal) participation under § 153 Abs. 3 VVG | [S3]; [REG-R24] |
| *Rentengarantiezeit* | **10 years** in the representative design; 5 / 10 / 15 / 20 / 25 / 30+ offered, or none | [R23]; [S5] [S7]; choice **[std]** (5) |
| Death inside the *Rentengarantiezeit* | The annuity **continues to be paid to the beneficiaries** until the agreed number of years has expired | [R23] |
| Death after it | **Nothing is payable** unless a *Kapitalrückgewähr* or a *Hinterbliebenenrente* was also bought | [R23]; structural |
| *Kapital-/Beitragsrückgewähr* | Optional: on death, the *Einmalbeitrag* **less the annuity instalments already paid**, floored at zero | [R23]; measured against the **guaranteed** annuity **[std]** (9) |
| *Hinterbliebenenrente* | Optional rider: 60 % or 100 % of the annuitant's annuity to a named second life, payable for that life's remaining lifetime | [S9]; percentages [unverified] |
| Maturity | **None.** The contract has no term and no maturity value | structural |
| Capital option | **None** after *Rentenbeginn*. The annuity may not be commuted at the policyholder's election | [R1]; [REG-R28] |
| Settlement on death | To the *Bezugsberechtigter*, not automatically to the estate; the designation is revocable unless made irrevocably | [REG-R26] |

8. **The payment timing was not established by any source in the delib corpus**, for this product
   or for the deferred one, and it is first-order: on this file's own basis the two conventions
   differ by about **5 %** of the annuity, because advance against arrears moves the annuity value
   by roughly half a month's interest *and* shifts every payout cash flow by one period. On the
   [std] basis at 1,00 %, `a12_due − a12_arrears = 1`, so the annuity per 100 000 € at age 65
   would be `100 000 / (12 × 19.426) = 428,99 €` in arrears against **407,98 €** in advance.
   *Vorschüssig*, with the first instalment at inception, is adopted as **[std]** because it is
   the German market convention for annuities in payment and because every arithmetic in the
   research file uses an annuity-due — but it is a convention stated as one, not a finding
   (research gap 11). The first payment date convention — the day the *Einmalbeitrag* is received
   against the first of the following month — was likewise not established.
9. **Whether the refund counts the *guaranteed* or the *total* annuity paid is a live contractual
   question, not established at any carrier**, and the two readings diverge materially over twenty
   years. The representative design measures the refund against the **guaranteed** annuity, on the
   argument that a guaranteed benefit cannot be defined by reference to a discretionary quantity.
   That is a modeller's argument, not a carrier's clause (research gap 10).

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Medical evidence | **None** | **[std]** (4), [unverified] |
| Rating factors | Attained age at *Rentenbeginn*; birth cohort; the elected options; the *Einmalbeitrag*. **Sex may not be a rating factor** for business written from 21 December 2012 | [S6] [R10]; unisex [REG-R34] |
| Mortality basis | **DAV 2004 R**, named in an insurer's own AVB: the annuity factor is calculated "on the basis of a recognised mortality table (currently DAV 2004 R) and an underlying interest rate (currently 0 percent p.a.)" — quoted from a search summary of [S6], not from the document | [S6]; [R10] [REG-R49] |
| Table type | A ***Generationentafel*** — a two-dimensional basis `q(x, τ)` in attained age and calendar year, **not** a period table. Mortality is given per **birth cohort** and the expected future improvement is **inside** the table | [R10]; [REG-R49] |
| First against second order | First-order probabilities carry safety margins relative to the second-order ("realistic") ones. For an annuity, prudent means **lighter** mortality **and a stronger assumed improvement trend** — safety in two dimensions | [R10]; [REG-R47] |
| Interest basis | The insurer's own choice **at or below** the *Höchstrechnungszins*, never automatically the cap; **0 % p.a.** observed at one carrier at an unestablished vintage | [S6]; [REG-R14] |
| Anti-selection | Real, and not underwritten away. Single-premium immediate annuities are bought disproportionately by people who expect to live long, and the table is understood to carry ***Selektionsfaktoren*** for exactly that | [REG-R49]; [unverified] |
| *Altersverschiebung* | DAV 2004 R carries an age-adjustment component with a base table; **its convention was not established** | [R10]; research gap 12 |

**What delib ships instead of the table, and why.** DAV 2004 R and DAV 2004 R-Bestand are the
property of the Deutsche Aktuarvereinigung, are distributed to members and licensees rather than
published, and are **not redistributable**. `delib` ships **no version of either** and quotes no
`q_x`, no improvement rate and no annuity factor from them [REG-R47] [REG-R49]. The decrement
CSV shipped with `Sofort_DE_S` is a **[std] proxy**, anchored so that the model's own worked
example reproduces exactly, with the anchor stated in the model's `Data` docstring. **A
replacement must preserve three things**: the **generational** structure — a `q(x, cohort)`
surface, because a period-table proxy applied to a forty-year annuity understates the liability
by a margin that dwarfs every other assumption in the model [REG-R49]; the **first-order margin
in both dimensions**, level and trend [REG-R47]; and the *Altersverschiebung* convention [R10].
Destatis's *Generationensterbetafeln für Deutschland* are the free, redistributable public
analogue and the intended base for a user-supplied replacement [REG-R52].

**DAV 2004 R-Bestand, and why the distinction is conceptually central here.** DAV 2004 R is the
**new-business** table; the *Bestand* variant is the table for the **existing annuity book**,
reflecting the different composition and selection history of annuities already in payment
[R11] [REG-R49]. **Nothing beyond the pairing was established** — not the difference in level, in
trend, in age range or in application rule — and nothing about it may be asserted downstream
(research gap 12). It matters nonetheless: a *Sofortrente* is priced once on the new-business
table and then spends thirty years in the *Bestand* to which the other table applies.

**The unisex tension bites harder on this product than on any other in the library.** German
annuity tables are built sex-distinctly while a tariff sold since 21 December 2012 must be unisex
[REG-R34] [REG-R49]. A *Sofortrente* is the purest longevity bet in the market; female annuitants
are materially longer-lived; so a unisex tariff on sex-distinct tables must be struck on an
**assumed portfolio sex mix that no insurer publishes**. Two consequences follow. A unisex annuity
is a worse deal for men and a better one for women, so the realised mix drives the
*Risikoergebnis* that the MindZV then shares [REG-R18]. And the reference implementation's
decrement table must be a **unisex [std] proxy**, described as one, with a stated mix assumption
(research gap 13).

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| *Abschluss- und Vertriebskosten* α | **2,5 %** of the *Einmalbeitrag*, taken once at inception | **[std]** (6) |
| Annuity administration loading β | **2,0 %** of each annuity payment | **[std]** (6) |
| Implicit margin in the *Rechnungsgrundlagen* | The *Sicherheitszuschlag* on the mortality table, and any pricing below the *Höchstrechnungszins* | [S6] [R10] [REG-R47]; not quantified |
| *Stornoabzug* | **None, ever.** § 169 Abs. 5 VVG permits a deduction only where agreed, quantified and appropriate — and there is no surrender to deduct from | [REG-R28]; structural |
| *Effektivkosten* (VVG-InfoV) | **Not established** for this product at any carrier | [REG-R31]; research gap 8 |
| *Renditeminderung* (PRIIPs) | **Not established**, and whether a payout-only *Sofortrente* is even within PRIIPs scope is itself unresolved | [S12] [REG-R32]; research gap 8 |
| Effect of both [std] charges | On the [std] gross annuity of 407,98 € at age 65 and 1,00 %: `407,98 × 0,975 / 1,02 = 389,99 €` per month per 100 000 €; a 10-year *Rentengarantiezeit* takes it to about **381 €** | **[std]** (10) |

10. This is a **constructed illustration**, not a market rate, and it is the shape of a quotable
    guaranteed *Sofortrente* on this file's own arithmetic. It is printed because a reader needs
    an order of magnitude to sanity-check a model against, and because printing the construction
    is the only honest alternative to printing a fabricated quotation. **No German carrier's
    quotation, at any age, for any year, appears anywhere in this specification** (research
    gap 5).

**The supervisory backdrop, and why it does not reach here.** BaFin's *Merkblatt 01/2023 (VA)* on
*wohlverhaltensaufsichtliche Aspekte* sets out what the supervisor expects so that a life product
delivers an *angemessener Kundennutzen*: it will scrutinise insurers whose *Effektivkosten* are
very high in a sector comparison and whose intermediary expenses are noticeably high, and
producers must formulate a return target for the target market [REG-R35]. **All of it is
addressed to *kapitalbildende* products — the accumulation side.** Whether BaFin has published
anything on payout annuities, and whether it scrutinises *Rentenhöhe* or surplus declarations for
value, **was not established** [R18].

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender (*Rückkauf*) | **None once the *Rentenbezug* has begun.** For a *Sofortrente*, whose *Rentenbeginn* is at or within weeks of inception, **the contract is irrevocable from the outset** | [R1] [R2]; [REG-R28]; see the discrepancy note below |
| *Rückkaufswert* | **None.** § 169 VVG is displaced: there is no surrender-value table, no *Stornoabzug* and no five-year cost-spreading rule to implement | [R2]; [REG-R28] |
| Lapse | **None.** A policyholder cannot lapse a contract they cannot terminate and on which no further premium is due | [R1]; structural |
| *Beitragsfreistellung* | **None.** § 165 VVG has no application: there is no premium to stop | [R5]; [REG-R28] |
| Paid-up value | **None**, for the same reason | [R5] |
| Termination of the contract | On the annuitant's death, subject to any *Rentengarantiezeit* still running, any *Kapitalrückgewähr* then due and any *Hinterbliebenenrente* then beginning | [R23]; structural |
| *Widerrufsrecht* | 30 days from being properly informed, for life insurance | [REG-R23] |
| Insolvency of the insurer | German life contracts transfer to **Protektor Lebensversicherungs-AG**, the statutory *Sicherungsfonds* | [REG-R12] |
| Unclaimed instalments | No product-specific rule established; ordinary civil prescription applies | [unverified] |
| *Aufschubzeit* qualification | The deferment variant has a genuine pre-*Rentenbeginn* window in which the termination bar does not yet bite, so a surrender right — and a *Rückkaufswert* under § 169 — **may** exist during it. **No carrier's terms were established**; the reference implementation switches the variant off in its base run | [R1] [R2]; research gap 17 |

**A discrepancy between two delib documents, named rather than resolved.** The product research
file states that **§ 168 Abs. 3 VVG** provides that in a *Rentenversicherung ohne
Kapitalwahlrecht* the right of termination exists only up to the start of the annuity payments
[R1], flagging the paragraph number as [unverified] and the whole point as research gap 9. The
cross-product reference library, working from nine search queries that touched §§ 165–170,
reports **§ 168 Abs. 3** as the carve-out excluding Abs. 1 and 2 for a *Basisrentenvertrag*
certified under § 5a AltZertG and where the parties irrevocably excluded realisation before
retirement [REG-R28]. **Neither was read at article level.** The two readings are not necessarily
inconsistent — one *Absatz* may carry more than one exclusion — but the delib corpus cannot
choose between them, and this specification does not pretend to. What matters for the model is
not the paragraph number but the **substance**, on which both entries, the consumer literature
[R21] [R23] and the economics agree: **once the *Rentenbezug* has begun there is no termination
right and no *Rückkaufswert*.** A surrenderable life annuity would be surrendered by exactly
those annuitants expecting to die soon, leaving the insurer with the long-lived; the bar is what
makes the mortality pooling — the whole product — possible. A reader who needs the paragraph
number must read the statute.

**What this does to the model, and it is a great deal.** `Sofort_DE_S` publishes **no
surrender-value cells, no lapse decrement, no paid-up state and no *Stornoabzug***. The only
decrement in the payout phase is **death**. The behavioural assumption set — the lapse rate, the
paid-up rate, the option take-up rate that every other delib product needs — is **empty**, which
makes this the cleanest of the ten to project and the one whose result depends most purely on the
mortality basis and the surplus assumption. Each of those absences is a **specification, not a
simplification**, and the technical notes say so at the point where a reader would otherwise
expect the cells.

---

## Contractual mechanics

### The *Einmalbeitrag* and the *Nettoeinmalbeitrag*

**The rule.** The insurer deducts the acquisition and distribution loading from the
*Einmalbeitrag* and annuitises the remainder. Debeka's own definition of the accumulation
quantity — the *Deckungskapital* is the sum of the contributions accumulated at the
*Rechnungszins*, insofar as those contributions are not required for risk and expense cover
[S8] — collapses for a single premium into one netting step:

    Nettoeinmalbeitrag = Einmalbeitrag × (1 − α)

**What it does.** It fixes, once and for all, the capital that the annuity is struck against.
There is no later accumulation, no *Beitragsdynamik* and no second netting: everything downstream
is a division of this one number by an annuity factor. It is also the whole of the product's
new-business strain: the acquisition cost is incurred at `t = 0` against a single inflow, so the
projection's first period carries a large positive `net_cf` and every later period a negative one.

### *Rentenhöhe* — how the guaranteed annuity is struck

**The rule.**

    R_garantiert = Einmalbeitrag × (1 − α) / ( 12 × a12(x, i) × (1 + β) )

where `a12(x, i)` is the monthly annuity-due factor at attained age `x` and *Rechnungszins* `i`,
computed on the **first-order** DAV 2004 R basis for the annuitant's birth cohort [S6] [R10].

**What it does, and the three things it settles.** First, **the mortality basis is DAV 2004 R**
and it is named in an insurer's own AVB [S6]. Second, **the interest basis need not be the
*Höchstrechnungszins***: the same clause continues "and an underlying interest rate (currently 0
percent p.a.)" [S6] — a carrier pricing a *guaranteed* annuity factor at zero while the statutory
maximum was positive. That is the *Sicherheitszuschlag* made concrete on the interest side, and it
establishes that the tariff rate is the insurer's choice **at or below** the cap, never
automatically the cap. Third, **the factor is fixed at inception**, which for a *Sofortrente*
means fixed once and never revisited, because inception and *Rentenbeginn* are the same date.

**The market's quoting unit** is the euro per 100 000 € of *Einmalbeitrag*, not the *Rentenfaktor*
per 10 000 € the deferred market uses. The two are one number scaled by ten: a *Rentenfaktor* of
40,80 and an annuity of 408 € per 100 000 € say the same thing.

**The [std] annuity table.** No annuity level was established at any carrier for any year, so the
research file **constructs** one and prints the construction. Mortality: a Gompertz–Makeham proxy
`mu(x) = A + B·c^x` with **A = 0,0002**, **B = 1,5 × 10⁻⁵**, **c = 1,10**, giving a
curtate-plus-half life expectancy of **24,29 years at 65**, 16,63 at 75 and 10,46 at 85, and
sample rates `q(65) = 0,00789`, `q(75) = 0,02001`, `q(85) = 0,05078`, `q(95) = 0,12617`. That is
a **prudent annuitant** shape of the right order for a first-order German basis; it is **not**
DAV 2004 R [R10]. Monthly-in-advance via `a12 = a_due − 11/24`. Charges excluded, so the figures
are gross values, not quotations. Annuity per 100 000 € of *Einmalbeitrag*, monthly in advance,
**[std]** (11):

| Age at *Rentenbeginn* | i = 0,25 % | i = 1,00 % | i = 1,75 % | uplift 0,25 % → 1,00 % |
|---|---|---|---|---|
| 60 | 314.43 | 352.08 | 391.63 | +12.0 % |
| 65 | 369.64 | 407.98 | 447.93 | +10.4 % |
| 70 | 443.58 | 482.84 | 523.40 | +8.9 % |
| 75 | 544.89 | 585.32 | 626.75 | +7.4 % |
| 80 | 687.02 | 728.86 | 771.44 | +6.1 % |

The corresponding annuity-due factors `a12(x, i)` at 1,00 % are 23.669, 20.426, 17.259, 14.237 and
11.433, so any cell can be checked as `100 000 / (12 × a12)`.

11. **[std]**, reproducible from the printed parameters, and **not any carrier's quotation.**
    Two forces will move a real tariff away from this table in both directions: carriers price
    below the cap [S6], and their first-order margin is heavier or lighter than this proxy. Two
    further forces move it over time: continuing improvement inside the *Trendfunktion* raises
    annuity values for each successive cohort, and any strengthening of the first-order margin
    does the same [R10] [REG-R49] — so **two cohorts buying ten years apart at the same
    *Rechnungszins* would not get the same annuity.**

**What is guaranteed, and what is not.** The *garantierte Rente* computed at inception is
guaranteed **for life** and is not adjustable. § 163 VVG is the only channel by which a German
life insurer may change a contract term after conclusion, and it requires three cumulative
conditions — a change in the *Leistungsbedarf* that is neither temporary nor foreseeable; a new
term that is appropriate and necessary to secure permanent fulfilment; and confirmation by an
independent *Treuhänder* — while expressly excluding adjustment to the extent the benefits were
insufficiently calculated in the first place [REG-R27]. The Landgericht Köln held the low-interest
phase **not** a sufficient ground, being entrepreneurial risk that cannot be passed to
policyholders (case reference and date not established) [R4]. A delib model therefore treats the
*garantierte Rente* as **immutable** and records § 163 as a model risk rather than a mechanic.

### *Rentengarantiezeit*

**The rule.** A guaranteed payment period runs from *Rentenbeginn*. **If the annuitant dies inside
it, the annuity continues to be paid to the beneficiaries until the agreed number of years has
expired** — the corpus's illustration is a 10-year period with death after six years, the spouse
receiving the remaining four [R23]. If the annuitant survives it, it lapses silently and the
annuity continues for life; afterwards nothing is payable on death unless a *Kapitalrückgewähr* or
a *Hinterbliebenenrente* was also bought.

**What it does.** It converts the first `n` years of the stream from a contingent payment into a
**certain** one. That is the arithmetic statement and it is the whole of the modelling
consequence: during the guarantee the payment must **not** be decremented for survival, and after
it, it must be. A model applying survival probabilities across the whole stream understates the
liability; one applying none overstates it.

**Where it sits in the market.** It is a tariff-level design feature carried in the product name
at NÜRNBERGER, whose deferred AVB is titled "… mit aufgeschobener Rentenzahlung **und
Rentengarantiezeit** nach Tarif NIR3301" [S5], and a policyholder-selectable parameter with a
contractual floor at Allianz, where the guarantee period "can be set to a minimum" [S7]. A
*Sofortrente* with **no** guarantee period is therefore a configuration, not the default.
Durations offered are **5, 10, 15, 20, 25 or more than 30 years**; typical durations are **15
years for retirement ages 61–70 and 10 years for 71 and above**; **most policyholders choose 10 to
20 years** [R23].

**What it costs**, on the [std] proxy basis at 1,00 %, age 65, per 100 000 € **[std]** (12):

| *Rentengarantiezeit* | `a12` | Monthly annuity | Reduction |
|---|---|---|---|
| none | 20.426 | 407.98 | — |
| 5 years | 20.530 | 405.92 | 0.51 % |
| 10 years | 20.897 | 398.78 | 2.26 % |
| 15 years | 21.624 | 385.38 | 5.54 % |
| 20 years | 22.821 | 365.16 | 10.50 % |
| 25 years | 24.591 | 338.87 | 16.94 % |
| 30 years | 26.972 | 308.97 | 24.27 % |

12. **[std]**, same basis, with `a12` replaced by an annuity-certain-due of `n` years plus an
    `n`-year-deferred life annuity. **The cost rises steeply with age, because the guarantee bites
    sooner**: a 10-year guarantee costs 2,26 % of the annuity at 65, 4,10 % at 70 and 7,42 % at
    75; a 20-year guarantee costs 10,50 %, 17,20 % and 26,71 % at those three ages. That is why
    the market's typical duration falls with age [R23]. A cross-check the corpus supplies: a
    consumer illustration on a *deferred* contract — 200 €/month over 30 years producing
    573 €/month with no guarantee — puts a 10-year guarantee at 3 €, a 20-year at 15 € and a
    30-year at 46 €, i.e. roughly 0,5 %, 2,6 % and 8,0 % [R23]. Materially cheaper at every
    duration, which is what one would expect from an annuity starting at a lower age with a longer
    expected duration: consistent in shape, different in level for a stated reason, and **neither
    is a tariff**.

**Two settlement forms exist and only one is modelled.** On death inside the period the
instalments may continue as they fall due, or the present value of the *Restgarantiezeit* may be
commuted to a lump sum. **Which form German carriers use, and on what basis a commutation would be
struck, was not established** (research gap 10). The reference implementation pays the
instalments — the form [R23] describes.

### *Kapital-* und *Beitragsrückgewähr*

**The rule.** On death the insurer refunds the *Einmalbeitrag* **less the annuity instalments
already paid**, floored at zero. The benefit therefore starts at the full *Einmalbeitrag* and runs
to nothing over roughly the period in which the annuitant recovers the capital nominally — on the
[std] basis, about **21,5 years** at age 65, i.e. to about age 86.

**What it does, and the trap inside it.** Because the refund is `Einmalbeitrag − instalments
paid`, and a *larger* refund means a *smaller* annuity, and a smaller annuity means the refund
runs off more slowly, the pricing equation is **implicit in the annuity**:

    Einmalbeitrag = 12 × R × a12(x, i) + PV( max(Einmalbeitrag − 12 × R × t, 0) payable on death at t )

It must be **solved**, not evaluated. An implementation that computes the plain annuity first and
then subtracts a refund cost gets a different — and wrong — answer. That is a numbered pitfall in
the technical notes and a test in the test module.

**What it costs.** On the [std] basis at 1,00 %, age 65, per 100 000 €, the monthly annuity falls
from **407,98 €** to **335,48 €**, a reduction of **17,8 %** **[std]** (13) — materially more than
a 20-year *Rentengarantiezeit* (10,5 %), and the honest answer to a buyer who asks why the
"money-back" version pays so much less.

13. **[std]**, solving the implicit equation above with deaths taken at mid-year and the refund
    discounted from mid-year. Variants named in the German market — ***volle Beitragsrückgewähr***
    (the full unconsumed *Einmalbeitrag*), a stated percentage, or a refund capped at a number of
    years' payments — exist, but **no carrier's variant was established**.

**Its relation to the *Rentengarantiezeit*.** The two protect the same risk in different shapes —
a fixed number of payments against a declining lump sum — and are usually offered as
alternatives; **which carriers permit the combination was not established** (research gap 10). The
representative design treats them as **mutually exclusive [std]**, and the reference
implementation asserts that exclusivity rather than silently permitting a configuration no source
supports.

### *Hinterbliebenenrente* and its *Anwartschaft*

**The rule.** A second life — the *mitversicherte Person*, in practice a spouse or registered
partner — is named at inception. While the annuitant lives, the main annuity is paid and the
second life holds an ***Anwartschaft***: a contingent, not-yet-payable entitlement. On the
annuitant's death, if the second life is then alive, the *Hinterbliebenenrente* begins at a stated
percentage of the annuitant's annuity and is paid for that life's remaining lifetime. **If the
second life predeceases the annuitant the entitlement lapses and nothing is refunded** — the cover
has been consumed.

**What it does.** It makes the contract a **joint-life-last-survivor** annuity: the liability runs
until *both* lives are dead, so the second life's age and sex matter as much as the annuitant's.
The second life is fixed at inception and generally cannot be substituted — a later marriage does
not acquire the entitlement [unverified].

**Its legal shape, and the modelling consequence that follows from it.** The German market treats
the survivor's annuity as a ***Zusatzversicherung*** — a rider with its own condition set,
attached to the base contract rather than being a benefit of it — and the GDV publishes model
conditions for exactly that [S9]. So in the reference implementation it is a **separate module
with its own insured life, off in the base run**, rather than a term in the main annuity's benefit
formula. Typical percentages are **60 % and 100 %** [unverified]; **no carrier's menu was
established**.

**What it costs**, on the [std] proxy basis at 1,00 %, annuitant 65 and second life 62 on the same
mortality, per 100 000 € **[std]** (14): 60 % survivor → `a12` 23.838, annuity **349,58 €**, a
reduction of 14,3 %; 100 % survivor → `a12` 26.113, annuity **319,12 €**, a reduction of 21,8 %.

14. **[std]**, applying the same mortality to both lives and assuming independence, both of which
    are simplifications: real joint-life pricing uses sex-distinct or portfolio-mix bases and a
    dependence allowance. The payout-plan exhaustion figures quoted in the overview are on the same
    basis: 100 000 € drawn monthly in advance is exhausted after 23,8 / 32,2 / 41,1 years at
    350 €/month and 0 % / 2 % / 3 % interest, and after 20,8 / 26,9 / 32,3 years at 400 €/month.

### Payment frequency and timing

**The rule.** The annuity is **monthly** [S7] [R23] and ***vorschüssig*** — payable in advance, at
the start of each payment period — with the first instalment at or within a month of inception.
Quarterly, half-yearly and annual frequencies exist as options [unverified].

**What it does.** It fixes the grid of the whole model. A monthly-in-advance stream is an
annuity-**due**, and every arithmetic in this specification uses one. **No source in the delib
corpus states the timing convention in terms**, for this product or the deferred one, so
*vorschüssig* is a **[std]** convention with the gap stated beside it, not an established fact —
and it is worth about **5 %** of the annuity (footnote 8, research gap 11). No loading or discount
for choosing a non-monthly frequency was established at any carrier.

### *Überschussbeteiligung* in the *Rentenbezug*

**The rule.** The annuity actually paid is `garantierte Rente + Überschussrente`. Only the first is
a promise. The second is declared annually out of surplus actually earned and **can move down as
well as up**. Participation is a **statutory right, not a marketing feature**: § 153 VVG entitles
the policyholder to a share of the *Überschuss* and of the *Bewertungsreserven* unless
participation is excluded by express agreement, and such an exclusion can only be made for the
whole of the profit participation [REG-R24]. The statute names the principle — a
*verursachungsorientiertes Verfahren* — and **does not prescribe the algorithm**, which is
precisely why every level below is **[std]** [REG-R24].

**It does not stop at *Rentenbeginn*.** Zurich Deutscher Herold's deferred pack describes the
transition to annuity payment as a key point for participation in *Bewertungsreserven* and states
that policyholders **also participate during the annuity payment period**, in accordance with the
applicable VVG and supervisory provisions, § 153 Abs. 3 VVG currently providing for *hälftige*
(equal) participation [S3] [REG-R24]. This is the only clause-level evidence in the delib corpus
that surplus participation continues in the payout phase, and it is load-bearing for the whole of
this section.

**The four *Überschussverwendung* forms**, elected at *Rentenbeginn* — here at inception, once,
irrevocably [unverified]:

| Form | Mechanic | Payment stream |
|---|---|---|
| ***konstante Überschussrente*** | The insurer fixes the total annuity at *Rentenbeginn* from the *garantierte Rente* plus a surplus share **projected for the whole annuity period**, and intends to hold it level [R21] | Highest at outset; flat thereafter **in intention only** |
| ***steigende (volldynamische) Überschussrente*** | The annuity **adjusts annually and flexibly to the actual surplus development** [R21] | Lowest at outset; rises each year surplus is declared |
| ***teildynamische Überschussrente*** | Part of the expected surplus is applied under the constant system and part under the dynamic one, so the annuity rises regularly by a **fixed percentage** provided the insurer earns corresponding surpluses [R21] [R23] | Intermediate at outset; rises at a stated rate, subject to surplus |
| ***Bonusrente*** | Declared surplus **buys a paid-up increment of annuity**, permanently added to the payment [R23] | Ratchets: each increment, once bought, does not come back off |

**The *Bonusrente* is the mechanism underneath the rising forms, not a fourth alternative.** That
is the corpus's reading [R23]: what makes a *volldynamische Rente* **ratchet rather than
fluctuate** is that its increments are bought as paid-up annuity. A carrier may market
*Bonusrente* as an option in its own right; a model treats it as the crediting mechanism and the
three dynamics as the profile.

**The single most important thing to understand about this product: the constant form is not
constant.** The total annuity under it is set from a **projection** of surplus over the whole
remaining lifetime; if the insurer earns less than projected, **the annuity is reduced** [R21]. A
model that treats the *konstante Überschussrente* as a level guaranteed stream models less than it
thinks. Only the *garantierte Rente* inside it is guaranteed, and the gap between the two — on
typical market designs, of the order of 15 % to 25 % of the payment [unverified] — is the amount
at risk. The trade-off across the four forms is one of timing, not of amount: all four distribute
the same expected surplus, the constant form front-loading it and carrying reduction risk, the
volldynamic form back-loading it and carrying the risk of dying before collecting. Franke und
Bornberg titled its treatment "Die Qual der Wahl" [R20] — there is no dominant answer.

**Nothing about the level was established.** No *Überschussrentensatz*, no *laufende Verzinsung*,
no *Zinsüberschussanteil* on the *Deckungsrückstellung* of annuities in payment, no dynamic
percentage, no *Bewertungsreserven* amount, at any carrier, for any year (research gap 4). [S10]
establishes the document class that publishes them — a carrier's annual *Überschussverteilung*,
current to 2026 — and nothing inside it; [R22] establishes the 24th edition of the market study
that aggregates them and nothing inside it. What the cross-product library does supply is the
market average for the accumulation side, and it must be read carefully: the German declared rate
is the ***laufende Verzinsung***, which is the *Garantieverzinsung* **plus** the *laufende
Zinsüberschussbeteiligung*, **not a surplus rate on top of the guarantee** — averaging **2,53 %
Klassik / 2,58 % Neue Klassik** for 2025, with three incompatible figures reported for 2026
(2,6–2,7 %, 2,87 % and 2,54 %) [REG-R53]. Adding a declared rate to a guaranteed rate is the
commonest arithmetic error in describing a German contract and is a numbered pitfall in every
affected delib product.

### Where the surplus comes from

**Three sources, unequally important for an annuity in payment.** The ***Zinsüberschuss*** — the
excess of actual investment return over the *Rechnungszins* on the *Deckungsrückstellung* — is
dominant here, because the reserve is large from day one and runs off slowly over decades. The
***Risikoüberschuss*** is, for an annuity, a **longevity** result rather than a mortality one: it
is positive when annuitants die **faster** than the first-order table assumed and negative when
they live longer, and it is the source that can go the wrong way for a whole cohort at once. The
***Kostenüberschuss*** is small in absolute terms, because a *Sofortrente* has one acquisition
event and then a long, cheap payment routine.

**The statutory floor.** The MindZV fixes a minimum share of each result that must be credited to
policyholders, computed separately: **90 % of the *Kapitalanlageergebnis* less the
*Rechnungszinsen*** — the guarantee is funded first and only the excess is shared — **90 % of the
*Risikoergebnis***, raised from 75 % by the LVRG with effect from 7 August 2014, and **50 % of the
*übrige Ergebnis*** [REG-R18] [REG-R20]. The *Direktgutschrift* is **deducted** from the sum and a
mathematically negative minimum is replaced by zero, which is why the MindZV is a minimum
**transfer to the *Rückstellung für Beitragsrückerstattung* (RfB), not a minimum payout**
[REG-R18]. Above it sit the RfB's own rules: § 140 VAG's ring fence and its escape hatches
[REG-R10], and the RfBV's ceiling on the *ungebundene* part with its *kollektiver Teil*
[REG-R19] — the device that makes cross-cohort smoothing legally possible without breaching the
§ 138 Abs. 2 VAG equal-treatment rule [REG-R8].

**The competition for the same money, and why it is a first-order driver here.** The
*Überschussrente* is paid from the same RfB that financed the ***Zinszusatzreserve*** (ZZR), the
additional HGB reserve arising when the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's
tariff rate [REG-R17]. The ZZR build-up suppressed declarations across the German market for a
decade; its release should work the other way. On trade-press figures — **never a supervisory
source** — the ZZR stood at about **84 Mrd €** at the 2024 balance-sheet date against a **96 Mrd €**
peak at end-2021, **2024 was the first year since introduction in which insurers had to add
nothing at all**, and about 5 Mrd € flowed back industry-wide, with a further 4 Mrd € for 2025;
released funds reach policyholders **through a higher *Überschussbeteiligung*** [REG-R17]. For a
cohort of German annuitants that release profile is the single largest driver of what they will
actually receive over the next decade, and a model projecting a flat surplus rate is ignoring it.

### The *Aufschubzeit* variant

**The rule.** The *Einmalbeitrag* is paid now and the annuity begins **after a short deferment**,
typically one to fifteen years. **No carrier's terms were established**; the Mecklenburgische
"Rente flex" is the corpus's only candidate and its feature is unestablished [S14].

**What it does — three things at once, which must not be conflated.** Interest accrues at the
*Rechnungszins*, so more capital is annuitised. **Mortality accrues**, so the survivors share the
fund of those who died — the survivorship credit that makes deferral powerful, and the reason the
deferment death benefit is a first-order design question rather than a detail. And the annuity
starts at an older age, so `a12` is smaller for two reasons at once.

**The death benefit during the deferment is what the variant turns on.** Two forms exist: a
**pure deferred annuity** with no death benefit, the fund of those who die being forfeited to the
survivors; and a *Beitragsrückgewähr* form refunding the *Einmalbeitrag* on death before
*Rentenbeginn*, much the more common retail form. **Neither was established for this product.**
Order of magnitude on the [std] basis at 1,00 %, purchase at exact age 65, 100 000 €, monthly in
advance **[std]** (15): a 2-year deferment gives 451,43 € without a deferment death benefit and
444,07 € with full *Beitragsrückgewähr*; 5 years gives 532,48 € and 508,12 €; 10 years gives
732,64 € and 651,24 €, against 407,98 € with no deferment.

15. **[std]**, same basis, gross of charges. A five-year deferment raises the annuity by about
    **25 %** with a death benefit and **31 %** without, and the gap between the two columns —
    4,6 % at five years, 11,1 % at ten — **is the price of the death benefit**, which is the honest
    way to present it.

### No surrender, no lapse, no *Beitragsfreistellung*

**The rule** and its consequences are set out under *Termination and values* above and are not
repeated. What belongs here is the **positive** statement a reader of a projection model needs:
the *Sofortrente* is the one German retail life product whose only decrement is death. Everything
else that would ordinarily appear in a liability model — a *Rückkaufswert* table, a *Stornoabzug*,
a five-year cost-spreading floor [REG-R28], a *Beitragsfreistellung* conversion, a lapse rate, a
dynamic surrender formula, a duration-12 tax threshold driving surrender behaviour [REG-R45] — is
**absent by specification**. The consumer warning that follows is the first thing every German
consumer page about this product says: the *Einmalbeitrag* is **irreversibly committed** [R21]
[R23].

---

## Riders and options

**In scope, and carried as model-point parameters:**

- **The *Rentengarantiezeit***, 0 to 30 years, priced as an annuity-certain floor on the first
  `n` years of the stream [R23] [S5] [S7].
- **The *Kapital-/Beitragsrückgewähr***, a declining refund on death netted against the guaranteed
  instalments already paid, solved implicitly [R23]; mutually exclusive with the guarantee period
  and with the survivor's annuity **[std]**.
- **The *Hinterbliebenenrente***, a *Zusatzversicherung* with its own second life and its own
  *Anwartschaft*, at 60 % or 100 % [S9]; **off in the base run**, because the German market treats
  it as a rider with its own condition set rather than a benefit of the base contract.
- **The *Aufschubzeit***, 0 to 15 years, with the deferment death benefit taking the same refund
  form; **off in the base run** [S14].
- **The *Überschussverwendung* form** — *konstant*, *teildynamisch*, *volldynamisch* or none —
  parameterised as an opening surplus percentage and an annual growth rate [R20] [R21] [R23], both
  **[std]**.
- **Payment frequency and timing** — monthly, quarterly, half-yearly or annual; *vorschüssig* or
  *nachschüssig* — both carried so that the unestablished timing convention (footnote 8) can be
  switched and its 5 % effect measured rather than assumed away.

**Out of scope, and said so rather than left to be discovered:**

- ***Bewertungsreserven* participation.** It continues throughout the payout phase and is a
  statutory entitlement [S3] [REG-R24], but it is path- and balance-sheet-dependent in a way a
  gross liability cash-flow model cannot reproduce: it is recomputed annually on the HGB accounts
  and reduced by the *Sicherungsbedarf* test of § 139 VAG and MindZV §§ 11–13, which compares a
  single month-end Bundesbank swap rate with the highest *Rechnungszins* applicable over the next
  fifteen years — a window that "bites hardest on annuity business" [REG-R18] [REG-R9]. The
  reference implementation models the declared *Überschussrente* explicitly and treats the
  *Bewertungsreserven* share as an **explicitly excluded component**.
- **A commuted settlement of the *Restgarantiezeit*.** The alternative settlement form on death
  inside the guarantee period; neither its use nor its basis was established (research gap 10).
- **A *Kapitalwahlrecht* or partial commutation after *Rentenbeginn*.** There is none [R1].
- **Indexed or inflation-linked annuities.** Not established to exist in the German retail
  *Sofortrente* market and not asserted to.
- **Impaired-life (*enhanced*) annuities.** Not established to exist in Germany.
- **Proof of life.** Failure to return the annual certificate suspends payment until it arrives —
  a timing effect on an otherwise unchanged obligation, not modelled.
- **The *fondsgebundene Sofortrente*** expressed in *Renten-Bezugseinheiten*, which belongs to
  `fondsgebundene_rentenversicherung`.

---

## Variations across insurers

**This specification supports no numeric variation table, and the reason is stated rather than
worked around.** No search was run for this product, so no carrier's *Rentenhöhe*, charge,
envelope, option menu or surplus rate was observed, and a table with a column per carrier would be
fabrication. Twenty-eight German life insurers are named in the research file as writers of the
right kind of business — Allianz, R+V, Debeka, Generali and CosmosDirekt, Dialog, HDI, Alte
Leipziger, LV 1871, Continentale and Europa, NÜRNBERGER, Swiss Life, Zurich Deutscher Herold,
ERGO, AXA, Barmenia, Hannoversche, Württembergische, Gothaer, Stuttgarter, Volkswohl Bund,
Baloise, Universa, DEVK, Signal Iduna, Provinzial, HUK-Coburg, Konzern Versicherungskammer and
Mecklenburgische [S13] — and **not one has a rate, a charge, an envelope or an option menu
attached**. Naming a carrier here asserts only that it is a German life insurer of the right kind;
it does not assert that it sells this product today.

### What each document in the corpus does establish

| Carrier | Document | What it establishes for this product |
|---|---|---|
| Zurich Deutscher Herold | [S2] immediate annuity, Fassung 01/2022; [S3] deferred, Fassung 01/2026 | that a conventional immediate-annuity pack exists in the same series as the deferred one (**no clause content**); and from [S3] the two-factor rule at *Rentenbeginn* and that *Bewertungsreserven* participation **continues in the payout phase** |
| NÜRNBERGER | [S4] AVB `gn331303_p`, *mit sofort beginnender Rentenzahlung* | that an insurer AVB for exactly this product exists, in the same numbered family as the deferred and unit-linked ones — so German insurers draft the immediate annuity as a member of the deferred series, not as a separate line |
| NÜRNBERGER | [S5] AVB tariff NIR3301 | the *Rentengarantiezeit* as a **tariff-level feature carried in the product name** |
| CosmosDirekt (Generali) | [S6] AVB LA 904 A | the conversion basis: **DAV 2004 R**, interest **0 % p.a.** at an unestablished vintage; and the standard surplus disclaimer |
| Allianz | [S7] KomfortDynamik page | that the current annuity factor **is** the carrier's immediate-annuity tariff; that the *Rentengarantiezeit* has a settable minimum |
| Debeka | [S8] B LV series, *Privatrente* page | the *Deckungskapital* definition this file's *Nettoeinmalbeitrag* degenerates from; the *Ertragsanteil* framing from an insurer's own page |
| GDV | [S1] [S9] | the model-conditions taxonomy, the **absence** of an immediate-annuity model set from it, and the survivor's annuity as a **rider with its own conditions** |
| Konzern Versicherungskammer | [S10] *Überschussverteilung 2026* | the annual surplus-declaration document class, current to 2026; **no rate** |
| Stuttgarter, Mecklenburgische | [S14] | that *Verbraucherinformation*, *Vertragsinformationen* and *Allgemeine Informationen* name the same pre-contractual pack |

**One negative finding worth recording.** The GDV maintains *Musterbedingungen* for the deferred
annuity, the *Basisrente*, two Riester wrappers and the *Hinterbliebenenrenten-Zusatzversicherung*
[S1] [S9] [REG-R37], and **no model condition set for a *Rentenversicherung mit sofort beginnender
Rentenzahlung* appears in that list**. Whether the association maintains one under another title,
or whether the market drafts from the deferred template with the *Aufschubzeit* set to zero, was
**not established** (research gap 3). [S2] and [S4] — immediate-annuity documents sitting inside
their carrier's deferred-annuity families — point to the second reading, but that is an inference
and is not asserted downstream.

### Structural variation the corpus supports

| Feature | Variants that exist | Evidence |
|---|---|---|
| *Rentengarantiezeit* | 5 / 10 / 15 / 20 / 25 / 30+ years, or none; typical 15 years to age 70 and 10 thereafter; most choose 10–20 | [R23]; tariff-level [S5]; settable minimum [S7] |
| Settlement inside the guarantee period | instalments continue, **or** the *Restgarantiezeit* is commuted | mechanic recorded; **which carriers use which, not established** |
| Death benefit menu | *Rentengarantiezeit*, *Kapital-/Beitragsrückgewähr*, *Hinterbliebenenrente*, or none | sections above; **no carrier's menu established** |
| Survivor's annuity | a *Zusatzversicherung* with its own condition set; 60 % and 100 % are the market's standard levels [unverified] | [S9] |
| *Überschussverwendung* in payout | konstant / teildynamisch / volldynamisch (steigend) / *Bonusrente* | [R19] [R20] [R21] [R23] |
| *Bewertungsreserven* in payout | continue, currently at equal participation | [S3] [REG-R24] |
| Interest basis of the guarantee | at or **below** the *Höchstrechnungszins*; **0 %** observed at one carrier | [S6] [REG-R14] |
| *Aufschubzeit* | 0 years (pure *Sofortrente*) or a short deferment | [S14]; **no carrier's range established** |
| Payment frequency | monthly standard; other frequencies [unverified] | [S7] [R23] |
| Distribution form | direct writer, broker, bancassurance, public-sector mutual — all present among the named carriers | [S13] |

### Parameters whose range is unknown

*Rentenhöhe* per 100 000 € at any age, carrier or year; the spread between the best and worst
quotation; α and β; *Effektivkosten* or *Renditeminderung*; the *Einmalbeitrag* and entry-age
envelopes; every surplus rate and every *Rentenanpassung* actually declared; the split of new
business between the four *Überschussverwendung* forms; the take-up of *Kapitalrückgewähr* against
*Rentengarantiezeit*; the market's size and average ticket. **Every one is a gap, not an
omission.** A reader who needs to know how German carriers differ on this product will find
nothing here and should start with a *Produktinformationsblatt* [S11], Stiftung Warentest's
periodic *Sofortrente* comparison [R21] and the dedicated comparison portals [R23] — in that
order, and none of them was located.

---

## Regulatory context

**Contract law — the VVG.** The contract is an ordinary *Lebensversicherung* under Kapitel 5 of
the VVG, whose provisions are largely *halbzwingend*: they may be varied only in the
policyholder's favour [REG-R22]. Six articles do the work. **§ 153** gives the statutory
*Überschussbeteiligung*, requires a *verursachungsorientiertes Verfahren* without prescribing the
algorithm, and requires the *Bewertungsreserven* to be recomputed annually and shared, currently
*hälftig*, subject to the LVRG's *Sicherungsbedarf* override [REG-R24] [REG-R20] [S3]. **§ 154**
requires a *Modellrechnung* wherever the insurer makes quantified statements about benefits beyond
the guaranteed ones — which a *Produktinformationsblatt* quoting a *Gesamtrente* does — computed
on the premium-calculation bases at **three interest rates set by § 2 Abs. 3 VVG-InfoV as the
*Höchstrechnungszins* × 1,67, that rate plus one point and that rate less one point**; at the
current 1,00 % the statutory triple is therefore **1,67 % / 2,67 % / 0,67 %** [REG-R25] [REG-R15].
**§ 155** requires an annual *Standmitteilung* in *Textform* disclosing the current status of the
policyholder's claims including profit participation and **to what extent that participation is
guaranteed**, and requires deviations from any statements made about future development to be
reported — which makes a published *Standmitteilung* a legitimate primary source class for
declared rates, and the absence of one from this corpus a real gap [REG-R25] [S15].
**§§ 150, 159–162** carry consent, the *Bezugsberechtigung* and its revocability, and the suicide
and unlawful-killing exclusions [REG-R26]; the three-year suicide bar is a *Todesfallversicherung*
rule and reaches this product only through the death benefits, which are refunds of the
policyholder's own capital rather than sums at risk. **§ 163** is the sole channel for changing a
contract term after conclusion and is narrow [REG-R27] [R4]. **§§ 165–170** carry
*Beitragsfreistellung*, termination, the *Rückkaufswert* with its five-year cost-spreading floor
and the *Stornoabzug* — and **none of them operates on this product once the *Rentenbezug* has
begun** [REG-R28] [R1] [R2] [R5]. The *Widerrufsrecht* is 30 days for life insurance [REG-R23].

**Tariff bases — the DeckRV and the DAV.** § 2 DeckRV fixes the *Höchstrechnungszins*, the maximum
rate at which the statutory *Deckungsrückstellung* may be discounted, and through § 138 Abs. 1
VAG's requirement that premiums be adequate to fund that reserve it caps the rate at which a new
tariff may be priced [REG-R14] [REG-R8]. **The rate applies at the time of contract conclusion and
then stays with the contract for its whole term**, which is why the German in-force book is a stack
of cohorts and why every delib model point carries its cohort's rate rather than today's: 3,50 %
to mid-1994; 4,00 % to mid-2000; 3,25 %; 2,75 %; 2,25 %; 1,75 %; 1,25 %; 0,90 %; 0,25 % for
2022–2024; **1,00 % from 2025** [REG-R15]. The instrument for the current rate is the *Sechste
Verordnung zur Änderung von Verordnungen nach dem Versicherungsaufsichtsgesetz* of 19 July 2024,
BGBl. 2024 I Nr. 250 [REG-R15]. The rate itself is set by the Bundesministerium der Finanzen on an
annual DAV recommendation — **practice, not law** — built from model calculations on a
representative *Neuanlageportfolio*, stochastically weighted scenarios, a five-year average and a
***Sicherheitsabschlag* of 40 %** [REG-R56]. **§ 4 DeckRV's *Höchstzillmersatz* of 25 ‰ does not
reach this product at all**, there being no *Beitragssumme* to zillmer against [REG-R16].
No statute names a mortality table: § 138 VAG requires prudent assumptions and § 2 DeckRV
prudently chosen bases, and the gap between "prudent" and "this specific `q_x`" is closed by the
*Verantwortlicher Aktuar* under § 141 VAG exercising professional judgement [REG-R56] [REG-R11].
**A German biometric basis is therefore soft law with hard consequences**, and an insurer may use
its own table: DAV 2004 R is a market default and benchmark, not a legal mandate [REG-R47]
[REG-R49].

**Unisex.** The ECJ held on 1 March 2011 in C-236/09 (*Test-Achats*) that using sex as a risk
factor in insurance is incompatible with the Charter and invalidated the Gender Directive's
derogation **with effect from 21 December 2012**; from that date sex may not lead to different
premiums or benefits for new contracts. On the German side § 19 AGG carries the prohibition and
names private insurance, § 20 Abs. 2 Satz 1 AGG — which had permitted sex-differentiated
actuarial pricing — **was repealed**, and § 33 Abs. 5 AGG preserves the old treatment for
relationships concluded before that date [REG-R34]. **Every delib model prices unisex.** A model
point may carry a `sex` attribute for **decrement** purposes, because the underlying tables are
sex-specific [REG-R49], but sex must not enter the premium or the annuity factor; letting it leak
into pricing reproduces a tariff unlawful in Germany since 2012 and is a numbered pitfall.

**Surplus, the RfB and the supervisor.** The arithmetic floor is the MindZV's 90 / 90 / 50
[REG-R18]; the RfB's ring fence and escape hatches are § 140 VAG [REG-R10]; the *ungebundene*
part's ceiling and the *kollektiver Teil* are the RfBV [REG-R19]; the *Sicherungsbedarf* test on
*Bewertungsreserven* is § 139 VAG with MindZV §§ 11–13 [REG-R9] [REG-R18]; the equal-treatment
constraint that binds the whole scheme is § 138 Abs. 2 VAG, which the BGH tied to § 153 VVG in
IV ZR 436/22 of 18 September 2024 [REG-R8] [REG-R36]. All of it is computed on the **HGB**
accounts, not the Solvency II ones [REG-R54]. Assets sit in the *Sicherungsvermögen* under the
qualitative § 124 VAG prudent-person principle; the AnlV quotas German market writing routinely
cites **do not bind** a Solvency II life insurer and must not be applied here [REG-R7].

**Disclosure and distribution.** The VVG-InfoV prescribes the pre-contractual information pack —
the *Verbraucherinformation* / *Vertragsinformationen* / *Allgemeine Informationen* class [S2]
[S3] [S14] — and carries the *Effektivkosten* disclosure [REG-R31]. The PRIIPs Regulation
generates the *Basisinformationsblatt* with its *Risikoindikator*, four performance scenarios and
*Renditeminderung* figures [REG-R32] [S12] — but **whether a payout-only *Sofortrente* falls
inside PRIIPs scope was not established**: it looks like an insurance-based investment product on
the usual reading, while its payout-only character and the absence of any surrender value make the
holding-period and "what you might get back" sections awkward (research gap 8). If a
*Basisinformationsblatt* exists it is the **only** public document giving this product's cost in
the standardised *Renditeminderung* form, and none was located. Distribution runs under the IDD as
transposed on 20 July 2017 and § 34d GewO [REG-R33].

**Taxation.** The whole of a *Sofortrente*'s cash flow is taxed under **§ 22 EStG** on the
*Ertragsanteil* and **none of it under § 20** [R13] [R14] [REG-R41] [REG-R45]. Only the "Ertrag
des Rentenrechts" — the interest element deemed contained in the annuity — is income; the
return-of-capital element is not taxed at all. The fraction is fixed once by the annuitant's age
at *Rentenbeginn* and never changes: **18 % at 65** [R13], 22 % at 60 [REG-R41], the remainder of
the statutory schedule being [unverified] in its entirety with the 65 value as its only check.
On the constructed 389,99 € monthly annuity of footnote 10 the taxable amount is 70,20 € a month,
so the tax is **17,55 € — 4,5 % of the annuity** at a 25 % marginal rate and 29,48 €, **7,6 %**, at
42 % **[std]**. The § 20 Abs. 1 Nr. 6 *Halbeinkünfteverfahren* requires the contract to have run
twelve years and the payment to fall after the 62nd birthday, applies only to lump sums and
payout-plan withdrawals, and **does not apply to monthly annuity payments** [REG-R45]; a
*Sofortrente* bought at 65 has by construction not run twelve years when its first payment falls
due and pays no lump sum in any event. **That boundary is the product's main quantitative selling
point** against a *Bankauszahlplan* whose interest is taxed in full at the *Abgeltungsteuer* rate.
Two further points reach the buyer. A death benefit paid to a named beneficiary is an ordinary
*Erwerb von Todes wegen* under § 3 Abs. 1 Nr. 4 ErbStG at the beneficiary's own *Steuerklasse* and
*Freibetrag* — Germany has **no insurance-specific death-benefit tax regime** [REG-R46]. And
social insurance can reverse the tax argument: a Schicht-3 annuity is **not** a *Versorgungsbezug*
under § 229 SGB V, so a compulsorily insured pensioner pays no health or long-term-care
contribution on it — but **§ 240 SGB V reverses that for *freiwillig versicherte* members**, for
whom the whole economic capacity is contributory, expressly including private annuities
[REG-R46]. **Not established, and needed:** whether *Rentengarantiezeit* payments made to a
beneficiary keep the original *Ertragsanteil*; whether a *Kapitalrückgewähr* refund is taxable at
all; whether a *Hinterbliebenenrente* is re-based on the survivor's own commencement age; and the
*Solidaritätszuschlag* (research gap 15).

**Prudential and accounting — cited, never specified.** BaFin supervises German life insurers
under Solvabilität II as transposed into the VAG [REG-R1] [REG-R2] [REG-R5] [REG-R6], with
Directive (EU) 2025/2 amending the regime [REG-R3] and EIOPA publishing the risk-free curves
[REG-R4]. A German insurer values this book **twice**: the HGB *Deckungsrückstellung* on the
first-order bases, increased by the ZZR [REG-R14] [REG-R17] [REG-R54], on which the whole surplus
system operates; and the Solvency II best estimate at the EIOPA curve plus a risk margin
[REG-R6]. IFRS 17 is a third measure and a group-reporting one, German solo statutory accounts
remaining HGB [REG-R55]. **`delib` computes none of them.** The reference models publish gross
best-estimate-style liability cash flows per model point, income-positive and **undiscounted**;
the discounting, the margins, the *Deckungsrückstellung* recursion, the ZZR, the RfB as a
balance-sheet stock and the CSM belong to a layer above, and this specification names them so that
a reader knows what the model is an input to.
