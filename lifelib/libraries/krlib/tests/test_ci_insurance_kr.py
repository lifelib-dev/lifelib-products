"""Golden and structural tests for CI_KR_A.

The golden values are the worked example in
products/ci_insurance/technical-notes.md ("Worked example"), which projects the anchor
cell 남자 / 보험나이 40 / 보험가입금액 KRW 100,000,000 (1억원) / 종신 with CI cover to the
100세 계약해당일 / 20년납 / 80% 선지급형 / 저해지환급형 k = 0.50, at an annual premium of
KRW 3,680,880 — twelve times the KRW 306,740 monthly figure one carrier publishes for
exactly that cell.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal,
in-force in the cash flow table to the six decimals it prints, the decrement basis to the
eight or ten decimals of its own columns, and the hand traces' counts to the sixteen the
traces carry.

**What this module is about is the acceleration.**  The chassis this product sits on —
the 종신보험 whole life model — supplies the 계약자적립액, the 해약환급금 net of a
해약공제액 capped by the 표준해약공제액, the 저해지환급형 suppression and its step at
납입완료, the 보험계약대출 and the 납입면제.  None of that is retested here.  What is new
is that **one decrement produces two payments at two dates on one sum assured**: the
선지급 of 80% of the 기본보험금 at the CI date, and a residual death benefit of the
complement whenever death follows, floored at 105% of an account that keeps growing.  So
the projection runs two cohorts, the post-CI one indexed by the year it accelerated in,
and almost every test below is a statement about that structure.

Every product fact the notes list under "Known modeling pitfalls" earns its own test,
named after the pitfall, because each of them is a way an implementation can look right
and be wrong:

* the acceleration is a **transition**, not an exit, so the roll-forward has four terms;
* the residual floor is **two-sided**, and its two limbs bind at opposite ends;
* the nominal is read off the entry anniversary and the floor off the current one;
* collapsing the post-CI cohorts loses the first-year 감액 one — invisible on a male
  cell at 0.15% of year-one claims and 17.86% on the female twin;
* the premium annuity must carry the CI decrement, worth 4.8% of the annuity;
* the post-CI cohort never pays a premium;
* the suppression has **two** exits and one of them is random;
* the step at 납입완료 is exactly 1 / k on one anniversary, not the adjacent-year ratio;
* the step is not a surrender-charge effect — the charge is gone thirteen years earlier;
* the 표준해약공제액 is computed on the pre-acceleration sum assured;
* CI before death before lapse, an ordering worth a factor of seven at attained 60;
* the two payments are one policy year apart, never simultaneous;
* the CI decrement stops at n_CI and nothing else does — three end dates, one horizon;
* ``ci_rate`` is a first-event rate and not a sum of marginal incidences;
* there is no survival period, the Korean supervisor having refused one;
* ``pols_if`` is the total in force, both states, and it weights maintenance expense;
* the claim expense is charged on three kinds of event, not one;
* every loan-netted payment is floored at zero and the 선지급 is not netted at all; and
* the two decrement tables are this product's, not the chassis's.

The nine ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared; that they are *true* on
every shipped model point is asserted once, in ``test_model_conventions_kr.py``, whose
sweep discovers them generically.  The optional modules are asserted in **both** positions
of their switch, and the [std] scalar assumptions the notes state are read off the model,
so that a silent change to an assumption fails a test rather than moving a result.
"""
import io
import re
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

MODEL_DIR = LIB / MODELS["CI_KR_A"][0]
CSV_DIR = MODEL_DIR.parent

WON = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-7       # pols_if in the cash flow table, displayed to 6 d.p.
TRACE = 5e-16        # the hand traces' counts, displayed to 16 d.p.
RATE = 5e-11         # ci_rate and lapse_rate, displayed to 10 d.p.
MORT = 5e-9          # mort_rate and mort_rate_ci, displayed to 8 d.p.
CAUSE = 5e-10        # the per-cause incidence grid, displayed to 9 d.p.
SPLIT = 5e-11        # the decrement split, displayed to 10 d.p.


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


def flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    These docstrings are hard-wrapped prose.  Searching the raw text for a sentence
    fragment finds it or not depending on where the wrap fell, which would make the
    assertions below test the line breaks rather than the content.
    """
    return re.sub(r"\s+", " ", doc)


# ---------------------------------------------------------------------------
# The notes' worked example, hard-coded
#
# "Derived scalars, at full precision", the anchor cell's own table.
OMEGA = 110
PROJ_LEN = 71
CI_COVER_END = 60
PREM_PERIOD = 20
SURR_CHG_YEARS = 7
DISC_FACTOR = 0.9756097560975611
A0_1 = 44892002.9507502913          # epv_ben(1)
A1_1 = 8148218.3575074952           # epv_resid(1)
ANNUITY_DUE_1 = 15.1228758581       # annuity_due(1)
P_NET = 2968483.2020010490          # prem_net_level_pp()
G_GROSS = 3680880.0000000000        # premium_pp(), sourced at 12 x KRW 306,740 [S4]
LOADING = 1.2399868045              # G / P
SC_CAP = 3944704.00                 # surr_chg_cap_pp(), the 표준해약공제액
SC_CAP_RULE_OF_THUMB = 3987620.0    # 13 x the monthly premium [REG-R29]
SC_STEP = 563529.1428571429         # SC* / 7, one year's run-off
ACCEL_RATE = 0.80
BREAST_SHARE_M = 0.005
CI_WAIT_FACTOR = 0.7534246575342466
LAPSE_ULT = 0.008

# "Two cross-checks that fell out of the model rather than being imposed", and the one
# that does not agree.  The 50% form is model point 3, which is the anchor's own cell at
# a = 0.50; the pricing quantities do not see k or the lapse basis.
A0_1_HALF = 41589404.25             # epv_ben(1) at a = 0.50
P_NET_HALF = 2750098.90             # prem_net_level_pp() at a = 0.50
FORM_RELATIVITY_MODEL = 1.0794      # P(80%) / P(50%)
FORM_RELATIVITY_PUBLISHED = 338100 / 311640     # 1.085 at 남40 / 17대 / 기본환급형 [S4]

# "The premium annuity must carry the CI decrement" — the wrong annuity and its premium.
ANNUITY_DUE_ORDINARY = 15.8467943703
P_NET_ORDINARY = 2832875.97

# "And the acceleration is expensive" — the same contract with no acceleration at all.
A0_1_NO_ACCEL = 36085073.09
P_NET_NO_ACCEL = 2386125.06
ACCELERATION_COST = 0.24406         # P / P(a = 0) - 1, the notes' 24.4%

# "The decrement basis at the anchor, t = 1 ... 25":
# t -> (attained 보험나이, ci_rate, mort_rate, mort_rate_ci, lapse_rate).
WORKED_EXAMPLE_BASIS = {
    1:  (40, 0.0025312484, 0.00068000, 0.00204000, 0.1000000000),
    2:  (41, 0.0030721810, 0.00070525, 0.00211575, 0.0784759970),
    3:  (42, 0.0033921090, 0.00073395, 0.00220185, 0.0615848211),
    4:  (43, 0.0037467810, 0.00076660, 0.00229980, 0.0483293024),
    5:  (44, 0.0041401050, 0.00080372, 0.00241116, 0.0379269019),
    6:  (45, 0.0045764400, 0.00084593, 0.00253779, 0.0297635144),
    7:  (46, 0.0050606550, 0.00089392, 0.00268176, 0.0233572147),
    8:  (47, 0.0055981780, 0.00094850, 0.00284550, 0.0183298071),
    9:  (48, 0.0061950720, 0.00101056, 0.00303168, 0.0143844989),
    10: (49, 0.0068581080, 0.00108113, 0.00324339, 0.0112883789),
    11: (50, 0.0075948480, 0.00116137, 0.00348411, 0.0088586679),
    12: (51, 0.0084137370, 0.00125261, 0.00375783, 0.0069519280),
    13: (52, 0.0093242150, 0.00135635, 0.00406905, 0.0054555948),
    14: (53, 0.0103368310, 0.00147431, 0.00442293, 0.0042813324),
    15: (54, 0.0114633740, 0.00160843, 0.00482529, 0.0033598183),
    16: (55, 0.0127170250, 0.00176092, 0.00528276, 0.0026366509),
    17: (56, 0.0141125250, 0.00193430, 0.00580290, 0.0020691381),
    18: (57, 0.0156663570, 0.00213143, 0.00639429, 0.0016237767),
    19: (58, 0.0173969630, 0.00235554, 0.00706662, 0.0012742750),
    20: (59, 0.0193249700, 0.00261034, 0.00783102, 0.0010000000),
    21: (60, 0.0214734650, 0.00290000, 0.00870000, 0.0080000000),
    22: (61, 0.0236169160, 0.00325949, 0.00977847, 0.0080000000),
    23: (62, 0.0257338530, 0.00366355, 0.01099065, 0.0080000000),
    24: (63, 0.0278056050, 0.00411769, 0.01235307, 0.0080000000),
    25: (64, 0.0298164800, 0.00462814, 0.01388442, 0.0080000000),
}

# "Per-cause incidence, male, at the ages worth printing":
# attained age -> (cancer, ami, stroke, other, ltc).
WORKED_EXAMPLE_CAUSES = {
    20: (0.000144000, 0.000027000, 0.000038000, 0.000021945, 0.0),
    40: (0.001023000, 0.000589000, 0.000907000, 0.000264495, 0.0),
    50: (0.003364142, 0.001604531, 0.001904493, 0.000721682, 0.0),
    60: (0.011063000, 0.004371000, 0.003999000, 0.002040465, 0.0),
    80: (0.028353209, 0.009653117, 0.007188769, 0.004745485, 0.008565526),
    99: (0.031734378, 0.010613464, 0.007711596, 0.005256241, 0.103263346),
}
CAUSE_ORDER = ("cancer", "ami", "stroke", "other", "ltc")
CI_TABLE_SUM_40 = 0.0027834950      # the age-40 sum before the 90-day proration

# "The first-year 감액 cohort", the anchor beside its female twin (point_id = 2).
REDUCED_SHARE_M = 0.0015224768
REDUCED_SHARE_F = 0.1785788593
POLS_CI_1_M = 0.0025312484
POLS_CI_1_F = 0.0025101377
POLS_CI_IN_1_0_M = 0.0000038538
POLS_CI_IN_1_1_M = 0.0025273947
POLS_CI_IN_1_0_F = 0.0004482575
POLS_CI_IN_1_1_F = 0.0020618802
ACCEL_COHORT_0 = 40000000.0         # a f B(1)
RESID_COHORT_0 = 60000000.0         # (1 - a f) B(1)
ACCEL_COHORT_1 = 80000000.0         # a B(1)
RESID_COHORT_1 = 20000000.0         # r B(1)

# "First periods of the base run", per policy issued, income-positive, two decimals.
# t: (pols_if, premiums, claims_ci, claims_death, claims_death_ci, claims_lapse,
#     claims_lapse_ci, claim_expenses, expenses, commissions, net_cf)
WORKED_EXAMPLE = {
    1:  (1.000000, 3680880.00,  202345.72,  67827.88,       0.00,      0.00,
         0.00,   962.86, 560000.00, 2944704.00,   -94960.46),
    2:  (0.899643, 3301168.86,  220487.09,  63074.41,     107.44,  95837.96,
         27.61,  1017.66,  54518.35,   99035.07,  2767063.27),
    3:  (0.828861, 3029712.40,  223496.20,  60242.25,     232.50, 155031.92,
         129.16,  1022.32,  50731.24,   90891.37,  2447935.45),
    4:  (0.777714, 2830554.84,  230706.13,  58782.68,     369.83, 177671.85,
         307.63,  1047.04,  48076.77,   84916.65,  2228676.26),
    5:  (0.740045, 2680801.41,  241510.24,  58362.95,     524.37, 180329.00,
         568.27,  1088.61,  46205.65,   80424.04,  2071788.28),
    6:  (0.711873, 2565614.83,  255569.54,  58780.55,     701.60, 172218.87,
         918.80,  1145.25,  44891.16,   76968.44,  1954420.62),
    7:  (0.690531, 2475022.37,  272713.12,  59910.73,     966.82, 158624.07,
         1369.16,  1216.02,  43980.77,   74250.67,  1861991.02),
    8:  (0.674179, 2402109.36,  292880.17,  61681.16,    1413.19, 139275.07,
         1886.08,  1300.60,  43368.68,   72063.28,  1788241.12),
    9:  (0.661516, 2341951.30,  316085.82,  64051.88,    2006.80, 120917.74,
         2513.60,  1399.07,  42979.60,   70258.54,  1721738.25),
    10: (0.651600, 2290957.96,  342399.04,  67008.12,    2790.65, 104026.79,
         3266.73,  1511.80,  42758.74,   68728.74,  1658467.34),
    11: (0.643742, 2246456.27,  371927.65,  70551.95,    3820.76,  88809.28,
         4162.71,  1639.42,  42665.52,   67393.69,  1595485.30),
    12: (0.637425, 2206416.97,  404807.21,  74699.16,    5170.03,  75311.49,
         5221.15,  1782.73,  42669.32,   66192.51,  1530563.38),
    19: (0.612442, 1951820.87,  741988.66, 123396.38,   36300.58,  20539.84,
         19430.89,  3320.79,  43954.29,   58554.63,   904334.83),
    20: (0.609667, 1910336.10,  806942.87, 133615.29,   47357.04,  33523.33,
         22857.18,  3632.94,  44192.65,   57310.08,   760904.71),
    21: (0.606785,       0.00,  876156.24, 144730.49,   58914.27, 265334.96,
         25572.73,  3972.33,  44423.61,       0.00, -1419104.62),
    22: (0.600132,       0.00,  932664.85, 157102.22,   73927.95, 259864.97,
         28519.43,  4281.19,  44375.84,       0.00, -1500736.45),
    30: (0.534280,       0.00, 1119820.70, 274344.69,  370227.02, 195551.95,
         55220.20,  6440.56,  42779.95,       0.00, -2064385.07),
    36: (0.454429,       0.00,  939735.86, 369909.07,  927116.19, 137915.69,
         66808.55,  7972.83,  38624.73,       0.00, -2488082.92),
    40: (0.376450,       0.00,  760086.23, 421392.17, 1450315.78, 101218.63,
         63423.56,  9143.32,  33296.00,       0.00, -2838875.69),
    50: (0.118327,       0.00,  310774.99, 376037.80, 1712695.56,  28635.64,
         18781.38,  7761.07,  11560.65,       0.00, -2466247.11),
    60: (0.003694,       0.00,   32650.34,  59881.52,   91380.48,   1173.85,
         71.52,   580.86,    398.65,       0.00,  -186137.21),
    61: (0.002152,       0.00,       0.00,  48303.96,   55170.51,    807.14,
         15.24,   312.26,    234.62,       0.00,  -104843.72),
    71: (0.000000,       0.00,       0.00,     12.35,       0.00,      0.00,
         0.00,     0.04,      0.01,       0.00,      -12.41),
}
CF_COLUMNS = ("pols_if", "premiums", "claims_ci", "claims_death", "claims_death_ci",
              "claims_lapse", "claims_lapse_ci", "claim_expenses", "expenses",
              "commissions", "net_cf")

# "The values run at the same anniversaries":
# t -> (pol_val_pp, surr_chg_pp, cv_std_pp, cv_pp, cv_pp_ci, resid_db_avg_pp).
WORKED_EXAMPLE_VALUES = {
    1:  (2760145.77, 3381174.86,        0.00,        0.00,        0.00,        0.00),
    2:  (5550566.30, 2817645.71,  2732920.59,  1366460.29,  2732920.59, 20060899.07),
    3:  (8392607.38, 2254116.57,  6138490.80,  3069245.40,  6138490.80, 20029061.61),
    4:  (11286594.94, 1690587.43,  9596007.52,  4798003.76,  9596007.52, 20018954.53),
    5:  (14232900.33, 1127058.29, 13105842.05,  6552921.02, 13105842.05, 20013924.12),
    6:  (17231963.00,  563529.14, 16668433.86,  8334216.93, 16668433.86, 20010881.51),
    7:  (20284322.89,       0.00, 20284322.89, 10142161.45, 20284322.89, 21307079.49),
    8:  (23390658.22,       0.00, 23390658.22, 11695329.11, 23390658.22, 24566693.06),
    9:  (26551836.49,       0.00, 26551836.49, 13275918.24, 26551836.49, 27884412.47),
    10: (29768973.76,       0.00, 29768973.76, 14884486.88, 29768973.76, 31261242.19),
    11: (33043510.43,       0.00, 33043510.43, 16521755.22, 33043510.43, 34698593.36),
    12: (36377303.35,       0.00, 36377303.35, 18188651.67, 36377303.35, 38198350.35),
    15: (46761639.79,       0.00, 46761639.79, 23380819.90, 46761639.79, 49100464.66),
    19: (61684507.76,       0.00, 61684507.76, 30842253.88, 61684507.76, 64768733.14),
    20: (65663373.78,       0.00, 65663373.78, 65663373.78, 65663373.78, 68946542.47),
    21: (66650546.84,       0.00, 66650546.84, 66650546.84, 66650546.84, 69983074.18),
    30: (74586898.30,       0.00, 74586898.30, 74586898.30, 74586898.30, 78316243.21),
    40: (82400303.57,       0.00, 82400303.57, 82400303.57, 82400303.57, 86520318.75),
    60: (93654892.89,       0.00, 93654892.89, 93654892.89, 93654892.89, 98337637.53),
    71: (0.00,              0.00,        0.00,        0.00,        0.00,        0.00),
}
VALUE_COLUMNS = ("pol_val_pp", "surr_chg_pp", "cv_std_pp", "cv_pp", "cv_pp_ci",
                 "resid_db_avg_pp")

# The 기본보험금, flat at SA and then following the account.
CUM_PREM_AT_PAID_UP = 73617600.0
BASE_BENEFIT_64 = 100368120.65
BASE_BENEFIT_70 = 102439024.39

# "The policy-loan room at the same anniversaries, showing the doubling the carve-out
# produces": t -> (loan_avail_pp, loan_avail_ci_pp).
LOAN_ROOM = {
    5:  (5242336.82, 10484673.64),
    7:  (8113729.16, 16227458.31),
    10: (11907589.50, 23815179.01),
    15: (18704655.92, 37409311.83),
    19: (24673803.10, 49347606.21),
    20: (52530699.02, 52530699.02),
    21: (53320437.47, 53320437.47),
}

# "Hand trace, year 1", every count the trace prints.
TRACE_1 = {
    "ci_rate": 0.0025312484246575,
    "phi": 0.0015224768480830,
    "pols_ci_in_0": 0.0000038537671233,
    "pols_ci_in_1": 0.0025273946575342,
    "pols_death": 0.0006782787510712,
    "pols_lapse": 0.0996790472824271,
    "pols_if_pre_2": 0.8971114255418441,
    "pols_if_ci_2": 0.0025312484246575,
    "pols_if_2": 0.8996426739665017,
    "pols_waived_2": 0.0002691334276626,
    "pols_if_pay_2": 0.8968422921141815,
}
CLAIMS_CI_1_COHORT_0 = 154.15
CLAIMS_CI_1_COHORT_1 = 202191.57
POL_VAL_1 = 2760145.7725
SURR_CHG_1 = 3381174.8571

# "Hand trace, year 2 — the first year with a residual death claim".
TRACE_2 = {
    "pols_ci": 0.0027560886764326,
    "pols_death": 0.0006307441013243,
    "pols_death_ci": 0.0000053554888545,
    "pols_lapse": 0.0701359284919917,
    "pols_lapse_ci": 0.0000101035717432,
}
FLOOR_2 = 5828094.62                 # c V(2), below both nominals
CV_2 = 1366460.2944697973
CV_CI_2 = 2732920.5889395946
CLAIM_EXPENSE_EVENTS_2 = 0.0033921882666

# "Hand trace, year 7 — the year the 105% floor takes over".
TRACE_7_COUNTS = {
    "pols_if_pre": 0.6736112278450073,
    "pols_if_ci": 0.0169199804209265,
    "pols_if": 0.6905312082659337,
    "pols_waived": 0.0012115911986317,
    "pols_if_pay": 0.6723996366463756,
}
TRACE_7_COHORTS = {
    0: 0.0000037338177352,
    1: 0.0024487289175376,
    2: 0.0026867133117816,
    3: 0.0027403514656868,
    4: 0.0028466616949308,
    5: 0.0029991719154471,
    6: 0.0031946192978073,
}
FLOOR_6 = 18093561.1545124950        # c V(6), below the KRW 20,000,000 nominal
FLOOR_7 = 21298539.0379573030        # c V(7), above it
POLS_DEATH_CI_7 = 0.0000453753266936
INFLATION_7 = 1.0615201506010

# "Hand trace, year 21 — the first premium-free year".
TRACE_21 = {
    "pols_if_pre": 0.5100226227551737,
    "pols_if_ci": 0.0967627562645090,
    "pols_if": 0.6067853790196827,
    "pols_ci": 0.0109519529389414,
    "pols_death": 0.0014473049424671,
    "pols_death_ci": 0.0008418359795012,
    "pols_lapse": 0.0039809869189901,
    "pols_lapse_ci": 0.0003836836811400,
}
FLOOR_21 = 69983074.18
INFLATION_21 = 1.2201900399480
CLAIM_EXPENSE_EVENTS_21 = 0.0132410938609

# "Roll-forward and undiscounted totals": the four exits and the transition beside them.
SUM_DEATH = 0.1368261313
SUM_DEATH_CI = 0.4111798384
SUM_LAPSE = 0.4301735885
SUM_LAPSE_CI = 0.0218204418
SUM_CI = 0.4330002802                # a transition, deliberately outside the sum
PERSON_YEARS = 26.9098928068
PERSON_YEARS_PRE = 21.0436025135
PERSON_YEARS_CI = 5.8662902933
PERSON_YEARS_PAY = 13.1487304967
POST_CI_PEAK_T = 36
POST_CI_PEAK = 0.2216701767

TOTALS = {
    "premiums": 48398899.11,
    "claims_ci": 34639868.26,
    "claims_death": 13682929.43,
    "claims_death_ci": 36441532.16,
    "claims_lapse": 6222421.82,
    "claims_lapse_ci": 1627249.46,
    "claim_expenses": 294301.87,
    "expenses": 2490051.85,
    "commissions": 4286244.57,
    "net_cf": -51285700.32,
}
PHASE_PAYING = 30720479.96           # sum net_cf, t = 1 ... 20
PHASE_RUN_OFF = -82006180.28         # sum net_cf, t = 21 ... 71

# "Reading the shape of the result" and "Key sensitivities".
TOTAL_BENEFITS = 92614001.14
CI_ORIGINATED = 71081400.43
CI_ORIGINATED_SHARE = 0.7675
DEATH_SHARE = 0.148
RESID_ON_NOMINAL = 8223730.34        # the residual stream with the floor removed
FLOOR_WORTH = 4.43                   # 36,441,532.16 / 8,223,730.34
CLAIMS_AFTER_CI_COVER = 214816.68
DEATH_CI_AFTER_YEAR_40 = 0.698
BENEFITS_AFTER_YEAR_40 = 0.426
INFLATION_TOTAL = 2.01               # 1.01 ** 70
CARVE_OUT_WORTH = 52813.69           # paid less the suppressed counterfactual
SUPPRESSED_LAPSE_CI = 1574435.76
SPURIOUS_PREMIUM_YEARS = 0.695569    # post-CI person-years inside the 납입기간
SPURIOUS_PREMIUM_WON = 2560307.45
SPURIOUS_PREMIUM_YEARS_ALL = 0.7291348   # post-CI plus the 장해 50%+ waived subset
SPURIOUS_PREMIUM_WON_ALL = 2683857.72
CLAIM_EXPENSE_UNDERSTATEMENT = 0.44  # charging on deaths alone
POST_CI_SHARE_OF_INFORCE_36 = 0.488
POST_CI_SHARE_OF_PERSON_YEARS = 0.218

# Sensitivities the notes quantify, as undiscounted sum net_cf on the anchor cell.
SENS_NO_WAIT = -51311242.52          # ci_wait_days = 0
SENS_NO_FIRST_YEAR_CUT = -51285849.76  # first_year_factor = 1.00
SENS_FULL_POST_CI_LAPSE = -50954936.47  # lapse_ci_factor = 1.00
SENS_LEVEL_4_PCT_LAPSE = -34122514.19   # a level 4% paying-period rate

CHECK_CELLS = {
    "check_pols_roll_fwd",
    "check_ci_state_roll_fwd",
    "check_decrement_sum",
    "check_pol_val_roll_fwd",
    "check_accel_complement",
    "check_resid_floor",
    "check_cv_carve_out",
    "check_loan_roll_fwd",
    "check_net_cf",
}


# ---------------------------------------------------------------------------
# The worked example


def test_the_anchor_cell_is_the_one_the_notes_describe(kr_ci_anchor):
    """남자 40 / 1억원 / 종신 / 20년납 / 80% 선지급 / 저해지 k = 0.50, at KRW 3,680,880.

    Every golden number below is conditional on the model point, so it is asserted first
    and in full.  A row silently edited in ``model_point_table.csv`` would otherwise move
    the whole of this module's expected values at once and read as a model failure.
    """
    a = kr_ci_anchor
    assert a.model_point()["policy_id"] == "CI-KR-0001"
    assert a.sex() == "M"
    assert a.age_at_entry() == 40
    assert a.sum_assured() == 100000000.0
    assert a.prem_term() == PREM_PERIOD
    assert a.premium_pp() == G_GROSS
    assert a.premium_pp() / 12 == 306740.0        # the published monthly figure [S4]
    assert a.pols_if_init() == 1.0
    assert a.accel_rate() == ACCEL_RATE
    assert a.resid_rate() == pytest.approx(0.20, abs=1e-15)
    assert a.cv_floor_ratio() == 0.50
    assert a.resid_floor_mult() == 1.05
    assert a.first_year_scope() == "breast"
    assert a.lapse_basis() == "log_linear"
    assert a.waiver_rate(1) == 0.0003
    assert a.pol_loan_util() == 0.0 and a.pol_loan_year() == 0
    assert a.mort_be_factor() == 1.0 and a.ci_be_factor() == 1.0
    assert a.mort_ci_factor() == 3.0


def test_worked_example_derived_scalars(kr_ci_anchor):
    """The notes' table of derived scalars, at the precision it prints them.

    These are the quantities every later number rests on — the horizon, the two
    boundaries, the three EPVs and the two premiums — so they are asserted once, here,
    rather than being inferred from a cash flow that happens to agree.
    """
    a = kr_ci_anchor
    assert a.omega_age() == OMEGA
    assert a.proj_len() == PROJ_LEN == OMEGA - 40 + 1
    assert a.ci_cover_end() == CI_COVER_END == 100 - 40
    assert a.prem_period() == a.prem_end() == PREM_PERIOD
    assert a.disc_factor() == pytest.approx(DISC_FACTOR, abs=5e-16)
    assert a.epv_ben(1) == pytest.approx(A0_1, abs=WON)
    assert a.epv_resid(1) == pytest.approx(A1_1, abs=WON)
    assert a.annuity_due(1) == pytest.approx(ANNUITY_DUE_1, abs=5e-11)
    assert a.prem_net_level_pp() == pytest.approx(P_NET, abs=WON)
    assert a.premium_pp() == G_GROSS
    assert a.premium_pp() / a.prem_net_level_pp() == pytest.approx(LOADING, abs=5e-11)
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    assert a.breast_share() == BREAST_SHARE_M
    assert a.ci_wait_factor() == pytest.approx(CI_WAIT_FACTOR, abs=5e-16)
    assert a.lapse_rate_ult() == LAPSE_ULT
    # A0(1) is 0.448920 of the sum assured, the figure the notes quote beside it.
    assert a.epv_ben(1) / a.sum_assured() == pytest.approx(0.448920, abs=5e-7)


def test_the_equivalence_principle_is_asserted_rather_than_assumed(kr_ci_anchor):
    """P x a-double-dot(1) reproduces A0(1) to the won.

    The net premium is *solved* from the two EPVs, so this is not a tautology about the
    division: it is the statement that the annuity and the benefit EPV are computed on
    the same decrements and the same discount factor.  A CI decrement present in one and
    absent from the other passes every cash flow test in this module and fails here.
    """
    a = kr_ci_anchor
    assert a.prem_net_level_pp() * a.annuity_due(1) == pytest.approx(A0_1, abs=WON)
    assert a.prem_net_level_pp() == pytest.approx(
        a.epv_ben(1) / a.annuity_due(1), rel=1e-14)


def test_the_standard_surrender_charge_cap_is_the_byeolpyo_14_arithmetic(kr_ci_anchor):
    """SC* = 0.80 G x 5% x 20 + 1% SA = KRW 2,944,704 + 1,000,000, in one line.

    The 표준해약공제액 is the statutory ceiling on what a surrender may be made to repay
    [REG-R20], and this model reproduces it from published quantities alone — the gross
    premium and the sum assured — rather than from its own pricing basis.  The notes'
    cross-check against the FSC's 13-times-monthly rule of thumb is asserted to the 1.1%
    they state, because an agreement quoted and not tested is an agreement that drifts.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(
        0.80 * G_GROSS * 0.05 * 20 + 0.01 * a.sum_assured(), rel=1e-14)
    assert 0.80 * G_GROSS * 0.05 * 20 == pytest.approx(2944704.0, abs=WON)
    assert 0.01 * a.sum_assured() == 1000000.0
    assert SC_CAP_RULE_OF_THUMB == pytest.approx(13 * 306740.0, abs=WON)
    gap = abs(a.surr_chg_cap_pp() / SC_CAP_RULE_OF_THUMB - 1.0)
    assert gap == pytest.approx(0.011, abs=5e-4)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(kr_ci_anchor, t):
    """Every cell of the notes' 23-row cash flow table, to the displayed precision.

    The five ``claims_*`` columns are asserted separately rather than as a total, which
    is the point of publishing them separately: ``claims_ci`` and ``claims_death_ci`` are
    two payments arising from **one** decrement at two different dates, and on this form
    the second is the larger of the two over the life of the contract.
    """
    a = kr_ci_anchor
    expected = dict(zip(CF_COLUMNS, WORKED_EXAMPLE[t]))
    assert a.pols_if(t) == pytest.approx(expected["pols_if"], abs=INFORCE)
    assert a.premiums(t) == pytest.approx(expected["premiums"], abs=WON)
    assert a.claims(t, "CI") == pytest.approx(expected["claims_ci"], abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(expected["claims_death"], abs=WON)
    assert a.claims(t, "DEATH_CI") == pytest.approx(
        expected["claims_death_ci"], abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(expected["claims_lapse"], abs=WON)
    assert a.claims(t, "LAPSE_CI") == pytest.approx(
        expected["claims_lapse_ci"], abs=WON)
    assert a.claim_expenses(t) == pytest.approx(expected["claim_expenses"], abs=WON)
    assert a.expenses(t) == pytest.approx(expected["expenses"], abs=WON)
    assert a.commissions(t) == pytest.approx(expected["commissions"], abs=WON)
    assert a.net_cf(t) == pytest.approx(expected["net_cf"], abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_BASIS))
def test_worked_example_decrement_basis_row(kr_ci_anchor, t):
    """The notes' basis table, t = 1 ... 25: the attained age and the four rates.

    The whole product is a race between the CI decrement and the death decrement, and
    the notes print both beside the post-CI rate and the surrender rate so a reader can
    see the race.  ``mort_rate`` at attained 40 and 60 must return [S3]'s own disclosed
    anchors, 0.00068 and 0.00290, with nothing applied to them.
    """
    a = kr_ci_anchor
    attained, ci, mort, mort_ci, lapse = WORKED_EXAMPLE_BASIS[t]
    assert a.age(t) == attained == 40 + t - 1
    assert a.ci_rate(t) == pytest.approx(ci, abs=RATE)
    assert a.mort_rate(t) == pytest.approx(mort, abs=MORT)
    assert a.mort_rate_ci(t) == pytest.approx(mort_ci, abs=MORT)
    assert a.lapse_rate(t) == pytest.approx(lapse, abs=RATE)
    # q' is exactly three times q, and the ratio is the model point's own column.
    assert a.mort_rate_ci(t) == pytest.approx(3.0 * a.mort_rate(t), rel=1e-14)


def test_the_two_sourced_mortality_anchors_are_returned_unmodified(kr_ci_anchor):
    """q(40) = 0.00068 and q(60) = 0.00290 are read, not fitted.

    The table is a Makeham construction everywhere else, so these two rows and q(20) are
    the only mortality in this model that rests on a document.  ``mort_be_factor`` is a
    lever on the decrement and not a change to the 산출방법서 basis, so at 1.00 the
    projection rate and the pricing rate must coincide exactly.
    """
    a = kr_ci_anchor
    assert a.mort_rate_at_age(20) == 0.00051
    assert a.mort_rate_at_age(40) == 0.00068
    assert a.mort_rate_at_age(60) == 0.00290
    assert a.mort_rate(1) == a.mort_rate_base(1) == a.mort_rate_at_age(40)
    assert a.mort_rate(21) == a.mort_rate_base(21) == a.mort_rate_at_age(60)


@pytest.mark.parametrize("attained", sorted(WORKED_EXAMPLE_CAUSES))
def test_worked_example_per_cause_incidence(kr_ci_anchor, attained):
    """The notes' five-cause grid, male, at the ages worth printing.

    The three headline causes at 20, 40 and 60 are [S3]'s disclosed 예정위험률 and are
    the only published Korean CI morbidity anywhere in this library; ``other`` and
    ``ltc`` are constructions.  The last row carries the warning the notes attach to it:
    at attained 99 the 장기요양 limb is two thirds of the whole rate and rests on nothing
    published, so it is asserted as a number rather than trusted as a basis.
    """
    a = kr_ci_anchor
    expected = WORKED_EXAMPLE_CAUSES[attained]
    for cause, value in zip(CAUSE_ORDER, expected):
        assert a.ci_rate_at_age(attained, cause) == pytest.approx(value, abs=CAUSE), cause
    total = sum(a.ci_rate_at_age(attained, c) for c in CAUSE_ORDER)
    assert total == pytest.approx(sum(expected), abs=CAUSE)
    if attained == 99:
        ltc = a.ci_rate_at_age(99, "ltc")
        assert ltc / total > 0.65
    if attained <= 60:
        assert a.ci_rate_at_age(attained, "ltc") == 0.0


def test_the_first_year_ci_rate_is_the_table_sum_less_the_ninety_day_proration(
        kr_ci_anchor):
    """0.0027834950 - (1 - 0.7534246575) x 0.001023 = 0.0025312484.

    Only the ``cancer`` and ``ltc`` limbs carry the 90-day 보장개시일; the other seven
    중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 are covered from the 계약일
    [S1] [S2 별표1 주1].  A model applying the wait to the whole first-year rate cuts the
    other three limbs' cover for ninety days the contract does not cut.
    """
    a = kr_ci_anchor
    table_sum = sum(a.ci_rate_at_age(40, c) for c in CAUSE_ORDER)
    assert table_sum == pytest.approx(CI_TABLE_SUM_40, abs=CAUSE)
    assert a.ci_rate(1) == pytest.approx(
        table_sum - (1 - CI_WAIT_FACTOR) * a.ci_rate_at_age(40, "cancer"), abs=1e-15)
    assert a.ci_rate(1) == pytest.approx(TRACE_1["ci_rate"], abs=TRACE)
    assert a.ci_rate(1) < table_sum
    # From year 2 the proration is gone and the rate is the plain table sum.
    assert a.ci_rate(2) == pytest.approx(
        sum(a.ci_rate_at_age(41, c) for c in CAUSE_ORDER), abs=1e-15)


def test_the_ci_decrement_dominates_the_mortality_decrement(kr_ci_anchor):
    """3.72 times the death rate in policy year 1 and 7.40 times it at attained 60.

    The notes call this the reason a projection of this product is a morbidity
    projection with a mortality tail rather than the reverse, and it is the arithmetic
    behind the processing order: routing an acceleration into the death decrement moves a
    claim to a rate several times smaller.
    """
    a = kr_ci_anchor
    assert a.ci_rate(1) / a.mort_rate(1) == pytest.approx(3.72, abs=5e-3)
    assert a.ci_rate(21) / a.mort_rate(21) == pytest.approx(7.40, abs=5e-3)


def test_the_first_year_reduced_cohort_on_both_sexes(ci_insurance, kr_ci_anchor):
    """The notes' 감액 table: a rounding error on the male cell, 17.86% on the female.

    Cohort 0 is the first-year breast-cancer cohort, paid ``a f B(1)`` and leaving a
    residual of ``(1 - a f) B(1)``.  On the anchor it is 0.15% of year-one accelerations
    and on the female twin it is 17.86% — which is the whole reason the female twin is in
    the shipped table, and the reason a model tested only on the anchor will not notice a
    bug in the cohort machinery.
    """
    male, female = kr_ci_anchor, ci_insurance.Projection[2]
    assert male.ci_reduced_share(1) == pytest.approx(REDUCED_SHARE_M, abs=RATE)
    assert female.ci_reduced_share(1) == pytest.approx(REDUCED_SHARE_F, abs=RATE)
    assert male.pols_ci(1) == pytest.approx(POLS_CI_1_M, abs=RATE)
    assert female.pols_ci(1) == pytest.approx(POLS_CI_1_F, abs=RATE)
    assert male.pols_ci_in(1, 0) == pytest.approx(POLS_CI_IN_1_0_M, abs=RATE)
    assert male.pols_ci_in(1, 1) == pytest.approx(POLS_CI_IN_1_1_M, abs=RATE)
    assert female.pols_ci_in(1, 0) == pytest.approx(POLS_CI_IN_1_0_F, abs=RATE)
    assert female.pols_ci_in(1, 1) == pytest.approx(POLS_CI_IN_1_1_F, abs=RATE)
    for p in (male, female):
        assert p.accel_benefit_pp(0) == ACCEL_COHORT_0
        assert p.resid_nominal_pp(0) == RESID_COHORT_0
        assert p.accel_benefit_pp(1) == ACCEL_COHORT_1
        assert p.resid_nominal_pp(1) == pytest.approx(RESID_COHORT_1, abs=1e-6)
        # The share is a share of that year's own decrement and nil in every other year.
        assert all(p.ci_reduced_share(t) == 0.0 for t in (2, 5, 20, 60))
    # The share is the breast-cancer part of the prorated cancer limb, not of the whole.
    assert male.ci_reduced_share(1) == pytest.approx(
        0.005 * male.ci_rate_at_age(40, "cancer") * CI_WAIT_FACTOR / male.ci_rate(1),
        rel=1e-14)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_VALUES))
def test_worked_example_values_row(kr_ci_anchor, t):
    """The notes' values run: the account, the charge, and the three surrender values.

    ``cv_std_pp`` is the 표준형 twin's value, ``cv_pp`` what a pre-CI policyholder is
    actually paid and ``cv_pp_ci`` what a post-CI one is — three quantities that coincide
    only after 납입완료, and whose separation is the CI-specific delta on the chassis.
    """
    a = kr_ci_anchor
    expected = dict(zip(VALUE_COLUMNS, WORKED_EXAMPLE_VALUES[t]))
    assert a.pol_val_pp(t) == pytest.approx(expected["pol_val_pp"], abs=WON)
    assert a.surr_chg_pp(t) == pytest.approx(expected["surr_chg_pp"], abs=WON)
    assert a.cv_std_pp(t) == pytest.approx(expected["cv_std_pp"], abs=WON)
    assert a.cv_pp(t) == pytest.approx(expected["cv_pp"], abs=WON)
    assert a.cv_pp_ci(t) == pytest.approx(expected["cv_pp_ci"], abs=WON)
    assert a.resid_db_avg_pp(t) == pytest.approx(expected["resid_db_avg_pp"], abs=WON)


def test_the_published_frames_carry_the_same_numbers_as_the_cells(kr_ci_anchor):
    """``result_cf()`` and ``result_val()`` reproduce the two tables the notes print.

    The cells and the frames are two routes to the same numbers and either could drift
    from the other — a column built from the wrong cells, or a row index off by one —
    without any single-cell assertion above noticing.
    """
    cf, val = kr_ci_anchor.result_cf(), kr_ci_anchor.result_val()
    for t, expected in WORKED_EXAMPLE.items():
        for column, value in zip(CF_COLUMNS, expected):
            tol = INFORCE if column == "pols_if" else WON
            assert cf.loc[t, column] == pytest.approx(value, abs=tol), (t, column)
    for t, expected in WORKED_EXAMPLE_VALUES.items():
        for column, value in zip(VALUE_COLUMNS, expected):
            assert val.loc[t, column] == pytest.approx(value, abs=WON), (t, column)


def test_the_average_residual_starts_above_the_nominal_and_then_leaves_it(kr_ci_anchor):
    """KRW 20,060,899.07 at t = 2 for the cohort-0 reason, KRW 86,520,318.75 at t = 40.

    Two different effects lift the in-force mean residual above the stated KRW 20,000,000
    and they must not be confused.  Before t = 7 it is cohort 0's KRW 60,000,000 inside
    the average, decaying as the full cohorts accumulate; from t = 7 it is the 105%
    account floor, and the decay reverses.  A model with one of the two would reproduce
    part of this curve and none of its shape.
    """
    a = kr_ci_anchor
    assert a.resid_db_avg_pp(2) > 20000000.0
    assert a.resid_db_avg_pp(6) < a.resid_db_avg_pp(2)          # the cohort-0 decay
    assert a.resid_db_avg_pp(6) == pytest.approx(20010881.51, abs=WON)
    assert a.resid_db_avg_pp(7) > a.resid_db_avg_pp(6)          # the floor takes over
    for t in range(7, 41):
        assert a.resid_db_avg_pp(t) >= a.resid_db_avg_pp(t - 1)
    assert a.resid_db_avg_pp(40) / 20000000.0 == pytest.approx(4.326, abs=5e-4)


def test_the_base_benefit_is_flat_and_then_follows_the_account(kr_ci_anchor):
    """B(t) = SA to t = 63 and c V(t) from t = 64; cumulative premiums never bind.

    The 기본보험금 is a maximum of three limbs and the notes say plainly that only one of
    them binds on this cell, and only at the very end of a 71-year projection.  Asserting
    the crossing year pins the statement: a model whose ``cum_prem_pp`` limb bound early
    would be paying a different benefit, and one whose ``c V`` limb never bound would have
    the definition of the 기본보험금 wrong at the top of the table.
    """
    a = kr_ci_anchor
    assert a.cum_prem_pp(20) == CUM_PREM_AT_PAID_UP
    assert a.cum_prem_pp(60) == CUM_PREM_AT_PAID_UP     # capped at m, not at t
    assert CUM_PREM_AT_PAID_UP < a.sum_assured()
    for t in (1, 20, 40, 63):
        assert a.base_benefit_pp(t) == a.sum_assured()
        assert a.accel_benefit_pp(t) == pytest.approx(80000000.0, abs=1e-6)
        assert a.resid_nominal_pp(t) == pytest.approx(20000000.0, abs=1e-6)
    assert a.base_benefit_pp(64) == pytest.approx(BASE_BENEFIT_64, abs=WON)
    assert a.base_benefit_pp(64) == pytest.approx(1.05 * a.pol_val_pp(64), rel=1e-14)
    assert a.base_benefit_pp(70) == pytest.approx(BASE_BENEFIT_70, abs=WON)
    assert a.base_benefit_pp(70) == max(
        a.base_benefit_pp(t) for t in range(1, a.proj_len() + 1))
    # V(T) is zero by construction, so the final year falls back to the face amount.
    assert a.pol_val_pp(71) == 0.0 and a.base_benefit_pp(71) == a.sum_assured()


@pytest.mark.parametrize("t", sorted(LOAN_ROOM))
def test_the_policy_loan_room_doubles_at_the_acceleration_date(kr_ci_anchor, t):
    """The notes' loan-room table: a ratio of exactly 2.00 inside the 납입기간.

    The 보험계약대출 limit is 80% of the *payable* value [REG-R25 제33조], and the payable
    value for a post-CI policy is the unsuppressed one at every duration.  So a diagnosis
    doubles the borrowing room with no other change to the contract — a consequence of
    the carve-out that is invisible unless both limits are published.
    """
    a = kr_ci_anchor
    pre, post = LOAN_ROOM[t]
    assert a.loan_avail_pp(t) == pytest.approx(pre, abs=WON)
    assert a.loan_avail_ci_pp(t) == pytest.approx(post, abs=WON)
    expected_ratio = 1.0 if t >= a.prem_period() else 2.0
    assert a.loan_avail_ci_pp(t) / a.loan_avail_pp(t) == pytest.approx(
        expected_ratio, rel=1e-14)
    assert a.loan_avail_pp(t) == pytest.approx(0.8 * a.cv_pp(t), rel=1e-14)
    assert a.loan_avail_ci_pp(t) == pytest.approx(0.8 * a.cv_pp_ci(t), rel=1e-14)


def test_worked_example_year_one_trace(kr_ci_anchor):
    """The notes' year-one trace, line by line.

    Premium on the whole cohort; the acquisition expense and the 80% initial commission;
    the CI transition split into the reduced and the full cohort; deaths among those who
    did **not** accelerate; surrenders paid nothing because CV(1) is zero, the account
    standing below the 해약공제액; and the claim expense charged on two kinds of event.
    """
    a = kr_ci_anchor
    assert a.pols_if_pre(1) == 1.0 and a.pols_if_ci(1) == 0.0
    assert a.pols_if(1) == 1.0 and a.pols_waived(1) == 0.0 and a.pols_if_pay(1) == 1.0
    assert a.premiums(1) == pytest.approx(G_GROSS, abs=WON)
    assert a.expenses(1) == pytest.approx(500000.0 + 60000.0, abs=WON)
    assert a.inflation_factor(1) == 1.0
    assert a.commissions(1) == pytest.approx(0.80 * G_GROSS, abs=WON)

    assert a.ci_reduced_share(1) == pytest.approx(TRACE_1["phi"], abs=TRACE)
    assert a.pols_ci_in(1, 0) == pytest.approx(TRACE_1["pols_ci_in_0"], abs=TRACE)
    assert a.pols_ci_in(1, 1) == pytest.approx(TRACE_1["pols_ci_in_1"], abs=TRACE)
    assert a.pols_ci_in(1, 0) + a.pols_ci_in(1, 1) == pytest.approx(
        a.pols_ci(1), rel=1e-14)
    assert a.pols_ci_in(1, 0) * ACCEL_COHORT_0 == pytest.approx(
        CLAIMS_CI_1_COHORT_0, abs=WON)
    assert a.pols_ci_in(1, 1) * ACCEL_COHORT_1 == pytest.approx(
        CLAIMS_CI_1_COHORT_1, abs=WON)
    assert a.claims(1, "CI") == pytest.approx(
        CLAIMS_CI_1_COHORT_0 + CLAIMS_CI_1_COHORT_1, abs=WON)

    assert a.pols_death(1) == pytest.approx(TRACE_1["pols_death"], abs=TRACE)
    assert a.pols_death(1) == pytest.approx(
        1.0 * (1 - a.ci_rate(1)) * a.mort_rate(1), rel=1e-14)
    assert a.claims(1, "DEATH") == pytest.approx(
        1e8 * TRACE_1["pols_death"], abs=WON)

    assert a.lapse_rate(1) == 0.10
    assert a.pols_lapse(1) == pytest.approx(TRACE_1["pols_lapse"], abs=TRACE)
    assert a.pol_val_pp(1) == pytest.approx(POL_VAL_1, abs=WON)
    assert a.surr_chg_pp(1) == pytest.approx(SURR_CHG_1, abs=WON)
    assert a.pol_val_pp(1) < a.surr_chg_pp(1)
    assert a.cv_std_pp(1) == 0.0 and a.cv_pp(1) == 0.0
    assert a.claims(1, "LAPSE") == 0.0
    assert a.claims(1, "LAPSE_CI") == 0.0
    assert a.claims(1, "DEATH_CI") == 0.0        # no post-CI cohort exists yet

    assert a.claim_expenses(1) == pytest.approx(
        300000.0 * (a.pols_ci(1) + a.pols_death(1)), rel=1e-14)
    assert a.net_cf(1) == pytest.approx(-94960.46, abs=WON)

    assert a.pols_if_pre(2) == pytest.approx(TRACE_1["pols_if_pre_2"], abs=TRACE)
    assert a.pols_if_ci(2) == pytest.approx(TRACE_1["pols_if_ci_2"], abs=TRACE)
    assert a.pols_if(2) == pytest.approx(TRACE_1["pols_if_2"], abs=TRACE)
    assert a.pols_waived(2) == pytest.approx(TRACE_1["pols_waived_2"], abs=TRACE)
    assert a.pols_if_pay(2) == pytest.approx(TRACE_1["pols_if_pay_2"], abs=TRACE)


def test_worked_example_year_two_trace(kr_ci_anchor):
    """The notes' year-two trace — the first year with a residual death claim.

    Two post-CI cohorts exist, both still on their nominal because 1.05 V(2) is below
    both; the residual death benefit is summed cohort by cohort, and the mean residual
    reads KRW 20,060,899.07 rather than KRW 20,000,000 for the cohort-0 reason.  The two
    surrender lines are the carve-out in one row: KRW 2,732,920.59 paid to a post-CI
    policyholder against KRW 1,366,460.29 to a pre-CI one at the same duration.
    """
    a = kr_ci_anchor
    assert a.premiums(2) == pytest.approx(G_GROSS * a.pols_if_pay(2), rel=1e-14)
    assert a.expenses(2) == pytest.approx(
        60000.0 * 1.01 * a.pols_if(2), abs=WON)
    assert a.commissions(2) == pytest.approx(0.03 * a.premiums(2), rel=1e-14)

    assert a.ci_reduced_share(2) == 0.0
    assert a.pols_ci(2) == pytest.approx(TRACE_2["pols_ci"], abs=TRACE)
    assert a.claims(2, "CI") == pytest.approx(
        TRACE_2["pols_ci"] * ACCEL_COHORT_1, abs=WON)

    assert a.pols_death(2) == pytest.approx(TRACE_2["pols_death"], abs=TRACE)
    assert a.pols_death_ci(2) == pytest.approx(TRACE_2["pols_death_ci"], abs=TRACE)
    assert 1.05 * a.pol_val_pp(2) == pytest.approx(FLOOR_2, abs=WON)
    assert a.resid_db_pp(2, 0) == RESID_COHORT_0        # both cohorts on the nominal
    assert a.resid_db_pp(2, 1) == pytest.approx(RESID_COHORT_1, abs=1e-6)
    assert a.claims(2, "DEATH_CI") == pytest.approx(
        a.pols_if_ci_at(2, 0) * a.mort_rate_ci(2) * RESID_COHORT_0
        + a.pols_if_ci_at(2, 1) * a.mort_rate_ci(2) * a.resid_db_pp(2, 1), abs=WON)
    assert a.resid_db_avg_pp(2) == pytest.approx(20060899.07, abs=WON)

    assert a.pols_lapse(2) == pytest.approx(TRACE_2["pols_lapse"], abs=TRACE)
    assert a.pols_lapse_ci(2) == pytest.approx(TRACE_2["pols_lapse_ci"], abs=TRACE)
    assert a.cv_pp(2) == pytest.approx(CV_2, abs=1e-6)
    assert a.cv_pp_ci(2) == pytest.approx(CV_CI_2, abs=1e-6)
    assert a.cv_pp_ci(2) == pytest.approx(2.0 * a.cv_pp(2), rel=1e-14)
    assert a.claims(2, "LAPSE") == pytest.approx(95837.96, abs=WON)
    assert a.claims(2, "LAPSE_CI") == pytest.approx(27.61, abs=WON)

    assert a.claim_expenses(2) == pytest.approx(
        300000.0 * CLAIM_EXPENSE_EVENTS_2, abs=WON)
    assert a.net_cf(2) == pytest.approx(2767063.27, abs=WON)


def test_worked_example_year_seven_trace(kr_ci_anchor):
    """The notes' year-seven trace — the year the 105% account floor takes over.

    1.05 V(6) is KRW 18,093,561.15, below the KRW 20,000,000 nominal, and 1.05 V(7) is
    KRW 21,298,539.04, above it, so the crossing falls inside year 7.  From that
    anniversary six of the seven cohorts carry an identical residual and only cohort 0,
    at KRW 60,000,000, is still on its own nominal.  The 해약공제액 reaches zero in the
    same year, thirteen years before 납입완료.
    """
    a = kr_ci_anchor
    for name, value in TRACE_7_COUNTS.items():
        assert getattr(a, name)(7) == pytest.approx(value, abs=TRACE), name
    assert a.premiums(7) == pytest.approx(
        G_GROSS * TRACE_7_COUNTS["pols_if_pay"], abs=WON)
    assert a.inflation_factor(7) == pytest.approx(INFLATION_7, abs=5e-14)
    assert a.expenses(7) == pytest.approx(
        60000.0 * INFLATION_7 * TRACE_7_COUNTS["pols_if"], abs=WON)
    assert a.commissions(7) == pytest.approx(0.03 * a.premiums(7), rel=1e-14)

    assert 1.05 * a.pol_val_pp(6) == pytest.approx(FLOOR_6, abs=1e-6)
    assert 1.05 * a.pol_val_pp(7) == pytest.approx(FLOOR_7, abs=1e-6)
    assert FLOOR_6 < 20000000.0 < FLOOR_7

    assert a.ci_cohort_ids(7) == [0, 1, 2, 3, 4, 5, 6]
    for s, count in TRACE_7_COHORTS.items():
        assert a.pols_if_ci_at(7, s) == pytest.approx(count, abs=TRACE), s
        expected = RESID_COHORT_0 if s == 0 else FLOOR_7
        assert a.resid_db_pp(7, s) == pytest.approx(expected, abs=1e-6), s
    assert sum(TRACE_7_COHORTS.values()) == pytest.approx(
        a.pols_if_ci(7), abs=TRACE)
    assert a.pols_death_ci(7) == pytest.approx(POLS_DEATH_CI_7, abs=TRACE)
    assert a.claims(7, "DEATH_CI") == pytest.approx(966.82, abs=WON)
    assert a.resid_db_avg_pp(7) == pytest.approx(21307079.4852701761, abs=1e-5)

    assert a.surr_chg_pp(7) == 0.0
    assert a.cv_std_pp(7) == pytest.approx(a.pol_val_pp(7), rel=1e-14)
    assert a.cv_pp(7) == pytest.approx(0.50 * a.pol_val_pp(7), rel=1e-14)
    assert a.cv_pp_ci(7) == pytest.approx(a.pol_val_pp(7), rel=1e-14)
    assert a.net_cf(7) == pytest.approx(1861991.02, abs=WON)


def test_worked_example_year_twenty_one_trace(kr_ci_anchor):
    """The notes' year-21 trace — the first premium-free year and the largest step.

    Three things change in this row: the premium stops, the renewal commission stops with
    it, and the pre-CI lapse rate steps eightfold from 0.001 to 0.008 onto a surrender
    value that has itself just doubled.  ``net_cf`` swings by KRW 2.18m and never returns
    to positive.
    """
    a = kr_ci_anchor
    for name, value in TRACE_21.items():
        assert getattr(a, name)(21) == pytest.approx(value, abs=TRACE), name
    assert a.pols_if_pay(21) == 0.0
    assert a.premiums(21) == 0.0 and a.commissions(21) == 0.0
    assert a.premiums(20) > 0.0 and a.commissions(20) > 0.0
    assert a.inflation_factor(21) == pytest.approx(INFLATION_21, abs=5e-13)
    assert a.expenses(21) == pytest.approx(
        60000.0 * INFLATION_21 * TRACE_21["pols_if"], abs=WON)

    assert a.claims(21, "CI") == pytest.approx(
        TRACE_21["pols_ci"] * ACCEL_COHORT_1, abs=WON)
    assert a.claims(21, "DEATH") == pytest.approx(
        1e8 * TRACE_21["pols_death"], abs=WON)
    assert 1.05 * a.pol_val_pp(21) == pytest.approx(FLOOR_21, abs=WON)
    assert all(a.resid_db_pp(21, s) == pytest.approx(FLOOR_21, abs=WON)
               for s in a.ci_cohort_ids(21))
    assert a.claims(21, "DEATH_CI") == pytest.approx(
        TRACE_21["pols_death_ci"] * FLOOR_21, abs=WON)

    assert a.lapse_rate(20) == pytest.approx(0.001, abs=5e-16)
    assert a.lapse_rate(21) == 0.008
    assert a.cv_mult(21) == 1.0
    assert a.claims(21, "LAPSE") == pytest.approx(
        a.cv_pp(21) * TRACE_21["pols_lapse"], abs=WON)
    assert a.claims(21, "LAPSE") == pytest.approx(265334.96, abs=WON)
    assert a.claims(21, "LAPSE_CI") == pytest.approx(25572.73, abs=WON)
    assert a.claim_expenses(21) == pytest.approx(
        300000.0 * CLAIM_EXPENSE_EVENTS_21, abs=WON)
    assert a.net_cf(20) == pytest.approx(760904.71, abs=WON)
    assert a.net_cf(21) == pytest.approx(-1419104.62, abs=WON)
    assert a.net_cf(20) - a.net_cf(21) == pytest.approx(2180009.33, abs=0.02)
    assert all(a.net_cf(t) < 0.0 for t in range(21, a.proj_len() + 1))


def test_worked_example_undiscounted_totals(kr_ci_anchor):
    """The notes' undiscounted totals over the full 71 years, column by column."""
    df = kr_ci_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert df["pols_if"].sum() == pytest.approx(PERSON_YEARS, abs=SPLIT)
    assert df.loc[1:20, "net_cf"].sum() == pytest.approx(PHASE_PAYING, abs=WON)
    assert df.loc[21:, "net_cf"].sum() == pytest.approx(PHASE_RUN_OFF, abs=WON)
    # Undiscounted, the contract loses money; discounting is out of scope.
    assert df["net_cf"].sum() < 0.0


def test_worked_example_decrement_split(kr_ci_anchor):
    """Four exits summing to exactly 1, with the CI transition standing outside them.

    This is the product's signature identity.  0.4330002802 of the cohort accelerates and
    none of that leaves: 0.4111798384 die having accelerated and 0.1368261313 die without,
    so of the 54.80% who die in force three quarters die post-CI.  A model that counted
    the acceleration as an exit would produce five terms summing above 1.
    """
    a = kr_ci_anchor
    ts = range(1, a.proj_len() + 1)
    deaths = sum(a.pols_death(t) for t in ts)
    deaths_ci = sum(a.pols_death_ci(t) for t in ts)
    lapses = sum(a.pols_lapse(t) for t in ts)
    lapses_ci = sum(a.pols_lapse_ci(t) for t in ts)
    accelerations = sum(a.pols_ci(t) for t in ts)
    assert deaths == pytest.approx(SUM_DEATH, abs=SPLIT)
    assert deaths_ci == pytest.approx(SUM_DEATH_CI, abs=SPLIT)
    assert lapses == pytest.approx(SUM_LAPSE, abs=SPLIT)
    assert lapses_ci == pytest.approx(SUM_LAPSE_CI, abs=SPLIT)
    assert deaths + deaths_ci + lapses + lapses_ci == pytest.approx(1.0, abs=1e-10)
    assert accelerations == pytest.approx(SUM_CI, abs=SPLIT)
    assert accelerations > lapses_ci + deaths      # far too large to be an exit
    assert a.pols_if(a.proj_len() + 1) == 0.0
    assert (deaths + deaths_ci) == pytest.approx(0.548006, abs=5e-7)
    assert deaths_ci / (deaths + deaths_ci) == pytest.approx(0.7503, abs=5e-5)


def test_worked_example_person_years_and_the_post_ci_peak(kr_ci_anchor):
    """26.9098928068 person-years, of which 5.8662902933 are post-CI.

    The post-CI cohort peaks at 0.2216701767 policies at t = 36, attained age 75 — 48.8%
    of the in-force count at that anniversary.  These are the weights on maintenance
    expense and on premium respectively, and getting either cohort's person-years wrong
    moves a whole expense or income line without moving any benefit.
    """
    a = kr_ci_anchor
    ts = range(1, a.proj_len() + 1)
    assert sum(a.pols_if(t) for t in ts) == pytest.approx(PERSON_YEARS, abs=SPLIT)
    assert sum(a.pols_if_pre(t) for t in ts) == pytest.approx(
        PERSON_YEARS_PRE, abs=SPLIT)
    assert sum(a.pols_if_ci(t) for t in ts) == pytest.approx(
        PERSON_YEARS_CI, abs=SPLIT)
    assert sum(a.pols_if_pay(t) for t in ts) == pytest.approx(
        PERSON_YEARS_PAY, abs=SPLIT)
    peak = max(ts, key=a.pols_if_ci)
    assert peak == POST_CI_PEAK_T
    assert a.pols_if_ci(peak) == pytest.approx(POST_CI_PEAK, abs=SPLIT)
    assert a.age(peak) == 75
    assert a.pols_if_ci(peak) / a.pols_if(peak) == pytest.approx(
        POST_CI_SHARE_OF_INFORCE_36, abs=5e-4)
    assert PERSON_YEARS_CI / PERSON_YEARS == pytest.approx(
        POST_CI_SHARE_OF_PERSON_YEARS, abs=5e-4)


def test_the_two_cross_checks_that_fell_out_of_the_model(ci_insurance, kr_ci_anchor):
    """The 80% form at 1.0794 times the 50% form, against [S4]'s published 1.085.

    Nothing in the construction was fitted to this.  Model point 3 is the anchor's own
    cell at a = 0.50 — same sex, same age, same sum assured, same 납입기간 — and the
    pricing quantities do not see the suppression factor or the lapse basis, so the ratio
    of the two net premiums is a clean second route to the price of thirty percentage
    points of acceleration.  Two independent routes agreeing to five parts in a thousand
    is a cross-check; quoting one and not testing it is a hostage.
    """
    a, half = kr_ci_anchor, ci_insurance.Projection[3]
    assert half.sex() == a.sex() and half.age_at_entry() == a.age_at_entry()
    assert half.sum_assured() == a.sum_assured()
    assert half.prem_period() == a.prem_period()
    assert half.accel_rate() == 0.50
    assert half.epv_ben(1) == pytest.approx(A0_1_HALF, abs=WON)
    assert half.prem_net_level_pp() == pytest.approx(P_NET_HALF, abs=WON)
    relativity = a.prem_net_level_pp() / half.prem_net_level_pp()
    assert relativity == pytest.approx(FORM_RELATIVITY_MODEL, abs=5e-5)
    assert abs(relativity / FORM_RELATIVITY_PUBLISHED - 1.0) < 0.006
    # The annuity is identical on the two forms: only the benefit EPV moves.
    assert half.annuity_due(1) == pytest.approx(a.annuity_due(1), rel=1e-14)


def test_the_gross_to_net_loading_is_not_the_published_premium_index(kr_ci_anchor):
    """1.2400 sits beside a disclosed 보험료지수 of 130.1% and is a different ratio.

    The index is computed against the 금융감독원's prescribed 표준순보험료 and this is
    against the model's own net premium, so the agreement is one of order only and
    neither figure was used to calibrate the other.  The test states the relationship the
    notes state — same order, not equal — so that nobody later "fixes" one to the other.
    """
    a = kr_ci_anchor
    loading = a.premium_pp() / a.prem_net_level_pp()
    assert loading == pytest.approx(LOADING, abs=5e-11)
    assert 1.15 < loading < 1.35
    assert loading != pytest.approx(1.301, rel=1e-3)
    assert a.prem_net_level_pp() < a.premium_pp()


def test_the_shape_of_the_result_is_the_one_the_notes_read(kr_ci_anchor):
    """The residual is the larger stream, and 76.7% of benefits are CI-originated.

    Three readings the notes take off the totals, each of which a plausible alternative
    implementation would break: the 20% residual pays more, undiscounted, than the 80%
    acceleration; the two CI-originated streams are three quarters of all benefits
    against the pre-CI death benefit's 14.8%; and 42.6% of all benefits fall after t = 40,
    so a projection truncated anywhere convenient understates materially.
    """
    a = kr_ci_anchor
    df = a.result_cf()
    benefits = df[["claims_ci", "claims_death", "claims_death_ci", "claims_lapse",
                   "claims_lapse_ci"]]
    assert benefits.sum().sum() == pytest.approx(TOTAL_BENEFITS, abs=WON)
    assert df["claims_death_ci"].sum() > df["claims_ci"].sum()
    assert df["claims_death_ci"].sum() > df["claims_death"].sum()
    ci_originated = df["claims_ci"].sum() + df["claims_death_ci"].sum()
    assert ci_originated == pytest.approx(CI_ORIGINATED, abs=WON)
    assert ci_originated / benefits.sum().sum() == pytest.approx(
        CI_ORIGINATED_SHARE, abs=5e-4)
    assert df["claims_death"].sum() / benefits.sum().sum() == pytest.approx(
        DEATH_SHARE, abs=5e-4)
    assert benefits.loc[41:].sum().sum() / benefits.sum().sum() == pytest.approx(
        BENEFITS_AFTER_YEAR_40, abs=5e-4)
    assert df.loc[41:, "claims_death_ci"].sum() / df["claims_death_ci"].sum() == (
        pytest.approx(DEATH_CI_AFTER_YEAR_40, abs=5e-4))


def test_the_residual_floor_is_worth_four_times_the_nominal_complement(kr_ci_anchor):
    """KRW 36,441,532.16 paid against KRW 8,223,730.34 on the nominal, a factor of 4.43.

    One number, ``resid_floor_mult = 1.05``, carries the largest benefit line in the
    projection.  Recomputing the post-CI death stream on the stated complement alone —
    which is what "80% now, 20% later" describes — collapses it to under a quarter, and
    that gap is the single largest structural feature of this liability and the easiest to
    omit.
    """
    a = kr_ci_anchor
    on_nominal = sum(
        sum(a.pols_if_ci_at(t, s) * a.mort_rate_ci(t) * a.resid_nominal_pp(s)
            for s in a.ci_cohort_ids(t))
        for t in range(1, a.proj_len() + 1))
    assert on_nominal == pytest.approx(RESID_ON_NOMINAL, abs=WON)
    paid = a.result_cf()["claims_death_ci"].sum()
    assert paid / on_nominal == pytest.approx(FLOOR_WORTH, abs=5e-3)


def test_the_acceleration_costs_a_quarter_of_the_net_premium(kr_ci_anchor):
    """A0(1) = KRW 36,085,073.09 with no acceleration, against KRW 44,892,002.95 with it.

    The counterfactual is the same three-state contract paying the whole sum assured on
    death whenever it falls — a = 0, r = 1 — on the identical table and decrements, so
    the difference is purely the timing effect of moving four fifths of one sum assured
    forward and flooring the remainder.  It is recomputed here from the model's own rate
    cells rather than from a second model point, because ``accel_rate`` validates to the
    open interval and a = 0 is not a contract this product admits.
    """
    a = kr_ci_anchor
    v, sa, t_end, m = a.disc_factor(), a.sum_assured(), a.proj_len(), a.prem_period()
    resid = 0.0
    resid_by_t = {t_end + 1: 0.0}
    for t in range(t_end, 0, -1):
        q = a.mort_rate_ci_base(t)
        resid = v * (q * sa + (1.0 - q) * resid)
        resid_by_t[t] = resid
    benefit = 0.0
    for t in range(t_end, 0, -1):
        qc, qd = a.ci_rate_base(t), a.mort_rate_base(t)
        benefit = v * ((1.0 - qc) * qd * sa + qc * resid_by_t[t + 1]
                       + (1.0 - qc) * (1.0 - qd) * benefit)
    annuity = 0.0
    for t in range(m, 0, -1):
        annuity = 1.0 + v * (1.0 - a.ci_rate_base(t)) * (
            1.0 - a.mort_rate_base(t)) * annuity
    assert benefit == pytest.approx(A0_1_NO_ACCEL, abs=WON)
    assert annuity == pytest.approx(a.annuity_due(1), rel=1e-14)   # unchanged by a
    assert benefit / annuity == pytest.approx(P_NET_NO_ACCEL, abs=WON)
    assert a.prem_net_level_pp() / (benefit / annuity) - 1.0 == pytest.approx(
        ACCELERATION_COST, abs=5e-5)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_the_acceleration_is_a_transition_not_an_exit(kr_ci_anchor):
    """l(t) - l(t+1) = D + D' + S + S' — **four** terms, and C(t) is not one of them.

    Adding the CI transition to the in-force roll-forward removes every claimant from the
    population on the day they claim, which is precisely what 감독규정 제7-60조제8호
    forbids the contract to do.  The symptom is a decrement sum above 1 and a post-CI
    cohort that never accumulates, and this is the most natural mistake on the product.
    """
    a = kr_ci_anchor
    assert a.check_pols_roll_fwd() is True
    for t in (1, 2, 7, 20, 21, 36, 60, 61, a.proj_len()):
        exits = (a.pols_death(t) + a.pols_death_ci(t)
                 + a.pols_lapse(t) + a.pols_lapse_ci(t))
        assert a.pols_if(t) - a.pols_if(t + 1) == pytest.approx(exits, abs=1e-12)
        assert a.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        # The five-term version is wrong by exactly the year's accelerations.
        assert a.pols_if(t) - a.pols_if(t + 1) - (exits + a.pols_ci(t)) == (
            pytest.approx(-a.pols_ci(t), abs=1e-12))
    # A claimant is still in force: the post-CI cohort accumulates for decades.
    assert a.pols_ci(2) > 0.0 and a.pols_if_ci(3) > a.pols_if_ci(2)
    assert a.check_decrement_sum() is True


def test_pitfall_the_residual_floor_is_two_sided(kr_ci_anchor):
    """max(r B(s), c V(t)) — the nominal binds early and the account binds late.

    A one-sided maximum is right for most of the projection and wrong at the ends: before
    t = 7 the nominal binds on every cohort and after it the account does, while cohort
    0's KRW 60,000,000 stays on its own nominal until t = 18.  ``check_resid_floor()``
    tests the two limbs separately, and both directions are asserted here.
    """
    a = kr_ci_anchor
    assert a.check_resid_floor() is True
    for t in (2, 6):
        assert 1.05 * a.pol_val_pp(t) < 20000000.0
        assert a.resid_db_pp(t, 1) == pytest.approx(RESID_COHORT_1, abs=1e-6)
        assert a.resid_db_pp(t, 1) > 1.05 * a.pol_val_pp(t)          # nominal limb
    for t in (7, 21, 40):
        assert 1.05 * a.pol_val_pp(t) > 20000000.0
        assert a.resid_db_pp(t, 1) == pytest.approx(
            1.05 * a.pol_val_pp(t), rel=1e-14)                       # account limb
    # Cohort 0 crosses seven years after cohort 1, on its own larger nominal.
    assert a.resid_db_pp(17, 0) == RESID_COHORT_0
    assert a.resid_db_pp(18, 0) == pytest.approx(1.05 * a.pol_val_pp(18), rel=1e-14)
    assert a.resid_db_pp(18, 0) > RESID_COHORT_0
    for t in (2, 7, 18, 40, 60):
        for s in a.ci_cohort_ids(t):
            assert a.resid_db_pp(t, s) >= a.resid_nominal_pp(s) - 1e-6
            assert a.resid_db_pp(t, s) >= 1.05 * a.pol_val_pp(t) - 1e-6
        assert a.check_resid_floor_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_pitfall_the_floor_and_the_nominal_are_read_off_different_anniversaries(
        kr_ci_anchor):
    """B(s) is the 기본보험금 at the acceleration date; V(t) is the account **now**.

    ``resid_db_pp(t, s)`` mixes two clocks on purpose, and reading both off t, or both
    off s, is wrong in opposite directions.  Neither error shows before t = 7, when both
    limbs still agree at the nominal — which is why a model can be built, tested on the
    early durations, and be wrong for sixty years.
    """
    a = kr_ci_anchor
    # The nominal moves with s and not with t; the floor moves with t and not with s.
    assert a.resid_nominal_pp(1) == pytest.approx(a.resid_nominal_pp(40), abs=1e-6)
    assert a.resid_nominal_pp(0) != pytest.approx(a.resid_nominal_pp(1), rel=1e-6)
    assert a.resid_db_pp(40, 1) == a.resid_db_pp(40, 39)      # the shared floor
    assert a.resid_db_pp(40, 1) != pytest.approx(a.resid_db_pp(20, 1), rel=1e-6)
    # Reading the nominal off t instead of s destroys cohort 0's larger residual.
    assert a.resid_db_pp(10, 0) == RESID_COHORT_0
    assert a.resid_db_pp(10, 1) < RESID_COHORT_0
    # Reading the floor off s instead of t freezes the residual at the entry account.
    assert 1.05 * a.pol_val_pp(1) < 1.05 * a.pol_val_pp(40)
    assert a.resid_db_pp(40, 1) > 1.05 * a.pol_val_pp(1)


def test_pitfall_collapsing_the_post_ci_cohorts_loses_the_first_year_reduced_one(
        ci_insurance):
    """Cohort 0 carries KRW 60,000,000 where every other cohort carries KRW 20,000,000.

    On the male anchor it is 0.15% of year-one accelerations and the error is invisible;
    on the female twin it is 17.86% and it is not.  This is why the test runs on
    ``point_id = 2`` and ``4`` and not only on the anchor: a model that averaged the
    cohorts would agree with the anchor's totals to four significant figures.
    """
    female = ci_insurance.Projection[2]
    assert female.ci_reduced_share(1) == pytest.approx(REDUCED_SHARE_F, abs=RATE)
    assert female.resid_nominal_pp(0) == RESID_COHORT_0
    assert female.resid_nominal_pp(1) == pytest.approx(RESID_COHORT_1, abs=1e-6)
    assert female.accel_benefit_pp(0) == 0.5 * female.accel_benefit_pp(1)
    # Cohort 0 survives the whole projection and never merges with the others.
    assert female.pols_if_ci_at(40, 0) > 0.0
    assert female.pols_if_ci_at(2, 0) == pytest.approx(female.pols_ci_in(1, 0), abs=1e-15)
    # The claim it produces in year 1 is a sixth of that year's acceleration outgo.
    reduced = female.pols_ci_in(1, 0) * female.accel_benefit_pp(0)
    assert reduced / female.claims(1, "CI") == pytest.approx(0.098, abs=5e-3)
    # The all-trigger design routes the whole of year one into cohort 0 and halves it.
    allpt = ci_insurance.Projection[4]
    assert allpt.first_year_scope() == "all"
    assert allpt.ci_reduced_share(1) == 1.0
    assert allpt.pols_ci_in(1, 1) == 0.0
    assert allpt.pols_ci_in(1, 0) == pytest.approx(allpt.pols_ci(1), rel=1e-14)
    assert allpt.claims(1, "CI") == pytest.approx(
        0.8 * 0.5 * allpt.sum_assured() * allpt.pols_ci(1), rel=1e-14)
    assert allpt.check_accel_complement() is True


def test_pitfall_the_premium_annuity_must_carry_the_ci_decrement(kr_ci_anchor):
    """15.1228758581 against an ordinary life annuity's 15.8467943703 — 4.8%.

    Any CI/LTC 지급사유 waives all future 기본보험료, so a premium stream that ran on
    through the post-CI state would over-fund the contract by the whole of the CI
    decrement.  The wrong annuity gives a net premium of KRW 2,832,875.97 against
    KRW 2,968,483.20, and ``check_pol_val_roll_fwd()`` fails immediately, which is what it
    is for.
    """
    a = kr_ci_anchor
    ordinary = 0.0
    for t in range(a.prem_period(), 0, -1):
        ordinary = 1.0 + a.disc_factor() * (1.0 - a.mort_rate_base(t)) * ordinary
    assert ordinary == pytest.approx(ANNUITY_DUE_ORDINARY, abs=5e-11)
    assert a.annuity_due(1) == pytest.approx(ANNUITY_DUE_1, abs=5e-11)
    assert ordinary / a.annuity_due(1) - 1.0 == pytest.approx(0.048, abs=5e-4)
    assert a.epv_ben(1) / ordinary == pytest.approx(P_NET_ORDINARY, abs=WON)
    # The annuity that is used discounts on both decrements, at every duration.
    for t in (1, 10, 20):
        assert a.annuity_due(t) == pytest.approx(
            1.0 + a.disc_factor() * (1.0 - a.ci_rate_base(t))
            * (1.0 - a.mort_rate_base(t)) * a.annuity_due(t + 1), rel=1e-14)
    assert a.annuity_due(a.prem_period() + 1) == 0.0
    assert a.check_pol_val_roll_fwd() is True


def test_pitfall_the_post_ci_cohort_never_pays_a_premium(kr_ci_anchor):
    """lp(t) = l0(t) - lw(t): the post-CI count is nowhere in the premium weight.

    Weighting premium by ``pols_if(t)`` reproduces year 1 exactly and diverges from year
    2 onward — a slow, quiet error worth 0.7291348 person-years of spurious premium inside
    the 납입기간, KRW 2,683,857.72 on this cell, of which the post-CI cohort is 0.6955694
    (KRW 2,560,307.45) and the 장해 50%+ waived subset the remaining 0.0335654.  It is the
    kind of mistake that never fails a roll-forward.
    """
    a = kr_ci_anchor
    assert a.pols_if_pay(1) == a.pols_if(1) == 1.0     # identical in year one only
    for t in (2, 7, 12, 20):
        assert a.pols_if_pay(t) == pytest.approx(
            a.pols_if_pre(t) - a.pols_waived(t), rel=1e-14)
        assert a.pols_if_pay(t) < a.pols_if(t)
        assert a.premiums(t) == pytest.approx(a.premium_pp() * a.pols_if_pay(t),
                                              rel=1e-14)
        assert a.premiums(t) < a.premium_pp() * a.pols_if(t)
    spurious = sum(a.pols_if_ci(t) for t in range(1, a.prem_end() + 1))
    assert spurious == pytest.approx(SPURIOUS_PREMIUM_YEARS, abs=5e-7)
    assert spurious * a.premium_pp() == pytest.approx(SPURIOUS_PREMIUM_WON, abs=0.02)
    # The full substitution error is the post-CI cohort *plus* the waived subset.
    spurious_all = sum(a.pols_if(t) - a.pols_if_pay(t)
                       for t in range(1, a.prem_end() + 1))
    assert spurious_all == pytest.approx(SPURIOUS_PREMIUM_YEARS_ALL, abs=5e-8)
    assert spurious_all * a.premium_pp() == pytest.approx(
        SPURIOUS_PREMIUM_WON_ALL, abs=0.02)
    # Renewal commission follows the cash, so it inherits the same weight.
    assert a.commissions(10) == pytest.approx(0.03 * a.premiums(10), rel=1e-14)


def test_pitfall_the_suppression_has_two_exits_and_one_of_them_is_random(kr_ci_anchor):
    """CV'(t) = W(t) at **every** duration, not from t = m.

    Applying k to the post-CI cohort halves the surrender benefit of exactly the
    policyholders the carve-out exists to protect.  Over the whole projection the
    carve-out is worth only KRW 52,813.69 — because most post-CI surrenders happen after
    납입완료 anyway — so the bug is nearly invisible in the totals and factor-of-two wrong
    at every individual duration inside the 납입기간.  It is tested at t = 2, not on the
    sum.
    """
    a = kr_ci_anchor
    assert a.check_cv_carve_out() is True
    for t in (1, 2, 5, 10, 19):
        assert a.cv_pp_ci(t) == pytest.approx(a.cv_std_pp(t), rel=1e-14)
        assert a.cv_mult(t) == 0.50
        if t > 1:
            assert a.cv_pp_ci(t) == pytest.approx(2.0 * a.cv_pp(t), rel=1e-14)
    for t in (20, 30, 60):
        assert a.cv_pp_ci(t) == pytest.approx(a.cv_pp(t), rel=1e-14)
    suppressed = sum(max(0.0, a.cv_pp(t) - a.loan_pp(t)) * a.pols_lapse_ci(t)
                     for t in range(1, a.proj_len() + 1))
    assert suppressed == pytest.approx(SUPPRESSED_LAPSE_CI, abs=WON)
    paid = a.result_cf()["claims_lapse_ci"].sum()
    assert paid - suppressed == pytest.approx(CARVE_OUT_WORTH, abs=WON)
    assert (paid - suppressed) / paid < 0.04          # invisible in the totals
    assert a.claims(2, "LAPSE_CI") == pytest.approx(
        2.0 * a.cv_pp(2) * a.pols_lapse_ci(2), rel=1e-14)   # and doubled at t = 2


def test_pitfall_the_step_at_paid_up_is_one_over_k_on_one_anniversary(kr_ci_anchor):
    """CV(20) / (k W(20)) = 2.0000000000; the adjacent-year ratio 2.1290 is not the step.

    The multiplier takes two values and only two — k inside the 납입기간 and 1 from it —
    so a model that grades, interpolates or smooths across the boundary fails here.  The
    year-on-year ratio mixes the step with a year of account accrual and must not be
    quoted as the step.
    """
    a = kr_ci_anchor
    m = a.prem_period()
    assert m == 20
    assert {a.cv_mult(t) for t in range(1, a.proj_len() + 1)} == {0.50, 1.0}
    assert a.cv_mult(m - 1) == 0.50 and a.cv_mult(m) == 1.0
    assert a.cv_pp(m) / (0.50 * a.cv_std_pp(m)) == pytest.approx(2.0, abs=5e-11)
    assert a.cv_pp(m) / (0.50 * a.cv_std_pp(m)) == pytest.approx(
        1.0 / a.cv_floor_ratio(), rel=1e-14)
    assert a.cv_pp(m) / a.cv_pp(m - 1) == pytest.approx(2.1290, abs=5e-5)
    assert a.pol_val_pp(m) / a.pol_val_pp(m - 1) < 1.10
    # A surrender in policy year m is paid on the full value, and both values exist.
    assert a.claims(m, "LAPSE") == pytest.approx(
        a.cv_std_pp(m) * a.pols_lapse(m), rel=1e-14)
    assert a.claims(m - 1, "LAPSE") == pytest.approx(
        0.50 * a.cv_std_pp(m - 1) * a.pols_lapse(m - 1), rel=1e-14)


def test_pitfall_the_step_is_not_a_surrender_charge_effect(kr_ci_anchor):
    """SC(t) = 0 from t = 7, thirteen years before the cliff, in seven equal steps.

    A model that ties the two together will place the step at the wrong duration on any
    point where the 해약공제기간 and the 납입기간 differ — which is every point in this
    table but one, the cap being seven years and the payment terms ten, twenty and thirty.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    for t in range(0, SURR_CHG_YEARS):
        assert a.surr_chg_pp(t) == pytest.approx(
            SC_CAP * (SURR_CHG_YEARS - t) / SURR_CHG_YEARS, abs=WON)
    assert a.surr_chg_pp(0) - a.surr_chg_pp(1) == pytest.approx(SC_STEP, abs=1e-6)
    assert all(a.surr_chg_pp(t) == 0.0 for t in (7, 8, 19, 20, 21, 60))
    assert SURR_CHG_YEARS < a.prem_period() - 12
    # The value steps at m with the charge long gone, so the two are unrelated.
    assert a.surr_chg_pp(a.prem_period()) == 0.0
    assert a.cv_pp(a.prem_period()) > 2.0 * a.cv_pp(a.prem_period() - 1)


def test_pitfall_the_statutory_cap_uses_the_pre_acceleration_sum_assured(kr_ci_anchor):
    """KRW 100,000,000, not the KRW 20,000,000 residual: a 20% under-statement avoided.

    별표 15 제3호 read with 제8호 takes the 일반사망보험금 before any 증감, and a CI
    contract covers death from any cause, so 일반사망 applies directly.  Building the cap
    off the residual would cut it from KRW 3,944,704 to KRW 3,144,704 and shrink every
    early surrender charge with it.
    """
    a = kr_ci_anchor
    assert a.surr_chg_cap_pp() == pytest.approx(SC_CAP, abs=WON)
    on_residual = (0.80 * a.premium_pp() * 0.05 * 20
                   + 0.01 * a.resid_rate() * a.sum_assured())
    assert on_residual == pytest.approx(3144704.0, abs=WON)
    assert a.surr_chg_cap_pp() - on_residual == pytest.approx(800000.0, abs=WON)
    assert on_residual / a.surr_chg_cap_pp() - 1.0 == pytest.approx(-0.203, abs=5e-4)
    # The cap is built from the gross premium and the face amount, nothing else.
    assert a.surr_chg_cap_pp() == pytest.approx(
        0.80 * a.premium_pp() * 0.05 * 20 + 0.01 * a.sum_assured(), rel=1e-14)


def test_pitfall_ci_before_death_before_lapse(kr_ci_anchor):
    """The processing order, asserted through a quantity that would move if it changed.

    Reversing the first two routes lives that would have accelerated into the death
    decrement, which is 3.72 times smaller in policy year 1 and 7.40 times smaller at
    attained 60.  The order is [std] and is asserted rather than described: deaths are
    taken from the survivors of the CI transition and surrenders from the survivors of
    both.
    """
    a = kr_ci_anchor
    for t in (1, 2, 7, 21, 40):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_death(t) == pytest.approx(
            a.pols_if_pre(t) * (1 - a.ci_rate(t)) * a.mort_rate(t), rel=1e-14)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_pre(t) * (1 - a.ci_rate(t)) * (1 - a.mort_rate(t))
            * a.lapse_rate(t), rel=1e-14)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(a.pols_if(t + 1), abs=1e-14)
        # Death first would give a strictly larger death count at every duration.
        death_first = a.pols_if_pre(t) * a.mort_rate(t)
        assert death_first > a.pols_death(t)
    # The re-routing is worth more than the whole pre-CI death stream in year 1.
    assert a.pols_if_pre(1) * a.mort_rate(1) - a.pols_death(1) == pytest.approx(
        a.ci_rate(1) * a.mort_rate(1), rel=1e-12)
    assert a.pols_if_at(1, "BEF_LAPSE") == pytest.approx(
        1.0 * (1 - a.ci_rate(1)) * (1 - a.mort_rate(1)) + a.pols_ci(1), rel=1e-14)
    assert a.check_ci_state_roll_fwd() is True


def test_pitfall_the_two_payments_are_one_step_apart(kr_ci_anchor):
    """A life accelerating in year t joins the post-CI state at the start of year t + 1.

    Paying an acceleration and a residual death benefit in the same year on the same life
    double-counts the claim expense and mis-times the residual.  Year 1 is the clean case:
    accelerations occur and no residual death benefit is paid at all.
    """
    a = kr_ci_anchor
    assert a.pols_ci(1) > 0.0
    assert a.pols_if_ci(1) == 0.0
    assert a.pols_death_ci(1) == 0.0 and a.claims(1, "DEATH_CI") == 0.0
    assert a.pols_if_ci(2) == pytest.approx(a.pols_ci(1), rel=1e-14)
    assert a.claims(2, "DEATH_CI") > 0.0
    for t in (2, 7, 21):
        # No cohort labelled t or later can be populated at the start of year t.
        assert a.ci_cohort_ids(t) == [0] + list(range(1, t))
        assert a.pols_if_ci_at(t, t) == 0.0
        assert a.pols_if_ci_at(t + 1, t) == pytest.approx(a.pols_ci_in(t, t), rel=1e-14)
    # The claim expense counts the acceleration once, in its own year.
    assert a.claim_expenses(1) == pytest.approx(
        300000.0 * (a.pols_ci(1) + a.pols_death(1)), rel=1e-14)


def test_pitfall_the_ci_decrement_stops_at_n_ci_and_nothing_else_does(kr_ci_anchor):
    """Three end dates in one projection: t = 20, t = 60 and t = 71.

    The premium stops at 납입완료, the CI cover at the 100세 계약해당일 and the contract at
    the mortality table's terminal age.  The eleven post-CI-cover years still carry
    KRW 214,816.68 of claims, so truncating the projection at the end of CI cover — or at
    attained age 100 — understates materially.
    """
    a = kr_ci_anchor
    assert (a.prem_end(), a.ci_cover_end(), a.proj_len()) == (20, 60, 71)
    assert a.age(a.ci_cover_end()) == 99
    assert a.ci_rate(60) > 0.0 and a.ci_rate(61) == 0.0
    assert all(a.ci_rate(t) == 0.0 for t in range(61, a.proj_len() + 1))
    assert a.claims(60, "CI") > 0.0 and a.claims(61, "CI") == 0.0
    assert a.premiums(20) > 0.0 and a.premiums(21) == 0.0
    for t in (61, 65, 70):
        assert a.claims(t, "DEATH") > 0.0
        assert a.claims(t, "LAPSE") > 0.0
        assert a.expenses(t) > 0.0
    assert a.claims(61, "DEATH_CI") > 0.0
    # A fourth date, and it is a consequence rather than a boundary: q' is three times
    # q and caps at 1 from attained age 101, so the post-CI cohort is extinguished at
    # t = 62 while the pre-CI one runs another nine years.
    assert a.mort_rate_ci(62) == 1.0 and a.mort_rate(62) < 1.0
    assert a.pols_if_ci(62) > 0.0 and a.pols_if_ci(63) == 0.0
    assert a.claims(63, "DEATH_CI") == 0.0 and a.claims(63, "DEATH") > 0.0
    tail = sum(a.claims(t) for t in range(a.ci_cover_end() + 1, a.proj_len() + 1))
    assert tail == pytest.approx(CLAIMS_AFTER_CI_COVER, abs=WON)
    # The horizon is the table's: q = 1 in the final year and nobody survives it.
    assert a.mort_rate(a.proj_len()) == 1.0
    assert a.mort_rate_ci(a.proj_len()) == 1.0
    assert a.pols_if(a.proj_len()) > 0.0
    assert a.pols_if(a.proj_len() + 1) == 0.0


def test_pitfall_ci_rate_is_a_first_event_rate(ci_insurance, kr_ci_anchor):
    """One rate across the whole trigger set, and one benefit paid once.

    The benefit is payable once only across eight 중대한 질병, four 중대한 수술, 중대한
    화상 및 부식 and 장기요양상태, and the Korean supervisor required the overlap between
    causes to be reflected in the filed rate.  A table built by adding published
    site-specific incidences double-counts every life carrying two qualifying conditions —
    so the model reads one grid, sums it once, and exposes no second CI decrement anywhere.
    """
    a = kr_ci_anchor
    assert a.ci_rate(21) == pytest.approx(
        sum(a.ci_rate_at_age(60, c) for c in CAUSE_ORDER), abs=1e-15)
    # There is exactly one CI decrement and one acceleration benefit kind.
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("ci_rate_cancer", "ci_rate_ami", "ci_rate_stroke",
                   "pols_ci_second", "claims_ci_second", "multi_pay"):
        assert absent not in names, f"{absent}: a second CI event"
    with pytest.raises(FormulaError):
        a.claims(5, "CI_SECOND")
    # A cohort accelerates once: entrants exist only in their own labelled year.
    assert a.pols_ci_in(5, 5) == pytest.approx(a.pols_ci(5), rel=1e-14)
    assert a.pols_ci_in(6, 5) == 0.0 and a.pols_ci_in(5, 4) == 0.0
    doc = flat(ci_insurance.Projection.cells["ci_rate_base"].doc)
    assert "first-event" in doc


def test_pitfall_there_is_no_survival_period(ci_insurance, kr_ci_anchor):
    """The Korean supervisor refused the overseas 30-day requirement, so none is modelled.

    Importing it would move lives from the CI decrement to the death decrement and change
    what they are paid from ``a B`` plus a later ``r B`` to ``B`` once.  The consequence
    the model does carry instead is post-CI excess mortality — the two decrements are
    correlated and ``mort_ci_factor`` is where that correlation lives.
    """
    a = kr_ci_anchor
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("survival_period", "survival_days", "surv_period_days",
                   "ci_survival_factor"):
        assert absent not in names, f"{absent}: this contract has no survival period"
    # A claimant is paid in the year of the event, whatever happens next.
    assert a.claims(1, "CI") > 0.0
    assert a.mort_ci_factor() == 3.0
    assert a.mort_rate_ci(1) == pytest.approx(3.0 * a.mort_rate(1), rel=1e-14)
    doc = flat(ci_insurance.Projection.cells["mort_ci_factor"].doc)
    assert "survival period" in doc
    assert "not independent competing risks" in doc


def test_pitfall_pols_if_is_the_total_in_force(kr_ci_anchor):
    """Maintenance expense is weighted by l(t), both states, and premium by lp(t).

    A post-CI policy is still a policy: it is administered, it can surrender, it can
    claim.  Weighting maintenance by ``pols_if_pre`` drops 48.8% of the in-force count at
    t = 36 and 21.8% of the projection's person-years; weighting premium by ``pols_if``
    adds a cohort that pays nothing.  The two errors point in opposite directions and
    neither breaks a roll-forward.
    """
    a = kr_ci_anchor
    for t in (2, 7, 21, 36, 60):
        assert a.pols_if(t) == pytest.approx(
            a.pols_if_pre(t) + a.pols_if_ci(t), rel=1e-14)
        assert a.expenses(t) == pytest.approx(
            60000.0 * a.inflation_factor(t) * a.pols_if(t), rel=1e-14)
        assert a.expenses(t) > 60000.0 * a.inflation_factor(t) * a.pols_if_pre(t)
    assert a.result_cf().loc[36, "pols_if"] == pytest.approx(
        a.pols_if(36), abs=INFORCE)
    assert 1.0 - a.pols_if_pre(36) / a.pols_if(36) == pytest.approx(
        POST_CI_SHARE_OF_INFORCE_36, abs=5e-4)
    # The acquisition expense and initial commission ride on l(1) alone.
    assert a.expenses(1) == pytest.approx(500000.0 + 60000.0, abs=WON)
    assert a.commissions(1) == pytest.approx(0.80 * a.premium_pp(), abs=WON)


def test_pitfall_the_claim_expense_is_charged_on_three_events(kr_ci_anchor):
    """CI, pre-CI death and post-CI death; charging on deaths alone loses 44%.

    Two payments mean two claim events and two handling costs, and the CI event is the
    more expensive of the two to adjudicate in practice, the whole dispute record of this
    product being about the 중대한 definitions.  The expense is published in its own
    column and is not inside ``expenses``.
    """
    a = kr_ci_anchor
    for t in (1, 7, 21, 60):
        assert a.claim_expenses(t) == pytest.approx(
            300000.0 * (a.pols_ci(t) + a.pols_death(t) + a.pols_death_ci(t)),
            rel=1e-14)
    total = a.result_cf()["claim_expenses"].sum()
    deaths_only = 300000.0 * sum(
        a.pols_death(t) + a.pols_death_ci(t) for t in range(1, a.proj_len() + 1))
    assert total == pytest.approx(TOTALS["claim_expenses"], abs=WON)
    assert 1.0 - deaths_only / total == pytest.approx(
        CLAIM_EXPENSE_UNDERSTATEMENT, abs=5e-3)
    # It is beside the expense line, not inside it.
    assert a.expenses(10) == pytest.approx(
        60000.0 * a.inflation_factor(10) * a.pols_if(10), rel=1e-14)
    assert "claim_expenses" in a.result_cf().columns


def test_pitfall_the_loan_is_floored_and_the_acceleration_is_not_netted(ci_insurance):
    """max(0, . - L) on four payments, and the 선지급 paid gross of the balance.

    Model point 7 is the only point with a loan and draws half the available room at
    duration 12, inside the 납입기간 where the base is the suppressed value.  The
    acceleration is paid gross — no retrieved document says the 선지급 is reduced by the
    balance — so the loan stays outstanding against the residual, which is where it bites.
    """
    p = ci_insurance.Projection[7]
    assert p.pol_loan_util() == 0.5 and p.pol_loan_year() == 12
    assert p.loan_pp(12) == 0.0
    assert p.pol_loan_draw(12) == pytest.approx(0.5 * p.loan_avail_pp(12), rel=1e-14)
    assert p.loan_pp(13) == pytest.approx(p.pol_loan_draw(12) * 1.04, rel=1e-12)
    assert p.check_loan_roll_fwd() is True
    for t in (13, 20, 40):
        assert p.claims(t, "DEATH") == pytest.approx(
            max(0.0, p.base_benefit_pp(t) - p.loan_pp(t)) * p.pols_death(t), rel=1e-12)
        assert p.claims(t, "LAPSE") == pytest.approx(
            max(0.0, p.cv_pp(t) - p.loan_pp(t)) * p.pols_lapse(t), rel=1e-12)
        assert p.claims(t, "LAPSE_CI") == pytest.approx(
            max(0.0, p.cv_pp_ci(t) - p.loan_pp(t)) * p.pols_lapse_ci(t), rel=1e-12)
        assert p.claims(t, "DEATH_CI") >= 0.0
        assert p.claims(t, "LAPSE") >= 0.0
    # The acceleration is not netted: it is the cohort count times the gross benefit.
    for t in (13, 20):
        assert p.claims(t, "CI") == pytest.approx(
            p.pols_ci_in(t, t) * p.accel_benefit_pp(t), rel=1e-14)
        assert p.loan_pp(t) > 0.0
    # A surrender at t = 13 pays the suppressed value net of a loan drawn on it.
    assert p.cv_pp(13) > p.loan_pp(13) > 0.0


def test_pitfall_the_two_decrement_tables_are_not_the_chassis(ci_insurance):
    """omega = 110 here against 115 on the whole life chassis, on different anchors.

    The two files are fitted to different disclosures on different bases, so swapping
    them changes the horizon by five years and the whole mortality level: q(M, 40) is
    0.00068 here, [S3]'s own disclosed CI 예정 경험 사망률, against 0.00085 there.  The
    chassis relationship this product states is about mechanics, not about tables.
    """
    ci_table = pd.read_csv(CSV_DIR / "mort_table.csv")
    chassis = pd.read_csv(CSV_DIR.parent / "whole_life" / "mort_table.csv")
    assert sorted(set(zip(ci_table[ci_table["mort_rate"] >= 1.0]["sex"],
                          ci_table[ci_table["mort_rate"] >= 1.0]["age"]))) == [
        ("F", 110), ("M", 110)]
    assert set(chassis[chassis["mort_rate"] >= 1.0]["age"]) == {115}
    ci_40 = ci_table[(ci_table.sex == "M") & (ci_table.age == 40)]["mort_rate"].iloc[0]
    wl_40 = chassis[(chassis.sex == "M") & (chassis.age == 40)]["mort_rate"].iloc[0]
    assert ci_40 == 0.00068 and wl_40 != ci_40
    assert ci_insurance.Projection[1].omega_age() == 110
    assert ci_insurance.Projection[1].proj_len() == 110 - 40 + 1


# ---------------------------------------------------------------------------
# The product's own identities and boundaries


def test_nine_check_cells_are_published_each_with_its_residual(ci_insurance):
    """Nine identities, asserted **by name**, each with the signed residual beside it.

    That they are *true*, on all nine model points, is asserted in
    ``test_model_conventions_kr.py``, whose sweep discovers every ``check_*``
    generically and calls it on every model point of every model in the library.  Generic
    discovery cannot notice a check that has *gone*: it simply stops being discovered.
    Naming them is the statement left here, and on this product the names matter — four
    of the nine exist only because of the acceleration.
    """
    cells = set(ci_insurance.Projection.cells)
    published = {c for c in cells
                 if c.startswith("check_") and not c.endswith("_resid")}
    assert published == CHECK_CELLS
    for name in published:
        assert name + "_resid" in cells, name
    # The four that are this product's rather than the chassis's.
    assert {"check_ci_state_roll_fwd", "check_accel_complement", "check_resid_floor",
            "check_cv_carve_out"} <= published


def test_the_two_state_roll_forward_closes_on_the_anchor(kr_ci_anchor):
    """The pre-CI cohort loses exactly C + D + S and the post-CI cohort gains exactly C.

    The total roll-forward cannot see a policy that leaves one state without arriving in
    the other, because the two errors cancel in the aggregate.  This is the identity that
    catches it, and it is the one an implementation of an acceleration most needs.
    """
    a = kr_ci_anchor
    assert a.check_ci_state_roll_fwd() is True
    for t in range(1, a.proj_len() + 1):
        pre_out = a.pols_ci(t) + a.pols_death(t) + a.pols_lapse(t)
        assert a.pols_if_pre(t) - a.pols_if_pre(t + 1) == pytest.approx(
            pre_out, abs=1e-12)
        post_in = a.pols_ci(t) - a.pols_death_ci(t) - a.pols_lapse_ci(t)
        assert a.pols_if_ci(t + 1) - a.pols_if_ci(t) == pytest.approx(
            post_in, abs=1e-12)
        assert a.check_ci_state_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_the_cohort_counts_reconstruct_the_post_ci_total(kr_ci_anchor):
    """l1(t) is the sum over cohorts, and every cohort decrements on its own two rates.

    The post-CI cohort is carried by entry year because the residual is a cohort property.
    That decomposition has to be exact, or the aggregate count and the cohort-by-cohort
    benefit calculation are describing different populations.
    """
    a = kr_ci_anchor
    for t in (2, 7, 21, 40):
        assert a.pols_if_ci(t) == pytest.approx(
            sum(a.pols_if_ci_at(t, s) for s in a.ci_cohort_ids(t)), rel=1e-13)
        for s in a.ci_cohort_ids(t):
            if t - 1 >= 1:
                assert a.pols_if_ci_at(t, s) == pytest.approx(
                    a.pols_ci_in(t - 1, s)
                    + a.pols_if_ci_at(t - 1, s) * (1 - a.mort_rate_ci(t - 1))
                    * (1 - a.lapse_rate_ci(t - 1)), rel=1e-13)
    assert a.pols_death_ci(21) == pytest.approx(
        a.pols_if_ci(21) * a.mort_rate_ci(21), rel=1e-14)
    assert a.pols_lapse_ci(21) == pytest.approx(
        a.pols_if_ci(21) * (1 - a.mort_rate_ci(21)) * a.lapse_rate_ci(21), rel=1e-14)


def test_the_acceleration_and_its_residual_sum_to_the_base_benefit(kr_ci_anchor):
    """a B + r B = B and a f B + (1 - a f) B = B, cohort by cohort.

    The one thing in this product that is exact rather than standardized: the
    acceleration never adds cover, it redistributes one sum assured across two dates.
    Holding r as the arithmetic complement rather than as a second model point column is
    what makes the identity unfalsifiable, and this asserts it on the cohorts actually
    formed — so a first-year model point checks both the full and the reduced arithmetic.
    """
    a = kr_ci_anchor
    assert a.check_accel_complement() is True
    assert a.accel_benefit_pp(0) + a.resid_nominal_pp(0) == pytest.approx(
        a.base_benefit_pp(1), rel=1e-14)
    for s in (1, 7, 21, 40):
        assert a.accel_benefit_pp(s) + a.resid_nominal_pp(s) == pytest.approx(
            a.base_benefit_pp(s), rel=1e-14)
        assert a.accel_benefit_pp(s) == pytest.approx(
            0.80 * a.base_benefit_pp(s), rel=1e-14)
    for t in (1, 5, 40):
        assert a.check_accel_complement_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_the_policy_value_rolls_forward_on_the_pricing_basis(kr_ci_anchor):
    """(V(t-1) + P 1{t<=m})(1+i) = the year's expected outgo plus (1-q_ci)(1-q) V(t).

    The prospective closed form and the retrospective recursion are the same object seen
    from two ends, so this catches a mis-set 납입기간, a discount factor applied on the
    wrong side, or a CI decrement present in the benefit and absent from the annuity —
    none of which the prospective formula alone would reveal.  The account runs on its own
    clock: it is a function of t, P, i and the two pricing decrements, and of no policy
    count at all.
    """
    a = kr_ci_anchor
    assert a.check_pol_val_roll_fwd() is True
    for t in (1, 2, 7, 20, 21, 40, a.proj_len()):
        assert a.check_pol_val_roll_fwd_resid(t) == pytest.approx(0.0, abs=1.0)
    assert a.pol_val_pp(0) == 0.0
    assert a.pol_val_pp(a.proj_len()) == 0.0
    # No premium term in the recursion once premiums have stopped.
    qc, qd = a.ci_rate_base(30), a.mort_rate_base(30)
    assert a.pol_val_pp(29) * 1.025 == pytest.approx(
        qc * (0.80 * a.sum_assured() + a.epv_resid(31))
        + (1 - qc) * qd * a.sum_assured()
        + (1 - qc) * (1 - qd) * a.pol_val_pp(30), abs=1.0)
    assert a.pol_val_pp(10) == pytest.approx(
        a.epv_ben(11) - a.prem_net_level_pp() * a.annuity_due(11), rel=1e-14)


def test_the_published_cash_flow_statement_closes(kr_ci_anchor):
    """net_cf equals the eleven published columns of the same row, every year.

    A sixth benefit kind added to ``claims`` and left out of the statement would vanish
    silently without this; it shows up here instead.  The columns are published as five
    ``claims_*`` splits rather than one total precisely so that they must sum.
    """
    a = kr_ci_anchor
    assert a.check_net_cf() is True
    df = a.result_cf()
    outgo = df[["claims_ci", "claims_death", "claims_death_ci", "claims_lapse",
                "claims_lapse_ci", "claim_expenses", "expenses",
                "commissions"]].sum(axis=1)
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-6)
    for t in (1, 21, 60):
        assert a.claims(t) == pytest.approx(
            sum(a.claims(t, k) for k in
                ("CI", "DEATH", "DEATH_CI", "LAPSE", "LAPSE_CI")), rel=1e-12)
        assert a.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-6)


def test_the_result_table_has_the_library_column_vocabulary(kr_ci_anchor):
    """pols_if first, net_cf last, five claims splits and no ``claims`` subtotal column.

    The five-way split is the point of the publication order: a three-column statement
    would hide the whole subject of this model, which is that ``claims_ci`` and
    ``claims_death_ci`` are two payments arising from one decrement at two dates.
    """
    df = kr_ci_anchor.result_cf()
    assert list(df.columns) == list(CF_COLUMNS)
    assert "claims" not in df.columns
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, PROJ_LEN + 1))
    assert df.notna().all().all()
    pols = kr_ci_anchor.result_pols()
    assert list(pols.columns) == [
        "pols_if", "pols_if_pre", "pols_if_ci", "pols_if_pay", "pols_ci",
        "pols_death", "pols_death_ci", "pols_lapse", "pols_lapse_ci",
        "mort_rate", "ci_rate", "lapse_rate"]
    vals = kr_ci_anchor.result_val()
    assert list(vals.columns) == [
        "pol_val_pp", "surr_chg_pp", "cv_std_pp", "cv_pp", "cv_pp_ci",
        "base_benefit_pp", "accel_benefit_pp", "resid_nominal_pp",
        "resid_db_avg_pp", "loan_pp"]


def test_net_cf_carries_the_notes_own_sign(ci_insurance, kr_ci_anchor):
    """Income-positive, so there is no outgo-positive ``liability_cf`` to publish.

    The shape the notes describe: a shallow strain in year 1 that the premium almost
    covers, a long positive stretch while the premium runs, then a negative step at
    납입완료 from which the stream never recovers.
    """
    assert "liability_cf" not in ci_insurance.Projection.cells
    a = kr_ci_anchor
    assert a.net_cf(1) < 0.0
    assert all(a.net_cf(t) > 0.0 for t in range(2, 21))
    assert all(a.net_cf(t) < 0.0 for t in (21, 30, 50, 71))
    assert a.net_cf(2) > 0.0 > a.net_cf(21)


def test_invalid_enum_values_raise(kr_ci_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    a = kr_ci_anchor
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")
    with pytest.raises(FormulaError):
        a.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        a.claims(1, "MATURITY")
    with pytest.raises(FormulaError):
        a.ci_rate_at_age(40, "thyroid")


def test_there_is_no_maturity_benefit_and_no_tail_states(ci_insurance, kr_ci_anchor):
    """종신 means no expiry date and no 만기보험금; the horizon is the table's.

    Only death benefits fall in the final year, and every policy issued has left by one of
    the four exits.  A maturity cells or a maturity kind would be describing a different
    contract.
    """
    a = kr_ci_anchor
    names = set(ci_insurance.Projection.cells) | set(ci_insurance.Projection.refs)
    for absent in ("pols_maturity", "claims_maturity", "policy_term", "maturity_age"):
        assert absent not in names, f"{absent}: this contract does not mature"
    t_end = a.proj_len()
    assert a.claims(t_end) == pytest.approx(a.claims(t_end, "DEATH"), rel=1e-12)
    assert a.claims(t_end, "CI") == 0.0
    assert a.pols_lapse(t_end) == 0.0        # nobody survives to surrender
    assert a.pols_if(t_end + 1) == 0.0


# ---------------------------------------------------------------------------
# Modules that are off in the base run, asserted in both positions


def test_the_policy_loan_is_off_in_the_base_run_and_doubles_at_a_ci_event_when_on(
        ci_insurance, kr_ci_anchor):
    """Identically zero on the anchor; drawn on point 7 at duration 12.

    The draw is placed inside the 납입기간 on purpose, because that is the only
    configuration in which the carve-out's doubling of the limit is visible: the pre-CI
    room is 80% of the suppressed value and the post-CI room 80% of the full one.
    """
    a = kr_ci_anchor
    assert a.pol_loan_util() == 0.0
    assert all(a.pol_loan_draw(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert all(a.loan_pp(t) == 0.0 for t in range(1, a.proj_len() + 2))
    assert a.check_loan_roll_fwd() is True

    p = ci_insurance.Projection[7]
    assert p.loan_avail_pp(12) == pytest.approx(23581915.16, abs=WON)
    assert p.loan_avail_ci_pp(12) == pytest.approx(47163830.33, abs=WON)
    assert p.loan_avail_ci_pp(12) == pytest.approx(
        2.0 * p.loan_avail_pp(12), rel=1e-14)
    assert p.pol_loan_draw(12) == pytest.approx(11790957.58, abs=WON)
    assert all(p.pol_loan_draw(t) == 0.0
               for t in range(1, p.proj_len() + 1) if t != 12)
    for t in range(13, 20):
        assert p.loan_pp(t + 1) == pytest.approx(p.loan_pp(t) * 1.04, rel=1e-12)
    assert p.check_loan_roll_fwd() is True
    assert p.check_pols_roll_fwd() is True     # the loan is a state, not a decrement


def test_the_fifty_percent_acceleration_form_is_a_different_product(ci_insurance):
    """a = 0.50 on points 3 and 8, and the residual floor then bites far later.

    On the 80% form the account has to pass KRW 19,050,000 for the floor to take over the
    KRW 20,000,000 nominal; on the 50% form it must pass KRW 47,600,000, which is one of
    the three reasons the composite takes the 80% fraction.  Both forms are in the shipped
    table, so the asymmetry is exercised rather than described.
    """
    for point_id in (3, 8):
        p = ci_insurance.Projection[point_id]
        assert p.accel_rate() == 0.50
        assert p.resid_rate() == pytest.approx(0.50, abs=1e-15)
        assert p.accel_benefit_pp(1) == pytest.approx(
            p.resid_nominal_pp(1), rel=1e-14)
        assert p.check_accel_complement() is True
        assert p.check_resid_floor() is True
        threshold = 0.50 * p.sum_assured() / 1.05
        crossing = min(t for t in range(1, p.proj_len() + 1)
                       if p.pol_val_pp(t) > threshold)
        assert crossing > 7
    half = ci_insurance.Projection[3]
    assert half.pol_val_pp(7) * 1.05 < 0.50 * half.sum_assured()


def test_the_three_suppression_grades_are_all_exercised(ci_insurance):
    """k = 0.00, 0.50 and 1.00 are all in the shipped table, and k = 0 pays nothing.

    On the 무해지 form the pre-CI surrender value is nil throughout the 납입기간, from
    which the FSS's finding that such a contract cannot support a policy loan at all
    during the payment period follows arithmetically.  The carve-out still holds: the
    post-CI value is the full one at every duration on every grade.
    """
    none_form = ci_insurance.Projection[4]
    assert none_form.cv_floor_ratio() == 0.0
    assert all(none_form.cv_pp(t) == 0.0 for t in range(1, none_form.prem_period()))
    assert all(none_form.loan_avail_pp(t) == 0.0
               for t in range(1, none_form.prem_period()))
    assert none_form.cv_pp_ci(10) > 0.0
    assert none_form.claims(10, "LAPSE") == 0.0
    assert none_form.claims(10, "LAPSE_CI") > 0.0
    assert none_form.cv_pp(none_form.prem_period()) > 0.0     # the step is still there
    assert none_form.check_cv_carve_out() is True

    ordinary = ci_insurance.Projection[3]
    assert ordinary.cv_floor_ratio() == 1.0
    assert {ordinary.cv_mult(t) for t in range(1, ordinary.proj_len() + 1)} == {1.0}
    for t in (2, 10, 19, 20):
        assert ordinary.cv_pp(t) == pytest.approx(ordinary.cv_std_pp(t), rel=1e-14)
        assert ordinary.cv_pp_ci(t) == pytest.approx(ordinary.cv_pp(t), rel=1e-14)
    assert ordinary.check_cv_carve_out() is True

    suppressed = ci_insurance.Projection[1]
    assert suppressed.cv_floor_ratio() == 0.50


def test_the_table_lapse_basis_runs_beside_the_principle_model(ci_insurance,
                                                               kr_ci_anchor):
    """The 표준형 duration curve on points 3, 6 and 8; the 로그-선형 원칙모형 elsewhere.

    Carrying both is the comparison the IFRS17 주요 계리가정 가이드라인 requires an
    insurer to disclose, and it is the reason the table survives on a product whose
    representative form does not use it.  No separate 완납 surrender spike is imposed on
    either basis: the eightfold step on the anchor is the guideline's own shape.
    """
    a = kr_ci_anchor
    assert a.lapse_basis() == "log_linear"
    assert a.lapse_rate(1) == 0.10
    assert a.lapse_rate(a.prem_end()) == pytest.approx(0.001, abs=1e-15)
    assert a.lapse_rate(a.prem_end() + 1) == 0.008
    assert a.lapse_rate_ult() == 0.008
    assert a.lapse_rate_ci(1) == pytest.approx(0.004, rel=1e-14)
    assert all(a.lapse_rate_ci(t) == a.lapse_rate_ci(1) for t in (2, 20, 21, 60))

    p = ci_insurance.Projection[3]
    assert p.lapse_basis() == "table"
    assert [p.lapse_rate(t) for t in (1, 2, 3, 4, 5, 6, 7)] == [
        0.09, 0.07, 0.055, 0.045, 0.038, 0.032, 0.028]
    assert p.lapse_rate(30) == 0.028
    assert p.lapse_rate_ult() == 0.028
    assert p.lapse_rate_ci(1) == pytest.approx(0.014, rel=1e-14)
    # No spike at 납입완료 on the table basis: it is a duration curve and nothing else.
    assert p.lapse_rate(p.prem_end()) == p.lapse_rate(p.prem_end() + 1)
    for point_id in (6, 8):
        assert ci_insurance.Projection[point_id].lapse_basis() == "table"


def test_the_best_estimate_levers_and_the_110_percent_floor(ci_insurance, kr_ci_anchor):
    """The base run is a valuation-basis run; point 9 is where the levers are exercised.

    ``mort_be_factor`` and ``ci_be_factor`` are 1.00 everywhere else, so the shipped
    projection runs on 예정위험률 carrying a 안전할증 nobody has sized against current
    Korean experience.  Point 9 moves both, halves the post-CI mortality multiple towards
    2.00 and runs the 110% residual floor [S3] publishes instead of 105%.
    """
    a = kr_ci_anchor
    assert a.mort_be_factor() == 1.0 and a.ci_be_factor() == 1.0
    for t in (1, 20, 60):
        assert a.mort_rate(t) == pytest.approx(a.mort_rate_base(t), rel=1e-14)
        assert a.ci_rate(t) == pytest.approx(a.ci_rate_base(t), rel=1e-14)

    p = ci_insurance.Projection[9]
    assert p.mort_be_factor() == 0.85 and p.ci_be_factor() == 0.75
    assert p.mort_ci_factor() == 2.0
    assert p.resid_floor_mult() == 1.10
    assert p.waiver_rate(1) == 0.0005
    assert p.mort_rate(1) == pytest.approx(0.85 * p.mort_rate_base(1), rel=1e-14)
    assert p.ci_rate(1) == pytest.approx(0.75 * p.ci_rate_base(1), rel=1e-14)
    assert p.mort_rate_ci(1) == pytest.approx(2.0 * p.mort_rate(1), rel=1e-14)
    # The pricing basis reads the tables straight, so the levers move no reserve.
    assert p.epv_ben(1) == pytest.approx(
        p.disc_factor() * (
            p.ci_rate_base(1) * p.accel_rate() * p.sum_assured()
            + (1 - p.ci_rate_base(1)) * p.mort_rate_base(1) * p.sum_assured()
            + p.ci_rate_base(1) * p.epv_resid(2)
            + (1 - p.ci_rate_base(1)) * (1 - p.mort_rate_base(1)) * p.epv_ben(2)),
        rel=1e-12)
    # The terminal rate is structural and survives every lever.
    assert p.mort_rate(p.proj_len()) == 1.0
    assert p.resid_db_pp(30, 1) == pytest.approx(1.10 * p.pol_val_pp(30), rel=1e-14)
    assert p.check_resid_floor() is True


def test_the_waiver_runs_on_every_shipped_point_and_is_not_a_module(ci_insurance):
    """0.03% p.a. inside the 납입기간 on eight points and 0.05% on the ninth, never nil.

    On this product the 납입면제 is part of the main contract rather than an option, so
    it is deliberately not in the list of switchable modules.  What is modelled is the
    residual 장해 50%+ limb only: the CI limb fires with essentially every CI claim and is
    already inside the post-CI cohort, which pays nothing at all.
    """
    for point_id in ci_insurance.Data.model_point_table().index:
        p = ci_insurance.Projection[point_id]
        assert p.waiver_rate(1) > 0.0
        assert p.waiver_rate(p.prem_end()) > 0.0
        assert p.waiver_rate(p.prem_end() + 1) == 0.0
        assert p.waiver_rate(0) == 0.0
    a = ci_insurance.Projection[1]
    assert a.pols_waived(1) == 0.0
    assert a.pols_waived(2) > 0.0
    # A waived policy stays pre-CI and inside the surrender-value machinery.
    assert a.pols_waived(10) < a.pols_if_pre(10)
    assert a.pols_if_pay(10) == pytest.approx(
        a.pols_if_pre(10) - a.pols_waived(10), rel=1e-14)
    assert a.pols_if_pay(a.prem_end() + 1) == 0.0


# ---------------------------------------------------------------------------
# The [std] assumptions, read off the model


def test_the_std_scalar_assumptions_are_the_ones_the_notes_state(ci_insurance):
    """Every [std] scalar the notes and ``model.md`` tabulate, read off the References.

    These are not derived quantities: they are the choices the reference implementation
    makes where Korea publishes nothing, and each one is listed with a rationale in
    ``model.md`` under *Standardizations used*.  Asserting them here means a silent change
    to an assumption fails a test rather than quietly moving a result somewhere else in
    this module.
    """
    proj = ci_insurance.Projection
    assert proj.prem_int_rate == 0.025           # 예정이율, the chassis's
    assert proj.i_loan == 0.04                   # 예정이율 + 1.5%
    assert proj.loan_cap_rate == 0.8             # of the payable value [REG-R25 제33조]
    assert proj.net_prem_ratio == 0.8            # 연납순보험료 entering 별표 14
    assert proj.surr_chg_rate == 0.05            # 별표 14's 5%
    assert proj.surr_chg_coef_cap == 20          # the 해약공제계수 cap for 보장성
    assert proj.surr_chg_sa_rate == 0.01         # 10/1000 of the 보험가입금액
    assert proj.surr_chg_years_cap == 7          # 해약공제기간 [REG-R19]
    assert proj.ci_cover_end_age == 100          # the 100세 계약해당일
    assert proj.ci_wait_days == 90               # the 보장개시일, sourced four times
    assert proj.first_year_factor == 0.5         # the first-year 감액
    assert proj.breast_share_m == 0.005
    assert proj.breast_share_f == 0.268
    assert proj.lapse_ll_first == 0.1            # the 원칙모형's [std] start
    assert proj.lapse_ll_target == 0.001         # its supervisory endpoint
    assert proj.lapse_post_paidup == 0.008       # its post-완납 ultimate
    assert proj.lapse_ci_factor == 0.5
    assert proj.expense_acq == 500000.0
    assert proj.expense_maint == 60000.0
    assert proj.expense_claim == 300000.0
    assert proj.inflation_rate == 0.01
    assert proj.comm_init_rate == 0.8
    assert proj.comm_renewal_rate == 0.03
    assert proj.roll_fwd_tol == 1e-10
    assert proj.val_tol == 1e-08


def test_expense_inflation_compounds_over_the_whole_horizon(kr_ci_anchor):
    """1% compounds to 2.01 over 71 years, which is why the rate is not a Western one.

    Over a horizon this long the inflation assumption is not a second-order adjustment: a
    3% rate would compound to 7.9 and produce a different product rather than a stressed
    one.  There is no published Korean expense basis to anchor either figure.
    """
    a = kr_ci_anchor
    assert a.inflation_factor(1) == 1.0
    assert a.inflation_factor(a.proj_len()) == pytest.approx(1.01 ** 70, rel=1e-14)
    assert a.inflation_factor(a.proj_len()) == pytest.approx(INFLATION_TOTAL, abs=5e-3)
    assert 1.03 ** 70 == pytest.approx(7.92, abs=5e-3)


@pytest.mark.parametrize("name,setter,expected", [
    ("ci_wait_days", "ci_wait_days", SENS_NO_WAIT),
    ("first_year_factor", "first_year_factor", SENS_NO_FIRST_YEAR_CUT),
    ("lapse_ci_factor", "lapse_ci_factor", SENS_FULL_POST_CI_LAPSE),
])
def test_the_sensitivities_the_notes_quantify(name, setter, expected):
    """Three levers moved one at a time, against the notes' own figures.

    The notes quantify each of these in *Key sensitivities* and the numbers are what
    justify the treatment: the 90-day wait is worth 0.05% of the liability, so its
    *level* is immaterial while its mechanism is not; the first-year 감액 is worth
    KRW 149.44 on a male cell and is material only on a female one; and doubling post-CI
    lapse moves the whole liability by 0.6%, so the level does not matter much in
    aggregate while the sign of the behavioural story does.
    """
    values = {"ci_wait_days": 0, "first_year_factor": 1.0, "lapse_ci_factor": 1.0}
    model = mx.read_model(MODEL_DIR, name="CI_KR_A_sens_" + name)
    try:
        setattr(model.Projection, setter, values[setter])
        model.Projection.clear_all()
        total = model.Projection[1].result_cf()["net_cf"].sum()
        assert total == pytest.approx(expected, abs=0.02)
        assert total != pytest.approx(TOTALS["net_cf"], abs=1.0)
    finally:
        model.close()


def test_the_lapse_vector_is_a_third_of_the_liability():
    """A level 4% paying-period rate moves sum net_cf from -51.3m to -34.1m.

    Lapse is not a second-order assumption on this product: it removes lives before the
    acceleration reaches them, so a third of the whole undiscounted liability rests on a
    vector whose two endpoints are supervisory and whose interpolation is [std].  The
    comparison holds the 0.8% post-완납 ultimate fixed and moves only the paying-period
    shape, which is the part the guideline's functional form governs.
    """
    model = mx.read_model(MODEL_DIR, name="CI_KR_A_level_lapse")
    try:
        model.Projection.lapse_ll_first = 0.04
        model.Projection.lapse_ll_target = 0.04
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.lapse_rate(1) == 0.04 and p.lapse_rate(20) == 0.04
        assert p.lapse_rate(21) == 0.008          # the ultimate is untouched
        assert p.result_cf()["net_cf"].sum() == pytest.approx(
            SENS_LEVEL_4_PCT_LAPSE, abs=0.02)
        assert p.check_pols_roll_fwd() is True
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Inputs


def test_inputs_live_beside_the_model():
    """The four input CSVs sit in the model folder's parent directory."""
    expected = {"model_point_table.csv", "mort_table.csv", "ci_incidence_table.csv",
                "lapse_table.csv"}
    assert expected == {p.name for p in CSV_DIR.iterdir() if p.suffix == ".csv"}


def test_the_csvs_are_utf8_without_a_bom():
    """The provenance columns are Korean, so the encoding is load-bearing."""
    for name in ("model_point_table.csv", "mort_table.csv", "ci_incidence_table.csv",
                 "lapse_table.csv"):
        raw = (CSV_DIR / name).read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"{name} carries a BOM"
        raw.decode("utf-8")


def test_the_shipped_mortality_table_marks_its_own_provenance():
    """Four [S3] anchor rows and 188 rows of Makeham and ramp, each tagged.

    Korea publishes no life table this model could ship: 보험개발원 releases only 평균수명
    and 기대여명 from the 경험생명표.  So the file is a construction, and marking the rows
    is what stops it being mistaken for a published table.  The four anchors are the whole
    documentary basis of the mortality in this product.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith(("[S3]", "[std]")).all()

    anchors = table[table["provenance"].str.startswith("[S3]")]
    assert len(anchors) == 4
    assert sorted(zip(anchors["sex"], anchors["age"])) == [
        ("F", 20), ("M", 20), ("M", 40), ("M", 60)]
    assert anchors["provenance"].str.contains("ANCHOR").all()
    assert list(anchors[anchors["sex"] == "M"]["mort_rate"]) == [
        0.00051, 0.00068, 0.00290]
    assert list(anchors[anchors["sex"] == "F"]["mort_rate"]) == [0.00027]

    constructed = table[table["provenance"].str.startswith("[std]")]
    assert len(constructed) == len(table) - 4
    assert constructed["provenance"].str.contains(
        "Makeham|log-linear|0.5294|terminal age", regex=True).all()
    assert constructed["provenance"].str.contains("terminal age").sum() == 2
    assert table["age"].min() == 15 and table["age"].max() == OMEGA
    assert (table["sex"] == "M").sum() == (table["sex"] == "F").sum() == 96
    terminal = table[table["mort_rate"] >= 1.0]
    assert sorted(zip(terminal["sex"], terminal["age"])) == [("F", 110), ("M", 110)]
    # The female table is the male one scaled, which the notes name as a known defect.
    male = table[table["sex"] == "M"].set_index("age")["mort_rate"]
    female = table[table["sex"] == "F"].set_index("age")["mort_rate"]
    assert (female.loc[30] / male.loc[30]) == pytest.approx(0.5294, abs=5e-4)


def test_the_shipped_incidence_table_marks_its_own_provenance():
    """Eighteen [S3] anchors across three causes and two sexes; everything else [std].

    ``other`` and ``ltc`` have no anchor rows at all, which is the file's own statement
    that they are constructions: the first a flat 10.5% of the three headline rates, the
    second a placeholder above age 65.  The 참조순보험요율 carries no CI item, so this and
    the four mortality anchors are the entire published Korean basis for this product.
    """
    table = pd.read_csv(CSV_DIR / "ci_incidence_table.csv")
    assert list(table.columns) == ["sex", "age", "cause", "ci_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith(("[S3]", "[std]")).all()
    assert sorted(table["cause"].unique()) == sorted(CAUSE_ORDER)
    assert table["age"].min() == 15 and table["age"].max() == 100

    anchors = table[table["provenance"].str.startswith("[S3]")]
    assert len(anchors) == 18
    assert sorted(anchors["age"].unique()) == [20, 40, 60]
    assert sorted(anchors["cause"].unique()) == ["ami", "cancer", "stroke"]
    assert anchors["provenance"].str.contains("ANCHOR").all()
    assert set(anchors["sex"]) == {"M", "F"}

    for cause in ("other", "ltc"):
        rows = table[table["cause"] == cause]
        assert rows["provenance"].str.startswith("[std]").all(), cause
    # The ltc limb is nil below 65 and the largest single limb at the top of the grid.
    ltc = table[(table["cause"] == "ltc") & (table["sex"] == "M")].set_index("age")
    assert (ltc.loc[15:64, "ci_rate"] == 0.0).all()
    assert ltc.loc[65, "ci_rate"] > 0.0
    assert ltc.loc[100, "ci_rate"] > ltc.loc[65, "ci_rate"]


def test_the_lapse_table_is_the_comparison_curve_and_holds_no_spike():
    """Six duration rows and a level tail, all [std], with no 완납 surge folded in.

    The surge at 납입완료 on the suppressed forms is produced by the 원칙모형's own shape
    and is not a row of this table; folding it in would make a behavioural assumption look
    like a duration curve, and would put it on the 기본환급형 points too, where the
    contract has no step to provoke it.
    """
    table = pd.read_csv(CSV_DIR / "lapse_table.csv", index_col="policy_year")
    assert list(table.columns) == ["lapse_rate", "provenance"]
    assert list(table["lapse_rate"]) == [0.09, 0.07, 0.055, 0.045, 0.038, 0.032, 0.028]
    assert table["provenance"].notna().all()
    assert table["provenance"].str.startswith("[std]").all()
    assert table["lapse_rate"].max() < 0.10
    assert table["lapse_rate"].is_monotonic_decreasing
    columns = pd.read_csv(CSV_DIR / "model_point_table.csv").columns
    assert "lapse_spike" not in columns
    assert "lapse_basis" in columns


def test_the_model_point_table_covers_both_sexes_and_every_module():
    """Nine points: both sexes, the age and sum-assured envelopes, every switch moved.

    A model point table that exercised only the anchor's configuration would leave the
    optional machinery untested in the one position that matters, and this product has
    six switches — the acceleration fraction, the suppression grade, the first-year scope,
    the lapse basis, the residual floor multiple and the loan.
    """
    table = pd.read_csv(CSV_DIR / "model_point_table.csv", index_col="point_id")
    assert len(table) == 9
    assert list(table.index) == list(range(1, 10))
    assert set(table["sex"]) == {"M", "F"}
    assert table["issue_age"].min() == 15 and table["issue_age"].max() == 60
    assert table["sum_assured"].min() == 10000000
    assert table["sum_assured"].max() == 200000000
    assert set(table["prem_term"]) == {10, 20, 30}
    assert set(table["accel_rate"]) == {0.5, 0.8}
    assert set(table["cv_floor_ratio"]) == {0.0, 0.5, 1.0}
    assert set(table["first_year_scope"]) == {"breast", "all"}
    assert set(table["lapse_basis"]) == {"log_linear", "table"}
    assert set(table["resid_floor_mult"]) == {1.05, 1.1}
    assert set(table["mort_ci_factor"]) == {2.0, 3.0}
    assert (table["pols_if_init"] == 1).all()
    assert (table.loc[table["pol_loan_util"] > 0].index == [7]).all()
    assert "provenance" not in table.columns     # a configuration, not an assumption


def test_the_model_point_premiums_follow_the_documented_rule(ci_insurance):
    """The anchor's premium is sourced; the other eight are the anchor's loading applied.

    ``model.md`` states the rule under *Standardizations*: each non-anchor cell is this
    model's own net level premium grossed up by the anchor's 1.2399868 loading, times the
    published form factor — 1.10224 for the 기본환급형, 1.000 for the 저해지 and 0.937
    [std] for the 무해지.  Without this test a premium typed into the CSV by hand moves
    every cash flow on that point and nothing in the suite notices.  The band is three
    parts in ten thousand, which bounds the arithmetic that produced the file; a hand
    edit is a percentage-level move and fails wide.
    """
    anchor = ci_insurance.Projection[1]
    loading = anchor.premium_pp() / anchor.prem_net_level_pp()
    assert loading == pytest.approx(LOADING, abs=5e-11)
    assert anchor.premium_pp() == 12 * 306740.0        # the one sourced premium [S4]

    form_factor = {0.0: 0.937, 0.5: 1.000, 1.0: 1.10224}
    for point_id in ci_insurance.Data.model_point_table().index:
        p = ci_insurance.Projection[point_id]
        expected = loading * form_factor[p.cv_floor_ratio()] * p.prem_net_level_pp()
        assert p.premium_pp() == pytest.approx(expected, rel=3e-4), point_id
    assert ci_insurance.Projection[3].premium_pp() == pytest.approx(
        loading * 1.10224 * ci_insurance.Projection[3].prem_net_level_pp(), rel=1e-5)


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """Point a filename Reference at a same-schema file and the projection follows.

    This is the property the external-file layout buys, and it is exactly what a user
    holding a real 예정위험률 grid does with it: drop it in as a CSV, change no formula.
    Doubling the incidence table doubles the year-one acceleration outgo, because the
    first year's claims are linear in the rate.
    """
    src = CSV_DIR / "ci_incidence_table.csv"
    doubled = pd.read_csv(src, index_col=["sex", "age", "cause"])
    doubled["ci_rate"] = (doubled["ci_rate"] * 2).clip(upper=1.0)

    model = mx.read_model(MODEL_DIR, name="CI_KR_A_swap")
    try:
        alt_name = "ci_incidence_doubled.csv"
        doubled.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].pols_ci(1)
            model.Data.ci_incidence_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].pols_ci(1) == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Docstrings and the round trip


def test_the_docstrings_describe_the_current_structure(ci_insurance):
    """Specifics a reader relies on, asserted so they cannot go stale silently."""
    doc = flat(ci_insurance.doc)
    assert "mechanics demonstration" in doc or "demonstrate is the acceleration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "two payments at two dates on one sum assured" in doc
    assert "Data" in doc and "Projection" in doc

    proj = flat(ci_insurance.Projection.doc)
    assert "Notes symbol" in proj                # the symbol-to-cells mapping table
    assert "보험나이" in proj                     # the age basis, per the registry
    for cells in ("proj_len", "model_point", "pols_if_ci_at", "resid_db_pp",
                  "cv_pp_ci", "accel_benefit_pp", "annuity_due", "ci_cover_end"):
        assert cells in proj, cells
    assert "transition" in proj and "never adds cover" in proj
    assert "two exits" in proj

    data = flat(ci_insurance.Data.doc)
    assert "TradLife_A" in data                  # the layout it follows
    for cells in ("input_dir", "model_point_table", "mort_table",
                  "ci_incidence_table", "lapse_table"):
        assert cells in data, cells


def test_the_projection_docstring_describes_the_shipped_model_points(ci_insurance):
    """The module summary must match the model point table it describes.

    A docstring that names a module the table does not exercise is worse than none: it is
    the one place a reader looks to find out what the shipped points cover.
    """
    proj = flat(ci_insurance.Projection.doc)
    table = ci_insurance.Data.model_point_table()
    assert "model point 7 at duration 12" in proj
    assert int(table.loc[7, "pol_loan_year"]) == 12
    assert float(table.loc[7, "pol_loan_util"]) == 0.5
    assert "model point 4" in proj
    assert table.loc[4, "first_year_scope"] == "all"
    assert "model point 9" in proj
    assert float(table.loc[9, "resid_floor_mult"]) == 1.1


def test_the_notes_and_the_model_agree_on_the_worked_example_cell():
    """The technical notes print the anchor's own numbers, not a spreadsheet's.

    Three figures are spot-checked in the notes' own text — the net cash flow total, the
    post-CI death benefit total and the 표준해약공제액 — because the worked example is
    only worth having if the document and the model cannot drift apart.  The whole table
    is asserted cell by cell above; this asserts that the *document* carries it.
    """
    notes = io.open(CSV_DIR / "technical-notes.md", encoding="utf-8").read()
    assert "−₩51,285,700.32" in notes
    assert "36,441,532.16" in notes
    assert "₩3,944,704" in notes
    assert "15.1228758581" in notes
    assert "0.4330002802" in notes


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    model = mx.read_model(MODEL_DIR, name="CI_KR_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    # Inputs are external, so they must travel with the model.
    for csv in CSV_DIR.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="CI_KR_A_rt")
    try:
        anchor = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert anchor.pols_if(t) == pytest.approx(row[0], abs=INFORCE)
            assert anchor.claims(t, "CI") == pytest.approx(row[2], abs=WON)
            assert anchor.net_cf(t) == pytest.approx(row[10], abs=WON)
        assert anchor.cv_pp(20) == pytest.approx(
            WORKED_EXAMPLE_VALUES[20][3], abs=WON)
        assert anchor.prem_net_level_pp() == pytest.approx(P_NET, abs=WON)
        assert "Notes symbol" in reread.Projection.doc
        assert {c for c in reread.Projection.cells
                if c.startswith("check_") and not c.endswith("_resid")} == CHECK_CELLS
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
