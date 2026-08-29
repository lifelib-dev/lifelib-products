"""Run the RV_DE_A reference model and print its cash flow statement.

    python products/klassische_rentenversicherung/run.py       # anchor cell (point_id = 1)
    python products/klassische_rentenversicherung/run.py 6     # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "RV_DE_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
mp = proj.model_point()
n = int(mp["aufschub_y"])

print("model point {}: {} - {}{} issued {}, duration {}, {} EUR {} to age {}".format(
    point_id, mp["policy_id"], mp["sex"], mp["issue_age"], mp["issue_year"],
    mp["duration_init"], mp["premium_form"], mp["prem_freq"],
    int(mp["issue_age"]) + n))
print("premium {:,.2f} EUR p.a. x {} y (freq load {:.3f})   Beitragssumme {:,.2f}   "
      "alpha {:,.2f}".format(
          proj.prem_pp(int(mp["duration_init"]) + 1), mp["prem_term_y"],
          proj.freq_load(), proj.beitragssumme_pp(), proj.alpha_total_pp()))
print("Rechnungszins {:.2%}   declared {:.2%}   bonus {:.2%}   charge set {}".format(
    proj.int_rate_guar(), proj.decl_rate(int(mp["duration_init"]) + 1),
    proj.bonus_rate(int(mp["duration_init"]) + 1), mp["charge_id"]))
print("Rentenbeginn t = {} (age {}):  capital {:,.2f}  Rentenfaktor max({:.2f}, {:.2f}) "
      "= {:.2f}  ->  garantierte Rente {:,.2f} EUR/month".format(
          n, int(mp["issue_age"]) + n, proj.capital_conv_pp(),
          proj.annuity_rate_guar(), proj.annuity_rate_curr(),
          proj.annuity_rate_appl(), proj.annuity_guar_mth_pp()))
print("Rentengarantiezeit {} y   Kapitalwahl {:.0%}   payout system {}   "
      "proj_len {}".format(
          mp["rgz_years"], float(mp["kapitalwahl_rate"]), mp["payout_system"],
          proj.proj_len()))
print()

df = proj.result_cf()
print(df.head(20).round(2).to_string())
print()
print("totals over t = {} .. {}: premiums {:,.2f}  claims {:,.2f}  annuity {:,.2f}  "
      "expenses {:,.2f}  net_cf {:,.2f}".format(
          df.index[0], df.index[-1],
          df["premiums"].sum(),
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_commutation"].sum(),
          df["annuity_payments"].sum(), df["expenses"].sum(),
          df["net_cf"].sum()))
print("checks: net_cf {}  pols {}  closure {}  av {}  av_sur {}  prem split {}  "
      "cv floor {}  conversion {}  annuity guarantee {}".format(
          proj.check_net_cf(), proj.check_pols_roll_fwd(),
          proj.check_decrement_closure(), proj.check_av_roll_fwd(),
          proj.check_av_sur_roll_fwd(), proj.check_prem_split(),
          proj.check_cv_floor(), proj.check_annuity_conv(),
          proj.check_annuity_guarantee()))

model.close()
