# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

r"""The by-contract projection of :mod:`~.RILA_US_SEC`.

``RILA_US_S`` run from a valuation date. The Space is parameterized by ``point_id``, so
``Projection[1]`` is an ItemSpace projecting model point 1, the anchor cell issued at the
valuation date, where every number is ``RILA_US_S``'s::

    >>> Projection[1].result_iv()          # the worked example's own table
    >>> Projection[1].result_cf()
    >>> Projection[16].result_cf()         # the anchor cell, in force 71 months
    >>> Projection.point_id = 2            # or switch the default, before computing

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/registered_index_linked_annuity/``, read at run time rather than stored inside
the model. The model folder therefore holds nothing but formulas — no ``_data/``, no
IOSpec, no embedded values — so a diff of the model shows logic changes only, and an input
can be edited or swapped without rewriting the model. This follows
``annuallife.TradLife_A``; contrast ``basiclife.BasicTerm_S``, which keeps its inputs
*inside* the model through modelx's IOSpec machinery.

The consequence worth knowing: **the model is not portable on its own.** Copying the
``RILA_US_SEC`` folder without its parent's CSVs produces a model that
reads and then fails on first evaluation.

The readers and the filename References live on the sibling
:mod:`~.RILA_US_SEC.Data` Space, reached here through the ``data``
Reference, so each file is read once per model rather than once per model point. Five of
the files are ``RILA_US_S``'s, read in place; the model point table and the market
scenarios are this model's own:

=========================  ==================================  ==========================
Reference (on Data)        Cells                               File
=========================  ==================================  ==========================
model_point_file           data.model_point_table()            model_point_table_sec.csv
mort_table_file            data.mort_table()                   mort_table.csv
market_scenario_file       data.market_scenario()              market_scenario_sec.csv
surr_charge_file           data.surr_charge_table()            surr_charge_table.csv
guar_min_rate_file         data.guar_min_rate_table()          guar_min_rate_table.csv
lapse_file                 data.lapse_table()                  lapse_table.csv
withdrawal_file            data.withdrawal_table()             withdrawal_table.csv
=========================  ==================================  ==========================

``market_scenario`` is the input class peculiar to this product: the *contractual* formula
consumes market data, so the index level, the Market Value Rate, the risk-free rate, the
dividend yield and the implied volatility are inputs on the same footing as the
withdrawal-charge schedule, not a valuation overlay. It runs on the valuation clock
(below), and each model point restated in force or issued after the valuation date reads
its own copy of its scenario, re-based to its month.

.. rubric:: Projection basis

``t`` counts **months from the valuation date** and is **0-based**: ``t = 0`` is the
valuation month, the same month for every model point however old the contract, month
``t`` runs from time ``t`` to time ``t + 1``, and the frame is ``t = 0 … proj_len() - 1``,
so ``len(result_cf()) == proj_len()``, with ``proj_len() = maturity_mth() -
duration_mth_init()``. The **policy clock** is :func:`duration_mth`,
``duration_mth_init() + t``, the policy months elapsed at the start of month ``t``, which is
``RILA_US_S``'s ``t``: on a contract issued at the valuation date the two clocks coincide,
and every number is ``RILA_US_S``'s. Following the notes, every within-month quantity is
evaluated at the month **end**, time ``t + 1``: the market state, the interim value, the
Account Value and the benefits on row ``t`` are the values there, while ``pols_if(t)`` is
the count entering the month at time ``t``. The Issue Date opens the contract's first
month, the one with ``duration_mth(t) == 0``, so the purchase payment, the acquisition
expense and the opening state of a contract issued at or after the valuation date fall
inside that row rather than in a row of their own.

**Two clocks.** The market runs on the **valuation** clock, which every point of a block
shares: the index level, the Market Value Rate and the option-pricing market month ``t``
is valued at are the scenario's at time ``t + 1`` (:func:`market_state`), and expense
inflation steps every twelve months from the valuation date (:func:`inflation_factor`).
Everything contractual runs on the **policy** clock: the terms and their Term Start and
End Dates (:func:`term_elapsed_mth`), the Contract Anniversaries and the free-withdrawal
base snapshotted at them, the withdrawal charge and the surrender behaviour keyed to it,
the attained age, the withdrawal programme (:func:`wd_amount_pm`) and the Maturity Date
(:func:`maturity_mth`). Each test of a month against a contractual date reads
``duration_mth(t)``, and a policy month that names a month to read, a Term Start Date or
an anniversary, is turned into a month from the valuation date once, by subtracting
``duration_mth_init()``, in the one cell that reads it.

**A month-end valuation has two readings of "the contract year", and the model carries
both.** ``duration(t) = duration_mth(t) // 12`` is the *interval* reading and lifelib's
0-based duration: the complete contract years elapsed at the **start** of month ``t``,
i.e. the contract year the whole month lies inside. It is the right one for a rate that
applies across the month — the attained age behind ``q_m(t)`` (:func:`age`).
``duration_eom(t) = (duration_mth(t) + 1) // 12`` is the *instant* reading, the notes'
``cy`` at the month end: how many complete contract years have elapsed at time ``t + 1``,
where the month's transactions and decrements settle. It is the right one for the
withdrawal charge a transaction bears (:func:`surr_charge_rate`), the free-withdrawal base
snapshotted at an anniversary (:func:`free_wd_base`), and the surrender behaviour keyed to
that charge (:func:`policy_year`, :func:`lapse_rate_sc_mult`, :func:`lapse_rate_base`),
which must see the charge expire in the same month the contract does. The two differ
**only in the month that closes on an anniversary**: at policy month 11 ``duration`` is 0
but ``duration_eom`` is 1, so that month bears the age-``x`` mortality rate while a
surrender settling at its end is already on the year-2 side of the charge schedule. The
expense inflation step is the one annual step on the valuation clock instead,
``1.025^(t // 12)``, so that every point of a block carries its expenses in
valuation-date dollars.

:mod:`.MYGA_US_S` needs only one reading, because its beginning-of-month transaction
convention makes the two coincide: there the anniversary month belongs to the year that is
opening, here the anniversary closes the month that has just run, and the two products'
``policy_year`` readings differ in exactly that one month a year. Each convention is the
right one for its own timing basis.

Within month ``t`` the notes' processing order is: refresh the **market state**; apply
**term-end crediting** if ``t`` is a Term End Date; apply the **renewal / transfer** roll
split and re-strike the option; compute **interim values**; accrue the **accounts** and
set the Account Value, snapshotting the free-withdrawal base on a Contract Anniversary;
take **contract-holder transactions**; and apply **decrements** at the end of the month —
death at ``q_m(t)``, then surrender at ``w_m(t)`` on survivors **[std order]**, plus the
discrete term-end surrender fraction ``phi`` at a Term End Date.

Two conventions carry that order through the cells. Every quantity of the option bucket is
**homogeneous of degree one in the Investment Amount** — the notes require it, and the
model imposes it by holding the per-unit ratio :func:`iv_ratio` and multiplying, so a
withdrawal reduces the interim value by exactly the cash removed. And each month's
valuation refers to the option **in force during that month**, which at a Term End Date is
the *expiring* one: :func:`tau` is 0 there, not ``T``, so the replicating portfolio
collapses to intrinsic value and reproduces the crediting rate exactly.

.. rubric:: In force at the valuation date

A model point is a contract issued at the valuation date (``duration_mth_init() == 0``),
one already in force there (the months since issue), or one to be issued ``k`` months
later (``-k``), up to ``Data.future_horizon_mth`` months on. Every recursion opens at
:func:`t_entry`, the first month on the books, and none reads a month before it. A
contract issued at or after the valuation date opens as ``RILA_US_S`` opens at issue: the
purchase payment allocated wholly to the option, the general accounts empty, no free
withdrawal amount, its contracts entering as :func:`pols_new_biz` in the issue month. A
contract in force opens from the model point's opening state, what ``RILA_US_S`` carries
into the valuation month, per contract, before any month-0 event: the Investment Amount,
which is also the crediting basis, the Fixed and Holding Accounts, the Account Value, the
Free Withdrawal Amount still unused and the return-of-premium base
(:func:`inv_amt_pp_init`, :func:`fixed_acct_pp_init`, :func:`holding_acct_pp_init`,
:func:`av_pp_init`, :func:`free_wd_remain_init`, :func:`rop_pp_init`), and the Account
Value at the Contract Anniversary on or before the valuation date, the base of the
contract year's Free Withdrawal Amount (:func:`av_pp_prev_anniv_init`); its count in
force is :func:`pols_if_init`.

The **term under way** is fixed at its Term Start Date. Where that date precedes the
valuation month, its index level, its Market Value Rate and its option-pricing market are
the model point's (:func:`index_at_term_start_init` and the four beside it), and so is the
cap re-solved there at a renewal under ``nge_reset`` (:func:`cap_rate_init`): facts frozen
at a past date, which a change to the market or to a Reference at the valuation date must
not move, and which no scenario re-based to the valuation date holds. A term that starts
at or after the valuation month reads its start from the scenario, as ``RILA_US_S`` does,
and re-solves its cap there. Terms align with issue, every ``12 x term_years`` policy
months, so the Term Start Date follows from the policy clock and takes no column.
``RILA_US_S`` does not implement the Performance Lock, and this model, ``RILA_US_S`` run in
force, adds none: a contract carries no lock flag and no locked value.

The Account Value may be of **either sign**. It is the interim value plus the two
accounts, and the interim value can be negative even when the index has risen [S2], so
``Data`` accepts any finite opening Account Value and refuses instead a contract in force
that holds nothing, no investment amount and no account balance.

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``, and
this library's deferred annuity chassis :mod:`.MYGA_US_S`, wherever those have
an analogue — ``pols_*`` for policy counts, ``av_*`` for account values, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-contract amounts, ``*_at(t, timing)``
for a quantity read at a point inside the month, ``*_init`` for a contract's opening state
at the valuation date (``basiclife.BasicTerm_SE``'s ``pols_if_init``), ``*_pm(m)`` for a
schedule read by policy month and ``*_py(y)`` by contract year. The technical notes use
compact actuarial symbols instead. The mapping is:

===========================  ================================  =============================
Notes symbol                 Cells                             Meaning
===========================  ================================  =============================
(valuation clock)            t, the cells argument             Month from the valuation
                                                               date, 0-based; time t opens
                                                               month t
t                            duration_mth(t)                   Policy months elapsed at the
                                                               start of month t
(none)                       duration_mth_init()               Policy months at the
                                                               valuation date; -k if issued
                                                               k months on
(none)                       t_entry()                         First month on the books
(none)                       is_active(t)                      Whether month t is in cover
cy(t) = floor(t/12)          duration(t)                       Complete years during month t
cy_end(t) = floor((t+1)/12)  duration_eom(t)                   Complete years at t's month
                                                               end
cy_end(t) + 1                policy_year(t)                    Contract year in force there
x                            age_at_entry                      Issue age (ANB)
x + cy(t)                    age(t)                            Attained age (ANB) during t
(Maturity Date)              policy_term                       Years from issue to maturity
(Maturity Date)              maturity_mth()                    Policy month cover ends at
(none)                       proj_len                          Months projected from the
                                                               valuation date
P                            premium_pp                        Single purchase payment
T                            term_years                        Index-linked term in years
(Term Start Date)            term_start_month(t)               First month of that term, a
                                                               policy month
(none)                       term_elapsed_mth(t)               Months elapsed in that term
(Term End Date)              is_term_end(t)                    True when t ends a term
tau_k(t)                     tau(t)                            Years remaining in the term
(the market path)            market_state(t, name)             The scenario at time t from
                                                               the valuation date
I(t)                         index_level(t)                    Index level
I_s                          index_at_term_start(t)            Index level at the Term Start
I_s, before t = 0            index_at_term_start_init          I_s of a term begun before
                                                               the valuation month
R_k(t)                       index_perf(t)                     I(t)/I_s - 1
r(t)                         mvr(t)                            Market Value Rate (CMT)
r_0                          mvr_at_term_start(t)              Market Value Rate at term
                                                               start
r_0, before t = 0            mvr_at_term_start_init            r_0 of a term begun before
                                                               the valuation month
(r, q, sigma)                risk_free(t), div_yield(t),       Option-pricing market state
                             impl_vol(t)
(r, q, sigma) at term start  risk_free_at_term_start(t),       Option-pricing market on the
                             div_yield_at_term_start(t),       Term Start Date
                             impl_vol_at_term_start(t)
(the same, before t = 0)     risk_free_at_term_start_init,     Their values for a term begun
                             div_yield_at_term_start_init,     before the valuation month
                             impl_vol_at_term_start_init
N(.)                         norm_cdf(x)                       Standard normal c.d.f.
d1, d2                       bs_d1(...), bs_d2(...)            Black-Scholes arguments
C(I,K,tau)                   bs_call(...)                      European call
P(I,K,tau)                   bs_put(...)                       European put
BC(I,K,tau)                  bs_binary_call(...)               Cash-or-nothing binary call
b                            buffer                            Buffer
c, s, e (model point)        declared_cap, declared_step,      Rates declared on the model
                             declared_edge                     point
c                            cap_rate(t)                       Cap Rate in force, floored
c, before t = 0              cap_rate_init                     Cap re-solved at a renewal
                                                               before the valuation month
s                            step_rate(t)                      Step Rate in force, floored
e                            edge_rate(t)                      Edge Rate in force, floored
PR                           participation                     Participation Rate
f                            floor_rate                        Floor (optional module)
(crediting type)             is_cap_crediting(),               crediting_type decoded
                             is_step_crediting(),
                             is_edge_crediting(),
                             is_floor_crediting()
(interim value family)       is_iv_portfolio(),                iv_family decoded
                             is_iv_notional(),
                             is_iv_delta(),
                             is_iv_legacy()
(amortization rule)          is_straight_line(),               amort_rule decoded
                             is_updated_expiry()
guar_min_cap(T)              guar_min_rate(kind)               Contractual minimum by term
(one option leg)             opt_component(t, leg, ...)        Signed per-unit leg value
(the leg set)                opt_legs()                        Legs of the replicating set
Pi(I, tau)                   opt_portfolio(t, spot, tau, mkt)  Per-unit portfolio value
(sum of \|legs\|)            opt_portfolio_abs(...)            Trading-cost assessment base
beta                         opt_budget(t)                     Initial option budget
y_e, spread                  earned_rate, nge_spread           Earned rate; target margin
                                                               [std]
beta_target(T)               opt_budget_target()               NGE cap-solve target
(the cap solve)              declared_cap_solved(t)            Cap solving Pi = beta_target
g                            credit_rate_term(t)               Term-end crediting rate
AccruedCapRate               credit_rate_accrued(t)            Pre-AG 54 time-prorated rate
B_k(t)                       budget_amort_pp(t)                Amortized initial budget
F_k(t)                       fixed_proxy_pp(t)                 Fixed Income Asset Proxy
D_k(t)                       deriv_proxy_pp(t)                 Derivative Asset Proxy
TC_k(t)                      trading_cost_pp(t)                Trading cost provision
kappa                        trading_cost_rate                 Trading cost factor
[(1+r_0)/(1+r(t))]^tau       mva_factor(t)                     Interim-value rate adjustment
CCF_k(t)                     cap_calc_factor(t)                Cap Calculation Factor,
                                                               family (b)
E_0                          iv_expense_rate                   CCF expense rate [std],
                                                               family (b)
rate(t), family (b)          risk_free(t) + iv_credit_spread   Investment-grade discount
                                                               rate
DailyAdjustment(t)           fixed_proxy_factor(t),            Family (c), the delta form
                             deriv_proxy_factor(t)
V_k(t)                       interim_value_pp_at(t, timing)    Interim Value
V_k(t)/IA_k(t)               iv_ratio(t)                       Interim Value per unit of
                                                               base
(the decomposition base)     iv_notional_pp(t, timing)         Notional a component sits on
IA_k(t)                      inv_amt_pp(t)                     Investment Amount
IA_k(t) inside the month     inv_amt_pp_at(t, timing)          BEF_CREDIT, BEF_ROLL,
                                                               BEF_WD, AFT_WD
IA_k, before t = 0           inv_amt_pp_init                   Investment Amount entering
                                                               month 0
FA(t)                        fixed_acct_pp(t)                  Fixed Account value
HA(t)                        holding_acct_pp(t)                Holding Account value
FA, HA before t = 0          fixed_acct_pp_init,               The accounts entering month 0
                             holding_acct_pp_init
i_declared                   acct_rate()                       Declared rate on FA and HA
AV(t)                        av_pp(t), av_pp_at(t, timing)     Account Value
AV, before t = 0             av_pp_init                        Account Value entering month
                                                               0
l(t) x AV(t)                 av_at(t, timing)                  In-force weighted Account
                                                               Value
ROP(t)                       rop_pp(t)                         ROP base at the end of month
                                                               t
ROP, before t = 0            rop_pp_init                       ROP base entering month 0
DB(t)                        death_ben_pp(t)                   Death benefit
CSV(t)                       surr_value_pp(t)                  Cash surrender value
AV_anniv(y)                  free_wd_base(t)                   Account Value at the
                                                               anniversary
AV_anniv(y), before t = 0    av_pp_prev_anniv_init             AV_anniv(y) of the year under
                                                               way, its anniversary before
                                                               the valuation month
0.10 x AV_anniv(y)           free_wd_allow(t)                  Free Withdrawal Amount
FW(t)                        free_wd_avail(t)                  Allowance before the
                                                               withdrawal
FW(t) after the withdrawal   free_wd_remain(t)                 Allowance a surrender can
                                                               shelter
FW, before t = 0             free_wd_remain_init               Allowance unused entering
                                                               month 0
FW_used(y)                   free_wd_avail/free_wd_remain      Consumed amount, as its
                                                               complement
G_total                      wd_pp(t)                          Gross amount removed
G_k                          wd_alloc_pp(t, bucket)            Amount taken from one bucket
(scheduled part of G)        wd_scheduled_pp(t)                Programme's withdrawal in
                                                               month t
(the programme)              wd_amount_pm(m)                   Its withdrawal at policy
                                                               month end m
(behavioural part of G)      wd_behavioral_pp(t)               The anniversary rule's
                                                               withdrawal
(free part of G)             wd_free_pp(t)                     Portion inside the free
                                                               amount
chargeable                   wd_excess_pp(t)                   Amount exposed to the charge
wc(cy)                       surr_charge_rate(t)               Withdrawal charge rate
wc(cy), by year              surr_charge_rate_at(cy)           Its rate in contract year cy
WC(t)                        wd_charge_pp(t)                   Withdrawal charge
net proceeds                 wd_payment_pp(t)                  Cash paid on the withdrawal
chargeable on a surrender    surr_excess_pp(t)                 AV(t) less the free amount
wc x chargeable              surr_charge_pp(t)                 Charge on a full surrender
q_m(t)                       mort_rate_mth(t)                  Monthly mortality rate
(annual q_x)                 mort_rate(t)                      Annual mortality rate
(q_x by age)                 mort_rate_base_at(x)              Table rate at attained age x
w_base(y)                    lapse_rate_base(t)                Un-shocked annual surrender
                                                               rate
w_base(y), by year           lapse_rate_base_py(y)             Its rate in contract year y
M_sc(y)                      lapse_rate_sc_mult(t),            Charge-expiry shock
                             lapse_shock_mult                  multiplier and its **[std]**
                                                               size, 3.0
(the shock year)             lapse_shock_year()                First charge-free contract
                                                               year
M_iv(t)                      lapse_iv_mult(t)                  Moneyness suppression
w_annual(y,t)                lapse_rate(t)                     Total annual surrender rate
w_m(t)                       lapse_rate_mth(t)                 Monthly surrender rate
phi                          term_end_lapse_rate(t)            Term-end surrender
                                                               concentration
l(t)                         pols_if(t)                        In force at the start of
                                                               month t
(none)                       policy_count                      Contracts the point stands
                                                               for
l at the valuation date      pols_if_init                      In force at the valuation
                                                               date
(new business)               pols_new_biz(t)                   Contracts issued in month t
l(t+1)                       pols_if_at(t, timing)             BEF_NB, BEF_DECR, BEF_LAPSE,
                                                               BEF_TERM_SURR, AFT_DECR
l(t) q_m                     pols_death(t)                     Deaths
l(t)(1-q_m) w_m + phi        pols_lapse(t)                     Full surrenders
(the phi part)               pols_lapse_term(t)                Term-end concentrated
                                                               surrenders
(none)                       pols_maturity(t)                  Forced annuitizations at
                                                               maturity
P in the issue month         premiums(t)                       Premium income
(premium credited)           prem_to_av_pp(t), prem_to_av(t)   Premium credited to the base
G_total - WC(t)              withdrawals(t)                    Withdrawal payments
(ledger benefit lines)       claims(t, kind)                   Benefit outgo by kind
(per contract)               claim_pp(t, kind)                 Benefit per contract by kind
(from the Account Value)     claims_from_av(t, kind)           Account Value released
(above the Account Value)    claims_over_av(t, kind)           Benefit paid above the AV
(investment return)          inv_income_pp(t), inv_income(t)   Return credited to the AV
(acquisition; maintenance)   expenses(t)                       0.06 P + 200; 60/12 x
                                                               1.025^(t//12)
1.025^(t//12)                inflation_factor(t)               Expense inflation, valuation
                                                               clock
premium tax                  premium_taxes(t)                  Premium tax, 0% [std]
NetCF(t)                     net_cf(t)                         Net cash flow
===========================  ================================  =============================

.. rubric:: Names that needed care

The notes reuse single letters across three different vocabularies — contract mechanics,
Black-Scholes and the deferred annuity chassis — and the collisions are real.

``T`` is the term length in **years** while ``t`` is a **month**, so it becomes
:func:`term_years`; ``tau`` is likewise in years and stays :func:`tau`. ``P`` is both the
single purchase payment and the Black-Scholes put: :func:`premium_pp` against
:func:`bs_put`. ``C`` is the Black-Scholes call, the [S2] fixed-leg symbol for the Market
Value Rate at term start, *and* the surrender charge on the chassis: :func:`bs_call`,
:func:`mvr_at_term_start` and :func:`surr_charge_pp`. ``B`` is the amortized option budget
here and the buffer is ``b``: :func:`budget_amort_pp` against :func:`buffer`. ``R`` is
index performance and ``r`` is the Market Value Rate: :func:`index_perf` against
:func:`mvr`. ``e`` is the Edge Rate, not Euler's number: :func:`edge_rate`.

One collision is worth stating in prose because getting it wrong would be a modelling
error rather than a naming one. On the deferred annuity chassis ``M(t)`` is a **contract**
market value adjustment applied to the surrender benefit. **This product has no such
thing** — the only MVA-like term in the prospectus is the ``[(1+C)/(1+D)]^E`` factor
*inside* the interim value [S2], which is why it is named :func:`mva_factor` (a factor, in
the interim value) and there is no ``mva_pp``, no ``mva_rate`` and no ``mva_cap_rule``
anywhere in this model. The notes' ``M_sc`` and ``M_iv`` are lapse multipliers and are
named :func:`lapse_rate_sc_mult` and :func:`lapse_iv_mult` so they cannot be read as
adjustments either. Nor is there an ``mgsv_pp``: AG 54 displaces Model #805 outright when
it is satisfied [R2][REG-R42][REG-R44], and the nonforfeiture value *is* the interim
value.

.. rubric:: Timing arguments

Investment Amount, ``inv_amt_pp_at(t, timing)``:

``"BEF_CREDIT"``
    the notional entering month ``t``, which is what the month's valuation applies to. In
    a contract's issue month it is the purchase payment allocated to the option — the
    opening state the Issue Date leaves behind — and in the valuation month of a contract
    in force it is :func:`inv_amt_pp_init`.
``"BEF_ROLL"``
    after term-end crediting, ``IA(1 + g)`` at a Term End Date and unchanged otherwise.
    This is the worked example's **Investment Amount** column.
``"BEF_WD"``
    after the renewal / transfer roll split, so ``roll_share("OPTION")`` of
    ``"BEF_ROLL"`` at a Term End Date and unchanged otherwise.
``"AFT_WD"``
    after the proportional withdrawal reduction. Equal to :func:`inv_amt_pp`.

Interim Value, ``interim_value_pp_at(t, timing)``, takes the same three of those points —
``"BEF_ROLL"``, ``"BEF_WD"``, ``"AFT_WD"`` — and is in each case the Investment Amount at
that point multiplied by :func:`iv_ratio`. ``"BEF_ROLL"`` is the worked example's
**Interim value** column.

The currency decomposition of that value — :func:`fixed_proxy_pp`,
:func:`opt_component_pp`, :func:`deriv_proxy_pp`, :func:`trading_cost_pp` and
:func:`budget_amort_pp` — takes two of them, ``"BEF_ROLL"`` (the default) and
``"AFT_WD"``, through :func:`iv_notional_pp`. That pair is what the worked example's rows
B1 and B2 are: the same month, the same market state, the decomposition before and after
an $8,000 withdrawal, every component scaled by one factor.

Account Value, ``av_pp_at(t, timing)``, following ``CashValue_SE``'s ``av_pp_at``:

``"BEF_WD"``
    ``AV(t)`` as the notes' step 5 leaves it — after crediting, the roll split, the
    interim value and the account accruals, before any transaction. This is the value the
    free-withdrawal base is snapshotted from and the base the withdrawal is allocated
    across.
``"AFT_WD"``
    after the transaction; equal to :func:`av_pp`, and the value every decrement benefit
    is measured on.

Policy counts, ``pols_if_at(t, timing)``, following ``CashValue_SE``'s ``pols_if_at`` and
``basiclife.BasicTerm_SE``'s ``BEF_NB``:

``"BEF_NB"``
    the count carried in from month ``t - 1``, before month ``t``'s new business:
    :func:`pols_if_init` at :func:`t_entry`, and the survivors of month ``t - 1`` after it.
``"BEF_DECR"``
    ``l(t)``, in force at the **start** of month ``t``: ``"BEF_NB"`` plus the month's new
    business, :func:`pols_new_biz`; equal to :func:`pols_if`.
``"BEF_LAPSE"``
    after deaths, ``l(t)(1 - q_m(t))``.
``"BEF_TERM_SURR"``
    after the background monthly surrender, ``l(t)(1 - q_m)(1 - w_m)``.
``"AFT_DECR"``
    after the discrete term-end surrender fraction ``phi``. This is the count at the month
    **end**, the notes' ``l(t+1)``: :func:`pols_if` carries the start-of-month count, so
    the end-of-month one lives here and nowhere else.

Benefit ``kind`` arguments are ``"DEATH"``, ``"LAPSE"`` and ``"MATURITY"``. Withdrawal
allocation ``bucket`` arguments are ``"OPTION"``, ``"FIXED"`` and ``"HOLDING"``. Option
``leg`` arguments are ``"ATM_CALL"``, ``"OTM_CALL"``, ``"OTM_PUT"``, ``"ATM_PUT"``,
``"FLOOR_PUT"``, ``"STEP_BINARY"`` and ``"EDGE_BINARY"``. Market-state ``mkt`` arguments
are ``"CURRENT"`` and ``"TERM_START"``. Any other value of any of these raises
``ValueError``.

There is no ``"ANNUITIZATION"`` kind. The notes give no elective annuitization take-up
for this product; the only annuitization modelled is the **forced** one at the Maturity
Date, which is ``"MATURITY"``.

.. rubric:: pols_maturity and the Maturity Date

Unlike the deferred annuity chassis, this product's horizon is contractual rather than
chosen: the Maturity Date is the later of the anniversary after the oldest owner's 90th
birthday and ten years from issue [S2], so ``policy_term()`` is
``max(90 - age_at_entry(), 10)`` years and :func:`maturity_mth` is twelve times that, the
policy month cover ends at — 360 on the anchor cell, whose last covered policy month is
359. :func:`proj_len` counts from the valuation date to there,
``maturity_mth() - duration_mth_init()``: 360 months on the anchor cell issued at the
valuation date, the last of them ``t = 359``, and 289 on the anchor in force 71 months.
The Maturity Date is that month's end, where the contract force-annuitizes at the Account
Value, and :func:`pols_maturity` carries the survivors out, so that the roll-forward::

    pols_if(t) - pols_if_at(t + 1, "BEF_NB")
        = pols_death(t) + pols_lapse(t) + pols_maturity(t)

closes for every ``t``, including the last — ``pols_if(t)`` opening month ``t`` and
``pols_if_at(t+1, "BEF_NB")`` the count carried into the next, which past the Maturity
Date is zero; the next month's new business is no part of month ``t``'s movement. The name
follows ``BasicTerm_S.pols_maturity`` and the construction follows :mod:`.Term_US_S` and
:mod:`.MYGA_US_S`. The payout stream bought at that date is not derived here: it is the
immediate-annuity chassis, restricted to the two forms this contract offers [S2].
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point, a row of *model_point_table_sec.csv*, as a Series.

    ``RILA_US_S``'s columns, ``pols_if_init`` renamed ``policy_count``, then
    ``duration_mth`` and the thirteen columns of the opening state, as
    ``Data.model_point_table`` checked them, and the generator's ``row_kind``,
    ``source_policy_id`` and ``source_mth``, which no formula reads. The decodes and the
    joins read it directly, so no projection cell calls a label accessor.
    """
    return data.model_point_table().loc[point_id]                    # noqa: F821


def policy_id():
    """The contract identifier of the selected model point."""
    return model_point()["policy_id"]


def age_at_entry():
    """The issue age (ANB) of the selected model point."""
    return int(model_point()["age_at_entry"])


def sex():
    """The sex of the selected model point, M or F."""
    return model_point()["sex"]


def premium_pp():
    """P: the single purchase payment per contract; no subsequent payments [S1][S2]."""
    return float(model_point()["premium"])


def policy_count():
    """The number of contracts the model point stands for, its ``policy_count`` column.

    A point in force at the valuation date counts the contracts in force then, before any
    month-0 event; any other point counts the contracts it issues. Either way the count
    enters the projection once: as :func:`pols_if_init` for the first, as
    :func:`pols_new_biz` in the issue month for the second. Every per-contract value — the
    Investment Amount, the interim value, the accounts, the allowance, the opening state
    — is the same whatever the count, and every cash flow is a per-contract amount
    weighted by it.
    """
    return float(model_point()["policy_count"])


def pols_if_init():
    """l at the valuation date: the contracts in force then, before any month-0 event.

    ``policy_count()`` for a point already in force at ``t = 0``
    (``duration_mth_init() > 0``), and 0 for one issued at or after it, whose contracts
    enter through :func:`pols_new_biz` in the issue month instead, as in
    ``basiclife.BasicTerm_SE``. So on a point issued at ``t = 0`` this is 0, and
    ``pols_if(0)`` is the issued count. ``RILA_US_S``'s cell of the name is the notes'
    ``l(0)``, the count at issue; in both models the count at a month's end is
    ``pols_if_at(t, "AFT_DECR")``.
    """
    return policy_count() if duration_mth_init() > 0 else 0.0


def duration_mth_init():
    """Completed policy months at the valuation date, the ``duration_mth`` column.

    The contract's age in months at ``t = 0``: 71 for the anchor cell valued in the last
    month of its first term, 0 for a contract issued at the valuation date, and -13 for
    one to be issued 13 months after it, which ``Data`` admits up to
    ``future_horizon_mth`` months ahead. It is read as ``basiclife.BasicTerm_SE`` reads it,
    as a whole number whatever the column's type, and is the one fact the policy clock
    takes from the model point.
    """
    return int(model_point()["duration_mth"])


def term_years():
    """T: the index-linked term in years, from the 1 / 3 / 6 menu [S1][S2]."""
    return int(model_point()["term_years"])


def buffer():
    """b: the buffer, guaranteed for the life of each term [S1][S2].

    The buffer absorbs the first ``b`` of index loss and passes the excess through; 10% is
    the one level present in every retrieved insurer's menu [S1]-[S6].
    """
    return float(model_point()["buffer"])


def crediting_type():
    """``CAP``, ``STEP``, ``EDGE`` or ``FLOOR``.

    The chassis offers Cap, Step and Edge crediting [S2]; ``FLOOR`` is the optional module
    that only one insurer in the sample offers and that needs a **four**-option
    replicating portfolio rather than three [S5].
    """
    return model_point()["crediting_type"]


def declared_cap():
    """c: the declared Cap Rate for the initial term, or blank for an uncapped option.

    100% at 6 years, 55% at 3 and 12% at 1 **[std]** — no current rate sheet was
    retrievable, both insurer rate pages returning HTTP 403. A blank means the option is
    uncapped, in which case the out-of-the-money call is valued at zero [S2].
    """
    return float(model_point()["declared_cap"])


def declared_step():
    """s: the declared Step Rate, 8% **[std]**; observed illustrative 8% [S1]."""
    return float(model_point()["declared_step"])


def declared_edge():
    """e: the declared Edge Rate, 6% **[std]**.

    No Edge value appears in any retrieved document; 6% is set below the 8% Step because
    the Edge design pays down to -b rather than to 0 and so buys a lower rate.
    """
    return float(model_point()["declared_edge"])


def participation():
    """PR: the Participation Rate, 100% [S4].

    At ``PR = 1`` the notes' BUFFER + CAP + PR portfolio collapses **exactly** to the
    BUFFER + CAP one, so a single branch serves both; see :func:`opt_component`.
    """
    return float(model_point()["participation"])


def floor_rate():
    """f: the floor for the ``FLOOR`` crediting module, a positive fraction [S5]."""
    return float(model_point()["floor_rate"])


def iv_family():
    """The interim value algebra: ``portfolio``, ``notional``, ``delta`` or ``legacy``.

    ``portfolio`` **[std]** is family (a), the AG 54-literal Hypothetical Portfolio form
    [S2][R2] and the baseline. ``notional`` is family (b), the full Segment Investment
    discounted at a current investment-grade rate plus an always-positive Cap Calculation
    Factor [S4][S6]. ``delta`` is family (c), a delta applied to the notional with **no
    interest-rate adjustment term at all** [S5]. ``legacy`` is the pre-AG 54 time-prorated
    design [S1], which uses no option pricing; it predates AG 54's July 1, 2024 effective
    date [R2] and is carried as a tractable regression contrast, not as a live design.
    """
    return model_point()["iv_family"]


def amort_rule():
    """``straight_line`` **[std]** [S2] or ``updated_expiry`` [S3].

    How the initial option budget is amortized: ``beta x IA x tau/T`` straight-line to
    term end, or the initial-market-conditions portfolio value re-read at the **updated
    time to expiry**. One insurer needs both, split by state [S3], so this is a
    configuration flag rather than a modelling opinion.
    """
    return model_point()["amort_rule"]


def nge_reset():
    """Whether the declared cap is re-solved at each renewal Term Start Date **[std]**.

    False holds the snapshot scale level, which is the notes' base projection. True
    applies the ASOP No. 2 determination rule in :func:`declared_cap_solved`, floored at
    the contractual guaranteed minimum [S2][R5][REG-R26].
    """
    return bool(model_point()["nge_reset"])


def wd_rate_ann():
    """The behavioural partial-withdrawal rate, 2% of Account Value a year **[std]**.

    Zero in contract year 1 because the free amount is zero there [S1][S2]; thereafter
    taken at each Contract Anniversary and capped at the Free Withdrawal Amount, so the
    base run incurs no withdrawal charge. It is a model point column rather than a
    Reference because the notes' worked example and the notes' behavioural rule are
    mutually inconsistent - see the product's ``model.md``, *The worked example and the
    base withdrawal rule contradict each other*.
    """
    return float(model_point()["wd_rate_ann"])


def scenario_id():
    """The market scenario the model point runs on, a key into *market_scenario_sec.csv*.

    A label for reporting: :func:`market_state` reads the model point's column directly.
    A point issued at the valuation date runs on ``RILA_US_S``'s scenario under its own
    id; one restated in force at policy month ``d`` runs on its own copy re-based to that
    month, ``up-M71``, and one issued ``k`` months on on its copy moved ``k`` months
    later, ``up-F13``, which holds no level before the issue month.
    """
    return model_point()["scenario_id"]


def wd_schedule_id():
    """The scheduled withdrawal programme, a key into *withdrawal_table.csv*."""
    return model_point()["wd_schedule_id"]


def is_cap_crediting():
    """Whether the option credits by the Cap Rate method, ``crediting_type`` ``CAP``.

    One of the four decodes of ``crediting_type``, each a bool read where ``RILA_US_S``
    compares the text, so that no projection cell compares the model point's text or
    calls :func:`crediting_type`: :func:`opt_legs`, :func:`opt_component` and
    :func:`credit_rate_at`. A value none of the four decodes knows is refused there, with
    ``RILA_US_S``'s message, where the projection meets it.
    """
    return bool(model_point()["crediting_type"] == "CAP")


def is_step_crediting():
    """Whether the option credits by the Step Rate method, ``crediting_type`` ``STEP``."""
    return bool(model_point()["crediting_type"] == "STEP")


def is_edge_crediting():
    """Whether the option credits by the Edge Rate method, ``crediting_type`` ``EDGE``."""
    return bool(model_point()["crediting_type"] == "EDGE")


def is_floor_crediting():
    """Whether the option credits by the Floor module, ``crediting_type`` ``FLOOR``."""
    return bool(model_point()["crediting_type"] == "FLOOR")


def is_iv_portfolio():
    """Whether the interim value is family (a), ``iv_family`` ``portfolio`` [S2][R2].

    One of the four decodes of ``iv_family``, read where ``RILA_US_S`` compares the text:
    :func:`fixed_proxy_factor`, :func:`deriv_proxy_factor`,
    :func:`trading_cost_factor`, :func:`cap_calc_factor` and :func:`iv_factor`. A value
    none of the four knows is refused in :func:`fixed_proxy_factor`, with ``RILA_US_S``'s
    message.
    """
    return bool(model_point()["iv_family"] == "portfolio")


def is_iv_notional():
    """Whether the interim value is family (b), ``iv_family`` ``notional`` [S4][S6]."""
    return bool(model_point()["iv_family"] == "notional")


def is_iv_delta():
    """Whether the interim value is family (c), ``iv_family`` ``delta`` [S5]."""
    return bool(model_point()["iv_family"] == "delta")


def is_iv_legacy():
    """Whether the interim value is the pre-AG 54 design, ``iv_family`` ``legacy`` [S1]."""
    return bool(model_point()["iv_family"] == "legacy")


def is_straight_line():
    """Whether the option budget amortizes straight-line, ``amort_rule`` ``straight_line``.

    One of the two decodes of ``amort_rule``, read where ``RILA_US_S`` compares the text,
    in :func:`budget_amort_factor`, which refuses a value neither knows with
    ``RILA_US_S``'s message.
    """
    return bool(model_point()["amort_rule"] == "straight_line")


def is_updated_expiry():
    """Whether the budget is re-read at the updated expiry, ``updated_expiry`` [S3]."""
    return bool(model_point()["amort_rule"] == "updated_expiry")


def inv_amt_pp_init():
    """IA_k entering month 0: the Investment Amount per contract at the valuation date.

    What ``RILA_US_S`` carries into the valuation month: the notional the month's
    crediting and interim value apply to, after every term-end credit, roll split and
    proportional withdrawal reduction before it. It is also the crediting basis, so no
    second basis column is needed. Read at :func:`t_entry` on a contract in force, by
    :func:`inv_amt_basis_pp` and :func:`inv_amt_pp`; 0 on a point issued at or after the
    valuation date, which opens with its purchase payment in its issue month.
    """
    return float(model_point()["inv_amt_pp_init"])


def fixed_acct_pp_init():
    """FA entering month 0: the Fixed Account value per contract at the valuation date.

    Read at :func:`t_entry` on a contract in force, by :func:`fixed_acct_pp_at` and
    :func:`fixed_acct_pp`; 0 before the first Term End Date, since only a term end
    transfers to the account, and on a point not yet in force.
    """
    return float(model_point()["fixed_acct_pp_init"])


def holding_acct_pp_init():
    """HA entering month 0: the Holding Account value per contract at the valuation date.

    Read at :func:`t_entry` on a contract in force, by :func:`holding_acct_pp_at` and
    :func:`holding_acct_pp`; 0 before the first Term End Date and on a point not yet in
    force, as :func:`fixed_acct_pp_init` is.
    """
    return float(model_point()["holding_acct_pp_init"])


def av_pp_init():
    """AV entering month 0: the Account Value per contract at the valuation date.

    The close of the month before the valuation month, after its withdrawal: the opening
    from which :func:`inv_income_pp` measures month 0's investment return and
    :func:`av_change` the block's movement. Of either sign: the interim value can be
    negative under the contract [S2]. 0 on a point not yet in force.
    """
    return float(model_point()["av_pp_init"])


def av_pp_prev_anniv_init():
    """AV_anniv(y) of the contract year under way: its base at the valuation date.

    The Account Value **before** withdrawals at the Contract Anniversary on or before the
    valuation date, ``av_pp_at(12 cy - 1, "BEF_WD")`` in ``RILA_US_S``, which
    :func:`free_wd_base` reads where that anniversary month precedes :func:`t_entry`: the
    Free Withdrawal Amount of the year under way is ``free_wd_rate`` times it. The
    purchase payment in the first contract year, which opened at issue; 0 on a point not
    yet in force. Where the anniversary month is in the frame, the valuation month being
    the last of its contract year, the projection reads the frame instead.
    """
    return float(model_point()["av_pp_prev_anniv_init"])


def free_wd_remain_init():
    """FW entering month 0: the Free Withdrawal Amount still unused in the contract year.

    ``RILA_US_S``'s ``free_wd_remain`` of the month before the valuation month, which
    :func:`free_wd_avail` carries from :func:`t_entry` until the next anniversary resets
    it. An allowance's remainder, not an accumulator, so it takes no ``_ytd``. 0 in the
    first contract year, which has no free amount, and on a point not yet in force;
    :func:`proj_len` holds it to the year's allowance.
    """
    return float(model_point()["free_wd_remain_init"])


def rop_pp_init():
    """ROP entering month 0: the return-of-premium death benefit base at the valuation date.

    The purchase payment reduced proportionally by every withdrawal before the valuation
    month, read at :func:`t_entry` on a contract in force by :func:`rop_pp`; at most the
    purchase payment, and 0 on a point not yet in force.
    """
    return float(model_point()["rop_pp_init"])


def index_at_term_start_init():
    """I_s of a term begun before the valuation month: its Term Start Date index level.

    A fact frozen at a past date, which no scenario re-based to the valuation date holds,
    so :func:`index_at_term_start` reads it from the model point wherever the term in
    force began before :func:`t_entry`. Given exactly there, and blank on every other
    point, where the term in force starts at or after the valuation month and its index
    is the scenario's; ``Data`` holds it above 0, since :func:`index_perf` divides by it.
    A blank column reads as NaN here, and no cell reads it.
    """
    return float(model_point()["index_at_term_start_init"])


def mvr_at_term_start_init():
    """r_0 of a term begun before the valuation month: its Term Start Date MVR.

    Read by :func:`mvr_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1.
    """
    return float(model_point()["mvr_at_term_start_init"])


def risk_free_at_term_start_init():
    """The risk-free rate on the Term Start Date of a term begun before ``t = 0``.

    One of the three option-pricing inputs fixed at the term's start, read by
    :func:`risk_free_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1. The budget, the amortized budget and the
    cap solve price under it.
    """
    return float(model_point()["risk_free_at_term_start_init"])


def div_yield_at_term_start_init():
    """The dividend yield on the Term Start Date of a term begun before ``t = 0``.

    Read by :func:`div_yield_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above -1.
    """
    return float(model_point()["div_yield_at_term_start_init"])


def impl_vol_at_term_start_init():
    """The implied volatility on the Term Start Date of a term begun before ``t = 0``.

    Read by :func:`impl_vol_at_term_start`, and given exactly where
    :func:`index_at_term_start_init` is; above 0.
    """
    return float(model_point()["impl_vol_at_term_start_init"])


def cap_rate_init():
    """c of a term begun at a renewal under ``nge_reset`` before the valuation month.

    The cap :func:`declared_cap_solved` re-solved at that renewal's Term Start Date and
    :func:`cap_rate` floored at the guaranteed minimum: a contractual fact fixed then,
    from the market and the References of that date, which a sensitivity run that changes
    ``earned_rate``, ``nge_spread`` or the market at the valuation date must not move.
    :func:`cap_rate` reads it for the rest of that term. Given exactly on a capped Cap
    Rate option under ``nge_reset`` whose term in force began at a renewal before the
    valuation month, and blank everywhere else: off ``nge_reset``, and in the initial
    term, the cap is the model point's declared cap, and a renewal at or after the
    valuation month re-solves from the scenario. ``Data`` holds it at or above the term's
    guaranteed minimum cap.
    """
    return float(model_point()["cap_rate_init"])


def is_uncapped():
    """True when the model point leaves ``declared_cap`` blank [S2]."""
    return bool(pd.isna(model_point()["declared_cap"]))              # noqa: F821


def policy_term():
    """Years from issue to the Maturity Date [S2].

    The later of the anniversary after the oldest owner's 90th birthday and ten years from
    issue, read on the ANB attained age **[std]**: 30 years at issue age 60, 10 at 80 or
    above.
    """
    return max(maturity_age - age_at_entry(), maturity_min_years)    # noqa: F821


def maturity_mth():
    """The policy month at which cover ends: ``12 * policy_term()``.

    The Maturity Date closes policy month ``maturity_mth() - 1``, so this is the
    ``duration_mth`` of the first month not covered: 360 at issue age 60, 120 at 80 or
    above. It is ``RILA_US_S``'s frame length, counted from issue on the policy clock;
    :func:`proj_len` counts from the valuation date instead.
    """
    return 12 * policy_term()


def proj_len():
    """The number of months from the valuation date to the Maturity Date.

    ``maturity_mth() - duration_mth_init()``: 360 for the anchor cell issued at ``t = 0``,
    289 for it in force 71 months, 1 for the notional family in its last covered month,
    and 373 for the anchor issued 13 months after the valuation date. The frame is
    ``t = 0, 1, ..., proj_len() - 1``; ``proj_len()`` is its exclusive end and the row
    count of :func:`result_cf`, and ``proj_len() - 1`` is the last covered month, the one
    ending on the Maturity Date.

    Two rules of the product, which need ``Projection`` References that ``Data`` cannot
    read, are checked here, in turn, each raising ``ValueError`` naming the point:

    * a point at or past its Maturity Date at the valuation date has no frame, and is
      refused rather than projecting nothing: an in-force extract should not carry it;
    * from the second contract year, ``duration_mth_init()`` 12 or more, the Free
      Withdrawal Amount still unused, :func:`free_wd_remain_init`, is at most the year's,
      ``free_wd_rate`` times :func:`av_pp_prev_anniv_init`, to a cent, the year's
      withdrawals only ever reducing it. The rule holds where that base is 0 or more, and
      is not applied below 0: on a negative base ``RILA_US_S``'s allowance is negative,
      and a behavioural rate above ``free_wd_rate`` then takes a withdrawal more negative
      still, which leaves a positive remainder that no allowance bounds. That is a state
      ``RILA_US_S`` reaches, on a negative interim value [S2], so it is accepted.
    """
    label = point_id                                                 # noqa: F821
    n = maturity_mth() - duration_mth_init()
    if n <= 0:
        raise ValueError(
            f"point_id {label}: duration_mth {duration_mth_init()} is at or past the "
            f"maturity date, policy month {maturity_mth()}; the contract has matured")
    if duration_mth_init() >= 12 and av_pp_prev_anniv_init() >= 0.0:
        allowance = free_wd_rate * av_pp_prev_anniv_init()           # noqa: F821
        if free_wd_remain_init() > allowance + 0.01:
            raise ValueError(
                f"point_id {label}: free_wd_remain_init {free_wd_remain_init()} is more "
                f"than the contract year's free withdrawal amount, free_wd_rate x "
                f"av_pp_prev_anniv_init, {allowance:.2f}")
    return n


def duration_mth(t):
    """Policy months elapsed at the **start** of month t: the policy clock.

    ``duration_mth_init() + t``, a closed form: 71 at ``t = 0`` for the anchor cell in
    force 71 months, 0 at ``t = 0`` for a contract issued at the valuation date, and 0 at
    ``t = 13`` for one issued 13 months later, negative before that. It is
    ``RILA_US_S``'s ``t``, and every contractual date is read on it: the terms, the
    anniversaries, the withdrawal charge, the attained age, the withdrawal programme and
    the Maturity Date. Defined in every month, before issue too.
    """
    return duration_mth_init() + t


def t_entry():
    """The first month the contract is on the books: ``max(0, -duration_mth_init())``.

    0 for a point in force at the valuation date or issued at it, ``k`` for one issued
    ``k`` months later. It is the base of every recursion: :func:`pols_if_at` opens there
    from :func:`pols_if_init`, the Investment Amount, the two accounts, the
    return-of-premium base and the free-withdrawal carry from the model point's opening
    state, and the Account Value's movement from :func:`av_pp_init`. No cell in cover
    reads a month before it, and a term or an anniversary that falls before it is read
    from the opening state.
    """
    return max(0, -duration_mth_init())


def is_active(t):
    """Whether month t is inside cover: issued, and not yet past the Maturity Date.

    ``0 <= duration_mth(t) < maturity_mth()``. False before issue and from the month after
    the one ending on the Maturity Date. Outside cover every count is zero, and so every
    cash flow; so is every value, rate and interim-value factor, but for the two surrender
    multipliers, which are 1.0, their neutral value; every flag is false, no market path
    is read, and no table is read at a contract year or an attained age the contract does
    not have.
    """
    return 0 <= duration_mth(t) < maturity_mth()


def duration(t):
    """cy(t): complete contract years elapsed at the start of month t, on the policy clock.

    lifelib's 0-based duration, ``duration_mth(t) // 12``: it is ``0`` through the whole
    of contract year 1, policy months 0 to 11, and steps to 1 at policy month 12. It is
    the *interval* reading of the contract year - the year the whole of month ``t`` lies
    inside - and so is the right one for a rate applied across the month: the attained age
    behind ``q_m(t)`` (:func:`age`). For a transaction settling at the month **end**, one
    instant later, use :func:`duration_eom`; the two differ only in the month that closes
    on an anniversary. Before issue it is negative, which is why no cell calls it outside
    cover. Expense inflation runs on the valuation clock instead (:func:`inflation_factor`).
    """
    return duration_mth(t) // 12


def duration_eom(t):
    """Complete contract years at the month **end** that closes month t.

    ``(duration_mth(t) + 1) // 12``, the *instant* reading, and the notes' own ``cy`` at
    that instant. Month ``t`` ends at time ``t + 1``, so the month ending on the first
    anniversary is policy month 11 and ``duration_eom`` is 1 there where :func:`duration`
    is 0. Anything settled at that instant takes this reading - the withdrawal charge a
    transaction bears (:func:`surr_charge_rate`), the free-withdrawal base snapshotted at
    the anniversary (:func:`free_wd_base`), and the surrender behaviour keyed to that
    charge (:func:`policy_year`, :func:`lapse_rate_sc_mult`), which must see the charge
    expire in the same month the contract does. No cell calls it outside cover.
    """
    return (duration_mth(t) + 1) // 12


def policy_year(t):
    """The contract year in force at the month end that closes month t, ``cy_end + 1``.

    A contractual, 1-based label on the policy clock, and the key the surrender table is
    read on. It takes the **month-end** reading ``duration_eom(t) + 1``, not the interval
    reading ``duration(t) + 1``, because the charge-expiry shock must land in the same
    month the charge a surrender settling there bears goes to zero, which is
    :func:`surr_charge_rate` on that same reading. So at policy month 11 it is 2: a
    surrender at the first anniversary already settles on the year-2 side of the
    schedule, while the mortality rate charged **over** that month is still contract year
    1's. Before issue it is 0 or below, so every call is guarded by :func:`is_active`.
    """
    return duration_eom(t) + 1


def age(t):
    """The attained age (ANB) during month t, ``x + duration(t)``, on the policy clock.

    Keyed on :func:`duration`, not :func:`duration_eom`: ``q_m(t) = 1 - (1 - q_x)^(1/12)``
    is an exposure rate for the whole of month ``t``, so all twelve months of contract
    year 1 - policy month 11, which ends on the anniversary, included - are charged at
    ``q_x`` and the attained age steps at the anniversary rather than one month before
    it. At the Maturity Date the attained age is therefore ``age(proj_len() - 1) + 1``, the
    age the contract's own rule names. Before issue it is below the issue age, so every
    call is guarded by :func:`is_active`.
    """
    return age_at_entry() + duration(t)


def is_anniv(t):
    """True when month t **ends** on a Contract Anniversary, on the policy clock.

    ``(duration_mth(t) + 1) % 12 == 0``. Month ``t`` ends at time ``t + 1``, so the first
    anniversary closes policy month 11.
    The Issue Date is not flagged: it opens policy month 0 rather than ending a month, and
    nothing the model does at an anniversary - the free-withdrawal reset, the behavioural
    withdrawal - happens there. False outside cover, where a month before issue can end on
    a multiple of 12 policy months short of it.
    """
    if not is_active(t):
        return False
    return (duration_mth(t) + 1) % 12 == 0


def term_elapsed_mth(t):
    """Months elapsed in the term of the option **in force during** month t.

    Counted at the month end on the policy clock, ``duration_mth(t) % (12T) + 1``: ``1``
    in the first month of a term and ``12T`` in the month that ends on a Term End Date -
    the expiring option, not the renewed one. Terms align with issue, so the term clock
    follows from the policy clock alone. Reading the boundary month as belonging to the
    term that is closing is what makes the term-end identity work: the replicating
    portfolio at ``tau = 0`` collapses to intrinsic value and reproduces ``g`` exactly.
    Defined in every month, but it means nothing outside cover, where no cell calls it.
    """
    return (duration_mth(t) % (12 * term_years())) + 1


def term_start_month(t):
    """The first month of the term in force during month t, as a **policy** month.

    Equivalently the Term Start Date itself as a time in policy months, since policy month
    ``m`` opens at time ``m``: ``0`` for the initial term, ``12T`` for the first renewal.
    It stays a policy month on either clock: the readers of the term-start market,
    :func:`index_at_term_start`, :func:`mvr_at_term_start` and the three option-pricing
    ones, turn it into a month from the valuation date once each, and read the opening
    state where it precedes the valuation month; :func:`cap_rate` compares it with 0 to
    find a renewal. Defined in every month, but no cell calls it outside cover.
    """
    return duration_mth(t) + 1 - term_elapsed_mth(t)


def tau(t):
    """tau_k(t): years remaining in the option's term at the end of month t.

    ``(12T - elapsed) / 12``. The notes define it as days remaining / 365 [S2]; on a
    monthly grid that is exact twelfths. ``tau(t) = 0`` at every Term End Date, and the
    term opens at ``tau = T`` - an instant, the opening of the term's first month, not a
    projected month. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return (12 * term_years() - term_elapsed_mth(t)) / 12.0


def is_term_end(t):
    """True when month t ends on a Term End Date, i.e. ``tau(t) == 0``.

    False outside cover.
    """
    if not is_active(t):
        return False
    return term_elapsed_mth(t) == 12 * term_years()


def market_state(t, name):
    """Step-function lookup of column ``name`` in the model point's market scenario.

    ``t`` is a **time** in months from the **valuation date**, ``t = 0`` at the valuation
    date, not the month index: the market state month ``t`` is valued at is
    ``market_state(t + 1, ...)``, and a term that starts at or after the valuation month
    reads the state locked on its Term Start Date at that date's time. Each row of
    *market_scenario_sec.csv* is keyed by that same ``month_end`` and states the market
    state that holds from it until the next row of the same scenario, so a flat path is
    one row. The index path is therefore piecewise constant between the scenario's own
    anchor months; that is a property of the deterministic scenario, not of the model.

    On the valuation clock, which every point of a block shares: the scenario is joined on
    the model point's ``scenario_id``, and a point restated in force or issued after the
    valuation date reads its own copy, re-based to its month. ``RILA_US_S`` keys the same
    lookup by policy month from issue, the valuation clock of a contract issued at the
    valuation date, and names its parameter ``k``; it is ``t`` here, a month on the
    valuation clock. A copy re-based to a later issue month holds no level before it, so
    a read there raises, and no cell reads it outside cover. ``Data.market_scenario_count``
    checks the file first.
    """
    data.market_scenario_count()                                     # noqa: F821
    sub = data.market_scenario().loc[model_point()["scenario_id"]]   # noqa: F821
    months = [i for i in sub.index if i <= t]
    return float(sub.loc[max(months), name])


def index_level(t):
    """I(t): the index level month t is valued at - its month end - price return [S1][S2].

    ``market_state(t + 1, "index_level")``, on the valuation clock. All representative
    indices are **price return**, which is why the dividend yield is a live pricing input:
    omitting it overprices every call in the portfolio. No cell calls it outside cover:
    before issue a future point's scenario holds no level.
    """
    return market_state(t + 1, "index_level")


def index_at_term_start(t):
    """I_s: the index level at the Term Start Date of the term in force during month t.

    The Term Start Date is the policy month :func:`term_start_month`, which is month
    ``term_start_month(t) - duration_mth_init()`` from the valuation date. Where that is
    :func:`t_entry` or later the term starts in the frame, and its index is the scenario's
    there, as in ``RILA_US_S``; where it is earlier the term began before the valuation
    month, and its index is the model point's :func:`index_at_term_start_init`, a level no
    scenario re-based to the valuation date holds. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return index_at_term_start_init()
    return market_state(k, "index_level")


def mvr(t):
    """r(t): the Market Value Rate at month t's month end, annual effective [S2].

    The Constant Maturity Treasury yield at the term's maturity, linearly interpolated
    between adjacent CMT maturities [S2]; the model takes it as an exogenous scalar series
    **[std]** rather than carrying a curve. ``market_state(t + 1, "mvr")``, on the
    valuation clock; no cell calls it outside cover.
    """
    return market_state(t + 1, "mvr")


def mvr_at_term_start(t):
    """r_0: the Market Value Rate on the Term Start Date [S2].

    Read as :func:`index_at_term_start` reads the index: the scenario's at the Term Start
    Date where that date is in the frame, the model point's
    :func:`mvr_at_term_start_init` where it precedes the valuation month. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return mvr_at_term_start_init()
    return market_state(k, "mvr")


def risk_free_at_term_start(t):
    """The risk-free rate on the Term Start Date of the term in force during month t.

    The option budget, the ``updated_expiry`` amortization and the cap solve price under
    the market of the Term Start Date, which ``RILA_US_S`` reads from its scenario at
    :func:`term_start_month` in place, in :func:`opt_component` and
    :func:`opt_budget_at_cap`. Here it is read as :func:`index_at_term_start` reads the
    index: the scenario's at that date where it is in the frame, the model point's
    :func:`risk_free_at_term_start_init` where it precedes the valuation month. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return risk_free_at_term_start_init()
    return market_state(k, "risk_free")


def div_yield_at_term_start(t):
    """The dividend yield on the Term Start Date of the term in force during month t.

    Read as :func:`risk_free_at_term_start` reads the rate, from
    :func:`div_yield_at_term_start_init` where the term began before the valuation month.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return div_yield_at_term_start_init()
    return market_state(k, "div_yield")


def impl_vol_at_term_start(t):
    """The implied volatility on the Term Start Date of the term in force during month t.

    Read as :func:`risk_free_at_term_start` reads the rate, from
    :func:`impl_vol_at_term_start_init` where the term began before the valuation month.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    k = term_start_month(t) - duration_mth_init()
    if k < t_entry():
        return impl_vol_at_term_start_init()
    return market_state(k, "impl_vol")


def risk_free(t):
    """The risk-free rate at month t's month end, annual effective, 4.00% **[std]**.

    ``market_state(t + 1, "risk_free")``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, "risk_free")


def div_yield(t):
    """q: the dividend yield at month t's month end, annual effective, 2.00% **[std]**.

    A live pricing input because every representative index is price return [S1][S2].
    ``market_state(t + 1, "div_yield")``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, "div_yield")


def impl_vol(t):
    """sigma: the implied volatility at month t's month end, 20.00% flat **[std]**.

    A flat surface is the largest single simplification in this model. AG 54 requires
    assumptions "consistent with the observable market prices of derivative assets over
    the Index Strategy Term, whenever possible" [R2], and a production implementation must
    supply a surface interpolated in both maturity and moneyness [S4]; that is a change to
    *market_scenario_sec.csv* plus a lookup, not to any formula here.
    ``market_state(t + 1, "impl_vol")``, on the valuation clock; no cell calls it outside
    cover.
    """
    return market_state(t + 1, "impl_vol")


def index_perf(t):
    """R_k(t): index performance to date, ``I(t) / I_s - 1``.

    At a Term End Date this is the crediting input; the cap applies to the **whole-term**
    return, never annually on a 3 or 6 year term [S5]. ``I_s`` is the model point's for a
    term begun before the valuation month (:func:`index_at_term_start`), held above 0 by
    ``Data``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return index_level(t) / index_at_term_start(t) - 1.0


def norm_cdf(x):
    """N(x): the standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))                # noqa: F821


def bs_d1(spot, strike, tau_, rate, divy, vol):
    """Black-Scholes d1.

    ``[ln(I/K) + (r_cc - q_cc + sigma^2/2) tau] / (sigma sqrt(tau))``. ``rate`` and
    ``divy`` are **annual effective** and are converted to continuous compounding here, so
    the 4.00% and 2.00% market inputs enter as ``ln 1.04 = 3.9221%`` and
    ``ln 1.02 = 1.9803%`` exactly as the notes state.
    """
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    return ((math.log(spot / strike)                                 # noqa: F821
             + (rate_cc - divy_cc + vol ** 2 / 2.0) * tau_)
            / (vol * math.sqrt(tau_)))                               # noqa: F821


def bs_d2(spot, strike, tau_, rate, divy, vol):
    """Black-Scholes d2, ``d1 - sigma sqrt(tau)``."""
    return (bs_d1(spot, strike, tau_, rate, divy, vol)
            - vol * math.sqrt(tau_))                                 # noqa: F821


def bs_call(spot, strike, tau_, rate, divy, vol):
    """C(I, K, tau): the European call, ``I e^(-q tau) N(d1) - K e^(-r tau) N(d2)``.

    At ``tau = 0`` it returns the intrinsic value ``max(I - K, 0)``, which is what makes
    the replicating portfolio collapse to the crediting rate at term end.
    """
    if tau_ <= 0.0:
        return max(spot - strike, 0.0)
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    d_1 = bs_d1(spot, strike, tau_, rate, divy, vol)
    d_2 = bs_d2(spot, strike, tau_, rate, divy, vol)
    return (spot * math.exp(-divy_cc * tau_) * norm_cdf(d_1)         # noqa: F821
            - strike * math.exp(-rate_cc * tau_) * norm_cdf(d_2))    # noqa: F821


def bs_put(spot, strike, tau_, rate, divy, vol):
    """P(I, K, tau): the European put, ``K e^(-r tau) N(-d2) - I e^(-q tau) N(-d1)``.

    At ``tau = 0`` it returns the intrinsic value ``max(K - I, 0)``.
    """
    if tau_ <= 0.0:
        return max(strike - spot, 0.0)
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    divy_cc = math.log(1.0 + divy)                                   # noqa: F821
    d_1 = bs_d1(spot, strike, tau_, rate, divy, vol)
    d_2 = bs_d2(spot, strike, tau_, rate, divy, vol)
    return (strike * math.exp(-rate_cc * tau_) * norm_cdf(-d_2)      # noqa: F821
            - spot * math.exp(-divy_cc * tau_) * norm_cdf(-d_1))     # noqa: F821


def bs_binary_call(spot, strike, tau_, rate, divy, vol):
    """BC(I, K, tau): the cash-or-nothing binary call paying 1, ``e^(-r tau) N(d2)``.

    At ``tau = 0`` it pays 1 when ``I >= K`` and 0 below. That discontinuity is
    contractual, not an artifact: a Step design pays the full step at ``R = 0.00%`` and
    zero at ``R = -0.01%`` [S4], and the binary option is what makes the interim value
    track it. Do not smooth it.
    """
    if tau_ <= 0.0:
        return 1.0 if spot >= strike else 0.0
    rate_cc = math.log(1.0 + rate)                                   # noqa: F821
    return (math.exp(-rate_cc * tau_)                                # noqa: F821
            * norm_cdf(bs_d2(spot, strike, tau_, rate, divy, vol)))


def guar_min_rate(kind):
    """The contractual minimum declared rate for the model point's term [S1][S2].

    2% / 6% / 8% for the Cap at 1 / 3 / 6 years and 2% for the Step and the Edge. These
    are **guaranteed elements** in ASOP No. 2 terms, so every renewal-rate assumption is
    floored here [R5][REG-R26]; the floor mechanically raises the option budget and
    compresses the spread, which is why the table is a genuine tail exposure. The table's
    one reader: it asks ``Data.guar_min_rate_count`` first, so a projection meets the
    table's checks before it reads a floor, and ``Data`` refuses a point whose term the
    table lacks.
    """
    data.guar_min_rate_count()                                       # noqa: F821
    row = data.guar_min_rate_table().loc[term_years()]                # noqa: F821
    if kind == "CAP":
        return float(row["guar_min_cap"])
    elif kind == "STEP":
        return float(row["guar_min_step"])
    elif kind == "EDGE":
        return float(row["guar_min_edge"])
    else:
        raise ValueError("invalid kind")


def opt_budget_target():
    """beta_target(T) = ``1 - (1 + y_e - spread)^(-T)``: the NGE cap-solve target **[std]**.

    ``y_e`` is the projected earned rate on supporting assets and ``spread`` the target
    margin, **[std]** 2.22% - the level implied by the snapshot 6-year cap, which opens
    its fixed leg at an equivalent accretion yield of 1.7834% against a 4.00% market rate.
    """
    return 1.0 - (1.0 + earned_rate - nge_spread) ** (-term_years())  # noqa: F821


def opt_budget_at_cap(t, cap):
    """The per-unit replicating portfolio value at term start for a trial Cap Rate.

    The cap-solve needs the portfolio as a function of ``c`` while :func:`cap_rate` is
    what the rest of the model reads, so this cell recomputes the BUFFER + CAP + PR
    portfolio directly rather than calling :func:`opt_portfolio`, which would close a
    cycle. It is monotonically increasing in ``cap``. The market is the Term Start
    Date's, through :func:`risk_free_at_term_start`, :func:`div_yield_at_term_start` and
    :func:`impl_vol_at_term_start`, where ``RILA_US_S`` reads its scenario at
    :func:`term_start_month` in place. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    i_s = index_at_term_start(t)
    tau_ = float(term_years())
    pr = participation()
    rate = risk_free_at_term_start(t)
    divy = div_yield_at_term_start(t)
    vol = impl_vol_at_term_start(t)
    atm = pr * bs_call(i_s, i_s, tau_, rate, divy, vol) / i_s
    otm = pr * bs_call(i_s, i_s * (1.0 + cap / pr), tau_, rate, divy, vol) / i_s
    otp = bs_put(i_s, i_s * (1.0 - buffer()), tau_, rate, divy, vol) / i_s
    return atm - otm - otp


def declared_cap_solved(t):
    """The Cap Rate solving ``Pi(c; b, T, sigma, r, q) = beta_target(T)`` **[std]**.

    The ASOP No. 2 determination rule the notes state for redetermining the declared cap
    at each Term Start Date [R5]. Solved by bisection because the portfolio value is
    monotone in ``c`` and no root finder may be imported; ``nge_solve_iter`` bisections of
    ``[0, nge_cap_search_max]`` reach machine precision on a rate. The result is floored
    at the contractual minimum by :func:`cap_rate`, not here. A term that began at a
    renewal before the valuation month carries its solved cap on the model point instead,
    :func:`cap_rate_init`, and this cell is not read for it. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    target = opt_budget_target()
    lo, hi = 0.0, nge_cap_search_max                                 # noqa: F821
    for _ in range(nge_solve_iter):                                  # noqa: F821
        mid = 0.5 * (lo + hi)
        if opt_budget_at_cap(t, mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def cap_rate(t):
    """c: the Cap Rate in force for the term containing month t, floored at the minimum.

    The snapshot declared cap on the initial term; on a renewal term either the same
    snapshot (the notes' base projection holds the scale level) or, with ``nge_reset``,
    the solved cap - in both cases floored at the guaranteed minimum [S2]. Returns
    ``math.inf`` for an uncapped option, which makes ``min(PR R, c)`` the uncapped payoff
    and switches the out-of-the-money call off in :func:`opt_component` [S2].

    A renewal under ``nge_reset`` whose Term Start Date precedes the valuation month was
    re-solved then, on the market of that date, so its cap is the model point's
    :func:`cap_rate_init` for the rest of the term; one at or after the valuation month
    re-solves from the scenario, as ``RILA_US_S`` does. The renewal is read on the policy
    clock: :func:`term_start_month` above 0. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_uncapped():
        return math.inf                                              # noqa: F821
    if nge_reset() and term_start_month(t) > 0:
        if term_start_month(t) - duration_mth_init() < t_entry():
            return cap_rate_init()
        return max(guar_min_rate("CAP"), declared_cap_solved(t))
    return max(guar_min_rate("CAP"), declared_cap())


def step_rate(t):
    """s: the Step Rate in force, floored at the 2% contractual minimum [S2].

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return max(guar_min_rate("STEP"), declared_step())


def edge_rate(t):
    """e: the Edge Rate in force, floored at the 2% contractual minimum [S2].

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return max(guar_min_rate("EDGE"), declared_edge())


def opt_legs():
    """The legs of the replicating portfolio for the model point's crediting type.

    Cap: at-the-money call, out-of-the-money call, out-of-the-money put [S2][S3][S5][S6].
    Step: step-scaled at-the-money binary call, out-of-the-money put [S2][S5]. Edge: the
    binary call is struck at ``I_s(1 - b)`` and is therefore **in the money**, because it
    pays when the index ratio is at or above ``1 - b`` [S2][S5]. Floor needs **four**
    options, not three - buy the at-the-money call spread, sell an at-the-money put, and
    buy back an out-of-the-money put struck at the floor so the short put exposure stops
    there [S5]. The crediting type is read through its four decodes,
    :func:`is_cap_crediting` and the three beside it; a type none knows raises
    ``RILA_US_S``'s message.
    """
    if is_cap_crediting():
        return ("ATM_CALL", "OTM_CALL", "OTM_PUT")
    elif is_step_crediting():
        return ("STEP_BINARY", "OTM_PUT")
    elif is_edge_crediting():
        return ("EDGE_BINARY", "OTM_PUT")
    elif is_floor_crediting():
        return ("ATM_CALL", "OTM_CALL", "ATM_PUT", "FLOOR_PUT")
    else:
        raise ValueError("invalid crediting_type")


def opt_component(t, leg, spot, tau_, mkt):
    """The **signed** value of one replicating-portfolio leg, per unit of notional.

    Each option's notional is the Investment Amount [S4], and every strike is set from the
    Term Start Date index level ``I_s``, so dividing by ``I_s`` makes each leg
    dimensionless and the portfolio a fraction of notional. ``mkt`` selects the market
    state: ``"CURRENT"`` prices at month ``t``'s month end, time ``t + 1`` on the
    valuation clock, and ``"TERM_START"`` under the initial market conditions of the term
    in force - its Term Start Date - which is what the option budget and the
    ``updated_expiry`` amortization need. The Term Start Date's market is read through
    :func:`risk_free_at_term_start`, :func:`div_yield_at_term_start` and
    :func:`impl_vol_at_term_start`, from the model point where the term began before the
    valuation month.

    The participation rate multiplies the call spread and re-strikes the short call at
    ``I_s(1 + c/PR)`` [S4]; at ``PR = 1`` that is exactly the plain Cap portfolio, so one
    branch serves both of the notes' first two rows. An uncapped option values the
    out-of-the-money call at zero [S2]. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if mkt == "CURRENT":
        k = t + 1
        rate = market_state(k, "risk_free")
        divy = market_state(k, "div_yield")
        vol = market_state(k, "impl_vol")
    elif mkt == "TERM_START":
        rate = risk_free_at_term_start(t)
        divy = div_yield_at_term_start(t)
        vol = impl_vol_at_term_start(t)
    else:
        raise ValueError("invalid mkt")
    i_s = index_at_term_start(t)
    pr = participation() if is_cap_crediting() else 1.0
    if leg == "ATM_CALL":
        return pr * bs_call(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == "OTM_CALL":
        cap = cap_rate(t)
        if math.isinf(cap):                                          # noqa: F821
            return 0.0
        strike = i_s * (1.0 + cap / pr)
        return -pr * bs_call(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "OTM_PUT":
        strike = i_s * (1.0 - buffer())
        return -bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "ATM_PUT":
        return -bs_put(spot, i_s, tau_, rate, divy, vol) / i_s
    elif leg == "FLOOR_PUT":
        strike = i_s * (1.0 - floor_rate())
        return bs_put(spot, strike, tau_, rate, divy, vol) / i_s
    elif leg == "STEP_BINARY":
        return step_rate(t) * bs_binary_call(spot, i_s, tau_, rate, divy, vol)
    elif leg == "EDGE_BINARY":
        strike = i_s * (1.0 - buffer())
        return edge_rate(t) * bs_binary_call(spot, strike, tau_, rate, divy, vol)
    else:
        raise ValueError("invalid leg")


def opt_portfolio(t, spot, tau_, mkt):
    """Pi(I, tau): the per-unit market value of the replicating option portfolio.

    The sum of the signed legs. **Verification identity**: at ``tau = 0`` this collapses
    to the crediting rate ``g`` for every crediting type - for the Cap design
    ``max(R,0) - max(R-c,0) - max(-b-R,0) = g``. If the interim value at term end does not
    reproduce ``IA(1 + g)`` exactly, the strike set or the notional convention is wrong;
    :func:`check_term_end_identity` tests it.
    """
    return sum(opt_component(t, leg, spot, tau_, mkt) for leg in opt_legs())


def opt_portfolio_abs(t, spot, tau_, mkt):
    """The sum of the **absolute** leg values: the trading cost assessment base **[std]**.

    A wider base than the Academy's net derivative value [R6], deliberately, because no
    prospectus quantifies the trading cost provision; the base must be stated whenever the
    factor is recalibrated.
    """
    return sum(abs(opt_component(t, leg, spot, tau_, mkt)) for leg in opt_legs())


def opt_budget(t):
    """beta: the initial option budget per unit of notional, ``Pi(I_s, T)``.

    Struck at each Term Start Date under the market conditions of that date. On the anchor
    cell ``beta = 10.0632%``, so the option budget is $10,063.19 of a $100,000 Investment
    Amount and the fixed leg opens at $89,936.81. A term that began before the valuation
    month prices it from the model point's term-start market, so the budget is the one
    struck then. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return opt_portfolio(t, index_at_term_start(t), float(term_years()), "TERM_START")


def fixed_leg_yield(t):
    """The equivalent geometric accretion yield on the fixed leg, ``(1-beta)^(-1/T) - 1``.

    1.7834% on the anchor cell: the rate at which $89,936.81 accretes to $100,000 over six
    years. The gap to the 4.00% market rate is :func:`nge_spread_implied`. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return (1.0 - opt_budget(t)) ** (-1.0 / term_years()) - 1.0


def nge_spread_implied(t):
    """The spread implied by the declared cap: ``earned rate - fixed leg yield``.

    2.22% on the anchor cell, and that is the **[std]** ``nge_spread`` input to the
    cap-solve rule - the model's own snapshot, read back out of the snapshot cap. 0.0
    outside cover.
    """
    if not is_active(t):
        return 0.0
    return earned_rate - fixed_leg_yield(t)                          # noqa: F821


def credit_rate_at(t, accrual):
    """g: the crediting rate applied to R(t), with the declared rates scaled by ``accrual``.

    ``accrual = 1`` is the contractual term-end rule [S1][S2][S4][S5]::

        BUFFER + CAP    g = min(PR R, c)      if R >= 0;  g = min(0, R + b)  if R < 0
        BUFFER + STEP   g = s                 if R >= 0;  g = min(0, R + b)  if R < 0
        BUFFER + EDGE   g = e                 if R >= -b; g = R + b          if R < -b
        FLOOR  + CAP    g = min(max(R, -f), c)

    The ``min(0, .)`` in the buffer branch is load-bearing: the Performance Rate can never
    be greater than zero if the Index Performance is negative [S1]. The discontinuities -
    a Step design paying the full step at ``R = 0.00%`` and zero at ``R = -0.01%``, an
    Edge design flipping at the buffer edge - are contractual; do not smooth them [S2][S4].

    ``accrual < 1`` is the **pre-AG 54** design [S1], which uses no option pricing at all:
    the buffer, Cap and Step Rates each accrue linearly over the term and the term-end
    rules are applied to the accrued rates. The crediting type is read through its four
    decodes, and a type none knows raises ``RILA_US_S``'s message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    perf = index_perf(t)
    buff = buffer() * accrual
    if is_cap_crediting():
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(participation() * perf, cap) if perf >= 0.0 else min(0.0, perf + buff)
    elif is_step_crediting():
        return step_rate(t) * accrual if perf >= 0.0 else min(0.0, perf + buff)
    elif is_edge_crediting():
        edge = edge_rate(t) * accrual
        return edge if perf >= -buff else perf + buff
    elif is_floor_crediting():
        cap = cap_rate(t)
        cap = cap if math.isinf(cap) else cap * accrual              # noqa: F821
        return min(max(perf, -floor_rate() * accrual), cap)
    else:
        raise ValueError("invalid crediting_type")


def credit_rate_term(t):
    """g at a Term End Date, zero in every other month.

    Applied as ``IA_k(term end) = IA_k(term start, adjusted for withdrawals) x (1 + g)``
    [S1][S2].
    """
    return credit_rate_at(t, 1.0) if is_term_end(t) else 0.0


def credit_rate_accrued(t):
    """The pre-AG 54 time-prorated crediting rate at month t [S1].

    ``credit_rate_at(t, elapsed / total)``, on the term clock :func:`term_elapsed_mth`
    reads from the policy clock. The source worked example - $50,000, a 10% buffer, a 10%
    Cap on a one-year term, index 500 to 600 at day 183 - gives an accrued cap of 5%, a 5%
    Performance Rate and an interim value of $52,500; on a monthly grid the sixth month
    end of twelve is exactly half the term, and that is the end of policy month 5, so the
    model reproduces it to the cent.
    """
    return credit_rate_at(t, 1.0 - tau(t) / term_years())


def budget_amort_factor(t):
    """B_k(t) / IA_k(t): the amortized initial option budget, per unit of notional.

    ``straight_line`` **[std]** [S2] gives ``beta x tau/T``; ``updated_expiry`` [S3] gives
    the initial-market-conditions portfolio value re-read at the current time to expiry.
    Both are forced to zero at ``tau = 0``, which is AG 54's boundary condition and what
    makes ``V = IA(1 + g)`` exact at term end.

    **This is where homogeneity is imposed.** ``B`` is defined against the *current*
    ``IA``, so every term of the interim value scales with the notional and a withdrawal
    reduces the interim value by exactly the cash removed. Freezing ``B`` at the
    term-start notional instead would make the contract silently gain or lose value on
    every withdrawal. The rule is read through its two decodes, :func:`is_straight_line`
    and :func:`is_updated_expiry`, and a rule neither knows raises ``RILA_US_S``'s
    message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if tau(t) <= 0.0:
        return 0.0
    if is_straight_line():
        return opt_budget(t) * tau(t) / term_years()
    elif is_updated_expiry():
        return opt_portfolio(t, index_at_term_start(t), tau(t), "TERM_START")
    else:
        raise ValueError("invalid amort_rule")


def mva_factor(t):
    """``[(1 + r_0) / (1 + r(t))]^tau``: the interim value's interest-rate adjustment [S2].

    The only market-value-adjustment-like term in the contract, and it lives **inside**
    the interim value rather than on the surrender benefit - this product has no contract
    MVA. At the worked-example parameters a 100 bp rise costs $2,687.62 of interim value
    at the term midpoint, two orders of magnitude more than the entire trading-cost
    provision. Family (c) has no such term at all [S5], so the choice of interim-value
    family is itself a rate-sensitivity assumption. ``r_0`` is the model point's for a term
    begun before the valuation month (:func:`mvr_at_term_start`). 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return ((1.0 + mvr_at_term_start(t)) / (1.0 + mvr(t))) ** tau(t)


def fixed_proxy_factor(t):
    """F_k(t) / IA_k(t): the Fixed Income Asset Proxy, per unit of notional.

    ``portfolio`` **[std]**: ``(1 - B/IA) x mva_factor`` - AG 54's hypothetical bond,
    starting at base less the derivative proxy and accreting to the base at unchanged
    yield [R2][S2]. ``notional``: the **full** notional discounted at an investment-grade
    rate, risk-free plus ``iv_credit_spread`` = **[std]** 1.00%, with no subtraction of an
    option budget [S4][S6]. No source quantifies that spread - [S4] says only that the
    rate is investment-grade, above swap rates, and therefore "will result in a lower
    value for that component" - so the 1.00% is a standardization on the same footing as
    ``iv_expense_rate``, and family (b)'s interim value moves with it. ``delta``:
    ``1 - B/IA``, the notional plus the amortization term, with no rate adjustment [S5].
    The family is read through its four decodes, :func:`is_iv_portfolio` and the three
    beside it, and a family none knows raises ``RILA_US_S``'s message. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_portfolio():
        return (1.0 - budget_amort_factor(t)) * mva_factor(t)
    elif is_iv_notional():
        return (1.0 + risk_free(t) + iv_credit_spread) ** (-tau(t))  # noqa: F821
    elif is_iv_delta():
        return 1.0 - budget_amort_factor(t)
    elif is_iv_legacy():
        return 0.0
    else:
        raise ValueError("invalid iv_family")


def deriv_proxy_factor(t):
    """D_k(t) / IA_k(t): the Derivative Asset Proxy, ``Pi(I(t), tau(t))``.

    Valued at the current market state, on the valuation clock. The pre-AG 54 ``legacy``
    engine has no derivative proxy at all - it uses no option pricing. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_legacy():
        return 0.0
    return opt_portfolio(t, index_level(t), tau(t), "CURRENT")


def trading_cost_factor(t):
    """TC_k(t) / IA_k(t): the trading cost provision, ``kappa x sum |leg values|``.

    Strictly interior to the term: ``kappa_effective = kappa x 1{tau > 0}`` **[std]**.
    There are no options left to exit at term end, the Academy example likewise shows no
    trading cost there [R6], and leaving the provision switched on at ``tau = 0`` breaks
    the term-end verification identity by ``kappa x IA x |g|``. Only family (a) carries
    it; family (b) has an always-positive expense rebate instead [S4] and family (c)
    states none [S5]. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if not is_iv_portfolio() or tau(t) <= 0.0:
        return 0.0
    return trading_cost_rate * opt_portfolio_abs(                    # noqa: F821
        t, index_level(t), tau(t), "CURRENT")


def cap_calc_factor(t):
    """CCF_k(t) / IA_k(t): the Cap Calculation Factor of family (b) [S4].

    ``E_0 x tau/T`` - "a return of estimated expenses for the portion of the Segment
    Duration that has not elapsed", always positive and declining to zero at term end;
    the source works it as $10 of estimated expenses on a one-year segment giving $6 with
    219 days remaining. ``E_0`` is expressed here as a rate of notional,
    ``iv_expense_rate`` = **[std]** 0.10%, because no source quantifies it - the same
    standing as family (b)'s other free parameter, ``iv_credit_spread``. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if not is_iv_notional():
        return 0.0
    return iv_expense_rate * tau(t) / term_years()                   # noqa: F821


def iv_factor(t):
    """V_k(t) / IA_k: the interim value per unit of the month's **opening** notional.

    ``F + D - TC + CCF`` for the three AG 54-era families, and ``1 + g_accrued`` for the
    pre-AG 54 one. Two boundaries fall out of the algebra rather than being imposed: at
    ``tau = T`` the fixed and derivative legs sum to exactly 1, which is AG 54's
    requirement that the Index Strategy Base equal the Strategy Value at term start [R2];
    at ``tau = 0`` they sum to ``1 + g``, which is the term-end Strategy Value.

    ``tau = T`` is an instant - the opening of the term's first month - and not a
    projected month, so no row of the frame carries it; the interim value is **undefined**
    at term start and term end alike, those points being Strategy Values rather than
    Interim Values [R6]. At a Term End Date, which *is* a month end, :func:`iv_ratio`
    returns 1 for the Transfer Period [S2] rather than this factor. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if is_iv_legacy():
        return 1.0 + credit_rate_accrued(t)
    return (fixed_proxy_factor(t) + deriv_proxy_factor(t)
            - trading_cost_factor(t) + cap_calc_factor(t))


def iv_ratio(t):
    """V_k(t) / IA_k(t): the interim value per unit of the **current** notional.

    1 at a Term End Date, where the Investment Amount has just been credited and the
    interim value equals it for the Transfer Period [S2]; the interim value factor
    otherwise. Multiplying by this is how homogeneity is carried through the model: the
    same ratio serves before and after a withdrawal, so the interim value falls by exactly
    the cash removed.
    """
    return 1.0 if is_term_end(t) else iv_factor(t)


def inv_amt_basis_pp(t):
    """IA_k: the notional the month-t valuation applies to, per contract.

    The Investment Amount **entering** month ``t``: the prior month's Investment Amount
    after the month the contract enters the books, :func:`t_entry`. In that month it is
    the opening state: the whole purchase payment in the issue month of a contract issued
    at or after the valuation date - the anchor cell allocates 100% to one 6-year option,
    and the payment falls at the opening of that month - and the model point's
    :func:`inv_amt_pp_init` on a contract in force. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        return inv_amt_pp(t - 1)
    if duration_mth(t) == 0:
        return premium_pp()
    return inv_amt_pp_init()


def iv_notional_pp(t, timing):
    """The notional an interim-value decomposition column is measured on.

    ``"BEF_ROLL"`` is the opening notional, the one in force during month ``t`` before the
    roll split - the notes' rows A1, B1, A2 and B3. ``"AFT_WD"`` is the notional after
    the proportional withdrawal reduction - the notes' row B2, in which **every** component
    of the interim value scales by the same factor, which is exactly why the interim value
    then falls by precisely the cash withdrawn.
    """
    if timing == "BEF_ROLL":
        return inv_amt_basis_pp(t)
    elif timing == "AFT_WD":
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def opt_component_pp(t, leg, timing="BEF_ROLL"):
    """The currency value of one replicating-portfolio leg, per contract.

    The notional at ``timing`` times the per-unit leg value at the current market state.
    These are the worked example's ATM call, OTM call and OTM put columns. 0.0 outside
    cover, where no market path is read.
    """
    if not is_active(t):
        return 0.0
    return iv_notional_pp(t, timing) * opt_component(
        t, leg, index_level(t), tau(t), "CURRENT")


def fixed_proxy_pp(t, timing="BEF_ROLL"):
    """F_k(t): the Fixed Income Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * fixed_proxy_factor(t)


def budget_amort_pp(t, timing="BEF_ROLL"):
    """B_k(t): the amortized initial option budget in currency, per contract."""
    return iv_notional_pp(t, timing) * budget_amort_factor(t)


def deriv_proxy_pp(t, timing="BEF_ROLL"):
    """D_k(t): the Derivative Asset Proxy in currency, per contract."""
    return iv_notional_pp(t, timing) * deriv_proxy_factor(t)


def trading_cost_pp(t, timing="BEF_ROLL"):
    """TC_k(t): the trading cost provision in currency, per contract."""
    return iv_notional_pp(t, timing) * trading_cost_factor(t)


def inv_amt_pp_at(t, timing):
    """IA_k: the Investment Amount per contract, read at a point inside month t.

    ``"BEF_CREDIT"`` is the opening notional, :func:`inv_amt_basis_pp`, whose opening on
    a contract in force is the model point's; ``"BEF_ROLL"`` applies term-end crediting;
    ``"BEF_WD"`` applies the renewal / transfer roll split; ``"AFT_WD"`` applies the
    proportional withdrawal reduction. Outside a Term End Date the first three coincide.
    """
    if timing == "BEF_CREDIT":
        return inv_amt_basis_pp(t)
    elif timing == "BEF_ROLL":
        return inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
    elif timing == "BEF_WD":
        rolled = inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t))
        return rolled * roll_share("OPTION") if is_term_end(t) else rolled
    elif timing == "AFT_WD":
        return inv_amt_pp(t)
    else:
        raise ValueError("invalid timing")


def inv_amt_pp(t):
    """IA_k(t): the Investment Amount (AG 54 Index Strategy Base) at end of month t.

    Term-end crediting, then the roll split, then **the universal proportional rule**::

        IA_k(t+) = IA_k(t-) x (1 - G_k / V_k(t-))

    Every insurer in the sample reduces the notional in proportion to the reduction in
    interim value, not dollar for dollar [S2][S3][S4][S6], and the reduction in notional
    therefore **exceeds the cash received** whenever the interim value is below the
    notional - by ``G (IA/V - 1)``, $1,433.62 on the worked example's $8,000 withdrawal.
    Modelling withdrawals as dollar-for-dollar reductions overstates the remaining
    notional in down markets and compounds through the rest of the term.

    The rule is undefined at a non-positive interim value, which this contract can produce
    [S2]; the model then leaves the notional unreduced **[std]**, the withdrawal having
    been allocated away from the option by :func:`wd_alloc_pp`.

    The opening is written inline, as :func:`inv_amt_basis_pp` gives it - the prior
    month's amount after :func:`t_entry`, the purchase payment in the issue month, the
    model point's :func:`inv_amt_pp_init` on a contract in force - so the chain of calls
    back to :func:`t_entry` is one cell a month, where ``RILA_US_S``'s runs through
    :func:`inv_amt_pp_at` and :func:`inv_amt_basis_pp`; the arithmetic, the crediting and
    the roll split are ``RILA_US_S``'s, bit for bit. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        opening = inv_amt_pp(t - 1)
    elif duration_mth(t) == 0:
        opening = premium_pp()
    else:
        opening = inv_amt_pp_init()
    rolled = opening * (1.0 + credit_rate_term(t))
    base = rolled * roll_share("OPTION") if is_term_end(t) else rolled
    value = interim_value_pp_at(t, "BEF_WD")
    if value <= 0.0:
        return base
    return base * (1.0 - wd_alloc_pp(t, "OPTION") / value)


def interim_value_pp_at(t, timing):
    """V_k: the Interim Value per contract, read at a point inside month t.

    ``"BEF_ROLL"`` is the worked example's Interim value column - the value at month
    ``t``'s month end of the option in force during it, after any term-end crediting and
    before the roll split.
    ``"BEF_WD"`` and ``"AFT_WD"`` are that value carried through the roll split and the
    withdrawal, each as the Investment Amount at that point times :func:`iv_ratio`.

    Every mid-term transaction settles here: withdrawal, surrender, death benefit,
    annuitization, transfer and any fee deduction [S1][S2][S4][S6]. It can be **negative
    even when the index is up** [S2]; flooring it at zero, or at the notional, is not
    implementing the contract.
    """
    if timing == "BEF_ROLL":
        return inv_amt_basis_pp(t) * iv_factor(t)
    elif timing == "BEF_WD":
        return inv_amt_pp_at(t, "BEF_WD") * iv_ratio(t)
    elif timing == "AFT_WD":
        return inv_amt_pp(t) * iv_ratio(t)
    else:
        raise ValueError("invalid timing")


def roll_share(bucket):
    """The Term End Date roll split **[std]**: 80 / 5 / 15 / 0.

    80% renew into the same option at the new declared rate - the contractual default
    [S1] - 5% transfer to a different index-linked option, modelled as renewal at the same
    parameters, and 15% transfer to the Fixed Account. The Holding Account share is zero
    on the base run: it receives maturing amounts only when the option **and** the Fixed
    Account are both unavailable [S2].

    On a probability-weighted single-contract model point the split is a split of *value*
    between the buckets, which is why it can be applied per contract and independently of
    the ``phi`` surrender fraction the notes place before it.
    """
    if bucket == "OPTION":
        return roll_renew_same + roll_transfer_other                 # noqa: F821
    elif bucket == "FIXED":
        return roll_transfer_fixed                                   # noqa: F821
    elif bucket == "HOLDING":
        return roll_transfer_holding                                 # noqa: F821
    else:
        raise ValueError("invalid bucket")


def roll_to_acct_pp(t, bucket):
    """The amount transferred out of the option into a general-account bucket at term end.
    """
    if not is_term_end(t):
        return 0.0
    return inv_amt_pp_at(t, "BEF_ROLL") * roll_share(bucket)


def acct_rate():
    """The declared Fixed and Holding Account rate, floored at the 1% minimum [S1][S2].

    3.00% **[std]** - only the contractual minimum is public.
    """
    return max(declared_acct_rate, guar_min_acct_rate)               # noqa: F821


def fixed_acct_pp_at(t, timing):
    """FA: the Fixed Account value per contract, read at a point inside month t.

    ``FA(t) = FA(t-1) x (1 + max(i_declared, 0.01))^(1/12)`` [S1][S2], plus any amount
    transferred in at a Term End Date, less its pro-rata share of the withdrawal. The
    transfer accrues for the month in which it arrives **[std]**. The bucket opens empty
    on a contract issued at or after the valuation date: the purchase payment is allocated
    wholly to the index-linked option, so the Fixed Account enters the issue month at zero
    and stays there until the first Term End Date. On a contract in force it opens at
    :func:`t_entry` from the model point, :func:`fixed_acct_pp_init`. 0.0 outside cover.
    """
    if timing == "BEF_WD":
        if not is_active(t):
            return 0.0
        prior = fixed_acct_pp(t - 1) if t > t_entry() else fixed_acct_pp_init()
        opening = prior + roll_to_acct_pp(t, "FIXED")
        return opening * (1.0 + acct_rate()) ** (1.0 / 12.0)
    elif timing == "AFT_WD":
        return fixed_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def fixed_acct_pp(t):
    """FA(t): the Fixed Account value per contract at the end of month t.

    ``fixed_acct_pp_at(t, "BEF_WD")`` less the account's share of the withdrawal,
    written inline from the prior month's value, so that the chain back to
    :func:`t_entry` is one cell a month; the arithmetic is ``RILA_US_S``'s. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    prior = fixed_acct_pp(t - 1) if t > t_entry() else fixed_acct_pp_init()
    opening = prior + roll_to_acct_pp(t, "FIXED")
    return opening * (1.0 + acct_rate()) ** (1.0 / 12.0) - wd_alloc_pp(t, "FIXED")


def holding_acct_pp_at(t, timing):
    """HA: the Holding Account value per contract, read at a point inside month t.

    Same accrual and the same 1% guaranteed minimum as the Fixed Account [S1][S2]. It
    holds maturing amounts to the next Contract Anniversary when the option and the Fixed
    Account are both unavailable [S2]; ``roll_transfer_holding`` is 0 on the base run, so
    the bucket stays empty and is carried for completeness of ``AV = sum V_k + FA + HA``.
    It opens empty for the same reason the Fixed Account does, and on a contract in force
    from the model point, :func:`holding_acct_pp_init`. 0.0 outside cover.
    """
    if timing == "BEF_WD":
        if not is_active(t):
            return 0.0
        prior = holding_acct_pp(t - 1) if t > t_entry() else holding_acct_pp_init()
        opening = prior + roll_to_acct_pp(t, "HOLDING")
        return opening * (1.0 + acct_rate()) ** (1.0 / 12.0)
    elif timing == "AFT_WD":
        return holding_acct_pp(t)
    else:
        raise ValueError("invalid timing")


def holding_acct_pp(t):
    """HA(t): the Holding Account value per contract at the end of month t.

    Written inline as :func:`fixed_acct_pp` is, one cell a month back to :func:`t_entry`.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    prior = holding_acct_pp(t - 1) if t > t_entry() else holding_acct_pp_init()
    opening = prior + roll_to_acct_pp(t, "HOLDING")
    return opening * (1.0 + acct_rate()) ** (1.0 / 12.0) - wd_alloc_pp(t, "HOLDING")


def av_pp_at(t, timing):
    """AV: the Account Value per contract, ``sum_k V_k(t) + FA(t) + HA(t)``.

    ``"BEF_WD"`` is the notes' step 5 value - after crediting, the roll split, the interim
    value and the account accruals, before any transaction. It is the base the withdrawal
    is allocated across, the base the free-withdrawal allowance is snapshotted from, and
    the base the return-of-premium reduction ratio uses. ``"AFT_WD"`` is
    :func:`av_pp`, the value every decrement benefit is measured on.

    Between term start and term end this contract has **no account value in the ordinary
    sense**: ``AV`` is a derivative price, depressed exactly when the option leg is out of
    the money - which is when the return-of-premium guarantee bites.

    There is no opening timing here. The Account Value entering a contract's issue month
    is the purchase payment itself, which :func:`inv_amt_basis_pp` carries, the
    general-account buckets opening empty; entering the valuation month on a contract in
    force it is the model point's :func:`av_pp_init`, and the buckets open from theirs.
    The ``"BEF_WD"`` value at an anniversary month is what :func:`free_wd_base` reads, from
    the frame where the anniversary is in it.
    """
    if timing == "BEF_WD":
        return (interim_value_pp_at(t, "BEF_WD")
                + fixed_acct_pp_at(t, "BEF_WD")
                + holding_acct_pp_at(t, "BEF_WD"))
    elif timing == "AFT_WD":
        return av_pp(t)
    else:
        raise ValueError("invalid timing")


def av_pp(t):
    """AV(t): the Account Value per contract at the end of month t."""
    return (interim_value_pp_at(t, "AFT_WD")
            + fixed_acct_pp(t) + holding_acct_pp(t))


def inv_income_pp(t):
    """The investment return credited to one contract's Account Value in month t.

    ``AV`` before the transaction less the value entering the month - the prior month end
    after :func:`t_entry`; in that month the purchase payment itself in the issue month,
    which is where the payment falls, and the model point's :func:`av_pp_init` on a
    contract in force. On this product it is not "interest credited": it is the month's
    movement in a derivative price plus the Fixed and Holding Accounts' accrual, and at a
    Term End Date it also carries the index credit. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        opening = av_pp(t - 1)
    elif duration_mth(t) == 0:
        opening = premium_pp()
    else:
        opening = av_pp_init()
    return av_pp_at(t, "BEF_WD") - opening


def free_wd_base(t):
    """AV_anniv(y): the Account Value at the most recent Contract Anniversary [S1][S2].

    Read **before** that month's transaction, which is the notes' step 5 - the snapshot is
    taken when the anniversary is reached and the withdrawal follows at step 6 - so an
    anniversary withdrawal is measured against a base that already includes that month's
    crediting. The anniversary at ``12 cy`` closes policy month ``12 cy - 1``, so the
    snapshot is that month's ``"BEF_WD"`` value, read at month
    ``12 cy - 1 - duration_mth_init()`` from the valuation date: from the frame where that
    month is :func:`t_entry` or later, and from the model point's
    :func:`av_pp_prev_anniv_init` where the anniversary precedes the valuation month.
    Before the first anniversary there is no snapshot and the base is the purchase
    payment; :func:`free_wd_allow` is zero there in any case. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    cy = duration_eom(t)
    if cy < 1:
        return premium_pp()
    m = 12 * cy - 1 - duration_mth_init()
    if m < t_entry():
        return av_pp_prev_anniv_init()
    return av_pp_at(m, "BEF_WD")


def free_wd_allow(t):
    """The Free Withdrawal Amount for the contract year month t's month end falls in.

    Zero in contract year 1; thereafter 10% of the Account Value at the prior Contract
    Anniversary, non-cumulative - nothing carries across an anniversary. On a negative
    base it is negative, as in ``RILA_US_S``. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if duration_eom(t) < 1:
        return 0.0
    return free_wd_rate * free_wd_base(t)                            # noqa: F821


def free_wd_avail(t):
    """FW(t): the unused free withdrawal allowance at month t, before that month's G.

    Reset to the whole allowance in the month that ends on a Contract Anniversary and
    carried forward within the contract year, reduced by amounts already withdrawn in it
    [S1][S2]: the month before's allowance less its free withdrawal,
    ``free_wd_avail(t - 1) - wd_free_pp(t - 1)``, which is ``RILA_US_S``'s
    ``free_wd_remain(t - 1)`` formed inline, so that the carry is one cell a month where
    ``RILA_US_S``'s runs through two. In the month the contract enters the books it is
    the model point's :func:`free_wd_remain_init`, which is 0 on a contract issued at or
    after the valuation date: its first month opens with nothing carried in. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    if is_anniv(t):
        return free_wd_allow(t)
    if t > t_entry():
        return free_wd_avail(t - 1) - wd_free_pp(t - 1)
    return free_wd_remain_init()


def wd_scheduled_pp(t):
    """The gross withdrawal scheduled for month t in *withdrawal_table.csv*, else zero.

    The programme is a contractual schedule, keyed by the **policy** month end the
    withdrawal is taken at, so month ``t`` reads policy month end ``duration_mth(t) + 1``
    through :func:`wd_amount_pm`: the worked example's $8,000 at the 3-year point sits at
    month end 36 and is taken in policy month 35, whatever the valuation date. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return wd_amount_pm(duration_mth(t) + 1)


def wd_amount_pm(m):
    """The gross withdrawal the model point's programme takes at policy month end ``m``.

    The withdrawal table's one reader, keyed by the policy month end, so that no per-month
    cell joins on the programme's text key: the amount at
    ``(model_point()["wd_schedule_id"], m)``, and 0.0 where the programme has no row at
    ``m``. It asks ``Data.withdrawal_count`` first, so a projection meets the table's
    checks before it reads an amount. :func:`wd_scheduled_pp` calls it in cover only, at
    ``m`` 1 or more.
    """
    data.withdrawal_count()                                          # noqa: F821
    table = data.withdrawal_table()                                  # noqa: F821
    key = (model_point()["wd_schedule_id"], m)
    return float(table.loc[key, "wd_amount"]) if key in table.index else 0.0


def wd_behavioral_pp(t):
    """The behavioural partial withdrawal at month t **[std]**.

    0% in contract year 1, the free amount being zero there [S1][S2]; thereafter
    ``wd_rate_ann`` of the Account Value taken at each Contract Anniversary and capped at
    the Free Withdrawal Amount, so the base run incurs no withdrawal charge. The
    anniversary closes policy month ``12y - 1``, and the first one that can bear a
    withdrawal is the end of policy month 11, where :func:`free_wd_allow` first turns
    positive. RMD-driven withdrawals for qualified cells are named in the notes as a
    behavioural input but no amount formula is given, so no RMD module is implemented.

    On a negative Account Value at the anniversary, which the interim value allows [S2],
    the Free Withdrawal Amount is a share of a negative base and so negative too, and
    ``min(rate x AV, allowance)`` takes the more negative of two negative amounts: a
    withdrawal below 0, which :func:`wd_pp` passes through. ``RILA_US_S`` computes the
    same, and this model, which is ``RILA_US_S`` run in force, keeps it. No shipped point's
    Account Value falls below 0.
    """
    if not is_anniv(t):
        return 0.0
    return min(wd_rate_ann() * av_pp_at(t, "BEF_WD"), free_wd_allow(t))


def wd_pp(t):
    """G_total: the gross amount removed from the contract at month t, per contract.

    The scheduled programme plus the behavioural rule. Gross by construction: the
    withdrawal charge is deducted **from** the amount withdrawn and is not grossed up on
    this chassis [S1][S2], in contrast to [S4]. Capped at the Account Value **[std]** so a
    request larger than the contract cannot drive it negative; the contractual treatment
    of a request that would leave less than the $2,000 minimum - it becomes a full
    withdrawal [S1][S2] - is not implemented. On a negative Account Value the cap is 0,
    and a positive request takes nothing. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    total = wd_scheduled_pp(t) + wd_behavioral_pp(t)
    return min(total, max(0.0, av_pp_at(t, "BEF_WD")))


def wd_free_pp(t):
    """The portion of G_total inside the Free Withdrawal Amount, free of charge [S1][S2]."""
    return min(wd_pp(t), free_wd_avail(t))


def free_wd_remain(t):
    """The unused free withdrawal allowance after month t's withdrawal.

    This, not :func:`free_wd_avail`, is the allowance a full surrender at the end of month
    t can still shelter.
    """
    return free_wd_avail(t) - wd_free_pp(t)


def wd_excess_pp(t):
    """chargeable: ``max(0, G_total - FW(t))``, the amount exposed to the charge [S1][S2].
    """
    return max(0.0, wd_pp(t) - free_wd_avail(t))


def surr_charge_rate(t):
    """wc(cy): the withdrawal charge rate at month t's month end, by **complete** years.

    7, 7, 6, 5, 4, 3, 0 per cent [S1][S2], zero once the schedule runs out. Keyed on
    :func:`duration_eom`, the complete contract years at the instant the transaction
    settles, on the policy clock, through :func:`surr_charge_rate_at`. Contract year 7 -
    the first with a zero charge - is also the first year following a 6-year Term End
    Date on this chassis, which is why the charge-expiry shock lapse is applied there.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return surr_charge_rate_at(duration_eom(t))


def surr_charge_rate_at(cy):
    """The withdrawal charge rate of complete contract year ``cy``, from the table.

    The withdrawal charge table's one reader, keyed by the complete contract years at the
    month end: the table's rate for ``cy`` in ``0 .. n - 1``, where ``n`` is
    ``Data.surr_charge_count()``, whose check holds the table's years to that run, and
    0.0 from ``n`` on, once the schedule has run out, as ``RILA_US_S`` reads a year the
    table lacks. It asks the count first, so a projection meets the table's checks before
    it reads a rate. :func:`surr_charge_rate` calls it in cover only, and
    :func:`lapse_shock_year` at the table's own years.
    """
    n = data.surr_charge_count()                                     # noqa: F821
    if cy < 0 or cy >= n:
        return 0.0
    return float(data.surr_charge_table().loc[cy, "surr_charge_rate"])  # noqa: F821


def wd_charge_pp(t):
    """WC(t): the withdrawal charge on month t's withdrawal, ``wc(cy) x chargeable``."""
    return surr_charge_rate(t) * wd_excess_pp(t)


def wd_payment_pp(t):
    """The cash paid on month t's withdrawal, ``G_total - WC(t)``.

    Not grossed up: the charge comes out of the amount withdrawn [S1][S2].
    """
    return wd_pp(t) - wd_charge_pp(t)


def wd_bucket_value_pp(t, bucket):
    """The value of one bucket at the allocation point, floored at zero.

    The flooring matters because the interim value can be negative [S2], and a negative
    weight in a pro-rata allocation is meaningless; a bucket at or below zero simply takes
    no share **[std]**.
    """
    if bucket == "OPTION":
        return max(0.0, interim_value_pp_at(t, "BEF_WD"))
    elif bucket == "FIXED":
        return max(0.0, fixed_acct_pp_at(t, "BEF_WD"))
    elif bucket == "HOLDING":
        return max(0.0, holding_acct_pp_at(t, "BEF_WD"))
    else:
        raise ValueError("invalid bucket")


def wd_alloc_pp(t, bucket):
    """G_k: the part of G_total taken from one bucket, pro rata to value **[std]**.

    The notes prescribe allocation across open options **pro rata to interim value**,
    the prospectuses not prescribing an allocation for an unspecified withdrawal; with a
    Fixed and a Holding Account present the model extends the same rule to all three
    buckets. On a single-option model point with empty general accounts the whole
    withdrawal falls on the option.
    """
    if wd_pp(t) <= 0.0:
        return 0.0
    total = sum(wd_bucket_value_pp(t, b) for b in ("OPTION", "FIXED", "HOLDING"))
    if total <= 0.0:
        return 0.0
    return wd_pp(t) * wd_bucket_value_pp(t, bucket) / total


def surr_excess_pp(t):
    """The part of the Account Value exposed to the charge on a full surrender [S1][S2]."""
    return max(0.0, av_pp(t) - free_wd_remain(t))


def surr_charge_pp(t):
    """The withdrawal charge on a full surrender at the end of month t."""
    return surr_charge_rate(t) * surr_excess_pp(t)


def surr_value_pp(t):
    """CSV(t): ``AV(t) - wc(cy) x max(0, AV(t) - FW(t))`` [S1][S2].

    The prospectus example reproduces here: a $100,000 payment with an $80,000 Account
    Value at the start of contract year 6 gives a free amount of $8,000, a chargeable
    $72,000, a 3% charge of $2,160 and a cash value of $77,840.
    """
    return av_pp(t) - surr_charge_pp(t)


def rop_pp(t):
    """ROP(t): the return-of-premium GMDB base at the **end** of month t, reduced
    **proportionally** [S1][S2].

    ``ROP(t+) = ROP(t-) x (1 - G_total / AV(t-))``, the ratio taken on the **gross** amount
    removed from the contract - including any withdrawal charge [S1] - and on the Account
    Value before the transaction. The base entering a contract's issue month is the
    purchase payment, which is where the guarantee starts; entering the valuation month on
    a contract in force it is the model point's :func:`rop_pp_init`. The opening is written
    inline, one cell a month back to :func:`t_entry`. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    if t > t_entry():
        prior = rop_pp(t - 1)
    elif duration_mth(t) == 0:
        prior = premium_pp()
    else:
        prior = rop_pp_init()
    base = av_pp_at(t, "BEF_WD")
    if base <= 0.0 or wd_pp(t) <= 0.0:
        return prior
    return prior * (1.0 - wd_pp(t) / base)


def death_ben_pp(t):
    """DB(t): ``max(AV(t), ROP(t))`` for issue ages 80 and under, ``AV(t)`` for 81+ [S2].

    The guarantee sits on top of a value that is itself a derivative price, so it is most
    in the money exactly when interim values are depressed: the guarantee and the account
    are not independent, and a deterministic run understates its cost.
    """
    if age_at_entry() <= db_rop_max_issue_age:                       # noqa: F821
        return max(av_pp(t), rop_pp(t))
    return av_pp(t)


def mort_rate(t):
    """The annual mortality rate at the attained age and sex, times the A/E factor.

    The shipped table is an illustrative annuitant curve **[std]**, *not* a published
    basis. The notes prescribe the 2012 IAM **Basic** table (VM-M section 2.C) with
    generational Projection Scale G2 [REG-R59], which may not be redistributed here; swap
    it in by repointing ``Data.mort_table_file`` before the model computes anything. Do
    **not** run best-estimate mortality off the 2012 IAM *Period* table: it carries the
    valuation margin built in at construction, so a 100% A/E against it sets
    deferral-phase mortality roughly 10% below the unloaded basis [REG-R60].
    ``mort_ae_factor`` is 100% **[std]** - a placeholder, not a measurement, because public
    deferred-period annuitant mortality is thin [REG-R65] and the payout chassis's 108.4%
    is annuitant-select and deliberately not imported.

    The product is capped at 1, written ``min(q, 1.0)``, so that an A/E above 1 cannot
    carry a rate past certainty, and with the bound second a missing input, a NaN, stays
    NaN, where ``min(1.0, q)`` would read it as 1. No shipped point reaches the cap. The
    cap is ``RILA_US_S``'s. The table rate is read through :func:`mort_rate_base_at`, at
    the attained age on the policy clock. 0.0 outside cover, where no table is read.
    """
    if not is_active(t):
        return 0.0
    rate = mort_rate_base_at(age(t))
    return min(rate * mort_ae_factor, 1.0)                           # noqa: F821


def mort_rate_base_at(x):
    """The table's annual mortality rate at attained age ``x`` for the model point's sex.

    The mortality table's one reader, keyed by attained age, so that no per-month cell
    joins on the table: the rate at ``(x, model_point()["sex"])``. It asks
    ``Data.mort_table_count`` first, so a projection meets the table's checks before it
    reads a rate. :func:`mort_rate` calls it in cover only, at the issue age or more.
    """
    data.mort_table_count()                                          # noqa: F821
    return float(data.mort_table().loc[                              # noqa: F821
        (x, model_point()["sex"]), "mort_rate"])


def mort_rate_mth(t):
    """q_m(t): the monthly mortality rate, ``1 - (1 - q_x)^(1/12)``."""
    return 1.0 - (1.0 - mort_rate(t)) ** (1.0 / 12.0)


def lapse_rate_base(t):
    """w_base(y): the un-shocked annual surrender rate for the contract year **[std]**.

    2.0% through contract year 7 and 6.0% thereafter, read as a step function of the
    contract year :func:`policy_year`, on the policy clock, through
    :func:`lapse_rate_base_py`. A shape placeholder: the VA/RILA behaviour study [REG-R64]
    reports aggregate counts only and its detailed tables sit behind a paid data package.
    The shock enters separately as :func:`lapse_rate_sc_mult`, so the two are
    multiplicative and neither is baked into the other. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return lapse_rate_base_py(policy_year(t))


def lapse_rate_base_py(y):
    """The base annual surrender rate of contract year ``y``, the table's step function.

    The lapse table's one reader, keyed by contract year: the rate of the last
    ``contract_year`` at or before ``y``, found by an explicit loop over the table's keys,
    where ``RILA_US_S`` takes the ``max`` of a list. It asks ``Data.lapse_table_count``
    first, whose check holds the table's first year at 1, so every contract year has a
    rate. :func:`lapse_rate_base` calls it in cover only, at ``y`` 1 or more.
    """
    data.lapse_table_count()                                         # noqa: F821
    table = data.lapse_table()                                       # noqa: F821
    year = 0
    for i in table.index:
        if bool(i <= y):
            year = max(year, int(i))
    return float(table.loc[year, "lapse_rate_base"])


def lapse_shock_year():
    """The contract year the withdrawal-charge-expiry surrender shock falls in.

    The first contract year with a zero withdrawal charge, derived from
    *surr_charge_table.csv* rather than hard-coded, so a different schedule moves the
    shock with it - the construction :mod:`.UL_US_S` uses. On the 7-7-6-5-4-3-0
    schedule that is contract year 7, which on this 6-year chassis is also the first year
    following a Term End Date [S1][S2]. The table's years run ``0 .. n - 1``, which
    ``Data.surr_charge_count`` checks, so an explicit loop over them through
    :func:`surr_charge_rate_at` finds the first charge-free year where ``RILA_US_S``
    takes the ``min`` of a list; with none, it is the year after the schedule runs out,
    as there.
    """
    n = data.surr_charge_count()                                     # noqa: F821
    for cy in range(n):
        if surr_charge_rate_at(cy) <= 0.0:
            return cy + 1
    return n + 1


def lapse_rate_sc_mult(t):
    """M_sc(y): the charge-expiry shock multiplier, ``lapse_shock_mult`` = 3.0 **[std]**.

    Applied in :func:`lapse_shock_year` only, and 1.0 in every other contract year. The
    size is the scalar Reference ``lapse_shock_mult`` and the year is derived from the
    charge schedule, matching the universal-life chassis's Reference / Cells split.
    Contract year 7 is the first year with a zero withdrawal charge [S1][S2] **and** the
    first following a 6-year Term End Date - on this chassis the two coincide. The
    order-of-magnitude anchors from adjacent products are ~33% without a living-benefit
    rider and ~10% with one for FIA [REG-R62][REG-R63][unverified]; the representative
    RILA carries no living-benefit rider, which argues for the un-suppressed end, but the
    term structure offsets it, so the **[std]** shock is set well below that anchor. 1.0
    outside cover, its neutral value, so that no contract year the contract does not have
    is compared.
    """
    if not is_active(t):
        return 1.0
    return lapse_shock_mult if policy_year(t) == lapse_shock_year() else 1.0  # noqa: F821


def lapse_iv_mult(t):
    """M_iv(t): interim-value moneyness suppression, the RILA-specific effect **[std]**.

    ``min(1.0, max(0.25, V_k(t) / IA_k(t)))^2``, so a bucket at ``V/IA = 0.85`` carries a
    0.72 multiplier and one at or above par carries 1.0. Surrendering mid-term
    crystallizes the interim value, which is punitive when the option leg is out of the
    money [S1][S2], and a rational holder defers. It is exactly 1 at a Term End Date,
    where the interim value equals the Investment Amount, which is what makes the
    term-end concentration :func:`term_end_lapse_rate` the whole story there. 1.0 outside
    cover, its neutral value.
    """
    if not is_active(t):
        return 1.0
    return min(1.0, max(iv_moneyness_floor, iv_ratio(t))) ** 2       # noqa: F821


def lapse_rate(t):
    """w_annual(y,t): the **annual** surrender rate, ``min(0.50, w_base x M_sc x M_iv)``.

    The 50% ceiling is a **[std] cap**, ``RILA_US_S``'s ``min`` with its bound first.
    ``lapse_rate`` is annual and :func:`lapse_rate_mth` is monthly, matching the
    ``mort_rate`` / ``mort_rate_mth`` pair; the decrement chain reads the monthly one.
    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return min(lapse_rate_max,                                       # noqa: F821
               lapse_rate_base(t) * lapse_rate_sc_mult(t) * lapse_iv_mult(t))


def lapse_rate_mth(t):
    """w_m(t): the monthly background surrender rate, ``1 - (1 - w_annual)^(1/12)``."""
    return 1.0 - (1.0 - lapse_rate(t)) ** (1.0 / 12.0)


def term_end_lapse_rate(t):
    """phi: the discrete term-end surrender fraction **[std]**.

    10% when the withdrawal charge is zero and 3% otherwise, applied at each Term End Date
    **in addition** to the background monthly rate. During the Transfer Period the interim
    value equals the Investment Amount - no option adjustment [S2] - so the economic
    penalty for exiting vanishes for five days each term and surrenders concentrate there.
    A model that spreads surrenders uniformly across the term systematically over-collects
    the negative interim value adjustment.
    """
    if not is_term_end(t):
        return 0.0
    return (term_end_lapse_free if surr_charge_rate(t) <= 0.0        # noqa: F821
            else term_end_lapse_charged)                             # noqa: F821


def pols_if_at(t, timing):
    """In-force at month t read at the point given by ``timing``.

    The notes' order is death at ``q_m(t)``, then surrender at ``w_m(t)`` on survivors
    **[std order]**, plus the discrete term-end fraction ``phi``::

        l(t+1) = l(t) (1 - q_m(t)) (1 - w_m(t)) (1 - phi(t))

    The timings in processing order:

    ``"BEF_NB"``
        the count carried in from month t - 1, before month t's new business: the
        survivors of month t - 1's deaths and surrenders, out of month t - 1's
        ``"BEF_DECR"`` count. At :func:`t_entry`, the first month on the books, it is
        :func:`pols_if_init`, the count in force at the valuation date (0 for a point
        issued at or after it), and the recursion reads no earlier month. Zero outside
        cover, so the survivors of the last covered month leave as :func:`pols_maturity`.
    ``"BEF_DECR"``
        ``l(t)``, the start-of-month count: ``"BEF_NB"`` plus :func:`pols_new_biz`, before
        any decrement; :func:`pols_if` itself, and the weight on that month's cash flows.
    ``"BEF_LAPSE"``
        after deaths, ``l(t)(1 - q_m(t))``.
    ``"BEF_TERM_SURR"``
        after the background monthly surrender, ``l(t)(1 - q_m)(1 - w_m)``.
    ``"AFT_DECR"``
        after the discrete term-end surrender fraction ``phi``: the count at the month
        **end**, the notes' ``l(t+1)``, which in the last covered month is what
        :func:`pols_maturity` force-annuitizes out.

    ``"BEF_NB"`` and ``"BEF_DECR"`` are ``basiclife.BasicTerm_SE``'s names, and any timing
    but these five raises. ``"BEF_NB"`` forms the count left at the end of month t - 1
    itself - month t - 1's ``"BEF_NB"`` plus its :func:`pols_new_biz`, after its three
    decrements, the products ``"AFT_DECR"`` takes in the order it takes them - rather than
    calling for it. So the chain of calls from month t back to :func:`t_entry` is one
    cell a month, where ``RILA_US_S``'s runs through two. Every count is zero outside
    cover, before any rate is read.
    """
    if timing == "BEF_NB":
        if not is_active(t):
            return 0.0
        if t == t_entry():
            return pols_if_init()
        return ((pols_if_at(t - 1, "BEF_NB") + pols_new_biz(t - 1))
                * (1.0 - mort_rate_mth(t - 1)) * (1.0 - lapse_rate_mth(t - 1))
                * (1.0 - term_end_lapse_rate(t - 1)))
    elif timing == "BEF_DECR":
        return pols_if_at(t, "BEF_NB") + pols_new_biz(t)
    elif timing == "BEF_LAPSE" or timing == "BEF_TERM_SURR" or timing == "AFT_DECR":
        if not is_active(t):
            return 0.0
        pols = pols_if_at(t, "BEF_DECR")
        pols = pols * (1.0 - mort_rate_mth(t))
        if timing == "BEF_LAPSE":
            return pols
        pols = pols * (1.0 - lapse_rate_mth(t))
        if timing == "BEF_TERM_SURR":
            return pols
        return pols * (1.0 - term_end_lapse_rate(t))
    raise ValueError("invalid timing")


def pols_if(t):
    """l(t): the number in force at the **start** of month t, the weight of row t.

    ``pols_if_at(t, "BEF_DECR")``: the count carried in from month t - 1 plus month t's new
    business, before month t's decrements - the population that takes the month's
    withdrawal, carries its expenses and is exposed to its decrements, so it is the weight
    on every cash flow of the same :func:`result_cf` row, which reconciles against the row
    it sits on: ``premiums(t) / premium_pp()`` in the issue month, ``withdrawals(t) /
    wd_payment_pp(t)`` and ``expenses(t)`` over the per-contract maintenance charge all
    return it. On a point issued at ``t = 0`` it is exactly ``RILA_US_S``'s ``pols_if``. A
    point in force at the valuation date opens with :func:`pols_if_init`, and one issued
    at or after it with its issued count in the issue month. Zero outside cover: before
    issue, and from ``t = proj_len()`` on, because the survivors of the last covered month
    are force-annuitized out through :func:`pols_maturity`.

    It is ``basiclife.BasicTerm_SE``'s ``BEF_DECR`` count, not its ``pols_if``, which is
    the count before maturity. The count at the month **end**, the notes' ``l(t+1)``, is
    ``pols_if_at(t, "AFT_DECR")``, which equals ``pols_if_at(t + 1, "BEF_NB")`` in every
    month but the last covered one.
    """
    return pols_if_at(t, "BEF_DECR")


def pols_new_biz(t):
    """Number of contracts issued in month t: ``policy_count()`` in the issue month.

    The issue month is the one with ``duration_mth(t) == 0``: ``t = 0`` for a point
    issued at the valuation date, ``t = k`` for one issued ``k`` months later. A point
    already in force at the valuation date has none.
    """
    return policy_count() if duration_mth(t) == 0 else 0.0


def pols_death(t):
    """Deaths in month t, weighted ``l(t) q_m(t)``; 0.0 outside cover."""
    if not is_active(t):
        return 0.0
    return pols_if_at(t, "BEF_DECR") * mort_rate_mth(t)


def pols_lapse_term(t):
    """The discrete term-end concentrated surrenders, non-zero only at a Term End Date.

    0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, "BEF_TERM_SURR") * term_end_lapse_rate(t)


def pols_lapse(t):
    """Full surrenders in month t: the background rate on survivors, plus ``phi``.

    Weighted ``l(t)(1 - q_m(t)) w_m(t)`` **[std timing]** for the background part. Both
    parts settle at the same cash surrender value, so they are one benefit line; the
    term-end part is broken out as :func:`pols_lapse_term` for diagnosis. 0.0 outside
    cover.
    """
    if not is_active(t):
        return 0.0
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate_mth(t) + pols_lapse_term(t)


def pols_maturity(t):
    """Forced annuitizations at the Maturity Date, non-zero only in the last month.

    The Maturity Date is the end of policy month ``maturity_mth() - 1``, the last month of
    the frame, ``t = proj_len() - 1``; the test is made on the policy clock. Not a
    decrement - the contract reaches its Maturity Date and must annuitize [S2] - but
    needed for the in-force roll-forward to close; see the Space docstring.
    """
    if duration_mth(t) != maturity_mth() - 1:
        return 0.0
    return pols_if_at(t, "AFT_DECR")


def pols_decr(t, kind):
    """The number of contracts leaving in month t by benefit ``kind``."""
    if kind == "DEATH":
        return pols_death(t)
    elif kind == "LAPSE":
        return pols_lapse(t)
    elif kind == "MATURITY":
        return pols_maturity(t)
    else:
        raise ValueError("invalid kind")


def claim_pp(t, kind):
    """The benefit paid per contract in month t by ``kind``.

    ``"DEATH"`` is :func:`death_ben_pp`, ``max(AV, ROP)`` in the return-of-premium band
    [S2]. ``"LAPSE"`` is the cash surrender value :func:`surr_value_pp`. ``"MATURITY"`` is
    the Account Value, force-annuitized at the Maturity Date [S2]; converting it to a
    payment stream is the immediate-annuity chassis, restricted to the two forms this
    contract offers - and note that this contract offers **no refund forms**, so that
    branch of the chassis is unused.
    """
    if kind == "DEATH":
        return death_ben_pp(t)
    elif kind == "LAPSE":
        return surr_value_pp(t)
    elif kind == "MATURITY":
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def claim_from_av_pp(t, kind):
    """The Account Value released per contract by a claim of ``kind``.

    ``AV(t)`` for all three: decrements act at the end of the month on the post-transaction
    Account Value. It differs from :func:`claim_pp` by the withdrawal charge retained on a
    surrender and by any return-of-premium excess on a death claim; that difference is
    :func:`claims_over_av`.
    """
    if kind in ("DEATH", "LAPSE", "MATURITY"):
        return av_pp(t)
    else:
        raise ValueError("invalid kind")


def premiums(t):
    """Premium income: the single purchase payment, at the opening of the issue month.

    The month with ``duration_mth(t) == 0`` [S1][S2], weighted by :func:`pols_new_biz`,
    the contracts issued there, so ``premiums(t) / premium_pp() == pols_if(t)`` in that
    month; none on a contract in force at the valuation date, whose payment was made
    before it.
    """
    return premium_pp() * pols_new_biz(t)


def prem_to_av_pp(t):
    """Premium credited to the Investment Amount per contract, in the issue month.

    There is no front-end load and no explicit asset-based charge on this chassis: the cap
    *is* the fee, and the margin appears as the spread between the earned rate and the
    option budget implied by the declared cap [S3][S4][S6]. The issue month is the one
    with ``duration_mth(t) == 0``.
    """
    return premium_pp() if duration_mth(t) == 0 else 0.0


def prem_to_av(t):
    """Premium credited to the block's Account Value, weighted by :func:`pols_new_biz`."""
    return prem_to_av_pp(t) * pols_new_biz(t)


def withdrawals(t):
    """Withdrawal payments in month t: ``(G_total - WC(t))`` weighted by :func:`pols_if`.

    The weight is the count entering month t - transactions are taken before the month's
    decrements - so ``withdrawals(t) / wd_payment_pp(t) == pols_if(t)``. The withdrawal
    charge is retained by the insurer, so it is not a cash flow of its own: it is the
    difference between the gross amount removed from the contract and the cash paid out.
    """
    return wd_payment_pp(t) * pols_if(t)


def claims(t, kind=None):
    """Benefit outgo in month t, for one ``kind`` or, with ``kind=None``, all three."""
    if kind is None:
        return (claims(t, "DEATH") + claims(t, "LAPSE") + claims(t, "MATURITY"))
    return claim_pp(t, kind) * pols_decr(t, kind)


def claims_from_av(t, kind):
    """The Account Value released by a claim of ``kind``, in-force weighted."""
    return claim_from_av_pp(t, kind) * pols_decr(t, kind)


def claims_over_av(t, kind=None):
    """Benefit paid less the Account Value released, ``claims - claims_from_av``.

    Signed. Negative on a surrender inside the charge period, where the contract pays out
    less than the Account Value it releases; positive on a death claim where the
    return-of-premium guarantee bites. A reconciliation quantity, not a cash flow of its
    own.
    """
    if kind is None:
        return (claims_over_av(t, "DEATH") + claims_over_av(t, "LAPSE")
                + claims_over_av(t, "MATURITY"))
    return claims(t, kind) - claims_from_av(t, kind)


def inflation_factor(t):
    """The expense inflation factor in month t, ``(1 + inflation_rate) ** (t // 12)``.

    On the **valuation** clock: ``t`` counts months from the valuation date, so the
    maintenance charge it inflates is in valuation-date dollars, whatever the contract's
    age, and every point of a block inflates alike. ``RILA_US_S``'s annual step is kept,
    ``1.025^k`` from ``t = 12 k`` to ``12 k + 11``, but it falls every twelve months from
    the valuation date rather than on the contract's anniversaries. On a point issued at
    ``t = 0`` the two are the same; on the anchor cell in force 71 months this model's
    charge is ``RILA_US_S``'s divided by ``1.025^6``, or by ``1.025^5`` at
    ``t = 0, 12, 24, …``, where the valuation clock has stepped and the contract's
    anniversary is a month away. Defined in every month, before issue too: it is an input,
    not a state of the contract.
    """
    return (1.0 + inflation_rate) ** (t // 12)                       # noqa: F821


def expenses(t):
    """Insurer expenses: acquisition at issue and inflating maintenance monthly **[std]**.

    ``0.06 x premium + 200`` at the opening of the issue month, ``duration_mth(t) == 0``,
    where the purchase payment falls, and ``60/12 x inflation_factor(t)`` per contract in
    every month including that one, weighted by :func:`pols_if` - the count entering the
    month, since the expense is incurred over it. The issue month therefore carries both
    lines, and the acquisition is per contract issued. The notes' ledger carries no
    separate commission line - distribution cost sits inside the acquisition expense - so
    this model has no ``commissions`` cells. 0.0 outside cover.
    """
    if not is_active(t):
        return 0.0
    acq = (expense_acq_rate * premium_pp()                           # noqa: F821
           + expense_acq_fixed) if duration_mth(t) == 0 else 0.0     # noqa: F821
    return (acq + (expense_maint / 12.0)                             # noqa: F821
            * inflation_factor(t)) * pols_if(t)


def premium_taxes(t):
    """Premium tax on the purchase payment, 0% **[std]** [S2].

    State-specific and not quantified in any retrieved document; the parameter is exposed
    rather than removed.
    """
    return premium_tax_rate * premiums(t)                            # noqa: F821


def net_cf(t):
    """Net cash flow in month t from the valuation date.

    Term-end index credits, the movement of the interim value, the withdrawal charge and
    the roll split between the option and the general accounts are **internal accounting
    entries**: they drive the Investment Amount, the Account Value and the benefit
    *amount*, but are never ledger lines. The option budget is not a liability cash flow
    at all - it is an asset-side flow, and the liability model sees it only through the
    declared cap. Only amounts paid to or received from the contract holder, and the
    insurer's own expenses, in valuation-date dollars, appear here.
    """
    return (premiums(t) - withdrawals(t) - claims(t)
            - expenses(t) - premium_taxes(t))


def av_at(t, timing):
    """The in-force weighted Account Value at month t; ``timing`` as in :func:`av_pp_at`.

    ``"BEF_WD"`` carries :func:`pols_if`, the count entering month ``t``. ``"AFT_WD"``
    carries the count *leaving* it, which under the start-of-period convention is
    ``pols_if_at(t + 1, "BEF_NB")``, the count carried into the next month before its new
    business - zero in the last month, where :func:`pols_maturity` has force-annuitized
    the survivors out and the block's Account Value is released in full. ``"AFT_WD"`` is
    zero outside cover, before it reads ``t + 1``, so that at ``t = proj_len()``, the month
    after cover, nothing reads the count a month past the frame.
    """
    if timing == "BEF_WD":
        return av_pp_at(t, "BEF_WD") * pols_if(t)
    elif timing == "AFT_WD":
        if not is_active(t):
            return 0.0
        return av_pp(t) * pols_if_at(t + 1, "BEF_NB")
    else:
        raise ValueError("invalid timing")


def inv_income(t):
    """The investment return credited to the whole block in month t."""
    return inv_income_pp(t) * pols_if(t)


def wd_from_av(t):
    """The Account Value released by month t's withdrawals, gross of the charge."""
    return wd_pp(t) * pols_if(t)


def av_change(t):
    """The change in the block's Account Value over month t.

    After :func:`t_entry`, the month before's close; in that month, the block's opening
    state, ``av_pp_init() x pols_if_init()``, which is nothing on a contract issued at or
    after the valuation date: its purchase payment arrives inside the issue month, as
    :func:`prem_to_av`.
    """
    opening = av_at(t - 1, "AFT_WD") if t > t_entry() else av_pp_init() * pols_if_init()
    return av_at(t, "AFT_WD") - opening


def roll_fwd_tol():
    """The absolute tolerance the ``check_*`` booleans hold a currency residual to.

    One part in a billion of the purchase payment. The roll-forward identities are
    differences of Account Values of that size, and the option pricer's own rounding sits
    well inside it; a genuine wiring error is orders of magnitude larger.
    """
    return 1e-9 * max(1.0, premium_pp())


def check_av_roll_fwd_resid(t):
    """Account value roll-forward residual; zero to floating point in every month.

    ``AV(t) - AV(t-1) = premium in - withdrawals out + investment return - the Account
    Value released by each of the three claim kinds``. The *cash* paid can differ from the
    Account Value released - by the withdrawal charge retained on a surrender and by the
    return-of-premium excess on a death claim - and that difference is
    :func:`claims_over_av`, not part of this identity. The month a contract enters the
    books is included: issued then, the block opens at nothing, the purchase payment
    arrives as :func:`prem_to_av`, and the identity closes on it like any other month; in
    force at the valuation date, it opens at its opening state (:func:`av_change`).

    The signed per-month residual, which is what a failing :func:`check_av_roll_fwd` needs
    for diagnosis; the boolean is implemented in terms of it.
    """
    expected = (prem_to_av(t) - wd_from_av(t) + inv_income(t)
                - claims_from_av(t, "DEATH") - claims_from_av(t, "LAPSE")
                - claims_from_av(t, "MATURITY"))
    return av_change(t) - expected


def check_av_roll_fwd():
    """True when the account value roll-forward closes in **every** projected month.

    No argument and a bool, following ``CashValue_SE.check_av_roll_fwd`` and the rest of
    this library, so one test can call the same check across every model;
    :func:`check_av_roll_fwd_resid` gives the signed residual of a month that fails. The
    residual is an aggregate over the point's contracts, so the tolerance is
    :func:`roll_fwd_tol` times ``max(policy_count(), 1)``: on a point counting one
    contract it is ``RILA_US_S``'s. ``RILA_US_S``'s ``all`` is kept, so a residual that
    is not a number fails the check.
    """
    tol = roll_fwd_tol() * max(policy_count(), 1.0)
    return all(abs(check_av_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_pols_roll_fwd_resid(t):
    """In-force roll-forward residual; zero to floating point in every month.

    ``pols_if(t) - pols_if_at(t + 1, "BEF_NB") = deaths + surrenders + forced
    annuitizations at the Maturity Date``: the start-of-month count opens the row, the
    exits are taken during it, and the next month opens on what is left, before its own
    new business, which is no part of month t's movement. Zero outside cover, before
    ``t + 1`` is read, so that at ``t = proj_len()``, the month after cover, nothing reads
    the count a month past the frame.
    """
    if not is_active(t):
        return 0.0
    return (pols_if(t) - pols_if_at(t + 1, "BEF_NB") - pols_death(t)
            - pols_lapse(t) - pols_maturity(t))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in **every** projected month.

    No argument and a bool; :func:`check_pols_roll_fwd_resid` gives the signed residual.
    The counts are probabilities of order 1 per contract, so the tolerance is absolute
    rather than the currency-scaled :func:`roll_fwd_tol`, ``1e-12`` times
    ``max(policy_count(), 1)``, scaling with the count as the residual does. On a point
    counting one contract it is ``RILA_US_S``'s ``1e-12``. ``RILA_US_S``'s ``all`` is kept,
    so a residual that is not a number fails the check.
    """
    tol = 1e-12 * max(policy_count(), 1.0)
    return all(abs(check_pols_roll_fwd_resid(t)) <= tol
               for t in range(proj_len()))


def check_term_end_identity_resid(t):
    """The notes' term-end verification identity, ``V_k = IA_k(1 + g)``; zero everywhere.

    At ``tau = 0`` the replicating portfolio collapses to intrinsic value and must
    reproduce the crediting rate exactly. If this is not zero to the cent, the strike set,
    the notional convention, the buffer sign - or a trading cost provision left switched on
    at ``tau = 0`` - is wrong. Zero by construction outside a Term End Date, where the
    identity does not apply.
    """
    if not is_term_end(t):
        return 0.0
    return (interim_value_pp_at(t, "BEF_ROLL")
            - inv_amt_basis_pp(t) * (1.0 + credit_rate_term(t)))


def check_term_end_identity():
    """True when ``V_k = IA_k(1 + g)`` holds at **every** Term End Date.

    No argument and a bool, like the two roll-forward checks;
    :func:`check_term_end_identity_resid` gives the signed residual of a term end that
    fails. This is the check the notes ask for by name.
    """
    return all(abs(check_term_end_identity_resid(t)) <= roll_fwd_tol()
               for t in range(proj_len()))


def result_cf():
    """Result table of cashflows, indexed by month ``t`` from the valuation date.

    The frame is ``t = 0 ... proj_len() - 1``, and row ``t`` is the same month for every
    model point, so the frames of a block sum row by row. A contract issued at or after
    the valuation date carries its purchase payment and acquisition expense in its issue
    month - they fall at its opening, which is the Issue Date - as well as that month's
    own maintenance expense and decrements, and zeros in every month before it. The
    surrender column is ``claims_lapse``, matching the ``"LAPSE"`` ``kind`` that produces
    it, and partial withdrawals sit in their own ``withdrawals`` column rather than among
    the claims - a withdrawal is a payment on the owner's election, not a claim. The cash
    flow columns sum to ``net_cf`` under the income-positive sign convention:
    ``premiums`` less every other flow. The columns are ``RILA_US_S``'s.

    ``pols_if`` is the count in force at the **start** of each month, so it is the weight
    the cash flows on that same row carry - the column and the row reconcile.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "withdrawals": [withdrawals(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_maturity": [claims(t, "MATURITY") for t in ts],
            "expenses": [expenses(t) for t in ts],
            "premium_taxes": [premium_taxes(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of in-force movements, indexed ``t = 0 ... proj_len() - 1``.

    ``pols_if`` opens the month, ``pols_new_biz`` is the contracts issued in it, the four
    movement columns are what leaves it, and ``pols_if_aft_decr`` is the count at the
    month end, the notes' ``l(t+1)`` - after death, surrender and the term-end
    concentration, but before the Maturity Date annuitization that ``pols_maturity``
    carries out. ``RILA_US_S``'s columns, with ``pols_new_biz`` after ``pols_if``, as
    ``basiclife.BasicTerm_SE``'s report carries it; zeros before issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_new_biz": [pols_new_biz(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_term": [pols_lapse_term(t) for t in ts],
            "pols_maturity": [pols_maturity(t) for t in ts],
            "pols_if_aft_decr": [pols_if_at(t, "AFT_DECR") for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_av():
    """Result table of per-contract values, indexed ``t = 0 ... proj_len() - 1``.

    The Investment Amount and Interim Value either side of the month's transaction, the
    Account Value, the general accounts, the return-of-premium base and the surrender and
    death benefits; zeros before issue.
    """
    ts = list(range(proj_len()))
    return pd.DataFrame(                                             # noqa: F821
        {
            "inv_amt_pp": [inv_amt_pp(t) for t in ts],
            "interim_value_pp": [interim_value_pp_at(t, "AFT_WD") for t in ts],
            "fixed_acct_pp": [fixed_acct_pp(t) for t in ts],
            "holding_acct_pp": [holding_acct_pp(t) for t in ts],
            "av_pp_bef_wd": [av_pp_at(t, "BEF_WD") for t in ts],
            "wd_pp": [wd_pp(t) for t in ts],
            "av_pp": [av_pp(t) for t in ts],
            "rop_pp": [rop_pp(t) for t in ts],
            "surr_charge_pp": [surr_charge_pp(t) for t in ts],
            "surr_value_pp": [surr_value_pp(t) for t in ts],
            "death_ben_pp": [death_ben_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_iv():
    """The interim value decomposition, one row per month - the worked example's table.

    Index level, index performance, the fixed income asset proxy, one column per
    replicating-portfolio leg, the derivative asset proxy, the trading cost, the interim
    value and the Investment Amount, each measured before the roll split so the columns
    line up with the notes. Indexed ``t = 0 ... proj_len() - 1``; before issue every
    column is 0.0, the index level included, which no market path is read for there.
    """
    ts = list(range(proj_len()))
    out = {
        "index_level": [index_level(t) if is_active(t) else 0.0 for t in ts],
        "index_perf": [index_perf(t) for t in ts],
        "tau": [tau(t) for t in ts],
        "fixed_proxy_pp": [fixed_proxy_pp(t) for t in ts],
    }
    for leg in opt_legs():
        out[leg.lower()] = [opt_component_pp(t, leg) for t in ts]
    out["deriv_proxy_pp"] = [deriv_proxy_pp(t) for t in ts]
    out["trading_cost_pp"] = [trading_cost_pp(t) for t in ts]
    out["interim_value_pp"] = [interim_value_pp_at(t, "BEF_ROLL") for t in ts]
    out["inv_amt_pp"] = [inv_amt_pp_at(t, "BEF_ROLL") for t in ts]
    return pd.DataFrame(out, index=pd.Index(ts, name="t"))           # noqa: F821


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

maturity_age = 90

maturity_min_years = 10

free_wd_rate = 0.1

trading_cost_rate = 0.001

iv_credit_spread = 0.01

iv_expense_rate = 0.001

earned_rate = 0.04

nge_spread = 0.0222

nge_cap_search_max = 5.0

nge_solve_iter = 80

declared_acct_rate = 0.03

guar_min_acct_rate = 0.01

roll_renew_same = 0.8

roll_transfer_other = 0.05

roll_transfer_fixed = 0.15

roll_transfer_holding = 0.0

db_rop_max_issue_age = 80

mort_ae_factor = 1.0

iv_moneyness_floor = 0.25

lapse_shock_mult = 3.0

lapse_rate_max = 0.5

term_end_lapse_free = 0.1

term_end_lapse_charged = 0.03

expense_acq_rate = 0.06

expense_acq_fixed = 200.0

expense_maint = 60.0

inflation_rate = 0.025

premium_tax_rate = 0.0

math = ("Module", "math")

pd = ("Module", "pandas")