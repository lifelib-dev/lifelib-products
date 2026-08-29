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

