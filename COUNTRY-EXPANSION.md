# Country Expansion — Which Market to Build Next

**Status:** Research note, 2026-08-18. Decision input for the "Additional countries" item on
the [README roadmap](README.md#roadmap).

Candidates assessed: **Germany, France, China, Switzerland, Japan, Korea, Hong Kong.**

> ### How solid is this note
>
> Every finding below was reached through **web search result summaries only**. The session's
> network egress policy blocked direct document retrieval — `aktuar.de`, `actuaries.jp` and
> `cran.r-project.org` all returned `EGRESS_BLOCKED`, so **no source document on this page was
> actually fetched, opened or read**. By the library's own standard every claim here is
> `[unverified]`: this note is a *ranking of where to spend the research effort*, not research
> output, and each recommended country still needs the gate probe in
> [§6](#6-before-committing-run-the-gate-probe) before a single product document is drafted.
> See [§7](#7-environment-the-research-passes-will-need) for what the research environment has
> to permit.

---

## 1. What "availability of public information" actually means here

The question is not whether a country's insurance market is documented. It is whether a
country can be carried through the [three-pass methodology](README.md#methodology) —
research, drafting, review — under the rule that **every quantitative parameter is either
source-tagged or marked `[std]`**. The uslib and uklib builds show exactly where that rule
bites, and the UK build shows what failure looks like:

> **Every decrement basis shipped here is a `[std]` proxy**, because the CMI tables that a UK
> insurer would actually use are restricted to Authorised Users and cannot be redistributed
> [...] Nor is there any public premium rate card: UK protection and annuity pricing is
> quote-driven.
> — [uklib/index.md](uklib/index.md)

That is the real constraint. uklib is a good library that has to warn its readers not to
trust its numbers, because two specific inputs were not publicly obtainable. So the candidates
are scored against six **gates**, in rough order of how badly failing one hurts:

| Gate | What it is | Why it decides the outcome |
|---|---|---|
| **G1 Product documents** | Policy conditions, brochures, key-features documents, prospectuses, freely downloadable | Without these there is no `product-spec.md`. uslib needed ~20 `[S#]` sources per product; uklib 15–26. |
| **G2 Standard wording** | A model/standard contract issued by a regulator or trade body | A short-cut straight to the *representative* product — it removes most of the "insurers differ, choose and justify" work that dominates drafting |
| **G3 Insured-lives tables** | Mortality / morbidity table obtainable **and redistributable** | The gate uklib failed. Pass it and the models ship real bases instead of `[std]` proxies |
| **G4 Price signal** | Published premium rates or payout rates | The other gate uklib failed. Lets a worked example be calibrated rather than invented |
| **G5 Prescriptive formulas** | Statutory reserve / cash-value / surplus-distribution formulas | Makes `technical-notes.md` *checkable*: the recursion has a right answer, not just a defensible one |
| **G6 Reference corpus** | Free prudential, conduct, tax and professional-standards sources | uklib's cross-product reference page carries 39 entries; uslib's is comparable. This has to exist for free |

Two modifiers sit on top: **language and long-run maintainability**, and **market weight and
product novelty** — a country only earns its place if it adds products that uslib and uklib
do not already cover.

---

## 2. Scorecard

`✔` = gate passes on the evidence found · `~` = partial or unconfirmed · `✖` = fails

| | G1 Product docs | G2 Standard wording | G3 Tables | G4 Price signal | G5 Prescriptive formulas | G6 Reference corpus | Language | Novelty vs US/UK |
|---|---|---|---|---|---|---|---|---|
| **Japan** | ✔✔ | ~ | ✔✔ | ~ | ✔✔ | ✔ | JA | high |
| **China** | ✔✔ | ✔✔ | ✔✔ | ~ | ✔✔ | ✔ | ZH | very high |
| **Hong Kong** | ✔ | ✔ | ✔ | ✔ | ~ | ✔ | **EN** | medium |
| **France** | ✔ | ~ | ✔✔ | ~ | ✔✔ | ✔✔ | FR | high |
| **Germany** | ✔✔ | ✔✔ | ~ | ~ | ✔✔ | ✔✔ | DE | high |
| **Korea** | ✔ | ✔✔ | ✖/~ | ✔ | ✔ | ✔ | KO | medium |
| **Switzerland** | ~ | ✖ | ✖ | ✖ | ~ | ✔ | DE/FR/IT | low |

---

## 3. Recommendation

**Build Japan first. Then China. Take Hong Kong whenever a cheap win is wanted — it is the
one candidate whose primary sources are already in English. France is the best European
choice, Germany the best *second* European one. Hold Korea behind a mortality-table probe.
Drop Switzerland.**

### Tier 1 — build these

**1. Japan** — *the only candidate where the statutory valuation basis itself is public.*

The Institute of Actuaries of Japan publishes the **Standard Mortality Table** (標準生命表
2018, and the 2007 and 1996 predecessors) as freely downloadable Excel files, and maintains an
English-language library page carrying `Standard_Mortality_Table.xlsx` and a
`Development_Process_of_Standard_Mortality_Table_2018.pdf`. That is not an experience study
sitting next to the real basis — under the 標準責任準備金 (standard policy reserve) regime it
**is** the table an insurer must value on, set by FSA notification. Pair it with the FSA's
published standard-reserve notifications and the reserve is not merely modelable but exactly
reproducible — precisely the `[std]`-proxy problem uklib had to disclaim, solved outright (G3, G5).

On G1 Japan is unusually rich: essentially every insurer publishes complete
**ご契約のしおり・約款** — the full policy conditions, not a summary — as free PDFs (Nippon Life,
Dai-ichi, Tokio Marine & Nichido Anshin, Japan Post Insurance, Lifenet all do). Compare with the
UK, where the equivalent took hunting through adviser-portal PDFs. G6 is covered by 保険業法 and
its enforcement ordinance on e-Gov, IAJ technical papers, and the Life Insurance Association's
統計資料 series. The regime is also *live*: the FSA's **economic-value-based solvency regulation**
(ICS-aligned, phased in from FY2025) is fully documented in free FSA papers, so a Japanese library
lands on current material rather than legacy rules.

Products that are new to this repo: 医療保険 and がん保険 (medical / cancer — morbidity products
with no US or UK analogue in scope), 収入保障保険 (income-guarantee term, a decreasing-annuity
death benefit), 学資保険 (educational endowment), 低解約返戻金型終身保険, 個人年金保険, and
外貨建保険 (FX-denominated savings with MVA — a large and distinctly Japanese book). The
`Projection` chassis carries straight over; the new content is the reserve/surrender-value
split and the dividend mechanics.

The soft factor is not small: lifelib is a Japanese-origin project, and a `jplib` reaches its
most concentrated existing audience.

*G4 is the one qualified gate.* Brochures carry 保険料例 and direct writers publish quotable
rates, but a full published rate card by age and sex was **not confirmed** — treat it as
`~` until probed.

**2. China** — *the largest volume of public primary source material of any candidate, by a wide margin.*

Three findings, each of which would be notable alone:

- The **人身保险产品信息库** (Personal Insurance Product Information Database), run by the
  Insurance Association of China at `iachina.cn`, offers free public multi-dimensional query
  and clause verification across *every* life, accident, health and annuity product filed with
  the regulator since the 2009 Insurance Law — in force and withdrawn. No other candidate has a
  national public register of actual policy wordings (G1, and effectively G2).
- The **experience tables are government-published**. The third set, 中国人身保险业经验生命表
  (2010—2013), was issued under CIRC notice 保监发〔2016〕107号; the **fourth set (2025)** was
  released on 2025-10-29 with a State Council–published notice from the NFDA, effective
  2026-01-01, comprising pension, non-pension I, non-pension II and — a first — single-life
  tables. Separately, the China Association of Actuaries publishes the **critical illness
  incidence table (2020)** with a 280-page compilation report drawn from ~2,900 products,
  ~400 million policy records and ~5.87 million claims. A **publicly published CI incidence
  basis** is something neither the US nor the UK library could obtain (G3).
- The **精算规定** series (普通型 / 分红型 / 万能型人身保险精算规定) lays down reserve, cash
  value and surplus rules as explicit formulas — e.g. the reserve floor "year-end unearned
  liability reserve shall not be less than year-end cash value plus year-end survival benefit",
  prospective per-policy valuation, and evaluation mortality keyed by name to the experience
  table. Full texts sit free on `gov.cn` (G5). On top of that, the Insurance Association's
  **重大疾病保险的疾病定义使用规范（2020年修订版）** standardises 28 CI condition definitions
  across the whole market — a standard product component, published free (G2).

Products new to the repo: 重疾险 (critical illness, on a public incidence table), 分红险
(participating, on a prescribed dividend-allocation rule), 万能险 (universal life with the
declared 结算利率 mechanism and a statutory minimum guarantee), 增额终身寿险 (increasing whole
life), and dual-account annuity designs.

Two real risks, both worth pricing in: the rules **churn fast** (pricing-rate caps moved
repeatedly through 2023–2025, and 报行合一 reshaped commission economics), so a Chinese library
dates faster than a Japanese one; and some of the highest-value hosts may be awkward to reach
from outside China — a retrieval question the gate probe must answer before drafting starts.

### Tier 2 — good, and each has one clear reason to pick it

**3. Hong Kong — the cheap win, because it is in English.** Every other candidate imposes a
translation layer on the reader; Hong Kong does not, which cuts both drafting cost and the
cost of anyone later checking the citations. And its table position is *better than the UK's*:
ASHK publishes **HKA22** (Hong Kong Assured Lives Mortality 2022 — fifth in the series, 2014–2021
study period, 13 insurers, 94% of in-force policies) as an openly-linked report PDF, alongside
HKA18, the older HKA01 tables and an assured-lives **critical illness** report. G4 is passed
outright by the government-owned **HKMC Annuity Plan**, whose public brochure carries actual
payout rates — a genuine public annuity price card, which the UK simply does not have. SFC-authorised
**ILAS** offering documents and Product Key Facts Statements sit on a public register at
prospectus grade, comparable to the SEC filings uslib leaned on. And the IA's **GN16/GL16**
regime forces every insurer to publish, per product series, the **fulfilment ratio** of actual
against illustrated non-guaranteed benefits — a public dataset for calibrating a participating
model that has no counterpart in uslib or uklib.

Against it: the smallest premium base of the seven, G5 is weaker (no statutory reserve
formula on the Chinese or Japanese scale), specimen policy contracts are often "request a
copy" rather than posted, and the flagship par-savings and high-net-worth universal life
products reuse the uslib chassis heavily — so it adds the least *new* modeling. It is the best
effort-to-output ratio here, not the best output.

**4. France — the cleanest legal position on tables of any candidate.** The regulatory
mortality tables **TH/TF 00-02** and **TGH/TGF 05** are annexed to article A.335-1 of the Code
des assurances, homologated by the arrêté of 1 August 2006 and published on Legifrance. They
are official legal texts, not a trade body's licensed intellectual property — meaning the
actual table values can in principle be **shipped in the repository**, which is exactly what
uklib could not do. The Code is likewise prescriptive on the mechanics that matter: technical
rate caps, the minimum profit participation (≥85% of financial results and ≥90% of technical
results), and the **PPB** with its eight-year release constraint (G3, G5, G6 — all free, all in
one place).

The product is genuinely different from anything in the repo: the **contrat d'assurance vie
multisupport**, a fonds euros with a capital guarantee and PPB-smoothed profit sharing running
alongside unités de compte. That is neither US participating whole life nor UK with-profits.
Add **assurance emprunteur** (creditor insurance, heavily reshaped by the Lemoine law) and the
post-PACTE **PER**, and France is a strong content addition. It sits below Japan and China only
because insurer-level product documentation is less standardised than the regulatory layer.

**5. Germany — the richest modeling content, and the highest effort.** G1, G2, G5 and G6 are
all excellent: the **GDV Musterbedingungen** are non-binding model policy conditions published
free (a representative-product short-cut of exactly the right kind); the **Produktinformationsblatt**
is mandatory under §4 VVG-InfoV with prescribed ordering, a §154 VVG model calculation and a
disclosed *Effektivkosten* figure; and DeckRV, MindZV and §§139–169 VVG give the Höchstrechnungszins
(raised to 1.00% from 2025-01-01 — the first rise in three decades), the Zinszusatzreserve, Zillmerung
and minimum-surrender-value rules as hard formulas on `gesetze-im-internet.de`.

**G3 is the reason Germany is not Tier 1.** The DAV derivation guidelines for **DAV 2008 T** and
**DAV 2004 R** are free PDFs on `aktuar.de` and the values appear in their annexes — but they are
DAV publications, and whether the tables may be *redistributed* inside a library is unresolved.
That is the CMI problem again, in a milder form, and it must be settled before Germany is
started, not after. The other cost is complexity: hybrid guarantee designs (i-CPPI, Zwei- and
Drei-Topf-Hybride), Überschussbeteiligung with Schlussüberschuss and Bewertungsreserven, and
Riester/Rürup certification make German products among the most modeling-intensive anywhere —
excellent content, but not a first country.

### Tier 3 — conditional

**6. Korea** passes almost everything except the gate that sank the UK. G2 is outstanding:
the **표준약관** (standard policy wording) for life, and for disease-and-injury, is published as
별표15 to the FSS's 보험업감독업무시행세칙 — a *regulator-issued standard contract*, free on
`law.go.kr`. G1 and G4 are solid: insurers and the Life Insurance Association are required to
publish 약관, 상품요약서, 사업방법서 and comparative premium disclosures in their 공시실.
G5 is covered by 보험업감독규정 (standard surrender values, net-premium reserves) and the public
K-ICS materials.

But **G3 is the problem**: the 경험생명표 is compiled every five years by KIDI (the 10th revision
completed November 2023), and the reference pure premium rates (참조순보험요율) are likewise KIDI
products. Free public availability of the actual mortality rates was **not confirmed** —
`bigin.kidi.or.kr` surfaced a 경험생명표 page but no open download. If those rates turn out to be
industry-distributed rather than public, Korea reproduces uklib's disclaimer exactly. Korea has
real content to offer — 무·저해지환급형 (no- and low-surrender-value designs, a live regulatory and
IFRS 17 lapse-assumption controversy), 변액보험 minimum guarantees, 실손의료보험 — so it is worth a
**one-day G3 probe**, and worth building only if that probe passes.

### Tier 4 — do not build

**7. Switzerland.** It fails on relevance before it fails on sources. The dominant Swiss life
business is **BVG occupational pensions**, which this repo explicitly scopes out as group and
institutional business; individual savings life is a small and shrinking remainder. There is no
standard wording (G2 ✖), no public rate card (G4 ✖), and Swiss actuarial tables are commercially
licensed (G3 ✖). Product documentation is fragmented across German, French and Italian, tripling
the maintenance surface for the thinnest corpus of the seven. The genuinely interesting Swiss
feature is the **SST** — and the repo already treats the capital layer as
[cited-not-specified](uklib/references/regulatory-and-actuarial-references.md), so even that
contributes little. Lowest return per unit of effort by a clear margin.

---

## 4. Recommended build order

| # | Country | Library | Why here |
|---|---|---|---|
| 1 | **Japan** | `jplib` | Public statutory valuation basis; complete policy conditions freely published; best audience fit |
| 2 | **China** | `cnlib` | Largest public source corpus anywhere — national product-clause register, government-published life *and* CI tables, formula-level actuarial regulations |
| 3 | **Hong Kong** | `hklib` | English sources, public assured-lives tables, a real public annuity price card. Cheapest per product — good to run alongside a heavier country |
| 4 | **France** | `frlib` | Mortality tables are legal texts and therefore shippable; fonds euros / PPB is genuinely new content |
| 5 | **Germany** | `delib` | Best-in-class model wordings and statutory formulas — **gated on resolving DAV table redistribution** |
| 6 | **Korea** | `krlib` | Only after the 경험생명표 access probe passes |
| — | Switzerland | — | Not recommended |

Japan and Hong Kong can proceed in parallel with little contention: they share almost no
sources, and Hong Kong's products lean on the uslib chassis while Japan's lean on new work.

---

## 5. Candidate product shortlists for the top three

Sized to match uslib (12 products) and uklib (7), and chosen for what is *not* already covered:

- **Japan (7–8):** 定期保険 (term) · 終身保険, low-surrender-value variant (whole life) ·
  養老保険 (endowment) · 収入保障保険 (income-guarantee term) · 医療保険 (medical) ·
  がん保険 (cancer) · 個人年金保険 (individual annuity) · 外貨建終身保険 (FX-denominated whole life)
- **China (6–7):** 重疾险 (critical illness) · 定期寿险 (term) · 增额终身寿险 (increasing whole
  life) · 分红险 (participating) · 万能险 (universal life) · 年金险 (annuity) · 投连险
  (investment-linked)
- **Hong Kong (5–6):** participating endowment/whole-life savings · universal life (HNW) ·
  critical illness · term · ILAS · HKMC-pattern immediate annuity

---

## 6. Before committing: run the gate probe

Do **not** open a country library on the strength of this note. For each country, spend one
day on a **single product** and answer six questions with retrieved documents:

1. **G1** — can five or more primary product documents for that one product be downloaded, in
   full, without a login? (uslib and uklib each needed 15–26 sources *per product*.)
2. **G2** — does a standard or model wording exist, and does it cover this product?
3. **G3** — can the mortality/morbidity table actually be downloaded, and what does its licence
   say about redistribution? **Read the licence, do not infer it.** This is the question that
   decides whether the library ships real bases or another `[std]` disclaimer.
4. **G4** — is there any published rate — premium, payout, or credited/declared rate?
5. **G5** — is there a statutory reserve or cash-value formula, and can it be recomputed by hand
   for one specimen policy?
6. **G6** — can 25–40 free regulatory and actuarial references be assembled, enough for a
   `references/` page on the scale of uklib's 39 entries?

A country that fails G3 can still be built — uklib was — but it must be **chosen knowingly**,
with the disclaimer written into `index.md` up front rather than discovered at review.

---

## 7. Environment the research passes will need

The research pass is retrieval-bound, and this session could not retrieve anything: `aktuar.de`,
`actuaries.jp` and `cran.r-project.org` were all refused by the egress proxy. Whichever
environment runs the actual research must permit at least these hosts:

| Country | Hosts that must be reachable |
|---|---|
| Japan | `actuaries.jp`, `fsa.go.jp`, `e-gov.go.jp`, `seiho.or.jp`, `jili.or.jp`, insurer domains (`nissay.co.jp`, `dai-ichi-life.co.jp`, `tmn-anshin.co.jp`, `jp-life.japanpost.jp`, `lifenet-seimei.co.jp`) |
| China | `iachina.cn`, `gov.cn`, `nfra.gov.cn`, `e-caa.org.cn`, insurer domains |
| Hong Kong | `actuaries.org.hk`, `ia.org.hk`, `sfc.hk`, `hkfi.org.hk`, `hkmca.hk`, `censtatd.gov.hk`, insurer domains |
| France | `legifrance.gouv.fr`, `acpr.banque-france.fr`, `institutdesactuaires.com`, insurer domains |
| Germany | `aktuar.de`, `gdv.de`, `bafin.de`, `gesetze-im-internet.de`, insurer domains |
| Korea | `law.go.kr`, `kidi.or.kr`, `klia.or.kr`, `fss.or.kr`, insurer domains |

Several sources are **PDF-only and large** (the China CI compilation report is ~280 pages; the
HKA22 report and the DAV derivation guidelines are substantial PDFs), and at least one UK source
in the existing library needed a browser user-agent to retrieve at all — so the environment needs
PDF text extraction and a user-agent that servers will serve, not just plain HTTP.

---

## 8. Sources consulted

All reached via web search result summaries; **none retrieved** — see the warning at the top.

**Japan** — [IAJ English library](https://www.actuaries.jp/english/lib/) ·
[IAJ 標準生命表](https://www.actuaries.jp/lib/standard-life-table/) ·
[FSA standard policy reserve notification amendment](https://www.fsa.go.jp/news/r2/hoken/20210423/20210423.html) ·
[FSA economic-value-based solvency regulation](https://www.fsa.go.jp/policy/economic_value-based_solvency/10.pdf) ·
[Life Insurance Association statistics](https://www.seiho.or.jp/data/statistics/) ·
[Nippon Life ご契約のしおり・約款](https://www.nissay.co.jp/kojin/shohin/seiho/mirainokatachi/shiori/01.pdf) ·
[Dai-ichi Life しおり・約款](https://dl-shiori.jp/) ·
[Lifenet 約款](https://www.lifenet-seimei.co.jp/policy/yakkan/)

**China** — [IAC 人身保险产品信息库](https://www.iachina.cn/col/col71/index.html) ·
[NFDA notice on the 2025 (fourth) experience life table](https://www.gov.cn/zhengce/zhengceku/202510/content_7046318.htm) ·
[CIRC 保监发〔2016〕107号 — CL(2010-2013)](https://www.waizi.org.cn/law/15897.html) ·
[CBIRC notice on the 2020 CI incidence table](https://www.gov.cn/zhengce/zhengceku/2020-11/06/content_5557791.htm) ·
[重大疾病保险的疾病定义使用规范（2020年修订版）](https://www.iachina.cn/art/2020/11/5/art_8616_104706.html) ·
[普通型人身保险精算规定](https://www.gov.cn/zhengce/zhengceku/2020-03/26/content_5495763.htm)

**Hong Kong** — [ASHK HKA22 report](https://www.actuaries.org.hk/storage/download/HKA22%20Report%20(final%2021%20Aug%202025).pdf) ·
[ASHK HKA22 press release](https://www.actuaries.org.hk/storage/download/Press%20Release%20-%20HKA22%20Public_eng.pdf) ·
[ASHK HKA18 report](https://www.actuaries.org.hk/storage/download/20200830%20ASHK%20Mortality%20Studies%20HKA18%20(Final)%20(Clean)_Updated.pdf) ·
[ASHK assured lives mortality and critical illness report](https://www.actuaries.org.hk/storage/download/ESR02-06.pdf) ·
[SFC Product Key Facts Statements](https://www.sfc.hk/en/Regulatory-functions/Products/List-of-publicly-offered-investment-products/Products-Key-Facts-Statements-KFS) ·
[SFC Code on ILAS](https://www.sfc.hk/-/media/EN/assets/components/codes/files-previous/web/codes/section-iii-code-on-investment-linked-assurance-schemes/2018-12-31---Section-III---Code-on-Investment-Linked-Assurance-Schemes---2018-12-31-000000.pdf) ·
[HKMC Annuity Plan brochure](https://www.hkmca.hk/eng/files/Product_brochure_E.pdf) ·
[IA GN16 fulfilment ratio commentary](https://www.lexology.com/library/detail.aspx?g=23b084d4-add0-4dde-b1c9-06df696c6821)

**France** — [Arrêté du 1er août 2006 (TGH05/TGF05 homologation)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000820127) ·
[Code des assurances art. A331-3](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006787891/2006-08-26)

**Germany** — [DAV — Herleitung DAV 2008 T](https://aktuar.de/content/PDF/Fachwissen/2022-11-29_DAV-Richtlinie_Herleitung_DAV2008T.pdf) ·
[DAV — Herleitung DAV 2004 R](https://aktuar.de/content/PDF/Fachwissen/2023-06-28_DAV-Richtlinie_Herleitung_DAV2004R.pdf) ·
[GDV Musterbedingungen](https://www.gdv.de/gdv/service/musterbedingungen) ·
[VVG-InfoV](https://www.gesetze-im-internet.de/vvg-infov/BJNR300400007.html) ·
[BaFin on VVG-InfoV](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Aufsichtsrecht/Verordnung/VVG-InfoV_va.html) ·
[§2 DeckRV Höchstzinssatz](https://www.buzer.de/gesetz/12006/a198101.htm) ·
[BaFin FAQ on the 2025 Höchstrechnungszins](https://www.bafin.de/SharedDocs/FAQs/DE/VA/Pensionskassen/01_Frage.html)

**Korea** — [보험업감독업무시행세칙 (표준약관 별표15)](https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%EB%B3%B4%ED%97%98%EC%97%85%EA%B0%90%EB%8F%85%EC%97%85%EB%AC%B4%EC%8B%9C%ED%96%89%EC%84%B8%EC%B9%99) ·
[보험업감독규정](https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%EB%B3%B4%ED%97%98%EC%97%85%EA%B0%90%EB%8F%85%EA%B7%9C%EC%A0%95) ·
[KIDI 경험생명표 (보험정보 빅데이터 플랫폼)](https://bigin.kidi.or.kr:9443/boarddetail/nd00017_6041)

**Switzerland** — [FINMA insurance market report 2024](https://www.finma.ch/en/~/media/finma/dokumente/dokumentencenter/myfinma/finma-publikationen/versicherungsbericht/20250903-versicherungsmarktbericht-2024.pdf) ·
[SVV Swiss insurance market shares](https://svv.ch/en/facts-and-figures/key-financial-figures/swiss-insurance-market-companies-and-market-shares) ·
[FINMA — life insurers authorisation](https://www.finma.ch/en/authorisation/insurers/getting-licensed/life-insurers/)
