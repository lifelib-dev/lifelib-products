# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/riester_rente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. Unused sources are omitted, so the
numbering has a gap: **R27** (the consumer, comparison and rating cluster — Stiftung Warentest /
*Finanztest*, Finanztip, the *Verbraucherzentralen*, Verivox, Check24, Handelsblatt, Morgen &
Morgen, Franke und Bornberg, Assekurata) is **not cited** by `product-spec.md` or
`technical-notes.md` and is therefore absent below. Its absence is itself the finding: that cluster
is where a normal research pass would have found the *Effektivkosten* comparisons, the
*Rentenfaktor* tables and the observed carrier spread a representative composite is built from,
**nothing from any of them was established**, and everything it would have supplied is instead a
**[std]** standardization with a stated rationale. Every other id in the research file — **S1–S16**
and **R1–R26** — is cited. Access date for all sources: **2026-08-29**. No sources were newly added
at drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

**Retrieval conditions — read this before relying on a single line below.** Two independent limits
applied while this library was built, and they are stated plainly here because a reader who picks up
this file alone has to learn them from it.

**1. Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl` are
refused with HTTP 403 at the egress gateway for every host outside a short package-registry
allowlist. Every host that matters for this product was tried and refused:
`gesetze-im-internet.de` (the AltZertG and the EStG), `bundesfinanzministerium.de` (the BMF
*Anwendungsschreiben* and the *Fokusgruppe* report), `bmas.de` (the quarterly Riester contract
statistics), `deutsche-rentenversicherung.de` (the ZfA), `bzst.de` (the certifying authority),
`bafin.de`, `gdv.de`, `aktuar.de`, `destatis.de`, `dejure.org`, `de.wikipedia.org`, and every
insurer, fund-house and bank host named below. **No document listed in this file was retrieved.
Nothing was downloaded, opened or read.**

**2. The session's `WebSearch` budget — 200 calls, shared across the parallel delib researchers —
was exhausted before this product's research file was begun.** Every search attempted for this
product returned the budget-exhausted message, so **this product had no research channel at all**:
neither retrieval nor search. Four items below are inherited from a **sibling delib research
session's** searches and say so at the point of use — the GDV *Musterbedingungen* index and its
taxonomy [S3], the "Stand: 21.07.2025" date line on the classic Riester model wording [S2], the
CosmosDirekt tariff code **LA 1005 A** [S4], and a third-party cost figure on an Allianz specimen
quotation [S5]. Everything else rests on general knowledge of German pension law, disciplined by
tagging every specific number.

**What follows from that.** Every entry records `Retrieved: no`, with the reason; **no entry
anywhere in this library says `Retrieved: yes`**. No URL, document number, edition, page count or
*Zertifizierungsnummer* was guessed: where none is available the entry says `URL: not established`,
and the three canonical `gesetze-im-internet.de` forms that do appear are marked `[unverified]`
because they are the form the host uses, not a link anyone followed. No verbatim quotation of any
document is given; German phrases in quotation marks are **terms of art**, not quotations. And
`[unverified]` is used generously in the product documents: every paragraph number, effective date,
monetary amount, percentage and threshold there is a claim no search corroborated. **A delib
citation is a pointer, not a certificate.** It names the instrument a claim should be checked
against; it does not assert that anyone checked it.

---

## Primary product sources

Sixteen known references in four families: the **GDV model conditions** [S1]–[S3]; the **insurance
wordings** [S4]–[S8] and [S16], which are the product this model represents; the **fund and bank
wordings** [S9]–[S12], the same subsidy on a different chassis; and the **Wohn-Riester** documents
[S13], the boundary of scope. [S14] and [S15] are the statutory disclosure and certification
artefacts every one of the others carries. They are listed because a source list's job is to name
the documents a downstream claim must be checked against, and because the *kinds* of document that
exist here are themselves a finding: German Riester disclosure is split across four — the **AVB**,
the **Produktinformationsblatt**, the **Verbraucherinformation** pack and the **jährliche
Information**.

(delib-riester_rente-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die fondsgebundene Rentenversicherung nach dem Altersvorsorgeverträge-Zertifizierungsgesetz" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *Musterbedingungen* — model general policy conditions for a **unit-linked** Riester annuity, non-binding and optional in use
- URL: not established
- Retrieved: no — direct HTTP egress blocked in the build environment; existence and title family established from a **sibling delib session's** search of the GDV index [S3]; no search corroboration in this session (budget exhausted)
- Used for: the proposition in `product-spec.md` that the association drafts an AltZertG condition set for the **unit-linked** wrapper, which places the *fondsgebundene* Riester chassis outside this model and inside `fondsgebundene_rentenversicherung`; and, in the four-chassis table, the identification of the unit-linked form's provider and guarantee mechanism. **No paragraph numbering, clause text, edition or page count is established and none is used**

(delib-riester_rente-s2)=

### S2 — GDV, non-unit-linked ("klassische") Riester model conditions, "Stand: 21.07.2025"
- Publisher / doc type: GDV; *Musterbedingungen* for the **general-account** variant of the same AltZertG wrapper — the direct template for the product this model represents
- URL: not established
- Retrieved: no — egress blocked; the **"Stand: 21.07.2025"** date line was returned to a **sibling delib session's** search of the GDV index [S3] and is recorded on that authority; no search corroboration in this session
- Used for: the two load-bearing propositions of the product spec's overview — that the classic Riester chassis was still being drafted by the industry association **after** the *Höchstrechnungszins* rose to 1,00 % on 1 January 2025 [R22], so the guarantee became financeable again at exactly the moment the wording was refreshed; and that the classic and unit-linked Riester wrappers are **separate condition sets**, so a delib model of the classic form models a real, separately drafted contract type rather than a simplification. **No clause content is established**

(delib-riester_rente-s3)=

### S3 — GDV, "Musterbedingungen" service index
- Publisher / doc type: GDV; publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen — **returned by a search in a sibling delib research session**, not by one run for this product
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the German product taxonomy used in the scope notes of `product-spec.md` and `technical-notes.md` — that separate model conditions exist for the Schicht-3 deferred annuity, the *Basisrente*, the AltZertG unit-linked wrapper [S1], its non-unit-linked variant [S2] and the *Hinterbliebenenrenten-Zusatzversicherung* rider; and for the observation that **the association names the Riester product by its certification statute, not by its benefit**

(delib-riester_rente-s4)=

### S4 — Cosmos Lebensversicherungs-AG (CosmosDirekt), Riester-Rentenversicherung AVB, tariff **LA 1005 A**
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Bedingungen* for a Riester annuity, tariff code **LA 1005 A**
- URL: not established
- Retrieved: no — egress blocked; the tariff code and its identification as the house's Riester wording were returned to a **sibling delib session's** search of the Cosmos AVB series and are recorded on that authority; no search corroboration in this session
- Used for: the only carrier fact in the product spec's variation section that is a fact at all — that a named Riester wording exists and sits in a **separate tariff family** from the same house's Schicht-3 annuity (LA 904 A, LA 1204 A / LA 1201 A) and *Basisrente* (LA 1100 A), so the Riester contract is not a rider on a Schicht-3 tariff. **Whether LA 1005 A strikes its guaranteed *Rentenfaktor* the way the same house's Schicht-3 wording does is not established** and is not asserted (gap 9)

(delib-riester_rente-s5)=

### S5 — Allianz Lebensversicherungs-AG, the *RiesterRente* product family
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; insurer product pages and the associated *Verbraucherinformation* / AVB packs. **The current product names, their tariff codes and which remain open to new business are not established** (gap 12)
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the market-leader comparator in the variation section, and for the **single quantitative charge datum anywhere in this corpus** — total costs of at most **0,95 € per 100 €** of capital formed in a *RiesterRente* variant, inherited from a **sibling delib session's** search of third-party commentary on a specimen quotation. Both the product spec and the technical notes use it only to say that it is *not enough to found a charge basis*: it is third-party commentary rather than a tariff sheet, and **every charge in this product's documents is therefore [std]** (gap 13)

(delib-riester_rente-s6)=

### S6 — Debeka Lebensversicherungsverein a. G., Riester-Rentenversicherung
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; AVB and product documentation for a Riester annuity
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the proposition in the variation section that a Debeka Riester wording is the most likely place in the German market to find the **classic** chassis still being written — the house being the largest writer of classically guaranteed life business and its membership heavily weighted to *Beamte*, who are *unmittelbar zulageberechtigt* [R7]. **No document, tariff code, vintage or clause is established**, and no parameter cites it for a level

(delib-riester_rente-s7)=

### S7 — R+V Lebensversicherung AG, Riester-Rentenversicherung
- Publisher / doc type: R+V Lebensversicherung AG, Wiesbaden; AVB and product documentation for a Riester annuity
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the cooperative-sector comparator, and specifically the observation that this is the one group whose Riester offering spans an insurance and a fund chassis in the **same** distribution network as [S9] — which is why the product spec can set the two chassis side by side without comparing across distribution models. **No document, tariff code, vintage or clause is established**

(delib-riester_rente-s8)=

### S8 — Alte Leipziger Lebensversicherung a. G., Riester-Rentenversicherung
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB and product documentation for a Riester annuity in a classic and a unit-linked form
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the broker-market comparator in the variation section, and for the proposition that a single house commonly writes both the classic and the unit-linked Riester form. **No document, tariff code, vintage or clause is established**; the house's product naming convention is `[unverified]` and is not reproduced

(delib-riester_rente-s9)=

### S9 — Union Investment, *UniProfiRente* and *UniProfiRente Select*
- Publisher / doc type: Union Investment Privatfonds GmbH, Frankfurt am Main; *Vertragsbedingungen* plus the statutory *Produktinformationsblatt* [S14] for a **Riester-Fondssparplan**
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the product spec's four-chassis table and its account of how the fund industry meets the same 100 % *Beitragsgarantie* — a **rule-based reallocation between an equity fund and a bond fund** — and of the **cash-lock** pathology that creates, which is the fund-chassis form of the problem the classic chassis meets through the *Deckungskapital*. **The reallocation rule, the fund names, the fee levels and the new-business status are not established** (gaps 11, 12)

(delib-riester_rente-s10)=

### S10 — DWS Investment GmbH, *DWS RiesterRente Premium* / *DWS TopRente*
- Publisher / doc type: DWS Investment GmbH (Deutsche Bank group), Frankfurt am Main; *Vertragsbedingungen* plus *Produktinformationsblatt* [S14] for a Riester-Fondssparplan
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the second of the three large Riester fund savings plans in the four-chassis table, on the same guarantee-by-reallocation principle as [S9], and for the product spec's statement that the fund houses' withdrawal from sale is part of what closed the Riester market. **No document, edition, fee level or new-business status is established**

(delib-riester_rente-s11)=

### S11 — Deka, *DekaBonusRente*
- Publisher / doc type: DekaBank Deutsche Girozentrale / Deka Investment GmbH, Frankfurt am Main; *Vertragsbedingungen* plus *Produktinformationsblatt* [S14] for a Riester-Fondssparplan
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the third of the three fund savings plans, distributed through the *Sparkassen*; same chassis, same guarantee problem, same caveats. **No document, edition or fee level is established**

(delib-riester_rente-s12)=

### S12 — Riester-Banksparplan *Vertragsbedingungen* (Sparkassen; Volks- und Raiffeisenbanken)
- Publisher / doc type: individual *Sparkassen* and cooperative banks — there is no single national product; deposit-contract terms for a certified Riester savings plan, typically a reference-rate-linked interest with a duration bonus scale
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the analytical control case in the product spec's guarantee argument — the one certified chassis on which the 100 % *Beitragsgarantie* costs **nothing**, because a deposit balance cannot fall below the sum of deposits, which isolates the guarantee's cost as the **return forgone** rather than as a capital charge. **No individual product, rate scale, bonus scale or provider is established**

(delib-riester_rente-s13)=

### S13 — Wohn-Riester documents: Riester-*Bausparvertrag* and Riester-*Darlehen*
- Publisher / doc type: the *Bausparkassen* — Schwäbisch Hall, LBS, Wüstenrot, BHW and others; *Allgemeine Bedingungen für Bausparverträge* in a certified Riester form, and loan agreements certified as an *Altersvorsorgevertrag* in the form of a *Darlehen* [R3]
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the scope boundary in both product documents — that the delib model's exclusion of Wohn-Riester excludes **real, certified, subsidy-drawing products** rather than a curiosity, and that a contract counted as "Riester" in an official statistic may be a mortgage [R19], so this model's contract count is not comparable with a published one without adjustment. **No document, edition, rate or fee is established**

(delib-riester_rente-s14)=

### S14 — *Produktinformationsblatt* under § 7 AltZertG, in the form prescribed by the *Altersvorsorge-Produktinformationsblattverordnung* (AltvPIBV)
- Publisher / doc type: every certified provider must issue one; the form is prescribed by statute and regulation, and the *Chancen-Risiko-Klasse* is assigned by the *Produktinformationsstelle Altersvorsorge*. Standardised pre-contractual comparison sheet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: the product spec's charges section and its disclosure section — that the **Effektivkosten** are computed individually for each contract offer and disclosed on a sheet standardised so that an insurance annuity, a fund savings plan and a bank savings plan produce the *same* sheet; that this is the document a real parameterisation of the model's charge basis would be read from; and that reproducing the disclosed **Chancen-Risiko-Klasse** would need the PIA's scenario set, which is neither public nor in scope. **No individual sheet was seen; no *Effektivkosten* figure, no CRK assignment and no model-case specification is established** (gap 13)

(delib-riester_rente-s15)=

### S15 — *Zertifizierungsbescheid* and *Zertifizierungsnummer*
- Publisher / doc type: the certifying authority — the **Bundeszentralamt für Steuern**, which took the function over from the BaFin `[unverified]` as to the date; the administrative decision certifying a contract type, whose number every certified product carries
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: two structural propositions of the product spec's identity table — that **certification attaches to the contract type, not to the individual policy**, so a provider certifies a tariff and then sells it; and that **certification is expressly not a quality judgement** [R2], which is why no delib document describes a Riester product as state-guaranteed or state-approved in any broader sense. **No certification number appears anywhere in this product's documents**

(delib-riester_rente-s16)=

### S16 — The second tier of Riester insurance wordings
- Publisher / doc type: Stuttgarter; NÜRNBERGER; Continentale; HUK-COBURG; Volkswohl Bund; LV 1871; Hannoversche; Barmenia; Gothaer; Signal Iduna; Provinzial; DEVK; Universa; ERGO; AXA; Swiss Life; Zurich Deutscher Herold; Baloise; Württembergische; HDI; Generali/Dialog — AVB, *Verbraucherinformationen* and *Produktinformationsblätter* for Riester annuities
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session
- Used for: one proposition only — that a body of carrier wordings exists, and that a single life is the base design with a survivor's benefit written as a rider rather than as a second life. The entry is deliberately not split per carrier because **nothing carrier-specific was established for any of them** (gap 12), and the product spec states in terms that **no parameter may cite [S16] for a level**

---

## Regulatory and actuarial references (product research numbering)

Twenty-six known references, [R1]–[R26]. The same retrieval statement applies to every one: **no
document was retrieved and no search was run for this product.** The statutory URLs given in
canonical `gesetze-im-internet.de` form are marked `[unverified]` — they are the form the host uses,
not a link anyone followed. The content each entry supports is stated in the product documents in
this library's own words, from general knowledge of German pension law, with every paragraph number,
date and figure tagged `[unverified]`.

Two structural points, stated once. **The product is defined by two statutes doing different jobs**:
the AltZertG says what a contract must contain to be certifiable, the EStG says who gets what
subsidy and how the benefit is taxed — a *product* rule is in the first, a *money* rule in the
second. And **no supervisory instrument sets Riester tariff levels**: the *Höchstrechnungszins*
[R22] binds the guarantee's discount rate and nothing else, while charges, *Rentenfaktoren* and
surplus are unregulated as to level and are disclosed rather than capped [R4] [R5].

(delib-riester_rente-r1)=

### R1 — AltZertG § 1, the criteria of a certifiable *Altersvorsorgevertrag*
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: https://www.gesetze-im-internet.de/altzertg/__1.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Used for: **the operative product statute, and the single most-cited reference in both documents.** It carries the earliest *Rentenbeginn* (completed 62nd year for a contract concluded from 2012, 60th before), which bounds `rentenbeginn_age` and is the boundary model point 13 sits on; the **Beitragserhaltungszusage** itself, which is `guar_pp` and `capital_conv_pp`; the lifelong constant-or-rising annuity form, which is why the projection does not stop at conversion; the **30 %** *Teilkapitalauszahlung* cap, which is `teilkapital_cap`; the **five-year** floor under acquisition-cost spreading, which is `acq_charge_years`; the *Wechselrecht* that makes `transfer_rate` a separate decrement; the unisex requirement; and the exclusion of biometric-rider contributions from the guarantee, capped as a share of total contributions, which is `guar_carve_out_pp`. Every specific in that list is `[unverified]`

(delib-riester_rente-r2)=

### R2 — AltZertG §§ 2, 3 and 5, certification and the certifying authority
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the product spec's insistence that certification is an administrative act confirming that a contract's **terms** satisfy the § 1 criteria and is **not** a statement about the provider's financial standing, its charges or its expected return — hence that the *Beitragsgarantie* is the **provider's own** and its ability to honour it is an ordinary solvency question, and that no delib document may call the product state-guaranteed

(delib-riester_rente-r3)=

### R3 — AltZertG § 1 Abs. 1a, the *Altersvorsorgevertrag* in the form of a *Darlehen*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the statutory hook behind the Wohn-Riester exclusion — that certification is available to a **loan** used to acquire owner-occupied residential property and to a *Bausparvertrag* combining the two, which is why "Riester" in German usage covers a mortgage as well as an annuity and why the delib documents must say which of the four chassis they represent

(delib-riester_rente-r4)=

### R4 — AltZertG §§ 7 ff., the *Produktinformationsblatt*, *Effektivkosten* and *Chancen-Risiko-Klassen*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the disclosure regime described in the product spec's charges and regulatory sections — the standardised sheet [S14], the **Effektivkosten** as a reduction in yield, and the **Chancen-Risiko-Klasse** on a 1-to-5 scale assigned by the *Produktinformationsstelle Altersvorsorge* from a common capital-market model rather than the provider's own projection; and for the observation that a 100 %-guaranteed product sits at the low-risk end of that scale by construction. It is also the reference behind the statement that charges are **disclosed rather than capped**

(delib-riester_rente-r5)=

### R5 — *Altersvorsorge-Produktinformationsblattverordnung* (AltvPIBV)
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the proposition that the *form* of the sheet — its model cases, contribution and term assumptions, return scenarios and the presentation of the *Effektivkosten* — is prescribed by regulation, so it is the instrument a delib charge basis would be calibrated **against**; and, in the variation table, that the disclosure format varies not at all across carriers while the disclosed values vary and none was established

(delib-riester_rente-r6)=

### R6 — EStG § 10a, the *Sonderausgabenabzug* and the *Günstigerprüfung*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__10a.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration
- Used for: the second subsidy route — contributions **together with the Zulagen** deductible up to **2 100 €** a year, a ceiling **not raised since 2008** and therefore nominal for two decades, which the product spec uses as a substantive fact about the product's decline; the automatic *Günstigerprüfung* granting the **larger** of the two benefits and not their sum; and the rule that a *mittelbar* eligible spouse has no § 10a deduction of their own. The technical notes cite it for **why the model has no cells for any of this**: only the Zulage reaches the policy, and the § 10a advantage is a personal tax refund (pitfall 5)

(delib-riester_rente-r7)=

### R7 — EStG § 79, who is *zulageberechtigt*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the eligibility rule that decides whether a model point can hold this contract at all — the *unmittelbar* list (compulsory members of the statutory pension insurance, *Beamte* and equivalent office-holders, farmers, *Arbeitslosengeld* recipients, parents in *Kindererziehungszeiten*, full *Erwerbsminderungsrentner*, *geringfügig Beschäftigte* who waived the exemption); the *mittelbar* derivation from a spouse, conditional on an own contract and the 60 € *Sockelbeitrag*, which is model point 5; and the exclusion of the self-employed outside compulsory insurance and of *Versorgungswerk* members, which is why delib carries `basisrente` as a separate product and why the two are complements rather than competitors. Also for the statement that eligibility is **annual and can change**, so it is an attribute of the saver rather than of the policy

(delib-riester_rente-r8)=

### R8 — EStG §§ 82 and 83, *Altersvorsorgebeiträge* and the *Altersvorsorgezulage*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the definitional claim the whole reporting design rests on — **the Zulage is a contribution, not a benefit**: it is paid to the provider, credited to the contract, counted in the *Beitragsgarantie*, invested, and taxed at the end like any other contribution, and it never reaches the saver's bank account. That is why `zulagen` is a separate positive income column of `result_cf()` and is never folded into `premiums` (pitfall 4); and, on the Wohn-Riester side, why *Tilgungsleistungen* on a certified loan count as subsidised contributions

(delib-riester_rente-r9)=

### R9 — EStG § 84 (*Grundzulage*, *Berufseinsteiger-Bonus*) and § 85 (*Kinderzulage*)
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: every Zulage amount in the model — *Grundzulage* **175,00 €** from contribution year 2018 (154,00 € 2008–2017, phased in from 38,00 €); the once-in-a-lifetime **200,00 €** *Berufseinsteiger-Bonus* for a saver under 25, which is model point 6; and the **185,00 € / 300,00 €** *Kinderzulage* split by whether the child was born before or from 1 January 2008. That split is a permanent **birth-cohort** rule rather than a transition, so a contract can draw both rates at once — model point 3, at 175 + 185 + 300 = 660,00 € — which is pitfall 6. Also for the fact that the *Kinderzulage* runs only while *Kindergeld* is drawn, which makes the Zulage stream a **falling step function** driven by a household variable the insurance contract does not observe, and hence why `zulage_schedule.csv` is an exogenous per-model-point schedule. All amounts `[unverified]`

(delib-riester_rente-r10)=

### R10 — EStG §§ 86 and 87 (*Mindesteigenbeitrag*, *Sockelbeitrag*)
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the contribution engine — `M(t) = max(60, min(0.04 × Y(t), 2 100) − Z*(t))`, with the **4 %** rate, the **2 100,00 €** ceiling and the **60,00 €** *Sockelbeitrag* floor all `[unverified]`; the **proportional** Kürzung, which reduces the Zulage in the ratio of the contribution paid to the minimum rather than withdrawing it, and which is model point 7 and pitfall 3; and the rule that the reference income is the **previous** calendar year's, which is the first of the model's two lags (pitfall 1). It also carries the product spec's worked *Mindesteigenbeitrag* cases, including the 60,00 €-for-775,00 € leverage of the low-income case that model point 4 reproduces

(delib-riester_rente-r11)=

### R11 — EStG §§ 89 to 91, and the *Zentrale Zulagenstelle für Altersvermögen* (ZfA)
- Publisher: Gesetze im Internet; Deutsche Rentenversicherung Bund
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the model's **timing** — that the saver applies through the provider, normally once by a *Dauerzulageantrag*; that the **ZfA** determines entitlement by matching the provider's data against earnings and *Kindergeld* data and then **pays the provider**, who credits the contract; and that a credit is therefore **provisional** and reversible. From this comes `zulage_pp(t) = zulage_granted_pp(t − 1)`, the second of the two lags, and the `zulage_init_pp` column that exists only because an in-force point opens owing one Zulage. **Neither the payment month nor the reversal frequency is established** (gap 6), so the one-year lag is a **[std]** convention. It also carries the ZfA administration inside the per-policy maintenance expense

(delib-riester_rente-r12)=

### R12 — EStG § 22 Nr. 5, the taxation of the benefit
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__22.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration
- Used for: the *nachgelagerte Besteuerung* rule that makes this a Schicht-2 product — benefits from the **subsidised** pool taxed in full as *sonstige Einkünfte* with **no** *Ertragsanteil*, so a Riester annuity is worth materially less to the saver than a Schicht-3 annuity of the same gross amount; the **two contribution pools** a single contract can carry at once, which is `pool_gefoerdert_pp` beside `pool_ungefoerdert_pp` and model point 8; the annual *Leistungsmitteilung* apportioning between them, which the model explicitly does **not** attempt for investment return; and the asymmetry that makes the *Teilkapitalauszahlung* taxable in full in its year while the *Kleinbetragsrenten-Abfindung* gets the *Fünftelregelung* [R15]

(delib-riester_rente-r13)=

### R13 — EStG §§ 92a and 92b, Wohn-Riester and the *Wohnförderkonto*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the informed exclusion of Wohn-Riester from the model — the *Altersvorsorge-Eigenheimbetrag* as a withdrawal that is **not** *schädliche Verwendung*, and the *Wohnförderkonto* as a **notional account carrying no cash whatsoever**, accruing a statutory notional rate and taxed in the payout phase. Both documents give this as the reason the housing route is out of scope: there is no liability and no cash flow to project, while from the insurer's side an *Eigenheimbetrag* is simply an early full-value exit, which the model does not implement either and says so

(delib-riester_rente-r14)=

### R14 — EStG §§ 93, 94 and 95, *schädliche Verwendung* and its consequences
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the reason a Riester surrender is not an ordinary surrender — a *Kündigung* repays **all** Zulagen and **all** § 10a relief (the *Rückzahlungsbetrag*) and makes the growth on the subsidised part taxable, which is the argument behind a `lapse_rate` set materially below a Schicht-3 one; the list of uses that are **not** *schädlich*, from which the model's option set is built — *Anbieterwechsel*, *Versorgungsausgleich*, *Eigenheimbetrag*, the *Kleinbetragsrenten-Abfindung*, and transfer to a surviving spouse's own certified contract; and the convention that benefits are published **gross** of the *Rückzahlungsbetrag*, because the provider's withholding is a tax collection and not a reduction in the insurer's obligation (pitfall 18). Its § 95 limb is cited only to record that the emigration rule is **not established** (gap 15)

(delib-riester_rente-r15)=

### R15 — EStG § 93 Abs. 3 with SGB IV § 18, the *Kleinbetragsrente*; EStG § 34, the *Fünftelregelung*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the commutation the model computes rather than assumes — the trigger at **1 % of the monthly *Bezugsgröße*** of § 18 SGB IV, which the documents render as **39,55 €** a month against a competing 1,5 % reading of **59,33 €** that cannot both be right; the fact that an *Abfindung* is **not** *schädliche Verwendung*, so no subsidy is repaid; and the *Fünftelregelung* and deferral election that apply to it but not to the *Teilkapitalauszahlung*. It is why `is_kleinbetrag()` exists at all, and why model points 4, 5, 10 and 13 pay `claims_commutation` instead of a lump sum and an annuity. **The threshold for any specific year is not established** (gap 7)

(delib-riester_rente-r16)=

### R16 — EStG § 97, non-transferability and protection from execution
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: two behavioural propositions in the technical notes — that the subsidised capital cannot be assigned as loan collateral, which removes a use a Schicht-3 endowment has; and that it is protected from attachment within limits, so a saver in difficulty cannot realise the contract as easily as a Schicht-3 one. Both feed the argument for a low `lapse_rate` and for *Beitragsfreistellung* being the characteristic exit rather than surrender

(delib-riester_rente-r17)=

### R17 — *Altersvermögensgesetz* (AVmG) and *Altersvermögensergänzungsgesetz* (AVmEG), 2001
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the founding statutes in the product spec's market-role section — that the same reform **reduced the future replacement rate of the statutory pension** and **created a subsidised private product to fill the gap**, which is the whole political logic of the product; and for the four two-step phase-in of the *Mindesteigenbeitrag* percentage (1 % / 2 % / 3 % / 4 %) and of the Zulagen to 2008

(delib-riester_rente-r18)=

### R18 — *Alterseinkünftegesetz* (AltEinkG), 2004
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the **three-layer taxonomy** every delib scope note uses — Schicht 1 *Basisversorgung*, Schicht 2 *Zusatzversorgung*, Schicht 3 *Kapitalanlageprodukte* — and for the placing of this contract in **Schicht 2**: relieved on the way in and taxed in full on the way out, alongside the *betriebliche Altersversorgung*, which is what distinguishes it from `klassische_rentenversicherung` on the same chassis

(delib-riester_rente-r19)=

### R19 — *Eigenheimrentengesetz* (EigRentG), 2008
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the creation of Wohn-Riester [R13] and of the certifiable loan [R3], and for the 300 € *Kinderzulage* rate for children born from 2008 that produces the permanent two-rate split [R9]; and, in the product spec's market section, for the warning that a material minority of "Riester contracts" in an official count are housing contracts that will never pay an annuity, so a contract count is not an annuity count

(delib-riester_rente-r20)=

### R20 — *Altersvorsorge-Verbesserungsgesetz* (AltvVerbG), 2013
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the administrative reform — the standardised *Produktinformationsblatt* [R4] [S14]; the **cap on the provider's charge for a *Wechsel***, which is why the model's flat 50,00 € transfer charge is a **[std]** value under a real but unestablished statutory ceiling (gap 8); and the **60 € *Sockelbeitrag* for a *mittelbar* eligible spouse**, which closed the zero-contribution entitlement and is the rule model point 5 sits on

(delib-riester_rente-r21)=

### R21 — *Betriebsrentenstärkungsgesetz* (BRSG), 2017
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the last substantive Riester reform — the *Grundzulage* raised from 154 € to **175 €** from contribution year 2018 [R9]; the *Kleinbetragsrenten-Abfindung* brought under the *Fünftelregelung* with a deferral election [R15]; the *Freibetrag* in the *Grundsicherung im Alter*, which repaired the product's sharpest design criticism; and the removal of the double *Krankenversicherung* charge on a Riester annuity drawn from a bAV vehicle. The product spec's reading of the set — **every one a repair to a criticism rather than an extension, and none of them touching the *Beitragsgarantie*** — rests on this entry

(delib-riester_rente-r22)=

### R22 — *Deckungsrückstellungsverordnung* (DeckRV) § 2, the *Höchstrechnungszins*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; the two recent values are corroborated in **sibling** delib research files from their own searches and are cited here on that authority
- Used for: the two values that matter to this product — **0,25 %** in force from 1 January 2022 and **1,00 %** from 1 January 2025 — which set the anchor's `rechnungszins` and the older model point 3's, and which carry the whole of the product spec's guarantee argument: the fraction of a contribution immobilised to back a nominal guarantee is `(1 + i)^−n`, so the 0,25 % regime left under 4 % of a thirty-year contribution for charges and risk assets, which is why new Riester business stopped, and the 2025 rise roughly quadrupled that headroom. The earlier rate sequence is `[unverified]` and belongs to [REG-R15]

(delib-riester_rente-r23)=

### R23 — Unisex pricing: the AltZertG rule and *Test-Achats*
- Publisher: Gesetze im Internet; Court of Justice of the European Union
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the rule that Riester contracts have been **unisex since 1 January 2006** by the AltZertG itself, six years before the general German market followed *Test-Achats* on 21 December 2012 — hence that `sex` is a reporting-only model point column that no rate in the model may read, and that a Riester *Rentenfaktor* is **not** comparable with a contemporaneous Schicht-3 one for a male life. The 2006 date, the case number and the judgment date are all `[unverified]`

(delib-riester_rente-r24)=

### R24 — BMF *Anwendungsschreiben* on the tax treatment of subsidised private pensions
- Publisher: Bundesministerium der Finanzen
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: nothing substantive. It is cited once, in the product spec, to record that the consolidated administrative guidance German practitioners actually work from — on the *Günstigerprüfung*, the two-pool tracking, the *Rückzahlungsbetrag* calculation and the *Wohnförderkonto* arithmetic — **was not identified, and its date, reference number and content are not established** (gap 3). Naming it is what makes the `[unverified]` tags on those mechanics locatable rather than vague

(delib-riester_rente-r25)=

### R25 — Riester contract statistics: BMAS quarterly series; GDV statistics
- Publisher: Bundesministerium für Arbeit und Soziales; Gesamtverband der Deutschen Versicherungswirtschaft
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the market section's order-of-magnitude statements — the contract count and its split by chassis, the collapse of new business, and the large minority of the book that is *beitragsfrei gestellt*, which is the fact behind the technical notes' decision to carry *Beitragsfreistellung* as a model-point switch and to warn that a book projection built from these model points needs a paid-up cohort weight. **Every figure is `[unverified]` recollection; neither series was retrieved or searched, and there is no official statistic for the *ruhende* share at all** (gap 2)

(delib-riester_rente-r26)=

### R26 — *Fokusgruppe private Altersvorsorge* (2023) and the pAV-Reform / *Altersvorsorgedepot* debate
- Publisher: Bundesministerium der Finanzen (the working group); the federal government (the bill)
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the product spec's closing argument that every reform proposal begins with the 100 % *Beitragsgarantie* — the 2023 working group recommending its relaxation or removal, a securities-account product without an insurance wrapper, a simplified proportional Zulage and wider eligibility, and the 2024 draft bill creating an *Altersvorsorgedepot* that **did not become law in that parliamentary term**. The spec accordingly describes a **legacy** product and frames the reform position as of that draft. **The position at the 2026-08-29 access date is not established** (gap 1), and the library's own 2026 closure date is carried from [REG-R44] instead

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **Every entry on that page records `Fetched:
no`** for the reasons given above; where an entry was corroborated by a search run while the budget
lasted, that page says so per fact. Entries cited by the Riester documents:

- **REG-R5** — VAG 2016, the statute and its Anlage 1: the supervisory frame the provider sits in, and the *Sparte* this contract is written in.
- **REG-R6** — VAG §§ 74–110 and § 40: the best-estimate-plus-risk-margin structure the published `liability_cf` feeds, and the SFCR that reports it. Nothing here discounts.
- **REG-R14** — DeckRV § 2: the *Höchstrechnungszins* as a cap on the **reserving** rate rather than on what a policy may guarantee — the distinction the model's `rechnungszins` **[std]** rests on.
- **REG-R15** — the *Höchstrechnungszins* rate history and the Sechste Verordnung of 19 July 2024: the 0,25 % and 1,00 % values used with [R22], and the 1,00 % `annuity_rechnungszins`.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the ceiling the model's initial commission is set at, and the German counterpart to the AltZertG's five-year spreading rule.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: named in the valuation pointers as out of scope, and the reason `rechnungszins` is a model point attribute rather than a library constant.
- **REG-R18** — MindZV: the statutory minimum allocation to the *Rückstellung für Beitragsrückerstattung*, which is the floor under the declared rate this model takes as an exogenous **[std]** scenario.
- **REG-R19** — RfBV: the collective RfB behind the same declared rate, and why a declared *laufende Verzinsung* is a management decision rather than an asset return.
- **REG-R20** — LVRG 2014: the commission and cost-disclosure reform that bounds the acquisition-charge and commission **[std]** levels.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171: the contract law that governs a certified Riester insurance contract exactly as it governs a Schicht-3 one, subject to the AltZertG's overrides.
- **REG-R24** — VVG § 153, *Überschussbeteiligung* and the *hälftige* participation in *Bewertungsreserven*: the basis of `bewres_pp()` at *Rentenbeginn*.
- **REG-R28** — VVG §§ 165–170: *prämienfreie Versicherung* (the statutory limb of *Beitragsfreistellung*), *Kündigung*, the *Rückkaufswert* and the agreed and appropriate *Stornoabzug* — `cv_pp` and `stornoabzug_rate`, and the five-year-spreading floor under the surrender value which this model satisfies by construction.
- **REG-R29** — VVG §§ 172–177: the *Berufsunfähigkeitsversicherung* whose premium creates the guarantee carve-out here and whose own liability lives in `berufsunfaehigkeit`.
- **REG-R31** — VVG §§ 6, 7 and 214 with the VVG-InfoV: the advice, information and cost-disclosure duties that sit alongside the AltZertG's own [R4].
- **REG-R32** — PRIIPs: the parallel European disclosure regime, named to distinguish it from the AltZertG sheet.
- **REG-R33** — the IDD as transposed: the distribution regime behind the commission assumption.
- **REG-R34** — Unisex: EuGH C-236/09 (*Test-Achats*) and the AGG — the general rule Riester preceded by six years [R23].
- **REG-R35** — BaFin Merkblatt 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener Kundennutzen*: the conduct lens a charge basis on a subsidised product is now read under.
- **REG-R36** — the BGH line of authority on German life contracts: the case law behind the surrender-value and *Stornoabzug* limbs.
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: the taxonomy [R18] states, in the cross-product form every delib product uses.
- **REG-R40** — ZPO §§ 850b and 851c, *Pfändungsschutz*: the execution protection that, with [R16], argues for a low surrender assumption.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a and § 55 EStDV: the *Ertragsanteil* the **unsubsidised** pool falls under, against the full taxation of the subsidised one [R12].
- **REG-R42** — EStG § 10a and Abschnitt XI (§§ 79–99), the Riester subsidy machinery: **the cross-product carrier of every figure in the subsidy chain** — the Zulagen amounts, the 4 % / 2 100 € / 60 € arithmetic, the proportional Kürzung, the ZfA lag and the *Kleinbetragsrente* threshold — reported at one remove from the product-level [R6] [R9] [R10] [R11] [R15].
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge: the cross-product carrier of the certification criteria, the *Beitragserhaltungszusage*, the 30 % lump-sum cap, the five-year cost spreading and the **20 % biometric carve-out** that `guar_carve_out_cap` implements.
- **REG-R44** — the Altersvorsorgereformgesetz 2026 and the *Altersvorsorgedepot*: the reform that closed this product to new business, and the source of the **1 January 2027** valuation date the whole model point table opens at.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the lump-sum tax rule the unsubsidised pool falls under, for contrast with § 22 Nr. 5.
- **REG-R46** — ErbStG and SGB V §§ 226, 229 and 240: contributions on an annuity in payment, and the *Bezugsgröße*-linked figures behind the two competing readings of the *Kleinbetragsrente* threshold.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: **why the two best-estimate factors run in opposite directions** (0.80 on the death basis, 1.15 on the annuity basis), and why no DAV table is redistributed here.
- **REG-R48** — DAV 2008 T: the death-benefit basis `mort_table_accum.csv` is a **[std]** proxy for.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the **generational** annuity basis `annuity_mort_table.csv` is a **[std]** proxy for, and the reason a period-table proxy would understate a seventeen-year-deferred annuitisation.
- **REG-R53** — the German life market in numbers: the region declared rates sat in during the mid-2020s, which is where the `base` scenario's 2,30 % comes from, and the statement that a declared *laufende Verzinsung* **includes** the *Rechnungszins*.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the statutory accounts these cash flows are not, named in the valuation pointers.
- **REG-R55** — IFRS 17: the other measurement frame the published cash flows feed, likewise out of scope here.

---

## Provenance note

Extraction details — one entry per source with an extended *Content* block, the mechanics sections
the product documents are written from, and the nineteen-item gaps-and-caveats register — live in
`_research/riester_rente.md`. That file is the citation ground truth for the S# and R# numbering
used here.

The caveats that most affect what these product documents can claim are these. **Nothing
carrier-specific was established, for any of the twenty-plus houses named in [S4]–[S8] and [S16]** —
not one AVB, *Rechnungszins*, *Rentenfaktor*, *Überschuss* declaration, guarantee design or
new-business status — so every carrier parameter in the model is **[std]** (gap 12). **No charge
figure exists in this corpus**: the single inherited datum [S5] is third-party commentary on a
specimen quotation, and **the charge base for the Zulagen is unknown** (gaps 13, 14), which matters
most on exactly the low-income cells the product was designed for. **No behavioural rate was
established** — no *Stornoquote*, no *Beitragsfreistellung* rate, no transfer-out rate, no
commutation take-up — so every rate in that class is an argument from the statutory consequences
rather than from data (gap 16). **No Riester tariff's conversion basis was established**, so the
two-*Rentenfaktor* construction and the question of which surplus components may close a guarantee
shortfall are both **[std]** (gap 9). **The *Kleinbetragsrente* is under-specified in three ways**
(gap 7). **Every statutory paragraph number here is `[unverified]`** — not one was confirmed against
the statute (gap 4) — and the BMF *Anwendungsschreiben* that would settle most of them was not
identified (gap 3). **No market figure was established** (gap 2). And **the status of the pAV reform
at the access date is not established** (gap 1), so nothing downstream asserts a current legal
position on it.

The honest summary is the research file's own: **treat this corpus as a well-organised set of
hypotheses about what the documents say, not a record of what they say.** The statutory half of the
product — the half that makes this a Riester contract rather than a private annuity — is stated from
general knowledge of German pension law and is not a composite; the carrier half is entirely
**[std]**, and each such parameter carries its rationale where it is used.
