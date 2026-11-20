#!/usr/bin/env python3
"""
Plot a nominal histogram together with nuisance Up/Down variations and
their ratios to the nominal histogram.

Example:
  python plot_qcd_norm.py \
      -f mkShapes__ltr1_NormTheoryUnc_test.root \
      -c All_incl -v events -p WW -n QCDscale_WW \
      -o plots

For a nuisance whose histograms are named:
  histo_WW_QCDscale_WWUp
  histo_WW_QCDscale_WWDown

The nominal histogram is expected to be named:
  histo_WW
"""

import argparse
import os
import sys

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot nominal and nuisance Up/Down histograms with ratios."
    )
    parser.add_argument("-f", "--file", required=True,
                        help="Input ROOT file")
    parser.add_argument("-c", "--category", default="All_incl",
                        help="Directory/category inside the ROOT file (default: All_incl)")
    parser.add_argument("-v", "--variable", default="events",
                        help="Variable directory inside the category (default: events)")
    parser.add_argument("-p", "--process", default="WW",
                        help="Process name (default: WW)")
    parser.add_argument("-n", "--nuisance", required=True,
                        help="Nuisance name without Up/Down suffix")
    parser.add_argument("-o", "--outdir", default=".",
                        help="Output directory for plots (default: current directory)")
    parser.add_argument("--y-title", default="Events",
                        help="Y-axis title for the upper panel")
    parser.add_argument("--ratio-min", type=float, default=0.9,
                        help="Minimum ratio-panel range (default: 0.9)")
    parser.add_argument("--ratio-max", type=float, default=1.1,
                        help="Maximum ratio-panel range (default: 1.1)")
    parser.add_argument("--log-y", action="store_true",
                        help="Use a logarithmic y-axis in the upper panel")
    parser.add_argument("--formats", nargs="+", default=["png", "pdf"],
                        choices=["png", "pdf", "root"],
                        help="Output formats (default: png pdf)")
    return parser.parse_args()


def get_histogram(directory, name):
    hist = directory.Get(name)
    if not hist:
        raise RuntimeError(
            "Histogram '{}' was not found in the requested ROOT directory.".format(name)
        )
    # Detach from the file so the histogram remains valid after file closure.
    hist = hist.Clone(name + "_plot")
    hist.SetDirectory(0)
    return hist


def make_plot(nominal, up, down, args):
    # Check binning before doing bin-by-bin ratios.
    if (nominal.GetNbinsX() != up.GetNbinsX()
            or nominal.GetNbinsX() != down.GetNbinsX()):
        raise RuntimeError("Nominal, Up and Down histograms have different bin counts.")

    for hist in (up, down):
        if not nominal.GetXaxis().GetXbins().GetSize():
            # For uniform binning, compare axis limits as well.
            if (abs(hist.GetXaxis().GetXmin() - nominal.GetXaxis().GetXmin()) > 1e-9
                    or abs(hist.GetXaxis().GetXmax() - nominal.GetXaxis().GetXmax()) > 1e-9):
                raise RuntimeError("Nominal, Up and Down histograms have different x ranges.")

    # Styling
    nominal.SetLineColor(ROOT.kBlack)
    nominal.SetMarkerColor(ROOT.kBlack)
    nominal.SetMarkerStyle(20)
    nominal.SetMarkerSize(0.8)
    nominal.SetLineWidth(2)

    up.SetLineColor(ROOT.kRed + 1)
    up.SetMarkerColor(ROOT.kRed + 1)
    up.SetLineWidth(2)
    up.SetLineStyle(2)

    down.SetLineColor(ROOT.kBlue + 1)
    down.SetMarkerColor(ROOT.kBlue + 1)
    down.SetLineWidth(2)
    down.SetLineStyle(2)

    # Ratios: Up/Nominal and Down/Nominal.
    ratio_up = up.Clone("ratio_up")
    ratio_down = down.Clone("ratio_down")
    ratio_up.SetDirectory(0)
    ratio_down.SetDirectory(0)
    ratio_up.Divide(nominal)
    ratio_down.Divide(nominal)

    ratio_up.SetLineColor(ROOT.kRed + 1)
    ratio_up.SetMarkerColor(ROOT.kRed + 1)
    ratio_up.SetLineWidth(2)
    ratio_up.SetMarkerStyle(24)

    ratio_down.SetLineColor(ROOT.kBlue + 1)
    ratio_down.SetMarkerColor(ROOT.kBlue + 1)
    ratio_down.SetLineWidth(2)
    ratio_down.SetMarkerStyle(25)

    # Canvas and pads
    canvas = ROOT.TCanvas("c_" + args.nuisance, "Nuisance comparison", 800, 800)
    top = ROOT.TPad("top", "top", 0.0, 0.30, 1.0, 1.0)
    bottom = ROOT.TPad("bottom", "bottom", 0.0, 0.0, 1.0, 0.30)

    top.SetBottomMargin(0.03)
    top.SetLeftMargin(0.13)
    top.SetRightMargin(0.05)
    bottom.SetTopMargin(0.03)
    bottom.SetBottomMargin(0.35)
    bottom.SetLeftMargin(0.13)
    bottom.SetRightMargin(0.05)

    if args.log_y:
        top.SetLogy()

    top.Draw()
    bottom.Draw()

    # Upper panel
    top.cd()
    nominal.SetTitle("")
    nominal.GetYaxis().SetTitle(args.y_title)
    nominal.GetYaxis().SetTitleSize(0.05)
    nominal.GetYaxis().SetTitleOffset(1.15)
    nominal.GetYaxis().SetLabelSize(0.045)
    nominal.GetXaxis().SetLabelSize(0)
    nominal.GetXaxis().SetTitle("")

    max_value = max(nominal.GetMaximum(), up.GetMaximum(), down.GetMaximum())
    min_value = min(nominal.GetMinimum(), up.GetMinimum(), down.GetMinimum())
    nominal.SetMaximum(max_value * (5.0 if args.log_y else 1.05))
    if args.log_y:
        positive_values = [
            h.GetMinimum() for h in (nominal, up, down) if h.GetMinimum() > 0
        ]
        nominal.SetMinimum(max(min(positive_values) * 0.5, 1e-5) if positive_values else 1e-3)
    else:
        nominal.SetMinimum(min_value /1.05)
        
        # nominal.SetMinimum(min(0.0, min_value * 1.2))

    nominal.Draw("E1")
    up.Draw("HIST SAME")
    down.Draw("HIST SAME")
    # Draw nominal points on top of the variation lines.
    nominal.Draw("E1 SAME")

    legend = ROOT.TLegend(0.60, 0.70, 0.93, 0.90)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(nominal, "Nominal", "lep")
    legend.AddEntry(up, "Up", "l")
    legend.AddEntry(down, "Down", "l")
    legend.Draw()

    label = ROOT.TLatex()
    label.SetNDC(True)
    label.SetTextSize(0.035)
    label.DrawLatex(0.14, 0.94, "{}  |  {}".format(args.category, args.variable))
    label.DrawLatex(0.14, 0.89, "{}  |  {}".format(args.process, args.nuisance))

    # Lower panel
    bottom.cd()
    frame = ratio_up.Clone("ratio_frame")
    frame.Reset("ICES")
    frame.SetTitle("")
    frame.GetYaxis().SetTitle("Variation / Nominal")
    frame.GetYaxis().SetNdivisions(505)
    frame.GetYaxis().SetTitleSize(0.11)
    frame.GetYaxis().SetTitleOffset(0.52)
    frame.GetYaxis().SetLabelSize(0.10)
    frame.GetXaxis().SetTitle(nominal.GetXaxis().GetTitle() or args.variable)
    frame.GetXaxis().SetTitleSize(0.13)
    frame.GetXaxis().SetTitleOffset(1.05)
    frame.GetXaxis().SetLabelSize(0.11)
    frame.SetMinimum(args.ratio_min)
    frame.SetMaximum(args.ratio_max)
    frame.Draw("AXIS")

    unity = ROOT.TLine(
        nominal.GetXaxis().GetXmin(), 1.0,
        nominal.GetXaxis().GetXmax(), 1.0
    )
    unity.SetLineColor(ROOT.kBlack)
    unity.SetLineStyle(2)
    unity.SetLineWidth(2)
    unity.Draw("SAME")

    ratio_up.Draw("E1 SAME")
    ratio_down.Draw("E1 SAME")

    canvas.cd()
    canvas.Update()

    os.makedirs(args.outdir, exist_ok=True)
    base = "{}_{}_{}_{}".format(
        args.process, args.nuisance, args.category, args.variable
    )
    for extension in args.formats:
        output_path = os.path.join(args.outdir, base + "." + extension)
        canvas.SaveAs(output_path)
        print("Saved:", output_path)

    return canvas


def main():
    args = parse_args()

    if not os.path.isfile(args.file):
        raise FileNotFoundError("Input ROOT file does not exist: {}".format(args.file))

    root_file = ROOT.TFile.Open(args.file, "READ")
    if not root_file or root_file.IsZombie():
        raise RuntimeError("Could not open ROOT file: {}".format(args.file))

    directory_path = "{}/{}/{}".format(
        args.category.strip("/"),
        args.variable.strip("/"),
        ""
    ).rstrip("/")
    directory = root_file.Get(directory_path)
    if not directory:
        root_file.Close()
        raise RuntimeError(
            "ROOT directory '{}' was not found in {}".format(directory_path, args.file)
        )

    nominal_name = "histo_{}".format(args.process)
    up_name = "histo_{}_{}Up".format(args.process, args.nuisance)
    down_name = "histo_{}_{}Down".format(args.process, args.nuisance)

    try:
        nominal = get_histogram(directory, nominal_name)
        up = get_histogram(directory, up_name)
        down = get_histogram(directory, down_name)
        make_plot(nominal, up, down, args)
    finally:
        root_file.Close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(1)
