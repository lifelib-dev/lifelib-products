# lifelib-products

**This repository is where reference models are drafted for merging into
[lifelib](https://github.com/lifelib-dev/lifelib).** It is a staging ground, not a package
to install or depend on: each library under `lifelib/libraries/` is written in the shape
lifelib expects, and is drafted, reviewed and held to standard here until it lands
upstream as a lifelib library of its own.

What it holds is a library of **product specifications for major life insurance products,
organized by country**, together with the documentation needed to build **reference
implementations of liability cash flow projection models** (lifelib/modelx style),
organized by product type and country.

**Status:** Draft, 2026-08-30. Current coverage: United States (6 individual life and
6 individual annuity product types), United Kingdom (7 product types, including pension
annuities), Japan (9 product types, three of them 第三分野 health products), France
(9 product types, five of them built on *assurance vie*), Germany (10 product types,
organised on the *Drei-Schichten-Modell*) and Korea (10 product types, four of them
제3보험 third-sector products).
**All fifty-seven products ship an executable reference model** in
`<library>/products/<product>/`, beside the documents that specify it — twelve in
`lifelib/libraries/uslib/`, seven in `lifelib/libraries/uklib/`, nine in
`lifelib/libraries/jplib/`, nine in `lifelib/libraries/frlib/`, ten in
`lifelib/libraries/delib/` and ten in `lifelib/libraries/krlib/`, each one reproducing its
own technical notes' worked example, asserted cell by cell. All six are lifelib libraries
in shape: they sit at the path lifelib puts its libraries on, they render as Sphinx page
trees, and every regulatory citation in them is a working link.

---

## Organization

```
lifelib/libraries/                   the path lifelib keeps its libraries on, and so does this
  <library>/                         uslib/, uklib/, jplib/, frlib/, delib/, krlib/ — named for the lifelib library each becomes
    index.md                         library overview, the models, citation conventions
    products/
      <product>/                     each product's documents and its executable model, together
        product-spec.md              representative product specification
        technical-notes.md           liability cash flow model: design, assumptions, recursions
        model.md                     how the model implements the notes, and what is [std]
        sources.md                   numbered source list for this product's documents
        run.py  *.csv  <Model>/      the modelx model and its inputs
    references/
      regulatory-and-actuarial-references.md
                                     curated cross-product bibliography
    tests/                           one module per model, plus the shared conventions suite
    _research/                       raw research notes — citation ground truth / provenance
```

The Sphinx pages are **not** in the library: `doc/source/libraries/<lib>/` holds a one-line
`{include}` stub per document, mirroring the library tree, plus the autodoc pages generated
from the models' own docstrings. They are plumbing, and a `lifelib.create()` copy is better
without them.

All six libraries are in this shape and ready to merge into lifelib — see
[USLIB-MERGE-PLAN.md](USLIB-MERGE-PLAN.md) for the design and [MERGE.md](MERGE.md) for the
lifelib-side checklist.

## Building the documentation

The documents live beside the models they describe rather than under `doc/`. The page tree
under `doc/source/libraries/<lib>/` is written out by `tools/gen_scaffolding.py`, one
`{include}` stub per document, so nothing is copied and nothing is generated at build time
— the same arrangement the documents have inside lifelib, down to the include paths.

```bash
cd doc && make html
```

To hold the documents to the standard they have to meet — every warning an error, and
**nitpicky**, without which an unresolved `:func:`/`:mod:` role is dropped silently rather
than reported:

```bash
python tools/doccheck.py
```

It should report zero across the six libraries. Run the model suites with:

```bash
python -m pytest lifelib/libraries/uslib/tests lifelib/libraries/uklib/tests \
    lifelib/libraries/jplib/tests lifelib/libraries/frlib/tests \
    lifelib/libraries/delib/tests lifelib/libraries/krlib/tests -q
```

- **`product-spec.md`** defines a *representative* product: a standardized composite
  built from publicly available documentation of real products, not any single
  insurer's contract. It records contractual mechanics, a full parameter set, observed
  variations across insurers, and the rationale for each representative choice.
- **`technical-notes.md`** specifies the liability cash flow projection model for that
  product: model point attributes, state variables, assumption inputs, cash flow
  recursions with explicit processing order, policyholder behavior, a numeric worked
  example, valuation pointers, and key sensitivities.
- **`sources.md`** lists every source cited by that product's documents, with URLs,
  access dates, and whether the document was actually retrieved.
- **`_research/`** holds the underlying research notes. Every sourced fact in the
  product documents traces back to a source entry in these files. They are provenance:
  keep them, do not renumber their source lists.

## Citation conventions

Used uniformly across the library. Whether a tag renders as a link says what kind of source
it is: a **specification** citation stays as bracketed text, an **authority** the model is
held to is a link you can follow.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (brochure, specimen policy, prospectus, producer guide, 約款, 契約締結前交付書面, *notice d'information*, *conditions générales*, *document d'information clé*) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library `references/regulatory-and-actuarial-references.md` (frozen R-numbering) |
| **[std]** | link | A *standardization introduced for the reference implementation* — a parameter or convention chosen where sources vary, are proprietary, or are silent. Each carries a rationale and, where available, the observed range across insurers |
| `[unverified]` | link | A claim from general knowledge or a secondary snippet that could **not** be confirmed against a retrieved document — treat as a to-verify item, not an established fact |

The hard rule throughout: **every quantitative parameter is either source-tagged or
marked [std]** — information taken from source materials is never mixed silently with
assumptions introduced for the representative specification.

## Methodology

Each country section is built in three passes:

1. **Research** — per product type, collect primary product documentation (insurer
   brochures and product guides, specimen policy forms, SEC prospectuses where the
   product is registered, 約款 and 契約締結前交付書面) and the governing actuarial/regulatory
   references, which differ by market: NAIC model laws and actuarial guidelines, the
   Valuation Manual, IRC provisions, SOA experience studies, AAA practice notes and ASOPs
   for the U.S.; the PRA Rulebook, FCA Handbook and CMI materials for the UK; 保険業法 and
   its 施行規則, the FSA 告示 and 監督指針, 日本アクチュアリー会's standard tables, and the
   公的 statistical series (患者調査, 全国がん登録, 介護保険事業状況報告) for Japan; and the Code
   des assurances on Légifrance, the ACPR, the *arrêtés* homologating TH 00-02 / TF 00-02
   and TGH05 / TGF05, INSEE, DREES / CNSA and France Assureurs for France; and the VAG,
   VVG, DeckRV and MindZV, the BaFin *Merkblätter*, the DAV table families, the *Drei-Schichten*
   provisions of the EStG and the AltZertG, and GDV and Destatis statistics for Germany;
   and 보험업법, 상법 제4편 and the 보험업감독규정 별표 on 국가법령정보센터, the 금융위원회
   and 금융감독원, 보험개발원's 경험생명표 and 참조순보험요율, the 생명보험협회 and
   손해보험협회 공시실, 국가암등록통계, and 국민건강보험공단's 건강보험 and 노인장기요양보험
   통계연보 for Korea. Everything lands in `_research/` with per-source fact extraction
   and explicit fetch-failure notes.
2. **Drafting** — write the product spec and technical notes from the research files
   under the citation discipline above, choosing and justifying a representative
   design where insurers differ.
3. **Review** — an adversarial pass per product (citation integrity against the
   research files, recomputation of all formulas and worked examples, internal
   consistency), then a cross-product consistency pass (shared terminology, shared
   base-chassis mechanics, link and tag integrity).

**The Germany library was drafted blind, then re-verified, and says so on every page it
touches.** `delib` was first built in an environment whose network policy blocked direct HTTP
egress to every host outside a package-registry allowlist — `gesetze-im-internet.de`,
`bafin.de`, `aktuar.de`, `gdv.de`, `destatis.de` and `eur-lex.europa.eu` were each tried and
each refused at the gateway — and the session's web-search budget was exhausted partway
through the regulatory research, so the later product files had no research channel at all.
That first draft rested on the authoring model's own knowledge of German insurance law and
practice, disciplined by **[std]** and **[unverified]** tags.

The policy was later lifted and **every citation re-checked against the document it names**.
All fifteen German instruments the library cites were read as canonical XML from
gesetze-im-internet with each law's *Stand* recorded, and **950 statutory section references
were checked, of which 950 were correct**; insurer *AVB*, *Verbraucherinformationen* and
*Produktinformationsblätter* were retrieved as PDFs and read. Of 969 source entries, **613 now
read `Retrieved: yes`**, 37 were reached in part, and 319 could not be opened — a 404, a
consent or JavaScript wall, a paywall, a subscription login, or an address never established.
An entry that still reads `Retrieved: no` remains a **pointer, not a certificate**.

The re-verification corrected the drafted text in every product, which is the strongest reason
to read a claim against its own entry rather than trusting the library as a whole. Coverage is
uneven, and unevenly by source type rather than by effort: the statutory core is near-complete,
while products whose primary sources are carrier wordings behind a document portal are
thinnest. Findings that reach a **modelled** rate or rule were recorded and deliberately not
acted on, since a model change moves the worked example and its golden tests with it.

## Coverage

| Country | Products | Status |
|---|---|---|
| [United States](lifelib/libraries/uslib/index.md) | **Life:** term life, whole life, universal life, indexed UL, variable UL, guaranteed UL<br>**Annuity:** fixed deferred (MYGA), fixed indexed, variable, registered index-linked (RILA), immediate (SPIA), deferred income (DIA/QLAC) | specs, technical notes and all 12 [models](lifelib/libraries/uslib/index.md#the-models); builds as a library |
| [United Kingdom](lifelib/libraries/uklib/index.md) | term assurance, critical illness, income protection, whole of life, with-profits, unit-linked bond, pension annuity | specs, technical notes and all 7 [models](lifelib/libraries/uklib/index.md#the-models); builds as a library |
| [Japan](lifelib/libraries/jplib/index.md) | **Protection:** 定期保険 term life, 収入保障保険 survivor income term<br>**Savings:** 終身保険 whole life, 養老保険 endowment (with 学資保険), 外貨建終身保険 FX whole life<br>**第三分野:** 医療保険 medical, がん保険 cancer, 介護保険 nursing care<br>**Annuity:** 個人年金保険 individual annuity | specs, technical notes and all 9 [models](lifelib/libraries/jplib/index.md#the-models); builds as a library |
| [France](lifelib/libraries/frlib/index.md) | **Épargne:** assurance vie fonds en euros, assurance vie unités de compte, eurocroissance<br>**Retraite:** PER assurantiel, rente viagère immédiate<br>**Prévoyance:** temporaire décès, assurance emprunteur, contrat obsèques, dépendance | specs, technical notes and all 9 [models](lifelib/libraries/frlib/index.md#the-models); builds as a library |
| [Germany](lifelib/libraries/delib/index.md) | **Schicht 3:** kapitalbildende Lebensversicherung, klassische Rentenversicherung, fondsgebundene Rentenversicherung, Indexpolice<br>**Geförderte Vorsorge:** Basisrente (Rürup), Riester-Rente<br>**Rentenbezug und Biometrie:** Sofortrente, Risikolebensversicherung, Berufsunfähigkeitsversicherung, Pflegerentenversicherung | specs, technical notes and all 10 [models](lifelib/libraries/delib/index.md#the-models); builds as a library |
| [Korea](lifelib/libraries/krlib/index.md) | **보장성:** 종신보험 whole life, 정기보험 term life, CI보험 critical illness<br>**제3보험:** 실손의료보험 indemnity medical, 암보험 cancer, 간병보험 long-term care, 어린이보험 children's<br>**저축·연금:** 연금저축보험 tax-qualified pension savings, 변액연금보험 variable annuity, 즉시연금 immediate annuity | specs, technical notes and all 10 [models](lifelib/libraries/krlib/index.md#the-models); builds as a library |

Scope note: all six libraries cover individual business, but what "individual life
insurance" means differs by market and the coverage follows the market rather than a
template. The U.S. library covers the deferred and payout annuity families sold at retail;
the UK library covers pension annuities, the dominant UK annuity form and the centrepiece
of the Solvency UK matching adjustment; the Japan library gives three of its nine slots to
**第三分野** health products — medical, cancer and nursing care — because third-sector cover
is what Japanese households buy most by policy count, and its benefit structure is
frequency x severity x limit rather than a sum assured. The France library gives five of
its nine to *assurance vie* and what is built on it, because *assurance vie* is the French
savings vehicle rather than one product among several, and a sixth to *assurance
emprunteur*, the cover a French borrower buys with a mortgage, which is the largest
individual protection market in the country and has no counterpart in the other three.
The Germany library is organized on the **Drei-Schichten-Modell** the *Alterseinkünftegesetz*
imposed on German retirement saving in 2005, because in Germany the tax layer a contract sits
in decides its mechanics rather than merely its treatment: a *Basisrente* may not be
surrendered at all, and a *Riester-Rente* carries a statutory 100 % *Beitragsgarantie*, and
both of those are model structure rather than parameters. A slot goes to the
**Berufsunfähigkeitsversicherung**, the country's flagship protection product, which has no
counterpart in the other four. The Korea library gives four of its ten slots to
**제3보험**, the statutory 상해·질병·간병 (accident, sickness, long-term care) category of
보험업법 제4조제1항제3호 that both life and non-life insurers may write, because that is
what Korean households buy; and one of those four, **실손의료보험**, is the only
**indemnity** contract anywhere in this repository — held by around two thirds of the
population and sold as a reimbursement layer on top of the public 국민건강보험, so its
급여/비급여 split, co-payment and annual limits are the model itself rather than a
description wrapped around a sum assured.
Group insurance, 共済 (cooperative insurance), *contrats collectifs*, German **betriebliche
Altersversorgung** and substitutive **private Krankenversicherung**, and institutional
business (bulk purchase annuities, pension risk transfer) are out of scope in all six.

## Roadmap

- **The merge itself**: all six libraries are prepared, and what remains is the
  lifelib-side half — [MERGE.md](MERGE.md) is the checklist. It was written for the first
  three and has not been revised for frlib, delib or krlib; the library-side work those
  three needed was the same, and the lifelib-side steps are unchanged apart from the
  directory names.
- **Additional countries**, and additional product families (group insurance,
  institutional/pension risk transfer business) as coverage grows.

## Disclaimer

This library is technical documentation for modeling purposes. The representative
specifications are standardized composites and do not describe any insurer's actual
contract; nothing here is insurance, investment, tax, or legal advice.
