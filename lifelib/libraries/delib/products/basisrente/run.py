"""Run the Basis_DE_A reference model and print its cash flow statement.

    python products/basisrente/run.py            # anchor cell (point_id = 1)
    python products/basisrente/run.py 5          # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Basis_DE_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
mp = proj.model_point()
print("model point {}: {} - {}{} concluded {}, duration {} at valuation".format(
    point_id, mp["policy_id"], proj.model_point()["sex"], proj.age(1),
    mp["conclusion_year"], proj.duration(1)))
print("Aufschubphase to Rentenbeginn at age {} (t = {}), projection to age {} "
      "(t = {})".format(
          mp["ret_age"], proj.ret_t(), proj.omega_age(), proj.proj_len()))
print("premium form = {} {}   Beitrag {:,.2f} EUR p.a. x freq load {:.3f}   "
      "Dynamik {:.1%}".format(
          mp["prem_form"], mp["prem_mode"], mp["prem_base_pp"],
          proj.prem_freq_load(), mp["prem_dyn_rate"]))
print("Beitragssumme {:,.2f} EUR   Zillmerung {:,.2f} EUR over {} years   "
      "Zuzahlung {:,.2f} EUR p.a. to duration {}".format(
          proj.beitragssumme_pp(), proj.alpha_total_pp(), proj.zill_spread_y,
          mp["zuzahlung_pp"], mp["zuzahlung_end_dur"]))
print("Rentenfaktor: guaranteed {:.2f}, current {:.2f}, option factor {:.3f} "
      "-> applied {:.4f}".format(
          mp["rentenfaktor_gtd"], proj.rentenfaktor_curr(),
          proj.rf_option_factor(), proj.rentenfaktor_applied()))
if proj.ret_t() >= 1:
    print("fund at Rentenbeginn {:,.2f} EUR -> annuity {:,.2f} EUR p.a. per "
          "annuitant".format(proj.fund_at_conv(), proj.ann_pp(proj.ret_t())))
else:
    print("opens in payment: annuity {:,.2f} EUR p.a. per annuitant".format(
        proj.ann_pp(1)))
print()

df = proj.result_cf()
head = df.head(8).round(2)
print(head.to_string())
print("...")
if proj.ret_t() >= 1:
    lo = max(1, proj.ret_t() - 1)
    print(df.loc[lo:lo + 3].round(2).to_string())
    print("...")
print()
print("totals over {} years: premiums {:,.2f}  Zuzahlungen {:,.2f}  "
      "annuities {:,.2f}".format(
          proj.proj_len(), df["premiums"].sum(), df["zuzahlungen"].sum(),
          df["claims_annuity"].sum()))
print("                      death {:,.2f}  survivor {:,.2f}  expenses {:,.2f}  "
      "commissions {:,.2f}".format(
          df["claims_death"].sum(), df["claims_survivor"].sum(),
          df["expenses"].sum(), df["commissions"].sum()))
print("                      net_cf {:,.2f}  liability_cf {:,.2f}".format(
    df["net_cf"].sum(), df["liability_cf"].sum()))
print("checks: net_cf {}  pols roll fwd {}  av roll fwd {}".format(
    proj.check_net_cf(), proj.check_pols_roll_fwd(), proj.check_av_roll_fwd()))
print("        conversion {}  no capital {}  annuity roll fwd {}".format(
    proj.check_conversion(), proj.check_no_capital(),
    proj.check_annuity_roll_fwd()))

model.close()
