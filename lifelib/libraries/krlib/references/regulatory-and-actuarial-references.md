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
