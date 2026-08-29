# Pflegerentenversicherung (private LTC annuity) — research notes (Germany)

Research notes for the German individual *Pflegerentenversicherung* — the private long-term-care
top-up written **as a life-insurance contract**, which pays a monthly *Pflegerente* for as long as
the *versicherte Person* holds a contractual *Pflegegrad*, graded by *Pflegegrad*, with
*Beitragsbefreiung im Leistungsfall* (waiver of premium in claim), a level *Beitrag* calculated
*nach Art der Lebensversicherung* against a *Deckungskapital* that performs the economic function of
an *Alterungsrückstellung*, and frequently a *Todesfallleistung* or *Beitragsrückgewähr*.

**In scope.** The individual, privately-written, single-life *Pflegerentenversicherung* sold by a
*Lebensversicherer*: a stand-alone contract (not a rider on an endowment or an annuity), with a
*vereinbarte Pflegerente* graded across the five *Pflegegrade* of SGB XI, a level lifelong or
term-limited *Beitrag* that the insurer may not re-rate, a prospective *Deckungsrückstellung*, a
*Rückkaufswert* under § 169 VVG and a *Beitragsfreistellung* right under § 165 VVG, an
*Überschussbeteiligung* under § 153 VVG, and a benefit trigger defined by reference to the
*Pflegegrad* determined under §§ 14, 15 SGB XI.

**Out of scope, and said so where it matters.**

- The **soziale Pflegeversicherung** of SGB XI itself, and the **private Pflegepflichtversicherung**
  (PPV) of § 23 SGB XI, are the compulsory first layer. They are not modelled. They are researched
  here in detail because the private product is sized against the gap they leave, and because the
  private product's benefit trigger is defined by reference to them.
- **Pflegetagegeldversicherung** and **Pflegekostenversicherung** are the other two private forms.
  They are written as *private Krankenversicherung*, not as *Lebensversicherung*, and their premium
  can be re-rated under § 203 VVG. They are researched here as contrast documents — the difference
  between them and the *Pflegerente* is the single most important structural fact about this product
  — but neither is the delib model.
- **Pflege-Bahr**, the state-subsidised cover of § 127 SGB XI, is confined by statute to the
  *Pflegetagegeld* form. It is researched here in full because the brief requires it and because it
  fixes a statutory minimum benefit grid that the private market reuses, but **a Pflegerente cannot
  be a geförderter Tarif** and the delib model does not implement the *Zulage*.
- *Berufsunfähigkeitsversicherung* (delib product 9) is the neighbouring biometric-risk product; it
  shares the *nach Art der Lebensversicherung* chassis, the *Beitragsbefreiung im Leistungsfall*, the
  *Nachprüfung* and the multi-state modelling problem, and differs in trigger, in duration and in
  the age at which the risk bites. It is referenced where the two diverge.
- *Betriebliche Altersversorgung* in all five *Durchführungswege*, *Gruppenversicherung*, the
  *private Krankenversicherung* proper, *Sterbegeldversicherung* and institutional risk transfer are
  outside the delib library entirely.
- *Pflegerente gegen Einmalbeitrag* — the single-premium form sold to people already close to, or
  already in, care — is recorded as a market variant and is **not** the base model.
- Austrian and Swiss LTC products are excluded: SGB XI, the VVG, the VAG and the DeckRV do not
  apply to them, and neither does the *Pflegegrad* concept.

These notes are the **citation ground truth** for the delib `pflegerentenversicherung` product
documents. Source ids **S1..S16** and **R1..R24** below are **frozen — never renumber**; unused ids
are simply omitted downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this section before reading any tagged fact in this file. It is the difference between a delib
citation and an frlib one.

**No document in this file was retrieved.** Direct HTTP egress from this build environment is
blocked by an organisation network policy. `WebFetch` and `curl` are refused with HTTP 403 at the
egress gateway for every host outside a short package-registry allowlist. The hosts that matter for
this product were all tried and all refused:

| Host | What it would have supplied | Result |
|---|---|---|
| `gesetze-im-internet.de` | SGB XI, VVG, VAG, EStG, SGB XII, DeckRV, KVAV | HTTP 403 |
| `bafin.de` | supervisory *Merkblätter*, *Fachartikel*, statistics | HTTP 403 |
| `gdv.de` | *Musterbedingungen*, life-market statistics | HTTP 403 |
| `aktuar.de` | DAV *Ergebnisberichte*, the DAV 2008 P derivation paper | HTTP 403 |
| `pkv.de` | PKV-Verband *Zahlenbericht*, Pflege-Bahr take-up, MB/EPV | HTTP 403 |
| `destatis.de` | *Pflegestatistik*, *Pflegevorausberechnung* | HTTP 403 |
| `bundesgesundheitsministerium.de` | SPV benefit amounts, *Beitragssatz* | HTTP 403 |
| `vdek.com` | *Eigenanteil* series for *Pflegeheime* | HTTP 403 |
| `de.wikipedia.org` | orientation only | HTTP 403 |

Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not
one statutory text, not one DAV paper and not one statistical release was opened.

**The session `WebSearch` budget was already exhausted when this product was started.** The session
shares a hard cap of 200 `WebSearch` calls across all delib work, and the cap had been reached
before the first query for this product could be issued. **This file therefore has no research
channel at all** — neither retrieval nor search. It is written from the author's own knowledge of
German insurance law and German actuarial practice, under the discipline that house rule 3 imposes
for exactly this case.

What that discipline means here, concretely:

1. **Every source entry is a *known reference*, never a read document.** Each records
   `Retrieved: no — direct HTTP egress blocked in the build environment; no search corroboration
   (session search budget exhausted)`. The entry names a publisher and a document type that exist
   and are the right kind of document for this product. It does not assert that any particular
   edition, document number, page count or publication date is correct, because none was checked.
2. **No URL is invented.** Where a canonical form is well known — `.../sgb_11/__15.html` for § 15
   SGB XI — it is given and marked `[unverified]`. Everywhere else the entry says
   `URL: not established`.
3. **No verbatim quotation of any instrument appears anywhere in this file.** Where a statutory rule
   is described, it is described in English, in the author's own words, as *what the instrument
   provides*. There is not a single German sentence in quotation marks attributed to a statute or to
   a *Bedingungswerk*, because there is no summary and no PDF behind one.
4. **`[unverified]` is used generously and means what it always means.** Every specific paragraph
   number, effective date, monetary amount, percentage, threshold and market figure below carries
   it, because no search result confirmed any of them. The general *shape* of a well-established
   mechanic — that a *Pflegerente* is graded by *Pflegegrad*, that premiums are waived in claim,
   that the *soziale Pflegeversicherung* is a *Teilleistungssystem* — is not tagged `[unverified]`,
   because tagging it would drown the signal. The moment a claim becomes **specific and numeric**,
   it is tagged.
5. **Uncertain levels are `[std]` parameters, not citations.** Where the mechanic is certain and the
   level is not — a *Leistungsstaffel* percentage, a *Karenzzeit*, a charge, a lapse rate, a premium
   at age 45 — this file ships a `[std]` value with a stated rationale and an argued plausible
   range, and it shows the arithmetic behind it (section 23). That is honest. A guessed `[S4]`
   figure would not be.
6. **The weight of the file is in the mechanics.** Sections 1 to 24 below are where a research file
   written under these conditions earns its place: they do not depend on having a PDF open, and they
   are what the product specification and the technical notes will be written from. The source list
   is deliberately thinner in its claims than an frlib source list, and the gaps register at the
   foot is deliberately longer.

**A delib citation is a pointer, not a certificate.** `[R2]` beside a statement about § 15 SGB XI
means *this is the instrument the statement should be checked against*. It does not mean anyone
checked it.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Pflegebedürftigkeit* | The insured event: a state of dependency on help with the ordinary business of living, defined in § 14 SGB XI by loss of *Selbstständigkeit* rather than by hours of care |
| *Pflegegrad* (1–5) | The five statutory degrees of *Pflegebedürftigkeit* in force since 1 January 2017; the benefit trigger and benefit scale of every private product |
| *Pflegestufe* (I–III, Härtefall) | The three pre-2017 degrees, replaced by the *Pflegegrade*; still cited in older wordings and older statistics |
| *Soziale Pflegeversicherung* (SPV) | The statutory LTC insurance of SGB XI, the fifth pillar of German social insurance |
| *Private Pflegepflichtversicherung* (PPV) | The compulsory private equivalent for people insured in the *private Krankenversicherung*, § 23 SGB XI |
| *Teilleistungssystem*, *Teilkaskoversicherung* | The design principle of the SPV: it deliberately meets only part of the cost of care |
| *Neues Begutachtungsassessment* (NBA) | The assessment instrument introduced with the five *Pflegegrade*; scores six *Module* and converts them into *gewichtete Punkte* |
| *Medizinischer Dienst* (MD, formerly MDK) / MEDICPROOF | The assessor for the SPV / the assessor for the PPV |
| *Pflegegeld* / *Pflegesachleistung* | The cash benefit for care given informally at home / the benefit in kind for a professional *Pflegedienst* |
| *Vollstationäre Pflege* | Care in a *Pflegeheim*; the setting in which the funding gap is largest |
| *Eigenanteil*, *einrichtungseinheitlicher Eigenanteil* (EEE) | The resident's own share of the cost of a *Pflegeheim* / the care-related part of it, equal for *Pflegegrade* 2 to 5 within one facility since 2017 |
| *Leistungszuschlag* | The duration-dependent statutory subsidy that reduces the *EEE* the longer the resident has been in the facility, § 43c SGB XI |
| *Versorgungslücke* | The funding gap the private product is sold to close |
| *Pflegezusatzversicherung* | Private LTC top-up cover generally, in any of its three forms |
| *Pflegetagegeldversicherung* / *Pflegekostenversicherung* / *Pflegerentenversicherung* | Daily-cash form (a *Summenversicherung*) / indemnity form / annuity form written as life assurance |
| *Pflege-Bahr* | The state-subsidised *Pflegetagegeld* of § 127 SGB XI, from the 2013 reform, carrying a monthly *Zulage* |
| *Pflegevorsorgezulage* | The 5 € monthly subsidy paid into a *Pflege-Bahr* contract |
| *Vereinbarte Pflegerente* | The contractual monthly annuity at the top *Pflegegrad*, the scaling constant of the whole benefit schedule |
| *Leistungsstaffel* | The schedule of benefit percentages by *Pflegegrad* |
| *Beitragsbefreiung im Leistungsfall* | Waiver of premium while the benefit is payable |
| *Wartezeit* / *Karenzzeit* | Qualifying period from inception before cover attaches / deferred period from the onset of *Pflegebedürftigkeit* before the annuity starts |
| *Nachprüfung* / *Herabstufung* | The insurer's periodic re-verification that the trigger still holds / a reduction of the *Pflegegrad*, which reduces or ends the annuity |
| *Dynamik* | Contractual indexation: *Beitragsdynamik* raises premium and cover before claim, *Leistungsdynamik* raises the annuity in payment |
| *Todesfallleistung* / *Beitragsrückgewähr* | Death benefit / return of premiums paid, the common form of it here |
| *Nach Art der Lebensversicherung* | Calculated on life-assurance principles: level premium, prospective reserve, ageing provision, no ordinary re-rating |
| *Alterungsrückstellung* | The ageing provision of *private Krankenversicherung*; the economic function the *Pflegerente*'s *Deckungskapital* performs |
| *Deckungskapital* / *Deckungsrückstellung* | The actuarial reserve of one contract / the balance-sheet provision covering it |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business, set in the DeckRV |
| *Rückkaufswert* / *Stornoabzug* | Surrender value / the deduction the insurer may make from it |
| *Beitragsfreistellung* | Conversion to a paid-up contract on the policyholder's demand, § 165 VVG |
| *Überschussbeteiligung* | Participation in the insurer's surplus, § 153 VVG |
| *Gesundheitsprüfung* / *Risikozuschlag* / *Leistungsausschluss* | Medical underwriting / extra-risk loading / an exclusion written into the individual contract |
| *Vorvertragliche Anzeigepflicht* | The applicant's pre-contractual duty of disclosure, § 19 VVG |
| *Reaktivierung* | Recovery from *Pflegebedürftigkeit* back to the active state; in this product a decrement out of the paying state |
| *Hilfe zur Pflege* | The means-tested social-assistance backstop of SGB XII, the alternative to private provision |
| *Elternunterhalt* | Adult children's maintenance liability for a parent's care costs, curtailed from 2020 |

---

## Primary sources

Every entry below carries the same retrieval status, stated once here rather than repeated sixteen
times: **Retrieved: no — direct HTTP egress blocked in the build environment; no search corroboration
(session search budget exhausted).** Each entry names a document that exists and is the right kind
of document for this product. Nothing in an entry asserts that a particular edition, document
number, page count or date is correct.

### S1 — PKV-Verband, *Musterbedingungen für die private Pflegepflichtversicherung* (MB/PPV)
- Publisher: Verband der Privaten Krankenversicherung e. V. (PKV-Verband), Köln
- Doc type: *Musterbedingungen* — model conditions for the compulsory private LTC cover of § 23
  SGB XI, adopted with variations by every private health insurer
- URL: not established
- Content and why it is here: the MB/PPV is the document in which the private sector's rendering of
  *Pflegebedürftigkeit* and of the five *Pflegegrade* is written down, mirroring §§ 14, 15 SGB XI
  [R2] and the benefit catalogue of §§ 36 ff. SGB XI [R3][R4]. It matters to a *Pflegerente* for one
  structural reason: **private top-up wordings normally define their own trigger by reference to the
  *Pflegegrad* established under SGB XI or the MB/PPV, rather than by writing an independent
  medical definition.** That reference is what makes the product cheap to administer and what ties
  its incidence experience to the statutory assessment regime, including every future change to it.
  An edition designation of the form "MB/PPV 2017" — the recension carrying the five *Pflegegrade*
  — is `[unverified]`; the current edition was not established.

### S2 — PKV-Verband, *Musterbedingungen für die ergänzende Pflegekrankenversicherung* (MB/EPV)
- Publisher: PKV-Verband
- Doc type: *Musterbedingungen* for the **top-up** LTC cover written as *private Krankenversicherung*
  — the *Pflegetagegeld* and *Pflegekosten* forms
- URL: not established
- Content and why it is here: this is the contrast document for the whole file. A *Pflegetagegeld*
  written on MB/EPV lines is a **health-insurance** contract: it is supervised under the health
  rules, it may carry a *Beitragsanpassung* clause under § 203 VVG, and where it is written *nach
  Art der Lebensversicherung* its ageing provision is an *Alterungsrückstellung* under § 146 VAG and
  the KVAV [R14]. A *Pflegerente* on the same risk is a **life** contract with a *Deckungsrückstellung*
  under the DeckRV [R13] and no ordinary re-rating power. Everything a customer is told about the
  two products' relative merits reduces to that difference. Edition designations are `[unverified]`.

### S3 — GDV, *Musterbedingungen* for life-assurance products
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV)
- Doc type: *Musterbedingungen* — model AVB published by the industry association for members to
  adopt, adapt or ignore, expressly *unverbindlich*
- URL: not established (the GDV maintains a public *Musterbedingungen* index; the index URL was not
  established)
- Content: the GDV publishes model AVB for the main life-assurance product families in the
  question-headed style adopted for post-2008 VVG wordings ("Welche Leistungen erbringen wir?").
  **Whether the GDV publishes a *Musterbedingung* specifically for the *Pflegerentenversicherung*
  was not established, and this file does not assume it does.** No benefit, premium, surrender or
  paid-up rule anywhere below is attributed to S3. The entry is retained because the model-conditions
  library is the first document a reader with a working network should look for, and because a GDV
  *Musterbedingung*, if one exists, would be the natural spine of a composite specification. Its
  competition-law disclaimer must be respected in any case: an S3-tagged fact would be a *market
  template*, weaker evidence about any carrier than that carrier's own AVB.

### S4 — *Allgemeine Bedingungen für die Pflegerentenversicherung* (AVB), as a document class
- Publisher: an individual German *Lebensversicherer* (no carrier's wording was located)
- Doc type: *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for a *Pflegerenten* tariff,
  typically bundled with *Tarifbedingungen* and delivered with the *Versicherungsschein*
- URL: not established
- Content — what a wording of this class contains, stated as a document-class description and not as
  a reading of any instance. The clause inventory is stable across the German life market and is the
  skeleton the delib product specification follows:
  - **Benefit clause.** What the insurer pays, on what trigger, from when, for how long: the
    *vereinbarte Pflegerente*, the *Leistungsstaffel* by *Pflegegrad*, whether *Pflegegrad* 1 is
    insured, whether the annuity differs between care at home and *vollstationäre* care, and whether
    it is payable for life.
  - **Trigger clause.** How *Pflegebedürftigkeit* is established: normally by the *Pflegegrad*
    determined by the SPV or the PPV, with a fallback assessment by a doctor the insurer appoints
    where the insured is not covered by either.
  - **Waiting and deferred periods.** *Wartezeit* from inception; *Karenzzeit* from the onset of
    *Pflegebedürftigkeit*; whether either is waived for *Pflegebedürftigkeit* caused by an accident.
  - **Waiver clause.** *Beitragsbefreiung im Leistungsfall*: from which *Pflegegrad*, from which
    month, and whether it is full or partial.
  - **Re-verification clause.** *Nachprüfung*: the insurer's right to require evidence that the
    *Pflegegrad* persists, and the consequences of a *Herabstufung* — reduction of the annuity to
    the lower step, or cessation.
  - **Death-benefit clause**, where one is written: *Beitragsrückgewähr*, a fixed sum, or the
    *Deckungskapital*.
  - **Indexation clause.** *Beitragsdynamik* before claim; *Leistungsdynamik* in payment; the
    policyholder's right to decline and whether declining is final.
  - **Surplus clause.** How the *Überschussbeteiligung* is declared and applied [R11].
  - **Surrender and paid-up clauses** under §§ 169 and 165 VVG, with the *Stornoabzug*.
  - **Disclosure and exclusion clauses**: § 19 VVG *vorvertragliche Anzeigepflicht*; exclusions for
    *Pflegebedürftigkeit* caused by war, by the insured's own intentional act, and — variably — by
    addiction, by aviation other than as a passenger, and by an existing condition disclosed and
    excluded at underwriting.
  - **Territorial clause**: whether the annuity remains payable if the insured is cared for outside
    Germany or the EU/EEA.
  No page count, no edition date and no clause number for any carrier's wording is asserted; every
  such specific is `[unverified]` and is recorded as gap 14.

### S5 — *Produktinformationsblatt* (PIB) / *Informationsblatt zu Versicherungsprodukten* (IPID)
- Publisher: an individual German *Lebensversicherer*
- Doc type: the short pre-contractual product summary. The German market uses both the national
  *Produktinformationsblatt* required by § 4 VVG-InfoV for certain life products and the EU IDD
  *Insurance Product Information Document* [R11][unverified as to which applies to this product]
- URL: not established
- Content: the document class that would have supplied, on one or two pages, exactly the parameters
  this file has to standardise — entry-age band, *vereinbarte Rente* band, the *Leistungsstaffel*,
  the *Wartezeit*, the *Karenzzeit*, the premium for a named specimen, and the charges. **Not one
  instance was located**, and this is the single most valuable missing document class in the file
  (gap 1).

### S6 — *Basisinformationsblatt* (PRIIP-KID)
- Publisher: an individual German *Lebensversicherer*
- Doc type: the three-page key information document required by Regulation (EU) No 1286/2014 [R25]
- URL: not established
- Content, and a genuine structural question the delib documents must answer rather than assume:
  **whether a *Pflegerentenversicherung* is a PRIIP at all depends on its own design.** The
  Regulation excludes life-insurance contracts whose benefits are payable only on death or in
  respect of incapacity due to injury, sickness or infirmity [R25][unverified as to the article]. A
  **pure-risk *Pflegerente* with no surrender value and no death benefit falls squarely inside that
  exclusion and needs no *Basisinformationsblatt***. A *Pflegerente* **with** *Beitragsrückgewähr*,
  or with a material *Rückkaufswert*, pays on events other than incapacity and death-in-claim and is
  much more likely to be an insurance-based investment product requiring one. The consequence for
  delib: the presence or absence of a *Basisinformationsblatt* in a carrier's document library is
  evidence about the tariff's design, and the delib base run — pure risk, no *Beitragsrückgewähr* —
  is the variant for which no KID would be expected. All of this is `[unverified]` and is recorded
  as gap 16.

### S7 — *Verbraucherinformationen* / *Vertragsinformationen* under the VVG-InfoV
- Publisher: an individual German *Lebensversicherer*
- Doc type: the pre-contractual information package required by § 7 VVG and the VVG-InfoV [R11]
- URL: not established
- Content: the package in which, for a life product, the *Abschluss- und Vertriebskosten* and the
  *Verwaltungskosten* must be disclosed in euro amounts, and in which the *Effektivkosten* (reduction
  in yield) appears for products with a savings element. For a biometric-risk product the euro
  disclosure of acquisition and administration costs is the operative one. **No instance was
  located**; every charge level in delib is therefore `[std]` (gap 2).

### S8 — *Jährliche Mitteilung zum Stand Ihrer Versicherung* (Standmitteilung)
- Publisher: an individual German *Lebensversicherer*; a GDV model exists for other life products
- Doc type: the annual statement owed to the policyholder under § 155 VVG [R11][unverified]
- URL: not established
- Content: the document in which the guaranteed benefit, the accumulated *Überschussbeteiligung*,
  the current *Rückkaufswert* and the current *beitragsfreie* benefit are reported side by side —
  i.e. it names the state variables a projection model has to carry. For a *Pflegerente* the
  guaranteed benefit reported is the *vereinbarte Pflegerente* at the top *Pflegegrad*, not a sum
  insured. **No instance was located and the field list is `[unverified]`.**

### S9 — *Tarifblatt* / *Beitragstabelle* for a *Pflegerenten* tariff
- Publisher: an individual German *Lebensversicherer*
- Doc type: the rate card — premium per unit of *vereinbarte Rente*, by entry age, sex, smoker
  status where used, *Beitragszahlungsdauer* and option set
- URL: not established
- Content: **no German insurer publishes a *Pflegerenten* rate card**, on the evidence available to
  this file, and none was located. This is the difference between this file and
  `frlib/_research/temporaire-deces.md`, where one insurer's complete attained-age grid was read off
  a retrieved PDF and became the reference implementation's premium basis. delib's
  `pflegerentenversicherung` model has **no published premium to reproduce**; its premium is struck
  by equivalence on `[std]` bases and its level is sanity-checked against the argued band in
  section 23 (gap 3).

### S10 — Stiftung Warentest / *Finanztest*, comparative tests of *Pflegezusatzversicherung*
- Publisher: Stiftung Warentest — **secondary**, not a product document
- Doc type: comparative product test with a scored ranking and a price table
- URL: not established
- Content: Stiftung Warentest has tested German *Pflegezusatzversicherung* repeatedly, and its tests
  are the most-cited public price source for the sector. Two things about the tests matter here and
  are structural rather than numeric: **the tests concentrate on *Pflegetagegeld***, because that is
  the dominant form by contract count, and **the tests are consistently critical of *Pflege-Bahr***
  for the ratio between the benefit it buys and the *Versorgungslücke* it is meant to close. No
  score, no price and no test date is asserted; every such specific is `[unverified]` (gap 4).

### S11 — Verbraucherzentrale, consumer guidance on *Pflegezusatzversicherung*
- Publisher: Verbraucherzentrale Bundesverband and the *Länder* consumer centres — **secondary**
- Doc type: consumer guidance pages
- URL: not established
- Content: the consumer-body view, which is where the three private forms are set against each
  other for a lay reader. The recurring points, stated as the sector's settled consumer-advice
  position rather than as a reading of any page: the *Pflegerente* is the most expensive of the
  three per euro of benefit but the only one with a premium the insurer cannot re-rate; the
  *Pflegetagegeld* is the cheapest to start and carries re-rating risk; the *Pflegekosten* form is
  effectively obsolete; and a *Pflegetagegeld* written **not** *nach Art der Lebensversicherung*
  (i.e. *nach Art der Schadenversicherung*, with no ageing provision) is the form to avoid, because
  its premium rises with attained age. `[unverified]` throughout.

### S12 — Finanztip, guidance on *Pflegezusatzversicherung*
- Publisher: Finanztip — **secondary**
- Doc type: consumer guidance
- URL: not established
- Content: same class of evidence as S11; retained separately because Finanztip publishes explicit
  recommended benefit levels — that a top-up should be sized against the *Eigenanteil* in a
  *Pflegeheim* rather than against a round number — which is the reasoning delib's `[std]`
  *vereinbarte Rente* of 1 000 € per month follows. Any specific recommended amount is
  `[unverified]`.

### S13 — Comparison portals: Verivox, Check24
- Publisher: Verivox GmbH; CHECK24 Vergleichsportal GmbH — **secondary**
- Doc type: quote engines and product-comparison pages
- URL: not established
- Content: the only public sources that produce a premium for a named age, benefit and option set on
  demand, and therefore the natural corroboration for section 23's premium band. **None was queried**
  (no egress, no search), so section 23's band rests on the actuarial arithmetic set out there and
  is `[std]`, not `[S13]`. Portals cover *Pflegetagegeld* far more thoroughly than *Pflegerente*;
  whether either portal quotes *Pflegerente* at all was not established (gap 5).

### S14 — Ratings agencies: Morgen & Morgen, Franke und Bornberg, Assekurata
- Publisher: MORGEN & MORGEN GmbH; Franke und Bornberg GmbH; ASSEKURATA Assekuranz Rating-Agentur
  GmbH — **secondary**
- Doc type: product ratings and market studies
- URL: not established
- Content: the three agencies that rate German biometric and life products and publish the ratings
  the market quotes. Franke und Bornberg and Morgen & Morgen rate *Pflegezusatzversicherung*
  wordings clause by clause and are therefore the best public route to the observed **range** of
  *Leistungsstaffel*, *Wartezeit*, *Karenzzeit* and *Nachprüfung* terms — precisely the ranges this
  file has to standardise. Assekurata publishes the annual *Überschussbeteiligung* market study that
  fixes declared rates. **Nothing from any of them was retrieved**, and the ranges in the variation
  table below are `[std]`/`[unverified]` reconstructions, not rating data (gap 6).

### S15 — *Pflege-Bahr* tariff conditions of a *geförderter Tarif*
- Publisher: an individual German *Krankenversicherer*
- Doc type: the AVB and *Tarifbedingungen* of a state-subsidised *Pflegetagegeld* tariff, which must
  satisfy § 127 SGB XI to attract the *Zulage* [R8]
- URL: not established
- Content: the document class in which the statutory minimum design of § 127 SGB XI appears as
  contract terms — no *Gesundheitsprüfung*, no *Risikozuschlag*, no *Leistungsausschluss*, a
  *Wartezeit*, and a benefit grid whose top step is at least 600 € per month with the lower
  *Pflegegrade* at fixed fractions of it. This is the **only** place in German private LTC where a
  *Leistungsstaffel* is prescribed by statute, which is why it anchors the ranges in section 7 even
  though it belongs to a different product form. Every figure attributed to it is `[R8][unverified]`.

### S16 — PKV-Verband, *Zahlenbericht der privaten Krankenversicherung* and the association's
  *Pflegezusatzversicherung* statistics
- Publisher: PKV-Verband — **secondary for product terms, primary for market counts**
- Doc type: annual statistical report and standing statistics pages
- URL: not established
- Content: the only public counting of German private LTC top-up contracts, split between
  *geförderte* (*Pflege-Bahr*) and *ungeförderte* business. Two structural cautions that matter more
  than any number: (a) the PKV-Verband counts **health-insurance** contracts, so *Pflegetagegeld*
  and *Pflegekosten* are inside its count and ***Pflegerentenversicherung*, written by
  *Lebensversicherer*, is not**; and (b) the count is of contracts, not of insured persons, and one
  person may hold more than one. Any figure taken from this class of source is `[unverified]` and is
  recorded in section 22 with that caution attached (gap 7).

---

## Regulatory and actuarial references

Same retrieval status as the primary sources: **Retrieved: no — direct HTTP egress blocked in the
build environment; no search corroboration (session search budget exhausted).** Canonical URLs are
given where the form is well known and are marked `[unverified]`; elsewhere `URL: not established`.

### R1 — SGB XI, *Elftes Buch Sozialgesetzbuch — Soziale Pflegeversicherung*
- Publisher: Bundesministerium der Justiz / juris, via `gesetze-im-internet.de`
- URL: `https://www.gesetze-im-internet.de/sgb_11/` `[unverified]`
- Content: the statute that creates the *soziale Pflegeversicherung* as the fifth pillar of German
  social insurance. Enacted by the *Pflege-Versicherungsgesetz* (PflegeVG); benefits for care at
  home began in **April 1995** and for *vollstationäre* care in **July 1996** `[unverified]`. Two
  design principles govern everything downstream and are not `[unverified]`, because they are the
  statute's structure rather than a figure: **membership follows health insurance** — everyone in
  the *gesetzliche Krankenversicherung* is in the SPV, everyone in the *private Krankenversicherung*
  must hold the PPV of § 23 [R7] — and the scheme is a **Teilleistungssystem**: it pays defined
  amounts per *Pflegegrad*, not the cost of care, and the residue falls on the insured person. The
  private market this file describes exists entirely because of the second principle.
- Contribution rate: **3,6 %** of assessable earnings from 1 January 2025, shared between employer
  and employee, with a childless surcharge of **0,6** percentage points and reductions of **0,25**
  percentage points per child for the second to the fifth child `[unverified]` — the reductions and
  the surcharge in their present shape date from the PUEG of 2023 [R10]. **Whether the rate changed
  again with effect from 1 January 2026 was not established** (gap 8). Saxony's employer/employee
  split differs `[unverified]`.

### R2 — SGB XI § 14 (*Begriff der Pflegebedürftigkeit*) and § 15 (*Ermittlung des Grades der
  Pflegebedürftigkeit*, the *Pflegegrade*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__14.html`,
  `https://www.gesetze-im-internet.de/sgb_11/__15.html` `[unverified]`
- Content: the two provisions that define the insured event of every German LTC product, public or
  private.
  - **§ 14** defines *Pflegebedürftigkeit* as a health-related impairment of *Selbstständigkeit* or
    of abilities, requiring help from others, expected to last **at least six months** `[unverified]`.
    The decisive reform of 2017 [R9] was to replace the old measure — minutes of care time in
    *Grundpflege* and *hauswirtschaftliche Versorgung* — with a measure of **independence across six
    areas of life**, which brought cognitive and psychiatric impairment (above all dementia) into
    the assessment on equal terms with physical impairment. That change is the reason the number of
    recognised *Pflegebedürftige* rose sharply after 2017 and the reason pre-2017 incidence data
    cannot be used for pricing without adjustment.
  - **§ 15** converts the assessment into a *Pflegegrad*. Six *Module* are scored, weighted and
    summed to *gewichtete Punkte* on a 0-to-100 scale, and the *Pflegegrad* follows from the total.
    Module weights `[unverified]`: *Mobilität* **10 %**; *kognitive und kommunikative Fähigkeiten*
    together with *Verhaltensweisen und psychische Problemlagen* **15 %** — the two are assessed
    separately and the **higher** of the two enters the total; *Selbstversorgung* **40 %**;
    *Bewältigung von und selbständiger Umgang mit krankheits- oder therapiebedingten Anforderungen
    und Belastungen* **20 %**; *Gestaltung des Alltagslebens und sozialer Kontakte* **15 %**. Two
    further areas — *außerhäusliche Aktivitäten* and *Haushaltsführung* — are assessed for care
    planning but **do not enter the score** `[unverified]`.
  - Thresholds on the weighted 0-to-100 scale `[unverified]`: *Pflegegrad* **1** from **12,5** to
    under **27** points (*geringe Beeinträchtigung der Selbstständigkeit*); **2** from **27** to
    under **47,5** (*erhebliche*); **3** from **47,5** to under **70** (*schwere*); **4** from **70**
    to under **90** (*schwerste*); **5** from **90** to **100** (*schwerste Beeinträchtigung mit
    besonderen Anforderungen an die pflegerische Versorgung*).
  - A separate route to *Pflegegrad* 5 exists for people with *besondere Bedarfskonstellationen*
    irrespective of the point total `[unverified]`.

### R3 — SGB XI §§ 36, 37, 38 (*Pflegesachleistung*, *Pflegegeld*, *Kombinationsleistung*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__36.html`, `.../__37.html`, `.../__38.html`
  `[unverified]`
- Content: the benefits for care **at home**, where roughly five in six *Pflegebedürftige* are cared
  for. § 36 provides *Pflegesachleistung* — professional care bought from an approved
  *Pflegedienst*, capped in euro per month by *Pflegegrad*. § 37 provides *Pflegegeld* — a cash sum
  paid to the *Pflegebedürftige* to pass on to whoever cares for them informally, at roughly 44 %
  of the corresponding *Sachleistung* `[unverified]`, conditional on periodic advisory visits.
  § 38 allows the two to be **combined pro rata**: drawing x % of the *Sachleistung* entitlement
  leaves (100 − x) % of the *Pflegegeld*. ***Pflegegrad* 1 receives neither** `[unverified]`. The
  amounts in force are tabulated in section 3 below.

### R4 — SGB XI § 43 (*vollstationäre Pflege*) and § 43c (*Leistungszuschläge*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__43.html`, `.../__43c.html` `[unverified]`
- Content: § 43 sets the monthly amount the SPV pays towards care in a *Pflegeheim*, by
  *Pflegegrad*, with *Pflegegrad* 1 receiving only a small flat contribution. The amount is a
  **contribution to the care-related cost only**: *Unterkunft und Verpflegung*, *Investitionskosten*
  and any *Ausbildungsumlage* are the resident's in full, and so is whatever care-related cost the
  contribution does not meet. Since 2017 [R9] the care-related residue is the
  **einrichtungseinheitlicher Eigenanteil (EEE)** — *identical for* Pflegegrade *2 to 5 within one
  facility*, so that a resident's own payment no longer rises when their condition worsens
  `[unverified]`. § 43c, in force since **1 January 2022** `[unverified]`, adds duration-dependent
  *Leistungszuschläge* that reduce the EEE the longer the resident has been in the facility; the
  steps were raised from **1 January 2024** to **15 %** in the first twelve months, **30 %** in
  months 13–24, **50 %** in months 25–36 and **75 %** from month 37 `[unverified]`, against
  originally 5 / 25 / 45 / 70 % `[unverified]`. The EEE and these *Zuschläge* together are the
  arithmetic of the *Versorgungslücke* (section 4).

### R5 — SGB XI § 45b (*Entlastungsbetrag*), § 39 (*Verhinderungspflege*), § 42 (*Kurzzeitpflege*),
  and the *gemeinsamer Jahresbetrag*
- URL: `https://www.gesetze-im-internet.de/sgb_11/__45b.html`, `.../__39.html`, `.../__42.html`
  `[unverified]`
- Content: the secondary benefit heads. The *Entlastungsbetrag* is a small monthly earmarked amount
  available in **every** *Pflegegrad* including 1, usable for approved relief services rather than
  paid in cash `[unverified]`. *Verhinderungspflege* funds substitute care when the informal carer
  is unavailable; *Kurzzeitpflege* funds short residential stays. From **1 July 2025** the two were
  merged into a single **gemeinsamer Jahresbetrag** for *Pflegegrade* 2 to 5 `[unverified]`, which
  removed the previous rules on transferring budget between them. These heads do not close the
  residential funding gap and are recorded for completeness rather than for the model.

### R6 — SGB XI § 18 (*Begutachtung*) and the *Begutachtungs-Richtlinien* (BRi) of the
  GKV-Spitzenverband
- URL: not established
- Content: § 18 requires the *Pflegekasse* to have *Pflegebedürftigkeit* assessed, in the SPV by the
  **Medizinischer Dienst (MD)**, formerly *MDK*, and in the PPV by **MEDICPROOF GmbH**, the
  assessment service the private sector maintains `[unverified]`. The operational instrument is the
  **Neues Begutachtungsassessment (NBA)**, standardised in the *Begutachtungs-Richtlinien* issued by
  the GKV-Spitzenverband, which prescribe the questions, the scoring of each *Modul*, the conversion
  to *gewichtete Punkte* and the resulting *Pflegegrad*. Four facts about the assessment are
  load-bearing for a private product and are structural rather than numeric:
  1. The assessment is done by a body that is **not the private insurer**, and the private insurer
     ordinarily accepts its result. That makes the private product's claim decision cheap, and it
     also means the private insurer carries **assessment-regime risk**: any loosening of the BRi or
     of § 15 raises the private product's incidence with no contractual change.
  2. Statutory decision deadlines apply to the *Pflegekasse* `[unverified]`, so the lag between
     onset and a determined *Pflegegrad* is measured in weeks, not years — which is why a
     *Karenzzeit* longer than a few months would be a real benefit reduction and not an
     administrative convenience.
  3. A *Höherstufung* is applied for by the insured person and re-assessed; a *Herabstufung* can
     follow a routine re-assessment. Both propagate straight into a private annuity graded by
     *Pflegegrad*.
  4. Assessment is **not** re-done by grade thresholds in continuous time: a person sits at a grade
     until re-assessed, which makes the discrete-state, discrete-time Markov representation of
     section 17 a good match for how the benefit actually behaves.

### R7 — SGB XI § 23 (*private Pflegepflichtversicherung*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__23.html` `[unverified]`
- Content: everyone insured in the *private Krankenversicherung* must hold a private LTC cover whose
  benefits are **at least equivalent** to the SPV's, on terms including a *Kontrahierungszwang* and
  a premium cap `[unverified]`. Its relevance here is entirely definitional: it means the *first
  layer* is the same size for a privately insured person as for a statutorily insured one, so **the
  *Versorgungslücke* the *Pflegerente* addresses is the same for both populations**, and the delib
  model needs no separate PPV variant.

### R8 — SGB XI §§ 126 to 130, in particular § 127 (*Pflege-Bahr*)
- URL: `https://www.gesetze-im-internet.de/sgb_11/__127.html` `[unverified]`
- Content: the state-subsidised private LTC top-up introduced by the *Pflege-Neuausrichtungs-Gesetz*
  (PNG) with effect from **1 January 2013** `[unverified]`, universally called ***Pflege-Bahr*** after
  the then health minister. The scheme, as the statute and the associated *Förderbedingungen*
  provide `[unverified]` throughout:
  - **Zulage**: **5 €** per month, **60 €** per year, paid to the insurer and credited to the
    contract, administered through the *Zentrale Zulagenstelle für Altersvermögen* `[unverified]`.
  - **Minimum own contribution**: **10 €** per month, so a subsidised contract costs at least
    **15 €** per month in total.
  - **No underwriting**: no *Gesundheitsprüfung*, no *Risikozuschlag*, no *Leistungsausschluss*, and
    a *Kontrahierungszwang* on the insurer — anyone aged **18** or over who is not already
    *pflegebedürftig* must be accepted.
  - **Wartezeit**: at most **five years**, shortened where *Pflegebedürftigkeit* results from an
    accident `[unverified]`.
  - **Minimum benefit grid**: at least **600 €** per month in the top *Pflegegrad*, with the lower
    grades at least **10 % / 20 % / 30 % / 40 %** of that amount for *Pflegegrade* 1 to 4
    respectively `[unverified]`. This is the only *Leistungsstaffel* fixed by German statute.
  - **Form restriction**: the subsidised contract must be a **Pflegetagegeld** (*Pflegemonatsgeld*)
    cover conducted *nach Art der Lebensversicherung* with an ageing provision `[unverified]`.
    ***A Pflegerentenversicherung written by a Lebensversicherer cannot be a geförderter Tarif.***
    That is the single most important fact in this entry for delib: the *Zulage* is not available to
    the modelled product, and the delib model does not implement it.
  - The combination of no underwriting with a fixed 5 € subsidy is the design tension the market
    identifies: the subsidy is small relative to the anti-selection the *Kontrahierungszwang*
    creates, so insurers price the residual defensively and the resulting cover is thin.

### R9 — *Zweites Pflegestärkungsgesetz* (PSG II)
- URL: not established
- Content: the reform act that replaced the three *Pflegestufen* with the five *Pflegegrade*,
  replaced the time-based assessment with the NBA, and introduced the *einrichtungseinheitlicher
  Eigenanteil*, with the operative changes taking effect on **1 January 2017** `[unverified]`. The
  act's own date is given in secondary literature as **21 December 2015** `[unverified]`. Three
  consequences for this product:
  1. **A structural break in every time series.** Counts of *Pflegebedürftige*, incidence rates and
     average durations before and after 2017 are not comparable. Any pricing basis calibrated on
     pre-2017 data — which includes any table derived from experience before that date — needs a
     stated mapping from *Pflegestufen* to *Pflegegrade*.
  2. **A broad transitional mapping** moved existing recipients into the new grades without
     re-assessment, generally *Pflegestufe* I → *Pflegegrad* 2, II → 3, III → 4, with a further step
     for people with recognised *eingeschränkte Alltagskompetenz* `[unverified]`. Older private
     wordings written on *Pflegestufen* had to be mapped by the insurer, and a *Pflegerente* sold
     before 2017 and still in force carries that mapping in its terms.
  3. **The population in cover widened**, because cognitive impairment now scores on equal terms.

### R10 — *Pflegeunterstützungs- und -entlastungsgesetz* (PUEG)
- URL: not established
- Content: the 2023 financing and benefit act `[unverified]`. It raised the contribution rate, put
  the childless surcharge and the per-child reductions into their present shape, uprated the benefit
  amounts in two steps — a first increase with effect from **1 January 2024** and a further
  **4,5 %** with effect from **1 January 2025** `[unverified]` — and legislated the merger of
  *Verhinderungspflege* and *Kurzzeitpflege* into a *gemeinsamer Jahresbetrag* from **1 July 2025**
  `[unverified]`. It also provided for regular future *Dynamisierung* of the amounts `[unverified]`.
  **Whether any further uprating took effect on 1 January 2026 was not established**; every benefit
  figure in section 3 is therefore stamped **2025** and gap 8 records the exposure.

### R11 — VVG — the contract-law provisions this product runs on
- Publisher: Bundesministerium der Justiz / juris
- URLs of the canonical form `https://www.gesetze-im-internet.de/vvg_2008/__169.html` etc.
  `[unverified]`
- Content, provision by provision, described in substance and never quoted:
  - **§ 7 and the VVG-InfoV** — pre-contractual information duties; the source of the document
    classes at S5 and S7.
  - **§ 19** — *vorvertragliche Anzeigepflicht*. The applicant must answer the insurer's written
    questions truthfully. The insurer's remedies for breach are graded by fault — rescission,
    termination, contract amendment — and are time-barred, generally after five years, ten in cases
    of intent `[unverified]`. On a product whose claims arrive forty years after underwriting, the
    time bar is what makes the *Gesundheitsprüfung* an incidence-shaping device only for the first
    decade and not thereafter.
  - **§ 153** — *Überschussbeteiligung*. The policyholder participates in the insurer's surplus and
    in the *Bewertungsreserven* unless participation is excluded by agreement; the method must be
    *verursachungsorientiert*. A biometric-risk product's surplus is dominated by the *Risikoergebnis*
    rather than the *Zinsergebnis*.
  - **§ 163** — the narrow circumstances in which a life insurer may adjust a premium: essentially
    where a calculation basis has changed in a way that is not merely temporary and an independent
    trustee agrees. **This is the whole of a *Lebensversicherer*'s re-rating power**, and it is far
    narrower than § 203's for health insurance.
  - **§ 165** — *Beitragsfreistellung*: the policyholder may demand conversion to a paid-up contract
    at any premium due date, the paid-up benefit being calculated by recognised actuarial rules from
    the reserve, less any agreed *Stornoabzug*.
  - **§ 169** — *Rückkaufswert*: on termination the insurer pays the surrender value, computed as
    the actuarial reserve on the tariff bases; acquisition costs must be spread over at least the
    first **five** years `[unverified]`; a *Stornoabzug* is admissible only if agreed, appropriate,
    and **quantified in the contract**. The provision carries an exception for covers that pay only
    on death within a defined period, which is why a *Risikolebensversicherung* has no surrender
    value. **Whether that exception reaches a pure-risk *Pflegerente* — which pays on an uncertain
    event other than death, and which does build a substantial reserve — was not established and is
    gap 9.**
  - **§ 155** — the annual statement (S8) `[unverified]`.
  - **§ 203** — *Beitragsanpassung*, and the point of the whole comparison: **it applies to health
    insurance, not to life insurance.** A *Pflegetagegeld* on the health chassis can be repriced on
    a trustee-approved trigger; a *Pflegerente* on the life chassis cannot, save under § 163.

### R12 — VAG §§ 138, 139, 146, and § 341f HGB
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Content:
  - **§ 138 VAG** — *Rechnungsgrundlagen*: premiums in life assurance must be calculated on
    prudently chosen assumptions and must be sufficient to meet the undertaking's obligations
    permanently `[unverified]`. For a *Pflegerente* the prudence requirement bites hardest on the
    *Pflegewahrscheinlichkeiten*, which are the least stable of the biometric bases.
  - **§ 139 VAG** — *Überschussbeteiligung* and the *Sicherungsbedarf* mechanics on the
    *Bewertungsreserven* `[unverified]`.
  - **§ 146 VAG** — the *substitutive Krankenversicherung* regime: calculation *nach Art der
    Lebensversicherung*, an *Alterungsrückstellung*, and the § 203 VVG adjustment machinery. Cited
    here only to locate the boundary the *Pflegerente* sits on the other side of.
  - **§ 341f HGB** — the *Deckungsrückstellung* in the commercial accounts, computed prospectively
    on the tariff bases `[unverified]`.

### R13 — DeckRV, *Deckungsrückstellungsverordnung*
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Content: the regulation that fixes the **Höchstrechnungszins** — the maximum technical interest
  rate for new business — and the **Höchstzillmersatz**, the cap on acquisition costs that may be
  financed through the reserve, expressed as a per-mille of the *Beitragssumme*. The rate applies to
  the cohort at issue and is then locked for the life of the contract. The German sequence
  `[unverified]` throughout: **4,00 %** to mid-2000, **3,25 %** to 2003, **2,75 %** 2004–2006,
  **2,25 %** 2007–2011, **1,75 %** 2012–2014, **1,25 %** 2015–2016, **0,90 %** 2017–2021,
  **0,25 %** 2022–2024, and **1,00 %** for new business from **1 January 2025**. The
  *Höchstzillmersatz* is **25 ‰** of the *Beitragssumme* `[unverified]`. Both are load-bearing for
  this product: a *Pflegerente* discounts benefits that fall on average some thirty-five years after
  issue, so its premium is more interest-sensitive than any other biometric product in delib, and
  its reserve is *gezillmert* like any other level-premium life contract.

### R14 — KVAV, *Krankenversicherungsaufsichtsverordnung*
- URL: not established
- Content: the calculation regulation for private health insurance — the *Alterungsrückstellung*, the
  *Sicherheitszuschlag*, the *Rechnungszins* ceiling for health business, and the auslösende Faktoren
  that trigger a § 203 VVG *Beitragsanpassung* `[unverified]`. Cited here as the regime the
  *Pflegetagegeld* comparison sits under, never as a rule applying to the modelled product.

### R15 — DAV 2008 P — the German *Pflegetafel*
- Publisher: Deutsche Aktuarvereinigung e. V. (DAV)
- Doc type: standard biometric table with a published derivation paper (*Herleitung*), issued by the
  responsible DAV committee
- URL: not established
- Content — the single most important actuarial reference for this product, and the one whose
  contents this library **cannot and does not redistribute**:
  - **DAV 2008 P is the German market's standard table for LTC business calculated *nach Art der
    Lebensversicherung***, covering both the *Pflegerentenversicherung* written by life insurers and
    the *Pflegetagegeld* written on the life chassis by health insurers `[unverified]`.
  - It is a **multi-state** table, not a single decrement series. What it has to supply for the
    product to be priced at all: **Pflegewahrscheinlichkeiten** — the probability that an active
    life aged *x* becomes *pflegebedürftig* within the year, by sex, by attained age, and **by
    degree of care**; **transition probabilities between degrees**, since deterioration is the
    normal path and is what moves a policyholder up the *Leistungsstaffel*; **Reaktivierungs­wahr­schein­lich­keiten**,
    the small probability of recovery to a lower degree or to the active state; and — decisively —
    **separate mortality for active lives and for lives in care, by degree**.
  - It was constructed on the *Pflegestufen* of the pre-2017 regime `[unverified]`. Its application
    to the five *Pflegegrade* therefore requires a mapping, and any recalibration to post-2017
    experience is the insurer's own work. This is the largest single source of basis risk in the
    product and is gap 10.
  - **The table is the property of the DAV, is not public, and is not redistributed by this
    library.** delib cites it by name, states what a replacement must preserve (section 17), and
    ships a `[std]` proxy anchored so the worked example reproduces exactly — the same posture uklib
    takes about CMI tables and frlib takes about TH00-02/TF00-02.
  - No effective date, no committee name, no *Sicherheitszuschlag* level and no numeric value from
    the table is asserted anywhere in this file.

### R16 — DAV 2008 T and DAV 2004 R
- Publisher: DAV
- URL: not established
- Content: the standard German mortality tables for covers with a death character (DAV 2008 T) and
  for annuities (DAV 2004 R, with its *Bestand* variant) `[unverified]`. They enter this product in
  two narrow places: the **mortality of active lives** before the LTC risk bites, where the DAV
  2008 P active-life mortality is the primary basis but a DAV 2008 T shape is the natural sanity
  check; and the **Todesfallleistung**, where a death benefit written into a *Pflegerente* is a
  death cover and is priced as one. **Neither table is redistributed here.** DAV 2004 R matters as a
  contrast: an annuity table is built to be prudent about people living *longer*, whereas the
  annuity in payment on a *Pflegerente* is paid to a heavily impaired population whose mortality is
  a multiple of the general population's, so **using an annuity table for a Pflegerente in payment
  would be prudent in the wrong direction and materially overprice the benefit**.

### R17 — BaFin supervisory material on life and LTC business
- Publisher: Bundesanstalt für Finanzdienstleistungsaufsicht
- URL: not established (`bafin.de` refused)
- Content: BaFin supervises German life and health insurers, approves the responsible actuary's
  function, and publishes *Merkblätter*, *Rundschreiben*, *Fachartikel* and its annual risk review.
  Its *Wohlverhaltensaufsicht* strand has concentrated on the cost of capital-forming life products
  and on whether products deliver customer value. **Nothing product-specific to
  *Pflegerentenversicherung* was located**, and no BaFin statement of any kind is cited in this file
  (gap 11). The entry is retained because a reader with a working network should look here first for
  any supervisory expectation about *Pflegetafel* prudence or about the *Nachprüfung*.

### R18 — Destatis, *Pflegestatistik*
- Publisher: Statistisches Bundesamt (Destatis)
- Doc type: biennial statutory statistics under SGB XI, reference date in December of the survey
  year, published with a lag
- URL: not established
- Content: the authoritative count of *Pflegebedürftige* in Germany, broken down by *Pflegegrad*, by
  care setting (*zu Hause* versus *vollstationär*), by age and by sex, together with counts of
  *Pflegeheime*, *Pflegedienste* and staff. Figures used in section 21 are `[unverified]`
  reconstructions from memory of this series and are **not** to be treated as read from it. Two
  cautions attach to the series itself and are structural: it counts **people receiving benefits**,
  which after 2017 includes a large *Pflegegrad* 1 population receiving almost nothing in cash; and
  its 2017 break [R9] makes it discontinuous.

### R19 — Destatis, *Pflegevorausberechnung*
- Publisher: Destatis
- URL: not established
- Content: the official projection of the number of *Pflegebedürftige* under stated assumptions
  about prevalence and demography. Its qualitative result is not in doubt and is the whole
  commercial case for the product: **the number of *Pflegebedürftige* rises materially over the next
  three decades, driven by the baby-boom cohorts reaching the ages at which prevalence is high**,
  with the steepest increase in the very oldest ages where prevalence exceeds one in two. Specific
  projected counts and dates are `[unverified]` and appear in section 21 with that tag.

### R20 — vdek and BMG material on the *Eigenanteil* in *Pflegeheimen*
- Publisher: Verband der Ersatzkassen e. V. (vdek); Bundesministerium für Gesundheit
- Doc type: the twice-yearly vdek series on the average resident payment, split into the
  care-related *EEE*, *Unterkunft und Verpflegung*, *Investitionskosten* and *Ausbildungsumlage*,
  by *Bundesland*
- URL: not established
- Content: this is the number the private product is sold against, and the series that shows it
  rising faster than the statutory benefit. Its structure matters as much as its level: **only the
  *EEE* component is reduced by the § 43c *Leistungszuschläge* [R4], and only the *EEE* is equalised
  across *Pflegegrade* 2 to 5** — *Unterkunft und Verpflegung* and *Investitionskosten* are neither
  capped nor subsidised and are the fastest-growing components. Levels are `[unverified]` and appear
  in section 4.

### R21 — PKV-Verband statistics on *Pflegezusatzversicherung* and *Pflege-Bahr*
- Publisher: PKV-Verband
- URL: not established
- Content: as S16, from the regulatory-reference side: the annual counts of subsidised and
  unsubsidised private LTC top-up contracts, the *Zulage* volume, and the associated commentary.
  The **structural** finding, which does not depend on a figure, is that *Pflege-Bahr* take-up rose
  quickly in its first three or four years and then **stopped growing**, and that the unsubsidised
  market is several times larger. Section 22 records the reasons.

### R22 — GDV life-market statistics
- Publisher: GDV
- URL: not established
- Content: the annual life-market series — new business and in-force by product family, premium
  income, and the *Stornoquote*. Its relevance here is entirely negative and worth stating plainly:
  **the GDV series does not carve out *Pflegerentenversicherung* as a reported product family** on
  the evidence available to this file, so **there is no sourced count of German *Pflegerente*
  contracts in force anywhere in this research** (gap 12). The market-size statement in section 22
  is therefore qualitative.

### R23 — EStG — the tax provisions
- Publisher: Bundesministerium der Justiz; BMF for the administrative guidance
- URL: `https://www.gesetze-im-internet.de/estg/` `[unverified]`
- Content, provision by provision, all `[unverified]` as to numbering:
  - **§ 10 Abs. 1 Nr. 3 and Nr. 3a EStG** — *Vorsorgeaufwendungen*. Contributions to the statutory
    LTC scheme and to a *Basiskrankenversicherung* are deductible in full under Nr. 3; contributions
    to a **private LTC top-up**, including a *Pflegerente*, fall under Nr. 3a as *sonstige
    Vorsorgeaufwendungen* and are deductible only within an annual ceiling of **1 900 €** for
    employees and pensioners and **2 800 €** for the self-employed `[unverified]`. Because the Nr. 3
    contributions are counted first and usually exhaust that ceiling on their own, **the deduction
    is worthless for most buyers in practice**. This is the honest statement the product
    specification must carry, and it is the reason the *Pflege-Bahr* *Zulage* [R8] was designed as a
    direct subsidy rather than as a further deduction.
  - **§ 3 Nr. 1a EStG** — exemption for benefits from a *Krankenversicherung*, a *Pflegeversicherung*
    and the statutory accident insurance `[unverified]`. This is what makes *Pflegetagegeld*
    benefits tax-free. **Whether it reaches a *Pflegerente* paid by a *Lebensversicherer* was not
    established and is gap 13** — the competing analysis taxes a lifelong care annuity at the
    *Ertragsanteil* under § 22 EStG, as a *Berufsunfähigkeitsrente* is taxed.
  - **§ 22 Nr. 1 EStG** — the *Ertragsanteil* taxation of *Leibrenten*, the competing analysis just
    described `[unverified]`.
  - **§ 20 Abs. 1 Nr. 6 EStG** — the taxation of life-assurance benefits, relevant only to a
    *Todesfallleistung* or a surrender payment out of a *Pflegerente* `[unverified]`. Death benefits
    are ordinarily outside income tax; *Erbschaftsteuer* may apply where the benefit passes to
    someone other than the policyholder's estate.

### R24 — SGB XII §§ 61 to 66 (*Hilfe zur Pflege*) and the *Angehörigen-Entlastungsgesetz*
- URL: `https://www.gesetze-im-internet.de/sgb_12/` `[unverified]`
- Content: the means-tested social-assistance backstop that pays what the resident cannot, after
  income and all but a small *Schonvermögen* have been used up. Two facts make it directly relevant
  to a private product:
  1. **A private *Pflegerente* with a *Rückkaufswert* is realisable assets** for the means test
     before the claim, and the annuity is **income** during it, so both reduce *Hilfe zur Pflege*
     dependent on the case `[unverified]`. A contract with no surrender value is, on that reasoning,
     the more robust design for a buyer whose likely destination is social assistance — an argument
     for the pure-risk variant that has nothing to do with price.
  2. The **Angehörigen-Entlastungsgesetz**, in force from **1 January 2020** `[unverified]`, limits
     adult children's *Elternunterhalt* liability to children with annual gross income above
     **100 000 €** `[unverified]`. That reform removed the most commonly cited motive for buying
     private LTC cover — protecting one's children from a maintenance claim — from all but
     high-earning families, and shifted the sales argument to protecting the buyer's **own** assets
     and standard of care. Any statement about the effect on sales volumes is `[unverified]`.
