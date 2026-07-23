import ROOT
import argparse
import os

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", required=True)
parser.add_argument("-c", "--category", default="SR_0j")
parser.add_argument("-v", "--variable", default="events")
parser.add_argument("-p", "--process", default="WW")
parser.add_argument("-n", "--nuisance", required=True)
parser.add_argument( "-o", "--outdir", default=".", help="Directory to save the output plots")


args = parser.parse_args()
os.makedirs(args.outdir, exist_ok=True)

f = ROOT.TFile.Open(args.file)
d = f.Get(f"{args.category}/{args.variable}")

nom  = d.Get(f"histo_{args.process}")
up   = d.Get(f"histo_{args.process}_{args.nuisance}Up")
down = d.Get(f"histo_{args.process}_{args.nuisance}Down")

for h in [nom, up, down]:
    if not h:
        raise RuntimeError("Histogram missing")

# ------------------------------------------------------------
# Style
# ------------------------------------------------------------

nom.SetLineColor(ROOT.kBlack)
up.SetLineColor(ROOT.kRed + 1)
down.SetLineColor(ROOT.kBlue + 1)

nom.SetLineWidth(2)
up.SetLineWidth(2)
down.SetLineWidth(2)

# ------------------------------------------------------------
# Y-axis range
# ------------------------------------------------------------

ymin = min(nom.GetMinimum(), up.GetMinimum(), down.GetMinimum())

if ymin > 0:
    nom.SetMinimum(0.9995 * ymin)
else:
    nom.SetMinimum(1.0005 * ymin)

nom.SetMaximum(
    1.0005 * max(
        nom.GetMaximum(),
        up.GetMaximum(),
        down.GetMaximum(),
    )
)

# ------------------------------------------------------------
# Canvas
# ------------------------------------------------------------

c = ROOT.TCanvas("c", "", 800, 800)

pad1 = ROOT.TPad("pad1", "", 0.0, 0.30, 1.0, 1.0)
pad2 = ROOT.TPad("pad2", "", 0.0, 0.00, 1.0, 0.30)

pad1.SetBottomMargin(0.02)

pad2.SetTopMargin(0.03)
pad2.SetBottomMargin(0.35)
pad2.SetGridy()

pad1.Draw()
pad2.Draw()

# ------------------------------------------------------------
# Top pad
# ------------------------------------------------------------

pad1.cd()

title = f"{args.category}_{args.variable}_{args.process}_{args.nuisance}"

nom.SetTitle(title)

nom.GetXaxis().SetLabelSize(0)
nom.GetXaxis().SetTitle("")

nom.GetYaxis().SetTitle("Events")
nom.GetYaxis().SetTitleSize(0.05)
nom.GetYaxis().SetLabelSize(0.04)

nom.Draw("hist")
up.Draw("hist same")
down.Draw("hist same")

leg = ROOT.TLegend(0.62, 0.72, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillStyle(0)

leg.AddEntry(nom, "Nominal", "l")
leg.AddEntry(up, "Up", "l")
leg.AddEntry(down, "Down", "l")

leg.Draw()

# ------------------------------------------------------------
# Ratio histograms
# ------------------------------------------------------------

pad2.cd()

ratioNom = nom.Clone("ratioNom")
ratioUp = up.Clone("ratioUp")
ratioDown = down.Clone("ratioDown")

for i in range(1, nom.GetNbinsX() + 1):

    n = nom.GetBinContent(i)

    if n != 0:

        ratioNom.SetBinContent(i, 1.0)
        ratioNom.SetBinError(i, 0.0)

        ratioUp.SetBinContent(i, up.GetBinContent(i) / n)
        ratioDown.SetBinContent(i, down.GetBinContent(i) / n)

        ratioUp.SetBinError(i, 0.0)
        ratioDown.SetBinError(i, 0.0)

    else:

        ratioNom.SetBinContent(i, 0.0)
        ratioUp.SetBinContent(i, 0.0)
        ratioDown.SetBinContent(i, 0.0)

ratioNom.SetLineColor(ROOT.kBlack)
ratioUp.SetLineColor(ROOT.kRed + 1)
ratioDown.SetLineColor(ROOT.kBlue + 1)

ratioNom.SetLineWidth(2)
ratioUp.SetLineWidth(2)
ratioDown.SetLineWidth(2)

ratioNom.SetTitle("")

ratioNom.GetYaxis().SetTitle("Variation/Nom.")

ratioNom.GetYaxis().CenterTitle()

ratioNom.GetYaxis().SetTitleSize(0.09)
ratioNom.GetYaxis().SetTitleOffset(0.50)
ratioNom.GetYaxis().SetLabelSize(0.08)
ratioNom.GetYaxis().SetNdivisions(505)

ratioNom.GetXaxis().SetTitle(args.variable)
ratioNom.GetXaxis().SetTitleSize(0.12)
ratioNom.GetXaxis().SetTitleOffset(1.10)
ratioNom.GetXaxis().SetLabelSize(0.10)

# Fixed CMS-style ratio range
ratioNom.SetMinimum(0.9)
ratioNom.SetMaximum(1.1)

ratioNom.Draw("hist")
ratioUp.Draw("hist same")
ratioDown.Draw("hist same")

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

c.cd()

out = os.path.join(
    args.outdir,
    f"{args.category}_{args.variable}_{args.process}_{args.nuisance}"
)

c.SaveAs(out + ".pdf")
c.SaveAs(out + ".png")