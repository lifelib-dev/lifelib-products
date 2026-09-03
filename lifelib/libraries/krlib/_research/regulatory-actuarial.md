# Regulatory and actuarial framework — research notes (Korea)

Research compiled 2026-09-03 for `krlib`, the Korea section of the reference-products
library. Purpose: the single provenance layer behind all ten Korean products —
`whole_life`, `term_life`, `ci_insurance`, `child`, `indemnity_medical`, `cancer`,
`long_term_care`, `pension_savings`, `variable_annuity` and `immediate_annuity`. Every
one of those products' `product-spec.md`, `technical-notes.md`, `model.md` and
`sources.md` rests on facts recorded here, and on
`references/regulatory-and-actuarial-references.md`, which is built from this file's
source list. **The source numbering below is frozen.** `S1` and `R1` mean the same
documents for the life of the library; product documents cite them through the
cross-product tag `[REG-R#]`, and renumbering would silently repoint every citation in
ten document sets.

Korea's insurance regulation is unusual among the markets in this repository in three
structural ways, and the file is organised so that a drafter meets all three early.
First, **both** of the two large accounting-and-solvency reforms of the decade have
been live since **2023-01-01**: K-IFRS 제1117호 (the Korean adoption of IFRS 17) and
**K-ICS** (신지급여력제도, the Korean Insurance Capital Standard). Japan's economic-value
solvency regime commences 2026 and the UK and EU regimes long predate IFRS 17; Korea
switched liability measurement and capital measurement in the same quarter. Second, on
top of those two Korea layers a **해약환급금준비금** (*haeyak-hwangeupgeum-junbigeum*,
surrender value reserve) inside retained earnings, whose whole purpose is to stop an
IFRS 17 balance sheet from distributing earnings that the surrender-value floor would
later demand — a mechanism with no counterpart in `uslib`, `uklib`, `jplib`, `frlib` or
`delib`. Third, **제3보험** (*je-sam boheom*, "third insurance") is a statutory licence
category, not a market label: 보험업법 제4조제1항제3호 names 상해보험, 질병보험 and
간병보험, and both life and non-life insurers write them. Four of `krlib`'s ten products
sit inside it.

A fourth Korea-specific fact governs the shape of every model in the library. The
industry mortality table, the **경험생명표** (*gyeongheom saengmyeongpyo*, Experience Life
Table) produced by 보험개발원 (Korea Insurance Development Institute, KIDI), is **not
published**. Only summary statistics are released — 평균수명 and 기대여명 — and the qx
table itself is available to member insurers, not to the public. There is therefore no
Korean analogue of Japan's 標準生命表 numeric table or Germany's DAV 2008 T. Every
`mort_table.csv` in `krlib` is consequently a **[std]** construction anchored on
published 국가데이터처 (formerly 통계청) 생명표 statistics and on the KIDI summary figures,
carrying a `provenance` column on every row. Section 26 records exactly what is and is
not public, and section 35 records what that forces on the models.

Citation discipline, as in the sister libraries: every fact below carries `[S#]` where
it was read from a retrieved primary legal or standard-form document, `[R#]` where it
came from a retrieved supervisory release, statistical publication or research paper,
and `[unverified]` where it rests on a search-result summary, on general knowledge, or
on a document that could not be opened. Numbers are given with their units and their
as-of date; Korean amounts are given in 만원 (10,000) and 억원 (100,000,000) as well as
in won, because that is how a Korean source states them.

A note on retrieval, because it determined what this file can say. `law.go.kr` (국가법령
정보센터) serves both statutes and 행정규칙 as a JavaScript shell; a plain fetch of
`https://www.law.go.kr/법령/<name>` returns navigation chrome only. The body is served
from two inner endpoints that **do** return full UTF-8 HTML —
`https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=<id>&efYd=<yyyymmdd>` for 법령 and
`https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=<id>` for 행정규칙 — and the 별표
(schedules), which are images inside those pages, are served as PDFs through
`admRulBylContentsInfoR.do?bylSeq=<id>` followed by `flDownload.do?flSeq=<pdfFlSeq>`.
That three-step route is how 별표 14 (표준해약공제액), 별표 15 (보험가입금액의 산정) and
별표 27 (공시기준이율 산출 기준) were obtained verbatim, and it is worth recording because
those three schedules carry the only published statement of Korea's surrender-charge
cap and crediting-rate formula. Where a formula in the body text of a regulation is
rendered as an image rather than as text, it is recorded here as not retrieved.

---

## Primary sources

### S1 — 보험업법, 법률 제20436호
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2025. 1. 31.] [법률 제20436호, 2024. 9. 20., 타법개정]**
- URL: https://www.law.go.kr/법령/보험업법
  (body retrieved from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=265389&efYd=20250131)
- Accessed: 2026-09-03
- Retrieved: yes (full statute, 127,346 characters of extracted text)
- What was read: the whole Act. Articles used below are 제2조 (정의), 제4조 (보험업의
  허가), 제5조 (허가신청서 등의 제출), 제108조 (특별계정), 제120조 (책임준비금 등의
  적립), 제123조 (재무건전성의 유지), 제124조 (공시 등), 제127조 (기초서류의 작성 및
  제출), 제128조 (기초서류에 대한 확인), 제128조의2 (기초서류 관리기준), 제128조의3
  (기초서류 작성ㆍ변경 원칙), 제176조 (보험요율 산출기관), 제181조 (보험계리) and
  제184조 (선임계리사의 의무 등). This is the statute that defines the product taxonomy
  the whole library sits in, and the document set (기초서류) a Korean product filing
  consists of.

### S2 — 보험업법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 4. 21.]** (lsiSeq 285553, efYd 20260421)
- URL: https://www.law.go.kr/법령/보험업법 시행령
  (body from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285553&efYd=20260421)
- Accessed: 2026-09-03
- Retrieved: yes (153,076 characters)
- What was read: 제1조의2 (보험상품 — the closed lists of 생명보험계약, 손해보험계약 and
  제3보험계약, and the six public schemes excluded from "보험상품"), 제63조 (책임준비금
  등의 계상 — the IFRS 17 vocabulary in delegated form), 제65조 (재무건전성 기준 — the
  100% 지급여력비율 floor), 제71조 (기초서류의 작성 및 변경 — the 30-day pre-filing).

### S3 — 보험업감독규정, 금융위원회고시 제2026-16호
- Publisher: 금융위원회 (보험과), served by 국가법령정보센터 as a 행정규칙
- Version: **[시행 2026. 5. 6.] [금융위원회고시 제2026-16호, 2026. 5. 6., 일부개정]**
- URL: https://www.law.go.kr/행정규칙/보험업감독규정
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000279112)
- Accessed: 2026-09-03
- Retrieved: yes (226,083 characters of extracted text; formulas that the page renders
  as images did **not** extract — see the fetch-failure section)
- What was read: the whole 고시. Articles used are 제1-2조 (정의 — 기준연령 요건,
  보장성보험, 저축성보험, 금리연동형보험, 평균공시이율, 최적기초율, 참조순보험료,
  요구자본, 충격시나리오방식), 제4-32조 (수수료등 지급기준), 제5-6조 (특별계정의
  설정ㆍ운용), 제5-7조 (특별계정 관련 자금이체), 제6-11조 (책임준비금의 적립),
  제6-11조의4 (적정성 검증), 제6-11조의5 (보증준비금), 제6-11조의6 (해약환급금준비금),
  제6-11조의7 and 제6-13조 (계약자배당), 제6-26조 (특별계정 계약자적립금),
  제7-1조 (지급여력금액), 제7-2조 (지급여력기준금액), 제7-2조의2 (건전성감독기준
  재무상태표), 제7-17조–제7-19조 (적기시정조치), 제7-51조 (신고기준), 제7-60조
  (생명보험의 보험상품설계), 제7-63조 (제3보험의 보험상품설계, including the whole
  실손의료보험 rule set as amended 2026-05-06), 제7-64조 (산출방법서 필수기재사항),
  제7-65조 (계약자적립액의 계산 and the 공시이율 machinery), 제7-66조 (생명보험
  해약환급금의 계산), 제7-67조–제7-70조, and the 부칙 of 금융위원회고시 제2022-53호
  (the K-ICS and 해약환급금준비금 commencement provisions).
- Comparison version also retrieved: **[시행 2023. 3. 2.] [금융위원회고시 제2023-10호]**
  (admRulSeq 2100000220196), used to date the 2023–2026 amendments. Notable drift: the
  filing document is renamed from "보험료 및 **책임준비금** 산출방법서" to "보험료 및
  **해약환급금** 산출방법서" in 제7-69조 and 제7-70조 by the current text.

### S4 — 보험업감독규정 [별표 14] 표준해약환급금계산시 적용되는 해약공제액 (제7-66조 관련)
- Publisher: 금융위원회, schedule to S3
- Version marker on the schedule: **<개정 2011.1.24, 2015.5.7., 2020.1.15.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240711
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927491)
- Accessed: 2026-09-03
- Retrieved: yes (1-page PDF, text extracted cleanly and in full)
- What was read: the complete statement of Korea's **표준해약공제액** — the statutory cap
  on the surrender charge — with all seven notes, including the 연금저축보험 and
  실손의료보험 special cases. This is the single most model-relevant page of Korean
  regulation in the whole file; it is reproduced verbatim in §16.

### S5 — 보험업감독규정 [별표 15] 보험가입금액의 산정 (제7-67조 관련)
- Publisher: 금융위원회, schedule to S3
- Version marker: **<개정 2011.1.24., 2020.1.15.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3240715
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=164927503)
- Accessed: 2026-09-03
- Retrieved: yes (1-page PDF, full text)
- What was read: how 보험가입금액 (the "sum insured" that enters the 표준해약공제액
  formula) is computed for products that are not plain death cover — the 위험보험료 ratio
  method of 제9호, and the exclusion of nursing-care benefit risk premium from it.

### S6 — 보험업감독업무시행세칙, 금융감독원세칙
- Publisher: 금융감독원 (보험감독국), served by 국가법령정보센터 as a 행정규칙
- Version: **[시행 2026. 9. 10.] [금융감독원세칙, 2026. 8. 28., 일부개정]**
- URL: https://www.law.go.kr/행정규칙/보험업감독업무시행세칙
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2200000108939)
- Accessed: 2026-09-03
- Retrieved: yes (114,610 characters)
- Caveat worth recording: the version law.go.kr serves as current takes effect
  **2026-09-10**, one week after the access date. Facts taken from it are facts about
  the imminent text, not about the text in force on 2026-09-03; where that matters it
  is said at the point of use.
- What was read: 제1-1조, 제1-2조, 제5-13조 (표준사업방법서 및 표준약관 → 별표 14 and
  별표 15 of the 세칙), 제5-16조 (the 공시기준이율 delegation and the four external index
  rates), 제5-17조의2, and the 부칙 dating the 계리적 가정 amendments.

### S7 — 보험업감독업무시행세칙 [별표 27] 공시기준이율 산출 기준 (제5-16조 관련)
- Publisher: 금융감독원, schedule to S6
- Version marker: **<신설 2012.9.26, 개정 2013.12.17., 2018.11.6., 2022.12.23.,
  2025.10.28.>**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295679
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885941)
- Accessed: 2026-09-03
- Retrieved: yes (3-page PDF, full text; two weight formulas render as images and did
  not extract, noted at the point of use)
- What was read: the complete 공시기준이율 formula — the α-weighted blend of an objective
  external index rate and the insurer's own 운용자산이익률, the four index instruments,
  the three-month weighted moving average, the 0.5 percentage-point rounding of the
  weights, and the 60% cap on α.

### S8 — 보험업감독업무시행세칙 [별표 15] 표준약관 (제5-13조제1항 관련)
- Publisher: 금융감독원, schedule to S6
- Version markers: 생명보험 표준약관 **<개정 … 2024.12.20., 2025.3.31., 2025.6.30.>**;
  실손의료보험 표준약관 amended **2026.5.6.**
- URL: https://www.law.go.kr/LSW/admRulBylContentsInfoR.do?bylSeq=3295613
  (PDF at https://www.law.go.kr/LSW/flDownload.do?flSeq=168885301)
- Accessed: 2026-09-03
- Retrieved: yes (**492-page PDF**, 441,610 characters extracted; the 장해분류표 and
  재해분류표 appendix tables extracted as running text, some tabular layout lost)
- What was read: the 표준약관 table of contents and then, in full, **Ⅰ. 생명보험**
  (제1조–제43조 plus 부표) and, of **Ⅱ. 손해보험**, the 실손의료보험 family: 기본형
  실손의료보험(급여), 실손의료보험 특별약관1(중증 비급여) and 실손의료보험 특별약관2
  (비중증 비급여). This is the definitive statement of the contract mechanics every
  Korean policy must contain — 보험나이, 청약철회, the three-month 품질보증해지, 계약 전
  알릴 의무 and its time bars, 납입최고 and 부활, 해약환급금, 보험계약대출 — and of the
  **fifth-generation 실손** design that took effect 2026-05-06.

### S9 — 상법 (제4편 보험), 법률 제20991호
- Publisher: 국가법령정보센터 (법제처) — 법무부 소관
- Version: **[시행 2026. 7. 23.] [법률 제20991호, 2025. 7. 22., 일부개정]**
- URL: https://www.law.go.kr/법령/상법
  (body from https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=…&efYd=20260723)
- Accessed: 2026-09-03
- Retrieved: yes (631,670 characters; 제4편 보험 read in full)
- What was read: 제638조 through 제739조의3 — the general part (제638조–제664조), 인보험
  (제727조–제729조), 생명보험 (제730조–제736조), 상해보험 (제737조–제739조) and 질병보험
  (제739조의2–제739조의3). This is the *contract* law; 보험업법 is the *supervisory* law,
  and Korean practice keeps them strictly apart.

### S10 — 소득세법, 법률
- Publisher: 국가법령정보센터 (법제처) — 기획재정부 소관
- Version: **[시행 2026. 7. 1.]** (lsiSeq 280405, efYd 20260701)
- URL: https://www.law.go.kr/법령/소득세법
- Accessed: 2026-09-03
- Retrieved: yes (356,757 characters)
- What was read: 제16조 (이자소득 — 제1항제9호 저축성보험의 보험차익 and its two
  exclusions), 제20조의3 (연금소득), 제59조의3 (연금계좌세액공제), 제59조의4
  (특별세액공제 — 보장성보험료), 제129조 (원천징수세율). The 연금소득 withholding-rate
  age table in 제129조제1항제5의2호가목 is rendered as an image and did **not** extract.

### S11 — 소득세법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 7. 1.]** (lsiSeq 286211, efYd 20260701)
- URL: https://www.law.go.kr/법령/소득세법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (624,319 characters)
- What was read: 제25조 (저축성보험의 보험차익 — the complete 10-year, ₩100,000,000,
  월적립식 and 종신형 연금보험 exemption conditions) and 제40조의2 (연금계좌 등 — the
  ₩18,000,000 annual contribution ceiling, the 55-and-five-years 연금수령 test and the
  연금수령한도 machinery).

### S12 — 상속세 및 증여세법, 법률
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 1. 2.]** (lsiSeq 276123, efYd 20260102)
- URL: https://www.law.go.kr/법령/상속세 및 증여세법
- Accessed: 2026-09-03
- Retrieved: yes (148,788 characters)
- What was read: 제8조 (상속재산으로 보는 보험금) and 제34조 (보험금의 증여).

### S13 — 금융소비자 보호에 관한 법률, 법률
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2026. 1. 2.]** (lsiSeq 277247, efYd 20260102)
- URL: https://www.law.go.kr/법령/금융소비자 보호에 관한 법률
- Accessed: 2026-09-03
- Retrieved: yes (62,444 characters)
- What was read: 제46조 (청약의 철회) in full — the statutory cooling-off right that the
  표준약관 implements.

### S14 — 예금자보호법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처) — 금융위원회 소관
- Version: **[시행 2025. 9. 1.]** (lsiSeq 273001, efYd 20250901)
- URL: https://www.law.go.kr/법령/예금자보호법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (46,515 characters)
- What was read: 제18조 (보험금의 계산방법의 예외 등), in particular **제7항**, which sets
  the protection limit and its per-bucket application. This is the article that
  supersedes the ₩50,000,000 figure that Korean consumer material carried until 2025.

### S15 — 국민건강보험법, 법률
- Publisher: 국가법령정보센터 (법제처) — 보건복지부 소관
- Version: **[시행 2026. 1. 2.]** (lsiSeq 276651, efYd 20260102)
- URL: https://www.law.go.kr/법령/국민건강보험법
- Accessed: 2026-09-03
- Retrieved: yes (98,719 characters)
- What was read: 제41조 (요양급여 and the 급여/비급여 boundary), 제42조 (요양기관 — the
  institution classes the 실손 co-payment table keys off), 제44조 (비용의 일부부담 and
  the 본인부담상한제).

### S16 — 노인장기요양보험법, 법률 제21690호
- Publisher: 국가법령정보센터 (법제처) — 보건복지부 소관
- Version: **[시행 2026. 5. 26.] [법률 제21690호, 2026. 5. 26., 일부개정]**
- URL: https://www.law.go.kr/법령/노인장기요양보험법
- Accessed: 2026-09-03
- Retrieved: yes (133,932 characters)
- What was read: 제2조 (정의 — 노인등, 장기요양급여 and the six-month test), 제15조
  (등급판정 등), 제23조 (장기요양급여의 종류), 제39조 (급여비용의 산정), 제40조
  (본인부담금).

### S17 — 노인장기요양보험법 시행령, 대통령령
- Publisher: 국가법령정보센터 (법제처)
- Version: **[시행 2026. 5. 12.]** (lsiSeq 286011, efYd 20260512)
- URL: https://www.law.go.kr/법령/노인장기요양보험법 시행령
- Accessed: 2026-09-03
- Retrieved: yes (42,367 characters)
- What was read: **제7조 (등급판정기준 등)** in full — the 장기요양인정점수 thresholds for
  등급 1 to 5 and 인지지원등급, which is the statutory definition of the trigger for
  `LTC_KR_S`.

### S18 — 보험업법 제4조 (보험업의 허가), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr), a third-party statute and case mirror
- URL: https://casenote.kr/법령/보험업법/제4조
- Accessed: 2026-09-03
- Retrieved: yes
- What was read: 제4조제1항 in its three-list form. Used only as a cross-check on S1;
  every fact is also present in S1, which is the authoritative retrieval. Recorded
  because it was the first route that returned article text when the law.go.kr friendly
  URL returned only a shell.

### S19 — 보험업법 제5조 (허가신청서 등의 제출), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr)
- URL: https://casenote.kr/법령/보험업법/제5조
- Accessed: 2026-09-03
- Retrieved: yes
- What was read: the four attachments to a licence application, including the
  three-document definition of 기초서류 — 사업방법서, 보험약관, 보험료 및 해약환급금의
  산출방법서. Cross-checked against S1.

### S20 — 보험업법 제2조 (정의), CaseNote 조문 view
- Publisher: CaseNote (casenote.kr)
- URL: https://casenote.kr/법령/보험업법/제2조
- Accessed: 2026-09-03
- Retrieved: in part (the summariser returned the numbered definitions but compressed
  the 가/나/다 sub-items)
- What was read: 제1호 보험상품 and the 생명보험상품 / 손해보험상품 / 제3보험상품 split.
  Superseded in every particular by S1, which returned the article verbatim.

### S21 — 보험업법 (대한민국), 위키문헌
- Publisher: ko.wikisource.org
- URL: https://ko.wikisource.org/wiki/보험업법_(대한민국)
- Accessed: 2026-09-03
- Retrieved: yes, but the text is **법률 제8902호, 시행 2008. 6. 15.** — seventeen years
  out of date
- What was read: nothing is cited from it. It is listed because it was tried and
  because a future reader should know that this mirror is stale and must not be used.

### S22 — 보험업감독규정, 금융위원회고시 제2023-10호 (comparison version)
- Publisher: 금융위원회
- Version: **[시행 2023. 3. 2.]**
- URL: https://www.law.go.kr/admRulLsInfoP.do?admRulSeq=2100000220196
  (body from https://www.law.go.kr/LSW/admRulLsInfoR.do?admRulSeq=2100000220196)
- Accessed: 2026-09-03
- Retrieved: yes (207,084 characters)
- What was read: the same articles as S3, to date amendments. Used only for
  before/after statements; all current-law facts are cited to S3.

---

## Regulatory and actuarial references

### R1 — 금융위원회·금융감독원, 제4차 보험개혁회의 보도자료 (계리가정·할인율)
- Publisher: 금융위원회 보험과 / 금융감독원 보험리스크관리국
- Date: 보도 2024-11-07, 배포 2024-11-06; the meeting was 2024-11-04
- URL: https://www.fsc.go.kr/no010101/83351
  (attachments at `…/comm/getFile?srvcId=BBSTY1&upperNo=83351&fileTy=ATTACH&fileNo=1`
  and the same with `fileNo=4`)
- Accessed: 2026-09-03
- Retrieved: yes (the 6-page 보도자료 PDF and the 6-page 별첨 「보험부채 할인율 현실화
  연착륙 방안」 PDF, both extracted in full; attachments 2, 3 and 5 are HWP/HWPX and were
  not converted)
- What it is good for: the **무·저해지 해지율** log-linear model and its 0.1% convergence
  point, the 0.8% post-완납 ultimate lapse rate, the ≥30% additional lapse at a
  단기납 종신보험 bonus date, the age-cohort loss-ratio requirement, the
  무·저해지 share-of-new-business series, and the whole IFRS 17 discount-curve
  architecture (LOT, LTFR 4.55%, liquidity premium 91bp) with its phase-in dates. This
  is the most important single supervisory document for `krlib`'s lapse assumptions.

### R2 — 금융감독원, 「2024년 실손의료보험 사업실적(잠정)」
- Publisher: 금융감독원 보험계리상품감독국 보험상품제도팀
- Date: 보도 2025-05-13, 배포 2025-05-12
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=266435
  (PDF via https://eiec.kdi.re.kr/policy/callDownload.do?num=266435&filenum=1)
- Accessed: 2026-09-03
- Retrieved: yes (7-page PDF, full text)
- What it is good for: the definitive quantitative picture of 실손의료보험 — contract
  counts by generation, premium income, 보험손익, 경과손해율 overall and by generation,
  premiums by generation for a 40-year-old male, the 급여/비급여 claims split, the
  claim concentration in 비급여 주사제 and 근골격계, claims by institution class, and
  average 비급여 claim per contract by generation. It also reproduces the
  co-payment-rate-by-generation table and the April 2025 reform design.

### R3 — 금융감독원, 「2025년 9월말 기준 보험회사 지급여력비율 현황」
- Publisher: 금융감독원
- Date: 2026-01-06
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=275691
- Accessed: 2026-09-03
- Retrieved: in part (the KDI summary page returned the headline ratios; the underlying
  PDF was not downloaded)
- What it is good for: K-ICS ratios after 경과조치 at 2025-09-30 — all insurers 210.8%,
  생보 201.4%, 손보 224.1%. Component amounts (지급여력금액, 지급여력기준금액) were not
  on the page.

### R4 — 금융위원회, 新회계·자본제도에 맞춘 보험업권 자본규제 고도화
- Publisher: 금융위원회 보험과
- Date: 2025-03-12
- URL: https://www.fsc.go.kr/no010101/84128
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the size of the capital-regime shift — 요구자본 ₩67.9조 under RBC
  at 2022-12-31 against ₩118.9조 under K-ICS at 2024-09-30; the 기본자본 K-ICS ratio
  series; 2024 capital-securities issuance; the 비상위험준비금 reform.

### R5 — 금융위원회, 무(저)해지환급금 보험 상품구조 개선 (감독규정 입법예고)
- Publisher: 금융위원회 보험과
- Date: 2020-07-27
- URL: https://www.fsc.go.kr/no010101/74468
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the origin and the arithmetic of the 무·저해지 환급률 cap that now
  sits in 보험업감독규정 제7-66조제4항제2호 — a worked 20-year 종신보험 comparison of
  97.3% (표준형) against 134.1% (무해지) and the rule that limits the latter to the
  former. Also the count of carriers writing the form in 2020.

### R6 — 금융위원회, 「오늘부터 새로운 예금보호한도 1억원 시대가 열립니다」
- Publisher: 금융위원회
- Date: published 2025-09-01 (release dated 2025-08-29)
- URL: https://www.fsc.go.kr/no010101/85200
- Accessed: 2026-09-03
- Retrieved: in part (title, dates and the general statement; the release as summarised
  does not itemise the insurance-specific buckets)
- What it is good for: dating the increase of the deposit-protection limit to
  ₩100,000,000. The per-bucket mechanics come from S14, which is authoritative.

### R7 — 금융위원회, 실손의료보험 개혁방안 보도자료 (5세대 설계)
- Publisher: 금융위원회 보험과
- Date: 2025-04-01 (the FSS release R2 refers to the same package as "'25.4.2. 旣발표")
- URL: https://www.fsc.go.kr/no010101/84272
- Accessed: 2026-09-03
- Retrieved: yes (page text)
- What it is good for: the design of **5세대 실손** before it became regulation — the
  급여 co-payment formula, the 중증/비중증 비급여 split with their co-payments and
  limits, the ₩5,000,000 annual co-payment cap on 중증 비급여 inpatient care at tertiary
  and general hospitals, the illustrative premium reductions, the 계약재매입 offer to
  first- and early-second-generation policyholders, and the 2026-07 to 2036-06
  ten-year conversion window.

### R8 — 보험개발원 제10회 경험생명표 — as reported by 보험매일
- Publisher of the underlying table: 보험개발원 (Korea Insurance Development Institute)
- Publisher of the retrieved document: 보험매일 (fins.co.kr), a trade newspaper
- Date: article 2024-01-10 (reporting the KIDI release of early January 2024)
- URL: https://www.fins.co.kr/news/articleView.html?idxno=99460
- Accessed: 2026-09-03
- Retrieved: yes (article text)
- **This is a news article, and it is the only retrieved source for the 제10회
  경험생명표 summary figures.** KIDI's own press-release listing (R22) does not carry a
  경험생명표 item in the range served, and the KIDI 보험정보 빅데이터 플랫폼 page refused
  connection. Facts taken from it are so marked.
- What it is good for: 평균수명 남 86.3세 / 여 90.7세 (up 2.8 and 2.2 years on the 제9회),
  65세 기대여명 남 23.7년 / 여 27.1년 (up 2.3 and 1.9), application from 2024-04 to new
  business only, and the directional premium effect by product class.

### R9 — 국가데이터처, 「2024년 생명표 작성 결과」
- Publisher: 국가데이터처 인구동향과 (the renamed 통계청)
- Date: 2025-12-03
- URL: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156732935
- Accessed: 2026-09-03
- Retrieved: yes (briefing text)
- What it is good for: 기대수명 at birth 2024 — 전체 83.7년, 남 80.8년, 여 86.6년; 65세
  기대여명 남 19.5년 / 여 23.7년; 40세 기대여명 남 41.9년 / 여 47.4년; survival to age
  80 of 64.4% (male) and 82.2% (female); the OECD comparison. This is the **public**
  mortality series that a `[std]` `mort_table.csv` must be anchored on.

### R10 — 통계청, 「2023년 생명표」
- Publisher: 통계청 (as it then was)
- Date: 2024-12-04
- URL: https://www.korea.kr/briefing/policyBriefingView.do?newsId=156664008
- Accessed: 2026-09-03
- Retrieved: yes (briefing text)
- What it is good for: the prior year of the same series — 기대수명 전체 83.5년, 남
  80.6년, 여 86.4년; 65세 기대여명 남 19.2년 / 여 23.6년; and the statement of what a
  Korean 생명표 is ("연령별 사망 수준이 그대로 유지될 경우 …"). Useful as the one-year
  check on R9's trend.

### R11 — 보건복지부·중앙암등록본부(국립암센터), 「2023년 국가암등록통계 참고자료」
- Publisher: 중앙암등록본부 / 국가암정보센터
- Date on the document: **2026-01-20**
- URL: https://www.cancer.go.kr/download.do?uuid=cfcd35c3-391f-4060-9688-641db3d86cbd.pdf
- Accessed: 2026-09-03
- Retrieved: yes (41-page PDF; extracted in full and read)
- What it is good for: everything `Cancer_KR_S` needs that is public — 암발생자수 by year
  and sex 1999–2023, 조발생률 and 연령표준화발생률, the top-ten cancers by sex with
  incidence rates, **평생 암발생/사망 위험도** by site and sex, 5-year relative survival
  by period and site, and 암유병자수 with 유병률. The thyroid-cancer share matters
  because Korean cancer policies pay 갑상선암 at the reduced 유사암 tier.

### R12 — 국민건강보험공단, 2024년도 건강보험환자 진료비 실태조사
- Publisher: 국민건강보험공단
- Date: 2025-12-30
- URL: https://kiri.or.kr/PDF/weeklytrend/20260105/trend20260105_1.pdf
  (the 보험연구원 weekly-trend reprint of the NHIS 보도자료)
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- What it is good for: the public-scheme underlay that 실손의료보험 sits on — 보장률
  64.9%, 법정 본인부담률 19.3%, 비급여 본인부담률 15.8%, the ₩138.6조 total treatment
  cost split into ₩90.0조 보험자부담금 / ₩26.8조 법정본인부담금 / ₩21.8조 비급여, the
  2012–2024 series, and 보장률 by institution class and by age band.

### R13 — 국민건강보험공단, 「장기요양 등급 판정 현황」 (자율공시 / 경영공시)
- Publisher: 국민건강보험공단
- As-of date on the retrieved table: **2026-06-30 (2026년 2/4분기)**
- URL: https://www.nhis.or.kr/announce/wbhaec11503m01.do
- Accessed: 2026-09-03
- Retrieved: yes (table)
- What it is good for: the grade distribution that `LTC_KR_S`'s incidence basis must
  reproduce in aggregate — 총 등급판정 1,411,466명, 인정자 1,275,370명 (90.4%), 등급외자
  136,096명, and the split 1등급 53,844 / 2등급 100,844 / 3등급 333,143 / 4등급 604,307 /
  5등급 151,681 / 인지지원등급 31,551.

### R14 — 보험연구원, 「K-ICS 경과조치 주요 내용과 시사점」 (KIRI 리포트 이슈 분석), 노건엽
- Publisher: 보험연구원 (Korea Insurance Research Institute)
- Date: 2022-03-07
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=139489
- Accessed: 2026-09-03
- Retrieved: yes (PDF, extracted in full)
- What it is good for: the complete inventory of K-ICS 경과조치 — which four items may be
  phased in over ten years, the eligibility tests, the 2024-to-2033 10%-a-year
  recognition of the 보험부채 증가분, the biennial and 50bp re-measurement triggers, the
  dividend-payout penalty, the five-year 적기시정조치 deferral, and a side-by-side
  comparison with Solvency II's transitionals.

### R15 — 보험연구원, 「2026년 보험산업 전망」 (2026년 보험산업 전망과 과제 세미나), 황인창
- Publisher: 보험연구원 금융시장분석실
- Date: 2025-10-21
- URL: http://www.kiri.or.kr/report/downloadFile.do?docId=778039
- Accessed: 2026-09-03
- Retrieved: yes (91-page presentation PDF, extracted in full)
- What it is good for: the market-size tables used in the Market overview section —
  생명보험 수입보험료 by line (보장성/저축성/변액/퇴직연금) for 2023, 2024, 2025(E) and
  2026(E) with growth rates, and the same for 손해보험 원수보험료 (장기손해보험, 개인연금,
  자동차, 일반, 퇴직연금).

### R16 — 한국보험신문, 「2025년 보험사 당기순이익 12.2조원… 생·손보 보험손익 동반 하락」
- Publisher: 한국보험신문 (insnews.co.kr); the figures are attributed in the article to
  금융감독원's 2025년 보험회사 경영실적
- Date: 2026-03-30
- URL: https://www.insnews.co.kr/news/articleView.html?idxno=89914
- Accessed: 2026-09-03
- Retrieved: yes (article text)
- **This is a news article standing in for an FSS release that could not be opened
  directly** (fss.or.kr refused a plain fetch). Facts from it are marked as
  news-sourced.
- What it is good for: 2025 outturn — 수입보험료 ₩266.6595조 (생보 ₩127.5061조, 손보
  ₩139.1533조), the 생보 line split, the 손보 line split, 당기순이익 ₩12.2172조, ROA
  0.94%, ROE 7.86%, 총자산 ₩1,344.2조.

### R17 — 하나생명, 「적용이율 공시 — 표준이율 및 평균공시이율」
- Publisher: 하나생명보험주식회사
- URL: https://www.hanalife.co.kr/anm/interestRate/interestRate_tab6.do
- Accessed: 2026-09-03
- Retrieved: yes (both tables)
- What it is good for: the **평균공시이율 time series** 2016–2026 as published by a
  carrier, and the 표준이율 series 2013–2015 that preceded it. 평균공시이율 is a
  regulatory input (S3 제1-2조제13호) and enters the tax-free-savings test, the 부활
  interest ceiling and the 저축성보험 design test, so its level matters to four of the
  ten products.

### R18 — 교보생명, 「공시기준이율 적용현황」
- Publisher: 교보생명보험주식회사
- URL: https://www.kyobo.com/dgt/web/disclosure/interest-rate-disclosure/status
- Accessed: 2026-09-03
- Retrieved: in part (the rate grid returned; **the month selector's value did not
  return**, so the as-of date of the figures is unknown)
- What it is good for: a worked example of the 공시기준이율 / 적용률 / 적용이율 triple that
  S7 defines, at 3.19% across 보장(무배당), 연금(무배당), 연금(배당), 저축(무배당) and
  연금저축(배당). Because the as-of month is unknown, the level is treated as
  illustrative and is not used as a dated fact.

### R19 — 생명보험협회, 공시실 (pub.insure.or.kr)
- Publisher: 생명보험협회 (Korea Life Insurance Association, KLIA)
- URL: https://pub.insure.or.kr/
- Accessed: 2026-09-03
- Retrieved: yes (landing page and category description)
- What it is good for: establishing what Korean product disclosure contains and where —
  상품비교공시 across eleven protection classes plus savings, variable, retirement and
  실손; 경영공시; 기타공시 (민원, 불완전판매비율, 소송). The comparison tool is the public
  route to 약관, 상품요약서 and 해약환급금 illustrations, and is the reason `krlib`'s
  product research files can cite real Korean product parameters at all.

### R20 — 생명보험협회, FACT BOOK
- Publisher: 생명보험협회
- URL: https://www.klia.or.kr/consumer/stats/factbook/list.do
- Accessed: 2026-09-03
- Retrieved: in part (edition list and contents description; the 2025 edition PDF itself
  was not downloaded)
- What it is good for: editions run 2001–2025; the 2025 edition covers FY2024 with
  contract, financial, reserve, asset, distribution and **생명표** sections. Recorded as
  the standard annual reference; no number in this file is taken from it.

### R21 — 생명보험협회, 금융통계월보(생명보험편)
- Publisher: 생명보험협회, with 보험개발원 preparing tables 5–9
- URL: https://www.klia.or.kr/consumer/stats/statHomSta/financeStats.do
- Accessed: 2026-09-03
- Retrieved: in part (structure and provenance; the monthly tables are behind a query
  form and were not retrieved)
- What it is good for: knowing that the monthly life series is a 통계청 국가승인통계 built
  from insurers' 업무보고서, with 보유계약, 보장성/저축성 split, 지급유형별
  보험금·환급금·배당금, 경과기간별 보험료수익 and 부문별 손익 prepared by KIDI.

### R22 — 보험개발원, 보도자료 listing
- Publisher: 보험개발원
- URL: https://www.kidi.or.kr/user/nd11592.do
- Accessed: 2026-09-03
- Retrieved: yes (listing, items 742–746, dated 2026-06-02 to 2026-08-18)
- What it is good for: negative evidence. The visible listing carries **no** 경험생명표,
  참조순보험요율 or 보험통계 item, which is why the 제10회 경험생명표 figures in this file
  rest on R8, a newspaper.

### R23 — 한국회계기준원 회계기준위원회, 「"보험계약" 국제회계기준(K-IFRS 제1117호) 제정 의결」
- Publisher: 한국회계기준원 (Korea Accounting Institute), mirrored by KDI 경제교육·정보센터
- Date of the resolution: **2018-05-25**
- URL: https://eiec.kdi.re.kr/policy/materialView.do?num=177159
- Accessed: 2026-09-03
- Retrieved: in part (the release body returned; the 별첨 HWP with the standard's
  substance was not converted)
- What it is good for: dating the Korean adoption of IFRS 17 as 기업회계기준서 제1117호
  「보험계약」. The release states an effective date of 2021-01-01, which was the
  pre-deferral date; the operative commencement of 2023-01-01 is established from S3's
  부칙 and from R4.

### R24 — 국민건강보험공단, 「2024 노인장기요양보험 통계연보」, as reported by 메디칼월드뉴스
- Publisher of the underlying yearbook: 국민건강보험공단
- Publisher of the retrieved document: 메디칼월드뉴스 (medicalworldnews.co.kr)
- URL: https://www.medicalworldnews.co.kr/m/view.php?idx=1510968457
- Accessed: 2026-09-03
- Retrieved: **no** — the item was returned only as a search-result summary; the article
  page itself was not opened
- What it would be good for: 2024 인정자 1,165천명 (+6.1%), 신청자 1,478천명 (+3.4%),
  판정 대비 인정률 89.5% (+0.9%p), the grade split (4등급 46.0%, 3등급 26.7%, 5등급 11.6%,
  2등급 8.5%, 1등급 4.8%, 인지지원 2.4%) and 급여비용 ₩16조1,762억 (+11.6%) with a
  공단부담률 of 91.3%. Every one of those figures is **[unverified]**; the grade
  *distribution* is independently corroborated by R13, which was retrieved.

### R25 — 보험저널, 2026년 보험료 전망 및 평균공시이율 관련 기사
- Publisher: 보험저널 (insjournal.co.kr), a trade outlet
- URL: https://www.insjournal.co.kr/news/articleView.html?idxno=29000
  (companion: …?idxno=29053)
- Accessed: 2026-09-03 (search-result summaries; the article pages were not opened)
- Retrieved: **no** (summary only)
- What it would be good for: the market's reading of the 2026 평균공시이율 cut to 2.50%
  and its transmission into 예정이율 and premium rates, and the statement that 보장성
  공시이율 stood at 2.2%, 연금 2.29% and 저축 2.22% at the month before the report. All of
  that is **[unverified]** here; the 평균공시이율 level itself is separately verified from
  R17.

### R26 — 금융감독원, 「2025년 3월말 / 6월말 기준 보험회사 지급여력비율 현황」
- Publisher: 금융감독원, mirrored by KDI 경제교육·정보센터
- URLs: https://eiec.kdi.re.kr/policy/materialView.do?num=267710 and
  https://eiec.kdi.re.kr/policy/materialView.do?num=271247
- Accessed: 2026-09-03
- Retrieved: **no** (listed in search results; neither page was opened)
- Recorded so that a later drafter has the quarter-by-quarter series to hand. Only R3's
  September 2025 figures are used.

### R27 — 보험연구원, 「2025년 보험산업 주요 이슈: ② IFRS17 및 K-ICS」
- Publisher: 보험연구원
- URL: https://www.kiri.or.kr/report/downloadFile.do?docId=618289
- Accessed: 2026-09-03
- Retrieved: **no** (identified in search results, not downloaded)
- Would carry the 2023–2025 supervisory-guideline chronology in one place, including the
  2023 실손의료보험 계리가정 산출기준 that R1 supersedes only in part.

### R28 — 금융감독원, 보험회사 종합공시 / 금융감독원 공식 사이트
- Publisher: 금융감독원
- URL: https://www.fss.or.kr
- Accessed: 2026-09-03
- Retrieved: **no** — a plain HTTPS request returned "Empty reply from server"; the site
  did not respond to the fetcher at all
- Consequence: every FSS release used in this file was obtained through a mirror (KDI
  경제교육·정보센터 for R2, R3) or through a trade newspaper (R16). Where only the
  newspaper route exists, the fact is marked as news-sourced.

---
