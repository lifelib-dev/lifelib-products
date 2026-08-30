# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/basisrente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so the
numbering has a gap: **S12** (the GDV *Musterbedingungen* service index) is **not cited** by
`product-spec.md`, `technical-notes.md` or `model.md` and is therefore absent below. The reason
is worth stating rather than leaving to the gap: **whether the GDV publishes a Basisrente model
condition set at all was never established** (gap 5). A GDV *Musterbedingung* would have been
the natural spine for a composite specification, as it was for the delib endowment product, and
this composite had to be built from the statute and the market's settled mechanics instead.
Nothing downstream may assume such a document exists. Every other id — **S1–S11, S13–S16 and
R1–R24** — is cited by at least one of the three product documents and appears below. Access
date for all sources: **2026-08-29**. No sources were newly added at drafting. Cross-product
[REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before relying on a single entry below.** They are the
conditions of house-rules section 3 and they are stated plainly, in the same terms, every time:

1. **Direct HTTP egress from the build environment is blocked by an organisation network
   policy.** `WebFetch` and `curl` are refused with HTTP 403 at the egress gateway for every
   host outside a short package-registry allowlist. The hosts that matter for this product were
   tried and every one was refused: `gesetze-im-internet.de` (EStG § 10 and § 22, AltZertG,
   ZPO § 851c, VVG, DeckRV), `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`,
   `bzst.de` — the authority that certifies *Basisrentenverträge* — and `de.wikipedia.org`.
   **Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one
   *Basisinformationsblatt*, not one statutory text and not one BMF-Schreiben was opened.**
2. **There was no search channel either.** The session's `WebSearch` budget — a hard cap of 200
   calls shared across all delib work — was **exhausted before this product was reached**. Two
   sibling delib research files consumed it. So this product's research was written with **no
   fetch, no search, no snippet and no summary**, which is a materially weaker evidential
   position than either sibling and is stated on every entry rather than glossed.

**A delib citation is a pointer, not a certificate.** An [R1] tag on a sentence about
§ 10 Abs. 1 Nr. 2 Buchst. b EStG means *this is the instrument that claim must be checked
against*. It does not mean anyone read it. **`Retrieved: yes` appears nowhere in this file**,
nothing below is quoted from a German statutory or contractual text, and no URL, document
number, edition, page count or publication date has been invented: where a canonical
`gesetze-im-internet.de` form is obvious it is offered and marked [unverified], and everywhere
else the entry says `URL: not established`. A small number of entries carry a stronger
retrieval line because their **identity** was established in a sibling delib research file
while search was still available; those say so and name the file.

---

## Primary product sources

(delib-basisrente-s1)=

### S1 — Cosmos Lebensversicherungs-AG (CosmosDirekt), *Allgemeine Bedingungen* for the Basisrente — tariffs LA 1100 A, LA 1079 A, LA 936 A, LA 1099 A
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Versicherungsbedingungen* for Basisrente tariffs, in the carrier's `LA nnnn A` house numbering
- URL: **not established.** The carrier's sibling Schicht-3 wording LA 904 A was returned under a `resource/blob` path, so the Basisrente wordings are expected to sit under the same scheme; **no blob path for a Basisrente wording was returned and none is guessed**
- Retrieved: **no** — direct HTTP egress blocked in the build environment; no search corroboration in this product's research (session search budget exhausted). Document identity carried over from the sibling delib research file `_research/klassische_rentenversicherung.md` [S8], which established the carrier's tariff-number list from a search-result summary while search was still available
- Used for: the **four parallel Basisrente tariff codes at one carrier**, which is the only observation in the whole corpus of what a Basisrente tariff family looks like and the single entry in the variations table of `product-spec.md`; the existence of the three premium forms (*laufender Beitrag*, *Zuzahlung*, *Einmalbeitrag*) that the model's `prem_form` and `zuzahlung_pp` implement; and the conversion convention — a *garantierter Rentenfaktor* fixed at inception on **DAV 2004 R at an interest basis of 0 % p.a.** — which stands behind `rentenfaktor_applied()` and the notes' "the conversion basis is not the projection basis" and is [unverified] **as a Basisrente fact**, being a Schicht-3 observation (gap 4)

(delib-basisrente-s2)=

### S2 — Allianz Lebensversicherungs-AG, **BasisRente KomfortDynamik** — specimen *persönlicher Vorschlag*
- Publisher / doc type: Allianz Lebensversicherungs-AG; a distributed specimen quotation ("Berechnung BasisRente KomfortDyn") hosted by a broker rather than by the carrier, dated by its path to **February 2025** [unverified], together with the carrier's *Vorsorgekonzept KomfortDynamik* product page
- URL: product page `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`; the specimen at a broker path recorded in the research file
- Retrieved: **no** — egress blocked; no search corroboration in this product's research (budget exhausted). Identity and both figures carried over from `_research/klassische_rentenversicherung.md` [S13]
- Used for: **the only Basisrente-specific charge evidence in the delib corpus**, and three claims rest on it. First, **the layer is a tax wrapper around a common chassis** — the same design is sold as PrivatRente, BasisRente and RiesterRente — which is the argument in `product-spec.md` for reusing the Schicht-3 chassis and in `model.md` for naming `RV_DE_A` as the sibling. Second, the hybrid asset form with selectable guarantee levels of **60 %, 80 % or 90 % of premiums paid**, 80 % standard [unverified], which is the third row of the asset-form table. Third, the two charge figures — an ***Abschlussprovision* of 1 575 €** on the specimen and **total costs relative to the capital formed of at most 0,95 € per 100 €** [unverified], both from third-party commentary rather than a tariff sheet — which are the only anchor behind `comm_init_rate` and the *Effektivkosten* band, and are why `model.md` calls the charge set a construction rather than a calibration

(delib-basisrente-s3)=

### S3 — Allianz Lebensversicherungs-AG, the **BasisRente** product family
- Publisher / doc type: Allianz Lebensversicherungs-AG; AVB, *Produktinformationsblätter* and *Verbraucherinformationen* for the carrier's Basisrente tariffs, marketed as BasisRente Klassik, BasisRente Perspektive and BasisRente InvestFlex [unverified] as to the current line-up
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing beyond the family's existence.** It appears in the variations table of `product-spec.md` as the second column's document set, and is named because Allianz is the largest German life writer, so its Basisrente wordings are the most consequential documents this corpus could not reach. Every substantive Allianz claim in the product documents is sourced to [S2] instead

(delib-basisrente-s4)=

### S4 — Alte Leipziger Lebensversicherung a. G., **AL_RoyalBasisRente** (Klassik and Fonds)
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB, *Produktinformationsblatt*, *Verbraucherinformation*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing beyond existence.** Named in the variations table of `product-spec.md` as the natural first target for a checker with a working network, because the carrier is repeatedly placed at the top of independent Basisrente ratings [R24]. The product names are [unverified]

(delib-basisrente-s5)=

### S5 — NÜRNBERGER Lebensversicherung AG, **Basis-Rente** with **Berufsunfähigkeits-Zusatzversicherung**
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for the Basisrente main contract and separate AVB for the BUZ rider
- URL: **not established.** The carrier's Schicht-3 wordings were returned in a sibling delib file under a `4allportal` document scheme, so its Basisrente wordings sit in the same scheme; **no Basisrente document id was returned and none is guessed**
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted); the document scheme carried over from `_research/klassische_rentenversicherung.md` [S9]
- Used for: **nothing beyond existence and the document scheme.** It carries the statement in `product-spec.md` that **no carrier's BUZ wording was reached** (gap 18) — the single most valuable document this corpus could not reach, because NÜRNBERGER is one of the market's principal *Berufsunfähigkeit* writers and therefore the natural place to see the 50 % *Beitragsanteil* rule expressed in contractual terms. The model carries that rule as `buz_prem_share < 0.50` and nothing else

(delib-basisrente-s6)=

### S6 — Volkswohl Bund Lebensversicherung a. G., **Basisrente**
- Publisher / doc type: Volkswohl Bund Lebensversicherung a. G., Dortmund; AVB, *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing beyond existence.** Named in the variations table of `product-spec.md` as a broker-channel carrier with a large Basisrente book [R24], the broker channel being where this product is sold

(delib-basisrente-s7)=

### S7 — LV 1871 (Lebensversicherung von 1871 a. G.), Basisrente
- Publisher / doc type: Lebensversicherung von 1871 a. G., München; AVB, *Produktinformationsblatt*, marketed under the names Golden Basic and MeinPlan Basis [unverified]
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: the asset-form row of `product-spec.md` that names a ***fondsgebundene* Basisrente with an open fund and ETF universe and no *Beitragsgarantie***, which is the form the documents argue is the commercial default of the modern Schicht-1 market and the form a checker should verify first. The attribution to this carrier is [unverified], and the claim that the form dominates new business is [unverified] general knowledge unsupported by any figure in the corpus (gap 3)

(delib-basisrente-s8)=

### S8 — Swiss Life Deutschland, Basisrente (**Swiss Life Maximo** family)
- Publisher / doc type: Swiss Life AG, Niederlassung für Deutschland; AVB, *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing beyond existence.** Cited beside [S2] in the asset-form table of `product-spec.md` as a second large broker-channel writer of the hybrid form with a selectable guarantee level. The product name is [unverified]

(delib-basisrente-s9)=

### S9 — Continentale Lebensversicherung AG, Basisrente (**Rente Invest Basis** family)
- Publisher / doc type: Continentale Lebensversicherung AG, Dortmund; AVB, *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing beyond existence.** Named in the variations table of `product-spec.md`; the product name is [unverified]

(delib-basisrente-s10)=

### S10 — Stuttgarter Lebensversicherung a. G., Basisrente
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; AVB, *Produktinformationsblatt*, marketed in *performance-safe* and *index-safe* variants [unverified]
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: the single sentence in `product-spec.md` recording that **a fourth asset form — an index-linked Basisrente — is plausible from one carrier's tariff naming and was not established** (gap 12). If the *index-safe* name is right it would be a bridge to delib product 4 (`indexpolice`). The documents acknowledge the possibility and assert nothing

(delib-basisrente-s11)=

### S11 — The carriers for which nothing whatever was established
- Publisher / doc type: **Debeka**, **R+V**, **HDI**, **Gothaer**, **Zurich Deutscher Herold**, **ERGO**, **AXA**, **Generali / Dialog**, **Barmenia**, **Universa**, **Württembergische**, **Signal Iduna**, **Baloise**, **DEVK**, **Provinzial**, **HUK-Coburg**, **Hannoversche**, **CosmosDirekt** (beyond [S1]), **die Bayerische**, **Condor** — each writes, or has written, a Basisrente and therefore publishes AVB, a *Produktinformationsblatt* and a *Verbraucherinformation* for it
- URL: not established for any of them
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **a statement of coverage rather than a fact.** It carries the sentence in `product-spec.md` that **twenty named German life writers whose Basisrente documents exist were not reached, and not one contributes a single fact** (gap 1), which is what justifies the whole of the composite's parameter set being **[std]**. Naming them with nothing attached is the honest form

(delib-basisrente-s13)=

### S13 — *Produktinformationsblatt* under § 7 AltZertG (the standardised PIB)
- Publisher / doc type: each provider, on a form and a computational method prescribed by law and administered by the **Produktinformationsstelle Altersvorsorge gGmbH (PIA)**, Kaiserslautern; the mandatory pre-sale document for a certified *Basisrentenvertrag*
- URL: not established (there is no single URL: every provider publishes its own, per tariff and per quotation)
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted). **Not one was obtained, for any carrier, at any quotation**
- Used for: the document type a delib reader must understand even though none was opened — it is **quotation-specific**, and it carries the ***Effektivkosten*** (the total charge burden as a single annualised reduction in yield) and a ***Chancen-Risiko-Klasse*** computed by PIA on a common capital-market model. It is the **only public document in the German market that states a Basisrente's total charge burden as a single comparable number**, which is why gap 2 is the most consequential gap in this corpus and why **every charge parameter in `model.md` is [std]** with an argued band rather than a calibration. Its current field list, scenario set and number of risk classes were not established (gap 7)

(delib-basisrente-s14)=

### S14 — *Basisinformationsblatt* (PRIIPs key information document)
- Publisher / doc type: each provider; the PRIIPs KID for an insurance-based investment product
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: the record in `product-spec.md` that the document type **exists for unit-linked and hybrid Basisrenten**, carrying a summary risk indicator, performance scenarios and a cost table with reduction-in-yield figures at several holding periods; and, more importantly, for the disclosure that **how it interacts with the § 7 AltZertG *Produktinformationsblatt* for a certified contract — whether both are required, or one substitutes for the other — was not established** (gap 6). Nothing downstream asserts either arrangement

(delib-basisrente-s15)=

### S15 — Annual statement to the policyholder (*jährliche Information*, § 7a AltZertG)
- Publisher / doc type: each provider; the statutory annual information for a certified contract
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted); the paragraph address is [unverified]
- Used for: one sentence in the regulatory-context section of `product-spec.md`. Its interest for delib is that the statement names, side by side, the state variables a projection model must carry — contributions paid in the year, accumulated value, guaranteed benefit and projected annuity — which is the same list `result_pols()` publishes. **The field list itself was not established**, so nothing rests on its contents

(delib-basisrente-s16)=

### S16 — Consumer, comparison and rating material
- Publisher / doc type: **Finanztip**, **Stiftung Warentest / Finanztest**, the **Verbraucherzentralen**, **Verivox**, **CHECK24**, **Handelsblatt** and the rating houses at [R24]; consumer guides, comparison-portal pages and product ratings — **secondary in every case**, and S-numbered in frlib's convention because they describe the product rather than regulate it
- URL: not established for any of them
- Retrieved: **no** — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing established.** These are the sources that in a normal research session would supply price points, market variation and the buyer profile, and **none was reached**. The entry carries the disclosure in `product-spec.md` that every price point, every market share and every buyer-profile statement there is either [unverified] general knowledge or a **[std]** construction, marked as such at the point of use (gap 3)

---

## Regulatory and actuarial references (product research numbering)

Same retrieval status throughout unless an entry says otherwise: **Retrieved: no — direct HTTP
egress blocked in the build environment; no search corroboration (session search budget
exhausted).** The content of each entry is stated in the product documents' own words, from
general knowledge of German law and practice; **they are pointers to be checked, not readings**,
and every paragraph number, date and figure that rests on them is [unverified].

(delib-basisrente-r1)=

### R1 — EStG § 10 Abs. 1 Nr. 2 Buchst. b — the definition of a Basisrentenvertrag
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: **more than any other instrument in this product.** The five prohibitions — *nicht vererblich*, *nicht übertragbar*, *nicht beleihbar*, *nicht veräußerbar*, *nicht kapitalisierbar* — and therefore the absence of a *Rückkaufswert*, a *Kapitalwahlrecht*, a *Teilkapitalauszahlung*, a policy loan, an assignment and a commutation, which `model.md` publishes as structural absences and `check_no_capital()` asserts; the requirement of a **monthly, lifelong annuity on the taxpayer's own life**, which fixes the payout phase's single shape; the **age floor** (completion of the 62nd year for contracts concluded after 31 December 2011, the 60th for earlier ones, both [unverified]) that model points 1 and 6 sit either side of; the **closed list of permitted survivors** and the rule that everything paid to a survivor is paid as an annuity, which is why `claims_death` is a survivor's single premium and never a lump sum; and the **50 % majority test** on supplementary covers, carried as the invariant `buz_prem_share < 0.50`

(delib-basisrente-r2)=

### R2 — EStG § 10 Abs. 3 — the Höchstbetrag, its knappschaftliche peg, and the employee reductions
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the single annual *Höchstbetrag* shared with the compulsory schemes of letter a, doubled on joint assessment, and its peg since 2015 to the maximum contribution to the *knappschaftliche Rentenversicherung*; the 2023–2026 ceiling series in `product-spec.md`, **every figure [unverified]** and reproducible only from its own inputs (gap 11); the two employee mechanisms — the GRV contributions consuming the ceiling and the tax-free employer share being subtracted afterwards — and the third reduction for taxpayers with a non-contributory entitlement; and the argument that runs through the whole premium design, that **the ceiling moves every year so the premium should too**, which is why the model carries a *Beitragsdynamik* and a *Zuzahlung* rather than a level premium. Model point 9 sits at the 2026 ceiling

(delib-basisrente-r3)=

### R3 — EStG § 10 Abs. 2 and Abs. 2a — certification and data transmission as conditions of relief
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the statement in `product-spec.md` that the *Sonderausgabenabzug* is conditional on certification under the AltZertG and on electronic transmission of the contribution data, so that an uncertified contract, however economically identical, gets **no relief at all** — which is what makes the prohibitions bind the insurer's product design rather than merely the policyholder's rights. The paragraph addresses are [unverified]

(delib-basisrente-r4)=

### R4 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. aa — the Besteuerungsanteil
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the payout-side rule of the layer — benefits taxed on a percentage fixed by the **calendar year of *Rentenbeginn*** (the *Kohortenprinzip*), with the cohort schedule and its 2058 endpoint set out in `product-spec.md` and **every individual percentage [unverified]**; the fact that ***der Rentenfreibetrag ist ein Euro-Betrag***, frozen in the first full year of receipt, so every later increase in the annuity is fully taxable and the choice of payout-phase *Überschussverwendung* has a tax dimension it lacks in Schicht 3; and the taxation of a *BU-Rente* from a *Basisrentenvertrag* on the same cohort basis (gap 16). **No delib model computes tax**: this instrument explains the economics and justifies the model point, and reaches no cash flow

(delib-basisrente-r5)=

### R5 — Alterseinkünftegesetz (AltEinkG), 2004
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; enabling statute
- URL: not established. **No Bundesgesetzblatt citation is given, because none could be confirmed** (gap 23)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the opening of the regulatory-context section of `product-spec.md` — the statute effective **1 January 2005** that built the three-layer architecture, introduced *nachgelagerte Besteuerung* for the first layer and created the Basisrente so that the self-employed would have a vehicle with the statutory scheme's tax treatment, following the report of the commission chaired by **Bert Rürup**, from which the market name. The *Bundesverfassungsgericht* decision it responded to is [unverified] as to year and case

(delib-basisrente-r6)=

### R6 — Wachstumschancengesetz (2024) — the half-point step and the 2058 endpoint
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the amendment that cut the annual step in the *Besteuerungsanteil* from one percentage point to **half a point** with retrospective effect for the **2023** cohort — which is why 2023 is 82,5 % and not 83 % — and moved the 100 % year from **2040 to 2058**. `product-spec.md` uses it, with [R7] and [R19], to frame the transition as **a slowing, not a change of principle**. The instrument's name and date are [unverified]; the arithmetic of the schedule is its only corroboration

(delib-basisrente-r7)=

### R7 — Jahressteuergesetz 2022 — the full Sonderausgabenabzug from 2023
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the rule that **100 % of the capped contribution is deductible from the assessment period 2023**, brought forward from 2025, with 94 % in 2021 and 96 % in 2022 [unverified]. It is a genuine simplification of the specification: for any model point written at 2023 or later no phase-in factor is needed, so `product-spec.md` carries the current rule and a note that pre-2023 cohorts differ

(delib-basisrente-r8)=

### R8 — Jahressteuergesetz 2007 — the age floor from 60 to 62
- Publisher / doc type: Deutscher Bundestag / Bundesgesetzblatt; amending statute
- URL: not established; no Bundesgesetzblatt citation (gap 23)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the **60/62 split at the end of 2011**, which is a model-point attribute rather than a formula: `conclusion_year` fixes which floor applies, and model point 6 is a 2009 contract converting at 60 while every new-business point converts at 67. Both figures are [unverified]. The entry also carries the resolution recorded at gap 22 — the commissioning brief said 63, the research file resolved it against 60, and no downstream document repeats the 63

(delib-basisrente-r9)=

### R9 — AltZertG § 5a — certification of Basisrentenverträge
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/altzertg/__5a.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: certification by the **Bundeszentralamt für Steuern** as a formal conformity check and a condition of the relief, required from 1 January 2010 [unverified]; and — the load-bearing part — that **§ 5a does not import the Riester *Beitragserhaltungsgarantie***, which is why a Basisrente may be sold with a full guarantee, a partial one or none at all, and why the two subsidised layers diverged after the interest-rate collapse. That omission is the sharpest structural contrast in `product-spec.md`'s asset-form section, and it is the reason `Riester_DE_A` and `Basis_DE_A` are different models rather than one with a switch

(delib-basisrente-r10)=

### R10 — AltZertG § 1 and § 2 Abs. 2 — what certification is, and the guarantee it does not extend
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/altzertg/__1.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the Riester conditions § 5a does **not** pick up — above all the *Beitragserhaltungsgarantie* — and the five-year spreading of acquisition and distribution costs, **whether that reaches *Basisrentenverträge* being unresolved** (gap 8), which is why `zill_spread_y = 5` is **[std]** rather than cited; and for the statement, repeated in every delib document that mentions certification, that **certification is expressly not a seal of quality**: it says nothing about charges, investment quality or the provider's strength

(delib-basisrente-r11)=

### R11 — AltZertG § 7 and the *Produktinformationsstelle Altersvorsorge*
- Publisher / doc type: Bundesministerium der Justiz / juris; Produktinformationsstelle Altersvorsorge gGmbH (PIA), Kaiserslautern; statutory provision and the body administering it
- URL: `https://www.gesetze-im-internet.de/altzertg/__7.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the pre-sale information regime behind [S13] — the standardised *Produktinformationsblatt*, the ***Effektivkosten*** the provider computes and the ***Chancen-Risiko-Klasse*** PIA computes on a common capital-market model. `product-spec.md` states plainly that **delib does not implement the PIA simulation**, and the entry carries the disclosure that a comparable total-charge figure for this product exists and is public per quotation, and that delib could not obtain one (gap 2, gap 7)

(delib-basisrente-r12)=

### R12 — ZPO § 851c — Pfändungsschutz bei Altersrenten
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/zpo/__851c.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the third leg of the product in `product-spec.md`, beside the relief and the prohibitions — the four conditions of Abs. 1 (periodic and lifelong, not before a stated age, not disposable, no third-party beneficiaries other than survivors, no capital payment other than on death), which are the **same four features § 10 demands**; and the protection of the accumulated fund on an age-graduated annual allowance subject to an aggregate ceiling. Two cautions the documents carry from this entry: **the § 851c age is 60, not 62** (gap 10), and **the annual bands are not reproduced anywhere in delib** because no source could confirm them (gap 9). The protection is a **by-product of the prohibitions**, and it is the principal non-tax reason a self-employed person buys the product

(delib-basisrente-r13)=

### R13 — ZPO § 851d, SGB II § 12, SGB XII § 90 — insolvency and means-testing
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the surrounding protection — old-age provision whose realisation is contractually excluded being exempt from the means test — which with [R12] is the market's *insolvenzfest* and *Hartz-IV-fest* claim; and, in the tax section, the social-insurance treatment of the annuity in payment, where the difference between a compulsorily and a voluntarily insured pensioner is of the order of 18 % of the annuity (gap 21). **All three paragraph addresses are [unverified]** and the precise conditions were not established; the direction is not in doubt

(delib-basisrente-r14)=

### R14 — VVG § 165 (Beitragsfreistellung), § 168 (Kündigung), § 169 (Rückkaufswert)
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html`, `.../__168.html`, `.../__169.html` — canonical forms, [unverified]
- Retrieved: **no** — egress blocked. §§ 165 and 169 were established at a higher level of detail in the sibling delib research files `_research/kapitallebensversicherung.md` and `_research/klassische_rentenversicherung.md`, which corroborated them by search while search was still available; no search corroboration in this product's research
- Used for: the exits, and what becomes of them here. **§ 165 survives intact** and is the product's only behavioural exit, which is the whole of `bf_rate`, `pols_paidup` and the premium-free account block — and the reason `model.md` insists a freeze is a transfer between ledgers rather than a decrement. **§ 168's termination right survives but has nothing to pay out**, so a purported *Kündigung* operates as a *Beitragsfreistellung*. **§ 169 is inoperative**: there is a *Deckungskapital* and no duration at which any part of it is payable as capital, which is why the model has no surrender cells, no *Stornoabzug* and no floor under `prem_to_av_pp`. How individual AVB word the first two is [unverified]; the outcomes are settled

(delib-basisrente-r15)=

### R15 — VVG § 153 — Überschussbeteiligung
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — canonical form; established by search in the sibling delib research file `_research/kapitallebensversicherung.md`
- Retrieved: **no** — egress blocked; identity carried over from that sibling file, which corroborated it by search
- Used for: the policyholder's statutory entitlement to a share of the *Überschuss* and of the *Bewertungsreserven*, which a Basisrente holds **on exactly the same terms as any other German life contract** — the layer changes the tax and the exits, not the surplus machinery. Two consequences the product documents draw from it: the *Überschussverwendung* options are narrower in the *Aufschubphase*, because cash-paying systems sit awkwardly with *nicht kapitalisierbar* (an inference, not a sourced fact, gap 17); and the ***Schlussüberschussanteil* has no early-exit trigger**, so it is allocated **only at *Rentenbeginn***, which is the single-date `terminal_bonus_rate` in `fund_at_conv()` and a cleaner cash flow than anywhere else in delib

(delib-basisrente-r16)=

### R16 — Deckungsrückstellungsverordnung (DeckRV) — Höchstrechnungszins and Höchstzillmersatz
- Publisher / doc type: Bundesministerium der Justiz / juris, with amendment by the Bundesministerium der Finanzen; regulation
- URL: **not established.** No delib session established a `gesetze-im-internet.de` address for the DeckRV and none is guessed
- Retrieved: **no** — egress blocked; content carried over from `_research/klassische_rentenversicherung.md`, where it was corroborated across five independent search results
- Used for: the two numbers in this model that are **not** standardizations. The ***Höchstrechnungszins*** rose from 0,25 % to **1,00 %** with effect from 1 January 2025 and is recommended at 1,00 % for 2026, and it **applies at conclusion and stays with the contract**, which is the `gtd_rate` column and the guarantee-vintage ladder that model points 6, 7 and 8 exercise. The ***Höchstzillmersatz*** caps acquisition costs written into the reserve at **25 ‰ of the *Beitragssumme***, reduced from 40 ‰ by the LVRG in 2015 [unverified], which is `zill_rate` and the two shipped tariffs. The full vintage ladder is [unverified] in delib except for the 0,25 % and the 1,00 %

(delib-basisrente-r17)=

### R17 — DAV 2004 R — the annuity table
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; actuarial table and its derivation guideline
- URL: **not established**; the DAV's own host refuses this build environment
- Retrieved: **no** — egress blocked; content carried over from `_research/klassische_rentenversicherung.md`, where it was corroborated by search
- Used for: the mortality basis of the whole product. That DAV 2004 R is a ***Generationentafel*** — the improvement inside the table rather than applied on top — is why `mort_rate_at_age` takes a calendar year and why `cal_year(t)` is carried; that **first-order probabilities carry prudential margins and price the guaranteed *Rentenfaktor*** while second order is the best estimate is the wedge `mort_be_factor` and `ann_bonus_rate` sit either side of; and the conversion rule `max(garantiert, aktuell)` and the one quantified conversion basis in the corpus (DAV 2004 R at 0 % p.a., a Schicht-3 observation, [unverified] here) stand behind `rentenfaktor_applied()`. **The table is not public and delib does not redistribute it**: `mort_table.csv` is a **[std]** proxy anchored at `qx(67) = 0.014000`, and the entry carries what a replacement must preserve. It also carries the [std] view that a non-surrenderable annuity should select *lighter* than a Schicht-3 portfolio, for which **no evidence was found**

(delib-basisrente-r18)=

### R18 — BMF-Schreiben on Vorsorgeaufwendungen and Altersbezüge
- Publisher / doc type: Bundesministerium der Finanzen; consolidated administrative circular
- URL: **not established. No BMF file number is given, because none could be confirmed** (gap 23)
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the disclosure of what could **not** be established. The circular is where the operational detail lives that the statute does not spell out — how the 50 % majority test is computed, what happens on a change of provider, how the *Rentenfreibetrag* is fixed, and what administrative tolerance exists for a very small annuity. **Not one of those points was established**, which is why `product-spec.md` says a provider transfer **must not be asserted** (gap 13) and why the question whether a trivially small annuity may be paid less often than monthly is left open (gap 19). It is the single most valuable document a checker with a working network should retrieve after the statute itself

(delib-basisrente-r19)=

### R19 — BFH, 19 May 2021 — the Doppelbesteuerung judgments
- Publisher / doc type: Bundesfinanzhof; two decisions of the same day, commonly cited as X R 33/19 and X R 20/19, **both file numbers [unverified]**
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the framing of the tax section in `product-spec.md`. The court accepted **in principle** that double taxation is unconstitutional where contributions were made from taxed income and benefits taxed again, found none on the facts, and identified the transition schedule as capable of producing one for later cohorts — **particularly for self-employed taxpayers whose phase-in contributions were only partly deductible**, precisely this product's own buyer. The legislative response was [R7] and [R6]. The case numbers, the date and the method are [unverified]; the causal story is the correct framing and is what the documents use it for

(delib-basisrente-r20)=

### R20 — Sozialversicherungsrechengrößen-Verordnung — the BBG series
- Publisher / doc type: Bundesministerium für Arbeit und Soziales, with the consent of the Bundesrat; annual regulation
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: the inputs to the *Höchstbetrag* arithmetic at [R2] — the *Beitragsbemessungsgrenzen* and contribution rates set each autumn for the following calendar year, uniform across the former East and West from 2025 [unverified]. Its real weight in these documents is a warning: **this instrument has to be re-read every year for this product in a way that is not true of any other delib product**, which is why the *Höchstbetrag* appears in the "living texts" paragraph of `product-spec.md` and in the model risks of `technical-notes.md`, and why every figure in the ceiling series is [unverified] (gap 11)

(delib-basisrente-r21)=

### R21 — BaFin — Wohlverhaltensaufsicht and value for money
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; supervisory *Merkblatt*, thematic publications and articles
- URL: **not established**; the host refuses this build environment
- Retrieved: **no** — egress blocked; the supervisory material carried over from `_research/kapitallebensversicherung.md`, where it concerned the endowment chassis rather than this layer
- Used for: the single statement in `product-spec.md` that **a Basisrente is squarely inside the conduct-supervision perimeter** for capital-forming life products sold through commissioned intermediaries, the *Effektivkosten* on the § 7 AltZertG *Produktinformationsblatt* being the number that supervision runs on — and for the disclosure that **nothing Basisrente-specific was established from BaFin** (gap 15)

(delib-basisrente-r22)=

### R22 — GDV and BMF statistics on the Basisrente stock and new business
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft; Bundesministerium der Finanzen; annual statistics
- URL: not established
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: **nothing quantitative, which is the point.** The entry carries the disclosure in `product-spec.md` that **no market statistic of any kind was established** — contract stock, new business, average contribution, the *klassisch*/*fondsgebunden* split and the distribution-channel split are all [unverified] general knowledge given as orders of magnitude — and the instruction that **nothing downstream may cite a delib figure for the size of the Basisrente market** (gap 3)

(delib-basisrente-r23)=

### R23 — EStG § 93 Abs. 3 — the Kleinbetragsrente, and its reach into Schicht 1
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__93.html` — canonical form, [unverified]
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: **the de-minimis exception to the *Kapitalisierungsverbot*.** Riester permits commutation of a *Kleinbetragsrente* at the start of the payout phase, at a threshold expressed as a percentage of the monthly *Bezugsgröße* of § 18 SGB IV — 1 % against a competing 1,5 %, both [unverified]. **Schicht 1 is not excluded from it**: § 10 Abs. 1 Nr. 2 Satz 3 EStG makes an *Abfindung* on the § 93 Abs. 3 Satz 2 and 3 mechanics harmless to a *Basisrentenvertrag*'s Schicht-1 status [R1] [REG-R42] [unverified]. **An earlier drafting of this product recorded the opposite — that Schicht 1 admitted no de-minimis exception whatever — and that reading is withdrawn**; [REG-R42] had the correct position throughout. The modelling consequence is now a **[std]** decision rather than a deduction from the statute: `Basis_DE_A` does not implement the commutation branch, because the threshold level is contested, no carrier's AVB was reached to establish whether an *Abfindung* is offered at all (gap 19), and `Riester_DE_A` already carries the mechanic. What the test module asserts is that decision — model point 10, at 300,00 € a year, projects a small annuity and no lump sum — and the unimplemented branch is a named model risk

(delib-basisrente-r24)=

### R24 — Independent rating and market-analysis houses
- Publisher / doc type: **Institut für Vorsorge und Finanzplanung (IVFP)**, Altenstadt; **Franke und Bornberg**, Hannover; **Morgen & Morgen**, Hofheim; **Assekurata**, Köln; comparative product ratings and market studies
- URL: not established for any of them
- Retrieved: no — egress blocked; no search corroboration (budget exhausted)
- Used for: naming, in the variations section of `product-spec.md`, the four houses a checker should go to for comparative analysis in this layer — the IVFP publishing the best-known Basisrente rating — and for the disclosure that **not one rating, score, ranking or figure was established**, so no downstream document may invent one. The two carriers described as highly rated or broker-strong ([S4], [S6]) rest on this entry and are [unverified]

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R1–R56 numbering, frozen; research
provenance in `_research/regulatory-actuarial.md`). **Every entry on that page records
`Fetched: no`** for the reason given above, and the ones marked there as search-corroborated
were corroborated by a *search-result summary*, never by a retrieved document. Entries cited by
the Basisrente documents:

- **REG-R1** — Directive 2009/138/EG (Solvabilität II): the framework the undiscounted cash flows feed, cited and never computed.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: why no contract-boundary rule, cost-of-capital rate or standard-formula shock in this library rests on a retrieved text.
- **REG-R4** — EIOPA risk-free term structures: the curves a best estimate would discount `liability_cf` on.
- **REG-R5** — VAG 2016 and its *Sparten*: the undertaking writing this contract is a Solvency II life insurer.
- **REG-R6** — VAG §§ 74–110 and § 40: best estimate plus risk margin, and the SFCR — the valuation layer that consumes these cash flows.
- **REG-R7** — VAG §§ 124/125: the *Sicherungsvermögen* the *klassisch* form's assets sit in, and the record that the AnlV quotas no longer bind this insurer.
- **REG-R8** — VAG § 138: premium adequacy, the rule that makes the *Höchstrechnungszins* a pricing cap and not merely a reserving one.
- **REG-R9** — VAG § 139: the *Überschussbeteiligung* and the *Sicherungsbedarf* test on *Bewertungsreserven* — why making the declared rate endogenous would need the insurer's whole HGB result.
- **REG-R10** — VAG §§ 140/145: the *RfB* the declared surplus is drawn from.
- **REG-R14** — DeckRV and its § 2: the *Höchstrechnungszins* as the statutory ceiling on `gtd_rate`.
- **REG-R15** — the *Höchstrechnungszins* rate history: the guarantee-vintage ladder from 2,75 % down to 0,25 % and back to 1,00 %, which is what makes an in-force model point carry its cohort's rate rather than today's.
- **REG-R16** — DeckRV § 4: the *Höchstzillmersätze*, 25 ‰ and the pre-2015 40 ‰ — the two shipped tariffs.
- **REG-R17** — DeckRV § 5 Abs. 3: the *Referenzzins* and the *Zinszusatzreserve*, an HGB reserve that bites hardest on exactly this business and that delib does not compute.
- **REG-R18** — MindZV: the 90 / 90 / 50 minimum allocation under the declared rate this model takes as a scenario.
- **REG-R19** — RfBV: the collective part of the *RfB*, behind the same scenario.
- **REG-R20** — LVRG 2014: the reduction of the *Zillmersatz* to 25 ‰ and the wider cost reform.
- **REG-R22** — VVG 2008 and § 171: the contract law that governs throughout, and the *halbzwingend* character of the provisions the product turns on.
- **REG-R23** — VVG §§ 8 and 152: the 30-day *Widerruf*, which applies here as to any German life contract and is not modelled.
- **REG-R24** — VVG § 153: the statutory *Überschussbeteiligung* and the half-share in the *Bewertungsreserven*, beside [R15].
- **REG-R25** — VVG §§ 154/155: the *Modellrechnung* and the *Standmitteilung*, the disclosure counterpart of [S15].
- **REG-R27** — VVG § 163: the premium- and benefit-adjustment channel, recorded as a model risk on the guaranteed *Rentenfaktor* and not implemented.
- **REG-R28** — VVG §§ 165–170: the *prämienfreie Versicherung*, the *Kündigung*, the *Rückkaufswert* and the *Stornoabzug* — the last two inoperative here, which is the product's defining absence.
- **REG-R29** — VVG §§ 172–177: the *Berufsunfähigkeitsversicherung* chapter a BUZ is written under; its mechanics belong to `BU_DE_S`.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: misstatement, payment default and the age-error rule, which apply unchanged and are not modelled.
- **REG-R31** — VVG §§ 6, 7 and 214 with the VVG-InfoV: the product-level cost-disclosure regime the § 7 AltZertG *Effektivkosten* sits on top of.
- **REG-R32** — PRIIPs: the regime behind the *Basisinformationsblatt* at [S14], reaching the unit-linked and hybrid forms.
- **REG-R33** — IDD and § 34d GewO: the distribution regime this product depends on, which is predominantly brokered.
- **REG-R34** — Unisex (EuGH C-236/09, AGG): why `sex` is a reporting-only model point column and may not enter pricing for contracts concluded from 21 December 2012.
- **REG-R35** — BaFin Merkblatt 01/2023 (VA): *angemessener Kundennutzen*, the conduct perimeter this product sits in, beside [R21].
- **REG-R36** — the BGH line of authority: the narrowing of the *Treuhänderklausel*, recorded as a model risk on the guaranteed *Rentenfaktor*.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the layer architecture, beside [R5].
- **REG-R39** — **EStG § 10 Abs. 1 Nr. 2 Buchst. b and Abs. 3**: the cross-product entry for the five prohibitions and the ceiling, and the **best-corroborated fact in the tax section** because [REG-R40] reaches the same product shape from a different statute in a different research sweep. It is the entry that says in terms that a Basisrente model offering only a level regular premium models the wrong product.
- **REG-R40** — ZPO §§ 850b and 851c: the *Pfändungsschutz* conditions, the **340 000 € aggregate ceiling** [unverified], and the record that the annual savings bands are **contradicted across summaries** — which is why no delib document prints one.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Besteuerungsanteil*, the *Rentenfreibetrag* and the *Ertragsanteil* comparator, beside [R4].
- **REG-R42** — EStG § 10a and Abschnitt XI (§§ 79–99): cited here for one thing only — its record that the *Kleinbetragsrenten-Abfindung* of § 93 Abs. 3 is available **for Riester and Basisrente alike**, and that both products need a commutation test at annuitisation. It is the entry that corrects this product's earlier reading, beside [R23]; the Riester subsidy machinery itself belongs to `Riester_DE_A`.
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the PIA: certification, the *Produktinformationsblatt* and the CRK scale, beside [R9] and [R11].
- **REG-R44** — the Altersvorsorgereformgesetz 2026: the reform that closes Riester to new business from 1 January 2027 and **leaves the Basisrente untouched** — the one piece of forward-looking context in `product-spec.md`.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag* and the 12/62 rule — Schicht-3 mechanics that **reach a Basisrente at no point in its life**.
- **REG-R46** — ErbStG and SGB V §§ 226, 229, 240: the social-insurance treatment of an annuity in payment (gap 21), stated as a driver of the after-tax comparison and not asserted.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV's ownership of the tables: the first-order/second-order distinction the conversion wedge is built on, and the reason no DAV table ships.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity bases, beside [R17], and what a replacement for `mort_table.csv` must preserve.
- **REG-R50** — DAV 1997 I / RI / TI: the *Berufsunfähigkeit* decrement family a BUZ would need, which lives in `BU_DE_S`.
- **REG-R52** — Destatis: the only freely reusable German mortality series, the intended base for a user-supplied replacement table.
- **REG-R53** — the German life market in numbers: named beside [R24] as where comparative figures would come from, and from which **none was obtained for this product**.
- **REG-R54** — HGB §§ 341–341o and the RechVersV: the statutory *Deckungsrückstellung* the model's `av_at` and annuity obligation stand behind, and which delib does not compute.
- **REG-R55** — IFRS 17: a profit-participating Basisrente is a direct-participating contract measured under the variable fee approach; nothing here implements it.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional practice the 1,00 % for 2026 rests on.

---

## Provenance note

Extraction details — one entry per source with an extended content block, the twenty-two
mechanic sections, and the twenty-five-item gaps-and-caveats register — live in
`_research/basisrente.md`. That file is the citation ground truth for the S# and R# numbering
used here, and it was written with **no research channel of any kind**: egress was blocked and
the session's search budget was already exhausted when this product was reached. Two sibling
delib research files, written while search was still available, supplied [S1], [S2] and the
carried-over material in [R14] through [R17] and [R21]; everything else rests on general
knowledge, disciplined by the tagging rules above and by that register.

The caveats that most affect what these product documents can claim are: **not one carrier's
Basisrente contract terms were established** (gap 1), so the variations table is a record of
absence rather than of variation and every parameter that would normally be sourced to a carrier
is **[std]**; **no *Effektivkosten* figure and no charge schedule was obtained** (gap 2), the
§ 7 AltZertG *Produktinformationsblatt* existing precisely to publish one; **no market statistic
of any kind was established** (gap 3), so no delib figure for the size of this market may be
cited; **no *Rentenfaktor* level, range or time series exists anywhere in the delib corpus**
(gap 4), for this or any product, which makes the model's single largest lever a **[std]**
choice; **the *Höchstbetrag* series is arithmetic, not evidence** (gap 11), the 2026 line least
securely of all; **the § 851c ZPO protected amounts are deliberately not reproduced** (gap 9),
because the practitioner ladders are contradicted across summaries; **the § 851c age condition
(60) and the § 10 EStG floor (62) are different provisions** and must not be merged (gap 10);
**whether a Basisrentenvertrag may be transferred to another provider was not resolved**
(gap 13), so nothing downstream asserts it; and **no *Bundesgesetzblatt* citation and no BMF
file number appears anywhere** (gap 23), because none could be confirmed and none was guessed.

Two items are living texts and move on their own schedule (gap 24): the *Höchstbetrag* changes
every year with the *Sozialversicherungsrechengrößen-Verordnung* [R20], and the
*Besteuerungsanteil* changes every year by construction [R4] [R6]. Check both, and every
paragraph number in these documents, before relying on anything here.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-basisrente-r1
[R11]: #delib-basisrente-r11
[R12]: #delib-basisrente-r12
[R14]: #delib-basisrente-r14
[R15]: #delib-basisrente-r15
[R17]: #delib-basisrente-r17
[R19]: #delib-basisrente-r19
[R2]: #delib-basisrente-r2
[R20]: #delib-basisrente-r20
[R21]: #delib-basisrente-r21
[R24]: #delib-basisrente-r24
[R4]: #delib-basisrente-r4
[R5]: #delib-basisrente-r5
[R6]: #delib-basisrente-r6
[R7]: #delib-basisrente-r7
[R9]: #delib-basisrente-r9
[REG-R40]: #delib-reg-r40
[REG-R42]: #delib-reg-r42
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
