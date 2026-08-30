# Product Specification

**Status:** Draft, 2026-08-29 (all sources accessed 2026-08-29).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a German **fondsgebundene Rentenversicherung** (FRV) — the
unit-linked deferred private annuity in which the accumulating capital is a holding of
*Anteileinheiten* (units) in *Investmentfonds* chosen by the policyholder, so that the insurer
guarantees the **number** of units and not their value, and whose single hard financial guarantee
is the *Rentenfaktor* applied at *Rentenbeginn* to whatever the fund is then worth. **It does not
describe any single insurer's product.** [S#] tags are primary product documents (*Allgemeine
Versicherungsbedingungen*, *Produktinformationsblatt*, *Basisinformationsblatt*,
*Verbraucherinformation*) and [R#] product-specific regulatory and actuarial references, both
numbered per `_research/fondsgebundene_rentenversicherung.md` and resolved in `sources.md` (same
directory; numbering frozen, never renumbered); [REG-R#] tags the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose R-numbering is distinct. **[std]**
marks a standardization introduced for the reference implementation, each with a rationale and,
where the research recorded one, the argued range across the German market; [unverified] marks a
claim no retrieved document or search result confirmed.

**Read this before anything else.** Two limits applied at full strength to this product. Direct
HTTP egress was blocked by an organisation network policy, so **no document cited anywhere in
this specification was retrieved** — not one *Bedingungswerk*, not one *Basisinformationsblatt*,
not one *Produktinformationsblatt*. And the session's `WebSearch` budget was exhausted before
this product's research began, so **no search was run for it either**; the few facts corroborated
at one remove come from searches run for sibling delib products and are attributed to them. A
delib citation is therefore **a pointer, not a certificate**. The **mechanics** below are common
ground in German practice and are written without hedging; the **levels** are almost entirely
**[std]**, because not one *Abschlusskostenquote*, not one *Verwaltungskostensatz*, not one
*Stückkosten* amount, not one *Effektivkostenquote* and not one *Rentenfaktor* was established at
any carrier.

Out of scope: **hybrid and guarantee designs** (*statische* and *dynamische Hybride*, *Zwei-* und
*Drei-Topf-Hybride*, i-CPPI, *Wertsicherungsfonds*), discussed but deliberately not specified
(see *Riders and options*); **indexgebundene Rentenversicherung** (delib `indexpolice`); the
**fondsgebundene Basisrente** and **Riester-Rente** (delib `basisrente`, `riester_rente`); the
**payout phase** (delib `sofortrente`); and **bAV** in all its forms.

---

## Product overview and market role

A *fondsgebundene Rentenversicherung* is a **deferred private annuity whose accumulating value is
a holding of units in investment funds chosen by the policyholder**. The insurer administers the
contract, bears the biometric risk and gives one financial guarantee — the *Rentenfaktor* — but
does not guarantee the value of the fund holding at any point before *Rentenbeginn* [S1]. The
defining sentence, which every German wording expresses in some form, is that **the insurer
guarantees the number of *Anteileinheiten*, not their value**, and everything else follows from
it: no *Rechnungszins* in the accumulation phase, no *Deckungskapital* in the general-account
sense, no *Zinsüberschuss*, no *Bewertungsreserven* worth speaking of, and no investment mismatch
between the insurer's assets and its unit liability, because the VAG requires a separate
*Anlagestock* — a ring-fenced section of the *Sicherungsvermögen* — for each *Anlageart* backing
unit-linked benefits [R15] [REG-R7].

Four consequences distinguish the German chassis from its French, British and American siblings,
and each changes the shape of the projected cash flows:

1. **The charge stack is the product.** A contract with no *Rechnungszins* has nowhere to hide its
   charges, and PRIIPs and the *VVG-Informationspflichtenverordnung* force them onto one page: the
   *Abschluss- und Vertriebskosten* must be disclosed **in euro**, the ongoing costs separately,
   and the ***Effektivkostenquote*** — all costs as the annual percentage by which they reduce the
   contract's return — has been required in quotations since 1 January 2015 `[unverified]` [R7]
   [REG-R31]. The first-order economics are *fund return minus charges*.
2. **The acquisition charge has a statutory cap and a statutory shape.** The *Höchstzillmersatz* of
   § 4 DeckRV caps the acquisition cost financed against future premiums at **25 ‰ (2,5 %) of the
   *Beitragssumme***, cut from 40 ‰ by the LVRG 2014 [R12] [R13] [REG-R16] [REG-R20], and § 169
   VVG requires it to be spread **evenly over the first five contract years** [R1] [REG-R28]. The
   two combine into one visible mechanic: a large early deduction from each premium that stops
   abruptly at month 60.
3. **The surrender value is the fund, and nothing else.** § 169 VVG sends *fondsgebundene
   Versicherungen* to a ***Zeitwert*** rather than a *Deckungskapital* [R1] [REG-R28], and for a
   pure unit-linked contract the *Zeitwert* is the *Fondsguthaben*: no discounting, no mortality
   basis, no *Rechnungszins*, no *Zillmerung* residue, no second-basis *Mindestrückkaufswert*.
4. **The only guarantee is about the conversion terms, not about the pension.** On a classic
   contract both the capital and the annuity factor are guaranteed, so the annuity is guaranteed.
   Here **only the factor is** — the capital it multiplies is the market's. Any product document
   implying otherwise is wrong, and this is the sentence a specification has to carry [R22].

**Market role, and what can and cannot be said about it.** This is understood to be the dominant
German new-business savings form, and the *Höchstrechnungszins* is the reason: a statutory maximum
technical rate of **0,25 %** through the low-interest decade, raised to **1,00 % from 1 January
2025** `[unverified]` [R12] [REG-R14] [REG-R15], caps what a classic tariff may promise but **has
no purchase at all on the accumulation phase of a pure fondsgebundene contract**, there being no
guaranteed accumulation rate to cap. It reaches this product only through the *Rentenfaktor* and
through hybrid designs whose guaranteed pot sits in the general account — the asymmetry that let
unit-linked new business grow while classic new business collapsed. **No GDV new-business split by
*Versicherungsart* was established, so no market-share figure appears anywhere in this document**
[R25] [REG-R53]; the claim of dominance is `[unverified]`. What *is* corroborated, at one remove,
is the market-structure fact behind it: **Debeka, Germany's largest life mutual by policy count,
discontinued its classic annuity tariff** [S14]. When the classic tariff closes, the new-business
flow goes to the fondsgebundene and hybrid forms.

**The supervisor is watching the charge level.** BaFin's *Merkblatt 01/2023 (VA)* requires
*kapitalbildende Lebensversicherungsprodukte* to offer an ***angemessener Kundennutzen***, states
that *Effektivkosten* between providers and products **differ considerably**, and says BaFin will
closely examine undertakings whose *Effektivkosten* are very high in a sector comparison and whose
*Aufwendungen für Versicherungsvermittler* are notably high; a retirement product must be likely
to achieve a **real** investment success — a return after costs above a justified inflation
expectation [R10] [REG-R35]. Three years later "Kosten von kapitalbildenden
Lebensversicherungen" is still a named focus risk in BaFin's 2026 agenda [R11]. **No numerical
threshold, band, median or sector benchmark appears in any of that material**, and none is quoted
here. The charge stack below is therefore treated as a **supervised** rather than a free parameter
and is presented as a design decision with an argued derivation, not as an observation.

---

## Representative specification

The representative design is a **pure fondsgebundene Rentenversicherung with no
*Beitragsgarantie***: single life, *Schicht 3* (unsubsidised private provision), monthly
*Beitrag*, one fund, an *Aufschubzeit* ending at a contractually fixed *Rentenbeginn*, a
*Beitragsrückgewähr* death benefit, a guaranteed *Rentenfaktor* applied as the higher of the
guaranteed and the current factor, a *Rückkaufswert* equal to the *Fondsguthaben* with no
*Stornoabzug*, and *Fondswechsel*, *Zuzahlung*, *Teilentnahme*, *Ablaufmanagement* and
*Beitragsfreistellung* as switchable options.

**Why that design and not another**, in four arguments — arguments rather than observations,
because no carrier-level observation was available:

1. **No guarantee**, because the guarantee technologies of the German market cannot be
   demonstrated honestly in a deterministic projection (see *Riders and options*), and because
   the guarantee-free form is a real and growing market form rather than a simplification of the
   only form sold [S7] [S8] [S9].
2. ***Beitragsrückgewähr* death benefit**, because it is the only death-benefit shape with
   corroboration anywhere in the delib corpus [S2] and the shape that makes the *Risikobeitrag*
   mechanic non-trivial without making it dominant: the net amount at risk is positive early and
   vanishes later, so the model must recompute it every month rather than once.
3. **Acquisition charge at the statutory cap, spread over five years**, because the cap [R12]
   [REG-R16] and the spreading [R1] [REG-R28] are the two acquisition-cost facts with any
   corroboration, and a reference implementation should demonstrate the binding constraint rather
   than an unsourced interior point.
4. **A derived rather than a quoted *Rentenfaktor***, because no market level exists anywhere in
   this corpus and a quoted one would be an invention; the derivation below, from a 0 %
   *Rechnungszins* [S10] and a generational annuitant table [R16] [REG-R49], is checkable
   arithmetic labelled **[std]** at every appearance.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Fondsgebundene Rentenversicherung, deferred, single life, *Schicht 3*; no *Beitragsgarantie*; unit-linked accumulation converted at *Rentenbeginn* | [S1] [S2] [S3]; design **[std]** (1) |
| *Versicherungssparte* | *Fonds- und indexgebundene Lebensversicherung*, a *Sparte* in its own right under Anlage 1 VAG, with a segregated *Anlagestock* | [R15] [REG-R5] [REG-R7] |
| Legal wrapper | Individual contract on the applicant's own life; the *Versicherungsnehmer* and the *versicherte Person* coincide | [S1] |
| Premium form (model-point parameter) | (i) `laufend` — level recurring *Beitrag*, the dominant form; (ii) `einmal` — *Einmalbeitrag* | (i) [S1] [S2]; (ii) **[std]** (2) |
| Payment frequency | Monthly, quarterly, half-yearly or annual; monthly by *SEPA-Lastschrift* is the dominant mode | [S1]; dominance `[unverified]` |
| Entry ages | 18 to 60 | envelope **[std]** (3) |
| *Rentenbeginn* age | 67; the contract may fix any age from 62 to 85 | tax floor 62 [R20] [REG-R45]; choice **[std]** (4) |
| Minimum *Aufschubzeit* | 12 years, so the contract can reach the § 20 EStG twelve-year threshold | [R20] [REG-R45]; level **[std]** (4) |
| Minimum premium | 25,00 EUR per month, or 5,000.00 EUR as an *Einmalbeitrag* | **[std]** (3) |
| Age basis | Age last birthday at inception, stepping at each policy anniversary | **[std]** (5) |
| Fund range | One fund in the reference implementation; real tariffs offer 50–300 *Investmentfonds* and ETFs | one fund **[std]** (6); range `[unverified]` [S6] [S13] |
| *Anteilspreis* and *Bewertungsstichtag* | Units bought and cancelled at the fund's *Rücknahmepreis* (redemption price), the *Ausgabeaufschlag* waived in full, at the month boundary — on a monthly grid the dealing-lag convention disappears | **[std]** (7) |
| Anchor model cell | Entry age 37, *Rentenbeginn* 67, monthly *Beitrag* 200,00 €, premium term 30 years, *Beitragsrückgewähr*, no options | **[std]** (8) |

Footnotes to **[std]** rows:

1. **No AVB, *Produktinformationsblatt* or *Basisinformationsblatt* for any German
   fondsgebundene Rentenversicherung was retrieved or searched.** The identity row states the
   product class, not a carrier's tariff. What the corpus does establish is that a
   market-standard clause inventory exists — the GDV publishes *Musterbedingungen* from which
   member insurers derive their AVB, which is why insurer wordings are structurally
   interchangeable [S1] [R23] [REG-R37].
2. The *Einmalbeitrag* form isolates the acquisition-charge mechanic: with no future premiums
   there is nothing to zillmer against, the five-year spread has no work to do, and the whole
   charge falls at inception, at the *Zuzahlungskosten* rate **[std]**.
3. **No entry-age, premium or term envelope was established at any carrier.** Entry ages roughly
   15/18 to the low 60s and minimum monthly premiums of 25 to 50 € are the shape the German
   market is understood to use `[unverified]`; the composite takes the wider end of each, and a
   model point at entry age 60 with a two-year deferment exercises the boundary.
4. *Rentenbeginn* at 67 matches the *Regelaltersgrenze*; 62 is a **tax** floor rather than a
   product floor, because the half-income treatment of a lump sum under § 20 Abs. 1 Nr. 6 EStG
   requires payment after completion of the 62nd year of life for contracts concluded after
   31 December 2011, and a term of at least twelve years [R20] [REG-R45]. **A model point whose
   configuration could not satisfy that test would not be representative of a real sold
   contract**, which is why the minimum deferment is set at twelve years.
5. **No age basis was established for any carrier.** Age last birthday is the convention the
   shipped mortality proxy is indexed on; on a monthly grid the difference from age next birthday
   is a twelve-month shift of one lookup, quantified in the technical notes.
6. Real tariffs offer a *Fondsauswahl* running to hundreds of funds and the premium may be split
   across several. With a deterministic return a multi-fund split is arithmetically identical to
   one composite fund at the weighted return, so the composite carries **one fund** and
   represents *Fondswechsel* and *Ablaufmanagement* as changes to the assumed return rather than
   as reallocations. The consequence — the model cannot show dispersion between funds — is a
   listed model risk.
7. German insurers are understood to buy policy units at the *Rücknahmepreis*, the policy's own
   acquisition charge taking the place of the retail *Ausgabeaufschlag*. **No wording confirming
   a full waiver was seen**, and no carrier's *Bewertungsstichtag* convention was established. On
   a monthly grid both are immaterial; on a daily one neither is.
8. Entry age 37 with a 30-year deferment and a 200,00 € monthly *Beitrag* makes the
   *Beitragssumme* exactly 72 000,00 €, the acquisition charge at the statutory cap exactly
   1 800,00 €, and the five-year instalment exactly **30,00 € per month — 15 % of each of the
   first 60 premiums**. The shape of the product is then legible in round numbers and the cliff
   at month 60 is exact.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| *Beitrag* | 200,00 EUR per month, level, payable for 30 years to *Rentenbeginn* | **[std]** (8) |
| *Beitragssumme* | `Beitrag × (12 / prem_mode_months) × premium term` = 72,000.00 EUR — the sum of all premiums **payable**, not paid | definition [R12] [REG-R16] |
| Premium timing | In advance, at the start of each payment period | **[std]** (9) |
| *Ratenzahlungszuschlag* | A loading for paying more often than annually; the composite reads the **instalment stated in the policy** and does not re-apply a loading | mechanic [S1]; level `[unverified]`; treatment **[std]** (9) |
| Premium-paying term | Equal to the *Aufschubzeit* in the base case; a shorter term is permitted and shortens the acquisition-charge spread | **[std]** (10) |
| *Beitragsdynamik* | Optional annual increase of the *Beitrag*, 3 % or 5 % or index-linked; individual increases may normally be declined | mechanic [S1] [S6]; levels `[unverified]`; base run 0 % **[std]** (11) |
| *Zuzahlung* | Additional single premium into an existing contract, minimum 500,00 EUR, subject to its own acquisition charge; raises the *Beitragssumme* | mechanic [S6]; minimum and maximum `[unverified]`; **[std]** (12) |
| Premium cessation | On death, on *Storno*, on *Beitragsfreistellung* and at *Rentenbeginn* | [S1] [R3] [REG-R28] |
| Non-payment path | *Mahnung* and, on continued default, conversion to a *beitragsfreie Versicherung* rather than termination, because the contract has a positive value from the first month | [R3] [REG-R28]; treatment **[std]** (13) |

9. Premiums in advance is the German norm and the only convention under which the
   *Beitragsverrechnung* below makes sense: the deductions are taken from a premium that has
   arrived. The *Ratenzahlungszuschlag* is real — German tariffs price an annual premium below
   twelve monthly ones — but **no level was established at any carrier**, the plausible band
   being 0–5 % of the annualised premium. Rather than invent one, the composite treats the model
   point's premium as the **instalment the policy states**, which already contains whatever
   loading the tariff applied. Applying a further loading to it is a listed pitfall.
10. A premium term shorter than the deferment exposes an edge in the statutory spreading rule:
    where it is shorter than five years there are fewer than sixty premiums to spread the
    acquisition charge over. The composite spreads it over `min(60, premium term in months)`
    instalments **[std]**, so the charge is fully taken and no instalment is charged against a
    premium that is not paid.
11. Real tariffs **re-zillmer each accepted increment over its own sixty months**, because an
    increment is optional and cannot be assumed at inception. The composite therefore fixes the
    *Beitragssumme* and the acquisition charge **on the initial premium level**; the direction of
    the bias — the acquisition charge on a dynamic contract is understated — is stated in the
    technical notes.
12. **No *Zuzahlung* minimum, annual maximum or charge rate was established at any carrier.** The
    500,00 € minimum and the 2,5 % charge are **[std]**.
13. § 165 VVG gives the right to demand a *beitragsfreie Versicherung* and § 166 converts the
    contract automatically where the insurer terminates for non-payment [R3] [REG-R28]. On a
    unit-linked contract that conversion is trivial — nothing is recomputed, the units stay — so
    the composite routes non-payment to *Beitragsfreistellung* rather than to surrender, which is
    both the statutory default and the economically correct one. Insurers set a **minimum
    *Fondsguthaben*** below which *Beitragsfreistellung* is refused; **no level was established**
    and the composite carries none.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit at *Rentenbeginn* | A lifelong monthly annuity, `Fondsguthaben / 10 000 × Rentenfaktor` | [R22]; factor level **[std]** (14) |
| *Rentenfaktor* rule | `max(garantierter Rentenfaktor, aktueller Rentenfaktor am Rentenbeginn)` — a guarantee **with upside** | [S4] [R22] |
| *Garantierter Rentenfaktor* | 25,00 EUR per month per 10 000 EUR of *Fondsguthaben* at age 67 | **[std]** (14) |
| Conversion basis | A recognised mortality table — currently DAV 2004 R, generational — at an underlying interest rate of currently 0 % p.a. | [S10] for the classic tariff at one carrier; transfer to the fondsgebundene tariff is an inference; [R16] [REG-R49] |
| *Rentengarantiezeit* | 10 years, not priced as a separate option in the composite | mechanic [S1]; menu 0/5/10/15 years `[unverified]`; choice **[std]** |
| *Kapitalwahlrecht* | The *Fondsguthaben* may be taken as a lump sum at *Rentenbeginn* instead of the annuity, on notice | mechanic [S1] [R20]; notice period `[unverified]`; take-up **[std]** (15) |
| *Todesfallleistung* before *Rentenbeginn* | `max(Fondsguthaben, Summe der gezahlten Beiträge)` — the *Beitragsrückgewähr* form | [S2] |
| Alternative death-benefit shapes | (i) *Fondsguthaben* alone; (ii) 100/105/110 % of the *Fondsguthaben*; (iii) a *garantierte Mindesttodesfallleistung* fixed at issue | (i)–(iii) mechanic [S1]; percentages `[unverified]`; all four carried as a model-point parameter |
| *Risikobeitrag* | Levied monthly by cancelling units, on the *riskiertes Kapital* = `max(Todesfallleistung − Fondsguthaben, 0)`, priced on a **death** table | mechanic [S1]; basis DAV 2008 T [R17] [REG-R48]; level **[std]** |
| *Überschussbeteiligung* | Arises from the *Risikoergebnis* and the *übrige Ergebnis* only; credited as additional units, as a charge reduction or as a *Schlussüberschuss* | [R5] [R14] [REG-R9] [REG-R18]; **not projected** (16) |

14. **This is the single most consequential [std] in the document, and it is derived rather than
    guessed.** No *Rentenfaktor* level, range or time series was established — not for this
    product, not for the classic one in a sibling delib file, not from the rating house whose
    article is titled with the question [R23]. The derivation: at a *Rechnungszins* of **0 %**
    [S10] a monthly annuity of `R` per 10 000 € payable for an expected `T` years has a present
    value of `12 × T × R` per 10 000 €, so the pre-cost factor is `10 000 / (12 × T)`. On a
    **generational** annuitant table [R16] [REG-R49] a 67-year-old of a cohort now in mid-career
    has an expected annuity duration materially longer than a period table implies; `T` of 25 to
    28 years gives a pre-cost factor between **29,8 and 33,3**. Deducting the payout-phase
    administration charge and a margin for the *Sicherheitsabschlag* and the *Rentengarantiezeit*
    brings the guaranteed factor materially below that, and the composite takes **25,00 €**, a
    round number inside the band and the value the consumer literature uses illustratively [R22].
    Read the other way, 25,00 at a 0 % *Rechnungszins* prices the guarantee as though the insurer
    will hold the capital for **33⅓ years** and earn nothing on it — a *Sicherheitsabschlag* on a
    thirty-year-forward promise made concrete. The composite's factor **varies with the
    *Rentenbeginn* age** on the same arithmetic, so a contract converting at 62 or at 70 is
    priced consistently.
15. **No *Kapitalwahlrecht* take-up rate was established anywhere**, and it is the largest
    behavioural unknown in the product, because the two tax regimes genuinely differ. The base
    run takes the **annuity** with a take-up of 0 % **[std]**, so that the *Rentenfaktor* — the
    only guarantee the contract carries — is the thing the worked example demonstrates. It is not
    an estimate of behaviour and must not be read as one.
16. The investment result belongs to the policyholder by construction, so it never enters the
    insurer's *Rohüberschuss* and the *Bewertungsreserven* limb of § 153 VVG has almost nothing
    to attach to [R5] [REG-R9]. What is left is a risk and cost surplus on a contract whose death
    cover is a *Beitragsrückgewähr* — second-order in size. **No crediting mechanism was
    confirmed at any carrier, no declared rate was established, and the MindZV percentages are
    `[unverified]`** [R14] [REG-R18]. The composite omits the credit and records the bias:
    omitting it understates the projected *Fondsguthaben*, the honest direction for a charge
    demonstration.

### Underwriting and rating

| Parameter | Representative value | Basis |
|---|---|---|
| Medical evidence | None on the representative design. A *Beitragsrückgewähr* death benefit puts almost no capital at risk, so a *Gesundheitsprüfung* is not normally required | mechanic [S1]; **[std]** (17) |
| When underwriting appears | Where the death benefit is a *garantierte Mindesttodesfallleistung* or a percentage of the fund materially above 100 %, the excess is death cover and is underwritten | mechanic [S1]; thresholds `[unverified]` |
| Rating factors | Attained age (through the *Risikobeitrag*) and the *Rentenbeginn* age (through the *Rentenfaktor*). **Sex may not be one** | [REG-R34]; [R16] [R17] |
| Occupation, smoker | Not rating factors on a savings tariff | **[std]** |
| Mortality basis for the death charge | **DAV 2008 T**, first order — a death-benefit table, *not* the annuity table | [R17] [REG-R48] (17) |
| Mortality basis for the *Rentenfaktor* | **DAV 2004 R**, generational, first order | [R16] [S10] [REG-R49] (17) |
| Best-estimate basis | The second-order versions of the same tables; the wedge between first and second order **is** the *Risikoergebnis* | [REG-R47]; levels **[std]** (18) |

17. **A German FRV carries two mortality bases at once**, and this is where they meet. The
    direction of prudence forks — a death cover is loaded by assuming mortality **higher** than
    expected, an annuity by assuming it **lower** and improving **faster** [REG-R47] — so **a
    model that uses one table for both misprices one of them**. That German tariffs are built
    this way is an inference from practice; **no AVB confirming it was seen**.
18. **DAV tables are the property of the Deutsche Aktuarvereinigung, are not public and are not
    redistributed by this library.** They are cited by name; the reference implementation ships
    **[std]** proxies with their anchors stated, and the technical notes say what a replacement
    must preserve — for DAV 2008 T an insured-lives death basis with selection and **no**
    projected improvement, for DAV 2004 R a generational basis with safety in **both** level and
    trend [REG-R47] [REG-R48] [REG-R49].

### Charges

**This is the most important table in the specification, and every level in it is [std].** The
**structure** is German market practice and is common ground; the **levels** were established
nowhere in this corpus — not one *Abschlusskostenquote*, not one *Verwaltungskostensatz* in
either form, not one *Stückkosten* amount, not one *Effektivkostenquote*, not one commission
rate, at any carrier [S3]–[S14] [S16] [S18] [R23] [R24]. The only numeric anchor in the whole
stack is the 25 ‰ *Höchstzillmersatz* [R12] [REG-R16], and that is corroborated only at the
level of a secondary consumer page in a sibling delib file.

| Charge | German name | Base | Timing and mechanism | Composite level | Argued range |
|---|---|---|---|---|---|
| Acquisition | *Abschluss- und Vertriebskosten* (*Alpha-Kosten*) | *Beitragssumme* | withheld from the premium, spread evenly over the first 60 months | **2.50 %** of the *Beitragssumme* — 1,800.00 EUR, i.e. 30.00 EUR per month | 0 % (*Nettotarif*) to 2.5 % (the statutory cap) |
| Premium admin | *beitragsbezogene Verwaltungskosten* (*Beta-Kosten*) | each gross *Beitrag* | withheld from the premium, whole premium-paying term | **4.00 %** of each premium | 2 % to 10 % |
| Fund admin | *kapitalbezogene Verwaltungskosten* (*Gamma-Kosten*) | *Fondsguthaben* | monthly, by cancelling units | **0.30 % p.a.**, taken as 0.025 % per month | 0.10 % to 1.20 % p.a. |
| Policy fee | *Stückkosten* | per policy | monthly, by cancelling units | **3.00 EUR** per month | 0 to 5 EUR per month |
| Risk charge | *Risikobeitrag* | *riskiertes Kapital* | monthly, by cancelling units | `q_tariff(x)/12 × riskiertes Kapital`, DAV 2008 T proxy | a priced risk, not a load |
| Fund cost | *TER* (*Gesamtkostenquote*) | fund assets | continuously, **inside the unit price** | **0.45 % p.a.**, netted off the assumed gross return | 0.15 % (ETF) to 2.00 % p.a. (active) |
| Trail rebate | *Kickback* / *Bestandsprovision* | fund assets | credited to the *Fondsguthaben* where credited at all | **0.00 % p.a.** | 0 % to 0.50 % p.a. |
| Top-up | *Zuzahlungskosten* | each *Zuzahlung* | withheld on receipt | **2.50 %** of the *Zuzahlung* | 0 % to 4 % |
| Fund switch | *Fondswechselgebühr* | per switch beyond a free allowance | on election | **0.00 EUR** (allowance not exhausted) | 0 to 25 EUR |
| Surrender | *Stornoabzug* | *Fondsguthaben* | on *Kündigung* | **0.00 %** | zero at many unit-linked tariffs; where present, must be quantified in the contract |
| Annuity admin | *Rentenbezugskosten* | each annuity payment | in payment — **out of scope**, delib `sofortrente` | 1.5 % of each payment | 0 % to 3 % |

**The acquisition charge is the one charge whose level has a real anchor, and the composite
takes the cap.** § 4 DeckRV caps the *Zillmersatz* at 25 ‰ of the *Beitragssumme*, the rate used
at conclusion applies for the whole term, and the cut from 40 ‰ took effect on 1 January 2015
with the LVRG [R12] [R13] [REG-R16] [REG-R20]. The composite takes **the cap as the level**,
because a reference implementation should demonstrate the binding constraint rather than a
guessed interior point and because the cap is the only acquisition-cost number with any
corroboration anywhere in this library. A *Nettotarif* — the same contract with the *Abschluss-
und Vertriebskosten* removed and the adviser paid a fee under a separate *Vergütungsvereinbarung*
[S18] — is carried as a **charge variant on the same chassis**, not as a separate product, and it
brackets the range from below.

**The two *Verwaltungskosten* are named by their base, and the difference is load-bearing.**
*Beitragsbezogene* charges are a percentage of each gross premium and **stop when premiums
stop**. *Kapitalbezogene* charges are a percentage per annum of the *Fondsguthaben*, taken
monthly by cancelling units, and **continue after premiums stop** — they make a paid-up policy
decay, and in a long contract they dominate the *Effektivkosten* because they compound against
the whole accumulated fund.

**The fund's own TER is inside the unit price and is not a policy charge.** It never appears in
the policy ledger: a model that charges it explicitly double-counts, one that ignores it
overstates the policyholder's return, and the composite **nets it off the assumed gross return**,
which is exactly what it is. The *Kickback* paid out of that TER is set to **zero** on the ground
that the composite's fund is a passive one that pays no trail — which sidesteps two unresolved
questions: whether an insurer may retain a *Bestandsprovision* under the IDD-derived
*Zuwendungen* rules [R15] [REG-R33], and how a rebate credited back is treated inside the PRIIPs
cost calculation [R7] [R8] [REG-R32].

**Commission is an expense, not a charge, and the composite sets it equal to the charge:**
acquisition commission of **2.50 % of the *Beitragssumme* at inception** — exactly the
acquisition charge it will recover over sixty months — plus a 200,00 € issue expense and renewal
commission of 1.5 % of each premium **[std]**. **No German commission scale was established at
any carrier.** The equality is deliberate: it makes the model demonstrate, in one number, the
financing problem the *Höchstzillmersatz* and the five-year spread exist to regulate.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| *Rückkaufswert* | The ***Zeitwert***, which on a pure unit-linked contract **is the *Fondsguthaben*** | [R1] [REG-R28] |
| *Stornoabzug* | **0.00 %.** Permissible only if *vereinbart*, *beziffert* and *angemessen*; a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten* is expressly ineffective, with the burden of proof on the insurer | [R1] [REG-R28]; level **[std]** (19) |
| *Kündigung* | At any time for the end of the current *Versicherungsperiode* — on a monthly-premium contract, a short notice period rather than an annual one | [R2] [REG-R28] |
| Early values | Poor, and **not because of a deduction**: at the composite's levels a contract surrendered in year 3 has had 15 % of every premium taken for acquisition plus the ongoing charges, so the *Rückkaufswert* is well below premiums paid even in a flat market | arithmetic on the [std] stack (20) |
| Protection for the policyholder | Sits **earlier**, in the *Beitragsverrechnung*: because the acquisition charge may only be taken over the first five years, units are bought from the first month and the value is positive from the start | [R1] [REG-R28] (20) |
| *Beitragsfreistellung* | Premiums stop, units stay, premium-based charges stop with the premium, fund-based charges and the *Risikobeitrag* continue by unit cancellation — so the contract **decays** | [R3] [REG-R28] |
| *Widerruf* | 30 days for a life contract; the amount repayable is tied to the **unit value at the date of cancellation**, so it is not a full premium refund after a market fall | [R6] [REG-R23]; rule `[unverified]`; **not projected** |
| *Teilentnahme* | A partial withdrawal during the *Aufschubzeit*, subject to a minimum and to a minimum remaining *Fondsguthaben* | mechanic [S6]; levels `[unverified]`; **[std]** |

19. **Many unit-linked tariffs have no *Stornoabzug* at all**, precisely because § 169 Abs. 5
    VVG makes a deduction for unamortised acquisition costs ineffective and puts the burden of
    proof on the insurer [R1] [REG-R28] [REG-R36]. The composite sets it to zero, the parameter
    present and switchable, because a non-zero level would be an unsourced number attached to a
    contested clause. **No BGH decision on *Rückkaufswert*, *Kostenverrechnung* or *Stornoabzug*
    is cited anywhere in this document**: the line of authority is well known and no case
    reference could be established [R26] [REG-R36].
20. Whether the statutory *Mindestrückkaufswert* floor formally reaches the *Zeitwert* branch at
    all, or whether the same protection operates through the tariff by limiting the deduction to
    one fifth per year so the units are never removed in the first place, **was not
    established**. The market implements the second, and that is what the composite models.
    **Both readings produce the same numbers on this design**, which is why the ambiguity is
    recorded rather than resolved.

---

## Contractual mechanics

### The *Beitragsverrechnung* — the operative rule of the accumulation phase

The rule is *what is taken out of each gross premium, in what order, before the remainder buys
units*. The German market order, which the reference implementation follows [S1]: the gross
*Beitrag* `B` arrives at the start of the payment period; the ***Abschluss- und
Vertriebskosten* instalment** `α(t)` is withheld, non-zero only in the first sixty months; the
***beitragsbezogene Verwaltungskosten*** `β × B` are withheld, for the whole premium-paying
term; the remainder is the ***Anlagebeitrag***, and it **buys units at the *Anteilspreis***.
Separately, and **by cancelling units rather than by withholding premium**, the
***kapitalbezogenen Verwaltungskosten*** `γ` are taken on the *Fondsguthaben*, together with the
***Stückkosten*** and the ***Risikobeitrag*** on the net amount at risk.

**That distinction is the easiest thing on this product to get wrong.** Premium-based charges are
withheld *before* units exist; fund-based charges cancel units that already exist. A paid-up
contract loses the first group entirely and keeps the second in full — which is why it decays.
**A model that nets the fund-based charge out of the premium instead of cancelling units produces
the right answer while premiums are paid and the wrong answer the moment they stop.**

The composite takes the ***Stückkosten* by cancellation**, where the German market takes it
either by withholding or by cancellation. The argument: cancellation is the only rule that
behaves identically at every payment frequency and identically before and after
*Beitragsfreistellung*, so the fixed fee cannot silently stop when premiums do. The alternative
gives the same total and a marginally different unit count, quantified in the technical notes.

### The unit / non-unit split, and what the insurer's cash flow actually is

The policy's value is the ***Fondsguthaben***: the number of *Anteileinheiten* held in each fund,
multiplied by that fund's *Anteilspreis* at the *Bewertungsstichtag* [S17]. **Units are the state
variable and euro are derived**; every operation on the contract is a purchase or a cancellation
of units at a price on a date.

Everything that is *not* the unit holding is a cash flow in the insurer's own accounts: the
charges it withholds or cancels, the *Risikobeitrag* it collects, the excess of a death benefit
over the fund it releases, its expenses and its commission. **The reference model projects the
non-unit cash flows and carries the unit fund only as the base on which they are computed** —
the right emphasis for a liability model, because the unit fund is the policyholder's money
passing through. Every benefit — the death benefit up to the fund, the *Rückkaufswert*, the
*Teilentnahme*, the capital converted at *Rentenbeginn* — is funded by cancelling the
policyholder's own units, so a gross presentation would count the same money twice, and the
insurer's non-unit cost on a death is **exactly the *riskiertes Kapital***. The VAG makes this
structural rather than a modelling convenience: assets covering unit-linked liabilities are held
**in the corresponding units**, in a separate *Anlagestock* section of the *Sicherungsvermögen*
[R15] [REG-R7], so **a unit-linked projection has no investment-mismatch term**.

### *Abschluss- und Vertriebskosten* — the cap, the spread and the cliff

Two independent rules combine and a specification has to keep them apart. § 4 DeckRV governs what
an insurer may **reserve**: the *Zillmersatz* may not exceed 25 ‰ of the *Beitragssumme*, and the
rate used at conclusion applies for the whole term [R12] [REG-R16]. § 169 Abs. 3 VVG governs what
it must **pay**: on *Kündigung* at least the *Deckungskapital* that results when the *angesetzte
Abschluss- und Vertriebskosten* are spread evenly over the first five contract years [R1]
[REG-R28]. In a unit-linked tariff the second is implemented inside the *Beitragsverrechnung* —
**only one fifth of the total may be withheld in each of the first five years**, so units are
bought from the first month rather than not at all.

The arithmetic on the anchor cell, because it is the shape the model reproduces: *Beitragssumme*
= 200 × 12 × 30 = **72 000,00 €**; acquisition charge at the 2,5 % cap = **1 800,00 €**; spread
over 60 months = **30,00 € per month**, which is **15 % of each of the first 60 premiums** and
**nothing thereafter**. The step at month 61 — the *Anlagebeitrag* jumping from 162,00 € to
192,00 € on an unchanged premium — is the single most legible fact in the projection.

Two derived rules follow. On an **in-force** contract past month 60 the charge is **zero**, and so
is any acquisition expense: the money was spent, and charging it again is a listed pitfall. On an
***Einmalbeitrag*** there are no future premiums to zillmer against, so the whole charge falls at
inception at the *Zuzahlungskosten* rate.

### *Todesfallleistung* and the *Risikobeitrag*

Four shapes are used in the German market, in ascending order of the risk they impose on the
insurer: the ***Fondsguthaben*** alone, with no net amount at risk and no *Risikobeitrag*;
***Beitragsrückgewähr***, `max(Fondsguthaben, Summe der gezahlten Beiträge)`; **a percentage of
the *Fondsguthaben***, commonly 100, 105 or 110 % `[unverified]`; and a ***garantierte
Mindesttodesfallleistung***, a stated sum chosen at issue and independent of the fund [S1].

The composite adopts **Beitragsrückgewähr**, the shape corroborated at DEVK [S2] and the only
death-benefit fact with corroboration anywhere in this corpus. It is also the shape that makes
the mechanic interesting: the net amount at risk is `max(Summe der gezahlten Beiträge −
Fondsguthaben, 0)`, positive **early, and after a market fall**, and vanishing once the fund
overtakes the premiums paid. **Cumulative premiums paid is therefore a state variable of this
product, not a reporting convenience** — and it is the premiums *paid*, gross, not the premiums
*invested*. The charge is recomputed every month, because both the benefit and the fund move:

    riskiertes Kapital(t) = max( Todesfallleistung(t) − Fondsguthaben(t), 0 )
    Risikobeitrag(t)      = q_tariff(x) / 12 × riskiertes Kapital(t)
    units cancelled       = Risikobeitrag(t) / Anteilspreis(t)

`q_tariff` is a **first-order death table** — DAV 2008 T [R17] [REG-R48] — carrying explicit
safety margins, while the projection's own decrement is the **second-order** best estimate
[REG-R47]. **The difference between them is the *Risikoergebnis***, and it is the source of the
*Überschussbeteiligung* the composite declines to project. A model that uses one table for both
makes the risk result identically zero and loses the mechanic.

### The *Rentenfaktor* — the product's only financial guarantee

    monatliche Rente = Fondsguthaben(Rentenbeginn) / 10 000 × Rentenfaktor

100 000 € at a factor of 25 yields 250 € per month [R22] — a teaching example, not a market
level. The *garantierter Rentenfaktor* is fixed in the contract documents at conclusion and rests
on the *Rechnungsgrundlagen* then in force: a mortality table, currently DAV 2004 R, and a
*Rechnungszins*, currently 0 % p.a. at the one carrier where the statement was corroborated, and
there for its **classic** tariff [S10] [R16] [REG-R49]. The *Sicherheitsabschlag* the insurer
applies is why the guaranteed factor is lower than the factor the same insurer would quote for an
immediate annuity today.

**The rule at *Rentenbeginn* is a maximum of two factors, and it is a guarantee with upside:**

    Rentenfaktor_angewendet = max( Rentenfaktor_garantiert, Rentenfaktor_aktuell )

At a conventional carrier the corroborated form is that at the start of annuity payments a second
factor is compared with the guaranteed one and **the higher of the two is guaranteed for the
payment period** [S4]; at the market leader the current bases at *Rentenbeginn* are those the
company uses at that time for immediately beginning annuities [S3] [R22]. **A model that applies
only the guaranteed factor understates the benefit whenever the current tariff is richer**, and
one model point in the shipped table is configured so that the `max()` actually bites.

**Reduction of a guaranteed factor.** Insurers could previously change guaranteed
*Rentenfaktoren* under a *Treuhänderklausel*, with an independent external *Treuhänder*'s
approval, on two triggers: an unexpectedly strong increase in life expectancy, and a sustainable
reduction in capital-market returns. **That route is now closed wherever the clause is drafted
asymmetrically.** In **BGH, Urteil vom 10. Dezember 2025 — IV ZR 34/25** a clause in the AVB of a
*fondsgebundene Rentenversicherung* letting the insurer reduce the *Rentenfaktor* named in the
*Versicherungsschein* — the monthly annuity per 10 000 € of *Vertragsguthaben* — **without a
corresponding duty to restore it if circumstances improve** was held **void** under § 308 Nr. 4
BGB and § 307 Abs. 1 Satz 1 BGB, on principles reported to reach all comparable clauses
[REG-R36]. The rule is therefore not that the guaranteed factor is "changeable only under
§ 163 VVG": it is that **a *garantierter Rentenfaktor* is a hard guarantee unless the AVB confers
a *symmetric* adjustment right**, with § 163 VVG the residual statutory route, on its own much
narrower conditions, where the tariff's calculation bases themselves fail [R4] [R22] [REG-R27].
Below that line the Landgericht Köln had already held that the low-interest phase is not a
sufficient ground, being entrepreneurial risk that cannot be passed to policyholders — **that
decision's reference, date and parties could not be established and no docket is given for it**.
Trade press of 4 February 2021 reports the market leader's position that customers could not
successfully object to an adjustment, placing a live commercial dispute at the largest German
life insurer inside the window in which the current in-force unit-linked book was written [R22].
The composite treats the guaranteed factor as **fixed for the life of the contract**, and after
IV ZR 34/25 that is **the legally correct default rather than a modelling simplification**
[REG-R36]. What remains a model risk is the narrow residue: a § 163 VVG adjustment, and an AVB
that does confer a symmetric right.

### *Rückkaufswert* — the *Zeitwert* branch, and what it removes

For *fondsgebundene Versicherungen* and other contracts whose benefit is not guaranteed at a
fixed amount, § 169 VVG makes the *Rückkaufswert* the ***Zeitwert*** of the insurance, computed
by recognised actuarial rules [R1] [REG-R28]. For a pure unit-linked contract with no
insurer-given benefit guarantee the *Zeitwert* is **the value of the units held**:

    Rückkaufswert(t) = Fondsguthaben(t) − Stornoabzug(t)

What that removes is the whole conventional apparatus: no discounting, no *Rechnungszins*, no
mortality basis, no *Zillmerung* residue, no *Mindestrückkaufswert* computation on a second
basis. It is the largest single modelling simplification in the delib library. The internal
paragraph designation of the *Zeitwert* branch is **`[unverified]`** and no delib document cites
a subsection number for it.

### *Beitragsfreistellung* — why a paid-up unit-linked policy decays

§ 165 VVG lets the policyholder demand conversion to a *prämienfreie Versicherung* for the end of
the current *Versicherungsperiode* [R3] [REG-R28]. **On a fondsgebundene contract nothing is
converted**: the units stay where they are, premium payment stops, the premium-based charges stop
with it because there are no more premiums to charge them on, and the *kapitalbezogenen
Verwaltungskosten*, the *Stückkosten* and the *Risikobeitrag* continue to be taken by cancelling
units. The paid-up contract therefore **decays** at the fund-based charge rate less the fund's
return, and where the death benefit is a *garantierte Mindesttodesfallleistung* the
*Risikobeitrag* accelerates the decay as the fund falls and the net amount at risk rises — a
feedback the model reproduces automatically and a real product risk. Insurers accordingly set a
minimum *Fondsguthaben* below which *Beitragsfreistellung* is refused and the contract is
surrendered instead; **no level was established**.

***Beitragsfreistellung* and *Storno* are two decrements, not one** — different triggers,
different cash flows, different subsequent projections. Conflating them is a listed pitfall.

### *Fondswechsel* and *Ablaufmanagement*

***Fondswechsel*** covers **two distinct operations**, and German wordings use the English words
*Shift* and *Switch* for them: **reallocating the existing *Fondsguthaben***, where units are
cancelled in the old fund and bought in the new one at the same *Bewertungsstichtag*; and
**redirecting future premiums**, leaving the existing holding where it is. **Which English word
denotes which operation is not consistent across German insurers, and this document asserts no
mapping** — each AVB defines its own terms, and the reference implementation names the
**operations**, not the labels. Free-switch allowances and switch fees were **not established**.

***Ablaufmanagement*** is automatic phased de-risking in the run-up to *Rentenbeginn*: the
*Fondsguthaben* is moved in tranches out of equity funds into money-market or *Wertsicherungs*
funds, or into the insurer's *Sicherungsvermögen*. **Whether it is opt-in or a default, over how
many years, in what tranches and into what were all not established** `[unverified]`; a five-year
ramp is the shape most often described. With one fund and a deterministic return a reallocation
and a change of assumed return are arithmetically the same thing, so the composite implements it
as a **deterministic glide of the assumed gross return to a money-market assumption over the last
60 months**, switchable off — the honest representation of what is known.

### *Zuzahlung*, *Teilentnahme* and the *Abrufphase*

A ***Zuzahlung*** is an additional single premium into an existing contract; it buys units at the
*Anteilspreis* on the following *Bewertungsstichtag*, raises the *Beitragssumme* and carries its
own acquisition charge. A ***Teilentnahme*** is a partial withdrawal during the *Aufschubzeit*,
modelled as a unit cancellation; it is a partial surrender with a partial surrender's tax
consequences [R20] [REG-R45], and it is an **owner election, not a claim**. Both carry minima and
maxima that were **not established** at any carrier.

The ***Abrufphase*** is a window inside which the conversion may be brought forward or deferred.
**Deferring changes the *Rentenfaktor***, because the factor is age-dependent; **whether the
*guaranteed* factor is restated on deferral or only the current one was not established**, nor
was the width of the window. The composite **fixes the *Rentenbeginn*** and records the
*Abrufphase* as an unmodelled option.

### *Effektivkosten* — the metric that ties the stack together

The ***Effektivkostenquote*** states all charges as the annual percentage by which they reduce
the contract's return. It has been required in quotations since 1 January 2015 under § 7 VVG and
the *VVG-InfoV* `[unverified]` [R7] [S16] [REG-R31], and appears in its PRIIPs form in the
*Basisinformationsblatt* at **three time points — one year, half the recommended holding period,
and the end of it** [S15] [R9] [REG-R32]. **For a fondsgebundene contract it must include the fund's
own costs**, which is what makes the *TER* a policy parameter rather than a fund parameter.

Two warnings a specification must carry. The German figure is now aligned to the
**total-cost-indicator method of Annex VI to Delegated Regulation (EU) 2017/653** [REG-R31]
[REG-R32]; the reference implementation does **not** implement Annex VI and does not specify a
recommended holding period, so the reduction in yield it publishes is a **delib-defined** measure
on the contract's own path and is **not** the statutory *Effektivkostenquote*. And **no market
level of any kind was established** [R10] [R23] [R24]: BaFin's "differ considerably" is
qualitative, so any order-of-magnitude figure in the technical notes is arithmetic on delib's own
[std] stack and must never be quoted as a market figure.

---

## Riders and options

**In scope and parameterized.** The **death-benefit shape** `db_form`, carried as a model-point
parameter across all four market shapes, with the *Beitragsrückgewähr* form as the base [S2];
***Beitragsfreistellung***, as a stated month at which premiums cease and the fund-based charges
continue [R3]; ***Zuzahlung*** and ***Teilentnahme***, as a stated month and amount;
***Ablaufmanagement***, as the return glide described above; ***Beitragsdynamik***, as an annual
premium increase with the acquisition charge fixed on the initial level; the ***Kapitalwahlrecht***,
as an election at *Rentenbeginn* that changes the tax treatment and not the amount released; the
***Rentenfaktor*** rule, with both the guaranteed and the current factor as inputs so the `max()`
is exercised; and the ***Stornoabzug***, present at zero and switchable.

**Described and deliberately not implemented — the guarantee technologies.** German insurers wrap
three distinct guarantee designs around this same unit-linked chassis. A ***statisches Hybrid***
(*Zwei-Topf-Hybrid*) splits the premium **once, at inception**, between the *Sicherungsvermögen*
— where a guaranteed pot accretes at the *Rechnungszins* to exactly the guaranteed amount at
*Rentenbeginn* — and free funds; simple, transparent, and at a low *Rechnungszins* it consumes
almost the whole premium for the guarantee. A ***dynamisches Hybrid*** recomputes the split
**periodically**, normally monthly, and its three-pot form inserts a ***Wertsicherungsfonds*** —
a fund with a contractual limit on its loss over a defined period — between the
*Sicherungsvermögen* and the free funds, so money can move out of equities in two steps rather
than one [S7] [S8]. ***i-CPPI*** sets the exposure to the risky fund **per policy and
continuously**, as a multiplier times the cushion between the policy value and the present value
of the guarantee: the most efficient of the three and the most path-dependent [S9].

**Why none is implemented.** Each is a rule for reallocating between a guaranteed pot and a risky
pot **along a path**, and its entire content is what it does when the risky pot falls. A
deterministic projection has one path and it is a smooth one, so a guarantee mechanism modelled
inside it either never triggers — dead code presented as a feature — or triggers on a hand-chosen
shock, which asserts a scenario the model has no basis for. What would have to be added is a
stochastic or at least multi-scenario asset model, a monthly reallocation rule, a guaranteed pot
accreting at a *Rechnungszins*, and a *Wertsicherungsfonds* return model. That is a different
model, and an honest reference implementation says so rather than gesturing at it. **No
reallocation rule, CPPI multiplier, *Wertsicherungsfonds* loss limit, guarantee-pot accretion
rule or carrier guarantee menu was established** [S7] [S8] [S9]. What the composite keeps from
the hybrid world is the *Ablaufmanagement* glide — de-risking without a guarantee, and
representable deterministically.

**Out of scope entirely.** Attached biometric riders (*Berufsunfähigkeits-Zusatzversicherung*,
*Unfall-Zusatzversicherung*, *Hinterbliebenenrente*, *Pflegeoption*), which are separate delib
products or separate covers on their own bases; the **payout phase** (delib `sofortrente`); and
the *Abrufphase*.

---

## Variations across insurers

**Read this first.** **Nothing carrier-specific was observed for this product**: no AVB, no
*Produktinformationsblatt*, no *Basisinformationsblatt* and no rate card was retrieved or
searched, so what follows is **not** a table of observations. The first table records — honestly
and mostly negatively — what is actually established about each named carrier, all of it at one
remove through a sibling delib research file; the second records the **dimensions along which
German carriers are known to differ**, with the range argued from the mechanics and the statutory
bounds.

### What is established, carrier by carrier

| Carrier | Established here | Source |
|---|---|---|
| DEVK | Publishes a *Kundeninformation* for a fondsgebundene Rentenversicherung, document 03101, edition 07/2024; death benefit before *Rentenbeginn* = fund value, **at least premiums paid** | [S2], via a sibling delib file |
| CosmosDirekt (Cosmos Leben) | Inception annuity factor computed on DAV 2004 R at an interest rate of **currently 0 % p.a.** — stated for the **classic** tariff | [S10], via a sibling delib file |
| Allianz Leben | Current bases at *Rentenbeginn* are those the company uses at that time for immediately beginning annuities; *Treuhänderklausel* position publicly defended in February 2021 | [S3] [R22], via a sibling delib file |
| Zurich Deutscher Herold | The *Verbraucherinformation* series is titled "für **Konventionelle** Versicherungen", implying a fondsgebundene companion; at *Rentenbeginn* the **higher of two factors** applies | [S4], via a sibling delib file |
| Debeka | **Discontinued its classic annuity tariff** — the market-structure fact behind this product's dominance | [S14], via a sibling delib file |
| NÜRNBERGER | Publishes per-tariff AVB with codes in an `NIR`/`N` series | [S11], via a sibling delib file |
| Alte Leipziger, LV 1871, Continentale, HDI, Volkswohl Bund, Stuttgarter, WWK, myLife | **Nothing.** Named as real carriers of the right product, with `[unverified]` product names | [S5]–[S9] [S12] [S13] [S18] |

### The dimensions of variation, and the argued range on each

| Parameter | Argued range across the German market | Where the composite sits | Tag |
|---|---|---|---|
| Death-benefit shape | *Fondsguthaben* / *Beitragsrückgewähr* / 100–110 % of fund / guaranteed sum | *Beitragsrückgewähr* | [S2] for the shape; range `[unverified]` |
| Acquisition charge | 0 % (*Nettotarif*) to 2.5 % of *Beitragssumme* (the cap) | 2.5 %, the cap | [R12] [REG-R16] for the cap; interior **[std]** |
| Acquisition spreading | 5 years, uniform — statutory, no variation | 60 months | [R1] [REG-R28] |
| Premium-based admin | 2 % to 10 % of each premium | 4.0 % | **[std]** |
| Fund-based admin | 0.10 % to 1.20 % p.a. of *Fondsguthaben* | 0.30 % p.a. | **[std]** |
| *Stückkosten* | 0 to 5 EUR per month | 3.00 EUR | **[std]** |
| Fund TER | 0.15 % (ETF) to 2.00 % p.a. (active) | 0.45 % | **[std]** |
| *Kickback* crediting | none to full crediting of the trail | none (passive fund) | **[std]**; rule `[unverified]` |
| *Effektivkosten* | a spread BaFin calls "considerable"; **no numeric range established** | approx. 1 % p.a. implied by the stack | [R10] [REG-R35]; level **[std]** |
| Guaranteed *Rentenfaktor* | **no level, range or time series established anywhere** | 25.00 EUR per 10,000 EUR at age 67 | **[std]**, derived |
| Factor rule at *Rentenbeginn* | `max(guaranteed, current)` — appears uniform | `max(guaranteed, current)` | [S4] [R22] |
| *Rentengarantiezeit* | 0, 5, 10, 15 years | 10 years, not priced separately | **[std]** |
| *Beitragsgarantie* | 0 %, 60 %, 80 %, 90 %, 100 % of premiums | 0 % — no guarantee | **[std]**; menu `[unverified]` |
| Guarantee technology | none / static hybrid / dynamic 2- or 3-pot / i-CPPI | none | argued above |
| *Ablaufmanagement* | absent, opt-in, or opt-out default; 3- to 10-year ramps | 5-year monthly glide, switchable | **[std]** |
| Free fund switches | a fixed annual allowance to unlimited | unlimited within modelled behaviour | **[std]** |
| *Stornoabzug* | zero at many unit-linked tariffs; where present, must be quantified | zero | [R1] [REG-R28]; level **[std]** |
| Minimum monthly premium | 25 to 50 EUR | 25 EUR | `[unverified]`; **[std]** |
| Entry ages | roughly 15/18 to the low 60s | 18 to 60 | `[unverified]`; **[std]** |
| *Rentenbeginn* age | commonly 62 (the tax floor) to 85 | 67 | tax floor [R20] [REG-R45]; choice **[std]** |
| Distribution model | commission tariff, direct writer, *Nettotarif* / *Honorartarif* | commission tariff, with a *Nettotarif* charge variant on the same chassis | [S10] [S13] [S18] |

**The one dimension worth isolating.** A *Nettotarif* is the same unit-linked contract with the
*Abschluss- und Vertriebskosten* removed from the tariff, the adviser being paid a fee under a
separate *Vergütungsvereinbarung* [S18]. It matters for one modelling reason: **the difference
between a gross tariff's reduction in yield and the same chassis's net reduction in yield *is*
the acquisition-cost load** — the single parameter this specification most needs and that no
document in the corpus supplies. **No net-tariff or gross-tariff figure is established**; the
observation that the gap exists is structural, not numeric. It is carried as a charge variant in
the shipped tables so that a reader can read the difference off the model instead of looking for
it in a document that was not retrieved.

---

## Regulatory context

**Contract law — the VVG.** Five provisions do the work, and every paragraph number below is
`[unverified]`. **§ 169** makes the *Rückkaufswert* of a fondsgebundene contract the *Zeitwert*,
requires the *angesetzte Abschluss- und Vertriebskosten* to be spread evenly over the first five
contract years for the purpose of the minimum surrender value, and permits a *Stornoabzug* only
where it is *vereinbart*, *beziffert* and *angemessen*, with a deduction for untilgte acquisition
costs expressly ineffective and the burden of proof on the insurer [R1] [REG-R28]. **§ 168** lets
the policyholder terminate at any time for the end of the current *Versicherungsperiode*, which
on a monthly-premium contract is a short notice period — paired with § 169 it makes *Storno* a
near-frictionless exit at fund value, which is why unit-linked lapse experience differs from
conventional lapse experience [R2] [REG-R28]. **§ 165** gives the right to a *prämienfreie
Versicherung* [R3] [REG-R28]. **§ 163** is the only remaining route by which a guaranteed
*Rentenfaktor* may be reduced, and only with an independent trustee's confirmation [R4] [R22]
[REG-R27]. **§ 153** entitles the policyholder to a share of the surplus unless excluded by
express agreement, and here that share can only come from the risk and cost results [R5]
[REG-R9] [REG-R24]. §§ 7–8 and § 152 govern pre-contractual information and the 30-day *Widerruf*
[R6] [REG-R23] [REG-R31].

**Prudential — the VAG and the reserving regulations.** Anlage 1 to the VAG lists *fonds- und
indexgebundene Lebensversicherung* as a *Versicherungssparte* in its own right, which is why
German statistics and insurers' accounts report it separately [R15] [REG-R5]. § 125 VAG requires
a separate section of the *Sicherungsvermögen* — the ***Anlagestock*** — for each *Anlageart*
where benefits are provided in units of an open fund, so unit assets and unit liability move
together exactly [R15] [REG-R7]. § 138 VAG requires premiums to be calculated on prudent
assumptions [REG-R8]. The **DeckRV** supplies the two numbers that matter: the
*Höchstrechnungszins*, which does **not** bind this product's accumulation phase, and the
*Höchstzillmersatz* of 25 ‰, which does [R12] [REG-R14] [REG-R15] [REG-R16]. The **MindZV** fixes
the minimum share of each surplus source credited to policyholders — here the *Risikoergebnis*
and the *übrige Ergebnis* only, because a unit-linked contract's investment result never enters
the *Rohüberschuss*; **the percentages are `[unverified]`** [R14] [REG-R18]. Above it sits
Solvency II through the VAG: a best estimate plus a risk margin [REG-R1] [REG-R2] [REG-R6], with
EIOPA publishing the curves [REG-R4] and Directive (EU) 2025/2 first applying on 30 January 2027
[REG-R3]. **Nothing in this library implements a 2027 basis.**

**Disclosure and conduct.** The PRIIPs Regulation requires a ***Basisinformationsblatt*** for
every packaged retail and insurance-based investment product, and a fondsgebundene
Rentenversicherung is the paradigm German IBIP: uniform delivery requirements apply regardless of
whether the underlying investment options are themselves PRIIPs, which pulls a contract with a
fund menu wholly into scope [R8] [REG-R32]. BaFin's own account of the required content is the
most precisely established regulatory fact available for this product: a **summary risk
indicator**; the **possible maximum loss** of invested capital; **four performance scenarios** —
*Stress*, *pessimistisch*, *moderat*, *optimistisch* — as annualised average returns in per cent;
the **costs the investor bears**; and complaint information — the scenarios and the costs shown at
**three time points**, after one year, after half the recommended holding period and at the end of
it, with the cost disclosure split into **one-off and ongoing costs** and the ***Reduction in
Yield* per year** stated [R9] [REG-R32]. For an FRV those points are typically year 1, year 15 and
year 30. **No actual *Basisinformationsblatt* for this product was located** [S15], so **no scenario
return, no cost figure and no reduction-in-yield value in this document comes from one**. The
categorisation matters and is `[unverified]`: a pure unit-linked contract's scenarios come from the
funds' own return history, a guarantee-bearing one from the DAV's standard method for **PRIIP
Kategorie 4** [R18] — which is why two documents for economically similar products can show very
different scenario returns, and why this specification cites **no** scenario return. Alongside
PRIIPs, § 2 VVG-InfoV requires the *Abschluss- und Vertriebskosten* included in the premium to be
disclosed **in euro**, the other costs separately, and a ***Modellrechnung***; **how many assumed
rates it prescribes for a fondsgebundene contract, and at what levels, was not pinned down** [R7]
[REG-R25] [REG-R31]. The IDD-derived *Zuwendungen* rules govern whether a *Kickback* may be
retained [R15] [REG-R33], and BaFin's *Merkblatt 01/2023 (VA)* supplies the German *Value for
Money* regime described in the overview [R10] [REG-R35].

**Taxation, and why it drives behaviour.** Three regimes meet on this contract, and the
differences between them are the product's commercial argument and its strongest behavioural
driver. In the **accumulation phase nothing is taxed** — no annual taxation of fund income inside
the wrapper, no *Vorabpauschale*, and **no taxable disposal on a *Fondswechsel*** [R20] [R21]
[REG-R45] — while a direct fund holding is taxed on both, which is why a cost comparison against
a *Depot* is not like-for-like. On the **annuity** only the ***Ertragsanteil*** is taxable, at a
statutory percentage set **once** by the annuitant's completed age at *Rentenbeginn* and never
changed, so every later increase is taxed at the same light rate: **at age 65 the figure is
18 %**, **every other age is `[unverified]`** and no table is reproduced here [R19] [REG-R41]. On
a **lump sum**, § 20 Abs. 1 Nr. 6 EStG taxes the ***Unterschiedsbetrag*** between the payment and
the premiums paid, and where the contract has run **at least twelve years** and payment falls
after completion of the **62nd** year of life (60th for contracts concluded before 1 January
2012), **only half** the gain is taxable, § 32d Abs. 2 Nr. 2 EStG putting that half into the
personal marginal rate rather than the flat *Abgeltungsteuer* [R20] [REG-R45]. A
***Teilfreistellung*** applies to the fund income inside the wrapper, commonly stated as **15 %**
for equity exposure — **the sentence, the percentage and the conditions are all `[unverified]`**
[R20] [R21] [REG-R45].

**The behavioural consequence, and the reason this is not merely context.** The twelve-year and
age-62 conditions create a **double threshold** that policyholders wait for: surrenders are
suppressed as it approaches and spike once both limbs are met, and the annuitise-or-commute
election at *Rentenbeginn* is a **tax election**, not a preference. A German Schicht-3 lapse
assumption that is flat in duration has ignored the strongest single driver of German surrender
behaviour [REG-R45]. The reference implementation models it as a duration-and-age-dependent lapse
shape with the threshold named and the level **[std]** — the treatment frlib gives the eight-year
threshold in French *assurance vie*. And the **50 % *Mindesttodesfallschutz* rule** for contracts
concluded from 1 April 2009 is a model-point design constraint rather than a footnote: **how it
applies to a *Rentenversicherung* with and without a *Kapitalwahlrecht* was not established**
`[unverified]` [REG-R45], and the composite's death benefit is not designed to satisfy it.

**Accounting and professional standards.** German statutory reporting runs under HGB §§ 341–341o
and the *RechVersV*, where unit-linked business is reported separately from the general account
[REG-R54]. Under IFRS 17 a fondsgebundene contract is the archetypal direct-participating
contract and would be measured under the **variable fee approach**; the VFA mechanics were not
read and are `[unverified]` [REG-R55]. Actuarial work sits under the DAV's *Fachgrundsätze* and
the responsible actuary's certifications under §§ 141–143 VAG [REG-R11] [REG-R56].

**Living texts.** VVG, VVG-InfoV, DeckRV, MindZV, VAG, EStG and InvStG all change; the PRIIPs
RTS was reworked with effect from 1 January 2023 `[unverified]`; the *Höchstrechnungszins*
changed on 1 January 2025 `[unverified]`; BaFin's focus-risk agenda is annual. **Every paragraph
number and every date in this document is `[unverified]`** and must be re-checked against the
instrument before anything in it is relied on.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-fondsgebundene_rentenversicherung-r1
[R10]: #delib-fondsgebundene_rentenversicherung-r10
[R11]: #delib-fondsgebundene_rentenversicherung-r11
[R12]: #delib-fondsgebundene_rentenversicherung-r12
[R13]: #delib-fondsgebundene_rentenversicherung-r13
[R14]: #delib-fondsgebundene_rentenversicherung-r14
[R15]: #delib-fondsgebundene_rentenversicherung-r15
[R16]: #delib-fondsgebundene_rentenversicherung-r16
[R17]: #delib-fondsgebundene_rentenversicherung-r17
[R18]: #delib-fondsgebundene_rentenversicherung-r18
[R19]: #delib-fondsgebundene_rentenversicherung-r19
[R2]: #delib-fondsgebundene_rentenversicherung-r2
[R20]: #delib-fondsgebundene_rentenversicherung-r20
[R21]: #delib-fondsgebundene_rentenversicherung-r21
[R22]: #delib-fondsgebundene_rentenversicherung-r22
[R23]: #delib-fondsgebundene_rentenversicherung-r23
[R24]: #delib-fondsgebundene_rentenversicherung-r24
[R25]: #delib-fondsgebundene_rentenversicherung-r25
[R26]: #delib-fondsgebundene_rentenversicherung-r26
[R3]: #delib-fondsgebundene_rentenversicherung-r3
[R4]: #delib-fondsgebundene_rentenversicherung-r4
[R5]: #delib-fondsgebundene_rentenversicherung-r5
[R6]: #delib-fondsgebundene_rentenversicherung-r6
[R7]: #delib-fondsgebundene_rentenversicherung-r7
[R8]: #delib-fondsgebundene_rentenversicherung-r8
[R9]: #delib-fondsgebundene_rentenversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R25]: #delib-reg-r25
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R3]: #delib-reg-r3
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R37]: #delib-reg-r37
[REG-R4]: #delib-reg-r4
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R7]: #delib-reg-r7
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
