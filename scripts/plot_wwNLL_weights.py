#!/usr/bin/env python3
import ROOT, os

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

indir="/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum"
outdir="plots_wwNLL_weights"
os.makedirs(outdir, exist_ok=True)

ROOT.gStyle.SetTitleSize(0.045,"XY")
ROOT.gStyle.SetLabelSize(0.04,"XY")
ROOT.gStyle.SetPadGridX(True)
ROOT.gStyle.SetPadGridY(True)

def read_graph(name):
    return ROOT.TGraph(os.path.join(indir,name))

import ctypes

def multiply(g1, g2):

    g = ROOT.TGraph()

    x = ctypes.c_double()
    y1 = ctypes.c_double()
    y2 = ctypes.c_double()

    n = min(g1.GetN(), g2.GetN())

    for i in range(n):

        g1.GetPoint(i, x, y1)
        g2.GetPoint(i, x, y2)

        g.SetPoint(i, x.value, y1.value * y2.value)

    return g

    
central=read_graph("central.dat")
scaleUp=read_graph("scale_up.dat")
scaleDown=read_graph("scale_down.dat")
resumUp=read_graph("resum_up.dat")
resumDown=read_graph("resum_down.dat")

qUp=multiply(central,scaleUp)
qDown=multiply(central,scaleDown)
rUp=multiply(central,resumUp)
rDown=multiply(central,resumDown)

colors={
"Central":ROOT.kBlack,
"Scale Up":ROOT.kRed+1,
"Scale Down":ROOT.kBlue+1,
"Resum Up":ROOT.kGreen+2,
"Resum Down":ROOT.kMagenta+2,
"Q Up":ROOT.kRed+1,
"Q Down":ROOT.kBlue+1,
"R Up":ROOT.kGreen+2,
"R Down":ROOT.kMagenta+2,
}

styles={
"Central":1,
"Scale Up":2,
"Scale Down":2,
"Resum Up":3,
"Resum Down":3,
"Q Up":2,
"Q Down":2,
"R Up":3,
"R Down":3,
}

def style(graph,name):
    graph.SetLineColor(colors[name])
    graph.SetLineStyle(styles[name])
    graph.SetLineWidth(3)

def yrange(graphs):
    ymin=1e9
    ymax=-1e9
    for g in graphs:
        for i in range(g.GetN()):
            y = g.GetPointY(i)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    return ymin*0.95,ymax*1.05

def draw_set(graphdict,title,ytitle,prefix,logx=False,ratio=False):
    for n,g in graphdict.items():
        style(g,n)
    ymin = 1e9
    ymax = -1e9

    for g in graphdict.values():
        for i in range(g.GetN()):
            y = g.GetPointY(i)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

    margin = 0.08*(ymax-ymin)

    ymin -= margin
    ymax += margin
    if ratio:
        ymin=0.70
        ymax=1.35

    for xmax,label in [(500,"0to500"),(60,"0to60")]:
        c=ROOT.TCanvas(f"{prefix}_{label}","",900,700)
        c.SetLeftMargin(0.12)
        c.SetBottomMargin(0.12)
        c.SetGrid()
        if logx:
            c.SetLogx()

        first=list(graphdict.values())[0]
        first.SetTitle(title)
        first.GetXaxis().SetTitle("p_{T}^{WW} [GeV]")
        first.GetYaxis().SetTitle(ytitle)
        first.GetXaxis().SetLimits(0.2,xmax)
        first.GetYaxis().SetRangeUser(ymin,ymax)
        first.Draw("AL")

        for g in list(graphdict.values())[1:]:
            g.Draw("L SAME")

        leg=ROOT.TLegend(0.58,0.64,0.88,0.88)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        for n,g in graphdict.items():
            leg.AddEntry(g,n,"l")
        leg.Draw()

        c.SaveAs(os.path.join(outdir,f"{prefix}_{label}.pdf"))
        c.SaveAs(os.path.join(outdir,f"{prefix}_{label}.png"))

# Plot 1
draw_set({
"Central":central,
"Scale Up":scaleUp,
"Scale Down":scaleDown,
"Resum Up":resumUp,
"Resum Down":resumDown},
"WW NLL Input Tables","Input value","wwNLL_inputs",logx=False)

# Plot 2
draw_set({
"Central":central,
"Q Up":qUp,
"Q Down":qDown,
"R Up":rUp,
"R Down":rDown},
"WW NLL Event Weights","Event weight","wwNLL_eventWeights",logx=False)

# Plot 3
one=ROOT.TGraph()
for i in range(central.GetN()):
    one.SetPoint(i, central.GetPointX(i), 1.0)

draw_set({
"Central":one,
"Scale Up":scaleUp,
"Scale Down":scaleDown,
"Resum Up":resumUp,
"Resum Down":resumDown},
"WW NLL Relative Variations","Variation / Central","wwNLL_relativeVariations",logx=False,ratio=True)

print("Finished. Plots written to",outdir)