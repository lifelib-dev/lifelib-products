"""Run the Index_DE_A reference model and print its cash flow statement.

    python products/indexpolice/run.py            # anchor cell (point_id = 1)
    python products/indexpolice/run.py 8          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Index_DE_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
df = proj.result_cf()

print("model point {}: {} - {}{} -> Rentenbeginn at {}, {} policy years "
      "(t = {} .. {})".format(
          point_id, proj.policy_id(), proj.sex(), proj.entry_age(),
          proj.ann_start_age(), len(df), proj.t_start(), proj.proj_len()))
print("premium form = {}   {:,.2f} EUR a year x {} years {} -> collected "
      "{:,.2f} EUR   Beitragssumme {:,.2f} EUR".format(
          proj.prem_form(), proj.prem_base_pp(proj.t_start()),
          proj.prem_term_y(), proj.prem_freq(),
          proj.prem_gross_pp(proj.t_start()), proj.prem_sum()))
print("payoff = {}   index = {}   Cap {:.2%} monthly   Quote {:.2%}   "
      "election = {}".format(
          proj.payoff_form(), proj.index_id(), proj.index_cap(proj.t_start()),
          proj.index_quote(proj.t_start()), proj.elect_id()))
print("guarantee = {:.0%} of Beitragssumme at i_g = {:.2%}   "
      "Beitragsgarantie {:,.2f} EUR   Stornoabzug {}".format(
          proj.guar_level(), proj.guar_rate(),
          proj.guar_level() * proj.prem_sum(),
          "on" if proj.surr_charge_on() else "off"))
print()
print(df.round(2).to_string())
print()
print("totals: premiums {:,.2f}  claims {:,.2f}  expenses {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["premiums"].sum(),
          df["claims_death"].sum() + df["claims_lapse"].sum()
          + df["claims_maturity"].sum(),
          df["expenses"].sum(), df["net_cf"].sum()))
print("credits: guaranteed interest {:,.2f}  safe arm {:,.2f}  index {:,.2f}  "
      "budget ratio {:.4f}".format(
          df["guar_int"].sum(), df["surplus_credit"].sum(),
          df["index_credit"].sum(), proj.index_budget_ratio()))
n = proj.proj_len()
print("at Rentenbeginn: account {:,.2f}  guaranteed capital {:,.2f}  "
      "benefit {:,.2f}  monthly Rente {:,.2f}".format(
          proj.av_pp(n + 1), proj.guar_cap_pp(n + 1), proj.mat_pp(n),
          proj.ann_monthly_pp()))
print("checks: net_cf {}  av roll fwd {}  pols roll fwd {}  surplus alloc {}  "
      "lock-in {}  index credit {}".format(
          proj.check_net_cf(), proj.check_av_roll_fwd(),
          proj.check_pols_roll_fwd(), proj.check_surplus_alloc(),
          proj.check_lock_in(), proj.check_index_credit()))

model.close()
