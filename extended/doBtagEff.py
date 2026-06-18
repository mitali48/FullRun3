import ROOT
import pandas as pd
import numpy as np
print(np.__version__)
import uproot
import subprocess
import matplotlib.pyplot as plt
import awkward as ak
print(ak.__version__)
print(np.__version__)

ROOT.EnableImplicitMT(8)

year = '2024'
#path_2022 = "/eos/user/s/sblancof/MC/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__sblancof__l2tight/nanoLatino_TTTo2L2Nu__part*.root" # 2022
#path_2022 = "/eos/user/s/sblancof/MC/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__sblancof__l2tight/nanoLatino_TTTo2L2Nu__part*.root" # 2022EE
#path_2022 = "/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__sblancof__l2tight/nanoLatino_TTTo2L2Nu__part*.root" # 2023
path_2022 = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer24_150x_nAODv15_Full2024v15/MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight/nanoLatino_TTTo2L2Nu__part*.root" # 2024

cmd = "find {}".format(path_2022)
fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
files = [fname.decode('ascii') for fname in fnames]

ROOT.gInterpreter.Declare('#include "/afs/cern.ch/user/m/misharma/private/condor_submit_area/include/headers.hh"')

df = ROOT.RDataFrame("Events", files[0:50])

_tmp = [
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 10.',
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'ptll>15',
    'mll > 12',
    # 'PuppiMET_pt>20' 
    'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
]

basic_sel = ' && '.join(_tmp)
df = df.Filter(basic_sel)

df = df.Define("MyCleanJet_pt", "CleanJet_pt[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_eta", "CleanJet_eta[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_jetIdx", "CleanJet_jetIdx[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_btagDeepFlavB", "Take(Jet_btagDeepFlavB, MyCleanJet_jetIdx)")
df = df.Define("MyCleanJet_btagPNetB", "Take(Jet_btagPNetB, MyCleanJet_jetIdx)")
if year == '2024':
    df = df.Define("Jet_btagRobustParTAK4B", "Jet_btagUParTAK4B")
df = df.Define("MyCleanJet_btagRobustParTAK4B", "Take(Jet_btagRobustParTAK4B, MyCleanJet_jetIdx)")
df = df.Define("MyCleanJet_hadronFlavour", "(ROOT::RVecI)Take(Jet_hadronFlavour, MyCleanJet_jetIdx)")

mydict = df.AsNumpy(["MyCleanJet_pt", "MyCleanJet_eta", "MyCleanJet_btagDeepFlavB", "MyCleanJet_btagPNetB", "MyCleanJet_btagRobustParTAK4B", "MyCleanJet_hadronFlavour"])

branches = ["MyCleanJet_pt", "MyCleanJet_eta", "MyCleanJet_btagDeepFlavB", "MyCleanJet_btagPNetB", "MyCleanJet_btagRobustParTAK4B", "MyCleanJet_hadronFlavour"]

def getBranchFlatten(events, branch):
    ak_array = [ak.Array(v) for v in events[branch]]
    np_array = ak.to_numpy(ak.flatten(ak_array))
    return np_array

df_np = {}
for key in branches:
    df_np[key] = getBranchFlatten(mydict, key)
df_ak = pd.DataFrame(df_np)

print("Save CSV file")
#df_ak.to_csv("/eos/user/s/sblancof/MC/Summer22_130x_nAODv12_Full2022v12/ttbar_2022_cleanjet.csv")
print("Saved!!")

pt_edges = np.array([   0.,   30.,   50.,   70.,  100.,  140.,  200.,  300.,  600., 1000.])
eta_edges = np.array([-2.5       , -1.47899997,  1.47899997,  2.5       ])

bjet_den = ROOT.TH2D("bjet_den", "bjet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_num = ROOT.TH2D("bjet_num", "bjet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_eff = ROOT.TH2D("bjet_eff", "bjet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

cjet_den = ROOT.TH2D("cjet_den", "cjet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_num = ROOT.TH2D("cjet_num", "cjet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_eff = ROOT.TH2D("cjet_eff", "cjet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

ljet_den = ROOT.TH2D("ljet_den", "ljet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_num = ROOT.TH2D("ljet_num", "ljet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_eff = ROOT.TH2D("ljet_eff", "ljet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

bjet_pnet_den = ROOT.TH2D("bjet_pnet_den", "bjet_pnet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_pnet_num = ROOT.TH2D("bjet_pnet_num", "bjet_pnet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_pnet_eff = ROOT.TH2D("bjet_pnet_eff", "bjet_pnet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

cjet_pnet_den = ROOT.TH2D("cjet_pnet_den", "cjet_pnet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_pnet_num = ROOT.TH2D("cjet_pnet_num", "cjet_pnet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_pnet_eff = ROOT.TH2D("cjet_pnet_eff", "cjet_pnet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

ljet_pnet_den = ROOT.TH2D("ljet_pnet_den", "ljet_pnet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_pnet_num = ROOT.TH2D("ljet_pnet_num", "ljet_pnet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_pnet_eff = ROOT.TH2D("ljet_pnet_eff", "ljet_pnet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

bjet_parT_den = ROOT.TH2D("bjet_parT_den", "bjet_parT_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_parT_num = ROOT.TH2D("bjet_parT_num", "bjet_parT_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_parT_eff = ROOT.TH2D("bjet_parT_eff", "bjet_parT_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

cjet_parT_den = ROOT.TH2D("cjet_parT_den", "cjet_parT_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_parT_num = ROOT.TH2D("cjet_parT_num", "cjet_parT_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_parT_eff = ROOT.TH2D("cjet_parT_eff", "cjet_parT_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

ljet_parT_den = ROOT.TH2D("ljet_parT_den", "ljet_parT_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_parT_num = ROOT.TH2D("ljet_parT_num", "ljet_parT_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_parT_eff = ROOT.TH2D("ljet_parT_eff", "ljet_parT_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

wp = {
    '2016': 0.0508,
    '2016_postVFP': 0.0480,
    '2017': 0.0532,
    '2018': 0.0490,
    '2022': 0.0583,
    '2022EE': 0.0614,
    '2023': 0.0479,
    '2023BPix': 0.048,
    '2024' : 0.048,
}

wp_pnet = {
    '2022': 0.047,
    '2022EE': 0.0499,
    '2023': 0.0358,
    '2023BPix': 0.0359,
    '2024': 0.0359,
}

wp_part = {
    '2022': 0.0849,
    '2022EE': 0.0897,
    '2023': 0.0681,
    '2023BPix': 0.0683,
    '2024': 0.0246,
}

total = len(df_ak)
for i in range(total):
    
    if (i%100000 == 0):
        print("Progress ---> " + str(100*i/total) + "%")
    
    jet_pt            = df_ak.loc[i].MyCleanJet_pt
    jet_eta           = df_ak.loc[i].MyCleanJet_eta
    jet_btagDeepFlavB = df_ak.loc[i].MyCleanJet_btagDeepFlavB
    jet_btagPNetB = df_ak.loc[i].MyCleanJet_btagPNetB
    jet_btagRobustParTAK4B = df_ak.loc[i].MyCleanJet_btagRobustParTAK4B
    jet_hadronFlavour = df_ak.loc[i].MyCleanJet_hadronFlavour
    
    if jet_hadronFlavour == 5:
        
        bjet_den.Fill(jet_pt, jet_eta)
        bjet_pnet_den.Fill(jet_pt, jet_eta)
        bjet_parT_den.Fill(jet_pt, jet_eta)
        
        if jet_btagDeepFlavB > wp[year]:
            bjet_num.Fill(jet_pt, jet_eta)

        if jet_btagPNetB > wp_pnet[year]:
            bjet_pnet_num.Fill(jet_pt, jet_eta)

        if jet_btagRobustParTAK4B > wp_part[year]:
            bjet_parT_num.Fill(jet_pt, jet_eta)
        
    elif jet_hadronFlavour == 4:
        
        cjet_den.Fill(jet_pt, jet_eta)
        cjet_pnet_den.Fill(jet_pt, jet_eta)
        cjet_parT_den.Fill(jet_pt, jet_eta)
        
        if jet_btagDeepFlavB > wp[year]:
            cjet_num.Fill(jet_pt, jet_eta)

        if jet_btagPNetB > wp_pnet[year]:
            cjet_pnet_num.Fill(jet_pt, jet_eta)

        if jet_btagRobustParTAK4B > wp_part[year]:
            cjet_parT_num.Fill(jet_pt, jet_eta)
            
    else:
        
        ljet_den.Fill(jet_pt, jet_eta)
        ljet_pnet_den.Fill(jet_pt, jet_eta)
        ljet_parT_den.Fill(jet_pt, jet_eta)
        
        if jet_btagDeepFlavB > wp[year]:
            ljet_num.Fill(jet_pt, jet_eta)

        if jet_btagPNetB > wp_pnet[year]:
            ljet_pnet_num.Fill(jet_pt, jet_eta)

        if jet_btagRobustParTAK4B > wp_part[year]:
            ljet_parT_num.Fill(jet_pt, jet_eta)

            
bjet_eff = bjet_num.Clone()
bjet_eff.Divide(bjet_den)

cjet_eff = cjet_num.Clone()
cjet_eff.Divide(cjet_den)

ljet_eff = ljet_num.Clone()
ljet_eff.Divide(ljet_den)


bjet_pnet_eff = bjet_pnet_num.Clone()
bjet_pnet_eff.Divide(bjet_pnet_den)

cjet_pnet_eff = cjet_pnet_num.Clone()
cjet_pnet_eff.Divide(cjet_pnet_den)

ljet_pnet_eff = ljet_pnet_num.Clone()
ljet_pnet_eff.Divide(ljet_pnet_den)


bjet_parT_eff = bjet_parT_num.Clone()
bjet_parT_eff.Divide(bjet_parT_den)

cjet_parT_eff = cjet_parT_num.Clone()
cjet_parT_eff.Divide(cjet_parT_den)

ljet_parT_eff = ljet_parT_num.Clone()
ljet_parT_eff.Divide(ljet_parT_den)

file = ROOT.TFile(f"bTagEff_{year}_ttbar_loose.root", "RECREATE")
file.cd()

bjet_den.Clone().Write("bjet_den")
bjet_num.Clone().Write("bjet_num")
bjet_eff.Clone().Write("bjet_eff")

cjet_den.Clone().Write("cjet_den")
cjet_num.Clone().Write("cjet_num")
cjet_eff.Clone().Write("cjet_eff")

ljet_den.Clone().Write("ljet_den")
ljet_num.Clone().Write("ljet_num")
ljet_eff.Clone().Write("ljet_eff")


bjet_pnet_den.Clone().Write("bjet_pnet_den")
bjet_pnet_num.Clone().Write("bjet_pnet_num")
bjet_pnet_eff.Clone().Write("bjet_pnet_eff")

cjet_pnet_den.Clone().Write("cjet_pnet_den")
cjet_pnet_num.Clone().Write("cjet_pnet_num")
cjet_pnet_eff.Clone().Write("cjet_pnet_eff")

ljet_pnet_den.Clone().Write("ljet_pnet_den")
ljet_pnet_num.Clone().Write("ljet_pnet_num")
ljet_pnet_eff.Clone().Write("ljet_pnet_eff")


bjet_parT_den.Clone().Write("bjet_parT_den")
bjet_parT_num.Clone().Write("bjet_parT_num")
bjet_parT_eff.Clone().Write("bjet_parT_eff")

cjet_parT_den.Clone().Write("cjet_parT_den")
cjet_parT_num.Clone().Write("cjet_parT_num")
cjet_parT_eff.Clone().Write("cjet_parT_eff")

ljet_parT_den.Clone().Write("ljet_parT_den")
ljet_parT_num.Clone().Write("ljet_parT_num")
ljet_parT_eff.Clone().Write("ljet_parT_eff")

file.Close()
            
            
