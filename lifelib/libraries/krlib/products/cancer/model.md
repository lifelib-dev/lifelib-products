# Model implementation notes — `Cancer_KR_S`

**Status:** Draft, 2026-09-03. Companion to `product-spec.md`, `technical-notes.md` and
`sources.md` in this directory. This file records *how the model is built*: the file
layout, the state structure, the processing order, the identities the `check_*` cells
assert, and every standardization made in translating the specification into formulas.

---

## 1. Layout

```
products/cancer/
    Cancer_KR_S/
        __init__.py              model docstring, _name, _spaces
        _system.json             {"modelx_version": [0, 32, 0], "serializer_version": 8}
        Data/__init__.py         readers and *_file References
        Projection/__init__.py   the projection, parameterized by point_id
    model_point_table.csv        10 model points, point 1 the anchor
    mort_table.csv               [std] Makeham, sex x age 15-100
    incidence_table.csv          [R5] [REG-R61] 암 발생률 ex C44/C73, sex x age
    tier_share_table.csv         [std] tier decomposition, sex x age 20/40/60/80
    tier_table.csv               benefit ladder and each tier's 면책기간
    survival_table.csv           [std] post-diagnosis excess hazard, sex x tier x year
    care_table.csv               [std] care intensity per diagnosed life, by select year
    lapse_table.csv              [std] [REG-R27] three-segment 최적해지율
    run.py                       ASCII-only runner
```

Inputs are **external CSVs in the model folder's parent** — the `annuallife/TradLife_A`
layout, not `basiclife/BasicTerm_S`'s embedded IOSpec — so the model folder holds nothing
but formulas. The readers live in the unparameterized `Data` Space, so each file is read
**once per model** rather than once per model point. `Data.input_dir()` resolves to
`_model.path.parent` at run time.

Every CSV but `model_point_table.csv` carries a `provenance` column and every cell in it
begins with a citation tag.

## 2. States

Three in-force states, not two, and the reason is the premium waiver:

| Cells | Meaning | Pays premium | Can lapse | Excess hazard |
|---|---|---|---|---|
| `pols_healthy(t)` | never invasively diagnosed | yes | yes | none |
| `pols_minor(t)` | 특정소액암 only | **yes** | yes | 특정소액암 basis |
| `pols_waived(t)` | 일반암 / 고액암 | no | no | general basis |

The 유사암 tier is **not** a state. It is a second benefit on its own once-only ledger
(`similar_avail`), it does not stop the premium and it carries no excess mortality.

Each diagnosed state is resolved into **six select-duration cohorts** — select years 1 to 5
and an ultimate — because relative survival is steeply select and a flat hazard fitted to
the five-year point kills long survivors, who are exactly whom the care limbs are paid for.
The cohorts are tracked exactly, as a **twelve-month delay on the entry flow**
(`waived_grad`, `minor_grad`), not as a transfer rate.

Transitions modelled: healthy to 특정소액암, healthy to 일반암, and **특정소액암 to
일반암**. Not modelled, each understating: a 일반암 life's later 특정소액암, and a 고액암
after a plain 일반암.

## 3. Processing order within month `t`

1. Premium and maintenance expense at the **start** of the month, on `pols_payer(t)` and
   `pols_if(t)` respectively.
2. Diagnoses: `diag_gen_h`, `diag_minor` out of `pols_healthy`; `diag_gen_m` out of
   `pols_minor`; `diag_high` as a subset of the general flow; `diag_similar` on the whole
   in-force against the once-only ledger.
3. Diagnosis benefits, scaled by `reduction_factor(t)` and gated by `cover(t)` for the
   invasive tiers and `cover_similar(t)` for 유사암.
4. Care benefits on the six duration cohorts of both diagnosed states.
5. Decrements at the **end** of the month, in the order **transition, then mortality, then
   lapse**, each state on its own basis. A life diagnosed in month `t` takes its new
   state's mortality for the rest of that month.
6. The 계약자적립액 recursion: `av_pp(t+1) = max(0, (av_pp(t) + prem_alloc_pp(t) −
   risk_prem_pp(t)) (1 + i)^(1/12))`. `claims(t, "DEATH")` releases `av_pp(t)` and
   `claims(t, "LAPSE")` releases `cv_pp(t)`.
7. At `t = proj_len()` the contract expires: `pols_maturity` takes the whole remaining
   exposure, every cash flow is zero and `claims(t, "MATURITY")` is zero, because nothing
   is paid at the 100세 계약해당일.

## 4. The identity each check asserts

| Check | Identity |
|---|---|
| `check_pols_roll_fwd` | `pols_if(t) − pols_if(t+1) = deaths + lapses + maturities` |
| `check_cancer_roll_fwd` | `pols_cancer(t+1) = sum over cohorts of exposure x survival`; the graduation terms telescope out |
| `check_canc_dur_ledger` | both states' cohort 1 rebuilt independently from the entry history |
| `check_similar_ledger` | `similar_avail(t) + similar_used(t) = 1`, `similar_used` read off the claim line |
| `check_treat_ledger` | the 최초 1회한 treatment benefit's cumulative per-life payment probability never passes 1 |
| `check_tier_shares` | 일반암 + 특정소액암 = the base rate; 고액암 is a subset of 일반암; 유사암 is non-negative |
| `check_waiting_period` | no invasive benefit and no invasive transition before the 암보장개시일 |
| `check_cv_floor` | `0 <= cv_pp <= cv_std_pp`, and `cv_pp = 0` for the whole 납입기간 on the 미지급형 form |
| `check_net_cf` | `result_cf()`'s own columns rebuild `net_cf(t)` |
| `check_hosp_cap` | no cohort's mean stay passes the 180-day per-stay cap |

`check_net_cf` is the identity `model.md` is required to state in one line: **premiums less
every `claims_*` column, less `expenses`, less `claim_expenses`, less `commissions`, equals
`net_cf`** — with no bare `claims` subtotal published beside its own parts.

## 5. Standardizations made in the model, beyond those in the specification

1. **만나이 rather than 보험나이.** Every decrement is published on 만나이; the half-year
   average offset is accepted and is worth about 3.5% of the rate at ages 60-70.
2. **Log-linear interpolation** of the incidence grid between its published ten-year ages,
   and **linear** interpolation of the tier shares between their four anchors.
3. **Age-graded tier shares** rather than the all-ages crude shares the registry publishes,
   because the tiers' age mixes differ violently. The grading itself is `[std]`.
4. **One aggregate 유사암 ledger** rather than five member ledgers. The contracts pay each
   of the five members once, so this understates the tier.
5. **No care benefits on the 유사암 tier.** Real contracts pay the inpatient and treatment
   limbs at 20-25% on 유사암; this understates.
6. **The 감액기간 applies to the diagnosis tiers only.** The clock runs to the 수술일 for a
   surgery or treatment benefit and to the 진단확정일 for a diagnosis benefit; the model
   uses the diagnosis clock throughout.
7. **A mid-cohort treatment availability** rather than an exact per-elapsed-month ledger,
   and a **zero ultimate first-treatment hazard**, which is what makes the once-only bound
   hold at any horizon.
8. **Lapse is absorbing**: 부활 is not modelled. Conservative, because a reinstated Korean
   cancer policy re-runs the 90 days from the 부활일.
9. **The 계약자적립액 is a retrospective recursion floored at zero.** On the anchor cell,
   whose premium is the specification's stated 45,000 won rather than the shipped basis's
   own equivalence level, the account is exhausted at about 만나이 78 and the death payment
   falls to nil thereafter. Every other model point carries its own equivalence premium.
10. **The 표준해약공제액's 보험가입금액 input** is a `[std]` 60% of the headline sum insured,
    standing in for the 별표 15 제9호 risk-premium ratio, and the whole is capped at 13
    months' premium — which binds, giving 585,000 won at the anchor cell.
11. **No 재진단암, no 요양병원 rider, no 암 사망 rider, no 다빈치로봇 limb, no 비흡연체
    differential.** Each is specified in `product-spec.md` and each is switched off because
    its rate cannot be sourced.
