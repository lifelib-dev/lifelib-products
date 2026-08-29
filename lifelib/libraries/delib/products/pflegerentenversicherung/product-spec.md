# Product Specification

**Status:** Draft, 2026-08-29 (research access date 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a German **Pflegerentenversicherung** — the individual,
privately written, single-life long-term-care annuity sold by a *Lebensversicherer*, which
pays a monthly *Pflegerente* for as long as the insured holds a contractual *Pflegegrad*
(statutory degree of care need). It describes **no single insurer's product**, and it must
not be read as one.

**How this composite differs from its frlib counterpart.**
`frlib/products/temporaire_deces/product-spec.md` is a composite of eight retrieved carriers,
seven of whose contracts were read in full. **Nothing was retrieved for this product.** Direct
HTTP egress from the build environment is blocked by an organisation network policy, and the
session's `WebSearch` budget was already exhausted when work on this product began, so there
was neither a retrieval channel nor a search channel. Not one *Bedingungswerk*, not one
*Produktinformationsblatt*, not one *Tarifblatt* and not one statutory text was opened. The
composite below is assembled from **document classes that exist and are the right kind of
document for this product**, and from the mechanics of German insurance law and German
actuarial practice, under the discipline house rule 3 imposes for exactly this case. **A delib
citation is a pointer, not a certificate:** `[R2]` beside a statement about § 15 SGB XI names
the instrument the statement should be checked against; it does not assert that anyone checked
it.

Facts carrying a source tag — [S#] (primary product document classes: *Musterbedingungen*,
*Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*, *Basisinformationsblatt*,
*Verbraucherinformation*, *Tarifblatt*) and [R#] (product-specific regulatory and actuarial
references), both numbered per `_research/pflegerentenversicherung.md` and resolved in
`sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
own R-numbering is distinct and also frozen) — name the instrument the claim belongs to.
Values marked **[std]** are standardizations introduced for the reference implementation;
each **[std]** table row carries a numbered footnote giving the rationale and, where the
research file recorded one, the observed or argued range. Claims no source could corroborate
are flagged [unverified], and on this product that is most of the specific numbers.

**Out of scope, and said so where it matters.** The *soziale Pflegeversicherung* of SGB XI
[R1] and the *private Pflegepflichtversicherung* of § 23 SGB XI [R7] are the compulsory first
layer and are described, not modelled. *Pflegetagegeldversicherung* and
*Pflegekostenversicherung* are written as *private Krankenversicherung* and are the contrast
documents of this file, never its subject [S2]. *Pflege-Bahr*, the subsidised cover of § 127
SGB XI, is confined by statute to the *Pflegetagegeld* form [R8]: **a
*Pflegerentenversicherung* cannot be a *geförderter Tarif***, and the *Zulage* is not modelled.
*Betriebliche Altersversorgung*, *Gruppenversicherung*, *Sterbegeldversicherung* and
institutional risk transfer are outside the delib library entirely. The neighbouring biometric
product is `products/berufsunfaehigkeit/` (`BU_DE_S`), which shares this product's chassis, its
waiver of premium and its multi-state modelling problem, and differs in trigger, in duration
and in the age at which the risk bites.

---

## Product overview and market role

### The three layers of German long-term-care funding

German long-term care is funded in **three layers**, and a *Pflegerentenversicherung* is the
third. The first is **compulsory statutory cover** — the *soziale Pflegeversicherung* (SPV) of
SGB XI [R1], or the *private Pflegepflichtversicherung* (PPV) of § 23 SGB XI for those insured
in the *private Krankenversicherung* [R7]; membership follows health insurance, so the layer is
universal, and it is a ***Teilleistungssystem*** by design, paying **defined amounts per
*Pflegegrad*** rather than the cost of care, with the residue falling on the insured person
[R1]. That constitutive choice, made in 1994 and never reversed, is the reason the third layer
exists as a market at all. The second layer is **the insured person's own resources**; the third
is **voluntary private top-up** or, failing that, means-tested *Hilfe zur Pflege* under §§ 61–66
SGB XII [R24].

The private product is sized against the gap the first layer leaves, and its benefit trigger is
**defined by reference to the first layer** rather than by an independent medical definition
[S1] [S4]. Both facts shape the model: the trigger is exogenous to the insurer, and the benefit
is a *Summenversicherung* payable irrespective of what care actually costs.

### The statutory first layer, quantified

All amounts as in force from 1 January 2025, per calendar month, and all `[unverified]`; no
figure below was confirmed by any retrieved document or search result, and whether any of
them changed on 1 January 2026 was not established (research gap 8).

| *Pflegegrad* | *Pflegegeld* (cash, informal care) | *Pflegesachleistung* (benefit in kind) | SPV contribution, *vollstationär* |
|---|---|---|---|
| 1 | none | none | 125.00 EUR (flat, not graded) |
| 2 | 347.00 EUR | 796.00 EUR | 805.00 EUR |
| 3 | 599.00 EUR | 1,497.00 EUR | 1,319.00 EUR |
| 4 | 800.00 EUR | 1,859.00 EUR | 1,855.00 EUR |
| 5 | 990.00 EUR | 2,299.00 EUR | 2,096.00 EUR |

Basis: home care [R3] [unverified]; residential care [R4] [unverified].

Three readings drive the private product's design. ***Pflegegrad* 1 is, for cash purposes,
uninsured by the state** — 125 € towards a *Pflegeheim* and an earmarked *Entlastungsbetrag* of
131,00 € a month, nothing else [R3] [R4] [R5] [unverified] — which is why most private
*Leistungsstaffeln*, and delib's, also pay nothing at grade 1. **The *Pflegegeld* is about 44 %
of the corresponding *Sachleistung*** at every grade [R3] [unverified], so the state pays
informal carers far less than professional ones, which is why roughly five in six
*Pflegebedürftige* are cared for at home [R18] [unverified]. And **the residential contribution
at grade 5 (2 096 €) is *lower* than the home *Sachleistung* at grade 5 (2 299 €)**
[R3] [R4] [unverified]: the scheme does not scale its residential contribution to the price of a
*Pflegeheim*, the facility sets the price, and the residue falls on the resident. That asymmetry
**is** the *Versorgungslücke*.

### The *Versorgungslücke* — the number the product is sold against

A resident of a *Pflegeheim* pays four separate components [R4] [R20]: the
***einrichtungseinheitlicher Eigenanteil*** (EEE), the care-related cost the SPV contribution
does not meet, **identical for *Pflegegrade* 2 to 5 within one facility** since 2017 [R9];
***Unterkunft und Verpflegung***; ***Investitionskosten***; and an ***Ausbildungsumlage*** where
levied. Only the EEE is equalised across grades and only the EEE is reduced by the § 43c
*Leistungszuschläge* — 15 % / 30 % / 50 % / 75 % in months 1–12, 13–24, 25–36 and from 37 on the
2024 step-up [R4] [unverified]. The other three are neither capped nor subsidised and are the
fastest-growing part of the bill [R20] [unverified].

| Line | Amount, 2025 | Basis |
|---|---|---|
| Average total resident payment, *Pflegeheim*, first year of stay | about 3,000.00 EUR/month | [R20] [unverified] |
| Less: net *gesetzliche Rente* of a median new retiree | of the order of 1,200.00 to 1,600.00 EUR/month | [unverified] |
| **Residual funded from savings, family or *Hilfe zur Pflege*** | **of the order of 1,400.00 to 1,800.00 EUR/month** | **[std]** (A) |

(A) The residual is arithmetic on the two lines above, not an observation. The *Eigenanteil*
figures are the least reliable numbers in the research corpus (research gap 15) and are used
here only to argue an order of magnitude. They are the reason the market sells *Pflegerenten*
of 1 000 € to 1 500 € a month [unverified], and the reason delib's `[std]` *vereinbarte
Pflegerente* is **1 000,00 € per month** — a round number at the lower end of that band, large
enough to close most of the gap for a resident with an average pension and small enough that
the resulting premium is recognisably a mass-market figure.

Two structural features of the gap matter for the model. **It widens over time**, because the
statutory amounts are uprated episodically by legislation [R10] while the *Eigenanteil* rises
with care-sector wage costs every year [R20] [unverified] — every uprating is a one-off catch-up
against a continuous drift, which is the case for the *Leistungsdynamik* option. And **it is
largest in the first year of a stay**, because the § 43c *Zuschläge* rise with length of stay
[R4] [unverified], so a constant annuity progressively over-covers it. No German wording is known
to offer a *decreasing* care annuity, and delib does not model one.

### The three private forms, and why the *Pflegerente* is one of them

| | *Pflegetagegeldversicherung* | *Pflegekostenversicherung* | ***Pflegerentenversicherung*** |
|---|---|---|---|
| Legal branch | private Krankenversicherung | private Krankenversicherung | ***Lebensversicherung*** |
| Benefit form | agreed daily/monthly cash per *Pflegegrad*, no proof of spend | reimbursement of a share of residual actual cost, invoices required | agreed **monthly annuity** per *Pflegegrad*, no proof of spend |
| Legal character | *Summenversicherung* | indemnity | *Summenversicherung* |
| Premium re-rating | **possible** under § 203 VVG on a trustee-approved trigger | possible | **not possible** save on the narrow § 163 VVG route |
| Ageing provision | *Alterungsrückstellung* where written *nach Art der Lebensversicherung*; **none** where written *nach Art der Schadenversicherung* | as *Pflegetagegeld* | ***Deckungsrückstellung*** always |
| Surrender value | none in substance | none | **yes**, § 169 VVG, subject to the open question below |
| Waiver of premium in claim | usual | usual | **usual, and contractual** |
| Death benefit | rare | none | **common option** |
| *Pflege-Bahr* eligible | **yes — the only eligible form** | no | **no** |
| Market share by contracts | **dominant** | negligible | small |
| Average premium | lowest | — | **highest** |

The branch, benefit-form, re-rating and *Pflege-Bahr* rows follow from [R11], [R14] and [R8]
and are structural. The market-share and average-premium rows are [unverified].

**The load-bearing difference is the re-rating power.** A *Pflegetagegeld* is health business:
on a deviation beyond an *auslösender Faktor* the insurer may raise the premium with a trustee's
agreement under § 203 VVG [R11] [R14]. A *Pflegerente* is life business, and the only route is
§ 163 VVG [REG-R27]. **A buyer at 45 who wants to know what the cover will cost at 80 gets an
answer from a *Pflegerente* and does not get one from a *Pflegetagegeld*.** Every consumer
comparison reduces to that trade, and so does the price difference: the *Pflegerente* costs more
because the insurer, not the policyholder, carries the basis risk on a fifty-year view of a
biometric table built on a superseded assessment regime [R15] [REG-R51]. The second difference
is the **ageing provision**: a *Pflegetagegeld* written *nach Art der Schadenversicherung* has
none, so its premium follows attained-age risk upward and becomes unaffordable at exactly the
ages the cover is needed [S11] [unverified]. The third is the **surrender value**, which cuts
both ways — it is the only one of the three from which a policyholder recovers anything on lapse
[REG-R28], and it makes the contract realisable assets in a *Hilfe zur Pflege* means test [R24].

### Market size

**There is no sourced count of German *Pflegerente* contracts in force anywhere in this
research** (research gap 12). The PKV-Verband series counts *health*-insurance top-up
contracts, so a *Pflegerente*, written by a *Lebensversicherer*, is not in it [S16] [R21]; and
the GDV life series does not carve the product out as a reported family [R22] [REG-R53]. What
can be said:

| Measure | Value | Year | Basis |
|---|---|---|---|
| *Pflegebedürftige* in Germany | about 5.7 million (about 5.0 million at end-2021) | end-2023 | [R18] [unverified] |
| Share cared for at home / in *vollstationäre Dauerpflege* | about 84–86 % / about 14–16 %, roughly 0.8 million people | 2023 | [R18] [unverified] |
| Projected *Pflegebedürftige* | of the order of 6.8 million | 2055 | [R19] [unverified] |
| Private LTC top-up contracts (health branch only) | of the order of 3.5 to 4.5 million, of which 0.8 to 0.9 million subsidised *Pflege-Bahr* | recent | [R21] [unverified] |
| ***Pflegerente* contracts in force** | **not established** | — | research gap 12 |

**Approximate distribution across *Pflegegrade*** [R18] [unverified], as shares because the
shape is more reliable than the counts: grade 1 about 9 %; 2 about 44 %; 3 about 27 %; 4 about
14 %; 5 about 6 %. The stock is heavily weighted to the lower grades, which is exactly why a
*Leistungsstaffel*'s **middle** steps drive its cost. **Age-specific prevalence** [R18]
[unverified] — the shape matters far more than the levels: under 1 % below 60; of the order of
10 % at 75–79; 20 % at 80–84; 40 % at 85–89; 70 % or more at 90 and above. **Prevalence roughly
doubles every five years of age above 75.** That curve is what the product is built on, and it
is why a level premium from age 45 accumulates for thirty-five years before it starts paying.

Qualitatively, and [unverified]: the *Pflegerente* is the **smallest of the three private forms
by contract count and the largest by average premium**, sold overwhelmingly through advised
channels. Penetration is low because the risk is distant, because *Hilfe zur Pflege* [R24] is a
visible backstop, because the *Angehörigen-Entlastungsgesetz* removed the *Elternunterhalt*
motive for all but high earners from 2020 [R24] [unverified], and because the products are hard
to compare.

---

## Representative specification

The representative design is a **composite**, not a carrier's tariff. Because no product
document of any kind was retrieved (research gap 14), every representative choice below is
argued against the **observed or argued range** the research file records, and every choice
that the corpus cannot source is a **[std]** standardization with a numbered rationale.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual, single-life, underwritten *Pflegerentenversicherung*; a **stand-alone contract**, not a rider on an endowment or a deferred annuity | [S4] |
| Legal branch | *Lebensversicherung*, written by a *Lebensversicherer*; calculated ***nach Art der Lebensversicherung*** — level premium, prospective *Deckungsrückstellung*, no ordinary re-rating | [R11] [R12]; [REG-R5] [REG-R8] |
| Benefit character | ***Summenversicherung***: an agreed monthly *Pflegerente*, paid without proof of expenditure and irrespective of the care setting | [S4]; setting-independence **[std]** (1) |
| Trigger | The statutory ***Pflegegrad*** determined under §§ 14, 15 SGB XI, normally by the *Medizinischer Dienst* for the statutorily insured or MEDICPROOF for the privately insured | [R2] [R6]; [REG-R51] |
| Lives basis | Single life. No joint-life *Pflegerente* is recorded anywhere in the corpus | [S4] [unverified] |
| Entry ages | **18 to 65** at entry, some tariffs to 70; purchase clusters at **45 to 60** | [unverified]; envelope **[std]** (2) |
| Cover period | **Whole of life.** The annuity is payable for as long as the insured holds an insured *Pflegegrad*, and the contract ends on death | [S4] [unverified] |
| Age basis | *Alter last birthday* at issue; the model steps the attained age at the policy anniversary | **[std]** (3) |
| *Vereinbarte Pflegerente* | **1 000,00 € per month** at *Pflegegrad* 5; market band 1 000 € to 1 500 € | **[std]** (4) |
| Currency | EUR | — |
| Sex | Carried for reporting and for the projection basis; **pricing is unisex** for contracts concluded from 21 December 2012 | [REG-R34]; blend **[std]** (5) |
| *Pflege-Bahr* eligibility | **None.** § 127 SGB XI confines the *Zulage* to a *Pflegetagegeld* conducted *nach Art der Lebensversicherung*; a *Pflegerente* cannot be a *geförderter Tarif* | [R8] [unverified] |
| Anchor model cell | Female, entry age 45, *vereinbarte Pflegerente* 1 000,00 €/month, `delib_std` *Leistungsstaffel*, lifelong monthly premium struck by equivalence, no *Wartezeit*, no *Karenzzeit*, no *Dynamik*, no *Todesfallleistung*, no *Stornoabzug* | **[std]** (6) |

Footnotes to **[std]** rows:

1. **Setting-independence is modern practice.** Older wordings paid the full annuity only for
   *vollstationäre* care and a reduced one at home [unverified]; modern practice pays irrespective
   of setting, which is what makes the product a *Summenversicherung*. A setting-dependent benefit
   would need a care-setting state the corpus supplies no transition data for.
2. **Observed entry ages: 18 to 65, some tariffs to 70** [unverified]. The composite takes 18–65
   as the envelope and 45 as the anchor because that is the lower edge of the observed *purchase*
   cluster, not of the permitted band — the two differ by twenty-five years, and conflating them is
   the commonest error in describing this product. Both boundary ages are exercised by model points.
3. No age basis is established for any *Pflegerenten* tariff; German practice uses the
   *versicherungstechnisches Alter* on carrier-specific rounding rules. The composite uses age last
   birthday at entry, the delib registry's convention; a different rule shifts the projection by at
   most one year of age.
4. **No *vereinbarte Rente* band was established from any product document** (research gap 1).
   1 000,00 € comes from the gap arithmetic above, sits at the lower end of the 1 000–1 500 € band
   the market is understood to sell [unverified], and is a **scaling constant** — every benefit is a
   percentage of it, so changing it rescales the whole liability linearly.
5. Unisex pricing is compulsory from 21 December 2012 [REG-R34], and matters more here than on any
   other delib product: **women have materially higher LTC incidence and longer care durations**
   [unverified], so the unisex premium embeds a cross-subsidy whose size depends on the sex mix
   written — itself endogenous to the price. The composite prices on a **50 / 50** blend **[std]**
   and projects on the point's own sex, so the cross-subsidy is visible rather than assumed away.
6. Entry age 45 gives a long enough pre-claim period for the *Deckungskapital* to be the object it
   is and makes the equivalence premium comparable with the argued band. The anchor is **female**
   deliberately: the projection then runs the higher-incidence basis against a unisex price.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium form | **Level monthly *Beitrag*, guaranteed for the life of the contract**, subject only to the narrow § 163 VVG route | [R11]; [REG-R27] |
| Premium-paying period | **Lifelong** in the base case, until death or the start of a waiver. Two alternatives are sold and are carried as options: an *abgekürzte Beitragszahlungsdauer* to a fixed age, typically **65** or **85**, and a single ***Einmalbeitrag*** | [unverified]; base choice **[std]** (7) |
| Payment frequency | Monthly, quarterly, half-yearly or annual, in advance | [S4] [unverified] |
| *Ratenzahlungszuschlag* | **Not modelled as a separate charge.** The instalment loading is folded into the single administration-cost assumption | **[std]** (8) |
| Premium level | **No German *Pflegerenten* rate card exists in this corpus.** The premium is struck by **equivalence** on the tariff (*erster Ordnung*) bases at the *Rechnungszins* | [R9] (absent); method [REG-R8] [REG-R47]; level **[std]** (9) |
| Argued premium band, 1 000 € *vereinbarte Rente*, `delib_std` grid, lifelong monthly premium, waiver, no death benefit, no dynamics | entry age 45: about **50,00 € to 100,00 €** per month; entry age 55: about **80,00 € to 160,00 €** per month | **[std]** (9) |
| Rating factors | Attained age at entry; *vereinbarte Rente*; the *Leistungsstaffel*; the premium-paying period; medical acceptance (*Risikozuschlag*). **Occupation is not a rating factor at all** — the sharpest single contrast with *Berufsunfähigkeit* | [S4] [unverified]; occupation [unverified] |
| *Risikozuschlag* | Carried as a model-point multiplier on the gross premium; **1.00** at standard rates. No scale was established | mechanics [S4] [unverified]; value **[std]** (10) |
| *Rechnungszins* | **1,00 %** p.a. — the *Höchstrechnungszins* of § 2 DeckRV for new business written from 1 January 2025 | [REG-R14] [REG-R15]; [R13] |
| Premium cessation | On death; on the start of an insured annuity (*Beitragsbefreiung*); at the end of the premium-paying period where one is agreed | [S4]; waiver **[std]** (11) |
| Premium revival | On a *Herabstufung* out of the annuity-paying grades, the premium obligation revives | [S4] [unverified] |
| Re-rating power | § 163 VVG only: a non-temporary, unforeseeable change in a calculation basis, a new premium that is appropriate and necessary, and an independent *Treuhänder*'s confirmation — and **excluded** where the original calculation was insufficient and a diligent actuary should have seen it | [REG-R27]; [R11] |

7. Three premium-paying periods are sold [unverified]: lifelong; to a fixed age; and a single
   *Einmalbeitrag*. The composite takes **lifelong**, the form that shows the *Deckungskapital*
   building and running off across the whole risk period. Both alternatives are model-point options
   and are exercised; the *Einmalbeitrag* is explicitly **not** the base model.
8. German tariffs load monthly, quarterly and half-yearly payment relative to annual [unverified];
   **no level was established** (research gap 2), and shipping a loading nobody sourced would put a
   fabricated price difference into the model. The frequency therefore changes the *timing* of
   premium income and nothing else. This is a stated departure from market practice and a listed
   pitfall, because a reader who reads a frequency difference off this model as a price difference
   reads it backwards: paying annually in advance is *earlier*, so the equivalence premium per month
   is slightly *lower*, the opposite sign to a real *Ratenzahlungszuschlag*.
9. **No German *Pflegerenten* premium was established from any source** (research gap 3) — the
   sharpest difference from `frlib/products/temporaire_deces`, which had a published rate card to
   reproduce. The band is derived arithmetic, set out in the research file § 23: a time-weighted
   average benefit of about 52 % of the *vereinbarte Rente* over a spell; about 25 000 € of expected
   nominal benefit per claim; a lifetime probability of reaching an insured grade of about 45 %; a
   mean age at first insured grade of about 82; discounting at 1,00 %; and a gross-to-net ratio
   between **2 and 3**. **It is not a market observation and must never be cited as one.** A model
   premium well outside it indicates an error in the bases; one inside it is not thereby validated.
10. Underwriting outcomes are documented in kind [S4] [unverified] but **no *Risikozuschlag* scale
    is public**, so the factor is a pure model-point input. It multiplies the **premium**, never the
    benefit.
11. Waiver detail that varies and was not established [unverified]: from which grade the waiver
    runs, whether it is full or proportionate, and whether the premium revives on a *Herabstufung*.
    The composite takes **full waiver, from the first month in which any annuity is payable, revived
    on exit from the paying grades** — the market-standard design, and the one that keeps waiver and
    benefit on a single trigger, which is what lets the model publish one `check_waiver()` identity
    reconciling both streams.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit | A monthly ***Pflegerente***, paid in advance, as a percentage of the *vereinbarte Pflegerente* set by the insured's current *Pflegegrad* | [S4] |
| ***Leistungsstaffel*** | **0 / 30 / 50 / 75 / 100 %** across *Pflegegrade* 1 to 5 | **[std]** (12) |
| Alternative *Leistungsstaffel* carried | **10 / 20 / 30 / 40 / 100 %** — the statutory *Pflege-Bahr* minimum grid, the only *Leistungsstaffel* fixed by German statute | [R8] [unverified] |
| Care setting | **Irrelevant to the benefit.** The same annuity is payable at home and in a *Pflegeheim* | **[std]** (1) |
| Payment start | From the beginning of the month in which the *Pflegegrad* takes effect, subject to any *Karenzzeit* | [S4] [unverified] (13) |
| Duration | For as long as an insured *Pflegegrad* holds; for life if it holds for life | [S4] |
| ***Wartezeit*** (from inception) | **None** in the base case. Observed: commonly none on an underwritten tariff, up to **3 years** where present, usually waived where care follows an accident; up to **5 years** on *Pflege-Bahr* | [R8] for the 5 years [unverified]; base **[std]** (14) |
| ***Karenzzeit*** (from onset) | **None** in the base case. Observed: commonly none; **3** or **6** months where present | [unverified]; base **[std]** (14) |
| ***Beitragsbefreiung im Leistungsfall*** | **Full**, from the first month in which any annuity is payable; the premium revives on exit from the paying grades | [S4]; detail **[std]** (11) |
| ***Nachprüfung*** | The insurer may require periodic evidence that the *Pflegegrad* persists. In practice the evidence is the statutory determination itself | [S4] [unverified] (15) |
| ***Herabstufung*** | The annuity falls to the lower step; if the grade falls below the insured threshold the annuity **stops** and the premium revives | [S4] [unverified] |
| ***Höherstufung*** | The annuity rises to the higher step from the effective date of the new *Pflegegrad* | [S4] [unverified] |
| ***Reaktivierung*** | Recovery to the active state ends the annuity and revives the premium | [S4] [unverified] |
| ***Todesfallleistung*** | **None** in the base case. Carried as a switchable *Beitragsrückgewähr* option | [S4]; base **[std]** (16) |
| ***Leistungsdynamik*** in payment | **Off** in the base case. Observed band **1 % to 3 %** a year | [unverified]; base **[std]** (17) |
| ***Beitragsdynamik*** before claim | **Not modelled.** Observed band **3 % to 5 %** a year, with a right to decline that lapses permanently after two or three refusals | [unverified]; scope **[std]** (17) |
| Exclusions | Care caused by war, by the insured's intentional act and, variably, by addiction; and any condition disclosed and excluded at underwriting | [S4] [unverified] |
| Territorial scope | Whether the annuity survives care given outside Germany or the EEA is a real term difference and was not established | [S4] [unverified] |

12. **The *Leistungsstaffel* is the most important parameter in the product and the one the corpus
    can least support** (research gap 6). The observed range, attributed to no carrier, is: grade 1
    **0–10 %**; 2 **10–30 %**; 3 **30–50 %**; 4 **60–75 %**; 5 **100 %**, universally. Two shapes
    recur — the statutory *Pflege-Bahr* 10 / 20 / 30 / 40 / 100 [R8], and a flatter, higher shape
    near 0 / 30 / 50 / 75 / 100, which is what a *Pflegerente* aimed at the residential gap uses
    because grades 3 to 5 are where residential care happens. The composite takes the second, each
    step argued: **grade 1 at 0 %** because grade 1 is not a funding event in the statutory scheme
    either, so insuring it would add incidence-heavy, low-severity claims that dominate the claim
    *count* and not the claim *cost*; **grade 2 at 30 %**, the top of its range, because grade 2 is
    where care at home begins in earnest; **3 at 50 %** and **4 at 75 %**, both mid-range; **5 at
    100 %**, the scaling constant. The schedule is read from a CSV with a `provenance` column.
13. The statutory determination is often backdated to the date of application, so a wording keyed
    to the *effective date* pays earlier than one keyed to the *decision date*. Which a tariff uses
    was not established; the composite keys off the effective date.
14. **The pairing between underwriting and waiting periods is near deterministic**: no underwriting
    implies a long *Wartezeit* (the *Pflege-Bahr* design [R8]); underwriting implies none. Both are
    **zero** in the base run, both are model-point parameters, and both are exercised — a
    *Karenzzeit* on a population with heavily elevated mortality removes disproportionately more
    claims than the same period would on a healthy population.
15. The insurer does not define the insured event — the state does, and re-defines it [R9] — and
    does not assess the claim [R6]. Claims administration is therefore materially cheaper than on a
    *Berufsunfähigkeitsrente* [REG-R29]. The price of that cheapness is **definition risk**: any
    loosening of the *Begutachtungs-Richtlinien* or of § 15 SGB XI raises incidence with no
    contractual change and no re-rating remedy.
16. A *Todesfallleistung* — most often a ***Beitragsrückgewähr*** [S4] [unverified] — converts a
    pure biometric cover into a savings-bearing contract: the reserve needed to fund it is close to
    the accumulated premium itself, it roughly doubles or more the premium for the same annuity
    **[std]** because the death benefit is close to certain to be paid whereas the annuity is not,
    and it very likely brings the contract inside the PRIIPs perimeter [REG-R32]. The base run omits
    it so that the LTC mechanics are what the model demonstrates.
17. **The *Leistungsdynamik* is the economically important dynamic**, for the reason given under the
    *Versorgungslücke*, and its cost is counter-intuitively small: the annuity is paid to a
    population with heavily elevated mortality, so a 2 % escalation on an annuity of about four
    years' expected duration costs of the order of **4 %** of its value, not the 15 % or 20 % it
    would cost on a healthy-life pension. The **Beitragsdynamik** is **not modelled at all**: the
    acceptance rate on each offer is a behavioural assumption this corpus cannot support.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Health evidence | Full ***Gesundheitsprüfung*** on the underwritten product | [S4] [unverified] |
| Question catalogue | Materially **shorter than a *Berufsunfähigkeit* application's**: the risk is driven by conditions that predict dependency in old age — cardiovascular and cerebrovascular disease, diabetes, neurological and psychiatric conditions, early cognitive impairment, musculoskeletal disease — rather than by occupation | [unverified] |
| Occupation | **Not a rating factor.** The sharpest single contrast with *Berufsunfähigkeit* | [unverified] |
| Outcomes | Accept at standard rates; accept with a *Risikozuschlag*; accept with a *Leistungsausschluss* for a named condition; defer; decline | [S4] [unverified] |
| Absolute bar | Existing *Pflegebedürftigkeit* at application | [S4] [unverified] |
| Disclosure duty | *Vorvertragliche Anzeigepflicht* under § 19 VVG; remedies graded by fault and time-barred, generally after five years and ten in cases of intent | [R11]; [REG-R30] [unverified] |
| Effect of selection on the liability | **Essentially irrelevant to the cost of the benefit.** Claims arrive thirty to forty years after underwriting, and the § 19 time bar confines the *Gesundheitsprüfung*'s effect to the first decade | [R11]; **[std]** (18) |
| Sex | Not a rating factor for contracts concluded from 21 December 2012 | [REG-R34] |
| Smoker status | Not established as a rating factor for this product | [unverified] |

18. This is the **opposite** of *Berufsunfähigkeit*, where selection is a first-order pricing
    effect because claims arrive within the working life. Here it matters only to the early-duration
    reserve, so the model ships **no selection factor at all**: stacking an unsourced selection
    curve on an already-`[std]` incidence proxy would compound two unsourced choices.

### Charges

**No charge level of any kind was established for any German *Pflegerenten* tariff** — not one
*Abschlusskostensatz*, not one administration rate, not one *Ratenzahlungszuschlag* and not one
*Effektivkosten* value (research gap 2). No *Produktinformationsblatt* [S5], no
*Verbraucherinformation* [S7] and no *Tarifblatt* [S9] was located. **Every charge in delib is
therefore `[std]`.** Only the statutory *ceiling* is known, and only [unverified].

| Parameter | Representative value | Basis |
|---|---|---|
| ***Abschluss- und Vertriebskosten*** | **25 ‰ of the *Beitragssumme***, charged at inception | **[std]** (19) |
| *Höchstzillmersatz* | **25 ‰ (2,5 %) of the *Beitragssumme***, § 4 DeckRV, cut from 40 ‰ by the LVRG with effect from 1 January 2015; the rate an undertaking uses at conclusion applies for the whole term | [REG-R16] [REG-R20]; [R13] [unverified] |
| *Beitragssumme* for the *Zillmerung* base | Level premium × 12 × (min(premium-end age, **85**) − entry age) | **[std]** (20) |
| ***Verwaltungskosten***, premium-related | **3,0 %** of each premium collected | **[std]** (19) |
| ***Verwaltungskosten***, per policy | **2,00 €** per policy in force per month, at inception prices | **[std]** (19) |
| Claims administration | **1,50 €** per annuity payment | **[std]** (19) |
| Expense inflation | **1,5 %** a year | **[std]** (19) |
| Disclosure obligation | *Abschluss- und Vertriebskosten* and *Verwaltungskosten* must be disclosed in euro amounts in the pre-contractual information package under § 7 VVG and the VVG-InfoV | [R11] [S7]; [REG-R31] |
| Commission | Not disclosed anywhere in the corpus; folded into the acquisition charge | **[std]** (19) |

19. **No observed range exists for any of these.** The levels are round-number placeholders, sized
    so that the acquisition charge on the anchor is of the same order as the first two years'
    premium. Claims administration is set **low**, the one charge with a real argument behind it:
    the trigger is determined by a third party [R6], so the insurer's own claims cost is materially
    smaller than on a *Berufsunfähigkeitsrente* [REG-R29].
20. The *Höchstzillmersatz* is a per-mille of the ***Beitragssumme***, the sum of all premiums
    payable under the contract [REG-R16] — **not** a percentage of the annual premium, and getting
    that base wrong is a listed pitfall. On a lifelong-premium contract the *Beitragssumme* is not
    finite without a convention, so the composite caps the premium term at attained age **85**
    **[std]**, making the anchor's *Beitragssumme* forty years of premium and the 25 ‰ ceiling bind
    visibly rather than notionally.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| ***Rückkaufswert*** | Payable on surrender. The base measure is the ***Deckungskapital*** computed on the premium calculation bases, with acquisition costs spread over at least the first **five** contract years as a **floor on the value**, not a cap on the charge | [R11]; [REG-R28] |
| Shipped surrender basis | A table of guaranteed surrender values expressed as a **fraction of premiums paid to date**, by completed policy year — the form in which a German contract actually states them | **[std]** (21) |
| Practical size | **Near zero for the first several years** and well below premiums paid for a long time, because the *Zillmerung* allowance is large and the early risk premium is small | **[std]** (21) |
| ***Stornoabzug*** | **0 %** in the base run. Admissible only if agreed, appropriate and **quantified in the contract**, with a deduction for unamortised acquisition costs expressly ineffective and the burden of proof on the insurer | [REG-R28]; level **[std]** (22) |
| ***Beitragsfreistellung*** | The policyholder may at any time demand conversion to a paid-up *Pflegerente* at a reduced *vereinbarte Rente*, computed from the same § 169 value the surrender path uses | [R11]; [REG-R28]; scope **[std]** (23) |
| The open statutory question | Whether a **pure-risk** *Pflegerente* — no death benefit, no survival benefit — falls inside the § 169 exception that denies a *Risikolebensversicherung* its surrender value **was not established** | [R11]; research gap 9 |
| Lapse | Voluntary surrender terminates the contract against payment of the *Rückkaufswert* less any *Stornoabzug* | [REG-R28] |
| Non-payment path | German lapse is a **three-way decrement** — surrender, *Beitragsfreistellung*, and premium-default conversion under § 38 VVG, the last two keeping the policy in force with a reduced benefit and a continuing expense loading | [REG-R28] [REG-R30]; scope **[std]** (23) |
| *Widerruf* | 30 days on a life contract, under § 152 VVG | [REG-R23] [unverified] |
| Expiry | **None.** The contract runs for life; there is no maturity and no survival benefit | [S4] |

21. **No *Rückkaufswert* table for any German *Pflegerenten* tariff was established.** The
    composite ships guaranteed values as **data** rather than computing a reserve, for two reasons.
    It is what a German contract does: § 165 VVG requires the paid-up benefit to be **stated in the
    contract for each insurance year** [REG-R28], so a table by policy year is the contractual
    object. And computing a reserve would break the library's rule that its models publish gross
    undiscounted cash flows. The shipped shape encodes two cited facts — the 25 ‰ *Zillmerung*
    allowance [REG-R16], which puts the value at zero for the first two years, and the § 169 Abs. 3
    five-year spread **floor** [REG-R28], which makes it positive from year three. Levels beyond
    that shape are **[std]**.
22. The German life-market *Stornoabzug* range runs from nil to about **5 %** of the
    *Deckungskapital* [unverified]; **none was established for this product**. § 169 Abs. 5 admits a
    deduction only if agreed, quantified and appropriate, so a non-zero default would assert a
    contractual quantification this corpus cannot supply. The base run is **0 %**; one model point
    switches it on at 5 %.
23. **The model implements the surrender path only.** *Beitragsfreistellung* and the § 38
    premium-default conversion both keep the policy in force at a reduced *vereinbarte Rente*,
    anchored to the same § 169 value [REG-R28], and carrying them needs a paid-up ledger with its
    own benefit, expense loading and decrements, for which the corpus supplies no take-up split. The
    model treats every voluntary exit as a surrender and records the bias: the omitted paths would
    move policies into a reduced-benefit ledger that still pays claims, so **the model understates
    late-duration claims and overstates surrender outgo**, by an amount the corpus cannot size.

---

## Contractual mechanics

### The benefit trigger — the statutory *Pflegegrad*

The operative rule: **the annuity is payable when, and for as long as, the insured holds a
*Pflegegrad* at or above the lowest grade the *Leistungsstaffel* pays on**, that grade being the
one determined under §§ 14, 15 SGB XI by the *Medizinischer Dienst* for the statutorily insured
or by MEDICPROOF for the privately insured [R2] [R6]. Wordings provide a fallback assessment by a
physician the insurer appoints where the insured is covered by neither [S4] [unverified].

§ 14 defines *Pflegebedürftigkeit* as a health-related impairment of *Selbstständigkeit* or of
abilities, requiring help from others and expected to last **at least six months**
[R2] [unverified]. § 15 converts the assessment into a *Pflegegrad*: six *Module* are scored,
weighted and summed to *gewichtete Punkte* on a 0-to-100 scale — *Mobilität* 10 %, cognitive and
behavioural functioning sharing 15 % with the **higher** entering, *Selbstversorgung* **40 %**,
management of illness- and therapy-related demands 20 %, daily life and social contact 15 % —
with thresholds at 12,5 / 27 / 47,5 / 70 / 90 points for grades 1 to 5 [R2] [unverified].
*Selbstversorgung* alone carries 40 % of the weight, and a reader coming from a US or UK product
will recognise an ADL trigger inside the scoring; the two should not be equated, because the
instrument reaches grade 2 on moderate impairments no two-ADL-failure trigger would catch and
scores dementia with no physical impairment at all. Three consequences reach the model: the
insurer **does not define the insured event** and so carries definition risk no wording can
hedge; the insurer **does not assess the claim**, which makes claims administration cheap and
disputes rare compared with *Berufsunfähigkeit*; and a *Pflegegrad* is a **step function of a
continuous state, re-assessed episodically** [R6] — which is exactly a discrete-state,
discrete-time Markov chain, and is why the model's state space is the natural representation
rather than an approximation.

**The 2017 break is the largest basis risk in the product.** PSG II replaced the three
*Pflegestufen* with the five *Pflegegrade* and the time-based assessment with the NBA from
1 January 2017 [R9] [unverified], deliberately **widening** the definition; recognised
*Pflegebedürftige* rose sharply afterwards, and every time series has a structural break there.
The market's standard basis, **DAV 2008 P**, was built on the *Pflegestufen* [R15] [unverified],
and the BGH has **refused to map the two scales** [REG-R36] [REG-R51]. If the courts will not map
the grades, a modeller may not silently do so either — which is why delib's transition rates are
an explicitly labelled `[std]` proxy shaped on *Pflegegrad* prevalence and are **not** a proxy
for DAV 2008 P.

### The *Leistungsstaffel*

The operative rule: **the contract fixes one number, the *vereinbarte Pflegerente* — the monthly
annuity at the top *Pflegegrad* — and a schedule of percentages of it by grade.** Everything else
in the benefit design is a modifier on that schedule.

What the schedule does to the liability is not obvious from its headline. Time spent at each
grade is very unequal: a person entering at grade 2 and deteriorating spends most of the spell at
grades 2 and 3 and only the final months at grade 5 [unverified], so **the time-weighted average
benefit percentage over a spell is far below 100 %** — about 52 % on the profile the research
file works through. Two tariffs with the same 100 % top step and different middle steps differ in
expected cost by more than the headline suggests. Comparing tariffs on the *vereinbarte Rente*
alone is therefore misleading, and so is any model that applies an average benefit percentage to
an average survival curve. The middle steps carry the cost because the stock distribution is
weighted to the lower grades — about 9 / 44 / 27 / 14 / 6 % across grades 1 to 5 [R18]
[unverified].

### *Wartezeit* and *Karenzzeit*

The two are different devices and are routinely confused in consumer material. A ***Wartezeit***
runs from **inception of the contract**: care beginning inside it is not covered at all, or is
covered only where it follows an accident. A ***Karenzzeit*** runs from **the onset of
*Pflegebedürftigkeit***: the claim is admitted but the annuity does not start until the deferred
period has run, and some wordings then pay retroactively to onset and some do not
[S4] [unverified].

Why the underwritten product usually has neither: the *Gesundheitsprüfung* does the screening a
*Wartezeit* does in the subsidised product. *Pflege-Bahr*, which by statute has no
*Gesundheitsprüfung*, is allowed a *Wartezeit* of up to **five years** for exactly that reason
[R8] [unverified]. The mechanic that matters for the model: **a
deferred period on a population with elevated mortality removes disproportionately more claims
than the same period would on a healthy population**, because a material share of new claimants
die inside it — selection *at onset*, not at underwriting.

### *Beitragsbefreiung im Leistungsfall*

The operative rule: **premiums are waived while the annuity is payable**, and the obligation
revives if the annuity stops. This is standard in the German market for *Pflegerenten* and is
contractual, not discretionary [S4].

**The waiver is not a cosmetic term.** On a contract issued at 45 and claiming at 82 it removes
the remaining premium stream for the whole paying period — of the order of four years of premium,
the same order as one year of benefit at the modelled levels. Its cost sits inside the level
premium and is one reason a *Pflegerente* is dearer than a *Pflegetagegeld* of nominally equal
benefit. The interlock with the *Leistungsstaffel* is the subtle part and the model has to get it
right: waiver runs from the first *Pflegegrad* at which an annuity is payable, so on the
0 / 30 / 50 / 75 / 100 grid a life at *Pflegegrad* 1 **is in care, receives nothing, and still
pays the premium**, while on the *Pflege-Bahr* grid, which pays 10 % at grade 1, the same life is
waived. Two tariffs differing only in whether they insure grade 1 differ in their premium
*income* as well as their benefit outgo, in opposite directions.

### *Nachprüfung*, *Herabstufung* and *Reaktivierung*

The operative rule: **the paying state has three exits, not one.** A life receiving the annuity
may die; may be downgraded to a lower insured grade, at which the annuity falls to that step; or
may be downgraded below the insured threshold or recover to the active state, at which the
annuity stops and the premium revives [S4] [unverified]. **Only death is absorbing.**

This is the most important structural fact for an implementation. A model that treats "in claim"
as one state exited only by death **overstates** the liability; a model that treats every
downgrade as a termination **understates** it. The model therefore carries the *Pflegegrad*
explicitly as a state variable and moves lives between grades in both directions. Some tariffs
guarantee that an annuity once granted will not be reduced; **whether such a guarantee is common
was not established** (research gap 17). With it the paying state is exited only by death and the
state space collapses. The composite models the **unguaranteed** form, the more general one; a
user holding a wording with the guarantee obtains it by setting the recovery and downgrade rates
to zero. The *Nachprüfung* itself is a documentation exercise rather than the adversarial
re-assessment that characterises *Berufsunfähigkeit*, because the evidence is the statutory
determination [R6] [S4] [unverified].

### The level guaranteed *Beitrag*

The operative rule: **the *Beitrag* is level and is guaranteed for the life of the contract**,
subject only to § 163 VVG [R11] [REG-R27]. This is the product's defining commercial property and
the whole of its price premium over a *Pflegetagegeld*.

Three things follow. The insurer carries the **basis risk** on a fifty-year view of a table built
on a superseded assessment regime, and § 163 is a narrow escape: it needs a non-temporary,
unforeseeable change in a calculation basis, an appropriate and necessary new premium and a
trustee's confirmation, and it is **excluded** to the extent the original calculation was
insufficient and a diligent actuary should have recognised it [REG-R27]. The premium must be
**prudently calculated and permanently sufficient** under § 138 VAG [REG-R8], and the prudence
requirement bites hardest on the *Pflegewahrscheinlichkeiten*, the least stable of the biometric
bases. And German biometric products are conventionally quoted as a *Bruttobeitrag* with a lower
*Zahlbeitrag* below it, the gap being a discretionary surplus rebate withdrawable **without
invoking § 163 at all** [REG-R27] [REG-R53] — so a level *Zahlbeitrag* is not the same promise as
a level *Bruttobeitrag*. **Whether the *Pflegerente* market quotes the pair as the
*Berufsunfähigkeit* market does was not established** (research gap 18); the composite models the
*Bruttobeitrag* and no rebate.

### The *Deckungskapital* as an ageing reserve

The contract is calculated ***nach Art der Lebensversicherung***, so the reserve is a
***Deckungsrückstellung*** under § 341f HGB and the DeckRV [R12] [R13] [REG-R14] [REG-R54] —
**not** an *Alterungsrückstellung*, which is the private-health-insurance object of § 146 VAG.
The precise words are worth using: *the* Deckungskapital *of a* Pflegerente *is an ageing reserve
in economic function and a* Deckungsrückstellung *in law and in the accounts*.

The annual probability of entering care is negligible before 60, small to 75 and rises steeply
thereafter; the level premium is far above the risk premium for three or four decades and far
below it afterwards, and the difference accumulates. Issued at 45, the *Deckungskapital* rises
for roughly thirty-five years, peaks in the early eighties where the incidence curve crosses the
level premium, then runs off — later-peaking and smaller relative to premiums paid than an
endowment's, and very much larger than a *Risikolebensversicherung*'s. *Zillmerung* applies up to
the *Höchstzillmersatz* of 25 ‰ of the *Beitragssumme* [REG-R16], producing a negative reserve in
the earliest years and a correspondingly poor early-duration surrender value. Two consequences
reach the model. **Interest sensitivity is the highest in delib**, because benefits fall on
average some thirty-five years after issue. And **lapse is profitable early and expensive late**:
a lapse at 70 removes a policyholder who paid for twenty-five years and never reached the risk
period, so lapse feeds the premium through the equivalence principle in a real tariff — while the
composite's pricing basis is deliberately **lapse-free**, both because that is German first-order
practice and because the house style forbids a pricing quantity that depends on a behavioural
assumption that depends on the path that depends on the premium.

### *Rückkaufswert*, *Beitragsfreistellung* and the *Stornoabzug*

§ 169 VVG entitles the policyholder to a surrender value computed as the *Deckungskapital* on the
premium calculation bases, with a floor equal to the value that results from spreading
acquisition and distribution costs evenly over the **first five contract years** — a floor on the
value, not a cap on the charge — and a *Stornoabzug* admissible **only if agreed, quantified and
appropriate**, with a deduction for unamortised acquisition costs expressly ineffective and the
burden of proof on the insurer [REG-R28]. § 165 gives an independent right to
*Beitragsfreistellung* at any premium due date, the reduced benefit computed on the same § 169
value and **stated in the contract for each insurance year** [REG-R28].

**The open question**, and it is genuinely open: whether a **pure-risk** *Pflegerente* falls
inside the § 169 exception for covers paying only on death within a defined period. The
exception's plain target is *Risikolebensversicherung*; a *Pflegerente* pays on an uncertain
event that is not death and **does** build a substantial reserve, which argues for full § 169
treatment. **This was not established** (research gap 9). The composite models a *Rückkaufswert*,
floors it at zero, exposes the *Stornoabzug* as a parameter, and says plainly that the statutory
question is open and that a carrier's own wording settles it for that carrier.

### *Überschussbeteiligung*

The contract participates in surplus under § 153 VVG and § 139 VAG like any other German life
contract, unless participation is excluded by agreement [R11] [R12] [REG-R24] [REG-R9]. **The
composition is different from an endowment's.** On a *Kapitallebensversicherung* the surplus is
dominated by the *Zinsergebnis*; here the reserve is smaller relative to the risk and the
biometric basis is the prudent one, so the ***Risikoergebnis*** is the dominant component, the
*Zinsergebnis* second and the *Kostenergebnis* third. That is the *Sicherheitszuschlag* between
the first- and second-order bases being released as experience emerges [REG-R47], distributed
through the *Rückstellung für Beitragsrückerstattung* under the MindZV and the RfBV [REG-R10]
[REG-R18] [REG-R19]. Application forms [unverified]: *Beitragsverrechnung*, where the declared
surplus reduces the premium called — dominant on biometric-risk products; *verzinsliche
Ansammlung*; and a *Bonus* form raising the *vereinbarte Rente*. **The base run carries no
*Überschussbeteiligung* at all**, deliberately: delib publishes gross undiscounted cash flows,
the surplus chassis is demonstrated in full by `products/kapitallebensversicherung/`, and a
discretionary *Beitragsverrechnung* would need a declared-rate assumption for which this corpus
supplies nothing.

## Riders and options

**In scope, modelled or parameterized.** ***Leistungsdynamik im Leistungsbezug*** — escalation
of the annuity in payment at an agreed 1 % to 3 % a year [unverified], off in the base run,
implemented as an escalation ledger running from the first month the annuity is payable; it is
the economically important dynamic on this product. ***Beitragsrückgewähr*** — a
*Todesfallleistung* returning the premiums paid, off in the base run, implemented in its
**gross** form, without an annuity offset, for the reason the technical notes give.
***Abgekürzte Beitragszahlungsdauer*** — premiums to a fixed attained age, typically 65 or 85
[unverified]. ***Einmalbeitrag*** — the single-premium form, explicitly **not** the base model
but carried so the chassis can price it. ***Wartezeit*** and ***Karenzzeit***, both zero in the
base run. ***Risikozuschlag***, a multiplier on the gross premium, 1.00 at standard rates.
***Stornoabzug***, 0 % in the base run. And an alternative ***Leistungsstaffel***, the statutory
*Pflege-Bahr* grid [R8], shipped beside the composite's own so that the effect of the middle
steps is demonstrable rather than asserted.

**Out of scope, and why.** ***Beitragsdynamik*** — indexation of premium and cover before claim
at 3 % to 5 % a year, with a right to decline that lapses permanently after two or three refusals
[unverified] — is not modelled at all: the acceptance rate on each offer is a behavioural
assumption for which this corpus supplies no evidence, and a declined-out contract is an
absorbing state needing its own ledger. ***Überschussbeteiligung*** is recorded above and
deliberately omitted. ***Beitragsfreistellung*** and the § 38 VVG premium-default conversion keep
the contract in force with a reduced benefit; the composite treats every voluntary exit as a
surrender and records the direction of the bias. A ***Pflegetagegeld*** or ***Pflegekosten***
rider on the same life is a different legal branch under a different supervisory regime
[S2] [R14]; ***Pflege-Bahr*** is statutorily unavailable [R8]; bundled assistance packages carry
no material cash flow; and no joint-life or couple *Pflegerente* is recorded in the corpus.

---

## Variations across insurers

**No carrier's *Pflegerenten* document was located, so this section names no carrier against
any figure** (research gap 14). That is the largest single difference between this
specification and its frlib counterpart, where eight carriers' contracts were read and the
variation table has eight columns. Naming a carrier against a parameter value no source
supplied would be exactly the fabrication house rule 3 forbids, and it is not done here. What
follows instead is the **parameter range the German market is understood to write**, with an
explicit attribution column that says, honestly, that nothing is attributed.

| Parameter | Observed / argued range | Attribution | Basis |
|---|---|---|---|
| *Leistungsstaffel*, *Pflegegrad* 1 | 0 % to 10 % | none established | [unverified] |
| *Leistungsstaffel*, *Pflegegrad* 2 | 10 % to 30 % | none established; 20 % is the *Pflege-Bahr* statutory step | [unverified]; [R8] for the 20 % |
| *Leistungsstaffel*, *Pflegegrad* 3 | 30 % to 50 % | none established; 30 % statutory in *Pflege-Bahr* | [unverified]; [R8] |
| *Leistungsstaffel*, *Pflegegrad* 4 | 60 % to 75 % | none established; 40 % statutory in *Pflege-Bahr* | [unverified]; [R8] |
| *Leistungsstaffel*, *Pflegegrad* 5 | 100 % | universal | [unverified] |
| *Wartezeit*, underwritten tariff | 0 to 3 years, usually waived for accident | none established | [unverified] |
| *Wartezeit*, *Pflege-Bahr* | up to 5 years | statutory | [R8] [unverified] |
| *Karenzzeit* | 0, 3 or 6 months | none established | [unverified] |
| Entry age | 18 to 65, some to 70 | none established | [unverified] |
| Purchase cluster | 45 to 60 | none established | [unverified] |
| *Vereinbarte Rente* as sold | 1 000 € to 1 500 € per month | none established | [unverified] |
| *Beitragsdynamik* | 3 % to 5 % a year | none established | [unverified] |
| *Leistungsdynamik* in payment | 1 % to 3 % a year | none established | [unverified] |
| *Todesfallleistung* | none / *Beitragsrückgewähr* / fixed sum / *Deckungskapital* | none established | [unverified] |
| *Beitragszahlungsdauer* | lifelong / to 65 / to 85 / *Einmalbeitrag* | none established | [unverified] |
| *Stornoabzug* | 0 % to about 5 % of the *Deckungskapital* | none established | [unverified] |
| Benefit by care setting | setting-independent (modern) / reduced at home (older wordings) | none established | [unverified] |
| *Herabstufung* guarantee | present in some wordings, absent in others | none established | [unverified]; research gap 17 |

**What can be said about carriers without a source.** The delib brief names twenty-six German
undertakings. **This corpus establishes nothing about any of them** — not one wording, rate
card, product name or parameter. The one structural statement that follows without a source,
because it follows from the branch table above, is that ***Pflegetagegeld* is written by the
*Krankenversicherer* in that list and *Pflegerente* by the *Lebensversicherer***; which
undertakings currently write a *Pflegerente* was not established.

**Where the ranges would have come from.** Franke und Bornberg and Morgen & Morgen rate
*Pflegezusatzversicherung* wordings clause by clause [S14] [REG-R53]; Stiftung Warentest and
Finanztip publish comparative tests, both concentrating on *Pflegetagegeld* [S10] [S12]; Verivox
and Check24 quote on demand, though whether either quotes *Pflegerente* at all was not
established [S13]. **None was retrieved or searched.**

**What does not vary.** Three rows above are legal facts rather than commercial ones and can be
stated without attribution: *Pflegegrad* 5 pays 100 %, which is the definition of the *vereinbarte
Rente* rather than a term; the premium cannot be re-rated outside § 163 VVG, because that is what
writing the cover as *Lebensversicherung* means [R11] [REG-R27]; and a *Pflegerente* cannot be a
*geförderter Tarif* under § 127 SGB XI, whatever its terms [R8].

---

## Regulatory context

**Social law — the trigger and the first layer.** SGB XI creates the *soziale
Pflegeversicherung* [R1]; the contribution rate is **3,6 %** of assessable earnings from
1 January 2025, and whether it changed again from 1 January 2026 was not established (research
gap 8) [R1] [unverified]. §§ 14 and 15 define *Pflegebedürftigkeit* and the five *Pflegegrade*
[R2]; §§ 36–38 the home-care benefits [R3]; §§ 43 and 43c residential care and the
*Leistungszuschläge* [R4]; §§ 39, 42 and 45b the secondary heads [R5]; § 18 and the
*Begutachtungs-Richtlinien* the assessment [R6]; § 23 the compulsory private equivalent [R7];
§ 127 the *Pflege-Bahr* subsidy [R8]. The reform acts that matter are **PSG II**, which
introduced the five grades and the *einrichtungseinheitlicher Eigenanteil* from 1 January 2017
[R9], and the **PUEG** of 2023 [R10] [unverified]. §§ 61–66 SGB XII provide the means-tested
backstop [R24].

**Contract law — the VVG.** § 7 and the VVG-InfoV impose the pre-contractual information duties,
including the euro disclosure of acquisition and administration costs [R11] [REG-R31]. § 19
governs the *vorvertragliche Anzeigepflicht*, with remedies graded by fault and generally
time-barred after five years, ten in cases of intent [REG-R30] [unverified] — on a product whose
claims arrive forty years after underwriting, the time bar is what confines the
*Gesundheitsprüfung*'s effect on incidence to the first decade. § 152 gives a 30-day *Widerruf*
[REG-R23]; § 153 the *Überschussbeteiligung* [REG-R24]; § 155 the annual *Standmitteilung*
[REG-R25] [S8], which here reports the guaranteed *vereinbarte Pflegerente* rather than a sum
insured; § 163 the whole of a life insurer's re-rating power [REG-R27]; and §§ 165–170 the
paid-up conversion, the surrender value, the five-year floor and the *Stornoabzug* [REG-R28].
And § 203, the *Beitragsanpassung* provision that dominates the *Pflegetagegeld* comparison,
**applies to health insurance and not to life insurance** [R11] [R14] — which is the point of the
entire comparison in this document.

**Whether Kapitel 6 VVG reaches this product was not established.** §§ 172–177 are the
*Berufsunfähigkeitsversicherung* chapter, and § 177 Abs. 1 extends §§ 173–176 to contracts
promising a benefit for a lasting impairment of **working capacity** [REG-R29]. A *Pflegerente*
promises a benefit for dependency, not for impairment of working capacity, so on the face of it
the extension does not reach it — but the point was not established and is [unverified]. It
matters: § 174's rule that a cessation of liability takes effect only after prior notice in
*Textform* and only from the end of the **third month** following that notice would, if it
applied, put a three-month tail on every *Herabstufung* and every *Reaktivierung*. **The model
does not implement such a tail**, and this is the reason.

**Supervisory law.** § 138 VAG requires premiums to be prudently calculated and permanently
sufficient [REG-R8]; § 139 governs the *Überschussbeteiligung* and the *Sicherungsbedarf* test
[REG-R9]; §§ 140 and 145 the *Rückstellung für Beitragsrückerstattung* [REG-R10], with the MindZV
[REG-R18] and the RfBV [REG-R19] below them; §§ 141–143 create the *Verantwortlicher Aktuar* and
the *Treuhänder* whose confirmation § 163 VVG requires [REG-R11]; § 146 defines the *substitutive
Krankenversicherung* regime and is cited only to locate the boundary this product sits on the
other side of [R14]. Above it sits Solvency II, reaching German life business **through** the VAG
[REG-R1] [REG-R2] [REG-R5] [REG-R6], with Directive (EU) 2025/2 effective 30 January 2027
[REG-R3]; nothing here implements a 2027 basis.

**Reserving and the technical rate.** § 341f HGB requires the *Deckungsrückstellung* to be
computed prospectively on the tariff bases [R12] [REG-R54]. § 2 DeckRV fixes the
*Höchstrechnungszins*, raised to **1,00 % with effect from 1 January 2025** by the Sechste
Verordnung of 19 July 2024 — the first increase in about thirty years — after 0,25 % for 2022–2024
and 0,90 % for 2017–2021 [REG-R14] [REG-R15]. The rate applies **at contract conclusion and then
stays with the contract for its whole term**, which is why the German in-force book is a stack of
cohorts and why an in-force model point carries its own cohort's rate rather than today's. § 4
DeckRV caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme*, cut from 40 ‰ from 1 January 2015 by
the LVRG [REG-R16] [REG-R20], and interacts with the independent § 169 VVG five-year floor: the
DeckRV governs what the insurer may **reserve**, § 169 what it must **pay**, and both apply
separately, the tighter binding [REG-R28]. § 5 Abs. 3 DeckRV builds the *Referenzzins* behind the
*Zinszusatzreserve* [REG-R17], an HGB reserve with no counterpart elsewhere in this repository
and which this model does not compute.

**Biometric bases.** **DAV 2008 P** is the market-standard first-order basis for German LTC
business on the life chassis [R15] [REG-R51]. It is a **multi-state** table: it supplies
*Pflegewahrscheinlichkeiten* by sex, attained age and grade of entry; transitions between grades;
*Reaktivierungswahrscheinlichkeiten*; and, decisively, **separate mortality for active lives and
for lives in care, by grade**. **It is the property of the Deutsche Aktuarvereinigung, is not
public, and is not redistributed by this library.** No value from it appears anywhere in delib
and none may. It was built on the pre-2017 *Pflegestufen* and the BGH has refused to map the two
scales [REG-R36] [REG-R51], so applying it to *Pflegegrade* is the insurer's own work — **the
largest single basis risk in the product** (research gap 10). Two neighbouring tables enter
narrowly: **DAV 2008 T** for a death benefit written into the contract [R16] [REG-R48]; and **DAV
2004 R** as a **contrast** — an annuity table is built to be prudent about people living
*longer*, whereas the annuity here is paid to a heavily impaired population whose mortality is a
multiple of the general population's, so using an annuity table **would be prudent in exactly the
wrong direction and would materially overprice the benefit** [R16] [REG-R49]. The German
two-basis structure — *Rechnungsgrundlagen erster Ordnung* for pricing and reserving, *zweiter
Ordnung* for best estimate, the *Sicherheitszuschlag* the wedge between them — is at [REG-R47],
and for **care** the direction of prudence is higher incidence, longer duration in care and
**lower** mortality of care recipients. An insurer may use its own table; the DAV table is a
market default, not a legal mandate [REG-R47].

**Unisex.** Direct or indirect sex-based differences in premiums and benefits are prohibited for
contracts concluded from 21 December 2012, following *Test-Achats* and §§ 19, 20 and 33 AGG
[REG-R34]. The tension is sharper here than anywhere else in delib, because the underlying bases
are sex-specific and the sex differential in LTC incidence and duration is large. The composite
prices on a stated 50 / 50 blend, projects on the model point's own sex, and lists "pricing
unisex on a 50 / 50 mix while writing 60 / 40" as a model risk.

**Taxation.** Premiums are *sonstige Vorsorgeaufwendungen* under § 10 Abs. 1 Nr. 3a EStG,
deductible only within an annual ceiling of the order of 1 900 € for employees and pensioners
and 2 800 € for the self-employed [R23] [unverified] — a ceiling the compulsory health and LTC
contributions of Nr. 3 normally exhaust on their own, so **in practice, for most buyers, the
premium is not deductible at all**. That is the honest statement, and it is why the
*Pflege-Bahr* *Zulage* was designed as a direct subsidy rather than as a further deduction [R8].
**The taxation of the benefit is unresolved** (research gap 13): either exemption under § 3
Nr. 1a EStG as a benefit from a *Pflegeversicherung*, the analysis universally applied to
*Pflegetagegeld*, or *Ertragsanteil* taxation under § 22 Nr. 1 EStG as a *Leibrente*, the
analysis applied to a *Berufsunfähigkeitsrente* and the one this product's life-assurance form
argues for [R23] [REG-R41] [unverified]. The distinction is worth several per cent of the
product's after-tax value. **delib does not model taxation of the benefit** and states the open
question instead. A *Todesfallleistung* follows the ordinary life-assurance treatment — outside
income tax as a death benefit, with *Erbschaftsteuer* possible depending on the beneficiary
designation [R23] [REG-R45] [REG-R46] [unverified].

**Disclosure.** Whether a *Pflegerentenversicherung* is a **PRIIP** requiring a
*Basisinformationsblatt* depends on its own design and **was not established** (research gap 16).
The PRIIPs Regulation excludes life-insurance contracts whose benefits are payable only on death
or in respect of incapacity due to injury, sickness or infirmity [REG-R32] [unverified as to the
article]. A **pure-risk *Pflegerente* with no surrender value and no death benefit falls squarely
inside that exclusion**; one with a *Beitragsrückgewähr*, or a material *Rückkaufswert*, pays on
other events and is much more likely to need one. The presence or absence of a
*Basisinformationsblatt* in a carrier's document library is therefore **evidence about the
tariff's design**. The IDD conduct layer applies in any event [REG-R33], as does BaFin's
*Wohlverhaltensaufsicht* strand [REG-R35] — though **no BaFin material specific to LTC was
located** and no supervisory statement about *Pflegetafel* prudence or about the *Nachprüfung* is
cited anywhere in this product's documents (research gap 11). The DAV's *Fachgrundsätze* bind its
members and the DAV makes the annual *Höchstrechnungszins* recommendation [REG-R56]; IFRS 17
applies to IFRS reporters with no German carve-out [REG-R55]; the statutory accounts run on HGB
§§ 341–341o, the RechVersV and the BerVersV [REG-R54].
