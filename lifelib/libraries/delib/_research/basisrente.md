# Basisrente (Rürup-Rente), Schicht 1 — research notes (Germany)

Research notes for the German **Basisrente** — the *Basisrentenvertrag* of § 10 Abs. 1 Nr. 2
Buchstabe b EStG, created by the *Alterseinkünftegesetz* of 2004 and sold under the popular name
*Rürup-Rente* after Bert Rürup, who chaired the commission that proposed it. It is the first layer
(*Schicht 1*) of the German three-layer retirement architecture: a privately written, funded,
individually owned contract that is nevertheless treated for tax purposes like the *gesetzliche
Rentenversicherung* — contributions deductible as *Sonderausgaben* on the way in, benefits taxed
as *sonstige Einkünfte* on the way out, at a *Besteuerungsanteil* fixed by the cohort year of
*Rentenbeginn*.

**The product is defined by prohibitions, not by benefits.** Its accumulation and payout mechanics
are those of an ordinary German deferred annuity — the same *Deckungskapital* recursion, the same
*Überschussbeteiligung*, the same *Rentenfaktor*, the same DAV 2004 R basis as the delib
`klassische_rentenversicherung` product. What makes it a distinct product, and what a projection
model has to get right, is a closed list of things it may **not** do: the entitlement may not be
inherited, transferred, charged as security, sold or turned into capital, and no *Rückkaufswert*
may be paid on termination. Everything else in this file follows from that sentence.

**In scope.** The individual, privately written *Basisrentenvertrag (Alter)* on a single life
against a *laufender Beitrag*, a *Zuzahlung* or a *Einmalbeitrag*, certified under § 5a AltZertG,
in all three of its asset forms — *klassisch* (general account), *fondsgebunden* (unit-linked) and
*fondsgebunden mit Beitragsgarantie* (hybrid) — together with the two riders the statute permits
inside the same contract: *Hinterbliebenenabsicherung* and *Berufsunfähigkeits-Zusatzversicherung*.

**Out of scope, and said so where it matters.**

- **The other two layers.** *Riester-Rente* (Schicht 2, delib product 6) shares the AltZertG
  certification regime but has a different subsidy (*Zulage* plus § 10a EStG), a mandatory
  *Beitragserhaltungsgarantie*, a permitted 30 % *Teilkapitalauszahlung* and a *Kleinbetragsrenten*
  commutation — four things the Basisrente does not have. *Klassische private Rentenversicherung*
  (Schicht 3, delib product 2) has the same chassis with none of the constraints: full
  *Kapitalwahlrecht*, a *Rückkaufswert*, free beneficiary designation, and *Ertragsanteil* taxation.
  Both are separate delib products and are referenced here only as contrasts.
- **The competing Schicht-1 vehicles.** The *gesetzliche Rentenversicherung*, the
  *berufsständische Versorgungswerke* and the *landwirtschaftliche Alterskasse* sit in
  § 10 Abs. 1 Nr. 2 **Buchstabe a** EStG and share the **same annual *Höchstbetrag*** as the
  Basisrente. They are not modelled, but the shared ceiling is a first-order fact about the product
  and is treated in mechanic 6.
- **The *Fonds-Basisrente*.** A Basisrentenvertrag may also be written by a
  *Kapitalverwaltungsgesellschaft* as a fund savings plan whose payout phase is bought in from a
  life insurer. It meets the same § 10 and § 5a AltZertG tests and competes for the same buyer, but
  its accumulation phase is not an insurance liability and delib does not model it.
- **Betriebliche Altersversorgung** in all five *Durchführungswege*, *Gruppenversicherung*, *private
  Krankenversicherung* and *Sterbegeldversicherung* are outside the delib library entirely.
- Austrian and Swiss documents are excluded even where a search would return them: the EStG, the
  AltZertG and the DeckRV do not apply to them.

These notes are the **citation ground truth** for the delib `basisrente` product documents. Source
ids **S1..S16** and **R1..R24** below are **frozen — never renumber**; unused ids are simply
omitted downstream, leaving gaps, and `sources.md` records which are absent and why.

Access date for all citations: **2026-08-29**.

---

## Retrieval conditions and citation discipline

Read this before reading anything else in the file. It is what separates a delib citation from an
frlib one.

**No document in this file was retrieved.** Direct HTTP egress from this build environment is
blocked by an organisation network policy. `WebFetch` and `curl` are refused at the egress gateway
for every host outside a short package-registry allowlist. The hosts that matter for this product
were tried again while writing this file and every one of them was refused with the identical
error — `curl: (56) CONNECT tunnel failed, response 403`:

| Host | What it holds for this product | Result |
|---|---|---|
| `gesetze-im-internet.de` | EStG § 10, § 22; AltZertG; ZPO § 851c; VVG; DeckRV | 403 at the gateway |
| `bafin.de` | supervisory material, *Merkblätter*, statistics | 403 at the gateway |
| `gdv.de` | *Musterbedingungen*, market statistics | 403 at the gateway |
| `de.wikipedia.org` | the encyclopaedic overview | 403 at the gateway |
| `aktuar.de` | DAV, *Höchstrechnungszins*, DAV 2004 R | 403 at the gateway |
| `bundesfinanzministerium.de` | BMF-Schreiben, *Sonderausgabenabzug* guidance | 403 at the gateway |
| `bzst.de` | the certifying authority for Basisrentenverträge | 403 at the gateway |

Not one *Bedingungswerk*, not one *Produktinformationsblatt*, not one *Basisinformationsblatt*, not
one statutory text, not one BMF-Schreiben and not one insurer *Verbraucherinformation* was opened.

**There was also no search channel.** The session's `WebSearch` budget — a hard cap of 200 calls
shared across all delib work — was **exhausted before this product was reached**. The two delib
research files written earlier (`kapitallebensversicherung.md`, `klassische_rentenversicherung.md`)
consumed it. This file was therefore written with **no research channel of any kind**: no fetch, no
search, no snippet, no summary. That is a materially weaker evidential position than either sibling
file, and it is stated on every source entry rather than glossed.

What follows from that, exactly, and it is applied without exception below:

1. **Every source entry carries the honest retrieval line.** The standard line in this file is
   `Retrieved: no — egress blocked; no search corroboration (session search budget exhausted)`. A
   small number of entries carry a stronger line because their **identity** was established in a
   sibling delib research file while search was still available; those say so and name the file.
   **`Retrieved: yes` appears nowhere in this document.**
2. **Nothing is quoted.** Not one sentence of German statutory or contractual wording appears here
   in quotation marks as though it were read. Where the substance of a provision is given, it is
   given in English, in this file's own words, as *what the provision does*. A reader who needs the
   wording must go to the instrument.
3. **No URL, document number, edition, page count or publication date is invented.** Where a
   canonical `gesetze-im-internet.de` form is obvious — `.../estg/__10.html` for § 10 EStG — it is
   offered and marked `[unverified]`. Everywhere else the entry says `URL: not established`. No
   *Bundesgesetzblatt* citation and no BMF-Schreiben file number appears anywhere in this file,
   because none could be confirmed.
4. **`[unverified]` is used generously and means what it always means.** Every specific paragraph
   number, every effective date, every monetary amount, every percentage and every market figure in
   this file carries it, because no search result confirmed any of them. The general *shape* of a
   well-established mechanic — that a Basisrente cannot be surrendered, that contributions are
   deductible, that the annuity is taxed on a cohort percentage — is not tagged, because tagging it
   would drown the signal. **The moment a claim becomes specific and numeric, it is tagged.**
5. **Uncertain numbers became `[std]` parameters, not citations.** Where the mechanic is certain and
   the level is not — a charge, a *Rentenfaktor*, a *Beitragsfreistellung* rate, a market share —
   this file ships a `[std]` value with a stated rationale and an argued plausible range rather than
   a fabricated source tag. A `[std]` number is honest. A guessed `[S4]` number is not.
6. **The weight of the file is in the mechanics.** Sections 1 to 22 below are the part that does not
   depend on having a PDF open, and they are written long and precise. The source blocks are
   correspondingly short: they name the documents a checker must go to, and they say plainly what
   they do and do not establish.

**A delib citation is a pointer, not a certificate.** An `[R1]` tag on a sentence about
§ 10 Abs. 1 Nr. 2 Buchst. b EStG means *this is the instrument this claim must be checked against*.
It does not mean anyone read it. Downstream documents must not upgrade that.

---

## German terminology

German terms of art stay in German, italicised on first use, with a gloss. The ones this product
turns on:

| Term | Gloss |
|---|---|
| *Basisrente*, *Rürup-Rente*, *Basisrentenvertrag* | The Schicht-1 private pension of § 10 Abs. 1 Nr. 2 Buchst. b EStG. "Rürup" is a market nickname; the statute and the certifying authority say *Basisrentenvertrag* |
| *Schicht 1 / 2 / 3* | The three layers of German retirement provision: basic (GRV, Versorgungswerk, Basisrente); subsidised supplementary (Riester, bAV); unsubsidised private |
| *Alterseinkünftegesetz* (AltEinkG) | The 2004 statute that created the layer architecture, the *nachgelagerte Besteuerung* and the Basisrente |
| *Nachgelagerte Besteuerung* | Deferred taxation: relief on contributions, tax on benefits — the design principle of Schicht 1 |
| *Sonderausgabenabzug* | Deduction of contributions from taxable income as *Sonderausgaben* under § 10 EStG |
| *Höchstbetrag* | The annual ceiling on deductible Schicht-1 contributions, pegged to the maximum contribution to the *knappschaftliche Rentenversicherung* |
| *Beitragsbemessungsgrenze* (BBG) | Contribution assessment ceiling of a social-insurance branch; the *knappschaftliche* BBG is what the *Höchstbetrag* tracks |
| *Knappschaftliche Rentenversicherung* | The miners' branch of the statutory pension scheme, with its own higher BBG and higher contribution rate |
| *Besteuerungsanteil* | The percentage of the annuity that is taxable, fixed by the calendar year of *Rentenbeginn* and constant for life |
| *Rentenfreibetrag* | The euro complement of the *Besteuerungsanteil*, frozen in the year after *Rentenbeginn* and never re-indexed |
| *Ertragsanteil* | The much lower taxable fraction applied to Schicht-3 annuities under § 22 EStG — the comparator, not this product's rule |
| *Kohortenprinzip* | The cohort principle: the taxable share depends on the year the annuity starts, not on the taxpayer |
| *Vererblichkeit*, *Übertragbarkeit*, *Beleihbarkeit*, *Veräußerbarkeit*, *Kapitalisierbarkeit* | The five properties a Basisrente entitlement must **not** have |
| *Hinterbliebenenabsicherung* | Survivor cover; permitted only for the spouse or registered partner and for children while *Kindergeld* runs |
| *Kindergeldberechtigung* | Entitlement to child benefit; the statutory test that defines an eligible child beneficiary |
| *Beitragsrückgewähr* | Return of contributions on death; in Schicht 1 it can only fund a survivor's annuity, never a lump sum |
| *Rentengarantiezeit* | Guaranteed payment period after *Rentenbeginn*; in Schicht 1 payable only to permitted survivors |
| *Berufsunfähigkeits-Zusatzversicherung* (BUZ) | Occupational-disability rider written inside the main contract |
| *Berufsunfähigkeit* / *verminderte Erwerbsfähigkeit* | Occupational disability / reduced earning capacity — the two disability risks the statute permits inside a Basisrente |
| *Beitragsfreistellung* | Making the contract paid-up; the Basisrente's only exit |
| *Kündigung* / *Rückkaufswert* | Termination / surrender value — both effectively unavailable on this product |
| *Zuzahlung* / *Einmalbeitrag* | A one-off top-up into an existing contract / a single-premium contract |
| *Beitragsdynamik* | Contractual annual premium escalation |
| *Rentenbeginn* | Vesting date; the boundary at which the accumulated capital becomes an annuity |
| *Aufschubphase* / *Rentenphase*, *Rentenbezugsphase* | Deferment (accumulation) phase / payout phase |
| *Rentenfaktor* | Monthly annuity per 10 000 € of capital at *Rentenbeginn* |
| *Deckungskapital* / *Deckungsrückstellung* | The actuarial reserve of one contract / the balance-sheet provision covering it |
| *Rechnungszins* / *Höchstrechnungszins* | The technical interest rate the contract is priced and reserved on / its statutory maximum for new business |
| *Überschussbeteiligung* / *Schlussüberschussanteil* | Participation in surplus / terminal bonus |
| *Zillmerung* / *Höchstzillmersatz* | Financing acquisition costs into the reserve / the statutory cap on the amount so financed |
| *Effektivkosten* | Reduction in yield: the annualised return give-up caused by all charges, disclosed on the *Produktinformationsblatt* |
| *Chancen-Risiko-Klasse* (CRK) | The standardised risk class shown on the *Produktinformationsblatt* |
| *Pfändungsschutz* | Protection from attachment by creditors; § 851c ZPO for this product |
| *Zertifizierung* | Certification of the contract by the *Bundeszentralamt für Steuern* under AltZertG |
| *Produktinformationsblatt* (PIB) | The standardised pre-sale document required for certified contracts |
| *Basisinformationsblatt* (BIB) | The PRIIP key information document |
| *Versorgungsausgleich* | Pension rights sharing on divorce — the one transfer the statute permits |
| *Kleinbetragsrente* | A trivially small annuity; commutable in Schicht 2, **not** in Schicht 1 |

---
