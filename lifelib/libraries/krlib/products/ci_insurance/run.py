"""Run the CI_KR_A reference model and print its cash flow statement.

    python products/ci_insurance/run.py            # anchor cell (point_id = 1)
    python products/ci_insurance/run.py 4          # another model point

Output is ASCII-only so it prints on a Windows console under any code page: amounts are
KRW, the product is written "CI boheom (jungdae jilbyeong boheom, critical illness)"
rather than in hangul, the acceleration is "seonjigeup biyul", and the suppressed
surrender-value form is "jeohaeji hwangeup-hyeong".
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "CI_KR_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
k = proj.cv_floor_ratio()
form = ("gibon hwangeup-hyeong (k = 1.00)" if k >= 1.0
        else "muhaeji hwangeup-hyeong (k = 0.00)" if k <= 0.0
        else "jeohaeji hwangeup-hyeong, k = {:.2f}".format(k))

print("CI_KR_A - CI boheom (jungdae jilbyeong boheom, critical illness), annual grid")
print("age basis: boheom nai (insurance age, six-month rounding)")
print("model point {}: {} - {}{}, cover KRW {:,.0f}, {}-year premium term, {}".format(
    point_id, proj.model_point()["policy_id"], proj.sex(), proj.age_at_entry(),
    proj.sum_assured(), proj.prem_term(), form))
print("seonjigeup biyul a = {:.2f}   residual r = {:.2f}   account floor c = {:.2f}   "
      "first-year reduction: {}".format(
          proj.accel_rate(), proj.resid_rate(), proj.resid_floor_mult(),
          proj.first_year_scope()))
print("gross premium = KRW {:,.2f} p.a.   net level premium = KRW {:,.2f} p.a.".format(
    proj.premium_pp(), proj.prem_net_level_pp()))
print("projection = {} years to attained age {}   CI cover ends in policy year {} "
      "(age 100)".format(proj.proj_len(), proj.omega_age(), proj.ci_cover_end()))
print("pyojun haeyak gongje-aek (statutory surrender-charge cap) = KRW {:,.2f}".format(
    proj.surr_chg_cap_pp()))
print("modules: lapse basis = {}   loan utilisation = {:.2%} at year {}   "
      "mort_be_factor = {:.2f}   ci_be_factor = {:.2f}   post-CI mortality x {:.2f}".format(
          proj.lapse_basis(), proj.pol_loan_util(), proj.pol_loan_year(),
          proj.mort_be_factor(), proj.ci_be_factor(), proj.mort_ci_factor()))
print()

df = proj.result_cf()
rows = [t for t in range(1, 13) if t <= proj.proj_len()]
m = proj.prem_period()
rows += [t for t in (m - 1, m, m + 1) if t <= proj.proj_len() and t not in rows]
print("first twelve policy years, and the years around the end of the premium term:")
print(df.loc[sorted(rows)].round(2).to_string())
print()
print("undiscounted totals per policy issued (KRW):")
print(df.sum().round(2).to_string())
print()

val = proj.result_val()
print("the acceleration, at three durations (per policy, KRW):")
for t in (5, 10, m):
    if t > proj.proj_len():
        continue
    print("  t = {:>2}  account V = {:>14,.0f}   surrender pre-CI = {:>14,.0f}   "
          "post-CI = {:>14,.0f}".format(
              t, val.loc[t, "pol_val_pp"], val.loc[t, "cv_pp"], val.loc[t, "cv_pp_ci"]))
    print("          accelerated a*B = {:>10,.0f}   nominal residual r*B = {:>12,.0f}   "
          "loan limit pre/post = {:,.0f} / {:,.0f}".format(
              val.loc[t, "accel_benefit_pp"], val.loc[t, "resid_nominal_pp"],
              proj.loan_avail_pp(t), proj.loan_avail_ci_pp(t)))
print()

print("checks: pols {}  ci states {}  decrements {}  account {}  complement {}".format(
    proj.check_pols_roll_fwd(), proj.check_ci_state_roll_fwd(),
    proj.check_decrement_sum(), proj.check_pol_val_roll_fwd(),
    proj.check_accel_complement()))
print("        residual floor {}  carve-out {}  loans {}  net cf {}".format(
    proj.check_resid_floor(), proj.check_cv_carve_out(),
    proj.check_loan_roll_fwd(), proj.check_net_cf()))

model.close()
