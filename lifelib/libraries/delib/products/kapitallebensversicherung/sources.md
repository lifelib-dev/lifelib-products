# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/kapitallebensversicherung.md` (the
citation ground truth for this product) and are **frozen — never renumber**. Unused sources are
omitted, so the numbering has gaps: **S14** (CosmosDirekt, "Erlebensfall: Was ist das und wie
läuft die Auszahlung?" — located, but the fused search summary attributed no statement to it, so
nothing in the product documents rests on it) and **R31** (the EUROPA Lebensversicherung and
Deutsche Lebensversicherungs-AG *Geschäftsberichte* 2024 — recorded in the research file as
locatable primary sources of per-undertaking *Stornoquoten* and cost ratios, with **no content
established**) are **not cited** by `product-spec.md`, `technical-notes.md` or `model.md` and are
therefore absent below. Access date for all sources: **2026-08-29**. No sources were newly added
at drafting. Cross-product [REG-R#] tags are listed in their own section at the end.

**The retrieval conditions, stated plainly, because they are unlike the sister libraries'.** Two
independent limits applied while this library was built, and both bear on every entry below.
First, **direct HTTP egress is blocked by an organisation network policy**: `WebFetch` and `curl`
are refused (HTTP 403 at the egress gateway) for every host outside a short package-registry
allowlist, and `gesetze-im-internet.de`, `bafin.de`, `gdv.de`, `aktuar.de`,
`bundesfinanzministerium.de`, `dejure.org`, `buzer.de`, `destatis.de` and `de.wikipedia.org` were
all tried and all refused. **Not one document listed here was retrieved** — not a *Bedingungswerk*,
not a *Basisinformationsblatt*, not a statutory text, not a BaFin *Merkblatt*. Everything rests on
`WebSearch` result summaries: real evidence, sometimes reproducing several sentences of a page,
but a **secondary summary and never a retrieved document**. Second, the session's shared
`WebSearch` budget of 200 calls was exhausted after **24 searches** on this product, which is why
the statutory and supervisory core is researched to a usable depth and the insurer-by-insurer
parameter sweep is not. A delib citation is therefore a **pointer, not a certificate**: it names
the instrument a claim should be checked against; it does not assert that anyone checked it.
Where a German sentence appears in a source entry, the quotation is of the **search-result
summary** and not of the instrument. Every URL below was returned by a search or is the obvious
canonical form of one; where there is none, the entry says `URL: not established` rather than
guessing.

---

## Primary product sources

(delib-kapitallebensversicherung-s1)=

### S1 — GDV, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung" (Musterbedingungen)
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V.; *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt or ignore, the GDV stating their use to be **unverbindlich** and purely optional
- URL: https://www.gdv.de/resource/blob/6348/075948efa290a72d0bb062dec766f56f/allgemeine-bedingungen-fuer-die-kapitalbildende-lebensversicherung-pdf-data.pdf (index: https://www.gdv.de/gdv/service/musterbedingungen)
- Retrieved: **NO** — direct HTTP egress blocked in the build environment; established from search-result summaries. **No article text beyond the § 1 heading "Welche Leistungen erbringen wir?" was returned**
- Used for: the existence of a market-wide model wording and the second-person, question-headed drafting style of post-2008 VVG AVB; and — negatively, and stated in the specification — that **no benefit, surplus, surrender or paid-up rule anywhere in these documents is attributed to S1**, each being attributed instead to the statute it implements or to a named carrier's wording

(delib-kapitallebensversicherung-s2)=

### S2 — GDV, "Jährliche Mitteilung zum Stand Ihrer Versicherung" (Muster-Standmitteilung, kapitalbildende Lebensversicherung, 02/2017)
- Publisher / doc type: GDV; model *Standmitteilung*, the annual statement sent to the policyholder, edition 02/2017
- URL: https://www.gdv.de/resource/blob/6302/890c551440e2d065eba74180437f6970/5-gdv-muster-standmitteilung-kapitalbildende-lebensversicherung-02-2017-data.pdf
- Retrieved: **NO** — egress blocked; established at the level of title, edition and subject only. **The field list itself was not established**, so any statement about its actual contents is [unverified]
- Used for: the four quantities a German endowment reports side by side each year — the guaranteed *Versicherungssumme*, the accumulated *Überschussguthaben*, the current *Rückkaufswert* and the current *beitragsfreie Versicherungssumme* — which are exactly the state variables the projection carries, and the statutory *Standmitteilung* duty in the specification's regulatory context

(delib-kapitallebensversicherung-s3)=

### S3 — Debeka Lebensversicherungsverein a. G., Bedingungswerk **B LV 85** (edition 01.07.2026)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G.; AVB for a kapitalbildende Lebensversicherung tariff, **21 pp.** (the running header "B LV 85 (01.07.2026) Seite 1 von 21" was reproduced in the search result). The **most recent** German endowment wording located, and the only carrier document in the corpus with quantified terms
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV85.pdf
- Retrieved: **NO** — egress blocked; established from search-result summaries. The *Überschussbeteiligung* clause numbering is tariff-dependent and any specific section number is [unverified]
- Used for: **the single most load-bearing mechanical fact in the corpus** — *Zinsüberschussanteile* and *Schlussüberschussanteile* are each fixed as a **percentage of the *Deckungskapital* calculated at the allocation date**, which is what fixes the model's `surplus_base_pp` as the reserve rather than the sum insured or the premium; the declared level being set **annually**, unguaranteeable and dependent on capital-market development and the insurer's own results, which is why `decl_rate` is a scenario; and the quantified *Stornoabzug* — a standard 5 % deduction plus a *kapitalmarktabhängige Stornogebühr* of 5 %, 10 % or 15 % of the *Deckungskapital* — which is the one observation the `storno_rate` schedule is set against

(delib-kapitallebensversicherung-s4)=

### S4 — Debeka, Bedingungswerk **B LV 86** (edition 01.01.2025)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G.; AVB for a kapitalbildende Lebensversicherung tariff, **19 pp.**
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV86.pdf
- Retrieved: **NO** — egress blocked; identity, edition date and page count established, substantive content not separately attributable
- Used for: the evidence that **one insurer maintains at least three parallel endowment wordings of different vintages**, which is the specification's variation argument and part of why the model treats `rechnungszins` and both DeckRV ceilings as cohort facts; and, with S5, for the observation that a German endowment wording runs to roughly 18–21 pages

(delib-kapitallebensversicherung-s5)=

### S5 — Debeka, Bedingungswerk **B LV 97** (edition 01.01.2025)
- Publisher / doc type: Debeka Lebensversicherungsverein a. G.; AVB for a kapitalbildende Lebensversicherung tariff, **18 pp.**
- URL: https://www.debeka.de/content/dam/de/webauftritt/vertragsgrundlagen/lebens-rentenversicherung/BLV97.pdf
- Retrieved: **NO** — egress blocked; identity, edition date and page count established only
- Used for: the third member of the 85 / 86 / 97 triple, and with S4 for the disclosure in the specification and in `model.md` that **no carrier in this corpus publishes a mortality basis, an expense loading or a commission scale**, so every such level in the model is [std]

(delib-kapitallebensversicherung-s6)=

### S6 — Debeka, "Vertragsgrundlagen und weitere Informationen (Bedingungswerke, Tarifbedingungen, IPID etc.)" — Kapitalbildende Lebensversicherung
- Publisher / doc type: Debeka; insurer document-library index page
- URL: https://www.debeka.de/service/bedingungen/Lebensversicherung___Rentenversicherung/Lebensversicherung/Kapitalbildende_Lebensversicherung/index.html
- Retrieved: **NO** — egress blocked; page title and taxonomy established from the search result
- Used for: the fact that **"Kapitalbildende Lebensversicherung" is a live product category in a major German insurer's own taxonomy** at the access date, which is the specification's market-role anchor on the manufacturer side; and the document types a German carrier publishes per product — *Bedingungswerke*, *Tarifbedingungen* and an **IPID** — the German market labelling the pre-contractual summary with the EU IDD term

(delib-kapitallebensversicherung-s7)=

### S7 — Gothaer, "Allgemeine Versicherungsbedingungen für die kapitalbildende Lebensversicherung"
- Publisher / doc type: Gothaer; AVB, served from the broker portal `partner.gothaer.de` through a streaming endpoint carrying a `scope` parameter, so it may not resolve for a public reader even without the egress block
- URL: https://partner.gothaer.de/StreamingServlet/app/dvz/DocumentDownload/215401?scope=makler_scope
- Retrieved: **NO** — egress blocked. The summary matched a group of documents and **did not separate Gothaer's wording from the others in it**, so the statements below are recorded with that warning
- Used for: payment of the agreed *Versicherungssumme* at the *Ablauftermin* named in the *Versicherungsschein* and the *Versicherungsschein* having to be submitted to claim; the reduction of the sum insured **in whole or in part** to a *beitragsfreie Versicherungssumme*; and — the operative rule a projection is most likely to get wrong — that **on death before the *Ablauftermin* no further premiums are due**, which is `prem_charged_pp`'s cessation rule and pitfall 11

(delib-kapitallebensversicherung-s8)=

### S8 — die Bayerische, "Allgemeine Bedingungen für die kapitalbildende Lebensversicherung", document **B 510121**
- Publisher / doc type: BL die Bayerische Lebensversicherung AG; AVB for a *Kapital-Lebensversicherung*. **The existence of this document is contested within the search evidence**: one search returned the URL under this title, a narrower search returned its sibling documents but not it and reported it "may not be publicly available online"
- URL: https://www.diebayerische.de/dam/jcr:e5f5f192-0edc-49b1-9be8-18c3cc503ae3/510121_avb_kapital-lebensversicherung.pdf
- Retrieved: **NO** — egress blocked; the URL was returned by a search and is recorded verbatim, **no content was established from it**, and its availability is [unverified]
- Used for: nothing substantive. It is cited in the specification only to record the contradiction rather than resolve it, and to count a fourth carrier in the variations table with the note that no term of the wording is known

(delib-kapitallebensversicherung-s9)=

### S9 — die Bayerische, AVB **Klassikrente** (B 520136, 01.2025) and AVB **gezillmerte Klassikrente** (B 520127, 01.2022)
- Publisher / doc type: BL die Bayerische Lebensversicherung AG; AVB for a *klassische Rentenversicherung* in a *gezillmert* and a non-*gezillmert* edition — **an annuity, not an endowment**, recorded as the nearest sibling wording found and used only where the rule transfers, which is said wherever the fact is used
- URL: https://www.diebayerische.de/dam/jcr:0936fd6c-71b9-453d-83f6-57ec76a76697/520136_avb_klassikrente.pdf and https://www.diebayerische.de/dam/jcr:0dcd832e-9107-44b4-a967-5e504c5c6fce/520127_avb_gezillmert_klassikrente.pdf
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: **the surplus allocation timing** — *Zinsüberschussanteile* allocated at each *Bilanzstichtag*, being 31 December, and **booked into the *Deckungskapital*** — which is the model's annual, period-end, reserve-crediting convention and the [std] shift of the *Bilanzstichtag* to the policy-year end; **entitlement beginning with the start of cover**, with no qualifying period, which is why `surplus_credit_pp` runs from `t_start()`; the statement that the future level **cannot be guaranteed and may be zero euros**, which is the `nil` scenario made runnable; and the existence of a *gezillmerte* and a non-*gezillmerte* edition of the **same** tariff, which is why `zillmer_on` is a model point column and model point 13 exists

(delib-kapitallebensversicherung-s10)=

### S10 — ÖSA, "Basisinformationsblatt — ÖSA StarthilfePlus (laufende Beitragszahlung)"
- Publisher / doc type: ÖSA Versicherungen; **PRIIP-Basisinformationsblatt**, 3 pp., for a regular-premium variant of a product named *StarthilfePlus*
- URL: https://www.oesa.de/export/sites/oesa/_resources/download/privat/service/bib/OeSA-StarthilfePlus_laufend_20.pdf
- Retrieved: **NO** — egress blocked. **Whether *StarthilfePlus* is an endowment, an annuity or a children's savings contract was not established**, and none of its risk-indicator, performance-scenario or cost figures were
- Used for: the fact that it is the **only actual PRIIP-BIB PDF for a German capital-forming life product located in this research**, cited in the specification's charges section to support the disclosure that **no *Effektivkosten* figure of any kind reached these documents** and that every charge level in the model is therefore [std]

(delib-kapitallebensversicherung-s11)=

### S11 — Allianz, "Kapitallebensversicherung: Ihr umfassender Ratgeber", with "Lebensversicherung: Arten im Überblick" and "Lebensversicherung Auszahlung: Ablauf & Steuer"
- Publisher / doc type: Allianz Lebensversicherungs-AG; three insurer product and guide pages on the German consumer site
- URLs: https://www.allianz.de/vorsorge/kapitallebensversicherung/ · https://www.allianz.de/vorsorge/lebensversicherung/ · https://www.allianz.de/vorsorge/lebensversicherung/auszahlung/
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: **the only declared rate in the corpus attached to a classic *endowment* book by its manufacturer — a *laufende Verzinsung* of 2,70 % for 2026** — which is `decl_rate` on the `base` scenario and the anchor cell's 1,70 pp interest surplus; the three-part description of the *klassisch* variant (guaranteed interest, savings component, death cover) that the specification's overview mirrors; the statement that the *Rückkaufswert* **can be below the premiums paid, especially in the early contract years**, with the investment return and the *Überschussbeteiligung* included in it — the economic signature of *Zillmerung*; and the market-role finding that the product "is rarely newly concluded today"

(delib-kapitallebensversicherung-s12)=

### S12 — ERGO, "Ratgeber Kapitallebensversicherung"
- Publisher / doc type: ERGO Group; insurer guide page
- URL: https://www.ergo.de/de/Ratgeber/finanzielle_vorsorge/kapitallebensversicherung
- Retrieved: **NO** — egress blocked. It contributed to a **fused** typical-parameters summary and **no statement was separately attributable to it**
- Used for: the group attribution behind the specification's typical-parameter table — term band, minimum sum insured and the *Sparanteil* / *Risikoanteil* / *Kostenanteil* decomposition of the premium — every row of which carries the group tag and a [std] mark, and none of which is used as a model parameter without one

(delib-kapitallebensversicherung-s13)=

### S13 — Sparkasse, "Kapitallebensversicherung — Für Rente & Familie vorsorgen"
- Publisher / doc type: Deutscher Sparkassen- und Giroverband; distributor product and guide page
- URL: https://www.sparkasse.de/pk/produkte/versicherung/vorsorge-und-risiko/lebensversicherung/kapitallebensversicherung.html
- Retrieved: **NO** — egress blocked; one of the pages behind the fused typical-parameters summary
- Used for: the distribution finding that the German endowment is sold through the **savings-bank network** as well as through tied agents and brokers, which the specification uses to argue that the *Vertriebsweg* drives the acquisition-cost level and that a single [std] commission scale stands for a range it cannot observe; and the same group attribution as S12

(delib-kapitallebensversicherung-s15)=

### S15 — Verivox, "Kapitallebensversicherung", "Überschussbeteiligung" and "Zillmerung"
- Publisher / doc type: Verivox GmbH, a comparison portal — **secondary**, not a product document; three consumer explainer pages
- URLs: https://www.verivox.de/kapitallebensversicherung/ · https://www.verivox.de/lebensversicherung/themen/ueberschussbeteiligung/ · https://www.verivox.de/lebensversicherung/themen/zillmerung/
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the second independent statement of the ***Höchstzillmersatz*** rule — the LVRG cut the maximum from **40 ‰ to 25 ‰** and since 1 January 2015 it may not exceed **2,5 % of the *Beitragssumme***, with only that much recognisable in the balance sheet as *Abschluss- und Vertriebskosten* — which is `deckrv_table.csv`'s second column and `check_zillmer_cap()`; and the four-component surplus split and the *Überschussverwendung* systems in the specification's mechanics sections

(delib-kapitallebensversicherung-s16)=

### S16 — Finanztip, "Überschussbeteiligung Lebensversicherung: Arten & Höhe" and "Steuer auf Lebensversicherung"
- Publisher / doc type: Finanztip Verbraucherinformation gGmbH — **secondary**, consumer journalism; two explainers
- URLs: https://www.finanztip.de/lebensversicherung/ueberschussbeteiligung-lebensversicherung/ · https://www.finanztip.de/lebensversicherung-versteuern/
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the clearest secondary statement of the **four-component surplus split** — *Zins-*, *Risiko-*, *Kostenüberschuss* and the *Schlussüberschussanteil* — and the consumer-facing quotas ("at least 90 % of the *Zins-* and *Risikoüberschuss*, half of the *Kostenüberschuss*"), which the specification records **beside** the MindZV framing at [R6] and expressly does not treat as the same rule; and the *Schlussüberschussanteil* arising from long-run results not fully allocated during the term and paid at termination, which is `term_bonus_pp`'s accrual shape

(delib-kapitallebensversicherung-s17)=

### S17 — HUK24, "Überschussbeteiligung der Risikolebensversicherung"
- Publisher / doc type: HUK24 AG (HUK-COBURG group); insurer guide page — **about term life, not endowment**
- URL: https://www.huk24.de/risikolebensversicherung/ratgeber-lebensversicherung/ueberschussbeteiligung
- Retrieved: **NO** — egress blocked. **No endowment-specific statement is taken from it**
- Used for: the corroboration that the four-component surplus vocabulary is used **across product lines by carriers themselves** and not only by journalists — which is what lets the specification present the four components as market vocabulary rather than as a commentator's construct

(delib-kapitallebensversicherung-s18)=

### S18 — "Bedingungen und Verbraucherinformationen für die Kapital bildende Lebensversicherung" (third-party contract-clause mirror)
- Publisher / doc type: publisher **not established**; hosted on `lawinsider.com`, a contract-clause database, in its German-language section; a mirror of an unnamed German insurer's *Bedingungen und Verbraucherinformationen*. The issuing insurer is [unverified]
- URL: https://lawinsider.com/de/contracts/duGC9LpAVlC
- Retrieved: **NO** — egress blocked. **Only the title was established**, and **nothing substantive is cited from it**
- Used for: one thing only — the **document pair** the German market actually delivers to a customer, *Bedingungen* **and** *Verbraucherinformationen*, which is the vocabulary the specification uses for the contract documentation set and the German counterpart of the French *conditions générales* plus *notice d'information* pair

---

## Regulatory and actuarial references (product research numbering)

(delib-kapitallebensversicherung-r1)=

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher: Bundesministerium der Justiz (Gesetze im Internet); mirrored by dejure.org and buzer.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__153.html · https://dejure.org/gesetze/VVG/153.html
- Retrieved: **NO** — egress blocked; established from search-result summaries. **No version date, no *Fassung* line and no amending statute later than the LVRG 2014 were returned**, so the reading is "current in substance as reported in August 2026" and is not version-pinned
- Used for: Abs. 1 — the entitlement to share in the surplus **and** the *Bewertungsreserven* unless excluded by express agreement, and only **entirely**, which is why the specification says there is no partially participating German endowment; Abs. 2 — the *verursachungsorientiertes Verfahren*, which allocation in proportion to reserve implements; Abs. 3 — annual redetermination of the *Bewertungsreserven* and the **half share on termination**, which is `bwr_rate`'s mechanism; and the LVRG-form Satz 3 proviso subordinating that determination to supervisory rules

(delib-kapitallebensversicherung-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de and buzer.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__169.html · https://dejure.org/gesetze/VVG/169.html
- Retrieved: **NO** — egress blocked; the Abs. 3 sentence reproduced in the research file is a quotation **of the search-result summary**, not of the statute
- Used for: **the whole surrender construction**. The five requirements of Abs. 3 — a *Deckungskapital*, computed by recognised actuarial rules, on the ***Rechnungsgrundlagen der Prämienkalkulation***, struck **at the end of the current *Versicherungsperiode***, and on *Kündigung* floored by the *Mindestrückkaufswert* — which are `res_guar_pp`'s four design decisions including its reading of the reserve at `t + 1`; the floor itself as the reserve obtained by spreading the *angesetzte Abschluss- und Vertriebskosten* **evenly over the first five contract years**, which is `res_min_pp`; the *Zeitwert* branch that governs a *fondsgebundene* contract and **not** this one; and the *Abzug* being permissible only where *vereinbart*, *beziffert* and *angemessen*, with a deduction for unrecovered acquisition costs void

(delib-kapitallebensversicherung-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de, LexMea and dejure.org
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__165.html · https://dejure.org/gesetze/VVG/165.html
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the *Beitragsfreistellung* right at the end of the current *Versicherungsperiode* **provided the agreed *Mindestversicherungsleistung* is reached**, and the failure branch in which the insurer must instead pay the *Rückkaufswert* including *Überschussanteile* under § 169 — the two branches `is_paid_up` and `lapse_rate` implement and model points 11 and 12 exercise; the paid-up sum being calculated **on the basis of the *Rückkaufswert* under § 169 Abs. 3 bis 5**, which is `bfz_si_pp` and why the paid-up sum inherits the five-year floor; the schedule being contractual and tabulated *für jedes Versicherungsjahr*; and the practical note that attached *Zusatzversicherungen* are regularly lost on paid-up

(delib-kapitallebensversicherung-r4)=

### R4 — VVG § 161, *Selbsttötung*
- Publisher: Bundesministerium der Justiz; mirrored by dejure.org, lxgesetze.de and rewis.io
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__161.html · https://rewis.io/gesetze/vvg/p/161-vvg/
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the insurer being *leistungsfrei* on an intentional suicide **within three years of conclusion**, the exception where free determination of the will was excluded by a *krankhafte Störung der Geistestätigkeit*, the three-year period being extendable by individual agreement, and — the rule the model turns on — that the insurer must nevertheless **pay the *Rückkaufswert* including *Überschussanteile* under § 169**, so the German rule is a benefit **substitution** and not a forfeiture. That is `benefit_death_pp`'s first-three-years branch and pitfall 7

(delib-kapitallebensversicherung-r5)=

### R5 — VVG § 19, *Vorvertragliche Anzeigepflicht*
- Publisher: Bundesministerium der Justiz; commentary from ra-zn.de and fairtest.de
- URLs: https://www.gesetze-im-internet.de/vvg_2008/__19.html · https://www.ra-zn.de/anzeigepflicht-19-vvg
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the question-bounded disclosure duty (*gefahrerhebliche Umstände* asked about in *Textform*); the insurer's right to accept **with restrictions** or **only at an increased premium**, which is what `rating_factor` represents; the retrospective adjustment remedies — exclusion of the undisclosed risk or a ***Risikozuschlag*** — as the usual outcome for negligent breach; and the five- and ten-year limits on those rights, in the specification's underwriting section

(delib-kapitallebensversicherung-r6)=

### R6 — MindZV, *Verordnung über die Mindestbeitragsrückerstattung in der Lebensversicherung*
- Publisher: Bundesministerium der Justiz; mirrored by lxgesetze.de and buzer.de
- URLs: https://www.gesetze-im-internet.de/mindzv_2016/BJNR083100016.html · https://lxgesetze.de/mindzv/6
- Retrieved: **NO** — egress blocked; the `mindzv_2016` / `BJNR083100016` identifiers indicate the 2016 consolidation
- Used for: the minimum allocations to the *Rückstellung für Beitragsrückerstattung* — **90 %** of the *anzurechnende Kapitalerträge* under § 3 Abs. 1, **90 %** of the *Risikoergebnis*, **50 %** of the *übriges Ergebnis*, with the *Aufwand für die Diskontierung der Deckungsrückstellung* deducted before the 90 % is struck — which the specification presents as the **origin** of the surplus and expressly not as what determines a declared rate; and the separate *Altbestand* / *Neubestand* computation

(delib-kapitallebensversicherung-r7)=

### R7 — DeckRV — *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher: Bundesministerium der Justiz; buzer.de carries the amendment history
- URL: https://www.buzer.de/gesetz/12006/index.htm
- Retrieved: **NO** — egress blocked. The *Bundesgesetzblatt* announcement date was returned as "24 July" with the **year inferred** to be 2024 from the surrounding chronology; that inference is [unverified]
- Used for: **the two cohort ceilings the model keys on `issue_year`** — the *Höchstrechnungszins* raised from 0,25 % to **1,00 % with effect from 1 January 2025**, the first increase since 1994, against a history falling from 4 % in 1994 to 0,25 % in 2022; and the *Höchstzillmersatz* of **25 ‰ of the *Beitragssumme***, cut from 40 ‰ by the LVRG with effect from 1 January 2015. Those are `deckrv_table.csv`'s two value columns, `check_rechnungszins_cap()` and `check_zillmer_cap()`, and `alpha_rate` sitting at the ceiling

(delib-kapitallebensversicherung-r8)=

### R8 — VAG § 139, *Überschussbeteiligung*, and the *Sicherungsbedarf*
- Publisher: Bundesministerium der Justiz; summary obtained through dejure.org
- URL: https://dejure.org/gesetze/VAG/139.html
- Retrieved: **NO** — egress blocked; established from a search-result summary. The ***Sockelbetrag*** reported by one weak secondary source has no corroboration and its existence, base and size are [unverified]
- Used for: the half share in the *Bewertungsreserven* and, decisively for the model, the restriction that **exiting policyholders participate only to the extent the reserves exceed the *Sicherungsbedarf*** arising from contracts with an interest guarantee — the reason `bwr_rate = 0` in the base run rather than being a nominal half share, and the reason the specification says the mechanism is established while the **amount is not**

(delib-kapitallebensversicherung-r9)=

### R9 — VVG-InfoV § 2, and the *Effektivkosten* disclosure
- Publisher: Bundesministerium der Justiz; mirrored by buzer.de; explained by the Institut für Finanz- und Aktuarwissenschaften (ifa Ulm)
- URLs: https://www.gesetze-im-internet.de/vvg-infov/__2.html · https://www.buzer.de/gesetz/8025/a153312.htm
- Retrieved: **NO** — egress blocked; established from search-result summaries. The date of the *Effektivkosten* amendment the ifa note concerns **was not established**
- Used for: the duty to disclose the *Abschluss- und Vertriebskosten* included in the premium **in euro amounts** (§ 7 Abs. 2 und 3 VVG i. V. m. §§ 2 und 3 VVG-InfoV); and the ***Effektivkostenquote* (Reduction in Yield)**, mandatory in quotations from 1 January 2015, which the technical notes name as a **validation target rather than an input** — reproducing one needs the PRIIPs Annex VI algorithm and a holding period, neither of which this library implements

(delib-kapitallebensversicherung-r10)=

### R10 — EStG § 20 Abs. 1 Nr. 6, and the *Einkommensteuer-Handbuch* annex
- Publisher: Bundesministerium der Finanzen (amtliches Einkommensteuer-Handbuch); commentary from NWB and Haufe
- URLs: https://esth.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-22a/I/inhalt.html · https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html
- Retrieved: **NO** — egress blocked; the current locus of the age-62 rule (cited to § 52 Abs. 36 Satz 9 EStG) is [unverified], § 52 having been renumbered repeatedly
- Used for: the ***Unterschiedsbetrag*** as the taxable amount and the **half-income rule** on payment after twelve years and after completion of the 60th — for contracts concluded after 31 December 2011, the **62nd** — year of life; the personal marginal rate rather than the *Abgeltungsteuer* where the halving applies. **The tax rules do not enter the projected cash flows**: they fix the anchor cell's twenty-five-year term ending at attained age 62, and the lapse table's twelve-year shape

(delib-kapitallebensversicherung-r11)=

### R11 — BMF-Schreiben of 1 October 2009, IV C 1 - S 2252/07/0001
- Publisher: Bundesministerium der Finanzen; *BMF-Schreiben*, binding administrative guidance to the tax offices
- URL: https://datenbank.nwb.de/Dokument/351401/ (NWB database record)
- Retrieved: **NO** — egress blocked. The reference and date were returned by a search; **no paragraph of its text was established**
- Used for: nothing substantive. It is cited in the specification's regulatory context solely to name the administrative guidance under which the *Mindesttodesfallschutz* test at [R12] is applied, and to record that its text did not reach these documents

(delib-kapitallebensversicherung-r12)=

### R12 — *Mindesttodesfallschutz*: the 50 %-rule for contracts concluded from 1 April 2009
- Publisher: Haufe (Haufe Finance Office Premium) and IWW (*Wirtschaftsberatung aktuell*) — secondary commentary
- URLs: https://www.haufe.de/id/beitrag/kapitallebensversicherungen-einkommensteuer-3121-einzelheiten-der-50-regel-HI8459275.html · https://www.iww.de/wvm/archiv/kapitallebensversicherungen-neuer-mindesttodesfallschutz-fuer-ab-dem-1-april-2009-abgeschlossene-vertraege-f14610
- Retrieved: **NO** — egress blocked. The second reported condition — the death benefit exceeding the *Deckungskapital* or *Zeitwert* by at least 10 % — arrives with a trailing qualifier that does not parse as a rule, so **its base, its time profile and the qualifier are [unverified]**
- Used for: the **50 %-Regel** — for contracts concluded from 1 April 2009 the *Todesfallleistung* must be at least 50 % of all premiums payable over the whole term — which is the constraint on `death_ratio` and is checked when the model point table is built rather than being a model formula; and the consequence of failing the test, full taxation with no halving

(delib-kapitallebensversicherung-r13)=

### R13 — The pre-2005 regime and the 2004/2005 boundary
- Publisher: Haufe; Bund der Steuerzahler; VLH; smartsteuer — secondary commentary
- URLs: https://www.haufe.de/steuern/steuerwissen-tipps/nach-dem-31122004-abgeschlossene-lebensversicherungen_170_448252.html · https://steuerzahler.de/bayern/newsticker-archiv/newsticker/news/kapitallebensversicherungen-versteuerungsregeln-sehr-differenziert/
- Retrieved: **NO** — egress blocked. **The conditions of the old regime were not established by any search result** and are [unverified]; they are asserted nowhere in delib
- Used for: the 1 January 2005 *Alterseinkünftegesetz* boundary and the taxation of the *Unterschiedsbetrag* on post-2004 contracts, which is what makes the specification's book **three tax cohorts** — pre-2005, 2005–2011 and 2012 onwards — and what fixes delib's composite as a post-2011 contract

(delib-kapitallebensversicherung-r14)=

### R14 — DAV, "Herleitung der Sterbetafel DAV 2008 T für Lebensversicherungen mit Todesfallcharakter"
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; *Fachgrundsatz* / *DAV-Richtlinie*, with a 2008 derivation paper and a 2022 restatement
- URLs: https://aktuar.de/content/PDF/Fachwissen/20080708_DAV_2008_T.pdf · https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf
- Retrieved: **NO** — egress blocked. **The table values are not public and are not redistributed here.** Whether a distinct first-order table exists for endowment as against pure term business **was not established**
- Used for: the name and provenance of the first-order basis the shipped `mort_table.csv` **stands in for** — derived over 2006–2008 from German insurers' own policy data with German population statistics, the cleansed insured data covering **60 % of the German market in the *Kapitallebensversicherung* segment**; the *Richtlinie* also fixing the method for the *Sicherheitszuschläge*, which is what `mort_be_factor = 0.75` represents; and DAV 2008 T R / NR being **unsuitable for business written without a *Gesundheitsprüfung***, so the whole basis presupposes the underwriting the specification describes

(delib-kapitallebensversicherung-r15)=

### R15 — DAV recommendations on the *Höchstrechnungszins* for 2025 and 2026
- Publisher: Deutsche Aktuarvereinigung e. V.; two newsroom items
- URLs: https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-empfiehlt-auch-fuer-2026-einen-hoechstrechnungszins-in-hoehe-von-1-prozent/ · https://aktuar.de/de/newsroom/detail/deutsche-aktuarvereinigung-begruesst-ministeriumsvorstoss-zum-hoechstrechnungszins-2025/
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the DAV recommending **1,0 % for 2026 as well**, which is the basis for holding `deckrv_table.csv` flat at 1,00 % for issue years after 2026 **[std]**; and the specification's point that the maximum technical rate is **set by regulation but proposed by the actuarial profession**, the recommendation having been adopted in both cycles evidenced here

(delib-kapitallebensversicherung-r16)=

### R16 — GDV, "Höchstrechnungszins-Erhöhung ist eine 'angemessene Reaktion auf gestiegene Zinsen'"
- Publisher: GDV; *Medieninformation*
- URL: https://www.gdv.de/gdv/medien/medieninformationen/hoechstrechnungszins-erhoehung-ist-eine-angemessene-reaktion-auf-gestiegene-zinsen--176848
- Retrieved: **NO** — egress blocked; established from a search-result summary. **Adds no independent figure**
- Used for: the industry association's public support for the increase to 1,0 %, cited in the specification's regulatory context to corroborate [R7] and [R15] and to show that the 2025 change was uncontested across the profession, the ministry and the industry

(delib-kapitallebensversicherung-r17)=

### R17 — BaFin, Merkblatt 01/2023 (VA), *zu wohlverhaltensaufsichtlichen Aspekten bei kapitalbildenden Lebensversicherungsprodukten*
- Publisher / doc type: BaFin; supervisory *Merkblatt*, published May 2023 — **the most important supervisory document for this product**
- URLs: https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Merkblatt/VA/mb_01_2023_wohlverhaltensaufsichtliche_aspekte_va.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Pressemitteilung/2023/pm_2023_05_08_Merkblatt_kapitalbildende_LV.html
- Retrieved: **NO** — egress blocked. **No numerical threshold was established** — not for *Effektivkosten*, not for commission, not for the real return. Any figure attributed to the *Merkblatt* would be an invention
- Used for: the requirement of an appropriate ***Kundennutzen***; the finding that *Effektivkosten* **differ considerably** between providers and products, with BaFin closely examining undertakings whose costs or *Aufwendungen für Versicherungsvermittler* are notably high; and the *Renditeziel* duty. This is why the specification treats charge levels as a **supervised rather than a free** parameter, while shipping every one of them as [std]

(delib-kapitallebensversicherung-r18)=

### R18 — BaFin, *Risiken im Fokus 2026* — "Kosten von kapitalbildenden Lebensversicherungen"
- Publisher / doc type: BaFin; annual supervisory risk-focus publication, 2026 edition, consumer-protection chapter
- URL: https://www.bafin.de/DE/die-bafin/publikationen-daten/risiken-im-fokus/Fokusrisiken_2026/RIF_Verbraucher_3/RIF_verbraucher_lebensversicherung_node.html
- Retrieved: **NO** — egress blocked. **No text of the chapter was established**
- Used for: the fact that the product's charge level is a **named focus risk in BaFin's 2026 risk agenda**, three years after the *Merkblatt*; and, through the associated BaFin consumer page in the same result family, the supervisor's one-sentence definition of the product combining a death cover with a savings process paid with interest at the contract's end, which the specification's overview follows

(delib-kapitallebensversicherung-r19)=

### R19 — BaFin *Fachartikel*: "Wenn Lebensversicherungen zu viel kosten" (2022), "PRIIPs-Verordnung" (2022), "Kundennutzen im Fokus" (2024)
- Publisher: BaFin (BaFinJournal / Fachartikel)
- URLs: https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2203_Effektivkosten_Versicherer.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2022/fa_bj_2207_priips_surfday.html · https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2024/bafin_fachartikel_wohlverhalten.html
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the **content requirements of a *Basisinformationsblatt*** — total risk indicator, maximum loss, four graded performance scenarios (*Stress*, *pessimistisch*, *moderat*, *optimistisch*) as annualised returns at three time points, and total costs with the Reduction in Yield split into one-off and ongoing — which the technical notes cite when explaining why the *Effektivkosten* is a validation target the model does not compute

(delib-kapitallebensversicherung-r20)=

### R20 — GDV, "Die deutsche Lebensversicherung in Zahlen 2024"
- Publisher: GDV; industry statistical annual and the Jahresmedienkonferenz page
- URLs: https://www.gdv.de/resource/blob/180978/b8ae8eb0b1bf4b15e7cc3354bc231af9/die-deutsche-lebensversicherung-in-zahlen-2024-publikation-pdf-data.pdf · https://www.gdv.de/gdv/statistik/jahresmedienkonferenz-zahlen-und-daten/lebensversicherung-2024-165748
- Retrieved: **NO** — egress blocked. **The two measures below are not reconcilable from the search evidence** and both are recorded; neither is endowment-specific or by duration
- Used for: the ***Stornoquote*** — **2,72 % in 2024** against 2,56 % in 2023 on the measure counting contracts terminated early, surrendered **or converted to *beitragsfrei*** as a percentage of the *Bestand*, and **1,2 %** on a second GDV measure by contract count. This is the evidence base for pitfall 10 and for `lapse_table.csv` being **[std]** rather than calibrated: the headline measure counts the paid-up route alongside surrenders, so calibrating a surrender decrement to it double-counts

(delib-kapitallebensversicherung-r21)=

### R21 — GDV statistics, "Neugeschäft und Bestand der Lebensversicherer für die letzten zehn Geschäftsjahre"
- Publisher: GDV; statistical series pages
- URL: https://www.gdv.de/gdv/statistik/statistiken-zur-deutschen-versicherungswirtschaft-uebersicht/lebensversicherung/neugeschaeft-und-bestand-der-lebensversicherer-fuer-die-letzten-zehn-geschaeftsjahre-137804
- Retrieved: **NO** — egress blocked. **No endowment-specific new-business or in-force figure was established**, and in particular no figure quantifying the post-2005 collapse of endowment new business
- Used for: the **shape** of the published series only — gross written premiums for the *Bestand*, and the ***Beitragssumme*** and Annual Premium Equivalent for the *Neugeschäft* — which is why the specification treats the *Beitragssumme* as a headline market measure and why the model publishes `beitragssumme()` as a derived quantity rather than only the annual premium

(delib-kapitallebensversicherung-r22)=

### R22 — BGH on the Debeka *Stornoabzug*: the *Bezifferung* requirement
- Publisher: Bundesgerichtshof; reported by LTO, LTMK and Cash.
- URLs: https://www.lto.de/recht/nachrichten/n/bgh-ivzr18424-debeka-stornogebuehr-transparenz-zurueckverweisung-olg-angemessen · https://www.ltmk.de/kapitalmarktabhaengiger-stornoabzug-in-der-lebensversicherung-bgh-klaert-die-anforderungen-an-die-bezifferung/
- Retrieved: **NO** — egress blocked. The docket reads as **IV ZR 184/24** **inferred from a URL slug**, and the decision date was not established; both are [unverified]
- Used for: the holding that ***beziffert*** does **not** require a concrete euro amount at conclusion — an unambiguous calculation procedure suffices, provided it leaves the insurer no *Ermessensspielraum* — so a **capital-market-dependent** *Stornoabzug* is lawful in principle and the deduction need not be constant; and the remittal of the *Angemessenheit* question, which is why the specification records the Debeka schedule as **unresolved at the access date**

(delib-kapitallebensversicherung-r23)=

### R23 — BGH, judgment of 20 January 2021, IV ZR 318/19 — *Bewertungsreserven* after the LVRG
- Publisher: Bundesgerichtshof; reported by rewis.io, NWB and RWS-Verlag
- URL: https://rewis.io/urteile/urteil/e7b-20-01-2021-iv-zr-31819/
- Retrieved: **NO** — egress blocked. The disposition of the parallel constitutional challenge to § 153 Abs. 3 Satz 3 VVG **was not established**
- Used for: the leading post-LVRG authority confirming that the half share of § 153 Abs. 3 VVG is **cut back by the *Sicherungsbedarf*** on contracts with interest guarantees and that the cut-back is lawful — the case law behind `bwr_rate = 0` and behind the specification's statement that the exit half share has frequently been nil

(delib-kapitallebensversicherung-r24)=

### R24 — The older BGH line on *Rückkaufswert* and *Stornoabzug* clauses (2001–2007)
- Publisher: Bundesgerichtshof; reported by verbraucherrecht.at and rechtsportal.de
- URL: https://www.rechtsportal.de/Rechtsprechung/Rechtsprechung/2007/BGH/Wirksamkeit-der-Klauseln-ueber-den-Stornoabzug-und-die-Hoehe-des-Rueckkaufswerts-in-der-Kapitallebensversicherung
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: the case law that produced the present § 169 — clauses failing to distinguish clearly between the *Rückkaufswert* and the *Stornoabzug* held void, and a deduction left to the insurer's discretion or named only after the *Kündigung* failing the transparency requirement. This is why the model treats `storno_rate` as a **contractual, pre-declared schedule** read from a table rather than as a decision taken at the exit

(delib-kapitallebensversicherung-r25)=

### R25 — Assekurata, 24. Marktstudie "Überschussbeteiligungen und Garantien 2026"
- Publisher: Assekurata Assekuranz Rating-Agentur GmbH; market study, reported by finanzwelt
- URL: https://www.assekurata-rating.de/2026/03/04/assekurata-marktstudie-zu-ueberschussbeteiligungen-und-garantien-2026/
- Retrieved: **NO** — egress blocked. **Critical caveat: both figures are for the *annuity*, not the endowment**, and that the two share a declared rate is plausible but [unverified]
- Used for: the market-average *laufende Verzinsung* for the **klassische private Rentenversicherung** — 2,62 % for 2026 against 2,53 % for 2025, with *Neue Klassik* at 2,65 % — which the specification prints beside Allianz's endowment rate [S11] to show the anchor cell's 2,70 % sits at the top of a narrow band; and the attribution of the caution in the increases to remaining ***stille Lasten***, which is why `decl_rate` is held level rather than trended

(delib-kapitallebensversicherung-r26)=

### R26 — Trade-press reporting on the 2026 declarations and the market position of *Klassik*
- Publisher: VersicherungsJournal, procontra, Versicherungsbote, Biallo, Versicherungsmonitor
- URLs: https://www.versicherungsjournal.de/markt-und-politik/etwa-jeder-dritte-lebensversicherer-erhoeht-die-ueberschussbeteiligung-154961.php · https://www.procontra-online.de/lebensversicherung/artikel/lebensversicherung-2026-klassik-wird-zur-nische · https://www.procontra-online.de/lebensversicherung/artikel/allianz-verzichtet-auf-erhohung-der-uberschussbeteiligung
- Retrieved: **NO** — egress blocked; established from search-result summaries
- Used for: **about one in three life insurers raising the *Überschussbeteiligung* for 2026** while **Allianz did not**, which is what makes holding `decl_rate` level a defensible modelling choice rather than a lazy one; the 2024 *Stornoquote* described as an eight-year high; and the trade characterisation "Klassik wird zur Nische", which with [S11] is the evidence base for the specification modelling **a large in-force book with a thin new-business layer**

(delib-kapitallebensversicherung-r27)=

### R27 — DAV, *Ergebnisbericht* — Standardverfahren PRIIP Kategorie 4 (1 July 2025); Franke und Bornberg on *Basisinformationsblätter*
- Publisher: Deutsche Aktuarvereinigung e. V.; Franke und Bornberg GmbH
- URLs: https://aktuar.de/content/PDF/Fachwissen/2025-07-01_DAV_Ergebnisbericht_LV_Standardverfahren_PRIIP_Kategorie_4.pdf · https://www.franke-bornberg.de/blog/basisinformationsblaetter-bib-zu-anlageprodukten-welche-informationen-liefern-bibs
- Retrieved: **NO** — egress blocked. **No content of the report was established**, and no figure is taken from the Franke und Bornberg pieces
- Used for: the existence of a **profession-agreed standard method** for PRIIP *Kategorie 4* — the category covering profit-participating life business — which is what the specification cites for the point that a German endowment's BIB performance scenarios come from a common method rather than from each insurer's own model, and hence that reproducing one is out of this library's scope

(delib-kapitallebensversicherung-r28)=

### R28 — Actuarial and lexicon reference works on *Deckungskapital*, *Zillmerung* and *Überschussverwendung*
- Publisher: various — DGVFM/DAV teaching series; Universität zu Köln; Universität Heidelberg; Gabler/Versicherungsmagazin lexicon; VersWiki; Wikipedia. **Secondary throughout**, and the search summaries **fused them**, so attribution is to the group
- URLs: https://werde-aktuar.de/content/DGVFM/PDF/Schulmaterialien/DGVFM_Band_4_Lebensversicherung.pdf · https://www.versicherungsmagazin.de/lexikon/gezillmerte-nettopraemie-1945423.html · https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Lebensversicherung%3A_Zillmerung · https://www.deutsche-versicherungsboerse.de/verswiki/index_dvb.php?title=Ratenzahlungszuschlag
- Retrieved: **NO** — egress blocked. **The prospective reserve formula itself was not returned**; it is standard actuarial content used as a [std] construction and cited to no source
- Used for: the ***Deckungskapital*** / ***Deckungsrückstellung*** distinction, which is why this library projects the former and references the latter; the ***gezillmerte Nettoprämie*** and *Zillmerung* reducing the reserve by the present value of unrecovered acquisition costs so that **a negative *Deckungskapital* arises in the early years**, which is `res_zill_pp(1) = -alpha_cost`; the four *Überschussverwendung* systems and — the discriminating fact the model turns on — that the *verzinsliche Ansammlung* gives a **higher payment at maturity** while the *Bonussystem* gives **higher death benefits**; and the ***Ratenzahlungszuschlag*** at 2 % half-yearly, 3 % quarterly and 5 % monthly, with the ***echte*** / ***unechte*** distinction that makes the loading inert on a genuine sub-annual *Versicherungsperiode*

(delib-kapitallebensversicherung-r29)=

### R29 — LVRG legislative and market-impact material
- Publisher: Deutscher Bundestag (GDV *Stellungnahme*); Pfefferminzia; Versicherungsbote; AssCompact
- URLs: https://www.bundestag.de/resource/blob/284406/e26d0309aa9989f59485ae83bf52bca9/08-GDV-data.pdf · https://www.pfefferminzia.de/vertrieb/untersuchung-zeigt-abschlusskosten-sinken-nach-lvrg-um-fast-8-prozent-1469012604/ · https://www.versicherungsbote.de/id/4804227/LVRG-Lebensversicherung-Provision-Modelle/
- Retrieved: **NO** — egress blocked. The author, sample and base year of the "almost 8 %" study **were not established**, and **no *Stornohaftung* period was established**
- Used for: the *Lebensversicherungsreformgesetz* of 1 August 2014 and its *Höchstzillmersatz* cut taking effect 1 January 2015; the reported fall in *Abschlusskosten* of almost 8 % after the LVRG; and **the only named-carrier commission figure in the corpus** — Die Stuttgarter cutting its *Abschlussprovision* to **25 ‰** and compensating brokers with *Bestandsprovision* — which is what `comm_init_rate = 2.5 %` and `comm_renew_rate = 1.5 %` are anchored to and why both are still [std]

(delib-kapitallebensversicherung-r30)=

### R30 — Verbraucherzentrale material on the Debeka *Stornoabzug* collective action
- Publisher: Verbraucherzentrale Bundesverband and its Land bodies (Hamburg, Niedersachsen)
- URLs: https://www.verbraucherzentrale.de/verfahren/debeka/faq · https://www.vzhh.de/themen/versicherungen/lebens-rentenversicherung/urteil-stornoabzug-der-debeka
- Retrieved: **NO** — egress blocked. The framing is adversarial and the figures are the consumer bodies', not Debeka's; they are corroborated across three independent bodies and the legal press [R22], so they are **not** [unverified], but **which tariff generation carries them remains unestablished**
- Used for: the running **collective action over the *Stornoklauseln***, and the corroboration of the quantified deduction structure at [S3] — a standard 5 % plus a capital-market-dependent 5 %, 10 % or 15 % of the *Deckungskapital*, an observed total range of **5 % to 20 %** for one carrier. That range is the only observation the [std] `storno_rate` schedule is set against, and the specification says so in the table itself

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **Every entry there carries the same retrieval
status as everything above: nothing was retrieved, and the prudential and contract-law entries were
established from search-result summaries while the search budget lasted.** Entries cited by the
kapitalbildende Lebensversicherung documents:

- **REG-R1** — Richtlinie 2009/138/EG (Solvabilität II): the framework the projected cash flows feed and which this library does not implement.
- **REG-R2** — Delegierte Verordnung (EU) 2015/35: the same, at the level of the standard formula and contract boundaries.
- **REG-R3** — Richtlinie (EU) 2025/2, the Solvency II review: named in the specification's regulatory context as pending.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the discount curves a valuation layer would apply to `liability_cf`.
- **REG-R5** — VAG 2016, its architecture and Anlage 1: the *Sparte* this product is written in.
- **REG-R6** — VAG §§ 74–110 and § 40: best estimate, risk margin, SCR/MCR and the SFCR — cited as the layer above this one.
- **REG-R8** — VAG § 138, *Prämienkalkulation* and *Gleichbehandlung*: the statutory frame for the first-order pricing basis.
- **REG-R9** — VAG § 139 and the *Sicherungsbedarf* test on *Bewertungsreserven*: the cross-product statement of the rule at [R8], and the argument for `bwr_rate = 0`.
- **REG-R10** — VAG §§ 140 and 145, the RfB and the *Verordnungsermächtigung*: the provision the declared surplus is paid out of, and which the model does not carry.
- **REG-R11** — VAG §§ 141–143, the *Verantwortlicher Aktuar* and the 1994 deregulation: why a German tariff is no longer approved in advance.
- **REG-R12** — VAG §§ 221–236 and § 314, Protektor and the supervisor's crisis powers: the § 314 write-down the specification names as out of scope.
- **REG-R14** — DeckRV and its § 2: the *Höchstrechnungszins* as a reserving-regulation quantity, keyed by cohort.
- **REG-R15** — the *Höchstrechnungszins* rate history and the Sechste Verordnung of 19 July 2024: the source of `deckrv_table.csv`'s first column, and of its two split-year [std] entries.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the source of the second column, and of `check_zillmer_cap()`.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins*, the *Zinszusatzreserve* and the *Korridormethode*: named and expressly not modelled.
- **REG-R18** — MindZV, the minimum allocation to the RfB: the cross-product statement of [R6].
- **REG-R19** — RfBV, the collective part of the RfB: cited for the *Schlussüberschussanteilfonds* the model does not carry.
- **REG-R20** — LVRG 2014: the statute behind the 25 ‰ cut and the *Effektivkosten* disclosure.
- **REG-R21** — BaFin, the FinDAG, the MaGo and the *Auslegungsentscheidungen*: the supervisory frame around [R17] and [R18].
- **REG-R22** — VVG 2008, Kapitel 5 and § 171 (*halbzwingende Vorschriften*): why §§ 153, 161, 165 and 169 cannot be contracted around to the policyholder's detriment.
- **REG-R24** — VVG § 153 and the *hälftige Beteiligung*: the cross-product statement of [R1].
- **REG-R25** — VVG §§ 154 and 155, *Modellrechnung* and *Standmitteilung*: the statutory duty behind [S2].
- **REG-R26** — VVG §§ 150, 159–162: *Einwilligung*, *Bezugsberechtigung* and the *Selbsttötung* rule at [R4].
- **REG-R27** — VVG § 163, *Prämien- und Leistungsänderung*: cited in pitfall 16 for what a *Beitragsverrechnung* offset is **not** — a discretionary rebate rather than a price change.
- **REG-R28** — VVG §§ 165–170: the cross-product statement of [R2] and [R3], and of the *Stornoabzug* conditions.
- **REG-R30** — VVG §§ 19, 37, 38, 157 and 158: the *Anzeigepflicht* at [R5]; §§ 37 and 38 are named as **not researched** and nothing is asserted about them.
- **REG-R31** — VVG §§ 6, 7, 1a, 7b, 7c and 214 with the VVG-InfoV: advice, information and the *Effektivkosten* at [R9].
- **REG-R32** — PRIIPs, Verordnung (EU) Nr. 1286/2014 and its technical standards: the BIB regime at [R19] and [R27].
- **REG-R33** — IDD, Richtlinie (EU) 2016/97 and § 34d GewO: the distribution frame behind the IPID at [S6].
- **REG-R34** — Unisex: EuGH C-236/09 (Test-Achats) and §§ 19, 20 and 33 AGG. **The hard constraint behind `mort_rate_at_age`** — new business unisex from 21 December 2012, so `sex` may not enter the premium (pitfall 17).
- **REG-R35** — BaFin Merkblatt 01/2023 and *angemessener Kundennutzen*: the cross-product statement of [R17].
- **REG-R36** — the BGH line of authority on German life contracts: the cross-product frame for [R22], [R23] and [R24].
- **REG-R38** — AltEinkG and the *Drei-Schichten-Modell*: where a *kapitalbildende Lebensversicherung* sits (Schicht 3), and the 2005 boundary at [R13].
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag*, the 12/62 rule and the *Mindesttodesfallschutz* — the cross-product statement of [R10] and [R12], and the reason the anchor cell matures at attained age 62.
- **REG-R46** — ErbStG and SGB V §§ 226, 229 and 240: the treatment of a death benefit, named and not modelled.
- **REG-R47** — *Rechnungsgrundlagen erster und zweiter Ordnung*, and the DAV as owner of the tables. The frame for the model's two mortality bases, for the *Sicherheitszuschlag* whose release **is** the *Risikoüberschuss*, and for the fact that the direction of prudence forks between the death and the survival leg (pitfalls 13 and 14).
- **REG-R48** — DAV 2008 T and its predecessors: the cross-product statement of [R14], including the selection factors the shipped proxy does **not** carry.
- **REG-R52** — Destatis *Sterbetafeln* and the reuse licence: the population benchmark an insured-lives replacement table must sit below.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Franke und Bornberg): the source of the statement that the *laufende Verzinsung* **is** the guarantee plus the interest surplus, which is pitfall 1 and the single most load-bearing line in the model.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: § 341f forming the *Deckungsrückstellung* **excluding verzinslich angesammelte Überschussanteile**, which is why `av_pp` is a cells of its own and not part of `res_pp`; and § 28 RechVersV naming the declared rate as a published quantity.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: named as the other measurement basis these cash flows feed.
- **REG-R56** — DAV *Fachgrundsätze* and the annual *Höchstrechnungszins* recommendation: the professional standard this documentation sits under, and the frame for [R15].

---

## Provenance note

Extraction details — which fact was read from which search summary, section-level notes organised
by mechanic, and the **twenty-four-item gaps and caveats register** — live in
`_research/kapitallebensversicherung.md`. That file is the citation ground truth for the S# and R#
numbering used here.

The caveats that most affect what these product documents can claim, and which are repeated in the
specification and the technical notes rather than left here: **no document was retrieved**, so every
citation above is a pointer rather than a certificate; **no statutory version date was established**
for any of §§ 19, 153, 161, 165 or 169 VVG, for the MindZV beyond its 2016 consolidation, for the
DeckRV beyond the 2025 amendment, or for § 139 VAG, so every statutory statement is current *in
substance as reported in August 2026* and none is version-pinned (gap 15); **no *Schlussüberschuss*
rate of any kind was established**, for any insurer, in any year, so `term_rate` is wholly [std]
(gap 1); **the only declared-rate market averages are for the annuity**, not the endowment, and that
the two share a rate is [unverified] (gap 2); **no charge level of any kind was established** — not
one *Effektivkosten* value, *Abschlusskostenquote* or *Verwaltungskostenquote*, and only one
commission figure, at another carrier — so every charge in the model is [std] (gap 7); **no German
*Produktinformationsblatt* or IPID for this product was located**, which is the single most valuable
missing document class, since one page of it would have supplied entry age, sum-insured band, term
band, charge levels and the *Effektivkosten* (gap 9); **the two GDV *Stornoquote* measures are
irreconcilable** and neither is a surrender rate (gap 10); **no premium rate table, underwriting grid
or *Risikozuschlag* scale is public for any German endowment**, so every premium here is computed by
the model's own equivalence principle and none reproduces a published figure (gap 16); **the DAV
tables are cited and never shipped**, so every decrement in the model is a [std] proxy (gap 14);
**the only *Stornoabzug* schedule in the corpus belongs to one carrier and is sub judice** (gap 18);
**four statutory provisions the product depends on were never searched** — §§ 168, 152, 37/38 and 150
VVG — and nothing is asserted about any of them (gap 20); and **nineteen of the twenty-six named
carriers produced no document at all**, so the variations table is six carriers wide and only one of
the six is quantified (gap 22). One Austrian wording was returned by a search and is **excluded**:
the VVG, the DeckRV and the MindZV do not apply to it, and nothing anywhere in delib is cited to it
(gap 24).
