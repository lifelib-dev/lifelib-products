# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/risikolebensversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. **No id is absent
from this file and the numbering has no gaps**: all seventeen primary sources **S1–S17** and all
twenty-three product-level references **R1–R23** are cited by `product-spec.md`, eighteen of the
R-entries again by `technical-notes.md`, and sixteen again by `model.md`. That completeness is not
evidential strength but its opposite. Under the retrieval conditions below **no document here was
opened**, so nothing could be dropped for saying too little: every entry is cited for what it
*would* settle and for the fact that it did not. Where a sibling library's `sources.md` records
omitted ids — frlib drops three for returning nothing citable — this one records absences of a
different kind, in each entry's `Retrieved` line and in the closing register. Access date for all
sources: **2026-08-29**. No sources were newly added at drafting. Cross-product [REG-R#] tags are
listed in their own section at the end.

**Retrieval conditions — read before any entry below.** Two independent limits applied, and this
product sits at the worse end of both. **(1) Direct HTTP egress is blocked** by an organisation
network policy: `WebFetch` and `curl` are refused with HTTP 403 at the egress gateway for every
host outside a short package-registry allowlist. `gesetze-im-internet.de`, `bafin.de`, `gdv.de`,
`aktuar.de`, `bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de` and
`de.wikipedia.org` were all tried and all refused. **No document cited anywhere in this file was
retrieved** — no AVB, no *Produktinformationsblatt*, no *Verbraucherinformation*, no statutory
text, no rate card, no comparison-portal result. **(2) The session's `WebSearch` budget — 200
calls, shared across the library — was exhausted *before* this product's research began**, during
the regulatory and contract-law work and during delib products 1 and 2. Every search attempted for
this product returned the budget-exhausted message, so it had **no research channel at all**.

What follows from that, stated plainly. **A delib citation is a pointer, not a certificate**: it
names the instrument a claim should be checked against and does not assert that anyone checked it.
Every entry below is a **known reference** — a document that exists and is the right kind of
document for the claim beside it — with `URL: not established` unless the canonical form is one
this author is confident of, and with a `Retrieved` line that says `no`. **No entry asserts an
edition, a tariff code, a document number, a page count or a publication date**, because none
could be established and none is guessed. **Nothing anywhere in this product's documents is
quoted**: every description of a statute or a clause is a paraphrase and every paragraph number is
`[unverified]`.

One thing here *is* evidence, and it is second-hand. Several instruments this product turns on
were **search-corroborated for the two sibling products while budget remained**, and their
findings are recorded in `_research/kapitallebensversicherung.md` and
`_research/klassische_rentenversicherung.md`. Where an entry below says **"inherited
corroboration"**, someone checked something — for the sibling's purpose, not for this one. That
chain covers §§ 161, 169, 165, 19 and 153 VVG, the MindZV percentages, the DeckRV rate history and
the DAV 2008 T *Richtlinie*, and it is the strongest thing in this file. **Everything not so marked
has none.** Uncertain numbers became **[std]** parameters rather than citations: not one
*Bruttobeitrag*, *Zahlbeitrag*, spread ratio, smoker ratio, charge, commission scale or lapse rate
in this product's documents is an observation, and `model.md`'s standardization table lists every
one.

---

## Primary product sources

(delib-risikolebensversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die Risikoversicherung" (*Musterbedingungen*)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt or ignore. Expressly *unverbindlich* and optional, which is a competition-law disclaimer and is load-bearing for citation weight
- URL: not established for the term-assurance wording. The *Musterbedingungen* index at `https://www.gdv.de/gdv/service/musterbedingungen` was returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` S1]; **the per-document path is not established and is not guessed**
- Retrieved: **no** — direct HTTP egress blocked in the build environment; **no search corroboration** (session search budget exhausted). Partial inherited corroboration of the index page only
- Used for: the existence of a market template for this line, and the question-headed second-person drafting style of post-2008-VVG German wordings, in `product-spec.md`'s overview and its variations section. **No article text was established**, so every benefit, surplus, exclusion or termination rule the documents state is attributed to the statute it implements [R1]–[R8] or carried as **[std]** — never to S1. An `[S1]` tag here means "the market has a template", not "a carrier's wording says this"

(delib-risikolebensversicherung-s2)=

### S2 — GDV, *Produktinformationsblatt* pattern for the *Risikoversicherung*
- Publisher / doc type: GDV; model *Produktinformationsblatt* (PIB) — the short pre-contractual product summary required for life products by the VVG-InfoV [R17]
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the document class `product-spec.md` names in its regulatory context and its identity table — the PIB, not a *Basisinformationsblatt*, is this product's pre-contractual summary [R17]. It matters more here than for any other delib product because the PIB is **the natural place a carrier states the *Bruttobeitrag* and the *Zahlbeitrag* side by side**, and no specimen was located, which is the direct cause of gap 1. The inference from the document's purpose is `[unverified]` and no field list is asserted

(delib-risikolebensversicherung-s3)=

### S3 — CosmosDirekt (Cosmos Lebensversicherungs-AG), *Risikolebensversicherung*
- Publisher / doc type: Cosmos Lebensversicherungs-AG; *Allgemeine Bedingungen für die Risikoversicherung*, *Verbraucherinformation* pack and product page
- URL: not established. The carrier's AVB naming convention runs `LA <number> <letter>` [inherited: `klassische_rentenversicherung.md` S8]; **the term-assurance tariff code is not established and is not guessed**
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the direct-channel end of the distribution range in `product-spec.md`'s variations and market-role sections, and — cited jointly with [S12] — the **structural** argument in `technical-notes.md` and `model.md` that the *Brutto*/*Zahlbeitrag* spread is widest where no *Abschlussprovision* is paid to an intermediary. That reasoning is structural, not sourced. It is also one of the two entries carrying `model.md`'s warning that the **[std]** acquisition cost at the 25 ‰ Zillmer ceiling may be far above a slim direct-channel cost

(delib-risikolebensversicherung-s4)=

### S4 — Hannoversche Lebensversicherung AG (VHV group), *Risikolebensversicherung*
- Publisher / doc type: Hannoversche Lebensversicherung AG; AVB, *Verbraucherinformation*, product page
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the second long-standing German direct writer of term assurance, in `product-spec.md`'s carrier-coverage table and its distribution paragraph, recorded for the same structural reason as [S3]. **No wording, tariff code, rate or edition date is asserted anywhere from it**

(delib-risikolebensversicherung-s5)=

### S5 — HUK-COBURG / HUK24, *Risikolebensversicherung* and the *Überschussbeteiligung* guide
- Publisher / doc type: HUK-COBURG / HUK24; insurer guide page **about term assurance specifically**, plus the product pages
- URL: `https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung` — **returned by a search during the sibling research** [inherited: `kapitallebensversicherung.md` S17]
- Retrieved: **no** — egress blocked; **inherited corroboration of the page's existence, title and vocabulary only**
- Used for: the single most useful inherited item in this product's corpus, and the one that contradicts the intuition an Anglophone modeller brings to "term life": a carrier's own page titled *Überschussbeteiligung der Risikolebensversicherung*, so the carrier itself treats surplus participation as **central to term assurance**. `product-spec.md` cites it for that characterisation and for the four-component surplus vocabulary — *Zins-*, *Risiko-*, *Kosten-* and *übrige Überschüsse* — used by carriers across product lines; `technical-notes.md` cites it in the contractual-elements table beside the *Zahlbeitrag* row. **No rate, no *Beitragsverrechnung* percentage and no spread ratio is inherited or asserted** (gap 1)

(delib-risikolebensversicherung-s6)=

### S6 — Debeka Lebensversicherungsverein a. G., *Bedingungswerk* for the *Risikoversicherung*
- Publisher / doc type: Debeka Lebensversicherungsverein a. G.; *Bedingungswerk* (Debeka's name for its AVB booklets) in the carrier's public *Vertragsgrundlagen* library
- URL: not established. The library's path pattern `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/<code>.pdf` was established from the sibling research [inherited: `kapitallebensversicherung.md` S3–S6]; **the term-assurance code is not established and no path is guessed**
- Retrieved: **no** — egress blocked; no search corroboration for any term-assurance wording
- Used for: the largest German life mutual by contract count in `product-spec.md`'s variations table, and for two inherited cautions the specification repeats rather than hides: a carrier may maintain **several parallel wordings of different vintages within one product family**, and *Überschussbeteiligung* clause numbering is **tariff-dependent**, so any specific section number in a German AVB is `[unverified]`. **No Debeka term-assurance figure is asserted**

(delib-risikolebensversicherung-s7)=

### S7 — Dialog Lebensversicherungs-AG (Generali group), *Risikolebensversicherung*
- Publisher / doc type: Dialog Lebensversicherungs-AG; AVB, *Verbraucherinformation*, broker-facing tariff material
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the German market's specialist term-life carrier for the broker channel, in `product-spec.md`'s variations and distribution sections, and for one argument that reaches the mechanics: a **monoline's *Risikoergebnis* is its entire technical result**, so the MindZV minimum allocation [R9] binds its surplus policy directly rather than competing with an investment result. The positioning is asserted from market knowledge; **no wording, tariff, rate, *Berufsgruppen* table or surplus declaration is asserted** (gap 5)

(delib-risikolebensversicherung-s8)=

### S8 — Allianz Lebensversicherungs-AG, *Risikolebensversicherung*
- Publisher / doc type: Allianz Lebensversicherungs-AG; AVB, *Produktinformationsblatt*, product page
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration for any term-assurance document
- Used for: the market leader by premium income and the tied-agent end of the distribution range in `product-spec.md`'s variations table, and as the natural reference for the **narrow-spread** end of the *Brutto*/*Zahlbeitrag* distribution — a structural argument, not an observation (gap 1). One inherited fact about the family of Allianz life wordings is recorded and then set aside: a declared *laufende Verzinsung* for 2026 of **2,70 %** on the classic book [inherited: `kapitallebensversicherung.md` S11], a **savings-side** rate of no use here, where the *Zinsüberschuss* is negligible

(delib-risikolebensversicherung-s9)=

### S9 — R+V Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: R+V Lebensversicherung AG; AVB, *Produktinformationsblatt*, product page
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the cooperative-bank channel comparator in `product-spec.md`'s variations and distribution sections. **Nothing about its wording, rating structure or surplus declaration is asserted**

(delib-risikolebensversicherung-s10)=

### S10 — NÜRNBERGER Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB, *Verbraucherinformation*
- URL: not established. The carrier's tariff-code convention is visible in the sibling research, which recorded an annuity wording headed "…nach Tarif NIR3301" [inherited: `klassische_rentenversicherung.md` S9]; **the term-assurance code is not established**
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: a broker-channel carrier with a long biometric-risk book, in `product-spec.md`'s variations table only. **No parameter is asserted**

(delib-risikolebensversicherung-s11)=

### S11 — LV 1871 (Lebensversicherung von 1871 a. G.), *Risikolebensversicherung*
- Publisher / doc type: Lebensversicherung von 1871 a. G.; AVB, *Produktinformationsblatt*
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the carrier whose range emphasises *Nachversicherungsgarantien* and occupational differentiation, cited in `product-spec.md`'s riders-and-options section and in `model.md`'s provenance table for `nvg_schedule.csv`. The emphasis is asserted from market knowledge; **no event list, exercise window, per-event cap, cumulative cap or age limit comes from it or from any other document** (gap 7), which is why the option is specified entirely in **[std]** parameters and is **off in the base run**

(delib-risikolebensversicherung-s12)=

### S12 — Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG, *Risikolebensversicherung*
- Publisher / doc type: Continentale Lebensversicherung a. G. and Europa Lebensversicherung AG; AVB, *Produktinformationsblätter*, product pages. Deliberately a **single entry**, because the pair is one group running a broker-channel and a direct-channel carrier side by side in the same product
- URL: not established for either
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: `product-spec.md`'s variations section, as **the cleanest natural experiment available** for isolating the channel effect on the *Brutto*/*Zahlbeitrag* spread with underwriting and reserving basis held constant — and for the record that **it was not run** (gap 5). Cited jointly with [S3] in `technical-notes.md` and `model.md` wherever the **[std]** acquisition cost at the Zillmer ceiling is flagged as the charge most likely to be overstated

(delib-risikolebensversicherung-s13)=

### S13 — Further carriers selling a *Risikolebensversicherung* in Germany
- Publisher / doc type: Alte Leipziger; Volkswohl Bund; Swiss Life Deutschland; Zurich Deutscher Herold; ERGO Vorsorge; AXA; Barmenia; Württembergische; Gothaer; Die Stuttgarter; Baloise (Deutschland); uniVersa; DEVK; SIGNAL IDUNA; Provinzial; Generali Deutschland; HDI — AVB and *Produktinformationsblätter*
- URL: not established for any of them
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: **one thing only** — that each of these carriers offers an individual *Risikolebensversicherung* in Germany, so `product-spec.md`'s variations section can state honestly that a market of this breadth exists and that **none of it was sampled**. **No `[S13]` tag appears on any parameter anywhere in the delib library**, and none may be added. Two of these carriers appear in the sibling research with located documents in *other* product families — Zurich Deutscher Herold [inherited: `klassische_rentenversicherung.md` S4–S7] and Gothaer [inherited: `kapitallebensversicherung.md` S7] — which establishes that their document libraries are public and nothing whatever about their term-assurance wordings

(delib-risikolebensversicherung-s14)=

### S14 — Comparison portals: Check24, Verivox, Tarifcheck — **secondary**
- Publisher / doc type: Check24, Verivox, Tarifcheck; price-comparison result pages and accompanying *Ratgeber* articles. Secondary, not product documents
- URL: not established for the term-assurance pages. The sibling research recorded Verivox *Ratgeber* pages on `Kapitallebensversicherung`, `Überschussbeteiligung` and `Zillmerung` [inherited: `kapitallebensversicherung.md` S15], establishing that the portal publishes explanatory pages of this kind and nothing about its term-assurance pages
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the finding that the portals are **the only public source of German RLV price points**, because no German carrier publishes a rate card and the PIB quotes only the applicant's own premium — and for **why none could be obtained even in principle**: a comparison result is generated per query and is not a published document. `product-spec.md` cites it in the premium section and the market-context section for that; `model.md` cites it in the mechanics-demonstration warning. **No price point of any kind is recorded from it** (gap 1)

(delib-risikolebensversicherung-s15)=

### S15 — Finanztip, "Risikolebensversicherung" — **secondary**
- Publisher / doc type: Finanztip; consumer guide article with a periodically refreshed carrier recommendation. Secondary
- URL: not established. The sibling research recorded Finanztip articles on `Überschussbeteiligung Lebensversicherung` and `Steuer auf Lebensversicherung` [inherited: `kapitallebensversicherung.md` S16], establishing coverage of the subject area and nothing about this article
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the German consumer publication that most consistently makes the ***Brutto*/*Zahlbeitrag* distinction the headline of its term-life advice** — compare the *Bruttobeitrag*, because the *Zahlbeitrag* is what you pay and the *Bruttobeitrag* what you can be made to pay. `product-spec.md` cites it in its overview and in the asymmetry section; `technical-notes.md` cites it beside the benefit rows for the plain statement that nothing is paid on survival or on *Kündigung*; `model.md` cites it for the three sum-insured shapes being structural. **No figure, ranking or spread statistic is asserted** (gap 1)

(delib-risikolebensversicherung-s16)=

### S16 — Stiftung Warentest / *Finanztest*, term-life comparison tests — **secondary**
- Publisher / doc type: Stiftung Warentest; periodic comparison test of RLV tariffs, paywalled with a free summary. Secondary
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the market's most influential comparison test, cited in `product-spec.md`'s variations and market-role sections and in `model.md`'s warning — and cited above all for **its design**, which is why it matters: *Finanztest* rates on the ***Zahlbeitrag* for defined model customers** at a stated age, sum, term and smoking status **and separately reports the *Bruttobeitrag***, so a published test is the one German document type that would supply exactly the paired figures this product lacks. **No edition, date, model-customer definition or premium figure is asserted** (gap 1)

(delib-risikolebensversicherung-s17)=

### S17 — Franke und Bornberg, MORGEN & MORGEN, ASSEKURATA — **secondary**
- Publisher / doc type: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA; tariff ratings (`FB-Unternehmensrating`, `M&M Rating Risikoleben`), market studies and *Bedingungsanalysen*. Secondary
- URL: not established for any term-life rating. The sibling research located Assekurata's "24. Marktstudie *Überschussbeteiligungen und Garantien 2026*" and Franke und Bornberg commentary on *Basisinformationsblätter* [inherited: `kapitallebensversicherung.md` R25, R27], establishing that these houses publish in this field and nothing about their term-life work
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: two market-design facts no statute supplies, both `[unverified]` and both structural rather than numeric: that the ***Brutto*/*Zahlbeitrag* spread is itself a rated criterion**, because it measures the insurer's unilateral headroom to raise the billed premium — which is why `product-spec.md`'s asymmetry section and `model.md`'s two-premium section can say the German market treats the spread as a quality signal — and that the ***Nachversicherungsgarantie* event list, caps and age limit are rated criteria**, which is why the market has converged on a recognisable list. **Neither is used as a numeric parameter anywhere**

---

## Regulatory and actuarial references (product research numbering)

Where a URL appears below it is the **canonical form** of the address on
`gesetze-im-internet.de`, which this author is confident of for the German federal codes. A URL is
marked `[unverified]` unless a search returned it during the **sibling** research, in which case
the entry says so and is marked **inherited corroboration**. Every paragraph number is
`[unverified]` in the documents that cite it, and all statutory content is described in this
author's own words — **nothing is quoted**.

(delib-risikolebensversicherung-r1)=

### R1 — VVG § 161, *Selbsttötung*
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsvertragsgesetz 2008); federal statute, Kapitel 5
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` — **returned by a search during the sibling research** [inherited: `kapitallebensversicherung.md` R4]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the URL and of the rule's content
- Used for: **the strongest single item in this product's corpus.** In an insurance for the event of death the insurer is *leistungsfrei* where the *versicherte Person* intentionally takes her own life **before three years have elapsed** since conclusion; the exception where the act was committed in a state excluding free determination of the will caused by a *krankhafte Störung der Geistestätigkeit*; the period is **extendable by individual agreement**; and where *leistungsfrei* the insurer must nevertheless pay the *Rückkaufswert* under § 169. `product-spec.md` builds its *Selbsttötung* section and its Germany/France comparison on it; `technical-notes.md` makes it the § 161 benefit switch, `suicide_years = 3`, applied to death claims only and tranche by tranche; `model.md` states the switch and its per-increment restart. **Whether the clock restarts on an increase is not established** and is `[unverified]` (gap 9)

(delib-risikolebensversicherung-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R2]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the URL and of Abs. 3's *Mindestrückkaufswert* and five-year acquisition-cost spread
- Used for: the section that decides this product by **not reaching it**. Abs. 1 confines the surrender-value duty to a life insurance whose insured event is **certain to occur**; a term assurance's is not, so there is **no statutory *Rückkaufswert***. `product-spec.md`'s termination-and-values section, `technical-notes.md`'s "no cash value anywhere" convention and `check_no_cash_value()`, and `model.md`'s statement that `claims_lapse` and `claims_maturity` are structurally zero all rest on it. **The scope limitation is asserted from knowledge of the section's structure and no search returned that wording: it is `[unverified]` and is the most consequential such tag in this product** (gap 2). Its practical result — nothing is paid on *Kündigung* — is corroborated by uniform market practice and is not in doubt

(delib-risikolebensversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung* (*Beitragsfreistellung*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R3]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the conversion right, the actuarial computation, the *Stornoabzug* and the minimum-benefit test
- Used for: the right that **exists in form and is empty in substance** on this product. The policyholder may at any time demand conversion into a *prämienfreie Versicherung* for the end of the current *Versicherungsperiode*; where the resulting benefit falls below an agreed minimum the insurer pays the *Rückkaufswert* instead — which here is nil [R2]. `product-spec.md`'s termination section states the collapse; `technical-notes.md` cites it for the absence of any paid-up state and for `claims(t, "LAPSE") = 0`. Whether § 165 carries the same *gewiss* limitation as § 169 Abs. 1 was **not established** (gap 2), and it makes no practical difference

(delib-risikolebensversicherung-r4)=

### R4 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and *Anfechtung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R5]; the `__20`, `__21`, `__22` forms are `[unverified]`
- Retrieved: **no** — egress blocked; **inherited corroboration on § 19 only**
- Used for: the whole of `product-spec.md`'s underwriting-and-rating section. § 19 Abs. 1 obliges the policyholder to disclose the *gefahrerhebliche Umstände* known to her **which the insurer has asked about in *Textform*** — **the duty is question-bounded**, with no free-standing duty to volunteer — and gives the insurer the right to accept with restrictions or only at an increased premium, which is where the *Risikozuschlag* and the individually agreed *Leistungsausschluss* come from. On a breach the insurer may **adjust the contract retrospectively** rather than refuse to perform; the remedies lapse **five years** after conclusion for negligent breach and **ten** for intentional or *arglistig* breach. The § 19 Abs. 5 warning requirement, the § 21 Abs. 2 causation defence and § 22's preservation of *Anfechtung wegen arglistiger Täuschung* are asserted and `[unverified]`. **Not cited by `technical-notes.md` or `model.md`: underwriting is a specification fact, and the model carries only its numeric residue, `rating_factor`**

(delib-risikolebensversicherung-r5)=

### R5 — VVG § 153, *Überschussbeteiligung*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R1]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the entitlement, the *verursachungsorientiert* requirement and the Abs. 3 *Bewertungsreserven* rule
- Used for: the statutory footing of the central mechanic. The policyholder is entitled to share in the surplus and in the *Bewertungsreserven*; participation may be **excluded only by express agreement**; and the allocation must be *verursachungsorientiert*. On a product whose only material surplus is the *Risikoüberschuss* and which has **no account to credit**, a cause-oriented allocation returns the RLV book's own margin **as a reduction of the premium** — which is what *Beitragsverrechnung* is. `product-spec.md`'s *Beitragsverrechnung* section, `technical-notes.md`'s derivation of `v_d`, and `model.md`'s two-premium section all rest on it, as does `surplus_form = keine`, the § 153-excluded non-participating tariff of model point 12. Participation in *Bewertungsreserven* is **structurally negligible** here `[unverified]`

(delib-risikolebensversicherung-r6)=

### R6 — VVG § 163, *Anpassung der Prämie* (the *Treuhänder* clause)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` `[unverified]`. The sibling research recorded the section as governing premium and condition adjustment in life insurance and located market commentary on the *Treuhänderklausel* [inherited: `klassische_rentenversicherung.md` R3, R17, R18]
- Retrieved: **no** — egress blocked; partial inherited corroboration of the section's subject matter
- Used for: **the single most important legal fact about the German term-life premium**, and it is a fact about what § 163 does *not* reach. The section governs increases of the ***Bruttobeitrag***, permitted only on an unforeseen and not merely temporary change confirmed by an independent *Treuhänder* — and on a German RLV that route is essentially never used, the *Bruttobeitrag* being guaranteed for the term. What moves the customer's bill is the ***Überschussdeklaration***: cutting the *Beitragsverrechnung* raises the *Zahlbeitrag* toward the *Bruttobeitrag* with **no § 163 procedure, no *Treuhänder* and no policyholder remedy**, because no guaranteed term has changed. `product-spec.md`'s asymmetry section, `technical-notes.md`'s `decl_scale` stress and `model.md`'s statement that a model carrying one premium stream cannot represent this product all cite it. That § 163 is not used in practice on RLV *Bruttobeiträge* is `[unverified]`

(delib-risikolebensversicherung-r7)=

### R7 — VVG §§ 150, 159, 162 — *versicherte Person*, *Bezugsberechtigung*, *Herbeiführung des Versicherungsfalles*
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `.../vvg_2008/__150.html`, `__159.html`, `__162.html`, canonical forms, all `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: `product-spec.md`'s three-roles paragraph, its *verbundene Leben* section and its *Über-Kreuz* section. § 150 permits insurance on the life of another and requires that person's ***schriftliche Einwilligung*** where the benefit exceeds ordinary funeral costs — the provision every *verbundene Leben* and *Über-Kreuz* arrangement runs on; § 159 governs the revocable or *unwiderruflich* *Bezugsberechtigung*, which is why the benefit reaches the beneficiary outside the estate; § 162 makes the insurer *leistungsfrei* where the policyholder intentionally and unlawfully brings about the death, and strips a beneficiary who does so. All `[unverified]`. **Not modelled**: the forfeitures are not best-estimate events

(delib-risikolebensversicherung-r8)=

### R8 — VVG § 152 (*Widerruf*), § 166 (*Beitragsverzug*), § 168 (*Kündigung*)
- Publisher / doc type: Gesetze im Internet; federal statute
- URL: `.../vvg_2008/__152.html`, `__166.html`, `__168.html`, canonical forms, all `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the exit machinery, in `product-spec.md`'s termination section and in `technical-notes.md`'s lapse and no-cash-value conventions. § 152 extends the *Widerrufsfrist* to **30 days** for life insurance, which delib absorbs into the year-one lapse rate **[std]** rather than modelling separately; § 166 requires a *Textform* demand with at least a month's deadline and converts the contract into a *prämienfreie Versicherung* rather than ending it — **unless** the paid-up benefit fails the minimum test, which here it does, so the contract simply ends [R3]; § 168 gives a termination right at the end of each *Versicherungsperiode*, and the period follows the *Zahlweise*, so **a monthly-paying contract is terminable monthly**. That last is why `technical-notes.md` names the annual grid's anniversary-only exits as its one approximation, and why the lapse assumption is argued from frictionlessness

(delib-risikolebensversicherung-r9)=

### R9 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*
- Publisher / doc type: Bundesministerium der Finanzen; federal regulation
- URL: `https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html` · `https://www.buzer.de/gesetz/12013/a198221.htm` — **both returned by a search during the sibling research** [inherited: `kapitallebensversicherung.md` R6]
- Retrieved: **no** — egress blocked; **inherited corroboration of the three percentages**
- Used for: **the engine of the German term product**, and the second load-bearing item here. The minimum allocation to the *Rückstellung für Beitragsrückerstattung* is **90 % of the *Risikoergebnis***, 90 % of the *anzurechnende Kapitalerträge* after the *Deckungsrückstellung* discounting charge, and 50 % of the *übriges Ergebnis*, computed separately for *Alt-* and *Neubestand*. An RLV's technical outcome is almost entirely *Risikoergebnis*, so **90 % of the tariff's mortality margin must go back**, and *Beitragsverrechnung* is the only route on a product with no account to credit. `technical-notes.md` derives `v_d` from it with `surplus_share = 0.90`; `model.md` names it as the reason the spread is wide and the reason the *Zahlbeitrag* is derived rather than assumed. **Section attribution is unsettled** between the sibling entry and the author's recollection, so **no MindZV section number is cited anywhere in this product's documents** (gap 4)

(delib-risikolebensversicherung-r10)=

### R10 — DeckRV, *Deckungsrückstellungsverordnung* — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Bundesministerium der Finanzen; federal regulation
- URL: `https://www.buzer.de/gesetz/12006/index.htm` — returned by a search during the sibling research, which used it for the amendment history [inherited: `kapitallebensversicherung.md` R7]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the rate history and the Zillmer cap
- Used for: the two bounds the tariff is struck inside. The ***Höchstrechnungszins*** was raised **from 0,25 % to 1,00 % with effect from 1 January 2025**, the first increase since 1994 on a sequence 4 % (1994) → 0,25 % (2022) → 1,00 % (2025); the ***Höchstzillmersatz*** may not exceed **25 ‰ of the *Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015. `technical-notes.md` sets `rechnungszins = 0.01` and `zillmer_rate = 0.025` from it and says the first **barely matters** on this product — the *Deckungskapital* is small and short-lived — while the second is why a *gezillmerte* term contract's reserve is negative for much of its term. `model.md` cites the ceiling and flags that **the composite assumes a term tariff runs at the cap**, which may well be wrong (gap 8). Whether the cap applies to a term product as to a savings contract was **not established** `[unverified]` (gap 11)

(delib-risikolebensversicherung-r11)=

### R11 — VAG §§ 138–140 — *Gleichbehandlung*, *Überschussbeteiligung*, RfB
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsaufsichtsgesetz 2016); federal statute
- URL: `https://dejure.org/gesetze/VAG/139.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R8]; the § 138 and § 140 forms are `[unverified]`
- Retrieved: **no** — egress blocked; **inherited corroboration on § 139 only**
- Used for: `product-spec.md`'s regulatory context and — the part that reaches the model — the *Gleichbehandlungsgrundsatz* of § 138, asserted and `[unverified]`: equal treatment of policyholders in equal circumstances in premium-setting and surplus allocation, which is **why an insurer declares one *Beitragsverrechnungssatz* per tariff generation and rating cell** rather than negotiating individual discounts, and therefore why `technical-notes.md` can model the *Zahlbeitrag* as a deterministic function of the *Bruttobeitrag* and a declared rate. § 139's *Bewertungsreserven* mechanics and *Sicherungsbedarf* test are recorded and are **economically empty** on this product [R5]

(delib-risikolebensversicherung-r12)=

### R12 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *DAV-Richtlinie* / *Fachgrundsatz*, with a 2008 derivation paper and a 2022 restatement
- URL: `https://aktuar.de/de/wissen/fachinformationen/detail/herleitung-der-sterbetafel-dav-2008-t-fuer-lebensversicherungen-mit-todesfallcharakter/` · `https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf` · `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf` · `https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T_R_NR.pdf` — **all returned by a search during the sibling research** [inherited: `kapitallebensversicherung.md` R14]
- Retrieved: **no** — egress blocked; **inherited corroboration**, and the third load-bearing item here
- Used for: **the mortality basis of this product.** Derived by the DAV *Arbeitsgruppe Biometrische Rechnungsgrundlagen* over **2006 to 2008** from German insurers' own policy data with German population statistics; the *Richtlinie* **regulates the derivation methodology and the procedure for setting the *Sicherheitszuschläge***, not their level; ***DAV 2008 T R*** and ***DAV 2008 T NR*** are in principle **suitable for premium calculation** differentiated by smoking status but **not for policies written without a *Gesundheitsprüfung***; adopted 4 December 2008, restated as a *Fachgrundsatz* dated 29 November 2022. From it the documents take four things: the German first-order basis is DAV 2008 T; the *Sicherheitszuschlag* is part of the table's construction, so first- and second-order are two levels of one framework and the model must publish both; the smoker split is **actuarially sanctioned for pricing**, which is why the market rates on it; and it is not available without underwriting, which is why simplified-issue German death covers are aggregate-rated. **The table values are not public and delib does not redistribute them** — `mort_table.csv` is a **[std]** proxy and `model.md` states the three anchors a replacement must preserve. **The magnitude of the loading was not established** (gap 6); the term-segment data coverage was truncated in the sibling's search summary (gap 12)

(delib-risikolebensversicherung-r13)=

### R13 — Unisex pricing: the EU Gender Directive, CJEU C-236/09 (*Test-Achats*), AGG § 20
- Publisher / doc type: Court of Justice of the European Union; Bundesministerium der Justiz; judgment and federal statute
- URL: not established for any of them
- Retrieved: **no** — egress blocked; no search corroboration. The **date** is corroborated obliquely: the frlib research reached the same cut-off independently from the French implementing article, which preserves the derogation only for contracts concluded "au plus tard le 20 décembre 2012" [`frlib` R10]
- Used for: the rule that **sex may not enter the premium for contracts concluded from 21 December 2012**, implemented in Germany through § 20 AGG, and the tension it creates with sex-distinct DAV 2008 T [R12]. `product-spec.md` states the rule and its consequence; `technical-notes.md` resolves it the only way § 138 VAG allows — the tariff blends the two tables and the projection uses the policy's own sex; `model.md`'s unisex section reports the cross-subsidy this produces between model points 1 and 2. **Every German tariff written since 2013 uses a carrier-chosen mixing ratio that no source discloses**, so `sex_mix_male = 0.50` is **[std]** and is named as one of the largest single sources of unexplained rate spread between German carriers. That female mortality at these ages is roughly half male is `[unverified]`

(delib-risikolebensversicherung-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6 and § 10 Abs. 1 Nr. 3a — income tax and premium deductibility
- Publisher / doc type: Bundesministerium der Justiz (Einkommensteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — returned by a search during the sibling research [inherited: `kapitallebensversicherung.md` R10]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the *Unterschiedsbetrag* rule, the 12/62 half-income treatment, the BMF-Schreiben of 1 October 2009 and the 50 % *Mindesttodesfallschutz* for post-1 April 2009 contracts
- Used for: **the section that does not apply**, in `product-spec.md`'s tax section. § 20 Abs. 1 Nr. 6 taxes the *Unterschiedsbetrag* on a **survival or surrender** payment, so a pure death benefit paid to a third party is not investment income of the policyholder and is **not caught**: the *Todesfallleistung* of an RLV is free of *Einkommensteuer* and the tax question moves entirely to the *Erbschaftsteuer* [R15]. The non-application is asserted and `[unverified]` (gap 16), corroborated indirectly by the *Mindesttodesfallschutz* rule, which exists precisely to stop savings contracts dressing themselves as death covers. Premiums fall among the *sonstige Vorsorgeaufwendungen* under § 10 Abs. 1 Nr. 3a within a ceiling in practice already exhausted, so the effective deduction is nil — `[unverified]`, and **no ceiling figure is stated anywhere** (gap 17). **Nothing here is modelled**

(delib-risikolebensversicherung-r15)=

### R15 — ErbStG §§ 3, 15, 16, 19 — the *Erbschaftsteuer* treatment of the death benefit
- Publisher / doc type: Bundesministerium der Justiz (Erbschaftsteuer- und Schenkungsteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/erbstg_1974/` `[unverified]`; per-section forms **not established**
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: **the only tax that reaches this product**, and the reason a German term-life specification documents a contracting structure alongside its cash flows. § 3 Abs. 1 Nr. 4 brings a *Todesfallleistung* paid to a *Bezugsberechtigter* under a contract the deceased concluded on his own life within ***Erwerb von Todes wegen***; § 15's three *Steuerklassen* put an unmarried partner in class III; § 16's *Freibeträge* run 500 000 € spouse, 400 000 € per child, 200 000 € per grandchild, 100 000 € parents, 20 000 € classes II and III; § 19's rates begin at 7 % in class I and 30 % in class III. On the representative 300 000 € the charge is nil to a spouse and of the order of **84 000 €** to an unmarried partner, which is why the *Über-Kreuz-Versicherung* exists. **Every figure is `[unverified]`** and is carried downstream as a **[std]** illustration and never as a citation (gap 18); the *structural* conclusion does not depend on them. `model.md` cites it once, to say the *Über-Kreuz* structure changes the tax outcome and **nothing in the cash flows**, so no column, cells or CSV refers to it

(delib-risikolebensversicherung-r16)=

### R16 — VersStG § 4 — *Versicherungsteuer* exemption for life insurance
- Publisher / doc type: Bundesministerium der Justiz (Versicherungsteuergesetz); federal statute
- URL: `https://www.gesetze-im-internet.de/verststg_1996/__4.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the absence of a premium-tax line. The *Versicherungsteuer* does not apply to life insurance, so a German RLV premium is billed **without insurance premium tax**, unlike a French *cotisation* quoted "TTC". `product-spec.md` states it in the premium section, `technical-notes.md` in its contractual-elements table, and `model.md` in the standardizations closing paragraph — recorded in all three **so a reader does not conclude the line was forgotten** (gap 19). That German life premiums bear no premium tax is not in doubt; the section reference is `[unverified]`

(delib-risikolebensversicherung-r17)=

### R17 — VVG-InfoV, and the PRIIP boundary for a pure protection product
- Publisher / doc type: Bundesministerium der Justiz (VVG-Informationspflichtenverordnung); federal regulation
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`. The sibling research recorded § 2 VVG-InfoV as the source of the pre-contractual information duties and of the *Effektivkosten* disclosure [inherited: `kapitallebensversicherung.md` R9]
- Retrieved: **no** — egress blocked; partial inherited corroboration of the regulation's subject matter
- Used for: the boundary this product sits on, and one of the most useful negative findings in the file. A *Basisinformationsblatt* (PRIIP-KID) is required for a **packaged retail investment product**; a pure *Risikolebensversicherung* has no investment component, is **not a PRIIP**, and none is produced for it — the applicable summary is the *Produktinformationsblatt* [S2]. Two consequences the documents state rather than leave to be discovered: the expectation of finding *Basisinformationsblätter* for this product is misplaced, and **there is no *Effektivkosten* figure for a term product, because a reduction in yield presupposes a yield**. `product-spec.md` cites it in the charges and regulatory sections and `model.md` in its charge-parameter rationale: German term-life charge levels are **structurally undisclosed, not merely unretrieved** (gap 8), which is why every charge parameter is **[std]**. Both statements `[unverified]`

(delib-risikolebensversicherung-r18)=

### R18 — GDV, *Die deutsche Lebensversicherung in Zahlen* and the *Risikoversicherung* statistics
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; annual statistical volume and a ten-year *Neugeschäft und Bestand* series
- URL: not established for the term-assurance breakdown. The sibling research located the statistics landing page and the ten-year series [inherited: `kapitallebensversicherung.md` R20, R21]
- Retrieved: **no** — egress blocked; **inherited corroboration** of the whole-market *Stornoquote* figures only
- Used for: a figure the documents **deliberately do not use**. The inherited whole-market *Stornoquote* is **2,72 % (2024)** and **2,56 % (2023)** on the main GDV measure, with a second irreconcilable measure at **1,2 % (2024)**; both are recorded in `product-spec.md`. `technical-notes.md` and `model.md` cite it to say the book average is dominated by long-dated savings contracts and is **not** the term-life lapse assumption, which is argued from structure instead and is **[std]** at 6 % / 4 % / 3 % — a listed modeling pitfall with a test of its own. **The size of the German *Risikoversicherung* segment is not established at all**: no contract count, new business, premium income, aggregate *versicherte Summe*, average sum insured, average premium or segment lapse rate (gap 13)

(delib-risikolebensversicherung-r19)=

### R19 — BaFin supervisory material on life insurance conduct and product governance
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; *Merkblätter*, *Auslegungsentscheidungen* and risk reports
- URL: not established for any term-life-specific item. The sibling research located **Merkblatt 01/2023 (VA)** *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*, published May 2023, and the *Risiken im Fokus 2026* item on the cost of *kapitalbildende* products [inherited: `kapitallebensversicherung.md` R17, R18]
- Retrieved: **no** — egress blocked; **inherited corroboration of the *Merkblatt*'s subject matter and its limit**
- Used for: a boundary, in `product-spec.md`'s regulatory context. The *Merkblatt*'s subject is expressly ***kapitalbildende*** life products and its concern is that costs be justified by customer value; **a pure *Risikolebensversicherung* is outside its stated subject matter**. It is cited so that a reader does not import an endowment-conduct standard into a term product, and so that the absence is on the record: **no supervisory literature specific to German term assurance was located** (gap 14)

(delib-risikolebensversicherung-r20)=

### R20 — Rating and analysis houses on German term-life tariff design
- Publisher / doc type: Franke und Bornberg; MORGEN & MORGEN; ASSEKURATA — the same corpus as [S17], seen from the product side; tariff ratings and market studies
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: the reference class behind two market-design facts no statute supplies, both `[unverified]` and both cited jointly with [S17] in `product-spec.md`: that the ***Brutto*/*Zahlbeitrag* spread is a rated criterion**, and that the ***Nachversicherungsgarantie* event list, caps and age limits are rated criteria**. **No rating, criterion weight or observed distribution is asserted**

(delib-risikolebensversicherung-r21)=

### R21 — HGB § 341f and RechVersV — statutory reserving for a term contract
- Publisher / doc type: Bundesministerium der Justiz (Handelsgesetzbuch; Versicherungsunternehmens-Rechnungslegungsverordnung); federal statute and regulation
- URL: `https://www.gesetze-im-internet.de/hgb/__341f.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: `technical-notes.md`'s valuation-and-reserve pointers and `model.md`'s statement that `res_pp_at` is a **pricing diagnostic and not a provision**. § 341f requires the *Deckungsrückstellung* to be computed prospectively on the bases used to determine the premium, with a prudent margin, including future administration costs where the premium-paying period is shorter than the cover period — which is exactly model point 6's situation; the RechVersV governs presentation. Both asserted and `[unverified]`. The ***Nullstellung*** question — whether a negative individual reserve arising from *Zillmerung* must be floored at zero — was **not established** (gap 11), and because no reserve of any kind enters `result_cf()` it does not reach these cash flows. **R21 is a pointer, not a model input**

(delib-risikolebensversicherung-r22)=

### R22 — Solvency II and the German prudential layer
- Publisher / doc type: EIOPA; BaFin; directive, delegated regulation and supervisory material
- URL: not established
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: a pointer only, on the same posture as [R21], in `product-spec.md`'s regulatory context and `technical-notes.md`'s valuation pointers. Nothing product-specific for German term assurance was located, and **no capital, risk-margin, contract-boundary or standard-formula stress figure appears anywhere in this product's documents**. The library publishes gross liability cash flows, undiscounted; the valuation layers consume them and are cited, never reproduced

(delib-risikolebensversicherung-r23)=

### R23 — German case law on *vorvertragliche Anzeigepflicht* and *Selbsttötung* in life insurance
- Publisher / doc type: Bundesgerichtshof and the *Oberlandesgerichte*; decided cases
- URL: not established. **No decision is cited by date or file number anywhere in this product's documents, and none is invented**
- Retrieved: **no** — egress blocked; no search corroboration
- Used for: a known reference class rather than a source. German term-life litigation clusters on whether the applicant's answers to the *Gesundheitsfragen* were complete and whether the insurer complied with the § 19 Abs. 5 warning requirement [R4], and on whether a *Selbsttötung* inside the three-year window was committed in a state excluding free will [R1]. `technical-notes.md` and `model.md` cite it for one consequence: **the mental-illness exception is the ground on which German suicide claims are actually litigated, so § 161 is not a clean contractual switch, and a best-estimate cash-flow model cannot represent that** — delib applies the rule as a benefit switch and records the exception as a known simplification. The sibling research located BGH authority on adjacent life questions — the *Stornoabzug* *Bezifferung* requirement and the *Bewertungsreserven* judgment of 20 January 2021, IV ZR 318/19 [inherited: `kapitallebensversicherung.md` R22, R23] — establishing that the court decides this area regularly and nothing about term assurance. **No holding is asserted** (gap 20)

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **Every entry in that library carries the same
retrieval status as this file**: no document was fetched, and each entry records per fact whether a
web search corroborated it before the budget was exhausted. Entries cited by the
`risikolebensversicherung` documents:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the projected cash flows feed. Nothing here computes it.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries and management actions. Cited to record that this product's boundary is *easier* than frlib's revisable one — the *Bruttobeitrag* is guaranteed for the term.
- **REG-R3** — Directive (EU) 2025/2, the Solvency II review, effective 30 January 2027: cited once, to say nothing here implements a 2027 basis.
- **REG-R6** — VAG §§ 74–110 and § 40, valuation, best estimate, risk margin and the SFCR: the German route by which Solvency II reaches this business.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the cross-product entry behind [R11], and why one declared rate applies per tariff generation and rating cell.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test: cited to say the *Bewertungsreserven* share is **economically empty** on a product whose reserve is nil or nominal.
- **REG-R10** — VAG §§ 140 and 145, the RfB: where a declared *Beitragsverrechnung* comes out of. The model's `prem_rebate` is the contract-level consequence, not the allocation itself.
- **REG-R11** — VAG §§ 141–143, *Verantwortlicher Aktuar* and *Treuhänder*: the office § 163 VVG's procedure runs through [R6], and the office that certifies the tariff bases.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the cap behind `rechnungszins = 0.01`.
- **REG-R15** — the *Höchstrechnungszins* history and the *Sechste Verordnung* of 19 July 2024 setting 1,00 % from 1 January 2025: the anchor cell's pricing rate, and the reason the notes say it **barely matters** here.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the 25 ‰ ceiling `zillmer_rate = 0.025` sits at, and half of the reason a *gezillmertes Deckungskapital* is negative for much of a term contract.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: cited to say it reaches this product **only nominally**, a reader expecting the discussion that dominates the endowment and annuity products will not find one, and that is a product fact.
- **REG-R18** — MindZV: the cross-product entry behind [R9], carrying the 90 % minimum from the *Risikoergebnis* that `surplus_share` is set to.
- **REG-R19** — RfBV, the collective part of the RfB: cited once, to say the MindZV minimum binds on the HGB accounts and is a transfer to the RfB rather than a payout.
- **REG-R20** — LVRG 2014: the reform that cut the *Höchstzillmersatz* to 25 ‰ with effect from 1 January 2015.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): the chapter this contract sits in, and the reason §§ 161, 165, 168 and 169 cannot be contracted around to the policyholder's detriment.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the 30-day window, absorbed into the year-one lapse rate **[std]** and not modelled separately.
- **REG-R24** — VVG § 153: the cross-product entry behind [R5], carrying the *verursachungsorientiertes Verfahren* and the half-share of *Bewertungsreserven*.
- **REG-R26** — VVG §§ 150, 159, 160, 161 and 162: the cross-product entry behind [R1] and [R7] — the *Einwilligung* every *verbundene Leben* and *Über-Kreuz* arrangement needs, the *Bezugsberechtigung*, and the three-year *Selbsttötung* window the model implements as `suicide_years = 3`.
- **REG-R27** — VVG § 163: the cross-product entry behind [R6], and the section the declaration cut does **not** engage.
- **REG-R28** — VVG §§ 165–170: the cross-product entry behind [R2], [R3] and [R8] — *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug*, all of which terminate in nil here.
- **REG-R29** — VVG §§ 172–177, Kapitel 6, *Berufsunfähigkeitsversicherung*: cited to place the BUZ rider outside this product and inside delib product 9.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the cross-product entry behind [R4], carrying the question-bounded *Anzeigepflicht* and the *Altersangabe* rule.
- **REG-R31** — VVG §§ 6, 7 and 7b with the VVG-InfoV: the cross-product entry behind [R17], and the source of the *Effektivkosten* duty that has **no application** to a product with no yield.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: cited for the boundary — a pure protection contract is **not** a PRIIP, so no *Basisinformationsblatt* exists for it.
- **REG-R33** — IDD and § 34d GewO: the distribution frame behind the three-channel market of the variations section.
- **REG-R34** — Unisex, CJEU C-236/09 and §§ 19, 20 and 33 AGG: the cross-product entry behind [R13], and the rule `sex_mix_male` exists to satisfy.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA): the cross-product entry behind [R19], cited for its **limit** — it is about *kapitalbildende* products and does not reach a pure protection contract.
- **REG-R36** — the BGH line of authority on German life contracts: the cross-product companion to [R23], cited for the same reason and with no holding asserted about term assurance.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6, the *Unterschiedsbetrag*, the 12/62 rule and the *Mindesttodesfallschutz*: the cross-product entry behind [R14], cited for the section's **non-application** to a pure death benefit.
- **REG-R46** — ErbStG and the SGB V contribution rules: the cross-product entry behind [R15], and the tax fact the *Über-Kreuz-Versicherung* exists to change.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the framework `mort_rate_tar` and `mort_rate` implement, and the reason the model publishes both orders.
- **REG-R48** — DAV 2008 T and its predecessors: the cross-product entry behind [R12] — **the** table for this product, cited by name and never shipped.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: cited once, to say the annuity family is **not** the basis for a death-benefit contract.
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: cited to say a population table is the **wrong starting point** for a replacement decrement basis — without a selection adjustment it overstates claims by a wide margin at the issue ages this product is sold at.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): the cross-product companion to [R18] and [R20], and the entry that records that **no term-segment figure was established**.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the cross-product entry behind [R21], and the frame in which the *Nullstellung* question sits.
- **REG-R55** — IFRS 17, effective 1 January 2023 with no German carve-out: cited once in the valuation pointers; grouping, CSM and risk adjustment are out of scope.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this model's documentation sits under.

---

## Provenance note

Extraction details — which fact would be settled by which document, the twenty mechanics sections
the product documents are actually written from, the `[std]` premium-scale construction of
mechanic 16 with its arithmetic shown, and the twenty-three-item gaps-and-caveats register — live
in `_research/risikolebensversicherung.md`. That file is the citation ground truth for the S# and
R# numbering used here, and it states these same retrieval conditions at its head.

The caveats that most constrain what these product documents can claim, in order of how much they
constrain the model:

1. **No price point of any kind was obtained — the largest gap** [S3]–[S16]. No German carrier
   publishes a rate card, the *Produktinformationsblatt* quotes the applicant's own premium, and a
   portal result is generated per query rather than published, so it would be unreachable without
   live egress in any event. **Not one *Bruttobeitrag*, *Zahlbeitrag*, spread ratio or smoker ratio
   anywhere in this product is an observation.** One published *Brutto*/*Zahlbeitrag* pair at a
   known age, sum and term would pin the *Sicherheitszuschlag* through the identity of mechanic 5
   and re-derive the whole scale.
2. **No carrier AVB was obtained** [S1] [S3]–[S13]. An AVB settles the *Nachversicherungsgarantie*
   event list and its caps, the *Kriegsklausel* wording, the smoker qualifying period, the
   *Berufsgruppen* structure, the health-question look-back periods and the medical-examination
   thresholds. **A single retrieved AVB would close most of gaps 7 and 22.**
3. **The statutory basis for the absence of a *Rückkaufswert* is `[unverified]`** [R2]. That
   § 169 Abs. 1 confines the duty to a contract whose insured event is certain to occur is asserted
   from the section's structure; no search returned that wording. The **result** — nothing is paid
   on *Kündigung* — is corroborated by uniform market practice and is not in doubt; the route is.
4. **The *Sicherheitszuschlag* level is not public** [R12], the *Richtlinie* regulating the
   procedure and not the level. It sets the *Brutto*/*Zahlbeitrag* spread almost by itself, and it
   ships as **[std]** `m = 1.25` with its calibration and sensitivity stated in full — moving it
   across 1.0 to 1.5 moves the *Bruttobeitrag* 22,5 % and the *Zahlbeitrag* 6,0 %.
5. **German term-life charge levels are structurally undisclosed, not merely unretrieved** [R17]:
   no *Effektivkostenquote*, no *Basisinformationsblatt*, and the PIB quotes premiums, not
   loadings. They would have been missing even with full egress. The **[std]** α at the 25 ‰
   Zillmer ceiling assumes a term tariff runs at the cap and **may well be wrong** [S3] [S12].
6. **No term-segment market or lapse figure exists in the corpus** [R18]. The whole-market
   *Stornoquote* is a book average dominated by long-dated savings contracts and is deliberately
   **not used**; the shipped 6 % / 4 % / 3 % is argued from structure and **no German figure
   supports any of it**.
7. **The unisex mixing ratio is proprietary everywhere** [R13]. The mechanism is law; the ratio is
   a carrier's own new-business mix, disclosed by nobody, and it moves the tariff a great deal.
8. **No case law is named** [R23] and **no BaFin material specific to term assurance was located**
   [R19]. Both absences are recorded rather than papered over, and the endowment conduct standard
   must not be imported here.
9. **Nothing here was retrieved and nothing is quoted.** The VVG, the DeckRV, the MindZV, the VAG,
   the EStG, the ErbStG and the DAV *Fachgrundsätze* are living texts, and the
   *Höchstrechnungszins* is reset by regulation. Every date, rate and paragraph number must be
   re-checked against the instrument before it is relied on. **A delib citation is a pointer, not
   a certificate.**
