# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/pflegerentenversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps. **S3** (GDV *Musterbedingungen* for life-assurance products)
is absent because the research file could not establish that the GDV publishes a model condition
for the *Pflegerentenversicherung* at all, and no benefit, premium, surrender or paid-up rule
anywhere in `product-spec.md` or `technical-notes.md` is attributed to it — citing it would
attribute a claim to a document that may not exist. **S6** (*Basisinformationsblatt* / PRIIP-KID)
is absent because the PRIIPs perimeter question the research file raises there is carried in the
product documents from the cross-product entry [REG-R32], which states the Regulation at article
level, rather than from a document class of which not one instance was located; the research
file's own `[R25]` pointer inside that entry is likewise not part of the frozen `R1..R24` range
and appears nowhere here. **S15** (*Pflege-Bahr* tariff conditions of a *geförderter Tarif*) is
absent because every *Pflege-Bahr* parameter the documents print — the 10 / 20 / 30 / 40 / 100 %
grid, the *Zulage*, the five-year *Wartezeit* — is cited to the statute [R8] and not to a
carrier's tariff conditions, none of which was located. **R17** (BaFin supervisory material on
life and LTC business) is absent because **nothing product-specific to *Pflegerentenversicherung*
was located at BaFin**, so no BaFin statement of any kind is cited; the supervisor enters the
product documents only through the cross-product entry [REG-R35]. Access date for
all sources: **2026-08-29**. No sources were newly added at drafting. Cross-product [REG-R#] tags
are listed in their own section at the end.

**Retrieval conditions, stated plainly.** Two independent limits applied while this library was
built, and this product was reached after both had bitten. This is the one product in `delib`
for which **neither** research channel was available.

1. **Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl` are refused with HTTP 403 at the egress gateway for every host outside a short package-registry allowlist. Every host that would have supplied a document for this product was tried and refused: `gesetze-im-internet.de` (SGB XI, VVG, VAG, EStG, SGB XII, DeckRV, KVAV), `bafin.de`, `gdv.de`, `aktuar.de` (the DAV 2008 P derivation), `pkv.de` (the PKV-Verband statistics and the MB/EPV), `destatis.de` (the *Pflegestatistik*), `bundesgesundheitsministerium.de`, `vdek.com` (the *Eigenanteil* series) and `de.wikipedia.org`. **No document cited anywhere in this file was retrieved** — not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not one statutory text, not one DAV paper and not one statistical release.
2. **The session's `WebSearch` budget — 200 calls, shared across the whole `delib` build — was exhausted before this product was started.** Every query attempted for `pflegerentenversicherung` returned the budget-exhausted message. **This product therefore had no research channel at all**: the research file was written from the author's own knowledge of German insurance law and German actuarial practice, under the discipline the house brief imposes for exactly that case.

What follows, and it governs every entry below:

- **A delib citation is a pointer, not a certificate.** `[R2]` beside a statement about § 15 SGB XI means *this is the instrument the statement should be checked against*. It does **not** assert that anyone checked it. Every `Retrieved` line says `no`, and none says otherwise.
- **Every entry is a *known reference*** — a document that exists and is the right kind of document for this product — with a publisher, a document type, `URL: not established` unless the canonical form is one this author is confident of, and both reasons on the `Retrieved` line. **No entry asserts an edition, a document number, a *Bundesgesetzblatt* citation, a page count or a publication date**, because none was checked.
- **Nothing in this chain is quoted.** There is not one German sentence in quotation marks attributed to a statute or to a *Bedingungswerk* anywhere in this product's documents; statutory rules are described in English, in the author's own words, as *what the instrument provides*.
- **`[unverified]` is used generously** in the product documents: every paragraph number, effective date, amount, percentage, threshold and market figure carries it unless it is a structural fact not in dispute.
- **Uncertain levels became `[std]` parameters rather than citations.** Every biometric rate, every charge, every lapse rate, the *Leistungsstaffel* levels, the *Stornoabzug* and the premium itself are **[std]**, each listed with its rationale in `model.md`. A `[std]` number is honest about being a construction; a fabricated `[S9]` premium would not be, and there is none.

---

## Primary product sources

(delib-pflegerentenversicherung-s1)=

### S1 — PKV-Verband, *Musterbedingungen für die private Pflegepflichtversicherung* (MB/PPV)
- Publisher / doc type: Verband der Privaten Krankenversicherung e. V. (PKV-Verband), Köln; *Musterbedingungen* — model conditions for the compulsory private LTC cover of § 23 SGB XI, adopted with variations by every private health insurer.
- URL: not established (`pkv.de` refused the fetch).
- Retrieved: **no** — direct HTTP egress blocked in the build environment; **no search corroboration** (session search budget exhausted).
- Used for: the one structural fact that matters to a *Pflegerente* — **private top-up wordings define their own trigger by reference to the *Pflegegrad* established under SGB XI or the MB/PPV rather than by writing an independent medical definition**, which is what ties the private product's incidence experience to the statutory assessment regime and to every future change in it. It is the document in which the private sector's rendering of *Pflegebedürftigkeit* and of the five *Pflegegrade* is written down. No edition designation is asserted.

(delib-pflegerentenversicherung-s2)=

### S2 — PKV-Verband, *Musterbedingungen für die ergänzende Pflegekrankenversicherung* (MB/EPV)
- Publisher / doc type: PKV-Verband; *Musterbedingungen* for the **top-up** LTC cover written as *private Krankenversicherung* — the *Pflegetagegeld* and *Pflegekosten* forms.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the contrast document of the whole product specification.** A *Pflegetagegeld* written on MB/EPV lines is a **health-insurance** contract: it is supervised under the health rules, it may carry a *Beitragsanpassung* clause under § 203 VVG [R11], and where it is written *nach Art der Lebensversicherung* its ageing provision is an *Alterungsrückstellung* under § 146 VAG and the KVAV [R12] [R14]. A *Pflegerente* on the same risk is a **life** contract with a *Deckungsrückstellung* and no ordinary re-rating power. The product specification's competing-forms section and its "why the *Pflegerente* costs more" argument reduce to that difference.

(delib-pflegerentenversicherung-s4)=

### S4 — *Allgemeine Bedingungen für die Pflegerentenversicherung* (AVB), as a document class
- Publisher / doc type: an individual German *Lebensversicherer* — **no carrier's wording was located**; *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for a *Pflegerenten* tariff, typically bundled with *Tarifbedingungen* and delivered with the *Versicherungsschein*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the most-cited entry in this product, and the one whose limits must be read carefully.** It carries the *clause inventory* that the representative specification follows — the *vereinbarte Pflegerente* and the *Leistungsstaffel*; the trigger clause and its fallback assessment by a physician the insurer appoints; the *Wartezeit* and *Karenzzeit* clauses; the *Beitragsbefreiung im Leistungsfall*; the *Nachprüfung* and the consequences of a *Herabstufung*, including the revival of the premium; the death-benefit, indexation, surrender and paid-up clauses; the § 19 VVG disclosure and exclusion clauses; and the territorial clause. It is cited as a **document-class description** and never as a reading of any instance: **no page count, no edition date, no clause number and no parameter for any carrier's wording is asserted anywhere**, and every level the class would have supplied is **[std]** instead.

(delib-pflegerentenversicherung-s5)=

### S5 — *Produktinformationsblatt* (PIB) / *Informationsblatt zu Versicherungsprodukten* (IPID)
- Publisher / doc type: an individual German *Lebensversicherer*; the short pre-contractual product summary. The German market uses both the national *Produktinformationsblatt* and the EU IDD *Insurance Product Information Document* [REG-R31] [REG-R33]; which applies to this product is `[unverified]`.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **nothing substantive — the entry exists to record an absence.** This is the document class that would have supplied, on one or two pages, exactly the parameters the delib documents had to standardise: the entry-age band, the *vereinbarte Rente* band, the *Leistungsstaffel*, the *Wartezeit*, the *Karenzzeit*, a specimen premium and the charges. **Not one instance was located**, and the product specification cites S5 only where it says so.

(delib-pflegerentenversicherung-s7)=

### S7 — *Verbraucherinformationen* / *Vertragsinformationen* under the VVG-InfoV
- Publisher / doc type: an individual German *Lebensversicherer*; the pre-contractual information package required by § 7 VVG and the VVG-InfoV [R11] [REG-R31].
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **disclosure obligation** the product specification records — that *Abschluss- und Vertriebskosten* and *Verwaltungskosten* must be disclosed in euro amounts in the pre-contractual package for a life product, the euro disclosure being the operative one for a biometric-risk contract that carries no *Effektivkosten* figure. And, as with S5, for the absence: **no instance was located, so every charge level in delib is `[std]`.**

(delib-pflegerentenversicherung-s8)=

### S8 — *Jährliche Mitteilung zum Stand Ihrer Versicherung* (Standmitteilung)
- Publisher / doc type: an individual German *Lebensversicherer*; the annual statement owed to the policyholder under § 155 VVG [R11] [REG-R25] `[unverified]`.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: one point in the valuation-and-disclosure section — that the annual statement reports the guaranteed benefit, the accumulated *Überschussbeteiligung*, the current *Rückkaufswert* and the current *beitragsfreie* benefit side by side, and that on a *Pflegerente* the guaranteed benefit is the ***vereinbarte Pflegerente* at the top *Pflegegrad*, not a sum insured**. The field list is `[unverified]`; no instance was located.

(delib-pflegerentenversicherung-s9)=

### S9 — *Tarifblatt* / *Beitragstabelle* for a *Pflegerenten* tariff
- Publisher / doc type: an individual German *Lebensversicherer*; the rate card — premium per unit of *vereinbarte Rente*, by entry age, sex, *Beitragszahlungsdauer* and option set.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the single most consequential absence in this product, recorded rather than papered over.** No German insurer publishes a *Pflegerenten* rate card on the evidence available to this corpus, and none was located. This is the difference between this product and frlib's `temporaire_deces`, where one carrier's complete attained-age grid was read off a retrieved PDF and became the reference implementation's premium basis. **`Pflege_DE_S` has no published premium to reproduce**: its *Beitrag* is struck by equivalence on stated `[std]` first-order bases and is sanity-checked against an argued band, never against a citation.

(delib-pflegerentenversicherung-s10)=

### S10 — Stiftung Warentest / *Finanztest*, comparative tests of *Pflegezusatzversicherung*
- Publisher / doc type: Stiftung Warentest — **secondary**, not a product document; comparative product test with a scored ranking and a price table.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two **structural** statements in the market section, neither numeric: that the public comparative tests concentrate on ***Pflegetagegeld***, because that is the dominant form by contract count, and that they are consistently critical of *Pflege-Bahr* for the ratio between the benefit it buys and the *Versorgungslücke* it is meant to close. **No score, no price and no test date is asserted**; every such specific is `[unverified]`.

(delib-pflegerentenversicherung-s11)=

### S11 — Verbraucherzentrale, consumer guidance on *Pflegezusatzversicherung*
- Publisher / doc type: Verbraucherzentrale Bundesverband and the *Länder* consumer centres — **secondary**; consumer guidance pages.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the settled consumer-advice position the product specification reports as such rather than as a reading of any page — that a *Pflegetagegeld* written **not** *nach Art der Lebensversicherung*, and so carrying no ageing provision, has a premium that follows attained-age risk upward and **becomes unaffordable at exactly the ages the cover is needed**, which is the form consumer bodies single out to avoid. `[unverified]` throughout.

(delib-pflegerentenversicherung-s12)=

### S12 — Finanztip, guidance on *Pflegezusatzversicherung*
- Publisher / doc type: Finanztip — **secondary**; consumer guidance.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the same class of evidence as S11, retained separately for one point the delib documents actually act on — that a top-up should be **sized against the *Eigenanteil* in a *Pflegeheim* rather than against a round number**, which is the reasoning behind the `[std]` *vereinbarte Rente* of 1 000,00 € a month. Any specific recommended amount is `[unverified]`; and, with S10, for the observation that the public guidance concentrates on *Pflegetagegeld*.

(delib-pflegerentenversicherung-s13)=

### S13 — Comparison portals: Verivox, Check24
- Publisher / doc type: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**; quote engines.
- URL: not established.
- Retrieved: **no** — egress blocked; **none was queried**, there being neither fetch nor search.
- Used for: recording that the **only public sources that would produce a premium for a named age, benefit and option set on demand were not consulted**, so the premium band the documents print rests on stated arithmetic and is `[std]`, never `[S13]`. Whether either portal quotes *Pflegerente* at all, as opposed to *Pflegetagegeld* only, was **not established**.

(delib-pflegerentenversicherung-s14)=

### S14 — Ratings agencies: Morgen & Morgen, Franke und Bornberg, Assekurata
- Publisher / doc type: MORGEN & MORGEN GmbH; Franke und Bornberg GmbH; ASSEKURATA Assekuranz Rating-Agentur GmbH — **secondary**; product ratings and market studies.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the statement that the German biometric-product rating agencies rate *Pflegezusatzversicherung* wordings **clause by clause**, and are therefore the best public route to the observed range of *Leistungsstaffel*, *Wartezeit*, *Karenzzeit* and *Nachprüfung* terms — precisely the ranges this product had to standardise. **Nothing from any of them was retrieved**, so the variation table in `product-spec.md` is an `[unverified]` market-range reconstruction and is **not** rating data. See also [REG-R53].

(delib-pflegerentenversicherung-s16)=

### S16 — PKV-Verband, *Zahlenbericht der privaten Krankenversicherung* and the association's *Pflegezusatzversicherung* statistics
- Publisher / doc type: PKV-Verband — **secondary** for product terms, primary for market counts; annual statistical report and standing statistics pages.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **negative** market finding the product specification has to make plainly: the only public counting of German private LTC top-up contracts counts **health-insurance** contracts, so *Pflegetagegeld* and *Pflegekosten* are in it and ***Pflegerentenversicherung*, written by *Lebensversicherer*, is not**; it counts contracts rather than insured persons; and, with [R22], there is therefore **no sourced count of German *Pflegerente* contracts in force anywhere in this research**. Any figure of this class is `[unverified]`.

---

## Regulatory and actuarial references (product research numbering)

Every entry below carries the same retrieval status as the primary sources, for the same two
reasons. Canonical URLs are given only where the form is one this author is confident of, and are
marked `[unverified]`; elsewhere `URL: not established`.

(delib-pflegerentenversicherung-r1)=

### R1 — SGB XI, *Elftes Buch Sozialgesetzbuch — Soziale Pflegeversicherung*
- Publisher / doc type: Bundesministerium der Justiz / juris; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the statute that creates the first layer, and the two design principles the whole product rests on — **membership follows health insurance**, so the layer is universal, and the scheme is a ***Teilleistungssystem***, paying defined amounts per *Pflegegrad* rather than the cost of care, with the residue falling on the insured person. That constitutive choice is why a third layer exists as a market at all. Also for the *Beitragssatz* figures in the regulatory-context section, every one of which is `[unverified]` and stamped with its year.

(delib-pflegerentenversicherung-r2)=

### R2 — SGB XI §§ 14 and 15 — *Begriff der Pflegebedürftigkeit* and the *Pflegegrade*
- Publisher / doc type: Bundesministerium der Justiz / juris; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__14.html`, `.../__15.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the insured event of this product.** § 14 defines *Pflegebedürftigkeit* by loss of *Selbstständigkeit* expected to last at least six months, not by minutes of care time, which is what brings cognitive and psychiatric impairment into the assessment on equal terms; § 15 converts the assessment into one of five *Pflegegrade* through six weighted *Module* scored on a 0-to-100 scale. The module weights, the grade thresholds and the *besondere Bedarfskonstellationen* route are all printed with `[unverified]`. The consequence the model turns on: **the private insurer does not define the insured event and does not assess the claim**, so it carries definition risk no wording can hedge, and a *Pflegegrad* is a step function of a continuous state, re-assessed episodically — which is exactly the discrete-state, discrete-time chain `Pflege_DE_S` implements.

(delib-pflegerentenversicherung-r3)=

### R3 — SGB XI §§ 36, 37, 38 — *Pflegesachleistung*, *Pflegegeld*, *Kombinationsleistung*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__36.html`, `.../__37.html`, `.../__38.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the first-layer benefits for **care at home**, which the product specification tabulates by *Pflegegrad* with every amount `[unverified]` and stamped 2025; the *Pflegegeld* running at roughly 44 % of the corresponding *Sachleistung*, which is what makes informal care viable and why five in six *Pflegebedürftige* are cared for at home; the pro-rata combination of the two; and ***Pflegegrad* 1 receiving neither**, which is the statutory fact behind the `[std]` decision to insure nothing at grade 1 on the `delib_std` *Leistungsstaffel*.

(delib-pflegerentenversicherung-r4)=

### R4 — SGB XI § 43 (*vollstationäre Pflege*) and § 43c (*Leistungszuschläge*)
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__43.html`, `.../__43c.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the arithmetic of the *Versorgungslücke*, which is the number the product is sized against.** § 43 sets the SPV's contribution to the **care-related** cost of a *Pflegeheim* only, leaving *Unterkunft und Verpflegung*, *Investitionskosten* and any *Ausbildungsumlage* to the resident in full, and the residue as the *einrichtungseinheitlicher Eigenanteil* — identical for *Pflegegrade* 2 to 5 within one facility. § 43c adds the duration-dependent *Leistungszuschläge* that reduce the EEE the longer the stay, which is why the *Eigenanteil* is **highest in the first year** and a constant annuity progressively over-covers the gap. Every amount and every percentage step is `[unverified]`.

(delib-pflegerentenversicherung-r5)=

### R5 — SGB XI § 45b (*Entlastungsbetrag*), § 39 (*Verhinderungspflege*), § 42 (*Kurzzeitpflege*)
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__45b.html`, `.../__39.html`, `.../__42.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the secondary first-layer heads, recorded for completeness and to support the statement that **they do not close the residential funding gap** — the earmarked *Entlastungsbetrag* available in every grade including 1, and the merger of *Verhinderungspflege* and *Kurzzeitpflege* into a *gemeinsamer Jahresbetrag*. Amounts and dates `[unverified]`.

(delib-pflegerentenversicherung-r6)=

### R6 — SGB XI § 18 (*Begutachtung*) and the *Begutachtungs-Richtlinien* (BRi) of the GKV-Spitzenverband
- Publisher / doc type: statute and the GKV-Spitzenverband's assessment guidance; the operational instrument is the *Neues Begutachtungsassessment* (NBA).
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **why this product's claims administration is cheap and its basis risk is not.** The assessment is made by the *Medizinischer Dienst* for the statutorily insured and by MEDICPROOF for the privately insured — bodies that are **not the private insurer**, whose determination the private insurer ordinarily accepts. Four consequences the documents carry: the *Nachprüfung* is a documentation exercise rather than the adversarial re-assessment that drives a *Berufsunfähigkeitsrente*'s claims cost, which is why `claim_expense_pp` is set low; the insurer carries **assessment-regime risk**, since any loosening of the BRi raises incidence with no contractual change; a *Höherstufung* is applied for and re-assessed, so grade change is **biometric** in the model rather than elective; and a person sits at a grade until re-assessed, which is what makes the Markov representation a match rather than an approximation.

(delib-pflegerentenversicherung-r7)=

### R7 — SGB XI § 23 — *private Pflegepflichtversicherung*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_11/__23.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: one definitional point with a direct modelling consequence — that everyone in the *private Krankenversicherung* must hold a private LTC cover at least equivalent to the SPV's, so **the first layer is the same size for a privately insured person as for a statutorily insured one**, the *Versorgungslücke* is the same for both populations, and `Pflege_DE_S` needs no separate PPV variant.

(delib-pflegerentenversicherung-r8)=

### R8 — SGB XI §§ 126–130, in particular § 127 — *Pflege-Bahr*
- Publisher / doc type: statute (the state-subsidised private LTC top-up introduced by the *Pflege-Neuausrichtungs-Gesetz*).
- URL: `https://www.gesetze-im-internet.de/sgb_11/__127.html` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two things this product genuinely needs. First, **the only *Leistungsstaffel* fixed by German statute** — the 10 / 20 / 30 / 40 / 100 % minimum grid, shipped as the `bahr` schedule in `benefit_scale_table.csv` and exercised by model point 5, and the reference point every private grid is read against. Second, **why a state subsidy that exists for LTC cover is unavailable to the modelled product**: § 127 confines the *Zulage* to a *Pflegetagegeld* conducted *nach Art der Lebensversicherung*, so ***a Pflegerentenversicherung cannot be a geförderter Tarif*** and delib does not implement the *Zulage*. The scheme's other parameters — the 5 € *Zulage*, the 10 € minimum contribution, the *Kontrahierungszwang*, the five-year *Wartezeit* — are printed with `[unverified]`, and its no-underwriting design is cited as the market's natural experiment on anti-selection.

(delib-pflegerentenversicherung-r9)=

### R9 — *Zweites Pflegestärkungsgesetz* (PSG II)
- Publisher / doc type: reform act; the operative changes took effect 1 January 2017 `[unverified]`.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the structural break that is the largest basis risk in the product.** The act replaced the three *Pflegestufen* with the five *Pflegegrade*, replaced the time-based assessment with the NBA [R6], and introduced the *einrichtungseinheitlicher Eigenanteil* [R4]. Three consequences the documents carry: every time series of *Pflegebedürftige*, incidence and duration is discontinuous at 2017, so any basis calibrated on earlier experience needs a stated mapping; a broad transitional mapping moved existing recipients into the new grades; and **the insured population widened**, because cognitive impairment now scores on equal terms. It is the reason `Pflege_DE_S` ships an explicitly labelled `[std]` proxy rather than anything presented as a calibration.

(delib-pflegerentenversicherung-r10)=

### R10 — *Pflegeunterstützungs- und -entlastungsgesetz* (PUEG)
- Publisher / doc type: financing and benefit act, 2023 `[unverified]`.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the point that the statutory amounts are uprated **episodically by legislation** while the *Eigenanteil* rises with care-sector wage costs every year [R20] — every uprating a one-off catch-up against a continuous drift. That asymmetry is the structural argument for the *Leistungsdynamik* option, which model point 8 switches on. The act's own uprating steps and dates are `[unverified]`, and whether anything further took effect on 1 January 2026 was **not established**.

(delib-pflegerentenversicherung-r11)=

### R11 — VVG — the contract-law provisions this product runs on
- Publisher / doc type: Bundesministerium der Justiz / juris; statute (§§ 7, 19, 153, 163, 165, 169, 155, 203).
- URL: canonical form `https://www.gesetze-im-internet.de/vvg_2008/__169.html` and siblings `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the product's whole contractual frame, and the comparison that defines it.** § 163 is the only route by which a life insurer may adjust a premium — a non-temporary change in a calculation basis with an independent trustee's agreement — and **§ 203, the health-insurance *Beitragsanpassung*, does not apply**, which is the single load-bearing difference between a *Pflegerente* and a *Pflegetagegeld* and the reason the *Pflegerente* costs more. Also: § 7 and the VVG-InfoV for the pre-contractual information duties [S5] [S7]; § 19 for the *vorvertragliche Anzeigepflicht*, with the time bar on the insurer's remedies in § 21 Abs. 3 `[unverified]`, which confines the *Gesundheitsprüfung*'s effect on incidence to the first decade of a contract whose claims arrive forty years out; § 153 for the *Überschussbeteiligung* the base run deliberately omits; § 165 for the *Beitragsfreistellung* the model does not implement; § 169 for the *Rückkaufswert*, the five-year acquisition-cost spread and the *Stornoabzug* conditions that keep the shipped deduction at zero; and § 155 for the *Standmitteilung* [S8]. **Whether the § 169 exception for covers paying only on death reaches a pure-risk *Pflegerente* was not established**, and the product specification states the open question rather than assuming it away.

(delib-pflegerentenversicherung-r12)=

### R12 — VAG §§ 138, 139, 146, and § 341f HGB
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: § 138 VAG, the requirement that life premiums be calculated on prudently chosen assumptions sufficient to meet the obligations permanently — which is the statutory anchor of the five first-order margins in `basis_table.csv` and which bites hardest on the *Pflegewahrscheinlichkeiten*, the least stable of the biometric bases; § 139 VAG for the supervisory side of the *Überschussbeteiligung*; **§ 146 VAG only to locate the boundary the *Pflegerente* sits on the other side of** — the *substitutive Krankenversicherung* regime with its *Alterungsrückstellung*; and § 341f HGB for the prospective *Deckungsrückstellung* in the commercial accounts, the reserve the model does not compute.

(delib-pflegerentenversicherung-r13)=

### R13 — DeckRV, *Deckungsrückstellungsverordnung*
- Publisher / doc type: regulation; fixes the *Höchstrechnungszins* and the *Höchstzillmersatz*.
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **two cited numbers in the whole pricing basis** — the **1,00 %** *Höchstrechnungszins* for new business from 1 January 2025, which attaches to the cohort at issue and is the rate `rechnungszins` carries, and the **25 ‰** *Höchstzillmersatz* of the *Beitragssumme* that `acq_permille` is set exactly at so the ceiling binds visibly. Both are `[unverified]` as to their dates, and the rate history the product specification prints is `[unverified]` throughout. The provision matters more here than on any other delib product: a *Pflegerente* discounts benefits falling on average some thirty-five years after issue, so its premium is the most interest-sensitive in the library. See also [REG-R14], [REG-R15], [REG-R16].

(delib-pflegerentenversicherung-r14)=

### R14 — KVAV, *Krankenversicherungsaufsichtsverordnung*
- Publisher / doc type: the calculation regulation for private health insurance — the *Alterungsrückstellung*, the *Sicherheitszuschlag*, and the *auslösende Faktoren* that trigger a § 203 VVG *Beitragsanpassung*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the regime the *Pflegetagegeld* comparison sits under, and never as a rule applying to the modelled product.** It is what makes the competing-forms table's re-rating and ageing-provision rows structural rather than `[unverified]`: a *Pflegetagegeld* is health business calculated under the KVAV, a *Pflegerente* is life business calculated under the DeckRV [R13].

(delib-pflegerentenversicherung-r15)=

### R15 — DAV 2008 P — the German *Pflegetafel*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV); standard biometric table with a published derivation paper.
- URL: not established (`aktuar.de` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the actuarial reference this product turns on, cited by name and never reproduced.** It is the German market's standard basis for LTC business calculated *nach Art der Lebensversicherung*, and it is a **multi-state** table: incidence by sex, attained age **and grade of entry**; transition probabilities between grades; *Reaktivierungswahrscheinlichkeiten*; and separate mortality for active lives and for lives in each grade. **The table is the property of the DAV, is not public, and is not redistributed by this library**; no value from it appears anywhere, and none may. What the documents carry instead is (a) what a replacement must preserve — the four properties listed in `model.md` and in the `Data` docstring — and (b) that it was built on the superseded *Pflegestufen* [R9], which is the largest single source of basis risk in the product and the reason every shipped transition rate is an explicitly labelled `[std]` proxy anchored so the worked example reproduces exactly. See also [REG-R51].

(delib-pflegerentenversicherung-r16)=

### R16 — DAV 2008 T and DAV 2004 R
- Publisher / doc type: DAV; the standard German mortality tables for covers with a death character and for annuities.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two narrow places, and one warning. The **active-life mortality** the shipped Gompertz proxy stands in for is stated to be neither DAV 2008 T nor the DAV 2008 P active-life table, and a *Todesfallleistung* written into a *Pflegerente* is a death cover priced as one. The warning is the one the model's `mort_mult` construction exists to prevent: **DAV 2004 R is built to be prudent about people living *longer*, whereas the annuity in payment on a *Pflegerente* is paid to a heavily impaired population, so using an annuity table here would be prudent in exactly the wrong direction and would materially overprice the benefit.** **Neither table is redistributed here.** See also [REG-R48], [REG-R49].

(delib-pflegerentenversicherung-r18)=

### R18 — Destatis, *Pflegestatistik*
- Publisher / doc type: Statistisches Bundesamt; biennial statutory statistics under SGB XI.
- URL: not established (`destatis.de` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the prevalence section, every figure of which is `[unverified]` and is a reconstruction **not** read from the series — the count of *Pflegebedürftige*, the home/residential split, the distribution across *Pflegegrade*, and the age-specific prevalence curve. Two of those carry real weight in the model: the **stock** distribution of about 9 / 44 / 27 / 14 / 6 %, which the documents use to argue that `entry_share` must be **lower** than the stock because deterioration moves people up over a spell; and **prevalence roughly doubling every five years of age above 75**, the one shape stated with confidence, which is what anchors the incidence proxy's slope at `ln 2 / 5 = 0.1386`. The series' own 2017 break [R9] is recorded.

(delib-pflegerentenversicherung-r19)=

### R19 — Destatis, *Pflegevorausberechnung*
- Publisher / doc type: Statistisches Bundesamt; official projection of the number of *Pflegebedürftige*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the qualitative statement behind the product's commercial case — that the number of *Pflegebedürftige* rises materially over the next three decades as the baby-boom cohorts reach the ages at which prevalence is high. The projected count and its date are `[unverified]`.

(delib-pflegerentenversicherung-r20)=

### R20 — vdek and BMG material on the *Eigenanteil* in *Pflegeheimen*
- Publisher / doc type: Verband der Ersatzkassen e. V.; Bundesministerium für Gesundheit; the twice-yearly series on the average resident payment by component and by *Bundesland*.
- URL: not established (`vdek.com` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the level and, more importantly, the **structure** of the number the product is sold against — only the *EEE* component is reduced by the § 43c *Leistungszuschläge* and only the *EEE* is equalised across *Pflegegrade* 2 to 5, while *Unterkunft und Verpflegung* and *Investitionskosten* are neither capped nor subsidised and are the fastest-growing components. The levels themselves are **the least reliable figures in this product's research**, are `[unverified]`, and are used only to argue the order of magnitude of the `[std]` *vereinbarte Rente* of 1 000,00 € — never as data.

(delib-pflegerentenversicherung-r21)=

### R21 — PKV-Verband statistics on *Pflegezusatzversicherung* and *Pflege-Bahr*
- Publisher / doc type: PKV-Verband; annual counts of subsidised and unsubsidised private LTC top-up contracts.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the same counting as [S16], from the regulatory-reference side, and for one structural finding that does not depend on a figure: **Pflege-Bahr take-up rose quickly in its first three or four years and then stopped growing**, while the unsubsidised market is several times larger. All contract counts are `[unverified]`.

(delib-pflegerentenversicherung-r22)=

### R22 — GDV life-market statistics
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; the annual life-market series — new business and in force by product family, premium income, the *Stornoquote*.
- URL: not established (`gdv.de` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: a purely **negative** statement, and it is worth making plainly: the GDV series does not carve out *Pflegerentenversicherung* as a reported product family on the evidence available here, so with [S16] and [R21] **there is no sourced count of German *Pflegerente* contracts in force anywhere in this research**, and the market-size statements in `product-spec.md` are qualitative. See also [REG-R53].

(delib-pflegerentenversicherung-r23)=

### R23 — EStG — the tax provisions
- Publisher / doc type: statute (§ 10 Abs. 1 Nr. 3 and Nr. 3a; § 3 Nr. 1a; § 22 Nr. 1; § 20 Abs. 1 Nr. 6), with BMF administrative guidance.
- URL: `https://www.gesetze-im-internet.de/estg/` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two statements the product specification has to make honestly. On **premiums**, that a *Pflegerente* premium is a *sonstige Vorsorgeaufwendung* deductible only within an annual ceiling that the compulsory health and LTC contributions normally exhaust on their own, so **in practice, for most buyers, the premium is not deductible at all** — which is also why the *Pflege-Bahr* subsidy [R8] was designed as a direct payment rather than as a further deduction. On **benefits**, that two analyses compete — exemption under § 3 Nr. 1a as a benefit from a *Pflegeversicherung*, the analysis universally applied to *Pflegetagegeld*, against *Ertragsanteil* taxation under § 22 as a *Leibrente*, the analysis applied to a *Berufsunfähigkeitsrente* and the one this product's life-assurance form argues for — and that **this corpus cannot say which governs**. delib does not model benefit taxation and states the open question instead. Every ceiling and paragraph number is `[unverified]`. See also [REG-R41], [REG-R45].

(delib-pflegerentenversicherung-r24)=

### R24 — SGB XII §§ 61–66 (*Hilfe zur Pflege*) and the *Angehörigen-Entlastungsgesetz*
- Publisher / doc type: statute.
- URL: `https://www.gesetze-im-internet.de/sgb_12/` `[unverified]`.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the means-tested backstop that completes the three-layer picture, and two consequences the documents draw from it. **A private *Pflegerente* with a *Rückkaufswert* is realisable assets** in the means test before a claim, and the annuity is income during it, so a contract with no surrender value is on that reasoning the more robust design for a buyer whose likely destination is social assistance — an argument for the pure-risk variant that has nothing to do with price. And the *Angehörigen-Entlastungsgesetz* removed the *Elternunterhalt* motive for all but high-earning families, which is one of the reasons the documents give for low market penetration. Every threshold and date is `[unverified]`.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **Every entry on that page records
`Fetched: no`**, for the same two reasons given at the head of this file, so these tags inherit
the same status. Entries cited by the *Pflegerentenversicherung* documents:

- **REG-R1 / REG-R2 / REG-R3 / REG-R4 / REG-R6** — Solvabilität II, the Delegated Regulation, the 2025 review, the EIOPA risk-free curves and VAG §§ 74–110: the valuation layer that consumes `liability_cf`, cited and never computed. A best estimate is `Σ v(t) liability_cf(t)` plus a risk margin, and **nothing in this library discounts**.
- **REG-R5** — VAG 2016 and its Anlage 1: the *Sparten* boundary that puts a *Pflegerente* in life and a *Pflegetagegeld* in health, which is the whole of [S2] and [R14] restated at statute level.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the premium-sufficiency requirement that the five first-order margins in `basis_table.csv` answer to. **Only the direction of prudence is cited**; no German *Sicherheitszuschlag* level for a *Pflegetafel* was established.
- **REG-R9 / REG-R10 / REG-R18 / REG-R19** — VAG §§ 139, 140 and 145, the MindZV and the RfBV: the surplus machinery the base run deliberately omits, recorded so that a user adding an *Überschussbeteiligung* knows which regime it sits under.
- **REG-R11** — VAG §§ 141–143: the *Verantwortlicher Aktuar* and the *Treuhänder*, the office that in practice sets the prudence margins this model ships as `[std]` numbers.
- **REG-R14 / REG-R15** — the DeckRV and the *Höchstrechnungszins* rate history: the **1,00 %** for new business from 1 January 2025 that `rechnungszins` carries and the equivalence discounts at — the one genuinely cited pricing assumption in the model.
- **REG-R16 / REG-R20** — DeckRV § 4 *Höchstzillmersätze* and the LVRG cut from 40 ‰ to 25 ‰: the ceiling `acq_permille` sits **exactly at**, so the ceiling binds visibly, and the reason `surrender_table.csv`'s first two years are zero.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins*, the *Zinszusatzreserve* and the *Korridormethode*: named in the valuation pointers as a reserve this model does not compute.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: absorbed into the first-year lapse rate rather than modelled.
- **REG-R24** — VVG § 153, the *Überschussbeteiligung* and the *hälftige Beteiligung an den Bewertungsreserven*: the article-level carrier for [R11]'s surplus limb, and why a biometric-risk product's surplus is dominated by the *Risikoergebnis*.
- **REG-R25** — VVG §§ 154 and 155, the *Modellrechnung* and the *Standmitteilung*: the article-level carrier for [S8].
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: **the whole of a *Lebensversicherer*'s re-rating power**, and the provision the product's central commercial claim rests on.
- **REG-R28** — VVG §§ 165–170: *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug* — the article-level source for the cash values, the five-year cost spread that shapes `surrender_table.csv`, and the requirement that a *Stornoabzug* be agreed, appropriate and **quantified in the contract**, which is why the shipped value is zero.
- **REG-R29** — VVG §§ 172–177, *Berufsunfähigkeitsversicherung*: cited only to mark the neighbouring product, whose insurer-run *Nachprüfung* is what makes its claims cost several times this product's.
- **REG-R30** — VVG §§ 19, 21, 37, 38, 157 and 158: the *Anzeigepflicht*, the § 21 Abs. 3 time bar on the insurer's remedies, and the *qualifizierte Mahnung* whose two-week period the model does not carry.
- **REG-R31 / REG-R33 / REG-R35** — the VVG-InfoV cost-disclosure regime, the IDD and BaFin's *Wohlverhaltensaufsicht*: the conduct layer, and why a pure biometric-risk contract carries a euro cost disclosure rather than an *Effektivkosten* figure.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: **the article-level carrier for the perimeter question **S6** would have carried.** The Regulation excludes life contracts paying only on death or in respect of incapacity, so a pure-risk *Pflegerente* is very likely outside it and a *Beitragsrückgewähr* form very likely inside — `[unverified]`, and the base run is the variant for which no *Basisinformationsblatt* would be expected.
- **REG-R34** — *Test-Achats* and the AGG: **unisex pricing for contracts concluded from 21 December 2012**, the constraint behind `unisex_mix_male = 0.50` and behind model points 1 and 2 pricing identically and projecting differently.
- **REG-R36** — the BGH line of authority on German life contracts: cited for the point that **the two *Pflege* scales have not been judicially mapped**, which compounds the DAV 2008 P vintage problem [R15].
- **REG-R41 / REG-R45 / REG-R46** — EStG § 22 Nr. 1 (*Ertragsanteil*), § 20 Abs. 1 Nr. 6 and the ErbStG with SGB V §§ 226, 229, 240: the tax section only — the competing analysis of the benefit, the treatment of a *Todesfallleistung* or a surrender payment, and contributions on an annuity in payment.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the direction-of-prudence argument behind the five first-order margins, and the statement that the tables are the DAV's property.
- **REG-R48 / REG-R49 / REG-R51** — DAV 2008 T, DAV 2004 R and **DAV 2008 P with the *Pflegegrad* break**: the entries stating that none of them is public or redistributed, and REG-R51 in particular as the cross-product carrier for [R15] — including the § 15 SGB XI redefinition that the pre-2017 table cannot capture.
- **REG-R52** — Destatis *Sterbetafeln*, *Generationensterbetafeln*, *Pflegestatistik* and the reuse licence: the intended base for a user-supplied replacement, and the cross-product carrier for [R18].
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): market scale, and the carrier for [S14] and [R22] — including the finding that *Pflegerentenversicherung* is not a separately reported family.
- **REG-R54 / REG-R55** — HGB §§ 341–341o with the RechVersV, and IFRS 17: the accounting layers the same expected-cash-flow engine feeds, and the article-level source for the *Deckungsrückstellung* limb of [R12].
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standards this model's documentation sits under.

---

## Provenance note

Extraction details — which fact was recorded from which document class, the twenty-three sections
of extracted mechanics, and the twenty-one-item gaps-and-caveats register — live in
`_research/pflegerentenversicherung.md`, which is the citation ground truth for the S# and R#
numbering used here and states these same retrieval conditions at its head.

The caveats that most affect what these product documents can claim, in the order in which they
constrain the model:

1. **Nothing was retrieved and nothing was searched.** This is the only delib product for which *both* channels were unavailable. Every [S#] and [R#] points to a document that exists and is the right kind of document; not one records a document read. The other delib research files record, per fact, what a search summary established; this one cannot, and says so.
2. **DAV 2008 P is cited and not read, and it was built on the superseded *Pflegestufen*** [R15] [REG-R51]. Two problems compound: the table's contents are unavailable, and the trigger it is applied to was redefined in 2017 [R9] in a way that widened the insured population, with the two scales judicially unmapped [REG-R36]. **This is the largest basis risk in the product**, and every transition rate in `care_table.csv`, `incidence_table.csv` and `mort_table.csv` is a `[std]` proxy with a stated shape and a stated anchor rather than a calibration.
3. **No premium was established and no rate card exists in this corpus** [S9]. `Pflege_DE_S` reproduces nothing external: its *Beitrag* is an **output** of a stated first-order basis, and the argued 50,00–100,00 € band it is checked against is derived arithmetic tagged `[std]`, which **must never be cited as a market figure**. A single portal quotation or *Tarifblatt* would close this gap.
4. **No charge level of any kind was established** [S5] [S7]. Not one *Abschlusskostensatz*, administration rate, *Ratenzahlungszuschlag* or *Effektivkosten* value for any *Pflegerenten* tariff. Only the statutory 25 ‰ **ceiling** is known [R13] [REG-R16], and only `[unverified]`; the acquisition charge is set exactly at it so that the one cited quantity is visible, and every other level in `expense_table.csv` is a placeholder.
5. **Not one carrier document, product name or parameter was established** [S4]. The variation table in `product-spec.md` is a market-range table **with no attribution**, and no German insurer is named against any figure anywhere. This is the largest single difference between this product and its frlib counterpart, where eight carriers' contracts were read in full.
6. **Every duration and incidence figure is unsourced** [R18] [R19], and duration is the direct multiplier on the liability. A change from four years to five in the mean spell moves the premium by about a quarter.
7. **No lapse rate for this product at any duration was established.** The shape in `lapse_table.csv` is argued from the *Zillmerung* [REG-R16] [REG-R28] and nothing else, and the pricing basis carries no lapse at all — which is German first-order practice and is also what keeps the model acyclic.
8. **The § 169 VVG scope question is open** [R11] [REG-R28]: whether a **pure-risk** *Pflegerente* falls inside the exception that denies a *Risikolebensversicherung* its surrender value was not established. The model prices a *Rückkaufswert* and the documents state the question; a carrier's own wording settles it for that carrier.
9. **The taxation of the benefit is unresolved** [R23] [REG-R41]. Two analyses compete and this corpus cannot choose between them; delib does not model benefit taxation.
10. **The statutory benefit amounts are 2025 values and the 2026 position was not established** [R3] [R4] [R10]. Every figure in the first-layer tables is stamped 2025 and tagged `[unverified]`. **Any downstream document must re-check the year.**
11. **No BaFin material specific to LTC was located**, which is why R17 is absent from this file altogether and why the supervisor enters only through [REG-R35]. There is no supervisory statement anywhere in these documents about *Pflegetafel* prudence, about the *Nachprüfung*, or about product value for this class.
12. **The SGB XI, the VVG, the VAG, the EStG and the DeckRV are living texts**, and the *Höchstrechnungszins* changes by instrument [R13] [REG-R15]. No version date is asserted anywhere. Check every provision against the current consolidated text before relying on it. **A delib citation is a pointer, not a certificate.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #delib-pflegerentenversicherung-r10
[R11]: #delib-pflegerentenversicherung-r11
[R12]: #delib-pflegerentenversicherung-r12
[R13]: #delib-pflegerentenversicherung-r13
[R14]: #delib-pflegerentenversicherung-r14
[R15]: #delib-pflegerentenversicherung-r15
[R18]: #delib-pflegerentenversicherung-r18
[R19]: #delib-pflegerentenversicherung-r19
[R20]: #delib-pflegerentenversicherung-r20
[R21]: #delib-pflegerentenversicherung-r21
[R22]: #delib-pflegerentenversicherung-r22
[R23]: #delib-pflegerentenversicherung-r23
[R3]: #delib-pflegerentenversicherung-r3
[R4]: #delib-pflegerentenversicherung-r4
[R6]: #delib-pflegerentenversicherung-r6
[R8]: #delib-pflegerentenversicherung-r8
[R9]: #delib-pflegerentenversicherung-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R25]: #delib-reg-r25
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R51]: #delib-reg-r51
[REG-R53]: #delib-reg-r53
[std]: #delib-std
<!-- END generated citation links -->
