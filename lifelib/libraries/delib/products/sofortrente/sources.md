# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/sofortrente.md` (the citation ground
truth for this product) and are **frozen — never renumber**. All fifteen primary sources
**S1–S15** are cited by `product-spec.md` or `technical-notes.md` and appear below. Nine of the
twenty-five product-level references are **not** cited by either document and are therefore
absent, leaving gaps in the R numbering: **R3** (VVG § 153, *Überschussbeteiligung*), **R7**
(DeckRV § 2, the *Höchstrechnungszins*), **R15** (MindZV), **R16** (VAG §§ 138–140 and the
*Zinszusatzreserve*), **R17** (VVG-InfoV and the PRIIPs Regulation) and **R24** (the unisex
rule) are each carried by the cross-product reference library under a frozen [REG-R#] id — as
[REG-R24], [REG-R14] / [REG-R15], [REG-R18], [REG-R9] / [REG-R10] / [REG-R17], [REG-R31] /
[REG-R32] and [REG-R34] respectively — and the product documents cite them from there, because
library-wide numbering is what lets a reader compare ten products against one instrument;
**R6** (VVG §§ 150, 159, 160, the *Bezugsberechtigung*) is likewise carried at [REG-R26], and
the beneficiary is in any event a pass-through that no cell in the model reads; **R9** (GDV and
HDI media items on the 2025 rate increase) supported no claim the two documents make that
[REG-R15] does not carry with a statutory instrument behind it; and **R12** (the DGVFM,
General Re and *qx-Club* expositions of DAV 2004 R) established **no content at all**, only
three presentation dates, and is cited in `model.md` alone, beside [R10], to record what a
later build should fetch to substantiate the first-order margin. Access date for all sources:
**2026-08-29**. No sources were newly added at drafting. Cross-product [REG-R#] tags are
listed in their own section at the end.

**Retrieval conditions — read before any entry below.** Two independent limits applied, and
this product was the worst-served of the ten. **(1) Direct HTTP egress is blocked** by an
organisation network policy: `WebFetch` and `curl` are refused with HTTP 403 at the egress
gateway for every host outside a short package-registry allowlist. `gesetze-im-internet.de`,
`bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`, `destatis.de`, `dejure.org`,
`eur-lex.europa.eu`, `de.wikipedia.org` and every insurer host named below were tried across
the delib build and all refused. **No document cited anywhere in this file was retrieved.**
**(2) The session's `WebSearch` budget — 200 calls, shared across the library — was exhausted
*before* work on the *Sofortrente* began.** Not one search was run for this product, against a
brief that anticipated thirty to eighty.

What follows from that, stated plainly. **A delib citation is a pointer, not a certificate**:
it names the instrument a claim should be checked against and does not assert that anyone
checked it. Where an entry below carries corroboration, that corroboration was recorded by a
**sibling delib research file** whose searches ran earlier in the session — principally
`_research/klassische_rentenversicherung.md`, which shares this product's *Rechnungsgrundlagen*
and, at two carriers, its tariff — and the entry says so and names the sibling file's own
source id. That is a traceable provenance chain and still one step weaker than a retrieval.
Every entry's `Retrieved` line says `no`. **No document number, URL, edition, page count or
publication date was guessed**: a URL recorded by a sibling file from a search result is
reproduced with attribution, the canonical `gesetze-im-internet.de` form of a statutory
provision is given and marked `[unverified]`, and everywhere else the entry reads `URL: not
established`. **Nothing is quoted except where a sibling file recorded the phrase from a search
summary**, and such a phrase is attributed to that summary rather than to the document. Every
specific paragraph number, date, amount and percentage that no search confirmed carries
`[unverified]`. Uncertain numbers became **[std]** parameters rather than citations, and
`model.md`'s standardization table lists every one — for this product that table is longer than
for any other in the library, because **the entire commercial character of a *Sofortrente* is a
number, the euros per month per 100 000 € of *Einmalbeitrag*, and that number could not be
established at any carrier for any year**.

---

## Primary product sources

(delib-sofortrente-s1)=

### S1 — GDV, *Musterbedingungen* service index, and the immediate-annuity model conditions
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin; publisher index page listing the association's *Musterbedingungen* — model general policy conditions members may adopt, adapt or ignore. Not binding, not a regulation
- URL: `https://www.gdv.de/gdv/service/musterbedingungen` — recorded by the sibling file `_research/klassische_rentenversicherung.md` [S3 there] from a search result
- Retrieved: no — egress blocked; no search corroboration in this session (budget exhausted); the URL and taxonomy are the sibling file's search record
- Used for: a **negative finding** and a structural one. The index lists model conditions for the deferred annuity, the *Basisrente*, two Riester wrappers and the *Hinterbliebenenrenten-Zusatzversicherung*, and **none for a *Rentenversicherung mit sofort beginnender Rentenzahlung*** — which is why `product-spec.md` states that the immediate annuity has no association template and reports the alternative reading, that the market drafts from the deferred one, as an inference rather than a finding (research gap 3). Cited with [S9] for the association's treatment of the survivor's annuity as a rider

(delib-sofortrente-s2)=

### S2 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Sofort beginnende Rentenversicherung", Fassung 01/2022
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, the consolidated pre-contractual pack a German life insurer must supply — general information, the AVB, the *Besondere Bedingungen* per option and the tax notes. Document code **521331402 2501**
- URL: `https://www.zurich.de/-/media/project/zwp/germany/br/documents/verbraucherinformationen/222202101_sofort-beginnende-rentenversicherung_verbraucherinformationen_2022_01.pdf` — returned by a search recorded in the sibling file [S16 there]
- Retrieved: no — egress blocked; the document's existence, title, code, vintage and URL are corroborated by the sibling file's search record; **no clause content was established from it**
- Used for: the product's identity and nothing quantitative. Its title establishes that the classic, general-account, non-unit-linked immediate annuity is a document class a named German carrier sells, which is what `product-spec.md`'s first table cites for "single-premium immediate life annuity on the general account, *konventionell*, profit-participating" and for "one *Einmalbeitrag*, paid once at inception; no premium stream, no *Beitragsdynamik*, no *Ratenzahlungszuschlag*". `product-spec.md` names it, with [S4], as **the first document a later build should fetch**, and records that its 01/2022 vintage places it in the 0,25 % *Höchstrechnungszins* era so any annuity level in it is not comparable with a current quotation [REG-R15]

(delib-sofortrente-s3)=

### S3 — Zurich Deutscher Herold Lebensversicherung AG, "Verbraucherinformation für Konventionelle Versicherungen — Aufgeschobene Rentenversicherung", Fassung 01/2026
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation*, deferred annuity. Document code **521331262 2601**
- URL: `https://www.zurich.de/-/media-assets/project/zurich-headless/germany/br/documents/verbraucherinformationen/32020_aufgeschobene-rentenversicherung_verbraucherinformationen_2026_01.pdf` — recorded by the sibling file [S4 there] from a search result
- Retrieved: no — egress blocked; the content used is the sibling file's search record, reproduced with attribution
- Used for: **the only clause-level evidence in the delib corpus that surplus participation does not stop at *Rentenbeginn***, which is load-bearing for this product. `product-spec.md` and `technical-notes.md` both cite it for "*Bewertungsreserven* participation continues during the annuity payment period, currently *hälftig* under § 153 Abs. 3 VVG" [REG-R24], and `technical-notes.md` cites it in class (a) for the *Überschussbeteiligung* as a statutory entitlement whose method is not prescribed and again under *Model scope* for the *Bewertungsreserven* share being **explicitly excluded** from the projection. Also carries the two-factor rule at *Rentenbeginn* on which [S7]'s pricing-primitive statement rests

(delib-sofortrente-s4)=

### S4 — NÜRNBERGER Lebensversicherung AG, *Allgemeine Bedingungen für die Rentenversicherung mit sofort beginnender Rentenzahlung*, publisher document id `gn331303_p`
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; an insurer's own AVB for exactly the product in scope
- URL: `https://www.nuernberger.de/medien/4allportal/gn331303_p.pdf` — the **document id was returned by a search** and is recorded by the sibling file [S9 there]; the URL is the carrier's established `4allportal` path form applied to that id and is `[unverified]` as a working address
- Retrieved: no — egress blocked; document id corroborated, URL constructed, **no clause content established**
- Used for: the fact that **an insurer AVB whose title names this product exists**, and that it sits in the same numbered family as that carrier's deferred [S5] and unit-linked condition sets — which is what `product-spec.md` cites for German insurers drafting the immediate annuity as a member of one AVB series rather than as a separate line, and which is the second half of the answer [S1] could not give. Named with [S2] as a priority fetch for a later build

(delib-sofortrente-s5)=

### S5 — NÜRNBERGER Lebensversicherung AG, "Allgemeine Bedingungen für die Rentenversicherung mit aufgeschobener Rentenzahlung und Rentengarantiezeit nach Tarif NIR3301", document id `gn331451_p`
- Publisher / doc type: NÜRNBERGER Lebensversicherung AG; AVB for a deferred annuity **with *Rentengarantiezeit***, tariff **NIR3301**
- URL: `https://www.nuernberger.de/medien/4allportal/gn331451_p.pdf` — recorded by the sibling file [S9 there] from a search result
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: **the *Rentengarantiezeit* as a tariff-level design feature carried in the product's own name**, not a rider bolted on. `product-spec.md` cites it beside [R23] and [S7] in the *Rentengarantiezeit* row of the representative specification, and `technical-notes.md` cites it in class (a) for `guar_years × payment_freq` instalments being payable **regardless of survival** from *Rentenbeginn* — the fact behind `certain_floor`, `check_guarantee_certain` and pitfalls 2 and 3

(delib-sofortrente-s6)=

### S6 — Cosmos Lebensversicherungs-AG (CosmosDirekt), "Allgemeine Bedingungen für die Rentenversicherung", tariff LA 904 A
- Publisher / doc type: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland; *Allgemeine Bedingungen* (AVB), tariff code **LA 904 A**
- URL: `https://www.cosmosdirekt.de/resource/blob/89106/31bbdccea1c7a5a530feb9e2a3be8d1c/allgemeine-bedingungen-rentenversicherung-la-904-a--data.pdf` — recorded by the sibling file [S8 there] from a search result
- Retrieved: no — egress blocked; the phrases used are the sibling file's record of a **search summary** and are attributed to that summary, not to the document
- Used for: **the most load-bearing entry in this file, and the only one that names a conversion basis.** Three claims rest on it: that the mortality basis of a German annuity tariff is **DAV 2004 R** [R10]; that the interest basis of a *guaranteed* annuity factor may be set **below** the statutory cap — "an underlying interest rate (currently 0 percent p.a.)", quoted from the search summary — which is why `check_tariff_int_rate` is an **inequality** and not an equality [REG-R14] [REG-R15]; and that the factor is fixed **at inception**, which for a *Sofortrente* means fixed once and never revisited. Also the source of the standard surplus disclaimer that the level of profit sharing depends on influences the company only limitedly controls, cited wherever the documents say a projected *Überschussrente* is never a guaranteed cash flow. **The AVB's vintage was not established** and the clause is time-stamped by its own word *currently* (research gap 6)

(delib-sofortrente-s7)=

### S7 — Allianz Lebensversicherungs-AG — the immediate-annuity tariff statement, and the Allianz immediate-annuity product documents
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; (a) the "Vorsorgekonzept KomfortDynamik" product page, recorded by the sibling file [S13 there] from a search result; (b) Allianz's own *Sofortrente* documents — PIB, AVB, BIB — **not established**
- URL: (a) `https://www.allianz.de/vorsorge/vorsorgekonzept/komfortdynamik/`, recorded by the sibling file; (b) not established
- Retrieved: no — egress blocked; (a) is the sibling file's search record, (b) is a known reference only
- Used for: three claims. That the calculation bases at *Rentenbeginn* relate to the interest rate and mortality table the company then uses **for immediately beginning annuities** — read with [S3]'s two-factor rule, this is what `product-spec.md` cites for the *Sofortrente* being the **pricing primitive** of every deferred German annuity. That the *Rentengarantiezeit* "can be set to a minimum", i.e. is a policyholder-selectable parameter with a contractual floor. And that the annuity is **monthly** in the market's standard form, cited with [R23] in the payment-frequency row. (b) supports only the disclosure, made in `product-spec.md`, that **no Allianz immediate-annuity document, tariff code or rate was established**, and the observation cited with [S8] that the classic *deferred* tariff was withdrawn at four large carriers

(delib-sofortrente-s8)=

### S8 — Debeka Lebensversicherungsverein a. G. — AVB series B LV, and the "Privatrente" product page
- Publisher / doc type: Debeka Lebensversicherungsverein a. G., Koblenz; AVB in the house **B LV** series, plus the insurer's *Privatrente* product page
- URL: `https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf` and `https://www.debeka.de/privatkunden/vorsorgensparen/zukunftalter/privatrente.html` — both recorded by the sibling file [S11] [S12 there] from search results
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: the ***Deckungskapital* definition** — the contributions accumulated at the *Rechnungszins* insofar as they are not required for risk and expense cover — which `product-spec.md` and `technical-notes.md` both cite for its degeneration, under a single premium, to the one netting step `Nettoeinmalbeitrag = Einmalbeitrag × (1 − α)`, the model's `net_single_prem()`. Also for the *Ertragsanteil* framing in an insurer's own words [R13], and, with [S7], for the withdrawal of classic deferred tariffs. **Whether Debeka writes a stand-alone *Sofortrente* was not established**

(delib-sofortrente-s9)=

### S9 — GDV, "Allgemeine Bedingungen für die Hinterbliebenenrenten-Zusatzversicherung zur Rentenversicherung"
- Publisher / doc type: GDV; *Musterbedingungen* for the **survivor's-annuity rider**
- URL: `https://www.gdv.de/resource/blob/6336/942f7b9aec6a969b486ec205279870a3/allgemeine-bedingungen-fuer-die-hinterbliebenenrenten-zusatzversicherung-zur-rentenversicherung-mit-aufgeschobener-rentenzahlung-0-pdf-data.pdf` — recorded by the sibling file [S10 there] from a search result. The slug names the **deferred** annuity; whether a separate set exists for the immediate one was not established
- Retrieved: no — egress blocked; no clause content established
- Used for: the single structural fact the documents need about the *Hinterbliebenenrente* — that **the German market treats it as a *Zusatzversicherung*, a rider with its own condition set, attached to the base contract rather than being a benefit of it.** `product-spec.md` cites it in the lives-basis and survivor-annuity rows, and `technical-notes.md` for the direct modelling consequence: a **separate gated leg with its own insured life, off in the base run**, rather than a term in the main annuity's benefit formula. The 60 % and 100 % levels attributed to the market are `[unverified]` and are not carried by this source

(delib-sofortrente-s10)=

### S10 — Konzern Versicherungskammer, "Überschussverteilung 2026"
- Publisher / doc type: Konzern Versicherungskammer, the Bavarian public-sector insurance group; the annual ***Überschussverteilung*** document — how a German life insurer publishes its declared *Überschussanteilsätze* for a year, by tariff generation and by phase
- URL: `https://www.konzern-versicherungskammer.de/dam/jcr:acf4c857-3b53-4521-a108-d1fb9b1cec67/BL_Ueberschussbeteiligung_2026.pdf` — recorded by the sibling file [S15 there] from a search result
- Retrieved: no — egress blocked; **the title and the 2026 vintage are corroborated; nothing inside the document was established**
- Used for: the **document class** that would supply every surplus rate this product's projection needs, and for the disclosure that **no rate, no percentage and no component split was established, for any carrier, for any year** (research gap 4). It is what `product-spec.md` and `technical-notes.md` both cite at the point where they say every figure in `surplus_scale_table.csv` is **[std]** and belongs to the insurer-discretionary class (b) rather than to the contractual class (a)

(delib-sofortrente-s11)=

### S11 — *Produktinformationsblatt* (PIB) for a sofort beginnende Rentenversicherung — document class
- Publisher / doc type: each insurer individually; the short pre-contractual product summary required by German insurance-distribution law [REG-R31] [REG-R33]. For an annuity it states the *Einmalbeitrag*, the *garantierte Rente*, the *Gesamtrente* including declared surplus, the *Rentengarantiezeit*, the death benefit and the costs
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)
- Used for: **known reference only**, and cited in `product-spec.md` for the disclosure that the class which would settle almost every quantitative gap here at a stroke — because a PIB for a *Sofortrente* prints the guaranteed and total annuity for a stated *Einmalbeitrag* and age — is the class of which **not one instance was located**. It is also where the documents place the statement that no charge parameter was established at any carrier (research gap 8)

(delib-sofortrente-s12)=

### S12 — *Basisinformationsblatt* (PRIIP-KID) for a sofort beginnende Rentenversicherung — document class
- Publisher / doc type: each insurer individually; the three-page key information document required by the PRIIPs Regulation [REG-R32], with its *Risikoindikator*, four performance scenarios and *Renditeminderung* cost figures
- URL: not established, for any carrier
- Retrieved: no — egress blocked; no search corroboration
- Used for: **known reference only, with a scope question attached.** `product-spec.md` cites it for two things: that if a BIB exists it is the **only** public document giving a cost figure in the standardised *Renditeminderung* form, and that **whether a payout-only *Sofortrente* is within PRIIPs scope at all was not established** — its payout-only character and the absence of a surrender value after *Rentenbeginn* [R1] make the holding-period and "what you might get back" sections awkward (research gap 8)

(delib-sofortrente-s13)=

### S13 — Carriers writing the product, recorded without documents
- Publisher / doc type: none — carrier names only: Allianz [S7]; R+V; Debeka [S8]; Generali and CosmosDirekt [S6]; Dialog; HDI; Alte Leipziger; LV 1871; Continentale and Europa; NÜRNBERGER [S4] [S5]; Swiss Life; Zurich Deutscher Herold [S2] [S3]; ERGO; AXA; Barmenia; Hannoversche; Württembergische; Gothaer; Stuttgarter [S14]; Volkswohl Bund; Baloise; Universa; DEVK; Signal Iduna; Provinzial; HUK-Coburg; Konzern Versicherungskammer [S10]; Mecklenburgische [S14]
- URL: not established
- Retrieved: no — egress blocked; no search corroboration
- Used for: the *Sofortrente*'s character as a **commodity product** ranked by comparison portals on the single dimension of *Rentenhöhe*, and — much more importantly — for the disclosure carried in `product-spec.md`'s variation section that **no carrier's product name, tariff code, envelope, rate or document was established**, so the observed-variation table is structural only and contains **no insurer-level quantitative comparison at all** (research gap 2). Naming a carrier here asserts that it is a German life insurer of the right kind and nothing more

(delib-sofortrente-s14)=

### S14 — Stuttgarter Lebensversicherung a. G. and Mecklenburgische Lebensversicherungs-AG — further pre-contractual packs
- Publisher / doc type: Stuttgarter Lebensversicherung a. G., "Allgemeine Informationen zu einem Altersversorgungssystem"; Mecklenburgische Lebensversicherungs-AG, "Vertragsinformationen für die Private Rentenversicherung mit flexiblem …" (product "Rente flex", title truncated in the search record)
- URL: `https://www.stuttgarter.de/documents/209195/221255/Allgemeine_Infos_Altersversorgungssystem_SLV.pdf/2657ea66-2bfa-9cec-04d2-8f72ac9731bd?t=1604038997833` and `https://www.mecklenburgische.de/pdfs/produkte/vertragsinformationen/Vertragsinformationen-zu-Leben/rente-flex_vertragsinformationen.pdf` — both recorded by the sibling file [S18] [S14 there] from search results
- Retrieved: no — egress blocked; no clause content established from either
- Used for: the naming fact that ***Verbraucherinformation*, *Vertragsinformationen* and *Allgemeine Informationen* are three names for the same pre-contractual pack**, which `product-spec.md` records so a later build searching for one searches for all three; and, in the *Aufschubzeit* row of the variation table, for the disclosure that the Mecklenburgische "Rente flex" is **the corpus's only candidate for the short-deferment variant and its feature is unestablished**, its title being truncated after "mit flexiblem" (research gap 17)

(delib-sofortrente-s15)=

### S15 — The annual *Standmitteilung* and *Rentenanpassungsmitteilung* in the *Rentenbezug* — document class
- Publisher / doc type: each insurer; the GDV publishes a *Muster-Standmitteilung*. For a contract in the *Rentenbezug* the statement reports the *garantierte Rente*, the current *Überschussrente*, the resulting *Gesamtrente*, and the increase taking effect at the anniversary under a rising *Überschussverwendung* [REG-R25]
- URL: not established for the payout form
- Retrieved: no — egress blocked; no search corroboration
- Used for: the **increase date**. `product-spec.md` and `technical-notes.md` both cite it for the *Überschussrente* stepping at the **policy anniversary** rather than on a calendar date — the fact behind `check_annuity_roll_fwd` and pitfall 14 — and for the running expense the annual statement and proof-of-life routine represent. It is also the source of two disclosures: that model point 10's `annuity_pp_init` is **[std]** because **no *Standmitteilung* was located at any carrier**, and that the corpus therefore contains **no evidence of what a *Rentenanpassung* has actually done** at any carrier in any year (research gap 16)

---

## Regulatory and actuarial references (product research numbering)

(delib-sofortrente-r1)=

### R1 — VVG § 168, *Kündigung des Versicherungsnehmers* — the rule that ends surrender at *Rentenbeginn*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__168.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted). **The provision was not read at article level**; its paragraph number, wording and the scope of the "*ohne Kapitalwahlrecht*" qualifier are all `[unverified]` (research gap 9)
- Used for: **the provision on which this product's entire "no surrender, no lapse, no paid-up" specification rests.** § 168 Abs. 3 VVG confines the right of termination in a *Rentenversicherung* without a *Kapitalwahlrecht* to the period before the annuity payments start, so for a *Sofortrente* the contract is **irrevocable from the outset**. It is cited in `product-spec.md` for the absence of a capital option, of a *Rückkaufswert* and of any lapse, and in `technical-notes.md` for the empty behavioural class, for the model carrying no lapse or surrender cells at all, and for the one qualification — a surrender right **may** survive inside an *Aufschubzeit*, on terms no carrier's document established, which is why the base run switches the deferment off

(delib-sofortrente-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` — recorded by the sibling file [R1 there] as returned by a search
- Retrieved: no — egress blocked; the content used is the sibling file's search record; the paragraph structure and the five-year spreading rule are `[unverified]`
- Used for: **its boundary, which is the point.** § 169 is displaced by § 168 Abs. 3 [R1] the moment the *Rentenbezug* begins, so `Sofort_DE_S` publishes **no surrender-value cells, no *Stornoabzug* and no five-year cost-spreading rule** — a specification rather than an omission, stated in that form in both documents and asserted by the test module's absent-names check

(delib-sofortrente-r4)=

### R4 — VVG § 163, *Anpassung der Prämie oder der Vertragsbestimmungen*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision, with commentary
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` — canonical form, `[unverified]`
- Retrieved: no — egress blocked; established at commentary level only, through the sibling file [R3, R17 there]
- Used for: the **immutability of the *garantierte Rente***. Both documents cite it, with [REG-R27], for § 163 being the only channel by which a German insurer could change the guaranteed annuity after conclusion, for that channel being narrow, and for the Landgericht Köln having narrowed it further by holding a low-interest phase to be entrepreneurial risk that cannot be passed to policyholders — **the case reference, date and parties were not established**. The model treats `annuity_guar_pp(t)` as level for life and records § 163 as a model risk

(delib-sofortrente-r5)=

### R5 — VVG § 165, *Prämienfreie Versicherung*, and § 166, *Kündigung des Versicherers*
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provisions
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` — recorded by the sibling file [R2 there] as returned by a search
- Retrieved: no — egress blocked
- Used for: **a boundary again.** § 165 gives the policyholder of a contract with recurring premiums the right to convert it to a premium-free one; a *Sofortrente* is bought with a single *Einmalbeitrag*, so **there is no future premium to cease and § 165 has no application to this product at all.** Both documents cite it for the absence of a `Beitragsfreistellung` decrement being a specification rather than a simplification

(delib-sofortrente-r8)=

### R8 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher / doc type: Deutsche Aktuarvereinigung e. V. (DAV), Cologne; press items, recorded by the sibling file [R8, R9 there] by title
- URL: not established
- Retrieved: no — egress blocked; the two titles are the sibling file's search record
- Used for: the single point that a contract written in 2026 sits on the **same interest basis** as one written in 2025, the DAV having recommended 1,0 % for both — which matters here because tariff vintage and contract vintage are the same date. Cited in `product-spec.md` beside [REG-R15] and [REG-R56]; the closing row of `hoechstrechnungszins_table.csv` carries it in its `provenance` tag

(delib-sofortrente-r10)=

### R10 — DAV, "Herleitung der DAV-Sterbetafel 2004 R für Rentenversicherungen"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *DAV-Richtlinie*, the profession's derivation guideline for the annuity table. In use since June 2004, for new business from 2005, the DAV document dated 22 February 2005, the derivation guideline reissued 28 June 2023
- URL: not established; the document and its 2023 reissue are recorded by the sibling file [R12 there]
- Retrieved: no — egress blocked; the content used is the sibling file's search record. **DAV 2004 R is DAV property, is not public and is not redistributed by delib**
- Used for: **the mortality basis of this product, structurally.** Four claims rest on it and each shapes the model. That DAV 2004 R is a ***Generationentafel***, mortality given per birth cohort with the expected improvement **inside** the table — which is why `birth_year` is a model point attribute, why `mort_rate_gen` takes a cohort, and why a period proxy is pitfall 8. That its component structure carries a **mortality trend in both a first- and a second-order version** — which is why the shipped proxy's first-order margin reaches the trend as well as the level and why collapsing them is pitfall 9. That first-order probabilities carry safety margins relative to the second-order realistic ones, and that for an annuity prudent means **lighter** mortality. And that the table carries an *Altersverschiebung* whose **convention was not established**, which `technical-notes.md` records as a condition on any replacement table (research gap 12)

(delib-sofortrente-r11)=

### R11 — DAV 2004 R-Bestand and the *Rentenbestandstafel* RBx
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; the companion table for the existing annuity book, paired with the new-business table in a 2004 presentation titled "DAV 2004 R und RBx"
- URL: not established; the pairing is recorded by the sibling file [R14 there]
- Retrieved: no — egress blocked
- Used for: **the pairing and nothing else.** `product-spec.md` cites it for the fact that a *Sofortrente* is priced on the new-business table at inception and then spends thirty years in the *Bestand* to which the other table applies, and — explicitly — for the disclosure that **the difference in level, in trend, in age range and in application rule between the two was not established**, so nothing about it is asserted downstream (research gap 12). `mort_table.csv`'s `provenance` names both tables as cited-not-shipped

(delib-sofortrente-r13)=

### R13 — EStG § 22 Nr. 1 Satz 3 Buchst. a Doppelbuchst. bb — the *Ertragsanteil* table
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` — recorded by the sibling file [R5 there] as **returned directly by a search**
- Retrieved: no — egress blocked; the general content is the sibling file's search record; the statutory address usually given for the table is itself `[unverified]`, and the schedule reproduced in `product-spec.md` is `[unverified]` in its entirety
- Used for: the product's tax logic, which is its main commercial argument. Both documents cite it for the annuity being taxed on the ***Ertragsanteil*** — the interest element deemed contained in the payment, a flat statutory percentage fixed by the annuitant's age at *Rentenbeginn* and never changed — and for the **one corroborated value, 18 % at age 65**, which is why the anchor cell's entry age is 65. The whole of the rest of the schedule carries `[unverified]` (research gap 15). Taxation falls on the annuitant and **is not a cash flow in this model** [REG-R41]

(delib-sofortrente-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6 — the *Kapitalabfindung* regime, and its boundary
- Publisher / doc type: Bundesministerium der Justiz / juris; statutory provision
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` — recorded by the sibling file [R6 there]
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: **a sharp boundary.** The *Halbeinkünfteverfahren* applies only to lump sums and payout-plan withdrawals and requires the 12/62 rule; a *Sofortrente* pays no lump sum and could not satisfy the twelve-year test in any event, so `product-spec.md` cites it, with [R13] and [REG-R45], for the whole of this product's cash flow being taxed under § 22 and **none of it under § 20** — which is precisely the arbitrage against a *Bankauszahlplan* the product is sold on

(delib-sofortrente-r18)=

### R18 — BaFin material on life-insurance product oversight
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin); *Merkblatt* 01/2023 (VA) on conduct supervision, the *Risiken im Fokus* cost section and the *Fachartikel* series, all recorded by the sibling KLV file [R17–R19 there]
- URL: not established
- Retrieved: no — egress blocked
- Used for: one disclosure only. All of the supervisor's *Wohlverhaltensaufsicht* material in the corpus is addressed to *kapitalbildende* products, i.e. the accumulation side, and **whether BaFin has published anything on payout annuities, or scrutinises *Rentenhöhe* or surplus declarations for value, was not established** — which is what `product-spec.md` cites at the point where it would otherwise have reported a value-for-money expectation for this product [REG-R35]

(delib-sofortrente-r19)=

### R19 — GDV / dieversicherer.de, "Private Rentenversicherung: Auszahlmöglichkeiten"
- Publisher / doc type: GDV under its consumer brand *Die Versicherer*; consumer article
- URL: `https://www.dieversicherer.de/versicherer/altersvorsorge/news/auszahlung-private-rentenversicherung-141750` — recorded by the sibling file [R21 there] from a search result
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: the industry association's own account of a private annuity's payout options, cited with [R20], [R21] and [R23] in both documents for the ***Überschussverwendung* taxonomy** — konstant, teildynamisch, volldynamisch and the *Bonusrente* — and for the election being made once, at *Rentenbeginn*, which for this product is inception. **No rate and no envelope was established from it**

(delib-sofortrente-r20)=

### R20 — Franke und Bornberg, "Altersvorsorge: Überschüsse im Rentenbezug — Teil 1: Die Qual der Wahl", and "Was bedeutet der Rentenfaktor und wie hoch ist er?"
- Publisher / doc type: Franke und Bornberg GmbH, Hannover — independent product-rating house; two blog articles, the second dated by its slug to 2021/2022
- URL: `https://www.franke-bornberg.de/blog/altersvorsorge-ueberschuesse-im-rentenbezug-teil-1-die-qual-der-wahl` and `https://www.franke-bornberg.de/de/blog/was-bedeutet-rentenfaktor-wie-hoch-2021-2022` — recorded by the sibling file [R19 there] from search results
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: the professional treatment of the choice between the *Überschussverwendung* forms — the documents' statement that all four distribute the same expected surplus and differ only in *when*, so there is no dominant answer, is cited to its title "Die Qual der Wahl" — and for the disclosure that the rating house's own article asking *how high* a *Rentenfaktor* is **returned no level, no range and no table** (research gap 5). It also stands behind `surplus_scale_table.csv`'s `provenance` tags

(delib-sofortrente-r21)=

### R21 — Consumer-organisation material on the *Sofortrente*
- Publisher / doc type: Finanztip Verbraucherinformation gemeinnützige GmbH; Stiftung Warentest (*Finanztest*); the *Verbraucherzentralen*
- URL: `https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/` and `https://www.finanztip.de/lebensversicherung-versteuern/` — recorded by the sibling file [R20 there]. **The *Sofortrente*-specific pages of all three publishers were not located and no URL for them is given**
- Retrieved: no — egress blocked; the content used is the sibling file's search record
- Used for: **the single most important qualitative claim in this product's documents** — that the *konstante Überschussrente* is constant **in intention only**, and that the annuity is reduced if the insurer earns less than projected. Both documents cite it for the *Überschussrente* being declared, non-guaranteed and **reducible**, for the [unverified] 15–25 % share of the payment that is at risk, and for the base run's decision to project a central estimate while the sensitivity section prices the downside. `product-spec.md` also records that **Stiftung Warentest's periodic *Sofortrente* comparison is the single most valuable unlocated document for this product**, whose existence is itself `[unverified]`

(delib-sofortrente-r22)=

### R22 — Assekurata, "Marktstudie Überschussbeteiligungen und Garantien"
- Publisher / doc type: Assekurata Assekuranz Rating-Agentur GmbH, Cologne; the market's annual survey of declared surplus rates, in its **24th edition, 2026**, per the sibling KLV file's search record [R25 there]
- URL: not established
- Retrieved: no — egress blocked; the title and edition number are the sibling file's search record
- Used for: the disclosure, made wherever the documents state that every surplus parameter is **[std]**, that the study which aggregates what [S10] publishes carrier by carrier yielded **no rate, no average, no range and no payout-phase breakdown** (research gap 4). Locating it is named as the third-highest-value action for a later build

(delib-sofortrente-r23)=

### R23 — Comparison-portal and broker cluster specific to the *Sofortrente*
- Publisher / doc type: `vergleich-sofortrente.de`; `lifefinance.de`; Verivox; CHECK24; and the German broker-blog cluster the sibling file records as [R24] there. **No individual page URL was recorded for any member** and none is given here
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session; every fact drawn from the cluster is corroborated by at least two of its members through the sibling file, and **none of them is a price**
- Used for: most of this product's **definitional mechanics**, which is why it is cited more often than any other reference. The *Rentengarantiezeit*: that the instalments continue to the beneficiaries until the agreed term expires, the durations offered (5 / 10 / 15 / 20 / 25 / 30+), the typical choices (15 years to retirement age 70, 10 years thereafter, most policyholders choosing 10 to 20), and the illustration of a 10-year period with death after 6. The *Kapitalrückgewähr* as the *Einmalbeitrag* less the instalments already paid. The *Bonusrente* ratchet — surplus buying a permanent paid-up increment — and the *Zinsüberschuss* definition. That the annuity is monthly [S7]. And the *Ertragsanteil* framing [R13]. **No price point, no *Rentenhöhe* and no charge was established from it** (research gap 5)

(delib-sofortrente-r25)=

### R25 — GDV statistics on *Einmalbeiträge* and the German annuity market
- Publisher / doc type: GDV; "Die deutsche Lebensversicherung in Zahlen" and the statistical series "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre", recorded by the sibling KLV file [R20, R21 there]
- URL: not established
- Retrieved: no — egress blocked
- Used for: the disclosure that there is **no sourced number anywhere in this product's documents for the size of the German *Sofortrente* market, the contracts in force, the average *Einmalbeitrag* or the average purchase age** (research gap 7). `product-spec.md` cites it with the reason that matters: the GDV series separates *Einmalbeiträge* from *laufende Beiträge*, but that line aggregates *Sofortrenten* with single-premium endowments, bAV contributions and *Zuzahlungen*, so **even a retrieved figure would not isolate this product**

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen;
research provenance in `_research/regulatory-actuarial.md`). **Every entry in that library
carries the same retrieval status as this file**: no document was fetched, and each entry
records per fact whether a web search corroborated it before the budget was exhausted. Entries
cited by the `sofortrente` documents:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the projected `liability_cf` feeds.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries and the treatment of future discretionary benefits, which is where a *Sofortrente*'s *Überschussrente* would sit in a valuation.
- **REG-R3** — Directive (EU) 2025/2, the Solvency II review: context for the framework these cash flows will be measured under.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve a valuation layer discounts on, and the reason pitfall 16 insists the tariff *Rechnungszins* is not that curve.
- **REG-R5** — VAG 2016 and its Anlage 1 *Sparten*: the statutory classification of the contract.
- **REG-R6** — VAG §§ 74–110: valuation, best estimate and risk margin, cited in the valuation pointers.
- **REG-R7** — VAG §§ 124–125, *Anlagegrundsätze* and *Sicherungsvermögen*: the annuity fund is general-account capital, not an *Anlagestock*.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and equal treatment: the supervisory frame around the tariff.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test on *Bewertungsreserven*: why the *Bewertungsreserven* share is referenced and not modelled.
- **REG-R10** — VAG §§ 140 and 145, the *Rückstellung für Beitragsrückerstattung*: where a declared *Überschussrente* is paid from.
- **REG-R11** — VAG §§ 141–143, the *Verantwortlicher Aktuar* and the 1994 deregulation: who signs the tariff bases off.
- **REG-R12** — VAG §§ 221–236 and Protektor, the *Sicherungsfonds*: what stands behind a lifelong promise, referenced in the product's risk section.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the reserving-rate cap `check_tariff_int_rate` tests against.
- **REG-R15** — the *Höchstrechnungszins* rate history and the regulation setting **1,00 % from 1 January 2025**, the first increase since 1994: the source of `hoechstrechnungszins_table.csv` and of the anchor cell's `tariff_int_rate`.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: cited for its **inapplicability** — there is no premium stream to zillmer against.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: the reserve that competes with the *Überschussrente* for the same RfB, referenced as a driver and never computed.
- **REG-R18** — MindZV: the statutory minimum share of each result that must reach policyholders, which bounds the discretion behind every **[std]** surplus figure — and, for an annuity, the floor under the *Risikoüberschuss* that longevity experience generates.
- **REG-R19** — RfBV, the collective part of the RfB: the mechanics behind the declaration.
- **REG-R20** — LVRG 2014: the reform that reshaped the *Bewertungsreserven* rule this product's payout phase participates in.
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): the statute the product's contract-law facts come from, and the reason § 168 Abs. 3 [R1] cannot be contracted around to the policyholder's disadvantage.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the withdrawal window, which is not modelled because a *Sofortrente* has no lapse machinery to absorb it into.
- **REG-R24** — VVG § 153: the cross-product entry behind the statutory *Überschussbeteiligung* and the *hälftige* share of *Bewertungsreserven* that [S3] evidences continuing into the payout phase.
- **REG-R25** — VVG §§ 154–155, *Modellrechnung* and *Standmitteilung*: the statutory basis of the document class [S15] belongs to, and what makes its absence here a real gap.
- **REG-R26** — VVG §§ 150, 159–162: consent of the *versicherte Person* and the *Bezugsberechtigung* machinery that makes the *Rentengarantiezeit* and the *Hinterbliebenenrente* work as contract law. The beneficiary is a pass-through in the model.
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: cited with [R4] wherever the documents state that the *garantierte Rente* is immutable.
- **REG-R28** — VVG §§ 165–170: the cross-product entry behind [R1], [R2] and [R5] — *prämienfreie Versicherung*, *Kündigung*, *Rückkaufswert* and the *Stornoabzug*, none of which this product has.
- **REG-R30** — VVG §§ 19, 37, 38, 157: the *Altersangabe* correction rule, which matters here because the annuity is priced entirely off an age.
- **REG-R31** — VVG §§ 6, 7 and the VVG-InfoV: the disclosure regime that generates the *Verbraucherinformation* class [S2] [S3] [S14] and the *Effektivkosten* figure that was not established.
- **REG-R32** — PRIIPs, Regulation (EU) No 1286/2014: the regime behind [S12], and the source of the *Renditeminderung* form no instance of which was located.
- **REG-R33** — IDD and § 34d GewO: the distribution regime behind the *Produktinformationsblatt* class [S11].
- **REG-R34** — Unisex: CJEU C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG. **The single most consequential cross-product entry for this model**: it is why `mort_rate_tariff` reads the blended `"U"` series and never the model point's own `sex`, and why pitfall 10 exists.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener Kundennutzen*: cited with [R18] for what is addressed to accumulation products and not to payout annuities.
- **REG-R36** — the BGH line of authority on German life contracts: the interpretive background to the AVB facts, and to the narrowing of § 163 [R4].
- **REG-R37** — GDV *Musterbedingungen* and German market practice: the cross-product entry behind [S1] and [S9].
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: what places this contract in **Schicht 3** — no deduction going in, *Ertragsanteil* coming out.
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a: the cross-product carrier of the *Ertragsanteil* rule behind [R13], and the entry the documents cite for taxation falling on the annuitant rather than on the insurer's liability.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6, the 12/62 rule: cited with [R14] for the boundary a *Sofortrente* can never cross.
- **REG-R46** — ErbStG and SGB V §§ 226, 229, 240: the *Erbschaftsteuer* treatment of a post-death payment and social-contribution treatment of an annuity in payment, both **not established** for this product (research gap 15).
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables: the entry behind the two-dimensional *Sicherheitszuschlag* — lighter level **and** stronger trend — and behind the statement that the DAV tables are not redistributed here.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand, the generational annuity tables: the cross-product entry behind [R10] and [R11], and the authority for the generational structure a replacement table must preserve.
- **REG-R52** — Destatis *Sterbetafeln* and *Generationensterbetafeln*, with their reuse licence: the intended base for a user-supplied replacement decrement table, and the comparator for the statement that population mortality overstates deaths in an annuity book.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen & Morgen, Franke und Bornberg): the cross-product carrier of the market statistics [R25] and [R22] could not supply.
- **REG-R54** — HGB §§ 341–341o and RechVersV: the statutory accounts in which the *Bewertungsreserven* the model excludes are measured.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: one of the two liability measures these cash flows feed; not computed here.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this documentation sits under, and the cross-product carrier of [R8].

---

## Provenance note

Extraction details — which fact was read from which document, the section-by-section
mechanics, and the nineteen-item gaps-and-caveats register — live in
`_research/sofortrente.md`, which is the citation ground truth for the S# and R# numbering
used here. The caveats that most affect what these product documents can claim are these.
**No search was run for this product at all**, so of fifteen primary entries exactly two name
the immediate annuity in their titles ([S2], [S4]) and **neither yielded a single clause**;
four are document classes with no instance located ([S11], [S12], [S13], [S15]); and the
remaining nine are deferred-annuity or shared-chassis documents used because the two products
share their machinery. **No paragraph number, clause heading or sentence of contractual
wording for a German *Sofortrente* appears anywhere in the corpus**, and none was invented.
**No *Rentenhöhe* and no *Rentenfaktor* level was established at any carrier for any year** —
the largest quantitative hole, and the number the product is actually bought on — so
`product-spec.md`'s annuity table is **constructed** from stated annuity mathematics on a
printed proxy basis and every cell of it is **[std]**; the claim that annuity levels moved
with the *Höchstrechnungszins* is directionally supported by the tariff formula [S6] and the
statutory rate history [REG-R15] and is quantitatively **[std]**. **No *Überschussbeteiligung*
rate was established, in either phase, for any year, at any carrier**, so every surplus figure
is **[std]** and belongs to the insurer-discretionary class. **No charge parameter was
established**, and whether a payout-only *Sofortrente* is even within PRIIPs scope is itself
unresolved [S12] [REG-R32]. **§ 168 Abs. 3 VVG was not read at article level** [R1], although
its substance is the uniform statement of the consumer literature and the economic
precondition for writing annuities at all. **DAV 2004 R is established structurally and not
numerically** [R10], its *Bestand* companion barely at all [R11], and both are DAV property
that delib cites by name and never ships — so the shipped decrement CSV is a **[std]** proxy
anchored to reproduce the worked example, and the `Data` docstring says so. And the payment
timing was not established for this product or for the deferred one [S7] [R23]: *vorschüssig*
is a **[std]** convention, and the research file's own estimate of what the alternative is
worth is wrong by a factor of twelve — an annual-annuity identity applied to a monthly
annuity. The research file is frozen and is not amended; the correction is recorded in
`technical-notes.md`, which measures the difference at 0,34 % directly from model points 1
and 9.
