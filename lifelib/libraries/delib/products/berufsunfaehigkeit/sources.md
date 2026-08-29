# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/berufsunfaehigkeit.md` (the citation
ground truth for this product) and are **frozen — never renumber**. Unused sources are omitted,
so the numbering has gaps. **S7** (Swiss Life AG, Niederlassung für Deutschland), **S10**
(Barmenia Lebensversicherung a. G.) and **S11** (Dialog Lebensversicherungs-AG) are named in the
research file as carriers whose wordings would settle the *Verweisung* clauses, the standalone
form and a pure-biometric *Überschussbeteiligung*, but **nothing from any of them is asserted**
in `product-spec.md` or `technical-notes.md` — those market positions are made generically from
[S12] — so citing them would attribute a claim to a document that supports no statement here.
**R26** (Deutsche Rentenversicherung Bund, *Rentenversicherung in Zahlen*) is absent for the
same reason: the statutory *Erwerbsminderungsrente* enters only through the statute [R24] [R25],
and no DRV statistic is printed anywhere, because none could be re-established and the house
rule forbids reproducing a recalled figure under a source tag. Access date for all sources:
**2026-08-29**. No sources were newly added at drafting. Cross-product [REG-R#] tags are listed
in their own section at the end.

**Retrieval conditions, stated plainly.** Two independent limits applied while this library was
built, and this product was reached after both had bitten.

1. **Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl` are refused with HTTP 403 at the egress gateway for every host outside a short package-registry allowlist. The hosts that matter here were tried and refused: `gesetze-im-internet.de` (VVG, VAG, SGB VI, EStG, DeckRV, MindZV, IfSG), `bafin.de`, `gdv.de`, `aktuar.de`, `deutsche-rentenversicherung.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`, `buzer.de` and `bundesgerichtshof.de`. **No document cited anywhere in this file was retrieved** — no *Bedingungswerk*, no *Produktinformationsblatt*, no statutory text, no DAV *Ergebnisbericht*, no BaFin publication, no BGH judgment.
2. **The session's `WebSearch` budget — 200 calls, shared across the delib build — was exhausted before this product was researched.** Every search attempted for `berufsunfaehigkeit` returned the budget-exhausted message, so this product had **no research channel at all**: the research file was written from the author's own knowledge of German insurance law and market practice, under the discipline the house brief imposes for exactly that case.

What follows, and it governs every entry below:

- **A delib citation is a pointer, not a certificate.** It names the instrument a claim should be checked against; it does **not** assert that anyone checked it. Every `Retrieved` line says `no` and none says otherwise.
- **Every entry is a *known reference*** — a document that exists and is the right kind of document — with publisher, doc type, `URL: not established` unless the canonical form is one this author is confident of, and both reasons on the `Retrieved` line. **No entry asserts an edition, document number, *Bundesgesetzblatt* citation, page count or publication date.**
- **Nothing in this chain is quoted.** No verbatim statutory or contractual wording appears here or in the documents that cite it; every description is a paraphrase.
- **`[unverified]` is used generously** in the product documents: every paragraph number, effective date, amount, percentage, table name and market figure carries it unless it is a structural fact not in dispute.
- **Uncertain levels became `[std]` parameters rather than citations.** Every biometric level, every charge level and the premium itself is **[std]**, each listed with its rationale in `model.md`. A `[std]` number is honest about being a construction; a fabricated `[S4]` number is not, and there are none.

---

## Primary product sources

(delib-berufsunfaehigkeit-s1)=

### S1 — GDV, *Allgemeine Bedingungen für die selbständige Berufsunfähigkeitsversicherung* (unverbindliche Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; *unverbindliche Musterbedingungen* — non-binding model conditions most German insurers use as the drafting skeleton for their own AVB. Non-binding precisely because binding recommended conditions would be a cartel, so each insurer's own AVB is the operative document.
- URL: not established (`gdv.de` refused the fetch).
- Retrieved: **no** — direct HTTP egress blocked in the build environment; **no search corroboration** (session search budget exhausted).
- Used for: **the most-cited document in this product.** The contractual definition of *Berufsunfähigkeit* — the 50 % threshold and the six-month *Prognosezeitraum*, both **AVB conventions and not statute** — the *Sechs-Monats-Fiktion*, retroactive payment from onset, the *Anerkenntnis* and *Nachprüfung* clauses, the *Beitragsbefreiung* as core cover, the *Karenzzeit* as a deferment of **payment**, the *Leistungsdauer* / *Versicherungsdauer* pair, the *Wiedereingliederungshilfe*, the exclusion list, and the absence of any death, maturity or surrender benefit as a modelled cash flow.

(delib-berufsunfaehigkeit-s2)=

### S2 — GDV, *Allgemeine Bedingungen für die Berufsunfähigkeits-Zusatzversicherung* (Muster-BUZ)
- Publisher / doc type: GDV; *unverbindliche Musterbedingungen* for the rider form.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the BUZ as a **wrapper variant of the same liability** — identical definition, claim procedure and *Nachprüfung* — and the one substantive difference recorded: in a BUZ the *Beitragsbefreiung* waives the **whole** host premium and the rider cannot outlive the host. It also bounds this product against delib products 2 and 5, which may carry the rider.

(delib-berufsunfaehigkeit-s3)=

### S3 — Allianz Lebensversicherungs-AG, AVB for the *selbständige Berufsunfähigkeitsversicherung*, with its *Produktinformationsblatt*
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart — the largest German life insurer; AVB (*Bedingungswerk*) plus *Produktinformationsblatt*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the most widely read BU wording in the market, cited for the market-standard shape it is expected to carry — the 50 % / six-month definition, waiver of the *abstrakte Verweisung*, a *Nachversicherungsgarantie* event list, a *Beitragsdynamik* option, occupational classification and the *Brutto* / *Zahlbeitrag* pair. **No product name, tariff code, edition date or parameter is asserted from it anywhere.**

(delib-berufsunfaehigkeit-s4)=

### S4 — Alte Leipziger Lebensversicherung a. G., AVB and *Tarifbestimmungen* for its BU range
- Publisher / doc type: Alte Leipziger Lebensversicherung a. G., Oberursel; AVB and *Tarifbestimmungen*, broker channel.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record of **what could not be settled** — the *Berufsgruppen* count, the *Nachversicherungsgarantie* event list with its per-event and aggregate caps, the *Verlängerungsoption* window and the *Karenzzeit* menu. It is cited at each of those to say the level is **[std]**, and for the *Nachversicherungsgarantie* being unmodelled.

(delib-berufsunfaehigkeit-s5)=

### S5 — LV 1871 (Lebensversicherung von 1871 a. G. München), AVB and PIB for its BU range
- Publisher / doc type: Lebensversicherung von 1871 a. G. München; AVB and *Produktinformationsblatt*, broker channel.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **tiered range on one risk basis** — tiers differing in the option set (*Nachversicherungsgarantie* breadth, *AU-Klausel*, *Leistungsdynamik*) rather than in the core definition. That is the normal German shape and is why the model implements one base tariff with switchable options rather than several tariffs.

(delib-berufsunfaehigkeit-s6)=

### S6 — NÜRNBERGER Lebensversicherung AG, AVB, *Tarifbestimmungen* and *Berufsgruppenverzeichnis*
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG, Nürnberg; AVB, *Tarifbestimmungen* and the *Berufsgruppenverzeichnis* — the occupational classification list running to hundreds of named occupations mapped to rating classes.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **occupation as the dominant rating factor**, and the shape of the classification — academic and office at the top, heavy manual and hazardous at the bottom, four to six classes typical, classes **not comparable between carriers**. It backs the model's one-base-table-plus- loadings design and the **[std]** BG1–BG5 cut with its 1,00 and 3,00 anchors. **No occupation-to-class mapping is asserted.**

(delib-berufsunfaehigkeit-s8)=

### S8 — HDI Lebensversicherung AG, AVB and PIB for its BU range
- Publisher / doc type: HDI Lebensversicherung AG, Köln (Talanx group); AVB and *Produktinformationsblatt* for a tiered broker-channel range.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the ***AU-Klausel*** and the three parameters bounding it — the certified duration of *Arbeitsunfähigkeit* required, the maximum benefit period under the clause, and whether payments are set off against a later BU decision. None could be established, which is why the model ships the clause with an inception uplift of exactly 1,00.

(delib-berufsunfaehigkeit-s9)=

### S9 — VOLKSWOHL BUND Lebensversicherung a. G., AVB and *Tarifbestimmungen*
- Publisher / doc type: VOLKSWOHL BUND Lebensversicherung a. G., Dortmund; AVB and *Tarifbestimmungen*, broker-channel BU specialist.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the practice of **printing a *Bruttobeitrag* and a *Zahlbeitrag* side by side in the quotation**, on which the whole two-premium-stream design of the model rests. The practice is recorded as a market fact; no figure from any quotation is asserted.

(delib-berufsunfaehigkeit-s12)=

### S12 — Further German BU carriers, *Bedingungswerke* and *Produktinformationsblätter* (document class)
- Publisher / doc type: R+V, Debeka, Continentale, Gothaer, Die Stuttgarter, Zurich Deutscher Herold, ERGO Vorsorge, AXA, Hannoversche, CosmosDirekt, Württembergische, Baloise, die Bayerische, universa, DEVK, SIGNAL IDUNA, Provinzial and HUK-COBURG — all real German life insurers writing BU; AVB, *Tarifbestimmungen*, PIBs and *Berufsgruppenverzeichnisse*.
- URL: not established for any of them.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **breadth of the market**, and the one structural split the research supports — the significant division is **channel**, not wording: direct writers and the bank / *Öffentliche* channels sell simpler tariffs with narrower occupational appetite, the broker channel the full option set. **Nothing quantitative is cited from this class** and no parameter is attributed to any named carrier.

(delib-berufsunfaehigkeit-s13)=

### S13 — *Produktinformationsblatt* (PIB) for a *selbständige Berufsunfähigkeitsversicherung* (document class)
- Publisher / doc type: each insurer, for each tariff; the short pre-contractual information sheet required by the VVG-InfoV [R12] `[unverified]` as to the precise article.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the ***Brutto* / *Zahlbeitrag* disclosure** — the one public document that routinely prints both figures for a named age, occupation and *BU-Rente*, with the explicit warning that the *Zahlbeitrag* may rise **as far as the *Bruttobeitrag* and no further**. That warning is the contractual content of `beitragsverrechnung` and of the contract-boundary argument. **No PIB was retrieved**, so the 0,70 ratio is **[std]** and the recalled 0,50–0,80 range `[unverified]` — the most consequential single gap in this product.

(delib-berufsunfaehigkeit-s14)=

### S14 — *Basisinformationsblatt* (PRIIP-KID) — and why a standalone SBU normally has none
- Publisher / doc type: each insurer, where the product is in scope; PRIIPs key information document under Regulation (EU) No 1286/2014 [REG-R32].
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: a **negative finding of substance**. PRIIPs covers insurance-based *investment* products, so a pure biometric contract falls outside it and an SBU is documented by a PIB [S13] and **not** by a *Basisinformationsblatt* — the opposite of delib's savings products, where that document is the richest public source. Hence this product hands the modeller **no cost table at all** and every charge level is **[std]**. The precise PRIIPs boundary is `[unverified]`.

(delib-berufsunfaehigkeit-s15)=

### S15 — Comparison portals, consumer press and rating agencies (document class)
- Publisher / doc type: Verivox, CHECK24, Finanztip, Stiftung Warentest / *Finanztest*, Handelsblatt, MORGEN & MORGEN, Franke und Bornberg, ASSEKURATA; comparison pages, consumer guides, product tests and ratings — **secondary throughout**.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the class where every published German BU **price point** and **wording-quality rating** lives, and the class this product most needed and least could reach. It carries the recalled 55–90 € monthly *Zahlbeitrag* band for an office occupation at age 30 for 1 500 € to 67, against which the worked example's 62,05 € instalment is sanity-checked — a plausibility check and **not** a calibration, every input to it being **[std]**. Every figure attributed to this class is `[unverified]`.

(delib-berufsunfaehigkeit-s16)=

### S16 — Verbraucherzentrale material on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: the *Verbraucherzentralen* and the *Verbraucherzentrale Bundesverband* (vzbv); consumer-advice pages and brochures — **secondary**.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the behavioural facts the assumptions must reflect — that the ***Bruttobeitrag* and not the *Zahlbeitrag* is the figure a buyer should compare**, the clearest external statement of why the pair is a modelling issue and not a presentational one; that incomplete *Gesundheitsfragen* are the commonest reason a claim later fails; that cover cannot be replaced once health has changed, which is why the German BU *Stornoquote* is low; that *Karenzzeit* and a reduced *Endalter* are the two premium levers; and that *Beitragsfreistellung* beats lapse.

---

## Regulatory and actuarial references (product research numbering)

Every entry carries the same retrieval status and states it rather than assuming it. Where a URL
is given it is the canonical form of a `gesetze-im-internet.de` address and is marked
`[unverified]`; the paragraph numbering it encodes is itself part of what is unverified.

(delib-berufsunfaehigkeit-r1)=

### R1 — VVG § 172, *Leistung des Versicherers* — the statutory definition of *Berufsunfähigkeit*
- Publisher / doc type: Bundesministerium der Justiz / Bundesamt für Justiz; statute, VVG 2008.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__172.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the anchor provision — liability for a BU arising **after inception**; the definition keyed to **the last occupation actually exercised, as it was arranged**, on a **medical** cause, prospectively permanently; and Abs. 3 permitting but **not implying** the *abstrakte Verweisung*. Also for the correction running through both documents: **neither the six-month period nor the 50 % threshold is statutory** — both are AVB conventions [S1].

(delib-berufsunfaehigkeit-r2)=

### R2 — VVG § 173, *Anerkenntnis*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__173.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the duty to declare in *Textform* whether liability is acknowledged; the restriction of the *befristetes Anerkenntnis* to **once**; and the effect that matters — once given it binds and the burden of proof reverses, so the insurer escapes only through § 174 [R3]. It is also the citation behind the model carrying **no acknowledged state**, paying from onset.

(delib-berufsunfaehigkeit-r3)=

### R3 — VVG § 174, *Leistungsfreiheit* — the *Nachprüfung* and its notice period
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__174.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the most model-relevant provision in the statutory frame** — the insurer stays liable to the end of the **third month after the notice reaches the policyholder**, which is the model's three-slot run-off ledger, its `runoff_months = 3` and its `check_runoff_roll_fwd` identity. Also for the requirement to demonstrate a **change** rather than re-decide the claim, and the *konkrete Verweisung* route that lets recovery and referral be one modelled rate.

(delib-berufsunfaehigkeit-r4)=

### R4 — VVG § 175, *Abweichende Vereinbarungen*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__175.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: §§ 173 and 174 being *halbzwingend*, so no departure to the policyholder's disadvantage is effective — which is why the *Anerkenntnis* and *Nachprüfung* mechanics are recorded as **uniform across the market and not a competitive variable**, and why the run-off is modelled as a statutory floor some insurers improve on.

(delib-berufsunfaehigkeit-r5)=

### R5 — VVG § 176, *Anzuwendende Vorschriften*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__176.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the cross-reference making an SBU a life contract in everything but its trigger, applying the life provisions *mutatis mutandis* — recalled as §§ 150–170 `[unverified]`. Every statement about the *Überschussbeteiligung* [R10], the suicide window [R11], the *beitragsfreie BU-Rente* [R8] and the *Rückkaufswert* [R9] depends on it, and **confirming the range it imports** is the first verification task the research file names.

(delib-berufsunfaehigkeit-r6)=

### R6 — VVG § 177, *Ähnliche Versicherungsverträge*
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__177.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **outer boundary of the product** — § 177 extends the *Anerkenntnis* / *Nachprüfung* frame to cover of reduced earning capacity and of *Arbeitsunfähigkeit*, so an *AU-Klausel* benefit inherits the same protections and *Grundfähigkeits-* and *Erwerbsunfähigkeitsversicherung* are named as neighbours rather than modelled.

(delib-berufsunfaehigkeit-r7)=

### R7 — VVG §§ 19–22, *Vorvertragliche Anzeigepflicht* and its consequences
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__19.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the underwriting section — the duty to disclose what is asked in *Textform*, the remedies graded by fault (*Rücktritt*, contract amendment, *Kündigung*, *Anfechtung*) and the five-/ten-year limits `[unverified]`; the *Risikovoranfrage* and the industry's HIS as behavioural consequences; and why an *Anzeigepflichtverletzung* sits **inside** the modelled *Anerkennungsquote* rather than beside it.

(delib-berufsunfaehigkeit-r8)=

### R8 — VVG § 165, *Prämienfreie Versicherung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the right to a **beitragsfreie *BU-Rente***, and the scope statement that follows — the model prices it **not at all**, because it is the release of a reserve the model does not compute. The paid-up benefit is small, a BU *Deckungsrückstellung* being a fraction of the present value of the remaining risk.

(delib-berufsunfaehigkeit-r9)=

### R9 — VVG § 169, *Rückkaufswert* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the existence of a genuine *Rückkaufswert*, the five-year spreading of acquisition costs for the *Mindestrückkaufswert*, and the conditions on a *Stornoabzug* `[unverified]`. It backs the structural zero of `claims(t, "LAPSE")`, published as a scope statement rather than an omission, and the reserve argument: a level *Bruttobeitrag* against a steeply rising inception rate builds a real reserve, which is what makes this a better demonstration than term life.

(delib-berufsunfaehigkeit-r10)=

### R10 — VVG § 153, *Überschussbeteiligung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the legal basis of the *Brutto* / *Zahlbeitrag* pair** — the entitlement to a share of the *Überschuss* on a *verursachungsorientiertes Verfahren*, which for BU is overwhelmingly risk plus expense surplus. It is the citation behind `beitragsverrechnung`, behind the `surplus_credit` column, and behind carrying **no surplus account and no declaration mechanic**, the surplus being applied immediately rather than accumulated.

(delib-berufsunfaehigkeit-r11)=

### R11 — VVG § 161, *Selbsttötung* (applied via § 176)
- Publisher / doc type: as R1; statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the exclusion of an **intentionally self-inflicted impairment**, and the three-year window `[unverified]` applying to the attempted-suicide case; whether the market's AVB run the window or exclude deliberate self-harm without a time limit is recorded as unresolved. Exclusions are absorbed into the calibration of the inception rate, not modelled separately.

(delib-berufsunfaehigkeit-r12)=

### R12 — VVG-Informationspflichtenverordnung (VVG-InfoV)
- Publisher / doc type: Bundesministerium der Justiz; statutory instrument prescribing pre-contractual information duties, including the *Produktinformationsblatt*.
- URL: `https://www.gesetze-im-internet.de/vvg-infov/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the mandate behind the PIB [S13], and the point that matters for the model — the *Effektivkosten* disclosure applies where there is a yield to reduce, so **a pure risk contract discloses its costs only through the *Brutto* / *Zahlbeitrag* pair**. That absence is why every charge assumption here is **[std]** while delib's savings products' are not.

(delib-berufsunfaehigkeit-r13)=

### R13 — Deckungsrückstellungsverordnung (DeckRV) — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Bundesministerium der Finanzen; statutory instrument.
- URL: `https://www.gesetze-im-internet.de/deckrv/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two model parameters. The *Höchstrechnungszins*, recalled as **1,00 %** for contracts written from 1 January 2025 `[unverified]` on both figure and date, is the `rechnungszins` used inside the premium equivalence and nowhere else; the *Höchstzillmersatz* of **25 ‰ of the *Beitragssumme*** `[unverified]` is the ceiling `acq_rate` sits at — the only sourced number in the whole charge structure, and even it carries the tag.

(delib-berufsunfaehigkeit-r14)=

### R14 — Mindestzuführungsverordnung (MindZV)
- Publisher / doc type: Bundesministerium der Finanzen; statutory instrument on the minimum allocation of surplus to policyholders.
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **risk-result minimum allocation** that governs a BU book, recalled as 90 % of the risk result `[unverified]`. It is the quantitative link between claims experience and the *Zahlbeitrag* charged, and sits behind `beitragsverrechnung` as the reason the credit is large and is expected to persist.

(delib-berufsunfaehigkeit-r15)=

### R15 — VAG §§ 138, 139, 141 — *Gleichbehandlung*, *Überschussbeteiligung*, *Verantwortlicher Aktuar*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Versicherungsaufsichtsgesetz*.
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]` as to the section numbers.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the *Gleichbehandlungsgrundsatz* that **legitimises *Berufsgruppen*** — pricing by occupation is the recognition that the risks are not equal — the supervisory counterpart of § 153 VVG, and the *Verantwortlicher Aktuar*'s responsibility for the bases. Also for **unisex**: sex may not enter premiums or benefits for contracts written from 21 December 2012, which is why `sex` is a reporting attribute that must not price.

(delib-berufsunfaehigkeit-r16)=

### R16 — DAV 1997 I, DAV 1997 RI and DAV 1997 TI — the *Rechnungsgrundlagen* for BU
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Köln; actuarial tables with their *Herleitung* report — *Invalidisierungs-*, *Reaktivierungs-* and *Sterbewahrscheinlichkeiten der Invaliden*. **Not public.**
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the three biometric bases the model proxies, and the statement that they are **DAV property, are not published and are not redistributed by delib**. It backs the shapes the **[std]** proxies must reproduce — a steeply rising inception curve, reactivation concentrated in the first one to two claim years and near zero after about five, and disabled-lives mortality materially above active and itself select on duration — and the record that the shipped reactivation proxy carries **no age-at-disablement dimension**, which the real table does. The table names themselves are `[unverified]`.

(delib-berufsunfaehigkeit-r17)=

### R17 — DAV 2008 T — active-lives mortality
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; first-order mortality table for contracts with death-benefit character, with its *Herleitung* report. **Not public.**
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **active state's** mortality decrement — an active life leaves by becoming *berufsunfähig*, by lapsing or by dying, and the last uses a *Todesfall*-character table rather than a population table. Cited by name and **not shipped**; the model's active column is an anchored **[std]** Gompertz proxy.

(delib-berufsunfaehigkeit-r18)=

### R18 — DAV *Ergebnisberichte* and *Fachgrundsätze* on biometric bases and BU
- Publisher / doc type: Deutsche Aktuarvereinigung e. V., *Ausschuss Lebensversicherung* and its working parties; results reports and professional standards, freely downloadable in normal conditions.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record of the three things the model most lacks quantitatively — the shape of the German BU inception curve, its trend over time, and the second-order reactivation pattern — and for the unresolved question of whether a homologated successor to DAV 1997 I exists at all.

(delib-berufsunfaehigkeit-r19)=

### R19 — BaFin material on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; *Merkblätter*, *Rundschreiben*, *BaFinJournal* articles and the industry *Beschwerdestatistik*.
- URL: not established (`bafin.de` refused).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the supervisory frame — BaFin's *Wohlverhaltensaufsicht* over the *Leistungsprüfung*, the quality of *Nachprüfung* notices and the *Brutto* / *Zahlbeitrag* disclosure. **Nothing quantitative is cited from BaFin anywhere in this product.**

(delib-berufsunfaehigkeit-r20)=

### R20 — GDV statistics on the *Berufsunfähigkeitsversicherung*
- Publisher / doc type: GDV; *Statistisches Taschenbuch der Versicherungswirtschaft*, *Die deutsche Lebensversicherung in Zahlen*, and GDV press material on BU.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the market-size framing of the product and the existence of an industry-wide *Anerkennungsquote*, one of the two references behind the **[std]** `accept_factor = 0,80`. Every specific figure of this kind is `[unverified]` and **none is printed**.

(delib-berufsunfaehigkeit-r21)=

### R21 — Franke und Bornberg, *BU-Leistungspraxis* and the *BU-Rating*
- Publisher / doc type: Franke und Bornberg GmbH, Hannover; recurring study of BU claims practice on data supplied and audited at participating insurers, plus clause-by-clause wording ratings.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the ***Anerkennungsquote*** — its usual publisher, and the principal reference behind `accept_factor = 0,80` **[std]** — with the composition of declines, the burden of proof resting on the insured at the initial claim, and the market's ranking of *Verweisung*, *AU-Klausel* and *Nachversicherungsgarantie* wordings. The recalled 75–80 % level is `[unverified]`.

(delib-berufsunfaehigkeit-r22)=

### R22 — Morgen & Morgen, *M&M Rating Berufsunfähigkeit* and the annual causes analysis
- Publisher / doc type: MORGEN & MORGEN GmbH, Hofheim am Taunus; annual rating of BU tariffs with an accompanying analysis of the **causes of BU**.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the causes-of-BU distribution — psychiatric conditions the largest group, accidents a small minority — which is why the specification argues against an accident-only variant; and the rating of ***Zahlbeitrag* stability against the *Bruttobeitrag***, the market's own recognition that the gap is a risk to the buyer. Every percentage is `[unverified]` with no confirmed year.

(delib-berufsunfaehigkeit-r23)=

### R23 — ASSEKURATA, market studies on *Überschussbeteiligung* and biometric products
- Publisher / doc type: ASSEKURATA Assekuranz Rating-Agentur GmbH, Köln; annual market studies of declared *Überschussbeteiligung*, and insurer ratings.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **stability of the *Beitragsverrechnung*** — which insurers have had to raise the *Zahlbeitrag* toward the *Bruttobeitrag*, and by how much. That history is the empirical content of the risk the *Bruttobeitrag* represents, it is **not established**, and its absence is the stated reason `beitragsverrechnung` is held constant in the base run.

(delib-berufsunfaehigkeit-r24)=

### R24 — SGB VI § 43, *Rente wegen Erwerbsminderung*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Sozialgesetzbuch, Sechstes Buch*.
- URL: `https://www.gesetze-im-internet.de/sgb_6/__43.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the statutory benefit the private contract sits on top of — two tiers, both measured against the **general labour market** in hours a day rather than against the insured's own occupation, with the *Wartezeit* conditions `[unverified]`. It carries the market-role argument and has **no consequence for the recursion**: the statutory pension is not offset against the *BU-Rente* in the standard German contract.

(delib-berufsunfaehigkeit-r25)=

### R25 — SGB VI § 240 — the abolished statutory *Berufsunfähigkeitsrente*
- Publisher / doc type: as R24; statute.
- URL: `https://www.gesetze-im-internet.de/sgb_6/__240.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **why this product exists**. The transitional provision preserves an occupational-disability element only for insured persons born before 2 January 1961 `[unverified]`; for everyone later the statutory scheme contains no occupational-disability pension at all, and the private SBU is its replacement.

(delib-berufsunfaehigkeit-r27)=

### R27 — EStG § 10 and § 22 — deductibility of the premium and taxation of the *BU-Rente*
- Publisher / doc type: Bundesministerium der Justiz; statute — *Einkommensteuergesetz*.
- URL: `https://www.gesetze-im-internet.de/estg/__10.html` and `.../__22.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the taxation section — the standalone SBU premium as a *sonstige Vorsorgeaufwendung* inside a ceiling in practice already exhausted, and the *BU-Rente* taxed as an *abgekürzte Leibrente* on its *Ertragsanteil*, keyed to the annuity's remaining term rather than the recipient's age. Every figure is `[unverified]`. **Taxation does not enter the model**: delib projects gross, pre-tax cash flows.

(delib-berufsunfaehigkeit-r28)=

### R28 — BMF-Schreiben on the *Basisrente* and the conditions for a BU component
- Publisher / doc type: Bundesministerium der Finanzen; administrative circular on the tax treatment of *Altersvorsorge* and *Basisrenten* contracts.
- URL: not established (`bundesfinanzministerium.de` refused).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the conditions a BU rider must satisfy inside a *Basisrente* — annuity form, no benefit beyond the host's deferment, and a BU premium share capped at 49 % `[unverified]`. It bounds this product against delib's `basisrente` and explains why the standalone SBU remains the dominant retail form.

(delib-berufsunfaehigkeit-r29)=

### R29 — BGH case law on *Verweisung*, *Anerkenntnis* and *Nachprüfung*
- Publisher / doc type: Bundesgerichtshof, IV. Zivilsenat; judgments. **No docket number is given anywhere in this product**, because none could be confirmed and inventing one is barred.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: four settled lines, each recalled in substance and `[unverified]` in detail — the binding effect of the *Anerkenntnis*; the *Nachprüfung* requiring a **demonstrated change** and an intelligible *Einstellungsmitteilung*, so a defective notice never starts the three-month clock; ***Lebensstellung*** as the limit on any *Verweisung*; and the self-employed insured's *Umorganisationspflicht*. The first two are why recovery and *konkrete Verweisung* are one rate.

(delib-berufsunfaehigkeit-r30)=

### R30 — Infektionsschutzgesetz (IfSG) — the basis of the *Infektionsklausel*
- Publisher / doc type: Bundesministerium der Justiz; statute.
- URL: `https://www.gesetze-im-internet.de/ifsg/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the *Tätigkeitsverbot* that ends a medical professional's ability to earn without her being ill in the sense of § 172 VVG, and hence the *Infektionsklausel* deeming the ban to be BU. It is cited to say the clause is **not modelled separately**: its effect is a higher inception rate in one occupational segment, which is already how *Berufsgruppen* enter.

(delib-berufsunfaehigkeit-r31)=

### R31 — Versicherungsteuergesetz (VersStG) § 4 — exemption of life and BU premiums
- Publisher / doc type: Bundesministerium der Justiz; statute.
- URL: `https://www.gesetze-im-internet.de/versstg/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the single statement that **the BU premium carries no premium tax**, unlike a German non-life premium — recorded so a modeller from a non-life background does not look for the tax line. The paragraph and precise scope are `[unverified]` and should be confirmed before use.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **Every entry on that page records
`Fetched: no`** for the same two reasons given above, so these tags inherit the same status.
Entries cited by the *Berufsunfähigkeit* documents:

- **REG-R1 / REG-R2 / REG-R4** — Solvabilität II, the Delegated Regulation and the EIOPA risk-free curves: the valuation layer that consumes `liability_cf`, cited and never computed.
- **REG-R8 / REG-R9 / REG-R11** — VAG §§ 138, 139 and 141–143: premium sufficiency and *Gleichbehandlung*, the supervisory side of the *Überschussbeteiligung*, the *Verantwortlicher Aktuar*.
- **REG-R14 / REG-R15** — the DeckRV and the *Höchstrechnungszins* rate history: the 1,00 % from 1 January 2025 the premium equivalence discounts at.
- **REG-R16 / REG-R20** — DeckRV § 4 *Höchstzillmersätze* and the LVRG cut from 40 ‰ to 25 ‰: the ceiling `acq_rate` sits at, the rate in use at conclusion applying for the whole term.
- **REG-R18 / REG-R19 / REG-R24** — MindZV, RfBV and VVG § 153: the surplus machinery behind the *Beitragsverrechnung*, and the risk-result minimum that governs a BU book.
- **REG-R23** — VVG §§ 8 and 152, the 14-day and 30-day *Widerrufsrechte*: absorbed into the first-year lapse rate rather than modelled.
- **REG-R28** — VVG §§ 165–170: *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug* — the article-level source for the cash values this model does not price.
- **REG-R29** — VVG §§ 172–177 as a whole: the cross-product carrier for [R1]–[R6], including the three-month run-off.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the *Anzeigepflicht*, and the *qualifizierte Mahnung* whose two-week period the model does not carry, so lapse falls about a month early.
- **REG-R31 / REG-R33 / REG-R35** — the VVG-InfoV cost-disclosure regime, the IDD and BaFin's *Wohlverhaltensaufsicht*: why a pure risk product has no *Effektivkosten* figure.
- **REG-R32** — PRIIPs: why a standalone SBU normally has **no** *Basisinformationsblatt*.
- **REG-R34** — *Test-Achats* and the AGG: unisex pricing from 21 December 2012.
- **REG-R36** — the BGH line of authority on German life contracts, the carrier for [R29].
- **REG-R37** — the GDV *Musterbedingungen* and German BU market practice: that page's own entry on the 50 % / six-month convention and the *BU-Fiktion*.
- **REG-R38 / REG-R39 / REG-R41** — the AltEinkG *Drei-Schichten-Modell*, the *Basisrente* deduction, and the *Ertragsanteil* / *Besteuerungsanteil* rules: the tax section only.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the direction-of-prudence argument behind the four first-order loads.
- **REG-R48 / REG-R50** — DAV 2008 T and the DAV 1997 I / RI / TI family: the entries stating that the tables are not public and not redistributed, and that a BU model cannot leave disabled-lives mortality unspecified.
- **REG-R53** — the German life market in numbers: market scale, and the *Anerkennungsquote* and gross-versus-net-of-declinature point behind `accept_factor`.
- **REG-R54 / REG-R55** — HGB §§ 341–341o with the RechVersV, and IFRS 17: the accounting layers the same expected-cash-flow engine feeds.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation.

---

## Provenance note

Extraction details — which fact was recorded from which document class, the twenty-six sections
of extracted mechanics, and the eighteen-item gaps-and-caveats register — live in
`_research/berufsunfaehigkeit.md`, which is the citation ground truth for the S# and R# numbering
used here and states these same retrieval conditions at its head.

The caveats that most affect what these product documents can claim, in order of how much they
constrain the model:

1. **Nothing was retrieved and nothing was searched.** This product has no primary evidence of any kind. Every [S#] and [R#] points to a document that exists and is the right kind of document; none records a document read.
2. **No *Produktinformationsblatt* was obtained, so no *Brutto* / *Zahlbeitrag* pair is sourced** [S13]. The 0,70 ratio is **[std]** and the recalled 0,50–0,80 range `[unverified]`. This is the most consequential single gap: the ratio drives modelled premium income directly and moves it by more than 40 % across that range.
3. **No rate card of any kind was obtained** — no tariff table, no occupational factor set, no age curve [S15]. The *Bruttobeitrag* is therefore an **output** of a stated first-order basis rather than an observation, and the worked example is **internally consistent only**: unlike frlib's `temporaire_deces`, this model reproduces nothing external.
4. **The DAV 1997 family and DAV 2008 T are not public and were not seen** [R16] [R17]. Their *shapes* are asserted from general actuarial knowledge; their *levels* are constructions anchored so the worked example reproduces exactly. The table **names** may themselves be wrong, and anyone citing one must confirm it first.
5. **No insurer *Bedingungswerk* was opened, so no carrier-level parameter is attributed** [S3]–[S12]. Eighteen named German life insurers write this product; the documents name them and attribute nothing to them.
6. **Every charge level is [std]** [R12] [S14]. No German insurer discloses BU acquisition, administration or claims-handling costs, and a pure risk contract carries no *Effektivkosten* disclosure. The 25 ‰ *Höchstzillmersatz* [R13] is the only sourced ceiling, and it carries `[unverified]` on its own figure.
7. **The *AU-Klausel*'s effect on inception is unquantified** [S8]. The clause ships switched on with an uplift of exactly 1,00 rather than with an invented loading.
8. **Every statutory paragraph number is `[unverified]`** [R1]–[R6]. The two items most at risk are the exact range of sections § 176 imports — on which the surrender value, the paid-up right and the *Überschussbeteiligung* all depend — and the wording of § 173 on the *befristetes Anerkenntnis*.
9. **The VVG, VAG, SGB VI, EStG, DeckRV, MindZV and IfSG are living texts**, and the *Höchstrechnungszins* changes by instrument [R13]. No version date is asserted anywhere. Check every provision against the current consolidated text before relying on it. **A delib citation is a pointer, not a certificate.**
