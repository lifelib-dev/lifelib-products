# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/klassische_rentenversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused ids are
omitted downstream, leaving gaps; **this product has none.** All nineteen primary sources
**S1–S19** and all twenty-four product-specific references **R1–R24** are cited by
`product-spec.md`, and the subset the model itself rests on is cited again in
`technical-notes.md` and `model.md`, so the numbering below runs unbroken. No source was newly
added at drafting. Access date for all sources: **2026-08-29**. Cross-product [REG-R#] tags are
listed in their own section at the end.

**Retrieval conditions — read this before reading anything below.** Two independent limits
applied while this library was built, and they are stated here rather than glossed.

1. **Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl`
   are refused with HTTP 403 at the egress gateway for every host outside a short
   package-registry allowlist. Every host that matters for this product —
   `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`, `dejure.org`,
   `de.wikipedia.org`, and every insurer host named below (`zurich.de`, `cosmosdirekt.de`,
   `nuernberger.de`, `debeka.de`, `allianz.de`) — was tried and refused. **No document listed
   here was retrieved.** Every entry therefore reads
   `Retrieved: no — direct HTTP egress blocked in the build environment`.
2. **The only research channel was `WebSearch`**, which returns titles, URLs and search-engine
   summaries, and its session budget — shared across fourteen parallel researchers — was
   **exhausted after eighteen queries on this product**. A search summary is real evidence and
   several of the load-bearing facts below came back as near-verbatim renderings of a
   document's own sentences, but it is a *secondary summary*, never a retrieved document.

What follows from that: **a delib citation is a pointer, not a certificate.** It names the
instrument a claim should be checked against; it does not assert that anyone checked it. No
quotation anywhere in these documents was invented — where a short phrase appears in quotation
marks it is a phrase a search summary itself returned, attributed to the summary. No URL, no
document reference number, no paragraph number and no figure was guessed; where a URL was not
returned it reads `URL: not established`. `[unverified]` is used generously and keeps its normal
meaning: a specific paragraph number, effective date, tariff level or market figure that no
search result confirmed. And **every quantitative parameter of the reference implementation that
the corpus did not establish is a `[std]` standardization with a stated rationale**, never a
number attributed to a source that does not carry it. The corpus establishes the *mechanics* of
this product thoroughly and its *levels* barely at all, which is why `model.md`'s standardization
table is as long as it is.

---

## Primary product sources

(delib-klassische_rentenversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *Musterbedingungen* — the association's model general policy conditions for a deferred annuity contract, which individual insurers adopt, adapt or ignore
- URL: https://www.gdv.de/resource/blob/6294/61b4fedd6f69db77539816e3421c7eeb/allgemeine-bedingungen-fuer-die-rentenversicherung-mit-aufgeschobener-rentenzahlung-data.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries, in the result set of two independent queries
- Used for: the model wording for **exactly the product in scope**, and hence the composite representative design; that the wording family addresses *Beitragsrückgewähr*, contract values, minimum guarantees and the conditions under which the annuity is paid; and the finding that ***Beitragsrückgewähr* is the model wording's own term** rather than a marketing label, which is what lets `death_benefit_form = prem_refund` be the base design. **No paragraph numbering, clause text or page count was established** (gap 2), and none is invented downstream

(delib-klassische_rentenversicherung-s2)=

### S2 — GDV, "02 GDV-Musterbedingung LV — Rentenversicherung mit aufgeschobener Rentenzahlung" (2021 edition)
- Publisher / doc type: GDV; *Musterbedingungen*, 2021 edition of the same wording family as [S1], on the same GDV resource path (blob id 6294 in both, distinct content hashes — two editions of one family)
- URL: https://www.gdv.de/resource/blob/6294/cacd502172fab87ad8859d194d9352c8/02-gdv-musterbedingung-lv-rentenversicherung-mit-aufgeschobener-rentenzahlung-2021-data.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the disclaimer the search result returned as the document's own title line, **"Diese Bedingungen sind unverbindlich"** — the GDV wording is non-binding and its use optional, which is the argument for describing a **composite** rather than adopting one carrier's wording wholesale; and the **2021** edition date, which places the family under the 0,90 % *Höchstrechnungszins* regime and before the 1,00 % regime of 2025 [R7] [R8]

(delib-klassische_rentenversicherung-s3)=

### S3 — GDV, "Musterbedingungen" service index
- Publisher / doc type: GDV; publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the **product taxonomy that fixes this product's boundary** — separate model conditions exist for the deferred annuity [S1] [S2], for the *Basisrente* (titled by reference to § 10 Abs. 1 Nr. 2 Buchst. b Doppelbuchst. aa EStG), for a *fondsgebundene* Riester wrapper under the *Altersvorsorgeverträge-Zertifizierungsgesetz*, for a non-unit-linked variant of the same (a sibling result carried "Stand: 21.07.2025"), and for the *Hinterbliebenenrenten-Zusatzversicherung* rider [S10]. This product is the one **without** a statutory qualification clause in its title, which is the Schicht-3 placing in the product spec's scope note; and that use of the model conditions is optional

(delib-klassische_rentenversicherung-s4)=

### S4 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung, Private Vorsorge (Schicht 3) und Rückdeckungsversicherung (Schicht 2)", Fassung 01/2026
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* — the consolidated pre-contractual pack (general information, AVB, special conditions for riders and options, tax notes). Document code **521331262 2601** appears in the search result's title line
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the current-vintage anchor document of the whole corpus.** The insurer's own *Schicht 3* placing of the product and the word *konventionell* for the general-account chassis; the structure of the German pre-contractual pack, which the product spec follows; the existence of the *Dynamik* as a documented option with its own condition set, ***"Besondere Bedingungen für die Anpassungsversicherung in der Rentenversicherung"***, which is what makes `dynamik_rate` a module rather than an invention; **the conversion rule** — at the start of annuity payments a second *Rentenfaktor* is compared with the guaranteed one and **the higher of the two is guaranteed for the annuity payment period**, which is `annuity_rate_appl() = max(f_g, f_c)`; and, on *Bewertungsreserven*, that **the transition to annuity payment is a key point for participation**, that policyholders **also participate during the payout phase** (cited and deliberately *not* modelled), and the restatement that **§ 153 Abs. 3 VVG currently provides for *hälftige* participation** [R4]

(delib-klassische_rentenversicherung-s5)=

### S5 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2021 — 44 pages
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation für Konventionelle Versicherungen*, deferred annuity, private provision. Document code **521331422 1507**; title line "Seite 1 von 44"
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/330202101_aufgeschobene-rentenversicherung-private-vorsorge_verbraucherinformationen_2021_01.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the same product five years before [S4], which establishes the wording as **continuously maintained** rather than a one-off; the section list — contract partners, scope of cover, design options and the *Überschussbeteiligung* — used in the product spec's account of what the pack contains; and the § 153 Abs. 3 restatement jointly with [S4] [R4]. One document in the same result set was reported to discuss the guarantee amounts and how benefits are calculated at the end of the deferment period, but the summary did not say which, so **the pinpoint is not claimed**

(delib-klassische_rentenversicherung-s6)=

### S6 — Zurich Gruppe, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung (Konsortial)" — 46 pages
- Publisher / doc type: Zurich Gruppe Deutschland; *Verbraucherinformation*, consortium (*Konsortialversicherung*) edition. Document code **521331432 1507**; title line "Seite 1 von 46"
- URL: https://www.zurich.de/-/media-assets/project/zurich-headless/germany/docs/privatkunden/vorsorge-und-vermoegen/existenzsicherung/231_zurich_gruppe_vi_aufgeschobene_rentenversicherung_konsortial.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the product spec's variation section, and one finding only — **one carrier issues the same wording in more than one distribution wrapper**, and a wrapper difference changes the parties to the contract and **not the cash flows**, which is why the model carries no wrapper attribute

(delib-klassische_rentenversicherung-s7)=

### S7 — Zurich Deutscher Herold Lebensversicherung AG, same series, Fassung 01/2022
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, deferred annuity. Document code **521331392 2501**
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/220202101_aufgeschobene-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the chronology alone. With [S5] (2021) and [S4] (01/2026) it shows one carrier writing this product **across three *Höchstrechnungszins* regimes** [R7] [R8] [R11], which is the documentary basis for the product spec's guarantee-vintage discussion and for the model's treatment of `int_rate_guar` as a **model-point attribute**. No clause-level content is claimed from this edition

(delib-klassische_rentenversicherung-s8)=

### S8 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", LA 904 A
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Bedingungen* (AVB) for a *Rentenversicherung*, tariff code **LA 904 A**
- URL: https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the most quantitatively load-bearing document in the corpus.** The summary returned the conversion basis in terms — the annuity factor determined at the beginning of the contract is calculated on a recognised mortality table (**currently DAV 2004 R**) and an underlying interest rate (**currently 0 percent p.a.**) — which establishes three things the documents rest on: the *garantierter Rentenfaktor* is **fixed at inception**, hence `annuity_rate_guar` is a model-point attribute; the mortality basis is **DAV 2004 R** [R12] [R13]; and **an insurer may guarantee on a basis below the statutory maximum**, the *Sicherheitsabschlag* made concrete. Also the standard AVB disclaimer that the amount of profit sharing depends on influences that are unpredictable and only limitedly controllable, which is why surplus is modelled as a **declaration** and never as a guarantee; and the death benefit before *Rentenbeginn*. **The vintage of LA 904 A is not established** (gap 5), which matters because the "currently 0 percent" clause is itself time-stamped

(delib-klassische_rentenversicherung-s9)=

### S9 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301"
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**, publisher document id `gn331451_p`
- URL: https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the conversion input in one sentence** — the contract value used for annuitisation **includes any *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value stated in the general contract data** — which is `capital_conv_pp() = max(guar_capital_pp, av + av_sur + val_reserve)` and the reason the commuting policyholders receive that same amount; and the finding that the ***Rentengarantiezeit* is a tariff-level design feature carried in the product name**, not merely a rider, which is why `rgz_years` sits on the model point. No paragraph numbering established

(delib-klassische_rentenversicherung-s10)=

### S10 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung mit aufgeschobener Rentenzahlung"
- Publisher / doc type: GDV; *Musterbedingungen* for the **survivor's-annuity rider** attaching to this product
- URL: https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the finding that the market treats the **survivor's annuity as a *Zusatzversicherung* with its own condition set**, attached to the base contract rather than a benefit of it — which is why the reference implementation carries it as a **module that is off** and why it is one of the two things the corpus *does* establish for post-*Rentenbeginn* death, the other being the *Rentengarantiezeit*. No clause content established

(delib-klassische_rentenversicherung-s11)=

### S11 — Debeka Lebensversicherungsverein a. G., "Allgemeine Bedingungen für eine Rentenversicherung mit …" (B LV 85)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; AVB, house document code **B LV 85**. The title was returned truncated, so the exact product variant is **not established**
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the cleanest statement of the accumulation recursion in the corpus** — the *Deckungskapital* is the sum of the contributions accumulated at the *Rechnungszins*, **insofar as those contributions are not required for risk and expense cover**. That single sentence fixes both the premium decomposition (`prem_to_av_pp = prem_pp − charge_from_prem_pp`) and the roll-forward the model implements, and it is the source behind the technical notes' § on the *Deckungskapital*. Siblings **B LV 100 (01.07.2026)** and **B LV 101 (01.01.2025)** establish that the AVB series was being reissued as recently as **1 July 2026** (gap 9); a specimen *Nachtrag Wiederinkraftsetzung* file name establishes reinstatement as a documented process and nothing more

(delib-klassische_rentenversicherung-s12)=

### S12 — Debeka, "Privatrente" product page
- Publisher / doc type: Debeka; insurer product page
- URL: https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the **split-surplus successor design** — from the savings portion a *Deckungskapital* is formed for the guaranteed benefits while accumulation-phase surplus shares are invested in an internal fund, and **fund holdings generally receive no *Überschussbeteiligung* from the general *Sicherungsvermögen* before *Rentenbeginn*** — recorded in the product spec as a **variation, not the representative design**; the insurer's own statement that it **no longer offers the classical annuity product**, corroborating [R22] from the carrier's own page; and the annuity side of the tax choice, that a lifelong monthly annuity is taxed only on the comparatively low *Ertragsanteil* depending on age at *Rentenbeginn* [R5]

(delib-klassische_rentenversicherung-s13)=

### S13 — Allianz Lebensversicherungs-AG, "Vorsorgekonzept KomfortDynamik" / PrivatRente KomfortDynamik
- Publisher / doc type: Allianz Lebensversicherungs-AG; insurer product page, plus a distributed *persönlicher Vorschlag* specimen quotation for the BasisRente variant hosted by a broker and dated by its path to **February 2025**
- URL: https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the operational definition of the *aktueller Rentenfaktor*** — the calculation bases at *Rentenbeginn* relate to the interest rate and mortality table the company uses **at that time for immediately beginning annuities** — which is the second carrier's corroboration of the `max(f_g, f_c)` rule [S4], the reason `rentenfaktor_table.csv` is indexed by attained age at *Rentenbeginn*, and the reason an immediate-annuity document [S16] belongs in this file; the successor design that replaced the classic tariff at the market leader, with **guarantee levels of 60 %, 80 % or 90 % of premiums paid**, selectable, 80 % standard, and "only modest guarantees" at inception including **a minimum annuity**, the *garantierter Rentenfaktor* in another guise; the *Rentengarantiezeit* as a policyholder-selectable parameter with a floor; and the corpus's **only two charge figures**, an *Abschlussprovision* of 1 575 € and total costs of at most 0,95 € per 100 € of capital formed — both from third-party analyses of a **Schicht-1/Schicht-2** quotation, `[unverified]` as Schicht-3 levels, and the reason every charge in the model is `[std]`

(delib-klassische_rentenversicherung-s14)=

### S14 — Mecklenburgische Versicherungsgruppe, "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (Rente flex)
- Publisher / doc type: Mecklenburgische Lebensversicherungs-AG; *Vertragsinformationen* for the "Rente flex" private annuity. The title is truncated after "mit flexiblem", so the product's distinguishing feature — most plausibly a flexible *Rentenbeginn* — is **not established**
- URL: https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the product spec's carrier table, as a **mid-sized-mutual data point**, and for the finding that *Vertragsinformationen* is a second common name for the same pre-contractual pack [S4]. No clause content and no parameter is claimed from it

(delib-klassische_rentenversicherung-s15)=

### S15 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher / doc type: Konzern Versicherungskammer, the Bavarian public-sector insurance group (the `BL_` path prefix indicates the Bayerische Landesbrandversicherung / Bayern-Versicherung life entity); the annual **surplus-declaration document**, the instrument by which a German life insurer publishes its declared *Überschussanteilsätze* for a calendar year
- URL: https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries, which returned the title and nothing else
- Used for: the **existence and current (2026) vintage of the declaration document type** — the primary source class for every surplus rate a model of this product needs — and, just as importantly, for the disclosure that **no rate, percentage or surplus-component split was established from it** (gap 4). That is why `decl_rate_table.csv` ships a `[std]` scenario path labelled an insurer-discretionary current assumption rather than a declaration attributed to a carrier

(delib-klassische_rentenversicherung-s16)=

### S16 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation … Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* for the **immediate** annuity. Document code **521331402 2501**
- URL: https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: one structural point, in the product spec and in `model.md`'s account of the *Rentenfaktor* — because the *aktueller Rentenfaktor* of a deferred contract is taken from the carrier's **then-current immediate-annuity tariff** [S13], the immediate-annuity document is direct evidence for the deferred contract's conversion basis. It also marks the boundary with delib's `sofortrente`, whose product this is. No clause content established from this edition

(delib-klassische_rentenversicherung-s17)=

### S17 — Zurich, "Private Rentenversicherung" product page
- Publisher / doc type: Zurich Gruppe Deutschland; insurer product page
- URL: https://www.zurich.de/de-de/pk/altersvorsorge/private-rentenversicherung
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the retail presentation of the family whose conditions are [S4]–[S7], in the product spec's market-role section. **No parameter, price point or envelope was established from it**, and the entry exists partly to record that

(delib-klassische_rentenversicherung-s18)=

### S18 — Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; general pre-contractual information on a retirement-provision system. The URL's `?t=1604038997833` parameter is a millisecond timestamp corresponding to **October/November 2020**, which dates the file
- URL: https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: a further carrier in the product spec's variation table, and a second example of the *allgemeine Informationen* document type that opens the German pre-contractual pack [S4]. No clause content established

(delib-klassische_rentenversicherung-s19)=

### S19 — DEVK, "Kundeninformation zur Fondsgebundenen Rentenversicherung", 03101/07/2024
- Publisher / doc type: DEVK Lebensversicherungsverein a. G.; *Kundeninformation* for a **unit-linked** annuity, document code **03101**, **07/2024**
- URL: https://medien.devk.de/assets/content/download/produkte/altersvorsorge-leben/devk-fondsrente-kundeninfo-03101-2024-07.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the death-benefit contrast, and nothing else.** On death before *Rentenbeginn* the unit-linked benefit is the fund value at the date of death **but at least the sum of the premiums paid (*Beitragsrückgewähr*)**. That `max(account value, premiums paid)` shape is the unit-linked form of what the classic product expresses as `max(Deckungskapital, premiums paid)` or as one or the other outright — which is why `death_benefit_form = max` ships as an option and is tagged **`[std]` for the classic product**, the classic analogue being `[unverified]` (gap 18). The product itself is out of scope; it is delib's `fondsgebundene_rentenversicherung`

---

## Regulatory and actuarial references (product research numbering)

(delib-klassische_rentenversicherung-r1)=

### R1 — VVG § 169, Rückkaufswert
- Publisher / doc type: Bundesministerium der Justiz / juris (Gesetze im Internet); statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__169.html
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries returned by **eight independent mirrors** (dejure.org, buzer.de, juraforum.de, lxgesetze.de, sozialgesetzbuch-sgb.de, datenbank.nwb.de, de.wikipedia.org, and the Deutsche Rentenversicherung commentary whose path dates that version to 1 January 2016)
- Used for: the surrender machinery of `cv_pp` — that **a deduction is permitted only if it is agreed, quantified (*beziffert*) and appropriate (*angemessen*)** and that **an agreement of a deduction in respect of not-yet-amortised *Abschluss- und Vertriebskosten* is void**, which is why `surr_charge_pp` is a **flat percentage with no duration term**; that the computed value may be reduced by an agreed and appropriate *Stornoabzug* and the result is the **statutory minimum surrender value**; and that Abs. 6 permits the insurer in defined cases to reduce surrender values to be paid out, a solvency valve that is named and not modelled. The **five-year spreading** commentary associates with Abs. 3 was not returned at article level and is `[unverified]` there (gap 12); the model takes it from [REG-R28]

(delib-klassische_rentenversicherung-r2)=

### R2 — VVG § 165, Prämienfreie Versicherung (Beitragsfreistellung)
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__165.html — **returned directly by the search**, and by five further mirrors
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **both branches of the *Beitragsfreistellung* the model implements.** That the policyholder may at any time demand, for the end of the current insurance period, conversion into a premium-free insurance **provided the agreed minimum insurance benefit is reached** — the statutory right behind `pup_year` and `paid_up(t)`; that **where that minimum is not reached the insurer must instead pay the surrender value including profit shares under § 169** — the cash-out branch of `pup_cashout()` and model point 8; and that **the premium-free benefit is calculated on the calculation basis of the premium calculation, on the basis of the surrender value under § 169 paragraphs 3 to 5** — which is `pup_value_pp()`. Also the distinction the product spec draws between *Beitragsfreistellung* and *Kündigung*, and the reason a paid-up contract still bears an administration charge. The ***Mindestversicherungsleistung* threshold is not established at any carrier** (gap 22) and is `[std]` at 30,00 € a month

(delib-klassische_rentenversicherung-r3)=

### R3 — VVG § 163, Anpassung der Prämie / Bedingungsanpassung
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article. The canonical URL form is given; the article was reached in this session through commentary rather than through a statute mirror
- URL: https://www.gesetze-im-internet.de/vvg_2008/__163.html [unverified]
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the finding that § 163 VVG is **the operative statutory basis on which a German life insurer may today change a guaranteed *Rentenfaktor***, having replaced the contractual *Treuhänderklausel* route for new business [R17]; and the two triggers commentary attributes to the clause family — an unexpectedly strong increase in life expectancy, and a sustained reduction in capital-market returns. The modelling consequence is stated in `model.md`: the guaranteed factor is treated as **fixed for the life of the contract** and § 163 is recorded as a model risk rather than implemented. **The article's paragraph structure and procedural requirements were not established** (gap 6)

(delib-klassische_rentenversicherung-r4)=

### R4 — VVG § 153, Überschussbeteiligung, and § 153 Abs. 3, Beteiligung an den Bewertungsreserven
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/vvg_2008/__153.html [unverified]
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries — here, unusually, from an **insurer's restatement** [S4] [S5] rather than from a statute mirror
- Used for: the ***hälftige* participation in the *Bewertungsreserven*** that `val_reserve_pp` stands for; that the **transition to annuity payment is a key point** for it, which is why the model crystallises it at the *Rentenbeginn* and nowhere else; and that **participation continues during the payout phase**, which the model cites and deliberately does not implement. The rest of § 153 — the *verursachungsorientiertes Verfahren*, the Abs. 1 opt-out and the LVRG 2014 *Sicherungsbedarf* restriction — was not established here and is cited from the cross-product library instead

(delib-klassische_rentenversicherung-r5)=

### R5 — EStG § 22, Ertragsanteilsbesteuerung der Leibrente
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article
- URL: https://www.gesetze-im-internet.de/estg/__22.html — **returned directly by the search**
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the taxation half of the *Kapitalwahlrecht* comparison the product spec sets out and the model deliberately does not compute — that payments from private annuity contracts are taxed on the ***Ertragsanteil*** basis, that **only the "Ertrag des Rentenrechts" is taxed**, that the fraction **depends on the annuitant's age at *Rentenbeginn***, and the single value any summary returned, **18 % at age 65**. Every other age on the statutory table is `[unverified]` here (gap 8), as is the precise statutory address usually given for it

(delib-klassische_rentenversicherung-r6)=

### R6 — EStG § 20 Abs. 1 Nr. 6, taxation of a Kapitalabfindung (the 12/62 rule and the Halbeinkünfteverfahren)
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory article, reached through tax commentary rather than a statute mirror
- URL: https://www.gesetze-im-internet.de/estg/__20.html [unverified]
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries, **corroborated across five independent commentaries** (IWW *AStW*, LV 1871 [R24], Finanzküche, GN Finanzpartner and Finanztip [R20])
- Used for: the other half of that comparison — the **"12/62 rule"**, at least twelve years of contract duration and payment after completion of the 62nd year of life; that where it is met **only half the gain is taxable** (*Halbeinkünfteverfahren*), and that this applies **only to lump sums and payout-plan withdrawals, not to monthly annuity payments**; and the pre-2005 cohort rule. It is also the argued shape behind the **duration-12 step in `lapse_table.csv`**, whose levels remain `[std]`

(delib-klassische_rentenversicherung-r7)=

### R7 — Deckungsrückstellungsverordnung (DeckRV), § 2 — Höchstrechnungszins
- Publisher / doc type: Bundesministerium der Justiz / juris (instrument); Bundesministerium der Finanzen (amendment)
- URL: **not established.** No search result returned a `gesetze-im-internet.de` address for the DeckRV and none was guessed; the instrument is established instead from [R8] [R9] [R10] [R11]
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries, corroborated across five independent sources
- Used for: the definition of the *Höchstrechnungszins*, **also commonly called the *Garantiezins***, as the maximum interest rate a life insurer may guarantee on the savings portions of the premium; the increase **from 0,25 % to 1,00 % with effect from 1 January 2025**, the **first since 1994**; and — the decisive point for the model — that **the increase applies to new contracts concluded from that date onwards while existing contracts keep the rate they were written on**, which is why `int_rate_guar` is a model-point attribute and points 1, 6 and 14 credit three different rates in one run. **The full rate history is not established** (gap 7); a legacy vintage cites the cross-product library instead

(delib-klassische_rentenversicherung-r8)=

### R8 — DAV, "Deutsche Aktuarvereinigung empfiehlt auch für 2026 einen Höchstrechnungszins in Höhe von 1,0 Prozent"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; association news release
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the rate applicable to new business **at this file's access date — 1,0 %** — on the profession's own recommendation, which is the `int_rate_guar` of the eleven 2026-issue model points; and the standing recommendation mechanism, DAV recommends and the BMF legislates [R9]

(delib-klassische_rentenversicherung-r9)=

### R9 — DAV, "Deutsche Aktuarvereinigung begrüßt Ministeriumsvorstoß zum Höchstrechnungszins 2025"
- Publisher / doc type: DAV; association news release
- URL: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the process and its timing — the **November 2023** DAV recommendation and the **late-April 2024** BMF adoption for a rate effective 1 January 2025 — and hence the product spec's point that the roughly fourteen-month lead time makes the *Rechnungszins* of a tariff a **known-in-advance** pricing parameter rather than a surprise

(delib-klassische_rentenversicherung-r10)=

### R10 — GDV, media information on the Höchstrechnungszins increase (two releases)
- Publisher / doc type: GDV; two *Medieninformationen*, ids 176848 and 157548 — the lower being the earlier, pre-legislation release
- URL: https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848 and https://www.gdv.de/gdv/medien/medieninformationen/versicherer-befuerworten-anhebung-des-hoechstrechnungszinses--157548
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: industry corroboration of [R7] on the increase and its rationale, in the product spec's regulatory-context section. **No figure beyond the 1,0 % was established**

(delib-klassische_rentenversicherung-r11)=

### R11 — HDI, "Höchstrechnungszins in der Lebensversicherung steigt zum 01.01.2025"
- Publisher / doc type: HDI Lebensversicherung AG; insurer press/blog item
- URL: https://pm.hdi.de/blog/h%C3%B6chstrechnungszins-in-der-lebensversicherung-steigt-zum-01.01.2025
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: an **insurer's own** statement of the change — the *Höchstrechnungszins* under the *Deckungsrückstellungsverordnung* rising from 0,25 % to 1,00 % — with the *Bundesgesetzblatt* announcement date of **24 July**. Third independent corroboration of [R7], and the one that names the instrument

(delib-klassische_rentenversicherung-r12)=

### R12 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen" (DAV-Richtlinie)
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; **DAV-Richtlinie** (professional guideline). The file name carries **2023-06-28**, so the guideline was reissued or last revised on 28 June 2023
- URL: https://aktuar.de/content/PDF/Fachwissen/2023-06-28_DAV-Richtlinie_Herleitung_DAV2004R.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **what a replacement mortality table must preserve**, which is the whole content of the `mort_table.csv` proxy note — the component structure (base tables and mortality trends of first and second order, plus an *Altersverschiebung*), and that **first-order probabilities carry safety margins relative to the second-order ("realistic") probabilities**, which is why `mort_be_factor` is **above one** for an annuity and why the model runs two bases. The 2023 reissue is also the evidence that DAV 2004 R was still the profession's maintained annuity basis twenty years after its base year — the fact behind the longevity trigger of § 163 VVG [R3]

(delib-klassische_rentenversicherung-r13)=

### R13 — DAV, "DAV 2004 R: Stand 22.02.2005"
- Publisher / doc type: DAV; the table document itself. The returned title line reads "- 1 - DAV 2004 R: Stand 22.02.2005" and the file name carries 2005-09-14
- URL: https://aktuar.de/content/PDF/Fachwissen/2005-09-14-DAV_2004_R.pdf
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: that **DAV 2004 R is a *Generationentafel*** whose expected future improvement is **built into the table rather than applied on top of it** — the reason `mort_rate_guar(t)` depends on `calendar_year(t)` as well as `age(t)`, and the tenth listed modeling pitfall; and that it was **intended for new business from 2005**, which is the proxy's `mort_base_year`. The numeric content is **not** here and is not shipped: the DAV tables are the property of the Deutsche Aktuarvereinigung, are not public, and delib cites them by name and ships an anchored `[std]` proxy instead

(delib-klassische_rentenversicherung-r14)=

### R14 — Contemporaneous expositions of DAV 2004 R (DGVFM, Gen Re, qx-Club)
- Publisher / doc type: Deutsche Gesellschaft für Versicherungs- und Finanzmathematik in *Blätter der DGVFM* (Springer); General Reinsurance, presented to the Aktuarvereinigung Österreichs on 27 October 2004; qx-Club Berlin, 16 August 2004; qx-Club (Helmert), 14 September 2004
- URL: https://link.springer.com/article/10.1007/BF02808312 , https://www.avoe.at/archiv/nachlese-20041027.pdf , http://www.qx-club-berlin.de/material/pdf/20040816-qx-Club-Sterbetafel-DAV2004R.pdf , https://www.qx-club.de/.cm4all/uproc.php/0/Vortr%C3%A4ge/vortrag_helmert_14092004.pdf?_=173ca294dfb&cdp=a
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the **dating of the market's adoption** of DAV 2004 R, between its June 2004 first use and its 2005 general application [R13], in the product spec's *Rechnungsgrundlagen* section; and the existence of a **companion in-force table**, the *Rentenbestandstafel* RBx, established from the Helmert presentation's title and nothing more. Slide and abstract content were not established

(delib-klassische_rentenversicherung-r15)=

### R15 — Wikipedia (German), "Sterbetafel"
- Publisher / doc type: Wikimedia Foundation; general-encyclopaedia article — **secondary**, not a professional or statutory source
- URL: https://de.wikipedia.org/wiki/Sterbetafel
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: corroboration only, of the generational characterisation of DAV 2004 R [R13] — that generation tables contain mortality per birth cohort including the expected future change. **Nothing in these documents rests on it alone**

(delib-klassische_rentenversicherung-r16)=

### R16 — Finanztip, "Urteil zum Rentenfaktor: Rentenkürzung verhindern"
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; consumer-organisation article — secondary
- URL: https://www.finanztip.de/private-rentenversicherung/rentenfaktor/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: headline-level corroboration, with [R17] and [R18], of the *Treuhänderklausel* narrative in the product spec — that **a subsequent reduction of the *Rentenfaktor* can be unlawful**. It is one of the reasons the model treats the guaranteed factor as fixed rather than adjustable

(delib-klassische_rentenversicherung-r17)=

### R17 — versicherungenmitkopf.de, pages on the Treuhänderklausel, the Rentenfaktor, the Rentengarantiezeit and the Ertragsanteil
- Publisher / doc type: versicherungenmitkopf.de, an independent broker's consumer pages — secondary, and the densest such account in the corpus
- URL: https://www.versicherungenmitkopf.de/treuhaenderklausel-rentenversicherung , /rentenversicherung/rentenfaktor , /rente/rentengarantiezeit-rentenversicherung-riester-und-co , /ertragsanteilsbesteuerung , /rentenversicherung/besteuerung-private-rentenversicherung-wie-viel-bleibt-uebrig
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the ***Treuhänderklausel* story** — that insurers could previously change guaranteed *Rentenfaktoren* with an independent trustee's approval, that **the clause is now used only in older contracts and today § 163 VVG is the only route** [R3], and the two triggers; the **Landgericht Köln** holding that the low-interest phase is **entrepreneurial risk** and not a ground for adjustment, cited with the disclosure that **no case reference or decision date was established** (gap 10); and, jointly with [R24], the *Rentengarantiezeit* material — that inside the guaranteed period the instalment is due whether the annuitant lives or not, which is `pols_annuity(t)` and the fourth listed pitfall

(delib-klassische_rentenversicherung-r18)=

### R18 — Versicherungswirtschaft-heute, "Treuhänderklausel: Allianz glaubt nicht, dass Kunden einer Anpassung des Rentenfaktors erfolgreich widersprechen können" (4 February 2021)
- Publisher / doc type: Versicherungswirtschaft-heute; trade press, dated 4 February 2021 by its own URL path
- URL: https://versicherungswirtschaft-heute.de/unternehmen-und-management/2021-02-04/treuhaenderklausel-allianz-glaubt-nicht-dass-kunden-einer-anpassung-des-rentenfaktors-erfolgreich-widersprechen-koennen/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries; **body content beyond the headline was not established**
- Used for: the product spec's point that the *Treuhänderklausel* question was a **live commercial dispute at the market leader in 2021** — not a historical curiosity but a mechanic carriers were actively defending inside the window in which the current in-force book was written

(delib-klassische_rentenversicherung-r19)=

### R19 — Franke und Bornberg, "Was bedeutet der Rentenfaktor und wie hoch ist er?" and "Altersvorsorge: Überschüsse im Rentenbezug Teil 1 — Die Qual der Wahl"
- Publisher / doc type: Franke und Bornberg GmbH, an independent product-rating house; two analyst articles, the first dated 2021/2022 by its slug
- URL: https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022 and https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the professional treatment of **surplus use in the payout phase** behind the three-system taxonomy — *konstant*, *teildynamisch*, *volldynamisch* — which is `payout_system` on the model point and `annuity_sur_mth_pp`. And, negatively but importantly: **no *Rentenfaktor* level, range or table was returned** by the very article that asks "wie hoch ist er?" (gap 3), which is why every factor in the model is `[std]`

(delib-klassische_rentenversicherung-r20)=

### R20 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; two consumer-organisation articles — secondary
- URL: https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/ and https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the **three payout-phase surplus systems and their directions**, jointly with [R19] [R21] [R24] — including the finding that **under the constant system the annuity can still fall**, because the value is set from a whole-period projection and is reduced if the insurer earns less, which is why the product spec states that only the *garantierte Rente* inside it is guaranteed; and corroboration of the 12/62 rule [R6]. **No level, rate or split was established for any of the three systems**, so `sur_ann_rate`, `sur_ann_growth` and `sur_ann_theta` are `[std]`

(delib-klassische_rentenversicherung-r21)=

### R21 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher / doc type: GDV under its consumer brand *Die Versicherer*; industry-association consumer article
- URL: https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: the industry association's own account of the **payout options** — the closest thing in the corpus to an authoritative statement of the *Kapitalwahlrecht*-versus-annuity choice that `kapitalwahl_rate` parameterises — and part of the result set behind the three payout-phase surplus systems. **The notice period for exercising the *Kapitalwahlrecht* was not established from it** (gap 11), so the model treats the election as a decision at a single known date with no notice mechanic

(delib-klassische_rentenversicherung-r22)=

### R22 — Versicherungsbote, "Debeka stellt klassische Rentenversicherung ein"
- Publisher / doc type: Versicherungsbote Verlag; trade press
- URL: https://www.versicherungsbote.de/id/4842718/Debeka-Rentenversicherung-Garantiezins/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: **the market-structure fact the whole product spec has to be read against** — that Debeka would no longer sell classic annuity insurance, confirmed by a company spokesperson; that from **1 July 2016** it introduced five "Chance" tariff variants, the safest guaranteeing **0,5 % interest** and the riskiest effectively a fund policy; and that **Allianz, Zurich and Generali had already stopped distributing the classic product**. The 0,5 % figure is one of only two hard guarantee levels in the corpus and sits **below** the then-current *Höchstrechnungszins*, corroborating [S8] that a carrier may guarantee less than the cap. It is also the source of the tension with [S4] that the documents record as **unresolved** (gap 9)

(delib-klassische_rentenversicherung-r23)=

### R23 — Versicherungsjournal, "Allianz 'KomfortDynamik': Noch immer eine Rentenversicherung?"
- Publisher / doc type: Versicherungsjournal Verlag; trade press, with a cluster of companion third-party analyses in the same result set
- URL: https://www.versicherungsjournal.de/versicherungen-und-finanzen/allianz-komfortdynamik-noch-immer-eine-rentenversicherung-123163.php
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: corroboration of [S13] on the KomfortDynamik construction and the **60 / 80 / 90 % guarantee ladder**, in the product spec's account of the successor designs; and the provenance of the two Allianz charge figures, which come from this analyst cluster rather than from a tariff sheet and are therefore `[unverified]` as market-representative levels

(delib-klassische_rentenversicherung-r24)=

### R24 — Consumer and comparison-portal cluster on the Rentenfaktor, the Rentengarantiezeit, the Überschussbeteiligung and the death benefit
- Publisher / doc type: LV 1871; NÜRNBERGER; Verivox; Gabler *Versicherungslexikon* and *Wirtschaftslexikon*; Wikipedia (German); Deutsche Rentenversicherung; fragfina.de; gn-finanzpartner.de; Finanzküche; Compeon; versicherung-vergleiche.de; financedoor.de; R+V; vr.de and others — **cited collectively, because no single member is load-bearing and every fact drawn from the cluster is corroborated by at least one other member**
- URL: representative members include https://www.lv1871.de/private-rentenversicherung/fragen/todesfall/ , https://www.nuernberger.de/themenwelt/beruf-vorsorge/rentenfaktor/ , https://wirtschaftslexikon.gabler.de/definition/ueberschussbeteiligung-48786 , https://www.fragfina.de/research/rentenfaktor-check-2025/ , https://www.finanzkueche.de/blog/garantierter-rentenfaktor , https://www.compeon.de/glossar/rentengarantiezeit/
- Retrieved: no — direct HTTP egress blocked in the build environment; established from search-result summaries
- Used for: most of the **definitional** material the technical notes formalise — the *Rentenfaktor* arithmetic, `monthly annuity = capital / 10 000 × Rentenfaktor`, and the guaranteed/current distinction with its *Sicherheitsabschlag*; that the guaranteed factor is a **floor** and the current factor applies when it is higher, the other side of [S4]'s rule; the *Zinsüberschuss* definition that makes the *Rechnungszins* the **hurdle rate** of the surplus mechanism rather than merely a discount rate; the ***verzinsliche Ansammlung*** mechanics — surplus credited to an *Ansammlungsguthaben* and accrued with interest, settling **at the end of each insurance year and on termination** — which is exactly `av_sur_pp_at(t, "AFT_INT")`; the *Bonusrente* alternative; the ***Rentengarantiezeit*** durations, typical choices and cost illustration; and the **three death-benefit forms before *Rentenbeginn***, *Beitragsrückgewähr* with or without attributable surplus, the accumulated *Deckungskapital*, or a *Hinterbliebenenrente* — which are `death_benefit_form` and `db_incl_surplus`. The teaching illustration "*Rentenfaktor* 25 on 100 000 € gives 250 € a month" is arithmetic and **is not used as a market level** (gap 3)

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). Every entry in that library carries
its own retrieval status, and the same two limits of house-rules section 3 apply there. Entries
cited by the klassische-Rentenversicherung documents, and what each gave them:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the framework the undiscounted cash flows feed, named and not implemented.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: contract boundaries and the best-estimate definition, in the valuation pointers.
- **REG-R4** — EIOPA risk-free term structures: the curve a valuation layer would discount `liability_cf` on.
- **REG-R5**, **REG-R6** — VAG 2016 and §§ 74–110: the supervisory frame, the best estimate and the risk margin.
- **REG-R10** — VAG §§ 140, 145: the *Rückstellung für Beitragsrückerstattung*, the reservoir a declaration is paid out of.
- **REG-R11** — VAG §§ 141–143: the *Verantwortlicher Aktuar* and the *Treuhänder*, who signs off a declaration.
- **REG-R12** — VAG §§ 221–236 and Protektor: the *Sicherungsfonds*, in the product spec's counterparty section.
- **REG-R14**, **REG-R15** — DeckRV and the *Höchstrechnungszins* history: the article-level home of the rate whose vintage stack the model carries, and the 1,00 % of the 2026 points.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the **25 ‰ / 40 ‰ ceilings** and the *Beitragssumme* base — the two `charge_id` sets and `alpha_total_pp`.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Zinszusatzreserve* and the *Korridormethode*: cited in the reserve pointers, not modelled.
- **REG-R18**, **REG-R19** — MindZV and RfBV: the minimum allocation to the RfB and its collective part, behind the statement that a declaration is constrained rather than free.
- **REG-R20** — LVRG 2014: the reform that lowered the *Höchstzillmersatz* to 25 ‰ and restricted the *Bewertungsreserven* share.
- **REG-R21** — BaFin, the MaGo and the *Auslegungsentscheidungen*: the supervisory expectations on model governance.
- **REG-R22** — VVG 2008 and § 171 (*halbzwingende Vorschriften*): why §§ 165 and 169 cannot be contracted away to the policyholder's detriment.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: the *Widerruf* that sits inside the year-1 lapse rate.
- **REG-R24** — VVG § 153 at article level: the *Überschussbeteiligung* obligation and the *hälftige* participation, the cross-product home of [R4].
- **REG-R25** — VVG §§ 154, 155: *Modellrechnung* and *Standmitteilung*, the disclosure duties around a declaration.
- **REG-R26** — VVG §§ 150, 159–162: *Bezugsberechtigung* and *Selbsttötung*, in the product spec's benefit provisions.
- **REG-R27** — VVG § 163 at article level: the adjustment channel [R3] is read against.
- **REG-R28** — VVG §§ 165–170: the **five-year spreading of acquisition costs** the § 169 Abs. 3 floor rests on, and the *Stornoabzug* conditions — `alpha_spread_years`, `cv_floor_pp` and `surr_charge_pp`.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: *Anzeigepflicht* and *Zahlungsverzug*, which make German lapse a three-way decrement the model does not split.
- **REG-R31** — VVG §§ 6, 7, 1a, 7b, 7c and the VVG-InfoV: cost disclosure and *Effektivkosten*, none of which the corpus produced for this product.
- **REG-R33** — IDD and § 34d GewO: the distribution frame, in the product spec's market-role section.
- **REG-R34** — Unisex, EuGH C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG: **the sixteenth pitfall** — `sex` reaches the mortality basis and never the tariff.
- **REG-R35** — BaFin Merkblatt 01/2023 (VA), *Wohlverhaltensaufsicht*: the *angemessener Kundennutzen* test on charges.
- **REG-R36** — the BGH line of authority on German life contracts: the case law behind the *Zillmerung* and surrender-value discussion.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the layer architecture that places this product in Schicht 3.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Ertragsanteil* at article level, the cross-product home of [R5].
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag* and the 12/62 rule at article level — the argued shape of the **duration-12 lapse step**.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the two-basis discipline `mort_rate_guar` / `mort_rate` implements, and the licensing reason the tables are cited and not shipped.
- **REG-R48** — DAV 2008 T: named only to mark the boundary — this product's death benefit before *Rentenbeginn* is priced on the **annuity** table, which is a German peculiarity the notes state explicitly.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity tables, and what the shipped proxy must preserve of them.
- **REG-R52** — Destatis *Sterbetafeln* and *Generationensterbetafeln*, with the reuse licence: the intended base for a user-supplied replacement decrement table.
- **REG-R53** — the German life market in numbers: the only public declared-rate pair the library has (2,53 % Klassik / 2,58 % Neue Klassik for 2025), which is what the `base` declared path of 2,55 % sits inside, and the statement that **the declared rate contains the guarantee**.
- **REG-R54** — HGB §§ 341–341o, RechVersV, BerVersV: the statutory accounts the *Deckungsrückstellung* is reported in, in the reserve pointers.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: named as the measurement model a participating contract falls under, and not implemented.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard the model documentation sits under.

---

## Provenance note

Extraction details — which fact was read from which document, the section-level notes organised
by mechanic, and the **twenty-six-item gaps-and-caveats register** — live in
`_research/klassische_rentenversicherung.md`. That file is the citation ground truth for the S#
and R# numbering used here.

The caveats that most affect what these product documents can claim, in the order they bite:

- **The research budget ran out after eighteen queries** (gap 1). Whole areas the brief asked
  for — current *Rentenfaktor* market levels, charge levels, entry-age and premium envelopes, the
  2025/2026 *Überschussbeteiligung* declarations, the *Kapitalwahlrecht* notice period, the
  *Zuzahlung*, the unisex rule — are recorded as **gaps, not as facts**, and nothing was written
  to fill them.
- **No clause-level text was established from any primary document** (gap 2). Not one AVB
  paragraph number, section heading or sentence of contractual wording was returned, so **there
  is no AVB § numbering anywhere in these documents and none was invented**.
- **No *Rentenfaktor* level, range or time series was established, at any carrier, for any year**
  (gap 3), and **no *Überschussbeteiligung* rate was established either** (gap 4). Those two are
  the parameters this product turns on, which is why `rentenfaktor_table.csv` and
  `decl_rate_table.csv` ship anchored `[std]` scenario paths and say so on every row.
- **No charge parameter and no behavioural rate was established** (gaps 13, 14, 20). Every charge,
  expense, lapse and take-up level in the model is `[std]` and labelled the modeller's view.
- **The DAV tables are not public and are not redistributed** [R12] [R13] [REG-R47] [REG-R49].
  `mort_table.csv` is an anchored `[std]` proxy that keeps the generational structure and none of
  the values.
- **The annuity payment timing was not established** (gap 19), although every source calls the
  annuity monthly; the model adopts monthly-in-advance compressed onto the annual grid as an
  explicit `[std]` convention.
- ***Beitragsrückgewähr in der Rentenbezugsphase* is mentioned by no source in this corpus**
  (gap 18) and is therefore **not asserted**: `claims_death(t)` is zero for every `t` after the
  *Rentenbeginn*.
- **Zurich's status is contradictory and unresolved** (gap 9): [R22] reports it among the carriers
  that stopped distributing classic annuity insurance, while [S4] is a Zurich
  *Verbraucherinformation* for this product in the Fassung 01/2026. The documents assert neither
  reading, and the representative design is described as **the German market's reference chassis**
  rather than as a currently purchasable product.
- **Living texts** (gap 26). § 169 VVG was reached through a commentary version dated 1 January
  2016; §§ 165, 163, 153 VVG and §§ 22, 20 EStG were reached without any version date. The DeckRV
  amendment is effective 1 January 2025 and the DAV recommendation extends 1,0 % to 2026; the DAV
  2004 R derivation guideline was reissued 28 June 2023; Zurich's pack is Fassung 01/2026 and a
  Debeka AVB sibling is dated 1 July 2026. **Check every article number and every figure for later
  amendment before relying on it.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #delib-klassische_rentenversicherung-r10
[R11]: #delib-klassische_rentenversicherung-r11
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R17]: #delib-klassische_rentenversicherung-r17
[R18]: #delib-klassische_rentenversicherung-r18
[R19]: #delib-klassische_rentenversicherung-r19
[R20]: #delib-klassische_rentenversicherung-r20
[R21]: #delib-klassische_rentenversicherung-r21
[R22]: #delib-klassische_rentenversicherung-r22
[R24]: #delib-klassische_rentenversicherung-r24
[R3]: #delib-klassische_rentenversicherung-r3
[R4]: #delib-klassische_rentenversicherung-r4
[R5]: #delib-klassische_rentenversicherung-r5
[R6]: #delib-klassische_rentenversicherung-r6
[R7]: #delib-klassische_rentenversicherung-r7
[R8]: #delib-klassische_rentenversicherung-r8
[R9]: #delib-klassische_rentenversicherung-r9
[REG-R28]: #delib-reg-r28
[REG-R47]: #delib-reg-r47
[REG-R49]: #delib-reg-r49
[unverified]: #delib-unverified
<!-- END generated citation links -->
