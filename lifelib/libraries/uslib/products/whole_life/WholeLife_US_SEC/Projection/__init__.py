# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WholeLife_US_SEC` model.

The Space is parameterized by ``point_id``, so ``Projection[19]`` is an ItemSpace
projecting model point 19, the loan variant in force 114 months at the valuation date::

    >>> Projection[19].result_cf()         # one row per month from the valuation date
    >>> Projection[19].result_pols()       # the counts behind it
    >>> Projection.point_id = 2            # or switch the default

This is :mod:`~.WholeLife_US_S` taught to run in force at a valuation date, as lifelib's
``basiclife.BasicTerm_SE`` extends ``basiclife.BasicTerm_S``. A formula of
:mod:`~.WholeLife_US_S` is rewritten where it depends on where the projection starts,
where it must answer for a month outside cover, or where it passed a policy month as
``t``; every other is :mod:`~.WholeLife_US_S`'s own. ``products/whole_life/model-sec.md``
lists the rewritten cells with the reason for each.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent
directory, ``products/whole_life/``, read at run time rather than stored inside the
model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an
input can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``WholeLife_US_SEC`` folder without its parent's CSVs produces a model that reads and
then fails on first evaluation.

Each table has a filename Reference and a reader Cells, both on the ``Data`` Space,
reached here through the ``data`` Reference. The five assumption tables are the files
:mod:`~.WholeLife_US_S` reads, read in place; the model point table is this model's own:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table_sec.csv
cv_file                 data.cv_table()                 cv_table.csv
nsp_file                data.nsp_table()                nsp_table.csv
np_guar_file            data.np_guar_table()            np_guar_table.csv
mort_table_file         data.mort_table()               mort_table.csv
premium_rates_file      data.premium_rates()            premium_rates.csv
======================  ==============================  ==========================

.. rubric:: Two clocks

``t`` counts months from the **valuation date**, 0-based, the clock
``basiclife.BasicTerm_SE`` runs on: ``t = 0`` is the valuation month for every model
point, however old the policy, period ``t`` runs from time ``t`` to time ``t + 1``, and
the frame is ``t = 0 .. proj_len() - 1``, where :func:`proj_len` counts the months from
the valuation date to maturity at attained age 100. Row ``t`` is the same month for every
point, so the frames of a block line up and sum row by row.

``duration_mth(t)`` counts **policy months**, the months the policy has been in force at
time ``t``: ``duration_mth(t) = duration_mth_init() + t``, where
:func:`duration_mth_init` is read from the model point — positive for a policy in force
at the valuation date, in any month of its policy year, 0 for one issued at it, ``-k``
for one issued ``k`` months later, at most ten years later. It is the technical notes'
month index, and everything contractual about this product reads it, all of it on an
**annual** cycle: the guaranteed cash value schedule, the dividend declaration, the
anniversary capitalization of loan interest, the premium-paying period. The policy year
is therefore derived and used as a lookup key throughout — ``duration(t) =
duration_mth(t) // 12`` is the completed policy years at the start of month ``t``,
``policy_year(t) = duration(t) + 1`` is the contractual 1-based label (the
``policy_year`` key of *cv_table.csv*), ``age(t) = age_at_entry() + duration(t)`` is the
attained age entering that policy year and ``age_anniv(t)`` the age at the anniversary
that ends it. ``is_anniv(t)`` is true in the **last month of a policy year**, which is
where every annual event lands, and :func:`anniv_mth` is the valuation month of that
anniversary. The anchor cell, in force 108 months, is in policy year 10 at attained age
54 at ``t = 0`` and reaches its tenth anniversary at ``t = 11``; the loan variant in
force 114 months pays its next premium at ``t = 6``.

One input reads the valuation clock instead: expense inflation,
``inflation_factor(t) = (1 + inflation_rate) ** (t / 12)``, so that the maintenance
charge is in valuation-date dollars for every point alike. Acquisition is charged per
policy issued, in the issue month, and is not inflated, as in ``basiclife.BasicTerm_SE``.

On a point issued at ``t = 0`` the two clocks coincide and this model computes what
:mod:`~.WholeLife_US_S` computes: every cell the two share agrees at every argument
:mod:`~.WholeLife_US_S` evaluates in its sweep, but for three whose meaning changed,
``pols_if_init``, now the count already in force at the valuation date, ``model_point``,
a row of another table, and ``result_pols``, which gains the month's new business. That
is how :mod:`~.WholeLife_US_S`'s goldens on its new-business points carry over, and
``tests/test_model_conventions.py`` asserts it cell by cell. On a point in force the
projection is :mod:`~.WholeLife_US_S`'s from the month the point is valued at, month for
month, its expenses apart, which are in valuation-date dollars. That is how the worked
example carries over: it sits on :mod:`~.WholeLife_US_S`'s point 1, in force at its
month 108, and the twin of that point is :mod:`~.WholeLife_US_S`'s projection from month
108 on, which ``tests/test_whole_life_us_sec.py`` asserts.

The **value** state variables are closing balances at the end of month ``t``:
``cv_pp(t)``, ``pua_face(t)``, ``pua_cv(t)``, ``div_accum(t)`` and ``loan_bal(t)``. The
value entering month ``t`` is the closing balance of month ``t - 1``, or, at
:func:`t_entry`, the first month on the books, the model point's opening state — written
inline as ``pua_face(t - 1) if t > t_entry() else pua_face_init()`` wherever an opening
balance is read, so that nothing is ever asked for a month before the valuation date or
before issue. For a point in force the opening state is seven columns of its row, per
policy, as the policy stands at the start of month 0: the paid-up additions, the loan and
the accumulation balance entering month 0 (:func:`pua_face_init`, :func:`loan_bal_init`,
:func:`div_accum_init`), the paid-up additions and the loan at the anniversary that
opened the policy year under way (:func:`pua_face_prev_anniv_init`,
:func:`loan_bal_prev_anniv_init`), the dividend credited there
(:func:`div_prev_anniv_init`), and the gross premium paid to date
(:func:`prem_cum_init`). For a point issued at or after the valuation date every one of
them is 0, the values at issue. Annual quantities read the balance entering the
**policy year** instead, twelve months back, or the opening state's anniversary values
where that month is before :func:`t_entry`.

.. rubric:: Counts

``pols_if(t)`` is the count that weights row ``t``: ``pols_if_at(t, "BEF_DECR")``, the
count carried in from ``t - 1`` (``"BEF_NB"``) plus the month's new business,
:func:`pols_new_biz`, before the month's decrements. A point in force at the valuation
date opens with :func:`pols_if_init`, its ``policy_count``; one issued at or after the
valuation date opens with none, and takes its ``policy_count`` as new business in its
issue month. The recursion's base is :func:`t_entry`, and nothing is counted outside
cover (:func:`is_active`): before issue every count, and so every cash flow, is zero,
and so is every value state and every dividend. Inside the month the decrements are
:mod:`~.WholeLife_US_S`'s, in the notes' order, and ``pols_if_at`` names the count
between each: ``"BEF_SURR"`` after deaths, ``"BEF_MAT"`` after surrenders and
``"AFT_DECR"`` after the maturities of the last covered month.

.. rubric:: What the monthly grid changes, and what it does not

Decrements run in two speeds, the library's convention: ``mort_rate(t)`` and
``lapse_rate(t)`` are the **annual** rates of the policy year containing month ``t`` —
the vectors the technical notes tabulate — and ``mort_rate_mth(t)`` and
``lapse_rate_mth(t)`` are the monthly rates actually applied, ``1 - (1 - q)^(1/12)``.
Twelve of those compound back to exactly the annual rate, so **the in-force at every
policy anniversary is what an annual-step model would carry**, to floating-point.

The annual events stay annual and land on ``is_anniv(t)``: the dividend is declared and
credited once a year, at the anniversary; loan interest capitalizes there; paid-up
additions are bought with the dividend there. What the finer grid buys is everything
that is *not* contractually annual — death claims settle at the end of the month of
death rather than the end of the policy year, maintenance expense accrues monthly, the
guaranteed cash value and the paid-up-additions cash value interpolate between
anniversaries so a mid-year surrender is valued where it happens, and a **modal premium
is collected when it is contractually due**. That last one is why the technical notes'
"premium mode modeled: annual" **[std]** is retired: the modal factors are sourced
([S1] for the participating design, [S7] for final expense) and the monthly grid is
what makes them expressible. ``result_cf_annual()`` sums the frame into policy years so
a monthly run can be laid beside an annual one.

Two interpolations are standardizations introduced here, both **[std]** and both exact
at the anniversary so that no anniversary quantity moves:

``cv_pp(t)``
    Straight-line between the schedule's anniversary values, ``(k + 1) / 12`` of the
    way from the value at the anniversary opening the policy year to the value at the
    one closing it, ``k = duration_mth(t) % 12``. Contractual cash value tables are
    printed at anniversaries only [unverified]; pro-rating for elapsed time is the
    ordinary policy-form convention and the Standard Nonforfeiture Law requires *some*
    adjustment for it.
``nsp_mth(t)``
    The same straight line applied to the net single premium between ``NSP_{x+dur}``
    and ``NSP_{x+dur+1}``, so the paid-up-additions block is valued on the same clock
    as the base cash value.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns
for cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts,
``claim_pp(t, kind)`` and ``pols_if_at(t, timing)`` for the argument-keyed families.
What running in force adds is named as ``basiclife.BasicTerm_SE`` names it:
``duration_mth`` read from the model point, ``policy_count``, ``pols_new_biz``,
``pols_if_at`` with its ``"BEF_NB"`` timing, ``is_active`` and ``result_pols``.
``duration_mth_init``, the policy months completed at the valuation date, takes
``UL_US_S``'s name. A column of the opening state measured entering month 0 is the cell
it opens with ``_init`` added, ``pua_face_init`` for :func:`pua_face`, and so is
``div_prev_anniv_init``, which :func:`div_prev_anniv` returns through the policy year
under way; a balance measured at the anniversary on or before the valuation date adds
``_prev_anniv_init`` instead, ``pua_face_prev_anniv_init``. ``t_entry`` and
``maturity_mth`` are this model's own. The technical notes use compact actuarial symbols
instead. The notes' month index is this model's ``duration_mth(t)``. The mapping is:

=========================  ============================  ===================================
Notes symbol               Cells                         Meaning
=========================  ============================  ===================================
x                          age_at_entry                  Issue age (ANB)
x + dur                    age(t)                        Attained age entering the
                                                         policy year of month t
x + dur + 1                age_anniv(t)                  Attained age at the
                                                         anniversary ending it
(none)                     policy_count                  Policies the model point stands for
(none)                     duration_mth_init             Completed policy months at the
                                                         valuation date; -k if issued k
                                                         months later
t                          duration_mth(t)               The notes' month index: completed
                                                         policy months at month t
(t // 12)                  duration(t)                   Completed policy years
dur(t)                     policy_year(t)                Policy year, duration(t) + 1
T = 12(100 - x)            maturity_mth                  Policy month at which cover ends
(frame)                    proj_len                      Months from the valuation date to
                                                         maturity; the frame ends at
                                                         proj_len - 1
(none)                     t_entry                       First month on the books
(none)                     is_active(t)                  Whether month t is inside cover
(anniversary)              is_anniv(t)                   Last month of a policy year
(anniversary month)        anniv_mth(t)                  Valuation month of the anniversary
                                                         ending the policy year of t
m                          policy_term                   Premium-paying period, years
F                          sum_assured                   Base face amount
G                          premium_pp_ann(t)             Gross **annual** premium
(modal)                    premium_pp(t)                 Premium due in month t
(modal factor)             modal_factor                  Fraction of G per instalment
(modal cycle)              prem_cycle                    Months between instalments
(due month)                prem_due(t)                   Whether an instalment is due
G^net_t                    premium_net_pp_ann(t)         Annual premium after offset
(modal)                    premium_net_pp(t)             The instalment actually collected
A_t                        rider_premium_pp_ann(t)       PUA rider premium, annual
(modal)                    rider_premium_pp(t)           The instalment due in month t
i_g                        int_rate_guar                 Guarantee interest, 4.00%
i_d                        int_rate_div                  Dividend interest rate, 6.00%
i_L                        int_rate_loan                 Policy loan rate, 6.00%
q^g_{x+t}                  mort_rate_guar(t)             Guarantee mortality, annual
q^g_y                      mort_rate_guar_at(y)          The same, keyed by age
q^sc_{x+t}                 mort_rate_scale(t)            Dividend-scale mortality
q^e_{x+t}                  mort_rate(t)                  Best-estimate mortality, annual
(q^e monthly)              mort_rate_mth(t)              The monthly rate applied
w_t                        lapse_rate(t)                 Surrender rate, annual
(w monthly)                lapse_rate_mth(t)             The monthly rate applied
w^dyn multiplier           dyn_lapse_factor(t)           Interest-sensitive overlay
l_t                        pols_if(t)                    In force weighting month t: after
                                                         new business, before decrements
l_{t+1}                    pols_if_at(t, "AFT_DECR")     In force at EOM t
l_t(1-q^e)                 pols_if_at(t, timing)         In force inside month t, BEF_NB
                                                         to AFT_DECR
(none)                     pols_if_init                  In force at the valuation date
(none)                     pols_new_biz(t)               Policies issued in month t
(none)                     pols_death(t)                 Deaths in month t
(none)                     pols_lapse(t)                 Surrenders at EOM t
(none)                     pols_maturity(t)              Maturities in the last covered
                                                         month
CV_t                       cv_pp(t)                      Guaranteed cash value, EOM t
CV at anniversary          cv_pp_anniv(y)                The schedule's own values
F - CV_t                   net_amt_at_risk(t)            Guarantee net amount at risk
NSP_y                      nsp(y)                        Net single premium, endow 100
(NSP monthly)              nsp_mth(t)                    NSP interpolated to EOM t
NP_g                       np_guar()                     Nonforfeiture net level premium
D^int_t                    div_int(t)                    Interest margin
D^mort_t                   div_mort(t)                   Mortality margin
D^exp_t (e^m_t)            div_exp(t)                    Expense margin
D_t                        div_base(t)                   Base-block dividend, floored
D^PUA_t                    div_pua(t)                    PUA-block dividend
D_t + D^PUA_t              div_credited(t)               Dividend credited at EOM t
D_{t-1}                    div_prev_anniv(t)             Dividend at the anniversary
                                                         opening the policy year of t
D^cash_t                   div_cash(t)                   Cash dividend per policy
(none)                     div_to_pua(t)                 Dividend applied to PUAs
dPUAF_t                    pua_face_purch(t)             PUA face bought by dividend
dPUAF^rider_t              pua_face_rider(t)             PUA face bought by the rider
(none)                     pua_face_offset(t)            PUA face from the RPD excess
PUAF_t                     pua_face(t)                   PUA face in force at EOM t
PUACV_t                    pua_cv(t)                     PUA cash value at EOM t
DA_t                       div_accum(t)                  Dividend accumulation balance
L_t                        loan_bal(t)                   Loan balance at EOM t
(none)                     loan_int(t)                   Loan interest capitalized
(none)                     loan_draw(t)                  Net new borrowing per policy
(opening PUAF)             pua_face_init                 PUA face entering month 0
(PUAF at anniversary)      pua_face_prev_anniv_init      PUA face at the anniversary
                                                         opening the year of month 0
(opening L)                loan_bal_init                 Loan balance entering month 0
(L at anniversary)         loan_bal_prev_anniv_init      Loan balance at the anniversary
                                                         opening the year of month 0
(opening DA)               div_accum_init                Accumulation balance entering
                                                         month 0
(D_{t-1} at month 0)       div_prev_anniv_init           Dividend at the anniversary
                                                         opening the year of month 0
(none)                     prem_cum_init                 Gross premium paid before the
                                                         valuation date
TF                         term_blend_target             Term-blend target face
OYT_t                      oyt_face(t)                   One-year-term face in the blend
(none)                     oyt_cost(t)                   Dividend absorbed by the OYT
DB_t                       claim_pp(t, "DEATH")          Death benefit per policy
CSV_t                      claim_pp(t, "LAPSE")          Surrender value per policy
MAT                        claim_pp(t, "MATURITY")       Maturity benefit per policy
(none)                     prem_cum(t)                   Cumulative premiums paid
E_t                        expenses(t)                   Acquisition + maintenance
1.02^(t/12)                inflation_factor(t)           Expense inflation, valuation clock
(none)                     premium_taxes(t)              Premium tax outgo
(none)                     premiums(t)                   Premium income
(none)                     rider_premiums(t)             PUA rider premium income
(none)                     claims(t, kind)               Benefit outgo
(none)                     div_cash_paid(t)              Cash dividend outgo
(none)                     loan_draws(t)                 Net loan advances
NetCF_t                    liability_cf(t)               Net liability CF, outgo +
(none)                     net_cf(t)                     The same, income positive
(none)                     result_cf_annual()            result_cf() summed into years
(none)                     result_pols()                 The counts and decrement rates
=========================  ============================  ===================================

Eight names needed care.

``mort_rate`` is the **best-estimate** rate — the one that actually decrements the
block — while the guarantee and dividend-scale rates are ``mort_rate_guar`` and
``mort_rate_scale``. All three come off the same shipped table through the References
``ae_best_est`` and ``ae_scale``. The notes call this out as a consistency trap: the
same table feeds claim outgo and the dividend's mortality margin **with opposite
signs**, so raising best-estimate mortality raises claims *and*, if the scale factor
moves with it, cuts the dividend.

``policy_term`` is the **premium-paying** period ``m`` in years, not the coverage
period. Coverage runs to ``maturity_mth()`` in every variant; on the base pay-to-100
design the two coincide, on ``PAY_10`` they do not. It stays in years because the
contract states it in years; ``premium_pp`` compares it against ``duration(t)``.

``pols_lapse`` counts **surrenders**. The notes say "surrenders", ``BasicTerm_S`` says
``pols_lapse``, and ``CashValue_SE``'s ``kind`` string is ``"LAPSE"``; the model keeps
the lifelib name so the ``kind`` vocabulary stays intact.

The notes' ``CSV_t`` is the cash surrender value, not a file. It is reached as
``claim_pp(t, "LAPSE")`` so that all three benefit amounts share one cells and one
``kind`` vocabulary with ``CashValue_SE``.

``age(t)`` and ``age_anniv(t)`` are both needed: the notes index mortality at the
attained age entering the policy year but price paid-up additions bought at the end of
it one year later. Getting them the wrong way round shifts every dividend purchase by
a year.

``anniv`` alone means the anniversary that **ends** a policy year — ``is_anniv(t)``,
``anniv_mth(t)``, ``age_anniv(t)`` — and ``prev_anniv`` the one that **opened** it, as in
``div_prev_anniv(t)``, so the opening state's ``pua_face_prev_anniv_init``,
``loan_bal_prev_anniv_init`` and ``div_prev_anniv_init`` are the values at the
anniversary on or before the valuation date. An extract that fills them from the
anniversary after it is a year out.

``pols_if(t)`` is the **start**-of-month count — the notes' ``l_t``, not their
``l_{t+1}`` — after the month's new business and before its decrements,
``pols_if_at(t, "BEF_DECR")``. That is the library-wide convention, the count every
cash flow on the same ``result_cf()`` row is weighted by, and on a point issued at
``t = 0`` it is ``WholeLife_US_S``'s ``pols_if``. The notes' end-of-period state
variable is not lost — it is ``pols_if_at(t, "AFT_DECR")``, which is
``pols_if_at(t + 1, "BEF_NB")`` by construction, the count carried into the next month
before that month's new business.

``liability_cf(t)`` and ``net_cf(t)`` are the same stream with opposite signs — see the
sign-convention rubric below.

.. rubric:: Timing and kind arguments

``pols_if_at(t, timing)`` takes five timings, in processing order: ``"BEF_NB"`` (the
count carried in from month t - 1, before month t's new business), ``"BEF_DECR"``
(start of month t, after its new business and before any decrement — the same number as
``pols_if(t)``), ``"BEF_SURR"`` (after deaths, before surrenders), ``"BEF_MAT"`` (after
surrenders, before maturity) and ``"AFT_DECR"`` (after every decrement, the notes'
``l_{t+1}``) — the notes' end-of-period processing order, deaths then dividend then
surrenders then maturity, now applied every month. ``"BEF_NB"`` and ``"BEF_DECR"`` are
``basiclife.BasicTerm_SE``'s names, and ``"BEF_DECR"`` and ``"BEF_MAT"``
``CashValue_SE``'s; ``"BEF_SURR"`` is added because this product settles deaths and
surrenders in one end-of-period step, and ``"AFT_DECR"`` because ``CashValue_SE`` has no
string for the point past the last decrement, which is where the notes' state variable
lives. One name means two instants in the two references: ``basiclife.BasicTerm_SE``'s
``"BEF_MAT"`` counts the policies at the **start** of a month, before that month's
maturities, where this model's, :mod:`~.WholeLife_US_S`'s, counts them at its **end**,
after its surrenders. The policies here mature at the end of the last covered month, as
the S goldens have it, so the name keeps the S meaning and ``basiclife.BasicTerm_SE``'s
timing is not adopted. ``claim_pp(t, kind)`` and ``claims(t, kind)`` take ``"DEATH"``,
``"LAPSE"`` and ``"MATURITY"``. Both raise ``ValueError("invalid timing")`` /
``ValueError("invalid kind")`` on anything else.

.. rubric:: The dividend is rounded to the cent

``div_round_digits = 2`` rounds the credited base dividend before it buys paid-up
additions. This is **[std]**, and it is not cosmetic: the notes' worked example adds the
*displayed* margins (216.00 + 85.25 + 25.00 = 326.25) and then divides 326.25 by the
net single premium. Carrying the unrounded 326.248 through instead moves the purchased
paid-up-additions face from 776.79 to 776.78 — a full displayed cent, because the exact
value sits just under the rounding boundary. Declared dividends are credited in whole
cents, so the model rounds; setting ``div_round_digits = None`` turns it off and a test
pins the size of the gap in both directions.

.. rubric:: The worked example sets the PUA-block dividend aside

The notes' worked-example table computes steps 11-15 from the base-block dividend
alone, saying so explicitly: "For clarity the PUA-block dividend ``D^PUA`` is
omitted from this table; in the model it adds ... to the amount in step 9." The
Reference ``pua_div_on`` ships **False** so the base deterministic run reproduces the
worked example exactly, the same way ``Term_US_S`` ships ``conv_rate_base = 0``. It is
a reproduction switch, not a claim that paid-up additions are excluded from the
dividend — they are dividend-eligible, and ``pua_div_on = True`` is the
product-faithful setting. ``div_pua(t)`` implements the notes' formula either way, and
a test asserts its value on the anchor cell against the notes' own parenthetical.

.. rubric:: The four guarantee-basis tables are not one construction

The notes' first "known modeling pitfall" is a mismatch between the cash value table and
the ``NSP``/annuity functions, and prescribes regenerating every guarantee-basis
quantity from one 2017 CSO / 4% source. **The shipped tables do not satisfy that**, and
no set of tables carrying the worked example's anchors could. On any single mortality
basis at interest ``i``, endowment insurance and the annuity-due satisfy
``A_{x:n} = 1 - d ae_{x:n}`` with ``d = i/(1+i)``, so the notes' own definition collapses
to ``NNLP = 1000 d NSP_45 / (1 - NSP_45)``; the worked example's ``NNLP = 13.00`` then
forces ``NSP_45 = 0.252616``. But
``NSP_y = v(NSP_{y+1} + q_y (1 - NSP_{y+1})) >= v NSP_{y+1}`` for any ``q_y >= 0``, so
``NSP_55 <= NSP_45 (1.04)^10 = 0.373933`` — below the worked example's ``NSP_55 = 0.42``.
Read the other way: ``NSP_55 = 0.42`` forces ``NSP_45 >= 0.283737`` and hence
``NNLP >= 15.236`` per $1,000, 17% above the notes' 13.00. The worked example's steps 3
and 10 are mutually unreachable, whatever mortality table is used.

What the shipped tables do instead **[std]**: *mort_table.csv* is an illustrative Makeham
curve pinned to ``q^g_54 = 0.00320``; *nsp_table.csv* is a separate parametric curve
pinned to ``NSP_55 = 0.42`` and ``NSP_100 = 1``; *np_guar_table.csv* holds
``1000 NSP_x / ae_{x:(100-x)}`` with the annuity taken on the mortality table's own
survivorship, which is what makes ``NP_g = 13.00``; and *cv_table.csv* is a monotone
shape solved through its policy-year 9 and 10 rows — the worked example's 95.00 and
112.00 per $1,000, which are ``cv_pp_anniv(9)`` and ``cv_pp_anniv(10)`` — to ``1000.00``
at attained age 100. Reconciling the NSP curve with the mortality table needs a
guarantee interest rate that falls from 5.99% at age 45 to 0.02% at age 99, and
inverting the curve for the implied ``q`` at 4% gives a negative rate at every age up to
57 and a rate above 1 from age 89 on.

The two *consequences* the pitfall names are nevertheless absent, and are asserted by
tests: ``NSP_100 = 1`` exactly, so ``pua_cv(t) == pua_face(t)`` in the last projected
month, ``t = proj_len() - 1``, which is the notes' month ``T - 1``, and the schedule
reaches exactly face in that final policy month, so ``cv_pp(t) == sum_assured()``
there. Neither block leaks at maturity. What is missing is the *means* — one basis —
not the endpoints. Swap in a licensed 2017 CSO / 4% set and all four files must be
replaced together; the worked example will then no longer reproduce, which is the honest
price of the notes' own arithmetic.

.. rubric:: Sign convention — two names, one stream

The whole-life notes print ``NetCF_t`` with **outgo positive**, which is the opposite of
the sign the other eleven reference models in ``products/`` carry. Rather than pick one
and lose the other, the model publishes both and names them apart:

``liability_cf(t)``
    The notes' ``NetCF_t``, verbatim: **outgo positive**. Premium and rider income enter
    with a minus sign; expenses, premium tax, claims, cash dividends and net loan
    advances enter with a plus. A positive ``liability_cf`` is money leaving the
    insurer. This is the number to compare against the notes.

``net_cf(t)``
    ``-liability_cf(t)``: **income positive**, the sign convention every model in
    ``products/`` carries, so that ``result_cf()["net_cf"]`` can be summed or compared
    across products. A positive ``net_cf`` is money arriving at the insurer.

Both are columns of ``result_cf()``. The pattern is ``SPIA_US_S`` and
``DIA_US_S``'s, which face the same clash. Nothing about the whole-life
notes' own convention is being denied — it is being kept under a name that does not
collide with the library-wide one, because a sign error in a 55-year liability
projection is invisible in a summary statistic.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point, its row of ``model_point_table_sec.csv``, as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def product():
    """The product code: WL_PAR, WL_FE_LEVEL or WL_FE_GRADED."""
    return model_point()["product"]


def is_par():
    """True for the participating design, which is the only one that pays dividends."""
    return product() == "WL_PAR"


def premium_period():
    """The premium period code: TO_100, PAY_10, PAY_20 or TO_65."""
    return model_point()["premium_period"]


def age_at_entry():
    """The issue age (ANB) of the selected model point.

    The age at issue, not at the valuation date: ``age(0)`` is the attained age then.
    """
    return int(model_point()["issue_age"])


def sex():
    """The sex of the selected model point; rates are sex-distinct throughout."""
    return model_point()["sex"]


def risk_class():
    """The underwriting class of the selected model point (PREF_NT / STD_NT / TOB)."""
    return model_point()["risk_class"]


def sum_assured():
    """The base face amount F of the selected model point."""
    return float(model_point()["face_amount"])


def dividend_option():
    """The elected dividend option: PUA, CASH, ACCUM, REDUCE_PREM, or NONE for non-par."""
    return model_point()["dividend_option"]


def premium_mode():
    """The premium mode of the selected model point: A, SA, Q or M.

    The technical notes' "premium mode modeled: annual" was a consequence of the annual
    grid, not of the contract: every design in the spec is sold on all four modes
    [S1] [S7]. On the monthly grid the mode is a model point attribute, and the shipped
    table exercises both ends of it.
    """
    return model_point()["premium_mode"]


def policy_count():
    """The number of policies the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the policies in force then, before any
    month-0 event; any other point counts the policies it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-policy value — the
    cash value, the paid-up additions, the dividend, the loan, the opening state — is the
    same whatever the count, and every cash flow is a per-policy amount weighted by it.
    """
    return float(model_point()["policy_count"])


def pols_if_init():
    """Policies in force at the valuation date, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose policies
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``WholeLife_US_S``'s cell of the name is the
    count at the start of its frame, which on new business is the issued count.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The policy's age in months at ``t = 0``: 108 for the anchor cell, valued on the
    anniversary that opens its tenth policy year, 114 for the loan variant, valued six
    months into its tenth year, 0 for a policy issued at the valuation date, and -3 for
    one to be issued 3 months after it, which ``Data`` admits up to
    ``future_horizon_mth`` months ahead. It is read as ``basiclife.BasicTerm_SE`` reads
    it, and is the one fact the policy clock takes from the model point. It replaces
    ``WholeLife_US_S``'s ``duration_inforce``, a count of whole policy years, so a policy
    can be valued in any month of its policy year, not on an anniversary alone.
    """
    return int(model_point()["duration_mth"])


def pua_face_init():
    """PUAF entering month 0: the paid-up-additions face per policy at the valuation date.

    The ``pua_face_init`` column: the block in force at the close of policy month
    ``duration_mth_init() - 1``, before any month-0 event, which is what
    ``WholeLife_US_S`` carries into that month as the closing ``pua_face`` of the month
    before. It is the opening balance of :func:`pua_face` at :func:`t_entry`, and the
    paid-up additions the death benefit of month 0 carries. For the anchor cell it is
    the worked example's stipulated 4,100, ``WholeLife_US_S``'s ``puaf_inforce``,
    renamed. Zero for a point not yet in force, as at issue.
    """
    return float(model_point()["pua_face_init"])


def pua_face_prev_anniv_init():
    """PUAF at the anniversary that opened the policy year of month 0, per policy.

    The ``pua_face_prev_anniv_init`` column: the block in force at the close of policy
    month ``12 * duration(0) - 1``, the anniversary on or before the valuation date. The
    annual quantities of a policy year read the block entering it — the PUA-block
    dividend (:func:`div_pua`) and the term-blend gap (:func:`oyt_face`) — and for the
    year already under way at the valuation date that block is this. It is
    :func:`pua_face_init` on a point valued on an anniversary, the same instant, which
    ``Data`` checks, and 0 in the first policy year, which opened at issue. In any other
    month the two can differ, by what the rider instalments and the REDUCE_PREM excess
    have bought since the anniversary.

    ``prev_anniv`` as in :func:`div_prev_anniv`: the anniversary that **opened** the
    year, where :func:`is_anniv`, :func:`anniv_mth` and :func:`age_anniv` name the one
    that ends it. Zero for a point not yet in force.
    """
    return float(model_point()["pua_face_prev_anniv_init"])


def loan_bal_init():
    """L entering month 0: the policy loan balance per policy at the valuation date.

    The ``loan_bal_init`` column: the balance outstanding at the close of policy month
    ``duration_mth_init() - 1``, capitalized interest included, before any month-0
    event. :func:`loan_draw` measures month 0's advance from it, and the death benefit
    of month 0 deducts it. ``WholeLife_US_S``'s ``loan_inforce``, renamed. Zero for a
    point not yet in force.
    """
    return float(model_point()["loan_bal_init"])


def loan_bal_prev_anniv_init():
    """L at the anniversary that opened the policy year of month 0, per policy.

    The ``loan_bal_prev_anniv_init`` column: the balance at the close of policy month
    ``12 * duration(0) - 1``. Loan interest capitalizes once a year on the balance
    outstanding at the previous anniversary (:func:`loan_int`), and the dividend's
    interest margin credits the loaned portion at the loan rate (:func:`div_int`), so
    the year under way at the valuation date reads this. It is :func:`loan_bal_init` on
    a point valued on an anniversary, which ``Data`` checks, and 0 in the first policy
    year. ``prev_anniv`` as in :func:`pua_face_prev_anniv_init`. Zero for a point not
    yet in force.
    """
    return float(model_point()["loan_bal_prev_anniv_init"])


def div_accum_init():
    """DA entering month 0: the dividend accumulation balance per policy.

    The ``div_accum_init`` column: the balance at the close of policy month
    ``duration_mth_init() - 1``, interest and dividends to date included. Only the ACCUM
    option holds one, and ``Data`` refuses a balance on any other. :func:`div_accum`
    opens from it at :func:`t_entry`, and the death benefit of month 0 carries it.
    ``WholeLife_US_S`` opens its in-force point at 0, the notes' ``DA = 0``; a balance
    built up before the valuation date is carried here instead, so that it reaches the
    death, surrender and maturity benefits. Zero for a point not yet in force.
    """
    return float(model_point()["div_accum_init"])


def div_prev_anniv_init():
    """D_{t-1} at month 0: the dividend credited at the anniversary opening its year.

    The ``div_prev_anniv_init`` column, per policy, named for the cell that returns it:
    the dividend credited at the close of policy month ``12 * duration(0) - 1``, the
    anniversary on or before the valuation date. :func:`div_prev_anniv` returns it in
    every month of the policy year under way at the valuation date, so the REDUCE_PREM
    offset, the excess it buys paid-up additions with and the premium-offset overlay all
    read last year's dividend, as they do in every later year. ``WholeLife_US_S`` takes
    it as zero there, an anniversary before its frame. Zero in the first policy year, on
    the non-participating design, and for a point not yet in force.
    """
    return float(model_point()["div_prev_anniv_init"])


def prem_cum_init():
    """Cumulative gross premium paid per policy before the valuation date.

    The ``prem_cum_init`` column: every instalment of :func:`premium_pp` due from issue
    to policy month ``duration_mth_init() - 1``, gross of any dividend offset. Only the
    final-expense graded plan reads it, through :func:`prem_cum`, for the
    110%-of-premiums-paid death benefit of policy years 1-2. Zero for a point not yet in
    force.
    """
    return float(model_point()["prem_cum_init"])


def loan_utilization():
    """Fraction of the guaranteed cash value held as a policy loan **[std]**.

    0 in the base run; the notes' variant is 0.20, maintained by borrowing and
    repaying as the cash value moves.
    """
    return float(model_point()["loan_utilization"])


def term_blend_target():
    """TF: the term-blend rider's target face amount; 0 switches the rider off."""
    return float(model_point()["term_blend_target"])


def is_blended():
    """True when the term-blend rider is active on this model point **[std]**.

    The blend needs the dividend to pay the one-year-term cost, so it is modelled only
    under the PUA dividend option and only on the participating design.
    """
    return is_par() and dividend_option() == "PUA" and term_blend_target() > sum_assured()


def maturity_mth():
    """The policy month at which cover ends: ``12 * (maturity_age - age_at_entry())``.

    The notes' ``T = 12(100 - x)``: the policy matures at attained age 100, so this is
    the ``duration_mth`` of the first month not covered, 660 at issue age 45, and the
    last covered month is ``maturity_mth() - 1``, the one ending at attained age 100. It
    is ``WholeLife_US_S``'s frame length, counted from issue on the policy clock;
    :func:`proj_len` counts from the valuation date instead.

    The contract itself matures at 121, but the guaranteed cash value equals face at
    100 and the paid-up-additions cash value equals paid-up-additions face there, so
    from 100 the policy is economically an endowment at face. Truncating at 100 is a
    **[std]** simplification that moves the age 100-121 payments from death to
    maturity without changing their amount per survivor.
    """
    return 12 * (maturity_age - age_at_entry())                      # noqa: F821


def proj_len():
    """The number of months from the valuation date to maturity.

    ``maturity_mth() - duration_mth_init()``: 660 for a policy issued at age 45 at the
    valuation date, 552 for the anchor cell in force 108 months, and 663 for point 22,
    issued 3 months after the valuation date. The frame is ``t = 0, 1, ...,
    proj_len() - 1``; ``proj_len()`` is its exclusive end, the row count of
    :func:`result_cf`, and ``proj_len() - 1`` is the last covered month, the one ending
    at attained age 100.

    A point at or past maturity at the valuation date has no frame, and raises here,
    naming the point, rather than projecting nothing: an in-force extract should not
    carry it.
    """
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {point_id}: duration_mth {duration_mth_init()} "  # noqa: F821
            f"is at or past maturity, policy month {maturity_mth()}")
    return n


def t_entry():
    """The first month the policy is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of every recursion: :func:`pols_if_at` opens
    there from :func:`pols_if_init`, :func:`pua_face`, :func:`div_accum` and
    :func:`prem_cum` open from the model point's opening state, and every balance read a
    month or a year back is read from the opening state where that month is before it.
    No cell in cover reads a month before it.
    """
    return max(0, -duration_mth_init())


def policy_term():
    """m: the premium-paying period in **years**, from the premium period code.

    This is *not* the coverage period, which runs to :func:`maturity_mth` in every
    variant. It stays in years because the contract states it in years;
    :func:`premium_pp_ann` compares it against ``duration(t)``.
    """
    p = premium_period()
    if p == "TO_100":
        return maturity_age - age_at_entry()                          # noqa: F821
    elif p == "PAY_10":
        return 10
    elif p == "PAY_20":
        return 20
    elif p == "TO_65":
        return max(65 - age_at_entry(), 1)
    else:
        raise ValueError("invalid premium_period")


def duration_mth(t):
    """Completed policy months at the start of month t, the **policy** clock.

    ``duration_mth_init() + t``: ``t`` counts months from the valuation date and
    ``duration_mth(t)`` months from issue, and the two move together. A closed form,
    where ``basiclife.BasicTerm_SE`` adds one a month by recursion: the same numbers,
    without a call chain as long as the frame. Negative before issue. Everything
    contractual reads this clock, through :func:`duration`, :func:`policy_year`,
    :func:`age` and :func:`is_anniv`, and the monthly vocabulary reads the same here as
    in the UL family and ``savings.CashValue_SE``.
    """
    return duration_mth_init() + t


def is_active(t):
    """Whether month t is inside cover: issued, and not yet matured.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from the month
    after the one ending at attained age 100. Outside cover every count is zero, and so
    every cash flow; so is every value state and every dividend, no count cell evaluates
    a rate there, and no table is read at a policy year or an attained age the policy
    does not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def duration(t):
    """Completed policy years at the start of month t, ``duration_mth(t) // 12``.

    0 throughout the first policy year, and negative before issue. Every contractual
    schedule in this product is annual, so this is what the attained age, the cash value
    schedule, the premium period and the decrement vectors are all read at.
    """
    return duration_mth(t) // 12


def policy_year(t):
    """The contractual policy year containing month t, ``duration(t) + 1``.

    A 1-based label on the policy clock, never indexed by: it is the ``policy_year`` key
    of *cv_table.csv*. It is 0 or less before issue, where nothing reads a table by it.
    """
    return duration(t) + 1


def is_anniv(t):
    """True in the **last month of a policy year**, where every annual event lands.

    The dividend is declared and credited here, loan interest capitalizes here, and
    paid-up additions are bought here. ``duration_mth(t) % 12 == 11`` inside cover, and
    False outside it: the month before issue, policy month -1, is no anniversary.
    """
    return is_active(t) and duration_mth(t) % 12 == 11


def anniv_mth(t):
    """The month of the anniversary that **ends** the policy year containing t.

    A **valuation** month, ``t + 11 - duration_mth(t) % 12``: ``t`` itself when
    :func:`is_anniv` is true, and never past the last covered month,
    ``proj_len() - 1``, since the frame ends on an anniversary. It is 11 at ``t = 0`` for
    the anchor cell, whose tenth anniversary is ``WholeLife_US_S``'s month 119:
    ``WholeLife_US_S`` returns the **policy** month ``12 * duration(t) + 11``, the same
    number only where the two clocks coincide. Used by the term-blend layer, which is
    bought at that anniversary and is in force for the whole of the policy year it
    closes, and, twelve months back, by :func:`div_prev_anniv`.
    """
    return t + 11 - duration_mth(t) % 12


def age(t):
    """The attained age x + duration(t) entering the policy year containing month t.

    Mortality in that policy year is indexed here; paid-up additions bought at the
    anniversary that ends it are priced at age_anniv(t).
    """
    return age_at_entry() + duration(t)


def age_anniv(t):
    """The attained age at the anniversary that ends the policy year containing month t."""
    return age_at_entry() + duration(t) + 1


def mec_flag():
    """True where the model point would need a Sect. 7702A test this model does not run.

    The notes are explicit that the reference model does not police Sect. 7702 or
    Sect. 7702A limits and should **flag** model points that would fail rather than
    silently projecting them **[std]**. Limited-pay designs sit near the 7-pay limit
    and paid-up-additions rider payments consume 7-pay room, so both raise the flag.
    """
    return premium_period() != "TO_100" or float(model_point()["pua_rider_premium"]) > 0.0


def premium_rate():
    """Final-expense annual premium per $1,000 of face, from *premium_rates.csv* [S7]."""
    key = (product(), sex(), risk_class(), age_at_entry())
    return float(data.premium_rates().loc[key, "rate_per_1000"])     # noqa: F821


def modal_factor():
    """The fraction of the annual premium collected per instalment [S1] [S7].

    The participating design takes the [S1] scale — semi-annual 0.515, quarterly
    0.26265, monthly 0.085833 — and the final-expense variant the [S7] scale printed on
    its own rate card — 0.52, 0.275, 0.089. Both are sourced, and both carry the modal
    loading inside the factor, so twelve monthly instalments come to 1.03 of the annual
    premium on the participating design and 1.068 on final expense. Each factor is its
    own Reference, so a carrier's own scale drops in without a formula change.
    """
    m = premium_mode()
    if m == "A":
        return 1.0
    elif m == "SA":
        return modal_factor_par_sa if is_par() else modal_factor_fe_sa   # noqa: F821
    elif m == "Q":
        return modal_factor_par_q if is_par() else modal_factor_fe_q     # noqa: F821
    elif m == "M":
        return modal_factor_par_m if is_par() else modal_factor_fe_m     # noqa: F821
    else:
        raise ValueError("invalid premium mode")


def prem_cycle():
    """Months between premium instalments: A 12, SA 6, Q 3, M 1.

    Arithmetic of the mode rather than an assumption, so it is written here rather than
    held in a Reference.
    """
    return {"A": 12, "SA": 6, "Q": 3, "M": 1}[premium_mode()]


def prem_due(t):
    """Whether a modal premium instalment falls due at the beginning of month t.

    Instalments start on the policy anniversary and repeat on the mode's own cycle on
    the policy clock, ``duration_mth(t) % prem_cycle() == 0``: annual in the first month
    of each policy year, semi-annual every sixth month, quarterly every third, monthly
    every month. None falls due outside cover. A point in force mid-year pays its next
    instalment on that cycle, so the loan variant in force 114 months, on annual mode,
    pays nothing until ``t = 6``.
    """
    return is_active(t) and duration_mth(t) % prem_cycle() == 0


def premium_pp_ann(t):
    """G: the gross **annual** premium per policy for the policy year containing month t.

    Level and guaranteed through the policy_term() premium-paying years
    ``duration(t) = 0 .. policy_term() - 1``, zero after, and zero outside cover, where
    the policy has no policy year. The participating design takes G from the model point
    (**[std illustrative]** — carrier rate books are not public); the final-expense
    variant computes it from the sourced rate table as
    ``(F / 1000) * rate(x, sex, class) + 36`` [S7].

    This is the notes' ``G`` and the base for the acquisition expense, the premium
    offset and the paid-up-additions purchases, none of which should move with the
    premium mode; :func:`premium_pp` is what is actually collected in month t.
    """
    if not is_active(t) or duration(t) >= policy_term():
        return 0.0
    elif is_par():
        return float(model_point()["annual_premium"])
    else:
        return sum_assured() / 1000.0 * premium_rate() + fe_policy_fee  # noqa: F821


def premium_net_pp_ann(t):
    """G^net_t: the **annual** premium actually charged for the policy year of month t.

    Under REDUCE_PREM the dividend credited at the anniversary opening that policy year
    offsets the premium, ``max(G - D, 0)``, and any excess buys paid-up additions
    through pua_face_offset(). The dynamic premium-offset overlay (**[std]**, off by
    default) applies a prem_offset_share fraction of the same offset once the dividend
    has grown to cover the premium. For the policy year under way at the valuation date
    that dividend is the model point's div_prev_anniv_init(): point 16, the REDUCE_PREM
    policy valued on the anniversary that opens its tenth year, pays 1,800.00 less last
    year's 288.66 at ``t = 0``.
    """
    g = premium_pp_ann(t)
    if g == 0.0:
        return 0.0
    d = div_prev_anniv(t)
    if dividend_option() == "REDUCE_PREM":
        return max(g - d, 0.0)
    elif prem_offset_on and d >= g:                                  # noqa: F821
        return g - prem_offset_share * min(d, g)                     # noqa: F821
    else:
        return g


def premium_pp(t):
    """The **gross** premium instalment per policy due at the beginning of month t.

    ``modal_factor() * G`` in an instalment month, zero otherwise: what the policy is
    billed before any dividend offset. :func:`premium_net_pp` is what is actually
    collected, and the two differ only under REDUCE_PREM and the premium-offset overlay.
    """
    return modal_factor() * premium_pp_ann(t) if prem_due(t) else 0.0


def premium_net_pp(t):
    """The premium per policy actually collected at the beginning of month t.

    ``modal_factor() * G^net`` in an instalment month, zero otherwise. The dividend
    offset is applied to the annual premium and the instalments then split what is
    left **[std]**, so a mode change moves the timing of the collection and not the
    amount the offset absorbs. This is what :func:`premiums` is weighted from.
    """
    return modal_factor() * premium_net_pp_ann(t) if prem_due(t) else 0.0


def rider_premium_pp_ann(t):
    """A_t: the **annual** paid-up-additions rider premium for the policy year of month t.

    Level while base premiums are payable **[std]**; the notes set it within limits
    fixed at issue and do not schedule it. Zero outside cover.
    """
    if not is_par() or not is_active(t) or duration(t) >= policy_term():
        return 0.0
    return float(model_point()["pua_rider_premium"])


def rider_premium_pp(t):
    """The paid-up-additions rider instalment paid at the beginning of month t.

    The rider is billed with the base premium, so it follows the same modal cycle and
    the same factor **[std]**.
    """
    return modal_factor() * rider_premium_pp_ann(t) if prem_due(t) else 0.0


def prem_cum(t):
    """Cumulative gross premium paid per policy through the beginning of month t.

    Only the final-expense graded plan uses it, for the 110%-of-premiums-paid death
    benefit in policy years 1-2 — and on the monthly grid it now grows with each
    instalment rather than once a year, which is what the graded benefit actually
    tracks [S6][S7]. That design is non-participating, so gross and net coincide there.
    It counts from issue: at :func:`t_entry` it opens from :func:`prem_cum_init`, the
    premiums paid before the valuation date, 0 for a point issued at or after it. Zero
    outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = prem_cum(t - 1) if t > t_entry() else prem_cum_init()
    return prev + premium_pp(t)


def cv_pp_anniv(y):
    """The guaranteed cash value per policy at the anniversary ending policy year y.

    The schedule as it is printed: *cv_table.csv* per $1,000 of face, keyed by the
    contractual 1-based ``policy_year``. Zero for ``y <= 0`` — there is no cash value
    at issue — and zero past maturity, ``y > maturity_mth() // 12``, the years from
    issue to maturity.

    The notes give the Standard Nonforfeiture Law adjusted-premium formula conceptually
    but prescribe a table input in practice, because contractual cash value tables are
    policy-form documents that are not public. The shipped schedule is **[std]**,
    calibrated to the worked example's CV_107 and CV_119 — the policy-year 9 and 10
    rows — and reaching exactly face at attained age 100.

    It is **sex-distinct**, as the notes require of every rate in this product: the male
    pay-to-100 schedule carries the worked example's anchors, and the female schedule is
    that schedule's funding-progress shape ``f = CV^M / (F NSP^M_{x+dur+1})`` applied
    to the female paid-up value ``F NSP^F_{x+dur+1}`` **[std]**. The shape — how far along
    the way to paid-up status the schedule has come — is a design choice that does not
    depend on sex; the value it is progressing towards does, through NSP. See the
    guarantee-basis rubric in the Space docstring for what this construction is *not*.
    """
    if y <= 0 or y > maturity_mth() // 12:
        return 0.0
    key = (premium_period(), sex(), age_at_entry(), y)
    return sum_assured() / 1000.0 * float(
        data.cv_table().loc[key, "cv_per_1000"])                     # noqa: F821


def cv_pp(t):
    """CV_t: the guaranteed cash value per policy at the **end of month t**.

    Straight-line between the schedule's anniversary values **[std]**: ``(k + 1) / 12``
    of the way from ``cv_pp_anniv(duration(t))`` to ``cv_pp_anniv(duration(t) + 1)``,
    where ``k = duration_mth(t) % 12``. Exact at the anniversary, where ``k = 11``, so
    no anniversary quantity — the dividend's interest margin, the net amount at risk,
    the anniversary surrender value — moves by a cent against the annual grid.

    Contractual tables are printed at anniversaries only [unverified]; pro-rating for
    elapsed time is the ordinary policy-form convention, and it is what makes a mid-year
    surrender value mean anything on this grid. Zero outside cover, before the schedule
    is read.
    """
    if not is_active(t):
        return 0.0
    lo = cv_pp_anniv(duration(t))
    hi = cv_pp_anniv(duration(t) + 1)
    return lo + (hi - lo) * (duration_mth(t) % 12 + 1) / 12


def net_amt_at_risk(t):
    """F - CV_t: the guarantee-basis net amount at risk carried by the mortality margin."""
    return sum_assured() - cv_pp(t)


def nsp(y):
    """NSP_y: net single premium per 1 of paid-up endowment-at-100 face at attained age y.

    The purchase basis for paid-up additions, unloaded, on the guarantee basis
    **[std]**. NSP_100 = 1 by construction, which is what makes the paid-up-additions
    cash value equal paid-up-additions face at maturity.

    The shipped curve is *not* the endowment-at-100 net single premium implied by
    *mort_table.csv* at 4%, and cannot be: see the guarantee-basis rubric in the Space
    docstring, which shows that the worked example's own anchors rule out any single
    mortality basis at 4%.
    """
    return float(data.nsp_table().loc[(sex(), y), "nsp"])            # noqa: F821


def nsp_mth(t):
    """The net single premium interpolated to the **end of month t** **[std]**.

    The same straight line :func:`cv_pp` takes, between ``NSP_{age(t)}`` and
    ``NSP_{age_anniv(t)}``, so the paid-up-additions block is valued on the same clock
    as the base cash value. Exact at the anniversary, where it is ``NSP_{age_anniv(t)}``
    — which is what keeps ``pua_cv`` equal to ``pua_face`` in the final month, where
    ``NSP_100 = 1``. Zero outside cover, before the table is read at an age the policy
    does not reach in force.
    """
    if not is_active(t):
        return 0.0
    lo, hi = nsp(age(t)), nsp(age_anniv(t))
    return lo + (hi - lo) * (duration_mth(t) % 12 + 1) / 12


def np_guar():
    """NP_g: the nonforfeiture net level premium per policy, from *np_guar_table.csv*.

    The dividend's interest margin is credited on the guaranteed fund *including* the
    year's net premium, so this quantity sits inside div_int() **[std]**.

    The notes define it over the **endowment** period, ``NNLP = F NSP_x / ae_{x:(100-x)}``,
    and annotate the *other* nonforfeiture quantity — the adjusted premium P_adj — with
    "(m = premium period)", so the (100 - x) subscript is deliberate: NNLP does not vary
    with the premium period. The shipped table therefore carries one value per (sex,
    issue age), repeated across the premium periods; the premium_period key is kept so a
    carrier table that *does* vary by m can be dropped in without a formula change.
    """
    key = (premium_period(), sex(), age_at_entry())
    return sum_assured() / 1000.0 * float(
        data.np_guar_table().loc[key, "np_guar_per_1000"])           # noqa: F821


def mort_rate_guar_at(y):
    """q^g_y: the guaranteed **annual** mortality rate at attained age y.

    Read from *mort_table.csv*. The shipped table is **[std]** illustrative and is *not*
    the 2017 CSO the notes name; that table is licensed and cannot be shipped here.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_guar(t):
    """q^g: the annual guarantee rate at the age entering the policy year of month t.

    Zero outside cover, before the table is read at an age the policy does not reach in
    force, so the scale and best-estimate rates built on it are zero there too.
    """
    if not is_active(t):
        return 0.0
    return mort_rate_guar_at(age(t))


def mort_rate_scale(t):
    """q^sc: the dividend scale's annual experience mortality, ae_scale x q^g **[std]**."""
    return ae_scale * mort_rate_guar(t)                              # noqa: F821


def mort_rate(t):
    """q^e: the **annual** best-estimate mortality rate of the policy year of month t.

    ``ae_best_est`` x q^g **[std]**. The notes' sensitivity list flags this as a
    consistency trap: the same table drives claim outgo here and the dividend's mortality
    margin through mort_rate_scale(), with opposite signs. :func:`mort_rate_mth` is the
    rate actually applied in the month.

    Capped at 1, written ``min(q, 1.0)``, as ``WholeLife_US_S`` caps it: past 1 the monthly
    rate has no real value, and with the bound second a missing input, a NaN, stays NaN,
    where ``min(1.0, q)`` would read it as 1. No shipped point reaches the cap.
    """
    return min(ae_best_est * mort_rate_guar(t), 1.0)                 # noqa: F821


def mort_rate_mth(t):
    """The monthly best-estimate mortality rate applied in month t **[std]**.

    ``1 - (1 - q^e)^(1/12)``, so twelve months of it compound back to exactly the
    policy year's annual rate and the in-force at every anniversary is what the annual
    grid carried.
    """
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def dyn_lapse_factor(t):
    """The interest-sensitive lapse multiplier **[std]**, for scenario runs.

    ``min(1 + 2.0 * max(0, r_cmp - i_d - 0.01), 3.0)``, where r_cmp is the competitor
    or market rate in the scenario. Off unless dyn_lapse_on; the calibration is
    judgmental and the research base records no dynamic-lapse study for whole life.
    """
    return min(1.0 + 2.0 * max(0.0, competitor_rate - int_rate_div - 0.01),  # noqa: F821
               3.0)


def lapse_rate(t):
    """w_t: the **annual** surrender rate of the policy year containing month t **[std]**.

    Participating: 5.0% in policy year 1 grading linearly to 2.0% in policy year 10,
    level 2.0% thereafter. Final expense (simplified issue, so heavier): 12% in year 1,
    10% in year 2, grading linearly to 6% by year 5 and level after. Zero in the final
    policy year — the notes' "0 through the final policy year", the year with
    ``duration(t) = maturity_mth() // 12 - 1`` — so that its survivors mature rather
    than surrender.
    """
    y = duration(t)
    if y >= maturity_mth() // 12 - 1:
        return 0.0
    elif is_par():
        w = 0.05 - 0.03 * min(y, 9) / 9.0
    elif y == 0:
        w = 0.12
    elif y == 1:
        w = 0.10
    else:
        w = max(0.10 - (0.04 / 3.0) * (y - 1), 0.06)
    return w * dyn_lapse_factor(t) if dyn_lapse_on else w            # noqa: F821


def lapse_rate_mth(t):
    """The monthly surrender rate applied at the end of month t **[std]**.

    ``1 - (1 - w)^(1/12)`` on the policy year's annual rate. Surrenders are now
    settled where they happen, against an interpolated cash value, rather than being
    collapsed onto the anniversary.
    """
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def div_prev_anniv(t):
    """D_{t-1}: the dividend credited at the anniversary that **opened** the policy year
    containing month t.

    That anniversary is the end of valuation month ``anniv_mth(t) - 12``. Where that
    month is on the books, at or after :func:`t_entry`, the dividend is the one this
    projection credited there. Where it is before, the policy year opened before the
    projection did, and the dividend is the model point's :func:`div_prev_anniv_init`:
    the one credited at the anniversary on or before the valuation date for a point in
    force, and 0 for a point in its first policy year or issued at or after the
    valuation date. Zero outside cover.

    Every annual use of "last year's dividend" — the REDUCE_PREM offset, the
    premium-offset overlay, the excess that buys paid-up additions — reads it here, so
    those rules keep working whichever month of the policy year the premium falls in.
    """
    if not is_active(t):
        return 0.0
    prev = anniv_mth(t) - 12
    return div_credited(prev) if prev >= t_entry() else div_prev_anniv_init()


def div_int(t):
    """D^int_t: the dividend's interest margin at the anniversary ending month t **[std]**.

    ``(i_d - i_g)(CV_{t-12} + NP_g - L_{t-12}) + (i_L - i_g) L_{t-12}``, with direct
    recognition: the loaned portion is credited at the loan rate rather than the
    portfolio dividend rate. With the snapshot i_L = i_d = 6.00% the adjustment is zero,
    which is a coincidence of the snapshot and not a model property. Zero in every month
    that is not an anniversary, as the dividend it is a margin of is, so zero outside
    cover too, before the schedule is read.

    ``CV_{t-12}`` and ``L_{t-12}`` are the balances entering the **policy year** that the
    anniversary closes. The cash value is the schedule's own value at the anniversary
    that opened it, ``cv_pp_anniv(duration(t))``, zero at issue, and the loan the closing
    balance of the month twelve back, or, where that month is before :func:`t_entry`,
    the model point's :func:`loan_bal_prev_anniv_init`. At the anniversary that is
    ``WholeLife_US_S``'s value, which reads the cash value as the closing ``cv_pp`` of the
    month twelve back, for a point in force a month that may precede the valuation date.
    ``WholeLife_US_S``'s cell also answers in the other months, where nothing reads it,
    and this one is zero there.
    """
    if not is_anniv(t):
        return 0.0
    fund = cv_pp_anniv(duration(t)) + np_guar()
    loan = loan_bal(t - 12) if t - 12 >= t_entry() else loan_bal_prev_anniv_init()
    return ((int_rate_div - int_rate_guar) * (fund - loan)           # noqa: F821
            + (int_rate_loan - int_rate_guar) * loan)                # noqa: F821


def div_mort(t):
    """D^mort_t: the dividend's mortality margin, (q^g - q^sc)(F - CV_t) **[std]**."""
    return (mort_rate_guar(t) - mort_rate_scale(t)) * net_amt_at_risk(t)


def div_exp(t):
    """D^exp_t: the dividend's expense margin, a flat per-policy amount **[std]**."""
    return expense_margin                                            # noqa: F821


def div_base(t):
    """D_t: the base-block dividend credited at the anniversary ending month t.

    ``max(D^int + D^mort + D^exp, 0)``, rounded to div_round_digits, and zero in every
    month that is not an anniversary — the declaration is annual [S1] — so zero outside
    cover too. The floor is **[std]**: dividends are non-negative distributions of
    surplus, so adverse experience does not claw back. No dividend is credited before
    **policy year** div_first_year — that is, for ``duration(t) < div_first_year - 1`` —
    a real cross-carrier design split that the notes keep as a parameter, and none at all
    on the non-participating final-expense design.
    """
    if (not is_anniv(t) or not is_par()
            or duration(t) < div_first_year - 1):                    # noqa: F821
        return 0.0
    d = max(div_int(t) + div_mort(t) + div_exp(t), 0.0)
    return d if div_round_digits is None else round(d, div_round_digits)  # noqa: F821


def div_pua(t):
    """D^PUA_t: the dividend earned by the paid-up-additions block **[std]**.

    ``(i_d - i_g) PUACV_{t-12} + (q^g - q^sc)(PUAF_{t-12} - PUACV_{t-12})``, on the block
    entering the **policy year** this anniversary closes — the closing block of the
    month twelve back, or, where that month is before :func:`t_entry`, the model point's
    :func:`pua_face_prev_anniv_init`, valued at ``NSP_{x+dur}``. Paid-up additions are
    dividend-eligible, and the compounding this creates is the notes' first-ranked
    sensitivity. Switched **off** by ``pua_div_on`` in the shipped base run because the
    worked example's table omits it; see the Space docstring. Zero outside cover, where
    no month is an anniversary.
    """
    if (not pua_div_on or not is_anniv(t) or not is_par()            # noqa: F821
            or duration(t) < div_first_year - 1):                    # noqa: F821
        return 0.0
    puaf = pua_face(t - 12) if t - 12 >= t_entry() else pua_face_prev_anniv_init()
    puacv = puaf * nsp(age(t))
    return ((int_rate_div - int_rate_guar) * puacv                   # noqa: F821
            + (mort_rate_guar(t) - mort_rate_scale(t)) * (puaf - puacv))


def div_credited(t):
    """D_t + D^PUA_t: the whole dividend credited to survivors at the end of month t.

    Non-zero only at an anniversary, which is where the declaration falls, and zero
    outside cover.
    """
    if not is_active(t):
        return 0.0
    return div_base(t) + div_pua(t)


def oyt_face(t):
    """OYT_t: the one-year-term face the term-blend rider carries **through the policy
    year containing month t**.

    The layer is bought at the anniversary that closes that policy year, from that
    year's dividend, and is a *one-year* term: it is level for the twelve months, which
    is why this cell is constant within the policy year rather than only defined at the
    anniversary. The amount is ``max(TF - F - PUAF_{prev}, 0)``, capped at what the
    dividend can fund **[std]**. Two readings had to be settled here, and both are
    standardizations:

    The notes write the gap as ``TF - F - PUAF_t``, which is circular — the term cost
    is deducted from the dividend that buys those very additions — so the model uses
    the paid-up-additions face entering the policy year: the closing balance of the
    month twelve before its anniversary, or, where that month is before
    :func:`t_entry`, the model point's :func:`pua_face_prev_anniv_init`.

    The notes are also silent on what happens when the dividend cannot pay for the
    whole gap. Leaving the formula uncapped would report a term face the model never
    charges for and would inflate the death benefit, so the layer is capped at
    ``D_t (1 + i_g) / q^sc_{x+dur+1}`` — as much term as the dividend actually buys.

    Whether the cap binds is a property of how the blend is funded, not of the design.
    On model point 8, where a $5,000 paid-up-additions rider premium funds the 2x
    target, it binds only in policy year 1, where no dividend is payable at all under
    div_first_year = 2, and the gap closes in policy year 8. On model point 14, the same
    2x target with no rider premium, it binds in policy years 1-3 while the dividend is
    small and again in every year from the thirtieth on as ``q^sc`` outruns it, and the
    block never crosses over. Crossover, after which the rider is pure paid-up
    additions, is where the gap itself reaches zero.

    So every month of a policy year reads the dividend of the anniversary that ends it,
    :func:`div_credited` at :func:`anniv_mth`, up to eleven months ahead: the one read
    this model makes further ahead than the month after its own. It opens no chain
    forward. That dividend depends on the balances entering the year and on the
    schedules alone, never on this layer or on a month after the anniversary, and the
    anniversary is never past the last covered month. Zero outside cover.
    """
    if not is_blended() or not is_active(t):
        return 0.0
    a = anniv_mth(t)
    prev = a - 12
    puaf = pua_face(prev) if prev >= t_entry() else pua_face_prev_anniv_init()
    gap = max(term_blend_target() - sum_assured() - puaf, 0.0)
    q = ae_scale * mort_rate_guar_at(age_anniv(t))                   # noqa: F821
    if gap == 0.0 or q <= 0.0:
        return gap
    return min(gap, div_credited(a) * (1.0 + int_rate_guar) / q)     # noqa: F821


def oyt_cost(t):
    """The dividend absorbed by the one-year-term layer at the anniversary **[std]**.

    ``q^sc_{x+dur+1} x OYT_t x v_g``, charged once a year against the dividend that
    buys the layer, so it is zero in every month that is not an anniversary.
    """
    if not is_anniv(t) or oyt_face(t) == 0.0:
        return 0.0
    return (ae_scale * mort_rate_guar_at(age_anniv(t))               # noqa: F821
            * oyt_face(t) / (1.0 + int_rate_guar))                   # noqa: F821


def div_to_pua(t):
    """The part of the credited dividend that buys paid-up additions at the end of month t.

    Under the PUA option, everything left after the term-blend cost. Under CASH it is
    paid out, under ACCUM it goes to div_accum(), and under REDUCE_PREM it offsets the
    next policy year's premium with the excess handled by pua_face_offset() — except at
    the final anniversary, the last covered month, where there is no following policy
    year to offset. The notes are silent on that last dividend; routing it anywhere else
    would drop it, so the whole of it is treated as REDUCE_PREM excess and buys paid-up
    additions at NSP_100 = 1 **[std]**, which is the same rule the option already
    applies in every year whose premium the dividend has outgrown. Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    elif dividend_option() == "PUA":
        return max(div_credited(t) - oyt_cost(t), 0.0)
    elif (dividend_option() == "REDUCE_PREM"
          and duration_mth(t) == maturity_mth() - 1):
        return div_credited(t)
    else:
        return 0.0


def div_cash(t):
    """D^cash_t: the cash dividend paid per surviving policy at the end of month t."""
    return div_credited(t) if dividend_option() == "CASH" else 0.0


def div_accum(t):
    """DA_t: the dividend accumulation balance at the end of month t.

    ``DA_{t-1}(1 + i_d)^(1/12) + D_t`` under the ACCUM option, zero otherwise and zero
    outside cover. The balance entering :func:`t_entry` is the model point's
    :func:`div_accum_init`: zero for a point issued at or after the valuation date — the
    notes' ``DA = 0`` initialization — and the balance built up before it for a point in
    force. The balance now accrues interest monthly, so twelve months of it compound to
    exactly the annual credit the notes state, and the dividend lands on it at the
    anniversary. The credit rate reuses the dividend interest rate **[std]**: one
    carrier announces its accumulation rate annually with the dividend scale [S2], and
    no separate figure is published. The balance adds to the death, surrender and
    maturity proceeds.
    """
    if not is_active(t) or dividend_option() != "ACCUM":
        return 0.0
    prev = div_accum(t - 1) if t > t_entry() else div_accum_init()
    return prev * (1 + int_rate_div) ** (1 / 12) + div_credited(t)   # noqa: F821


def pua_face_purch(t):
    """dPUAF_t: paid-up-additions face bought by the dividend, div / NSP_{x+dur+1}.

    Non-zero only at an anniversary, where the dividend is credited, and priced at the
    attained age reached there — the notes' ``NSP_{x+dur(t)+1}``.
    """
    d = div_to_pua(t)
    return d / nsp(age_anniv(t)) if d else 0.0


def pua_face_rider(t):
    """dPUAF^rider_t: paid-up-additions face bought by the rider instalment paid in month t.

    ``A (1 - load) / NSP``, a 10% load **[std]** chosen from the observed 7.5%-10%
    range on rider payments. Dividend purchases carry no load; only rider payments do.
    Each instalment buys additions when it is paid, priced at the net single premium
    where the payment falls, the **start** of month t — ``k / 12`` of the way from
    ``NSP_{age(t)}`` to ``NSP_{age_anniv(t)}``, ``k = duration_mth(t) % 12``, on the
    straight line :func:`nsp_mth` draws, so ``NSP_{age(t)}`` itself at the anniversary
    — so a monthly-mode rider buys twelve small layers through the year rather than one
    at the anniversary. ``WholeLife_US_S`` reads the same price as ``nsp_mth`` at the
    month before, which for a point valued mid-year would be a month before the
    valuation date.
    """
    a = rider_premium_pp(t)
    if not a:
        return 0.0
    lo, hi = nsp(age(t)), nsp(age_anniv(t))
    price = lo + (hi - lo) * (duration_mth(t) % 12) / 12
    return a * (1 - pua_rider_load) / price                          # noqa: F821


def pua_face_offset(t):
    """Paid-up-additions face bought by the REDUCE_PREM excess, when the premium falls.

    Once the prior anniversary's dividend exceeds the annual premium it is offsetting,
    the excess buys paid-up additions **[std]** rather than being paid out. It is
    applied in the month the policy year's premium is first due, and priced at the
    attained age entering that policy year. It carries the dividend of the anniversary
    that opened the policy year, so it can never carry the final one; that last
    dividend is routed through div_to_pua() instead — see its docstring. Zero outside
    cover.
    """
    if (dividend_option() != "REDUCE_PREM" or not is_active(t)
            or duration_mth(t) % 12):
        return 0.0
    excess = max(div_prev_anniv(t) - premium_pp_ann(t), 0.0)
    return excess / nsp(age(t)) if excess else 0.0


def pua_face(t):
    """PUAF_t: paid-up-additions face in force at the end of month t.

    ``PUAF_{t-1}`` plus the dividend, rider and premium-offset purchases of month t.
    The opening balance at :func:`t_entry` is the model point's :func:`pua_face_init`,
    which is what makes the worked example's stipulated prior balance of 4,100 an input
    rather than a projection, and 0 for a point issued at or after the valuation date.
    Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    prev = pua_face(t - 1) if t > t_entry() else pua_face_init()
    return (prev + pua_face_purch(t)
            + pua_face_rider(t) + pua_face_offset(t))


def pua_cv(t):
    """PUACV_t: the cash value of the paid-up additions, PUAF_t x nsp_mth(t) **[std]**.

    Valuing the whole block at the attained-age net single premium is exact at the
    issue of each layer and again at age 100, and approximate in between; the monthly
    interpolation of NSP puts it on the same clock as the base cash value. Zero outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return pua_face(t) * nsp_mth(t)


def loan_int(t):
    """Loan interest capitalized at the anniversary ending month t, L_{prev anniv} x i_L.

    Capitalization is contractually annual [S1], so it lands on the anniversary and is
    zero in every other month, and outside cover. The balance it is charged on is the
    one outstanding at the previous anniversary: the closing balance of the month twelve
    back, or, where that month is before :func:`t_entry`, the model point's
    :func:`loan_bal_prev_anniv_init`.
    """
    if not is_anniv(t):
        return 0.0
    opening = loan_bal(t - 12) if t - 12 >= t_entry() else loan_bal_prev_anniv_init()
    return opening * int_rate_loan                                   # noqa: F821


def loan_bal(t):
    """L_t: the policy loan balance at the end of month t **[std]**.

    The notes' variant holds the loan at ``loan_utilization x CV_t``, maintained by
    borrowing and repaying as the cash value moves; the base run sets loan_utilization
    to zero. Because ``cv_pp`` now moves monthly, so does the balance. Loans reduce the
    death, surrender and maturity proceeds. A point in force at the valuation date is
    held at the same fraction from month 0 on, whatever its :func:`loan_bal_init`, and
    month 0's :func:`loan_draw` closes any gap between the two. Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    return loan_utilization() * cv_pp(t)


def loan_draw(t):
    """Net new borrowing per policy in month t; negative repays.

    The balance change net of the interest that capitalized into it, so the cash the
    insurer actually advances. Summed over a policy year it is exactly the annual
    grid's single advance, because the interest term lands once, at the anniversary.
    The balance entering :func:`t_entry` is the model point's :func:`loan_bal_init`, 0
    for a point issued at or after the valuation date. Zero outside cover.
    """
    if not is_active(t):
        return 0.0
    opening = loan_bal(t - 1) if t > t_entry() else loan_bal_init()
    return loan_bal(t) - opening - loan_int(t)


def claim_pp(t, kind):
    """The benefit amount per policy in month t, by kind.

    ``"DEATH"``
        DB_t = F + PUAF_{t-1} + OYT_t + DA_{t-1} - L_{t-1}. Deaths fall at the end of the
        month, and at an anniversary *before* the dividend is credited, so the benefit
        carries the paid-up additions, accumulation balance and loan entering the month
        **[std]** — the closing balances of month t - 1, or the model point's opening
        state at :func:`t_entry`. The one-year-term layer is the one in force through the
        policy year, where ``F + PUAF + OYT`` is the notes' "target face plus excess
        paid-up additions" written so that it still holds when the dividend funds only
        part of the gap. On the final-expense graded plan, natural-cause deaths in policy
        years 1-2 pay 110% of cumulative premiums paid and accidental deaths pay the full
        face from day one [S6][S7]; the two are blended by fe_accid_share **[std]**,
        since the model carries one mortality decrement. Zero outside cover.
    ``"LAPSE"``
        CSV_t = CV_t + PUACV_t + DA_t - L_t, the surrender value at the end of month t,
        including any dividend just credited. Both cash value components interpolate
        between anniversaries, so a mid-year surrender is valued where it happens.
    ``"MATURITY"``
        MAT = F + PUAF + DA - L at the end of the last covered month,
        ``duration_mth(t) = maturity_mth() - 1``, which is ``t = proj_len() - 1``, and
        zero in every other month. On the non-participating design this is F - L.
    """
    if kind == "DEATH":
        if not is_active(t):
            return 0.0
        if product() == "WL_FE_GRADED" and duration(t) < fe_graded_years:  # noqa: F821
            return ((1 - fe_accid_share) * fe_graded_factor * prem_cum(t)  # noqa: F821
                    + fe_accid_share * sum_assured())                # noqa: F821
        puaf = pua_face(t - 1) if t > t_entry() else pua_face_init()
        accum = div_accum(t - 1) if t > t_entry() else div_accum_init()
        loan = loan_bal(t - 1) if t > t_entry() else loan_bal_init()
        face = sum_assured() + puaf + oyt_face(t)
        return face + accum - loan
    elif kind == "LAPSE":
        return cv_pp(t) + pua_cv(t) + div_accum(t) - loan_bal(t)
    elif kind == "MATURITY":
        if duration_mth(t) != maturity_mth() - 1:
            return 0.0
        return sum_assured() + pua_face(t) + div_accum(t) - loan_bal(t)
    else:
        raise ValueError("invalid kind")


def pols_if_at(t, timing):
    """The number of policies in force at a point inside month t.

    The timings in processing order:

    ``"BEF_NB"``
        the count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's deaths and surrenders, out of month t - 1's
        ``"BEF_DECR"`` count. At :func:`t_entry`, the first month on the books, it is
        :func:`pols_if_init`, the count in force at the valuation date (0 for a point
        issued at or after it), and the recursion reads no earlier month. Zero outside
        cover, so the survivors of the last covered month leave as
        :func:`pols_maturity`.
    ``"BEF_DECR"``
        l_t: ``"BEF_NB"`` plus :func:`pols_new_biz`, before any decrement; the same
        number as pols_if(t), and the weight on that month's cash flows.
    ``"BEF_SURR"``
        after deaths, before surrenders — the population the dividend is
        credited to and the one surrenders are taken from.
    ``"BEF_MAT"``
        after surrenders, before maturity; the survivors of the month. It is
        ``WholeLife_US_S``'s ``"BEF_MAT"``, at the end of the month, and not
        ``basiclife.BasicTerm_SE``'s, which counts the policies at the start of a
        month, before that month's maturities: the name is shared, the instant is not.
    ``"AFT_DECR"``
        l_{t+1}, the notes' end-of-period state variable: what is left once the month's
        deaths, surrenders and — in the last covered month — the maturities have all
        been taken, so it is zero there and outside cover. It is
        ``pols_if_at(t + 1, "BEF_NB")`` by construction, the count carried into the
        next month before that month's new business. The string is added to
        CashValue_SE's set because that model has no name for the point past the last
        decrement, which is where these notes keep their in-force probability.

    ``"BEF_NB"`` and ``"BEF_DECR"`` are ``basiclife.BasicTerm_SE``'s names, and any timing
    but these five raises. ``"BEF_NB"`` forms the count left at the end of month t - 1
    itself — month t - 1's ``"BEF_NB"`` plus its :func:`pols_new_biz`, after its deaths
    and surrenders, the products ``"BEF_MAT"`` takes in the order it takes them — rather
    than calling for it. So the chain of calls from month t back to :func:`t_entry` is
    one cell a month, where ``WholeLife_US_S``'s ran through five: a compiled model runs
    that chain on the C stack. Every count is zero outside cover, before any rate is
    read.
    """
    if timing == "BEF_NB":
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, "BEF_NB") + pols_new_biz(t - 1))
                * (1 - mort_rate_mth(t - 1)) * (1 - lapse_rate_mth(t - 1)))
    elif timing == "BEF_DECR":
        return pols_if_at(t, "BEF_NB") + pols_new_biz(t)
    elif timing == "BEF_SURR":
        if not is_active(t):
            return 0.0
        return pols_if_at(t, "BEF_DECR") * (1 - mort_rate_mth(t))
    elif timing == "BEF_MAT":
        if not is_active(t):
            return 0.0
        return pols_if_at(t, "BEF_SURR") * (1 - lapse_rate_mth(t))
    elif timing == "AFT_DECR":
        if not is_active(t) or duration_mth(t) == maturity_mth() - 1:
            return 0.0
        return pols_if_at(t, "BEF_MAT")
    else:
        raise ValueError("invalid timing")


def pols_if(t):
    """The number of policies in force at the **start** of month t, the weight of row t.

    ``pols_if_at(t, "BEF_DECR")``, the notes' l_t: the count carried in from month t - 1
    plus month t's new business, before month t's decrements — the population that pays
    the month's premium, carries its expenses and is exposed to its decrements, so it is
    the weight on every cash flow of the same result_cf() row. On a point issued at
    ``t = 0`` it is exactly ``WholeLife_US_S``'s ``pols_if``. A point in force at the
    valuation date opens with pols_if_init(), and one issued at or after it with its
    issued count in the issue month. Zero outside cover: before issue, and from
    ``t = proj_len()`` on, because everything still in force in the last covered month
    matures there and the contract terminates.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity. The notes' end-of-period l_{t+1} is
    ``pols_if_at(t, "AFT_DECR")``.
    """
    return pols_if_at(t, "BEF_DECR")


def pols_new_biz(t):
    """Number of policies issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later. A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Deaths in month t, the monthly rate applied to the policies in force at its start.

    Zero outside cover.
    """
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t) if is_active(t) else 0.0


def pols_lapse(t):
    """Surrenders at the end of month t, the monthly rate applied to its survivors.

    Zero outside cover.
    """
    return pols_if_at(t, "BEF_SURR") * lapse_rate_mth(t) if is_active(t) else 0.0


def pols_maturity(t):
    """Policies maturing at attained age 100; non-zero only in the last covered month.

    That month is ``duration_mth(t) = maturity_mth() - 1``, the frame's last row,
    ``t = proj_len() - 1``. Not a decrement — the modelled contract simply ends — but
    the in-force roll-forward does not close without it.
    """
    return (pols_if_at(t, "BEF_MAT")
            if duration_mth(t) == maturity_mth() - 1 else 0.0)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t / 12)``.

    On the **valuation** clock: ``t`` counts months from the valuation date, so the
    maintenance charge it inflates is in valuation-date dollars, whatever the policy's
    age, and every point of a block inflates alike. ``WholeLife_US_S`` inflates from
    issue; on a point issued at ``t = 0`` the two are the same, and on the anchor cell,
    in force 108 months, this model's charge is ``WholeLife_US_S``'s divided by
    ``1.02^9``. Acquisition is not inflated (see :func:`expenses`). Compounded on the
    monthly grid rather than stepped at anniversaries: on the annual grid the factor
    could only move once a year, and the monthly refinement is one of the things the
    finer grid buys. It is still exactly ``1.02^k`` ``k`` years after the valuation date.
    """
    return (1 + inflation_rate) ** (t / 12)                          # noqa: F821


def premiums(t):
    """Premium income at the start of month t (an inflow), net of any dividend offset."""
    return premium_net_pp(t) * pols_if_at(t, "BEF_DECR")


def rider_premiums(t):
    """Paid-up-additions rider premium income at the start of month t (an inflow)."""
    return rider_premium_pp(t) * pols_if_at(t, "BEF_DECR")


def premium_taxes(t):
    """Premium tax at the start of month t **[std]**, on premium and rider income.

    The notes' processing order collects it alongside the expenses; their one-line
    NetCF formula omits it. The model follows the processing order and keeps it as its
    own line, so it now falls with each instalment rather than once a year.
    """
    return premium_tax_rate * (premiums(t) + rider_premiums(t))      # noqa: F821


def expenses(t):
    """E_t: acquisition and inflating maintenance expense in month t **[std]**.

    90% of the first year's **annual** premium plus $250 per policy issued — charged in
    the issue month, on :func:`pols_new_biz`, and not inflated, as in
    ``basiclife.BasicTerm_SE`` — then $60 per policy per year inflating at 2% on the
    valuation clock, accruing at a twelfth a month on the policies in force at the start
    of the month. The acquisition charge does not move with the premium mode, and a
    point in force at the valuation date never sees it, because it was issued before.
    ``WholeLife_US_S`` charges it at ``t = 0`` on the policies in force there, which on a
    point issued at ``t = 0`` is the same charge.
    """
    acq = ((expense_acq_prem_rate * premium_pp_ann(t) + expense_acq)  # noqa: F821
           * pols_new_biz(t))
    return (acq + expense_maint / 12 * inflation_factor(t)           # noqa: F821
            * pols_if_at(t, "BEF_DECR"))


def claims(t, kind=None):
    """Benefit outgo in month t, by kind; the total when kind is omitted."""
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "MATURITY"))
    elif kind == "DEATH":
        return claim_pp(t, "DEATH") * pols_death(t)
    elif kind == "LAPSE":
        return claim_pp(t, "LAPSE") * pols_lapse(t)
    elif kind == "MATURITY":
        return claim_pp(t, "MATURITY") * pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def div_cash_paid(t):
    """Cash dividends paid out at the end of month t, to the survivors of the month."""
    return div_cash(t) * pols_if_at(t, "BEF_SURR")


def loan_draws(t):
    """Net policy loans advanced at the end of month t **[std]**, an outflow.

    The notes report gross liability flows plus a separate loan account rather than
    netting the loan into a net-amount-at-risk presentation. Advances go to the
    policies still in force; the balance is recovered through the death, surrender and
    maturity benefits, which are all net of the loan.
    """
    return loan_draw(t) * pols_if_at(t, "BEF_MAT")


def liability_cf(t):
    """NetCF_t: the net liability cash flow in month t, **outgo positive**.

    The technical notes' formula verbatim, and the one to compare against them: premium
    and rider income enter with a minus sign; expenses, premium tax, death, surrender
    and maturity benefits, cash dividends and net loan advances enter with a plus, so a
    positive value is money leaving the insurer. Internal dividend applications —
    paid-up additions, accumulation, premium reduction — are not cash flows when
    credited: they emerge later through the death benefit, the surrender value and the
    maturity benefit.

    These notes are the only ones in the library that print the outgo-positive sign, so
    the stream is published twice: here under the notes' sign, and negated as net_cf(t)
    under the library's. See the sign-convention rubric in the Space docstring.
    """
    return (-premiums(t) - rider_premiums(t)
            + expenses(t) + premium_taxes(t)
            + claims(t) + div_cash_paid(t) + loan_draws(t))


def net_cf(t):
    """The net cash flow in month t, **income positive**: -liability_cf(t).

    Income less outgo, the sign every model in ``products/`` carries, so that a
    ``result_cf()["net_cf"]`` column can be summed or compared across products. A
    positive value is money arriving at the insurer. liability_cf(t) is the same stream
    under the technical notes' own outgo-positive sign; both are result_cf() columns
    because neither reading may be lost.
    """
    return -liability_cf(t)


def result_cf():
    """Result table of cashflows, one row per month ``t = 0 .. proj_len() - 1``.

    Row 0 is the valuation month for every model point, so the frames of a block line up
    and sum row by row, and a point issued after the valuation date has zeros until its
    issue month. The columns are ``WholeLife_US_S``'s. ``pols_if`` is the
    start-of-month count, which is the weight applied to every cash flow on the same
    row. Both signs of the net flow are published: ``net_cf`` is income-positive, the
    library-wide convention, and ``liability_cf`` is the technical notes'
    outgo-positive ``NetCF_t``; the two are negatives of each other.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "rider_premiums": [rider_premiums(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "div_cash_paid": [div_cash_paid(t) for t in ts],
            "loan_draws": [loan_draws(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
            "liability_cf": [liability_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cf_annual():
    """:func:`result_cf` summed into policy years, indexed by ``policy_year``.

    Every cash flow column is the total of the year's months in the frame, and
    ``pols_if`` is the count in its first month in the frame. The months before issue
    belong to no policy year and are left out. On a point issued at ``t = 0`` every year
    is whole, ``pols_if`` is the count at the **start** of the policy year, which is the
    number the annual-step model carried on the same row, and the table is
    ``WholeLife_US_S``'s. A point in force at the valuation date may open part-way
    through a policy year, as the loan variant in force 114 months does: its first row
    then holds the rest of that year only, and its ``pols_if`` is the count at the
    valuation date. The two grids agree on ``pols_if`` exactly and on nothing else,
    which is the point of the finer one — see the Space docstring.
    """
    df = result_cf()
    df = df.loc[[t for t in df.index if is_active(t)]]
    years = pd.Index([duration(t) + 1 for t in df.index],            # noqa: F821
                     name="policy_year")
    out = df.drop(columns="pols_if").groupby(years).sum()
    out.insert(0, "pols_if", df["pols_if"].groupby(years).first())
    return out


def result_pols():
    """Result table of policy counts and decrement rates, indexed by t.

    One row per month ``t = 0 .. proj_len() - 1``. First the counts :func:`result_cf`
    weights its rows by, and how they move, as ``basiclife.BasicTerm_SE``'s
    ``result_pols`` sets them out: ``pols_if``, the count of month t; ``pols_new_biz``,
    the part of it issued in month t; then month t's deaths and surrenders in processing
    order, and the maturities of the last covered month. Row by row, ``pols_if`` at
    ``t + 1`` is ``pols_if`` less the three outflows of month t, plus the new business of
    month ``t + 1``. Then ``WholeLife_US_S``'s four decrement rates, annual and monthly,
    which are 0 outside cover, where the model reads no rate.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "mort_rate": [mort_rate(t) if is_active(t) else 0.0 for t in ts],
            "mort_rate_mth": [mort_rate_mth(t) if is_active(t) else 0.0 for t in ts],
            "lapse_rate": [lapse_rate(t) if is_active(t) else 0.0 for t in ts],
            "lapse_rate_mth": [lapse_rate_mth(t) if is_active(t) else 0.0 for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_cv():
    """Result table of the guaranteed and non-guaranteed values, indexed by t.

    The account-value analogue for this product: the guaranteed cash value, the
    paid-up-additions block, the accumulation balance and the loan, plus the dividend
    that drives them and the two benefit amounts they feed. Every balance on row t is
    the **closing** value of month t. One row per month ``t = 0 .. proj_len() - 1``,
    zeros before a point's issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "cv_pp": [cv_pp(t) for t in ts],
            "div_base": [div_base(t) for t in ts],
            "div_pua": [div_pua(t) for t in ts],
            "pua_face": [pua_face(t) for t in ts],
            "pua_cv": [pua_cv(t) for t in ts],
            "div_accum": [div_accum(t) for t in ts],
            "loan_bal": [loan_bal(t) for t in ts],
            "db_pp": [claim_pp(t, "DEATH") for t in ts],
            "surr_value_pp": [claim_pp(t, "LAPSE") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in month t; zero everywhere.

    ``pols_if(t) - pols_if_at(t + 1, "BEF_NB") - deaths - surrenders - maturities``, the
    notes' ``l_t - l_{t+1} - ...``, where ``l_{t+1}`` is the count carried into the next
    month before its new business, which is no part of month t's movement. Maturities
    are non-zero only in the last covered month, where the survivors neither die nor
    surrender: their contract ends. Without that term the last month appears to lose
    lives with no cause.
    """
    return (pols_if(t) - pols_if_at(t + 1, "BEF_NB")
            - pols_death(t) - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected month.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so
    one test can call it across every model. check_pols_roll_fwd_resid(t) gives the
    signed residual of the month that failed. The tolerance scales with policy_count(),
    since the residual is an accumulation of rounding on that many policies, in force at
    the valuation date or issued after it.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= 1e-10 * max(policy_count(), 1.0)
               for t in range(proj_len()))


def check_pua_roll_fwd_resid(t):
    """The paid-up-additions roll-forward residual in month t; zero everywhere.

    ``PUAF_t - PUAF_{t-1} - dividend purchases - rider purchases - offset purchases``,
    with ``PUAF_{t-1}`` the block entering the month — pua_face_init() at t_entry(). The
    analogue of ``CashValue_SE.check_av_roll_fwd`` for a product whose accumulating state
    is a face amount rather than an account value.
    """
    opening = pua_face(t - 1) if t > t_entry() else pua_face_init()
    return (pua_face(t) - opening - pua_face_purch(t)
            - pua_face_rider(t) - pua_face_offset(t))


def check_pua_roll_fwd():
    """True when the paid-up-additions roll-forward closes in every projected month.

    No argument, one bool over all t, matching check_pols_roll_fwd();
    check_pua_roll_fwd_resid(t) gives the signed residual. The tolerance is relative to
    the block itself, which reaches six figures of face on a compounding projection.
    """
    return all(abs(check_pua_roll_fwd_resid(t)) <= 1e-9 * max(pua_face(t), 1.0)
               for t in range(proj_len()))


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

maturity_age = 100

modal_factor_par_sa = 0.515

modal_factor_par_q = 0.26265

modal_factor_par_m = 0.085833

modal_factor_fe_sa = 0.52

modal_factor_fe_q = 0.275

modal_factor_fe_m = 0.089

int_rate_guar = 0.04

int_rate_div = 0.06

int_rate_loan = 0.06

ae_scale = 0.7

ae_best_est = 0.7

expense_margin = 25.0

div_first_year = 2

div_round_digits = 2

pua_div_on = False

pua_rider_load = 0.1

expense_acq_prem_rate = 0.9

expense_acq = 250.0

expense_maint = 60.0

inflation_rate = 0.02

premium_tax_rate = 0.02

fe_policy_fee = 36.0

fe_graded_years = 2

fe_graded_factor = 1.1

fe_accid_share = 0.03

dyn_lapse_on = False

competitor_rate = 0.06

prem_offset_on = False

prem_offset_share = 0.5

pd = ("Module", "pandas")
