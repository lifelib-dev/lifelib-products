# Sources

Source ids [S#]/[R#] are carried verbatim from `_research/indexpolice.md` (the citation ground
truth for this product) and are **frozen — never renumber**. **No id is absent from this file.**
Unlike its frlib and delib siblings, the `indexpolice` numbering has no gaps: all sixteen primary
sources **S1–S16** and all twenty-two product-level regulatory references **R1–R22** are cited by
`product-spec.md`, and thirteen of the S# and R# entries are cited again by `technical-notes.md`.
That is not a sign of unusual evidential strength. It is the opposite: under the retrieval
conditions below nothing could be *discarded* for saying too little, because none of these
documents was opened, and every one of them is cited for what it **would** settle and for the fact
that it did not. Where a sibling library's `sources.md` records omissions, this one records
absences of a different kind, in each entry's `Retrieved` line. Access date for all sources:
**2026-08-29**. No sources were newly added at drafting. Cross-product [REG-R#] tags are listed in
their own section at the end.

---

## Retrieval conditions — read this before any entry below

**Two independent limits applied while this library was built, and both bound this product
hardest.**

1. **Direct HTTP egress is blocked by an organisation network policy.** `WebFetch` and `curl` are
   refused with HTTP 403 at the egress gateway for every host outside a short package-registry
   allowlist. The hosts that matter here were tried and refused: `gesetze-im-internet.de`,
   `bafin.de`, `gdv.de`, `aktuar.de`, `bundesfinanzministerium.de`, `dejure.org`, `buzer.de`,
   `destatis.de`, `eur-lex.europa.eu` and `de.wikipedia.org`. **No document cited anywhere in this
   file was retrieved.** No *Bedingungswerk*, no *Produktinformationsblatt*, no
   *Basisinformationsblatt*, no statutory text, no BaFin *Merkblatt* and no index rulebook was
   opened.
2. **The session's `WebSearch` budget — 200 calls, shared across the library — was exhausted before
   this product was researched**, during the regulatory and contract-law work and during delib
   products 1 and 2. Every search attempted for `indexpolice` returned the budget-exhausted
   message. **This product therefore had no research channel at all**: `_research/indexpolice.md`
   was written from the author's own knowledge of German insurance law and product design,
   disciplined by the rules the house brief sets for exactly that situation.

What follows from that, stated plainly and without softening:

- **A delib citation is a pointer, not a certificate.** It names the instrument a claim should be
  checked against. It does not assert that anyone checked it.
- **Every entry below is a *known reference*** — a document that exists and is the right kind of
  document for this product — recorded with publisher and document type, with `URL: not
  established` unless the canonical form is one this author is confident of, and with a `Retrieved`
  line that says `no`. **No entry asserts an edition, a document number, a page count or a
  publication date**, because none could be established and none is guessed.
- **Nothing in this file or in the documents that cite it is quoted.** There is no verbatim
  statutory or contractual wording anywhere, because no document was opened and no search summary
  was available to attribute one to. Every description of a statute or a clause is a paraphrase.
- **`[unverified]` is used generously** in the product documents: every paragraph number, effective
  date, amount, percentage, cap level, participation rate, product name and market figure carries
  it unless it is a structural fact of the product that is not in dispute.
- **Uncertain numbers became `[std]` parameters rather than citations.** `indexpolice` carries a
  higher proportion of `[std]` than any other delib product, and `model.md`'s standardization table
  lists every one. A `[std]` number is honest; a fabricated `[S4]` number is not.

---

## Primary product sources

(delib-indexpolice-s1)=

### S1 — GDV, *Musterbedingungen* for the *Rentenversicherung mit aufgeschobener Rentenzahlung*
- Publisher / doc type: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV);
  *Musterbedingungen* — model AVB published by the industry association for members to adopt, adapt
  or ignore. Not binding, not a regulation.
- URL: not established (the GDV *Musterbedingungen* index is a service page on `gdv.de`, which
  refused the fetch).
- Retrieved: **no** — direct HTTP egress blocked in the build environment; **no search
  corroboration** (session search budget exhausted).
- Used for: the clause skeleton every German deferred annuity shares and the Indexpolice inherits
  unchanged — the *Erlebensfall* obligation at *Rentenbeginn*, the *Todesfallleistung* in the
  *Aufschubphase*, the *Überschussbeteiligung* clause, *Rückkaufswert* and *Beitragsfreistellung*,
  the premium-cessation events, the *Rentenphase* clauses and *Selbsttötung*; the single-life,
  unisex design type of the specification's identity table; and — the finding that matters most —
  that **the GDV publishes no model wording for an index-participation module**, which is why
  `product-spec.md` labels its *Indexbeteiligung* clause set a **composite** attributed to no
  carrier and records that wording varies more across insurers here than for any other delib
  product.

(delib-indexpolice-s2)=

### S2 — Allianz Lebensversicherungs-AG, *Allgemeine Versicherungsbedingungen* / *Bedingungswerk* for **Allianz IndexSelect**
- Publisher / doc type: Allianz Lebensversicherungs-AG, Stuttgart; AVB / *Bedingungswerk* for a
  deferred annuity tariff with *Indexbeteiligung*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the product name **Allianz IndexSelect**, carried `[unverified]` as one of the three
  names the specification permits itself; and, far more importantly, for the **central gap**. This
  is the document that would settle the *Indexjahr* definition and its observation dates, the exact
  payoff wording, the base of the participation, the *Wahlrecht* timing and notice period, the
  *Cap-Festlegung* clause and any *Mindest-Cap*, the *Lock-in* clause and the *Ersatzindex* clause.
  **None of that is established from the document**, and `product-spec.md`'s first numbered caveat
  says so. The *Indexjahr* mechanic that `technical-notes.md` implements is cited to it as a
  mechanic that is firm while every level attaching to it is **[std]**.

(delib-indexpolice-s3)=

### S3 — Allianz Lebensversicherungs-AG, *Produktinformationsblatt* / IPID for **Allianz IndexSelect**
- Publisher / doc type: Allianz Lebensversicherungs-AG; *Produktinformationsblatt* — the German
  pre-contractual product summary required by the VVG-InfoV, in the market also labelled with the
  IDD term **IPID**.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **commercial envelope that could not be established** — entry-age band, minimum and
  maximum *Beitrag*, *Aufschubdauer* band, the *Garantieniveau* menu and the guaranteed
  *Rentenfaktor*. `product-spec.md` cites it at its second numbered caveat and at the premium and
  charge tables to record that every one of those parameters is **[std]** construction, not an
  observation, and that the 200,00 € monthly premium and the 40 → 67 term of the anchor cell are
  chosen rather than found.

(delib-indexpolice-s4)=

### S4 — Allianz Lebensversicherungs-AG, *Basisinformationsblatt* (PRIIP-KID) for **Allianz IndexSelect**
- Publisher / doc type: Allianz Lebensversicherungs-AG; *Basisinformationsblatt* under Regulation
  (EU) No 1286/2014 [R10] — the three-page document with the risk indicator, four performance
  scenarios and the full cost table including the *Reduktion der Wertentwicklung*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record that **the only public document class putting a number on the cost and the
  modelled return distribution of a German Indexpolice was not reached**. `product-spec.md` cites
  it in the charge section and in the regulatory-context section for that absence, which is why
  every charge level in delib — *Abschlusskosten*, `β`, `γ`, the *Stornoabzug* — is **[std]** and
  why no performance scenario is reproduced anywhere in this product's documents.

(delib-indexpolice-s5)=

### S5 — Allianz Lebensversicherungs-AG, annual customer notification of the *Indexbeteiligung* parameters for the coming *Indexjahr*
- Publisher / doc type: Allianz Lebensversicherungs-AG; annual policyholder letter or
  customer-portal notice announcing, before each *Indexjahr* begins, the **Cap** (or the
  *Partizipationsquote*) that will apply, and inviting the *Wahlrecht* election.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the mechanic that **the Cap is fixed by the insurer for one *Indexjahr* at a time,
  before it begins, and is then binding for its whole length** — cited in the specification's
  *Indexjahr* row and in `technical-notes.md`'s payoff row as a mechanic that is firm. And for the
  gap: this is the document class in which a real cap level for a named insurer and a named year
  lives, it is sent to policyholders rather than published, and **no instance and no cap value was
  established**. delib's 3,00 % monthly Cap is **[std]**, the midpoint of an argued 1,5–5,0 % band.

(delib-indexpolice-s6)=

### S6 — Allianz Lebensversicherungs-AG, **Allianz Perspektive** documents (the *Neue Klassik* comparator)
- Publisher / doc type: Allianz Lebensversicherungs-AG; AVB, *Produktinformationsblatt* and
  *Basisinformationsblatt* for a *Neue Klassik* deferred annuity **without** index participation.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the ***Neue Klassik* guarantee architecture** on which this whole product rests — a
  guarantee falling due at *Rentenbeginn* rather than accruing as an annual guaranteed rate on the
  reserve, which is what permits the riskier asset mix that generates the surplus that becomes the
  option budget. It carries the specification's design-type row, its account of why guarantee
  levels fell below 100 %, and `technical-notes.md`'s pitfall 11 — that running the guarantee as an
  annual guaranteed rate on the reserve overstates it. The product name **Perspektive** is
  `[unverified]`.

(delib-indexpolice-s7)=

### S7 — R+V Lebensversicherung AG, AVB and product documents for **R+V-IndexInvest**
- Publisher / doc type: R+V Lebensversicherung AG, Wiesbaden; AVB / *Bedingungswerk*,
  *Produktinformationsblatt* and *Basisinformationsblatt* for a deferred annuity with
  *Indexbeteiligung*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the second of the three carrier names the specification permits itself, `[unverified]`;
  and for the reason **no statement of the form "the market does X" appears anywhere in this
  product's documents about any clause** — a second carrier wording is the minimum needed before
  such a statement can be made, and none was obtained. It carries the specification's first
  numbered caveat jointly with [S2] and [S8] and the "not established" column of its variations
  table.

(delib-indexpolice-s8)=

### S8 — Stuttgarter Lebensversicherung a. G., AVB and product documents for **Stuttgarter index-safe**
- Publisher / doc type: Stuttgarter Lebensversicherung a. G.; AVB / *Bedingungswerk*,
  *Produktinformationsblatt* and *Basisinformationsblatt* for a deferred annuity with
  *Indexbeteiligung*.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the third and last carrier name, `[unverified]`, and the specification's statement that
  **no fourth is added**; and for the observation that mid-sized carriers were the most active
  adopters of **house multi-asset indices** in place of the EURO STOXX 50, which is the qualitative
  fact behind the shipped `houseidx_vol5` path and its higher Cap and 100 % *Partizipationsquote*.
  No index name, volatility target or index-level fee is asserted for this or any carrier.

(delib-indexpolice-s9)=

### S9 — Zurich Deutscher Herold Lebensversicherung AG, *Verbraucherinformation* series for konventionelle Rentenversicherungen
- Publisher / doc type: Zurich Deutscher Herold Lebensversicherung AG; *Verbraucherinformation* — a
  combined document carrying the AVB and the VVG-InfoV pre-contractual information for a family of
  conventional annuity tariffs.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the inherited chassis**. The delib research for product 2 (*klassische
  Rentenversicherung*) establishes this series as existing and takes from it the max-of-two
  *Rentenfaktor* rule and the surplus-allocation timing. `product-spec.md` cites it for the
  chassis's *Aufschubphase*/*Rentenphase* structure and for the **standard *Todesfallleistung*
  being a return of the accumulated capital** rather than a sum at risk — the fact that makes the
  *Risikoüberschuss* small, underwriting light and § 161 VVG close to inoperative, and that
  `technical-notes.md` builds `db_pp(t)` on. **Whether the series contains an index variant is not
  established.**

(delib-indexpolice-s10)=

### S10 — GDV *Muster-Standmitteilung* for a *Rentenversicherung*, and carriers' own *Standmitteilungen*
- Publisher / doc type: GDV (model) and individual carriers (actual); the annual statement of
  contract status.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the document class in which an *Indexjahr* result is reported to the policyholder — the
  capital at the start of the year, the Cap that applied, the resulting *Indexrendite* or the
  statement that it was zero, the amount credited and locked in, and the new guaranteed capital.
  `product-spec.md` cites it for the second route by which a cap level reaches the public record
  and, at its gaps discussion, for **the file's most frustrating single absence: no real
  *Standmitteilung* showing a completed *Indexjahr* with its twelve monthly index movements was
  ever obtained.** That absence is the reason the model's two *Indexjahre* at `t = 9` and `t = 10`
  are **constructed** and labelled **[std]** in every cell.

(delib-indexpolice-s11)=

### S11 — *Produktinformationsblatt* under the AltZertG, with the *Chancen-Risiko-Klasse*, for a *Basisrente* or *Riester* index variant
- Publisher / doc type: the certifying carrier, with the class assignment by the
  *Produktinformationsstelle Altersvorsorge gGmbH*; the standardised *Produktinformationsblatt*
  prescribed for certified *Altersvorsorge* products, carrying the **Chancen-Risiko-Klasse** on a
  scale of 1 to 5 [R12] [REG-R43].
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record that **the German market's one standardised, mandatory, comparable product
  disclosure exists only for *Schicht 1* and *Schicht 2* and was not obtained for any index
  variant**. `product-spec.md` cites it jointly with [S3] for the missing commercial envelope and
  in the charge section for the missing effective-cost quota — the two places where a retrieved
  instance would have replaced a **[std]** with an observation.

(delib-indexpolice-s12)=

### S12 — Finanztip, guidance pages on *Indexpolicen*
- Publisher / doc type: Finanztip Verbraucherinformation gGmbH — **secondary**, not a product
  document; consumer guidance page.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: nothing numeric. `product-spec.md` names it, with [S13], [S14] and [S16], in its
  criticism section solely to say **which publishers carry the standing consumer critique of this
  product and that none of them was retrieved** — so the criticisms it then states are reproduced
  as arguments with their strength assessed, not as findings, and no cost quota, cap level or
  outcome statistic is taken from any of them.

(delib-indexpolice-s13)=

### S13 — Stiftung Warentest / *Finanztest*, comparative tests of *Indexpolicen*
- Publisher / doc type: Stiftung Warentest — **secondary**; comparative product test with scoring
  and a cost analysis.
- URL: not established (Stiftung Warentest content is largely paywalled in any case).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the same disclosure as [S12]. A comparative test of this class would supply cap levels,
  cost quotas and modelled outcomes for a named panel of carriers in a named year — precisely the
  evidence the specification's cap and charge gaps record as missing. **Nothing is cited from it.**

(delib-indexpolice-s14)=

### S14 — Verbraucherzentrale Bundesverband e. V. and the Länder consumer centres, pages on *Indexpolicen*
- Publisher / doc type: Verbraucherzentrale Bundesverband and the Länder centres — **secondary**;
  consumer-advice pages.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the attribution of the sector's standing criticisms — that the payoff formula is not
  comprehensible to a normal purchaser, that the Cap is redetermined annually at the insurer's
  discretion, and that a zero year is a frequent outcome — which `product-spec.md` records as
  **positions**, not findings, in its criticism section. **Not retrieved**, so no figure attaches
  to any of them.

(delib-indexpolice-s15)=

### S15 — Comparison portals: Verivox, Check24
- Publisher / doc type: Verivox GmbH and CHECK24 Vergleichsportal GmbH — **secondary**;
  product-comparison and explainer pages.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the usual fallback source for the commercial envelope — minimum premium, entry ages,
  term bands — when insurer *Produktinformationsblätter* are unreachable. `product-spec.md` cites
  it with [S3] and [S11] for the fact that **this fallback failed too**, which is why the
  envelope parameters and the shipped model points are **[std]** construction throughout.

(delib-indexpolice-s16)=

### S16 — German insurance trade press: *procontra*, *Versicherungsbote*, *Versicherungsjournal*, *Cash.Online*, *Versicherungswirtschaft*, *Handelsblatt*
- Publisher / doc type: various — **secondary**; trade and financial press reporting.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record of where cap changes, index switches and the repricing or withdrawal of
  index tariffs are reported, and hence the practical route by which a cap level for a named
  carrier and year reaches the public record alongside [S5] and [R21]. `product-spec.md` names it
  in the criticism section with the other secondary publishers. **Not retrieved**; every figure
  that would have come from it is a gap.

---

## Regulatory and actuarial references (product research numbering)

Where a URL is given below it is the **canonical form** of the address on
`gesetze-im-internet.de`, which this author is confident of for the German federal codes. Every
such URL is tagged `[unverified]` because no search returned it and no fetch confirmed it, and
every paragraph number is `[unverified]` in the documents that cite it. Statutory content is
described in this author's own words.

(delib-indexpolice-r1)=

### R1 — VVG § 153, *Überschussbeteiligung*
- Publisher / doc type: Bundesministerium der Justiz / juris (Gesetze im Internet); federal statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__153.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the statutory hinge of this product**, and the single most load-bearing citation in
  its documents. The policyholder's entitlement is to a share of the surplus and of the
  *Bewertungsreserven*, allocated by a *verursachungsorientiertes Verfahren* or another comparable
  appropriate method agreed in the contract, with half the *Bewertungsreserven* determined at
  termination paid out subject to the supervisory proviso. From it `product-spec.md` takes the
  **correct legal characterisation of the product** — the index participation is a form of
  *Überschussverwendung* with **no independent statutory footing**, so the *Wahlrecht* is an
  *Überschussverwendungswahlrecht* and the payoff formula stands or falls as a contract term — and
  the consequence the model must respect: because the surplus may be zero, **the option budget may
  be zero**, and the year's credit is then necessarily zero whatever the index does. It also
  carries the specification's "no minimum option budget" row.

(delib-indexpolice-r2)=

### R2 — VVG § 169, *Rückkaufswert*
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__169.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the surrender machinery of the product and three separate model facts. That the
  *Rückkaufswert* is the *Zeitwert* / actuarial reserve on recognised principles — hence **a
  general-account reserve and not a unit value**, which is half of the specification's
  not-unit-linked argument; that acquisition and distribution costs must be spread over **at least
  the first five years** for the purpose of the *Mindestrückkaufswert*, which is `min_surr_pp(t)`
  and the shadow account behind it; and that a *Stornoabzug* is effective only if agreed,
  appropriate **and quantified in the contract**, which is why `surr_charge_on` is a model-point
  column rather than a global switch. It also carries the two unestablished points the model
  records as **[std]**: that locked-in credits are inside the surrender value while **the running
  *Indexjahr* is not**, and that whether the unspent option budget is refunded on a mid-year exit
  is not established.

(delib-indexpolice-r3)=

### R3 — VVG § 165, *Prämienfreie Versicherung*
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__165.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the *Beitragsfreistellung* right — conversion at any time to a paid-up contract for the
  reduced benefit computed on recognised actuarial principles for the end of the current insurance
  period, under the same *Stornoabzug* discipline — and the index-specific delta the specification
  states: **a paid-up Indexpolice keeps its index participation on the capital already accumulated
  and the *Wahlrecht* survives**, because the participation attaches to the capital and not to the
  premium. It also carries the premium-cessation row. `technical-notes.md` records
  *Beitragsfreistellung* as deliberately **not modeled**, the paid-up account diverging from the
  premium-paying one at conversion and needing a conversion-cohort ledger.

(delib-indexpolice-r4)=

### R4 — VVG § 163 (*Anpassung der Prämie*) and § 164 (*Ersetzung von Bedingungen*)
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__163.html` and `.../__164.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the most important legal distinction in this product, and the one a careless document
  would blur.** § 163 permits an adjustment of the premium or of the benefit where the calculation
  bases have changed unforeseeably and not merely temporarily, with the confirmation of an
  *unabhängiger Treuhänder*; § 164 permits an ineffective clause to be replaced on the same
  footing. `product-spec.md` cites both to establish that **the annual redetermination of the Cap
  is neither of them** — it is not an adjustment of the contract but the exercise of a discretion
  the contract confers, governed by § 315 BGB [R22]. The *Treuhänder* does appear elsewhere here:
  in the *Ersatzindex* clause, where trustee confirmation is `[unverified]`, and in the historic
  clause on the *Rentenfaktor* inherited from the chassis.

(delib-indexpolice-r5)=

### R5 — VVG § 154 (*Modellrechnung*) and VVG-InfoV § 2 (pre-contractual information)
- Publisher / doc type: Gesetze im Internet; federal statute and federal regulation.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__154.html` and
  `https://www.gesetze-im-internet.de/vvg-infov/__2.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the *Modellrechnung* duty — where the insurer quotes possible benefits beyond the
  contractually agreed ones, three prescribed interest assumptions with a warning that the values
  are not guaranteed — and the pre-contractual information catalogue including the
  ***Effektivkosten***, which `product-spec.md` records as a validation target rather than a model
  input. It also carries the specification's observation that **a *Modellrechnung* for an
  Indexpolice is intrinsically awkward**, the interest assumption reaching the payoff only through
  the option budget and then the Cap, non-linearly; **how carriers discharge the duty for this
  product is not established.**

(delib-indexpolice-r6)=

### R6 — VVG § 161, *Selbsttötung*
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/vvg_2008/__161.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the three-year suicide exclusion on a death cover, with the *Rückkaufswert* owed where
  it applies — carried in the specification's termination table and cited in `technical-notes.md`
  as a clause that is **deliberately not modeled** because it is close to inoperative in economic
  terms here: the *Aufschubphase* death benefit is a return of capital rather than a sum at risk,
  so suppressing it changes almost nothing. Recorded so the documents can say that rather than
  leave it out.

(delib-indexpolice-r7)=

### R7 — *Deckungsrückstellungsverordnung* (DeckRV): *Höchstrechnungszins* and *Höchstzillmersatz*
- Publisher / doc type: Gesetze im Internet; federal regulation.
- URL: `https://www.gesetze-im-internet.de/deckrv_2016/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two of the model's parameters and one of its explanations. The **`guar_rate` cohorts** —
  1,00 % for 2025–2026, 0,90 % for a 2017–2021 cohort, 0,25 % for 2022–2024 — which is why a book
  of this product cannot be projected on one rate and why three cohorts ship; the
  ***Höchstzillmersatz* of 25 ‰ of the *Beitragssumme*** `[unverified]`, the ceiling against which
  delib's 2,5 % acquisition charge sits; and **the reason the product exists at all**: at a
  *Höchstrechnungszins* of 0,25 % the guaranteed component of a conventional annuity's return is
  negligible and the discretionary component is the whole story, so an Indexpolice converts that
  same component into a bounded lottery. The rate history is `[unverified]` step by step.

(delib-indexpolice-r8)=

### R8 — *Mindestzuführungsverordnung* (MindZV)
- Publisher / doc type: Gesetze im Internet; federal regulation.
- URL: `https://www.gesetze-im-internet.de/mindzv/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **where the option budget comes from**, which the specification puts on its first page.
  The MindZV prescribes the minimum share of each source of surplus allocated to policyholders
  through the RfB — 90 % of the *anzurechnende Kapitalerträge* after the charge for discounting the
  *Deckungsrückstellung*, 90 % of the *Risikoergebnis*, 50 % of the *übrige Ergebnis*, as
  established in the sibling delib files. From it both product documents take the corollary that
  **an Indexpolice has exactly the same risk budget as a classic contract of the same vintage and
  spends it differently**, and the model takes its stated limitation: it consumes a **declared**
  rate and does not close the MindZV loop, so changing an expense assumption moves `net_cf` without
  moving what the policyholder receives.

(delib-indexpolice-r9)=

### R9 — VAG § 139 (*Überschussbeteiligung*, *Sicherungsbedarf*), § 124 (*Anlagegrundsatz*) and the *Sicherungsvermögen* provisions
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/vag_2016/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the supervisory side of the surplus participation and the *Sicherungsbedarf*
  restriction on exiting policyholders' share of the *Bewertungsreserven*; the **prudent person**
  investment principle and the derivative provisions permitting derivatives that reduce risk or
  facilitate efficient portfolio management `[unverified]` at section level. `product-spec.md`
  cites it for the proposition that buying index options to back an index-participation obligation
  is **the paradigm of a derivative hedging a liability the insurer has itself written** — matched
  by construction, month for month and cap for cap — so the insurer takes no equity view for the
  policyholder and the Cap is whatever level makes that purchase cost the option budget.

(delib-indexpolice-r10)=

### R10 — PRIIPs: Regulation (EU) No 1286/2014 and Delegated Regulation (EU) 2017/653
- Publisher / doc type: EUR-Lex (the host refused the fetch); EU regulation and delegated
  regulation.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the *Basisinformationsblatt* duty and its prescribed structure — risk indicator, four
  performance scenarios, costs over time and their composition, recommended holding period — and
  the **product categorisation**: an Indexpolice is a **Category 4** PRIIP, part of its value
  depending on a factor not observed in the market, the insurer's discretionary surplus
  declaration, rather than a Category 3 derivative product. `product-spec.md` cites it in the
  regulatory-context section for that, and for the consequence that Category 4 permits the
  insurer's own model, which is why two Indexpolicen with similar mechanics can publish very
  different favourable scenarios. `[unverified]` for any specific carrier's KID.

(delib-indexpolice-r11)=

### R11 — DAV, *Ergebnisbericht* of the *Ausschuss Lebensversicherung* on the PRIIP Category 4 *Standardverfahren*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; professional *Ergebnisbericht*.
- URL: not established (`aktuar.de` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the existence of a German profession-wide standard procedure for computing PRIIP
  performance scenarios for exactly the discretionary-surplus component that makes an Indexpolice a
  Category 4 product — established as existing by the sibling `kapitallebensversicherung` research
  file. `product-spec.md` and `technical-notes.md` cite it beside [R12] at the guarantee row for
  the *Neue Klassik* reading of what is owed at *Rentenbeginn*, and in the PRIIPs discussion for
  the fact that **its content for the index case is not established**, so nothing can be said here
  about how a German Indexpolice's disclosed scenarios are actually computed.

(delib-indexpolice-r12)=

### R12 — *Altersvorsorgeverträge-Zertifizierungsgesetz* (AltZertG) and the *Produktinformationsstelle Altersvorsorge*
- Publisher / doc type: Gesetze im Internet (statute); Produktinformationsstelle Altersvorsorge
  gGmbH (the classification body).
- URL: `https://www.gesetze-im-internet.de/altzertg/` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the sharpest single fact in this product's documents about guarantee levels** — that
  the guarantee level of an index product is set by its **wrapper**, not by its index module. A
  *Schicht 3* Indexpolice may be sold at 60 %, 80 % or 90 % *Beitragsgarantie*; a *Riester* variant
  may not, the *Beitragserhaltungszusage* requiring 100 % of contributions and allowances by
  statute, so it has structurally the smallest option budget of the four wrappers. It carries the
  specification's *Garantieniveau* rows and its account of why the *Riester* market effectively
  closed to new business at a 0,25 % *Höchstrechnungszins*, and, with [R11], the guarantee row of
  `technical-notes.md`. The AltZertG also mandates the standardised *Produktinformationsblatt* of
  [S11] with its *Chancen-Risiko-Klasse*.

(delib-indexpolice-r13)=

### R13 — EStG § 22 Nr. 1 Satz 3, *Ertragsanteilsbesteuerung* of a *Leibrente*
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/estg/__22.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the taxation of a privately funded *Schicht 3* annuity on its ***Ertragsanteil*** only,
  a percentage fixed once and for all by the annuitant's age at *Rentenbeginn* — about 17 % at age
  67 `[unverified]`. `product-spec.md` cites it in the tax section to record that **the index
  mechanic does not change the annuity's tax treatment**, the credits having been absorbed into the
  capital before conversion, and that the wrapper changes it entirely. No tax is computed anywhere
  in this model.

(delib-indexpolice-r14)=

### R14 — EStG § 20 Abs. 1 Nr. 6, the *Kapitalabfindung* and the *Mindesttodesfallschutz*
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/estg/__20.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **three quantitative facts the model actually uses.** The half-income treatment of a
  *Kapitalabfindung* where the contract has run at least **twelve years** and the payment falls
  after the **62nd** birthday `[unverified]`, which is why the specification's *Aufschubdauer* band
  starts at 12 and why a model point shorter than that is excluded on tax grounds rather than
  product grounds; the ***Mindesttodesfallschutz*** condition for contracts concluded from 1 April
  2009, in its standard formulation a death benefit of at least **50 % of the premiums payable**
  `[unverified]`, which is `death_min_rate` and the floor under `db_pp(t)`; and the **duration-12
  step in the lapse table**, the tax threshold being the strongest single driver of German
  surrender behaviour. `product-spec.md` also records the wrinkle that exercising the annual
  *Wahlrecht* is not a change of contract and does not restart the twelve-year clock
  `[unverified]`.

(delib-indexpolice-r15)=

### R15 — RechVersV and the VAG *Sparten*: what "indexgebundene Lebensversicherung" means in regulation
- Publisher / doc type: Gesetze im Internet (RechVersV, VAG); BaFin (statistical classifications);
  federal regulation and statute.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **a terminological trap that a careless document falls into, and the classification the
  whole product rests on.** In the regulatory and accounting vocabulary, the class containing
  *fondsgebundene* and *indexgebundene* life insurance means contracts where the **policyholder
  bears the investment risk** — and an Indexpolice of this kind **does not belong there**: the
  capital is in the *Sicherungsvermögen*, the guarantee is the insurer's, and the downside is
  limited to forgoing one year's surplus. It is booked and reserved as a **conventional
  profit-participating contract**, and in the Solvency II lines of business it sits in *insurance
  with profit participation* rather than *index-linked and unit-linked insurance* `[unverified]` as
  to the numbering. It carries the specification's design-type and where-the-capital-sits rows,
  `technical-notes.md`'s pitfall 1 and its Solvency II pointer, and the delib convention that the
  documents use *Indexpolice* / *Indexbeteiligung* for the product and reserve *indexgebunden* for
  its regulatory sense.

(delib-indexpolice-r16)=

### R16 — BaFin, *Merkblatt* 01/2023 (VA) on conduct supervision of capital-forming life insurance products
- Publisher / doc type: Bundesanstalt für Finanzdienstleistungsaufsicht; supervisory *Merkblatt*.
- URL: not established (`bafin.de` refused the fetch).
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: BaFin's expectations on the product governance and *angemessener Kundennutzen* of
  capital-forming life products — established as existing by the sibling `kapitallebensversicherung`
  research file, where it supported the propositions that *Effektivkosten* differ considerably
  across the market and that BaFin will examine outliers. `product-spec.md` cites it in the charge
  section and the regulatory frame, and `technical-notes.md` in its charge sensitivity, for the
  observation that an Indexpolice raises the value-for-money question in its sharpest form — a
  design that credits zero in a substantial fraction of years while carrying a full acquisition-cost
  load. **Whether the *Merkblatt* names index products is not established.**

(delib-indexpolice-r17)=

### R17 — BaFin, *Risiken im Fokus* and the BaFin *Fachartikel* series on costs and PRIIPs
- Publisher / doc type: BaFin; annual risk report and supervisory articles.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the context that the cost of capital-forming life insurance is a **named supervisory
  focus risk**, cited once in `product-spec.md`'s charge discussion beside [R16] to place the
  **[std]** charge levels against a supervisory frame rather than against a market observation.
  Nothing numeric is taken from it.

(delib-indexpolice-r18)=

### R18 — DAV recommendations on the *Höchstrechnungszins*
- Publisher / doc type: Deutsche Aktuarvereinigung e. V.; annual professional recommendation to the
  Bundesministerium der Finanzen, which sets the rate by regulation.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **1,00 %** recommendation for 2025 and again for 2026, established from search
  evidence in the sibling delib files and reproduced here as a cross-reference rather than as a
  finding of this file. It fixes the guarantee basis of a contract issued at the access date, and
  hence the split between the guaranteed capital and the option budget, and it carries the anchor
  cell's `guar_rate = 0,0100` in both product documents.

(delib-indexpolice-r19)=

### R19 — GDV statistics: *Die deutsche Lebensversicherung in Zahlen* and the new-business and in-force series
- Publisher / doc type: GDV; annual industry statistics.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: two negatives that both product documents state rather than gloss. **The GDV product
  split does not isolate Indexpolicen** — they are counted within conventional annuity business,
  because that is what they are [R15] — so **there is no published figure for the size of the
  German index-participation segment**, and no statement about its size appears anywhere in this
  product's documents. And the *Stornoquote*: the market-wide measures recorded in the sibling file
  are irreconcilable with each other and **no index-specific rate exists at all**, which is why
  `lapse_table.csv` is **[std]** in level and shaped only by the tax threshold of [R14].

(delib-indexpolice-r20)=

### R20 — Assekurata, *Marktstudie* on *Überschussbeteiligungen und Garantien*
- Publisher / doc type: Assekurata Assekuranz Rating-Agentur GmbH; annual market survey of declared
  surplus rates and guarantee designs.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the **declared surplus rate**, which for this product *is* the option budget [R8], so
  an Assekurata declared-rate series is the closest public proxy for its size. The 2026 market
  averages recorded in the sibling delib files place `surplus_rate = 2,50 %` inside an argued
  2,0–3,0 % band; both product documents cite it there and both say the figure is a
  cross-reference, not a finding of this product's research. **Whether Assekurata publishes cap
  levels as such is not established.**

(delib-indexpolice-r21)=

### R21 — Rating houses on *Indexpolicen*: IVFP, Franke und Bornberg, Morgen & Morgen
- Publisher / doc type: Institut für Vorsorge und Finanzplanung GmbH; Franke und Bornberg GmbH;
  MORGEN & MORGEN GmbH; product ratings of retirement-savings contracts.
- URL: not established.
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: the record of **the one document class that would have closed three gaps at once** — a
  rating of index-linked annuities is the only systematic public compilation this author is aware
  of that puts cap levels and participation rates for a panel of named carriers side by side, and
  it would have supplied the product-name inventory as well. `product-spec.md` cites it, with [S5]
  and [S10], for the fact that **nothing from it was established**, and therefore that the
  1,5–5,0 % cap band quoted throughout is this author's recollection of the market and is
  `[unverified]`, while the shipped 3,00 % is **[std]**.

(delib-indexpolice-r22)=

### R22 — BGB § 315, *Bestimmung der Leistung durch eine Partei* (*billiges Ermessen*)
- Publisher / doc type: Gesetze im Internet; federal statute.
- URL: `https://www.gesetze-im-internet.de/bgb/__315.html` `[unverified]`
- Retrieved: **no** — egress blocked; no search corroboration.
- Used for: **the correct legal frame for the annual *Cap-Festlegung***, which is the point on
  which this product's documents most needed to be right. Where a contract leaves the determination
  of a term to one party, that party must exercise it according to reasonable discretion; a
  determination made otherwise is not binding and, on application, is made by the court. The Cap is
  a unilateral determination of a term deciding the policyholder's return for the coming year, so
  it is reviewable under § 315 BGB — **not** under § 163 VVG, which governs adjustments of the
  contract itself [R4]. `product-spec.md` states that distinction twice, once in the
  *Cap-Festlegung* mechanics and once in the criticism section, and records that **no German
  decision on the point is known to this author and none was established**, so the framing is
  doctrinally sound and untested in the sources available here.

---

## Cross-product references ([REG-R#])

[REG-R#] tags resolve against the cross-product German reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, R1–R56, frozen; research
provenance in `_research/regulatory-actuarial.md`). **Every entry in that library carries the same
retrieval status as this file**: no document was fetched, and each entry records per fact whether a
web search corroborated it before the budget was exhausted. Entries cited by the `indexpolice`
documents:

- **REG-R1** — Directive 2009/138/EC (Solvency II): the best-estimate-plus-risk-margin frame the
  projected cash flows feed.
- **REG-R2** — Delegated Regulation (EU) 2015/35: contract boundaries, future discretionary
  benefits and management actions — none read from a retrieved text, so every such figure would be
  `[unverified]`.
- **REG-R4** — EIOPA risk-free term structures, the UFR and the *Volatilitätsanpassung*: the curve
  a valuation layer would discount `liability_cf` on. Nothing here discounts.
- **REG-R7** — VAG §§ 124–125, *Anlagegrundsätze*, *Sicherungsvermögen* and *Anlagestock*: the
  statutory pair behind the specification's central distinction — the capital of an Indexpolice is
  in the *Sicherungsvermögen* and there is no *Anlagestock*.
- **REG-R9** — VAG § 139, *Überschussbeteiligung* and the *Sicherungsbedarf* test on
  *Bewertungsreserven*: the supervisory side of [R1], and the reason the *Bewertungsreserven* share
  is referenced and not modeled.
- **REG-R10** — VAG §§ 140 and 145, the RfB: where the declared rate comes out of.
- **REG-R13** — VAG §§ 351–353, the Solvency II transitional measures: context only.
- **REG-R14** — DeckRV and its § 2, the *Höchstrechnungszins*: the reserving rate cap behind
  `guar_rate`.
- **REG-R15** — the *Höchstrechnungszins* rate history and the 2024 regulation setting 1,00 % from
  1 January 2025: the anchor cell's guaranteed rate and the three shipped cohorts.
- **REG-R16** — DeckRV § 4, *Höchstzillmersätze*: the 25 ‰ ceiling the 2,5 % acquisition charge
  sits at, and half of pitfall 13.
- **REG-R17** — DeckRV § 5 Abs. 3, the *Referenzzins* and the *Zinszusatzreserve*: referenced as a
  reserving layer this library does not compute.
- **REG-R18** — MindZV: the statutory minimum allocation that bounds the option budget, cited with
  [R8] wherever the financing identity is stated.
- **REG-R20** — LVRG 2014: the reform that cut the *Höchstzillmersatz* to 25 ‰ and reshaped the
  *Bewertungsreserven* rule.
- **REG-R23** — VVG §§ 8 and 152, the *Widerrufsrechte*: the withdrawal window, absorbed into the
  first-year lapse rate and not modeled separately.
- **REG-R24** — VVG § 153: the cross-product entry behind [R1], carrying the
  *verursachungsorientiertes Verfahren* and the half-share of *Bewertungsreserven*.
- **REG-R25** — VVG §§ 154–155, *Modellrechnung* and *Standmitteilung*: the statutory basis of the
  document class [S10] belongs to, and the three-interest-rate model the specification reports at a
  1,00 % *Höchstrechnungszins*.
- **REG-R26** — VVG §§ 150, 159–162: *Selbsttötung* and the beneficiary machinery, behind [R6].
- **REG-R27** — VVG § 163: the cross-product entry behind [R4] and the *Treuhänder* requirement.
- **REG-R28** — VVG §§ 165–170: the exit machinery — *prämienfreie Versicherung*, *Kündigung*,
  *Rückkaufswert* and the *Stornoabzug* — behind [R2] and [R3], and the other half of pitfall 13.
- **REG-R30** — VVG §§ 19, 37, 38, 157, 158: *Anzeigepflicht*, *Zahlungsverzug* and the age-error
  rule; context for the termination table.
- **REG-R31** — VVG §§ 6, 7, 1a and the VVG-InfoV: advice, information and the *Effektivkosten*
  disclosure duty, cited with [R5].
- **REG-R32** — PRIIPs Regulation and the delegated technical standards: the cross-product entry
  behind [R10] and the Category 4 classification.
- **REG-R34** — Unisex: CJEU C-236/09 (*Test-Achats*) and §§ 19, 20, 33 AGG — why `sex` selects a
  best-estimate mortality row and never a premium, a charge or a benefit.
- **REG-R35** — BaFin *Merkblatt* 01/2023 (VA), *Wohlverhaltensaufsicht* and *angemessener
  Kundennutzen*: the cross-product entry behind [R16].
- **REG-R41** — EStG § 22 Nr. 1 Satz 3 Buchst. a: *Besteuerungsanteil* and *Ertragsanteil*, behind
  [R13].
- **REG-R43** — AltZertG, the BZSt, the AltvPIBV and the Produktinformationsstelle Altersvorsorge:
  the cross-product entry behind [R12] and [S11], and the source of the statutory 100 % *Riester*
  guarantee.
- **REG-R45** — EStG § 20 Abs. 1 Nr. 6: the *Unterschiedsbetrag*, the 12/62 rule and the
  *Mindesttodesfallschutz*, behind [R14] and behind `death_min_rate = 0,50`.
- **REG-R48** — DAV 2008 T: the death-benefit mortality basis, **cited by name and never shipped**.
- **REG-R49** — DAV 2004 R and DAV 2004 R-Bestand: the generational annuity tables, **cited by name
  and never shipped** — and the reason the *Rentenfaktor* is a **[std]** input rather than a
  computed quantity.
- **REG-R53** — the German life market in numbers (GDV, BaFin, Assekurata, Map-Report, Morgen &
  Morgen, Franke und Bornberg): the 2026 declared-rate averages behind `surplus_rate = 2,50 %`, the
  sector *Verwaltungskostenquote* band, and the *Neue Klassik* context.
- **REG-R54** — HGB §§ 341–341o, RechVersV and BerVersV: the statutory *Deckungsrückstellung*,
  including **profit shares already allocated** — the phrase that makes every locked-in index credit
  part of the reserve from the moment it is credited.
- **REG-R55** — IFRS 17 and the Variable Fee Approach: the measurement model this contract is the
  archetype of; its mechanics were not read and are `[unverified]`.

---

## Provenance note

Extraction details — which fact would be settled by which document, the mechanics sections the
product documents are actually written from, the two constructed *Indexjahre*, the expected-value
arithmetic behind the cap, and the twenty-four-item gaps-and-caveats register — live in
`_research/indexpolice.md`. That file is the citation ground truth for the S# and R# numbering used
here, and it states its own retrieval conditions at its head in the same terms as this file.

The caveats that most affect what these product documents can claim, in order of how much they
constrain the model:

1. **No carrier *Bedingungswerk* for an index tariff was obtained** [S2] [S7] [S8]. The AVB settles
   the *Indexjahr* definition, the observation dates, the payoff wording, the base of the
   participation, the *Wahlrecht* timing, the *Cap-Festlegung* clause, any *Mindest-Cap*, the
   *Lock-in* and the *Ersatzindex* clause. Everything on those points is written from knowledge of
   the design family. **Get one AVB and half of this register closes.**
2. **No cap level, for any insurer, in any year, was established** [S5] [S10] [R21]. Not one. The
   1,5–5,0 % band is recollection and is `[unverified]`; the shipped 3,00 % is **[std]**.
3. **No documented worked *Indexjahr* was found** [S10] — no *Standmitteilung*, no insurer
   illustration, no consumer-press example with twelve monthly movements and a resulting credit.
   The two *Indexjahre* the model reproduces at `t = 9` and `t = 10` are **constructed**, and every
   cell of them is **[std]**.
4. **The commercial envelope is entirely [std]** [S3] [S11] [S15]: no entry-age band, minimum
   premium, term band, *Garantieniveau* menu or *Rentenfaktor* level was established for any
   carrier, so the thirteen shipped model points are construction rather than observation.
5. **No charge level of any kind was established** [S4], and the three index-specific give-ups —
   the dealing spread inside the Cap, a house index's level fee and volatility-target drag, and the
   forgone dividend yield of a price index — are **structurally invisible in any disclosure**. That
   invisibility is a finding; their magnitude is a gap.
6. **The base `G` of the participation is unestablished** — whole *Deckungskapital*,
   index-participating sub-account, or accumulated *Überschussguthaben* alone. delib takes the whole
   capital **[std]**; **a different reading rescales every credit in the model**, which makes this
   the largest unquantified uncertainty in the product.
7. **The mid-year exit treatment is unestablished** [R2]: whether surrender, death or annuitisation
   inside an *Indexjahr* attracts a pro-rata credit, a refund of the unspent option budget, or
   nothing. delib's **[std]** is nothing, and it is a real cash-flow difference.
8. **No decided German case on the *Cap-Festlegung* is known** [R22], and no house multi-asset
   index is named anywhere, because none could be established and a wrong name would be worse than
   none.
9. **Nothing in this file's chain is quoted, and nothing was retrieved.** The VVG, the DeckRV, the
   MindZV, the VAG, the AltZertG, the EStG and the PRIIPs delegated regulation are all living
   texts, and the *Höchstrechnungszins* is reset by regulation. Every date, rate and paragraph
   number must be re-checked against the instrument before it is relied on. **A delib citation is a
   pointer, not a certificate.**
