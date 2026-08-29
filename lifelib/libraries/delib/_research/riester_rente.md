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

