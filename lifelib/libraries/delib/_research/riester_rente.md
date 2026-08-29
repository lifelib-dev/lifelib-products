# Riester-Rente (Schicht 2) — research notes (Germany)

Research notes for the German **state-subsidised private pension of the second layer** — the
*Riester-Rente*, a **zertifizierter Altersvorsorgevertrag** under the
*Altersvorsorgeverträge-Zertifizierungsgesetz* (AltZertG) whose defining features are three:
the state pays *Zulagen* (subsidy payments) **into the contract as real cash flows**; the provider
must guarantee that at *Rentenbeginn* (the start of the payout phase) **at least the sum of the
contributions paid plus the Zulagen credited** is available; and the resulting benefit is a
**lifelong** monthly annuity taxed **in full** as *sonstige Einkünfte* under § 22 Nr. 5 EStG.

**In scope.** The single-life **klassische Riester-Rentenversicherung**: a deferred general-account
annuity contract, sold to an individual, certified under the AltZertG, funded by a level or
increasing *Eigenbeitrag* (the saver's own contribution) plus the annual *Grundzulage*,
*Kinderzulage* and, once only, the *Berufseinsteiger-Bonus*; accumulating in the insurer's
*Deckungskapital* at the guaranteed *Rechnungszins* with *Überschussbeteiligung*; carrying the
statutory **100 % Beitragsgarantie** at *Rentenbeginn*; converting at *Rentenbeginn* into a lifelong
*Leibrente* at a guaranteed *Rentenfaktor*, with up to **30 %** of the capital available as a
*Teilkapitalauszahlung*; and carrying the statutory options — *Anbieterwechsel*,
*Beitragsfreistellung*, *Kündigung* with the *förderschädliche* consequences that follow, and the
*Kleinbetragsrenten-Abfindung*.

**Out of scope, and named here so the boundary is explicit.**

- **Wohn-Riester** (*Eigenheimrente*) — the *Altersvorsorge-Eigenheimbetrag* of § 92a EStG, the
  Riester-*Bausparvertrag*, the Riester-*Darlehen* and the *Wohnförderkonto* of § 92a/§ 92b EStG.
  These are described at length in section 16 below, because a reader of a Riester model will ask
  where they went, and because a Riester **insurance** contract can itself be emptied into a
  property purchase. They are excluded from the model for one structural reason: the
  *Wohnförderkonto* is a **notional tax-bookkeeping account carrying no cash flow at all**, and the
  Riester-*Darlehen* is a loan liability, not an insurance liability. Neither produces a benefit
  cash flow a liability projection can publish.
- **Riester-Fondssparplan** and **Riester-Banksparplan** — certified under the same AltZertG and
  drawing the same Zulagen, but with no insurance liability: the provider is a
  *Kapitalverwaltungsgesellschaft* or a bank, the accumulation is a fund or deposit balance, and
  the lifelong element is bought in only at the end (section 17). They are recorded here in full
  because the **Zulagen mechanics are identical** and because the shape of the market cannot be
  understood without them.
- **Fondsgebundene Riester-Rentenversicherung** — the unit-linked wrapper with the same guarantee.
  Its guarantee machinery (*statisches* and *dynamisches Hybridmodell*, *i-CPPI*, the two- and
  three-pot designs) is described in section 18 because it is the sharpest illustration of what the
  100 % *Beitragsgarantie* does to an asset allocation; the delib model for the unit-linked chassis
  is `fondsgebundene_rentenversicherung`, which is Schicht 3 and unsubsidised.
- **Basisrente (Rürup), Schicht 1** — delib `basisrente`. It shares the *nachgelagerte Besteuerung*
  and the annuitisation constraint but has **no Zulagen, no Beitragsgarantie requirement, no
  Teilkapitalauszahlung and no Kapitalwahlrecht**, and is deductible under § 10 Abs. 1 Nr. 2 EStG
  rather than § 10a. The GDV maintains a **separate** model condition set for it [S3].
- **Riester in der betrieblichen Altersversorgung** — a *Direktversicherung*, *Pensionskasse* or
  *Pensionsfonds* funded from taxed salary and Riester-subsidised under § 82 Abs. 2 EStG. bAV is
  outside delib entirely. The one point kept here is that the *Betriebsrentenstärkungsgesetz* 2017
  removed the double *Krankenversicherung* charge on such annuities (section 15).
- **Klassische Schicht-3 Rentenversicherung** — delib `klassische_rentenversicherung`. It is the
  same general-account chassis with none of the Schicht-2 apparatus; that file is the primary home
  for the *Deckungskapital* recursion, the four *Überschuss* components, § 169 VVG *Rückkaufswert*
  and § 165 VVG *Beitragsfreistellung*. Those mechanics are restated here only to the extent the
  Riester rules change them, which they do in three places: the guarantee, the surrender, and the
  taxation.
- **Gruppenversicherung**, **private Krankenversicherung**, **Sterbegeldversicherung** and
  institutional pension-risk transfer.

These notes are the citation ground truth for the delib `riester_rente` product documents: source
ids **S1..S16** and **R1..R26** below are **frozen — never renumber**. Unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which ids are absent and why.

Access date for all citations: **2026-08-29**.

---

## Citation discipline and retrieval conditions

**No document listed in this file was retrieved, and no web search was run for it.** Two
independent limits applied, and both must be stated plainly because a reader who picks up this
document alone has to learn them from it.

**Limit 1 — direct HTTP egress is blocked.** An organisation network policy refuses `WebFetch` and
`curl` with HTTP 403 at the egress gateway for every host outside a short package-registry
allowlist. The hosts that matter for this product were all refused in the delib build session:
`gesetze-im-internet.de` (the AltZertG and the EStG), `bundesfinanzministerium.de` (the BMF
*Anwendungsschreiben* and the *Fokusgruppe* report), `bmas.de` (the quarterly Riester contract
statistics), `bafin.de`, `gdv.de`, `aktuar.de`, `deutsche-rentenversicherung.de` (the ZfA),
`bzst.de` (the *Zertifizierungsstelle*), `destatis.de`, `dejure.org`, `de.wikipedia.org`, and every
insurer, fund-house and bank host named below. **Nothing was downloaded, opened or read.**

**Limit 2 — the session's `WebSearch` budget was exhausted before this file was started.** The
budget of 200 calls was shared across the parallel delib researchers and was spent on the
prudential and contract-law files; every search attempted for this product returned the
budget-exhausted message. **This file therefore had no research channel at all** — neither
retrieval nor search.

What follows from that, exactly, and it governs every line below:

1. **Every source entry records `Retrieved: no — direct HTTP egress blocked in the build
   environment; no search corroboration (session search budget exhausted)`.** Nothing here is
   marked retrieved. The sources are listed as **known references** — documents that exist and are
   the right kind of document for this product — not as documents anyone consulted.
2. **No URL, document number, edition, page count, publication date or *Zertifizierungsnummer* was
   guessed.** Where a URL is not available the entry says `URL: not established`. Two URLs appear
   in canonical `gesetze-im-internet.de` form and one `gdv.de` index URL appears; the statutory
   ones are marked `[unverified]`, and the GDV index URL is the one a search returned in a **sibling
   delib research session**, attributed as such.
3. **No verbatim quotation of any document is given.** Where a German phrase appears in quotation
   marks it is a **term of art**, not a quotation from an instrument.
4. **`[unverified]` is used generously.** Every paragraph number, effective date, monetary amount,
   percentage, threshold and market figure in this file is a claim from general knowledge of German
   pension law that **no search result confirmed**, and carries the tag. The general *shape* of a
   well-established mechanic — that a Zulage is paid into the contract, that the payout must be a
   lifelong annuity — is not tagged, because tagging it would drown the signal. The moment a claim
   becomes specific and numeric, it is tagged.
5. **Where the mechanic is certain and the level is not, the level becomes a `[std]` parameter of
   the reference implementation with a stated rationale, not a citation.** Every charge level, every
   *Rentenfaktor*, every *Überschuss* rate, every lapse and *Beitragsfreistellung* rate downstream
   is `[std]`. A `[std]` number is honest; a guessed `[S5]` number is not.

**Three facts in this file come from a sibling delib research session's searches**, and are
attributed to that file rather than claimed here: the GDV's *Musterbedingungen* index and its
product taxonomy including a *fondsgebundene* Riester wrapper under the AltZertG and a
non-unit-linked variant carrying "Stand: 21.07.2025" [S3]; the CosmosDirekt AVB numbering series in
which **LA 1005 A** is the Riester wording [S4]; and a third-party cost analysis of an Allianz
specimen quotation reporting total costs in the *RiesterRente* variant of at most **0,95 € per
100 €** of capital formed [S5]. Those three are the only search-corroborated items here, and each
says so at the point of use.

**The arithmetic in sections 4, 12 and 19 is computed, not sourced.** Where this file derives a
number — the *Mindeseigenbeitrag* worked cases, the guarantee-headroom table, the income thresholds
at which the *Sockelbeitrag* binds — the inputs are tagged and the derivation is shown, so a reader
can redo it. Derived numbers are marked `[std] derived` and are exact given their inputs.

---

## German terminology

German terms of art stay in German throughout the delib documents, italicised on first use with a
gloss. The vocabulary this product needs, beyond the shared Schicht-3 vocabulary carried in
`_research/klassische_rentenversicherung.md`:

| Term | Gloss |
|---|---|
| *Altersvorsorgevertrag* | the statutory contract type of § 1 AltZertG; only a **certified** contract attracts the subsidy |
| *Zertifizierung* | the confirmation by the certifying authority that the contract's **terms** meet the § 1 AltZertG criteria — expressly **not** a statement about the provider's solvency, the product's cost or its expected return |
| *Zulage* / *Altersvorsorgezulage* | the state subsidy paid **into the contract**; the umbrella term for *Grundzulage* and *Kinderzulage* |
| *Grundzulage* | the basic annual subsidy per eligible saver |
| *Kinderzulage* | the annual subsidy per child for whom *Kindergeld* is drawn |
| *Berufseinsteiger-Bonus* | a one-off addition to the *Grundzulage* for a young saver in the first subsidised year |
| *unmittelbar zulageberechtigt* | directly eligible: the saver's own status (statutory pension insurance, civil service, and the listed equivalents) creates the entitlement |
| *mittelbar zulageberechtigt* | indirectly eligible: entitlement derived from a spouse who is *unmittelbar* eligible, conditional on the saver holding an own contract and paying the *Sockelbeitrag* |
| *Mindesteigenbeitrag* | the saver's own contribution required in full to draw the full Zulagen; a percentage of the previous year's income, capped, **less** the Zulagen |
| *Sockelbeitrag* | the floor under the *Mindesteigenbeitrag*: the smallest own contribution that will ever draw the full Zulagen |
| *Eigenbeitrag* | the part of the contribution the saver actually pays, as against the Zulagen |
| *Sonderausgabenabzug* | the income-tax deduction of § 10a EStG for the contributions **and** the Zulagen |
| *Günstigerprüfung* | the tax office's automatic comparison of the § 10a deduction against the Zulagen, granting whichever is more favourable |
| *Beitragsgarantie* / *Beitragserhaltungszusage* | the provider's undertaking that at *Rentenbeginn* at least the contributions paid plus the Zulagen credited are available |
| *Rentenbeginn* / *Beginn der Auszahlungsphase* | the boundary between accumulation and payout; the date the *Beitragsgarantie* is tested |
| *Teilkapitalauszahlung* | the lump sum, capped at a statutory share of the capital, that may be taken at *Rentenbeginn* without losing the subsidy |
| *Auszahlungsplan mit Restverrentung* | the non-insurance payout form: scheduled withdrawals, then a lifelong annuity bought with the remainder from a statutory age |
| *Kleinbetragsrente* | an annuity too small to administer, which the provider may commute to a lump sum without *schädliche Verwendung* |
| *Abfindung* | that commutation payment |
| *Fünftelregelung* | the spread-over-five-years tariff relief of § 34 EStG applied to such a commutation |
| *nachgelagerte Besteuerung* | deferred taxation: contributions relieved, benefits taxed in full |
| *schädliche Verwendung* | a use of the capital outside the permitted purposes, which triggers repayment of the subsidy |
| *Rückzahlungsbetrag* | the amount of Zulagen and § 10a tax relief repayable on *schädliche Verwendung* |
| *förderunschädlich* | subsidy-preserving; the opposite of *schädlich* |
| *Anbieterwechsel* / *Wechselrecht* | the statutory right to move the accumulated capital to another certified contract |
| *ruhender Vertrag* | a contract on which contributions have stopped but which has not been surrendered — *beitragsfrei gestellt* |
| *Wohn-Riester* / *Eigenheimrente* | the housing variant: capital withdrawn for, or loan repayments made on, owner-occupied property |
| *Wohnförderkonto* | the notional account recording the housing use for later taxation, accruing a statutory notional rate |
| *Produktinformationsblatt* (PIB) | the standardised pre-contractual disclosure prescribed for Altersvorsorgeverträge, carrying the *Effektivkosten* and the *Chancen-Risiko-Klasse* |
| *Effektivkosten* | reduction in yield: the annual percentage by which charges reduce the return |
| *Chancen-Risiko-Klasse* (CRK) | the 1-to-5 risk/return class assigned to a certified product by the *Produktinformationsstelle Altersvorsorge* |
| *Zentrale Zulagenstelle für Altersvermögen* (ZfA) | the authority that determines, pays and reclaims the Zulagen |
| *Leistungsmitteilung* | the provider's annual statement of benefits paid, sent to the recipient and to the tax administration |

---

## Primary sources

Sixteen known references. **None was retrieved and none was corroborated by a search run for this
file** (three carry corroboration inherited from a sibling delib session and say so). They are
listed because a research file's job is to name the documents a downstream claim must be checked
against, and because the *kinds* of document that exist for a German Riester product are themselves
a finding: unlike the French corpus, where a single *notice d'information* carries everything, the
German Riester disclosure is split across four documents — the **AVB** (the contract terms), the
**Produktinformationsblatt** (the statutory comparison sheet, with the *Effektivkosten* and the
*Chancen-Risiko-Klasse*), the **Verbraucherinformation / vorvertragliche Information** (the VVG-InfoV
pack) and the **jährliche Information** (the annual statement) [R4] [R5].

Four families are represented: the **GDV model conditions** [S1] [S2] [S3], the shared drafting
template; the **insurance wordings** [S4]–[S8] [S16], which are the product this model represents;
the **fund and bank wordings** [S9]–[S12], which are the same subsidy on a different chassis; and
the **Wohn-Riester** documents [S13], which are the boundary of scope. [S14] and [S15] are the two
statutory disclosure artefacts that every one of the others carries.

### S1 — GDV, "Allgemeine Bedingungen für die fondsgebundene Rentenversicherung nach dem Altersvorsorgeverträge-Zertifizierungsgesetz" (Musterbedingungen)
- Publisher: Gesamtverband der Deutschen Versicherungswirtschaft e. V. (GDV), Berlin
- Doc type: *Musterbedingungen* — model general policy conditions for a **unit-linked Riester
  annuity**; the association's template wording, which individual insurers adopt, adapt or ignore.
  The GDV's own standing disclaimer on this series is that the wording is **non-binding**, its use
  optional [S3].
- URL: not established
- Retrieved: no — direct HTTP egress blocked in the build environment; existence and title family
  established from a **sibling delib research session's** search of the GDV *Musterbedingungen*
  index [S3]; no search corroboration in this session (budget exhausted).
- Content: establishes that the GDV maintains a model condition set **specifically for the
  Altersvorsorgevertrag under the AltZertG**, drafted as a *fondsgebundene Rentenversicherung*.
  That the unit-linked variant is the one the association drafts first is itself the market's
  statement of where Riester insurance business went: the guarantee is carried by the design, not
  by the *Rechnungszins*. **No paragraph numbering, no clause text, no edition and no page count
  are established, and none may be invented downstream.**

### S2 — GDV, non-unit-linked ("klassische") Riester model conditions, "Stand: 21.07.2025"
- Publisher: GDV
- Doc type: *Musterbedingungen* for the **general-account** variant of the same AltZertG wrapper —
  the direct template for the product this model represents.
- URL: not established
- Retrieved: no — egress blocked; the **"Stand: 21.07.2025"** date line was returned to a sibling
  delib session's search of the GDV index [S3] and is recorded on that authority; no search
  corroboration in this session.
- Content: the existence of a **maintained 2025-vintage** classic Riester model wording is the
  single most useful thing the GDV corpus gives this file. It fixes two things. First, the classic
  Riester chassis was still being drafted by the industry association **after** the
  *Höchstrechnungszins* rose to 1,00 % on 1 January 2025 [R22] — i.e. the guarantee became
  financeable again at exactly the moment the model wording was refreshed. Second, it confirms that
  the classic and unit-linked Riester wrappers are **separate condition sets**, so a delib model of
  the classic form is modelling a real, separately drafted contract type and not a simplification.
  No clause content is established.

### S3 — GDV, "Musterbedingungen" service index
- Publisher: GDV
- Doc type: publisher index page listing the association's model-condition sets
- URL: https://www.gdv.de/gdv/service/musterbedingungen — **this URL was returned by a search in a
  sibling delib research session**, not by one run for this file
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the source of the German product taxonomy used in the scope note. The index establishes
  that separate model conditions exist for (a) *Rentenversicherung mit aufgeschobener
  Rentenzahlung* — the Schicht-3 deferred annuity; (b) *Rentenversicherung* under § 10 Abs. 1
  Nr. 2 Buchstabe b Doppelbuchstabe aa EStG — the **Basisrente**; (c) a **fondsgebundene
  Rentenversicherung nach dem Altersvorsorgeverträge-Zertifizierungsgesetz** — the Riester wrapper
  [S1]; (d) a **non-unit-linked variant of the same, "Stand: 21.07.2025"** [S2]; and (e) the
  *Hinterbliebenenrenten-Zusatzversicherung* rider. The taxonomy matters for this file in one
  specific way: **the association names the Riester product by its certification statute, not by
  its benefit** — the wrapper is defined by the AltZertG, and everything else about it is ordinary
  annuity machinery.

### S4 — Cosmos Lebensversicherungs-AG (CosmosDirekt), Riester-Rentenversicherung AVB, tariff **LA 1005 A**
- Publisher: Cosmos Lebensversicherungs-AG, the direct-writing arm of Generali Deutschland
- Doc type: *Allgemeine Bedingungen* (AVB) for a Riester annuity; tariff code **LA 1005 A**
- URL: not established
- Retrieved: no — egress blocked; the tariff code and its identification as the house's Riester
  wording were returned to a **sibling delib session's** search of the Cosmos AVB series and are
  recorded on that authority; no search corroboration in this session.
- Content: the only Riester wording in the corpus that is identified by its **tariff code**. Its
  siblings in the same series fix the house numbering — **LA 904 A** and **LA 1204 A / LA 1201 A
  (11.22)** for the Schicht-3 annuity, **LA 1100 A** and **LA 1079 / 936 / 1099 A** for the
  Basisrente, **LA 1311 A** for FlexInvest, **LA 1081 A** for the *Direktversicherung* — which
  places the Riester wording as a **separate tariff family**, not a rider on the Schicht-3 tariff.
  The sibling delib file establishes, for the **Schicht-3** wording of the same house, that the
  guaranteed *Rentenfaktor* is struck at inception on a recognised mortality table (DAV 2004 R) and
  a stated interest basis. **Whether LA 1005 A uses the same construction is not established** and
  must not be asserted; it is the natural expectation and it is a gap (gap 9). No vintage, no page
  count, no clause text.

### S5 — Allianz Lebensversicherungs-AG, the *RiesterRente* product family
- Publisher: Allianz Lebensversicherungs-AG, Stuttgart
- Doc type: insurer product pages plus the associated *Verbraucherinformation* / AVB packs for the
  Riester tariffs. The house has marketed the Riester contract under several names across vintages —
  a **klassisch** general-account form, a **fondsgebunden** form, and a form built on the
  *Sicherungsvermögen* with the house's own guarantee design. **The exact current product names,
  their tariff codes and which of them remain open to new business are not established** (gap 12).
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the market-leader comparator. One quantitative item is inherited from a **sibling delib
  session's** search: a third-party analysis of an Allianz specimen quotation reported, for the
  *BasisRente* and *RiesterRente* variants of the house's current savings concept, **total costs
  relative to the capital formed of at most 0,95 € per 100 €**, alongside an *Abschlussprovision*
  of **1 575 €** on that specimen. Both figures come from third-party commentary rather than an
  Allianz tariff sheet, both are `[unverified]` as market-representative levels, and the second is
  not for a Riester contract at all. They are the **only** charge figures anywhere in the delib
  Riester corpus, and they are not enough to found a charge basis — see gap 13.

### S6 — Debeka Lebensversicherungsverein a. G., Riester-Rentenversicherung
- Publisher: Debeka Lebensversicherungsverein a. G., Koblenz
- Doc type: AVB and product documentation for a Riester annuity
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: Debeka is the German market's largest writer of **classically guaranteed** life business
  and its membership is heavily weighted to *Beamte* (civil servants), who are *unmittelbar
  zulageberechtigt* under the § 10a route [R6] [R7] and are therefore the single most natural
  Riester constituency. A Debeka Riester wording is consequently the most likely place in the German
  market to find the **classic** chassis still being written. Recorded as a known reference on that
  reasoning alone: **no document, tariff code, vintage or clause is established**, and the sibling
  delib file records that this house **withdrew its classic Schicht-3 annuity from sale**, which
  says nothing either way about its Riester tariff.

### S7 — R+V Lebensversicherung AG, Riester-Rentenversicherung
- Publisher: R+V Lebensversicherung AG, Wiesbaden
- Doc type: AVB and product documentation for a Riester annuity
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the cooperative-sector comparator. R+V distributes through the *Volks- und
  Raiffeisenbanken*, the same network that distributes the cooperative fund house's Riester fund
  savings plan [S9] — so this is the one group in the corpus whose Riester offering spans an
  insurance and a fund chassis in the **same** distribution channel, which is why the two appear
  side by side in section 17. **No document, tariff code, vintage or clause is established.**

### S8 — Alte Leipziger Lebensversicherung a. G., Riester-Rentenversicherung
- Publisher: Alte Leipziger Lebensversicherung a. G., Oberursel
- Doc type: AVB and product documentation for a Riester annuity, in a classic and a unit-linked form
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the broker-market comparator; a house whose Riester tariffs are routinely present in
  broker comparison tables. **No document, tariff code, vintage or clause is established.** The
  product naming convention this house uses is `[unverified]` and is not reproduced here.

### S9 — Union Investment, *UniProfiRente* and *UniProfiRente Select*
- Publisher: Union Investment Privatfonds GmbH, Frankfurt am Main
- Doc type: *Vertragsbedingungen* plus the statutory *Produktinformationsblatt* [S14] for a
  **Riester-Fondssparplan**
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the cooperative sector's Riester fund savings plan and, historically, the largest single
  Riester fund product in Germany. Its guarantee mechanism is the reason it belongs in this file:
  a **rule-based reallocation between an equity fund and a bond fund** — the fund-industry answer
  to the same 100 % *Beitragsgarantie* an insurer meets with its *Deckungskapital*. When the
  guarantee's present value rises (falling rates, short remaining term), capital is moved out of the
  equity fund; when it falls, capital is moved back. The pathology this creates — a contract locked
  into the safe fund after a market fall and unable to participate in the recovery, the
  **cash-lock** — is the fund-chassis form of the same problem section 19 describes for the insurer.
  **The reallocation rule, the fund names, the fee levels and the current new-business status are
  not established** (gaps 11 and 12).

### S10 — DWS Investment GmbH, *DWS RiesterRente Premium* / *DWS TopRente*
- Publisher: DWS Investment GmbH (Deutsche Bank group), Frankfurt am Main
- Doc type: *Vertragsbedingungen* plus *Produktinformationsblatt* [S14] for a Riester-Fondssparplan
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the second of the three large Riester fund savings plans, on the same
  guarantee-by-reallocation principle as [S9]. Recorded for the same reason and with the same
  caveats. **No document, edition, fee level or new-business status is established.**

### S11 — Deka, *DekaBonusRente*
- Publisher: DekaBank Deutsche Girozentrale / Deka Investment GmbH, Frankfurt am Main
- Doc type: *Vertragsbedingungen* plus *Produktinformationsblatt* [S14] for a Riester-Fondssparplan
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the third of the three, distributed through the *Sparkassen*. Same chassis, same
  guarantee problem, same caveats.

### S12 — Riester-Banksparplan *Vertragsbedingungen* (Sparkassen; Volks- und Raiffeisenbanken)
- Publisher: individual *Sparkassen* and cooperative banks; there is no single national product
- Doc type: deposit-contract terms for a certified Riester savings plan, typically paying a
  reference-rate-linked interest with a bonus scale by duration
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the **structurally simplest** certified Riester product and the one for which the 100 %
  *Beitragsgarantie* costs nothing at all: a deposit balance can never fall below the sum of
  deposits, so the guarantee is satisfied by construction. That is exactly why the *Banksparplan*
  is the analytical control case in section 19 — it isolates the guarantee's cost as the **return
  forgone** rather than as a capital charge. Its historical drawback is the mirror image: a deposit
  rate that has, over most of the product's life, been at or near zero. **No individual product,
  rate scale, bonus scale or provider is established**, and the market is fragmented across
  hundreds of institutions.

### S13 — Wohn-Riester documents: Riester-*Bausparvertrag* and Riester-*Darlehen*
- Publisher: the *Bausparkassen* — Bausparkasse Schwäbisch Hall, LBS, Wüstenrot, BHW and others
- Doc type: *Allgemeine Bedingungen für Bausparverträge* (ABB) in a certified Riester form, and loan
  agreements certified as an *Altersvorsorgevertrag* in the form of a *Darlehen*
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the boundary of this file's scope. The AltZertG recognises an *Altersvorsorgevertrag* in
  the form of a **loan**, and the *Tilgungsleistungen* (capital repayments) on such a loan count as
  subsidised contributions in the same way a savings contribution does [R13] `[unverified]` at the
  paragraph level. Two products result: a Riester *Bausparvertrag* that saves toward, then lends
  for, an owner-occupied property, and a direct Riester *Darlehen* whose repayments draw the
  Zulagen. Both feed the *Wohnförderkonto* (section 16). **No document, edition, rate or fee is
  established.** They are named so that a reader knows the delib model's exclusion of Wohn-Riester
  is an exclusion of **real, certified, subsidy-drawing products**, not of a curiosity.

### S14 — *Produktinformationsblatt* under § 7 AltZertG, in the form prescribed by the *Altersvorsorge-Produktinformationsblattverordnung* (AltvPIBV)
- Publisher: every certified provider must issue one; the **form** is prescribed by statute and
  regulation, and the *Chancen-Risiko-Klasse* is assigned by the *Produktinformationsstelle
  Altersvorsorge* (PIA)
- Doc type: standardised two-page pre-contractual comparison sheet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: **the most important primary-document type for this product, and the reason a German
  Riester product is more transparently priced than a Schicht-3 one.** The sheet is standardised so
  that competing products are comparable line by line, and it carries, for a set of prescribed model
  cases: the product's **Chancen-Risiko-Klasse** on a 1-to-5 scale, the **Effektivkosten** (the
  reduction in yield expressed as an annual percentage), the *Kosten* broken into acquisition,
  administration and (where applicable) fund costs, and a projection of the benefit at
  *Rentenbeginn*. It is the document any real parameterisation of the delib model's charge basis
  would be read from. **No individual sheet was seen; no *Effektivkosten* figure, no CRK assignment
  and no model-case specification is established** (gap 13). `[unverified]` at the level of § 7
  AltZertG and the AltvPIBV as the governing instruments.

### S15 — *Zertifizierungsbescheid* and *Zertifizierungsnummer*
- Publisher: the certifying authority — the **Bundeszentralamt für Steuern** (BZSt), which took the
  function over from the BaFin `[unverified]` as to the date of transfer
- Doc type: the administrative decision certifying a contract type, whose number every certified
  product carries in its documentation
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: the artefact that makes a contract a Riester contract. Two properties of it matter
  downstream and both are structural rather than numeric. First, **certification attaches to the
  contract type, not to the individual policy** — a provider certifies a tariff and then sells it.
  Second, **certification is expressly not a quality judgement**: the authority confirms that the
  terms meet the § 1 AltZertG criteria and makes no statement about the provider's financial
  soundness, the product's cost, or its expected return [R2] `[unverified]` at paragraph level. A
  delib document must therefore never describe a Riester product as "state-approved" in any sense
  broader than that. **No individual certification number appears in this file and none may be
  invented.**

### S16 — The second tier of Riester insurance wordings
- Publishers: Stuttgarter Lebensversicherung a. G.; NÜRNBERGER Lebensversicherung AG; Continentale
  Lebensversicherung AG; HUK-COBURG-Lebensversicherung AG; Volkswohl Bund Lebensversicherung a. G.;
  LV 1871; Hannoversche; Barmenia; Gothaer; Signal Iduna; Provinzial; DEVK; Universa; ERGO; AXA;
  Swiss Life; Zurich Deutscher Herold; Baloise; Württembergische; HDI; Generali/Dialog
- Doc type: AVB, *Verbraucherinformationen* and *Produktinformationsblätter* for Riester annuities
- URL: not established
- Retrieved: no — egress blocked; no search corroboration in this session.
- Content: a single grouped known-reference entry, deliberately not split into per-carrier entries,
  because **nothing carrier-specific was established for any of them**. They are named because the
  brief asked for named insurers and because a downstream reader needs to know which houses' Riester
  documents a real research pass would go to. **Which of these houses ever wrote Riester business,
  which still do, and what their tariffs contain are all unestablished** (gap 12). No parameter in
  the delib `riester_rente` documents may cite [S16] for a **level**; it may be cited only for the
  proposition that a body of carrier wordings exists.

---

## Regulatory and actuarial references

Twenty-seven known references. The same retrieval statement applies to every one of them: **no
document was retrieved and no search was run for this file.** The statutory URLs given in canonical
`gesetze-im-internet.de` form are marked `[unverified]` — they are the form the host uses, not a
link anyone followed. The **content blocks state what the instrument provides, in this file's own
words, from general knowledge of German pension law**, with every paragraph number, date and figure
tagged. That is the honest description of their status and it is weaker than a citation.

Two structural points about the German arrangement, stated once so they need not be repeated. First,
**the Riester product is defined by two statutes that do different jobs**: the AltZertG says what a
contract must contain to be certifiable, and the EStG says who gets what subsidy and how the
benefits are taxed. A delib document that wants a *product* rule looks in the AltZertG; one that
wants a *money* rule looks in the EStG. Second, **there is no supervisory instrument that sets
Riester tariff levels**. The *Höchstrechnungszins* [R22] binds the guarantee's discount rate and
nothing else; charges, *Rentenfaktoren* and surplus are unregulated as to level and are disclosed
rather than capped [R4] [R5].

### R1 — AltZertG § 1, the criteria of a certifiable *Altersvorsorgevertrag*
- Publisher: Bundesministerium der Justiz / juris (Gesetze im Internet)
- URL: https://www.gesetze-im-internet.de/altzertg/__1.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration (session search budget exhausted).
- Content: the operative product statute. What it requires of the contract, as this file
  understands it, with every specific tagged:
  - **Payout may not begin before a statutory age.** The threshold is the completed **62nd** year of
    life for contracts concluded from **1 January 2012**, and the completed **60th** for contracts
    concluded before that date `[unverified]` on both the ages and the cut-off; the alternative
    trigger is the start of an old-age pension from a statutory scheme. The change was made by the
    *RV-Altersgrenzenanpassungsgesetz*, which lifted the statutory retirement age generally
    `[unverified]`.
  - **A *Beitragserhaltungszusage***: the provider must undertake that at the beginning of the
    payout phase **at least the sum of the *Altersvorsorgebeiträge* paid in — the saver's own
    contributions **and** the Zulagen credited — is available** for the benefit. This is the "100 %
    Beitragsgarantie". It is nominal, it is tested **only at *Rentenbeginn***, and it is the
    mechanical heart of the product (section 19).
  - **A lifelong benefit form.** Either a *lebenslange Leibrente* with **constant or rising**
    monthly payments, or an *Auszahlungsplan* with constant or rising instalments followed
    immediately by a **lifelong** *Teilkapitalverrentung* beginning at the latest from the
    **85th** year of life `[unverified]` on the age. A falling annuity is not certifiable; nor is a
    pure drawdown with no lifelong element.
  - **A *Teilkapitalauszahlung* of up to 30 %** of the capital available at the start of the payout
    phase may be taken as a lump sum without losing the subsidy `[unverified]` on the percentage.
    The remainder must be annuitised.
  - **Acquisition and distribution costs must be spread over at least five years** `[unverified]`
    on the period — the statutory cap on *Zillmerung* in this product, and a materially tighter
    constraint than anything the VVG imposes on a Schicht-3 contract.
  - **A *Wechselrecht***: the saver may terminate and have the accumulated capital transferred to
    another certified contract. The notice period is stated as a period to a quarter end
    `[unverified]`, and the transferring provider's charge for the transfer is capped at a fixed
    euro amount `[unverified]` — see gap 8.
  - **Information duties**: before conclusion, and annually thereafter on the use of contributions,
    the capital accumulated, the costs charged and the income earned.
  - **Unisex**: equal contributions for men and women, required for Riester contracts from
    **1 January 2006** — six years before the general unisex rule [R23] `[unverified]` on the date.
  - **Contributions used to insure reduced earning capacity or a survivor's benefit** may be
    included in the contract but are **limited to a share of total contributions** and are excluded
    from the *Beitragserhaltungszusage* `[unverified]` on the share. This is why a Riester contract
    can carry a *Berufsunfähigkeits-Zusatzversicherung* without the guarantee having to reproduce
    its premiums.
  - **The claim must not be assignable, pledgeable or realisable** — see [R16].

### R2 — AltZertG §§ 2, 3 and 5, certification and the certifying authority
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: certification is an administrative act confirming that a contract's **terms** satisfy the
  § 1 criteria [R1]. It is **not** a statement about the provider's financial standing, the
  product's charges, or its expected return, and the statute says so `[unverified]` at paragraph
  level. The certifying authority is the **Bundeszentralamt für Steuern**; the function previously
  sat with the **BaFin** and was transferred `[unverified]` as to the date. Certification can be
  withdrawn where a contract ceases to meet the criteria. **Consequence for delib**: no document may
  describe a Riester product as state-guaranteed or state-endorsed. The state guarantees nothing;
  the **provider** gives the *Beitragsgarantie*, and the provider's ability to honour it is a
  solvency question governed by the ordinary prudential regime.

### R3 — AltZertG § 1 Abs. 1a, the *Altersvorsorgevertrag* in the form of a *Darlehen*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: certification is available not only to savings contracts but to a **loan** used to
  acquire owner-occupied residential property, and to a *Bausparvertrag* combining the two
  `[unverified]` at paragraph level. This is the statutory hook for Wohn-Riester's lending side
  [S13] [R13] [R19]. Its relevance here is negative and definitional: it is why "Riester" in German
  usage covers a mortgage as well as an annuity, and why the delib model must say which of the four
  chassis it represents.

### R4 — AltZertG §§ 7 ff., the *Produktinformationsblatt*, *Effektivkosten* and *Chancen-Risiko-Klassen*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the disclosure regime, and the most distinctive feature of German subsidised-pension
  regulation. Every certified product must be offered with a **standardised**
  *Produktinformationsblatt* [S14] whose layout and content are prescribed so that products are
  comparable across chassis — an insurance annuity, a fund savings plan and a bank savings plan
  produce the *same sheet*. It carries the **Effektivkosten** (reduction in yield, an annual
  percentage) and a **Chancen-Risiko-Klasse** on a scale of **1 to 5** assigned by the
  **Produktinformationsstelle Altersvorsorge** (PIA), an institution established for the purpose,
  which computes the class from a common stochastic capital-market model rather than from the
  provider's own projection `[unverified]` on the scale, on the PIA's constitution and on the
  methodology. A 100 %-guaranteed product sits at the low-risk end of that scale by construction.
  **The regime was introduced by [R20]** `[unverified]`.

### R5 — *Altersvorsorge-Produktinformationsblattverordnung* (AltvPIBV)
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the regulation that prescribes the *form* of the sheet [S14] [R4] — the model cases, the
  contribution and term assumptions, the return scenarios and the presentation of the
  *Effektivkosten*. It is the document a delib charge basis would be calibrated against, because it
  fixes **what** the disclosed cost figure means. Nothing about its content is established here.

### R6 — EStG § 10a, the *Sonderausgabenabzug* and the *Günstigerprüfung*
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__10a.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration.
- Content: the second of the two subsidy routes. Contributions to a certified contract, **together
  with the Zulagen credited**, are deductible as *Sonderausgaben* up to **2 100 € per year**
  `[unverified]`. The ceiling was phased in — **525 €**, **1 050 €**, **1 575 €**, then **2 100 €**
  from the 2008 assessment year `[unverified]` — and has **not been raised since**, which is a
  substantive fact about the product's decline, not a detail: the ceiling has been nominal for
  roughly two decades. The *Günstigerprüfung* is performed **automatically by the tax office**: it
  computes the tax reduction the deduction would produce, compares it with the Zulagen entitlement,
  and grants the deduction only where it is the more favourable; where it is, the Zulagen are added
  back to the assessed tax so that the saver receives the **difference** and not both `[unverified]`
  on the mechanism's precise expression. The deduction is available only to those *unmittelbar*
  eligible [R7]; a *mittelbar* eligible spouse has no § 10a deduction of their own `[unverified]`.
  Civil servants and the other groups whose income data the pension insurance does not hold must
  consent to the transmission of their remuneration data for the entitlement to be determined
  `[unverified]`.

### R7 — EStG § 79, who is *zulageberechtigt*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the eligibility rule, and the one that decides whether a model point can hold this
  product at all.
  - ***Unmittelbar zulageberechtigt*** — those compulsorily insured in the **gesetzliche
    Rentenversicherung**; **Beamte**, judges, soldiers and equivalent office-holders whose old-age
    provision is a civil-service pension; those insured in the **Alterssicherung der Landwirte**;
    recipients of *Arbeitslosengeld*; persons credited with **Kindererziehungszeiten**; recipients
    of a full *Erwerbsminderungsrente* or *Dienstunfähigkeitsrente*; and **geringfügig
    Beschäftigte** who have waived the exemption from compulsory insurance `[unverified]` on the
    completeness and precise wording of the list.
  - ***Nicht* berechtigt** — the self-employed who are not compulsorily insured, and members of the
    **berufsständische Versorgungswerke** (doctors, lawyers, architects and the like). This is the
    single largest design criticism of the product and it is structural: the group with the weakest
    statutory pension is the group the subsidy does not reach `[unverified]` as a characterisation.
  - ***Mittelbar zulageberechtigt*** — the spouse or registered partner of an *unmittelbar*
    eligible person, where the couple are not permanently separated and both are resident in an
    EU/EEA state, **provided the *mittelbar* eligible person holds an own certified contract**. From
    the **2012** contribution year that person must also pay the **60 € *Sockelbeitrag*** in their
    own contract [R10] [R20] `[unverified]` on the year. Before that change, a *mittelbar* eligible
    spouse drew the full *Grundzulage* on a **zero** own contribution — the most generous provision
    the product ever contained, and the one most often described as its administrative low point.

### R8 — EStG § 82 and § 83, *Altersvorsorgebeiträge* and the *Altersvorsorgezulage*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: § 82 defines what counts as a subsidised contribution — payments into a certified
  contract, and, on the Wohn-Riester side, *Tilgungsleistungen* on a certified loan [R3] [R13]; it
  also brings **Riester-funded bAV contributions** (paid from **taxed** salary into a
  *Direktversicherung*, *Pensionskasse* or *Pensionsfonds*) into the subsidy `[unverified]` at
  paragraph level. § 83 establishes the *Altersvorsorgezulage* as the sum of *Grundzulage* and
  *Kinderzulage* [R9]. The point that matters for the model is definitional and load-bearing:
  **the Zulage is a contribution, not a benefit.** It is paid to the provider, credited to the
  contract, counted in the *Beitragsgarantie*, invested, and taxed at the end like any other
  contribution. It never reaches the saver's bank account.

### R9 — EStG § 84 (*Grundzulage*, *Berufseinsteiger-Bonus*) and § 85 (*Kinderzulage*)
- Publisher: Gesetze im Internet
- URLs: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the money. All figures `[unverified]`.
  - **Grundzulage: 175 € per year**, from the **2018** contribution year. Its history is
    **38 €** (2002–2003), **76 €** (2004–2005), **114 €** (2006–2007), **154 €** (2008–2017), then
    175 € — raised by [R21]. It has not moved since 2018.
  - **Berufseinsteiger-Bonus: a one-off 200 €** added to the *Grundzulage*, for an *unmittelbar*
    eligible saver who has **not completed the 25th year of life** at the start of the contribution
    year, granted **once**, in the first year for which a Zulage is claimed. Introduced for
    contribution years from **2008**.
  - **Kinderzulage: 185 € per year** per child for whom *Kindergeld* is drawn, for children born
    **before 1 January 2008**; **300 € per year** for children born **on or after 1 January 2008**.
    Its history mirrors the *Grundzulage* phase-in: 46 €, 92 €, 138 €, then 185 €. The two-tier
    split is permanent — it is a **birth-cohort** rule, not a transitional one, so a contract can
    carry both rates at once.
  - The *Kinderzulage* is credited to the **mother's** contract unless both parents jointly request
    otherwise `[unverified]`. It runs for as long as *Kindergeld* is drawn, and stops when
    *Kindergeld* stops — typically at 18, or later while the child is in education `[unverified]`.
    **This makes the Zulage stream a function of a household variable that the insurance contract
    itself does not observe**, which is the most awkward fact in the whole product for a
    per-policy projection model.

### R10 — EStG § 86 (*Mindesteigenbeitrag*, *Sockelbeitrag*) and § 87
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the condition on the money. To draw the **full** Zulagen the saver must pay an own
  contribution of at least the *Mindesteigenbeitrag*, defined `[unverified]` as
  **4 % of the previous calendar year's contribution-liable earnings, capped at 2 100 €, less the
  Zulagen entitlement**, subject to a floor — the *Sockelbeitrag* — of **60 € per year**. The
  percentage was phased in at **1 %** (2002–2003), **2 %** (2004–2005), **3 %** (2006–2007) and
  **4 %** from 2008 `[unverified]`. Where the saver pays **less** than the *Mindesteigenbeitrag*,
  the Zulagen are **reduced in the ratio of the contribution actually paid to the
  *Mindesteigenbeitrag***, rather than lost — a proportional, not a cliff-edge, sanction
  `[unverified]`. § 87 governs the case of a saver holding more than one certified contract: the
  Zulage is granted on a limited number of contracts and the saver must designate `[unverified]`.
  The reference income is the **previous** year's — so the Zulage year `t` entitlement depends on
  income in `t − 1`, a one-year lag the model must carry explicitly.

### R11 — EStG §§ 89 to 91, and the *Zentrale Zulagenstelle für Altersvermögen* (ZfA)
- Publisher: Gesetze im Internet; Deutsche Rentenversicherung Bund
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the administration, and the source of the model's **timing**. The saver applies for the
  Zulage **through the provider**, normally once by a *Dauerzulageantrag* that then runs
  automatically; the application deadline is the **end of the second calendar year following the
  contribution year** `[unverified]`. The **ZfA**, a unit of the Deutsche Rentenversicherung Bund,
  determines entitlement by matching the provider's contribution data against the pension
  insurance's earnings data and the *Kindergeld* data, then **pays the Zulage to the provider**,
  who credits it to the contract. Where entitlement later proves wrong, the ZfA **reclaims** and
  the provider debits the contract — so a Zulage credit is **provisional** until the data match
  settles. **Consequence for the model**: the Zulage for contribution year `t` is a cash inflow in
  a **later** period, conventionally `t + 1`, and it is subject to a small reversal risk. Neither
  the payment month nor the reversal frequency is established (gap 6).

### R12 — EStG § 22 Nr. 5, the taxation of the benefit
- Publisher: Gesetze im Internet
- URL: https://www.gesetze-im-internet.de/estg/__22.html `[unverified]`
- Retrieved: no — egress blocked; no search corroboration.
- Content: the *nachgelagerte Besteuerung* rule, and the sharpest difference between this product
  and the Schicht-3 annuity of `klassische_rentenversicherung`.
  - Benefits from an *Altersvorsorgevertrag* are **sonstige Einkünfte**. To the extent they derive
    from **subsidised** contributions — own contributions that attracted a Zulage or a § 10a
    deduction, plus the Zulagen themselves, plus all the investment return on both — they are
    taxable **in full** at the recipient's marginal rate. There is **no *Ertragsanteil*** on that
    part `[unverified]` at paragraph level.
  - To the extent they derive from **unsubsidised** contributions — money paid into the same
    contract above the § 10a ceiling, or after eligibility lapsed — the ordinary private-annuity
    rules apply: the *Ertragsanteil* for an annuity, or the § 20 Abs. 1 Nr. 6 rules for a lump sum
    `[unverified]`. A single Riester contract can therefore carry **two tax regimes at once**, and
    the provider must track the two contribution pools separately for the life of the contract.
  - The provider issues an annual ***Leistungsmitteilung*** to the recipient and to the tax
    administration, stating how much of the year's benefit falls in each pool `[unverified]`.
  - The *Werbungskosten-Pauschbetrag* for *sonstige Einkünfte* is **102 €** `[unverified]`.
  - **Consequence for delib**: the model publishes **gross** liability cash flows, so tax is
    context, not a cash flow. But the tax rule is what makes the *Teilkapitalauszahlung* and the
    *Kleinbetragsrenten-Abfindung* interesting [R15], and it is why a Riester annuity of a given
    gross amount is worth materially less to the saver than a Schicht-3 annuity of the same gross
    amount.

### R13 — EStG § 92a and § 92b, Wohn-Riester and the *Wohnförderkonto*
- Publisher: Gesetze im Internet
- URLs: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the housing route, out of the model's scope and described here so that the exclusion is
  informed. All figures `[unverified]`.
  - **§ 92a — *Altersvorsorge-Eigenheimbetrag***: the saver may withdraw capital from a certified
    contract, **without *schädliche Verwendung***, to acquire or build an owner-occupied dwelling,
    to repay a loan on one, to buy cooperative housing shares, or to fund a **barrier-reducing
    conversion**. Minimum and maximum amounts and a minimum share of the capital apply to the
    various uses, and the conversion use carries its own thresholds and a requirement that the works
    meet stated standards.
  - **§ 92a/§ 92b — the *Wohnförderkonto***: because the withdrawn money escapes the annuity, the
    subsidy attached to it must still be taxed. The amounts withdrawn, and the *Tilgungsleistungen*
    on a certified loan [R3], are recorded in a **notional account** that accrues at a statutory
    notional rate of **2 % per year** and is then taxed in the payout phase — either **spread
    annually** until the year the saver reaches **85**, or **in one sum with a 30 % discount** on
    the balance if the saver so elects.
  - **The *Wohnförderkonto* carries no cash whatsoever.** It is a tax memorandum. That is the reason
    Wohn-Riester is out of scope for a liability cash-flow model: there is no liability and no cash
    flow to project. What the model **can** represent, and what a delib document should say it does
    not, is the **withdrawal itself** — an *Eigenheimbetrag* is, from the insurer's side, an early
    and complete exit that terminates the annuity liability.

### R14 — EStG § 93, § 94 and § 95, *schädliche Verwendung* and its consequences
- Publisher: Gesetze im Internet
- URLs: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the sanction, and the reason a Riester surrender is not an ordinary surrender.
  - **§ 93 — *schädliche Verwendung***: any use of the capital outside the permitted purposes —
    paradigmatically **surrender for cash** — triggers repayment of **all Zulagen credited and all
    § 10a tax reductions granted**, the *Rückzahlungsbetrag*. The provider deducts it from the
    payment and remits it. **On top of that**, the accumulated **investment return** attributable
    to the subsidised part becomes taxable under § 22 Nr. 5 at the saver's marginal rate
    `[unverified]` at paragraph level. So the saver loses the subsidy **and** pays tax on the
    growth, which is why the German market speaks of a Riester contract as effectively
    unsurrenderable in economic terms.
  - **Not *schädlich***, and this list is what the model's option set is built from: transfer of the
    capital to another certified contract (*Anbieterwechsel*) [R1]; transfer to the spouse's
    certified contract under a *Versorgungsausgleich* on divorce; the *Eigenheimbetrag* [R13];
    payment of a *Kleinbetragsrente* as a lump sum [R15]; and, on death, transfer of the capital to
    a surviving spouse's own certified contract, subject to conditions `[unverified]`.
  - **Death without that transfer is *schädlich***: the capital passes to the estate net of the
    *Rückzahlungsbetrag*. A *Rentengarantiezeit* or a survivor's annuity running to the spouse is
    the *förderunschädlich* route.
  - **§ 95 — end of unlimited tax liability**: emigration historically triggered repayment. The rule
    was challenged as incompatible with the free movement of workers and was amended so that a move
    within the EU/EEA no longer has that effect `[unverified]` as to the judgment, the amending
    statute and the date. This is recorded as a **gap** (gap 15), not as a fact: the current rule
    was not established and must not be asserted downstream.

### R15 — EStG § 93 Abs. 3 with SGB IV § 18, the *Kleinbetragsrente*; EStG § 34, the *Fünftelregelung*
- Publisher: Gesetze im Internet
- URLs: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the small-annuity commutation, and the one place where German pension law lets a
  subsidised contract pay a lump sum outside the 30 % rule. All figures `[unverified]`.
  - **Threshold**: the provider may commute the annuity to a lump sum, without *schädliche
    Verwendung*, where the monthly annuity would not exceed **1 % of the monatliche Bezugsgröße**
    of § 18 SGB IV. The *Bezugsgröße* is reset annually; its monthly value has been in the
    **3 500 € to 3 800 €** region in the mid-2020s, putting the *Kleinbetragsrente* threshold near
    **35 € to 38 € per month**. **The precise value for any given year is not established** (gap 7),
    and a separate East/West value applied until the values were unified `[unverified]`.
  - **Taxation**: the *Abfindung* is taxable in full under § 22 Nr. 5 [R12], but since **2018** it
    is taxed under the **ermäßigte Besteuerung** of § 34 EStG — the *Fünftelregelung*, which
    computes the tax as five times the tax on one fifth of the amount, flattening the progression.
    Introduced by [R21].
  - **Deferral election**: also since 2018, the saver may elect to have the *Abfindung* paid at the
    **beginning of the following calendar year**, so that it falls into a year with lower other
    income `[unverified]`.
  - **Why it matters for the model**: a Riester contract with a small accumulated capital does not
    produce an annuity at all — it produces a lump sum at *Rentenbeginn*. Given that a substantial
    share of Riester contracts are *ruhend* with small balances (section 20), the
    *Kleinbetragsrente* is not an edge case; it is a **material second payout mode** and belongs in
    the model as a switch on the anchor decrement.

### R16 — EStG § 97, non-transferability and protection from execution
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the entitlement to the Zulage and the **subsidised** capital are **not transferable** and
  are protected from attachment `[unverified]` at paragraph level and as to the extent of the
  protection. The practical effects are two: the contract cannot be assigned as loan collateral,
  which removes a use that a Schicht-3 endowment has; and the subsidised capital is, within limits,
  protected in personal insolvency. Neither produces a cash flow, but both bear on lapse behaviour —
  a saver in financial difficulty cannot realise the contract as easily as a Schicht-3 one, and this
  is one of the reasons the German Riester book shows **Beitragsfreistellung** where another market
  would show surrender.

### R17 — *Altersvermögensgesetz* (AVmG) and *Altersvermögensergänzungsgesetz* (AVmEG), 2001
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the founding statutes, in force for contribution years from **2002** `[unverified]`. They
  did two things at once, and the pairing is the whole political logic of the product: they
  **reduced the future replacement rate of the statutory pension** and **created a subsidised
  private product to fill the gap**. The subsidy was phased in over four two-year steps to 2008
  [R9] [R10]. The product is named after the then federal labour minister; the name is colloquial
  and appears in no statute.

### R18 — *Alterseinkünftegesetz* (AltEinkG), 2004
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the statute that created the **three-layer** taxonomy German practice now uses —
  **Schicht 1** *Basisversorgung* (statutory pension, *Basisrente*), **Schicht 2**
  *Zusatzversorgung* (Riester, bAV), **Schicht 3** *Kapitalanlageprodukte* (unsubsidised private
  annuities and endowments) — and moved the statutory pension to *nachgelagerte Besteuerung* on a
  long transition `[unverified]` on the dates. Riester was already taxed that way from the start,
  which is why it is a Schicht-2 rather than a Schicht-3 product. The delib library uses this
  taxonomy in every product's scope note.

### R19 — *Eigenheimrentengesetz* (EigRentG), 2008
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the statute that created **Wohn-Riester** — the *Eigenheimbetrag*, the certifiable loan
  [R3] and the *Wohnförderkonto* [R13] `[unverified]` on the year. It also raised the *Kinderzulage*
  for children born from 2008 to 300 € [R9] `[unverified]`. Its effect on the shape of the Riester
  book is large and is the reason a contract count cannot be read as an annuity count: a material
  minority of all Riester contracts are housing contracts that will never pay an annuity
  (section 20).

### R20 — *Altersvorsorge-Verbesserungsgesetz* (AltvVerbG), 2013
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the administrative reform. It introduced the standardised *Produktinformationsblatt*
  [R4] [S14], capped the provider's charge for a *Wechsel* [R1], and required the **60 €
  *Sockelbeitrag* of a *mittelbar* eligible spouse** [R7] [R10] — closing the zero-contribution
  entitlement — with effect for contribution years from **2012** `[unverified]` on all four points
  and on the year.

### R21 — *Betriebsrentenstärkungsgesetz* (BRSG), 2017
- Publisher: Bundesgesetzblatt / Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the last substantive Riester reform. It raised the **Grundzulage from 154 € to 175 €**
  with effect from the **2018** contribution year [R9]; brought the *Kleinbetragsrenten-Abfindung*
  under the **Fünftelregelung** and added the **deferral election** [R15]; introduced a
  ***Freibetrag* in der Grundsicherung im Alter** so that a Riester annuity is no longer offset
  one-for-one against means-tested basic security — a base amount plus a percentage of the excess,
  subject to a cap `[unverified]` on all three figures; and removed the **double
  *Krankenversicherung* charge** on Riester annuities drawn from a **bAV** vehicle `[unverified]`.
  Every one of these was a repair to a criticism of the product rather than an extension of it, and
  none of them changed the *Beitragsgarantie*.

### R22 — *Deckungsrückstellungsverordnung* (DeckRV) § 2, the *Höchstrechnungszins*
- Publisher: Gesetze im Internet
- URL: not established
- Retrieved: no — egress blocked; no search corroboration; the two most recent values below are
  corroborated in the **sibling** delib research files from their own searches and are cited here on
  that authority.
- Content: the statutory maximum technical interest rate for new German life business. The two
  values that matter to this product are **0,25 %**, in force **from 1 January 2022**, and
  **1,00 %**, in force **from 1 January 2025** — the first increase in the series since 1994. The
  earlier sequence — 4 %, 3,25 %, 2,75 %, 2,25 %, 1,75 %, 1,25 %, 0,90 % — and every effective date
  in it is `[unverified]` here and belongs in the cross-product reference library rather than this
  file. **Why it is a Riester reference at all**: the *Beitragsgarantie* [R1] is a nominal guarantee
  at a fixed future date, and the rate at which an insurer may discount it is the rate that decides
  how much of each contribution must be immobilised to back it. The 0,25 % regime of 2022–2024 is
  the direct cause of the Riester new-business collapse (sections 19 and 20).

### R23 — Unisex pricing: the AltZertG rule and *Test-Achats*
- Publisher: Gesetze im Internet; Court of Justice of the European Union
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: Riester contracts have been required to be **unisex** — equal contributions for men and
  women — since **1 January 2006**, by the AltZertG itself [R1] `[unverified]`. The general German
  market followed only from **21 December 2012**, after the Court of Justice's judgment in the
  *Test-Achats* case (C-236/09, **1 March 2011**) `[unverified]` on the case number and date. **The
  ordering is the substantive point**: Riester was the German market's first unisex product, so
  Riester annuity tariffs were struck on a unisex basis from a vintage at which Schicht-3 tariffs
  were still sex-distinct, and a Riester *Rentenfaktor* is therefore **not** comparable with a
  contemporaneous Schicht-3 one for a male life.

### R24 — BMF *Anwendungsschreiben* on the tax treatment of subsidised private pensions
- Publisher: Bundesministerium der Finanzen
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the consolidated administrative guidance on §§ 10a and 79 to 99 EStG and on § 22 Nr. 5 —
  the document German practitioners actually work from, running to well over a hundred paragraphs
  and reissued periodically. It is the authoritative source for exactly the points this file has had
  to leave `[unverified]`: the treatment of a change of eligibility mid-year, the mechanics of the
  *Günstigerprüfung*, the two-pool tracking of subsidised and unsubsidised contributions, the
  *Rückzahlungsbetrag* calculation, and the *Wohnförderkonto* arithmetic. **Its date, reference
  number and content are not established** and none may be invented (gap 3).

### R25 — Riester contract statistics: BMAS quarterly series; GDV statistics
- Publisher: Bundesministerium für Arbeit und Soziales; Gesamtverband der Deutschen
  Versicherungswirtschaft
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the official count. The BMAS publishes a **quarterly** series of the number of
  Riester contracts split by chassis — *Versicherungsverträge*, *Investmentfondsverträge*,
  *Banksparpläne* and *Wohn-Riester-Verträge* — derived from the ZfA's own data [R11]; the GDV
  publishes the insurance subset with premium volumes. **These are the documents any market figure
  in the delib Riester documents must be checked against.** What this file says about levels in
  section 20 is `[unverified]` order-of-magnitude recollection, not a reading of either series, and
  the whole of section 20 is qualified accordingly (gap 2).

### R26 — *Fokusgruppe private Altersvorsorge* (2023) and the pAV-Reform / *Altersvorsorgedepot* debate
- Publisher: Bundesministerium der Finanzen (the working group); the federal government (the bill)
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the reform track, described in section 21. The *Fokusgruppe*, convened by the finance
  ministry with the labour, justice and economics ministries and reporting in **2023**
  `[unverified]`, recommended reforming rather than replacing the subsidised private layer:
  **relaxing or removing the 100 % *Beitragsgarantie***, admitting a **securities-account product**
  without an insurance wrapper, simplifying the Zulage into a proportional match, and widening
  eligibility. A draft bill followed in **2024** creating an ***Altersvorsorgedepot*** alongside
  guaranteed products, with a proportional *Grundzulage* per euro contributed, a proportional
  *Kinderzulage*, a retained *Berufseinsteiger-Bonus* and a supplement for low earners
  `[unverified]` on every element. **The bill did not become law in that parliamentary term**
  `[unverified]`. **The position as at the 2026-08-29 access date is not established** and is
  recorded as gap 1 — the single most important thing this file could not determine.

### R27 — Consumer, comparison and rating cluster
- Publishers: Stiftung Warentest / *Finanztest*; Finanztip; the *Verbraucherzentralen*; Verivox;
  Check24; Handelsblatt; Morgen & Morgen; Franke und Bornberg; Assekurata
- URL: not established
- Retrieved: no — egress blocked; no search corroboration.
- Content: the secondary layer that, in a normal research pass, supplies the price points and the
  observed spread across carriers that a representative composite is built from — *Effektivkosten*
  comparisons, *Rentenfaktor* tables, guarantee-design ratings and the running commentary on
  providers leaving the market. **Nothing from any of them is established in this file.** They are
  named so that the gaps register can say precisely what a follow-up pass should read, and so that
  no delib document mistakes their absence for their non-existence. Anything they would have
  supplied is `[std]` downstream.

---

## Extracted facts, by mechanic

This is the section the `product-spec.md` and `technical-notes.md` are written from. It is long
because it is the part of a research file that does not depend on having a PDF open: the mechanics
of the German subsidy are statutory, stable and well documented in the profession's general
knowledge, and they can be stated precisely even where a level cannot. **Every level that could not
be established appears here as a `[std]` parameter with a rationale, never as a citation.**

### 1. Product structure, legal form and the Schicht-2 placing

- A Riester contract is an ordinary **private law contract** — an insurance contract, a fund savings
  contract, a deposit contract or a loan — that has additionally been **certified** under the
  AltZertG [R1] [R2]. Certification does not change the contract's legal nature. An insurance
  Riester contract is a *Lebensversicherungsvertrag* governed by the VVG, and every VVG mechanic
  that applies to a Schicht-3 annuity applies here too, **subject to** the AltZertG's overrides.
- The three overrides that matter, and they are the whole product:
  1. **Money comes in from the state** [R8] [R9], as a contribution rather than a benefit.
  2. **A guarantee is compulsory** [R1] — the provider may not write the contract without it.
  3. **The exit is closed** [R14] — surrender is permitted by contract law but is punished by tax
     law severely enough to make it economically irrational in most cases.
- **Schicht 2** in the *Alterseinkünftegesetz* taxonomy [R18]: subsidised supplementary provision,
  relieved on the way in and taxed in full on the way out, alongside the *betriebliche
  Altersversorgung*. Schicht 1 (*Basisrente*) is relieved more generously and is completely
  illiquid; Schicht 3 is unrelieved and liquid. Riester sits between the two on both axes and is,
  in the German market's own description, the layer designed for the employed household of modest
  income with children.
- **The subsidy is the product.** Stripped of the Zulagen and the § 10a deduction, a Riester annuity
  is a worse Schicht-3 annuity: same chassis, more constraints, full taxation instead of the
  *Ertragsanteil*. Every economic argument for the product runs through the subsidy, and every
  criticism of it runs through the cost of the constraints the subsidy buys.
- No delib document may call the product "state-guaranteed". The state pays a subsidy and certifies
  the terms; the guarantee is the provider's own [R2].

### 2. Eligibility: who can hold this contract

- ***Unmittelbar zulageberechtigt*** — the eligibility that the saver holds in their own right
  [R7]: compulsory members of the statutory pension insurance (the great majority of employees);
  *Beamte*, judges, soldiers and equivalent office-holders, on consenting to the transmission of
  their remuneration data; farmers in the *Alterssicherung der Landwirte*; recipients of
  *Arbeitslosengeld*; parents credited with *Kindererziehungszeiten*, for up to three years per
  child `[unverified]`; recipients of a full *Erwerbsminderungs-* or *Dienstunfähigkeitsrente*; and
  *geringfügig Beschäftigte* who have waived the exemption from compulsory insurance.
- ***Mittelbar zulageberechtigt*** — derived from a spouse or registered partner who is
  *unmittelbar* eligible, provided the couple are not permanently separated, both are EU/EEA
  resident, and **the derived person holds an own certified contract and pays at least the 60 €
  *Sockelbeitrag*** [R7] [R10] [R20].
- **Not eligible**: the self-employed who are not compulsorily insured, and members of the
  *berufsständische Versorgungswerke* [R7]. Those groups are directed to the *Basisrente* instead —
  which is exactly why delib carries `basisrente` as a separate product.
- **Eligibility is annual and can change.** A saver can be *unmittelbar* eligible in one year,
  *mittelbar* in the next and not eligible at all in a third, without the contract changing. Nothing
  happens to the contract when eligibility lapses: contributions may continue, but they are
  **unsubsidised** [R12] and go into the second tax pool (section 6).
- **Consequence for the model.** Eligibility is a **model-point attribute of the saver, not of the
  policy**, and it drives the entire Zulage stream. The reference implementation carries it as a
  per-period flag with a `[std]` default of "*unmittelbar* eligible throughout", because the model
  is a mechanics demonstration and a stochastic eligibility path would obscure the mechanic it is
  demonstrating. A second model point exercising a mid-term lapse of eligibility is the honest way
  to show that the mechanic exists.

### 3. The Zulagen: amounts, entitlement and the cohort rule

All amounts `[unverified]` — no search corroborated any of them; they are stated from general
knowledge of §§ 84 and 85 EStG [R9] and are the figures a downstream document must check.

| Component | Amount per year | From | Condition |
|---|---|---|---|
| *Grundzulage* | **175 €** | contribution year 2018 | one per eligible saver, own contract |
| *Grundzulage*, previous level | 154 € | 2008–2017 | raised by [R21] |
| *Grundzulage*, phase-in | 38 € / 76 € / 114 € | 2002–03 / 2004–05 / 2006–07 | [R17] |
| *Berufseinsteiger-Bonus* | **200 €**, **once** | contribution year 2008 | *unmittelbar* eligible, under 25 at the start of the contribution year |
| *Kinderzulage*, child born **before** 1 Jan 2008 | **185 €** | 2008 | per child, while *Kindergeld* is drawn |
| *Kinderzulage*, child born **from** 1 Jan 2008 | **300 €** | 2008 | per child, while *Kindergeld* is drawn |
| *Kinderzulage*, phase-in | 46 € / 92 € / 138 € | 2002–03 / 2004–05 / 2006–07 | [R17] |

- **The two *Kinderzulage* rates are a permanent birth-cohort split, not a transition** [R9] [R19].
  A household with a child born in 2006 and one born in 2009 draws 185 € and 300 € simultaneously.
  A model that treats the *Kinderzulage* as a single rate will misprice every family model point
  spanning the 2008 boundary, and that is a listed pitfall for the technical notes.
- **The *Kinderzulage* is credited to the mother's contract** unless the parents jointly elect
  otherwise `[unverified]` [R9]. In a one-contract household model this is a labelling question; in
  a two-contract household it decides which contract's *Mindesteigenbeitrag* the Zulagen offset,
  and therefore which contract needs how much own money.
- **The *Kinderzulage* stops when *Kindergeld* stops** — normally at the child's 18th birthday,
  later during education `[unverified]`. So the Zulage stream on a family contract is a **step
  function that falls**, typically twice or three times, during a contract that runs thirty or forty
  years. The reference implementation carries a *Kinderzulage* schedule as an external CSV column
  per model point rather than as a scalar, for exactly this reason.
- **The *Berufseinsteiger-Bonus* is once in a lifetime, not once per contract** `[unverified]`. A
  saver who takes a second contract does not get a second bonus. In a per-policy model it is a
  first-period addition to the Zulage on the anchor model point and is switched off elsewhere.
- **The Zulage is paid to the provider and credited to the contract** [R8] [R11]. It is not paid to
  the saver, it is not a tax refund, and it does not appear in the saver's bank statement. In the
  model it is a **premium-equivalent inflow with a different payer**.

### 4. The *Mindesteigenbeitrag*, the *Sockelbeitrag*, and what they do to the contribution

The rule [R10], with the derivation set out because it is the arithmetic the model's premium cells
implement:

> *Mindesteigenbeitrag* = **min( 4 % × income of the previous calendar year , 2 100 € ) − Zulagen**,
> floored at the *Sockelbeitrag* of **60 €**.

Inputs `[unverified]` [R10]: the 4 %, the 2 100 € cap and the 60 € floor. Everything derived below
is `[std] derived` — exact arithmetic on those inputs, shown so a reader can redo it.

**The total contribution** into the contract is then `Eigenbeitrag + Zulagen`, and where the saver
pays exactly the *Mindesteigenbeitrag* that total equals **min(4 % × income, 2 100 €)** — the
Zulagen are a **substitute** for the saver's own money, not an addition to it. This is the single
most misunderstood feature of the product and it must be said explicitly in the product spec: at the
*Mindesteigenbeitrag*, **raising the Zulage does not raise the amount invested; it lowers the amount
the saver pays.**

**Worked cases** — all `[std] derived` on the [R10] and [R9] inputs, 2018-and-later rates:

| Case | Prior-year income | Zulagen | 4 % of income | *Mindesteigenbeitrag* | *Eigenbeitrag* paid | Total into contract | Zulage share |
|---|---|---|---|---|---|---|---|
| A — single, no children | 40 000 € | 175 € | 1 600,00 € | 1 425,00 € | 1 425,00 € | 1 600,00 € | 10,94 % |
| B — single, at the cap | 60 000 € | 175 € | 2 400,00 € → capped 2 100,00 € | 1 925,00 € | 1 925,00 € | 2 100,00 € | 8,33 % |
| C — one child born 2010 | 30 000 € | 475 € | 1 200,00 € | 725,00 € | 725,00 € | 1 200,00 € | 39,58 % |
| D — two children born from 2008 | 20 000 € | 775 € | 800,00 € | 25,00 € → floor **60,00 €** | 60,00 € | 835,00 € | 92,81 % |
| E — *mittelbar* eligible spouse | n/a | 175 € | n/a | **60,00 €** | 60,00 € | 235,00 € | 74,47 % |

- **Case D is the product's political case and its actuarial oddity at once.** A household paying
  **60 €** of its own money draws **775 €** of Zulagen — a multiple of **12,92×** `[std] derived` —
  and the contract receives 835 € a year. No other German savings product has anything like that
  leverage, and it is the reason the product's defenders describe it as working exactly as intended
  for its target group.
- **The income at which the *Sockelbeitrag* stops binding** is `(60 € + Zulagen) / 4 %`
  `[std] derived`: **5 875 €** for a childless single, **10 500 €** with one pre-2008 child,
  **13 375 €** with one post-2008 child, and **20 875 €** with two post-2008 children. Below those
  incomes the contribution is a flat 60 € plus the Zulagen and does not vary with income at all.
- **The income at which the 2 100 € cap binds** is `2 100 € / 4 % = 52 500 €` `[std] derived`.
  Above it the total contribution is frozen at 2 100 € regardless of earnings, which is why the
  product's subsidy value falls monotonically with income once the cap is reached.
- **Under-payment is proportional, not fatal** [R10]: pay half the *Mindesteigenbeitrag* and receive
  half the Zulagen. A model that treats the *Mindesteigenbeitrag* as a cliff will misstate every
  path in which the saver reduces contributions, and the German book is full of those paths
  (section 21).
- **The reference income is the previous calendar year's** [R10]. The Zulage entitlement for
  contribution year `t` is a function of income in `t − 1`, and the Zulage cash itself lands in
  `t + 1` [R11]. The model therefore carries **two distinct lags** in the subsidy chain and they are
  a listed pitfall.

### 5. The *Sonderausgabenabzug* and the *Günstigerprüfung*

- Contributions **plus the Zulagen** are deductible under § 10a EStG up to **2 100 € per year**
  `[unverified]` [R6]. The ceiling covers the two together, so a saver at the maximum contributes
  2 100 € of which the state has supplied the Zulagen.
- The **Günstigerprüfung** is automatic [R6]: the tax office computes the tax reduction the deduction
  would give, compares it against the Zulagen entitlement, and applies the deduction only if it is
  better. Where it is, the Zulagen are added back to the assessed tax so that the saver ends up with
  the **larger** of the two benefits and not their sum `[unverified]` on the mechanism.
- **Who gains from which route.** The Zulagen route dominates for low incomes and for households with
  children, because a fixed euro subsidy is worth more than a percentage deduction when the marginal
  rate is low and the Zulagen are large. The § 10a route dominates for high incomes with no children.
  The crossover is a function of marginal rate and family composition and is **not** established
  numerically here — see gap 5.
- **The 2 100 € ceiling has not been raised since 2008** `[unverified]` [R6]. Over the same period the
  contribution ceiling of the statutory pension insurance and the *Basisrente* deduction have both
  risen substantially. That divergence is a fact about the product's decline and belongs in the
  product spec's market-role section.
- **A *mittelbar* eligible spouse has no § 10a deduction of their own** `[unverified]` [R6] [R7];
  their subsidy is the Zulage alone.
- **Consequence for the model: none directly.** The delib model publishes gross liability cash flows
  and does not compute the saver's tax. The *Sonderausgabenabzug* matters to the model in exactly one
  indirect way — it is part of what is repaid on *schädliche Verwendung* [R14], and therefore part of
  the reason the modelled lapse rate for a Riester contract should be materially **below** a
  Schicht-3 one.

### 6. Contribution structure, and the two contribution pools

- **Contributions are flexible in a way a Schicht-3 tariff usually is not.** The AltZertG does not
  require a level premium; what it requires is that the guarantee cover whatever was paid [R1]. In
  practice German Riester insurance tariffs are written with a nominal level annual or monthly
  contribution and a wide right to vary it, because the *Mindesteigenbeitrag* itself moves every year
  with income and family status [R10].
- **Three contribution movements are routine and all three must be representable**: an increase to
  restore the *Mindesteigenbeitrag* after a pay rise; a reduction to the *Sockelbeitrag*; and a
  complete stop (*Beitragsfreistellung*), which leaves the contract in force and the guarantee
  standing on what has been paid (section 14).
- **The two pools.** A single Riester contract can hold **subsidised** and **unsubsidised**
  contributions at once [R12]:
  - *geförderte Beiträge* — own contributions up to the § 10a ceiling that attracted a Zulage or a
    deduction, plus the Zulagen. Taxed **in full** on the way out.
  - *ungeförderte Beiträge* — anything paid above the ceiling, or paid in a year in which the saver
    was not eligible. Taxed on the *Ertragsanteil* (annuity) or under the § 20 rules (lump sum).
  The provider must track the two pools and their investment return separately for the whole life of
  the contract, and must apportion every benefit between them in the annual *Leistungsmitteilung*
  [R12] `[unverified]`.
- **Both pools count for the *Beitragsgarantie***. The guarantee is on the *Altersvorsorgebeiträge*
  paid in — it does not distinguish subsidised from unsubsidised money `[unverified]` [R1]. This is
  worth stating because it is the natural place for an implementer to go wrong.
- **Reference implementation.** The delib model carries a **single pool** and states that it does so:
  the anchor model point contributes at or below the ceiling throughout, so the two pools coincide.
  A second model point with contributions above the ceiling exists to prove the split is
  representable, and the technical notes list "collapsing the two pools" as a pitfall. This is a
  `[std]` simplification with a stated rationale, not an omission.

### 7. The AltZertG criteria, read as product constraints

The § 1 criteria [R1] are the product's specification. Read as constraints on a cash-flow model,
they are these, with every specific `[unverified]`:

| Criterion | Constraint on the model |
|---|---|
| Payout not before age **62** (contracts from 2012; **60** before) | `Rentenbeginn` is bounded below; a model point with an earlier annuity start is not a Riester contract |
| **Beitragserhaltungszusage** — contributions **and** Zulagen available at *Rentenbeginn* | a floor on the conversion capital: `max(Deckungskapital + Überschuss, Σ contributions + Σ Zulagen)` |
| Benefit must be a **lifelong** annuity, **constant or rising** | no decreasing annuity, no fixed-term-only payout; a *Rentengarantiezeit* is permitted because it does not make the annuity fall |
| Or an **Auszahlungsplan** with **Restverrentung** from age **85** | a second payout topology, used by the fund and bank chassis, not by the insurance one |
| **Teilkapitalauszahlung ≤ 30 %** at *Rentenbeginn* | a single lump-sum election at one date, sized as a fraction of the conversion capital |
| Acquisition costs spread over **≥ 5 years** | the charge basis cannot front-load the whole acquisition cost into year 1 |
| **Wechselrecht** with capital transfer | a termination that pays out the **full** accumulated capital to another provider, with no subsidy consequence |
| **Unisex** contributions | one mortality basis; no sex as a rating factor and none in the *Rentenfaktor* |
| Risk-cover contributions capped and excluded from the guarantee | a *Berufsunfähigkeits-Zusatzversicherung* premium does not enlarge the guarantee |
| Annual information duty | no cash-flow effect; a per-policy expense |

- **Two of these are much stronger than anything in the Schicht-3 product.** The five-year cost
  spreading is a statutory cap on *Zillmerung* aimed at this product specifically, and the
  *Wechselrecht* is a portability right with no Schicht-3 analogue. Both are constraints on the
  provider's economics rather than on the policyholder's, and both push a Riester tariff toward
  lower front-end charges and a thinner acquisition margin than a comparable Schicht-3 tariff
  `[unverified]` as a market characterisation.
- **The 30 % *Teilkapitalauszahlung* is an election, not an entitlement to a design.** The contract
  must permit it; the saver need not take it. In the model it is a switch on the anchor decrement,
  and its default should be **taken**, because German market commentary consistently reports it as
  the usual choice `[unverified]` — see gap 10, which is where that claim's lack of support is
  recorded.

### 8. The *Beitragsgarantie*

- **What is guaranteed**: that at the beginning of the payout phase, the capital available for the
  benefit is **at least the sum of the *Altersvorsorgebeiträge* paid in** — the saver's own
  contributions **plus** the Zulagen credited [R1].
- **What is not guaranteed, and each of these is load-bearing:**
  - **Not the value at any other date.** The guarantee is tested **once**, at *Rentenbeginn*. Before
    that date the contract's surrender value can be, and in the early years of a charged contract
    usually is, **below** the contributions paid.
  - **Not on surrender.** A saver who terminates for cash gets the *Rückkaufswert*, which the
    guarantee does not floor, **and** loses the subsidy [R14].
  - **Not on transfer.** A saver exercising the *Wechselrecht* transfers the capital as it stands.
    Whether the guarantee is preserved, restarted or lost on transfer is a design question of the
    receiving contract and is **not established** — gap 8.
  - **Not in real terms.** It is a **nominal** guarantee. Over a thirty-year contract at even
    moderate inflation the guaranteed floor is worth a fraction of the contributions in real terms,
    which is the substance of the most serious criticism of the product's design.
  - **Not the annuity.** The guarantee is on the **capital** at *Rentenbeginn*. What that capital
    buys is a separate guarantee — the *garantierter Rentenfaktor* (section 10) — and the two are
    frequently conflated in consumer material.
  - **Not the risk-cover premiums.** Contributions applied to a *Berufsunfähigkeits-* or
    survivor's-benefit rider are excluded, within a statutory share `[unverified]` [R1].
- **Why it is compulsory.** Certification is unavailable without it [R1] [R2], and without
  certification there is no subsidy. So the guarantee is not a competitive feature a provider may
  drop; it is the entry ticket. That is the fact that makes the *Höchstrechnungszins* [R22] a
  Riester-market variable rather than a pricing detail, and it is the whole content of section 19.
- **How an insurer meets it.** In the classic chassis, by holding the *Deckungskapital* in the
  general account and accumulating it at the guaranteed *Rechnungszins*; the guarantee then binds
  only if the cumulative charges exceed the cumulative guaranteed interest, which at a low
  *Rechnungszins* they easily do (section 19). In the unit-linked chassis, by a dynamic split
  between a guarantee asset and a risk asset (section 18). In the bank chassis, trivially [S12].
- **Modelling it.** The guarantee is a **running accumulator** on contributions and Zulagen, not a
  discounted quantity: `G(t) = G(t−1) + Eigenbeitrag(t) + Zulage(t)`, with `G(0) = 0`. The
  conversion capital at `Rentenbeginn` is `max(AV(T), G(T))`, and the excess of `G(T)` over `AV(T)`
  — the *Garantielücke* — is a **cost the insurer bears out of its own funds** in that scenario. A
  model that never exhibits a positive *Garantielücke* on any model point has not demonstrated the
  product's defining mechanic, and the delib model point set must contain at least one point on
  which it bites.

### 9. The accumulation phase

- The classic Riester chassis is the Schicht-3 chassis: the contribution less charges and less any
  risk premium is the *Sparbeitrag*, which is credited to the *Deckungskapital* and accumulates at
  the guaranteed *Rechnungszins*; declared *Überschussbeteiligung* is credited on top, in one of the
  standard German surplus systems. The full recursion, the four surplus components
  (*Zinsüberschuss*, *Risikoüberschuss*, *Kostenüberschuss*, *Schlussüberschussanteil*) and the
  *Bewertungsreserven* participation of § 153 Abs. 3 VVG are documented in
  `_research/klassische_rentenversicherung.md` and are **not restated here**; they are unchanged by
  the AltZertG.
- **What the AltZertG changes in the accumulation phase is three things and no more:**
  1. **The Zulage arrives as an extra contribution**, in a later period than the contribution year
     it belongs to [R11], and is charged like any other contribution unless the tariff says
     otherwise. **Whether German Riester tariffs levy acquisition charges on the Zulagen as well as
     on the *Eigenbeitrag* is not established** and is gap 14 — it is a material charge-base
     question, because the Zulagen can be the majority of the contribution in the low-income cases
     of section 4.
  2. **The guarantee accumulator runs alongside the account value** (section 8).
  3. **Acquisition costs must be spread over at least five years** [R1], which changes the *shape*
     of the early-duration charge run-off relative to a Schicht-3 tariff.
- **Surplus in the Riester chassis is doing double duty.** In a Schicht-3 contract surplus is upside.
  Here, at a low *Rechnungszins*, surplus is the **first line of defence for the guarantee**: it is
  what closes the *Garantielücke* before the insurer's own funds have to. That inverts the usual
  reading of a surplus assumption — a low surplus assumption does not merely reduce the projected
  benefit, it increases the projected guarantee cost. The technical notes must carry this as a
  sensitivity, and it is a listed pitfall.
- **All levels are `[std]`.** No *Rechnungszins* vintage, no *Überschuss* declaration, no charge and
  no *Rentenfaktor* was established for any Riester tariff at any carrier (gaps 12, 13, 14).

### 10. *Rentenbeginn*: conversion, *Teilkapitalauszahlung* and the *Rentenfaktor*

- **The date.** Contractually fixed at inception, bounded below by the statutory age [R1] — **62**
  for contracts concluded from 2012, **60** before `[unverified]`. German practice sets it at or near
  the saver's statutory retirement age. Deferral is normally possible; **whether a statutory upper
  bound applies to the start of the payout phase itself, as distinct from the age-85 bound on the
  *Restverrentung*, was not established** — gap 10.
- **The conversion capital** is `max(Deckungskapital + Überschussguthaben + Schlussüberschuss +
  Bewertungsreserven-Anteil, Σ Eigenbeiträge + Σ Zulagen)` — the guarantee floor of section 8
  applied to the sum of the account's own parts. Which of the surplus components count toward
  satisfying the guarantee, and in particular whether a *Schlussüberschussanteil* may be used to
  close the *Garantielücke*, is a tariff-design question that **was not established** (gap 9); the
  reference implementation counts all of them and says so as a `[std]` convention.
- **The *Teilkapitalauszahlung***: up to **30 %** of the conversion capital may be taken as a lump
  sum at *Rentenbeginn* without *schädliche Verwendung* `[unverified]` [R1]. It is taxed in full
  under § 22 Nr. 5 in the year it is paid [R12] — with **no** *Fünftelregelung*, which is available
  only for the *Kleinbetragsrenten-Abfindung* [R15] `[unverified]`. That asymmetry is worth stating:
  a 30 % lump sum on a large contract is taxed at the top of the saver's rate in one year, and the
  German consumer literature accordingly treats the decision as non-obvious.
- **The remaining 70 % must be annuitised** into a lifelong, constant-or-rising monthly *Leibrente*
  [R1].
- **The *Rentenfaktor*.** The conversion runs at the *garantierter Rentenfaktor* struck at inception,
  compared at *Rentenbeginn* with the carrier's then-current factor, the **higher** of the two
  applying. That two-factor construction is documented for the German market in
  `_research/klassische_rentenversicherung.md` from a sibling session's searches; **it was not
  established for any Riester tariff** and is carried here as the expected construction, `[std]` in
  the reference implementation with that rationale (gap 9).
- **The Riester *Rentenfaktor* is unisex from a 2006 vintage** [R23] — earlier than the Schicht-3
  market — so a Riester factor and a same-vintage Schicht-3 factor for a male life are **not**
  comparable. No level, at any carrier, for any year, was established; every *Rentenfaktor* in the
  delib Riester documents is `[std]`, anchored so the worked example reproduces exactly.
- **The mortality basis** for the annuity is the German annuitant table family — DAV 2004 R,
  generational, in its unisex application. The tables are the property of the Deutsche
  Aktuarvereinigung, are not public and are **not redistributed** in this library; the delib CSV is a
  `[std]` proxy anchored to the worked example, and the model documentation says what a replacement
  must preserve.

### 11. The payout phase

- **A lifelong monthly annuity**, constant or rising [R1]. The German market pays it monthly in
  advance `[unverified]`.
- **Surplus continues in payment.** The payout-phase surplus systems of the German market — a
  *Gewinnrente* added to the guaranteed annuity, a *Bonusrente*, or a *flexible*/*dynamische*
  *Überschussrente* that can fall — are the same as for a Schicht-3 annuity and are documented in
  the sibling file. **The AltZertG's "constant or rising" requirement constrains which of them may be
  used on a Riester contract**: a surplus system whose declared component can be reduced would make
  the total annuity fall, so the certifiable forms are those in which the guaranteed floor never
  decreases `[unverified]` as a legal reading. This is a genuine product difference from Schicht 3
  and the product spec should state it.
- **A *Rentengarantiezeit*** — a guaranteed minimum payment period — is permitted and is common.
  Because it does not make the annuity fall, it is compatible with the AltZertG constraint; and
  because payments in the guarantee period run to the beneficiaries rather than the estate, it is
  the *förderunschädliche* route for a death shortly after *Rentenbeginn* [R14] (section 13).
- **The payout-phase administration charge** is normally a percentage of each annuity payment. No
  level was established; `[std]`.
- **The *Auszahlungsplan mit Restverrentung*** is the alternative topology [R1]: level or rising
  scheduled withdrawals, then a lifelong annuity bought with the remaining capital, beginning at the
  latest from the **85th** year of life `[unverified]`. It is the fund and bank chassis's payout form
  [S9]–[S12], not the insurance one, and the delib model does not implement it. It is described here
  because it is the reason a Riester fund savings plan still ends in an insurance annuity: **the
  insurance industry receives the *Restverrentung* capital of the fund industry's contracts**, which
  is a real, if indirect, source of immediate-annuity business.

### 12. *Kleinbetragsrente* and the *Abfindung*

- **Trigger** [R15]: the monthly annuity that the conversion capital would buy does not exceed
  **1 % of the monatliche Bezugsgröße** of § 18 SGB IV — a threshold in the region of **35 € to
  38 € per month** in the mid-2020s `[unverified]`, reset annually and **not** established for any
  specific year (gap 7).
- **Effect**: the provider may pay the whole capital as a lump sum. This is **not** *schädliche
  Verwendung*; the subsidy is not repaid [R15].
- **Taxation**: full taxation under § 22 Nr. 5 [R12], but with the **Fünftelregelung** of § 34 EStG
  since 2018 [R21], and with an election to have the payment made at the **beginning of the
  following calendar year** `[unverified]`.
- **It is the provider's option, not the saver's** `[unverified]` — the statute permits the payment,
  and the contract terms decide whether the provider must, may, or will on request. **This was not
  established** and is gap 7.
- **Why it matters more here than the threshold suggests.** The Riester book contains a large tail of
  small contracts: contracts taken to draw the Zulagen at the *Sockelbeitrag* (case D and case E of
  section 4), and contracts that went *ruhend* early (section 21). On a 60 €-plus-Zulagen contract
  run for twenty years, the accumulated capital is of the order of **10 000 € to 20 000 €**
  `[std] derived` from the section 4 cases, which at any plausible *Rentenfaktor* produces a monthly
  annuity in the tens of euros — squarely in *Kleinbetragsrente* territory. **A material fraction of
  Riester contracts will therefore never pay an annuity at all.** The delib model must carry the
  commutation as a real payout mode with its own model point, not as a footnote.

### 13. Death benefits and *Hinterbliebenenschutz*

- **Before *Rentenbeginn***. The contract's death benefit is normally the accumulated capital
  `[unverified]` as a market characterisation. The subsidy treatment, not the benefit design, is
  what is distinctive [R14]:
  - **Transfer to a surviving spouse's own certified contract is *förderunschädlich***, subject to
    conditions (marriage subsisting, not permanently separated) `[unverified]`. This is the route the
    product intends.
  - **Payment to any other heir is *schädlich***: the *Rückzahlungsbetrag* — all Zulagen and all
    § 10a relief — is deducted before payment, and the investment return on the subsidised part
    becomes taxable `[unverified]`.
- **After *Rentenbeginn***. Continuation to a spouse under a survivor's-annuity option, or payments
  for the remainder of a *Rentengarantiezeit*, are *förderunschädlich* `[unverified]`. A lump-sum
  death benefit outside those forms is not certifiable at all [R1].
- **Riders.** A Riester contract may carry a *Berufsunfähigkeits-Zusatzversicherung* or a survivor's
  benefit, with the contributions applied to them capped as a share of total contributions and
  excluded from the *Beitragsgarantie* [R1] `[unverified]`. **The cap's level was not established**
  (gap 11).
- **Consequence for the model**: the death benefit before *Rentenbeginn* is the account value, and
  the *Rückzahlungsbetrag* is a **deduction from the benefit paid, not an insurer cash flow** — the
  provider withholds it and remits it to the ZfA. A gross-liability model may publish the death
  benefit either gross or net of the *Rückzahlungsbetrag*; the reference implementation publishes it
  **gross** and states the convention, because the withholding is a tax collection, not a change in
  the insurer's obligation.

### 14. Options: *Anbieterwechsel*, *Beitragsfreistellung*, *Kündigung*

- **Anbieterwechsel** [R1]. A statutory right: terminate, and have the accumulated capital
  transferred directly to another certified contract. No *schädliche Verwendung*, no tax
  consequence, the guarantee accumulator travels with the money `[unverified]` — **and it is the
  single most important structural difference from every other product in delib.** No Schicht-3
  German life contract carries a portability right of this kind. Its cash-flow consequence is that a
  Riester "lapse" is frequently **not** a surrender at all but a **transfer out at full value**,
  which for the ceding insurer is a full-value exit and for the model is a distinct decrement from
  a surrender. **The notice period and the transfer-charge cap were not established** (gap 8).
- **Beitragsfreistellung** — stopping contributions and leaving the contract in force. Under § 165
  VVG the policyholder of a German life contract may convert to a paid-up contract at any time; the
  Riester overlay is that the contract stays certified, the guarantee stands on what was paid, no
  further Zulagen arrive, and no subsidy is repaid. **This is the German Riester book's dominant
  exit** (section 21).
- **Kündigung with payment of the *Rückkaufswert*** — permitted by the VVG and punished by the EStG.
  The saver receives the surrender value **less** the *Rückzahlungsbetrag* (all Zulagen and all
  § 10a relief), and the growth on the subsidised part becomes taxable [R14]. Against a surrender
  value that is itself below the contributions paid in the early years, the combination makes a cash
  surrender an economically severe act. It is the reason a Riester lapse assumption should be
  materially **lower** than a Schicht-3 one and the reason the *ruhender Vertrag* exists as a
  category at all.
- **Versorgungsausgleich** on divorce — internal or external division of the contract, transfer to
  the other spouse's certified contract, *förderunschädlich* `[unverified]` [R14].
- **Wohn-Riester withdrawal** — a complete or partial exit into property, *förderunschädlich*, with
  the *Wohnförderkonto* consequence (section 16) [R13].
- **Reference implementation.** Four exits: death; transfer out (*Anbieterwechsel*) at full value;
  *Beitragsfreistellung*, which is a change of state rather than an exit; and surrender, at a `[std]`
  rate set low with the rationale above. Wohn-Riester withdrawal is **not** implemented and the
  model documentation says so.

### 15. Taxation

- **In**: contributions relieved via the Zulagen [R9] or the § 10a deduction [R6], whichever the
  *Günstigerprüfung* favours.
- **Out**: **full** taxation of the benefit as *sonstige Einkünfte* under § 22 Nr. 5 EStG, to the
  extent it derives from subsidised contributions [R12]. No *Ertragsanteil*. This is what "Schicht 2"
  means in cash terms.
- **The unsubsidised pool** is taxed on the *Ertragsanteil* (annuity) or under § 20 Abs. 1 Nr. 6
  (lump sum) [R12]; the provider apportions in the annual *Leistungsmitteilung* `[unverified]`.
- **The *Teilkapitalauszahlung*** is taxed in full in its year, with no *Fünftelregelung*
  `[unverified]`; the *Kleinbetragsrenten-Abfindung* **does** get the *Fünftelregelung* [R15] [R21].
- **Social insurance**: a Riester annuity from a **private** contract is not a *Versorgungsbezug* and
  is not subject to *Krankenversicherung* contributions for a compulsorily insured pensioner; a
  Riester annuity from a **bAV** vehicle was, and the double charge was removed by [R21]
  `[unverified]` on both limbs. Voluntarily insured pensioners are assessed on all income
  `[unverified]`.
- **Means-tested basic security**: a *Freibetrag* applies so that a Riester annuity is no longer
  offset one-for-one against *Grundsicherung im Alter* [R21] `[unverified]` on the amounts. This
  repaired the product's sharpest design criticism — that for a low earner the subsidy could end up
  benefiting the state rather than the saver — and it is the reason the low-income case D of
  section 4 can be described as working.
- **Consequence for the model: none in the cash flows.** delib publishes gross liability cash flows;
  tax is a recipient-side matter. It is documented because the product spec must be able to say why
  a Riester annuity of a given gross amount is not comparable with a Schicht-3 annuity of the same
  gross amount.

### 16. Wohn-Riester and the *Wohnförderkonto* — and why they are out of scope

- **What it is** [R13] [R19] [S13]. Two routes into owner-occupied property: withdraw the
  accumulated capital as an *Altersvorsorge-Eigenheimbetrag* to buy, build, repay a loan on, or
  barrier-reduce a dwelling; or hold a certified **loan** or *Bausparvertrag* [R3] whose
  *Tilgungsleistungen* themselves draw the Zulagen [R8].
- **The *Wohnförderkonto*** [R13]. Because the money left the annuity, the subsidy attached to it
  must still be taxed. Withdrawals and subsidised repayments are recorded in a **notional** account
  accruing at a statutory **2 %** per year `[unverified]`, whose balance is taxed in the payout
  phase either **spread annually to the year the saver reaches 85** or **in one sum with a 30 %
  discount** `[unverified]`.
- **Why it is excluded from the delib model, in three reasons of decreasing weight:**
  1. **There is no cash flow.** The *Wohnförderkonto* is a tax memorandum with a notional interest
     rate; it never holds money, never pays money, and never appears in an insurer's liability. A
     liability cash-flow projection has nothing to project.
  2. **The liability, where there is one, is a loan.** A Riester *Darlehen* or *Bausparvertrag* is a
     banking liability with a repayment schedule, an interest rate and a credit exposure — a
     different model, in a different library, if it were in scope at all.
  3. **From the insurer's side the withdrawal is simply an exit.** An *Eigenheimbetrag* taken out of
     a Riester **insurance** contract terminates the annuity liability at full value. The model can
     represent that as a decrement; it cannot represent what happens to the money afterwards, and
     pretending otherwise would be the kind of scope creep the delib brief forbids.
- **What the delib documents must nonetheless say.** That Wohn-Riester exists, that it is a large
  share of the Riester contract count (section 20), that a contract counted as "Riester" in an
  official statistic may be a mortgage, and that the model's contract count is therefore **not**
  comparable with a published Riester contract count without adjustment.

### 17. The four product forms, and which one this model represents

| Form | Provider | Accumulation | Guarantee met by | Payout | In delib? |
|---|---|---|---|---|---|
| **Klassische Riester-Rentenversicherung** | life insurer | *Deckungskapital* at the *Rechnungszins* + *Überschuss* | the general account and the guaranteed interest | lifelong annuity at a *Rentenfaktor* | **yes — `riester_rente`, `Riester_DE_A`** |
| Fondsgebundene Riester-Rentenversicherung | life insurer | unit funds + a guarantee asset | dynamic reallocation (section 18) | lifelong annuity at a *Rentenfaktor* | no — chassis documented in `fondsgebundene_rentenversicherung` |
| Riester-Fondssparplan | *Kapitalverwaltungsgesellschaft* [S9]–[S11] | fund units | rule-based reallocation between an equity and a bond fund | *Auszahlungsplan* + *Restverrentung* from 85 | no |
| Riester-Banksparplan | bank / *Sparkasse* [S12] | deposit balance + bonus scale | trivially — a deposit cannot fall | *Auszahlungsplan* + *Restverrentung* from 85 | no |
| Wohn-Riester (*Bausparvertrag*, *Darlehen*) | *Bausparkasse* / bank [S13] | savings, then a loan | n/a | property use + *Wohnförderkonto* | no (section 16) |

- **The delib model represents the first row**: the classic general-account Riester annuity. The
  reasons are three, and the product spec should give all of them. It is the form for which the
  *Beitragsgarantie* interacts with an actuarial mechanic (the *Rechnungszins*) rather than with an
  asset-allocation algorithm, so the guarantee's cost is **visible in the recursion** instead of
  hidden in a rebalancing rule. It is the form whose payout is an insurance annuity throughout, so
  the whole contract is one liability. And it is the form the GDV still maintains a 2025-vintage
  model wording for [S2], so it is a live contract type and not a historical curiosity.
- **What the model deliberately does not do**: no unit-linked funds, no rebalancing algorithm, no
  *Auszahlungsplan*, no loan, no *Wohnförderkonto*. Each of those is stated in `model.md` as an
  explicit non-implementation rather than left to be discovered.

### 18. The unit-linked guarantee designs, for contrast

Recorded because they are the sharpest illustration of section 19 and because a reader will ask why
a 100 %-guaranteed unit-linked product is possible at all. All of this is `[unverified]` as a
description of any particular product; it is the German market's generic taxonomy.

- **Statisches Hybridmodell** — each contribution is split **once**, at receipt, between the
  *Sicherungsvermögen* (which must accumulate to the guaranteed amount at *Rentenbeginn*) and a free
  fund. The split ratio is exactly the `(1 + i)^−n` factor of section 19 and is fixed for that
  contribution's remaining term. Simple, transparent, and maximally conservative.
- **Dynamisches Hybridmodell (two- or three-pot)** — the split is **rebalanced periodically** between
  the *Sicherungsvermögen*, a *Wertsicherungsfonds* and a free fund, so that a contract running ahead
  of its guarantee can carry more risk.
- **i-CPPI** — an individual constant-proportion portfolio insurance rule: the risk allocation is a
  multiple of the *cushion* (the excess of the account value over the present value of the
  guarantee), rebalanced frequently and per policy.
- **The pathology all three share is the *cash lock***. When the account value falls to the present
  value of the guarantee, the cushion is zero, the risk allocation is zero, and the contract is
  locked into the guarantee asset for its remaining term — it cannot participate in a subsequent
  recovery. The lower the *Rechnungszins* and the shorter the remaining term, the more easily this
  happens, which is why the 0,25 % regime of 2022–2024 [R22] was as damaging to the unit-linked
  Riester designs as to the classic ones.
- **The classic chassis has no cash lock** because it has no risk asset at the policy level: the
  policyholder's account is always the *Deckungskapital*, and the asset risk sits in the insurer's
  general account under the *Überschussbeteiligung*. That is a real advantage of the form this model
  represents and the product spec should say so.

