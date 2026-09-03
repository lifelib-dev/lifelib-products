# Regulatory and Actuarial References — Korea Life Insurance

**Status:** Draft, 2026-09-03.

Curated reference library for the Korea section of the reference-product library. It covers
the prudential and supervisory (금융위원회 / 금융감독원 / 보험업법 / 시행령 / 보험업감독규정 /
보험업감독업무시행세칙), actuarial (보험개발원, 경험생명표), public-statistics,
legislation-and-conduct, public-scheme and tax-and-accounting sources that the reference
cash-flow-model implementations (whole_life / term_life / ci_insurance / child /
indemnity_medical / cancer / long_term_care / pension_savings / variable_annuity /
immediate_annuity) rely on. Product folders cite entries on this page as **[REG-R#]** (e.g.
`[REG-R1]`); the R1–R60 numbering below is **frozen** — never renumber an entry and never
reuse a number, because ten product document sets cite against it. Within this page, plain
`[R#]` refers to the same entries. Facts stated under an entry that was actually retrieved
were read from the fetched document; a claim taken from general knowledge, from a
search-result summary, or from a document that could not be opened is tagged
**[unverified]** and is a to-verify item, not an established fact. Every failed fetch is
disclosed in the entry that needed it and again in §7. No URL on this page is fabricated.
All URLs accessed **2026-09-03**.

**Regulatory architecture in one line:** the **금융위원회** (*Geumnyung-wiwonhoe*, Financial
Services Commission, FSC) makes the rules and grants the licence, the **금융감독원**
(*Geumnyung-gamdogwon*, Financial Supervisory Service, FSS) examines and writes the
implementing 세칙, and a Korean actuary works down a five-rung ladder — 법률 → 시행령
(Presidential Decree) → 시행규칙 (Prime Ministerial Rule) → **보험업감독규정** (an FSC 고시)
→ **보험업감독업무시행세칙** (an FSS 세칙) → 별표 (schedules to either) — in which nearly
every operative number lives on the last two rungs and not in the statute [R1] [R9] [R23].
**보험업법** (*Boheomeop-beop*, Insurance Business Act) governs the *undertaking*; **상법 제4편
보험** (Commercial Act, Part IV) governs the *contract*; the two have different sponsoring
ministries (금융위원회 and 법무부) and Korean practice keeps them strictly apart [R1] [R49].

**Four things make the Korean frame unlike every other library in this repository, and a
document that imports a `jplib` or `uklib` reflex will be wrong about all four.**

1. **IFRS 17 and K-ICS have both been live since 2023-01-01.** K-IFRS 제1117호 「보험계약」 is
   the Korean adoption of IFRS 17 [R60] and **K-ICS** (신지급여력제도, the Korean Insurance
   Capital Standard) is the economic-value solvency regime [R13]; both commenced in the same
   quarter, under the same 부칙 [R14]. Japan's economic-value regime commences 2026 and the
   EU's long predates IFRS 17. Korea switched liability measurement and capital measurement
   together, and is four years into living with the result.
2. **On top of them sits the 해약환급금준비금** (*haeyak-hwangeupgeum-junbigeum*, surrender
   value reserve) — a company-level appropriation inside 이익잉여금 whose whole purpose is to
   stop an IFRS 17 balance sheet from distributing earnings that the contractual
   surrender-value floor would later demand [R11]. It has no counterpart in `uslib`, `uklib`,
   `jplib`, `frlib` or `delib`. It is a **distributable-earnings** device, not a solvency
   device.
3. **제3보험** (*je-sam boheom*, "third insurance") is a statutory licence category, not a
   market label. 보험업법 제4조제1항제3호 names 상해보험, 질병보험 and 간병보험, and 제4조제3항
   deems a fully licensed life insurer *or* a fully licensed non-life insurer to hold it, so
   both sides of the market write the same 암보험 and the same 간병보험 [R1]. Four of the ten
   `krlib` products sit in it, and the surrender-value rules reach them by the *mutatis
   mutandis* cross-references of 감독규정 제7-69조 and 제7-70조 [R19].
4. **경험생명표 is an industry table that is not published in full.** 보험개발원 (Korea
   Insurance Development Institute, KIDI) releases only 평균수명 and 기대여명 summary
   statistics for the 제10회 경험생명표 applied from 2024-04; the qx table itself goes to member
   insurers [R33] [R34]. There is no Korean analogue of Japan's downloadable 標準生命表 or of
   the DAV tables documented in German Fachgrundsätze. **Every `mort_table.csv` in `krlib` is
   therefore a `[std]` construction** anchored on the public 국가데이터처 생명표 [R38] and on
   the two published KIDI summary figures [R33], carrying a `provenance` column on every row.
   The same is true of morbidity: 참조순보험요율 are filed with the FSC, never published, and
   become visible to the public only as the *ratio* called the 보험가격지수 [R4] [R22].

**Scope note on capital and reserving.** This library projects **gross best-estimate
liability cash flows**. 책임준비금 [R3] [R10], 해약환급금준비금 [R11], 보증준비금 [R10] [R26],
비상위험준비금 [R8], the K-ICS 요구자본 and its seven life sub-risks [R13], the K-ICS 경과조치
[R35] and the IFRS 17 risk adjustment and CSM [R60] are **cited, not specified** — the entries
below tell a drafter exactly what the regime requires without the library implementing any of
it, the same way `uklib` treats the SCR and `jplib` the ESR. What `krlib` *does* compute is
the **계약자적립액 / 보험료적립금** and the **해약환급금**, because those are contractual
quantities defined by the (unpublished) 산출방법서 and **bounded by a published schedule**,
별표 14 [R20]. That bound is the sharpest single difference from the US and UK libraries: in
Korea the surrender charge has a statutory cap with a formula, and it is public.

**Host behaviour observed in this session, because it determined what this page can say.**
`law.go.kr` (국가법령정보센터) serves both statutes and 행정규칙 as a JavaScript shell; a plain
fetch of `https://www.law.go.kr/법령/<name>` returns navigation chrome only. Two inner
endpoints **do** return full UTF-8 HTML — `LSW/lsInfoR.do?lsiSeq=<id>&efYd=<yyyymmdd>` for
법령 and `LSW/admRulLsInfoR.do?admRulSeq=<id>` for 행정규칙 — and the 별표, which are images
inside those pages, come as PDFs through `admRulBylContentsInfoR.do?bylSeq=<id>` followed by
`flDownload.do?flSeq=<pdfFlSeq>`. That three-step route is the only way 별표 14 [R20], 별표 15
[R21], 별표 27 [R24] and the 492-page 표준약관 [R25] were obtained, and it is the single most
useful retrieval fact in this file. `fsc.go.kr` serves server-rendered HTML and its attachment
PDFs. `fss.or.kr` refused the fetcher used for the cross-product research pass but **served
normally** to the product research passes — see the correction in §7. Where a formula in the
body of a regulation is rendered as an image rather than as text, this page records it as not
retrieved rather than paraphrasing it.

**A convention every product document inherits from this page.** 감독규정 제1-2조제2호 defines
the **기준연령 요건** as "전기납 및 월납 조건으로 **남자가 만 40세**에 보험에 가입하는 경우"
[R9]. That 40-year-old-male, monthly-premium, whole-term-pay cell is the single reference
point of Korean product regulation — the 표준해약공제액 comparison, the 보장성/저축성 test and
the 보험가입금액 scaling are all computed at it — and `krlib` makes it model point 1 wherever
the product allows.

---

## Product-relevance matrix

`x` = load-bearing (a product's documents cite the entry for a specific parameter, definition
or constraint); `(x)` = qualified or background relevance (context, framing, or a mechanic the
product names but does not model); blank = not indicated. Column key: **WL** = whole_life,
**TL** = term_life, **CI** = ci_insurance, **CH** = child, **MED** = indemnity_medical,
**CAN** = cancer, **LTC** = long_term_care, **PEN** = pension_savings, **VA** =
variable_annuity, **IA** = immediate_annuity.

| R# | Reference (short name) | WL | TL | CI | CH | MED | CAN | LTC | PEN | VA | IA |
|----|------------------------|----|----|----|----|-----|-----|-----|-----|----|----|
| R1 | 보험업법 제2조·제4조 — 보험상품 and 제3보험 | x | x | x | x | x | x | x | x | x | x |
| R2 | 보험업법 제5조·제127조·제128조 — 기초서류 | x | x | x | x | x | x | x | x | x | x |
| R3 | 보험업법 제120조 — 책임준비금 | x | x | x | x | x | x | x | x | x | x |
| R4 | 보험업법 제176조 — 참조순보험요율 | x | x | x | x | x | x | x | x | x | x |
| R5 | 보험업법 제181조·제184조 — 선임계리사 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R6 | 보험업법 제108조 — 특별계정 | | | | | | | | x | x | |
| R7 | 시행령 제1조의2 — 보험상품의 범위 | x | x | x | x | x | x | x | x | x | x |
| R8 | 시행령 제63조·제65조·제71조 | x | x | x | x | x | x | x | x | x | x |
| R9 | 보험업감독규정 — 고시 제2026-16호, 제1-2조 정의 | x | x | x | x | x | x | x | x | x | x |
| R10 | 감독규정 제6-11조 계열 — 책임준비금·보증준비금 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R11 | 감독규정 제6-11조의6 — 해약환급금준비금 | x | (x) | (x) | (x) | (x) | (x) | (x) | x | x | (x) |
| R12 | 감독규정 제6-11조의7·제6-13조 — 계약자배당 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R13 | 감독규정 제7-1조·제7-2조 — K-ICS 지급여력 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | 감독규정 제7-17조~제7-19조 and 부칙 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R15 | 감독규정 제5-6조·제5-7조·제6-26조 — 특별계정 | | | | | | | | x | x | |
| R16 | 감독규정 제7-60조 — 생명보험 상품설계 | x | x | x | (x) | | | | x | x | x |
| R17 | 감독규정 제7-63조 — 제3보험 상품설계, 실손 | | | x | x | x | x | x | | | |
| R18 | 감독규정 제7-64조·제7-65조 — 산출방법서, 공시이율 | x | x | x | x | x | x | x | x | x | x |
| R19 | 감독규정 제7-66조~제7-70조 — 해약환급금, 무·저해지 | x | x | x | x | x | x | x | x | x | x |
| R20 | 감독규정 [별표 14] 표준해약공제액 | x | x | x | x | x | x | x | x | x | x |
| R21 | 감독규정 [별표 15] 보험가입금액의 산정 | x | x | x | x | x | x | x | (x) | (x) | (x) |
| R22 | 감독규정 제4-32조·제7-45조·제7-51조 | x | (x) | (x) | (x) | x | (x) | (x) | (x) | (x) | (x) |
| R23 | 보험업감독업무시행세칙 (본문) | x | x | x | x | x | x | x | x | x | x |
| R24 | 시행세칙 [별표 27] 공시기준이율 산출 기준 | x | (x) | x | (x) | (x) | (x) | (x) | x | (x) | x |
| R25 | 시행세칙 [별표 15] 표준약관 | x | x | x | x | x | x | x | x | x | x |
| R26 | 시행세칙 [별표 22]·[별표 24] — not retrieved | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R27 | 제4차 보험개혁회의 — 계리가정·할인율 (2024-11-07) | x | x | x | x | x | x | x | x | x | x |
| R28 | 무(저)해지환급금 보험 상품구조 개선 (2019–2020) | x | x | x | x | (x) | x | x | (x) | (x) | (x) |
| R29 | 사업비·모집수수료 개편 (2019-08-01) | x | x | x | x | (x) | x | x | (x) | x | (x) |
| R30 | 자본규제 고도화 and 지급여력비율 현황 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R31 | 실손의료보험 개혁방안 (2025-04-01) | | | | (x) | x | (x) | | | | |
| R32 | 예금보호한도 1억원 (2025-09-01) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R33 | 보험개발원 제10회 경험생명표 (via 보험매일) | x | x | x | x | x | x | x | x | x | x |
| R34 | 보험개발원 공개 채널 — negative evidence | x | x | x | x | x | x | x | x | x | x |
| R35 | 보험연구원 — K-ICS 경과조치 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R36 | 보험연구원 CEO Report 03호 — 건전성 제도 | x | x | x | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R37 | 보험연구원 — 사업비 및 모집수수료 개선 (2019-04) | x | x | (x) | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R38 | 국가데이터처 생명표 (2024년, 2023년) | x | x | x | x | (x) | (x) | x | x | x | x |
| R39 | KOSIS 완전생명표 — not retrieved | x | x | x | x | (x) | (x) | x | x | x | x |
| R40 | 국가암등록통계 (2023년, 발표 2026-01-20) | (x) | | x | x | (x) | x | | | | |
| R41 | 건강보험환자 진료비 실태조사 (2024년도) | | | (x) | (x) | x | (x) | (x) | | | |
| R42 | 장기요양 등급 판정 현황 (2026-06-30) | (x) | | (x) | | (x) | | x | | | |
| R43 | 노인장기요양보험 통계연보 2024 — not retrieved | | | | | (x) | | x | | | |
| R44 | 2024년 실손의료보험 사업실적(잠정) | | | (x) | (x) | x | (x) | (x) | | | |
| R45 | 생명보험협회 공시실, FACT BOOK, 금융통계월보 | x | x | x | x | x | x | x | x | x | x |
| R46 | 보험연구원 「2026년 보험산업 전망」 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R47 | 한국보험신문 — 2025년 보험사 경영실적 | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R48 | 평균공시이율 and 공시기준이율 — carrier disclosure | x | (x) | (x) | (x) | (x) | (x) | (x) | x | x | x |
| R49 | 상법 제4편 제1장 통칙 (제638조~제664조) | x | x | x | x | x | x | x | x | x | x |
| R50 | 상법 제4편 인보험 (제727조~제739조의3) | x | x | x | x | x | x | x | x | x | x |
| R51 | 금융소비자보호법 제46조 — 청약철회 | x | x | x | x | x | x | x | x | x | x |
| R52 | 예금자보호법 시행령 제18조 — 1억원 | x | x | x | x | x | x | x | x | x | x |
| R53 | 국민건강보험법 제41조·제42조·제44조 | | | (x) | (x) | x | (x) | (x) | | | |
| R54 | 노인장기요양보험법 제2조·제15조 등 | (x) | | (x) | | (x) | | x | | | |
| R55 | 노인장기요양보험법 시행령 제7조 — 등급판정기준 | (x) | | (x) | | (x) | | x | | | |
| R56 | 소득세법 연금계좌 세액공제·연금소득 package | (x) | | | | | | | x | x | x |
| R57 | 소득세법 제59조의4 — 보장성보험료 세액공제 | x | x | x | x | x | x | x | | | |
| R58 | 저축성보험 보험차익 — 소득세법 제16조, 영 제25조 | x | | (x) | | | | | (x) | x | x |
| R59 | 상속세 및 증여세법 제8조·제34조 | x | x | (x) | (x) | | | | | (x) | (x) |
| R60 | K-IFRS 제1117호 「보험계약」 | x | x | x | x | x | x | x | x | x | x |

---

## 1. Prudential and supervisory — 보험업법, 시행령, 감독규정, 감독업무시행세칙

The five instruments in this section are the whole of Korean insurance supervision that
`krlib` touches. Read them in order: the Act says who may write what and what documents a
filing consists of; the Decree closes the product lists and sets the 100% solvency floor; the
FSC's 고시 carries every operative reserving, design and surrender rule; the FSS's 세칙 carries
the 표준약관 and the crediting-rate formula; and the 별표 to both carry the numbers.

### R1 — 국가법령정보센터 (법제처), 보험업법 제2조 (정의) and 제4조 (보험업의 허가)

- Version: [시행 2025. 1. 31.] [법률 제20436호, 2024. 9. 20., 타법개정]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes — the whole Act, 127,346 characters of extracted text, through the
  `LSW/lsInfoR.do` body endpoint. The friendly URL `https://www.law.go.kr/법령/보험업법`
  returns only the navigation shell. Cross-checked article by article against the CaseNote
  mirror `https://casenote.kr/법령/보험업법/제4조` and `…/제2조`, which agreed in every
  particular.
- **What it establishes:**
  - **제2조제1호** defines 보험상품 as "위험보장을 목적으로 우연한 사건 발생에 관하여 금전 및
    그 밖의 급여를 지급할 것을 약정하고 대가를 수수(授受)하는 계약" and splits it three ways:
    **가. 생명보험상품** (survival or death of a person); **나. 손해보험상품** — indemnity for
    loss from a fortuitous event, expressly **excluding** "다목에 따른 질병ㆍ상해 및 간병";
    and **다. 제3보험상품** — "위험보장을 목적으로 사람의 질병ㆍ상해 또는 이에 따른 간병에
    관하여" a payment. 제2조제5호 then defines 제3보험업 as the business of dealing in them.
  - The carve-out in 나목 is the structural point: Korea does **not** treat sickness, injury
    and nursing care as a sub-species of indemnity insurance, it makes them a third category
    of their own. There is no US, UK, French or German parallel; the closest is Japan's
    第三分野, which is a licence *scope* rather than a product *class*.
  - **제4조제1항** requires a licence 보험종목별로 and lists them: 제1호 생명보험업 — 가.
    생명보험 나. 연금보험(퇴직보험을 포함한다) 다. 그 밖에 대통령령으로 정하는 보험종목;
    제2호 손해보험업 — 화재, 해상(항공ㆍ운송 포함), 자동차, 보증, 재보험, and Decree
    additions; **제3호 제3보험업 — 가. 상해보험 나. 질병보험 다. 간병보험** 라. Decree
    additions.
  - **제4조제3항** is the provision that makes 제3보험 a shared field: a person licensed for
    *all* the 생명보험업 종목, or for *all* the 손해보험업 종목 excluding 보증보험 and 재보험,
    "제3보험업에 해당하는 보험종목에 대한 허가를 받은 것으로 본다". Both a life and a
    non-life insurer may therefore write the same 암보험 or 간병보험, and in practice both do.
  - 제4조제6항 restricts licensees to 주식회사, 상호회사 and 외국보험회사, and treats a
    licensed foreign branch as a 보험회사 under the Act.
- **Used by:** every product, for the taxonomy sentence in `product-spec.md`. whole_life,
  term_life, pension_savings, variable_annuity and immediate_annuity are **생명보험상품**;
  indemnity_medical, cancer and long_term_care are **제3보험상품**; ci_insurance and child are
  composites — a 생명보험 주계약 with 제3보험 특약, or the reverse — which 제4조제3항 is what
  makes possible. The market-overview paragraph in `index.md` cites 제4조제3항 for why Korean
  personal protection is written on both sides of the market.

### R2 — 국가법령정보센터, 보험업법 제5조·제127조·제128조·제128조의2·제128조의3 (기초서류)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (same full-Act retrieval as [R1]; 제5조 additionally cross-checked at
  https://casenote.kr/법령/보험업법/제5조)
- **What it establishes:**
  - **제5조제3호** names the **기초서류** a licence application must attach: "**사업방법서,
    보험약관, 보험료 및 해약환급금의 산출방법서**" — three documents, alongside the 정관 and a
    three-year business plan with projected financial statements. That is what a Korean
    product filing consists of.
  - **제127조제1항**: "보험회사는 취급하려는 보험상품에 관한 기초서류를 작성하여야 한다."
    제127조제2항 makes prior notification to the FSC the **exception**, not the rule — required
    only where a new product is introduced or made compulsory by legislation (제1호) or where
    the Decree so provides for policyholder protection (제3호).
  - **제128조** lets the FSC require FSS verification of a filing and lets it require a
    verification certificate from the 보험요율 산출기관 or an 독립계리업자 on the 보험료 및
    해약환급금 산출방법서. **제128조의2** requires every insurer to maintain a
    **기초서류관리기준** covering drafting procedure, internal and external verification, error
    control and the 선임계리사's role. **제128조의3** sets the drafting principles: no
    illegality, no unjustified reduction of policyholder rights, conformity to FSC standards.
- **What follows for provenance, and it governs the whole library.** The **산출방법서** is
  where the 예정이율, the 예정위험률, the 예정사업비율 and the surrender-value formula actually
  live, and it is **not published**. Only the 약관, the 상품요약서 and the 공시 disclosures are.
  Every pricing-basis parameter in `krlib` is therefore `[std]`, and every contractual
  parameter is sourced from a public 약관 or 상품요약서 with an `[S#]` tag. This is the same
  position `jplib` reaches from 保険業法第4条 and for the same reason.
- **Used by:** every product, in the provenance paragraph of `sources.md` and in the
  assumption tables of `technical-notes.md`.

### R3 — 국가법령정보센터, 보험업법 제120조 (책임준비금 등의 적립)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** 제120조제1항 — "보험회사는 결산기마다 보험계약의 종류에 따라
  대통령령으로 정하는 **책임준비금**과 **비상위험준비금**을 계상(計上)하고 따로 작성한 장부에
  각각 기재하여야 한다." 제2항 delegates the mechanics to a 총리령; 제3항 lets the FSC set
  accounting standards for their proper recognition. The statute carries **no method and no
  rate**: the whole content sits downstream, in 시행령 제63조 [R8] and 감독규정 제6-11조 [R10],
  and — for the Korea-specific overlay — in 감독규정 제6-11조의6 [R11]. This is the hook on
  which the entire post-2023 reserving chain hangs, and `krlib` cites the chain rather than
  stating a formula of its own.
- **Used by:** every product, in the "what this model does not compute" paragraph of
  `technical-notes.md`.

### R4 — 국가법령정보센터, 보험업법 제176조 (보험요율 산출기관)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** insurers may, with FSC authorisation, establish a **보험요율
  산출기관** — in fact **보험개발원** (KIDI) — whose statutory tasks under 제176조제3항 are
  "순보험요율의 산출ㆍ검증 및 제공", the collection of insurance information and statistics, and
  research. A rate the bureau files with the FSC is a **참조순보험요율**, and an insurer
  applying it "순보험료에 대하여 제127조제2항 및 제3항에 따른 신고 또는 제출을 한 것으로 본다"
  — deemed to have filed (제176조제6항). 제176조제9항 lets the bureau publish "순보험요율 산출에
  관한 자료" where policyholder protection requires it.
- **What follows:** the deeming provision is why a small Korean insurer can write a full
  health portfolio without its own experience, and the absence of any publication obligation
  is why **no 참조순보험요율 value was retrieved and none exists in public** [R34]. Every
  morbidity, incidence and disability rate in `krlib` is consequently `[std]`, constructed
  from public epidemiology [R40] [R41] [R42] and marked as such at the point of use.
- **Used by:** every product, in the morbidity/mortality provenance note. cancer,
  ci_insurance, long_term_care and child lean on it hardest, because for them there is no
  public rate of any kind.

### R5 — 국가법령정보센터, 보험업법 제181조 (보험계리) and 제184조 (선임계리사의 의무 등)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:**
  - **제181조제1항** requires an insurer to carry out 보험계리 — defined in the article itself
    as "기초서류의 내용 및 배당금 계산 등의 정당성 여부를 확인하는 것" — by employing
    보험계리사 or by outsourcing to a 보험계리업자. **제181조제2항** requires the appointment of
    a **선임계리사**, described since the 2022-12-31 amendment as the actuary who "보험계리에
    관한 업무 전반을 관리하고 이를 검증 및 확인하는 등 보험계리 관련 업무를 총괄하는" — a
    widening from verification to management of the whole actuarial function.
  - **제184조제1항**: "선임계리사는 기초서류의 내용 및 보험계약에 따른 배당금의 계산 등이
    정당한지 여부를 검증하고 확인하여야 한다." 제2항 adds duties to check compliance with the
    기초서류관리기준, to report breaches to the board, and to report any statutory breach in the
    기초서류 **to the FSC**.
  - **제184조제4항** gives the office tenure: once appointed the 선임계리사 may not be dismissed
    until the end of three consecutive business years following the year of appointment,
    subject to four exceptions (leaking secrets, negligence causing loss, improper demands or
    pressure, an FSC dismissal demand under 제192조).
  - **제184조제7항**, new in 2022, bars the 선임계리사 from three jobs — direct product
    development (verification excepted), CEO and CFO, plus any conflicted role the Decree
    names. This is a hard separation of pricing from sign-off, and it is stricter than the
    UK Actuarial Function / Chief Actuary split.
- **Used by:** every product, as background in `sources.md`; no model implements anything from
  it. Cited in the library index for the sentence about who signs a Korean product off.

### R6 — 국가법령정보센터, 보험업법 제108조 (특별계정의 설정ㆍ운용)

- Version: [시행 2025. 1. 31.] [법률 제20436호]
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131
- Accessed: 2026-09-03
- Retrieved: yes (full-Act retrieval)
- **What it establishes:** the statutory permission for an insurer to set up and operate a
  **특별계정** (separate account) for contract classes the Decree names, keeping their assets
  and results apart from the general account. The operative list, the permitted transfers and
  the 계약자적립금 rule are all in 감독규정 제5-6조, 제5-7조 and 제6-26조 [R15]; the statute is
  the enabling provision only.
- **Used by:** variable_annuity, for which the separate account is the product; and
  pension_savings, because a 연금저축계좌 established under 소득세법 제20조의3제1항제2호 is a
  **mandatory** 특별계정 class under 감독규정 제5-6조제1항제1호 [R15] — the single most
  important structural fact about `Pension_KR_A`.

### R7 — 국가법령정보센터, 보험업법 시행령 제1조의2 (보험상품)

- Version: [시행 2026. 4. 21.] (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421
- Accessed: 2026-09-03
- Retrieved: yes (153,076 characters)
- **What it establishes:** the Decree closes the three lists the Act opened [R1].
  - **생명보험상품** is 생명보험계약 and 연금보험계약(퇴직보험계약을 포함한다) — **two**
    contract types only (제1조의2제2항).
  - **손해보험상품** is a list of fourteen: 화재, 해상, 자동차, 보증, 재보험, 책임, 기술, 권리,
    도난, 유리, 동물, 원자력, 비용, 날씨 (제3항).
  - **제3보험상품** is exactly three: **상해보험계약, 질병보험계약, 간병보험계약** (제4항).
  - **제1조의2제1항 excludes six public schemes from "보험상품" altogether**: 고용보험,
    **국민건강보험**, 국민연금, **노인장기요양보험**, 산업재해보상보험 and 선불식 할부계약.
- **Why the exclusion matters more than the lists.** Two of the six excluded schemes are
  precisely the public layers that `Medical_KR_S` and `LTC_KR_S` sit on top of. The Decree is
  explicit that the private product is a different animal from the public one — so a `krlib`
  document may describe 실손의료보험 as a reimbursement layer above 국민건강보험 [R53], and
  간병보험 as paying on a 노인장기요양보험 grade [R54], without any suggestion that the two are
  the same instrument.
- **Used by:** every product for the taxonomy; indemnity_medical and long_term_care for the
  public-scheme boundary paragraph.

### R8 — 국가법령정보센터, 보험업법 시행령 제63조·제65조·제71조

- Version: [시행 2026. 4. 21.] (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제63조제1항, as amended 2022-12-27, restates the reserve in IFRS 17 vocabulary**: 1.
    **보험계약부채**, being the sum of 가. **발생사고요소** ("매 결산기 말 현재 보험계약상
    지급사유가 발생한 보험금등을 지급하기 위해 미래현금흐름에 대한 **현행추정치**를 적용하여
    적립한 금액") and 나. **잔여보장요소** (the same, for benefits whose trigger has not yet
    occurred); 2. **투자계약부채**, for contracts in the legal form of insurance that fall
    outside K-IFRS 1117 and are classified as investment contracts; 3. anything else the FSC
    prescribes on a current-estimate basis. 제63조제4항 keeps **비상위험준비금** for **non-life
    business only**, within 50% of the year's premiums (150% for 보증보험) — so it is not a
    life-side item and `krlib` does not model it.
  - **제65조제1항** defines the three solvency quantities: **지급여력금액** (available
    capital), **지급여력기준금액** (required capital) and **지급여력비율** = the first divided
    by the second. **제65조제2항제1호, as amended 2026-04-21, states the requirement in one
    line: "지급여력비율은 100분의 100 이상을 유지할 것".** 제65조제2항제3호 is the delegation
    under which the 해약환급금준비금 [R11] is required.
  - **제71조제1항** sends 법 제127조제2항제3호 to 별표 6; **제71조제2항** requires the
    보험상품신고서 to be filed **30 days before the sale-start date** (15 days where it follows
    an FSC recommendation), with two attachments — the 기초서류 verified by the **선임계리사**
    under 법 제184조제1항, and, where premiums, surrender values or 위험률 change, a
    verification certificate from the 보험요율 산출기관 or an 독립계리업자.
- **Used by:** every product. The 100% floor is quoted in each `product-spec.md` solvency
  note; the 30-day pre-filing is quoted in `sources.md` to explain why a Korean product's
  parameters become public at launch and not before.

### R9 — 금융위원회, 보험업감독규정 (금융위원회고시 제2026-16호)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호, 2026. 5. 6., 일부개정].
  Comparison version also retrieved: [시행 2023. 3. 2.] [금융위원회고시 제2023-10호]
  (admRulSeq 2100000220196, 207,084 characters), used only to date 2023–2026 amendments.
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes — 226,083 characters of extracted text, the whole 고시, through the
  행정규칙 body endpoint. **Formulas that the page renders as images did not extract**; each is
  recorded as a gap at the entry that needed it and again in §7.
- **What it establishes (the definitions the rest of this page uses):** 제1-2조 —
  - **제1호 참조순보험요율**: "법 제176조제4항 및 영 제87조제1항에 따라 **보험요율산출기관이
    금융위에 신고한 위험률**".
  - **제2호 기준연령 요건**: "전기납 및 월납 조건으로 **남자가 만 40세**에 보험에 가입하는
    경우", with the mid-point issue age where a 40-year-old male cannot buy the product or the
    product is age-terminating (including 종신보험 and 연금보험), and the longest available
    payment term where whole-term pay is unavailable.
  - **제3호 보장성보험 / 제4호 저축성보험**, distinguished at the 기준연령 요건 by whether the
    maturity value exceeds premiums paid — the same economic test 소득세법 제59조의4 uses
    [R57].
  - **제6호 금리연동형보험** (the 계약자적립액 rate varies with the insurer's investment return
    and market rates) and **제7호 금리확정형보험** (it is fixed).
  - **제13호 평균공시이율**: the average of all insurers' 공시이율, computed as the FSS
    Governor prescribes.
  - **제17호 최적기초율** (best-estimate bases) and **제18호 참조순보험료**: "평균공시이율,
    **평균해지율** 및 참조순보험요율을 적용하여 계산한 순보험료… 참조순보험요율이 없는 경우에는
    제17호의 최적위험률을 보수적으로 할인ㆍ할증한 위험률을 사용한다" (신설 2012-02-28, 개정
    2023-06-27). The 2023 amendment **added 평균해지율 to the inputs** — a direct consequence
    of the lapse-assumption controversy of [R27] [R28].
  - **요구자본** and **충격시나리오방식**, the K-ICS vocabulary of [R13].
- **Drift worth recording** [comparison version]: the filing document is renamed from "보험료
  및 **책임준비금** 산출방법서" to "보험료 및 **해약환급금** 산출방법서" in 제7-69조 and
  제7-70조 between 2023 and 2026 — the visible trace of a regime in which the reserve is no
  longer a locked-in contractual quantity and the surrender value still is.
- **Used by:** every product. 기준연령 요건 is quoted in every `technical-notes.md` to justify
  model point 1; 보장성/저축성 in every `product-spec.md`.

### R10 — 금융위원회, 보험업감독규정 제6-11조, 제6-11조의4, 제6-11조의5 (책임준비금의 적립, 적정성 검증, 보증준비금)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; the calculation itself is delegated and not in the 고시)
- **What it establishes:**
  - **제6-11조** splits 책임준비금 into 보험계약부채, 재보험계약부채 and 투자계약부채; 제2항
    splits each of the first two into 잔여보장요소 and 발생사고요소, with the rule that where a
    portfolio's two components sum below zero the balance is presented as a **보험계약자산**.
    제3항 defines 투자계약부채 as the measured value of contracts "보험계약의 법률적 형식을
    취하고 있으나, 한국채택국제회계기준 제1117호의 적용을 받지 않아 투자계약으로 분류된
    계약들". **제4항 delegates the detailed calculation to the FSS Governor** — i.e. to the
    시행세칙 and its 별표 [R23] [R26].
  - **Ten paragraphs of the old 제6-11조 (⑤ to ⑩) were deleted on 2022-12-21.** That deletion
    is the visible trace of the switch from a locked-in statutory reserve to a
    current-estimate one: before 2023 the 고시 itself carried accumulation rules, after 2023 it
    carries a taxonomy and a delegation.
  - **제6-11조의4** requires a **책임준비금 적정성 검증보고서** within six months of the
    financial-year end, on a form the FSS Governor sets.
  - **제6-11조의5** requires a **보증준비금** inside retained earnings for expected losses on
    benefit guarantees, and 제2항 makes it explicitly junior: "보증준비금은 제6-11조의6에 따른
    **해약환급금준비금을 적립한 후에** 적립하여야 하며, 이익잉여금에서 … 해약환급금준비금을
    차감한 금액을 한도로 한다."
- **Used by:** every product for the reserving-scope note; variable_annuity load-bearing,
  because the ordering in 제6-11조의5제2항 means the surrender-value reserve is taken **first**
  and the guarantee reserve second — which is the opposite of the intuition a drafter brings
  from a market where guarantee reserves are liabilities.

### R11 — 금융위원회, 보험업감독규정 제6-11조의6 (해약환급금준비금)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제2항 단서 amended 2025-06-11
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text in full)
- **What it establishes.** This is the Korea-specific layer with no counterpart anywhere else
  in this repository, so it is given at length.
  - **Legal chain**: 보험업법 제120조 [R3] → 시행령 제65조제2항제3호 [R8] → 감독규정
    제6-11조의6 (life) and 제6-18조의6 (non-life).
  - **제1항**: "보험회사는 영 제65조제2항제3호에 따라 보험계약 해지에 대한 위험을 고려하여
    **보험회사 전체단위로** 해약환급금준비금을 산출하여 적립 또는 환입한다" — a
    **company-level** calculation, not a contract-level or portfolio-level one.
  - **제2항 sets the test.** At each balance-sheet date, including quarterly interim closes,
    for in-force contracts, compare **제1호** — 책임준비금 restricted to the 잔여보장요소 of
    보험계약부채 and 재보험계약부채 plus 투자계약부채, net of the 잔여보장요소 of any
    보험계약자산 and 재보험계약자산 and of investment-contract policy loans, **plus** 특별계정부채
    limited to the 계약자적립금 of 제6-26조제1항제1호, grossed up for unrealised gains and
    losses on those contracts recognised in OCI before tax — against **제2호**, the
    **해약환급금 computed under 제7-66조제1항** (on that rule **even for the 제7-66조제4항
    products that may contractually pay less**) **plus** the 미경과보험료 of 제7-66조제5항,
    adjusted for policy-loan balances drawn and amounts to be settled with reinsurers on
    surrender. Where 제1호 < 제2호, the shortfall is appropriated to a **해약환급금준비금 inside
    이익잉여금**.
  - **제2항 단서, amended 2025-06-11**: "다만, 직전 분기말 경과조치 적용 전 지급여력비율이
    **130% 이상**인 경우 제3호의 금액을 적립한다", 제3호 being "그 차액에 **100분의 80**을
    곱하여 산출한 금액". A well-capitalised insurer — measured on the K-ICS ratio **before**
    transitional measures at the previous quarter-end — appropriates only 80% of the shortfall.
    This is a solvency-conditioned distributable-earnings rule and it is new; the 2023 text
    carried no such relief.
  - **제3항**: where the insurer carries an 미처리결손금 the appropriation starts only once that
    deficit is cleared, and any excess over the required balance is released. **제4항**: under a
    공동재보험계약 the cedant and the reinsurer each hold the reserve in proportion to the ceded
    share.
  - **Transitional**: the 부칙 to 금융위원회고시 제2022-53호 (2022-12-22, in force 2023-01-01)
    lets insurers that adopted K-IFRS 1117 early compute the reserve for the first year of
    application **for corporate-tax purposes**, with an external audit-firm verification and a
    별지 제26호 「해약환급금준비금 산출명세서」 filed with the FSS and reported to the board.
- **Why it exists, stated plainly.** Under IFRS 17 a profitable in-force block can carry a
  liability materially below the aggregate contractual surrender value, because the CSM is a
  liability that unwinds into profit rather than a cash obligation. Distributing the resulting
  retained earnings would leave the insurer short if policyholders actually surrendered. The
  해약환급금준비금 quarantines the difference. It sits in 이익잉여금 and is therefore **inside**
  K-ICS 가용자본, unlike a genuine liability — a distributable-earnings device, not a solvency
  device.
- **Scale and the K-ICS-graded accumulation ratio** are in [R36], which quotes the 감독규정 부칙
  schedule; the reserve stood at **₩23.7조 at end-2022 and ₩32.2조 at end-2023**.
- **Used by:** whole_life, pension_savings and variable_annuity load-bearing — in each the gap
  between 계약자적립액 and IFRS 17 liability is the whole point of the earnings profile, and the
  무·저해지 forms [R19] [R28] make that gap negative in the early years and steeply positive
  after 납입완료, which is exactly the shape the reserve was built to catch. Every other product
  cites it once, in the scope note. **No `krlib` model computes it.**

### R12 — 금융위원회, 보험업감독규정 제6-11조의7 and 제6-13조 (계약자배당)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제6-11조의7** splits the dividend-related reserves three ways — 계약자배당준비금,
    계약자이익배당준비금 and 배당보험손실보전준비금. The 2026 text subdivides 계약자배당준비금
    into **금리차보장준비금, 총괄배당준비금, 장기유지특별배당준비금** and **재평가특별배당
    준비금**; the 2023 text had a five-way subdivision naming **위험률차배당준비금,
    이자율차배당준비금 and 사업비차배당준비금** separately, since collapsed into 총괄배당준비금.
    The Korean three-source vocabulary (위험률차 / 이자율차 / 사업비차 — the direct analogue of
    Japan's 三利源) was therefore **regulatory language until recently and is no longer**; it
    survives in practice and in older filings. `krlib` may use the vocabulary and must not
    attribute it to the current regulation.
  - **제6-13조제1항** is the surplus-sharing rule for life insurers: after setting the
    책임준비금 the residual (계약자배당준비금적립전잉여금) is split into 유배당보험손익,
    무배당보험손익 and 자본계정운용손익; the second and third go wholly to shareholders, and of
    the **유배당보험이익 the shareholder share is capped at 100분의 10**. 제3항 ring-fences the
    policyholder share to dividends and to the 배당보험손실보전준비금. **제6-13조제4항** makes a
    shareholder dividend conditional on the **지급여력비율 being 100% or more at the year end**.
  - Interest added to a declared but unpaid dividend must be at least the **prior year's
    평균공시이율** [R48].
- **Market fact carried with it:** Korean retail protection business is overwhelmingly
  **무배당** (non-participating). Every product name in the 표준약관 illustrations [R25] and in
  the carrier disclosures examined carries 무배당; 유배당 survives mainly in legacy annuity
  blocks. **`krlib` models no dividend, and each `product-spec.md` says so and cites this
  entry.**
- **Used by:** every product, one line each.

### R13 — 금융위원회, 보험업감독규정 제7-1조, 제7-2조, 제7-2조의2 (K-ICS 지급여력)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; **the 기본요구자본 aggregation formula renders as an image and
  did not extract** — see §7)
- **What it establishes:**
  - **제7-2조의2** sets the balance sheet the ratio is computed on — the **건전성감독기준
    재무상태표**, which is (1) based in principle on the K-IFRS consolidated balance sheet and
    (2) measured "경제적이고 시장가격과 일관된 가치로", assets at exit price and liabilities at
    transfer or settlement price, with **no adjustment for the insurer's own credit standing**.
    That last exclusion is the standard economic-value convention and matches Solvency II.
  - **제7-1조** builds 지급여력금액 as 순자산 on that balance sheet plus loss-absorbing liability
    items, less non-loss-absorbing assets, and — 제2항, new in 2022 — classifies the total into
    **기본자본** (tier 1) and **보완자본** (tier 2) by loss-absorbing capacity, with 제4항
    capping 보완자본 at **50% of the 지급여력기준금액**.
  - **제7-2조제1항** builds 지급여력기준금액 as **기본요구자본 − 법인세조정액 + 기타요구자본**,
    where 기본요구자본 aggregates five risk amounts through a correlation formula the FSS
    Governor sets: **생명ㆍ장기손해보험위험액, 일반손해보험위험액, 시장위험액, 신용위험액,
    운영위험액**.
  - **제7-2조제2항 decomposes the life and long-term-health module into seven sub-risks**, each
    with its stated measurement method: 1. **사망위험액** (net asset value falls when mortality
    rises) — 충격시나리오방식; 2. **장수위험액** (falls when mortality *falls*) — shock; 3.
    **장해ㆍ질병위험액** — shock; 4. **장기재물ㆍ기타위험액** — shock; 5. **해지위험액** —
    "보험계약자의 옵션행사율 변화 또는 보험계약 대량해지", shock; 6. **사업비위험액** — shock;
    7. **대재해위험액** (epidemics, mass accidents) — **위험계수방식**.
  - 제7-2조제4항 decomposes 시장위험액 into 금리, 주식, 부동산, 외환 (all shock) plus
    **자산집중위험** (factor); 제5항 and 제6항 make 신용위험액 and 운영위험액 factor-based;
    제7항 permits either the **표준모형** or an approved **내부모형**.
- **Direct relevance to `krlib`:** sub-risks 1, 2, 3, 5 and 6 map one-for-one onto the
  decrements and expense assumptions the ten models carry. A `krlib` sensitivity section should
  name the K-ICS sub-risk its sensitivity corresponds to, because that is the vocabulary a
  Korean actuary uses. **해지위험액** in particular is why the 무·저해지 lapse assumption is a
  supervisory issue and not only an earnings issue — the shock magnitudes are in 시행세칙 별표
  22, which was not retrieved [R26] and is quoted only at second hand from [R36].
- **Used by:** every product, in the sensitivity paragraph of `technical-notes.md`. **No
  `krlib` model computes 요구자본.**

### R14 — 금융위원회, 보험업감독규정 제7-17조~제7-19조 (적기시정조치) and the 부칙 to 금융위원회고시 제2022-53호

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 부칙 of 고시 제2022-53호 dated
  2022-12-22, in force 2023-01-01
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제7-17조제1항제1호**: the FSC **must** issue a 경영개선권고 where "지급여력비율이 **50%
    이상 100% 미만**인 경우", or on stated 경영실태평가 grade combinations. 제7-17조제2항's
    measures include capital increase or reduction, expense cuts, branch rationalisation,
    limits on fixed assets, disposal of impaired assets, staff and organisational change, and
    **a restriction on shareholder or policyholder dividends**. 제7-18조 (경영개선요구) and
    제7-19조 (경영개선명령) are the next two rungs.
  - **The commencement 부칙** is where K-IFRS 1117 and K-ICS both start: the 감독규정's IFRS 17
    articles commence **2023-01-01**. The same 부칙 carries the 해약환급금준비금 first-year
    corporate-tax provision [R11] and, at **제4조제1항**, the **five-year 적기시정조치
    deferral** — the FSC may defer 제7-17조제1항제1호, 제7-18조제1항제1호 or 제7-19조제1항제2호
    **until the 2027-12-31 closing** for an insurer whose post-transitional K-ICS ratio at the
    first post-commencement balance-sheet date was below 100%, provided the ratio under the
    **old** regime would not have triggered them, a 경영개선협약 is signed with the FSS Governor,
    and compliance is reported quarterly; 제2항 requires cancellation on breach.
  - The same 부칙 accumulates the transition-date 변액보험 guarantee reserve at the pricing
    interest rate and, for 변액보험, at "매 사업연도별 해당시점의 평균공시이율" [R48].
- **Used by:** every product, in the "both regimes commenced 2023-01-01" sentence;
  variable_annuity additionally for the guarantee-reserve roll-forward rate.

### R15 — 금융위원회, 보험업감독규정 제5-6조, 제5-7조, 제6-26조 (특별계정)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes:**
  - **제5-6조제1항 requires a 특별계정 for six contract classes**: 1. contracts establishing a
    **연금저축계좌** under 소득세법 제20조의3제1항제2호; 2. 근로자퇴직급여 보장법 제29조제2항
    retirement-pension contracts (other than 퇴직연금실적배당보험) and legacy 퇴직보험; 3.
    **변액보험계약 written by a life insurer**, and 퇴직연금실적배당보험; 4. (deleted); 5.
    **장기손해보험 written by a non-life insurer**; 6. **자산연계형보험** other than those
    applying the 공시이율.
  - **제5-6조제3항**: a life insurer's 변액보험 may be run as **two or more 집합투자기구**,
    excluding PEF-type vehicles — the legal form of the fund menu.
  - **제5-6조제5항**: what goes into the separate account is the **적립 보험료** — "영업보험료
    에서 위험보장에 필요한 부분과 사업비 등 기초서류에서 정한 사항을 차감한 금액" — and its
    investment return. This is precisely the `av_pp` recursion `VA_KR_S` implements: gross
    premium, less risk charge, less expense charge, accumulated at the fund return.
  - **제5-6조제6항**: for classes 1 and 5 the applied rate follows the **공시이율** machinery of
    제7-65조제3항 [R18] — so a **연금저축보험 is a separate-account product whose account credits
    at the 공시이율**.
  - **제5-7조** lists the only permitted transfers between separate and general accounts:
    premium receipt and benefit/dividend/refund payment; transfer to the general account of
    amounts needed for risk cover and for acquisition, maintenance and administration;
    management fees, loans and repayments; bond settlement; **covering a separate-account
    deficit out of the general account's shareholder equity**; and anything else necessary to
    maintain the account.
  - **제6-26조**: the separate-account 계약자적립금 for 변액보험 is the **whole** profit or loss
    arising in that account in the year, appropriated to the contract; for 원리금보장형 it is
    the amount computed under the general account's 산출방법서.
- **Used by:** variable_annuity (the account recursion and the fund menu) and pension_savings
  (the mandatory separate account and the 공시이율 credit).

### R16 — 금융위원회, 보험업감독규정 제7-60조 (생명보험의 보험상품설계 등)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제7호 and 제10호 신설 2022-12-22,
  제3의2호 신설 2023-06-27
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes** — the design rules a Korean life product must satisfy:
  - **제2호**: for a 저축성보험 the survival benefit must **exceed premiums paid**, except for an
    annuity paying a 생존연금 and for 변액보험.
  - **제3호 and 제4호** — the 평균공시이율 accumulation test: the 계약자적립액 accumulated at the
    평균공시이율 must exceed premiums paid at 납입완료 (seven years where the payment term is
    seven years or more, fifteen months for single premium); for a whole-life 생존연금 or a
    연금저축보험 the test may be run at **평균공시이율 + 0.25%p**; and 제4호 requires the risk
    premium, guarantee charge and separate-account management fee to be set to **zero** in that
    test.
  - **제3의2호** (신설 2023-06-27) exempts an annuity product whose 계약자적립액 or annuity
    amount at the annuity commencement date, computed at the 평균공시이율, exceeds that of a
    제3호-compliant design, provided the two are compared and explained to the customer.
  - **제7호**: **변액보험 and 금리연동형보험 (other than annuities) must set a 최저사망보험금**.
  - **제8호**: except where severe injury or disease makes cover impracticable, a contract must
    **not be extinguished** while the risk it covers remains effective. This is the rule behind
    Korean cancer and CI products that continue after a diagnosis payment rather than
    terminating.
  - **제9호**: the **death benefit must be at least cumulative premiums paid**, except after
    annuity payments have begun and except where the premium-paying period ends at age 80 or
    below.
  - **제10호** (신설 2022-12-22): **금리연동형보험 must set a 최저보증이율 or a 최저보증금액.** A
    Korean interest-sensitive product is therefore *required by regulation* to carry a
    guaranteed floor; its level is a company matter and is not published.
- **Used by:** whole_life, term_life, ci_insurance, pension_savings, variable_annuity and
  immediate_annuity load-bearing; child in part. 제8호 is cited by ci_insurance and cancer for
  the continue-after-diagnosis design; 제10호 by whole_life and pension_savings for the
  최저보증이율.

### R17 — 금융위원회, 보험업감독규정 제7-63조 (제3보험의 보험상품설계 등), as amended 2026-05-06

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제2항제2의3호 신설 2026-05-06
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text in full; the co-payment amounts below were read from it and
  cross-checked against the 표준약관 [R25])
- **What it establishes:**
  - **제7-63조제1항제1호** — a 제3보험 product must be designed so that, **on death from a cause
    the policy does not cover**, the **계약자적립액** and the 미경과보험료 of 제7-66조제5항 are
    paid and the contract terminates. This single rule is why `Cancer_KR_S`, `LTC_KR_S`,
    `Medical_KR_S` and `Child_KR_S` all need an account balance even though they are not
    savings products, and it is a **first-order modelling requirement**: a `krlib` 제3보험 model
    must have a defined payment on non-covered death. 제7-61조 applies the whole of 제7-63조 to
    **장기손해보험**, so a non-life insurer's long-term health product is designed identically.
  - **제7-63조제2항 is the 실손의료보험 rule set**, and the 2026-05-06 amendment is the fifth
    generation:
    - **제2호 — 기본형 실손의료보험(급여)**. 입원: pay **80% of the 본인부담금** (a 20%
      co-payment), the deducted amount capped at **₩2,000,000 (200만원) a year**, the excess
      reimbursed within the sum insured. 통원, per visit: deduct the greater of **₩20,000
      (2만원)**, 20% of covered cost, or the **건강보험 본인부담률** at a 전문요양기관,
      상급종합병원 or 종합병원; and the greater of **₩10,000 (1만원)**, 20%, or the 건강보험
      본인부담률 elsewhere.
    - **제2의2호 — 실손의료보험 특별약관1 (중증 비급여)**. 입원: deduct **30%**; where the
      deduction on care at a 종합병원 or 상급종합병원 exceeds **₩5,000,000 (500만원) a year**,
      deduct only ₩5,000,000, with 근골격계질환 이학요법료, 체외충격파치료 and 비급여주사제
      excluded from that aggregation and deducted separately. 통원: the greater of **₩30,000
      (3만원)** and **30%**, per visit.
    - **제2의3호 — 실손의료보험 특별약관2 (비중증 비급여)** (신설 2026-05-06). 입원: deduct
      **50%**. 통원: the greater of **₩50,000 (5만원)** and **50%**, per visit. **제1호 requires
      비중증비급여 to be written as a separate 특약**, not inside the base contract.
    - **제3호 — the ±25% corridor**: "실손의료보험에서 **위험구분단위별로 보험료의 변경이 매년
      ±25%를 초과하지 않을 것**", except where the insurer is under, or likely to come under,
      제7-16조~제7-19조 measures. This is a hard bound on the annual re-rating a `Medical_KR_S`
      model may apply.
    - **제3의2호 and 제3의3호** (amended 2026-05-06) — the **비급여 할인·할증**: an insurer may
      apply a **요율 상대도** to the net premium of the 비중증 비급여 특약 on renewal, based on
      claims paid in the twelve months ending three months before the renewal date, with the
      ±25% corridor applying to the **pre-relativity** premium. The five-band table is in the
      표준약관 [R25].
    - **제5호 — 노후실손**: sum insured capped at the combined annual maximum of a normal 실손;
      outpatient per-visit limit **₩1,000,000 (100만원)**; a first-tier deduction of
      **₩300,000 (30만원) inpatient / ₩30,000 (3만원) outpatient** before further co-payments of
      at least 20% (급여) and at least 30% (비급여), the inpatient deduction capped at
      **₩5,000,000 (500만원) a year**.
    - **제6호** — annual verification of the adequacy of the net rate from experience, with five
      years' grace for genuinely new cover (가목); the **benefit-change cycle of five years or
      less** — "보험기간 및 보장내용 **변경주기를 5년 이내**로 할 것" — three years for 노후실손
      and 유병력자실손 (나목); and a requirement to sell or hold a 노후실손 product if covering
      ages 75 and over (다목). 나목 is the **재가입** cycle: a Korean 실손 contract renews
      annually at attained-age rates and **re-enters the then-current generation every five
      years**, a contract-boundary structure with no counterpart elsewhere in this repository.
    - **제7호 and 제8호** — a mandatory suspend-and-resume facility for policyholders doubly
      covered through a group scheme, and a mandatory conversion facility from group-only cover
      to an individual policy.
- **Used by:** indemnity_medical load-bearing throughout; cancer, long_term_care and child for
  제1항제1호 (the payment on non-covered death); ci_insurance for the 제3보험 design frame.

### R18 — 금융위원회, 보험업감독규정 제7-64조 (산출방법서 필수기재사항) and 제7-65조 (계약자적립액의 계산)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (article text; **the two 계약자적립액 accrual formulas of 제7-66조제1항제4호 are
  images and did not extract** — recorded at [R19] and in §7)
- **What it establishes:**
  - **제7-64조 — the five 필수기재사항 of the 산출방법서**: 1. the premium calculation, and for
    contracts longer than three years that must use **현금흐름방식** (cash-flow pricing) an
    analysis of premium adequacy based on **최적기초율** with projected cash flows; 2. the
    reserve calculation, including the interest and morbidity/mortality rates used in the
    보험료적립금; 3. the **해약환급금** calculation, including the interest rate, the 위험률, the
    해약공제액 and — where the 계약체결비용 exceeds the **표준해약공제액** at the 기준연령 요건 —
    a comparison of the two; 4. the calculation where benefits or premiums change; 5. the
    calculation of any **보증비용**.
  - **제7-65조제1항**: "계약자적립액은 보험료 및 책임준비금 산출방법서에 따라 계산한 금액으로
    한다"; **제2항** permits it to be computed on an **annualised premium** basis ("연납보험료를
    기준으로 하여 산출할 수 있다"). That permission is why a Korean monthly-premium product can
    carry an annual-recursion account, and it is directly how `Cancer_KR_S`, `Medical_KR_S`,
    `Child_KR_S`, `LTC_KR_S` and `VA_KR_S` reconcile a monthly grid with an annual reserve.
  - **제7-65조제3항 — the 공시이율**: "공시이율은 **공시기준이율**에 **조정률**을 반영하여 다음
    각호의 방법에 따라 결정하여야 한다": 1. 공시기준이율 is computed per the FSS Governor's rules
    as a weighted average of an objective external index rate and the **운용자산이익률**; 2.
    **운용자산이익률 = 운용자산수익률 − 투자지출률**, on invested assets excluding unrealised
    gains and losses not passed through profit or loss, with 운용자산수익률 from the **preceding
    twelve months'** investment income excluding insurance finance income and the cost from the
    same period's investment expense excluding insurance finance expense; 3. the 공시이율 must be
    **uniform across a product class** the FSS Governor defines [R23], with four exceptions —
    유배당 versus 무배당, timing mismatches from differing reset cycles, the 농협생명/농협손해보험
    legacy 공제계약 versus post-2012-03-02 products, and setting a rate **below the floor
    applying to existing contracts**; 4. items 1 and 2 must be written into the 기초서류.
- **Used by:** every product. The 연납보험료 permission of 제7-65조제2항 is quoted in the
  monthly-grid models' `technical-notes.md`; the 공시이율 chain is load-bearing for whole_life,
  pension_savings, immediate_annuity and ci_insurance.

### R19 — 금융위원회, 보험업감독규정 제7-66조 (생명보험 해약환급금의 계산), 제7-67조, 제7-69조, 제7-70조

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]; 제4항제1호 신설 2020-11-19, 제5항
  신설 2022-12-21
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes (operative words in full; **the 해약환급금 formula display and the two
  계약자적립액 accrual formulas render as images and did not extract**)
- **What it establishes:**
  - **제1항제1호**: "해약환급금은 **계약자적립액에서 … 해약공제액을 공제하여 계산한 금액 이상**
    으로 산출할 수 있다. 다만, 계약자적립액에서 해약공제액을 공제한 금액이 **음(陰)의 값**인
    경우에는 이를 **영(零)으로** 처리한다." A floor of zero, not a negative value.
  - **제1항제2호**: "제1호에 따른 **해약공제기간**은 보험료 납입기간 또는 신계약비 부가기간으로
    하되, 보험료 납입기간 또는 신계약비 부가기간이 **7년 이상일 때에는 7년으로** 한다."
  - **제1항제3호**: "제1호에 따른 … 해약공제액은 **별표 14에서 정한 표준해약공제액으로** 한다"
    [R20].
  - **제1항제4호**: 계약자적립액 accrues **monthly before 납입완료** ("보험료 납입이 완료되기
    이전에는 … 월별 기간경과에 따라 산출한다") and **daily afterwards** ("일별 기간경과에 따라
    산출한다"). The two formulas themselves are images and did not extract.
  - **제3항**: for contracts on which no 해약공제액 is deducted, benefits may instead be
    differentiated on early surrender.
  - **제4항 — the 무해지 / 저해지 permission.** For a **순수보장성보험** or a whole-life 생존연금
    whose premiums or benefits were calculated using a **최적해지율**, the insurer "제1항에서
    정한 해약환급금 **미만으로 지급할 수 있다**" — may pay less than the 별표-14-floored value.
    That is the legal basis of the form: not a contractual gimmick but a **regulatory
    dispensation conditional on having used a best-estimate lapse rate in pricing**. Three
    exceptions: **제1호 변액보험인 경우** (신설 2020-11-19) — a variable product may never use
    it; **제2호**, where the surrender value during the payment period is **less than 50% of an
    otherwise identical 표준형 상품's**, both of 가. the post-payment surrender value **exceeds
    50%** of the 표준형's, and 나. the post-payment **환급률** (surrender value over cumulative
    premiums at each point) **exceeds the greater of 100% and the 표준형's 환급률**, must hold;
    제3호 (deleted).
  - Read carefully, 제2호 is the **환급률 cap**: it permits the deep-discount form only if the
    post-payment refund ratio clears 100% *and* the standard product's ratio. See [R28] for the
    FSC's worked example — a 20-year-pay 종신보험 with a 표준형 20-year 환급률 of **97.3%**
    against a then-current 무해지 환급률 of **134.1%**, the amendment limiting the latter to the
    former.
  - **제5항** (신설 2022-12-21): "보험회사는 보험계약이 해지되는 경우 해약환급금에 **미경과
    보험료 등을 가산한 금액**을 보험계약자에게 지급하여야 한다."
  - **제7-69조** applies the whole of 제7-65조~제7-68조 to **장기손해보험** (including
    연금저축손해보험 and 퇴직보험); **제7-70조** applies it to **제3보험** — "보험요율의 산출과
    보험료 및 해약환급금 산출방법서의 작성 등은 제7-65조, 제7-66조, 제7-67조 및 제7-68조를
    준용한다". **One surrender-value regime governs all ten `krlib` products.**
- **Used by:** every product. whole_life, term_life, ci_insurance, child, cancer and
  long_term_care cite 제4항 for the 무해지/저해지 forms; variable_annuity cites 제4항제1호 for why
  it may **not** use them and must carry a full 별표-14-floored surrender value.

### R20 — 금융위원회, 보험업감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액 (제7-66조 관련)

- Version marker on the schedule: <개정 2011.1.24, 2015.5.7., 2020.1.15.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240711
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927491)
- Accessed: 2026-09-03
- Retrieved: yes — 1-page PDF, text extracted cleanly and in full, including all seven notes
- **What it establishes.** The single most model-relevant page of Korean regulation in this
  library: the statutory cap on the surrender charge, with no US or UK analogue at this level
  of prescription. Reproduced in its operative parts:
  > **표준해약공제액 = 연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000**
  >
  > 주)
  > 1. 장기손해보험에서 연령에 관계없이 단일보험료를 적용하는 상품 및 비용손해담보상품의
  >    경우에는 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납위험보험료의
  >    45%**」로 적용 <개정 2020.1.15.>
  > 2. **해약공제계수**는 다음과 같이 적용함 — 보장성보험: **보험기간(최대 20년)**;
  >    저축성보험: **보험료 납입기간(최대 12년)**, 명칭을 불문하고 납입기간의 범위 내에서
  >    의무적으로 납입해야 하는 별도의 기간을 설정한 경우에는 당해 별도의 납입기간을 보험료
  >    납입기간으로 함, 다만 **일시납보험의 경우 납입기간을 1년**으로 함
  > 3. **연납순보험료 및 연납위험보험료**는 다음과 같이 적용함 — 보장성보험: **전기납(단,
  >    보험기간이 20년 이상인 경우 20년납)**으로 조정하여 산출한 연납순보험료 및 연납위험
  >    보험료, 다만 연납위험보험료 계산시 별표15 제9호 단서의 위험보험료 계산에 관한 규정을
  >    준용한다; 저축성보험: **납입기간(최대 10년)** 동안 동일하게 배분한 평균식 부가보험료를
  >    제외한 연간순보험료 <개정 2020.1.15.>
  > 4. **보험기간이 종신인 생존연금보험(연금저축보험은 제외)**의 경우에는 **연납순보험료의
  >    6%**를 적용하되, 연납순보험료의 5%와 **해약공제계수 12년**을 적용하여 산출한 해약공제액을
  >    초과할 수 없음
  > 5. **연금저축보험**의 경우에는 **연납순보험료의 4%(무배당 연금저축보험은 3%)**를 적용함
  >    <신설 2014.12.31>
  > 6. 보험계약 체결에 사용할 금액을 보험료 납입기간 동안 보험료에 부가하는 저축성보험의
  >    경우에는 보험료에 부가된 금액을 **평균공시이율로 할인**하여 표준해약공제액에서 차감하여
  >    적용함 <신설 2012.2.28, 개정 2014.12.31., 2020.1.15.>
  > 7. **실손의료보험**은 「보장성보험의 보험가입금액의 10/1000」을 「보장성보험의 **연납위험
  >    보험료의 15%**」로 적용한다 <신설 2015.5.7., 개정 2020.1.15.>
- **Reading it for `krlib`.** The cap is a **level** amount, not a schedule: one 표준해약공제액
  is computed once and deducted from the 계약자적립액 during the 해약공제기간, which is the
  premium-paying period capped at seven years [R19]. Product by product:
  - `Term_KR_A`, `WholeLife_KR_A`, `CI_KR_A`, `Child_KR_S` (protection portion), `Cancer_KR_S`,
    `LTC_KR_S` — 보장성보험. Coefficient = policy term capped at 20; annual net premium
    recomputed on a whole-term-pay basis (20-year pay where the term is 20 years or more); plus
    10/1000 of the sum assured.
  - `Medical_KR_S` — 보장성보험, but **note 7** replaces the sum-assured term with **15% of the
    annual risk premium**. This is the only product-specific override in the schedule, and it
    exists precisely because an indemnity product has no 보험가입금액 in the ordinary sense.
  - `Pension_KR_A` — 연금저축보험: **4% of the annual net premium (3% if 무배당)**, coefficient
    = premium-paying period capped at 12.
  - `Immediate_KR_A` — a whole-life 생존연금 that is not a 연금저축보험: **note 4's 6%**, subject
    to the 5% × 12-year ceiling, with a single-premium contract taking a coefficient of **1**.
    The interaction matters: a single-premium immediate annuity's cap is very small relative to
    premium.
  - `VA_KR_S` — 저축성보험 for the coefficient (payment period capped at 12, annual premium
    computed over a payment period capped at 10), and barred from the sub-cap surrender values
    by 제7-66조제4항제1호 [R19].
- **Used by:** every product, load-bearing, in `technical-notes.md`.

### R21 — 금융위원회, 보험업감독규정 [별표 15] 보험가입금액의 산정 (제7-67조 관련)

- Version marker: <개정 2011.1.24., 2020.1.15.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240715
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927503)
- Accessed: 2026-09-03
- Retrieved: yes — 1-page PDF, full text
- **What it establishes.** The 보험가입금액 that enters the 표준해약공제액 formula [R20] is not
  simply "the face amount". The schedule caps it — "다음 각호에서 정한 방법에 의하여 계산된 금액
  **이하**로 하여야 한다" — and the operative items are:
  > 3. **일반사망을 보장하는 보장성보험은 일반사망보험금으로 한다.** <개정 2020.1.15.>
  > 6. 유족연금 등과 같이 보험금이 확정되지 아니하는 보험은 **기준연령 요건**으로 가입하여
  >    중간시점에 사망한 것으로 하여 지급되는 보험기간별 보험금액 중 **최저 보험금액**으로 한다.
  > 8. 제3호는 **체증 또는 체감되기 이전의 금액**으로 한다. <개정 2020.1.15.>
  > 9. 제3호에 해당되지 아니한 경우에는 기준연령 요건에서 다음과 같이 산출한다.
  >    **보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의 보험가입금액**
  >    다만, 정기보험은 해당 보험상품과 동일한 보험기간 기준으로 적용하며, 위험보험료 계산시
  >    다음의 항목은 포함하지 아니한다 — 위험 발생여부와 관계없이 지급하는 보험금을 위한 부분;
  >    특정 위험이 발생하지 않을 경우 지급하는 보험금을 위한 부분; **치매 또는 일상생활장해 등
  >    타인의 간병을 필요로 하는 상태 및 이로 인한 치료 등의 위험 발생시 지급하는 보험금을 위한
  >    부분**.
- **Three things follow.** First, a 제3보험 product with **no death benefit** gets a *notional*
  보험가입금액 by scaling a term policy's face amount by the ratio of risk premiums — which is
  how 별표 14's "보험가입금액의 10/1000" term is given meaning for `Cancer_KR_S` and
  `Child_KR_S`. Second, the third bullet of 제9호 **excludes long-term-care risk premium** from
  that ratio, so `LTC_KR_S`'s notional 보험가입금액 is driven by whatever non-care risk the
  contract carries, not by the care benefit. Third, the whole computation is performed at the
  **기준연령 요건** [R9] — the 40-year-old-male, monthly, whole-term-pay cell.
- **Used by:** cancer, long_term_care, child and ci_insurance load-bearing (it is the only route
  to a 보험가입금액 for a benefit that is not a death benefit); whole_life and term_life for
  제3호 and 제8호; indemnity_medical for the interaction with 별표 14 note 7.

### R22 — 금융위원회, 보험업감독규정 제4-32조 (수수료등 지급기준), 제7-45조 (공시), 제7-51조 (신고기준)

- Version: [시행 2026. 5. 6.] [금융위원회고시 제2026-16호]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112
- Accessed: 2026-09-03
- Retrieved: yes
- **What it establishes** — the expense-and-disclosure ring around the surrender-charge cap:
  - **제4-32조제5항**: for a 보장성보험 other than general non-life and motor, the commission and
    other remuneration paid in the **first year** must not exceed the premium the policyholder
    is expected to pay in that year; and where the contract deducts **80% or more of the
    표준해약공제액** on surrender, the projected surrender value at the one-year point is added
    to the commission side of that test. **제6항**: if the contract lapses within a year,
    remuneration actually paid (again with the surrender value added in the 80%-plus case) must
    not exceed premiums actually received. **제8항**: where the 표준해약공제액 exceeds one year's
    premiums, the insurer must offer distributors an instalment structure paying **no more than
    60% of the 표준해약공제액 a year** (수수료 분할지급방식).
  - **제7-45조제7항**: a 보장성보험 other than general non-life must publish in its 상품요약서 a
    **보험가격지수** — "보험료총액을 참조순보험료 총액과 보험회사 평균사업비총액을 합한 금액으로
    나눈 비율" — and a **보장범위지수**; for **실손의료보험 the 보험가격지수 must be explained on
    each renewal** as well. So the rate bureau's reference rates [R4] become visible to the
    public only as a *ratio*, never as a rate.
  - **제7-45조제11항**: a 보장성보험 whose **계약체결비용 exceeds the 표준해약공제액** must
    disclose a **계약체결비용지수** and a **부가보험료지수** — except that a whole-life
    death-benefit 보장성보험 need not, provided the 계약체결비용 is within **1.4 times** the
    표준해약공제액 (applied to the death-benefit portion only where the product covers both
    death and non-death risks). **That 1.4× tolerance is a useful outer bound for a `[std]`
    acquisition-cost assumption on `WholeLife_KR_A`**: an insurer may load up to 1.4 ×
    표준해약공제액 on a whole-life death product without triggering index disclosure, so a
    reference implementation that sets 계약체결비용 at or below the 표준해약공제액 is
    conservative and defensible.
  - **제7-51조** lists the three cases in which a 산출방법서 must be pre-notified: 1. a 저축성보험
    that does **not** spread at least 50% of the acquisition cost evenly over the premium-paying
    period (40% for a whole-life 생존연금, 70% bancassurance, 100% online), the period being at
    least seven years where the payment term is seven years or more and at least fifteen months
    for single premium; 2. a 보장성보험 that does not spread the acquisition cost evenly over the
    premium-paying period; 3. a renewable or re-entry product whose **계약체결비용 on renewal
    exceeds 70% of the first contract's 계약체결비용**.
- **Used by:** whole_life (the 1.4× bound) and indemnity_medical (the renewal-time 보험가격지수
  and the 70% renewal-cost test, which bites directly on a one-year renewable product) load-
  bearing; every other product cites 제4-32조 in the expense-assumption rationale.

### R23 — 금융감독원, 보험업감독업무시행세칙 (금융감독원세칙)

- Version: [시행 2026. 9. 10.] [금융감독원세칙, 2026. 8. 28., 일부개정]
- URL: https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2200000108939
- Accessed: 2026-09-03
- Retrieved: yes (114,610 characters)
- **Caveat, and it must travel with every citation of this entry.** The version law.go.kr
  serves as current **takes effect 2026-09-10, one week after the access date**. Facts taken
  from it are facts about the imminent text, not about the text in force on 2026-09-03. Where
  that matters a product document must say so at the point of use.
- **What it establishes:**
  - **제5-13조** — the **표준사업방법서 and 표준약관** are 별표 14 and **별표 15** to the 세칙
    [R25]. Insurers write their own conditions against the 표준약관; it is not a model law to be
    adapted at will, and its clauses appear near-verbatim in every retail Korean policy.
  - **제5-16조제3항** — the **objective external index rates** entering the 공시기준이율 are the
    yields on **국고채(5년), 회사채(무보증 3년, AA-), 통화안정증권(1년)** and **양도성예금증서
    (91일)**, with substitution allowed if a publisher discontinues one; the calculation itself
    is **별표 27** [R24]; and a newly established insurer, or one with a sharp fall in
    investment return, may use an alternative method notified to the FSS.
  - **제5-16조제4항** fixes the **product classes across which the 공시이율 must be uniform**:
    생명보험 — 보장성보험(순수보장성 및 기타보장성), 보장성보험(**종신보험**), 생사혼합보험(만기
    7년 이하), 생사혼합보험(만기 7년 초과), **연금보험**, 교육보험; 손해보험 — 보장성보험(만기
    15년 이하), 보장성보험(만기 15년 초과), 저축성보험(만기 7년 이하), 저축성보험(만기 7년 초과),
    개인연금보험.
  - **제5-17조의2** and the 부칙 dating the 계리적 가정 amendments were read for chronology.
- **Used by:** every product. The 공시이율 product-class list is load-bearing for whole_life
  (종신보험 is its own class), pension_savings and immediate_annuity (연금보험).

### R24 — 금융감독원, 보험업감독업무시행세칙 [별표 27] 공시기준이율 산출 기준 (제5-16조 관련)

- Version markers: <신설 2012.9.26, 개정 2013.12.17., 2018.11.6., 2022.12.23., 2025.10.28.>
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295679
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885941)
- Accessed: 2026-09-03
- Retrieved: yes — 3-page PDF, full text; **two weight formulas render as images and did not
  extract**, noted below
- **What it establishes**, verbatim in its operative parts:
  > 공시기준이율 = 객관적인 외부지표금리 × α + 운용자산이익률 × (1−α)
  >
  > 객관적 외부지표금리 = 국고채(5년) 수익률 × β1 + 회사채(무보증 3년, AA-) 수익률 × β2
  > + 통화안정증권(1년) 수익률 × β3 + 양도성예금증서(91일) 유통수익률 × β4
  - the four yields are taken as a **three-month weighted moving average ending at the end of
    the month two months before the application date**;
  - **β1…β4** are the shares of the insurer's own prior-year average balances of domestic
    public bonds, corporate bonds, monetary stabilisation bonds and CDs, "직전년도" being the
    twelve months ending three months before the start of the business year; the weights are
    **rounded to 0.5 percentage points, constrained to [0%, 100%]** and held constant through
    the business year;
  - **α** is a function of the opening 계약자적립액, the prior year-end asset duration and the
    prior year's premium income — **the formula itself is an image and did not extract** — and
    is **rounded to 0.5 percentage points**, held constant through the business year, and **may
    not exceed 60%**;
  - the rate is computed **separately by account** (계정별) unless an account is too small;
  - added 2025-10-28: for a reinsurance treaty where the assuming insurer recognises the whole
    investment result on identified assets, those assets and their investment income enter the
    **assuming** insurer's 운용자산이익률, not the ceding insurer's.
- **What this is for.** The 공시기준이율 is the regulated *floor construction* under the
  **공시이율** a Korean interest-sensitive product actually credits [R18]; the insurer then
  applies a 조정률 to reach the 적용이율 it publishes monthly. Because α is capped at 60%, a
  Korean declared rate is **majority-weighted to the insurer's own realised 운용자산이익률**, not
  to market yields — which is why Korean 공시이율 move sluggishly against government bond yields
  and why a `krlib` crediting-rate assumption is modelled as a slow-moving `[std]` scalar rather
  than as a function of a yield curve.
- **Used by:** whole_life, pension_savings, immediate_annuity and ci_insurance load-bearing;
  every other product cites it once for the crediting-rate frame.

### R25 — 금융감독원, 보험업감독업무시행세칙 [별표 15] 표준약관 (제5-13조제1항 관련)

- Version markers: 생명보험 표준약관 <개정 … 2024.12.20., 2025.3.31., 2025.6.30.>;
  실손의료보험 표준약관 amended **2026.5.6.**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295613
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885301)
- Accessed: 2026-09-03
- Retrieved: yes — a **492-page PDF**, 441,610 characters extracted. Read in full: the table of
  contents, **Ⅰ. 생명보험** (제1조~제43조 plus 부표), and, of **Ⅱ. 손해보험**, the 실손의료보험
  family — 기본형 실손의료보험(급여), 실손의료보험 특별약관1(중증 비급여) and 실손의료보험
  특별약관2(비중증 비급여). The 장해분류표 and 재해분류표 appendix tables extracted as running
  text with some tabular layout lost.
- **What it establishes** — the clauses every Korean retail policy carries:
  - **보험나이 (제21조)**, verbatim: "① 이 약관에서의 피보험자의 나이는 **보험나이**를 기준으로
    합니다. 다만, 제19조(계약의 무효) 제2호의 경우에는 실제 **만 나이**를 적용합니다. ② 제1항의
    보험나이는 계약일 현재 피보험자의 실제 만 나이를 기준으로 **6개월 미만의 끝수는 버리고
    6개월 이상의 끝수는 1년으로** 하여 계산하며, 이후 매년 계약 해당일에 나이가 증가하는 것으로
    합니다." The 약관 prints its own worked example — 생년월일 1988-10-02, 계약일 2014-04-13,
    difference 25년 6월 11일 ⇒ **26세**. This is nearest-birthday age by a six-month rule and it
    differs from 만나이 for half of all issue dates. **Every `krlib` model declares which it
    uses: 보험나이 for pricing, 만나이 for statistics**, because the 생명표 [R38] and the NHIS
    statistics [R41] [R42] are on 만나이.
  - **청약철회 (제17조)** — withdrawal within **15 days of receiving the 보험증권** and never
    after **30 days from the application date**; three exclusions (insurer-funded health
    examination, contracts of **90 days or less**, a 전문금융소비자); effective **on despatch**;
    premiums returned **within 3 business days**, late return carrying interest at the
    **보험계약대출이율 compounded annually**. Statutory source: 금융소비자보호법 제46조 [R51].
  - **품질보증해지 (제18조제3항)** — where the insurer failed to deliver the 약관 and the
    policyholder's copy of the application, or failed to explain the important content, or the
    policyholder did not sign, cancellation **within three months of formation** with premiums
    returned plus 보험계약대출이율 interest. Statutory source: 상법 제638조의3제2항 [R49].
  - **계약 전 알릴 의무 (제13조, 제14조)** — the 약관 states in terms that this "상법상
    '고지의무'와 같습니다". The insurer may **not** terminate where: it knew or was negligent in
    not knowing at formation; **one month** has passed since it learned of the breach, or **two
    years** from the 보장개시일 without a claim event (**one year for disease in a 진단계약**);
    **three years** have passed since the contract date; it accepted on a health-examination
    document and the claim arises from a matter stated in it; or the 보험설계사 prevented
    truthful disclosure. 제14조제4항 carries the causation defence; 제14조제5항 bars termination
    for non-disclosure of **other insurance held**.
  - **사기에 의한 계약 (제15조)** — proxy examination, drug use to pass underwriting, forged
    certificates or concealment of a pre-application cancer or HIV diagnosis: cancellation
    **within five years of the 보장개시일 and one month of learning of the fraud**.
  - **납입최고 and 해지 (제26조)** — a demand period of **at least 14 days** (7 where the policy
    term is under a year), stating that the contract terminates the day after it ends and that
    **policy-loan principal and interest are immediately deducted from the surrender value**.
  - **부활 (제27조)** — where the contract terminated under 제26조 and **the surrender value has
    not been drawn** (including where a policy loan consumed it, and including where there is
    none — the 무해지 case), reinstatement may be applied for **within three years**, paying
    arrears with interest at a rate the insurer sets **within 평균공시이율 + 1%**; the insurer
    may **not** refuse because a claim event occurred before termination.
  - **해약환급금 (제32조)** — computed per the 산출방법서, paid **within 3 business days**, with
    interest per 부표 4-1; **the insurer must give the policyholder a table of surrender values
    by elapsed period** (제3항). Where the contract is terminated as a 위법계약 under 제29조의2
    the **계약자적립액** is returned instead.
  - **보험계약대출 (제33조)** — borrowing within the surrender value on the insurer's terms,
    "그러나 **순수보장성보험 등** 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다";
    unpaid principal and interest deducted from any benefit or surrender value. **A 무해지
    protection product may therefore have no policy loan at all during the payment period** — a
    point `WholeLife_KR_A` and `Term_KR_A` must state, and one the FSS made explicitly in its
    2019 consumer alert [R28].
  - **계약의 소멸 (제22조)** — where death makes further benefits impossible and death is not
    itself an insured event, the insurer pays "산출방법서에서 정하는 바에 따라 회사가 적립한
    **사망 당시의 계약자적립액**". This is the 표준약관's implementation of 감독규정
    제7-63조제1항제1호 [R17] for 제3보험 products, and the statutory floor beneath it is 상법
    제736조 [R50].
  - **보험금의 지급사유 (제3조)** — the five categories a Korean life policy pays on: 중도보험금,
    만기보험금, 사망보험금, **장해보험금** (on the 장해분류표 percentage scale), and **입원보험금
    등** — "질병이 진단확정되거나 입원, 통원, 요양, 수술 또는 **수발**이 필요한 상태가 되었을
    때". The fifth is where 제3보험 benefits attach, and **수발** is the 약관's word for the need
    of care a 간병보험 pays on.
  - **장해분류표 (부표 3)** defines 장해 as "상해 또는 질병에 대하여 치유된 후 신체에 남아 있는
    **영구적인** 정신 또는 육체의 훼손상태 및 기능상실 상태", excluding temporary states during
    treatment. It is the common **percentage** scale behind 납입면제 (premium waiver) in every
    Korean protection product — not a binary trigger.
  - **소멸시효 (제37조)** and **예금보험에 의한 지급보장 (제43조)** carry the 상법 제662조
    three-year period [R49] and the cross-reference to 예금자보호법 [R52].
  - **실손의료보험 표준약관** (2026-05-06) carries the fifth-generation design: the 건강보험
    본인부담률 definition — `급여일부본인부담 항목의 본인부담금 ÷ (급여일부본인부담 항목의
    본인부담금 + 급여 공단부담금)`, with 100%-본인부담 items excluded from both ratio and cover;
    annual 보험가입금액 up to **₩50,000,000 (5천만원)** for each of 상해급여 and 질병급여 with
    outpatient capped at **₩200,000 (20만원) per visit**; the 비중증 비급여 rider's annual
    ₩50,000,000 limits, its 3대비급여 sub-limit, its per-visit 비급여 cap of **₩3,000,000
    (300만원)** on certain items and its **50% of 비급여 병실료** rule with a daily average cap;
    the limitation of cover to "실제 본인이 부담한 금액 (관련 법령에서 사전 또는 사후 환급이
    가능한 금액은 제외한 금액)", which makes the **본인부담상한제** refund [R53] reduce the
    insured loss; and the **비급여 할인·할증 five-band table** (특별약관2 제6조제3항):
    | 단계 | 1단계 (할인) | 2단계 (유지) | 3단계 (할증) | 4단계 (할증) | 5단계 (할증) |
    |---|---|---|---|---|---|
    | 12-month claims paid | ₩0 (no claim) | >₩0, <₩1,000,000 | ₩1,000,000–<₩1,500,000 | ₩1,500,000–<₩3,000,000 | ≥₩3,000,000 |
    | 요율 상대도 | 할인 (balancing) | 100% | 200% | 300% | 400% |
    The surcharge applies only to contracts with **₩1,000,000 or more** of annual claims, the
    discount is set each year so total premium before and after the relativity is unchanged — a
    pure redistribution — and **장기요양 1등급 and 2등급 under 노인장기요양보험법 are excluded**
    from the claims count [R54], a direct statutory cross-reference between `Medical_KR_S` and
    `LTC_KR_S`.
- **Used by:** every product, load-bearing. It is the source of every contractual mechanic in
  `krlib` that is not carrier-specific, and it is why `krlib` can state a 보험나이 rule, a
  cooling-off period and a reinstatement window without citing any individual insurer.

### R26 — 금융감독원, 보험업감독업무시행세칙 [별표 22] (K-ICS 지급여력) and [별표 24] (보증준비금 산출기준)

- URLs tried: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2200000080687 and
  https://lbox.kr/v2/statute-admin/보험업감독업무시행세칙
- Accessed: 2026-09-03
- Retrieved: **no** — law.go.kr returned the navigation shell for the 별표 index at the
  admRulSeq tried, and `lbox.kr` returned HTTP 403. The 별표 route that worked for 별표 14, 15
  and 27 (`admRulBylContentsInfoR.do?bylSeq=…` → `flDownload.do?flSeq=…`) was **not** resolved
  for these two schedules, because their `bylSeq` values were never obtained.
- **What it would establish, quoted at second hand and therefore [unverified] here:**
  - **[별표 22]** carries the K-ICS 지급여력 standards, including the **대량해지위험 shock**,
    which [R36] reproduces as: 표준형 — 저축성보험 계약 **35%**, 보장성보험 계약 **25%**
    일시해지; 저해지환급형 고환급형 — 순자산 감소상품 향후 1년 해지율 **+35%p**, 순자산 증가상품
    향후 1년 해지율 **× (1 − 40%)**; 저해지환급형 비고환급형 — **+25%p** / **× (1 − 40%)**;
    with 고환급형 defined as "경과기간 시점별 '기납입보험료 대비 해약환급금 비율'이 '기납입보험료
    대비 기납입보험료를 평균공시이율로 부리한 금액의 비율'보다 큰 시점이 존재하는 상품". Note the
    direct dependence on the **평균공시이율** series [R48]: the same product can be 고환급형 in
    one issue year and not in another purely because the 평균공시이율 moved.
  - **[별표 24]** carries the **보증준비금 산출기준**: the guarantee reserve is the greater of a
    stochastic **CTE(70)** figure — "사망률, 해지율, 자산이익률(1,000개)을 이용하여 만기까지
    장래 예상되는 순손실액을 현가로 환산한 상위 30% 평균 금액" — and a standard factor tabulated
    by 보험종류 × 최저보증종류 × 보증수준 × 주식비중한도. A search result indicates the annex is
    invoked by 감독규정 제6-11조 제10호 and computed under 시행세칙 제4-15조; **neither article was
    retrieved, so those article numbers are [unverified]**.
- **Used by:** variable_annuity load-bearing (the 보증준비금 basis, which is why the product's
  보증비용 exists at all) with every dependent figure tagged [unverified]; whole_life, term_life
  and the other protection products cite 별표 22 only through [R36], and must say so.

### R27 — 금융위원회·금융감독원, 제4차 보험개혁회의 보도자료 — 「합리적인 계리가정과 단계적 할인율 조정을 …」

- Publisher: 금융위원회 보험과 / 금융감독원 보험리스크관리국; meeting 2024-11-04, 배포
  2024-11-06, 보도 2024-11-07
- URL: https://www.fsc.go.kr/no010101/83351
  (attachments at `…/comm/getFile?srvcId=BBSTY1&upperNo=83351&fileTy=ATTACH&fileNo=1` and the
  same with `fileNo=4`)
- Accessed: 2026-09-03
- Retrieved: yes — the 6-page 보도자료 PDF and the 6-page 별첨 「보험부채 할인율 현실화 연착륙
  방안」 PDF, both extracted in full. Attachments 2, 3 and 5 are HWP/HWPX and were not converted.
- **What it establishes.** This is the most important single supervisory document for `krlib`'s
  lapse assumptions, and it is the reason the library's protection products can carry a
  defensible `[std]` lapse vector at all.
  - **The problem the FSS named:** because there is no experience on 무·저해지 business,
    insurers assumed **high lapse right up to 완납**, which flatters profitability; the resulting
    switching out of 표준형 products raised observed 표준형 lapse, which was then fed back into
    the 무해지 assumption — "악순환".
  - **The ruling:** among models converging to zero lapse at 완납, the **로그-선형(log-linear)
    모형** is judged most appropriate and is adopted as the **원칙모형**, with a practical
    convergence point of **0.1%**. Alternatives are permitted only within a closed list —
    **선형-로그모형** (converging to 0% at 완납) and **로그-로그모형** (converging to 0.1%) — and
    only if the insurer discloses, in the audit report and the management disclosure, the reason
    for the choice, an external actuarial verification, and the difference from the principle
    model in **CSM, best-estimate liability, K-ICS ratio (both required and available capital)
    and net income**, reports the difference to the FSS quarterly, and submits to an on-site
    inspection.
  - **Post-완납 ultimate lapse rate: 0.8%**, taken from overseas statistics, or alternatively a
    **20% relativity** to the overseas standard-form lapse rate.
  - **단기납 종신보험**: where a short-pay whole-life product (5–7 year pay) carries a bonus at,
    say, year 10 producing a refund ratio of e.g. **135%**, the insurer must assume an
    **additional lapse of at least 30%** at the bonus date, or back it out from the standard
    product's cumulative persistency. The 30% floor is calibrated to the ten-year average of the
    **11th-year lapse rate on single-premium bancassurance savings business, 29.4%–30.2%** —
    the point at which the tax exemption [R58] is met and the refund ratio jumps.
  - **Loss ratios must be split by age cohort** where experience is sufficient and the split is
    statistically significant. The worked industry example is the 상해수술 cover: **30s 89% →
    40s 103% → 50s 140% → 60s 186%**.
  - **The 무·저해지 share of 보장성 초회보험료**: 2018 **11.4%** → 2021 **30.4%** → 2023 **47.0%**
    → 2024 H1 **63.8%**. Nearly two-thirds of new Korean protection business by first-year
    premium is written in a form whose surrender value is nil or suppressed until 납입완료. **Any
    Korean reference library that models only 표준형 products is modelling a minority of the
    market.**
  - **The IFRS 17 discount-curve architecture**: the risk-free term structure is built from
    국고채 yields, with **관찰금리** used directly to the **최종관찰만기 (LOT/LLP), currently 20
    years**, then interpolation to 60 years and a convergence segment beyond; the convergence
    point is the **장기선도금리 (LTFR)**, "실질이자율 장기평균 + 물가상승 목표", **currently
    4.55%**; a **유동성프리미엄** is added, being the total risk spread less the credit spread
    unrelated to the contract, **currently 91bp**. The August 2023 phase-in raises the annual
    LTFR adjustment cap from 15bp to **25bp** (2024), realises the loan-yield input to the
    liquidity premium (2024), removes unexpected risk from it (2027), rationalises the 100%
    adjustment ratio (2026) and extends the LOT from **20 to 30 years from 2025** — the last of
    which the November 2024 decision then spread over **three years**.
  - **Government 10-year yields quoted as the reason for the slow-down**: **3.74%** (2022
    year-end) → **3.18%** (2023 year-end) → **3.40%** (2024-03) → **3.26%** (2024-06) → **2.99%**
    (2024-09). At a 10-year yield of 3.0% the industry K-ICS ratio was expected to fall about
    **20 percentage points** from the 2024-06-30 level of **217.3%**.
  - **Application**: from the **2024 year-end closing**, with loss-ratio assumptions permitted to
    slip to 2025 Q1 where systems could not be changed in time; the discount-rate soft landing
    applies from **2025-01**.
- **Modelling consequence, and it appears in every protection product's technical notes.** The
  `lapse_rate` vector on a 무해지 or 저해지 form is **not free**. A `krlib` reference
  implementation uses a **log-linear decay to 0.1% at 납입완료 and 0.8% thereafter**, tagged
  `[std]` with this entry as its rationale, and carries a switch to the 표준형 assumption so the
  two can be compared — which is exactly the comparison the guideline requires an insurer to
  disclose.
- **Used by:** every product, load-bearing. whole_life, term_life, ci_insurance, child, cancer
  and long_term_care for the lapse vector; every product for the discount-curve paragraph.

### R28 — 금융위원회, 무(저)해지환급금 보험 상품구조 개선 (2020-07-27 입법예고, 2020-11-18 확정) and 금융감독원, 저해지환급금 보험상품 소비자경보 (2019-10-23)

- URLs: https://www.fsc.go.kr/no010101/74468 (입법예고, 2020-07-27);
  https://fsc.go.kr/no010101/74613 (확정, 2020-11-18);
  https://www.fsc.go.kr/no010101/73932 (금융감독원 소비자경보, 2019-10-23)
- Accessed: 2026-09-03
- Retrieved: yes (all three, server-rendered HTML)
- **What it establishes:**
  - **The definition.** The 입법예고 defines a 무(저)해지환급금 보험 as "보험료 산출 또는
    보험금(연금액) 산출시 **해지율을 사용한 보험**" — an assumption-driven, not a
    contract-driven, class.
  - **The market count at July 2020**: **20 life insurers and 11 non-life insurers** were selling
    the form as a flagship product, against 4 and 3 not selling it. No market-share figure was
    given in the release.
  - **The mis-selling concern**: "저축성보험처럼 환급률만을 강조하며 판매".
  - **The arithmetic that became 감독규정 제7-66조제4항제2호** [R19]: on a 20년납 종신보험
    (1,000만원, 남 40세) the 표준형 20-year 환급률 was **97.3%** against a then-current 무해지
    20-year 환급률 of **134.1%**; the amendment, effective **2020-11-19**, requires the second to
    be designed "전(全) 보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로".
  - **The internal controls**: 시행세칙 제5-19조 was strengthened on lapse-rate derivation,
    verification and profitability sensitivity.
  - **From the 2019 FSS consumer alert**: life insurers began selling the form in **July 2015**
    and non-life insurers in **July 2016**; about **4 million contracts** had been written to
    March 2019; the form is a **보장성보험 and unsuitable as savings**; and — operationally
    important, and repeated in the 표준약관 제33조 [R25] — **a 무해지환급금 contract cannot
    support a policy loan during the payment period**.
- **Used by:** whole_life, term_life, ci_insurance, child, cancer and long_term_care
  load-bearing — the 환급률 cap is what shapes the surrender-value curve every one of them
  publishes, and the no-policy-loan point is a stated product limitation. variable_annuity cites
  it to explain why it is *excluded* from the form.

### R29 — 금융위원회, 「불합리한 보험 사업비와 모집수수료를 개편하여 …」 (2019-08-01)

- Publisher: 금융위원회
- URL: https://fsc.go.kr/no010101/73816
- Accessed: 2026-09-03
- Retrieved: yes (server-rendered HTML)
- **What it establishes:** the 2019 expense-and-commission reform, and in particular the
  **표준해약공제액 expressed as a multiple of the monthly premium** — **보장성보험 13배,
  저축성보험 3배**; the rule that the savings element of a 보장성보험 must carry 저축성 expense
  and surrender-deduction levels at **70%** of the then-current amount; and the 모집수수료 분급
  rule that the annual commission may not exceed **60% of the 표준해약공제액** with the instalment
  total at least **5%** above the up-front total. Timetable: expense reform to April 2020,
  commission reform from January 2021. The 60% figure is the same one that now sits in 감독규정
  제4-32조제8항 [R22].
- **Why the multiples matter.** 별표 14 [R20] states the cap as a formula in 연납순보험료 and
  보험가입금액; this release states the same cap as a **rule of thumb in monthly premiums**, which
  is how Korean practitioners actually carry it. A `krlib` acquisition-cost assumption that
  computes 별표 14 exactly and then sanity-checks it against "13 months' premium for a
  보장성보험" is doing what a Korean pricing actuary does.
- **Used by:** whole_life, term_life, ci_insurance, child, cancer, long_term_care and
  variable_annuity, in the expense-assumption rationale.

### R30 — 금융위원회, 「新회계·자본제도에 맞춘 보험업권 자본규제 고도화」 (2025-03-12) and 금융감독원, 「2025년 9월말 기준 보험회사 지급여력비율 현황」

- URLs: https://www.fsc.go.kr/no010101/84128 (FSC, 2025-03-12);
  https://eiec.kdi.re.kr/policy/materialView.do?num=275691 (FSS release of 2026-01-06, mirrored
  by KDI 경제교육·정보센터)
- Accessed: 2026-09-03
- Retrieved: **in part** — the FSC page returned in full; the FSS quarterly returned only the
  headline ratios through the KDI summary page, and the underlying PDF was not downloaded, so
  the component amounts (지급여력금액, 지급여력기준금액) are not available here.
- **What it establishes:**
  - **The size of the capital-regime shift** [FSC]: 요구자본 rose from **₩67.9조 under RBC at
    2022-12-31 to ₩118.9조 under K-ICS at 2024-09-30**; the **기본자본 K-ICS ratio** fell from
    **145.1%** (2023-03) to **132.6%** (2024-09); 2024 capital-securities issuance reached
    **₩8.7조, 272% of the prior year's ₩3.2조**; and the 비상위험준비금 was reformed.
  - **K-ICS ratios after 경과조치 at 2025-09-30** [FSS]: all insurers **210.8%**, 생명보험
    **201.4%**, 손해보험 **224.1%**. The regulatory minimum is **100%** [R8] and 경영개선권고
    begins below it [R14].
- **Used by:** every product, as one line of context in `product-spec.md`. Nothing is modelled
  from it. The quarterly series for 2025-03 and 2025-06 exists at
  `https://eiec.kdi.re.kr/policy/materialView.do?num=267710` and `…num=271247` and was **not**
  opened — recorded so a later drafter has it to hand.

### R31 — 금융위원회, 실손의료보험 개혁방안 보도자료 (2025-04-01) and the 5세대 launch release (2026-05-06)

- URLs: https://www.fsc.go.kr/no010101/84272 (개혁방안, 2025-04-01);
  https://www.fss.or.kr/fss/bbs/B0000188/view.do?nttId=217561&menuNo=200218 (금융위원회·금융감독원
  joint release, 배포 2026-05-04, 보도 2026-05-06, 15 pp.)
- Accessed: 2026-09-03
- Retrieved: yes — the 2025 개혁방안 page text, and the 2026 launch 보도자료 as a 655 KB, 15-page
  PDF (13,903 characters) whose 참고1 comparison table extracted in full
- **What it establishes:**
  - **The 5세대 design before it became regulation** [2025-04-01]: the 급여 co-payment formula,
    the 중증/비중증 비급여 split with their co-payments and limits, the **₩5,000,000 annual
    co-payment cap** on 중증 비급여 inpatient care at tertiary and general hospitals, the
    illustrative premium reductions, the **계약재매입** offer to first- and early-second-
    generation policyholders — about **16 million** of them — and the **2026-07 to 2036-06**
    ten-year conversion window. The FSC's own framing of the 급여 co-payment change is
    "건보정책과의 연계성 강화": the private co-payment now tracks the public one [R53].
  - **The launch** [2026-05-06]: the product in full; the **4세대-versus-5세대 comparison table**,
    which is the only retrieved document stating the complete 4세대 limit and sub-limit set in
    one place; the premium effect — **−30% against 4세대**, **−50% or more against 1·2세대**, with
    base plus 특약1 only at roughly **50% of the 4세대 premium**; the 선택형 할인 특약 and the
    계약전환 할인 (계약재매입) schemes commencing **2026-11** for the ~**47.5%** of in-force
    policies written before 2013-03 with no re-entry clause; a worked 60-대 여성 premium table
    across options; and the launch carrier list of **16 companies (7 생보, 9 손보)**.
- **Used by:** indemnity_medical load-bearing; child and cancer for the generation frame. The
  operative rules themselves are cited to 감독규정 제7-63조 [R17] and the 표준약관 [R25], not to
  the release.

### R32 — 금융위원회, 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」 (2025-09-01)

- Publisher: 금융위원회; release dated 2025-08-29, published on the commencement date
- URL: https://www.fsc.go.kr/no010101/85200
- Accessed: 2026-09-03
- Retrieved: **in part** — title, dates and the general statement returned; the release as
  summarised does not itemise the insurance-specific buckets
- **What it establishes:** it dates the increase of the deposit-protection limit to
  **₩100,000,000 (1억원)**, in force **2025-09-01**. **The per-bucket mechanics come from
  예금자보호법 시행령 제18조제7항 [R52], which is authoritative and was retrieved in full**; this
  entry is cited only for the date and the public framing.
- **Used by:** pension_savings load-bearing (the 연금저축계좌 bucket is separate from the
  ₩100,000,000 covering the policyholder's other insurance claims); every other product for the
  one-line 예금자보호 sentence that 표준약관 제43조 [R25] requires the 약관 to carry.

---
