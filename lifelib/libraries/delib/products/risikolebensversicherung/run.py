"""Run the RLV_DE_A reference model and print its cash flow statement.

    python products/risikolebensversicherung/run.py            # anchor cell (point_id = 1)
    python products/risikolebensversicherung/run.py 8          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "RLV_DE_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {} - {}{} {}{} - Versicherungssumme {:,.0f} EUR {}, "
      "cover {} y to age {}, premiums {} y".format(
          point_id, proj.model_point()["policy_id"], proj.sex(),
          proj.issue_age(), proj.smoker(),
          "" if proj.lives() == 1 else " + {}{} (verbundene Leben)".format(
              proj.issue_age2(), proj.smoker2()),
          proj.sum_assured(), proj.benefit_schedule_id(),
          proj.policy_term(), proj.cover_end_age(), proj.prem_term()))
print("premium form = {}   Zahlweise = {} ({} instalments, load {:.3f})   "
      "surplus = {}".format(
          proj.premium_form(), proj.prem_freq(), proj.instalments(),
          proj.prem_freq_load(), proj.surplus_form()))
print("rating factor = {:.2f}   NVG schedule = {}   duration = {} y   "
      "frame t = {} .. {}".format(
          proj.rating_factor(), proj.nvg_schedule_id(), proj.duration_y(),
          proj.proj_start(), proj.proj_len()))
print()
print("Bruttobeitrag  G  = {:,.4f} EUR   Nettopraemie Gn = {:,.4f} EUR".format(
    proj.prem_gross_level_pp(), proj.prem_net_level_pp()))
print("Beitragsverrechnungssatz v_d = {:.8f}   Zahlbeitrag = {:,.4f} EUR   "
      "Zahl/Brutto = {:.6f}".format(
          proj.beitragsverrechnung_rate(), proj.prem_paid_pp(1),
          proj.prem_paid_pp(1) / proj.prem_gross_pp(1)))
print()
df = proj.result_cf()
print(df.head(12).round(2).to_string())
print()
print("totals over {} years: prem_gross {:,.2f}  premiums {:,.2f}  "
      "prem_rebate {:,.2f}".format(
          len(df), df["prem_gross"].sum(), df["premiums"].sum(),
          df["prem_rebate"].sum()))
print("                      claims {:,.2f}  expenses {:,.2f}  "
      "commissions {:,.2f}  net_cf {:,.2f}".format(
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_maturity"].sum(),
          df["expenses"].sum(), df["commissions"].sum(), df["net_cf"].sum()))
print("decrements: deaths {:.8f}  lapses {:.8f}  expiries {:.8f}".format(
    sum(proj.pols_death(t) for t in range(proj.proj_start(), proj.proj_len() + 1)),
    sum(proj.pols_lapse(t) for t in range(proj.proj_start(), proj.proj_len() + 1)),
    proj.pols_maturity(proj.proj_len())))
print("checks: net_cf {}  pols roll fwd {}  prem split {}  "
      "reserve roll fwd {}  no cash value {}".format(
          proj.check_net_cf(), proj.check_pols_roll_fwd(),
          proj.check_prem_split(), proj.check_res_roll_fwd(),
          proj.check_no_cash_value()))

model.close()
