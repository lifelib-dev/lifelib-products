"""Run the Riester_DE_A reference model and print its cash flow statement.

    python products/riester_rente/run.py            # anchor cell (point_id = 1)
    python products/riester_rente/run.py 11         # another model point

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx

model = mx.read_model(Path(__file__).parent / "Riester_DE_A")
point_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

proj = model.Projection[point_id]
print("model point {}: {}{} concluded at age {}, in force {} years, "
      "Rentenbeginn {}".format(
          point_id, proj.sex(), proj.age(1), proj.issue_age(),
          proj.duration_init(), proj.rentenbeginn_age()))
print("contribution form = {} ({}), contrib_ratio = {:.2f}, "
      "frequency = {} (phi = {:.4f}), bfs_year = {}".format(
          proj.contrib_form(), proj.income_id(), proj.contrib_ratio(),
          proj.prem_freq(), proj.prem_freq_load(), proj.bfs_year()))
print("t = 1 .. {}, conversion at t = {} (age {}, calendar {}), "
      "rechnungszins = {:.4f}, scenario = {}".format(
          proj.proj_len(), proj.t_conv(), proj.age(proj.t_conv()),
          proj.calendar_year(proj.t_conv()), proj.rechnungszins(),
          proj.scenario_id()))
print("opening: av_pp = {:,.2f}  guar_pp = {:,.2f}  "
      "garantieluecke_pp = {:,.2f}".format(
          proj.av_pp(1), proj.guar_pp(1), proj.garantieluecke_pp(1)))
print()
print("conversion: account {:,.2f}  guarantee {:,.2f}  capital {:,.2f}  "
      "Garantieluecke {:,.2f}".format(
          proj.account_conv_pp(), proj.guar_pp(proj.t_conv() + 1),
          proj.capital_conv_pp(), proj.garantieluecke_conv_pp()))
print("            ann_factor {:.8f}  rentenfaktor curr {:.6f} / guar {:.2f} "
      "-> applied {:.6f}".format(
          proj.ann_factor(), proj.rentenfaktor_curr(),
          proj.rentenfaktor_guar(), proj.rentenfaktor_applied()))
print("            Kleinbetragsrente {}  Teilkapital {:,.2f}  "
      "Abfindung {:,.2f}  annuity {:,.2f} p.a.".format(
          proj.is_kleinbetrag(), proj.teilkapital_pp(),
          proj.commutation_pp(), proj.annuity_pp(proj.t_conv())))
print()
df = proj.result_cf()
print(df.head(20).round(2).to_string())
print()
print("totals over {} years: premiums {:,.2f}  zulagen {:,.2f}  "
      "claims {:,.2f}".format(
          proj.proj_len(), df["premiums"].sum(), df["zulagen"].sum(),
          df[["claims_death", "claims_lapse", "claims_transfer",
              "claims_lumpsum", "claims_commutation",
              "claims_annuity"]].to_numpy().sum()))
print("                     expenses {:,.2f}  commissions {:,.2f}  "
      "net_cf {:,.2f}".format(
          df["expenses"].sum(), df["commissions"].sum(), df["net_cf"].sum()))
print("checks: net_cf {}  av {}  guar {}  pols {}  conversion {}  "
      "zulage lag {}".format(
          proj.check_net_cf(), proj.check_av_roll_fwd(),
          proj.check_guar_roll_fwd(), proj.check_pols_roll_fwd(),
          proj.check_conversion(), proj.check_zulage_lag()))

model.close()
