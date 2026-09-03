# Product Specification

**Status:** Draft, 2026-09-03 (every cited source accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a Korean **children's insurance (어린이보험, *eorini
boheom*)** contract — a fixed-benefit (정액, *jeongaek*) 제3보험 (*je-sam boheom*,
third-sector) policy written on a child, very often **before the child is born**, running
from birth to a 100세 만기 (*mangi*, expiry), and consisting of a small accidental-disability
basic contract carrying a very large bundle of riders. It describes **no single insurer's
contract**, and it must not be read as one.

Facts carrying a source tag — [S#] (primary product documents: 보험약관 (*boheom yakgwan*,
policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory pre-contract product
summary), and the 손해보험협회 comparison-disclosure board) and [R#] (product-specific
supervisory, statutory and research references), both numbered per `_research/child.md` and
resolved in `sources.md` in this directory (numbering frozen, never renumbered), and
[REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct and
also frozen) — name the document the claim was read from. Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] row carries a
numbered footnote giving the rationale and, where the research file brackets it, the range
observed across insurers. Claims no retrieved document could confirm are flagged
[unverified].

The composite is drawn from **eleven carriers**. Five current 상품요약서 from five 손해보험
(non-life) writers give the benefit menus, the issue-age grids, the 면책기간 matrix and three
complete cash-value tables [S2] [S3] [S4] [S5] [S6]; one 2019 상품요약서 from the same line as
[S3] gives the pre-2023 issue ages, the graded 무해지 scale and the only **published pricing
lapse rates and the only published incidence rate** in the whole file [S1]; three 약관 —
two 생명보험 (life) and one 손해보험 — give the 태아가입특칙 verbatim, the 생명보험 form of
the premium waiver and a pure 비갱신 무해지 wording [S8] [S9] [S10] [S12]; one 약관 gives the
갱신형 architecture and the 보험나이 article with its worked example [S7]; and the
손해보험협회's regulated comparison board supplies **41 products from 10 carriers** with their
published premiums, 예정이율, 공시이율, 최저보증이율 and 보험가격지수 [S11]. Two documents
could not be used: a 생명보험 약관 whose CID-keyed fonts defeated extraction [S14] and a
carrier product page whose two fetches returned mutually contradictory renderings [S15]; a
third is used only as a marker of [unverified] figures [S16]. Company and branded product
names appear only in `sources.md` and in `_research/child.md`.

**Deltas against the fixed-benefit 제3보험 chassis.** The
[cancer specification (암보험)](../cancer/product-spec.md) is `krlib`'s 정액 제3보험 chassis:
diagnosis-triggered lump sums on a tier ladder keyed to the KCD, a 90-day 면책기간 whose
breach makes the affected cover void, a 감액기간 on top of it, a 유사암 reduced tier, a
premium waiver correlated with the diagnosis benefit, and a contract with no death benefit
that pays the 계약자적립액 (*gyeyakja jeongnipaek*, the policyholder's account balance) on a
death it does not cover. `Child_KR_S` inherits all six and changes six things. Three of them
have no counterpart anywhere in this repository.

1. **태아가입 (*taea gaip*, foetal enrolment): the contract is written before the insured
   exists.** A 태아 has no legal personality and cannot be the 피보험자 of an 인보험
   contract, so the 태아가입특칙 makes the foetus the insured **at birth** [S8 제54조] [R3].
   Cover attaches at birth and not at the 계약일 — sixteen insurers were ordered in 2016 to
   stop advertising otherwise [R2] — the 계약나이 is fixed at 0 at the 계약일 [S8 제60조], the
   contract is **priced male** because the sex is unknown and trued up after delivery [R3]
   [S8], and if the pregnancy ends in 유산 (miscarriage) or 사산 (stillbirth) the contract is
   **무효** and every premium is returned [S8 제56조]. The projection therefore opens on a life
   that does not yet exist, and its first months carry premium income, a void decrement and a
   short pre-birth benefit term, but no mortality and no morbidity on the insured at all.
2. **보험료 납입면제 on the 계약자 (*gyeyakja*, policyholder): a premium-waiver decrement on a
   life who is not the insured.** On the 생명보험 form the waiver fires on the child's cancer
   diagnosis or 50% disability **or on the 계약자's own death or 50% disability**, in one
   clause [S10 제22조]; the clause works because that wording makes the 피보험자 of the contract
   「계약자와 가입자녀」 — the policyholder is himself an insured [S10 제3조]. On the 손해보험
   form the same economics arrive as a compulsory 부양자 (dependant-supporter) death rider
   written on the parent's own life, obligatory on any 태아 contract [S5] [S11]. Either way the
   model carries **two decrement lives**, and the premium stream stops on the earlier of two
   events drawn from two different mortality tables.
3. **The 면책기간 is disapplied below 보험나이 15, and entirely on a 태아 contract.** The
   90-day cancer waiting period that defines the chassis was removed for 어린이보험 in 2006 on
   the reasoning that there was no evidence of anti-selection or of a 위험률차손 at child ages
   [R5]; current wordings implement it as 「최초계약과 부활계약의 면책기간은 **보험나이 15세
   이상인 경우에만 적용**」 [S3], and a 태아가입용 rider has 「면책기간 없음」 at all [S3]. The
   chassis's sharpest anti-selection control is switched off for the first fifteen years of a
   hundred-year contract.
4. **There is no 감액기간, and on a 태아 contract there may not be one.** The market has moved
   to 감액없음 and prints the word in the benefit names themselves [S1] [S3] [S11]; where a
   감액 survives it is a first-year 50% [S6] [S11]. And a supervisory 변경권고 of 2015 removed
   the 감액 for contracts written while the insured was a foetus, across 17 carriers and 56
   products, with the before-and-after wording set out side by side [R2].
5. **No death benefit below 만 15세, by statute rather than by design.** `Cancer_KR_S` has no
   death benefit because the composite chose not to carry one; `Child_KR_S` may not have one.
   상법 제732조 makes a contract on the death of a person under 15 **void**, and the 표준약관
   restates it at 제19조제2호 with an express refusal to extend the age-correction saving to it
   [R7] [REG-R50] [REG-R25]. 제739조 disapplies 제732조 to 상해보험, so an accidental-death
   cover on a child is lawful, but the market does not write one below 15 [S1] [S4] [S11].
6. **The benefit is a bundle, not a ladder.** The basic contract is a 상해후유장해 (accidental
   residual-disability) cover paying **보험가입금액 × 장해지급률** on a continuous percentage
   scale [S1] [S2] [S4] [S5] [S11]; the cancer, cerebrovascular and cardiac diagnosis benefits
   the chassis is built around are three riders among more than a hundred [R5]. Two whole rider
   blocks are written **on other lives** — the 부양자 stack on the parent and the 임신·출산질환
   stack on the mother — and one, 가족일상생활배상책임, is a **third-party liability** cover
   that only a non-life licence may attach [R5] [S5].

The horizon is the other structural fact. At 계약나이 0 to a 100세 만기 the projection runs
**1,200 monthly periods**, the longest in `krlib`, and the premium is paid over the first 240
of them. A child policy is a seventy-to-hundred-year guarantee on a bundled rider stack
whose morbidity has barely begun, written on a life whose sex is not yet known.

---

## Product overview and market role

### What an 어린이보험 is, and the two licences that write it

The industry disclosure board's own definition is 「태아·어린이를 포함한 성장기 자녀에게
발생할 수 있는 질병과 상해위험을 보장하는 보험」 [R12]. The supervisor's older and fuller
formulation adds the liability limb and the issue-age band: 「자녀의 성장 과정 중 발생할 수
있는 질병·상해로 인한 의료비와 자녀의 일상생활 중 발생하는 배상책임 등을 보장하는
보험상품(가입연령 : 0세~15세)」 [R2].

It is 제3보험 business — 상해보험 and 질병보험 together, under 보험업법 제2조제1호다목 and
제4조제1항제3호 — and 제4조제3항's deeming provision makes the class writable by a life or a
non-life insurer alike [REG-R1]. In this product the two licences have **not** converged, and
that is the first thing a specification has to get right. 보험연구원's account is direct:
「어린이 보장성 상품은 손해보험회사를 중심으로 판매되고 있으며, 생명보험회사는 변액과
연금의 강점을 내세워 어린이 저축성 상품 시장을 선점」, and it attributes the split to the
fact that only a non-life insurer may attach **배상책임담보** and **비용담보** [R5]. The
손해보험협회's comparison board carries **41 products from 10 non-life carriers** [S11]; there
is no 생명보험 counterpart to it in this file, and that absence is the largest single gap
behind this document.

The composite is therefore drafted as a **non-life carrier's 장기손해보험**, which 감독규정
제7-61조 designs identically to a 제3보험 contract by applying the whole of 제7-63조 to it
[REG-R17], with one deliberate exception: the **premium waiver is taken from the 생명보험
form** [S10 제22조], because that is the only retrieved wording in which the 계약자's death is
a contractual event of the main contract rather than the benefit of a separate rider, and
because the 계약자 waiver is one of the two mechanics this product exists to demonstrate.

Structurally, the contract is a **small 기본계약 plus a very large 특별약관 stack**. At every
non-life carrier examined the 기본계약 is a 상해후유장해 cover paying 가입금액 × 장해지급률
[S1] [S2] [S4] [S5] [S11]; everything else — cancer diagnosis, cerebrovascular and ischaemic
heart diagnosis, surgery, hospital cash, fracture, burn, liability, the foetal covers, the
parent covers, the mother covers — is a rider. The rider count is a competitive strategy and
not an accident: by 2018 a child policy carried 「100여개 이상의 질병 및 상해사고에 대한 보장
담보」 [R5], [S1]'s eligibility section runs the riders together in continuous prose over
several pages, and [S2]'s runs to roughly forty pages of tables.

Naming is not standardised — 어린이보험, 자녀보험, 아이보험, 태아보험 and branded names all
appear, and the 2023 supervisory restriction bites on the **name** rather than the design
[R1], so a product sold at older issue ages may be renamed rather than restructured.

### 태아보험 is not a product — it is an 어린이보험 with a 특칙 attached

The 태아보험 (*taea boheom*) of ordinary Korean speech has no separate legal existence. The
supervisor says so:

> 법규 상 '태아보험'이라는 별도의 보험상품은 없으나, 어린이보험에 태아가입특약(胎兒加入
> 特約)이 첨부되어 출생 전 태아 상태에서 보험가입이 가능한 상품을 실무적으로 '태아보험'
> 으로 지칭하고 있음
> \* 태아는 법적으로 인격(人格)을 갖지 못하므로 인보험의 보호대상이 될 수 없음. 따라서
> 태아의 출생을 조건으로 하는 '태아가입특약'을 통해 태아를 대상으로 한 보험계약을 체결

and, in one line, 「태아보험 = 어린이보험 + 출생시 위험보장」 [R3].

It is not a fringe variant. In FY2007 **335,135 of 1,622,639 new child contracts — 20.7% —
were written in utero**, and about the same fraction of premium [R3]. The 태아가입특약 was
introduced in 2000 and 보험연구원 calls it the single largest contributor to the product's
growth [R5]. Every current 상품요약서 retrieved offers it, with 가입나이 written as 「태아」
at the head of the issue-age grid [S2] [S3] [S4] [S5] [S6].

### The market: size, share and the shape of the in-force book

**Current size, from a primary supervisory document.** 어린이보험 annual premium is
**₩9.4조원**, against about **₩42.7조원** for all 보장성 인보험, both as at 2026-03 [R6]. That
puts 어린이보험 at roughly **22% of all Korean protection personal-lines premium** — a
remarkable share for a product sold to a cohort that is shrinking every year.

**Historic size and the reversal of the licence split** [R3], 참고자료2, 수입보험료 in 억원:

| | FY05 | FY06 | FY07 | 신계약건수 FY07 (태아가입) |
|---|---|---|---|---|
| 생명보험 | 23,947 | 24,888 | 23,995 | 583,888 (138,965) |
| 손해보험 | 3,936 | 5,888 | 8,406 | 1,038,751 (196,170) |
| 합계 | 27,883 | 30,776 | 32,401 | 1,622,639 (335,135) |

In FY07 the market was ₩3.24조원 and **74% of it was 생명보험**; the 손해보험 side then
doubled in two years while the 생명보험 side was flat, which is the 굿앤굿어린이CI보험 effect
[R5]. Today the position is reversed. **In-force, 2013–2015**, sourced by the FSS to
보험개발원: 보유계약 1,141만건 (2013.4–12) → 1,182만건 (2014) → 1,162만건 (2015 잠정), with
수입보험료 ₩33,385억 → ₩45,611억 → ₩44,906억 and 신계약 88만건 → 127만건 → 123만건 against
출생자수 of 43.7만 / 43.5만 / 43.9만 [R2]. New child contracts ran at roughly **three times the
birth count** — which is what a multi-rider, multi-contract product looks like in a count
statistic, and a warning that "contracts" in Korean insurance statistics are not "insured
children".

**Growth against a falling birth rate, and the mechanism.** 보험연구원 predicted in 2018 that
「출산율 저하에 따라 15세 미만 인구 수가 지속적으로 줄어들어 어린이보험의 시장규모가 앞으로
크게 성장할 가능성은 낮다」 [R5] and was wrong: ₩3.24조원 (FY07) [R3] and ₩4.49조원 (2015)
[R2] became ₩9.4조원 by 2026 [R6]. The mechanism is the one [R5] itself identified — the
**term extension**. A 100세만기 policy written at age 0 collects premium for twenty years and
stays in force for a hundred, so the in-force premium grows even as the cohort shrinks. That
is also the whole of the product's IFRS 17 problem, and it is why this reference model runs
1,200 periods.

**Loss ratio.** [R5], writing in 2018: 「어린이보험의 손해율은 보험회사 평균 손해율(약 80%
수준) 미만인 것으로 알려져 있어 우려할 만한 수준은 아니지만, 이러한 담보경쟁은 향후
어린이보험의 손해율이 높아질 가능성이 매우 높다」. Two documented deteriorations exist: the
2010 outpatient riders, whose frequent infant colds and fevers were accumulated and claimed
together with the then-attachable 실손 rider, and the 2013 requirement to pay neonatal claims
on the diagnosis name rather than the KCD code, which ended refusals of 뇌출혈 claims coded
**P52** and raised frequency sharply [R5]. **No current loss-ratio figure for 어린이보험 was
retrieved** and none is asserted here.

### How the product reached 100세 만기, and the 2023 supervisory action

The line is old and the dates are known [R5] unless marked. 1958-07: 진학보험, Korea's first
education endowment. 1960s–1980s: 교육보험 is the dominant individual product, over half the
individual market at its peak. From 1990 it declines as tuition inflation outruns the benefit.
**1997**: the first true 어린이 보장성 상품, at 가입연령 2~14세 and 15/20년 or 18/22세만기, with
a 사망위로금 that returned premiums if death occurred before 15. **2000**: the 태아가입특약.
**2003** and **2004-07**: the first child CI products, the second of which [R5] describes as
the best-selling child policy ever written in Korea, at 주피보험자 태아~15세, 피부양자 20~50세
and 보험기간 15/18/20세만기. **2005**: high-cost critical-illness benefits. **2006**: the
90-day cancer waiting period is removed for 어린이보험. **2010**: outpatient riders, and their
loss experience. **2011**: the move to **100세 만기**, after which a hundred-year term becomes
the norm and adult-disease covers are bolted on for the post-30 segment of the term.
**2012-10-01**: all foetuses of a multiple pregnancy become insurable [R4]. **2013-09**: the
P-code decision. **2015-06-17 → 2016-04**: the 감액 for foetal contracts is removed [R2].
**2016-07**: sixteen carriers are ordered to stop advertising cover before birth [R2].

**2023-07-19** is the datable intervention and it is easy to get wrong. It is a **감독행정**
(supervisory administration), not a rule change, announced in a 보도자료 distributed
2023-07-19 for publication on 2023-07-20, with existing products to be amended by the end of
**2023-08** [R1]. The 어린이보험 section reads, verbatim:

> **2 어린이보험**
> □ (현황 및 문제점) 가입연령을 35세까지 확대함에 따라 어린이 특화 상품에 성인이
> 가입하는 등 불합리한 상품 판매 심화
> ◦ 또한, 어린이에게 발생빈도가 극히 희박한 뇌졸중, 급성심근경색 등 성인질환 담보를
> 불필요하게 부가
> □ (추진방안) 최대 가입연령이 15세를 초과하는 경우 '어린이(자녀)보험' 등 소비자 오인
> 소지가 있는 상품명 사용 제한

Three things follow that this document has to get right. First, **the measure restricts the
product name, not the issue age**; a carrier remains free to sell at issue ages above 15, it
may not call the result an 어린이보험. In practice every carrier cut the age, and the current
상품요약서 show 태아~15세 [S2] [S4]. Second, the second limb is a **supervisory statement
about the morbidity basis**: the adult-disease riders on a 100세만기 child policy are priced
on an exposure that barely exists for the first three decades of the term. Third, the framing
is prudential as well as conduct — the release names 「보험계약마진(CSM) 증대 등을 위한
불합리한 보험상품 개발·판매」 as the cause, and flags that the 무·저해지 lapse assumption
would be dealt with separately 「금년 중」, which it was [R11] [REG-R27].

The age creep itself, evidenced within two product lines:

| Product line | Edition | 가입나이 (100세만기 forms) | Source |
|---|---|---|---|
| Carrier A, 어린이보험 1910 | 2019-10 | 0 ~ 30세 | [S1] |
| Carrier B, 다이렉트 어린이보험 (Hi2204) | 2022-04 | 0 ~ 30세 | [S7] |
| Carrier B, 어린이종합보험Q (Hi2607) | 2026-07 | 태아 ~ 15세 | [S2] |
| Carrier C, 자녀보험Plus (26.07) | 2026-07 | 태아, 0 ~ 15세 | [S4] |

The **35** figure named in [R1] is not visible in any retrieved product document; both
pre-action products stop at 30, and that two carriers went to 35 in 2023 rests on news
reports and is **[unverified]**.

### What is public, what is not, and what that forces

The data position for this product is worse than for `Cancer_KR_S` and it must be stated at
the outset, because it decides which parameters below can be sourced and which cannot.

**Public and used.** The 손해보험협회's regulated comparison board publishes, for every
non-life 어린이보험 on sale, the product name, the channel, the **보장부분 적용이율**, the
**적립부분 공시이율** and its **최저보증이율**, a specimen male and female monthly premium on
a standardised basis, the **보험가격지수**, and a link to the 상품요약서 [S11]. The
standardised basis itself is printed on the board and is the only specification of a Korean
child policy that the market itself publishes [R12]. Every 상품요약서 publishes a complete
surrender-value grid on a named specimen contract [S1] [S2] [S3] [S4].

**Not public, and the consequence.** 보험개발원 files the **참조순보험요율** with the FSC under
보험업법 제176조제4항 and there is no obligation to publish it [REG-R4]; the **산출방법서** is a
기초서류 filed with the supervisor and not disclosed [REG-R2]; the **경험생명표** is released
only as summary statistics [REG-R33] [REG-R34]. Nothing on child incidence — cancer,
cerebrovascular disease, congenital anomaly, low birth weight, NICU admission — was retrieved
from 보험개발원, 국가암정보센터 or 통계청 in this pass. **Every incidence assumption in
`Child_KR_S` is therefore a [std] construction and says so at the point of use.**

Three public anchors bound the construction and they are all this document has. The
**published premium levels** on the [R12] basis (§*Premiums*) bound the total; the
**보험가격지수** bounds the ratio of total premium to the sum of the 참조순보험료 and average
expense [S11] [REG-R22]; and exactly **one 적용위험률 is published anywhere in this file** —
일반상해 후유장해 발생률(3~100%) at the 기본계약, 5세, 상해 1급: **남자 0.0001823, 여자
0.0001163** [S1]. That single pair of numbers is the only observation of a Korean child
morbidity rate in the whole research file, and it is the calibration point for the basic
contract's decrement in `technical-notes.md`.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 어린이보험, **무배당** (*mubaedang*, non-participating), **정액** (fixed-benefit); a 상해후유장해 기본계약 with a bundled 특별약관 stack, plus a 태아 module, a 계약자 waiver module and rider blocks on the parent and the mother | [S1] [S2] [S4] [S5] [S11]; menu **[std]** (1) |
| Regulatory class | 제3보험상품 — 상해보험 and 질병보험 (보험업법 제2조제1호다목, 제4조제1항제3호), written as a **장기손해보험** to which 감독규정 제7-61조 applies the whole 제3보험 design rule | [REG-R1]; [REG-R17] |
| Written by | A **손해보험회사**; the composite adopts the **생명보험** wording of the premium waiver only | [R5]; [S10]; **[std]** (1) |
| 보장성 / 저축성 | **보장성보험** — the maturity value does not exceed premiums paid at the 기준연령 요건 (감독규정 제1-2조제3호) | [REG-R9]; [REG-R57] |
| Chassis | **비갱신형** on the core covers; **갱신형 blocks** on 가족일상생활배상책임 (3년만기) and named riders, renewing at attained age | [S2] [S3] [S12] vs [S7]; **[std]** (2) |
| Policy term (보험기간) | To the **100세 계약해당일**; no 만기환급금 on the protection part | [S1] [S2] [S3] [S5] [S6] [S11]; **[std]** (3) |
| Premium-paying period (보험료 납입기간) | **20년납** on the core covers; 전기납 on the 태아 module and on the 갱신형 blocks | [R12]; [S2] [S4]; **[std]** (4) |
| Issue age (가입나이) | **태아 ~ 보험나이 15세** | [S2] [S4] [S5] [S6]; [R1]; **[std]** (5) |
| Issue age, pre-2023 | **0 ~ 30세** on the 100세만기 forms — retained as a documented historic variant, not offered | [S1] [S7]; [R1] |
| Contractual age basis | **보험나이** (*boheom nai*, insurance age): 계약일 현재 만 나이 with a fraction under six months discarded and six months or more rounded up, incrementing at each 계약해당일. The 만 15세 nullity test uses **실제 만 나이** | [S7 제27조] [S8 제30조] [S12 제30조]; [REG-R25 제21조]; [R8] |
| Foetal age basis | **계약나이 0세** at the 계약일; the benefit-scale age runs **from the date of birth**; the 계약일 is moved back where birth falls more than six months after it | [S8 제58조·제60조·제61조] |
| Model age basis | **만나이** (age last birthday), offset from 보험나이 by up to six months | **[std]** (6) |
| Sum insured, 기본계약 | **₩100,000,000 (1억원)** of 상해후유장해, paid as 보험가입금액 × 장해지급률 | [R12]; [S11] |
| Lives basis | **Three lives.** The child is the 피보험자; the **계약자** (a parent) carries the waiver decrement; the **mother** carries the 임신·출산질환 block. All three are on one contract | [S2] [S5] [S10]; **[std]** (7) |
| 계약자 | A parent, **만 33세** at the 계약일, male | [S2]; **[std]** (7) |
| Sex of the insured | **Male at pricing on a 태아 contract**, since the sex is unknown at issue; trued up after delivery | [R3]; [S8]; **[std]** (8) |
| Underwriting | 계약 전 알릴 의무 questionnaire, no medical examination; a 태아 contract is additionally subject to a **gestational-week window** on the neonatal riders | [S5]; [REG-R25 제13조] |
| Substandard terms | 특정 신체부위·질병 보장제한부 인수특약 | [S8] |
| 배당 | None — 무배당 | [S1]–[S6] [S11]; [REG-R12] |
| Death benefit | **None below 만 15세, by statute.** On death the **계약자적립액 + 미경과보험료** is paid and the contract ends | [R7]; [REG-R50 제732조]; [REG-R17 제7-63조제1항제1호]; [REG-R25 제22조]; [REG-R19 제7-66조제5항]; **[std]** (9) |
| 암보장개시일 | **제1회 보험료를 받은 때** while the insured is 보험나이 15 미만; the 91st day counting the 계약일 as day 1 from 보험나이 15; **no waiting period at all** on a 태아가입 cover | [S3]; [S11]; [R5]; **[std]** (10) |
| 감액기간 | **None** | [S1] [S3] [S11] vs [S6]; [R2]; **[std]** (11) |
| Surrender-value form | **표준형** base, with **해약환급금 미지급형 (납입기간 중 0%, 납입 후 50%)** as the switch | [S2] [S11]; [REG-R19 제7-66조제4항]; **[std]** (12) |
| **Anchor model cell (point_id 1)** | **태아가입**; 계약나이 0 at the 계약일, priced male; **birth at policy month 5**; 보험기간 to the 100세 계약해당일 (`t = 1200`); **20년납** (`t = 240`); 월납; 표준형; 계약자 male 만 33 with the waiver module on; 기본계약 상해후유장해 ₩100,000,000; the [R12] rider set at 질병후유장해 ₩10,000,000, 암진단비(유사암 제외) ₩10,000,000, 유사암진단비 ₩2,000,000, 뇌출혈진단비 ₩10,000,000, 급성심근경색증진단비 ₩10,000,000, 암·뇌출혈·급성심근경색증 수술비 ₩5,000,000 each, 상해·질병 입원일당 ₩40,000 per day to 180 days per stay, 골절진단비 ₩400,000, 화상진단비 ₩200,000, 가족일상생활배상책임 ₩100,000,000; 태아 module on to `t = 17`; office premium **₩31,000 per month to `t = 16`, ₩28,000 from `t = 17` to `t = 239`** | **[std]** (13) |

Footnotes to the [std] rows:

1. **The menu, and the licence.** No two retrieved products carry the same rider set and none
   could be reproduced in full: [S2]'s eligibility tables run to roughly forty pages and
   [S4]'s 상품요약서 is 207 pages. What every retrieved non-life product does share is the
   **shape** — a 상해후유장해 기본계약 paying 가입금액 × 장해지급률, with everything else a
   특별약관 [S1] [S2] [S4] [S5] [S11] — and a **published standardised specification** of the
   compulsory covers exists, printed on the comparison board [R12]. The composite therefore
   takes [R12]'s specification as its rider set rather than any one carrier's, because it is
   the only child-policy benefit menu the Korean market itself publishes and because every
   published premium in §*Premiums* is quoted on it. The contract is drafted non-life because
   the protection product is a non-life product [R5] and because the liability rider requires
   a non-life licence; 감독규정 제7-61조 makes the design rules identical either way
   [REG-R17], so nothing in the model turns on the licence except the waiver wording of
   footnote (14).
2. **비갱신형 with 갱신형 blocks inside it, which is what the market actually sells.** The two
   pure forms both exist: one direct product is built end to end of 20년만기 / 30년만기
   renewable blocks with renewal ceilings written as `(100−보험기간)세` [S7], and one product
   is sold as a **비갱신 무해지** contract in its pure form [S12]. Between them sits the
   dominant design — a 비갱신 core with a small number of 갱신형 riders, of which
   가족일상생활배상책임 is universally one, at a **3년만기** renewal at one carrier [S2] and a
   갱신형 at two more [S3] [S5]. The composite takes the mixed form because it is the majority
   and because it is the only one on which the two things this product is for — a level
   premium over a hundred-year term, and a waiver that fires once and stays fired — coexist
   with a renewal mechanic the model must nevertheless carry. What the 갱신형 flag does is
   specified at *Contractual mechanics*.
3. **100세 만기.** Observed maxima: 100세 at four carriers [S1] [S2] [S5] [S6] and **110세** at
   one [S4], which is the longest term found anywhere in this research. The full 만기 ladder
   at the archetypal product is 10세 / 20세 / 30세 / 80세 / 90세 / 100세만기 [S2]. 100세 is
   taken because it is the modal maximum, because it is the term on which every published
   premium and every published cash-value grid in this file is quoted [S11] [S2] [S1], and
   because the 2011 move to it is the datable event that made the product what it is [R5].
   110세 is a documented variant and not the base: a further ten years of a decrement that is
   [std] in any case adds no mechanic. There is **no 만기환급금** on the protection part —
   the published grids show the 표준형's value at 95 years down to ₩1,928,830 (16.0% of
   premiums paid) and the 미지급형's at nil [S2] — and the residual at maturity is the
   적립부분, not a guaranteed benefit.
4. **20년납.** Observed on the 100세만기 forms: 10 / 15 / 20 / 25 / 30년납 at both current
   carriers [S2] [S4] and 10 / 20 / 25 / 30년납 in the pre-2023 generation [S1]. 20 years is
   the payment term on which the comparison board quotes every premium — 「100세만기 / 20년납
   for 세만기 covers」 [R12] — and it is the **해약공제계수 cap** for a 보장성보험 in 감독규정
   [별표 14], 「보험기간(최대 20년)」, and the basis on which the same schedule's note 3 forces
   the 연납순보험료 to be recomputed where the term is 20 years or more [REG-R20]. It puts
   납입완료 at a known date, which is what makes the 무해지 step-up a cliff [S2]. And it leaves
   **eighty years of paid-up cover** on the anchor cell — four times the payment period, and
   the reason a child policy's IFRS 17 measurement is dominated by what happens long after the
   premium stops.
5. **가입나이 태아 ~ 15세.** The current envelope, from two 2026 상품요약서 [S2] [S4] and
   confirmed at two more [S5] [S6]. The full grid narrows the upper bound as the payment term
   lengthens — 30세만기 20년납 accepts to 9세 and 25년납 to 4세, because the payment period may
   not outrun the term [S2] — and the composite carries the 100세만기 row, at which every
   payment term accepts to 15. **The bound is a supervisory artefact and is datable**: the
   pre-action generation of the same two lines accepted to 30 [S1] [S7], and the 2023
   감독행정 restricted the product name above 15 rather than the age itself [R1]. 15 is also
   the age at which two other rules in this document change sign — the 면책기간 switches on
   (footnote 10) and 상법 제732조 stops voiding a death benefit (footnote 9) — so it is the
   single most load-bearing age in the product.
6. **The two age bases, and the third one a foetal contract adds.** The contract ages on
   **보험나이**: 「계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고
   6개월 이상의 끝수는 1년으로 하여 계산하며, 이후 매년 계약해당일에 나이가 증가」, identical
   in the 생명보험 and 질병·상해보험 표준약관 and reproduced verbatim by every carrier [R8]
   [S7 제27조] [S8 제30조] [S12 제30조] [REG-R25 제21조], with the 표준약관's worked example
   생년월일 1988-10-02, 계약일 2014-04-13 ⇒ 25년 6월 11일 ⇒ **26세**. Because of the six-month
   rule 보험나이 differs from 만나이 for **roughly half of all issue dates**. `Child_KR_S`
   projects on **만나이**, because every decrement it could use — the 국가데이터처 생명표
   [REG-R38] [REG-R39], the 국가암등록통계 age bands [REG-R40] and the NHIS statistics
   [REG-R41] — is published on 만나이, and no source supplies the distribution of issue dates
   within a policy year that a conversion would need. On a **태아** contract the offset is not
   an average but a **stated quantity**: the 계약나이 is 0 at the 계약일 [S8 제60조] and the
   child's 만나이 is 0 at birth, so 보험나이 runs ahead of 만나이 by exactly the pre-birth
   period, which [S8 제61조] caps at six months. On the anchor cell that offset is **five
   months for the life of the contract** (footnote 13).
7. **Three lives on one contract, and why the 계약자's age is 33.** The child is the 피보험자.
   The 부양자 block is written on the parent, at issue ages 만15세 ~ (77−보험기간)세 [S2]. The
   임신·출산질환 block is written on the mother, at issue ages **20세 ~ 47세** for most riders,
   20~39세 for 출산전특정태아이상진단 and 20~40세 for the 융모막·양수검사 rider [S2]. The
   composite sets the 계약자 at 만 33 because it is the **mid-point of the 20~47 band the
   mother-side riders themselves state** [S2], which is the only sourced anchor for a parental
   age anywhere in this file. Korean population statistics on mean age at first birth were not
   retrieved and are not relied on. The 계약자 is taken as male so that the waiver decrement
   runs on the male table, which is the conservative direction; a female 계약자 is a model-point
   variant.
8. **The male-rate convention on a 태아 contract.** 「보험료는 일반적으로 피보험자의 성별에
   따라 다르지만, 태아보험 가입시 태아의 성별을 구별하기가 어려운 점 때문에, 일단 남자 아이를
   기준으로 납입보험료가 산정되고 출산 후 성별대로 정산하는 구조」 [R3], and a carrier's own
   published 민원 case says the same [S8]. The composite adopts it and **does not model the
   true-up**, because the direction is no longer reliable: the current published premium tables
   show the female rate above the male at four carriers and below it at seven [S11], so a
   refund on the birth of a girl is a product-specific fact rather than a market rule
   (footnote 16).
9. **No death benefit, and what is paid instead.** 상법 제732조: 「15세미만자, 심신상실자 또는
   심신박약자의 사망을 보험사고로 한 보험계약은 무효로 한다」 [R7] [REG-R50], restated by the
   표준약관 at 제19조제2호 with 제19조제3호 refusing to extend the age-correction saving to it
   [R8] [REG-R25]. The product-design consequences are visible everywhere: 일반상해사망 is
   fixed only 「기본계약 최초가입시 피보험자의 나이가 15세 이상인 경우」 [S1], one carrier
   writes it only at 만 15세 [S4], the board note reads 「15세이상 가입시 일반상해사망 특약
   고정부가」 [S11], the 생명보험 wording pays a 사망보험금 only 「만 15세 계약해당일 이후」
   [S10 제21조], and the 1997 product returned premiums on death before 15 [R5]. The
   supervisor states the general rule: 「15세 미만의 미성년자를 피보험자로 하는 보험상품에서도
   피보험자의 사망시 사망보험금이 아니라 **기납입보험료**가 지급됨」 [R3]. The composite pays
   the **계약자적립액 plus the 미경과보험료** instead of returning premiums, because that is
   what 감독규정 제7-63조제1항제1호 requires of a 제3보험 contract on a death it does not cover
   [REG-R17], what the 표준약관 제22조 implements [REG-R25], and what 상법 제736조 puts a
   statutory floor beneath [REG-R50]. On a 무해지 contract inside the payment period that sum
   is close to nil, which is a real and uncomfortable feature of the form and is stated rather
   than smoothed. **상법 제739조 disapplies 제732조 to 상해보험**, so accidental-death cover on
   a child under 15 is lawful [R7]; the market's uniform refusal to write it is therefore more
   conservative than the statute requires, and the reading is [unverified] as a matter of
   Korean law since no judgment or commentary on the point was retrieved.
10. **The waiting period, disapplied.** Two independent primary statements, from two carriers
    and two document types. A 상품요약서 footnote to the 면책기간 matrix: 「주1) 최초계약과
    부활계약의 면책기간은 **보험나이 15세 이상인 경우에만 적용**」 [S3]. A benefit definition on
    the comparison board: 「피보험자가 보장개시일(계약일로부터 90일이 지난날의 다음날, **계약일
    현재 보험나이 15세 미만 피보험자의 경우 1회 보험료를 받은 때**) 이후에 암(유사암제외)으로
    진단확정시」 [S11]. The origin is 2006 and the reasoning is recorded: 「암에 대한 위험률이
    낮아 역선택 우려가 있다거나 이로 인한 위험률차손이 크다는 근거가 없기 때문에 암 보장에
    대한 90일 부담보 기간이 삭제되었다」 [R5]. A 태아가입용 cover goes further and has 「면책기간
    없음」 at all, including on the 10-day waits that some infection and influenza riders carry
    [S3]. The composite implements all three limbs. **Waiting periods that do survive** are
    named at *Contractual mechanics*: the 90-day 보장개시일 on 누수사고 under the liability rider
    [S5] [S3], the 90-day 책임개시일 on cancer-treatment hospital-cash and outpatient riders
    [S5], and the re-run of every waiting period from a 부활일 [S3].
11. **No 감액기간.** The market has moved to 감액없음 and puts the word in the benefit names —
    암진단비(유사암제외)**(감액없음)**, 뇌혈관질환진단비**(감액없음)** — at five carriers
    [S1] [S3] [S11]. Where a 감액 survives it is a first-year 50%: one carrier publishes its
    암진단비 as 「1천만원(1년이내 50%지급)」 and its 항암방사선·약물치료비 as 「100만원(1년미만
    50%지급)」 [S6] [S11]. One carrier applies 감액 only to dental benefits, at 25% or 50%
    「최초계약일부터 2년 경과시점 전일 이전」, with cancer at 「-」 throughout [S3]. The
    composite takes 감액없음 as the base and carries `reduction_months` as a parameter with
    observed values 0 and 12, so the 감액 machinery specified by `Cancer_KR_S` remains
    reachable. **A foetal contract may not be subject to 감액 at all**: the 2015 변경권고
    inserted 「단, 피보험자가 보험가입 당시 태아(胎兒)인 경우에는 보험금의 100%를 지급합니다」
    across 17 carriers and 56 products, on the reasoning that 「태아는 보험가입시 역선택
    가능성이 거의 없는데도 성인과 동일한 기준을 적용하여」, and the trigger case was a newborn
    with a cerebral haemorrhage paid at 50% [R2]. A current carrier confirms it still holds
    [S8].
12. **표준형 as the base, 무해지 as the switch — the opposite of `Cancer_KR_S`.** Every carrier
    on the board offers a 해약환급금 미지급형 beside the 표준형 [S11], and the 무·저해지 share
    of 보장성 초회보험료 ran 11.4% (2018) → 30.4% (2021) → 47.0% (2023) → **63.8%** (2024 H1)
    [R11] [REG-R27], so the suppressed form is where the market is. `Cancer_KR_S` accordingly
    ships the 미지급형 as its base. `Child_KR_S` deliberately ships the **표준형**, for three
    reasons. The 적립부분 credited at the **공시이율** — with its own 최저보증이율 and its own
    reset machinery — exists only on the 표준형; the suppressed forms are 순수보장성 and show
    「-」 for the 적립부분 on the board [S11] [S2]. The 표준형's surrender value **exceeds
    premiums paid from about year 30** on the published grid [S2], which is a shape no other
    protection product in `krlib` produces and which only a hundred-year term can. And shipping
    the two forms on two products lets a reader compare them inside one library without either
    model having to carry both as its base. The 무해지 switch is fully specified at
    *Termination and values* and its premium ratio at footnote (17).
13. **The anchor cell, and why it is the foetal one.** `Cancer_KR_S` anchors on the 기준연령
    요건 of 감독규정 제1-2조제2호 — 남자 만 40세, 전기납, 월납 [REG-R9] — because that is the
    cell at which the 표준해약공제액 and the 보험가입금액 computations are performed. **No child
    policy can be written at that cell**, so 제1-2조제2호's own fallback applies: where a
    40-year-old male cannot buy the product, the 기준연령 요건 is taken at the mid-point issue
    age and the longest available payment term [REG-R9]. That fallback is what this document
    uses for the regulatory computations, and it is not the same as the modelling anchor. The
    modelling anchor is the **태아 contract at 계약나이 0**, because 태아가입 and the 계약자
    waiver are the two mechanics this product exists to demonstrate and a worked example that
    exercises neither would be a worked example of `Cancer_KR_S`. **Birth at policy month 5**
    is [std]: the neonatal riders close at 임신 22주 [S5], which leaves at most 18 weeks — 4.1
    months — of gestation at issue, and [S8 제61조] caps the pre-birth period at six months by
    resetting the 계약일; five months is between them and is a whole number of monthly grid
    steps. The **premium is a model-point input, not a computed or a quoted rate** — see
    footnote (16) for what the two figures are anchored on. A second, calibration cell is
    shipped alongside it: **male, 보험나이 5, 표준형, no 태아 module, no 계약자 waiver**, at
    ₩27,000 a month, which is the cell every published premium in this file is quoted on [R12]
    [S11].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | **Level** for the whole 납입기간 on the 비갱신 core; 무배당, so no dividend and no premium review. The 갱신형 blocks are recomputed at each renewal on the attained age and the rate basis then in force | [S1] [S2] [S11]; [S7 제29조]; [REG-R12] |
| Frequency (납입주기) | **월납**; 연납 offered; one product on the board is 일시납 | [S1] [S2] [S7] [S11]; **[std]** (15) |
| Anchor premium | **₩31,000 per month to `t = 16`; ₩28,000 from `t = 17` to `t = 239`** — being ₩27,000 of core 보장보험료, ₩1,000 for the 계약자 waiver module and ₩3,000 for the 태아 module over `t = 0..16` | **[std]** (16) |
| Calibration-cell premium | **₩27,000 per month**, male, 보험나이 5, 상해 1급, 100세만기 20년납, on the [R12] specification | published cluster [S11]; **[std]** (16) |
| Rating factors | 보험나이, sex, 보험가입금액 per cover, riders elected, 형 (표준형 / 미지급형), 납입기간, **상해급수** (the comparison basis is 상해 1급), 계약 전 알릴 의무 outcome | [R12]; [S1] [S2] [S11] |
| Rate structure | **Not published by any carrier.** The 참조순보험요율 is filed with the FSC and never disclosed; the 산출방법서 is a 기초서류 | [REG-R4]; [REG-R2]; [REG-R34] |
| The one published rate | 일반상해 후유장해 발생률(3~100%), 기본계약, **5세, 상해 1급: 남 0.0001823, 여 0.0001163** | [S1] |
| 보험가격지수 | Published per product, sex and 형; observed **79.6–116.0** (male) and **72.4–123.3** (female). The **미지급형's index is 3–16 points above the 표준형's at every carrier** | [S11]; [REG-R22 제7-45조제7항] |
| Pricing method | **현금흐름방식** — mandatory for a contract longer than three years, with an adequacy analysis on 최적기초율 and projected cash flows | [REG-R18 제7-64조제1호] |
| 보장부분 적용이율 (예정이율) | **2.75% p.a.** | observed 2.50–3.00 [S11]; **[std]** (18) |
| 적립부분 공시이율 | **1.70% p.a.**, reset off a published 공시기준이율 | observed 1.60–2.20 [S11] [S2]; **[std]** (18) |
| 최저보증이율 | **0.30% p.a.** | observed 0.20–0.50 [S11]; **[std]** (18) |
| 평균공시이율 | **2.50%**, itself capped at the 공시이율 in force on the selling date | [S2]; [REG-R9 제1-2조제13호]; [REG-R48] |
| Pricing lapse rate (적용해지율) | Disclosed on the suppressed forms at one carrier: **5.0% / 3.0% / 1.0% p.a.** during the payment period by duration band (≤10년 / 10–15년 / >15년), **0.5%** afterwards on the 미지급형Ⅱ and **0.65%** on the 미지급형Ⅲ; 「1형(표준형) 및 2형(계약전환형)에는 적용해지율이 적용되지 않습니다」 | [S1]; **[std]** (19) |
| Lapse basis adopted | The **2024 계리가정 guideline** — log-linear decay to **0.1%** at 납입완료 and **0.8%** thereafter — not the 2019 disclosure | [R11]; [REG-R27]; **[std]** (19) |
| Minimum premium | **₩20,000 a month** modal; observed ₩0–₩25,000 | [S11]; **[std]** (15) |
| Published discounts | 다자녀 1%–3% (2 or 3+ siblings); 출산할인 2% on a **sibling's** policy; 국가유공자 3%; existing-policyholder 1% | [S11] |
| Statutory discount, 2026 | **1%–5% for one year** on a 보장성 어린이보험 where the policyholder or spouse is within a year of a birth, on 육아휴직 or on 육아기 근로시간 단축; industry-wide from **2026-04-01**. 어린이보험 is **expressly excluded** from the companion premium-deferral scheme | [R6]; **[std]** (20) |
| Premium waiver — the child | 50% 이상 후유장해 (상해 or 질병), **or** diagnosis of one of the **7대질병**, **or** a 중대한특정상해수술; with a **P코드 carve-out** | [S2]; **[std]** (14) |
| Premium waiver — the 계약자 | The **계약자's death**, or a cumulative 장해지급률 of **50% 이상** from one cause | [S10 제22조]; **[std]** (14) |
| Effect of either waiver | 차회 이후의 보장보험료 waived for the remainder of the 납입기간; payment of the **적립보험료 stops as well**; cover continues in full | [S2]; **[std]** (14) |
| Waiver and renewal | A waiver granted in one renewal cycle **does not carry into the renewed contract** on the 표준형 | [S2] |
| Commission | First-year remuneration may not exceed the first year's expected premium; instalment structures pay no more than **60% of the 표준해약공제액** a year | [REG-R22 제4-32조제5항·제8항]; [REG-R29] |
| Acquisition and maintenance cost | Named in the 약관, **never quantified** in any retrieved document; the composite sets 계약체결비용 at or below the **표준해약공제액** of 감독규정 [별표 14] | [REG-R20]; [REG-R29]; **[std]** (21) |

15. **월납, and why the model runs on a monthly grid.** Every retrieved product quotes 월납
    [S1] [S2] [S11] and one adds 연납 [S7]; a single 3년만기 product on the board is 일시납
    [S11]. Monthly is also what the arithmetic wants: the 90-day waiting period that applies
    from 보험나이 15 lands on a grid boundary at 180 months from a 계약나이-0 issue, the
    태아보장기간 and the 1년만기 neonatal block are whole numbers of months, and the premium
    stream and the 계약자적립액 recursion share one step. 감독규정 제7-65조제2항 permits the
    계약자적립액 to be computed 「연납보험료를 기준으로 하여 산출할 수 있다」, which is the
    provision that lets a monthly-premium Korean product carry an annual account recursion, and
    it is the reconciliation `Child_KR_S` shares with `Cancer_KR_S`, `Medical_KR_S` and
    `LTC_KR_S` [REG-R18]. The **최저가입 보험료** is a real product parameter and is published:
    ₩20,000 at five carriers, ₩25,000 at one, ₩15,000 and ₩10,000 on two channels of another,
    보장보험료 ₩5,000 at one, and 「없음」 on two direct forms [S11].
16. **The two premium figures, and what they are anchored on.** No carrier publishes a rate
    table by age and duration for this product, so the office premium is a **model-point
    input**. What is published is a specimen premium per product on a standardised basis: 보험나이
    5세, 상해 1급, 100세만기 20년납, 월납, being the **보장보험료 of the compulsory covers only**
    [R12] [S11]. The observed levels vary by a factor of seven — ₩21,502 to ₩148,250 for a male
    5-year-old — because carriers include different compulsory sets in the quoted figure, so
    the level is not comparable across the board and the 보험가격지수 is the normalising
    statistic rather than the premium. The composite takes **₩27,000** for the calibration
    cell, which is the tight cluster of the three mid-market carriers whose compulsory sets are
    closest to [R12]'s (₩26,841, ₩26,999 and ₩27,480) [S11]. The anchor cell adds ₩1,000 for
    the 계약자 waiver module and ₩3,000 for the 태아 module over its own 17-month term. On the
    entry age, [R5] publishes a premium-by-issue-age index on a simulation of 암진단 ₩40,000,000
    (4천만원), 20년 납입, 100세 만기 — total premium at 0세 100%, 20세 189%, 30세 264%, 60세
    625%, with the residual term at 100 / 80 / 70 / 40 years — from which a 계약나이-0 rate sits
    slightly **below** a 5세 rate on the same specification. The composite does not attempt that
    refinement and holds ₩27,000 at both, which is a **[std] simplification** stated here so a
    later pass can remove it. **`technical-notes.md` performs the equivalence calculation on the
    shipped basis and its figure governs where the two differ**; nothing in this library depends
    on ₩27,000 or ₩31,000 being a market rate.
17. **The 무해지 discount, measured.** Taking every carrier on the board that publishes both a
    표준형 and a suppressed form on the same specification, the suppressed premium as a
    percentage of the 표준형's is 70.4 / 71.2 (M/F), 72.6 / 74.0, 79.7 / 81.9, 72.6 / 71.6,
    78.0 / 79.4, 78.9 / 79.9, 76.5 / 77.9, 76.4 / 76.9 and 67.4 / 68.2 [S11]. The observed range
    is **67%–82% of the 표준형 premium**, i.e. an 18%–33% discount, and the composite takes
    **78%** — the modal cluster and, at the anchor cell, ₩21,840 against ₩28,000.
18. **Interest.** A full-text search of the 감독규정 returns **zero** occurrences of 예정이율:
    the regulation speaks only of the **계약자적립액 적용이율** and of the 금리확정형 /
    금리연동형 distinction [REG-R9] [REG-R48]. What the comparison board publishes instead, per
    product, is the **보장부분 적용이율** — which is the pricing rate under another name — and
    the **적립부분 적용이율** with its 최저보증이율 [S11]:

    | 보장부분 적용이율 | 적립부분 공시이율 (최저보증) |
    |---|---|
    | 2.65% | 2.20% (0.3%) |
    | 2.75% | 1.60% (0.3%) |
    | 3.00% | 1.60% (0.3%) |
    | 3.00% | 1.60% (0.3%) |
    | 2.75% | 1.90% (0.25%) |
    | 2.70% | 1.70% (0.3%) |
    | 2.75% / 2.50% | 1.65% (0.2%) |
    | 2.75% / 2.50% | 1.75% (0.2%) |
    | 3.00% | 1.75% (0.5%) |

    Observed: **보장부분 2.50%–3.00%, 공시이율 1.60%–2.20%, 최저보증이율 0.20%–0.50%** [S11].
    The composite takes **2.75% / 1.70% / 0.30%**, the modal value of each column. The 공시이율
    is a **금리연동형** quantity reset off a published 공시기준이율 under 감독규정 제7-65조제3항
    and 시행세칙 [별표 27] [REG-R18] [REG-R24]; one carrier prints the formula in full,
    「공시기준이율(%) = 외부지표금리수익률 × α + 운용자산이익률 × (1−α)」 with α a function of the
    prior-year opening 보험료적립금, the asset duration and the prior-year premium income, but
    the extracted bracketing of α is uncertain and is [unverified] [S1]. `Child_KR_S`
    **does not implement the reset**; it credits the fixed 1.70% with a 0.30% floor and carries
    the machinery by reference to `WholeLife_KR_A`. The 평균공시이율 of 2.50% enters only
    through the surrender-charge and disclosure computations [S2] [REG-R9] [REG-R48].
19. **The lapse basis, and the one carrier that published its own.** [S1] discloses the
    **적용해지율** actually used to price each suppressed form — a step function at 5.0% / 3.0%
    / 1.0% a year during the payment period by duration band, and 0.5% or 0.65% after
    납입완료 — and states that the 표준형 carries none [S1]. That is a published, product-specific
    decrement basis and it is directly usable, but it is **of exactly the shape the supervisor
    moved against**: the 2024-11-07 계리가정 guideline names the log-linear model converging to
    **0.1%** at 납입완료 as the 원칙모형, sets the post-completion ultimate at **0.8%** (or a 20%
    relativity to the 표준형 rate), and requires an insurer departing from it to disclose the
    CSM, BEL, K-ICS and net-income differences quarterly [R11] [REG-R27]. 어린이보험 is not named
    in the release, but every 무해지 어린이보험 form on the board is inside its scope [S11].
    `Child_KR_S` uses the **guideline basis** and ships [S1]'s 2019 vector as a comparison
    switch, which is exactly the comparison the guideline requires an insurer to disclose.
20. **The 2026 discount is a real cash-flow item and is carried as a parameter.** From
    2026-04-01 every Korean insurer operates a **1%–5% premium discount for one year** on a
    보장성 어린이보험, the rate and period set by each insurer, where the policyholder or spouse
    is within a year of a birth, on 육아휴직, or on 육아기 근로시간 단축 for a child of 12 or
    under [R6]. On the birth limb the discount applies to a **sibling's** policy and not the
    newborn's own — 「(출산) 형제, 자매 출산 시 보험료 할인 가능(피보험자 출산사유 할인은
    제외)」 [R6]. It is limited to one use per contract, pre-existing contracts qualify, and the
    expected industry cost is about **₩1,200억원 a year** [R6]. Two things follow. It is a
    premium haircut with a one-year duration on an identifiable subset of the in-force book, so
    it is a `premium_discount_rate` and a `premium_discount_months` parameter, **off in the base
    run**. And 어린이보험 is **expressly excluded** from the companion 6- or 12-month
    interest-free premium-deferral limb of the same scheme [R6], so no deferral state is needed.
    Whether the discount applies to the 영업보험료 or the 보장보험료 is not stated in the release
    and is [unverified].
21. **Expenses.** No retrieved document quantifies any expense item for this product. What is
    available is a statutory ceiling: 감독규정 [별표 14] caps the deductible acquisition cost at
    the **표준해약공제액** [REG-R20], and the FSC's 2019 expense reform states the same cap as
    thirteen months' premium for a 보장성보험 [REG-R29]. The composite sets 계약체결비용 at or
    below the 표준해약공제액 and computes the schedule at *Contractual mechanics*. The
    보험가격지수 gives an independent bound the other way: it is the ratio of total premium to
    the sum of the 참조순보험료 total and the average expense total [S11], so an index of 98
    means the product's premium is 2% below the reference net-plus-average-expense premium, and
    the observed 79.6–116.0 band brackets how far a real product sits from that reference.
